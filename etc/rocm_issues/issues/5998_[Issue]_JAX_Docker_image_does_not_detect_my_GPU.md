# [Issue]: JAX Docker image does not detect my GPU

> **Issue #5998**
> **状态**: open
> **创建时间**: 2026-02-24T22:48:52Z
> **更新时间**: 2026-03-16T20:42:13Z
> **作者**: yasharhon
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5998

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

I tried installing ROCm and pulling a JAX Docker image to run JAX code, following the instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/jax-install.html). Running the test snippet to test the installation returns

```
[RocmDevice(id=0)]
Traceback (most recent call last):

... Stack trace here

jax.errors.JaxRuntimeError: INTERNAL: unable to find ld.lld in PATH: No such file or directory
```

It seems to run fine with Pytorch, so I feel somewhat confident that the ROCm install went OK.

Note: I observed the same issue as #4043, so I ran the same udev fix as was suggested there.

### Operating System

Ubuntu 24.04.4

### CPU

Intel(R) Core(TM) i5-7600 CPU @ 3.50GHz. 

### GPU

AMD Radeon RX 9060 XT.

### ROCm Version

ROCm 7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module version 6.16.13 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.15
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
  Name:                    Intel(R) Core(TM) i5-7600 CPU @ 3.50GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i5-7600 CPU @ 3.50GHz
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
  Max Clock Freq. (MHz):   4100                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            4                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    24550368(0x1769be0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24550368(0x1769be0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    24550368(0x1769be0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    24550368(0x1769be0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1200                            
  Uuid:                    GPU-76d4de1a1944b098               
  Marketing Name:          AMD Radeon RX 9060 XT              
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
    L3:                      32768(0x8000) KB                   
  Chip ID:                 30096(0x7590)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2620                               
  BDFID:                   1024                               
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
  Packet Processor uCode:: 128                                
  SDMA engine uCode::      662                                
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
      Name:                    amdgcn-amd-amdhsa--gfx1200         
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
```

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — chejh-amd (2026-02-28T06:48:25Z)

Hi @yasharhon You mentioned that you ran the same udev fix as [#4043](https://github.com/ROCm/ROCm/issues/4043) was suggested, how about the result?

---

### 评论 #2 — yasharhon (2026-02-28T20:39:34Z)

@Michelle-HCJ  Seemed to work fine. I got the same error as the issue mentioned, and running the udev fix made the error not appear anymore. Note that everything is installed on my host OS, not in a container as in that issue.

ETA: For clarity, that solved the post-installation verification issues, not the issues running JAX.

Here's what I get when doing the post-install verification steps:

- Package installation - `apt list --installed | grep rocm`  
```
rocm-cmake/noble,now 0.14.0.70200-43~24.04 amd64 [installed,automatic]
rocm-core/noble,now 7.2.0.70200-43~24.04 amd64 [installed,automatic]
rocm-dbgapi/noble,now 0.77.4.70200-43~24.04 amd64 [installed,automatic]
rocm-debug-agent/noble,now 2.1.0.70200-43~24.04 amd64 [installed,automatic]
rocm-developer-tools/noble,now 7.2.0.70200-43~24.04 amd64 [installed,automatic]
rocm-device-libs/noble,now 1.0.0.70200-43~24.04 amd64 [installed,automatic]
rocm-gdb/noble,now 16.3.70200-43~24.04 amd64 [installed,automatic]
rocm-hip/noble,now 7.2.0.70200-43~24.04 amd64 [installed,automatic]
rocm-llvm/noble,now 22.0.0.26014.70200-43~24.04 amd64 [installed,automatic]
rocm-opencl-dev/noble,now 2.0.0.70200-43~24.04 amd64 [installed,automatic]
rocm-opencl-sdk/noble,now 7.2.0.70200-43~24.04 amd64 [installed,automatic]
rocm-opencl/noble,now 2.0.0.70200-43~24.04 amd64 [installed,automatic]
rocm-openmp/noble,now 7.2.0.70200-43~24.04 amd64 [installed,automatic]
rocm-smi-lib/noble,now 7.8.0.70200-43~24.04 amd64 [installed,automatic]
rocm/noble,now 7.2.0.70200-43~24.04 amd64 [installed]
rocminfo/noble,now 1.0.0.70200-43~24.04 amd64 [installed,automatic]
```
- ROCm installation - `rocminfo | grep -i "Marketing Name:"`:  
```
  Marketing Name:          Intel(R) Core(TM) i5-7600 CPU @ 3.50GHz
  Marketing Name:          AMD Radeon RX 9060 XT
```
- ROCm installation - `clinfo | grep -i "Board name:"`:  
```
  Board name:					 AMD Radeon RX 9060 XT
```
- ROCm installation - `amd-smi version`:  
```
AMDSMI Tool: 26.2.1+fc0010cf6a | AMDSMI Library version: 26.2.1 | ROCm version: 7.2.0 | amdgpu version: 6.16.13 | hsmp version: N/A
```

---

### 评论 #3 — lucbruni-amd (2026-03-02T21:32:20Z)

Hi @yasharhon, thanks for reporting this issue.

I am able to reproduce this with `rocm/jax:latest` following the instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/jax-install.html#use-a-prebuilt-docker-image-with-jax-preinstalled), and running the tests:

```
python3 -c "import jax; print(jax.devices())"
python3 -c "import jax.numpy as jnp; x = jnp.arange(5); print(x)"
```

The workaround is to run the following: `export LLVM_PATH=/opt/rocm/llvm`.

I can see this issue was fixed in the nightly built image [here](https://github.com/ROCm/rocm-jax/actions/workflows/nightly.yml) after pulling it. However, these images built against ROCm 7.2.0 do not seem to be available to the public yet, hence why [only the 7.0.0 image is documented](https://github.com/ROCm/rocm-jax?tab=readme-ov-file#docker-images). I am currently inquiring about this.

You can find more of these images [here](https://github.com/orgs/ROCm/packages?repo_name=rocm-jax). If you have issues pulling them as per the above, let me know.

If you do try out `ghcr.io/rocm/jax-ubu24.rocm700:nightly` or any of the other images, you may run into https://github.com/ROCm/rocm-jax/issues/163. If so, workaround by running:

```
apt update
apt install libdw1
```

That issue is also fixed with the latest nightlies for ROCm 7.2.0. I will update this ticket further when both fixes are consolidated into the `rocm/jax:latest` image, which is what this issue is about.

Let me know if you have additional questions/concerns. Thanks!


---

### 评论 #4 — yasharhon (2026-03-03T15:28:30Z)

@lucbruni-amd Thanks for getting back to me! It might take a few days before I'm able to run the test, unfortunately. I'll get back to you as soon as that's done.

Just to be clear:
- I only need to add the `LLVM_PATH` env variable? No other installation is needed?
- If that doesn't work with ROCm 7.2.0, the next step is to downgrade to 7.0.0 and follow the instructions using a nightly-based Docker image, as the fix should be in place for those?

---

### 评论 #5 — lucbruni-amd (2026-03-03T15:43:47Z)

>I only need to add the LLVM_PATH env variable? No other installation is needed?

Yes, this should workaround the first issue you encountered.

>If that doesn't work with ROCm 7.2.0, the next step is to downgrade to 7.0.0 and follow the instructions using a nightly-based Docker image, as the fix should be in place for those?

My apologies for the confusion in my message above. If you have no luck with the env variable above inside the `rocm/jax:latest` container, you can try the [nightly](https://github.com/ROCm/rocm-jax/pkgs/container/jax-ubu24.rocm720). You can find a bunch of options [here](https://github.com/orgs/ROCm/packages?repo_name=rocm-jax).

Please don't hesitate to reach out if you have any additional questions or issues. Happy to help!

---

### 评论 #6 — yasharhon (2026-03-05T18:28:43Z)

@lucbruni-amd Finally got around to testing it, here are some findings:

- Changing `LLVM_PATH` did not fix anything on its own.
- The `LLVM_PATH` variable had the wrong value inside the (latest) JAX container.
- Updating the variables both in the container and on my host OS seems to have made JAX runnable, but I still get just one device.

I assume this means that the run was successful, given that JAX didn't crash this time. Is JAX also detecting my GPU, given that it finds a `RocmDevice`?

---

### 评论 #7 — lucbruni-amd (2026-03-11T15:20:55Z)

Yes, that means the run was successful. `RocmDevice` is JAX’s device type for AMD GPUs. So `RocmDevice(id=0)` should be your RX 9060 XT. Let me know if you have further issues/questions.

---

### 评论 #8 — yasharhon (2026-03-12T21:44:20Z)

No, that was it, this issue has been solved as far as I am concerned. Please update the documentation, though

---

### 评论 #9 — lucbruni-amd (2026-03-16T20:36:34Z)

The workaround of setting `LLVM_PATH` within the container should be sufficient on it's own. The steps I took to achieve this (following [this page](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/jax-install.html#use-a-prebuilt-docker-image-with-jax-preinstalled)):

```
$ docker pull rocm/jax:latest

# The docker run flags only give the container access to the GPU devices (--device=/dev/kfd, --device=/dev/dri), not the host’s filesystem.
# So the host’s /opt/rocm is not mounted; the container uses its own /opt/rocm and /opt/rocm-7.2.0.
$ docker run -it \
    --network=host \
    --device=/dev/kfd \
    --device=/dev/dri \
    --ipc=host \
    --shm-size 64G \
    --group-add video \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    -v $(pwd):/jax_dir \
    --name rocm_jax \
    rocm/jax:latest /bin/bash

$ python3 -c "import jax; print(jax.devices())"
[RocmDevice(id=0)]
$ python3 -c "import jax.numpy as jnp; x = jnp.arange(5); print(x)"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/local/lib/python3.12/dist-packages/jax/_src/numpy/lax_numpy.py", line 5946, in arange
    return _arange(start, stop=stop, step=step, dtype=dtype,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/jax/_src/numpy/lax_numpy.py", line 5989, in _arange
    return lax.broadcasted_iota(dtype, (start,), 0, out_sharding=out_sharding)  # type: ignore[arg-type]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/jax/_src/lax/lax.py", line 3455, in broadcasted_iota
    return iota_p.bind(*dynamic_shape, dtype=dtype, shape=tuple(static_shape),
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/jax/_src/core.py", line 632, in bind
    return self._true_bind(*args, **params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/jax/_src/core.py", line 648, in _true_bind
    return self.bind_with_trace(prev_trace, args, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/jax/_src/core.py", line 660, in bind_with_trace
    return trace.process_primitive(self, args, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/jax/_src/core.py", line 1189, in process_primitive
    return primitive.impl(*args, **params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/jax/_src/dispatch.py", line 94, in apply_primitive
    outs = fun(*args)
           ^^^^^^^^^^
jax.errors.JaxRuntimeError: INTERNAL: unable to find ld.lld in PATH: No such file or directory
--------------------
For simplicity, JAX has removed its internal frames from the traceback of the following exception. Set JAX_TRACEBACK_FILTERING=off to include these.

$ export LLVM_PATH=/opt/rocm/llvm
$ python3 -c "import jax; print(jax.devices())"
[RocmDevice(id=0)]
$ python3 -c "import jax.numpy as jnp; x = jnp.arange(5); print(x)"
[0 1 2 3 4]
```

>The LLVM_PATH variable had the wrong value inside the (latest) JAX container.

That's right. Verified this with:
```
$ docker run --rm rocm/jax:latest env | grep -i llvm
PATH=/root/bin:/root/.local/bin:/opt/rocm-7.2/opencl/bin:/opt/rocm-7.2/bin:/opt/rocm-7.2/hcc/bin:/opt/rocm-7.2//bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/rocm/bin:/opt/rocm/llvm/bin
LLVM_PATH=/opt/rocm-7.2/llvm

# ls -l /opt
total 4
lrwxrwxrwx 1 root root   22 Jan 21 21:07 rocm -> /etc/alternatives/rocm
drwxr-xr-x 8 root root 4096 Jan 21 21:07 rocm-7.2.0
```

This shows the `rocm/jax:latest` image was built with an incorrect argument, causing `LLVM_PATH` to be incorrectly set (see https://github.com/ROCm/rocm-jax/blob/33fbb4bc8c3f59ba91b81a5a152fd17da1e09bf9/docker/Dockerfile.base-ubu24#L155). So this is not a documentation issue, we just have to make sure that `rocm/jax:latest` gets built correctly before it is shipped in conjunction with the next ROCm release. I'll keep this open until that happens.

---
