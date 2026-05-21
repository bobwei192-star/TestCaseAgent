# [Issue]: rocm-clinfo 6.2.0 segmentation fault

> **Issue #3664**
> **状态**: closed
> **创建时间**: 2024-09-03T14:13:25Z
> **更新时间**: 2024-10-07T15:28:21Z
> **关闭时间**: 2024-10-07T15:15:29Z
> **作者**: Germano0
> **标签**: Under Investigation, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3664

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

`rocm-clinfo` crashes.

Despite the GPU may not be any longer supported, rocm-clinfo should handle the exception without crashing.
Please remove `AMD Radeon VII` label, cause it was a random GPU I selected in the limited-choice menu concerning GPU type
```
OS:
NAME="Fedora Linux"
VERSION="40 (KDE Plasma)"

CPU: 
model name      : AMD Ryzen 5 3600 6-Core Processor

GPU:
  Name:                    AMD Ryzen 5 3600 6-Core Processor  
  Marketing Name:          AMD Ryzen 5 3600 6-Core Processor  
  Name:                    gfx803                             
  Marketing Name:          AMD Radeon RX 480 Graphics         
      Name:                    amdgcn-amd-amdhsa--gfx803 
```
```
# coredumpctl gdb 2050183
           PID: 2050183 (rocm-clinfo)
           UID: 1000 (user)
           GID: 1000 (user)
        Signal: 11 (SEGV)
     Timestamp: Tue 2024-09-03 16:01:21 CEST (2min 49s ago)
  Command Line: rocm-clinfo
    Executable: /usr/bin/rocm-clinfo
 Control Group: /user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.yakuake@autostart.service
          Unit: user@1000.service
     User Unit: app-org.kde.yakuake@autostart.service
         Slice: user-1000.slice
     Owner UID: 1000 (user)
       Boot ID: 31dd572ef5774add8ec96d9b45ea797d
    Machine ID: 56106060e6fd4ce59080ab83290e52dc
      Hostname: machine
       Storage: /var/lib/systemd/coredump/core.rocm-clinfo.1000.31dd572ef5774add8ec96d9b45ea797d.2050183.1725372081000000.zst (present)
  Size on Disk: 1.6M
       Package: rocclr/6.2.0-1.fc40
      build-id: 1fe1a0ad46b8199df7fac9014d376c6be119c14a
       Message: Process 2050183 (rocm-clinfo) of user 1000 dumped core.
                
                Module libhsakmt.so.1 from rpm hsakmt-1.0.6-41.rocm6.2.0.fc40.x86_64
                Module libnuma.so.1 from rpm numactl-2.0.16-5.fc40.x86_64
                Module libhsa-runtime64.so.1 from rpm rocm-runtime-6.2.0-2.fc40.x86_64
                Module libamd_comgr.so.2 from rpm rocm-compilersupport-18-2.rocm6.2.0.fc40.x86_64
                Module libSPIRV-Tools-link.so from rpm spirv-tools-2024.3-2.fc40.x86_64
                Module libSPIRV-Tools.so from rpm spirv-tools-2024.3-2.fc40.x86_64
                Module libSPIRV-Tools-opt.so from rpm spirv-tools-2024.3-2.fc40.x86_64
                Module libLLVMSPIRVLib.so.18.1 from rpm spirv-llvm-translator-18.1.2-1.fc40.x86_64
                Module libRusticlOpenCL.so.1 from rpm mesa-24.1.6-1.fc40.x86_64
                Module libdrm_amdgpu.so.1 from rpm libdrm-2.4.123-1.fc40.x86_64
                Module libdrm_radeon.so.1 from rpm libdrm-2.4.123-1.fc40.x86_64
                Module pipe_radeonsi.so from rpm mesa-24.1.6-1.fc40.x86_64
                Module libtinfo.so.6 from rpm ncurses-6.4-12.20240127.fc40.x86_64
                Module libedit.so.0 from rpm libedit-3.1-53.20240808cvs.fc40.x86_64
                Module libffi.so.8 from rpm libffi-3.4.4-7.fc40.x86_64
                Module libexpat.so.1 from rpm expat-2.6.2-1.fc40.x86_64
                Module libdrm.so.2 from rpm libdrm-2.4.123-1.fc40.x86_64
                Module libelf.so.1 from rpm elfutils-0.191-4.fc40.x86_64
                Module libzstd.so.1 from rpm zstd-1.5.6-1.fc40.x86_64
                Module libz.so.1 from rpm zlib-ng-2.1.7-1.fc40.x86_64
                Module libMesaOpenCL.so.1 from rpm mesa-24.1.6-1.fc40.x86_64
                Module libOpenCL.so.1 from rpm ocl-icd-2.3.2-6.fc40.x86_64
                Module rocm-clinfo from rpm rocclr-6.2.0-1.fc40.x86_64
                Stack trace of thread 2050183:
                #0  0x00007f76b617cb49 __memset_avx2_unaligned_erms (libc.so.6 + 0x16db49)
                #1  0x00007f76a0838860 _ZNK4rocr3AMD8GpuAgent14AssembleShaderEPKcNS1_14AssembleTargetERPvRm (libhsa-runtime64.so.1 + 0x38860)
                #2  0x00007f76a083a92b _ZN4rocr3AMD8GpuAgent13PostToolsInitEv (libhsa-runtime64.so.1 + 0x3a92b)
                #3  0x00007f76a0851b9d _ZN4rocr3HSA8hsa_initEv (libhsa-runtime64.so.1 + 0x51b9d)
                #4  0x00007f76a99505d4 _ZN3amd3roc6Device4initEv (libamdocl64.so.6.2 + 0xb85d4)
                #5  0x00007f76a99b2863 _ZN3amd6Device4initEv (libamdocl64.so.6.2 + 0x11a863)
                #6  0x00007f76a991d14d _ZZNSt9once_flag18_Prepare_executionC4IZSt9call_onceIZ22clIcdGetPlatformIDsKHREUlvE_JEEvRS_OT_DpOT0_EUlvE_EERS5_ENUlvE_4_FUNEv (libamdocl64.so.6.2 + 0x8514d)
                #7  0x00007f76b60aba4b __pthread_once_slow (libc.so.6 + 0x9ca4b)
                #8  0x00007f76b60abab9 ___pthread_once (libc.so.6 + 0x9cab9)
                #9  0x00007f76a991cfae __gthread_once (libamdocl64.so.6.2 + 0x84fae)
                #10 0x00007f76b65d9465 _find_and_check_platforms (libOpenCL.so.1 + 0xd465)
                #11 0x00007f76b65db68c _initClIcd (libOpenCL.so.1 + 0xf68c)
                #12 0x0000561bdba113b0 _ZN2cl8Platform3getEPSt6vectorIS0_SaIS0_EE (rocm-clinfo + 0xc3b0)
                #13 0x0000561bdba085be main (rocm-clinfo + 0x35be)
                #14 0x00007f76b6039088 __libc_start_call_main (libc.so.6 + 0x2a088)
                #15 0x00007f76b603914b __libc_start_main_impl (libc.so.6 + 0x2a14b)
                #16 0x0000561bdba0eaa5 _start (rocm-clinfo + 0x9aa5)
                
                Stack trace of thread 2050185:
                #0  0x00007f76b60a2da9 __futex_abstimed_wait_common64 (libc.so.6 + 0x93da9)
                #1  0x00007f76b60a57f9 __pthread_cond_wait_common (libc.so.6 + 0x967f9)
                #2  0x00007f76a9f57a9d cnd_wait (pipe_radeonsi.so + 0x157a9d)
                #3  0x00007f76a9f3aa0b util_queue_thread_func (pipe_radeonsi.so + 0x13aa0b)
                #4  0x00007f76a9f579fc impl_thrd_routine (pipe_radeonsi.so + 0x1579fc)
                #5  0x00007f76b60a66d7 start_thread (libc.so.6 + 0x976d7)
                #6  0x00007f76b612a60c __clone3 (libc.so.6 + 0x11b60c)
                
                Stack trace of thread 2050184:
                #0  0x00007f76b60a2da9 __futex_abstimed_wait_common64 (libc.so.6 + 0x93da9)
                #1  0x00007f76b60a57f9 __pthread_cond_wait_common (libc.so.6 + 0x967f9)
                #2  0x00007f76a9f57a9d cnd_wait (pipe_radeonsi.so + 0x157a9d)
                #3  0x00007f76a9f3aa0b util_queue_thread_func (pipe_radeonsi.so + 0x13aa0b)
                #4  0x00007f76a9f579fc impl_thrd_routine (pipe_radeonsi.so + 0x1579fc)
                #5  0x00007f76b60a66d7 start_thread (libc.so.6 + 0x976d7)
                #6  0x00007f76b612a60c __clone3 (libc.so.6 + 0x11b60c)
                
                Stack trace of thread 2050187:
                #0  0x00007f76b60a2da9 __futex_abstimed_wait_common64 (libc.so.6 + 0x93da9)
                #1  0x00007f76b60a57f9 __pthread_cond_wait_common (libc.so.6 + 0x967f9)
                #2  0x00007f76a9f57a9d cnd_wait (pipe_radeonsi.so + 0x157a9d)
                #3  0x00007f76a9f3aa0b util_queue_thread_func (pipe_radeonsi.so + 0x13aa0b)
                #4  0x00007f76a9f579fc impl_thrd_routine (pipe_radeonsi.so + 0x1579fc)
                #5  0x00007f76b60a66d7 start_thread (libc.so.6 + 0x976d7)
                #6  0x00007f76b612a60c __clone3 (libc.so.6 + 0x11b60c)
                
                Stack trace of thread 2050189:
                #0  0x00007f76b60a2da9 __futex_abstimed_wait_common64 (libc.so.6 + 0x93da9)
                #1  0x00007f76b60a57f9 __pthread_cond_wait_common (libc.so.6 + 0x967f9)
                #2  0x00007f76a9f57a9d cnd_wait (pipe_radeonsi.so + 0x157a9d)
                #3  0x00007f76a9f3aa0b util_queue_thread_func (pipe_radeonsi.so + 0x13aa0b)
                #4  0x00007f76a9f579fc impl_thrd_routine (pipe_radeonsi.so + 0x1579fc)
                #5  0x00007f76b60a66d7 start_thread (libc.so.6 + 0x976d7)
                #6  0x00007f76b612a60c __clone3 (libc.so.6 + 0x11b60c)
                
                Stack trace of thread 2050186:
                #0  0x00007f76b60a2da9 __futex_abstimed_wait_common64 (libc.so.6 + 0x93da9)
                #1  0x00007f76b60a57f9 __pthread_cond_wait_common (libc.so.6 + 0x967f9)
                #2  0x00007f76a9f57a9d cnd_wait (pipe_radeonsi.so + 0x157a9d)
                #3  0x00007f76a9f3aa0b util_queue_thread_func (pipe_radeonsi.so + 0x13aa0b)
                #4  0x00007f76a9f579fc impl_thrd_routine (pipe_radeonsi.so + 0x1579fc)
                #5  0x00007f76b60a66d7 start_thread (libc.so.6 + 0x976d7)
                #6  0x00007f76b612a60c __clone3 (libc.so.6 + 0x11b60c)
                
                Stack trace of thread 2050188:
                #0  0x00007f76b60a2da9 __futex_abstimed_wait_common64 (libc.so.6 + 0x93da9)
                #1  0x00007f76b60a57f9 __pthread_cond_wait_common (libc.so.6 + 0x967f9)
                #2  0x00007f76a9f57a9d cnd_wait (pipe_radeonsi.so + 0x157a9d)
                #3  0x00007f76a9f3aa0b util_queue_thread_func (pipe_radeonsi.so + 0x13aa0b)
                #4  0x00007f76a9f579fc impl_thrd_routine (pipe_radeonsi.so + 0x1579fc)
                #5  0x00007f76b60a66d7 start_thread (libc.so.6 + 0x976d7)
                #6  0x00007f76b612a60c __clone3 (libc.so.6 + 0x11b60c)
                ELF object binary architecture: AMD x86-64

GNU gdb (Fedora Linux) 14.2-3.fc40
Copyright (C) 2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-redhat-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from /usr/bin/rocm-clinfo...
Reading symbols from /usr/lib/debug/usr/bin/rocm-clinfo-6.2.0-1.fc40.x86_64.debug...
[New LWP 2050183]
[New LWP 2050185]
[New LWP 2050184]
[New LWP 2050187]
[New LWP 2050189]
[New LWP 2050186]
[New LWP 2050188]

This GDB supports auto-downloading debuginfo from the following URLs:
  <https://debuginfod.fedoraproject.org/>
Enable debuginfod for this session? (y or [n]) n
Debuginfod has been disabled.
To make this setting permanent, add 'set debuginfod enabled off' to .gdbinit.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
Core was generated by `rocm-clinfo'.
Program terminated with signal SIGSEGV, Segmentation fault.
--Type <RET> for more, q to quit, c to continue without paging--c
#0  __memset_avx2_unaligned_erms () at ../sysdeps/x86_64/multiarch/memset-vec-unaligned-erms.S:246
246             VMOVU   %VMM(0), (%rdi)
[Current thread is 1 (Thread 0x7f76b64b5740 (LWP 2050183))]
(gdb) set height 0
(gdb) set print elements 0
(gdb) set print frame-arguments all
(gdb) thread apply all backtrace

