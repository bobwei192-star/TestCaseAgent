# Obsolete -src repo setup by amdgpu-install 

> **Issue #6140**
> **状态**: open
> **创建时间**: 2026-04-11T00:14:38Z
> **更新时间**: 2026-05-13T16:50:07Z
> **作者**: dvdgomez
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6140

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

Installing the `amdgpu-install` package gives a repo file `/etc/yum.repos.d/amdgpu.repo` with the repository definition of:

```
[amdgpu-src]
name=AMDGPU 30.30.1 repository
baseurl=https://repo.radeon.com/amdgpu/30.30.1/el/$amdgpudistro/main/source
enabled=0
gpgcheck=1
gpgkey=file:///etc/amdgpu-install/rocm.gpg.key
```

However, when attempting to use said repository it reports back a 404 error:
```
dnf --repo=amdgpu-src list available
AMDGPU 30.30.1 repository                                                                                                                                                                                       
Errors during downloading metadata for repository 'amdgpu-src':
  - Status code: 404 for https://repo.radeon.com/amdgpu/30.30.1/el/9.7/main/source/repodata/repomd.xml
Error: Failed to download metadata for repo 'amdgpu-src': Cannot download repomd.xml: Cannot download repodata/repomd.xml: All mirrors were tried
```
I checked the index listing and it seems source is not there like x86_64 as an option https://repo.radeon.com/amdgpu/30.30/el/9.7/main/

Is this repository meant to be there and if so can this be fixed? Sorry in advance if this is not the place to file this issue. 

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2026-04-13T19:13:47Z)

Hey @dvdgomez, so we're only enabling the `amdgpu` entry not `amdgpu-src`, see the `enabled=0/1` entries.
```
[amdgpu]
name=AMDGPU 30.30.1 repository
baseurl=https://repo.radeon.com/amdgpu/30.30.1/el/$amdgpudistro/main/x86_64
enabled=1
gpgcheck=1
gpgkey=file:///etc/amdgpu-install/rocm.gpg.key

[amdgpu-src]
name=AMDGPU 30.30.1 repository
baseurl=https://repo.radeon.com/amdgpu/30.30.1/el/$amdgpudistro/main/source
enabled=0
gpgcheck=1
gpgkey=file:///etc/amdgpu-install/rocm.gpg.key
```
Looking at the older releases, it doesn't look like we ever had packages available `../el/$amdgpudistro/main/source` so it's likely that this is an obsolete entry that hasn't been removed. Will check in with the installer team if we're good to remove this but you shouldn't see any functional issues with this being disabled by default.

---

### 评论 #2 — dvdgomez (2026-04-13T20:52:46Z)

Thank you for the response @harkgill-amd! I see, I would have been interested in the source rpms if that repository existed to provide them. Confirming that I can access the other repository just fine for amdgpu-dkms as it is enabled by default and the repository url is valid.  

---
