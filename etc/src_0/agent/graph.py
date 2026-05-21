from functools import partial

from deepagents.graph import create_deep_agent
from langgraph.graph import StateGraph, START, END

from .state import AgentState
from .nodes import coder, checker, router


def build_graph(model, tools=None):
    """构建 Test Case Agent 的 LangGraph 图。

    Args:
        model: LangChain ChatModel 实例
        tools: 可选的自定义工具列表

    Returns:
        编译好的 StateGraph
    """
    agent = create_deep_agent(
        model=model,
        tools=tools or [],
        system_prompt=(
            "你是一个测试用例生成专家。"
            "根据用户需求生成 pytest 格式的 Python 测试代码。"
            "代码必须完整可执行，包含必要的 import、fixture 和断言。"
            "只输出代码，不要额外解释。"
        ),
    )

    coder_with_agent = partial(coder, agent=agent)

    builder = StateGraph(AgentState)
    builder.add_node("coder", coder_with_agent)
    builder.add_node("checker", checker)

    builder.add_edge(START, "coder")
    builder.add_edge("coder", "checker")
    builder.add_conditional_edges(
        "checker",
        router,
        {"ok": END, "retry": "coder", "giveup": END},
    )

    return builder.compile()
