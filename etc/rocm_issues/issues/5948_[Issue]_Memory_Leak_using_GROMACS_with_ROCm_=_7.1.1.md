# [Issue]: Memory Leak using GROMACS with ROCm >= 7.1.1

> **Issue #5948**
> **状态**: closed
> **创建时间**: 2026-02-10T15:57:07Z
> **更新时间**: 2026-04-09T12:11:19Z
> **关闭时间**: 2026-04-09T12:11:19Z
> **作者**: alexschroeter
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5948

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

Running GROMACS workloads with ROCm >= 7.1.1 (7.0.0 untested) we see huge memory leaks.
The leak was found after we upgraded from ROCm 6.1.3 to 7.1.1 but it is also present in 7.2.0 ~and not present in 6.4.4~
I also tested the 7.2.0 driver (30.30) with ROCm 6.1.3 but leak was still happening, which makes me believe the error is not in library but the driver.

### Operating System

Alma 9.7

### CPU

AMD EPYC 7452 32-Core Processor

### GPU

MI210

### ROCm Version

7.1.1, 7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

Because there is a difference between building GROMACS for 7.2.0 and 7.1.1, I split the reproduce steps into those versions. The instructions for 7.1.1 also work for the older ROCm versions because it still uses LLVM20 and not 22 like 7.2.0.

Depending on those differences we need slightly different versions but the concept stays the same. We build adaptivecpp and use it to build gromacs with mpi and ucx support. You need `rocm-llvm-devel` and make sure to change the GPU targets (gfx..) to whatever model you are using.

# Build

Building GROMACS with AdaptiveCpp, MPI and UCX

## 7.1.1

Get AdaptiveCpp v25.10.0 https://github.com/AdaptiveCpp/AdaptiveCpp and build with 
```
cmake .. -DCMAKE_C_COMPILER=/opt/rocm/llvm/bin/clang -DCMAKE_CXX_COMPILER=/opt/rocm/llvm/bin/clang++ -DLLVM_DIR=/opt/rocm/llvm/lib/cmake/llvm/ -DACPP_COMPILER_FEATURE_PROFILE=minimal -DCMAKE_INSTALL_PREFIX=~/.adaptivecpp
make -j
make install % To ~/.adaptivecpp where we tell gromacs to look for it
```

Get GROMACS v2025.4 https://gitlab.com/gromacs/gromacs and build with
```
cmake .. -DCMAKE_C_COMPILER=/opt/rocm/llvm/bin/clang -DCMAKE_CXX_COMPILER=/opt/rocm/llvm/bin/clang++ -DGMX_GPU=SYCL -DGMX_SYCL=ACPP -DACPP_TARGETS='hip:gfx90a' -Dadaptivecpp_DIR=~/.adaptivecpp/lib/cmake/AdaptiveCpp/ -Dhipsycl_DIR=~/.adaptivecpp/lib/cmake/hipSYCL/  -DGMX_MPI=on
```

## 7.2.0

Get AdaptiveCpp https://github.com/alexschroeter/AdaptiveCpp branch llvm-22-getDecl and build with 
```
cmake .. -DCMAKE_C_COMPILER=/opt/rocm/llvm/bin/clang -DCMAKE_CXX_COMPILER=/opt/rocm/llvm/bin/clang++ -DLLVM_DIR=/opt/rocm/llvm/lib/cmake/llvm/ -DACPP_COMPILER_FEATURE_PROFILE=minimal -DCMAKE_INSTALL_PREFIX=~/.adaptivecpp -DACPP_EXPERIMENTAL_LLVM=ON
make -j
make install % To ~/.adaptivecpp where we tell gromacs to look for it
```

Get GROMACS v2025.4 https://gitlab.com/gromacs/gromacs and build with
```
cmake .. -DCMAKE_C_COMPILER=/opt/rocm/llvm/bin/clang -DCMAKE_CXX_COMPILER=/opt/rocm/llvm/bin/clang++ -DGMX_GPU=SYCL -DGMX_SYCL=ACPP -DACPP_TARGETS='hip:gfx90a' -Dadaptivecpp_DIR=~/.adaptivecpp/lib/cmake/AdaptiveCpp/ -Dhipsycl_DIR=~/.adaptivecpp/lib/cmake/hipSYCL/  -DGMX_MPI=on
```

# Run GROMACS

Download the prod.tpr https://next.hessenbox.de/index.php/s/fKEHLSpcNYPXSa6
```
mkdir gromacs_run
cd gromacs_run
cp <path to download>/prod.tpr .
for i in {1..8}; do mkdir res$i && cp prod.tpr res$i;done
% if you have 8 gpus
mpirun -np 8 <path to gromacs build>/bin/gmx_mpi mdrun -ntomp 8 -pin on -multidir rep* -deffnm prod
% if you have 1 gpu
mpirun -np 1 <path to gromacs build>/bin/gmx_mpi mdrun -ntomp 8 -pin on -deffnm prod
```

watch the leak eat all the memory

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support


OS:
NAME="AlmaLinux"
VERSION="9.7 (Moss Jungle Cat)"

CPU:
model name      : AMD EPYC 7452 32-Core Processor

GPU:
  Name:                    AMD EPYC 7452 32-Core Processor
  Marketing Name:          AMD EPYC 7452 32-Core Processor
  Name:                    AMD EPYC 7452 32-Core Processor
  Marketing Name:          AMD EPYC 7452 32-Core Processor
  Name:                    gfx90a
  Marketing Name:          AMD Instinct MI210
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a
  Marketing Name:          AMD Instinct MI210
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a
  Marketing Name:          AMD Instinct MI210
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a
  Marketing Name:          AMD Instinct MI210
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a
  Marketing Name:          AMD Instinct MI210
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a
  Marketing Name:          AMD Instinct MI210
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a
  Marketing Name:          AMD Instinct MI210
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a
  Marketing Name:          AMD Instinct MI210
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-

### Additional Information

_No response_

---

## 评论 (33 条)

### 评论 #1 — tcgu-amd (2026-02-11T21:20:49Z)

Hi @alexschroeter, thanks for the detailed instructions! I am not quite sure if I was able to reproduce the issue, but I managed to build GROMACS and ran your workload. It seems like it takes a long time to run, which makes profiling and debugging a bit difficult. Do you by chance have a smaller task that can finish within a minute or so? Or am I doing something wrong? Thanks! 

---

### 评论 #2 — alexschroeter (2026-02-12T09:39:18Z)

You can add `-nsteps 1000` to the command to limit the number steps taken. This should finish in a couple of seconds. Since I don't know exactly where the leak is, it could also happen after these steps. So you might need to raise the time. If you don't have success with this you could also use `-maxh 0.25` (would be 15min) to limit the time of the simulation.

