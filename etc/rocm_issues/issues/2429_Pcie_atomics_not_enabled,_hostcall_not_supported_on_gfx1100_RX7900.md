# Pcie atomics not enabled, hostcall not supported on gfx1100 RX7900

> **Issue #2429**
> **状态**: closed
> **创建时间**: 2023-09-01T14:38:17Z
> **更新时间**: 2023-12-21T16:02:53Z
> **关闭时间**: 2023-12-21T16:02:53Z
> **作者**: mergmann
> **标签**: hardware:Radeon, application:pytorch
> **URL**: https://github.com/ROCm/ROCm/issues/2429

## 标签

- **hardware:Radeon** (颜色: #2B113F)
- **application:pytorch** (颜色: #bfdadc)

## 负责人

- hongxiayang

## 描述

I tried to use pytorch with ROCm, however it fails with 
```log
:1:rocvirtual.cpp           :2902: 1550313166 us: 7740 : [tid:0x7f5681dfb6c0] Pcie atomics not enabled, hostcall not supported
:1:rocvirtual.cpp           :3235: 1550313176 us: 7740 : [tid:0x7f5681dfb6c0] AQL dispatch failed!
HIP error: the operation cannot be performed in the present state
```

From previous issues in this repository, it seems like PCIe atomics were only a problem with gfx8 GPUs and old CPUs, so I'm wondering why I have this problem. I couldn't find much information about which CPUs support this feature and which don't. Is there a compatibility list somewhere?

ROCm version: 5.6
PyTorch: version: 2.1.0.dev20230901+rocm5.6
GPU: RX 7900 XT
CPU: i5-11400F

dmesg | grep atomic
```log
amdgpu 0000:03:00.0: amdgpu: PCIE atomic ops is not supported
```

However, I don't get the infamous `kfd: PCI rejects atomics`


<details>
    <summary>lspci -tv</summary>

    -[0000:00]-+-00.0  Intel Corporation Device 4c53
               +-01.0-[01-03]----00.0-[02-03]----00.0-[03]--+-00.0  Advanced Micro Devices, Inc. [AMD/ATI] Navi 31 [Radeon RX 7900 XT/7900 XTX]
               |                                            \-00.1  Advanced Micro Devices, Inc. [AMD/ATI] Navi 31 HDMI/DP Audio
               +-06.0-[04]----00.0  Micron/Crucial Technology P5 Plus NVMe PCIe SSD
               +-14.0  Intel Corporation Tiger Lake-H USB 3.2 Gen 2x1 xHCI Host Controller
               +-14.2  Intel Corporation Tiger Lake-H Shared SRAM
               +-15.0  Intel Corporation Tiger Lake-H Serial IO I2C Controller #0
               +-16.0  Intel Corporation Tiger Lake-H Management Engine Interface
               +-17.0  Intel Corporation Device 43d2
               +-1c.0-[05]--
               +-1d.0-[06]--
               +-1f.0  Intel Corporation B560 LPC/eSPI Controller
               +-1f.3  Intel Corporation Tiger Lake-H HD Audio Controller
               +-1f.4  Intel Corporation Tiger Lake-H SMBus Controller
               +-1f.5  Intel Corporation Tiger Lake-H SPI Controller
               \-1f.6  Intel Corporation Ethernet Connection (14) I219-V
</details>
The device 00:01.0 is the PCIe x16 root port to which the GPU is connected, but it apparently does not support PCIe atomics (note the flags '32bit' and '64-bit'):

<details>
    <summary>lspci -vvvs 00:01.0</summary>

    ...
    DevCap2: Completion Timeout: Range ABC, TimeoutDis+ NROPrPrP- LTR+
                             10BitTagComp- 10BitTagReq- OBFF Via WAKE#, ExtFmt- EETLPPrefix-
                             EmergencyPowerReduction Not Supported, EmergencyPowerReductionInit-
                             FRS- LN System CLS Not Supported, TPHComp- ExtTPHComp- ARIFwd+
                             AtomicOpsCap: Routing- 32bit- 64bit- 128bitCAS-
                    DevCtl2: Completion Timeout: 50us to 50ms, TimeoutDis- LTR+ 10BitTagReq- OBFF Disabled, ARIFwd-
                             AtomicOpsCtl: ReqEn+ EgressBlck+
    ...
</details>
I tried setting those bits with a udev rule which caused the error messages to disappear, but then it just freezes whenever any ROCm operation is performed on the GPU. Is there some BIOS setting or driver configuration required to enable PCIe atomics? Or is it simply that my CPU or mainboard doesn't support them?

---

## 评论 (26 条)

### 评论 #1 — NeedsMoar (2023-09-04T12:35:15Z)

There are all kinds of reasons this might not work, especially on a consumer board, and since this is for bug reports on ROCm (and this issue is documented with consumer boards specifically mentioned as being iffy) you'd probably be way better off 
a) Asking Intel on their forums, they actually respond so you'll probably get a quick answer on CPU support
b) Asking the motherboard manufacturer if it's not one of the consumer focused ones.  Supermicro will get you extensive responses to any questions within a business day,  Tyan or Gigabyte are likely going to be pretty quick too.  OTOH Asus will never respond or respond with irrelevant garbage links to FAQ searches and you'll end up on spam mailing lists in Chinese for a cloud storage service, so use this option carefully.  
c) Try messing with IOMMU settings and any PCIe DMA mitigation settings in the BIOS that might be forcing devices to not communicate.  

