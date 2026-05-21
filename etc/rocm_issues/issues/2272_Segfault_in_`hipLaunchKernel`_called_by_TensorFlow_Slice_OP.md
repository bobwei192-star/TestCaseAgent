# Segfault in `hipLaunchKernel` called by TensorFlow Slice OP

> **Issue #2272**
> **状态**: closed
> **创建时间**: 2023-06-26T18:48:15Z
> **更新时间**: 2024-03-31T14:11:22Z
> **关闭时间**: 2024-03-31T14:11:22Z
> **作者**: njzjz
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2272

## 描述

ROCm 5.3.0

I got a Segmentation fault when I ran a complex program that finally used tensorflow-rocm. I used GDB to debug it, and it looks like the Segmentation fault occurred inside `hipLaunchKernel` and is called by the Eigen kernel of the TensorFlow Slice OP.

Below is the GDB traceback:
```
Thread 22 "lmp" received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7ffd4affd700 (LWP 1587920)]
__memmove_avx_unaligned_erms () at ../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:440
440     ../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S: No such file or directory.
(gdb) bt
#0  __memmove_avx_unaligned_erms () at ../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:440
#1  0x00007fffb189573d in ?? () from /mnt/beegfs/software/rocm/rocm-5.3.0/lib/libamdhip64.so.5
#2  0x00007fffb1895df4 in ?? () from /mnt/beegfs/software/rocm/rocm-5.3.0/lib/libamdhip64.so.5
#3  0x00007fffb1867c04 in ?? () from /mnt/beegfs/software/rocm/rocm-5.3.0/lib/libamdhip64.so.5
#4  0x00007fffb175cecf in ?? () from /mnt/beegfs/software/rocm/rocm-5.3.0/lib/libamdhip64.so.5
#5  0x00007fffb1787f8d in ?? () from /mnt/beegfs/software/rocm/rocm-5.3.0/lib/libamdhip64.so.5
#6  0x00007fffb1752b56 in ?? () from /mnt/beegfs/software/rocm/rocm-5.3.0/lib/libamdhip64.so.5
#7  0x00007fffb175860b in hipLaunchKernel () from /mnt/beegfs/software/rocm/rocm-5.3.0/lib/libamdhip64.so.5
#8  0x00007fffbea10daf in Eigen::internal::TensorExecutor<Eigen::TensorAssignOp<Eigen::TensorMap<Eigen::Tensor<float, 2, 1, int>, 16, Eigen::MakePointer>, Eigen::TensorSlicingOp<Eigen::DSizes<int, 2> const, Eigen::DSizes<int, 2> const, Eigen::TensorMap<Eigen::Tensor<float const, 2, 1, int>, 16, Eigen::MakePointer> const> const> const, Eigen::GpuDevice, false, (Eigen::internal::TiledEvaluation)1>::run(Eigen::TensorAssignOp<Eigen::TensorMap<Eigen::Tensor<float, 2, 1, int>, 16, Eigen::MakePointer>, Eigen::TensorSlicingOp<Eigen::DSizes<int, 2> const, Eigen::DSizes<int, 2> const, Eigen::TensorMap<Eigen::Tensor<float const, 2, 1, int>, 16, Eigen::MakePointer> const> const> const&, Eigen::GpuDevice const&) ()
   from /mnt/beegfs/home/jzzeng/anaconda3/lib/python3.9/site-packages/tensorflow/python/_pywrap_tensorflow_internal.so
#9  0x00007fffbea108e8 in void tensorflow::internal::MaybeWith32BitIndexingImpl<Eigen::GpuDevice>::operator()<tensorflow::functor::Slice<Eigen::GpuDevice, float, 2>::operator()(Eigen::GpuDevice const&, Eigen::TensorMap<Eigen::Tensor<float, 2, 1, long>, 16, Eigen::MakePointer>, Eigen::TensorMap<Eigen::Tensor<float const, 2, 1, long>, 16, Eigen::MakePointer>, Eigen::DSizes<long, 2> const&, Eigen::DSizes<long, 2> const&)::{lambda(auto:1, auto:2, auto:3, auto:4)#1}, Eigen::TensorMap<Eigen::Tensor<float, 2, 1, long>, 16, Eigen::MakePointer>&, Eigen::TensorMap<Eigen::Tensor<float const, 2, 1, long>, 16, Eigen::MakePointer>&, Eigen::DSizes<long, 2> const&, Eigen::DSizes<long, 2> const&>(tensorflow::functor::Slice<Eigen::GpuDevice, float, 2>::operator()(Eigen::GpuDevice const&, Eigen::TensorMap<Eigen::Tensor<float, 2, 1, long>, 16, Eigen::MakePointer>, Eigen::TensorMap<Eigen::Tensor<float const, 2, 1, long>, 16, Eigen::MakePointer>, Eigen::DSizes<long, 2> const&, Eigen::DSizes<long, 2> const&)::{lambda(auto:1, auto:2, auto:3, auto:4)#1}, Eigen::TensorMap<Eigen::Tensor<float, 2, 1, long>, 16, Eigen::MakePointer>&, Eigen::TensorMap<Eigen::Tensor<float const, 2, 1, long>, 16, Eigen::MakePointer>&, Eigen::DSizes<long, 2> const&, Eigen::DSizes<long, 2> const&) const ()
   from /mnt/beegfs/home/jzzeng/anaconda3/lib/python3.9/site-packages/tensorflow/python/_pywrap_tensorflow_internal.so
#10 0x00007fffbe9f1059 in tensorflow::functor::Slice<Eigen::GpuDevice, float, 2>::operator()(Eigen::GpuDevice const&, Eigen::TensorMap<Eigen::Tensor<float, 2, 1, long>, 16, Eigen::MakePointer>, Eigen::TensorMap<Eigen::Tensor<float const, 2, 1, long>, 16, Eigen::MakePointer>, Eigen::DSizes<long, 2> const&, Eigen::DSizes<long, 2> const&) ()
   from /mnt/beegfs/home/jzzeng/anaconda3/lib/python3.9/site-packages/tensorflow/python/_pywrap_tensorflow_internal.so
#11 0x00007fffbe95ee20 in tensorflow::(anonymous namespace)::SliceOp<Eigen::GpuDevice, float>::Compute(tensorflow::OpKernelContext*) ()
   from /mnt/beegfs/home/jzzeng/anaconda3/lib/python3.9/site-packages/tensorflow/python/_pywrap_tensorflow_internal.so
#12 0x00007fffb492fe3a in tensorflow::BaseGPUDevice::Compute(tensorflow::OpKernel*, tensorflow::OpKernelContext*) ()
   from /mnt/beegfs/home/jzzeng/anaconda3/lib/python3.9/site-packages/tensorflow/libtensorflow_framework.so.2
#13 0x00007fffb4884c90 in tensorflow::(anonymous namespace)::ExecutorState<tensorflow::PropagatorState>::Process(tensorflow::PropagatorState::TaggedNode, long) () from /mnt/beegfs/home/jzzeng/anaconda3/lib/python3.9/site-packages/tensorflow/libtensorflow_framework.so.2
#14 0x00007fffb4886c58 in std::_Function_handler<void (), tensorflow::(anonymous namespace)::ExecutorState<tensorflow::PropagatorState>::RunTask<tensorflow::(anonymous namespace)::ExecutorState<tensorflow::PropagatorState>::ScheduleReady(absl::lts_20220623::InlinedVector<tensorflow::PropagatorState::TaggedNode, 8ul, std::allocator<tensorflow::PropagatorState::TaggedNode> >*, tensorflow::PropagatorState::TaggedNodeReadyQueue*)::{lambda()#3}>(tensorflow::(anonymous namespace)::ExecutorState<tensorflow::PropagatorState>::ScheduleReady(absl::lts_20220623::InlinedVector<tensorflow::PropagatorState::TaggedNode, 8ul, std::allocator<tensorflow::PropagatorState::TaggedNode> >*, tensorflow::PropagatorState::TaggedNodeReadyQueue*)::{lambda()#3}&&, int)::{lambda()#1}>::_M_invoke(std::_Any_data const&) ()
   from /mnt/beegfs/home/jzzeng/anaconda3/lib/python3.9/site-packages/tensorflow/libtensorflow_framework.so.2
#15 0x00007fffcce99485 in Eigen::ThreadPoolTempl<tsl::thread::EigenEnvironment>::WorkerLoop(int) ()
   from /mnt/beegfs/home/jzzeng/anaconda3/lib/python3.9/site-packages/tensorflow/python/_pywrap_tensorflow_internal.so
#16 0x00007fffcce96733 in std::_Function_handler<void (), tsl::thread::EigenEnvironment::CreateThread(std::function<void ()>)::{lambda()#1}>::_M_invoke(std::_Any_data const&) () from /mnt/beegfs/home/jzzeng/anaconda3/lib/python3.9/site-packages/tensorflow/python/_pywrap_tensorflow_internal.so
#17 0x00007fffb470968c in tsl::(anonymous namespace)::PThread::ThreadFn(void*) () from /mnt/beegfs/home/jzzeng/anaconda3/lib/python3.9/site-packages/tensorflow/libtensorflow_framework.so.2
#18 0x00007ffff523e609 in start_thread (arg=<optimized out>) at pthread_create.c:477
#19 0x00007ffff4de4133 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:95
```


