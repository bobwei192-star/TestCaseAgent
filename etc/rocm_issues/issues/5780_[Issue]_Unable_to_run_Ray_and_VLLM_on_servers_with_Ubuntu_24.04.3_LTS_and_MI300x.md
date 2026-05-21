# [Issue]: Unable to run Ray and VLLM on servers with Ubuntu 24.04.3 LTS and MI300x GPUs

> **Issue #5780**
> **状态**: open
> **创建时间**: 2025-12-15T22:42:54Z
> **更新时间**: 2026-02-26T15:02:53Z
> **作者**: mnoiseux
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5780

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

We have been given access to 4 servers each having 8 MI300x GPUs in them. But we have not been able to successfully run VLLM with Ray which prevent us from being able to run VLLM on more then one server.

The problem is that when we start VLLM on a Ray node we get the error torch.AcceleratorError: HIP error: invalid device ordinal

Note that if we start VLLM without Ray, it starts without problem. 

We are also able to start VLLM with Ray on the 4 servers when we use a docker image that has Ubuntu 22.04.5 LTS  with glibc 2.35   instead of Ubuntu 24.04.3 LTS with glibc 2.39.

To run tests and troubleshoot the issue we created docker images. One with the same Ubuntu version then the one on the host and one with an older version.

Component                | Host Venv                         | Docker Ubuntu 24.04       | Docker Ubuntu 22.04 (TCP)
-------------------- |--------------------------|--------------------------|---------------------------
OS                               | Ubuntu 24.04.3 LTS        | Ubuntu 24.04.3 LTS          | Ubuntu 22.04.5 LTS       
glibc                            | 2.39                                  | 2.39                                    | 2.35                     
Python                        | 3.12.3                                | 3.12.3                                 | 3.12.12                  
vLLM                          | 0.11.2                                 | 0.11.2                                  | 0.11.2                   
PyTorch                     | 2.9.0a0+git1c57644         | 2.9.0a0+git1c57644        | 2.9.0a0+git1c57644       
Ray                            | 2.52.1                                 | 2.52.1                                 | 2.52.1                   
ROCm                        | 7.1.1                                    | 7.1.0                                  | 7.1.0                    

=== BEHAVIOR SUMMARY ===

Host Venv (runing on the host itself)+ Ray :         ❌ HIP error: invalid device ordinal
Host Venv (runing on the host itself) Without Ray:      ✅ Works (not tested in this report)
Docker Ubuntu 24.04 + Ray: ❌ HIP error: invalid device ordinal
Docker Ubuntu 24.04 (no Ray): ✅ Works
Docker Ubuntu 22.04 + Ray: ✅ Works

If it may help, we also tried different environment variables setting but without success, We tried GPU_DEVICE_ORDINAL (any variation), HIP_VISIBLE_DEVICES,  ROCR_VISIBLE_DEVICES,  CUDA_VISIBLE_DEVICES,  ROCM_PATH, HIP_PATH, VLLM_USE_V1

So there seems to be a GPU numbering mismatch between Ray and HIP. 

Would you be able to help us figuring out where the problem is and how to fix it ^Maybe you have a modified code that works on tour side we can use ?

Thanks a lot for your help on this

### Operating System

OS: NAME="Ubuntu" VERSION="24.04.3 LTS (Noble Numbat)"

### CPU

CPU:  model name      : AMD EPYC 9534 64-Core Processor

### GPU

GPU:   Name:                    AMD EPYC 9534 64-Core Processor       Marketing Name:          AMD EPYC 9534 64-Core Processor       Name:                    AMD EPYC 9534 64-Core Processor       Marketing Name:          AMD EPYC 9534 64-Core Processor       Name:                    gfx942                                Marketing Name:          AMD Instinct MI300X                       Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-       Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-   Name:                    gfx942                                Marketing Name:          AMD Instinct MI300X                       Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-       Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-   Name:                    gfx942                                Marketing Name:          AMD Instinct MI300X                       Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-       Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-   Name:                    gfx942                                Marketing Name:          AMD Instinct MI300X                       Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-       Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-   Name:                    gfx942                                Marketing Name:          AMD Instinct MI300X                       Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-       Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-   Name:                    gfx942                                Marketing Name:          AMD Instinct MI300X                       Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-       Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-   Name:                    gfx942                                Marketing Name:          AMD Instinct MI300X                       Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-       Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-   Name:                    gfx942                                Marketing Name:          AMD Instinct MI300X                       Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-       Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-

