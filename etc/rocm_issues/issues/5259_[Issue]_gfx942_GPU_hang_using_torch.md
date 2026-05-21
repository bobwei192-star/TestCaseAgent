# [Issue]: gfx942 GPU hang using torch

> **Issue #5259**
> **状态**: closed
> **创建时间**: 2025-09-05T14:35:12Z
> **更新时间**: 2025-10-22T21:01:26Z
> **关闭时间**: 2025-10-22T21:01:25Z
> **作者**: diegolmoreno
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5259

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- tcgu-amd

## 描述

### Problem Description

During a PyTorch run a user is hitting a GPU Hang. After a few hours the node ends up crashing without generating any crashdump.

The application would fail with these messages (GPU Hang):

```
Loss/train_mean_inlier_rep_error: 4.7540 (4.7279) | Grad/pos_proj: 1.0838 (1.5358) | Grad/point_encoder: 0.0000 (0.0000) | Grad/point_decoder: 7.3522 (6.8609) | Grad/point: 65.9949 (74.0430) | Grad/conf_decoder: 0.0125 (0.0336) | Grad/conf_head: 0.1573 (1.1025) | Grad/decoder: 0.8831 (1.3174) | Grad/register_token,query_token: 0.0038 (0.0064)
HW Exception by GPU node-4 (Agent handle: 0x1ebc04e0) reason :GPU Hang
HW Exception by GPU node-4 (Agent handle: 0x2df30600) reason :GPU Hang
HW Exception by GPU node-4 (Agent handle: 0x33c245e0) reason :GPU Hang
HW Exception by GPU node-4 (Agent handle: 0x462ca2e0) reason :GPU Hang
W0902 15:10:48.626000 819010 torch/distributed/elastic/multiprocessing/api.py:900] Sending process 819027 closing signal SIGTERM
W0902 15:10:48.632000 819010 torch/distributed/elastic/multiprocessing/api.py:900] Sending process 819028 closing signal SIGTERM
E0902 15:10:49.013000 819010 torch/distributed/elastic/multiprocessing/api.py:874] failed (exitcode: -6) local_rank: 0 (pid: 819025) of binary: <masked_by_issue_reporter>/bin/python
Traceback (most recent call last):
```

On syslog we can see how the driver had indeed a fatal bug:

