# 🐞 Bug Report: Strix Halo (Ryzen AI Max 395+) + ROCm 7.1 + AI workloads + Video Encoding → GPU Hang, VRAM Loss, GNOME  Crash

> **Issue #5665**
> **状态**: closed
> **创建时间**: 2025-11-14T00:54:21Z
> **更新时间**: 2026-03-04T14:51:46Z
> **关闭时间**: 2026-01-19T00:24:30Z
> **作者**: kickinz1
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5665

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- adityas-amd

## 描述

### Problem Description

**System:**

* **Device:** Evo-x2 AI Max 395+ (Strix Halo, Ryzen AI Max 395+)
* **RAM:** 128GB
* **OS:** Ubuntu 24.04 OEM
* **Kernel:** 6.14.0-1015-oem
* **ROCm:** ROCm 7.1.25424-4179531dcd

* **Display Server:** GNOME Shell on Wayland (also reproducible on Xorg)
* **Other software:** Ollama (ROCm backend), Open-WebUI (PyTorch 2.8.0+rocm7.1.0), Sunshine (streaming, various encoders)

## Firmware details

linux-firmware: 20240318.git3b128b60-0ubuntu2.19
Firmware blobs present in /lib/firmware/amdgpu/:
- navi10_*.bin.zst
- navi12_*.bin.zst
- navi14_*.bin.zst

(No strix_halo or gfx1151 blobs found in this firmware version, but all up-to-date navi blobs present.)

No explicit amdgpu firmware load lines appear in dmesg, but the driver is working and ROCm detects the GPU (gfx1151) with correct VRAM and PCI ID.

---

## **Description**

Running *heavy AI workloads* (Ollama, PyTorch, WebUI) with **ROCm 7.1** on the Strix Halo iGPU is stable **unless** the **Sunshine streaming server** (hardware video encoding for game streaming) is also running.

When **AI compute and Sunshine streaming (using hardware encoder/VPE)** run at the same time, the system will eventually:

* Freeze or hang
* Crash the GNOME Shell session 
* Drop all GPU VRAM (“VRAM is lost due to GPU reset!”)
* Cause full GPU reset/failure to recover
* Show *catastrophic* MES/SDMA/VPE driver errors

This makes Strix Halo APUs **unusable for simultaneous AI + game/desktop streaming**, even though both are stable when run separately.

> **NOTE:**
> I can successfully run a **Shadow of the Tomb Raider** benchmark **at the same time** as I use **Gemma3:27B** with Open-WebUI (Ollama ROCm backend) with *no crash or instability*.
> The issue only appears when combining AI workloads with Sunshine streaming (video encoding).



## **What I Expected**

* Both AI compute (e.g., **Gemma3:27B** inference) and hardware-accelerated streaming should be possible at the same time on a high-end APU.
* ROCm/AMDGPU drivers should recover gracefully from heavy/parallel workloads.
* No session or GPU crash.

---

## **What Actually Happens**

* Catastrophic driver failure, logs show:

  * `amdgpu: MES failed to respond to msg=REMOVE_QUEUE`
  * `amdgpu: GPU reset begin!`
  * `amdgpu: VRAM is lost due to GPU reset!`
  * `amdgpu: Ring sdma0 reset failure`
  * `amdgpu: resume of IP block <vpe_v6_1> failed -110`
  * `amdgpu: suspend of IP block <mes_v11_0> failed -110`
  * Full context loss: “fatal server error”, “Xwayland exited unexpectedly”, “context is innocent”, etc.

---

## **Full Log Excerpt**

```text
amdgpu: MES failed to respond to msg=REMOVE_QUEUE
amdgpu: MES might be in unrecoverable state, issue a GPU reset
amdgpu: GPU reset begin!
amdgpu: Failed to evict process queues
amdgpu: VRAM is lost due to GPU reset!
amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu: suspend of IP block <mes_v11_0> failed -110
amdgpu: resume of IP block <vpe_v6_1> failed -110
amdgpu: Ring sdma0 reset failure
amdgpu: GPU reset begin!
...
gnome-shell: JS ERROR: Gio.IOErrorEnum: Xwayland exited unexpectedly
[drm:do_aquire_global_lock.isra.0 [amdgpu]] *ERROR* [CRTC:79:crtc-0] hw_done or flip_done timed out
```

**Full dmesg/syslog available on request.**

---

## **Workarounds**

