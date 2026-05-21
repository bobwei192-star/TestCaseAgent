# [Issue]: Jax example fails with wheel from PyPI, but not with docker container

> **Issue #4311**
> **状态**: closed
> **创建时间**: 2025-01-29T10:11:21Z
> **更新时间**: 2025-02-12T09:18:17Z
> **关闭时间**: 2025-02-07T19:50:16Z
> **作者**: ffrancesco94
> **标签**: Under Investigation, ROCm 6.0.0, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/4311

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

Upon running the [jax quickstart](https://jax.readthedocs.io/en/latest/quickstart.html) tutorial, I get an XLA-related error in the `batched_apply_matrix()` function (I'm attaching a [minimal example](https://github.com/user-attachments/files/18585609/jax_example.txt) to the post), with the following stacktrace:

```
F0129 11:09:12.654758   18620 stream_executor_util.cc:515] Non-OK-status: kernel->Launch(se::ThreadDim(threads_per_block, 1, 1), se::BlockDim(blocks_per_grid, 1, 1), stream, buffer, host_buffer_bytes, static_cast<int64_t>(buffer.size()))
Status: INTERNAL: Failed to launch ROCm kernel: RepeatBufferKernel with block dimensions: 256x1x1: hipError_t(303)
*** Check failure stack trace: ***
    @     0x14dea86e8d54  absl::lts_20230802::log_internal::LogMessage::SendToLog()
    @     0x14dea86e86f4  absl::lts_20230802::log_internal::LogMessage::Flush()
    @     0x14dea86e91b9  absl::lts_20230802::log_internal::LogMessageFatal::~LogMessageFatal()
    @     0x14dea5055837  xla::gpu::InitializeTypedBuffer<>()
    @     0x14dea50500af  xla::primitive_util::FloatingPointTypeSwitch<>()
    @     0x14dea504e4c3  xla::gpu::InitializeBuffer()
    @     0x14dea504a634  stream_executor::RedzoneAllocator::CreateBuffer()
    @     0x14dea3957536  xla::gpu::RedzoneBuffers::CreateInputs()
    @     0x14dea39571df  xla::gpu::RedzoneBuffers::FromInstruction()
    @     0x14dea3947b6a  xla::gpu::GemmFusionAutotunerImpl::MeasurePerformance()
    @     0x14dea3948ba7  xla::gpu::GemmFusionAutotunerImpl::Profile()
    @     0x14dea39496d9  xla::gpu::GemmFusionAutotunerImpl::Autotune()
    @     0x14dea394c29b  xla::gpu::GemmFusionAutotuner::Run()
    @     0x14dea3962abf  xla::HloPassPipeline::RunHelper()
    @     0x14dea395fd15  xla::HloPassPipeline::RunPassesInternal<>()
    @     0x14dea395f66a  xla::HloPassPipeline::Run()
    @     0x14dea02554ee  xla::gpu::GpuCompiler::OptimizeHloPostLayoutAssignment()
    @     0x14dea0247ab1  xla::gpu::AMDGPUCompiler::OptimizeHloPostLayoutAssignment()
    @     0x14dea0250644  xla::gpu::GpuCompiler::OptimizeHloModule()
    @     0x14dea02591c2  xla::gpu::GpuCompiler::RunHloPasses()
    @     0x14dea0230a6f  xla::Service::BuildExecutable()
    @     0x14dea01a9187  xla::LocalService::CompileExecutables()
    @     0x14dea01a3bf4  xla::LocalClient::Compile()
    @     0x14dea01450fb  xla::PjRtStreamExecutorClient::CompileInternal()
    @     0x14dea01463d0  xla::PjRtStreamExecutorClient::Compile()
    @     0x14dea00b244a  std::__detail::__variant::__gen_vtable_impl<>::__visit_invoke()
    @     0x14dea00a1ddc  pjrt::PJRT_Client_Compile()
    @     0x14e210a0676d  xla::InitializeArgsAndCompile()
    @     0x14e210a06e9e  xla::PjRtCApiClient::Compile()
    @     0x14e218458f38  xla::ifrt::PjRtLoadedExecutable::Create()
    @     0x14e218463010  xla::ifrt::PjRtCompiler::Compile()
    @     0x14e2172e4cff  xla::PyClient::CompileIfrtProgram()
    @     0x14e2172e595b  xla::PyClient::Compile()
    @     0x14e2172eca26  nanobind::detail::func_create<>()::{lambda()#1}::__invoke()
    @     0x14e218430ec8  nanobind::detail::nb_func_vectorcall_complex()
    @     0x14e233ae882c  nanobind::detail::nb_bound_method_vectorcall()
    @     0x14e2345e6d33  PyObject_Vectorcall

[18620] signal 6 (-6): Aborted
in expression starting at none:0
gsignal at /lib64/libc.so.6 (unknown line)
abort at /lib64/libc.so.6 (unknown line)
```

And many more mangled names from `xla_rocm_plugin.so`. The code also fails if I pull an official ROCm container from DockerHub and install jax with `pip3 install jax[rocm]` according to [AMD instructions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/jax-install.html#using-a-rocm-base-docker-image-and-installing-jax), but runs successfully if I use the rocm-jax container from DockerHub. I believe there is an issue with the PyPI wheels (see below).

### Operating System

Manjaro Linux

### CPU

AMD Ryzen 5 7600 with Radeon Graphics

### GPU

AMD Radeon RX6950XT, MI Instinct 250X

### ROCm Version

ROCm 6.0.0, ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

1. Install ROCm and the jax pip wheel with `pip install jax[rocm]`
2. Realise that the PyPI wheel does not include any `[rocm]` extensions, so manual installation of `jax-rocm60-plugin` and `jax-rocm60-pjrt` is needed.
3. Run the attached MWE based on the jax quick start guide as `LLVM_PATH=/opt/rocm/llvm ROCM_PATH=/opt/rocm python jax_example;py`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

There must be something wrong with the wheels published on PyPI since the `rocm` extensions aren't even provided and the `plugin` and `pjrt` packages need manual installation, both on bare-metal and in the ROCm Docker containers. 

---

## 评论 (14 条)

### 评论 #1 — ppanchad-amd (2025-01-29T14:35:00Z)

Hi @ffrancesco94. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-01-30T19:05:10Z)

@ffrancesco94 Thanks for reporting the issue! It has been reproduced on our test system; we will begin investigation shortly. 

---

### 评论 #3 — tcgu-amd (2025-01-30T20:11:56Z)

Hi @ffrancesco94, seems like this is a PyPI versioning issue -- currently, the [rocm] extra is only supported on Jax version 0.5.0 (latest), with a dependency on jax-rocm60-plugin==0.5.0 and jax-rocm60-pjrt==0.5.0. However, the latest version of jax-rocm60-plugin and jax-rocm60-pjrt is only at 0.4.35. 

We will work on fixing this issue. Meanwhile, please use the work around of 

```
pip install jax==0.4.35 jax-rocm60-pjrt==0.4.35 jax-rocm60-plugin==0.4.35
```
Thanks!

Edit: fixed  jax-rocm60-lib ->  jax-rocm60-plugin

---

### 评论 #4 — ffrancesco94 (2025-01-30T20:24:47Z)

Hi! 
I tried your suggested workaround, but `jax-rocm60-lib` does not seem to exist on PyPI. I did install manually the `jax-rocm60-pjrt` and `jax-rocm60-plugin` packages, which led me to the stacktrace in OP. 

---

### 评论 #5 — tcgu-amd (2025-01-30T21:11:13Z)

> Hi! I tried your suggested workaround, but `jax-rocm60-lib` does not seem to exist on PyPI. I did install manually the `jax-rocm60-pjrt` and `jax-rocm60-plugin` packages, which led me to the stacktrace in OP.

@ffrancesco94, sorry I messed up the naming....it should have been jax-rocm60-plugin -- please ignore jax-rocm60-lib. 

---

### 评论 #6 — tcgu-amd (2025-01-30T21:26:26Z)

@ffrancesco94, would you be able to run your reproducer with AMD_LOG_LEVEL=5 and show me the logs? Thanks

---

### 评论 #7 — ffrancesco94 (2025-01-30T21:44:05Z)

I think it's too big for a github comment so it's attached [here](https://github.com/user-attachments/files/18609056/log.log). Thanks!

---

### 评论 #8 — Ruturaj4 (2025-02-07T16:26:45Z)

@ffrancesco94 what is the output of `python -c "import jax; print(jax.devices())"`

also please give us the output of `pip list | grep jax`

---

### 评论 #9 — ffrancesco94 (2025-02-07T18:44:10Z)

```
LLVM_PATH=/opt/rocm/llvm ROCM_PATH=/opt/rocm python -c "import jax; print(jax.devices())"
[RocmDevice(id=0)]
```

```
 python3 -m pip list | grep jax 
jax               0.4.35
jax-rocm60-pjrt   0.4.35
jax-rocm60-plugin 0.4.35
jaxlib            0.4.35

[notice] A new release of pip is available: 24.0 -> 25.0
[notice] To update, run: pip3 install --upgrade pip
```


---

### 评论 #10 — ffrancesco94 (2025-02-07T18:50:40Z)

EDIT: I noticed that adding manually the `jax-rocm60-pjrt` and `jax-rocm60-plugin` to the cluster environment with an MI250X makes my reproducer not fail, so the main issue for that is fixing the pip package. As for my personal RX6950XT, I just tried to spoof the architecture of my GPU by using `HSA_GFX_OVERRIDE_VERSION=10.3.0` and the reproducer does not fail. It is quite interesting that if I use the Docker image I do not need to set the `HSA_GFX_OVERRIDE_VERSION` variable, whereas if I install things from pip I do. What might be the underlying issue?
If there is a way for me to contribute to the documentation and write about this somewhere where people can find it, I'd be very happy to. Otherwise the issue from my side can be closed. 


---

### 评论 #11 — tcgu-amd (2025-02-07T19:50:09Z)

> `LLVM_PATH=/opt/rocm/llvm ROCM_PATH=/opt/rocm python -c "import jax; print(jax.devices())"
[RocmDevice(id=0)]`

It appears that for some reason, Jax was not able to find the GPU, which is bit odd. It can be something in the system/docker configuration or library linkage. Is there a reason why you had to manually specify the ROCM/LLVM_PATH environment variables? 

>EDIT: I noticed that adding manually the jax-rocm60-pjrt and jax-rocm60-plugin to the cluster environment with an MI250X makes my reproducer not fail, so the main issue for that is fixing the pip package. As for my personal RX6950XT, I just tried to spoof the architecture of my GPU by using HSA_GFX_OVERRIDE_VERSION=10.3.0 and the reproducer does not fail. It is quite interesting that if I use the Docker image I do not need to set the HSA_GFX_OVERRIDE_VERSION variable, whereas if I install things from pip I do. What might be the underlying issue?
If there is a way for me to contribute to the documentation and write about this somewhere where people can find it, I'd be very happy to. Otherwise the issue from my side can be closed.

The pip packaging will be fixed soon in an update. Unfortunately, we do not keep official documentation of HSA_FGX_OVERRIDE_VERSION because technically this env variable is not needed on officially supported architectures. For now, I guess this post will serve as documenation.

I will be closing this issue for now, but please feel free to continue to update it for any additional questions/feedbacks.

Thanks!

---

### 评论 #12 — ffrancesco94 (2025-02-07T20:11:39Z)

Ok!

> It can be something in the system/docker configuration or library linkage. Is there a reason why you had to manually specify the ROCM/LLVM_PATH environment variables?

If I don't, it complains about some opencl .so files that can't be found and not finding ld.lld respectively (if I run it outside of the container). It is also needed if I use a rocm (non-jax) container and install jax there myself. 

---

### 评论 #13 — tcgu-amd (2025-02-07T20:22:39Z)

> Ok!
> 
> > It can be something in the system/docker configuration or library linkage. Is there a reason why you had to manually specify the ROCM/LLVM_PATH environment variables?
> 
> If I don't, it complains about some opencl .so files that can't be found and not finding ld.lld respectively (if I run it outside of the container). It is also needed if I use a rocm (non-jax) container and install jax there myself.

Interesting. I didn't have that issue when trying to use the `rocm/dev-ubuntu-22.04:6.3-complete`. Were you able to run `rocminfo` on it?

---

### 评论 #14 — ffrancesco94 (2025-02-12T09:18:15Z)

Hi,
I think I may have used `latest` and not one ending with `-complete`, maybe that was the difference. Thank you for all the help!

---
