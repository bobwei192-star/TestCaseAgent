"""节点级单元测试（#25）。

覆盖所有 5 个核心节点：
- requirement_parser
- planner
- generator
- sandbox_executor
- context_retriever

使用 mock LLM 避免真实 API 调用，测试节点的纯逻辑和边缘情况。
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from langchain_core.messages import HumanMessage, AIMessage

from src.agent.state import AgentState


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def base_state() -> AgentState:
    """基础状态 fixture，包含所有必需字段。"""
    return {
        "messages": [HumanMessage(content="测试rocm-smi命令的存在性")],
        "requirement": "测试rocm-smi命令的存在性",
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
def mock_llm_response():
    """模拟 LLM 返回的 AIMessage。"""
    mock_msg = Mock()
    mock_msg.content = "这是模拟的 LLM 响应内容"
    return mock_msg


# ============================================================
# RequirementParser 测试
# ============================================================

class TestRequirementParserNode:
    """需求解析节点单元测试。"""

    def test_parser_returns_required_fields(self, base_state):
        """解析器必须返回 parsed_requirement 和 intent。"""
        from src.agent.nodes.node_requirement_parser import requirement_parser
        from unittest.mock import patch

        mock_llm = Mock()
        mock_msg = Mock()
        mock_msg.content = "结构化需求规格"
        mock_llm.invoke.return_value = {"messages": [mock_msg]}

        with patch(
            "src.agent.nodes.node_requirement_parser.get_llm",
            return_value=mock_llm,
        ):
            result = requirement_parser(base_state)

        assert "parsed_requirement" in result
        assert "parsed_intent" in result
        assert "intent" in result
        assert result["parsed_intent"] == "GENERATE"

    def test_parser_handles_empty_requirement(self, base_state):
        """解析器能处理空需求（fallback 到 messages 中的用户消息）。"""
        from src.agent.nodes.node_requirement_parser import requirement_parser
        from unittest.mock import patch

        state = {**base_state}
        state["requirement"] = ""

        mock_llm = Mock()
        mock_msg = Mock()
        mock_msg.content = "fallback spec"
        mock_llm.invoke.return_value = {"messages": [mock_msg]}

        with patch(
            "src.agent.nodes.node_requirement_parser.get_llm",
            return_value=mock_llm,
        ):
            result = requirement_parser(state)

        assert "parsed_requirement" in result
        # 当 requirement 为空时，从 _last_user_message 回退得到 base_state 中的消息文本
        assert len(result["requirement"]) > 0

    def test_parser_intent_detection(self, base_state):
        """解析器正确识别意图。"""
        from src.agent.nodes.node_requirement_parser import requirement_parser
        from unittest.mock import patch

        mock_llm = Mock()
        mock_msg = Mock()
        mock_msg.content = "spec content"
        mock_llm.invoke.return_value = {"messages": [mock_msg]}

        with patch(
            "src.agent.nodes.node_requirement_parser.get_llm",
            return_value=mock_llm,
        ):
            result = requirement_parser(base_state)

        assert "parsed_intent" in result
        assert "intent_cluster" in result
        assert "template_name" in result

    def test_parser_adds_aimessage(self, base_state):
        """解析器在 messages 中追加 AIMessage。"""
        from src.agent.nodes.node_requirement_parser import requirement_parser
        from unittest.mock import patch

        mock_llm = Mock()
        mock_msg = Mock()
        mock_msg.content = "parsed"
        mock_llm.invoke.return_value = {"messages": [mock_msg]}

        with patch(
            "src.agent.nodes.node_requirement_parser.get_llm",
            return_value=mock_llm,
        ):
            result = requirement_parser(base_state)

        assert "messages" in result
        assert len(result["messages"]) >= 1

    def test_parser_with_memory_manager(self, base_state):
        """解析器在有 memory manager 时正常运行。"""
        from src.agent.nodes.node_requirement_parser import requirement_parser
        from unittest.mock import patch

        mock_llm = Mock()
        mock_msg = Mock()
        mock_msg.content = "spec with memory"
        mock_llm.invoke.return_value = {"messages": [mock_msg]}

        mock_runtime = Mock()
        mock_runtime.context.user_id = "test_user"

        with patch(
            "src.agent.nodes.node_requirement_parser.get_llm",
            return_value=mock_llm,
        ):
            result = requirement_parser(base_state, runtime=mock_runtime)

        assert "parsed_requirement" in result


# ============================================================
# Planner 测试
# ============================================================

class TestPlannerNode:
    """规划节点单元测试。"""

    def test_planner_returns_case_plan(self, base_state):
        """规划器返回 case_plan 和 execution_plan。"""
        from src.agent.nodes.node_planner import planner
        from unittest.mock import patch

        # 创建返回具体文本的 mock（模拟 AIMessage）
        mock_response = Mock()
        mock_response.content = (
            "1. 测试目标: 验证 rocm-smi\n"
            "2. Suite 划分:\n"
            "   - Suite: 冒烟 | 类名: TestSmoke\n"
            "```yaml\n"
            "execution_plan:\n"
            "  environment:\n"
            "    type: local\n"
            "    timeout: 120\n"
            "  preconditions: []\n"
            "  steps:\n"
            "    - name: 执行测试\n"
            "      action: run\n"
            "      commands:\n"
            "        - pytest test_*.py -v\n"
            "  risk_level: safe\n"
            "```"
        )

        mock_llm = Mock()
        mock_llm.invoke.return_value = mock_response

        with patch(
            "src.agent.nodes.node_planner.get_llm",
            return_value=mock_llm,
        ):
            result = planner(base_state)

        assert "case_plan" in result
        assert "execution_plan" in result
        assert len(result["case_plan"]) > 0

    def test_planner_parses_execution_plan(self, base_state):
        """规划器正确解析 YAML 格式的 execution_plan。"""
        from src.agent.nodes.node_planner import planner
        from unittest.mock import patch

        mock_response = Mock()
        mock_response.content = (
            "Test plan content\n"
            "```yaml\n"
            "execution_plan:\n"
            "  environment:\n"
            "    type: local\n"
            "    timeout: 60\n"
            "  preconditions: []\n"
            "  steps: []\n"
            "  risk_level: safe\n"
            "```"
        )

        mock_llm = Mock()
        mock_llm.invoke.return_value = mock_response

        with patch(
            "src.agent.nodes.node_planner.get_llm",
            return_value=mock_llm,
        ):
            result = planner(base_state)

        ep = result["execution_plan"]
        assert isinstance(ep, dict)
        assert ep.get("status") == "parsed"
        assert ep.get("environment", {}).get("type") == "local"
        assert ep.get("risk_level") == "safe"

    def test_planner_execution_plan_no_yaml(self, base_state):
        """规划器在无 YAML 块时给出降级 execution_plan。"""
        from src.agent.nodes.node_planner import planner
        from unittest.mock import patch

        mock_response = Mock()
        mock_response.content = "Just a plain text plan, no YAML block."

        mock_llm = Mock()
        mock_llm.invoke.return_value = mock_response

        with patch(
            "src.agent.nodes.node_planner.get_llm",
            return_value=mock_llm,
        ):
            result = planner(base_state)

        ep = result["execution_plan"]
        assert isinstance(ep, dict)
        assert ep.get("status") == "defaulted"

    def test_planner_handles_feedback(self, base_state):
        """规划器在收到反馈时进入重规划模式。"""
        from src.agent.nodes.node_planner import planner
        from unittest.mock import patch

        state = {**base_state, "feedback": "测试失败: subprocess 未找到"}

        mock_response = Mock()
        mock_response.content = (
            "Re-plan due to failure.\n"
            "```yaml\n"
            "execution_plan:\n"
            "  environment:\n"
            "    type: local\n"
            "    timeout: 60\n"
            "  preconditions: []\n"
            "  steps: []\n"
            "  risk_level: safe\n"
            "```"
        )

        mock_llm = Mock()
        mock_llm.invoke.return_value = mock_response

        with patch(
            "src.agent.nodes.node_planner.get_llm",
            return_value=mock_llm,
        ):
            result = planner(state)

        assert "case_plan" in result

    def test_planner_messages_output(self, base_state):
        """规划器正确输出 AIMessage。"""
        from src.agent.nodes.node_planner import planner
        from unittest.mock import patch

        mock_response = Mock()
        mock_response.content = "plan"

        mock_llm = Mock()
        mock_llm.invoke.return_value = mock_response

        with patch(
            "src.agent.nodes.node_planner.get_llm",
            return_value=mock_llm,
        ):
            result = planner(base_state)

        msgs = result.get("messages", [])
        assert len(msgs) >= 1


# ============================================================
# Generator 测试
# ============================================================

class TestGeneratorNode:
    """代码生成节点单元测试。"""

    def test_generator_with_valid_code(self, base_state):
        """生成器生成有效的 pytest 代码。"""
        from src.agent.nodes.node_generator import generator
        from unittest.mock import patch

        state = {**base_state, "case_plan": "测试 rocm-smi 命令存在性"}

        mock_model = Mock()
        mock_msg = Mock()
        mock_msg.content = (
            "```python\n"
            "import subprocess\n"
            "import pytest\n\n"
            "def test_rocm_smi_exists():\n"
            '    result = subprocess.run(["which", "rocm-smi"], capture_output=True, text=True)\n'
            "    assert result.returncode == 0\n"
            "```"
        )
        mock_model.invoke.return_value = mock_msg

        with patch(
            "src.agent.nodes.node_generator.get_llm",
            return_value=mock_model,
        ):
            result = generator(state, model=mock_model)

        assert "generated_code" in result
        assert "code" in result
        assert "validation_result" in result

    def test_generator_rejects_dangerous_code(self, base_state):
        """安全审查拦截危险代码（#40）。"""
        from src.agent.nodes.node_generator import generator
        from unittest.mock import patch

        state = {**base_state, "case_plan": "test"}

        mock_model = Mock()
        mock_msg = Mock()
        mock_msg.content = (
            "```python\n"
            "import os\n"
            "def test_danger():\n"
            "    eval('1+1')\n"
            "```"
        )
        mock_model.invoke.return_value = mock_msg

        with patch(
            "src.agent.nodes.node_generator.get_llm",
            return_value=mock_model,
        ):
            result = generator(state, model=mock_model)

        vr = result.get("validation_result", {})
        assert vr.get("status") == "failed"
        assert vr.get("quality_gate") == "security_review"

    def test_generator_handles_empty_plan(self, base_state):
        """生成器处理空计划。"""
        from src.agent.nodes.node_generator import generator
        from unittest.mock import patch

        state = {**base_state, "case_plan": ""}

        mock_model = Mock()
        mock_msg = Mock()
        mock_msg.content = (
            "```python\n"
            "import subprocess\n"
            "def test_fallback():\n"
            '    result = subprocess.run(["echo", "hello"], capture_output=True, text=True)\n'
            "    assert result.returncode == 0\n"
            "```"
        )
        mock_model.invoke.return_value = mock_msg

        with patch(
            "src.agent.nodes.node_generator.get_llm",
            return_value=mock_model,
        ):
            result = generator(state, model=mock_model)

        assert "generated_code" in result

    def test_generator_saves_file(self, base_state, tmp_path):
        """生成器保存代码到文件。"""
        from src.agent.nodes.node_generator import generator, OUTPUT_DIR
        from unittest.mock import patch

        import src.agent.nodes.node_generator as gen_module
        original_output = gen_module.OUTPUT_DIR
        gen_module.OUTPUT_DIR = str(tmp_path)

        try:
            state = {**base_state, "case_plan": "test"}

            mock_model = Mock()
            mock_msg = Mock()
            mock_msg.content = (
                "```python\n"
                "import subprocess\n"
                "def test_save():\n"
                '    result = subprocess.run(["echo", "ok"], capture_output=True, text=True)\n'
                "    assert result.returncode == 0\n"
                "```"
            )
            mock_model.invoke.return_value = mock_msg

            with patch(
                "src.agent.nodes.node_generator.get_llm",
                return_value=mock_model,
            ):
                result = generator(state, model=mock_model)

            saved = result.get("saved_filepath")
            if saved:
                import os
                assert os.path.exists(saved)
        finally:
            gen_module.OUTPUT_DIR = original_output

    def test_generator_validation_failed_keeps_old_code(self, base_state):
        """验证失败时保留上一轮有效代码。"""
        from src.agent.nodes.node_generator import generator
        from unittest.mock import patch

        old_code = (
            "import subprocess\n"
            "def test_old():\n"
            '    result = subprocess.run(["echo", "ok"], capture_output=True, text=True)\n'
            "    assert result.returncode == 0\n"
        )
        state = {
            **base_state,
            "case_plan": "test",
            "generated_code": old_code,
            "code": old_code,
        }

        mock_model = Mock()
        mock_msg = Mock()
        # 返回无效代码
        mock_msg.content = "No code, just text."
        mock_model.invoke.return_value = mock_msg

        with patch(
            "src.agent.nodes.node_generator.get_llm",
            return_value=mock_model,
        ):
            result = generator(state, model=mock_model)

        # 应该保留旧代码
        assert result["generated_code"] == old_code


