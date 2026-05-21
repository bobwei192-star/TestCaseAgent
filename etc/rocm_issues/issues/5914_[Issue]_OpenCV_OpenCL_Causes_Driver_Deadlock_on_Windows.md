# [Issue]: OpenCV OpenCL Causes Driver Deadlock on Windows

> **Issue #5914**
> **状态**: closed
> **创建时间**: 2026-01-29T16:22:57Z
> **更新时间**: 2026-02-25T16:15:05Z
> **关闭时间**: 2026-02-25T14:26:11Z
> **作者**: yanite
> **标签**: Windows, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5914

## 标签

- **Windows** (颜色: #c2e0c6)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

When using OpenCV (Python or C++) in a Windows environment to initialize OpenCL devices (specifically AMD Radeon RX 7000 series GPUs), the application enters an indefinite deadlock state, failing to create the OpenCL context.

### Operating System

Windows 24H2 26100.7623

### CPU

AMD Ryzen 9 7950X 16-Core Processor

### GPU

AMD Radeon RX 7900 XTX [Driver 26.1.1]

### ROCm Version

7.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Reproduction Steps
Execute standard OpenCV OpenCL detection code (e.g., cv.ocl.haveOpenCL() or cv::ocl::getPlatfomsInfo()).
The program hangs indefinitely while attempting to interface with the AMD OpenCL ICD loader.
Expected Result
The program should successfully enumerate all OpenCL platforms and devices and return control.
Actual Result/Issue
The program deadlocks and becomes unresponsive, requiring a forced termination. Internal OpenCV logs stop during the context creation phase, as the driver function call does not return.
Attempted Solutions
The following methods were attempted without success:
No OPENCV_OPENCL_DEVICE environment variable set: Program deadlocks.
Setting OPENCV_OPENCL_DEVICE=DISABLED: Program runs without deadlocking (but with OpenCL disabled), confirming the issue is specific to the OpenCL initialization phase.
Attempting to specify a specific device (AMD:GPU:0): Program deadlocks.
Clearing OpenCV cache files: No effect.
Reproduced in both Python and C++ bindings: Both environments trigger the same issue.
Stack Trace
According to C++ debugger analysis, the deadlock consistently occurs within the following driver module and function (the function call does not return):
amdocl64.dll!clSetKernelExecInfo+0x503279 (0x7ffdf4f0c6d9)
C:\Windows\System32\DriverStore\FileRepository\amdocl.inf_amd64_71fdb5a0a9dd7076\amdocl64.dll
... (other memory addresses omitted) ...
The issue appears to be a deadlock within the AMD OpenCL driver when processing multi-platform/device enumeration requests.
Would you like me to draft the reproduction code snippet in C++ to include with this report?

---

## 评论 (7 条)

### 评论 #1 — yanite (2026-01-30T14:29:13Z)

This bug is really confusing. I've already cleaned up the drivers and reinstalled them, and I've also looked at the relevant OpenCV code—it doesn't seem to have any obvious issues.

<img width="1022" height="643" alt="Image" src="https://github.com/user-attachments/assets/f0c589ec-7134-4991-993f-16e9baae0350" />

---

### 评论 #2 — schung-amd (2026-01-30T16:22:10Z)

Hi @yanite, thanks for the report, I'll look into it.

> Would you like me to draft the reproduction code snippet in C++ to include with this report?

Reproducer code would be great. `clinfo` output might also be helpful.

---

### 评论 #3 — yanite (2026-01-30T17:00:18Z)

`#define CL_TARGET_OPENCL_VERSION 200
#include <CL/cl.h>
#include <iostream>
#include <vector>

const char* programSource = 
"__kernel void vectorAdd(__global const float *A, __global const float *B, __global float *C) {"
"    int gid = get_global_id(0);"
"    C[gid] = A[gid] + B[gid];"
"}";

int main() {
    // 初始化数据
    const int elements = 1024;
    std::vector<float> A(elements, 1.0f);
    std::vector<float> B(elements, 2.0f);
    std::vector<float> C(elements, 0.0f);

    // 获取平台ID和设备ID
    cl_platform_id platformId = nullptr;
    cl_device_id deviceId = nullptr;
    cl_uint numPlatforms;
    cl_uint numDevices;

    clGetPlatformIDs(1, &platformId, &numPlatforms);
    clGetDeviceIDs(platformId, CL_DEVICE_TYPE_GPU, 1, &deviceId, &numDevices);

    // 创建上下文
    cl_context context = clCreateContext(nullptr, 1, &deviceId, nullptr, nullptr, nullptr);

    // 创建命令队列（这里设置了QUEUE_PROPERTIES）
    cl_int status;
    cl_command_queue commandQueue = clCreateCommandQueue(context, deviceId,
        CL_QUEUE_PROFILING_ENABLE, // 示例中使用了 profiling 属性
        &status);

    if (status != CL_SUCCESS) {
        std::cerr << "Failed to create command queue." << std::endl;
        return -1;
    }

    // 创建内存对象
    cl_mem aBuffer = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
        sizeof(float) * elements, A.data(), &status);
    cl_mem bBuffer = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
        sizeof(float) * elements, B.data(), &status);
    cl_mem cBuffer = clCreateBuffer(context, CL_MEM_WRITE_ONLY,
        sizeof(float) * elements, nullptr, &status);

    // 创建程序并构建
    cl_program program = clCreateProgramWithSource(context, 1, &programSource, nullptr, &status);
    status = clBuildProgram(program, 1, &deviceId, nullptr, nullptr, nullptr);

    // 创建内核
    cl_kernel kernel = clCreateKernel(program, "vectorAdd", &status);

    // 设置内核参数
    status = clSetKernelArg(kernel, 0, sizeof(cl_mem), &aBuffer);
    status |= clSetKernelArg(kernel, 1, sizeof(cl_mem), &bBuffer);
    status |= clSetKernelArg(kernel, 2, sizeof(cl_mem), &cBuffer);

    // 执行内核
    size_t globalSize = elements;
    status = clEnqueueNDRangeKernel(commandQueue, kernel, 1, nullptr, &globalSize, nullptr, 0, nullptr, nullptr);

    // 读取输出
    status = clEnqueueReadBuffer(commandQueue, cBuffer, CL_TRUE, 0, sizeof(float) * elements, C.data(), 0, nullptr, nullptr);

    // 清理资源
    clReleaseMemObject(aBuffer);
    clReleaseMemObject(bBuffer);
    clReleaseMemObject(cBuffer);
    clReleaseProgram(program);
    clReleaseKernel(kernel);
    clReleaseCommandQueue(commandQueue);
    clReleaseContext(context);

    // 输出结果检查
    for(int i = 0; i < 5; ++i) { // 只打印前五个元素作为验证
        std::cout << "C[" << i << "] = " << C[i] << std::endl;
    }

    return 0;
}`
`
clang++ vector_add_opencl.cpp -IU:\cpp\opencv\opencv\3rdparty\include\opencl\1.2\ -LU:\cpp_libs\OpenCL-ICD-Loader\build\RelWithDebInfo -lOpenCL
-o vector_add_opencl.exe -lOpenCL
`
Such a standard program, yet it won't run.



stop at clCreateCommandQueue


---

### 评论 #4 — yanite (2026-01-30T17:35:24Z)

$ clinfo
Number of platforms:                             1
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3652.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_khr_d3d10_sharing cl_khr_d3d11_sharing cl_khr_dx9_media_sharing cl_amd_event_callback cl_amd_offline_devices


  Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               2
  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Board name:                                    AMD Radeon RX 7900 XTX
  Device Topology:                               PCI[ B#3, D#0, F#0 ]
  Max compute units:                             48
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
  Max clock frequency:                           2482Mhz
  Address bits:                                  64
  Max memory allocation:                         21890072576
  Image support:                                 Yes
  Max number of images read arguments:           128
  Max number of images write arguments:          64
  Max image 2D width:                            16384
  Max image 2D height:                           16384
  Max image 3D width:                            2048
  Max image 3D height:                           2048
  Max image 3D depth:                            2048
  Max samplers within kernel:                    16
  Max size of kernel argument:                   1024
  Alignment (bits) of base address:              2048
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
  Global memory size:                            25753026560
  Constant buffer size:                          21890072576
  Max number of constant args:                   8
  Local memory type:                             Local
  Local memory size:                             65536
  Max pipe arguments:                            16
  Max pipe active reservations:                  16
  Max pipe packet size:                          415236096
  Max global variable size:                      19701065216
  Max global variable preferred total size:      25753026560
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



Using opencl.dll version 2.2.6.0 (the version bundled with ROCm) does not cause a hang, but it also has no effect:

$ python -c "import cv2; dev = cv2.ocl.Device.getDefault(); print(f'Selected device: {dev.name()}')"

[ERROR:0@0.194] global ocl.cpp:1006 cv::ocl::OpenCLExecutionContext::Impl::getInitializedExecutionContext OpenCL: Can't create default OpenCL queue
Selected device:
When setting OPENCV_OPENCL_DEVICE=AMD:GPU:0 and using the system-provided opencl.dll version 3.0.6.0, the program hangs exactly at the point shown above (it freezes there).
(Interestingly, how does HIP even use OpenCL?)

clint.exe clinfo also seems to have issues.

出错应用程序名称： clinfo.exe，版本： 0.0.0.0，时间戳： 0x694b6ac6
出错模块名称： amdocl64.dll， 版本： 32.0.21041.1000，时间戳： 0x695fe751
异常代码： 0xc0000005
错误偏移： 0x00000000000cef57
出错进程 ID： 0x4EC4
出错应用程序开始时间： 0x1DC920E8876FF4B
Faulting 应用程序路径： C:\WINDOWS\system32\clinfo.exe
Faulting 模块路径： C:\WINDOWS\System32\DriverStore\FileRepository\amdocl.inf_amd64_92169942827ae652\amdocl64.dll
Report ID： 2adc39ac-b1fe-45c2-a05a-738278bf6e58
Faulting 包全名： 
Faulting 程序包相对应用程序 ID：  个

---

### 评论 #5 — schung-amd (2026-02-10T21:32:35Z)

 Trying to match your environment exactly; what install methods did you use for OpenCV and the OpenCL ICD loader?

---

### 评论 #6 — yanite (2026-02-25T14:28:40Z)

Sorry  My apologies—redundant ROCm paths are triggering OpenCL errors. Specifically, the inclusion of U:\ROCm\TheRock\build\compiler\amd-llvm\build\bin is causing a version mismatch between LLVM 22.0git and LLVM 19.0, resulting in OpenCL instability.

If others encounter similar issues, try excluding the HIP path from your environment or correcting it to avoid conflicts.

---

### 评论 #7 — schung-amd (2026-02-25T16:15:05Z)

Thanks for the update, glad to hear you figured it out. Good to know that's a potential footgun to look out for in future issues.

---
