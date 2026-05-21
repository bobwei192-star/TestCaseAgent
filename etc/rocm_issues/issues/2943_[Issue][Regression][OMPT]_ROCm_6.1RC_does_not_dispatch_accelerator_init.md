# [Issue][Regression][OMPT]: ROCm 6.1RC does not dispatch accelerator init

> **Issue #2943**
> **状态**: closed
> **创建时间**: 2024-03-05T11:58:01Z
> **更新时间**: 2024-03-24T13:05:50Z
> **关闭时间**: 2024-03-24T13:05:50Z
> **作者**: Thyre
> **标签**: AMD Instinct MI250X, ROCm 6.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/2943

## 标签

- **AMD Instinct MI250X** (颜色: #ededed)
- **ROCm 6.0.0** (颜色: #ededed)

## 负责人

- dhruvachak

## 描述

### Problem Description

Right now, ROCm is the only compiler implementing most of the OMPT accelerator events, including the device tracing interface for accurate timestamps for executed kernels and data transfers. While there are still some issues left, which are already fixed in AOMP, I consider the interface in ROCm 6.0.2 mostly usable, if users know the limitations.
Score-P has based its (in development) implementation of the OMPT support for offloading, including the device tracing interface, on ROCm (which can be found [here](https://perftools.pages.jsc.fz-juelich.de/cicd/scorep/branches/MR344/latest.tar.gz)). 

With ROCm 6.1 RC however, the interface is broken enough, that performance tools will not be able to use the interface at all. Now, only `ompt_callback_target_emi`, `ompt_callback_target_submit_emi` and `ompt_callback_target_data_op_emi` are dispatched. We do not get any events for device initialization (`ompt_callback_device_initialize`) anymore, preventing usage of the device tracing interface.
This is quite bad for us, as this will simply mean that users will not be able to use ROCm 6.1 to get events for their OpenMP programs with offloading. We would like to continue recommending the latest and greatest versions to users, as bugs are fixed continuously.

### Operating System

Apptainer -- Ubuntu 22.04.3 LTS on JURECA-DC Evaluation Platform

### CPU

2x AMD EPYC 7443 24-Core Processor

### GPU

4x AMD Instinct MI250X

### ROCm Version

ROCm 6.1.0 RC

### ROCm Component

llvm-project

### Steps to Reproduce

With ROCm 6.1 RC installed, one can reproduce the issue with the following steps:

- 1. Get the test case from [aomp/tree/aomp-dev/test/smoke/veccopy-ompt-target-emi](https://github.com/ROCm/aomp/tree/aomp-dev/test/smoke/veccopy-ompt-target-emi)
- 2. Compile the test case via `amdclang -fopenmp --offload-arch=gfx90a`
- 3. Run the test case. You will see the following output:
```
Callback Target EMI: kind=1 endpoint=1 device_num=0 task_data=0x913880 (0x0) target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) code=0x229fa8
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000002) src=0x7ffe3b8c6c30 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x145b46c0639e
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000002) src=0x7ffe3b8c6c30 src_device_num=8 dest=0x145942220000 dest_device_num=0 bytes=400000 code=0x145b46c0639e
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000003) src=0x7ffe3b8c6c30 src_device_num=8 dest=0x145942220000 dest_device_num=0 bytes=400000 code=0x145b46c071db
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000003) src=0x7ffe3b8c6c30 src_device_num=8 dest=0x145942220000 dest_device_num=0 bytes=400000 code=0x145b46c071db
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000004) src=0x7ffe3b8651b0 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x145b46c0639e
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000004) src=0x7ffe3b8651b0 src_device_num=8 dest=0x145942282000 dest_device_num=0 bytes=400000 code=0x145b46c0639e
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000005) src=0x7ffe3b8651b0 src_device_num=8 dest=0x145942282000 dest_device_num=0 bytes=400000 code=0x145b46c071db
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000005) src=0x7ffe3b8651b0 src_device_num=8 dest=0x145942282000 dest_device_num=0 bytes=400000 code=0x145b46c071db
  Callback Submit EMI: endpoint=1  req_num_teams=1 target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000005)
  Callback Submit EMI: endpoint=2  req_num_teams=1 target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000005)
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000006) src=0x145942282000 src_device_num=0 dest=0x7ffe3b8651b0 dest_device_num=8 bytes=400000 code=0x145b46c08613
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000006) src=0x145942282000 src_device_num=0 dest=0x7ffe3b8651b0 dest_device_num=8 bytes=400000 code=0x145b46c08613
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000007) src=0x145942220000 src_device_num=0 dest=0x7ffe3b8c6c30 dest_device_num=8 bytes=400000 code=0x145b46c08613
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000007) src=0x145942220000 src_device_num=0 dest=0x7ffe3b8c6c30 dest_device_num=8 bytes=400000 code=0x145b46c08613
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000008) src=0x145942282000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x145b46c07e1e
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000008) src=0x145942282000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x145b46c07e1e
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000009) src=0x145942220000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x145b46c07e1e
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) host_op_id=0x145b465f4520 (0x8000000000000009) src=0x145942220000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x145b46c07e1e
Callback Target EMI: kind=1 endpoint=2 device_num=0 task_data=0x913880 (0x0) target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x8000000000000001) code=0x229fa8
Callback Target EMI: kind=1 endpoint=1 device_num=0 task_data=0x913880 (0x0) target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) code=0x22a1ca
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000b) src=0x7ffe3b8c6c30 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x145b46c0639e
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000b) src=0x7ffe3b8c6c30 src_device_num=8 dest=0x145942220000 dest_device_num=0 bytes=400000 code=0x145b46c0639e
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000c) src=0x7ffe3b8c6c30 src_device_num=8 dest=0x145942220000 dest_device_num=0 bytes=400000 code=0x145b46c071db
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000c) src=0x7ffe3b8c6c30 src_device_num=8 dest=0x145942220000 dest_device_num=0 bytes=400000 code=0x145b46c071db
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000d) src=0x7ffe3b8651b0 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x145b46c0639e
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000d) src=0x7ffe3b8651b0 src_device_num=8 dest=0x145942282000 dest_device_num=0 bytes=400000 code=0x145b46c0639e
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000e) src=0x7ffe3b8651b0 src_device_num=8 dest=0x145942282000 dest_device_num=0 bytes=400000 code=0x145b46c071db
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000e) src=0x7ffe3b8651b0 src_device_num=8 dest=0x145942282000 dest_device_num=0 bytes=400000 code=0x145b46c071db
  Callback Submit EMI: endpoint=1  req_num_teams=0 target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000e)
  Callback Submit EMI: endpoint=2  req_num_teams=0 target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000e)
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000f) src=0x145942282000 src_device_num=0 dest=0x7ffe3b8651b0 dest_device_num=8 bytes=400000 code=0x145b46c08613
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x800000000000000f) src=0x145942282000 src_device_num=0 dest=0x7ffe3b8651b0 dest_device_num=8 bytes=400000 code=0x145b46c08613
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x8000000000000010) src=0x145942220000 src_device_num=0 dest=0x7ffe3b8c6c30 dest_device_num=8 bytes=400000 code=0x145b46c08613
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x8000000000000010) src=0x145942220000 src_device_num=0 dest=0x7ffe3b8c6c30 dest_device_num=8 bytes=400000 code=0x145b46c08613
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x8000000000000011) src=0x145942282000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x145b46c07e1e
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x8000000000000011) src=0x145942282000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x145b46c07e1e
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x8000000000000012) src=0x145942220000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x145b46c07e1e
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) host_op_id=0x145b465f4520 (0x8000000000000012) src=0x145942220000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x145b46c07e1e
Callback Target EMI: kind=1 endpoint=2 device_num=0 task_data=0x913880 (0x0) target_task_data=0x914c98 (0x0) target_data=0x145b465f4578 (0x800000000000000a) code=0x22a1ca
Success
```

Notice the missing lines like:
```
  /// CHECK: Callback Init:
  /// CHECK: Callback Load:
[...]
  /// CHECK: Callback Fini:
```

With a tool with device tracing, the issue becomes even more apparent. If you try to run [veccopy-ompt-target-emi-tracing](https://github.com/ROCm/aomp/tree/aomp-dev/test/smoke/veccopy-ompt-target-emi-tracing), execution will simply segmentation fault at the end, since no device was initialized:

```
Callback Target EMI: kind=1 endpoint=1 device_num=0 task_data=0xf80900 (0x0) target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) code=0x22c8f8
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000002) src=0x7ffe3eb158e0 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x14832039439e
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000002) src=0x7ffe3eb158e0 src_device_num=8 dest=0x147b10c20000 dest_device_num=0 bytes=400000 code=0x14832039439e
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000003) src=0x7ffe3eb158e0 src_device_num=8 dest=0x147b10c20000 dest_device_num=0 bytes=400000 code=0x1483203951db
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000003) src=0x7ffe3eb158e0 src_device_num=8 dest=0x147b10c20000 dest_device_num=0 bytes=400000 code=0x1483203951db
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000004) src=0x7ffe3eab3e60 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x14832039439e
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000004) src=0x7ffe3eab3e60 src_device_num=8 dest=0x147b10c82000 dest_device_num=0 bytes=400000 code=0x14832039439e
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000005) src=0x7ffe3eab3e60 src_device_num=8 dest=0x147b10c82000 dest_device_num=0 bytes=400000 code=0x1483203951db
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000005) src=0x7ffe3eab3e60 src_device_num=8 dest=0x147b10c82000 dest_device_num=0 bytes=400000 code=0x1483203951db
  Callback Submit EMI: endpoint=1 req_num_teams=1 target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000005)
  Callback Submit EMI: endpoint=2 req_num_teams=1 target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000005)
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000006) src=0x147b10c82000 src_device_num=0 dest=0x7ffe3eab3e60 dest_device_num=8 bytes=400000 code=0x148320396613
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000006) src=0x147b10c82000 src_device_num=0 dest=0x7ffe3eab3e60 dest_device_num=8 bytes=400000 code=0x148320396613
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000007) src=0x147b10c20000 src_device_num=0 dest=0x7ffe3eb158e0 dest_device_num=8 bytes=400000 code=0x148320396613
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000007) src=0x147b10c20000 src_device_num=0 dest=0x7ffe3eb158e0 dest_device_num=8 bytes=400000 code=0x148320396613
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000008) src=0x147b10c82000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x148320395e1e
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000008) src=0x147b10c82000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x148320395e1e
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000009) src=0x147b10c20000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x148320395e1e
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) host_op_id=0x14832009d200 (0x8000000000000009) src=0x147b10c20000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x148320395e1e
Callback Target EMI: kind=1 endpoint=2 device_num=0 task_data=0xf80900 (0x0) target_task_data=0xf81cd8 (0x0) target_data=0x14832009d258 (0x8000000000000001) code=0x22c8f8
Segmentation fault
```

---

Here are the same examples with ROCm 6.0.2. Here, everything is working fine:

**veccopy-ompt-target-emi:**

<details>
<summary>Click to open</summary>

```
Callback Init: device_num=0 type=gfx90a device=0x1070160 lookup=0x14c4e0cf0c90 doc=(nil)
Callback Load: device_num:0 filename:(null) host_adddr:0x200378 device_addr:(nil) bytes:142712
Callback Target EMI: kind=1 endpoint=1 device_num=0 task_data=0xb40d00 (0x0) target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) code=0x225b48
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000002) src=0x7ffc1db6c260 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x14c4e9b5862b
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000002) src=0x7ffc1db6c260 src_device_num=8 dest=0x14bcdde20000 dest_device_num=0 bytes=400000 code=0x14c4e9b5862b
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000003) src=0x7ffc1db6c260 src_device_num=8 dest=0x14bcdde20000 dest_device_num=0 bytes=400000 code=0x14c4e9b594bb
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000003) src=0x7ffc1db6c260 src_device_num=8 dest=0x14bcdde20000 dest_device_num=0 bytes=400000 code=0x14c4e9b594bb
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000004) src=0x7ffc1db0a7e0 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x14c4e9b5862b
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000004) src=0x7ffc1db0a7e0 src_device_num=8 dest=0x14bcdde82000 dest_device_num=0 bytes=400000 code=0x14c4e9b5862b
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000005) src=0x7ffc1db0a7e0 src_device_num=8 dest=0x14bcdde82000 dest_device_num=0 bytes=400000 code=0x14c4e9b594bb
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000005) src=0x7ffc1db0a7e0 src_device_num=8 dest=0x14bcdde82000 dest_device_num=0 bytes=400000 code=0x14c4e9b594bb
  Callback Submit EMI: endpoint=1  req_num_teams=1 target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000005)
  Callback Submit EMI: endpoint=2  req_num_teams=1 target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000005)
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000006) src=0x14bcdde82000 src_device_num=0 dest=0x7ffc1db0a7e0 dest_device_num=8 bytes=400000 code=0x14c4e9b5a8e3
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000006) src=0x14bcdde82000 src_device_num=0 dest=0x7ffc1db0a7e0 dest_device_num=8 bytes=400000 code=0x14c4e9b5a8e3
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000007) src=0x14bcdde20000 src_device_num=0 dest=0x7ffc1db6c260 dest_device_num=8 bytes=400000 code=0x14c4e9b5a8e3
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000007) src=0x14bcdde20000 src_device_num=0 dest=0x7ffc1db6c260 dest_device_num=8 bytes=400000 code=0x14c4e9b5a8e3
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000008) src=0x14bcdde82000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x14c4e9b5a100
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000008) src=0x14bcdde82000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x14c4e9b5a100
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000009) src=0x14bcdde20000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x14c4e9b5a100
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) host_op_id=0x14c4e957a760 (0x8000000000000009) src=0x14bcdde20000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x14c4e9b5a100
Callback Target EMI: kind=1 endpoint=2 device_num=0 task_data=0xb40d00 (0x0) target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x8000000000000001) code=0x225b48
Callback Target EMI: kind=1 endpoint=1 device_num=0 task_data=0xb40d00 (0x0) target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) code=0x225d6a
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000b) src=0x7ffc1db6c260 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x14c4e9b5862b
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000b) src=0x7ffc1db6c260 src_device_num=8 dest=0x14bcdde20000 dest_device_num=0 bytes=400000 code=0x14c4e9b5862b
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000c) src=0x7ffc1db6c260 src_device_num=8 dest=0x14bcdde20000 dest_device_num=0 bytes=400000 code=0x14c4e9b594bb
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000c) src=0x7ffc1db6c260 src_device_num=8 dest=0x14bcdde20000 dest_device_num=0 bytes=400000 code=0x14c4e9b594bb
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000d) src=0x7ffc1db0a7e0 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x14c4e9b5862b
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000d) src=0x7ffc1db0a7e0 src_device_num=8 dest=0x14bcdde82000 dest_device_num=0 bytes=400000 code=0x14c4e9b5862b
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000e) src=0x7ffc1db0a7e0 src_device_num=8 dest=0x14bcdde82000 dest_device_num=0 bytes=400000 code=0x14c4e9b594bb
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000e) src=0x7ffc1db0a7e0 src_device_num=8 dest=0x14bcdde82000 dest_device_num=0 bytes=400000 code=0x14c4e9b594bb
  Callback Submit EMI: endpoint=1  req_num_teams=0 target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000e)
  Callback Submit EMI: endpoint=2  req_num_teams=0 target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000e)
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000f) src=0x14bcdde82000 src_device_num=0 dest=0x7ffc1db0a7e0 dest_device_num=8 bytes=400000 code=0x14c4e9b5a8e3
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x800000000000000f) src=0x14bcdde82000 src_device_num=0 dest=0x7ffc1db0a7e0 dest_device_num=8 bytes=400000 code=0x14c4e9b5a8e3
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x8000000000000010) src=0x14bcdde20000 src_device_num=0 dest=0x7ffc1db6c260 dest_device_num=8 bytes=400000 code=0x14c4e9b5a8e3
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x8000000000000010) src=0x14bcdde20000 src_device_num=0 dest=0x7ffc1db6c260 dest_device_num=8 bytes=400000 code=0x14c4e9b5a8e3
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x8000000000000011) src=0x14bcdde82000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x14c4e9b5a100
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x8000000000000011) src=0x14bcdde82000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x14c4e9b5a100
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x8000000000000012) src=0x14bcdde20000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x14c4e9b5a100
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) host_op_id=0x14c4e957a760 (0x8000000000000012) src=0x14bcdde20000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x14c4e9b5a100
Callback Target EMI: kind=1 endpoint=2 device_num=0 task_data=0xb40d00 (0x0) target_task_data=0xb42118 (0x0) target_data=0x14c4e957a7b8 (0x800000000000000a) code=0x225d6a
Success
Callback Fini: device_num=0
```

</details>

**veccopy-ompt-target-emi-tracing:**

<details>
<summary>Click to open</summary>

```
Callback Init: device_num=0 type=gfx90a device=0x1651170 lookup=0x1553007b7c90 doc=(nil)
Callback Load: device_num:0 filename:(null) host_adddr:0x200378 device_addr:(nil) bytes:142712
Callback Target EMI: kind=1 endpoint=1 device_num=0 task_data=0x1121d40 (0x0) target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) code=0x228488
Allocated 256 bytes at 0x11c2010 in buffer request callback
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000002) src=0x7ffde9be04f0 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x15530930462b
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000002) src=0x7ffde9be04f0 src_device_num=8 dest=0x154afd820000 dest_device_num=0 bytes=400000 code=0x15530930462b
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000003) src=0x7ffde9be04f0 src_device_num=8 dest=0x154afd820000 dest_device_num=0 bytes=400000 code=0x1553093054bb
Allocated 256 bytes at 0x1658a50 in buffer request callback
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000003) src=0x7ffde9be04f0 src_device_num=8 dest=0x154afd820000 dest_device_num=0 bytes=400000 code=0x1553093054bb
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000004) src=0x7ffde9b7ea70 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x15530930462b
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000004) src=0x7ffde9b7ea70 src_device_num=8 dest=0x154afd882000 dest_device_num=0 bytes=400000 code=0x15530930462b
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000005) src=0x7ffde9b7ea70 src_device_num=8 dest=0x154afd882000 dest_device_num=0 bytes=400000 code=0x1553093054bb
Allocated 256 bytes at 0x1654da0 in buffer request callback
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000005) src=0x7ffde9b7ea70 src_device_num=8 dest=0x154afd882000 dest_device_num=0 bytes=400000 code=0x1553093054bb
  Callback Submit EMI: endpoint=1 req_num_teams=1 target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000005)
  Callback Submit EMI: endpoint=2 req_num_teams=1 target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000005)
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000006) src=0x154afd882000 src_device_num=0 dest=0x7ffde9b7ea70 dest_device_num=8 bytes=400000 code=0x1553093068e3
Allocated 256 bytes at 0x1653640 in buffer request callback
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000006) src=0x154afd882000 src_device_num=0 dest=0x7ffde9b7ea70 dest_device_num=8 bytes=400000 code=0x1553093068e3
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000007) src=0x154afd820000 src_device_num=0 dest=0x7ffde9be04f0 dest_device_num=8 bytes=400000 code=0x1553093068e3
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000007) src=0x154afd820000 src_device_num=0 dest=0x7ffde9be04f0 dest_device_num=8 bytes=400000 code=0x1553093068e3
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000008) src=0x154afd882000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x155309306100
Allocated 256 bytes at 0x16539a0 in buffer request callback
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000008) src=0x154afd882000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x155309306100
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000009) src=0x154afd820000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x155309306100
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) host_op_id=0x155309041740 (0x8000000000000009) src=0x154afd820000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x155309306100
Allocated 256 bytes at 0x1655450 in buffer request callback
Callback Target EMI: kind=1 endpoint=2 device_num=0 task_data=0x1121d40 (0x0) target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x8000000000000001) code=0x228488
Executing buffer complete callback: 0 0x11c2010 208 0x11c2010 0
rec=0x11c2010 type=8 (Target task) time=0 thread_id=0 target_id=0x8000000000000001 kind=1 endpoint=1 device=0 task_id=0 codeptr=0x228488
rec=0x11c2078 type=9 (Target data op) time=968206593060673 thread_id=0 target_id=0x8000000000000001 host_op_id=0x8000000000000002 optype=1 src_addr=0x7ffde9be04f0 src_device=8 dest_addr=0x154afd820000 dest_device=0 bytes=400000 end_time=968206593062733 duration=2060 ns codeptr=0x15530930462b
Executing buffer complete callback: 0 0x11c2010 0 (nil) 1
Deallocated 0x11c2010
Executing buffer complete callback: 0 0x1658a50 208 0x1658a50 0
rec=0x1658a50 type=9 (Target data op) time=968206593225757 thread_id=0 target_id=0x8000000000000001 host_op_id=0x8000000000000003 optype=2 src_addr=0x7ffde9be04f0 src_device=8 dest_addr=0x154afd820000 dest_device=0 bytes=400000 end_time=968206593259518 duration=33761 ns codeptr=0x1553093054bb
rec=0x1658ab8 type=9 (Target data op) time=968206593268762 thread_id=0 target_id=0x8000000000000001 host_op_id=0x8000000000000004 optype=1 src_addr=0x7ffde9b7ea70 src_device=8 dest_addr=0x154afd882000 dest_device=0 bytes=400000 end_time=968206593269422 duration=660 ns codeptr=0x15530930462b
Executing buffer complete callback: 0 0x1658a50 0 (nil) 1
Deallocated 0x1658a50
Executing buffer complete callback: 0 0x1654da0 208 0x1654da0 0
rec=0x1654da0 type=9 (Target data op) time=968206593384003 thread_id=0 target_id=0x8000000000000001 host_op_id=0x8000000000000005 optype=2 src_addr=0x7ffde9b7ea70 src_device=8 dest_addr=0x154afd882000 dest_device=0 bytes=400000 end_time=968206593417764 duration=33761 ns codeptr=0x1553093054bb
rec=0x1654e08 type=10 (Target kernel) time=968206595483767 thread_id=0 target_id=0x8000000000000001 host_op_id=0x8000000000000005 requested_num_teams=1 granted_num_teams=1 end_time=968206596836141 duration=1352374 ns
Executing buffer complete callback: 0 0x1654da0 0 (nil) 1
Deallocated 0x1654da0
Executing buffer complete callback: 0 0x1653640 208 0x1653640 0
rec=0x1653640 type=9 (Target data op) time=968206596860942 thread_id=0 target_id=0x8000000000000001 host_op_id=0x8000000000000006 optype=3 src_addr=0x154afd882000 src_device=0 dest_addr=0x7ffde9b7ea70 dest_device=8 bytes=400000 end_time=968206596895024 duration=34082 ns codeptr=0x1553093068e3
rec=0x16536a8 type=9 (Target data op) time=968206596915185 thread_id=0 target_id=0x8000000000000001 host_op_id=0x8000000000000007 optype=3 src_addr=0x154afd820000 src_device=0 dest_addr=0x7ffde9be04f0 dest_device=8 bytes=400000 end_time=968206596947826 duration=32641 ns codeptr=0x1553093068e3
Executing buffer complete callback: 0 0x1653640 0 (nil) 1
Deallocated 0x1653640
Executing buffer complete callback: 0 0x16539a0 208 0x16539a0 0
rec=0x16539a0 type=9 (Target data op) time=968206596955345 thread_id=0 target_id=0x8000000000000001 host_op_id=0x8000000000000008 optype=4 src_addr=0x154afd882000 src_device=0 dest_addr=(nil) dest_device=-1 bytes=0 end_time=968206596957085 duration=1740 ns codeptr=0x155309306100
rec=0x1653a08 type=9 (Target data op) time=968206596965845 thread_id=0 target_id=0x8000000000000001 host_op_id=0x8000000000000009 optype=4 src_addr=0x154afd820000 src_device=0 dest_addr=(nil) dest_device=-1 bytes=0 end_time=968206596966285 duration=440 ns codeptr=0x155309306100
Executing buffer complete callback: 0 0x16539a0 0 (nil) 1
Deallocated 0x16539a0
Executing buffer complete callback: 0 0x1655450 104 0x1655450 0
rec=0x1655450 type=8 (Target task) time=0 thread_id=0 target_id=0x8000000000000001 kind=1 endpoint=2 device=0 task_id=0 codeptr=0x228488
Callback Target EMI: kind=1 endpoint=1 device_num=0 task_data=0x1121d40 (0x0) target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) code=0x228739
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000b) src=0x7ffde9be04f0 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x15530930462b
Allocated 256 bytes at 0x1655590 in buffer request callback
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000b) src=0x7ffde9be04f0 src_device_num=8 dest=0x154afd820000 dest_device_num=0 bytes=400000 code=0x15530930462b
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000c) src=0x7ffde9be04f0 src_device_num=8 dest=0x154afd820000 dest_device_num=0 bytes=400000 code=0x1553093054bb
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000c) src=0x7ffde9be04f0 src_device_num=8 dest=0x154afd820000 dest_device_num=0 bytes=400000 code=0x1553093054bb
  Callback DataOp EMI: endpoint=1 optype=1 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000d) src=0x7ffde9b7ea70 src_device_num=8 dest=(nil) dest_device_num=0 bytes=400000 code=0x15530930462b
Allocated 256 bytes at 0x1655760 in buffer request callback
  Callback DataOp EMI: endpoint=2 optype=1 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000d) src=0x7ffde9b7ea70 src_device_num=8 dest=0x154afd882000 dest_device_num=0 bytes=400000 code=0x15530930462b
  Callback DataOp EMI: endpoint=1 optype=2 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000e) src=0x7ffde9b7ea70 src_device_num=8 dest=0x154afd882000 dest_device_num=0 bytes=400000 code=0x1553093054bb
  Callback DataOp EMI: endpoint=2 optype=2 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000e) src=0x7ffde9b7ea70 src_device_num=8 dest=0x154afd882000 dest_device_num=0 bytes=400000 code=0x1553093054bb
  Callback Submit EMI: endpoint=1 req_num_teams=0 target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000e)
Allocated 256 bytes at 0x1653080 in buffer request callback
  Callback Submit EMI: endpoint=2 req_num_teams=0 target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000e)
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000f) src=0x154afd882000 src_device_num=0 dest=0x7ffde9b7ea70 dest_device_num=8 bytes=400000 code=0x1553093068e3
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x800000000000000f) src=0x154afd882000 src_device_num=0 dest=0x7ffde9b7ea70 dest_device_num=8 bytes=400000 code=0x1553093068e3
  Callback DataOp EMI: endpoint=1 optype=3 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x8000000000000010) src=0x154afd820000 src_device_num=0 dest=0x7ffde9be04f0 dest_device_num=8 bytes=400000 code=0x1553093068e3
Allocated 256 bytes at 0x16533e0 in buffer request callback
  Callback DataOp EMI: endpoint=2 optype=3 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x8000000000000010) src=0x154afd820000 src_device_num=0 dest=0x7ffde9be04f0 dest_device_num=8 bytes=400000 code=0x1553093068e3
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x8000000000000011) src=0x154afd882000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x155309306100
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x8000000000000011) src=0x154afd882000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x155309306100
  Callback DataOp EMI: endpoint=1 optype=4 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x8000000000000012) src=0x154afd820000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x155309306100
Allocated 256 bytes at 0x1657110 in buffer request callback
  Callback DataOp EMI: endpoint=2 optype=4 target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) host_op_id=0x155309041740 (0x8000000000000012) src=0x154afd820000 src_device_num=0 dest=(nil) dest_device_num=-1 bytes=0 code=0x155309306100
Callback Target EMI: kind=1 endpoint=2 device_num=0 task_data=0x1121d40 (0x0) target_task_data=0x1123118 (0x0) target_data=0x155309041798 (0x800000000000000a) code=0x228739
Success
Callback Fini: device_num=0
```

</details>


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Here's the used version of ROCm 6.1 RC:

```console
$ amdclang --version
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.0 24075 ebda2d525e447354b65c646df27f0289927b5fbe)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.1.0/lib/llvm/bin
Configuration file: /opt/rocm-6.1.0/lib/llvm/bin/clang.cfg
$ apt search rocm-llvm
Sorting... Done
Full Text Search... Done
rocm-llvm/jammy,now 17.0.0.24075.60100-28~22.04 amd64 [installed,automatic]
  ROCm core compiler
[...]
```

---

## 评论 (4 条)

### 评论 #1 — dhruvachak (2024-03-08T17:53:17Z)

The regression has been fixed. Thanks for reporting it @Thyre 

---

### 评论 #2 — Thyre (2024-03-11T09:53:33Z)

Thanks for the update. I will close the issue once the fix has landed in a RC I have access to.

---

### 评论 #3 — oscarbg (2024-03-24T12:03:23Z)

how to obtain/test ROCm 6.1 RC? is under NDA? thanks..

---

### 评论 #4 — Thyre (2024-03-24T13:05:50Z)

> how to obtain/test ROCm 6.1 RC? is under NDA? thanks..

ROCm 6.1 is currently not publicly available and there is no official way to obtain the release candidates for testing.
The newest available release is ROCm 6.0.2. 

---

The issue seems to be fixed in:

```
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.0 24095 dd8a9741464a2adf616a8ca3cc75494392c26db3)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/apps/software/ROCm/6.1.0/lib/llvm/bin
Configuration file: /opt/apps/software/ROCm/6.1.0/lib/llvm/bin/clang.cfg
```

Thanks for looking into the issue! Will close this issue and do further investigation in the coming days, to ensure that there are no further regressions or bugs previously seen in AOMP. 

---