# ============================================================
# SandboxExecutor 测试
# ============================================================

class TestSandboxExecutorNode:
    """沙盒执行节点单元测试。"""

    def test_executor_missing_code(self, base_state):
        """缺少代码时返回失败。"""
        from src.agent.nodes.node_sandbox_executor import sandbox_executor

        state = {**base_state, "generated_code": "", "code": ""}

        result = sandbox_executor(state)

        assert result["execution_result"]["status"] == "failed"
        assert result["execution_result"]["stage"] == "missing_code"

    def test_executor_query_intent_skips(self, base_state):
        """查询类意图跳过执行。"""
        from src.agent.nodes.node_sandbox_executor import sandbox_executor

        state = {
            **base_state,
            "generated_code": "import subprocess\ndef test_x(): pass",
            "parsed_intent": "DIAGNOSE",
        }

        result = sandbox_executor(state)

        assert result["execution_result"]["status"] == "skipped"
        assert "query_intent" in result["execution_result"]["stage"]

    def test_executor_probe_intent_skips(self, base_state):
        """PROBE 意图也跳过执行。"""
        from src.agent.nodes.node_sandbox_executor import sandbox_executor

        state = {
            **base_state,
            "generated_code": "code",
            "parsed_intent": "PROBE",
        }

        result = sandbox_executor(state)
        assert result["execution_result"]["status"] == "skipped"


