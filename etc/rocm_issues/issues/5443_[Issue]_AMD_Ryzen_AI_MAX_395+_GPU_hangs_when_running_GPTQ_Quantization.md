# [Issue]: AMD Ryzen AI MAX 395+ GPU hangs when running GPTQ Quantization

> **Issue #5443**
> **状态**: closed
> **创建时间**: 2025-09-29T12:35:53Z
> **更新时间**: 2025-12-08T10:02:12Z
> **关闭时间**: 2025-12-08T10:02:12Z
> **作者**: big-yellow-duck
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5443

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- amd-nicknick

## 描述

### Problem Description

GPU Hangs when running GPTQ quantization

### Operating System

CachyOS Linux

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

6.4.4

### ROCm Component

HIP, rocBLAS

### Steps to Reproduce

Run docker with rocm 6.4.4 with pytorch 
```
docker run -it  --name rocm6.4.4_vllm \
  --device /dev/kfd \
  --device /dev/dri \
  --security-opt seccomp=unconfined \
  --net=host \
  rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1 bash 
```

# Install GPTQmodel to quantize weights
```
pip install -v gptqmodel --no-build-isolation
pip install logbar
pip install tokenicer
pip install device_smi
pip install random_word
```
# Run the script 
```
from gptqmodel import GPTQModel, QuantizeConfig
from datasets import load_dataset


# tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

MODEL_ID = "Qwen/Qwen3-30B-A3B-Instruct-2507"
QUANT_PATH ="Qwewn3-30B-A3B-Insturct-2507-4bit" 
# Select calibration dataset.
DATASET_ID = "HuggingFaceH4/ultrachat_200k"
DATASET_SPLIT = "train_sft"
NUM_CALIBRATION_SAMPLES = 512
MAX_SEQUENCE_LENGTH = 2048

# ds = load_dataset(DATASET_ID, split=DATASET_SPLIT).select(range(1024))['text']

calibration_dataset = load_dataset(
    "allenai/c4",
    data_files="en/c4-train.00001-of-01024.json.gz",
    split="train"
  ).select(range(1024))["text"]

quant_config = QuantizeConfig(bits=4, group_size=128)

model= GPTQModel.load(MODEL_ID, quant_config,)

model.quantize(calibration_dataset, batch_size=2)
model.save(QUANT_PATH)
```

