"""流式输出模块（#50 #51）。

支持 LangGraph 的 AstreamEvent 流式输出：
- stream_mode="messages": LLM Token 级打字机效果
- stream_mode="updates": 节点级进度更新
- stream_mode="custom": 自定义事件

用法：
    from .streaming import stream_graph_execution
    async for event in stream_graph_execution(graph, state, config):
        print(event)

CLI 流式输出：
    python -m src.agent.cli stream "测试 rocm-smi 命令"
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, AsyncIterator, Iterator

from .state import AgentState
from .logging_config import get_logger

_logger = get_logger("streaming")


async def stream_graph_execution(
    graph,
    state: AgentState,
    config: dict[str, Any],
    stream_mode: str = "updates",
) -> AsyncIterator[dict[str, Any]]:
    """异步流式执行图，返回事件流。

    支持三种流模式：
    - "messages": Token 级流式（需要 LLM 支持 streaming）
    - "updates": 节点级更新（每个节点完成后发送事件）
    - "custom": 自定义事件

    Args:
        graph: 编译后的 LangGraph CompiledGraph
        state: 初始状态
        config: 运行时配置（含 thread_id）
        stream_mode: 流模式

    Yields:
        流式事件字典
    """
    _logger.info("stream_start", mode=stream_mode)

    try:
        async for event in graph.astream(state, config=config, stream_mode=stream_mode):
            yield {"type": stream_mode, "data": event, "timestamp": time.time()}
    except Exception as exc:
        _logger.exception("stream_failed", error=str(exc))
        yield {"type": "error", "data": str(exc), "timestamp": time.time()}


def stream_graph_sync(
    graph,
    state: AgentState,
    config: dict[str, Any],
    stream_mode: str = "updates",
) -> Iterator[dict[str, Any]]:
    """同步流式执行图（用于非 async 环境如 pytest）。

    使用 graph.stream() 返回同步迭代器。
    """
    _logger.info("sync_stream_start", mode=stream_mode)

    try:
        for event in graph.stream(state, config=config, stream_mode=stream_mode):
            yield {"type": stream_mode, "data": event, "timestamp": time.time()}
    except Exception as exc:
        _logger.exception("sync_stream_failed", error=str(exc))
        yield {"type": "error", "data": str(exc), "timestamp": time.time()}


def format_stream_event(event: dict[str, Any], mode: str = "updates") -> str:
    """格式化流事件为可读字符串。"""
    etype = event.get("type", "unknown")
    data = event.get("data", {})

    if etype == "error":
        return f"[❌ ERROR] {data}"
    if mode == "updates":
        # 节点更新事件
        parts = []
        for node_name, node_output in data.items():
            if isinstance(node_output, dict):
                # 提取有意义的输出键
                keys = [
                    k for k in node_output
                    if k in ("parsed_intent", "case_plan", "generated_code",
                             "code", "execution_result")
                ]
                brief = ", ".join(
                    f"{k}={str(node_output[k])[:50]}" for k in keys[:3]
                )
                parts.append(f"  [{node_name}] {brief}")
            else:
                parts.append(f"  [{node_name}] {str(node_output)[:100]}")
        return "\n".join(parts) if parts else str(data)
    elif mode == "messages":
        # 消息事件
        msg = data
        if isinstance(msg, list):
            last = msg[-1] if msg else {}
            content = getattr(last, "content", str(last))
            return f"[MSG] {str(content)[:200]}"
        return f"[MSG] {str(msg)[:200]}"

    return str(data)[:200]
