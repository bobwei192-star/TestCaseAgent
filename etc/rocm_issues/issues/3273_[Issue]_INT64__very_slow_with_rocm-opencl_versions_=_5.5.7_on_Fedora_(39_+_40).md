# [Issue]: INT64 _very_slow with rocm-opencl versions >= 5.5.7 on Fedora (39 + 40)

> **Issue #3273**
> **状态**: closed
> **创建时间**: 2024-06-10T01:22:35Z
> **更新时间**: 2024-09-13T20:58:51Z
> **关闭时间**: 2024-09-11T13:17:44Z
> **作者**: ImperiousLeader
> **标签**: Under Investigation, ROCm 6.0.0, ROCm 5.7.1, AMD Radeon RX 7900 XTX, ROCm 5.6.0, ROCm 5.7.0, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3273

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **ROCm 5.7.1** (颜色: #ededed)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 5.6.0** (颜色: #ededed)
- **ROCm 5.7.0** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

When comparing INT64 in very large arrays I have a significant slow down when using rocm-opencl since 5.5.7 onwards.

I copy the very large array to global memory prior to commencement of the comparison check.
My kernel compares 15,000 INT64 values against an 14Gb array of INT64 values, using a VERY basic kernel that essentially says if (myBigArray[get_global_id()] == targetValue) atomic_inc a pointer.

When using rocm-opencl-5.5.1 on Fedora 39 or 40 (currently using FC40) I can perform approximately 1.7 Trillion comparisons per second on a 7900XTX or 1.2 Trillion comparisons per second of a 6900XT. 
When using rocm-opencl-5.7.1, this crashed to 450 and 350 billion comparisons / sec respectively. Using rocm-opencl-6.0.2, the system freezes.

- Downgrading the version of rocm-opencl to 5.5.1 on any version of Fedora resolves the issue with speed of comparison returned to normal.
- There is no issue running the same opencl on a machine with RTX308ti's using the Nvidia libOpenCL.so.
- When using a known test value - the comparison succeeds the pointer is incremented and returned correctly by the kernel.
- There is no difference switching between LLVM and GCC, although I use GCC by default.

### Operating System

Fedora 40

### CPU

AMD Ryzen 5950x

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0, ROCm 6.0.0, ROCm 5.7.1, ROCm 5.7.0, ROCm 5.6.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (45 条)

### 评论 #1 — ImperiousLeader (2024-06-12T00:50:41Z)

rocminfo --support output

[37mROCk module is loaded[0m
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
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
  Name:                    AMD Ryzen 9 5950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 5950X 16-Core Processor
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
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65740764(0x3eb1fdc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65740764(0x3eb1fdc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65740764(0x3eb1fdc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-5c811bd7666b1682               
  Marketing Name:          AMD Radeon RX 7900 XTX             
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
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2526                               
  BDFID:                   1536                               
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
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
  Packet Processor uCode:: 102                                
  SDMA engine uCode::      20                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
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
Agent 3                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-dedf2bc303025e57               
  Marketing Name:          AMD Radeon RX 6900 XT              
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
    L1:                      16(0x10) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      131072(0x20000) KB                 
  Chip ID:                 29631(0x73bf)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2660                               
  BDFID:                   2816                               
  Internal Node ID:        2                                  
  Compute Unit:            80                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
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
  Packet Processor uCode:: 118                                
  SDMA engine uCode::      83                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1030         
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

---

### 评论 #2 — ImperiousLeader (2024-06-12T00:56:03Z)

The kernel:
   __kernel void Int_Search(global unsigned long *trip,global unsigned int *idx,global unsigned int *wire,global unsigned long *hugeArray,constant unsigned int *testCnt, global unsigned int *cnt) {
     unsigned int i = get_global_id(0);
      unsigned int a;
      for (a = 0; a < *testCnt; a++) {
        if (hugeArray[a] == trip[i]) {
          idx[*cnt]  = a;
          wire[*cnt] = i;
          atomic_inc(cnt);
        }
      }
    }


---

### 评论 #3 — ImperiousLeader (2024-06-12T01:00:44Z)

Prior to invoking the kernel the following is used to ensure the huge array is copied to the device: 

tripwires = (quint64*)malloc(sizeof(quint64) * BUFFERSIZE);
**code in here which fill in the tripwire values in the array**
tripwire_buffer = clCreateBuffer(context,CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,sizeof(cl_ulong) * BUFFERSIZE,tripwires,&err);
cl_event *evt;
cl_int err = clEnqueueWriteBuffer(queue,tripwire_buffer,CL_TRUE,0,sizeof(cl_ulong) * BUFFERSIZE,tripwires,0,NULL,evt);


---

### 评论 #4 — ImperiousLeader (2024-06-12T01:05:04Z)

As previously noted this works with AMD GPUs with rocm-opencl 5.5.1 on Fedora 38/39+40, or on my second machine with NVidia 3080ti's and libOpenCL.so from NVidia (Ubuntu 23.04). 
Upgrading rocm-opencl to 5.7.1 or later results in a 75% slowdown and 6.0.2 causes a complete lock up / freeze. Downgrading to opencl-5.5.1 resolves the issue.

---

### 评论 #5 — harkgill-amd (2024-07-17T14:24:06Z)

Hi @ImperiousLeader, could you please provide a minimal reproducible example so we can try to reproduce this issue internally? 

---

### 评论 #6 — ImperiousLeader (2024-07-22T08:27:39Z)

Sure - what form would you like that to take... as in source code of an example program? Or intermediate output from the compile?
Ant

---

### 评论 #7 — harkgill-amd (2024-07-22T13:41:26Z)

Source code of an example program would be best.

---

### 评论 #8 — ImperiousLeader (2024-07-23T00:20:25Z)

[program.zip](https://github.com/user-attachments/files/16341081/program.zip)


---

### 评论 #9 — ImperiousLeader (2024-07-23T00:24:07Z)

Small program that shows the basics of the code. This was built in Qt-Creator 13.0.2 using Qt 6.7.2. GCC 14.1.1 20240701. The GPU OpenCL code is in compute.cpp
Novice programmer - so please do not laugh too hard at how simple things are.
Some things not included: Test values and 14Gb array of 64 bit test values - for obvious size reasons. Test values inserted into the arrays test as expected.
1.7 Trillion comparisons per second on 7900XTX and 1.2 Trillion on the 6900XT. Down to about a 1/4 of that under any version greater than 5.5.1, except for 6.0.2-2.FC40 which just results in an untidy crash.
Kernel also tested OK on 3080TIs using the CUDA SDK.

---

### 评论 #10 — ImperiousLeader (2024-07-28T08:43:31Z)

Updated to rocm-opencl-6.1.2-1.fc40. Ugly crash when running the kernel.... got this from journalctl --system -r

Jul 28 20:34:45 b550 kernel: ---[ end trace 0000000000000000 ]---
Jul 28 20:34:45 b550 kernel:  </TASK>
Jul 28 20:34:45 b550 kernel:  ret_from_fork_asm+0x1a/0x30
Jul 28 20:34:45 b550 kernel:  ? __pfx_kthread+0x10/0x10
Jul 28 20:34:45 b550 kernel:  ret_from_fork+0x34/0x50
Jul 28 20:34:45 b550 kernel:  ? __pfx_kthread+0x10/0x10
Jul 28 20:34:45 b550 kernel:  kthread+0xd2/0x100
Jul 28 20:34:45 b550 kernel:  ? __pfx_worker_thread+0x10/0x10
Jul 28 20:34:45 b550 kernel:  worker_thread+0x266/0x3a0
Jul 28 20:34:45 b550 kernel:  process_one_work+0x17e/0x340
Jul 28 20:34:45 b550 kernel:  pm_runtime_work+0x98/0xb0
Jul 28 20:34:45 b550 kernel:  ? __schedule+0x3fa/0x1710
Jul 28 20:34:45 b550 kernel:  rpm_suspend+0xe6/0x5f0
Jul 28 20:34:45 b550 kernel:  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
Jul 28 20:34:45 b550 kernel:  rpm_callback+0x55/0x60
Jul 28 20:34:45 b550 kernel:  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
Jul 28 20:34:45 b550 kernel:  __rpm_callback+0x44/0x170
Jul 28 20:34:45 b550 kernel:  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
Jul 28 20:34:45 b550 kernel:  pci_pm_runtime_suspend+0x6a/0x1a0
Jul 28 20:34:45 b550 kernel:  amdgpu_pmops_runtime_suspend+0xb9/0x190 [amdgpu]
Jul 28 20:34:45 b550 kernel:  amdgpu_device_suspend+0xcf/0x170 [amdgpu]
Jul 28 20:34:45 b550 kernel:  amdgpu_device_ip_suspend_phase2+0x144/0x5d0 [amdgpu]
Jul 28 20:34:45 b550 kernel:  smu_suspend+0x76/0xe0 [amdgpu]
Jul 28 20:34:45 b550 kernel:  smu_smc_hw_cleanup+0x6f/0x370 [amdgpu]
Jul 28 20:34:45 b550 kernel:  ? amdgpu_irq_put+0x46/0x70 [amdgpu]
Jul 28 20:34:45 b550 kernel:  ? asm_exc_invalid_op+0x1a/0x20
Jul 28 20:34:45 b550 kernel:  ? exc_invalid_op+0x17/0x70
Jul 28 20:34:45 b550 kernel:  ? handle_bug+0x3c/0x80
Jul 28 20:34:45 b550 kernel:  ? report_bug+0xff/0x140
Jul 28 20:34:45 b550 kernel:  ? amdgpu_irq_put+0x46/0x70 [amdgpu]
Jul 28 20:34:45 b550 kernel:  ? __warn.cold+0x8e/0xe8
Jul 28 20:34:45 b550 kernel:  ? amdgpu_irq_put+0x46/0x70 [amdgpu]
Jul 28 20:34:45 b550 kernel:  <TASK>
Jul 28 20:34:45 b550 kernel: Call Trace:
Jul 28 20:34:45 b550 kernel: PKRU: 55555554
Jul 28 20:34:45 b550 kernel: CR2: 00007f517b1ffcf8 CR3: 0000000369f10000 CR4: 0000000000f50ef0
Jul 28 20:34:45 b550 kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Jul 28 20:34:45 b550 kernel: FS:  0000000000000000(0000) GS:ffff92030ee80000(0000) knlGS:0000000000000000
Jul 28 20:34:45 b550 kernel: R13: ffff91f440880000 R14: 0000000000000003 R15: ffffffffc1233fd0
Jul 28 20:34:45 b550 kernel: R10: 0000000000000100 R11: 0000000000000000 R12: ffff91f440880000
Jul 28 20:34:45 b550 kernel: RBP: ffff91f40141a000 R08: 0000000000000001 R09: 0000000000000000
Jul 28 20:34:45 b550 kernel: RDX: 0000000000000000 RSI: ffff91f40141a008 RDI: ffff91f440880000
Jul 28 20:34:45 b550 kernel: RAX: ffff91f410608fe8 RBX: ffff91f40141a000 RCX: 0000000000000000
Jul 28 20:34:45 b550 kernel: RSP: 0018:ffffaef947bafc70 EFLAGS: 00010246
Jul 28 20:34:45 b550 kernel: Code: c0 74 33 48 8b 4e 10 48 83 39 00 74 29 89 d1 48 8d 04 88 8b 08 85 c9 74 11 f0 ff 08 74 07 31 c0 e9 fa c2 d1 f5 e9 1a fd ff ff <0f> 0b b8 ea ff ff ff e9 e9 c2 d1 f5 b8 ea ff ff ff e9 df c2 d1 f5
Jul 28 20:34:45 b550 kernel: RIP: 0010:amdgpu_irq_put+0x46/0x70 [amdgpu]
Jul 28 20:34:45 b550 kernel: Workqueue: pm pm_runtime_work
Jul 28 20:34:45 b550 kernel: Hardware name: ASUS System Product Name/TUF GAMING B550-PLUS (WI-FI), BIOS 3607 03/18/2024
Jul 28 20:34:45 b550 kernel: CPU: 25 PID: 5589 Comm: kworker/25:0 Not tainted 6.9.11-200.fc40.x86_64 #1
Jul 28 20:34:45 b550 kernel:  sha512_ssse3 nvme_core sha256_ssse3 ccp sha1_ssse3 cec sp5100_tco nvme_auth wmi ip6_tables ip_tables fuse
Jul 28 20:34:45 b550 kernel: Modules linked in: uinput snd_seq_dummy snd_hrtimer nf_conntrack_netbios_ns nf_conntrack_broadcast nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tabl>
Jul 28 20:34:45 b550 kernel: WARNING: CPU: 25 PID: 5589 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:630 amdgpu_irq_put+0x46/0x70 [amdgpu]
Jul 28 20:34:45 b550 kernel: ------------[ cut here ]------------


---

### 评论 #11 — ImperiousLeader (2024-07-28T08:50:09Z)

Downgraded to rocm-opencl-5.5.1-10 and rocm-opencl-devel-5.5.1-10.  Recompiled - running without error, at full speed.

---

### 评论 #12 — schung-amd (2024-07-29T20:45:12Z)

Hi @ImperiousLeader, thanks for the detailed issue report and version testing. I'll need some more information about your test data to reproduce the issue. 

- Are the values distributed in any specific way? 
- What is the range of values in your test data? 
- How many collisions do you observe between the test values and the array? 

Also, if you could provide the 15000 INT64 test values, that would be helpful. Thanks!

---

### 评论 #13 — ImperiousLeader (2024-07-30T03:48:44Z)

In the instance of the array of comparative values it is an even distribution.
For an 8 Gb Array of test values... there are 0x3FFFFFFF items in the array. unsigned long myArray[0x3FFFFFFF].
Starting from zero... increment each element of the array by 0x2000000080000002000000080000001FD755DC1C3340847844FC5DB2A, and take the first 64 bits.. so element 1 would equal 0x2000000080000002.
In the case of an 8Gb array of test values: 
myArray = (unsigned long*)malloc(sizeof(unsigned long) * 0x3FFFFFFF);
Fill the array as above, then that is copied to the GPU memory using
cl_mem t_buffer = clCreateBuffer(context,CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,sizeof(cl_ulong) * 0x3FFFFFFF,myArray,&err);
clEnqueueWriteBuffer(queue,t_buffer,CL_TRUE,0,sizeof(cl_ulong) * 0x3FFFFFFF,myArray,0,NULL,evt);

The kernel is invoked with the number of threads equalling the array dimension of 0x3FFFFFFF using:
clEnqueueNDRangeKernel(queue,myTestKernel,1,NULL,cl::NDRange(0x3FFFFFFF),NULL,0,NULL,NULL);


The test values are randomly distributed points - due to the nature of a 64 bit space collisions are rare (even at 15,000 odd total test values). Essentially... create 15,000 random unsigned long values - if any of those random 15,000 values matches a value in the array on the GPU you have a successful match.
Essentially:
unsigned long x;
srand(time(NULL));
for (int a =0; a < 15,000; a++) {
 x = rand(); x <<= 32; x |= rand();
 testPointArray[a] = x;
}
I can generate some sort of raw binary file of these values if you want - or is the generation process sufficient?

---

### 评论 #14 — ImperiousLeader (2024-07-30T03:56:09Z)

Appendum... if I do insert a known matching value from the 8GB array and randomly insert it into the testPointArray the code confirms a returned match as intended.

---

### 评论 #15 — schung-amd (2024-07-31T14:37:20Z)

Thanks, that should be enough detail to recreate your tests. Can you upload the image files you're using? Also, does the slowdown you're observing appear to scale with the number of collisions?

---

### 评论 #16 — ImperiousLeader (2024-08-01T01:12:51Z)

[resources.zip](https://github.com/user-attachments/files/16448481/resources.zip)

Apologies... attached. Thank you for looking into this issue :)
Collisions are rare - which is important as this test is mostly designed to thrash the GPU in terms of checking for total comparisons per second and also GPU temps / potential for throttling. Comparison/s per second is calculated as (testValues * memoryArrayDimension) / seconds to run kernel.
To answer your question :
No - there is no correlation to collisions. Upgrading from rocm-opencl-*-5.5.1 initially resulted in 1/4 of the speed. From version 6.x just a complete crash.


---

### 评论 #17 — schung-amd (2024-08-02T19:44:08Z)

Do you experience the same issue if you force the 7900XTX to use the 8Gb array instead of the 14Gb array?

---

### 评论 #18 — ImperiousLeader (2024-08-02T22:52:01Z)

So - upgraded to rocm-opencl-6.1.2-1. Forced lesser 8Gb array. 6900XT running at 1.12 Trillion comparisons / sec (basically correct). 7900XTX 1.3 Trillion - not 1.7 trillion comparisons. Avoided system crash from a user POV. Error from journalctl --system -r:

Aug 03 10:48:39 b550 kernel: ---[ end trace 0000000000000000 ]---
Aug 03 10:48:39 b550 kernel:  </TASK>
Aug 03 10:48:39 b550 kernel:  ret_from_fork_asm+0x1a/0x30
Aug 03 10:48:39 b550 kernel:  ? __pfx_kthread+0x10/0x10
Aug 03 10:48:39 b550 kernel:  ret_from_fork+0x34/0x50
Aug 03 10:48:39 b550 kernel:  ? __pfx_kthread+0x10/0x10
Aug 03 10:48:39 b550 kernel:  kthread+0xd2/0x100
Aug 03 10:48:39 b550 kernel:  ? __pfx_worker_thread+0x10/0x10
Aug 03 10:48:39 b550 kernel:  worker_thread+0x266/0x3a0
Aug 03 10:48:39 b550 kernel:  process_one_work+0x17e/0x340
Aug 03 10:48:39 b550 kernel:  pm_runtime_work+0x98/0xb0
Aug 03 10:48:39 b550 kernel:  ? __schedule+0x3fa/0x1710
Aug 03 10:48:39 b550 kernel:  rpm_suspend+0xe6/0x5f0
Aug 03 10:48:39 b550 kernel:  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
Aug 03 10:48:39 b550 kernel:  rpm_callback+0x55/0x60
Aug 03 10:48:39 b550 kernel:  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
Aug 03 10:48:39 b550 kernel:  __rpm_callback+0x44/0x170
Aug 03 10:48:39 b550 kernel:  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
Aug 03 10:48:39 b550 kernel:  pci_pm_runtime_suspend+0x6a/0x1a0
Aug 03 10:48:39 b550 kernel:  amdgpu_pmops_runtime_suspend+0xb9/0x190 [amdgpu]
Aug 03 10:48:39 b550 kernel:  amdgpu_device_suspend+0xcf/0x170 [amdgpu]
Aug 03 10:48:39 b550 kernel:  amdgpu_device_ip_suspend_phase2+0x144/0x5d0 [amdgpu]
Aug 03 10:48:39 b550 kernel:  smu_suspend+0x76/0xe0 [amdgpu]
Aug 03 10:48:39 b550 kernel:  smu_smc_hw_cleanup+0x6f/0x370 [amdgpu]
Aug 03 10:48:39 b550 kernel:  ? amdgpu_irq_put+0x46/0x70 [amdgpu]
Aug 03 10:48:39 b550 kernel:  ? asm_exc_invalid_op+0x1a/0x20
Aug 03 10:48:39 b550 kernel:  ? exc_invalid_op+0x17/0x70
Aug 03 10:48:39 b550 kernel:  ? handle_bug+0x3c/0x80
Aug 03 10:48:39 b550 kernel:  ? report_bug+0xff/0x140
Aug 03 10:48:39 b550 kernel:  ? amdgpu_irq_put+0x46/0x70 [amdgpu]
Aug 03 10:48:39 b550 kernel:  ? __warn.cold+0x8e/0xe8
Aug 03 10:48:39 b550 kernel:  ? amdgpu_irq_put+0x46/0x70 [amdgpu]
Aug 03 10:48:39 b550 kernel:  <TASK>
Aug 03 10:48:39 b550 kernel: Call Trace:
Aug 03 10:48:39 b550 kernel: PKRU: 55555554
Aug 03 10:48:39 b550 kernel: CR2: 00007f37242aa020 CR3: 000000015364c000 CR4: 0000000000f50ef0
Aug 03 10:48:39 b550 kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Aug 03 10:48:39 b550 kernel: FS:  0000000000000000(0000) GS:ffff8eb98e280000(0000) knlGS:0000000000000000
Aug 03 10:48:39 b550 kernel: R13: ffff8eaac2100000 R14: 0000000000000003 R15: ffffffffc1425fd0
Aug 03 10:48:39 b550 kernel: R10: ffffaea4056d5000 R11: ffffaea4056d5000 R12: ffff8eaac2100000
Aug 03 10:48:39 b550 kernel: RBP: ffff8eaa8dfc6000 R08: ffff8eaac2116f70 R09: 0000000000000000
Aug 03 10:48:39 b550 kernel: RDX: 0000000000000000 RSI: ffff8eaa8dfc6008 RDI: ffff8eaac2100000
Aug 03 10:48:39 b550 kernel: RAX: ffff8eaaa4c979d0 RBX: ffff8eaa8dfc6000 RCX: 0000000000000000
Aug 03 10:48:39 b550 kernel: RSP: 0018:ffffaea411c5fc70 EFLAGS: 00010246
Aug 03 10:48:39 b550 kernel: Code: c0 74 33 48 8b 4e 10 48 83 39 00 74 29 89 d1 48 8d 04 88 8b 08 85 c9 74 11 f0 ff 08 74 07 31 c0 e9 fa a2 b2 f6 e9 1a fd ff ff <0f> 0b b8 ea ff ff ff e9 e9 a2 b2 f6 b8 ea ff ff ff e9 df a2 b2 f6
Aug 03 10:48:39 b550 kernel: RIP: 0010:amdgpu_irq_put+0x46/0x70 [amdgpu]
Aug 03 10:48:39 b550 kernel: Workqueue: pm pm_runtime_work
Aug 03 10:48:39 b550 kernel: Hardware name: ASUS System Product Name/TUF GAMING B550-PLUS (WI-FI), BIOS 3607 03/18/2024
Aug 03 10:48:39 b550 kernel: CPU: 1 PID: 328217 Comm: kworker/1:1 Tainted: G        W          6.9.11-200.fc40.x86_64 #1
Aug 03 10:48:39 b550 kernel:  ghash_clmulni_intel sha512_ssse3 nvme_core sha256_ssse3 ccp cec sha1_ssse3 sp5100_tco nvme_auth wmi ip6_tables ip_tables fuse
Aug 03 10:48:39 b550 kernel: Modules linked in: uas usb_storage uinput snd_seq_dummy snd_hrtimer nf_conntrack_netbios_ns nf_conntrack_broadcast nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv>
Aug 03 10:48:39 b550 kernel: WARNING: CPU: 1 PID: 328217 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:630 amdgpu_irq_put+0x46/0x70 [amdgpu]
Aug 03 10:48:39 b550 kernel: ------------[ cut here ]------------


---

### 评论 #19 — ImperiousLeader (2024-08-02T22:53:59Z)

Restarting process with 14Gb array.... (prior to starting kernel):

Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: [drm] Cannot find any crtc or sizes
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring jpeg_dec uses VM inv eng 8 on hub 8
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring vcn_enc_1.1 uses VM inv eng 7 on hub 8
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring vcn_enc_1.0 uses VM inv eng 6 on hub 8
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring vcn_dec_1 uses VM inv eng 5 on hub 8
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring sdma3 uses VM inv eng 15 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring sdma2 uses VM inv eng 14 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Aug 03 10:52:23 b550 kernel: [drm] JPEG decode initialized successfully.
Aug 03 10:52:23 b550 kernel: [drm] VCN decode and encode initialized successfully(under DPG Mode).
Aug 03 10:52:23 b550 kernel: [drm] kiq ring mec 2 pipe 1 q 0
Aug 03 10:52:23 b550 kernel: [drm] DMUB hardware initialized: version=0x02020020
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: SMU is resumed successfully!
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: dpm has been enabled
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: SMU driver if version not matched
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: smu driver if version = 0x00000040, smu fw if version = 0x00000041, smu fw program = 0, version = 0x003a5a00 (58.90.0)
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: SMU is resuming...
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: reserve 0xa00000 from 0x83fd000000 for PSP TMR
Aug 03 10:52:23 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: PSP is resuming...
Aug 03 10:52:23 b550 kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008000000000).


---

### 评论 #20 — ImperiousLeader (2024-08-02T23:05:12Z)

14GB enabled - crash:

Aug 03 11:00:20 b550 kernel: [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <smu> failed -22
Aug 03 11:00:20 b550 kernel: amdgpu 0000:0a:00.0: amdgpu: Fail to disable thermal alert!
Aug 03 11:00:20 b550 kernel: ---[ end trace 0000000000000000 ]---
Aug 03 11:00:20 b550 kernel:  </TASK>
Aug 03 11:00:20 b550 kernel:  ret_from_fork_asm+0x1a/0x30
Aug 03 11:00:20 b550 kernel:  ? __pfx_kthread+0x10/0x10
Aug 03 11:00:20 b550 kernel:  ret_from_fork+0x34/0x50
Aug 03 11:00:20 b550 kernel:  ? __pfx_kthread+0x10/0x10
Aug 03 11:00:20 b550 kernel:  kthread+0xd2/0x100
Aug 03 11:00:20 b550 kernel:  ? __pfx_worker_thread+0x10/0x10
Aug 03 11:00:20 b550 kernel:  worker_thread+0x266/0x3a0
Aug 03 11:00:20 b550 kernel:  process_one_work+0x17e/0x340
Aug 03 11:00:20 b550 kernel:  pm_runtime_work+0x98/0xb0
Aug 03 11:00:20 b550 kernel:  ? add_timer_on+0xfa/0x1a0
Aug 03 11:00:20 b550 kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Aug 03 11:00:20 b550 kernel:  ? __schedule+0x3fa/0x1710
Aug 03 11:00:20 b550 kernel:  rpm_suspend+0xe6/0x5f0
Aug 03 11:00:20 b550 kernel:  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
Aug 03 11:00:20 b550 kernel:  rpm_callback+0x55/0x60
Aug 03 11:00:20 b550 kernel:  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
Aug 03 11:00:20 b550 kernel:  __rpm_callback+0x44/0x170
Aug 03 11:00:20 b550 kernel:  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
Aug 03 11:00:20 b550 kernel:  pci_pm_runtime_suspend+0x6a/0x1a0
Aug 03 11:00:20 b550 kernel:  amdgpu_pmops_runtime_suspend+0xb9/0x190 [amdgpu]
Aug 03 11:00:20 b550 kernel:  amdgpu_device_suspend+0xcf/0x170 [amdgpu]
Aug 03 11:00:20 b550 kernel:  amdgpu_device_ip_suspend_phase2+0x144/0x5d0 [amdgpu]
Aug 03 11:00:20 b550 kernel:  smu_suspend+0x76/0xe0 [amdgpu]
Aug 03 11:00:20 b550 kernel:  smu_smc_hw_cleanup+0x6f/0x370 [amdgpu]
Aug 03 11:00:20 b550 kernel:  ? amdgpu_irq_put+0x46/0x70 [amdgpu]
Aug 03 11:00:20 b550 kernel:  ? asm_exc_invalid_op+0x1a/0x20
Aug 03 11:00:20 b550 kernel:  ? exc_invalid_op+0x17/0x70
Aug 03 11:00:20 b550 kernel:  ? handle_bug+0x3c/0x80
Aug 03 11:00:20 b550 kernel:  ? report_bug+0xff/0x140
Aug 03 11:00:20 b550 kernel:  ? amdgpu_irq_put+0x46/0x70 [amdgpu]
Aug 03 11:00:20 b550 kernel:  ? __warn.cold+0x8e/0xe8
Aug 03 11:00:20 b550 kernel:  ? amdgpu_irq_put+0x46/0x70 [amdgpu]
Aug 03 11:00:20 b550 kernel:  <TASK>
Aug 03 11:00:20 b550 kernel: Call Trace:
Aug 03 11:00:20 b550 kernel: PKRU: 55555554
Aug 03 11:00:20 b550 kernel: CR2: 00007fbfe9c47000 CR3: 0000000729428000 CR4: 0000000000f50ef0
Aug 03 11:00:20 b550 kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Aug 03 11:00:20 b550 kernel: FS:  0000000000000000(0000) GS:ffff9cd6cee80000(0000) knlGS:0000000000000000
Aug 03 11:00:20 b550 kernel: R13: ffff9cc802600000 R14: 0000000000000003 R15: ffffffffc1d31fd0
Aug 03 11:00:20 b550 kernel: R10: ffffaabd85690000 R11: ffffaabd85690000 R12: ffff9cc802600000
Aug 03 11:00:20 b550 kernel: RBP: ffff9cc8026ae000 R08: ffff9cc802616f70 R09: 0000000000000000
Aug 03 11:00:20 b550 kernel: RDX: 0000000000000000 RSI: ffff9cc8026ae008 RDI: ffff9cc802600000
Aug 03 11:00:20 b550 kernel: RAX: ffff9cc7d43d4450 RBX: ffff9cc8026ae000 RCX: 0000000000000000
Aug 03 11:00:20 b550 kernel: RSP: 0018:ffffaabd80affc70 EFLAGS: 00010246
Aug 03 11:00:20 b550 kernel: Code: c0 74 33 48 8b 4e 10 48 83 39 00 74 29 89 d1 48 8d 04 88 8b 08 85 c9 74 11 f0 ff 08 74 07 31 c0 e9 fa 72 a1 d9 e9 1a fd ff ff <0f> 0b b8 ea ff ff ff e9 e9 72 a1 d9 b8 ea ff ff ff e9 df 72 a1 d9
Aug 03 11:00:20 b550 kernel: RIP: 0010:amdgpu_irq_put+0x46/0x70 [amdgpu]
Aug 03 11:00:20 b550 kernel: Workqueue: pm pm_runtime_work
Aug 03 11:00:20 b550 kernel: Hardware name: ASUS System Product Name/TUF GAMING B550-PLUS (WI-FI), BIOS 3607 03/18/2024
Aug 03 11:00:20 b550 kernel: CPU: 25 PID: 275 Comm: kworker/25:1 Not tainted 6.9.12-200.fc40.x86_64 #1
Aug 03 11:00:20 b550 kernel:  sha512_ssse3 nvme_core sha256_ssse3 ccp sha1_ssse3 cec sp5100_tco nvme_auth wmi ip6_tables ip_tables fuse
Aug 03 11:00:20 b550 kernel: Modules linked in: uinput snd_seq_dummy snd_hrtimer nf_conntrack_netbios_ns nf_conntrack_broadcast nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tabl>
Aug 03 11:00:20 b550 kernel: WARNING: CPU: 25 PID: 275 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:630 amdgpu_irq_put+0x46/0x70 [amdgpu]
Aug 03 11:00:20 b550 kernel: ------------[ cut here ]------------


---

### 评论 #21 — ImperiousLeader (2024-08-02T23:13:33Z)

As a precaution, ran the kernel on the 6900XT only using rocm-6.1.2-1.fc40..... It starts but speed drops from 1.2 Trillion comparisons / second to 331 billion... so 1/4 speed. No new errors showing in the system journal.

Running the kernel only on the 7900XTX = immediate desktop environment crash (rocm-6.1.2-1.fc40). I am using GNOME Wayland - just as an aside.

Downgraded to 5.5.1... running normally again. Rebooted and no system journal errors reported. I did think at one point the system log amdgpu error was showing with opencl-5.5.1 as well however made a woopsie there (so you might see I have edited prior comments) - I hadn't actually rebooted.
From what I can see at the moment, with 5.5.1 there are no journal errors reported and running at 1.75 / 1.21 trillion comparisons for the 7900XTX and 6900XT respectively. 
Once rocm-opencl is upgraded to 6.x the journal errors appear and the 7900XTX crashes - being the primary GPU - that also equals system crash out of the desktop.

Edit: No kernel / journal errors running for the last two hours with both GPUs running concurrently and continuously. rocm-opencl ver 5.5.1 with kernel 6.9.12-200.fc40.x86_64 #1 SMP PREEMPT_DYNAMIC Sat Jul 27 15:56:15 UTC 2024 x86_64 GNU/Linux... so now reconfirmed that the journal errors only occur with the later versions of rocm-opencl.

---

### 评论 #22 — schung-amd (2024-08-06T20:43:05Z)

Thanks for the detailed investigation! I have your code running without issue on ROCm 6.2, so try that if possible. I'll be working to see if I can reproduce your issues on previous ROCm versions. 

In general, there are a lot of moving parts in your application, so it is difficult to isolate which parts may be causing a slowdown, but I suspect the root cause is somewhere in the memory allocation, transfer, and cleanup. The timestamp captures these in addition to the actual kernel work, which adds significant overhead. For example, with all of the memory transfers I get around 800 billion comparisons/sec with your metric using an 8G array, but removing the initialization, transfer, and cleanup of `cnt` and `d_CNT` and hardcoding the loop bounds gives me 2 trillion comparisons per second with an 8G array. This indicates that the slowdown you're seeing is likely due to overhead such as memory transfer and logging, and that the 75% slowdown is not actually a 75% reduction in compute.

As mentioned I'll be rolling back ROCm versions to see if I can reproduce the crashes you're observing in ROCm 6.0 and 6.1 as well as the performance differences in older versions, but I suspect any issue will be related to memory transfer.

---

### 评论 #23 — schung-amd (2024-08-07T20:46:51Z)

I was able to run the simple kernel without crashing on ROCm 6.1.0, 6.1.1, 6.1.2, 6.1.3, and 6.2, with both 8G and 14G arrays and with or without the removal of `cnt` with negligible performance differences between the versions. Notably, I also removed the `evt` pointer as it was not being used and QtCreator was complaining (rightfully) about it not being initialized. I am also using Qt5 and not Qt6, although I'm not sure if that makes a difference, and I am testing in Ubuntu 22.04.

I was also able to run it on ROCm 5.7.1 where I did see some performance degradation as you have observed. However, I would like to note that ROCm 5.7.1 does not support the 7900XTX, so this is not necessarily expected to function well.

In order to determine what's causing your crashes, I first suggest trying the newly released ROCm 6.2. Then, if you also crash there, please provide a more minimal reproduction of the issue (i.e. not in a Qt GUI). While the kernel itself is simple, it is currently tangled with a lot of other moving parts and it would be good to be able to isolate the problem better.

---

### 评论 #24 — ImperiousLeader (2024-08-08T03:31:39Z)

OK - as soon as 6.2 comes out in the Fedora repos I will give it a go and report back ! 

---

### 评论 #25 — ImperiousLeader (2024-08-08T05:19:51Z)

Picking up on your work and investigation I have done the following:
Change the kernel to be:
    __kernel void Value_Search(global unsigned long *trip, global unsigned int *cnt, global unsigned long *mValue) {
      unsigned int i = get_global_id(0);
      unsigned long b;
      for (unsigned long a = 0; a < 10000; a++) {
        b =  *mValue;
        b += a;
        if (b == trip[i]) {
          *cnt = i;
        }
      }
    }

So no arrays are transferred at invocation. The huge array copied t the device one when the application starts (and is unloaded/freed on closing it). With this kernel during any particular loop a pointer to the huge array is passed along with an unsigned int and unsigned long global variables.
There is a 10,000 repetition loop to ensure the GPU is running for long enough to see true speed.
The Comparisons calculation is thus: Huge array size * 10000 / second. 
 The kernel is invoked as thus:

    cl_uint cnt = 0;
    cl_mem d_CNT = clCreateBuffer(context,CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR,sizeof(cl_uint),&cnt,&err);
    if (err != CL_SUCCESS) { consoleMsg("gpuRun(): clCreateBuffer(5) failed: " + getCLErrorString(err)); deviceStatus = "ERROR"; }

    cl_ulong test = 0x6347634672446234;
    if (endTest) test = (cl_ulong)testValue;

    cl_mem d_TEST = clCreateBuffer(context,CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR,sizeof(cl_ulong),&test,&err);
    if (err != CL_SUCCESS) { consoleMsg("gpuRun(): clCreateBuffer(5) failed: " + getCLErrorString(err)); deviceStatus = "ERROR"; }


    err = clSetKernelArg(kernelCompute,0,sizeof(cl_mem),&tripwire_buffer);
    if (err != CL_SUCCESS) { consoleMsg("gpuRun(): clCreateBuffer(0) failed: " + getCLErrorString(err)); deviceStatus = "ERROR"; }
    err = clSetKernelArg(kernelCompute,1,sizeof(cl_mem),&d_CNT);
    if (err != CL_SUCCESS) { consoleMsg("gpuRun(): clCreateBuffer(5) failed: " + getCLErrorString(err)); deviceStatus = "ERROR"; }
    err = clSetKernelArg(kernelCompute,2,sizeof(cl_mem),&d_TEST);
    if (err != CL_SUCCESS) { consoleMsg("gpuRun(): clCreateBuffer(5) failed: " + getCLErrorString(err)); deviceStatus = "ERROR"; }

    err = clEnqueueNDRangeKernel(queue,kernelCompute,1,NULL,cl::NDRange(BUFFERSIZE),NULL,0,NULL,NULL);
    if (err != CL_SUCCESS) { consoleMsg("gpuRun(): clEnqueueNDRangeKernel() failed : " + getCLErrorString(err)); deviceStatus = "ERROR"; }
    err = clFinish(queue);
    if (err != CL_SUCCESS) { consoleMsg("gpuRun(): clFinish() failed : " + getCLErrorString(err)); deviceStatus = "ERROR"; }

    err = clEnqueueReadBuffer(queue,d_CNT,CL_TRUE,0,sizeof(cl_uint),&cnt,0,NULL,NULL);
    if (err != CL_SUCCESS) { consoleMsg("gpuRun(): clEnqueueReadBuffer(2) failed : " + getCLErrorString(err)); deviceStatus = "ERROR"; }
    if (cnt > 0) {
        consoleMsg("Array size: " + QString::number(BUFFERSIZE,16));
        consoleMsg(deviceName + " result: " + QString::number(cnt) + " ********** SUCCESS *************");
        gotResult = true;
    } else {
        consoleMsg(deviceName + " result: " + QString::number(cnt));
    }

    clReleaseMemObject(d_CNT);
    clReleaseMemObject(d_TEST);

On the 6th loop the flag endTest is switched to true and the test value is set (this is equal to hugearray[1024])


---

### 评论 #26 — ImperiousLeader (2024-08-08T05:21:19Z)

Hopefully this is less convoluted. My results:

Kernel
// ===============================================================================================================================================================
// The OpenCL kernel that is run on the GPU / Compute device.
// ===============================================================================================================================================================
    __kernel void Value_Search(global unsigned long *trip, global unsigned int *cnt, global unsigned long *mValue) {
      unsigned int i = get_global_id(0);
      unsigned long b;
      for (unsigned long a = 0; a < 10000; a++) {
        b =  *mValue;
        b += a;
        if (b == trip[i]) {
          *cnt = i;
        }
      }
    }

=====================================================================================================================================
[08 Gb Array, rocm-opencl-6.1.2-1]

AMD Radeon RX 7900 XTX Loading tripwires: 08G
Test value 1024 is : feeaac3bc2fb6dd0
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 361.55 Billion in 29698 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.25 Trillion in 1719 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.25 Trillion in 1719 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.25 Trillion in 1717 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.27 Trillion in 1712 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.27 Trillion in 1712 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.26 Trillion in 1716 msecs
Array size: 3fffffff
AMD Radeon RX 7900 XTX result: 1024 ********** SUCCESS *************
AMD Radeon RX 7900 XTX KPS : 6.25 Trillion in 1717 msecs

AMD Radeon RX 6900 XT Loading tripwires: 08G
Test value 1024 is : feeaac3bc2fb6dd0
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 417.98 Billion in 25689 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.34 Trillion in 2474 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.33 Trillion in 2478 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.33 Trillion in 2478 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.33 Trillion in 2478 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.33 Trillion in 2478 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.33 Trillion in 2478 msecs
Array size: 3fffffff
AMD Radeon RX 6900 XT result: 1024 ********** SUCCESS *************
AMD Radeon RX 6900 XT KPS : 4.33 Trillion in 2478 msecs

=====================================================================================================================================
[14 Gb Array, rocm-opencl-6.1.2-1]

AMD Radeon RX 7900 XTX Loading tripwires: 14G
Test value 1024 is : ade73ab905b843a9
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 206.84 Billion in 51912 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 2.00 Trillion in 8470 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 2.00 Trillion in 8473 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 1.99 Trillion in 8479 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 2.00 Trillion in 8463 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 1.99 Trillion in 8479 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 1.99 Trillion in 8478 msecs
Array size: 64cccccb
AMD Radeon RX 7900 XTX result: 1024 ********** SUCCESS *************
AMD Radeon RX 7900 XTX KPS : 2.00 Trillion in 8471 msecs

AMD Radeon RX 6900 XT Loading tripwires: 14G
Test value 1024 is : ade73ab905b843a9
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 219.85 Billion in 48840 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 1.36 Trillion in 12429 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 1.36 Trillion in 12427 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 1.36 Trillion in 12429 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 1.36 Trillion in 12430 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 1.36 Trillion in 12428 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 1.36 Trillion in 12454 msecs
Array size: 64cccccb
AMD Radeon RX 6900 XT result: 1024 ********** SUCCESS *************
AMD Radeon RX 6900 XT KPS : 1.36 Trillion in 12454 msecs

=====================================================================================================================================
[08 Gb Array, rocm-opencl-5.5.1-10]

AMD Radeon RX 7900 XTX Loading tripwires: 08G
Test value 1024 is : feeaac3bc2fb6dd0
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 313.90 Billion in 34207 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.91 Trillion in 1554 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.92 Trillion in 1551 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.92 Trillion in 1551 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.91 Trillion in 1553 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.91 Trillion in 1554 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.91 Trillion in 1553 msecs
Array size: 3fffffff
AMD Radeon RX 7900 XTX result: 1024 ********** SUCCESS *************
AMD Radeon RX 7900 XTX KPS : 6.91 Trillion in 1554 msecs

AMD Radeon RX 6900 XT Loading tripwires: 08G
Test value 1024 is : feeaac3bc2fb6dd0
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 355.70 Billion in 30187 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.80 Trillion in 2235 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.80 Trillion in 2236 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.80 Trillion in 2237 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.80 Trillion in 2237 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.80 Trillion in 2237 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.80 Trillion in 2238 msecs
Array size: 3fffffff
AMD Radeon RX 6900 XT result: 1024 ********** SUCCESS *************
AMD Radeon RX 6900 XT KPS : 4.80 Trillion in 2238 msecs

=====================================================================================================================================
[14 Gb Array, rocm-opencl-5.5.1-10]

AMD Radeon RX 7900 XTX Loading tripwires: 14G
Test value 1024 is : ade73ab905b843a9
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 200.80 Billion in 53474 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.96 Trillion in 2431 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.96 Trillion in 2431 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.96 Trillion in 2431 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.96 Trillion in 2429 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.96 Trillion in 2429 msecs
AMD Radeon RX 7900 XTX result: 0
AMD Radeon RX 7900 XTX KPS : 6.96 Trillion in 2429 msecs
Array size: 64cccccb
AMD Radeon RX 7900 XTX result: 1024 ********** SUCCESS *************
AMD Radeon RX 7900 XTX KPS : 6.96 Trillion in 2429 msecs

AMD Radeon RX 6900 XT Loading tripwires: 14G
Test value 1024 is : ade73ab905b843a9
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 227.80 Billion in 47136 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.80 Trillion in 3521 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.80 Trillion in 3524 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.80 Trillion in 3526 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.80 Trillion in 3526 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.79 Trillion in 3527 msecs
AMD Radeon RX 6900 XT result: 0
AMD Radeon RX 6900 XT KPS : 4.79 Trillion in 3528 msecs
Array size: 64cccccb
AMD Radeon RX 6900 XT result: 1024 ********** SUCCESS *************
AMD Radeon RX 6900 XT KPS : 4.79 Trillion in 3529 msecs

---

### 评论 #27 — ImperiousLeader (2024-08-08T05:28:35Z)

So with the 8Gb array loaded this kernel runs at the same speed using rocm-opencl 5.5.1-10 or 6.1.2-1
Switching to the 14Gb immediately shows the difference with both GPUs slowing down dramatically.

GPU            Array     OpenCl       Comparisons / sec
6900XT        8 Gb     5.5.1-10      4.8 Trillion
7900XTX      8 Gb     5.5.1-10      6.9 Trillion
6900XT        8 Gb     6.1.2-1         4.3 Trillion
7900XTX      8 Gb     6.1.2-1         6.2 Trillion

6900XT        14 Gb    5.5.1-10     4.8 Trillion
7900XTX      14 Gb    5.5.1-10     6.9 Trillion
6900XT        14 Gb    6.1.2-1        1.3 Trillion
7900XTX      14 Gb    6.1.2-1        2.0 Trillion


---

### 评论 #28 — ImperiousLeader (2024-08-08T05:31:31Z)

Oh and these kernels did not crash :) Does this much simpler kernel info help at all... clearly showing an issue with speed of memory access for the large array as far as I can see - affecting both the 6900XT and 7900XTX. The test output data was run with each GPU running alone - not concurrently to ensure that wasn't an issue as well.

---

### 评论 #29 — schung-amd (2024-08-08T13:42:59Z)

I'm not sure I understand the KPS metric. I understand the denominator is the time elapsed, but I would expect the numerator to be the number of comparisons, which should be constant for the same array size. Does the numerator represent something else here?

---

### 评论 #30 — ImperiousLeader (2024-08-09T00:44:37Z)

> I'm not sure I understand the KPS metric. I understand the denominator is the time elapsed, but I would expect the numerator to be the number of comparisons, which should be constant for the same array size. Does the numerator represent something else here?

Sorry for not being clear. If the kernel was asking each core to only do one operation it would be true that the Comparisons per second (KPS) would equal the number of elements in the array/time. In the second kernel from the other day each thread does a value add 10,000 times over and compares that against memory... so effectively in terms of comparisons it is <Array Size> * 10,000 / time.
The end goal is to get the total number of times per second the GPU is asked <does this 64 bit value == A 64 bit value in the huge array> and divide that by time to give a per second result.

---

### 评论 #31 — schung-amd (2024-08-09T13:37:22Z)

Ah, I see now that the first number is your rate calculation and not just the total number of comparisons. I'm curious as to where this breaks; you're seeing a performance degradation somewhere between 8G and 14G, but how big can you make the array before performance drops off? I haven't been able to reproduce your issue, so hopefully there's a clue we can find there.

---

### 评论 #32 — ImperiousLeader (2024-08-29T08:42:35Z)

Sorry for the delay - have been away. I thought I might have discovered the source of the bug - but alas no. Will reply next week re: different array sizes. I have made some changes to the setup code, relying exclusively on clCreateBuffer with flags CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR - and this is working for Nvidia cards (using cuda libraries) and AMD with rocm-opencl 5.5.1. I have verified the array loads to GPU  memory correctly. With the new arrangement rocm-opencl 6.x crashes horribly on AMD cards. Will upload when I can. AMD array sizes currently 13 and 20 Gb respectively for 6900XT and 7900XTX.

---

### 评论 #33 — ImperiousLeader (2024-09-09T23:38:54Z)

I am going a little nutty at this end. Attached is a small test linux console program to test performance. Arrrgh... some things solved, some new things revealed.
[AMD_GPU_PERFORMANCE.zip](https://github.com/user-attachments/files/16937567/AMD_GPU_PERFORMANCE.zip)

Using this little app I am NOT getting any slow down.... which infers something is screwy when compiling the GUI in QtCreator .... so:
1. For arrays of <= 16Gb in size, with the latest rocm I am getting 2 Trillion comparisons per second for the 7900XTX and 1.47 Trillion for the 6900XT - noticeably FASTER than the same code inside a GUI compilation which is bizarre.
2. Arrays greater than 16 Gb (only applies to the 7900XTX) but less than the 20Gb MAX_ALLOC limit I get "Memory access fault by GPU node-1 (Agent handle: 0x3d34c350) on address 0x7f362e60a000. Reason: Page not present or supervisor privilege."
3. For arrays greater than the MAX_ALLOC I get an expected error when attempting to cl_createBuffer()... which does not occur in the QtCreator GUI compilation/debug run. Weird.

So now the current bug to work out is why arrays between 16b and 20Gb (the ALLOC_MAX for the 7900XTX) cause the memory fault when the kernel is running.
In the meantime I am going to have to look at how QtCreator is somehow screwing something up in the background. Grrrrr. I am working on the theory it is something in the GCC compilation arguments or similar in the CMakelist.user file which is not used by the console app.

---

### 评论 #34 — ImperiousLeader (2024-09-09T23:40:58Z)

![Screenshot from 2024-09-10 11-40-41](https://github.com/user-attachments/assets/6671749f-7443-42d8-aa8f-d84c524a49f3)


---

### 评论 #35 — ImperiousLeader (2024-09-09T23:43:57Z)

![Screenshot from 2024-09-10 11-42-30](https://github.com/user-attachments/assets/e771ebac-00de-4610-9c9e-b26b8a702b45)


---

### 评论 #36 — schung-amd (2024-09-10T16:06:01Z)

Hi @ImperiousLeader, thanks for following up. I was able to reproduce your new issue on ROCm 6.2 with >16Gb arrays after changing the include `opencl.hpp` to `cl2.hpp` as that's what is packaged with ROCm. After some debugging I noticed the segfault occurs when the global id is 2^22, and I think your issue is just related to overflowing data types. In your kernel, changing `int idx = get_global_id(0);` to `unsigned int idx = get_global_id(0);` gets rid of the segfault all the way up to 20Gb.

---

### 评论 #37 — ImperiousLeader (2024-09-10T18:19:28Z)

Hah! Now that is an embarrassing noob error - good spotting. Thank you :)
I am away for the next 45 days - so can not work on the Qt/OpenCL slow down question for a while.
when I am back - will work up some most basic programs and see where the wheels fall off. Currently sitting about 1/2 expected speed with latest kernel and rocm in the Qt GUI compiled programs. The info re: cl2.hpp is very helpful - will switch to those to ensure I have not missed something there despite documentation saying everything is backwards compatible. 
Sideline: Interesting can allocate and access 22Gb arrays (greater than the max_alloc limit) without error/warning using opencl.hpp... I wonder if that is an accidental win.

---

### 评论 #38 — schung-amd (2024-09-10T18:25:22Z)

I think the header files should be interchangeable, was just noting a difference in our configurations; but wouldn't hurt to check. Are you still crashing on ROCm 6.0 and later, or was that in QtCreator only?

---

### 评论 #39 — ImperiousLeader (2024-09-10T20:47:17Z)

The last test I did had a 16gb array, which was running at 1.2 trillion comparisons / sec (vs console test app 2 trillion). When using a 22gb array it crashes but that will most likely be secondary to being greater than the MAX_ALLOC limit as cl_createBuffer does not panic at oversize buffers when compiling in qtcreator with gcc. A 22gb array does fail to compile outside of qtcreator with the appropriate warning about an invalid buffer size.
So I need to work out why the qt GUI is so much slower... this will take a little more testing on my side.... build a basic gui version of the console app, and work up from there to see what happens and when.

Ant

Get Outlook for Android<https://aka.ms/AAb9ysg>
________________________________
From: schung-amd ***@***.***>
Sent: Wednesday, September 11, 2024 6:25:44 AM
To: ROCm/ROCm ***@***.***>
Cc: ImperiousLeader ***@***.***>; Mention ***@***.***>
Subject: Re: [ROCm/ROCm] [Issue]: INT64 _very_slow with rocm-opencl versions >= 5.5.7 on Fedora (39 + 40) (Issue #3273)


I think the header files should be interchangeable, was just noting a difference in our configurations; but wouldn't hurt to check. Are you still crashing on ROCm 6.0 and later, or was that in QtCreator only?

—
Reply to this email directly, view it on GitHub<https://github.com/ROCm/ROCm/issues/3273#issuecomment-2341718768>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/AZ7JYDG55WOATK42ZVHCQQ3ZV42SRAVCNFSM6AAAAABJBLU2DGVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGNBRG4YTQNZWHA>.
You are receiving this because you were mentioned.Message ID: ***@***.***>


---

### 评论 #40 — schung-amd (2024-09-10T20:52:36Z)

If you're not crashing with normal loads (i.e. not beyond the MAX_ALLOC limit), this seems like an issue with QtCreator configuration rather than with the ROCm stack. I suggest we close this issue, and we can revisit this when you are able to pin down what's going on with QtCreator.

---

### 评论 #41 — ImperiousLeader (2024-09-11T01:53:54Z)

Sounds logical. Thanks.
Ant

Get Outlook for Android<https://aka.ms/AAb9ysg>
________________________________
From: schung-amd ***@***.***>
Sent: Wednesday, September 11, 2024 8:52:57 AM
To: ROCm/ROCm ***@***.***>
Cc: ImperiousLeader ***@***.***>; Mention ***@***.***>
Subject: Re: [ROCm/ROCm] [Issue]: INT64 _very_slow with rocm-opencl versions >= 5.5.7 on Fedora (39 + 40) (Issue #3273)


If you're not crashing with normal loads (i.e. not beyond the MAX_ALLOC limit), this seems like an issue with QtCreator configuration rather than with the ROCm stack. I suggest we close this issue, and we can revisit this when you are able to pin down what's going on with QtCreator.

—
Reply to this email directly, view it on GitHub<https://github.com/ROCm/ROCm/issues/3273#issuecomment-2341990202>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/AZ7JYDDSKKKALY3KDQISCITZV5L2TAVCNFSM6AAAAABJBLU2DGVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDGNBRHE4TAMRQGI>.
You are receiving this because you were mentioned.Message ID: ***@***.***>


---

### 评论 #42 — schung-amd (2024-09-11T13:18:28Z)

Feel free to reopen this or submit a new issue when you're able to work on it again. Thanks!

---

### 评论 #43 — ImperiousLeader (2024-09-12T03:31:06Z)

*EDIT*
Found the issue - not 100% where the fix will be yet - and it is platform independent (same results on an NVidia 3080ti) - so the issue is with my programming or OpenCL.
This kernel works correctly - full speed:
__kernel void TEST_KERNEL(global unsigned long *bigArray,global unsigned long *testValues, global unsigned int *cnt, global unsigned int *testMatch, global unsigned int *arrayMatch) {
      unsigned int idx = get_global_id(0);
      for (unsigned int i = 0; i < 10000; i++) {
        if (bigArray[idx] == testValues[i]) {
          testMatch[*cnt] = i;
          arrayMatch[*cnt] = idx;
          atomic_inc(cnt);
        }
      }
    }

HOWEVER if change the for loop to read: for (unsigned int i = 0; i < *mCnt; i++) and add that variable to the kernel declaration the performance halves. Your thoughts... is this another basic programming error on my behalf, or is this something odd in the compiler?

---

### 评论 #44 — ImperiousLeader (2024-09-12T03:32:40Z)

BAD Kernel: 
__kernel void TEST_KERNEL(global unsigned long *bigArray,global unsigned long *testValues, global unsigned int *cnt, global unsigned int *testMatch, global unsigned int *arrayMatch, constant unsigned int *mCnt) {
unsigned int idx = get_global_id(0);
for (unsigned int i = 0; i < *mCnt; i++) {
if (bigArray[idx] == testValues[i]) {
testMatch[*cnt] = i;
arrayMatch[*cnt] = idx;
atomic_inc(cnt);
}
}
}

---

### 评论 #45 — schung-amd (2024-09-13T20:55:44Z)

My initial thoughts are that the compiler can make some optimizations with a known loop size, whereas mCnt is not known at compile time so these would be impossible. I don't know what goes on under the hood for OpenCL specifically, but this might include, for example, loop unrolling. Also, feeding the loop bounds in from mCnt is going to incur some additional overhead. If you're interested in optimizing this, I recommend profiling your code to see where most of the time is being spent and how the memory is being used; this would inform how you structure your data and computation in order to make the best use of your hardware. I also suggest using HIP over OpenCL, as in my opinion it is more modern and easier to use, but that's neither here nor there.

---