I don't think switch chips necessarily show up in the tree unless something is running off of them so if there's one of those (to deal with the needed retimer as well) handling a second slot further down the board when it's populated and run both slots in x8 mode it could be a blocking component if I'm not mistaken about the visibility thing.  

If your GPU is on a riser cable so it can be mounted vertically, none of those cables are in-spec for PCIe 4.0 (usually the cable length alone is enough to violate SNR / signal strength requirements, and the ones short enough to not violate them probably still do by having the extra connection.)  and it might be getting dropped to a lower feature set because of bad signal, install directly in the PCIe slot and try again.  If that turns out to be a problem the only compliant way to manage that mounting situation is with a 2x8i oculink card in the slot the gpu was in and both cables leading to a 2x8i Oculink -> PCIe 4.0 x16 card so you get retimers in the path.   Ironically this solution is the same price as the "pretty" cables which don't and can't reliably work, but it wasn't available until recently and will probably require slight amounts of case modding to get the card with the slot lined up correctly and at the right height.

My first assumption though is that a mid to low tier consumer CPU from an era where Intel has been dropping features from their non-Xeons more and more that only supports 20 PCIe lanes might not have bothered implementing it.  There's probably not a lot of call for ensuring atomic update of memory on PCIe devices when you can install at most 3 of them connected directly to the CPU depending on the board.  The reason Haswell-E and Broadwell-E are still selling and being used was that they're really just stripped down Xeons that (most) boards disable ECC RDIMMs on (most) models of, the 6960x being an exception on some boards, so the BIOSes had all of the higher end features and you didn't have to deal with guesswork nonsense.  


---

### 评论 #2 — hongxiayang (2023-11-16T15:03:25Z)

@MattisBergmann 
This is the link that have the wheels to fix the above issue. Please try and let us know.
https://repo.radeon.com/rocm/manylinux/.private-05b1d2750b39ef78de979ed9f59ce4c6/297/

also please refer to this issue for more detailed discussion: https://github.com/pytorch/pytorch/issues/103973

---

### 评论 #3 — mergmann (2023-11-17T16:43:00Z)

I tried using that wheel with a simple python script:
```py
import torch
print(torch.version.hip)
a = torch.Tensor([1, 2, 3, 4]).cuda()
q = torch.sum(a)
print('sum:', q)
```
However, now I get a different error instead: `RuntimeError: HIP error: invalid device function`
It prints `5.7.31921-d1770ee1b` as the HIP version. Running it with `AMD_LOG_LEVEL=3` I get a lot of
```log
hipErrorNoBinaryForGpu: Unable to find code object for all current devices!
  Devices:
    amdgcn-amd-amdhsa--gfx1100 - [Not Found]
  Bundled Code Objects:
    host-x86_64-unknown-linux-- - [Unsupported]
    hipv4-amdgcn-amd-amdhsa--gfx1030 - [code object targetID is amdgcn-amd-amdhsa--gfx1030]
[out.log](https://github.com/RadeonOpenCompute/ROCm/files/13394495/out.log)

    hipv4-amdgcn-amd-amdhsa--gfx900 - [code object targetID is amdgcn-amd-amdhsa--gfx900]
    hipv4-amdgcn-amd-amdhsa--gfx906 - [code object targetID is amdgcn-amd-amdhsa--gfx906]
    hipv4-amdgcn-amd-amdhsa--gfx908 - [code object targetID is amdgcn-amd-amdhsa--gfx908]
    hipv4-amdgcn-amd-amdhsa--gfx90a - [code object targetID is amdgcn-amd-amdhsa--gfx90a]
```
Running it with `MD_LOG_LEVEL=3 HSA_OVERRIDE_GFX_VERSION="11.0.0" PYTORCH_ROCM_ARCH="gfx1100" HIP_VISIBLE_DEVICES=0` didn't change anything.
It seems to me that the wheel does not support gfx1100.

