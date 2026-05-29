"""Sandbox execution node - 使用策略模式执行

根据 guide/09_promot优化.md 设计：
- 使用策略模式根据意图选择执行方式
- PytestStrategy: 执行 pytest 测试
- DockerBuildStrategy: 执行 docker build
- ExternalRunStrategy: 执行外部套件

支持的意图：
- GENERATE/APPEND/UPDATE/REFACTOR: 执行 pytest
- ENV_BUILD: 执行 docker build
- EXECUTE_EXTERNAL: 执行外部脚本
- DIAGNOSE/COVERAGE/PROBE: 查询类，不执行
"""

from __future__ import annotations

import os
from typing import Any

from langchain_core.messages import AIMessage

from ..sandbox import CommandResult, SandboxConfig, build_sandbox_client
from ..sandbox.feedback import build_feedback
from ..sandbox import strategy as sandbox_strategy
from ..sandbox.strategy import StrategyFactory
from ..state import AgentState
from ..intent_router import IntentType
from ..logging_config import get_logger

_logger = get_logger("nodes.sandbox_executor")

_REMOTE_DIR = "/tmp/testcase_agent"
_REMOTE_TEST_FILE = f"{_REMOTE_DIR}/test_generated.py"
_PYTHON_BIN_COMMAND = "PYTHON_BIN=$(command -v python3 || command -v python)"
_INSTALL_PYTEST_COMMAND = (
    f"{_PYTHON_BIN_COMMAND} && "
    'test -n "$PYTHON_BIN" && '
    '$PYTHON_BIN -m pytest --version >/dev/null 2>&1 || '
    '$PYTHON_BIN -m pip install pytest -q'
)
_RUN_PYTEST_COMMAND = (
    f"{_PYTHON_BIN_COMMAND} && "
    'test -n "$PYTHON_BIN" && '
    '$PYTHON_BIN -m pytest test_generated.py -v'
)


def _build_config(raw_config: dict[str, Any] | None) -> SandboxConfig:
    """Create a typed sandbox config from state data."""
    config = raw_config or {}
    env_vars = config.get("env_vars") or {}
    return SandboxConfig(
        provider=str(
            config.get("provider")
            or os.environ.get("TEST_CASE_AGENT_SANDBOX_PROVIDER")
            or "remote_ssh_docker"
        ),
        image=str(
            config.get("image")
            or os.environ.get("TEST_CASE_AGENT_SANDBOX_IMAGE")
            or "rocm/dev-ubuntu-22.04:6.0"
        ),
        timeout=int(config.get("timeout", 120)),
        block_network=bool(config.get("block_network", False)),
        env_vars={str(k): str(v) for k, v in env_vars.items()},
        remote_host=str(
            config.get("remote_host")
            or os.environ.get("TEST_CASE_AGENT_REMOTE_HOST")
            or ""
        ),
        remote_user=str(
            config.get("remote_user")
            or os.environ.get("TEST_CASE_AGENT_REMOTE_USER")
            or "jenkins"
        ),
        remote_password=str(
            config.get("remote_password")
            or os.environ.get("TEST_CASE_AGENT_REMOTE_PASSWORD")
            or ""
        ),
        remote_work_dir=str(
            config.get("remote_work_dir")
            or os.environ.get("TEST_CASE_AGENT_REMOTE_WORK_DIR")
            or "/tmp/testcase_agent"
        ),
        device_name=str(
            config.get("device_name")
            or os.environ.get("TEST_CASE_AGENT_DEVICE_NAME")
            or "/dev/kfd,/dev/dri"
        ),
    )


def _failure_update(
    *,
    state: AgentState,
    stage: str,
    error: str,
    config: SandboxConfig | None = None,
    command_result: CommandResult | None = None,
    sandbox_id: str = "",
    output: str = "",
) -> dict:
    """Build a consistent failed node update."""
    retry_count = int(state.get("sandbox_retry_count", 0))
    max_retries = int(state.get("max_sandbox_retries", 3))
    next_retry_count = min(retry_count + 1, max_retries)
    provider = config.provider if config else "unknown"

    feedback = build_feedback(
        stage=stage,
        error=error,
        retry_count=retry_count,
        max_retries=max_retries,
        command_result=command_result,
        output=output,
    )
    stdout = command_result.stdout if command_result else output
    stderr = command_result.stderr if command_result else ""
    exit_code = command_result.exit_code if command_result else 1

    _logger.warning(
        "sandbox_failure",
        stage=stage,
        error=error,
        retry=retry_count,
        max_retries=max_retries,
    )

    return {
        "execution_result": {
            "status": "failed",
            "stage": stage,
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code,
            "error": error,
            "provider": provider,
            "duration_seconds": (
                command_result.duration_seconds if command_result else 0.0
            ),
        },
        "sandbox_retry_count": next_retry_count,
        "feedback": feedback,
        "error_log": [f"[{stage}] {error}"],
        "sandbox_id": sandbox_id,
        "messages": [AIMessage(content=feedback)],
    }


def sandbox_executor(state: AgentState) -> dict:
    """Run generated code in an isolated sandbox using strategy pattern."""
    code = state.get("generated_code") or state.get("code") or ""
    if not code.strip():
        return _failure_update(
            state=state,
            stage="missing_code",
            error="generated_code is empty; sandbox execution cannot start.",
        )

    # 获取意图信息
    parsed_intent: IntentType = state.get("parsed_intent", "GENERATE")
    _logger.info("sandbox_executor_start", intent=parsed_intent)

    # 查询类意图不需要执行
    if parsed_intent in ["DIAGNOSE", "COVERAGE", "PROBE"]:
        return {
            "execution_result": {
                "status": "skipped",
                "stage": "query_intent",
                "message": f"意图 {parsed_intent} 是查询类，无需执行沙盒测试",
            },
            "feedback": "",
            "messages": [AIMessage(content=f"查询类意图 {parsed_intent}，跳过沙盒执行。")],
        }

    # 获取保存的文件路径
    saved_filepath = state.get("saved_filepath")

    # 使用策略模式执行
    strategy_result = sandbox_strategy.execute_with_strategy(
        intent=parsed_intent,
        artifact_path=saved_filepath,
        state=dict(state),
    )

    status = strategy_result.get("status", "failed")
    stdout = strategy_result.get("stdout", "")
    stderr = strategy_result.get("stderr", "")
    returncode = strategy_result.get("returncode", 1)

    if status == "success":
        _logger.info("sandbox_success", intent=parsed_intent)
        return {
            "execution_result": {
                "status": "success",
                "stage": f"{parsed_intent.lower()}_execution",
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": returncode,
                "error": None,
                "provider": "local",
                "duration_seconds": 0.0,
            },
            "feedback": "",
            "messages": [AIMessage(content=f"{parsed_intent} 执行成功。")],
        }
    else:
        errors = strategy_result.get("errors", [])
        return _failure_update(
            state=state,
            stage=f"{parsed_intent.lower()}_execution",
            error="\n".join(errors) if errors else "执行失败",
            command_result=CommandResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=returncode,
                duration_seconds=0.0,
            ),
        )
