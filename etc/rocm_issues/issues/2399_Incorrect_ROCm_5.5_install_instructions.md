# Incorrect ROCm 5.5 install instructions

> **Issue #2399**
> **状态**: closed
> **创建时间**: 2023-08-23T17:47:58Z
> **更新时间**: 2023-08-24T17:35:28Z
> **关闭时间**: 2023-08-24T14:13:05Z
> **作者**: cgmb
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2399

## 描述

Following the [ROCm 5.5 install instructions](https://rocm.docs.amd.com/en/docs-5.5.1/deploy/linux/installer/install.html) will result in installing ROCm 5.6.

For example:

```
sudo apt update
wget https://repo.radeon.com/amdgpu-install/5.6/ubuntu/focal/amdgpu-install_5.6.50600-1_all.deb
sudo apt install ./amdgpu-install_5.6.50600-1_all.deb
```

---

## 评论 (4 条)

### 评论 #1 — Promesis (2023-08-24T02:42:38Z)

So it should be this?

```shell
sudo apt update
wget https://repo.radeon.com/amdgpu-install/5.5.1/ubuntu/focal/amdgpu-install_5.5.50501-1_all.deb
sudo apt install ./amdgpu-install_5.5.50501-1_all.deb
```

---

### 评论 #2 — Promesis (2023-08-24T05:09:29Z)

A lot of mistakes. RHEL and SUSE. 

---

### 评论 #3 — Promesis (2023-08-24T06:54:40Z)

I incorrectly edited it on `develop` branch. It should be `docs/5.5.1`.

---

### 评论 #4 — cgmb (2023-08-24T17:35:27Z)

Thanks @Promesis!

---
