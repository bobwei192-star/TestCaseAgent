# Regression in rocm 5.3 and newer for gfx1010

> **Issue #2527**
> **状态**: closed
> **创建时间**: 2023-10-05T20:01:29Z
> **更新时间**: 2024-11-14T19:08:39Z
> **关闭时间**: 2024-11-14T19:08:39Z
> **作者**: DGdev91
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2527

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Since when pytorch 2 was officially released, i wasn't able to run it on my 5700XT, while i was previously able to use it just fine on pytorch 1.13.1 by setting "export HSA_OVERRIDE_GFX_VERSION=10.3.0"
There are many reporting the same issue on the 5000 series, like for example
https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/6420

--precison-full and --no-half are also needed because the card seems like can't use fp16 on linux/rocm, as already reported here https://github.com/RadeonOpenCompute/ROCm/issues/1857

i also read about the PCI atomics requirement, following this issue https://github.com/pytorch/pytorch/issues/103973
....But that doesn't seems to be my case. the command "grep flags /sys/class/kfd/kfd/topology/nodes/*/io_links/0/properties" returns:
```
/sys/class/kfd/kfd/topology/nodes/0/io_links/0/properties:flags 3
/sys/class/kfd/kfd/topology/nodes/1/io_links/0/properties:flags 1
```
Also, i tried to compile pytorch using the new "-mprintf-kind=buffered" flag, but it didn't change anything.



Finally, i recently found out that pytorch 2 works just fine on gfx1010 if that's compiled by rocm 5.2, as suggested here https://github.com/pytorch/pytorch/issues/106728



---

## 评论 (66 条)

### 评论 #1 — langyuxf (2023-10-06T08:53:13Z)

What's your motivation to use newer ROCm? Expect better performance?

---

### 评论 #2 — DGdev91 (2023-10-06T09:41:52Z)

> What's your motivation to use newer ROCm? Expect better performance?

Well, for example to be able to use the official pytorch builds instead of using old nighties or compliling from source.

---

### 评论 #3 — kode54 (2023-11-06T07:59:29Z)

Also, PyTorch deleted their rocm5.2 repo, so all that's available now is the broken 5.6.

Edit: Never mind, I missed that the relevant repositories are specific to Python 3.10.

---

### 评论 #4 — kmsedu (2023-11-16T23:57:09Z)

@hongxiayang 

> Good to hear you make it work, though with the old version. Firstly, I am not sure whether your problem is related to PCIe atomics, or it is just related to gfx arch (1010 is not in the list of compiled targets of the recent wheels). I would hope the 5.7 wheels we build will work if the problem is related to atomics. If you don't have atomics issue, then we should discuss in a different issue.

This is not an atomics issue for gfx1010 users, 

```bash
λ ~/ grep flags /sys/class/kfd/kfd/topology/nodes/*/io_links/0/properties                                                                                                              INSERT
flags 1
```

For 1010 users, my understanding is that there is no official target. We have had to use the `HSA_OVERRIDE_GFX_VERSION` hack to allow ROCm to function at all. Ever since the release of ROCm5.3, some change in memory access code for the gfx1030 arch has prevented us from using this hack, due to OOB errors.

https://github.com/pytorch/pytorch/issues/103973 caught my eye (and likely other users with similar consumer GPUs) because it's the first issue stating that functionality was lost beyond torch1.13+rocm5.2 that has had a thorough looking at.

In addition, the (greatly appreciated) work of @jeffdaily was the first step we've seen with regards to bumping up the usable version of PyTorch for us.

I understand that the work required to isolate and undo whatever memory access changes took place between 5.2-5.3 is probably more than what its worth, considering AMD's stance on maintaining compat for older GPUs, as well as possibly breaking the actually supported gfx1030 GPUs. Therefore we've been left to fend for ourselves a little.

That's how the issue got a little hijacked, apologies for the intrusion there. 

I would say that this issue would be the appropriate place for any continued conversation on the matter. :+1: 

---

### 评论 #5 — hongxiayang (2023-11-17T00:42:51Z)

ok, we will tackle this issue next @kmsedu @DGdev91 

---

### 评论 #6 — hongxiayang (2023-11-17T16:13:49Z)

Have you tried to simulate gfx906, like:
```
export HSA_OVERRIDE_GFX_VERSION=9.0.6
```


---

### 评论 #7 — kmsedu (2023-11-17T16:39:34Z)

@hongxiayang

> Have you tried to simulate gfx906, like:
> 
> ```
> export HSA_OVERRIDE_GFX_VERSION=9.0.6
> ```

Results below:

```
(57venv) λ ~/ai/stable-diffusion-webui/ master* python --version                                                                                                                       INSERT
Python 3.10.6

(57venv) λ ~/ai/stable-diffusion-webui/ master* pip list | grep rocm                                                                                                                   INSERT
torch                     2.2.0.dev20231114+rocm5.7
torchvision               0.17.0+rocm5.7

(57venv) λ ~/ai/stable-diffusion-webui/ master* HSA_OVERRIDE_GFX_VERSION=9.0.6 python mnist_main.py --dry-run                                                                          INSERT
use_cuda=True arg no_cuda=False cuda available=True
[1]    141921 segmentation fault (core dumped)  HSA_OVERRIDE_GFX_VERSION=9.0.6 python mnist_main.py --dry-run
```

Stack trace from coredump here:

```
                Found module linux-vdso.so.1 with build-id: aa98f5cb7cb88a767d1a384eb7b00d363d9d711e
                Found module libfribidi.so with build-id: 6e075a666e1da8ffdb948d734e75d82b1b6dc0fb
                Found module librt.so.1 with build-id: 1e261495981090dca22c9006c3218baead278c7a
                Found module ld-linux-x86-64.so.2 with build-id: 9718d3757f00d2366056830aae09698dbd35e32c
                Found module libc.so.6 with build-id: a43bfc8428df6623cd498c9c0caeb91aec9be4f9
                Found module libm.so.6 with build-id: d2c7d1fdefc7a876b6017c090ccd55fb21e8d77f
                Found module libutil.so.1 with build-id: 24f02e478ddf82435d8c5e0d7eb96f8338f2670b
                Found module libdl.so.2 with build-id: 8ab13ce8a1e6a9b18a844da65688e882f3eb132d
                Found module libpthread.so.0 with build-id: 81f46d553e2f7c999e43c3eede73a822bc8d5d93
                Stack trace of thread 141921:
                #0  0x00007f4fb826614e n/a (/home/kms/ai/stable-diffusion-webui/57venv/lib/python3.10/site-packages/torch/lib/libamdhip64.so + 0x26614e)
```



---

### 评论 #8 — hongxiayang (2023-11-17T17:31:22Z)

Thanks for trying. Next thing we can try is to build pytorch on rocm from source. Since you don't have PCIe atomics issue, we will use official pytorch repository. Here is instructions:

1) start another terminal, start a new container of (rocm/pytorch:latest-base) with the parameters using the instruction above
```
sudo docker run -it --network=host --device=/dev/kfd --device=/dev/dri --group-add=video --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --shm-size 8G -u root rocm/pytorch:latest-base
```

(2) clone the pytorch inside your docker container
```
git clone --recursive https://github.com/pytorch/pytorch.git
cd pytorch
python tools/amd_build/build_amd.py 
PYTORCH_ROCM_ARCH=gfx1010 python setup.py develop
```
(3) run the test again inside pytorch folder.



---

### 评论 #9 — kmsedu (2023-11-17T19:50:28Z)

I have compiled torch 2.2.0a0+git6849d75 and torchvision 0.17.0a0+4433680.
Below is the output:

