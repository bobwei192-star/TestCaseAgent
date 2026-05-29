"""配置验证与管理模块 —— 启动时校验所有必需配置项，防止运行时 KeyError。

提供:
- ConfigSchema: 配置结构定义
- validate_config(): 启动时校验，打印缺失项
- get_config(): 获取类型安全的配置值
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ConfigSchema:
    """应用配置 schema，定义所有可选/必需配置项及其默认值。"""

    # === LLM Provider ===
    model_provider: str = "amd"
    llm_temperature: float = 0.2
    llm_request_timeout: int = 120
    llm_max_retries: int = 2

    # === Provider-specific ===
    amd_llm_base_url: str = "https://llm-api.amd.com/OnPrem"
    amd_llm_model: str = "GPT55"
    amd_llm_api_key: str = "dummy"
    amd_llm_subscription_key: str = ""
    amd_llm_user: str = ""

    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_model: str = "deepseek-chat"
    deepseek_api_key: str = ""

    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o"
    openai_api_key: str = ""

    ark_base_url: str = "https://ark.cn-beijing.volces.com/api/v3"
    ark_model: str = ""
    ark_api_key: str = ""

    llm_base_url: str = ""
    llm_model: str = ""
    llm_api_key: str = ""

    # === Langfuse ===
    langfuse_host: str = "http://localhost:3000"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""

    # === LangGraph ===
    langgraph_api_url: str = "http://127.0.0.1:2024"

    # === Sandbox ===
    sandbox_provider: str = "remote_ssh_docker"
    sandbox_image: str = "rocm/dev-ubuntu-22.04:6.0"
    remote_host: str = ""
    remote_user: str = "jenkins"
    remote_password: str = ""

    # === Runtime ===
    thread_id: str = "test-case-agent-debug"
    trace_dir: str = "traces/test-case-agent-debug"
    log_level: str = "INFO"
    output_dir: str = "test_case"

    @classmethod
    def from_env(cls) -> "ConfigSchema":
        """从环境变量构建配置对象。"""
        return cls(
            model_provider=os.getenv("TEST_CASE_AGENT_MODEL_PROVIDER", "amd"),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
            llm_request_timeout=int(os.getenv("LLM_REQUEST_TIMEOUT", "120")),
            llm_max_retries=int(os.getenv("LLM_MAX_RETRIES", "2")),
            amd_llm_base_url=os.getenv("AMD_LLM_BASE_URL", "https://llm-api.amd.com/OnPrem"),
            amd_llm_model=os.getenv("AMD_LLM_MODEL", "GPT55"),
            amd_llm_api_key=os.getenv("AMD_LLM_API_KEY", "dummy"),
            amd_llm_subscription_key=os.getenv("AMD_LLM_SUBSCRIPTION_KEY", ""),
            amd_llm_user=os.getenv("AMD_LLM_USER", ""),
            deepseek_base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
            deepseek_model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", ""),
            openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            ark_base_url=os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
            ark_model=os.getenv("ARK_MODEL", ""),
            ark_api_key=os.getenv("ARK_API_KEY", ""),
            llm_base_url=os.getenv("LLM_BASE_URL", ""),
            llm_model=os.getenv("LLM_MODEL", ""),
            llm_api_key=os.getenv("LLM_API_KEY", ""),
            langfuse_host=os.getenv("LANGFUSE_HOST", "http://localhost:3000"),
            langfuse_public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
            langfuse_secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
            langgraph_api_url=os.getenv("LANGGRAPH_API_URL", "http://127.0.0.1:2024"),
            sandbox_provider=os.getenv("TEST_CASE_AGENT_SANDBOX_PROVIDER", "remote_ssh_docker"),
            sandbox_image=os.getenv("TEST_CASE_AGENT_SANDBOX_IMAGE", "rocm/dev-ubuntu-22.04:6.0"),
            remote_host=os.getenv("TEST_CASE_AGENT_REMOTE_HOST", ""),
            remote_user=os.getenv("TEST_CASE_AGENT_REMOTE_USER", "jenkins"),
            remote_password=os.getenv("TEST_CASE_AGENT_REMOTE_PASSWORD", ""),
            thread_id=os.getenv("TEST_CASE_AGENT_THREAD_ID", "test-case-agent-debug"),
            trace_dir=os.getenv("TEST_CASE_AGENT_TRACE_DIR", "traces/test-case-agent-debug"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            output_dir=os.getenv("TEST_CASE_OUTPUT_DIR", "test_case"),
        )


def validate_config(config: Optional[ConfigSchema] = None) -> list[str]:
    """校验配置完整性，返回缺失/警告项列表。

    Args:
        config: 配置对象，为 None 时从环境变量构建

    Returns:
        警告信息列表，空列表表示配置完整
    """
    if config is None:
        config = ConfigSchema.from_env()

    warnings: list[str] = []
    provider = config.model_provider

    # 根据 provider 检查必需的 API 密钥
    if provider == "deepseek" and not config.deepseek_api_key:
        warnings.append("DEEPSEEK_API_KEY 未设置，DeepSeek provider 无法工作")
    elif provider == "openai" and not config.openai_api_key:
        warnings.append("OPENAI_API_KEY 未设置，OpenAI provider 无法工作")
    elif provider == "ark" and not config.ark_api_key:
        warnings.append("ARK_API_KEY 未设置，Ark provider 无法工作")
    elif provider == "amd":
        if not config.amd_llm_subscription_key:
            warnings.append("AMD_LLM_SUBSCRIPTION_KEY 未设置（可选，部分 API 需要）")

    if not config.remote_host and config.sandbox_provider == "remote_ssh_docker":
        warnings.append("TEST_CASE_AGENT_REMOTE_HOST 未设置，远程沙盒执行将使用默认值")

    return warnings


def print_config_warnings() -> bool:
    """打印配置警告，返回是否有致命警告。"""
    warnings = validate_config()
    if not warnings:
        return False

    print("\n⚠️  配置警告:")
    for w in warnings:
        print(f"  - {w}")
    print("  请检查 .env 文件配置。\n")
    return bool(warnings)


# 全局配置单例（惰性初始化）
_config: Optional[ConfigSchema] = None


def get_config() -> ConfigSchema:
    """获取全局配置单例（线程安全，惰性初始化）。"""
    global _config
    if _config is None:
        _config = ConfigSchema.from_env()
    return _config


def get_model_rotation_list() -> list[dict[str, str]]:
    """获取模型轮换降级列表（#32）。

    从环境变量 MODEL_ROTATION_LIST 读取 JSON 格式的降级链：
    '[{"provider":"deepseek","model":"deepseek-chat"},...]'

    未配置时返回空列表。
    """
    import json
    import os

    raw = os.getenv("MODEL_ROTATION_LIST", "")
    if not raw:
        return []

    try:
        chain = json.loads(raw)
        if isinstance(chain, list):
            return chain
    except json.JSONDecodeError:
        pass

    return []
