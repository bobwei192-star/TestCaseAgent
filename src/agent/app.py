"""LangGraph Studio application entrypoint."""

from typing import Any

from src.agent.graph import build_graph
from src.agent.model import build_model
from src.agent.tracing import build_langfuse_config
from src.agent.tools import TOOLS


def build_studio_graph() -> Any:
    try:
        model = build_model()
    except RuntimeError:
        compiled_graph = build_graph(use_persistence=False)
    else:
        compiled_graph = build_graph(
            model=model,
            tools=TOOLS,
            use_persistence=False,
        )

    langfuse_config = build_langfuse_config(
        thread_id="langgraph-dev",
        tags=["langgraph-dev", "test-case-agent"],
    )
    if not langfuse_config:
        return compiled_graph

    return compiled_graph.with_config(langfuse_config)


# LangGraph Studio / langgraph dev 通过导入此变量加载图
graph = build_studio_graph()
