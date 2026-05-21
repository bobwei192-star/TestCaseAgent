# [Issue]: MI300x GPUs not recognized (amdgpu: get invalid ip discovery binary signature)

> **Issue #4454**
> **状态**: closed
> **创建时间**: 2025-03-06T16:56:35Z
> **更新时间**: 2025-04-03T07:15:45Z
> **关闭时间**: 2025-03-13T19:59:23Z
> **作者**: lschoepps
> **标签**: Under Investigation, AMD Instinct MI300X, ROCm 6.3.3
> **URL**: https://github.com/ROCm/ROCm/issues/4454

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 6.3.3** (颜色: #aaaaaa)

## 描述

### Problem Description

MI300x GPUs are not recognized at boot with the notable error message "amdgpu: get invalid ip discovery binary signature". 

The machine is a Dell PowerEdge XE9680 with 8 AMD Instinct MI300X. We tried a few different setups (ubuntu 22.04, debian 12, rocm 6.2, firmware updates) to no avail.

For example with a clean install of Ubuntu 24.04 and rocm 6.3.3:
```
apt install -y "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
apt install -y python3-setuptools python3-wheel
wget https://repo.radeon.com/amdgpu-install/6.3.3/ubuntu/noble/amdgpu-install_6.3.60303-1_all.deb
apt install -y ./amdgpu-install_6.3.60303-1_all.deb
apt update
amdgpu-install -y --usecase=dkms,rocmdev
apt upgrade
```

Then at boot we have the following errors:
```
[   37.766927] [drm] amdgpu kernel modesetting enabled.
[   37.773237] scsi host16: usb-storage 1-10.4.2:1.0
[   37.777979] [drm] amdgpu version: 6.10.5
[   37.777980] [drm] OS DRM version: 6.8.0
[   37.778379] amdgpu: Virtual CRAT table created for CPU
[   37.782810] usbcore: registered new interface driver usb-storage
[   37.786670] amdgpu: Topology: Add CPU node
[   37.807233] usbcore: registered new interface driver uas
[   37.810294] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A1 0x1002:0x74A1 0x00).
[   37.822558] [drm] register mmio base: 0x96200000
[   37.827694] [drm] register mmio size: 2097152
[   37.863386] mlx5_core 0000:9e:00.0: MLX5E: StrdRq(1) RqSz(8) StrdSz(2048) RxCqeCmprss(0 enhanced)
[   37.890008] mlx5_core 0000:9e:00.0: is_dpll_supported:213:(pid 1313): Missing SyncE capability
[   37.918937] mlx5_core 0000:9e:00.0 enp158s0np0: renamed from eth0
[   37.957063] MACsec IEEE 802.1AE
[   38.827427] scsi 16:0:0:0: CD-ROM            Linux    Virtual CD/DVD   0001 PQ: 0 ANSI: 0
[   38.838590] sr 16:0:0:0: Power-on or device reset occurred
[   39.080489] sr 16:0:0:0: [sr0] scsi-1 drive
[   39.085419] cdrom: Uniform CD-ROM driver Revision: 3.20
[   39.332858] sr 16:0:0:0: Attached scsi generic sg4 type 5
[   40.890184] amdgpu 0000:1b:00.0: amdgpu: get invalid ip discovery binary signature
[   42.114302] [drm:amdgpu_discovery_set_ip_blocks [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   42.124800] amdgpu 0000:1b:00.0: amdgpu: Fatal error during GPU init
[   42.150575] amdgpu 0000:1b:00.0: amdgpu: amdgpu: finishing device.
[   42.157273] amdgpu: probe of 0000:1b:00.0 failed with error -22
[   42.177011] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A1 0x1002:0x74A1 0x00).
[   42.186395] [drm] register mmio base: 0xA8A00000
[   42.191236] [drm] register mmio size: 2097152
[   45.216954] amdgpu 0000:3d:00.0: amdgpu: get invalid ip discovery binary signature
[   46.441299] [drm:amdgpu_discovery_set_ip_blocks [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   46.451754] amdgpu 0000:3d:00.0: amdgpu: Fatal error during GPU init
[   46.478632] amdgpu 0000:3d:00.0: amdgpu: amdgpu: finishing device.
[   46.485328] amdgpu: probe of 0000:3d:00.0 failed with error -22
[   46.504007] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A1 0x1002:0x74A1 0x00).
[   46.513410] [drm] register mmio base: 0xB1200000
[   46.518259] [drm] register mmio size: 2097152
[   49.543949] amdgpu 0000:4e:00.0: amdgpu: get invalid ip discovery binary signature
[   50.765299] [drm:amdgpu_discovery_set_ip_blocks [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   50.775815] amdgpu 0000:4e:00.0: amdgpu: Fatal error during GPU init
[   50.801011] amdgpu 0000:4e:00.0: amdgpu: amdgpu: finishing device.
[   50.807796] amdgpu: probe of 0000:4e:00.0 failed with error -22
[   50.824520] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A1 0x1002:0x74A1 0x00).
[   50.850925] [drm] register mmio base: 0xB9A00000
[   50.855796] [drm] register mmio size: 2097152
[   53.876773] amdgpu 0000:5f:00.0: amdgpu: get invalid ip discovery binary signature
[   54.198293] amdgpu 0000:5f:00.0: amdgpu: socket: 2, aid: 0, fw_status: 0xe6985b2d, firmware load failed at boot time
[   54.523298] amdgpu 0000:5f:00.0: amdgpu: socket: 2, aid: 1, fw_status: 0xe6985b2d, firmware load failed at boot time
[   54.848298] amdgpu 0000:5f:00.0: amdgpu: socket: 2, aid: 2, fw_status: 0xe6985d2d, firmware load failed at boot time
[   55.173298] amdgpu 0000:5f:00.0: amdgpu: socket: 2, aid: 3, fw_status: 0xe6985b2d, firmware load failed at boot time
[   55.184658] [drm:amdgpu_discovery_set_ip_blocks [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   55.195208] amdgpu 0000:5f:00.0: amdgpu: Fatal error during GPU init
[   55.218851] amdgpu 0000:5f:00.0: amdgpu: amdgpu: finishing device.
[   55.241502] amdgpu: probe of 0000:5f:00.0 failed with error -22
[   55.248363] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A1 0x1002:0x74A1 0x00).
[   55.258464] [drm] register mmio base: 0xD2A00000
[   55.264266] [drm] register mmio size: 2097152
[   58.274047] amdgpu 0000:9d:00.0: amdgpu: get invalid ip discovery binary signature
[   59.496299] [drm:amdgpu_discovery_set_ip_blocks [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   59.506916] amdgpu 0000:9d:00.0: amdgpu: Fatal error during GPU init
[   59.530656] amdgpu 0000:9d:00.0: amdgpu: amdgpu: finishing device.
[   59.537391] amdgpu: probe of 0000:9d:00.0 failed with error -22
[   59.554167] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A1 0x1002:0x74A1 0x00).
[   59.579911] [drm] register mmio base: 0xDEA00000
[   59.584836] [drm] register mmio size: 2097152
[   62.606117] amdgpu 0000:bd:00.0: amdgpu: get invalid ip discovery binary signature
[   63.831299] [drm:amdgpu_discovery_set_ip_blocks [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   63.841805] amdgpu 0000:bd:00.0: amdgpu: Fatal error during GPU init
[   63.866296] amdgpu 0000:bd:00.0: amdgpu: amdgpu: finishing device.
[   63.872947] amdgpu: probe of 0000:bd:00.0 failed with error -22
[   63.892500] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A1 0x1002:0x74A1 0x00).
[   63.901926] [drm] register mmio base: 0xE7A00000
[   63.906795] [drm] register mmio size: 2097152
[   66.931096] amdgpu 0000:cd:00.0: amdgpu: get invalid ip discovery binary signature
[   68.153300] [drm:amdgpu_discovery_set_ip_blocks [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   68.163763] amdgpu 0000:cd:00.0: amdgpu: Fatal error during GPU init
[   68.189328] amdgpu 0000:cd:00.0: amdgpu: amdgpu: finishing device.
[   68.195961] amdgpu: probe of 0000:cd:00.0 failed with error -22
[   68.215793] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A1 0x1002:0x74A1 0x00).
[   68.225225] [drm] register mmio base: 0xF0A00000
[   68.230090] [drm] register mmio size: 2097152
[   71.255872] amdgpu 0000:dd:00.0: amdgpu: get invalid ip discovery binary signature
[   72.478298] [drm:amdgpu_discovery_set_ip_blocks [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   72.488834] amdgpu 0000:dd:00.0: amdgpu: Fatal error during GPU init
[   72.514522] amdgpu 0000:dd:00.0: amdgpu: amdgpu: finishing device.
[   72.521195] amdgpu: probe of 0000:dd:00.0 failed with error -22
```
```
lspci -k | grep -i amd
19:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 1500
        Subsystem: Advanced Micro Devices, Inc. [AMD] Device 1500
1a:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
1b:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Kernel modules: amdgpu
3b:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 1500
        Subsystem: Advanced Micro Devices, Inc. [AMD] Device 1500
3c:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
3d:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Kernel modules: amdgpu
4c:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 1500
        Subsystem: Advanced Micro Devices, Inc. [AMD] Device 1500
4d:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
4e:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Kernel modules: amdgpu
5d:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 1500
        Subsystem: Advanced Micro Devices, Inc. [AMD] Device 1500
5e:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
5f:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Kernel modules: amdgpu
9b:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 1500
        Subsystem: Advanced Micro Devices, Inc. [AMD] Device 1500
9c:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
9d:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Kernel modules: amdgpu
bb:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 1500
        Subsystem: Advanced Micro Devices, Inc. [AMD] Device 1500
bc:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
bd:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Kernel modules: amdgpu
cb:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 1500
        Subsystem: Advanced Micro Devices, Inc. [AMD] Device 1500
cc:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
cd:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Kernel modules: amdgpu
db:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD] Device 1500
        Subsystem: Advanced Micro Devices, Inc. [AMD] Device 1500
dc:00.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Device 1501
dd:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
        Kernel modules: amdgpu
```

rocm-smi does not detect the GPUs

### Operating System

Ubuntu 24.04.2 LTS (Noble Numbat)

### CPU

2x Intel(R) Xeon(R) Platinum 8470

### GPU

8 x AMD Instinct MI300x

### ROCm Version

6.3.3

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

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
  Name:                    Intel(R) Xeon(R) Platinum 8470     
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Xeon(R) Platinum 8470     
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
  Max Clock Freq. (MHz):   3800                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            104                                
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    1056321436(0x3ef62f9c) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    1056321436(0x3ef62f9c) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    1056321436(0x3ef62f9c) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    1056321436(0x3ef62f9c) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    Intel(R) Xeon(R) Platinum 8470     
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Xeon(R) Platinum 8470     
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
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3800                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            104                                
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    1056915364(0x3eff3fa4) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    1056915364(0x3eff3fa4) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    1056915364(0x3eff3fa4) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    1056915364(0x3eff3fa4) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***

### Additional Information

Linux Kernel: 6.8.0-55-generic

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2025-03-06T19:00:30Z)

Hi @lschoepps. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — darren-amd (2025-03-10T18:17:12Z)

Hi @lschoepps,

Thanks for reporting the issue! Could you please provide the complete dump of `dmesg` for us to further investigate? Also, do you have an AMD FAE helping you out? It would be beneficial if we could connect to further assist with this issue, thanks!

---

### 评论 #3 — lschoepps (2025-03-11T10:09:22Z)

Hello, here is the complete dmesg output: [dmesg.txt](https://github.com/user-attachments/files/19180694/dmesg.txt)

We will have an AMD FAE coming this week on Thursday, I will ask him to contact you

---

### 评论 #4 — darren-amd (2025-03-13T19:59:23Z)

Hi @lschoepps,

I have been informed that this issue has been fixed and am going to close the ticket off. Please feel free to create another ticket if you run into any further issues, thanks!

---

### 评论 #5 — liyong (2025-04-03T06:10:14Z)

Hi @lschoepps,

Hey, we're having the same issue here. Is this a ROCm software thing? Or do we need to swap out some hardware parts?

---

### 评论 #6 — lschoepps (2025-04-03T07:15:44Z)

Hello, in our case we had to replace one of the GPU. There was some related errors in the Lifecycle logs of the idrac

---
