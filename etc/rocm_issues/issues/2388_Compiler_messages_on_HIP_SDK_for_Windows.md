# Compiler messages on HIP SDK for Windows

> **Issue #2388**
> **状态**: closed
> **创建时间**: 2023-08-18T20:01:24Z
> **更新时间**: 2025-01-31T14:48:44Z
> **关闭时间**: 2025-01-31T14:48:34Z
> **作者**: bdenhollander
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2388

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- gargrahul

## 描述

The HIP SDK for Windows is working great thus far. Here are a few suggestions to clean up `hipcc.bin.exe` compiler output on Windows:

- References to `"/usr/local/include"` and `"/usr/include"` could be removed.
- Despite this being HIP: `warning: '--gpu-max-threads-per-block=256' is ignored since it is only supported for HIP`. Is the flag being ignored?
- `x86_64-pc-windows-msvc` is identified correctly in several places but then Linux is mentioned in `"C:\\AMD\\ROCm\\5.5\\bin\\clang-offload-bundler" -type=o -bundle-align=4096 -targets=host-x86_64-unknown-linux`

<details>
<summary>Full compiler output</summary>

```
clang version 17.0.0 (git@github.amd.com:Compute-Mirrors/llvm-project e3201662d21c48894f2156d302276eb1cf47c7be)
Target: x86_64-pc-windows-msvc
Thread model: posix
InstalledDir: C:\AMD\ROCm\5.5\bin
Found HIP installation: C:\AMD\ROCm\5.5, version 5.5.0
 "C:\\AMD\\ROCm\\5.5\\bin\\clang++.exe" -cc1 -triple amdgcn-amd-amdhsa -aux-triple x86_64-pc-windows-msvc -E -save-temps=obj -disable-free -clear-ast-before-backend -disable-llvm-verifier -discard-value-names -main-file-name 48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip.cpp -mrelocation-model pic -pic-level 2 -fhalf-no-semantic-interposition -mframe-pointer=none -menable-no-infs -menable-no-nans -fapprox-func -funsafe-math-optimizations -fno-signed-zeros -mreassociate -freciprocal-math -ffp-contract=fast -fno-rounding-math -ffast-math -ffinite-math-only -mconstructor-aliases -aux-target-cpu x86-64 -fcuda-is-device -mllvm -amdgpu-internalize-symbols --gpu-max-threads-per-block=256 -fcuda-allow-variadic-functions -fvisibility=hidden -fapply-global-visibility-to-externs -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\hip.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\ocml.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\ockl.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_daz_opt_off.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_unsafe_math_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_finite_only_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_correctly_rounded_sqrt_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_wavefrontsize64_off.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_isa_version_1032.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_abi_version_400.bc" -target-cpu gfx1032 -debugger-tuning=gdb -v -resource-dir "C:\\AMD\\ROCm\\5.5\\lib\\clang\\17.0.0" -internal-isystem "C:\\AMD\\ROCm\\5.5\\lib\\clang\\17.0.0\\include\\cuda_wrappers" -idirafter "C:\\AMD\\ROCm\\5.5\\include" -include __clang_hip_runtime_wrapper.h -isystem "C:\\AMD\\ROCm\\5.5\\lib\\clang\\17.0.0\\include\\.." -isystem "C:\\AMD\\ROCm\\5.5\\include" -internal-isystem "C:\\AMD\\ROCm\\5.5\\lib\\clang\\17.0.0\\include" -internal-isystem "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.29.30133\\include" -internal-isystem "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.29.30133\\atlmfc\\include" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\shared" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\um" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\winrt" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\cppwinrt" -internal-isystem "C:\\AMD\\ROCm\\5.5\\lib\\clang\\17.0.0\\include" -internal-isystem "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.29.30133\\include" -internal-isystem "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.29.30133\\atlmfc\\include" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\shared" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\um" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\winrt" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\cppwinrt" -O3 -Wall -std=c++14 -fdeprecated-macro -fno-autolink "-fdebug-compilation-dir=C:\\HIP" -ferror-limit 19 -fmessage-length=120 -fhip-new-launch-api -fms-extensions -fms-compatibility -fms-compatibility-version=19.29.30151 -fdelayed-template-parsing -fcxx-exceptions -fexceptions -fcolor-diagnostics -vectorize-loops -mllvm -amdgpu-early-inline-all=true -mllvm -amdgpu-function-calls=false -cuid=8e7352f2a0fd0b20 -fcuda-allow-variadic-functions -munsafe-fp-atomics -faddrsig -D__GCC_HAVE_DWARF2_CFI_ASM=1 -o "C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip-hip-amdgcn-amd-amdhsa-gfx1032.hipi" -x hip "C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip.cpp"
clang -cc1 version 17.0.0 based upon LLVM 17.0.0git default target x86_64-pc-windows-msvc
ignoring nonexistent directory "/usr/local/include"
ignoring nonexistent directory "/usr/include"
ignoring duplicate directory "C:\AMD\ROCm\5.5\lib\clang\17.0.0\include"
ignoring duplicate directory "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include"
ignoring duplicate directory "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\atlmfc\include"
ignoring duplicate directory "C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\ucrt"
ignoring duplicate directory "C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\shared"
ignoring duplicate directory "C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\um"
ignoring duplicate directory "C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\winrt"
ignoring duplicate directory "C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\cppwinrt"
ignoring duplicate directory "C:\AMD\ROCm\5.5\lib\clang\17.0.0\include"
ignoring duplicate directory "C:\AMD\ROCm\5.5\include"
#include "..." search starts here:
#include <...> search starts here:
 C:\AMD\ROCm\5.5\lib\clang\17.0.0\include\..
 C:\AMD\ROCm\5.5\include
 C:\AMD\ROCm\5.5\lib\clang\17.0.0\include\cuda_wrappers
 C:\AMD\ROCm\5.5\lib\clang\17.0.0\include
 C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include
 C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\atlmfc\include
 C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\ucrt
 C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\shared
 C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\um
 C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\winrt
 C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\cppwinrt
End of search list.
 "C:\\AMD\\ROCm\\5.5\\bin\\clang++.exe" -cc1 -triple amdgcn-amd-amdhsa -aux-triple x86_64-pc-windows-msvc -emit-llvm-bc -emit-llvm-uselists -save-temps=obj -disable-free -clear-ast-before-backend -disable-llvm-verifier -discard-value-names -main-file-name 48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip.cpp -mrelocation-model pic -pic-level 2 -fhalf-no-semantic-interposition -mframe-pointer=none -menable-no-infs -menable-no-nans -fapprox-func -funsafe-math-optimizations -fno-signed-zeros -mreassociate -freciprocal-math -ffp-contract=fast -fno-rounding-math -ffast-math -ffinite-math-only -mconstructor-aliases -aux-target-cpu x86-64 -fcuda-is-device -mllvm -amdgpu-internalize-symbols --gpu-max-threads-per-block=256 -fcuda-allow-variadic-functions -fvisibility=hidden -fapply-global-visibility-to-externs -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\hip.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\ocml.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\ockl.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_daz_opt_off.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_unsafe_math_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_finite_only_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_correctly_rounded_sqrt_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_wavefrontsize64_off.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_isa_version_1032.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_abi_version_400.bc" -target-cpu gfx1032 -mllvm -treat-scalable-fixed-error-as-warning -debugger-tuning=gdb -v -resource-dir "C:\\AMD\\ROCm\\5.5\\lib\\clang\\17.0.0" -O3 -Wall -std=c++14 -fdeprecated-macro -fno-autolink "-fdebug-compilation-dir=C:\\HIP" -ferror-limit 19 -fmessage-length=120 -fhip-new-launch-api -fms-extensions -fms-compatibility -fms-compatibility-version=19.29.30151 -fdelayed-template-parsing -fcxx-exceptions -fexceptions -fcolor-diagnostics -vectorize-loops -mllvm -amdgpu-early-inline-all=true -mllvm -amdgpu-function-calls=false -disable-llvm-passes -cuid=8e7352f2a0fd0b20 -fcuda-allow-variadic-functions -munsafe-fp-atomics -faddrsig -D__GCC_HAVE_DWARF2_CFI_ASM=1 -o "C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip-hip-amdgcn-amd-amdhsa-gfx1032.bc" -x hip-cpp-output "C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip-hip-amdgcn-amd-amdhsa-gfx1032.hipi"
clang -cc1 version 17.0.0 based upon LLVM 17.0.0git default target x86_64-pc-windows-msvc
ignoring nonexistent directory "/usr/local/include"
ignoring nonexistent directory "/usr/include"
#include "..." search starts here:
#include <...> search starts here:
 C:\AMD\ROCm\5.5\lib\clang\17.0.0\include
End of search list.
 "C:\\AMD\\ROCm\\5.5\\bin\\clang++.exe" -cc1 -triple amdgcn-amd-amdhsa -aux-triple x86_64-pc-windows-msvc -S -save-temps=obj -disable-free -clear-ast-before-backend -disable-llvm-verifier -discard-value-names -main-file-name 48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip.cpp -mrelocation-model pic -pic-level 2 -fhalf-no-semantic-interposition -mframe-pointer=none -menable-no-infs -menable-no-nans -fapprox-func -funsafe-math-optimizations -fno-signed-zeros -mreassociate -freciprocal-math -ffp-contract=fast -fno-rounding-math -ffast-math -ffinite-math-only -mconstructor-aliases -aux-target-cpu x86-64 -fcuda-is-device -mllvm -amdgpu-internalize-symbols --gpu-max-threads-per-block=256 -fcuda-allow-variadic-functions -fvisibility=hidden -fapply-global-visibility-to-externs -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\hip.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\ocml.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\ockl.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_daz_opt_off.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_unsafe_math_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_finite_only_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_correctly_rounded_sqrt_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_wavefrontsize64_off.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_isa_version_1032.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.5\\amdgcn\\bitcode\\oclc_abi_version_400.bc" -target-cpu gfx1032 -mllvm -treat-scalable-fixed-error-as-warning -debugger-tuning=gdb -v -resource-dir "C:\\AMD\\ROCm\\5.5\\lib\\clang\\17.0.0" -O3 -Wall -std=c++14 -fno-autolink "-fdebug-compilation-dir=C:\\HIP" -ferror-limit 19 -fmessage-length=120 -fhip-new-launch-api -fms-extensions -fms-compatibility -fms-compatibility-version=19.29.30151 -fdelayed-template-parsing -fcolor-diagnostics -vectorize-loops -mllvm -amdgpu-early-inline-all=true -mllvm -amdgpu-function-calls=false -cuid=8e7352f2a0fd0b20 -fcuda-allow-variadic-functions -munsafe-fp-atomics -faddrsig -o "C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip-hip-amdgcn-amd-amdhsa-gfx1032.s" -x ir "C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip-hip-amdgcn-amd-amdhsa-gfx1032.bc"
warning: '--gpu-max-threads-per-block=256' is ignored since it is only supported for HIP
clang -cc1 version 17.0.0 based upon LLVM 17.0.0git default target x86_64-pc-windows-msvc
1 warning generated.
 "C:\\AMD\\ROCm\\5.5\\bin\\clang++.exe" -cc1as -triple amdgcn-amd-amdhsa -filetype obj -main-file-name 48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip.cpp -target-cpu gfx1032 "-fdebug-compilation-dir=C:\\HIP" -dwarf-version=5 -mrelocation-model pic -mincremental-linker-compatible -mllvm -amdgpu-early-inline-all=true -mllvm -amdgpu-function-calls=false -o "C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip-hip-amdgcn-amd-amdhsa-gfx1032.o" "C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip-hip-amdgcn-amd-amdhsa-gfx1032.s"
 "C:\\AMD\\ROCm\\5.5\\bin\\lld" -flavor gnu -m elf64_amdgpu --no-undefined -shared -plugin-opt=-amdgpu-internalize-symbols -plugin-opt=mcpu=gfx1032 -plugin-opt=O3 --lto-CGO3 -plugin-opt=-amdgpu-early-inline-all=true -plugin-opt=-amdgpu-function-calls=false -save-temps -o "C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip-hip-amdgcn-amd-amdhsa-gfx1032.out" "C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip-hip-amdgcn-amd-amdhsa-gfx1032.o"
 "C:\\AMD\\ROCm\\5.5\\bin\\clang-offload-bundler" -type=o -bundle-align=4096 -targets=host-x86_64-unknown-linux,hipv4-amdgcn-amd-amdhsa--gfx1032 -input=nul "-input=C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hip-hip-amdgcn-amd-amdhsa-gfx1032.out" "-output=C:\\HIP\\48b1fa0c2c3f442e97955f3aaeeafc313e28a359.hsaco"
```
</details>

