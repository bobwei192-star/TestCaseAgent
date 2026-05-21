# [Issue]: Segmentation fault when training models using any TensorFlow version on R9700

> **Issue #5864**
> **状态**: open
> **创建时间**: 2026-01-17T02:46:04Z
> **更新时间**: 2026-03-18T12:48:06Z
> **作者**: aloheac
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5864

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- amd-nicknick

## 描述

### Problem Description

I consistently get a segmentation error when training TensorFlow models on an AMD Radeon AI PRO R9700 under Linux. This may be related to issue #5718, but I additionally get a segmentation fault with both TensorFlow versions 2.19.1 and 2.18.1. This occurs on bare metal in addition to under Docker. I have also attempted a fresh install of Ubuntu Server 24.04 and ROCm 7.1.1 with the same result. ROCm 6.4.3 was also tried. I have not yet found a combination that avoids this issue.



### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen Threadripper 3960X

### GPU

AMD Radeon AI PRO R9700

### ROCm Version

ROCm 7.1.1

### ROCm Component

HIP

### Steps to Reproduce

This issue can be reproduced simply by running the MNIST example posted at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/tensorflow-install.html and increasing the number of epochs to 100. The failure point happens within the same epoch for a given session. This happens for other models as well.

```
import tensorflow as tf
print("TensorFlow version:", tf.__version__)
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])
predictions = model(x_train[:1]).numpy()
tf.nn.softmax(predictions).numpy()
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
loss_fn(y_train[:1], predictions).numpy()
model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100)
model.evaluate(x_test,  y_test, verbose=2)
```

When running with gdb, the seg fault originates from libamdhip64.so.7. The full stack trace and logs are in the additional information section.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module version 6.16.6 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.14
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen Threadripper 3960X 24-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen Threadripper 3960X 24-Core Processor
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    0                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3800                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    49155112(0x2ee0c28) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    49155112(0x2ee0c28) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    49155112(0x2ee0c28) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    49155112(0x2ee0c28) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-11ac8a4bc02c5165               
  Marketing Name:          AMD Radeon AI PRO R9700            
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30033(0x7551)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   8960                               
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          32(0x20)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    1024(0x400)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 108                                
  SDMA engine uCode::      662                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31309824(0x1ddc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1201         
      Machine Models:          HSA_MACHINE_MODEL_LARGE            
      Profiles:                HSA_PROFILE_BASE                   
      Default Rounding Mode:   NEAR                               
      Default Rounding Mode:   NEAR                               
      Fast f16:                TRUE                               
      Workgroup Max Size:      1024(0x400)                        
      Workgroup Max Size per Dimension:
        x                        1024(0x400)                        
        y                        1024(0x400)                        
        z                        1024(0x400)                        
      Grid Max Size:           4294967295(0xffffffff)             
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
      Machine Models:          HSA_MACHINE_MODEL_LARGE            
      Profiles:                HSA_PROFILE_BASE                   
      Default Rounding Mode:   NEAR                               
      Default Rounding Mode:   NEAR                               
      Fast f16:                TRUE                               
      Workgroup Max Size:      1024(0x400)                        
      Workgroup Max Size per Dimension:
        x                        1024(0x400)                        
        y                        1024(0x400)                        
        z                        1024(0x400)                        
      Grid Max Size:           4294967295(0xffffffff)             
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
*** Done *** 
```

### Additional Information

**gdb stack trace:**
```
Thread 149 "python3" received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7ffbc27fc6c0 (LWP 18258)]
0x00007ffff1e5136f in ?? () from /opt/rocm/lib/libamdhip64.so.7
(gdb) bt
#0  0x00007ffff1e5136f in ?? () from /opt/rocm/lib/libamdhip64.so.7
#1  0x00007ffff1e51f64 in ?? () from /opt/rocm/lib/libamdhip64.so.7
#2  0x00007ffff1ad2734 in ?? () from /opt/rocm/lib/libamdhip64.so.7
#3  0x00007ffff1ad06a2 in ?? () from /opt/rocm/lib/libamdhip64.so.7
#4  0x00007ffff1b0c5cd in ?? () from /opt/rocm/lib/libamdhip64.so.7
#5  0x00007ffff600d27b in stream_executor::gpu::RocmCommandBuffer::UpdateKernelNode(stream_executor::gpu::GpuCommandBuffer::GraphNodeHandleOpaque*, stream_executor::ThreadDim const&, stream_executor::BlockDim const&, stream_executor::Kernel const&, stream_executor::KernelArgsPackedArrayBase const&)
    () from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#6  0x00007ffff6012f26 in stream_executor::gpu::GpuCommandBuffer::LaunchWithPackedArgs(tsl::gtl::IntType<stream_executor::CommandBuffer::ExecutionScopeId_tag_, unsigned long>, stream_executor::ThreadDim const&, stream_executor::BlockDim const&, stream_executor::Kernel const&, stream_executor::KernelArgsPackedArrayBase const&) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#7  0x00007ffff60131b1 in stream_executor::gpu::GpuCommandBuffer::Launch(tsl::gtl::IntType<stream_executor::CommandBuffer::ExecutionScopeId_tag_, unsigned long>, stream_executor::ThreadDim const&, stream_executor::BlockDim const&, stream_executor::Kernel const&, stream_executor::KernelArgs const&)
    () from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#8  0x00007fffd273e5a2 in xla::gpu::LaunchCmd::Record(xla::gpu::Thunk::ExecuteParams const&, xla::gpu::CommandBufferCmd::RecordParams const&, stream_executor::CommandBuffer*) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#9  0x00007fffd273b656 in xla::gpu::CommandBufferCmdSequence::Record(xla::gpu::Thunk::ExecuteParams const&, xla::gpu::CommandBufferCmd::RecordParams const&, stream_executor::CommandBuffer*, xla::gpu::CommandBufferCmdSequence::RecordMode) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#10 0x00007fffd27381ff in xla::gpu::CommandBufferThunk::ExecuteOnStream(xla::gpu::Thunk::ExecuteParams const&) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#11 0x00007fffd38c479c in xla::gpu::SequentialThunk::ExecuteOnStream(xla::gpu::Thunk::ExecuteParams const&) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#12 0x00007fffd38becb4 in xla::gpu::(anonymous namespace)::ExecuteThunks(xla::DebugOptions const*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, xla::gpu::SequentialThunk&, xla::gpu::Thunk::ExecutableSource, xla::ServiceExecutableRunOptions const*, xla::gpu::BufferAllocations const&, bool, absl::lts_20230802::flat_hash_set<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long>, absl::lts_20230802::hash_internal::Hash<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long> >, std::equal_to<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long> >, std::allocator<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long> > > const&) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#13 0x00007fffd38bbd12 in xla::gpu::GpuExecutable::ExecuteAsyncOnStreamImpl(xla::ServiceExecutableRunOptions const*, std::variant<absl::lts_20230802::Span<xla::ShapedBuffer const* const>, absl::lts_20230802::Span<xla::ExecutionInput> >) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#14 0x00007fffd38ba70d in xla::gpu::GpuExecutable::ExecuteAsyncOnStream(xla::ServiceExecutableRunOptions const*, std::vector<xla::ExecutionInput, std::allocator<xla::ExecutionInput> >) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
