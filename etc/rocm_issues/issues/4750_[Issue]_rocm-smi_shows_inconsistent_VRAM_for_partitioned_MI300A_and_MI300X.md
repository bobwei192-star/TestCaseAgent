# [Issue]: rocm-smi shows inconsistent VRAM for partitioned MI300A and MI300X

> **Issue #4750**
> **状态**: closed
> **创建时间**: 2025-05-17T06:36:43Z
> **更新时间**: 2025-05-21T19:35:32Z
> **关闭时间**: 2025-05-21T19:35:31Z
> **作者**: maxweiss
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4750

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

When a MI300A is in a non-SPX mode, rocm-smi shows the memory of each individual partition as `<total_gpu_memory>/<number_of_partitions>`.
When a MI300X is in a non-SPX mode, rocm-smi shows the memory of each individual partition as `<total_gpu_memory>`.

The same happens with amd-smi and when we use the rocm/amd-smi API directly.
I've tried various modes (even NPS4 on the MI300X) and ROCm 6.3 - 6.4.

Is this expected? Or is it a bug?

MI300A SPX mode:

```
$ amd-smi version
AMDSMI Tool: 24.7.1+8dc45db | AMDSMI Library version: 25.1.0.0 | ROCm version: 6.3.3

$ rocm-smi -i


============================ ROCm System Management Interface ============================
=========================================== ID ===========================================
GPU[0]		: Device Name: 		AMD Instinct MI300A
GPU[0]		: Device ID: 		0x74a0
GPU[0]		: Device Rev: 		0x00
GPU[0]		: Subsystem ID: 	0x74a0
GPU[0]		: GUID: 		32223
==========================================================================================
================================== End of ROCm SMI Log ===================================

$ rocm-smi


============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK   MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                  
==========================================================================================================================
0       1     0x74a0,   32223  32.0°C      127.0W    NPS1, SPX, 0        95Mhz  1300Mhz  0%   auto  550.0W  0%     0%    
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================


$ rocm-smi --showmeminfo vram


============================ ROCm System Management Interface ============================
================================== Memory Usage (Bytes) ==================================
GPU[0]		: VRAM Total Memory (B): 100742320128
GPU[0]		: VRAM Total Used Memory (B): 8388608
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

MI300A TPX mode:

```
$ rocm-smi


============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK    MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                   
==========================================================================================================================
0       1     0x74a0,   39408  32.0°C      125.0W    NPS1, TPX, 0        94Mhz   1300Mhz  0%   auto  550.0W  0%     0%    
1       2     0x74a0,   8689   32.0°C      125.0W    NPS1, TPX, 1        95Mhz   1300Mhz  0%   auto  550.0W  0%     0%    
2       3     0x74a0,   43505  32.0°C      125.0W    NPS1, TPX, 2        100Mhz  1300Mhz  0%   auto  550.0W  0%     0%    
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================


$ rocm-smi --showmeminfo vram


============================ ROCm System Management Interface ============================
================================== Memory Usage (Bytes) ==================================
GPU[0]		: VRAM Total Memory (B): 33580773376
GPU[0]		: VRAM Total Used Memory (B): 8388608
GPU[1]		: VRAM Total Memory (B): 33580773376
GPU[1]		: VRAM Total Used Memory (B): 8388608
GPU[2]		: VRAM Total Memory (B): 33580773376
GPU[2]		: VRAM Total Used Memory (B): 8388608
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

MI300X SPX mode:

```
$ amd-smi version
AMDSMI Tool: 24.7.1+8dc45db | AMDSMI Library version: 25.1.0.0 | ROCm version: 6.3.3

$ rocm-smi -i


============================ ROCm System Management Interface ============================
=========================================== ID ===========================================
GPU[0]		: Device Name: 		AMD Instinct MI300X OAM
GPU[0]		: Device ID: 		0x74a1
GPU[0]		: Device Rev: 		0x00
GPU[0]		: Subsystem ID: 	0x74a1
GPU[0]		: GUID: 		28851
==========================================================================================
================================== End of ROCm SMI Log ===================================

$ rocm-smi


============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK    MCLK    Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                  
==========================================================================================================================
0       2     0x74a1,   28851  47.0°C      133.0W    NPS1, SPX, 0        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================
root@7c6438444a9e:/# rocm-smi --showmeminfo vram


============================ ROCm System Management Interface ============================
================================== Memory Usage (Bytes) ==================================
GPU[0]		: VRAM Total Memory (B): 206141652992
GPU[0]		: VRAM Total Used Memory (B): 297771008
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

MI300X QPX mode:

```
$ rocm-smi


============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK    MCLK    Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                  
==========================================================================================================================
0       2     0x74a1,   1971   47.0°C      133.0W    NPS1, QPX, 0        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
1       3     0x74a1,   49074  47.0°C      133.0W    NPS1, QPX, 1        136Mhz  900Mhz  0%   auto  750.0W  0%     0%    
2       4     0x74a1,   14258  47.0°C      133.0W    NPS1, QPX, 2        136Mhz  900Mhz  0%   auto  750.0W  0%     0%    
3       5     0x74a1,   36787  47.0°C      133.0W    NPS1, QPX, 3        153Mhz  900Mhz  0%   auto  750.0W  0%     0%     
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================

$ rocm-smi --showmeminfo vram


============================ ROCm System Management Interface ============================
================================== Memory Usage (Bytes) ==================================
GPU[0]		: VRAM Total Memory (B): 206141652992
GPU[0]		: VRAM Total Used Memory (B): 297771008
GPU[1]		: VRAM Total Memory (B): 206141652992
GPU[1]		: VRAM Total Used Memory (B): 297771008
GPU[2]		: VRAM Total Memory (B): 206141652992
GPU[2]		: VRAM Total Used Memory (B): 297771008
GPU[3]		: VRAM Total Memory (B): 206141652992
GPU[3]		: VRAM Total Used Memory (B): 297771008
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

### Operating System

Ubuntu 22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD EPYC 9654 96-Core Processor

### GPU

MI300A/MI300X

