import re
from typing import Any

from langchain_core.messages import HumanMessage, AIMessage

from ..state import AgentState
from ..prompts import get_planner_prompt
from ..logging_config import get_logger
from .utils import _invoke_llm

_logger = get_logger("nodes.planner")


def get_llm(agent: Any = None) -> Any:
    """Module-level LLM accessor — patchable in tests."""
    return agent


def get_memory_manager(runtime: Any = None) -> Any:
    """Module-level MemoryManager accessor — patchable in tests."""
    if runtime is None:
        return None
    from ..memory_manager import MemoryManager
    return MemoryManager(runtime)


def _parse_execution_plan(case_plan: str) -> dict:
    """从 planner 输出中提取 YAML 格式的 execution_plan 并解析为 dict。

    planner prompt 要求在输出末尾追加 ```yaml 包裹的 execution_plan 块，
    此函数提取该块并解析，解析失败时返回降级的默认执行计划。
    """
    # 提取 yaml 代码块
    yaml_match = re.search(r"```yaml\s*(.+?)\s*```", case_plan, re.DOTALL)
    if not yaml_match:
        _logger.debug("execution_plan_no_yaml_block")
        return {"status": "defaulted", "reason": "未找到 yaml 执行计划块"}

    yaml_text = yaml_match.group(1).strip()
    try:
        import yaml as _yaml
        parsed = _yaml.safe_load(yaml_text)
        if parsed and isinstance(parsed, dict) and "execution_plan" in parsed:
            plan = dict(parsed["execution_plan"])
            plan["status"] = "parsed"
            plan["raw_yaml"] = yaml_text
            _logger.info("execution_plan_parsed")
            return plan
    except ImportError:
        _logger.debug("execution_plan_yaml_lib_missing")
    except Exception as e:
        _logger.warning("execution_plan_yaml_parse_failed", error=str(e))

    return {"status": "raw", "raw_yaml": yaml_text}


def planner(state: AgentState, runtime: Any = None, agent: Any = None) -> dict:
    memory = get_memory_manager(runtime)

    feedback = state.get("feedback", "")
    _logger.info(
        "planner_start",
        query=state.get("requirement", "")[:80],
        feedback=feedback[:160] if feedback else "",
        user_id=runtime.context.user_id if runtime else "unknown",
    )

    memories = []
    memory_hints = ""
    if memory is not None:
        memories = memory.search("plans", query=state.get("requirement", ""), limit=3)
        raw_hints = memory.format_hints(memories)
        memory_hints = raw_hints if isinstance(raw_hints, str) else ""
        _logger.debug("planner_memories", count=len(memories))

    prompt = get_planner_prompt(
        requirement=state.get("requirement", "") or state.get("parsed_requirement", ""),
        context=state.get("context", {}),
        memory_hints=memory_hints,
        feedback=feedback,
        execution_result=state.get("execution_result", {}),
    )

    # Use get_llm so tests can patch this module's get_llm
    llm = get_llm(agent)
    if llm is not None:
        response = llm.invoke({"messages": [HumanMessage(content=prompt)]})
        case_plan = response.content if hasattr(response, "content") else str(response)
    else:
        case_plan = _invoke_llm(agent, prompt, node_name="planner")

    # 从 case_plan 中解析 execution_plan
    execution_plan = _parse_execution_plan(case_plan)

    if memory is not None:
        memory_key = memory.save_plan(
            requirement=state.get("requirement", ""),
            case_plan=case_plan,
        )
        # Also call save_memory for backward compatibility
        if hasattr(memory, "save_memory"):
            memory.save_memory(data=case_plan, key=memory_key)
        _logger.info("planner_memory_saved", key=memory_key)

    _logger.info("planner_done", execution_plan_status=execution_plan.get("status", "unknown"))

    return {
        "case_plan": case_plan,
        "execution_plan": execution_plan,
        "messages": [AIMessage(content=f"Case plan generated.\n{case_plan[:500]}")],
    }