--Type <RET> for more, q to quit, c to continue without paging--c
#15 0x00007fffdda784df in xla::Executable::ExecuteAsyncOnStreamWrapper(xla::ServiceExecutableRunOptions const*, std::vector<xla::ExecutionInput, std::allocator<xla::ExecutionInput> >) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#16 0x00007fffd455e8d9 in xla::LocalExecutable::RunAsync(absl::lts_20230802::Span<xla::Shape const* const>, std::vector<xla::ExecutionInput, std::allocator<xla::ExecutionInput> >, xla::ExecutableRunOptions) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#17 0x00007fffd455f01e in xla::LocalExecutable::RunAsync(std::vector<xla::ExecutionInput, std::allocator<xla::ExecutionInput> >, xla::ExecutableRunOptions) () from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#18 0x00007fffd3b49262 in tensorflow::(anonymous namespace)::RunExecutable(tensorflow::XlaPlatformInfo const&, tensorflow::XlaComputationLaunchContext const&, std::vector<xla::ExecutionInput, std::allocator<xla::ExecutionInput> >, xla::ExecutableRunOptions, xla::LocalExecutable*, tensorflow::OpKernelContext*, stream_executor::DeviceMemoryAllocator*) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#19 0x00007fffd3b54216 in std::_Function_handler<void (), tensorflow::XlaLocalLaunchBase::ComputeAsync(tensorflow::OpKernelContext*, std::function<void ()>)::$_1>::_M_invoke(std::_Any_data const&) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#20 0x00007fffd3b428b0 in tensorflow::XlaLocalLaunchBase::ComputeAsync(tensorflow::OpKernelContext*, std::function<void ()>) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#21 0x00007ffff504099b in tensorflow::BaseGPUDevice::ComputeAsync(tensorflow::AsyncOpKernel*, tensorflow::OpKernelContext*, std::function<void ()>)
    () from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#22 0x00007ffff514610b in tensorflow::(anonymous namespace)::ExecutorState<tensorflow::PropagatorState>::Process(tensorflow::PropagatorState::TaggedNode const&, long) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#23 0x00007ffff604b045 in Eigen::ThreadPoolTempl<tsl::thread::EigenEnvironment>::WorkerLoop(int) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#24 0x00007ffff604a211 in void std::__invoke_impl<void, tsl::thread::EigenEnvironment::CreateThread(std::function<void ()>)::{lambda()#1}&>(std::__invoke_other, tsl::thread::EigenEnvironment::CreateThread(std::function<void ()>)::{lambda()#1}&) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#25 0x00007ffff54d4cfa in tsl::(anonymous namespace)::PThread::ThreadFn(void*) ()
   from /home/loheac/Projects/complex/venv/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#26 0x00007ffff7c9caa4 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:447
