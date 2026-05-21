# [Issue]: AMD Clang 18 not correctly linking to math libraries | lld: error: undefined hidden symbol: expf

> **Issue #3573**
> **状态**: closed
> **创建时间**: 2024-08-13T01:36:00Z
> **更新时间**: 2024-11-07T16:23:06Z
> **关闭时间**: 2024-11-07T16:23:06Z
> **作者**: YellowRoseCx
> **标签**: Under Investigation, AMD Radeon Pro W6800, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3573

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon Pro W6800** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

When compiling a C++ project with Clang 18 from the latest ROCm 6.2.0 install, when using the flag: ``-fmath-errno`` I get this error: ``lld: error: undefined hidden symbol: expf`` eventually followed by ``clang++: error: amdgcn-link command failed with exit code 1 (use -v to see invocation)``

While trying to fix the issue, I reinstalled ROCm 6.1.2 and compiled the same code using AMD Clang 17 by using the environment variable ``ROCM_PATH=/opt/rocm-6.1.2`` and had no issues, everything compiled fine. Also compiled fine when using the ROCm 6.2.0 path/files, but specifying the makefile to use Clang 17 from ROCm v6.1.2




### Operating System

Linux Mint 21.3 (Virginia)

### CPU

12th Gen Intel(R) Core(TM) i5-12600K

### GPU

AMD Radeon RX 6800 XT

### ROCm Version

ROCm 6.2.0

### ROCm Component

llvm-project

### Steps to Reproduce

1. Install ROCm 6.2.0 in full and have a supported GPU installed
2. Compile the source code (modify -j as needed):
```
git clone https://github.com/YellowRoseCx/koboldcpp-rocm.git -b v1.72.yr0-ROCm
make LLAMA_HIPBLAS=1 -j14
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module version 6.8.5 is loaded
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
  Name:                    12th Gen Intel(R) Core(TM) i5-12600K
  Uuid:                    CPU-XX                             
  Marketing Name:          12th Gen Intel(R) Core(TM) i5-12600K
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
  Max Clock Freq. (MHz):   5000                               
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
      Size:                    65698236(0x3ea79bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65698236(0x3ea79bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65698236(0x3ea79bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-05965f569492ad18               
  Marketing Name:          AMD Radeon RX 6800 XT              
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
    L3:                      131072(0x20000) KB                 
  Chip ID:                 29631(0x73bf)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2575                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            72                                 
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
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB              
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx1010                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 5600 XT              
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
  Chip ID:                 29471(0x731f)                      
  ASIC Revision:           2(0x2)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1780                               
  BDFID:                   2304                               
  Internal Node ID:        2                                  
  Compute Unit:            36                                 
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
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    1280(0x500)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 149                                
  SDMA engine uCode::      35                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    6275072(0x5fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    6275072(0x5fc000) KB               
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

```
$ ROCR_VISIBLE_DEVICES=0 CUDA_VISIBLE_DEVICES=0 make LLAMA_HIPBLAS=1 -j14
I llama.cpp build info: 
I UNAME_S:  Linux
I UNAME_P:  x86_64
I UNAME_M:  x86_64
I CFLAGS:   -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native
I CXXFLAGS: -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread
I LDFLAGS:  
I CC:       cc (Ubuntu 13.1.0-8ubuntu1~22.04) 13.1.0
I CXX:      g++ (Ubuntu 13.1.0-8ubuntu1~22.04) 13.1.0

cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -Ofast -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native  -c ggml/src/ggml.c -o ggml.o
cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -Ofast -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native  -c otherarch/ggml_v3.c -o ggml_v3.o
cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -Ofast -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native  -c otherarch/ggml_v2.c -o ggml_v2.o
cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -Ofast -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native  -c otherarch/ggml_v1.c -o ggml_v1.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -c expose.cpp -o expose.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -c gpttype_adapter.cpp -o gpttype_adapter.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -c otherarch/sdcpp/sdtype_adapter.cpp -o sdcpp_default.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -c otherarch/whispercpp/whisper_adapter.cpp -o whispercpp_default.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -c examples/llava/clip.cpp -o llavaclip_default.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -c examples/llava/llava.cpp -o llava.o
cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native -c ggml/src/ggml-backend.c -o ggml-backend_default.o
cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native -c ggml/src/ggml-alloc.c -o ggml-alloc.o
cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native -c ggml/src/ggml-aarch64.c -o ggml-aarch64.o
cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native  -c ggml/src/ggml-quants.c -o ggml-quants.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -c src/unicode.cpp -o unicode.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -c src/unicode-data.cpp -o unicode-data.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread  -c ggml/src/llamafile/sgemm.cpp -o sgemm.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -c common/common.cpp -o common.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -c common/sampling.cpp -o sampling.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -c common/grammar-parser.cpp -o grammar-parser.o
cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -Ofast -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native   -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include -c ggml/src/ggml.c -o ggml_v4_cublas.o
cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -Ofast -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native   -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include -c otherarch/ggml_v3.c -o ggml_v3_cublas.o
cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -Ofast -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native   -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include -c otherarch/ggml_v2.c -o ggml_v2_cublas.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread  -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include -c gpttype_adapter.cpp -o gpttype_adapter_cublas.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread  -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include -c otherarch/sdcpp/sdtype_adapter.cpp -o sdcpp_cublas.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread  -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include -c otherarch/whispercpp/whisper_adapter.cpp -o whispercpp_cublas.o
g++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread  -c examples/llava/clip.cpp -o llavaclip_cublas.o
cc  -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c11   -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-deprecated -Wno-deprecated-declarations -pthread -march=native -mtune=native  -c ggml/src/ggml-backend.c -o ggml-backend_cublas.o
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml-cuda.o ggml/src/ggml-cuda.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml_v3-cuda.o otherarch/ggml_v3-cuda.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
otherarch/ggml_v3-cuda.cu:590:1: warning: function declared 'noreturn' should not return [-Winvalid-noreturn]
  590 | }
      | ^
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml_v2-cuda.o otherarch/ggml_v2-cuda.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml_v2-cuda-legacy.o otherarch/ggml_v2-cuda-legacy.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/acc.o ggml/src/ggml-cuda/acc.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/arange.o ggml/src/ggml-cuda/arange.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/argsort.o ggml/src/ggml-cuda/argsort.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/binbcast.o ggml/src/ggml-cuda/binbcast.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/clamp.o ggml/src/ggml-cuda/clamp.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/concat.o ggml/src/ggml-cuda/concat.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/convert.o ggml/src/ggml-cuda/convert.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/conv-transpose-1d.o ggml/src/ggml-cuda/conv-transpose-1d.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/cpy.o ggml/src/ggml-cuda/cpy.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/diagmask.o ggml/src/ggml-cuda/diagmask.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/dmmv.o ggml/src/ggml-cuda/dmmv.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/fattn.o ggml/src/ggml-cuda/fattn.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/fattn-tile-f16.o ggml/src/ggml-cuda/fattn-tile-f16.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/fattn-tile-f32.o ggml/src/ggml-cuda/fattn-tile-f32.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/getrows.o ggml/src/ggml-cuda/getrows.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/im2col.o ggml/src/ggml-cuda/im2col.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/mmq.o ggml/src/ggml-cuda/mmq.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
/opt/rocm/llvm/bin/clang++ -I. -Iggml/include -Iggml/src -Iinclude -Isrc -I./common -I./include -I./include/CL -I./otherarch -I./otherarch/tools -I./otherarch/sdcpp -I./otherarch/sdcpp/thirdparty -I./include/vulkan -O3 -fno-finite-math-only -fmath-errno -DNDEBUG -std=c++11 -fPIC -DLOG_DISABLE_LOGS -D_GNU_SOURCE -DGGML_USE_LLAMAFILE -pthread -s -Wno-multichar -Wno-write-strings -Wno-deprecated -Wno-deprecated-declarations -pthread -DGGML_USE_HIPBLAS -DGGML_USE_CUDA -DSD_USE_CUBLAS  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.2.0/include -I/include --offload-arch=gfx1030 -DGGML_CUDA_DMMV_X=32 -DGGML_CUDA_MMV_Y=1 -DK_QUANTS_PER_ITERATION=2 -x hip -c -o ggml/src/ggml-cuda/mmvq.o ggml/src/ggml-cuda/mmvq.cu
clang++: warning: argument unused during compilation: '-s' [-Wunused-command-line-argument]
lld: error: undefined hidden symbol: expf
>>> referenced by /tmp/fattn-gfx1030-87b27f.o:(void flash_attn_combine_results<256, 4>(float const*, HIP_vector_type<float, 2u> const*, float*))
>>> referenced by /tmp/fattn-gfx1030-87b27f.o:(void flash_attn_combine_results<256, 4>(float const*, HIP_vector_type<float, 2u> const*, float*))
>>> referenced by /tmp/fattn-gfx1030-87b27f.o:(void flash_attn_combine_results<256, 2>(float const*, HIP_vector_type<float, 2u> const*, float*))
>>> referenced 3 more times
clang++: error: amdgcn-link command failed with exit code 1 (use -v to see invocation)
make: *** [Makefile:274: ggml/src/ggml-cuda/fattn.o] Error 1
make: *** Waiting for unfinished jobs....
otherarch/ggml_v3-cuda.cu:5747:24: warning: loop not unrolled: the optimizer was unable to perform the requested transformation; the transformation might be disabled or specified as part of an unsupported transformation ordering [-Wpass-failed=transform-warning]
 5747 | static __global__ void soft_max_f32(const float * x, const float * y, float * dst, const int ncols_par, const int nrows_y, const float scale) {
      |                        ^
otherarch/ggml_v3-cuda.cu:5747:24: warning: loop not unrolled: the optimizer was unable to perform the requested transformation; the transformation might be disabled or specified as part of an unsupported transformation ordering [-Wpass-failed=transform-warning]
otherarch/ggml_v3-cuda.cu:5747:24: warning: loop not unrolled: the optimizer was unable to perform the requested transformation; the transformation might be disabled or specified as part of an unsupported transformation ordering [-Wpass-failed=transform-warning]
otherarch/ggml_v3-cuda.cu:5747:24: warning: loop not unrolled: the optimizer was unable to perform the requested transformation; the transformation might be disabled or specified as part of an unsupported transformation ordering [-Wpass-failed=transform-warning]
otherarch/ggml_v3-cuda.cu:5747:24: warning: loop not unrolled: the optimizer was unable to perform the requested transformation; the transformation might be disabled or specified as part of an unsupported transformation ordering [-Wpass-failed=transform-warning]
otherarch/ggml_v3-cuda.cu:5747:24: warning: loop not unrolled: the optimizer was unable to perform the requested transformation; the transformation might be disabled or specified as part of an unsupported transformation ordering [-Wpass-failed=transform-warning]
lld: error: undefined hidden symbol: expf
>>> referenced by /tmp/fattn-tile-f16-gfx1030-4a7125.o:(void flash_attn_combine_results<64, 4>(float const*, HIP_vector_type<float, 2u> const*, float*))
>>> referenced by /tmp/fattn-tile-f16-gfx1030-4a7125.o:(void flash_attn_combine_results<64, 4>(float const*, HIP_vector_type<float, 2u> const*, float*))
>>> referenced by /tmp/fattn-tile-f16-gfx1030-4a7125.o:(void flash_attn_combine_results<128, 4>(float const*, HIP_vector_type<float, 2u> const*, float*))
>>> referenced 5 more times
clang++: error: amdgcn-link command failed with exit code 1 (use -v to see invocation)
make: *** [Makefile:274: ggml/src/ggml-cuda/fattn-tile-f16.o] Error 1
lld: error: undefined hidden symbol: expf
>>> referenced by /tmp/fattn-tile-f32-gfx1030-726ef6.o:(void flash_attn_tile_ext_f32<64, 16, 8, 4>(char const*, char const*, char const*, char const*, float*, HIP_vector_type<float, 2u>*, float, float, float, float, unsigned int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int))
>>> referenced by /tmp/fattn-tile-f32-gfx1030-726ef6.o:(void flash_attn_tile_ext_f32<64, 16, 8, 4>(char const*, char const*, char const*, char const*, float*, HIP_vector_type<float, 2u>*, float, float, float, float, unsigned int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int))
>>> referenced by /tmp/fattn-tile-f32-gfx1030-726ef6.o:(void flash_attn_combine_results<64, 4>(float const*, HIP_vector_type<float, 2u> const*, float*))
>>> referenced 17 more times
clang++: error: amdgcn-link command failed with exit code 1 (use -v to see invocation)
make: *** [Makefile:274: ggml/src/ggml-cuda/fattn-tile-f32.o] Error 1
7 warnings generated when compiling for gfx1030.
lld: error: undefined hidden symbol: expf
>>> referenced by /tmp/ggml_v3-cuda-gfx1030-0d42b1.o:(silu_f32(float const*, float*, int))
>>> referenced by /tmp/ggml_v3-cuda-gfx1030-0d42b1.o:(silu_f32(float const*, float*, int))
>>> referenced by /tmp/ggml_v3-cuda-gfx1030-0d42b1.o:(gelu_quick_f32(float const*, float*, int))
>>> referenced 21 more times
clang++: error: amdgcn-link command failed with exit code 1 (use -v to see invocation)
make: *** [Makefile:282: ggml_v3-cuda.o] Error 1
```

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-08-21T14:52:20Z)

Hi @YellowRoseCx, I was able to reproduce the error by compiling the source code provided. I will create an internal ticket to further investigate this issue.

---

### 评论 #2 — schung-amd (2024-08-23T14:14:09Z)

Hi @YellowRoseCx, I've spoken to the internal team about this. ROCm does not support the `-fmath-errno` flag on the GPU, so passing this flag to clang is causing your issues. Previously, we were pulling in math functions which did not implement errno to begin with, so this was failing silently. We're looking at finding a way to allow passing `-fmath-errno` to clang without breaking things so that builds like yours can function as they used to. As a workaround for now, you can pass `-Xarch_host -fmath-errno` to clang instead of `-fmath-errno`, which will enable this flag on the host only.

---

### 评论 #3 — schung-amd (2024-11-07T16:23:06Z)

Closing this for now, this is on our radar and there is a corresponding issue upstream (https://github.com/llvm/llvm-project/issues/105776) but there is no clear timeline for a fix. In the meanwhile, the workaround should suffice.

---