If you put both it will stop at the first limit reached.

---

### 评论 #3 — alexschroeter (2026-02-12T14:30:54Z)

Update: I got tricked by the leak being much slower in 6.4.4 but it is still there. The leak seems to appears somewhere inbetween ROCm > 6.2.4 and <= 6.4.4

---

### 评论 #4 — alexschroeter (2026-02-17T08:49:14Z)

As an update: The leak is also present in the hip_feature_branch of GROMACS v2026. I tested using ROCm 7.2.0 with the 30.10.3 driver + MPI 5.0.9 + UCX 1.19.1 

@paubauer as you suggested here is the asan output of a 3 min run without mpi (since there was a confilict between asan and ucx). As I already mentioned, in the beginning I believed this to be driver related because changing the driver and going back to last known good rocm 6.1.3 still had the leak. I since have found that this rocm version is not compatible with driver 30.30 which might be the reason that there was also a leak with this combination. I am now more on the side of the leak being introduced somewhere between ROCm > 6.2.4 and < 6.4.4

```
ASAN_OPTIONS=detect_leaks=1 gmx mdrun -ntomp 8 -pin on -deffnm prod -maxh 0.05
 :-) GROMACS - gmx mdrun, 2026.0-2026_HIP_ENABLEMENT-dev-20260210-2724d58cfa (-:

Executable:   /cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx
Data prefix:  /cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0
Working dir:  /home/compeng/schroeter/gromacs_test
Command line:
  gmx mdrun -ntomp 8 -pin on -deffnm prod -maxh 0.05


Back Off! I just backed up prod.log to ./#prod.log.3#
Reading file prod.tpr, VERSION 2025.3-dev-20250829-820db9e499-unknown (single precision)
Note: file tpx version 137, software tpx version 138
Changing nstlist from 10 to 100, rlist from 1.1 to 1.254

Update groups can not be used for this system because atoms that are (in)directly constrained together are interdispersed with other atoms

1 GPU selected for this run.
Mapping of GPU IDs to the 2 GPU tasks in the 1 rank on this node:
  PP:0,PME:0
PP tasks will do non-perturbed short-ranged interactions on the GPU
PP task will update and constrain coordinates on the GPU
PME tasks will do all aspects on the GPU
Using 8 OpenMP threads 


Back Off! I just backed up prod.xtc to ./#prod.xtc.3#

Back Off! I just backed up prod.edr to ./#prod.edr.3#
starting mdrun 'Generic title'
25000000000 steps, 50000000.0 ps.

Step 838300: Run time exceeded 0.050 hours, will terminate the run within 100 steps

               Core t (s)   Wall t (s)        (%)
       Time:     1426.017      179.168      795.9
                 (ns/day)    (hour/ns)    (ms/step)  (Matom*steps/s) 
Performance:      808.602        0.030        0.214           30.571 

GROMACS reminds you: "Making merry out of nothing, like in refugee camp" (Gogol Bordello)


=================================================================
==761495==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 43008 byte(s) in 768 object(s) allocated from:
    #0 0x00000036d01d in operator new(unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36d01d)
    #1 0x147ad7a69c67  (/opt/rocm/lib/libhsa-runtime64.so.1+0x69c67) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)

Direct leak of 5616 byte(s) in 78 object(s) allocated from:
    #0 0x00000036d01d in operator new(unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36d01d)
    #1 0x147ad7a69e18  (/opt/rocm/lib/libhsa-runtime64.so.1+0x69e18) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)

Direct leak of 936 byte(s) in 13 object(s) allocated from:
    #0 0x00000036d01d in operator new(unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36d01d)
    #1 0x147ad7a54b8d  (/opt/rocm/lib/libhsa-runtime64.so.1+0x54b8d) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)
    #2 0x147ad7a4aa2f  (/opt/rocm/lib/libhsa-runtime64.so.1+0x4aa2f) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)
    #3 0x147ad7a60331  (/opt/rocm/lib/libhsa-runtime64.so.1+0x60331) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)
    #4 0x147ae23e14c1  (/opt/rocm/lib/libamdhip64.so.7+0x3e14c1) (BuildId: 113b5b19bfaa79865d339f990c3c7f995b27112c)
    #5 0x147ae23f96ab  (/opt/rocm/lib/libamdhip64.so.7+0x3f96ab) (BuildId: 113b5b19bfaa79865d339f990c3c7f995b27112c)

Direct leak of 576 byte(s) in 8 object(s) allocated from:
    #0 0x00000036d01d in operator new(unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36d01d)
    #1 0x147ad7a54b8d  (/opt/rocm/lib/libhsa-runtime64.so.1+0x54b8d) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)
    #2 0x147ad7a4aa2f  (/opt/rocm/lib/libhsa-runtime64.so.1+0x4aa2f) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)
    #3 0x147ad7a442dc  (/opt/rocm/lib/libhsa-runtime64.so.1+0x442dc) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)

Direct leak of 344 byte(s) in 1 object(s) allocated from:
    #0 0x00000036d01d in operator new(unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36d01d)
    #1 0x147ae8634f5a in gmx::gpu_init(gmx::DeviceStreamManager const&, interaction_const_t const*, gmx::PairlistParams const&, gmx::nbnxn_atomdata_t const*, bool, std::optional<int>) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3deef5a)

Direct leak of 200 byte(s) in 4 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x147ae86ffac9 in shaderGen_FFT(VkFFTSpecializationConstantsLayout*, int) gpu_3dfft_hip_vkfft.cpp

Direct leak of 100 byte(s) in 2 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x147ae86fec31 in shaderGen_FFT(VkFFTSpecializationConstantsLayout*, int) gpu_3dfft_hip_vkfft.cpp

Direct leak of 36 byte(s) in 1 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x147ae6a171cc in save_calloc(char const*, char const*, int, unsigned long, unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x21d11cc)
    #2 0x147ae83f82d0 in init_ekinstate(ekinstate_t*, t_inputrec const*) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3bb22d0)
    #3 0x147ae8360a97 in set_state_entries(t_state*, t_inputrec const*, bool) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3b1aa97)
    #4 0x147ae8801482 in gmx::Mdrunner::mdrunner() (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3fbb482)
    #5 0x00000037097b in gmx::gmx_mdrun(GmxNoMpiDummyMpiComm*, gmx_hw_info_t const&, int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x37097b)
    #6 0x0000003703ab in gmx::gmx_mdrun(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x3703ab)
    #7 0x147ae7928c01 in gmx::CommandLineModuleManager::run(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x30e2c01)
    #8 0x00000036e4f8 in main (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36e4f8)
    #9 0x147ae402a60f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: e650335ac8463e9e58c04e07c6f36c5f826ed953)

Direct leak of 36 byte(s) in 1 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x147ae6a171cc in save_calloc(char const*, char const*, int, unsigned long, unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x21d11cc)
    #2 0x147ae83f836c in init_ekinstate(ekinstate_t*, t_inputrec const*) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3bb236c)
    #3 0x147ae8360a97 in set_state_entries(t_state*, t_inputrec const*, bool) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3b1aa97)
    #4 0x147ae8801482 in gmx::Mdrunner::mdrunner() (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3fbb482)
    #5 0x00000037097b in gmx::gmx_mdrun(GmxNoMpiDummyMpiComm*, gmx_hw_info_t const&, int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x37097b)
    #6 0x0000003703ab in gmx::gmx_mdrun(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x3703ab)
    #7 0x147ae7928c01 in gmx::CommandLineModuleManager::run(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x30e2c01)
    #8 0x00000036e4f8 in main (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36e4f8)
    #9 0x147ae402a60f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: e650335ac8463e9e58c04e07c6f36c5f826ed953)

Direct leak of 36 byte(s) in 1 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x147ae6a171cc in save_calloc(char const*, char const*, int, unsigned long, unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x21d11cc)
    #2 0x147ae83f831e in init_ekinstate(ekinstate_t*, t_inputrec const*) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3bb231e)
    #3 0x147ae8360a97 in set_state_entries(t_state*, t_inputrec const*, bool) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3b1aa97)
    #4 0x147ae8801482 in gmx::Mdrunner::mdrunner() (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3fbb482)
    #5 0x00000037097b in gmx::gmx_mdrun(GmxNoMpiDummyMpiComm*, gmx_hw_info_t const&, int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x37097b)
    #6 0x0000003703ab in gmx::gmx_mdrun(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x3703ab)
    #7 0x147ae7928c01 in gmx::CommandLineModuleManager::run(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x30e2c01)
    #8 0x00000036e4f8 in main (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36e4f8)
    #9 0x147ae402a60f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: e650335ac8463e9e58c04e07c6f36c5f826ed953)

Direct leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0x000000328e74 in malloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x328e74)
    #1 0x147ae17c7ebc  (/lib64/libgomp.so.1+0xdebc) (BuildId: ec4fbe8aa26fd14d8ab164545c217e51df48588d)

Indirect leak of 3600 byte(s) in 75 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x147ad7b27c04  (/opt/rocm/lib/libhsa-runtime64.so.1+0x127c04) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)

SUMMARY: AddressSanitizer: 54496 byte(s) leaked in 953 allocation(s).
```