---

## 评论 (6 条)

### 评论 #1 — saadrahim (2023-08-21T13:11:57Z)

@gargrahul Can you please share this feedback with the windows team?

---

### 评论 #2 — ppanchad-amd (2024-05-14T16:05:04Z)

@bdenhollander Thanks for the feedback.  Can you please check with HIP SDK version 5.7.1? Thanks!

---

### 评论 #3 — bdenhollander (2024-05-14T21:09:57Z)

The second warning about `--gpu-max-threads-per-block=256` is gone in 5.7.1. The first and third items related to Linux are still present.

<details>
<summary>Full compiler output</summary>
clang version 17.0.0 (git@github.amd.com:Compute-Mirrors/llvm-project 6e709f613348e5258188527d11ee8d78376f26b7)
Target: x86_64-pc-windows-msvc
Thread model: posix
InstalledDir: C:\AMD\ROCm\5.7\bin
Found HIP installation: C:\AMD\ROCm\5.7, version 5.7.32000
 "C:\\AMD\\ROCm\\5.7\\bin\\clang++.exe" -cc1 -triple amdgcn-amd-amdhsa -aux-triple x86_64-pc-windows-msvc -emit-obj -mincremental-linker-compatible -disable-free -clear-ast-before-backend -disable-llvm-verifier -discard-value-names -main-file-name s8ac.0.hip.cpp -mrelocation-model pic -pic-level 2 -fhalf-no-semantic-interposition -mframe-pointer=none -menable-no-infs -menable-no-nans -fapprox-func -funsafe-math-optimizations -fno-signed-zeros -mreassociate -freciprocal-math -ffp-contract=fast -fno-rounding-math -ffast-math -ffinite-math-only -mconstructor-aliases -aux-target-cpu x86-64 -fcuda-is-device -mllvm -amdgpu-internalize-symbols --gpu-max-threads-per-block=256 -fcuda-allow-variadic-functions -fvisibility=hidden -fapply-global-visibility-to-externs -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.7\\amdgcn\\bitcode\\hip.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.7\\amdgcn\\bitcode\\ocml.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.7\\amdgcn\\bitcode\\ockl.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.7\\amdgcn\\bitcode\\oclc_daz_opt_off.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.7\\amdgcn\\bitcode\\oclc_unsafe_math_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.7\\amdgcn\\bitcode\\oclc_finite_only_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.7\\amdgcn\\bitcode\\oclc_correctly_rounded_sqrt_on.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.7\\amdgcn\\bitcode\\oclc_wavefrontsize64_off.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.7\\amdgcn\\bitcode\\oclc_isa_version_1032.bc" -mlink-builtin-bitcode "C:\\AMD\\ROCm\\5.7\\amdgcn\\bitcode\\oclc_abi_version_500.bc" -target-cpu gfx1032 -mllvm -treat-scalable-fixed-error-as-warning -debugger-tuning=gdb -v -resource-dir "C:\\AMD\\ROCm\\5.7\\lib\\clang\\17.0.0" -internal-isystem "C:\\AMD\\ROCm\\5.7\\lib\\clang\\17.0.0\\include\\cuda_wrappers" -idirafter "C:\\AMD\\ROCm\\5.7\\include" -include __clang_hip_runtime_wrapper.h -isystem "C:\\AMD\\ROCm\\5.7\\include" -internal-isystem "C:\\AMD\\ROCm\\5.7\\lib\\clang\\17.0.0\\include" -internal-isystem "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.29.30133\\include" -internal-isystem "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.29.30133\\atlmfc\\include" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\shared" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\um" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\winrt" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\cppwinrt" -internal-isystem "C:\\AMD\\ROCm\\5.7\\lib\\clang\\17.0.0\\include" -internal-isystem "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.29.30133\\include" -internal-isystem "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.29.30133\\atlmfc\\include" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\shared" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\um" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\winrt" -internal-isystem "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\cppwinrt" -O3 -Wall -fdeprecated-macro -fno-autolink "-fdebug-compilation-dir=C:\\Users\\~user~\\.conda\\envs\\openmm-8.1\\Library\\share\\openmm\\examples" -ferror-limit 19 -fmessage-length=120 -fhip-new-launch-api -fms-extensions -fms-compatibility -fms-compatibility-version=19.29.30154 -std=c++14 -fdelayed-template-parsing -fcxx-exceptions -fexceptions -fcolor-diagnostics -vectorize-loops -mllvm -amdgpu-early-inline-all=true -mllvm -amdgpu-function-calls=false -cuid=2ea434703a8d8056 -fcuda-allow-variadic-functions -munsafe-fp-atomics -faddrsig -D__GCC_HAVE_DWARF2_CFI_ASM=1 -o "C:\\Users\\~user~\\AppData\\Local\\Temp\\s8ac-gfx1032-4fbb12.o" -x hip "C:\\Users\\~user~\\AppData\\Local\\Temp\\s8ac.0.hip.cpp"
