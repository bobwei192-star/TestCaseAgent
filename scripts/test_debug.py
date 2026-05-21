#!/usr/bin/env python3
import os
import traceback

from src.agent.runner import build_runnable_graph, create_initial_state
from src.agent.tracing import build_langfuse_config, dump_execution_trace, flush_langfuse


DEFAULT_PROMPT = "先告诉我你是哪个模型,然后为 ROCm 基础环境生成一个 pytest 测试用例，验证当前机器能正常执行 rocminfo，并检查输出中至少包含一个 GPU agent、设备名称和 ISA 信息。如果 rocminfo 不存在，应标记为 skipped，而不是直接 fail"


def _message_content(message) -> str:
    """Return content from dict or LangChain message."""
    if isinstance(message, dict):
        return str(message.get("content", ""))
    return str(getattr(message, "content", ""))


def main() -> None:
    """Run a minimal Test Case Agent debug flow."""
    provider = os.environ.get("TEST_CASE_AGENT_MODEL_PROVIDER")
    prompt = os.environ.get("TEST_CASE_AGENT_DEBUG_PROMPT", DEFAULT_PROMPT)
    thread_id = os.environ.get("TEST_CASE_AGENT_THREAD_ID", "test-case-agent-debug")
    trace_dir = os.environ.get("TEST_CASE_AGENT_TRACE_DIR", f"traces/{thread_id}")

    print(">>> 0. 构建 graph...")
    graph = build_runnable_graph(provider=provider, enable_checkpoint=True)

    config = {
        "configurable": {"thread_id": thread_id},
    }
    config.update(build_langfuse_config(thread_id=thread_id))

    initial_state = create_initial_state(prompt)

    print(">>> 1. 开始调用 graph.invoke...")
    result = graph.invoke(initial_state, config=config)

    print(">>> 2. 调用完成")
    for index, message in enumerate(result["messages"]):
        print(f"[message {index}] {_message_content(message)[:120]}...")

    print(f"\n需求:\n{result.get('requirement', '')[:300]}")
    print(f"\n测试计划:\n{result.get('case_plan', '')[:800]}")
    print(f"\n代码:\n{(result.get('generated_code') or result.get('code', ''))[:800]}")
    print(f"\n执行计划:\n{result.get('execution_plan', {})}")
    print(f"\n执行结果:\n{result.get('execution_result', {})}")
    print(f"\n修复建议:\n{result.get('repair_suggestion', '')[:500]}")
    print(f"\n最终报告:\n{result.get('final_report', {})}")
    print(f"重试: {result.get('retry', 0)}")
    print(f"修复次数: {result.get('repair_count', 0)}")

    dump_execution_trace(graph, config, output_dir=trace_dir)
    flush_langfuse()
    print(f">>> trace 已保存到: {trace_dir}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        raise