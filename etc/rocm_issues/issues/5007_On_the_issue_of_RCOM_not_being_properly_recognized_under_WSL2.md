# On the issue of RCOM not being properly recognized under WSL2

> **Issue #5007**
> **状态**: open
> **创建时间**: 2025-07-08T12:35:02Z
> **更新时间**: 2025-08-08T14:50:55Z
> **作者**: InkyFish
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5007

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### System Environment Description

1. Windows 10 latest version with WSL2 Ubuntu 22.04  
2. GPU: RX 9070 XT; CPU: Ryzen 7 9700X  
3. ROCm 6.4.1; PyTorch 2.6.0; vLLM 0.8.2 (using 0.8.2 because vLLM 0.9.1 requires PyTorch 2.7.0)  
4. ROCm [installation reference](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html);  
   PyTorch [installation reference](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html)  

### Self-check status

`
rocminfo
Agent 2
  Name:                    gfx1201
  Marketing Name:          AMD Radeon RX 9070 XT
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU`

`root@DESKTOP-3IMOAOF:~# python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'
Success`
`root@DESKTOP-3IMOAOF:~# python3 -c 'import torch; print(torch.cuda.is_available())'
True`

`root@DESKTOP-3IMOAOF:~# python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))"
/usr/local/lib/python3.10/dist-packages/torch/cuda/__init__.py:736: UserWarning: Can't initialize amdsmi - Error code: 34
  warnings.warn(f"Can't initialize amdsmi - Error code: {e.err_code}")
device name [0]: AMD Radeon RX 9070 XT`

`
# modprobe amdgpu command fails after WSL reboot
root@DESKTOP-3IMOAOF:~# lsmod | grep amdgpu
root@DESKTOP-3IMOAOF:~# rocm-smi
ERROR:root:Driver not initialized (amdgpu not found in modules)
root@DESKTOP-3IMOAOF:~# modprobe amdgpu
root@DESKTOP-3IMOAOF:~# lsmod | grep amdgpu
amdgpu               8892416  0
drm_exec               12288  1 amdgpu
amdxcp                 12288  1 amdgpu
drm_buddy              16384  1 amdgpu
gpu_sched              49152  1 amdgpu
video                  65536  1 amdgpu
drm_suballoc_helper    12288  1 amdgpu
drm_display_helper    155648  1 amdgpu
i2c_algo_bit           12288  1 amdgpu
root@DESKTOP-3IMOAOF:~# rocm-smi
ERROR:root:ROCm SMI returned 8 (the expected value is 0)`

### Problem Description
The /dev/kfd and /dev/dri directories do not exist, and the rocm-smi command reports errors. I suspect the GPU passthrough feature is not working. The GPU driver on Windows is the latest version (25.6.1). How can I resolve this?
When running large models with vLLM, errors occur, but running them directly with PyTorch works fine. However, this remains an issue, and a fix is expected to be provided.


---

## 评论 (11 条)

### 评论 #1 — ppanchad-amd (2025-07-08T14:15:54Z)

Hi @InkyFish. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-07-08T15:21:40Z)

Hi @InkyFish, WSL does not work the same way as native Linux; `amdgpu` will not be loaded the same way in WSL as in native Linux and loading it should not be necessary, and `/dev/kfd` and `/dev/dri` won't exist (`/dev/dxg` is used instead). Due to architectural differences, `rocm-smi` and `amd-smi` are not functional on WSL, which we've noted at https://rocm.docs.amd.com/projects/radeon/en/latest/docs/limitations.html#rocm-support-in-wsl-environments.

> When running large models with vLLM, errors occur

We can take a look at these errors here or in a separate issue if you'd like.

---

### 评论 #3 — InkyFish (2025-07-09T13:52:22Z)

@schung-amd Error message when running large models with vLLM is as follows (environment details were provided earlier):
error message：
`INFO 07-09 21:48:57 [__init__.py:243] No platform detected, vLLM is running on UnspecifiedPlatform
WARNING 07-09 21:48:58 [rocm.py:32] Failed to import from vllm._C with ImportError('libcudart.so.12: cannot open shared object file: No such file or directory')
WARNING 07-09 21:48:58 [rocm.py:38] Failed to import from vllm._rocm_C with ModuleNotFoundError("No module named 'vllm._rocm_C'")
Traceback (most recent call last):
  File "/root/vllmtest.py", line 3, in <module>
    from vllm.platforms.rocm import ROCmPlatform
ImportError: cannot import name 'ROCmPlatform' from 'vllm.platforms.rocm' (/usr/local/lib/python3.10/dist-packages/vllm/platforms/rocm.py)`

code：
`import os
from vllm import LLM, SamplingParams
from vllm.platforms.rocm import ROCmPlatform
from vllm.platforms import set_platform

set_platform(ROCmPlatform())

os.environ["VLLM_USE_ROCM"] = "1"

model_path = os.path.expanduser("/root/models/Qwen3-0.6B")
llm = LLM(
    model=model_path,
    device="hip",
    tensor_parallel_size=1,
    enforce_eager=True,
    disable_async_execution=True,
    max_model_len=2048,
)

prompts = ["hello"]
sampling_params = SamplingParams(temperature=0.8, top_p=0.9, max_tokens=50)
outputs = llm.generate(prompts, sampling_params)

print("output:", outputs[0].outputs[0].text)`

---

### 评论 #4 — schung-amd (2025-07-09T15:16:53Z)

