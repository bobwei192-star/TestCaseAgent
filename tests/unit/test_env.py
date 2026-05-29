"""环境校验测试。两部分：
1. .env 键值逻辑 — 检查选定的 provider 对应的密钥是否填写、Langfuse/LangGraph 配置是否完备。
2. 依赖可导入 — 检查 requirements.txt / pyproject.toml / install.sh 中记录的主力依赖是否可 import。
"""

import os
import re
from pathlib import Path

import pytest

# ── 常量 ──────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOTENV_PATH = PROJECT_ROOT / ".env"
DOTENV_EXAMPLE_PATH = PROJECT_ROOT / ".env.example"
VENV_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"


# ── 辅助 ──────────────────────────────────────────────────────────────────


def _load_dotenv_file(path: Path) -> dict[str, str]:
    """解析 .env 文件为 dict（忽略注释行和空行）。"""
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        env[key] = val
    return env


# ══════════════════════════════════════════════════════════════════════════
# Part 1 — .env 键值逻辑
# ══════════════════════════════════════════════════════════════════════════


class TestDotenvExists:
    def test_dotenv_file_exists(self):
        assert DOTENV_PATH.exists(), f".env 文件不存在: {DOTENV_PATH}"

    def test_dotenv_example_exists(self):
        assert DOTENV_EXAMPLE_PATH.exists(), f".env.example 文件不存在"


class TestDotenvRequiredKeys:
    """检查 .env 中关键键是否存在且值非空。"""

    @pytest.fixture(autouse=True)
    def env(self) -> dict[str, str]:
        return _load_dotenv_file(DOTENV_PATH)

    def test_runtime_keys_present(self, env):
        for key in (
            "TEST_CASE_AGENT_MODEL_PROVIDER",
            "TEST_CASE_AGENT_THREAD_ID",
            "TEST_CASE_AGENT_TRACE_DIR",
        ):
            assert key in env, f"缺少必需键: {key}"
            assert env[key], f"键 {key} 值为空"

    def test_provider_is_valid(self, env):
        provider = env["TEST_CASE_AGENT_MODEL_PROVIDER"].lower()
        valid = {"deepseek", "amd", "openai", "generic", "ark"}
        assert provider in valid, f"未知 provider: {provider}，应为 {valid}"

    def test_deepseek_keys_when_provider_selected(self, env):
        provider = env["TEST_CASE_AGENT_MODEL_PROVIDER"].lower()
        if provider != "deepseek":
            pytest.skip("当前 provider 非 deepseek")
        for key in ("DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL", "DEEPSEEK_MODEL"):
            assert key in env, f"缺少 DeepSeek 所需键: {key}"
            assert env[key], f"键 {key} 值不能为空"

    def test_langfuse_keys_present(self, env):
        has_public = bool(env.get("LANGFUSE_PUBLIC_KEY", ""))
        has_secret = bool(env.get("LANGFUSE_SECRET_KEY", ""))
        has_host = bool(env.get("LANGFUSE_HOST") or env.get("LANGFUSE_BASE_URL"))
        assert has_public, "缺少 LANGFUSE_PUBLIC_KEY"
        assert has_secret, "缺少 LANGFUSE_SECRET_KEY"
        assert has_host, "缺少 LANGFUSE_HOST 或 LANGFUSE_BASE_URL"

    def test_langfuse_host_format(self, env):
        url = env.get("LANGFUSE_HOST") or env.get("LANGFUSE_BASE_URL") or ""
        if not url:
            pytest.skip("Lanfuse URL 未配置")
        assert url.startswith("http"), f"Lanfuse URL 应以 http 开头: {url}"

    def test_langgraph_api_url_present(self, env):
        key = "LANGGRAPH_API_URL"
        assert key in env, f"缺少 {key}"
        assert env[key], f"{key} 值为空"
        assert env[key].startswith("http"), f"{key} 应以 http 开头: {env[key]}"

    def test_shared_llm_options_present(self, env):
        for key in ("LLM_TEMPERATURE", "LLM_REQUEST_TIMEOUT", "LLM_MAX_RETRIES"):
            assert key in env, f"缺少 {key}"
            try:
                float(env[key])
            except ValueError:
                pytest.fail(f"{key} 应为数字，实际值: {env[key]!r}")

    def test_api_key_not_placeholder(self, env):
        provider = env["TEST_CASE_AGENT_MODEL_PROVIDER"].lower()
        key_map = {
            "deepseek": "DEEPSEEK_API_KEY",
            "openai": "OPENAI_API_KEY",
            "amd": "AMD_LLM_SUBSCRIPTION_KEY",
        }
        api_key_name = key_map.get(provider)
        if not api_key_name:
            pytest.skip(f"不检查 generic provider 的 API Key 占位")
        val = env.get(api_key_name, "")
        if not val:
            pytest.skip(f"{api_key_name} 未填写，无法检查")
        placeholders = {
            "your",
            "changeme",
            "xxx",
            "dummy",
            "example",
            "your-api-key",
            "sk-your",
        }
        lower = val.lower()
        assert not any(p in lower for p in placeholders), (
            f"{api_key_name} 疑似占位符，请填写真实密钥。当前值: {val[:20]}..."
        )

    def test_example_vs_real_no_leaked_sensitive(self):
        example_env = _load_dotenv_file(DOTENV_EXAMPLE_PATH)
        real_env = _load_dotenv_file(DOTENV_PATH)
        assert "sk-" not in str(example_env.values()), (
            ".env.example 不应包含真实密钥，请确保已脱敏"
        )


