# [Issue]: Device side enqueue with enqueue_kernel() fails on Radeon RX 7600M XT

> **Issue #3748**
> **状态**: closed
> **创建时间**: 2024-09-18T14:48:19Z
> **更新时间**: 2024-09-27T20:30:07Z
> **关闭时间**: 2024-09-27T19:49:42Z
> **作者**: mdoube
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XT, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3748

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

I have an AMD Radeon RX 7600M XT that fails whenever `enqueue_kernel()` is called, despite this being a core feature of OpenCL 2.0 and the device supporting 2.0. I get this in the console every time:
```
Memory access fault by GPU node-1 (Agent handle: 0x75d8c4c87dc0) on address (nil). Reason: Page not present or supervisor privilege.
``` 


### Operating System

Ubuntu 22.04.4 LTS

### CPU

Intel(R) Core(TM) m7-6Y75 CPU @ 1.20GHz

### GPU

AMD Radeon RX 7600M XT

### ROCm Version

ROCm 6.2.0, ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

Make a call to `enqueue_kernel()` in device code. Same code works fine on NVIDIA drivers.
Something as simple as a no-op example will cause the program to fail:
```opencl
__kernel void parent (
) {
    queue_t queue = get_default_queue();
    size_t local_work_size = 32;
    size_t global_work_size = 1024;
    ndrange_t ndrange = ndrange_1D(global_work_size, local_work_size);
    enqueue_kernel(queue, CLK_ENQUEUE_FLAGS_WAIT_KERNEL, ndrange,
	^{ }
    );
}
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.14
Runtime Ext Version:     1.6
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    Intel(R) Core(TM) m7-6Y75 CPU @ 1.20GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) m7-6Y75 CPU @ 1.20GHz
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
  Max Clock Freq. (MHz):   3100                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            4                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16262516(0xf82574) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16262516(0xf82574) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16262516(0xf82574) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon™ RX 7600M XT          
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
    L2:                      2048(0x800) KB                     
  Chip ID:                 29824(0x7480)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2023                               
  BDFID:                   15360                              
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 52                                 
  SDMA engine uCode::      16                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1102         
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***  

### Additional Information

May be similar to #1326 

clinfo says:

```
  Platform Name                                   AMD Accelerated Parallel Processing
  Platform Vendor                                 Advanced Micro Devices, Inc.
  Platform Version                                OpenCL 2.1 AMD-APP (3625.0)
  Platform Profile                                FULL_PROFILE
  Platform Extensions                             cl_khr_icd cl_amd_event_callback 
  Platform Extensions function suffix             AMD
  Platform Host timer resolution                  1ns


  Platform Name                                   AMD Accelerated Parallel Processing