* **Disabling hardware video encoding (forcing Sunshine to use software encoder, `libx264`)** eliminates the crash entirely, but at the cost of high CPU use.
* Running only AI or only streaming is stable; running both with hardware encoding = crash.
* Latest firmware, kernel, ROCm, PyTorch (all ROCm 7.1 matched) — no change.
* All kernel tuning and `iommu`/`amdgpu` GRUB parameters tested — no improvement.

---

## **Impact**

* **Cannot use Strix Halo iGPU for simultaneous AI and hardware-accelerated game/desktop streaming**
* **Blocks advanced multi-modal workloads (AI + AV/streaming)**
* **Major regression vs. expectations for top-end APU**

> **Again, note:**
> Running **Shadow of the Tomb Raider benchmark** **at the same time as Gemma3:27B/Open-WebUI** works fine—no crash.
> **The crash is uniquely triggered by AI + hardware video encoding via Sunshine.**

---

## **What Help Do I Need?**

* **Bug acknowledgement**
* **Instructions for advanced debug tracing if needed**
* **ETA for fix in ROCm/amdgpu/firmware**
* **Beta firmware or kernel to try**

---

## **Environment Details**

```
Device: Evo-x2 AI Max 395+ (Strix Halo, Ryzen AI Max 395+)
RAM: 128GB
OS: Ubuntu 24.04 OEM
Kernel: 6.14.0-1015-oem
ROCm: 7.1.0
firmware: [EDIT: paste output of `apt show linux-firmware`]
PyTorch: 2.8.0+rocm7.1.0
Ollama: [latest ROCm backend]
Sunshine: 2025.924.154138 commit: 86188d47a7463b0f73b35de18a628353adeaa20e
```

---

## **Attachments**

* [Include full dmesg/syslog excerpts as files, or provide a pastebin link.]

---

**Thank you! If you need extra logs, traces, or want me to test a patch, I’m happy to help.**

---

