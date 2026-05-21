# [Issue]: OOM ERROR on Pytorch Windows preview

> **Issue #5542**
> **状态**: closed
> **创建时间**: 2025-10-19T12:38:00Z
> **更新时间**: 2025-12-17T19:14:57Z
> **关闭时间**: 2025-12-17T19:14:57Z
> **作者**: kjhanjee
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5542

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

[###](

<img width="2240" height="1329" alt="Image" src="https://github.com/user-attachments/assets/758c4bcd-e805-4d59-9c82-5c898f49a9be" />

) Problem Description

Frequent OOM errors on using Pytorch for Windows preview. Below are my system specifications:
```
(Get-WmiObject Win32_OperatingSystem).Version: 10.0.26200
(Get-WmiObject win32_Processor).Name: AMD Ryzen 5 7600X 6-Core Processor
(Get-WmiObject win32_VideoController).Name: AMD Radeon RX 7900 XTX
```

```
HIP SDK Libraries: 6.4.0 & 6.2.0
Pytorch Wheels version: 2.8.0a0+gitfc14c65
```

Please let me know if this is to be expected and if there is any other information required from end.

### Operating System

Windows 11

### CPU

AMD Ryzen 5 7600X

### GPU

AMD Radeon 7900XTX

### ROCm Version

6.2

### ROCm Component

HIP

### Steps to Reproduce

Run  the below code:
```python
import torch

class MODEL(torch.nn.Module):
    def __init__(self, in_size=2048, out_size=50000, device="cuda:0"):
        super().__init__()
        self.linear = torch.nn.Linear(in_features=in_size, out_features=out_size, device = device)
        self.layer_norm = torch.nn.LayerNorm(out_size, device = device)
        
    def forward(self, input, mask):
        input += mask
        out = self.linear(input)
        out = self.layer_norm(out)
        print(out.min().item(), out.max().item())
        return out
    
      
        
model = MODEL().half()
for m in model.modules():
    if isinstance(m, (torch.nn.Linear)):
        torch.nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
        if m.bias is not None:
            torch.nn.init.zeros_(m.bias)
            
loss = torch.nn.CrossEntropyLoss(label_smoothing=0.1, ignore_index=3)
optimizer = optimizer = torch.optim.AdamW(model.parameters(), 
                                lr=3e-4,
                                betas=(0.9, 0.999),    # defaults
                                eps=1e-6,              # numerical stability
                                weight_decay=1e-8
                                )
# scaler = torch.amp.GradScaler(device="cuda:0")

for i in range(1,11):
    print(f"Step {i}")
    input = torch.randn(size=(2,8192,2048), device="cuda:0").half()
    target = torch.randint(low = 0, high=50000, size=(2,8192), device="cuda:0", dtype = torch.long)
    mask = (input != 3).to("cuda:0").half()
    # with torch.autocast(device_type="cuda", dtype = torch.float16):
    #     with torch.set_grad_enabled(True):
    out = model.forward(input, mask).to(dtype=torch.float32)
    loss_val = loss(out.view(out.shape[0]*out.shape[1], out.shape[2]), target.view(target.shape[0]*target.shape[1]))
    print(loss_val.item())
    loss_val.backward()
    for name, param in model.named_parameters():
        if param.grad is not None:
            if torch.isnan(param.grad).any() or torch.isinf(param.grad).any():
                print(f"⚠️ NaN/Inf detected in gradient of {name}")
                # Optional: sanitize instead of skipping
                # param.grad = torch.nan_to_num(param.grad, nan=0.0, posinf=1e4, neginf=-1e4)

    optimizer.step()
```
Even a tiny Model like this takes upwards of 17 Gigs of VRAM while training.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — huanrwan-amd (2025-10-20T21:46:28Z)

Hi @kjhanjee, thanks for posting questions. Have you tried to upgrade the ROCm to 7.0?
I have the same program running under rocm7.0+7900xtx under ubuntu22 using
`       allocated = torch.cuda.memory_allocated() / 1024**3  # GB`
`       reserved = torch.cuda.memory_reserved() / 1024**3   # GB`
had:
`VRAM - Allocated: 4.05GB, Reserved: 18.89GB, Total: 23.98GB`

