# ROCm installation might fail in some Linux distribution kernels

> **Issue #4671**
> **状态**: open
> **创建时间**: 2025-04-23T16:07:20Z
> **更新时间**: 2025-04-30T04:54:13Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4671

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

ROCm 6.4.0 might encounter an installation issue on some Linux distribution kernels, including the [patch](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=9011e49d54dcc7653ebb8a1e05b5badb5ecfa9f9) that adds more restrictions for symbol lookups. This change breaks the standard symbol lookup methods in the kernel.

As a result, the AMD kernel driver Dynamic Kernel Mode Support (DKMS) package might fail to install when the symbols required to use the PeerDirect API with Mellanox NICs are not found. In the event of such a failure, the AMD DKMS package attempts to locate these symbols directly from the Mellanox installation. However, for non-standard Mellanox NIC installations, the AMD DKMS package might not be able to locate these symbols.

This issue will be fixed in a future ROCm release. As a workaround, you can run this [script](https://github.com/ROCm/ROCm/releases/download/rocm-6.4.0/64_workaround.sh) that allows the DKMS package to locate Mellanox symbols from the Mellanox installation without you requiring to update the new DKMS package. 

## Workaround 

Follow the steps to run the script: 

1. Download the [script](https://github.com/ROCm/ROCm/releases/download/rocm-6.4.0/64_workaround.sh).

2. Move the script to the machine to be updated, and become the root user (sudo –s). 

3. Run the following commands: 

 
```
chmod +x 64_workaround.sh 

export DEBIAN_FRONTEND=noninteractive 

./64_workaround.sh 
```
                
  The script might take a significant amount of time to download all the components and install ROCm 6.4.0.  

4. After the script runs successfully, you will see the following output in the CLI.  
 

![Image](https://github.com/user-attachments/assets/f9d7d70f-556e-4c53-b92e-f382f8de19e9)

Note that the version of the driver is 6.12.12. 

 
## Workaround details

To mitigate the issue, the script provided will drive the installation of ROCm 6.4 on Ubuntu 22.04 with a 6.8.0-x kernel. 

This script will remove pre-existing `amdgpu-dkms` drivers, `libucx` libraries, and the `ucx` package that might interfere with this installation. Moreover, the script removes the specific DKMS amdgpu kernel build that resulted in the symbol lookup errors when attempting ROCm installation.  The script then adds the updated repositories, updates the package cache, and installs the amdgpu-dkms driver. 

This installation will fail in a specific manner, indicating that there are missing symbols.  A patch to the DKMS Kbuild is then applied, enabling the use of those symbols. 

If the soft links for searching the kernel config for the symbols are not present, the script also creates the two soft links.

The script will then pass the two needed environment variables to the `apt install –f` command, which will then repair the installation and rerun the DKMS build and installation steps using the patch and environment variables. 

As a result, ROCm 6.4 is installed, a `depmod` scan for the module dependencies is made, the `amdgpu` module is inserted into the kernel, and the `rocm-smi` command is run, listing your GPUs.  Finally, `modinfo amdgpu` command is run to check the version of the module being used.

---

## 评论 (1 条)

### 评论 #1 — jhlee508 (2025-04-30T04:54:12Z)

This issue also happens on [ROCm 6.3.4 for Radeon GPUs](https://rocm.docs.amd.com/projects/radeon/en/latest/index.html) since this ROCm version also has similar version of Linux kernel, which also needs to updated on future ROCm (for Radeon GPUs) release.

---
