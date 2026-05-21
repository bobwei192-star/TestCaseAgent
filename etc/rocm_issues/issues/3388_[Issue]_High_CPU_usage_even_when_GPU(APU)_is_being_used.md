# [Issue]: High CPU usage even when GPU(APU) is being used

> **Issue #3388**
> **状态**: closed
> **创建时间**: 2024-07-03T05:32:04Z
> **更新时间**: 2025-01-29T21:57:24Z
> **关闭时间**: 2025-01-29T21:57:23Z
> **作者**: jin9012
> **标签**: Under Investigation, AMD Radeon VII, ROCm 5.7.0
> **URL**: https://github.com/ROCm/ROCm/issues/3388

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon VII** (颜色: #ededed)
- **ROCm 5.7.0** (颜色: #ededed)

## 描述

### Problem Description

I'm using Ryzen 7530u(APU), Ubuntu 24.04, Linux kernel 6.10-rc4, ROCm 5.7 
(I followed this instruction : https://medium.vaningelgem.be/installing-pytorch-rocm-on-ubuntu-mantic-23-10-3da0f84c65d9)

I've tried MNIST with transformers and  I get the same results as Google colab. 
The problem I have is that the CPU usage is always 100% when training. I understand its GPU usage gets high, but is it normal to keep 100% CPU usage the whole time? When I used directml-torch on Windows, it used CPU(50~70%) when there were some functions that the library didn't support yet. I wonder if it's a similar case or there are other reasons, hopefully that can be fixed! 


### Operating System

Ubuntu 24.04

### CPU

7530u

### GPU

AMD Radeon VII

### ROCm Version

ROCm 5.7.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — ppanchad-amd (2024-07-03T13:54:24Z)

@jin9012 Ubuntu 24.04 is not currently supported yet.  Also, can you please try if it's reproducible with the latest ROCm 6.1.2? Thanks!

---

### 评论 #2 — jin9012 (2024-07-04T06:36:17Z)

> @jin9012 Ubuntu 24.04 is not currently supported yet. Also, can you please try if it's reproducible with the latest ROCm 6.1.2? Thanks!

I have another laptop with 4500u apu. I just installed Ubuntu 22.04 and ROCm 6.1.2 on it and the same issue happens. Do you have any advice? 

![20240704_152353](https://github.com/ROCm/ROCm/assets/136994159/8aa116b2-517d-4351-b519-759aecaa9bee)



---

### 评论 #3 — jamesxu2 (2024-07-04T14:15:03Z)

Hi @jin9012, 

Unfortunately, [ROCm doesn't officially support APUs](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html). You may be seeing this issue because your APU is not detected as a valid ROCm device (i.e. if you query ```torch.cuda.is_available()```) and may not be able to accelerate your ML workload.

However, if you provide more information on:
- What exactly you're running (i.e. ML framework, program source code if possible)
- the output of  ```/opt/rocm/bin/rocminfo --support```

I may be able to advise further. 


---

### 评论 #4 — jin9012 (2024-07-05T02:14:09Z)

> Hi @jin9012,
> 
> Unfortunately, [ROCm doesn't officially support APUs](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html). You may be seeing this issue because your APU is not detected as a valid ROCm device (i.e. if you query `torch.cuda.is_available()`) and may not be able to accelerate your ML workload.
> 
> However, if you provide more information on:
> 
> * What exactly you're running (i.e. ML framework, program source code if possible)
> * the output of  `/opt/rocm/bin/rocminfo --support`
> 
> I may be able to advise further.

Thank you for the comment. 
When I query ```torch.cuda.is_available()```, it says ```True```. I'm not sure if it still uses CPU.
This is the output of ```/opt/rocm/bin/rocminfo --support``` on the 7530u laptop and the code I ran.

```
[37mROCk module version 6.7.0 is loaded[0m
=====================
HSA System Attributes
=====================
Runtime Version:         1.13
Runtime Ext Version:     1.4
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 5 7530U with Radeon Graphics
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 5 7530U with Radeon Graphics
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   4546
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            12
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    7448828(0x71a8fc) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    7448828(0x71a8fc) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    7448828(0x71a8fc) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx90c
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon Graphics
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      1024(0x400) KB
  Chip ID:                 5607(0x15e7)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2000
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            7
  SIMDs per CU:            4
  Shader Engines:          1
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          64(0x40)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        40(0x28)
  Max Work-item Per CU:    2560(0xa00)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 471
  SDMA engine uCode::      40
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    524288(0x80000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    524288(0x80000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx90c:xnack-
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***
```

```
## FROM : https://comsci.blog/posts/vit

from os import putenv
putenv("HSA_OVERRIDE_GFX_VERSION", "9.0.0")

import torch
import torch.nn.functional as F
from torch import nn
from torchvision import datasets, transforms
from datetime import datetime

class ViT(nn.Module):
    def __init__(self, img_width, img_channels, patch_size, d_model, num_heads, num_layers, num_classes, ff_dim):
        super().__init__()

        self.patch_size = patch_size

        # given 7x7 flattened patch, map it into an embedding
        self.patch_embedding = nn.Linear(img_channels * patch_size * patch_size, d_model)

        # cls_token we are using we will be concatenating
        self.cls_token = nn.Parameter(torch.randn(1, 1, d_model))

        # (1, 4*4 + 1, 64)
        # + 1 because we add cls tokens
        self.position_embedding = nn.Parameter(
            torch.rand(1, (img_width // patch_size) * (img_width // patch_size) + 1, d_model)
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model, nhead=num_heads, dim_feedforward=ff_dim, batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        # mapping 64 to 10 at the end
        self.fc = nn.Linear(d_model, num_classes)

    def forward(self, x):
        N, C, H, W = x.shape

        # we divide the image into 4 different 7x7 patches, and then flatten those patches
        # img shape will be 4*4 x 7*7
        x = x.unfold(2, self.patch_size, self.patch_size).unfold(3, self.patch_size, self.patch_size)
        x = x.contiguous().view(N, C, -1, self.patch_size, self.patch_size)
        x = x.permute(0, 2, 3, 4, 1).contiguous().view(N, -1, C * self.patch_size * self.patch_size)

        # each 7*7 flatten patch will be embedded to 64 dim vector
        x = self.patch_embedding(x)

        # cls tokens concatenated after repeating it for the batch
        cls_tokens = self.cls_token.repeat(N, 1, 1)
        x = torch.cat((cls_tokens, x), dim=1)

        # learnable position embeddings added
        x = x + self.position_embedding

        # transformer takes 17x64 tensor, like it is a sequence with 17 words (17 because 4*4 + 1 from cls)
        x = self.transformer_encoder(x)

        # only taking the transformed output of the cls token
        x = x[:, 0]

        # mapping to number of classes
        x = self.fc(x)

        return x


batch_size = 128
lr = 3e-4
num_epochs = 15

img_width = 28
img_channels = 1
num_classes = 100
patch_size = 7
embedding_dim = 64
ff_dim = 2048
num_heads = 8
num_layers = 3
weight_decay = 1e-4

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST("./data", train=True, download=True, transform=transforms.ToTensor()),
    batch_size=batch_size,
    shuffle=True,
)

test_loader = torch.utils.data.DataLoader(
    datasets.MNIST("./data", train=False, download=True, transform=transforms.ToTensor()),
    batch_size=batch_size,
    shuffle=True,
)



device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"{device=}")

model = ViT(
    img_width=img_width,
    img_channels=img_channels,
    patch_size=patch_size,
    d_model=embedding_dim,
    num_heads=num_heads,
    num_layers=num_layers,
    num_classes=num_classes,
    ff_dim=ff_dim,
).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

for epoch in range(num_epochs):
    losses = []
    total_train = 0
    correct_train = 0

    model.train()
    for img, label in train_loader:
        img = img.to(device)
        label = label.to(device)

        pred = model(img)
        loss = F.cross_entropy(pred, label)

        pred_class = torch.argmax(pred, dim=1)
        correct_train += (pred_class == label).sum().item()
        total_train += pred.shape[0]

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        losses.append(loss.item())

    model.eval()
    total = 0
    correct = 0
    with torch.no_grad():
        for img, label in test_loader:
            img = img.to(device)
            pred = torch.argmax(model(img), dim=1).cpu()

            correct += (pred == label).sum().item()
            total += pred.shape[0]

    print(f"{epoch}:{loss.data}, {correct / total}")
```

When I set ROCR_VISIBLE_DEVICES as 1, it uses all the cpu processes(shows more than 500% cpu usage in this case)

---

### 评论 #5 — jamesxu2 (2024-07-08T15:02:38Z)

Hi @jin9012 ,

Thanks for the info. I've tried running your program on my system as well (CPU - 7950X, GPU - RX7900XT) and I also observe 100% CPU usage. I don't think that full utilization of your CPU is necessarily a problem though, and actually expected as the CPU _is_ being loaded by your program - not all compute happens on the GPU.

Regarding this comment:
> When I query torch.cuda.is_available(), it says True. I'm not sure if it still uses CPU.

You can test this by disabling the GPU - Force ```device = 'cpu'``` or ```export CUDA_VISIBLE_DEVICES=""``` and assess if your program takes significantly longer to run.

---

### 评论 #6 — jamesxu2 (2024-07-17T13:37:51Z)

Hello @jin9012, do you have an update?

---

### 评论 #7 — harkgill-amd (2025-01-29T21:57:23Z)

Closing this issue out due to lack of response. @jin9012, if you have any updates on the tests prescribed by @jamesxu2, please leave a comment and I will re-open this issue.

---
