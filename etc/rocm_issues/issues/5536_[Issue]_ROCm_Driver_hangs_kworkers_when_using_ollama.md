# [Issue]: ROCm Driver hangs kworkers when using ollama.

> **Issue #5536**
> **状态**: closed
> **创建时间**: 2025-10-17T18:08:23Z
> **更新时间**: 2025-12-16T17:13:15Z
> **关闭时间**: 2025-12-16T17:13:15Z
> **作者**: Hubert97
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5536

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

When runnig ollama the system begins to slowdown gradually. Load average rises to very high levels although htop show minimal CPU usage.
Ollama doesn't have to run any model. Just running it causes the issue.
The
```
ps -eo pid,ppid,cmd,state,wchan:20 | grep "^ *[0-9].* D"
```
Shows many kworkers in "D" state.
```
ubuntu@ubuntu:~$ ps -eo pid,ppid,cmd,state,wchan:20 | grep "^ *[0-9].* D" | wc -l
140
```
Call stack of these kworkers:
```
root@ubuntu:/proc/2464# cat stack 
[<0>] dma_fence_default_wait+0x1e1/0x220
[<0>] dma_fence_wait_timeout+0x116/0x140
[<0>] amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]
[<0>] process_one_work+0x184/0x3a0
[<0>] worker_thread+0x306/0x440
[<0>] kthread+0xf2/0x120
[<0>] ret_from_fork+0x47/0x70
[<0>] ret_from_fork_asm+0x1b/0x30
root@ubuntu:/proc/2464# 
```
dmesg has following errors:
```
[  303.249906] systemd-journald[570]: /var/log/journal/3ee6620f748f4315899859223e174032/user-1000.journal: Journal file uses a different sequence number ID, rotating.
[  367.891831] [drm:amddrm_sched_entity_push_job [amd_sched]] *ERROR* Trying to push to a killed entity
[  369.802805] amdgpu: Freeing queue vital buffer 0x773322600000, queue evicted
[  369.866431] [drm:amddrm_sched_entity_push_job [amd_sched]] *ERROR* Trying to push to a killed entity
[  492.679899] INFO: task kworker/12:0:91 blocked for more than 122 seconds.
[  492.679942]       Tainted: G           OE      6.8.0-85-generic #85-Ubuntu
[  492.679969] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[  492.679996] task:kworker/12:0    state:D stack:0     pid:91    tgid:91    ppid:2      flags:0x00004000
[  492.680006] Workqueue: events amdgpu_tlb_fence_work [amdgpu]
[  492.680591] Call Trace:
[  492.680595]  <TASK>
[  492.680603]  __schedule+0x27c/0x6b0
[  492.680619]  schedule+0x33/0x110
[  492.680628]  schedule_timeout+0x157/0x170
[  492.680639]  dma_fence_default_wait+0x1e1/0x220
[  492.680649]  ? __pfx_dma_fence_default_wait_cb+0x10/0x10
[  492.680659]  dma_fence_wait_timeout+0x116/0x140
[  492.680668]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]
[  492.681161]  process_one_work+0x184/0x3a0
[  492.681170]  worker_thread+0x306/0x440
[  492.681177]  ? __pfx_worker_thread+0x10/0x10
[  492.681183]  kthread+0xf2/0x120
[  492.681190]  ? __pfx_kthread+0x10/0x10
[  492.681197]  ret_from_fork+0x47/0x70
[  492.681204]  ? __pfx_kthread+0x10/0x10
[  492.681211]  ret_from_fork_asm+0x1b/0x30
[  492.681223]  </TASK>
[  492.681232] INFO: task kworker/12:1:153 blocked for more than 122 seconds.
[  492.681256]       Tainted: G           OE      6.8.0-85-generic #85-Ubuntu
[  492.681279] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[  492.681302] task:kworker/12:1    state:D stack:0     pid:153   tgid:153   ppid:2      flags:0x00004000
[  492.681310] Workqueue: events amdgpu_tlb_fence_work [amdgpu]
[  492.681800] Call Trace:
[  492.681802]  <TASK>
[  492.681807]  __schedule+0x27c/0x6b0
[  492.681818]  schedule+0x33/0x110
[  492.681825]  schedule_timeout+0x157/0x170
[  492.681834]  dma_fence_default_wait+0x1e1/0x220
[  492.681842]  ? __pfx_dma_fence_default_wait_cb+0x10/0x10
[  492.681850]  dma_fence_wait_timeout+0x116/0x140
[  492.681859]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]
[  492.682359]  process_one_work+0x184/0x3a0
[  492.682368]  worker_thread+0x306/0x440
[  492.682375]  ? srso_return_thunk+0x5/0x5f
[  492.682381]  ? _raw_spin_lock_irqsave+0xe/0x20
[  492.682390]  ? __pfx_worker_thread+0x10/0x10
[  492.682396]  kthread+0xf2/0x120
[  492.682404]  ? __pfx_kthread+0x10/0x10
[  492.682412]  ret_from_fork+0x47/0x70
[  492.682419]  ? __pfx_kthread+0x10/0x10
[  492.682426]  ret_from_fork_asm+0x1b/0x30
[  492.682440]  </TASK>
[  492.682487] INFO: task kworker/12:2:2318 blocked for more than 122 seconds.
[  492.682522]       Tainted: G           OE      6.8.0-85-generic #85-Ubuntu
[  492.682548] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[  492.682575] task:kworker/12:2    state:D stack:0     pid:2318  tgid:2318  ppid:2      flags:0x00004000
[  492.682585] Workqueue: events amdgpu_tlb_fence_work [amdgpu]
[  492.683145] Call Trace:
[  492.683148]  <TASK>
[  492.683154]  __schedule+0x27c/0x6b0
[  492.683167]  schedule+0x33/0x110
[  492.683175]  schedule_timeout+0x157/0x170
[  492.683185]  dma_fence_default_wait+0x1e1/0x220
[  492.683193]  ? __pfx_dma_fence_default_wait_cb+0x10/0x10
[  492.683203]  dma_fence_wait_timeout+0x116/0x140
[  492.683212]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]
[  492.683771]  process_one_work+0x184/0x3a0
[  492.683779]  worker_thread+0x306/0x440
[  492.683786]  ? __pfx_worker_thread+0x10/0x10
[  492.683792]  kthread+0xf2/0x120
[  492.683799]  ? __pfx_kthread+0x10/0x10
[  492.683807]  ret_from_fork+0x47/0x70
[  492.683813]  ? __pfx_kthread+0x10/0x10
[  492.683820]  ret_from_fork_asm+0x1b/0x30
[  492.683832]  </TASK>
[  492.683835] INFO: task kworker/12:3:2319 blocked for more than 122 seconds.
[  492.683859]       Tainted: G           OE      6.8.0-85-generic #85-Ubuntu
[  492.683882] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[  492.683905] task:kworker/12:3    state:D stack:0     pid:2319  tgid:2319  ppid:2      flags:0x00004000
[  492.683913] Workqueue: events amdgpu_tlb_fence_work [amdgpu]
[  492.684394] Call Trace:
[  492.684397]  <TASK>
[  492.684402]  __schedule+0x27c/0x6b0
[  492.684413]  schedule+0x33/0x110
[  492.684420]  schedule_timeout+0x157/0x170
[  492.684429]  dma_fence_default_wait+0x1e1/0x220
[  492.684436]  ? __pfx_dma_fence_default_wait_cb+0x10/0x10
[  492.684444]  dma_fence_wait_timeout+0x116/0x140
[  492.684452]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]
[  492.684940]  process_one_work+0x184/0x3a0
[  492.684948]  worker_thread+0x306/0x440
[  492.684956]  ? __pfx_worker_thread+0x10/0x10
[  492.684962]  kthread+0xf2/0x120
[  492.684969]  ? __pfx_kthread+0x10/0x10
[  492.684979]  ret_from_fork+0x47/0x70
[  492.684985]  ? __pfx_kthread+0x10/0x10
[  492.684992]  ret_from_fork_asm+0x1b/0x30
[  492.685004]  </TASK>
[  492.685007] INFO: task kworker/12:4:2320 blocked for more than 122 seconds.
[  492.685031]       Tainted: G           OE      6.8.0-85-generic #85-Ubuntu
[  492.685054] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[  492.685078] task:kworker/12:4    state:D stack:0     pid:2320  tgid:2320  ppid:2      flags:0x00004000
[  492.685085] Workqueue: events amdgpu_tlb_fence_work [amdgpu]
[  492.685574] Call Trace:
[  492.685577]  <TASK>
[  492.685583]  __schedule+0x27c/0x6b0
[  492.685594]  schedule+0x33/0x110
[  492.685602]  schedule_timeout+0x157/0x170
[  492.685611]  dma_fence_default_wait+0x1e1/0x220
[  492.685618]  ? __pfx_dma_fence_default_wait_cb+0x10/0x10
[  492.685627]  dma_fence_wait_timeout+0x116/0x140
[  492.685635]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]
[  492.686115]  process_one_work+0x184/0x3a0
[  492.686123]  worker_thread+0x306/0x440
[  492.686131]  ? __pfx_worker_thread+0x10/0x10
[  492.686136]  kthread+0xf2/0x120
[  492.686143]  ? __pfx_kthread+0x10/0x10
[  492.686150]  ret_from_fork+0x47/0x70
[  492.686156]  ? __pfx_kthread+0x10/0x10
[  492.686162]  ret_from_fork_asm+0x1b/0x30
[  492.686174]  </TASK>
[  492.686177] INFO: task kworker/12:5:2321 blocked for more than 122 seconds.
[  492.686201]       Tainted: G           OE      6.8.0-85-generic #85-Ubuntu
[  492.686222] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[  492.686245] task:kworker/12:5    state:D stack:0     pid:2321  tgid:2321  ppid:2      flags:0x00004000
[  492.686252] Workqueue: events amdgpu_tlb_fence_work [amdgpu]
[  492.686740] Call Trace:
[  492.686743]  <TASK>
[  492.686748]  __schedule+0x27c/0x6b0
[  492.686759]  schedule+0x33/0x110
[  492.686766]  schedule_timeout+0x157/0x170
[  492.686775]  dma_fence_default_wait+0x1e1/0x220
[  492.686782]  ? __pfx_dma_fence_default_wait_cb+0x10/0x10
[  492.686791]  dma_fence_wait_timeout+0x116/0x140
[  492.686799]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]
[  492.687280]  process_one_work+0x184/0x3a0
[  492.687288]  worker_thread+0x306/0x440
[  492.687296]  ? __pfx_worker_thread+0x10/0x10
[  492.687301]  kthread+0xf2/0x120
[  492.687308]  ? __pfx_kthread+0x10/0x10
[  492.687316]  ret_from_fork+0x47/0x70
[  492.687321]  ? __pfx_kthread+0x10/0x10
[  492.687328]  ret_from_fork_asm+0x1b/0x30
[  492.687340]  </TASK>
[  492.687343] INFO: task kworker/12:6:2322 blocked for more than 122 seconds.
[  492.687366]       Tainted: G           OE      6.8.0-85-generic #85-Ubuntu
[  492.687388] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[  492.687412] task:kworker/12:6    state:D stack:0     pid:2322  tgid:2322  ppid:2      flags:0x00004000
[  492.687419] Workqueue: events amdgpu_tlb_fence_work [amdgpu]
[  492.687909] Call Trace:
[  492.687911]  <TASK>
[  492.687916]  __schedule+0x27c/0x6b0
[  492.687928]  schedule+0x33/0x110
[  492.687935]  schedule_timeout+0x157/0x170
[  492.687944]  dma_fence_default_wait+0x1e1/0x220
[  492.687952]  ? __pfx_dma_fence_default_wait_cb+0x10/0x10
[  492.687961]  dma_fence_wait_timeout+0x116/0x140
[  492.687969]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]
[  492.688449]  process_one_work+0x184/0x3a0
[  492.688457]  worker_thread+0x306/0x440
[  492.688464]  ? __pfx_worker_thread+0x10/0x10
[  492.688470]  kthread+0xf2/0x120
[  492.688477]  ? __pfx_kthread+0x10/0x10
[  492.688484]  ret_from_fork+0x47/0x70
[  492.688490]  ? __pfx_kthread+0x10/0x10
[  492.688505]  ret_from_fork_asm+0x1b/0x30
[  492.688517]  </TASK>
[  492.688520] INFO: task kworker/12:7:2323 blocked for more than 122 seconds.
[  492.688544]       Tainted: G           OE      6.8.0-85-generic #85-Ubuntu
[  492.688567] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[  492.688590] task:kworker/12:7    state:D stack:0     pid:2323  tgid:2323  ppid:2      flags:0x00004000
[  492.688597] Workqueue: events amdgpu_tlb_fence_work [amdgpu]
[  492.689077] Call Trace:
[  492.689080]  <TASK>
[  492.689085]  __schedule+0x27c/0x6b0
[  492.689096]  schedule+0x33/0x110
[  492.689103]  schedule_timeout+0x157/0x170
[  492.689112]  dma_fence_default_wait+0x1e1/0x220
[  492.689119]  ? __pfx_dma_fence_default_wait_cb+0x10/0x10
[  492.689127]  dma_fence_wait_timeout+0x116/0x140
[  492.689135]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]
[  492.689622]  process_one_work+0x184/0x3a0
[  492.689630]  worker_thread+0x306/0x440
[  492.689638]  ? __pfx_worker_thread+0x10/0x10
[  492.689643]  kthread+0xf2/0x120
[  492.689650]  ? __pfx_kthread+0x10/0x10
[  492.689658]  ret_from_fork+0x47/0x70
[  492.689664]  ? __pfx_kthread+0x10/0x10
[  492.689671]  ret_from_fork_asm+0x1b/0x30
[  492.689683]  </TASK>
[  492.689687] INFO: task kworker/12:8:2324 blocked for more than 122 seconds.
[  492.689710]       Tainted: G           OE      6.8.0-85-generic #85-Ubuntu
[  492.689732] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[  492.689756] task:kworker/12:8    state:D stack:0     pid:2324  tgid:2324  ppid:2      flags:0x00004000
[  492.689763] Workqueue: events amdgpu_tlb_fence_work [amdgpu]
[  492.690243] Call Trace:
[  492.690246]  <TASK>
[  492.690250]  __schedule+0x27c/0x6b0
[  492.690261]  schedule+0x33/0x110
[  492.690268]  schedule_timeout+0x157/0x170
[  492.690277]  dma_fence_default_wait+0x1e1/0x220
[  492.690284]  ? __pfx_dma_fence_default_wait_cb+0x10/0x10
[  492.690293]  dma_fence_wait_timeout+0x116/0x140
[  492.690301]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]
[  492.690789]  process_one_work+0x184/0x3a0
[  492.690797]  worker_thread+0x306/0x440
[  492.690805]  ? __pfx_worker_thread+0x10/0x10
[  492.690811]  kthread+0xf2/0x120
[  492.690818]  ? __pfx_kthread+0x10/0x10
[  492.690825]  ret_from_fork+0x47/0x70
[  492.690831]  ? __pfx_kthread+0x10/0x10
[  492.690839]  ret_from_fork_asm+0x1b/0x30
[  492.690851]  </TASK>
[  492.690854] INFO: task kworker/12:9:2325 blocked for more than 122 seconds.
[  492.690877]       Tainted: G           OE      6.8.0-85-generic #85-Ubuntu
[  492.690900] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[  492.690923] task:kworker/12:9    state:D stack:0     pid:2325  tgid:2325  ppid:2      flags:0x00004000
[  492.690930] Workqueue: events delayed_fput
[  492.690938] Call Trace:
[  492.690940]  <TASK>
[  492.690945]  __schedule+0x27c/0x6b0
[  492.690951]  ? srso_return_thunk+0x5/0x5f
[  492.690961]  schedule+0x33/0x110
[  492.690968]  schedule_timeout+0x157/0x170
[  492.690977]  dma_fence_default_wait+0x1e1/0x220
[  492.690984]  ? __pfx_dma_fence_default_wait_cb+0x10/0x10
[  492.690992]  dma_fence_wait_timeout+0x116/0x140
[  492.691000]  amdgpu_vm_fini+0xf1/0x610 [amdgpu]
[  492.691480]  ? srso_return_thunk+0x5/0x5f
[  492.691486]  ? amdgpu_ctx_mgr_fini+0x105/0x1d0 [amdgpu]
[  492.691978]  amdgpu_driver_postclose_kms+0x1b7/0x2f0 [amdgpu]
[  492.692445]  drm_file_free+0x1e9/0x260
[  492.692453]  drm_release+0xb7/0x130
[  492.692460]  __fput+0xa3/0x2e0
[  492.692467]  delayed_fput+0x23/0x40
[  492.692473]  process_one_work+0x184/0x3a0
[  492.692481]  worker_thread+0x306/0x440
[  492.692488]  ? __pfx_worker_thread+0x10/0x10
[  492.692503]  kthread+0xf2/0x120
[  492.692510]  ? __pfx_kthread+0x10/0x10
[  492.692518]  ret_from_fork+0x47/0x70
[  492.692524]  ? __pfx_kthread+0x10/0x10
[  492.692531]  ret_from_fork_asm+0x1b/0x30
[  492.692543]  </TASK>
[  492.692546] Future hung task reports are suppressed, see sysctl kernel.hung_task_warnings
```


