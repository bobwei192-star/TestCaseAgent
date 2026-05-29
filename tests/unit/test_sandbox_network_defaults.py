from src.agent.nodes.node_sandbox_executor import _build_config
from src.agent.runner import create_initial_state
from src.agent.sandbox.base import SandboxConfig
from src.agent.sandbox.local_docker import LocalDockerSandboxClient


def test_sandbox_config_defaults_to_network_enabled():
    config = SandboxConfig()

    assert config.block_network is False


def test_executor_config_defaults_to_network_enabled():
    config = _build_config({})

    assert config.block_network is False


def test_executor_config_defaults_to_remote_amd_host():
    config = _build_config({})

    assert config.provider == "remote_ssh_docker"
    # 环境变量未设置时，remote_host 为空（#18：已移除硬编码 IP）
    assert config.remote_host == ""
    assert config.remote_user == "jenkins"
    assert config.remote_password == ""
    assert config.device_name == "/dev/kfd,/dev/dri"


def test_initial_state_defaults_to_network_enabled():
    state = create_initial_state("生成一个 pytest 用例")

    assert state["sandbox_config"]["block_network"] is False


def test_initial_state_defaults_to_remote_amd_host():
    state = create_initial_state("生成一个 pytest 用例")

    assert state["sandbox_config"]["provider"] == "remote_ssh_docker"
    # 环境变量未设置时，remote_host 为空（#18：已移除硬编码 IP）
    assert state["sandbox_config"]["remote_host"] == ""
    assert state["sandbox_config"]["remote_user"] == "jenkins"
    # remote_password 不再存入 sandbox_config
    assert state["sandbox_config"]["device_name"] == "/dev/kfd,/dev/dri"


def test_local_docker_omits_network_none_when_network_enabled(monkeypatch):
    calls = {}

    class FakeContainer:
        id = "fake-container-id"

    class FakeContainers:
        def run(self, image, **kwargs):
            calls["image"] = image
            calls["kwargs"] = kwargs
            return FakeContainer()

    class FakeDockerClient:
        containers = FakeContainers()

    class FakeDockerModule:
        class errors:
            class NotFound(Exception):
                pass

        @staticmethod
        def from_env():
            return FakeDockerClient()

    monkeypatch.setattr(
        LocalDockerSandboxClient,
        "_docker_module",
        staticmethod(lambda: FakeDockerModule),
    )

    handle = LocalDockerSandboxClient().create(SandboxConfig(block_network=False))

    assert handle.sandbox_id == "fake-container-id"
    assert calls["kwargs"]["network_mode"] is None


def test_local_docker_uses_network_none_when_block_network_enabled(monkeypatch):
    calls = {}

    class FakeContainer:
        id = "fake-container-id"

    class FakeContainers:
        def run(self, image, **kwargs):
            calls["kwargs"] = kwargs
            return FakeContainer()

    class FakeDockerClient:
        containers = FakeContainers()

    class FakeDockerModule:
        class errors:
            class NotFound(Exception):
                pass

        @staticmethod
        def from_env():
            return FakeDockerClient()

    monkeypatch.setattr(
        LocalDockerSandboxClient,
        "_docker_module",
        staticmethod(lambda: FakeDockerModule),
    )

    LocalDockerSandboxClient().create(SandboxConfig(block_network=True))

    assert calls["kwargs"]["network_mode"] == "none"