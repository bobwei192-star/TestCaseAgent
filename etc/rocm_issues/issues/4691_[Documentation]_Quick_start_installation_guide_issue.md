# [Documentation]: Quick start installation guide issue

> **Issue #4691**
> **状态**: closed
> **创建时间**: 2025-04-27T12:37:11Z
> **更新时间**: 2025-04-29T13:52:35Z
> **关闭时间**: 2025-04-29T13:52:34Z
> **作者**: Toni67
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4691

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Description of errors

On the [quick installation guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html) for ROCm with Ubuntu 22.04 

The script :
`wget https://repo.radeon.com/amdgpu-install/6.4/ubuntu/jammy/amdgpu-install_6.4.60400-1_all.deb
sudo apt install ./amdgpu-install_6.4.60400-1_all.deb
sudo apt update
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
sudo apt install rocm`

Return an error :
`Err:7 https://repo.radeon.com/rocm/apt/6.4.0 jammy Release
  404  Not Found`


Had to edit : `/etc/apt/sources.list.d/rocm.list` 


Replaced:
`deb https://repo.radeon.com/rocm/apt/6.4.0 jammy main`

by:
`deb https://repo.radeon.com/rocm/apt/6.4 jammy main`

To get it to work





### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2025-04-28T14:36:43Z)

Hi @Toni67, I'm not seeing `deb https://repo.radeon.com/rocm/apt/6.4.0 jammy main` being installed on my end with the [22.04 quick start install instructions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#rocm-installation).

To double check, could you please remove you're current ROCm installation with 
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```
Then reinstall `amdgpu-install`, which sets up the repos, with 
```
wget https://repo.radeon.com/amdgpu-install/6.4/ubuntu/jammy/amdgpu-install_6.4.60400-1_all.deb
sudo apt install ./amdgpu-install_6.4.60400-1_all.deb
sudo apt update
```
You should now see `deb https://repo.radeon.com/rocm/apt/6.4 jammy main` in the output of `cat /etc/apt/sources.list.d/rocm.list`. If you're still seeing `deb https://repo.radeon.com/rocm/apt/6.4.0 jammy main`, please let me know and I'll investigate further.

---

### 评论 #2 — Toni67 (2025-04-28T22:06:31Z)

Yes, it's working perfectly, my bad
I tried a fresh new install and the script from the guide worked on first try
Yesterday too it was on a new install, I don't know what happened, sorry for the trouble

---

### 评论 #3 — harkgill-amd (2025-04-29T13:52:34Z)

No worries. It's possible there may have been an intermittent bug that was fixed. Will close this issue out.

---
