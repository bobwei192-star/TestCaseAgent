# Using RX6650XT, rocm5.4.2 reports an error when running stable diffusion

> **Issue #2329**
> **状态**: closed
> **创建时间**: 2023-07-22T06:48:07Z
> **更新时间**: 2024-02-26T08:16:38Z
> **关闭时间**: 2023-07-23T02:50:09Z
> **作者**: 14790897
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2329

## 描述

python launch.py --precision full --no-half
Python 3.9.17 (main, Jul  5 2023, 20:41:20) 
[GCC 11.2.0]
Version: v1.4.1
Commit hash: f865d3e11647dfd6c7b2cdf90dde24680e58acd8
Installing requirements
Launching Web UI with arguments: --precision full --no-half
No module 'xformers'. Proceeding without it.
Loading weights [18ed2b6c48] from /home/ubuntu/sd/stable-diffusion-webui/models/Stable-diffusion/xxmix9realistic_v40.safetensors
preload_extensions_git_metadata for 7 extensions took 0.00s
Running on local URL:  http://127.0.0.1:7860

To create a public link, set `share=True` in `launch()`.
Startup time: 2.9s (import torch: 0.9s, import gradio: 0.5s, import ldm: 0.2s, other imports: 0.5s, load scripts: 0.3s, create ui: 0.4s, gradio launch: 0.1s).
MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(), c_options.size(), c_options.data())' naive_conv.cpp: HIPRTC_ERROR_COMPILATION (6)
MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION (6), source file: naive_conv.cpp
MIOpen(HIP): Warning [BuildHip] /tmp/comgr-8f15a2/input/naive_conv.cpp:39:10: fatal error: 'limits' file not found
#include <limits> // std::numeric_limits
         ^~~~~~~~
1 error generated when compiling for gfx1030.
terminate called after throwing an instance of 'miopen::Exception'
  what():  /long_pathname_so_that_rpms_can_package_the_debug_info/data/driver/MLOpen/src/hipoc/hipoc_program.cpp:304: Code object build failed. Source: naive_conv.cpp
Aborted (core dumped)


---

## 评论 (7 条)

### 评论 #1 — 14790897 (2023-07-22T06:51:38Z)

pytorch can run a bit：
>>> import torch

>>> print(torch.__version__)
2.0.1+rocm5.4.2
>>> if torch.cuda.is_available():
...     x = torch.rand(5, 3).cuda()
...     print(x)
... else:
...     print("No AMD GPU available")
... 
tensor([[0.8301, 0.5985, 0.4911],
        [0.8105, 0.9210, 0.2274],
        [0.7984, 0.7864, 0.3693],
        [0.8469, 0.1225, 0.1067],
        [0.9466, 0.5537, 0.4603]], device='cuda:0')

then, when I train the neural network
(sd) ubuntu@ubuntu-System-Product-Name:~/Documents/git-program/neural-net$ python mni.py 
MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(), c_options.size(), c_options.data())' naive_conv.cpp: HIPRTC_ERROR_COMPILATION (6)
MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION (6), source file: naive_conv.cpp
MIOpen(HIP): Warning [BuildHip] /tmp/comgr-d09741/input/naive_conv.cpp:39:10: fatal error: 'limits' file not found
#include <limits> // std::numeric_limits
         ^~~~~~~~
1 error generated when compiling for gfx1032.
terminate called after throwing an instance of 'miopen::Exception'
  what():  /long_pathname_so_that_rpms_can_package_the_debug_info/data/driver/MLOpen/src/hipoc/hipoc_program.cpp:304: Code object build failed. Source: naive_conv.cpp
Aborted (core dumped)

---

### 评论 #2 — 14790897 (2023-07-22T07:13:48Z)

When I use rocm5.6.0, I enter the webpage of sd webui, but there is a similar error as before when generating the picture, which is 'limits' file not found'
error information:
DiffusionWrapper has 859.52 M params.
Downloading (…)olve/main/vocab.json: 100%|████| 961k/961k [00:01<00:00, 830kB/s]
Downloading (…)olve/main/merges.txt: 100%|███| 525k/525k [00:00<00:00, 2.86MB/s]
Downloading (…)cial_tokens_map.json: 100%|█████| 389/389 [00:00<00:00, 2.54MB/s]
Downloading (…)okenizer_config.json: 100%|█████| 905/905 [00:00<00:00, 5.86MB/s]
Downloading (…)lve/main/config.json: 100%|█| 4.52k/4.52k [00:00<00:00, 23.5MB/s]
Applying attention optimization: Doggettx... done.
Textual inversion embeddings loaded(0): 
Model loaded in 12.7s (calculate hash: 4.6s, load weights from disk: 0.1s, create model: 6.0s, apply weights to model: 0.9s, apply half(): 0.4s, move model to device: 0.4s, load textual inversion embeddings: 0.1s, calculate empty prompt: 0.2s).
Calculating sha256 for /home/ubuntu/sd/stable-diffusion-webui/models/Stable-diffusion/xxmix9realistic_v40.safetensors: 18ed2b6c48fda400330e5dec9e6f4d714ef664869ea8d4021f12ba699b31da06
Loading weights [18ed2b6c48] from /home/ubuntu/sd/stable-diffusion-webui/models/Stable-diffusion/xxmix9realistic_v40.safetensors
Applying attention optimization: Doggettx... done.
Weights loaded in 4.2s (calculate hash: 2.3s, load weights from disk: 0.4s, apply weights to model: 1.1s, move model to device: 0.4s).
  0%|                                                    | 0/20 [00:00<?, ?it/s]MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(), c_options.size(), c_options.data())' convolution_forward_implicit_gemm_v6r1_dlops_nchw_kcyx_nkhw.cpp: HIPRTC_ERROR_COMPILATION (6)
MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION (6), source file: convolution_forward_implicit_gemm_v6r1_dlops_nchw_kcyx_nkhw.cpp
MIOpen(HIP): Warning [BuildHip] In file included from /tmp/comgr-58dcf8/input/convolution_forward_implicit_gemm_v6r1_dlops_nchw_kcyx_nkhw.cpp:1:
In file included from /tmp/comgr-58dcf8/include/common_header.hpp:10:
/tmp/comgr-58dcf8/include/data_type.hpp:14:10: fatal error: 'limits' file not found
#include <limits> // std::numeric_limits
         ^~~~~~~~
1 error generated when compiling for gfx1030.
terminate called after throwing an instance of 'miopen::Exception'
  what():  /MIOpen/src/hipoc/hipoc_program.cpp:304: Code object build failed. Source: convolution_forward_implicit_gemm_v6r1_dlops_nchw_kcyx_nkhw.cpp
./webui.sh: line 241: 16653 Aborted                 (core dumped) "${python_cmd}" "${LAUNCH_SCRIPT}" "$@"

---

### 评论 #3 — 14790897 (2023-07-22T07:14:30Z)

'limits' file not found' is the problem we need to solve

---

### 评论 #4 — 14790897 (2023-07-22T07:18:45Z)

I have spent four days on installing rocm and pytorch, can you guys help me?

---

### 评论 #5 — xuhuisheng (2023-07-22T12:49:17Z)

pytorch 1.13 should fine.
there must be bug on pytorch 2.x with  rocm.

---

### 评论 #6 — 14790897 (2023-07-27T07:20:21Z)

just run 'sudo apt install libstdc++-12-dev'

---

### 评论 #7 — 14790897 (2024-02-26T08:16:37Z)

https://are-we-gfx1100-yet.github.io/post/a1111-webui/#fatal-error-limits-file-not-found

---