Thanks for the quick reply, and sorry for the inconvenience. Frustratingly, vLLM has some code that requires initialization of amdsmi to detect if ROCm should be used (see https://github.com/vllm-project/vllm/blob/efe73d0575951767180468dac8202739cb479074/vllm/platforms/__init__.py#L98-L116) so that won't work on WSL. We are aware of this issue and have implemented some functionality to make detection of ROCm possible on WSL via `amdsmi.amdsmi_get_rocm_version()`, but it appears that it is not supported by vLLM as of yet. 

The platform check issue can be worked around by replacing the check with something like

```
is_rocm = False
logger.debug("Checking if ROCm platform is available.")
import amdsmi
if amdsmi.amdsmi_get_rocm_version()[0] == True:
        is_rocm = True
        logger.debug("Confirmed ROCm platform is available.")

return "vllm.platforms.rocm.RocmPlatform" if is_rocm else None
```

I'm seeing other errors when I try this with the vLLM 0.8.2 release though, will see if there's an easy workaround for those. Normally we recommend using the vLLM Docker images, but I'm not sure if these are compatible with WSL.

---

### 评论 #5 — InkyFish (2025-07-10T02:16:04Z)

@schung-amd 
Thank you very much. It seems that I can only download the source code, modify it, and then compile it myself. Do you have any recommended compilation methods? I tried before but the compilation failed. Maybe it will succeed after modifying the code, but I'm not sure. I hope you can provide a correct way to compile it.

---

### 评论 #6 — schung-amd (2025-07-10T14:32:13Z)

You don't actually need to compile anything if only modifying the python files. You can just edit the files at the location mentioned in the error logs; in your case, the vLLM files look to be contained at `/usr/local/lib/python3.10/dist-packages/vllm`. This way you can work with vLLM installed in one of our Docker images or from a wheel in addition to vLLM built from source.

If do you need to modify the C source files and recompile the libraries, it's easier to build from source in the first place, although it is possible to do this in our Dockers or from a wheel as well. I have had success in the past following the instructions at https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html using CK flash attention, but haven't tried recently. If you want to try building from source and run into errors, post them here or in a separate issue and we can take a look.

To modify and recompile the C source in our Docker images, you'll need to download the source code of a matching version. Then you can modify that code, compile the libraries, and replace the libraries in the installed vLLM location with the new libraries. Your paths may vary, but for example on my system I do this with
```
cmake -S ./vllm -DVLLM_TARGET_DEVICE=rocm -DVLLM_GPU_LANG=hip -DVLLM_PYTHON_EXECUTABLE=$(which python) -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -B build
cd build && make -j8
cp ./*.so /opt/conda/envs/py_3.10/lib/python3.1/site-packages/vllm
```


---

### 评论 #7 — brunobenchimol (2025-08-06T01:43:58Z)

Im having the same issue running vllm on AMD cards on WSL2. I also tried to test the docker version but without success.

Every suggestion is to change the source code as explained to @schung-amd. 

Is it possible to code a variable like `WSL2_DEVICES=True` that could fix checking the proper devices ? 

I already tried to expose libhsa-runtime64.so.1 and /dev/dxg to docker and still no success.

It seems to be very hard AMD running AI tasks. I really hope we find an easy to run it on amd cards, because it takes a lot of effort to just make it work.

I was able run pytorch on amd docker rocm images, but rocm/vllm does not work as expected. Probably because its devices to are hard-coded? 

---

### 评论 #8 — schung-amd (2025-08-07T20:57:10Z)

I'm working on a PR for upstream vLLM to provide an alternative initialization method that will enable vLLM in WSL, but haven't tested vLLM functionality in WSL yet.

> I was able run pytorch on amd docker rocm images, but rocm/vllm does not work as expected. Probably because its devices to are hard-coded?

Our vLLM dockers don't have WSL-compatible torch installed. You can install a WSL-compatible torch to fix this by following https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html. There is no reason at the moment to provide compatible torch in the vLLM images since vLLM itself won't work, but once we have vLLM working we can provide compatible torch versions.

---

### 评论 #9 — InkyFish (2025-08-08T02:01:18Z)

@schung-amd WSL itself is a form of virtualization. I think installing Docker inside WSL is not a very good choice. If possible, I still prefer to install vllm natively.

---

### 评论 #10 — schung-amd (2025-08-08T14:29:16Z)

@InkyFish Are you running into any issues with pytorch and vLLM built from source aside from vLLM not detecting the ROCm platform properly (which can be circumvented with the workaround to use python-only amdsmi API)?

---

### 评论 #11 — brunobenchimol (2025-08-08T14:50:55Z)

> I'm working on a PR for upstream vLLM to provide an alternative initialization method that will enable vLLM in WSL, but haven't tested vLLM functionality in WSL yet.
> 
> > I was able run pytorch on amd docker rocm images, but rocm/vllm does not work as expected. Probably because its devices to are hard-coded?
> 
> Our vLLM dockers don't have WSL-compatible torch installed. You can install a WSL-compatible torch to fix this by following https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html. There is no reason at the moment to provide compatible torch in the vLLM images since vLLM itself won't work, but once we have vLLM working we can provide compatible torch versions.

Thanks for the heads up. I am looking forward to it whenever it gets avaliable. 

I managed to get it working and fully detected my GPU (9070XT) when using Option B from the following link.


@InkyFish There is no way to run Docker on Windows without WSL2. In fact its a type of virtualization.
I also tried other hypervisors to try it, but do not have gpu passthrought. From my research i found out that Hyper-V probably can do it, but it only works on Windows Pro editions.

Atm i can not afford to dual boot to try it on bare metal, thats why im running on WSL. This way is very easy to develop and test something without breaking things. 

My main point is that it should not be hard to run the software itself, so we can focus on AI itself. Looks like every AI software is dominated by cuda/nvidia. I remember back in the days when games were only optimized for nvidia... now they run fine on amd aswell, but AI softwares are still developing support for amd. Hopefully in a few years it will be transparent for users whatever brand of gpu you are using.

---
