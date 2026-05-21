# Is there a difference between "Numa Node" and "Numa Affinity" in rocm-smi --showtoponuma?

> **Issue #4740**
> **状态**: closed
> **创建时间**: 2025-05-14T14:00:21Z
> **更新时间**: 2025-05-15T14:10:39Z
> **关闭时间**: 2025-05-15T14:10:37Z
> **作者**: maxweiss
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4740

## 描述

On all our systems, `rocm-smi --showtoponuma` reports the same "Numa Node" and "Numa Affinity" values for each individual GPU. For example:

```
$ rocm-smi --showtoponuma

============================ ROCm System Management Interface ============================
======================================= Numa Nodes =======================================
GPU[0]		: (Topology) Numa Node: 0
GPU[0]		: (Topology) Numa Affinity: 0
GPU[1]		: (Topology) Numa Node: 0
GPU[1]		: (Topology) Numa Affinity: 0
GPU[2]		: (Topology) Numa Node: 0
GPU[2]		: (Topology) Numa Affinity: 0
GPU[3]		: (Topology) Numa Node: 0
GPU[3]		: (Topology) Numa Affinity: 0
GPU[4]		: (Topology) Numa Node: 1
GPU[4]		: (Topology) Numa Affinity: 1
GPU[5]		: (Topology) Numa Node: 1
GPU[5]		: (Topology) Numa Affinity: 1
GPU[6]		: (Topology) Numa Node: 1
GPU[6]		: (Topology) Numa Affinity: 1
GPU[7]		: (Topology) Numa Node: 1
GPU[7]		: (Topology) Numa Affinity: 1
================================== End of ROCm SMI Log ===================================
```

Is there a difference between these two values, or can we assume they will always be equal? Are there systems or GPUs where "Numa Node" and "Numa Affinity" differ?

---

## 评论 (4 条)

### 评论 #1 — Matthew-Jenkins (2025-05-14T14:07:51Z)

Numa node is which physical cpu grouping it's on. 
Numa affinity is if you have it pinned to another node. 

---

### 评论 #2 — maxweiss (2025-05-15T10:17:50Z)

How can I pin a GPU to a different NUMA node? What happens if I do that? Does the GPU then have affinity to more than one NUMA node?

Sorry if these questions are stupid, but I can’t find any documentation on this.

---

### 评论 #3 — Matthew-Jenkins (2025-05-15T13:47:53Z)

numa isn't specific to rocm. It's a normal part of a multi-socket machine. 
https://en.wikipedia.org/wiki/Non-uniform_memory_access 

You don't pin using rocm. You either pin specific software to specific cores or sockets or you pin specific pci devices to other nodes. 

You usually do not want to pin hardware to a different node than it's on. You typically do so as part of HPC tuning or to solve a specific performance issue. 

Generally, if it is on a different physical node then you're going to go through the interconnect regardless. Pinning it will just add further overhead because userspace might act on it like it is local to the wrong node.

---

### 评论 #4 — maxweiss (2025-05-15T14:10:37Z)

I didn't know that it is possible to pin PCI devices to other NUMA nodes.

Thank you!

---
