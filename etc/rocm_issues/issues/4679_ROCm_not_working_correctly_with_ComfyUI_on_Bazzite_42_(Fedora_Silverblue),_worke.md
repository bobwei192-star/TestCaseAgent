# ROCm not working correctly with ComfyUI on Bazzite 42 (Fedora Silverblue), worked fine on Bazzite 41

> **Issue #4679**
> **状态**: closed
> **创建时间**: 2025-04-24T09:41:27Z
> **更新时间**: 2025-04-28T13:08:44Z
> **关闭时间**: 2025-04-28T13:08:43Z
> **作者**: BTekV4
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4679

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### **Title:** 
ROCm not working correctly with ComfyUI on Bazzite 42 (Fedora Silverblue), worked fine on Bazzite 41

### **Description:**
 After upgrading from Bazzite 41 (March 31, 2025 version) to Bazzite 42 (Fedora Silverblue-based), ComfyUI no longer works properly with ROCm on my AMD Radeon RX 6800 XT (gfx1030). It was working flawlessly on Bazzite 41.

![Image](https://github.com/user-attachments/assets/98c9cc43-bc09-4b57-8415-6d62078946bb)

Additionally, other software such as Automatic1111, SD Next, and Kohya_ss also fail to work correctly with ROCm on Bazzite 42. These applications were functioning without issues on Bazzite 41.

Now, when I run a workflow in ComfyUI, it gets stuck at 0% for several minutes. However, rocm-smi reports 99% GPU usage, suggesting the GPU is doing something — but no progress is made and no image is produced.

### **System Info:**

OS: Bazzite 42 (based on Fedora Silverblue)
Kernel: 6.14.3-101.bazzite.fc42.x86_64
GPU: AMD Radeon RX 6800 XT (gfx1030)
ROCm version: 6.3.1
ComfyUI version: 0.3.29
Python version: 3.10.11
Session type: Wayland ($XDG_SESSION_TYPE=wayland)
Package manager: rpm-ostree (not using DNF)

### **Installed ROCm/Mesa packages:**

rpm -qa | grep -E 'mesa|rocm'

mesa-libGLU-9.0.3-6.fc42.x86_64
mesa-libxatracker-25.0.2-1.fc42.x86_64
mesa-filesystem-25.0.4-1.fc42.x86_64
mesa-libgbm-25.0.4-1.fc42.x86_64
mesa-dri-drivers-25.0.4-1.fc42.x86_64
mesa-libGL-25.0.4-1.fc42.x86_64
mesa-libEGL-25.0.4-1.fc42.x86_64
mesa-vulkan-drivers-25.0.4-1.fc42.x86_64
mesa-va-drivers-25.0.4-1.fc42.x86_64
rocm-llvm-filesystem-18-37.rocm6.3.1.fc42.x86_64
rocm-libc++-18-37.rocm6.3.1.fc42.x86_64
rocm-llvm-libs-18-37.rocm6.3.1.fc42.x86_64
rocm-clang-libs-18-37.rocm6.3.1.fc42.x86_64
rocm-lld-18-37.rocm6.3.1.fc42.x86_64
rocm-llvm-18-37.rocm6.3.1.fc42.x86_64
rocm-llvm-devel-18-37.rocm6.3.1.fc42.x86_64
rocm-llvm-static-18-37.rocm6.3.1.fc42.x86_64
rocm-libc++-devel-18-37.rocm6.3.1.fc42.x86_64
rocm-clang-runtime-devel-18-37.rocm6.3.1.fc42.x86_64
rocm-clinfo-6.3.1-3.fc42.x86_64
rocm-comgr-18-37.rocm6.3.1.fc42.x86_64
rocm-runtime-6.3.1-4.fc42.x86_64
rocm-clang-18-37.rocm6.3.1.fc42.x86_64
rocm-clang-devel-18-37.rocm6.3.1.fc42.x86_64
rocm-device-libs-18-37.rocm6.3.1.fc42.x86_64
hipcc-18-37.rocm6.3.1.fc42.x86_64
rocm-hip-6.3.1-3.fc42.x86_64
rocm-opencl-6.3.1-3.fc42.x86_64
rocm-smi-6.3.1-3.fc42.x86_64

### **rocm-clinfo:**

Number of platforms:				 1
  Platform Profile:				 FULL_PROFILE
  Platform Version:				 OpenCL 2.1 AMD-APP (3635.0)
  Platform Name:				 AMD Accelerated Parallel Processing
  Platform Vendor:				 Advanced Micro Devices, Inc.
  Platform Extensions:				 cl_khr_icd cl_amd_event_callback 


  Platform Name:				 AMD Accelerated Parallel Processing
Number of devices:				 1
  Device Type:					 CL_DEVICE_TYPE_GPU
  Vendor ID:					 1002h
  Board name:					 AMD Radeon RX 6800 XT
  Device Topology:				 PCI[ B#12, D#0, F#0 ]
  Max compute units:				 36
  Max work items dimensions:			 3
    Max work items[0]:				 1024
    Max work items[1]:				 1024
    Max work items[2]:				 1024
  Max work group size:				 256
  Preferred vector width char:			 4
  Preferred vector width short:			 2
  Preferred vector width int:			 1
  Preferred vector width long:			 1
  Preferred vector width float:			 1
  Preferred vector width double:		 1
  Native vector width char:			 4
  Native vector width short:			 2
  Native vector width int:			 1
  Native vector width long:			 1
  Native vector width float:			 1
  Native vector width double:			 1
  Max clock frequency:				 2575Mhz
  Address bits:					 64
  Max memory allocation:			 14588628168
  Image support:				 Yes
  Max number of images read arguments:		 128
  Max number of images write arguments:		 8
  Max image 2D width:				 16384
  Max image 2D height:				 16384
  Max image 3D width:				 16384
  Max image 3D height:				 16384
  Max image 3D depth:				 8192
  Max samplers within kernel:			 16
  Max size of kernel argument:			 1024
  Alignment (bits) of base address:		 2048
  Minimum alignment (bytes) for any datatype:	 128
  Single precision floating point capability
    Denorms:					 Yes
    Quiet NaNs:					 Yes
    Round to nearest even:			 Yes
    Round to zero:				 Yes
    Round to +ve and infinity:			 Yes
    IEEE754-2008 fused multiply-add:		 Yes
  Cache type:					 Read/Write
  Cache line size:				 128
  Cache size:					 16384
  Global memory size:				 17163091968
  Constant buffer size:				 14588628168
  Max number of constant args:			 8
  Local memory type:				 Local
  Local memory size:				 65536
  Max pipe arguments:				 16
  Max pipe active reservations:			 16
  Max pipe packet size:				 1703726280
  Max global variable size:			 14588628168
  Max global variable preferred total size:	 17163091968
  Max read/write image args:			 64
  Max on device events:				 1024
  Queue on device max size:			 8388608
  Max on device queues:				 1
  Queue on device preferred size:		 262144
  SVM capabilities:				 
    Coarse grain buffer:			 Yes
    Fine grain buffer:				 Yes
    Fine grain system:				 No
    Atomics:					 No
  Preferred platform atomic alignment:		 0
  Preferred global atomic alignment:		 0
  Preferred local atomic alignment:		 0
  Kernel Preferred work group size multiple:	 32
  Error correction support:			 0
  Unified memory for Host and Device:		 0
  Profiling timer resolution:			 1
  Device endianess:				 Little
  Available:					 Yes
  Compiler available:				 Yes
  Execution capabilities:				 
    Execute OpenCL kernels:			 Yes
    Execute native function:			 No
  Queue on Host properties:				 
    Out-of-Order:				 No
    Profiling :					 Yes
  Queue on Device properties:				 
    Out-of-Order:				 Yes
    Profiling :					 Yes
  Platform ID:					 0x7f0d86308900
  Name:						 gfx1030
  Vendor:					 Advanced Micro Devices, Inc.
  Device OpenCL C version:			 OpenCL C 2.0 
  Driver version:				 3635.0 (HSA1.1,LC)
  Profile:					 FULL_PROFILE
  Version:					 OpenCL 2.0 
  Extensions:					 cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_depth_images cl_amd_copy_buffer_p2p cl_amd_assembly_program 

### **What works:**

ROCm tools correctly detect the GPU.
rocm-smi shows high usage (99%) while ComfyUI is supposedly working.
All relevant ROCm libraries are installed, and PyTorch is using torch==2.7.0+rocm6.2.4.

### **What doesn’t work:**

ComfyUI appears frozen when generating images — no progress beyond 0%.

**Output in ComfyUI terminal logs stops here:**


[START] Security scan
[DONE] Security scan
## ComfyUI-Manager: installing dependencies done.
** ComfyUI startup time: 2025-04-24 11:03:57.224
** Platform: Linux
** Python version: 3.10.11 (main, May  7 2023, 19:26:31) [Clang 16.0.3 ]
** Python executable: /var/home/maurizio/AppImages/Data/Packages/ComfyUI/venv/bin/python3
** ComfyUI Path: /var/home/maurizio/AppImages/Data/Packages/ComfyUI
** ComfyUI Base Folder Path: /var/home/maurizio/AppImages/Data/Packages/ComfyUI
** User directory: /var/home/maurizio/AppImages/Data/Packages/ComfyUI/user
** ComfyUI-Manager config path: /var/home/maurizio/AppImages/Data/Packages/ComfyUI/user/default/ComfyUI-Manager/config.ini
** Log path: /var/home/maurizio/AppImages/Data/Packages/ComfyUI/user/comfyui.log

Prestartup times for custom nodes:
   0.0 seconds: /var/home/maurizio/AppImages/Data/Packages/ComfyUI/custom_nodes/rgthree-comfy
   1.2 seconds: /var/home/maurizio/AppImages/Data/Packages/ComfyUI/custom_nodes/ComfyUI-Manager

Checkpoint files will always be loaded safely.
Total VRAM 16368 MB, total RAM 48060 MB
pytorch version: 2.7.0+rocm6.2.4
AMD arch: gfx1030
Set vram state to: HIGH_VRAM
Device: cuda:0 AMD Radeon Graphics : native
Using split optimization for attention
Python version: 3.10.11 (main, May  7 2023, 19:26:31) [Clang 16.0.3 ]
ComfyUI version: 0.3.29
ComfyUI frontend version: 1.17.11
[Prompt Server] web root: /var/home/maurizio/AppImages/Data/Packages/ComfyUI/venv/lib/python3.10/site-packages/comfyui_frontend_package/static

Starting server

To see the GUI go to: http://127.0.0.1:8188
got prompt
model weight dtype torch.float16, manual cast: None
model_type EPS

Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.float16
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cpu, dtype: torch.float16
loaded diffusion model directly to GPU
Requested to load BaseModel
loaded completely 9.5367431640625e+25 1639.406135559082 True
Requested to load SD1ClipModel
loaded completely 9.5367431640625e+25 235.84423828125 True
  0%|          | 0/20 [00:00<?, ?it/s]

**After 2 hours (It normally takes a few seconds):**
 10%|█         | 2/20 [17:36<3:06:14, 620.82s/it]

### **rocm-smi:**

ROCm System Management Interface:
- **Device**: 0
- **Node IDs**: 1
- **Device ID**: 0x73bf
- **GUID**: 22705
- **Temp (Edge)**: 50.0°C
- **Power (Avg)**: 37.0W
- **Partitions (Mem, Compute, ID)**: N/A, N/A, 0
- **SCLK**: 2445Mhz
- **MCLK**: 456Mhz
- **Fan**: 0%
- **Perf**: auto
- **PwrCap**: 300.0W
- **VRAM Usage**: 32%
- **GPU Usage**: 99%

End of ROCm SMI Log


### **Steps to Reproduce:**

Install Bazzite 42 (Fedora Silverblue-based)
Install ComfyUI with ROCm support (via StabilityMatrix or manual setup)
Launch a workflow and attempt to generate an image

### **Expected behavior:**
 
ComfyUI should be able to fully utilize the AMD GPU through ROCm to render images, as it did in Bazzite 41.

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2025-04-24T14:47:01Z)

Hi @BTekV4. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-04-24T18:06:27Z)