### Operating System

NAME="Ubuntu" VERSION="24.04.3 LTS (Noble Numbat)

### CPU

model name      : AMD Ryzen 7 1700X Eight-Core Processor

### GPU

  Name:                    AMD Ryzen 7 1700X Eight-Core Processor   Marketing Name:          AMD Ryzen 7 1700X Eight-Core Processor   Name:                    gfx1201                               Marketing Name:          AMD Radeon RX 9070 XT                     Name:                    amdgcn-amd-amdhsa--gfx1201                Name:                    amdgcn-amd-amdhsa--gfx12-generic   

### ROCm Version

ROCm 7.0.2, ROCm 7.0.1, ROCm 6.4.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ubuntu@ubuntu:~$ rocminfo --support 
ROCk module version 6.14.14 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.11
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
  Name:                    AMD Ryzen 7 1700X Eight-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 1700X Eight-Core Processor
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
      Size:                    32784440(0x1f44038) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32784440(0x1f44038) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32784440(0x1f44038) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32784440(0x1f44038) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-79c2a0d8c9ec94dd               
  Marketing Name:          AMD Radeon RX 9070 XT              
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30032(0x7550)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2460                               
  BDFID:                   2816                               
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 58                                 
  SDMA engine uCode::      380                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16695296(0xfec000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1201         
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
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

_No response_

---

## 评论 (25 条)

### 评论 #1 — Hubert97 (2025-10-17T18:10:05Z)

To reproduce:
Install ROCm 7.0.2
Run ollama in amd flavor in docker
Killing ollama doesn't end kworkers.
Reloading driver is impossible.
Ollama actually works in this state for some time.
Models can be loaded and run. However after some time the whole system becomes unresponsive (running basic command like ps, uptime or cd takes really long time).
While Ollama runs number of kworker increases.

---

### 评论 #2 — ExileInParadise (2025-10-19T12:43:58Z)

This fix in 6.17 may be related:
https://web.git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=aa5fc4362fac9351557eb27c745579159a2e4520

---

### 评论 #3 — Hubert97 (2025-10-19T21:01:15Z)

Upgraded to 6.17. Sadly behaviour didn't change.

---

### 评论 #4 — huanrwan-amd (2025-10-20T20:09:11Z)

Hi @Hubert97, thanks for posting the issue. From the dmesg logs, it seems the kworkers are waiting on a DMA fence that is never signaled. Can you please post the firmware version and driver version using `amd-smi firmware` and `amd-smi`? Thanks.

---

### 评论 #5 — Hubert97 (2025-10-20T20:28:14Z)

Sure. I have updated to ROCm 7.0.2 yesterday in hopes that it will work with kernel 6.17 but no luck.
```
ubuntu@ubuntu:~$ amd-smi firmware
GPU: 0
    FW_LIST:
        FW 0:
            FW_ID: CP_PFP
            FW_VERSION: 2630
        FW 1:
            FW_ID: CP_ME
            FW_VERSION: 2590
        FW 2:
            FW_ID: CP_MEC1
            FW_VERSION: 2800
        FW 3:
            FW_ID: RLC
            FW_VERSION: 12483700
        FW 4:
            FW_ID: SDMA0
            FW_VERSION: 6812397
        FW 5:
            FW_ID: SDMA1
            FW_VERSION: 6812397
        FW 6:
            FW_ID: VCN
            FW_VERSION: 09.10.40.01
        FW 7:
            FW_ID: PSP_SOSDRV
            FW_VERSION: 00.3A.06.14
        FW 8:
            FW_ID: ASD
            FW_VERSION: 553648359
        FW 9:
            FW_ID: PM
            FW_VERSION: 00.104.57.00
```

=======================================================
```
ubuntu@ubuntu:~$ amd-smi
+------------------------------------------------------------------------------+
| AMD-SMI 26.0.2+39589fda      amdgpu version: Linuxver ROCm version: 7.0.2    |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:0b:00.0  AMD Radeon RX 9070 XT | 2 %      30 °C   0            19/317 W |
|   0       0     N/A             N/A | 3 %      0.0 %            538/16304 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
```

---

### 评论 #6 — huanrwan-amd (2025-10-20T21:38:03Z)

@Hubert97 Seems amdgpu version is truncated: "**amdgpu version: Linuxver**"
Can you try `dkms status` or `amd-smi version` ?

---

### 评论 #7 — Hubert97 (2025-10-20T21:49:41Z)

Sure @huanrwan-amd 
```
ubuntu@ubuntu:~$ dkms status
ubuntu@ubuntu:~$ amd-smi version
AMDSMI Tool: 26.0.2+39589fda | AMDSMI Library version: 26.0.2 | ROCm version: 7.0.2 | amdgpu version: Linuxversion6.17.0(ubuntu@ubuntu)(gcc(Ubuntu13.3.0-6ubuntu2~24.04)13.3.0,GNUld(GNUBinutilsforUbuntu)2.42)#2SMPPREEMPT_DYNAMICSunOct1920:26:32UTC2025 | amd_hsmp version: N/A
ubuntu@ubuntu:~$ 
```

---

### 评论 #8 — Hubert97 (2025-10-20T21:53:00Z)

To install amdgpu i did:
```
sudo apt update
wget https://repo.radeon.com/amdgpu-install/7.0.2/ubuntu/jammy/amdgpu-install_7.0.2.70002-1_all.deb
sudo apt install ./amdgpu-install_7.0.2.70002-1_all.deb
sudo amdgpu-install -y --usecase=graphics,rocm
sudo usermod -a -G render,video $LOGNAME

```
from: [https://www.amd.com/en/support/downloads/drivers.html/graphics/radeon-rx/radeon-rx-9000-series/amd-radeon-rx-9070-xt.html](url)

During installation i observed no issues.

---

### 评论 #9 — huanrwan-amd (2025-10-21T18:20:55Z)

@Hubert97 Thanks for providing the info. An internal ticket is created to track this.

---

### 评论 #10 — num2gardena (2025-10-27T21:08:45Z)

Same issue on Bazzite 42 with ROCm 6.3.1. Number of D-state kworkers keeps increasing until the system crashes.

---

### 评论 #11 — num2gardena (2025-10-28T18:39:29Z)

@Hubert97 have you found any workaround for this issue? I can hardly believe this problem has existed ever since 6.3.1 (from 10 months ago) without anyone noticing issues in Ollama. Have you tried older versions of Ollama?

---

### 评论 #12 — Hubert97 (2025-10-28T19:05:31Z)

I did. But to no avail. Behaves the same.
Clearly the problem is with drivers. Kernel waits for events that never come.
I do not know of awareness in ollama community about this issue.
Maybe this behavior can be worked around by using vulkan backend. Might be worth checking

---

### 评论 #13 — unclejack (2025-10-29T18:23:12Z)

I've encountered the very same problem with amdgpu and rocm.
```
[  246.947584] INFO: task kworker/2:4:944 blocked for more than 122 seconds.
[  246.947588]       Not tainted 6.17.5-arch1-1 #1
[  246.947593] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[  246.947596] task:kworker/2:4     state:D stack:0     pid:944   tgid:944   ppid:2      task_flags:0x4208060 flags:0x00004000
[  246.947604] Workqueue: events amdgpu_tlb_fence_work [amdgpu]
[  246.948114] Call Trace:
[  246.948117]  <TASK>
[  246.948124]  __schedule+0x418/0x1330
[  246.948134]  ? srso_return_thunk+0x5/0x5f
[  246.948141]  ? srso_return_thunk+0x5/0x5f
[  246.948147]  ? srso_return_thunk+0x5/0x5f
[  246.948153]  ? place_entity+0x1b/0x150
[  246.948160]  ? srso_return_thunk+0x5/0x5f
[  246.948172]  schedule+0x27/0xd0
[  246.948180]  schedule_timeout+0xbd/0x100
[  246.948191]  dma_fence_default_wait+0x199/0x280
[  246.948198]  ? __pfx_dma_fence_default_wait_cb+0x10/0x10
[  246.948209]  dma_fence_wait_timeout+0x129/0x150
[  246.948217]  amdgpu_tlb_fence_work+0x2c/0xe0 [amdgpu 02022ce4aee5e37157721ed7588d157409a3623e]
[  246.948720]  ? lock_timer_base+0x70/0x90
[  246.948727]  process_one_work+0x193/0x350
[  246.948736]  worker_thread+0x2d7/0x410
[  246.948745]  ? __pfx_worker_thread+0x10/0x10
[  246.948752]  kthread+0xfc/0x240
[  246.948759]  ? __pfx_kthread+0x10/0x10
[  246.948766]  ? __pfx_kthread+0x10/0x10
[  246.948775]  ret_from_fork+0x1c4/0x1f0
[  246.948782]  ? __pfx_kthread+0x10/0x10
[  246.948790]  ret_from_fork_asm+0x1a/0x30
[  246.948807]  </TASK>
```
It doesn't exactly inspire trust, nor does it make one consider recommending these AMD GPUs for serious use at work.

---

### 评论 #14 — Hubert97 (2025-10-29T18:45:26Z)

It certainly feels rushed.

---

### 评论 #15 — unclejack (2025-10-30T07:27:14Z)

The recently released Linux kernel 6.17.6 doesn't seem to include any fixes for amdgpu at all.

This bug is extremely serious. The system becomes unstable and crashes after a while. It also has zombie processes due to this same problem. Older kernels don't help. There were bugs all the way back to kernel 6.12. Resetting the GPU doesn't help at all.

AMD's GPUs are starting to look like a joke due to these bugs. Who do these people at AMD expect to keep throwing money at their unreliable hardware and software stack?

---

### 评论 #16 — zoitrok (2025-10-30T08:27:11Z)

I've encountered exactly the same.
I have two desktops running EndeavourOS. It happens on a desktop with a RX 6650 XT, but not on a desktop with a RX 7900 XTX.

I believe it started after installing [linux-firmware-amdgpu 20251011-1](https://gitlab.archlinux.org/archlinux/packaging/packages/linux-firmware/-/commits/main). Or around that time -- no major kernel updates in the days around that, at least.

Edit:
I just tried rolling back to linux-firmware 20250917-1, with no success. I'll have to dig deeper what packages were updated around that same time.

---

### 评论 #17 — Hubert97 (2025-10-31T15:49:15Z)

Checked today using newest 7.1.0.
Issue is still present.

---

### 评论 #18 — ExileInParadise (2025-11-04T16:29:36Z)

As I've been wrangling this myself - I think this describes the key, relevant change:
https://lkml.org/lkml/2025/8/18/1146

And I think it is this specific code change which needs to be reverted or done differently:
https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/drivers/gpu/drm/amd/amdgpu/amdgpu_vm.c?id=1f02f2044bda1db1fd995bc35961ab075fa7b5a2

I am looking to build a test a kernel with just that change reverted to see if that unblocks the stuck kernel workers. If I can figure something out, I will update.

---

### 评论 #19 — jimfunk (2025-11-05T18:51:05Z)

I applied the patches suggested in https://gitlab.freedesktop.org/drm/amd/-/issues/4513 and https://patchwork.freedesktop.org/patch/684793/ to 6.18-rc3 and it appears to have been solved.

---

### 评论 #20 — unclejack (2025-11-08T18:04:35Z)

Older versions of the kernel don't have this bug either. Several hours of testing have confirmed this is indeed the case. It doesn't behave like a hardware bug. At least that means this can be fixed with some changes made to the kernel's code.

---

### 评论 #21 — num2gardena (2025-11-17T21:13:43Z)

Works 

> I applied the patches suggested in https://gitlab.freedesktop.org/drm/amd/-/issues/4513 and https://patchwork.freedesktop.org/patch/684793/ to 6.18-rc3 and it appears to have been solved.

I upgraded my kernel to 6.17.8 which includes your referenced patch, now it works for me on Fedora 43 with RX 7900 GRE.

---

### 评论 #22 — mamoit (2025-11-18T19:31:55Z)

For my use case, which is just running ollama, I ditched the proprietary driver and rocm altogether and started using [vulkan](https://docs.ollama.com/gpu#vulkan-gpu-support) instead.
So far so good, will report back if there are any issues.

---

### 评论 #23 — huanrwan-amd (2025-11-19T19:13:23Z)

Hi @Hubert97, have you tested with the following?

> Works
> 
> > I applied the patches suggested in https://gitlab.freedesktop.org/drm/amd/-/issues/4513 and https://patchwork.freedesktop.org/patch/684793/ to 6.18-rc3 and it appears to have been solved.
> 
> I upgraded my kernel to 6.17.8 which includes your referenced patch, now it works for me on Fedora 43 with RX 7900 GRE.



---

### 评论 #24 — ExileInParadise (2025-11-24T19:20:21Z)

Debian 14 "Forky" with kernel 6.17.8+ no longer throws the "drm:amddrm_sched_entity_push_job [amd_sched]] *ERROR* Trying to push to a killed entity" for me as well
Switching to Vulkan for Ollama also got everything working again on my gfx900 Radeon 64 node as well.
Great tips and fixes everyone thank you much!

---

### 评论 #25 — huanrwan-amd (2025-12-16T17:13:15Z)

close the issue as fixed

---
