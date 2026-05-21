# [Issue]: [ollama/ollama] Qwen3.5:9b rocBLAS error from hip error code: 'hipErrorInvalidDeviceFunction':98 ggml_cuda_compute_forward: SOLVE_TRI failed ROCm error: invalid device function

> **Issue #6120**
> **状态**: closed
> **创建时间**: 2026-04-06T02:04:24Z
> **更新时间**: 2026-04-20T14:05:27Z
> **关闭时间**: 2026-04-20T14:05:27Z
> **作者**: DaveyBonez
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6120

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

PowerShell 7.6.0
PS C:\Users\DaveyBoneZ>   (Get-WmiObject Win32_OperatingSystem).Version
10.0.26200
PS C:\Users\DaveyBoneZ>   (Get-WmiObject win32_Processor).Name
AMD Ryzen 7 5800X3D 8-Core Processor
PS C:\Users\DaveyBoneZ>   (Get-WmiObject win32_VideoController).Name
AMD Radeon RX 9060 XT
PS C:\Users\DaveyBoneZ>

### Additional details & troubleshooting already performed (RX 9060 XT - RDNA 4)

**Hardware:**  
- GPU: AMD Radeon RX 9060 XT 16 GB (RDNA 4 / gfx12xx)  
- OS: Windows 11 Pro 24H2  
- Confirmed working: **LM Studio** runs Qwen3.5 models perfectly on the exact same hardware with zero errors (using its bundled ROCm stack).

**What I already tried:**
- Fresh Ollama install (latest version)
- Multiple ROCm versions (including 6.4 and 7.1)
- Hijacked LM Studio’s entire ROCm stack (copied DLLs + set `HIP_PATH`, `PATH`, `LD_LIBRARY_PATH`, etc.) → still got the exact same `hipErrorInvalidDeviceFunction (98)`
- Confirmed the error happens during model load / rocBLAS kernel launch (`SOLVE_TRI failed`)

