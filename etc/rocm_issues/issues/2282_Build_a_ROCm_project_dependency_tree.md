# Build a ROCm project dependency tree

> **Issue #2282**
> **状态**: open
> **创建时间**: 2023-06-28T13:22:24Z
> **更新时间**: 2025-04-15T18:23:09Z
> **作者**: saadrahim
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2282

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

- How will it be built?
- How will it be maintained?
https://github.com/mgaitan/sphinxcontrib-mermaid
https://devblogs.microsoft.com/cppblog/vcpkg-integration-with-the-github-dependency-graph/

---

## 评论 (9 条)

### 评论 #1 — SamuelMarks (2023-07-10T18:50:03Z)

@saadrahim How's this progressing?

FYI - I've been using this unofficial guide: https://gist.github.com/rigtorp/d9483af100fb77cee57e4c9fa3c74245

---

### 评论 #2 — saadrahim (2023-07-21T21:28:04Z)

@SamuelMarks no activity on this issue has been started. There will be a PR mentioning this when we start.

---

### 评论 #3 — amd-isparry (2023-07-23T05:16:40Z)

Internally the CI has a single source of truth for this. 

---

### 评论 #4 — SamuelMarks (2023-07-23T19:49:12Z)

FYI: In the meantime I've started updating and improving that aforementioned guide in my fork: https://gist.github.com/SamuelMarks/2342bb814126b825e8b995446f9dc8e6

Currently debugging https://github.com/RadeonOpenCompute/ROCR-Runtime:
```
[100%] Linking CXX shared library libhsa-runtime64.so
/usr/bin/ld: cannot find -lhsakmt: No such file or directory
collect2: error: ld returned 1 exit status
gmake[2]: *** [CMakeFiles/hsa-runtime64.dir/build.make:674: libhsa-runtime64.so.1.1.9] Error 1
gmake[1]: *** [CMakeFiles/Makefile2:89: CMakeFiles/hsa-runtime64.dir/all] Error 2
gmake: *** [Makefile:156: all] Error 2
-- Install configuration: ""
CMake Error at cmake_install.cmake:57 (file):
  file INSTALL cannot find
  "ROCm/ROCR-Runtime/src/build/libhsa-runtime64.so.1.1.9": No
  such file or directory.
```

---

### 评论 #5 — nartmada (2024-03-16T02:36:47Z)

Hi @saadrahim, do you know if this "ROCm project dependency tree" has been completed?  If not, I will need to assign this ticket to the documentation team.  Thanks.

---

### 评论 #6 — saadrahim (2024-03-22T14:39:33Z)

This has not been completed. 

---

### 评论 #7 — nartmada (2024-03-22T14:47:13Z)

An internal task ticket has been created to track the progress.

---

### 评论 #8 — garrettbyrd (2025-03-26T19:40:37Z)

I just opened a [PR on rocm-blogs](https://github.com/ROCm/rocm-blogs/pull/64) for a blog post that included a ROCm dependency matrix graphic.

[Is this the kind of dependency visualization you are looking for?](https://github.com/ROCm/rocm-blogs/blob/47d8d57b27d3e5e1f91aad702ba772df5ef2af8c/blogs/software-tools-optimization/spack-installation/images/dep_matrix.png)

Obviously the titular request here is for a dep *tree*, not a matrix, but a dep tree for ~70 packages can be... messy. Regardless, I store it as an np array so it can be visualized as such if desired.

The major caveat here is that this visualization utilizes Spack to get dependencies. (Quick shoutout to the ROCm Spack team for staying diligent on keeping ROCm Spack packages up-to-date.)

I am using a standalone Python script to generate this for now. If you're interested and you have a specific directory/repo in mind where I might contribute this, let me know.



---

### 评论 #9 — garrettbyrd (2025-04-15T18:23:09Z)

@saadrahim @nartmada Just circling back on this. Now that [this blog post](https://rocm.blogs.amd.com/software-tools-optimization/spack-installation/README.html#rocm-component-dependencies) is up and we've demonstrated that you can generate this kind of graphic using a package manager (in this case Spack, but could be generalized to apt, dnf, etc), are you interested in utilizing the Python script that was used for this?

I know there's a dependency matrix [here](https://github.com/ROCm/ROCm/blob/develop/tools/rocm-build/ROCm.mk), but thought I would again offer this as an alternative.

---