Full log:
[out.log](https://github.com/RadeonOpenCompute/ROCm/files/13394500/out.log)


---

### 评论 #4 — hongxiayang (2023-11-17T16:59:16Z)

Right, we did not build for gfx1100. For the short term, would you mind trying to build from source using below instruction I wrote in the other similar issue related to atomics. 

(1) start another terminal, start a new container of (rocm/pytorch:latest-base) with the parameters using the instruction above
```
sudo docker run -it --network=host --device=/dev/kfd --device=/dev/dri --group-add=video --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --shm-size 8G -u root rocm/pytorch:latest-base
```
(2) clone the pytorch inside your docker environment
```
git clone --recursive https://github.com/ROCmSoftwarePlatform/pytorch.git
cd pytorch
git checkout rocm57_hostcall
```
(3) run this:
```
python tools/amd_build/build_amd.py 
```
(4) run rocm-info to check your GPU GFX Arch
rocminfo

for example, gfx1100

(5) build pytorch by source (replace with your gfx arch).
```
PYTORCH_ROCM_ARCH="$YOUR_GFX_ARCH" python setup.py develop
```

(6) run the torch.sum test again.

Details:
https://github.com/pytorch/pytorch/issues/103973#issuecomment-1743678566



---

### 评论 #5 — mergmann (2023-11-17T21:02:06Z)

I compiled pytorch according to your instructions. Running a simple python program
```py
import torch
a = torch.Tensor([1, 2, 3, 4]).cuda()
print(torch.sum(a))
```
crashes my graphics driver. Sometimes the crash happens on the second line and sometimes on the third. I have to manually kill the python process, CTRL+C does not work. Also the GPU usage goes up to 100% and stays there until a system reboot.
This is similar to what I experienced with blender. As soon as I switch to the Cycles renderer, I experience driver crashes sometimes and the GPU usage goes up to 100%, core clock 2.9GHz and stays there until closing blender.

Debugging it with GDB:
```
#0  0x00007f2a9822fa7f in ?? () from target:/opt/rocm-5.7.0/lib/libhsa-runtime64.so.1
#1  0x00007f2a9822f8de in ?? () from target:/opt/rocm-5.7.0/lib/libhsa-runtime64.so.1
#2  0x00007f2a98224f59 in ?? () from target:/opt/rocm-5.7.0/lib/libhsa-runtime64.so.1
#3  0x00007f2ad0bd8395 in ?? () from target:/opt/rocm/lib/libroctracer64.so.4
#4  0x00007f2af35a0c8b in ?? () from target:/opt/rocm/hip/lib/libamdhip64.so.5
#5  0x00007f2af35a63ae in ?? () from target:/opt/rocm/hip/lib/libamdhip64.so.5
#6  0x00007f2af35d5a9a in ?? () from target:/opt/rocm/hip/lib/libamdhip64.so.5
#7  0x00007f2af35d752d in ?? () from target:/opt/rocm/hip/lib/libamdhip64.so.5
#8  0x00007f2af35d774b in ?? () from target:/opt/rocm/hip/lib/libamdhip64.so.5
#9  0x00007f2af35a303e in ?? () from target:/opt/rocm/hip/lib/libamdhip64.so.5
#10 0x00007f2af3579fb4 in ?? () from target:/opt/rocm/hip/lib/libamdhip64.so.5
#11 0x00007f2af34048aa in ?? () from target:/opt/rocm/hip/lib/libamdhip64.so.5
#12 0x00007f2af3409fb4 in hipMemcpyWithStream () from target:/opt/rocm/hip/lib/libamdhip64.so.5
#13 0x00007f2af56df23a in at::native::copy_kernel_cuda(at::TensorIterator&, bool) () from target:/pytorch/torch/lib/libtorch_hip.so
#14 0x00007f2b00c901a3 in at::native::copy_impl(at::Tensor&, at::Tensor const&, bool) () from target:/pytorch/torch/lib/libtorch_cpu.so
#15 0x00007f2b00c914aa in at::native::copy_(at::Tensor&, at::Tensor const&, bool) () from target:/pytorch/torch/lib/libtorch_cpu.so
#16 0x00007f2b01ab2302 in at::_ops::copy_::call(at::Tensor&, at::Tensor const&, bool) () from target:/pytorch/torch/lib/libtorch_cpu.so
#17 0x00007f2b00f9aa50 in at::native::_to_copy(at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) ()
   from target:/pytorch/torch/lib/libtorch_cpu.so
#18 0x00007f2b01eccdcf in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeExplicitAutograd___to_copy>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat> > >, at::Tensor (at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) () from target:/pytorch/torch/lib/libtorch_cpu.so
#19 0x00007f2b0152c959 in at::_ops::_to_copy::redispatch(c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) () from target:/pytorch/torch/lib/libtorch_cpu.so
#20 0x00007f2b01ca036a in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>), &at::(anonymous namespace)::_to_copy>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat> > >, at::Tensor (at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) () from target:/pytorch/torch/lib/libtorch_cpu.so
```

---

### 评论 #6 — mergmann (2023-11-18T15:39:29Z)

I tried torch.sum() in a python shell with AMD_LOG_LEVEL=3:
```
Python 3.9.18 (main, Sep 11 2023, 13:41:44) 
[GCC 11.2.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> a = torch.Tensor(range(8))
>>> b = a.cuda()
:3:rocdevice.cpp            :442 : 0298654226 us: [pid:16    tid:0x7f54f7603280] Initializing HSA stack.
:3:comgrctx.cpp             :33  : 0298664682 us: [pid:16    tid:0x7f54f7603280] Loading COMGR library.
:3:rocdevice.cpp            :208 : 0298664736 us: [pid:16    tid:0x7f54f7603280] Numa selects cpu agent[0]=0x492a0f0(fine=0x75f3bc0,coarse=0x7750e80) for gpu agent=0x7751460 CPU<->GPU XGMI=0
:3:rocdevice.cpp            :1680: 0298665080 us: [pid:16    tid:0x7f54f7603280] Gfx Major/Minor/Stepping: 11/0/0
:3:rocdevice.cpp            :1682: 0298665085 us: [pid:16    tid:0x7f54f7603280] HMM support: 1, XNACK: 0, Direct host access: 0
:3:rocdevice.cpp            :1684: 0298665088 us: [pid:16    tid:0x7f54f7603280] Max SDMA Read Mask: 0x0, Max SDMA Write Mask: 0x0
:3:hip_context.cpp          :48  : 0298665457 us: [pid:16    tid:0x7f54f7603280] Direct Dispatch: 1
:3:hip_device_runtime.cpp   :546 : 0298670632 us: [pid:16    tid:0x7f54f7603280]  hipGetDeviceCount ( 0x7ffcaf46b5a0 ) 
:3:hip_device_runtime.cpp   :548 : 0298670641 us: [pid:16    tid:0x7f54f7603280] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :546 : 0298670651 us: [pid:16    tid:0x7f54f7603280]  hipGetDeviceCount ( 0x7f54a5733194 ) 
:3:hip_device_runtime.cpp   :548 : 0298670654 us: [pid:16    tid:0x7f54f7603280] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_device.cpp           :381 : 0298670658 us: [pid:16    tid:0x7f54f7603280]  hipGetDeviceProperties ( 0x7ffcaf46b2c0, 0 ) 
:3:hip_device.cpp           :383 : 0298670662 us: [pid:16    tid:0x7f54f7603280] hipGetDeviceProperties: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :546 : 0298670693 us: [pid:16    tid:0x7f54f7603280]  hipGetDeviceCount ( 0x7ffcaf46b5d8 ) 
:3:hip_device_runtime.cpp   :548 : 0298670695 us: [pid:16    tid:0x7f54f7603280] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0298670704 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46b344 ) 
:3:hip_device_runtime.cpp   :539 : 0298670706 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :546 : 0298670708 us: [pid:16    tid:0x7f54f7603280]  hipGetDeviceCount ( 0x7ffcaf46b0c0 ) 
:3:hip_device_runtime.cpp   :548 : 0298670710 us: [pid:16    tid:0x7f54f7603280] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_context.cpp          :355 : 0298670857 us: [pid:16    tid:0x7f54f7603280]  hipDevicePrimaryCtxGetState ( 0, 0x7ffcaf46b158, 0x7ffcaf46b15c ) 
:3:hip_context.cpp          :369 : 0298670862 us: [pid:16    tid:0x7f54f7603280] hipDevicePrimaryCtxGetState: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0298670865 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46b3a4 ) 
:3:hip_device_runtime.cpp   :539 : 0298670867 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_context.cpp          :355 : 0298670870 us: [pid:16    tid:0x7f54f7603280]  hipDevicePrimaryCtxGetState ( 0, 0x7ffcaf46b1b8, 0x7ffcaf46b1bc ) 
:3:hip_context.cpp          :369 : 0298670872 us: [pid:16    tid:0x7f54f7603280] hipDevicePrimaryCtxGetState: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0298670877 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46b334 ) 
:3:hip_device_runtime.cpp   :539 : 0298670879 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_context.cpp          :355 : 0298670881 us: [pid:16    tid:0x7f54f7603280]  hipDevicePrimaryCtxGetState ( 0, 0x7ffcaf46b148, 0x7ffcaf46b14c ) 
:3:hip_context.cpp          :369 : 0298670883 us: [pid:16    tid:0x7f54f7603280] hipDevicePrimaryCtxGetState: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0298671139 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46b804 ) 
:3:hip_device_runtime.cpp   :539 : 0298671144 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0298671178 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46aa34 ) 
:3:hip_device_runtime.cpp   :539 : 0298671181 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0298671185 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46a914 ) 
:3:hip_device_runtime.cpp   :539 : 0298671187 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0298671195 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46a904 ) 
:3:hip_device_runtime.cpp   :539 : 0298671198 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_stream.cpp           :395 : 0298671206 us: [pid:16    tid:0x7f54f7603280]  hipDeviceGetStreamPriorityRange ( 0x7ffcaf46a6d8, 0x7ffcaf46a6dc ) 
:3:hip_stream.cpp           :403 : 0298671209 us: [pid:16    tid:0x7f54f7603280] hipDeviceGetStreamPriorityRange: Returned hipSuccess : 
:3:hip_error.cpp            :27  : 0298671215 us: [pid:16    tid:0x7f54f7603280]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :531 : 0298671219 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46a104 ) 
:3:hip_device_runtime.cpp   :539 : 0298671222 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_graph.cpp            :887 : 0298671230 us: [pid:16    tid:0x7f54f7603280]  hipStreamIsCapturing ( stream:<null>, 0x7ffcaf46a148 ) 
:3:hip_graph.cpp            :888 : 0298671233 us: [pid:16    tid:0x7f54f7603280] hipStreamIsCapturing: Returned hipSuccess : 
:3:hip_memory.cpp           :566 : 0298671241 us: [pid:16    tid:0x7f54f7603280]  hipMalloc ( 0x7ffcaf46a238, 2097152 ) 
:3:rocdevice.cpp            :2230: 0298671287 us: [pid:16    tid:0x7f54f7603280] device=0x77baaa0, freeMem_ = 0x4fee00000
:3:hip_memory.cpp           :568 : 0298671292 us: [pid:16    tid:0x7f54f7603280] hipMalloc: Returned hipSuccess : 0x7f52ad200000: duration: 51 us
:3:hip_device_runtime.cpp   :561 : 0298671300 us: [pid:16    tid:0x7f54f7603280]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0298671302 us: [pid:16    tid:0x7f54f7603280] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :561 : 0298671305 us: [pid:16    tid:0x7f54f7603280]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0298671306 us: [pid:16    tid:0x7f54f7603280] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0298671335 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46a934 ) 
:3:hip_device_runtime.cpp   :539 : 0298671337 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0298671340 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46a934 ) 
:3:hip_device_runtime.cpp   :539 : 0298671342 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_memory.cpp           :652 : 0298671349 us: [pid:16    tid:0x7f54f7603280]  hipMemcpyWithStream ( 0x7f52ad200000, 0x75edf40, 32, hipMemcpyHostToDevice, stream:<null> ) 
:3:rocdevice.cpp            :2732: 0298671354 us: [pid:16    tid:0x7f54f7603280] number of allocated hardware queues with low priority: 0, with normal priority: 0, with high priority: 0, maximum per priority is: 4
:3:rocdevice.cpp            :2810: 0298679708 us: [pid:16    tid:0x7f54f7603280] created hardware queue 0x7f53ae300000 with size 16384 with priority 1, cooperative: 0
:3:rocdevice.cpp            :2902: 0298679719 us: [pid:16    tid:0x7f54f7603280] acquireQueue refCount: 0x7f53ae300000 (1)
:3:devprogram.cpp           :2684: 0298833285 us: [pid:16    tid:0x7f54f7603280] Using Code Object V5.
:3:rocvirtual.hpp           :66  : 0298834625 us: [pid:16    tid:0x7f54f7603280] Host active wait for Signal = (0x7f53b1858800) for -1 ns
:3:hip_memory.cpp           :663 : 0298834737 us: [pid:16    tid:0x7f54f7603280] hipMemcpyWithStream: Returned hipSuccess : : duration: 163388 us
:3:hip_device_runtime.cpp   :561 : 0298834758 us: [pid:16    tid:0x7f54f7603280]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0298834760 us: [pid:16    tid:0x7f54f7603280] hipSetDevice: Returned hipSuccess : 
>>> c = torch.sum(b)
:3:hip_device_runtime.cpp   :531 : 0304627939 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46b1f4 ) 
:3:hip_device_runtime.cpp   :539 : 0304627946 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0304627952 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46af04 ) 
:3:hip_device_runtime.cpp   :539 : 0304627955 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0304627961 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46aed4 ) 
:3:hip_device_runtime.cpp   :539 : 0304627964 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :561 : 0304627976 us: [pid:16    tid:0x7f54f7603280]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0304627979 us: [pid:16    tid:0x7f54f7603280] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0304628012 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46aae4 ) 
:3:hip_device_runtime.cpp   :539 : 0304628015 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device.cpp           :381 : 0304628022 us: [pid:16    tid:0x7f54f7603280]  hipGetDeviceProperties ( 0x7ffcaf46a7b0, 0 ) 
:3:hip_device.cpp           :383 : 0304628026 us: [pid:16    tid:0x7f54f7603280] hipGetDeviceProperties: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0304628029 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46aaf4 ) 
:3:hip_device_runtime.cpp   :539 : 0304628032 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0304628035 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46aaf4 ) 
:3:hip_device_runtime.cpp   :539 : 0304628040 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0304628044 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46a7f4 ) 
:3:hip_device_runtime.cpp   :539 : 0304628047 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0304628051 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46a7f4 ) 
:3:hip_device_runtime.cpp   :539 : 0304628053 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_platform.cpp         :193 : 0304628059 us: [pid:16    tid:0x7f54f7603280]  __hipPushCallConfiguration ( {1,1,1}, {8,1,1}, 0, stream:<null> ) 
:3:hip_platform.cpp         :197 : 0304628063 us: [pid:16    tid:0x7f54f7603280] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :202 : 0304628068 us: [pid:16    tid:0x7f54f7603280]  __hipPopCallConfiguration ( {0,0,0}, {0,0,0}, 0x7ffcaf46a840, 0x7ffcaf46a838 ) 
:3:hip_platform.cpp         :211 : 0304628072 us: [pid:16    tid:0x7f54f7603280] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :678 : 0304628080 us: [pid:16    tid:0x7f54f7603280]  hipLaunchKernel ( 0x7f54e318f2d8, {1,1,1}, {8,1,1}, 0x7ffcaf46a830, 0, stream:<null> ) 
:3:devprogram.cpp           :2684: 0304629187 us: [pid:16    tid:0x7f54f7603280] Using Code Object V5.
:3:rocvirtual.cpp           :781 : 0304631217 us: [pid:16    tid:0x7f54f7603280] Arg0:   = val:4150904307
:3:rocvirtual.cpp           :2897: 0304631222 us: [pid:16    tid:0x7f54f7603280] ShaderName : _ZN2at6native13reduce_kernelILi512ELi1ENS0_8ReduceOpIfNS0_14func_wrapper_tIfZNS0_11sum_functorIfffEclERNS_14TensorIteratorEEUlffE_EEjfLi4EEEEEvT1_
:3:hip_module.cpp           :679 : 0304631228 us: [pid:16    tid:0x7f54f7603280] hipLaunchKernel: Returned hipSuccess : 
:3:hip_error.cpp            :27  : 0304631231 us: [pid:16    tid:0x7f54f7603280]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :561 : 0304631237 us: [pid:16    tid:0x7f54f7603280]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :565 : 0304631239 us: [pid:16    tid:0x7f54f7603280] hipSetDevice: Returned hipSuccess : 
>>> d = c.cpu()
:3:hip_device_runtime.cpp   :531 : 0325815744 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46a974 ) 
:3:hip_device_runtime.cpp   :539 : 0325815753 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :531 : 0325815758 us: [pid:16    tid:0x7f54f7603280]  hipGetDevice ( 0x7ffcaf46a974 ) 
:3:hip_device_runtime.cpp   :539 : 0325815761 us: [pid:16    tid:0x7f54f7603280] hipGetDevice: Returned hipSuccess : 
:3:hip_memory.cpp           :652 : 0325815768 us: [pid:16    tid:0x7f54f7603280]  hipMemcpyWithStream ( 0x7c1d7c0, 0x7f52ad200200, 4, hipMemcpyDeviceToHost, stream:<null> ) 
:3:rocvirtual.hpp           :66  : 0325815787 us: [pid:16    tid:0x7f54f7603280] Host active wait for Signal = (0x7f53b1858780) for -1 ns
```
torch.sum() works fine, but copying it back to RAM (like for printing its contents) seems to hang indefinitely.

---

### 评论 #7 — hongxiayang (2023-11-18T22:22:35Z)

@MattisBergmann 
If torch.sum() gave the correct result, it means it also worked for you.
Regarding the hanging:

I saw your previous note when you report the problem, you mentioned it started to freeze after below change:

>lspci -vvvs 00:01.0
>I tried setting those bits with a udev rule which caused the error messages to disappear, but then it just freezes whenever any >ROCm operation is performed on the GPU. Is there some BIOS setting or driver configuration required to enable PCIe >atomics? >Or is it simply that my CPU or mainboard doesn't support them?

Is the hanging potentially related to the above change? Will you be able to revert the above change? It seems to me that the atomics issue is solved by the wheel, but because of the above change, you have been experiencing hanging since then.



---

### 评论 #8 — mergmann (2023-11-18T22:26:36Z)

The PCIe configuration change was only temporarily, it got reverted automatically by amdgpu after rebooting. The hanging also happened on older rocm versions (before 5.5).

---

### 评论 #9 — hongxiayang (2023-11-18T22:28:09Z)

what is your iommu setting? 

---

### 评论 #10 — hongxiayang (2023-11-18T22:39:48Z)

Try to disable iommu (iommu=off) in /etc/default/grub append to GRUB_CMDLINE_LINUX, then

sudo update-grub
then reboot.
See whether this helps.

---

### 评论 #11 — mergmann (2023-11-18T22:48:04Z)

IOMMU is enabled on my motherboard, but I didn't enable it in grub. Maybe it is enabled by default? I will try turning it off tomorrow, if that doesn't help, I will install a fresh Ubuntu, maybe some broken packages cause these problems.

---

### 评论 #12 — GbGp (2023-11-19T09:50:50Z)

Hello, I have the same issue and I am following the same steps indicated in this thread (recompiling pytorch from `rocm57_hostcall`, note that I forgot to run docker, so I am running in a simple venv).
I'm not sure If my report can be useful (my gpu is mounted on TB4 adapter..) but I see the same issue:
 
After the recompilation I don't have the issue with `RuntimeError: HIP error: the operation cannot be performed in the present state`.
But my system now also hangs after `torch.sum()` (with reported cpu and gpu usage stuck at 100%).
I noticed that `torch.sum()`  triggers some error that eventually ends with a gpu reset a few seconds later:
<details>
  <summary>gpu error dmesg log</summary>
  <pre><code>
[Nov19 10:33] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[  +0.000388] amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[  +0.000002] amdgpu: MES might be in unrecoverable state, issue a GPU reset
[  +0.000002] amdgpu: Failed to evict queue 1
[  +0.000001] amdgpu: Failed to evict process queues
[  +0.000001] amdgpu: Failed to quiesce KFD
[  +0.000050] amdgpu 0000:0e:00.0: amdgpu: GPU reset begin!
[  +0.046245] amdgpu: Failed to remove queue 0
[  +0.851431] amdgpu 0000:0e:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[  +0.000026] amdgpu 0000:0e:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[  +0.000010] amdgpu 0000:0e:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3A
[  +0.000008] amdgpu 0000:0e:00.0: amdgpu:       Faulty UTCL2 client ID: CPC (0x5)
[  +0.000007] amdgpu 0000:0e:00.0: amdgpu:       MORE_FAULTS: 0x0
[  +0.000006] amdgpu 0000:0e:00.0: amdgpu:       WALKER_ERROR: 0x5
[  +0.000006] amdgpu 0000:0e:00.0: amdgpu:       PERMISSION_FAULTS: 0x3
[  +0.000005] amdgpu 0000:0e:00.0: amdgpu:       MAPPING_ERROR: 0x1
[  +0.000005] amdgpu 0000:0e:00.0: amdgpu:       RW: 0x0
[  +0.125083] amdgpu 0000:0e:00.0: amdgpu: IP block:gfx_v11_0 is hung!
[  +0.001089] amdgpu 0000:0e:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:173 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[  +0.000025] amdgpu 0000:0e:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[  +0.000010] amdgpu 0000:0e:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B5B
[  +0.000008] amdgpu 0000:0e:00.0: amdgpu:       Faulty UTCL2 client ID: CPC (0x5)
[  +0.000007] amdgpu 0000:0e:00.0: amdgpu:       MORE_FAULTS: 0x1
[  +0.000006] amdgpu 0000:0e:00.0: amdgpu:       WALKER_ERROR: 0x5
[  +0.000005] amdgpu 0000:0e:00.0: amdgpu:       PERMISSION_FAULTS: 0x5
[  +0.000006] amdgpu 0000:0e:00.0: amdgpu:       MAPPING_ERROR: 0x1
[  +0.000005] amdgpu 0000:0e:00.0: amdgpu:       RW: 0x1
[  +0.000018] amdgpu 0000:0e:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:173 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[  +0.000011] amdgpu 0000:0e:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[  +0.000007] amdgpu 0000:0e:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[  +0.000006] amdgpu 0000:0e:00.0: amdgpu:       Faulty UTCL2 client ID: CB/DB (0x0)
[  +0.000006] amdgpu 0000:0e:00.0: amdgpu:       MORE_FAULTS: 0x0
[  +0.000005] amdgpu 0000:0e:00.0: amdgpu:       WALKER_ERROR: 0x0
[  +0.000005] amdgpu 0000:0e:00.0: amdgpu:       PERMISSION_FAULTS: 0x0
[  +0.000005] amdgpu 0000:0e:00.0: amdgpu:       MAPPING_ERROR: 0x0
[  +0.000005] amdgpu 0000:0e:00.0: amdgpu:       RW: 0x0
[  +0.000031] amdgpu 0000:0e:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:173 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[  +0.000009] amdgpu 0000:0e:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[  +0.000006] amdgpu 0000:0e:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[  +0.000006] amdgpu 0000:0e:00.0: amdgpu:       Faulty UTCL2 client ID: CB/DB (0x0)
[  +0.000006] amdgpu 0000:0e:00.0: amdgpu:       MORE_FAULTS: 0x0
[  +0.000005] amdgpu 0000:0e:00.0: amdgpu:       WALKER_ERROR: 0x0
[  +0.000005] amdgpu 0000:0e:00.0: amdgpu:       PERMISSION_FAULTS: 0x0
[  +0.000005] amdgpu 0000:0e:00.0: amdgpu:       MAPPING_ERROR: 0x0
[  +0.000004] amdgpu 0000:0e:00.0: amdgpu:       RW: 0x0
[  +0.000100] [drm] kiq ring mec 3 pipe 1 q 0
[  +1.011759] amdgpu 0000:0e:00.0: amdgpu: IP block:gfx_v11_0 is hung!
[  +0.000903] amdgpu 0000:0e:00.0: amdgpu: soft reset failed, will fallback to full reset!
[  +0.777591] [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[  +0.047552] amdgpu 0000:0e:00.0: amdgpu: MODE1 reset
[  +0.000007] amdgpu 0000:0e:00.0: amdgpu: GPU mode1 reset
[  +0.000288] amdgpu 0000:0e:00.0: amdgpu: GPU smu mode1 reset
[  +0.507334] amdgpu 0000:0e:00.0: amdgpu: GPU reset succeeded, trying to resume
[ +16.673468] amdgpu 0000:0e:00.0: amdgpu: failed to write reg 1a6f4 wait reg 1a706
[ +16.675458] amdgpu 0000:0e:00.0: amdgpu: failed to write reg 1a6f4 wait reg 1a706
[  +0.000020] [drm] PCIE GART of 512M enabled (table at 0x0000008000000000).
[  +0.000242] [drm] VRAM is lost due to GPU reset!
[  +0.000007] [drm] PSP is resuming...
[  +0.061697] [drm] reserve 0x1300000 from 0x81fc000000 for PSP TMR
[  +0.106287] amdgpu 0000:0e:00.0: amdgpu: RAS: optional ras ta ucode is not available
[  +0.008244] amdgpu 0000:0e:00.0: amdgpu: RAP: optional rap ta ucode is not available
[  +0.000007] amdgpu 0000:0e:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[  +0.000008] amdgpu 0000:0e:00.0: amdgpu: SMU is resuming...
[  +0.000016] amdgpu 0000:0e:00.0: amdgpu: smu driver if version = 0x00000035, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x00524b00 (82.75.0)
[  +0.000013] amdgpu 0000:0e:00.0: amdgpu: SMU driver if version not matched
[  +0.053036] amdgpu 0000:0e:00.0: amdgpu: SMU is resumed successfully!
[  +0.002450] [drm] DMUB hardware initialized: version=0x07002100
[Nov19 10:34] amdgpu 0000:0e:00.0: amdgpu: failed to write reg 291c wait reg 292e
[  +0.000665] [drm] kiq ring mec 3 pipe 1 q 0
[  +0.006090] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  +0.000820] amdgpu 0000:0e:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
[  +0.002109] amdgpu 0000:0e:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  +0.000004] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  +0.000002] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  +0.000002] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  +0.000001] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  +0.000001] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  +0.000002] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  +0.000001] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  +0.000001] amdgpu 0000:0e:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  +0.000001] amdgpu 0000:0e:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  +0.000002] amdgpu 0000:0e:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  +0.000001] amdgpu 0000:0e:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[  +0.000002] amdgpu 0000:0e:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[  +0.000001] amdgpu 0000:0e:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[  +0.005158] amdgpu 0000:0e:00.0: amdgpu: recover vram bo from shadow start
[  +0.000382] amdgpu 0000:0e:00.0: amdgpu: recover vram bo from shadow done
[  +0.000065] [drm] Skip scheduling IBs!
[  +0.000006] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000003] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000004] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000003] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000005] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000004] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000003] [drm] Skip scheduling IBs!
[  +0.000003] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000002] [drm] Skip scheduling IBs!
[  +0.000001] [drm] Skip scheduling IBs!
[  +0.000671] [drm] ring gfx_32773.1.1 was added
[  +0.000744] [drm] ring compute_32773.2.2 was added
[  +0.000848] [drm] ring sdma_32773.3.3 was added
[  +0.000091] [drm] ring gfx_32773.1.1 ib test pass
[  +0.000041] [drm] ring compute_32773.2.2 ib test pass
[  +0.000268] [drm] ring sdma_32773.3.3 ib test pass
[  +0.001278] amdgpu 0000:0e:00.0: amdgpu: GPU reset(1) succeeded!
</code></pre>
</details>

