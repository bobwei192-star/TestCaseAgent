# [Issue]: rocm-smi 6.4.1 shows "N/A" for most partition related values (MI300A, MI300X)

> **Issue #4759**
> **状态**: open
> **创建时间**: 2025-05-21T13:13:29Z
> **更新时间**: 2025-12-24T07:51:58Z
> **作者**: maxweiss
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4759

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

ROCm 6.4.1 was installed with this installer: https://repo.radeon.com/amdgpu-install/6.4.1/ubuntu/noble/amdgpu-install_6.4.60401-1_all.deb.

The CLI shows "N/A" for most of the partition related values.
The rocm-smi API seems to have the same problem. For example, `rsmi_dev_name_get()` returns RSMI_STATUS_SUCCESS for the GPU itself (partition 0), but RSMI_STATUS_NOT_SUPPORTED for all other partitions. 

MI300A:

```
$ amd-smi version
AMDSMI Tool: 25.4.2+aca1101 | AMDSMI Library version: 25.4.0 | ROCm version: 6.4.1 | amdgpu version: 6.10.5 | amd_hsmp version: N/A

$ rocm-smi -i


============================ ROCm System Management Interface ============================
=========================================== ID ===========================================
GPU[0]		: Device Name: 		AMD Instinct MI300A
GPU[0]		: Device ID: 		0x74a0
GPU[0]		: Device Rev: 		0x00
GPU[0]		: Subsystem ID: 	0x74a0
GPU[0]		: GUID: 		39408
GPU[1]		: Device Name: 		AMD Instinct MI300A
GPU[1]		: Device ID: 		N/A
GPU[1]		: Device Rev: 		N/A
GPU[1]		: Subsystem ID: 	N/A
GPU[1]		: GUID: 		8689
GPU[2]		: Device Name: 		AMD Instinct MI300A
GPU[2]		: Device ID: 		N/A
GPU[2]		: Device Rev: 		N/A
GPU[2]		: Subsystem ID: 	N/A
GPU[2]		: GUID: 		43505
==========================================================================================
================================== End of ROCm SMI Log ===================================
$ rocm-smi


============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK   MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                  
==========================================================================================================================
0       1     0x74a0,   39408  30.0°C      120.0W    NPS1, TPX, 0        94Mhz  1300Mhz  0%   auto  550.0W  0%     0%    
1       2     N/A,      8689   N/A         N/A       N/A, N/A, 1         N/A    N/A      0%   n/a   N/A     0%     N/A   
2       3     N/A,      43505  N/A         N/A       N/A, N/A, 2         N/A    N/A      0%   n/a   N/A     0%     N/A   
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================
```

MI300X:

