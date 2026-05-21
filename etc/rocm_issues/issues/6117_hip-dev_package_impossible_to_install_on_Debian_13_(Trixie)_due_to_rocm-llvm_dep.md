# hip-dev package impossible to install on Debian 13 (Trixie) due to rocm-llvm dependency on ancient libstdc++

> **Issue #6117**
> **状态**: closed
> **创建时间**: 2026-04-04T04:17:32Z
> **更新时间**: 2026-04-06T20:11:14Z
> **关闭时间**: 2026-04-06T20:11:14Z
> **作者**: manishthatte
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6117

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

## Summary

On Debian 13 Trixie, the `hip-dev` package from AMD's ROCm 6.4 repository cannot be installed. It pulls in `rocm-llvm`, which declares a dependency on `libstdc++-5-dev | libstdc++-7-dev | libstdc++-11-dev`. Debian 13 ships only `libstdc++-14-dev`. The dependency cannot be satisfied, making the `-dev` side of the ROCm stack uninstallable on current Debian stable.

## Environment

- **OS:** Debian 13 Trixie, kernel 6.12.74
- **ROCm version:** 6.4.0 (from AMD's `noble` Ubuntu repository)
- **GPU:** 2x AMD Radeon Pro W7900 (RDNA3, gfx1100)
- **System compiler:** GCC 14.2.0 / clang-19 (LLVM 19)

## Reproduction

```bash
sudo apt install hip-dev
```

**Result:**
```
rocm-llvm : Depends: libstdc++-5-dev but it is not installable or
                     libstdc++-7-dev but it is not installable or
                     libstdc++-11-dev but it is not installable
```

**Runtime packages all install fine:**
```bash
sudo apt install hip-runtime-amd hipblas rocblas rocfft hipsolver  # all succeed
```

## Impact

Without `hip-dev`, there are no CMake config files for `hip::amdhip64`, `hip::host`, or `hip::device`. Any project using `find_package(hip)` fails at configure time, even though the GPU runtime is fully functional.

| Package | Installs? |
|---|---|
| `hip-runtime-amd`, `hipblas`, `rocblas`, `rocfft` | Yes |
| `hip-dev`, `rocm-dev` | **No** — blocked by `rocm-llvm` |

## Workaround (confirmed working)

1. Custom `hipcc` wrapper using system `clang++-19` with `--rocm-path=/opt/rocm --offload-arch=gfx1100 -x hip`
2. Manual CMake config files for `hip::amdhip64`, `hip::host`, `hip::device` pointing to `/opt/rocm/lib/libamdhip64.so.6`
3. Filter GCC-specific flags (`-mcpu=native`) that clang rejects

This workaround was validated by successfully building and running ABINIT 10.6.5 with full HIP GPU support (hipblas, rocblas, rocfft, hipsolver) on 2x W7900.

## Suggested fix

Update `rocm-llvm` dependency to include `libstdc++-14-dev`:

```
Depends: libstdc++-5-dev | libstdc++-7-dev | libstdc++-11-dev | libstdc++-14-dev
```

Or provide a Debian 13 native repository, or make `hip-dev` not depend on `rocm-llvm` when system clang (17+) is available.

---

## 评论 (1 条)

### 评论 #1 — tcgu-amd (2026-04-06T20:11:14Z)

Hi @manishthatte, thanks for reaching out! This has been a known issue and was fixed in ROCm 7.10 (see https://github.com/ROCm/ROCm/issues/4612/). Unfortunately, we do not have plans to backport the fix to earlier versions. But thanks for coming up with a workaround! I will be closing this issue. Please feel free to follow up if you have any other questions. Thank you!

---
