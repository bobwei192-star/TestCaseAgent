# Reduce RocM Image size

> **Issue #3935**
> **状态**: closed
> **创建时间**: 2024-10-22T23:50:21Z
> **更新时间**: 2024-11-13T22:45:04Z
> **关闭时间**: 2024-10-31T18:57:14Z
> **作者**: michaelfeil
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/3935

## 描述

Note: If I am raising this issue at the wrong place, please forward it to the correct location

https://hub.docker.com/r/rocm/pytorch currently is a ~32 GB decompressed container size.
Most build systems, e.g. github actions only have 25/29GB of total disk space available for the build




---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2024-10-31T18:57:14Z)

Hi @michaelfeil, we are aware of this issue and there are ongoing efforts to minimize the ROCm docker image sizes. The main cause of this is the ROCm installation itself which is under scrutiny. 

A workaround would be to use multi-stage docker build with only the specific ROCm components required for your usecase. The rocm/pytorch image also includes a conda environment (~15% of it's total size) which can be avoided in a custom build. I will close this issue out for now as this is being tracked internally by the respective teams. Please feel free to leave a comment with any further questions.

---

### 评论 #2 — michaelfeil (2024-11-13T22:45:03Z)

@harkgill-amd I found that there is e.g. a 8.12GB folder called `/var/lib/jenkins/pytorch`

![image](https://github.com/user-attachments/assets/863084e8-0078-4439-af5d-0a1ed3225958)


---
