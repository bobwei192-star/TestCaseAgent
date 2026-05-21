"""
核心追踪策略（一句话版）

1. 别手动造轮子：Langfuse Python SDK v4 已转向 OpenTelemetry，手动 start_as_current_observation()
   维护成本高、易 break，且无法自动捕获节点内部的 LLM/Tool 调用。

2. 自动拦截才是正道：Langfuse 官方提供 CallbackHandler，利用 LangChain Callbacks 事件总线
   自动追踪 Node、Edge、LLM、Token、Latency，一行代码接入。

3. 本地审计不能丢：保留 dump_execution_trace() 只做本地 JSON + Mermaid 落盘，用于事后复盘
   和状态对比；Langfuse 云端 trace 负责可视化时间线。

4. 对标 LangSmith：LangSmith 纯环境变量零侵入；Langfuse 目前仍需显式传入 CallbackHandler，
   但追踪粒度（Node/Generation/Tool）完全一致。

5. 推荐组合：CallbackHandler 管云端自动上报，dump_execution_trace() 管本地文件归档，
   @observe() 装饰器管自定义非 LangChain 逻辑。三者互补，不重复。
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

try:
    from langfuse.langchain import CallbackHandler
except ImportError:
    CallbackHandler = None

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOTENV_PATH = PROJECT_ROOT / ".env"


def _build_langfuse_handler() -> Any | None:
    """Create Langfuse callback handler when credentials are configured."""
    if CallbackHandler is None:
        return None

    load_dotenv(dotenv_path=DOTENV_PATH)
    required_env = (
        "LANGFUSE_HOST",
        "LANGFUSE_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY",
    )
    if any(not os.environ.get(name) for name in required_env):
        return None

    return CallbackHandler()


# v3/v4 的 CallbackHandler 不接受 user_id/tags 等构造参数。
# 这些属性通过 invoke 时的 config["metadata"] 动态传入。
langfuse_handler = _build_langfuse_handler()


def build_langfuse_config(
    thread_id: str | None = None,
    tags: list[str] | None = None,
) -> dict[str, Any]:
    """Build LangGraph config that enables Langfuse tracing when configured.

    Args:
        thread_id: Optional user or thread identifier attached to Langfuse
            metadata.
        tags: Optional Langfuse tags.

    Returns:
        LangGraph runnable config. Empty when Langfuse is not configured.
    """
    if langfuse_handler is None:
        return {}

    metadata: dict[str, Any] = {
        "langfuse_tags": tags or ["langgraph", "test-case-agent"],
    }
    if thread_id:
        metadata["langfuse_user_id"] = thread_id

    return {
        "callbacks": [langfuse_handler],
        "metadata": metadata,
    }


def flush_langfuse() -> None:
    """Flush Langfuse observations when the installed SDK exposes a flush hook."""
    if langfuse_handler is None:
        return
    flush = getattr(langfuse_handler, "flush", None)
    if callable(flush):
        flush()


def _safe_json_value(value: Any, max_length: int = 2000) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        text = value
    else:
        text = str(value)

    if isinstance(text, str) and len(text) > max_length:
        return text[:max_length] + "...<<truncated>"
    return text


def dump_execution_trace(graph: Any, config: dict[str, Any], output_dir: str = "./traces") -> None:
    """只保留本地文件落盘，Langfuse 云端上报完全交给 CallbackHandler。"""
    trace_dir = Path(output_dir)
    trace_dir.mkdir(parents=True, exist_ok=True)

    try:
        graph_mmd = graph.get_graph(xray=True).draw_mermaid()
        (trace_dir / "graph.mmd").write_text(graph_mmd, encoding="utf-8")
    except Exception:
        pass

    history = list(graph.get_state_history(config))
    for index, state in enumerate(history):
        next_name = "_".join(state.next) if state.next else "end"
        payload = {
            "step": index,
            "next_node": state.next,
            "values": {
                key: _safe_json_value(value)
                for key, value in state.values.items()
            },
            "metadata": state.metadata,
        }
        (trace_dir / f"step_{index:03d}_{next_name}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )

    summary = {
        "total_steps": len(history),
        "nodes_visited": [state.next for state in history],
        "final_state_keys": list(history[-1].values.keys()) if history else [],
        "timestamp": datetime.now().astimezone().isoformat(),
    }
    (trace_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    print(f"Local trace saved to: {trace_dir}")