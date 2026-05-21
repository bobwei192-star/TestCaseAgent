# [Feature]: Support 64-bit global work size in OpenCL

> **Issue #5524**
> **状态**: open
> **创建时间**: 2025-10-15T17:08:05Z
> **更新时间**: 2025-10-31T15:41:33Z
> **作者**: ProjectPhysX
> **标签**: Feature Request, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5524

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: assessed** (颜色: #e6d813)

## 负责人

- zichguan-amd

## 描述

### Problem Description

AMD's OpenCL driver fails to dispatch kernels with 64-bit global range >2³² (>4 billion threads), making the kernel throw OpenCL error -63.

Impact: Due to this bug, FluidX3D simulations on Instinct MI355X will not work with VRAM allocation >225GB. The full 288GB VRAM capacity cannot be used. Other software will potentially also be broken.

### Operating System

Linux, Windows

### CPU

AMD EPYC, Intel Core i7-8700K

### GPU

reproduced on AMD Instinct MI355X and AMD RX 7700 XT

### ROCm Version

latest as of today

### ROCm Component

ROCR-Runtime

### Steps to Reproduce

To reproduce:
0. You need an AMD GPU with at least 6GB VRAM.
1. `git clone https://github.com/ProjectPhysX/OpenCL-Wrapper.git`
2. modify `src/main.cpp` to
```c
#include "opencl.hpp"

int main() {
	Device device(select_device_with_most_flops()); // compile OpenCL C code for the fastest available device
	
	//const ulong N = 4ull*1024ull*1024ull*1024ull-64ull; // works
	const ulong N = 4ull*1024ull*1024ull*1024ull+64ull; // broken

	Memory<char> A(device, N); // allocate memory on both host and device
	Kernel add_kernel(device, N, "add_kernel", A); // kernel that runs on the device

	print_info("Value before kernel execution: A[0] = "+to_string((int)A[0]));
	A.write_to_device(); // copy data from host memory to device memory
	add_kernel.run(); // run add_kernel on the device
	A.read_from_device(); // copy data from device memory to host memory
	print_info("Value after kernel execution: A[0] = "+to_string((int)A[0]));

	wait();
	return 0;
}
```
3. modify `src/kernel.cpp` to
```c
#include "kernel.hpp" // note: unbalanced round brackets () are not allowed and string literals can't be arbitrarily long, so periodically interrupt with )+R(
string opencl_c_container() { return R( // ########################## begin of OpenCL C code ####################################################################

kernel void add_kernel(global char* A) {
	A[get_global_id(0)] = 7;
}

);} // ############################################################### end of OpenCL C code #####################################################################
```
4. Compile and run (on Linux via `./make.sh`, on Windows via Visual Studio Community)
5. expected output: 7, output for N>2³²: kernel errors with OpenCL error code -63

Can be reproduced on both Linux and Windows with lartest drivers as of today.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Please add OpenCL to "ROCm Component" field!

---

## 评论 (7 条)

### 评论 #1 — nicholasmalaya (2025-10-15T20:18:26Z)

This is a good bug report, and I do agree with the assessment that this sounds like a classic unsigned int 32: 2^32: 4,294,967,296 is close to the 4 billion threads mentioned above. 

---

### 评论 #2 — zichguan-amd (2025-10-22T19:08:17Z)

Hi @ProjectPhysX, thanks for reporting it. >32 bit is not supported at the moment, regardless of the device capability.  https://github.com/ROCm/rocm-systems/blob/e453705d9bea47f0a8b8ae9a2fe8fe868005af52/projects/clr/opencl/amdocl/cl_execute.cpp#L234-L238. I think this is due to an HSA limitation https://github.com/ROCm/rocm-systems/blob/e453705d9bea47f0a8b8ae9a2fe8fe868005af52/projects/rocr-runtime/runtime/hsa-runtime/inc/hsa.h#L3004

---

### 评论 #3 — ProjectPhysX (2025-10-23T02:00:05Z)

Hi @zichguan-amd, I'm aware of that. I'm asking to make 64-bit support happen. AMD GPUs now have 288GB VRAM capacity. 32-bit kernel range limitation is not contemporary anymore. Workloads are only going to get larger, and soon other applications will run into this issue.

---

### 评论 #4 — zichguan-amd (2025-10-23T15:16:28Z)

I see, this needs more discussion on how to implement it. The limitation comes from the HSA spec that only reserves 32 bits for the workgroup size in AQL packets. I'll turn this issue into a feature request and bring it up internally.

---

### 评论 #5 — zichguan-amd (2025-10-30T15:06:20Z)

Hi @ProjectPhysX, after some internal discussions, the consensus was to use kernel striding to build scalable and flexible kernels instead of increasing the limit. Here is an example of the suggested approach in CUDA https://developer.nvidia.com/blog/cuda-pro-tip-write-flexible-kernels-grid-stride-loops/. And similarly in OpenCL:
```
// main.cpp
int main() {
	Device device(select_device_with_most_flops()); // compile OpenCL C code for the fastest available device

	const ulong GRID_SIZE = 4ull*1024ull*1024ull*1024ull-64ull;
	const ulong N = GRID_SIZE*2; // problem size
 
	Memory<float> A(device, N); // allocate memory on both host and device
	Memory<float> B(device, N);
	Memory<float> C(device, N);

	Kernel add_kernel(device, GRID_SIZE, (N-GRID_SIZE)/GRID_SIZE + 1, "add_kernel", N, A, B, C); // kernel that runs on the device

	A[N-1] = 3.0f; // initialize memory
	B[N-1] = 2.0f;
	C[N-1] = 1.0f;

	print_info("Value before kernel execution: C[" + to_string(N-1) +"] = "+to_string(C[N-1]));

	A.write_to_device(); // copy data from host memory to device memory
	B.write_to_device();
	add_kernel.run(); // run add_kernel on the device
	C.read_from_device(); // copy data from device memory to host memory

	print_info("Value after kernel execution: C[" + to_string(N-1) +"] = "+to_string(C[N-1]));

	wait();
	return 0;
}

// kernel.cpp
kernel void add_kernel(ulong N, global float* A, global float* B, global float* C) {
	size_t global_id = get_global_id(0);
	size_t global_size = get_global_size(0);

	for(size_t i = global_id; i < N; i += global_size) {
		C[i] = A[i]+B[i];
	}
}
```
This allows kernels to launch for any problem size and reduces the overhead of launching new workgroups since the kernel is kept alive to work on a broader range of indices. The real-world workload is likely to be memory-bound with the VRAM usage you mentioned, we get the same memory efficiency and can still saturate the memory bandwidth with this approach. 

Please let me know if this is suited for your workload and if there's additional concerns or questions.

---

### 评论 #6 — ProjectPhysX (2025-10-31T06:31:30Z)

Hi @zichguan-amd, this is a good workaround but not a satisactory solution. I'd have to modify all kernels and add another magic tuning parameter. And the workaround somewhat obfuscates the mechanism to set kernel range on host side.
Intel already supports 64-bit `get_global_id` on both GPU and CPU, and Nvidia will support it in next driver release. You can do it too!

---

### 评论 #7 — zichguan-amd (2025-10-31T15:41:33Z)

Thanks for the feedback. I'll pass it to internal teams to keep the discussion going. Also marked the issue for internal awareness.

---