I will retry later to recompile in a clean env.

---

### 评论 #13 — mergmann (2023-11-19T13:50:11Z)

This might be relevant:
https://github.com/RadeonOpenCompute/ROCm/issues/2625

EDIT:
I tested it with a simple c++ program that creates a stream, without the module option the gpu usage is 100%, with setting the option it does indeed go down. But using pytorch it still stays at 100%

---

### 评论 #14 — GbGp (2023-11-19T14:04:27Z)

To exclude an hardware issue I tried to run an similar testcase to sum() using opencl:
https://gist.github.com/GbGp/120d4f15e021ce0917e24470fa534ec1
This runs perfectly fine on my gpu.

---

### 评论 #15 — mergmann (2023-11-19T14:19:17Z)

In my previous attempts, I found out, that it got stuck in
https://github.com/RadeonOpenCompute/ROCR-Runtime/blob/6fdf759273a098829dfd642fb730ea410f33b152/src/core/runtime/interrupt_signal.cpp#L139
Looking at the stacktrace, this seems to be the same problem. Back then, I thought that would be because ROCm 5.4.2 didn't yet support gfx11.
Here is the link to the issue:
https://github.com/evshiron/rocm_lab/issues/4#issuecomment-1584740343

---

### 评论 #16 — mergmann (2023-11-19T15:02:51Z)