---

### 评论 #5 — tcgu-amd (2026-02-17T20:51:38Z)

@alexschroeter Thanks for the update! Can you also try to see if a longer run will change the amount of memory being leaked? HIP is known to allocate a bunch of objects that persist throughout the lifetime of the process, which can get marked as false positives by ASAN. They are usually reused as well so more like a one-time overhead. Having more datapoints should help with identifying which ones are the actual leaks. Thanks! 


---

### 评论 #6 — b-sumner (2026-02-17T21:52:18Z)

Can someone here explain why malloc and friends have a stack trace starting with 

 #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)

---

### 评论 #7 — alexschroeter (2026-02-18T10:47:11Z)

> [@alexschroeter](https://github.com/alexschroeter) Thanks for the update! Can you also try to see if a longer run will change the amount of memory being leaked? HIP is known to allocate a bunch of objects that persist throughout the lifetime of the process, which can get marked as false positives by ASAN. They are usually reused as well so more like a one-time overhead. Having more datapoints should help with identifying which ones are the actual leaks. Thanks!

I ran with ASAN 100 times longer but the output is the same. So it seems to me that asan doesn't see the leak.

```
 :-) GROMACS - gmx mdrun, 2026.0-2026_HIP_ENABLEMENT-dev-20260210-2724d58cfa (-:

Executable:   /cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx
Data prefix:  /cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0
Working dir:  /home/compeng/schroeter/gromacs_test
Command line:
  gmx mdrun -ntomp 8 -pin on -deffnm prod -maxh 5


Back Off! I just backed up prod.log to ./#prod.log.8#
Reading file prod.tpr, VERSION 2025.3-dev-20250829-820db9e499-unknown (single precision)
Note: file tpx version 137, software tpx version 138
Changing nstlist from 10 to 100, rlist from 1.1 to 1.254

Update groups can not be used for this system because atoms that are (in)directly constrained together are interdispersed with other atoms

1 GPU selected for this run.
Mapping of GPU IDs to the 2 GPU tasks in the 1 rank on this node:
  PP:0,PME:0
PP tasks will do non-perturbed short-ranged interactions on the GPU
PP task will update and constrain coordinates on the GPU
PME tasks will do all aspects on the GPU
Using 8 OpenMP threads


Back Off! I just backed up prod.xtc to ./#prod.xtc.8#

Back Off! I just backed up prod.edr to ./#prod.edr.8#
starting mdrun 'Generic title'
25000000000 steps, 50000000.0 ps.

Step 78901300: Run time exceeded 4.950 hours, will terminate the run within 100 steps

               Core t (s)   Wall t (s)        (%)
       Time:   142560.583    18052.135      789.7
                         5h00:52
                 (ns/day)    (hour/ns)    (ms/step)  (Matom*steps/s)
Performance:      755.266        0.032        0.229           28.554

GROMACS reminds you: "Lets get back to beer" (Yuxuan Zhuang, in a discussion about science communication)


=================================================================
==762964==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 43008 byte(s) in 768 object(s) allocated from:
    #0 0x00000036d01d in operator new(unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36d01d)
    #1 0x154dfaa69c67  (/opt/rocm/lib/libhsa-runtime64.so.1+0x69c67) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)

Direct leak of 5616 byte(s) in 78 object(s) allocated from:
    #0 0x00000036d01d in operator new(unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36d01d)
    #1 0x154dfaa69e18  (/opt/rocm/lib/libhsa-runtime64.so.1+0x69e18) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)

Direct leak of 936 byte(s) in 13 object(s) allocated from:
    #0 0x00000036d01d in operator new(unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36d01d)
    #1 0x154dfaa54b8d  (/opt/rocm/lib/libhsa-runtime64.so.1+0x54b8d) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)
    #2 0x154dfaa4aa2f  (/opt/rocm/lib/libhsa-runtime64.so.1+0x4aa2f) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)
    #3 0x154dfaa60331  (/opt/rocm/lib/libhsa-runtime64.so.1+0x60331) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)
    #4 0x154e053e14c1  (/opt/rocm/lib/libamdhip64.so.7+0x3e14c1) (BuildId: 113b5b19bfaa79865d339f990c3c7f995b27112c)
    #5 0x154e053f96ab  (/opt/rocm/lib/libamdhip64.so.7+0x3f96ab) (BuildId: 113b5b19bfaa79865d339f990c3c7f995b27112c)

Direct leak of 576 byte(s) in 8 object(s) allocated from:
    #0 0x00000036d01d in operator new(unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36d01d)
    #1 0x154dfaa54b8d  (/opt/rocm/lib/libhsa-runtime64.so.1+0x54b8d) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)
    #2 0x154dfaa4aa2f  (/opt/rocm/lib/libhsa-runtime64.so.1+0x4aa2f) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)
    #3 0x154dfaa442dc  (/opt/rocm/lib/libhsa-runtime64.so.1+0x442dc) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)

Direct leak of 344 byte(s) in 1 object(s) allocated from:
    #0 0x00000036d01d in operator new(unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36d01d)
    #1 0x154e0b801f5a in gmx::gpu_init(gmx::DeviceStreamManager const&, interaction_const_t const*, gmx::PairlistParams const&, gmx::nbnxn_atomdata_t const*, bool, std::optional<int>) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3deef5a)

Direct leak of 200 byte(s) in 4 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x154e0b8ccac9 in shaderGen_FFT(VkFFTSpecializationConstantsLayout*, int) gpu_3dfft_hip_vkfft.cpp

Direct leak of 100 byte(s) in 2 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x154e0b8cbc31 in shaderGen_FFT(VkFFTSpecializationConstantsLayout*, int) gpu_3dfft_hip_vkfft.cpp

Direct leak of 36 byte(s) in 1 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x154e09be41cc in save_calloc(char const*, char const*, int, unsigned long, unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x21d11cc)
    #2 0x154e0b5c52d0 in init_ekinstate(ekinstate_t*, t_inputrec const*) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3bb22d0)
    #3 0x154e0b52da97 in set_state_entries(t_state*, t_inputrec const*, bool) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3b1aa97)
    #4 0x154e0b9ce482 in gmx::Mdrunner::mdrunner() (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3fbb482)
    #5 0x00000037097b in gmx::gmx_mdrun(GmxNoMpiDummyMpiComm*, gmx_hw_info_t const&, int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x37097b)
    #6 0x0000003703ab in gmx::gmx_mdrun(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x3703ab)
    #7 0x154e0aaf5c01 in gmx::CommandLineModuleManager::run(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x30e2c01)
    #8 0x00000036e4f8 in main (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36e4f8)
    #9 0x154e0702a60f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: e650335ac8463e9e58c04e07c6f36c5f826ed953)

Direct leak of 36 byte(s) in 1 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x154e09be41cc in save_calloc(char const*, char const*, int, unsigned long, unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x21d11cc)
    #2 0x154e0b5c536c in init_ekinstate(ekinstate_t*, t_inputrec const*) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3bb236c)
    #3 0x154e0b52da97 in set_state_entries(t_state*, t_inputrec const*, bool) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3b1aa97)
    #4 0x154e0b9ce482 in gmx::Mdrunner::mdrunner() (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3fbb482)
    #5 0x00000037097b in gmx::gmx_mdrun(GmxNoMpiDummyMpiComm*, gmx_hw_info_t const&, int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x37097b)
    #6 0x0000003703ab in gmx::gmx_mdrun(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x3703ab)
    #7 0x154e0aaf5c01 in gmx::CommandLineModuleManager::run(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x30e2c01)
    #8 0x00000036e4f8 in main (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36e4f8)
    #9 0x154e0702a60f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: e650335ac8463e9e58c04e07c6f36c5f826ed953)

Direct leak of 36 byte(s) in 1 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x154e09be41cc in save_calloc(char const*, char const*, int, unsigned long, unsigned long) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x21d11cc)
    #2 0x154e0b5c531e in init_ekinstate(ekinstate_t*, t_inputrec const*) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3bb231e)
    #3 0x154e0b52da97 in set_state_entries(t_state*, t_inputrec const*, bool) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3b1aa97)
    #4 0x154e0b9ce482 in gmx::Mdrunner::mdrunner() (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x3fbb482)
    #5 0x00000037097b in gmx::gmx_mdrun(GmxNoMpiDummyMpiComm*, gmx_hw_info_t const&, int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x37097b)
    #6 0x0000003703ab in gmx::gmx_mdrun(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x3703ab)
    #7 0x154e0aaf5c01 in gmx::CommandLineModuleManager::run(int, char**) (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/lib64/libgromacs.so.11+0x30e2c01)
    #8 0x00000036e4f8 in main (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x36e4f8)
    #9 0x154e0702a60f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: e650335ac8463e9e58c04e07c6f36c5f826ed953)

Direct leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0x000000328e74 in malloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x328e74)
    #1 0x154dfa639ebc  (/lib64/libgomp.so.1+0xdebc) (BuildId: ec4fbe8aa26fd14d8ab164545c217e51df48588d)

Indirect leak of 3600 byte(s) in 75 object(s) allocated from:
    #0 0x000000329049 in calloc (/cluster/labs/applications/gromacs/v2026/hip-asan_rocm-7.2.0/bin/gmx+0x329049)
    #1 0x154dfab27c04  (/opt/rocm/lib/libhsa-runtime64.so.1+0x127c04) (BuildId: ce7eb4791df94450257662c9ed8b8236765decfa)

SUMMARY: AddressSanitizer: 54496 byte(s) leaked in 953 allocation(s).
```

---

### 评论 #8 — paubauer (2026-02-18T15:40:31Z)

One of the GROMACS maintainers has collected some extra information upstream (https://gitlab.com/gromacs/gromacs/-/issues/5563#note_3093502422), thanks @al42and

---

### 评论 #9 — al42and (2026-02-18T19:00:43Z)

Note, that my info there is from different HW (RDNA 2 GPU, ROCm 7.2, Ubuntu HWE 6.14 kernel and whatever amdgpu module comes with it) and different input system.

One special thing about this case here could be a very high iteration rate: the `prod.tpr` shared above is _tiny_, I'd expect, ballpark, 1000 steps/second on MI210, limited by how fast ROCm runtime can handle task submissions. If the sawtooth memory usage pattern I've seen is relevant, then could be that there is some memory pool for events in ROCm stack that is cleaned up slower than things are being thrown at it.

---

### 评论 #10 — alexschroeter (2026-02-19T08:37:59Z)

@al42and Thanks, for looking into this. I believe this to be a red hering thow. I have seen the same leak in workloads from other people in the group. I added the prod.tpr to the issue since it grows quite fast (most likely due to the high interation rate) and you can see the memory grow in htop. Other systems just grow slower as far as I can tell. Your theory also doesn't fit the it appeared in ROCm > 6.2.4, I think.

---

### 评论 #11 — tcgu-amd (2026-02-25T21:46:47Z)

Hi @alexschroeter @al42and, thanks for the input! I am not really familiar with the technical details of GROMACS, but if a "sawtooth" memory pattern is being observed, then I agree that the issue is likely not a "leak", since memory *is* being freed. 

---

### 评论 #12 — al42and (2026-03-03T14:48:23Z)

@tcgu-amd, while it might not be a leak (again, I might be seeing a different issue from what @alexschroeter reported), having tons of allocations and wildly changing working set size is not normal. GROMACS itself does not do any mallocs (host or device) on most of the steps (except for one std::string used for logging, which I have since fixed), so the current behavior of the driver is, at best, suboptimal.

---

### 评论 #13 — alexschroeter (2026-03-04T14:06:23Z)

Hi, is there some progress on this issue? I was under the impression the issue was verified by @tcgu-amd . If this is not the case let me know how I can be of assistance. 

- Is there some more complete debug output that will show more? It seems that the memory growth is not tracked by the tools and parameters I have tried so far or the debugging tools are soo slow that I haven't gotten to the leak yet.
- If there is some sort of developer cloud I can get access to I can try to reproduce there.



---

### 评论 #14 — tcgu-amd (2026-03-04T18:36:39Z)

Hi @alexschroeter, sorry for the confusion -- I was not able to verify the issue. I was able to run your workload and were able to observe the leak. However, I can't tell if it is a problem in ROCm, at least valgrind did not report any abnormal memory leaks. 

As for the driver, I think @al42and has a good point and we can take a look to see what's going on down there. Thanks! 

---

### 评论 #15 — tcgu-amd (2026-03-04T20:16:15Z)

@alexschroeter @al42and, I just did more testing and think I might have found a leak. I was running @alexschroeter's reproducer with HSAKMT_DEBUG_LEVEL=7 and found this snippet repeatedly showing up in the logs

```
[hsaKmtAllocMemoryAlign] node 0 bind_mem_to_numa mem 0x74de45e00000 flags 0x20040 size 0x2000000 node_id 0 numa_node_id is out range: numa_node_id 0, num_node 1 
[hsaKmtAllocMemoryAlign] node 0 address 0x74de45e00000 size 33554432 from host 
[hsaKmtMapMemoryToGPUNodes] address 0x74de45e00000 number of nodes 1`
```
And I don't see the correspondign deallocation, so I put a break point at `hsaKmtAllocMemoryAlign` and try to see what as calling it.

Here's the stack trace

```
#0  hsaKmtAllocMemoryAlign (PreferredNode=0, SizeInBytes=134217728, Alignment=0, MemFlags=..., MemoryAddress=0x7fffffff89f0)
    at /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocr-runtime/libhsakmt/src/memory.c:120
#1  0x00007ffff27e6379 in rocr::AMD::KfdDriver::AllocateKfdMemory (size=134217728, node_id=0, flags=<synthetic pointer>...)
    at /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocr-runtime/runtime/hsa-runtime/core/driver/kfd/amd_kfd_driver.cpp:511
#2  rocr::AMD::KfdDriver::AllocateMemory (this=<optimized out>, mem_region=..., alloc_flags=0, mem=0x7fffffff8b00, size=134217728, agent_node_id=<optimized out>)
    at /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocr-runtime/runtime/hsa-runtime/core/driver/kfd/amd_kfd_driver.cpp:292
#3  0x00007ffff2815c12 in rocr::AMD::MemoryRegion::Allocate (this=0x3ab820, size=@0x7fffffff8a88: 134217728, alloc_flags=0, address=0x7fffffff8b00, agent_node_id=0)
    at /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocr-runtime/runtime/hsa-runtime/core/runtime/amd_memory_region.cpp:131
#4  0x00007ffff284e1ad in rocr::core::Runtime::AllocateMemory (this=0x39ed30, region=0x3ab820, size=<optimized out>, alloc_flags=0, address=address@entry=0x7fffffff8b00, agent_node_id=<optimized out>)
    at /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocr-runtime/runtime/hsa-runtime/core/runtime/runtime.cpp:317
#5  0x00007ffff284e34a in operator() (__closure=<optimized out>, __closure=<optimized out>, alignment=<optimized out>, agent_node_id=<optimized out>, alloc_flags=<optimized out>, size=<optimized out>)
    at /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocr-runtime/runtime/hsa-runtime/core/runtime/runtime.cpp:199
#6  std::__invoke_impl<void*, rocr::core::Runtime::RegisterAgent(rocr::core::Agent*, bool)::<lambda(size_t, size_t, rocr::core::MemoryRegion::AllocateFlags, int)>&, long unsigned int, long unsigned int, unsigned int, int> (__f=...) at /usr/include/c++/11/bits/invoke.h:61
#7  std::__invoke_r<void*, rocr::core::Runtime::RegisterAgent(rocr::core::Agent*, bool)::<lambda(size_t, size_t, rocr::core::MemoryRegion::AllocateFlags, int)>&, long unsigned int, long unsigned int, unsigned int, int> (__fn=...) at /usr/include/c++/11/bits/invoke.h:114
#8  std::_Function_handler<void*(long unsigned int, long unsigned int, unsigned int, int), rocr::core::Runtime::RegisterAgent(rocr::core::Agent*, bool)::<lambda(size_t, size_t, rocr::core::MemoryRegion::AllocateFlags, int)> >::_M_invoke(const std::_Any_data &, unsigned long &&, unsigned long &&, unsigned int &&, int &&) (__functor=..., __args#0=<optimized out>, __args#1=<optimized out>, __args#2=<optimized out>,
    __args#3=<optimized out>) at /usr/include/c++/11/bits/std_function.h:290
#9  0x00007ffff286f1b5 in std::function<void* (unsigned long, unsigned long, unsigned int, int)>::operator()(unsigned long, unsigned long, unsigned int, int) const (__args#3=<optimized out>,
    __args#2=<optimized out>, __args#1=<optimized out>, __args#0=<optimized out>, this=0x7ffff2b23ba0 <rocr::core::BaseShared::allocate_()::alloc>) at /usr/include/c++/11/bits/std_function.h:590
#10 rocr::core::SharedSignalPool_t::alloc (this=0x39f568)
    at /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocr-runtime/runtime/hsa-runtime/core/runtime/signal.cpp:79
#11 0x00007ffff286f50a in rocr::core::Shared<rocr::core::SharedSignal, rocr::core::SharedSignalPool_t>::Shared (flags=0, pool=<optimized out>, this=0x1d7e34e8)
    at /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocr-runtime/runtime/hsa-runtime/core/common/shared.h:129
#12 rocr::core::LocalSignal::LocalSignal (this=this@entry=0x1d7e34e8, initial_value=initial_value@entry=0, exportable=exportable@entry=false)
    at /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocr-runtime/runtime/hsa-runtime/core/runtime/signal.cpp:127
```

Long story short, it seems like there are signals being created and the signal pool is allocating memory to accomodate it, but was not free properly, Not 100% sure if this is the cause but it seems pretty likely. Need to investigate more to see what is triggering the signal creation. 

Edit:
btw this is the gromacs side of the stack trace
```
#30 0x00007ffff709334a in DeviceEvent::enqueueWait(DeviceStream const&) () from /root/gromacs/build/bin/../lib/libgromacs_mpi.so.12
#31 0x00007ffff75c5874 in gmx::nbnxn_gpu_x_to_nbat_x(gmx::Grid const&, gmx::NbnxmGpu*, DeviceBuffer<gmx::BasicVector<float> >, GpuEventSynchronizer*, gmx::AtomLocality, int, int, bool) ()
   from /root/gromacs/build/bin/../lib/libgromacs_mpi.so.12
#32 0x00007ffff67d5aef in gmx::nbnxn_atomdata_x_to_nbat_x_gpu(gmx::GridSet const&, gmx::AtomLocality, gmx::NbnxmGpu*, DeviceBuffer<gmx::BasicVector<float> >, GpuEventSynchronizer*) ()
   from /root/gromacs/build/bin/../lib/libgromacs_mpi.so.12
#33 0x00007ffff694c0ec in gmx::nonbonded_verlet_t::convertCoordinatesGpu(gmx::AtomLocality, DeviceBuffer<gmx::BasicVector<float> >, GpuEventSynchronizer*) ()
   from /root/gromacs/build/bin/../lib/libgromacs_mpi.so.12
#34 0x00007ffff7448e45 in gmx::do_force(_IO_FILE*, t_commrec const*, t_inputrec const&, gmx::MDModulesNotifiers const&, gmx::Awh*, gmx_enfrot*, gmx::ImdSession*, pull_t*, long, t_nrnb*, gmx_wallcycle*, gmx_localtop_t const*, float const (*) [3], gmx::ArrayRefWithPadding<gmx::BasicVector<float> >, gmx::ArrayRef<gmx::BasicVector<float> >, history_t const*, gmx::ForceBuffersView*, float (*) [3], t_mdatoms const*, gmx_enerdata_t*, gmx::ArrayRef<float const>, t_forcerec*, gmx::MdrunScheduleWorkload const&, gmx::VirtualSitesHandler*, float*, double, gmx_edsam*, CpuPpLongRangeNonbondeds*, DDBalanceRegionHandler const&) ()
   from /root/gromacs/build/bin/../lib/libgromacs_mpi.so.12
#35 0x00007ffff77e41e6 in gmx::LegacySimulator::do_md() () from /root/gromacs/build/bin/../lib/libgromacs_mpi.so.12
#36 0x00007ffff7806f69 in gmx::Mdrunner::mdrunner() () from /root/gromacs/build/bin/../lib/libgromacs_mpi.so.12
#37 0x000000000020ec65 in gmx::gmx_mdrun(ompi_communicator_t*, gmx_hw_info_t const&, int, char**) ()
#38 0x000000000020e909 in gmx::gmx_mdrun(int, char**) ()
#39 0x00007ffff7031d0d in gmx::CommandLineModuleManager::run(int, char**) () from /root/gromacs/build/bin/../lib/libgromacs_mpi.so.12
#40 0x000000000020d46a in main ()
```


---

### 评论 #16 — al42and (2026-03-04T23:37:41Z)

> btw this is the gromacs side of the stack trace

FYI, [`enqueueWait` does just `hipStreamWaitEvent`](https://gitlab.com/gromacs/gromacs/-/blob/v2026.0/src/gromacs/gpu_utils/device_event_hip.h?ref_type=tags#L100-107).

Inspired by that, the code below also exhibits pretty stable memory growth on my system.

<details><summary>`hip_ping_pong.cpp`</summary>
<p>

```cpp
#include <hip/hip_runtime.h>
#include <iostream>

__global__ void short_kernel() {
    // Just a dummy kernel doing minimal work
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx == 0) {
    }
}

int main() {
    hipStream_t streamA, streamB;
    hipError_t err;

    err = hipStreamCreate(&streamA);
    if (err != hipSuccess) {
        std::cerr << "Failed to create stream A" << std::endl;
        return 1;
    }

    err = hipStreamCreate(&streamB);
    if (err != hipSuccess) {
        std::cerr << "Failed to create stream B" << std::endl;
        return 1;
    }

    hipEvent_t eventA, eventB;
    err = hipEventCreate(&eventA);
    if (err != hipSuccess) {
        std::cerr << "Failed to create event A" << std::endl;
        return 1;
    }

    err = hipEventCreate(&eventB);
    if (err != hipSuccess) {
        std::cerr << "Failed to create event B" << std::endl;
        return 1;
    }

    std::cout << "Starting infinite loop. Press Ctrl+C to exit." << std::endl;

    long long iter = 0;
    while (true) {
        // Submit short kernel to stream A
        hipLaunchKernelGGL(short_kernel, dim3(1), dim3(1), 0, streamA);

        // Record event A in stream A
        hipEventRecord(eventA, streamA);

        // Stream B waits on event A
        hipStreamWaitEvent(streamB, eventA, 0);

        // Submit short kernel to stream B
        hipLaunchKernelGGL(short_kernel, dim3(1), dim3(1), 0, streamB);

        // Record event B in stream B
        hipEventRecord(eventB, streamB);

        // Stream A waits on event B
        hipStreamWaitEvent(streamA, eventB, 0);

        iter++;
        if (iter % 10000 == 0) {
            hipStreamSynchronize(streamA);
        }
        if (iter % 100000 == 0) {
            std::cout << "Iterations: " << iter << "\r" << std::flush;
        }
    }

    // Cleanup (unreachable due to infinite loop, but good practice)
    hipEventDestroy(eventA);
    hipEventDestroy(eventB);
    hipStreamDestroy(streamA);
    hipStreamDestroy(streamB);

    return 0;
}
```

</p>
</details> 

---

### 评论 #17 — kentrussell (2026-03-12T18:20:53Z)

@ApurvMishra-amd Do you think your leak investigation could apply to this one too? Maybe once we get all of your patches and Shweta's patches in, we can re-test and see if we can repro the leak, or if we caught it with the other leak issues we're working on.

---

### 评论 #18 — ApurvMishra-amd (2026-03-17T23:59:04Z)

> [@ApurvMishra-amd](https://github.com/ApurvMishra-amd) Do you think your leak investigation could apply to this one too? Maybe once we get all of your patches and Shweta's patches in, we can re-test and see if we can repro the leak, or if we caught it with the other leak issues we're working on.

Hi, @kentrussell . My patch has been merged. The issue here seems different as it comes from signals created on every _hipStreamWaitEvent_ which should be destroyed once the dependency is satisfied. Thus, it seems like a HIP runtime bug, coming from _libamdhip64_ library.

---

### 评论 #19 — alexschroeter (2026-03-20T08:35:25Z)

Are there any updates? Asking for a friend ;)

---

### 评论 #20 — tcgu-amd (2026-03-20T20:56:52Z)

@alexschroeter Yes, I have spent the past few days trying to pin down the root cause of the issue in clr. @ApurvMishra-amd I think you are right, the source of the problem is probably here 
https://github.com/ROCm/rocm-systems/blob/982b3e7b98a3410fd0d3dc63ce28b4201781742d/projects/clr/rocclr/device/rocm/rocvirtual.cpp#L473-L483

```
  // If GPU is still busy with processing, then add more signals to avoid more frequent stalls
  if (Hsa::signal_load_relaxed(signal_list_[temp_id]->signal_) > 0) {
    std::unique_ptr<ProfilingSignal> signal(new ProfilingSignal());
    if ((signal != nullptr) && CreateSignal(signal.get())) {
      // Find valid new index
      ++current_id_ %= signal_list_.size();
      // Insert the new signal into the current slot and ignore any wait
      signal_list_.insert(signal_list_.begin() + current_id_, signal.release());
      new_signal = true;
    }
  }
````
Due to the snippet above, the signal list will continue to increase, and there doesn't seem like to be a mechanism to trim it down during runtime. I'm getting in touch with the devs for this part of the code to see how this can be fixed. Thanks! 

---

### 评论 #21 — tcgu-amd (2026-03-23T19:46:30Z)

Hi @alexschroeter @al42and, I think the issue is at least partially addressed in the latest version of the code via commit https://github.com/ROCm/rocm-systems/commit/839fb957173fcef0fc29dcd0f7efaab1a797a4b2

To explain, I had a conversation with authors of the snippet I linked above. What is happening here is that `signal_list_` is a ring buffer acting as a queue for signals to be processed. The logic above basically translates to if the buffer is full of actively queued up signal, then we expand the buffer by inserting the signal to the list directly so we can keep on submitting work to without stalling the CPU until previous signals are processed by the GPU. This design is necessary to avoid latency in ROCm and is key to ROCm's performance.

Just as @al42and has theorized, when GROMACS starts creating events at a faster rate than the GPU can process them, we see that the buffer will simply keep on growing. In normal compute workloads, this is not much of a problem because the GPU is rarely kept at a busy state 100% of the time and in-between compute cycles it will be allowed a chance to catch up to the CPU, but this is not true for GROMACS.  

I think this problem has always been there, but previously, it was leaking at a far slower speed, and somewhere around ROCm 7.1 it got worse significantly due to this commit https://github.com/ROCm/rocm-systems/commit/8971f7b089#diff-b8c72dfa6d0480c775e1b13acdb1e2879fb76ead1c862924c1893e75674dfa0dR442, which is probably why it became really noticeable.  After https://github.com/ROCm/rocm-systems/commit/839fb957173fcef0fc29dcd0f7efaab1a797a4b2, I tested with GROMACS again and I think it is now reverted back to its previous level of memory consumption in ROCm 6.x, which should be more manageable.

So how can we fix this? An idea would be to arbitrarily limit the size of signal_list_, so beyond a certain size we stop immediately inserting signals to the list and instead wait for a slot to free up. However, this is tricky because in a lot of cases trading memory for latency **is** beneficial and there's no reliable way to tell how big of a signal_list_ is too big. I am currently in discussion with the internal devs but it is still unclear if this is going to be the direction to take.

Another option is to have clearer documentation/error messaging regarding this behavior and encouraging users to limit the rate at which events are submitted to avoid running into this problem. 

What do you guys think? Please feel free to comment as any thoughts and ideas would be appreciated. Thanks!!! :)


