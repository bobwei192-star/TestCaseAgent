"""Mock 测试用例生成器 —— 无需 LLM API，使用预设响应跑完整流水线。

用法:
    python -m src.agent.mock_gen "写一个pytest测试用例，测试rocm-smi指令"
    python -m src.agent.mock_gen  # 使用默认需求
    make mock_gen                 # Makefile 快捷方式
"""

from __future__ import annotations

import re
import sys
from typing import Any


def _print_banner():
    print("=" * 60)
    print("  Mock Test Case Generator (offline mode)")
    print("  使用预设 LLM 响应，无需 API 调用")
    print("=" * 60)
    print()


def _run_pipeline(requirement: str) -> dict[str, Any]:
    """用 mock LLM 输出顺序跑完完整 4 节点流水线。

    与 build_graph() / make gen 使用完全相同的节点函数（graph.py 注册的同名函数），
    唯一区别：LLM 调用通过 patch get_llm 注入 mock 响应，无需 API 和 function calling。

    流程: requirement_parser → planner → generator → sandbox_executor
    """
    from unittest.mock import patch

    from .state import AgentState  # type: ignore[attr-defined]
    from .mock_llm import get_mock_for_node

    state: AgentState = {
        "requirement": requirement,
        "messages": [],
        "context": {},
    }

    # ---- Step 1: requirement_parser ----
    print("[1/4] requirement_parser  → 解析需求（mock LLM）...")
    with patch(
        "src.agent.nodes.node_requirement_parser.get_llm",
        return_value=get_mock_for_node("requirement_parser"),
    ):
        from .nodes.node_requirement_parser import requirement_parser  # type: ignore[attr-defined]
        result = requirement_parser(state)
        state.update(result)

    intent = state.get("parsed_intent", "UNKNOWN")
    print(f"      意图: {intent}  |  模板: {state.get('template_name', 'N/A')}")
    print()

    # ---- Step 2: planner ----
    print("[2/4] planner              → 生成测试计划 + 执行计划（mock LLM）...")
    with patch(
        "src.agent.nodes.node_planner.get_llm",
        return_value=get_mock_for_node("planner"),
    ):
        from .nodes.node_planner import planner  # type: ignore[attr-defined]
        result = planner(state)
        state.update(result)

    case_plan = state.get("case_plan", "")
    execution_plan = state.get("execution_plan", {})
    print(f"      计划长度: {len(case_plan)} 字符")
    print(f"      执行计划状态: {execution_plan.get('status', 'N/A')}")
    if execution_plan.get("status") == "parsed":
        env = execution_plan.get("environment", {})
        print(f"      风险等级: {execution_plan.get('risk_level', 'N/A')}")
        print(f"      环境类型: {env.get('type', 'N/A')}")
    print()

    # ---- Step 3: generator ----
    print("[3/4] generator            → 生成测试代码（mock LLM）...")
    with patch(
        "src.agent.nodes.node_generator.get_llm",
        return_value=get_mock_for_node("generator"),
    ):
        from .nodes.node_generator import generator  # type: ignore[attr-defined]
        result = generator(state)
        state.update(result)

    code = state.get("generated_code") or state.get("code", "")
    validation = state.get("validation_result", {})
    saved = state.get("saved_filepath", "")
    print(f"      代码长度: {len(code)} 字符")
    print(f"      验证状态: {validation.get('status', 'N/A')}")
    if validation.get("errors"):
        for err in validation["errors"]:
            print(f"        ⚠ {err}")
    if saved:
        print(f"      保存路径: {saved}")
    print()

    # ---- Step 4: sandbox_executor ----
    # 与 graph.py 注册的是同一个函数，无需 mock LLM（沙盒执行不调用 LLM）
    print("[4/4] sandbox_executor     → 执行测试代码...")
    from .nodes.node_sandbox_executor import sandbox_executor  # type: ignore[attr-defined]
    result = sandbox_executor(state)
    state.update(result)

    exec_result = state.get("execution_result", {})
    status = exec_result.get("status", "N/A")
    if status == "success":
        print(f"      执行状态: ✅ 成功")
    elif status == "skipped":
        print(f"      执行状态: ⏭ 跳过 — {exec_result.get('message', 'N/A')}")
    else:
        print(f"      执行状态: ❌ 失败")
        print(f"      失败阶段: {exec_result.get('stage', 'unknown')}")
        err = exec_result.get("error", "")
        if err:
            print(f"      错误信息: {str(err)[:150]}")
    print()

    return state


