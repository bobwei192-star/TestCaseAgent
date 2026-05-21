# [Issue]: ROCm 6.1 amdgpu-dkms fails to build on Linux

> **Issue #3036**
> **状态**: closed
> **创建时间**: 2024-04-17T22:24:43Z
> **更新时间**: 2024-09-14T18:49:40Z
> **关闭时间**: 2024-05-31T14:12:30Z
> **作者**: hankster112
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/3036

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

Issue is with latest release of ROCm 6.1.
```
DKMS make.log for amdgpu-6.7.0-1756574.22.04 for kernel 6.6.13+bpo-amd64 (amd64)
Wed Apr 17 09:26:34 AM CDT 2024
make: Entering directory '/usr/src/linux-headers-6.6.13+bpo-amd64'
/tmp/amd.Z35UpKSZ/Makefile:52: *** dma_resv->seq is missing. exit....  Stop.
make[1]: *** [/usr/src/linux-headers-6.6.13+bpo-common/Makefile:1938: /tmp/amd.Z35UpKSZ] Error 2
make: *** [/usr/src/linux-headers-6.6.13+bpo-common/Makefile:246: __sub-make] Error 2
make: Leaving directory '/usr/src/linux-headers-6.6.13+bpo-amd64'
```
Used the latest install instructions from https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html
Tried with repos for Ubuntu 22.04 and Ubuntu 20.04 which should also work on Debian. Purged all config files and AMD apt sources beforehand.

Devuan 5 Daedalus (fork of Debian 12 without systemd)
AMD Ryzen 7 2700
MSI Radeon 5700 XT
Kernel 6.6.13+bpo-amd64

### Operating System

Debian 12

### CPU

AMD Ryzen 7 2700

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