---

### 评论 #22 — al42and (2026-03-23T22:13:23Z)

Thanks for digging to the bottom of it, @tcgu-amd.

One thing that's still not quite clear to me. GROMACS workload is fairly regular: we submit a few hundred timesteps, then wait for the GPU (on one event, but it should be dependent on all the submitted work), then repeat. There's an upper bound on the number of operations in flight, and it should be reached quite quickly. We're talking about a few walltime ms per step in this case, so GROMACS does device-host sync every few walltime seconds; I can see why the list would have grown initially, but it should have stabilized after a few seconds, no? Or is it growing every time we exceed the ring buffer size, regardless of whether we exceed the previous maximum?

> However, this is tricky because in a lot of cases trading memory for latency is beneficial and there's no reliable way to tell how big of a signal_list_ is too big. I am currently in discussion with the internal devs but it is still unclear if this is going to be the direction to take.

FWIW, for GROMACS, it can be up to ~500 timesteps between host-device syncs and ~30 device ops/step. Can be more, but that's an upper bound for typical cases.

> Another option is to have clearer documentation/error messaging regarding this behavior and encouraging users to limit the rate at which events are submitted to avoid running into this problem.

Warnings would be good, but implementing throttling on the application side sounds unpleasant.

---

### 评论 #23 — alexschroeter (2026-03-24T09:02:41Z)

