"""CLI Runner —— 封装 graph.stream + Rich 实时渲染 + HITL"""

import re
from pathlib import Path
from typing import Any, Dict

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree

from ..runner import build_runnable_graph, build_runtime_config, create_initial_state
from ..state import AgentContext
from ..tracing import flush_langfuse
from ..input_filter import clean_input, is_meaningful
from ..message_utils import get_message_content

console = Console()

NODE_NAMES = [
    "requirement_parser",
    "context_retriever",
    "planner",
    "generator",
    "sandbox_executor",
]

NODE_OUTPUT_KEYS = {
    "requirement_parser": "parsed_requirement",
    "context_retriever": "context",
    "planner": "case_plan",
    "generator": "generated_code",
    "sandbox_executor": "execution_result",
}

# ✅ 修复 1：取消注释，放到全局作用域
HITL_NODES = {"planner"}

_CODE_PREVIEW_CHARS = 2000
_CODE_SAVE_DIR = "output"


def _extract_code_from_messages(node_output: Dict[str, Any]) -> str:
    msgs = node_output.get("messages", [])
    if not msgs:
        return ""
    raw = get_message_content(msgs[-1])
    m = re.search(r"```python\s*(.*?)\s*```", raw, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"```\s*(.*?)\s*```", raw, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""


def _extract_summary(node_name: str, node_output: Dict[str, Any]) -> str:
    if node_name == "sandbox_executor":
        result = node_output.get("execution_result", {})
        if isinstance(result, dict):
            status = result.get("status", "unknown")
            stage = result.get("stage", "unknown")
            exit_code = result.get("exit_code", "unknown")
            return f"沙盒执行 {status}, stage={stage}, exit_code={exit_code}"
        return "沙盒执行完成"

    if node_name == "generator":
        code = (
            node_output.get("generated_code")
            or node_output.get("code")
            or _extract_code_from_messages(node_output)
        )
        if code:
            func_count = len(re.findall(r"def test_", code))
            return f"生成代码 {len(code)} chars, {func_count} 个测试函数"
        exp = node_output.get("explanation", "")
        if exp:
            return f"说明: {exp[:200]}"
        msgs = node_output.get("messages", [])
        if msgs:
            raw = get_message_content(msgs[-1])
            return f"LLM 响应 {len(raw)} chars"
        return "已生成"

    key = NODE_OUTPUT_KEYS.get(node_name)
    if key:
        content = node_output.get(key)
        if isinstance(content, str) and content.strip():
            return content[:300]
        if isinstance(content, dict):
            if node_name == "context_retriever":
                keys = list(content.keys())
                return f"上下文就绪 ({len(keys)} 个字段: {', '.join(keys[:4])})"
            return str(content)[:200]

    msgs = node_output.get("messages", [])
    if msgs:
        for msg in reversed(msgs):
            text = get_message_content(msg)
            if text.strip():
                return text[:300]
    return ""


def _node_failed(node_name: str, node_output: Dict[str, Any]) -> bool:
    """Return whether a streamed node update represents a failed step."""
    if node_name != "sandbox_executor":
        return False
    result = node_output.get("execution_result", {})
    return isinstance(result, dict) and result.get("status") == "failed"


def _is_node_complete(node_name: str, node_output: Dict[str, Any]) -> bool:
    """判断节点是否执行完成。
    
    根据节点类型检查是否包含最终输出字段。
    
    Args:
        node_name: 节点名称
        node_output: 节点输出
        
    Returns:
        True if node is complete, False otherwise
    """
    # 检查节点是否有对应的最终输出字段
    complete_keys = {
        "requirement_parser": "parsed_requirement",
        "context_retriever": "context",
        "planner": "case_plan",
        "generator": "generated_code",
        "sandbox_executor": "execution_result",
    }
    
    key = complete_keys.get(node_name)
    if key:
        return key in node_output
    
    # 默认认为是完成状态（兼容未知节点）
    return True


# ─── 新增：信息提取函数 ──────────────────────────────

def _extract_rag_info(state: Dict[str, Any]) -> Dict[str, Any]:
    """提取 RAG 检索信息"""
    ctx = state.get("context", {})
    chunks = ctx.get("chunks", [])
    sources = ctx.get("sources", [])
    roots = ctx.get("roots", [])
    total_chars = sum(len(str(c)) for c in chunks) if isinstance(chunks, list) else 0
    return {
        "phase": ctx.get("phase", "unknown"),
        "chunks": total_chars,
        "sources": sources,
        "roots": len(roots) if isinstance(roots, list) else 0,
    }


def _extract_memory_info(state: Dict[str, Any], thread_id: str = "unknown") -> Dict[str, Any]:
    """提取最终 State 输出状态。

    注意：这里读取的是 graph 最终 state，不是直接查询 InMemoryStore。
    """
    return {
        "thread_id": thread_id,
        "retry_count": state.get("retry_count", 0),
        "repair_count": state.get("repair_count", 0),
        "sandbox_retry_count": state.get("sandbox_retry_count", 0),
        "plans": bool(state.get("case_plan")),
        "generations": bool(state.get("generated_code")),
        "requirements": bool(state.get("parsed_requirement")),
    }


def _extract_tool_info(state: Dict[str, Any]) -> Dict[str, Any]:
    """提取 Tool Use 信息"""
    validation = state.get("validation_result", {})
    if not isinstance(validation, dict):
        return {}
    status = validation.get("status", "unknown")
    errors = validation.get("errors", [])
    return {
        "save_to_file": "success" if state.get("generated_code") else "unknown",
        "code_validator": status,
        "details": errors,
    }


def _format_generation_quality(validation: Dict[str, Any]) -> str:
    """Format the static quality gate applied before sandbox execution."""
    status = validation.get("status", "unknown")
    gate = validation.get("quality_gate", "unknown")
    errors = validation.get("errors") or []
    if status == "passed":
        return (
            f"passed (quality_gate={gate}; 检查项: 已提取 Python 代码、"
            "语法可解析、包含 pytest 测试函数、包含真实命令执行入口、"
            "未发现 mock/fake/dry-run 标记)"
        )
    return f"failed (quality_gate={gate}; errors={errors})"


# ─── 新增：调试信息汇总面板 ────────────────────────────

def print_debug_summary(state: Dict[str, Any], thread_id: str = "unknown"):
    """执行完成后统一展示调试信息"""
    console.print("\n" + "━" * 60)
    console.print("📊 调试信息汇总\n")

    # 🔍 RAG 检索
    rag = _extract_rag_info(state)
    console.print("[bold]🔍 RAG 检索[/bold]")
    console.print(f"  Phase          {rag.get('phase', 'unknown')}")
    console.print(f"  检索字符数     {rag.get('chunks', 0)}")
    console.print(f"  来源文档数     {len(rag.get('sources', []))}")
    console.print(f"  参考根目录     {rag.get('roots', 0)}")
    if rag.get("sources"):
        console.print("  来源文档:")
        for src in rag.get("sources", [])[:5]:
            console.print(f"    - {src}")
    console.print()

    # 💾 State 输出状态
    mem = _extract_memory_info(state, thread_id)
    console.print("[bold]💾 State 输出状态[/bold]")
    console.print(f"  Checkpointer thread_id         {mem['thread_id']}")
    console.print(f"    - retry_count                {mem['retry_count']}")
    console.print(f"    - repair_count               {mem['repair_count']}")
    console.print(f"    - sandbox_retry_count        {mem['sandbox_retry_count']}")
    console.print("  Final State")
    console.print(f"    - case_plan                  {'✅ 已输出' if mem['plans'] else '❌ 未输出'}")
    console.print(f"    - generated_code             {'✅ 已输出' if mem['generations'] else '❌ 未输出'}")
    console.print(f"    - parsed_requirement         {'✅ 已输出' if mem['requirements'] else '❌ 未输出'}")
    console.print()

    execution = state.get("execution_result", {})
    if isinstance(execution, dict) and execution:
        console.print("[bold]🏃 Sandbox[/bold]")
        console.print(f"  Status         {execution.get('status', 'unknown')}")
        console.print(f"  Stage          {execution.get('stage', 'unknown')}")
        console.print(f"  Exit code      {execution.get('exit_code', 'unknown')}")
        if execution.get("error"):
            console.print(f"  Error          {execution.get('error')}")
        console.print()

    # 🛠️ Tool Use
    tools = _extract_tool_info(state)
    if tools:
        console.print("[bold]🛠️ Tool Use[/bold]")
        console.print(f"  {'工具':<<16} {'状态':<<10} 详情")
        save_status = "✅ success" if tools.get("save_to_file") == "success" else "❌ failed"
        val_status = f"✅ {tools['code_validator']}" if tools.get("code_validator") == "passed" else f"❌ {tools['code_validator']}"
        console.print(f"  {'save_to_file':<<16} {save_status:<10} 代码已生成")
        console.print(f"  {'code_validator':<<16} {val_status:<10} {tools.get('details', [])}")


class CLIRunner:
    def __init__(self, provider: str = None, thread_id: str = "cli", hitl: bool = True):
        self.graph = build_runnable_graph(
            provider=provider,
            enable_checkpoint=True,
            enable_store=True,
        )
        self.config = build_runtime_config(thread_id=thread_id)
        self.outputs: Dict[str, str] = {}
        self._hitl_enabled = hitl          # ✅ 修复 2：保存 hitl 到实例
        self._thread_id = thread_id

    # ✅ 使用 LangGraph interrupt 机制替代手动 HITL
    def run(self, prompt: str) -> Dict[str, Any]:
        import time

        cleaned = clean_input(prompt)
        if not cleaned or not is_meaningful(cleaned):
            console.print("\n[bold red]❌ 输入无效或为空，请重新输入。[/bold red]")
            return {}

        state = create_initial_state(cleaned)
        context = AgentContext(user_id="cli_user")

        tree = Tree("🧪 TestCaseAgent", guide_style="bold cyan")
        node_branches = {}
        for name in NODE_NAMES:
            branch = tree.add(f"[dim]○ {name}[/dim]")
            node_branches[name] = branch

        final_output: Dict[str, Any] = {}
        node_timings: Dict[str, float] = {}  # 记录每个节点的耗时
        node_start_time: Dict[str, float] = {}  # 记录每个节点的开始时间
        total_start_time = time.time()

        try:
            with Live(tree, console=console, refresh_per_second=4) as live:
                try:
                    for chunk in self.graph.stream(
                        state,
                        config=self.config,
                        context=context,
                        stream_mode="updates",
                    ):
                        # 检查 interrupt
                        if "__interrupt__" in chunk:
                            interrupt_data = chunk["__interrupt__"]
                            self._handle_interrupt(interrupt_data)
                            continue

                        for node_name, node_output in chunk.items():
                            if node_name not in node_branches:
                                continue

                            # 记录节点开始时间（只在第一次看到节点时记录）
                            if node_name not in node_start_time:
                                node_start_time[node_name] = time.time()

                            # 始终更新耗时（确保每个节点都有耗时记录）
                            elapsed = time.time() - node_start_time[node_name]
                            node_timings[node_name] = elapsed

                            # 检查节点是否完成（通过检查是否有最终输出）
                            is_complete = _is_node_complete(node_name, node_output)
                            
                            if not is_complete:
                                # 节点正在执行中
                                label = Text()
                                label.append(f"⚡ {node_name}", style="bold yellow")
                                label.append(" 执行中...", style="dim")
                                label.append(f" [{elapsed:.2f}s]", style="bold blue")
                                node_branches[node_name].label = label
                                live.update(tree)
                            else:
                                # 节点完成，显示最终状态
                                summary = _extract_summary(node_name, node_output)
                                self.outputs[node_name] = summary
                                if summary:
                                    node_branches[node_name].add(Text(summary, style="dim"))

                                failed = _node_failed(node_name, node_output)
                                label = Text()
                                if failed:
                                    label.append(f"❌ {node_name}", style="bold red")
                                else:
                                    label.append(f"✅ {node_name}", style="bold green")
                                label.append(f" ({len(summary)} chars)", style="dim")
                                label.append(f" [{elapsed:.2f}s]", style="bold blue")
                                node_branches[node_name].label = label
                                live.update(tree)

                            final_output = node_output

                except Exception as e:
                    console.print(f"\n[bold red]❌ Graph 执行出错: {e}[/bold red]")
                    raise
        finally:
            flush_langfuse()

        # 打印耗时统计
        total_time = time.time() - total_start_time
        console.print("\n")
        console.print("[bold blue]⏱️ 执行耗时统计[/bold blue]")
        console.print("-" * 50)
        for node_name in NODE_NAMES:
            if node_name in node_timings:
                elapsed = node_timings[node_name]
                percentage = (elapsed / total_time) * 100 if total_time > 0 else 0
                console.print(f"  {node_name:<20} {elapsed:>6.2f}s  ({percentage:>5.1f}%)")
            else:
                console.print(f"  {node_name:<20} {'N/A':>6}")
        console.print("-" * 50)
        console.print(f"  {'总耗时':<20} {total_time:>6.2f}s")
        console.print()

        try:
            full_state = self.graph.get_state(self.config)
            return full_state.values if full_state else (final_output or {})
        except Exception:
            return final_output or {}

    def _handle_interrupt(self, interrupt_data: Any) -> None:
        """处理 LangGraph interrupt 中断请求。
        
        Args:
            interrupt_data: LangGraph 返回的中断数据，格式可能是 dict、Interrupt 对象或其他类型
        """
        # 处理 Interrupt 对象（langgraph.types.Interrupt）
        if hasattr(interrupt_data, 'name') and hasattr(interrupt_data, 'data'):
            self._process_interrupt_item(interrupt_data.name, interrupt_data.data)
        # 处理 dict 格式
        elif isinstance(interrupt_data, dict):
            for interrupt_name, data in interrupt_data.items():
                self._process_interrupt_item(interrupt_name, data)
        # 处理列表/元组格式
        elif isinstance(interrupt_data, (list, tuple)):
            for item in interrupt_data:
                if isinstance(item, dict):
                    name = item.get("name", "unknown")
                    item_data = item.get("data", item)
                    self._process_interrupt_item(name, item_data)
                elif hasattr(item, 'name') and hasattr(item, 'data'):
                    self._process_interrupt_item(item.name, item.data)
        else:
            console.print(f"[yellow]⚠️ 未知的中断数据格式: {type(interrupt_data)}[/yellow]")

    def _process_interrupt_item(self, interrupt_name: str, data: Any) -> None:
        """处理单个中断项。"""
        if interrupt_name == "planner_approval":
            console.print("\n")
            summary = data.get("summary", "") if isinstance(data, dict) else str(data)
            console.print(
                Panel(
                    summary[:1200] if summary else "(无内容)",
                    title="[bold yellow]🔍 测试计划确认[/]",
                    border_style="yellow",
                )
            )
            choice = input("\n确认并继续? [Y/n]: ").strip().lower()
            if choice not in ("", "y", "yes"):
                console.print("\n[red]❌ 用户拒绝，终止执行[/red]")
                raise RuntimeError("User rejected the plan")
            # 恢复执行：使用 continue 会自动继续 stream
            # 这里不需要额外操作，stream 会自动恢复


def print_final_result(state: Dict[str, Any]):
    code = state.get("generated_code") or state.get("code") or ""
    plan = state.get("case_plan") or ""
    explanation = state.get("explanation") or ""
    validation = state.get("validation_result", {})
    execution = state.get("execution_result", {})
    sandbox_status = (
        execution.get("status") if isinstance(execution, dict) else None
    )

    console.print("\n" + "━" * 60)
    if sandbox_status == "failed":
        console.print("[bold red]❌ 执行结束：沙盒验证失败[/bold red]\n")
    else:
        console.print("[bold green]✅ 执行完成[/bold green]\n")

    if plan:
        plan_label = f"📋 测试计划 ({len(plan)} 字符)"
        console.print(Panel(plan[:3000], title=plan_label, border_style="blue"))
    if code:
        code_label = f"🐍 生成代码 ({len(code)} 字符)"
        if len(code) > _CODE_PREVIEW_CHARS:
            code_label += f" — 前 {_CODE_PREVIEW_CHARS} 字符"
        console.print(
            Panel(code[:_CODE_PREVIEW_CHARS], title=code_label, border_style="green")
        )
    if explanation:
        console.print(Panel(explanation[:1500], title="📝 说明", border_style="cyan"))

    if isinstance(validation, dict) and validation.get("status"):
        status = validation.get("status", "unknown")
        detail = _format_generation_quality(validation)
        errors = validation.get("errors", [])
        color = "green" if status == "passed" else "red"
        console.print(f"\n[bold {color}]🧪 生成代码静态校验: {detail}[/]")
        if errors:
            for err in errors[:5]:
                console.print(f"  [red]- {err}[/]")

    if isinstance(execution, dict) and execution:
        status = execution.get("status", "unknown")
        stage = execution.get("stage", "unknown")
        exit_code = execution.get("exit_code", "unknown")
        color = "green" if status == "success" else "red"
        console.print(
            f"\n[bold {color}]🏃 沙盒执行结果: "
            f"{status}, stage={stage}, exit_code={exit_code}[/]"
        )
        if execution.get("error"):
            console.print(f"  [red]- {execution.get('error')}[/]")

    if code and sandbox_status != "failed":
        dest = _save_code(code)
        if dest:
            console.print(
                f"\n[bold green]💾 完整代码 ({len(code)} 字符) 已保存到 {dest}[/]"
            )
    elif code:
        console.print(
            "\n[bold yellow]💾 沙盒验证失败，跳过保存完整代码到 output/[/]"
        )

    # ✅ 新增：调试信息汇总
    print_debug_summary(state)

    console.print("\n[dim]💾 记忆已自动保存[/dim]\n")


def _save_code(code: str) -> str | None:
    if not code or not code.strip():
        return None
    out_dir = Path(_CODE_SAVE_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    from datetime import datetime

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = out_dir / f"test_generated_{ts}.py"
    dest.write_text(code, encoding="utf-8")
    return str(dest)