Attempt to build from source on Debian 12.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 7 2700 Eight-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 2700 Eight-Core Processor
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
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3200                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16301932(0xf8bf6c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16301932(0xf8bf6c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16301932(0xf8bf6c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1010                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 5700 XT              
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
    L1:                      16(0x10) KB                        
    L2:                      4096(0x1000) KB                    
  Chip ID:                 29471(0x731f)                      
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   11008                              
  Internal Node ID:        1                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          32(0x20)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    1280(0x500)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    8372224(0x7fc000) KB               
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
      Name:                    amdgcn-amd-amdhsa--gfx1010:xnack-  
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

## 评论 (36 条)

### 评论 #1 — Wedge009 (2024-04-17T23:40:57Z)

https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.1.0/reference/system-requirements.html suggests kernel 6.6 is not supported (yet?). I'm concerned about this because of #2993 -> #2939.

---

### 评论 #2 — hankster112 (2024-04-18T02:13:11Z)

> https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.1.0/reference/system-requirements.html suggests kernel 6.6 is not supported (yet?). I'm concerned about this because of #2993 -> #2939.

My distro only has official kernels for 6.1 or 6.6, no in-between. It's like I'm caught between downgrading to Debian 11 where kernel 5.x might work, or waiting until 6.x to see if ROCm _might_ work. It's really frustrating.

---

### 评论 #3 — Wedge009 (2024-04-18T02:15:29Z)

Yes, similar situation with Ubuntu 22.04 vs 24.04.

Most recent kernel I have working with ROCm is kernel 6.5 with Vega20 GPU.

---

### 评论 #4 — vkomenda (2024-04-19T10:31:29Z)

6.6 kernel support was [promised](https://github.com/ROCm/ROCm/issues/2451#issuecomment-1938773547) earlier to arrive in the 6.1 release. It hasn't.

Even if the failing check on lines 51-53 of the DKMS driver `Makefile` is commented out, there are more compilation errors, and those also look the same as in the 6.0 driver release. I fail to see what's changed with regards to newer kernel support.

---

### 评论 #5 — powderluv (2024-04-23T02:49:11Z)

are you able to use stock upstream `amdgpu` driver and firmware with just the ROCm userspace install ? Usually that is also at a good functioning state. 

---

### 评论 #6 — hankster112 (2024-04-24T21:55:06Z)

> are you able to use stock upstream `amdgpu` driver and firmware with just the ROCm userspace install ? Usually that is also at a good functioning state.

No, I need ROCm for Blender GPU support.

---

### 评论 #7 — IMbackK (2024-04-30T11:20:42Z)

ROCM works perfectly fine without the dkms module with just the upstream amdgpu module built into the kernel. the dkms module is really only for when some features have not landed in the kernel and to support old enterprise distributions:
i would like to add the following strong recommendations:
1. Prefer simply using the upstream default amdgpu, unless you expirance issues or need a specific feature it lacks. If you are on a recent kernel its generally better than the dkms module anyhow
2. STROGNLY prefer to use rocm from distro packages (available in debian, arch linux and others) over using the offical amd packages or distrobutions.

---

### 评论 #8 — hankster112 (2024-04-30T20:50:27Z)

> ROCM works perfectly fine without the dkms module with just the upstream amdgpu module built into the kernel. the dkms module is really only for when some features have not landed in the kernel and to support old enterprise distributions: i would like to add the following strong recommendations:
> 
> 1. Prefer simply using the upstream default amdgpu, unless you expirance issues or need a specific feature it lacks. If you are on a recent kernel its generally better than the dkms module anyhow
> 2. STROGNLY prefer to use rocm from distro packages (available in debian, arch linux and others) over using the offical amd packages or distrobutions.

ROCm is not available from my distro's package manager. Trying to install ROCm from AMD's website with the --no-dkms flag results in failed dependences since it relies on systemd for some reason (Devuan is a fork of Debian with no dependencies on systemd). Blender needs ROCm to use GPU acceleration.

---

### 评论 #9 — IMbackK (2024-05-01T09:30:32Z)

Your trying to install packages from a totally (Ubuntu) different distribution on devuan of course that dosent work. As with any piece of software on linux, unless its totaly static (which you defiantly dont want for a system library like compute drivers) you need to either have it in your distros repository or you need to compile it yourself. Since devuan is so close to debian you might also get away with installing the rocm packages for debian for the corrisponding debian version, but thats not great either.

I would also petition your distro maintainers to import the packages from debian to build on thair ci, since the debian-ai team have packaged all rocm componants with /debian directories this should be pretty easy, with only limited modification of the packageing files for devuan.

---

### 评论 #10 — vkomenda (2024-05-03T17:53:39Z)

> ROCM works perfectly fine without the dkms module with just the upstream amdgpu module built into the kernel. the dkms module is really only for when some features have not landed in the kernel and to support old enterprise distributions: i would like to add the following strong recommendations:
> 
> 1. Prefer simply using the upstream default amdgpu, unless you expirance issues or need a specific feature it lacks. If you are on a recent kernel its generally better than the dkms module anyhow
> 2. STROGNLY prefer to use rocm from distro packages (available in debian, arch linux and others) over using the offical amd packages or distrobutions.

The upstream driver lacks power-saving features and colour control. My laptop display is very bright and drains the battery quickly. It has to be tuned down.

What seems to be the problem with upstream kernel support? My laptop is almost a year old and there's still no support in the mainline.

Also there is no external monitor support in the mainline driver, which is a big deal.

---

### 评论 #11 — nairboon (2024-05-18T13:14:53Z)

> 6.6 kernel support was [promised](https://github.com/ROCm/ROCm/issues/2451#issuecomment-1938773547) earlier to arrive in the 6.1 release. It hasn't.

Kernels up to 6.8 are now supported with the latest rocm 6.1.1 release


---

### 评论 #12 — supernovae (2024-05-20T16:02:26Z)

> > 6.6 kernel support was [promised](https://github.com/ROCm/ROCm/issues/2451#issuecomment-1938773547) earlier to arrive in the 6.1 release. It hasn't.
> 
> Kernels up to 6.8 are now supported with the latest rocm 6.1.1 release

any supported way to get to 6.8 kernel? i tried mainline kernels process but anything above 6.7 won't install headers because of glibc update that's not on 22.0.4

would be nice to just have 24.04 support :+1: 

---

### 评论 #13 — hankster112 (2024-05-21T21:20:30Z)

> > 6.6 kernel support was [promised](https://github.com/ROCm/ROCm/issues/2451#issuecomment-1938773547) earlier to arrive in the 6.1 release. It hasn't.
> 
> Kernels up to 6.8 are now supported with the latest rocm 6.1.1 release

Same error.

```
user@device:~$ sudo apt install amdgpu-dkms
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  amdgpu-dkms-firmware
The following NEW packages will be installed:
  amdgpu-dkms amdgpu-dkms-firmware
0 upgraded, 2 newly installed, 0 to remove and 7 not upgraded.
Need to get 22.3 MB of archives.
After this operation, 555 MB of additional disk space will be used.
Do you want to continue? [Y/n] y
Get:1 https://repo.radeon.com/amdgpu/6.1.1/ubuntu jammy/main amd64 amdgpu-dkms-firmware all 1:6.7.0.60101-1769056.22.04 [11.5 MB]
Get:2 https://repo.radeon.com/amdgpu/6.1.1/ubuntu jammy/main amd64 amdgpu-dkms all 1:6.7.0.60101-1769056.22.04 [10.8 MB]
Fetched 22.3 MB in 1s (17.7 MB/s)       
Selecting previously unselected package amdgpu-dkms-firmware.
(Reading database ... 520152 files and directories currently installed.)
Preparing to unpack .../amdgpu-dkms-firmware_1%3a6.7.0.60101-1769056.22.04_all.deb ...
Unpacking amdgpu-dkms-firmware (1:6.7.0.60101-1769056.22.04) ...
Selecting previously unselected package amdgpu-dkms.
Preparing to unpack .../amdgpu-dkms_1%3a6.7.0.60101-1769056.22.04_all.deb ...
Unpacking amdgpu-dkms (1:6.7.0.60101-1769056.22.04) ...
Setting up amdgpu-dkms-firmware (1:6.7.0.60101-1769056.22.04) ...
Setting up amdgpu-dkms (1:6.7.0.60101-1769056.22.04) ...
Loading new amdgpu-6.7.0-1769056.22.04 DKMS files...
Building for 6.6.13+bpo-amd64
Building for architecture amd64
Building initial module for 6.6.13+bpo-amd64
Error! Bad return status for module build on kernel: 6.6.13+bpo-amd64 (amd64)
Consult /var/lib/dkms/amdgpu/6.7.0-1769056.22.04/build/make.log for more information.
dpkg: error processing package amdgpu-dkms (--configure):
 installed amdgpu-dkms package post-installation script subprocess returned error exit status 10
Errors were encountered while processing:
 amdgpu-dkms
needrestart is being skipped since dpkg has failed
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

---

### 评论 #14 — vkomenda (2024-05-21T21:27:23Z)


> Kernels up to 6.8 are now supported with the latest rocm 6.1.1 release

Yeah, those "up to 6.8" kernels are HWE, which don't exist outside Ubuntu. Is mainlining the only case when the GPU driver becomes available in Debian and other distros? Because I'm not using Ubuntu 22.

Is there a plan for mainlining? Are there any blockages?


---

### 评论 #15 — nairboon (2024-05-22T04:47:30Z)


> 
> Same error.

Then the problem is something else, maybe as mentioned previously related to Ubuntu's glibc version.

I just pointed out that the 6.1.1 rocm release does finally compile with a newish kernel, which the previous releases did not, due to kernel compatibility issues.

I'm currently running the latest rocm on Debian with a 6.8.10 kernel.




---

### 评论 #16 — vkomenda (2024-05-22T21:27:21Z)

> Then the problem is something else, maybe as mentioned previously related to Ubuntu's glibc version.
> 
> I just pointed out that the 6.1.1 rocm release does finally compile with a newish kernel, which the previous releases did not, due to kernel compatibility issues.
> 
> I'm currently running the latest rocm on Debian with a 6.8.10 kernel.

Does anyone get the apt GPG key signature mismatch? apt cannot download package lists.

```
Warning: GPG error: https://repo.radeon.com/amdgpu/6.1.1/ubuntu jammy InRelease: The following signatures were invalid: ERRSIG 9386B48A1A693C5C
Error: The repository 'https://repo.radeon.com/amdgpu/6.1.1/ubuntu jammy InRelease' is not signed.
```

I checked the key signature and it matches:
```
$ gpg --list-packets /etc/apt/trusted.gpg.d/rocm-keyring.gpg 
# off=0 ctb=99 tag=6 hlen=3 plen=525
:public key packet:
	version 4, algo 1, created 1470083360, expires 0
	pkey[0]: [4096 bits]
	pkey[1]: [17 bits]
	keyid: 9386B48A1A693C5C
```

Difficult to tell what's going on.

---

### 评论 #17 — vkomenda (2024-05-22T21:38:01Z)

Same error with kernel 6.7.12 on Debian. That's amdgpu-dkms 6.1.1. 

```
*** dma_resv->seq is missing. exit....  Stop.
```

---

### 评论 #18 — hankster112 (2024-05-25T21:55:06Z)

Still waiting for any kind of update/explanation for this. Still on the same kernel when I made the OP, same error as vkomenda when building.

---

### 评论 #19 — hankster112 (2024-05-26T17:56:49Z)

amdgpu DKMS module still fails to build for the latest 6.7.12 kernel.
```
dpkg: error processing package linux-headers-amd64 (--configure):
 dependency problems - leaving unconfigured
Errors were encountered while processing:
 linux-image-6.7.12+bpo-amd64
 linux-image-amd64
 linux-headers-6.7.12+bpo-amd64
 linux-headers-amd64
needrestart is being skipped since dpkg has failed
E: Sub-process /usr/bin/dpkg returned an error code (1)
```
The error in make.log:
```
DKMS make.log for amdgpu-6.7.0-1756574.22.04 for kernel 6.7.12+bpo-amd64 (x86_64)
Sun May 26 12:47:00 PM CDT 2024
make: Entering directory '/usr/src/linux-headers-6.7.12+bpo-amd64'
/tmp/amd.UmjcyhcM/Makefile:52: *** dma_resv->seq is missing. exit....  Stop.
make[1]: *** [/usr/src/linux-headers-6.7.12+bpo-common/Makefile:1936: /tmp/amd.UmjcyhcM] Error 2
make: *** [/usr/src/linux-headers-6.7.12+bpo-common/Makefile:246: __sub-make] Error 2
make: Leaving directory '/usr/src/linux-headers-6.7.12+bpo-amd64'
```

---

### 评论 #20 — hankster112 (2024-05-28T22:49:45Z)

Same error with latest kernel.

```
DKMS make.log for amdgpu-6.7.0-1769056.20.04 for kernel 6.7.12+bpo-amd64 (amd64)
Tue May 28 05:45:45 PM CDT 2024
make: Entering directory '/usr/src/linux-headers-6.7.12+bpo-amd64'
/tmp/amd.DeGLA8su/Makefile:52: *** dma_resv->seq is missing. exit....  Stop.
make[1]: *** [/usr/src/linux-headers-6.7.12+bpo-common/Makefile:1936: /tmp/amd.DeGLA8su] Error 2
make: *** [/usr/src/linux-headers-6.7.12+bpo-common/Makefile:246: __sub-make] Error 2
make: Leaving directory '/usr/src/linux-headers-6.7.12+bpo-amd64'
```

---

### 评论 #21 — kentrussell (2024-05-29T14:50:13Z)

@nartmada @ppanchad-amd Can we get an internal JIRA made and assign it to the KCL team? I  feel like the resv->seq check isn't correct here. Even though this isn't a supported kernel, it's still an oversight. Hopefully they can figure out what's happening, even on an unsupported kernel . Thanks!

---

### 评论 #22 — ppanchad-amd (2024-05-29T15:11:25Z)

@kentrussell Internal JIRA ticket has been created to investigate this issue. Thanks!

---

### 评论 #23 — ppanchad-amd (2024-05-31T14:12:30Z)

@hankster112 Packaged driver on Debian is not supported. Closing ticket.

---

### 评论 #24 — vkomenda (2024-05-31T14:37:44Z)

> @hankster112 Packaged driver on Debian is not supported. Closing ticket.

You meant it's not supported and it *will not* be supported?

That it's not supported is already obvious.

---

### 评论 #25 — IMbackK (2024-05-31T14:45:01Z)

@vkomenda its supported via the packages in debain repo, there is nothing for amd to do here.

---

### 评论 #26 — vkomenda (2024-05-31T14:57:39Z)

> @vkomenda its supported via the packages in debain repo, there is nothing for amd to do here.

Can you please link this Debian repo. The installation instructions don't refer to any Debian repo. The `amdgpu-install` package I was downloading came from the Ubuntu repo.

---

### 评论 #27 — IMbackK (2024-05-31T15:07:59Z)

all the rocm componants are in the default debain repos where you would install anything from.
rocblas for instance: https://packages.debian.org/sid/librocblas0
its just apt install librocbas0 away

or rocm-smi:
https://packages.debian.org/sid/rocm-smi

---

### 评论 #28 — vkomenda (2024-05-31T15:25:22Z)

@IMbackK what is missing in the debian repo? A fork of `amdgpu-install`? My main issue is that the GPU DKMS driver doesn't compile.

---

### 评论 #29 — IMbackK (2024-05-31T16:47:14Z)

Nothing is missing You dont need any amdgpu kernel driver besides the one that is already built into the upstream mainline kernel

---

### 评论 #30 — vkomenda (2024-05-31T19:25:39Z)

Sorry the upstream driver doesn't fully support my GPU. No power
management, no external monitor.

On Fri, 31 May 2024, 18:47 uvos, ***@***.***> wrote:

> Nothing is missing You dont need any amdgpu kernel driver besides the one
> that is already built into the upstream mainline kernel
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/3036#issuecomment-2142633805>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/ABKF7IOYNJQCMVP244ELUXDZFCSSPAVCNFSM6AAAAABGMESWOWVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDCNBSGYZTGOBQGU>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #31 — IMbackK (2024-05-31T20:27:00Z)

what gpu would that be?


---

### 评论 #32 — vkomenda (2024-06-01T08:50:34Z)

> what gpu would that be?

Radeon 780M

---

### 评论 #33 — IMbackK (2024-06-01T10:01:53Z)

Well aside from the fact that that is obviously not a supported rocm device and apus have some quirks with how memory managment works that makes them quite hard to use usefully with rocm atm, the mainline kernel absolutely should support full pm and all crts for that device. You are barking up the wrong tree, if one of those dose not work this is a kernel bug that you should file against the kernel on the mailing list (after trying the latest patch of linux 6.9 of course), not here.

Given the patch diff between mainline and rocm-dkms its also somewhat unlikely that it would behave any different anyhow.

---

### 评论 #34 — vkomenda (2024-06-01T10:14:17Z)

> Well aside from the fact that that is obviously not a supported rocm device and apus have some quirks with how memory managment works that makes them quite hard to use usefully with rocm atm, the mainline kernel absolutely should support full pm and all crts for that device. You are barking up the wrong tree, if one of those dose not work this is a kernel bug that you should file against the kernel on the mailing list (after trying the latest patch of linux 6.9 of course), not here.
> 
> Given the patch diff between mainline and rocm-dkms its also somewhat unlikely that it would behave any different anyhow.

Sorry, what did you say? I suggest you check the AMD driver installation instructions at https://www.amd.com/en/support/linux-drivers. There is no mention of the mainline kernel driver. It recommends amdgpu-install.

Of course it's no problem to report bugs to the mainline if there is no consistency within the AMD, sure.

---

### 评论 #35 — nairboon (2024-06-29T15:07:27Z)

> @nartmada @ppanchad-amd Can we get an internal JIRA made and assign it to the KCL team? I feel like the resv->seq check isn't correct here. Even though this isn't a supported kernel, it's still an oversight. Hopefully they can figure out what's happening, even on an unsupported kernel . Thanks!

I think the dma_resv->seq check is a result of a build configuration error on Debian. @kentrussell could you take a look at #3379 ?

---

### 评论 #36 — davidbulladoenercoop (2024-07-17T14:48:25Z)

:speaker:  For those who are just looking for a workaround 

As suggested in https://github.com/ROCm/ROCm/issues/3379, this quick and dirty fix worked for me:
```sh
# Adapt this path to your kernel version (ls /usr/lib)
PATH_LINUX_KBUILD="/usr/lib/linux-kbuild-6.7.12+bpo" 
# For x86 users, move objtool.real-x86 to objtool
sudo mv $PATH_LINUX_KBUILD/tools/objtool/objtool.real-x86 $PATH_LINUX_KBUILD/tools/objtool/objtool
```  
I'm now able to apt upgrade! :fireworks: 

---