### ROCm Version

7.1.1 (also tried 7.1.0)

### ROCm Component

_No response_

### Steps to Reproduce

Start a single Ray node on a single server and then launch VLLM. The error is seen as VLLM initialize

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (21 条)

### 评论 #1 — schung-amd (2025-12-16T17:52:04Z)

Hi @mnoiseux, thanks for the report, I'll look into it. Can you post the output on the failing system? We have seen this error before when not specifying ray as the backend (https://github.com/ROCm/ROCm/issues/5567), and I suspect your issue might also stem from `ray` not being used; make sure you have `--distributed_executor_backend="ray"` in your `vllm serve` command.

---

### 评论 #2 — mnoiseux (2025-12-16T18:58:40Z)

Please find the file vllm_launch.log. In it you'll see we are setting --distributed_executor_backend to ray at line 6. Setting this argument is part of our launching script command:

python3 -m vllm.entrypoints.openai.api_server \
    --model ${MODEL_NAME} \
    --host 0.0.0.0 \
    --port ${VLLM_PORT} \
    --tensor-parallel-size ${TENSOR_PARALLEL_SIZE} \
    --pipeline-parallel-size ${PIPELINE_PARALLEL_SIZE} \
    $( $ENABLE_EXPERT_PARALLEL && echo "--enable_expert_parallel" ) \
    $( [[ -n "${MAX_MODEL_LEN}" ]] && echo "--max-model-len ${MAX_MODEL_LEN}" ) \
    $( [[ -n "${MAX_NUM_BATCHED_TOKENS}" ]] && echo "--max-num-batched-tokens ${MAX_NUM_BATCHED_TOKENS}" ) \
    $( [[ -n "${MAX_NUM_SEQS}" ]] && echo "--max-num-seqs ${MAX_NUM_SEQS}" ) \
    $( [[ -n "${GPU_MEMORY_UTILIZATION}" ]] && echo "--gpu-memory-utilization ${GPU_MEMORY_UTILIZATION}" ) \
    $( [[ -n "${API_KEY}" ]] && echo "--api-key ${API_KEY}" ) \
    --trust-remote-code \
    --distributed-executor-backend ray \
    --disable-log-requests"

You'll also see the logs and backtraces when the torch.AcceleratorError: HIP error: invalid device ordinal error happen. If you need anything else, let me know