# Error
Quantizing mlp.experts.14.up_proj in layer     [1 of 47] ██-------------------------------------------------------------| 0:19:08 / 7:39:12 [2/48] 4.2%Memory access fault by GPU node-1 (Agent handle: 0x556e9b7e3360) on address 0x7f52c3f5f000. Reason: Page not present or supervisor privilege.
HW Exception by GPU node-1 (Agent handle: 0x563e71f098b0) reason :GPU Hang
Aborted (core dumped)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
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
      Size:                    131009976(0x7cf0db8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131009976(0x7cf0db8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131009976(0x7cf0db8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131009976(0x7cf0db8) KB            
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
  Packet Processor uCode:: 31                                 
  SDMA engine uCode::      14                                 
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
*** Done ***             

### Additional Information

this is what i see in ```dmseg | grep amd``` 

[244504.829208] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[244546.988929] amdgpu: Freeing queue vital buffer 0x7f4445000000, queue evicted
[244546.988935] amdgpu: Freeing queue vital buffer 0x7f444d000000, queue evicted
[244546.988937] amdgpu: Freeing queue vital buffer 0x7f444f000000, queue evicted
[244546.988939] amdgpu: Freeing queue vital buffer 0x7f4450800000, queue evicted
[245848.086124] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[245848.086130] amdgpu 0000:c5:00.0: amdgpu:  in process python3 pid 2261545 thread python3 pid 2261545)
[245848.086131] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f52c3f5f000 from client 10
[245848.086133] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[245848.086135] amdgpu 0000:c5:00.0: amdgpu:     Faulty UTCL2 client ID: TCP (0x8)
[245848.086136] amdgpu 0000:c5:00.0: amdgpu:     MORE_FAULTS: 0x1
[245848.086137] amdgpu 0000:c5:00.0: amdgpu:     WALKER_ERROR: 0x0
[245848.086137] amdgpu 0000:c5:00.0: amdgpu:     PERMISSION_FAULTS: 0x3
[245848.086138] amdgpu 0000:c5:00.0: amdgpu:     MAPPING_ERROR: 0x0
[245848.086139] amdgpu 0000:c5:00.0: amdgpu:     RW: 0x0
[245848.086146] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[245848.086147] amdgpu 0000:c5:00.0: amdgpu:  in process python3 pid 2261545 thread python3 pid 2261545)
[245848.086147] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f52c3f7c000 from client 10
[245848.086154] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[245848.086154] amdgpu 0000:c5:00.0: amdgpu:  in process python3 pid 2261545 thread python3 pid 2261545)
[245848.086155] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f52c3f6b000 from client 10
[245848.086161] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[245848.086162] amdgpu 0000:c5:00.0: amdgpu:  in process python3 pid 2261545 thread python3 pid 2261545)
[245848.086162] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f52c3f68000 from client 10
[245848.086168] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[245848.086169] amdgpu 0000:c5:00.0: amdgpu:  in process python3 pid 2261545 thread python3 pid 2261545)
[245848.086169] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f52c3f59000 from client 10
[245848.086175] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[245848.086176] amdgpu 0000:c5:00.0: amdgpu:  in process python3 pid 2261545 thread python3 pid 2261545)
[245848.086176] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f52c3f61000 from client 10
[245848.086182] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[245848.086183] amdgpu 0000:c5:00.0: amdgpu:  in process python3 pid 2261545 thread python3 pid 2261545)
[245848.086183] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f52c3f64000 from client 10
[245848.086189] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[245848.086189] amdgpu 0000:c5:00.0: amdgpu:  in process python3 pid 2261545 thread python3 pid 2261545)
[245848.086190] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f52c3f6f000 from client 10
[245848.086196] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[245848.086196] amdgpu 0000:c5:00.0: amdgpu:  in process python3 pid 2261545 thread python3 pid 2261545)
[245848.086197] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f52c3f75000 from client 10
[245848.086202] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[245848.086203] amdgpu 0000:c5:00.0: amdgpu:  in process python3 pid 2261545 thread python3 pid 2261545)
[245848.086204] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f52c3f72000 from client 10
[245850.667623] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[245850.667629] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
[245850.667845] amdgpu 0000:c5:00.0: amdgpu: failed to suspend gangs from MES
[245850.667846] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[245850.667849] amdgpu 0000:c5:00.0: amdgpu: Suspending all queues failed
[245850.667871] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!
[245851.086396] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 4
[245851.086403] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 3
[245851.086404] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 2
[245851.086405] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[245851.086405] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 0
[245851.086441] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[245851.086454] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[245851.086463] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[245851.086464] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[245851.086473] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[245851.086479] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[245851.086484] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[245851.086488] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[245851.086494] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[245851.086501] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[245851.086505] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[245851.088427] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[245851.096704] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[245851.129821] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[245851.130359] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[245851.130361] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card0/device/devcoredump/data
[245851.130363] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[245851.139255] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[245851.151027] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09002600
[245851.157761] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[245851.157764] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[245851.157765] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[245851.157766] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[245851.157767] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[245851.157768] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[245851.157768] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[245851.157769] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[245851.157769] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[245851.157770] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[245851.157770] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[245851.157771] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[245851.157771] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[245851.157772] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[245851.157772] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[245851.157773] amdgpu 0000:c5:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[245851.160282] amdgpu 0000:c5:00.0: amdgpu: GPU reset(15) succeeded!
[245851.160291] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[245895.778362] amdgpu: Freeing queue vital buffer 0x7f52bd600000, queue evicted
[245895.778367] amdgpu: Freeing queue vital buffer 0x7f52c1400000, queue evicted
[245895.778367] amdgpu: Freeing queue vital buffer 0x7f52c3200000, queue evicted
[245895.778368] amdgpu: Freeing queue vital buffer 0x7f52c8e00000, queue evicted




---

## 评论 (15 条)

### 评论 #1 — ppanchad-amd (2025-09-29T13:53:05Z)

Hi @big-yellow-duck. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — big-yellow-duck (2025-09-29T14:26:00Z)

for more context. I've set the kernel flags to allow the more gtt memory 
GRUB_CMDLINE_LINUX_DEFAULT="nowatchdog nvme_load=YES zswap.enabled=0 splash loglevel=3 amd_iommu=off  ttm.pages_limit=31457280 ttm.page_pool_size=31457280"

I will reverting this then strictly test with other UMA values using the BIOS settings

---

### 评论 #3 — waltercool (2025-10-01T16:48:03Z)

Hi @big-yellow-duck ,

I would strongly recommend using the amd-ttm CLI for GTT management instead of manual handling:

https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#configure-shared-memory

For two reasons:
- You can take the exact values for APU GTT.
- Seems like page_pool_size is not required.

---

### 评论 #4 — big-yellow-duck (2025-10-02T08:33:36Z)

@waltercool  I've followed your advice to use ```amd-ttm cli``` but its not working as expected:

