# [Documentation]: Incorrect wget URL in Radeon docs

> **Issue #5615**
> **状态**: closed
> **创建时间**: 2025-11-02T06:44:35Z
> **更新时间**: 2025-11-04T15:31:27Z
> **关闭时间**: 2025-11-04T15:31:27Z
> **作者**: dpasceri
> **标签**: status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/5615

## 标签

- **status: fix submitted** (颜色: #75d97e)

## 负责人

- harkgill-amd

## 描述

### Description of errors

In the Radeon specific ROCm 7.1 install guide, the wget command points to an invalid repo path because the version number (7.1) is missing from the beggining of the URL.

### Attach any links, screenshots, or additional evidence you think will be helpful.

From the non radeon docs 
"wget https://repo.radeon.com/amdgpu-install/7.1/ubuntu/noble/amdgpu-install_7.1.70100-1_all.deb"

From the radeon docs
"wget https://repo.radeon.com/amdgpu-install/ubuntu/noble/amdgpu-install_7.1.70100-1_all.deb"

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-11-03T16:10:56Z)

Thanks for the heads up @dpasceri - will get this fixed.

---

### 评论 #2 — harkgill-amd (2025-11-04T15:31:27Z)

This is fixed over at https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html#install-amd-unified-driver-package-repositories-and-installer-script. Thanks again!

---
