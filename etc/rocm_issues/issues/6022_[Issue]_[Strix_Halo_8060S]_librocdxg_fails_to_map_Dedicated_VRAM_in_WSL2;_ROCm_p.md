# [Issue]: [Strix Halo / 8060S] librocdxg fails to map Dedicated VRAM in WSL2; ROCm pool size is limited by .wslconfig memory setting

> **Issue #6022**
> **状态**: closed
> **创建时间**: 2026-03-07T15:59:42Z
> **更新时间**: 2026-05-02T15:23:54Z
> **关闭时间**: 2026-04-24T17:51:29Z
> **作者**: sandynz
> **标签**: status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/6022

## 标签

- **status: fix submitted** (颜色: #75d97e)

## 负责人

- harkgill-amd

## 描述

### Problem Description

## Env

### Windows11
```
(Get-WmiObject Win32_OperatingSystem).Version
10.0.26200

(Get-WmiObject win32_Processor).Name
AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

(Get-WmiObject win32_VideoController).Name
AMD Radeon(TM) 8060S Graphics
```

### WSL2
```
$ echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";
OS:
NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"

$ echo "CPU: " && cat /proc/cpuinfo | grep "model name" | sort --unique;
CPU:
model name      : AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

$ echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
GPU:
Load librocdxg.so successully!
Load all DTIF APIs OK!
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151
  Marketing Name:          AMD Radeon(TM) 8060S Graphics
Unload librocdxg.so successully!
      Name:                    amdgcn-amd-amdhsa--gfx1151
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
```

### ROCm

Version: /opt/rocm-7.2.0

### librocdxg

https://github.com/ROCm/librocdxg.git
commit: 4880c78da9f1f400d0c1a985afb72e7f3ea05161 ( Date:   Mon Feb 9 15:45:39 2026 +0800 )

### python3 -m torch.utils.collect_env
```
PyTorch version: 2.9.1+rocm7.2.0.git7e1940d4
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 7.2.26015-fc0010cf6a

OS: Ubuntu 24.04.3 LTS (x86_64)
GCC version: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
Clang version: Could not collect
CMake version: version 3.28.3
Libc version: glibc-2.39

Python version: 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0] (64-bit runtime)
Python platform: Linux-6.6.114.1-microsoft-standard-WSL2-x86_64-with-glibc2.39
Is CUDA available: True
CUDA runtime version: Could not collect
CUDA_MODULE_LOADING set to:
GPU models and configuration: AMD Radeon(TM) 8060S Graphics (gfx1151)
Nvidia driver version: Could not collect
cuDNN version: Could not collect
Is XPU available: False
HIP runtime version: 7.2.26015
MIOpen runtime version: 3.5.1
Is XNNPACK available: True

Versions of relevant libraries:
[pip3] numpy==2.4.2
[pip3] torch==2.9.1+rocm7.2.0.lw.git7e1940d4
[pip3] torchaudio==2.9.0+rocm7.2.0.gite3c6ee2b
[pip3] torchvision==0.24.0+rocm7.2.0.gitb919bd0c
[pip3] triton==3.5.1+rocm7.2.0.gita272dfa8
[conda] Could not collect
```

### BIOS
- **BIOS UMA Settings:** `Dedicated Graphics Memory` (UMA FB Size) set to **96GB**

## Problem Description
On the **Strix Halo (8060S)** platform, `librocdxg` appears to fail to recognize or map the **Dedicated GPU Memory (Local Segment)** in the WSL2 environment. Instead, the ROCm memory pool size is strictly tied to the system memory allocated to the WSL2 VM via the `.wslconfig` file.

This prevents the GPU from utilizing its full 96GB UMA potential for large-scale AI workloads (e.g., LLM inference) within WSL2, despite the hardware being fully capable in native Windows.

## Observed Evidence

### 1. Native Windows vs. WSL2 Discrepancy
- **Native Windows:** Running `ollama` (qwen3.5:27b) in native Windows successfully utilizes **41.5GB** of the **96GB Dedicated VRAM** (monitored via AMD Software: Adrenalin Edition).
- **WSL2 Mapping:** In WSL2, `rocminfo` reports a `Pool Size` that exactly matches the `memory` limit defined in `.wslconfig`. 

### 2. `.wslconfig` Correlation Test
The ROCm pool size scales with the VM's assigned RAM rather than the BIOS UMA setting:
- When `.wslconfig` is default (~16GB), `rocminfo` reports: `Pool 1 Size: 16187412 (0xf70014) KB`.
- When `.wslconfig` is set to `memory=24GB`, `rocminfo` reports: `Pool 1 Size: 24604680 (0x1777008) KB`.

### 3. Performance & Stability Issues
When a PyTorch script requests memory near the `.wslconfig` limit (e.g., 14GB allocation in a 16GB VM), the following occurs:
- Windows Task Manager shows **Shared GPU Memory** usage spiking to 14.6/15.8 GB.
- CPU temperature rises to **85°C** due to heavy memory paging/swapping overhead.
- The process hangs, while the **96GB Dedicated GPU Memory** remains completely idle (0.6GB used).

### 4. IOMMU Status
`rocminfo` reports `IOMMU Support: None` in WSL2, even though IOMMU and SVM are enabled in the BIOS.

## Reproduction Steps
1. Set BIOS UMA FB Size to 96GB.
2. Install ROCm with `librocdxg` in WSL2 Ubuntu 24.04.
3. Run `rocminfo` and compare `Pool 1 Size` with the memory limit in `.wslconfig`.
4. Run a PyTorch script to allocate memory exceeding the WSL2 RAM limit but within the 96GB UMA limit.
5. Observe that the allocation triggers system paging or fails, instead of using the Dedicated VRAM.

## Expected Behavior
`librocdxg` should map the 96GB Dedicated VRAM (UMA Frame Buffer) as the primary `LOCAL_SEGMENT` for the ROCm runtime, allowing for large allocations independent of the WSL2 system memory limit.

## Additional Context
- Setting `ROCM_DEBUG_ENABLE_WDDM_ANY=1` does not change the reported pool size.
- The 8060S compute cores are functional, reaching ~30.93 TFLOPS in GEMM tests, indicating the issue is strictly related to memory segment mapping.


### Operating System

Windows 11 Professional + WSL2: Ubuntu 24.04

### CPU

AMD RYZEN AI MAX+ 395 w

### GPU

Radeon 8060S

### ROCm Version

/opt/rocm-7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information


## Test script and screenshots

### 1, Run `ollama run qwen3.5:27b` on Windows 11

Task Manager, screenshot attachment 1

<img width="836" height="356" alt="Image" src="https://github.com/user-attachments/assets/2409eb6a-3556-42f7-9bf0-55bbcd1f4c51" />

### 2, Run Python script in WSL2

`target_gb` was changed from `14` to `8`.

```
import torch
import time

def test_strix_halo_performance():
    print(f"--- Hardware & Environment Check ---")
    print(f"PyTorch Version: {torch.__version__}")
    print(f"ROCm Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Device Name: {torch.cuda.get_device_name(0)}")
    else:
        print("Error: ROCm GPU not detected by PyTorch.")
        return

    # 8060S excels at FP16/BF16 computation.
    device = torch.device("cuda")
    dtype = torch.float16 

    print(f"\n--- Phase 1: Peak Compute Test (GEMM) ---")
    # Stressing the GPU cores with large matrix multiplication
    size = 8192  
    a = torch.randn(size, size, device=device, dtype=dtype)
    b = torch.randn(size, size, device=device, dtype=dtype)
    
    # Warm-up
    for _ in range(10):
        torch.matmul(a, b)
    
    torch.cuda.synchronize()
    start = time.time()
    iters = 50
    for _ in range(iters):
        torch.matmul(a, b)
    torch.cuda.synchronize()
    end = time.time()
    
    # Calculate TFLOPS: (2 * N^3 * iterations) / time
    tflops = (2 * size**3 * iters) / (end - start) / 1e12
    print(f"Matrix Size: {size}x{size}")
    print(f"Avg Latency: {(end - start)/iters*1000:.2f} ms")
    print(f"Estimated Throughput: {tflops:.2f} TFLOPS")

    print(f"\n--- Phase 2: Memory Bandwidth Test ---")
    # Testing data movement speed within the Unified Memory
    gb_size = 4 
    elements = (gb_size * 1024**3) // 2  # float16 = 2 bytes
    x = torch.randn(elements, device=device, dtype=dtype)
    y = torch.empty_like(x)
    
    torch.cuda.synchronize()
    start = time.time()
    for _ in range(100):
        y.copy_(x)
    torch.cuda.synchronize()
    end = time.time()
    
    # Bandwidth = (Size * Iterations * 2 for Read+Write) / Time
    bandwidth = (gb_size * 100 * 2) / (end - start)
    print(f"Transfer Size: {gb_size} GB")
    print(f"Actual Bandwidth: {bandwidth:.2f} GB/s")

    print(f"\n--- Phase 3: Memory Capacity Stress Test ---")
    # Attempting to allocate a large chunk of VRAM
    # NOTE: On Strix Halo in WSL2, this often hits the .wslconfig limit instead of Dedicated VRAM.
    target_gb = 8
    print(f"Attempting to allocate {target_gb} GB of GPU memory...")
    try:
        n_elements = (target_gb * 1024**3) // 2
        dummy_tensor = torch.zeros(n_elements, device=device, dtype=dtype)
        print(f"Success! Allocated {target_gb} GB.")
        
        # Verify write stability
        dummy_tensor.fill_(1.0)
        print("Memory write verification passed.")
    except RuntimeError as e:
        print(f"Allocation Failed: {e}")
        print("\nPossible Cause: librocdxg is mapping System RAM instead of Dedicated VRAM.")

if __name__ == "__main__":
    test_strix_halo_performance()
```

Result:
```
(rocm_env) @WIN-:~$ python3 scripts/test_strix_halo_power.py
--- Hardware & Environment Check ---
PyTorch Version: 2.9.1+rocm7.2.0.git7e1940d4
Load librocdxg.so successully!
Load all DTIF APIs OK!
ROCm Available: True
Device Name: AMD Radeon(TM) 8060S Graphics

--- Phase 1: Peak Compute Test (GEMM) ---
Matrix Size: 8192x8192
Avg Latency: 33.37 ms
Estimated Throughput: 32.95 TFLOPS

--- Phase 2: Memory Bandwidth Test ---
Transfer Size: 4 GB
Actual Bandwidth: 172.05 GB/s

--- Phase 3: Memory Capacity Stress Test ---
Attempting to allocate 8 GB of GPU memory...
Killed
```

Task Manager, screenshot attachment 2

<img width="860" height="359" alt="Image" src="https://github.com/user-attachments/assets/1c36f2e7-1e41-4176-b994-67091bc4b25a" />


---

## 评论 (19 条)

### 评论 #1 — junshichen (2026-03-12T12:18:33Z)

I have exactly the same problem. 

---

### 评论 #2 — harkgill-amd (2026-03-24T19:22:44Z)

Hey @sandynz, is the `.wslconfig` file being auto-generated or is this something you're setting on your end? Could you share the contents of the file here?

EDIT: Was able to reproduce the behaviour of WSL VRAM being limited by the `memory` constraint of `.wslconfig`. I'd imagine we'd want the complete 96GB VRAM allocation to be visible instead of this limited pool - will run this by the WSL team and keep this thread updated. Thanks for the reports!

---

### 评论 #3 — sandynz (2026-03-25T12:21:09Z)

> Was able to reproduce the behaviour of WSL VRAM being limited by the memory constraint of .wslconfig

Hi @harkgill-amd , I reproduced it.

### Current memory settings
Current GPU memory settings is different with before (Total memory: 128GB):
- Dedicated GPU memory: 64GB
- Shared GPU memory (and NPU): 32GB
- Memory: It shows 64GB, shared with `Shared GPU memory`, 32GB in fact.

### Conclusion
It could be reproduced.

### Case 1: Leave `.wslconfig` empty.
rocminfo Result:
Pool 1 `Size:                    32677892(0x1f2a004) KB`

### Case 2: Limit memory to 24GB in `.wslconfig`
```
[wsl2]
memory=24GB
```

Steps:
- wsl --shutdown
- Start Ubuntu 24.04 again, run `rocminfo` again

rocminfo Result:
Pool 1 `Size:                    24604680(0x1777008) KB`


---

### 评论 #4 — harkgill-amd (2026-04-01T14:34:51Z)

Hey @sandynz, this miscalculation of available memory has been addressed with https://github.com/ROCm/librocdxg/pull/12. `rocminfo` now correctly reports the `Pool 1 Size:` as Dedicated GPU Memory + Shared GPU Memory as seen in the screenshot below.

<img width="953" height="297" alt="Image" src="https://github.com/user-attachments/assets/9f724a70-e4c8-48a9-9466-59331e3a19f3" />

Give this a try with the develop branch of librocdxg and let me know if you have any questions.

---

### 评论 #5 — sandynz (2026-04-02T14:57:08Z)

Hi @harkgill-amd , thanks. I pull the latest code and make install again.

## Current Memory Settings
- Dedicated GPU memory: 64GB
- Shared GPU memory (and NPU): 32GB
- Memory: It shows 64GB, shared with Shared GPU memory, 32GB in fact.

## Result - `rocminfo` Pool 1 Size [works]

Steps:
```
~/open_source/librocdxg/build-97b984ba$ sudo rm -f /opt/rocm/lib/librocdxg.so*
~/open_source/librocdxg/build-97b984ba$ ll /opt/rocm/lib/librocdxg.so*
ls: cannot access '/opt/rocm/lib/librocdxg.so*': No such file or directory
~/open_source/librocdxg/build-97b984ba$ sudo make install
...
~/open_source/librocdxg/build-97b984ba$ rocminfo
```

Result:
```
Agent 1
*******
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Vendor Name:             CPU
...
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32683096(0x1f2b458) KB

Agent 2
*******
  Name:                    gfx1151
  Uuid:                    GPU-ffffffffffffffff
  Marketing Name:          AMD Radeon(TM) 8060S Graphics
  Vendor Name:             AMD
...
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    100442262(0x5fca096) KB
```
Agent 1 is CPU, Pool 1 Size 32683096 (31.17GB).
Agent 2 is GPU, Pool 1 Size 100442262 (95.79GB).
Looks it's correct.

## Result - `python3 scripts/test_strix_halo_power.py` [doesn't work]

I've changed `target_gb = 8` to `target_gb = 64`.

```
python3 scripts/test_strix_halo_power.py
--- Hardware & Environment Check ---
PyTorch Version: 2.9.1+rocm7.2.0.git7e1940d4
Load librocdxg.so successully!
Load all DTIF APIs OK!
ROCm Available: True
Device Name: AMD Radeon(TM) 8060S Graphics

--- Phase 1: Peak Compute Test (GEMM) ---
Matrix Size: 8192x8192
Avg Latency: 38.35 ms
Estimated Throughput: 28.67 TFLOPS

--- Phase 2: Memory Bandwidth Test ---
Transfer Size: 4 GB
Actual Bandwidth: 291.58 GB/s

--- Phase 3: Memory Capacity Stress Test ---
Attempting to allocate 64 GB of GPU memory...
Killed
```
It still allocate GPU memory in `shared GPU memory`, and allocate 64 GB GPU memory failled. I killed the process.

Screenshot:
<img width="696" height="236" alt="Image" src="https://github.com/user-attachments/assets/d367381b-c245-4725-b593-27ca1e6958a6" />


---

### 评论 #6 — harkgill-amd (2026-04-02T21:04:55Z)

Haven't been able to repro this behaviour on my end with a simple `hipMalloc` based program,
```
#include <hip/hip_runtime.h>
#include <cstdio>
int main() {
  size_t free_mem = 0, total_mem = 0;
  hipError_t err = hipMemGetInfo(&free_mem, &total_mem);
  if (err == hipSuccess) {
      printf("GPU memory: %.2f GB total, %.2f GB free\n",
             total_mem / (1024.0 * 1024.0 * 1024.0),
             free_mem / (1024.0 * 1024.0 * 1024.0));
  }
  const size_t alloc_size = (size_t)64 * 1024 * 1024 * 1024;
  printf("Attempting to allocate %.0f GB (%zu bytes)...\n",
         alloc_size / (1024.0 * 1024.0 * 1024.0), alloc_size);
  void *ptr = nullptr;
  err = hipMalloc(&ptr, alloc_size);
  if (err == hipSuccess) {
      printf("Success! Allocated 64 GB at %p\n", ptr);
      hipFree(ptr);
      printf("Freed.\n");
  } else {
      printf("Failed: %s (%d)\n", hipGetErrorString(err), err);
  }
  return 0;
}
```

<img width="1575" height="601" alt="Image" src="https://github.com/user-attachments/assets/8a28cc0e-108e-4d27-915e-4b533486c391" />

Can you give this a try and also share the `test_strix_halo_power.py` script?

---

### 评论 #7 — sandynz (2026-04-04T15:06:22Z)

Hi @harkgill-amd , my test results:

## Test `hipMalloc` [it use Shared GPU memory]
Steps:
```
sudo apt update
sudo apt install rocm-dev

# vi hipMalloc_test.cpp , change `alloc_size` to 24GB, since Shared GPU memory is 32GB on my Windows

/opt/rocm/bin/hipcc hipMalloc_test.cpp -o a.out

(rocm_env) sandynz@WIN-:~$ ./a.out
Load librocdxg.so successully!
Load all DTIF APIs OK!
GPU memory: 95.79 GB total, 93.17 GB free
Attempting to allocate 24 GB (25769803776 bytes)...
Success! Allocated 24 GB at 0x78539f600000
Freed.
Unload librocdxg.so successully!
```
Screenshot:
<img width="681" height="226" alt="Image" src="https://github.com/user-attachments/assets/ade7d8a3-7797-4b4e-b21c-51c47a32a075" />

## scripts/test_strix_halo_power_2.py [`torch.zeros` is used]
`scripts/test_strix_halo_power_2.py`
```
import torch
import time

def test_strix_halo_performance():
    print(f"--- Hardware & Environment Check ---")
    print(f"PyTorch Version: {torch.__version__}")
    print(f"ROCm Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Device Name: {torch.cuda.get_device_name(0)}")
    else:
        print("Error: ROCm GPU not detected by PyTorch.")
        return

    # 8060S excels at FP16/BF16 computation.
    device = torch.device("cuda")
    dtype = torch.float16 

    print(f"\n--- Phase 3: Memory Capacity Stress Test ---")
    # Attempting to allocate a large chunk of VRAM
    target_gb = 8
    print(f"Attempting to allocate {target_gb} GB of GPU memory...")
    try:
        n_elements = (target_gb * 1024**3) // 2
        dummy_tensor = torch.zeros(n_elements, device=device, dtype=dtype)
        print(f"Success! Allocated {target_gb} GB.")
        
        # Verify write stability
        dummy_tensor.fill_(1.0)
        print("Memory write verification passed.")
    except RuntimeError as e:
        print(f"Allocation Failed: {e}")
        print("\nPossible Cause: librocdxg is mapping System RAM instead of Dedicated VRAM.")

if __name__ == "__main__":
    test_strix_halo_performance()
```

## Run `rocprof --hip-trace python scripts/test_strix_halo_power_2.py`
```
$ rocprof --hip-trace python scripts/test_strix_halo_power_2.py

WARNING: We are phasing out development and support for roctracer/rocprofiler/rocprof/rocprofv2 in favor of rocprofiler-sdk/rocprofv3 in upcoming ROCm releases. Going forward, only critical defect fixes will be addressed for older versions of profiling tools and libraries. We encourage all users to upgrade to the latest version, rocprofiler-sdk library and rocprofv3 tool, to ensure continued support and access to new features.

Load librocdxg.so successully!
Load all DTIF APIs OK!
Unload librocdxg.so successully!
RPL: on '260404_223639' from '/opt/rocm-7.2.0' in '/home/sandynz'
RPL: profiling '"python" "scripts/test_strix_halo_power_2.py"'
RPL: input file ''
RPL: output dir '/tmp/rpl_data_260404_223639_2359'

------------ ------------ ------------
WARNING: rocprof(v1) is not supported on this device. Recommended use: rocprofv2
Please refer project's README for a list of supported architecures.
------------ ------------ ------------

RPL: result dir '/tmp/rpl_data_260404_223639_2359/input_results_260404_223639'
Load librocdxg.so successully!
Load all DTIF APIs OK!
ROCtracer (2385):
    HIP-trace(*)
--- Hardware & Environment Check ---
PyTorch Version: 2.9.1+rocm7.2.0.git7e1940d4
ROCm Available: True
Device Name: AMD Radeon(TM) 8060S Graphics

--- Phase 3: Memory Capacity Stress Test ---
Attempting to allocate 8 GB of GPU memory...
Success! Allocated 8 GB.
Memory write verification passed.
Warning: Resource leak detected by SharedSignalPool, 2 Signals leaked.
Unload librocdxg.so successully!
Load librocdxg.so successully!
Load all DTIF APIs OK!
Unload librocdxg.so successully!
hsa_copy_deps: 0
scan hip API data 75:76                                                                                                    File '/home/sandynz/results.hip_stats.csv' is generating
dump json 75:76
File '/home/sandynz/results.json' is generating
```

$ cat results.hip_stats.csv
```
"Name","Calls","TotalDurationNs","AverageNs","Percentage"
"hipLaunchKernel",8,763876322,95484540,61.900517428679926
"hipMalloc",1,470125840,470125840,38.096524155114196
"hipStreamIsCapturing",1,17036,17036,0.001380507792353055
"hipGetDevicePropertiesR0600",2,7905,3952,0.0006405796019341922
"hipGetDevice",26,3752,144,0.0003040423360477026
"__hipPushCallConfiguration",8,2537,317,0.00020558512967831064
"__hipPopCallConfiguration",8,1548,193,0.0001254417740410031
"hipSetDevice",5,1369,273,0.00011093655598329022
"hipDevicePrimaryCtxGetState",3,917,305,7.430885451912135e-05
"hipGetLastError",9,783,87,6.345019966027483e-05
"hipGetDeviceCount",4,558,139,4.521738366594298e-05
"hipDeviceGetStreamPriorityRange",1,103,103,8.346577988516356e-06
```

Part of `results.json`:
```
,{"ph":"X","name":"hipMalloc","pid":2,"tid":2385,"ts":"1201478076","dur":"470125",
  "args":{
    "BeginNs":"1201478076289",
    "EndNs":"1201948202129",
    "pid":"2385",
    "tid":"2385",
    "Name":"hipMalloc",
    "args":"( ptr(0x7d2933000000) size(8589934592))",
    "Data":"",
    "DurationNs":"470125840"
  }
}
```


---

### 评论 #8 — harkgill-amd (2026-04-06T15:44:53Z)

So your test script does still work on my end with all of the memory allocation coming from the Dedicated GPU Memory. Noticed you're on ROCm 7.2.0 - could you try matching the working configuration on my end,

- ROCm 7.2.1 with librocdxg https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/wsl/howto_wsl.html#install-wsl-with-rocdxg
- Adrenalin 26.2.2 https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-26-2-2.html
- torch 2.9.1+rocm7.2.1 https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-pytorch.html#option-a-install-pytorch-via-pip-installation

EDIT - Just gave 7.2.0 a try and Shared GPU memory was being used. Upgrading to 7.2.1 with librocdxg is the correct fix here.

---

### 评论 #9 — sandynz (2026-04-08T14:26:01Z)

Hi @harkgill-amd , I tested on 7.2.1.

## Result : doesn't work
Run hipMalloc test cpp code, Windows Task Manager screenshot:
<img width="689" height="231" alt="Image" src="https://github.com/user-attachments/assets/0be2cada-27a2-41be-bac1-6d31a38de372" />

## Test Steps

### Adrenalin version
26.3.1 (Released at 2026/3/9. Auto update to latest version)

### Update PyTorch
Verify:
```
python3 -m torch.utils.collect_env

PyTorch version: 2.9.1+rocm7.2.1.gitff65f5bc
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 7.2.53211-e1a6bc5663
```

### Remove v7.2.0 rocm, hip, amdgpu-install
```
sudo amdgpu-install --uninstall

dpkg -l | grep -E "amdgpu|rocm|hip" | awk '{print $2}' | xargs sudo apt-get purge -y

sudo apt autoremove
sudo apt clean
sudo apt update
```

### Install ROCm 7.2.1
```
wget https://repo.radeon.com/amdgpu-install/7.2.1/ubuntu/noble/amdgpu-install_7.2.1.70201-1_all.deb
sudo apt install ./amdgpu-install_7.2.1.70201-1_all.deb

dpkg -L amdgpu-install

cat /etc/amdgpu-install/amdgpu-setup.conf
BASEURL=https://repo.radeon.com
AMDGPUREL=30.30.1
RELEASE=7.2.1

sudo apt autoremove amdgpu-dkms dkms

amdgpu-install -y --usecase=rocm --no-dkms
```
Verify:
```
ls -lht /opt/ | grep -i rocm
drwxr-xr-x 8 root root 4.0K Apr  8 21:41 rocm-7.2.1
lrwxrwxrwx 1 root root   22 Apr  8 21:41 rocm -> /etc/alternatives/rocm
drwxr-xr-x 4 root root 4.0K Apr  8 21:19 rocm-7.2.0 [just left librocdxg.so]

ls -lht /etc/alternatives/ | grep -i rocm
lrwxrwxrwx 1 root root  28 Apr  8 21:41 amdclang -> /opt/rocm-7.2.1/bin/amdclang
...
lrwxrwxrwx 1 root root  25 Mar 13 07:02 hipcc -> /opt/rocm-7.2.1/bin/hipcc
lrwxrwxrwx 1 root root  29 Mar 13 07:02 hipconfig -> /opt/rocm-7.2.1/bin/hipconfig
lrwxrwxrwx 1 root root  28 Mar 13 07:01 rocminfo -> /opt/rocm-7.2.1/bin/rocminfo
...
```

### Re-install librocdxg
```
ll /opt/rocm/lib/librocdxg.so*
ls: cannot access '/opt/rocm/lib/librocdxg.so*': No such file or directory
```

Re-install librocdxg, follow https://github.com/ROCm/librocdxg/
Verify:
```
ll /opt/rocm/lib/librocdxg.so*
lrwxrwxrwx 1 root root      14 Apr  8 21:46 /opt/rocm/lib/librocdxg.so -> librocdxg.so.1
lrwxrwxrwx 1 root root      18 Apr  8 21:46 /opt/rocm/lib/librocdxg.so.1 -> librocdxg.so.1.1.1
-rw-r--r-- 1 root root 3690464 Apr  8 21:46 /opt/rocm/lib/librocdxg.so.1.1.1
```
librocdxg.so with the latest modification time.

### Restart Ubuntu in WSL2
```
wsl --shutdown
```

### Re-compile hipMalloc_test.cpp
```
/opt/rocm/bin/hipcc --version
HIP version: 7.2.53211-e1a6bc5663
AMD clang version 22.0.0git (https://github.com/RadeonOpenCompute/llvm-project roc-7.2.1 26084 f58b06dce1f9c15707c5f808fd002e18c2accf7e)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-7.2.1/lib/llvm/bin
Configuration file: /opt/rocm-7.2.1/lib/llvm/bin/clang++.cfg
```

```
/opt/rocm/bin/hipcc hipMalloc_test.cpp -o a.out
hipMalloc_test.cpp:18:7: warning: ignoring return value of type 'hipError_t' declared with 'nodiscard' attribute [-Wunused-value]
   18 |       hipFree(ptr);
      |       ^~~~~~~~~~~~
1 warning generated when compiling for gfx1151.
hipMalloc_test.cpp:18:7: warning: ignoring return value of type 'hipError_t' declared with 'nodiscard' attribute [-Wunused-value]
   18 |       hipFree(ptr);
      |       ^~~~~~~~~~~~
1 warning generated when compiling for host.
```

### Test a.out with LOG_LEVEL=4
```
(rocm_env) sandynz@WIN-:~/test_code$ export AMD_LOG_LEVEL=4
(rocm_env) sandynz@WIN-:~/test_code$ export ROC_LOG_LEVEL=4
(rocm_env) sandynz@WIN-:~/test_code$ ./a.out
:3:rocdevice.cpp            :415 : 0031205673 us: [pid:403 tid: 0x7b6b4eeeef80] Initalizing runtime stack, Enumerated GPU agents = 1
:3:rocdevice.cpp            :182 : 0031206297 us: [pid:403 tid: 0x7b6b4eeeef80] Numa selects cpu agent[0]=0x241f5b90(fine=0x241ed480,coarse=0x241f7b80) for gpu agent=0x2420a9e0 CPU<->GPU XGMI=0
:3:rocsettings.cpp          :269 : 0031206326 us: [pid:403 tid: 0x7b6b4eeeef80] Using dev kernel arg wa = 0
:3:comgrctx.cpp             :126 : 0031268497 us: [pid:403 tid: 0x7b6b4eeeef80] Loaded COMGR library version 3.0.
:3:rocdevice.cpp            :1565: 0031270694 us: [pid:403 tid: 0x7b6b4eeeef80] addressableNumVGPRs=256, totalNumVGPRs=1536, vGPRAllocGranule=24, availableRegistersPerCU_=196608
:3:rocdevice.cpp            :1579: 0031270731 us: [pid:403 tid: 0x7b6b4eeeef80] imageSupport=1
:3:rocdevice.cpp            :1610: 0031270737 us: [pid:403 tid: 0x7b6b4eeeef80] Gfx Major/Minor/Stepping: 11/5/1
:3:rocdevice.cpp            :1612: 0031270738 us: [pid:403 tid: 0x7b6b4eeeef80] HMM support: 0, XNACK: 0, Direct host access: 0
:3:rocdevice.cpp            :1614: 0031270767 us: [pid:403 tid: 0x7b6b4eeeef80] Max SDMA Read Mask: 0x1, Max SDMA Write Mask: 0x1
:4:rocdevice.cpp            :2018: 0031272661 us: [pid:403 tid: 0x7b6b4eeeef80] Allocate hsa host memory 0x7afa0e400000, size 0x400000, numa_node = 0, mem_seg = 0
:4:rocdevice.cpp            :2018: 0031273272 us: [pid:403 tid: 0x7b6b4eeeef80] Allocate hsa host memory 0x7afa0e800000, size 0x38, numa_node = 0, mem_seg = 1
:3:hip_context.cpp          :60  : 0031273318 us: [pid:403 tid: 0x7b6b4eeeef80] HIP Version: 7.2.53211.e1a6bc5663, Direct Dispatch: 1
:3:os_posix.cpp             :934 : 0031273327 us: [pid:403 tid: 0x7b6b4eeeef80] HIP Library Path: /opt/rocm-7.2.1/lib/libamdhip64.so.7
:3:hip_memory.cpp           :932 : 0031274192 us: [pid:403 tid: 0x7b6b4eeeef80]  hipMemGetInfo ( 0x7ffcc56184f8, 0x7ffcc56184f0 )
:3:hip_memory.cpp           :956 : 0031274808 us: [pid:403 tid: 0x7b6b4eeeef80] hipMemGetInfo: Returned hipSuccess :
GPU memory: 95.79 GB total, 93.09 GB free
Attempting to allocate 24 GB (25769803776 bytes)...
:3:hip_memory.cpp           :779 : 0031275198 us: [pid:403 tid: 0x7b6b4eeeef80]  hipMalloc ( 0x7ffcc56184e8, 25769803776 )
:4:rocdevice.cpp            :2185: 0033254396 us: [pid:403 tid: 0x7b6b4eeeef80] Allocate hsa device memory 0x7b0b0e200000, size 0x600000000, hsa_mem_flags 0x0h
:3:rocdevice.cpp            :2225: 0033254484 us: [pid:403 tid: 0x7b6b4eeeef80] Device=0x242277d0, freeMem_ = 0x11f2825800
:3:hip_memory.cpp           :781 : 0033254510 us: [pid:403 tid: 0x7b6b4eeeef80] hipMalloc: Returned hipSuccess : 0x7b0b0e200000: duration: 1979312 us
Success! Allocated 64 GB at 0x7b0b0e200000
:3:hip_memory.cpp           :795 : 0033254740 us: [pid:403 tid: 0x7b6b4eeeef80]  hipFree ( 0x7b0b0e200000 )
:4:rocdevice.cpp            :2203: 0033942238 us: [pid:403 tid: 0x7b6b4eeeef80] Free hsa memory 0x7b0b0e200000
:3:rocdevice.cpp            :2225: 0033942320 us: [pid:403 tid: 0x7b6b4eeeef80] Device=0x242277d0, freeMem_ = 0x17f2825800
:3:hip_memory.cpp           :797 : 0033942356 us: [pid:403 tid: 0x7b6b4eeeef80] hipFree: Returned hipSuccess :
Freed.
:4:rocdevice.cpp            :2203: 0033976626 us: [pid:403 tid: 0x7b6b4eeeef80] Free hsa memory 0x7afa0e400000
:4:rocdevice.cpp            :2203: 0033977041 us: [pid:403 tid: 0x7b6b4eeeef80] Free hsa memory 0x7afa0e800000
:1:rocdevice.cpp            :3339: 0033977089 us: [pid:403 tid: 0x7b6b4eeeef80] Unknown Event Type
```
There is `HIP Library Path: /opt/rocm-7.2.1/lib/libamdhip64.so.7`.

Could you guide me to collect more debug info if neccessary?



---

### 评论 #10 — harkgill-amd (2026-04-15T16:13:37Z)

Could you share the exact Strix Halo system you're using (manufacturer and model), along with the BIOS version and output of `wsl --version`?

---

### 评论 #11 — sandynz (2026-04-17T13:53:42Z)

> Could you share the exact Strix Halo system you're using (manufacturer and model), along with the BIOS version and output of `wsl --version`?

1. AI Station
- Manufacturer: abee
- Model: AI Station 395 Max

2. BIOS info
```
Get-CimInstance -ClassName Win32_Bios | Select-Object Manufacturer, SMBIOSBIOSVersion, ReleaseDate

Manufacturer                            SMBIOSBIOSVersion ReleaseDate
------------                            ----------------- -----------
American Megatrends International, LLC. 0.11              2025/10/15 8:00:00
```

3. `wsl --version`
```
wsl --version
WSL version: 2.7.0.0
Kernel version: 6.6.114.1-1
WSLg version: 1.0.71
MSRDC version: 1.2.6676
Direct3D version: 1.611.1-81528511
DXCore version: 10.0.26100.1-240331-1435.ge-release
Windows: 10.0.26200.8246
```


---

### 评论 #12 — harkgill-amd (2026-04-20T18:48:00Z)

Are you able to configure `Resizable Bar` settings in your BIOS - this is only exposed on certain motherboards/BIOS. 

We've reproduced the shared memory allocations on WSL when ReBAR is disabled, enabling it will correctly allocate to the dedicated memory portion. On Native Windows, allocations always go to dedicated GPU memory regardless of ReBAR settings which is inline with what you mentioned in your testing as well. We're currently investigating this discrepancy between WSL and native Windows and will share any updates we have here.

---

### 评论 #13 — sandynz (2026-04-21T13:32:45Z)

I have further investigated the hardware resources on my Strix Halo system (AMI BIOS v0.11). Here are the findings:
- BIOS Confirmation: As previously stated, Above 4G Decoding and Re-Size BAR Support are both Enabled.
- Resource Discrepancy: In Windows Device Manager (Resources tab), I only see a 256MB memory range (9800000000 - 980FFFFFFF). I do NOT see the "Large Memory Range" typically associated with a fully functional Resizable BAR implementation.

<img width="1156" height="248" alt="Image" src="https://github.com/user-attachments/assets/889f0db6-65d0-4853-ba23-ec7560dd6232" />

`Re-Size BAR Support` is enabled by default, I didn't change the setting.

------
Update (summary by LLM):
Significant discrepancy between BIOS settings and OS reporting on my Strix Halo (Ryzen AI MAX+ 395) system:
- BIOS Setting: I manually configured UMA FB Size to 64GB in GFX Configuration.
- OS Reporting: Running Get-CimInstance Win32_VideoController shows AdapterRAM is only 4,293,918,720 bytes (exactly 4GB).
- Resource View: Device Manager still shows a small 256MB memory range, and no "Large Memory Range" is present despite Re-Size BAR being Enabled in BIOS.

Raw data:
```
Get-CimInstance -ClassName Win32_VideoController | Select-Object Name, AdapterRAM

Name                          AdapterRAM
----                          ----------
AMD Radeon(TM) 8060S Graphics 4293918720
```

------
Update (summary by LLM):

Found Device Start Error in Windows Event Log (at 2026/4/1):
I found a critical error in the Device Manager > Events tab for the "AMD Radeon(TM) 8060S Graphics":
- Status: 0xC00000E5 (STATUS_INVALID_PARAMETER)
- Service: amduw23g

Technical Correlation:
This error occurred exactly when the system attempted to start the device. It explains why AdapterRAM is capped at 4GB despite the BIOS being set to 64GB. The driver appears to be failing its memory-mapping request during initialization because the firmware (v0.11) is providing an invalid parameter or an unaddressable memory range for the Strix Halo's unified buffer.

This further confirms that the issue is not with WSL2 settings, but with how the v0.11 BIOS/Firmware interacts with the WDDM driver to expose the Large Memory Range required for ReBAR.

Raw data:
```
设备 PCI\VEN_1002&DEV_1586&SUBSYS_00301F66&REV_C1\4&35fe04f8&0&0041 在启动时出现问题。

驱动程序名称: oem9.inf
类 GUID: {4d36e968-e325-11ce-bfc1-08002be10318}
服务: amduw23g-198975-8f57807d
低层筛选程序: 
高层筛选程序: 
问题: 0x0
问题状态: 0xC00000E5
```



---

### 评论 #14 — sandynz (2026-04-21T14:12:54Z)

Update:

Summary by LLM:
Latest GPU-Z Analysis on Strix Halo (8060S):

I’ve captured a screenshot from GPU-Z (Advanced Tab) which clearly identifies the root cause:
- Hardware is Capable: GPU-Z confirms GPU Hardware Support: Yes.
- BIOS Handshake Failure: Even though Above 4G Decode is detected as Yes, the field Resizable BAR enabled in BIOS shows Unsupported GPU.
- BAR Sizes: The PCI-Express BAR Sizes also shows Unsupported GPU, confirming the system is failing to expose a Large Memory Range.

Conclusion:
This confirms that the v0.11 BIOS is not correctly enumerating the Strix Halo GPU for ReBAR operations, even when the setting is toggled to "Enabled." This directly leads to the 0xC00000E5 device start error and the fallback to shared memory in WSL2.

Screenshot:
<img width="516" height="663" alt="Image" src="https://github.com/user-attachments/assets/1879ddc7-b1a8-4201-9e3a-e2482a2c9046" />

---

### 评论 #15 — harkgill-amd (2026-04-21T14:17:28Z)

The `Get-CimInstance -ClassName Win32_VideoController | Select-Object Name, AdapterRAM` command here is not accurate as with both ReBAR off and on, it'll be capped at 4GB. Not having a "Large Memory Range" in device manager does point to ReBAR being disabled.

https://github.com/ROCm/librocdxg/pull/20 adds the ability to allocate from the invisible heap which is where almost all your dedicated memory will be sitting if ReBAR is disabled. This'll make it so that regardless of ReBAR settings, your allocations should always go  to the dedicated memory portion first, consistent with what we see on Native Windows. Could you try building librocdxg from source using the `longlyao/fix-alloc-list` branch with the patch and giving the test program a run?


---

### 评论 #16 — sandynz (2026-04-21T14:54:42Z)

I tried `longlyao/fix-alloc-list` branch to re-compile and install, it works.

Use the previous hipMalloc test code:
```
:~/test_code$ ./a.out
GPU memory: 95.79 GB total, 92.82 GB free
Attempting to allocate 24 GB (25769803776 bytes)...
Success! Allocated 24 GB at 0x7e69e3c00000
Freed.
```

Windows Task Manager Screenshot:

<img width="685" height="226" alt="Image" src="https://github.com/user-attachments/assets/7b16f55f-fce2-4b33-a8fd-bcaf1356e3dd" />


---

### 评论 #17 — harkgill-amd (2026-04-24T17:51:29Z)

Perfect! I see the PR was merged last night as well so we're good to close this one out. We got 2 pretty important fixes out of this issue - thanks for all your help in both finding the bugs and testing!

---

### 评论 #18 — xuzijian2019 (2026-04-27T19:42:39Z)

Hi, just want a quick check-in. I cloned the [librocdxg](https://github.com/ROCm/librocdxg) repo today, and those fixes are indeed merged. however, seems it is not working on my setup, still the WSL memory= setting is limiting the pool I see in AGENT2 strictly

---

### 评论 #19 — sandynz (2026-05-02T15:12:09Z)

> Hi, just want a quick check-in. I cloned the [librocdxg](https://github.com/ROCm/librocdxg) repo today, and those fixes are indeed merged. however, seems it is not working on my setup, still the WSL memory= setting is limiting the pool I see in AGENT2 strictly

I tested on current latest commit `7772ad6215c86e575d5c614036b53c544a31e46c` (date `Apr 30 17:12:05 2026 +0800`), it works.

### 1. rocminfo Pool 1 Size
```
(rocm_env) sandynz@WIN-:~/open_source/librocdxg/build-260430-7772ad62$ ls -lht /opt/rocm/lib/librocdxg.so*
lrwxrwxrwx 1 root root   14 May  2 23:07 /opt/rocm/lib/librocdxg.so -> librocdxg.so.1
lrwxrwxrwx 1 root root   18 May  2 23:07 /opt/rocm/lib/librocdxg.so.1 -> librocdxg.so.1.1.2
-rw-r--r-- 1 root root 3.5M May  2 23:07 /opt/rocm/lib/librocdxg.so.1.1.2
(rocm_env) sandynz@WIN-:~/open_source/librocdxg/build-260430-7772ad62$
(rocm_env) sandynz@WIN-:~/open_source/librocdxg/build-260430-7772ad62$ rocminfo | grep 'Pool 1' -A 3
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32677896(0x1f2a008) KB
      Allocatable:             TRUE
--
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    100442262(0x5fca096) KB
      Allocatable:             TRUE
```
The second `Pool 1` Size is related to AMD Radeon(TM) 8060S Graphics.

### 2. hipMalloc 90 GB
Test code from https://github.com/ROCm/ROCm/issues/6022#issuecomment-4180470252 , `alloc_size` is changed to 90 GB.
```
$ ./a.out
GPU memory: 95.79 GB total, 93.41 GB free
Attempting to allocate 90 GB (96636764160 bytes)...
Success! Allocated 90 GB at 0x77d081a00000
```

<img width="705" height="237" alt="Image" src="https://github.com/user-attachments/assets/2209071c-2326-4ada-a9b4-feeaa03deb98" />


---