### ROCm Version

6.3.0-6.4.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — ppanchad-amd (2025-05-20T20:37:47Z)

Hi @maxweiss. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-05-20T21:19:22Z)

Hi @maxweiss, ~~is the MI300X set to NPS1 or NPS4?~~ nevermind, I see you've tried NPS4. I did a quick search and don't see any reference to expected `rocm-smi --showmeminfo vram` or `amd-smi metric -m` output, I'll take a look to see what's going on here.

---

### 评论 #3 — maxweiss (2025-05-21T04:49:30Z)

Hi @schung-amd. Thank you for looking into this!

Yes, I've tried NPS1 and NPS4. But it doesn't seem to matter, rocm-smi and amd-smi always show the full GPU memory for each partition:

SPX mode:
```
$ rocm-smi && rocm-smi --showmeminfo vram


============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK    MCLK    Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                  
==========================================================================================================================
0       2     0x74a1,   28851  48.0°C      135.0W    NPS1, SPX, 0        124Mhz  900Mhz  0%   auto  750.0W  0%     0%    
1       3     0x74a1,   43178  42.0°C      131.0W    NPS1, SPX, 0        145Mhz  900Mhz  0%   auto  750.0W  0%     0%    
2       4     0x74a1,   32898  46.0°C      137.0W    NPS1, SPX, 0        128Mhz  900Mhz  0%   auto  750.0W  0%     0%    
3       5     0x74a1,   22683  41.0°C      133.0W    NPS1, SPX, 0        129Mhz  900Mhz  0%   auto  750.0W  0%     0%    
4       6     0x74a1,   53458  45.0°C      137.0W    NPS1, SPX, 0        124Mhz  900Mhz  0%   auto  750.0W  0%     0%    
5       7     0x74a1,   2251   41.0°C      133.0W    NPS1, SPX, 0        124Mhz  900Mhz  0%   auto  750.0W  0%     0%    
6       8     0x74a1,   8419   47.0°C      133.0W    NPS1, SPX, 0        153Mhz  900Mhz  0%   auto  750.0W  0%     0%    
7       9     0x74a1,   63738  43.0°C      134.0W    NPS1, SPX, 0        128Mhz  900Mhz  0%   auto  750.0W  0%     0%    
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================


============================ ROCm System Management Interface ============================
================================== Memory Usage (Bytes) ==================================
GPU[0]      : VRAM Total Memory (B): 206141652992
GPU[0]      : VRAM Total Used Memory (B): 297771008
GPU[1]      : VRAM Total Memory (B): 206141652992
GPU[1]      : VRAM Total Used Memory (B): 297771008
GPU[2]      : VRAM Total Memory (B): 206141652992
GPU[2]      : VRAM Total Used Memory (B): 297771008
GPU[3]      : VRAM Total Memory (B): 206141652992
GPU[3]      : VRAM Total Used Memory (B): 297771008
GPU[4]      : VRAM Total Memory (B): 206141652992
GPU[4]      : VRAM Total Used Memory (B): 297775104
GPU[5]      : VRAM Total Memory (B): 206141652992
GPU[5]      : VRAM Total Used Memory (B): 297775104
GPU[6]      : VRAM Total Memory (B): 206141652992
GPU[6]      : VRAM Total Used Memory (B): 297775104
GPU[7]      : VRAM Total Memory (B): 206141652992
GPU[7]      : VRAM Total Used Memory (B): 297775104
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

CPX mode (NPS1):

```
$ rocm-smi && rocm-smi --showmeminfo vram