**AMD Support Ticket:**  
I already provided full diagnostics to AMD Global Customer Care (Ticket #3520556):
- Complete MSInfo32 (.nfo)
- DxDiag report
- Full Ollama error logs showing the hipErrorInvalidDeviceFunction(98)
- Confirmed the issue has existed since the very first attempt (never worked)

AMD has now asked me to open this GitHub issue so the ROCm team can investigate.

**Related issue:**  
This appears to be the same problem as #14423 (Radeon AI Pro R9700 — also RDNA 4).

**Reproduction steps:**
1. Install latest Ollama
2. `ollama run qwen3.5` (or any Qwen3.5 variant)
3. Immediate 500 error with `hipErrorInvalidDeviceFunction (98)` + rocBLAS failure

Smaller Qwen3 models and other families may work, but all Qwen3.5 models fail.

Happy to provide any additional logs, run specific tests, or share the full AMD diagnostics files if needed.

Thanks for looking into this — really hoping we can get RDNA 4 consumer cards working properly with Ollama + ROCm.

### Additional Context & Deep Troubleshooting (RX 9060 XT - RDNA 4)

**Critical observation that may help narrow this down:**

- **LM Studio runs Qwen3.5 models perfectly** with zero errors on this exact same RX 9060 XT hardware.
- I went **much further** and **completely hijacked LM Studio’s entire working ROCm stack**:
  - Copied all DLLs, libraries, and binaries from LM Studio’s ROCm installation
  - Overrode `HIP_PATH`, `PATH`, `LD_LIBRARY_PATH`, and every relevant environment variable to force Ollama to use LM Studio’s exact ROCm environment
- Even with LM Studio’s proven-working ROCm stack fully in control, **Ollama still immediately fails** with the exact same `hipErrorInvalidDeviceFunction (98)` + `SOLVE_TRI failed`.

This strongly suggests the problem is **not** a missing or broken ROCm install, but something specific in how **Ollama itself** builds/calls the HIP/rocBLAS kernels on RDNA 4 (gfx12xx).

**Other details already provided:**
- Issue has existed since the very first attempt (never worked)
- AMD Support Ticket #3520556 with full MSInfo32 (.nfo), DxDiag, and raw Ollama error logs
- Related issue: #14423 (same error on Radeon AI Pro R9700 — also RDNA 4)

**Reproduction:**
1. Latest Ollama
2. `ollama run qwen3.5` (any size)
3. Immediate 500 error during model load

Happy to run any specific tests, share the full AMD diagnostics files, or provide whatever else is needed.

Thanks for looking into this.

### Operating System

Windows 11

### CPU

AMD Ryzen 7 5800X3D

### GPU

AMD Radeon RX 9060 XT

### ROCm Version

7.1.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (13 条)

### 评论 #1 — tcgu-amd (2026-04-06T20:32:34Z)

Hi @DaveyBonez thanks for reaching out! Did you by chance have an iGPU active on your system that was not disabled? Can you also provide the full Ollama log up until the error (I don't have access to the support tickets)? I am happy to take a look but by the sound of it I would guess the problem is with Ollama/hardware configuration problem rather than inherently a ROCm bug. 

---

### 评论 #2 — DaveyBonez (2026-04-06T23:40:53Z)

No integrated GPU I can't give error at the moment at the hospital.

On Mon, Apr 6, 2026, 4:32 PM Tim Gu ***@***.***> wrote:

> *tcgu-amd* left a comment (ROCm/ROCm#6120)
> <https://github.com/ROCm/ROCm/issues/6120#issuecomment-4194827929>
>
> Hi @DaveyBonez <https://github.com/DaveyBonez> thanks for reaching out!
> Did you by chance have an iGPU active on your system that was not disabled?
> Can you also provide the full Ollama log up until the error (I don't have
> access to the support tickets)? I am happy to take a look but by the sound
> of it I would guess the problem is with Ollama/hardware configuration
> problem rather than inherently a ROCm bug.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/6120#issuecomment-4194827929>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AXDTDLUFSRIXIV6EPALVBSL4UQH7TAVCNFSM6AAAAACXNTVICSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHM2DCOJUHAZDOOJSHE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #3 — DaveyBonez (2026-04-06T23:49:19Z)

https://github.com/ollama/ollama/issues/15343
time=2026-03-30T13:42:49.541-04:00 level=DEBUG source=runner.go:264
msg="refreshing free memory"
time=2026-03-30T13:42:49.541-04:00 level=DEBUG source=runner.go:328
msg="unable to refresh all GPUs with existing runners, performing bootstrap
discovery"
time=2026-03-30T13:42:49.544-04:00 level=INFO source=server.go:432
msg="starting runner"
cmd="C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Ollama\\ollama.exe
runner --ollama-engine --port 56996"
time=2026-03-30T13:42:49.544-04:00 level=DEBUG source=server.go:433
msg=subprocess HIP_PATH="C:\\Program Files\\AMD\\ROCm\\6.4\\"
HIP_PATH_64="C:\\Program Files\\AMD\\ROCm\\6.4\\" HIP_PATH_71="C:\\Program
Files\\AMD\\ROCm\\7.1\\" OLLAMA_CONTEXT_LENGTH=32768 OLLAMA_DEBUG=1
OLLAMA_FLASH_ATTENTION=1 OLLAMA_HOST=0.0.0.0 OLLAMA_KV_CACHE_TYPE=q8_0
PATH="C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Ollama\\lib\\ollama;C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Ollama\\lib\\ollama\\rocm;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\WINDOWS\\System32\\OpenSSH\\;C:\\Users\\DaveyBoneZ\\AppData\\Local\\AMD\\AI_Bundle\\VSCode\\bin;C:\\Program
Files\\Git\\cmd;C:\\Program
Files\\Docker\\Docker\\resources\\bin;C:\\Program
Files\\PowerShell\\7\\;C:\\Program
Files\\AMD\\ROCm\\7.1\\bin;C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Python\\Launcher\\;C:\\Users\\DaveyBoneZ\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Users\\DaveyBoneZ\\AppData\\Local\\AMD\\AI_Bundle\\Ollama;C:\\Users\\DaveyBoneZ\\.lmstudio\\bin;C:\\Users\\DaveyBoneZ\\AppData\\Local\\Python\\bin;C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Ollama"
OLLAMA_LIBRARY_PATH=C:\Users\DaveyBoneZ\AppData\Local\Programs\Ollama\lib\ollama;C:\Users\DaveyBoneZ\AppData\Local\Programs\Ollama\lib\ollama\rocm
HIP_VISIBLE_DEVICES=0
time=2026-03-30T13:42:49.909-04:00 level=DEBUG source=runner.go:437
msg="bootstrap discovery took" duration=367.4097ms
OLLAMA_LIBRARY_PATH="[C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Ollama\\lib\\ollama
C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Ollama\\lib\\ollama\\rocm]"
extra_envs=map[HIP_VISIBLE_DEVICES:0]
time=2026-03-30T13:42:49.909-04:00 level=DEBUG source=runner.go:40
msg="overall device VRAM discovery took" duration=367.9302ms
time=2026-03-30T13:42:49.910-04:00 level=INFO source=cpu_windows.go:148
msg=packages count=1
time=2026-03-30T13:42:49.910-04:00 level=INFO source=cpu_windows.go:195
msg="" package=0 cores=8 efficiency=0 threads=16
time=2026-03-30T13:42:49.910-04:00 level=DEBUG source=sched.go:220
msg="updating default concurrency" OLLAMA_MAX_LOADED_MODELS=3 gpu_count=1
time=2026-03-30T13:42:49.910-04:00 level=DEBUG source=sched.go:229
msg="loading first model"
model=C:\Users\DaveyBoneZ\.ollama\models\blobs\sha256-dec52a44569a2a25341c4e4d3fee25846eed4f6f0b936278e3a3c900bb99d37c
time=2026-03-30T13:42:49.977-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=general.alignment default=32
time=2026-03-30T13:42:50.013-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=general.alignment default=32
time=2026-03-30T13:42:50.016-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.pooling_type default=0
time=2026-03-30T13:42:50.016-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.attention.head_count_kv default=0
time=2026-03-30T13:42:50.016-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.expert_count default=0
time=2026-03-30T13:42:50.016-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.rope.scaling.type default=""
time=2026-03-30T13:42:50.016-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.rope.type default=""
time=2026-03-30T13:42:50.016-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.rope.scaling.factor default=1
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.rope.scaling.original_context_length
default=0
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.attention.scale default=0
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.expert_count default=0
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.expert_used_count default=0
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.norm_top_k_prob default=true
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.mrope_interleaved default=false
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.vision.attention.layer_norm_epsilon
default=9.999999974752427e-07
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.vision.rope.freq_base default=10000
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.vision.num_positional_embeddings
default=2304
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=tokenizer.ggml.add_bos_token default=false
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=tokenizer.ggml.bos_token_id default=0
time=2026-03-30T13:42:50.017-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=tokenizer.ggml.eos_token_ids default="&{size:0
values:[]}"
time=2026-03-30T13:42:50.017-04:00 level=INFO source=server.go:247
msg="enabling flash attention"
time=2026-03-30T13:42:50.018-04:00 level=INFO source=server.go:432
msg="starting runner"
cmd="C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Ollama\\ollama.exe
runner --ollama-engine --model
C:\\Users\\DaveyBoneZ\\.ollama\\models\\blobs\\sha256-dec52a44569a2a25341c4e4d3fee25846eed4f6f0b936278e3a3c900bb99d37c
--port 57002"
time=2026-03-30T13:42:50.018-04:00 level=DEBUG source=server.go:433
msg=subprocess HIP_PATH="C:\\Program Files\\AMD\\ROCm\\6.4\\"
HIP_PATH_64="C:\\Program Files\\AMD\\ROCm\\6.4\\" HIP_PATH_71="C:\\Program
Files\\AMD\\ROCm\\7.1\\" OLLAMA_CONTEXT_LENGTH=32768 OLLAMA_DEBUG=1
OLLAMA_FLASH_ATTENTION=1 OLLAMA_HOST=0.0.0.0 OLLAMA_KV_CACHE_TYPE=q8_0
PATH="C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Ollama\\lib\\ollama;C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Ollama\\lib\\ollama\\rocm;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\WINDOWS\\System32\\OpenSSH\\;C:\\Users\\DaveyBoneZ\\AppData\\Local\\AMD\\AI_Bundle\\VSCode\\bin;C:\\Program
Files\\Git\\cmd;C:\\Program
Files\\Docker\\Docker\\resources\\bin;C:\\Program
Files\\PowerShell\\7\\;C:\\Program
Files\\AMD\\ROCm\\7.1\\bin;C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Python\\Launcher\\;C:\\Users\\DaveyBoneZ\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Users\\DaveyBoneZ\\AppData\\Local\\AMD\\AI_Bundle\\Ollama;C:\\Users\\DaveyBoneZ\\.lmstudio\\bin;C:\\Users\\DaveyBoneZ\\AppData\\Local\\Python\\bin;C:\\Users\\DaveyBoneZ\\AppData\\Local\\Programs\\Ollama"
OLLAMA_LIBRARY_PATH=C:\Users\DaveyBoneZ\AppData\Local\Programs\Ollama\lib\ollama;C:\Users\DaveyBoneZ\AppData\Local\Programs\Ollama\lib\ollama\rocm
HIP_VISIBLE_DEVICES=0
time=2026-03-30T13:42:50.021-04:00 level=INFO source=sched.go:484
msg="system memory" total="31.9 GiB" free="22.8 GiB" free_swap="25.3 GiB"
time=2026-03-30T13:42:50.021-04:00 level=INFO source=sched.go:491 msg="gpu
memory" id=0 library=ROCm available="14.4 GiB" free="14.8 GiB"
minimum="457.0 MiB" overhead="0 B"
time=2026-03-30T13:42:50.021-04:00 level=INFO source=server.go:759
msg="loading model" "model layers"=33 requested=-1
time=2026-03-30T13:42:50.051-04:00 level=INFO source=runner.go:1411
msg="starting ollama engine"
time=2026-03-30T13:42:50.052-04:00 level=INFO source=runner.go:1446
msg="Server listening on 127.0.0.1:57002"
time=2026-03-30T13:42:50.063-04:00 level=INFO source=runner.go:1284
msg=load request="{Operation:fit LoraPath:[] Parallel:1 BatchSize:512
FlashAttention:Enabled KvSize:32768 KvCacheType:q8_0 NumThreads:8
GPULayers:33[ID:0 Layers:33(0..32)] MultiUserCache:false ProjectorPath:
MainGPU:0 UseMmap:false}"
time=2026-03-30T13:42:50.100-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=general.alignment default=32
time=2026-03-30T13:42:50.102-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=general.name default=""
time=2026-03-30T13:42:50.102-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=general.description default=""
time=2026-03-30T13:42:50.103-04:00 level=INFO source=ggml.go:136 msg=""
architecture=qwen35 file_type=Q4_K_M name="" description="" num_tensors=883
num_key_values=52
time=2026-03-30T13:42:50.103-04:00 level=DEBUG source=ggml.go:94 msg="ggml
backend load all from path"
path=C:\Users\DaveyBoneZ\AppData\Local\Programs\Ollama\lib\ollama
load_backend: loaded CPU backend from
C:\Users\DaveyBoneZ\AppData\Local\Programs\Ollama\lib\ollama\ggml-cpu-haswell.dll
time=2026-03-30T13:42:50.116-04:00 level=DEBUG source=ggml.go:94 msg="ggml
backend load all from path"
path=C:\Users\DaveyBoneZ\AppData\Local\Programs\Ollama\lib\ollama\rocm
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon RX 9060 XT, gfx1200 (0x1200), VMM: no, Wave Size:
32, ID: 0
load_backend: loaded ROCm backend from
C:\Users\DaveyBoneZ\AppData\Local\Programs\Ollama\lib\ollama\rocm\ggml-hip.dll
time=2026-03-30T13:42:50.142-04:00 level=INFO source=ggml.go:104 msg=system
CPU.0.SSE3=1 CPU.0.SSSE3=1 CPU.0.AVX=1 CPU.0.AVX2=1 CPU.0.F16C=1
CPU.0.FMA=1 CPU.0.BMI2=1 CPU.0.LLAMAFILE=1 CPU.1.LLAMAFILE=1
ROCm.0.NO_VMM=1 ROCm.0.NO_PEER_COPY=1 ROCm.0.PEER_MAX_BATCH_SIZE=128
compiler=cgo(clang)
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.pooling_type default=0
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.attention.head_count_kv default=0
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.expert_count default=0
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.rope.scaling.type default=""
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.rope.type default=""
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.rope.scaling.factor default=1
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.rope.scaling.original_context_length
default=0
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.attention.scale default=0
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.expert_count default=0
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.expert_used_count default=0
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.norm_top_k_prob default=true
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.mrope_interleaved default=false
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.vision.attention.layer_norm_epsilon
default=9.999999974752427e-07
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.vision.rope.freq_base default=10000
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=qwen35.vision.num_positional_embeddings
default=2304
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=tokenizer.ggml.add_bos_token default=false
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=tokenizer.ggml.bos_token_id default=0
time=2026-03-30T13:42:50.146-04:00 level=DEBUG source=ggml.go:324 msg="key
with type not found" key=tokenizer.ggml.eos_token_ids default="&{size:0
values:[]}"
time=2026-03-30T13:42:50.544-04:00 level=DEBUG source=ggml.go:852
msg="compute graph" nodes=1258 splits=1
rocBLAS error from hip error code: 'hipErrorInvalidDeviceFunction':98
ggml_cuda_compute_forward: SOLVE_TRI failed
ROCm error: invalid device function
  current device: 0, in function ggml_cuda_compute_forward at
