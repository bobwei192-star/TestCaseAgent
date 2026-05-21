# [Issue]: Ubuntu 22.04 fails to render login (sddm) in combination of ROCm 6.0.2 and Mesa 24.0.2 - no opengl?

> **Issue #2958**
> **状态**: closed
> **创建时间**: 2024-03-10T10:00:24Z
> **更新时间**: 2024-08-11T06:01:15Z
> **关闭时间**: 2024-03-19T00:50:03Z
> **作者**: smirgol
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/2958

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

I'm experiencing an issue with the combination of ROCm 6.0.2 and Mesa 24.0.2 installed from kisak ppa.
If both of these two are installed, after rebooting, the login (sddm / sddm-greeter) fails to render anything: I'm presented with a black screen and a flickering white bar at the top.

It seems to me that `opengl` isn't working, so while it is completing starting up processes in the background as usual, I cannot log in as the login screen can't be rendered. If I start X11 manually in the console using `startx`, the Desktop will start up as usually, but `glxinfo` will fail.

Now, if I either downgrade Mesa to stock Mesa or remove ROCm, everything is back to normal. I can use one of them, but not both at the same time. Actually I can install ROCm in addition to Mesa and as long as I don't reboot, both will work. It is only after rebooting, that things break. It used to work with ROCm 6.0 - I'm not sure which Mesa version I was using there, but after I've tried to upgrade to 6.0.2, and Ubuntu having also pushed the newer kernel meanwhile, it broke and I can't get it working again.

I've tried installing ROCm using the amdgpu-installer:
`amdgpu-install --usecase=hiplibsdk,rocm` - worked in the past

I've also tried installing it directly with the package manager:
`sudo apt install rocm6.0.2` - this installs less packages, e.g. no kernel module, but still breaks after rebooting

I have no idea what's going on and how to fix this, so I'd appreciate any help here.

### Operating System

Ubuntu 22.04.4 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 9 3900X 12-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

1. Install fresh Ubuntu 20.04.4 LTS with current HWE kernel `6.5.0-25-generic`.
2. Install Mesa 24.0.2 from kisak ppa `ppa:kisak/kisak-mesa`
3. Reboot
4. Login is broken

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
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
  Name:                    AMD Ryzen 9 3900X 12-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 3900X 12-Core Processor
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
  Max Clock Freq. (MHz):   3800                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65749000(0x3eb4008) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65749000(0x3eb4008) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65749000(0x3eb4008) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-9eccd5536937880d               
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
  BDFID:                   3584                               
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
  Packet Processor uCode:: 550                                
  SDMA engine uCode::      19                                 
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
*** Done ***             


### Additional Information

**/var/log/Xorg.0.log**
```bash
[  1675.337] (WW) AMDGPU(0): gbm_create_device returned NULL, using ShadowFB
[  1675.400] (WW) AMDGPU(0): Direct rendering disabled
```

**/var/log/syslog**
```bash
Mar 10 01:35:31 valhalla systemd[1]: Started Session 14 of User sddm.
Mar 10 01:35:31 valhalla sddm-helper[5732]: Writing cookie to "/tmp/xauth_iHETGS"
Mar 10 01:35:31 valhalla sddm-helper[5732]: Starting X11 session: "" "/usr/bin/sddm-greeter --socket /tmp/sddm-:0-FjyfYl --theme /usr/share/sddm/themes/ubuntu-theme"
Mar 10 01:35:31 valhalla sddm[3326]: Greeter session started successfully
Mar 10 01:35:31 valhalla sddm-greeter[5746]: High-DPI autoscaling Enabled
Mar 10 01:35:31 valhalla sddm-greeter[5746]: Reading from "/usr/local/share/xsessions/plasma.desktop"
Mar 10 01:35:31 valhalla sddm-greeter[5746]: Reading from "/usr/share/xsessions/plasma.desktop"
Mar 10 01:35:31 valhalla sddm-greeter[5746]: Reading from "/usr/local/share/xsessions/xfce.desktop"
Mar 10 01:35:31 valhalla sddm-greeter[5746]: Reading from "/usr/share/xsessions/xfce.desktop"
Mar 10 01:35:31 valhalla sddm-greeter[5746]: Loading theme configuration from "/usr/share/sddm/themes/ubuntu-theme/theme.conf"
Mar 10 01:35:31 valhalla sddm-greeter[5746]: Connected to the daemon.
Mar 10 01:35:31 valhalla sddm[3326]: Message received from greeter: Connect
Mar 10 01:35:31 valhalla sddm-greeter[5746]: QGLXContext: Failed to create dummy context
Mar 10 01:35:31 valhalla sddm-greeter[5746]: Loading file:///usr/share/sddm/themes/ubuntu-theme/Main.qml...
Mar 10 01:35:31 valhalla sddm-greeter[5746]: QObject: Cannot create children for a parent that is in a different thread.#012(Parent is QGuiApplication(0x7ffe2c3accb0), parent's thread is QThread(0x64e304036190), current thread is QThread(0x64e304206bf0)
Mar 10 01:35:31 valhalla sddm-greeter[5746]: message repeated 2 times: [ QObject: Cannot create children for a parent that is in a different thread.#012(Parent is QGuiApplication(0x7ffe2c3accb0), parent's thread is QThread(0x64e304036190), current thread is QThread(0x64e304206bf0)]
Mar 10 01:35:31 valhalla sddm-greeter[5746]: QObject::installEventFilter(): Cannot filter events for objects in a different thread.
Mar 10 01:35:31 valhalla sddm-greeter[5746]: failed to acquire GL context to resolve capabilities, using defaults..
Mar 10 01:35:32 valhalla sddm-greeter[5746]: Adding view for "DisplayPort-0" QRect(0,0 1920x1080)
Mar 10 01:35:32 valhalla sddm-greeter[5746]: Loading file:///usr/share/sddm/themes/ubuntu-theme/Main.qml...
Mar 10 01:35:32 valhalla sddm-greeter[5746]: QQmlEngine::setContextForObject(): Object already has a QQmlContext
Mar 10 01:35:32 valhalla sddm-greeter[5746]: QQmlEngine::setContextForObject(): Object already has a QQmlContext
Mar 10 01:35:32 valhalla sddm-greeter[5746]: failed to acquire GL context to resolve capabilities, using defaults..
Mar 10 01:35:32 valhalla sddm-greeter[5746]: Adding view for "HDMI-A-0" QRect(1920,0 1920x1080)
Mar 10 01:35:32 valhalla sddm-greeter[5746]: Loading file:///usr/share/sddm/themes/ubuntu-theme/Main.qml...
Mar 10 01:35:32 valhalla sddm-greeter[5746]: QQmlEngine::setContextForObject(): Object already has a QQmlContext
Mar 10 01:35:32 valhalla sddm-greeter[5746]: QQmlEngine::setContextForObject(): Object already has a QQmlContext
Mar 10 01:35:32 valhalla sddm-greeter[5746]: failed to acquire GL context to resolve capabilities, using defaults..
Mar 10 01:35:32 valhalla sddm-greeter[5746]: Adding view for "HDMI-A-1" QRect(3840,0 1920x1080)
Mar 10 01:35:32 valhalla sddm-greeter[5746]: Failed to create OpenGL context for format QSurfaceFormat(version 2.0, options QFlags<QSurfaceFormat::FormatOption>(ResetNotification), depthBufferSize 24, redBufferSize -1, greenBufferSize -1, blueBufferSize -1, alphaBufferSize -1, stencilBufferSize 8, samples -1, swapBehavior QSurfaceFormat::DoubleBuffer, swapInterval 1, colorSpace QSurfaceFormat::DefaultColorSpace, profile  QSurfaceFormat::NoProfile)
Mar 10 01:35:33 valhalla sddm-helper[5732]: [PAM] Closing session
Mar 10 01:35:33 valhalla sddm-helper[5732]: [PAM] Ended.
Mar 10 01:35:33 valhalla sddm[3326]: Auth: sddm-helper exited with 6
Mar 10 01:35:33 valhalla sddm[3326]: Greeter stopped. SDDM::Auth::HelperExitStatus(6)

```

