"""全局测试 fixtures 和 conftest 配置（#23）。

提供：
- 通用 mock LLM fixture：mock_llm、mock_model
- 通用 mock Runtime fixture：mock_runtime
- 通用 AgentState fixture：base_state
- 环境变量临时设置 helper
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock

# 确保项目根目录在 sys.path 中
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def mock_llm():
    """模拟 LLM agent，可被节点调用 invoke()。"""
    llm = Mock()
    msg = Mock()
    msg.content = "mock response"
    llm.invoke.return_value = {"messages": [msg]}
    return llm


@pytest.fixture
def mock_model():
    """模拟底层 model（ChatOpenAI 兼容）。"""
    model = Mock()
    msg = Mock()
    msg.content = "```python\ndef test_x(): pass\n```"
    model.invoke.return_value = msg
    return model


@pytest.fixture
def mock_runtime():
    """模拟 LangGraph Runtime。"""
    runtime = Mock()
    runtime.context.user_id = "test_user"
    runtime.context.project_id = "test_project"
    return runtime


@pytest.fixture
def base_state():
    """基础 AgentState fixture，所有必需字段已初始化。"""
    from langchain_core.messages import HumanMessage
    from src.agent.state import AgentState

    return {
        "messages": [HumanMessage(content="测试 rocm-smi 命令")],
        "requirement": "测试 rocm-smi 命令的存在性和正确性",
        "parsed_requirement": "",
        "parsed_intent": "GENERATE",
        "intent": "GENERATE",
        "intent_cluster": "create",
        "cluster": "create",
        "template_name": "template_a",
        "context": {},
        "case_plan": "",
        "code": "",
        "generated_code": "",
        "explanation": "",
        "validation_result": {},
        "execution_plan": {},
        "execution_result": {},
        "parsed_result": {},
        "repair_suggestion": "",
        "final_report": {},
        "retry": 0,
        "repair_count": 0,
        "saved_filepath": "",
        "sandbox_config": {"provider": "local", "timeout": 30},
        "sandbox_id": "",
        "sandbox_retry_count": 0,
        "max_sandbox_retries": 3,
        "feedback": "",
        "error_log": [],
        "session_id": "test-session",
    }


@pytest.fixture
def sandbox_state():
    """带沙盒执行结果的 state fixture。"""
    from langchain_core.messages import HumanMessage

    return {
        "messages": [HumanMessage(content="test")],
        "requirement": "test",
        "execution_result": {"status": "success", "stage": "test", "error": None},
        "sandbox_retry_count": 0,
        "max_sandbox_retries": 3,
        "generated_code": "import subprocess\ndef test_x(): pass",
        "code": "import subprocess\ndef test_x(): pass",
        "parsed_intent": "GENERATE",
        "feedback": "",
        "error_log": [],
        "sandbox_id": "",
    }


@pytest.fixture(autouse=True)
def reset_metrics():
    """每个测试前重置 metrics 计数器。"""
    from src.agent.metrics import reset_metrics as _reset
    _reset()


@pytest.fixture
def temp_env():
    """临时设置环境变量的上下文管理器。

    用法：
        with temp_env(KEY="value"):
            # KEY 在这一段内被设置为 "value"
    """
    import contextlib

    @contextlib.contextmanager
    def _set(**kwargs):
        old = {k: os.environ.get(k) for k in kwargs}
        try:
            os.environ.update({k: str(v) for k, v in kwargs.items()})
            yield
        finally:
            for k, old_val in old.items():
                if old_val is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = old_val

    return _set
