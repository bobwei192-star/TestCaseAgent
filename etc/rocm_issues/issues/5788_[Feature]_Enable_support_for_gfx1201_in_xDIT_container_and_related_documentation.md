# [Feature]: Enable support for gfx1201 in xDIT container and related documentation

> **Issue #5788**
> **状态**: open
> **创建时间**: 2025-12-17T22:53:35Z
> **更新时间**: 2026-01-30T09:54:36Z
> **作者**: MrDrMcCoy
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5788

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Suggestion Description

There are exciting developments in the world of using multiple-GPUs for diffusion inference with xDIT. Unfortunately, the upstream documentation for xDIT does not produce a working environment for ROCm devices, and the AMD-supplied container refuses to run on gfx1201 for the Radeon Pro AI 9700 XT, which I bought three of. What I am hoping can be provided is the following:

1. Update the xDIT-ROCm container and associated docs to support gfx1201, and preferably also RDNA 3.5, which I also have and am looking forward to using. Ideally, ROCm-related frameworks should run on any ROCm-supported hardware, with a warning rather than a refusal if a specific architecture is not known to work.
2. Expand the xDIT ROCm docs to include non-Docker installations on Linux.

### Operating System

_No response_

### GPU

Radeon Pro AI 9700 XT (gfx1201)

### ROCm Component

_No response_

---

## 评论 (8 条)

### 评论 #1 — jcaraban (2026-01-14T20:57:19Z)

Hi @MrDrMcCoy, sorry for the late answer, only got to know of this issue yesterday. By "AMD-supplied container" I presume you are referring to https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/inference/xdit-diffusion-inference.html, aka `rocm/pytorch-xdit`?

