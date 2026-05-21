# ROCm  on Ubuntu 22.04  Using PyTorch With  AMD RX-7900-XTX GPU

> **Issue #2866**
> **状态**: closed
> **创建时间**: 2024-02-04T04:20:10Z
> **更新时间**: 2024-09-13T15:24:15Z
> **关闭时间**: 2024-09-13T15:08:51Z
> **作者**: automatic-dolphin
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2866

## 描述

Hello,

I have ROCm installed on Ubuntu 22.04 . (dumps from  rocminfo and clinfo follow question)

I am trying various benchmarks for PyTorch.

It seems like PyTorch is still just using my CPU cores when testing benchmarks.

How can I test PyTorch and/or ROCm  using python3 to ensure use of the GPUs?

Thanks for any enlightenment.



'**rocminfo**' reports:

ROCm module is loaded
-----   
HSA System Attributes    
-----   
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          YES

'**HSA Agents**'              


'**Agent 1**'          
                
  Name:                    AMD Ryzen Threadripper PRO 5965WX 24-Cores
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen Threadripper PRO 5965WX 24-Cores
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
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    527984256(0x1f786680) KB           
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    527984256(0x1f786680) KB           
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    527984256(0x1f786680) KB           
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
                  
**Agent 2**                  
                 
  Name:                    gfx1100                            
  Uuid:                    GPU-0aac02dbebd629ee               
  Marketing Name:          Radeon RX 7900 XTX                 
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
  Max Clock Freq. (MHz):   2371                               
  BDFID:                   8960                               
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
                                 
'** Done **'            

'**clinfo**' reports:

