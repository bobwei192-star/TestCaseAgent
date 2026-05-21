# [Documentation]: WSL installation and conda

> **Issue #3914**
> **状态**: closed
> **创建时间**: 2024-10-17T14:20:34Z
> **更新时间**: 2024-12-19T06:05:33Z
> **关闭时间**: 2024-12-06T15:39:15Z
> **作者**: jschoch
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/3914

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

after following the installation for WSL on ubuntu when you check for a working torch install you get t his error when you have an active conda environment.  

`
ImportError: /home/schoch/miniconda3/envs/Pose2Sim/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.30' not found (required by /home/schoch/miniconda3/envs/Pose2Sim/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so)
`

This can be fixed by running: `conda install -c conda-forge gcc=12.1.0`

Should be useful to wsl users and considered to be added to the rocm wsl install documentation.

It may also trip users up that python 3.10 is required, it doesn't actually say that in the install docs.

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (6 条)

### 评论 #1 — jamesxu2 (2024-10-24T16:00:10Z)

Hi @jschoch,

Thanks for reporting this issue. I'm able to reproduce it using a conda environment inside a default WSL using Ubuntu 22.04 LTS. 

> It may also trip users up that python 3.10 is required, it doesn't actually say that in the install docs.

That is a good point. I ran into this too. I'll forward it to the docs team.

> ImportError: /home/schoch/miniconda3/envs/Pose2Sim/bin/../lib/libstdc++.so.6: versionGLIBCXX_3.4.30' not found (required by /home/schoch/miniconda3/envs/Pose2Sim/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so)

I think this could be added to the Troubleshooting section, but it is sort of an issue with Conda packaging an older version of libstdcxx and overriding the WSL system default (which does work). 


---

### 评论 #2 — jschoch (2024-11-16T20:28:12Z)

@jamesxu2   can you reopen this.  it seems that my fix for GLIBCXX_3.4.30  breaks things and when you try to compile vllm it creates pthread linker issues.  the better fix seems to be to run `ln -sf /usr/lib/x86_64-linux-gnu/libstdc++.so.6 ${CONDA_PREFIX}/lib/libstdc++.so.6`  

it seems crazy to me that this is a problem.

Also, i can create a new issue if needed, but I spent 2 days trying to get vllm to compile from source using wsl and I can't make it work.   I have built the rocm fork of vllm but i  get a `RuntimeError: Failed to infer device type`   There don't seem to be any clear docs on doing this (particularly for gfx1100).   I hit all sorts of snags with crazy stuff like sphinx.doc and not finding hipbsolidxgemm, something that literally has 1 link on google search (turns out you have to install gradlib from the one built in vllm.  

---

### 评论 #3 — jamesxu2 (2024-11-18T15:25:36Z)

Hi @jschoch, could you provide some more information on what exactly you're doing to run into the pthread linker issues? I'd can try reproducing that error. This seems like an artifact of conda's packaged libstdc++ version and by your symlink you are overwriting the libstdc++ library that conda comes with, with the base WSL one. 

I will note that ROCm on WSL is in a [beta state](https://community.amd.com/t5/ai/new-amd-rocm-6-1-software-for-radeon-release-offers-more-choices/ba-p/688840) as of ROCm 6.1.3, and so while I feel your frustration getting this to work, it's not unexpected that you'd run into issues. 

Also, please create a new issue for the problems you're running into while attempting to use vLLM on WSL. I think the scope of this may be more of a "feature request" than something that can be enabled with a simple fix, but I (or the rest of my team) would be happy to assess that.

---

### 评论 #4 — jschoch (2024-11-19T21:17:56Z)

I pulled the rocm/vllm repo and just tried to build VLLM, the linker though lpthreads was in /lib64 and the a file was in /usr/lib64 so something with the linker path was broken by conda by installing gcc.  I had to create another conda env and do that ln -sf hack to get it to build.  I don't have the error handy, building VLLM is like 2MB of logging output and the old conda env is gone.

---

### 评论 #5 — jamesxu2 (2024-12-06T15:39:15Z)

Building VLLM for ROCm is a bit complicated, and we do provide a Docker image for it and instructions on use in **native linux** (ref: [VLLM Usecase](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/advanced/vllm/build-docker-image.html)). I have seen a number of issues as well attempting to build rocm/vllm locally, and I don't think we provide instructions on using VLLM outside the Docker container. 

This error:
> RuntimeError: Failed to infer device type

Is an artifact of VLLM using amd-smi to search for devices before running, but won't work in WSL as @harkgill-amd [explained](https://github.com/ROCm/ROCm/issues/4055#issuecomment-2501049734) in the linked issue.

One way to bypass that RuntimeError is to pass `--device cuda` in your invocation of VLLM, but you will likely run into other issues downstream of that. 

---

In summary: The current status is that VLLM has been verified on native Linux and we provide a docker image to support that usecase. However, there are additional steps needed and updates required to make it work on WSL and it won't work out of the box on WSL. 

We plan to support VLLM on WSL in a future release of ROCm. WSL-specific instructions and a compatible docker image are in development, but VLLM on WSL is not currently supported. 





---

### 评论 #6 — githust66 (2024-12-10T06:35:45Z)

> Building VLLM for ROCm is a bit complicated, and we do provide a Docker image for it and instructions on use in **native linux** (ref: [VLLM Usecase](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/advanced/vllm/build-docker-image.html)). I have seen a number of issues as well attempting to build rocm/vllm locally, and I don't think we provide instructions on using VLLM outside the Docker container.
> 
> This error:
> 
> > RuntimeError: Failed to infer device type
> 
> Is an artifact of VLLM using amd-smi to search for devices before running, but won't work in WSL as @harkgill-amd [explained](https://github.com/ROCm/ROCm/issues/4055#issuecomment-2501049734) in the linked issue.
> 
> One way to bypass that RuntimeError is to pass `--device cuda` in your invocation of VLLM, but you will likely run into other issues downstream of that.
> 
> In summary: The current status is that VLLM has been verified on native Linux and we provide a docker image to support that usecase. However, there are additional steps needed and updates required to make it work on WSL and it won't work out of the box on WSL.
> 
> We plan to support VLLM on WSL in a future release of ROCm. WSL-specific instructions and a compatible docker image are in development, but VLLM on WSL is not currently supported.

I used https://github.com/vllm-project/vllm to build vllm from source code, and referred to the get_amdgpu_memory_capacity method in https://github.com/sgl-project/sglang/blob/main/python/sglang/srt/utils.py file to modify the amdsmi-related code in https://github.com/vllm-project/vllm/blob/main/vllm/platforms/__init__.py file, using rocminfo instead of amdsmi. This allows vllm to be used on wsl.
![image](https://github.com/user-attachments/assets/f6f277c1-ed5c-46c0-9097-2851f4881ddb)


---