============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK    MCLK    Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                  
==========================================================================================================================
0       2     0x74a1,   4403   48.0°C      135.0W    NPS1, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
1       3     0x74a1,   60722  48.0°C      135.0W    NPS1, CPX, 1        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
2       4     0x74a1,   43314  48.0°C      135.0W    NPS1, CPX, 2        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
3       5     0x74a1,   21811  48.0°C      135.0W    NPS1, CPX, 3        135Mhz  900Mhz  0%   auto  750.0W  0%     0%    
4       6     0x74a1,   8498   48.0°C      135.0W    NPS1, CPX, 4        135Mhz  900Mhz  0%   auto  750.0W  0%     0%    
5       7     0x74a1,   56627  48.0°C      135.0W    NPS1, CPX, 5        147Mhz  900Mhz  0%   auto  750.0W  0%     0%    
6       8     0x74a1,   39219  48.0°C      136.0W    NPS1, CPX, 6        147Mhz  900Mhz  0%   auto  750.0W  0%     0%    
7       9     0x74a1,   25906  48.0°C      136.0W    NPS1, CPX, 7        163Mhz  900Mhz  0%   auto  750.0W  0%     0%    
8       10    0x74a1,   51498  42.0°C      130.0W    NPS1, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
9       11    0x74a1,   13611  42.0°C      130.0W    NPS1, CPX, 1        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
10      12    0x74a1,   28971  42.0°C      130.0W    NPS1, CPX, 2        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
11      13    0x74a1,   36138  42.0°C      130.0W    NPS1, CPX, 3        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
12      14    0x74a1,   63787  42.0°C      131.0W    NPS1, CPX, 4        131Mhz  900Mhz  0%   auto  750.0W  0%     0%    
13      15    0x74a1,   1322   42.0°C      131.0W    NPS1, CPX, 5        131Mhz  900Mhz  0%   auto  750.0W  0%     0%    
14      16    0x74a1,   16682  42.0°C      131.0W    NPS1, CPX, 6        145Mhz  900Mhz  0%   auto  750.0W  0%     0%    
15      17    0x74a1,   48427  42.0°C      131.0W    NPS1, CPX, 7        145Mhz  900Mhz  0%   auto  750.0W  0%     0%    
16      18    0x74a1,   57602  46.0°C      136.0W    NPS1, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
17      19    0x74a1,   7427   46.0°C      136.0W    NPS1, CPX, 1        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
18      20    0x74a1,   22787  46.0°C      136.0W    NPS1, CPX, 2        127Mhz  900Mhz  0%   auto  750.0W  0%     0%    
19      21    0x74a1,   42242  46.0°C      136.0W    NPS1, CPX, 3        127Mhz  900Mhz  0%   auto  750.0W  0%     0%    
20      22    0x74a1,   53507  46.0°C      136.0W    NPS1, CPX, 4        132Mhz  900Mhz  0%   auto  750.0W  0%     0%    
21      23    0x74a1,   11522  46.0°C      136.0W    NPS1, CPX, 5        132Mhz  900Mhz  0%   auto  750.0W  0%     0%    
22      24    0x74a1,   26882  46.0°C      136.0W    NPS1, CPX, 6        146Mhz  900Mhz  0%   auto  750.0W  0%     0%    
23      25    0x74a1,   38147  46.0°C      137.0W    NPS1, CPX, 7        146Mhz  900Mhz  0%   auto  750.0W  0%     0%    
24      26    0x74a1,   14619  41.0°C      133.0W    NPS1, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
25      27    0x74a1,   50458  41.0°C      133.0W    NPS1, CPX, 1        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
26      28    0x74a1,   33050  41.0°C      133.0W    NPS1, CPX, 2        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
27      29    0x74a1,   32027  41.0°C      133.0W    NPS1, CPX, 3        136Mhz  900Mhz  0%   auto  750.0W  0%     0%    
28      30    0x74a1,   2330   41.0°C      133.0W    NPS1, CPX, 4        136Mhz  900Mhz  0%   auto  750.0W  0%     0%    
29      31    0x74a1,   62747  41.0°C      133.0W    NPS1, CPX, 5        152Mhz  900Mhz  0%   auto  750.0W  0%     0%    
30      32    0x74a1,   45339  41.0°C      133.0W    NPS1, CPX, 6        152Mhz  900Mhz  0%   auto  750.0W  0%     0%    
31      33    0x74a1,   19738  41.0°C      133.0W    NPS1, CPX, 7        168Mhz  900Mhz  0%   auto  750.0W  0%     0%    
32      34    0x74a1,   45394  45.0°C      137.0W    NPS1, CPX, 0        123Mhz  900Mhz  0%   auto  750.0W  0%     0%    
33      35    0x74a1,   19795  45.0°C      137.0W    NPS1, CPX, 1        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
34      36    0x74a1,   2387   45.0°C      137.0W    NPS1, CPX, 2        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
35      37    0x74a1,   62802  45.0°C      137.0W    NPS1, CPX, 3        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
36      38    0x74a1,   33107  45.0°C      137.0W    NPS1, CPX, 4        131Mhz  900Mhz  0%   auto  750.0W  0%     0%    
37      39    0x74a1,   32082  45.0°C      137.0W    NPS1, CPX, 5        131Mhz  900Mhz  0%   auto  750.0W  0%     0%    
38      40    0x74a1,   14674  45.0°C      137.0W    NPS1, CPX, 6        152Mhz  900Mhz  0%   auto  750.0W  0%     0%    
39      41    0x74a1,   50515  45.0°C      137.0W    NPS1, CPX, 7        152Mhz  900Mhz  0%   auto  750.0W  0%     0%    
40      42    0x74a1,   26955  41.0°C      133.0W    NPS1, CPX, 0        123Mhz  900Mhz  0%   auto  750.0W  0%     0%    
41      43    0x74a1,   38218  41.0°C      133.0W    NPS1, CPX, 1        127Mhz  900Mhz  0%   auto  750.0W  0%     0%    
42      44    0x74a1,   53578  41.0°C      133.0W    NPS1, CPX, 2        127Mhz  900Mhz  0%   auto  750.0W  0%     0%    
43      45    0x74a1,   11595  41.0°C      133.0W    NPS1, CPX, 3        130Mhz  900Mhz  0%   auto  750.0W  0%     0%    
44      46    0x74a1,   22858  41.0°C      133.0W    NPS1, CPX, 4        130Mhz  900Mhz  0%   auto  750.0W  0%     0%    
45      47    0x74a1,   42315  41.0°C      133.0W    NPS1, CPX, 5        140Mhz  900Mhz  0%   auto  750.0W  0%     0%    
46      48    0x74a1,   57675  41.0°C      133.0W    NPS1, CPX, 6        140Mhz  900Mhz  0%   auto  750.0W  0%     0%    
47      49    0x74a1,   16739  47.0°C      133.0W    NPS1, CPX, 0        123Mhz  900Mhz  0%   auto  750.0W  0%     0%    
48      50    0x74a1,   48482  47.0°C      133.0W    NPS1, CPX, 1        123Mhz  900Mhz  0%   auto  750.0W  0%     0%    
49      51    0x74a1,   63842  47.0°C      133.0W    NPS1, CPX, 2        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
50      52    0x74a1,   1379   47.0°C      133.0W    NPS1, CPX, 3        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
51      53    0x74a1,   29026  47.0°C      133.0W    NPS1, CPX, 4        145Mhz  900Mhz  0%   auto  750.0W  0%     0%    
52      54    0x74a1,   36195  47.0°C      133.0W    NPS1, CPX, 5        145Mhz  900Mhz  0%   auto  750.0W  0%     0%    
53      55    0x74a1,   51555  47.0°C      133.0W    NPS1, CPX, 6        160Mhz  900Mhz  0%   auto  750.0W  0%     0%    
54      56    0x74a1,   13666  47.0°C      133.0W    NPS1, CPX, 7        160Mhz  900Mhz  0%   auto  750.0W  0%     0%    
55      57    0x74a1,   39290  43.0°C      134.0W    NPS1, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
56      58    0x74a1,   25979  43.0°C      134.0W    NPS1, CPX, 1        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
57      59    0x74a1,   8571   43.0°C      134.0W    NPS1, CPX, 2        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
58      60    0x74a1,   56698  43.0°C      134.0W    NPS1, CPX, 3        130Mhz  900Mhz  0%   auto  750.0W  0%     0%    
59      61    0x74a1,   43387  43.0°C      134.0W    NPS1, CPX, 4        130Mhz  900Mhz  0%   auto  750.0W  0%     0%    
60      62    0x74a1,   21882  43.0°C      134.0W    NPS1, CPX, 5        146Mhz  900Mhz  0%   auto  750.0W  0%     0%    
61      63    0x74a1,   4474   43.0°C      134.0W    NPS1, CPX, 6        146Mhz  900Mhz  0%   auto  750.0W  0%     0%    
62      64    0x74a1,   60795  43.0°C      134.0W    NPS1, CPX, 7        146Mhz  900Mhz  0%   auto  750.0W  0%     0%    
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================