Unfortunately the xDiT docker has an enterprise focus and RDNA support is not a short-term priority. _(Note with this statement I'm referring to the xDiT docker only, not ROCm in general)_. However we are aware of the growing diffusion community and want to include RDNA as soon as possible, even if performance is suboptimal at first. With that goal, it would help to understand more precisely your workflow, and how you attempt to use xDiT 🙂 

You mention multiple-GPU and three gfx1201 devices. Is your goal to run distributed inference across multiple GPUs on a single machine? If otoh you run single-gpu (i.e. data parallel), I'd think support is already available on ROCm 7.1.1, and possibly earlier depending on [windows](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/windows/windows_compatibility.html) or [Linux](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/native_linux/native_linux_compatibility.html) or [WSL](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/wsl/wsl_compatibility.html).

Alternatively [TheRock](https://github.com/ROCm/TheRock/tree/main) already provides ROCm releases for gfx1201 (see [link](https://github.com/ROCm/TheRock/blob/main/ROADMAP.md?plain=1#L37)) but let's hear first what your setup is 🙂 



---

### 评论 #2 — MrDrMcCoy (2026-01-15T06:30:20Z)

Hi @jcaraban, thanks for the reply!

Yes, I was referring to the `rocm/pytorch-xdit` container. The incompatibility I was referring to was that `chip_info.py` checks for specific cards and refuses to run if one's GPU is not on the list. If I alter that script to return `MI350`, I'm able to get further, but  the example scripts for Flux and Z-Image error out seemingly no matter what settings I give them. 

<details><summary>Commands</summary>

This is how I tart the container, trying to use two GPUs since I have read that odd numbers are hard.

```shell

run=(
  podman run -it --rm
  --env GPU_DEVICE_ORDINAL=0,1
  --env HIP_VISIBLE_DEVICES=0,1
  --env CUDA_VISIBLE_DEVICES=0,1
  --env LLAMA_HIPLAS=0,1
  --env GGML_VULKAN_DEVICE=0,1
  --env GGML_VK_VISIBLE_DEVICES=0,1
  --env ROCR_VISIBLE_DEVICES=GPU-6cd948adfa8a0662,GPU-baa51ac4e73599f5
  --env AITER_ROCM_ARCH=gfx1201
  --env GFX_ARCH=gfx1201
  --env HCC_AMDGPU_TARGET=gfx1201
  --env PYTORCH_ROCM_ARCH=gfx1201
  --env HSA_NO_SCRATCH_RECLAIM=1
  --env HSA_OVERRIDE_GFX_VERSION=12.0.1
  --env OMP_NUM_THREADS=$(($(nproc)/2))
  --env PYTORCH_ALLOC_CONF=expandable_segments:True
  --env HF_HOME=/data/ai/hf
  --env HF_TOKEN=<redacted>
  --cap-add=SYS_PTRACE
  -v /data/ai:/data/ai
  -v /data/ai/scripts/chip_info.py:/app/external/aiter/aiter/jit/utils/chip_info.py
  --security-opt seccomp=unconfined
  --user root
  --device=/dev/kfd
  --device=/dev/dri
  --group-add video
  --ipc=host
  --network host
  --privileged
  --replace
  --{host,}name=xdit
  rocm/pytorch-xdit:v25.13
)
${run[@]}

```

Inside the container:

```shell
cd /app/Z-Image
run=(
torchrun --nproc_per_node=2 run.py
   --model Tongyi-MAI/Z-Image-Turbo
   --prompt "a cat"
   --height 512 --width 320
   --num_frames 1
   --num_inference_steps 4
   --warmup_steps 1
   --ulysses_degree 2
   --dit_parallel_size 2
   --enable_tiling --enable_slicing
   --use_torch_compile
   --benchmark_output_directory /data/ai/out
)
${run[@]}
```

That yields the following error:

```text
E0115 05:44:28.210000 6139 torch/distributed/elastic/multiprocessing/api.py:882] failed (exitcode: -11) local_rank: 0 (pid: 6174) of binary: /venv/bin/python
Traceback (most recent call last):
  File "/venv/bin/torchrun", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/venv/lib/python3.12/site-packages/torch/distributed/elastic/multiprocessing/errors/__init__.py", line 357, in wrapper
    return f(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^
  File "/venv/lib/python3.12/site-packages/torch/distributed/run.py", line 936, in main
    run(args)
  File "/venv/lib/python3.12/site-packages/torch/distributed/run.py", line 927, in run
    elastic_launch(
  File "/venv/lib/python3.12/site-packages/torch/distributed/launcher/api.py", line 156, in __call__
    return launch_agent(self._config, self._entrypoint, list(args))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/venv/lib/python3.12/site-packages/torch/distributed/launcher/api.py", line 293, in launch_agent
    raise ChildFailedError(
torch.distributed.elastic.multiprocessing.errors.ChildFailedError:
======================================================
run.py FAILED
------------------------------------------------------
Failures:
[1]:
  time      : 2026-01-15_05:44:28
  host      : xdit
  rank      : 1 (local_rank: 1)
  exitcode  : -11 (pid: 6175)
  error_file: <N/A>
  traceback : Signal 11 (SIGSEGV) received by PID 6175
------------------------------------------------------
Root Cause (first observed failure):
[0]:
  time      : 2026-01-15_05:44:28
  host      : xdit
  rank      : 0 (local_rank: 0)
  exitcode  : -11 (pid: 6174)
  error_file: <N/A>
  traceback : Signal 11 (SIGSEGV) received by PID 6174
======================================================
```

Same story for Flux1-dev. HunyuanVideo, which I have no interest in, runs out of memory.
</details>

I was not able to locate adequate documentation for setting up xDIT for ROCm outside of Docker. 

As for my goals, yes, I am trying to distribute inference across the three GPUs within a single machine. Some models like Flux2 are quite large and more or less need to run across multiple of these cards if they are expected to run without extreme quantization. My workflow mostly consists of writing scripts to bulk-generate various prompt permutations until images emerge that match what I'm looking for. Given that ~5% of generated images match what I'm looking for, speed in image generation is paramount. 

I have had some success with stable-diffusion.cpp, but it has no ability to use multiple GPUs and it makes you choose between serving an API with caching and being able to use various LORAs since its server mode doesn't let you dynamically swap LORAs yet.

I can write some Python, but not to the level required to truly contribute to these projects, as I lack the CompSci/math background to truly understand low-level AI. I could open a PR for `chip_info.py` to replace those refusals to run with a warning, but I'm not sure how welcome that would be, or if there is a better fallback than `MI350` for RDNA.

---

### 评论 #3 — jcaraban (2026-01-15T14:46:12Z)

>The incompatibility I was referring to was that chip_info.py

right, AITER added gfx1201 in mid december but that [commit](https://github.com/ROCm/aiter/commit/f4bb76d29eb7762329658c50f82898d1fe6f29d4) didn't make it into `pytorch_xdit:v26.13`
anyway the AMD xDiT image doesn't contain sources for gfx1201, so it wouldn't work at the end
this is maybe the reason why you get `exitcode: -11` later on 🤔 

>I was not able to locate adequate documentation for setting up xDIT for ROCm outside of Docker.

I apologize for that. We don't include baremetal instructions (yet) because it entails building much of the underlying ROCm libs from source. The background here is that ROCm is undergoing a revamp and soon we will ship releases via TheRock. The xDiT docker already uses TheRock, but officially the switch happens with ROCm 8 in a couple of months. By that time installing latest ROCm should be more trivial, at pip install level.

For now what we can do (thanks @lauri9 !) is to provide a Dockerfile which you can try to get a gfx1202 environment. Sadly we only have a 16GB gfx1201 right now and couldn't load the models we tried. Did your GPUs have 32GB? If so hopefully you can get further, otherwise let us know.

```docker
FROM ubuntu:24.04
ARG GPU_ARCH="gfx120X-all"

RUN apt-get update && apt-get install -y --no-install-recommends \
    automake \
    bison \
    cmake \
    flex \
    g++ \
    gfortran \
    git \
    libegl1-mesa-dev \
    libtool \
    ninja-build \
    patchelf \
    pkg-config \
    python3-dev \
    python3-venv \
    texinfo \
    xxd \
    && rm -rf /var/lib/apt/lists/*

# setup virtual environment
WORKDIR /app
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# install ROCm 
RUN pip install \
    --no-cache-dir \
    --index-url https://rocm.nightlies.amd.com/v2/${GPU_ARCH}/ "rocm[libraries,devel]"
RUN rocm-sdk init

# install torch
RUN pip install \
    --no-cache-dir \
    --index-url https://rocm.nightlies.amd.com/v2/${GPU_ARCH}/ torch torchaudio torchvision

# install xDiT
RUN git clone https://github.com/xdit-project/xDiT.git && \
    cd xDiT && \
    pip install -e .
```
Notes:
- This does not pin any specific versions, so latest nightlies from TheRock / latest commit from xDiT will be installed.
- ROCm + torch installation is done using the docs here: https://github.com/ROCm/TheRock/blob/main/RELEASES.md
- Inside a container, one can run rocm-sdk test to verify the installation works.
- Tested Z-Image-Turbo briefly, but it looks like it runs out of memory (exceed 16GB) - likely memory saving changes to xDiT source code will be needed.

---

### 评论 #4 — MrDrMcCoy (2026-01-17T03:55:01Z)

Hi @jcaraban ,

Thanks so much for that! I was able to successfully run a Z-Image test on a single card since I have the 32GB versions of these cards. I modified that Dockerfile to make it more reliable and able to build much faster with `uv`:

<details><summary>Dockerfile</summary>

```dockerfile
FROM ubuntu:24.04
ARG GPU_ARCH="gfx120X-all"

RUN apt-get update && apt-get dist-upgrade --no-install-recommends -y && apt-get install -y --no-install-recommends \
  automake \
  bison \
  build-essential \
  clang \
  cmake \
  curl \
  flex \
  g++ \
  gfortran \
  git \
  gpg \
  libegl1-mesa-dev \
  libtool \
  ninja-build \
  patchelf \
  pkg-config \
  python3-pip \
  texinfo \
  xxd \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PATH="/root/.local/bin:/app/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV UV_COMPILE_BYTECODE=1
ENV UV_HTTP_TIMEOUT=500
ENV UV_INDEX_STRATEGY="unsafe-best-match"
ENV UV_LINK_MODE=copy
ENV VIRTUAL_ENV=/app/venv
RUN --mount=type=cache,target=/root/.cache/uv \
  pip3 install --no-cache --break-system-packages uv && \
  uv python install python3.12 && \
  uv venv --python python3.12 /app/venv && \
  uv pip install \
  --index-url https://rocm.nightlies.amd.com/v2/${GPU_ARCH}/ \
  "rocm[libraries,devel]" \
  torch \
  torchvision \
  torchaudio
RUN --mount=type=cache,target=/root/.cache/uv \
  git clone --recurse-submodules --depth=1 https://github.com/xdit-project/xDiT.git && \
  cd xDiT && \
  uv pip install -e .
```

</details>

Here are my findings from running it on a single card:

Model: Z-Image-Turbo
Size: 320x512
Steps: 4
Epoch time: 0.99 sec
Parameter memory: 20.70 GB
Memory: 21.77 GB

The only multi-card parameters I could get to work were:

- `--shard_t5_encoder --shard_dit --use_parallel_vae --tensor_parallel_degree 3` with `torchrun --nproc_per_node=3`
- `--shard_t5_encoder --shard_dit --use_parallel_vae --dit_parallel_size 2` with `torchrun --nproc_per_node=2`
- `--shard_t5_encoder --shard_dit --use_parallel_vae --data_parallel_degree 2` with `torchrun --nproc_per_node=2`

While they did run on all specified cards, they all resulted in the exact same execution time as the single card. Only `tensor_parallel_degree` seems able to accommodate an odd number of cards.

I'll include some errors as well for the various other parallel combinations.

`--ring_degree` gives `RuntimeError: Selected attention backend does not support ring parallelism.`

<details><summary>`--ulysses_parallel 2`</summary>

```text
WARNING 01-17 03:41:34 [runtime_state.py:120] Using SDPA as attention backend.
  0%|                                                                               | 0/9 [00:00<?, ?it/s]/app/venv/lib/python3.12/site-packages/torch/_dynamo/variables/functions.py:1692: UserWarning: Dynamo detected a call to a `functools.lru_cache`-wrapped function. Dynamo ignores the cache wrapper and directly traces the wrapped function. Silent incorrectness is only a *potential* risk, not something we have observed. Enable TORCH_LOGS="+dynamo" for a DEBUG stack trace.
  torch._dynamo.utils.warn_once(msg)
/app/venv/lib/python3.12/site-packages/torch/_dynamo/variables/functions.py:1692: UserWarning: Dynamo detected a call to a `functools.lru_cache`-wrapped function. Dynamo ignores the cache wrapper and directly traces the wrapped function. Silent incorrectness is only a *potential* risk, not something we have observed. Enable TORCH_LOGS="+dynamo" for a DEBUG stack trace.
  torch._dynamo.utils.warn_once(msg)
  0%|                                                                               | 0/9 [00:08<?, ?it/s]

[rank1]: Traceback (most recent call last):
[rank1]:   File "/app/xDiT/examples/zimage_example.py", line 96, in <module>
[rank1]:     main()
[rank1]:   File "/app/xDiT/examples/zimage_example.py", line 68, in main
[rank1]:     output = run_pipe(pipe, input_config)
[rank1]:              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/xDiT/examples/zimage_example.py", line 27, in run_pipe
[rank1]:     return pipe(
[rank1]:            ^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/utils/_contextlib.py", line 120, in decorate_context
[rank1]:     return func(*args, **kwargs)
[rank1]:            ^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/diffusers/pipelines/z_image/pipeline_z_image.py", line 527, in __call__
[rank1]:     model_out_list = self.transformer(
[rank1]:                      ^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/_dynamo/eval_frame.py", line 414, in __call__
[rank1]:     return super().__call__(*args, **kwargs)
[rank1]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
[rank1]:     return self._call_impl(*args, **kwargs)
[rank1]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
[rank1]:     return forward_call(*args, **kwargs)
[rank1]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/_dynamo/eval_frame.py", line 832, in compile_wrapper
[rank1]:     return fn(*args, **kwargs)
[rank1]:            ^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
[rank1]:     return self._call_impl(*args, **kwargs)
[rank1]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
[rank1]:     return forward_call(*args, **kwargs)
[rank1]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/xDiT/xfuser/model_executor/models/transformers/transformer_z_image.py", line 174, in forward
[rank1]:     x_freqs_cis = list(self.rope_embedder(torch.cat(x_pos_ids, dim=0)).split([len(_) for _ in x_pos_ids], dim=0))
[rank1]:   File "/app/xDiT/xfuser/model_executor/models/transformers/transformer_z_image.py", line 174, in torch_dynamo_resume_in_forward_at_174
[rank1]:     x_freqs_cis = list(self.rope_embedder(torch.cat(x_pos_ids, dim=0)).split([len(_) for _ in x_pos_ids], dim=0))
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/_dynamo/eval_frame.py", line 1044, in _fn
[rank1]:     return fn(*args, **kwargs)
[rank1]:            ^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/_functorch/aot_autograd.py", line 1130, in forward
[rank1]:     return compiled_fn(full_args)
[rank1]:            ^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/_functorch/_aot_autograd/runtime_wrappers.py", line 353, in runtime_wrapper
[rank1]:     all_outs = call_func_at_runtime_with_args(
[rank1]:                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/_functorch/_aot_autograd/utils.py", line 129, in call_func_at_runtime_with_args
[rank1]:     out = normalize_as_list(f(args))
[rank1]:                             ^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/_functorch/_aot_autograd/runtime_wrappers.py", line 526, in wrapper
[rank1]:     return compiled_fn(runtime_args)
[rank1]:            ^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/_inductor/output_code.py", line 613, in __call__
[rank1]:     return self.current_callable(inputs)
[rank1]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/_inductor/utils.py", line 3017, in run
[rank1]:     out = model(new_inputs)
[rank1]:           ^^^^^^^^^^^^^^^^^
[rank1]:   File "/tmp/torchinductor_root/vu/cvu3x4ixszhl5ga7lowtnmnilmlwosgpddz5ghoizc2p2xhn7teo.py", line 10328, in call
[rank1]:     buf2105 = torch.ops._c10d_functional.all_gather_into_tensor.default(buf2104, 2, '20')
[rank1]:               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/app/venv/lib/python3.12/site-packages/torch/_ops.py", line 841, in __call__
[rank1]:     return self._op(*args, **kwargs)
[rank1]:            ^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]: RuntimeError: NCCL Error 3: internal error - please report this issue to the NCCL developers
[rank0]: Traceback (most recent call last):
[rank0]:   File "/app/xDiT/examples/zimage_example.py", line 96, in <module>
[rank0]:     main()
[rank0]:   File "/app/xDiT/examples/zimage_example.py", line 68, in main
[rank0]:     output = run_pipe(pipe, input_config)
[rank0]:              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/xDiT/examples/zimage_example.py", line 27, in run_pipe
[rank0]:     return pipe(
[rank0]:            ^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/utils/_contextlib.py", line 120, in decorate_context
[rank0]:     return func(*args, **kwargs)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/diffusers/pipelines/z_image/pipeline_z_image.py", line 527, in __call__
[rank0]:     model_out_list = self.transformer(
[rank0]:                      ^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/_dynamo/eval_frame.py", line 414, in __call__
[rank0]:     return super().__call__(*args, **kwargs)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
[rank0]:     return self._call_impl(*args, **kwargs)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
[rank0]:     return forward_call(*args, **kwargs)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/_dynamo/eval_frame.py", line 832, in compile_wrapper
[rank0]:     return fn(*args, **kwargs)
[rank0]:            ^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
[rank0]:     return self._call_impl(*args, **kwargs)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
[rank0]:     return forward_call(*args, **kwargs)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/xDiT/xfuser/model_executor/models/transformers/transformer_z_image.py", line 174, in forward
[rank0]:     x_freqs_cis = list(self.rope_embedder(torch.cat(x_pos_ids, dim=0)).split([len(_) for _ in x_pos_ids], dim=0))
[rank0]:   File "/app/xDiT/xfuser/model_executor/models/transformers/transformer_z_image.py", line 174, in torch_dynamo_resume_in_forward_at_174
[rank0]:     x_freqs_cis = list(self.rope_embedder(torch.cat(x_pos_ids, dim=0)).split([len(_) for _ in x_pos_ids], dim=0))
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/_dynamo/eval_frame.py", line 1044, in _fn
[rank0]:     return fn(*args, **kwargs)
[rank0]:            ^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/_functorch/aot_autograd.py", line 1130, in forward
[rank0]:     return compiled_fn(full_args)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/_functorch/_aot_autograd/runtime_wrappers.py", line 353, in runtime_wrapper
[rank0]:     all_outs = call_func_at_runtime_with_args(
[rank0]:                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/_functorch/_aot_autograd/utils.py", line 129, in call_func_at_runtime_with_args
[rank0]:     out = normalize_as_list(f(args))
[rank0]:                             ^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/_functorch/_aot_autograd/runtime_wrappers.py", line 526, in wrapper
[rank0]:     return compiled_fn(runtime_args)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/_inductor/output_code.py", line 613, in __call__
[rank0]:     return self.current_callable(inputs)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/_inductor/utils.py", line 3017, in run
[rank0]:     out = model(new_inputs)
[rank0]:           ^^^^^^^^^^^^^^^^^
[rank0]:   File "/tmp/torchinductor_root/fu/cfulkr3dlpb6tfwie6ndfo3wb6tfa7cn5pb7ytd4a7ciasphp3e2.py", line 10328, in call
[rank0]:     buf2105 = torch.ops._c10d_functional.all_gather_into_tensor.default(buf2104, 2, '20')
[rank0]:               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/app/venv/lib/python3.12/site-packages/torch/_ops.py", line 841, in __call__
[rank0]:     return self._op(*args, **kwargs)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]: RuntimeError: NCCL Error 3: internal error - please report this issue to the NCCL developers
[rank0]:[W117 03:41:45.075470549 ProcessGroupNCCL.cpp:1524] Warning: WARNING: destroy_process_group() was not called before program exit, which can leak resources. For more info, please see https://pytorch.org/docs/stable/distributed.html#shutdown (function operator())
[rank1]:[W117 03:41:45.095140387 ProcessGroupNCCL.cpp:1524] Warning: WARNING: destroy_process_group() was not called before program exit, which can leak resources. For more info, please see https://pytorch.org/docs/stable/distributed.html#shutdown (function operator())
E0117 03:41:47.744000 10821 torch/distributed/elastic/multiprocessing/api.py:882] failed (exitcode: 1) local_rank: 0 (pid: 10857) of binary: /app/venv/bin/python3
Traceback (most recent call last):
  File "/app/venv/bin/torchrun", line 10, in <module>
    sys.exit(main())
             ^^^^^^
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/elastic/multiprocessing/errors/__init__.py", line 357, in wrapper
    return f(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/run.py", line 936, in main
    run(args)
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/run.py", line 927, in run
    elastic_launch(
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/launcher/api.py", line 156, in __call__
    return launch_agent(self._config, self._entrypoint, list(args))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/launcher/api.py", line 293, in launch_agent
    raise ChildFailedError(
torch.distributed.elastic.multiprocessing.errors.ChildFailedError:
============================================================
zimage_example.py FAILED
------------------------------------------------------------
Failures:
[1]:
  time      : 2026-01-17_03:41:47
  host      : xdit
  rank      : 1 (local_rank: 1)
  exitcode  : 1 (pid: 10858)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
------------------------------------------------------------
Root Cause (first observed failure):
[0]:
  time      : 2026-01-17_03:41:47
  host      : xdit
  rank      : 0 (local_rank: 0)
  exitcode  : 1 (pid: 10857)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
============================================================
```

</details>

I noticed an early warning in the output complaining about Aiter being missing and falling back to a sub-optimal attention mechanism. After modifying the container to include Aiter and Iris, new errors appear:

<details><summary>With Aiter</summary>

```text
[aiter] start build [module_aiter_enum] under /app/venv/lib/python3.12/site-packages/aiter/jit/build/module_aiter_enum
[aiter] waiting for baton release at /app/venv/lib/python3.12/site-packages/aiter/jit/build/lock_module_aiter_enum
[aiter] waiting for baton release at /app/venv/lib/python3.12/site-packages/aiter/jit/build/lock_module_aiter_enum
[aiter] Current hipcc not support: -mllvm -amdgpu-coerce-illegal-types=1, skip it.
[aiter] failed jit build [module_aiter_enum]↓↓↓↓↓↓↓↓↓↓
-->[History]: Traceback (most recent call last):
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 820, in wrapper
    module = get_module(md_name)
             ^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 508, in get_module
    get_module_custom_op(md_name)
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 281, in wrapper_custom
    else getattr(torch.ops.aiter, f"{loadName}")(
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/torch/_ops.py", line 1255, in __call__
    return self._op(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 319, in outer_wrapper_dummy
    wrapper(*args, **kwargs)
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 197, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 500, in get_module_custom_op
    __mds[md_name] = importlib.import_module(f"{__package__}.{md_name}")
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/root/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
-->  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
-->  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
-->ModuleNotFounderror: No module named 'aiter.jit.module_aiter_enum'
-->
During handling of the above exception, another exception occurred:

-->Traceback (most recent call last):
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 823, in wrapper
    module = get_module(md)
             ^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 508, in get_module
    get_module_custom_op(md_name)
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 281, in wrapper_custom
    else getattr(torch.ops.aiter, f"{loadName}")(
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/torch/_ops.py", line 1255, in __call__
    return self._op(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 319, in outer_wrapper_dummy
    wrapper(*args, **kwargs)
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 197, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 500, in get_module_custom_op
    __mds[md_name] = importlib.import_module(f"{__package__}.{md_name}")
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/root/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
-->  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
-->  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
-->ModuleNotFounderror: No module named 'aiter.jit.module_aiter_enum'
-->
During handling of the above exception, another exception occurred:

-->Traceback (most recent call last):
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/cpp_extension.py", line 1477, in _run_ninja_build
    subprocess.run(
-->  File "/root/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 571, in run
    raise CalledProcessError(retcode, process.args,
-->subprocess.CalledProcesserror: Command '['ninja', '-v', '-j', '25']' returned non-zero exit status 1.
-->
The above exception was the direct cause of the following exception:

-->Traceback (most recent call last):
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 661, in MainFunc
    _jit_compile(
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/cpp_extension.py", line 1226, in _jit_compile
    _write_ninja_file_and_build_library(
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/cpp_extension.py", line 1352, in _write_ninja_file_and_build_library
    _run_ninja_build(
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/cpp_extension.py", line 1494, in _run_ninja_build
    raise RuntimeError(message) from e
-->Runtimeerror: Error building extension 'module_aiter_enum': [1/2] /app/venv/bin/hipcc  -DWITH_HIP -D_GLIBCXX_USE_CXX11_ABI=1 -I/app/venv/lib/python3.12/site-packages/aiter_meta/3rdparty/ck_helper -I/app/venv/lib/python3.12/site-packages/aiter_meta/3rdparty/composable_kernel/include -I/app/venv/lib/python3.12/site-packages/aiter_meta/3rdparty/composable_kernel/library/include -I/app/venv/lib/python3.12/site-packages/aiter_meta/csrc/include -I/app/venv/lib/python3.12/site-packages/aiter/jit/build/module_aiter_enum/blob -I/app/venv/lib/python3.12/site-packages/aiter_meta/csrc/include/torch -I/app/venv/lib/python3.12/site-packages/pybind11/include -isystem /app/venv/lib/python3.12/site-packages/torch/include/TH -isystem /app/venv/lib/python3.12/site-packages/torch/include/THC -isystem /app/venv/lib/python3.12/site-packages/torch/include -isystem /app/venv/lib/python3.12/site-packages/torch/include/torch/csrc/api/include -isystem /root/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/include/python3.12 -fPIC -std=c++20 -O3 -std=c++20 -fPIC -D__HIP_PLATFORM_AMD__=1 -DUSE_ROCM=1 -DHIPBLAS_V2 -DCUDA_HAS_FP16=1 -D__HIP_NO_HALF_OPERATORS__=1 -D__HIP_NO_HALF_CONVERSIONS__=1 -mcmodel=large -fno-unique-section-names -ffunction-sections -fdata-sections -fvisibility=hidden -fvisibility-inlines-hidden --offload-arch=native -DDLLVM_MAIN_REVISION=554785 -DLEGACY_HIPBLAS_DIRECT -DUSE_PROF_API=1 -D__HIP_PLATFORM_AMD__=1 -D__HIP_PLATFORM_HCC__=1 -U__HIP_NO_HALF_CONVERSIONS__ -U__HIP_NO_HALF_OPERATORS__ -Wno-macro-redefined -Wno-missing-template-arg-list-after-template-kw -Wno-switch-bool -Wno-undefined-func-template -Wno-unused-result -Wno-vla-cxx-extension -fgpu-flush-denormals-to-zero -fno-offload-uniform-block -mllvm --amdgpu-kernarg-preload-count=16 -mllvm --lsr-drop-solution=1 -mllvm -amdgpu-early-inline-all=true -mllvm -amdgpu-function-calls=false -mllvm -enable-post-misched=0 -fno-gpu-rdc -c /app/venv/lib/python3.12/site-packages/aiter_meta/csrc/pybind/aiter_enum_pybind.cu -o aiter_enum_pybind.cuda.o
[2/2] c++ @module_aiter_enum.so.rsp -shared -mcmodel=large -ffunction-sections -fdata-sections -Wl,--gc-sections -Wl,--cref -L/app/venv/lib -lamdhip64 -o module_aiter_enum.so
FAILED: [code=1] module_aiter_enum.so
c++ @module_aiter_enum.so.rsp -shared -mcmodel=large -ffunction-sections -fdata-sections -Wl,--gc-sections -Wl,--cref -L/app/venv/lib -lamdhip64 -o module_aiter_enum.so
/usr/bin/ld: cannot find -lamdhip64: No such file or directory
collect2: error: ld returned 1 exit status
ninja: build stopped: subcommand failed.

failed jit build [module_aiter_enum]↑↑↑↑↑↑↑↑↑↑
[aiter] finish build [module_aiter_enum], cost 12.4s
WARNING 01-17 03:48:39 [envs.py:205] Using AMD GPUs, but library "aiter" is not installed, defaulting to other attention mechanisms
[aiter] start build [module_aiter_enum] under /app/venv/lib/python3.12/site-packages/aiter/jit/build/module_aiter_enum
[aiter] failed jit build [module_aiter_enum]↓↓↓↓↓↓↓↓↓↓
-->[History]: Traceback (most recent call last):
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 820, in wrapper
    module = get_module(md_name)
             ^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 508, in get_module
    get_module_custom_op(md_name)
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 281, in wrapper_custom
    else getattr(torch.ops.aiter, f"{loadName}")(
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/torch/_ops.py", line 1255, in __call__
    return self._op(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 319, in outer_wrapper_dummy
    wrapper(*args, **kwargs)
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 197, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 500, in get_module_custom_op
    __mds[md_name] = importlib.import_module(f"{__package__}.{md_name}")
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/root/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
-->  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
-->  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
-->ModuleNotFounderror: No module named 'aiter.jit.module_aiter_enum'
-->
During handling of the above exception, another exception occurred:

-->Traceback (most recent call last):
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 823, in wrapper
    module = get_module(md)
             ^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 508, in get_module
    get_module_custom_op(md_name)
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 281, in wrapper_custom
    else getattr(torch.ops.aiter, f"{loadName}")(
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/torch/_ops.py", line 1255, in __call__
    return self._op(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 319, in outer_wrapper_dummy
    wrapper(*args, **kwargs)
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/utils/torch_guard.py", line 197, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 500, in get_module_custom_op
    __mds[md_name] = importlib.import_module(f"{__package__}.{md_name}")
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "/root/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
-->  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
-->  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
-->ModuleNotFounderror: No module named 'aiter.jit.module_aiter_enum'
-->
During handling of the above exception, another exception occurred:

-->Traceback (most recent call last):
-->  File "/app/venv/lib/python3.12/site-packages/aiter/jit/core.py", line 677, in MainFunc
    shutil.copy(f"{opbd_dir}/{target_name}", f"{get_user_jit_dir()}")
-->  File "/root/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/lib/python3.12/shutil.py", line 435, in copy
    copyfile(src, dst, follow_symlinks=follow_symlinks)
-->  File "/root/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/lib/python3.12/shutil.py", line 260, in copyfile
    with open(src, 'rb') as fsrc:
         ^^^^^^^^^^^^^^^
-->FileNotFounderror: [Errno 2] No such file or directory: '/app/venv/lib/python3.12/site-packages/aiter/jit/build/module_aiter_enum/build/module_aiter_enum.so'
failed jit build [module_aiter_enum]↑↑↑↑↑↑↑↑↑↑
[aiter] finish build [module_aiter_enum], cost 0.0s
[aiter] build [module_aiter_enum] under /app/venv/lib/python3.12/site-packages/aiter/jit/build/module_aiter_enum/build failed !!!!!!
WARNING 01-17 03:48:39 [envs.py:205] Using AMD GPUs, but library "aiter" is not installed, defaulting to other attention mechanisms
WARNING 01-17 03:48:39 [envs.py:205] Using AMD GPUs, but library "aiter" is not installed, defaulting to other attention mechanisms
[aiter] start build [module_aiter_enum] under /app/venv/lib/python3.12/site-packages/aiter/jit/build/module_aiter_enum
[aiter] waiting for baton release at /app/venv/lib/python3.12/site-packages/aiter/jit/build/lock_module_aiter_enum
W0117 03:48:39.914000 14 torch/distributed/elastic/multiprocessing/api.py:908] Sending process 50 closing signal SIGTERM
W0117 03:48:39.914000 14 torch/distributed/elastic/multiprocessing/api.py:908] Sending process 51 closing signal SIGTERM
E0117 03:48:40.028000 14 torch/distributed/elastic/multiprocessing/api.py:882] failed (exitcode: 1) local_rank: 2 (pid: 52) of binary: /app/venv/bin/python3
Traceback (most recent call last):
  File "/app/venv/bin/torchrun", line 10, in <module>
    sys.exit(main())
             ^^^^^^
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/elastic/multiprocessing/errors/__init__.py", line 357, in wrapper
    return f(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/run.py", line 936, in main
    run(args)
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/run.py", line 927, in run
    elastic_launch(
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/launcher/api.py", line 156, in __call__
    return launch_agent(self._config, self._entrypoint, list(args))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/launcher/api.py", line 293, in launch_agent
    raise ChildFailedError(
torch.distributed.elastic.multiprocessing.errors.ChildFailedError:
============================================================
zimage_example.py FAILED
------------------------------------------------------------
Failures:
  <NO_OTHER_FAILURES>
------------------------------------------------------------
Root Cause (first observed failure):
[0]:
  time      : 2026-01-17_03:48:39
  host      : xdit
  rank      : 2 (local_rank: 2)
  exitcode  : 1 (pid: 52)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
============================================================
```

</details>

The Aiter error seems like it could be from using an incompatible version of the library. If so, I don't know what version should be pinned.


---

### 评论 #5 — jcaraban (2026-01-19T08:28:03Z)

Hi @MrDrMcCoy, nice to hear you got Z-Image to work! I will try to get a couple of 32GB RDNA4 so we can start testing such setup, with the goal of supporting consumer GPUs in the future.

> The only multi-card parameters I could get to work were:

I have not played with weights sharding much since (for inference) these models fit in our enterprise GPUs even at max resolution... but we will adjust our priorities and try to bring FSDP to more models (we just did for [Wan2.x](https://github.com/xdit-project/xDiT/pull/615))

> While they did run on all specified cards, they all resulted in the exact same execution time as the single card.

That's odd 🤔 `Epoch time: 0.99 sec` here means the full inference took only 1 second? In my experience xDiT is not capable of reducing e2e below 1 sec, maybe because of scheduling overhead. Did you try increasing the resolution?

If your goal is to reduce the inference latency of a single batch, I think the best perf will come from getting Ulysses to work. In your logs I see a NCCL/RCCL error, I'll ask around to understand where that comes from


---

### 评论 #6 — lauri9 (2026-01-20T13:41:01Z)

Hi @MrDrMcCoy I had access to a system with four Radeon AI Pro R9700 and attempted to reproduce the issues you had on Z-Image Turbo.

I am using the `Dockerfile` that @jcaraban shared [above](https://github.com/ROCm/ROCm/issues/5788#issuecomment-3755225528), built locally to have the tag `diffusion:latest`. Here's how I am launching the container:
```bash
docker run \
    -it \
    --rm \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    --user root \
    --device=/dev/kfd \
    --device=/dev/dri \
    --group-add video \
    --ipc=host \
    --network host \
    --privileged \
    --name xdit-test \
    diffusion:latest \
    bash
```
I am omitting only volume mapping for `HF_HOME` and results directory. I could then successfully run Z-Image Turbo example from xDiT upstream in the container as follows:
```bash
torchrun --nproc-per-node=2 \
    /app/xDiT/examples/zimage_example.py \
   --model Tongyi-MAI/Z-Image-Turbo \
   --prompt "a cat" \
   --height 512 \
   --width 320 \
   --num_inference_steps 4 \
   --ulysses_degree 2 \
   --use_torch_compile \
   --enable_tiling \
   --enable_slicing
```


Could you try if you still see the same errors reproducing the steps above? If you still hit the RCCL error, could you collect and share the `.log` files recorded by setting the environmental variables
```
NCCL_DEBUG=INFO
NCCL_DEBUG_FILE=rccl.%h.%p.log
```
and then running the workload?


Ring attention is not available with the default SDPA backend, but the upstream xDiT examples accept an attention backend argument that can make it work. With `--attention_backend sdpa_flash` for instance I was able to also use `ring_degree > 1` successfully.

---

### 评论 #7 — MrDrMcCoy (2026-01-29T01:00:53Z)

Hi @lauri9 ,

Sorry for the delayed reply. Life... uhh... got in the way.

I tried rebuilding the Docker image exactly as you had it and ran the command you provided, but it failed:

<details><summary>Errors</summary>

```log
WARNING 01-29 00:54:07 [envs.py:206] Using AMD GPUs, but library "aiter" is not installed, defaulting to other attention mechanisms
WARNING 01-29 00:54:07 [envs.py:206] Using AMD GPUs, but library "aiter" is not installed, defaulting to other attention mechanisms
Traceback (most recent call last):
  File "/app/venv/lib/python3.12/site-packages/diffusers/utils/import_utils.py", line 1016, in _get_module
    return importlib.import_module("." + module_name, self.__name__)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/app/venv/lib/python3.12/site-packages/diffusers/pipelines/hunyuandit/pipeline_hunyuandit.py", line 20, in <module>
    from transformers import BertModel, BertTokenizer, CLIPImageProcessor, MT5Tokenizer, T5EncoderModel
ImportError: cannot import name 'MT5Tokenizer' from 'transformers' (/app/venv/lib/python3.12/site-packages/transformers/__init__.py)Traceback (most recent call last):
  File "/app/venv/lib/python3.12/site-packages/diffusers/utils/import_utils.py", line 1016, in _get_module
    return importlib.import_module("." + module_name, self.__name__)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/app/venv/lib/python3.12/site-packages/diffusers/pipelines/hunyuandit/pipeline_hunyuandit.py", line 20, in <module>
    from transformers import BertModel, BertTokenizer, CLIPImageProcessor, MT5Tokenizer, T5EncoderModel
ImportError: cannot import name 'MT5Tokenizer' from 'transformers' (/app/venv/lib/python3.12/site-packages/transformers/__init__.py)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/xDiT/examples/zimage_example.py", line 4, in <module>
    from xfuser.config.diffusers import has_valid_diffusers_version, get_minimum_diffusers_version
  File "/app/xDiT/xfuser/__init__.py", line 1, in <module>
    from xfuser.model_executor.pipelines import (
  File "/app/xDiT/xfuser/model_executor/pipelines/__init__.py", line 9, in <module>
    from .pipeline_hunyuandit import xFuserHunyuanDiTPipeline
  File "/app/xDiT/xfuser/model_executor/pipelines/pipeline_hunyuandit.py", line 6, in <module>
    from diffusers import HunyuanDiTPipeline
  File "<frozen importlib._bootstrap>", line 1412, in _handle_fromlist
  File "/app/venv/lib/python3.12/site-packages/diffusers/utils/import_utils.py", line 1007, in __getattr__
    value = getattr(module, name)
            ^^^^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/diffusers/utils/import_utils.py", line 1007, in __getattr__
    value = getattr(module, name)
            ^^^^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/diffusers/utils/import_utils.py", line 1006, in __getattr__
    module = self._get_module(self._class_to_module[name])
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/diffusers/utils/import_utils.py", line 1018, in _get_module
    raise RuntimeError(
RuntimeError: Failed to import diffusers.pipelines.hunyuandit.pipeline_hunyuandit because of the following error (look up to see its traceback):
cannot import name 'MT5Tokenizer' from 'transformers' (/app/venv/lib/python3.12/site-packages/transformers/__init__.py)


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/xDiT/examples/zimage_example.py", line 4, in <module>
    from xfuser.config.diffusers import has_valid_diffusers_version, get_minimum_diffusers_version
  File "/app/xDiT/xfuser/__init__.py", line 1, in <module>
    from xfuser.model_executor.pipelines import (
  File "/app/xDiT/xfuser/model_executor/pipelines/__init__.py", line 9, in <module>
    from .pipeline_hunyuandit import xFuserHunyuanDiTPipeline
  File "/app/xDiT/xfuser/model_executor/pipelines/pipeline_hunyuandit.py", line 6, in <module>
    from diffusers import HunyuanDiTPipeline
  File "<frozen importlib._bootstrap>", line 1412, in _handle_fromlist
  File "/app/venv/lib/python3.12/site-packages/diffusers/utils/import_utils.py", line 1007, in __getattr__
    value = getattr(module, name)
            ^^^^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/diffusers/utils/import_utils.py", line 1007, in __getattr__
    value = getattr(module, name)
            ^^^^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/diffusers/utils/import_utils.py", line 1006, in __getattr__
    module = self._get_module(self._class_to_module[name])
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/diffusers/utils/import_utils.py", line 1018, in _get_module
    raise RuntimeError(
RuntimeError: Failed to import diffusers.pipelines.hunyuandit.pipeline_hunyuandit because of the following error (look up to see its traceback):
cannot import name 'MT5Tokenizer' from 'transformers' (/app/venv/lib/python3.12/site-packages/transformers/__init__.py)
E0129 00:54:12.960000 9 torch/distributed/elastic/multiprocessing/api.py:882] failed (exitcode: 1) local_rank: 0 (pid: 45) of binary: /app/venv/bin/python3
Traceback (most recent call last):
  File "/app/venv/bin/torchrun", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/elastic/multiprocessing/errors/__init__.py", line 357, in wrapper
    return f(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/run.py", line 936, in main
    run(args)
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/run.py", line 927, in run
    elastic_launch(
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/launcher/api.py", line 156, in __call__
    return launch_agent(self._config, self._entrypoint, list(args))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/venv/lib/python3.12/site-packages/torch/distributed/launcher/api.py", line 293, in launch_agent
    raise ChildFailedError(
torch.distributed.elastic.multiprocessing.errors.ChildFailedError:
============================================================
/app/xDiT/examples/zimage_example.py FAILED
------------------------------------------------------------
Failures:
[1]:
  time      : 2026-01-29_00:54:12
  host      : xdit
  rank      : 1 (local_rank: 1)
  exitcode  : 1 (pid: 46)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
------------------------------------------------------------
Root Cause (first observed failure):
[0]:
  time      : 2026-01-29_00:54:12
  host      : xdit
  rank      : 0 (local_rank: 0)
  exitcode  : 1 (pid: 45)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
============================================================
```

</details>

Although it was run with the logging variables set, I don't see any log files in `/app`. Perhaps it failed before that had a chance to activate.

---

### 评论 #8 — lauri9 (2026-01-30T09:54:36Z)

Hi @MrDrMcCoy , I ran into the same error yesterday as well. The error happens due to an incompatible version of the `transformers` package getting installed -- they just recently released [version 5](https://github.com/huggingface/transformers/releases/tag/v5.0.0) that appears to be [incompatible](https://github.com/huggingface/diffusers/commit/52766e6a6939ac6e74375bde5e19c5e0b90d24c1). As the Dockerfile does not mandate a version below 5, we get this incompatible version.

Uninstalling that and downgrading to a version below 5 should allow you to proceed, for example adding at the end of the Dockerfile or running before starting the inference script:
```bash
pip uninstall -y transformers && pip install "transformers==4.57.6"
```

Sorry about the back and forth, but things are moving fast in the community which requires us to play catch-up as breaking changes come in!

---