Number of devices                                 1
  Device Name                                     gfx1102
  Device Vendor                                   Advanced Micro Devices, Inc.
  Device Vendor ID                                0x1002
  Device Version                                  OpenCL 2.0 
  Driver Version                                  3625.0 (HSA1.1,LC)
  Device OpenCL C Version                         OpenCL C 2.0 
  Device Type                                     GPU
  Device Board Name (AMD)                         AMD Radeon™ RX 7600M XT
  Device PCI-e ID (AMD)                           0x7480
  Device Topology (AMD)                           PCI-E, 0000:3c:00.0
  Device Profile                                  FULL_PROFILE
  Device Available                                Yes
  Compiler Available                              Yes
  Linker Available                                Yes
  Max compute units                               16
  SIMD per compute unit (AMD)                     4
  SIMD width (AMD)                                32
  SIMD instruction width (AMD)                    1
  Max clock frequency                             2023MHz
  Graphics IP (AMD)                               11.0
  Device Partition                                (core)
    Max number of sub-devices                     16
    Supported partition types                     None
    Supported affinity domains                    (n/a)
  Max work item dimensions                        3
  Max work item sizes                             1024x1024x1024
  Max work group size                             256
  Preferred work group size (AMD)                 256
  Max work group size (AMD)                       1024
  Preferred work group size multiple (kernel)     32
  Wavefront width (AMD)                           32
  Preferred / native vector sizes                 
    char                                                 4 / 4       
    short                                                2 / 2       
    int                                                  1 / 1       
    long                                                 1 / 1       
    half                                                 1 / 1        (cl_khr_fp16)
    float                                                1 / 1       
    double                                               1 / 1        (cl_khr_fp64)
  Half-precision Floating-point support           (cl_khr_fp16)
    Denormals                                     Yes
    Infinity and NANs                             Yes
    Round to nearest                              Yes
    Round to zero                                 Yes
    Round to infinity                             Yes
    IEEE754-2008 fused multiply-add               Yes
    Support is emulated in software               No
  Single-precision Floating-point support         (core)
    Denormals                                     Yes
    Infinity and NANs                             Yes
    Round to nearest                              Yes
    Round to zero                                 Yes
    Round to infinity                             Yes
    IEEE754-2008 fused multiply-add               Yes
    Support is emulated in software               No
    Correctly-rounded divide and sqrt operations  Yes
  Double-precision Floating-point support         (cl_khr_fp64)
    Denormals                                     Yes
    Infinity and NANs                             Yes
    Round to nearest                              Yes
    Round to zero                                 Yes
    Round to infinity                             Yes
    IEEE754-2008 fused multiply-add               Yes
    Support is emulated in software               No
  Address bits                                    64, Little-Endian
  Global memory size                              8573157376 (7.984GiB)
  Global free memory (AMD)                        8192000 (7.812GiB) 8192000 (7.812GiB)
  Global memory channels (AMD)                    4
  Global memory banks per channel (AMD)           4
  Global memory bank width (AMD)                  256 bytes
  Error Correction support                        No
  Max memory allocation                           7287183768 (6.787GiB)
  Unified memory for Host and Device              No
  Shared Virtual Memory (SVM) capabilities        (core)
    Coarse-grained buffer sharing                 Yes
    Fine-grained buffer sharing                   Yes
    Fine-grained system sharing                   No
    Atomics                                       No
  Minimum alignment for any data type             128 bytes
  Alignment of base address                       1024 bits (128 bytes)
  Preferred alignment for atomics                 
    SVM                                           0 bytes
    Global                                        0 bytes
    Local                                         0 bytes
  Max size for global variable                    7287183768 (6.787GiB)
  Preferred total size of global vars             8573157376 (7.984GiB)
  Global Memory cache type                        Read/Write
  Global Memory cache size                        32768 (32KiB)
  Global Memory cache line size                   64 bytes
  Image support                                   Yes
    Max number of samplers per kernel             16
    Max size for 1D images from buffer            134217728 pixels
    Max 1D or 2D image array size                 8192 images
    Base address alignment for 2D image buffers   256 bytes
    Pitch alignment for 2D image buffers          256 pixels
    Max 2D image size                             16384x16384 pixels
    Max 3D image size                             16384x16384x8192 pixels
    Max number of read image args                 128
    Max number of write image args                8
    Max number of read/write image args           64
  Max number of pipe args                         16
  Max active pipe reservations                    16
  Max pipe packet size                            2992216472 (2.787GiB)
  Local memory type                               Local
  Local memory size                               65536 (64KiB)
  Local memory size per CU (AMD)                  65536 (64KiB)
  Local memory banks (AMD)                        32
  Max number of constant args                     8
  Max constant buffer size                        7287183768 (6.787GiB)
  Preferred constant buffer size (AMD)            16384 (16KiB)
  Max size of kernel argument                     1024
  Queue properties (on host)                      
    Out-of-order execution                        No
    Profiling                                     Yes
  Queue properties (on device)                    
    Out-of-order execution                        Yes
    Profiling                                     Yes
    Preferred size                                262144 (256KiB)
    Max size                                      8388608 (8MiB)
  Max queues on device                            1
  Max events on device                            1024
  Prefer user sync for interop                    Yes
  Number of P2P devices (AMD)                     0
  Profiling timer resolution                      1ns
  Profiling timer offset since Epoch (AMD)        0ns (Thu Jan  1 01:00:00 1970)
  Execution capabilities                          
    Run OpenCL kernels                            Yes
    Run native kernels                            No
    Thread trace supported (AMD)                  No
    Number of async queues (AMD)                  8
    Max real-time compute queues (AMD)            8
    Max real-time compute units (AMD)             16
  printf() buffer size                            4194304 (4MiB)
  Built-in kernels                                (n/a)
  Device Extensions                               cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_depth_images cl_amd_copy_buffer_p2p cl_amd_assembly_program 

