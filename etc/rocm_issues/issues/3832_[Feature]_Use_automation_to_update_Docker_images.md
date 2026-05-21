# [Feature]: Use automation to update Docker images.

> **Issue #3832**
> **状态**: closed
> **创建时间**: 2024-09-28T19:41:23Z
> **更新时间**: 2024-10-15T19:48:42Z
> **关闭时间**: 2024-10-15T19:47:02Z
> **作者**: rudiservo
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/3832

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

Docker hub does not have latest version of ROCm images, I recommend using some sort of automation to build new images and publish in docker hub and in github.
Update the base image to 24.04.

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-10-11T18:50:28Z)

Hi @rudiservo, you can find the latest Ubuntu 24.04 ROCm docker image at https://hub.docker.com/r/rocm/dev-ubuntu-24.04. Is there a specific image you are referring to?

---

### 评论 #2 — rudiservo (2024-10-11T22:02:50Z)

Hi @harkgill-amd, I think that at the time 24.04 didn't have 6.2.1 the latest version is 6.2.2, a minor change so I don't know how relevant the update is.

---

### 评论 #3 — harkgill-amd (2024-10-15T19:47:02Z)

We do now have automation in place to build and publish new images to docker hub in the form of a GitHub action. The automation is triggered by a PR, which was just done for ROCm 6.2.2. You should see the new image up shortly.

In the future, if you notice that a ROCm release does not have a corresponding docker image, feel free to leave a comment here or create a new issue.

---