clang -cc1 version 17.0.0 based upon LLVM 17.0.0git default target x86_64-pc-windows-msvc
ignoring nonexistent directory "/usr/local/include"
ignoring nonexistent directory "/usr/include"
ignoring duplicate directory "C:\AMD\ROCm\5.7\lib\clang\17.0.0\include"
ignoring duplicate directory "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include"
ignoring duplicate directory "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\atlmfc\include"
ignoring duplicate directory "C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\ucrt"
ignoring duplicate directory "C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\shared"
ignoring duplicate directory "C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\um"
ignoring duplicate directory "C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\winrt"
ignoring duplicate directory "C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\cppwinrt"
ignoring duplicate directory "C:\AMD\ROCm\5.7\lib\clang\17.0.0\include"
ignoring duplicate directory "C:\AMD\ROCm\5.7\include"
#include "..." search starts here:
#include <...> search starts here:
 C:\AMD\ROCm\5.7\include
 C:\AMD\ROCm\5.7\lib\clang\17.0.0\include\cuda_wrappers
 C:\AMD\ROCm\5.7\lib\clang\17.0.0\include
 C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include
 C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\atlmfc\include
 C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\ucrt
 C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\shared
 C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\um
 C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\winrt
 C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\cppwinrt
End of search list.
 "C:\\AMD\\ROCm\\5.7\\bin\\lld" -flavor gnu -m elf64_amdgpu --no-undefined -shared -plugin-opt=-amdgpu-internalize-symbols -plugin-opt=mcpu=gfx1032 -plugin-opt=O3 --lto-CGO3 -plugin-opt=-amdgpu-early-inline-all=true -plugin-opt=-amdgpu-function-calls=false -o "C:\\Users\\~user~\\AppData\\Local\\Temp\\s8ac-gfx1032-dfb79a.out" "C:\\Users\\~user~\\AppData\\Local\\Temp\\s8ac-gfx1032-4fbb12.o"
 "C:\\AMD\\ROCm\\5.7\\bin\\clang-offload-bundler" -type=o -bundle-align=4096 -targets=host-x86_64-unknown-linux,hipv4-amdgcn-amd-amdhsa--gfx1032 -input=nul "-input=C:\\Users\\~user~\\AppData\\Local\\Temp\\s8ac-gfx1032-dfb79a.out" "-output=C:\\Users\\~user~\\AppData\\Local\\Temp\\s8ac.0.hsaco"
</details>

---

### 评论 #4 — searlmc1 (2024-05-16T16:07:11Z)

+ @david-salinas 

---

### 评论 #5 — david-salinas (2024-07-04T13:48:45Z)

This is an issue with the ROCm Installation Detection code in clang Driver.  I have a PR:  https://github.com/llvm/llvm-project/pull/97668

---

### 评论 #6 — darren-amd (2025-01-31T14:48:34Z)

Hi @bdenhollander,

This appears to be fixed on the latest version of ROCm, please give it a try and create another ticket if the issue persists, thanks!

---
