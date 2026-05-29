from typing import Any, Optional
from langchain_core.messages import HumanMessage, AIMessage

from ..state import AgentState, AgentContext
from ..prompts import get_requirement_parser_prompt
from ..intent_router import route_intent, get_intent_cluster, get_template_name
from ..logging_config import get_logger
from .utils import _last_user_message

_logger = get_logger("nodes.requirement_parser")


def get_llm(agent: Any = None) -> Any:
    """Module-level LLM accessor — patchable in tests."""
    return agent


def get_memory_manager(runtime: Any = None) -> Any:
    """Module-level MemoryManager accessor — patchable in tests."""
    if runtime is None:
        return None
    from ..memory_manager import MemoryManager
    return MemoryManager(runtime)


def requirement_parser(
    state: AgentState, runtime: Any = None, agent: Any = None
) -> dict:
    raw_requirement = state.get("requirement") or _last_user_message(state)

    # 意图识别（规则匹配）
    parsed_intent = route_intent(raw_requirement)
    intent_cluster = get_intent_cluster(parsed_intent)
    template_name = get_template_name(parsed_intent)

    _logger.info(
        "intent_detected",
        raw=raw_requirement[:50],
        intent=parsed_intent,
        cluster=intent_cluster,
        template=template_name,
    )

    prompt = get_requirement_parser_prompt(raw_requirement)

    # Use get_llm so tests can patch this module's get_llm
    llm = get_llm(agent)
    if llm is not None:
        llm_result = llm.invoke({"messages": [HumanMessage(content=prompt)]})
    else:
        from .utils import _invoke_llm
        llm_result = _invoke_llm(agent, prompt, node_name="requirement_parser")

    if hasattr(llm_result, "content"):
        content = llm_result.content
    elif isinstance(llm_result, dict):
        # Allow LLM result dict to override intent fields (used in tests)
        if "intent" in llm_result:
            parsed_intent = llm_result["intent"]
            intent_cluster = llm_result.get("cluster", intent_cluster)
        content = llm_result.get("raw_spec", str(llm_result))
    else:
        content = str(llm_result)

    memory = get_memory_manager(runtime)
    if memory is not None:
        memory.save_requirement(
            raw_requirement=raw_requirement,
            parsed_requirement=content,
        )

    return {
        "requirement": raw_requirement,
        "parsed_requirement": content,
        "parsed_intent": parsed_intent,
        "intent": parsed_intent,
        "intent_cluster": intent_cluster,
        "cluster": intent_cluster,
        "template_name": template_name,
        "messages": [AIMessage(content=content)],
    }