def _parse_pytest_output(stdout: str) -> dict[str, int]:
    """从 pytest stdout 中提取测试结果统计。

    Returns:
        {"passed": N, "failed": N, "skipped": N, "error": N, "total": N}
    """
    stats: dict[str, int] = {"passed": 0, "failed": 0, "skipped": 0, "error": 0, "total": 0}

    # 匹配 pytest 汇总行，如: "2 passed in 0.02s" / "1 failed, 2 passed in 5s"
    summary_match = re.search(
        r"(\d+)\s+failed[,\s]*.*?(\d+)\s+passed|"
        r"(\d+)\s+passed[,\s]*.*?(\d+)\s+failed|"
        r"(\d+)\s+passed|"
        r"(\d+)\s+failed|"
        r"(\d+)\s+skipped",
        stdout,
    )

    # 逐行匹配单个测试结果
    for line in stdout.split("\n"):
        m = re.match(r".*?\b(PASSED|FAILED|SKIPPED|ERROR)\b", line)
        if m:
            key = m.group(1).lower()
            stats[key] = stats.get(key, 0) + 1
            stats["total"] += 1

    # 如果逐行没解析到，尝试从汇总行提取
    if stats["total"] == 0:
        m = re.search(r"^=+\s+(.+?)\s+=+$", stdout, re.MULTILINE)
        if m:
            summary_str = m.group(1)
            passed_m = re.search(r"(\d+)\s+passed", summary_str)
            failed_m = re.search(r"(\d+)\s+failed", summary_str)
            skipped_m = re.search(r"(\d+)\s+skipped", summary_str)
            error_m = re.search(r"(\d+)\s+error", summary_str)
            if passed_m:
                stats["passed"] = int(passed_m.group(1))
            if failed_m:
                stats["failed"] = int(failed_m.group(1))
            if skipped_m:
                stats["skipped"] = int(skipped_m.group(1))
            if error_m:
                stats["error"] = int(error_m.group(1))
            stats["total"] = stats["passed"] + stats["failed"] + stats["skipped"] + stats["error"]

    return stats


def _print_final_conclusion(state: dict[str, Any]):
    """打印最终结论——智能体的执行总结。"""
    exec_result = state.get("execution_result", {})
    exec_stdout = exec_result.get("stdout", "")
    exec_status = exec_result.get("status", "N/A")
    parsed_intent = state.get("parsed_intent", "GENERATE")
    saved = state.get("saved_filepath", "")
    code = state.get("generated_code") or state.get("code", "")

    print()
    print("=" * 60)
    print("  最终结论")
    print("=" * 60)

    # 1. 整体状态
    if exec_status == "success":
        print(f"  🎯 任务状态:  成功")
    elif exec_status == "skipped":
        print(f"  🎯 任务状态:  已跳过（{exec_result.get('message', 'N/A')}）")
    else:
        print(f"  🎯 任务状态:  失败")
        err = exec_result.get("error", "")
        if err:
            print(f"     错误原因:  {str(err)[:200]}")

    # 2. 测试执行结果解析
    if exec_stdout:
        stats = _parse_pytest_output(exec_stdout)
        if stats["total"] > 0:
            print(f"  📊 测试用例:  {stats['total']} 个")
            parts = []
            if stats["passed"]:
                parts.append(f"{stats['passed']} 通过")
            if stats["failed"]:
                parts.append(f"{stats['failed']} 失败")
            if stats["skipped"]:
                parts.append(f"{stats['skipped']} 跳过")
            if stats["error"]:
                parts.append(f"{stats['error']} 错误")
            print(f"     结果:      {', '.join(parts)}")

            # 逐条测试结果
            print()
            for line in exec_stdout.strip().split("\n"):
                stripped = line.strip()
                if "PASSED" in stripped:
                    name = re.sub(r"\s*PASSED.*", "", stripped)
                    print(f"     ✅ PASS | {name}")
                elif "FAILED" in stripped:
                    name = re.sub(r"\s*FAILED.*", "", stripped)
                    print(f"     ❌ FAIL | {name}")
                elif "SKIPPED" in stripped:
                    name = re.sub(r"\s*SKIPPED.*", "", stripped)
                    print(f"     ⏭ SKIP | {name}")

    # 3. 交付物
    print()
    print(f"  📋 意图类型:  {parsed_intent}")
    print(f"  📦 生成代码:  {len(code)} 字符")
    print(f"  💾 代码保存:  {saved or '未保存'}")
    print(f"  🐳 执行方式:  Docker 沙盒（容器已自动清理）")

    # 4. 一句话结论
    print()
    if exec_status == "success":
        if stats.get("total", 0) > 0 and stats.get("failed", 0) == 0 and stats.get("error", 0) == 0:
            print(f"  💡 结论: 智能体成功生成了测试代码并在 Docker 沙盒中验证通过")
            print(f"          所有 {stats['total']} 个测试用例执行结果符合预期。")
        else:
            print(f"  💡 结论: 智能体已完成代码生成和沙盒执行。")
    elif exec_status == "skipped":
        print(f"  💡 结论: 智能体已生成代码，沙盒执行被跳过（意图为查询类）。")
    else:
        print(f"  💡 结论: 智能体已生成代码，但沙盒执行时发生错误，"
              f"请检查上述错误信息。")

    print()


