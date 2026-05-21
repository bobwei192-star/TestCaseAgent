# aqlprofiles and opencl-icd-loaders build will fail on rpm-based systems, …

> **Issue #3868**
> **状态**: closed
> **创建时间**: 2024-10-06T13:17:16Z
> **更新时间**: 2025-06-26T14:31:00Z
> **关闭时间**: 2025-06-26T14:31:00Z
> **作者**: jdumke
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3868

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

… even the supported ones.
Hi,
while my studies of the build_*.sh scrpits I found these two mentioned above.
Both seem to be binary only packages and the precompiled binaries are only distributed as deb for the supported incarnations of Ubuntu, but when building under RHEL or SLES this packages will fail, hence there is no building path which leads to success. Three reasons for that:
1. These systems will fail the implemented distro check
2.  In regular, they won't have dpkg installed.
3. It is not known which deb to choose to meet the versions of dependencies

Is it possible to provide the binary blobs as tar-balls and repack it after checking which package management is used?

Here are my suggestions for those checks:

```bash
isDpkgAvail(){
  if  [ "" != $(which dpkg) ]; then
    return 0
 else
    return -1
  fi
}

isRpmAvail(){
  if [ "" != $(which rpm) ]; then
    return 0
  else
    return -1
  fi
}
```


---

## 评论 (5 条)

### 评论 #1 — schung-amd (2024-10-07T17:04:36Z)

Hi, thanks for reporting this. I'm not sure why `build_aqlprofile.sh` explicitly requires Ubuntu, as the internal build script does not have this check. As ROCm can be installed with other installation methods on RHEL and SLES I suspect either we do have packages that can be provided for this component or this just isn't installed on RHEL and SLES; I'll reach out to the internal team to figure out what's going on here. 

I don't see `build_opencl-icd-loaders.sh` in `ROCm/tools/rocm-build/`, is this somewhere else?

---

### 评论 #2 — jdumke (2024-10-07T19:26:38Z)

It seems to appear, when opencl_on_rocclr tries to fullfill its dependcies, or the T_opencl_icd_loaders target is called. 
This target is listed by make -f ROCm/tools/rocm-build/ROCm.mk list_components. There are some scripts which appears when a depending package tries to fullfill it's prequisites.
In my fork of ROCm the file is absent, but in the synced clone it's present.

---

### 评论 #3 — schung-amd (2024-10-07T20:14:56Z)

Interesting, I'll take a look.

As for `build_aqlprofile.sh`, there are several factors complicating this, and the internal team is discussing how to handle it. As you've noted, this component uses a pre-compiled binary because it is currently closed-source. There is some work being done to make this open-source in a future release, but in the meanwhile we should probably provide an rpm for it as well. It sounds like we'll probably have a fix for this soon, potentially backported to 6.2.

---

### 评论 #4 — jdumke (2024-10-07T22:26:11Z)

I think the deb packages contain a mandatory agreement to licence-terms, which is the point why the project could not provide tar-balls with the blobs. 

---

### 评论 #5 — schung-amd (2025-06-26T14:31:00Z)

Closing this for now. AQLprofile is now open source, but also building from source is now supported by TheRock (https://github.com/ROCm/TheRock) rather than these build scripts.

---