After some more tests, I found out that this program somehow works:
```py
import torch
t1 = torch.Tensor(range(256)).cuda()
t2 = torch.Tensor(range(256, 512)).cuda()
q_gpu = t1 + t2
q_cpu = q_gpu.cpu()
```
It seems to have problems with copying scalars back to host.

EDIT:
My GPU (or driver) didn't like that and started drawing nonsense / flashing colorful boxes all over the screen, I had to do SysRq + REISUB to restart my system

---

### 评论 #17 — mergmann (2023-11-19T16:52:46Z)

I managed to run this huggingface example by recompiling PyTorch with NumPy support.
https://huggingface.co/docs/diffusers/using-diffusers/write_own_pipeline
However, more complex pipelines tend to freeze on hipMemcpyWithStream.

---

### 评论 #18 — hongxiayang (2023-11-20T19:45:14Z)

Not sure whether you have turned off iommu or not with the above progress?

---

### 评论 #19 — mergmann (2023-11-20T23:26:56Z)

I turned iommu off in the bios (intel vt-d) as well as in grub (iommu=off in kernel commandline)

---

### 评论 #20 — hongxiayang (2023-11-21T19:33:57Z)

Can you check this documentation and perform the pre-requisites steps?

https://rocm.docs.amd.com/projects/radeon/en/latest/docs/prerequisites.html


