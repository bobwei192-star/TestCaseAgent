# [Issue]: ROCm fails to build on Debian 13 with unit test errors GCC too new maybe

> **Issue #4272**
> **状态**: closed
> **创建时间**: 2025-01-19T16:54:50Z
> **更新时间**: 2025-02-10T20:01:14Z
> **关闭时间**: 2025-02-10T20:01:14Z
> **作者**: brcisna
> **标签**: Under Investigation, ROCm 6.2.1
> **URL**: https://github.com/ROCm/ROCm/issues/4272

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.1** (颜色: #ededed)

## 描述

### Problem Description

Debian 13 Trixie   AMD Radeon Pro W6600

dual processor 40 cores, 128GB system ram 

Trying to compile the latest ROCm6.3.1

`ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          YES

`
Trying to compile from source doing a make all,
The build procedure runs for about 30 minutes then just exits with no errors with the following at the end of the log in 'lightning.log' 
unit tests are killing the process somehow,,,i think?
I also tried doing the docker setup for Ubuntu24 but the setup for docker Ubuntu 24 doesnt complete with password,,will not let extra depedencies install:(
Tried a few times and gace up.
Am pretty certtain this build failure is due to the later GCC versions etc.  version 14.

`
`/home/superuser/Downloads/ROCm/out/debian-/build/lightning/tools/mlir/test/lib/Dialect/Test/TestOps.h.inc:32712:18: note: use unary ‘+’ which decays operands to pointers or ‘&(rhs.test::detail::TestOpUsingPropertyInCustomGenericAdaptorBase::Properties::prop)[0] == &(((const test::detail::TestOpUsingPropertyInCustomGenericAdaptorBase::Properties*)this)->test::detail::TestOpUsingPropertyInCustomGenericAdaptorBase::Properties::prop)[0]’ to compare the addresses
/home/superuser/Downloads/ROCm/out/debian-/build/lightning/tools/mlir/test/lib/Dialect/Test/TestOps.h.inc: In member function ‘bool test::detail::TestOpWithPropertiesGenericAdaptorBase::Properties::operator==(const test::detail::TestOpWithPropertiesGenericAdaptorBase::Properties&) const’:
/home/superuser/Downloads/ROCm/out/debian-/build/lightning/tools/mlir/test/lib/Dialect/Test/TestOps.h.inc:33130:19: warning: comparison between two arrays [-Warray-compare]
33130 |         rhs.array == this->array &&
      |         ~~~~~~~~~~^~~~~~~~~~~~~~
/home/superuser/Downloads/ROCm/out/debian-/build/lightning/tools/mlir/test/lib/Dialect/Test/TestOps.h.inc:33130:19: note: use unary ‘+’ which decays operands to pointers or ‘&(rhs.test::detail::TestOpWithPropertiesGenericAdaptorBase::Properties::array)[0] == &(((const test::detail::TestOpWithPropertiesGenericAdaptorBase::Properties*)this)->test::detail::TestOpWithPropertiesGenericAdaptorBase::Properties::array)[0]’ to compare the addresses
ninja: build stopped: subcommand failed.


real	27m53.741s
user	927m12.025s
sys	23m39.796s

real	27m53.777s
user	927m12.053s
sys	23m39.806s
+ mv /home/superuser/Downloads/ROCm/out/debian-//logs/lightning.inprogress /home/superuser/Downloads/ROCm/out/debian-//logs/lightning.errors
+ echo Error in lightning
Error in lightning
+ exit 1'

### Operating System

Debian 13

### CPU

Intel 

### GPU

AMD Radeon Pro W6600

### ROCm Version

ROCm 6.2.1

### ROCm Component

_No response_

### Steps to Reproduce

try and compile ROCm from source package 

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-01-20T21:56:45Z)

Hi @brcisna, thanks for the report. Currently trying to reproduce this on our end and I do see that lightning/LLVM is taking quite long, though no error logs are generated as in your case. 

In the meantime, can you give this another try with the Ubuntu-24 docker image but skip the prerequisite installation? This step is only necessary for a baremetal installation as the docker image has all the dependencies pre-installed.

---

### 评论 #2 — harkgill-amd (2025-01-30T19:36:19Z)

@brcisna, have you gotten a chance to try building ROCm with the Ubuntu-24 docker image as mentioned previously? I wasn't able to reproduce either of the errors reported on this supported configuration. 

---