```
root@mainPC:/home/pytorch# pip list | grep torch
torch                    2.2.0a0+git6849d75 /opt/conda/envs/py_3.9/lib/python3.9/site-packages
torchvision              0.17.0a0+4433680   /home/vision

root@mainPC:/home/pytorch# python examples/mnist/main.py --dry-run
Segmentation fault (core dumped)

root@mainPC:/home/pytorch# python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_arch_list())"
True
['gfx1010']
```

If a stack trace could be of use, please let me know and I'll figure out how to setup coredumpctl in the docker container.

---

### 评论 #10 — DGdev91 (2023-12-09T02:53:39Z)

Any news on this? need more infos?

---

### 评论 #11 — DGdev91 (2023-12-18T20:39:47Z)

I tried it also with the new ROCm 6.0, it doesn't really seem to change much. works fine with an old nigtly build of pytorch 2.0 compiled on rocm5.2, but crashes on the last --pre pytorch
`Memory access fault by GPU node-1 (Agent handle: 0x968d080) on address 0x7fa860641000. Reason: Page not present or supervisor privilege.
`
happens with both HSA_OVERRIDE_GFX_VERSION=10.3.0 and without. but it's probably needed since it doesn't work on the 5.2 build without it.

---

### 评论 #12 — theron29 (2024-01-11T20:47:34Z)

> `Memory access fault by GPU node-1 (Agent handle: 0x968d080) on address 0x7fa860641000. Reason: Page not present or supervisor privilege. `
> happens with both HSA_OVERRIDE_GFX_VERSION=10.3.0 and without.

I made this work with HSA_OVERRIDE_GFX_VERSION=9.4.0 (and I had to find this out purely by trial & error....).
It is not fully stable, but it worked with SD within at least two separate system boots...

---

### 评论 #13 — DGdev91 (2024-01-26T10:55:40Z)

> > `Memory access fault by GPU node-1 (Agent handle: 0x968d080) on address 0x7fa860641000. Reason: Page not present or supervisor privilege. `
> > happens with both HSA_OVERRIDE_GFX_VERSION=10.3.0 and without.
> 
> I made this work with HSA_OVERRIDE_GFX_VERSION=9.4.0 (and I had to find this out purely by trial & error....). It is not fully stable, but it worked with SD within at least two separate system boots...

I changed the gpu on my machine and cannot verify that. @kmsedu can you?

Aldo, are you sure you were actually running on the last pytorch version? In automatic1111's webui there's a workaround for making it use by default an older pytorch version compiled on ROCm 5.2 on older navi cards like the RX5700xt (i know that well because... I wrote that workaround).

---

### 评论 #14 — theron29 (2024-01-26T17:40:15Z)

> Aldo, are you sure you were actually running on the last pytorch version? In automatic1111's webui there's a workaround for making it use by default an older pytorch version compiled on ROCm 5.2 on older navi cards like the RX5700xt (i know that well because... I wrote that workaround).

Hey there. No, I'm not running on the latest version of pytorch.
And yes, you are correct, I've run this on/witth automatic1111's webui with (your :pray: :heart:) workaround in place. The env HSA_OVERRIDE_GFX_VERSION=9.4.0 made the solution to automatically downgrade the version of pytorch to the version built with rocm 5.2.

---

### 评论 #15 — hongxiayang (2024-01-26T18:39:18Z)

Since gfx1010 is not in the support gfx target list (  https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus), the latest versions may not work for your gpu. 


---

### 评论 #16 — DGdev91 (2024-01-28T17:57:11Z)

> Hey there. No, I'm not running on the latest version of pytorch. And yes, you are correct, I've run this on/witth automatic1111's webui with (your 🙏 ❤️) workaround in place. The env HSA_OVERRIDE_GFX_VERSION=9.4.0 made the solution to automatically downgrade the version of pytorch to the version built with rocm 5.2.

Ok, then you have just the same problem. We know that anything compiled using Rocm 5.2 or older works just fine on that card.
If you try to force it to a newer version in webui_user.sh probably it's not going to work.
Also, usually HSA_OVERRIDE_GFX_VERSION=10.3.0 is used for the override.
Automatic1111's webui should force it automatically for older gpus, so maybe you were actually using that.

> Since gfx1010 is not in the support gfx target list ( https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus), the latest versions may not work for your gpu.

I know. But it's still wierd that a gpu wich worked perfectly fine with pytorch compiled for an older romc version + HSA_OVERRIDE_GFX_VERSION=10.3.0 (even if not officially  supported) suddently stops working on everything compiled using something newer.
I also tried to pick up an old docker image with rocm 5.2 but it doesn't seems able to compile it.

This is also true for other softwares wich rely on rocm, like llama-cpp with hipblas support

---

### 评论 #17 — cgmb (2024-01-28T22:29:37Z)

> I know. But it's still wierd that a gpu wich worked perfectly fine with pytorch compiled for an older romc version + HSA_OVERRIDE_GFX_VERSION=10.3.0 (even if not officially supported) suddently stops working on everything compiled using something newer.

When you use `HSA_OVERRIDE_GFX_VERSION=10.3.0`, you are telling the ROCm runtime to pretend that your RDNA 1 GPU is an RDNA 2 GPU. The weird thing is that ever worked, not that it stopped working.

> This is also true for other softwares wich rely on rocm, like llama-cpp with hipblas support

If you're on Debian 13 or Ubuntu 23.10 or later, use libhipblas-dev. The OS-provided packages have gfx1010 enabled.

---

### 评论 #18 — DGdev91 (2024-01-28T23:43:20Z)

> If you're on Debian 13 or Ubuntu 23.10 or later, use libhipblas-dev. The OS-provided packages have gfx1010 enabled.

Isn't that just the same as installing the rocm stack (or at least part of it)? It depends on rocblas, wich depends on hip, wich depends on the HSA runtime, and so on.
Also, as i already wrote, the problem isn't the rocm version installed, but the one used to compile the software. And compiling them using the old version usually isn't straightforward/possibile.

---

### 评论 #19 — cgmb (2024-01-29T04:55:28Z)

> Isn't that just the same as installing the rocm stack (or at least part of it)? It depends on rocblas, wich depends on hip, wich depends on the HSA runtime, and so on.

HIP works fine on gfx1010. It's mainly just that the math libraries in AMD's binary packages are (mostly) not built for that architecture.

When I packaged rocBLAS for Debian, I specified for it to be built for gfx1010. I also packaged the test suites for rocBLAS and hipBLAS, and ran them on both the RX 5700 XT, and Radeon W5700. All tests passed.

Of course, nobody has packaged MIOpen for Debian yet, so while the OS packages should be sufficient for llama-cpp, they are not sufficient yet for something like PyTorch.

---

### 评论 #20 — DGdev91 (2024-01-29T17:08:57Z)

> > Isn't that just the same as installing the rocm stack (or at least part of it)? It depends on rocblas, wich depends on hip, wich depends on the HSA runtime, and so on.
> 
> HIP works fine on gfx1010. It's mainly just that the math libraries in AMD's binary packages are (mostly) not built for that architecture.
> 
> When I packaged rocBLAS for Debian, I specified for it to be built for gfx1010. I also packaged the test suites for rocBLAS and hipBLAS, and ran them on both the RX 5700 XT, and Radeon W5700. All tests passed.
> 
> Of course, nobody has packaged MIOpen for Debian yet, so while the OS packages should be sufficient for llama-cpp, they are not sufficient yet for something like PyTorch.

Last time i tried i had a memory access error (just like the newer pytorch versions) when trying to load a model in lama.cpp with both hipblas and clblast offloading, while the second worked fine on Windows. I had the same problem in both ArchLinux and Ubuntu.
But it can easly be a totally different issue.

