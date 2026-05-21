# [Issue]: Hunyuan3D-2.1 corrupted texture output with ROCm 7.1 on AMD r9700.

> **Issue #5981**
> **状态**: closed
> **创建时间**: 2026-02-19T05:33:43Z
> **更新时间**: 2026-04-28T01:47:14Z
> **关闭时间**: 2026-02-26T14:11:11Z
> **作者**: manjunaths
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5981

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- zichguan-amd

## 描述

### Problem Description

There is texture corruption observed with Hunyuan3D-2.1 with ROCm on AMD r9700 GPUs. This is not observed with nVidia GPUs, as you can see in the attached pictures. The mesh generation seems to be okay, but the textures are corrupted.

As this is a pain to get working, I have created a Dockerfile and requirements.txt. Below are the steps to build the container and run. One other issue observed is that even 32GB memory the default single file generator that is given the Hunyuan3D-2.1 runs out of memory. So I have created code that splits the generation into 2 parts, a mesh generator and a texture generator. 

I have tested this with ROCm versions all the way from 6.4.0 to 7.2.0 and this issue persists.

I have tested this on nVidia GPUs, the same code, and it works with no corruption.

Thanks.

### Operating System

OS: NAME="Ubuntu" VERSION="22.04.5 LTS (Jammy Jellyfish)"

### CPU

CPU: model name      : AMD Ryzen 7 7800X3D 8-Core Processor

### GPU

AMD Radeon AI PRO R9700 

### ROCm Version

ROCm 7.2

### ROCm Component

_No response_

### Steps to Reproduce

1. Clone https://github.com/manjunaths/HY3D-2.1-ROCm
`git clone https://github.com/manjunaths/HY3D-2.1-ROCm`

2. Build docker container
` docker build --no-cache -t pytorch:rocm7.1_ubuntu22.04_py3.11_pytorch_release_2.9.1_hunyuan3D_2.1 .`

3. Run docker container
```
docker run --rm -it       --name=$(whoami)_hy3d       --privileged --network=host       --device=/dev/kfd --device=/dev/dri       --group-add video --cap-add=SYS_PTRACE       --security-opt seccomp=unconfined       --ipc=host --shm-size 16G pytorch:rocm7.1_ubuntu22.04_py3.11_pytorch_release_2.9.1_hunyuan3D_2.1 bash
```

4. Run the command
```
cd /root/Hunyuan3d-2.1
python generate3d.py assets/demo.png
```

There are some files generated after you run this command. Like these,

```
root@archlinux:~/Hunyuan3D-2.1# ls -1 demo_*
demo_shape_20260219034230.glb
demo_textured_20260219034230.glb
demo_textured_20260219034230.jpg
demo_textured_20260219034230.mtl
demo_textured_20260219034230_metallic.jpg
demo_textured_20260219034230_roughness.jpg
```

The number in the filename is a time stamp and varies. 

You can load the glb files into some three.js website such as https://threejs.org/editor/ (You can add two directional lights at the front and back) or [this](https://jessyleite.dev/super-glb-viewer/) (preferred). Or you can load it into your favorite 3d modeller like Blender. 

What you should see.

<img width="695" height="813" alt="Image" src="https://github.com/user-attachments/assets/dfb86f70-9b22-464d-8436-10ff89100f94" />

What I actually see.

<img width="604" height="710" alt="Image" src="https://github.com/user-attachments/assets/d4b5d3d4-7be8-40c1-a4c6-66a1726ca4cc" />

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

