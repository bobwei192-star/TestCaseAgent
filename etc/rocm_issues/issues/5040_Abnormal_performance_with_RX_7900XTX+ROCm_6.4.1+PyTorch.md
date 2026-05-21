# Abnormal performance with RX 7900XTX+ROCm 6.4.1+PyTorch

> **Issue #5040**
> **状态**: open
> **创建时间**: 2025-07-14T13:51:54Z
> **更新时间**: 2025-07-22T19:53:08Z
> **作者**: octaveoclx
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5040

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Dear all,
I was performing a simple case from [https://discuss.pytorch.org/t/timings-for-intel-arc-graphics-xpu-vs-nvidia-rtx-3000-gpu-on-a-laptop/218200/2](https://discuss.pytorch.org/t/timings-for-intel-arc-graphics-xpu-vs-nvidia-rtx-3000-gpu-on-a-laptop/218200/2) to test the timing of 7900XTX with nightly built of PyTorch (today). However, it produced the performance way below other devices as indicated by pyfan in the link.
7900XTX took around 53 seconds, which seems to be too slow.

/home/jc/PycharmProjects/PythonProject/.venv/bin/python /home/jc/PycharmProjects/PythonProject/t1.py 
2.9.0.dev20250713+rocm6.4
True
version.cuda: None
Radeon RX 7900 XTX
_CudaDeviceProperties(name='Radeon RX 7900 XTX', major=11, minor=0, gcnArchName='gfx1100', total_memory=24560MB, multi_processor_count=48, uuid=35626461-6536-3132-3434-633261393430, pci_bus_id=45, pci_device_id=0, pci_domain_id=0, L2_cache_size=6MB)
device: cuda
lossInit: tensor(0.7298, device='cuda:0', grad_fn=<MseLossBackward0>)
lossFinl: tensor(0.0299, device='cuda:0', grad_fn=<MseLossBackward0>)
device: cuda  time: 53.3579    nBatch: 100000  nEpoch: 1000

Process finished with exit code 0

Best wishes


---

## 评论 (13 条)

### 评论 #1 — octaveoclx (2025-07-14T13:53:38Z)

Also the multi_processor_count=48 is not correct, which should be 96 for this device while using torch.cuda.get_device_properties()? 

---

### 评论 #2 — ppanchad-amd (2025-07-14T15:29:43Z)

Hi @octaveoclx. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — schung-amd (2025-07-14T16:17:03Z)

Hi @octaveoclx, haven't taken a look at the benchmark yet, but

>  the multi_processor_count=48 is not correct, which should be 96 for this device while using torch.cuda.get_device_properties()?

This is probably due to WGP mode, which groups CUs in pairs by default on gfx10+; see https://github.com/ROCm/hip/issues/3767.

---

### 评论 #4 — B4rr3l-Rid3r (2025-07-14T22:34:23Z)

> Hi [@octaveoclx](https://github.com/octaveoclx), haven't taken a look at the benchmark yet, but
> 
> > the multi_processor_count=48 is not correct, which should be 96 for this device while using torch.cuda.get_device_properties()?
> 
> This is probably due to WGP mode, which groups CUs in pairs by default on gfx10+; see [ROCm/hip#3767](https://github.com/ROCm/hip/issues/3767).

on 9070 it says 28 so it is half, 70s on 9070 is awful.

---

### 评论 #5 — schung-amd (2025-07-17T20:11:44Z)

Was able to reproduce this on a 9070, getting around 60s reported for the test. rocprofv3 sys-trace output shows 85 of the hipLaunchKernel calls taking >650ms while others are on the magnitude of 100us, which accounts for >50s of the execution time. We've seen issues with occasional extreme kernel launch overhead in workloads which spawn many small kernels in the past, looking into these to see if there was a determined root cause and/or available workaround.

---

### 评论 #6 — NTFSynergy (2025-07-19T23:00:33Z)

Running this bench on stock install 9070XT, Ubuntu  24.04.2 LTS, produces this result:

```python
2.9.0.dev20250705+rocm6.4
version.cuda: None
AMD Radeon RX 9070 XT
_CudaDeviceProperties(name='AMD Radeon RX 9070 XT', major=12, minor=0, gcnArchName='gfx1201', total_memory=16304MB, multi_processor_count=32, uuid=34343130-6635-6462-3464-313035313064, pci_bus_id=9, pci_device_id=0, pci_domain_id=0, L2_cache_size=8MB)
device: cuda
lossInit: tensor(0.7307, device='cuda:0', grad_fn=<MseLossBackward0>)
lossFinl: tensor(0.0289, device='cuda:0', grad_fn=<MseLossBackward0>)
device: cuda  time: 58.9353    nBatch: 100000  nEpoch: 1000

``` 
however, since I tinkered around with my venv for SD.Next, I wanted to know what will be the difference between stock and tuned, so I added these commands before running the benchmark:

```python
export LD_PRELOAD=libtcmalloc.so.4 PYTORCH_TUNABLEOP_ENABLED=1 PYTORCH_TUNABLEOP_TUNING=1 PYTORCH_TUNABLEOP_FILENAME=./tunableop_resultsTestBench.csv PYTORCH_TUNABLEOP_RECORD_UNTUNED=0 TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 PYTORCH_TUNABLEOP_VERBOSE=1 FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE" FLASH_ATTENTION_TRITON_AMD_AUTOTUNE="TRUE" MIOPEN_FIND_MODE=FAST
``` 
(ROCBLAS_VERBOSE_HIPBLASLT_ERROR=1 spams a lot of these: "hipBLASLt error: algo not supported.", omitted)
It produces this result:

```python
2.9.0.dev20250705+rocm6.4
version.cuda: None
AMD Radeon RX 9070 XT
_CudaDeviceProperties(name='AMD Radeon RX 9070 XT', major=12, minor=0, gcnArchName='gfx1201', total_memory=16304MB, multi_processor_count=32, uuid=34343130-6635-6462-3464-313035313064, pci_bus_id=9, pci_device_id=0, pci_domain_id=0, L2_cache_size=8MB)
device: cuda
reading tuning results from ./tunableop_resultsTestBench0.csv
could not open ./tunableop_resultsTestBench0.csv for reading tuning results
hipBLASLt error: algo not supported.
This message will be only be displayed once, unless the ROCBLAS_VERBOSE_HIPBLASLT_ERROR environment variable is set.
lossInit: tensor(0.7307, device='cuda:0', grad_fn=<MseLossBackward0>)
lossFinl: tensor(0.0289, device='cuda:0', grad_fn=<MseLossBackward0>)
device: cuda  time: 34.1846    nBatch: 100000  nEpoch: 1000
``` 

Subsequent run:

```python
2.9.0.dev20250705+rocm6.4
version.cuda: None
AMD Radeon RX 9070 XT
_CudaDeviceProperties(name='AMD Radeon RX 9070 XT', major=12, minor=0, gcnArchName='gfx1201', total_memory=16304MB, multi_processor_count=32, uuid=34343130-6635-6462-3464-313035313064, pci_bus_id=9, pci_device_id=0, pci_domain_id=0, L2_cache_size=8MB)
device: cuda
reading tuning results from ./tunableop_resultsTestBench0.csv
Validator PT_VERSION=2.9.0
Validator ROCM_VERSION=6.4.1.0-83-69b59e5
Validator HIPBLASLT_VERSION=1201-4d62e135
Validator GCN_ARCH_NAME=gfx1201
Validator ROCBLAS_VERSION=4.4.0.80e5394d
ROCBLAS_VERSION validation: expect 4.4.0.80e5394d to match 4.4.0.80e5394d
GCN_ARCH_NAME validation: expect gfx1201 to match gfx1201
HIPBLASLT_VERSION validation: expect 1201-4d62e135 to match 1201-4d62e135
ROCM_VERSION validation: expect 6.4.1.0-83-69b59e5 to match 6.4.1.0-83-69b59e5
PT_VERSION validation: expect 2.9.0 to match 2.9.0
Loading results
lossInit: tensor(0.7307, device='cuda:0', grad_fn=<MseLossBackward0>)
lossFinl: tensor(0.0289, device='cuda:0', grad_fn=<MseLossBackward0>)
device: cuda  time: 29.4553    nBatch: 100000  nEpoch: 1000

``` 

Not sure if this is of any help, but I use this setup with SD.Next and I get up to 60% better performance than stock install.

List of pip installed packages and tuned file  attached

[tunableop_resultsTestBench0.csv](https://github.com/user-attachments/files/21332018/tunableop_resultsTestBench0.csv)

[package list.txt](https://github.com/user-attachments/files/21332010/package.list.txt)



---

### 评论 #7 — relaxis (2025-07-21T19:28:08Z)

A solution to this would be much appreciated. 

---

### 评论 #8 — octaveoclx (2025-07-22T02:58:20Z)

@NTFSynergy Thank you!
Meanwhile, dear AMD team please keep investigating for Intel(R) Arc™ A770 is around 20s while 4060ti is similar. I guess this would be a great performance improvement for Radeon if the root of this problem is eliminated. I also have other cases where AMD cards are expected to perform way more better. 

---

### 评论 #9 — schung-amd (2025-07-22T17:22:31Z)

After playing around with the environment variables suggested by @NTFSynergy, the pytorch tunable ops seem mandatory to get good performance in this benchmark on Radeon cards. We do have some guidance on this, for example https://rocm.blogs.amd.com/artificial-intelligence/pytorch-tunableop/README.html and https://rocm.blogs.amd.com/artificial-intelligence/gemm_blog/README.html, but this should probably be more visible if it gives such a large performance boost. I'll need to look into why the performance gap is so large and whether we can improve the out-of-the-box GEMM performance on Radeon cards, as ideally users should not have to run the pytorch tuning themselves for every GEMM-heavy application.

This seems to be specifically bad on the 9070; with a 7900XTX, `PYTORCH_TUNABLEOP_ENABLED=1` reduces the execution time from ~50s to 13s after the first run, while on the 9070 I'm only seeing a speedup to around 30s (in agreement with what @NTFSynergy reports). I've heard that we may have some improvements on this end coming in ROCm 7.0, but will need to do some testing to see if any progress has been made in our internal builds.

For now, using the pytorch tunable ops should give you acceptable performance on the 7900XTX. I haven't tried this on other hardware yet, so if you run into other AMD cards with poor performance even with tunable ops enabled please report them so we have more data points.

---

### 评论 #10 — relaxis (2025-07-22T17:33:49Z)

I would normally agree with you but for image or video generation
PYTORCH_TUNABLEP_ENABLED=1 caches weights between generations, which means
if you load and unload loras then the image becomes ugly pretty fast.

On Tue, Jul 22, 2025 at 7:22 PM schung-amd ***@***.***> wrote:

> *schung-amd* left a comment (ROCm/ROCm#5040)
> <https://github.com/ROCm/ROCm/issues/5040#issuecomment-3103959663>
>
> After playing around with the environment variables suggested by
> @NTFSynergy <https://github.com/NTFSynergy>, the pytorch tunable ops seem
> mandatory to get good performance in this benchmark on Radeon cards. We do
> have some guidance on this, for example
> https://rocm.blogs.amd.com/artificial-intelligence/pytorch-tunableop/README.html
> and
> https://rocm.blogs.amd.com/artificial-intelligence/gemm_blog/README.html,
> but this should probably be more visible if it gives such a large
> performance boost. I'll need to look into why the performance gap is so
> large and whether we can improve the out-of-the-box GEMM performance on
> Radeon cards, as ideally users should not have to run the pytorch tuning
> themselves for every GEMM-heavy application.
>
> This seems to be specifically bad on the 9070; with a 7900XTX,
> PYTORCH_TUNABLEOP_ENABLED=1 reduces the execution time from ~50s to 13s
> after the first run, while on the 9070 I'm only seeing a speedup to around
> 30s (in agreement with what @NTFSynergy <https://github.com/NTFSynergy>
> reports). I've heard that we may have some improvements on this end coming
> in ROCm 7.0, but will need to do some testing to see if any progress has
> been made in our internal builds.
>
> For now, using the pytorch tunable ops should give you acceptable
> performance on the 7900XTX. I haven't tried this on other hardware yet, so
> if you run into other AMD cards with poor performance even with tunable ops
> enabled please report them so we have more data points.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5040#issuecomment-3103959663>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/ABK3FJCW2O65SYQULKHRCWT3JZXO3AVCNFSM6AAAAACBPEBXYKVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTCMBTHE2TSNRWGM>
> .
> You are receiving this because you commented.Message ID:
> ***@***.***>
>


---

### 评论 #11 — schung-amd (2025-07-22T17:59:34Z)

@relaxis IMO that could/should be a separate issue, while the need for `PYTORCH_TUNABLEOP_ENABLED=1` is rooted in poorly performing out-of-the-box GEMM kernels there may be other ways for us to help with that specific workflow. I'd recommend submitting a new issue with an example and a reproducer if possible. I think even if out-of-the-box performance becomes acceptable we would still be interested in making tunableops compatible with that workflow.

---

### 评论 #12 — relaxis (2025-07-22T19:36:58Z)

Perhaps later, there is no real way to debug or log what happens inside an
AI model running in comfyui and the behaviors of models don’t throw errors,
they have to be observed. I’ll write one up anyway if you want.

On Tue, 22 Jul 2025 at 19:59, schung-amd ***@***.***> wrote:

> *schung-amd* left a comment (ROCm/ROCm#5040)
> <https://github.com/ROCm/ROCm/issues/5040#issuecomment-3104128581>
>
> @relaxis <https://github.com/relaxis> IMO that could/should be a separate
> issue, while the need for PYTORCH_TUNABLEOP_ENABLED=1 is rooted in poorly
> performing out-of-the-box GEMM kernels there may be other ways for us to
> help with that specific workflow. I'd recommend submitting a new issue with
> an example and a reproducer if possible. I think even if out-of-the-box
> performance becomes acceptable we would still be interested in making
> tunableops compatible with that workflow.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5040#issuecomment-3104128581>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/ABK3FJDSM7L62RIO7YBDWJT3JZ3ZXAVCNFSM6AAAAACBPEBXYKVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTCMBUGEZDQNJYGE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #13 — schung-amd (2025-07-22T19:53:08Z)

That would be helpful if possible, we may be able to provide assistance regardless of the outcome of this issue. There may also be relevant info in a similar issue to this one opened for ComfyUI performance on the 9070 (https://github.com/ROCm/ROCm/issues/4846), although I don't think those users are reloading LORAs and so might not run into the issues you're seeing with tunableop enabled.

---
