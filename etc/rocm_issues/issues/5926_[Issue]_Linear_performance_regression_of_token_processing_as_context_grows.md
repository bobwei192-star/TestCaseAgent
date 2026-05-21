# [Issue]: Linear performance regression of token processing as context grows.

> **Issue #5926**
> **状态**: open
> **创建时间**: 2026-02-03T13:10:17Z
> **更新时间**: 2026-03-08T11:10:31Z
> **作者**: winmutt
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5926

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- benrichard-amd

## 描述

### Problem Description

With large context models, there is a linear performance regression of token processing. 

```
Feb 01 12:45:52  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 0, memory_seq_rm [0, end)
Feb 01 12:45:52  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 2048, batch.n_tokens = 2048, progress = 0.030386
Feb 01 12:45:54  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 2048, memory_seq_rm [2048, end)
Feb 01 12:45:54  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 4096, batch.n_tokens = 2048, progress = 0.060772
Feb 01 12:45:56  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 4096, memory_seq_rm [4096, end)
Feb 01 12:45:56  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 6144, batch.n_tokens = 2048, progress = 0.091157
Feb 01 12:45:59  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 6144, memory_seq_rm [6144, end)
Feb 01 12:45:59  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 8192, batch.n_tokens = 2048, progress = 0.121543
Feb 01 12:46:02  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 8192, memory_seq_rm [8192, end)
Feb 01 12:46:02  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 10240, batch.n_tokens = 2048, progress = 0.151929
Feb 01 12:46:06  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 10240, memory_seq_rm [10240, end)
Feb 01 12:46:06  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 12288, batch.n_tokens = 2048, progress = 0.182315
Feb 01 12:46:11  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 12288, memory_seq_rm [12288, end)
Feb 01 12:46:11  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 14336, batch.n_tokens = 2048, progress = 0.212700
Feb 01 12:46:16  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 14336, memory_seq_rm [14336, end)
Feb 01 12:46:16  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 16384, batch.n_tokens = 2048, progress = 0.243086
Feb 01 12:46:23  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 16384, memory_seq_rm [16384, end)
Feb 01 12:46:23  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 18432, batch.n_tokens = 2048, progress = 0.273472
Feb 01 12:46:30  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 18432, memory_seq_rm [18432, end)
Feb 01 12:46:30  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 20480, batch.n_tokens = 2048, progress = 0.303858
Feb 01 12:46:37  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 20480, memory_seq_rm [20480, end)
Feb 01 12:46:37  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 22528, batch.n_tokens = 2048, progress = 0.334243
Feb 01 12:46:46  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 22528, memory_seq_rm [22528, end)
Feb 01 12:46:46  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 24576, batch.n_tokens = 2048, progress = 0.364629
Feb 01 12:46:55  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 24576, memory_seq_rm [24576, end)
Feb 01 12:46:55  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 26624, batch.n_tokens = 2048, progress = 0.395015
Feb 01 12:47:04  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 26624, memory_seq_rm [26624, end)
Feb 01 12:47:04  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 28672, batch.n_tokens = 2048, progress = 0.425401
Feb 01 12:47:15  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 28672, memory_seq_rm [28672, end)
Feb 01 12:47:15  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 30720, batch.n_tokens = 2048, progress = 0.455786
Feb 01 12:47:26  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 30720, memory_seq_rm [30720, end)
Feb 01 12:47:26  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 32768, batch.n_tokens = 2048, progress = 0.486172
Feb 01 12:47:38  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 32768, memory_seq_rm [32768, end)
Feb 01 12:47:38  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 34816, batch.n_tokens = 2048, progress = 0.516558
Feb 01 12:47:51  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 34816, memory_seq_rm [34816, end)
Feb 01 12:47:51  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 36864, batch.n_tokens = 2048, progress = 0.546944
Feb 01 12:48:05  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 36864, memory_seq_rm [36864, end)
Feb 01 12:48:05  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 38912, batch.n_tokens = 2048, progress = 0.577329
Feb 01 12:48:19  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 38912, memory_seq_rm [38912, end)
Feb 01 12:48:19  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 40960, batch.n_tokens = 2048, progress = 0.607715
Feb 01 12:48:34  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 40960, memory_seq_rm [40960, end)
Feb 01 12:48:34  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 43008, batch.n_tokens = 2048, progress = 0.638101
Feb 01 12:48:50  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 43008, memory_seq_rm [43008, end)
Feb 01 12:48:50  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 45056, batch.n_tokens = 2048, progress = 0.668487
Feb 01 12:49:06  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 45056, memory_seq_rm [45056, end)
Feb 01 12:49:06  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 47104, batch.n_tokens = 2048, progress = 0.698872
Feb 01 12:49:23  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 47104, memory_seq_rm [47104, end)
Feb 01 12:49:23  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 49152, batch.n_tokens = 2048, progress = 0.729258
Feb 01 12:49:41  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 49152, memory_seq_rm [49152, end)
Feb 01 12:49:41  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 51200, batch.n_tokens = 2048, progress = 0.759644
Feb 01 12:49:59  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 51200, memory_seq_rm [51200, end)
Feb 01 12:49:59  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 53248, batch.n_tokens = 2048, progress = 0.790030
Feb 01 12:50:18  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 53248, memory_seq_rm [53248, end)
Feb 01 12:50:18  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 55296, batch.n_tokens = 2048, progress = 0.820415
Feb 01 12:50:38  lemonade-server[2027]: slot update_slots: id  3 | task 0 | n_tokens = 55296, memory_seq_rm [55296, end)
Feb 01 12:50:38  lemonade-server[2027]: slot update_slots: id  3 | task 0 | prompt processing progress, n_tokens = 57344, batch.n_tokens = 2048, progress = 0.850801
```