Hi @BTekV4, thanks for reaching out! I am sorry that you are experiencing issues with ROCm. 

Can you please set env variable AMD_LOG_LEVEL=7 and attach the outputs near where it gets stuck? 

Please keep in mind that Fedora is not an officially supported OS for ROCm and maintains its own fork. It might help to bring the issue to their attention as well.

Thanks! 

---

### 评论 #3 — BTekV4 (2025-04-25T14:51:21Z)

> Hi [@BTekV4](https://github.com/BTekV4), thanks for reaching out! I am sorry that you are experiencing issues with ROCm.
> 
> Can you please set env variable AMD_LOG_LEVEL=7 and attach the outputs near where it gets stuck?
> 
> Please keep in mind that Fedora is not an officially supported OS for ROCm and maintains its own fork. It might help to bring the issue to their attention as well.
> 
> Thanks!

Hi, I let main.py run with AMD_LOG_LEVEL=7 enabled for 3 minutes and 30 seconds using timeout, and captured the output to a log file.

Let me know if you'd like a shorter or longer run, or if there's any specific part of the log you'd like me to highlight!

[rocm_debug.log](https://github.com/user-attachments/files/19911190/rocm_debug.log)

---

### 评论 #4 — tcgu-amd (2025-04-25T17:53:39Z)

@BTekV4 Thanks for the update! Looks like the CPU tried to initialize a memory copy operation to the GPU and never got a confirmation for the completion of the operation. This is likely a driver-level issue, and given that it hasn't happened on Bazzite 41, my guess is that the kernel packaged with Bazzite 42 is causing trouble for the amdgpu-dkms module which ROCm relies on. 

The kernel version for Bazzite 42 seems to be 6.14, which is quite far ahead of 6.11, the latest supported by ROCm. Using newer kernels tends to lead to bugs like these, and we can't really fix them unless we provide support for the particular kernel version. Unfortunately, this means that there's not much more we can do at the moment because if the kernel were going to be supported, it would likely already be a work-in-progress, and if it were not going to be supported, this likely wouldn't change that. 

At this point, reverting to the Bazzite version that works seems to be our best option.

Sorry for not being able to offer a more immediate solution, and thanks again for the update.

---

### 评论 #5 — BTekV4 (2025-04-27T15:35:52Z)

@tcgu-amd  Yes, going back to a previous version of the kernel (Linux 6.13.7-108.bazzite.fc42.x86_64) it is back to working properly, thanks a lot for the help

---

### 评论 #6 — tcgu-amd (2025-04-28T13:08:43Z)

@BTekV4 No problem! Glad it worked! 

---