```

---

## 评论 (8 条)

### 评论 #1 — harkgill-amd (2024-09-20T14:24:51Z)

Hi @mdoube, device enqueues are supported on gfx1102 and are tested with the OpenCL Conformance Tests. Could you please run the tests at https://github.com/KhronosGroup/OpenCL-CTS/tree/main/test_conformance/device_execution and confirm if you are still seeing the page fault errors?

---

### 评论 #2 — mdoube (2024-09-20T15:23:51Z)

Thanks for picking this up.

> Hi @mdoube, device enqueues are supported on gfx1102 and are tested with the OpenCL Conformance Tests. Could you please run the tests at https://github.com/KhronosGroup/OpenCL-CTS/tree/main/test_conformance/device_execution and confirm if you are still seeing the page fault errors?

Tests pass, no errors in the log
[tests.log](https://github.com/user-attachments/files/17076954/tests.log)

The other dimension that may be relevant is that I'm compiling and running the OpenCL kernel via calls from JOCL, although as mentioned before, the same code works fine on NVIDIA devices (GTX 980 and RTX A4000). I can give you access to the private repo where the code is if it would help.

---

### 评论 #3 — harkgill-amd (2024-09-20T18:27:41Z)

> I can give you access to the private repo where the code is if it would help.

That would be great. I'll give it a try on my side as well to rule out any hardware related issues.

---

### 评论 #4 — mdoube (2024-09-21T09:55:19Z)

This small sample, slightly modified from the [JOCL sample](https://github.com/gpu/JOCLSamples/blob/master/src/main/java/org/jocl/samples/JOCLSample.java) by Marco Hutter, replicates it. Make sure to set `platformIndex` and `deviceIndex` to the platform and device numbers that you are testing:
```java
/*
 * JOCL - Java bindings for OpenCL
 * 
 * Copyright 2009 Marco Hutter - http://www.jocl.org/
 */

import static org.jocl.CL.*;

import org.jocl.*;

/**
 * A small JOCL sample.
 */
public class JOCLSample
{
    /**
     * The source code of the OpenCL program to execute
     */
    private static String programSource =
        "__kernel void "+
        "sampleKernel(__global const float *a,"+
        "             __global const float *b,"+
        "             __global float *c)"+
        "{"+
        "    queue_t queue = get_default_queue();"+
        "    size_t local_work_size = 1;"+
        "    size_t global_work_size = 10;"+
        "    ndrange_t ndrange = ndrange_1D(global_work_size, local_work_size);"+
        	"printf(\"Solo parent kernel enqueueing child kernel in %d work items...\\n\", global_work_size);"+
        "    enqueue_kernel(queue, CLK_ENQUEUE_FLAGS_WAIT_KERNEL, ndrange,"+
        "	^{" +
        "      int gid = get_global_id(0);"+
    	"      printf(\"Child kernel %d says hi\\n\", gid);"+
        "      c[gid] = a[gid] * b[gid];"+
        "    });"+
        "}";
    

