# [Issue]: Pytorch performance problem with ROCm on Radeon RX 9060XT with basic operation of matrix multiplication

> **Issue #5442**
> **状态**: open
> **创建时间**: 2025-09-28T17:31:14Z
> **更新时间**: 2025-11-14T15:18:27Z
> **作者**: spagoc
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5442

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- adityas-amd

## 描述

### Problem Description

I have good ROCm performance for matrix dimensions: sizes = [512, 1024, 2048, 4096] but bad performance for matrix dimensions: sizes = [500, 1000, 2000, 3000, 4000, 5000]
I used pytorch.matmul() but the situation is similar using pytorch.mm().

<img width="800" height="600" alt="Image" src="https://github.com/user-attachments/assets/8b816bf0-aeab-4cda-8eee-6b39e277e79b" />

<img width="800" height="600" alt="Image" src="https://github.com/user-attachments/assets/3ee33fb2-a6d0-44b9-ae73-47f1ca0a14a6" />

### Operating System

Ubuntu  24.04.3 LTS (Noble Numbat)

### CPU

12th Gen Intel(R) Core(TM) i5-12500

### GPU

AMD Radeon RX 9060 XT    gfx1200

### ROCm Version

ROCm 7.0.1

### ROCm Component

_No response_

### Steps to Reproduce

