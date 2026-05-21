# [FAQ] what is CUDA GPU direct nvme equivalent thing in ROCm

> **Issue #2251**
> **状态**: closed
> **创建时间**: 2023-06-18T15:05:21Z
> **更新时间**: 2024-07-20T14:56:08Z
> **关闭时间**: 2024-07-19T19:53:26Z
> **作者**: gaowayne
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2251

## 描述

two questions on ROCm interface with storage?
1. if ROCm has similar thing like CUDA GPU direct NVMe?
2. if ROCm can connect NVMeOF now?



---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2024-05-13T19:37:40Z)

@gaowayne Apologies for the delayed response.

1: Currently ROCm does not have a GPUDirect equivalent. 

2: RDMA is supported by ROCm, but there is no NVMEOF-specific code in ROCm. They’d have to check with the network driver (Mellanox, etc) to enable it.


---

### 评论 #2 — ppanchad-amd (2024-06-18T19:49:30Z)

@gaowayne Can we close this ticket? Thanks!

---

### 评论 #3 — ppanchad-amd (2024-07-19T19:53:26Z)

@gaowayne Closing ticket since there is no response for a while. If you still require assistance, please re-open the ticket. Thanks! 


---

### 评论 #4 — gaowayne (2024-07-20T14:56:08Z)

thank you so much

---