---

### 评论 #2 — kjhanjee (2025-10-20T21:53:28Z)

Hi,

Thanks for responding. I cannot do 7.0 since I am on windows. The windows preview only supports 6.4. i had the same issues earlier with 6.4 on Ubuntu as well. Though this seems a bit odd since the base BERT model has more params and layers than this. I am not sure but I think this should be much lesser at around 8-9 Gigs rather than 18-19 Gigs.
> Hi @kjhanjee, thanks for posting questions. Have you tried to upgrade the ROCm to 7.0?
> I have the same program running under rocm7.0+7900xtx under ubuntu22 using
> `       allocated = torch.cuda.memory_allocated() / 1024**3  # GB`
> `       reserved = torch.cuda.memory_reserved() / 1024**3   # GB`
> had:
> `VRAM - Allocated: 4.05GB, Reserved: 18.89GB, Total: 23.98GB`



---

### 评论 #3 — huanrwan-amd (2025-10-21T15:04:15Z)

Hi @kjhanjee , thanks for the updates. Since this is a preview version for windows, can you please use the above two line to check the allocated/reserved gpu memory that I can check with internal team?
`allocated = torch.cuda.memory_allocated() / 1024**3  # GB`
`reserved = torch.cuda.memory_reserved() / 1024**3   # GB`

---

### 评论 #4 — kjhanjee (2025-10-23T16:58:36Z)

> Hi [@kjhanjee](https://github.com/kjhanjee) , thanks for the updates. Since this is a preview version for windows, can you please use the above two line to check the allocated/reserved gpu memory that I can check with internal team? `allocated = torch.cuda.memory_allocated() / 1024**3 # GB` `reserved = torch.cuda.memory_reserved() / 1024**3 # GB`

I am getting the below outputs from these commands:

Step 1
-5.74609375 5.890625
11.319807052612305
Allocated: 3.973839282989502
Reserved: 15.841796875

Step 2
-5.4140625 11.0390625
12.065423965454102
Allocated: 3.973839282989502
Reserved: 15.841796875

Step 3
-65.3125 6.109375
11.489068031311035
Allocated: 3.973839282989502
Reserved: 15.841796875

Step 4
-97.3125 5.57421875
11.389830589294434
Allocated: 3.973839282989502
Reserved: 15.841796875

Step 5
-113.375 5.15625
11.363329887390137
Allocated: 3.973839282989502
Reserved: 15.841796875

Step 6
-122.875 4.8984375
11.373958587646484
Allocated: 3.973839282989502
Reserved: 15.841796875

Step 7
-129.0 4.6796875
11.382454872131348
Allocated: 3.973839282989502
Reserved: 15.841796875

Step 8
-133.375 4.51171875
11.415124893188477
Allocated: 3.973839282989502
Reserved: 15.841796875

Step 9
-136.5 4.4609375
11.444831848144531
Allocated: 3.973839282989502
Reserved: 15.841796875

Step 10
-138.875 4.5078125
11.47266674041748
Allocated: 3.973839282989502
Reserved: 15.841796875

---

### 评论 #5 — huanrwan-amd (2025-10-23T19:07:49Z)

@kjhanjee Thanks for posting the result. Our results seems the same. The "Allocated: 3.97GB" is correct with theoretical value. 

---

### 评论 #6 — kjhanjee (2025-10-23T19:11:54Z)

No issues and thanks for confirming but then why is the reserved memory so high nearly 5x?
> @kjhanjee Thanks for posting the result. Our results seems the same. The "Allocated: 3.97GB" is correct with theoretical value. 



---

### 评论 #7 — huanrwan-amd (2025-10-23T19:50:31Z)

@kjhanjee Usually it is designed for performance. There are pytorch documentation on memory management that you can search for.

---

### 评论 #8 — huanrwan-amd (2025-12-17T19:14:57Z)

close as answered. 

---
