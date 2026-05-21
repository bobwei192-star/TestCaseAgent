# New multi-install instructions for new 6.4.0 are incorrect

> **Issue #4620**
> **状态**: closed
> **创建时间**: 2025-04-13T11:19:14Z
> **更新时间**: 2025-04-17T18:04:25Z
> **关闭时间**: 2025-04-17T18:04:25Z
> **作者**: Krytern
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/4620

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

On Ubuntu 22.04.5 (Jammy) it is these instructions https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/multi-version-install.html

The following command doesn't work;
```
for ver in 6.4.0 6.3.3; do
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/$ver jammy main" \
    | sudo tee --append /etc/apt/sources.list.d/rocm.list
done
echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' \
    | sudo tee /etc/apt/preferences.d/rocm-pin-600
sudo apt update
```

It should instead be written like this;
```
for ver in 6.4 6.3.3; do
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/$ver jammy main" \
    | sudo tee --append /etc/apt/sources.list.d/rocm.list
done
echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' \
    | sudo tee /etc/apt/preferences.d/rocm-pin-600
sudo apt update
```

When adding the repositories, it only works correctly when taking off the .0 on version numbers. When installing from the repositories with `sudo apt install`then you need to keep the .0 there.

This was an issue that had been forwarded to the docs team for an old version 5.7 instructions the other day so this seems to be an ongoing confusion.

I'd recommend making things actually consistent, have the .0 there for both or not there for both, doesn't make much sense to have them different when you're doing one command right after the other.

EDIT: Another error I forgot to mention is when adding the amdgpu-dkms repository, you need to remove some spaces on the first line or it won't work on Ubuntu (Both Noble and Jammy)

Current instructions that don't work;
```
ver = 6.4
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/$ver/ubuntu jammy main" \
    | sudo tee /etc/apt/sources.list.d/amdgpu.list
sudo apt update
```

Changed to this so it works;
```
ver=6.4
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/$ver/ubuntu jammy main" \
    | sudo tee /etc/apt/sources.list.d/amdgpu.list
sudo apt update
```

The error where you need to remove the spaces is in older version install instructions too.

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-04-14T13:56:09Z)

Hi @Krytern. Internal ticket has been created to update instructions. Thanks!

---

### 评论 #2 — harkgill-amd (2025-04-16T14:45:17Z)

Hi @Krytern, thanks again for the report. The changes you suggested were implemented under https://github.com/ROCm/rocm-install-on-linux/pull/437. Please take a look and close out the issue if everything's been addressed and is working on your end.

---

### 评论 #3 — Krytern (2025-04-17T18:04:20Z)

Hello, following the instructions now by just copy-pasting works without any errors so closing this issue.

---
