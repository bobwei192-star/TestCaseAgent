"""Prometheus Metrics 指标采集模块（#35）。

提供：
- MetricsCollector: 单例指标收集器，追踪 LLM 调用次数、Token 用量、延迟、错误率
- get_metrics_collector(): 获取全局单例
- 与 structlog 日志协同工作，关键路径自动计数

用法：
    from .metrics import get_metrics_collector
    mc = get_metrics_collector()
    mc.record_llm_call(node="planner", duration=2.5, tokens=1500, success=True)
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any

from .logging_config import get_logger

_logger = get_logger("metrics")


@dataclass
class NodeMetrics:
    """单节点的指标统计。"""

    calls: int = 0
    failures: int = 0
    total_duration: float = 0.0
    total_tokens: int = 0


@dataclass
class MetricsCollector:
    """全局指标收集器（线程安全）。

    追踪每个节点的调用统计、延迟分布和错误率。
    可用于导出到 Prometheus 或其他监控系统。
    """

    _lock: threading.Lock = field(default_factory=threading.Lock)
    nodes: dict[str, NodeMetrics] = field(default_factory=dict)
    start_time: float = field(default_factory=time.time)

    # 全局计数器
    total_llm_calls: int = 0
    total_llm_failures: int = 0
    total_tokens_used: int = 0
    total_sandbox_executions: int = 0
    total_sandbox_failures: int = 0
    total_graph_executions: int = 0
    total_graph_failures: int = 0
    total_repair_loops: int = 0

    # 安全审查计数器
    total_security_reviews: int = 0
    total_security_blocks: int = 0

    def _ensure_node(self, name: str) -> NodeMetrics:
        if name not in self.nodes:
            self.nodes[name] = NodeMetrics()
        return self.nodes[name]

    def record_llm_call(
        self,
        node: str,
        duration: float,
        tokens: int = 0,
        success: bool = True,
    ) -> None:
        """记录一次 LLM 调用。"""
        with self._lock:
            nm = self._ensure_node(node)
            nm.calls += 1
            nm.total_duration += duration
            nm.total_tokens += tokens
            self.total_llm_calls += 1
            if not success:
                nm.failures += 1
                self.total_llm_failures += 1
            self.total_tokens_used += tokens

    def record_sandbox_execution(self, success: bool = True) -> None:
        """记录一次沙盒执行。"""
        with self._lock:
            self.total_sandbox_executions += 1
            if not success:
                self.total_sandbox_failures += 1

    def record_graph_execution(self, success: bool = True) -> None:
        """记录一次图执行。"""
        with self._lock:
            self.total_graph_executions += 1
            if not success:
                self.total_graph_failures += 1

    def record_repair_loop(self) -> None:
        """记录一次修复循环。"""
        with self._lock:
            self.total_repair_loops += 1

    def record_security_review(self, blocked: bool = False) -> None:
        """记录一次安全审查。"""
        with self._lock:
            self.total_security_reviews += 1
            if blocked:
                self.total_security_blocks += 1

    def snapshot(self) -> dict[str, Any]:
        """获取当前指标快照。"""
        with self._lock:
            return {
                "uptime_seconds": round(time.time() - self.start_time, 2),
                "llm_calls": self.total_llm_calls,
                "llm_failures": self.total_llm_failures,
                "llm_failure_rate": (
                    round(self.total_llm_failures / self.total_llm_calls, 4)
                    if self.total_llm_calls > 0
                    else 0.0
                ),
                "total_tokens_used": self.total_tokens_used,
                "sandbox_executions": self.total_sandbox_executions,
                "sandbox_failures": self.total_sandbox_failures,
                "sandbox_failure_rate": (
                    round(self.total_sandbox_failures / self.total_sandbox_executions, 4)
                    if self.total_sandbox_executions > 0
                    else 0.0
                ),
                "graph_executions": self.total_graph_executions,
                "graph_failures": self.total_graph_failures,
                "repair_loops": self.total_repair_loops,
                "security_reviews": self.total_security_reviews,
                "security_blocks": self.total_security_blocks,
                "nodes": {
                    name: {
                        "calls": nm.calls,
                        "failures": nm.failures,
                        "avg_duration": round(nm.total_duration / nm.calls, 3) if nm.calls > 0 else 0,
                        "avg_tokens": round(nm.total_tokens / nm.calls, 1) if nm.calls > 0 else 0,
                    }
                    for name, nm in self.nodes.items()
                },
            }


_collector: MetricsCollector | None = None
_collector_lock = threading.Lock()


def get_metrics_collector() -> MetricsCollector:
    """获取全局指标收集器单例（线程安全）。"""
    global _collector
    if _collector is None:
        with _collector_lock:
            if _collector is None:
                _collector = MetricsCollector()
    return _collector


def reset_metrics() -> None:
    """重置全局指标（主要用于测试）。"""
    global _collector
    with _collector_lock:
        _collector = MetricsCollector()