C:/a/ollama/ollama/ml/backend/ggml/ggml/src/ggml-cuda/ggml-cuda.cu:2882
  err
C:/a/ollama/ollama/ml/backend/ggml/ggml/src/ggml-cuda/ggml-cuda.cu:94: ROCm
error
time=2026-03-30T13:42:51.742-04:00 level=ERROR source=server.go:1207
msg="do load request" error="Post \"http://127.0.0.1:57002/load\": read tcp
127.0.0.1:57007->127.0.0.1:57002: wsarecv: An existing connection was
forcibly closed by the remote host."
time=2026-03-30T13:42:51.742-04:00 level=ERROR source=server.go:1207
msg="do load request" error="Post \"http://127.0.0.1:57002/load\": dial tcp
127.0.0.1:57002: connectex: No connection could be made because the target
machine actively refused it."
time=2026-03-30T13:42:51.743-04:00 level=INFO source=sched.go:511 msg="Load
failed"
model=C:\Users\DaveyBoneZ\.ollama\models\blobs\sha256-dec52a44569a2a25341c4e4d3fee25846eed4f6f0b936278e3a3c900bb99d37c
error="model failed to load, this may be due to resource limitations or an
internal error, check ollama server logs for details"
time=2026-03-30T13:42:51.743-04:00 level=DEBUG source=server.go:1832
msg="stopping llama server" pid=2444
[GIN] 2026/03/30 - 13:42:51 | 500 |    2.3317189s |       127.0.0.1 | POST
   "/api/chat"
