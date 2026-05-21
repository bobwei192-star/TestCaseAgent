# [Issue]: RuntimeError: HIP error: invalid device function

> **Issue #5668**
> **状态**: closed
> **创建时间**: 2025-11-14T11:11:23Z
> **更新时间**: 2025-12-01T16:34:38Z
> **关闭时间**: 2025-12-01T16:34:38Z
> **作者**: gqyalh
> **标签**: Documentation, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5668

## 标签

- **Documentation** (颜色: #5319e7)
- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

### Operating System

Ubuntu 24

### CPU

AMD radeon AI max+395

### GPU

product: Strix Halo [Radeon Graphics / Radeon 8050S Graphics / Radeon 8060S Graphics]

### ROCm Version

ROCk module version 6.16.6 is loaded

### ROCm Component

_No response_

### Steps to Reproduce

RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


### Additional Information

**1.system is ubuntu**
**2.rocminfo**
rocminfo
ROCk module version 6.16.6 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES
**3.rocm-smi**
ROCM-SMI version: 3.0.0+03a4530
ROCM-SMI-LIB version: 7.5.0
**4.pytorch version**
torch                    2.4.1+rocm6.0
torch-complex            0.4.4
torchaudio               2.4.1+rocm6.0
torchvision              0.19.1+rocm6.0

---

## 评论 (13 条)

### 评论 #1 — harkgill-amd (2025-11-14T14:59:26Z)

Hey @gqyalh, noticing your torch wheels are a little outdated (ROCm 6.0). Could you install the latest ROCm and torch wheels from https://github.com/ROCm/TheRock/blob/main/RELEASES.md and give your workload a try. If you could also share the workload or a small reproducer, I can look into it further on my end as well.

---

### 评论 #2 — gqyalh (2025-11-17T01:54:37Z)

<img width="1363" height="191" alt="Image" src="https://github.com/user-attachments/assets/b1a65ac6-c510-467c-b288-22ccd8a983d1" />

<img width="1375" height="254" alt="Image" src="https://github.com/user-attachments/assets/88b89168-5fa5-4e05-8149-2e335f8df44e" />

---

### 评论 #3 — gqyalh (2025-11-17T05:09:36Z)


**rocm-smi --version**
ROCM-SMI version: 4.0.0+7721681424
ROCM-SMI-LIB version: 7.8.0

``
**rocminfo**
ROCk module version 6.16.6 is loaded


**pip list**
torch                      2.10.0a0+rocm7.10.0a20251015
torch-complex              0.4.4
torchaudio                 2.8.0a0+rocm7.10.0a20251015
torchvision                0.25.0a0+rocm7.10.0a20251015

/home/gqy/miniconda3/envs/family_assistant_p312/bin/python3 /home/gqy/py_workspace/familyAssistantP312/family_assistant_sensevoice.py 
初始化家庭管家应用程序...
PyTorch版本: 2.10.0a0+rocm7.10.0a20251015
可用音频设备数量: 11
默认输入设备: default
正在初始化各个模块...
正在加载Silero VAD模型...
使用本地模型路径: /home/gqy/py_workspace/familyAssistantP312/snakers4-silero-vad-3ca476e
正在加载模型文件，请稍候...
模型文件加载完成，VAD模型使用CPU模式（确保实时性和稳定性）...
VAD模型加载完成
[设备检测] PyTorch版本: 2.10.0a0+rocm7.10.0a20251015
[设备检测] PyTorch支持ROCm: 7.1.25413-7721681424
[设备检测] 系统ROCm版本: 7.8.0
[设备检测] 检测到ROCm环境变量: ROCM_PATH, HIP_VISIBLE_DEVICES
  ROCM_PATH=/opt/rocm
  HIP_VISIBLE_DEVICES=0
[设备检测] torch.cuda.is_available() = True
[设备检测] GPU设备数量: 1
[设备检测] GPU设备名称: Radeon 8060S Graphics
[设备检测] GPU总内存: 96.00 GB
[设备检测] ✓ 检测到AMD GPU设备: Radeon 8060S Graphics
[设备检测] ROCm 7.1.25413-7721681424
[设备检测] 将使用GPU (ROCm) 进行语音识别加速
正在加载SenseVoiceSmall模型...
正在从ModelScope下载SenseVoiceSmall模型...
（首次下载可能需要一些时间，请耐心等待）
Downloading Model from https://www.modelscope.cn to directory: /home/gqy/py_workspace/familyAssistantP312/.modelscope_cache/iic/SenseVoiceSmall
模型下载完成，路径: /home/gqy/py_workspace/familyAssistantP312/.modelscope_cache/iic/SenseVoiceSmall
正在加载模型（设备: cuda）...
[GPU检测] GPU设备: Radeon 8060S Graphics, 内存: 96.00 GB
[TensileLibrary] 找到有效的库文件: /home/gqy/miniconda3/envs/family_assistant_p312/lib/python3.12/site-packages/torch/lib/rocblas/library/TensileLibrary.dat

Process finished with exit code 139 (interrupted by signal 11:SIGSEGV) 



---

### 评论 #4 — benlau (2025-11-17T19:13:13Z)

> Hey [@gqyalh](https://github.com/gqyalh), noticing your torch wheels are a little outdated (ROCm 6.0). Could you install the latest ROCm and torch wheels from https://github.com/ROCm/TheRock/blob/main/RELEASES.md and give your workload a try. If you could also share the workload or a small reproducer, I can look into it further on my end as well.

What is the different between the torch package from TheROCK and from the https://download.pytorch.org/whl/nightly/rocm7.1 ? Which one is recommended to use for ? 


---

### 评论 #5 — harkgill-amd (2025-11-17T19:32:48Z)

@gqyalh could you share more information about your workload, possibly a small reproducer script that narrows down what's actually failing on your end? At first glance, it looks like your working with some `torchaudio` specific workloads. We've seen similar errors in https://github.com/ROCm/TheRock/issues/1371 and the workaround in that case was to was to preload `libllvmlite.so` with 
```
LD_PRELOAD="</path/to/venv>/lib/python3.12/site-packages/llvmlite/binding/libllvmlite.so" python script.py
```
It's a shot in the dark without more information but could you give this a try on your end?

@benlau The torch package from https://download.pytorch.org/whl/nightly/rocm7.1 is apart of our [production release stream](https://rocm.docs.amd.com/en/latest/release/versions.html) whereas TheRock torch packages are part of our [technology preview stream](https://rocm.docs.amd.com/en/7.9.0-preview/release/versions.html). The main difference is that the TheRock (technology preview stream) will have the latest changes and features that might not have been picked up by our production releases. As an end user, the choice is basically yours as to whether you want the bleeding edge or a slightly older but more stable release. Going forward, we will be shifting to only using the TheRock (technology preview stream) which should minimize any confusion that the two streams cause.


---

### 评论 #6 — gqyalh (2025-11-19T02:25:19Z)

I installed torch using the following command:

python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ \
  "rocm[libraries,devel]"

pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ \
  --pre torch torchaudio torchvision

Do you mean to install torch via this specific .whl link: https://download.pytorch.org/whl/nightly/rocm7.1/torch-2.10.0.dev20251110%2Brocm7.1-cp312-cp312-manylinux_2_28_x86_64.whl?

or use 
pip install
--index-url  https://download.pytorch.org/whl/nightly/rocm7.1 


---

### 评论 #7 — gqyalh (2025-11-19T03:06:18Z)

should i  install whl follow list
torch-2.10.0.dev20251113+rocm7.1-cp312-cp312-manylinux_2_28_x86_64.whl
torchaudio-2.10.0.dev20251118+rocm7.1-cp312-cp312-manylinux_2_28_x86_64.whl
torchvision-0.25.0.dev20251118+rocm7.1-cp312-cp312-manylinux_2_28_x86_64.whl




---

### 评论 #8 — benlau (2025-11-19T19:01:41Z)

FYI, I have a machine with an AMD Radeon AI max+395 with ROCm 7.1 installed. ComfyUI crashes randomly with the error message of "RuntimeError: HIP error: invalid device function" (the same error message mentioned in this post). If I run sd-scripts to train LoRA, it will crash randomly with a 700/709 error. According to a few discussions in this project, I tried to set amdgpu.cwsr_enable=0 via grub. And then, after executing for a day, those errors were gone.

---

### 评论 #9 — harkgill-amd (2025-11-19T20:01:59Z)

@gqyalh, the packages you have installed here are good.
```
pip list
torch 2.10.0a0+rocm7.10.0a20251015
torch-complex 0.4.4
torchaudio 2.8.0a0+rocm7.10.0a20251015
torchvision 0.25.0a0+rocm7.10.0a20251015
```
Could you give the `LD_PRELOAD` workaround that I shared in https://github.com/ROCm/ROCm/issues/5668#issuecomment-3543536297 a try and report back.

Disabling cwsr can be inconclusive but it's also worth a try if the aforementioned workaround doesn't work. @gqyalh, please try this as well. For context, we do have a pair of fixes going in that should resolve this issue as well https://github.com/ROCm/ROCm/issues/5590#issuecomment-3538640902. That being said, the best way to debug this would be a small reproducer or more information on the actual workload that's being run prior to the invalid device function errors, please share this if possible.

---

### 评论 #10 — gqyalh (2025-11-20T01:52:04Z)

The problem has been solved  by pipping torch 2.10.0a0+rocm7.10.0a20251015 torchaudio 2.8.0a0+rocm7.10.0a20251015 torchvision 0.25.0a0+rocm7.10.0a20251015
tks

---

### 评论 #11 — gqyalh (2025-11-20T10:09:18Z)

new question

VLLM_USE_MODELSCOPE=true vllm serve deepseek-ai/DeepSeek-R1-Distill-Llama-70B --tensor-parallel-size 2 --max-model-len 32768 --enforce-eager
INFO 11-20 18:08:10 [__init__.py:220] No platform detected, vLLM is running on UnspecifiedPlatform
WARNING 11-20 18:08:11 [_custom_ops.py:20] Failed to import from vllm._C with ImportError('libcudart.so.12: cannot open shared object file: No such file or directory')
Traceback (most recent call last):
  File "/home/gqy/miniconda3/envs/vllm/bin/vllm", line 7, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/gqy/miniconda3/envs/vllm/lib/python3.12/site-packages/vllm/entrypoints/cli/main.py", line 46, in main
    cmd.subparser_init(subparsers).set_defaults(
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gqy/miniconda3/envs/vllm/lib/python3.12/site-packages/vllm/entrypoints/cli/serve.py", line 70, in subparser_init
    serve_parser = make_arg_parser(serve_parser)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gqy/miniconda3/envs/vllm/lib/python3.12/site-packages/vllm/entrypoints/openai/cli_args.py", line 263, in make_arg_parser
    parser = AsyncEngineArgs.add_cli_args(parser)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gqy/miniconda3/envs/vllm/lib/python3.12/site-packages/vllm/engine/arg_utils.py", line 1714, in add_cli_args
    parser = EngineArgs.add_cli_args(parser)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gqy/miniconda3/envs/vllm/lib/python3.12/site-packages/vllm/engine/arg_utils.py", line 919, in add_cli_args
    vllm_kwargs = get_kwargs(VllmConfig)
                  ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gqy/miniconda3/envs/vllm/lib/python3.12/site-packages/vllm/engine/arg_utils.py", line 281, in get_kwargs
    return copy.deepcopy(_compute_kwargs(cls))
                         ^^^^^^^^^^^^^^^^^^^^
  File "/home/gqy/miniconda3/envs/vllm/lib/python3.12/site-packages/vllm/engine/arg_utils.py", line 182, in _compute_kwargs
    default = field.default_factory()
              ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gqy/miniconda3/envs/vllm/lib/python3.12/site-packages/pydantic/_internal/_dataclasses.py", line 121, in __init__
    s.__pydantic_validator__.validate_python(ArgsKwargs(args, kwargs), self_instance=s)
  File "/home/gqy/miniconda3/envs/vllm/lib/python3.12/site-packages/vllm/config/device.py", line 58, in __post_init__
    raise RuntimeError(
RuntimeError: Failed to infer device type, please set the environment variable `VLLM_LOGGING_LEVEL=DEBUG` to turn on verbose logging to help debug the issue.



---

### 评论 #12 — harkgill-amd (2025-11-20T16:38:37Z)

>  ImportError('libcudart.so.12: cannot open shared object file: No such file or directory')

From the error message, it looks like your vLLM installation wasn't built for ROCm. The easiest way to get started with vLLM on ROCm with Strix Halo is by using the prebuilt docker images https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/advanced/advancedryz/linux/llm/build-docker-image.html. I did have to additionally install modelscope with `pip install modelscope>=1.18.1` as it's not included by default. `--tensor-parallel-size` also isn't applicable in this case as we're not working with parallelism/multiple GPUs. With these two changes, I was able to run your command successfully using the docker image. 

As a side note `DeepSeek-R1-Distill-Llama-70B` is a rather large model (~140 GB using FP16). You'll likely run into out of memory errors depending on your system's memory limitations in which case you can play around with the precision where possible or use a smaller model.

---

### 评论 #13 — harkgill-amd (2025-12-01T16:34:38Z)

@gqyalh, I'll close this one out for now. If you are still experiencing any issues with vLLM on your Strix Halo, please leave a comment and I'll re-open this ticket. Thanks!

---
