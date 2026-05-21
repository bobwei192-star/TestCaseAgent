# [Issue]: rocminfo.exe does not exist

> **Issue #4024**
> **状态**: closed
> **创建时间**: 2024-11-10T20:26:16Z
> **更新时间**: 2024-11-11T15:43:25Z
> **关闭时间**: 2024-11-11T15:43:24Z
> **作者**: linghubingli
> **标签**: ROCm 6.1.0, OrayIddDriver Device AMD Radeon RX 6750 GRE 12GB
> **URL**: https://github.com/ROCm/ROCm/issues/4024

## 标签

- **ROCm 6.1.0** (颜色: #ededed)
- **OrayIddDriver Device AMD Radeon RX 6750 GRE 12GB** (颜色: #ededed)

## 描述

### Problem Description

After installing with the HIP SDK, I can't find the rocminfo file in the bin folder
Here are my py files:

import subprocess
import os

# 设置环境变量
os.environ['HIP_PATH'] = 'D:\\ROCm\\6.1'
os.environ['ROCM_PATH'] = 'D:\\ROCm\\6.1'

# 定义要调用的命令
commands = [
    ('rocminfo', ['rocminfo']),
    ('amdgpu-arch', ['amdgpu-arch']),
    ('clang', ['clang', '--version']),
    ('clang++', ['clang++', '--version']),
    ('clang-cl', ['clang-cl', '--version']),
    ('clang-format', ['clang-format', '--version']),
    ('clang-offload-bundler', ['clang-offload-bundler', '--help']),
    ('hipcc', ['hipcc', '--version']),
    ('hipconfig', ['hipconfig']),
    ('hipify-clang', ['hipify-clang', '--help']),
    ('hipInfo', ['hipInfo']),
    ('ld.lld', ['ld.lld', '--version']),
    ('lld', ['lld', '--version']),
    ('lld-link', ['lld-link', '--version']),
    ('llvm-ar', ['llvm-ar', '--version']),
    ('opt', ['opt', '--version'])
]

# 执行命令并捕获输出
for name, cmd in commands:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"=== {name} ===")
        print(result.stdout)
        print(f"=== {name} (stderr) ===")
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"=== {name} (error) ===")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print(f"=== {name} (not found) ===")
        print(f"The command '{name}' was not found.")

But his output was:

D:\gpligins\plugins>python tempfile_1731269073941.py
=== rocminfo (not found) ===
The command 'rocminfo' was not found.
=== amdgpu-arch ===
gfx1031

=== amdgpu-arch (stderr) ===

=== clang ===
clang version 19.0.0git (git@github.amd.com:Compute-Mirrors/llvm-project b3dbdf4f03718d63a3292f784216fddb3e73d521)
Target: x86_64-pc-windows-msvc
Thread model: posix
InstalledDir: D:\ROCm\6.1\bin

=== clang (stderr) ===

=== clang++ ===
clang version 19.0.0git (git@github.amd.com:Compute-Mirrors/llvm-project b3dbdf4f03718d63a3292f784216fddb3e73d521)
Target: x86_64-pc-windows-msvc
Thread model: posix
InstalledDir: D:\ROCm\6.1\bin

=== clang++ (stderr) ===

=== clang-cl ===
clang version 19.0.0git (git@github.amd.com:Compute-Mirrors/llvm-project b3dbdf4f03718d63a3292f784216fddb3e73d521)
Target: x86_64-pc-windows-msvc
Thread model: posix
InstalledDir: D:\ROCm\6.1\bin

=== clang-cl (stderr) ===

=== clang-format ===
clang-format version 19.0.0git (git@github.amd.com:Compute-Mirrors/llvm-project b3dbdf4f03718d63a3292f784216fddb3e73d521)

=== clang-format (stderr) ===

=== clang-offload-bundler ===
OVERVIEW: A tool to bundle several input files of the specified type <type>
referring to the same source file but different targets into a single
one. The resulting file can also be unbundled into different files by
this tool if -unbundle is provided.

USAGE: clang-offload-bundler [options]

OPTIONS:

Generic Options:

  --help                  - Display available options (--help-hidden for more)
  --help-list             - Display list of available options (--help-list-hidden for more)
  --version               - Display the version of this program

clang-offload-bundler options:

  --###                   - Print any external commands that are to be executed instead of actually executing them - for testing purposes.
  --allow-missing-bundles - Create empty files if bundles are missing when unbundling.
  --bundle-align=<uint>   - Alignment of bundle for binary files
  --check-input-archive   - Check if input heterogeneous archive is valid in terms of TargetID rules.
  --compress              - Compress output file when bundling.
  --hip-openmp-compatible - Treat hip and hipv4 offload kinds as compatible with openmp kind, and vice versa.
  --input=<string>        - Input file. Can be specified multiple times for multiple input files.
  --inputs=<string>       - [<input file>,...] (deprecated)
  --list                  - List bundle IDs in the bundled file.
  --output=<string>       - Output file. Can be specified multiple times for multiple output files.
  --outputs=<string>      - [<output file>,...] (deprecated)
  --targets=<string>      - [<offload kind>-<target triple>,...]
  --type=<string>         - Type of the files to be bundled/unbundled.
                            Current supported types are:
                              i    - cpp-output
                              ii   - c++-cpp-output
                              cui  - cuda-cpp-output
                              hipi - hip-cpp-output
                              d    - dependency
                              ll   - llvm
                              bc   - llvm-bc
                              s    - assembler
                              o    - object
                              a    - archive of objects
                              gch  - precompiled-header
                              ast  - clang AST file
  --unbundle              - Unbundle bundled file into several output files.
  --verbose               - Print debug information.