time=2026-03-30T13:42:51.764-04:00 level=ERROR source=server.go:304
msg="llama runner terminated" error="exit status 1"
[GIN] 2026/03/30 - 13:43:19 | 200 |      1.5188ms |       127.0.0.1 | GET
    "/api/tags"
[GIN] 2026/03/30 - 13:43:50 | 200 |       505.2µs |       127.0.0.1 | GET
    "/api/tags"

On Mon, Apr 6, 2026, 7:40 PM David Potts ***@***.***> wrote:

> No integrated GPU I can't give error at the moment at the hospital.
>
> On Mon, Apr 6, 2026, 4:32 PM Tim Gu ***@***.***> wrote:
>
>> *tcgu-amd* left a comment (ROCm/ROCm#6120)
>> <https://github.com/ROCm/ROCm/issues/6120#issuecomment-4194827929>
>>
>> Hi @DaveyBonez <https://github.com/DaveyBonez> thanks for reaching out!
>> Did you by chance have an iGPU active on your system that was not disabled?
>> Can you also provide the full Ollama log up until the error (I don't have
>> access to the support tickets)? I am happy to take a look but by the sound
>> of it I would guess the problem is with Ollama/hardware configuration
>> problem rather than inherently a ROCm bug.
>>
>> —
>> Reply to this email directly, view it on GitHub
>> <https://github.com/ROCm/ROCm/issues/6120#issuecomment-4194827929>, or
>> unsubscribe
>> <https://github.com/notifications/unsubscribe-auth/AXDTDLUFSRIXIV6EPALVBSL4UQH7TAVCNFSM6AAAAACXNTVICSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHM2DCOJUHAZDOOJSHE>
>> .
>> You are receiving this because you were mentioned.Message ID:
>> ***@***.***>
>>
>


---

### 评论 #4 — tcgu-amd (2026-04-08T17:19:35Z)

Hi @DaveyBonez, thanks for reaching out! This is quite strange because `hipErrorInvalidDeviceFunction` typically means a library mismatch somewhere within the hip runtime. In this case, since it happens during SOLVE, the mismatch is likely between rocblas.dll and amdhip64.dll. In other words, this is an environment configuration problem. I would suggest uninstalling Ollama and both ROCm 7.1 and ROCm 6.4 on your system, clear your ENV variables, then reinstalling Ollama from their official site. If the issue still persists following these steps. then likely something is wrong on the Ollama side, and I would recommend opening a ticket there. 

In any case, based on the logs this is unlikely an issue with ROCm itself. I will be closing this issue for now, but please feel free to follow up with additional questions. Or if after fixing the library mismatch problem you discover new error messages that indicate something is indeed problematic in ROCm, we can reopen the ticket I will be happy to take another look. 

Thanks! 

---

### 评论 #5 — DaveyBonez (2026-04-09T16:39:59Z)

@tcgu-amd 

With all due respect, this is **not** an environment or library mismatch.

**Facts already provided + concrete proof from both applications + latest test:**

- Ollama works perfectly with **all other models** — the error is **specific to Qwen3.5** models only.
- **LM Studio** runs Qwen3.5 models with zero errors and **ComfyUI and Amuse** have zero errors on this exact same RX 9060 XT using the identical ROCm stack.
- I **hijacked LM Studio’s entire working ROCm stack** (DLLs + every environment variable) and forced Ollama to use it — still got the exact same `hipErrorInvalidDeviceFunction (98)` + `SOLVE_TRI failed`.
- I performed a **completely fresh Windows 11 reinstall** and the issue persisted from the very first Ollama install.
- **Even when I inject the environment paths** (`HIP_PATH`, `PATH`, `LD_LIBRARY_PATH`, etc.) to point directly at the full ROCm 7.1 / LM Studio ROCm folders, **Ollama detects the newer ROCm** but **still fails** with the exact same error.

**Smoking gun — bundled rocBLAS libraries compared:**

**Ollama’s own rocBLAS library** only contains kernels for gfx1030 / gfx1100–gfx1151 / gfx906.  
**No** gfx1200 or gfx1201 files at all.

**LM Studio’s rocBLAS library** contains full `Kernels.so-000-gfx1200.hsaco` + `gfx1201.hsaco` + all matching TensileLibrary files.

Even when Ollama is explicitly told to use the correct newer ROCm/HIP libraries via environment variables, it still fails on RDNA 4 for Qwen3.5.

This is clearly a compatibility issue in **Ollama’s ROCm backend / rocBLAS kernel handling** with RDNA 4 (gfx12xx).

Please **reopen this issue**. I am happy to provide any additional logs, run any targeted tests, or share the exact environment injection commands I used.

Thank you.

---

### 评论 #6 — DaveyBonez (2026-04-09T17:04:14Z)

Either Ollama is not properly using the gfx12xx kernels provided by the ROCm drivers **or** there is an issue with the ROCm stack provided by AMD for RDNA 4. (LM Studio doesn’t even need AMD’s stack because it ships its own.)

Happy to run any tests, provide raw logs, or share any additional info.

Thank you.

---

### 评论 #7 — tcgu-amd (2026-04-09T17:26:10Z)

Hi @DaveyBonez thanks for the clarifications.  As you said, `Ollama’s own rocBLAS library only contains kernels for gfx1030 / gfx1100–gfx1151 / gfx906. No gfx1200 or gfx1201 files at all.`, which suggests that `hipErrorInvalidDeviceFunction` is triggered due to missing modules. In other words, Ollama was not built with gfx12 support on Windows. I checked out Ollama docs https://docs.ollama.com/gpu#windows-support, and it does indeed seem to suggest that Ollama on windows is still stuck on ROCm 6.1 and does not suport gfx12. In anycase, it seems to be more appropriate to raise this on the Ollama side. 

---

### 评论 #8 — DaveyBonez (2026-04-09T17:45:07Z)

@tcgu-amd

Thank you for the follow-up and for confirming the missing
gfx1200/gfx1201 kernels.

I agree this ultimately needs to be fixed on the **Ollama side**
(their Windows build is shipping an outdated rocBLAS that doesn’t
include RDNA 4 support).

However, since the Ollama team has already reopened my issue (#15343)
and is now actively looking at it, could you please keep this ROCm
issue open as well? It serves as clear evidence that the official ROCm
stack (and LM Studio’s vendor build) **does** contain the gfx12xx
kernels — the problem is only that Ollama is not using them on
Windows.

Cross-reference:
- Ollama issue (reopened): https://github.com/ollama/ollama/issues/15343
- Original similar report: https://github.com/ollama/ollama/issues/14423

Happy to provide any additional information the Ollama team needs to
update their Windows ROCm packaging.

Thanks again!


On Thu, Apr 9, 2026 at 1:26 PM Tim Gu ***@***.***> wrote:

> *tcgu-amd* left a comment (ROCm/ROCm#6120)
> <https://github.com/ROCm/ROCm/issues/6120#issuecomment-4216175584>
>
> Hi @DaveyBonez <https://github.com/DaveyBonez> thanks for the
> clarifications. As you said, Ollama’s own rocBLAS library only contains
> kernels for gfx1030 / gfx1100–gfx1151 / gfx906. No gfx1200 or gfx1201 files
> at all., which suggests that hipErrorInvalidDeviceFunction is triggered
> due to missing modules. In other words, Ollama was not built with Windows
> support. I checked out Ollama docs
> https://docs.ollama.com/gpu#windows-support, and it does indeed seem to
> suggest that Ollama on windows is still stuck on ROCm 6.1 and is not suport
> gfx12. In anycase, it seems to be more appropriate to raise this on the
> Ollama side.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/6120#issuecomment-4216175584>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AXDTDLUECI4KYDHZOW25IED4U7MMPAVCNFSM6AAAAACXNTVICSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHM2DEMJWGE3TKNJYGQ>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #9 — e-strelock (2026-04-09T18:42:48Z)

It doesn't seem that this issue has any relation to gfx12xx or is specific to Ollama on Windows.

Here (https://github.com/ggml-org/llama.cpp/issues/19442) the exact same problem (ggml_cuda_compute_forward: SOLVE_TRI failed) with llama.cpp is described, occurring on an AMD Radeon Instinct Mi50 (gfx906 under Linux), which is supported regardless.

---

### 评论 #10 — tcgu-amd (2026-04-09T19:00:41Z)

> Here ([ggml-org/llama.cpp#19442](https://github.com/ggml-org/llama.cpp/issues/19442)) the exact same problem (ggml_cuda_compute_forward: SOLVE_TRI failed) with llama.cpp is described, occurring on an AMD Radeon Instinct Mi50 (gfx906 under Linux), which is supported regardless.

Hi @e-strelock, I am actually not sure on that. Can you link me to a documentation where it says gfx906 is supported? Afaik even on TheRock nightly we only have a tentative build for 906 that is far from release-ready. 


---

### 评论 #11 — e-strelock (2026-04-09T19:35:49Z)


Hi @tcgu-amd .

> Hi [@e-strelock](https://github.com/e-strelock), I am actually not sure on that. Can you link me to a documentation where it says gfx906 is supported? Afaik even on TheRock nightly we only have a tentative build for 906 that is far from release-ready.

I assume you know better than I do which hardware is supported by ROCm and which isn’t. I’m simply pointing out that your assumption that the only cause of the error is just a missing relevant module in Ollama itself may not be the case, as noted above:

> Ollama’s own rocBLAS library only contains kernels for gfx1030 / gfx1100–gfx1151 / gfx906.

That said, I do see that the ROCm library files bundled with Ollama differ from those shipped with HIP SDK 7.1.1, which is installed on my machine and which I’m using in place of Ollama’s own versions. Am I correct in understanding that the issue presumably lies not in an incorrect implementation of the kernels required for SOLVE_TRI in HIP SDK 7.1.1, but rather in the current version of Ollama simply being unable to properly utilize them? I’m highly surprised that the issue is isolated to SOLVE_TRI and doesn’t manifest in any other cases, but I suppose anything is possible.


---

### 评论 #12 — DaveyBonez (2026-04-09T21:34:28Z)

@e-strelock I would use LM Studio till Ollama gets their stuff right LM Studio has the gfx906 built into their backend.
PS C:\Users\DaveyBoneZ\.lmstudio\extensions\backends\vendor\win-llama-rocm-vendor-v5\bin\rocblas\library> ls

    Directory: C:\Users\DaveyBoneZ\.lmstudio\extensions\backends\vendor\win-llama-rocm-vendor-v5\bin\rocblas\library

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---           7/22/2025  6:46 PM         247864 Kernels.so-000-gfx1030.hsaco
-a---           7/22/2025  6:46 PM         260928 Kernels.so-000-gfx1100.hsaco
-a---           7/22/2025  6:46 PM         261184 Kernels.so-000-gfx1101.hsaco
-a---           7/22/2025  6:46 PM         260928 Kernels.so-000-gfx1102.hsaco
-a---           7/22/2025  6:46 PM         259136 Kernels.so-000-gfx1150.hsaco
-a---           7/22/2025  6:46 PM         259136 Kernels.so-000-gfx1151.hsaco
-a---           7/22/2025  6:46 PM         273736 Kernels.so-000-gfx1200.hsaco
-a---           7/22/2025  6:46 PM         273736 Kernels.so-000-gfx1201.hsaco
-a---           7/22/2025  6:46 PM         243256 Kernels.so-000-gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          23026 TensileLibrary_lazy_gfx1030.dat
-a---           7/22/2025  6:46 PM          24186 TensileLibrary_lazy_gfx1100.dat
-a---           7/22/2025  6:46 PM          24186 TensileLibrary_lazy_gfx1101.dat
-a---           7/22/2025  6:46 PM          24186 TensileLibrary_lazy_gfx1102.dat
-a---           7/22/2025  6:46 PM          24186 TensileLibrary_lazy_gfx1150.dat
-a---           7/22/2025  6:46 PM          17653 TensileLibrary_lazy_gfx1151.dat
-a---           7/22/2025  6:46 PM          17653 TensileLibrary_lazy_gfx1200.dat
-a---           7/22/2025  6:46 PM          17653 TensileLibrary_lazy_gfx1201.dat
-a---           7/22/2025  6:46 PM          31798 TensileLibrary_lazy_gfx906.dat
-a---           7/22/2025  6:46 PM         163184 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         172152 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         171896 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         173176 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         173176 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         171896 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         181120 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         181120 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         158064 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          43864 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM          86880 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM         687592 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         127866 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         135432 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         143120 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         143120 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         143888 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         143376 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         142352 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         151576 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         151576 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         131080 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          37530 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM          27576 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM        1936520 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         251655 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         162672 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         171128 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         171128 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         172664 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         171896 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         170872 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         181632 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         181632 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         157808 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          44208 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM          89232 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM        1058448 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         165470 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         134664 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         142352 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         142352 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         142864 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         142864 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         142352 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         151576 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         151576 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         131592 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          37698 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         110848 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM        1320792 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         206603 TensileLibrary_Type_4xi8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         503016 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         534000 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         534000 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         534256 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         530928 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         530160 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         574712 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         574712 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         490472 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          56571 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM       16798720 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         553773 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM       17275968 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         587914 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM       11487656 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         245804 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM       11487656 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         245804 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         446136 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         478912 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         478912 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         480448 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         474304 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         472768 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         505288 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         505288 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         436920 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          53587 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM       16199424 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         650515 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM        6410688 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         311687 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM        8035680 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         216528 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM        8035680 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         216528 TensileLibrary_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         190824 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         200560 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         200560 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         201840 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         201072 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         199536 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         207224 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         207224 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         189288 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          39842 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM       15259064 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         594996 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM       12111472 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         481545 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM       13516648 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         319948 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM       13516648 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         319948 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         439480 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         476096 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         475584 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         476864 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         471488 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         470976 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         504776 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         504776 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         431800 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          53714 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM       11708648 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         580906 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM        6025104 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         385767 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM        4275648 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         146261 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM        4275648 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         146261 TensileLibrary_Type_BB_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         475360 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         497896 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         497896 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         497640 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         496872 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         496872 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         537840 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         537840 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         464608 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          54776 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         242744 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         253760 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         253760 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         255040 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         254016 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         252992 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         268616 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         268616 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         239672 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          32244 TensileLibrary_Type_BS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM          81840 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          84920 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          84920 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          86200 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          85176 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          84408 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          88000 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          88000 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          79792 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          17206 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         198088 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         206288 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         206288 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         207312 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         206544 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         205776 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         219352 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         219352 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         194504 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          28527 TensileLibrary_Type_BS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM          44480 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          46536 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          46536 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          46536 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          46536 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          46536 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          47568 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          47568 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          43456 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7346 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         457144 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM          31078 TensileLibrary_Type_CC_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          44488 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          46544 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          46544 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          46544 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          46288 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          46288 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          47576 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          47576 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          43464 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7358 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM          53720 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM           4054 TensileLibrary_Type_CC_Contraction_l_Ailk_BjlkC_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          44224 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          46536 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          46536 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          46536 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          46280 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          46280 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          47568 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          47568 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          43456 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7362 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         352456 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM          25508 TensileLibrary_Type_CC_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          44224 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          46536 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          46536 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          46536 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          46280 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          46280 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          47568 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          47568 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          43456 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7362 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         381464 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM          27365 TensileLibrary_Type_CC_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          44232 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          46544 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          46544 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          47312 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          46544 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          46544 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          47576 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          47576 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          43464 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7374 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM          53336 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM           4054 TensileLibrary_Type_CC_Contraction_l_Alik_BjlkC_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          43968 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          45768 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          45768 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          46280 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          45512 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          45512 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          46800 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          46800 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          42432 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7362 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         427824 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM          27371 TensileLibrary_Type_CC_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          44232 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          46544 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          46544 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          47056 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          46544 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          46288 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          47576 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          47576 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          43464 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7374 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM          53336 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM           4054 TensileLibrary_Type_CC_Contraction_l_AlikC_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          46544 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          48344 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          48344 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          48344 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          48344 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          48344 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          49632 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          49632 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          45520 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7386 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM          59864 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM           4060 TensileLibrary_Type_CC_Contraction_l_AlikC_BjlkC_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          43976 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          46032 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          46032 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          46288 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          46032 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          45520 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          46808 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          46808 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          42440 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7374 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM          52944 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM           4054 TensileLibrary_Type_CC_Contraction_l_AlikC_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          20096 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          20872 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          20872 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          20872 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          20872 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          20872 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          21392 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          21392 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          19840 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7154 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        5990032 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM        1944642 TensileLibrary_Type_DD_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          33696 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          34984 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          34984 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          34984 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          34984 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          34984 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          36784 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          36784 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          32928 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           8877 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        6759672 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM        1592220 TensileLibrary_Type_DD_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          20096 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          20616 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          20616 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          20616 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          20616 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          20616 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          21392 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          21392 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          19584 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7170 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         431376 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM          39655 TensileLibrary_Type_DD_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          19584 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          20616 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          20616 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          20616 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          20616 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          20616 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          20880 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          20880 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          19328 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7170 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         654864 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM          50646 TensileLibrary_Type_DD_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         184672 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         198248 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         198248 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         198504 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         194920 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         194920 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         207728 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         207728 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         182112 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          27904 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        5667272 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM         322852 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       12455104 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         522001 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM       16953184 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         631291 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM        9981152 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         259531 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM        9981152 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         259531 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM        1865800 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         318666 TensileLibrary_Type_HH_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          88840 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          95760 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          95760 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          96016 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          94224 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          94480 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         101144 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         101144 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          86792 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          21156 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM       10899144 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM         611314 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       10171928 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         573213 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM        5949272 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         338732 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM        9584240 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         325225 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM        9584240 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         325225 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM        2224080 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         234582 TensileLibrary_Type_HH_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         103184 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         110872 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         111128 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         110872 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         109080 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         109592 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         116768 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         116768 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         101648 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          21160 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        5846304 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM         349268 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       10478584 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         511734 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM       11279448 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         508961 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM        7762232 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         241790 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM        7762232 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         241790 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM        1292048 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         149918 TensileLibrary_Type_HH_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          88072 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          95248 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          95248 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          95248 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          93456 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          93456 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         100120 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         100120 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          85512 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          21156 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        8806072 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM         436598 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM        7843008 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         530465 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM        4909640 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         378783 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM        3627192 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         165827 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM        3627192 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         165827 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM        1541456 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         262237 TensileLibrary_Type_HH_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         404032 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         422216 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         422216 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         423496 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         420936 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         420168 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         455760 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         455760 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         390976 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          75064 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        9250576 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM         628517 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       13129224 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         544835 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM       14238976 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         527504 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM        4892728 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         140368 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM        4892728 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         140368 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM          56024 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM        3464752 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         322022 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         197248 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         207752 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         207752 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         209032 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         207240 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         205960 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         218256 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         218256 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         190848 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          52814 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM       13249024 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM        1167877 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       10984512 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         567287 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM        5834072 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         332190 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM       12036640 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         394906 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM       12036640 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         394906 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM          47536 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM        5248008 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         471150 TensileLibrary_Type_HH_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         108840 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         113456 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         113456 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         113456 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         112944 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         113200 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         116792 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         116792 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         106280 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          46000 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        1538264 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM         144630 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       11004072 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         541818 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM        9958528 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         477292 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM        8283400 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         253357 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM        8283400 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         253357 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         120720 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM         421792 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM          55262 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         163888 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         172344 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         172344 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         173624 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         171832 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         170552 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         181568 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         181568 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         159536 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          46024 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM       11981520 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM        1067430 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM        8804808 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         567927 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM        4893352 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         379587 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM        5387472 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         228034 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM        5387472 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         228034 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         483848 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM        4086720 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         439215 TensileLibrary_Type_HH_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         365832 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         379152 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         379152 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         379664 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         378896 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         377872 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         412696 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         412696 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         356360 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          46978 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         978120 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM         864088 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         251511 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         203216 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         211672 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         211672 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         212696 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         212184 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         210904 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         222944 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         222944 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         199888 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          28301 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         700568 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM        1035992 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         243597 TensileLibrary_Type_HS_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         102664 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         106768 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         106768 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         107024 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         106256 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         106000 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         110360 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         110360 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         100360 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          20669 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         870904 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM         748112 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         225064 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         239160 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         248896 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         248896 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         249920 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         249408 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         248128 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         263240 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         263240 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         233016 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          32006 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         765368 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM         625232 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         214830 TensileLibrary_Type_HS_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         478104 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         525216 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         525216 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         525216 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         522912 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         522912 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         550056 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         550056 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         470424 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          71204 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        3254024 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM         321264 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       22255776 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         684883 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM       15519904 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         576175 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM       17097936 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         330068 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM       17097936 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         330068 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         326440 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         357168 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         357168 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         356912 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         356400 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         356656 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         375352 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         375352 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         320040 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          57304 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        2191152 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM         198753 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       17182264 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         704398 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM        7241184 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         416663 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM       15757960 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         400235 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM       15757960 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         400235 TensileLibrary_Type_I8I_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         452400 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         499000 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         498744 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         497976 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         496952 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         497976 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         526656 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         526656 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         442672 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          68073 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        2486472 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM         236651 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       16680720 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         638820 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM        5576904 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         339816 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM       14922016 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         378313 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM       14922016 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         378313 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         402432 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM         441608 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM         441352 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM         442632 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM         441608 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM         440584 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM         468752 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM         468752 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM         393472 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM          66274 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        2302592 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM         236531 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       10926616 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         716443 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM        3804808 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM         390494 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM        7114992 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM         320431 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM        7114992 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM         320431 TensileLibrary_Type_I8I_HPA_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM          52616 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          58256 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          58256 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          58256 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          56720 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          56720 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          61592 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          61592 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          49800 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7174 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM       15770520 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM        1271499 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       15770520 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM        1271499 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM          28064 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM           2031 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM          13312 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM           2022 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM          13312 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM           2022 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         358016 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM       13071136 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM        2221564 TensileLibrary_Type_SS_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          34696 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          37520 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          37520 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          37776 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          37008 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          36752 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          39576 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          39576 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          33416 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7170 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM       16283648 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM        1456397 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       16283648 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM        1456397 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM          28072 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM           2032 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM          13320 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM           2022 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM          13320 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM           2022 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         520360 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM       19996744 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM        3399321 TensileLibrary_Type_SS_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          34184 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          37008 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          37008 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          37008 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          36496 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          36496 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          39064 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          39064 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          32904 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7174 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM        8104600 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM         567372 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM        8104600 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM         567372 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM          28072 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM           2031 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM          13320 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM           2022 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM          13320 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM           2022 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         236936 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM        1989144 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM         494531 TensileLibrary_Type_SS_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          43400 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          46736 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          46736 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          46992 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          45712 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          45712 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          48792 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          48792 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          41864 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7174 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM       17987464 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1030.co
-a---           7/22/2025  6:46 PM        1431428 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1030.dat
-a---           7/22/2025  6:46 PM       17987464 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1100.co
-a---           7/22/2025  6:46 PM        1431428 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1100.dat
-a---           7/22/2025  6:46 PM          28080 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1101.co
-a---           7/22/2025  6:46 PM           2032 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1101.dat
-a---           7/22/2025  6:46 PM          13328 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1102.co
-a---           7/22/2025  6:46 PM           2022 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1102.dat
-a---           7/22/2025  6:46 PM          13328 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1150.co
-a---           7/22/2025  6:46 PM           2022 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx1150.dat
-a---           7/22/2025  6:46 PM         385456 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM       23023680 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM        3239703 TensileLibrary_Type_SS_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          48320 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          51664 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          51664 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          47552 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7386 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         640896 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM          66511 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          48328 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          51672 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          51672 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          47560 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7390 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         128840 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM           7944 TensileLibrary_Type_ZZ_Contraction_l_Ailk_BjlkC_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          48320 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          51664 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          51664 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          47552 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7394 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         574256 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM          43130 TensileLibrary_Type_ZZ_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          48320 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          50376 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          51664 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          51664 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          47552 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7394 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         277672 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM          20140 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          48328 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          51672 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          51672 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          47560 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7406 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         128848 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM           7944 TensileLibrary_Type_ZZ_Contraction_l_Alik_BjlkC_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          48064 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          50120 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          50120 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          50120 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          50120 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          50120 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          51152 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          51152 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          47040 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7394 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         391336 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM          23868 TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          48328 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          50384 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          51672 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          51672 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          47560 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7406 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         128848 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM           7944 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bjlk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          48336 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          50392 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          50392 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          50392 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          50392 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          50392 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          51680 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          51680 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          47568 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7418 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         128864 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM           7956 TensileLibrary_Type_ZZ_Contraction_l_AlikC_BjlkC_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM          48072 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1030.hsaco
-a---           7/22/2025  6:46 PM          50128 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1100.hsaco
-a---           7/22/2025  6:46 PM          50128 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1101.hsaco
-a---           7/22/2025  6:46 PM          50128 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1102.hsaco
-a---           7/22/2025  6:46 PM          50128 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1150.hsaco
-a---           7/22/2025  6:46 PM          50128 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1151.hsaco
-a---           7/22/2025  6:46 PM          51160 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1200.hsaco
-a---           7/22/2025  6:46 PM          51160 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx1201.hsaco
-a---           7/22/2025  6:46 PM          47048 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback_gfx906-xnack-.hsaco
-a---           7/22/2025  6:46 PM           7406 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_fallback.dat
-a---           7/22/2025  6:46 PM         128856 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_gfx906.co
-a---           7/22/2025  6:46 PM           7944 TensileLibrary_Type_ZZ_Contraction_l_AlikC_Bljk_Cijk_Dijk_gfx906.dat
-a---           7/22/2025  6:46 PM         118224 TensileManifest.txt

PS C:\Users\DaveyBoneZ\.lmstudio\extensions\backends\vendor\win-llama-rocm-vendor-v5\bin\rocblas\library>

---

### 评论 #13 — tcgu-amd (2026-04-20T14:05:27Z)

Hi I will be closing this issue. Please reach out to Ollama's side for proper issue resolution. Thanks. 

---
