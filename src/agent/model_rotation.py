"""模型轮换与降级模块（#32）。

当 LLM 调用失败时自动尝试备用模型列表，支持：
1. 主模型 → 备用模型 1 → 备用模型 2 → ... 的链式降级
2. 按优先级尝试不同 provider/model 组合
3. 同一 provider 下不同 model 的轮换

配置：
    MODEL_ROTATION_LIST 环境变量（JSON 格式）定义降级链：
    '[
      {"provider": "deepseek", "model": "deepseek-chat"},
      {"provider": "openai", "model": "gpt-4o-mini"},
      {"provider": "ark", "model": "doubao-lite-32k"}
    ]'

用法：
    from .model_rotation import ModelRotation
    rotation = ModelRotation()
    for entry in rotation.fallback_chain():
        try:
            result = call_llm(provider=entry["provider"], model=entry["model"])
            break
        except Exception:
            continue
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

from .logging_config import get_logger

_logger = get_logger("model_rotation")


@dataclass
class ModelEntry:
    """单个模型条目。"""

    provider: str
    model: str
    base_url: str = ""
    api_key: str = ""


@dataclass
class ModelRotation:
    """模型轮换管理器。

    从环境变量 MODEL_ROTATION_LIST 读取降级链配置，
    提供 fallback_chain() 生成器按优先级依次尝试。
    """

    entries: list[ModelEntry] = field(default_factory=list)
    current_index: int = 0

    def __post_init__(self) -> None:
        if not self.entries:
            self.entries = self._from_env()

    @staticmethod
    def _from_env() -> list[ModelEntry]:
        raw = os.getenv("MODEL_ROTATION_LIST", "")
        if not raw:
            return []

        try:
            chain = json.loads(raw)
        except json.JSONDecodeError:
            _logger.warning("model_rotation_parse_failed", raw=raw[:100])
            return []

        entries: list[ModelEntry] = []
        for item in chain:
            if not isinstance(item, dict):
                continue
            entries.append(ModelEntry(
                provider=item.get("provider", ""),
                model=item.get("model", ""),
                base_url=item.get("base_url", ""),
                api_key=item.get("api_key", ""),
            ))

        _logger.info("model_rotation_configured", count=len(entries))
        return entries

    def fallback_chain(self):
        """生成器：依次 yield 每个可用的模型配置。

        每次 yield 返回 dict：
            {"provider": str, "model": str, "base_url": str, "api_key": str}
        """
        if not self.entries:
            _logger.debug("model_rotation_empty")
            return

        for i, entry in enumerate(self.entries):
            _logger.info(
                "model_rotation_try",
                index=i + 1,
                total=len(self.entries),
                provider=entry.provider,
                model=entry.model,
            )
            yield {
                "provider": entry.provider,
                "model": entry.model,
                "base_url": entry.base_url,
                "api_key": entry.api_key,
            }

    def __bool__(self) -> bool:
        return bool(self.entries)

    def __len__(self) -> int:
        return len(self.entries)