    /**
     * The entry point of this sample
     * 
     * @param args Not used
     */
    public static void main(String args[])
    {
        // Create input- and output data 
        int n = 10;
        float srcArrayA[] = new float[n];
        float srcArrayB[] = new float[n];
        float dstArray[] = new float[n];
        for (int i=0; i<n; i++)
        {
            srcArrayA[i] = i;
            srcArrayB[i] = i;
        }
        Pointer srcA = Pointer.to(srcArrayA);
        Pointer srcB = Pointer.to(srcArrayB);
        Pointer dst = Pointer.to(dstArray);

        // The platform, device type and device number
        // that will be used
        final int platformIndex = 0;
        final long deviceType = CL_DEVICE_TYPE_ALL;
        final int deviceIndex = 0;

        // Enable exceptions and subsequently omit error checks in this sample
        CL.setExceptionsEnabled(true);

        // Obtain the number of platforms
        int numPlatformsArray[] = new int[1];
        clGetPlatformIDs(0, null, numPlatformsArray);
        int numPlatforms = numPlatformsArray[0];

        // Obtain a platform ID
        cl_platform_id platforms[] = new cl_platform_id[numPlatforms];
        clGetPlatformIDs(platforms.length, platforms, null);
        cl_platform_id platform = platforms[platformIndex];

        // Initialize the context properties
        cl_context_properties contextProperties = new cl_context_properties();
        contextProperties.addProperty(CL_CONTEXT_PLATFORM, platform);
        
        // Obtain the number of devices for the platform
        int numDevicesArray[] = new int[1];
        clGetDeviceIDs(platform, deviceType, 0, null, numDevicesArray);
        int numDevices = numDevicesArray[0];
        
        // Obtain a device ID 
        cl_device_id devices[] = new cl_device_id[numDevices];
        clGetDeviceIDs(platform, deviceType, numDevices, devices, null);
        cl_device_id device = devices[deviceIndex];

        // Create a context for the selected device
        cl_context context = clCreateContext(
            contextProperties, 1, new cl_device_id[]{device}, 
            null, null, null);
        
        // Create a command-queue for the selected device
        cl_command_queue commandQueue = 
            clCreateCommandQueue(context, device, 0, null);

        // Allocate the memory objects for the input- and output data
        cl_mem memObjects[] = new cl_mem[3];
        memObjects[0] = clCreateBuffer(context, 
            CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
            Sizeof.cl_float * n, srcA, null);
        memObjects[1] = clCreateBuffer(context, 
            CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
            Sizeof.cl_float * n, srcB, null);
        memObjects[2] = clCreateBuffer(context, 
            CL_MEM_READ_WRITE, 
            Sizeof.cl_float * n, null, null);
        
        // Create the program from the source code
        cl_program program = clCreateProgramWithSource(context,
            1, new String[]{ programSource }, null, null);
        
        // Build the program
        clBuildProgram(program, 0, null, "-cl-std=CL2.0", null, null);
        
        // Create the kernel
        cl_kernel kernel = clCreateKernel(program, "sampleKernel", null);
        
        // Set the arguments for the kernel
        clSetKernelArg(kernel, 0, 
            Sizeof.cl_mem, Pointer.to(memObjects[0]));
        clSetKernelArg(kernel, 1, 
            Sizeof.cl_mem, Pointer.to(memObjects[1]));
        clSetKernelArg(kernel, 2, 
            Sizeof.cl_mem, Pointer.to(memObjects[2]));
        
        // Set the work-item dimensions to 1 to make a solo parent
        long global_work_size[] = new long[]{1};
        long local_work_size[] = new long[]{1};
        
        // Execute the kernel
        clEnqueueNDRangeKernel(commandQueue, kernel, 1, null,
            global_work_size, local_work_size, 0, null, null);
        
        // Read the output data
        clEnqueueReadBuffer(commandQueue, memObjects[2], CL_TRUE, 0,
            n * Sizeof.cl_float, dst, 0, null, null);
        
        // Release kernel, program, and memory objects
        clReleaseMemObject(memObjects[0]);
        clReleaseMemObject(memObjects[1]);
        clReleaseMemObject(memObjects[2]);
        clReleaseKernel(kernel);
        clReleaseProgram(program);
        clReleaseCommandQueue(commandQueue);
        clReleaseContext(context);
        
        // Verify the result
        boolean passed = true;
        final float epsilon = 1e-7f;
        for (int i=0; i<n; i++)
        {
            float x = dstArray[i];
            float y = srcArrayA[i] * srcArrayB[i];
            boolean epsilonEqual = Math.abs(x - y) <= epsilon * Math.abs(x);
            if (!epsilonEqual)
            {
                passed = false;
                break;
            }
        }
        System.out.println("Test "+(passed?"PASSED":"FAILED"));
        if (n <= 10)
        {
            System.out.println("Result: "+java.util.Arrays.toString(dstArray));
        }
    }
}
```
Output on Radeon RX 7600M XT:
```
Memory access fault by GPU node-1 (Agent handle: 0x70ba9cbf1720) on address (nil). Reason: Page not present or supervisor privilege.
```

Output on NVIDIA RTX A4000:
```
Solo parent kernel enqueueing child kernel in 10 work items...
Child kernel 6 says hi
Child kernel 0 says hi
Child kernel 8 says hi
Child kernel 2 says hi
Child kernel 9 says hi
Child kernel 3 says hi
Child kernel 7 says hi
Child kernel 1 says hi
Child kernel 4 says hi
Child kernel 5 says hi
Test PASSED
Result: [0.0, 1.0, 4.0, 9.0, 16.0, 25.0, 36.0, 49.0, 64.0, 81.0]
```


---

### 评论 #5 — harkgill-amd (2024-09-23T14:34:58Z)

@mdoube thank you for providing the sample program. I was able to reproduce the Memory Access Fault on the 7900XTX as well, indicating that the issue is not hardware-specific. I have opened an internal ticket to investigate this further.

---

### 评论 #6 — schung-amd (2024-09-27T14:30:08Z)

Hi @mdoube, I was able to reproduce this as well. The issue here is that child kernels are device-side and need to be launched on a device-side queue rather than a host-side queue; see https://registry.khronos.org/OpenCL/specs/3.0-unified/html/OpenCL_API.html#device-side-enqueue (although technically this document is for 3.0).

Starting in OpenCL 2.0 `clCreateCommandQueue()` is deprecated, and you should use `clCreateCommandQueueWithProperties()` instead, which allows specification of whether a command queue is a host-side queue or a device-side queue. By default, queues are host-side. You will need two command queues here: a host-side queue for your parent kernel, and a device-side queue for your child kernels. That would look like this with JOCL:
```
cl_queue_properties qprop = new cl_queue_properties();
qprop.addProperty(CL_QUEUE_PROPERTIES, CL_QUEUE_ON_DEVICE | CL_QUEUE_ON_DEVICE_DEFAULT);