```
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.434750] [drm:gfx_v9_4_3_priv_reg_irq [amdgpu]] *ERROR* Illegal register access in command stream
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.446310] [drm:gfx_v9_4_3_priv_reg_irq [amdgpu]] *ERROR* Illegal register access in command stream
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.457623] [drm:gfx_v9_4_3_priv_reg_irq [amdgpu]] *ERROR* Illegal register access in command stream
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.468889] [drm:gfx_v9_4_3_priv_reg_irq [amdgpu]] *ERROR* Illegal register access in command stream
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.480141] [drm:gfx_v9_4_3_priv_reg_irq [amdgpu]] *ERROR* Illegal register access in command stream
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.491372] ------------[ cut here ]------------
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.491376] Bug: No PASID in KFD interrupt
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.491441] WARNING: CPU: 18 PID: 0 at /tmp/amd.F7CEdP4i/amd/amdgpu/../amdkfd/kfd_int_process_v9.c:324 event_interrupt_isr_v9+0x2e0/0x2f0 [amdgpu]
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.491776] Modules linked in: mgc(OE) lustre(OE) mdc(OE) fid(OE) lov(OE) osc(OE) lmv(OE) fld(OE) ptlrpc(OE) obdclass(OE) ksocklnd(OE) overlay nfsv3 nfs_acl nfs lockd grace fscache netfs lnet(OE) libcfs(OE) nvme_fabrics uio_pci_generic uio cuse rdma_ucm(OE) rdma_cm(OE) iw_cm(OE) ib_ipoib(OE) ib_cm(OE) ib_umad(OE) sunrpc binfmt_misc xfs libcrc32c intel_rapl_msr intel_rapl_common edac_mce_amd kvm_amd ccp kvm crct10dif_pclmul crc32_pclmul ghash_clmulni_intel sha256_ssse3 sha1_ssse3 aesni_intel crypto_simd cryptd rapl mlx5_ib(OE) ib_uverbs(OE) wmi_bmof amdgpu(OE) ast amddrm_ttm_helper(OE) drm_vram_helper amdttm(OE) ipmi_ssif amdxcp(OE) drm_ttm_helper amddrm_buddy(OE) amd_sched(OE) ttm mlx5_core(OE) amdkcl(OE) nvme mlxdevm(OE) mlxfw(OE) drm_kms_helper psample nvme_core tls pci_hyperv_intf cec rc_core i2c_algo_bit bnxt_en fb_sys_fops syscopyarea sysfillrect sysimgblt ib_core(OE) xhci_pci mlx_compat(OE) i2c_piix4 xhci_pci_renesas wmi acpi_ipmi ipmi_si ipmi_devintf ipmi_msghandler mac_hid
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.491959]  sch_fq_codel knem(OE) efi_pstore drm ip_tables x_tables autofs4
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.491976] CPU: 18 PID: 0 Comm: swapper/18 Kdump: loaded Tainted: P           OE     5.15.0-152-generic #162-Ubuntu
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.491984] Hardware name: Giga Computing G383-R80-AAP1-000/MR83-AC0-000, BIOS F13 02/19/2025
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.491987] RIP: 0010:event_interrupt_isr_v9+0x2e0/0x2f0 [amdgpu]
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492273] Code: e3 bd 00 3c 01 0f 87 87 2c 65 00 83 e0 01 0f 85 7c fe ff ff 48 c7 c7 e8 1f 6d c2 88 45 d4 c6 05 ac e3 bd 00 01 e8 d7 e1 6d e6 <0f> 0b 0f b6 45 d4 e9 5d fe ff ff 0f 1f 44 00 00 0f 1f 44 00 00 55
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492278] RSP: 0018:ffff9c188ccc0d08 EFLAGS: 00010086
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492284] RAX: 0000000000000000 RBX: 0000000000000014 RCX: 0000000000000027
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492287] RDX: ffff8fb3906a0588 RSI: 0000000000000001 RDI: ffff8fb3906a0580
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492290] RBP: ffff9c188ccc0d38 R08: 0000000000000003 R09: ffff9c188ccc0ca0
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492293] R10: 000000000000001f R11: 0000000000000001 R12: ffff9c18a2338de0
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492296] R13: ffff8f96d976dc00 R14: 00000000032400b8 R15: 0000000000000000
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492299] FS:  0000000000000000(0000) GS:ffff8fb390680000(0000) knlGS:0000000000000000
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492303] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492306] CR2: 00007f155daa5258 CR3: 00000001128a4001 CR4: 0000000000770ee0
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492310] PKRU: 55555554
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492312] Call Trace:
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492317]  <IRQ>
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492328]  event_interrupt_isr_v9_4_3+0x6b/0x80 [amdgpu]
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492604]  interrupt_is_wanted+0x19/0x30 [amdgpu]
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.492884]  kgd2kfd_interrupt+0xbc/0x180 [amdgpu]
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.493178]  ? srso_alias_return_thunk+0x5/0x7f
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.493194]  ? gfx_v9_4_3_fault.isra.0+0x2d/0xf0 [amdgpu]
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.493488]  amdgpu_amdkfd_interrupt+0x1a/0x30 [amdgpu]
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.493773]  amdgpu_irq_dispatch+0x179/0x2a0 [amdgpu]
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.494071]  amdgpu_ih_process+0xa3/0x1d0 [amdgpu]
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.494357]  amdgpu_irq_handler+0x24/0x60 [amdgpu]
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.494641]  __handle_irq_event_percpu+0x3f/0x170
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.494655]  handle_irq_event+0x59/0xb0
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.494662]  handle_edge_irq+0x8c/0x230
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.494668]  __common_interrupt+0x4f/0xe0
2025-09-02T15:10:23+00:00 mi300 kernel: [947698.494678]  common_interrupt+0x89/0xa0
```

The server has 4 x MI300A.

```
#   echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
GPU:
  Name:                    AMD Instinct MI300A Accelerator
  Marketing Name:          AMD Instinct MI300A Accelerator
  Name:                    AMD Instinct MI300A Accelerator
  Marketing Name:          AMD Instinct MI300A Accelerator
  Name:                    AMD Instinct MI300A Accelerator
  Marketing Name:          AMD Instinct MI300A Accelerator
  Name:                    AMD Instinct MI300A Accelerator
  Marketing Name:          AMD Instinct MI300A Accelerator
  Name:                    gfx942
  Marketing Name:
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
      Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
  Name:                    gfx942
  Marketing Name:
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
      Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
  Name:                    gfx942
  Marketing Name:
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
      Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
  Name:                    gfx942
  Marketing Name:
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
      Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
```