---

## 评论 (6 条)

### 评论 #1 — nartmada (2024-03-11T16:16:46Z)

Internal ticket has been created for investigation.

---

### 评论 #2 — extraymond (2024-03-12T10:41:34Z)

Similar issue observed on ubuntu 22.04 gnome with kisak/mesa ppa, with rocm 6.0.2.

---

### 评论 #3 — ipanfilo (2024-03-19T00:50:03Z)

Kisak/Mesa PPA requires newer libdrm-amdgpu than one installed with ROCm6.0.2.
The necessary changes are in ROCm6.1
Alternatively, you may make your system using libdrm-amdgpu from /usr/lib/x86_64-linux-gnu/  which is installed with Mesa rather than default from /opt/amdgpu/lib/x86_64-linux-gnu/.
Do it by configuring and rebuilding ldd cache or just replace  libdrm_amdgpu.so.1.0.0

---

### 评论 #4 — smirgol (2024-03-20T07:59:52Z)

I've created a conf file in `/etc/ld.so.conf.d/` and put `/usr/lib/x86_64-linux-gnu/libdrm_amdgpu.so.1.0.0` inside it, then ran `ldconfig`.
This allows me to boot into my desktop again after installing ROCm. Unfortunately the render stack is still broken in some way. For example, here's a log of `glxinfo`:

```
name of display: :0.0
MESA-LOADER: failed to open radeonsi: /usr/lib/dri/radeonsi_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib/x86_64-linux-gnu/dri:\$${ORIGIN}/dri:/usr/lib/dri, suffix _dri)
failed to load driver: radeonsi
MESA-LOADER: failed to open radeonsi: /usr/lib/dri/radeonsi_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib/x86_64-linux-gnu/dri:\$${ORIGIN}/dri:/usr/lib/dri, suffix _dri)
failed to load driver: radeonsi
MESA-LOADER: failed to open swrast: /usr/lib/dri/swrast_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib/x86_64-linux-gnu/dri:\$${ORIGIN}/dri:/usr/lib/dri, suffix _dri)
failed to load driver: swrast
X Error of failed request:  BadValue (integer parameter out of range for operation)
  Major opcode of failed request:  152 (GLX)
  Minor opcode of failed request:  24 (X_GLXCreateNewContext)
  Value in failed request:  0x0
  Serial number of failed request:  50
  Current serial number in output stream:  51
```

Edit:
Nevermind, looks like that does not work the way I thought it would. I ended up replacing the file in `/etc/amdgpu/lib` and updated the symlinks. Now it seems to work, but need to test some more. :)

---

### 评论 #5 — ipanfilo (2024-03-21T23:06:18Z)

Indeed, there looks be another overlooked problem. For me it worked with 6.0.2 cause /usr/lib/dri/ pointed to /usr/lib/x86_64-linux-gnu/dri/ where radeonsi_dri.so is actually installed by Mesa

---

### 评论 #6 — pleasewhy (2024-08-11T06:01:14Z)

I fix this with the following command
sudo amdgpu-install --usecase=graphics


---
