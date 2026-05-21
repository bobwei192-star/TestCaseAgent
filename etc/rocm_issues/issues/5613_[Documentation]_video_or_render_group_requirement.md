# [Documentation]: video or render group requirement

> **Issue #5613**
> **状态**: closed
> **创建时间**: 2025-10-31T22:23:14Z
> **更新时间**: 2025-12-22T16:12:14Z
> **关闭时间**: 2025-11-06T20:17:04Z
> **作者**: vysocky
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5613

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Description of errors

Hi, the requirement to be a member of the render or video group is no longer in the documentation. In the past, it was mentioned in https://rocmdocs.amd.com/en/latest/InstallGuide.html#setting-permissions-for-groups (for reference #1622), but this page is no longer part of the guide.

Has this requirement been removed in the recent ROCm version? I have not found such a change in the changelog. Thank you.

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2025-11-03T16:26:57Z)

Hey @vysocky, the requirement for GPU access is still present https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#configuring-permissions-for-gpu-access. We added the udev option as an alternative to `video` and `render` group membership - though one (udev) or the other (video/render) is still required.

---

### 评论 #2 — harkgill-amd (2025-11-06T20:17:04Z)

Closing this out but feel free to leave a comment if you have any questions.

---

### 评论 #3 — vysocky (2025-11-21T09:38:53Z)

Hi @harkgill-amd, it is not clear to me whether the user must be a member of one of these groups or both. Thanks

---

### 评论 #4 — vysocky (2025-12-19T23:20:03Z)

Hi @harkgill-amd can you clarify the answer?

---

### 评论 #5 — harkgill-amd (2025-12-22T16:12:14Z)

Hey @vysocky, sorry I missed this the first time. You'd need to be apart of both the video and render groups for ROCm - see this excerpt for more info on them https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#using-group-membership

> By default, GPU access is managed through membership in the video and render groups. The video and render groups are system groups in Linux used to manage access to graphics hardware and related functionality. Traditionally, the video group is used to control access to video devices, including graphics cards and video capture devices. The render group is more recent and specifically controls access to GPU rendering capabilities through Direct Rendering Manager (DRM) render nodes.

---