Before that, the server keeps logging thousands of logs on a regular basis with 2 patterns:

```
2025-09-02T01:38:55+00:00 mi300 kernel: [899010.254914] amdgpu 0001:01:00.0: amdgpu: [gfxhub0] no-retry page fault (src_id:0 ring:144 vmid:3 pasid:32789)
2025-09-02T01:38:55+00:00 mi300  kernel: [899010.268068] amdgpu 0001:01:00.0: amdgpu:  for process rocpctl pid 789221 thread rocpctl pid 789221)
2025-09-02T01:38:55+00:00 mi300 kernel: [899010.279490] amdgpu 0001:01:00.0: amdgpu:   in page starting at address 0x00007ff5519dd000 from IH client 0x1b (UTCL2)
2025-09-02T01:38:55+00:00 mi300 kernel: [899010.292475] amdgpu 0001:01:00.0: amdgpu:   cookie node_id 9 fault from die AID2.XCD0
2025-09-02T01:38:55+00:00 mi300 kernel: [899010.302385] amdgpu 0001:01:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00300831
2025-09-02T01:38:55+00:00 mi300 kernel: [899010.311894] amdgpu 0001:01:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
2025-09-02T01:38:55+00:00 mi300 kernel: [899010.320911] amdgpu 0001:01:00.0: amdgpu:      MORE_FAULTS: 0x1
2025-09-02T01:38:55+00:00 mi300 kernel: [899010.328187] amdgpu 0001:01:00.0: amdgpu:      WALKER_ERROR: 0x0
2025-09-02T01:38:55+00:00 mi300 kernel: [899010.335435] amdgpu 0001:01:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
2025-09-02T01:38:55+00:00 mi300 kernel: [899010.343174] amdgpu 0001:01:00.0: amdgpu:      MAPPING_ERROR: 0x0
2025-09-02T01:38:55+00:00 mi300 kernel: [899010.350504] amdgpu 0001:01:00.0: amdgpu:      RW: 0x0
```

```
2025-09-02T23:56:23+00:00 mi300 kernel: [11067.106221] amdgpu: Freeing queue vital buffer 0x7f3ce9600000, queue evicted
2025-09-02T23:56:23+00:00 mi300 kernel: [11067.106231] amdgpu: Freeing queue vital buffer 0x7f3cfa200000, queue evicted
2025-09-02T23:56:23+00:00 mi300 kernel: [11067.106233] amdgpu: Freeing queue vital buffer 0x7f3d00000000, queue evicted
2025-09-02T23:56:23+00:00 mi300 kernel: [11067.106236] amdgpu: Freeing queue vital buffer 0x7f3d0ae00000, queue evicted
2025-09-02T23:56:23+00:00 mi300 kernel: [11067.106238] amdgpu: Freeing queue vital buffer 0x7f3d1ba00000, queue evicted
```

### Operating System

Ubuntu 22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD Instinct MI300A Accelerator

### GPU

4 x AMD Instinct MI300A Accelerator

### ROCm Version

6.4.3.60403-128~22.04

### ROCm Component

_No response_

### Steps to Reproduce