[matmul_benchmark.py](https://github.com/user-attachments/files/22584163/matmul_benchmark.py)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.14.14 is loaded
=====================    
 
[rocminfo.txt](https://github.com/user-attachments/files/22584180/rocminfo.txt)

### Additional Information

_No response_

---

## 评论 (16 条)

### 评论 #1 — ppanchad-amd (2025-09-29T13:59:05Z)

Hi @spagoc. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — taylding-amd (2025-09-30T21:46:59Z)

Hi @spagoc, I tested your code in my environment and was unable to reproduce the issue you're seeing. Here are the results I obtained:
```
   Matrix 500x500
   CPU: 0.0061 s
   GPU: 0.0001 s
   CPU/GPU: 55.14 s

   Matrix 1000x1000
   CPU: 0.0032 s
   GPU: 0.0003 s
   CPU/GPU: 9.29 s

   Matrix 2000x2000
   CPU: 0.0135 s
   GPU: 0.0026 s
   CPU/GPU: 5.22 s

   Matrix 3000x3000
   CPU: 0.0289 s
   GPU: 0.0074 s
   CPU/GPU: 3.90 s

   Matrix 4000x4000
   CPU: 0.0717 s
   GPU: 0.0179 s
   CPU/GPU: 4.01 s

   Matrix 5000x5000
   CPU: 0.1498 s
   GPU: 0.0346 s
   CPU/GPU: 4.32 s
```

To rule out any environment-specific issues, could you please try running your tests using our latest PyTorch Docker image? You can find the usage instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html#using-docker-with-pytorch-pre-installed).

---

### 评论 #3 — spagoc (2025-10-01T16:59:59Z)

Hy @taylding-amd  I followed the documentation step by step but I got an error trying to run the docker image:

$ docker run -it \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    --device=/dev/kfd \
    --device=/dev/dri \
    --group-add video \
    --ipc=host \
    --shm-size 8G \
    rocm/pytorch:latest
docker: Error response from daemon: error gathering device information while adding custom device "/dev/kfd": no such file or directory

the same for /dev/dri

running only with:

docker run -it \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    --group-add video \
    --ipc=host \
    --shm-size 8G \
    rocm/pytorch:latest

it's ok but in the Ubuntu container there aren't /dev/kfs and /dev/dri and no GPU detected inside the container:

rocminfo
ROCk module is NOT loaded, possibly no GPU devices

and:

python3 matmul_benchmark_bad_perf.py 
PyTorch ROCm version: 7.0.51831-a3e329ad8
HIP/ROCm disponibile: False
⚠ No detected GPU by ROCm/PyTorch. Only the CPU will be used.


➡️ Matrix 500x500
   CPU: 0.0085 s

➡️ Matrix 1000x1000
   CPU: 0.0039 s

➡️ Matrix 2000x2000
   CPU: 0.0235 s

➡️ Matrix 3000x3000
   CPU: 0.0772 s

➡️ Matrix 4000x4000
   CPU: 0.2018 s

➡️ Matrix 5000x5000
   CPU: 0.3476 s


---

### 评论 #4 — taylding-amd (2025-10-01T19:28:59Z)

Can you try running with sudo? 

---

### 评论 #5 — spagoc (2025-10-02T07:49:00Z)

Hy @taylding-amd , docker run with sudo works but the performances are quite bad:

root@8355a76e7263:/home/ubuntu# python3 matmul_benchmark_bad_perf.py 
PyTorch ROCm version: 7.0.51831-a3e329ad8
HIP/ROCm disponibile: True
Detected GPU: AMD Radeon RX 9060 XT

➡️ Matrix 500x500
   CPU: 0.0008 s
   GPU: 0.0003 s
   CPU/GPU: 2.82

➡️ Matrix 1000x1000
   CPU: 0.0031 s
   GPU: 0.0018 s
   CPU/GPU: 1.70

➡️ Matrix 2000x2000
   CPU: 0.0231 s
   GPU: 0.0126 s
   CPU/GPU: 1.84

➡️ Matrix 3000x3000
   CPU: 0.0768 s
   GPU: 0.0415 s
   CPU/GPU: 1.85

➡️ Matrix 4000x4000
   CPU: 0.1852 s
   GPU: 0.1187 s
   CPU/GPU: 1.56

➡️ Matrix 5000x5000
   CPU: 0.3609 s
   GPU: 0.2266 s
   CPU/GPU: 1.59


---

### 评论 #6 — spagoc (2025-10-02T11:35:59Z)

Same data for CUDA on a similar priced RTX old generation card: 

PyTorch ROCm version: None
HIP/ROCm disponibile: True
Detected GPU: NVIDIA GeForce RTX 2060 SUPER

➡️ Matrix 500x500
   CPU: 0.0008 s
   GPU: 0.0001 s
   CPU/GPU: 7.97

➡️ Matrix 1000x1000
   CPU: 0.0032 s
   GPU: 0.0005 s
   CPU/GPU: 5.85

➡️ Matrix 2000x2000
   CPU: 0.0236 s
   GPU: 0.0033 s
   CPU/GPU: 7.16

➡️ Matrix 3000x3000
   CPU: 0.0750 s
   GPU: 0.0091 s
   CPU/GPU: 8.28

➡️ Matrix 4000x4000
   CPU: 0.1733 s
   GPU: 0.0214 s
   CPU/GPU: 8.10

➡️ Matrix 5000x5000
   CPU: 0.3377 s
   GPU: 0.0414 s
   CPU/GPU: 8.15

![Image](https://github.com/user-attachments/assets/79fe9690-3ce1-4b8a-a4b0-effc84672796)

[matmul_benchmark-unified.py](https://github.com/user-attachments/files/22658624/matmul_benchmark-unified.py)



---

### 评论 #7 — naromero77amd (2025-10-03T20:08:53Z)

@spagoc  Can you clarify which Docker image was used?

Do you still see this performance issues in the nightly PyTorch wheel? (from https://pytorch.org/)
```
pip3 install --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/rocm7.0
```


---

### 评论 #8 — spagoc (2025-10-04T10:18:06Z)

Hy @naromero77amd ,
I did it,  here is the result:

PyTorch ROCm version: 7.0.51831-a3e329ad8
PyTorch version: 2.10.0.dev20251001+rocm7.0
HIP/ROCm disponibile: True
Detected GPU: AMD Radeon RX 9060 XT

➡️ Matrix 500x500
   CPU: 0.0011 s
   GPU: 0.0003 s
   CPU/GPU: 3.52

➡️ Matrix 1000x1000
   CPU: 0.0054 s
   GPU: 0.0019 s
   CPU/GPU: 2.87

➡️ Matrix 2000x2000
   CPU: 0.0424 s
   GPU: 0.0119 s
   CPU/GPU: 3.57

➡️ Matrix 3000x3000
   CPU: 0.0780 s
   GPU: 0.0394 s
   CPU/GPU: 1.98

➡️ Matrix 4000x4000
   CPU: 0.2010 s
   GPU: 0.1144 s
   CPU/GPU: 1.76

➡️ Matrix 5000x5000
   CPU: 0.3699 s
   GPU: 0.2234 s
   CPU/GPU: 1.66




---

### 评论 #9 — reywang18 (2025-10-04T18:07:41Z)

So this is for 16GB RX 9060XT ?
[500, 1000, 2000, 3000, 4000, 5000] has bad performance, but 512 .. are good.
Not clear 500 vs 512, is it just move on with 512, unless there is a particular reason we need 500 setting?
Could 512, power of 2 so GPU has better performance..

---

### 评论 #10 — naromero77amd (2025-10-06T15:53:35Z)

@spagoc Thank you for trying the nightly wheel. Can you please try one more thing?

For the matrix sizes that are exhibiting poor performance, can you try running your benchmark with this environment variable set:
```
TORCH_BLAS_PREFER_HIPBLASLT=0
```

This will force it to use rocBLAS for the GEMMs.


---

### 评论 #11 — spagoc (2025-10-07T06:45:40Z)

@naromero77amd 
I did it, here is the result:

(nightly) rino@game2:~/Documenti/gpu/pytorch-gpu-unified$ TORCH_BLAS_PREFER_HIPBLASLT=0 python matmul_benchmark-unified.py 
PyTorch hip/ROCm version: 7.0.51831-a3e329ad8
PyTorch version: 2.10.0.dev20251001+rocm7.0
HIP/ROCm disponibile: True
Detected GPU: AMD Radeon RX 9060 XT

➡️ Matrix 500x500
   CPU: 0.0011 s
   GPU: 0.0003 s
   CPU/GPU: 4.08

➡️ Matrix 1000x1000
   CPU: 0.0054 s
   GPU: 0.0018 s
   CPU/GPU: 2.98

➡️ Matrix 2000x2000
   CPU: 0.0413 s
   GPU: 0.0133 s
   CPU/GPU: 3.10

➡️ Matrix 3000x3000
   CPU: 0.0766 s
   GPU: 0.0439 s
   CPU/GPU: 1.74

➡️ Matrix 4000x4000
   CPU: 0.1851 s
   GPU: 0.1192 s
   CPU/GPU: 1.55

➡️ Matrix 5000x5000
   CPU: 0.3601 s
   GPU: 0.2246 s
   CPU/GPU: 1.60

<img width="800" height="600" alt="Image" src="https://github.com/user-attachments/assets/2ffc3974-f1ff-43fd-8e2f-a6c56a983c5d" />

---

### 评论 #12 — naromero77amd (2025-10-07T18:31:09Z)

@spagoc thanks for the data, unfortunately no improvement

---

### 评论 #13 — fjankovi (2025-10-22T16:04:06Z)

Is the issue still present in ROCm 7.0.2? Some gfx12 hipblaslt changes were added in 7.0.2 such as: https://github.com/ROCm/rocm-libraries/commit/f3c7769bb180bce42c09b0373f7b81d8ea94ab0d

---

### 评论 #14 — spagoc (2025-10-24T09:08:08Z)

@fjankovi I am already using 7.0.2 as you can see from the following command:

$ amd-smi version
AMDSMI Tool: 26.0.2+39589fda | AMDSMI Library version: 26.0.2 | ROCm version: 7.0.2 | amdgpu version: 6.14.14 | amd_hsmp version: N/A

and I installed again the pytorch nightly version for ROCm 7.0 as in:  https://pytorch.org/get-started/locally/

And there is not performance improvement:

HIP/ROCm or CUDA available: True
PyTorch hip/ROCm version: 7.0.51831-7c9236b16
PyTorch CUDA version: None
PyTorch version: 2.10.0.dev20251022+rocm7.0
Detected GPU: AMD Radeon RX 9060 XT

➡️ Matrix 500x500
   CPU: 0.0012 s
   GPU: 0.0003 s
   CPU/GPU: 4.34

➡️ Matrix 1000x1000
   CPU: 0.0054 s
   GPU: 0.0020 s
   CPU/GPU: 2.68

➡️ Matrix 2000x2000
   CPU: 0.0371 s
   GPU: 0.0101 s
   CPU/GPU: 3.69

➡️ Matrix 3000x3000
   CPU: 0.0772 s
   GPU: 0.0405 s
   CPU/GPU: 1.90

➡️ Matrix 4000x4000
   CPU: 0.1865 s
   GPU: 0.1188 s
   CPU/GPU: 1.57

➡️ Matrix 5000x5000
   CPU: 0.3624 s
   GPU: 0.2224 s
   CPU/GPU: 1.63


---

### 评论 #15 — vuksan314 (2025-10-24T14:32:29Z)

Hi @spagoc would you consider using torch.float16?


---

### 评论 #16 — spagoc (2025-10-27T09:58:05Z)

Hi @vuksan314  in case of matrices made of pytorch.float16 (half precision) elements I have very, very bad CPU performance and very good ROCm performance:

(torch-env-nightly) rino@game2:~/Documenti/gpu/pytorch-gpu-unified$ python matmul_benchmark_unified_dtype.py 
HIP/ROCm or CUDA available: True
PyTorch hip/ROCm version: 7.0.51831-7c9236b16
PyTorch CUDA version: None
PyTorch version: 2.10.0.dev20251022+rocm7.0
PyTorch dtype: torch.float16
Detected GPU: AMD Radeon RX 9060 XT

➡️ Matrix 500x500
   CPU: 0.0733 s
   GPU: 0.0001 s
   CPU/GPU: 611.61

➡️ Matrix 1000x1000
   CPU: 0.5923 s
   GPU: 0.0005 s
   CPU/GPU: 1187.52

➡️ Matrix 2000x2000
   CPU: 5.1933 s
   GPU: 0.0003 s
   CPU/GPU: 15426.48

➡️ Matrix 3000x3000
   CPU: 45.3127 s
   GPU: 0.0012 s
   CPU/GPU: 36374.22

➡️ Matrix 4000x4000
   CPU: 115.1721 s
   GPU: 0.0023 s
   CPU/GPU: 49027.40

➡️ Matrix 5000x5000
   CPU: 241.8485 s
   GPU: 0.0042 s
   CPU/GPU: 57251.73

<img width="800" height="600" alt="Image" src="https://github.com/user-attachments/assets/49ce6729-2e67-4131-850b-49c3dadb3649" />

[matmul_benchmark_unified_dtype.py](https://github.com/user-attachments/files/23161606/matmul_benchmark_unified_dtype.py)

---