Thread 7 (Thread 0x7f76a28006c0 (LWP 2050188)):
#0  0x00007f76b60a2da9 in __futex_abstimed_wait_common64 (private=0, futex_word=0x561bfb99f780, expected=0, op=393, abstime=0x0, cancel=true) at futex-internal.c:57
#1  __futex_abstimed_wait_common (futex_word=futex_word@entry=0x561bfb99f780, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0, cancel=cancel@entry=true) at futex-internal.c:87
#2  0x00007f76b60a2e2f in __GI___futex_abstimed_wait_cancelable64 (futex_word=futex_word@entry=0x561bfb99f780, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0) at futex-internal.c:139
#3  0x00007f76b60a57f9 in __pthread_cond_wait_common (cond=0x561bfb99f758, mutex=<optimized out>, clockid=0, abstime=0x0) at pthread_cond_wait.c:503
#4  ___pthread_cond_wait (cond=0x561bfb99f758, mutex=<optimized out>) at pthread_cond_wait.c:618
#5  0x00007f76a9f57a9d in cnd_wait (cond=<optimized out>, mtx=<optimized out>) at ../src/c11/impl/threads_posix.c:135
#6  0x00007f76a9f3aa0b in util_queue_thread_func (input=input@entry=0x561bfb9e40f0) at ../src/util/u_queue.c:290
#7  0x00007f76a9f579fc in impl_thrd_routine (p=<optimized out>) at ../src/c11/impl/threads_posix.c:67
#8  0x00007f76b60a66d7 in start_thread (arg=<optimized out>) at pthread_create.c:447
#9  0x00007f76b612a60c in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:78

Thread 6 (Thread 0x7f76a3e006c0 (LWP 2050186)):
#0  0x00007f76b60a2da9 in __futex_abstimed_wait_common64 (private=0, futex_word=0x561bfb911f08, expected=0, op=393, abstime=0x0, cancel=true) at futex-internal.c:57
#1  __futex_abstimed_wait_common (futex_word=futex_word@entry=0x561bfb911f08, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0, cancel=cancel@entry=true) at futex-internal.c:87
#2  0x00007f76b60a2e2f in __GI___futex_abstimed_wait_cancelable64 (futex_word=futex_word@entry=0x561bfb911f08, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0) at futex-internal.c:139
#3  0x00007f76b60a57f9 in __pthread_cond_wait_common (cond=0x561bfb911ee0, mutex=<optimized out>, clockid=0, abstime=0x0) at pthread_cond_wait.c:503
#4  ___pthread_cond_wait (cond=0x561bfb911ee0, mutex=<optimized out>) at pthread_cond_wait.c:618
#5  0x00007f76a9f57a9d in cnd_wait (cond=<optimized out>, mtx=<optimized out>) at ../src/c11/impl/threads_posix.c:135
#6  0x00007f76a9f3aa0b in util_queue_thread_func (input=input@entry=0x561bfb9902a0) at ../src/util/u_queue.c:290
#7  0x00007f76a9f579fc in impl_thrd_routine (p=<optimized out>) at ../src/c11/impl/threads_posix.c:67
#8  0x00007f76b60a66d7 in start_thread (arg=<optimized out>) at pthread_create.c:447
#9  0x00007f76b612a60c in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:78

Thread 5 (Thread 0x7f76a1e006c0 (LWP 2050189)):
#0  0x00007f76b60a2da9 in __futex_abstimed_wait_common64 (private=0, futex_word=0x561bfb9f2ee0, expected=0, op=393, abstime=0x0, cancel=true) at futex-internal.c:57
#1  __futex_abstimed_wait_common (futex_word=futex_word@entry=0x561bfb9f2ee0, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0, cancel=cancel@entry=true) at futex-internal.c:87
#2  0x00007f76b60a2e2f in __GI___futex_abstimed_wait_cancelable64 (futex_word=futex_word@entry=0x561bfb9f2ee0, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0) at futex-internal.c:139
#3  0x00007f76b60a57f9 in __pthread_cond_wait_common (cond=0x561bfb9f2eb8, mutex=<optimized out>, clockid=0, abstime=0x0) at pthread_cond_wait.c:503
#4  ___pthread_cond_wait (cond=0x561bfb9f2eb8, mutex=<optimized out>) at pthread_cond_wait.c:618
#5  0x00007f76a9f57a9d in cnd_wait (cond=<optimized out>, mtx=<optimized out>) at ../src/c11/impl/threads_posix.c:135
#6  0x00007f76a9f3aa0b in util_queue_thread_func (input=input@entry=0x561bfba28e30) at ../src/util/u_queue.c:290
#7  0x00007f76a9f579fc in impl_thrd_routine (p=<optimized out>) at ../src/c11/impl/threads_posix.c:67
#8  0x00007f76b60a66d7 in start_thread (arg=<optimized out>) at pthread_create.c:447
#9  0x00007f76b612a60c in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:78

Thread 4 (Thread 0x7f76a34006c0 (LWP 2050187)):
#0  0x00007f76b60a2da9 in __futex_abstimed_wait_common64 (private=0, futex_word=0x561bfb9120b8, expected=0, op=393, abstime=0x0, cancel=true) at futex-internal.c:57
#1  __futex_abstimed_wait_common (futex_word=futex_word@entry=0x561bfb9120b8, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0, cancel=cancel@entry=true) at futex-internal.c:87
#2  0x00007f76b60a2e2f in __GI___futex_abstimed_wait_cancelable64 (futex_word=futex_word@entry=0x561bfb9120b8, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0) at futex-internal.c:139
#3  0x00007f76b60a57f9 in __pthread_cond_wait_common (cond=0x561bfb912090, mutex=<optimized out>, clockid=0, abstime=0x0) at pthread_cond_wait.c:503
#4  ___pthread_cond_wait (cond=0x561bfb912090, mutex=<optimized out>) at pthread_cond_wait.c:618
#5  0x00007f76a9f57a9d in cnd_wait (cond=<optimized out>, mtx=<optimized out>) at ../src/c11/impl/threads_posix.c:135
#6  0x00007f76a9f3aa0b in util_queue_thread_func (input=input@entry=0x561bfb9904e0) at ../src/util/u_queue.c:290
#7  0x00007f76a9f579fc in impl_thrd_routine (p=<optimized out>) at ../src/c11/impl/threads_posix.c:67
#8  0x00007f76b60a66d7 in start_thread (arg=<optimized out>) at pthread_create.c:447
#9  0x00007f76b612a60c in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:78

