# [Issue]: ROCm 7.0.2 crashing instantly on gfx1151 (Strix Halo) with latest llama.cpp

> **Issue #5534**
> **状态**: closed
> **创建时间**: 2025-10-17T16:53:42Z
> **更新时间**: 2025-10-21T13:48:06Z
> **关闭时间**: 2025-10-17T19:40:50Z
> **作者**: SteelPh0enix
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5534

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

After building llama.cpp (b6786) with latest ROCm 7.0.2 built via Docker (Dockerfiles below), trying to start llama-server with any model results in ROCm error and crash from MUT_MAL error.

```
0.00.138.420 I load_tensors: loading model tensors, this can take a while... (mmap = true)
0.03.887.585 I load_tensors: offloading 40 repeating layers to GPU
0.03.887.588 I load_tensors: offloading output layer to GPU
0.03.887.589 I load_tensors: offloaded 41/41 layers to GPU
0.03.887.599 I load_tensors:        ROCm0 model buffer size = 19137.83 MiB
0.03.887.600 I load_tensors:   CPU_Mapped model buffer size =   680.00 MiB
...............................................................................................
0.04.485.078 W llama_init_from_model: model default pooling_type is [0], but [-1] was specified
0.04.485.312 I llama_context: constructing llama_context
0.04.485.313 I llama_context: n_seq_max     = 1
0.04.485.313 I llama_context: n_ctx         = 4096
0.04.485.314 I llama_context: n_ctx_per_seq = 4096
0.04.485.314 I llama_context: n_batch       = 2048
0.04.485.315 I llama_context: n_ubatch      = 512
0.04.485.315 I llama_context: causal_attn   = 1
0.04.485.316 I llama_context: flash_attn    = auto
0.04.485.316 I llama_context: kv_unified    = false
0.04.485.322 I llama_context: freq_base     = 1000000000.0
0.04.485.322 I llama_context: freq_scale    = 1
0.04.485.323 W llama_context: n_ctx_per_seq (4096) < n_ctx_train (131072) -- the full capacity of the model will not be utilized
0.04.498.866 I llama_context:  ROCm_Host  output buffer size =     0.50 MiB
0.04.526.894 I llama_kv_cache:      ROCm0 KV buffer size =   640.00 MiB
0.04.530.089 I llama_kv_cache: size =  640.00 MiB (  4096 cells,  40 layers,  1/1 seqs), K (f16):  320.00 MiB, V (f16):  320.00 MiB
0.04.530.656 I llama_context: Flash Attention was auto, set to enabled
0.04.546.491 I llama_context:      ROCm0 compute buffer size =   266.00 MiB
0.04.546.492 I llama_context:  ROCm_Host compute buffer size =    18.01 MiB
0.04.546.493 I llama_context: graph nodes  = 1247
0.04.546.493 I llama_context: graph splits = 2
0.04.546.508 I common_init_from_params: added </s> logit bias = -inf
0.04.546.972 I common_init_from_params: setting dry_penalty_last_n to ctx_size = 4096
0.04.546.972 W common_init_from_params: warming up the model with an empty run - please wait ... (--no-warmup to disable)
/buildroot/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:88: ROCm error
0.04.548.266 E ggml_cuda_compute_forward: MUL_MAT failed
0.04.548.271 E ROCm error: invalid device function
0.04.548.272 E   current device: 0, in function ggml_cuda_compute_forward at /buildroot/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:2540
0.04.548.272 E   err
[New LWP 43]
[New LWP 42]
[New LWP 41]
[New LWP 40]
[New LWP 39]
[New LWP 38]
[New LWP 37]
[New LWP 36]
[New LWP 35]
[New LWP 34]
[New LWP 33]
[New LWP 32]
[New LWP 31]
[New LWP 30]
[New LWP 29]
[New LWP 28]
[New LWP 27]
[New LWP 26]
[New LWP 25]
[New LWP 24]
[New LWP 23]
[New LWP 22]
[New LWP 21]
[New LWP 20]
[New LWP 19]
[New LWP 18]
[New LWP 17]
[New LWP 16]
[New LWP 15]
[New LWP 14]
[New LWP 13]
[New LWP 12]
[New LWP 11]
[New LWP 10]
[New LWP 7]
warning: could not find '.gnu_debugaltlink' file for /lib/x86_64-linux-gnu/liblber.so.2
warning: could not find '.gnu_debugaltlink' file for /lib/x86_64-linux-gnu/libbrotlidec.so.1
warning: could not find '.gnu_debugaltlink' file for /lib/x86_64-linux-gnu/libbrotlicommon.so.1
warning: 30     ../sysdeps/unix/sysv/linux/wait4.c: No such file or directory
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
0x00007fe9ceef6813 in __GI___wait4 (pid=44, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
#0  0x00007fe9ceef6813 in __GI___wait4 (pid=44, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
30      in ../sysdeps/unix/sysv/linux/wait4.c
#1  0x00007fe9cf3a5ae3 in ggml_print_backtrace () from /usr/local/lib/libggml-base.so
#2  0x00007fe9cf3a5c8b in ggml_abort () from /usr/local/lib/libggml-base.so
#3  0x00007fe9ce4ad1f2 in ggml_cuda_error(char const*, char const*, char const*, int, char const*) () from /usr/local/lib/libggml-hip.so
#4  0x00007fe9ce4b4387 in ggml_backend_cuda_graph_compute(ggml_backend*, ggml_cgraph*) () from /usr/local/lib/libggml-hip.so
#5  0x00007fe9cf3bf547 in ggml_backend_sched_graph_compute_async () from /usr/local/lib/libggml-base.so
#6  0x00007fe9cf4dfba1 in llama_context::graph_compute(ggml_cgraph*, bool) () from /usr/local/lib/libllama.so
#7  0x00007fe9cf4e15dc in llama_context::process_ubatch(llama_ubatch const&, llm_graph_type, llama_memory_context_i*, ggml_status&) () from /usr/local/lib/libllama.so
#8  0x00007fe9cf4e78cf in llama_context::decode(llama_batch const&) () from /usr/local/lib/libllama.so
#9  0x00007fe9cf4e87ef in llama_decode () from /usr/local/lib/libllama.so
#10 0x0000559f827fc60d in common_init_from_params(common_params&) ()
#11 0x0000559f826c7961 in server_context::load_model(common_params const&) ()
#12 0x0000559f82659b4c in main ()
[Inferior 1 (process 1) detached]
```

