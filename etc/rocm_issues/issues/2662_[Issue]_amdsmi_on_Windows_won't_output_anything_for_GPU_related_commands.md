# [Issue]: amdsmi on Windows won't output anything for GPU related commands

> **Issue #2662**
> **状态**: closed
> **创建时间**: 2023-11-22T17:35:06Z
> **更新时间**: 2024-10-01T19:15:51Z
> **关闭时间**: 2024-10-01T19:15:51Z
> **作者**: NeedsMoar
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2662

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

amdsmi.exe on windows won't report any information.

### Operating System

Microsoft Windows 10 Pro for Workstations 10.0.19045 N/A Build 19045

### CPU

AMD Ryzen Threadripper PRO 5975WX 32-Cores

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

5.5.0 (Windows)

### ROCm Component

amdsmi

### Steps to Reproduce

Run amdsmi with any command.  Only ill-formatted commands, no input (help) or errors due to OS type / host / baremetal related to command context display.  
list and all other commands show nothing. I attempted to plug in the GPU number (0 according to hipinfo and common sense) and same nothing. 
Output to file also fails. This happened before and after I installed a 4090 as well;  it is currently the card being used for both connected displays until I get time to switch those and test the cuda-only mode drivers for the 4090 and see if speed gains are  worth the hassle of restricting that card's features,  so the 7900xtx is headless.  nvidia-smi works fine.  I haven't seen any driver conflicts between the two. 

### Output of /opt/rocm/bin/rocminfo --support

Windows doen't have rocminfo and the support flag doesn't seem to work on hipinfo, but:

hipinfo

--------------------------------------------------------------------------------
device#                           0
Name:                             AMD Radeon RX 7900 XTX
pciBusID:                         35
pciDeviceID:                      0
pciDomainID:                      0
multiProcessorCount:              48
maxThreadsPerMultiProcessor:      2048
isMultiGpuBoard:                  0
clockRate:                        2526 Mhz
memoryClockRate:                  1250 Mhz
memoryBusWidth:                   0
totalGlobalMem:                   23.98 GB
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
peers:
non-peers:                        device#0

memInfo.total:                    23.98 GB
memInfo.free:                     23.86 GB (99%)

Additional info:
Memory: 512GB (8x64GB) 3200MHz ECC RDIMMs  
Driver Version
23.20.17.03-231016a-396906C-AMD-Software-Adrenalin-Edition
Resizable bar is on gpu-z reports:
BAR0	32768 MB
BAR1	256 MB

as expected.  Device manager shows no conflicts.  
NUMA is setup as single node right now but I could flip on L3 as SRAT to get things onto 4 nodes if that's some suspected issue (don't know why it would be but hey).  IOMMU is off.


---

## 评论 (4 条)

### 评论 #1 — NeedsMoar (2023-12-10T13:13:34Z)

I ran this on my other machine which has updated drivers which included amdsmi but no system python, and it apparently tried to call out to the windows python installer stand-in executable and crashed.   Is this one of those py2exe type wrappers that's not bundled with all of the libs it needs?

---

### 评论 #2 — NeedsMoar (2023-12-21T06:42:59Z)

Recently switched to python311 as system python, rather than absolutely nothing I got this:

```cmd
C:\>amdsmi
Traceback (most recent call last):
  File "PyInstaller\loader\pyimod03_ctypes.py", line 53, in __init__
  File "ctypes\__init__.py", line 376, in __init__
FileNotFoundError: Could not find module 'libsmi_guest.dll' (or one of its dependencies). Try using the full path with constructor syntax.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "main.py", line 25, in <module>
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller\loader\pyimod02_importers.py", line 352, in exec_module
  File "exceptions.py", line 22, in <module>
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller\loader\pyimod02_importers.py", line 352, in exec_module
  File "amdsmi_import\__init__.py", line 83, in <module>
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller\loader\pyimod02_importers.py", line 352, in exec_module
  File "amdsmi_import\amdsmi_baremetal\gpuvsmi_package\amdsmi\__init__.py", line 24, in <module>
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller\loader\pyimod02_importers.py", line 352, in exec_module
  File "amdsmi_import\amdsmi_baremetal\gpuvsmi_package\amdsmi\smi_interface.py", line 29, in <module>
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller\loader\pyimod02_importers.py", line 352, in exec_module
  File "amdsmi_import\amdsmi_baremetal\gpuvsmi_package\amdsmi\smi_wrapper.py", line 152, in <module>
  File "PyInstaller\loader\pyimod03_ctypes.py", line 55, in __init__
pyimod03_ctypes.install.<locals>.PyInstallerImportError: Failed to load dynlib/dll 'libsmi_guest.dll'. Most likely this dynlib/dll was not found when the application was frozen.
[20348] Failed to execute script 'main' due to unhandled exception!

I'm not sure where this would have come from since the installer for HIP didn't put it in either python's lib directory 

---

### 评论 #3 — harkgill-amd (2024-06-18T15:13:56Z)

Hi @NeedsMoar, an internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #4 — harkgill-amd (2024-10-01T19:15:51Z)

@NeedsMoar, amdsmi for Windows does not currently support consumer cards such as the 7900XTX. There are plans to improve support in the future though in the meantime, it will be removed as part of the installation. 

---