Thread 3 (Thread 0x7f76a94006c0 (LWP 2050184)):
#0  0x00007f76b60a2da9 in __futex_abstimed_wait_common64 (private=0, futex_word=0x561bfb90da68, expected=0, op=393, abstime=0x0, cancel=true) at futex-internal.c:57
#1  __futex_abstimed_wait_common (futex_word=futex_word@entry=0x561bfb90da68, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0, cancel=cancel@entry=true) at futex-internal.c:87
#2  0x00007f76b60a2e2f in __GI___futex_abstimed_wait_cancelable64 (futex_word=futex_word@entry=0x561bfb90da68, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0) at futex-internal.c:139
#3  0x00007f76b60a57f9 in __pthread_cond_wait_common (cond=0x561bfb90da40, mutex=<optimized out>, clockid=0, abstime=0x0) at pthread_cond_wait.c:503
#4  ___pthread_cond_wait (cond=0x561bfb90da40, mutex=<optimized out>) at pthread_cond_wait.c:618
#5  0x00007f76a9f57a9d in cnd_wait (cond=<optimized out>, mtx=<optimized out>) at ../src/c11/impl/threads_posix.c:135
#6  0x00007f76a9f3aa0b in util_queue_thread_func (input=input@entry=0x561bfb90b920) at ../src/util/u_queue.c:290
#7  0x00007f76a9f579fc in impl_thrd_routine (p=<optimized out>) at ../src/c11/impl/threads_posix.c:67
#8  0x00007f76b60a66d7 in start_thread (arg=<optimized out>) at pthread_create.c:447
#9  0x00007f76b612a60c in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:78

Thread 2 (Thread 0x7f76a8a006c0 (LWP 2050185)):
#0  0x00007f76b60a2da9 in __futex_abstimed_wait_common64 (private=0, futex_word=0x561bfb956048, expected=0, op=393, abstime=0x0, cancel=true) at futex-internal.c:57
#1  __futex_abstimed_wait_common (futex_word=futex_word@entry=0x561bfb956048, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0, cancel=cancel@entry=true) at futex-internal.c:87
#2  0x00007f76b60a2e2f in __GI___futex_abstimed_wait_cancelable64 (futex_word=futex_word@entry=0x561bfb956048, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=private@entry=0) at futex-internal.c:139
#3  0x00007f76b60a57f9 in __pthread_cond_wait_common (cond=0x561bfb956020, mutex=<optimized out>, clockid=0, abstime=0x0) at pthread_cond_wait.c:503
#4  ___pthread_cond_wait (cond=0x561bfb956020, mutex=<optimized out>) at pthread_cond_wait.c:618
#5  0x00007f76a9f57a9d in cnd_wait (cond=<optimized out>, mtx=<optimized out>) at ../src/c11/impl/threads_posix.c:135
#6  0x00007f76a9f3aa0b in util_queue_thread_func (input=input@entry=0x561bfb9569a0) at ../src/util/u_queue.c:290
#7  0x00007f76a9f579fc in impl_thrd_routine (p=<optimized out>) at ../src/c11/impl/threads_posix.c:67
#8  0x00007f76b60a66d7 in start_thread (arg=<optimized out>) at pthread_create.c:447
#9  0x00007f76b612a60c in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:78