I've tested it with gpt-oss-120b, gpt-oss-20b and Devstral. Each resulted in the same error. Also checked both with and without flash-attention enabled, and both with and without ROCWMMA support enabled, no difference either.

### Operating System

NixOS 25.05

### CPU

AMD RYZEN AI MAX+ 395

### GPU

Radeon 8060S

### ROCm Version

7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

1. Build ROCm container using Dockerfile below (name it rocm7:latest for compatibility with llama.cpp dockerfile)
2. Build llama.cpp container using Dockerfile below
3. Try to run any model. I've used the following script (change LLM directory to your own):

```fish
#!/run/current-system/sw/bin/fish

set llms_dir ~/LLMs

function docker-rocm
    docker run --privileged --network=host --device=/dev/kfd --device=/dev/dri --group-add video --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --ipc=host --shm-size 24G -v $llms_dir:/llms -w /llms --rm $argv
end

function llm-server
    docker-rocm llamacpp:latest llama-server --log-prefix --log-timestamps --gpu-layers 999 --host 172.17.0.1 --port 51536 --timeout 60 --jinja $argv
end

set model_name $argv[1]

if [ $model_name = "gpt-oss-120b" ]
    llm-server --model "/llms/gpt-oss-120b-UD-Q6_K_XL.gguf" --ctx-size 4096
end

if [ $model_name = "gpt-oss-20b" ]
    llm-server --model "/llms/gpt-oss-20b.gguf" --ctx-size 4096
end

if [ $model_name = "devstral" ]
    llm-server --model "/llms/Devstral-Small-2507-UD-Q6_K_XL.gguf" --ctx-size 4096
end
```

4. llama-server should crash immediately after loading the model into memory.