this is what I see in ```/etc/modprobe.d/ttm.conf``` when setting the ttm memory to 112 GB
```
options ttm pages_limit=29360128
```

I've reverted my ```GRUB_CMDLINE_LINUX_DEFAULT``` to defaults to make sure nothing's messing with it.

after rebooting ```amd-ttm``` shows this
```
$uv run amd-ttm
💻 Current TTM pages limit: 16376245 pages (62.47 GB)
💻 Total system memory: 124.94 GB

```
It seems like its not working in the mean time I got other stuff running with 112GB of gtt memory using this
```
GRUB_CMDLINE_LINUX_DEFAULT="nowatchdog nvme_load=YES zswap.enabled=0 splash loglevel=3 amd_iommu=off amdgpu.gttsize=114688 ttm.pages_limit=29360128"
```

using the UMA set to 96GB still causes gpu hangs.

will test and comeback soon.

---

### 评论 #5 — AntonBushmelev (2025-10-06T07:08:34Z)

same issue  Linux fedora 6.16.9-200.fc42.x86_64 #1 SMP PREEMPT_DYNAMIC Thu Sep 25 18:05:50 UTC 2025 x86_64 GNU/Linux AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
[  591.197925] amdgpu: Freeing queue vital buffer 0x7f5dc0600000, queue evicted
[  591.197933] amdgpu: Freeing queue vital buffer 0x7f5dc1800000, queue evicted
[  591.197934] amdgpu: Freeing queue vital buffer 0x7f5dc2600000, queue evicted


---

### 评论 #6 — reywang18 (2025-10-07T20:44:19Z)

Passing through an AMD GPU to a Docker container on a Linux host typically involves making the necessary device files accessible within the container. 
So you did the Pass thru setup here ?

---

### 评论 #7 — big-yellow-duck (2025-10-08T03:24:08Z)

yes bro. 

I'm using the rocm6.4.4 image like this:
```
docker run -it  \
  --device /dev/kfd \
  --device /dev/dri \
  --security-opt seccomp=unconfined \
  --net=host \
  -v /home/akk/.cache/huggingface:/root/.cache/huggingface \
  rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1 bash 
```

inside the container rocm-smi works when using it directly. 
```
$ rocm-smi


========================================= ROCm System Management Interface =========================================
=================================================== Concise Info ===================================================
Device  Node  IDs              Temp    Power     Partitions          SCLK  MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Socket)  (Mem, Compute, ID)                                                 
====================================================================================================================
0       1     0x1586,   51259  36.0°C  23.039W   N/A, N/A, 0         N/A   1000Mhz  0%   auto  N/A     34%    0%    
====================================================================================================================
=============================================== End of ROCm SMI Log ================================================
```


---

### 评论 #8 — ianbmacdonald (2025-10-21T12:44:50Z)

`[245850.667623] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND`

Isn't this the pending MES fix?

https://github.com/torvalds/linux/commit/1fb710793ce2619223adffaf981b1ff13cd48f17

---

### 评论 #9 — amd-nicknick (2025-10-22T08:08:15Z)

Hi @big-yellow-duck and @ianbmacdonald, I was able to repro this issue on my end. On some instance, it is indeed caused by long-running compute work that causes MES to misjudge as a hang scenario. This is resolvable with the MES fix. https://github.com/torvalds/linux/commit/1fb710793ce2619223adffaf981b1ff13cd48f17

But sometimes it seems the failure is caused by an actual page fault. Below is one example:
```
[63560.165384] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[63560.165405] amdgpu 0000:c4:00.0: amdgpu:  in process python pid 60775 thread python pid 60775)
[63560.165408] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ffd6c055000 from client 10
[63560.165412] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[63560.165414] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[63560.165415] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x1
[63560.165417] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x0
[63560.165418] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[63560.165419] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x0
[63560.165420] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x0
[63560.165447] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[63560.165449] amdgpu 0000:c4:00.0: amdgpu:  in process python pid 60775 thread python pid 60775)
[63560.165451] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ffd6c05d000 from client 10
[63560.165457] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[63560.165459] amdgpu 0000:c4:00.0: amdgpu:  in process python pid 60775 thread python pid 60775)
[63560.165460] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ffd6c038000 from client 10
[63560.165467] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[63560.165468] amdgpu 0000:c4:00.0: amdgpu:  in process python pid 60775 thread python pid 60775)
[63560.165470] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ffd6c04a000 from client 10
[63560.165476] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[63560.165478] amdgpu 0000:c4:00.0: amdgpu:  in process python pid 60775 thread python pid 60775)
[63560.165479] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ffd6c013000 from client 10
[63560.165485] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[63560.165487] amdgpu 0000:c4:00.0: amdgpu:  in process python pid 60775 thread python pid 60775)
[63560.165488] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ffd6c001000 from client 10
[63560.165493] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[63560.165495] amdgpu 0000:c4:00.0: amdgpu:  in process python pid 60775 thread python pid 60775)
[63560.165496] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ffd6c026000 from client 10
[63560.165502] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[63560.165503] amdgpu 0000:c4:00.0: amdgpu:  in process python pid 60775 thread python pid 60775)
[63560.165505] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ffd6c042000 from client 10
[63560.165511] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[63560.165513] amdgpu 0000:c4:00.0: amdgpu:  in process python pid 60775 thread python pid 60775)
[63560.165514] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ffd6bf5c000 from client 10
[63560.165520] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[63560.165522] amdgpu 0000:c4:00.0: amdgpu:  in process python pid 60775 thread python pid 60775)
[63560.165523] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ffd6bf6e000 from client 10
```