# ══════════════════════════════════════════════════════════════════════════
# Part 2 — 依赖可导入
# ══════════════════════════════════════════════════════════════════════════


class TestDependenciesImportable:
    """验证 requirements.txt / pyproject.toml / install.sh 中记录的主力依赖可 import。"""

    @pytest.mark.parametrize(
        "module,import_path",
        [
            # ── LangGraph 家族 ──
            ("langgraph", "langgraph"),
            ("langchain", "langchain"),
            ("langchain_openai", "langchain_openai"),
            ("langchain_core", "langchain_core"),
            ("langchain_mcp_adapters", "langchain_mcp_adapters"),
            # ── LLM ──
            ("openai", "openai"),
            ("langfuse", "langfuse"),
            ("python-dotenv (dotenv)", "dotenv"),
            # ── Agent 框架 ──
            ("deepagents", "deepagents"),
            # ── 项目本身 ──
            ("test_case_agent (src)", "src.agent"),
            # ── 测试 ──
            ("pytest", "pytest"),
            ("pytest_asyncio", "pytest_asyncio"),
            # ── MCP ──
            ("mcp", "mcp"),
            # ── HuggingFace ──
            ("huggingface_hub", "huggingface_hub"),
        ],
    )
    def test_can_import(self, module, import_path):
        mod = __import__(import_path)
        assert mod is not None, f"无法导入 {module}"

    @pytest.mark.parametrize(
        "module,attribute",
        [
            ("langgraph.graph.StateGraph", "StateGraph"),
            ("langgraph.graph.START", "START"),
            ("langgraph.graph.END", "END"),
            ("langchain_openai.ChatOpenAI", "ChatOpenAI"),
            ("langchain_core.tools.tool", "tool"),
            ("langfuse.langchain.CallbackHandler", "CallbackHandler"),
            ("dotenv.load_dotenv", "load_dotenv"),
        ],
    )
    def test_import_key_attribute(self, module, attribute):
        mod = __import__(module.rsplit(".", 1)[0], fromlist=[attribute])
        assert hasattr(mod, attribute), f"{module} 中缺少 {attribute}"

    def test_venv_python_exists(self):
        assert VENV_PYTHON.exists(), (
            f"虚拟环境 Python 不存在: {VENV_PYTHON}。请执行: python3 -m venv .venv"
        )

    def test_venv_python_is_correct_version(self):
        import subprocess, sys

        result = subprocess.run(
            [str(VENV_PYTHON), "-c", "import sys; print(sys.version_info[:2])"],
            capture_output=True,
            text=True,
        )
        major_minor = result.stdout.strip()
        assert major_minor.startswith("(3, 12)") or major_minor.startswith("(3, 13)"), (
            f"需要 Python >= 3.12，当前: {major_minor}"
        )

    def test_langfuse_callbackhandler_importable(self):
        try:
            from langfuse.langchain import CallbackHandler

            assert CallbackHandler is not None
        except ImportError as exc:
            pytest.fail(f"langfuse.langchain.CallbackHandler 不可导入: {exc}")

    def test_langgraph_agent_can_import(self):
        """验证项目自己的 Agent 可以导入（但不依赖 LLM 密钥）。"""
        from src.agent.state import AgentState, AgentContext
        from src.agent.graph import build_graph

        g = build_graph()
        nodes = [n for n in g.get_graph().nodes.keys() if not n.startswith("__")]
        assert len(nodes) == 4, f"预期 4 个节点，实际: {len(nodes)}: {nodes}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
