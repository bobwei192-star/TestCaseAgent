import uuid
from typing import Any
from langgraph.runtime import Runtime
from ..state import AgentState, AgentContext
from ..prompts import get_requirement_parser_prompt
from .utils import _invoke_llm, _last_user_message, _memory_namespace


def requirement_parser(
    state: AgentState, runtime: Runtime[AgentContext], agent: Any
) -> dict:
    raw_requirement = state.get("requirement") or _last_user_message(state)

    prompt = get_requirement_parser_prompt(raw_requirement)

    llm_result = _invoke_llm(agent, prompt, node_name="requirement_parser")

    if hasattr(llm_result, "content"):
        content = llm_result.content
    else:
        content = str(llm_result)

    ns = _memory_namespace(runtime, "requirements")
    memory_key = f"req_{uuid.uuid4().hex[:8]}"
    runtime.store.put(
        ns,
        memory_key,
        {
            "raw": raw_requirement,
            "parsed": content,
        },
    )

    msg = {"role": "assistant", "content": content}

    return {
        "requirement": raw_requirement,
        "parsed_requirement": content,
        "messages": [msg],
    }