Could you please help capture your dmesg so we could make sure you're running into this page fault as well? I am investigating this fault, mine occurred during `torch.linalg.cholesky`, but it could be asynchronous HIP launches, so I need to take a look further.

Also, I recommend using ROCm 7 based PyTorch container moving forward, there is a lot of fixes for STH in ROCm 7 vs 6.4, the subsequent page fault I captured is with ROCm 7 container as well (`rocm/pytorch:rocm7.0.2_ubuntu24.04_py3.12_pytorch_release_2.8.0`). 

---

### 评论 #10 — ianbmacdonald (2025-10-28T02:03:27Z)

The page fault can be easily reproduced using the current [AMD vLLM image](https://hub.docker.com/layers/rocm/vllm/rocm7.0.0_vllm_0.10.2_20251006/images/sha256-94fd001964e1cf55c3224a445b1fb5be31a7dac302315255db8422d813edd7f5) (docker pull rocm/vllm:rocm7.0.0_vllm_0.10.2_20251006) trying to serve new [IBM Granite 4 H Small](ibm-granite/granite-4.0-h-small). 

```
[ 2648.208294] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[ 2648.208358] amdgpu 0000:c5:00.0: amdgpu:  in process VLLM::EngineCor pid 6030 thread VLLM::EngineCor pid 6030)
[ 2648.208372] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3827d5a000 from client 10
[ 2648.208385] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[ 2648.208396] amdgpu 0000:c5:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[ 2648.208406] amdgpu 0000:c5:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[ 2648.208414] amdgpu 0000:c5:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[ 2648.208423] amdgpu 0000:c5:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[ 2648.208432] amdgpu 0000:c5:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[ 2648.208441] amdgpu 0000:c5:00.0: amdgpu: 	 RW: 0x0
[ 2648.208463] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[ 2648.208478] amdgpu 0000:c5:00.0: amdgpu:  in process VLLM::EngineCor pid 6030 thread VLLM::EngineCor pid 6030)
[ 2648.208491] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3827f2d000 from client 10
[ 2648.208510] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[ 2648.208522] amdgpu 0000:c5:00.0: amdgpu:  in process VLLM::EngineCor pid 6030 thread VLLM::EngineCor pid 6030)
[ 2648.208537] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3827d81000 from client 10
[ 2648.208563] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[ 2648.208577] amdgpu 0000:c5:00.0: amdgpu:  in process VLLM::EngineCor pid 6030 thread VLLM::EngineCor pid 6030)
[ 2648.208592] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3827da8000 from client 10
[ 2648.208620] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[ 2648.208629] amdgpu 0000:c5:00.0: amdgpu:  in process VLLM::EngineCor pid 6030 thread VLLM::EngineCor pid 6030)
[ 2648.208639] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3827dcf000 from client 10
[ 2648.209064] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[ 2648.209302] amdgpu 0000:c5:00.0: amdgpu:  in process VLLM::EngineCor pid 6030 thread VLLM::EngineCor pid 6030)
[ 2648.209515] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3827f06000 from client 10
[ 2648.209728] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[ 2648.209934] amdgpu 0000:c5:00.0: amdgpu:  in process VLLM::EngineCor pid 6030 thread VLLM::EngineCor pid 6030)
[ 2648.210138] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3827df6000 from client 10
[ 2648.210361] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[ 2648.210565] amdgpu 0000:c5:00.0: amdgpu:  in process VLLM::EngineCor pid 6030 thread VLLM::EngineCor pid 6030)
[ 2648.210772] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3827d88000 from client 10
[ 2648.210980] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[ 2648.211184] amdgpu 0000:c5:00.0: amdgpu:  in process VLLM::EngineCor pid 6030 thread VLLM::EngineCor pid 6030)
[ 2648.211387] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3827f1d000 from client 10
[ 2648.211650] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[ 2648.211855] amdgpu 0000:c5:00.0: amdgpu:  in process VLLM::EngineCor pid 6030 thread VLLM::EngineCor pid 6030)
[ 2648.212061] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3827d90000 from client 10
[ 2650.759244] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[ 2650.759536] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
[ 2650.759671] amdgpu 0000:c5:00.0: amdgpu: failed to suspend gangs from MES
[ 2650.760004] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 2650.760169] amdgpu 0000:c5:00.0: amdgpu: Suspending all queues failed
[ 2650.760416] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!
[ 2651.448479] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 3
[ 2651.449034] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 2
[ 2651.449647] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[ 2651.450229] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 0
[ 2651.450592] amdgpu: Failed to quiesce KFD
[ 2651.467147] amdgpu: Freeing queue vital buffer 0x7f37f1c00000, queue evicted
[ 2651.467621] amdgpu: Freeing queue vital buffer 0x7f37f3200000, queue evicted
[ 2651.467854] amdgpu: Freeing queue vital buffer 0x7f3827000000, queue evicted
[ 2653.309745] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[ 2653.310355] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
[ 2653.310674] amdgpu 0000:c5:00.0: amdgpu: failed to suspend gangs from MES
[ 2653.311286] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[ 2653.312184] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 2653.312192] amdgpu 0000:c5:00.0: amdgpu: Suspending all queues failed
[ 2653.312215] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 2653.312221] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 2653.312225] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 2653.312226] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 2653.312228] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 2653.312230] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 2653.312231] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 2653.312233] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 2653.312235] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 2653.312236] amdgpu 0000:c5:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 2653.313421] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[ 2654.222255] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[ 2654.253631] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 2654.254301] [drm] PCIE GART of 512M enabled (table at 0x000000801FB00000).
[ 2654.254381] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[ 2654.254383] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card0/device/devcoredump/data
[ 2654.254386] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[ 2654.262093] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[ 2654.275090] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09002E00
[ 2654.332488] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 2654.332496] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 2654.332498] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 2654.332500] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 2654.332502] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 2654.332503] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 2654.332505] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 2654.332506] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 2654.332508] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 2654.332509] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 2654.332511] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 2654.332512] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[ 2654.332514] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[ 2654.332516] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[ 2654.332517] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 2654.332519] amdgpu 0000:c5:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[ 2654.376091] amdgpu 0000:c5:00.0: amdgpu: GPU reset(2) succeeded!
[ 2654.376337] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset

```
```
export HSA_OVERRIDE_GFX_VERSION=11.0.0
vllm serve ibm-granite/granite-4.0-h-small --compilation-config '{"cudagraph_mode":"PIECEWISE"}'

```
On [a current nightly](https://hub.docker.com/layers/rocm/vllm-dev/nightly_main_20251026/images/sha256-46d2e8735b4b619f02f7d8c3583071afa281b1cf3a018250fe3f16dbb5d60831) the HSA_OVERRIDE and compilation-config are no longer required, but the result is the same. 

```
sudo cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080

```

---

### 评论 #11 — big-yellow-duck (2025-10-28T06:14:02Z)

@amd-nicknick  I'll try using the image u suggested with the latest kernel I see the fix was backported to kernel 6.17.2 so it might work. I'll try it out and let u all know.

---

### 评论 #12 — ianbmacdonald (2025-10-28T16:27:50Z)

It is no different on Ubuntu, Debian, 6.12 thru 6.17 .. I have tested them all, also with variants of Pytorch (the rock, rocm7 nightlies).  Going to open a new issue with the easily reproducable insights so AMD can focus on the fix without variants from dynamically pulled wheels, and upstream git repos. 

---

### 评论 #13 — amd-nicknick (2025-10-29T07:38:38Z)

Hi @ianbmacdonald, I agree that page fault looks like something else that has nothing to do with LR compute. I saw you have opened a new issue. I will try your reproduce method and see if it's a same page fault to this one, thanks! 

---

### 评论 #14 — amd-nicknick (2025-11-11T08:22:42Z)

Hi @big-yellow-duck, on my local end, with the patched kernel, the GPTQ quantization will run out of memory before completion. Could you please help check if you will encounter this issue?

---

### 评论 #15 — amd-nicknick (2025-12-08T10:02:12Z)

Closing this issue due to inactivity, feel free to open a new issue if you have further question. Thanks!

---