# ============================================================
# Code Security 测试
# ============================================================

class TestCodeSecurity:
    """代码安全审查测试（#39 #40）。"""

    def test_review_clean_code(self):
        """安全审查通过正常代码。"""
        from src.agent.code_security import review_code

        code = (
            "import subprocess\n"
            "import pytest\n\n"
            "def test_hello():\n"
            "    result = subprocess.run(['echo', 'hello'], capture_output=True, text=True)\n"
            "    assert result.returncode == 0\n"
        )

        result = review_code(code)
        assert result.passed is True
        assert result.severity == "safe"

    def test_review_dangerous_eval(self):
        """安全审查拦截 eval()。"""
        from src.agent.code_security import review_code

        code = "def test_x():\n    eval('1+1')\n"

        result = review_code(code)
        assert result.passed is False
        assert result.severity == "critical"

    def test_review_dangerous_exec(self):
        """安全审查拦截 exec()。"""
        from src.agent.code_security import review_code

        code = "def test_x():\n    exec('print(1)')\n"

        result = review_code(code)
        assert result.passed is False

    def test_review_dangerous_os_system(self):
        """安全审查拦截 os.system()。"""
        from src.agent.code_security import review_code

        code = "import os\ndef test_x():\n    os.system('ls')\n"

        result = review_code(code)
        assert result.passed is False

    def test_review_empty_code(self):
        """安全审查对空代码降级为 warning（非 critical）。"""
        from src.agent.code_security import review_code

        result = review_code("")
        assert result.severity == "warning"
        assert "代码为空" in result.issues[0]

    def test_sandbox_hardening_defaults(self):
        """沙盒加固具有默认安全配置。"""
        from src.agent.code_security import build_sandbox_hardening

        hardening = build_sandbox_hardening()
        assert hardening.block_network is True
        assert hardening.cpu_limit == 4
        assert hardening.memory_limit_mb == 4096
        assert hardening.timeout_seconds == 300