def _print_summary(state: dict[str, Any]):
    print("=" * 60)
    print("  生成摘要")
    print("=" * 60)

    code = state.get("generated_code") or state.get("code", "")
    saved = state.get("saved_filepath", "")
    validation = state.get("validation_result", {})
    execution_plan = state.get("execution_plan", {})
    exec_result = state.get("execution_result", {})

    print(f"  需求:        {state.get('requirement', '')[:60]}...")
    print(f"  意图:        {state.get('parsed_intent', 'N/A')}")
    print(f"  代码量:      {len(code)} 字符")
    print(f"  代码验证:    {validation.get('status', 'N/A')}")
    print(f"  执行计划:    {execution_plan.get('status', 'N/A')}")

    exec_status = exec_result.get("status", "N/A")
    exec_stdout = exec_result.get("stdout", "")
    exec_stderr = exec_result.get("stderr", "")
    exec_exit_code = exec_result.get("exit_code", "N/A")

    print(f"  沙盒执行:    {exec_status} (exit_code={exec_exit_code})")

    errors = validation.get("errors", [])
    if errors:
        print(f"  验证问题:    {len(errors)} 项")
        for e in errors:
            print(f"    ⚠ {e}")
    else:
        print("  验证问题:    无")

    # ---- 沙盒执行输出 ----
    if exec_stdout:
        print()
        print("--- pytest 执行输出 ---")
        for line in exec_stdout.strip().split("\n"):
            print(f"  {line}")
    if exec_stderr and exec_stderr.strip():
        print()
        print("--- 执行 stderr ---")
        for line in exec_stderr.strip().split("\n")[:20]:
            print(f"  {line}")
        if len(exec_stderr.strip().split("\n")) > 20:
            print("  ... (截断)")
    print()

    # ---- 生成的代码 ----
    if code:
        print("--- 生成的代码（前 40 行）---")
        lines = code.split("\n")[:40]
        for line in lines:
            print(f"  {line}")
        if len(code.split("\n")) > 40:
            print("  ... (截断)")
        print(f"  📝 完整代码已保存到: {saved}")
    print()


def main(requirement: str | None = None):
    """Mock 生成器主入口。

    Args:
        requirement: 测试需求文本，为 None 时使用默认值
    """
    if requirement is None:
        requirement = "写一个pytest测试用例，测试rocm-smi指令的存在性和正确性"

    _print_banner()

    try:
        state = _run_pipeline(requirement)
        _print_summary(state)
        _print_final_conclusion(state)
        sys.exit(0)
    except Exception as exc:
        print(f"\n❌ 生成失败: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # 支持命令行参数: python -m src.agent.mock_gen "你的需求"
    req = sys.argv[1] if len(sys.argv) > 1 else None
    main(req)
