# Low bandwidth with xGMI/MI100/CPU7003

> **Issue #2499**
> **状态**: closed
> **创建时间**: 2023-09-25T20:03:36Z
> **更新时间**: 2024-07-19T18:28:57Z
> **关闭时间**: 2024-07-19T18:28:56Z
> **作者**: LukaOo
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2499

## 描述

Hi. 
 We try to build HPC server for deep learning based on AMD solution with 8xMI100 and AMD CPU 7003. There are two hives and all GPU inside single hive connected by Infinity Fabric. We have **ROCm 5.6** installed. It seems server has very poore bandwidth performance.
Here is output of  ./rocm_bandwidth_test command:

![image](https://github.com/RadeonOpenCompute/ROCm/assets/18306546/75968856-7b94-4bfc-ab48-7cfbc6820530)

 Screenshot above shows:
1. Bidirectional speed between two GPU's in same hive is about 70GB/s, but according to official documentation must be about 92GB/s.
2. Bidirectional transfer speed  from GPU and CPU is about 50GB/s but should be about 64GB/s
3. Bidirectional transfer speed between CPU form one NUMA to GPU from second NUMA  is about  28GB/s  but it is significaly less then expected.

We followed with this Guide https://rocm.docs.amd.com/en/docs-5.1.3/how_to/tuning_guides/mi100.html to setup.

**Platform:**
![image](https://github.com/RadeonOpenCompute/ROCm/assets/18306546/64dc3816-adb4-42de-baa6-0807cd4f5b73)

**System:**
Alma Linux 9
ROCm 5.6

---

## 评论 (3 条)

### 评论 #1 — vstempen (2024-01-23T19:39:14Z)

The official numbers are calculated based on XGMI peak rate and M100 XGMI link configuration. When compared to real measurements, real world efficiency loss must be taken in account, due to CRC overhead, protocol, token stall, etc. Considering the efficiency loss, the real rate should be approximately 89% of Unidirectional and 71% for Bidirectional traffic on MI100, which uses XGMI gen3. 

---

### 评论 #2 — ppanchad-amd (2024-05-14T20:02:50Z)

@LukaOo Has your issue been resolved? If so, please close the ticket. Thanks!

---

### 评论 #3 — ppanchad-amd (2024-07-19T18:28:56Z)

@LukaOo Closing ticket since there is no response for a while. If you still require assistance or believe this issue needs to remain open, please re-open the ticket. Thanks! 



---
