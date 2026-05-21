# [Issue]: ROCm 7.11 with Strix Point (gfx1151) results in HSA_STATUS_ERROR_INVALID_CODE_OBJECT (Invalid Kernel Image) on Llama.cpp

> **Issue #6042**
> **状态**: closed
> **创建时间**: 2026-03-18T04:06:18Z
> **更新时间**: 2026-03-20T03:00:46Z
> **关闭时间**: 2026-03-20T02:14:28Z
> **作者**: odellus
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6042

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- amd-nicknick

## 描述

### Problem Description

```bash
OS:
NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"
CPU:
model name      : AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
GPU:
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151
  Marketing Name:          Radeon 8060S Graphics
      Name:                    amdgcn-amd-amdhsa--gfx1151
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
  Name:                    aie2p
  Marketing Name:          RyzenAI-npu5
```


running this on latest master of llama.cpp 
```bash
export ROCM_PATH=/opt/rocm/core-7.11
export GCC13_PATH=/usr/lib/gcc/x86_64-linux-gnu/13
cmake -S . -B build   \
  -DGGML_HIP=ON  \
  -DAMDGPU_TARGETS=gfx1151  \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_HIP_COMPILER="$ROCM_PATH/lib/llvm/bin/clang++"  \
  -DCMAKE_HIP_FLAGS="--gcc-toolchain=/usr/lib/gcc/x86_64-linux-gnu/13 -isystem /usr/include/c++/13 \
  -isystem /usr/include/x86_64-linux-gnu/c++/13 \
  -L$GCC13_PATH \
  -Wl,-rpath,$GCC13_PATH -DGGML_HIP_V6"   \
  -DCMAKE_EXE_LINKER_FLAGS="-L$GCC13_PATH"
```

results in this error
```bash
build/bin/llama-server -hf unsloth/Qwen3.5-35B-A3B-GGUF:Q4_K_M -c 180000 --host 0.0.0.0 --port 1234 --api-key lm-studio -ngl 99 -b 2048 -t 12
...
/home/thomas-wood/src/self-host/rocm/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:98: ROCm error
ROCm error: device kernel image is invalid
  current device: 0, in function ggml_cuda_op_mul_mat at /home/thomas-wood/src/self-host/rocm/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:1773
  hipGetLastError()
[New LWP 41346]
[New LWP 41345]
[New LWP 41344]
[New LWP 41343]
[New LWP 41342]
[New LWP 41341]
[New LWP 41340]
[New LWP 41339]
[New LWP 41338]
[New LWP 41337]
[New LWP 41336]
[New LWP 41335]
[New LWP 41334]
[New LWP 41333]
[New LWP 41332]
[New LWP 41331]
[New LWP 41330]
[New LWP 41329]
[New LWP 41328]
[New LWP 41327]
[New LWP 41326]
[New LWP 41325]
[New LWP 41324]
[New LWP 41323]
[New LWP 41322]
[New LWP 41321]
[New LWP 41320]
[New LWP 41319]
[New LWP 41318]
[New LWP 41317]
[New LWP 41316]
[New LWP 41315]
[New LWP 41314]
[New LWP 41311]
[New LWP 41310]

This GDB supports auto-downloading debuginfo from the following URLs:
  <https://debuginfod.ubuntu.com>
Enable debuginfod for this session? (y or [n]) [answered N; input not from terminal]
Debuginfod has been disabled.
To make this setting permanent, add 'set debuginfod enabled off' to .gdbinit.
warning: could not find '.gnu_debugaltlink' file for /lib/x86_64-linux-gnu/libnss_mdns4_minimal.so.2
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
0x00007b1d61b10813 in __GI___wait4 (pid=41353, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
warning: 30     ../sysdeps/unix/sysv/linux/wait4.c: No such file or directory
#0  0x00007b1d61b10813 in __GI___wait4 (pid=41353, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
30      in ../sysdeps/unix/sysv/linux/wait4.c
#1  0x00007b1d6268c7c3 in ggml_print_backtrace () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libggml-base.so.0
#2  0x00007b1d6268c96b in ggml_abort () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libggml-base.so.0
#3  0x00007b1d612e3412 in ggml_cuda_error(char const*, char const*, char const*, int, char const*) () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libggml-hip.so.0
#4  0x00007b1d612f518a in ggml_cuda_op_mul_mat(ggml_backend_cuda_context&, ggml_tensor const*, ggml_tensor const*, ggml_tensor*, void (*)(ggml_backend_cuda_context&, ggml_tensor const*, ggml_tensor const*, ggml_tensor*, char const*, float const*, char const*, float*, long, long, long, long, ihipStream_t*), void (*)(float const*, int const*, void*, ggml_type, long, long, long, long, long, long, long, long, ihipStream_t*)) () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libggml-hip.so.0
#5  0x00007b1d612ef6d6 in ggml_cuda_mul_mat(ggml_backend_cuda_context&, ggml_tensor const*, ggml_tensor const*, ggml_tensor*) () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libggml-hip.so.0
#6  0x00007b1d612ea9a1 in ggml_cuda_graph_evaluate_and_capture(ggml_backend_cuda_context*, ggml_cgraph*, bool, bool, void const*) () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libggml-hip.so.0
#7  0x00007b1d612e8981 in ggml_backend_cuda_graph_compute(ggml_backend*, ggml_cgraph*) () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libggml-hip.so.0
#8  0x00007b1d626a9427 in ggml_backend_sched_graph_compute_async () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libggml-base.so.0
#9  0x00007b1d622c6021 in llama_context::graph_compute(ggml_cgraph*, bool) () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libllama.so.0
#10 0x00007b1d622c8134 in llama_context::process_ubatch(llama_ubatch const&, llm_graph_type, llama_memory_context_i*, ggml_status&) () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libllama.so.0
#11 0x00007b1d622cf3e6 in llama_context::decode(llama_batch const&) () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libllama.so.0
#12 0x00007b1d622d0e7f in llama_decode () from /home/thomas-wood/src/self-host/rocm/llama.cpp/build/bin/libllama.so.0
#13 0x000063852cbfd9e2 in server_context_impl::update_slots() ()
#14 0x000063852cc4afee in server_queue::start_loop(long) ()
#15 0x000063852cb58069 in main ()
[Inferior 1 (process 41308) detached]
Aborted (core dumped)
thomas-wood@coast-after-3:~/src/self-host/rocm/llama.cpp$
```

