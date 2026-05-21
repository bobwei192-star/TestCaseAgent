import copy
from collections.abc import Iterable
from typing import Any

from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

from .graph import build_graph
from .model import build_model
from .state import AgentState, AgentContext
from .tools import TOOLS


def create_initial_state(user_prompt: str) -> AgentState:
    return {
        "messages": [{"role": "user", "content": user_prompt}],
        "requirement": user_prompt,
        "context": {},
        "case_plan": "",
        "code": "",
        "generated_code": "",
        "validation_result": {},
        "execution_plan": {},
        "execution_result": {},
        "parsed_result": {},
        "repair_suggestion": "",
        "final_report": {},
        "retry": 0,
        "repair_count": 0,
        "session_id": "",
    }


def build_runnable_graph(
    provider: str | None = None,
    tools: list[Any] | None = None,
    enable_checkpoint: bool = True,
    enable_store: bool = True,
):
    """Build a model-backed graph for actual execution."""
    model = build_model(provider=provider)
    checkpointer = MemorySaver() if enable_checkpoint else None
    store = InMemoryStore() if enable_store else None
    
    return build_graph(
        model=model,
        tools=tools if tools is not None else TOOLS,
        checkpointer=checkpointer,
        store=store,
    )


def run_once(
    user_prompt: str,
    provider: str | None = None,
    thread_id: str = "test-case-agent-debug",
    enable_checkpoint: bool = True,
    enable_store: bool = True,
    user_id: str = "default_user",
    project_id: str | None = None,
) -> AgentState:
    graph = build_runnable_graph(
        provider=provider,
        enable_checkpoint=enable_checkpoint,
        enable_store=enable_store,
    )
    config = {"configurable": {"thread_id": thread_id}}
    context = AgentContext(user_id=user_id, project_id=project_id)
    return graph.invoke(create_initial_state(user_prompt), config=config, context=context)


def run_multi_turn(
    turns: list[str],
    provider: str | None = None,
    thread_id: str = "multi-turn-test",
    user_id: str = "default_user",
    project_id: str | None = None,
) -> list[AgentState]:
    """多轮对话：同一 thread，Agent 记住上下文。"""
    
    graph = build_runnable_graph(
        provider=provider,
        enable_checkpoint=True,   # ✅ 启用短期记忆
        enable_store=True,        # ✅ 启用长期记忆
    )
    config = {"configurable": {"thread_id": thread_id}}
    context = AgentContext(user_id=user_id, project_id=project_id)
    
    # 只初始化一次 state
    state: AgentState = {
        "messages": [],
        "requirement": "",
        "context": {},
        "case_plan": "",
        "code": "",
        "generated_code": "",
        "validation_result": {},
        "execution_plan": {},
        "execution_result": {},
        "parsed_result": {},
        "repair_suggestion": "",
        "final_report": {},
        "retry": 0,
        "repair_count": 0,
    }
    
    results = []
    for i, prompt in enumerate(turns):
        print(f"\n{'='*60}")
        print(f"TURN {i+1}: {prompt[:50]}...")
        print(f"{'='*60}")
        
        # 追加消息
        state["messages"].append({"role": "user", "content": prompt})
        state["requirement"] = prompt
        
        # 调用图
        state = graph.invoke(state, config=config, context=context)
        # ✅ 深拷贝后再追加，避免 results 里全是同一对象引用
        results.append(copy.deepcopy(state))
        
        last_msg = state["messages"][-1]
        content = last_msg.get("content", "") if isinstance(last_msg, dict) else str(last_msg)
        print(f"Assistant: {content[:300]}...")
    
    return results