# De-bloat docker images so they can be used as bases for Dockerfiles

> **Issue #2093**
> **状态**: closed
> **创建时间**: 2023-04-28T04:27:47Z
> **更新时间**: 2024-10-10T18:14:22Z
> **关闭时间**: 2024-10-10T17:55:01Z
> **作者**: deftdawg
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/2093

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

Related to https://github.com/RadeonOpenCompute/ROCm-docker/issues/92

I had to use `podman` to download `rocm5.4.2_ubuntu20.04_py3.8_pytorch_2.0.0_preview`, because `docker` gets stuck downloading some of the layers... 

Podman reports the image as consuming 38GB of disk space!
```
docker.io/rocm/pytorch   rocm5.4.2_ubuntu20.04_py3.8_pytorch_2.0.0_preview  96c28752acb8  3 weeks ago   37.5 GB
```

38 GB is unusable for anyone without terabytes of free disk space.

Each layer operation uses 38GB (+ whatever the layer does), meaning a relatively simple **7 layer** `Dockerfile` based from `rocm5.4.2_ubuntu20.04_py3.8_pytorch_2.0.0_preview` requires more that **450 GB** of free space to build!

I don't know how these images are being built, but there has to be a better way...  Please de-bloat them, so others can make use of them as bases.

---

## 评论 (9 条)

### 评论 #1 — set-soft (2023-05-12T09:38:51Z)

I agree with this, the images I tested range from 29.2 GB to 34.6 GB and I suspect they have a lot of repeated stuff.
I was able to create images of 9 GB containing PyTorch+ROCm, but I understand the images available at docker hub are designed for any ROCm use and also for PyTorch, not the other way around (for PyTorch using ROCm as backend)

P.S. when I say repeated stuff here is what I mean:

```
diff -u /var/lib/jenkins/pytorch/torch/lib/libtorch_cpu.so /opt/conda/lib/python3.7/site-packages/torch/lib/libtorch_cpu.so
```

It returns 0, so you have PyTorch twice: one in Conda, and another in /var/lib/jenkins/

```
# du -hsc /var/lib/jenkins/
4.6G	/var/lib/jenkins/
4.6G	total
# du -hsc /var/lib/jenkins/pytorch
3.8G	/var/lib/jenkins/pytorch
3.8G	total
```

Is this a left over of the docker image build process?

Another source of bloat: the use of Conda, this is a nice tool ... for Windows, not Linux, and definitely not for a docker image. The PyTorch should be compiled for the system Python and avoid Conda.

---

### 评论 #2 — takov751 (2023-10-10T14:54:19Z)

I did a fresh install from a ubuntu docker and was able to run stable diffusion webui without issue 25GB disk space.
I mean it something. work in progress. This is the base image. Loads of room for improvement.

pip.conf
```
[install]
compile = no

[global]
no-cache-dir = True
```

dockerfile
```
FROM ubuntu:22.04 as base
ENV PYTHONDONTWRITEBYTECODE=1
ENV HSA_OVERRIDE_GFX_VERSION=10.3.0
ARG ROCM_VERSION=5.6
ARG AMDGPU_VERSION=5.6
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
  curl -sL http://repo.radeon.com/rocm/rocm.gpg.key | apt-key add - && \
  sh -c 'echo deb [arch=amd64] http://repo.radeon.com/rocm/apt/$ROCM_VERSION/ jammy main > /etc/apt/sources.list.d/rocm.list' && \
  sh -c 'echo deb [arch=amd64] https://repo.radeon.com/amdgpu/$AMDGPU_VERSION/ubuntu jammy main > /etc/apt/sources.list.d/amdgpu.list' && \
  sh -c 'echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' | sudo tee /etc/apt/preferences.d/rocm-pin-600 ' && \
  apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y -f --no-install-recommends \
  sudo \
  rocm-libs \
#  rocm-hip-runtime \
#  libelf1 \
#  libnuma-dev \
#  build-essential \
  git \
  file \
  python3 \
  python3-pip \
  python3.10-venv \
  libgl1 \
  libglib2.0-0 \
#  rocm-dev \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  mkdir /app

COPY ./pip.conf /etc/pip.conf

WORKDIR /app
RUN python3 -m venv /app/venv &&  /app/venv/bin/pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.6




```

