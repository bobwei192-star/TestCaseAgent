# [Issue]: MIOpen missing headers for JIT compilation on Windows 11 + RX 7900 XTX + driver 26.1.1

> **Issue #5941**
> **状态**: open
> **创建时间**: 2026-02-07T01:47:35Z
> **更新时间**: 2026-03-04T19:23:10Z
> **作者**: mgersonde
> **标签**: Windows, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5941

## 标签

- **Windows** (颜色: #c2e0c6)
- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

# AMD ROCm Windows Bug Report

**For submission to:** [github.com/ROCm/ROCm/issues](https://github.com/ROCm/ROCm/issues)

---

## Title
`torch.cuda.is_available()` causes access violation crash on Windows 11 with RX 7900 XTX and driver 26.1.1

## Environment

| Component | Version |
|-----------|---------|
| **GPU** | AMD Radeon RX 7900 XTX (24GB VRAM) |
| **OS** | Windows 11 |
| **Driver** | AMD Adrenalin Edition 26.1.1 |
| **Python** | 3.12.12 (Anaconda) |
| **PyTorch** | 2.9.1+rocmsdk20260116 |
| **HIP Version** | 7.2.26024-f6f897bd3d |
| **ROCm SDK** | 7.2.0.dev0 (pip wheels from repo.radeon.com) |

## Description

Calling `torch.cuda.is_available()` causes a hard crash with "Windows fatal exception: access violation" in the HIP runtime. This occurs despite:
- Driver 26.1.1 installed correctly (confirmed in Adrenalin GUI)
- HIP DLLs loading successfully
- PyTorch importing correctly
- `torch.version.hip` reporting correct version

## Steps to Reproduce

1. Install AMD Adrenalin Edition 26.1.1
2. Create Python 3.12 environment
3. Install ROCm SDK and PyTorch from repo.radeon.com:
```bash
pip install --no-cache-dir \
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_core-7.2.0.dev0-py3-none-win_amd64.whl \
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm-7.2.0.dev0.tar.gz \
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torch-2.9.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl
```
4. Run:
```python
import torch
print(torch.__version__)  # Works: 2.9.1+rocmsdk20260116
print(torch.version.hip)  # Works: 7.2.26024-f6f897bd3d
print(torch.cuda.is_available())  # CRASH
```

## Expected Behavior

`torch.cuda.is_available()` should return `True` and GPU should be accessible.

## Actual Behavior

Process crashes with:
```
Windows fatal exception: access violation

Current thread 0x00004d48 (most recent call first):
  File "...\torch\cuda\__init__.py", line 182 in is_available
```

## Additional Notes

- AMD's AI Bundle (installed via Adrenalin's "AI Bundle" option) includes Amuse with HIP 6.0.4 DLLs, while the pip wheels install HIP 7.2. This version mismatch may contribute to the issue.
- The crash occurs with both:
  - Conda environment with pip-installed ROCm
  - System Python 3.12 installed by AMD's AI Bundle
- HIP DLLs (`amdhip64_7.dll`) load successfully via ctypes before the crash
- Environment variables set: `HIP_PATH`, `ROCM_HOME`, `HSA_ENABLE_SDMA=0`

## System Specs

- CPU: AMD Ryzen 9 9900X (12-Core)
- RAM: 32 GB
- GPU: AMD Radeon RX 7900 XTX + AMD Radeon(TM) Graphics (integrated)


### Operating System

Windows 11

### CPU

AMD Ryzen 9 9900X 12-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 7.2.0.dev0 (HIP 7.2.26024-f6f897bd3d)

### ROCm Component

_No response_

### Steps to Reproduce

ROCm Component:   HIP Runtime (amdhip64_7.dll), PyTorch Windows wheels


1. Install AMD Adrenalin Edition 26.1.1
2. Create Python 3.12 environment
3. pip install PyTorch from repo.radeon.com/rocm/windows/rocm-rel-7.2/
4. Run: import torch; torch.cuda.is_available()
5. Observe crash: "Windows fatal exception: access violation"


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (21 条)

### 评论 #1 — Pimpmuckl (2026-02-08T21:10:56Z)

Ran into the same issue, ended up copying the `amdhip64_7.dll `from System32 into `.\.venv\Lib\site-packages\_rocm_sdk_core\bin` and that resolved the `torch.cuda.is_available()` crash.

File Versions are mismatched, it seems. The installed one in the venv is `10.0.3581.0`, the Sys32 dll is `10.0.3665.0`.

I haven't tested for accuracy though. So wouldn't recommend this without proper testing.

Full error printout, in case that helps:

```(rocm-torch-playground) PS C:\Code\rocm-torch-playground> python -X faulthandler -c "import torch; print(torch.__version__); print(torch.version.hip); print(torch.cuda.device_count())"
2.9.1+rocmsdk20260116
7.2.26024-f6f897bd3d
Windows fatal exception: access violation

Current thread 0x00005a4c (most recent call first):
  File "C:\Code\rocm-torch-playground\.venv\Lib\site-packages\torch\cuda\__init__.py", line 1034 in device_count
  File "<string>", line 1 in <module>
(rocm-torch-playground) PS C:\Code\rocm-torch-playground> Get-WinEvent -FilterHashtable @{LogName='Application'; Id=1000} |
>>   Where-Object { $_.Message -match 'python\.exe' } |
>>   Select-Object -First 1 |
>>   Format-List TimeCreated, Message

TimeCreated : 08/02/2026 22:00:43
Message     : Faulting application name: python.exe, version: 3.12.11150.1013, time stamp: 0x68962e82
              Faulting module name: amdhip64_7.dll, version: 10.0.3581.0, time stamp: 0x69695bad
              Exception code: 0xc0000005
              Fault offset: 0x00000000004c7fe1
              Faulting process id: 0x7420
              Faulting application start time: 0x1DC993DFC185EBA
              Faulting application path:
              C:\Users\jonat\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\python.exe
              Faulting module path:
              C:\Code\rocm-torch-playground\.venv\Lib\site-packages\_rocm_sdk_core\bin\amdhip64_7.dll
              Report Id: 03c4221e-1cac-4042-a381-ba628b4007c1
              Faulting package full name:
              Faulting package-relative application ID:```

---

### 评论 #2 — mgersonde (2026-02-10T18:58:09Z)

Thanks for your input JJ.

Here is my report the attempt to implement the fix for AMD to follow up on:

# [Bug Report] ROCm on Windows: MIOpen JIT Compilation Fails due to Missing SDK Headers (RX 7900 XTX)
**GPU:** AMD Radeon RX 7900 XTX (gfx1100)
**OS:** Windows 11 Pro
**Software:** ROCm 6.2 / PyTorch 2.9.1+rocmsdk20260116 (Nightly)
## Summary
While `torch.cuda.is_available()` can be successfully enabled on Windows by resolving a DLL version mismatch, actual training fails due to **Release Engineering gaps** in the Windows distribution. specifically, the lack of C++ development headers required for MIOpen's runtime kernel compilation (JIT).
## 1. The DLL Mismatch (Solved)
**Issue:** The `amdhip64_7.dll` bundled with PyTorch (via pip, ~14MB) does not match the system driver installed by AMD Adrenalin (~18MB), causing a hard crash (`Access Violation 0xc0000005`) during initialization.
**Crash Log (Before Fix):**
```
Faulting application name: python.exe
Faulting module name: amdhip64_7.dll
Exception code: 0xc0000005 (Access Violation)
Faulting module path: ...\site-packages\_rocm_sdk_core\bin\amdhip64_7.dll
```
**Fix:** Copying `C:\Windows\System32\amdhip64_7.dll` to `venv\Lib\site-packages\_rocm_sdk_core\bin\` resolves initialization.
> **Note:** Thanks to the community member who identified this DLL version mismatch. This workaround successfully enables GPU visibility.
**Result:** 
- GPU detected: `AMD Radeon RX 7900 XTX`
- Basic tensor operations: **Pass**
## 2. The Blocker: Missing Headers for JIT Compilation
**Issue:** MIOpen attempts to compile kernels at runtime (e.g., Dropout, Reductions) but fails because standard C++ and ROCm headers are missing from the Windows environment.
**Error Log:**
```
MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram' ... HIPRTC_ERROR_COMPILATION (6)
fatal error: 'rocrand/rocrand_xorwow.h' file not found
fatal error: 'type_traits' file not found
```
**Root Cause Analysis:**
The Windows driver installer (Pro/Adrenalin) provides **Runtime Binaries Only**. Unlike the Linux `rocm-hip-sdk` package, there is no mechanism to install the development headers (`include/*`) required by `hiprtc`.
- Verified: `C:\Program Files\AMD` contains **zero** SDK headers.
- Verified: `pip install torch` does not bundle the full ROCm SDK headers.
## 3. Requirements for Resolution
To make Windows a viable platform for custom model training, AMD must:
1.  **Bundle SDK Headers:** Include the full `include/` directory (containing `rocrand`, `hip`, `miopen`, and standard C++ traits) in the Windows driver installer or a separate "ROCm SDK for Windows" installer.
2.  **Synchronize DLLs:** Ensure PyTorch binaries link against a stable ABI or bundle a compatible driver DLL, eliminating the need for manual file copying.
**Impact:** Without these headers, Windows support is limited to pre-compiled kernels only (inference), making research/training impossible.

---

### 评论 #3 — huanrwan-amd (2026-02-17T15:00:44Z)

Hi @mgersonde, thanks for posting. Reading through the post, you had solved DLL mismatch issue.  
For the Missing Headers issue, did you test with ROCm7.2? thanks.

---

### 评论 #4 — mgersonde (2026-02-18T18:46:03Z)

Yes, We did try  ROCm7.2

Thanks Wang. Here is the following report for your reference

Environment
Component Version
*GPU* AMD Radeon RX 7900 XTX (24GB VRAM)
*OS* Windows 11
*Driver* AMD Adrenalin Edition 26.1.1
*Python* 3.12.12 (Anaconda)
*PyTorch* 2.9.1+rocmsdk20260116
*HIP Version* 7.2.26024-f6f897bd3d
*ROCm SDK* 7.2.0.dev0 (pip wheels from repo.radeon.com) Description

Calling torch.cuda.is_available() causes a hard crash with "Windows fatal
exception: access violation" in the HIP runtime. This occurs despite:

   - Driver 26.1.1 installed correctly (confirmed in Adrenalin GUI)
   - HIP DLLs loading successfully
   - PyTorch importing correctly
   - torch.version.hip reporting correct version



On Tue, Feb 17, 2026 at 7:01 AM Huanran Wang ***@***.***>
wrote:

> *huanrwan-amd* left a comment (ROCm/ROCm#5941)
> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3915226859>
>
> Hi @mgersonde <https://github.com/mgersonde>, thanks for posting. Reading
> through the post, you had solved DLL mismatch issue.
> For the Missing Headers issue, did you test with ROCm7.2? thanks.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3915226859>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AJ74GPH6FMAFWLXQUH766UT4MMULHAVCNFSM6AAAAACUJNBDRSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTSMJVGIZDMOBVHE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #5 — mgersonde (2026-02-19T02:32:11Z)

 quick update: we identified instability caused by mixed HIP DLL resolution
(HIP 6.x/7.x) on PATH. We implemented a hardened Windows launch policy:
enforce conda rocm_env execution + sanitize PATH to exclude
AI_Bundle|Amuse|HIP\6|ROCm\6, then run a capability probe before starting
the app/worker. Under this policy, ROCm PyTorch initializes cleanly (
torch.version.hip present) and torch.cuda.is_available() returns True
without the prior access violation; trivial GPU tensor ops also pass. Next
step is validating end-to-end app workload actually runs on GPU (we
currently still have CPU-only enforcement in the worker path), and we’ll
follow up with effective_device proof + workload timing once complete.

Addendum: we now have an operator-override run where the worker reports
device_policy=gpu_auto and selected_device=cuda (with conda_env=rocm_env)
in the /status proof, so the app’s GPU execution path is reachable and runs
successfully. In an initial paired run, end-to-end runtime improved only
~5%, which suggests the pipeline is still dominated by CPU-side
preprocessing/I/O rather than GPU-bound training. Next we’re instrumenting
a breakdown of time spent in data fetch/AFML transforms vs model training,
and will share a GPU utilization/profile capture if you have recommended
tooling for ROCm-on-Windows PyTorch.

On Wed, Feb 18, 2026 at 10:45 AM Michael Gersonde ***@***.***>
wrote:

> Yes, We didtry  ROCm7.2
>
> Thanks Wang. Here is the following report for your reference
>
> Environment
> Component Version
> *GPU* AMD Radeon RX 7900 XTX (24GB VRAM)
> *OS* Windows 11
> *Driver* AMD Adrenalin Edition 26.1.1
> *Python* 3.12.12 (Anaconda)
> *PyTorch* 2.9.1+rocmsdk20260116
> *HIP Version* 7.2.26024-f6f897bd3d
> *ROCm SDK* 7.2.0.dev0 (pip wheels from repo.radeon.com) Description
>
> Calling torch.cuda.is_available() causes a hard crash with "Windows fatal
> exception: access violation" in the HIP runtime. This occurs despite:
>
>    - Driver 26.1.1 installed correctly (confirmed in Adrenalin GUI)
>    - HIP DLLs loading successfully
>    - PyTorch importing correctly
>    - torch.version.hip reporting correct version
>
>
>
> On Tue, Feb 17, 2026 at 7:01 AM Huanran Wang ***@***.***>
> wrote:
>
>> *huanrwan-amd* left a comment (ROCm/ROCm#5941)
>> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3915226859>
>>
>> Hi @mgersonde <https://github.com/mgersonde>, thanks for posting.
>> Reading through the post, you had solved DLL mismatch issue.
>> For the Missing Headers issue, did you test with ROCm7.2? thanks.
>>
>> —
>> Reply to this email directly, view it on GitHub
>> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3915226859>, or
>> unsubscribe
>> <https://github.com/notifications/unsubscribe-auth/AJ74GPH6FMAFWLXQUH766UT4MMULHAVCNFSM6AAAAACUJNBDRSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTSMJVGIZDMOBVHE>
>> .
>> You are receiving this because you were mentioned.Message ID:
>> ***@***.***>
>>
>


---

### 评论 #6 — mgersonde (2026-02-20T05:03:08Z)

Subject: ROCm PyTorch training: GPU selected, but LSTM train stage slower
than CPU (evidence attached)


Quick update with evidence from our WIN_MODE test harness (Windows 11)
after hardening environment gating:

*Environment / build*

   -

   Conda env strictly gated to rocm_env (wrapper enforced; base execution
   refused).
   -

   PyTorch: 2.9.1+rocmsdk20260116
   -

   HIP: 7.2.26024-f6f897bd3d
   -

   Probe reports cuda_is_available=true (ROCm backend).

*GPU selection proof*

   -

   When we set AUTOQUANT_DEVICE_POLICY=gpu_auto, /status reports:
   -

      conda_env=rocm_env
      -

      device_policy=gpu_auto
      -

      selected_device=cuda
      -

   We also now surface “device truth” telemetry from the trainer (model
   param device / first batch device / effective training device) through
   /status and the results payload.

*Performance finding (current)*

   -

   Paired benchmark (10 CPU vs 10 GPU_AUTO) on the same workflow shows *no
   statistically meaningful speedup* overall.
   -

   After fixing stage timing capture, we can attribute time: the *dominant
   stage is training*, and training is *slower on GPU_AUTO* for our current
   model/data shape (train stage ≈82s GPU_AUTO vs ≈68s CPU in the captured
   benchmark).
   -

   CI across paired deltas crosses zero, but the stage attribution
   consistently points to training as the driver of slower GPU_AUTO runs.

*Request*

   1.

   Are there known slow paths for LSTM/RNN training on ROCm in this torch
   ROCm build (2.9.1+rocmsdk20260116) under Windows?
   2.

   Do you have recommended “minimum performant” shapes (batch size, seq
   length, hidden size) where ROCm should decisively beat CPU for LSTM?
   3.

   Any recommended flags/settings for ROCm PyTorch to avoid
   fallback/inefficient kernels for RNN/LSTM?

*Next evidence in progress*
We are running a training-only microbenchmark sweep (warmup discarded +
batch-size sweep) to isolate pure training throughput from orchestration
overhead. I will send those isolated results next.

Thanks,
Michael


On Tue, Feb 17, 2026 at 7:01 AM Huanran Wang ***@***.***>
wrote:

> *huanrwan-amd* left a comment (ROCm/ROCm#5941)
> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3915226859>
>
> Hi @mgersonde <https://github.com/mgersonde>, thanks for posting. Reading
> through the post, you had solved DLL mismatch issue.
> For the Missing Headers issue, did you test with ROCm7.2? thanks.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3915226859>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AJ74GPH6FMAFWLXQUH766UT4MMULHAVCNFSM6AAAAACUJNBDRSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTSMJVGIZDMOBVHE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #7 — mgersonde (2026-02-20T08:11:37Z)

Subject: Update: training-only microbenchmark shows gpu_auto falls back to
CPU (effective trainer device = CPU)


Follow-up with isolated training evidence.

We implemented and ran a *training-only CPU vs GPU_AUTO microbenchmark*
under WIN_MODE with the rocm wrapper enforced.

*Benchmark design*

   -

   Warmup: 1 run discarded
   -

   Measured: 5 runs
   -

   Batch sizes: 32 / 64 / 128
   -

   Evidence captured to: test_output/training_only_benchmark.json
   (untracked) and summary doc: docs/TRAINING_ONLY_BENCHMARK.md

*Key result*

   -

   In this training-only benchmark, *GPU_AUTO reported the trainer’s
   effective device as CPU*, even though the system previously showed
   selected_device=cuda in /status under GPU_AUTO.
   -

   CPU was faster across tested batch sizes (GPU-minus-CPU wall-time deltas
   were positive), consistent with the trainer not actually executing on GPU.

*Interpretation*
This looks like a *silent fallback/mismatch*: device selection path
indicates “cuda” (ROCm), but the training execution path/device-truth
indicates CPU. That suggests either:

   -

   an intentional WIN_MODE safety fallback in our trainer path (we can
   point you to the code locations), or
   -

   an unsupported/slow kernel path triggering CPU fallback, or
   -

   a device-routing mismatch between model/device selection and the
   training loop.

*Question*
What specific ROCm/PyTorch debug flags/logs would you like captured to
identify why the trainer executes on CPU under GPU_AUTO (e.g., op fallback
reporting, hip/miopen diagnostics, torch logging categories)?

Thanks,
Michael


On Thu, Feb 19, 2026 at 9:02 PM Michael Gersonde ***@***.***>
wrote:

> Subject: ROCm PyTorch training: GPU selected, but LSTM train stage slower
> than CPU (evidence attached)
>
>
> Quick update with evidence from our WIN_MODE test harness (Windows 11)
> after hardening environment gating:
>
> *Environment / build*
>
>    -
>
>    Conda env strictly gated to rocm_env (wrapper enforced; base execution
>    refused).
>    -
>
>    PyTorch: 2.9.1+rocmsdk20260116
>    -
>
>    HIP: 7.2.26024-f6f897bd3d
>    -
>
>    Probe reports cuda_is_available=true (ROCm backend).
>
> *GPU selection proof*
>
>    -
>
>    When we set AUTOQUANT_DEVICE_POLICY=gpu_auto, /status reports:
>    -
>
>       conda_env=rocm_env
>       -
>
>       device_policy=gpu_auto
>       -
>
>       selected_device=cuda
>       -
>
>    We also now surface “device truth” telemetry from the trainer (model
>    param device / first batch device / effective training device) through
>    /status and the results payload.
>
> *Performance finding (current)*
>
>    -
>
>    Paired benchmark (10 CPU vs 10 GPU_AUTO) on the same workflow shows *no
>    statistically meaningful speedup* overall.
>    -
>
>    After fixing stage timing capture, we can attribute time: the *dominant
>    stage is training*, and training is *slower on GPU_AUTO* for our
>    current model/data shape (train stage ≈82s GPU_AUTO vs ≈68s CPU in the
>    captured benchmark).
>    -
>
>    CI across paired deltas crosses zero, but the stage attribution
>    consistently points to training as the driver of slower GPU_AUTO runs.
>
> *Request*
>
>    1.
>
>    Are there known slow paths for LSTM/RNN training on ROCm in this torch
>    ROCm build (2.9.1+rocmsdk20260116) under Windows?
>    2.
>
>    Do you have recommended “minimum performant” shapes (batch size, seq
>    length, hidden size) where ROCm should decisively beat CPU for LSTM?
>    3.
>
>    Any recommended flags/settings for ROCm PyTorch to avoid
>    fallback/inefficient kernels for RNN/LSTM?
>
> *Next evidence in progress*
> We are running a training-only microbenchmark sweep (warmup discarded +
> batch-size sweep) to isolate pure training throughput from orchestration
> overhead. I will send those isolated results next.
>
> Thanks,
> Michael
>
>
> On Tue, Feb 17, 2026 at 7:01 AM Huanran Wang ***@***.***>
> wrote:
>
>> *huanrwan-amd* left a comment (ROCm/ROCm#5941)
>> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3915226859>
>>
>> Hi @mgersonde <https://github.com/mgersonde>, thanks for posting.
>> Reading through the post, you had solved DLL mismatch issue.
>> For the Missing Headers issue, did you test with ROCm7.2? thanks.
>>
>> —
>> Reply to this email directly, view it on GitHub
>> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3915226859>, or
>> unsubscribe
>> <https://github.com/notifications/unsubscribe-auth/AJ74GPH6FMAFWLXQUH766UT4MMULHAVCNFSM6AAAAACUJNBDRSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTSMJVGIZDMOBVHE>
>> .
>> You are receiving this because you were mentioned.Message ID:
>> ***@***.***>
>>
>


---

### 评论 #8 — huanrwan-amd (2026-02-20T17:08:08Z)

Hi @mgersonde, have you fixed the miopen JIT compilation issue on your env? For performance issue, there are discussion on https://github.com/ROCm/TheRock/issues/2591 . 
BTW, seems you are using AI generated auto reply?

---

### 评论 #9 — mgersonde (2026-02-21T18:30:02Z)

 Hi Huanran

Yes.  The report was compiled w/ GPT 5.3-Codex High

 — update: we ran the TheRock#2591-style heavy capture and now have a clear
JIT failure + fallback.

*Log bundle:* test_output/amd_logs/20260221T175250Z/

   -

   miopen_output_logs.txt
   -

   hipblaslt_log.txt / hipblaslt_sorted.txt
   -

   env_truth.txt
   -

   README_AMD.md

*Key failure signature (HIPRTC / MIOpen):*

   -

   HIPRTC_ERROR_COMPILATION (6)
   -

   type_traits file not found
   -

   followed by miopenStatusUnknownError and *CPU fallback*
   (see miopen_output_logs.txt lines 8–20)

*Device truth (same run):*

   -

   selected_device: cuda
   -

   training_device_effective: cpu
   -

   first_batch_device: cpu

*hipBLASLt shapes logged (sorted, all available lines):*

   -

   m=256,n=1,k=256 (solution_index 1214)
   -

   m=256,n=256,k=1 (solution_index 1214)
   -

   m=1,n=256,k=256 (solution_index 1214)

*Question:* what is the recommended fix on Windows ROCm for HIPRTC failing
due to missing C++ standard headers (type_traits not found)? Is there a
known include-path/toolchain requirement, or a way to disable/avoid HIPRTC
JIT for MIOpen/hipBLASLt in this configuration?

Thanks,
Michael


On Fri, Feb 20, 2026 at 12:10 AM Michael Gersonde ***@***.***>
wrote:

> Subject: Update: training-only microbenchmark shows gpu_auto falls back to
> CPU (effective trainer device = CPU)
>
>
> Follow-up with isolated training evidence.
>
> We implemented and ran a *training-only CPU vs GPU_AUTO microbenchmark*
> under WIN_MODE with the rocm wrapper enforced.
>
> *Benchmark design*
>
>    -
>
>    Warmup: 1 run discarded
>    -
>
>    Measured: 5 runs
>    -
>
>    Batch sizes: 32 / 64 / 128
>    -
>
>    Evidence captured to: test_output/training_only_benchmark.json
>    (untracked) and summary doc: docs/TRAINING_ONLY_BENCHMARK.md
>
> *Key result*
>
>    -
>
>    In this training-only benchmark, *GPU_AUTO reported the trainer’s
>    effective device as CPU*, even though the system previously showed
>    selected_device=cuda in /status under GPU_AUTO.
>    -
>
>    CPU was faster across tested batch sizes (GPU-minus-CPU wall-time
>    deltas were positive), consistent with the trainer not actually executing
>    on GPU.
>
> *Interpretation*
> This looks like a *silent fallback/mismatch*: device selection path
> indicates “cuda” (ROCm), but the training execution path/device-truth
> indicates CPU. That suggests either:
>
>    -
>
>    an intentional WIN_MODE safety fallback in our trainer path (we can
>    point you to the code locations), or
>    -
>
>    an unsupported/slow kernel path triggering CPU fallback, or
>    -
>
>    a device-routing mismatch between model/device selection and the
>    training loop.
>
> *Question*
> What specific ROCm/PyTorch debug flags/logs would you like captured to
> identify why the trainer executes on CPU under GPU_AUTO (e.g., op fallback
> reporting, hip/miopen diagnostics, torch logging categories)?
>
> Thanks,
> Michael
>
>
> On Thu, Feb 19, 2026 at 9:02 PM Michael Gersonde ***@***.***>
> wrote:
>
>> Subject: ROCm PyTorch training: GPU selected, but LSTM train stage slower
>> than CPU (evidence attached)
>>
>>
>> Quick update with evidence from our WIN_MODE test harness (Windows 11)
>> after hardening environment gating:
>>
>> *Environment / build*
>>
>>    -
>>
>>    Conda env strictly gated to rocm_env (wrapper enforced; base
>>    execution refused).
>>    -
>>
>>    PyTorch: 2.9.1+rocmsdk20260116
>>    -
>>
>>    HIP: 7.2.26024-f6f897bd3d
>>    -
>>
>>    Probe reports cuda_is_available=true (ROCm backend).
>>
>> *GPU selection proof*
>>
>>    -
>>
>>    When we set AUTOQUANT_DEVICE_POLICY=gpu_auto, /status reports:
>>    -
>>
>>       conda_env=rocm_env
>>       -
>>
>>       device_policy=gpu_auto
>>       -
>>
>>       selected_device=cuda
>>       -
>>
>>    We also now surface “device truth” telemetry from the trainer (model
>>    param device / first batch device / effective training device) through
>>    /status and the results payload.
>>
>> *Performance finding (current)*
>>
>>    -
>>
>>    Paired benchmark (10 CPU vs 10 GPU_AUTO) on the same workflow shows *no
>>    statistically meaningful speedup* overall.
>>    -
>>
>>    After fixing stage timing capture, we can attribute time: the *dominant
>>    stage is training*, and training is *slower on GPU_AUTO* for our
>>    current model/data shape (train stage ≈82s GPU_AUTO vs ≈68s CPU in the
>>    captured benchmark).
>>    -
>>
>>    CI across paired deltas crosses zero, but the stage attribution
>>    consistently points to training as the driver of slower GPU_AUTO runs.
>>
>> *Request*
>>
>>    1.
>>
>>    Are there known slow paths for LSTM/RNN training on ROCm in this
>>    torch ROCm build (2.9.1+rocmsdk20260116) under Windows?
>>    2.
>>
>>    Do you have recommended “minimum performant” shapes (batch size, seq
>>    length, hidden size) where ROCm should decisively beat CPU for LSTM?
>>    3.
>>
>>    Any recommended flags/settings for ROCm PyTorch to avoid
>>    fallback/inefficient kernels for RNN/LSTM?
>>
>> *Next evidence in progress*
>> We are running a training-only microbenchmark sweep (warmup discarded +
>> batch-size sweep) to isolate pure training throughput from orchestration
>> overhead. I will send those isolated results next.
>>
>> Thanks,
>> Michael
>>
>>
>> On Tue, Feb 17, 2026 at 7:01 AM Huanran Wang ***@***.***>
>> wrote:
>>
>>> *huanrwan-amd* left a comment (ROCm/ROCm#5941)
>>> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3915226859>
>>>
>>> Hi @mgersonde <https://github.com/mgersonde>, thanks for posting.
>>> Reading through the post, you had solved DLL mismatch issue.
>>> For the Missing Headers issue, did you test with ROCm7.2? thanks.
>>>
>>> —
>>> Reply to this email directly, view it on GitHub
>>> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3915226859>, or
>>> unsubscribe
>>> <https://github.com/notifications/unsubscribe-auth/AJ74GPH6FMAFWLXQUH766UT4MMULHAVCNFSM6AAAAACUJNBDRSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTSMJVGIZDMOBVHE>
>>> .
>>> You are receiving this because you were mentioned.Message ID:
>>> ***@***.***>
>>>
>>


---

### 评论 #10 — huanrwan-amd (2026-02-24T16:31:35Z)

Hi @mgersonde , can you post the logs and all your ROCm path? Thanks.

---

### 评论 #11 — mgersonde (2026-02-24T18:27:47Z)

------------------------------
Summary (Windows, ROCm/TheRock, PyTorch ROCm)

We can reproduce a *MIOpen JIT / HIPRTC compilation failure* on Windows
that forces a *runtime fallback to CPU* even when the run reports a
GPU-selected device.
Key symptom

   -

   *Device selection says GPU*, but *training executes on CPU*:
   -

      selected_device: cuda
      -

      training_device_effective: cpu
      -

      first_batch_device: cpu

Primary failure

   -

   *HIPRTC JIT compilation fails* during MIOpen path:
   -

      HIPRTC_ERROR_COMPILATION (6)
      -

      'type_traits' file not found
      -

      followed by miopenStatusUnknownError and *CPU fallback*

This looks consistent with a missing/undiscoverable C++ standard library
header path during HIPRTC compilation on Windows.
------------------------------
Repro evidence bundle (latest)

*UTC_TS:* 20260221T175250Z
*Output dir:* test_output/amd_logs/20260221T175250Z/
Environment truth

   -

   Confirmed conda env + ROCm torch:
   -

      rocm_env
      -

      torch 2.9.1+rocmsdk20260116
      -

      HIP 7.2.26024-f6f897bd3d
      -

      torch.cuda.is_available() == True

(See env_truth.txt in bundle.)
Error locations

   -

   HIPRTC compilation failure + missing header:
   -

      miopen_output_logs.txt shows:
      -

         HIPRTC_ERROR_COMPILATION (6)
         -

         'type_traits' file not found
         -

   MIOpen runtime fallback:
   -

      miopenStatusUnknownError → CPU fallback

hipBLASLt signal

   -

   hipblaslt_sorted.txt has *very minimal content* (3 non-empty lines),
   below the expected “top lines” target—suggesting limited/partial
   enumeration in this run.

Device-truth (same run)

   -

   runner_result.json shows mismatch:
   -

      selected_device: cuda
      -

      training_device_effective: cpu
      -

      first_batch_device: cpu

------------------------------
Question: “Have you fixed the MIOpen JIT compilation issue?”

*No.* The latest diagnostic still reproduces the HIPRTC compile failure (
type_traits not found) and MIOpen falls back to CPU.
------------------------------
What we are asking / next debugging steps (guidance requested)

   1.

   *Is there a known Windows HIPRTC include-path issue* in ROCm/TheRock on
   Windows where standard headers like <type_traits> are not found?
   2.

   What is the *supported mechanism to provide the correct C++
   header/include paths* for HIPRTC on Windows for MIOpen JIT?
   3.

   If ROCm/TheRock issue #2591 is related: is the expected resolution to
   update a specific ROCm/TheRock nightly/build, or to adjust environment
   variables / toolchain discovery?

If you want, I can provide a *minimal standalone HIPRTC compilation repro*
(single file/kernel) to confirm the header-include failure independently of
PyTorch/MIOpen.
------------------------------
Note on responses (AI tooling)

Some of the narrative formatting is AI-assisted, but the *logs, bundles,
and device-truth fields are direct outputs from the run*.
------------------------------


On Tue, Feb 24, 2026 at 8:31 AM Huanran Wang ***@***.***>
wrote:

> *huanrwan-amd* left a comment (ROCm/ROCm#5941)
> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3953308381>
>
> Hi @mgersonde <https://github.com/mgersonde> , can you post the logs and
> all your ROCm path? Thanks.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3953308381>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AJ74GPFWLS3XK6GBZMMF2634NR4H3AVCNFSM6AAAAACUJNBDRSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTSNJTGMYDQMZYGE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>

hipblaslt-bench --api_method c -m 1 -n 256 -k 256 --lda 1 --ldb 256 --ldc 1 --ldd 1  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 1.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 256 -n 256 -k 1 --lda 256 --ldb 1 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 256 -n 1 -k 256 --lda 256 --ldb 256 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 1 -n 256 -k 256 --lda 1 --ldb 256 --ldc 1 --ldd 1  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 1.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 256 -n 256 -k 1 --lda 256 --ldb 1 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 256 -n 1 -k 256 --lda 256 --ldb 256 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 1 -n 256 -k 256 --lda 1 --ldb 256 --ldc 1 --ldd 1  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 1.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 256 -n 256 -k 1 --lda 256 --ldb 1 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 256 -n 1 -k 256 --lda 256 --ldb 256 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 1 -n 256 -k 256 --lda 1 --ldb 256 --ldc 1 --ldd 1  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 1.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 256 -n 256 -k 1 --lda 256 --ldb 1 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 256 -n 1 -k 256 --lda 256 --ldb 256 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 1 -n 256 -k 256 --lda 1 --ldb 256 --ldc 1 --ldd 1  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 1.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 256 -n 256 -k 1 --lda 256 --ldb 1 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
hipblaslt-bench --api_method c -m 256 -n 1 -k 256 --lda 256 --ldb 256 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 

HIP Library Path: C:\Users\mgers\anaconda3\envs\rocm_env\Lib\site-packages\_rocm_sdk_core\bin\amdhip64_7.dll
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -c 0 -F 1 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -c 0 -F 1 -t 1 -w 1
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 2 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 2 -t 1 -w 1
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 4 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 4 -t 1 -w 1
MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(), c_options.size(), c_options.data())' gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp: HIPRTC_ERROR_COMPILATION (6)
MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION (6), source file: gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp
MIOpen(HIP): Warning [BuildHip] In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-18-3ed1ee\input\gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp:28:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-18-3ed1ee\include\sequence.hpp:8:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-18-3ed1ee\include\type.hpp:8:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-18-3ed1ee\include\enable_if.hpp:7:
C:\Users\mgers\AppData\Local\Temp\comgr-56808-18-3ed1ee\include\miopen_type_traits.hpp:151:10: fatal error: 'type_traits' file not found
  151 | #include <type_traits>
      |          ^~~~~~~~~~~~~
1 error generated when compiling for gfx1100.
MIOpen Error: The_Beast:C:/develop/TheRock/rocm-libraries/projects/miopen/src/hipoc/hipoc_program.cpp:299: Code object build failed. Source: gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp
WIN_MODE CUDA/ROCm runtime failure during training: miopenStatusUnknownError
Falling back to CPU for this training loop.
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -c 0 -F 1 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -c 0 -F 1 -t 1 -w 1
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 2 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 2 -t 1 -w 1
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 4 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 4 -t 1 -w 1
MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(), c_options.size(), c_options.data())' gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp: HIPRTC_ERROR_COMPILATION (6)
MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION (6), source file: gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp
MIOpen(HIP): Warning [BuildHip] In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-19-7d0656\input\gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp:28:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-19-7d0656\include\sequence.hpp:8:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-19-7d0656\include\type.hpp:8:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-19-7d0656\include\enable_if.hpp:7:
C:\Users\mgers\AppData\Local\Temp\comgr-56808-19-7d0656\include\miopen_type_traits.hpp:151:10: fatal error: 'type_traits' file not found
  151 | #include <type_traits>
      |          ^~~~~~~~~~~~~
1 error generated when compiling for gfx1100.
MIOpen Error: The_Beast:C:/develop/TheRock/rocm-libraries/projects/miopen/src/hipoc/hipoc_program.cpp:299: Code object build failed. Source: gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp
WIN_MODE CUDA/ROCm runtime failure during training: miopenStatusUnknownError
Falling back to CPU for this training loop.
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -c 0 -F 1 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -c 0 -F 1 -t 1 -w 1
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 2 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 2 -t 1 -w 1
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 4 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 4 -t 1 -w 1
MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(), c_options.size(), c_options.data())' gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp: HIPRTC_ERROR_COMPILATION (6)
MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION (6), source file: gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp
MIOpen(HIP): Warning [BuildHip] In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-20-c56070\input\gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp:28:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-20-c56070\include\sequence.hpp:8:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-20-c56070\include\type.hpp:8:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-20-c56070\include\enable_if.hpp:7:
C:\Users\mgers\AppData\Local\Temp\comgr-56808-20-c56070\include\miopen_type_traits.hpp:151:10: fatal error: 'type_traits' file not found
  151 | #include <type_traits>
      |          ^~~~~~~~~~~~~
1 error generated when compiling for gfx1100.
MIOpen Error: The_Beast:C:/develop/TheRock/rocm-libraries/projects/miopen/src/hipoc/hipoc_program.cpp:299: Code object build failed. Source: gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp
WIN_MODE CUDA/ROCm runtime failure during training: miopenStatusUnknownError
Falling back to CPU for this training loop.
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -c 0 -F 1 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -c 0 -F 1 -t 1 -w 1
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 2 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 2 -t 1 -w 1
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 4 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 4 -t 1 -w 1
MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(), c_options.size(), c_options.data())' gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp: HIPRTC_ERROR_COMPILATION (6)
MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION (6), source file: gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp
MIOpen(HIP): Warning [BuildHip] In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-21-95abe0\input\gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp:28:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-21-95abe0\include\sequence.hpp:8:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-21-95abe0\include\type.hpp:8:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-21-95abe0\include\enable_if.hpp:7:
C:\Users\mgers\AppData\Local\Temp\comgr-56808-21-95abe0\include\miopen_type_traits.hpp:151:10: fatal error: 'type_traits' file not found
  151 | #include <type_traits>
      |          ^~~~~~~~~~~~~
1 error generated when compiling for gfx1100.
MIOpen Error: The_Beast:C:/develop/TheRock/rocm-libraries/projects/miopen/src/hipoc/hipoc_program.cpp:299: Code object build failed. Source: gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp
WIN_MODE CUDA/ROCm runtime failure during training: miopenStatusUnknownError
Falling back to CPU for this training loop.
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -c 0 -F 1 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -c 0 -F 1 -t 1 -w 1
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 2 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 2 -t 1 -w 1
rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 4 -t 1 -w 1
MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 45 -F 4 -t 1 -w 1
MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(), c_options.size(), c_options.data())' gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp: HIPRTC_ERROR_COMPILATION (6)
MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION (6), source file: gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp
MIOpen(HIP): Warning [BuildHip] In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-22-47c72f\input\gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp:28:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-22-47c72f\include\sequence.hpp:8:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-22-47c72f\include\type.hpp:8:
In file included from C:\Users\mgers\AppData\Local\Temp\comgr-56808-22-47c72f\include\enable_if.hpp:7:
C:\Users\mgers\AppData\Local\Temp\comgr-56808-22-47c72f\include\miopen_type_traits.hpp:151:10: fatal error: 'type_traits' file not found
  151 | #include <type_traits>
      |          ^~~~~~~~~~~~~
1 error generated when compiling for gfx1100.
MIOpen Error: The_Beast:C:/develop/TheRock/rocm-libraries/projects/miopen/src/hipoc/hipoc_program.cpp:299: Code object build failed. Source: gridwise_generic_reduction_first_call_multiblock_reduce_partial_dims.cpp
WIN_MODE CUDA/ROCm runtime failure during training: miopenStatusUnknownError
Falling back to CPU for this training loop.
RUNNER_RESULT=D:\My Documents\Cascade projects\LSTM\lstm_investment_strategy\test_output\amd_logs\20260221T175250Z\runner_result.json

﻿5	hipblaslt-bench --api_method c -m 256 -n 1 -k 256 --lda 256 --ldb 256 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
5	hipblaslt-bench --api_method c -m 256 -n 256 -k 1 --lda 256 --ldb 1 --ldc 256 --ldd 256  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 0.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 
5	hipblaslt-bench --api_method c -m 1 -n 256 -k 256 --lda 1 --ldb 256 --ldc 1 --ldd 1  --stride_a 0 --stride_b 0 --stride_c 0 --stride_d 0  --alpha 1.000000 --beta 1.000000 --transA N --transB N --batch_count 1 --scaleA 0 --scaleB 0  --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --scale_type f32_r --bias_type f32_r   --compute_type f32_r --algo_method index --solution_index 1214 --activation_type none --any_stride --rotating 0 --cold_iters 0 --iters 0 

﻿HIP Library Path: C:\Users\mgers\anaconda3\envs\rocm_env\Lib\site-packages\_rocm_sdk_core\bin\amdhip64_7.dll
C:\Users\mgers\anaconda3\envs\rocm_env\python.exe
rocm_env
2.9.1+rocmsdk20260116
7.2.26024-f6f897bd3d
True


---

### 评论 #12 — huanrwan-amd (2026-02-24T20:23:45Z)

Hi @mgersonde , thanks for posting. Can you format the generated response for better reading/viewing? Can you also provide a minimum repro? Thanks.

---

### 评论 #13 — nekoteai (2026-02-24T21:06:36Z)

I met this problem as well when I run an OCR model using mineru.
I'm using latest nightly build 
Name: rocm-sdk-libraries-gfx1151
Version: 7.12.0a20260223

logs:

OCR-det:   0%|                                                                                  | 0/30 [00:00<?, ?it/s]
MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(), c_options.size(), c_options.data())' MIOpenBatchNormFwdInferSpatialHIP.cpp: HIPRTC_ERROR_COMPILATION (6)
MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION (6), source file: **MIOpenBatchNormFwdInferSpatialHIP.cpp
MIOpen(HIP): Warning [BuildHip] In file included from <temp_path>/input/MIOpenBatchNormFwdInferSpatialHIP.cpp:30:**
In file included from <temp_path>/include/bnorm_spatial_activation_functions.hpp:32:
In file included from <temp_path>/include/configuration.hpp:34:
In file included from <temp_path>/include/vector_types.hpp:8:
**<temp_path>/include/miopen_type_traits.hpp:151:10: fatal error: 'type_traits' file not found
  151 | #include <type_traits>**
      |          ^~~~~~~~~~~~~
1 error generated when compiling for gfx1151.
MIOpen Error: ZenFlow:<source_path>/rocm-libraries/projects/miopen/src/hipoc/hipoc_program.cpp:299: Code object build failed. Source: MIOpenBatchNormFwdInferSpatialHIP.cpp
OCR-det:   0%|                                                                                  | 0/30 [00:00<?, ?it/s]
2026-02-25 04:00:04.025 | ERROR    | mineru.cli.client:parse_doc:211 - miopenStatusUnknownError
Traceback (most recent call last):

  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code

  File "<venv_path>/mineru.exe\__main__.py", line 10, in <module>
    sys.exit(main())

  File "<venv_path>/click\core.py", line 1485, in __call__
    return self.main(*args, **kwargs)
  File "<venv_path>/click\core.py", line 1406, in main
    rv = self.invoke(ctx)
  File "<venv_path>/click\core.py", line 1269, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "<venv_path>/click\core.py", line 824, in invoke
    return callback(*args, **kwargs)
  File "<venv_path>/click\decorators.py", line 34, in new_func
    return f(get_current_context(), *args, **kwargs)
  File "<venv_path>/mineru\cli\client.py", line 220, in main
    parse_doc([Path(input_path)])
> File "<venv_path>/mineru\cli\client.py", line 196, in parse_doc
    do_parse(
  File "<venv_path>/mineru\cli\common.py", line 478, in do_parse
    _process_hybrid(
  File "<venv_path>/mineru\cli\common.py", line 337, in _process_hybrid
    middle_json, infer_result, _vlm_ocr_enable = hybrid_doc_analyze(
  File "<venv_path>/mineru\backend\hybrid\hybrid_analyze.py", line 427, in doc_analyze
    inline_formula_list, ocr_res_list, hybrid_pipeline_model = _process_ocr_and_formulas(
  File "<venv_path>/mineru\backend\hybrid\hybrid_analyze.py", line 253, in _process_ocr_and_formulas
    ocr_res_list = ocr_det(
  File "<venv_path>/mineru\backend\hybrid\hybrid_analyze.py", line 78, in ocr_det
    ocr_res = hybrid_pipeline_model.ocr_model.ocr(
  File "<venv_path>/mineru\model\ocr\pytorch_paddle.py", line 220, in ocr
    dt_boxes, elapse = self.text_detector(img)
  File "<venv_path>/mineru\model\utils\tools\infer\predict_det.py", line 313, in __call__
    outputs = self.net(inp)
  File "<venv_path>/torch\nn\modules\module.py", line 1776, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "<venv_path>/torch\nn\modules\module.py", line 1787, in _call_impl
    return forward_call(*args, **kwargs)
  File "<venv_path>/mineru\model\utils\pytorchocr\modeling\architectures\base_model.py", line 74, in forward
    x = self.backbone(x)

  File "<venv_path>/torch\nn\functional.py", line 2846, in batch_norm
    return torch.batch_norm(

RuntimeError: miopenStatusUnknownError

---

### 评论 #14 — mgersonde (2026-02-25T19:42:26Z)

Hi @huanrwan-amd â€”
cleaned summary + paths + min repro (Windows / gfx1100 RX 7900 XTX).

Issue:
- MIOpen HIPRTC JIT compilation fails during RNN/LSTM driver invocation on
gfx1100.
- Error includes: fatal error: 'type_traits' file not found
- Followed by: miopenStatusUnknownError and fallback to CPU.

ROCm / HIP paths (Windows):
- Conda env: rocm_env
- Python: (see python_env.txt)
- HIP DLL: (see python_env.txt)
- Torch: (see python_env.txt)
- GPU: (see python_env.txt / rocminfo.txt)

Attachments:
- repro_bundle.zip (this folder zipped)
- runner_result.json (if found)

On Tue, Feb 24, 2026 at 1:06 PM 茶糕·晴 ***@***.***> wrote:

> *nekoteai* left a comment (ROCm/ROCm#5941)
> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3954730350>
>
> I met this problem as well when I run an OCR model using mineru.
> I'm using latest nightly build
> Name: rocm-sdk-libraries-gfx1151
> Version: 7.12.0a20260223
>
> logs:
>
> OCR-det: 0%| | 0/30 [00:00<?, ?it/s]
> MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(),
> c_options.size(), c_options.data())' MIOpenBatchNormFwdInferSpatialHIP.cpp:
> HIPRTC_ERROR_COMPILATION (6)
> MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION
> (6), source file:
> *MIOpenBatchNormFwdInferSpatialHIP.cpp MIOpen(HIP): Warning [BuildHip] In
> file included from
> <temp_path>/input/MIOpenBatchNormFwdInferSpatialHIP.cpp:30:*
> In file included from
> <temp_path>/include/bnorm_spatial_activation_functions.hpp:32:
> In file included from <temp_path>/include/configuration.hpp:34:
> In file included from <temp_path>/include/vector_types.hpp:8:
>
> *<temp_path>/include/miopen_type_traits.hpp:151:10: fatal error:
> 'type_traits' file not found 151 | #include <type_traits>*
> | ^~~~~~~~~~~~~
> 1 error generated when compiling for gfx1151.
> MIOpen Error:
> ZenFlow:<source_path>/rocm-libraries/projects/miopen/src/hipoc/hipoc_program.cpp:299:
> Code object build failed. Source: MIOpenBatchNormFwdInferSpatialHIP.cpp
> OCR-det: 0%| | 0/30 [00:00<?, ?it/s]
> 2026-02-25 04:00:04.025 | ERROR | mineru.cli.client:parse_doc:211 -
> miopenStatusUnknownError
> Traceback (most recent call last):
>
> File "", line 198, in _run_module_as_main
> File "", line 88, in _run_code
>
> File "<venv_path>/mineru.exe_*main*_.py", line 10, in
> sys.exit(main())
>
> File "<venv_path>/click\core.py", line 1485, in *call*
> return self.main(*args, **kwargs)
> File "<venv_path>/click\core.py", line 1406, in main
> rv = self.invoke(ctx)
> File "<venv_path>/click\core.py", line 1269, in invoke
> return ctx.invoke(self.callback, **ctx.params)
> File "<venv_path>/click\core.py", line 824, in invoke
> return callback(*args, **kwargs)
> File "<venv_path>/click\decorators.py", line 34, in new_func
> return f(get_current_context(), *args, **kwargs)
> File "<venv_path>/mineru\cli\client.py", line 220, in main
> parse_doc([Path(input_path)])
>
> File "<venv_path>/mineru\cli\client.py", line 196, in parse_doc
> do_parse(
> File "<venv_path>/mineru\cli\common.py", line 478, in do_parse
> _process_hybrid(
> File "<venv_path>/mineru\cli\common.py", line 337, in _process_hybrid
> middle_json, infer_result, _vlm_ocr_enable = hybrid_doc_analyze(
> File "<venv_path>/mineru\backend\hybrid\hybrid_analyze.py", line 427, in
> doc_analyze
> inline_formula_list, ocr_res_list, hybrid_pipeline_model =
> _process_ocr_and_formulas(
> File "<venv_path>/mineru\backend\hybrid\hybrid_analyze.py", line 253, in
> _process_ocr_and_formulas
> ocr_res_list = ocr_det(
> File "<venv_path>/mineru\backend\hybrid\hybrid_analyze.py", line 78, in
> ocr_det
> ocr_res = hybrid_pipeline_model.ocr_model.ocr(
> File "<venv_path>/mineru\model\ocr\pytorch_paddle.py", line 220, in ocr
> dt_boxes, elapse = self.text_detector(img)
> File "<venv_path>/mineru\model\utils\tools\infer\predict_det.py", line
> 313, in *call*
> outputs = self.net(inp)
> File "<venv_path>/torch\nn\modules\module.py", line 1776, in
> _wrapped_call_impl
> return self._call_impl(*args, **kwargs)
> File "<venv_path>/torch\nn\modules\module.py", line 1787, in _call_impl
> return forward_call(*args, **kwargs)
> File
> "<venv_path>/mineru\model\utils\pytorchocr\modeling\architectures\base_model.py",
> line 74, in forward
> x = self.backbone(x)
>
> File "<venv_path>/torch\nn\functional.py", line 2846, in batch_norm
> return torch.batch_norm(
>
> RuntimeError: miopenStatusUnknownError
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3954730350>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AJ74GPFN7MQ2TX6B5QPECJT4NS4PFAVCNFSM6AAAAACUJNBDRSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTSNJUG4ZTAMZVGA>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #15 — huanrwan-amd (2026-02-25T20:15:08Z)

Hi @mgersonde, thanks for formatting the response. The attachments are still missing…

---

### 评论 #16 — mgersonde (2026-02-25T21:21:57Z)

[runner_result.json](https://github.com/user-attachments/files/25558117/runner_result.json)

[repro_bundle.zip](https://github.com/user-attachments/files/25558094/repro_bundle.zip)



---

### 评论 #17 — huanrwan-amd (2026-02-26T19:48:43Z)

Hi @mgersonde , checked the attached files. logs and cmd shows "NOT FOUND". Can you please check those files? Thanks.

---

### 评论 #18 — mgersonde (2026-02-26T23:14:59Z)

Subject: ROCm/ROCm#5941 — concise Windows repro evidence (gfx1100)

Hi @huanrwan-amd,

Attached is a corrected repro_bundle.zip from my Windows RX 7900 XTX
(gfx1100) run.

Key evidence (in attached logs):

HIPRTC_ERROR_COMPILATION (6)
fatal error: 'type_traits' file not found
miopenStatusUnknownError, then fallback to CPU
runner_result.json shows selected_device: cuda but
training_device_effective: cpu
This reproduces the issue in a minimal, review-friendly package.

If you want one additional direct run, please share the exact expected
Windows MIOpenDriver.exe path/package layout and I will execute that
command verbatim.

Best,
Michael



On Thu, Feb 26, 2026 at 11:49 AM Huanran Wang ***@***.***>
wrote:

> *huanrwan-amd* left a comment (ROCm/ROCm#5941)
> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3968839208>
>
> Hi @mgersonde <https://github.com/mgersonde> , checked the attached
> files. logs and cmd shows "NOT FOUND". Can you please check those files?
> Thanks.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5941#issuecomment-3968839208>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AJ74GPDZP5ZWMDNUVECVO234N5E3FAVCNFSM6AAAAACUJNBDRSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTSNRYHAZTSMRQHA>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>

﻿MIOpenDriver.exe NOT FOUND under expected roots.

﻿MIOpen(HIP): Command [LogCmdRNN] MIOpenDriver.exe rnn -n 256 -W 30 -H 256 -l 2 -b 1 -m lstm -p 0 -r 0 -q 0 -k 128 -c 0 -F 1 -t 1 -w 1

﻿HIP Library Path: C:\Users\mgers\anaconda3\envs\rocm_env\Lib\site-packages\_rocm_sdk_core\bin\amdhip64_7.dll
C:\Users\mgers\anaconda3\envs\rocm_env\python.exe
rocm_env
2.9.1+rocmsdk20260116
7.2.26024-f6f897bd3d
True


---

### 评论 #19 — huanrwan-amd (2026-03-02T14:44:18Z)

Hi @mgersonde, can you please check the repro_bundle.zip is posted on github side? Thanks.

---

### 评论 #20 — mgersonde (2026-03-04T19:19:51Z)

Hi @huanrwan-amd,

Thanks for calling out the earlier ambiguity — you were right that the previous bundle showed MIOpenDriver.exe as NOT FOUND.

I prepared a refreshed Windows evidence bundle and re-ran filesystem discovery. On this install, MIOpenDriver.exe is: **NOT FOUND** (see find_miopendriver.txt for roots searched and results).

The refreshed bundle is ready to upload on ROCm/ROCm#5941 and includes env/path truth plus runtime evidence: HIPRTC_ERROR_COMPILATION (6), fatal error: 'type_traits' file not found, miopenStatusUnknownError, CPU fallback, and runner_result device mismatch (selected_device=cuda, training_device_effective=cpu).

Could you confirm the expected Windows packaging/layout for MIOpenDriver.exe in ROCm/TheRock? If MIOpenDriver.exe is not expected on Windows, what is the preferred Windows-native equivalent command/tool to capture the same MIOpen JIT diagnostics?

---

### 评论 #21 — mgersonde (2026-03-04T19:23:10Z)

[env_truth.txt](https://github.com/user-attachments/files/25749486/env_truth.txt)
[find_miopendriver.txt](https://github.com/user-attachments/files/25749484/find_miopendriver.txt)
[hipblaslt_log.txt](https://github.com/user-attachments/files/25749479/hipblaslt_log.txt)
[hipblaslt_sorted.txt](https://github.com/user-attachments/files/25749483/hipblaslt_sorted.txt)
[miopen_output_logs.txt](https://github.com/user-attachments/files/25749485/miopen_output_logs.txt)
[path.txt](https://github.com/user-attachments/files/25749478/path.txt)
[README_AMD.md](https://github.com/user-attachments/files/25749481/README_AMD.md)
[runner_result.json](https://github.com/user-attachments/files/25749480/runner_result.json)

---