Thanks for the investigation @tcgu-amd, this is definitely progress. However, I'm not fully convinced this addresses the core issue.
If I understand correctly, ROCm/rocm-systems@839fb95 reverts the acceleration introduced by ROCm/rocm-systems@8971f7b089 which landed around ROCm 7.1. That explains why the leak got dramatically worse in 7.1.1 — but the leak itself was already present in 6.4.4 (just slower). So reverting to "6.x levels of memory consumption" means reverting to a slower leak, not fixing it.

The regression window I've been able to narrow down is ROCm > 6.2.4 and <= 6.4.4. Something changed in that window that broke the signal recycling, and ROCm/rocm-systems@8971f7b089 only made it worse later. Your fix addresses the acceleration, not the introduction.

As @al42and pointed out, GROMACS does a host-device sync every few seconds, so the number of in-flight operations is bounded. The signal_list_ should reach a steady state fairly quickly and stop growing. The fact that it keeps growing indefinitely suggests that completed signals are not being properly recycled back into the ring buffer, causing the insert path to fire continuously instead of being a rare event.

This also matches what I see with ASAN — the same ~54KB of leaked allocations after 3 minutes and after 5 hours. The actual memory growth isn't coming from malloc-visible allocations but from the HSA signal pool (hsaKmtAllocMemoryAlign) which goes through mmap/kernel allocations that ASAN can't track. That's consistent with your stack trace showing SharedSignalPool_t::alloc allocating 128MB chunks via hsaKmtAllocMemoryAlign that never get freed.
So I think there are two bugs here:

- ✅ The signal_list_ growth acceleration introduced in ~7.1 — addressed by ROCm/rocm-systems@839fb95 
- The broken signal recycling introduced between 6.2.4 and 6.4.4 that prevents the signal_list_ from reaching a steady state — still open

Could you check what changed in CLR's signal management in that version window? Something must have changed in how signals are reclaimed after completion.


---

### 评论 #24 — alexschroeter (2026-03-24T09:47:04Z)

I am looking at this commit for a likely candidate https://github.com/ROCm/rocm-systems/commit/18187cd8fe724a3af6d5e4c27c31e5a5a2629bd9

**6.2.4 flow** with `hipStreamWaitEvent`:
1. `AddExternalSignal()` sets `engine_ = External`
2. Next `WaitingSignal(Compute)`: `Compute != External` → **`explicit_wait = true`**
3. Inside the explicit_wait block: **adds the internal signal `signal_list_[current_id_]` to the wait list**
4. The internal signal gets waited on (CPU wait or GPU barrier)
5. This gives the GPU time to complete operations → `ActiveSignal()` finds completed signals → **no list growth**

**6.3.0 flow** with `hipStreamWaitEvent`:
1. `AddExternalSignal()` does NOT change `engine_` (stays `Compute`)
2. Next `WaitingSignal(Compute)`: `Compute == Compute` → **`explicit_wait = false`**
3. External signals are validated and cleared (moved outside the block), but **the internal signal is NOT waited on**
4. CPU races ahead without back-pressure → `ActiveSignal()` finds busy signals → **list grows**