If you want to check that on the same models i've used, download Unsloth's Q6_K_XL quant of gpt-oss-120b or Devstral-Small-2507.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
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
      Size:                    131165284(0x7d16c64) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131165284(0x7d16c64) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131165284(0x7d16c64) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131165284(0x7d16c64) KB            
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
  BDFID:                   49664                              
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
  Packet Processor uCode:: 32                                 
  SDMA engine uCode::      17                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    125829120(0x7800000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    125829120(0x7800000) KB            
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
*** Done ***

### Additional Information

Dockerfiles i've used to get ROCm and llama.cpp:

ROCm:

```dockerfile
FROM ubuntu:24.04
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# core packages
RUN apt-get update -q \
    && DEBIAN_FRONTEND=noninteractive apt-get install -qy --no-install-recommends \
    build-essential \
    bzip2 \
    ca-certificates \
    curl \
    environment-modules \
    git \
    git-lfs \
    gpg \
    netbase \
    python3-full \
    python3-pip \
    python3-setuptools \
    python3-venv \
    python3-wheel \
    sed \
    unzip \
    wget \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

# add AMD ROCm key
# Make the directory if it doesn't exist yet.
# This location is recommended by the distribution maintainers.
# Afterwards, cownload the key, convert the signing-key to a full
# keyring required by apt and store in the keyring directory
RUN mkdir --parents --mode=0755 /etc/apt/keyrings && \
    wget https://repo.radeon.com/rocm/rocm.gpg.key -O - | \
    gpg --dearmor | \
    tee /etc/apt/keyrings/rocm.gpg > /dev/null

# add repos
RUN echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/7.0.2 noble main" > /etc/apt/sources.list.d/rocm.list && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/graphics/7.0.2/ubuntu noble main" >> /etc/apt/sources.list.d/rocm.list

RUN echo "Package: *" > /etc/apt/preferences.d/rocm-pin-600 && \
    echo "Pin: release o=repo.radeon.com" >> /etc/apt/preferences.d/rocm-pin-600 && \
    echo "Pin-Priority: 600" >> /etc/apt/preferences.d/rocm-pin-600

# install ROCm
RUN apt-get update -q \
    && DEBIAN_FRONTEND=noninteractive apt-get install -qy \
    rocm \
    && rm -rf /var/lib/apt/lists/*

# setup user for GPU access
ARG DOCKER_USER_NAME=ubuntu
RUN groupadd render && usermod -aG render,video ${DOCKER_USER_NAME}

# add ROCm env vars
ENV HIP_PATH="/opt/rocm-7.0.2"
ENV HIPCXX="${HIP_PATH}/lib/llvm/bin/clang"
ENV HIP_DEVICE_LIB_PATH="${HIP_PATH}/lib/llvm/lib/clang/20/lib/amdgcn/bitcode/"
```

llama.cpp:

```
FROM rocm7:latest
WORKDIR /buildroot
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG DOCKER_USER_NAME=ubuntu

# setup prerequisites
USER root
RUN apt-get update -q \
    && DEBIAN_FRONTEND=noninteractive apt-get install -qy --no-install-recommends \
    cmake \
    curl \
    libcurl4-openssl-dev \
    libssl-dev \
    ninja-build \
    openssl \
    pipx \
    && rm -rf /var/lib/apt/lists/*

# configure environment
ARG GPU_ARCHS="gfx1151"
ARG HSA_OVERRIDE_GFX_VERSION="11.5.1"
ARG LLAMA_CPP_REPO="https://github.com/ggml-org/llama.cpp.git"
ARG LLAMA_CPP_BRANCH="master"

RUN chown -R ${DOCKER_USER_NAME} /buildroot
USER ${DOCKER_USER_NAME}

ENV USE_ROCM=1
ENV GPU_ARCHS=${GPU_ARCHS}
ENV HSA_OVERRIDE_GFX_VERSION=${HSA_OVERRIDE_GFX_VERSION}
ENV PATH=${PATH}:/home/ubuntu/.local/bin
ENV LLAMA_CPP_DIR="/buildroot/llama.cpp"
ENV LLAMA_CPP_BUILD_DIR="/buildroot/llama.cpp-build"
ENV LLAMA_CPP_VENV_DIR="/buildroot/.venv"
ENV LD_LIBRARY_PATH="/usr/local/lib"
ENV ROCBLAS_USE_HIPBLASLT=1

# setup python venv
RUN pipx install uv \
    && uv venv --python 3.13 ${LLAMA_CPP_VENV_DIR}

# add llama.cpp code
ADD ./llama.cpp ${LLAMA_CPP_DIR}
USER root
RUN chown -R ${DOCKER_USER_NAME} ${LLAMA_CPP_DIR}
USER ${DOCKER_USER_NAME}

# install llama.cpp deps
RUN source ${LLAMA_CPP_VENV_DIR}/bin/activate \
    && uv pip install --requirements ${LLAMA_CPP_DIR}/requirements.txt \
        --prerelease=allow \
        --index-strategy unsafe-best-match

# prepare llama.cpp build
RUN cmake -S ${LLAMA_CPP_DIR} -B ${LLAMA_CPP_BUILD_DIR} -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    # ROCm support
    -DGGML_HIP=ON \
    -DGPU_TARGETS=gfx1151 \
    -DGGML_HIP_ROCWMMA_FATTN=ON \
    # picking what to build
    -DLLAMA_STANDALONE=ON \
    -DLLAMA_BUILD_TESTS=OFF \
    -DLLAMA_BUILD_TOOLS=ON \
    -DLLAMA_BUILD_TOOLS=ON \
    -DLLAMA_BUILD_EXAMPLES=ON \
    -DLLAMA_BUILD_SERVER=ON \
    -DLLAMA_TOOLS_INSTALL=ON \
    -DLLAMA_CURL=ON \
    -DLLAMA_OPENSSL=ON \
    # additional ggml settings \
    -DGGML_NATIVE=ON \
    -DGGML_LTO=ON \
    -DGGML_CCACHE=OFF \
    -DGGML_CPU=ON \
    -DGGML_SSE42=ON \
    -DGGML_AVX=ON \
    -DGGML_AVX_VNNI=ON \
    -DGGML_AVX2=ON \
    -DGGML_BMI2=ON \
    -DGGML_AVX512=ON \
    -DGGML_AVX512_VBMI=ON \
    -DGGML_AVX512_VNNI=ON \
    -DGGML_AVX512_BF16=ON \
    -DGGML_FMA=ON \
    -DGGML_F16C=ON \
    -DGGML_CUDA_FA_ALL_QUANTS=ON \
    -DGGML_OPENMP=ON

# build llama.cpp
RUN cmake --build ${LLAMA_CPP_BUILD_DIR} --config Release -j 32
USER root
RUN cmake --install ${LLAMA_CPP_BUILD_DIR} --config Release
USER ${DOCKER_USER_NAME}
```

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2025-10-17T19:25:55Z)

