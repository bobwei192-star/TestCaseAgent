# [Issue]: Critical: ROCm 6.4.4 Core Dump with RDNA 4 (RX 9060 XT) - Basic Operations Fail

> **Issue #5657**
> **状态**: closed
> **创建时间**: 2025-11-12T13:43:12Z
> **更新时间**: 2025-12-03T15:24:01Z
> **关闭时间**: 2025-12-03T15:15:19Z
> **作者**: Horus-p
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5657

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

### Problem Description

Subject: Critical: ROCm 6.4.4 Core Dump with RDNA 4 (RX 9060 XT) - Basic Operations Fail

Hardware:

AMD Radeon RX 9060 XT (gfx1100, Device ID: 7590)

Ubuntu 24.04.3 (officially supported)

Kernel 6.14.0-35-generic

Issue:
Basic GPU operations crash with core dump, including:

PyTorch: torch.tensor([1.0]).cuda() causes system crash

HIP: Simple vector addition kernel fails with addrlib.cpp assertion

Error:

text
test_hip: ./src/image/addrlib/src/core/addrlib.cpp:240: 
static ADDR_E_RETURNCODE rocr::Addr::Lib::Create(const rocr::ADDR_CREATE_INPUT*, rocr::ADDR_CREATE_OUTPUT*): 
Assertion `false' failed.
Aborted (core dumped)
Environment:

ROCm 6.4.4 (fresh install from official repo)

PyTorch 2.9.1+rocm6.4

All components verified at version 6.4.4

Expected:
Basic operations should work per AMD's compatibility statement.

Actual:
System crashes on fundamental GPU operations, making ROCm unusable with RDNA 4.

Request:
Please investigate this RDNA 4 compatibility issue and provide fix timeline.

### Operating System

Ubuntu 24.04.3

### CPU

Dell 7480 i7

### GPU

AMD Radeon RX 9060 XT (gfx1100, Device ID: 7590)

### ROCm Version

ROCm 6.4.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (16 条)

### 评论 #1 — darren-amd (2025-11-12T22:03:51Z)

Hi @Horus-p,

Thanks for reporting this issue. According to our [Compatibility Matrix](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#compatibility-matrix), RDNA4 is supported from ROCm 7.0.2 onwards. Could you please try updating your ROCm version by following the instructions available [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-ubuntu.html) for ROCm 7.1, and let me know if the issue persists? Thanks!

---

### 评论 #2 — Horus-p (2025-11-19T15:26:21Z)

Hi, sorry for delay, after your suggestion I I upgraded to ROCm 7.1, but the system still crashes during PyTorch GPU operations. The RDNA4 support in 7.1 doesn't appear to be working correctly in my Thunderbolt eGPU setup."

---

### 评论 #3 — darren-amd (2025-11-19T15:34:46Z)

Thanks for confirming @Horus-p,

Is it failing on the same `torch.tensor([1.0]).cuda()` operation? Could you please share the version of torch you are running on (`pip list | grep torch`), as well as try installing our latest torch wheels and see if the issue persists: `pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm7.1`? If so, could you please share the full error log as well as the output of `rocminfo`? Thanks!

---

### 评论 #4 — Horus-p (2025-11-20T03:03:31Z)

I would like to comment on one core issue. a part of your users live in countries where a month's salary is USD 500 and where a 5 GB download often half of their monthly internet quota, besides having to deal with heavy chocked speeds 10 to 300 kb/sec. Unless of course it is a main upgrade that includes the whole code, can the structure be different to reduce download size? Very frustrating to get on a disk with 800 GB free space this msg,
Downloading https://download.pytorch.org/whl/nightly/rocm7.1/torch-2.10.0.dev20251118%2Brocm7.1-cp311-cp311-manylinux_2_28_x86_64.whl (5240.4 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸━━━━━━━━━ 4.0/5.2 GB 258.8 kB/s eta 1:18:59ERROR: Could not install packages due to an OSError: [Errno 28] No space left on device

     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸━━━━━━━━━ 4.0/5.2 GB 258.8 kB/s eta 1:18:59
4 GB in the drain.

Further I did test this wheel before with same result.
torch-2.7.0a0+gitbfd8155-cp313-cp313-linux_x86_64.whl,

the question remains is it a pytorch fault or a AMD 7.1 driver fault?

---

### 评论 #5 — Horus-p (2025-11-22T05:20:57Z)

Last test.

![Image](https://github.com/user-attachments/assets/ba199fd7-8b6f-477c-8415-9f91b2cfb1a3)
![Image](https://github.com/user-attachments/assets/f9fbd6d5-0418-4afb-aacd-3d10a27612da)

---

### 评论 #6 — Horus-p (2025-11-26T04:24:03Z)

[DivLOGs.txt](https://github.com/user-attachments/files/23761217/DivLOGs.txt)

After a freeze a few times: python -c "import torch; torch.tensor([1.0]).cuda(); print('Did it work?')",
I did take a look in the sys log Ubuntu 24.10, it seems that

GPU detected as amdgpu 0000:0a:00.0 (RDNA4 - gfx_v12_0)
VRAM: 16304M recognized correctly
All GPU IP blocks loaded
Kernel mode setting (KFD) initialized
Ring buffers tested and passed
GPU fully initialized: Initialized amdgpu 3.61.0
The issue happens AFTER successful initialization - when actual compute workloads start.
Critical lines:

text
amdgpu 0000:0a:00.0: amdgpu: PCIE atomic ops is not supported
This suggests Thunderbolt limitations in PCIe atomic operations, which ROCm compute heavily relies on.

The problem appears to be Thunderbolt PCIe limitations preventing proper ROCm compute operations, even though basic GPU initialization works fine.

This after installing,

https://download.pytorch.org/whl/nightly/rocm7.1/torch-2.10.0.dev20251118%2Brocm7.1-cp311-cp311-manylinux_2_28_x86_64.whl

More digging:

"ROCm misidentifies RX 9060 XT (RDNA4/gfx1200) as RDNA3/gfx1100, leading to architecture mismatch and system freezes. Also missing OpenCL compiler headers."

This is the Smoking Gun:
The compatibility matrix is wrong - ROCm 7.1 doesn't properly support RDNA4, it just misidentifies the architecture and crashes.

Your hardware works fine - it's ROCm's architecture detection that's broken. ????

---

### 评论 #7 — darren-amd (2025-11-26T14:58:26Z)

Hi @Horus-p,

Could you please try upgrading amdgpu by following the instructions [here](https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/install/detailed-install/package-manager/package-manager-ubuntu.html) and share the outputs of `amd-smi` and `rocminfo`? Also, just to confirm, were you able to upgrade your torch wheels? Could you please also share the output of `pip list | grep torch`? Thanks!

---

### 评论 #8 — Horus-p (2025-11-27T04:46:13Z)

Last report from my "Assistent"

Follow-up Report: RDNA4 Instruction Set Mismatch
Critical New Finding:
GPU successfully wakes from low-power state when compute starts (fans activate)

System freezes during execution, not during wake-up

Evidence of architecture instruction mismatch: ROCm generating RDNA3 (gfx1100) code for RDNA4 (gfx1200) hardware

The Actual Failure Sequence:
✅ GPU power management works (wakes on demand)

✅ GPU is operational and responsive

❌ ROCm sends wrong instruction set (RDNA3 → RDNA4)

❌ Hardware-level crash freezes entire system

Conclusion:
ROCm 7.1's RDNA4 support is fundamentally broken - it compiles for the wrong architecture. The compatibility matrix is incorrect and users should be warned that RDNA4 GPUs will not work properly.

Urgent Need:
Either fix RDNA4 architecture detection or officially document this incompatibility to prevent other users from wasting time and resources.

This clearly shows the problem isn't power management or detection - it's wrong code generation for the actual hardware architecture.

From other forums I see I'm not alone.

"ROCm 7.1 has known installation and compatibility issues affecting multiple users. Evidence shows:
Broken package dependencies preventing clean upgrades
Mixed version installations causing system instability
Working older ROCm versions becoming broken in 7.1
My RDNA4 architecture detection bug is part of this broader ROCm 7.1 quality regression"

Please fix this ASAP 

---

### 评论 #9 — darren-amd (2025-11-27T19:30:53Z)

Hi @Horus-p,

Would you mind providing the information I requested above? It would help me to further debug this issue, thanks!

---

### 评论 #10 — Horus-p (2025-11-28T05:15:22Z)

amd-smi: command not found
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-f8c7e95787a83fef               
  Marketing Name:          AMD Radeon RX 9060 XT              
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
    L2:                      4096(0x1000) KB                    
    L3:                      32768(0x8000) KB                   
  Chip ID:                 30096(0x7590)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2787                               
  BDFID:                   2560                               
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
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
  Packet Processor uCode:: 1012                               
  SDMA engine uCode::      86                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16695296(0xfec000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16695296(0xfec000) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1100         
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
*** Done ***             

torch                   2.10.0.dev20251118+rocm7.1


Tried several test after all this (all freeze), so for what it it is worth
The KFD device exists with correct permissions but ROCm still can't use it. This points to a deep kernel-level compatibility issue between ROCm's KFD and Thunderbolt.

The evidence continues to point toward fundamental incompatibility rather than configuration issues.

[   12.587308] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[   12.587335] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[   12.587600] kfd kfd: amdgpu: added device 1002:7590
KFD initialized successfully! The kernel messages show:

✅ KFD module loaded

✅ GPU detected (1002:7590 = RX 9060 XT)

✅ Memory allocated properly

✅ Device node created

But ROCm userspace still can't open /dev/kfd
This is a userspace/kernel API mismatch - the kernel KFD works, but ROCm's userspace libraries are using the wrong API to talk to it.

The Core Problem:
ROCm 7.1 userspace is incompatible with the KFD kernel module that got loaded, despite both showing version 6.12.12.

This is Unfixable Without AMD:
Kernel KFD works

Hardware works

Permissions work

But ROCm userspace can't communicate with its own kernel component

Final Conclusion:
ROCm 7.1 is fundamentally broken - the userspace and kernel components can't communicate properly, especially in Thunderbolt eGPU configurations.

ROCk module version 6.12.12 is loaded
Unable to open /dev/kfd read-write: Invalid argument

Even ROCm's own diagnostic tool can't access the KFD device that ROCm's own kernel module created.

The Inescapable Conclusion:
ROCm 7.1 is self-incompatible - its userspace tools can't communicate with its own kernel components.

---

### 评论 #11 — darren-amd (2025-12-01T14:59:09Z)

Hi @Horus-p,

Could you confirm if ROCm is installed properly? `amd-smi` should be included with ROCm unless your paths weren't set correctly. As above, could you please try upgrading amdgpu by following the instructions [here](https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/install/detailed-install/package-manager/package-manager-ubuntu.html) and share the full outputs of `apt list | grep rocm`, `amd-smi` and `rocminfo`? Also, just to confirm, were you able to upgrade your torch wheels? Could you please also share the output of pip list | grep torch? Thanks!

---

### 评论 #12 — Horus-p (2025-12-02T12:32:05Z)

As in my last post
amd-smi: command not found

apt list | grep rocm

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

libfcgi-procmanager-maxrequests-perl/plucky,plucky 0.2-1.1 all
libfcgi-procmanager-perl/plucky,plucky 0.28-3 all
librocm-dbgapi0/plucky 5.7.1-2 amd64
librocm-smi-dev/plucky 6.1.2-1 amd64
librocm-smi-dev/plucky 6.1.2-1 i386
librocm-smi64-1/plucky 6.1.2-1 amd64
librocm-smi64-1/plucky 6.1.2-1 i386
librust-profiling-procmacros-dev/plucky 1.0.16-1 amd64
pkg-rocm-tools/plucky,plucky 0.8.2 all
procmail-lib/plucky,plucky 1:2009.1202-6 all
procmail/plucky 3.24-1ubuntu3 amd64
procmeter3/plucky 3.6-3.1build2 amd64
rocm-bandwidth-test-rpath7.1.0/noble 2.6.0.70100-20~24.04 amd64
rocm-bandwidth-test7.1.0/noble 2.6.0.70100-20~24.04 amd64
rocm-bandwidth-test/noble 2.6.0.70100-20~24.04 amd64
rocm-cmake-rpath7.1.0/noble 0.14.0.70100-20~24.04 amd64
rocm-cmake7.1.0/noble 0.14.0.70100-20~24.04 amd64
rocm-cmake/noble 0.14.0.70100-20~24.04 amd64
rocm-core-dbgsym/noble 7.1.0.70100-20~24.04 amd64
rocm-core-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-core7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-core/noble,now 7.1.0.70100-20~24.04 amd64 [installed,automatic]
rocm-dbgapi-dbgsym/noble 0.77.4.70100-20~24.04 amd64
rocm-dbgapi-rpath7.1.0/noble 0.77.4.70100-20~24.04 amd64
rocm-dbgapi7.1.0/noble 0.77.4.70100-20~24.04 amd64
rocm-dbgapi/noble 0.77.4.70100-20~24.04 amd64
rocm-debug-agent-dbgsym/noble 2.1.0.70100-20~24.04 amd64
rocm-debug-agent-rpath7.1.0/noble 2.1.0.70100-20~24.04 amd64
rocm-debug-agent7.1.0/noble 2.1.0.70100-20~24.04 amd64
rocm-debug-agent/noble 2.1.0.70100-20~24.04 amd64
rocm-dev-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-dev7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-dev/noble 7.1.0.70100-20~24.04 amd64
rocm-developer-tools-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-developer-tools7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-developer-tools/noble 7.1.0.70100-20~24.04 amd64
rocm-device-libs-17/plucky 6.0+git20231212.5a852ed-2 amd64
rocm-device-libs-rpath7.1.0/noble 1.0.0.70100-20~24.04 amd64
rocm-device-libs7.1.0/noble 1.0.0.70100-20~24.04 amd64
rocm-device-libs/noble 1.0.0.70100-20~24.04 amd64
rocm-gdb-rpath7.1.0/noble 16.3.70100-20~24.04 amd64
rocm-gdb7.1.0/noble 16.3.70100-20~24.04 amd64
rocm-gdb/noble 16.3.70100-20~24.04 amd64
rocm-hip-libraries-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-hip-libraries7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-hip-libraries/noble,now 7.1.0.70100-20~24.04 amd64 [installed,automatic]
rocm-hip-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-hip-runtime-dev-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-hip-runtime-dev7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-hip-runtime-dev/noble 7.1.0.70100-20~24.04 amd64
rocm-hip-runtime-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-hip-runtime7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-hip-runtime/noble 7.1.0.70100-20~24.04 amd64
rocm-hip-sdk-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-hip-sdk7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-hip-sdk/noble,now 7.1.0.70100-20~24.04 amd64 [installed]
rocm-hip7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-hip/noble 7.1.0.70100-20~24.04 amd64
rocm-language-runtime-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-language-runtime7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-language-runtime/noble 7.1.0.70100-20~24.04 amd64
rocm-libs-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-libs7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-libs/noble 7.1.0.70100-20~24.04 amd64
rocm-llvm-dev-rpath7.1.0/noble 20.0.0.25425.70100-20~24.04 amd64
rocm-llvm-dev7.1.0/noble 20.0.0.25425.70100-20~24.04 amd64
rocm-llvm-dev/noble 20.0.0.25425.70100-20~24.04 amd64
rocm-llvm-docs-rpath7.1.0/noble 20.0.0.25425.70100-20~24.04 amd64
rocm-llvm-docs7.1.0/noble 20.0.0.25425.70100-20~24.04 amd64
rocm-llvm-docs/noble 20.0.0.25425.70100-20~24.04 amd64
rocm-llvm-rpath7.1.0/noble 20.0.0.25425.70100-20~24.04 amd64
rocm-llvm7.1.0/noble 20.0.0.25425.70100-20~24.04 amd64
rocm-llvm/noble 20.0.0.25425.70100-20~24.04 amd64
rocm-ml-libraries-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-ml-libraries7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-ml-libraries/noble 7.1.0.70100-20~24.04 amd64
rocm-ml-sdk-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-ml-sdk7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-ml-sdk/noble 7.1.0.70100-20~24.04 amd64
rocm-ocltst-dbgsym/noble 2.0.0.70100-20~24.04 amd64
rocm-ocltst-rpath7.1.0/noble 2.0.0.70100-20~24.04 amd64
rocm-ocltst7.1.0/noble 2.0.0.70100-20~24.04 amd64
rocm-ocltst/noble 2.0.0.70100-20~24.04 amd64
rocm-opencl-dbgsym/noble 2.0.0.70100-20~24.04 amd64
rocm-opencl-dev-rpath7.1.0/noble 2.0.0.70100-20~24.04 amd64
rocm-opencl-dev7.1.0/noble 2.0.0.70100-20~24.04 amd64
rocm-opencl-dev/noble 2.0.0.70100-20~24.04 amd64
rocm-opencl-icd/plucky 5.7.1-5build1 amd64
rocm-opencl-rpath7.1.0/noble 2.0.0.70100-20~24.04 amd64
rocm-opencl-runtime-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-opencl-runtime7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-opencl-runtime/noble 7.1.0.70100-20~24.04 amd64
rocm-opencl-sdk-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-opencl-sdk7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-opencl-sdk/noble 7.1.0.70100-20~24.04 amd64
rocm-opencl7.1.0/noble 2.0.0.70100-20~24.04 amd64
rocm-opencl/noble 2.0.0.70100-20~24.04 amd64
rocm-openmp-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-openmp-sdk-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-openmp-sdk7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-openmp-sdk/noble 7.1.0.70100-20~24.04 amd64
rocm-openmp7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-openmp/noble 7.1.0.70100-20~24.04 amd64
rocm-podman-support/plucky,plucky 0.8.2 all
rocm-qemu-support/plucky,plucky 0.8.2 all
rocm-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-smi-lib-dbgsym/noble 7.8.0.70100-20~24.04 amd64
rocm-smi-lib-rpath7.1.0/noble 7.8.0.70100-20~24.04 amd64
rocm-smi-lib7.1.0/noble 7.8.0.70100-20~24.04 amd64
rocm-smi-lib/noble,now 7.8.0.70100-20~24.04 amd64 [installed]
rocm-smi/plucky 6.1.2-1 amd64
rocm-smi/plucky 6.1.2-1 i386
rocm-utils-rpath7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-utils7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm-utils/noble 7.1.0.70100-20~24.04 amd64
rocm-validation-suite-rpath7.1.0/noble 1.2.0.70100-20~24.04 amd64
rocm-validation-suite7.1.0/noble 1.2.0.70100-20~24.04 amd64
rocm-validation-suite/noble 1.2.0.70100-20~24.04 amd64
rocm7.1.0/noble 7.1.0.70100-20~24.04 amd64
rocm/noble 7.1.0.70100-20~24.04 amd64
rocminfo-dbgsym/noble 1.0.0.70100-20~24.04 amd64
rocminfo-rpath7.1.0/noble 1.0.0.70100-20~24.04 amd64
rocminfo7.1.0/noble 1.0.0.70100-20~24.04 amd64
rocminfo/noble,now 1.0.0.70100-20~24.04 amd64 [installed,automatic]

as described in my last post

rocminfo
ROCk module version 6.12.12 is loaded
Unable to open /dev/kfd read-write: Invalid argument
nix is member of video group

to upgrade your torch wheels //
_ guess the one nightly was the last version?
Is installed_

---

### 评论 #13 — darren-amd (2025-12-02T15:03:33Z)

It looks like your system cannot find `amd-smi`, please try looking into the `bin` folder in rocm for `amd-smi`. Also, did you follow the guide to upgrade amdgpu? Please confirm the output of `apt list | grep amdgpu`. Also are you in a container of some sort? `rocminfo` does not appear to be working on your machine either. Another thing I am seeing is:
```
Name: gfx1100
Uuid: GPU-f8c7e95787a83fef
Marketing Name: AMD Radeon RX 9060 XT
```
Did you override this yourself? 

---

### 评论 #14 — darren-amd (2025-12-02T19:37:36Z)

Also to add on, could you try one of our PyTorch docker containers available [here](https://hub.docker.com/layers/rocm/pytorch/latest/images/sha256-683765a52c61341e1674fe730ab3be861a444a45a36c0a8caae7653a08a0e208)? It should help us to rule out issues related specifically to your environment.

---

### 评论 #15 — Horus-p (2025-12-03T10:19:23Z)

Hi Darren, I feel I answered these questions in my last post. I have no other result now and are hesitant after downloading 20 GB of trials to play around and test, when it seems clear that installing official packages are missing parts?

Summary of ROCm 7.1 Installation Issues:
1. Missing/Broken Components:
amd-smi command doesn't exist - only rocm-smi exists and it's a broken symlink

Missing Python files: /opt/rocm/libexec/rocm_smi/rocm_smi.py doesn't exist (symlink target)

Missing Python module: rocm_smi module not installed despite rocm-smi-lib package being installed

2. Current State:
bash
# Broken rocm-smi symlink
$ ls -la /opt/rocm/bin/rocm-smi
lrwxrwxrwx 1 root root 31 Oct 25 03:31 /opt/rocm/bin/rocm-smi -> ../libexec/rocm_smi/rocm_smi.py

# Missing target file
$ ls -la /opt/rocm/libexec/rocm_smi/
total 8
drwxr-xr-x 2 root root 4096 Nov 28 12:54 .
drwxr-xr-x 3 root root 4096 Nov 28 12:54 ..
-rw-r--r-- 1 root root    0 Nov 28 12:54 __init__.py  # Empty file!

# Missing Python module
$ python3 -c "import rocm_smi"
ModuleNotFoundError: No module named 'rocm_smi'
3. Architecture Detection (Now Fixed):
Initially: ROCm 7.1 incorrectly detected RDNA4 RX 9060 XT as gfx1100 (RDNA3)

After clean reinstall: Now correctly detects as gfx1200 (RDNA4)

No manual overrides - this was a ROCm bug

4. Core Incompatibility:
bash
$ /opt/rocm/bin/rocminfo
ROCk module version 6.12.12 is loaded
Unable to open /dev/kfd read-write: Invalid argument
nix is member of video group
/dev/kfd exists with correct permissions (crw-rw----+, ACL allows user access)

User is in video, render, and kfd groups

But ROCm's own tool (rocminfo) cannot access ROCm's own kernel device

5. System Freezes Persist:
Even with correct architecture detection, any PyTorch GPU operation causes system freeze:

bash
python -c "import torch; torch.tensor([1.0]).cuda()"  # System freezes
6. Environment Details:
Bare metal Ubuntu 25 (development branch), not a container

Dell Latitude 7480 + Thunderbolt 3 + HexaSoul Nano G3 dock

AMD RX 9060 XT (RDNA4)

Kernel: 6.14.0-36-generic

Docker/containerd present but no containers running (could be interfering with device access)

7. Installation Attempts:
Followed official ROCm 7.1 installation guide

Clean reinstall with apt remove --purge rocm-* and reinstall

Verified AMDGPU DKMS packages installed (amdgpu-dkms, amdgpu-dkms-firmware)

Multiple reboots after group changes and driver installations

---

### 评论 #16 — darren-amd (2025-12-03T15:15:19Z)

Hi @Horus-p,

We do not currently support Ubuntu 25, I'd recommend installing one of our supported OS's by consulting our [compatibility matrix](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#compatibility-matrix), and if the issue persists please feel free to create a new ticket. Thanks!



---
