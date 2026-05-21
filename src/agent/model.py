import os
from dataclasses import dataclass

from langchain_openai import ChatOpenAI


@dataclass(frozen=True)
class ModelConfig:
    """OpenAI-compatible chat model configuration."""

    model: str
    base_url: str
    api_key: str
    temperature: float = 0.2
    subscription_key: str | None = None
    user: str | None = None


def _optional_load_dotenv() -> None:
    """Load .env when python-dotenv is installed."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv()


def build_model_config(provider: str | None = None) -> ModelConfig:
    """Build model configuration from environment variables.

    Args:
        provider: Model provider name. Supported values are ``amd``,
            ``deepseek``, ``openai`` and ``generic``. If omitted, reads
            ``TEST_CASE_AGENT_MODEL_PROVIDER`` and falls back to ``amd``.

    Returns:
        ModelConfig used by ``build_model``.

    Raises:
        RuntimeError: If the selected provider lacks required credentials.
    """
    _optional_load_dotenv()
    selected_provider = (
        provider
        or os.environ.get("TEST_CASE_AGENT_MODEL_PROVIDER")
        or os.environ.get("LLM_PROVIDER")
    )
    if not selected_provider:
        selected_provider = "amd"
    selected_provider = selected_provider.lower()

    if selected_provider == "deepseek":
        api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("LLM_API_KEY")
        if not api_key:
            raise RuntimeError("Missing DEEPSEEK_API_KEY or LLM_API_KEY.")
        return ModelConfig(
            model=(
                os.environ.get("DEEPSEEK_MODEL")
                or os.environ.get("LLM_MODEL_ID")
                or os.environ.get("LLM_MODEL")
                or "deepseek-chat"
            ),
            base_url=os.environ.get("DEEPSEEK_BASE_URL")
            or os.environ.get("LLM_BASE_URL")
            or "https://api.deepseek.com/v1",
            api_key=api_key,
            temperature=float(os.environ.get("LLM_TEMPERATURE", "0.2")),
        )

    if selected_provider == "amd":
        subscription_key = os.environ.get("AMD_LLM_SUBSCRIPTION_KEY")
        if not subscription_key:
            raise RuntimeError("Missing AMD_LLM_SUBSCRIPTION_KEY.")
        return ModelConfig(
            model=os.environ.get("AMD_LLM_MODEL", "GPT55"),
            base_url=os.environ.get("AMD_LLM_BASE_URL", "https://llm-api.amd.com/OnPrem"),
            api_key=os.environ.get("AMD_LLM_API_KEY", "dummy"),
            temperature=float(os.environ.get("LLM_TEMPERATURE", "0.2")),
            subscription_key=subscription_key,
            user=os.environ.get("AMD_LLM_USER") or os.environ.get("USER"),
        )

    if selected_provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Missing OPENAI_API_KEY.")
        return ModelConfig(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
            base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            api_key=api_key,
            temperature=float(os.environ.get("LLM_TEMPERATURE", "0.2")),
        )

    api_key = os.environ.get("LLM_API_KEY")
    base_url = os.environ.get("LLM_BASE_URL")
    model = os.environ.get("LLM_MODEL")
    if not api_key or not base_url or not model:
        raise RuntimeError("Generic provider requires LLM_API_KEY, LLM_BASE_URL and LLM_MODEL.")
    return ModelConfig(
        model=model,
        base_url=base_url,
        api_key=api_key,
        temperature=float(os.environ.get("LLM_TEMPERATURE", "0.2")),
    )


def build_model(provider: str | None = None):
    """Create a ChatOpenAI-compatible model from environment variables."""
    config = build_model_config(provider=provider)
    default_headers = None
    if config.subscription_key:
        default_headers = {
            "Ocp-Apim-Subscription-Key": config.subscription_key,
        }
        if config.user:
            default_headers["user"] = config.user

    return ChatOpenAI(
        model=config.model,
        base_url=config.base_url,
        api_key=config.api_key,
        temperature=config.temperature,
        default_headers=default_headers,
        request_timeout=int(os.environ.get("LLM_REQUEST_TIMEOUT", "120")),
        max_retries=int(os.environ.get("LLM_MAX_RETRIES", "2")),
    )