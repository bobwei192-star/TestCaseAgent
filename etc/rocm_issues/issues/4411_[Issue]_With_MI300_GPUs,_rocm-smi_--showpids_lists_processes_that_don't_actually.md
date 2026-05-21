# [Issue]: With MI300 GPUs, rocm-smi --showpids lists processes that don't actually use the GPU(s)

> **Issue #4411**
> **状态**: open
> **创建时间**: 2025-02-24T09:21:20Z
> **更新时间**: 2025-04-25T06:45:37Z
> **作者**: maxweiss
> **标签**: Under Investigation, AMD Instinct MI300A, ROCm 6.3.3
> **URL**: https://github.com/ROCm/ROCm/issues/4411

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300A** (颜色: #ededed)
- **ROCm 6.3.3** (颜色: #aaaaaa)

## 描述

### Problem Description

We have a daemon that uses the amd-smi/rocm-smi API to update the GPU information every couple of seconds. The daemon itself doesn't have any OpenCL/HIP/... code, so it doesn't actually "use" the GPU(s). On our machine with MI300 GPUs, rocm --showpids lists the daemon as KFD process:

```
$ rocm-smi --showpids


============================ ROCm System Management Interface ============================
===================================== KFD Processes ======================================
KFD process information:
PID    	PROCESS NAME	GPU(s)	VRAM USED	SDMA USED	CU OCCUPANCY	
1058463	<daemon>     	0     	0        	0        	0           	
==========================================================================================
================================== End of ROCm SMI Log ===================================
```
```
$ rocm-smi --showpidgpus


============================ ROCm System Management Interface ============================
================================== GPUs Indexed by PID ===================================
PID 1058463 is using 0 DRM device(s)
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

And more importantly, we cannot change the compute/memory mode, unless we shut down the daemon:

```
# rocm-smi --setcomputepartition TPX


============================ ROCm System Management Interface ============================
============================== Set compute partition to TPX ==============================
GPU[0]		: Device is currently busy, try again later
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

* It also happens with older ROCm versions
* It happens with all MI300 compute modes (SPX, TPX, CPX).
* It doesn't happen on machines with Radeon or MI210 GPUs.
* Using `rsmi_shut_down()` to shut down ROCm doesn't help. The process has to exit to make sure that rocm-smi --showpids doesn't list it anymore.
* The same happens with amd-smi and its API.


### Operating System

22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD Proto Sample : SH5-MI300A-A0

### GPU

AMD Instinct MI300A

### ROCm Version

6.3.3

### ROCm Component

_No response_

### Steps to Reproduce

It can be reproduced with this example:

```
#include <iostream>
#include <unistd.h>

#include <rocm_smi/rocm_smi.h>

int main() {
   // Initialize the ROCm SMI library
   rsmi_status_t status = rsmi_init(0);
   if (status != RSMI_STATUS_SUCCESS) {
      std::cerr << "Failed to initialize ROCm SMI library" << std::endl;
      return -1;
   }

   // Get the number of GPU devices
   uint32_t device_count = 0;
   status = rsmi_num_monitor_devices(&device_count);
   if (status != RSMI_STATUS_SUCCESS) {
      std::cerr << "Failed to get GPU device count" << std::endl;
      rsmi_shut_down();
      return -1;
   }

   std::cout << "Number of GPUs detected: " << device_count << std::endl;

   // Iterate over each GPU and get memory usage
   for (uint32_t i = 0; i < device_count; i++) {
      uint64_t used_memory = 0;
      status = rsmi_dev_memory_usage_get(i, RSMI_MEM_TYPE_VRAM, &used_memory);
      if (status == RSMI_STATUS_SUCCESS) {
         std::cout << "GPU " << i << " VRAM Used: " << used_memory / (1024 * 1024) << " MB" << std::endl;
      } else {
         std::cerr << "Failed to get memory usage for GPU " << i << std::endl;
      }
   }

   std::cout << "Shutting down ROCm" << std::endl;
   // Shutdown the ROCm SMI library
   rsmi_shut_down();

   // Sleep for 100 seconds to simulate the daemon behaviour
   std::cout << "Sleeping for 100 seconds" << std::endl;
   sleep(100);

   return 0;
}
```

While the process is sleeping, rocm-smi lists the process as KFD process.

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
  Name:                    AMD Proto Sample : SH5-MI300A-A0   
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Proto Sample : SH5-MI300A-A0   
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
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131174896(0x7d191f0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131174896(0x7d191f0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131174896(0x7d191f0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131174896(0x7d191f0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx940                             
  Uuid:                    GPU-8a034d0fdebb161c               
  Marketing Name:          AMD Instinct MI300A                
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
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   256                                
  Internal Node ID:        1                                  
  Compute Unit:            228                                
  SIMDs per CU:            4                                  
  Shader Engines:          24                                 
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       APU
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
      Size:                    98381172(0x5dd2d74) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98381172(0x5dd2d74) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98381172(0x5dd2d74) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx940:sramecc+:xnack-
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

## 评论 (9 条)

### 评论 #1 — maxweiss (2025-02-24T09:27:29Z)

I did some debugging and it looks like `rsmi_dev_memory_usage_get()` is the culprit. If we remove the call to `rsmi_dev_memory_usage_get()`, everything works fine (even if we use other rsmi_* functions to get the UUID, total memory, etc.).

With MI300 GPUs, the function `rsmi_dev_memory_usage_get()` goes into the fallback code and calls `kfd_node->get_used_memory(used)`. `open("/dev/kfd")` seems to cause this issue, and not even the `close()` call helps.

I used an example that does nothing but open/close `/dev/kfd`, and rocm-smi --showpids lists the process as KFD process:

```
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

int main() {
    int fd = open("/dev/kfd", O_RDWR);
    if (fd < 0) {
        perror("Failed to open /dev/kfd");
        return 1;
    }

    close(fd);
    sleep(100);

    return 0;
}
```

```
$ rocm-smi --showpids


============================ ROCm System Management Interface ============================
===================================== KFD Processes ======================================
KFD process information:
PID    	PROCESS NAME	GPU(s)	VRAM USED	SDMA USED	CU OCCUPANCY	
1075718	kfd_open    	0     	0        	0        	0           	
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

With other AMD GPUs, the kfd fallback in `rsmi_dev_memory_usage_get()` is not needed as rocm-smi successfully reads the memory from /sys/class/drm/card*/device/mem_info_vram_used.

For MI300's the file exists, but the content is always 0. Is this expected/known?

---

### 评论 #2 — ppanchad-amd (2025-02-24T15:21:21Z)

Hi @maxweiss. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #3 — darren-amd (2025-03-03T20:50:43Z)

Hi @maxweiss,

I don't currently have an MI300A machine and have been unable to reproduce this on an MI300X machine. Could you please share the log from `/var/log/rocm_smi_lib` after running the program with `export RSMI_LOGGING=1`. Also, could you see if you are able to reproduce the issue with `amd-smi`? (`amd-smi process` and `amd-smi set --compute-partition TPX`). That should help me further investigate, thanks!

---

### 评论 #4 — fluidnumericsJoe (2025-03-07T15:45:13Z)

Hey @darren-amd, Fluid Numerics has an MI300A system and has a contract with AMD where we can provide you access. Please reach out to support@fluidnumerics.com and I will route you to the internal folks at AMD we are working with to get this squared away.

---

### 评论 #5 — phani544 (2025-03-07T16:43:45Z)

can confirm the process is seen with rocm-smi and not with amd-smi on MI300X. Logging an internal defect to dev team


![Image](https://github.com/user-attachments/assets/dd2ef1ab-1043-4391-9772-523d121c6958)







---

### 评论 #6 — garrettbyrd (2025-03-07T19:46:11Z)

Testing on MI300A, I have walked through the steps suggested by @darren-amd.

I can confirm I get the following output when running `rocm-smi --showpids` while the minimal reproducer @maxweiss provided is running:

```
============================ ROCm System Management Interface ============================
===================================== KFD Processes ======================================
KFD process information:
PID    	PROCESS NAME	GPU(s)	VRAM USED	SDMA USED	CU OCCUPANCY	
1684258	kfd_open    	0     	0        	0        	0           	
==========================================================================================
================================== End of ROCm SMI Log ===================================

```

With `RSMI_LOGGING=1`, here is the output from `/var/log/rocm_smi_lib`:

```
2025-03-07 13:44:52.335839  [ALWAYS]: =============== ROCM SMI initialize ================
2025-03-07 13:44:52.339157  [INFO]: ====== Gathered system details ============
SYSTEM NAME: Linux
OS DISTRIBUTION: Rocky Linux 9.5 (Blue Onyx)
NODE NAME: nicholson
RELEASE: 5.14.0-503.19.1.el9_5.x86_64
VERSION: #1 SMP PREEMPT_DYNAMIC Thu Dec 19 12:55:03 UTC 2024
MACHINE TYPE: x86_64
DOMAIN: (none)
ENDIANNESS: Little Endian, multi-bit symbols encoded as little endian (LSB first)
ROCM BUILD TYPE: debug
ROCM-SMI-LIB PATH: /opt/rocm-6.3.1/libexec/rocm_smi/../../lib/librocm_smi64.so.7
ROCM-SMI-LIB BUILD DATE: Sat Jan 11 11:15:45 2025
ROCM ENV VARIABLES: 
	RSMI_DEBUG_BITFIELD = <undefined>
	RSMI_DEBUG_DRM_ROOT_OVERRIDE = <undefined>
	RSMI_DEBUG_HWMON_ROOT_OVERRIDE = <undefined>
	RSMI_DEBUG_PP_ROOT_OVERRIDE = <undefined>
	RSMI_DEBUG_INFINITE_LOOP = <undefined>
	RSMI_LOGGING = 1
	RSMI_LOGGING (are logs on) = TRUE
	RSMI_DEBUG_ENUM_OVERRIDE = {}
AMD GFX VERSIONS: 
	N/A - No AMD devices detected

2025-03-07 13:44:52.339276  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | Discovered a potential of 35 cards | 
2025-03-07 13:44:52.339441  [DEBUG]: int amd::smi::get_gpu_id(uint32_t, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/0/gpu_id | Successfully read node #0 for gpu_id | Data (gpu_id) *gpu_id = 0 | return = 0 | 
2025-03-07 13:44:52.339516  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/0/properties | Successfully read node #0 for property_name = unique_id | Data (unique_id) * val = 0 | return = 22 | 
2025-03-07 13:44:52.339587  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/0/properties | Successfully read node #0 for property_name = location_id | Data (location_id) * val = 0 | return = 0 | 
2025-03-07 13:44:52.339658  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/0/properties | Successfully read node #0 for property_name = domain | Data (domain) * val = 0 | return = 0 | 
2025-03-07 13:44:52.339752  [DEBUG]: int amd::smi::get_gpu_id(uint32_t, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/1/gpu_id | Successfully read node #1 for gpu_id | Data (gpu_id) *gpu_id = 0 | return = 0 | 
2025-03-07 13:44:52.339821  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/1/properties | Successfully read node #1 for property_name = unique_id | Data (unique_id) * val = 0 | return = 22 | 
2025-03-07 13:44:52.339902  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/1/properties | Successfully read node #1 for property_name = location_id | Data (location_id) * val = 0 | return = 0 | 
2025-03-07 13:44:52.339972  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/1/properties | Successfully read node #1 for property_name = domain | Data (domain) * val = 0 | return = 0 | 
2025-03-07 13:44:52.340065  [DEBUG]: int amd::smi::get_gpu_id(uint32_t, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/2/gpu_id | Successfully read node #2 for gpu_id | Data (gpu_id) *gpu_id = 0 | return = 0 | 
2025-03-07 13:44:52.340133  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/2/properties | Successfully read node #2 for property_name = unique_id | Data (unique_id) * val = 0 | return = 22 | 
2025-03-07 13:44:52.340202  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/2/properties | Successfully read node #2 for property_name = location_id | Data (location_id) * val = 0 | return = 0 | 
2025-03-07 13:44:52.340272  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/2/properties | Successfully read node #2 for property_name = domain | Data (domain) * val = 0 | return = 0 | 
2025-03-07 13:44:52.340366  [DEBUG]: int amd::smi::get_gpu_id(uint32_t, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/3/gpu_id | Successfully read node #3 for gpu_id | Data (gpu_id) *gpu_id = 0 | return = 0 | 
2025-03-07 13:44:52.340434  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/3/properties | Successfully read node #3 for property_name = unique_id | Data (unique_id) * val = 0 | return = 22 | 
2025-03-07 13:44:52.340503  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/3/properties | Successfully read node #3 for property_name = location_id | Data (location_id) * val = 0 | return = 0 | 
2025-03-07 13:44:52.340575  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/3/properties | Successfully read node #3 for property_name = domain | Data (domain) * val = 0 | return = 0 | 
2025-03-07 13:44:52.340930  [DEBUG]: int amd::smi::get_gpu_id(uint32_t, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/4/gpu_id | Successfully read node #4 for gpu_id | Data (gpu_id) *gpu_id = 19794 | return = 0 | 
2025-03-07 13:44:52.341192  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/4/properties | Successfully read node #4 for property_name = unique_id | Data (unique_id) * val = 13321655985203289421 | return = 0 | 
2025-03-07 13:44:52.341449  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/4/properties | Successfully read node #4 for property_name = location_id | Data (location_id) * val = 256 | return = 0 | 
2025-03-07 13:44:52.341705  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/4/properties | Successfully read node #4 for property_name = domain | Data (domain) * val = 0 | return = 0 | 
2025-03-07 13:44:52.342016  [DEBUG]: int amd::smi::get_gpu_id(uint32_t, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/5/gpu_id | Successfully read node #5 for gpu_id | Data (gpu_id) *gpu_id = 48483 | return = 0 | 
2025-03-07 13:44:52.342272  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/5/properties | Successfully read node #5 for property_name = unique_id | Data (unique_id) * val = 16908369143281941404 | return = 0 | 
2025-03-07 13:44:52.342529  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/5/properties | Successfully read node #5 for property_name = location_id | Data (location_id) * val = 16640 | return = 0 | 
2025-03-07 13:44:52.342778  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/5/properties | Successfully read node #5 for property_name = domain | Data (domain) * val = 0 | return = 0 | 
2025-03-07 13:44:52.343093  [DEBUG]: int amd::smi::get_gpu_id(uint32_t, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/6/gpu_id | Successfully read node #6 for gpu_id | Data (gpu_id) *gpu_id = 60723 | return = 0 | 
2025-03-07 13:44:52.343356  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/6/properties | Successfully read node #6 for property_name = unique_id | Data (unique_id) * val = 13297715105545626452 | return = 0 | 
2025-03-07 13:44:52.343612  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/6/properties | Successfully read node #6 for property_name = location_id | Data (location_id) * val = 33024 | return = 0 | 
2025-03-07 13:44:52.343868  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/6/properties | Successfully read node #6 for property_name = domain | Data (domain) * val = 0 | return = 0 | 
2025-03-07 13:44:52.344177  [DEBUG]: int amd::smi::get_gpu_id(uint32_t, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/7/gpu_id | Successfully read node #7 for gpu_id | Data (gpu_id) *gpu_id = 7426 | return = 0 | 
2025-03-07 13:44:52.344437  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/7/properties | Successfully read node #7 for property_name = unique_id | Data (unique_id) * val = 1919957156416991372 | return = 0 | 
2025-03-07 13:44:52.344697  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/7/properties | Successfully read node #7 for property_name = location_id | Data (location_id) * val = 49408 | return = 0 | 
2025-03-07 13:44:52.344979  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/7/properties | Successfully read node #7 for property_name = domain | Data (domain) * val = 0 | return = 0 | 
2025-03-07 13:44:52.345002  [ERROR]: int amd::smi::get_gpu_id(uint32_t, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/8/gpu_id | Issue: Could not read node #8, KFD node was an unsupported node. | return = 1 | 
2025-03-07 13:44:52.345020  [ERROR]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/8/properties | Issue: Could not read node #8, KFD node was an unsupported node. | return = 1 | 
2025-03-07 13:44:52.345038  [ERROR]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/8/properties | Issue: Could not read node #8, KFD node was an unsupported node. | return = 1 | 
2025-03-07 13:44:52.345055  [ERROR]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/8/properties | Issue: Could not read node #8, KFD node was an unsupported node. | return = 1 | 
2025-03-07 13:44:52.345072  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | Ordered system nodes found = {
[node_id = 7; gpu_id = 7426; unique_id = 1919957156416991372; location_id = 49408; bdf = 0x000000000000c100; domain = 0x0000; bus = 0xc1; device = 0x00; function = 0; partition_id = 0], 
[node_id = 6; gpu_id = 60723; unique_id = 13297715105545626452; location_id = 33024; bdf = 0x0000000000008100; domain = 0x0000; bus = 0x81; device = 0x00; function = 0; partition_id = 0], 
[node_id = 4; gpu_id = 19794; unique_id = 13321655985203289421; location_id = 256; bdf = 0x0000000000000100; domain = 0x0000; bus = 0x01; device = 0x00; function = 0; partition_id = 0], 
[node_id = 5; gpu_id = 48483; unique_id = 16908369143281941404; location_id = 16640; bdf = 0x0000000000004100; domain = 0x0000; bus = 0x41; device = 0x00; function = 0; partition_id = 0], }
2025-03-07 13:44:52.345146  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card0 is an amdgpu device -  FALSE
2025-03-07 13:44:52.345204  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card1 is an amdgpu device - TRUE
2025-03-07 13:44:52.345229  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= start =======, dv_ind = 0
2025-03-07 13:44:52.345237  [TRACE]: rsmi_status_t rsmi_dev_unique_id_get(uint32_t, uint64_t*)| ======= start =======
2025-03-07 13:44:52.345244  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | primary node add ;  BDF = 18446744073709551615
2025-03-07 13:44:52.345252  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | (primary node add) After AddToDeviceList() -->
[node_id = 7; gpu_id = 7426; unique_id = 1919957156416991372; location_id = 49408; bdf = 0x000000000000c100; domain = 0x0000; bus = 0xc1; device = 0x00; function = 0; partition_id = 0], 
2025-03-07 13:44:52.345259  [TRACE]: void amd::smi::RocmSMI::AddToDeviceList(std::string, uint64_t) | ======= start =======
2025-03-07 13:44:52.345380  [TRACE]: int32_t amd::smi::Monitor::setTempSensorLabelMap() | ======= start =======
2025-03-07 13:44:52.345401  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card1/device/hwmon/hwmon1/temp1_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 1 | Data:  | Returning: 2 |
2025-03-07 13:44:52.345434  [INFO]: Successfully read SYSFS file (/sys/class/drm/card1/device/hwmon/hwmon1/temp2_label), returning str = junction
2025-03-07 13:44:52.345441  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card1/device/hwmon/hwmon1/temp2_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 2 | Data: junction | Returning: 0 |
2025-03-07 13:44:52.345471  [INFO]: Successfully read SYSFS file (/sys/class/drm/card1/device/hwmon/hwmon1/temp3_label), returning str = mem
2025-03-07 13:44:52.345477  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card1/device/hwmon/hwmon1/temp3_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 3 | Data: mem | Returning: 0 |
2025-03-07 13:44:52.345492  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card1/device/hwmon/hwmon1/temp4_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 4 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.345507  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card1/device/hwmon/hwmon1/temp5_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 5 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.345522  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card1/device/hwmon/hwmon1/temp6_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 6 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.345536  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card1/device/hwmon/hwmon1/temp7_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 7 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.345552  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card1/device/hwmon/hwmon1/in0_label | Type: MonitorTypes::kMonVoltLabel | Sensor id: 0 | Data:  | Returning: 2 |
2025-03-07 13:44:52.345575  [DEBUG]: uint32_t amd::smi::GetDrmRenderMinor(std::string) | Discovered drmRenderMinor = 128 | For drm_path = /sys/class/drm/card1/device/drm | 
2025-03-07 13:44:52.345605  [DEBUG]: void amd::smi::RocmSMI::AddToDeviceList(std::string, uint64_t) | Adding to device list dev_name = card1 | path = /sys/class/drm/card1 | bdfid = 18446744073709551615 | card index = 1 | 
2025-03-07 13:44:52.345618  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | Ordered system nodes seen in lookup = {
[node_id = 7; gpu_id = 7426; unique_id = 1919957156416991372; location_id = 49408; bdf = 0x000000000000c100; domain = 0x0000; bus = 0xc1; device = 0x00; function = 0; partition_id = 0], 
[node_id = 6; gpu_id = 60723; unique_id = 13297715105545626452; location_id = 33024; bdf = 0x0000000000008100; domain = 0x0000; bus = 0x81; device = 0x00; function = 0; partition_id = 0], 
[node_id = 4; gpu_id = 19794; unique_id = 13321655985203289421; location_id = 256; bdf = 0x0000000000000100; domain = 0x0000; bus = 0x01; device = 0x00; function = 0; partition_id = 0], 
[node_id = 5; gpu_id = 48483; unique_id = 16908369143281941404; location_id = 16640; bdf = 0x0000000000004100; domain = 0x0000; bus = 0x41; device = 0x00; function = 0; partition_id = 0], }
2025-03-07 13:44:52.345625  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= start =======, dv_ind = 0
2025-03-07 13:44:52.345633  [TRACE]: rsmi_status_t get_compute_partition(uint32_t, std::string&) | ======= start =======, 0
2025-03-07 13:44:52.345667  [INFO]: int amd::smi::Device::openSysfsFileStream(amd::smi::DevInfoTypes, T*, const char*) [with T = std::basic_ifstream<char>] | Successfully opened SYSFS file (/sys/class/drm/card1/device/current_compute_partition) for DevInfoInfoType (kDevComputePartition)
2025-03-07 13:44:52.345690  [INFO]: int amd::smi::Device::readDevInfoStr(amd::smi::DevInfoTypes, std::string*)Successfully read device info string for DevInfoType (kDevComputePartition): SPX |  File stream is closed | [GOOD] No bad bit read, successful read operation | [GOOD] No fail - Successful read operation | [GOOD] No eof - Successful read operation | [GOOD] read good - Successful read operation
2025-03-07 13:44:52.345696  [TRACE]: rsmi_status_t get_compute_partition(uint32_t, std::string&) | ======= END =======, 0
2025-03-07 13:44:52.345704  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= end =======  | Success  | Device #: 0 | Type: kDevComputePartition | Data: SPX | Returning = RSMI_STATUS_SUCCESS: The function has been executed successfully. |
2025-03-07 13:44:52.345710  [TRACE]: rsmi_status_t rsmi_dev_unique_id_get(uint32_t, uint64_t*)| ======= start =======
2025-03-07 13:44:52.345737  [INFO]: int amd::smi::Device::openSysfsFileStream(amd::smi::DevInfoTypes, T*, const char*) [with T = std::basic_ifstream<char>] | Successfully opened SYSFS file (/sys/class/drm/card1/device/unique_id) for DevInfoInfoType (kDevUniqueId)
2025-03-07 13:44:52.345747  [INFO]: int amd::smi::Device::readDevInfoStr(amd::smi::DevInfoTypes, std::string*)Successfully read device info string for DevInfoType (kDevUniqueId): b8e0078991ff9d4d |  File stream is closed | [GOOD] No bad bit read, successful read operation | [GOOD] No fail - Successful read operation | [GOOD] No eof - Successful read operation | [GOOD] read good - Successful read operation
2025-03-07 13:44:52.345757  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | device/node id (cardId) = 1 | card id (cardAdded) = 0 | numMonDevices = 1 | compute partition = SPX | temp_primary_unique_id = 13321655985203289421 | Num of nodes matching temp_primary_unique_id = 1 | device_uuid (hex/uint) = Hex (MSB): 0xb8e0078991ff9d4d, Unsigned int: 13321655985203289421, Byte Size: 8, Bits: 64 | device_uuid (uint64_t) = 13321655985203289421
2025-03-07 13:44:52.345763  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | REFRESH - primary_unique_id = 13321655985203289421 has 1 known gpu nodes
2025-03-07 13:44:52.345770  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | After finding primary_unique_id = 13321655985203289421 erased 1 nodes
2025-03-07 13:44:52.345808  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card2 is an amdgpu device -  FALSE
2025-03-07 13:44:52.345836  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card3 is an amdgpu device -  FALSE
2025-03-07 13:44:52.345866  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card4 is an amdgpu device -  FALSE
2025-03-07 13:44:52.345911  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card5 is an amdgpu device -  FALSE
2025-03-07 13:44:52.345944  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card6 is an amdgpu device -  FALSE
2025-03-07 13:44:52.345973  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card7 is an amdgpu device -  FALSE
2025-03-07 13:44:52.346003  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card8 is an amdgpu device -  FALSE
2025-03-07 13:44:52.346058  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card9 is an amdgpu device - TRUE
2025-03-07 13:44:52.346065  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= start =======, dv_ind = 1
2025-03-07 13:44:52.346071  [TRACE]: rsmi_status_t rsmi_dev_unique_id_get(uint32_t, uint64_t*)| ======= start =======
2025-03-07 13:44:52.346077  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | primary node add ;  BDF = 18446744073709551615
2025-03-07 13:44:52.346089  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | (primary node add) After AddToDeviceList() -->
[node_id = 7; gpu_id = 7426; unique_id = 1919957156416991372; location_id = 49408; bdf = 0x000000000000c100; domain = 0x0000; bus = 0xc1; device = 0x00; function = 0; partition_id = 0], 
2025-03-07 13:44:52.346096  [TRACE]: void amd::smi::RocmSMI::AddToDeviceList(std::string, uint64_t) | ======= start =======
2025-03-07 13:44:52.346175  [TRACE]: int32_t amd::smi::Monitor::setTempSensorLabelMap() | ======= start =======
2025-03-07 13:44:52.346191  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card9/device/hwmon/hwmon2/temp1_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 1 | Data:  | Returning: 2 |
2025-03-07 13:44:52.346222  [INFO]: Successfully read SYSFS file (/sys/class/drm/card9/device/hwmon/hwmon2/temp2_label), returning str = junction
2025-03-07 13:44:52.346229  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card9/device/hwmon/hwmon2/temp2_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 2 | Data: junction | Returning: 0 |
2025-03-07 13:44:52.346259  [INFO]: Successfully read SYSFS file (/sys/class/drm/card9/device/hwmon/hwmon2/temp3_label), returning str = mem
2025-03-07 13:44:52.346266  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card9/device/hwmon/hwmon2/temp3_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 3 | Data: mem | Returning: 0 |
2025-03-07 13:44:52.346281  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card9/device/hwmon/hwmon2/temp4_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 4 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.346296  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card9/device/hwmon/hwmon2/temp5_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 5 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.346311  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card9/device/hwmon/hwmon2/temp6_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 6 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.346326  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card9/device/hwmon/hwmon2/temp7_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 7 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.346343  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card9/device/hwmon/hwmon2/in0_label | Type: MonitorTypes::kMonVoltLabel | Sensor id: 0 | Data:  | Returning: 2 |
2025-03-07 13:44:52.346365  [DEBUG]: uint32_t amd::smi::GetDrmRenderMinor(std::string) | Discovered drmRenderMinor = 136 | For drm_path = /sys/class/drm/card9/device/drm | 
2025-03-07 13:44:52.346381  [DEBUG]: void amd::smi::RocmSMI::AddToDeviceList(std::string, uint64_t) | Adding to device list dev_name = card9 | path = /sys/class/drm/card9 | bdfid = 18446744073709551615 | card index = 9 | 
2025-03-07 13:44:52.346392  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | Ordered system nodes seen in lookup = {
[node_id = 7; gpu_id = 7426; unique_id = 1919957156416991372; location_id = 49408; bdf = 0x000000000000c100; domain = 0x0000; bus = 0xc1; device = 0x00; function = 0; partition_id = 0], 
[node_id = 6; gpu_id = 60723; unique_id = 13297715105545626452; location_id = 33024; bdf = 0x0000000000008100; domain = 0x0000; bus = 0x81; device = 0x00; function = 0; partition_id = 0], 
[node_id = 5; gpu_id = 48483; unique_id = 16908369143281941404; location_id = 16640; bdf = 0x0000000000004100; domain = 0x0000; bus = 0x41; device = 0x00; function = 0; partition_id = 0], }
2025-03-07 13:44:52.346404  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= start =======, dv_ind = 1
2025-03-07 13:44:52.346410  [TRACE]: rsmi_status_t get_compute_partition(uint32_t, std::string&) | ======= start =======, 1
2025-03-07 13:44:52.346436  [INFO]: int amd::smi::Device::openSysfsFileStream(amd::smi::DevInfoTypes, T*, const char*) [with T = std::basic_ifstream<char>] | Successfully opened SYSFS file (/sys/class/drm/card9/device/current_compute_partition) for DevInfoInfoType (kDevComputePartition)
2025-03-07 13:44:52.346457  [INFO]: int amd::smi::Device::readDevInfoStr(amd::smi::DevInfoTypes, std::string*)Successfully read device info string for DevInfoType (kDevComputePartition): SPX |  File stream is closed | [GOOD] No bad bit read, successful read operation | [GOOD] No fail - Successful read operation | [GOOD] No eof - Successful read operation | [GOOD] read good - Successful read operation
2025-03-07 13:44:52.346464  [TRACE]: rsmi_status_t get_compute_partition(uint32_t, std::string&) | ======= END =======, 1
2025-03-07 13:44:52.346470  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= end =======  | Success  | Device #: 1 | Type: kDevComputePartition | Data: SPX | Returning = RSMI_STATUS_SUCCESS: The function has been executed successfully. |
2025-03-07 13:44:52.346477  [TRACE]: rsmi_status_t rsmi_dev_unique_id_get(uint32_t, uint64_t*)| ======= start =======
2025-03-07 13:44:52.346503  [INFO]: int amd::smi::Device::openSysfsFileStream(amd::smi::DevInfoTypes, T*, const char*) [with T = std::basic_ifstream<char>] | Successfully opened SYSFS file (/sys/class/drm/card9/device/unique_id) for DevInfoInfoType (kDevUniqueId)
2025-03-07 13:44:52.346512  [INFO]: int amd::smi::Device::readDevInfoStr(amd::smi::DevInfoTypes, std::string*)Successfully read device info string for DevInfoType (kDevUniqueId): eaa69826c47efb9c |  File stream is closed | [GOOD] No bad bit read, successful read operation | [GOOD] No fail - Successful read operation | [GOOD] No eof - Successful read operation | [GOOD] read good - Successful read operation
2025-03-07 13:44:52.346521  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | device/node id (cardId) = 9 | card id (cardAdded) = 1 | numMonDevices = 2 | compute partition = SPX | temp_primary_unique_id = 16908369143281941404 | Num of nodes matching temp_primary_unique_id = 1 | device_uuid (hex/uint) = Hex (MSB): 0xeaa69826c47efb9c, Unsigned int: 16908369143281941404, Byte Size: 8, Bits: 64 | device_uuid (uint64_t) = 16908369143281941404
2025-03-07 13:44:52.346527  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | REFRESH - primary_unique_id = 16908369143281941404 has 1 known gpu nodes
2025-03-07 13:44:52.346534  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | After finding primary_unique_id = 16908369143281941404 erased 1 nodes
2025-03-07 13:44:52.346567  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card10 is an amdgpu device -  FALSE
2025-03-07 13:44:52.346594  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card11 is an amdgpu device -  FALSE
2025-03-07 13:44:52.346623  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card12 is an amdgpu device -  FALSE
2025-03-07 13:44:52.346654  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card13 is an amdgpu device -  FALSE
2025-03-07 13:44:52.346685  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card14 is an amdgpu device -  FALSE
2025-03-07 13:44:52.346716  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card15 is an amdgpu device -  FALSE
2025-03-07 13:44:52.346744  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card16 is an amdgpu device -  FALSE
2025-03-07 13:44:52.346799  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card17 is an amdgpu device - TRUE
2025-03-07 13:44:52.346805  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= start =======, dv_ind = 2
2025-03-07 13:44:52.346811  [TRACE]: rsmi_status_t rsmi_dev_unique_id_get(uint32_t, uint64_t*)| ======= start =======
2025-03-07 13:44:52.346818  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | primary node add ;  BDF = 18446744073709551615
2025-03-07 13:44:52.346825  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | (primary node add) After AddToDeviceList() -->
[node_id = 7; gpu_id = 7426; unique_id = 1919957156416991372; location_id = 49408; bdf = 0x000000000000c100; domain = 0x0000; bus = 0xc1; device = 0x00; function = 0; partition_id = 0], 
2025-03-07 13:44:52.346832  [TRACE]: void amd::smi::RocmSMI::AddToDeviceList(std::string, uint64_t) | ======= start =======
2025-03-07 13:44:52.346917  [TRACE]: int32_t amd::smi::Monitor::setTempSensorLabelMap() | ======= start =======
2025-03-07 13:44:52.346935  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card17/device/hwmon/hwmon3/temp1_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 1 | Data:  | Returning: 2 |
2025-03-07 13:44:52.346966  [INFO]: Successfully read SYSFS file (/sys/class/drm/card17/device/hwmon/hwmon3/temp2_label), returning str = junction
2025-03-07 13:44:52.346973  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card17/device/hwmon/hwmon3/temp2_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 2 | Data: junction | Returning: 0 |
2025-03-07 13:44:52.347003  [INFO]: Successfully read SYSFS file (/sys/class/drm/card17/device/hwmon/hwmon3/temp3_label), returning str = mem
2025-03-07 13:44:52.347009  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card17/device/hwmon/hwmon3/temp3_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 3 | Data: mem | Returning: 0 |
2025-03-07 13:44:52.347024  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card17/device/hwmon/hwmon3/temp4_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 4 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.347039  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card17/device/hwmon/hwmon3/temp5_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 5 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.347054  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card17/device/hwmon/hwmon3/temp6_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 6 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.347069  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card17/device/hwmon/hwmon3/temp7_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 7 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.347084  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card17/device/hwmon/hwmon3/in0_label | Type: MonitorTypes::kMonVoltLabel | Sensor id: 0 | Data:  | Returning: 2 |
2025-03-07 13:44:52.347107  [DEBUG]: uint32_t amd::smi::GetDrmRenderMinor(std::string) | Discovered drmRenderMinor = 144 | For drm_path = /sys/class/drm/card17/device/drm | 
2025-03-07 13:44:52.347123  [DEBUG]: void amd::smi::RocmSMI::AddToDeviceList(std::string, uint64_t) | Adding to device list dev_name = card17 | path = /sys/class/drm/card17 | bdfid = 18446744073709551615 | card index = 17 | 
2025-03-07 13:44:52.347132  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | Ordered system nodes seen in lookup = {
[node_id = 7; gpu_id = 7426; unique_id = 1919957156416991372; location_id = 49408; bdf = 0x000000000000c100; domain = 0x0000; bus = 0xc1; device = 0x00; function = 0; partition_id = 0], 
[node_id = 6; gpu_id = 60723; unique_id = 13297715105545626452; location_id = 33024; bdf = 0x0000000000008100; domain = 0x0000; bus = 0x81; device = 0x00; function = 0; partition_id = 0], }
2025-03-07 13:44:52.347141  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= start =======, dv_ind = 2
2025-03-07 13:44:52.347147  [TRACE]: rsmi_status_t get_compute_partition(uint32_t, std::string&) | ======= start =======, 2
2025-03-07 13:44:52.347174  [INFO]: int amd::smi::Device::openSysfsFileStream(amd::smi::DevInfoTypes, T*, const char*) [with T = std::basic_ifstream<char>] | Successfully opened SYSFS file (/sys/class/drm/card17/device/current_compute_partition) for DevInfoInfoType (kDevComputePartition)
2025-03-07 13:44:52.347193  [INFO]: int amd::smi::Device::readDevInfoStr(amd::smi::DevInfoTypes, std::string*)Successfully read device info string for DevInfoType (kDevComputePartition): SPX |  File stream is closed | [GOOD] No bad bit read, successful read operation | [GOOD] No fail - Successful read operation | [GOOD] No eof - Successful read operation | [GOOD] read good - Successful read operation
2025-03-07 13:44:52.347199  [TRACE]: rsmi_status_t get_compute_partition(uint32_t, std::string&) | ======= END =======, 2
2025-03-07 13:44:52.347206  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= end =======  | Success  | Device #: 2 | Type: kDevComputePartition | Data: SPX | Returning = RSMI_STATUS_SUCCESS: The function has been executed successfully. |
2025-03-07 13:44:52.347212  [TRACE]: rsmi_status_t rsmi_dev_unique_id_get(uint32_t, uint64_t*)| ======= start =======
2025-03-07 13:44:52.347238  [INFO]: int amd::smi::Device::openSysfsFileStream(amd::smi::DevInfoTypes, T*, const char*) [with T = std::basic_ifstream<char>] | Successfully opened SYSFS file (/sys/class/drm/card17/device/unique_id) for DevInfoInfoType (kDevUniqueId)
2025-03-07 13:44:52.347248  [INFO]: int amd::smi::Device::readDevInfoStr(amd::smi::DevInfoTypes, std::string*)Successfully read device info string for DevInfoType (kDevUniqueId): b88af96f2664a354 |  File stream is closed | [GOOD] No bad bit read, successful read operation | [GOOD] No fail - Successful read operation | [GOOD] No eof - Successful read operation | [GOOD] read good - Successful read operation
2025-03-07 13:44:52.347256  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | device/node id (cardId) = 17 | card id (cardAdded) = 2 | numMonDevices = 3 | compute partition = SPX | temp_primary_unique_id = 13297715105545626452 | Num of nodes matching temp_primary_unique_id = 1 | device_uuid (hex/uint) = Hex (MSB): 0xb88af96f2664a354, Unsigned int: 13297715105545626452, Byte Size: 8, Bits: 64 | device_uuid (uint64_t) = 13297715105545626452
2025-03-07 13:44:52.347262  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | REFRESH - primary_unique_id = 13297715105545626452 has 1 known gpu nodes
2025-03-07 13:44:52.347268  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | After finding primary_unique_id = 13297715105545626452 erased 1 nodes
2025-03-07 13:44:52.347300  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card18 is an amdgpu device -  FALSE
2025-03-07 13:44:52.347330  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card19 is an amdgpu device -  FALSE
2025-03-07 13:44:52.347359  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card20 is an amdgpu device -  FALSE
2025-03-07 13:44:52.347389  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card21 is an amdgpu device -  FALSE
2025-03-07 13:44:52.347419  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card22 is an amdgpu device -  FALSE
2025-03-07 13:44:52.347452  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card23 is an amdgpu device -  FALSE
2025-03-07 13:44:52.347483  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card24 is an amdgpu device -  FALSE
2025-03-07 13:44:52.347537  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card25 is an amdgpu device - TRUE
2025-03-07 13:44:52.347543  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= start =======, dv_ind = 3
2025-03-07 13:44:52.347549  [TRACE]: rsmi_status_t rsmi_dev_unique_id_get(uint32_t, uint64_t*)| ======= start =======
2025-03-07 13:44:52.347556  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | primary node add ;  BDF = 18446744073709551615
2025-03-07 13:44:52.347563  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | (primary node add) After AddToDeviceList() -->
[node_id = 7; gpu_id = 7426; unique_id = 1919957156416991372; location_id = 49408; bdf = 0x000000000000c100; domain = 0x0000; bus = 0xc1; device = 0x00; function = 0; partition_id = 0], 
2025-03-07 13:44:52.347570  [TRACE]: void amd::smi::RocmSMI::AddToDeviceList(std::string, uint64_t) | ======= start =======
2025-03-07 13:44:52.347643  [TRACE]: int32_t amd::smi::Monitor::setTempSensorLabelMap() | ======= start =======
2025-03-07 13:44:52.347659  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card25/device/hwmon/hwmon4/temp1_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 1 | Data:  | Returning: 2 |
2025-03-07 13:44:52.347688  [INFO]: Successfully read SYSFS file (/sys/class/drm/card25/device/hwmon/hwmon4/temp2_label), returning str = junction
2025-03-07 13:44:52.347695  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card25/device/hwmon/hwmon4/temp2_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 2 | Data: junction | Returning: 0 |
2025-03-07 13:44:52.347725  [INFO]: Successfully read SYSFS file (/sys/class/drm/card25/device/hwmon/hwmon4/temp3_label), returning str = mem
2025-03-07 13:44:52.347731  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card25/device/hwmon/hwmon4/temp3_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 3 | Data: mem | Returning: 0 |
2025-03-07 13:44:52.347747  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card25/device/hwmon/hwmon4/temp4_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 4 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.347762  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card25/device/hwmon/hwmon4/temp5_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 5 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.347777  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card25/device/hwmon/hwmon4/temp6_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 6 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.347792  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card25/device/hwmon/hwmon4/temp7_label | Type: MonitorTypes::kMonTempLabel | Sensor id: 7 | Data: mem | Returning: 2 |
2025-03-07 13:44:52.347807  [INFO]: int amd::smi::Monitor::readMonitor(amd::smi::MonitorTypes, uint32_t, std::string*) | Success | Read hwmon file: /sys/class/drm/card25/device/hwmon/hwmon4/in0_label | Type: MonitorTypes::kMonVoltLabel | Sensor id: 0 | Data:  | Returning: 2 |
2025-03-07 13:44:52.347827  [DEBUG]: uint32_t amd::smi::GetDrmRenderMinor(std::string) | Discovered drmRenderMinor = 152 | For drm_path = /sys/class/drm/card25/device/drm | 
2025-03-07 13:44:52.347845  [DEBUG]: void amd::smi::RocmSMI::AddToDeviceList(std::string, uint64_t) | Adding to device list dev_name = card25 | path = /sys/class/drm/card25 | bdfid = 18446744073709551615 | card index = 25 | 
2025-03-07 13:44:52.347853  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | Ordered system nodes seen in lookup = {
[node_id = 7; gpu_id = 7426; unique_id = 1919957156416991372; location_id = 49408; bdf = 0x000000000000c100; domain = 0x0000; bus = 0xc1; device = 0x00; function = 0; partition_id = 0], }
2025-03-07 13:44:52.347859  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= start =======, dv_ind = 3
2025-03-07 13:44:52.347865  [TRACE]: rsmi_status_t get_compute_partition(uint32_t, std::string&) | ======= start =======, 3
2025-03-07 13:44:52.347901  [INFO]: int amd::smi::Device::openSysfsFileStream(amd::smi::DevInfoTypes, T*, const char*) [with T = std::basic_ifstream<char>] | Successfully opened SYSFS file (/sys/class/drm/card25/device/current_compute_partition) for DevInfoInfoType (kDevComputePartition)
2025-03-07 13:44:52.347918  [INFO]: int amd::smi::Device::readDevInfoStr(amd::smi::DevInfoTypes, std::string*)Successfully read device info string for DevInfoType (kDevComputePartition): SPX |  File stream is closed | [GOOD] No bad bit read, successful read operation | [GOOD] No fail - Successful read operation | [GOOD] No eof - Successful read operation | [GOOD] read good - Successful read operation
2025-03-07 13:44:52.347925  [TRACE]: rsmi_status_t get_compute_partition(uint32_t, std::string&) | ======= END =======, 3
2025-03-07 13:44:52.347931  [TRACE]: rsmi_status_t rsmi_dev_compute_partition_get(uint32_t, char*, uint32_t) | ======= end =======  | Success  | Device #: 3 | Type: kDevComputePartition | Data: SPX | Returning = RSMI_STATUS_SUCCESS: The function has been executed successfully. |
2025-03-07 13:44:52.347937  [TRACE]: rsmi_status_t rsmi_dev_unique_id_get(uint32_t, uint64_t*)| ======= start =======
2025-03-07 13:44:52.347963  [INFO]: int amd::smi::Device::openSysfsFileStream(amd::smi::DevInfoTypes, T*, const char*) [with T = std::basic_ifstream<char>] | Successfully opened SYSFS file (/sys/class/drm/card25/device/unique_id) for DevInfoInfoType (kDevUniqueId)
2025-03-07 13:44:52.347972  [INFO]: int amd::smi::Device::readDevInfoStr(amd::smi::DevInfoTypes, std::string*)Successfully read device info string for DevInfoType (kDevUniqueId): 1aa50edc8434308c |  File stream is closed | [GOOD] No bad bit read, successful read operation | [GOOD] No fail - Successful read operation | [GOOD] No eof - Successful read operation | [GOOD] read good - Successful read operation
2025-03-07 13:44:52.347980  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | device/node id (cardId) = 25 | card id (cardAdded) = 3 | numMonDevices = 4 | compute partition = SPX | temp_primary_unique_id = 1919957156416991372 | Num of nodes matching temp_primary_unique_id = 1 | device_uuid (hex/uint) = Hex (MSB): 0x1aa50edc8434308c, Unsigned int: 1919957156416991372, Byte Size: 8, Bits: 64 | device_uuid (uint64_t) = 1919957156416991372
2025-03-07 13:44:52.347987  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | REFRESH - primary_unique_id = 1919957156416991372 has 1 known gpu nodes
2025-03-07 13:44:52.347993  [DEBUG]: uint32_t amd::smi::RocmSMI::DiscoverAmdgpuDevices() | After finding primary_unique_id = 1919957156416991372 erased 1 nodes
2025-03-07 13:44:52.348022  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card26 is an amdgpu device -  FALSE
2025-03-07 13:44:52.348048  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card27 is an amdgpu device -  FALSE
2025-03-07 13:44:52.348080  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card28 is an amdgpu device -  FALSE
2025-03-07 13:44:52.348108  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card29 is an amdgpu device -  FALSE
2025-03-07 13:44:52.348134  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card30 is an amdgpu device -  FALSE
2025-03-07 13:44:52.348167  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card31 is an amdgpu device -  FALSE
2025-03-07 13:44:52.348196  [DEBUG]: bool amd::smi::isAMDGPU(std::string) | device_path = /sys/class/drm/card32 is an amdgpu device -  FALSE
2025-03-07 13:44:52.348208  [TRACE]: void amd::smi::RocmSMI::Initialize(uint64_t) | [before] device->path() = /sys/class/drm/card1
 | bdfid = 256
 | device->bdfid() = 18446744073709551615 (0xffffffffffffffff)
 | (legacy/pcie card) setting device->set_bdfid(bdfid)
2025-03-07 13:44:52.348215  [TRACE]: void amd::smi::RocmSMI::Initialize(uint64_t) | [after] device->path() = /sys/class/drm/card1
 | bdfid = 256
 | device->bdfid() = 256 (0x0000000000000100)
 | final update: device->bdfid() holds correct device bdf
2025-03-07 13:44:52.348225  [TRACE]: void amd::smi::RocmSMI::Initialize(uint64_t) | [before] device->path() = /sys/class/drm/card9
 | bdfid = 16640
 | device->bdfid() = 18446744073709551615 (0xffffffffffffffff)
 | (legacy/pcie card) setting device->set_bdfid(bdfid)
2025-03-07 13:44:52.348231  [TRACE]: void amd::smi::RocmSMI::Initialize(uint64_t) | [after] device->path() = /sys/class/drm/card9
 | bdfid = 16640
 | device->bdfid() = 16640 (0x0000000000004100)
 | final update: device->bdfid() holds correct device bdf
2025-03-07 13:44:52.348241  [TRACE]: void amd::smi::RocmSMI::Initialize(uint64_t) | [before] device->path() = /sys/class/drm/card17
 | bdfid = 33024
 | device->bdfid() = 18446744073709551615 (0xffffffffffffffff)
 | (legacy/pcie card) setting device->set_bdfid(bdfid)
2025-03-07 13:44:52.348247  [TRACE]: void amd::smi::RocmSMI::Initialize(uint64_t) | [after] device->path() = /sys/class/drm/card17
 | bdfid = 33024
 | device->bdfid() = 33024 (0x0000000000008100)
 | final update: device->bdfid() holds correct device bdf
2025-03-07 13:44:52.348257  [TRACE]: void amd::smi::RocmSMI::Initialize(uint64_t) | [before] device->path() = /sys/class/drm/card25
 | bdfid = 49408
 | device->bdfid() = 18446744073709551615 (0xffffffffffffffff)
 | (legacy/pcie card) setting device->set_bdfid(bdfid)
2025-03-07 13:44:52.348263  [TRACE]: void amd::smi::RocmSMI::Initialize(uint64_t) | [after] device->path() = /sys/class/drm/card25
 | bdfid = 49408
 | device->bdfid() = 49408 (0x000000000000c100)
 | final update: device->bdfid() holds correct device bdf
2025-03-07 13:44:52.348270  [DEBUG]: void amd::smi::RocmSMI::Initialize(uint64_t) Sort index based on BDF.
2025-03-07 13:44:52.351045  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/4/properties | Successfully read node #4 for property_name = gfx_target_version | Data (gfx_target_version) * val = 90402 | return = 0 | 
2025-03-07 13:44:52.351059  [DEBUG]: int amd::smi::KFDNode::get_gfx_target_version(uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/4/properties | Read node: 4 for gfx_target_version | Data (*gfx_target_version): 90402 | Return: RSMI_STATUS_SUCCESS | 
2025-03-07 13:44:52.351067  [INFO]: rsmi_status_t amd::smi::rsmi_get_gfx_target_version(uint32_t, std::string*) | kfd_target_version = 90402; major = 900; minor = 40; rev = 2
Reporting rsmi_get_gfx_target_version = gfx942

2025-03-07 13:44:52.351328  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/5/properties | Successfully read node #5 for property_name = gfx_target_version | Data (gfx_target_version) * val = 90402 | return = 0 | 
2025-03-07 13:44:52.351337  [DEBUG]: int amd::smi::KFDNode::get_gfx_target_version(uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/5/properties | Read node: 5 for gfx_target_version | Data (*gfx_target_version): 90402 | Return: RSMI_STATUS_SUCCESS | 
2025-03-07 13:44:52.351343  [INFO]: rsmi_status_t amd::smi::rsmi_get_gfx_target_version(uint32_t, std::string*) | kfd_target_version = 90402; major = 900; minor = 40; rev = 2
Reporting rsmi_get_gfx_target_version = gfx942

2025-03-07 13:44:52.351609  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/6/properties | Successfully read node #6 for property_name = gfx_target_version | Data (gfx_target_version) * val = 90402 | return = 0 | 
2025-03-07 13:44:52.351618  [DEBUG]: int amd::smi::KFDNode::get_gfx_target_version(uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/6/properties | Read node: 6 for gfx_target_version | Data (*gfx_target_version): 90402 | Return: RSMI_STATUS_SUCCESS | 
2025-03-07 13:44:52.351624  [INFO]: rsmi_status_t amd::smi::rsmi_get_gfx_target_version(uint32_t, std::string*) | kfd_target_version = 90402; major = 900; minor = 40; rev = 2
Reporting rsmi_get_gfx_target_version = gfx942

2025-03-07 13:44:52.351904  [DEBUG]: int amd::smi::read_node_properties(uint32_t, std::string, uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/7/properties | Successfully read node #7 for property_name = gfx_target_version | Data (gfx_target_version) * val = 90402 | return = 0 | 
2025-03-07 13:44:52.351914  [DEBUG]: int amd::smi::KFDNode::get_gfx_target_version(uint64_t*) | File: /sys/class/kfd/kfd/topology/nodes/7/properties | Read node: 7 for gfx_target_version | Data (*gfx_target_version): 90402 | Return: RSMI_STATUS_SUCCESS | 
2025-03-07 13:44:52.351921  [INFO]: rsmi_status_t amd::smi::rsmi_get_gfx_target_version(uint32_t, std::string*) | kfd_target_version = 90402; major = 900; minor = 40; rev = 2
Reporting rsmi_get_gfx_target_version = gfx942

2025-03-07 13:44:52.351929  [INFO]: ====== Gathered system details ============
SYSTEM NAME: Linux
OS DISTRIBUTION: Rocky Linux 9.5 (Blue Onyx)
NODE NAME: nicholson
RELEASE: 5.14.0-503.19.1.el9_5.x86_64
VERSION: #1 SMP PREEMPT_DYNAMIC Thu Dec 19 12:55:03 UTC 2024
MACHINE TYPE: x86_64
DOMAIN: (none)
ENDIANNESS: Little Endian, multi-bit symbols encoded as little endian (LSB first)
ROCM BUILD TYPE: debug
ROCM-SMI-LIB PATH: /opt/rocm-6.3.1/libexec/rocm_smi/../../lib/librocm_smi64.so.7
ROCM-SMI-LIB BUILD DATE: Sat Jan 11 11:15:45 2025
ROCM ENV VARIABLES: 
	RSMI_DEBUG_BITFIELD = <undefined>
	RSMI_DEBUG_DRM_ROOT_OVERRIDE = <undefined>
	RSMI_DEBUG_HWMON_ROOT_OVERRIDE = <undefined>
	RSMI_DEBUG_PP_ROOT_OVERRIDE = <undefined>
	RSMI_DEBUG_INFINITE_LOOP = <undefined>
	RSMI_LOGGING = 1
	RSMI_LOGGING (are logs on) = TRUE
	RSMI_DEBUG_ENUM_OVERRIDE = {}
AMD GFX VERSIONS: 
	Device[0]: gfx942
	Device[1]: gfx942
	Device[2]: gfx942
	Device[3]: gfx942

2025-03-07 13:44:52.351937  [DEBUG]: void amd::smi::RocmSMI::Initialize(uint64_t) | current device paths = Vector = {/sys/class/drm/card1, /sys/class/drm/card9, /sys/class/drm/card17, /sys/class/drm/card25}

2025-03-07 13:44:52.352007  [TRACE]: rsmi_status_t rsmi_dev_vendor_id_get(uint32_t, uint16_t*)| ======= start =======
2025-03-07 13:44:52.352035  [INFO]: int amd::smi::Device::openSysfsFileStream(amd::smi::DevInfoTypes, T*, const char*) [with T = std::basic_ifstream<char>] | Successfully opened SYSFS file (/sys/class/drm/card1/device/vendor) for DevInfoInfoType (kDevVendorID)
2025-03-07 13:44:52.352045  [INFO]: int amd::smi::Device::readDevInfoStr(amd::smi::DevInfoTypes, std::string*)Successfully read device info string for DevInfoType (kDevVendorID): 0x1002 |  File stream is closed | [GOOD] No bad bit read, successful read operation | [GOOD] No fail - Successful read operation | [GOOD] No eof - Successful read operation | [GOOD] read good - Successful read operation
2025-03-07 13:44:52.352155  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/pasid), returning str = 32776
2025-03-07 13:44:52.352246  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/pasid), returning str = 32776
2025-03-07 13:44:52.352278  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/vram_60723), returning str = 0
2025-03-07 13:44:52.352325  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/sdma_60723), returning str = 0
2025-03-07 13:44:52.352360  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/stats_60723/cu_occupancy), returning str = 0
2025-03-07 13:44:52.352390  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/vram_48483), returning str = 0
2025-03-07 13:44:52.352421  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/sdma_48483), returning str = 0
2025-03-07 13:44:52.352453  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/stats_48483/cu_occupancy), returning str = 0
2025-03-07 13:44:52.352481  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/vram_19794), returning str = 0
2025-03-07 13:44:52.352514  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/sdma_19794), returning str = 0
2025-03-07 13:44:52.352547  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/stats_19794/cu_occupancy), returning str = 0
2025-03-07 13:44:52.352572  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/vram_7426), returning str = 0
2025-03-07 13:44:52.352603  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/sdma_7426), returning str = 0
2025-03-07 13:44:52.352636  [INFO]: Successfully read SYSFS file (/sys/class/kfd/kfd/proc/1684336/stats_7426/cu_occupancy), returning str = 0
```

Running `rocm-smi --setcomputepartition TPX` while it is running indeed outputs the following:
```
============================ ROCm System Management Interface ============================
============================== Set compute partition to TPX ==============================
GPU[0]          : Device is currently busy, try again later
GPU[1]          : Device is currently busy, try again later
GPU[2]          : Device is currently busy, try again later
GPU[3]          : Device is currently busy, try again later
==========================================================================================
================================== End of ROCm SMI Log ===================================
```

Running `amd-smi process` while it is running outputs the following:
```
[1] 1689147
GPU: 0
    PROCESS_INFO: No running processes detected

GPU: 1
    PROCESS_INFO: No running processes detected

GPU: 2
    PROCESS_INFO: No running processes detected

GPU: 3
    PROCESS_INFO: No running processes detected
```

Running `amd-smi set --compute-partition TPX` while the process is running produces the following:
```
[1] 1689277
amdsmi.amdsmi_exception.AmdSmiLibraryException: Error code:
        30 | AMDSMI_STATUS_BUSY - Device busy

The above exception was the direct cause of the following exception:

ValueError: Unable to set compute partition to TPX on GPU ID: 0 BDF:0000:01:00.0
```

Some things which might differ from the original issue:
- Our system is running Rocky Linux 9.5 (original issue is Ubuntu 22).
- Out system is running ROCm 6.3.1 (original issue is 6.3.3).

Differences acknowledged, it seems the behavior is still consistent.


---

### 评论 #7 — darren-amd (2025-03-07T20:27:42Z)

Thanks @garrettbyrd @fluidnumerics-joe for the offer and logs,

I was able to get my hands on an MI300A system internally and have been able to reproduce the issue as well. I suspect it is related to access to `/dev/kfd` as previously mentioned but am investigating further, will keep everyone updated, thanks!


---

### 评论 #8 — garrettbyrd (2025-04-03T19:25:12Z)

@darren-amd any updates on this? Let me know if you need reliable access to an MI300A system, we'd be more than happy to provide access for this type of triage.

---

### 评论 #9 — darren-amd (2025-04-25T06:45:36Z)

Hi @garrettbyrd @maxweiss,

I have access to a machine and an internal team is looking into this issue currently, I will follow up and see if I can get an update for this issue, thanks!

---
