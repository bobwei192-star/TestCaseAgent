import uuid
from typing import Any
from langgraph.runtime import Runtime
from ..state import AgentState, AgentContext
from ..prompts import get_planner_prompt
from .utils import _invoke_llm, _memory_namespace, _format_memories


def planner(state: AgentState, runtime: Runtime[AgentContext], agent: Any) -> dict:
    ns = _memory_namespace(runtime, "plans")

    print(f"\n{'=' * 60}")
    print(
        f"[DEBUG planner] Runtime context: user_id={runtime.context.user_id}, project_id={runtime.context.project_id}"
    )
    print(f"[DEBUG planner] Memory namespace: {ns}")
    print(f"[DEBUG planner] Query: {state.get('requirement', '')[:80]}...")

    memories = runtime.store.search(ns, query=state.get("requirement", ""), limit=3)
    memory_hints = _format_memories(memories)

    print(f"[DEBUG planner] Retrieved {len(memories)} memories:")
    for i, m in enumerate(memories):
        data = m.value.get("data", "")[:100] if hasattr(m, "value") else str(m)[:100]
        print(f"  [{i}] key={m.key}, data={data}...")
    print(f"[DEBUG planner] Formatted hints length: {len(memory_hints)} chars")
    print(f"{'=' * 60}\n")

    prompt = get_planner_prompt(
        requirement=state.get("requirement", ""),
        context=state.get("context", {}),
        memory_hints=memory_hints,
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
        "messages": [
            {"role": "assistant", "content": f"Case plan generated.\n{case_plan[:500]}"}
        ],
    }