Hi @SteelPh0enix, stepping back from the docker images, I wasn't able to reproduce the crashes with the following setup,

- Baremetal gfx1151 
- llama.cpp built from source (b6791) w/ flags you've shared
- ROCm 7.0.2 following the [ROCm on Ryzen](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#install-amd-unified-driver-package-repositories-and-installer-script) steps including oem kernel
- `llama-server -hf unsloth/gpt-oss-20b-GGUF:Q4_K_M` and or your expanded `llm-server` command

Could you give this config a try as well. It'll help narrow down whether the issue lies within the software stack or the docker images. Will try your steps in parallel as well. 

We normally see invalid device function errors when unsupported architectures are override through `HSA_OVERRIDE_GFX_VERSION`. In your case, `gfx1151` is already supported, removing ENV GPU_ARCHS=${GPU_ARCHS}
ENV HSA_OVERRIDE_GFX_VERSION=${HSA_OVERRIDE_GFX_VERSION} could potentially be a quick fix.

---

### 评论 #2 — SteelPh0enix (2025-10-17T19:40:50Z)

@harkgill-amd the issue seems to be located - as usual - between the keyboard and chair :)

I've used wrong define name when building llama.cpp - `GPU_TARGETS` instead of `AMDGPU_TARGETS`, after switching it to `AMDGPU_TARGETS` everything seems to work fine.

---

### 评论 #3 — harkgill-amd (2025-10-17T19:49:53Z)

Ah, that's in line with what the error was reporting - nice catch. 

llama.cpp's [rocm.Dockerfile](https://github.com/ggml-org/llama.cpp/blob/master/.devops/rocm.Dockerfile) might be good to reference as well when building your own Dockerfile.

---