# ============================================================
# State Validator 测试
# ============================================================

class TestStateValidator:
    """状态校验测试（#13）。"""

    def test_validate_parser_output(self):
        from src.agent.state_validator import validate_parser_output

        output = {
            "parsed_requirement": "test spec",
            "parsed_intent": "GENERATE",
            "intent_cluster": "create",
        }

        validated = validate_parser_output(output)
        assert validated.parsed_requirement == "test spec"
        assert validated.parsed_intent == "GENERATE"

    def test_validate_planner_output(self):
        from src.agent.state_validator import validate_planner_output

        output = {
            "case_plan": "1. Test goal: verify rocm-smi",
            "execution_plan": {"status": "parsed", "risk_level": "safe"},
        }

        validated = validate_planner_output(output)
        assert "verify rocm-smi" in validated.case_plan

    def test_validate_generator_output(self):
        from src.agent.state_validator import validate_generator_output

        output = {
            "generated_code": "import subprocess\ndef test_x(): pass",
            "validation_result": {"status": "passed"},
        }

        validated = validate_generator_output(output)
        assert len(validated.generated_code) > 0

    def test_validate_execution_output(self):
        from src.agent.state_validator import validate_execution_output

        output = {
            "execution_result": {"status": "success"},
            "feedback": "",
            "sandbox_retry_count": 0,
        }

        validated = validate_execution_output(output)
        assert validated.execution_result["status"] == "success"


