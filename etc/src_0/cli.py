"""Test Case Agent 命令行入口。

用法:
    python -m src.cli generate "为 rocBLAS sgemm 生成功能测试"
    python -m src.cli chat
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from .agent.graph import build_graph
from .agent.tools import TOOLS

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIR = PROJECT_ROOT / "generated_cases"


def get_model():
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL_ID", "deepseek-chat"),
        base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1"),
        api_key=os.getenv("LLM_API_KEY", "sk-placeholder"),
        temperature=0.2,
    )


def generate(requirement: str):
    """单次生成模式：给定需求，生成测试代码并落盘。"""
    print(f"\U0001f4dd 需求: {requirement}")
    print("\u23f3 正在生成...")

    graph = build_graph(model=get_model(), tools=TOOLS)
    result = graph.invoke({
        "messages": [{"role": "user", "content": requirement}],
        "code": "",
        "retry": 0,
    })

    code = result.get("code", "")
    retry = result.get("retry", 0)

    print(f"\n{'='*60}")
    for msg in result["messages"]:
        role = "\U0001f464" if msg["role"] == "user" else "\U0001f916"
        content = str(msg.get("content", ""))
        if len(content) > 200:
            content = content[:200] + "..."
        print(f"{role} {content}")

    if code:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = requirement[:40].replace(" ", "_").replace("/", "_")
        filename = f"test_{safe_name}_{timestamp}.py"
        filepath = GENERATED_DIR / filename
        GENERATED_DIR.mkdir(parents=True, exist_ok=True)

        header = (
            f"# 自动生成于 {datetime.now().isoformat()}\n"
            f"# 需求: {requirement}\n\n"
        )
        filepath.write_text(header + code, encoding="utf-8")
        print(f"\n\U0001f4be 已保存: {filepath}")
    else:
        print(f"\n\u274c 未生成有效代码 (重试 {retry} 次)")

    return code


def chat():
    """交互式对话模式。"""
    print("=" * 60)
    print("  Test Case Agent - 交互模式")
    print("  输入需求，Agent 生成 pytest 测试代码")
    print("  输入 'quit' 或 'exit' 退出")
    print("=" * 60)

    model = get_model()
    graph = build_graph(model=model, tools=TOOLS)

    while True:
        try:
            user_input = input("\n\U0001f464 你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\U0001f44b 再见!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("\U0001f44b 再见!")
            break

        print("\u23f3 正在生成...")
        result = graph.invoke({
            "messages": [{"role": "user", "content": user_input}],
            "code": "",
            "retry": 0,
        })

        code = result.get("code", "")
        for msg in result["messages"]:
            if msg["role"] == "assistant":
                content = str(msg.get("content", ""))
                print(f"\n\U0001f916 Agent: {content}")

        if code:
            print(f"\n--- 生成代码 ---")
            print(code)
            print("--- 结束 ---")

            save = input("\n\U0001f4be 是否保存? [y/N]: ").strip().lower()
            if save == "y":
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = user_input[:40].replace(" ", "_").replace("/", "_")
                filename = f"test_{safe_name}_{timestamp}.py"
                filepath = GENERATED_DIR / filename
                GENERATED_DIR.mkdir(parents=True, exist_ok=True)

                header = (
                    f"# 自动生成于 {datetime.now().isoformat()}\n"
                    f"# 需求: {user_input}\n\n"
                )
                filepath.write_text(header + code, encoding="utf-8")
                print(f"\u2705 已保存: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Test Case Agent - 自动生成 pytest 测试用例",
    )
    subparsers = parser.add_subparsers(dest="command")

    gen_parser = subparsers.add_parser("generate", help="单次生成模式")
    gen_parser.add_argument("requirement", help="测试需求描述")

    subparsers.add_parser("chat", help="交互式对话模式")

    args = parser.parse_args()

    if args.command == "generate":
        generate(args.requirement)
    elif args.command == "chat":
        chat()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
