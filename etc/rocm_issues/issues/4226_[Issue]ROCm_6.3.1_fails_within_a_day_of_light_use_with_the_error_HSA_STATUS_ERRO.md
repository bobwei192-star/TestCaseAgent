# [Issue]:ROCm 6.3.1 fails within a day of light use with the error HSA_STATUS_ERROR_OUT_OF_RESOURCES

> **Issue #4226**
> **状态**: closed
> **创建时间**: 2025-01-06T11:39:05Z
> **更新时间**: 2025-06-04T07:11:21Z
> **关闭时间**: 2025-05-01T14:34:26Z
> **作者**: pkautio
> **标签**: Under Investigation, ROCm 6.3.0, Radeon Pro W7800
> **URL**: https://github.com/ROCm/ROCm/issues/4226

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.0** (颜色: #ededed)
- **Radeon Pro W7800** (颜色: #ededed)

## 描述

### Problem Description

After booting the system Ollama (latest version) works fine less than one day. After that it cannot allocate GPU resources anymore and fails to start Llama 3.3 70b (or any other LLM). 

Running rocminfo in this situation gives error:
"hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1306
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events."

Rebooting system fixes the problem, which comes back within one day of restart.

System is on latest Ubuntu 24.04.1 LTS with all the fixes applied. Rocm 6.3.1 installed with all amdgpu driver updates. With 6.3.0 the issue was the same. Rocm docs says that Ubuntu 24.04.2 LTS should be used, but such a version is not yet available (is there a documentation error?)

echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";
  echo "CPU: " && cat /proc/cpuinfo | grep "model name" | sort --unique;
  echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
OS:
NAME="Ubuntu"
VERSION="24.04.1 LTS (Noble Numbat)"
CPU: 
model name	: AMD EPYC 7C13 64-Core Processor
GPU:
  Name:                    AMD EPYC 7C13 64-Core Processor    
  Marketing Name:          AMD EPYC 7C13 64-Core Processor    
  Name:                    gfx1100                            
  Marketing Name:          AMD Radeon PRO W7800               
      Name:                    amdgcn-amd-amdhsa--gfx1100 





### Operating System

Ubuntu 24.04.1 LTS

### CPU

AMD EPYC 7C13

### GPU

Radeon Pro W7800

### ROCm Version

ROCm 6.3.0

### ROCm Component

rocminfo

### Steps to Reproduce

rocminfo

Also, Ollama fails to use rocm.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    AMD EPYC 7C13 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7C13 64-Core Processor    
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
  Max Clock Freq. (MHz):   2000                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            128                                
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    527983364(0x1f786304) KB           
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    527983364(0x1f786304) KB           
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    527983364(0x1f786304) KB           
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    527983364(0x1f786304) KB           
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-10d1c27f5067cb9a               
  Marketing Name:          AMD Radeon PRO W7800               
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
    L2:                      6144(0x1800) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 29790(0x745e)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1895                               
  BDFID:                   33536                              
  Internal Node ID:        1                                  
  Compute Unit:            70                                 
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
      Size:                    31440896(0x1dfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    31440896(0x1dfc000) KB             
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
*** Done ***  

### Additional Information

_No response_

---

## 评论 (36 条)

### 评论 #1 — ppanchad-amd (2025-01-06T15:01:23Z)

Hi @pkautio. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — tuxology (2025-01-09T18:03:46Z)

I can replicate this exact same issue on my system as well on exactly the same workload, but different GPU & OS. Both listed as supported. After almost a day's light use, the GPU is inaccessible. Here are my specs:

```
OS:
NAME="Red Hat Enterprise Linux"
VERSION="9.5 (Plow)"

CPU: 
model name      : AMD Ryzen 9 5950X 16-Core Processor

GPU: 7900 XT
```

Here are the kernel logs for additional info. @pkautio Do you have same kernel logs? 

```
$ dmesg

[200584.540184] pcieport 0000:08:00.0: Unable to change power state from D3hot to D0, device inaccessible
[200584.542122] pcieport 0000:09:00.0: Unable to change power state from D3hot to D0, device inaccessible
[200584.544050] amdgpu 0000:0a:00.0: Unable to change power state from D3hot to D0, device inaccessible
[200588.950412] [drm:gmc_v11_0_flush_gpu_tlb [amdgpu]] *ERROR* Timeout waiting for sem acquire in VM flush!
[200589.106207] amdgpu 0000:0a:00.0: amdgpu: Timeout waiting for VM flush ACK!
[200589.106210] [drm] PCIE GART of 512M enabled (table at 0x0000008000300000).
[200589.106227] amdgpu 0000:0a:00.0: amdgpu: PSP is resuming...
[200589.146583] amdgpu 0000:0a:00.0: amdgpu: reserve 0x1300000 from 0x84fc000000 for PSP TMR
[200589.146791] amdgpu 0000:0a:00.0: amdgpu: RAS Init Status: 0xFFFFFFFF
[200589.146910] amdgpu 0000:0a:00.0: amdgpu: RAP: optional rap ta ucode is not available
[200589.146912] amdgpu 0000:0a:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[200589.146914] amdgpu 0000:0a:00.0: amdgpu: SMU is resuming...
[200589.146919] amdgpu 0000:0a:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e7f00 (78.127.0)
[200589.146923] amdgpu 0000:0a:00.0: amdgpu: SMU driver if version not matched
[200589.146929] amdgpu 0000:0a:00.0: amdgpu: SMU is resumed successfully!
[200589.303208] amdgpu 0000:0a:00.0: amdgpu: rlc autoload: gc ucode autoload timeout
[200589.303212] amdgpu 0000:0a:00.0: amdgpu: (-110) failed to wait rlc autoload complete
[200589.303216] [drm:amdgpu_device_ip_resume_phase2 [amdgpu]] *ERROR* resume of IP block <gfx_v11_0> failed -110
[200589.303338] amdgpu 0000:0a:00.0: amdgpu: amdgpu_device_ip_resume failed (-110).
[201072.164685] [drm:gmc_v11_0_flush_gpu_tlb [amdgpu]] *ERROR* Timeout waiting for sem acquire in VM flush!
[201072.321476] amdgpu 0000:0a:00.0: amdgpu: Timeout waiting for VM flush ACK!
[201075.365552] amdgpu 0000:0a:00.0: amdgpu: MES failed to respond to msg=MISC (SET_SHADER_DEBUGGER)
[201075.365562] [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
[201075.521484] [drm:gmc_v11_0_flush_gpu_tlb [amdgpu]] *ERROR* Timeout waiting for sem acquire in VM flush!
[201075.677408] amdgpu 0000:0a:00.0: amdgpu: Timeout waiting for VM flush ACK!
```  





---

### 评论 #3 — sohaibnd (2025-01-10T20:28:06Z)

Hi @pkautio @tuxology, I am trying to reproduce this issue so I want to confirm the steps to follow:

1. Start the model with `ollama run llama3.3`
2. Give it some prompts, then exit the session when done with `/bye` but keep the model running
3. Keep the system on for around a day
4. Then run `rocminfo` and observe the HSA_STATUS_ERROR_OUT_OF_RESOURCES error

Am I missing anything? Also, are you able to reproduce this issue consistently by following these steps?


---

### 评论 #4 — tuxology (2025-01-10T22:19:41Z)

@sohaibnd These are the exact steps except in step 2, I am using Ollama via API calls and not on the ollama shell. I have now also tested on different models. It fails on `llama3.2-vision`, `qwen-2.5-coder:14b` as well and can reproduce this. 

---

### 评论 #5 — sohaibnd (2025-01-10T23:11:01Z)

Thanks, I'll try to reproduce this and get back to you with an update.

---

### 评论 #6 — pkautio (2025-01-11T07:18:39Z)

> Hi @pkautio @tuxology, I am trying to reproduce this issue so I want to confirm the steps to follow:
> 
> 
> 
> 1. Start the model with `ollama run llama3.3`
> 
> 2. Give it some prompts, then exit the session when done with `/bye` but keep the model running
> 
> 3. Keep the system on for around a day
> 
> 4. Then run `rocminfo` and observe the HSA_STATUS_ERROR_OUT_OF_RESOURCES error
> 
> 
> 
> Am I missing anything? Also, are you able to reproduce this issue consistently by following these steps?
> 
> 

Yes, these are the exact steps to reproduce this.

There are some Ollama logs too indicating that it is unable to free allocated Rocm memory. I will copy them here later today.

And yes, the issue happens consistently every time. I am never able to use the system for Ollama more than one day.

I'm also using Ollama through API, but Ollama run should behave in a same way.

Rocm 6.3.0 and 6.3.1 both behave in a same way.

---

### 评论 #7 — pkautio (2025-01-12T09:45:23Z)

> I can replicate this exact same issue on my system as well on exactly the same workload, but different GPU & OS. Both listed as supported. After almost a day's light use, the GPU is inaccessible. Here are my specs:
> 
> ```
> OS:
> NAME="Red Hat Enterprise Linux"
> VERSION="9.5 (Plow)"
> 
> CPU: 
> model name      : AMD Ryzen 9 5950X 16-Core Processor
> 
> GPU: 7900 XT
> ```
> 
> Here are the kernel logs for additional info. @pkautio Do you have same kernel logs?
> 
> ```
> $ dmesg

Quite similiar errors:

[326845.787414] amdgpu 0000:83:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000017 SMN_C2PMSG_82:0x00000003
[326845.787424] amdgpu 0000:83:00.0: amdgpu: Failed to exit BACO state!
[326850.861825] amdgpu 0000:83:00.0: amdgpu: Timeout waiting for VM flush ACK!
[326850.861832] [drm] PCIE GART of 512M enabled (table at 0x000000877EB00000).
[326850.861925] amdgpu 0000:83:00.0: amdgpu: PSP is resuming...
[326854.676595] amdgpu 0000:83:00.0: amdgpu: PSP load kdb failed!
[326854.676604] amdgpu 0000:83:00.0: amdgpu: PSP resume failed
[326854.676607] [drm:amdgpu_device_fw_loading [amdgpu]] *ERROR* resume of IP block <psp> failed -62
[326854.676843] amdgpu 0000:83:00.0: amdgpu: amdgpu_device_ip_resume failed (-62).
[326854.835289] rfkill: input handler enabled
[326855.830424] rfkill: input handler disabled

I got this after:
ollama run llama3.1:latest
ask something
/bye

... and by waiting to next morning. Rocminfo gives the error "HSA_STATUS_ERROR_OUT_OF_RESOURCES".


---

### 评论 #8 — sohaibnd (2025-01-13T21:20:11Z)

@tuxology @pkautio Thanks for the information. I tried following the steps above but am not able to reproduce the same error. Are you running Ollama on bare metal OS or from inside a VM or Docker? Can you also share the entire kernel log?

Based on the logs and steps to reproduce, it could be a sleep issue. Can you also check which sleep states are supported by your system (`cat /sys/power/state` and `cat /sys/power/mem_sleep`). Then, try following the steps to reproduce above except replace step 3 with putting your system into a supported sleep state manually and then waking it back up. See [here](https://www.kernel.org/doc/html/v5.2/admin-guide/pm/sleep-states.html) on how to set different sleep states. For example, you can put your system in the suspend-to-idle state (if supported) with `echo freeze > /sys/power/state`. Let me know if you are able to reproduce the same issue with any of the sleep states.



---

### 评论 #9 — sohaibnd (2025-01-13T22:41:45Z)

@tuxology @pkautio You are both using a single GPU right? Can you please also include the output from rocm-smi that you get when you reproduce the original issue.



---

### 评论 #10 — tuxology (2025-01-15T20:24:15Z)

> [@tuxology](https://github.com/tuxology) [@pkautio](https://github.com/pkautio) You are both using a single GPU right? Can you please also include the output from rocm-smi that you get when you reproduce the original issue.

I have a single GPU only. Running this on baremetal. I am going to try setting up different sleep state and paste my results here

1. rocm-smi before I have the issue:

```
$ rocm-smi


======================================== ROCm System Management Interface ========================================
================================================== Concise Info ==================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK    MCLK   Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                 
==================================================================================================================
0       1     0x744c,   34156  32.0°C  58.0W  N/A, N/A, 0         527Mhz  96Mhz  0%   auto  257.0W  0%     15%   
==================================================================================================================
============================================== End of ROCm SMI Log ===============================================
```

2. Checking sleep states

```
$ cat /sys/power/state
freeze mem disk

$ cat /sys/power/mem_sleep 
s2idle [deep]
```

3. Setting sleep state to `s2idle`

```
echo freeze > /sys/power/state
```

Machine compeltely freezes. Nothing on UI. The GPU is at max power utilization. 

4. Hard restart machine, Ollama has started and serving one model

```
Jan 14 19:05:43 tor-1 ollama[1672]: time=2025-01-14T19:05:43.713-05:00 level=INFO source=routes.go:1310 msg="Listening on 127.0.0.1:11434 (version 0.5.4)"
Jan 14 19:05:43 tor-1 ollama[1672]: time=2025-01-14T19:05:43.713-05:00 level=INFO source=routes.go:1339 msg="Dynamic LLM libraries" runners="[cuda_v11_avx cuda_v12_avx rocm_avx cpu cpu_avx cpu_avx2]"
Jan 14 19:05:43 tor-1 ollama[1672]: time=2025-01-14T19:05:43.713-05:00 level=INFO source=gpu.go:226 msg="looking for compatible GPUs"
Jan 14 19:05:43 tor-1 ollama[1672]: time=2025-01-14T19:05:43.721-05:00 level=INFO source=amd_linux.go:388 msg="amdgpu is supported" gpu=GPU-e423b557db994259 gpu_type=gfx1100
Jan 14 19:05:43 tor-1 ollama[1672]: time=2025-01-14T19:05:43.725-05:00 level=INFO source=types.go:131 msg="inference compute" id=GPU-e423b557db994259 library=rocm variant="" compute=gfx1100 driver=6.10 name=1002:744c total="20.0 GiB" available="20.0 GiB"
```

5. Wait for 3-4 hours. Observe that GPU fan has started spinning faster and machine is idle. Check `rocm-smi`

```
$ rocm-smi


Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
========================================== ROCm System Management Interface ==========================================
==================================================== Concise Info ====================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK  MCLK  Fan  Perf     PwrCap       VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                      
======================================================================================================================
0       1     0x744c,   34156  N/A     N/A    N/A, N/A, 0         None  None  0%   unknown  Unsupported  0%     0%    
======================================================================================================================
================================================ End of ROCm SMI Log =================================================
```

6. Check kernel logs

```
[ 4155.542753] amdgpu 0000:0a:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[ 4155.545610] amdgpu 0000:0a:00.0: [drm] Cannot find any crtc or sizes
[ 4155.546437] [drm] ring gfx_32771.1.1 was added
[ 4155.546862] [drm] ring compute_32771.2.2 was added
[ 4155.547257] [drm] ring sdma_32771.3.3 was added
[ 4155.547298] [drm] ring gfx_32771.1.1 ib test pass
[ 4155.547329] [drm] ring compute_32771.2.2 ib test pass
[ 4155.547425] [drm] ring sdma_32771.3.3 ib test pass
[11186.057666] [drm] PCIE GART of 512M enabled (table at 0x0000008000300000).
[11186.057726] amdgpu 0000:0a:00.0: amdgpu: PSP is resuming...
[11186.117205] amdgpu 0000:0a:00.0: amdgpu: reserve 0x1300000 from 0x84fc000000 for PSP TMR
[11186.261728] amdgpu 0000:0a:00.0: amdgpu: RAP: optional rap ta ucode is not available
[11186.261732] amdgpu 0000:0a:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[11186.261735] amdgpu 0000:0a:00.0: amdgpu: SMU is resuming...
[11186.261740] amdgpu 0000:0a:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e7f00 (78.127.0)
[11186.261743] amdgpu 0000:0a:00.0: amdgpu: SMU driver if version not matched
[11186.397788] amdgpu 0000:0a:00.0: amdgpu: SMU is resumed successfully!
[11186.406935] [drm] DMUB hardware initialized: version=0x07002A00
[11186.413564] amdgpu 0000:0a:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[11186.413566] amdgpu 0000:0a:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[11186.413568] amdgpu 0000:0a:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[11186.413569] amdgpu 0000:0a:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[11186.413570] amdgpu 0000:0a:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[11186.413571] amdgpu 0000:0a:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[11186.413573] amdgpu 0000:0a:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[11186.413574] amdgpu 0000:0a:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[11186.413575] amdgpu 0000:0a:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[11186.413576] amdgpu 0000:0a:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[11186.413577] amdgpu 0000:0a:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[11186.413579] amdgpu 0000:0a:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[11186.413580] amdgpu 0000:0a:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[11186.413581] amdgpu 0000:0a:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[11186.413583] amdgpu 0000:0a:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[11186.416252] amdgpu 0000:0a:00.0: [drm] Cannot find any crtc or sizes
[11186.416874] [drm] ring gfx_32771.1.1 was added
[11186.417275] [drm] ring compute_32771.2.2 was added
[11186.417643] [drm] ring sdma_32771.3.3 was added
[11186.417684] [drm] ring gfx_32771.1.1 ib test pass
[11186.417717] [drm] ring compute_32771.2.2 ib test pass
[11186.417802] [drm] ring sdma_32771.3.3 ib test pass
[39535.436980] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:23 param:0x00000003 message:ArmD3?
[39535.436993] amdgpu 0000:0a:00.0: amdgpu: Failed to exit BACO state!
[39540.088346] [drm] PCIE GART of 512M enabled (table at 0x0000008000300000).
[39540.088426] amdgpu 0000:0a:00.0: amdgpu: PSP is resuming...
[39540.459472] amdgpu 0000:0a:00.0: amdgpu: PSP create ring failed!
[39540.459476] amdgpu 0000:0a:00.0: amdgpu: PSP resume failed
[39540.459479] [drm:amdgpu_device_fw_loading [amdgpu]] *ERROR* resume of IP block <psp> failed -62
[39540.459698] amdgpu 0000:0a:00.0: amdgpu: amdgpu_device_ip_resume failed (-62).
[51737.262727] evm: overlay not supported
[51737.333220] overlayfs: idmapped layers are currently not supported
```

This time error is not -110. It is -62. Unsure if this helps @sohaibnd 


---

### 评论 #11 — sohaibnd (2025-01-16T18:35:24Z)

@tuxology Thanks for the information, still looking into this. After putting the system to sleep, did you try waking it up normally first (by providing keyboard input for example) before rebooting? Just want to make sure it was actually frozen and not just asleep.

---

### 评论 #12 — tuxology (2025-01-18T12:33:00Z)

> [@tuxology](https://github.com/tuxology) Thanks for the information, still looking into this. After putting the system to sleep, did you try waking it up normally first (by providing keyboard input for example) before rebooting? Just want to make sure it was actually frozen and not just asleep.

Yes, I provided keyboard/mouse input but noting changed. One more point to note is that this machine is not connected to any display. I connected display as well and it was still frozen completely, nothing on display, with PSU fan running at max and GPU fan at max with max power draw and heat. No amount of keyboard input fixed this. Only reset fixed it. 

---

### 评论 #13 — pkautio (2025-01-19T13:21:39Z)

Couple of hours ago I tried to run mistral-small successfully. Just few hours later rcominfo gives the error again.

And yes, setup is a single GPU setup running on bare metal. Ollama is running on top of OS without docker.

This is a server setup, ASRock Rack ROMED8U-2T motherboard, no keyboard or display. Power mode is "balanced". I don't see how this could go to sleep mode.

Logs:
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: PSP is resuming...
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: reserve 0x1300000 from 0x877c000000 for PSP TMR
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: GECC is enabled
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: RAP: optional rap ta ucode is not available
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: SMU is resuming...
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e7f00 (78.127.0)
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: SMU driver if version not matched
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: SMU is resumed successfully!
[Sun Jan 19 14:09:00 2025] [drm] DMUB hardware initialized: version=0x07002A00
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[Sun Jan 19 14:09:00 2025] amdgpu 0000:83:00.0: [drm] Cannot find any crtc or sizes
[Sun Jan 19 14:09:00 2025] [drm] ring gfx_32775.1.1 was added
[Sun Jan 19 14:09:00 2025] [drm] ring compute_32775.2.2 was added
[Sun Jan 19 14:09:00 2025] [drm] ring sdma_32775.3.3 was added
[Sun Jan 19 14:09:00 2025] [drm] ring gfx_32775.1.1 ib test pass
[Sun Jan 19 14:09:00 2025] [drm] ring compute_32775.2.2 ib test pass
[Sun Jan 19 14:09:00 2025] [drm] ring sdma_32775.3.3 ib test pass
[Sun Jan 19 14:10:00 2025] [drm] PCIE GART of 512M enabled (table at 0x000000877EB00000).
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: PSP is resuming...
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: reserve 0x1300000 from 0x877c000000 for PSP TMR
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: GECC is enabled
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: RAP: optional rap ta ucode is not available
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: SMU is resuming...
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e7f00 (78.127.0)
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: SMU driver if version not matched
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: SMU is resumed successfully!
[Sun Jan 19 14:10:00 2025] [drm] DMUB hardware initialized: version=0x07002A00
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[Sun Jan 19 14:10:00 2025] amdgpu 0000:83:00.0: [drm] Cannot find any crtc or sizes
[Sun Jan 19 14:10:00 2025] [drm] ring gfx_32775.1.1 was added
[Sun Jan 19 14:10:00 2025] [drm] ring compute_32775.2.2 was added
[Sun Jan 19 14:10:00 2025] [drm] ring sdma_32775.3.3 was added
[Sun Jan 19 14:10:00 2025] [drm] ring gfx_32775.1.1 ib test pass
[Sun Jan 19 14:10:00 2025] [drm] ring compute_32775.2.2 ib test pass
[Sun Jan 19 14:10:00 2025] [drm] ring sdma_32775.3.3 ib test pass
[Sun Jan 19 14:11:07 2025] amdgpu 0000:83:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000017 SMN_C2PMSG_82:0x00000003
[Sun Jan 19 14:11:07 2025] amdgpu 0000:83:00.0: amdgpu: Failed to exit BACO state!
[Sun Jan 19 14:11:12 2025] amdgpu 0000:83:00.0: amdgpu: Timeout waiting for VM flush ACK!
[Sun Jan 19 14:11:12 2025] [drm] PCIE GART of 512M enabled (table at 0x000000877EB00000).
[Sun Jan 19 14:11:12 2025] amdgpu 0000:83:00.0: amdgpu: PSP is resuming...
[Sun Jan 19 14:11:16 2025] amdgpu 0000:83:00.0: amdgpu: PSP load kdb failed!
[Sun Jan 19 14:11:16 2025] amdgpu 0000:83:00.0: amdgpu: PSP resume failed
[Sun Jan 19 14:11:16 2025] [drm:amdgpu_device_fw_loading [amdgpu]] *ERROR* resume of IP block <psp> failed -62
[Sun Jan 19 14:11:16 2025] amdgpu 0000:83:00.0: amdgpu: amdgpu_device_ip_resume failed (-62).
[Sun Jan 19 14:11:16 2025] rfkill: input handler enabled
[Sun Jan 19 14:11:17 2025] rfkill: input handler disabled
[Sun Jan 19 15:00:06 2025] audit: type=1400 audit(1737291606.280:268): apparmor="DENIED" operation="capable" class="cap" profile="/snap/snapd/23545/usr/lib/snapd/snap-confine" pid=521634 comm="snap-confine" capability=12  capname="net_admin"
[Sun Jan 19 15:00:06 2025] audit: type=1400 audit(1737291606.280:269): apparmor="DENIED" operation="capable" class="cap" profile="/snap/snapd/23545/usr/lib/snapd/snap-confine" pid=521634 comm="snap-confine" capability=38  capname="perfmon"
[Sun Jan 19 15:00:06 2025] audit: type=1400 audit(1737291606.469:270): apparmor="DENIED" operation="capable" class="cap" profile="/snap/snapd/23545/usr/lib/snapd/snap-confine" pid=521676 comm="snap-confine" capability=12  capname="net_admin"
[Sun Jan 19 15:00:06 2025] audit: type=1400 audit(1737291606.469:271): apparmor="DENIED" operation="capable" class="cap" profile="/snap/snapd/23545/usr/lib/snapd/snap-confine" pid=521676 comm="snap-confine" capability=38  capname="perfmon"
[Sun Jan 19 15:00:06 2025] audit: type=1400 audit(1737291606.722:272): apparmor="DENIED" operation="capable" class="cap" profile="/snap/snapd/23545/usr/lib/snapd/snap-confine" pid=521714 comm="snap-confine" capability=12  capname="net_admin"
[Sun Jan 19 15:00:06 2025] audit: type=1400 audit(1737291606.722:273): apparmor="DENIED" operation="capable" class="cap" profile="/snap/snapd/23545/usr/lib/snapd/snap-confine" pid=521714 comm="snap-confine" capability=38  capname="perfmon"
[Sun Jan 19 15:00:06 2025] audit: type=1400 audit(1737291606.974:274): apparmor="DENIED" operation="capable" class="cap" profile="/snap/snapd/23545/usr/lib/snapd/snap-confine" pid=521757 comm="snap-confine" capability=12  capname="net_admin"
[Sun Jan 19 15:00:06 2025] audit: type=1400 audit(1737291606.974:275): apparmor="DENIED" operation="capable" class="cap" profile="/snap/snapd/23545/usr/lib/snapd/snap-confine" pid=521757 comm="snap-confine" capability=38  capname="perfmon"
[Sun Jan 19 15:05:18 2025] audit: type=1400 audit(1737291918.637:276): apparmor="DENIED" operation="capable" class="cap" profile="/snap/snapd/23545/usr/lib/snapd/snap-confine" pid=524010 comm="snap-confine" capability=12  capname="net_admin"
[Sun Jan 19 15:05:18 2025] audit: type=1400 audit(1737291918.637:277): apparmor="DENIED" operation="capable" class="cap" profile="/snap/snapd/23545/usr/lib/snapd/snap-confine" pid=524010 comm="snap-confine" capability=38  capname="perfmon"
[Sun Jan 19 15:05:24 2025] workqueue: kfd_process_wq_release [amdgpu] hogged CPU for >10000us 8 times, consider switching to WQ_UNBOUND
[Sun Jan 19 15:05:27 2025] amdgpu 0000:83:00.0: amdgpu: MES failed to respond to msg=MISC (SET_SHADER_DEBUGGER)
[Sun Jan 19 15:05:27 2025] [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
[Sun Jan 19 15:06:53 2025] amdgpu 0000:83:00.0: amdgpu: MES failed to respond to msg=MISC (SET_SHADER_DEBUGGER)
[Sun Jan 19 15:06:53 2025] [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger

rocm-smi

Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
========================================== ROCm System Management Interface ==========================================
==================================================== Concise Info ====================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK  MCLK  Fan  Perf     PwrCap       VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                      
======================================================================================================================
0       1     0x745e,   4147   N/A     N/A    N/A, N/A, 0         None  None  0%   unknown  Unsupported  0%     0%    
======================================================================================================================
================================================ End of ROCm SMI Log =================================================



---

### 评论 #14 — sohaibnd (2025-01-20T02:07:07Z)

@pkautio If you haven't rebooted your machine since the error can you confirm the system didn't enter any sleep mode with: 
`sudo dmesg | grep "PM: suspend"`

---

### 评论 #15 — pkautio (2025-01-20T18:45:29Z)

> @pkautio If you haven't rebooted your machine since the error can you confirm the system didn't enter any sleep mode with: 
> `sudo dmesg | grep "PM: suspend"`

No such events in the log.

From my previous log above you can clearly see the issue happening here:

[Sun Jan 19 14:11:07 2025] amdgpu 0000:83:00.0: amdgpu: Failed to exit BACO state!

When you are trying to replicate the issue, do you have either Radeon Pro W7800 or W7900 in your system?

---

### 评论 #16 — sohaibnd (2025-01-21T01:11:33Z)

> No such events in the log.
> 
> From my previous log above you can clearly see the issue happening here:
> 
> [Sun Jan 19 14:11:07 2025] amdgpu 0000:83:00.0: amdgpu: Failed to exit BACO state!

I see so your GPU is going into BACO without the system entering sleep.

> When you are trying to replicate the issue, do you have either Radeon Pro W7800 or W7900 in your system?

Yes, I am using a Radeon Pro W7800.

One workaround that you could try in the meantime is to disable runtime power management by setting the [runpm kernel parameter](https://docs.kernel.org/gpu/amdgpu/module-parameters.html#runpm-int): `amdgpu.runpm=0` (see [here](https://wiki.archlinux.org/title/Kernel_parameters) for a guide on how to set kernel parameters). 

---

### 评论 #17 — sohaibnd (2025-01-21T20:59:19Z)

@pkautio @tuxology Some additional questions:

- Does this issue with rocminfo occur if you don't run ollama at all? 
- Can you provide more information on how exactly you are using ollama through the API?

---

### 评论 #18 — tuxology (2025-01-22T01:12:16Z)

> [@pkautio](https://github.com/pkautio) [@tuxology](https://github.com/tuxology) Some additional questions:
> 
> * Does this issue with rocminfo occur if you don't run ollama at all?
*>

 - Yes, a new issue occurs now even after ollama disable. Let me share below 👇 

> * Can you provide more information on how exactly you are using ollama through the API?

 - Ollama service runs with https://ollama.com/library/qwen2.5-coder model on system start. I use OpenWebUI to make the requests (https://github.com/open-webui/open-webui) From the code it seems thse are standard Ollama API requests as seen in Ollama logs as well. I make 2-3 requests and leave the machine. Then after a few hours I recheck the machine and get the error in rocminfo and rocm-smi as well as `dmesg`. The error is very deterministic and same as what I shared here https://github.com/ROCm/ROCm/issues/4226#issuecomment-2580945633 and here. After changing the power state, I get this error consistently now: https://github.com/ROCm/ROCm/issues/4226#issuecomment-2593861613 

There is a new observation. After adding `amdgpu.runpm=0` I am getting this error consistently now after just 10-20 minutes of machine running:

```
[  580.400613] snd_hda_intel 0000:0a:00.1: Unable to change power state from D3hot to D0, device inaccessible
[  580.568166] snd_hda_intel 0000:0a:00.1: CORB reset timeout#2, CORBRP = 65535
[ 1393.559692] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 1393.559702] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.559794] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 1393.559799] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.559848] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 1393.559853] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.559909] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 1393.559915] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.559972] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 1393.559977] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.560027] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 1393.560032] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.560080] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 1393.560085] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.560183] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 1393.560189] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.560243] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 1393.560249] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.560319] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:18 param:0x00000005 message:TransferTableSmu2Dram?
[ 1393.560324] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.563932] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.563934] amdgpu 0000:0a:00.0: amdgpu: Failed to get current clock freq!
[ 1393.563980] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.563981] amdgpu 0000:0a:00.0: amdgpu: Failed to get current clock freq!
[ 1393.564023] amdgpu 0000:0a:00.0: amdgpu: Failed to export SMU metrics table!
[ 1393.564024] amdgpu 0000:0a:00.0: amdgpu: Failed to get fan speed(PWM)!
```

---

### 评论 #19 — pkautio (2025-01-22T06:03:10Z)

> @pkautio @tuxology Some additional questions:
> 
> - Does this issue with rocminfo occur if you don't run ollama at all? 
> - Can you provide more information on how exactly you are using ollama through the API?

I don't need to use API at all. Just run ollama with "ollama run llama3.3:70b", ask something and /bye.

Rocm crash will occur within one day.

Any other model will do the same.

---

### 评论 #20 — tuxology (2025-01-24T15:48:59Z)

@sohaibnd I've done almost everything possible except reinstalling the whole system (which I was postponing till now) without much success. Here is all that I tried:

1. Physically reinstall the card
2. Use default kernel cmdline params provided in RH 9.5 by removing all extra params I had. I was using `iommu=pt` very early on, which I removed
3. Add the `amdgpu.runpm=0` cmdline
4. Change powerstate using tuned-adm profiles to all possibel values in the list
5. Remove the kernel module immediately after boot, then re-add it
6. Uninstall module using amdgpu-install and then reinstall
7. Rebuild the amdgpu module from scratch and insmod it

I am now giving up on this and reinstalling complete system with RH 9.5 first. If that doesn't work, I will attempt installing latest Ubuntu LTS and get back to you. 

One thing to note is that I upgraded from an Nvidia card directly and this was NOT a fresh install on a new machine. @pkautio was this the case with you also?

---

### 评论 #21 — pkautio (2025-01-24T19:20:12Z)


> One thing to note is that I upgraded from an Nvidia card directly and this was NOT a fresh install on a new machine. @pkautio was this the case with you also?

No; this system is a fresh install with Radeon Pro W7800. I do not own any Nvidia card.

---

### 评论 #22 — sohaibnd (2025-01-24T23:10:08Z)

@tuxology @pkautio Thanks for the additional information and your effort in trying to fix this issue. I was able to put my W7800 in BACO state but was still not able to reproduce this issue. Some other questions/possibilities:

- Which vbios version (`sudo cat /sys/kernel/debug/dri/<gpu-index>/amdgpu_firmware_info` and `amd-smi static --vbios`) and linux kernel version (`uname -a`) are you on?
- When you reproduce the issue, can you try running rocminfo with these environment variables `AMD_LOG_LEVEL=5 HSAKMT_DEBUG_LEVEL=7 rocminfo` and include the output in a file. Also include the full output of `journalctl` after running rocminfo.
- Does your system support PCIe atomics?
- Just a sanity check, is the GPU properly seated in the PCIe slot and the power cables connected properly?
- Are you overclocking or undervolting your GPU or doing anything else?
- @tuxology which motherboard are you using?
- Are you able to reproduce this issue on the same system but with a different GPU (if you have any other AMD GPUs)?

---

### 评论 #23 — pkautio (2025-01-25T09:29:00Z)

I'm running this on ASRockRACK ROMED8U-2T motherboard with Epyc Milan processor, so yes it supports PCIe atomics.

All cables are well-connected and no overclocking nor undervolting.

I had quite old BIOS, since their support pages do not provide anything newer. Yesterday, however, I got newer version from their support and now BIOS supports Re-Size BAR functionality.

Since I ran Ollama yesterday, it has not crashed yet. Could Re-Size BAR support affect how BACO works with this card?

Can you preproduce this with Re-Size BAR support off?

---

### 评论 #24 — tuxology (2025-01-25T18:10:02Z)

Quick update: I did a clean install of the server, with RH 9.5 and have been serving models via ollama for 24hrs+ now without any crash. I did not install rocm via `amdgpu-install`. Just using the defaults for now - possibly the default driver via Redhat. I do not have `rocm-smi` and `amd-smi` commands and may separately build them sometime later if needed, but won't be installing rocm via amdgpu-install anymore.


> @tuxology which motherboard are you using?

I have ASUS Strix B550i motherboard with AMD Ryzen 9 5950X


---

### 评论 #25 — sohaibnd (2025-01-26T00:13:25Z)

> I had quite old BIOS, since their support pages do not provide anything newer. Yesterday, however, I got newer version from their support and now BIOS supports Re-Size BAR functionality.
> 
> Since I ran Ollama yesterday, it has not crashed yet. Could Re-Size BAR support affect how BACO works with this card?
> 
> Can you preproduce this with Re-Size BAR support off?

@pkautio That's great to hear! I don't think it's related to  Re-Size BAR but I'll give it a go anyways and let you know. If the issue does show up again, can you please provide the information from the first two points in my [comment](https://github.com/ROCm/ROCm/issues/4226#issuecomment-2613567927) too.

> Quick update: I did a clean install of the server, with RH 9.5 and have been serving models via ollama for 24hrs+ now without any crash. I did not install rocm via `amdgpu-install`. Just using the defaults for now - possibly the default driver via Redhat. I do not have `rocm-smi` and `amd-smi` commands and may separately build them sometime later if needed, but won't be installing rocm via amdgpu-install anymore.
> 
> > [@tuxology](https://github.com/tuxology) which motherboard are you using?
> 
> I have ASUS Strix B550i motherboard with AMD Ryzen 9 5950X

@tuxology That's great! Can you confirm that it is actually running on the GPU with `ollama ps`





---

### 评论 #26 — tuxology (2025-01-28T13:23:20Z)

@sohaibnd It took me a approx. 35hours to see the crash again. I can confirm ollama was using GPU. When GPU is used power draw increases to ~491W  for the total machine - I have a separate watt-meter. I have a 750W PSU, so this should be more than suffcient. Indication that GPU is about to crash is that GPU fan will work even with zero use. Total power draw increases from around 41W  idle to 49W idle (whole machine). When you give any load on it after that, it throws up this kernel log (different than old one). This is absolute fresh RHEL 9.5 install with no other amd installation. Kernel version is `5.14.0-503.22.1.el9_5.x86_64`

```
[74973.973226] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74973.973428] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74974.101649] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74974.101788] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74974.230027] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74974.230176] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74974.358374] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74974.358509] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74974.486593] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74974.486738] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74974.614923] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74974.615062] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74974.743185] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74974.743340] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74974.871464] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74974.871604] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74974.871863] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:41 param:0x00000000 message:DisallowGfxOff?
[74974.871884] amdgpu 0000:0a:00.0: amdgpu: Failed to disable gfxoff!
[74976.031475] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74976.031655] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74976.159801] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74976.159947] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74976.288024] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74976.288170] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74976.416257] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74976.417552] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74976.546714] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74976.547986] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74976.676979] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[74976.678026] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[74985.049825] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring sdma1 timeout, signaled seq=32838, emitted seq=32840
[74985.051475] amdgpu 0000:0a:00.0: amdgpu: GPU reset begin!
[74985.051523] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:41 param:0x00000000 message:DisallowGfxOff?
[74985.051528] amdgpu 0000:0a:00.0: amdgpu: Failed to disable gfxoff!
[74985.365495] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:59 param:0x00000000 message:DFCstateControl?
[74985.365502] amdgpu 0000:0a:00.0: amdgpu: [SetDfCstate] failed!
[74985.365506] amdgpu 0000:0a:00.0: amdgpu: Failed to disallow df cstate
[74985.549917] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[74985.550054] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[74985.677424] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[74985.677556] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[74985.804891] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[74985.805022] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[74985.932385] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[74985.932514] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[74986.059872] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[74986.059997] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[74986.187350] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[74986.187482] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[74986.314824] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[74986.314956] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[74986.442303] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[74986.442428] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[74986.569726] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[74986.569862] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[74987.163109] [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[74987.163331] amdgpu 0000:0a:00.0: amdgpu: ring_buffer_start = 0000000090c2164c; ring_buffer_end = 000000008e80e4ed; write_frame = 00000000f4794666
[74987.163337] amdgpu 0000:0a:00.0: amdgpu: write_frame is pointing to address out of bounds
[74987.163340] amdgpu 0000:0a:00.0: amdgpu: Failed to terminate ras ta
[74987.163343] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <psp> failed -22
[74987.164539] amdgpu 0000:0a:00.0: amdgpu: MODE1 reset
[74987.164543] amdgpu 0000:0a:00.0: amdgpu: GPU mode1 reset
[74987.167757] amdgpu 0000:0a:00.0: amdgpu: GPU smu mode1 reset
[74987.167760] amdgpu 0000:0a:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:47 param:0x00000000 message:Mode1Reset?
[74987.167765] amdgpu 0000:0a:00.0: amdgpu: GPU mode1 reset failed
[74987.167768] amdgpu 0000:0a:00.0: amdgpu: ASIC reset failed with error, -121 for drm dev, 0000:0a:00.0
[74987.167781] amdgpu 0000:0a:00.0: amdgpu: GPU reset(1) failed
[74987.167802] snd_hda_intel 0000:0a:00.1: Unable to change power state from D3hot to D0, device inaccessible
[74987.336963] snd_hda_intel 0000:0a:00.1: CORB reset timeout#2, CORBRP = 65535
[74987.336979] amdgpu 0000:0a:00.0: amdgpu: GPU reset end with ret = -121
[74987.336981] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* GPU Recovery Failed: -121
[74997.337885] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring sdma1 timeout, signaled seq=32840, emitted seq=32842
[74997.338120] amdgpu 0000:0a:00.0: amdgpu: GPU reset begin!
[74997.652224] amdgpu 0000:0a:00.0: amdgpu: Failed to disallow df cstate
```


---

### 评论 #27 — pkautio (2025-01-28T13:43:57Z)

> [@tuxology](https://github.com/tuxology) [@pkautio](https://github.com/pkautio) Thanks for the additional information and your effort in trying to fix this issue. I was able to put my W7800 in BACO state but was still not able to reproduce this issue. Some other questions/possibilities:
> 
>     * Which vbios version (`sudo cat /sys/kernel/debug/dri/<gpu-index>/amdgpu_firmware_info` and `amd-smi static --vbios`) and linux kernel version (`uname -a`) are you on?
> 
>     * When you reproduce the issue, can you try running rocminfo with these environment variables `AMD_LOG_LEVEL=5 HSAKMT_DEBUG_LEVEL=7 rocminfo` and include the output in a file. Also include the full output of `journalctl` after running rocminfo.
> 
>     * Does your system support PCIe atomics?
> 
>     * Just a sanity check, is the GPU properly seated in the PCIe slot and the power cables connected properly?
> 
>     * Are you overclocking or undervolting your GPU or doing anything else?
> 
>     * [@tuxology](https://github.com/tuxology) which motherboard are you using?
> 
>     * Are you able to reproduce this issue on the same system but with a different GPU (if you have any other AMD GPUs)?

Still crashing.

amd-smi static --vbios
GPU: 0
    VBIOS:
        NAME: N/A
        BUILD_DATE: N/A
        PART_NUMBER: N/A
        VERSION: 113-D7071100-101

uname -a
6.8.0-51-generic #52-Ubuntu SMP PREEMPT_DYNAMIC Thu Dec  5 13:09:44 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux

journalctl lines after running rocminfo:

Jan 28 15:35:10 XXXX kernel: amdgpu 0000:83:00.0: amdgpu: MES failed to respond to msg=MISC (SET_SHADER_DEBUGGER)
Jan 28 15:35:10 XXXX kernel: [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger

sudo cat /sys/kernel/debug/dri/1/amdgpu_firmware_info
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x000008e8
PFP feature version: 29, firmware version: 0x00000942
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x00000080
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x00000019
RLCV feature version: 1, firmware version: 0x00000022
MEC feature version: 29, firmware version: 0x0000099c
IMU feature version: 0, firmware version: 0x0b1f4b00
SOS feature version: 3211314, firmware version: 0x00310032
ASD feature version: 553648355, firmware version: 0x210000e3
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b000205
TA HDCP feature version: 0x00000000, firmware version: 0x17000041
TA DTM feature version: 0x00000000, firmware version: 0x12000017
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x004e7f00 (78.127.0)
SDMA0 feature version: 60, firmware version: 0x00000018
SDMA1 feature version: 60, firmware version: 0x00000018
VCN feature version: 0, firmware version: 0x09116006
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x07002a00
TOC feature version: 12, firmware version: 0x0000000c
MES_KIQ feature version: 6, firmware version: 0x00000100
MES feature version: 1, firmware version: 0x0000006a
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-D7071100-101



---

### 评论 #28 — tuxology (2025-01-28T17:28:42Z)

@sohaibnd After restarting, got a crash on the 2nd try when using ollama. This time there is also a stack trace:

```
[13908.084587] pcieport 0000:08:00.0: Unable to change power state from D3hot to D0, device inaccessible
[13908.085799] pcieport 0000:09:00.0: Unable to change power state from D3hot to D0, device inaccessible
[13908.086998] amdgpu 0000:0a:00.0: Unable to change power state from D3hot to D0, device inaccessible
[13912.492473] [drm:gmc_v11_0_flush_gpu_tlb [amdgpu]] *ERROR* Timeout waiting for sem acquire in VM flush!
[13912.648919] amdgpu 0000:0a:00.0: amdgpu: Timeout waiting for VM flush ACK!
[13912.805202] [drm:gmc_v11_0_flush_gpu_tlb [amdgpu]] *ERROR* Timeout waiting for sem acquire in VM flush!
[13912.961636] amdgpu 0000:0a:00.0: amdgpu: Timeout waiting for VM flush ACK!
[13912.961639] [drm] PCIE GART of 512M enabled (table at 0x0000008000300000).
[13912.961659] amdgpu 0000:0a:00.0: amdgpu: PSP is resuming...
[13913.002005] amdgpu 0000:0a:00.0: amdgpu: reserve 0x1300000 from 0x84fc000000 for PSP TMR
[13913.002210] amdgpu 0000:0a:00.0: amdgpu: RAS Init Status: 0xFFFFFFFF
[13913.002329] amdgpu 0000:0a:00.0: amdgpu: RAP: optional rap ta ucode is not available
[13913.002331] amdgpu 0000:0a:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[13913.002333] amdgpu 0000:0a:00.0: amdgpu: SMU is resuming...
[13913.002338] amdgpu 0000:0a:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e7e00 (78.126.0)
[13913.002341] amdgpu 0000:0a:00.0: amdgpu: SMU driver if version not matched
[13913.002348] amdgpu 0000:0a:00.0: amdgpu: SMU is resumed successfully!
[13913.002569] [drm] DMUB unsupported on ASIC
[13918.064628] ------------[ cut here ]------------
[13918.064630] WARNING: CPU: 28 PID: 5872 at drivers/gpu/drm/amd/amdgpu/../display/dc/dcn20/dcn20_hubbub.c:566 hubbub2_get_dchub_ref_freq+0x9c/0xc0 [amdgpu]
[13918.064803] Modules linked in: tls xt_mark vhost_net vhost vhost_iotlb tap xt_CHECKSUM xt_MASQUERADE xt_conntrack ipt_REJECT nft_compat nf_nat_tftp nft_objref nf_conntrack_tftp nft_counter bridge stp llc binfmt_misc tun nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink bnep sunrpc vfat fat iwlmvm mac80211 snd_hda_codec_realtek libarc4 snd_hda_codec_generic snd_hda_scodec_component snd_hda_codec_hdmi amd_atl intel_rapl_msr intel_rapl_common snd_hda_intel snd_intel_dspcfg edac_mce_amd snd_intel_sdw_acpi snd_hda_codec iwlwifi btusb btrtl kvm_amd btintel snd_hda_core btbcm btmtk snd_hwdep kvm snd_pcm cfg80211 bluetooth snd_timer eeepc_wmi asus_wmi snd rapl sparse_keymap wmi_bmof acpi_cpufreq pcspkr k10temp soundcore i2c_piix4 rfkill i2c_designware_platform gpio_amdpt i2c_designware_core gpio_generic xfs libcrc32c ahci libahci libata igc amdgpu video amdxcp i2c_algo_bit
[13918.064842]  drm_ttm_helper ttm drm_exec gpu_sched drm_suballoc_helper drm_buddy drm_display_helper drm_kms_helper nvme crct10dif_pclmul crc32_pclmul crc32c_intel drm nvme_core ghash_clmulni_intel ccp cec sp5100_tco nvme_auth t10_pi wmi dm_mirror dm_region_hash dm_log dm_mod fuse
[13918.064856] CPU: 28 PID: 5872 Comm: ollama_llama_se Kdump: loaded Not tainted 5.14.0-503.22.1.el9_5.x86_64 #1
[13918.064858] Hardware name: ASUS System Product Name/ROG STRIX B550-I GAMING, BIOS 2603 02/09/2022
[13918.064859] RIP: 0010:hubbub2_get_dchub_ref_freq+0x9c/0xc0 [amdgpu]
[13918.065026] Code: 83 c0 63 ff ff 3d 20 4e 00 00 77 22 89 5d 00 48 8b 44 24 08 65 48 2b 04 25 28 00 00 00 75 24 48 83 c4 10 5b 5d e9 2f 3d e0 c1 <0f> 0b eb de 0f 0b eb da d1 eb 8d 83 c0 63 ff ff 3d 20 4e 00 00 76
[13918.065027] RSP: 0018:ffffaa1603f9b6b8 EFLAGS: 00010246
[13918.065028] RAX: 0000000000001000 RBX: 00000000000186a0 RCX: 0000000000000000
[13918.065029] RDX: ffffaa1603f9b6bc RSI: 00000000000039e5 RDI: ffff9932daf80000
[13918.065030] RBP: ffff9932da91b3a0 R08: ffffaa1603f9b6b8 R09: 000000000000000c
[13918.065031] R10: ffffaa16206f3500 R11: ffffffff83de93e8 R12: ffff9932da91b000
[13918.065032] R13: ffff9932c225ca00 R14: ffff9932daf80010 R15: ffff9932c225d000
[13918.065033] FS:  00007f0dab0f3340(0000) GS:ffff9941af100000(0000) knlGS:0000000000000000
[13918.065034] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[13918.065035] CR2: 00007ff55b7fdf17 CR3: 000000013071c000 CR4: 0000000000750ef0
[13918.065036] PKRU: 55555554
[13918.065036] Call Trace:
[13918.065038]  <TASK>
[13918.065039]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.065043]  ? show_trace_log_lvl+0x26e/0x2df
[13918.065047]  ? show_trace_log_lvl+0x26e/0x2df
[13918.065050]  ? dcn32_init_hw+0x158/0x8c0 [amdgpu]
[13918.065225]  ? hubbub2_get_dchub_ref_freq+0x9c/0xc0 [amdgpu]
[13918.065388]  ? __warn+0x7e/0xd0
[13918.065391]  ? hubbub2_get_dchub_ref_freq+0x9c/0xc0 [amdgpu]
[13918.065559]  ? report_bug+0x100/0x140
[13918.065563]  ? handle_bug+0x3c/0x70
[13918.065565]  ? exc_invalid_op+0x14/0x70
[13918.065566]  ? asm_exc_invalid_op+0x16/0x20
[13918.065570]  ? hubbub2_get_dchub_ref_freq+0x9c/0xc0 [amdgpu]
[13918.065731]  dcn32_init_hw+0x158/0x8c0 [amdgpu]
[13918.065908]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.065910]  ? dmub_reg_get+0x21/0x40 [amdgpu]
[13918.066059]  dc_set_power_state+0x66/0xb0 [amdgpu]
[13918.066214]  dm_resume+0xf9/0x660 [amdgpu]
[13918.066385]  amdgpu_device_ip_resume_phase2+0x52/0xc0 [amdgpu]
[13918.066493]  amdgpu_device_resume+0x7b/0x2a0 [amdgpu]
[13918.066607]  amdgpu_pmops_runtime_resume+0x54/0x110 [amdgpu]
[13918.066714]  ? __pfx_pci_pm_runtime_resume+0x10/0x10
[13918.066716]  __rpm_callback+0x44/0x120
[13918.066719]  ? __pfx_pci_pm_runtime_resume+0x10/0x10
[13918.066721]  rpm_callback+0x5d/0x70
[13918.066722]  rpm_resume+0x4dc/0x770
[13918.066724]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066726]  ? __flush_work.isra.0+0x195/0x230
[13918.066728]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066731]  __pm_runtime_resume+0x4a/0x80
[13918.066733]  amdgpu_driver_open_kms+0x4c/0x250 [amdgpu]
[13918.066841]  drm_file_alloc+0x1b7/0x280 [drm]
[13918.066862]  drm_open_helper+0x7b/0x140 [drm]
[13918.066877]  drm_open+0x6b/0x110 [drm]
[13918.066891]  drm_stub_open+0xae/0x150 [drm]
[13918.066907]  chrdev_open+0xc3/0x250
[13918.066911]  ? __pfx_chrdev_open+0x10/0x10
[13918.066913]  do_dentry_open+0x14f/0x440
[13918.066916]  do_open+0x21a/0x450
[13918.066919]  path_openat+0x111/0x280
[13918.066922]  do_filp_open+0xb2/0x160
[13918.066925]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066927]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066929]  ? __check_object_size.part.0+0x47/0xd0
[13918.066932]  do_sys_openat2+0x96/0xd0
[13918.066934]  __x64_sys_openat+0x53/0xa0
[13918.066936]  do_syscall_64+0x5f/0xf0
[13918.066938]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066940]  ? vfs_read+0x1e9/0x330
[13918.066943]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066945]  ? mutex_lock+0xe/0x30
[13918.066947]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066949]  ? kernfs_seq_start+0x28/0xd0
[13918.066951]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066953]  ? kernfs_seq_stop+0x30/0x40
[13918.066954]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066955]  ? seq_read_iter+0x209/0x4b0
[13918.066958]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066960]  ? vfs_read+0x1e9/0x330
[13918.066963]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066965]  ? syscall_exit_work+0x103/0x130
[13918.066967]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066969]  ? syscall_exit_to_user_mode+0x19/0x40
[13918.066971]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066972]  ? do_syscall_64+0x6b/0xf0
[13918.066974]  ? srso_alias_return_thunk+0x5/0xfbef5
[13918.066975]  ? exc_page_fault+0x62/0x150
[13918.066978]  entry_SYSCALL_64_after_hwframe+0x78/0x80
[13918.066979] RIP: 0033:0x7f0d74afd884
[13918.067001] Code: 24 20 eb 8f 66 90 44 89 54 24 0c e8 f6 88 f8 ff 44 8b 54 24 0c 44 89 e2 48 89 ee 41 89 c0 bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 77 34 44 89 c7 89 44 24 0c e8 48 89 f8 ff 8b 44
[13918.067002] RSP: 002b:00007ffc4a7df3a0 EFLAGS: 00000293 ORIG_RAX: 0000000000000101
[13918.067003] RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007f0d74afd884
[13918.067004] RDX: 0000000000080002 RSI: 00007ffc4a7df430 RDI: 00000000ffffff9c
[13918.067005] RBP: 00007ffc4a7df430 R08: 0000000000000000 R09: 00007ffc4a7df1b5
[13918.067006] R10: 0000000000000000 R11: 0000000000000293 R12: 0000000000080002
[13918.067006] R13: 00007ffc4a7df430 R14: 646e65725f6d7264 R15: 00007ffc4a7df500
[13918.067009]  </TASK>
[13918.067010] ---[ end trace 0000000000000000 ]---
[13918.068618] amdgpu 0000:0a:00.0: [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_hubp_pg_control line:176
[13918.070206] amdgpu 0000:0a:00.0: [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_hubp_pg_control line:180
[13918.071798] amdgpu 0000:0a:00.0: [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_hubp_pg_control line:184
[13918.073385] amdgpu 0000:0a:00.0: [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_hubp_pg_control line:188
[13918.074973] amdgpu 0000:0a:00.0: [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:94
[13918.076561] amdgpu 0000:0a:00.0: [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:102
[13918.078146] amdgpu 0000:0a:00.0: [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:110
[13918.079732] amdgpu 0000:0a:00.0: [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:118
[13927.571165] amdgpu 0000:0a:00.0: amdgpu: rlc autoload: gc ucode autoload timeout
[13927.571174] amdgpu 0000:0a:00.0: amdgpu: (-110) failed to wait rlc autoload complete
[13927.571178] [drm:amdgpu_device_ip_resume_phase2 [amdgpu]] *ERROR* resume of IP block <gfx_v11_0> failed -110
[13927.571336] amdgpu 0000:0a:00.0: amdgpu: amdgpu_device_ip_resume failed (-110).
[13928.063398] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[13928.063585] [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
[13928.225133] [drm:gmc_v11_0_flush_gpu_tlb [amdgpu]] *ERROR* Timeout waiting for sem acquire in VM flush!
[13928.380808] amdgpu 0000:0a:00.0: amdgpu: Timeout waiting for VM flush ACK!
```

I see my B550-I motherboard bios is from 2022. The manufacturer has also released an update which updates "AGESA to ComboV2PI 1.2.0.Cc" which is AMD related? I will update my bios and then restart and observe again. 

---

### 评论 #29 — sohaibnd (2025-01-28T18:53:56Z)

> amd-smi static --vbios GPU: 0 VBIOS: NAME: N/A BUILD_DATE: N/A PART_NUMBER: N/A VERSION: 113-D7071100-101

Interesting, it seems like vbios version can't be read properly which could point to a hardware/firmware issue. How did you obtain this graphics card?

> journalctl lines after running rocminfo:
>
> Jan 28 15:35:10 XXXX kernel: amdgpu 0000:83:00.0: amdgpu: MES failed to respond to msg=MISC (SET_SHADER_DEBUGGER) Jan 28 15:35:10 XXXX kernel: [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] _ERROR_ failed to set_shader_debugger

Can you please include the entire dmesg or jornalctl log so I can see what's happening before, the last few lines on their own are not enough. Also try running `AMD_LOG_LEVEL=5 HSAKMT_DEBUG_LEVEL=7 rocminfo` when you reproduce the issue.



---

### 评论 #30 — pkautio (2025-01-31T19:07:28Z)

> > amd-smi static --vbios GPU: 0 VBIOS: NAME: N/A BUILD_DATE: N/A PART_NUMBER: N/A VERSION: 113-D7071100-101
> 
> Interesting, it seems like vbios version can't be read properly which could point to a hardware/firmware issue. How did you obtain this graphics card?
> 
> > journalctl lines after running rocminfo:
> > Jan 28 15:35:10 XXXX kernel: amdgpu 0000:83:00.0: amdgpu: MES failed to respond to msg=MISC (SET_SHADER_DEBUGGER) Jan 28 15:35:10 XXXX kernel: [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] _ERROR_ failed to set_shader_debugger
> 
> Can you please include the entire dmesg or jornalctl log so I can see what's happening before, the last few lines on their own are not enough. Also try running `AMD_LOG_LEVEL=5 HSAKMT_DEBUG_LEVEL=7 rocminfo` when you reproduce the issue.

Now amd-smi static --vbios reports it correctly. I don't know what was the issue earlier:

amd-smi static --vbios
GPU: 0
    VBIOS:
        NAME: AMD D70711_XLW_A0_32GB_MBA_Working
        BUILD_DATE: 2023/04/27 12:27
        PART_NUMBER: 113-D7071100-101
        VERSION: 022.001.002.030.000001

Updated Rocm package (including amdgpu driver) to 6.3.2 and the issue persists. I will report more detailed data after next crash.

Reloading driver fixes the issue:
sudo modprobe -r amdgpu
sudo modprobe amdgpu
... and card works again.


---

### 评论 #31 — tuxology (2025-02-06T16:26:08Z)

@sohaibnd @pkautio Quick update. I think I fixed the issue - uptime has been 2+ days now. 

## TL;DR 
Issue was power/cables related.

## The Fix
So even after my bios update here https://github.com/ROCm/ROCm/issues/4226#issuecomment-2619638508 I was still getting exactly the same errors as before. The total power draw from whole machine was ~418W and without GPU it was around 48W Idle. After all options were exhausted, I started diagnosing hardware. When inference began, the GPU was giving a high pitch sound. I think the internal voltage regulation could be an issue.  It would work for 2-4 inference queries at max power and then would throw same error. I started measuring the current draw going in the GPU for individual cables - there are 3 inputs to the GPU all provided via a 12v-2x6 connector with 2 connected to the power supply. I realized one PCIe cable was getting lower current draw than other. I replaced it and I hope the issue is now gone given the different load conditions I've tested the GPU on. 

---

### 评论 #32 — sohaibnd (2025-02-10T21:17:47Z)

@tuxology any issue yet?

---

### 评论 #33 — tuxology (2025-02-21T02:48:44Z)

> [@tuxology](https://github.com/tuxology) any issue yet?

No issue yet. Had uptime of 10+ days without any issue

---

### 评论 #34 — sohaibnd (2025-02-21T15:07:09Z)

That's great!

@pkautio Can you recheck you HW as well for issues (with the cables, PCIe slot on motherboard, power supply, etc.)?

---

### 评论 #35 — sohaibnd (2025-05-01T14:34:26Z)

Closing this issue since I am unable to reproduce it (@tuxology's was an issue with the gpu power cables and I suspect @pkautio's is a HW issue as well).

---

### 评论 #36 — hawkli-1994 (2025-06-04T07:11:20Z)

This issue still persists, and the version is 6.4.1. I will provide detailed system information.
GPU w7900
```
root@node2:~# rocm-smi


Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
======================================== ROCm System Management Interface ========================================
================================================== Concise Info ==================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK  MCLK  Fan  Perf     PwrCap  VRAM%  GPU%
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)
==================================================================================================================
0       1     0x744a,   5599   N/A     N/A    N/A, N/A, 0         N/A   N/A   0%   unknown  N/A     0%     0%
1       2     0x744a,   61077  N/A     N/A    N/A, N/A, 0         N/A   N/A   0%   unknown  N/A     0%     0%
==================================================================================================================
============================================== End of ROCm SMI Log ===============================================

<br>
root@node2:~# cat /etc/os-release
PRETTY_NAME="Ubuntu 22.04.5 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.5 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
<br>
root@node2:~# uname -r
5.15.0-138-generic

<br>
root@node2:~# uname -a
Linux node2 5.15.0-138-generic #148-Ubuntu SMP Fri Mar 14 19:05:48 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux

<br>
root@node2:~# ls /opt/
amdgpu  amdgpu-pro  cni  containerd  harbor  harbor-offline-installer-v2.13.0.tgz  rocm  rocm-6.4.1
```


---
