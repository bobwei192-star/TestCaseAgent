# [Feature]: Pytorch wheels built against Python 3.12 for Comfy_UI support

> **Issue #4473**
> **状态**: closed
> **创建时间**: 2025-03-10T15:52:15Z
> **更新时间**: 2025-05-27T15:46:20Z
> **关闭时间**: 2025-03-17T14:22:47Z
> **作者**: fluidnumericsJoe
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4473

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

TLDR; Add a pytorch wheel with ROCm support built against Python 3.12 in addition to Python 3.10.


In triaging issues for users, I've found that there's strong interest in using [Comfy_UI[(https://github.com/comfyanonymous/ComfyUI) for running diffusion models on AMD GPUs, particularly in WSL2 environments and with Radeon GPUs. (e.g. [r/ROCm subbreddit discussion](https://www.reddit.com/r/ROCm/comments/1j3eyp5/comment/mgnia05/), [discuss.pytorch.org](https://discuss.pytorch.org/t/comfy-ui-attempting-to-use-hipblaslt-on-a-unsupported-architecture/215776/19) )

Users have pointed out that Comfy_UI requires Python 3.12, but the Pytorch wheels packages for AMD GPUs are built against  Python 3.10 (See the notes in [ROCm docs](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html#install-methods) ), which may be causing problems out of the box.

The workaround of course, is to [build pytorch from source with the preferred Python version](https://github.com/pytorch/pytorch/?tab=readme-ov-file#amd-rocm-support). However, this is a time-intensive process that does not contribute to a good user experience (for those that don't like installing packages from source).




### Operating System

WSL2

### GPU

_No response_

### ROCm Component

pytorch

---

## 评论 (9 条)

### 评论 #1 — james-banks (2025-03-10T17:07:37Z)

The Ubuntu 24.04 instructions in the link provided give the downloads to Python 3.12 versions of the wheels you are discussing!

```bash
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/torch-2.4.0%2Brocm6.3.4.git7cecbf6d-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/torchvision-0.19.0%2Brocm6.3.4.gitfab84886-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/pytorch_triton_rocm-3.0.0%2Brocm6.3.4.git75cc27c2-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/torchaudio-2.4.0%2Brocm6.3.4.git69d40773-cp312-cp312-linux_x86_64.whl
pip3 uninstall torch torchvision pytorch-triton-rocm
pip3 install torch-2.4.0+rocm6.3.4.git7cecbf6d-cp312-cp312-linux_x86_64.whl torchvision-0.19.0+rocm6.3.4.gitfab84886-cp312-cp312-linux_x86_64.whl torchaudio-2.4.0+rocm6.3.4.git69d40773-cp312-cp312-linux_x86_64.whl pytorch_triton_rocm-3.0.0+rocm6.3.4.git75cc27c2-cp312-cp312-linux_x86_64.whl
```

Looks like the notice about Python 3.10 needs removing, though. 

---

### 评论 #2 — fluidnumericsJoe (2025-03-10T17:21:48Z)

Got it. I'd say if that notice gets updated, I'll be happy to close this issue

---

### 评论 #3 — harkgill-amd (2025-03-10T18:52:44Z)

Will work on getting that notice updated/removed. Thanks for pointing this out!

---

### 评论 #4 — fluidnumericsJoe (2025-03-13T14:15:04Z)

Hey @harkgill-amd - If this hasn't been assigned to a dev internally or is not already in progress internally, Im happy to make a documentation contribution. Could you point me to the appropriate repository where this documentation is maintained ? I'd gladly make a PR to help relieve some of the workload for your team.


---

### 评论 #5 — harkgill-amd (2025-03-13T14:25:17Z)

Hey @fluidnumerics-joe, I've already submitted a PR, just waiting for the changes to be reviewed. Should be live by the EOD.

> Could you point me to the appropriate repository where this documentation is maintained

The ROCm on Radeon docs repository is not currently publicly visible. We are working to transition it to a public repository under the ROCm org, similar to https://github.com/ROCm/rocm-install-on-linux.



---

### 评论 #6 — fluidnumericsJoe (2025-03-13T14:56:39Z)

Excellent to hear. 

On a related note : The more visibility the public has to what's going on behind the scenes, the more opportunity there is for the public to help contribute to ROCm without duplicating efforts. 

---

### 评论 #7 — harkgill-amd (2025-03-14T19:25:14Z)

@fluidnumerics-joe, the note regarding Python wheel versioning has been updated to the following,
```
Important! When manually downloading WHLs from repo.radeon, ensure to select the compatible WHLs for specific Python versions.
```
This change is live at https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-pytorch.html.

---

### 评论 #8 — fluidnumericsJoe (2025-03-17T14:22:47Z)

Thanks @harkgill-amd for working on this one! You guys are awesome

---

### 评论 #9 — zheliangzhi (2025-05-27T15:46:18Z)

在《https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html》中，对ROCM to Ubuntu的描述还停留在6.3。 不过很高兴对pytorch to rocm的描述更新了。希望工作人员能把相关物料更新贴上网站，这会减少很多工作量。在amd网页上rocm以及sdk的寻找太过麻烦

---