```
# Token Processing Analysis Report

## Processing Statistics

| Metric | Value |
|--------|-------|
| Total Tokens Processed | 57,344 |
| Batch Size | 2,048 tokens |
| Total Processing Time | ~5 minutes 40 seconds |
| Average Tokens per Second | ~164 tokens/sec |
| Minimum Tokens per Second | ~102 tokens/sec |
| Maximum Tokens per Second | ~227 tokens/sec |

### Tokens Per Second Calculation

Based on the processing timeline, the tokens per second values for each interval:
- 2,048 tokens / 2 seconds = 1,024 tokens/sec
- 2,048 tokens / 4 seconds = 512 tokens/sec  
- 2,048 tokens / 7 seconds = 292.6 tokens/sec
- 2,048 tokens / 9 seconds = 227.6 tokens/sec
- 2,048 tokens / 11 seconds = 186.2 tokens/sec
- 2,048 tokens / 12 seconds = 170.7 tokens/sec
- 2,048 tokens / 13 seconds = 157.5 tokens/sec
- 2,048 tokens / 14 seconds = 146.3 tokens/sec
- 2,048 tokens / 15 seconds = 136.5 tokens/sec
- 2,048 tokens / 16 seconds = 128 tokens/sec
- 2,048 tokens / 17 seconds = 120.5 tokens/sec
- 2,048 tokens / 18 seconds = 113.8 tokens/sec
- 2,048 tokens / 19 seconds = 107.8 tokens/sec
- 2,048 tokens / 20 seconds = 102.4 tokens/sec

Overall average: ~164 tokens/sec

## Processing Timeline

| Timestamp | Time (seconds) | Token Count | Progress (%) | Time Interval (seconds) |
|-----------|----------------|-------------|--------------|------------------------|
| Feb 01 12:45:52 | 0.00 | 0 | 0.00% | - |
| Feb 01 12:45:52 | 0.00 | 2,048 | 3.04% | 0.00 |
| Feb 01 12:45:54 | 2.00 | 4,096 | 6.08% | 2.00 |
| Feb 01 12:45:56 | 4.00 | 6,144 | 9.12% | 2.00 |
| Feb 01 12:45:59 | 7.00 | 8,192 | 12.15% | 3.00 |
| Feb 01 12:46:02 | 10.00 | 10,240 | 15.19% | 3.00 |
| Feb 01 12:46:06 | 14.00 | 12,288 | 18.23% | 4.00 |
| Feb 01 12:46:11 | 19.00 | 14,336 | 21.27% | 5.00 |
| Feb 01 12:46:16 | 24.00 | 16,384 | 24.31% | 5.00 |
| Feb 01 12:46:23 | 31.00 | 18,432 | 27.35% | 7.00 |
| Feb 01 12:46:30 | 38.00 | 20,480 | 30.39% | 7.00 |
| Feb 01 12:46:37 | 45.00 | 22,528 | 33.42% | 7.00 |
| Feb 01 12:46:46 | 54.00 | 24,576 | 36.46% | 9.00 |
| Feb 01 12:46:55 | 63.00 | 26,624 | 39.50% | 9.00 |
| Feb 01 12:47:04 | 72.00 | 28,672 | 42.54% | 9.00 |
| Feb 01 12:47:15 | 83.00 | 30,720 | 45.58% | 11.00 |
| Feb 01 12:47:26 | 94.00 | 32,768 | 48.62% | 11.00 |
| Feb 01 12:47:38 | 106.00 | 34,816 | 51.66% | 12.00 |
| Feb 01 12:47:51 | 119.00 | 36,864 | 54.69% | 13.00 |
| Feb 01 12:48:05 | 133.00 | 38,912 | 57.73% | 14.00 |
| Feb 01 12:48:19 | 147.00 | 40,960 | 60.77% | 14.00 |
| Feb 01 12:48:34 | 162.00 | 43,008 | 63.81% | 15.00 |
| Feb 01 12:48:50 | 178.00 | 45,056 | 66.85% | 16.00 |
| Feb 01 12:49:06 | 194.00 | 47,104 | 69.89% | 16.00 |
| Feb 01 12:49:23 | 211.00 | 49,152 | 72.93% | 17.00 |
| Feb 01 12:49:41 | 229.00 | 51,200 | 75.96% | 18.00 |
| Feb 01 12:49:59 | 247.00 | 53,248 | 79.00% | 18.00 |
| Feb 01 12:50:18 | 266.00 | 55,296 | 82.04% | 19.00 |
| Feb 01 12:50:38 | 286.00 | 57,344 | 85.08% | 20.00 |
```

