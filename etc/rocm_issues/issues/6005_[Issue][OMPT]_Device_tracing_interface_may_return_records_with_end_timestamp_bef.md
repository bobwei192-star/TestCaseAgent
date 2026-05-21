# [Issue][OMPT]: Device tracing interface may return records with end timestamp before begin timestamp

> **Issue #6005**
> **状态**: open
> **创建时间**: 2026-02-27T15:24:51Z
> **更新时间**: 2026-02-27T16:30:41Z
> **作者**: Thyre
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6005

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- adityas-amd

## 描述

### Problem Description

While investigating the current state of the device tracing interface in ROCm v7.2.0 and one of the latest development snapshots of TheRock, I've noticed a test failure in the performance measurement infrastructure Score-P due to an inconsistent profile.

```
[Score-P] src/adapters/ompt/scorep_ompt_events_device_callbacks.inc.c:176: Warning: [OMPT] Zero byte buffer received on device gfx1101 (0).
[Score-P] src/measurement/scorep_location_management.c:438: Fatal: Bug 'timestamp < location->last_timestamp': Wrong timestamp order on location 2: 174045318878735 (last recorded) > 174045318877265 (current). This might be an indication of thread migration. Please pin your threads. Using a SCOREP_TIMER different from tsc might also help.
[Score-P] Please report this to support@score-p.org. Thank you.
[Score-P] Try also to preserve any generated core dumps.
```

Upon closer inspection, I found out that one particular test case in our CI may cause the OpenMP runtime to return an `ompt_record_ompt_t` record where `record->time` is higher than `record->record.target_data_op.end_time`.
This behavior is reproducible without Score-P as well. However, it doesn't occur consistently, which leads me to think that I might be triggering some race condition.

### Operating System

Ubuntu 22.04 LTS

### CPU

Intel Core i7-12700

### GPU

AMD Radeon RX 7700 XT

### ROCm Version

ROCm 7.2.0 // TheRock 20260225

### ROCm Component

llvm-project

### Steps to Reproduce

The test code itself, adapted from the OpenMP Example's [target_data.3.c](https://github.com/OpenMP/Examples/blob/main/devices/sources/target_data.3.c), looks like this:
```c
/*
* @@name:	target_data.3
* @@type:	C
* @@operation:	compile
* @@expect:	success
* @@version:	omp_4.0
*/
#include <math.h>

#define COLS 100

void gramSchmidt(float Q[][COLS], const int rows) {
    int cols = COLS;
#pragma omp target data map(Q[0:rows][0:cols])
    for (int k = 0; k < cols; k++) {
        double tmp = 0.0;

#pragma omp target map(tofrom: tmp)
#pragma omp parallel for reduction(+:tmp)
        for (int i = 0; i < rows; i++)
            tmp += (Q[i][k] * Q[i][k]);

        tmp = 1 / sqrt(tmp);

#pragma omp target
#pragma omp parallel for
        for (int i = 0; i < rows; i++)
            Q[i][k] *= tmp;
    }
}

/* Note:  The variable tmp is now mapped with tofrom, for correct
          execution with 4.5 (and pre-4.5) compliant compilers.
          See Devices Intro.
 */
int main(void)
{
    float Q[COLS][COLS];
    gramSchmidt(Q, COLS);
}
```

We can attach a tools interface to this, and abort when we encounter the scenario described above. This yields this full reproducer:

- [reproducer.zip](https://github.com/user-attachments/files/25607543/reproducer.zip)

I've used the OMPT interface used in AOMP for [this test](https://github.com/ROCm/aomp/tree/887673190d7b43835e8b61e0c39a849cc247cc1d/examples/tools/ompt/veccopy-ompt-target-tracing), but adapted it slightly:

```diff
--- callbacks.h.orig    2026-02-27 16:23:24.596475342 +0100
+++ callbacks.h 2026-02-27 16:16:33.642458748 +0100
@@ -1,4 +1,6 @@
 #include <assert.h>
+#include <stdio.h>
+#include <stdlib.h>

 // Available at $INSTALL_DIR/include/omp-tools.h
 #include <omp-tools.h>
@@ -57,6 +59,7 @@
             target_data_op_rec.bytes, target_data_op_rec.end_time,
             target_data_op_rec.end_time - rec->time,
             target_data_op_rec.codeptr_ra);
+      assert(rec->time < target_data_op_rec.end_time);
       break;
     }
   case ompt_callback_target_submit:
@@ -68,6 +71,7 @@
             target_kernel_rec.host_op_id, target_kernel_rec.requested_num_teams,
             target_kernel_rec.granted_num_teams, target_kernel_rec.end_time,
             target_kernel_rec.end_time - rec->time);
+      assert(rec->time < target_kernel_rec.end_time);
     break;
     }
   default:
```

We can run this reproducer via:

```console
$ amdclang -fopenmp --offload-arch=gfx1101 reproducer.c -lm
$ export OMP_TARGET_OFFLOAD=mandatory
$ for i in $(seq 1 10); do ./a.out; if [ $? != 0 ]; then echo "====TEST FAILED===="; break; fi; done
```

which will yield:

```
[...]
Allocated 256 bytes at 0x3676e5a0 in buffer request callback
a.out: ./callbacks.h:74: void print_record_ompt(ompt_record_ompt_t *): Assertion `rec->time < target_kernel_rec.end_time' failed.
  Callback DataOp: target_id=196 host_op_id=200 optype=3 src=0x7a5b7742a000 src_device_num=0 dest=0x7ffd047449e0 dest_device_num=1 bytes=8 code=0x20efe8
====TEST FAILED====
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

<details>
<summary>Click to open</summary>

```
ROCk module version 6.18.4 is loaded
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
  Name:                    12th Gen Intel(R) Core(TM) i7-12700
  Uuid:                    CPU-XX
  Marketing Name:          12th Gen Intel(R) Core(TM) i7-12700
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
  Max Clock Freq. (MHz):   4800
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            20
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    65578992(0x3e8a7f0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65578992(0x3e8a7f0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65578992(0x3e8a7f0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65578992(0x3e8a7f0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1101
  Uuid:                    GPU-1cf1a6db839c29d5
  Marketing Name:          AMD Radeon RX 7700 XT
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
    L3:                      49152(0xc000) KB
  Chip ID:                 29822(0x747e)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2171
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            54
  SIMDs per CU:            2
  Shader Engines:          3
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
  Packet Processor uCode:: 412
  SDMA engine uCode::      25
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    12566528(0xbfc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    12566528(0xbfc000) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx1101
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
```

</details>

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — Thyre (2026-02-27T15:25:59Z)

CC @jplehr, found while I took a look at TheRock.
@mhalk, @dhruvachak, this may be interesting for you as well.

---

### 评论 #2 — Thyre (2026-02-27T16:30:41Z)

Checking with TheRock 20260225 on a MI250X system, I'm not able to trigger this issue.
Maybe this is architecture dependent?

---
