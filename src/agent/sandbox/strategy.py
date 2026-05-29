"""策略模式执行器 - 根据意图选择执行策略

根据 guide/09_promot优化.md 设计：
- PytestStrategy: 执行 pytest 测试（本机）
- LocalDockerPytestStrategy: 在本地 Docker 容器中执行 pytest
- DockerBuildStrategy: 执行 docker build
- ExternalRunStrategy: 执行外部套件
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import os
import io
import tarfile
import time
import shutil

from ..intent_router import IntentType


class ExecutionStrategy(ABC):
    """执行策略接口"""

    @abstractmethod
    def execute(self, artifact_path: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """执行策略

        Args:
            artifact_path: 生成的产物路径（test_xxx.py 或 Dockerfile）
            state: 当前状态

        Returns:
            执行结果
        """
        pass


class PytestStrategy(ExecutionStrategy):
    """Pytest 测试执行策略"""

    def execute(self, artifact_path: str, state: Dict[str, Any]) -> Dict[str, Any]:
        import subprocess
        import tempfile
        import os

        print(f"[策略执行] 使用 PytestStrategy 执行: {artifact_path}")

        # 创建临时目录用于执行
        with tempfile.TemporaryDirectory() as tmp_dir:
            # 复制测试文件到临时目录
            test_filename = os.path.basename(artifact_path)
            dest_path = os.path.join(tmp_dir, test_filename)
            
            try:
                with open(artifact_path, 'r') as src, open(dest_path, 'w') as dst:
                    dst.write(src.read())
            except Exception as e:
                return {"status": "failed", "errors": [f"无法读取测试文件: {e}"]}

            # 执行 pytest
            try:
                result = subprocess.run(
                    ["python", "-m", "pytest", dest_path, "-v", "--tb=short"],
                    cwd=tmp_dir,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                return {
                    "status": "success" if result.returncode == 0 else "failed",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
            except subprocess.TimeoutExpired:
                return {"status": "failed", "errors": ["测试执行超时"]}
            except Exception as e:
                return {"status": "failed", "errors": [f"执行失败: {e}"]}


class LocalDockerPytestStrategy(ExecutionStrategy):
    """在本地 Docker 容器中执行 pytest 测试策略"""

    def __init__(self):
        self._docker_prefix = ""
        self._container_id = None

    def _check_docker_access(self):
        """检查 Docker 访问权限，尝试使用 sg 命令"""
        import subprocess
        
        # 首先尝试直接访问
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            self._docker_prefix = ""
            return True
        
        # 如果没有权限，尝试使用 sg docker
        if shutil.which("sg") is not None:
            result = subprocess.run(
                ["sg", "docker", "-c", "docker info"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self._docker_prefix = "sg docker -c"
                print("[策略执行] 使用 sg docker 执行 Docker 命令")
                return True
        
        return False

    def _run_docker_command(self, command):
        """执行 Docker 命令"""
        import subprocess
        import shlex

        if self._docker_prefix:
            # sg 内部用 /bin/sh (dash) 执行命令，嵌套引号极易出错
            # 使用 shlex.quote() 安全转义整个命令字符串
            full_command = f"{self._docker_prefix} {shlex.quote(command)}"
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True
            )
        else:
            # 使用 shlex.split() 正确解析 shell 引号，
            # 避免 command.split() 把单引号字符串拆碎
            result = subprocess.run(
                shlex.split(command),
                capture_output=True,
                text=True
            )

        return result

    def _upload_file_to_container(self, container_id, content, remote_path):
        """使用 docker cp 将文件上传到容器"""
        import subprocess
        import tempfile
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            # 使用 docker cp 上传文件
            command = f"docker cp {temp_path} {container_id}:{remote_path}"
            result = self._run_docker_command(command)
            if result.returncode != 0:
                raise RuntimeError(f"上传文件失败: {result.stderr}")
        finally:
            os.unlink(temp_path)

    def execute(self, artifact_path: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """在本地 Docker 容器中执行 pytest 测试"""
        print(f"[策略执行] 使用 LocalDockerPytestStrategy 执行: {artifact_path}")

        # 检查 Docker 访问权限
        if not self._check_docker_access():
            return {"status": "failed", "errors": ["无法访问 Docker，请检查权限配置"]}

        # 获取配置
        image = state.get("sandbox_image", os.environ.get("TEST_CASE_AGENT_SANDBOX_IMAGE", "python:3.12-slim"))
        timeout = int(state.get("sandbox_timeout", 120))
        device_name = state.get("device_name", os.environ.get("TEST_CASE_AGENT_DEVICE_NAME", ""))

        # 读取测试文件内容
        try:
            with open(artifact_path, 'r') as f:
                test_content = f.read()
        except Exception as e:
            return {"status": "failed", "errors": [f"无法读取测试文件: {e}"]}

        try:
            # 构建设备参数
            device_args = ""
            if device_name:
                devices = [d.strip() for d in device_name.split(",") if d.strip()]
                device_args = " ".join(f"--device {d}" for d in devices)

            # 创建容器
            print("[策略执行] 创建 Docker 容器...")
            command = f"docker run -d {device_args} -w /tmp/testcase_agent {image} sleep infinity"
            result = self._run_docker_command(command)
            if result.returncode != 0:
                return {"status": "failed", "errors": [f"创建容器失败: {result.stderr}"]}
            
            container_id = result.stdout.strip()
            self._container_id = container_id
            print(f"[策略执行] 容器创建成功: {container_id[:12]}")

            # 上传测试文件
            print("[策略执行] 上传测试文件...")
            self._upload_file_to_container(container_id, test_content, "/tmp/testcase_agent/test_generated.py")
            print("[策略执行] 测试文件上传成功")

            # 安装 pytest（如果需要）
            print("[策略执行] 安装 pytest...")
            command = f"docker exec {container_id} sh -lc 'python -m pytest --version >/dev/null 2>&1 || python -m pip install pytest -q'"
            result = self._run_docker_command(command)
            if result.returncode != 0:
                return {"status": "failed", "errors": [f"安装 pytest 失败: {result.stderr}"]}

            # 执行测试
            print("[策略执行] 执行 pytest...")
            started = time.time()
            command = f"docker exec {container_id} sh -lc 'timeout {timeout}s python -m pytest test_generated.py -v --tb=short'"
            result = self._run_docker_command(command)
            duration = time.time() - started

            return {
                "status": "success" if result.returncode == 0 else "failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "duration_seconds": duration,
                "container_id": container_id[:12]
            }

        except Exception as e:
            return {"status": "failed", "errors": [f"Docker 执行失败: {str(e)}"]}

        finally:
            # 清理容器
            if self._container_id:
                try:
                    command = f"docker rm -f {self._container_id}"
                    self._run_docker_command(command)
                    print(f"[策略执行] 容器已清理: {self._container_id[:12]}")
                except Exception as e:
                    print(f"[策略执行] 清理容器失败: {e}")


class DockerBuildStrategy(ExecutionStrategy):
    """Docker 构建策略"""

    def execute(self, artifact_path: str, state: Dict[str, Any]) -> Dict[str, Any]:
        import subprocess
        import re

        print(f"[策略执行] 使用 DockerBuildStrategy 构建: {artifact_path}")

        try:
            # 提取镜像标签（从状态或文件名）
            image_tag = state.get("image_tag", "rocm-test:latest")
            
            # 执行 docker build
            result = subprocess.run(
                ["docker", "build", "-f", artifact_path, "-t", image_tag, "."],
                capture_output=True,
                text=True,
                timeout=300
            )

            # 提取镜像标签
            image_tag_output = image_tag
            if result.returncode == 0:
                # 尝试从输出中提取镜像 ID
                match = re.search(r'Successfully built (\w+)', result.stdout)
                if match:
                    image_tag_output = f"{image_tag} ({match.group(1)})"

            return {
                "status": "success" if result.returncode == 0 else "failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "image_tag": image_tag_output
            }
        except subprocess.TimeoutExpired:
            return {"status": "failed", "errors": ["Docker 构建超时"]}
        except Exception as e:
            return {"status": "failed", "errors": [f"Docker 构建失败: {e}"]}


class ExternalRunStrategy(ExecutionStrategy):
    """外部套件执行策略"""

    def execute(self, artifact_path: str, state: Dict[str, Any]) -> Dict[str, Any]:
        import subprocess

        print(f"[策略执行] 使用 ExternalRunStrategy 执行: {artifact_path}")

        try:
            # 执行外部脚本/命令
            result = subprocess.run(
                ["bash", artifact_path],
                capture_output=True,
                text=True,
                timeout=300
            )

            return {
                "status": "success" if result.returncode == 0 else "failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "report": result.stdout[:2000] if result.stdout else ""
            }
        except subprocess.TimeoutExpired:
            return {"status": "failed", "errors": ["外部执行超时"]}
        except Exception as e:
            return {"status": "failed", "errors": [f"外部执行失败: {e}"]}


class StrategyFactory:
    """策略工厂 - 根据意图和配置获取执行策略"""

    _strategies: Dict[IntentType, ExecutionStrategy] = {
        "GENERATE": PytestStrategy(),
        "APPEND": PytestStrategy(),
        "UPDATE": PytestStrategy(),
        "REFACTOR": PytestStrategy(),
        "ENV_BUILD": DockerBuildStrategy(),
        "EXECUTE_EXTERNAL": ExternalRunStrategy(),
        # DIAGNOSE/COVERAGE/PROBE 不需要执行策略（查询类）
        "DIAGNOSE": PytestStrategy(),  # 默认策略，实际不会被调用
        "COVERAGE": PytestStrategy(),
        "PROBE": PytestStrategy(),
    }

    @classmethod
    def get_strategy(cls, intent: IntentType) -> ExecutionStrategy:
        """根据意图获取执行策略（默认使用本机执行）

        Args:
            intent: 意图类型

        Returns:
            对应的执行策略
        """
        return cls._strategies.get(intent, PytestStrategy())

    @classmethod
    def _check_docker_available(cls) -> bool:
        """检查 Docker 是否可用"""
        import subprocess
        
        # 尝试直接访问
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True
        
        # 尝试使用 sg docker
        if shutil.which("sg") is not None:
            result = subprocess.run(
                ["sg", "docker", "-c", "docker info"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True
        
        return False

    @classmethod
    def get_strategy_with_config(cls, intent: IntentType, state: Dict[str, Any] = None) -> ExecutionStrategy:
        """根据意图和配置获取执行策略

        如果配置了远程主机且无法连接，则回退到本地 Docker 执行。
        如果本地 Docker 也无法访问，则回退到本机执行。

        Args:
            intent: 意图类型
            state: 当前状态，包含配置信息

        Returns:
            对应的执行策略
        """
        if state is None:
            state = {}

        # 检查是否配置了远程执行
        remote_host = state.get("remote_host") or os.environ.get("TEST_CASE_AGENT_REMOTE_HOST")
        
        # 如果没有配置远程主机，尝试使用本地 Docker
        if not remote_host or remote_host.strip() == "":
            # 检查 Docker 是否可用
            if cls._check_docker_available():
                print("[策略工厂] 未配置远程主机，使用本地 Docker 执行")
                if intent in ["GENERATE", "APPEND", "UPDATE", "REFACTOR"]:
                    return LocalDockerPytestStrategy()
            else:
                print("[策略工厂] 未配置远程主机，且 Docker 不可用，使用本机执行")
            
            return cls._strategies.get(intent, PytestStrategy())

        # 检查是否强制使用本地 Docker
        sandbox_provider = state.get("sandbox_provider") or os.environ.get("TEST_CASE_AGENT_SANDBOX_PROVIDER", "")
        if sandbox_provider == "local_docker":
            if cls._check_docker_available():
                print("[策略工厂] 配置强制使用本地 Docker")
                if intent in ["GENERATE", "APPEND", "UPDATE", "REFACTOR"]:
                    return LocalDockerPytestStrategy()
            else:
                print("[策略工厂] 配置强制使用本地 Docker，但 Docker 不可用，回退到本机执行")
            
            return cls._strategies.get(intent, PytestStrategy())

        # 默认使用普通策略
        return cls._strategies.get(intent, PytestStrategy())

    @classmethod
    def register_strategy(cls, intent: IntentType, strategy: ExecutionStrategy) -> None:
        """注册自定义策略

        Args:
            intent: 意图类型
            strategy: 执行策略实例
        """
        cls._strategies[intent] = strategy


def execute_with_strategy(intent: IntentType, artifact_path: str, 
                          state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """使用策略模式执行

    根据配置自动选择执行策略：
    - 如果配置了远程主机但无法连接，自动回退到本地 Docker
    - 如果没有配置远程主机，直接使用本地 Docker

    Args:
        intent: 意图类型
        artifact_path: 生成的产物路径
        state: 当前状态（可选）

    Returns:
        执行结果
    """
    if state is None:
        state = {}

    # 使用带配置的策略选择，支持自动回退到本地 Docker
    strategy = StrategyFactory.get_strategy_with_config(intent, state)
    return strategy.execute(artifact_path, state)