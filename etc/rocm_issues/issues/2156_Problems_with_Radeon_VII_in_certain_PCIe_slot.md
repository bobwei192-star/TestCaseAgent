# Problems with Radeon VII in certain PCIe slot

> **Issue #2156**
> **状态**: closed
> **创建时间**: 2023-05-21T15:26:09Z
> **更新时间**: 2024-08-01T14:20:15Z
> **关闭时间**: 2024-08-01T14:20:15Z
> **作者**: nadvornik
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2156

## 描述

I have Radeon VII, Asus PRIME X570-P  board and AMD Ryzen 7 3700X.

When the GPU is in the first PCIe slot (x16, connected to CPU), everything works fine.

When the GPU is in the second PCIe slot (x4, connected to chipset), it does not work correctly. Stable diffusion fails with message "A tensor with all NaNs was produced in Unet".
It might be the same issue as https://github.com/RadeonOpenCompute/ROCm/issues/2055

I have minimized the pytorch reproducer to this:
```
import torch
device = torch.device("cuda" if (torch.cuda.is_available()) else "cpu")
data = torch.rand(3,3).float()
print('Initial Data nan', torch.any(torch.isnan(data)))
data = data.to(device)
print('Device Data nan', torch.any(torch.isnan(data)))
data = data.to("cpu")
print('CPU Data nan', torch.any(torch.isnan(data)))
```
It prints
```
Initial Data nan tensor(False)
Device Data nan tensor(True, device='cuda:0')
CPU Data nan tensor(False)
```

I haven't noticed any problems outside of pytorch, the rvs testsuite does not report  anything suspicious.

In the first PCIe slot the GPU works fine even with HSA_ENABLE_SDMA=0.

Tested on openSUSE Leap 15.4,  kernel 5.14.21-150400.24.60-default, amdgpu-dkms 1:6.0.5.50500-1581431,
the official torch-2.0.1+rocm5.4.2 (the same result with self-compiled torch against ROCm 5.5).

If I understand the documentation correctly, Radeon VII is supported, does not need  PCIe atomics and thus it should work
in any PCIe slot.



---

## 评论 (3 条)

### 评论 #1 — skein12 (2023-05-29T03:38:31Z)

would like to add to this, same exact issue but WX 9100

kernel: 5.19.0-42-generic
python: 3.10.6
ryzen 5500
linux ubuntu 22.04
torch 2.0.1+rocm5.5

---

### 评论 #2 — wxianxin (2023-06-05T05:20:06Z)

Add one more case:

Error seems to be that matrix operation doesn’t work. The results are very small identical numbers in all the cells regardless of the input and operation 
. (Same GPU tested working fine on full x16 slot on a different PC (i5 13600k + b660)

GPU: 6800xt
CPU Intel i5 1140G7
torch 2.0.1 + ROCM 5.4.2 (from pytorch.org installation matrix)

I am using a thunderbolt eGPU, which means the GPU also gets on PCIE 3.0 x4 bandwidth, like @nadvornik 

---

### 评论 #3 — ppanchad-amd (2024-05-13T17:35:47Z)

@nadvornik Apologies for the lack of response. Do you still need assistance with this ticket? If not, please close the ticket. Thanks!

---