---

### 评论 #3 — takov751 (2023-10-14T18:45:28Z)

And now just by changing to fedora and installing rocm-opencl and rocm-hip package and some requirements i am between 10-15GB 

---

### 评论 #4 — ppanchad-amd (2024-05-13T15:32:14Z)

@deftdawg Apologies for the lack of response. Can you please test with latest ROCm 6.1.1? If resolved, please close ticket. Thanks!

---

### 评论 #5 — deftdawg (2024-05-17T20:36:20Z)

> @deftdawg Apologies for the lack of response. Can you please test with latest ROCm 6.1.1? If resolved, please close ticket. Thanks!

Why? Did you actually do anything to fix the issue or are you hoping it went away on it's own?

---

### 评论 #6 — saadrahim (2024-05-17T20:50:19Z)

@deftdawg The docker images have not reduced in size and in fact are likely bigger in size. AMD is aware of this issue and action on this is planned in the long term. 

In the interim, no official workaround is available. 

I am interested in some feedback on possible solutions. Much of the bloat in the size of the docker images are due to supporting multiple GPU architectures. Most end users only have one type of GPU in their system. At the expense of increasing the number of docker containers to choose from, would you prefer choosing between multiple containers? Each container is built for a GPU family such as the CDNA2. The resulting containers would be much smaller than the current.


---

### 评论 #7 — takov751 (2024-05-18T05:01:37Z)

@saadrahim I have done some testing few months ago I was able to create a pytorch-rocm base image for out-of-box stable diffusion (without any additional dependency or plugin) only thing i did was that i rebased docker image to fedora. It seems rpm packages has a different structure and dependencies. And While it's obvious that the official rocm-pytorch has more dev libraries installed to be a proper dev environment. On the other hand for some reason i saw there is duplicated pytorch builds inside that container, which does makes the layers ~2-4GB heavier . So a multi-stage build might be a better approach to keep the layer sizes down.
My example rebased base Dockerfile .The results were around 10GB image size.

```
FROM fedora:38 as base
ENV PYTHONDONTWRITEBYTECODE=1
# force rx6xxx compatible version 
ENV HSA_OVERRIDE_GFX_VERSION=10.3.0
ARG ROCM_VERSION=5.6
ARG AMDGPU_VERSION=5.6
RUN dnf install -y python3-pip git curl  rocm-clinfo && \
    dnf install -y rocm-hip mesa-libGL && \
    dnf clean all && rm -rf /var/cache/yum
COPY ./pip.conf /etc/pip.conf

WORKDIR /app
COPY ./requirements.txt /app
RUN python3 -m venv /app/venv &&  /app/venv/bin/pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.6 && /app/venv/bin/pip3 install -r ./requirements.txt

```


---

### 评论 #8 — tcgu-amd (2024-10-10T17:53:57Z)

Hi @deftdawg, sorry for the lack of responses. ROCm-docker is intended to be a quick way to get started with Docker, hence we included most of the commonly used tools and ROCm components in it such that it works out-of-the-box on supported systems for most usecases. We understand that it can be quite big as a result, and unfortunately we don't see the size decreasing unless we shrink ROCm itself, which is an effort at a much grander scale. 

As @saadrahim suggested, using multi-stage custom builds that only include the necessary components might be the best way to use ROCm on docker for now if storage is an issue. This needs to be done case-by-case. Unfortunately, there is little we can do at the moment. 

However, we are always looking into ways to improve our user's experience with ROCm. Please stay tuned for future ROCm updates that can potentially address this issue. 

I hope this helps. Since there is no clear actionable items attached to this issue at the moment, it will be closed for now, but please feel free to continue the discussion with more follow up questions.

Thanks!!


 

---

### 评论 #9 — deftdawg (2024-10-10T18:14:21Z)

Looking to improve user experiences with RoCM?🤣

If I might humbly suggest as an action item you hire someone who knows how to build docker containers properly and ask them to fix your container build process...

---