---

### 评论 #25 — gandryey (2026-03-25T00:13:46Z)

There are already other native limits on scheduled GPU workloads, specifically the queue size and constant buffer size. As a result, the signal pool size cannot exceed the AQL queue size, which is capped at 16K AQL packets. With 4 hardware queues by default, the total HSA signals should be limited to a maximum of 64K per GPU. If the observed count is significantly higher than that, something is likely wrong.

---

### 评论 #26 — ye-luo (2026-03-25T01:02:35Z)

If GROMACS ends normally in a long run, are there still leaks?
If the answer is yes, the leak can be potentially a more severe issue since it can be a cause of slow growing memory.

---

### 评论 #27 — tcgu-amd (2026-03-30T18:56:17Z)

@gandryey @al42and @alexschroeter. So a couple new findings. 

As I have mentioned before, after updating to the latest ROCm nightly build from TheRock and rebuilding GROMACs, I have found the "leak" speed to be significantly slower now. Previously it would easily consume tens of gbs in a few minutes, and now it would only consume a couple GB  over a few hours.

So I was curious to see if the "leak" would continue or will there be some sort equilibrium state it will eventually reach. I left GROMACS to run over the weekend, and this morning I saw it had consumed 68 out of 90 GB available on my dev system. In other words, it is still very much an unbounded leak. 

