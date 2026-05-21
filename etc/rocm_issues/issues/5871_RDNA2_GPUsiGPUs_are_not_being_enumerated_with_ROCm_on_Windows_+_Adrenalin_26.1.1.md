# RDNA2 GPUs/iGPUs are not being enumerated with ROCm on Windows + Adrenalin 26.1.1

> **Issue #5871**
> **状态**: closed
> **创建时间**: 2026-01-21T01:28:37Z
> **更新时间**: 2026-04-04T13:21:52Z
> **关闭时间**: 2026-03-17T20:21:24Z
> **作者**: brubeedoobee
> **标签**: Windows, application:pytorch, status: triage, status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/5871

## 标签

- **Windows** (颜色: #c2e0c6)
- **application:pytorch** (颜色: #bfdadc)
- **status: triage** (颜色: #585dd7)
- **status: fix submitted** (颜色: #75d97e)

## 负责人

- harkgill-amd

## 描述

Update:
Update: Tested with ROCm 7.2 - Issue persists
I've installed the latest AMD Software: Adrenalin Edition 26.1.1 (released January 21, 2026) with the AI Bundle, which includes ROCm 7.2.
Results:

✅ Model still loads successfully to GPU
❌ Same crash on text generation - Python process terminates silently
❌ Same Event Viewer error:

Faulting module: amdhip64_7.dll
Exception code: 0xc0000005 (Access Violation)
System specs:

Driver: Adrenalin 26.1.1 (released today)
PyTorch: 2.9.0+rocmsdk20251116 (from AI Bundle)
ROCm: 7.2
GPU: AMD Radeon RX 7900 XTX
CPU: AMD Ryzen 9 9950X
OS: Windows 11 Build 10.0.26200

The bug has now been confirmed across ROCm 7.1.1 and 7.2 with both driver versions 25.20.01.17 and 26.1.1.

Log Name:      Application
Source:        Application Error
Date:          1/21/2026 8:01:56 PM
Event ID:      1000
Task Category: Application Crashing Events
Level:         Error
Keywords:      
User:          AORUSX870E\bruce
Computer:      AorusX870E
Description:
Faulting application name: python.exe, version: 3.12.10150.1013, time stamp: 0x67f515a7
Faulting module name: amdhip64_7.dll, version: 10.0.3581.0, time stamp: 0x69198ccb
Exception code: 0xc0000005
Fault offset: 0x00000000002ab8ba
Faulting process id: 0x3560
Faulting application start time: 0x1DC8B3A7B7F1C4E
Faulting application path: C:\Users\bruce\AppData\Local\Programs\Python\Python312\python.exe
Faulting module path: D:\text-generation-webui\venv\Lib\site-packages\_rocm_sdk_core\bin\amdhip64_7.dll
Report Id: 48a78f7a-9a69-48ac-91f8-af963f486ac6
Faulting package full name: 
Faulting package-relative application ID: 
Event Xml:
<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
  <System>
    <Provider Name="Application Error" Guid="{a0e9b465-b939-57d7-b27d-95d8e925ff57}" />
    <EventID>1000</EventID>
    <Version>0</Version>
    <Level>2</Level>
    <Task>100</Task>
    <Opcode>0</Opcode>
    <Keywords>0x8000000000000000</Keywords>
    <TimeCreated SystemTime="2026-01-22T01:01:56.1806364Z" />
    <EventRecordID>5007</EventRecordID>
    <Correlation />
    <Execution ProcessID="8404" ThreadID="19116" />
    <Channel>Application</Channel>
    <Computer>AorusX870E</Computer>
    <Security UserID="S-1-5-21-97673550-4160431826-3737378671-1001" />
  </System>
  <EventData>
    <Data Name="AppName">python.exe</Data>
    <Data Name="AppVersion">3.12.10150.1013</Data>
    <Data Name="AppTimeStamp">67f515a7</Data>
    <Data Name="ModuleName">amdhip64_7.dll</Data>
    <Data Name="ModuleVersion">10.0.3581.0</Data>
    <Data Name="ModuleTimeStamp">69198ccb</Data>
    <Data Name="ExceptionCode">c0000005</Data>
    <Data Name="FaultingOffset">00000000002ab8ba</Data>
    <Data Name="ProcessId">0x3560</Data>
    <Data Name="ProcessCreationTime">0x1dc8b3a7b7f1c4e</Data>
    <Data Name="AppPath">C:\Users\bruce\AppData\Local\Programs\Python\Python312\python.exe</Data>
    <Data Name="ModulePath">D:\text-generation-webui\venv\Lib\site-packages\_rocm_sdk_core\bin\amdhip64_7.dll</Data>
    <Data Name="IntegratorReportId">48a78f7a-9a69-48ac-91f8-af963f486ac6</Data>
    <Data Name="PackageFullName">
    </Data>
    <Data Name="PackageRelativeAppId">
    </Data>
  </EventData>
</Event>

### Problem Description

Sharing my experience getting oobabooga running on AMD 7900 XTX with Windows. Got very close but hit an AMD bug. Documenting for others.

AMD Radeon RX 7900 XTX + Windows 11 + ROCm 7.1.1: Model Loads Successfully, Crashes on Text Generation

TL;DR: Model loads to GPU perfectly, crashes immediately on first generation attempt. Root cause: HIP runtime bug in amdhip64_7.dll. Awaiting AMD fix.
Hardware/Software Configuration

GPU: AMD Radeon RX 7900 XTX (24GB VRAM)
OS: Windows 11
Driver: AMD Software PyTorch Edition 25.20.01.17 (driver store version 32.0.22001.17002)
Python: 3.12.10
PyTorch: 2.9.0+rocmsdk20251116 (ROCm 7.1.1)
oobabooga: Latest main branch (January 2026)

Installation Steps & Reproduction
1. Install Python 3.12

Download from python.org
During install, check "Add Python to PATH" and "Disable path length limit"

2. Clone oobabooga
cmdcd D:\
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui
3. Create virtual environment
cmdpython -m venv venv
venv\Scripts\activate.bat
4. Install oobabooga base requirements
cmdpip install -r requirements\full\requirements.txt
5. Install ROCm SDK + PyTorch (in the activated venv)
cmdpip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/rocm_sdk_core-0.1.dev0-py3-none-win_amd64.whl

pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/rocm_sdk_devel-0.1.dev0-py3-none-win_amd64.whl

pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/rocm_sdk_libraries_custom-0.1.dev0-py3-none-win_amd64.whl

pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/rocm-0.1.dev0.tar.gz

pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/torch-2.9.0+rocmsdk20251116-cp312-cp312-win_amd64.whl

pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/torchaudio-2.9.0+rocmsdk20251116-cp312-cp312-win_amd64.whl

pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/torchvision-0.24.0+rocmsdk20251116-cp312-cp312-win_amd64.whl
6. Verify PyTorch sees GPU
cmdpython -c "import torch; print(torch.cuda.is_available())"
python -c "import torch; print(torch.cuda.get_device_name(0))"
Expected output: True and AMD Radeon RX 7900 XTX
7. Start oobabooga
cmdpython server.py
8. Reproduce the crash

Open browser to http://127.0.0.1:7860/
Go to Model tab
In "Download model or LoRA", enter: mistralai/Mistral-7B-Instruct-v0.2
Click Download (wait for completion, ~15GB)
Select the model from dropdown
Model loader: Transformers
attn-implementation: eager (or sdpa, both crash)
Click Load → ✅ Succeeds ("Successfully loaded" message appears)
Go to Chat tab
Type any message (e.g., "Hello")
Click Generate → ❌ Python crashes silently
Check Windows Event Viewer for amdhip64_7.dll crash

What Works ✅

PyTorch correctly detects 7900 XTX
Model downloads successfully
Model loads to GPU successfully (completes in ~22 seconds)
Shows "Successfully loaded" message

What Fails ❌

Text generation crashes immediately on first GPU compute
Python process terminates with no console error
Windows Event Viewer shows amdhip64_7.dll access violation

### Root Cause
**Windows Event Viewer shows:**
```
Faulting module: amdhip64_7.dll (version 10.0.3581.0)
Exception code: 0xc0000005 (Access Violation)
Fault offset: 0x00000000002ab8ba
Module path: D:\text-generation-webui\venv\Lib\site-packages\_rocm_sdk_core\bin\amdhip64_7.dll

This is AMD's HIP runtime library crashing during the first GPU compute operation.
Attempted Fixes That Don't Help

❌ Disabling Windows TDR (registry edits to TdrDelay, TdrLevel)
❌ Changing attention implementation (eager vs sdpa)
❌ Environment variables (HSA_OVERRIDE_GFX_VERSION, HSA_ENABLE_SDMA=0, AMD_DIRECT_DISPATCH=0)
❌ Different models or quantization levels
❌ Lowering truncation length

Status
This appears to be a known bug in ROCm 7.1.1 for Windows with RDNA3 GPUs (similar crashes reported in llama.cpp GitHub issues #17429).
The good news: We're extremely close - model loading works perfectly. This should be fixed in the next AMD driver/ROCm release.
Workarounds:

Wait for AMD driver update (25.30.x or ROCm 7.2+)
Dual-boot Linux - ROCm works perfectly on Linux
CPU-only mode - Set CUDA_VISIBLE_DEVICES=-1 (slow but functional)

For AMD/ROCm Team
If you need additional diagnostics (core dumps, debug logs, etc.) from a Windows 11 + 7900 XTX setup, happy to provide them.



### Operating System

window 11 OS Version: 10.0.26200

### CPU

CPU: AMD Ryzen 9 9950X 16-Core Processor

### GPU

AMD Radeon(TM) Graphics AMD Radeon RX 7900 XTX

### ROCm Version

ROCm: 7.1.52802-561cc400e1 PyTorch: 2.9.0+rocmsdk20251116

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (26 条)

### 评论 #1 — harkgill-amd (2026-01-22T17:52:46Z)

Hey @brubeedoobee, from 

> Install oobabooga base requirements
cmdpip install -r requirements\full\requirements.txt

It looks like this requirements.txt file will pull in cuda specific wheels during install ([ref](https://github.com/oobabooga/text-generation-webui/blob/main/requirements/full/requirements.txt#L45-L46)) - have you given the `requirements_amd.txt` file a try? That's setup to pull Vulkan specific wheels for Windows and ROCm wheels for Linux with there being no Windows+ROCm/HIP option provided here yet https://github.com/oobabooga/llama-cpp-binaries/releases/tag/v0.76.0.

---

### 评论 #2 — brubeedoobee (2026-01-23T00:02:08Z)

Response to harkgill-amd:
Thank you for the suggestion. I tested with requirements_amd.txt using both ROCm 7.1.1 and 7.2. Here are the detailed results:
HARDWARE:

GPU: AMD Radeon RX 7900 XTX
CPU: AMD Ryzen 9 9950X 16-Core
RAM: 64GB
OS: Windows 11 Build 10.0.26200

DRIVER: AMD Software: Adrenalin Edition 26.1.1 (released January 21, 2026)
SOFTWARE: oobabooga text-generation-webui (latest main branch)
INSTALLATION STEPS (Fresh venv):
cd D:\text-generation-webui
rmdir /s venv
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements\full\requirements_amd.txt
TEST 1: ROCm 7.1.1
Install ROCm 7.1.1 packages:
pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/rocm_sdk_core-0.1.dev0-py3-none-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/rocm_sdk_devel-0.1.dev0-py3-none-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/rocm_sdk_libraries_custom-0.1.dev0-py3-none-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/rocm-0.1.dev0.tar.gz https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/torch-2.9.0+rocmsdk20251116-cp312-cp312-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/torchaudio-2.9.0+rocmsdk20251116-cp312-cp312-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/torchvision-0.24.0+rocmsdk20251116-cp312-cp312-win_amd64.whl
Verification commands and results:

python -c "import torch; print(torch.__version__)" → 2.9.0+rocmsdk20251116
python -c "import torch; print(torch.cuda.is_available())" → True
python -c "import torch; print(torch.cuda.get_device_name(0))" → AMD Radeon RX 7900 XTX

Oobabooga test:

Started server: python server.py
Loaded model: mistralai/Mistral-7B-Instruct-v0.2 with Transformers loader
Result: Model loaded successfully in 22 seconds
Attempted text generation in Chat tab
Result: Python process crashed silently

Event Viewer Error:
Faulting module: amdhip64_7.dll
Module version: 10.0.3581.0
Module timestamp: 0x69198ccb
Exception code: 0xc0000005 (Access Violation)
Fault offset: 0x00000000002ab8ba
TEST 2: ROCm 7.2
Install ROCm 7.2 packages:
pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_core-7.2.0.dev0-py3-none-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_devel-7.2.0.dev0-py3-none-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_libraries_custom-7.2.0.dev0-py3-none-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm-7.2.0.dev0.tar.gz https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torch-2.9.1+rocmsdk20260116-cp312-cp312-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torchaudio-2.9.1+rocmsdk20260116-cp312-cp312-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torchvision-0.24.1+rocmsdk20260116-cp312-cp312-win_amd64.whl
Verification commands and results:

python -c "import torch; print(torch.__version__)" → 2.9.1+rocmsdk20260116
python -c "import torch; print(torch.cuda.is_available())" → (hangs indefinitely, crashes silently)

Oobabooga test:

Started server: python server.py
Attempted to load model: mistralai/Mistral-7B-Instruct-v0.2
Result: Python crashed during model loading before completion

Event Viewer Error:
Faulting module: amdhip64_7.dll
Module version: 10.0.3581.0
Module timestamp: 0x69695bad (DIFFERENT from 7.1.1!)
Exception code: 0xc0000005 (Access Violation)
Fault offset: 0x00000000004c7fe1 (DIFFERENT from 7.1.1!)
COMPARISON SUMMARY:
ROCm 7.1.1:

torch.cuda.is_available(): Works (returns True)
torch.cuda.get_device_name(): Works (returns GPU name)
Model loading: Completes successfully
Text generation: Crashes
Crash location: amdhip64_7.dll offset 0x2ab8ba

ROCm 7.2:

torch.cuda.is_available(): Hangs/crashes
torch.cuda.get_device_name(): Crashes
Model loading: Crashes mid-load
Text generation: Cannot test (crashes earlier)
Crash location: amdhip64_7.dll offset 0x4c7fe1 (different offset!)

CRITICAL FINDING: The amdhip64_7.dll timestamp changed between ROCm 7.1.1 (0x69198ccb) and 7.2 (0x69695bad), confirming AMD updated the HIP runtime. However, ROCm 7.2 crashes at a different offset (0x4c7fe1 vs 0x2ab8ba) and earlier in the initialization sequence, indicating a regression in stability.
CONCLUSION:
ROCm 7.2 regressed stability compared to 7.1.1 on Windows + 7900 XTX. The HIP runtime now crashes during basic GPU queries and model loading, whereas 7.1.1 successfully loaded models and only crashed during compute operations.
Note: I'm using the Transformers loader (pure PyTorch), not llama.cpp, so the llama-cpp-binaries you referenced aren't involved in this crash path.
Is there a Windows ROCm 7.2 hotfix or nightly build I should test? Or should I wait for a future release?

---

### 评论 #3 — harkgill-amd (2026-01-23T20:08:57Z)

> Note: I'm using the Transformers loader (pure PyTorch), not llama.cpp, so the llama-cpp-binaries you referenced aren't involved in this crash path.

Thanks for the clarification. I gave this a try on my end and was able to get text-generation-webui up and running with mistralai/Mistral-7B-Instruct-v0.2. The first thing we'd need to address is the basic torch failures that you're seeing with ROCm 7.2 (`torch.cuda.is_available(): Hangs/crashes` .etc). 

Your package versions do look correct for `torch` but there might be some conflicts going on in your venv causing the errors parsing for your 7900XTX. The easiest way to identify this would be to spin up a fresh venv using the Adrenalin 26.1.1 AI Bundle Create PyTorch Virtual Environment option. This'll create the venv and pull in the latest ROCm/torch 7.2.0 packages avoiding the need to manually pip install anything. Once you've done this, can you give the basic torch commands another try?

Beyond this setup, I was running into a `ModuleNotFoundError: No module named 'torch._C._distributed_c10d';` when trying to load the Mistral model. This had to do with the `torchao` build pulled in by requirements.txt conflicting with our `torch 2.9.1+rocmsdk20260116` build as we don't have distributed support on Windows yet - removing `torchao` worked around this and I was able to start up a chat with the model.

---

### 评论 #4 — brubeedoobee (2026-01-23T22:43:41Z)

<img width="1092" height="917" alt="Image" src="https://github.com/user-attachments/assets/f8db496d-e4e5-4cdf-99f8-08a1d2053e63" />

What code is supposed to be in that box on the create a virtual environment popup? If I click the copy command and go to a prompt there is nothing to paste


---

### 评论 #5 — harkgill-amd (2026-01-26T15:02:52Z)

That box would normally have the `pip install` commands for installing ROCm listed out. Could you try clicking the "Create" button anyways to see if the venv get's created successfully? We might need to track this separately as a UI or functional issue with the AI bundle.

---

### 评论 #6 — brubeedoobee (2026-01-26T21:54:03Z)

It tells me that it failed to install 

<img width="754" height="525" alt="Image" src="https://github.com/user-attachments/assets/d9be2285-b86f-4a41-883c-64fb58ac8999" />

---

### 评论 #7 — harkgill-amd (2026-01-28T15:44:17Z)

Thanks for sharing. I've created https://github.com/ROCm/ROCm/issues/5909 to track this issue separately. Could you please share the logs from `C:\Program Files\AMD\AMDInstallManager\Logs` there, this'll help narrow down what's failing as we're having some trouble reproducing this on our end.

As for the original failures detecting your GPU with ROCm 7.2, let's try manually creating a fresh virtual environment and giving the torch commands a try. You can do this with the following (In powershell),
```
python -m venv my_env
.\my_venv\Scripts\activate

#ROCm Install
pip install --no-cache-dir `
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_core-7.2.0.dev0-py3-none-win_amd64.whl `
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_devel-7.2.0.dev0-py3-none-win_amd64.whl `
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm_sdk_libraries_custom-7.2.0.dev0-py3-none-win_amd64.whl `
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/rocm-7.2.0.dev0.tar.gz

#Torch Install
pip install --no-cache-dir `
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torch-2.9.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl `
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torchaudio-2.9.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl `
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2/torchvision-0.24.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl

#Torch commands
python -c "import torch; print(torch.cuda.is_available())"
python -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))"
```
Let me know if you run into any errors prior to running the torch commands.

---

### 评论 #8 — brubeedoobee (2026-01-29T00:53:47Z)

U{DATE:
**SOLUTION FOUND:**
Disabling integrated graphics (Radeon Graphics from 9950X) in BIOS resolved the crash.
ROCm now works perfectly with only the discrete RX 7900 XTX enabled.

Test results after disabling IGPU:
- torch.cuda.is_available() = True
- torch.cuda.get_device_name(0) = AMD Radeon RX 7900 XTX

This appears to be a conflict between ROCm and systems with both integrated + discrete AMD GPUs.


PS C:\Users\bruce> python -c "import torch; print(torch.cuda.is_available())"
True
PS C:\Users\bruce> python -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))"
device name [0]: AMD Radeon RX 7900 XTX

I would love to be able to have

**System Configuration:**
- CPU: AMD Ryzen 9 9950X (with integrated Radeon Graphics)
- Discrete GPU: AMD Radeon RX 7900 XTX
- OS: Windows 11
- AMD Adrenalin Driver: 25.1.1 (32.0.23017.1001, dated 2026-01-08)
- Python: 3.12
- ROCm: 7.2.0.dev0

**Issue:**
Manual installation of ROCm 7.2 and PyTorch succeeded, but crashes when attempting to use torch.cuda APIs. Both test commands crash silently:
- `python -c "import torch; print(torch.cuda.is_available())"`
- `python -c "import torch; print(torch.cuda.get_device_name(0))"`

**Event Viewer Errors:**
Faulting module: amdhip64_7.dll (v10.0.3581.0)
Exception code: 0xc0000005 (Access Violation)
Fault offset: 0x00000000004c7fe1

**GPU Detection:**
System has both integrated graphics (Radeon Graphics from 9950X) and discrete RX 7900 XTX. ROCm appears to crash when enumerating devices.
 

---

### 评论 #9 — harkgill-amd (2026-01-29T21:45:36Z)

Nice catch! If you'd rather not completely disable your iGPU, you can also hide it from HIP by setting the environment variable `HIP_VISIBLE_DEVICES=1`. Are you able to get the model loaded and running now that torch is working or are there still any errors blocking you? Reminder to `pip uninstall torchao` to workaround the error mentioned here https://github.com/ROCm/ROCm/issues/5871#issuecomment-3792171418.

---

### 评论 #10 — brubeedoobee (2026-01-30T00:42:50Z)

I can't hide the iGPU.  I tried with an environmental variable, and Powershell. I tried device 1 and 0 and nothing worked,  for now I'll keep the iGPU disabled.

---

### 评论 #11 — harkgill-amd (2026-01-30T17:15:31Z)

What are you seeing when you set the environment variable and then try to run the torch commands? Here's a quick little script you can use to debug what HIP can see pre and post setting the variable,
```
#include <hip/hip_runtime.h>
#include <stdio.h>

int main() {
    int deviceCount = 0;
    hipError_t err = hipGetDeviceCount(&deviceCount);
    
    if (err != hipSuccess) {
        printf("Error getting device count: %s\n", hipGetErrorString(err));
        return 1;
    }
    
    printf("HIP Visible Devices: %d\n\n", deviceCount);
    
    for (int i = 0; i < deviceCount; i++) {
        hipDeviceProp_t props;
        hipGetDeviceProperties(&props, i);
        
        printf("Device %d: %s\n", i, props.name);
        printf("  GCN Architecture: %s\n", props.gcnArchName);
        printf("\n");
    }
    
    return 0;
}
```
Then run the following to compile and run the program,
```
hipcc hip_device.cpp
.\a.exe
```
For example, I see the following output on my 7900XTX machine without an iGPU prior to setting any environment variables,
```
.\a.exe
HIP Visible Devices: 1

Device 0: AMD Radeon RX 7900 XTX
  GCN Architecture: gfx1100
```
After setting `$env:HIP_VISIBLE_DEVICES = "1"`, which will limit HIP to only seeing `Device 1`, I see 
```
.\a.exe
Error getting device count: no ROCm-capable device is detected
```
As there is no Device 1 in my case. You should be able to swap between the two devices using this method.


---

### 评论 #12 — brubeedoobee (2026-01-30T19:18:33Z)

I apologize for not having an apples-to-apples comparison - I upgraded from the RX 7900 XTX to the Radeon AI PRO R9700 before seeing your diagnostic request. However, here are the results with the R9700 (gfx1201):

**With iGPU enabled in BIOS:**
```
.\a.exe
HIP Library Path: C:\WINDOWS\SYSTEM32\amdhip64_7.dll
HIP Visible Devices: 1
Device 0: AMD Radeon AI PRO R9700
  GCN Architecture: gfx1201
```

However, `torch.cuda.is_available()` returns `False` in this configuration, and `torch.cuda.get_device_name(0)` raises `RuntimeError: No HIP GPUs are available`.

**With iGPU disabled in BIOS:**
```
.\a.exe
HIP Library Path: C:\WINDOWS\SYSTEM32\amdhip64_7.dll
HIP Visible Devices: 1
Device 0: AMD Radeon AI PRO R9700
  GCN Architecture: gfx1201
```

PyTorch now works correctly:
- `torch.cuda.is_available()` returns `True`
- `torch.cuda.get_device_name(0)` returns `AMD Radeon AI PRO R9700`

**Environment variable testing:**
Setting `HIP_VISIBLE_DEVICES` to either `0` or `1` had no effect on the behavior. The dual-GPU issue affects both the RX 7900 XTX and R9700. For now, disabling the iGPU in BIOS remains the only working solution.

---

### 评论 #13 — harkgill-amd (2026-02-03T20:46:04Z)

I wasn't able to reproduce this behavior where enabling the iGPU caused torch to fail however, I did see the following,

> With iGPU enabled in BIOS:
> 
> .\a.exe
> HIP Library Path: C:\WINDOWS\SYSTEM32\amdhip64_7.dll
> HIP Visible Devices: 1
> Device 0: AMD Radeon AI PRO R9700
>   GCN Architecture: gfx1201

This in itself seems like a regression as I'd expect the iGPU to be enumerated here. We're looking into this issue specifically which may uncover why torch ends up failing downstream in your configuration as well. For now, please continue with manually disabling your iGPU.

---

### 评论 #14 — alexsarmiento (2026-02-26T02:25:58Z)

@harkgill-amd  I am having the same exact issue. I have a 7900XTX dGPU and a Ryzen 9 7900 CPU. Python 3.12 and Adrenaline 26.1.1

And HIP_VISIBLE_DEVICES=1 doesn't work. Only disabling the iGPU in BIOS works

However, the last working pytorch build that works for me without this problem is `torch==2.10.0+rocm7.12.0a20260218`. After that, pytorch, hipinfo etc just fail.  


---

### 评论 #15 — harkgill-amd (2026-02-26T15:13:37Z)

Thanks for sharing @alexsarmiento. We're looking into the lack of iGPU enumeration but still haven't been able to reproduce the actual failures (torch, hipinfo.etc) when the iGPU is enabled. Could you share the following when you get a chance,

w/ Last known working ROCm/Pytorch Build (iGPU enabled)
- Output of `hipInfo`
- `python -c "import torch; print(torch.cuda.is_available())"`
- `python -c "import torch; print([torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])"`

w/Latest TheRock nightly (iGPU enabled)
- Output of `hipInfo`
- `python -c "import torch; print(torch.cuda.is_available())"`


---

### 评论 #16 — alexsarmiento (2026-02-26T18:55:19Z)

@harkgill-amd 
$env:HIP_VISIBLE_DEVICES = "1"
 torch 2.10.0+rocm7.12.0a20260218
```
hipInfo
(venv) PS D:\ComfyUI>
--------------------------------------------------------------------------------
device#                           0
Name:                             AMD Radeon RX 7900 XTX
pciBusID:                         3
pciDeviceID:                      0
pciDomainID:                      0
multiProcessorCount:              48
maxThreadsPerMultiProcessor:      2048
isMultiGpuBoard:                  0
clockRate:                        2482 Mhz
memoryClockRate:                  1250 Mhz
memoryBusWidth:                   384
totalGlobalMem:                   23.98 GB
totalConstMem:                    2147483647
sharedMemPerBlock:                64.00 KB
canMapHostMemory:                 1
regsPerBlock:                     196608
warpSize:                         32
l2CacheSize:                      6291456
computeMode:                      0
maxThreadsPerBlock:               1024
maxThreadsDim.x:                  1024
maxThreadsDim.y:                  1024
maxThreadsDim.z:                  1024
maxGridSize.x:                    2147483647
maxGridSize.y:                    65536
maxGridSize.z:                    65536
major:                            11
minor:                            0
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
gcnArchName:                      gfx1100
maxAvailableVgprsPerThread:       256 DWORDs
peers:
non-peers:                        device#0

memInfo.total:                    23.98 GB
memInfo.free:                     23.84 GB (99%)
```

```
python -c "import torch; print(torch.cuda.is_available())"
Failed to get device count: no ROCm-capable device is detected (error code: 100)
True
```
```
python -c "import torch; print([torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])"
Failed to get device count: no ROCm-capable device is detected (error code: 100)
['AMD Radeon RX 7900 XTX']
```

############################
torch 2.10.0+rocm7.12.0a20260226

```
hipInfo


```

```
python -c "import torch; print(torch.cuda.is_available())"
Failed to get device count: no ROCm-capable device is detected (error code: 100)
```

```
python -c "import torch; print([torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])"
Failed to get device count: no ROCm-capable device is detected (error code: 100)
```

So after torch>2.10.0+rocm7.12.0a20260218 hipinfo produces no output, and pytorch fails too.

At some point "Failed to get device count: no ROCm-capable device is detected (error code: 100)" error started to appear, but still worked. 

Another person reported the same issue while using comfyui: https://github.com/Comfy-Org/ComfyUI/issues/12598

---

### 评论 #17 — harkgill-amd (2026-02-26T21:02:55Z)

I ran some tests on my end on Adrenalin 26.2.2 w/ 7900XT + RDNA2 iGPU. The 2/18 wheels do work correctly with both the iGPU and dGPU being enumerated in the hipInfo output, 
```
(2_18_wheels) C:\Users\rocmWindows\Documents>hipInfo | findstr "gcnArchName"
gcnArchName:                      gfx1100
gcnArchName:                      gfx1036
```
This is in contrast to the 7.2.0 wheels and any of the newer nightlies where the RDNA2 entry is missing. Oddly enough, in all of these cases, I did not encounter any torch failures with `python -c "import torch; print(torch.cuda.is_available())"` always returning true. I'm thinking the torch errors you're seeing might be a combination of the iGPU being dropped + HIP_VISIBLE_DEVICES hiding the remaining GPU. Could you retry the torch commands without the environment variable set? 

---

### 评论 #18 — alexsarmiento (2026-02-26T21:55:13Z)

@harkgill-amd 
With the updated driver and without setting HIP_VISIBLE_DEVICES:
torch-2.10.0+rocm7.12.0a20260226:
```
(venv) PS D:\ComfyUI> hipInfo | findstr "gcnArchName"
(venv) PS D:\ComfyUI>
(venv) PS D:\ComfyUI> python -c "import torch; print([torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])"
(venv) PS D:\ComfyUI>
```
I get nothing. Not even the "Failed to get device count: no ROCm-capable device is detected (error code: 100)" error msg appears anymore.

Reverting back to torch-2.10.0+rocm7.12.0a20260218:

```
(venv) PS D:\ComfyUI> hipInfo | findstr "gcnArchName"
gcnArchName:                      gfx1036
gcnArchName:                      gfx1100
(venv) PS D:\ComfyUI> python -c "import torch; print([torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])"
['AMD Radeon(TM) Graphics', 'AMD Radeon RX 7900 XTX']
```

---

### 评论 #19 — harkgill-amd (2026-03-06T15:56:29Z)

A quick update on this issue. We've put up a fix for the lack of RDNA2 device enumeration which should make it's way into the nightlies some time next week. This fix will at minimum resolve the issue of dGPUs and iGPUs not being visible to HIP and other third party applications. 

We still haven't been able to reproduce any of the iGPU enabled torch crashing, though there's a good chance that'll be resolved with the aforementioned fix as well. If the crashing does end up persisting post-fix, we'll continue to investigate. 

Thanks for all the help in narrowing this down!

---

### 评论 #20 — djismgaming (2026-03-06T18:30:54Z)

> A quick update on this issue. We've put up a fix for the lack of RDNA2 device enumeration which should make it's way into the nightlies some time next week. This fix will at minimum resolve the issue of dGPUs and iGPUs not being visible to HIP and other third party applications.

This is amazing!!! 🤗


---

### 评论 #21 — 0xDELUXA (2026-03-11T13:10:58Z)

> 
> Beyond this setup, I was running into a `ModuleNotFoundError: No module named 'torch._C._distributed_c10d';` when trying to load the Mistral model. This had to do with the `torchao` build pulled in by requirements.txt conflicting with our `torch 2.9.1+rocmsdk20260116` build as we don't have distributed support on Windows yet - removing `torchao` worked around this and I was able to start up a chat with the model.

[This](https://github.com/pytorch/ao/pull/4017) would resolve the `distributed` issue in `torchao`.

---

### 评论 #22 — harkgill-amd (2026-03-12T20:11:29Z)

@alexsarmiento, the enumeration fix is present in the latest nightlies and RDNA2 devices are now correctly being reported. Could you give these wheels a try and confirm that both hipInfo and torch are working correctly with your configuration? Make sure to remove `HIP_VISIBLE_DEVICES` if previously set. 

---

### 评论 #23 — alexsarmiento (2026-03-12T21:42:28Z)

@harkgill-amd 
> [@alexsarmiento](https://github.com/alexsarmiento), the enumeration fix is present in the latest nightlies and RDNA2 devices are now correctly being reported. Could you give these wheels a try and confirm that both hipInfo and torch are working correctly with your configuration? Make sure to remove `HIP_VISIBLE_DEVICES` if previously set.

```
Successfully installed rocm-7.13.0a20260312 rocm-sdk-core-7.13.0a20260312 rocm-sdk-devel-7.13.0a20260312 rocm-sdk-libraries-gfx110X-all-7.13.0a20260312 torch-2.10.0+rocm7.13.0a20260312 torchaudio-2.10.0+rocm7.13.0a20260312 torchvision-0.25.0+rocm7.13.0a20260312
(venv) PS D:\ComfyUI> hipInfo | findstr "gcnArchName"
gcnArchName:                      gfx1036
gcnArchName:                      gfx1100
(venv) PS D:\ComfyUI> python -c "import torch; print([torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])"
['AMD Radeon(TM) Graphics', 'AMD Radeon RX 7900 XTX']
```

Seems to be working now!. I'll keep testing with comfyui.

Edit: So far comfyui seems to work normally.

---

### 评论 #24 — harkgill-amd (2026-03-13T19:03:31Z)

Nice, the 3/12 nightlies are the earliest builds with the fix and it looks like everything is working as expected.

Our gfx103X nightly pipelines ran into unrelated build failures so we haven't got a nightly for RDNA2 only configurations just yet. Once one get's published (hopefully tonight) and everything works there as well, we can wrap this issue up.

---

### 评论 #25 — harkgill-amd (2026-03-17T20:21:24Z)

gfx103X nightlies are also now available with the fix present. Will close this issue out for now - please open a new issue if you're running into any similar issues or a regression.

---

### 评论 #26 — CarlGao4 (2026-04-04T12:01:14Z)

Have anybody tried that can the nightly builds successfully run LLMs on RDNA2 iGPUs?

I've just read the issue, it seems that this issue only fixed the device enumerating process, but not the original crash during inference process. I'm testing with TheRock 7.12 (ROCm 7.2) with 780m iGPU, but it crashes all the time. Then with the latest patch applied, can I run pytorch on this iGPU?

If I want to build it from source, which commit should I build?

---
