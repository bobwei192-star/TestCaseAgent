# [Issue]: Cannot set PwrCap for RX 7900 XTX

> **Issue #4360**
> **状态**: closed
> **创建时间**: 2025-02-09T09:47:19Z
> **更新时间**: 2025-03-01T15:03:34Z
> **关闭时间**: 2025-02-28T15:47:33Z
> **作者**: seesturm
> **标签**: Under Investigation, ROCm 6.2.0, AMD Radeon RX 7900XTX
> **URL**: https://github.com/ROCm/ROCm/issues/4360

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.0** (颜色: #ededed)
- **AMD Radeon RX 7900XTX** (颜色: #ededed)

## 描述

### Problem Description


I have a RX 7900 XTX which I want to use for long running tasks. The default PwrCap is 327W, which is producing way too much heat and noise for my use case. So I need to limit the power usage to 150W. With my Vega 56 I can set the power limit using "rocm-smi --setpoweroverdrive <value>".

But with the RX 7900 XTX this does not work. `The rocm-smi` tool seems to do nothing. After setting the new limit the old limit (327W) is still in effect.

### Operating System

Ubuntu 24.04.1 LTS (Noble Numbat)

### CPU

AMD Ryzen Threadripper 1950X 16-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.2

### ROCm Component

rocm_smi_lib

### Steps to Reproduce

Query current PwrCap
```
$ rocm-smi
========================================== ROCm System Management Interface ==========================================
==================================================== Concise Info ====================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK     MCLK    Fan    Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                     
======================================================================================================================
0       2     0x744c,   47942  33.0°C  72.0W  N/A, N/A, 0         1502Mhz  96Mhz   20.0%  auto  327.0W  0%     31%   
1       3     0x687f,   35091  56.0°C  10.0W  N/A, N/A, 0         852Mhz   800Mhz  9.41%  auto  100.0W  7%     0%    
======================================================================================================================
================================================ End of ROCm SMI Log ================================================
```

Set new PwrCap to 150W for device 0. This has no effect.
```
$ rocm-smi -d 0 --setpoweroverdrive 150


============================ ROCm System Management Interface ============================
================================ Set GPU Power OverDrive =================================
==========================================================================================
================================== End of ROCm SMI Log ===================================
```


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module version 6.10.5 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.14
Runtime Ext Version:     1.6
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen Threadripper 1950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen Threadripper 1950X 16-Core Processor
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
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3400                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32828796(0x1f4ed7c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32828796(0x1f4ed7c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32828796(0x1f4ed7c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD Ryzen Threadripper 1950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen Threadripper 1950X 16-Core Processor
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3400                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32956804(0x1f6e184) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32956804(0x1f6e184) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32956804(0x1f6e184) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-3473c371150209ba               
  Marketing Name:          AMD Radeon RX 7900 XTX             
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
    L2:                      6144(0x1800) KB                    
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2482                               
  BDFID:                   3328                               
  Internal Node ID:        2                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 412                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*******                  
Agent 4                  
*******                  
  Name:                    gfx900                             
  Uuid:                    GPU-021500f10f942104               
  Marketing Name:          AMD Radeon RX Vega                 
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
    L1:                      16(0x10) KB                        
    L2:                      4096(0x1000) KB                    
  Chip ID:                 26751(0x687f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1590                               
  BDFID:                   17664                              
  Internal Node ID:        3                                  
  Compute Unit:            56                                 
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
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 472                                
  SDMA engine uCode::      434                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    8372224(0x7fc000) KB               
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
      Name:                    amdgcn-amd-amdhsa--gfx900:xnack-   
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
*** Done ***             
```

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — IMbackK (2025-02-10T09:20:26Z)

The kernel enforces the minimum from the cards vbios, some cards have a minimum that is the same as default, you can check this by looking at the files in /sys/class/drm/card0/device/hwmon/hwmon*

---

### 评论 #2 — harkgill-amd (2025-02-10T17:02:04Z)

Hi @seesturm, please note that rocm-smi is planned to be deprecated and it's recommended to use the new amd-smi tool instead. To set the GPUs power cap, the relevant amd-smi command would be
```
sudo amd-smi set -g 0 --power-cap <WATTS>
```
This command will also print out the minimum and maximum power caps that are configurable if a valid value is not passed. For example with a 7900XTX on ROCm 6.3.2
```
GPU: 0
    POWERCAP: Power cap must be between 272 and 402
```
Please give this a try and let me know if this resolves your issue.

---

### 评论 #3 — seesturm (2025-02-10T17:09:30Z)

Using the new command I still cannot set 150W PwrCap.

```
$ amd-smi set -g 0 --power-cap 150
GPU: 0
    POWERCAP: Power cap must be between 294 and 350
```

---

### 评论 #4 — harkgill-amd (2025-02-10T19:39:08Z)

The preset minimum and maximum limits are set by the VBIOS, as mentioned by @IMbackK, to help ensure there is no damage to the GPU when configuring the power cap. In your case, the valid range is between 294 and 350 which is a HW limitation.

Any value outside of this range will not be set when running the amd-smi command as highlighted in the error message.

---

### 评论 #5 — IMbackK (2025-02-10T20:05:59Z)

@seesturm you CAN make the kernel ignore the limit of course, however this could conceivably cause damage so you have to accept full responsibility for doing so and i will not explicitly recommend taking this path. A possible patch to amdgpu to do so is below:

```
From 8dcdcc54b0dddec106bb9b68b2bba2c725c84c7b Mon Sep 17 00:00:00 2001
From: Steven Barrett <steven@liquorix.net>
Date: Fri, 15 Mar 2024 12:36:51 -0500
Subject: [PATCH] ZEN: drm/amdgpu/pm: Allow override of min_power_limit with
 ignore_min_pcap

---
 drivers/gpu/drm/amd/amdgpu/amdgpu.h       |  1 +
 drivers/gpu/drm/amd/amdgpu/amdgpu_drv.c   | 10 ++++++++++
 drivers/gpu/drm/amd/pm/amdgpu_pm.c        |  3 +++
 drivers/gpu/drm/amd/pm/swsmu/amdgpu_smu.c | 14 ++++++++++++--
 4 files changed, 26 insertions(+), 2 deletions(-)

diff --git a/drivers/gpu/drm/amd/amdgpu/amdgpu.h b/drivers/gpu/drm/amd/amdgpu/amdgpu.h
index f87d53e183c3d0..c489d3b2576b13 100644
--- a/drivers/gpu/drm/amd/amdgpu/amdgpu.h
+++ b/drivers/gpu/drm/amd/amdgpu/amdgpu.h
@@ -159,6 +159,7 @@ struct amdgpu_watchdog_timer {
  */
 extern int amdgpu_modeset;
 extern unsigned int amdgpu_vram_limit;
+extern int amdgpu_ignore_min_pcap;
 extern int amdgpu_vis_vram_limit;
 extern int amdgpu_gart_size;
 extern int amdgpu_gtt_size;
diff --git a/drivers/gpu/drm/amd/amdgpu/amdgpu_drv.c b/drivers/gpu/drm/amd/amdgpu/amdgpu_drv.c
index ea14f1c8f43044..bb0b636d0d75cb 100644
--- a/drivers/gpu/drm/amd/amdgpu/amdgpu_drv.c
+++ b/drivers/gpu/drm/amd/amdgpu/amdgpu_drv.c
@@ -132,6 +132,7 @@ enum AMDGPU_DEBUG_MASK {
 };

 unsigned int amdgpu_vram_limit = UINT_MAX;
+int amdgpu_ignore_min_pcap = 0; /* do not ignore by default */
 int amdgpu_vis_vram_limit;
 int amdgpu_gart_size = -1; /* auto */
 int amdgpu_gtt_size = -1; /* auto */
@@ -243,6 +244,15 @@ struct amdgpu_watchdog_timer amdgpu_watchdog_timer = {
 	.period = 0x0, /* default to 0x0 (timeout disable) */
 };

+/**
+ * DOC: ignore_min_pcap (int)
+ * Ignore the minimum power cap.
+ * Useful on graphics cards where the minimum power cap is very high.
+ * The default is 0 (Do not ignore).
+ */
+MODULE_PARM_DESC(ignore_min_pcap, "Ignore the minimum power cap");
+module_param_named(ignore_min_pcap, amdgpu_ignore_min_pcap, int, 0600);
+
 /**
  * DOC: vramlimit (int)
  * Restrict the total amount of VRAM in MiB for testing.  The default is 0 (Use full VRAM).
diff --git a/drivers/gpu/drm/amd/pm/amdgpu_pm.c b/drivers/gpu/drm/amd/pm/amdgpu_pm.c
index c11952a4389bcb..52f54a228b39c7 100644
--- a/drivers/gpu/drm/amd/pm/amdgpu_pm.c
+++ b/drivers/gpu/drm/amd/pm/amdgpu_pm.c
@@ -3155,6 +3155,9 @@ static ssize_t amdgpu_hwmon_show_power_cap_min(struct device *dev,
 					 struct device_attribute *attr,
 					 char *buf)
 {
+	if (amdgpu_ignore_min_pcap)
+		return sysfs_emit(buf, "%i\n", 0);
+
 	return amdgpu_hwmon_show_power_cap_generic(dev, attr, buf, PP_PWR_LIMIT_MIN);
 }

diff --git a/drivers/gpu/drm/amd/pm/swsmu/amdgpu_smu.c b/drivers/gpu/drm/amd/pm/swsmu/amdgpu_smu.c
index e1796ecf9c05c4..5e46bd2932059b 100644
--- a/drivers/gpu/drm/amd/pm/swsmu/amdgpu_smu.c
+++ b/drivers/gpu/drm/amd/pm/swsmu/amdgpu_smu.c
@@ -2749,7 +2749,10 @@ int smu_get_power_limit(void *handle,
 			*limit = smu->max_power_limit;
 			break;
 		case SMU_PPT_LIMIT_MIN:
-			*limit = smu->min_power_limit;
+			if (amdgpu_ignore_min_pcap)
+				*limit = 0;
+			else
+				*limit = smu->min_power_limit;
 			break;
 		default:
 			return -EINVAL;
@@ -2773,7 +2776,14 @@ static int smu_set_power_limit(void *handle, uint32_t limit)
 		if (smu->ppt_funcs->set_power_limit)
 			return smu->ppt_funcs->set_power_limit(smu, limit_type, limit);

-	if ((limit > smu->max_power_limit) || (limit < smu->min_power_limit)) {
+	if (amdgpu_ignore_min_pcap) {
+		if ((limit > smu->max_power_limit)) {
+			dev_err(smu->adev->dev,
+				"New power limit (%d) is over the max allowed %d\n",
+				limit, smu->max_power_limit);
+			return -EINVAL;
+		}
+	} else if ((limit > smu->max_power_limit) || (limit < smu->min_power_limit)) {
 		dev_err(smu->adev->dev,
 			"New power limit (%d) is out of range [%d,%d]\n",
 			limit, smu->min_power_limit, smu->max_power_limit);
```

---

### 评论 #6 — harkgill-amd (2025-02-28T15:48:30Z)

Closed issue as power cap can be successfully set within expected boundaries.

---

### 评论 #7 — seesturm (2025-02-28T17:53:27Z)

> The preset minimum and maximum limits are set by the VBIOS, as mentioned by [@IMbackK](https://github.com/IMbackK), to help ensure there is no damage to the GPU when configuring the power cap. In your case, the valid range is between 294 and 350 which is a HW limitation.
> 
> Any value outside of this range will not be set when running the amd-smi command as highlighted in the error message.

So you are saying AMD intentionally allows their board partners to manufacture such cards? How to find out before purchase what the limits are?

---

### 评论 #8 — seesturm (2025-02-28T17:59:14Z)

Just to give a bit of additional context: This is the current top of the line AMD consumer graphics card currently available. The limitation is totally surprising and makes the device unusable for my compute use-case. My previous Vega 56 device didn't have such a limitation.

---

### 评论 #9 — IMbackK (2025-03-01T12:15:54Z)

Your vega56 did have this limitation in its vbios, the kernel just ignored it in previous versions.

---

### 评论 #10 — seesturm (2025-03-01T15:03:34Z)

> Your vega56 did have this limitation in its vbios, the kernel just ignored it in previous versions.

This is not true. I can set any limit between 1 and 165 with my Vega 56
```
$ sudo amd-smi set -g 1 --power-cap 200
GPU: 1
    POWERCAP: Power cap must be between 1 and 165

```

---
