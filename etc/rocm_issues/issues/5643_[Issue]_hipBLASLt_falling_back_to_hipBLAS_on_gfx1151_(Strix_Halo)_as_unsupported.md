# [Issue]: hipBLASLt falling back to hipBLAS on gfx1151 (Strix Halo) as unsupported architecture

> **Issue #5643**
> **状态**: closed
> **创建时间**: 2025-11-08T05:39:40Z
> **更新时间**: 2025-11-10T23:53:49Z
> **关闭时间**: 2025-11-10T23:53:49Z
> **作者**: ianbmacdonald
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5643

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

In Ubuntu 24.04 with current ROCm 7.1 the Lt fastpath is not working on the gfx1151 with an `unsupported architecture!` error in the test shown below.

```
(rocm71) imac@ai2:~/src/rocm71$ export PYTORCH_ROCM_ARCH='gfx1151'
(rocm71) imac@ai2:~/src/rocm71$ export LD_LIBRARY_PATH=/opt/rocm/lib:/opt/rocm/lib64
(rocm71) imac@ai2:~/src/rocm71$ export TORCH_BLAS_PREFER_HIPBLASLT=1
(rocm71) imac@ai2:~/src/rocm71$ uv pip list
Package           Version
----------------- ------------------------------
filelock          3.20.0
fsspec            2025.10.0
jinja2            3.1.6
markupsafe        3.0.3
mpmath            1.3.0
networkx          3.5
numpy             2.3.4
setuptools        80.9.0
sympy             1.14.0
torch             2.8.0+rocm7.1.0.lw.git7a520360
triton            3.4.0+rocm7.1.0.gitf9e5bf54
typing-extensions 4.15.0
(rocm71) imac@ai2:~/src/rocm71$ python - <<'PY'
import torch, time
def bench():
    A = torch.randn(4096,4096, device="cuda")
    B = torch.randn(4096,4096, device="cuda")
    torch.cuda.synchronize()
    t=time.time(); C = A@B; torch.cuda.synchronize()
    print("GEMM ms:", (time.time()-t)*1e3)
bench()
PY
<stdin>:6: UserWarning: Attempting to use hipBLASLt on an unsupported architecture! Overriding blas backend to hipblas (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:373.)
GEMM ms: 60.364484786987305

```

```
(rocm71) imac@ai2:~/src/rocm71$ sudo cat /sys/kernel/debug/dri/1/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080
(rocm71) imac@ai2:~/src/rocm71$ modinfo amdgpu | head -n3
filename:       /lib/modules/6.14.0-1015-oem/updates/dkms/amdgpu.ko.zst
version:        6.16.6
license:        GPL and additional rights

```


```
OS:
NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"
CPU: 
model name	: AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
GPU:
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151                            
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx1151         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
  Name:                    aie2                               
  Marketing Name:          AIE-ML  
```

### Operating System

Ubuntu 24.04

### CPU

Strix Halo

### GPU

gfx1151

### ROCm Version

7.1

### ROCm Component

hipBLASLt

### Steps to Reproduce

Spawn a Python 3.12 venv 

```
imac@ai2:~/src$ cd rocm71/
imac@ai2:~/src/rocm71$ uv init --python 3.12
Initialized project `rocm71`
imac@ai2:~/src/rocm71$ source .venv/bin/activate

```
Download the current pre-built ROCm 7.1 pytorch wheels and some dependencies

