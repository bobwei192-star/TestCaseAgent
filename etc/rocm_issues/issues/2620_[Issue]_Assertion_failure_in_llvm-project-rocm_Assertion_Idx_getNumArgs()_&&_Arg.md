# [Issue]: Assertion failure in llvm-project-rocm: Assertion Idx < getNumArgs() && "Argument index out of range!" failed.

> **Issue #2620**
> **状态**: closed
> **创建时间**: 2023-11-02T00:27:14Z
> **更新时间**: 2024-10-21T13:21:28Z
> **关闭时间**: 2024-10-21T13:21:27Z
> **作者**: telans
> **标签**: Under Investigation, 5.6.0, 5.7.1
> **URL**: https://github.com/ROCm/ROCm/issues/2620

## 标签

- **Under Investigation** (颜色: #0052cc)
- **5.6.0** (颜色: #b60205)
- **5.7.1** (颜色: #b60205)

## 描述

### Problem Description

I am encountering a (frontend?) crash with rocm-llvm with the following trace:
```
$ /opt/rocm/llvm/bin/clang -target amdgcn-amd-amdhsa -nogpulib -o out reduced.ll 
clang-16: /usr/src/debug/rocm-llvm/llvm-project-rocm-5.6.1/clang/include/clang/Basic/Diagnostic.h:1590: clang::DiagnosticsEngine::ArgumentKind clang::Diagnostic::getArgKind(unsigned int) const: Assertion `Idx < getNumArgs() && "Argument index out of range!"' failed.
PLEASE submit a bug report to https://github.com/llvm/llvm-project/issues/ and include the crash backtrace, preprocessed source, and associated run script.
Stack dump:
0.      Program arguments: /opt/rocm/llvm/bin/clang-16 -cc1 -triple amdgcn-amd-amdhsa -emit-obj -mrelax-all -disable-free -clear-ast-before-backend -main-file-name reduced.ll -mrelocation-model pic -pic-level 1 -fhalf-no-semantic-interposition -mframe-pointer=all -ffp-contract=on -fno-rounding-math -mconstructor-aliases -fvisibility=hidden -fapply-global-visibility-to-externs -mllvm -treat-scalable-fixed-error-as-warning -debugger-tuning=gdb -resource-dir /opt/rocm/llvm/lib/clang/16.0.0 -fdebug-compilation-dir=/tmp/cvise -ferror-limit 19 -nogpulib -fcolor-diagnostics -faddrsig -o /tmp/reduced-ae3ff8.o -x ir reduced.ll
1.      Code generation
2.      Running pass 'Function Pass Manager' on module 'reduced.ll'.
3.      Running pass 'AMDGPU Assembly Printer' on function '@x'
 #0 0x00005638c2744993 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) (/opt/rocm/llvm/bin/clang-16+0x2c81993)
 #1 0x00005638c2741b8f llvm::sys::RunSignalHandlers() (/opt/rocm/llvm/bin/clang-16+0x2c7eb8f)
 #2 0x00005638c2741cdd (/opt/rocm/llvm/bin/clang-16+0x2c7ecdd)
 #3 0x00007f6ad0c5c710 (/usr/lib/libc.so.6+0x3e710)
 #4 0x00007f6ad0cac83c (/usr/lib/libc.so.6+0x8e83c)
 #5 0x00007f6ad0c5c668 gsignal (/usr/lib/libc.so.6+0x3e668)
 #6 0x00007f6ad0c444b8 abort (/usr/lib/libc.so.6+0x264b8)
 #7 0x00007f6ad0c443dc (/usr/lib/libc.so.6+0x263dc)
 #8 0x00007f6ad0c54d26 (/usr/lib/libc.so.6+0x36d26)
 #9 0x00005638c2af5180 clang::Diagnostic::FormatDiagnostic(char const*, char const*, llvm::SmallVectorImpl<char>&) const (/opt/rocm/llvm/bin/clang-16+0x3032180)
#10 0x00005638c3420852 clang::TextDiagnosticPrinter::HandleDiagnostic(clang::DiagnosticsEngine::Level, clang::Diagnostic const&) (/opt/rocm/llvm/bin/clang-16+0x395d852)
#11 0x00005638c2afc5b3 clang::DiagnosticIDs::ProcessDiag(clang::DiagnosticsEngine&) const (/opt/rocm/llvm/bin/clang-16+0x30395b3)
#12 0x00005638c2af2dec clang::DiagnosticsEngine::EmitCurrentDiagnostic(bool) (/opt/rocm/llvm/bin/clang-16+0x302fdec)
#13 0x00005638c0ab624f (/opt/rocm/llvm/bin/clang-16+0xff324f)
#14 0x00005638c3baead3 clang::BackendConsumer::DiagnosticHandlerImpl(llvm::DiagnosticInfo const&) (/opt/rocm/llvm/bin/clang-16+0x40ebad3)
#15 0x00005638c3baed01 clang::ClangDiagnosticHandler::handleDiagnostics(llvm::DiagnosticInfo const&) (/opt/rocm/llvm/bin/clang-16+0x40ebd01)
#16 0x00005638c1eed13d llvm::LLVMContext::diagnose(llvm::DiagnosticInfo const&) (/opt/rocm/llvm/bin/clang-16+0x242a13d)
#17 0x00005638c0ac79ef (/opt/rocm/llvm/bin/clang-16+0x10049ef)
#18 0x00005638c0acd7a0 (/opt/rocm/llvm/bin/clang-16+0x100a7a0)
#19 0x00005638c1909939 (/opt/rocm/llvm/bin/clang-16+0x1e46939)
#20 0x00005638c1f121d1 llvm::FPPassManager::runOnFunction(llvm::Function&) (/opt/rocm/llvm/bin/clang-16+0x244f1d1)
#21 0x00005638c1f12381 llvm::FPPassManager::runOnModule(llvm::Module&) (/opt/rocm/llvm/bin/clang-16+0x244f381)
#22 0x00005638c1f12c8d llvm::legacy::PassManagerImpl::run(llvm::Module&) (/opt/rocm/llvm/bin/clang-16+0x244fc8d)
#23 0x00005638c2b5a85c (/opt/rocm/llvm/bin/clang-16+0x309785c)
#24 0x00005638c2b5b753 clang::EmitBackendOutput(clang::DiagnosticsEngine&, clang::HeaderSearchOptions const&, clang::CodeGenOptions const&, clang::TargetOptions const&, clang::LangOptions const&, llvm::StringRef, llvm::Module*, clang::BackendAction, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>) (/opt/rocm/llvm/bin/clang-16+0x3098753)
#25 0x00005638c3bb3cb2 clang::CodeGenAction::ExecuteAction() (/opt/rocm/llvm/bin/clang-16+0x40f0cb2)
#26 0x00005638c33c6919 clang::FrontendAction::Execute() (/opt/rocm/llvm/bin/clang-16+0x3903919)
#27 0x00005638c334c8b1 clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) (/opt/rocm/llvm/bin/clang-16+0x38898b1)
#28 0x00005638c34a0b84 clang::ExecuteCompilerInvocation(clang::CompilerInstance*) (/opt/rocm/llvm/bin/clang-16+0x39ddb84)
#29 0x00005638c0ab72d5 cc1_main(llvm::ArrayRef<char const*>, char const*, void*) (/opt/rocm/llvm/bin/clang-16+0xff42d5)
#30 0x00005638c0ab22c1 (/opt/rocm/llvm/bin/clang-16+0xfef2c1)
#31 0x00005638c0ab4553 clang_main(int, char**) (/opt/rocm/llvm/bin/clang-16+0xff1553)
#32 0x00007f6ad0c45cd0 (/usr/lib/libc.so.6+0x27cd0)
#33 0x00007f6ad0c45d8a __libc_start_main (/usr/lib/libc.so.6+0x27d8a)
#34 0x00005638c0aac975 _start (/opt/rocm/llvm/bin/clang-16+0xfe9975)
clang-16: error: unable to execute command: Aborted (core dumped)
clang-16: error: clang frontend command failed due to signal (use -v to see invocation)
clang version 16.0.0
Target: amdgcn-amd-amdhsa
Thread model: posix
InstalledDir: /opt/rocm/llvm/bin
clang-16: note: diagnostic msg: Error generating preprocessed source(s) - no preprocessable inputs.
```

The reduced OpenCL kernel:

```opencl
$ cat repro.cl
__kernel void x() {
  __local float temp[32768];
  int lidx = get_local_id(1);
  float2 val = *(temp + lidx);
  *temp = 0;
  float *data = 0;
  data[2] = val.y;
}
```

Using `/opt/rocm/bin/clang-ocl repro.cl -o repro.out` it crashes with the same trace.

Reduced LLVM IR (rocm-llvm trunk https://github.com/RadeonOpenCompute/llvm-project/commit/00c4ab90c5c5334a7276dd506bee1d30a5267241):

```llvm
$ cat reduced.ll 
target datalayout = "e-p:64:64-p1:64:64-p2:32:32-p3:32:32-p4:64:64-p5:32:32-p6:32:32-p7:160:256:256:32-p8:128:128-i64:64-v16:16-v24:32-v32:32-v48:64-v96:128-v192:256-v256:256-v512:512-v1024:1024-v2048:2048-n32:64-S32-A5-G1-ni:7:8"
target triple = "amdgcn-amd-amdhsa"

@x.temp = external addrspace(3) global [32768 x float]

define amdgpu_kernel void @x() {
entry:
  %add.ptr = getelementptr float, ptr addrspace(3) @x.temp, i32 0
  ret void
}
```

Reduced LLVM IR (rocm-llvm 5.6.1):

```llvm
$ cat reduced.ll 
target datalayout = "e-p:64:64-p1:64:64-p2:32:32-p3:32:32-p4:64:64-p5:32:32-p6:32:32-i64:64-v16:16-v24:32-v32:32-v48:64-v96:128-v192:256-v256:256-v512:512-v1024:1024-v2048:2048-n32:64-S32-A5-G1-ni:7"
target triple = "amdgcn-amd-amdhsa"

@x.temp = external addrspace(3) global [32768 x float]

define amdgpu_kernel void @x() {
entry:
  store float 0.000000e+00, ptr addrspace(3) @x.temp, align 4
  ret void
}

```

Using `/opt/rocm/llvm/bin/clang -target amdgcn-amd-amdhsa -nogpulib -o out reduced.ll` it crashes with the same trace.

Tested with rocm-llvm trunk ([00c4ab90c5c5334a7276dd506bee1d30a5267241](https://github.com/RadeonOpenCompute/llvm-project/commit/00c4ab90c5c5334a7276dd506bee1d30a5267241)), 5.6.1, and 5.7.1. The IR differs a little per version with each not crashing when used on a different version. The OpenCL code always crashes.

I've attached the original OpenCL kernel. Original downstream bug reported at https://github.com/tinygrad/tinygrad/issues/2186

[repro.cl.orig.txt](https://github.com/RadeonOpenCompute/ROCm/files/13232828/repro.cl.orig.txt)


### Operating System

`Arch Linux`

### CPU

`AMD Ryzen 7 3700X 8-Core Processor`

### GPU

`AMD Radeon RX 6700 XT (gfx1031)`

### ROCm Version

5.6.1, 5.7.1, trunk

### ROCm Component

rocm-llvm (https://github.com/RadeonOpenCompute/llvm-project)

### Steps to Reproduce

_No response_

### Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
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
  Name:                    AMD Ryzen 7 3700X 8-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 3700X 8-Core Processor 
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
  Max Clock Freq. (MHz):   3600                               
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
      Size:                    65793792(0x3ebef00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65793792(0x3ebef00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65793792(0x3ebef00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1031                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 6700 XT              
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
    L2:                      3072(0xc00) KB                     
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29663(0x73df)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2855                               
  BDFID:                   10240                              
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
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    1024(0x400)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    12566528(0xbfc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1031         
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

---

## 评论 (3 条)

### 评论 #1 — ruiling (2023-11-10T12:58:48Z)

Based on your rocminfo output:
```
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB
```
Seems you are using (32768 * 4) bytes local memory, which is more than the available. I don't know why the diagnostic message was not propagated properly.

---

### 评论 #2 — ppanchad-amd (2024-05-16T16:08:56Z)

@telans Can you please test with latest ROCm 6.1.1? If resolved, please close the ticket. Thanks!

---

### 评论 #3 — darren-amd (2024-09-17T14:30:12Z)

Hi @telans,

I ran your OpenCL kernel code and was able to run successfully on the latest version of ROCm (6.2) with some minor modifications:
```
__kernel void x() {
  __local float temp[16384];
  int lidx = get_local_id(1);
  float2 val = *(temp + lidx);
  *temp = 0;
  float data[3];
  data[2] = val.y;
}
```
It looks like the last two lines were initializing a nullptr and then attempting to index into it, which was resulting in an error. I also edited the size of the local array to 16384 as my local memory was 65536 bytes. You can find your local memory size by running `clinfo` and looking under "Local memory size:". I was able to compile with hipcc as: `hipcc repro.cpp -o repro.out -lOpenCL`.




---
