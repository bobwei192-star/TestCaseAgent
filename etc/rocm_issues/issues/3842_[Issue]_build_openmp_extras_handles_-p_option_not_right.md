# [Issue]:  build_openmp_extras  handles -p option not right

> **Issue #3842**
> **状态**: closed
> **创建时间**: 2024-10-01T09:51:40Z
> **更新时间**: 2025-06-19T19:03:51Z
> **关闭时间**: 2025-06-19T15:36:43Z
> **作者**: jdumke
> **标签**: Under Investigation, AMD Radeon VII, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3842

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon VII** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

The optionsparser in build_openmp_extras.sh sets in lines 42–43  "TARGET"  to "package", but doesn't use $2 to set "MAKETARGET" to given  package format:
'        -p  | --package )
            TARGET="package" ;;'
A coressponding target is not defined in the target selector in lines 666–671:
'case $TARGET in
    (clean) clean_openmp_extras ;;
    (build) build_openmp_extras; package_openmp_extras ;;
    (outdir) print_output_directory ;;
    (*) die "Invalid target $TARGET" ;;
esac'
Given format is ignored, like said above.

### Operating System

Debian 12 Bookworm with Backports

### CPU

AMD Ryzen 5 5600G with Radeon Graphics

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.2.0

### ROCm Component

aomp-extras

### Steps to Reproduce

Open build_openmp_extras.sh in editor, inspect line 42–43 and 666–671.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — ppanchad-amd (2024-10-01T16:01:01Z)

Hi @jdumke, internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — schung-amd (2024-10-02T19:20:21Z)

Hi @jdumke, I'll take a look into whether we should be providing this flag or not. The readme at https://github.com/ROCm/ROCm/tree/develop/tools/rocm-build only states support for `-r` and `-c`, which are defined in the script, and I don't know if this script is meant to be invoked with any of the other options.

Flags aside, the package type is set at https://github.com/ROCm/ROCm/blob/8b630923334b98dd16ac5c604121dc70974d79e2/tools/rocm-build/build_openmp_extras.sh#L549-L557
which is sufficient for the distros that we officially support. If this isn't working for whatever distro you're using you can try editing this.

---

### 评论 #3 — jdumke (2024-10-03T09:53:58Z)

I issued that, hence I find this kind of handling the -p option inconsistent compared to most other scripts within the project, which builds without problems in my environment. 
Ignoring an argument described on the usage-screen is really untypical. And I'm thinking, that the callier to the script implicitly awaits the standard behaviour by passing the option. 
P.S.:
Sometimes a build in wild-life, like mine, shows up things, which would be unrevealed in the closed habitat. And most stage 1 packages build clean actually.

---

### 评论 #4 — schung-amd (2024-10-03T13:32:16Z)

Yes, your observations are correct, and thanks for pointing this out. I understand that we are presenting non-functional options here (and possibly in other scripts), and I'm checking internally to see if we can match how the other scripts consume them or if we should be removing these options. If you come across this issue in any of the other build scripts, please let us know. 

---

### 评论 #5 — jdumke (2024-10-04T09:44:35Z)

I edited the optionhandler to perform the standard behaviour and the script runs properly until the point you quoted, which isn't done by ohther scripts in the same way. Why does set the script the package-type this way and doesn't trust the caller by using the argument passed with -p.  
Optionhandling is quite a thing, which has serveral qualities within the project, for example build_half.sh actually doesn't consume any options, I fixed this in my actual pull request.
Packagegeneration in general is other thing offering a wide range within ROCm. Some subprojects generate not only deb and rpm, but also tar-balls and zip, some doesn't offer the last two.
A last remark for this post: The correct treat of -p is exactly the functionality I requested in #3742.

---

### 评论 #6 — schung-amd (2024-10-04T13:59:58Z)

These issues arise because the GitHub build scripts are ported from internal build scripts and it seems like we haven't sufficiently prepared them for external use. In the case of the `-p` flag in build_openmp_extras, this was probably functional at some point but was changed it to just use `-r` instead with the hardcoded package types. This isn't because we don't trust the caller but rather because this doesn't matter internally, as we have control over how they are being called. Of course, this specific script is still broken since it will consume the `-p` flag in an erroneous way (even internally) and should be addressed.

From a design standpoint, we need to determine whether we intend to only provide functionality for `-c` and `-r` (as stated in the README), or if we want to give external users more control. These scripts work out of the box for any distro we officially support, and handling unsupported distros is likely out of scope, but I'll discuss this with the internal team. 

---

### 评论 #7 — schung-amd (2025-06-19T15:36:43Z)

Moving forward, we will support building from source through TheRock (https://github.com/ROCm/TheRock). As such I'm closing this issue, but feel free to comment if you would like additional guidance.

---

### 评论 #8 — jdumke (2025-06-19T19:02:14Z)

I've forgotten this issue, after the package built without issues in 6.4.1, so I'm fine with closing it.

---
