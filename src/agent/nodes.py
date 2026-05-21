# nodes.py —— 修复 generator 提取逻辑与 prompt 歧义

import ast
import re
import uuid
from typing import Any

from langgraph.runtime import Runtime

from .state import AgentState, AgentContext


def _message_content(message: Any) -> str:
    """Return message content from dict or LangChain message."""
    if isinstance(message, dict):
        return str(message.get("content", ""))
    return str(getattr(message, "content", ""))


def _last_user_message(state: AgentState) -> str:
    """Extract the latest user message from state messages."""
    for message in reversed(state.get("messages", [])):
        role = message.get("role") if isinstance(message, dict) else getattr(message, "type", "")
        if role in ("user", "human"):
            return _message_content(message)
    return ""


def _invoke_llm(agent: Any, prompt: str, node_name: str = "LLM") -> str:
    """Invoke the deep agent with a single prompt and return text content."""
    if agent is None:
        raise RuntimeError("LLM node requires a model-backed agent. Pass model to build_graph().")

    print(f"\n[{node_name}] Invoking LLM ({len(prompt)} chars prompt)...")
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        last_msg = result["messages"][-1]
        content = _message_content(last_msg)
        print(f"[{node_name}] LLM response: {len(content)} chars")
        return content
    except PermissionError:
        import sys
        print(f"\n[{node_name}] ❌ 文件写入权限不足（LLM 可能企图写系统路径 /test_case/...）", file=sys.stderr)
        raise
    except Exception:
        import os, sys, traceback
        exc_name = type(sys.exc_info()[1]).__name__
        exc_msg = str(sys.exc_info()[1])[:200]
        provider = os.environ.get("TEST_CASE_AGENT_MODEL_PROVIDER", "unknown")
        model = os.environ.get("LLM_MODEL") or os.environ.get("DEEPSEEK_MODEL") or "unknown"
        base_url = os.environ.get("LLM_BASE_URL") or os.environ.get("DEEPSEEK_BASE_URL") or "unknown"
        print(f"\n[{node_name}] ❌ Agent invoke 失败: {exc_name}: {exc_msg}", file=sys.stderr)
        print(f"  provider={provider}  model={model}  base_url={base_url}", file=sys.stderr)
        print(f"  Check .env API keys 或排查上方具体错误。", file=sys.stderr)
        print(f"\n--- traceback ---", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print(f"--- end traceback ---\n", file=sys.stderr)
        raise


def _extract_code(text: str) -> str:
    """Extract fenced code if present, otherwise return raw text.
    
    修复：当围栏提取为空但原文非空时，回退到原文，避免 LLM 未加围栏导致返回空。
    """
    original = text.strip()
    if not original:
        return ""
    
    if "```python" in text:
        extracted = text.split("```python", 1)[1].split("```", 1)[0].strip()
        return extracted or original
    if "```bash" in text:
        extracted = text.split("```bash", 1)[1].split("```", 1)[0].strip()
        return extracted or original
    if "```sh" in text:
        extracted = text.split("```sh", 1)[1].split("```", 1)[0].strip()
        return extracted or original
    if "```" in text:
        extracted = text.split("```", 1)[1].split("```", 1)[0].strip()
        return extracted or original
    
    return original


def _validate_real_test_code(code: str) -> list[str]:
    """Return quality issues that indicate mock-only generated pytest code."""
    issues: list[str] = []
    lowered = code.lower()

    if "pytest.mark.dry_run_only" in code:
        issues.append("Generated pytest code must not be marked dry_run_only.")

    if re.search(r"^\s*#\s*.*subprocess\.run", code, flags=re.MULTILINE):
        issues.append("subprocess.run appears to be commented out.")

    if "subprocess.run" not in code:
        issues.append("Generated pytest code should execute the target command with subprocess.run.")

    if re.search(r"output\s*=\s*(?:'''|\"\"\")", code):
        issues.append("Generated pytest code must not use hard-coded successful command output.")

    if "mock" in lowered or "fake output" in lowered:
        issues.append("Generated pytest code must not use mock or fake output for real tests.")

    return issues


def _memory_namespace(runtime: Runtime[AgentContext], suffix: str) -> tuple:
    """构建 Store 命名空间：(user_id, [project_id], suffix)"""
    ctx = runtime.context
    parts = [ctx.user_id]
    if ctx.project_id:
        parts.append(ctx.project_id)
    parts.append(suffix)
    return tuple(parts)


def _format_memories(memories: list) -> str:
    """将检索到的记忆格式化为提示词片段。"""
    if not memories:
        return ""
    lines = ["\n## 历史相关记忆"]
    for m in memories:
        data = m.value.get("data", "") if hasattr(m, "value") else str(m)
        lines.append(f"- {data}")
    return "\n".join(lines)


# ----------------------------------------------------------------------
# 以下节点保持不变（无需记忆）
# ----------------------------------------------------------------------
def requirement_parser(state: AgentState) -> dict:
    requirement = state.get("requirement") or _last_user_message(state)
    return {
        "requirement": requirement,
        "messages": [{"role": "assistant", "content": f"Requirement parsed: {requirement[:120]}"}],
    }


def context_retriever(state: AgentState) -> dict:
    requirement = state.get("requirement", "")
    context = {
        "phase": "phase_one_placeholder",
        "requirement": requirement,
        "reference_roots": [
            "/home/zx/CICD/test_case",
            "/home/zx/CICD/rocm-on-radeon",
        ],
        "case_format": "test_case/suites/<suite>/test_<name>.sh or pytest draft",
        "execution_mode": "dry_run_only",
        "todo": "Replace this placeholder with RAG and repository retrieval in phase two.",
    }
    return {
        "context": context,
        "messages": [{"role": "assistant", "content": "Context retrieved: phase-one placeholder context."}],
    }


def execution_planner(state: AgentState) -> dict:
    generated_code = state.get("generated_code") or state.get("code", "")
    execution_plan = {
        "mode": "dry_run",
        "will_execute": False,
        "has_generated_code": bool(generated_code),
        "command_summary": "pytest <generated_test_file>  # dry-run only, not executed",
        "risk": "safe",
        "human_confirm_required": False,
    }
    return {
        "execution_plan": execution_plan,
        "messages": [{"role": "assistant", "content": f"Execution plan created: {execution_plan}"}],
    }


def dry_run_executor(state: AgentState) -> dict:
    has_generated_code = bool(state.get("generated_code") or state.get("code", ""))
    execution_result = {
        "status": "skipped_dry_run",
        "executed": False,
        "has_generated_code": has_generated_code,
        "reason": "Phase one does not execute shell or tests.",
    }
    return {
        "execution_result": execution_result,
        "messages": [{"role": "assistant", "content": f"Dry-run execution result: {execution_result}"}],
    }


def result_parser(state: AgentState) -> dict:
    execution_result = state.get("execution_result", {})
    has_generated_code = bool(state.get("generated_code") or state.get("code", ""))
    validation_result = state.get("validation_result", {})
    validation_failed = validation_result.get("status") == "failed"
    parsed_result = {
        "status": execution_result.get("status", "unknown"),
        "has_generated_code": has_generated_code,
        "needs_repair": (not has_generated_code) or validation_failed,
        "summary": "Dry-run completed. No real test command was executed.",
        "validation_result": validation_result,
    }
    return {
        "parsed_result": parsed_result,
        "messages": [{"role": "assistant", "content": f"Result parsed: {parsed_result}"}],
    }


def finalizer(state: AgentState) -> dict:
    final_report = {
        "status": "completed",
        "requirement": state.get("requirement", ""),
        "has_case_plan": bool(state.get("case_plan")),
        "has_generated_code": bool(state.get("generated_code") or state.get("code")),
        "validation_status": state.get("validation_result", {}).get("status", "unknown"),
        "validation_errors": state.get("validation_result", {}).get("errors", []),
        "execution_status": state.get("execution_result", {}).get("status", "unknown"),
        "repair_count": state.get("repair_count", 0),
        "dry_run_only": True,
    }
    return {
        "final_report": final_report,
        "messages": [{"role": "assistant", "content": f"Final report: {final_report}"}],
    }


def static_validator(state: AgentState) -> dict:
    code = state.get("generated_code") or state.get("code", "")
    if not code:
        return {
            "validation_result": {
                "status": "failed",
                "language": "unknown",
                "errors": ["No generated code."],
            },
            "retry": 1,
            "messages": [{"role": "assistant", "content": "Static validation failed: no code."}],
        }

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return {
            "validation_result": {
                "status": "failed",
                "language": "python",
                "errors": [str(exc)],
            },
            "retry": 1,
            "messages": [{"role": "assistant", "content": f"Static validation failed: {exc}"}],
        }

    funcs = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    imports = [
        node.names[0].name if hasattr(node, "names") and node.names else ""
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    result = {
        "status": "passed",
        "language": "python",
        "function_count": len(funcs),
        "import_count": len(imports),
        "functions": funcs,
        "imports": imports,
    }
    return {
        "validation_result": result,
        "messages": [{"role": "assistant", "content": f"Static validation passed: {result}"}],
    }


# ----------------------------------------------------------------------
# 以下节点接入长期记忆（核心改造）
# ----------------------------------------------------------------------

def planner(state: AgentState, runtime: Runtime[AgentContext], agent) -> dict:
    """规划节点：读取历史计划记忆 → 生成计划 → 写入新记忆"""
    ns = _memory_namespace(runtime, "plans")
    
    print(f"\n{'='*60}")
    print(f"[DEBUG planner] Runtime context: user_id={runtime.context.user_id}, project_id={runtime.context.project_id}")
    print(f"[DEBUG planner] Memory namespace: {ns}")
    print(f"[DEBUG planner] Query: {state.get('requirement', '')[:80]}...")
    
    memories = runtime.store.search(ns, query=state.get("requirement", ""), limit=3)
    memory_hints = _format_memories(memories)
    
    print(f"[DEBUG planner] Retrieved {len(memories)} memories:")
    for i, m in enumerate(memories):
        data = m.value.get("data", "")[:100] if hasattr(m, "value") else str(m)[:100]
        print(f"  [{i}] key={m.key}, data={data}...")
    print(f"[DEBUG planner] Formatted hints length: {len(memory_hints)} chars")
    print(f"{'='*60}\n")

    prompt = (
        "你是 Test Case Agent 的规划器。请基于下面需求输出一个简洁测试计划，"
        "包含测试目标、suite 建议、前置条件、步骤、预期结果、风险和 dry-run 执行计划。\n\n"
        f"需求:\n{state.get('requirement', '')}\n\n"
        f"上下文:\n{state.get('context', {})}\n"
        f"{memory_hints}\n"
    )
    case_plan = _invoke_llm(agent, prompt, node_name="planner")

    memory_key = f"plan_{uuid.uuid4().hex[:8]}"
    memory_value = {
        "data": f"需求: {state.get('requirement', '')[:120]}... | 计划摘要: {case_plan[:200]}...",
        "requirement": state.get("requirement", ""),
        "full_plan": case_plan,
    }
    runtime.store.put(ns, memory_key, memory_value)
    
    print(f"\n[DEBUG planner] ✅ Wrote memory: key={memory_key}, namespace={ns}")
    print(f"[DEBUG planner] Memory value preview: {memory_value['data'][:100]}...")

    return {
        "case_plan": case_plan,
        "messages": [{"role": "assistant", "content": f"Case plan generated.\n{case_plan[:500]}"}],
    }


def generator(state: AgentState, runtime: Runtime[AgentContext], agent) -> dict:
    """生成节点：读取历史生成风格 → 生成代码 → 写入生成记录"""
    ns = _memory_namespace(runtime, "generations")
    
    print(f"\n{'='*60}")
    print(f"[DEBUG generator] Memory namespace: {ns}")
    print(f"[DEBUG generator] Query (case_plan): {state.get('case_plan', '')[:80]}...")
    
    memories = runtime.store.search(ns, query=state.get("case_plan", ""), limit=2)
    memory_hints = _format_memories(memories)
    
    print(f"[DEBUG generator] Retrieved {len(memories)} memories:")
    for i, m in enumerate(memories):
        data = m.value.get("data", "")[:100] if hasattr(m, "value") else str(m)[:100]
        print(f"  [{i}] key={m.key}, data={data}...")
    print(f"[DEBUG generator] Formatted hints length: {len(memory_hints)} chars")
    print(f"{'='*60}\n")

    # 注入上一轮代码（限制大小，防止多轮后 prompt 爆炸）
    _MAX_PREVIOUS_CODE_CHARS = 5000
    previous_code = state.get('generated_code') or state.get('code', '')
    previous_code_hint = ""
    if previous_code:
        truncated = previous_code
        if len(previous_code) > _MAX_PREVIOUS_CODE_CHARS:
            truncated = previous_code[:_MAX_PREVIOUS_CODE_CHARS] + "\n# ... (已截断，上述代码太长)"
        previous_code_hint = (
            f"\n\n上一轮生成的代码（请在此基础上修改，输出完整可执行文件）：\n"
            f"```python\n{truncated}\n```\n"
        )

    # ✅ 关键修复：明确禁止只返回片段/差异，强制输出完整代码块
    prompt = (
        "你是 Test Case Agent 的生成器。请根据测试计划生成最小可执行的 pytest 测试代码草案。"
        "注意：Agent 当前流程是 dry-run，不会在生成阶段执行 shell；"
        "但你输出的 pytest 文件本身必须是真实可执行测试，必须在测试运行时通过 subprocess.run "
        "或等价方式执行目标命令。禁止使用 mock output、fake output、硬编码成功输出，"
        "禁止把真实执行代码注释掉，禁止给最终测试加 dry_run_only 标记。"
        "命令不存在时应使用 pytest.skip，命令执行失败时应暴露 returncode/stdout/stderr 诊断。"
        "\n\n【强制要求】即使只是补充一个函数或做小幅修改，也必须输出完整的 pytest 文件代码，"
        "不要只返回新增片段、diff 或文字说明。必须包含所有 import 和全部测试函数。"
        "\n\n【路径约束】保存文件时一律使用相对路径，如 test_xxx.py 或 output/test_xxx.py，"
        "禁止使用 /test_case/、/home/、/tmp/ 等绝对路径。代码中不要出现 save_to_file 调用。"
        "请用 ```python ... ``` 代码块包裹完整代码。\n\n"
        f"测试计划:\n{state.get('case_plan', '')}\n"
        f"{memory_hints}\n"
        f"{previous_code_hint}\n"
    )
    reply = _invoke_llm(agent, prompt, node_name="generator")
    print(f"\n[DEBUG generator] Raw reply length: {len(reply)} chars")
    print(f"[DEBUG generator] Raw reply preview: {reply[:200]}...")
    
    generated_code = _extract_code(reply)
    print(f"[DEBUG generator] Extracted code length: {len(generated_code)} chars")
    
    quality_issues = _validate_real_test_code(generated_code)
    validation_result = {
        "status": "failed" if quality_issues else "passed",
        "quality_gate": "real_pytest_code",
        "errors": quality_issues,
    }

    memory_key = f"gen_{uuid.uuid4().hex[:8]}"
    memory_value = {
        "data": f"为需求 [{state.get('requirement', '')[:80]}...] 生成了 {len(generated_code)} 字符代码",
        "code_preview": generated_code[:500],
    }
    runtime.store.put(ns, memory_key, memory_value)
    
    print(f"\n[DEBUG generator] ✅ Wrote memory: key={memory_key}, namespace={ns}")
    print(f"[DEBUG generator] Memory value preview: {memory_value['data'][:100]}...")

    return {
        "code": generated_code,
        "generated_code": generated_code,
        "validation_result": validation_result,
        "messages": [{"role": "assistant", "content": reply}],
    }


def repairer(state: AgentState, runtime: Runtime[AgentContext], agent) -> dict:
    """修复节点：读取历史修复记录 → 生成修复建议 → 写入新记录"""
    parsed_result = state.get("parsed_result", {})
    if not parsed_result.get("needs_repair", False):
        suggestion = "No repair needed in phase-one dry-run."
        print(f"\n[DEBUG repairer] No repair needed.")
        return {
            "repair_suggestion": suggestion,
            "messages": [{"role": "assistant", "content": suggestion}],
        }

    ns = _memory_namespace(runtime, "repairs")
    
    print(f"\n{'='*60}")
    print(f"[DEBUG repairer] Memory namespace: {ns}")
    print(f"[DEBUG repairer] Query (validation_result): {str(state.get('validation_result', {}))[:80]}...")
    
    memories = runtime.store.search(ns, query=str(state.get("validation_result", {})), limit=3)
    memory_hints = _format_memories(memories)
    
    print(f"[DEBUG repairer] Retrieved {len(memories)} memories:")
    for i, m in enumerate(memories):
        data = m.value.get("data", "")[:100] if hasattr(m, "value") else str(m)[:100]
        print(f"  [{i}] key={m.key}, data={data}...")
    print(f"[DEBUG repairer] Formatted hints length: {len(memory_hints)} chars")
    print(f"{'='*60}\n")

    prompt = (
        "你是 Test Case Agent 的失败修复器。下面的测试草案需要修复，"
        "请给出简洁修复建议，不要执行命令。最终 pytest 代码必须真实执行目标命令，"
        "不能使用 mock output、fake output 或硬编码成功输出。\n\n"
        f"需求:\n{state.get('requirement', '')}\n\n"
        f"质量检查:\n{state.get('validation_result', {})}\n\n"
        f"解析结果:\n{state.get('parsed_result', {})}\n\n"
        f"代码:\n{state.get('generated_code') or state.get('code', '')}\n"
        f"{memory_hints}\n"
    )
    suggestion = _invoke_llm(agent, prompt, node_name="repairer")

    memory_key = f"repair_{uuid.uuid4().hex[:8]}"
    memory_value = {
        "data": f"修复了 [{state.get('requirement', '')[:80]}...] 的问题",
        "issue": str(state.get("validation_result", {})),
        "fix": suggestion[:500],
    }
    runtime.store.put(ns, memory_key, memory_value)
    
    print(f"\n[DEBUG repairer] ✅ Wrote memory: key={memory_key}, namespace={ns}")
    print(f"[DEBUG repairer] Memory value preview: {memory_value['data'][:100]}...")

    return {
        "repair_count": 1,
        "repair_suggestion": suggestion,
        "messages": [{"role": "assistant", "content": f"Repair suggestion generated.\n{suggestion[:500]}"}],
    }


# Backward-compatible aliases
def coder(state: AgentState, agent) -> dict:
    return generator(state, runtime=None, agent=agent)  # type: ignore[arg-type]


def checker(state: AgentState) -> dict:
    return static_validator(state)


def router(state: AgentState) -> str:
    retry = state.get("retry", 0)
    validation_status = state.get("validation_result", {}).get("status")
    if retry >= 3:
        return "giveup"
    if validation_status == "passed":
        return "ok"
    return "retry"