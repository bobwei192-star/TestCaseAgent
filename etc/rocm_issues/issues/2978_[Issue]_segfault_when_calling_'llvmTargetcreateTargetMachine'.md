# [Issue]: segfault when calling 'llvm::Target::createTargetMachine'

> **Issue #2978**
> **状态**: closed
> **创建时间**: 2024-03-25T20:58:34Z
> **更新时间**: 2024-10-01T20:01:56Z
> **关闭时间**: 2024-10-01T20:01:56Z
> **作者**: fwinter
> **标签**: Under Investigation, AMD Instinct MI250X, AMD Instinct MI250, ROCm 5.6.0
> **URL**: https://github.com/ROCm/ROCm/issues/2978

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI250X** (颜色: #ededed)
- **AMD Instinct MI250** (颜色: #ededed)
- **ROCm 5.6.0** (颜色: #ededed)

## 描述

### Problem Description

With ROCm 5.6.0 and later I'm getting a segfault when calling 'llvm::Target::createTargetMachine'. Earlier versions work fine.

The system:
Device name                         : AMD Instinct MI250X
GCN architecture                    : gfx910

My application uses the LLVM compiler that is bundled with the ROCm installation (/opt/rocm/llvm/). The call to 'createTargetMachine' goes like
    

```
llvm::TargetOptions options;
TargetMachine.reset(TheTarget->createTargetMachine(
                                                       "amdgcn-amd-amdhsa", // triple
                                                       "gfx90a",            // CPU
                                                       "",                  // feature str
                                                       options,
                                                       llvm::Reloc::PIC_
                                                       ));

```
This was never a problem. But since ROCm version 5.6.0 I get segfaults like:


```
  Thread 1 "t_dslashm" received signal SIGSEGV, Segmentation fault.
0x00000000008a6b81 in llvm::RegisterTargetMachine<llvm::GCNTargetMachine>::Allocator(llvm::Target const&, llvm::Triple const&, llvm::StringRef, llvm::StringRef, llvm::TargetOptions const&, std::optional<llvm::Reloc::Model>, std::optional<llvm::CodeModel::Model>, llvm::CodeGenOpt::Level, bool) ()
Missing separate debuginfos, use: zypper install krb5-debuginfo-1.19.2-150400.3.6.1.x86_64 libbrotlicommon1-debuginfo-1.0.7-3.3.1.x86_64 libbrotlidec1-debuginfo-1.0.7-3.3.1.x86_64 libcom_err2-debuginfo-1.46.4-150400.3.3.1.x86_64 libcurl4-debuginfo-8.0.1-150400.5.41.1.x86_64 libelf1-debuginfo-0.185-150400.5.3.1.x86_64 libidn2-0-debuginfo-2.2.0-3.6.1.x86_64 libjitterentropy3-debuginfo-3.4.0-150000.1.9.1.x86_64 libjson-c3-debuginfo-0.13-3.3.1.x86_64 libkeyutils1-debuginfo-1.6.3-5.6.1.x86_64 libldap-2_4-2-debuginfo-2.4.46-150200.14.17.1.x86_64 liblzma5-debuginfo-5.2.3-150000.4.7.1.x86_64 libncurses6-debuginfo-6.1-150000.5.20.1.x86_64 libnghttp2-14-debuginfo-1.40.0-150200.12.1.x86_64 libnl3-200-debuginfo-3.3.0-1.29.x86_64 libnuma1-debuginfo-2.0.14.20.g4ee5e0c-150400.1.24.x86_64 libopenssl1_1-debuginfo-1.1.1l-150400.7.60.2.x86_64 libpcre1-debuginfo-8.45-150000.20.13.1.x86_64 libpsl5-debuginfo-0.20.1-150000.3.3.1.x86_64 libselinux1-debuginfo-3.1-150400.1.69.x86_64 libssh4-debuginfo-0.9.6-150400.1.5.x86_64 libunistring2-debuginfo-0.9.10-1.1.x86_64 libxml2-2-debuginfo-2.9.14-150400.5.25.1.x86_64 libyaml-0-2-debuginfo-0.1.7-1.17.x86_64 libz1-debuginfo-1.2.11-150000.3.48.1.x86_64
(gdb) bt
#0  0x00000000008a6b81 in llvm::RegisterTargetMachine<llvm::GCNTargetMachine>::Allocator(llvm::Target const&, llvm::Triple const&, llvm::StringRef, llvm::StringRef, llvm::TargetOptions const&, std::optional<llvm::Reloc::Model>, std::optional<llvm::CodeModel::Model>, llvm::CodeGenOpt::Level, bool) ()
#1  0x0000000000578e4b in llvm::Target::createTargetMachine (this=0x48a9800 <llvm::getTheGCNTarget()::TheGCNTarget>, TT=..., CPU=..., Features=..., Options=..., RM=..., CM=..., OL=llvm::CodeGenOpt::Default, JIT=false)
    at /opt/rocm-5.6.0/llvm/include/llvm/MC/TargetRegistry.h:488
```

What am I missing?


### Operating System

Linux frontier07423 5.14.21-150400.24.46_12.0.83-cray_shasta_c

### CPU

AMD EPYC 7A53 64-Core Processor

### GPU

AMD Instinct MI250X, AMD Instinct MI250

### ROCm Version

ROCm 5.6.0

### ROCm Component

llvm-project

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — nartmada (2024-03-26T16:28:06Z)

An internal ticket has been created for investigation.

---

### 评论 #2 — fwinter (2024-03-27T16:02:13Z)

Here's the reproducer:

```
#include "llvm/InitializePasses.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Support/TargetSelect.h"
#include "llvm/Target/TargetMachine.h"

#include <iostream>

    
int main()
{
  llvm::InitializeAllTargets();
  llvm::InitializeAllTargetMCs();
  llvm::InitializeAllAsmPrinters();
  llvm::InitializeAllAsmParsers();

  llvm::PassRegistry *Registry = llvm::PassRegistry::getPassRegistry();
  llvm::initializeCore(*Registry);
  llvm::initializeCodeGen(*Registry);
  llvm::initializeLoopStrengthReducePass(*Registry);
  llvm::initializeLowerIntrinsicsPass(*Registry);
  llvm::initializeUnreachableBlockElimLegacyPassPass(*Registry);
  llvm::initializeConstantHoistingLegacyPassPass(*Registry);


  llvm::Triple TheTriple;
  TheTriple.setArch (llvm::Triple::ArchType::amdgcn);
  TheTriple.setVendor (llvm::Triple::VendorType::AMD);
  TheTriple.setOS (llvm::Triple::OSType::AMDHSA);

  std::string Error;
  const llvm::Target *TheTarget = llvm::TargetRegistry::lookupTarget( TheTriple.str() , Error );
  if (!TheTarget) {
    std::cout << Error;
    std::cout << "Something went wrong setting the target\n";
    return 1;
  }

    
  llvm::TargetOptions Options;

  std::unique_ptr<llvm::TargetMachine> TargetMachine;

  TargetMachine.reset(TheTarget->createTargetMachine(
						     "amdgcn-amd-amdhsa", // triple
						     "gfx90a",   // CPU
						     "" , // FeatureStr 
						     Options,
						     llvm::Reloc::PIC_
						     )
		      );

  std::cout << "LLVM initialization" << std::endl;
  std::cout << "  Target machine CPU                  : " << TargetMachine->getTargetCPU().str() << "\n";
  std::cout << "  Target triple                       : " << TargetMachine->getTargetTriple().str() << "\n";

  return 0;
}

```

CMakeLists.txt

```
cmake_minimum_required(VERSION 3.17)
project(SEGFAULT VERSION 0.1 LANGUAGES CXX;C)

find_package(LLVM "16.0" REQUIRED CONFIG)

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in ${LLVM_DIR}")

add_executable(llvm_init llvm_init.cc)

set_target_properties( llvm_init PROPERTIES CXX_STANDARD 17 )

target_include_directories(llvm_init PUBLIC ${LLVM_INCLUDE_DIRS} )

target_link_libraries( llvm_init PUBLIC ${LLVM_AVAILABLE_LIBS} )

```


build.sh

```
export CXX=CC
export CC=cc
cmake ../
```

Steps to reproduce on Frontier:

module load zstd
module load rocm/5.5.1                                                                                                                                                                                                                                      
module load PrgEnv-gnu
mkdir build; cd build
../build.sh
-- The CXX compiler identification is GNU 12.2.0
-- The C compiler identification is GNU 12.2.0
-- Cray Programming Environment 2.7.19 CXX
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /opt/cray/pe/craype/2.7.19/bin/CC - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Cray Programming Environment 2.7.19 C
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /opt/cray/pe/craype/2.7.19/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Performing Test Terminfo_LINKABLE
-- Performing Test Terminfo_LINKABLE - Success
-- Found Terminfo: /usr/lib64/libtinfo.so  
-- Found ZLIB: /usr/lib64/libz.so (found version "1.2.11") 
-- Found LLVM 16.0.0git
-- Using LLVMConfig.cmake in /opt/rocm-5.5.1/llvm/lib/cmake/llvm
-- Configuring done
-- Generating done
-- Build files have been written to: /ccs/home/fwinter/llvm_segfault/build

$make 
[ 50%] Building CXX object CMakeFiles/llvm_init.dir/llvm_init.cc.o
[100%] Linking CXX executable llvm_init
[100%] Built target llvm_init

./llvm_init
LLVM initialization
  Target machine CPU                  : gfx90a
  Target triple                       : amdgcn-amd-amdhsa

module load rocm/5.6.0
(clean directory, rebuild executable)

$ ../build.sh 
-- The CXX compiler identification is GNU 12.2.0
-- The C compiler identification is GNU 12.2.0
-- Cray Programming Environment 2.7.19 CXX
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /opt/cray/pe/craype/2.7.19/bin/CC - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Cray Programming Environment 2.7.19 C
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /opt/cray/pe/craype/2.7.19/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Performing Test Terminfo_LINKABLE
-- Performing Test Terminfo_LINKABLE - Success
-- Found Terminfo: /usr/lib64/libtinfo.so  
-- Found ZLIB: /usr/lib64/libz.so (found version "1.2.11") 
-- Found zstd: /sw/frontier/spack-envs/base/opt/linux-sles15-x86_64/gcc-7.5.0/zstd-1.5.2-g7yosuyngtahpkmypk25drrmoykqxsr4/lib/libzstd.so  
-- Found LLVM 16.0.0git
-- Using LLVMConfig.cmake in /opt/rocm-5.6.0/llvm/lib/cmake/llvm
-- Configuring done
-- Generating done
-- Build files have been written to: /ccs/home/fwinter/llvm_segfault/build
$ make
[ 50%] Building CXX object CMakeFiles/llvm_init.dir/llvm_init.cc.o
[100%] Linking CXX executable llvm_init
[100%] Built target llvm_init

$ ./llvm_init 
Segmentation fault (core dumped)

Program received signal SIGSEGV, Segmentation fault.
0x0000000001055b71 in llvm::RegisterTargetMachine<llvm::GCNTargetMachine>::Allocator(llvm::Target const&, llvm::Triple const&, llvm::StringRef, llvm::StringRef, llvm::TargetOptions const&, std::optional<llvm::Reloc::Model>, std::optional<llvm::CodeModel::Model>, llvm::CodeGenOpt::Level, bool) ()
Missing separate debuginfos, use: zypper install krb5-debuginfo-1.19.2-150400.3.6.1.x86_64 libbrotlicommon1-debuginfo-1.0.7-3.3.1.x86_64 libbrotlidec1-debuginfo-1.0.7-3.3.1.x86_64 libcom_err2-debuginfo-1.46.4-150400.3.3.1.x86_64 libcurl4-debuginfo-8.0.1-150400.5.41.1.x86_64 libidn2-0-debuginfo-2.2.0-3.6.1.x86_64 libjitterentropy3-debuginfo-3.4.0-150000.1.9.1.x86_64 libjson-c3-debuginfo-0.13-3.3.1.x86_64 libkeyutils1-debuginfo-1.6.3-5.6.1.x86_64 libldap-2_4-2-debuginfo-2.4.46-150200.14.17.1.x86_64 libncurses6-debuginfo-6.1-150000.5.20.1.x86_64 libnghttp2-14-debuginfo-1.40.0-150200.12.1.x86_64 libnl3-200-debuginfo-3.3.0-1.29.x86_64 libopenssl1_1-debuginfo-1.1.1l-150400.7.60.2.x86_64 libpcre1-debuginfo-8.45-150000.20.13.1.x86_64 libpsl5-debuginfo-0.20.1-150000.3.3.1.x86_64 libselinux1-debuginfo-3.1-150400.1.69.x86_64 libssh4-debuginfo-0.9.6-150400.1.5.x86_64 libunistring2-debuginfo-0.9.10-1.1.x86_64 libyaml-0-2-debuginfo-0.1.7-1.17.x86_64 libz1-debuginfo-1.2.11-150000.3.48.1.x86_64
(gdb) bt
#0  0x0000000001055b71 in llvm::RegisterTargetMachine<llvm::GCNTargetMachine>::Allocator(llvm::Target const&, llvm::Triple const&, llvm::StringRef, llvm::StringRef, llvm::TargetOptions const&, std::optional<llvm::Reloc::Model>, std::optional<llvm::CodeModel::Model>, llvm::CodeGenOpt::Level, bool) ()
#1  0x000000000049bc93 in llvm::Target::createTargetMachine(llvm::StringRef, llvm::StringRef, llvm::StringRef, llvm::TargetOptions const&, std::optional<llvm::Reloc::Model>, std::optional<llvm::CodeModel::Model>, llvm::CodeGenOpt::Level, bool) const ()
#2  0x000000000049b441 in main ()


---

### 评论 #3 — enginekun (2024-05-11T09:36:42Z)

Is there any updates? I have a similar problem with x86_64 cpu too.

---

### 评论 #4 — nartmada (2024-06-14T04:30:06Z)

@enginekun, sorry for not getting back sooner.  We are still working on the issue.  Thanks.

---

### 评论 #5 — lamb-j (2024-06-17T18:52:33Z)

Possible fix: https://github.com/llvm/llvm-project/pull/79866

---

### 评论 #6 — jamesxu2 (2024-06-25T15:11:13Z)

Hello @fwinter , 

Thank you for the detailed reproduction info. 

I'm using your CMakeLists, build.sh and llvm_init.cc files and I'm unable to reproduce your issue on my system (AMD Ryzen 9 5950X x86_64 CPU, RX7900XT gfx1100 GPU).

I have tried using the LLVM version included with: 
- ROCm 5.5 (LLVM version 16.0.0.23243) using g++11
- ROCm 5.6 (LLVM version 16.0.0.23194)  using g++ 11 and g++ 12
- ROCm 5.7 (LLVM version 17.0.0.23382) using g++ 11 and g++ 12

and I'm unable to reproduce your segfault using the steps you've provided. I get the expected output in each of these configurations:

```
$ ./llvm_init
LLVM initialization
  Target machine CPU                  : gfx90a
  Target triple                       : amdgcn-amd-amdhsa
```

Please let me know if the steps I'm following are incorrect or if I'm otherwise missing something.

---

### 评论 #7 — fwinter (2024-06-27T19:21:01Z)

Thanks for looking into this. I just tried again on Frontier at ORNL; still segfaults for rocm >= 5.6 on frontend node as well as compute node. So, then this might be Frontier-specific!?

---

### 评论 #8 — jamesxu2 (2024-07-08T14:29:47Z)

Hello @fwinter , 

I've done some more testing on a Frontier-like system and have some recommendations:

I am able to successfully compile and run your test program, with a more recent ROCm stack (6.1.1) and LLVM (19). I think your problem is not likely to be Frontier specific.

```
$ make -j88
-- Cray Programming Environment 2.7.31.11 CXX
-- Cray Programming Environment 2.7.31.11 C
-- Found LLVM 19.0.0git
-- Using LLVMConfig.cmake in /home/USER/llvm-project/build/lib/cmake/llvm
-- Configuring done
-- Generating done
-- Build files have been written to: /home/USER/experiment/build
Consolidate compiler generated dependencies of target llvm_init
[ 50%] Building CXX object CMakeFiles/llvm_init.dir/[llvm_init.cc](http://llvm_init.cc/).o
[100%] Linking CXX executable llvm_init
[100%] Built target llvm_init

$:  ~/experiment/build> ./llvm_init
LLVM initialization
  Target machine CPU                  : gfx90a
  Target triple                       : amdgcn-amd-amdhsa
```

At this point, I think the only untested difference is the compiler - if you are able to compile this test program with a different compiler, it may provide more information.

Additionally, you may consider upgrading LLVM and ROCm, though given we've both tested multiple versions of this it's probably not the issue here. If you decide to do so, I have a few recommendations:

One thing to note is, that since ROCm 6.1, the LLVM development tools needed for compiler development are no longer packaged with the base ROCm driver ([ref](https://github.com/ROCm/ROCm/issues/2703)). While you can simply install the **rocm-llvm-dev** package on Ubuntu to fix this issue, it may not be so easy on your OS and you may have to build ROCm/llvm-project from source following these instructions: https://github.com/ROCm/llvm-project/blob/amd-staging/llvm/docs/GettingStarted.rst (This may take a while).

Following that, set your LLVM_DIR environment variable to point to the build directory and change your CMakeLists.txt to match the installed version of LLVM:
```export LLVM_DIR=/home/USER/llvm-project/build```

---

### 评论 #9 — jamesxu2 (2024-07-24T18:26:25Z)

Hi @fwinter, do you have any update?

---

### 评论 #10 — jamesxu2 (2024-10-01T20:01:56Z)

I'm going to close this ticket due to lack of activity - you are welcome to reopen it if you do come back to this @fwinter .

---
