# [Issue]: `roc-obj-ls` and `perl` modules broken in `rocm/dev-ubuntu-24.04:6.4`

> **Issue #4629**
> **状态**: closed
> **创建时间**: 2025-04-15T15:26:19Z
> **更新时间**: 2025-04-24T19:10:08Z
> **关闭时间**: 2025-04-24T19:10:08Z
> **作者**: maartenarnst
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4629

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

The script `roc-obj-ls` and perl modules are broken in `rocm/dev-ubuntu-24.04:6.4`.

Calling `roc-obj-ls` results in an error message like:

```
Can't locate File/Which.pm in @INC (you may need to install the File::Which module) (@INC entries checked: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.38.2 /usr/local/share/perl/5.38.2 /usr/lib/x86_64-linux-gnu/perl5/5.38 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl-base /usr/lib/x86_64-linux-gnu/perl/5.38 /usr/share/perl/5.38 /usr/local/lib/site_perl) at /usr/bin/roc-obj-ls line 25.
1.404 BEGIN failed--compilation aborted at /usr/bin/roc-obj-ls line 25.
```

This is a reproducer:

<details>
<summary>
Dockerfile
</summary>

```
FROM rocm/dev-ubuntu-24.04:6.4

COPY <<EOF saxpy.cpp
#include <hip/hip_runtime.h>

__global__ void saxpy_kernel(const float a, const float* d_x, float* d_y, const unsigned int size)
{
    const unsigned int global_idx = blockIdx.x * blockDim.x + threadIdx.x;

    if(global_idx < size) {
        d_y[global_idx] = a * d_x[global_idx] + d_y[global_idx];
    }
}
EOF

RUN <<EOF
    hipcc --offload-arch=gfx906 -c saxpy.cpp -o saxpy.o

    roc-obj-ls -v saxpy.o
EOF
```
</details>

Running this file with `docker buildx build -f Dockerfile .` produces the above mentioned error message.

Issue observed while upgrading our code base to rocm 6.4 with @romintomasetti.

### Operating System

Ubuntu 24.04

### CPU

AND Ryzen 5950x

### GPU

Radeon Pro VII

### ROCm Version

ROCm 6.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2025-04-15T18:36:54Z)

Hi @maartenarnst, thanks for the report and repro steps. I am seeing the same error on my end when running with the `rocm/dev-ubuntu-24.04:6.4` image, though the `roc-obj-ls` works fine on a baremetal installation of ROCm 6.4, see below. 
```
roc-obj-ls saxpy.o
Warning:  This tool is being DEPRECATED.  Similar funcitonality is provided in the rocm-llvm package with llvm-objdump.
1       host-x86_64-unknown-linux--                                         file://saxpy.o#offset=8192&size=0
1       hipv4-amdgcn-amd-amdhsa--gfx906                                     file://saxpy.o#offset=8192&size=4168
```
As highlighted in the output, the ROCm Object Tooling tools are deprecated as of ROCm 6.4 and it's now recommended to use the `llvm-objdump` tool in there place. You can find more information on the deprecation [here](https://rocm.docs.amd.com/en/latest/about/release-notes.html#changes-to-rocm-object-tooling). I'll continue to look into the errors on the 6.4 docker image but in the meantime, give the `llvm-objdump` tool a try and let me know if you have any questions.

---

### 评论 #2 — harkgill-amd (2025-04-15T19:02:58Z)

With the release of ROCm 6.4, `libfile-which-perl` and `liburi-perl` are no longer depended on by `hip-base` and as a result, these packages are not installed during the docker build which utilizes `--no-install-recommends`. 

You can resolve the errors by installing these packages though, it'd be best to switch to `llvm-objdump`.

---

### 评论 #3 — maartenarnst (2025-04-16T10:08:26Z)

OK. Thanks for taking a look and for pointing to `llvm-objdump`. 

We've just tried using `llvm-objdump`. We can indeed use it to extract the code objects. However, it seems it does not list the code objects. In particular, when we use `llvm-objdump --offloading --arch-name=gfx906 saxpy.o` in our reproducer,  the file `saxpy.o:0.hipv4-amdgcn-amd-amdhsa--gfx906` is dumped, but the output to `stdout` is only `saxpy.o:        file format elf64-x86-64`. This behavior appears inconsistent with what may have been expected from the "help" which says "--offloading Display the content of the offloading section". 

---

### 评论 #4 — harkgill-amd (2025-04-16T14:31:39Z)

Thanks for giving it a try. Just spoke with the developer leading the change in tooling and confirmed, `llvm-objdump` is currently limited to code object extraction similar to the existing `roc-obj` tool The functionality to list code objects will be introduced in a future release, apologies for the mix-up there. 

For now, please continue to use `roc-obj-ls` by installing the `libfile-which-perl` and `liburi-perl` packages on top of the 6.4 base image. 

---

### 评论 #5 — harkgill-amd (2025-04-24T19:10:06Z)

Closing this issue out. Feel free to leave a comment if you have any further questions on which tooling to use.

---