Here is the Tensorflow log. It shows that the error occurred when the Slice OP was executed.
```
2023-06-26 20:36:51.766377: I tensorflow/core/common_runtime/executor.cc:883] Synchronous kernel done: 634 step 8 {{node filter_type_4/strided_slice_2}} = StridedSlice[Index=DT_INT32, T=DT_INT32, _XlaHasReferenceVars=false, begin_mask=0, ellipsis_mask=0, end_mask=0, new_axis_mask=0, shrink_axis_mask=1, _device="/job:localhost/replica:0/task:0/device:GPU:0"](gradients/filter_type_4/Reshape_20_grad/Shape, strided_slice_83/stack, strided_slice_86/stack, strided_slice_86/stack) device: /job:localhost/replica:0/task:0/device:GPU:0
2023-06-26 20:36:51.766384: I tensorflow/core/common_runtime/executor.cc:826] Process node: 635 step 8 {{node gradients/filter_type_4/Slice_5_grad/Shape_1}} = Shape[T=DT_FLOAT, _XlaHasReferenceVars=false, out_type=DT_INT32, _device="/job:localhost/replica:0/task:0/device:GPU:0"](filter_type_4/Reshape_14) device: /job:localhost/replica:0/task:0/device:GPU:0
2023-06-26 20:36:51.766388: I tensorflow/core/common_runtime/gpu/gpu_device.cc:660] GpuDevice::ComputeHelper gradients/filter_type_4/Slice_5_grad/Shape_1 op Shape on GPU 0 stream[0]
2023-06-26 20:36:51.766400: I tensorflow/core/framework/log_memory.cc:34] __LOG_MEMORY__ MemoryLogTensorAllocation { step_id: 8 kernel_name: "gradients/filter_type_4/Slice_5_grad/Shape_1" tensor { dtype: DT_INT32 shape { dim { size: 2 } } allocation_description { requested_bytes: 8 allocated_bytes: 8 allocator_name: "cpu" allocation_id: 32212 has_single_reference: true ptr: 140433689570112 } } }
2023-06-26 20:36:51.766404: I tensorflow/core/common_runtime/gpu/gpu_device.cc:697] GpuDevice::ComputeHelper scheduled gradients/filter_type_4/Slice_5_grad/Shape_1 op Shape on GPU 0 stream[0]
2023-06-26 20:36:51.766414: I tensorflow/core/framework/log_memory.cc:34] __LOG_MEMORY__ MemoryLogTensorOutput { step_id: 8 kernel_name: "gradients/filter_type_4/Slice_5_grad/Shape_1" tensor { dtype: DT_INT32 shape { dim { size: 2 } } allocation_description { requested_bytes: 8 allocated_bytes: 8 allocator_name: "cpu" allocation_id: 32212 has_single_reference: true ptr: 140433689570112 } } }
2023-06-26 20:36:51.766420: I tensorflow/core/common_runtime/executor.cc:883] Synchronous kernel done: 635 step 8 {{node gradients/filter_type_4/Slice_5_grad/Shape_1}} = Shape[T=DT_FLOAT, _XlaHasReferenceVars=false, out_type=DT_INT32, _device="/job:localhost/replica:0/task:0/device:GPU:0"](filter_type_4/Reshape_14) device: /job:localhost/replica:0/task:0/device:GPU:0
2023-06-26 20:36:51.766427: I tensorflow/core/common_runtime/executor.cc:826] Process node: 636 step 8 {{node filter_type_4/Slice_5}} = Slice[Index=DT_INT32, T=DT_FLOAT, _XlaHasReferenceVars=false, _device="/job:localhost/replica:0/task:0/device:GPU:0"](filter_type_4/Reshape_14, Slice_6/begin, filter_type_0/Slice_1/size) device: /job:localhost/replica:0/task:0/device:GPU:0
2023-06-26 20:36:51.766431: I tensorflow/core/common_runtime/gpu/gpu_device.cc:660] GpuDevice::ComputeHelper filter_type_4/Slice_5 op Slice on GPU 0 stream[0]
2023-06-26 20:36:51.766436: I tensorflow/tsl/framework/bfc_allocator.cc:260] AllocateRaw GPU_0_bfc  2053376
2023-06-26 20:36:51.766441: I tensorflow/tsl/framework/bfc_allocator.cc:307] AllocateRaw GPU_0_bfc  2053376 0x7fb912c85100
2023-06-26 20:36:51.766452: I tensorflow/core/framework/log_memory.cc:34] __LOG_MEMORY__ MemoryLogTensorAllocation { step_id: 8 kernel_name: "filter_type_4/Slice_5" tensor { dtype: DT_FLOAT shape { dim { size: 513344 } dim { size: 1 } } allocation_description { requested_bytes: 2053376 allocated_bytes: 2053376 allocator_name: "GPU_0_bfc" allocation_id: 362 has_single_reference: true ptr: 140432860795136 } } }
```