=== clang-offload-bundler (stderr) ===

=== hipcc (not found) ===
The command 'hipcc' was not found.
=== hipconfig (not found) ===
The command 'hipconfig' was not found.
=== hipify-clang ===
USAGE: hipify-clang [options] <source0> [... <sourceN>]

OPTIONS:

CUDA to HIP source translator options:

  --                                              - Separator between hipify-clang and clang options; don't specify if there are no clang options
  -D <macro>=<value>                              - Define <macro> to <value> or 1 if <value> omitted
  -I <directory>                                  - Add directory to include search path
  --amap                                          - Try to hipify as much as possible; ignores 'default-preprocessor'
  --clang-resource-directory=<directory>          - The clang resource path - the path to the parent folder for the 'include' folder, containing '__clang_cuda_runtime_wrapper.h' and other header files used on runtime
  --csv                                           - Generate documentation in CSV format
  --cuda-gpu-arch=<value>                         - CUDA GPU architecture (e.g. sm_35); may be specified more than once
  --cuda-kernel-execution-syntax                  - Keep CUDA kernel launch syntax (default)
  --cuda-path=<directory>                         - CUDA installation path
  --default-preprocessor                          - Enable default preprocessor behaviour (synonymous with '--skip-excluded-preprocessor-conditional-blocks')
  --doc-format=<value>                            - Documentation format: 'full' (default), 'strict', or 'compact'; the '--md' or '--csv' option must be specified
  --doc-roc=<value>                               - ROC documentation generation: 'skip' (default), 'separate', or 'joint'; the '--md' or '--csv' option must be specified
  --examine                                       - Combine the '-no-output' and '-print-stats' options
  --experimental                                  - Hipify HIP APIs that are experimentally supported, otherwise, the corresponding warnings will be emitted
  --extra-arg=<string>                            - Additional argument to append to the compiler command line
  --extra-arg-before=<string>                     - Additional argument to prepend to the compiler command line
  --hip-kernel-execution-syntax                   - Transform CUDA kernel launch syntax to a regular HIP function call (overrides '--cuda-kernel-execution-syntax')
  --inplace                                       - Modify input file in-place
  --md                                            - Generate documentation in Markdown format
  --miopen                                        - Translate to 'miopen' instead of 'hip' where it is possible
  --no-backup                                     - Don't create a backup file for the hipified source
  --no-output                                     - Don't write any translated output to stdout
  --no-undocumented-features                      - Do not rely on undocumented features in code transformation
  --no-warnings-on-undocumented-features          - Suppress warnings on undocumented features in code transformation
  -o <filename>                                   - Output filename
  --o-dir=<directory>                             - Output directory
  --o-hipify-perl-dir=<directory>                 - Output directory for hipify-perl script
  --o-python-map-dir=<directory>                  - Output directory for Python map
  --o-stats=<filename>                            - Output filename for statistics
  -p <string>                                     - Build path
  --perl                                          - Generate hipify-perl
  --print-stats                                   - Print translation statistics
  --print-stats-csv                               - Print translation statistics in a CSV file
  --python                                        - Generate hipify-python
  --roc                                           - Translate to 'roc' instead of 'hip' where it is possible
  --save-temps                                    - Save temporary files
  --skip-excluded-preprocessor-conditional-blocks - Enable default preprocessor behaviour by skipping undefined conditional blocks
  --temp-dir=<directory>                          - Temporary directory
  --use-hip-data-types                            - Use 'hipDataType' instead of 'hipblasDatatype_t' or 'rocblas_datatype'
  -v                                              - Show commands to run and use verbose output
  --versions                                      - Display the versions of the supported 3rd-party software

Generic Options:

  --help                                          - Display available options (--help-hidden for more)
  --help-list                                     - Display list of available options (--help-list-hidden for more)
  --version                                       - Display the version of this program

-p <build-path> is used to read a compile command database.

        For example, it can be a CMake build directory in which a file named
        compile_commands.json exists (use -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
        CMake option to get this output). When no build path is specified,
        a search for compile_commands.json will be attempted through all
        parent paths of the first input file . See:
        https://clang.llvm.org/docs/HowToSetupToolingForLLVM.html for an
        example of setting up Clang Tooling on a source tree.

