"""
test_gpu_temperature.py — ROCm GPU 温度测试

测试内容：
  1. test_gpu_temperature_in_range : GPU 温度在 0~110°C 安全范围内
  2. test_gpu_temperature_reading_validity : 温度读数是有效数值（非 NaN、非负、非异常值）

所有数据均通过真实命令 rocm-smi 或真实 sysfs 文件获取，无 mock、无硬编码。
"""

import re
import shutil
import subprocess
import glob as glob_mod
import pytest


# ── 辅助函数 ──────────────────────────────────────────────


def _is_rocm_smi_available() -> bool:
    """检测 rocm-smi 命令是否存在且可执行。"""
    return shutil.which("rocm-smi") is not None


def _has_gpu_device() -> bool:
    """检测系统是否存在 AMD GPU 设备（通过 sysfs）。"""
    return len(glob_mod.glob("/sys/class/drm/card*/device/")) > 0


def _gpu_temp_via_rocm_smi() -> float:
    """通过 rocm-smi --showtemp 获取 GPU 温度，返回摄氏度。"""
    result = subprocess.run(
        ["rocm-smi", "--showtemp"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"rocm-smi 返回非零退出码 {result.returncode}\n"
            f"stderr: {result.stderr.strip()}"
        )

    # 典型输出: "GPU[0] : Temperature (Sensor 0) (C) : 45.0"
    match = re.search(r"Temperature.*\(C\).*:\s*([\d.]+)", result.stdout)
    if not match:
        raise RuntimeError(
            f"无法从 rocm-smi 输出中解析温度值\n"
            f"stdout: {result.stdout.strip()}"
        )
    return float(match.group(1))


def _gpu_temp_via_sysfs() -> float:
    """回退方案：通过 sysfs 读取 GPU 温度，返回摄氏度。

    sysfs 温度单位为毫摄氏度（millidegree Celsius），需除以 1000。
    """
    hwmon_dirs = glob_mod.glob(
        "/sys/class/drm/card*/device/hwmon/hwmon*/temp1_input"
    )
    if not hwmon_dirs:
        raise RuntimeError("未找到 sysfs 温度文件 (temp1_input)")

    # 取第一个 GPU 的温度
    temp_path = hwmon_dirs[0]
    with open(temp_path, "r") as f:
        raw = f.read().strip()

    if not raw:
        raise RuntimeError(f"sysfs 文件 {temp_path} 内容为空")

    try:
        millidegree = int(raw)
    except ValueError:
        raise RuntimeError(
            f"sysfs 文件 {temp_path} 内容无法转为整数: {raw!r}"
        )

    return millidegree / 1000.0


def _get_gpu_temperature() -> float:
    """获取 GPU 温度，优先 rocm-smi，失败回退 sysfs。

    Returns:
        float: GPU 温度（摄氏度）

    Raises:
        RuntimeError: 所有方案均失败时抛出，附带完整诊断信息。
    """
    errors = []

    if _is_rocm_smi_available():
        try:
            return _gpu_temp_via_rocm_smi()
        except (subprocess.TimeoutExpired, RuntimeError, OSError) as e:
            errors.append(f"rocm-smi 方案失败: {e}")

    if _has_gpu_device():
        try:
            return _gpu_temp_via_sysfs()
        except (OSError, RuntimeError) as e:
            errors.append(f"sysfs 方案失败: {e}")

    raise RuntimeError(
        "所有 GPU 温度获取方案均失败:\n" + "\n".join(errors)
    )


# ── 跳过条件 ──────────────────────────────────────────────

no_gpu = not _has_gpu_device()
no_rocm_smi = not _is_rocm_smi_available()
skip_no_gpu = pytest.mark.skipif(
    no_gpu and no_rocm_smi,
    reason="系统无 AMD GPU 设备且 rocm-smi 不可用",
)


# ── 测试用例 1: 温度范围检查 ──────────────────────────────


@skip_no_gpu
def test_gpu_temperature_in_range():
    """验证 GPU 温度在 0~110°C 安全范围内。

    真实执行 rocm-smi --showtemp 或读取 sysfs 温度文件，
    断言温度值在合理物理范围内。
    """
    try:
        temp = _get_gpu_temperature()
    except RuntimeError as e:
        pytest.fail(f"获取 GPU 温度失败: {e}")

    assert 0 <= temp <= 110, (
        f"GPU 温度 {temp:.1f}°C 超出安全范围 (0~110°C)"
    )


# ── 测试用例 2: 温度读数有效性检查 ──────────────────────


@skip_no_gpu
def test_gpu_temperature_reading_validity():
    """验证 GPU 温度读数是有效数值。

    检查项：
      - 温度值不是 NaN
      - 温度值 >= 0（物理上不可能为负的绝对温度）
      - 温度值 < 200°C（异常值检测，防止传感器故障误报）
      - 温度值可以通过 float() 正确解析
    """
    try:
        temp = _get_gpu_temperature()
    except RuntimeError as e:
        pytest.fail(f"获取 GPU 温度失败: {e}")

    # 检查是否为有效浮点数
    assert isinstance(temp, (int, float)), (
        f"温度值类型异常: {type(temp).__name__}, 值: {temp!r}"
    )

    # 检查 NaN
    assert not (isinstance(temp, float) and temp != temp), (
        f"温度值为 NaN"
    )

    # 检查无穷大
    assert not (isinstance(temp, float) and abs(temp) == float("inf")), (
        f"温度值为无穷大: {temp}"
    )

    # 检查非负
    assert temp >= 0, (
        f"GPU 温度为负值: {temp:.1f}°C，传感器可能异常"
    )

    # 检查异常高温（传感器故障检测）
    assert temp < 200, (
        f"GPU 温度 {temp:.1f}°C 异常高（>200°C），疑似传感器故障"
    )

    # 输出实际温度供诊断参考
    print(f"\n  [INFO] GPU 温度: {temp:.1f}°C")
