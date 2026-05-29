"""Agent 节点通用工具函数 —— 统一消息处理、LLM 调用、代码提取等。

函数：
- _message_content: 统一获取消息内容
- _last_user_message: 获取最后一条用户消息
- _invoke_llm: 标准 LLM 调用（使用 BaseMessage）
- _looks_like_python_code: 检查代码是否像 Python
- _fix_code_by_truncation: 截断修复代码
- _extract_code: 从 LLM 回复中提取代码
- _validate_real_test_code: 验证测试代码有效性
- _memory_namespace: 构建记忆命名空间
- _format_memories: 格式化记忆列表
"""

import ast
import re
from typing import Any

from langchain_core.messages import HumanMessage

from ..state import AgentState, AgentContext
from ..logging_config import get_logger

_logger = get_logger("nodes.utils")


def _message_content(message: Any) -> str:
    if hasattr(message, "content"):
        return str(message.content)
    if isinstance(message, dict):
        return str(message.get("content", ""))
    return str(message)


def _last_user_message(state: AgentState) -> str:
    msgs = state.get("messages", [])
    if not msgs:
        return ""
    for message in reversed(msgs):
        if hasattr(message, "type"):
            role = message.type
            if role in ("user", "human"):
                content = getattr(message, "content", "")
                if content:
                    return str(content)
        elif isinstance(message, dict):
            role = message.get("role", "")
            if role in ("user", "human"):
                content = message.get("content", "")
                if content:
                    return str(content)
    return _message_content(msgs[-1])


def _invoke_llm(agent: Any, prompt: str, node_name: str = "LLM") -> str:
    if agent is None:
        raise RuntimeError(
            "LLM node requires a model-backed agent. Pass model to build_graph()."
        )

    _logger.info("invoke_llm_start", node=node_name, prompt_len=len(prompt))
    try:
        result = agent.invoke({"messages": [HumanMessage(content=prompt)]})
        last_msg = result["messages"][-1]
        content = _message_content(last_msg)
        _logger.info("invoke_llm_done", node=node_name, response_len=len(content))
        return content
    except PermissionError:
        _logger.error("invoke_llm_permission_error", node=node_name)
        raise
    except (ConnectionError, TimeoutError) as e:
        _logger.error("invoke_llm_network_error", node=node_name, error=str(e))
        raise
    except Exception as e:
        _logger.exception("invoke_llm_failed", node=node_name, error=str(e)[:200])
        raise RuntimeError(f"[{node_name}] LLM invoke 失败: {type(e).__name__}: {e}") from e


def _looks_like_python_code(text: str) -> tuple[bool, str]:
    """严格检查：返回 (是否有效, 原因)。不做截断修复。"""
    stripped = text.strip()
    if not stripped:
        return False, "代码为空"
    if not any(kw in stripped for kw in ("import ", "def ", "class ")):
        return False, "缺少 Python 基本语法特征（import/def/class）"
    if "def test_" not in stripped:
        return False, "缺少 pytest 测试函数（def test_...）"
    try:
        ast.parse(stripped)
        return True, ""
    except SyntaxError as exc:
        return False, f"语法错误: {exc}"


def _fix_code_by_truncation(code: str) -> str | None:
    """截断代码到最长可解析前缀，修复尾部未闭合 f-string 等错误。"""
    lines = code.split("\n")
    for i in range(len(lines), 0, -1):
        snippet = "\n".join(lines[:i])
        try:
            ast.parse(snippet)
            return snippet
        except SyntaxError:
            pass
    return None


def _extract_code(text: str) -> tuple[str, str, str]:
    """返回 (code, explanation, status)。新增截断修复能力。"""
    original = text.strip()
    if not original:
        return "", "", "空回复"

    candidates = []

    python_blocks = re.findall(r"```python\s*(.*?)\s*```", text, re.DOTALL)
    candidates.extend(block.strip() for block in python_blocks)

    if not candidates:
        generic_blocks = re.findall(r"```\s*(.*?)\s*```", text, re.DOTALL)
        candidates.extend(block.strip() for block in generic_blocks)

    if not candidates and "```python" in text:
        unclosed = text.split("```python", 1)[1].strip()
        candidates.append(unclosed)

    explanation = re.sub(
        r"```(?:python)?\s*.*?\s*```", "", text, flags=re.DOTALL
    ).strip()
    explanation = re.sub(r"```python\s*.*$", "", explanation, flags=re.DOTALL).strip()

    best_code = ""
    best_status = "未找到有效代码块"

    for candidate in candidates:
        is_valid, reason = _looks_like_python_code(candidate)
        if is_valid:
            best_code = candidate
            best_status = "成功提取有效代码"
            break
        else:
            # 尝试截断修复尾部语法错误
            fixed = _fix_code_by_truncation(candidate)
            if fixed:
                is_valid_fixed, _ = _looks_like_python_code(fixed)
                if is_valid_fixed:
                    best_code = fixed
                    best_status = "成功提取并截断修复代码"
                    break
            if best_status == "未找到有效代码块":
                best_code = candidate
                best_status = f"代码块提取成功但验证失败: {reason}"

    if not best_code:
        is_valid, reason = _looks_like_python_code(original)
        if is_valid:
            best_code = original
            best_status = "成功提取有效代码（无围栏）"
            explanation = ""
        else:
            fixed = _fix_code_by_truncation(original)
            if fixed:
                is_valid_fixed, _ = _looks_like_python_code(fixed)
                if is_valid_fixed:
                    best_code = fixed
                    best_status = "成功提取并截断修复代码（无围栏）"
                    explanation = ""
                else:
                    best_status = f"无围栏代码验证失败: {reason}"
            else:
                best_status = f"无围栏代码验证失败: {reason}"

    return best_code, explanation, best_status


def _validate_real_test_code(code: str) -> list[str]:
    issues: list[str] = []
    if not code or not code.strip():
        issues.append("No generated code extracted.")
        return issues

    lowered = code.lower()

    if "def test_" not in code:
        issues.append(
            "Generated pytest code must contain at least one test function (def test_...)."
        )

    try:
        ast.parse(code)
    except SyntaxError as exc:
        issues.append(f"Syntax error in generated code: {exc}")

    if "pytest.mark.dry_run_only" in code:
        issues.append("Generated pytest code must not be marked dry_run_only.")

    if re.search(r"^\s*#\s*.*subprocess\.run", code, flags=re.MULTILINE):
        issues.append("subprocess.run appears to be commented out.")

    has_subprocess = "subprocess" in lowered or "subprocess.run" in lowered
    has_popen = "popen" in lowered
    has_run_cmd = "run_cmd" in lowered or "execute" in lowered
    if not (has_subprocess or has_popen or has_run_cmd):
        issues.append(
            "Generated pytest code should execute the target command with subprocess or equivalent."
        )

    if re.search(r"output\s*=\s*(?:'''|\"\"\")", code):
        issues.append(
            "Generated pytest code must not use hard-coded successful command output."
        )

    if "mock" in lowered or "fake output" in lowered:
        issues.append(
            "Generated pytest code must not use mock or fake output for real tests."
        )

    return issues


def _memory_namespace(runtime: Any, suffix: str) -> tuple:
    ctx = runtime.context
    parts = [ctx.user_id]
    if ctx.project_id:
        parts.append(ctx.project_id)
    parts.append(suffix)
    return tuple(parts)


def _format_memories(memories: list) -> str:
    if not memories:
        return ""
    lines = ["\n## 历史相关记忆"]
    for m in memories:
        data = m.value.get("data", "") if hasattr(m, "value") else str(m)
        lines.append(f"- {data}")
    return "\n".join(lines)