```
(rocm71) imac@ai2:~/src/rocm71$ source .venv/bin/activate
(rocm71) imac@ai2:~/src/rocm71$ wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.1/triton-3.4.0%2Brocm7.1.0.gitf9e5bf54-cp312-cp312-linux_x86_64.whl
(rocm71) imac@ai2:~/src/rocm71$ wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.1/torch-2.8.0%2Brocm7.1.0.lw.git7a520360-cp312-cp312-linux_x86_64.whl
(rocm71) imac@ai2:~/src/rocm71$ uv add ./triton-3.4.0+rocm7.1.0.gitf9e5bf54-cp312-cp312-linux_x86_64.whl
(rocm71) imac@ai2:~/src/rocm71$ uv add ./torch-2.8.0+rocm7.1.0.lw.git7a520360-cp312-cp312-linux_x86_64.whl
(rocm71) imac@ai2:~/src/rocm71$ uv add numpy
```
Run the test as described above


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
(rocm71) imac@ai2:~/src/rocm71$ amd-smi
+------------------------------------------------------------------------------+
| AMD-SMI 26.1.0+5df6c765      amdgpu version: 6.16.6   ROCm version: 7.1.0    |
| VBIOS version: 00107962                                                      |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:c5:00.0    AMD Radeon Graphics | N/A        N/A   0             N/A/0 W |
|   0       0     N/A             N/A | N/A        N/A              161/512 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
(rocm71) imac@ai2:~/src/rocm71$ rocminfo 
ROCk module version 6.16.6 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.14
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
      Size:                    131009792(0x7cf0d00) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131009792(0x7cf0d00) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131009792(0x7cf0d00) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131009792(0x7cf0d00) KB            
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
  Marketing Name:          AMD Radeon Graphics                
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
  SDMA engine uCode::      17                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    125829120(0x7800000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    125829120(0x7800000) KB            
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
  Name:                    aie2                               
  Uuid:                    AIE-XX                             
  Marketing Name:          AIE-ML                             
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
      Size:                    131009792(0x7cf0d00) KB            
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
      Size:                    131009792(0x7cf0d00) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***            
``` 


### Additional Information

The same test works fine on gfx1100 but the HIPBlastLt was slower than HIPBlas. 

I am wondering if this is related to https://github.com/ROCm/ROCm/issues/5344 and also applies to gfx11  (warmed up the gap widens to ~9x)

```
(rocm71) imac@ai3-debian:/mnt/cache/src/rocm71$ export TORCH_BLAS_PREFER_HIPBLASLT=1
(rocm71) imac@ai3-debian:/mnt/cache/src/rocm71$ python - <<'PY'
import torch, time
def bench():
    A = torch.randn(4096,4096, device="cuda")
    B = torch.randn(4096,4096, device="cuda")
    torch.cuda.synchronize()
    t=time.time(); C = A@B; torch.cuda.synchronize()
    print("GEMM ms:", (time.time()-t)*1e3)
bench()
PY
GEMM ms: 194.48208808898926
(rocm71) imac@ai3-debian:/mnt/cache/src/rocm71$ export TORCH_BLAS_PREFER_HIPBLASLT=0
(rocm71) imac@ai3-debian:/mnt/cache/src/rocm71$ python - <<'PY'
import torch, time
def bench():
    A = torch.randn(4096,4096, device="cuda")
    B = torch.randn(4096,4096, device="cuda")
    torch.cuda.synchronize()
    t=time.time(); C = A@B; torch.cuda.synchronize()
    print("GEMM ms:", (time.time()-t)*1e3)
bench()
PY
GEMM ms: 115.24629592895508
(rocm71) imac@ai3-debian:/mnt/cache/src/rocm71$ rocm-smi --showperflevel --showclocks


============================ ROCm System Management Interface ============================
WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status

=============================== Current clock frequencies ================================
GPU[0]		: dcefclk clock level: 1: (200Mhz)
GPU[0]		: fclk clock level: 7: (2301Mhz)
GPU[0]		: mclk clock level: 3: (1249Mhz)
GPU[0]		: sclk clock level: 1: (6Mhz)
GPU[0]		: socclk clock level: 1: (1500Mhz)
GPU[0]		: pcie clock level: 0 (8.0GT/s x16)
==========================================================================================
================================= Show Performance Level =================================
GPU[0]		: Performance Level: high
==========================================================================================
================================== End of ROCm SMI Log ===================================
(rocm71) imac@ai3-debian:/mnt/cache/src/rocm71$ amd-smi 
+------------------------------------------------------------------------------+
| AMD-SMI 26.1.0+5df6c765      amdgpu version: Linuxver ROCm version: 7.1.0    |
| VBIOS version: 022.001.002.031.000001                                        |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:03:00.0 AMD Radeon RX 7900 XTX | 0 %      35 °C   0            14/327 W |
|   0       0     N/A             N/A | 0 %      0.0 %             40/24560 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+

```

---

## 评论 (3 条)

### 评论 #1 — tcgu-amd (2025-11-10T18:59:31Z)

Hi @ianbmacdonald which version of PyTorch are you using? 

`gfx1151` was added in a recent commit https://github.com/pytorch/pytorch/commit/44a5d419935a77b3308f247279a457e6d0b9a292. It did not make it into the 2.9 release afaik. 

---

### 评论 #2 — ianbmacdonald (2025-11-10T20:55:36Z)

Cherry picking that into the 2.9 release, there still appears to be a speed regression.

```
(vllm_11) imac@ai2:/mnt/models/src/vllm_11$ export TORCH_BLAS_PREFER_HIPBLASLT=1
(vllm_11) imac@ai2:/mnt/models/src/vllm_11$ python - <<'PY'
import torch
M=K=N=4096
A = torch.randn(M,K, device="cuda")
B = torch.randn(K,N, device="cuda")

# one warm-up to build context & pick kernels
(A@B).sum().item()
torch.cuda.synchronize()

start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)

start.record()
C = A @ B
end.record()
torch.cuda.synchronize()
print("GPU ms:", start.elapsed_time(end))
PY
GPU ms: 149.57565307617188
(vllm_11) imac@ai2:/mnt/models/src/vllm_11$ export TORCH_BLAS_PREFER_HIPBLASLT=0
(vllm_11) imac@ai2:/mnt/models/src/vllm_11$ python - <<'PY'
import torch
M=K=N=4096
A = torch.randn(M,K, device="cuda")
B = torch.randn(K,N, device="cuda")

# one warm-up to build context & pick kernels
(A@B).sum().item()
torch.cuda.synchronize()

start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)

start.record()
C = A @ B
end.record()
torch.cuda.synchronize()
print("GPU ms:", start.elapsed_time(end))
PY
GPU ms: 47.21492385864258

```

---

### 评论 #3 — ianbmacdonald (2025-11-10T23:53:49Z)

I reproduced this on `torch 2.9.0+git7e899b7` created using the following

```
git switch -c r29_local origin/release/2.9_aiter_update
git -c submodule.recurse=false fetch https://github.com/pytorch/pytorch.git pull/164744/head:pr-164744
git cherry-pick -x ea8c7885ce6e5a525a451269ef55defae32232e0 93253201b822fac30d10fcf7820c8073a7399b6a ccf163a44639a9ae2d83e0ac8ce8e54283848faf
git submodule sync --recursive
git submodule update --init --recursive
uv pip install -r requirements.txt
python tools/amd_build/build_amd.py
python setup.py bdist_wheel
```



---
