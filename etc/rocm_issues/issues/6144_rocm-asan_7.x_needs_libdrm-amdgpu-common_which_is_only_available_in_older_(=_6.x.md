# rocm-asan 7.x needs libdrm-amdgpu-common which is only available in older (<= 6.x) amdgpu drivers

> **Issue #6144**
> **状态**: closed
> **创建时间**: 2026-04-13T11:47:33Z
> **更新时间**: 2026-04-20T14:34:59Z
> **关闭时间**: 2026-04-20T14:34:58Z
> **作者**: ragges
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6144

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

Hi,

rocm-asan 7.x needs libdrm-amdgpu-common which is only available in older (<= 6.x) amdgpu drivers.

I guess libdrm-amdgpu-common should be shipped with amdgpu >= 7.x (also >= 25.x).

Regards
Ragnar


---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2026-04-13T14:43:29Z)

Hey @ragges, how are you installing rocm-asan in this case? Looks like the `libdrm-amdgpu-common` packages were moved from https://repo.radeon.com/amdgpu/ to https://repo.radeon.com/graphics/ with ROCm 7.

---

### 评论 #2 — ragges (2026-04-13T16:06:57Z)

Hi @harkgill-amd,

Thanks for looking into this!
I am downloading amdgpu from https://repo.radeon.com/amdgpu/${version}/, and rocm from 
https://repo.radeon.com/rocm/zyp/${version}/, and since rocm 5 I have been installation with essentially:

latestver=7.2.1
zypper -i ${IMGNAME} install rocm${latestver} rocm-language-runtime${latestver} rocm-hip-runtime${latestver} rocm-opencl-runtime${latestver} rocm-hip-runtime-devel${latestver} rocm-opencl-sdk${latestver} rocm-hip-libraries${latestver} rocm-hip-sdk${latestver} rocm-developer-tools${latestver} rocm-ml-sdk${latestver} rocm-ml-libraries${latestver} rocm-openmp-sdk${latestver} rocm-llvm${latestver} rocm-llvm-devel${latestver} rocm-llvm-docs${latestver} rocm-validation-suite${latestver} rocm-bandwidth-test${latestver} rdc${latestver} \
       rocm-asan-7.2.1.70201 rocm-ml-sdk-asan-7.2.1.70201 rocm-developer-tools-asan-7.2.1.70201

Note:
* The reason for pointing out an explicit version is that when I am building a new image, I have repos for all relevant ROCm versions available, I install rocm-core for all versions of rocm that I want to include one by one, and then full ROCm only for the last version as above (to have the /etc/alternatives etc set correctly for the last version (though for my case I would actually prefer if it didn't touch /etc/alternatives or /{bin,sbin,usr/bin,usr/sbin} or the rest of the filesystem at all and just put everything in /opt/rocm-N.N.N and did not touch anything else)). After the installation, I remove the entire /opt/rocm-${latestver} from the image and replace it with an empty directory. When the nodes boot they mount in squashfs images for every /opt/rocm-N.N.N directory there is with full ROCm installations. That way I don't have to have all ROCm:s fully installed on all different compute node images, which saves a _lot_ of space when you are experimenting with different images.
* The rocm-asan stuff on the last line is different; it used to work with rocm-asan${ver} etc, but in 7.2.1, and 7.0.3, those packages are missing (and they also seem to be duplicates of the ones mentioned above, so there might be reasons for removing them, but it was still a bit surprising to me). I have opened a ticket for that thing too, to figure out if it is intentional and I should adapt to it or not.
Maybe I should change my procedure, but this has worked until now.

---

### 评论 #3 — harkgill-amd (2026-04-13T17:32:50Z)

So with ROCm 7+, it is actually necessary to setup the `graphics` repo alongside both `rocm` and `amdgpu` repos. See the following excerpt from https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-sles.html#registering-rocm-repositories
```
Registering ROCm repositories

SLES 15.7
sudo tee /etc/zypp/repos.d/rocm.repo <<EOF
[rocm]
name=ROCm 7.2.1 repository
baseurl=https://repo.radeon.com/rocm/zyp/7.2.1/main
enabled=1
gpgcheck=1
gpgkey=https://repo.radeon.com/rocm/rocm.gpg.key

[amdgraphics]
name=AMD Graphics 7.2.1 repository
baseurl=https://repo.radeon.com/graphics/7.2.1/sle/15.7/main/x86_64/
enabled=1
priority=50
gpgcheck=1
gpgkey=https://repo.radeon.com/rocm/rocm.gpg.key
EOF
sudo zypper refresh
```
With this in place, the asan packages from your command should be able to pull in the `libdrm-amdgpu-common` dependency.

---

### 评论 #4 — harkgill-amd (2026-04-20T14:34:58Z)

Closing this out for now but feel free to leave a comment if you have any questions.

---