============================ ROCm System Management Interface ============================
================================== Memory Usage (Bytes) ==================================
GPU[0]      : VRAM Total Memory (B): 206141652992
GPU[0]      : VRAM Total Used Memory (B): 297771008
GPU[1]      : VRAM Total Memory (B): 206141652992
GPU[1]      : VRAM Total Used Memory (B): 297771008
GPU[2]      : VRAM Total Memory (B): 206141652992
GPU[2]      : VRAM Total Used Memory (B): 297771008
GPU[3]      : VRAM Total Memory (B): 206141652992
GPU[3]      : VRAM Total Used Memory (B): 297771008
GPU[4]      : VRAM Total Memory (B): 206141652992
GPU[4]      : VRAM Total Used Memory (B): 297771008
GPU[5]      : VRAM Total Memory (B): 206141652992
GPU[5]      : VRAM Total Used Memory (B): 297771008
GPU[6]      : VRAM Total Memory (B): 206141652992
GPU[6]      : VRAM Total Used Memory (B): 297771008
GPU[7]      : VRAM Total Memory (B): 206141652992
GPU[7]      : VRAM Total Used Memory (B): 297771008
GPU[8]      : VRAM Total Memory (B): 206141652992
GPU[8]      : VRAM Total Used Memory (B): 297771008
GPU[9]      : VRAM Total Memory (B): 206141652992
GPU[9]      : VRAM Total Used Memory (B): 297771008
GPU[10]     : VRAM Total Memory (B): 206141652992
GPU[10]     : VRAM Total Used Memory (B): 297771008
GPU[11]     : VRAM Total Memory (B): 206141652992
GPU[11]     : VRAM Total Used Memory (B): 297771008
GPU[12]     : VRAM Total Memory (B): 206141652992
GPU[12]     : VRAM Total Used Memory (B): 297771008
GPU[13]     : VRAM Total Memory (B): 206141652992
GPU[13]     : VRAM Total Used Memory (B): 297771008
GPU[14]     : VRAM Total Memory (B): 206141652992
GPU[14]     : VRAM Total Used Memory (B): 297771008
GPU[15]     : VRAM Total Memory (B): 206141652992
GPU[15]     : VRAM Total Used Memory (B): 297771008
GPU[16]     : VRAM Total Memory (B): 206141652992
GPU[16]     : VRAM Total Used Memory (B): 297771008
GPU[17]     : VRAM Total Memory (B): 206141652992
GPU[17]     : VRAM Total Used Memory (B): 297771008
GPU[18]     : VRAM Total Memory (B): 206141652992
GPU[18]     : VRAM Total Used Memory (B): 297771008
GPU[19]     : VRAM Total Memory (B): 206141652992
GPU[19]     : VRAM Total Used Memory (B): 297771008
GPU[20]     : VRAM Total Memory (B): 206141652992
GPU[20]     : VRAM Total Used Memory (B): 297771008
GPU[21]     : VRAM Total Memory (B): 206141652992
GPU[21]     : VRAM Total Used Memory (B): 297771008
GPU[22]     : VRAM Total Memory (B): 206141652992
GPU[22]     : VRAM Total Used Memory (B): 297771008
GPU[23]     : VRAM Total Memory (B): 206141652992
GPU[23]     : VRAM Total Used Memory (B): 297771008
GPU[24]     : VRAM Total Memory (B): 206141652992
GPU[24]     : VRAM Total Used Memory (B): 297771008
GPU[25]     : VRAM Total Memory (B): 206141652992
GPU[25]     : VRAM Total Used Memory (B): 297771008
GPU[26]     : VRAM Total Memory (B): 206141652992
GPU[26]     : VRAM Total Used Memory (B): 297771008
GPU[27]     : VRAM Total Memory (B): 206141652992
GPU[27]     : VRAM Total Used Memory (B): 297771008
GPU[28]     : VRAM Total Memory (B): 206141652992
GPU[28]     : VRAM Total Used Memory (B): 297771008
GPU[29]     : VRAM Total Memory (B): 206141652992
GPU[29]     : VRAM Total Used Memory (B): 297771008
GPU[30]     : VRAM Total Memory (B): 206141652992
GPU[30]     : VRAM Total Used Memory (B): 297771008
GPU[31]     : VRAM Total Memory (B): 206141652992
GPU[31]     : VRAM Total Used Memory (B): 297771008
GPU[32]     : VRAM Total Memory (B): 206141652992
GPU[32]     : VRAM Total Used Memory (B): 297775104
GPU[33]     : VRAM Total Memory (B): 206141652992
GPU[33]     : VRAM Total Used Memory (B): 297775104
GPU[34]     : VRAM Total Memory (B): 206141652992
GPU[34]     : VRAM Total Used Memory (B): 297775104
GPU[35]     : VRAM Total Memory (B): 206141652992
GPU[35]     : VRAM Total Used Memory (B): 297775104
GPU[36]     : VRAM Total Memory (B): 206141652992
GPU[36]     : VRAM Total Used Memory (B): 297775104
GPU[37]     : VRAM Total Memory (B): 206141652992
GPU[37]     : VRAM Total Used Memory (B): 297775104
GPU[38]     : VRAM Total Memory (B): 206141652992
GPU[38]     : VRAM Total Used Memory (B): 297775104
GPU[39]     : VRAM Total Memory (B): 206141652992
GPU[39]     : VRAM Total Used Memory (B): 297775104
GPU[40]     : VRAM Total Memory (B): 206141652992
GPU[40]     : VRAM Total Used Memory (B): 297775104
GPU[41]     : VRAM Total Memory (B): 206141652992
GPU[41]     : VRAM Total Used Memory (B): 297775104
GPU[42]     : VRAM Total Memory (B): 206141652992
GPU[42]     : VRAM Total Used Memory (B): 297775104
GPU[43]     : VRAM Total Memory (B): 206141652992
GPU[43]     : VRAM Total Used Memory (B): 297775104
GPU[44]     : VRAM Total Memory (B): 206141652992
GPU[44]     : VRAM Total Used Memory (B): 297775104
GPU[45]     : VRAM Total Memory (B): 206141652992
GPU[45]     : VRAM Total Used Memory (B): 297775104
GPU[46]     : VRAM Total Memory (B): 206141652992
GPU[46]     : VRAM Total Used Memory (B): 297775104
GPU[47]     : VRAM Total Memory (B): 206141652992
GPU[47]     : VRAM Total Used Memory (B): 297775104
GPU[48]     : VRAM Total Memory (B): 206141652992
GPU[48]     : VRAM Total Used Memory (B): 297775104
GPU[49]     : VRAM Total Memory (B): 206141652992
GPU[49]     : VRAM Total Used Memory (B): 297775104
GPU[50]     : VRAM Total Memory (B): 206141652992
GPU[50]     : VRAM Total Used Memory (B): 297775104
GPU[51]     : VRAM Total Memory (B): 206141652992
GPU[51]     : VRAM Total Used Memory (B): 297775104
GPU[52]     : VRAM Total Memory (B): 206141652992
GPU[52]     : VRAM Total Used Memory (B): 297775104
GPU[53]     : VRAM Total Memory (B): 206141652992
GPU[53]     : VRAM Total Used Memory (B): 297775104
GPU[54]     : VRAM Total Memory (B): 206141652992
GPU[54]     : VRAM Total Used Memory (B): 297775104
GPU[55]     : VRAM Total Memory (B): 206141652992
GPU[55]     : VRAM Total Used Memory (B): 297775104
GPU[56]     : VRAM Total Memory (B): 206141652992
GPU[56]     : VRAM Total Used Memory (B): 297775104
GPU[57]     : VRAM Total Memory (B): 206141652992
GPU[57]     : VRAM Total Used Memory (B): 297775104
GPU[58]     : VRAM Total Memory (B): 206141652992
GPU[58]     : VRAM Total Used Memory (B): 297775104
GPU[59]     : VRAM Total Memory (B): 206141652992
GPU[59]     : VRAM Total Used Memory (B): 297775104
GPU[60]     : VRAM Total Memory (B): 206141652992
GPU[60]     : VRAM Total Used Memory (B): 297775104
GPU[61]     : VRAM Total Memory (B): 206141652992
GPU[61]     : VRAM Total Used Memory (B): 297775104
GPU[62]     : VRAM Total Memory (B): 206141652992
GPU[62]     : VRAM Total Used Memory (B): 297775104
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