---

### 评论 #21 — hongxiayang (2023-11-21T19:48:35Z)

@GbGp Please use docker and exact step to test again. Also, what is your gfx target. Please run 
```
rocminfo
```

---

### 评论 #22 — GbGp (2023-11-21T20:31:10Z)

@hongxiayang sure, gfx1102 RX7600

<details>
  <summary>rocminfo</summary>

```
ROCk module is loaded
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

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
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
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   4000                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            8                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16105164(0xf5becc) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16105164(0xf5becc) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16105164(0xf5becc) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 7600                 
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
    L2:                      2048(0x800) KB                     
  Chip ID:                 29824(0x7480)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2283                               
  BDFID:                   3584                               
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 528                                
  SDMA engine uCode::      16                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1102         
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***       
      
```
</details>


---

### 评论 #23 — GbGp (2023-11-24T22:04:11Z)

sorry for the delay, I can confirm that I have the same issue after repeating all steps in the docker container.

Anyway looks my issue is better described by #2196, could it be the same problem?

---

### 评论 #24 — mergmann (2023-12-09T14:58:59Z)

I've installed ubuntu 22.04.3 and follwed the ROCm installation guide step by step. Yet I still get the same problem: It freezes at some point. Upon killing the python process, the gpu driver crashes and my system locks up.

---

### 评论 #25 — mergmann (2023-12-20T17:10:52Z)

The current nightly wheel has fixed the Initial problem "Pcie atomics not enabled, hostcall not supported", but the torch.sum() program still does not work, but instead always hangs and crashes amdgpu with a lot of messages similar to
```
[drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
```
Sometimes it shows also a page fault.

---

### 评论 #26 — mergmann (2023-12-21T16:02:29Z)

I've installed ROCm 6.0.0 and PyTorch 5.7 on my ubuntu installation and it surprisingly works.

---