#27 0x00007ffff7d29c6c in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:78
```

**Log emitted by ROCm with AMD_LOG_LEVEL=4 at the failure point:**
```
GB1_GRPM1_GRVW1_GSU1_GSUASB_GLS0_ISA000_IU1_K1_KLS_LBSPPA0_LBSPPB0_LPA0_LPB0_LDL1_LRVW1_LWPMn1_LDW0_FMA_MIAV0_MDA2_MO40_MMFSC_MKFGSU256_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR1_PLR1_PKA0_SIA1_SLW1_SS0_SU32_SUM0_SUS256_SCIUI1_SPO0_SRVW0_SSO0_SVW2_SNLL0_TSGRA0_TSGRB0_TT2_2_TLDS0_UMLDSA0_UMLDSB0_U64SL1_USFGRO0_VAW1_VS1_VW1_VWB1_VFLRP0_WSGRA0_WSGRB0_WS64_WG16_16_1_WGM8
:3:hip_graph.cpp            :1913: 32130193118 us: [pid:39416 tid: 0x71a40bfff6c0]  hipGraphExecKernelNodeSetParams ( 0x7198ca566060, 0x7198d6903100, 0x71a40bffa708 ) 
:4:rocvirtual.cpp           :792 : 32130193132 us: [pid:39416 tid: 0x71a40bfff6c0] Arg0:   = ptr:0x719bff2a0400 obj:[0x719bfaa00000-0x71a3bfe00000]
:4:rocvirtual.cpp           :792 : 32130193141 us: [pid:39416 tid: 0x71a40bfff6c0] Arg1:   = ptr:0x719bfd2a0400 obj:[0x719bfaa00000-0x71a3bfe00000]
:4:rocvirtual.cpp           :792 : 32130193150 us: [pid:39416 tid: 0x71a40bfff6c0] Arg2:   = ptr:0x719bfb18fa00 obj:[0x719bfaa00000-0x71a3bfe00000]
:4:rocvirtual.cpp           :792 : 32130193159 us: [pid:39416 tid: 0x71a40bfff6c0] Arg3:   = ptr:0x719c00cf4400 obj:[0x719bfaa00000-0x71a3bfe00000]
:4:rocvirtual.cpp           :792 : 32130193169 us: [pid:39416 tid: 0x71a40bfff6c0] Arg4:   = ptr:0x719bfe2a0400 obj:[0x719bfaa00000-0x71a3bfe00000]
:3:rocvirtual.cpp           :3503: 32130193178 us: [pid:39416 tid: 0x71a40bfff6c0] ShaderName : input_reduce_select_fusion_3
:3:hip_graph.cpp            :1931: 32130193186 us: [pid:39416 tid: 0x71a40bfff6c0] hipGraphExecKernelNodeSetParams: Returned hipSuccess : 
:3:hip_graph.cpp            :1913: 32130193197 us: [pid:39416 tid: 0x71a40bfff6c0]  hipGraphExecKernelNodeSetParams ( 0x7198ca566060, 0x71a3c3b83540, 0x71a40bffa708 ) 
:4:rocvirtual.cpp           :792 : 32130193211 us: [pid:39416 tid: 0x71a40bfff6c0] Arg0:   = ptr:0x719bfaf88f00 obj:[0x719bfaa00000-0x71a3bfe00000]
:4:rocvirtual.cpp           :792 : 32130193220 us: [pid:39416 tid: 0x71a40bfff6c0] Arg1:   = ptr:0x719bffaa0400 obj:[0x719bfaa00000-0x71a3bfe00000]
:3:rocvirtual.cpp           :3503: 32130193229 us: [pid:39416 tid: 0x71a40bfff6c0] ShaderName : loop_complex_fusion_5
:3:hip_graph.cpp            :1931: 32130193237 us: [pid:39416 tid: 0x71a40bfff6c0] hipGraphExecKernelNodeSetParams: Returned hipSuccess : 
:3:hip_graph.cpp            :1982: 32130193247 us: [pid:39416 tid: 0x71a40bfff6c0]  hipGraphExecChildGraphNodeSetParams ( 0x7198ca566060, 0x71a3c2da2470, 0x7198c974d900 ) 
:4:rocvirtual.cpp           :792 : 32130193262 us: [pid:39416 tid: 0x71a40bfff6c0] Arg0:   = ptr:0x719bff2a0400 obj:[0x719bfaa00000-0x71a3bfe00000]
:4:rocvirtual.cpp           :792 : 32130193272 us: [pid:39416 tid: 0x71a40bfff6c0] Arg1:   = ptr:0x719bff2a0400 obj:[0x719bfaa00000-0x71a3bfe00000]
:4:rocvirtual.cpp           :792 : 32130193283 us: [pid:39416 tid: 0x71a40bfff6c0] Arg2:   = ptr:0x719bffaa0400 obj:[0x719bfaa00000-0x71a3bfe00000]
:4:rocvirtual.cpp           :792 : 32130193292 us: [pid:39416 tid: 0x71a40bfff6c0] Arg3:   = ptr:0x719bfe2a0400 obj:[0x719bfaa00000-0x71a3bfe00000]
:4:rocvirtual.cpp           :882 : 32130193301 us: [pid:39416 tid: 0x71a40bfff6c0] Arg4:   = val:0x3f800000 (size:0x8)
:4:rocvirtual.cpp           :882 : 32130193308 us: [pid:39416 tid: 0x71a40bfff6c0] Arg5:   = val:0x0 (size:0x8)
:4:rocvirtual.cpp           :882 : 32130193314 us: [pid:39416 tid: 0x71a40bfff6c0] Arg6:   = val:0x200 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193321 us: [pid:39416 tid: 0x71a40bfff6c0] Arg7:   = val:0x0 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193328 us: [pid:39416 tid: 0x71a40bfff6c0] Arg8:   = val:0x200 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193335 us: [pid:39416 tid: 0x71a40bfff6c0] Arg9:   = val:0x0 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193342 us: [pid:39416 tid: 0x71a40bfff6c0] Arg10:   = val:0x200 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193349 us: [pid:39416 tid: 0x71a40bfff6c0] Arg11:   = val:0x0 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193355 us: [pid:39416 tid: 0x71a40bfff6c0] Arg12:   = val:0x200 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193362 us: [pid:39416 tid: 0x71a40bfff6c0] Arg13:   = val:0x0 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193369 us: [pid:39416 tid: 0x71a40bfff6c0] Arg14:   = val:0x200 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193376 us: [pid:39416 tid: 0x71a40bfff6c0] Arg15:   = val:0x400 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193382 us: [pid:39416 tid: 0x71a40bfff6c0] Arg16:   = val:0x1 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193389 us: [pid:39416 tid: 0x71a40bfff6c0] Arg17:   = val:0x200 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193396 us: [pid:39416 tid: 0x71a40bfff6c0] Arg18:   = val:0xf (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193403 us: [pid:39416 tid: 0x71a40bfff6c0] Arg19:   = val:0x10 (size:0x4)
:4:rocvirtual.cpp           :882 : 32130193410 us: [pid:39416 tid: 0x71a40bfff6c0] Arg20:   = val:0x20 (size:0x4)
:3:rocvirtual.cpp           :3503: 32130193416 us: [pid:39416 tid: 0x71a40bfff6c0] ShaderName : Cijk_Alik_Bljk_CB_MT32x32x8_SN_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASM_ASAE01_ASCE01_ASEM1_AAC0_BL0_BS1_CLR0_DTLA0_DTLB0_DTVA0_DTVB0_DVO0_ETSP_EPS0_ELFLR0_EMLL0_FSSC10_FL0_GLVWA1_GLVWB1_GRCGA1_GRCGB1_GRPM1_GRVW1_GSU1_GSUASB_GLS0_ISA000_IU1_K1_KLS_LBSPPA0_LBSPPB0_LPA0_LPB0_LDL1_LRVW1_LWPMn1_LDW0_FMA_MIAV0_MDA2_MO40_MMFSC_MKFGSU256_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR1_PLR1_PKA0_SIA1_SLW1_SS0_SU32_SUM0_SUS256_SCIUI1_SPO0_SRVW0_SSO0_SVW2_SNLL0_TSGRA0_TSGRB0_TT2_2_TLDS0_UMLDSA0_UMLDSB0_U64SL1_USFGRO0_VAW1_VS1_VW1_VWB1_VFLRP0_WSGRA0_WSGRB0_WS64_WG16_16_1_WGM8
:4:rocdevice.cpp            :2186: 32130196219 us: [pid:39416 tid: 0x71a40bfff6c0] Allocate hsa device memory (nil), size 0x29b00, hsa_mem_flags 0x4h
:1:rocdevice.cpp            :2190: 32130196231 us: [pid:39416 tid: 0x71a40bfff6c0] Fail allocation local memory
Segmentation fault (core dumped)
```

---

## 评论 (11 条)

### 评论 #1 — aloheac (2026-01-22T16:26:57Z)

I've checked that I receive the same seg fault under ROCm 7.2. I assume the root cause is the same as the known issue
#5878.

---

### 评论 #2 — amd-nicknick (2026-01-23T09:18:47Z)

Hi @aloheac, I'm checking internally on the known issue details. I'll update my assessment soon.
Could you please help confirm if I understood you correctly: The same segfault + same AMDLOG msg also occurs when running with ROCm 7.2 + TF 2.20 dev?
Thanks!

---

### 评论 #3 — aloheac (2026-01-24T22:04:00Z)

My previous comment was in reference to ROCm 7.2 + TF 2.19.1. I just tried the same under TF 2.20 dev and the seg fault seems harder to reproduce. Small models run long without issue, while larger models crash quickly. When it does happen, the stack trace seems to indicate a different shader than before. I'll keep trying to find a simple way to reproduce it and test it on nightly releases of TF.

```
:3:hip_graph.cpp            :1913: 18585998369 us: [pid:90329 tid: 0x7344d0ff96c0]  hipGraphExecKernelNodeSetParams ( 0x73446cacf3a0, 0x73446fdab390, 0x7344d0ff48c0 ) 
:4:rocvirtual.cpp           :891 : 18585998383 us: [pid:90329 tid: 0x7344d0ff96c0] Arg0:   = ptr:0x733d42b71f00 obj:[0x733d42a00000-0x734467e00000]
:4:rocvirtual.cpp           :891 : 18585998393 us: [pid:90329 tid: 0x7344d0ff96c0] Arg1:   = ptr:0x733d42c8e200 obj:[0x733d42a00000-0x734467e00000]
:3:rocvirtual.cpp           :3596: 18585998404 us: [pid:90329 tid: 0x7344d0ff96c0] ShaderName : input_reduce_fusion_25
:3:hip_graph.cpp            :1931: 18585998412 us: [pid:90329 tid: 0x7344d0ff96c0] hipGraphExecKernelNodeSetParams: Returned hipSuccess : 
:3:hip_graph.cpp            :1913: 18585998422 us: [pid:90329 tid: 0x7344d0ff96c0]  hipGraphExecKernelNodeSetParams ( 0x73446cacf3a0, 0x733a2178bb80, 0x7344d0ff48c0 ) 
:4:rocvirtual.cpp           :891 : 18585998434 us: [pid:90329 tid: 0x7344d0ff96c0] Arg0:   = ptr:0x733d42c8e200 obj:[0x733d42a00000-0x734467e00000]
:4:rocvirtual.cpp           :891 : 18585998444 us: [pid:90329 tid: 0x7344d0ff96c0] Arg1:   = ptr:0x733d42c8ee00 obj:[0x733d42a00000-0x734467e00000]
:3:rocvirtual.cpp           :3596: 18585998453 us: [pid:90329 tid: 0x7344d0ff96c0] ShaderName : input_reduce_fusion_22
:3:hip_graph.cpp            :1931: 18585998461 us: [pid:90329 tid: 0x7344d0ff96c0] hipGraphExecKernelNodeSetParams: Returned hipSuccess : 
:3:hip_module.cpp           :195 : 18585998473 us: [pid:90329 tid: 0x7344d0ff96c0]  hipFuncSetAttribute ( 0x73446cf74520, 8, 12288 ) 
:3:hip_module.cpp           :240 : 18585998484 us: [pid:90329 tid: 0x7344d0ff96c0] hipFuncSetAttribute: Returned hipSuccess : 
:3:hip_graph.cpp            :1913: 18585998492 us: [pid:90329 tid: 0x7344d0ff96c0]  hipGraphExecKernelNodeSetParams ( 0x73446cacf3a0, 0x73446de6d310, 0x7344d0ff48c0 ) 
:4:rocvirtual.cpp           :891 : 18585998506 us: [pid:90329 tid: 0x7344d0ff96c0] Arg0:  arg0 = ptr:0x733d42af1f00 obj:[0x733d42a00000-0x734467e00000]
:4:rocvirtual.cpp           :891 : 18585998515 us: [pid:90329 tid: 0x7344d0ff96c0] Arg1:  arg1 = ptr:0x733d42a01c00 obj:[0x733d42a00000-0x734467e00000]
:4:rocvirtual.cpp           :891 : 18585998525 us: [pid:90329 tid: 0x7344d0ff96c0] Arg2:  arg2 = ptr:0x733d42b71f00 obj:[0x733d42a00000-0x734467e00000]
:4:rocvirtual.cpp           :891 : 18585998534 us: [pid:90329 tid: 0x7344d0ff96c0] Arg3:  arg3 = ptr:0x733d42b31f00 obj:[0x733d42a00000-0x734467e00000]
:3:rocvirtual.cpp           :3596: 18585998544 us: [pid:90329 tid: 0x7344d0ff96c0] ShaderName : gemm_fusion_dot_937
:4:rocdevice.cpp            :2185: 18586004100 us: [pid:90329 tid: 0x7344d0ff96c0] Allocate hsa device memory (nil), size 0x25700, hsa_mem_flags 0x4h
:1:rocdevice.cpp            :2189: 18586004114 us: [pid:90329 tid: 0x7344d0ff96c0] Fail allocation local memory
Segmentation fault (core dumped)
```

---

### 评论 #4 — amd-nicknick (2026-01-26T10:27:00Z)

Hi @aloheac, I think we should focus on the TF 2.20 dev case (unless you have specific reasons to stick on 2.19? In that case, please let me know). Could you please work out a sample that I could try reproducing? Thanks!

---

### 评论 #5 — amd-nicknick (2026-01-28T08:11:46Z)

Hi @aloheac, a quick update, I was able to repro this issue with large epochs running the MNIST sample, albeit with different shader that faulted.
My initial guess would be some sort of problem in memory allocator, I'll keep this issue updated with my progress.
Thanks for brining this to our attention.

---

### 评论 #6 — aloheac (2026-01-28T23:17:06Z)

I'm glad you were able to reproduce it. I was having trouble coming up with a concise example on TF 2.20-dev without having to run it a long time. Thanks for taking the time to look into this!

---

### 评论 #7 — amd-nicknick (2026-01-29T12:21:20Z)

Hi @aloheac, a quick update on the internal issue, the one you're facing now does not look similar to the internal one we're already working on.
I'll keep this issue updated on my progress. As a sanity check, could you please help check if you could also repro this with MNIST + large epochs on 2.20? Just to ensure we're looking at the same thing.

---

### 评论 #8 — aloheac (2026-01-30T06:17:31Z)

Hi @amd-nicknick,

It seems like I'm not able to get MNIST to seg fault on TF 2.20. Below is code that will consistently produce a seg fault on 2.20, generally within 100 epochs.

```
import numpy as np
import tensorflow as tf


# Fit y = sin(x) over (0, 10 pi)         
def gen_data(batch_size, input_dim):
    while True:
        x = tf.random.uniform((batch_size, input_dim)) * 10 * np.pi
        y = tf.sin(x)

        yield x, y
    

class Model(tf.keras.Model):
    def __init__(self):
        super(Model, self).__init__()
        self.dense1 = tf.keras.layers.Dense(64, activation="tanh")
        self.dense2 = tf.keras.layers.Dense(64, activation="tanh")
        self.dense3 = tf.keras.layers.Dense(64, activation="tanh")
        self.dense4 = tf.keras.layers.Dense(64, activation="tanh")
        self.dense5 = tf.keras.layers.Dense(64, activation="tanh")
        self.dense6 = tf.keras.layers.Dense(64, activation="tanh")
        self.dense7 = tf.keras.layers.Dense(64, activation="tanh")
        self.dense8 = tf.keras.layers.Dense(64, activation="tanh")
        self.dense9 = tf.keras.layers.Dense(64, activation="tanh")
        self.dense10 = tf.keras.layers.Dense(64, activation="tanh")
        self.dense11 = tf.keras.layers.Dense(64, activation="tanh")
        self.dense12 = tf.keras.layers.Dense(1)
        

    def call(self, inputs):
        y = self.dense1(inputs)
        y = self.dense2(y)
        y = self.dense3(y)
        y = self.dense4(y)
        y = self.dense5(y)
        y = self.dense6(y)
        y = self.dense7(y)
        y = self.dense8(y)
        y = self.dense9(y)
        y = self.dense10(y)
        y = self.dense11(y)
        y = self.dense12(y)

        return y   
    
    
    # Define a custom step for updating the gradients. Normally I implement an adaptive
    # timestep here, but removed it to simplify the code. Throwing a seg fault seems to depend
    # on having a custom train_step(), instead of the default.
    def train_step(self, data):
        x_batch, y_batch = data
        
        with tf.GradientTape() as tape:
            pred_y = self.call(x_batch)
            
            losses = [tf.keras.losses.mse(y_batch, pred_y)] + [tf.reduce_sum(loss) for loss in self.losses]
            total_loss = tf.reduce_mean(tf.stack(losses))
        
        grads = tape.gradient(total_loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))

        return {"loss": total_loss, "rmse": tf.sqrt(total_loss)}
 