```
$ amd-smi version
AMDSMI Tool: 25.4.2+aca1101 | AMDSMI Library version: 25.4.0 | ROCm version: 6.4.1 | amdgpu version: 6.10.5 | amd_hsmp version: N/A

$ rocm-smi -i


============================ ROCm System Management Interface ============================
=========================================== ID ===========================================
GPU[0]		: Device Name: 		AMD Instinct MI300X
GPU[0]		: Device ID: 		0x74a1
GPU[0]		: Device Rev: 		0x00
GPU[0]		: Subsystem ID: 	0x74a1
GPU[0]		: GUID: 		10931
GPU[1]		: Device Name: 		AMD Instinct MI300X
GPU[1]		: Device ID: 		N/A
GPU[1]		: Device Rev: 		N/A
GPU[1]		: Subsystem ID: 	N/A
GPU[1]		: GUID: 		6834
GPU[2]		: Device Name: 		AMD Instinct MI300X
GPU[2]		: Device ID: 		0x74a1
GPU[2]		: Device Rev: 		0x00
GPU[2]		: Subsystem ID: 	0x74a1
GPU[2]		: GUID: 		62122
GPU[3]		: Device Name: 		AMD Instinct MI300X
GPU[3]		: Device ID: 		N/A
GPU[3]		: Device Rev: 		N/A
GPU[3]		: Subsystem ID: 	N/A
GPU[3]		: GUID: 		49835
GPU[4]		: Device Name: 		AMD Instinct MI300X
GPU[4]		: Device ID: 		0x74a1
GPU[4]		: Device Rev: 		0x00
GPU[4]		: Subsystem ID: 	0x74a1
GPU[4]		: GUID: 		55938
GPU[5]		: Device Name: 		AMD Instinct MI300X
GPU[5]		: Device ID: 		N/A
GPU[5]		: Device Rev: 		N/A
GPU[5]		: Subsystem ID: 	N/A
GPU[5]		: GUID: 		60035
GPU[6]		: Device Name: 		AMD Instinct MI300X
GPU[6]		: Device ID: 		0x74a1
GPU[6]		: Device Rev: 		0x00
GPU[6]		: Subsystem ID: 	0x74a1
GPU[6]		: GUID: 		667
GPU[7]		: Device Name: 		AMD Instinct MI300X
GPU[7]		: Device ID: 		N/A
GPU[7]		: Device Rev: 		N/A
GPU[7]		: Subsystem ID: 	N/A
GPU[7]		: GUID: 		12954
GPU[8]		: Device Name: 		AMD Instinct MI300X
GPU[8]		: Device ID: 		0x74a1
GPU[8]		: Device Rev: 		0x00
GPU[8]		: Subsystem ID: 	0x74a1
GPU[8]		: GUID: 		35538
GPU[9]		: Device Name: 		AMD Instinct MI300X
GPU[9]		: Device ID: 		N/A
GPU[9]		: Device Rev: 		N/A
GPU[9]		: Subsystem ID: 	N/A
GPU[9]		: GUID: 		47827
GPU[10]		: Device Name: 		AMD Instinct MI300X
GPU[10]		: Device ID: 		0x74a1
GPU[10]		: Device Rev: 		0x00
GPU[10]		: Subsystem ID: 	0x74a1
GPU[10]		: GUID: 		21195
GPU[11]		: Device Name: 		AMD Instinct MI300X
GPU[11]		: Device ID: 		N/A
GPU[11]		: Device Rev: 		N/A
GPU[11]		: Subsystem ID: 	N/A
GPU[11]		: GUID: 		25290
GPU[12]		: Device Name: 		AMD Instinct MI300X
GPU[12]		: Device ID: 		0x74a1
GPU[12]		: Device Rev: 		0x00
GPU[12]		: Subsystem ID: 	0x74a1
GPU[12]		: GUID: 		31459
GPU[13]		: Device Name: 		AMD Instinct MI300X
GPU[13]		: Device ID: 		N/A
GPU[13]		: Device Rev: 		N/A
GPU[13]		: Subsystem ID: 	N/A
GPU[13]		: GUID: 		19170
GPU[14]		: Device Name: 		AMD Instinct MI300X
GPU[14]		: Device ID: 		0x74a1
GPU[14]		: Device Rev: 		0x00
GPU[14]		: Subsystem ID: 	0x74a1
GPU[14]		: GUID: 		41722
GPU[15]		: Device Name: 		AMD Instinct MI300X
GPU[15]		: Device ID: 		N/A
GPU[15]		: Device Rev: 		N/A
GPU[15]		: Subsystem ID: 	N/A
GPU[15]		: GUID: 		37627
==========================================================================================
================================== End of ROCm SMI Log ===================================

$ rocm-smi


============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK    MCLK    Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                  
==========================================================================================================================
0       2     0x74a1,   10931  48.0°C      135.0W    NPS1, DPX, 0        124Mhz  900Mhz  0%   auto  750.0W  0%     0%    
1       3     N/A,      6834   N/A         N/A       N/A, N/A, 1         N/A     N/A     0%   n/a   N/A     0%     N/A   
2       4     0x74a1,   62122  43.0°C      131.0W    NPS1, DPX, 0        124Mhz  900Mhz  0%   auto  750.0W  0%     0%    
3       5     N/A,      49835  N/A         N/A       N/A, N/A, 1         N/A     N/A     0%   n/a   N/A     0%     N/A   
4       6     0x74a1,   55938  47.0°C      137.0W    NPS1, DPX, 0        124Mhz  900Mhz  0%   auto  750.0W  0%     0%    
5       7     N/A,      60035  N/A         N/A       N/A, N/A, 1         N/A     N/A     0%   n/a   N/A     0%     N/A   
6       8     0x74a1,   667    41.0°C      133.0W    NPS1, DPX, 0        124Mhz  900Mhz  0%   auto  750.0W  0%     0%    
7       9     N/A,      12954  N/A         N/A       N/A, N/A, 1         N/A     N/A     0%   n/a   N/A     0%     N/A   
8       10    0x74a1,   35538  46.0°C      138.0W    NPS1, DPX, 0        124Mhz  900Mhz  0%   auto  750.0W  0%     0%    
9       11    N/A,      47827  N/A         N/A       N/A, N/A, 1         N/A     N/A     0%   n/a   N/A     0%     N/A   
10      12    0x74a1,   21195  41.0°C      133.0W    NPS1, DPX, 0        123Mhz  900Mhz  0%   auto  750.0W  0%     0%    
11      13    N/A,      25290  N/A         N/A       N/A, N/A, 1         N/A     N/A     0%   n/a   N/A     0%     N/A   
12      14    0x74a1,   31459  47.0°C      133.0W    NPS1, DPX, 0        124Mhz  900Mhz  0%   auto  750.0W  0%     0%    
13      15    N/A,      19170  N/A         N/A       N/A, N/A, 1         N/A     N/A     0%   n/a   N/A     0%     N/A   
14      16    0x74a1,   41722  44.0°C      135.0W    NPS1, DPX, 0        124Mhz  900Mhz  0%   auto  750.0W  0%     0%    
15      17    N/A,      37627  N/A         N/A       N/A, N/A, 1         N/A     N/A     0%   n/a   N/A     0%     N/A   
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================
```

