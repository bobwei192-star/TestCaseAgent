#!/usr/bin/env python3
"""调试脚本：调用 langgraph dev 并打印完整流事件。"""

import json
import sys
import time
from typing import Any

import requests


class LangGraphDevDebugger:
    """LangGraph dev SSE 调试客户端。"""

    def __init__(
        self,
        api_url: str = "http://127.0.0.1:2024",
        assistant_id: str = "test_case_agent",
    ) -> None:
        """初始化调试客户端。

        Args:
            api_url: LangGraph dev 服务地址。
            assistant_id: LangGraph assistant ID。
        """
        self.api_url = api_url.rstrip("/")
        self.assistant_id = assistant_id

    def run(
        self,
        prompt: str,
        thread_id: str,
        user_id: str,
        project_id: str,
    ) -> None:
        """发起流式请求并打印所有事件。

        Args:
            prompt: 用户需求文本。
            thread_id: LangGraph thread ID。
            user_id: 长期记忆用户 ID。
            project_id: 长期记忆项目 ID。
        """
        url = f"{self.api_url}/runs/stream"
        payload = self._build_payload(prompt, thread_id, user_id, project_id)

        print(f"Sending: {prompt[:80]}...")
        print(f"thread_id={thread_id}, user_id={user_id}, project_id={project_id}")
        print(f"stream_mode={payload['stream_mode']}\n")

        with requests.post(
            url,
            json=payload,
            stream=True,
            headers={"Accept": "text/event-stream"},
            timeout=300,
        ) as response:
            print(f"HTTP {response.status_code}")
            if response.status_code >= 400:
                print(response.text[:2000])
            response.raise_for_status()
            self._consume_sse(response)

        print("\n=== 请求完成 ===")

    def _build_payload(
        self,
        prompt: str,
        thread_id: str,
        user_id: str,
        project_id: str,
    ) -> dict[str, Any]:
        """构建 LangGraph API 请求体。"""
        return {
            "assistant_id": self.assistant_id,
            "stream_mode": ["updates", "values"],
            "input": {
                "messages": [{"role": "user", "content": prompt}],
                "requirement": prompt,
            },
            "context": {
                "user_id": user_id,
                "project_id": project_id,
                "thread_id": thread_id,
            },
        }

    def _consume_sse(self, response: requests.Response) -> None:
        """逐行消费 SSE，兼容 CRLF/LF 分隔并打印每个事件。"""
        event_type = "message"
        data_lines: list[str] = []
        event_count = 0

        for line in response.iter_lines(decode_unicode=True):
            if line is None:
                continue

            if line == "":
                if data_lines:
                    event_count += 1
                    self._handle_event(event_count, event_type, "\n".join(data_lines))
                    event_type = "message"
                    data_lines = []
                continue

            if line.startswith("event:"):
                event_type = line.removeprefix("event:").strip()
            elif line.startswith("data:"):
                data_lines.append(line.removeprefix("data:").strip())
            else:
                print(f"[SSE RAW] {line}")

        if data_lines:
            event_count += 1
            self._handle_event(event_count, event_type, "\n".join(data_lines))

        print(f"\nTotal events: {event_count}")

    def _handle_event(self, index: int, event_type: str, data_str: str) -> None:
        """解析并打印单个 SSE 事件。"""
        data = self._load_json(data_str)
        inner_event, inner_data = self._normalize_event(event_type, data)

        self._print_section(f"EVENT #{index}: {inner_event}")
        print(f"raw_event={event_type}")

        if inner_event == "updates":
            self._print_updates(inner_data)
        elif inner_event == "values":
            self._print_values(inner_data)
        elif inner_event == "error":
            print(self._to_json(inner_data, limit=2000))
        elif inner_event == "metadata":
            print(self._to_json(inner_data, limit=2000))
        elif inner_event == "end":
            print("Stream ended.")
        else:
            print(self._to_json(inner_data, limit=2000))

    def _normalize_event(self, event_type: str, data: Any) -> tuple[str, Any]:
        """兼容嵌套事件和 LangGraph 直接事件两种格式。"""
        if isinstance(data, dict) and "event" in data and "data" in data:
            return str(data["event"]), data["data"]
        return event_type, data

    def _print_updates(self, data: Any) -> None:
        """打印 updates 模式的节点增量输出。"""
        if not isinstance(data, dict):
            print(self._to_json(data, limit=2000))
            return

        for node_name, node_output in data.items():
            print(f"\n[NODE] {node_name}")
            if isinstance(node_output, dict):
                self._print_state_fields(node_output)
            else:
                print(self._to_json(node_output, limit=1200))

    def _print_values(self, data: Any) -> None:
        """打印 values 模式的完整状态快照。"""
        if not isinstance(data, dict):
            print(self._to_json(data, limit=2000))
            return

        self._print_state_fields(data)

    def _print_state_fields(self, state: dict[str, Any]) -> None:
        """打印状态字段，长文本自动截断但保留结构。"""
        priority_keys = [
            "requirement",
            "context",
            "case_plan",
            "generated_code",
            "validation_result",
            "execution_plan",
            "execution_result",
            "parsed_result",
            "repair_suggestion",
            "final_report",
            "retry",
            "repair_count",
            "messages",
        ]
        keys = [key for key in priority_keys if key in state]
        keys.extend(key for key in state.keys() if key not in keys)

        for key in keys:
            value = state[key]
            if key == "messages":
                self._print_messages(value)
            else:
                print(f"[{key}] {self._to_json(value, limit=1800)}")

    def _print_messages(self, messages: Any) -> None:
        """打印消息列表，展示最后几条内容。"""
        if not isinstance(messages, list):
            print(f"[messages] {self._to_json(messages, limit=1200)}")
            return

        print(f"[messages] count={len(messages)}")
        start_index = max(len(messages) - 4, 1)
        for index, message in enumerate(messages[-5:], start=start_index):
            role = self._message_role(message)
            content = self._message_content(message)
            print(f"  - #{index} {role}: {self._preview(content, limit=1200)}")

    def _message_role(self, message: Any) -> str:
        """从 dict 或 LangChain 序列化消息中提取角色。"""
        if isinstance(message, dict):
            return str(message.get("role") or message.get("type") or "message")
        return str(getattr(message, "type", "message"))

    def _message_content(self, message: Any) -> str:
        """从 dict 或 LangChain 序列化消息中提取内容。"""
        if isinstance(message, dict):
            if "content" in message:
                return str(message["content"])
            kwargs = message.get("kwargs")
            if isinstance(kwargs, dict) and "content" in kwargs:
                return str(kwargs["content"])
            return self._to_json(message, limit=1200)
        return str(getattr(message, "content", message))

    def _load_json(self, data_str: str) -> Any:
        """解析 JSON，失败时返回原始文本。"""
        if data_str in ("", "null"):
            return None
        try:
            return json.loads(data_str)
        except json.JSONDecodeError:
            return data_str

    def _to_json(self, value: Any, limit: int) -> str:
        """格式化 JSON 并限制输出长度。"""
        if isinstance(value, str):
            return self._preview(value, limit=limit)
        text = json.dumps(value, ensure_ascii=False, indent=2, default=str)
        return self._preview(text, limit=limit)

    def _preview(self, text: str, limit: int) -> str:
        """限制长文本显示长度。"""
        if len(text) <= limit:
            return text
        return f"{text[:limit]}... <truncated {len(text) - limit} chars>"

    def _print_section(self, title: str) -> None:
        """打印分隔标题。"""
        print(f"\n{'=' * 80}")
        print(title)
        print("=" * 80)


def main() -> None:
    """CLI 入口。"""
    prompt = sys.argv[1] if len(sys.argv) > 1 else "生成1个测试rocminfo的 pytest 测试用例"
    thread_id = sys.argv[2] if len(sys.argv) > 2 else f"debug-{time.time():.0f}"
    user_id = sys.argv[3] if len(sys.argv) > 3 else "zx"
    project_id = sys.argv[4] if len(sys.argv) > 4 else "rocm"

    debugger = LangGraphDevDebugger()
    debugger.run(prompt, thread_id, user_id, project_id)


if __name__ == "__main__":
    main()