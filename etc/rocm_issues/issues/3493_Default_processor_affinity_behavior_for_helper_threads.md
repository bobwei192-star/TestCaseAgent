# Default processor affinity behavior for helper threads

> **Issue #3493**
> **状态**: closed
> **创建时间**: 2024-08-02T18:21:21Z
> **更新时间**: 2024-12-03T22:20:12Z
> **关闭时间**: 2024-12-03T22:20:12Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3493

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.2.0** (颜色: #31778C)

## 描述

Processor affinity is a critical setting to ensure that ROCm helper threads run on the correct cores. By default, ROCm helper threads are spawned on all available cores, ignoring the parent thread’s processor affinity. This can lead to threads competing for available cores, which may result in suboptimal performance. This behavior occurs by default if the environment variable `HSA_OVERRIDE_CPU_AFFINITY_DEBUG` is not set or is set to `1`. If `HSA_OVERRIDE_CPU_AFFINITY_DEBUG` is set to `0`, the ROCr runtime uses the parent process’s core affinity mask when creating helper threads. The parent’s affinity mask should then be set to account for the presence of additional threads by ensuring the affinity mask contains enough cores. Depending on the affinity settings of the software environment, batch system, launch commands like `numactl`/`taskset`, or explicit mask manipulation by the application itself, changing the setting may be advantageous to performance.

To ensure the parent’s core affinity mask is honored by the ROCm helper threads, set the `HSA_OVERRIDE_CPU_AFFINITY_DEBUG` environment variable as follows:

`export HSA_OVERRIDE_CPU_AFFINITY_DEBUG=0`

To ensure ROCm helper threads run on all available cores, set the `HSA_OVERRIDE_CPU_AFFINITY_DEBUG` environment variable as follows:

`export HSA_OVERRIDE_CPU_AFFINITY_DEBUG=1`

Or the default:

`unset HSA_OVERRIDE_CPU_AFFINITY_DEBUG`

If unsure of the default processor affinity settings for your environment, run the following command from the shell:

`bash -c "echo taskset -p \$\$"`

---

## 评论 (1 条)

### 评论 #1 — peterjunpark (2024-12-03T22:20:12Z)

The default behavior of `HSA_OVERRIDE_CPU_AFFINITY_DEBUG` is unchanged. See the documentation at [MI300X system optimization](https://rocm.docs.amd.com/en/latest/how-to/system-optimization/mi300x.html#change-affinity-of-rocm-helper-threads) or [MI300A system optimization](https://rocm.docs.amd.com/en/latest/how-to/system-optimization/mi300a.html#mi300a-processor-affinity) to learn more about this setting for system performance tuning.

---