### Operating System

Ubuntu 24.04

### CPU

AMD EPYC 9654 96-Core

### GPU

AMD Instinct MI300X, AMD Instinct MI300A

### ROCm Version

ROCm 6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — maxweiss (2025-05-21T13:16:35Z)

ROCm 6.4.0 works fine:

```
$ amd-smi version
AMDSMI Tool: 25.3.0+ede62f2 | AMDSMI Library version: 25.3.0 | ROCm version: 6.4.0 | amdgpu version: 6.10.5 | amd_hsmp version: N/A
$ rocm-smi -i


============================ ROCm System Management Interface ============================
=========================================== ID ===========================================
GPU[0]		: Device Name: 		AMD Instinct MI300A
GPU[0]		: Device ID: 		0x74a0
GPU[0]		: Device Rev: 		0x00
GPU[0]		: Subsystem ID: 	0x74a0
GPU[0]		: GUID: 		39408
GPU[1]		: Device Name: 		AMD Instinct MI300A
GPU[1]		: Device ID: 		0x74a0
GPU[1]		: Device Rev: 		0x00
GPU[1]		: Subsystem ID: 	0x74a0
GPU[1]		: GUID: 		8689
GPU[2]		: Device Name: 		AMD Instinct MI300A
GPU[2]		: Device ID: 		0x74a0
GPU[2]		: Device Rev: 		0x00
GPU[2]		: Subsystem ID: 	0x74a0
GPU[2]		: GUID: 		43505
==========================================================================================
================================== End of ROCm SMI Log ===================================
$ rocm-smi   


============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK    MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                   
==========================================================================================================================
0       1     0x74a0,   39408  30.0°C      117.0W    NPS1, TPX, 0        94Mhz   1300Mhz  0%   auto  550.0W  0%     0%    
1       2     0x74a0,   8689   30.0°C      118.0W    NPS1, TPX, 1        108Mhz  1300Mhz  0%   auto  550.0W  0%     0%    
2       3     0x74a0,   43505  30.0°C      118.0W    NPS1, TPX, 2        108Mhz  1300Mhz  0%   auto  550.0W  0%     0%    
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================
```

---

### 评论 #2 — ppanchad-amd (2025-05-26T14:46:07Z)

Hi @maxweiss. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — harkgill-amd (2025-07-02T18:32:46Z)

Hi @maxweiss, this is to be expected with the changes highlighted in https://github.com/ROCm/rocm_smi_lib/blob/amd-staging/CHANGELOG.md#resolved-issues-1.

>  Previously, partitions incorrectly reflected the primary node (1st GPU) and showed the DRM Render Minor as renderD128. Partition nodes mirrored renderD128's information, which was incorrect.

In ROCm 6.4.0, the partitions would essentially copy information from the primary partition which was incorrect. This has been fixed in the 6.4.1 release but as the partitions don't have their own metric files, they display N/A values when amd-smi queries them. We're working towards adding in new per partition metrics that will replace _N/A_ with the correct values. 

---

### 评论 #4 — ctiml (2025-12-24T07:51:58Z)

Hi, I have the same issue in ROCm 7.1.1. Looking forward to this issue being resolved :)

---