[37mROCk module is loaded[0m
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
  Name:                    AMD Ryzen 7 7800X3D 8-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7800X3D 8-Core Processor
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
  Max Clock Freq. (MHz):   5053                               
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
      Size:                    64862440(0x3ddb8e8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    64862440(0x3ddb8e8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    64862440(0x3ddb8e8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    64862440(0x3ddb8e8) KB             
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
  Uuid:                    GPU-ae866dfe401a6542               
  Marketing Name:          AMD Radeon AI PRO R9700            
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
  Chip ID:                 30033(0x7551)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   768                                
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
  Packet Processor uCode:: 128                                
  SDMA engine uCode::      662                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    33406976(0x1fdc000) KB             
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx1036                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Ryzen 7 7800X3D 8-Core Processor
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
    L2:                      256(0x100) KB                      
  Chip ID:                 5710(0x164e)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   4864                               
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
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
  Packet Processor uCode:: 121                                
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32431220(0x1eedc74) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32431220(0x1eedc74) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1036         
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
      Name:                    amdgcn-amd-amdhsa--gfx10-3-generic 
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

## 评论 (9 条)

### 评论 #1 — zichguan-amd (2026-02-23T17:30:05Z)

Hi @manjunaths, just tried this out on a 7900XTX and got this output which seems a bit different than your "correct output". Can you confirm if this should be the expected output? I'll test on a gfx1201 to make sure it's not gfx12 specific. 

<img width="819" height="1070" alt="Image" src="https://github.com/user-attachments/assets/f8dab34a-2939-4525-a6c5-3a7377aa2e8f" />

---

### 评论 #2 — manjunaths (2026-02-23T20:40:30Z)

Greetings,

This is the expected output. 

Unfortunately, I do not have access to a 7900xtx right now to test this. This could be an issue specific to the r9700. 

---

### 评论 #3 — zichguan-amd (2026-02-23T21:05:08Z)

The model is too big for a regular 9070XT, I'll try to see if 2x 9070XT works, otherwise I'll need to find a R9700 which could take some time.

---

### 评论 #4 — zichguan-amd (2026-02-24T16:39:12Z)

Got my hands on a r9700 and indeed the output texture doesn't seem right compared to the 7900xtx output. This does appear to be a gfx12 specific issue.

<img width="494" height="668" alt="Image" src="https://github.com/user-attachments/assets/e510320d-865d-4dc4-9a08-6195dce26173" />

---

### 评论 #5 — zichguan-amd (2026-02-25T03:13:59Z)

Hi @manjunaths, I tested with lates TheRock gfx1201 wheels with `torch==2.9.1+rocm7.12.0a20260218` and got the expected result

<img width="499" height="673" alt="Image" src="https://github.com/user-attachments/assets/ffa6a9b7-370d-4d06-be98-d84a1a524092" />

Unfortunately, HY3D needs `bpy` which requires python3.11, and we don't have a ROCm 7.2 python3.11 docker image so I need a bit more time to verify if this issue is fixed in 7.2.

I would recommend switching to use TheRock nightlies if possible.

---

### 评论 #6 — manjunaths (2026-02-25T07:17:17Z)

Can you suggest the changes that you did ? I linked [my repo](https://github.com/manjunaths/HY3D-2.1-ROCm) with a Dockerfile and requirements.txt. 

Is it possible to make the changes to these two files to get them working with the r9700 ?

---

### 评论 #7 — zichguan-amd (2026-02-25T16:37:45Z)

This is a modified version of your Dockerfile that I verified to produce the above output using TheRock wheels.
```
FROM ubuntu:22.04
WORKDIR /root
RUN apt update && apt install -y python3.11 python3.11-venv git wget gcc g++ python3.11-dev curl libglib2.0-0 libxkbcommon0
RUN git clone https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1
COPY requirements.txt /root/Hunyuan3D-2.1
COPY generate3D.py /root/Hunyuan3D-2.1
COPY shape_gen.py /root/Hunyuan3D-2.1
COPY paint_gen.py /root/Hunyuan3D-2.1
#COPY wheels.tar.gz /root
#RUN tar -zxvf wheels.tar.gz
WORKDIR /root/Hunyuan3D-2.1

ENV VIRTUAL_ENV=/opt/venv
RUN python3.11 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"
RUN pip install "setuptools<70" wheel
RUN pip install torch torchaudio torchvision rocm[devel] \
    --index-url https://rocm.nightlies.amd.com/v2/gfx120X-all/
RUN pip install -r requirements.txt
#ENV MAKEFLAGS="-j8"
RUN apt install -y libgl1 libx11-dev libxi-dev libxxf86vm-dev libboost-dev libxrender-dev libglu1-mesa-dev freeglut3-dev mesa-common-dev
RUN pip install pymeshlab onnxruntime open3d

RUN rocm-sdk init
ENV ROCM_PATH="/opt/venv/lib/python3.11/site-packages/_rocm_sdk_devel"

WORKDIR /root/Hunyuan3D-2.1/hy3dpaint/custom_rasterizer
RUN python setup.py bdist_wheel
RUN pip install dist/custom_rasterizer-0.1-cp311-cp311-linux_x86_64.whl
WORKDIR /root/Hunyuan3D-2.1/hy3dpaint/DifferentiableRenderer
RUN ln -sf /usr/bin/python3.11-config /usr/bin/python3-config
RUN sh compile_mesh_painter.sh
WORKDIR /root/Hunyuan3D-2.1
# Stage 2 (texturing) needs RealESRGAN checkpoint
RUN mkdir -p hy3dpaint/ckpt \
    && curl -sL -o hy3dpaint/ckpt/RealESRGAN_x4plus.pth \
    "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
WORKDIR /root
COPY degradations.py /opt/venv/lib/python3.11/site-packages/basicsr/data/
WORKDIR /root/Hunyuan3D-2.1
ENV TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
# RUN python generate3D.py assets/demo.png
CMD ["/bin/bash"]
```

---

### 评论 #8 — manjunaths (2026-02-26T14:11:11Z)

This worked! Thank you so much.

---

### 评论 #9 — zichguan-amd (2026-02-26T14:37:44Z)

You're welcome! Glad it helped.

---
