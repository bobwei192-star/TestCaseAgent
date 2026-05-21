# [Issue]: HIP error: invalid argument when running an example code from the vllm repo

> **Issue #3246**
> **状态**: closed
> **创建时间**: 2024-06-05T16:10:58Z
> **更新时间**: 2024-10-15T13:33:29Z
> **关闭时间**: 2024-07-24T17:17:41Z
> **作者**: gopikrishnan92
> **标签**: Under Investigation, ROCm 6.0.0, AMD Instinct MI210
> **URL**: https://github.com/ROCm/ROCm/issues/3246

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Instinct MI210** (颜色: #ededed)

## 描述

### Problem Description

I'm trying to get started vllm on ROCM. I built and ran the docker image by following the instructions on this page https://docs.vllm.ai/en/latest/getting_started/amd-installation.html# 

I tried running the following code provided in the examples 

from vllm import LLM, SamplingParams


# Sample prompts.
prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]
# Create a sampling params object.
#sampling_params = SamplingParams(temperature=0.8, top_p=0.95)


sampling_params = SamplingParams(max_tokens=128,
    skip_special_tokens=True,
    temperature=0.8,
    top_k=20,
    top_p=0.95,)

# Create an LLM.
llm = LLM(model="facebook/opt-125m")
#llm = LLM(model="mistralai/Mistral-7B-Instruct-v0.3")
# Generate texts from the prompts. The output is a list of RequestOutput objects
# that contain the prompt, generated text, and other information.
outputs = llm.generate(prompts, sampling_params)
# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")


and got the following error

 python offline_inference.py