model = Model()
model.compile(loss="mse", optimizer="adam")

model.optimizer.learning_rate=0.001
batch_size = 1024   # Large batches can help throw the seg fault.
model.fit(gen_data(batch_size, 1), batch_size=batch_size, steps_per_epoch=1000, epochs=500)
```

The stack trace I get is similar to before:

```

Thread 148 "python3" received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7ffb8ddfd6c0 (LWP 128547)]
0x00007ffee42600df in ?? () from /opt/rocm/lib/libamdhip64.so.7
(gdb) bt
#0  0x00007ffee42600df in ?? () from /opt/rocm/lib/libamdhip64.so.7
#1  0x00007ffee4260cd4 in ?? () from /opt/rocm/lib/libamdhip64.so.7
#2  0x00007ffee3ed4194 in ?? () from /opt/rocm/lib/libamdhip64.so.7
#3  0x00007ffee3ed2109 in ?? () from /opt/rocm/lib/libamdhip64.so.7
#4  0x00007ffee3f0ef7d in ?? () from /opt/rocm/lib/libamdhip64.so.7
#5  0x00007fff78d29acc in stream_executor::gpu::RocmCommandBuffer::UpdateKernelNode(stream_executor::gpu::GpuCommandBuffer::GraphNodeHandleOpaque*, stream_executor::ThreadDim const&, stream_executor::BlockDim const&, stream_executor::Kernel const&, stream_executor::KernelArgsPackedArrayBase const&) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#6  0x00007fff78d2d751 in stream_executor::gpu::GpuCommandBuffer::UpdateLaunch(stream_executor::CommandBuffer::Command const*, stream_executor::ThreadDim const&, stream_executor::BlockDim const&, stream_executor::Kernel const&, stream_executor::KernelArgs const&) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#7  0x00007fff70ddc279 in absl::lts_20250127::Status absl::lts_20250127::functional_internal::InvokeObject<xla::gpu::LaunchCmd::Record(xla::gpu::Thunk::ExecuteParams const&, xla::gpu::CommandBufferCmd::RecordParams const&, std::variant<xla::gpu::CommandBufferCmd::RecordCreate, xla::gpu::CommandBufferCmd::RecordUpdate>, stream_executor::CommandBuffer*)::$_1, absl::lts_20250127::Status, stream_executor::CommandBuffer::Command const*>(absl::lts_20250127::functional_internal::VoidPtr, absl::lts_20250127::functional_internal::ForwardT<stream_executor::CommandBuffer::Command const*>::type) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#8  0x00007fff70dc4c54 in xla::gpu::Handle(std::variant<xla::gpu::CommandBufferCmd::RecordCreate, xla::gpu::CommandBufferCmd::RecordUpdate>, absl::lts_20250127::FunctionRef<absl::lts_20250127::StatusOr<stream_executor::CommandBuffer::Command const*> (absl::lts_20250127::Span<stream_executor::CommandBuffer::Command const* const>)>, absl::lts_20250127::FunctionRef<absl::lts_20250127::Status (stream_executor::CommandBuffer::Command const*)>) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#9  0x00007fff70dc6419 in xla::gpu::LaunchCmd::Record(xla::gpu::Thunk::ExecuteParams const&, xla::gpu::CommandBufferCmd::RecordParams const&, std::variant<xla::gpu::CommandBufferCmd::RecordCreate, xla::gpu::CommandBufferCmd::RecordUpdate>, stream_executor::CommandBuffer*) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#10 0x00007fff70dc1984 in xla::gpu::CommandBufferCmdExecutor::RecordUpdate(xla::gpu::Thunk::ExecuteParams const&, xla::gpu::CommandBufferCmd::RecordParams const&, stream_executor::CommandBuffer*) const ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#11 0x00007fff70dc14fb in xla::gpu::CommandBufferCmdExecutor::Record(xla::gpu::Thunk::ExecuteParams const&, xla::gpu::CommandBufferCmd::RecordParams const&, stream_executor::CommandBuffer*) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#12 0x00007fff70dbd643 in xla::gpu::CommandBufferThunk::ExecuteOnStream(xla::gpu::Thunk::ExecuteParams const&) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#13 0x00007fff7177c654 in xla::gpu::SequentialThunk::ExecuteOnStream(xla::gpu::Thunk::ExecuteParams const&) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#14 0x00007fff7176bbd4 in xla::gpu::(anonymous namespace)::ExecuteThunksImpl(xla::DebugOptions const*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, xla::gpu::SequentialThunk&, xla::gpu::Thunk::ExecutableSource, xla::ServiceExecutableRunOptions const*, xla::gpu::BufferAllocations const&, bool, absl::lts_20250127::flat_hash_set<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long>, absl::lts_20250127::hash_internal::Hash<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long> >, std::equal_to<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long> >, std::allocator<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long> > > const&) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
--Type <RET> for more, q to quit, c to continue without paging--c
#15 0x00007fff71769d6e in xla::gpu::GpuExecutable::ExecuteThunks(xla::gpu::BufferAllocations const&, xla::ServiceExecutableRunOptions const*) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#16 0x00007fff71767f94 in xla::gpu::GpuExecutable::ExecuteAsyncOnStreamImpl(xla::ServiceExecutableRunOptions const*, std::variant<absl::lts_20250127::Span<xla::ShapedBuffer const* const>, absl::lts_20250127::Span<xla::ExecutionInput> >) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#17 0x00007fff717678cd in xla::gpu::GpuExecutable::ExecuteAsyncOnStream(xla::ServiceExecutableRunOptions const*, std::vector<xla::ExecutionInput, std::allocator<xla::ExecutionInput> >) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#18 0x00007fff77e6cf1f in xla::Executable::ExecuteAsyncOnStreamWrapper(xla::ServiceExecutableRunOptions const*, std::vector<xla::ExecutionInput, std::allocator<xla::ExecutionInput> >) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#19 0x00007fff6b7ed9e9 in xla::LocalExecutable::RunAsync(absl::lts_20250127::Span<xla::Shape const* const>, std::vector<xla::ExecutionInput, std::allocator<xla::ExecutionInput> >, xla::ExecutableRunOptions) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#20 0x00007fff6b7ee38e in xla::LocalExecutable::RunAsync(std::vector<xla::ExecutionInput, std::allocator<xla::ExecutionInput> >, xla::ExecutableRunOptions) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#21 0x00007fff717b97b8 in tensorflow::(anonymous namespace)::RunExecutable(tensorflow::XlaPlatformInfo const&, tensorflow::XlaComputationLaunchContext const&, std::vector<xla::ExecutionInput, std::allocator<xla::ExecutionInput> >, xla::ExecutableRunOptions, xla::LocalExecutable*, tensorflow::OpKernelContext*, stream_executor::DeviceMemoryAllocator*) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#22 0x00007fff717c4268 in std::_Function_handler<void (), tensorflow::XlaLocalLaunchBase::ComputeAsync(tensorflow::OpKernelContext*, std::function<void ()>)::$_1>::_M_invoke(std::_Any_data const&) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#23 0x00007fff717b380d in tensorflow::XlaLocalLaunchBase::ComputeAsync(tensorflow::OpKernelContext*, std::function<void ()>) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_cc.so.2
#24 0x00007fff77802359 in tensorflow::BaseGPUDevice::ComputeAsync(tensorflow::AsyncOpKernel*, tensorflow::OpKernelContext*, std::function<void ()>) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#25 0x00007fff79172b2b in tensorflow::(anonymous namespace)::ExecutorState<tensorflow::PropagatorState>::Process(tensorflow::PropagatorState::TaggedNode const&, long) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#26 0x00007fff79a9f414 in Eigen::ThreadPoolTempl<tsl::thread::EigenEnvironment>::WorkerLoop(int) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#27 0x00007fff79a9f2b1 in void std::__invoke_impl<void, tsl::thread::EigenEnvironment::CreateThread(std::function<void ()>)::{lambda()#1}&>(std::__invoke_other, tsl::thread::EigenEnvironment::CreateThread(std::function<void ()>)::{lambda()#1}&) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#28 0x00007fff79a8b308 in tsl::(anonymous namespace)::PThread::ThreadFn(void*) ()
   from /home/loheac/Projects/complex/venv3/lib/python3.12/site-packages/tensorflow/python/platform/../../libtensorflow_framework.so.2
#29 0x00007ffff7c9caa4 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:447
#30 0x00007ffff7d29c6c in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:78
```


---

### 评论 #9 — amd-nicknick (2026-02-06T07:22:52Z)

@aloheac, just for isolation, could you please help run the workload with the following environment variable set?
`export xla_gpu_graph_level=0`
Initial analysis shows the failure occurred during allocation of kernel argument space on GPU memory when graph capture is active. The flag disables XLA capturing HIP graph to isolate the codepath and ensure we're seeing the same failure.

After setting the key, it should no longer fail. I'm looking into why the allocation fails.

Kindly let me know the result once you have it available. Thanks!

---

### 评论 #10 — aloheac (2026-02-07T03:59:16Z)

Hi @amd-nicknick. Indeed, even my original model which crashes quickly runs just fine with this flag enabled. When I first encountered this issue I tried entirely disabling XLA, which prevented the seg fault but ran very slowly. I have little performance loss with this option, so it's a great workaround for now. Thanks!

---

### 评论 #11 — amd-nicknick (2026-02-09T08:17:29Z)

Thanks for confirming. Let me check what's wrong with graph capture in this case.

---