### Operating System

Ubuntu 24.04

### CPU

AMD Ryzen AI Max+ 395

### GPU

AMD Ryzen AI Max+ 395

### ROCm Version

7.11

### ROCm Component

_No response_

### Steps to Reproduce

Follow the instructions [here](https://rocm.docs.amd.com/en/7.11.0-preview/install/rocm.html?fam=ryzen&gpu=max-395&os=ubuntu&os-version=24.04&i=pkgman#rocm-install-meta-packages) and try to build llama.cpp

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```bash
thomas-wood@coast-after-3:~/src/self-host/rocm/llama.cpp$ rocminfo --support
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.15
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      49152(0xc000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   5187
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            32
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    130498388(0x7c73f54) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    130498388(0x7c73f54) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    130498388(0x7c73f54) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    130498388(0x7c73f54) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1151
  Uuid:                    GPU-XX
  Marketing Name:          Radeon 8060S Graphics
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      2048(0x800) KB
    L3:                      32768(0x8000) KB
  Chip ID:                 5510(0x1586)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2900
  BDFID:                   50432
  Internal Node ID:        1
  Compute Unit:            40
  SIMDs per CU:            2
  Shader Engines:          2
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:       APU
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        2147483647(0x7fffffff)
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 32
  SDMA engine uCode::      14
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    128000000(0x7a12000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    128000000(0x7a12000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1151
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
    ISA 2
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
*******
Agent 3
*******
  Name:                    aie2p
  Uuid:                    AIE-XX
  Marketing Name:          RyzenAI-npu5
  Vendor Name:             AMD
  Feature:                 AGENT_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        1(0x1)
  Queue Min Size:          64(0x40)
  Queue Max Size:          64(0x40)
  Queue Type:              SINGLE
  Node:                    0
  Device Type:             DSP
  Cache Info:
    L2:                      2048(0x800) KB
    L3:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          0(0x0)
  Max Clock Freq. (MHz):   0
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            0
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:0
  Memory Properties:
  Features:                AGENT_DISPATCH
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    130498388(0x7c73f54) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65536(0x10000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    130498388(0x7c73f54) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***
thomas-wood@coast-after-3:~/src/self-host/rocm/llama.cpp$
```

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — odellus (2026-03-18T04:53:37Z)

Trying to use stable leaves me in a low power state

```bash
thomas-wood@coast-after-3:~/src/self-host/rocm/llama.cpp$ rocm-smi


WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status

========================================= ROCm System Management Interface =========================================
=================================================== Concise Info ===================================================
Device  Node  IDs              Temp    Power     Partitions          SCLK  MCLK     Fan  Perf  PwrCap  VRAM%  GPU%
              (DID,     GUID)  (Edge)  (Socket)  (Mem, Compute, ID)
====================================================================================================================
0       1     0x1586,   27490  29.0°C  18.076W   N/A, N/A, 0         N/A   1000Mhz  0%   auto  N/A     15%    0%
====================================================================================================================
=============================================== End of ROCm SMI Log ================================================
thomas-wood@coast-after-3:~/src/self-host/rocm/llama.cpp$
```

So I am trying to use 7.11 and it doesn't work. My computer turned off from a loss of power and I haven't been able to get it to work after 3 days of continuous effort. 

This is ridiculous.

---

### 评论 #2 — odellus (2026-03-18T04:56:43Z)

How long has the AMD Ryzen AI Max+ 395 been released? And I am still putting together how to do anything from a dozen contradictory documents? Why is stable broken? Why are you guys telling me to put llama.cpp in a docker image? And why are you putting llama-cli as the entrypoint? It makes ZERO SENSE

---

### 评论 #3 — odellus (2026-03-18T05:10:39Z)

here's a sample of the high quality documentation I have to resolve my plethora of issues. Here's how I'm instructed to uninstall the 7.11 preview! Looks legit! About the same quality I've come to expect from AMD after fighting with their non-existent documentation and paper thin support for a device that's over a year old
<img width="1077" height="453" alt="Image" src="https://github.com/user-attachments/assets/bec5ab4e-c5af-45c0-bcaa-02bf02694c26" />

---

### 评论 #4 — odellus (2026-03-18T05:51:02Z)

I've been sitting with gemini, chatgpt, and qwen3.5-plus for the past three days trying to figure out what's wrong. Here's what I've got so far:

I bought a brand new, top-of-the-line Ryzen AI Max+ APU, and because AMD's mainline releases (7.1.1 and 7.2) have broken kernel power management for my specific chip, they effectively brick my GPU by trapping it in a coma. Then, their preview build fixes the power issue so the hardware actually wakes up, but ships with a completely broken compiler backend for my chip's designation.

So yes, I am forced to use the preview driver to keep the hardware awake, and then lie to their own compiler to make it generate code that won't immediately crash. It is the definition of a hacked-together software stack.

When can I use my computer again?


---

### 评论 #5 — odellus (2026-03-18T05:58:35Z)

Before my power turned off 7.1.1 was working swimmingly. Building from the master branch of llama.cpp regularly. My power went out and now my computer no longer works.

---

### 评论 #6 — chejh-amd (2026-03-18T07:48:24Z)

On gfx1151 + ROCm preview, `device kernel image is invalid` is usually a mismatch between the ROCm toolchain you built with and the runtime libraries/driver that are actually loaded (e.g. leftover 7.1.x/7.2 packages, or extra HIP flags that don’t match the preview stack).

Maybe you can try:
1) Check that only one ROCm stack is installed:
   `dpkg -l | grep -Ei 'rocm|amdgpu'`