/opt/conda/envs/py_3.9/lib/python3.9/site-packages/huggingface_hub/file_download.py:1132: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
INFO 06-05 15:52:17 llm_engine.py:81] Initializing an LLM engine (v0.4.0.post1) with config: model='facebook/opt-125m', speculative_config=None, tokenizer='facebook/opt-125m', tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.float16, max_seq_len=2048, download_dir=None, load_format=auto, tensor_parallel_size=1, disable_custom_all_reduce=True, quantization=None, enforce_eager=False, kv_cache_dtype=auto, quantization_param_path=None, device_config=cuda, seed=0)
INFO 06-05 15:52:17 pynccl.py:59] Loading nccl from library librccl.so.1
INFO 06-05 15:52:19 selector.py:35] Using ROCmFlashAttention backend.
Traceback (most recent call last):
  File "/vllm/examples/offline_inference.py", line 25, in <module>
    llm = LLM(model="facebook/opt-125m")
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/vllm/entrypoints/llm.py", line 112, in __init__
    self.llm_engine = LLMEngine.from_engine_args(
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/vllm/engine/llm_engine.py", line 234, in from_engine_args
    engine = cls(
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/vllm/engine/llm_engine.py", line 119, in __init__
    self.model_executor = executor_class(
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/vllm/executor/gpu_executor.py", line 41, in __init__
    self._init_worker()
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/vllm/executor/gpu_executor.py", line 66, in _init_worker
    self.driver_worker.init_device()
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/vllm/worker/worker.py", line 97, in init_device
    self.init_gpu_memory = torch.cuda.mem_get_info()[0]
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/cuda/memory.py", line 663, in mem_get_info
    return torch.cuda.cudart().cudaMemGetInfo(device)
RuntimeError: HIP error: invalid argument
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing HIP_LAUNCH_BLOCKING=1.
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.



### Operating System

"Ubuntu 22.04.3 LTS

### CPU

AMD EPYC 9554 64-Core Processor

### GPU

AMD Instinct MI210

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          NO

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD EPYC 9554 64-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 9554 64-Core Processor
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
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   3100
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            128
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    528082608(0x1f79e6b0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    528082608(0x1f79e6b0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    528082608(0x1f79e6b0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    AMD EPYC 9554 64-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 9554 64-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   3100
  BDFID:                   0
  Internal Node ID:        1
  Compute Unit:            128
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    528393356(0x1f7ea48c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    528393356(0x1f7ea48c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    528393356(0x1f7ea48c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 3
*******
  Name:                    gfx90a
  Uuid:                    GPU-209951be100ce86a
  Marketing Name:          AMD Instinct MI210
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    2
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      8192(0x2000) KB
  Chip ID:                 29711(0x740f)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1700
  BDFID:                   18432
  Internal Node ID:        2
  Compute Unit:            104
  SIMDs per CU:            4
  Shader Engines:          8
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          64(0x40)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    2048(0x800)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 55
  SDMA engine uCode::      8
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*******
Agent 4
*******
  Name:                    gfx90a
  Uuid:                    GPU-2c0c6a9ce4219723
  Marketing Name:          AMD Instinct MI210
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    3
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      8192(0x2000) KB
  Chip ID:                 29711(0x740f)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1700
  BDFID:                   19200
  Internal Node ID:        3
  Compute Unit:            104
  SIMDs per CU:            4
  Shader Engines:          8
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          64(0x40)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    2048(0x800)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 55
  SDMA engine uCode::      8
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*******
Agent 5
*******
  Name:                    gfx90a
  Uuid:                    GPU-28245c4c823f5e8d
  Marketing Name:          AMD Instinct MI210
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    4
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      8192(0x2000) KB
  Chip ID:                 29711(0x740f)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1700
  BDFID:                   2048
  Internal Node ID:        4
  Compute Unit:            104
  SIMDs per CU:            4
  Shader Engines:          8
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          64(0x40)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    2048(0x800)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 55
  SDMA engine uCode::      8
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*******
Agent 6
*******
  Name:                    gfx90a
  Uuid:                    GPU-b34d8a37a141e632
  Marketing Name:          AMD Instinct MI210
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    5
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      8192(0x2000) KB
  Chip ID:                 29711(0x740f)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1700
  BDFID:                   2816
  Internal Node ID:        5
  Compute Unit:            104
  SIMDs per CU:            4
  Shader Engines:          8
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          64(0x40)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    2048(0x800)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 55
  SDMA engine uCode::      8
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***


### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — gopikrishnan92 (2024-06-05T19:03:11Z)

When I ran the code with AMD_LOG_LEVEL =3 I got the following info
:3:hip_device.cpp           :475 : 1131970506621 us: [pid:1318  tid:0x7fe57f9fc4c0] hipGetDevicePropertiesR0600: Returned hipSuccess :
INFO 06-05 18:45:36 selector.py:35] Using ROCmFlashAttention backend.
:3:hip_device_runtime.cpp   :623 : 1131970533591 us: [pid:1318  tid:0x7fe57f9fc4c0]  hipGetDevice ( 0x7ffeace89094 )
:3:hip_device_runtime.cpp   :631 : 1131970533604 us: [pid:1318  tid:0x7fe57f9fc4c0] hipGetDevice: Returned hipSuccess :
:3:hip_device_runtime.cpp   :623 : 1131970533653 us: [pid:1318  tid:0x7fe57f9fc4c0]  hipGetDevice ( 0x7ffeace88f04 )
:3:hip_device_runtime.cpp   :631 : 1131970533658 us: [pid:1318  tid:0x7fe57f9fc4c0] hipGetDevice: Returned hipSuccess :
:3:hip_device_runtime.cpp   :623 : 1131970533677 us: [pid:1318  tid:0x7fe57f9fc4c0]  hipGetDevice ( 0x7ffeace88d10 )
:3:hip_device_runtime.cpp   :631 : 1131970533680 us: [pid:1318  tid:0x7fe57f9fc4c0] hipGetDevice: Returned hipSuccess :
:3:hip_memory.cpp           :777 : 1131970533694 us: [pid:1318  tid:0x7fe57f9fc4c0]  hipMemGetInfo ( 0x7ffeace88ce8, 0x7ffeace88cf0 )
:1:rocdevice.cpp            :1885: 1131970533709 us: [pid:1318  tid:0x7fe57f9fc4c0] HSA_AMD_AGENT_INFO_MEMORY_AVAIL query failed.
:3:hip_memory.cpp           :790 : 1131970533713 us: [pid:1318  tid:0x7fe57f9fc4c0] hipMemGetInfo: Returned hipErrorInvalidValue :
:3:hip_error.cpp            :36  : 1131970533715 us: [pid:1318  tid:0x7fe57f9fc4c0]  hipGetLastError (  )
:3:hip_device_runtime.cpp   :653 : 1131970534242 us: [pid:1318  tid:0x7fe57f9fc4c0]  hipSetDevice ( 0 )
:3:hip_device_runtime.cpp   :657 : 1131970534248 us: [pid:1318  tid:0x7fe57f9fc4c0] hipSetDevice: Returned hipSuccess :
Traceback (most recent call last):


---

### 评论 #2 — ppanchad-amd (2024-06-24T15:39:15Z)

@gopikrishnan92 Can you please check if you see still see the issue with the latest ROCm 6.1.2? Thanks!

---

### 评论 #3 — kyujin-cho (2024-07-02T08:29:47Z)

@ppanchad-amd Can confirm same issue stands on our side with ROCm 6.1.2 installed. Using MI250 with Ubuntu 22.04.

---

### 评论 #4 — ppanchad-amd (2024-07-02T14:55:58Z)

@gopikrishnan92 @kyujin-cho Internal ticket is created to fix this issue. Thanks!

---

### 评论 #5 — jamesxu2 (2024-07-11T14:36:05Z)

Hi @gopikrishnan92 , I've run some tests on an MI210 system as well as on an RX7900XT and am not able to reproduce the hipMemGetInfo failure you're experiencing. 

![image](https://github.com/ROCm/ROCm/assets/172289477/e5ee3078-0f24-47b2-900c-8ce0a4531407)

However, it is possible that this issue can appear when your host system's AMDGPU driver (i.e. outside your container) is not installed correctly, or is outdated. This driver is installed alongside ROCm but may be outdated on your side and this issue may be fixed by doing a clean uninstall and reinstall of a recent ROCm. Can you provide the following:

1. The output of ```sudo apt info rocm-libs```, executed from your linux host (to get your ROCm version)
2. The output of ```sudo dkms status```, executed from your linux host (to get your AMDGPU kernel driver version)
3. More details on how you installed ROCm on your Linux host sytem?

Also, please wrap code and logs in triple backticks (```) so it's more legible. Github markdown is changing your python comment "#"s into large-text titles! 


---

### 评论 #6 — jamesxu2 (2024-07-23T13:39:48Z)

Hello @gopikrishnan92, do you have any updates? 

---

### 评论 #7 — gopikr92 (2024-07-24T14:55:19Z)

@jamesxu2   yes the problem is resolved now. I repeated all the steps and it started working fine. I’m not sure what went wrong in the first place

---

### 评论 #8 — Buliqioqiolibusdo (2024-10-13T16:50:23Z)

@jamesxu2 I have a problem:
# torch.cuda.mem_get_info runtime error: hip error: invalid argument
sudo apt info rocm-libs
```
Package: rocm-libs
Version: 6.2.2.60202-116~22.04
Priority: optional
Section: devel
Maintainer: ROCm Dev Support <rocm-dev.support@amd.com>
Installed-Size: 13.3 kB
Depends: hipblas (= 2.2.0.60202-116~22.04), hipblaslt (= 0.8.0.60202-116~22.04), hipfft (= 1.0.15.60202-116~22.04), hipsolver (= 2.2.0.60202-116~22.04), hipsparse (= 3.1.1.60202-116~22.04), hiptensor (= 1.3.0.60202-116~22.04), miopen-hip (= 3.2.0.60202-116~22.04), half (= 1.12.0.60202-116~22.04), rccl (= 2.20.5.60202-116~22.04), rocalution (= 3.2.0.60202-116~22.04), rocblas (= 4.2.1.60202-116~22.04), rocfft (= 1.0.29.60202-116~22.04), rocrand (= 3.1.0.60202-116~22.04), hiprand (= 2.11.0.60202-116~22.04), rocsolver (= 3.26.0.60202-116~22.04), rocsparse (= 3.2.0.60202-116~22.04), rocm-core (= 6.2.2.60202-116~22.04), hipsparselt (= 0.2.1.60202-116~22.04), composablekernel-dev (= 1.1.0.60202-116~22.04), hipblas-dev (= 2.2.0.60202-116~22.04), hipblaslt-dev (= 0.8.0.60202-116~22.04), hipcub-dev (= 3.2.0.60202-116~22.04), hipfft-dev (= 1.0.15.60202-116~22.04), hipsolver-dev (= 2.2.0.60202-116~22.04), hipsparse-dev (= 3.1.1.60202-116~22.04), hiptensor-dev (= 1.3.0.60202-116~22.04), miopen-hip-dev (= 3.2.0.60202-116~22.04), rccl-dev (= 2.20.5.60202-116~22.04), rocalution-dev (= 3.2.0.60202-116~22.04), rocblas-dev (= 4.2.1.60202-116~22.04), rocfft-dev (= 1.0.29.60202-116~22.04), rocprim-dev (= 3.2.0.60202-116~22.04), rocrand-dev (= 3.1.0.60202-116~22.04), hiprand-dev (= 2.11.0.60202-116~22.04), rocsolver-dev (= 3.26.0.60202-116~22.04), rocsparse-dev (= 3.2.0.60202-116~22.04), rocthrust-dev (= 3.1.0.60202-116~22.04), rocwmma-dev (= 1.5.0.60202-116~22.04), hipsparselt-dev (= 0.2.1.60202-116~22.04)
Homepage: https://github.com/RadeonOpenCompute/ROCm
Download-Size: 1,062 B
APT-Manual-Installed: yes
APT-Sources: https://repo.radeon.com/rocm/apt/6.2.2 jammy/main amd64 Packages
Description: Radeon Open Compute (ROCm) Runtime software stack
```
sudo apt show amdgpu-dkms
```
Package: amdgpu-dkms
Version: 1:6.8.5.60202-2041575.22.04
Priority: optional
Section: misc
Maintainer: Advanced Micro Devices (AMD) <gpudriverdevsupport@amd.com>
Installed-Size: 513 MB
Provides: rock-dkms
Depends: dkms (>= 1.95), libc-dev | libc6-dev, autoconf, automake, initramfs-tools, amdgpu-dkms-firmware (= 1:6.8.5.60202-2041575.22.04)
Conflicts: rock-dkms (<< 1:6.8.5.60202-2041575.22.04)
Breaks: rock-dkms (<< 1:6.8.5.60202-2041575.22.04)
Replaces: rock-dkms (<< 1:6.8.5.60202-2041575.22.04)
Download-Size: 11.5 MB
APT-Sources: https://repo.radeon.com/amdgpu/6.2.2/ubuntu jammy/main amd64 Packages
Description: amdgpu driver in DKMS format
```

pip show torch
```
Name: torch
Version: 2.6.0.dev20240918+rocm6.2
Summary: Tensors and Dynamic neural networks in Python with strong GPU acceleration
Home-page: https://pytorch.org/
Author: PyTorch Team
Author-email: packages@pytorch.org
License: BSD-3-Clause
Location: /home/eacloud/miniconda3/envs/vllm6_env/lib/python3.10/site-packages
Requires: filelock, fsspec, jinja2, networkx, pytorch-triton-rocm, sympy, typing-extensions
Required-by: accelerate, flash_attn, peft, tensorizer
```
lsb_release -a
```
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.5 LTS
Release:        22.04
Codename:       jammy
```

```
Python 3.10.15 (main, Oct  3 2024, 07:27:34) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> torch.cuda.get_device_name()
'AMD Instinct MI210'
>>> torch.cuda.current_device()
0
>>> torch.cuda.get_device_capability()
(9, 0)
>>> torch.cuda.device_count()
4
>>> torch.cuda.mem_get_info()[0]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/eacloud/miniconda3/envs/vllm6_env/lib/python3.10/site-packages/torch/cuda/memory.py", line 712, in mem_get_info
    return torch.cuda.cudart().cudaMemGetInfo(device)
RuntimeError: HIP error: invalid argument
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

I would appreciate your reply!

---

### 评论 #9 — jamesxu2 (2024-10-15T13:33:28Z)

Hi @Buliqioqiolibusdo , 

Next time, please open a new ticket instead of adding on to an existing one. 

Are you running this example on a baremetal system or inside a container like the original reporter of this ticket? If you are running inside a container, do you have ROCm installed on the host system (eg. outside the container)?

---