cl_command_queue hostQueue = clCreateCommandQueueWithProperties(context, device, null, null);
cl_command_queue deviceQueue = clCreateCommandQueueWithProperties(context, device, qprop, null);
```
Note that the syntax here for adding the queue properties differs from what you might see in other documentation and examples, I believe this is due to JOCL's wrapper around them. 

Launch the parent kernel on the host-side queue: 
```
clEnqueueNDRangeKernel(hostQueue, kernel, 1, null, global_work_size, local_work_size, 0, null, null);
```
The child kernels will launch on the device-side queue, as it has been set to the default device queue and this will be detected inside the parent kernel with your call to `get_default_queue()`.

With these changes, your code executes fine on my system with correct results, with the caveat that the print statement in the child kernel will not display anything.

---

### 评论 #7 — mdoube (2024-09-27T14:54:36Z)

@harkgill-amd @schung-amd thanks for your help with this.

I can confirm that the change you suggest helps, however, it breaks execution on my NVIDIA card. To make it work I have to set the `CL_QUEUE_OUT_OF_ORDER_EXEC_MODE_ENABLE` flag. According to the [docs](https://registry.khronos.org/OpenCL/sdk/3.0/docs/man/html/clCreateCommandQueueWithProperties.html):

> CL_QUEUE_ON_DEVICE - Indicates that this is a device queue. If CL_QUEUE_ON_DEVICE is set, CL_QUEUE_OUT_OF_ORDER_EXEC_MODE_ENABLE [[1](https://registry.khronos.org/OpenCL/sdk/3.0/docs/man/html/clCreateCommandQueueWithProperties.html#_footnotedef_1)] must also be set.

It also means that implied ordering of child kernels can't be assumed and if order is important it needs to be handled with events.

The working code looks like this:
 ```java
cl_command_queue hostCommandQueue = 
            clCreateCommandQueueWithProperties(context, device, null, null);
cl_queue_properties deviceQProperties = new cl_queue_properties();
deviceQProperties.addProperty(CL_QUEUE_PROPERTIES, CL_QUEUE_ON_DEVICE | CL_QUEUE_ON_DEVICE_DEFAULT | CL_QUEUE_OUT_OF_ORDER_EXEC_MODE_ENABLE);
cl_command_queue deviceQueue = clCreateCommandQueueWithProperties(context, device, deviceQProperties, null);
```

---

### 评论 #8 — schung-amd (2024-09-27T20:30:06Z)

Thanks for the update, and the information about `CL_QUEUE_OUT_OF_ORDER_EXEC_MODE_ENABLE`! 

---