[vllm_launch.log](https://github.com/user-attachments/files/24198205/vllm_launch.log)

---

### 评论 #3 — schung-amd (2025-12-16T19:26:26Z)

Thanks for the quick response, from the logs ray is indeed being used.

---

### 评论 #4 — schung-amd (2025-12-16T20:26:20Z)

Can you try `RAY_EXPERIMENTAL_NOSET_ROCR_VISIBLE_DEVICES=1`? https://github.com/vllm-project/vllm/issues/12572 looks similar to your issue here.

Also, are your Docker images based on one of our rocm/vllm or rocm/vllm-dev Docker images, or vLLM built from source? Will try to repro with a similar a configuration as possible (although sourcing MI300s has been tricky lately).

---

### 评论 #5 — mnoiseux (2025-12-16T21:12:12Z)

In the course of trying to make it work we used different base image and different approches for building the docker image. The one which was used to gather the logs we sent you is based on ubuntu 24.4 on which we added the required pieces. This is the one which make us the most progress as it is working fine if Ray is not used before starting VLLM. 
We also tried building an image from rocm/vllm-dev:rocm7.1.1_navi_ubuntu24.04_py3.12_pytorch_2.8_vllm_0.10.2rc1 but we were seeing segfaults when starting VLLM and running tests.
If you want we can provide the script we use to build the image with which we made most progress.
About your suggestion, let me try it and get back to you.

---

### 评论 #6 — schung-amd (2025-12-16T21:15:02Z)

> If you want we can provide the script we use to build the image with which we made most progress.

That would be great, thanks.

---

### 评论 #7 — mnoiseux (2025-12-16T21:55:38Z)

Unfortunately we still got the torch.AcceleratorError: HIP error: invalid device ordinal error with RAY_EXPERIMENTAL_NOSET_ROCR_VISIBLE_DEVICES set to 1. It was validated that RAY_EXPERIMENTAL_NOSET_ROCR_VISIBLE_DEVICES was set in the Ray process before VLLM was started. But unfortunately the error is still there. We'll prepare the script and docker file you'll need to build the docker image. We need to remove some parts which contains propriatary code which is not required to reproduce the issue

---

### 评论 #8 — mnoiseux (2025-12-16T22:18:17Z)

FYI, I modified the scripts and Docker file. Now I am buidling on my side to make sure it builds. Once validated I'll share the files

---

### 评论 #9 — mnoiseux (2025-12-17T14:51:18Z)

Sorry for the delay. We are facing issues building ubuntu 24.4 for you because ours is build using another internal image. But we are not block because we can see the same HIP issue if we use rocm/vllm-dev:rocm7.1.1_navi_ubuntu24.04_py3.12_pytorch_2.8_vllm_0.10.2rc1 as the base image and add Ray 2.52.1 to it. You will find below the script and Docker file (tar to be able to attach it) needed to build the image

You just need to run the script and this will create the image v0.10.2-rocm7.1.1-ubuntu24.04-minimal

On a related subject, is there any docker file available you can point us to which have been proven working correctly with Ubuntu 24.4 and Ray/VLLM for multi node/multi GPU  with tensor and pipeline parallelism ? 

Thanks a lot for your support

[build_amd_ubuntu2404_minimal.sh](https://github.com/user-attachments/files/24215487/build_amd_ubuntu2404_minimal.sh)

[Dockerfile.vllm-amd-ubuntu2404-minimal.tar.gz](https://github.com/user-attachments/files/24215643/Dockerfile.vllm-amd-ubuntu2404-minimal.tar.gz)

---

### 评论 #10 — schung-amd (2025-12-17T16:33:03Z)

Thanks!

> is there any docker file available you can point us to which have been proven working correctly with Ubuntu 24.4 and Ray/VLLM for multi node/multi GPU with tensor and pipeline parallelism ?

I've been testing with `rocm/vllm:latest` for tensor parallelism. My test case is quite minimal though; two nodes with a single GPU each, tensor parallelism 2, and a small model. If your issue is due to some breakage in device enumeration this might not repro it. I'll reach out internally to see if anyone's had recent success with similar configurations to yours.

e: This testing was done with ray specifically.

---

### 评论 #11 — mnoiseux (2025-12-17T16:36:08Z)

Ok thanks. As a reminder, the problem happens when Ray is use. On a single node/8 GPUs we can run VLLM withoyt Ray. It is when we add Ray to the equation (either for single or multiple node) that the issue is seen.

---

### 评论 #12 — schung-amd (2025-12-17T16:42:11Z)

Yes, thanks for the reminder. My testing has all been done with ray, will edit the above message to mention that.

---

### 评论 #13 — mnoiseux (2025-12-18T01:03:05Z)

FYI, we also just tried the latest Ray version to see it it could contain a fix for the issue we are seeing updating one of our failed Docker image with:

RUN pip3 uninstall -y ray && \
    pip3 install --no-cache-dir -U "ray[default,serve] @ https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp312-cp312-manylinux2014_x86_64.whl"

But we still have the same torch.AcceleratorError: HIP error: invalid device ordinal error.

We have not been able to find the proper mix of Ray, VLLM, PyTorch, ROCm, HIP which would allow us to run multi-node Ubuntu 24.4/multi-GPUs MI300x tensor/pipeline parallelism. When you'll get the information on this let us know. Thanks

---

### 评论 #14 — huanrwan-amd (2025-12-19T19:03:07Z)

Hi @mnoiseux, is Ubuntu 24.04 a hard requirement for you as Ubuntu 22.04 works for you guys?

It would be noticed that `rocm7.1.1_navi_ubuntu24.04_py3.12_pytorch_2.8_vllm_0.10.2rc1` in the given script seems used for Navi card not for Instinct. 


---

### 评论 #15 — mnoiseux (2025-12-19T20:12:26Z)

Unfortunately yes ubuntu 24.04 is a hard requirement. This is what is present on the servers we are provided with. We had a docker image made from rocm/dev-ubuntu-22.04:latest but couldn't managed to make it work using the Broadcom NICs present on the server due to what points to a glibc incompatibility between the docker image and host at the Broadcom level.  We were able to use the single Mellanox NIC on the server with this image but not the 8 x Broadcom NICs.

We can send you some of the docker image we used if it can help and if you have a way for us to send it to you.

Is there an official/or development docker file for Ubuntu 24.4 with Ray, VLLM, PyTorch, ROCm, HIP which would allow us to run multi-node Ubuntu 24.4/multi-GPUs MI300x tensor/pipeline parallelism nad has been proven working ? Or maybe proven steps to build such validated image ? 

Thanks a lot for your support

---

### 评论 #16 — mnoiseux (2025-12-19T21:45:22Z)

The docker image rocm/vllm-dev:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.9.1_atom_ds_1208 you pointed us to does not have Ray and VLLM despite the name contains VLLM in it. Can you confirm we are not missing it ? If it is not in the image, do you have a recommendation on which one to use or we go with what we used in our other images i.e. Ray 2.52.1 and VLLM 0.11.2 ? Thanks

---

### 评论 #17 — mnoiseux (2025-12-20T00:57:52Z)

We have built a new docker image from rocm/vllm-dev:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.9.1_atom_ds_1208 as you suggested. We added Ray: 2.52.1 and vLLM: 0.11.3.dev0+g275de3417.d20251220  in it, ran our test and got the same HIP error: invalid device ordinal, YOu will find below the Docker file twe used to create our Docker image amd-ray-vllm:amd-12-19-25-test, the script we used to create this image as well as a document providing information about the host, docker and environment variables set in it when we run our test. It you need more information let us know.

[build_amd_12_19_25_image.sh](https://github.com/user-attachments/files/24267837/build_amd_12_19_25_image.sh)

[DockerFile.From-AMD-12-19-25-Image.tar.gz](https://github.com/user-attachments/files/24267840/DockerFile.From-AMD-12-19-25-Image.tar.gz)

[System-Test-Docker-Information.rtf](https://github.com/user-attachments/files/24267842/System-Test-Docker-Information.rtf)


---

### 评论 #18 — huanrwan-amd (2025-12-22T18:19:02Z)

Hi @mnoiseux, talked with internal Ray team. There is no official Ubuntu 24.04 image release yet. I also tried on my side: the one posted on the vllm-dev does not have vllm pre-installed. I will post once we have any update.

---

### 评论 #19 — mnoiseux (2025-12-22T19:40:57Z)

Thanks for your feedback. Do you think the instructions we sent in the previous post to add Ray and VLLM can be use by the Ray team top recreate and trouble shoot the problem ?

---

### 评论 #20 — mnoiseux (2026-01-05T14:26:28Z)

Hello. We were wondering if it would be possible to let us know if the instructions we sent 3 posts ago which describe how to add Ray and VLLM to rocm/vllm-dev:rocm7.1.1_ubuntu24.04_py3.12_pytorch_release_2.9.1_atom_ds_1208 image can be use by the Ray team to recreate and troubleshoot the problem ? Also, do you have an estimated time when the official Ubuntu 24.04 image working with Ray will be released ? Thanks

---

### 评论 #21 — yaoliu13 (2026-02-25T19:19:26Z)

@mnoiseux Could you share which company or university you are working for?

---
