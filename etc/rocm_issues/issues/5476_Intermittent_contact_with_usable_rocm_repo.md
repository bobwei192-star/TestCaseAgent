# Intermittent contact with usable rocm repo

> **Issue #5476**
> **状态**: closed
> **创建时间**: 2025-10-07T11:53:08Z
> **更新时间**: 2025-10-14T14:53:11Z
> **关闭时间**: 2025-10-07T17:30:20Z
> **作者**: sjr20
> **标签**: status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/5476

## 标签

- **status: fix submitted** (颜色: #75d97e)

## 负责人

- harkgill-amd

## 描述

Hi,

Since last week I have been experiencing increasing difficulty using the ROCm repo at

https://repo.radeon.com/rocm/el9/latest/main

Occasionally, I can access this successfully but I am now repeatedly receiving download errors like the following:

`dnf --refresh --enablerepo=ROCm list rocm
AMD ROCm repository                                                                                               2.2 kB/s | 1.1 kB     00:00    
Errors during downloading metadata for repository 'ROCm':
  - Status code: 404 for https://repo.radeon.com/rocm/el9/latest/main/repodata/83977142cdd069243fe3e3bdd41cbff686dbe6c1dfccdf6496b5c25141baab49-primary.xml.gz (IP: 23.48.165.4)
  - Status code: 404 for https://repo.radeon.com/rocm/el9/latest/main/repodata/5e84f1ad7df04733eda63d4fe25ccf18a114570dbf58ea9117c482a0811a5ca5-filelists.xml.gz (IP: 23.48.165.4)
Error: Failed to download metadata for repo 'ROCm': Yum repo downloading error: Downloading error(s): repodata/83977142cdd069243fe3e3bdd41cbff686dbe6c1dfccdf6496b5c25141baab49-primary.xml.gz - Cannot download, all mirrors were already tried without success; repodata/5e84f1ad7df04733eda63d4fe25ccf18a114570dbf58ea9117c482a0811a5ca5-filelists.xml.gz - Cannot download, all mirrors were already tried without success
`
I believe the repos on at least the ip addresses 23.1.96.192, 23.48.165.4, 23.48.165.31, 2.19.248.134, 2.19.248.149 may be missing some files under repodata. This is making it very difficult to install the latest ROCm on the MI300X boxes we have in Cambridge.

Many thanks for your attention -

Best regards

Stuart


---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2025-10-07T14:07:05Z)

Thanks for the report @sjr20. Do you see these download errors for previous releases or just latest, https://repo.radeon.com/rocm/el9/latest/main?

---

### 评论 #2 — sjr20 (2025-10-07T14:30:20Z)

Thanks for your reply - I've tried a couple of other releases and they seem fine, so I think this issue just affects the latest version.

---

### 评论 #3 — harkgill-amd (2025-10-07T16:40:24Z)

We just finalized some changes on our backend for https://repo.radeon.com/rocm/el9/latest/main. Could you check to see if the 404 errors are resolved on your end?

---

### 评论 #4 — sjr20 (2025-10-07T16:54:29Z)

Things are looking much better, no more 404 errors produced during multiple further attempts. Many thanks for your swift help.

Best regards,

Stuart


---

### 评论 #5 — harkgill-amd (2025-10-07T17:30:20Z)

No problem. I'm going to go ahead and close this issue out but if you do encounter the 404 errors again, please leave a comment and I'll re-open this.

---
