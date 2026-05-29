import copy
import os
import time
from collections.abc import Iterable
from typing import Any

from langchain_core.messages import HumanMessage

from .graph import build_graph
from .model import build_model
from .state import AgentState, AgentContext
from .tools import TOOLS
from .tracing import build_langfuse_config, flush_langfuse
from .logging_config import get_logger
from .config import get_config, print_config_warnings

# Initialize logger
logger = get_logger("runner")


def create_initial_state(user_prompt: str) -> AgentState:
    return {
        "messages": [HumanMessage(content=user_prompt)],
        "requirement": user_prompt,
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
        "sandbox_config": {
            "provider": os.environ.get(
                "TEST_CASE_AGENT_SANDBOX_PROVIDER", "remote_ssh_docker"
            ),
            "image": os.environ.get(
                "TEST_CASE_AGENT_SANDBOX_IMAGE",
                "rocm/dev-ubuntu-22.04:6.0",
            ),
            "block_network": False,
            "timeout": 120,
            "remote_host": os.environ.get(
                "TEST_CASE_AGENT_REMOTE_HOST", ""
            ),
            "remote_user": os.environ.get("TEST_CASE_AGENT_REMOTE_USER", "jenkins"),
            "remote_work_dir": os.environ.get(
                "TEST_CASE_AGENT_REMOTE_WORK_DIR", "/tmp/testcase_agent"
            ),
            "device_name": os.environ.get(
                "TEST_CASE_AGENT_DEVICE_NAME", "/dev/kfd,/dev/dri"
            ),
        },
        "sandbox_id": "",
        "sandbox_retry_count": 0,
        "max_sandbox_retries": 3,
        "feedback": "",
        "error_log": [],
        "session_id": "",
    }


def build_runnable_graph(
    provider: str | None = None,
    tools: list[Any] | None = None,
    enable_checkpoint: bool = True,
    enable_store: bool = True,
):
    """Build a model-backed graph for actual execution."""
    model = build_model(provider=provider)
    # graph.py 内部自动选择 MemorySaver 或 PostgreSQL Checkpointer/Store
    return build_graph(
        model=model,
        tools=tools if tools is not None else TOOLS,
        checkpointer=None,  # auto-select in build_graph
        store=None,  # auto-select in build_graph
    )


def build_runtime_config(thread_id: str) -> dict[str, Any]:
    """Build LangGraph invoke config with checkpoint and tracing metadata."""
    config: dict[str, Any] = {"configurable": {"thread_id": thread_id}}
    config.update(build_langfuse_config(thread_id=thread_id))
    return config


def run_once(
    user_prompt: str,
    provider: str | None = None,
    thread_id: str = "test-case-agent-debug",
    enable_checkpoint: bool = True,
    enable_store: bool = True,
    user_id: str = "default_user",
    project_id: str | None = None,
) -> AgentState:
    # 启动时校验配置
    print_config_warnings()

    start_time = time.time()
    logger.info(
        "run_once_start",
        user_prompt=user_prompt[:100] + "..." if len(user_prompt) > 100 else user_prompt,
        provider=provider,
        thread_id=thread_id,
        user_id=user_id,
        project_id=project_id,
    )

    try:
        graph = build_runnable_graph(
            provider=provider,
            enable_checkpoint=enable_checkpoint,
            enable_store=enable_store,
        )
        logger.debug("graph_built", provider=provider)

        config = build_runtime_config(thread_id=thread_id)
        context = AgentContext(user_id=user_id, project_id=project_id)

        logger.debug("invoking_graph", thread_id=thread_id)
        result = graph.invoke(
            create_initial_state(user_prompt), config=config, context=context
        )

        elapsed = time.time() - start_time
        generated_code = result.get("generated_code", "") or result.get("code", "")
        logger.info(
            "run_once_complete",
            elapsed=round(elapsed, 2),
            code_length=len(generated_code),
            has_code=bool(generated_code),
            validation_status=result.get("validation_result", {}).get("status"),
            errors=result.get("error_log", []),
        )

        return result
    except Exception as e:
        elapsed = time.time() - start_time
        logger.exception(
            "run_once_failed",
            elapsed=round(elapsed, 2),
            error=str(e),
            user_prompt=user_prompt[:100] if user_prompt else "",
        )
        raise
    finally:
        flush_langfuse()


def run_multi_turn(
    turns: list[str],
    provider: str | None = None,
    thread_id: str = "multi-turn-test",
    user_id: str = "default_user",
    project_id: str | None = None,
) -> list[AgentState]:
    """多轮对话：同一 thread，Agent 记住上下文。

    修复要点：
    1. 第一轮传入完整初始状态。
    2. 后续轮次只传入增量更新（新消息 + requirement），
       让 Checkpointer 自动恢复历史状态，避免 messages 重复累积。
    3. 每轮结束后深拷贝保存结果，避免引用污染。
    """
    graph = build_runnable_graph(
        provider=provider,
        enable_checkpoint=True,  # ✅ 启用短期记忆
        enable_store=True,  # ✅ 启用长期记忆
    )
    config = build_runtime_config(thread_id=thread_id)
    context = AgentContext(user_id=user_id, project_id=project_id)

    results = []
    try:
        for i, prompt in enumerate(turns):
            print(f"\n{'=' * 60}")
            print(f"TURN {i + 1}: {prompt[:50]}...")
            print(f"{'=' * 60}")

            if i == 0:
                # 第一轮：传入完整初始状态
                state = create_initial_state(prompt)
            else:
                # 后续轮次：只传增量更新。
                # Checkpointer 会自动恢复该 thread_id 的历史状态，
                # messages 通过 add_messages 追加，requirement 直接覆盖。
                state = {
                    "messages": [HumanMessage(content=prompt)],
                    "requirement": prompt,
                }

            # 调用图
            final_state = graph.invoke(state, config=config, context=context)
            # ✅ 深拷贝后再追加，避免 results 里全是同一对象引用
            results.append(copy.deepcopy(final_state))

            last_msg = final_state["messages"][-1]
            content = (
                last_msg.content
                if hasattr(last_msg, "content")
                else str(last_msg)
            )
            print(f"Assistant: {content[:300]}...")

        return results
    finally:
        flush_langfuse()