---

### 评论 #21 — DGdev91 (2024-01-29T21:15:37Z)

> Since gfx1010 is not in the support gfx target list ( https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus), the latest versions may not work for your gpu.

> When you use `HSA_OVERRIDE_GFX_VERSION=10.3.0`, you are telling the ROCm runtime to pretend that your RDNA 1 GPU is an RDNA 2 GPU. The weird thing is that ever worked, not that it stopped working.

Anyway, i'm perfectly aware of that. You are right, that card wasn't never supposed to work on rocm in the first place and it works with some older pytorch builds just thanks to a workaround.
That's also true for every consumer-grade amd gpu other than the 7900xt and 7900xtx, wich many users are still using thanks to the same workaround.

But after this reply on november 17th
> ok, we will tackle this issue next @kmsedu @DGdev91

I was expecting to see something on this matter anyway.


---

### 评论 #22 — cgmb (2024-01-29T22:10:15Z)

> Last time i tried i had a memory access error [...] when trying to load a model in lama.cpp with both hipblas and clblast offloading, while the second worked fine on Windows. I had the same problem in both ArchLinux and Ubuntu.

To be clear, on Ubuntu were you using `libhipblas-dev` (which installs to `/usr/lib/x86_64-linux-gnu`) or were you using `hipblas-dev` (which installs to `/opt/rocm/lib`)? If you were using `libhipblas-dev`, I'm very interested in learning more. Could you provide some instructions on how to reproduce the problem?

> That's also true for every consumer-grade amd gpu other than the 7900xt and 7900xtx, wich many users are still using thanks to the same workaround.

Using `HSA_OVERRIDE_GFX_VERSION=10.3.0` on RDNA 2 GPUs is fundamentally different from using it on RDNA 1 GPUs. All RDNA 2 GPUs use the exact same instructions, but there's a bunch of differences between the instructions used on RDNA 1 and RDNA 2 GPUs. The only way to undo this 'regression' with `HSA_OVERRIDE_GFX_VERSION` would be to change LLVM so that the compiler only uses instructions available on RDNA 1, even when asked to compile for RDNA 2. That's not going to happen.

A better path to getting gfx1010 enabled in PyTorch would be to build the ROCm math and AI libraries for gfx1010 (or gfx10.1-generic). That is probably not going to happen in AMD's official packages, but there are other groups building and distributing ROCm packages. I can't speak for other distributions, but I expect to have it enabled later this year on Debian. With that said, my work with Debian is strictly volunteer work (on top of my full-time job), so don't expect it to happen quickly.

---

### 评论 #23 — DGdev91 (2024-01-29T22:51:14Z)

> > Last time i tried i had a memory access error [...] when trying to load a model in lama.cpp with both hipblas and clblast offloading, while the second worked fine on Windows. I had the same problem in both ArchLinux and Ubuntu.
> 
> To be clear, on Ubuntu were you using `libhipblas-dev` (which installs to `/usr/lib/x86_64-linux-gnu`) or were you using `hipblas-dev` (which installs to `/opt/rocm/lib`)? If you were using `libhipblas-dev`, I'm very interested in learning more. Could you provide some instructions on how to reproduce the problem?
> 
> > That's also true for every consumer-grade amd gpu other than the 7900xt and 7900xtx, wich many users are still using thanks to the same workaround.
> 
> Using `HSA_OVERRIDE_GFX_VERSION=10.3.0` on RDNA 2 GPUs is fundamentally different from using it on RDNA 1 GPUs. All RDNA 2 GPUs use the exact same instructions, but there's a bunch of differences between the instructions used on RDNA 1 and RDNA 2 GPUs. The only way to undo this 'regression' with `HSA_OVERRIDE_GFX_VERSION` would be to change LLVM so that the compiler only uses instructions available on RDNA 1, even when asked to compile for RDNA 2. That's not going to happen.
> 
> A better path to getting gfx1010 enabled in PyTorch would be to build the ROCm math and AI libraries for gfx1010 (or gfx10.1-generic). That is probably not going to happen in AMD's official packages, but there are other groups building and distributing ROCm packages. I can't speak for other distributions, but I expect to have it enabled later this year on Debian. With that said, my work with Debian is strictly volunteer work (on top of my full-time job), so don't expect it to happen quickly.

Ok, now it's more clear.
I can confirm i used hipblas-dev

I was also thinking that the hsa override flag was needed for rocblas too, because i couldn't use it on native 1010 since the libs for 1010 were missing in the official packages.

I also just found this PR wich has been merged just 5 days ago wich makes life a bit more simple for compiling the tensile libs for 1010
https://github.com/ROCm/Tensile/pull/1862

---

### 评论 #24 — Zakhrov (2024-04-17T12:45:25Z)

Now that ROCM 6.1 is out, I tried it with the latest pytorch nightly (which still is built with Rocm 6.0) and this is the error I get when trying to run ComfyUI:
``` 
:3:hip_platform.cpp         :211 : 14629861941 us: [pid:31113 tid:0x7fa5a37fe700] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :668 : 14629861947 us: [pid:31113 tid:0x7fa5a37fe700]  hipLaunchKernel ( 0x7fa9706d5550, {57,1,1}, {256,1,1}, 0x7fa5a37fc9a0, 0, stream:<null> ) 
:3:hip_module.cpp           :669 : 14629861952 us: [pid:31113 tid:0x7fa5a37fe700] hipLaunchKernel: Returned hipErrorInvalidDeviceFunction : 
:3:hip_error.cpp            :35  : 14629861955 us: [pid:31113 tid:0x7fa5a37fe700]  hipGetLastError (  ) 
:3:hip_error.cpp            :35  : 14629861957 us: [pid:31113 tid:0x7fa5a37fe700]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :652 : 14629866892 us: [pid:31113 tid:0x7fa5a37fe700]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :656 : 14629866904 us: [pid:31113 tid:0x7fa5a37fe700] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :652 : 14629866934 us: [pid:31113 tid:0x7fa5a37fe700]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :656 : 14629866937 us: [pid:31113 tid:0x7fa5a37fe700] hipSetDevice: Returned hipSuccess : 
!!! Exception during processing !!!
Traceback (most recent call last):
  File "/home/aaron/Projects/personal/ComfyUI/execution.py", line 151, in recursive_execute
    output_data, output_ui = get_output_data(obj, input_data_all)
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aaron/Projects/personal/ComfyUI/execution.py", line 81, in get_output_data
    return_values = map_node_over_list(obj, input_data_all, obj.FUNCTION, allow_interrupt=True)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aaron/Projects/personal/ComfyUI/execution.py", line 74, in map_node_over_list
    results.append(getattr(obj, func)(**slice_dict(input_data_all, i)))
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aaron/Projects/personal/ComfyUI/nodes.py", line 1378, in sample
    return common_ksampler(model, noise_seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise, disable_noise=disable_noise, start_step=start_at_step, last_step=end_at_step, force_full_denoise=force_full_denoise)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aaron/Projects/personal/ComfyUI/nodes.py", line 1314, in common_ksampler
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aaron/Projects/personal/ComfyUI/comfy/sample.py", line 37, in sample
    samples = sampler.sample(noise, positive, negative, cfg=cfg, latent_image=latent_image, start_step=start_step, last_step=last_step, force_full_denoise=force_full_denoise, denoise_mask=noise_mask, sigmas=sigmas, callback=callback, disable_pbar=disable_pbar, seed=seed)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aaron/Projects/personal/ComfyUI/comfy/samplers.py", line 755, in sample
    return sample(self.model, noise, positive, negative, cfg, self.device, sampler, sigmas, self.model_options, latent_image=latent_image, denoise_mask=denoise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aaron/Projects/personal/ComfyUI/comfy/samplers.py", line 657, in sample
    return cfg_guider.sample(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aaron/Projects/personal/ComfyUI/comfy/samplers.py", line 644, in sample
    output = self.inner_sample(noise, latent_image, device, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/aaron/Projects/personal/ComfyUI/comfy/samplers.py", line 616, in inner_sample
    if latent_image is not None and torch.count_nonzero(latent_image) > 0: #Don't shift the empty latent image.
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
Compile with TORCH_USE_HIP_DSA to enable device-side assertions.


Prompt executed in 6.49 seconds
```