Number of platforms:                             1
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3602.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback 


  Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               1
  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Board name:                                    Radeon RX 7900 XTX
  Device Topology:                               PCI[ B#35, D#0, F#0 ]
  Max compute units:                             48
  Max work items dimensions:                     3
    Max work items[0]:                           1024
    Max work items[1]:                           1024
    Max work items[2]:                           1024
  Max work group size:                           256
  Preferred vector width char:                   4
  Preferred vector width short:                  2
  Preferred vector width int:                    1
  Preferred vector width long:                   1
  Preferred vector width float:                  1
  Preferred vector width double:                 1
  Native vector width char:                      4
  Native vector width short:                     2
  Native vector width int:                       1
  Native vector width long:                      1
  Native vector width float:                     1
  Native vector width double:                    1
  Max clock frequency:                           2371Mhz
  Address bits:                                  64
  Max memory allocation:                         21890072576
  Image support:                                 Yes
  Max number of images read arguments:           128
  Max number of images write arguments:          8
  Max image 2D width:                            16384
  Max image 2D height:                           16384
  Max image 3D width:                            16384
  Max image 3D height:                           16384
  Max image 3D depth:                            8192
  Max samplers within kernel:                    16
  Max size of kernel argument:                   1024
  Alignment (bits) of base address:              1024
  Minimum alignment (bytes) for any datatype:    128
  Single precision floating point capability
    Denorms:                                     Yes
    Quiet NaNs:                                  Yes
    Round to nearest even:                       Yes
    Round to zero:                               Yes
    Round to +ve and infinity:                   Yes
    IEEE754-2008 fused multiply-add:             Yes
  Cache type:                                    Read/Write
  Cache line size:                               64
  Cache size:                                    32768
  Global memory size:                            25753026560
  Constant buffer size:                          21890072576
  Max number of constant args:                   8
  Local memory type:                             Scratchpad
  Local memory size:                             65536
  Max pipe arguments:                            16
  Max pipe active reservations:                  16
  Max pipe packet size:                          415236096
  Max global variable size:                      21890072576
  Max global variable preferred total size:      25753026560
  Max read/write image args:                     64
  Max on device events:                          1024
  Queue on device max size:                      8388608
  Max on device queues:                          1
  Queue on device preferred size:                262144
  SVM capabilities:                              
    Coarse grain buffer:                         Yes
    Fine grain buffer:                           Yes
    Fine grain system:                           No
    Atomics:                                     No
  Preferred platform atomic alignment:           0
  Preferred global atomic alignment:             0
  Preferred local atomic alignment:              0
  Kernel Preferred work group size multiple:     32
  Error correction support:                      0
  Unified memory for Host and Device:            0
  Profiling timer resolution:                    1
  Device endianess:                              Little
  Available:                                     Yes
  Compiler available:                            Yes
  Execution capabilities:                                
    Execute OpenCL kernels:                      Yes
    Execute native function:                     No
  Queue on Host properties:                              
    Out-of-Order:                                No
    Profiling :                                  Yes
  Queue on Device properties:                            
    Out-of-Order:                                Yes
    Profiling :                                  Yes
  Platform ID:                                   0x7fb2d71f0f90
  Name:                                          gfx1100
  Vendor:                                        Advanced Micro Devices, Inc.
  Device OpenCL C version:                       OpenCL C 2.0 
  Driver version:                                3602.0 (HSA1.1,LC)
  Profile:                                       FULL_PROFILE
  Version:                                       OpenCL 2.0 
  Extensions:                                    cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_depth_images cl_amd_copy_buffer_p2p cl_amd_assembly_program 




 

---

## 评论 (28 条)

### 评论 #1 — ErykDev (2024-02-05T13:50:54Z)

Hello,

Here is a simple script to test gpu usage.
[test-rocm.py.txt](https://github.com/ROCm/ROCm/files/14166421/test-rocm.py.txt)

make sure to use newest drivers
drivers : https://repo.radeon.com/amdgpu-install/23.40.2/

it's quite important to specify that you want rocm while installing
amdgpu-install --usecase=graphics,rocm

Also use pytorch/torchvision from AMD repos
pytorch/torchvision: https://repo.radeon.com/rocm/manylinux/rocm-rel-6.0/

Best of luck
Eryk Szmyt


---

### 评论 #2 — automatic-dolphin (2024-02-06T00:26:42Z)

Hello Erik,

Thanks for the pointer to the wheel files for torch and torch-vision.

After installing and validating ROCm, and testing with the utilities, I was trying to build pyTorch from source.
I kept getting an error related to libncurses6 not being able to find functions in libtinfo.

objdump shows the functions as available. I can only guess that the **python setup develop**  script is somehow getting the  -ltinfo  -L<path to tinfo>   in the wrong order for xxxxxxLINKER_FLAGS .

I will try the wheel files for now and continue to figure out the pyTorch build.





---

### 评论 #3 — terryrankine (2024-02-07T02:50:04Z)

So the pytorch stack seems to 'find itself' in the venv folder - so before you build - make sure you dont have other pytorch things in your venv....

delete torch* in your venv folder to make sure you get a clean one.

I can now build it against the 6.0.2 libs, and i have it working locally. I cant tell you if its built 'properly'.... but its working for me.

```
source /mnt/data/automatic1111/stable-diffusion-webui/venv/bin/activate
export PYTORCH_ROCM_ARCH=gfx1100
export USE_NINJA=1
export USE_CUDA=0
export USE_ROCM=1
export USE_LMDB=1
export USE_OPENCV=1
export MAX_JOBS=10


cd pytorch
git pull --recurse-submodules
git pull
python tools/amd_build/build_amd.py
python setup.py build install
./.ci/pytorch/build.sh
cd ..


cd vision
git pull --recurse-submodules
python setup.py develop
python setup.py build install
cd ..


cd audio
git pull --recurse-submodules
python setup.py develop
python setup.py build install
cd ..
```



---

### 评论 #4 — automatic-dolphin (2024-02-07T04:01:46Z)

Thanks Terry,

I will look at trying that. Seems similar to my build PyTorch process.

I think I may just be missing a couple symbolic links to  libtinfo   in /usr/lib .
The binaries for libtinfo seem to live in an architecture path. 
There is also no 'tinfo-config'. The CMake build would have difficulty finding the correct -L and -l   paths for GCC.


---

### 评论 #5 — terryrankine (2024-02-07T05:10:47Z)

https://packages.ubuntu.com/search?keywords=libtinfo

which one have you got installed?

---

### 评论 #6 — veb-101 (2024-02-07T19:47:40Z)

Unhelpful comment.

Please do post your benchmark results here if you get it running 🙌.

---

### 评论 #7 — briansp2020 (2024-02-07T21:36:02Z)

If using docker is OK, their latest pytorch docker build works on my 7900XTX

>docker pull rocm/pytorch:rocm6.0_ubuntu20.04_py3.9_pytorch_2.1.1

---

### 评论 #8 — automatic-dolphin (2024-02-08T00:30:02Z)

Thanks Brian,

I am not using a container. This is a build on a workstation.




---

### 评论 #9 — automatic-dolphin (2024-02-08T00:34:49Z)

Hello veb-101,

Of course. I will provide some benchmark results once i have them.
I will be programming C/C++ primarily, but was hoping to just use some of the existing python example benchmarks supplied at  rocm.amd  .  The torch wheel appears to have installed, I will be returning to working on the system in a couple days.

I will also post my findings and work-arounds for some of the undocumented 'gotchas'  that were encountered when installing ROCm and PyTorch.  Perhaps a full script that contains all the workarounds.

---

### 评论 #10 — terryrankine (2024-02-08T00:39:10Z)

#sidenote - https://python-poetry.org/ - pretty sure this would help the whole torch-vision and torch-audio depending on torch thing...... not my monkey.

I have the build working.

If you are building whl's in your venv - make sure you install wheel into that venv... stupid me....

I cant work out how to show you want is installed from the amd repos.... so here is my lazy approach....
```terryr@theblob:~$ dpkg -l | grep -E "rocm|hip|AMD "
ii  amd-smi-lib                                    23.4.2.60002-115~22.04                         amd64        AMD System Management libraries
ii  amd64-microcode                                3.20191218.1ubuntu2.2                          amd64        Processor microcode firmware for AMD CPUs
ii  composablekernel-dev                           1.1.0.60002-115~22.04                          amd64        High Performance Composable Kernel for AMD GPUs
ii  hip-dev                                        6.0.32831.60002-115~22.04                      amd64        HIP:Heterogenous-computing Interface for Portability
ii  hip-doc                                        6.0.32831.60002-115~22.04                      amd64        HIP:Heterogenous-computing Interface for Portability
ii  hip-runtime-amd                                6.0.32831.60002-115~22.04                      amd64        HIP:Heterogenous-computing Interface for Portability
ii  hip-samples                                    6.0.32831.60002-115~22.04                      amd64        HIP: Heterogenous-computing Interface for Portability [HIP SAMPLES]
ii  hipblas                                        2.0.0.60002-115~22.04                          amd64        Radeon Open Compute BLAS marshalling library
ii  hipblas-dev                                    2.0.0.60002-115~22.04                          amd64        Radeon Open Compute BLAS marshalling library
ii  hipblaslt                                      0.6.0.60002-115~22.04                          amd64        Radeon Open Compute BLAS marshalling library
ii  hipblaslt-dev                                  0.6.0.60002-115~22.04                          amd64        Radeon Open Compute BLAS marshalling library
ii  hipcc                                          1.0.0.60002-115~22.04                          amd64        HIP Compiler Driver
ii  hipcub-dev                                     3.0.0.60002-115~22.04                          amd64        hipCUB (rocPRIM backend)
ii  hipfft                                         1.0.13.60002-115~22.04                         amd64        ROCm FFT marshalling library
ii  hipfft-dev                                     1.0.13.60002-115~22.04                         amd64        ROCm FFT marshalling library
ii  hipfort-dev                                    0.4.0.60002-115~22.04                          amd64        Fortran Interface For GPU Kernel Libraries
ii  hipify-clang                                   17.0.0.60002-115~22.04                         amd64        Hipify CUDA source
ii  hiprand                                        2.10.16.60002-115~22.04                        amd64        Radeon Open Compute RAND library
ii  hiprand-dev                                    2.10.16.60002-115~22.04                        amd64        Radeon Open Compute RAND library
ii  hipsolver                                      2.0.0.60002-115~22.04                          amd64        Radeon Open Compute LAPACK marshalling library
ii  hipsolver-dev                                  2.0.0.60002-115~22.04                          amd64        Radeon Open Compute LAPACK marshalling library
ii  hipsparse                                      3.0.0.60002-115~22.04                          amd64        ROCm SPARSE library
ii  hipsparse-dev                                  3.0.0.60002-115~22.04                          amd64        ROCm SPARSE library
ii  hiptensor                                      1.1.0.60002-115~22.04                          amd64        Adaptation library of tensor contraction with composable_kernel backend
ii  hiptensor-dev                                  1.1.0.60002-115~22.04                          amd64        Adaptation library of tensor contraction with composable_kernel backend
ii  hsa-amd-aqlprofile                             1.0.0.60002.60002-115~22.04                    amd64        AQLPROFILE library for AMD HSA runtime API extension support
ii  hsa-rocr                                       1.12.0.60002-115~22.04                         amd64        AMD Heterogeneous System Architecture HSA - Linux HSA Runtime for Boltzmann (ROCm) platforms
ii  hsa-rocr-dev                                   1.12.0.60002-115~22.04                         amd64        AMD Heterogeneous System Architecture HSA development package.
ii  libflashrom1:amd64                             1.2-5build1                                    amd64        Identify, read, write, erase, and verify BIOS/ROM/flash chips - library
ii  libresid-builder0c2a                           2.1.1-15ubuntu2                                amd64        SID chip emulation class based on resid
ii  miopen-hip                                     3.00.0.60002-115~22.04                         amd64        AMD's DNN Library
ii  miopen-hip-dev                                 3.00.0.60002-115~22.04                         amd64        AMD's DNN Library
ii  mivisionx                                      2.5.0.60002-115~22.04                          amd64        AMD MIVisionX is a comprehensive Computer Vision and ML Inference Toolkit
ii  rocblas                                        4.0.0.60002-115~22.04                          amd64        rocBLAS is AMD's library for BLAS on ROCm. It is implemented in HIP and optimized for AMD GPUs.
ii  rocblas-dev                                    4.0.0.60002-115~22.04                          amd64        rocBLAS is AMD's library for BLAS on ROCm. It is implemented in HIP and optimized for AMD GPUs.
ii  rocm                                           6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) software stack meta package
ii  rocm-clang-ocl                                 0.5.0.60002-115~22.04                          amd64        OpenCL compilation with clang compiler.
ii  rocm-cmake                                     0.11.0.60002-115~22.04                         amd64        rocm-cmake built using CMake
ii  rocm-core                                      6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-dbgapi                                    0.71.0.60002-115~22.04                         amd64        Library to provide AMD GPU debugger API
ii  rocm-debug-agent                               2.0.3.60002-115~22.04                          amd64        Radeon Open Compute Debug Agent (ROCdebug-agent)
ii  rocm-dev                                       6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-developer-tools                           6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-device-libs                               1.0.0.60002-115~22.04                          amd64        Radeon Open Compute - device libraries
ii  rocm-gdb                                       13.2.60002-115~22.04                           amd64        ROCgdb
ii  rocm-hip-libraries                             6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime                               6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime-dev                           6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-sdk                                   6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-language-runtime                          6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-libs                                      6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-llvm                                      17.0.0.24012.60002-115~22.04                   amd64        ROCm compiler
ii  rocm-ml-libraries                              6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-ml-sdk                                    6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-ocl-icd                                   2.0.0.60002-115~22.04                          amd64        clr built using CMake
ii  rocm-opencl                                    2.0.0.60002-115~22.04                          amd64        clr built using CMake
ii  rocm-opencl-dev                                2.0.0.60002-115~22.04                          amd64        clr built using CMake
ii  rocm-opencl-runtime                            6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-opencl-sdk                                6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-openmp-sdk                                6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) OpenMP Software development Kit.
ii  rocm-smi-lib                                   6.0.0.60002-115~22.04                          amd64        AMD System Management libraries
ii  rocm-utils                                     6.0.2.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocminfo                                       1.0.0.60002-115~22.04                          amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool
ii  rocprofiler                                    2.0.60002.60002-115~22.04                      amd64        ROCPROFILER library for AMD HSA runtime API extension support
ii  rocprofiler-dev                                2.0.60002.60002-115~22.04                      amd64        ROCPROFILER library for AMD HSA runtime API extension support
ii  rocprofiler-plugins                            2.0.60002.60002-115~22.04                      amd64        ROCPROFILER library for AMD HSA runtime API extension support
ii  rocsolver                                      3.24.0.60002-115~22.04                         amd64        AMD ROCm SOLVER library
ii  rocsolver-dev                                  3.24.0.60002-115~22.04                         amd64        AMD ROCm SOLVER library
ii  roctracer                                      4.1.60002.60002-115~22.04                      amd64        AMD ROCTRACER library
ii  roctracer-dev                                  4.1.60002.60002-115~22.04                      amd64        AMD ROCTRACER library
ii  whiptail                                       0.52.21-5ubuntu2                               amd64        Displays user-friendly dialog boxes from shell scripts
```


---

### 评论 #11 — terryrankine (2024-02-08T00:45:35Z)

and that looks like this
```
-- Git branch: main
-- Git SHA: 02586da797dbfa201721d2080e2171805202f72c
-- Git tag: None
-- PyTorch dependency: torch
-- Building version 2.2.0a0+02586da
running bdist_wheel
running build
running build_py
copying src/torchaudio/version.py -> build/lib.linux-x86_64-3.10/torchaudio
running build_ext
Building PyTorch for GPU arch: gfx1100
HIP VERSION: 6.0.32831-204d35d16
-- Caffe2: Header version is: 6.0.2

***** ROCm version from rocm_version.h ****

ROCM_VERSION_DEV: 6.0.2
ROCM_VERSION_DEV_MAJOR: 6
ROCM_VERSION_DEV_MINOR: 0
ROCM_VERSION_DEV_PATCH: 2
ROCM_VERSION_DEV_INT:   60002
HIP_VERSION_MAJOR: 6
HIP_VERSION_MINOR: 0
TORCH_HIP_VERSION: 600

***** Library versions from dpkg *****

rocm-dev VERSION: 6.0.2.60002-115~22.04
rocm-developer-tools VERSION: 6.0.2.60002-115~22.04
rocm-device-libs VERSION: 1.0.0.60002-115~22.04
rocm-libs VERSION: 6.0.2.60002-115~22.04
hsakmt-roct-dev VERSION: 20231016.2.245.60002-115~22.04
hsa-rocr-dev VERSION: 1.12.0.60002-115~22.04

***** Library versions from cmake find_package *****

hip VERSION: 6.0.24015
hsa-runtime64 VERSION: 1.12.60002
amd_comgr VERSION: 2.6.0
rocrand VERSION: 3.0.0
hiprand VERSION: 2.10.16
rocblas VERSION: 4.0.0
hipblas VERSION: 2.0.0
hipblaslt VERSION: 0.6.0
miopen VERSION: 3.00.0
hipfft VERSION: 1.0.13
hipsparse VERSION: 3.0.0
rccl VERSION: 2.18.3
rocprim VERSION: 3.0.0
hipcub VERSION: 3.0.0
rocthrust VERSION: 3.0.0
hipsolver VERSION: 2.0.0
hipblaslt is NOT using custom data type
hipblaslt is NOT using custom compute type
```

which happily compiles 


---

### 评论 #12 — automatic-dolphin (2024-02-08T00:55:27Z)

Very nice Terry.

I have ROCm installed and working already.

My only (current) issue is performing a local build of PyTorch for installing into Anaconda.

The PyTorch build has no complaints at all about ROCm. The **setup.py**  for PyTorch is not finding  **libtinfo.so**  during link. This is indirectly a complaint about missing references on behalf of **NCURSES6**  .

![Screen Shot 2024-02-07 at 16 48 25](https://github.com/ROCm/ROCm/assets/158794430/99896b44-39eb-4aea-add4-ebd2a73f482e)





---

### 评论 #13 — terryrankine (2024-02-08T01:05:27Z)

sorry @automatic-dolphin - im not using anaconda here. and dont have your build tree / command to try replicate


---

### 评论 #14 — terryrankine (2024-02-08T01:08:32Z)

> https://packages.ubuntu.com/search?keywords=libtinfo
> 
> which one have you got installed?

did this ever get answered?

---

### 评论 #15 — automatic-dolphin (2024-02-08T01:14:04Z)

Here are the tinfo packages.


--------------------------------------------------------------------------------------
apt list --installed | grep tinfo

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

lib32tinfo6/jammy-updates,jammy-security,now 6.3-2ubuntu0.1 amd64 [installed]
libtinfo-dev/jammy-updates,jammy-security,now 6.3-2ubuntu0.1 amd64 [installed,automatic]
libtinfo5/jammy-updates,jammy-security,now 6.3-2ubuntu0.1 amd64 [installed,automatic]
libtinfo6/jammy-updates,jammy-security,now 6.3-2ubuntu0.1 amd64 [installed]
libtinfo6/jammy-updates,jammy-security,now 6.3-2ubuntu0.1 i386 [installed,automatic]

----------------------------------------------------------------------------------------

Here are AMD GPU packages

amdgpu-core/jammy,jammy,now 1:6.0.60001-1710620.22.04 all [installed,automatic]
amdgpu-dkms-firmware/jammy,jammy,now 1:6.3.6.60001-1710620.22.04 all [installed,automatic]
amdgpu-dkms/jammy,jammy,now 1:6.3.6.60001-1710620.22.04 all [installed]
amdgpu-install/jammy,jammy,now 6.0.60001-1710620.22.04 all [installed]
amdgpu-lib32/jammy,now 1:6.0.60001-1710620.22.04 amd64 [installed]
amdgpu-lib/jammy,now 1:6.0.60001-1710620.22.04 amd64 [installed]
amdgpu-pro-core/now 23.40-1710631.22.04 all [installed,local]
gst-omx-amdgpu/jammy,now 1:1.0.0.1.60001-1710620.22.04 amd64 [installed,automatic]
libdrm-amdgpu-amdgpu1/jammy,now 1:2.4.116.60001-1710620.22.04 amd64 [installed]
libdrm-amdgpu-amdgpu1/jammy,now 1:2.4.116.60001-1710620.22.04 i386 [installed,automatic]
libdrm-amdgpu-common/jammy,jammy,now 1.0.0.60001-1716197.22.04 all [installed,automatic]
libdrm-amdgpu-dev/jammy,now 1:2.4.116.60001-1710620.22.04 amd64 [installed]
libdrm-amdgpu-radeon1/jammy,now 1:2.4.116.60001-1710620.22.04 amd64 [installed,automatic]
libdrm-amdgpu-radeon1/jammy,now 1:2.4.116.60001-1710620.22.04 i386 [installed,automatic]
libdrm-amdgpu-utils/jammy,now 1:2.4.116.60001-1710620.22.04 amd64 [installed]
libdrm-amdgpu1/jammy-updates,now 2.4.113-2~ubuntu0.22.04.1 amd64 [installed]
libdrm-amdgpu1/jammy-updates,now 2.4.113-2~ubuntu0.22.04.1 i386 [installed,automatic]
libdrm2-amdgpu/jammy,now 1:2.4.116.60001-1710620.22.04 amd64 [installed]
libdrm2-amdgpu/jammy,now 1:2.4.116.60001-1710620.22.04 i386 [installed,automatic]
libegl1-amdgpu-mesa-drivers/jammy,now 1:23.3.0.60001-1710620.22.04 amd64 [installed,automatic]
libegl1-amdgpu-mesa-drivers/jammy,now 1:23.3.0.60001-1710620.22.04 i386 [installed,automatic]
libegl1-amdgpu-mesa/jammy,now 1:23.3.0.60001-1710620.22.04 amd64 [installed,automatic]
libegl1-amdgpu-mesa/jammy,now 1:23.3.0.60001-1710620.22.04 i386 [installed,automatic]
libgbm1-amdgpu/jammy,now 1:23.3.0.60001-1710620.22.04 amd64 [installed,automatic]
libgbm1-amdgpu/jammy,now 1:23.3.0.60001-1710620.22.04 i386 [installed,automatic]
libgl1-amdgpu-mesa-dri/jammy,now 1:23.3.0.60001-1710620.22.04 amd64 [installed,automatic]
libgl1-amdgpu-mesa-dri/jammy,now 1:23.3.0.60001-1710620.22.04 i386 [installed,automatic]
libgl1-amdgpu-mesa-glx/jammy,now 1:23.3.0.60001-1710620.22.04 amd64 [installed,automatic]
libgl1-amdgpu-mesa-glx/jammy,now 1:23.3.0.60001-1710620.22.04 i386 [installed,automatic]
libglapi-amdgpu-mesa/jammy,now 1:23.3.0.60001-1710620.22.04 amd64 [installed,automatic]
libglapi-amdgpu-mesa/jammy,now 1:23.3.0.60001-1710620.22.04 i386 [installed,automatic]
libllvm17.0.60001-amdgpu/jammy,now 1:17.0.60001-1710620.22.04 amd64 [installed,automatic]
libllvm17.0.60001-amdgpu/jammy,now 1:17.0.60001-1710620.22.04 i386 [installed,automatic]
libva-amdgpu-drm2/jammy,now 2.16.0.60001-1710620.22.04 amd64 [installed,automatic]
libva-amdgpu-drm2/jammy,now 2.16.0.60001-1710620.22.04 i386 [installed,automatic]
libva-amdgpu-glx2/jammy,now 2.16.0.60001-1710620.22.04 amd64 [installed,automatic]
libva-amdgpu-glx2/jammy,now 2.16.0.60001-1710620.22.04 i386 [installed,automatic]
libva-amdgpu-wayland2/jammy,now 2.16.0.60001-1710620.22.04 amd64 [installed,automatic]
libva-amdgpu-wayland2/jammy,now 2.16.0.60001-1710620.22.04 i386 [installed,automatic]
libva-amdgpu-x11-2/jammy,now 2.16.0.60001-1710620.22.04 amd64 [installed,automatic]
libva-amdgpu-x11-2/jammy,now 2.16.0.60001-1710620.22.04 i386 [installed,automatic]
libva2-amdgpu/jammy,now 2.16.0.60001-1710620.22.04 amd64 [installed,automatic]
libva2-amdgpu/jammy,now 2.16.0.60001-1710620.22.04 i386 [installed,automatic]
libwayland-amdgpu-client0/jammy,now 1.22.0.60001-1710620.22.04 amd64 [installed,automatic]
libwayland-amdgpu-client0/jammy,now 1.22.0.60001-1710620.22.04 i386 [installed,automatic]
libwayland-amdgpu-egl1/jammy,now 1.22.0.60001-1710620.22.04 i386 [installed,automatic]
libwayland-amdgpu-server0/jammy,now 1.22.0.60001-1710620.22.04 amd64 [installed,automatic]
libwayland-amdgpu-server0/jammy,now 1.22.0.60001-1710620.22.04 i386 [installed,automatic]
libxatracker2-amdgpu/jammy,now 1:23.3.0.60001-1710620.22.04 amd64 [installed,automatic]
libxatracker2-amdgpu/jammy,now 1:23.3.0.60001-1710620.22.04 i386 [installed,automatic]
mesa-amdgpu-omx-drivers/jammy,now 1:23.3.0.60001-1710620.22.04 amd64 [installed,automatic]
mesa-amdgpu-va-drivers/jammy,now 1:23.3.0.60001-1710620.22.04 amd64 [installed,automatic]
mesa-amdgpu-va-drivers/jammy,now 1:23.3.0.60001-1710620.22.04 i386 [installed,automatic]
mesa-amdgpu-vdpau-drivers/jammy,now 1:23.3.0.60001-1710620.22.04 amd64 [installed,automatic]
mesa-amdgpu-vdpau-drivers/jammy,now 1:23.3.0.60001-1710620.22.04 i386 [installed,automatic]
vulkan-amdgpu-pro/now 23.40-1710631.22.04 amd64 [installed,local]
vulkan-amdgpu-pro/now 23.40-1710631.22.04 i386 [installed,local]
vulkan-amdgpu/jammy,now 23.40-1710631.22.04 amd64 [installed]
xserver-xorg-amdgpu-video-amdgpu/jammy,now 1:22.0.0.60001-1710620.22.04 amd64 [installed,automatic]
xserver-xorg-video-amdgpu/jammy-updates,now 22.0.0-1ubuntu0.2 amd64 [installed,automatic]

-----------------------------------------------------------------------------------------------

Here are ROCm packages.


rocm-clang-ocl/jammy,now 0.5.0.60001-108~22.04 amd64 [installed,automatic]
rocm-cmake/jammy,now 0.11.0.60001-108~22.04 amd64 [installed,automatic]
rocm-core/jammy,now 6.0.1.60001-108~22.04 amd64 [installed,automatic]
rocm-dbgapi/jammy,now 0.71.0.60001-108~22.04 amd64 [installed,automatic]
rocm-debug-agent/jammy,now 2.0.3.60001-108~22.04 amd64 [installed,automatic]
rocm-dev/jammy,now 6.0.1.60001-108~22.04 amd64 [installed]
rocm-developer-tools/jammy,now 6.0.1.60001-108~22.04 amd64 [installed]
rocm-device-libs/jammy,now 1.0.0.60001-108~22.04 amd64 [installed,automatic]
rocm-gdb/jammy,now 13.2.60001-108~22.04 amd64 [installed,automatic]
rocm-hip-libraries/jammy,now 6.0.1.60001-108~22.04 amd64 [installed,automatic]
rocm-hip-runtime-dev/jammy,now 6.0.1.60001-108~22.04 amd64 [installed,automatic]
rocm-hip-runtime/jammy,now 6.0.1.60001-108~22.04 amd64 [installed]
rocm-hip-sdk/jammy,now 6.0.1.60001-108~22.04 amd64 [installed]
rocm-language-runtime/jammy,now 6.0.1.60001-108~22.04 amd64 [installed,automatic]
rocm-llvm/jammy,now 17.0.0.24012.60001-108~22.04 amd64 [installed,automatic]
rocm-ml-libraries/jammy,now 6.0.1.60001-108~22.04 amd64 [installed,automatic]
rocm-ml-sdk/jammy,now 6.0.1.60001-108~22.04 amd64 [installed]
rocm-ocl-icd/jammy,now 2.0.0.60001-108~22.04 amd64 [installed,automatic]
rocm-opencl-dev/jammy,now 2.0.0.60001-108~22.04 amd64 [installed,automatic]
rocm-opencl-runtime/jammy,now 6.0.1.60001-108~22.04 amd64 [installed]
rocm-opencl-sdk/jammy,now 6.0.1.60001-108~22.04 amd64 [installed]
rocm-opencl/jammy,now 2.0.0.60001-108~22.04 amd64 [installed,automatic]
rocm-openmp-sdk/jammy,now 6.0.1.60001-108~22.04 amd64 [installed]
rocm-smi-lib/jammy,now 6.0.0.60001-108~22.04 amd64 [installed,automatic]
rocm-utils/jammy,now 6.0.1.60001-108~22.04 amd64 [installed]
rocminfo/jammy,now 1.0.0.60001-108~22.04 amd64 [installed,automatic]

NOTE: the crossed out lines are an artefact of the forum, they are not supposed to be crossed out.

---

### 评论 #16 — automatic-dolphin (2024-02-08T01:19:27Z)

My PyTorch build is just using the simple instructions, and a few of peoples suggestions.

#get a fresh copy of the PyTorch repo
git clone https://github.com/pytorch/pytorch.git

#move into the download directory
cd pytorch/

#set some environnment variables
export PYTORCH_ROCM_ARCH=gfx1100
export USE_NINJA=1
export USE_CUDA=0
export USE_ROCM=1
export USE_LMDB=1
export USE_OPENCV=1
export MAX_JOBS=10

#make sure the git is fresh
git pull --recurse-submodules
git pull

#let it know its AMD
python tools/amd_build/build_amd.py

#run setup
python setup.py develop






---

### 评论 #17 — terryrankine (2024-02-08T01:41:37Z)

my only comment is 6.0.2 is out now.....
and
`libtinfo-dev` and `libncurses-dev` would be the only things i can think of that should be there for the compile.

why its not finding it - no idea...

---

### 评论 #18 — automatic-dolphin (2024-02-08T01:56:20Z)

I had  **libtinfo-dev** but removed it to see if it was interfering.

You just made me think of something though. I will add those  dev packages back.

The thing that I am thinking of is when I ran  '**rocm-install**'  to do the ROCm build,  one of the missing bits in the documentation was that part of ROCm relies on legacy i386 architecture packages. ROCm would not build for me without:

**sudo dpkg --add-architecture i386**

My distro did not have both **amd64**  and  **i386** .

Once I added i386, ROCm built just fine.

**arch-test
amd64
i386** 


I am now wondering if I need to specify an install of  libtinfo:i386  because ROCm was originally linked against i386 libtinfo ...(?)


Anyone see that as a possibility?












---

### 评论 #19 — terryrankine (2024-02-08T01:57:23Z)

im not a 32 guy

my amdinstall always has --no-32 on it....

---

### 评论 #20 — automatic-dolphin (2024-02-08T02:03:49Z)

I used **amdgpu-install**  from the available amd.rocm  packages.

wget https://repo.radeon.com/amdgpu-install/6.0.2/ubuntu/jammy/amdgpu-install_6.0.60002-1_all.deb
 
sudo dpkg -i amdgpu-install_6.0.60002-1_all.deb

sudo amdgpu-install --usecase=rocm,rocmdev,rocmdevtools,opencl,hip,hiplibsdk,graphics,dkms --vulkan=amdvlk,pro -y --accept-eula





---

### 评论 #21 — terryrankine (2024-02-08T02:24:17Z)

read those two lines super closely....

you downloaded one thing and installed another....



---

### 评论 #22 — terryrankine (2024-02-08T02:24:55Z)

and is there any reason you wanted the 32bit versions?


---

### 评论 #23 — automatic-dolphin (2024-02-09T00:09:31Z)

Yeah, the deb versions are different. 
I aggregated some commands from two different shell histories. 
Hence the difference in the deb versions. The commands are from two different machines but used to provide context.
Good catch. I updated the post.

I think the only reason I added i386 as an architecture was I missed the  **--no-32**   flag.  The added architecture was the problem with the PyTorch build I believe. I am making a clean, 64 bit only, system to test this stuff. Should know in a day or so.

Incidentally, that was a brilliant bit of information from you.  I went and did **amdgpu-install --help**  and there it was. 

---

### 评论 #24 — terryrankine (2024-02-09T00:45:11Z)

So

- No 32bit
- Make sure you install whatever the latest is (6.0.2) at the time of this post, as your package list shows 6.0.1 packages installed....
- make sure you have the -dev package installed for anything you want to link to
- be careful about pytorch linking to old versions of itself in the pypath. I delete from site-packages before I build. 

I think that's about all my advice 

---

### 评论 #25 — automatic-dolphin (2024-02-09T04:34:42Z)

It's in the midst of the build now.      Very exciting!!!

This will show if all the settings result in a good  build of pytorch.

---

### 评论 #26 — terryrankine (2024-02-09T04:43:14Z)

well - i just closed my ticket.... even though no one cared for 2.5months - https://github.com/ROCm/ROCm/issues/2689

but i finally have something i cant crash in 4 mins


---

### 评论 #27 — ppanchad-amd (2024-06-19T19:14:27Z)

@automatic-dolphin Have you resolved your issue? If so, please close the ticket. Thanks!

---

### 评论 #28 — harkgill-amd (2024-09-13T15:08:51Z)

Hi @automatic-dolphin, did you get a chance to try the ROCm 6.1 or 6.2 PyTorch wheels for installation? After successful installation, you can use the `HIP_VISIBLE_DEVICES` environment variable to target your GPU, ensuring it's usage. Here is the latest documentation on [using a wheels package](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html#using-a-wheels-package) to install PyTorch and also on [GPU Isolation Techniques](https://rocm.docs.amd.com/en/latest/conceptual/gpu-isolation.html#hip-visible-devices). 

The following output is from the MNIST example using a 7900XTX.
```
Train Epoch: 1 [57600/60000 (96%)]      Loss: 0.096597
Train Epoch: 1 [58240/60000 (97%)]      Loss: 0.135910
Train Epoch: 1 [58880/60000 (98%)]      Loss: 0.027735
Train Epoch: 1 [59520/60000 (99%)]      Loss: 0.063364

Test set: Average loss: 0.0523, Accuracy: 9822/10000 (98%)
```

I will close out this ticket. If you do still encounter issues following these steps, please leave a comment and I will re-open this ticket. Thanks!

---
