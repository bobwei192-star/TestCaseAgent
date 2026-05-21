# custom accelerator using rocm.

> **Issue #3014**
> **状态**: closed
> **创建时间**: 2024-04-15T20:51:24Z
> **更新时间**: 2024-04-16T16:01:30Z
> **关闭时间**: 2024-04-16T16:01:30Z
> **作者**: notlober
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/3014

## 描述

can i build a custom accelerator that support rocm api to have rocm as a bridge between my hardware and the target program? will there be any problems like license or law issues? just asking.

---

## 评论 (2 条)

### 评论 #1 — notlober (2024-04-15T21:03:16Z)

like for example i want to use pytorch with my custom hardware, and without writing too many code, like just modifying my custom drivers of my hardware for rocm api calls, i can use pytorch, this is not a problem for now, but if i want to go commercial with same setup, will there be any problems?

---

### 评论 #2 — IMbackK (2024-04-16T15:28:43Z)

you can def implement the hip api with no issue, its an open standart, and people have done so: https://github.com/illuhad/hipCPU hip itself is also quite small and very fesable to implement.

However to make something like pytorch work is a totally different animal and is _hard_ and a huge tonne of work as it depends on highly complex libiaries like rocBlas and miopen that are agressively machine specific to amd gpus, you will have write new, api compatable versions of those, an impossible undertakeing if your not a large team

---
