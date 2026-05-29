"""Mock LLM 输出模板 —— 预设各节点的 LLM 响应，用于离线生成测试用例。

使用方式：
    from src.agent.mock_llm import create_mock_llm, MOCK_GENERATED_CODE
    mock = create_mock_llm(MOCK_GENERATED_CODE)

每个 mock 输出都经过验证，确保下游节点能够正确解析。
"""

from __future__ import annotations

from unittest.mock import MagicMock

from langchain_core.messages import AIMessage


# ============================================================================
# Mock 响应模板
# ============================================================================

MOCK_PARSED_REQUIREMENT = """## 需求分析

### 测试目标
验证 ROCm 系统管理接口 (rocm-smi) 命令的可用性和输出正确性。

### 意图识别
- 意图类型: GENERATE
- 意图聚类: create_intent
- 模板名称: create_intent

### 测试范围
1. **命令存在性验证**: 确认 rocm-smi 命令已安装且在 PATH 中
2. **基本执行验证**: 确认 rocm-smi --showproductname 可正常执行
3. **输出内容验证**: 确认默认输出包含 GPU 硬件相关信息

### 等价类分析
- 有效等价类: ROCm 驱动正常安装的环境中执行 rocm-smi
- 无效等价类: 命令未安装、路径错误、权限不足

### 边界条件
- 无 GPU 环境：应优雅跳过而非报错
- 多 GPU 环境：应能列出所有 GPU 信息

### 测试策略
- 冒烟测试: 命令存在性 + 基本执行
- 功能测试: 输出包含 GPU/ROCm 关键字段
"""

MOCK_CASE_PLAN = """1. 测试目标: 验证 rocm-smi 指令的存在性和正确性（命令可用性 + 输出有效性）

2. Suite 划分与类名映射:
   - Suite: 冒烟 | 类名: TestRocmSmiSmoke | 包含测试点: 命令存在性、基本执行
   - Suite: 功能 | 类名: TestRocmSmiFunctional | 包含测试点: 输出验证、GPU信息验证

3. 前置条件:
   - 环境: ROCm 6.0+, AMD GPU 驱动, rocm-smi 在 PATH 中
   - 数据: 无特殊数据文件要求
   - 权限: 普通用户权限即可（rocm 组）

4. 执行顺序与依赖:
   - 步骤1: 检查 rocm-smi 命令是否存在 (shutil.which)
   - 步骤2: 执行 rocm-smi --showproductname 验证产品信息
   - 步骤3: 执行 rocm-smi 默认命令验证输出内容

5. 预期结果映射:
   - 有效类: 返回码 0, stdout 包含 "GPU" 或 "ROCm" 关键字段
   - 无效类: pytest.skip 当命令不存在时（优雅跳过）

6. 风险与应对:
   - 风险: 无 GPU/无 ROCm 环境 → pytest.skip 跳过
   - 风险: 命令超时 → subprocess.run 设置 timeout=30

7. Fixture 复用与作用域方案:
   - 共享Fixture: rocm_smi_available (scope=module) 统一检查命令可用性
   - Skip逻辑集中点: 在 fixture 内判断 shutil.which("rocm-smi") is None

Suite/Case 映射:
- suite: smoke
- case_name: test_rocm_smi_exists
- file_name: test_rocm_smi_exists.py
- test_goal: 验证 rocm-smi 命令存在且可正常执行
- steps: Arrange(检查rocm-smi可用)/Act(执行--showproductname)/Assert(返回码0、输出非空)

- suite: functional
- case_name: test_rocm_smi_output
- file_name: test_rocm_smi_output.py
- test_goal: 验证 rocm-smi 默认输出包含 GPU 硬件信息
- steps: Arrange(检查rocm-smi可用)/Act(执行rocm-smi)/Assert(输出含GPU/ROCm关键词)

```yaml
execution_plan:
  environment:
    type: "local"
    image: ""
    timeout: 60
  preconditions:
    - name: "检查 rocm-smi 安装"
      command: "which rocm-smi"
      expected: "exit_code == 0"
  steps:
    - name: "执行冒烟测试"
      action: "run"
      commands:
        - "pytest test_rocm_smi_exists.py -v"
    - name: "执行功能测试"
      action: "run"
      commands:
        - "pytest test_rocm_smi_output.py -v"
  risk_level: "safe"
```
"""

MOCK_GENERATED_CODE = """以下是针对 rocm-smi 指令存在性和正确性的 pytest 测试用例。

```python
import subprocess
import shutil

import pytest


@pytest.fixture(scope="module")
def rocm_smi_available():
    \"\"\"检查 rocm-smi 命令是否可用，不可用则跳过模块内所有测试。\"\"\"
    if shutil.which("rocm-smi") is None:
        pytest.skip("rocm-smi 命令在当前环境中不可用，跳过测试")


class TestRocmSmiSmoke:
    \"\"\"冒烟测试：验证 rocm-smi 命令的基本可用性。\"\"\"

    def test_rocm_smi_command_exists(self, rocm_smi_available):
        \"\"\"验证 rocm-smi --showproductname 可正常执行并返回产品信息。\"\"\"
        result = subprocess.run(
            ["rocm-smi", "--showproductname"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"rocm-smi --showproductname 执行失败, "
            f"exit_code={result.returncode}, stderr={result.stderr[:200]}"
        )
        assert result.stdout.strip(), "rocm-smi --showproductname 输出为空"


class TestRocmSmiFunctional:
    \"\"\"功能测试：验证 rocm-smi 默认输出的正确性。\"\"\"

    def test_rocm_smi_default_output(self, rocm_smi_available):
        \"\"\"验证 rocm-smi 默认执行输出包含 GPU 相关信息。\"\"\"
        result = subprocess.run(
            ["rocm-smi"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"rocm-smi 执行失败, exit_code={result.returncode}"
        )
        stdout_upper = result.stdout.upper()
        keywords = ["GPU", "ROCm"]
        found = [kw for kw in keywords if kw.upper() in stdout_upper]
        assert found, (
            f"rocm-smi 输出中未找到预期关键词 ({keywords}), "
            f"实际输出前 500 字符: {result.stdout[:500]}"
        )
```
"""

# ============================================================================
# 工具函数
# ============================================================================


def create_mock_llm(text_response: str) -> MagicMock:
    """创建模拟 LLM 的 MagicMock 对象。

    invoke() 调用返回包含指定文本的 AIMessage，兼容如下调用形式：
    - llm.invoke({"messages": [...]})     # planner / requirement_parser 使用
    - llm.invoke([HumanMessage(...)])      # generator 使用
    - llm.invoke(any_input)                # 通用

    Args:
        text_response: LLM 应返回的文本内容

    Returns:
        配置好的 MagicMock 实例，.invoke() 返回 AIMessage(content=text_response)
    """
    mock = MagicMock()
    mock.invoke.return_value = AIMessage(content=text_response)
    return mock


def get_mock_for_node(node: str) -> MagicMock:
    """根据节点名称获取对应的 mock LLM 实例。

    Args:
        node: 节点名称，支持 "requirement_parser" / "planner" / "generator"

    Returns:
        对应节点的 mock LLM MagicMock 实例

    Raises:
        ValueError: 未知的节点名称
    """
    mock_map = {
        "requirement_parser": MOCK_PARSED_REQUIREMENT,
        "planner": MOCK_CASE_PLAN,
        "generator": MOCK_GENERATED_CODE,
    }
    if node not in mock_map:
        raise ValueError(f"未知节点: {node}，支持: {list(mock_map.keys())}")
    return create_mock_llm(mock_map[node])