Let me know if you want it as a Markdown file or with any other formatting!
This is the ideal format to post on [[ROCm GitHub Issues](https://github.com/RadeonOpenCompute/ROCm/issues)](https://github.com/RadeonOpenCompute/ROCm/issues) or the AMD Community forums.

### Operating System

Ubuntu 24.04 OEM

### CPU

Ryzen AI Max 395+

### GPU

Integrated Radeon 8060s

### ROCm Version

ROCm 7.1.25424-4179531dcd

### ROCm Component

_No response_

### Steps to Reproduce

## **How to Reproduce**

1. Boot Ubuntu 24.04 OEM on Evo-x2 AI Max 395+ (Strix Halo)
2. Confirm ROCm stack (`hipconfig`, `rocminfo`) is working and AI workloads are stable.
3. Start **Ollama** or Open-WebUI and run a large language model (**Gemma3:27B**, with 80+ layers on GPU, batch size 256, ROCm backend).
4. While the AI workload is running, start **Sunshine** and connect a streaming client (default encoder, or VPE hardware encoder).
5. Within minutes (sometimes hour), the system hangs/crashes. Graphics session dies; must restart.


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
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
      Size:                    32486536(0x1efb488) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32486536(0x1efb488) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32486536(0x1efb488) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32486536(0x1efb488) KB             
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
  Name:                    aie2                               
  Uuid:                    AIE-XX                             
  Marketing Name:          AIE-ML                             
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
      Size:                    32486536(0x1efb488) KB             
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
      Size:                    32486536(0x1efb488) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***
```

### Additional Information

Workarounds

Disabling hardware video encoding (forcing Sunshine to use software encoder, libx264) eliminates the crash entirely, but at the cost of high CPU use.

Running only AI or only streaming is stable; running both with hardware encoding = crash.

Latest firmware, kernel, ROCm, PyTorch (all ROCm 7.1 matched) — no change.

All kernel tuning and iommu/amdgpu GRUB parameters tested — no improvement.

Attached the output of: `journalctl -b -1 | grep -Ei "amdgpu|rocm|gpu|error" | tee journal_grepped.txt`

[journal_grepped.txt](https://github.com/user-attachments/files/23537090/journal_grepped.txt)

---

## 评论 (19 条)

### 评论 #1 — ianbmacdonald (2025-11-15T02:02:13Z)

Looks very similar too #5590 and #5151 where increasing the workload can generate `amdgpu: MES failed to respond to msg=REMOVE_QUEUE`

---

### 评论 #2 — mixer3d (2025-11-19T21:59:10Z)

just found this by accident, did you tried to upgrade kernel? @kickinz1 try at least 6.16.x which introduced improvements for AMD APU's... i see you have an issue on ubuntu: so try something from here, there are 6.17.x already, and rc for 6.18 https://kernel.ubuntu.com/mainline/

---

### 评论 #3 — adityas-amd (2025-12-01T05:29:23Z)

@kickinz1 could you please try therock latest nightlies and 6.18-rc6 kernel 
ROCm PR that was merged into the develop branch: https://github.com/ROCm/rocm-systems/pull/1807 (already in nightlies)
kernel 6.18-rc6 includes the commit https://github.com/torvalds/linux/commit/d15deafab5d722afb9e2f83c5edcdef9d9d98bd1


---

### 评论 #4 — kickinz1 (2025-12-01T07:47:54Z)

I will and report here.

Le 1 décembre 2025 06:29:46 GMT+01:00, Aditya Srichandan ***@***.***> a écrit :
>adityas-amd left a comment (ROCm/ROCm#5665)
>
>@kickinz1 could you please try therock latest nightlies and 6.18-rc6 kernel 
>ROCm PR that was merged into the develop branch: https://github.com/ROCm/rocm-systems/pull/1807 (already in nightlies)
>kernel 6.18-rc6 includes the commit https://github.com/torvalds/linux/commit/d15deafab5d722afb9e2f83c5edcdef9d9d98bd1
>
>
>-- 
>Reply to this email directly or view it on GitHub:
>https://github.com/ROCm/ROCm/issues/5665#issuecomment-3594601624
>You are receiving this because you were mentioned.
>
>Message ID: ***@***.***>

---

### 评论 #5 — adityas-amd (2026-01-13T14:18:13Z)

@kickinz1 is the issue resolved now?

---

### 评论 #6 — zw963 (2026-01-13T16:56:28Z)

I use 780M,  the MES crash frequency has dropped a lot.

Following is all my package version, I use Arch Linux.

```
amd-ucode 20260110-1
amdgpu_top-git 0.11.0.r24.gcb0d967-1
hip-runtime-amd 7.1.1-1
lib32-vulkan-amdgpu-pro 25.10_2202160-1
linux-amd-drm-fixes 6.19.2026.01.06-1
linux-amd-drm-fixes-headers 6.19.2026.01.06-1
linux-amd-drm-next 6.20.2026.01.09-1
linux-amd-drm-next-headers 6.20.2026.01.09-1
linux-firmware-amdgpu 20260110-1
ollama-rocm 0.13.5-1
python-pytorch-rocm 2.9.1-7
rocm-cmake 7.1.1-1
rocm-core 7.1.1-1
rocm-device-libs 2:7.1.1-2
rocm-hip-libraries 7.1.1-1
rocm-hip-runtime 7.1.1-1
rocm-hip-sdk 7.1.1-1
rocm-language-runtime 7.1.1-1
rocm-llvm 2:7.1.1-2
rocm-opencl-runtime 7.1.1-1
rocm-opencl-sdk 7.1.1-1
rocm-smi-lib 7.1.1-1
rocminfo 7.1.1-1
vulkan-amdgpu-pro 25.10_2202160-1
xf86-video-amdgpu 25.0.0-1
```

I current use `linux-amd-drm-fixes`  kernel.

```
 ╰──➤ $ \cat /proc/cmdline
root=LABEL=ArchLinux rw initrd=boot\amd-ucode.img resume=LABEL=swap sysrq_always_enabled=1 amdgpu.gpu_recovery=1 initrd=\boot\initramfs-linux-amd-drm-fixes.img
```



---

### 评论 #7 — adityas-amd (2026-01-19T00:24:30Z)

We can close this issue now as it is fixed. @kickinz1 feel free to reopen if you see any other issues.

---

### 评论 #8 — zw963 (2026-01-19T14:03:12Z)

Hi, @adityas-amd , MES hung issue still happen on my 7840hs's 780M, as the env describe in https://github.com/ROCm/ROCm/issues/5665#issuecomment-3745400015.

---

### 评论 #9 — darkbasic (2026-01-19T14:20:52Z)

@zw963 you're not using ROCM 7.2+ so that's expected.

---

### 评论 #10 — zw963 (2026-02-03T13:16:17Z)

Hello, I am trying to run ComfyUI use 6.18.8 kernal with rOCm 7.2.0 use 780M, but still system crash (iGpu reset) and force login out if remove `amdgpu.cwsr_enable=0` 

```
 ╰──➤ $ uname -a
Linux mingfan 6.18.8-x64v3-xanmod1-1 #1 SMP PREEMPT_DYNAMIC Sat, 31 Jan 2026 05:51:47 +0000 x86_64 GNU/Linux
```

```
 ╰──➤ $ \cat /proc/cmdline
root=LABEL=ArchLinux rw initrd=boot\amd-ucode.img resume=LABEL=swap sysrq_always_enabled=1 amdgpu.gpu_recovery=1 amdgpu.gttsize=24576 ttm.pages_limit=6291456 initrd=\boot\initramfs-linux-xanmod.img
```

Following is the dmesg broken log:

```
[  292.487846] userif-5: sent link down event.
[  292.487856] userif-5: sent link up event.
[  950.818166] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  950.818171] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1802
[  950.818174] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[  950.818177] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[  950.818179] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[  950.818199] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[  950.818212] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 5
[  950.818215] amdgpu: Failed to suspend process pid 14368
[  950.818218] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 64667
[  950.818245] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[  950.820337] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[  952.916113] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  952.916120] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[  953.391196] amdgpu: Freeing queue vital buffer 0x7f2e70800000, queue evicted
[  953.391202] amdgpu: Freeing queue vital buffer 0x7f2e9da00000, queue evicted
[  953.391204] amdgpu: Freeing queue vital buffer 0x7f340c400000, queue evicted
[  953.391207] amdgpu: Freeing queue vital buffer 0x7f340fa00000, queue evicted
[  953.391209] amdgpu: Freeing queue vital buffer 0x7f3414400000, queue evicted
[  954.920081] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  954.920088] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[  956.924070] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  956.924077] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[  957.131282] [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[  957.132772] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[  957.165393] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[  957.166061] [drm] PCIE GART of 512M enabled (table at 0x000000807FD00000).
[  957.166190] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[  957.166192] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[  957.166195] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[  957.167841] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[  957.173995] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[  957.296277] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  957.296286] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  957.296288] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  957.296290] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  957.296291] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  957.296293] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  957.296294] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  957.296295] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  957.296297] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  957.296300] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  957.296301] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[  957.296303] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[  957.296305] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[  957.298461] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[  957.298474] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[  958.892620] rfkill: input handler enabled
[  959.357038] userif-5: sent link down event.
[  959.357044] userif-5: sent link up event.
[  961.343114] amdgpu: Freeing queue vital buffer 0x7f4e7ca00000, queue evicted
[  961.343128] amdgpu: Freeing queue vital buffer 0x7f4ec8600000, queue evicted
[  961.343133] amdgpu: Freeing queue vital buffer 0x7f4f03600000, queue evicted
[  961.343135] amdgpu: Freeing queue vital buffer 0x7f4f04400000, queue evicted
[  961.480700] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  961.480930] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1800
[  961.481136] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[  961.481177] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[  961.481200] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[  961.481201] amdgpu: Resetting wave fronts (cpsch) on dev 000000000ff73c32
[  961.481203] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[  961.481250] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[  961.484928] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[  961.583988] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[  961.617548] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[  961.618214] [drm] PCIE GART of 512M enabled (table at 0x000000807FD00000).
```

Following is new installed rocm related package version:


```
composable-kernel-7.2.0-1-x86_64 1557.0 MiB 16.6 MiB/s 01:34 [###########################################] 100%
hipblaslt-7.2.0-1-x86_64 1525.6 MiB 12.7 MiB/s 02:01 [###########################################] 100%
rocm-llvm-2:7.2.0-1-x86_64 956.8 MiB 14.0 MiB/s 01:08 [###########################################] 100%
rocsolver-7.2.0-1-x86_64 690.6 MiB 17.9 MiB/s 00:39 [###########################################] 100%
rccl-7.2.0-1-x86_64 423.2 MiB 18.8 MiB/s 00:22 [###########################################] 100%
rocblas-7.2.0-1-x86_64 331.3 MiB 16.7 MiB/s 00:20 [###########################################] 100%
miopen-hip-7.2.0-1-x86_64 251.1 MiB 17.2 MiB/s 00:15 [###########################################] 100%
rocfft-7.2.0-1-x86_64 120.8 MiB 17.4 MiB/s 00:07 [###########################################] 100%
rocsparse-7.2.0-1-x86_64 72.1 MiB 16.2 MiB/s 00:04 [###########################################] 100%
comgr-2:7.2.0-1-x86_64 42.1 MiB 16.5 MiB/s 00:03 [###########################################] 100%
hipsparselt-7.2.0-1-x86_64 41.6 MiB 18.5 MiB/s 00:02 [###########################################] 100%
rocrand-7.2.0-1-x86_64 22.5 MiB 15.9 MiB/s 00:01 [###########################################] 100%
rocalution-7.2.0-1-x86_64 8.3 MiB 19.2 MiB/s 00:00 [###########################################] 100%
hip-runtime-amd-7.2.0-1-x86_64 7.3 MiB 20.1 MiB/s 00:00 [###########################################] 100%
rocm-smi-lib-7.2.0-1-x86_64 1052.3 KiB 1253 KiB/s 00:01 [###########################################] 100%
hsa-rocr-7.2.0-1-x86_64 856.7 KiB 1727 KiB/s 00:00 [###########################################] 100%
rocm-opencl-runtime-7.2.0-1-x86_64 580.5 KiB 2044 KiB/s 00:00 [###########################################] 100%
rocm-device-libs-2:7.2.0-1-x86_64 537.9 KiB 2.29 MiB/s 00:00 [###########################################] 100%
roctracer-7.2.0-2-x86_64 526.5 KiB 2.62 MiB/s 00:00 [###########################################] 100%
rocthrust-7.2.0-1-x86_64 426.2 KiB 2.42 MiB/s 00:00 [###########################################] 100%
rocprim-7.2.0-1-any 307.8 KiB 2.21 MiB/s 00:00 [###########################################] 100%
hipblas-7.2.0-1-x86_64 165.5 KiB 1724 KiB/s 00:00 [###########################################] 100%
hipsparse-7.2.0-1-x86_64 116.3 KiB 1264 KiB/s 00:00 [###########################################] 100%
rocprofiler-register-7.2.0-1-x86_64 105.4 KiB 1054 KiB/s 00:00 [###########################################] 100%
hipcub-7.2.0-1-x86_64 93.8 KiB 1117 KiB/s 00:00 [###########################################] 100%
hipsolver-7.2.0-1-x86_64 83.1 KiB 989 KiB/s 00:00 [###########################################] 100%
hipfft-7.2.0-1-x86_64 66.1 KiB 870 KiB/s 00:00 [###########################################] 100%
rocm-core-7.2.0-1-x86_64 29.5 KiB 388 KiB/s 00:00 [###########################################] 100%
rocminfo-7.2.0-1-x86_64 28.8 KiB 400 KiB/s 00:00 [###########################################] 100%
hiprand-7.2.0-1-x86_64 28.6 KiB 376 KiB/s 00:00 [###########################################] 100%
rocm-cmake-7.2.0-1-any 28.1 KiB 369 KiB/s 00:00 [###########################################] 100%
hipblas-common-7.2.0-1-any 8.1 KiB 107 KiB/s 00:00 [###########################################] 100%
rocm-hip-sdk-7.2.0-1-any 2.2 KiB 30.8 KiB/s 00:00 [###########################################] 100%
rocm-hip-libraries-7.2.0-1-any 2.2 KiB 24.9 KiB/s 00:00 [###########################################] 100%
rocm-hip-runtime-7.2.0-1-any 2.1 KiB 31.5 KiB/s 00:00 [###########################################] 100%
rocm-opencl-sdk-7.2.0-1-any 2.1 KiB 26.6 KiB/s 00:00 [###########################################] 100%
rocm-language-runtime-7.2.0-1-any 2.1 KiB 27.8 KiB/s 00:00 [###########################################] 100%
```

---

### 评论 #11 — zw963 (2026-02-03T13:26:12Z)

ping @adityas-amd @darkbasic 

---

### 评论 #12 — zw963 (2026-02-03T14:01:45Z)

I tested on 6.12 lts kernel, no luck.

```
 ╰──➤ $ uname -a
Linux mingfan 6.12.68-1-lts #1 SMP PREEMPT_DYNAMIC Fri, 30 Jan 2026 11:42:40 +0000 x86_64 GNU/Linux
```

<img width="1812" height="1006" alt="Image" src="https://github.com/user-attachments/assets/ebb52d15-a91c-4189-a9b9-d96e31ef4d31" />

---

### 评论 #13 — darkbasic (2026-02-03T14:07:30Z)

@zw963 I gave up a long time ago with my 780M, fortunately with Strix Halo the ROCm support is in a much better shape. If I recall correctly there are patched ROCm packages on the AUR (Arch User Repository) with additional patches for gfx1103: https://aur.archlinux.org/packages?O=0&SeB=nd&K=gfx1103&outdated=&SB=p&SO=d&PP=50&submit=Go
You might also try `HSA_OVERRIDE_GFX_VERSION=11.0.0` but I wouldn't expect much: AMD skipped their homeworks for 780M.

---

### 评论 #14 — zw963 (2026-02-04T13:22:08Z)

Following is the summary by GPT:

On gfx1103 (780M iGPU), KFD queue eviction/removal triggers MES firmware path; MES stops responding to REMOVE_QUEUE, leading to failed eviction and GPU reset/logout. Workarounds: keep amdgpu.cwsr_enable=0; optionally test amdgpu.mes=0. There is an LKML patch specifically for gfx1103 iGPU removing evict/restore calls to MES.

---

### 评论 #15 — zw963 (2026-02-04T13:23:36Z)

> You might also try `HSA_OVERRIDE_GFX_VERSION=11.0.0` but I wouldn't expect much

Okay, thanks, although, not set this env, ollama still can use GPU 100% on my arch.

---

### 评论 #16 — zw963 (2026-02-23T18:42:03Z)

@darkbasic , 780M get fixed now, tested on my arch linux.

check https://github.com/ROCm/ROCm/issues/5180#issuecomment-3946430208

---

### 评论 #17 — darkbasic (2026-02-23T18:52:19Z)

@zw963 good to know, thanks. Can you please share how you got it working?

---

### 评论 #18 — zw963 (2026-02-24T07:54:45Z)

> [@zw963](https://github.com/zw963) good to know, thanks. Can you please share how you got it working?

It's just working after recent update, I even don't know when this MES hang issue gone.

I tested this before use ComfulUI, it always broken if not set amdgpu.cwsr_enable=0, so, I set it and  deleted it several weeks ago, I use the qwen3:30b large model for translation every day on my local machine, but I don't remember when I switch back to not disable cwsr version kernel boot cmdline(I have many option, probably select wrong), I just realized that I've been using qwen3:30b for translation, and it's never crashed as before.

Then, I use gpt 5.2 write a test bash script, and run it ten minutes, no crash!

<details>
<summary>ollama_rocm_hang_tester.sh</summary>

```
#!/usr/bin/env bash
set -euo pipefail

# =========================
# Ollama ROCm hang/reset tester
# - Stress GPU via long generations
# - Watch kernel logs for amdgpu/MES/reset/timeout keywords
# - Stop immediately on first HIT and save evidence
#
# Usage:
#   sudo ./ollama_rocm_hang_tester.sh [MODEL] [OUTDIR] [LOOPS]
#
# Env overrides:
#   NUM_PREDICT=4096 CTX=8192 TIMEOUT_SEC=600 SLEEP_BETWEEN=1 \
#   PATTERN='...' OLLAMA_HOST='http://127.0.0.1:11434' \
#   sudo ./ollama_rocm_hang_tester.sh gemma3:27b-it-qat ./logs 200
# =========================

MODEL="${1:-qwen3:30b-instruct}"
OUTDIR="${2:-./ollama_rocm_hang_logs}"
LOOPS="${3:-200}"

NUM_PREDICT="${NUM_PREDICT:-2048}"     # more = more stress
CTX="${CTX:-4096}"                     # context
TIMEOUT_SEC="${TIMEOUT_SEC:-300}"      # per-iteration timeout seconds
SLEEP_BETWEEN="${SLEEP_BETWEEN:-1}"    # sleep between iterations
OLLAMA_HOST="${OLLAMA_HOST:-http://127.0.0.1:11434}"

# Kernel keywords that usually appear when GPU hangs/resets
PATTERN="${PATTERN:-amdgpu|MES|mes|ring .*timeout|gpu reset|GPU reset|job timed out|amdgpu_job_timedout|ASIC reset|resetting gpu|recovering|GFX timeout|VRAM lost|RAS|ras|Xid|fault|hang}"

# -------------------------
# Init
# -------------------------
mkdir -p "$OUTDIR"
TS="$(date +%F_%H-%M-%S)"
RUN_DIR="$OUTDIR/$TS"
mkdir -p "$RUN_DIR"

echo "[i] Model        : $MODEL"
echo "[i] Output dir   : $RUN_DIR"
echo "[i] Loops        : $LOOPS"
echo "[i] num_predict  : $NUM_PREDICT"
echo "[i] ctx          : $CTX"
echo "[i] timeout/iter : ${TIMEOUT_SEC}s"
echo "[i] ollama host  : $OLLAMA_HOST"
echo "[i] pattern      : $PATTERN"
echo

# Check Ollama API
if ! curl -fsS "$OLLAMA_HOST/api/tags" >/dev/null; then
  echo "[!] Cannot reach Ollama API at $OLLAMA_HOST"
  echo "    Start it with: ollama serve"
  exit 2
fi

# Save basic system info
{
  echo "=== date ==="; date -Is
  echo
  echo "=== uname ==="; uname -a
  echo
  echo "=== lspci (VGA/3D) ==="; lspci -nn | grep -Ei 'vga|display|3d' || true
  echo
  echo "=== ollama version ==="; ollama --version 2>/dev/null || true
  echo
  echo "=== ollama tags ==="
  curl -sS "$OLLAMA_HOST/api/tags" | head -c 20000 || true
  echo
} > "$RUN_DIR/system_info.txt" 2>&1

START_ISO="$(date -Is)"
echo "[i] Kernel log baseline time: $START_ISO" | tee "$RUN_DIR/baseline.txt"

HIT_FILE="$RUN_DIR/HIT_DETECTED.txt"
KLOG_FILE="$RUN_DIR/kernel_follow.log"

# Prompt designed to force long output (stable stress)
PROMPT_FILE="$RUN_DIR/prompt.txt"
cat > "$PROMPT_FILE" <<'EOF'
你现在是一个“随机数据生成器”。请严格输出 1 到 4096 的编号行，每行格式如下：
<编号>\t<32个十六进制字符>\t<32个十六进制字符>\t<32个十六进制字符>
要求：
- 只输出这些行，不要解释，不要额外空行。
- 32个十六进制字符必须是小写 [0-9a-f]。
EOF

# Background watcher: follow kernel log, grep keywords, stop on first match
echo "[i] Starting kernel log watcher..."
(
  journalctl -k -f -o short-iso --since "now" 2>/dev/null \
  | tee -a "$KLOG_FILE" \
  | grep -Eai --line-buffered "$PATTERN" \
  | while read -r line; do
      {
        echo "=== HIT DETECTED @ $(date -Is) ==="
        echo "$line"
        echo "=== See full kernel_follow.log for more context ==="
      } | tee "$HIT_FILE" >/dev/null
      exit 0
    done
) &
WATCHER_PID=$!
echo "$WATCHER_PID" > "$RUN_DIR/watcher.pid"

cleanup() {
  if kill -0 "$WATCHER_PID" >/dev/null 2>&1; then
    kill "$WATCHER_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

# Helper: JSON-escape prompt using python (no jq dependency)
json_escape_file() {
  local file="$1"
  python -c 'import json,sys; print(json.dumps(sys.stdin.read()))' < "$file"
}

FAIL_COUNT=0
echo "[i] Starting stress loop..."

for i in $(seq 1 "$LOOPS"); do
  ITER_DIR="$RUN_DIR/iter_$(printf "%04d" "$i")"
  mkdir -p "$ITER_DIR"

  echo "[*] Iteration $i/$LOOPS ..."

  if [[ -f "$HIT_FILE" ]]; then
    echo "[!] Kernel HIT detected. Stop."
    break
  fi

  REQ_JSON="$ITER_DIR/request.json"
  RESP_BODY="$ITER_DIR/response_body.json"
  META_TXT="$ITER_DIR/meta.txt"
  HTTP_CODE_FILE="$ITER_DIR/http_code.txt"

  PROMPT_JSON="$(json_escape_file "$PROMPT_FILE")"

  cat > "$REQ_JSON" <<EOF
{
  "model": "$(printf "%s" "$MODEL")",
  "prompt": $PROMPT_JSON,
  "stream": false,
  "options": {
    "num_predict": $NUM_PREDICT,
    "num_ctx": $CTX,
    "temperature": 0
  }
}
EOF

  echo "start_iso=$(date -Is)" > "$META_TXT"
  T0="$(date +%s)"

  # Run request; always capture body + status code
  set +e
  timeout "$TIMEOUT_SEC" curl -sS \
    -H "Content-Type: application/json" \
    --data-binary @"$REQ_JSON" \
    -o "$RESP_BODY" -w "%{http_code}" \
    "$OLLAMA_HOST/api/generate" \
    > "$HTTP_CODE_FILE"
  CURL_RC=$?
  set -e

  T1="$(date +%s)"
  DUR=$((T1 - T0))
  HTTP_CODE="$(cat "$HTTP_CODE_FILE" 2>/dev/null || echo "")"

  {
    echo "duration_sec=$DUR"
    echo "curl_rc=$CURL_RC"
    echo "http_code=$HTTP_CODE"
  } >> "$META_TXT"

  # Determine failure
  FAILED=0
  if [[ $CURL_RC -ne 0 ]]; then
    FAILED=1
  elif [[ "$HTTP_CODE" != "200" ]]; then
    FAILED=1
  fi

  if [[ $FAILED -eq 1 ]]; then
    echo "[!] Iteration $i failed (curl_rc=$CURL_RC http=$HTTP_CODE dur=${DUR}s)"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "FAIL_ITER=$i curl_rc=$CURL_RC http=$HTTP_CODE dur=${DUR}s" >> "$RUN_DIR/fail_summary.txt"

    # Snapshot recent kernel log since baseline (tail) for quick view
    journalctl -k -o short-iso --since "$START_ISO" | tail -n 300 > "$ITER_DIR/kernel_tail_300.log" 2>/dev/null || true

    # If kernel watcher already hit, stop now
    if [[ -f "$HIT_FILE" ]]; then
      echo "[!] Kernel HIT detected. Stop."
      break
    fi

    # Stop after too many failures (prevents endless spam)
    if [[ $FAIL_COUNT -ge 3 ]]; then
      echo "[!] Too many failures ($FAIL_COUNT). Stop."
      break
    fi
  fi

  if [[ -f "$HIT_FILE" ]]; then
    echo "[!] Kernel HIT detected. Stop."
    break
  fi

  sleep "$SLEEP_BETWEEN"
done

echo
echo "========== SUMMARY =========="
echo "[i] Logs: $RUN_DIR"
if [[ -f "$HIT_FILE" ]]; then
  echo "[!] RESULT: Kernel HIT detected (likely amdgpu/MES hang/reset/timeout)."
  echo "    See: $HIT_FILE"
  exit 10
fi
if [[ -f "$RUN_DIR/fail_summary.txt" ]]; then
  echo "[!] RESULT: Request failures occurred (see fail_summary.txt), but no kernel HIT matched pattern."
  echo "    You can widen PATTERN to catch your exact dmesg strings."
  exit 11
fi
echo "[+] RESULT: No kernel HIT and no request failure within limits."
exit 0
```

</details>

Maybe you could give ComfyUI a try.



---

### 评论 #19 — zw963 (2026-03-04T14:51:46Z)

probably still not fixed on 780M?

```
[73314.889668] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73314.889675] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[73314.889677] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[73314.889681] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[73314.889682] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[73314.889684] amdgpu: Failed to quiesce KFD
[73314.889701] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[73314.891684] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 49700
[73314.891708] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[73314.893432] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[73316.994500] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73316.994507] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[73318.998481] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73318.998487] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[73318.999856] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[73319.031470] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[73319.031938] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[73319.032193] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[73319.032198] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[73319.032202] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[73319.033702] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[73319.039404] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[73319.185138] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[73319.185150] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[73319.185153] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[73319.185155] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[73319.185157] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[73319.185158] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[73319.185160] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[73319.185162] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[73319.185163] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[73319.185165] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[73319.185167] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[73319.185169] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[73319.185171] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[73319.187263] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[73319.187276] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[73327.541061] amdgpu: Freeing queue vital buffer 0x7f2e27400000, queue evicted
[73327.541067] amdgpu: Freeing queue vital buffer 0x7f3041200000, queue evicted
[73327.541070] amdgpu: Freeing queue vital buffer 0x7f3047400000, queue evicted
[73327.541071] amdgpu: Freeing queue vital buffer 0x7f3047a00000, queue evicted
[73327.541075] amdgpu: Freeing queue vital buffer 0x7f3196600000, queue evicted
[73327.649199] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73327.649205] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[73327.649207] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[73327.649211] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[73327.649212] amdgpu: Resetting wave fronts (cpsch) on dev 0000000058c303b6
[73327.649214] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[73327.649214] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[73327.649312] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[73327.652804] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[73327.758867] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[73327.793270] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[73327.793923] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[73327.793983] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[73327.793985] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[73327.793988] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[73327.796093] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[73327.803519] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[73328.541797] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[73328.541804] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[73328.541807] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[73328.541808] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[73328.541810] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[73328.541811] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[73328.541813] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[73328.541814] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[73328.541815] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[73328.541817] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[73328.541819] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[73328.541820] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[73328.541822] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[73328.543914] amdgpu 0000:c5:00.0: amdgpu: GPU reset(2) succeeded!
[73328.543927] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
```

---
