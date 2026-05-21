# Memory access fault by GPU node in Pytorch

> **Issue #2235**
> **状态**: closed
> **创建时间**: 2023-06-10T14:12:42Z
> **更新时间**: 2023-12-05T20:57:51Z
> **关闭时间**: 2023-12-05T20:57:51Z
> **作者**: linwk20
> **标签**: hardware:Radeon, application:pytorch
> **URL**: https://github.com/ROCm/ROCm/issues/2235

## 标签

- **hardware:Radeon** (颜色: #2B113F)
- **application:pytorch** (颜色: #bfdadc)

## 描述

Hi, 
I am running rocm + pytorch. I am using rocm 5.4.2 + Pytorch2.0.0 docker.
I have two types of cards, RX6300, and Radeon VII. RX 6300 worked fine, but when I using Radeon VII, I encountered a memory fault. Codes are shown below:
```
 torch.cuda.set_device(2)
print(f"running with device: {torch.cuda.get_device_name(torch.cuda.current_device())}")
\\ return running with device: AMD Radeon VII
a = torch.rand((1,1)).float()
a.to(torch.device('cuda'))
\\ error messeage: Memory access fault by GPU node-10 (Agent handle: 0x7538750) on address (nil). Reason: Page not present or 
\\ supervisor privilege.
\\ Aborted (core dumped)

\\ sometimes, it return: Segmentation fault (core dumped) 
```

Can anyone help me? Thanks in advance!


---

## 评论 (3 条)

### 评论 #1 — linwk20 (2023-06-10T14:35:55Z)

It might be memory access problems? when I run "clinfo", it also return errors:
```
clinfo

  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Board name:                                    AMD Radeon VII
  Device Topology:                               PCI[ B#67, D#0, F#0 ]
  Max compute units:                             60
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
  Max clock frequency:                           1801Mhz
  Address bits:                                  64
  Max memory allocation:                         14588628168
  Image support:                                 Yes
  Max number of images read arguments:           128
  Max number of images write arguments:          8
  Max image 2D width:                            16384
  Max image 2D height:                           16384
  Max image 3D width:                            16384
  Max image 3D height:                           16384
  Max image 3D depth:                            8192
  Max samplers within kernel:                    26287
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
  Cache size:                                    16384
  Global memory size:                            17163091968
  Constant buffer size:                          14588628168
  Max number of constant args:                   8
  Local memory type:                             Scratchpad
  Local memory size:                             65536
  Max pipe arguments:                            16
  Max pipe active reservations:                  16
  Max pipe packet size:                          1703726280
  Max global variable size:                      14588628168
  Max global variable preferred total size:      17163091968
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
ERROR: clCreateKernel(-6)
```

---

### 评论 #2 — hongxiayang (2023-12-05T20:39:42Z)

This is case of mixed gpu types. 
Can you do the following command:
```
rocminfo|grep gfx
```


---

### 评论 #3 — linwk20 (2023-12-05T20:57:51Z)

Yes. I have solved it after plug out the RX6300.

Thank you @hongxiayang 

---