CPX mode (NPS4):
```
$ rocm-smi && rocm-smi --showmeminfo vram


============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK    MCLK    Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                  
==========================================================================================================================
0       34    0x74a1,   42546  48.0°C      142.0W    NPS4, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
1       35    0x74a1,   23091  48.0°C      142.0W    NPS4, CPX, 1        131Mhz  900Mhz  0%   auto  750.0W  0%     0%    
2       36    0x74a1,   7731   48.0°C      141.0W    NPS4, CPX, 2        131Mhz  900Mhz  0%   auto  750.0W  0%     0%    
3       37    0x74a1,   57906  48.0°C      141.0W    NPS4, CPX, 3        149Mhz  900Mhz  0%   auto  750.0W  0%     0%    
4       38    0x74a1,   38451  48.0°C      141.0W    NPS4, CPX, 4        149Mhz  900Mhz  0%   auto  750.0W  0%     0%    
5       39    0x74a1,   27186  48.0°C      141.0W    NPS4, CPX, 5        163Mhz  900Mhz  0%   auto  750.0W  0%     0%    
6       40    0x74a1,   10032  48.0°C      142.0W    NPS4, CPX, 6        163Mhz  900Mhz  0%   auto  750.0W  0%     0%    
7       41    0x74a1,   56113  48.0°C      142.0W    NPS4, CPX, 7        170Mhz  900Mhz  0%   auto  750.0W  0%     0%    
8       10    0x74a1,   32299  42.0°C      137.0W    NPS4, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
9       11    0x74a1,   33322  42.0°C      137.0W    NPS4, CPX, 1        129Mhz  900Mhz  0%   auto  750.0W  0%     0%    
10      12    0x74a1,   50730  42.0°C      137.0W    NPS4, CPX, 2        129Mhz  900Mhz  0%   auto  750.0W  0%     0%    
11      13    0x74a1,   14891  42.0°C      137.0W    NPS4, CPX, 3        145Mhz  900Mhz  0%   auto  750.0W  0%     0%    
12      14    0x74a1,   20010  42.0°C      137.0W    NPS4, CPX, 4        145Mhz  900Mhz  0%   auto  750.0W  0%     0%    
13      15    0x74a1,   45611  42.0°C      137.0W    NPS4, CPX, 5        145Mhz  900Mhz  0%   auto  750.0W  0%     0%    
14      16    0x74a1,   65321  42.0°C      137.0W    NPS4, CPX, 6        161Mhz  900Mhz  0%   auto  750.0W  0%     0%    
15      17    0x74a1,   808    42.0°C      137.0W    NPS4, CPX, 7        161Mhz  900Mhz  0%   auto  750.0W  0%     0%    
16      2     0x74a1,   22019  47.0°C      143.0W    NPS4, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
17      3     0x74a1,   43522  47.0°C      143.0W    NPS4, CPX, 1        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
18      4     0x74a1,   60930  47.0°C      143.0W    NPS4, CPX, 2        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
19      5     0x74a1,   4611   47.0°C      143.0W    NPS4, CPX, 3        126Mhz  900Mhz  0%   auto  750.0W  0%     0%    
20      6     0x74a1,   26114  47.0°C      143.0W    NPS4, CPX, 4        137Mhz  900Mhz  0%   auto  750.0W  0%     0%    
21      7     0x74a1,   39427  47.0°C      143.0W    NPS4, CPX, 5        137Mhz  900Mhz  0%   auto  750.0W  0%     0%    
22      8     0x74a1,   55041  47.0°C      143.0W    NPS4, CPX, 6        152Mhz  900Mhz  0%   auto  750.0W  0%     0%    
23      9     0x74a1,   11008  47.0°C      143.0W    NPS4, CPX, 7        152Mhz  900Mhz  0%   auto  750.0W  0%     0%    
24      26    0x74a1,   36378  41.0°C      140.0W    NPS4, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
25      27    0x74a1,   29211  41.0°C      140.0W    NPS4, CPX, 1        130Mhz  900Mhz  0%   auto  750.0W  0%     0%    
26      28    0x74a1,   13851  41.0°C      140.0W    NPS4, CPX, 2        130Mhz  900Mhz  0%   auto  750.0W  0%     0%    
27      29    0x74a1,   51738  41.0°C      140.0W    NPS4, CPX, 3        144Mhz  900Mhz  0%   auto  750.0W  0%     0%    
28      30    0x74a1,   48667  41.0°C      140.0W    NPS4, CPX, 4        144Mhz  900Mhz  0%   auto  750.0W  0%     0%    
29      31    0x74a1,   16922  41.0°C      140.0W    NPS4, CPX, 5        160Mhz  900Mhz  0%   auto  750.0W  0%     0%    
30      32    0x74a1,   3864   41.0°C      140.0W    NPS4, CPX, 6        160Mhz  900Mhz  0%   auto  750.0W  0%     0%    
31      33    0x74a1,   62233  41.0°C      140.0W    NPS4, CPX, 7        171Mhz  900Mhz  0%   auto  750.0W  0%     0%    
32      50    0x74a1,   1619   46.0°C      142.0W    NPS4, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
33      51    0x74a1,   64082  46.0°C      142.0W    NPS4, CPX, 1        127Mhz  900Mhz  0%   auto  750.0W  0%     0%    
34      52    0x74a1,   48722  46.0°C      142.0W    NPS4, CPX, 2        127Mhz  900Mhz  0%   auto  750.0W  0%     0%    
35      53    0x74a1,   16979  46.0°C      142.0W    NPS4, CPX, 3        143Mhz  900Mhz  0%   auto  750.0W  0%     0%    
36      54    0x74a1,   13906  46.0°C      143.0W    NPS4, CPX, 4        143Mhz  900Mhz  0%   auto  750.0W  0%     0%    
37      55    0x74a1,   51795  46.0°C      143.0W    NPS4, CPX, 5        143Mhz  900Mhz  0%   auto  750.0W  0%     0%    
38      56    0x74a1,   34641  46.0°C      142.0W    NPS4, CPX, 6        158Mhz  900Mhz  0%   auto  750.0W  0%     0%    
39      57    0x74a1,   31568  46.0°C      142.0W    NPS4, CPX, 7        158Mhz  900Mhz  0%   auto  750.0W  0%     0%    
40      58    0x74a1,   56906  41.0°C      139.0W    NPS4, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
41      59    0x74a1,   8779   41.0°C      139.0W    NPS4, CPX, 1        127Mhz  900Mhz  0%   auto  750.0W  0%     0%    
42      60    0x74a1,   26187  41.0°C      138.0W    NPS4, CPX, 2        127Mhz  900Mhz  0%   auto  750.0W  0%     0%    
43      61    0x74a1,   39498  41.0°C      138.0W    NPS4, CPX, 3        143Mhz  900Mhz  0%   auto  750.0W  0%     0%    
44      62    0x74a1,   61003  41.0°C      139.0W    NPS4, CPX, 4        143Mhz  900Mhz  0%   auto  750.0W  0%     0%    
45      63    0x74a1,   4682   41.0°C      139.0W    NPS4, CPX, 5        158Mhz  900Mhz  0%   auto  750.0W  0%     0%    
46      64    0x74a1,   24392  41.0°C      139.0W    NPS4, CPX, 6        158Mhz  900Mhz  0%   auto  750.0W  0%     0%    
47      42    0x74a1,   63074  47.0°C      140.0W    NPS4, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
48      43    0x74a1,   2659   47.0°C      140.0W    NPS4, CPX, 1        127Mhz  900Mhz  0%   auto  750.0W  0%     0%    
49      44    0x74a1,   20067  47.0°C      140.0W    NPS4, CPX, 2        127Mhz  900Mhz  0%   auto  750.0W  0%     0%    
50      45    0x74a1,   45666  47.0°C      140.0W    NPS4, CPX, 3        136Mhz  900Mhz  0%   auto  750.0W  0%     0%    
51      46    0x74a1,   50787  47.0°C      140.0W    NPS4, CPX, 4        136Mhz  900Mhz  0%   auto  750.0W  0%     0%    
52      47    0x74a1,   14946  47.0°C      140.0W    NPS4, CPX, 5        136Mhz  900Mhz  0%   auto  750.0W  0%     0%    
53      48    0x74a1,   30560  47.0°C      140.0W    NPS4, CPX, 6        153Mhz  900Mhz  0%   auto  750.0W  0%     0%    
54      49    0x74a1,   35681  47.0°C      140.0W    NPS4, CPX, 7        153Mhz  900Mhz  0%   auto  750.0W  0%     0%    
55      18    0x74a1,   11899  43.0°C      140.0W    NPS4, CPX, 0        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
56      19    0x74a1,   53882  43.0°C      140.0W    NPS4, CPX, 1        122Mhz  900Mhz  0%   auto  750.0W  0%     0%    
57      20    0x74a1,   38522  43.0°C      140.0W    NPS4, CPX, 2        131Mhz  900Mhz  0%   auto  750.0W  0%     0%    
58      21    0x74a1,   27259  43.0°C      140.0W    NPS4, CPX, 3        131Mhz  900Mhz  0%   auto  750.0W  0%     0%    
59      22    0x74a1,   7802   43.0°C      140.0W    NPS4, CPX, 4        150Mhz  900Mhz  0%   auto  750.0W  0%     0%    
60      23    0x74a1,   57979  43.0°C      140.0W    NPS4, CPX, 5        150Mhz  900Mhz  0%   auto  750.0W  0%     0%    
61      24    0x74a1,   44921  43.0°C      140.0W    NPS4, CPX, 6        164Mhz  900Mhz  0%   auto  750.0W  0%     0%    
62      25    0x74a1,   21368  43.0°C      140.0W    NPS4, CPX, 7        164Mhz  900Mhz  0%   auto  750.0W  0%     0%    
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================


============================ ROCm System Management Interface ============================
================================== Memory Usage (Bytes) ==================================
GPU[0]		: VRAM Total Memory (B): 206141652992
GPU[0]		: VRAM Total Used Memory (B): 297771008
GPU[1]		: VRAM Total Memory (B): 206141652992
GPU[1]		: VRAM Total Used Memory (B): 297771008
GPU[2]		: VRAM Total Memory (B): 206141652992
GPU[2]		: VRAM Total Used Memory (B): 297771008
GPU[3]		: VRAM Total Memory (B): 206141652992
GPU[3]		: VRAM Total Used Memory (B): 297771008
GPU[4]		: VRAM Total Memory (B): 206141652992
GPU[4]		: VRAM Total Used Memory (B): 297771008
GPU[5]		: VRAM Total Memory (B): 206141652992
GPU[5]		: VRAM Total Used Memory (B): 297771008
GPU[6]		: VRAM Total Memory (B): 206141652992
GPU[6]		: VRAM Total Used Memory (B): 297771008
GPU[7]		: VRAM Total Memory (B): 206141652992
GPU[7]		: VRAM Total Used Memory (B): 297771008
GPU[8]		: VRAM Total Memory (B): 206141652992
GPU[8]		: VRAM Total Used Memory (B): 297771008
GPU[9]		: VRAM Total Memory (B): 206141652992
GPU[9]		: VRAM Total Used Memory (B): 297771008
GPU[10]		: VRAM Total Memory (B): 206141652992
GPU[10]		: VRAM Total Used Memory (B): 297771008
GPU[11]		: VRAM Total Memory (B): 206141652992
GPU[11]		: VRAM Total Used Memory (B): 297771008
GPU[12]		: VRAM Total Memory (B): 206141652992
GPU[12]		: VRAM Total Used Memory (B): 297771008
GPU[13]		: VRAM Total Memory (B): 206141652992
GPU[13]		: VRAM Total Used Memory (B): 297771008
GPU[14]		: VRAM Total Memory (B): 206141652992
GPU[14]		: VRAM Total Used Memory (B): 297771008
GPU[15]		: VRAM Total Memory (B): 206141652992
GPU[15]		: VRAM Total Used Memory (B): 297771008
GPU[16]		: VRAM Total Memory (B): 206141652992
GPU[16]		: VRAM Total Used Memory (B): 297771008
GPU[17]		: VRAM Total Memory (B): 206141652992
GPU[17]		: VRAM Total Used Memory (B): 297771008
GPU[18]		: VRAM Total Memory (B): 206141652992
GPU[18]		: VRAM Total Used Memory (B): 297771008
GPU[19]		: VRAM Total Memory (B): 206141652992
GPU[19]		: VRAM Total Used Memory (B): 297771008
GPU[20]		: VRAM Total Memory (B): 206141652992
GPU[20]		: VRAM Total Used Memory (B): 297771008
GPU[21]		: VRAM Total Memory (B): 206141652992
GPU[21]		: VRAM Total Used Memory (B): 297771008
GPU[22]		: VRAM Total Memory (B): 206141652992
GPU[22]		: VRAM Total Used Memory (B): 297771008
GPU[23]		: VRAM Total Memory (B): 206141652992
GPU[23]		: VRAM Total Used Memory (B): 297771008
GPU[24]		: VRAM Total Memory (B): 206141652992
GPU[24]		: VRAM Total Used Memory (B): 297771008
GPU[25]		: VRAM Total Memory (B): 206141652992
GPU[25]		: VRAM Total Used Memory (B): 297771008
GPU[26]		: VRAM Total Memory (B): 206141652992
GPU[26]		: VRAM Total Used Memory (B): 297771008
GPU[27]		: VRAM Total Memory (B): 206141652992
GPU[27]		: VRAM Total Used Memory (B): 297771008
GPU[28]		: VRAM Total Memory (B): 206141652992
GPU[28]		: VRAM Total Used Memory (B): 297771008
GPU[29]		: VRAM Total Memory (B): 206141652992
GPU[29]		: VRAM Total Used Memory (B): 297771008
GPU[30]		: VRAM Total Memory (B): 206141652992
GPU[30]		: VRAM Total Used Memory (B): 297771008
GPU[31]		: VRAM Total Memory (B): 206141652992
GPU[31]		: VRAM Total Used Memory (B): 297771008
GPU[32]		: VRAM Total Memory (B): 206141652992
GPU[32]		: VRAM Total Used Memory (B): 297775104
GPU[33]		: VRAM Total Memory (B): 206141652992
GPU[33]		: VRAM Total Used Memory (B): 297775104
GPU[34]		: VRAM Total Memory (B): 206141652992
GPU[34]		: VRAM Total Used Memory (B): 297775104
GPU[35]		: VRAM Total Memory (B): 206141652992
GPU[35]		: VRAM Total Used Memory (B): 297775104
GPU[36]		: VRAM Total Memory (B): 206141652992
GPU[36]		: VRAM Total Used Memory (B): 297775104
GPU[37]		: VRAM Total Memory (B): 206141652992
GPU[37]		: VRAM Total Used Memory (B): 297775104
GPU[38]		: VRAM Total Memory (B): 206141652992
GPU[38]		: VRAM Total Used Memory (B): 297775104
GPU[39]		: VRAM Total Memory (B): 206141652992
GPU[39]		: VRAM Total Used Memory (B): 297775104
GPU[40]		: VRAM Total Memory (B): 206141652992
GPU[40]		: VRAM Total Used Memory (B): 297775104
GPU[41]		: VRAM Total Memory (B): 206141652992
GPU[41]		: VRAM Total Used Memory (B): 297775104
GPU[42]		: VRAM Total Memory (B): 206141652992
GPU[42]		: VRAM Total Used Memory (B): 297775104
GPU[43]		: VRAM Total Memory (B): 206141652992
GPU[43]		: VRAM Total Used Memory (B): 297775104
GPU[44]		: VRAM Total Memory (B): 206141652992
GPU[44]		: VRAM Total Used Memory (B): 297775104
GPU[45]		: VRAM Total Memory (B): 206141652992
GPU[45]		: VRAM Total Used Memory (B): 297775104
GPU[46]		: VRAM Total Memory (B): 206141652992
GPU[46]		: VRAM Total Used Memory (B): 297775104
GPU[47]		: VRAM Total Memory (B): 206141652992
GPU[47]		: VRAM Total Used Memory (B): 297775104
GPU[48]		: VRAM Total Memory (B): 206141652992
GPU[48]		: VRAM Total Used Memory (B): 297775104
GPU[49]		: VRAM Total Memory (B): 206141652992
GPU[49]		: VRAM Total Used Memory (B): 297775104
GPU[50]		: VRAM Total Memory (B): 206141652992
GPU[50]		: VRAM Total Used Memory (B): 297775104
GPU[51]		: VRAM Total Memory (B): 206141652992
GPU[51]		: VRAM Total Used Memory (B): 297775104
GPU[52]		: VRAM Total Memory (B): 206141652992
GPU[52]		: VRAM Total Used Memory (B): 297775104
GPU[53]		: VRAM Total Memory (B): 206141652992
GPU[53]		: VRAM Total Used Memory (B): 297775104
GPU[54]		: VRAM Total Memory (B): 206141652992
GPU[54]		: VRAM Total Used Memory (B): 297775104
GPU[55]		: VRAM Total Memory (B): 206141652992
GPU[55]		: VRAM Total Used Memory (B): 297775104
GPU[56]		: VRAM Total Memory (B): 206141652992
GPU[56]		: VRAM Total Used Memory (B): 297775104
GPU[57]		: VRAM Total Memory (B): 206141652992
GPU[57]		: VRAM Total Used Memory (B): 297775104
GPU[58]		: VRAM Total Memory (B): 206141652992
GPU[58]		: VRAM Total Used Memory (B): 297775104
GPU[59]		: VRAM Total Memory (B): 206141652992
GPU[59]		: VRAM Total Used Memory (B): 297775104
GPU[60]		: VRAM Total Memory (B): 206141652992
GPU[60]		: VRAM Total Used Memory (B): 297775104
GPU[61]		: VRAM Total Memory (B): 206141652992
GPU[61]		: VRAM Total Used Memory (B): 297775104
GPU[62]		: VRAM Total Memory (B): 206141652992
GPU[62]		: VRAM Total Used Memory (B): 297775104
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

---

### 评论 #4 — schung-amd (2025-05-21T16:44:45Z)

Thanks for the additional output. My test system's output is showing node 0 with the full amount of VRAM and the rest with the proper number, which isn't exactly what you're seeing but is still wrong. This system is on an internal build of ROCm so might be some difference there. 

Does `rocminfo` report the correct amount of VRAM per partition on your system? My reproducer reports the correct amount with `rocminfo`, and the correct amount of VRAM per partition is reported by the driver in `/sys/class/kfd/kfd/topology/nodes/<device id>/mem_banks/0/properties`.

---

### 评论 #5 — maxweiss (2025-05-21T17:18:00Z)

Yes, rocminfo and the mem_banks files show the correct amount of VRAM.

In CPX mode:

```
$ cat /sys/class/kfd/kfd/topology/nodes/3/mem_banks/0/properties 
heap_type 1
size_in_bytes 25767706624
flags 0
width 8192
mem_clk_max 1300
```

```
*******                  
Agent 3                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-dc91284879207f2b               
  Marketing Name:          AMD Instinct MI300X                
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
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29857(0x74a1)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1950                               
  BDFID:                   1280                               
  Internal Node ID:        2                                  
  Compute Unit:            38                                 
  SIMDs per CU:            4                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
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
  Packet Processor uCode:: 166                                
  SDMA engine uCode::      22                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25163776(0x17ff800) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25163776(0x17ff800) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    25163776(0x17ff800) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
  Name:                    gfx942                             
  Uuid:                    GPU-dc91284879207f2b               
  Marketing Name:          AMD Instinct MI300X                
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
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29857(0x74a1)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1950                               
  BDFID:                   1281                               
  Internal Node ID:        3                                  
  Compute Unit:            38                                 
  SIMDs per CU:            4                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
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
  Packet Processor uCode:: 166                                
  SDMA engine uCode::      22                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25163776(0x17ff800) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25163776(0x17ff800) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    25163776(0x17ff800) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
```

I've attached the complete output of rocminfo.

[rocm.log](https://github.com/user-attachments/files/20372850/rocm.log)

---

### 评论 #6 — schung-amd (2025-05-21T19:05:02Z)

Thanks for verifying. I spoke with the rocm-smi/amd-smi team, they're currently working on this as part of a bigger initiative to support per-XCD activities in an upcoming ROCm release. I don't have a clear timeframe on this, but can provide further guidance if needed.

---

### 评论 #7 — maxweiss (2025-05-21T19:33:34Z)

It's okay for us to know that it's a bug and that it will be fixed at some point. Thank you!

---

### 评论 #8 — schung-amd (2025-05-21T19:35:31Z)

Great, I'll close this for now then, feel free to comment if you come across anything else in rocm-smi or amd-smi you need guidance on and we can reopen if necessary.

---