>4 hardware queues by default, the total HSA signals should be limited to a maximum of 64K per GPU. If the observed count is significantly higher than that, something is likely wrong.

I checked the size of signal_pool_ in the ActiveSignal function by the end of the run, and it indeed appear to have an  _**enormous size of 7.6M elements**_ , which far exceeds the number of elements you mentioned. (or maybe my calculations are wrong, since `signal_pool_.size` does not work in gdb, so I had to calculate the size manually based on the internal variables. This is what I saw from gdb 
```
p signal_pool_
$1 = {c = {<std::_Deque_base<amd::roc::ProfilingSignal*, std::allocator<amd::roc::ProfilingSignal*> >> = {
      _M_impl = {<std::allocator<amd::roc::ProfilingSignal*>> = {<__gnu_cxx::new_allocator<amd::roc::ProfilingSignal*>> = {<No data fields>}, <No data fields>}, <std::_Deque_base<amd::roc::ProfilingSignal*,
std::allocator<amd::roc::ProfilingSignal*> >::_Deque_impl_data> = {_M_map = 0x555fc6d6b090, _M_map_size = 327678, _M_start = {_M_cur = 0x555556052060, _M_first = 0x555556052060, _M_last = 0x555556052260,
            _M_node = 0x555fc6e405d8}, _M_finish = {_M_cur = 0x5560e92e0da0, _M_first = 0x5560e92e0ca0, _M_last = 0x5560e92e0ea0, _M_node = 0x555fc6f29de0}}, <No data fields>}}, <No data fields>}}
```
please feel free to verify :)
)

I also checked the block size from the ROCR Runtime side, in the [`SharedSignalPool_t::alloc()` function](https://github.com/ROCm/rocm-systems/blob/56ce0c6855152fd0de483e7fc1c9c2aadbf02c42/projects/rocr-runtime/runtime/hsa-runtime/core/runtime/signal.cpp#L99).  _**The current `block_size_` is sitting at 134217728**_, which means the latest block allocated has a size of `67108864*128 = 8.7 GB`. This doesn't appear to be normal either. 

So based on the above findings, I think we can conclude that the problem, in the very least, still largely exists around the signal lifecycles. @gandryey Any suggestion how we can kick off an in-depth investigation? 

---

### 评论 #28 — al42and (2026-04-01T22:16:46Z)

> If GROMACS ends normally in a long run, are there still leaks?

There could be some memory allocations not freed at the end of the run from GROMACS itself. However, those should be **one-off**, allocated only once at the start of the run, with no ongoing memory growth. People are sometimes running GROMACS for weeks (if their scheduling system allows that) and we take care to avoid continuous memory leaks.

---

### 评论 #29 — tcgu-amd (2026-04-06T18:05:49Z)

Hi @al42and, @alexschroeter, we recently merged a PR that seem to fix this issue https://github.com/ROCm/rocm-systems/pull/4653. I built GROMACS with the latest ROCm 7.13 nightly from TheRock that includes the patch and tested with @alexschroeter's workload -- I didn't see any significant memory leak. At least if there still is, it is at a far slower rate compared to before. 

---

### 评论 #30 — al42and (2026-04-07T23:38:35Z)

Thanks, @tcgu-amd! Could you please summarize which versions of software were affected so we can write up a known issue?

---

### 评论 #31 — tcgu-amd (2026-04-08T14:20:02Z)

Hi @al42and, the affected versions should include ROCm 6.3.1 - ROCm 7.2.1. Thanks! 

---

### 评论 #32 — al42and (2026-04-08T19:19:12Z)

Thanks for tracking this thing down, @tcgu-amd and @alexschroeter!

---

### 评论 #33 — alexschroeter (2026-04-09T12:11:19Z)

I have been running with ROCm 7.13.0-nightly now for 2h and there is no sign of the leak. Thank you for tracking this down and the fix.

---