The issue is not 100% reproducible and the user has to submit a few on this pytorch jobs before it fails though it fails in around 70% of the cases.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
[37mROCk module version 6.12.12 is loaded[0m
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
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
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
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
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131005620(0x7cefcb4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131005620(0x7cefcb4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131005620(0x7cefcb4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131005620(0x7cefcb4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
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
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131815368(0x7db57c8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131815368(0x7db57c8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131815368(0x7db57c8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131815368(0x7db57c8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    2                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        2                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131815368(0x7db57c8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131815368(0x7db57c8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131815368(0x7db57c8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131815368(0x7db57c8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 4                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    3                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        3                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    129663296(0x7ba8140) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    129663296(0x7ba8140) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    129663296(0x7ba8140) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    129663296(0x7ba8140) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 5                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-cd0cb8e28fce8c84               
  Marketing Name:                                             
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    4                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   256                                
  Internal Node ID:        4                                  
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
  Packet Processor uCode:: 185                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98306184(0x5dc0888) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98306184(0x5dc0888) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98306184(0x5dc0888) KB             
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
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
Agent 6                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-9701816febd21c93               
  Marketing Name:                                             
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    5                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   256                                
  Internal Node ID:        5                                  
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
  Packet Processor uCode:: 185                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98306184(0x5dc0888) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98306184(0x5dc0888) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98306184(0x5dc0888) KB             
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
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
Agent 7                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-47a9d4a84f0aa643               
  Marketing Name:                                             
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    6                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   256                                
  Internal Node ID:        6                                  
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
  Packet Processor uCode:: 185                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98306184(0x5dc0888) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98306184(0x5dc0888) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98306184(0x5dc0888) KB             
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
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
Agent 8                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-5adb90220e168d40               
  Marketing Name:                                             
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    7                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   512                                
  Internal Node ID:        7                                  
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
  Packet Processor uCode:: 185                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98306184(0x5dc0888) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98306184(0x5dc0888) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98306184(0x5dc0888) KB             
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
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

```
# dpkg -l | grep rocm
ii  rocm-core                              6.4.3.60403-128~22.04                   amd64        ROCm Runtime software stack
ii  rocm-smi-lib                           7.7.0.60403-128~22.04                   amd64        AMD System Management libraries
ii  rocminfo                               1.0.0.60403-128~22.04                   amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool
```

```
# dpkg -l | grep amdgpu
ii  amdgpu-dkms                            1:6.12.12.60403-2194681.22.04           all          amdgpu driver in DKMS format.
ii  amdgpu-dkms-firmware                   1:6.12.12.60403-2194681.22.04           all          firmware blobs used by amdgpu driver in DKMS format
ii  libdrm-amdgpu1:amd64                   2.4.113-2~ubuntu0.22.04.1               amd64        Userspace interface to amdgpu-specific kernel DRM services -- runtime
```

```
ii  amd64-microcode                        3.20191218.1ubuntu2.3                   amd64        Processor microcode firmware for AMD CPUs
ii  amdgpu-dkms-firmware                   1:6.12.12.60403-2194681.22.04           all          firmware blobs used by amdgpu driver in DKMS format
```

---

## 评论 (7 条)

### 评论 #1 — ppanchad-amd (2025-09-05T15:28:31Z)

Hi @diegolmoreno. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — gcapodagAMD (2025-09-05T21:52:19Z)

does calling `rocm-smi` recover the processes from hanging?

---

### 评论 #3 — tcgu-amd (2025-09-08T15:10:03Z)

@diegolmoreno Thanks for reaching out, and sorry that you guys are experiencing issues. At a glance, there seems to be a lot of page faults happening. Do you have a minimal reproducer that we can use to reproduce the issue? Thanks! 

---

### 评论 #4 — tcgu-amd (2025-09-19T14:50:39Z)

Hi @diegolmoreno, we are seeing similar issues somewhere else as well and are in the process of investigating. In the meantime, if you could provide a reproducer that can help verify if it is the same issue that would be very helpful. Thanks! 

---

### 评论 #5 — diegolmoreno (2025-09-22T15:07:31Z)

Hi, apologies for the silence during last week.

We're still trying to get a good reproducer from the user triggering this, what I can tell you is for now the relevant packages that are involved when this is triggered:

python 3.12.8 with:
 - pytorch-triton-rocm       3.4.0
 - torch                     2.8.0+rocm6.4 (wheel https://download.pytorch.org/whl/rocm6.4)
 - torchvision               0.23.0+rocm6.4 (wheel https://download.pytorch.org/whl/rocm6.4)

The issue arrives after 10 or 20 hours of run and only for some runs. There are some particulars like the user loading data with mmap (over Lustre). I'm still trying to find a reproducer by running user's code.

---

### 评论 #6 — tcgu-amd (2025-10-17T16:54:26Z)

Hi @diegolmoreno, any updates? Thanks! 

---

### 评论 #7 — tcgu-amd (2025-10-22T21:01:25Z)

Hi @diegolmoreno, I will be closing this issue for now due to inactivity. Please let us know when you have an update. Thanks! 

---