setting HSA_OVERRIDE_GFX_VERSION to 10.3.0 still doesn't work it just maxes out the GPU clock and graphics pipeline but doesn't actually do anything.

---

### 评论 #25 — Zakhrov (2024-04-22T07:19:51Z)

I tried it again with the pytorch wheels from https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1/ which have been compiled against ROCM 6.1 and they exhibit the same issue. Will try to compile pytorch from source next. In the meantime, here is the full output of the ComfyUI command
[pytorch_error.log](https://github.com/ROCm/ROCm/files/15058975/pytorch_error.log)
Using ``HSA_OVERRIDE_GFX_VERSION=10.3.0`` still just maxes out the GPU clock and doesn't actually do anything, while setting it to 11.0.0 or to 9.4.0 causes a GPU reset and locks my laptop up until I hard reboot it

---

### 评论 #26 — Zakhrov (2024-04-23T12:48:30Z)

Well, that was a colossal waste of time, looks like rocBLAS doesn't ship with [https://github.com/ROCm/Tensile/pull/1862](https://github.com/ROCm/Tensile/pull/1862) at least not for the SLES/OpenSUSE packages
```
rocBLAS error: Cannot read /opt/rocm/lib/rocblas/library/TensileLibrary.dat: No such file or directory for GPU arch : gfx1010
 List of available TensileLibrary Files : 
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx900.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx906.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx908.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx90a.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx940.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx941.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx942.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1102.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1101.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1030.dat"
"/opt/rocm/lib/rocblas/library/TensileLibrary_lazy_gfx1100.dat"
Aborted (core dumped)
```
Going to try to build rocBLAS and Tensile now

---

### 评论 #27 — Zakhrov (2024-04-24T08:07:57Z)

Pytorch wasn't building because of [https://github.com/ROCm/aotriton/issues/18](https://github.com/ROCm/aotriton/issues/18) so I hacked it out and made pytorch compile without aotriton. This actually works and I'm able to run ComfyUI!
## Notes:
* rocBLAS must be built with gfx1010 Tensile libraries and installed into ROCM_PATH, the SLES package does not include them
* Because of my dirty hacks, pytorch does not have flash or memory efficient attention, so ``--use-pytorch-cross-attention`` can lead to HIP out of memory errors, subquadratic attention seems to work better.
* Forcing fp16 works and gives proper images
* Forcing fp32 also works
* You don't need the HSA_OVERRIDE_GFX_VERSION anymore, it works with ``python main.py`` 
* Performance is slower than pytorch built against ROCM 5.2 (although this could be because of thermal throttling) but seems to be much more stable (no random GPU resets despite both the CPU and GPU running near the thermal throttle limit - so far)

I'm trying again with aotriton patched with the fix @xinyazhang suggested to see if that helps with easier/more straightforward building and possibly with performance.


---

### 评论 #28 — Zakhrov (2024-04-24T09:09:28Z)

OK after a lot of trial and error I've managed to get a consistent set of steps.

## Steps:
* Build and install rocBLAS to get the Tensile library to build against gfx1010 (can skip if your distribution already builds it, the official SLES package doesnt) use ``cmake -B build -S . -DCMAKE_INSTALL_PREFIX=/opt/rocm-6.1.0 -DAMDGPU_TARGETS="gfx1010"``
* Patch the `comgr` library with the code from here: [https://github.com/GZGavinZhao/ROCm-CompilerSupport/commit/3419d519fca9b03ba82dde037cc4600348a9d71d](https://github.com/GZGavinZhao/ROCm-CompilerSupport/commit/3419d519fca9b03ba82dde037cc4600348a9d71d)
* Build `comgr` and install it to `ROCM_PATH`
* Build and install  rocSPARSE for the `gfx1010` target
* Start the build process for pytorch from source against your system rocm. I used ``ROCM_PATH=/opt/rocm USE_ROCM=1 PYTORCH_ROCM_ARCH=gfx1010 python3 setup.py develop`` 
* Abort the pytorch build process once it completes configuring aotriton, and then patch aotriton with this: [https://github.com/ROCm/aotriton/commit/0873896ab690d5767975f2bb9ab850b1a103b26e](https://github.com/ROCm/aotriton/commit/0873896ab690d5767975f2bb9ab850b1a103b26e) Changing the commit hash in ``pytorch/External/aotriton.cmake`` didn't work for me, so I manually edited the file
* Start the build process again. This can take an ***insanely long*** time, thanks to aotriton building triton from source, and compiling a whole bunch of HSA command objects for the MI200 and MI300X. Disabling ``USE_FLASH_ATTENTION`` will still cause it to be built so might as well keep it enabled. Stopping and starting the build process will cause all of those HSA command objects / HIP kernels to recompile, so be prepared for pytorch to take over an hour to build
* Once pytorch has been successfully built and installed, build and install torchvision from source. This won't take as long, but it will need to be done every time you update the pytorch build
* With pytorch and torchvision built and installed, you can run ComfyUI or any other pytorch workload, without needing the ``HSA_OVERRIDE_GFX_VERSION`` variable. Also gfx1010 will now work in both fp16 and fp32 modes, and it should be a little more stable without random SDMA queue timeouts and GPU resets

## Caveats:
* Pytorch's SDP backend for cross attention does not work and fails with the following error: 
 ```
 torch.OutOfMemoryError: HIP out of memory. Tried to allocate 14.00 MiB. GPU 0 has a total capacity of 5.98 GiB of which 6.00 MiB is free. Of the allocated memory 5.63 GiB is allocated by PyTorch, and 190.05 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)

```
* The expandable memory segments that pytorch suggests you set, also does not work and fails with this error:
```
UserWarning: expandable_segments not supported on this platform (Triggered internally at ../c10/hip/HIPAllocatorConfig.h:29.)

```
* These steps are not something you can easily add into an automated build system or script, as of the time of writing, it requires you to manually edit files in the pytorch build directory **after** a build has partially completed. Furthermore, this **only** targets gfx1010

---------------------------------------------------------------------------

The key takeaway from this exercise is that I would have probably been better off had I not nuked my Windows install and just used DirectML. Needless to say it was both educational and frustrating. Anyway, hopefully this should help others until AMD releases ROCM 6.2 with the fallback libraries in the official rocBLAS packages and the docker images used to build pytorch, and pytorch themselves build pytorch wheels against those 
 


---

### 评论 #29 — daniandtheweb (2024-04-24T10:57:37Z)

That's amazing, could you share the pytorch files you've built? I'm trying to build on Debian Unstable, which is compatible with gfx1010 by default using the rocm libraries, but I'm unable to build correctly (I've probably messed something up in the setup process of the pytorch packages).

---

### 评论 #30 — Zakhrov (2024-04-24T11:31:55Z)

> That's amazing, could you share the pytorch files you've built? I'm trying to build on Debian Unstable, which is compatible with gfx1010 by default using the rocm libraries, but I'm unable to build correctly (I've probably messed something up in the setup process of the pytorch packages).

I'll try to build a wheel from my pytorch setup

---

### 评论 #31 — Zakhrov (2024-04-24T11:58:55Z)

@daniandtheweb here you go: [https://drive.google.com/file/d/1Y2kQ3bnoihs892tHOpXHkvfMQJH_gYa9/view?usp=drive_link](https://drive.google.com/file/d/1Y2kQ3bnoihs892tHOpXHkvfMQJH_gYa9/view?usp=drive_link)
I'm not entirely sure if it will work for you. See my updated caveats

---

### 评论 #32 — Zakhrov (2024-04-24T12:23:07Z)

OK more instability.
Trying to run ComfyUI with the `dpmpp_2m_sde_gpu` sampler and the `karras` scheduler triggers this error:
```
:0:rocdevice.cpp            :2881: 33809159190 us: [pid:7301  tid:0x7fb3acfff700] Callback: Queue 0x7fb168400000 aborting with error : HSA_STATUS_ERROR_MEMORY_APERTURE_VIOLATION: The agent attempted to access memory beyond the largest legal address. code: 0x29

```
I suppose I'll have to build torchsde manually for that to work 


---

### 评论 #33 — Zakhrov (2024-04-24T12:31:47Z)

OK can confirm that the `_gpu` and the `sde` samplers do not work with these workarounds. Perhaps there is more stuff I'm overlooking

---

### 评论 #34 — daniandtheweb (2024-04-24T12:34:33Z)

@Zakhrov try taking a look at this: https://lists.debian.org/debian-ai/2024/02/msg00164.html

---

### 评论 #35 — hongxiayang (2024-04-24T13:23:27Z)

As you might be aware from this documentation (https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus), gfx1010 was not among the supported gfx architectures, and therefore, the behavior is undefined.  You can close this issue.

---

### 评论 #36 — Zakhrov (2024-04-24T16:58:56Z)

> As you might be aware from this documentation (https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus), gfx1010 was not among the supported gfx architectures, and therefore, the behavior is undefined. You can close this issue.

I'm well aware of the supported gfx architectures. What we are following is the advice given here: [https://github.com/ROCm/ROCm/issues/1735#issuecomment-1128314977](https://github.com/ROCm/ROCm/issues/1735#issuecomment-1128314977)

---

### 评论 #37 — Zakhrov (2024-04-25T07:18:53Z)

Update: building rocSPARSE and comgr from source with @GZGavinZhao's patch available here: [https://github.com/GZGavinZhao/ROCm-CompilerSupport/commit/3419d519fca9b03ba82dde037cc4600348a9d71d](https://github.com/GZGavinZhao/ROCm-CompilerSupport/commit/3419d519fca9b03ba82dde037cc4600348a9d71d) got the SDE ksamplers to work in ComfyUI. Performance is still slower than with ROCM 5.2 (probably because of missing MiOpen and Composable Kernels)

---

### 评论 #38 — GZGavinZhao (2024-04-25T14:28:27Z)

![Who pinged me](https://tenor.com/view/who-pinged-me-ping-discord-up-opening-door-gif-20065356.gif)

Ok in all seriousness, this issue should be resolved if ROCm/Tensile#1897 is cherry-picked into a release. I'll open an issue there (ROCm/Tensile#1916). @Zakhrov if you really want to test gfx1010 support, you can try on Solus (the distro that I'm a maintainer for) with Docker. Note that the docker image is experimental/community-maintained so this shouldn't be used for anything serious, just for testing purposes:

```bash
# I personally use podman because I don't need to deal with sudo permission issues,
# but if you're more comfortable with Docker, replace `podman` with `sudo docker`
podman run -it --device=/dev/kfd --device=/dev/dri --group-add=video --group-add=render --group-add=nobody --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined silkeh/solus:devel bash
```

Inside the container, run the following to install PyTorch with ROCm support:
```bash
sudo eopkg ur && sudo eopkg up --ignore-comar -y # similar to sudo apt-get update && sudo apt-get upgrade
sudo eopkg it --ignore-comar pytorch python-torchaudio python-torchvision python-torchtext rocm-info -y
```

Now, you can proceed to run ComfyUI as normal. We didn't test against ComfyUI but we did test against Fooocus, so the process shoudl be similar. I assume you would need to create a `venv` to run ComfyUI. The only change you would have to make is that when creating the `venv` (e.g. `python3 -m venv <rest-of-your-arguments>`, you should add the flag `--system-site-packages`. With Fooocus, it looks something like this:

```bash
# Before everything, check that ROCm is not completely broken
rocminfo
# Assume you're already inside the Fooocus directory 
python3 -m venv venv --system-site-packages
source venv/bin/activate
# You may get warnings about dependencies failed to be uninstalled/updated, but in practice we haven't found this to be problematic
pip3 install -r requirements.txt 
# Now run Fooocus!
```

If you're familiar with Nix, after NixOS/nixpkgs#298388 is merged, you should also be able to use `gfx101*` GPUs with Nix. With PyTorch in particular, this may be a bit difficult due to how Nix handles Python packages, but stuff that are just binary executables like `llama-cpp` should work seamlessly with Nix.

Regarding `composable_kernel`, `gfx1010` is not supported. At Solus, we have a [patch](https://github.com/getsolus/packages/blob/f9f4ad4f3fdd98a44a466f070d83271900f4cb82/packages/c/composable-kernel/package.yml#L49) that enables some sort of support for it, so you may get a little performance boost, though nobody on the Solus team has a GPU to verify this claim :sweat_smile: 

---

### 评论 #39 — Zakhrov (2024-04-25T14:53:49Z)

> Ok in all seriousness, this issue should be resolved if [ROCm/Tensile#1897](https://github.com/ROCm/Tensile/pull/1897) is cherry-picked into a release. I'll open an issue there. @Zakhrov if you really want to test gfx1010 support, you can try on Solus (the distro that I'm a maintainer for) with Docker.


I'm currently on openSUSE 15.5 (which is compatible with packages built for SLES 15 SP5) and I run rocm on bare metal for the most part. Your patch works fine for everything except torchsde workloads - that needs `comgr` and `rocsparse` as well.
> Regarding `composable_kernel`, `gfx1010` is not supported. At Solus, we have a [patch](https://github.com/getsolus/packages/blob/f9f4ad4f3fdd98a44a466f070d83271900f4cb82/packages/c/composable-kernel/package.yml#L49) that enables some sort of support for it, so you may get a little performance boost, though nobody on the Solus team has a GPU to verify this claim 😅


That's what I manually patched in to `composable_kernel` as well. It just finished building, now have to try building MIOpen. I'll report back once I manage to build that



---

### 评论 #40 — GZGavinZhao (2024-04-25T15:04:56Z)

> I'm currently on openSUSE 15.5 (which is compatible with packages built for SLES 15 SP5) and I run rocm on bare metal for the most part. Your patch works fine for everything except torchsde workloads - that needs `comgr` and `rocsparse` as well.

I'm surprised that you need to rebuild `rocSPARSE`. `comgr` is needed because of https://lists.debian.org/debian-ai/2024/02/msg00178.html. In short, ROCm 6.0 changed the behavior such that device code unbundling is handled by `comgr` (which was not patched), but previously the unbundling is done by clr (which was patched). The fix is to simply switch back the behavior to avoid patching `comgr`. I'm not sure why `rocSPARSE` is affected by this.

> That's what I manually patched in to `composable_kernel` as well. It just finished building, now have to try building MIOpen. I'll report back once I manage to build that

I assume that you know you can pass the CMake flag `-DGPU_TARGETS=<your-gpu-target>` to only build for your own GPU. This can save a ton of time.

---

### 评论 #41 — GZGavinZhao (2024-04-25T15:11:19Z)

Wait @Zakhrov are you not on `gfx1010`? The `comgr` patch is only for allowing `gfx1011`, `gfx1012` to run code compiled against `gfx1010`. If you're already on `gfx1010`, the `comgr` patch shouldn't be needed.

---

### 评论 #42 — Zakhrov (2024-04-25T15:37:10Z)

> Wait @Zakhrov are you not on `gfx1010`? The `comgr` patch is only for allowing `gfx1011`, `gfx1012` to run code compiled against `gfx1010`. If you're already on `gfx1010`, the `comgr` patch shouldn't be needed.

I have a Radeon RX 5600M which shows as gfx1010 in rocminfo. Maybe I built rocBLAS wrong the first time around

---

### 评论 #43 — GZGavinZhao (2024-04-25T20:30:31Z)

Good news, ROCm/Tensile#1897 will be included in the ROCm 6.2 release judging from the `release-staging/rocm-rel-6.2` branch at ROCm/Tensile. It seems like no additional ROCm 6.1 releases are planned, so this means `gfx101*` GPUs will likely be fixed in the next (minor) ROCm release.

---

### 评论 #44 — cgmb (2024-04-25T22:59:21Z)

Note that all the system packages on Ubuntu 24.04 have gfx1010 enabled. However, to use PyTorch you still need MIOpen. Once `miopen` and `pytorch-rocm` are packaged for Debian, I will port them to gfx1010 and set up a PPA for Ubuntu 24.04. With that said, performance will probably be quite poor as rocBLAS depends heavily on tuned assembly kernels for optimal performance (and nobody has done tuning for RDNA 1).

---

### 评论 #45 — ppanchad-amd (2024-05-14T20:41:30Z)

@DGdev91 Has your issue been resolved? If so, please close ticket. Thanks!

---

### 评论 #46 — DGdev91 (2024-05-14T22:12:54Z)

> @DGdev91 Has your issue been resolved? If so, please close ticket. Thanks!

I can't really test it anymore, as i changed the gpu some months ago (i now have a 7900XT, working fine)

But according to @GZGavinZhao, the fix will be included in 6.2 release, so i was waiting for someone testing that version as soon it's released, before closing

---

### 评论 #47 — kchousos (2024-06-15T18:01:18Z)

Does anyone have an ETA for ROCm 6.2?

---

### 评论 #48 — waheedi (2024-07-18T21:43:42Z)

> That's what I manually patched in to composable_kernel as well. It just finished building, now have to try building MIOpen. I'll report back once I manage to build that

@Zakhrov So were you able to build it with gfx1010, i could not build it (MIOpen), do i need ck to be already built? 

> Start the build process again. This can take an insanely long time, thanks to aotriton building triton from source, and compiling a whole bunch of HSA command objects for the MI200 and MI300X. Disabling USE_FLASH_ATTENTION will still cause it to be built so might as well keep it enabled. Stopping and starting the build process will cause all of those HSA command objects / HIP kernels to recompile, so be prepared for pytorch to take over an hour to build

there is already a PR going for that part https://github.com/pytorch/pytorch/issues/125230#issuecomment-2211893054



---

### 评论 #49 — waheedi (2024-07-25T17:29:04Z)

> > That's what I manually patched in to composable_kernel as well. It just finished building, now have to try building MIOpen. I'll report back once I manage to build that
> 
> @Zakhrov So were you able to build it with gfx1010, i could not build it (MIOpen), do i need ck to be already built?
> 
> > Start the build process again. This can take an insanely long time, thanks to aotriton building triton from source, and compiling a whole bunch of HSA command objects for the MI200 and MI300X. Disabling USE_FLASH_ATTENTION will still cause it to be built so might as well keep it enabled. Stopping and starting the build process will cause all of those HSA command objects / HIP kernels to recompile, so be prepared for pytorch to take over an hour to build
> 
> there is already a PR going for that part [pytorch/pytorch#125230 (comment)](https://github.com/pytorch/pytorch/issues/125230#issuecomment-2211893054)

Ok I actually managed to build the whole stack for gfx1010, with latest pytorch and all develop rocm 

So I thought I would make an update on that. Thanks a lot anyway.

---

### 评论 #50 — veyn3141 (2024-07-26T06:42:37Z)

@waheedi Amazing, would it be possible to upload the pytorch wheels somewhere?

---

### 评论 #51 — waheedi (2024-07-26T07:00:10Z)

> @waheedi Amazing, would it be possible to upload the pytorch wheels somewhere?

@veyn3141 Amazing what man :), the wheel on its own is not going to help, as that would be bundled with some libraries that you actually won't have with a standard rocm installation so I dont think it would be of any help.

But also I hit a blocker for building the last 200 tasks of torch and right now I'm a bit blocked. #3445



---

### 评论 #52 — TheTrustedComputer (2024-07-31T18:17:22Z)

I have two 5500 XTs (the 8GB model to be specific, not the 4GB one) that I regularly run machine learning applications on both cards. This bug meant I had to compile affected ROCm versions and the latest PyTorch from source to target the `gfx1012` architecture to restore functionality.

I wasted many long hours patching pieces of code and tweaking build flags to make the process successful from start to finish. I was relieved to find the PyTorch test suites were working without the need to set the `HSA_OVERRIDE_GFX_VERSION` environment variable.

I look forward to an official upstream fix sooner or later. Hopefully, this will save users time by not having to rebuild everything from scratch when a future problem occurs. Better a late fix than no fix.

---

### 评论 #53 — TheTrustedComputer (2024-08-02T20:00:02Z)

> Does anyone have an ETA for ROCm 6.2?

It has been released just about now. Whether it fixes the issue remains to be seen.

---

### 评论 #54 — genehand (2024-08-03T17:38:58Z)

Replaced ollama compiled with vulkan support with rocm 6.2 and the 0.3.3 release binary. A quick benchmark went from ~18.7 token/s to 45.6 😎 

```
time=2024-08-03T10:42:38.769-07:00 level=INFO source=payload.go:44 msg="Dynamic LLM libraries [cpu cpu_avx cpu_avx2 cuda_v11 rocm_v60102]"
time=2024-08-03T10:42:38.769-07:00 level=INFO source=gpu.go:205 msg="looking for compatible GPUs"
time=2024-08-03T10:42:38.775-07:00 level=INFO source=amd_linux.go:345 msg="amdgpu is supported" gpu=0 gpu_type=gfx1010
time=2024-08-03T10:42:38.775-07:00 level=INFO source=types.go:105 msg="inference compute" id=0 library=rocm compute=gfx1010 driver=6.8 name=1002:731f total="8.0 GiB" available="8.0 GiB"
```

Edit: re-ran without whisper running

---

### 评论 #55 — GZGavinZhao (2024-08-04T13:17:06Z)

I don't have the hardware to test right now, but since ROCm/Tensile#1897 is included in the 6.2 release, rocBLAS should now work fine on RDNA1 (gfx101*) hardware. This means that running LLMs such as `llama-cpp` should now work properly. Other ML workflows such as stable diffusion that need libraries other than rocBLAS (e.g. CK and MIOpen) may or may not work.

---

### 评论 #56 — Zakhrov (2024-08-05T08:32:52Z)

The official pytorch wheels don't work. I suppose they need to be built against rocm 6.2. I am rebuilding pytorch locally against my new rocm 6.2 installation

---

### 评论 #57 — ethragur (2024-08-06T21:03:11Z)

Building the pytorch wheels via docker/podman worked:
https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.2.0/install/3rd-party/pytorch-install.html#using-the-pytorch-upstream-docker-file

1. `git clone https://github.com/pytorch/pytorch.git && git submodule update --init --recursive`
2. apply the patches https://github.com/pytorch/pytorch/pull/132555/commits/0a53e6396902c075f547b8187e6457f82d6dc682
3. `cd .ci/docker`
4. `export PYTORCH_ROCM_ARCH=gfx1010`
5. `./build.sh pytorch-linux-ubuntu22.04-rocm6.2-py3.10 -t rocm/pytorch:build_from_dockerfile` (had to change a lot of package names in the install shell scripts, the ones prefixed with 6.2.0 worked)
6. ```docker/podman run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined  --user root --device=/dev/kfd --device=/dev/dri --group-add video --ipc=host --shm-size 8G -v ~/pytorch:/pytorch rocm/pytorch:build_from_dockerfile```
7. `export PYTORCH_ROCM_ARCH=gfx1010`
8. `.ci/pytorch/build.sh`

Some tests fail when running. I've installed ComfyUI in the container and run a basic example. All the basic samplers except SDE ones seem to work fine. You also don't need to force fp32 anymore (saves some vram)

---

### 评论 #58 — wrouesnel (2024-08-07T02:46:07Z)

Has anyone gotten pytorch to build against 6.2 yet? (I'm on Ubuntu 24.04).

I've gotten most of the way through the process but I'm stuck at this bizarre linker failure:

```
FAILED: bin/c10_hip_HIPAssertionsTest_from_2_processes 
: && /usr/bin/c++ -D_GLIBCXX_USE_CXX11_ABI=1 -fvisibility-inlines-hidden -DUSE_PTHREADPOOL -DNDEBUG -DUSE_KINETO -DLIBKINETO_NOCUPTI -DUSE_FBGEMM -DUSE_PYTORCH_QNNPACK -DUSE_XNNPACK -DSYMBOLICATE_MOBILE_DEBUG_HANDLE -O2 -fPIC -Wall -Wextra -Werror=return-type -Werror=non-virtual-dtor -Werror=range-loop-construct -Werror=bool-operation -Wnarrowing -Wno-missing-field-initializers -Wno-type-limits -Wno-array-bounds -Wno-unknown-pragmas -Wno-unused-parameter -Wno-strict-overflow -Wno-strict-aliasing -Wno-stringop-overflow -Wsuggest-override -Wno-psabi -Wno-error=pedantic -Wno-error=old-style-cast -Wno-missing-braces -fdiagnostics-color=always -faligned-new -Wno-unused-but-set-variable -Wno-maybe-uninitialized -fno-math-errno -fno-trapping-math -Werror=format -Wno-stringop-overflow -O3 -DNDEBUG -DNDEBUG -rdynamic -Wl,-rpath-link,/usr/lib/x86_64-linux-gnu     -Wl,--no-as-needed  -o bin/c10_hip_HIPAssertionsTest_from_2_processes  -Wl,-rpath,/home/will/src/pytorch/build/lib:/opt/rocm/lib:  lib/libc10_hip.so  lib/libc10.so  lib/libgtest_main.a  /opt/rocm/lib/libamdhip64.so  lib/libgtest.a && /usr/bin/cmake -E __run_co_compile --lwyu="ldd;-u;-r" --source=bin/c10_hip_HIPAssertionsTest_from_2_processes && :
/usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_import_shareable_handle@ROCR_1'
/usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_handle_create@ROCR_1'
/usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_unmap@ROCR_1'
/usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_set_access@ROCR_1'
/usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_map@ROCR_1'
/usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_get_access@ROCR_1'
/usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_address_reserve@ROCR_1'
/usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_address_free@ROCR_1'
/usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_handle_release@ROCR_1'
/usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_export_shareable_handle@ROCR_1'
```

The problem seems to be that those functions are defined in `/opt/rocm/lib/libhsa-runtime64.so` but I absolutely cannot figure out where or how these build command lines are being generated such that it's not included as a link target?

EDIT: By going through Pytorch and hacking the `libhsa-runtime64.so` path into all the tests and libs I was able to get it to build. But for my trouble I discovered that even if I just run the rocm-validation-suite on my XT 5700 I get a hard crash of the GPU (PyTorch also crashes). If anyone's got this hardware running, I'd be keen to know how - I'd really like to get to just having torch hanging around in my user python environment able to be used without all the drama.

---

### 评论 #59 — ethragur (2024-08-11T07:17:19Z)

I've tried the 6.2 wheels from https://repo.radeon.com/rocm/manylinux/
They don't work, getting the same[ error as with 6.1](https://github.com/ROCm/ROCm/issues/2527#issuecomment-2061177601)

Seem's like you need to build it yourself with gpu arch set to gfx1010. I might try building the manywheel (so everyone can use it) docker container with rocm6.2 and gfx1010. 


> Building the pytorch wheels via docker/podman worked: https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.2.0/install/3rd-party/pytorch-install.html#using-the-pytorch-upstream-docker-file
> 
>     1. `git clone https://github.com/pytorch/pytorch.git && git submodule update --init --recursive`
> 
>     2. apply the patches [pytorch/pytorch@0a53e63](https://github.com/pytorch/pytorch/commit/0a53e6396902c075f547b8187e6457f82d6dc682)
> 
>     3. `cd .ci/docker`
> 
>     4. `export PYTORCH_ROCM_ARCH=gfx1010`
> 
>     5. `./build.sh pytorch-linux-ubuntu22.04-rocm6.2-py3.10 -t rocm/pytorch:build_from_dockerfile` (had to change a lot of package names in the install shell scripts, the ones prefixed with 6.2.0 worked)
> 
>     6. `docker/podman run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined  --user root --device=/dev/kfd --device=/dev/dri --group-add video --ipc=host --shm-size 8G -v ~/pytorch:/pytorch rocm/pytorch:build_from_dockerfile`
> 
>     7. `export PYTORCH_ROCM_ARCH=gfx1010`
> 
>     8. `.ci/pytorch/build.sh`
> 
> 
> Some tests fail when running. I've installed ComfyUI in the container and run a basic example. All the basic samplers except SDE ones seem to work fine. You also don't need to force fp32 anymore (saves some vram)

I've done more testing with this wheel. While it works, it often runs out of memory and it takes a very long time to initialize. The ones build on 5.2 still work better in my case

---

### 评论 #60 — TheTrustedComputer (2024-08-11T13:00:10Z)

I've set up the ROCm 6.2 Ubuntu 24.04 apt repository in Docker to verify. My handcrafted C++ tests for HIPCC returned incorrect outputs on some libraries when compiling for my 8GB 5500 XT (gfx1012). Here are my test results:

**Working:**
rocBLAS/hipBLAS
rocFFT/hipFFT
MIOpen
MIGraphX

**Not Working:**
rocRAND/hipRAND
rocSPARSE/hipSPARSE
rocSOLVER/hipSOLVER

The workaround is to build and target the impacted libraries for your card's architecture. Unfortunately, that's the best users can do. Be prepared to wait many hours for the compilation process to complete and have patches ready in advance. This is a problem for the impatient and less technically oriented.

Reports say PyTorch + ROCm 6.2 + gfx1010 still doesn't work. I haven't tested PyTorch with the official ROCm build, so whether it works for me is difficult to tell. However, I was able to get PyTorch to build with my gfx1012 targeted ROCm installation, and the machine learning sample tests ran flawlessly.

I took the extra step of building ONNX Runtime with my specialized ROCm installation to get GPU acceleration. I found no issues creating a simple model and running a test inference.

---

### 评论 #61 — Zakhrov (2024-08-26T06:00:55Z)

I got pytorch 2.4.0 to compile successfully from source on rocm 6.2, and it works pretty well. A lot less hassle than previously. However there are reports that the official nightly wheels of pytorch still don't work. I'm downloading it now in a fresh venv to confirm. I have a sneaking suspicion that we'll just need to manually copy the Tensile files into the venv for it to work

---

### 评论 #62 — Zakhrov (2024-08-28T06:25:26Z)

Confirmed. The pytorch official wheels still don't work with GFX1010. Looks like we are stuck with building pytorch from source for now

---

### 评论 #63 — Giger22 (2024-08-28T07:50:13Z)

Yeah, it does not work.
https://github.com/pytorch/pytorch/issues/132570#issuecomment-2313071756

---

### 评论 #64 — riverzhou (2024-09-13T07:38:29Z)

> Has anyone gotten pytorch to build against 6.2 yet? (I'm on Ubuntu 24.04).
> 
> I've gotten most of the way through the process but I'm stuck at this bizarre linker failure:
> 
> ```
> FAILED: bin/c10_hip_HIPAssertionsTest_from_2_processes 
> : && /usr/bin/c++ -D_GLIBCXX_USE_CXX11_ABI=1 -fvisibility-inlines-hidden -DUSE_PTHREADPOOL -DNDEBUG -DUSE_KINETO -DLIBKINETO_NOCUPTI -DUSE_FBGEMM -DUSE_PYTORCH_QNNPACK -DUSE_XNNPACK -DSYMBOLICATE_MOBILE_DEBUG_HANDLE -O2 -fPIC -Wall -Wextra -Werror=return-type -Werror=non-virtual-dtor -Werror=range-loop-construct -Werror=bool-operation -Wnarrowing -Wno-missing-field-initializers -Wno-type-limits -Wno-array-bounds -Wno-unknown-pragmas -Wno-unused-parameter -Wno-strict-overflow -Wno-strict-aliasing -Wno-stringop-overflow -Wsuggest-override -Wno-psabi -Wno-error=pedantic -Wno-error=old-style-cast -Wno-missing-braces -fdiagnostics-color=always -faligned-new -Wno-unused-but-set-variable -Wno-maybe-uninitialized -fno-math-errno -fno-trapping-math -Werror=format -Wno-stringop-overflow -O3 -DNDEBUG -DNDEBUG -rdynamic -Wl,-rpath-link,/usr/lib/x86_64-linux-gnu     -Wl,--no-as-needed  -o bin/c10_hip_HIPAssertionsTest_from_2_processes  -Wl,-rpath,/home/will/src/pytorch/build/lib:/opt/rocm/lib:  lib/libc10_hip.so  lib/libc10.so  lib/libgtest_main.a  /opt/rocm/lib/libamdhip64.so  lib/libgtest.a && /usr/bin/cmake -E __run_co_compile --lwyu="ldd;-u;-r" --source=bin/c10_hip_HIPAssertionsTest_from_2_processes && :
> /usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_import_shareable_handle@ROCR_1'
> /usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_handle_create@ROCR_1'
> /usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_unmap@ROCR_1'
> /usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_set_access@ROCR_1'
> /usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_map@ROCR_1'
> /usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_get_access@ROCR_1'
> /usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_address_reserve@ROCR_1'
> /usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_address_free@ROCR_1'
> /usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_handle_release@ROCR_1'
> /usr/bin/x86_64-linux-gnu-ld.bfd.real: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_export_shareable_handle@ROCR_1'
> ```
> 
> The problem seems to be that those functions are defined in `/opt/rocm/lib/libhsa-runtime64.so` but I absolutely cannot figure out where or how these build command lines are being generated such that it's not included as a link target?
> 
> EDIT: By going through Pytorch and hacking the `libhsa-runtime64.so` path into all the tests and libs I was able to get it to build. But for my trouble I discovered that even if I just run the rocm-validation-suite on my XT 5700 I get a hard crash of the GPU (PyTorch also crashes). If anyone's got this hardware running, I'd be keen to know how - I'd really like to get to just having torch hanging around in my user python environment able to be used without all the drama.

Same problem:
```bash
/usr/bin/ld: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_import_shareable_handle@ROCR_1'
/usr/bin/ld: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_handle_create@ROCR_1'
/usr/bin/ld: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_unmap@ROCR_1'
/usr/bin/ld: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_set_access@ROCR_1'
/usr/bin/ld: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_map@ROCR_1'
/usr/bin/ld: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_get_access@ROCR_1'
/usr/bin/ld: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_address_reserve@ROCR_1'
/usr/bin/ld: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_address_free@ROCR_1'
/usr/bin/ld: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_handle_release@ROCR_1'
/usr/bin/ld: /opt/rocm/lib/libamdhip64.so: undefined reference to `hsa_amd_vmem_export_shareable_handle@ROCR_1'
```

I checked libamdhip64.so with objdump:
```bash
root@drfxi:~# objdump -T /opt/rocm/lib/libamdhip64.so |grep hsa_amd_vmem
0000000000000000      DF *UND*  0000000000000000 (ROCR_1)     hsa_amd_vmem_export_shareable_handle
0000000000000000      DF *UND*  0000000000000000 (ROCR_1)     hsa_amd_vmem_import_shareable_handle
0000000000000000      DF *UND*  0000000000000000 (ROCR_1)     hsa_amd_vmem_handle_release
0000000000000000      DF *UND*  0000000000000000 (ROCR_1)     hsa_amd_vmem_unmap
0000000000000000      DF *UND*  0000000000000000 (ROCR_1)     hsa_amd_vmem_get_access
0000000000000000      DF *UND*  0000000000000000 (ROCR_1)     hsa_amd_vmem_handle_create
0000000000000000      DF *UND*  0000000000000000 (ROCR_1)     hsa_amd_vmem_address_free
0000000000000000      DF *UND*  0000000000000000 (ROCR_1)     hsa_amd_vmem_address_reserve
0000000000000000      DF *UND*  0000000000000000 (ROCR_1)     hsa_amd_vmem_map
0000000000000000      DF *UND*  0000000000000000 (ROCR_1)     hsa_amd_vmem_set_access
```

---

### 评论 #65 — Zakhrov (2024-11-11T05:54:17Z)

 I was able to get the latest pytorch main code to build successfully. Also, no that aotriton is pre-built, the compilation time  is much faster.

---

### 评论 #66 — jamesxu2 (2024-11-14T18:50:55Z)

Thanks to all of you who have contributed to the discussion here. As [has been stated previously](https://github.com/ROCm/ROCm/issues/1735#issuecomment-2032752765), RDNA1 is not, and has never been officially supported by ROCm.

We appreciate your effort in finding workarounds to create a semblance of support for older cards outside our support matrix - I admire your resolve and the contributions you've made to the ROCm community. However, as has been stated previously in this thread, this issue is beyond our capability to definitively close and support - the nature of unsupported hardware is that it will continue to slip behind the breakthroughs in the ML space - and we must draw the line somewhere.

I will be converting this issue in particular to a discussion, as it has evolved from a specific issue to be solved into a discussion on the state of ROCm on gfx101X. 

You are welcome to file new specific issues when you encounter broken components, and we will try to address those issues to some extent, even if they fall outside our support matrix. Unfortunately, some of those issues will not be resolvable, whether due to hardware differences, lower-level driver support, or the magnitude of changes that would be required to "enable" new software to run on unsupported hardware (we do have to draw the line somewhere!), but we'll do our best to resolve what we can, and collaborate with the community to find fixes.



---