Thread 1 (Thread 0x7f76b64b5740 (LWP 2050183)):
#0  __memset_avx2_unaligned_erms () at ../sysdeps/x86_64/multiarch/memset-vec-unaligned-erms.S:246
#1  0x00007f76a0838860 in memset (__dest=<optimized out>, __ch=0, __len=<optimized out>) at /usr/include/bits/string_fortified.h:59
#2  rocr::AMD::GpuAgent::AssembleShader (this=this@entry=0x561bfbb1c650, func_name=func_name@entry=0x7f76a08e8173 "TrapHandler", assemble_target=assemble_target@entry=rocr::AMD::GpuAgent::AssembleTarget::ISA, code_buf=@0x561bfbb1ca50: 0x0, code_buf_size=@0x561bfbb1ca58: 4096) at /usr/src/debug/rocm-runtime-6.2.0-2.fc40.x86_64/src/core/runtime/amd_gpu_agent.cpp:393
#3  0x00007f76a083a92b in rocr::AMD::GpuAgent::BindTrapHandler (this=0x561bfbb1c650) at /usr/src/debug/rocm-runtime-6.2.0-2.fc40.x86_64/src/core/runtime/amd_gpu_agent.cpp:2147
#4  rocr::AMD::GpuAgent::PostToolsInit (this=0x561bfbb1c650) at /usr/src/debug/rocm-runtime-6.2.0-2.fc40.x86_64/src/core/runtime/amd_gpu_agent.cpp:887
#5  0x00007f76a0851b9d in rocr::core::Runtime::Load (this=0x561bfbb160c0) at /usr/src/debug/rocm-runtime-6.2.0-2.fc40.x86_64/src/core/runtime/runtime.cpp:1915
#6  rocr::core::Runtime::Acquire () at /usr/src/debug/rocm-runtime-6.2.0-2.fc40.x86_64/src/core/runtime/runtime.cpp:139
#7  rocr::HSA::hsa_init () at /usr/src/debug/rocm-runtime-6.2.0-2.fc40.x86_64/src/core/runtime/hsa.cpp:206
#8  0x00007f76a99505d4 in amd::roc::Device::init () at /usr/src/debug/rocclr-6.2.0-1.fc40.x86_64/rocclr/device/rocm/rocdevice.cpp:479
#9  0x00007f76a99b2863 in amd::Device::init () at /usr/src/debug/rocclr-6.2.0-1.fc40.x86_64/rocclr/device/device.cpp:605
#10 amd::Runtime::init() [clone .isra.0] () at /usr/src/debug/rocclr-6.2.0-1.fc40.x86_64/rocclr/platform/runtime.cpp:76
#11 0x00007f76a991d14d in std::once_flag::_Prepare_execution::_Prepare_execution<std::call_once<clIcdGetPlatformIDsKHR::{lambda()#1}>(std::once_flag&, clIcdGetPlatformIDsKHR::{lambda()#1}&&)::{lambda()#1}>(clIcdGetPlatformIDsKHR::{lambda()#1}&)::{lambda()#1}::_FUN() () at /usr/src/debug/rocclr-6.2.0-1.fc40.x86_64/opencl/amdocl/cl_icd.cpp:224
#12 0x00007f76b60aba4b in __pthread_once_slow (once_control=0x7f76a99f63f0 <clIcdGetPlatformIDsKHR::initOnce>, init_routine=0x7f76b62e5f60 <std::__once_proxy()>) at pthread_once.c:116
#13 0x00007f76b60abab9 in ___pthread_once (once_control=<optimized out>, init_routine=<optimized out>) at pthread_once.c:143
#14 0x00007f76a991cfae in __gthread_once (__once=0x7f76a99f63f0 <clIcdGetPlatformIDsKHR::initOnce>, __func=<optimized out>) at /usr/include/c++/14/x86_64-redhat-linux/bits/gthr-default.h:713
#15 std::call_once<clIcdGetPlatformIDsKHR(cl_uint, _cl_platform_id**, cl_uint*)::<lambda()> > (__once=@0x7f76a99f63f0: {_M_once = 1}, __f=@0x7ffc8f3a341f: {<No data fields>}) at /usr/include/c++/14/mutex:916
#16 clIcdGetPlatformIDsKHR (num_entries=<optimized out>, platforms=0x0, num_platforms=0x7ffc8f3a34ac) at /usr/src/debug/rocclr-6.2.0-1.fc40.x86_64/opencl/amdocl/cl_icd.cpp:274
#17 0x00007f76b65d9465 in _find_and_check_platforms (num_icds=3) at /usr/src/debug/ocl-icd-2.3.2-6.fc40.x86_64/ocl_icd_loader.c:479
#18 __initClIcd () at /usr/src/debug/ocl-icd-2.3.2-6.fc40.x86_64/ocl_icd_loader.c:890
#19 _initClIcd_real () at /usr/src/debug/ocl-icd-2.3.2-6.fc40.x86_64/ocl_icd_loader.c:941
#20 0x00007f76b65db68c in _initClIcd () at /usr/src/debug/ocl-icd-2.3.2-6.fc40.x86_64/ocl_icd_loader.c:970
#21 clGetPlatformIDs (num_entries=0, platforms=0x0, num_platforms=0x7ffc8f3a35f4) at /usr/src/debug/ocl-icd-2.3.2-6.fc40.x86_64/ocl_icd_loader.c:1135
#22 0x0000561bdba113b0 in cl::Platform::get (platforms=platforms@entry=0x7ffc8f3a37b0) at /usr/src/debug/rocclr-6.2.0-1.fc40.x86_64/opencl/tools/clinfo/../../khronos/headers/opencl2.2/CL/cl2.hpp:2474
#23 0x0000561bdba085be in main (argc=<optimized out>, argv=<optimized out>) at /usr/src/debug/rocclr-6.2.0-1.fc40.x86_64/opencl/tools/clinfo/clinfo.cpp:75
```

---

## 评论 (24 条)

### 评论 #1 — jamesxu2 (2024-09-04T14:12:06Z)

Hi @Germano0 , unfortunately I don't think we can do much about this segmentation fault. The fedora package that I think you are using, rocm-clinfo, [has been deprecated for a year](https://src.fedoraproject.org/rpms/rocm-opencl), so even if we were able to create a fix, there's nowhere to push it to. 

---

### 评论 #2 — Germano0 (2024-09-04T14:36:05Z)

@jamesxu2 this ticket concerns the 6.2.0 rocm stack. The package you mentioned in the URL, is an obsolete package no longer used since it has been merged into [rocclr](https://src.fedoraproject.org/rpms/rocclr) package.
The (should) complete list of rocm packages is
https://src.fedoraproject.org/rpms/hsakmt
https://src.fedoraproject.org/rpms/rocm-compilersupport
https://src.fedoraproject.org/rpms/rocm-cmake
https://src.fedoraproject.org/rpms/rocm-smi
https://src.fedoraproject.org/rpms/rocm-runtime
https://src.fedoraproject.org/rpms/rocminfo
https://src.fedoraproject.org/rpms/rocclr

Since 6.2.0 is only available on Fedora > 40, I ported rocm 6.2.0 on Fedora 40 on my [personal repository](https://copr.fedorainfracloud.org/coprs/germano/rocclr/)

---

### 评论 #3 — Germano0 (2024-09-04T17:46:04Z)

In light of what I have written in my previous message, I request the reopening of the bug report

---

### 评论 #4 — jamesxu2 (2024-09-04T18:05:41Z)

Hi @Germano0 , I will look further into this issue. 

Based on your detailed backtrace (thanks for collecting that), I believe the crash is happening [around here](https://github.com/ROCm/ROCR-Runtime/blob/75143555fa068ac6afd2879b4398681c341a1215/runtime/hsa-runtime/core/runtime/amd_gpu_agent.cpp#L405-L413) in the ROCr Runtime component. I'll try to get a similar device and environment set up to reproduce your issue with clinfo (as a proxy for deprecated rocm-clinfo) and see what exactly is causing the crash. However, I can't guarantee that we can get clinfo to run on your configuration given that it's not officially supported.


---

### 评论 #5 — jamesxu2 (2024-09-06T18:39:14Z)

Hi @Germano0 , can you try running **clinfo** with environment variable AMD_LOG_LEVEL=4? I cannot repro your issue.

I do notice an invalid free() causing segfault on older ROCm, but not in ROCm 6.2, when you attempt to run with an invalid device. 

However, on ROCm 6.2 with RX460, I see this:
```
$ AMD_LOG_LEVEL=4 clinfo
:3:rocdevice.cpp            :469 : 8226031478d us:  Initializing HSA stack.
:3:rocdevice.cpp            :555 : 8226052090d us:  Enumerated GPU agents = 1
:1:rocdevice.cpp            :708 : 8226052119d us:  Unsupported HSA device gfx803 (PCI ID 67ef) for ISA amdgcn-amd-amdhsa--gfx803
:1:rocdevice.cpp            :565 : 8226052123d us:  Error creating new instance of Device.
:3:comgrctx.cpp             :126 : 8226052133d us:  Loaded COMGR library version 2.8.
:4:runtime.cpp              :85  : 8226052259d us:  init
Number of platforms:                             1
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP.dbg (3581.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback


  Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               0
```

Notice "Unsupported HSA device gfx803 (PCI ID 67ef) for ISA amdgcn-amd-amdhsa--gfx803" from the AMD LOG, which explicitly says that this device is not supported.

---

### 评论 #6 — Germano0 (2024-09-06T21:29:15Z)

```
# AMD_LOG_LEVEL=4 clinfo 
:3:rocdevice.cpp            :471 : 619068689471 us: [pid:3552352 tid:0x7f27dd29a740] Initializing HSA stack.
Errore di segmentazione (core dump creato)
```

do you need the GDB trace also of this crash?

---

### 评论 #7 — jamesxu2 (2024-09-09T19:51:41Z)

Hi @Germano0 , the GDB trace of the clinfo crash would also be helpful. It doesn't seem to get far, so there's a possibility it crashes before even encountering the GPU, but we could verify this from your backtrace.

Additionally, I'm not sure if you have tried running ```clinfo``` on a supported operating system (See: [ROCm Supported Operating Systems](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems)), but you may want to verify it there if that's convenient for you. That could help us rule out if it's a device or OS-related issue.

---

### 评论 #8 — Germano0 (2024-09-20T23:53:06Z)

[clinfo gdb.txt](https://github.com/user-attachments/files/17081693/clinfo.gdb.txt)
[clinfo strace.txt](https://github.com/user-attachments/files/17081694/clinfo.strace.txt)


>Additionally, I'm not sure if you have tried running clinfo on a supported operating system (See: [ROCm Supported Operating Systems](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems)), but you may want to verify it there if that's convenient for you. That could help us rule out if it's a device or OS-related issue.

No, I run it on Fedora 40 + [rocm 6.2.0 Copr repo](https://copr.fedorainfracloud.org/coprs/germano/rocclr/packages/) (created by me). And those packages work fine cause I am successfully running `clinfo` on a second computer and it works (Thinkpad X13 Gen3 AMD).
At the moment I cannot install RHEL9 to test it there

---

### 评论 #9 — Germano0 (2024-09-24T09:14:41Z)

I apologize, in my previous [message](https://github.com/ROCm/ROCm/issues/3664#issuecomment-2364760791) I pasted the output of [clinfo](https://github.com/Oblomov/clinfo) instead of rocm-clinfo

Here the correct gdb and strace
[rocm-clinfo_gdb.txt](https://github.com/user-attachments/files/17111645/rocm-clinfo_gdb.txt)
[rocm-clinfo_strace.txt](https://github.com/user-attachments/files/17111646/rocm-clinfo_strace.txt)


---

### 评论 #10 — jamesxu2 (2024-09-24T13:27:38Z)

@Germano0 , thanks, this looks fine. I can more easily reproduce this issue on clinfo and the backtraces look similar. 

Also, this issue does not appear to be OS-dependent, as I've noticed another issue with similar symptoms pop up on the CLR issue board and they're using a GFX8 card + Ubuntu. https://github.com/ROCm/clr/issues/93


---

### 评论 #11 — jamesxu2 (2024-09-26T19:52:56Z)

Hi @Germano0 , another question about your setup - 

How are you getting your clr repository? Note that https://github.com/ROCm/ROCclr is also deprecated and moved to [ROCm/clr](https://github.com/ROCm/clr/tree/amd-staging/opencl) 

```
#8  0x00007f76a99505d4 in amd::roc::Device::init () at /usr/src/debug/rocclr-6.2.0-1.fc40.x86_64/rocclr/device/rocm/rocdevice.cpp:479
```

I was doing some testing using the **rocm-6.2.x** branch and 6.2.x release of ROCm and I see that there is an free(): invalid pointer due to delete[] of an uninitialized array (p2p_agents_list_) when running clinfo. However, this is a [fix](https://github.com/ROCm/clr/commit/7448113cfc6193918118d5e5d4beefaf3d5f1b1e) for this that was merged into amd-staging but not yet released. This fix would be in the libamdocl64.so library generated from compiling the [OCL part of ROCm/clr](https://github.com/ROCm/clr/tree/amd-staging/opencl#building)

This crash is not the same as the one you observe, but I think the reason I'm unable to reproduce your issue might be the repository source. 

Is it possible for you to build from the most recent version of clr and rerun clinfo? 








---

### 评论 #12 — Germano0 (2024-09-26T22:54:51Z)

> How are you getting your clr repository?

The sources are from Fedora repository for Fedora 41, and among Fedora Rocm packagers there is your AMD colleague Tom Rix. I am now re-creating my Copr repo (for Fedora 40) from the scratch and in an improved way, so I can avoid as much as possible any possible fault on my side.
Moreover I recently upgraded to 6.2.1 and the problem still remains, but this time I tried also to run Valgrind, and for some reason, when `rocm-clrinfo` is run within Valgrind, it does not do segmentation fault

```
# valgrind rocm-clinfo --leak-check=full -s
==2931245== Memcheck, a memory error detector
==2931245== Copyright (C) 2002-2024, and GNU GPL'd, by Julian Seward et al.
==2931245== Using Valgrind-3.23.0 and LibVEX; rerun with -h for copyright info
==2931245== Command: rocm-clinfo --leak-check=full -s
==2931245== 
==2931245== Warning: set address range perms: large range [0x59cb6000, 0x859c96000) (noaccess)
Number of platforms:                             3
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 1.1 Mesa 24.1.7
  Platform Name:                                 Clover
  Platform Vendor:                               Mesa
  Platform Extensions:                           cl_khr_icd
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 3.0 
  Platform Name:                                 rusticl
  Platform Vendor:                               Mesa/X.org
  Platform Extensions:                           cl_khr_byte_addressable_store cl_khr_create_command_queue cl_khr_expect_assume cl_khr_extended_versioning cl_khr_icd cl_khr_il_program cl_khr_spirv_no_integer_wrap_decoration cl_khr_suggested_local_work_size
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3625.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback 


  Platform Name:                                 Clover
Number of devices:                               1
  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Max compute units:                             36
  Max work items dimensions:                     3
    Max work items[0]:                           256
    Max work items[1]:                           256
    Max work items[2]:                           256
  Max work group size:                           256
  Preferred vector width char:                   16
  Preferred vector width short:                  8
  Preferred vector width int:                    4
  Preferred vector width long:                   2
  Preferred vector width float:                  4
  Preferred vector width double:                 2
  Native vector width char:                      16
  Native vector width short:                     8
  Native vector width int:                       4
  Native vector width long:                      2
  Native vector width float:                     4
  Native vector width double:                    2
  Max clock frequency:                           1288Mhz
  Address bits:                                  64
  Max memory allocation:                         2147483648
  Image support:                                 No
  Max size of kernel argument:                   1024
  Alignment (bits) of base address:              32768
  Minimum alignment (bytes) for any datatype:    128
  Single precision floating point capability
    Denorms:                                     No
    Quiet NaNs:                                  Yes
    Round to nearest even:                       Yes
    Round to zero:                               No
    Round to +ve and infinity:                   No
    IEEE754-2008 fused multiply-add:             No
  Cache type:                                    None
  Cache line size:                               0
  Cache size:                                    0
  Global memory size:                            8589934592
  Constant buffer size:                          67108864
  Max number of constant args:                   16
  Local memory type:                             Local
  Local memory size:                             65536
ERROR: clBuildProgram(-11)
==2931245== 
==2931245== HEAP SUMMARY:
==2931245==     in use at exit: 746,549 bytes in 3,099 blocks
==2931245==   total heap usage: 77,250 allocs, 74,151 frees, 17,126,561 bytes allocated
==2931245== 
==2931245== LEAK SUMMARY:
==2931245==    definitely lost: 0 bytes in 0 blocks
==2931245==    indirectly lost: 0 bytes in 0 blocks
==2931245==      possibly lost: 4,080 bytes in 12 blocks
==2931245==    still reachable: 742,413 bytes in 3,085 blocks
==2931245==         suppressed: 56 bytes in 2 blocks
==2931245== Rerun with --leak-check=full to see details of leaked memory
==2931245== 
==2931245== For lists of detected and suppressed errors, rerun with: -s
==2931245== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

Tomorrow I will apply the patch you mentioned in your last message and I will provide a feedback

---

### 评论 #13 — jamesxu2 (2024-09-27T13:24:14Z)

Hi @Germano0 ,  a few things:
1. The output of your clinfo is odd - there should be a check in rocdevice.cpp that would block your GFX8 device from being enumerated. This makes me think there is still some deviation between the code running on your machine and the latest public sources.

[GFX8 Check](https://github.com/ROCm/clr/blob/07c9c7fe56858e7272cb6c8c9cd053cd049ed3c2/rocclr/device/rocm/rocdevice.cpp#L701-L706)


2. I also observed that running clinfo with valgrind (or with a build using sanitized addresses both of which slow down execution) would avert a crash, suggesting some sort of race condition. However, this crash was fixed in the patch I mentioned in my previous comment, and is probably different than what you're experiencing.

3. The bug I observed from my previous comment is not patched yet in ROCm 6.2.1 or any current ROCm release, it's only available in the amd-staging branch of ROCm/clr
4.  I'll reach out to our internal team to see if they have any insight on this ticket.

Thanks for your patience!

---

### 评论 #14 — Germano0 (2024-09-27T17:09:52Z)

> Thanks for your patience!

No worries, consider me always available to test patches

I tried to apply [your patch](https://github.com/ROCm/clr/commit/7448113cfc6193918118d5e5d4beefaf3d5f1b1e#diff-96787a2d61857359a61d0915ded962b719e2db4d4e8fcd2c64f42cab2021bc20L60) (for details see [here](https://download.copr.fedorainfracloud.org/results/germano/rocclr/fedora-40-x86_64/08085542-rocclr/) `7448113.patch` file inside SRPM [rocclr-6.2.1-2.fc40.src.rpm](https://download.copr.fedorainfracloud.org/results/germano/rocclr/fedora-40-x86_64/08085542-rocclr/rocclr-6.2.1-2.fc40.src.rpm) ) but I still get segmentation fault

[rocm-clinfo_gdb_2024-09-27.txt](https://github.com/user-attachments/files/17167354/rocm-clinfo_gdb_2024-09-27.txt)
[rocm-clinfo_strace_2024-09-27.txt](https://github.com/user-attachments/files/17167355/rocm-clinfo_strace_2024-09-27.txt)



> 1. The output of your clinfo is odd - there should be a check in rocdevice.cpp that would block your GFX8 device from being enumerated. This makes me think there is still some deviation between the code running on your machine and the latest public sources.

With `latest public sources` do you mean stuff in master branch (or amd-staging branch of ROCm/clr) or latest stable (6.2.1) release?

Thank you for your support

---

### 评论 #15 — jamesxu2 (2024-09-27T20:32:01Z)

Hi @Germano0 , by latest public sources I mean either the changes in the Github master **or** stable branch. The reason I think it shouldn't work is because the change to disable GFX8 support was added years ago to the Github ROCm/clr repo. That results in my testing printing this line:
```
:1:rocdevice.cpp            :708 : 8226052119d us:  Unsupported HSA device gfx803 (PCI ID 67ef) for ISA amdgcn-amd-amdhsa--gfx803
```

So, if you were remotely up to date, then you would have [this branch](https://github.com/ROCm/clr/pull/97/commits/909fa3dcb644f7ca422ed1a980a54ac426d831b1) which would prevent your device from being enumerated.

However, someone flagged this branch as a bug and reported it here: https://bugzilla.redhat.com/show_bug.cgi?id=2277002 and it apparently was patched very recently (I think, literally today in f40?). However, this patch does not exist yet in the public source for Github/clr. Also, the reporter of this bug appears to be running a similar working configuration to yours with a gfx8 device.

To summarize, there appears to be at least 3 mysteries/issues here:
1. invalid free() in everything but ROCm/clr amd-staging. This only causes a crash if the next issue (2) is enabled
2. discrepancy between what code sources include [this branch](https://github.com/ROCm/clr/pull/97/commits/909fa3dcb644f7ca422ed1a980a54ac426d831b1) causing gfx8 to be explicitly disabled. In my understanding, there is a period of time from gfx8 release to a few years ago where gfx8 is supported, then a period of time when gfx8 is broken, and finally a third period of time very recently where gfx8 is fixed again. I don't know where you are in this timeline as it seems that gfx8 is supported for you.
3. Whatever the root cause of your segfault is, which I still have not been able to reproduce.

I think if I still cannot get find answers, I will try to sync up to your exact system configuration and debug it there as this bug is turning out to be pretty elusive. 

---

### 评论 #16 — jamesxu2 (2024-10-03T14:47:00Z)

Hi @Germano0 , I have some more findings:

I attempt to run rocm-clinfo on a clean install of Fedora 40, after installing rocm-clinfo and rocm-opencl packages both from both:

- Fedora sources (6.1.2-1.fc40 rocm-opencl, 6.1.2-1.fc40 rocm-clinfo) 
- your COPR repository (rocm-opencl 6.2.1-2.fc40 from copr:copr.fedorainfracloud.org:germano:rocclr, rocm-clinfo 6.2.1-2.fc40 from the same COPR repo).

The result is the same, which is that the [gfx8-disabled branch](https://github.com/ROCm/clr/pull/97/commits/909fa3dcb644f7ca422ed1a980a54ac426d831b1) is entered giving me:
```
$ AMD_LOG_LEVEL=4 rocm-clinfo
:3:rocdevice.cpp            :471 : 0460287439 us: [pid:2626  tid:0x7f26c7b17740] Initializing HSA stack.
:3:rocdevice.cpp            :557 : 0460292762 us: [pid:2626  tid:0x7f26c7b17740] Enumerated GPU agents = 1
:1:rocdevice.cpp            :710 : 0460292793 us: [pid:2626  tid:0x7f26c7b17740] Unsupported HSA device gfx803 (PCI ID 67df) for ISA amdgcn-amd-amdhsa--gfx803
:1:rocdevice.cpp            :567 : 0460292796 us: [pid:2626  tid:0x7f26c7b17740] Error creating new instance of Device.
:3:rocsettings.cpp          :290 : 0460292801 us: [pid:2626  tid:0x7f26c7b17740] Using dev kernel arg wa = 0
:3:comgrctx.cpp             :33  : 0460292804 us: [pid:2626  tid:0x7f26c7b17740] Loading COMGR library.
:3:comgrctx.cpp             :126 : 0460292828 us: [pid:2626  tid:0x7f26c7b17740] Loaded COMGR library version 2.8.
[...extra logs...]
Number of platforms:                             1
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3625.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback


  Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               0

```

Is this what you expect to see? There is no segfault. Is this installation process correct? 

---

### 评论 #17 — Germano0 (2024-10-04T10:18:43Z)

> 2\. discrepancy between what code sources include [this branch](https://github.com/ROCm/clr/pull/97/commits/909fa3dcb644f7ca422ed1a980a54ac426d831b1) causing gfx8 to be explicitly disabled. In my understanding, there is a period of time from gfx8 release to a few years ago where gfx8 is supported, then a period of time when gfx8 is broken, and finally a third period of time very recently where gfx8 is fixed again. I don't know where you are in this timeline as it seems that gfx8 is supported for you.

That's a good point, but I am confused too about it. Do we have somewhere a table that maps the `gfx` nomenclature to the architecture codename? It's hard to remember all of them by heart

> Is this what you expect to see? There is no segfault. Is this installation process correct?

Can you please show the output of command `dnf list --installed | grep roc`

I tried with two new builds which both include the `rocclr/device/device.hpp` [commit](https://github.com/ROCm/clr/pull/97/commits/909fa3dcb644f7ca422ed1a980a54ac426d831b1) you mentioned
1) 6.2.1-3 still includes also [this patch](https://github.com/ROCm/clr/commit/7448113cfc6193918118d5e5d4beefaf3d5f1b1e#diff-96787a2d61857359a61d0915ded962b719e2db4d4e8fcd2c64f42cab2021bc20L60)
it still crashed, here the [GDB log](https://github.com/user-attachments/files/17256572/rocm-clinfo_gdb_2024-10-04-6.2.1-3.txt)

2) 6.2.1-4 does not include [this patch](https://github.com/ROCm/clr/commit/7448113cfc6193918118d5e5d4beefaf3d5f1b1e#diff-96787a2d61857359a61d0915ded962b719e2db4d4e8fcd2c64f42cab2021bc20L60)
it still crashed, here the [GDB log](https://github.com/user-attachments/files/17256712/rocm-clinfo_gdb_2024-10-04-6.2.1-4.txt)

Look at this weird thing. During past days I was forced to use darktable with `rusticl` OpenCL, by adding the env variable `RUSTICL_ENABLE=radeonsi`.
If I use the same variable on `rocl-clinfo`, I get the following output
```
# RUSTICL_ENABLE=radeonsi rocm-clinfo
Number of platforms:                             3
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 1.1 Mesa 24.1.7
  Platform Name:                                 Clover
  Platform Vendor:                               Mesa
  Platform Extensions:                           cl_khr_icd
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 3.0 
  Platform Name:                                 rusticl
  Platform Vendor:                               Mesa/X.org
  Platform Extensions:                           cl_khr_byte_addressable_store cl_khr_create_command_queue cl_khr_expect_assume cl_khr_extended_versioning cl_khr_icd cl_khr_il_program cl_khr_spirv_no_integer_wrap_decoration cl_khr_suggested_local_work_size
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3625.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback 


  Platform Name:                                 Clover
Number of devices:                               1
  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Max compute units:                             36
  Max work items dimensions:                     3
    Max work items[0]:                           256
    Max work items[1]:                           256
    Max work items[2]:                           256
  Max work group size:                           256
  Preferred vector width char:                   16
  Preferred vector width short:                  8
  Preferred vector width int:                    4
  Preferred vector width long:                   2
  Preferred vector width float:                  4
  Preferred vector width double:                 2
  Native vector width char:                      16
  Native vector width short:                     8
  Native vector width int:                       4
  Native vector width long:                      2
  Native vector width float:                     4
  Native vector width double:                    2
  Max clock frequency:                           1288Mhz
  Address bits:                                  64
  Max memory allocation:                         2147483648
  Image support:                                 No
  Max size of kernel argument:                   1024
  Alignment (bits) of base address:              32768
  Minimum alignment (bytes) for any datatype:    128
  Single precision floating point capability
    Denorms:                                     No
    Quiet NaNs:                                  Yes
    Round to nearest even:                       Yes
    Round to zero:                               No
    Round to +ve and infinity:                   No
    IEEE754-2008 fused multiply-add:             No
  Cache type:                                    None
  Cache line size:                               0
  Cache size:                                    0
  Global memory size:                            8589934592
  Constant buffer size:                          67108864
  Max number of constant args:                   16
  Local memory type:                             Local
  Local memory size:                             65536
ERROR: clBuildProgram(-11)
```

This is the list of rocm packages I have on my system
```
root@Magic-5:/dev# dnf5 list --installed | rg roc
hipcc.x86_64                                         18-7.rocm6.2.1.fc40                     copr:copr.fedorainfracloud.org:germano:rocclr
hsakmt.x86_64                                        1.0.6-44.rocm6.2.1.fc40                 copr:copr.fedorainfracloud.org:germano:rocclr
hsakmt-debuginfo.x86_64                              1.0.6-44.rocm6.2.1.fc40                 copr:copr.fedorainfracloud.org:germano:rocclr
hsakmt-debugsource.x86_64                            1.0.6-44.rocm6.2.1.fc40                 copr:copr.fedorainfracloud.org:germano:rocclr
hsakmt-devel.x86_64                                  1.0.6-44.rocm6.2.1.fc40                 copr:copr.fedorainfracloud.org:germano:rocclr
microcode_ctl.x86_64                                 2:2.1-61.3.fc40                         updates
opencv-imgproc.x86_64                                4.9.0-3.fc40                            <unknown>
procps-ng.x86_64                                     4.0.4-3.fc40                            <unknown>
python3-ptyprocess.noarch                            0.7.0-7.fc40                            <unknown>
python3-zeroconf.x86_64                              0.118.0-5.fc40                          <unknown>
rocclr-debuginfo.x86_64                              6.2.1-4.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocclr-debugsource.x86_64                            6.2.1-4.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-clinfo.x86_64                                   6.2.1-4.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-clinfo-debuginfo.x86_64                         6.2.1-4.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-cmake.noarch                                    6.2.0-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-comgr.x86_64                                    18-7.rocm6.2.1.fc40                     copr:copr.fedorainfracloud.org:germano:rocclr
rocm-comgr-debuginfo.x86_64                          18-7.rocm6.2.1.fc40                     copr:copr.fedorainfracloud.org:germano:rocclr
rocm-comgr-devel.x86_64                              18-7.rocm6.2.1.fc40                     copr:copr.fedorainfracloud.org:germano:rocclr
rocm-compilersupport-debuginfo.x86_64                18-2.rocm6.2.0.fc40                     copr:copr.fedorainfracloud.org:germano:rocclr
rocm-compilersupport-debugsource.x86_64              18-7.rocm6.2.1.fc40                     copr:copr.fedorainfracloud.org:germano:rocclr
rocm-compilersupport-macros.x86_64                   18-7.rocm6.2.1.fc40                     copr:copr.fedorainfracloud.org:germano:rocclr
rocm-core.x86_64                                     6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-core-debuginfo.x86_64                           6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-core-debugsource.x86_64                         6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-core-devel.x86_64                               6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-device-libs.x86_64                              18-7.rocm6.2.1.fc40                     copr:copr.fedorainfracloud.org:germano:rocclr
rocm-hip.x86_64                                      6.2.1-4.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-hip-debuginfo.x86_64                            6.2.1-4.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-hip-devel.x86_64                                6.2.1-4.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-opencl.x86_64                                   6.2.1-4.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-opencl-debuginfo.x86_64                         6.2.1-4.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-opencl-devel.x86_64                             6.2.1-4.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-rpm-macros.x86_64                               6.2-3.fc40                              copr:copr.fedorainfracloud.org:germano:rocclr
rocm-rpm-macros-modules.x86_64                       6.2-3.fc40                              copr:copr.fedorainfracloud.org:germano:rocclr
rocm-runtime.x86_64                                  6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-runtime-debuginfo.x86_64                        6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-runtime-debugsource.x86_64                      6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-runtime-devel.x86_64                            6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-smi.x86_64                                      6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-smi-debuginfo.x86_64                            6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-smi-debugsource.x86_64                          6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocm-smi-devel.x86_64                                6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocminfo.x86_64                                      6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocminfo-debuginfo.x86_64                            6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
rocminfo-debugsource.x86_64                          6.2.1-1.fc40                            copr:copr.fedorainfracloud.org:germano:rocclr
```



---

### 评论 #18 — jamesxu2 (2024-10-04T15:17:50Z)

>  Do we have somewhere a table that maps the gfx nomenclature to the architecture codename? 

LLVM  has one: https://llvm.org/docs/AMDGPUUsage.html#processors

> Can you please show the output of command dnf list --installed | grep roc

```
$ dnf list --installed | grep roc
hsakmt.x86_64                                        1.0.6-44.rocm6.2.1.fc40             @copr:copr.fedorainfracloud.org:germano:rocclr
rocm-clinfo.x86_64                                   6.2.1-4.fc40                        @copr:copr.fedorainfracloud.org:germano:rocclr
rocm-comgr.x86_64                                    18-7.rocm6.2.1.fc40                 @copr:copr.fedorainfracloud.org:germano:rocclr
rocm-opencl.x86_64                                   6.2.1-4.fc40                        @copr:copr.fedorainfracloud.org:germano:rocclr
rocm-runtime.x86_64                                  6.2.1-1.fc40                        @copr:copr.fedorainfracloud.org:germano:rocclr
```

Upon closer inspection, I notice you have 3 OpenCL platforms (drivers) installed, which means we're getting a bit into the weeds with OpenCL mechanics - I think the driver that's providing the clinfo output might not even be ROCm; and is actually Clover. I'm not sure how this got installed in your system.

I only see "Platform Name: AMD Accelerated Parallel Processing". 

If possible, you should try to remove the other two OpenCL platforms from your system. I'm not sure exactly what the interactions are between those external clover/rusticl platforms and our rocm-opencl driver but I think it may be causing this divergent behaviour, and is why you're not seeing that gfx8-disable branch.

Finally, just to make sure this isn't an issue with your backport, could you try running rocm-clinfo with the ROCm 6.1.2 fedora package after removing those OpenCL platforms?




---

### 评论 #19 — Germano0 (2024-10-05T11:51:37Z)

I have some good news, by not changing anything on my computer since my last message (so still with rocm 6.2.1-4 build) and just removing package `mesa-libOpenCL`, the problem has been solved
```
# dnf info mesa-libOpenCL
Name         : mesa-libOpenCL
Version      : 24.1.7
Rilascio     : 1.fc40
Architecture : x86_64
Size         : 8.0 M
Sorgente     : mesa-24.1.7-1.fc40.src.rpm
Repository   : updates
Summary      : Mesa OpenCL runtime library
URL          : http://www.mesa3d.org
Licenza      : MIT AND BSD-3-Clause AND SGI-B-2.0
Description  : Mesa OpenCL runtime library.

# rpm -ql mesa-libOpenCL.x86_64
/etc/OpenCL/vendors/mesa.icd
/etc/OpenCL/vendors/rusticl.icd
/usr/lib/.build-id
/usr/lib/.build-id/cc
/usr/lib/.build-id/cc/4873280bd26c80ef540e616002034e0c461bb5
/usr/lib/.build-id/f0
/usr/lib/.build-id/f0/25f235169b397160bb2c9e6ab5735f5c592ac8
/usr/lib64/libMesaOpenCL.so.1
/usr/lib64/libMesaOpenCL.so.1.0.0
/usr/lib64/libRusticlOpenCL.so.1
/usr/lib64/libRusticlOpenCL.so.1.0.0
```

```
# rocm-clinfo
Number of platforms:                             1
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3625.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback 


  Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               1
  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Board name:                                    AMD Radeon RX 480 Graphics
  Device Topology:                               PCI[ B#9, D#0, F#0 ]
  Max compute units:                             36
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
  Max clock frequency:                           1288Mhz
  Address bits:                                  64
  Max memory allocation:                         7301444400
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
    Denorms:                                     No
    Quiet NaNs:                                  Yes
    Round to nearest even:                       Yes
    Round to zero:                               Yes
    Round to +ve and infinity:                   Yes
    IEEE754-2008 fused multiply-add:             Yes
  Cache type:                                    Read/Write
  Cache line size:                               64
  Cache size:                                    16384
  Global memory size:                            8589934592
  Constant buffer size:                          7301444400
  Max number of constant args:                   8
  Local memory type:                             Local
  Local memory size:                             65536
  Max pipe arguments:                            16
  Max pipe active reservations:                  16
  Max pipe packet size:                          3006477104
  Max global variable size:                      7301444400
  Max global variable preferred total size:      8589934592
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
  Kernel Preferred work group size multiple:     64
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
  Platform ID:                                   0x7fbbd311c7e8
  Name:                                          gfx803
  Vendor:                                        Advanced Micro Devices, Inc.
  Device OpenCL C version:                       OpenCL C 2.0 
  Driver version:                                3625.0 (HSA1.1,LC)
  Profile:                                       FULL_PROFILE
  Version:                                       OpenCL 1.2 
  Extensions:                                    cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_depth_images cl_amd_copy_buffer_p2p cl_amd_assembly_program 
```

```
$ darktable-cltest
darktable 4.8.1
Copyright (C) 2012-2024 Johannes Hanika and other contributors.

Compile options:
  Bit depth              -> 64 bit
  Debug                  -> DISABLED
  SSE2 optimizations     -> ENABLED
  OpenMP                 -> ENABLED
  OpenCL                 -> ENABLED
  Lua                    -> ENABLED  - API version 9.3.0
  Colord                 -> ENABLED
  gPhoto2                -> ENABLED
  GMIC                   -> ENABLED  - Compressed LUTs are supported
  GraphicsMagick         -> ENABLED
  ImageMagick            -> DISABLED
  libavif                -> ENABLED
  libheif                -> ENABLED
  libjxl                 -> ENABLED
  OpenJPEG               -> ENABLED
  OpenEXR                -> ENABLED
  WebP                   -> ENABLED

See https://www.darktable.org/resources/ for detailed documentation.
See https://github.com/darktable-org/darktable/issues/new/choose to report bugs.

     0.0235 [dt_get_sysresource_level] switched to 2 as `large'
     0.0235   total mem:       128726MB
     0.0235   mipmap cache:    16090MB
     0.0235   available mem:   87996MB
     0.0235   singlebuff:      2011MB
     0.0367 [opencl_init] opencl library 'libOpenCL' found on your system and loaded, preference 'default path'
     0.1006 [opencl_init] found 1 platform
[opencl_init] found 1 device

[dt_opencl_device_init]
   DEVICE:                   0: 'gfx803'
   CONF KEY:                 cldevice_v5_amdacceleratedparallelprocessinggfx803
   PLATFORM, VENDOR & ID:    AMD Accelerated Parallel Processing, Advanced Micro Devices, Inc., ID=4098
   CANONICAL NAME:           amdacceleratedparallelprocessinggfx803
   DRIVER VERSION:           3625.0 (HSA1.1,LC)
   DEVICE VERSION:           OpenCL 1.2 
   DEVICE_TYPE:              GPU, dedicated mem
   GLOBAL MEM SIZE:          8192 MB
   MAX MEM ALLOC:            6963 MB
   MAX IMAGE SIZE:           16384 x 16384
   MAX WORK GROUP SIZE:      256
   MAX WORK ITEM DIMENSIONS: 3
   MAX WORK ITEM SIZES:      [ 1024 1024 1024 ]
   ASYNC PIXELPIPE:          NO
   PINNED MEMORY TRANSFER:   NO
   AVOID ATOMICS:            NO
   MICRO NAP:                250
   ROUNDUP WIDTH & HEIGHT    16x16
   CHECK EVENT HANDLES:      128
   TILING ADVANTAGE:         0.000
   DEFAULT DEVICE:           NO
   KERNEL BUILD DIRECTORY:   /usr/share/darktable/kernels
   KERNEL DIRECTORY:         /home/user/.cache/darktable/cached_v3_kernels_for_AMDAcceleratedParallelProcessinggfx803_36250HSA11LC
   CL COMPILER OPTION:       -cl-fast-relaxed-math
   CL COMPILER COMMAND:      -w -cl-fast-relaxed-math  -DAMD=1 -I"/usr/share/darktable/kernels"
   KERNEL LOADING TIME:       0.0180 sec
[opencl_init] OpenCL successfully initialized. internal numbers and names of available devices:
[opencl_init]           0       'AMD Accelerated Parallel Processing gfx803'
     0.4072 [opencl_init] FINALLY: opencl PREFERENCE=ON is AVAILABLE and ENABLED.
[opencl_init] opencl_scheduling_profile: 'default'
[opencl_init] opencl_device_priority: '*/!0,*/*/*/!0,*'
[opencl_init] opencl_mandatory_timeout: 200
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       -1      0       0       -1
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       0       0       0       0
[opencl_synchronization_timeout] synchronization timeout set to 200
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       -1      0       0       -1
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       0       0       0       0
[opencl_synchronization_timeout] synchronization timeout set to 200
```

I think I have to open a bugreport in Fedora to let rocm package maintainers be aware of such conflict between ` mesa-libOpenCL` and `rocm-opencl`.
I believe Fedora is a good test bench for AMD software stack because Fedora is the upstream of Red Hat Enterprise Linux (which is the officially supported distribution by AMD).

To doublecheck I also tested the old rocm 6.1.x which should be disabled on `gfx803` and indeed it did not work

```
# dnf remove rocm*
# dnf copr disable germano/rocclr
# dnf5 install rocm*

# rocm-clinfo
Number of platforms:                             1
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3614.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback 
  Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               0

$ darktable-cltest
darktable 4.8.1
Copyright (C) 2012-2024 Johannes Hanika and other contributors.

Compile options:
  Bit depth              -> 64 bit
  Debug                  -> DISABLED
  SSE2 optimizations     -> ENABLED
  OpenMP                 -> ENABLED
  OpenCL                 -> ENABLED
  Lua                    -> ENABLED  - API version 9.3.0
  Colord                 -> ENABLED
  gPhoto2                -> ENABLED
  GMIC                   -> ENABLED  - Compressed LUTs are supported
  GraphicsMagick         -> ENABLED
  ImageMagick            -> DISABLED
  libavif                -> ENABLED
  libheif                -> ENABLED
  libjxl                 -> ENABLED
  OpenJPEG               -> ENABLED
  OpenEXR                -> ENABLED
  WebP                   -> ENABLED

See https://www.darktable.org/resources/ for detailed documentation.
See https://github.com/darktable-org/darktable/issues/new/choose to report bugs.

     0.0250 [dt_get_sysresource_level] switched to 2 as `large'
     0.0250   total mem:       128726MB
     0.0250   mipmap cache:    16090MB
     0.0250   available mem:   87996MB
     0.0250   singlebuff:      2011MB
     0.0396 [opencl_init] opencl disabled via darktable preferences
     0.0397 [opencl_init] opencl library 'libOpenCL' found on your system and loaded, preference 'default path'
     0.1003 [opencl_init] found 1 platform
     0.1004 [opencl_init] no devices found for Advanced Micro Devices, Inc. (vendor) - AMD Accelerated Parallel Processing (name)
[opencl_init] found 0 device
     0.1004 [opencl_init] FINALLY: opencl PREFERENCE=OFF is NOT AVAILABLE and NOT ENABLED.
```

> I think it may be causing this divergent behaviour, and is why you're not seeing that gfx8-disable branch.

Since we are discussing `gfx803` rocm support, I would like to ask some clarifications. The topic is a bit non trivial for people non expert of AMD software stack. 
The commit [Fix gfx8 opencl](https://github.com/ROCm/clr/pull/97/commits/909fa3dcb644f7ca422ed1a980a54ac426d831b1) re-enables gfx8 OpenCL on rocm. Its commit message says:
```
This condition was added when we supported PAL openCL on gfx8, but when
ROC_ENABLE_PRE_VEGA was dropped and PAL OpenCL on Linux was deprecated,
this logic should have been dropped completely.
```

May I ask you what was PAL openCL? I have done some search on the web about PAL OpenCL but I just found [this discussion](https://github.com/ROCm/ROCm/issues/1660)

Thank you for your support

---

### 评论 #20 — Germano0 (2024-10-07T00:40:08Z)

An update about the `mesa-libOpenCL` and `rocm-opencl` packages conflict. I own also a Thinkpad X13 Gen 3 with a Radeon 680M (gfx1035) and on such system, if both packages are installed, `rocm-clinfo` does not segfault. Hereby I show the output of `rocm-clinfo` and `darktable-cltest` when both packages are installed and then, without `mesa-libOpenCL`

**Output with both `mesa-libOpenCL` and `rocm-opencl` packages installed**
```
$ rocm-clinfo 
Number of platforms:                             3
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 1.1 Mesa 24.1.7
  Platform Name:                                 Clover
  Platform Vendor:                               Mesa
  Platform Extensions:                           cl_khr_icd
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3625.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback 
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 3.0 
  Platform Name:                                 rusticl
  Platform Vendor:                               Mesa/X.org
  Platform Extensions:                           cl_khr_byte_addressable_store cl_khr_create_command_queue cl_khr_expect_assume cl_khr_extended_versioning cl_khr_icd cl_khr_il_program cl_khr_spirv_no_integer_wrap_decoration cl_khr_suggested_local_work_size


  Platform Name:                                 Clover
Number of devices:                               1
  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Max compute units:                             12
  Max work items dimensions:                     3
    Max work items[0]:                           256
    Max work items[1]:                           256
    Max work items[2]:                           256
  Max work group size:                           256
  Preferred vector width char:                   16
  Preferred vector width short:                  8
  Preferred vector width int:                    4
  Preferred vector width long:                   2
  Preferred vector width float:                  4
  Preferred vector width double:                 2
  Native vector width char:                      16
  Native vector width short:                     8
  Native vector width int:                       4
  Native vector width long:                      2
  Native vector width float:                     4
  Native vector width double:                    2
  Max clock frequency:                           2200Mhz
  Address bits:                                  64
  Max memory allocation:                         4042498048
  Image support:                                 No
  Max size of kernel argument:                   1024
  Alignment (bits) of base address:              32768
  Minimum alignment (bytes) for any datatype:    128
  Single precision floating point capability
    Denorms:                                     No
    Quiet NaNs:                                  Yes
    Round to nearest even:                       Yes
    Round to zero:                               No
    Round to +ve and infinity:                   No
    IEEE754-2008 fused multiply-add:             No
  Cache type:                                    None
  Cache line size:                               0
  Cache size:                                    0
  Global memory size:                            16169992192
  Constant buffer size:                          67108864
  Max number of constant args:                   16
  Local memory type:                             Local
  Local memory size:                             65536
ERROR: clBuildProgram(-11)


user@X13:~$ darktable-cltest 
darktable 4.8.1
Copyright (C) 2012-2024 Johannes Hanika and other contributors.

Compile options:
  Bit depth              -> 64 bit
  Debug                  -> DISABLED
  SSE2 optimizations     -> ENABLED
  OpenMP                 -> ENABLED
  OpenCL                 -> ENABLED
  Lua                    -> ENABLED  - API version 9.3.0
  Colord                 -> ENABLED
  gPhoto2                -> ENABLED
  GMIC                   -> ENABLED  - Compressed LUTs are supported
  GraphicsMagick         -> ENABLED
  ImageMagick            -> DISABLED
  libavif                -> ENABLED
  libheif                -> ENABLED
  libjxl                 -> ENABLED
  OpenJPEG               -> ENABLED
  OpenEXR                -> ENABLED
  WebP                   -> ENABLED

See https://www.darktable.org/resources/ for detailed documentation.
See https://github.com/darktable-org/darktable/issues/new/choose to report bugs.

     0.0439 [dt_get_sysresource_level] switched to 1 as `default'
     0.0440   total mem:       30841MB
     0.0440   mipmap cache:    3855MB
     0.0440   available mem:   15420MB
     0.0440   singlebuff:      240MB
     0.0723 [opencl_init] opencl library 'libOpenCL' found on your system and loaded, preference 'default path'
     0.2148 [opencl_init] found 3 platforms
     0.2149 [check platform] platform 'Clover' with key 'clplatform_clover' is NOT active
     0.2149 [check platform] platform 'rusticl' with key 'clplatform_rusticl' is NOT active
[opencl_init] found 1 device

[dt_opencl_device_init]
   DEVICE:                   0: 'gfx1035'
   CONF KEY:                 cldevice_v5_amdacceleratedparallelprocessinggfx1035
   PLATFORM, VENDOR & ID:    AMD Accelerated Parallel Processing, Advanced Micro Devices, Inc., ID=4098
   CANONICAL NAME:           amdacceleratedparallelprocessinggfx1035
   DRIVER VERSION:           3625.0 (HSA1.1,LC)
   DEVICE VERSION:           OpenCL 2.0 
   DEVICE_TYPE:              GPU, unified mem
   GLOBAL MEM SIZE:          15421 MB
   MAX MEM ALLOC:            13108 MB
   MAX IMAGE SIZE:           16384 x 16384
   MAX WORK GROUP SIZE:      256
   MAX WORK ITEM DIMENSIONS: 3
   MAX WORK ITEM SIZES:      [ 1024 1024 1024 ]
   ASYNC PIXELPIPE:          NO
   PINNED MEMORY TRANSFER:   NO
   AVOID ATOMICS:            NO
   MICRO NAP:                250
   ROUNDUP WIDTH & HEIGHT    16x16
   CHECK EVENT HANDLES:      128
   TILING ADVANTAGE:         0.000
   DEFAULT DEVICE:           NO
   KERNEL BUILD DIRECTORY:   /usr/share/darktable/kernels
   KERNEL DIRECTORY:         /home/user/.cache/darktable/cached_v3_kernels_for_AMDAcceleratedParallelProcessinggfx1035_36250HSA11LC
   CL COMPILER OPTION:       -cl-fast-relaxed-math
   CL COMPILER COMMAND:      -w -cl-fast-relaxed-math  -DAMD=1 -I"/usr/share/darktable/kernels"
   KERNEL LOADING TIME:       0.0277 sec
[opencl_init] OpenCL successfully initialized. internal numbers and names of available devices:
[opencl_init]           0       'AMD Accelerated Parallel Processing gfx1035'
     0.7484 [opencl_init] FINALLY: opencl PREFERENCE=ON is AVAILABLE and ENABLED.
[opencl_init] opencl_scheduling_profile: 'default'
[opencl_init] opencl_device_priority: '*/!0,*/*/*/!0,*'
[opencl_init] opencl_mandatory_timeout: 400
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       -1      0       0       -1
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       0       0       0       0
[opencl_synchronization_timeout] synchronization timeout set to 200
   UNIFIED MEM SIZE:         7710 MB reserved for 'amdacceleratedparallelprocessinggfx1035'
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       -1      0       0       -1
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       0       0       0       0
[opencl_synchronization_timeout] synchronization timeout set to 200
```


**Output without `mesa-libOpenCL` package**
```
$ rocm-clinfo 
Number of platforms:                             1
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3625.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback 


  Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               1
  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Board name:                                    AMD Radeon Graphics
  Device Topology:                               PCI[ B#51, D#0, F#0 ]
  Max compute units:                             6
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
  Max clock frequency:                           2200Mhz
  Address bits:                                  64
  Max memory allocation:                         13744493360
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
  Cache line size:                               128
  Cache size:                                    16384
  Global memory size:                            16169992192
  Constant buffer size:                          13744493360
  Max number of constant args:                   8
  Local memory type:                             Local
  Local memory size:                             65536
  Max pipe arguments:                            16
  Max pipe active reservations:                  16
  Max pipe packet size:                          859591472
  Max global variable size:                      13744493360
  Max global variable preferred total size:      16169992192
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
  Unified memory for Host and Device:            1
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
  Platform ID:                                   0x7f91c5a007e8
  Name:                                          gfx1035
  Vendor:                                        Advanced Micro Devices, Inc.
  Device OpenCL C version:                       OpenCL C 2.0 
  Driver version:                                3625.0 (HSA1.1,LC)
  Profile:                                       FULL_PROFILE
  Version:                                       OpenCL 2.0 
  Extensions:                                    cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_depth_images cl_amd_copy_buffer_p2p cl_amd_assembly_program 


user@X13:~$ darktable-cltest 
darktable 4.8.1
Copyright (C) 2012-2024 Johannes Hanika and other contributors.

Compile options:
  Bit depth              -> 64 bit
  Debug                  -> DISABLED
  SSE2 optimizations     -> ENABLED
  OpenMP                 -> ENABLED
  OpenCL                 -> ENABLED
  Lua                    -> ENABLED  - API version 9.3.0
  Colord                 -> ENABLED
  gPhoto2                -> ENABLED
  GMIC                   -> ENABLED  - Compressed LUTs are supported
  GraphicsMagick         -> ENABLED
  ImageMagick            -> DISABLED
  libavif                -> ENABLED
  libheif                -> ENABLED
  libjxl                 -> ENABLED
  OpenJPEG               -> ENABLED
  OpenEXR                -> ENABLED
  WebP                   -> ENABLED

See https://www.darktable.org/resources/ for detailed documentation.
See https://github.com/darktable-org/darktable/issues/new/choose to report bugs.

     0.0440 [dt_get_sysresource_level] switched to 1 as `default'
     0.0440   total mem:       30841MB
     0.0440   mipmap cache:    3855MB
     0.0440   available mem:   15420MB
     0.0440   singlebuff:      240MB
     0.0692 [opencl_init] opencl library 'libOpenCL' found on your system and loaded, preference 'default path'
     0.1646 [opencl_init] found 1 platform
[opencl_init] found 1 device

[dt_opencl_device_init]
   DEVICE:                   0: 'gfx1035'
   CONF KEY:                 cldevice_v5_amdacceleratedparallelprocessinggfx1035
   PLATFORM, VENDOR & ID:    AMD Accelerated Parallel Processing, Advanced Micro Devices, Inc., ID=4098
   CANONICAL NAME:           amdacceleratedparallelprocessinggfx1035
   DRIVER VERSION:           3625.0 (HSA1.1,LC)
   DEVICE VERSION:           OpenCL 2.0 
   DEVICE_TYPE:              GPU, unified mem
   GLOBAL MEM SIZE:          15421 MB
   MAX MEM ALLOC:            13108 MB
   MAX IMAGE SIZE:           16384 x 16384
   MAX WORK GROUP SIZE:      256
   MAX WORK ITEM DIMENSIONS: 3
   MAX WORK ITEM SIZES:      [ 1024 1024 1024 ]
   ASYNC PIXELPIPE:          NO
   PINNED MEMORY TRANSFER:   NO
   AVOID ATOMICS:            NO
   MICRO NAP:                250
   ROUNDUP WIDTH & HEIGHT    16x16
   CHECK EVENT HANDLES:      128
   TILING ADVANTAGE:         0.000
   DEFAULT DEVICE:           NO
   KERNEL BUILD DIRECTORY:   /usr/share/darktable/kernels
   KERNEL DIRECTORY:         /home/user/.cache/darktable/cached_v3_kernels_for_AMDAcceleratedParallelProcessinggfx1035_36250HSA11LC
   CL COMPILER OPTION:       -cl-fast-relaxed-math
   CL COMPILER COMMAND:      -w -cl-fast-relaxed-math  -DAMD=1 -I"/usr/share/darktable/kernels"
   KERNEL LOADING TIME:       0.0285 sec
[opencl_init] OpenCL successfully initialized. internal numbers and names of available devices:
[opencl_init]           0       'AMD Accelerated Parallel Processing gfx1035'
     0.6998 [opencl_init] FINALLY: opencl PREFERENCE=ON is AVAILABLE and ENABLED.
[opencl_init] opencl_scheduling_profile: 'default'
[opencl_init] opencl_device_priority: '*/!0,*/*/*/!0,*'
[opencl_init] opencl_mandatory_timeout: 400
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       -1      0       0       -1
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       0       0       0       0
[opencl_synchronization_timeout] synchronization timeout set to 200
   UNIFIED MEM SIZE:         7710 MB reserved for 'amdacceleratedparallelprocessinggfx1035'
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       -1      0       0       -1
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities]           image   preview export  thumbs  preview2
[dt_opencl_update_priorities]           0       0       0       0       0
[opencl_synchronization_timeout] synchronization timeout set to 200
```

---

### 评论 #21 — jamesxu2 (2024-10-07T15:10:00Z)

Hi @Germano0 

I'm glad to hear we've somewhat resolved this mystery. 

PAL ("Platform Abstraction Layer") was a previous backend to allow a GPU-agnostic interface for compute programming, as a predecessor of ROCm. The PAL backend for OpenCL is deprecated at this point, since around 2020. 

Regarding your second test on your Thinkpad, I'm not sure rocm-clinfo really works with mesa-libOpenCL since it still fails with ERROR: clBuildProgram(-11). It looks like darktable-cltest in both cases is also for some reason using the AMD openCL backend and not the Mesa one  (```   PLATFORM, VENDOR & ID:    AMD Accelerated Parallel Processing, Advanced Micro Devices, Inc., ID=4098```), though it's a bit beyond the scope for us in ROCm support to debug that. 

Can we close this ticket? I think the root cause here is having multiple conflicting OpenCL platforms installed and not a ROCm issue.

---

### 评论 #22 — Germano0 (2024-10-07T15:15:29Z)

Sure we can close the ticket, thank you for your kind support!

---

### 评论 #23 — jamesxu2 (2024-10-07T15:17:21Z)

@Germano0  Thanks for the debugging effort on your end too! Cheers :) 

---

### 评论 #24 — Germano0 (2024-10-07T15:28:19Z)

A final note: I informed Fedora rocm package maintainers [here](https://bugzilla.redhat.com/show_bug.cgi?id=2316985)
Cheers

---