### Operating System

NAME="Ubuntu" VERSION="24.04.3 LTS (Noble Numbat)"

### CPU

model name      : AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S   Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S   Name:                    gfx1151                               Marketing Name:          AMD Radeon Graphics                       Name:                    amdgcn-amd-amdhsa--gfx1151                Name:                    amdgcn-amd-amdhsa--gfx11-generic      Name:                    aie2p                                 Marketing Name:          RyzenAI-npu5  

### ROCm Version

rocm-core/noble,now 7.2.0.70200-43~24.04 amd64 [installed,automatic]

### ROCm Component

_No response_

### Steps to Reproduce

Using lemonade-server llama.cpp and rocm, load and significant context.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.15
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
      Size:                    32490760(0x1efc508) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32490760(0x1efc508) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32490760(0x1efc508) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32490760(0x1efc508) KB
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
  SDMA engine uCode::      14
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    100663296(0x6000000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    100663296(0x6000000) KB
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
  Name:                    aie2p                              
  Uuid:                    AIE-XX                             
  Marketing Name:          RyzenAI-npu5                       
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
      Size:                    32490760(0x1efc508) KB             
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
      Size:                    32490760(0x1efc508) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***             
```

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — winmutt (2026-03-08T11:10:31Z)

Hi @benrichard-amd and @ppanchad-amd , I was wondering if you had any thoughts on this. Is this a rocm issue or a llamacpp issue?

---