<source0> ... specify the paths of source files. These paths are
        looked up in the compile command database. If the path of a file is
        absolute, it needs to point into CMake's source tree. If the path is
        relative, the current working directory needs to be in the CMake
        source tree and the file must be in a subdirectory of the current
        working directory. "./" prefixes in the relative files will be
        automatically removed, but the rest of a relative path must be a
        suffix of a path in the compile command database.


=== hipify-clang (stderr) ===

=== hipInfo ===

--------------------------------------------------------------------------------
device#                           0
Name:                             AMD Radeon RX 6750 GRE 12GB
pciBusID:                         3
pciDeviceID:                      0
pciDomainID:                      0
multiProcessorCount:              20
maxThreadsPerMultiProcessor:      2048
isMultiGpuBoard:                  0
clockRate:                        2439 Mhz
memoryClockRate:                  1000 Mhz
memoryBusWidth:                   0
totalGlobalMem:                   11.98 GB
totalConstMem:                    2147483647
sharedMemPerBlock:                64.00 KB
canMapHostMemory:                 1
regsPerBlock:                     0
warpSize:                         32
l2CacheSize:                      4194304
computeMode:                      0
maxThreadsPerBlock:               1024
maxThreadsDim.x:                  1024
maxThreadsDim.y:                  1024
maxThreadsDim.z:                  1024
maxGridSize.x:                    2147483647
maxGridSize.y:                    65536
maxGridSize.z:                    65536
major:                            10
minor:                            3
concurrentKernels:                1
cooperativeLaunch:                0
cooperativeMultiDeviceLaunch:     0
isIntegrated:                     0
maxTexture1D:                     16384
maxTexture2D.width:               16384
maxTexture2D.height:              16384
maxTexture3D.width:               2048
maxTexture3D.height:              2048
maxTexture3D.depth:               2048
hostNativeAtomicSupported:        1
isLargeBar:                       0
asicRevision:                     0
maxSharedMemoryPerMultiProcessor: 64.00 KB
clockInstructionRate:             1000.00 Mhz
arch.hasGlobalInt32Atomics:       1
arch.hasGlobalFloatAtomicExch:    1
arch.hasSharedInt32Atomics:       1
arch.hasSharedFloatAtomicExch:    1
arch.hasFloatAtomicAdd:           1
arch.hasGlobalInt64Atomics:       1
arch.hasSharedInt64Atomics:       1
arch.hasDoubles:                  1
arch.hasWarpVote:                 1
arch.hasWarpBallot:               1
arch.hasWarpShuffle:              1
arch.hasFunnelShift:              0
arch.hasThreadFenceSystem:        1
arch.hasSyncThreadsExt:           0
arch.hasSurfaceFuncs:             0
arch.has3dGrid:                   1
arch.hasDynamicParallelism:       0
gcnArchName:                      gfx1031
peers:
non-peers:                        device#0

memInfo.total:                    11.98 GB
memInfo.free:                     11.85 GB (99%)


=== hipInfo (stderr) ===

=== ld.lld (not found) ===
The command 'ld.lld' was not found.
=== lld (error) ===
Return code: 1
Output:
Stderr: lld is a generic driver.
Invoke ld.lld (Unix), ld64.lld (macOS), lld-link (Windows), wasm-ld (WebAssembly) instead

=== lld-link ===
LLD 19.0.0

=== lld-link (stderr) ===

=== llvm-ar ===
AOMP-18.0-12 (http://github.com/ROCm-Developer-Tools/aomp):
 Source ID:18.0-12-ce1873ac686bb90ddec72bb99889a4e80e2de382
  LLVM version 19.0.0git
  Optimized build.

=== llvm-ar (stderr) ===

=== opt ===
AOMP-18.0-12 (http://github.com/ROCm-Developer-Tools/aomp):
 Source ID:18.0-12-ce1873ac686bb90ddec72bb99889a4e80e2de382
  LLVM version 19.0.0git
  Optimized build.
  Default target: x86_64-pc-windows-msvc
  Host CPU: alderlake

=== opt (stderr) ===


D:\gpligins\plugins>

### Operating System

Windows 10.0.19045

### CPU

12th Gen Intel(R) Core(TM) i5-12400F

### GPU

OrayIddDriver Device AMD Radeon RX 6750 GRE 12GB

### ROCm Version

ROCm 6.1.0

### ROCm Component

rocminfo

### Steps to Reproduce

After the installation is completed, I run rocminfo in the terminal and it says that this command is not found, and then the rocminfo.exe file is not found in the bin directory of the folder

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

I don't know if it's if it's an installation error, I don't have this directory
![image](https://github.com/user-attachments/assets/8ed35adf-cf21-4603-bce0-5afe978cd5cf)


### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — linghubingli (2024-11-10T20:27:51Z)

如果有回复，可以在1544192510@qq.com提醒我吗

---

### 评论 #2 — harkgill-amd (2024-11-11T15:43:24Z)

Hi @Smart-huhu, `rocminfo` is only present within Linux based installations of ROCm (Baremetal or WSL). For the Windows HIP SDK, `...\ROCm\6.1\bin\hipInfo.exe` is used as an alternative. If you have any other questions, feel free to leave a comment.

---
