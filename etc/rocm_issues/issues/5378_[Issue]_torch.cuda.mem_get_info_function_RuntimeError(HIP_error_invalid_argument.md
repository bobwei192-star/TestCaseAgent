# [Issue]: torch.cuda.mem_get_info function RuntimeError(HIP error: invalid argument) from rocm/gpu-operator

> **Issue #5378**
> **状态**: closed
> **创建时间**: 2025-09-18T09:05:50Z
> **更新时间**: 2025-09-22T18:04:08Z
> **关闭时间**: 2025-09-22T18:04:08Z
> **作者**: jaeyung2
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5378

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- harkgill-amd

## 描述

I moved the issue from [rocm/gpu-operator](https://github.com/ROCm/gpu-operator) to here.
- https://github.com/ROCm/gpu-operator/issues/330 

### Problem Description

I'm try to run sample code in container after install gpu-operator helm chart on my cluster(1.32.8 k8s version). my test code is below.

```python
import torch
if torch.cuda.is_available():
    free_memory_bytes, total_memory_bytes = torch.cuda.mem_get_info()

    free_memory_gb = free_memory_bytes / (1024**3)
    total_memory_gb = total_memory_bytes / (1024**3)

    print(f"Free GPU memory: {free_memory_gb:.2f} GB")
    print(f"Total GPU memory: {total_memory_gb:.2f} GB")

else:
    print("CUDA is not available. Cannot get GPU memory info.")
```

and error message is:
```
Traceback (most recent call last):
  File "/var/lib/jenkins/test.py", line 4, in <module>
    free_memory_bytes, total_memory_bytes = torch.cuda.mem_get_info()
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/cuda/memory.py", line 738, in mem_get_info
    return torch.cuda.cudart().cudaMemGetInfo(device)
RuntimeError: HIP error: invalid argument
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

my pod yaml information:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: rocm-pytorch-test
  namespace: kube-amd-gpu
  labels:
    app: rocm-pytorch-test
spec:
  restartPolicy: Never
  tolerations:
    - key: "amd.com/gpu"
      operator: "Exists"
      effect: "NoSchedule"
  containers:
    - name: rocm-pytorch
      image: rocm/pytorch:rocm6.4.2_ubuntu22.04_py3.10_pytorch_release_2.6.0
      imagePullPolicy: IfNotPresent
      command: ["sleep", "infinity"]
      resources:
        limits:
          "amd.com/gpu": 8
```

And our team just found that the issue occured from ubuntu 22.04. but not in ubuntu 24.04. We tested with hip code like below.

- test_pod.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: rocminfo
  namespace: kube-amd-gpu
spec:
  containers:
  - image: docker.io/rocm/rocm-terminal:latest
    name: rocminfo
    command: ["/bin/sh","-c"]
    args: ["rocminfo && sleep infinity"]
    securityContext:
      runAsUser: 0
    resources:
      limits:
        amd.com/gpu: 8
  restartPolicy: Never
```

- test.cpp (build in container)
```cpp
#include <hip/hip_runtime.h>
#include <iostream>

void checkHipError(hipError_t err) {
    if (err != hipSuccess) {
        std::cerr << "HIP Error: " << hipGetErrorString(err) << std::endl;
        exit(EXIT_FAILURE);
    }
}

int main() {
    checkHipError(hipSetDevice(0));
    std::cout << "✅ HIP Runtime and Initialize GPU device success." << std::endl;

    size_t free_bytes, total_bytes;

    hipError_t err = hipMemGetInfo(&free_bytes, &total_bytes);

    if (err != hipSuccess) {
        std::cerr << "❌ Error: Failed to get GPU memory information." << std::endl;
        std::cerr << "HIP Error: " << hipGetErrorString(err) << std::endl;
        return -1;
    }

    std::cout << "🎉 Success: Available to get GPU memory information." << std::endl;

    double free_mb = static_cast<double>(free_bytes) / (1024.0 * 1024.0);
    double total_mb = static_cast<double>(total_bytes) / (1024.0 * 1024.0);
    
    std::cout << "----------------------------------------" << std::endl;
    std::cout << "GPU memory info:" << std::endl;
    std::cout << "  - Total memory (Total): " << total_mb << " MB" << std::endl;
    std::cout << "  - Available memory (Free): " << free_mb << " MB" << std::endl;
    std::cout << "----------------------------------------" << std::endl;

    return 0;
}
```

- ubuntu 22.04 (kernel version: 5.15.0-153-generic, rocm version: 6.4.2)
```
root@rocminfo:/home/rocm-user# ./test 
✅ HIP Runtime and Initialize GPU device success.
❌ Error: Failed to get GPU memory information.
HIP Error: invalid argument
```

- ubuntu 24.04 (kernel version: 6.8.0-83-generic, rocm version: 6.4.2)
```
root@rocminfo:/home/rocm-user# ./test
✅ HIP Runtime and Initialize GPU device success.
🎉 Success: Available to get GPU memory information.
----------------------------------------
GPU memory info:
  - Total memory (Total):65520 MB
  - Available memory (Free): 65446 MB
----------------------------------------
```

and also found that difference kernel module load between ubuntu22.04 and ubuntu24.04.

```
# ubuntu 24.04 (after reboot)
root@mi250-041:~# lsmod | grep -i amd
amdgpu              19730432  10
amddrm_ttm_helper      12288  1 amdgpu
amdttm                114688  2 amdgpu,amddrm_ttm_helper
amddrm_buddy           24576  1 amdgpu
amdxcp                 12288  1 amdgpu
amd_sched              61440  1 amdgpu
amdkcl                 36864  3 amd_sched,amdttm,amdgpu
drm_exec               12288  1 amdgpu
drm_suballoc_helper    16384  1 amdgpu
drm_display_helper    237568  1 amdgpu
cec                    94208  2 drm_display_helper,amdgpu
video                  77824  1 amdgpu
amd64_edac             61440  0
edac_mce_amd           28672  1 amd64_edac
kvm_amd               208896  0
kvm                  1409024  1 kvm_amd
ccp                   143360  1 kvm_amd
i2c_algo_bit           16384  3 igb,ast,amdgpu

# ubuntu 22.04 (after reboot)
root@mi250-042:~/gpu-operator# lsmod | grep -i amd
amd64_edac             53248  0
edac_mce_amd           36864  1 amd64_edac
kvm_amd               155648  0
kvm                  1040384  1 kvm_amd
ccp                   110592  1 kvm_amd
amdgpu               9904128  10
iommu_v2               24576  1 amdgpu
gpu_sched              45056  1 amdgpu
drm_ttm_helper         16384  3 drm_vram_helper,ast,amdgpu
ttm                    86016  3 drm_vram_helper,amdgpu,drm_ttm_helper
drm_kms_helper        315392  5 drm_vram_helper,ast,amdgpu
drm                   622592  8 gpu_sched,drm_kms_helper,drm_vram_helper,ast,amdgpu,drm_ttm_helper,ttm
i2c_algo_bit           16384  3 igb,ast,amdgpu
```

I think it should work on Ubuntu 22.04, but I don't know the exact reason why the problem is happening. Does it happen as a kernel module difference as mentioned above?

### Operating System

Ubuntu 22.04, Ubuntu 24.04

### CPU

AMD EPYC 7413 24-Core Processor

### GPU

AMD Instinct MI250X/MI250

### ROCm Version

ROCm 6.4.2

### ROCm Component

HIP

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — jaeyung2 (2025-09-18T11:49:21Z)

update comment: https://github.com/ROCm/gpu-operator/issues/330#issuecomment-3306876919

---

### 评论 #2 — ppanchad-amd (2025-09-18T14:08:45Z)

Hi @jaeyung2. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — harkgill-amd (2025-09-19T19:23:20Z)

Investigation continuing over at https://github.com/ROCm/gpu-operator/issues/330

---

### 评论 #4 — harkgill-amd (2025-09-22T18:04:08Z)

Closing this issue out as it's root caused/pending a fix in the aforementioned ticket.

---
