# Inquiry About Image Changes Between Oct 20 to now for rocm/7.0-preview:rocm7.0_preview_ubuntu_22.04_vllm_0.10.1_instinct_beta

> **Issue #5687**
> **状态**: closed
> **创建时间**: 2025-11-21T07:13:54Z
> **更新时间**: 2026-02-20T19:07:24Z
> **关闭时间**: 2026-02-20T19:07:24Z
> **作者**: Jiarwang77
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5687

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

I am currently using the Docker image:
rocm/7.0-preview:rocm7.0_preview_ubuntu_22.04_vllm_0.10.1_instinct_beta
 
Recently, I pulled this image again and noticed that although the tag remains the same, the source code inside the preinstalled vllm package (specifically the filesystem under /opt/venv/lib/python3.10/site-packages/vllm) is different from what I obtained in an earlier pull. Because I need to modify the VLLM source code to support MXFP emulation experiments qdq.
 
This caused the current image to be slower than the previous one, but I accidentally deleted the previous image version. I thought it would be the same, so I re-pulled this image, but the VLLM inference speed has become slower.
 
So, were there any updates, rebuilds, or modifications made to this image between October 20 to now? Even if the tag did not change, any rebuild that altered the content would be important for me to know.
 
If there were changes, is it possible to obtain or access the image version that between Oct 20-Oct 24? If you're not sure, could you tell me who I can contact to know this problem?


---

## 评论 (4 条)

### 评论 #1 — ianbmacdonald (2025-11-29T01:28:30Z)

Interesting.  There is a very similar [7.0-preview/rocm7.0_preview_ubuntu_22.04_vllm_0.10.1_instinct_rc1](https://hub.docker.com/layers/rocm/7.0-preview/rocm7.0_preview_ubuntu_22.04_vllm_0.10.1_instinct_rc1/images/sha256-eee29678dc4dc8f2e054de889555be6f4fd74e58053bf7277d56ace1a850513e) 

Since this repo was [built for an event](https://hub.docker.com/r/rocm/7.0-preview), where this image might be kicking around on somebody's image shelf....   

a) Crowd source it.   Anyone with an older image, post here in the comments.  If it looks different than below, you have an older digest.

```
$ docker images --digests | grep rocm/7.0-preview
rocm/7.0-preview   rocm7.0_preview_ubuntu_22.04_vllm_0.10.1_instinct_beta   sha256:ac5bf30a1ce1daf41cc68081ce41b76b1fba6bf44c8fab7ccba01f86d8f619b8   2df455ea2093   3 months ago   35.3GB
```

Once posted, download that older immutable digest:
```
docker pull rocm/7.0-preview@sha256:ac5bf30a1ce1daf41cc68081ce41b76b1fba6bf44c8fab7ccba01f86d8f619b8
```

b) Fast forward.  you can change any / all of  ROCm version / Ubuntu version / vLLM version forwards/backwards in a packaged environment + uv managed venv, working around the underlying issue.  It has been manageable for a while;  I can help. [MI300X is buttery smooth](https://netstatz.com/rocm-7-quickstart-cloudrift-mi300x/).

---

### 评论 #2 — darren-amd (2025-12-02T19:34:51Z)

Hi @Jiarwang77.

I'm going to reach out to the internal team to see if we made any changes to those released images. As suggested above, having your own managed environment may be more stable for the future. We also have vllm docker images available [here](https://hub.docker.com/r/rocm/vllm-dev/tags) with dated container releases.

---

### 评论 #3 — darren-amd (2026-02-03T20:33:47Z)

Hi @Jiarwang77,

Just an update on this, I haven't gotten a hold of the team that published the event docker containers but since it's been a while I wanted to check in if the above suggestions solved the issue for you or if the issue persists?

---

### 评论 #4 — darren-amd (2026-02-20T19:07:24Z)

I'm going to close this off since the container is outdated now. We have newer containers available [here](https://hub.docker.com/r/rocm/dev-ubuntu-24.04/tags).

---
