# "RuntimeError: miopenStatusUnknownError" code in sdwebui by using pytorch2.1.0+ROCm5.6

> **Issue #2355**
> **状态**: closed
> **创建时间**: 2023-07-30T06:01:15Z
> **更新时间**: 2023-07-31T01:36:44Z
> **关闭时间**: 2023-07-31T01:36:44Z
> **作者**: PennyFranklin
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2355

## 描述

GPU: 7900xtx
version of sdwebui: v1.5.1
version of pytorch: https://download.pytorch.org/whl/nightly/rocm5.6
Failed to generate pictures after swiching the pytorch from https://evshiron.github.io/ to pytorch.org. 
It used to work well with evshiron's pytorch version with ROCm5.6.
But still have response when key  in "rocm-smi"  code.
So I don't know whether there is a bug on bytorch or rocm or my steps :(
![截图 2023-07-30 13-59-15](https://github.com/RadeonOpenCompute/ROCm/assets/104998459/50980e4e-85d9-4da4-8420-d4483cdb7995)


---

## 评论 (5 条)

### 评论 #1 — evshiron (2023-07-30T09:06:18Z)

Hmmm. I switched to it today and it [worked well](https://vladmandic.github.io/sd-extension-system-info/pages/benchmark.html) on my end. Here are my steps:

```bash
source venv/bin/activate
pip3 uninstall torch torchvision torchaudio
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm5.6
bash launch.sh
```

Would you mind making a fresh installation of A1111 WebUI by following the tutorial and see if it works?

* https://are-we-gfx1100-yet.github.io/post/a1111-webui/#the-easy-approach

---

### 评论 #2 — PennyFranklin (2023-07-30T14:43:19Z)

I tried the steps above and got the same error.I'll make a total fresh installion and see. 

---

### 评论 #3 — PennyFranklin (2023-07-30T15:27:39Z)

Full reinstalled the webui after the guide in the web ,still miopen error.
Every seems to go wrong after upgrading the Ubuntu.
Put the error code:

penny@neko:~/stable-diffusion-webui$ '/home/penny/stable-diffusion-webui/webui.sh' 

################################################################
Install script for stable-diffusion + Web UI
Tested on Debian 11 (Bullseye)
################################################################

################################################################
Running on penny user
################################################################

################################################################
Repo already cloned, using it as install directory
################################################################

################################################################
Create and activate python venv
################################################################

################################################################
Launching launch.py...
################################################################
Cannot locate TCMalloc (improves CPU memory usage)
Python 3.10.6 (main, May 29 2023, 11:10:38) [GCC 11.3.0]
Version: v1.5.1
Commit hash: 68f336bd994bed5442ad95bad6b6ad5564a5409a

Launching Web UI with arguments: 
no module 'xformers'. Processing without...
no module 'xformers'. Processing without...
No module 'xformers'. Proceeding without it.
Loading weights [ed989d673d] from /home/penny/stable-diffusion-webui/models/Stable-diffusion/dreamshaper_7.safetensors
Running on local URL:  http://127.0.0.1:7860

To create a public link, set `share=True` in `launch()`.
Startup time: 5.7s (launcher: 1.9s, import torch: 1.7s, import gradio: 0.5s, setup paths: 0.4s, other imports: 0.4s, load scripts: 0.2s, create ui: 0.3s, gradio launch: 0.1s).
Creating model from config: /home/penny/stable-diffusion-webui/configs/v1-inference.yaml
LatentDiffusion: Running in eps-prediction mode
DiffusionWrapper has 859.52 M params.
Applying attention optimization: Doggettx... done.
Model loaded in 2.2s (load weights from disk: 0.5s, create model: 0.2s, apply weights to model: 0.8s, apply half(): 0.2s, move model to device: 0.2s, calculate empty prompt: 0.1s).
  0%|                                                    | 0/20 [00:00<?, ?it/s]MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(), c_options.size(), c_options.data())' convolution_forward_implicit_gemm_v6r1_dlops_nchw_kcyx_nkhw.cpp: HIPRTC_ERROR_COMPILATION (6)
MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION (6), source file: convolution_forward_implicit_gemm_v6r1_dlops_nchw_kcyx_nkhw.cpp
MIOpen(HIP): Warning [BuildHip] In file included from /tmp/comgr-874f1c/input/convolution_forward_implicit_gemm_v6r1_dlops_nchw_kcyx_nkhw.cpp:1:
In file included from /tmp/comgr-874f1c/include/common_header.hpp:10:
/tmp/comgr-874f1c/include/data_type.hpp:14:10: fatal error: 'limits' file not found
#include <limits> // std::numeric_limits
         ^~~~~~~~
1 error generated when compiling for gfx1100.
MIOpen Error: /MIOpen/src/hipoc/hipoc_program.cpp:304: Code object build failed. Source: convolution_forward_implicit_gemm_v6r1_dlops_nchw_kcyx_nkhw.cpp
  0%|                                                    | 0/20 [00:00<?, ?it/s]
*** Error completing request
*** Arguments: ('task(9pidu8fusenim1o)', '1girl', '', [], 20, 0, False, False, 1, 1, 7, -1.0, -1.0, 0, 0, 0, False, 512, 512, False, 0.7, 2, 'Latent', 0, 0, 0, 0, '', '', [], <gradio.routes.Request object at 0x7f1e5c312800>, 0, False, False, 'positive', 'comma', 0, False, False, '', 1, '', [], 0, '', [], 0, '', [], True, False, False, False, 0) {}
    Traceback (most recent call last):
      File "/home/penny/stable-diffusion-webui/modules/call_queue.py", line 58, in f
        res = list(func(*args, **kwargs))
      File "/home/penny/stable-diffusion-webui/modules/call_queue.py", line 37, in f
        res = func(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/modules/txt2img.py", line 62, in txt2img
        processed = processing.process_images(p)
      File "/home/penny/stable-diffusion-webui/modules/processing.py", line 677, in process_images
        res = process_images_inner(p)
      File "/home/penny/stable-diffusion-webui/modules/processing.py", line 794, in process_images_inner
        samples_ddim = p.sample(conditioning=p.c, unconditional_conditioning=p.uc, seeds=p.seeds, subseeds=p.subseeds, subseed_strength=p.subseed_strength, prompts=p.prompts)
      File "/home/penny/stable-diffusion-webui/modules/processing.py", line 1054, in sample
        samples = self.sampler.sample(self, x, conditioning, unconditional_conditioning, image_conditioning=self.txt2img_image_conditioning(x))
      File "/home/penny/stable-diffusion-webui/modules/sd_samplers_kdiffusion.py", line 464, in sample
        samples = self.launch_sampling(steps, lambda: self.func(self.model_wrap_cfg, x, extra_args={
      File "/home/penny/stable-diffusion-webui/modules/sd_samplers_kdiffusion.py", line 303, in launch_sampling
        return func()
      File "/home/penny/stable-diffusion-webui/modules/sd_samplers_kdiffusion.py", line 464, in <lambda>
        samples = self.launch_sampling(steps, lambda: self.func(self.model_wrap_cfg, x, extra_args={
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/utils/_contextlib.py", line 115, in decorate_context
        return func(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/repositories/k-diffusion/k_diffusion/sampling.py", line 145, in sample_euler_ancestral
        denoised = model(x, sigmas[i] * s_in, **extra_args)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
        return self._call_impl(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
        return forward_call(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/modules/sd_samplers_kdiffusion.py", line 183, in forward
        x_out = self.inner_model(x_in, sigma_in, cond=make_condition_dict(cond_in, image_cond_in))
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
        return self._call_impl(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
        return forward_call(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/repositories/k-diffusion/k_diffusion/external.py", line 112, in forward
        eps = self.get_eps(input * c_in, self.sigma_to_t(sigma), **kwargs)
      File "/home/penny/stable-diffusion-webui/repositories/k-diffusion/k_diffusion/external.py", line 138, in get_eps
        return self.inner_model.apply_model(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/modules/sd_hijack_utils.py", line 17, in <lambda>
        setattr(resolved_obj, func_path[-1], lambda *args, **kwargs: self(*args, **kwargs))
      File "/home/penny/stable-diffusion-webui/modules/sd_hijack_utils.py", line 28, in __call__
        return self.__orig_func(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/repositories/stable-diffusion-stability-ai/ldm/models/diffusion/ddpm.py", line 858, in apply_model
        x_recon = self.model(x_noisy, t, **cond)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
        return self._call_impl(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
        return forward_call(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/repositories/stable-diffusion-stability-ai/ldm/models/diffusion/ddpm.py", line 1335, in forward
        out = self.diffusion_model(x, t, context=cc)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
        return self._call_impl(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
        return forward_call(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/modules/sd_unet.py", line 91, in UNetModel_forward
        return ldm.modules.diffusionmodules.openaimodel.copy_of_UNetModel_forward_for_webui(self, x, timesteps, context, *args, **kwargs)
      File "/home/penny/stable-diffusion-webui/repositories/stable-diffusion-stability-ai/ldm/modules/diffusionmodules/openaimodel.py", line 797, in forward
        h = module(h, emb, context)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
        return self._call_impl(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
        return forward_call(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/repositories/stable-diffusion-stability-ai/ldm/modules/diffusionmodules/openaimodel.py", line 82, in forward
        x = layer(x, emb)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
        return self._call_impl(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
        return forward_call(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/repositories/stable-diffusion-stability-ai/ldm/modules/diffusionmodules/openaimodel.py", line 249, in forward
        return checkpoint(
      File "/home/penny/stable-diffusion-webui/repositories/stable-diffusion-stability-ai/ldm/modules/diffusionmodules/util.py", line 121, in checkpoint
        return CheckpointFunction.apply(func, len(inputs), *args)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/autograd/function.py", line 539, in apply
        return super().apply(*args, **kwargs)  # type: ignore[misc]
      File "/home/penny/stable-diffusion-webui/repositories/stable-diffusion-stability-ai/ldm/modules/diffusionmodules/util.py", line 136, in forward
        output_tensors = ctx.run_function(*ctx.input_tensors)
      File "/home/penny/stable-diffusion-webui/repositories/stable-diffusion-stability-ai/ldm/modules/diffusionmodules/openaimodel.py", line 262, in _forward
        h = self.in_layers(x)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
        return self._call_impl(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
        return forward_call(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/container.py", line 217, in forward
        input = module(input)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
        return self._call_impl(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
        return forward_call(*args, **kwargs)
      File "/home/penny/stable-diffusion-webui/extensions-builtin/Lora/networks.py", line 376, in network_Conv2d_forward
        return torch.nn.Conv2d_forward_before_network(self, input)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/conv.py", line 460, in forward
        return self._conv_forward(input, self.weight, self.bias)
      File "/home/penny/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/conv.py", line 456, in _conv_forward
        return F.conv2d(input, weight, bias, self.stride,
    RuntimeError: miopenStatusUnknownError

---


---

### 评论 #4 — evshiron (2023-07-30T16:21:38Z)

https://are-we-gfx1100-yet.github.io/post/a1111-webui/#fatal-error-limits-file-not-found

---

### 评论 #5 — PennyFranklin (2023-07-31T01:36:37Z)

It works well after installing libstdc++-12-dev.. So maybe in the very beginning just install this thing and the problem will be solved, but I don't realize and try again over again in vain 🤡 Thanks a lot. 

---
