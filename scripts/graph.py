# graph.py
from functools import partial
from langgraph.graph import StateGraph, START, END

from .state import AgentState, AgentContext
from .nodes import (
    context_retriever, dry_run_executor, execution_planner,
    finalizer, generator, planner, repairer,
    requirement_parser, result_parser,
)


DEFAULT_SYSTEM_PROMPT = (
    "你是一个测试用例生成专家。"
    "你会先规划测试用例，再生成最小可执行的测试草案。"
    "一期 Agent 流程只做 dry-run，不在生成阶段执行 shell 命令；"
    "但最终生成的 pytest 代码必须是真实可执行测试，不能使用 mock output 或硬编码成功输出。"
)


def build_graph(
    model=None,
    tools=None,
    checkpointer=None,   # 默认 None
    store=None,        # 默认 None
    system_prompt: str | None = None,
):
    """构建 Test Case Agent 的 LangGraph 图。

    注意：在 LangGraph API / langgraph dev 模式下，不要传 store 和 checkpointer，
    持久化由平台自动管理。本地脚本调用时可传入。
    """
    agent = None
    if model is not None:
        from deepagents import create_deep_agent
        agent = create_deep_agent(
            model=model,
            tools=tools or [],
            system_prompt=system_prompt or DEFAULT_SYSTEM_PROMPT,
        )

    planner_with_agent = partial(planner, agent=agent)
    generator_with_agent = partial(generator, agent=agent)
    repairer_with_agent = partial(repairer, agent=agent)

    # ✅ 关键：增加 context_schema，Runtime 才能注入
    builder = StateGraph(AgentState, context_schema=AgentContext)

    builder.add_node("requirement_parser", requirement_parser)
    builder.add_node("context_retriever", context_retriever)
    builder.add_node("planner", planner_with_agent)
    builder.add_node("generator", generator_with_agent)
    builder.add_node("execution_planner", execution_planner)
    builder.add_node("dry_run_executor", dry_run_executor)
    builder.add_node("result_parser", result_parser)
    builder.add_node("repairer", repairer_with_agent)
    builder.add_node("finalizer", finalizer)

    builder.add_edge(START, "requirement_parser")
    builder.add_edge("requirement_parser", "context_retriever")
    builder.add_edge("context_retriever", "planner")
    builder.add_edge("planner", "generator")
    builder.add_edge("generator", "execution_planner")
    builder.add_edge("execution_planner", "dry_run_executor")
    builder.add_edge("dry_run_executor", "result_parser")
    builder.add_edge("result_parser", "repairer")
    builder.add_edge("repairer", "finalizer")
    builder.add_edge("finalizer", END)

    # ✅ 条件传参：LangGraph API 模式下不传，避免 ValueError
    compile_kwargs = {}
    if checkpointer is not None:
        compile_kwargs["checkpointer"] = checkpointer
    if store is not None:
        compile_kwargs["store"] = store

    return builder.compile(**compile_kwargs)