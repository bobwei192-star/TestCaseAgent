"""Subgraph 路由模式（#49）。

按意图聚类将请求分发到不同的子图：
- create (GENERATE/APPEND): 标准生成子图
- modify (UPDATE/REFACTOR/FIX): 修改修复子图
- query (DIAGNOSE/COVERAGE/PROBE): 查询子图
- external (EXECUTE_EXTERNAL): 外部执行子图
- build (ENV_BUILD): 环境构建子图

用法：
    from .subgraph import build_subgraph_router
    graph, router = build_subgraph_router()

当前为简化实现，使用单图 + 条件路由模拟子图分发。
完全拆分需要 LangGraph 1.0+ 的 Subgraph API，后续迭代。
"""

from __future__ import annotations

from typing import Any

from .state import AgentState
from .logging_config import get_logger

_logger = get_logger("subgraph")

# 意图聚类 → 子图映射规则
INTENT_CLUSTER_MAP: dict[str, str] = {
    "create": "standard_gen_graph",
    "modify": "modify_graph",
    "query": "query_graph",
    "external": "external_graph",
    "build": "build_graph",
}


def route_to_subgraph(state: AgentState) -> str:
    """根据意图聚类路由到对应子图。

    这是一个条件路由函数，用于在 graph 中将不同意图
    分发到不同的处理节点。

    Returns:
        子图名称字符串
    """
    cluster = state.get("intent_cluster", "") or state.get("cluster", "")
    if not cluster:
        # 回退：从 intent 推断
        intent = state.get("parsed_intent", "") or state.get("intent", "")
        if intent in ("GENERATE", "APPEND"):
            cluster = "create"
        elif intent in ("UPDATE", "REFACTOR"):
            cluster = "modify"
        elif intent in ("DIAGNOSE", "COVERAGE", "PROBE"):
            cluster = "query"
        elif intent == "EXECUTE_EXTERNAL":
            cluster = "external"
        elif intent == "ENV_BUILD":
            cluster = "build"

    subgraph_name = INTENT_CLUSTER_MAP.get(cluster, "standard_gen_graph")
    _logger.info("subgraph_route", cluster=cluster, target=subgraph_name)

    return subgraph_name
