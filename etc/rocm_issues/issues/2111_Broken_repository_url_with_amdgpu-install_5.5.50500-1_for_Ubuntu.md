# Broken repository url with amdgpu-install 5.5.50500-1 for Ubuntu

> **Issue #2111**
> **状态**: closed
> **创建时间**: 2023-05-04T12:37:27Z
> **更新时间**: 2024-05-13T16:08:33Z
> **关闭时间**: 2024-05-13T16:08:32Z
> **作者**: illwieckz
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/2111

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

When installing `amdgpu-install_5.5.50500-1_all.deb` it writes a file named `/etc/apt/sources.list.d/amdgpu-proprietary.list` that contains this content:

```
# Enabling this repository requires acceptance of the following license:
# /usr/share/amdgpu-install/AMDGPUPROEULA
#deb https://repo.radeon.com/amdgpu/@AMDGPUVER@/ubuntu jammy proprietary
```

Notice the bad `@AMDGPUVER@` string (instead of `5.5` version string) that makes this file unusable.

---

## 评论 (8 条)

### 评论 #1 — sofiageo (2023-05-04T13:25:41Z)

somewhat related, the proprieraty repository is missing completely (this is very common though for most releases)

---

### 评论 #2 — illwieckz (2023-05-08T09:40:29Z)

Yes, I had to set `5.4.5` instead:

```
# Enabling this repository requires acceptance of the following license:
# /usr/share/amdgpu-install/AMDGPUPROEULA
deb https://repo.radeon.com/amdgpu/5.4.5/ubuntu jammy proprietary
```

---

### 评论 #3 — dictvm (2023-07-19T09:40:09Z)

Stumbled upon this as well. Am I mistaken if I assume that having fixed versions (like 5.6) in my sources.list-files would mean that ROCM won't update to versions (like 5.7) in the future? That'd be my expectation and I don't really want to manually look up ROCM versions every now an then. 

---

### 评论 #4 — MathiasMagnus (2023-07-19T12:30:24Z)

@dictvm Not 100% authoritative answer, but to my best knowledge current AMD Linux release strategy is that versioned repositories don't update automatically and that is by design. Take a look at https://repo.radeon.com/rocm/apt/ where all versioned entries live. There is an unversioned `latest` repository, but do take two things into account:
- `latest` for whatever reason doesn't follow patch versions. If at some time 5.6 is latest and 5.6.1 or 5.6.2 is released, `latest` will still point to 5.6.
- As a long time user of ROCm, my experience is that incremental updates typically don't work. At one point I/we gave up and just do the quarterly update manually by uninstalling everything, unregistering the old, registering the new, install and call it a day. I would very much like to live in a world where that's not the case, but my impression is that this use case is outside the packaging test matrix and something _always_ breaks. Feel free to give it a spin, but do expect sharp edges and the fact that point releases are not serviced this way.

If someone is looking for auto-updating versions of ROCm, they may be better off with the repo maintainers packaging of the ecosystem. They are still in their infancy, but may be a viable alternative (with a potentially different set of headaches).

---

### 评论 #5 — illwieckz (2023-07-20T02:03:31Z)

My experience is that when updating the package, the version string in the `amdgpu-proprietary.list` file gets replaced by `@AMDGPUVER@` again.

_Edit:_ using `latest` brings warnings but works, I doubt it prevents to be overwritten by `@AMDGPUVER@` again, but this makes easy to fix it mindlessly.

---

### 评论 #6 — dictvm (2023-07-26T12:37:06Z)

Thanks to the both of you! I'll keep it as it is for now. 5.6 is performing decently and I'll know if versions >5.6  will be released so I can manually update anyways!

---

### 评论 #7 — ppanchad-amd (2024-05-13T15:41:20Z)

@illwieckz Apologies for the lack of response. Can you please test with latest ROCm 6.1.1? If resolved, please close ticket. Thanks!

---

### 评论 #8 — illwieckz (2024-05-13T16:08:32Z)

@ppanchad-amd Hi, the problem is fixed since ROCm 5.7.

---