2) Rebuild llama.cpp with the simplest ROCm config (no custom HIP flags/toolchain overrides):
   `cmake -S . -B build -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1151 -DCMAKE_BUILD_TYPE=Release && cmake --build build -j`

People with similar gfx1151 setups have seen this clear up once old ROCm bits and extra flags were removed.

---

### 评论 #7 — amd-nicknick (2026-03-19T11:15:12Z)

Hi @odellus, it is likely you're compiling & linking against different ROCm libs than what's being used in runtime.
I suggest uninstalling & cleaning up everything, then use TheRock tarballs if you'd like to try out the latest ROCm stack.

List ROCm installed pkgs:
```
sudo apt list --installed | grep rocm
```

Uninstall & purge all files.
```
sudo apt autoremove --purge <pkgs listed>
```

Here's sample steps for building Llama.cpp:
1. Download & untar the latest tarball release of ROCm nightlies.
    https://rocm.nightlies.amd.com/tarball/
    In this example, I used `therock-dist-linux-gfx1151-7.13.0a20260319.tar.gz`
2. Clone Llama.cpp
    I used `b8422` tag
3. Set env variables, configure and compile
    ```
    export HIP_PATH=<Path to extracted tarball root>
    export HIPCXX=$HIP_PATH/lib/llvm/bin/clang
    cd <Llama.cpp clone directory>
    cmake -S . -B build -DGGML_HIP=ON -DGPU_TARGETS=gfx1151 -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_PREFIX_PATH=$HIP_PATH
    cmake --build build --config RelWithDebInfo -- -j 16
    ```
4. Run Llama.cpp, the LD_LIBRARY_PATH variable ensures the shared libs are sourced from the prebuilt ROCm tarball. You could also package the libs together with Llama.cpp binaries to create a portable installation.
    ```
    LD_LIBRARY_PATH=$HIP_PATH/lib ./llama.cpp/build/bin/llama-bench -m Phi-3-mini-4k-instruct-fp16.gguf
    ```

Hope this quick guidance helps. We're actively working on enhancing the system package installation experience.

A side note: the message regarding low power state from rocm-smi doesn't reflect actual system state, it is just a spurious warning and is fixed in later release where we properly implement DRM based waking.

Feel free to raise any further questions if you encounter any trouble along the way. Thanks!

---

### 评论 #8 — odellus (2026-03-20T02:14:28Z)

Thank you @amd-nicknick ! Your suggestion worked. Closing.

---