---

## 评论 (4 条)

### 评论 #1 — jayfurmanek (2023-06-28T13:52:13Z)

Hi thanks for the report!

Can you let us know some additional information so we can try to recreate:
 - which version of Tensorflow
 - which GPU
 - What are you running here? Can you post a small script that recreates this behaviour?
 

---

### 评论 #2 — njzjz (2023-06-28T20:44:08Z)

Thanks!

TensorFlow version: `tensorflow-rocm 2.11.1.550` installed using `pip install tensorflow-rocm`
GPU: both MI210 and MI250 have this behavior. I use the AMD Cloud Platform and can provide you with the account for an existing environment for recreating.

The thing to run is a bit complex. I am a developer of the [DeePMD-kit package](https://github.com/deepmodeling/deepmd-kit), which utilizes both TensorFlow and [LAMMPS](https://github.com/lammps/lammps) to perform molecular dynamics simulations. (Recently we have [a paper on arxiv](https://arxiv.org/abs/2304.09409) to describe how it works.) I want to test how many atoms a GPU card can simulate at maximum. When the number of atoms is small, everything is OK. However, the seg fault happens when the number of atoms increases, saying 40000 atoms. (by the way, CUDA works fine with the same thing)

I tried to create a script but failed to reproduce the seg fault. But I guess the reason is that some integers might overflow, considering it works fine when the input is small.

[frozen_model.pbtxt.tar.gz](https://github.com/RadeonOpenCompute/ROCm/files/11899815/frozen_model.pbtxt.tar.gz)

Here I upload `frozen_model.pbtxt` to show what the computing graph looks like. But note that it contains customized OPs, so it cannot run without installing our packages.

---

### 评论 #3 — nartmada (2024-03-16T02:38:47Z)

Hi @njzjz, apologies for not following up.  Do you still see the issue with latest ROCm 6.0.2?  Thanks.

---

### 评论 #4 — nartmada (2024-03-31T14:11:22Z)

Closing the ticket.  @njzjz, please re-open if you still see the issue with latest ROCm 6.0.2.  Thanks.

---