# ============================================================
# Model Rotation 测试
# ============================================================

class TestModelRotation:
    """模型轮换测试（#32）。"""

    def test_empty_rotation(self):
        from src.agent.model_rotation import ModelRotation

        rotation = ModelRotation()
        assert len(rotation) == 0
        assert not rotation

    def test_rotation_entries(self):
        from src.agent.model_rotation import ModelRotation, ModelEntry

        entries = [
            ModelEntry(provider="deepseek", model="deepseek-chat"),
            ModelEntry(provider="openai", model="gpt-4o-mini"),
        ]
        rotation = ModelRotation(entries=entries)
        assert len(rotation) == 2

        chain = list(rotation.fallback_chain())
        assert len(chain) == 2
        assert chain[0]["provider"] == "deepseek"
        assert chain[1]["provider"] == "openai"


# ============================================================
# Metrics 测试
# ============================================================

class TestMetrics:
    """Metrics 指标测试（#35）。"""

    def test_singleton(self):
        from src.agent.metrics import get_metrics_collector, reset_metrics

        reset_metrics()
        c1 = get_metrics_collector()
        c2 = get_metrics_collector()
        assert c1 is c2

    def test_record_llm_call(self):
        from src.agent.metrics import get_metrics_collector, reset_metrics

        reset_metrics()
        mc = get_metrics_collector()
        mc.record_llm_call(node="planner", duration=1.5, tokens=500, success=True)
        mc.record_llm_call(node="planner", duration=2.0, tokens=300, success=False)

        snapshot = mc.snapshot()
        assert snapshot["llm_calls"] == 2
        assert snapshot["llm_failures"] == 1
        assert snapshot["total_tokens_used"] == 800

    def test_record_sandbox(self):
        from src.agent.metrics import get_metrics_collector, reset_metrics

        reset_metrics()
        mc = get_metrics_collector()
        mc.record_sandbox_execution(success=True)
        mc.record_sandbox_execution(success=False)
        mc.record_sandbox_execution(success=True)

        snapshot = mc.snapshot()
        assert snapshot["sandbox_executions"] == 3
        assert snapshot["sandbox_failures"] == 1

    def test_record_security(self):
        from src.agent.metrics import get_metrics_collector, reset_metrics

        reset_metrics()
        mc = get_metrics_collector()
        mc.record_security_review(blocked=False)
        mc.record_security_review(blocked=True)

        snapshot = mc.snapshot()
        assert snapshot["security_reviews"] == 2
        assert snapshot["security_blocks"] == 1

    def test_node_metrics(self):
        from src.agent.metrics import get_metrics_collector, reset_metrics

        reset_metrics()
        mc = get_metrics_collector()
        mc.record_llm_call(node="planner", duration=1.0, tokens=100)
        mc.record_llm_call(node="generator", duration=2.0, tokens=200)

        snapshot = mc.snapshot()
        nodes = snapshot["nodes"]
        assert "planner" in nodes
        assert "generator" in nodes
        assert nodes["planner"]["calls"] == 1
        assert nodes["generator"]["calls"] == 1
