# [Issue]: MIOpen 7.0 hipErrorInvalidValue on 1x1 Conv2d with non-contiguous inputs (GEMM rewrite)

> **Issue #5694**
> **状态**: closed
> **创建时间**: 2025-11-25T17:03:03Z
> **更新时间**: 2025-12-02T16:48:42Z
> **关闭时间**: 2025-12-02T16:47:49Z
> **作者**: EmilienM
> **标签**: AMD Instinct MI300X, status: triage, project: miopen
> **URL**: https://github.com/ROCm/ROCm/issues/5694

## 标签

- **AMD Instinct MI300X** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)
- **project: miopen** (颜色: #962619)

## 负责人

- tcgu-amd

## 描述

### Problem Description

### **Description**

In ROCm 7, 1x1 convolutions fail with `RuntimeError: HIP error: invalid argument` when the input tensor is non-contiguous (e.g., resulting from slicing or permuting). This appears to be a regression caused by the architectural change noted in the ROCm 7.0 changelog: *"1x1 convolutions are now rewritten to GEMMs."*

Previous versions of ROCm (5.x/6.x) handled non-contiguous inputs for 1x1 convolutions correctly, likely via a Direct solver fallback. The new GEMM-based path in MIOpen 7.0 appears to enforce strict memory layout constraints (e.g., leading dimension strides) without the PyTorch integration layer automatically handling the necessary data repacking.

This breaks common computer vision architectures (e.g., `timm` models using `Attention2d`, `ConvNeXt`, `MaxxVit`) where strided views are passed directly to projection layers.

See https://github.com/huggingface/pytorch-image-models/issues/2613 for more context.

### **Environment**

  * **Hardware:** MI300X
  * **OS:** Linux (RHEL 9.6)
  * **ROCm Version:** 7.0.51831-7c9236b16
  * **PyTorch Version:** 2.9 from https://github.com/ROCm/pytorch
  * **Library:** MIOpen (via `ATen`)


### **Stack Trace**

RuntimeError: HIP error: invalid argument
...
File "torch/nn/modules/conv.py", line 456, in \_conv\_forward
return F.conv2d(input, weight, bias, self.stride,
RuntimeError: HIP error: invalid argument
*(Note: Use `AMD_SERIALIZE_KERNEL=3` to confirm the synchronous failure at launch)*

### **Analysis**

The ROCm 7.0 Release Notes state:

> *"1x1 convolutions are now rewritten to GEMMs."* [1]

It appears that the `GEMM` solver selected by MIOpen for this operation requires the input tensor to be contiguous (or satisfy specific BLAS stride constraints). When `ATen` passes a strided tensor descriptor to MIOpen, the API call is rejected with `hipErrorInvalidValue`.

**Expected Behavior:**
The framework integration (or the library itself) should detect the non-contiguous memory layout and either:

1.  Fallback to a generic convolution solver that supports strided inputs (like `Direct` solvers in previous versions).
2.  Or, implicit repacking should occur before dispatching to the strict `GEMM` solver.

### **References**

[1] ROCm 7.0 Changelog: [https://rocm.docs.amd.com/en/latest/release/changelog.html](https://rocm.docs.amd.com/en/latest/release/changelog.html)

### Operating System

Red Hat Enterprise Linux 9.6

### CPU

amd

### GPU

MI300X

### ROCm Version

ROCm 7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

### **Minimal Reproduction Script**

The following script succeeds on ROCm 6.x and CUDA, but fails on ROCm 7.0:

```python
import torch
import torch.nn as nn

def test_1x1_conv_contiguity():
    if not torch.cuda.is_available():
        print("Skipping: CUDA/ROCm not available")
        return

    device = torch.device("cuda")
    print(f"Running on: {torch.cuda.get_device_name(device)}")

    # 1. Setup a standard NCHW tensor
    # Shape: (Batch=1, Channels=64, H=32, W=48)
    x_contiguous = torch.randn(1, 64, 32, 48, device=device)

    # 2. Define a 1x1 Convolution
    # ROCm 7.0 MIOpen rewrites this to a GEMM operation
    conv = nn.Conv2d(64, 64, kernel_size=1).to(device)

    # 3. Create a non-contiguous view
    # Slicing creates a valid tensor with non-default strides
    # This simulates operations found in Attention2d (slice/permute/view)
    x_non_contiguous = x_contiguous[:, :, ::2, ::2] 
    
    print(f"Input Shape: {x_non_contiguous.shape}")
    print(f"Input Is Contiguous? {x_non_contiguous.is_contiguous()}")

    try:
        # Failure occurs here on ROCm 7.0
        out = conv(x_non_contiguous)
        print("PASS: Convolution successful.")
    except RuntimeError as e:
        print("\nFAIL: Convolution crashed.")
        print(f"Error: {e}")
        
        # Verify workaround
        print("\nAttempting workaround (.contiguous())...")
        out_fixed = conv(x_non_contiguous.contiguous())
        print("PASS: Workaround successful.")

if __name__ == "__main__":
    test_1x1_conv_contiguity()
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — rwightman (2025-11-25T17:55:42Z)

As maintainer of `timm`, worth pointing out @EmilienM provided a 'fix' for a specific model family by adding .contiguous() prior to the 1x1 conv. While it works in this scenario, there would be A LOT of other models in timm impacted by this and it's not reasonable to require modelling code to change. 

---

### 评论 #2 — tcgu-amd (2025-11-26T15:47:55Z)

Hi @rwightman @EmilienM, thanks for reaching out! Will look into this shortly.

---

### 评论 #3 — BradPepersAMD (2025-11-26T17:11:31Z)

Thanks for posting this @EmilienM!  I head up the MIOpen group and will get this checked out ASAP.


---

### 评论 #4 — BradPepersAMD (2025-11-26T18:26:14Z)

Heads up I tested this with a very recent internal mainline build of what will be ROCm 7.2 and pytorch 2.9 and I don't see the error.  Output is just:

Running on: AMD Radeon Graphics
Input Shape: torch.Size([1, 64, 16, 24])
Input Is Contiguous? False
PASS: Convolution successful.

I'm going back in time to try and figure out when we fixed this.

---

### 评论 #5 — stmcgovern (2025-11-26T18:31:52Z)

Hi @BradPepersAMD, I think that the issue is fixed in pytorch with the following context:

Apparently this problem in pytorch's wrapper for MIOpen was addressed on Sept 3, 2025 (https://github.com/pytorch/pytorch/pull/161687) . That commit (99f356fa58c ) is in 2.9.0. 
Two follow on commits related were added after the 2.9 branch cut Sept 9 (https://dev-discuss.pytorch.org/t/pytorch-release-2-9-branch-cut-is-complete/3229)
     Batchnorm fix (Sept 11)        (d65ffdef3d3): ✅ YES
     Conv ReLU fix (Sept 15)        (0def79fdd9c): ✅ YES

 0def79fdd9c is likely what will resolve this. 

---

### 评论 #6 — BradPepersAMD (2025-11-26T18:34:45Z)

yeah we did some rework on the pytorch/MIOpen integration around that time that fixed some issues with contiguous tensors and it's what I've been suspecting as the fix though it didn't fit the ROCm 7.0 release note about 1x1 convs but I think that isn't related since that "1x1 convolutions are now rewritten to GEMMs" is part of the MIGraphX release notes so unrelated to MIOpen.

that 99f356fa58c work on the pytorch wrappers should be the fix but wouldn't hurt to grab the next couple you found!

---

### 评论 #7 — tcgu-amd (2025-12-02T16:47:49Z)

@EmilienM, just verified that the problem indeed does not exist with Pytorch `'2.10.0a0+rocm7.10.0a20251015'`

<img width="429" height="116" alt="Image" src="https://github.com/user-attachments/assets/2055ccf2-5740-4bc4-8676-61deaae76520" />

You can install it from TheRock releases here https://github.com/ROCm/TheRock/blob/main/RELEASES.md. 

This issue will be closed. Thanks!


---
