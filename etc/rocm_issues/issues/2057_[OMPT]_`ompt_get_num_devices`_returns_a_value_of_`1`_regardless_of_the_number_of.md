# [OMPT] `ompt_get_num_devices` returns a value of `1` regardless of the number of devices present

> **Issue #2057**
> **状态**: closed
> **创建时间**: 2023-04-17T11:48:20Z
> **更新时间**: 2024-08-07T19:25:20Z
> **关闭时间**: 2024-08-07T19:25:20Z
> **作者**: Thyre
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2057

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

**Description:**

The OMPT interface offers several functions to allow the interface to retrieve information, for example about the number of GPUs present. This function is called `ompt_get_num_devices`. The function pointer will be returned upon calling the lookup function passed during the tool initialization. 

The lookup functions are required by the OpenMP standard. [Section 19.5 of the OpenMP Standard 5.2 specifications](https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-5-2.pdf#page=493) states the following restriction:
> Tool callbacks may not use OpenMP directives or call any runtime library routines described in Chapter 18.

While the function `omp_get_num_devices` works fine (outside of callback regions in the OMPT interface), `ompt_get_num_devices` does not. Regardless when the function is called, the returned value is always a fixed value of `1`. This can be explained by the [source code behind this function](https://github.com/RadeonOpenCompute/llvm-project/blob/amd-stg-open/openmp/runtime/src/ompt-general.cpp#L857):

```C
OMPT_API_ROUTINE int ompt_get_num_devices(void) {
  return 1; // only one device (the current device) is available
}
```

This issue can affect the proper initialization of the OMPT interface when trying to allocate buffers. Without this function, one would need to check the `device_num` in each `ompt_device_initialize` to allocate buffers accordingly. This is possible, but not ideal. 

**Reproduce the issue:**
On a system with more than one available AMD GPU, you can use the following source code:

```C
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <omp-tools.h>

ompt_finalize_tool_t ompt_finalize_tool;

static int
initialize_tool( ompt_function_lookup_t lookup,
                 int                    initialDeviceNum,
                 ompt_data_t*           toolData )
{
    ompt_set_callback_t set_callback =
        ( ompt_set_callback_t )lookup( "ompt_set_callback" );
    assert( set_callback != 0 );
    ompt_finalize_tool =
        ( ompt_finalize_tool_t )lookup( "ompt_finalize_tool" );
    assert( ompt_finalize_tool != 0 );
    ompt_get_num_devices_t get_num_devices =
        ( ompt_get_num_devices_t )lookup( "ompt_get_num_devices" );
    assert( get_num_devices != 0 );
    int num_devices = get_num_devices();
    assert( num_devices > 1 );

    return 1;
}

static void
finalize_tool( ompt_data_t* toolData )
{
    printf("%s\n", __FUNCTION__);
}

ompt_start_tool_result_t*
ompt_start_tool( unsigned int omp_version, /* == _OPENMP */
                 const char*  runtime_version )
{
    static ompt_start_tool_result_t tool = { &initialize_tool,
                                             &finalize_tool,
                                             ompt_data_none };
    return &tool;
}

#define N 10
int main(void) {
    int a[N];
    #pragma omp target map(a[:N])
    {
        a[N-1] = 0;
    }
    ompt_finalize_tool();
    return a[N - 1];
}
```

Compiling and running the tool with ROCm 5.4.x yields the following output

```bash
> amdclang -fopenmp -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=gfx90a -O3 -g error_ompt_get_num_devices.c -o error_ompt_get_num_devices
> ./error_ompt_get_num_devices 
error_ompt_get_num_devices: error_ompt_get_num_devices.c:23: int initialize_tool(ompt_function_lookup_t, int, ompt_data_t *): Assertion `num_devices > 1' failed.
Aborted
```

---

## 评论 (13 条)

### 评论 #1 — Thyre (2023-04-27T08:00:26Z)

Like suggested, I tried to use the `omp_get_num_devices()` function at different points in our code, outside of the `OMPT` functions. Unfortunately, it seems like the `omp_get_num_devices()` function returns a value of `0` until entering the first OpenMP directive / function on the host side. This will trigger `ompt_start_tool`.

I've built this small example in C++ to show the current issue.

**main.cpp**
```CPP
#include <omp.h>
#include <stdio.h>

#define N 10

int main( int argc, char** argv )
{
    printf("Before first OpenMP function call\n");
    printf("omp_get_num_devices in main returns %d\n", omp_get_num_devices());

    int a[N];
    #pragma omp target teams distribute parallel for map(a[:N])
    for(int i = 0; i < N; ++i)
    {
        a[i] = 0;
    }
    return a[N-1];
}
```

**main_ompt.cpp**
```CPP
#include <assert.h>
#include <omp.h>
#include <omp-tools.h>
#include <stdio.h>

static int main_ompt_num_devices = omp_get_num_devices();

// Init functions
int ompt_initialize( ompt_function_lookup_t lookup,
                     int initial_device_num,
                     ompt_data_t *tool_data)
{
    ompt_get_num_devices_t ompt_get_num_devices =
        ( ompt_get_num_devices_t )lookup( "ompt_get_num_devices" );
    assert( ompt_get_num_devices != 0 );

    printf("omp_get_num_devices before ompt_start_tool returns %d\n", main_ompt_num_devices);
    printf("omp_get_num_devices in initialize_tool returns %d\n", omp_get_num_devices());
    printf("ompt_get_num_devices returns %d\n", ompt_get_num_devices());
      
    return 1; //success
}

void ompt_finalize(ompt_data_t *tool_data)
{
}

// ompt_start_tool must be defined for a tool to use OMPT
#ifdef __cplusplus
extern "C" {
#endif
ompt_start_tool_result_t *ompt_start_tool( unsigned int omp_version,
                                           const char *runtime_version )
{
  printf("ompt_start_tool called\n");
  static ompt_start_tool_result_t ompt_start_tool_result = {&ompt_initialize,&ompt_finalize, 0};
  return &ompt_start_tool_result;
}
#ifdef __cplusplus
}
#endif
```

Compiling and running the tool yields the following output:
```bash
> amdclang++ -fopenmp -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=gfx90a -O3 -g main.cpp main_ompt.cpp
> ./a.out
ompt_start_tool called
omp_get_num_devices before ompt_start_tool returns 0
omp_get_num_devices in initialize_tool returns 0
ompt_get_num_devices returns 1
Before first OpenMP function call
omp_get_num_devices in main returns 8
```

Looking at this problem more closely with `LIBOMPTARGET_DEBUG=1`, we see the output down below. The interesting things here are, that the OMPT library is completely initialized before loading CUDA RTL / AMDGPU RTL. I would guess that those RTLs set the number of devices for `omp_get_num_devices`. After `ompt_init` has finished, we are able to call `omp_get_num_devices()` and get the right number of GPUs:
```
Libomptarget --> Init target library!
Libomptarget --> OMPT: Entering ompt_init
Libomptarget --> OMPT: Trying to load library libomp.so
Libomptarget --> OMPT: Trying to get address of connection routine libomp_ompt_connect
Libomptarget --> OMPT: Library connection handle = 0x14a23a3da730
ompt_start_tool called
Libomptarget --> Call to omp_get_num_devices returning 0
omp_get_num_devices before ompt_start_tool returns 0
Libomptarget --> Call to omp_get_num_devices returning 0
omp_get_num_devices in initialize_tool returns 0
ompt_get_num_devices returns 1
Libomptarget --> OMPT: Exit ompt_init
Libomptarget --> Loading RTLs...
Libomptarget --> Loading library 'libomptarget.rtl.ppc64.so'...
Libomptarget --> Unable to load 'libomptarget.rtl.ppc64.so': libomptarget.rtl.ppc64.so: cannot open shared object file: No such file or directory!
Libomptarget --> Loading library 'libomptarget.rtl.x86_64.so'...
Libomptarget --> Successfully loaded library 'libomptarget.rtl.x86_64.so'!
Libomptarget --> Registering RTL libomptarget.rtl.x86_64.so supporting 4 devices!
Libomptarget --> Loading library 'libomptarget.rtl.cuda.so'...
Target CUDA RTL --> Start initializing CUDA
Target CUDA RTL --> Unable to load library 'libcuda.so': libcuda.so: cannot open shared object file: No such file or directory!
Target CUDA RTL --> Failed to load CUDA shared library
Libomptarget --> Successfully loaded library 'libomptarget.rtl.cuda.so'!
Libomptarget --> No devices supported in this RTL
Libomptarget --> Loading library 'libomptarget.rtl.aarch64.so'...
Libomptarget --> Unable to load 'libomptarget.rtl.aarch64.so': libomptarget.rtl.aarch64.so: cannot open shared object file: No such file or directory!
Libomptarget --> Loading library 'libomptarget.rtl.ve.so'...
Libomptarget --> Unable to load 'libomptarget.rtl.ve.so': libomptarget.rtl.ve.so: cannot open shared object file: No such file or directory!
Libomptarget --> Loading library 'libomptarget.rtl.amdgpu.so'...
Target AMDGPU RTL --> Start initializing AMDGPU
Target AMDGPU RTL --> There are 8 devices supporting HSA.
Target AMDGPU RTL --> Alloc allowed in memory pool check failed: HSA_STATUS_ERROR: A generic error has occurred.
Target AMDGPU RTL --> Alloc allowed in memory pool check failed: HSA_STATUS_ERROR: A generic error has occurred.
Target AMDGPU RTL --> Alloc allowed in memory pool check failed: HSA_STATUS_ERROR: A generic error has occurred.
Target AMDGPU RTL --> Alloc allowed in memory pool check failed: HSA_STATUS_ERROR: A generic error has occurred.
Target AMDGPU RTL --> Alloc allowed in memory pool check failed: HSA_STATUS_ERROR: A generic error has occurred.
Target AMDGPU RTL --> Alloc allowed in memory pool check failed: HSA_STATUS_ERROR: A generic error has occurred.
Target AMDGPU RTL --> Alloc allowed in memory pool check failed: HSA_STATUS_ERROR: A generic error has occurred.
Target AMDGPU RTL --> Alloc allowed in memory pool check failed: HSA_STATUS_ERROR: A generic error has occurred.
Target AMDGPU RTL --> Device 0: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 1: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 2: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 3: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 4: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 5: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 6: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 7: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> OMPT: Entering ompt_init
Target AMDGPU RTL --> OMPT: Trying to load library libomptarget.so
Target AMDGPU RTL --> OMPT: Trying to get address of connection routine libomptarget_ompt_connect
Target AMDGPU RTL --> OMPT: Library connection handle = 0x14a23a2b7310
Libomptarget --> OMPT: Enter libomptarget_ompt_connect: OMPT enabled == 0
Libomptarget --> OMPT: Leave libomptarget_ompt_connect
Target AMDGPU RTL --> OMPT: Exiting ompt_init
Libomptarget --> Successfully loaded library 'libomptarget.rtl.amdgpu.so'!
Libomptarget --> Registering RTL libomptarget.rtl.amdgpu.so supporting 8 devices!
Libomptarget --> Loading library 'libomptarget.rtl.rpc.so'...
Libomptarget --> Unable to load 'libomptarget.rtl.rpc.so': libomptarget.rtl.rpc.so: cannot open shared object file: No such file or directory!
Libomptarget --> RTLs loaded!
Libomptarget -->  register_image_info image 0 of 1 offload-arch:gfx90a VERSION:1
Libomptarget --> Image 0x0000000000200c30 is NOT compatible with RTL libomptarget.rtl.x86_64.so!
Libomptarget --> Image 0x0000000000200c30 is compatible with RTL libomptarget.rtl.amdgpu.so!
Libomptarget --> RTL 0x0000000001b14e70 has index 0!
Libomptarget --> Registering image 0x0000000000200c30 with RTL libomptarget.rtl.amdgpu.so!
Libomptarget --> Done registering entries!
Libomptarget --> Call to omp_get_num_devices returning 8
Before first OpenMP function call
Libomptarget --> Call to omp_get_num_devices returning 8
omp_get_num_devices in main returns 8
Libomptarget --> Entering target region with entry point 0x0000000000200be0 and device Id -1
Libomptarget --> Call to omp_get_num_devices returning 8
Libomptarget --> Default TARGET OFFLOAD policy is now mandatory (devices were found)
Libomptarget --> Use default device id 0
Libomptarget --> Call to omp_get_num_devices returning 8
Libomptarget --> Call to omp_get_num_devices returning 8
Libomptarget --> Call to omp_get_initial_device returning 8
Libomptarget --> Checking whether device 0 is ready.
Libomptarget --> Is the device 0 (local ID 0) initialized? 0
Target AMDGPU RTL --> Init requires flags to 1
Target AMDGPU RTL --> Initialize the device id: 0
Target AMDGPU RTL --> Using 104 compute unis per grid
Target AMDGPU RTL --> Using 1024 ROCm blocks per grid
Target AMDGPU RTL --> Capped thread limit: 1024
Target AMDGPU RTL --> Queried wavefront size: 64
Target AMDGPU RTL --> Default number of teams = 4 * number of compute units 104
Target AMDGPU RTL --> Default number of threads set according to library's default 256
Target AMDGPU RTL --> Device 0: default limit for groupsPerDevice 1024 & ThreadsPerGroup 1024
Target AMDGPU RTL --> Device 0: wavefront size 64, total threads 1024 x 1024 = 1048576
Libomptarget --> Device 0 is ready to use.
Target AMDGPU RTL --> ELFABIVERSION Version: 3
Target AMDGPU RTL --> Explicit Kernel Arg[0] "" (8, 0)
Target AMDGPU RTL --> Implicit Kernel Arg[1] "" (4, 8)
Target AMDGPU RTL --> Implicit Kernel Arg[2] "" (4, 12)
Target AMDGPU RTL --> Implicit Kernel Arg[3] "" (4, 16)
Target AMDGPU RTL --> Implicit Kernel Arg[4] "" (2, 20)
Target AMDGPU RTL --> Implicit Kernel Arg[5] "" (2, 22)
Target AMDGPU RTL --> Implicit Kernel Arg[6] "" (2, 24)
Target AMDGPU RTL --> Implicit Kernel Arg[7] "" (2, 26)
Target AMDGPU RTL --> Implicit Kernel Arg[8] "" (2, 28)
Target AMDGPU RTL --> Implicit Kernel Arg[9] "" (2, 30)
Target AMDGPU RTL --> Implicit Kernel Arg[10] "" (8, 48)
Target AMDGPU RTL --> Implicit Kernel Arg[11] "" (8, 56)
Target AMDGPU RTL --> Implicit Kernel Arg[12] "" (8, 64)
Target AMDGPU RTL --> Implicit Kernel Arg[13] "" (2, 72)
Target AMDGPU RTL --> Implicit Kernel Arg[14] "" (8, 88)
Target AMDGPU RTL --> Implicit Kernel Arg[15] "" (8, 104)
Target AMDGPU RTL --> [__omp_offloading_35_6f318d8_main_l12: kernarg seg size] (264 --> 264)
Target AMDGPU RTL --> Modules loaded successful? 1
Target AMDGPU RTL --> Exec Symbol type: 0
Target AMDGPU RTL --> Symbol omptarget_device_environment = 0x14a1394e7004 (16 bytes)
Target AMDGPU RTL --> Exec Symbol type: 0
Target AMDGPU RTL --> Symbol __omp_offloading_35_6f318d8_main_l12_exec_mode = 0x14a1394e0a02 (1 bytes)
Target AMDGPU RTL --> Exec Symbol type: 0
Target AMDGPU RTL --> Symbol __omp_offloading_35_6f318d8_main_l12_wg_size = 0x14a1394e0a00 (2 bytes)
Target AMDGPU RTL --> Exec Symbol type: 0
Target AMDGPU RTL --> Symbol needs_hostcall_buffer = 0x14a1394e7000 (4 bytes)
Target AMDGPU RTL --> Exec Symbol type: 1
Target AMDGPU RTL --> Kernel __omp_offloading_35_6f318d8_main_l12 --> 14a1394e09c0 symbol 9786 group segsize 40 pvt segsize 264 bytes kernarg
Target AMDGPU RTL --> "Module registering" succeeded
Target AMDGPU RTL --> Setting global device environment after load (16 bytes)
Target AMDGPU RTL --> AMDGPU module successfully loaded!
Target AMDGPU RTL --> Init kernel launch failed on AMDGPU Device 0 for image(0x0000000000200c30)!
 Target AMDGPU RTL --> No device_state symbol found, skipping initialization
Target AMDGPU RTL --> to find the kernel name: __omp_offloading_35_6f318d8_main_l12 size: 36
Target AMDGPU RTL --> Warning: Loading KernDesc '__omp_offloading_35_6f318d8_main_l12_kern_desc' - symbol not found, Target AMDGPU RTL --> After loading global for __omp_offloading_35_6f318d8_main_l12_wg_size WGSize = 256
Target AMDGPU RTL --> "Loading WGSize computation property" succeeded
Target AMDGPU RTL --> After loading global for __omp_offloading_35_6f318d8_main_l12_exec_mode ExecMode = 2
Target AMDGPU RTL --> "Loading computation property" succeeded
Target AMDGPU RTL --> Construct kernelinfo: ExecMode 2
Target AMDGPU RTL --> Entry point 0 maps to __omp_offloading_35_6f318d8_main_l12
Libomptarget --> Entry  0: Base=0x00007fff3f35c4b0, Begin=0x00007fff3f35c4b0, Size=40, Type=0x23, Name=a[:10]
Libomptarget --> loop trip count is 10.
Libomptarget --> Looking up mapping(HstPtrBegin=0x00007fff3f35c4b0, Size=40)...
Target AMDGPU RTL --> Tgt alloc data 40 bytes, (tgt:000014a139020000).
Libomptarget --> Creating new map entry with HstPtrBase=0x00007fff3f35c4b0, HstPtrBegin=0x00007fff3f35c4b0, TgtPtrBegin=0x000014a139020000, Size=40, DynRefCount=1, HoldRefCount=0, Name=a[:10]
Libomptarget --> Moving 40 bytes (hst:0x00007fff3f35c4b0) -> (tgt:0x000014a139020000)
Target AMDGPU RTL --> Submit data 40 bytes, (hst:00007fff3f35c4b0) -> (tgt:000014a139020000).
Target AMDGPU RTL --> locking_async_memcpy: lockingPtr=0x7fff3f35c4b0 lockedPtr=0x14a13954c4b0 Size = 40
Libomptarget --> There are 40 bytes allocated at target address 0x000014a139020000 - is new
Libomptarget --> Looking up mapping(HstPtrBegin=0x00007fff3f35c4b0, Size=40)...
Libomptarget --> Mapping exists with HstPtrBegin=0x00007fff3f35c4b0, TgtPtrBegin=0x000014a139020000, Size=40, DynRefCount=1 (update suppressed), HoldRefCount=0
Libomptarget --> Obtained target argument 0x000014a139020000 from host pointer 0x00007fff3f35c4b0
Libomptarget --> Launching target execution __omp_offloading_35_6f318d8_main_l12 with pointer 0x0000000001b1f810 (index=0).
Target AMDGPU RTL --> Run target team region thread_limit 0
Target AMDGPU RTL --> Arg_num: 1
Target AMDGPU RTL --> Offseted base: arg[0]:0x000014a139020000
Target AMDGPU RTL --> Preparing 256 threads
Target AMDGPU RTL --> Set default num of groups 416
Target AMDGPU RTL --> Using 1 teams due to loop trip count 10 and number of threads per block 256
Target AMDGPU RTL --> Final 1 NumGroups and 256 ThreadsPerGroup
Target AMDGPU RTL --> Malloced 0x149a30600000
Target AMDGPU RTL --> Implicit argument count: 15
Target AMDGPU RTL --> Setting fields of ImplicitArgs for COV5
Target AMDGPU RTL --> Kernel completed
Libomptarget --> Looking up mapping(HstPtrBegin=0x00007fff3f35c4b0, Size=40)...
Libomptarget --> Mapping exists with HstPtrBegin=0x00007fff3f35c4b0, TgtPtrBegin=0x000014a139020000, Size=40, DynRefCount=0 (decremented, delayed deletion), HoldRefCount=0
Libomptarget --> There are 40 bytes allocated at target address 0x000014a139020000 - is last
Libomptarget --> Moving 40 bytes (tgt:0x000014a139020000) -> (hst:0x00007fff3f35c4b0)
Target AMDGPU RTL --> Retrieve data 40 bytes, (tgt:000014a139020000) -> (hst:00007fff3f35c4b0).
Target AMDGPU RTL --> dataRetrieve: Creating AsyncData with HostPtr 0x7fff3f35c4b0 HstOrPoolPtr 0x7fff3f35c4b0
Target AMDGPU RTL --> DONE Retrieve data 40 bytes, (tgt:000014a139020000) -> (hst:00007fff3f35c4b0).
Target AMDGPU RTL --> releaseResource for HstPtr 0x7fff3f35c4b0	 HstOrPoolPtr 0x7fff3f35c4b0
Target AMDGPU RTL --> Calling hsa_amd_memory_unlock 0x7fff3f35c4b0
Target AMDGPU RTL --> releaseResource for HstPtr 0x7fff3f35c4b0	 HstOrPoolPtr 0x7fff3f35c4b0
Libomptarget --> Looking up mapping(HstPtrBegin=0x00007fff3f35c4b0, Size=40)...
Libomptarget --> Deleting tgt data 0x000014a139020000 of size 40
Target AMDGPU RTL --> Tgt free data (tgt:000014a139020000).
Target AMDGPU RTL --> Freed 0x14a139020000
Libomptarget --> Removing map entry with HstPtrBegin=0x00007fff3f35c4b0, TgtPtrBegin=0x000014a139020000, Size=40, Name=a[:10]
Libomptarget --> Unloading target library!
Libomptarget --> Image 0x0000000000200c30 is compatible with RTL 0x0000000001b14e70!
Libomptarget --> Unregistered image 0x0000000000200c30 from RTL 0x0000000001b14e70!
Libomptarget --> Done unregistering images!
Libomptarget --> Removing translation table for descriptor 0x000000000020a8c0
Libomptarget --> Done unregistering library!
Libomptarget --> Deinit target library!
Target AMDGPU RTL --> Finalizing the AMDGPU DeviceInfo.
Target AMDGPU RTL --> Fini kernel launch failed on AMDGPU Device 0 for image(0x0000000000200c30)!
 Target AMDGPU RTL --> Fini kernel launch failed on AMDGPU Device 1 for image(0x0000000000200c30)!
 Target AMDGPU RTL --> Fini kernel launch failed on AMDGPU Device 2 for image(0x0000000000200c30)!
 Target AMDGPU RTL --> Fini kernel launch failed on AMDGPU Device 3 for image(0x0000000000200c30)!
 Target AMDGPU RTL --> Fini kernel launch failed on AMDGPU Device 4 for image(0x0000000000200c30)!
 Target AMDGPU RTL --> Fini kernel launch failed on AMDGPU Device 5 for image(0x0000000000200c30)!
 Target AMDGPU RTL --> Fini kernel launch failed on AMDGPU Device 6 for image(0x0000000000200c30)!
 Target AMDGPU RTL --> Fini kernel launch failed on AMDGPU Device 7 for image(0x0000000000200c30)!
 Target AMDGPU RTL --> Freed 0x149a30600000
```

---

### 评论 #2 — Thyre (2023-04-27T08:19:18Z)

Calling `omp_get_num_devices()` at any point **after** `ompt_init` has finished works for ROCm / aomp and returns the number of devices correctly. So, one could use the function at the first device initialization. However, theoretically it is against the OpenMP specifications and can cause issues with other runtimes. This is the case for NVHPC where the tool (sometimes) deadlocks when calling this function inside of an `ompt_[...]` function.

**Code:**

main.cpp
```C++
#include <omp.h>
#include <stdio.h>

#define N 10

int main( void )
{
    printf("Before first OpenMP function call\n");
//    printf("omp_get_num_devices in main returns %d\n", omp_get_num_devices());

    int a[N];
    #pragma omp target teams distribute parallel for map(a[:N])
    for(int i = 0; i < N; ++i)
    {
        a[i] = 0;
    }
    return a[N-1];
}
```

main_ompt.cpp
```C++
#include <assert.h>
#include <omp.h>
#include <omp-tools.h>
#include <stdio.h>

#define register_ompt_callback_t(name, type)                                   \
  do {                                                                         \
    type f_##name = &on_##name;                                                \
    if (ompt_set_callback(name, (ompt_callback_t)f_##name) == ompt_set_never)  \
      printf("0: Could not register callback '" #name "'\n");                  \
  } while (0)
#define register_ompt_callback(name) register_ompt_callback_t(name, name##_t)

static ompt_set_callback_t ompt_set_callback;
static int main_ompt_num_devices = omp_get_num_devices();

// Synchronous callbacks
// The device init callback must obtain the handles to the tracing
// entry points, if required.
static void on_ompt_callback_device_initialize( int device_num,
	                                 	const char *type,
					      	ompt_device_t *device,
					      	ompt_function_lookup_t lookup,
					      	const char *documentation) 
{
    printf("omp_get_num_devices in device_initialize %d\n", omp_get_num_devices());
}

// Called at device finalize
static void on_ompt_callback_device_finalize( int device_num ) 
{
    printf("omp_get_num_devices in device_finalize %d\n", omp_get_num_devices());
}

// Init functions
int ompt_initialize( ompt_function_lookup_t lookup,
                     int initial_device_num,
                     ompt_data_t *tool_data)
{
    ompt_set_callback = (ompt_set_callback_t) lookup("ompt_set_callback");

    if (!ompt_set_callback) return 0; // failed
    ompt_get_num_devices_t ompt_get_num_devices =
        ( ompt_get_num_devices_t )lookup( "ompt_get_num_devices" );
    assert( ompt_get_num_devices != 0 );

    printf("omp_get_num_devices before ompt_start_tool returns %d\n", main_ompt_num_devices);
    printf("omp_get_num_devices in initialize_tool returns %d\n", omp_get_num_devices());
    printf("ompt_get_num_devices returns %d\n", ompt_get_num_devices());
      
    register_ompt_callback(ompt_callback_device_initialize);
    register_ompt_callback(ompt_callback_device_finalize);
    return 1; //success
}

void ompt_finalize(ompt_data_t *tool_data)
{
    printf("omp_get_num_devices in finalize_tool returns %d\n", omp_get_num_devices());
}

// ompt_start_tool must be defined for a tool to use OMPT
#ifdef __cplusplus
extern "C" {
#endif
ompt_start_tool_result_t *ompt_start_tool( unsigned int omp_version,
                                           const char *runtime_version )
{
  printf("ompt_start_tool called\n");
  static ompt_start_tool_result_t ompt_start_tool_result = {&ompt_initialize,&ompt_finalize, 0};
  return &ompt_start_tool_result;
}
#ifdef __cplusplus
}
#endif

```


**Output:**
```bash
> amdclang++ -fopenmp -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=gfx90a -O3 -g main.cpp main_ompt.cpp
> ./a.out
ompt_start_tool called
omp_get_num_devices before ompt_start_tool returns 0
omp_get_num_devices in initialize_tool returns 0
ompt_get_num_devices returns 1
Before first OpenMP function call
omp_get_num_devices in device_initialize 8
omp_get_num_devices in finalize_tool returns 8
omp_get_num_devices in device_finalize 8
```

---

### 评论 #3 — dhruvachak (2023-05-22T17:52:21Z)

```
Calling `omp_get_num_devices()` at any point **after** `ompt_init` has finished works for ROCm / aomp and returns the number of devices correctly. So, one could use the function at the first device initialization. However, theoretically it is against the OpenMP specifications and can cause issues with other runtimes. 
```
@Thyre Can you please point out where the OMPT spec mentions that a tool is not allowed to call omp_ APIs from within a callback? While I haven't looked at the implementation of omp_get_num_devices, it seems from your description that until a device-specific plugin is initialized, the implementation may not know whether a device is available or not.

What I found in the spec is the following:
```
Restrictions on OMPT runtime entry points are as follows:
• OMPT runtime entry points must not be called from a signal handler on a native thread
before a native-thread-begin or after a native-thread-end event.
• OMPT device runtime entry points must not be called after a device-finalize event for that
device.
```

---

### 评论 #4 — Thyre (2023-05-22T17:56:37Z)

You can find the restriction in the OpenMP 5.2 spec in section 19.5:

```
The C/C++ header file (omp-tools.h) provides the definitions of the types that are specified throughout this subsection. Restrictions to the OpenMP tool callbacks are as follows:

Restrictions
• Tool callbacks may not use OpenMP directives or call any runtime library routines described in Chapter 18.
• Tool callbacks must exit by either returning to the caller or aborting

```

---

### 评论 #5 — dhruvachak (2023-05-22T18:23:01Z)

Ok, thanks! Is it possible to call omp_get_num_devices after device initialization from the tool but not from an OMPT callback? I would think that the workflow of your tool could make this call based on whether device initialization callback has been received. Perhaps this would require some delayed initialization of the tool maintained metadata.

---

### 评论 #6 — Thyre (2023-05-23T13:09:02Z)

It would be quite hard to achieve this. 

I've had another look at an example code I'm using right now for checking multiple target devices. I've noticed that we can see a few host events before the target side is even initialized. This means that we cannot use our subsystem methods to determine the number of target devices which would probably have been the best spot between `ompt_start_tool` and OMPT callback events which does not rely on OMPT. 

You can see the issue in the output of Score-P and `LIBOMPTARGET_DEBUG=-1` down below. The target side of OMPT is initialized on the first usage of a directive / function which utilizes target devices which means that `ompt_callback_device_initialize` is probably the first time where we would be able to use `omp_get_num_devices()`. This works, but is technically not allowed.

```
Apptainer> LIBOMPTARGET_DEBUG=-1 SCOREP_DEBUG=OMPT ./test_omp_memcpy.rocm 
Libomptarget --> Init target library!
Libomptarget --> OMPT: Entering ompt_init
Libomptarget --> OMPT: Trying to load library libomp.so
Libomptarget --> OMPT: Trying to get address of connection routine libomp_ompt_connect
Libomptarget --> OMPT: Library connection handle = 0x14cc81e21790
[Score-P] Active debug module(s): OMPT
[Score-P - 0] src/adapters/ompt/scorep_ompt_mgmt.c:71: [ompt_start_tool] omp_version="201611"; runtime_version="LLVM OMP version: 5.0.20140926"
[Score-P - 0] src/adapters/ompt/scorep_ompt_mgmt.c:342: [ompt_subsystem_register] OMPT subsystem id: 5
[Score-P - 0] src/adapters/ompt/scorep_ompt_mgmt.c:351: [ompt_subsystem_init] register paradigm
[Score-P - 0] src/adapters/ompt/scorep_ompt_mgmt.c:425: [ompt_subsystem_init_location] initial location 0x14cc808683e8
[Score-P - 0] src/adapters/ompt/scorep_ompt_mgmt.c:379: [ompt_subsystem_begin] start recording OMPT events
Libomptarget --> Call to omp_get_num_devices returning 0
Libomptarget --> Call to omp_get_num_devices returning 0
[Score-P - 0] src/adapters/ompt/scorep_ompt_mgmt.c:127: [initialize_tool] initial_device_num=0
[...]
[Score-P - 0] src/adapters/ompt/scorep_ompt_events_host.inc.c:357: [scorep_ompt_cb_host_thread_begin] atid 1 | thread_type initial
[Score-P - 0] src/adapters/ompt/scorep_ompt_events_host.inc.c:672: Entering function 'scorep_ompt_cb_host_implicit_task': atid 1 | endpoint begin | parallel_data->ptr (nil) | task_data->ptr (nil) | actual_parallelism 1 | index 1 | flags initial
[Score-P - 0] src/adapters/ompt/scorep_ompt_events_host.inc.c:692: Leaving function 'scorep_ompt_cb_host_implicit_task': atid 1 | initial_task: task_data->ptr 0x14cc822bcbd0 | implicit_parallel: parallel_data->ptr 0x14cc822bcc38 | location 0x14cc808683e8
Libomptarget --> OMPT: enter libomptarget_ompt_initialize!
Libomptarget --> ompt_set_frame_enter=0x14cc81e22e90
Libomptarget --> ompt_get_task_data=0x14cc81e22ee0
Libomptarget --> ompt_get_target_task_data=0x14cc81e22f20
Libomptarget --> OMPT: class bound ompt_callback_device_initialize=0x14cc822b5fa0
Libomptarget --> OMPT: class bound ompt_callback_device_finalize=0x14cc822b68c0
Libomptarget --> OMPT: class bound ompt_callback_device_load=0x14cc822b61a0
Libomptarget --> OMPT: class bound ompt_callback_device_unload=0x14cc822b6700
Libomptarget --> OMPT: class bound ompt_callback_target=(nil)
Libomptarget --> OMPT: class bound ompt_callback_target_data_op=(nil)
Libomptarget --> OMPT: class bound ompt_callback_target_submit=(nil)
Libomptarget --> OMPT: class bound ompt_callback_target_map=(nil)
Libomptarget --> OMPT: class bound ompt_callback_target_emi=0x14cc822b69a0
Libomptarget --> OMPT: class bound ompt_callback_target_data_op_emi=0x14cc822b6ca0
Libomptarget --> OMPT: class bound ompt_callback_target_submit_emi=0x14cc822b7720
Libomptarget --> OMPT: class bound ompt_callback_target_map_emi=0x14cc822b7570
Libomptarget --> OMPT: exit libomptarget_ompt_initialize!
Libomptarget --> OMPT: Exit ompt_init
Libomptarget --> Loading RTLs...
[...]
Libomptarget --> Loading library 'libomptarget.rtl.amdgpu.so'...
Target AMDGPU RTL --> Start initializing AMDGPU
Target AMDGPU RTL --> There are 8 devices supporting HSA.
Target AMDGPU RTL --> Device 0: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 1: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 2: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 3: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 4: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 5: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 6: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> Device 7: Initial groupsPerDevice 128 & ThreadsPerGroup 256
Target AMDGPU RTL --> OMPT: Entering ompt_init
Target AMDGPU RTL --> OMPT: Trying to load library libomptarget.so
Target AMDGPU RTL --> OMPT: Trying to get address of connection routine libomptarget_ompt_connect
Target AMDGPU RTL --> OMPT: Library connection handle = 0x14cc81cfe4e0
Libomptarget --> OMPT: Enter libomptarget_ompt_connect: OMPT enabled == 1
Target AMDGPU RTL --> OMPT: Enter ompt_device_init
Target AMDGPU RTL --> OMPT: libomptarget_get_target_info = 0x14cc81cfdcd0
Target AMDGPU RTL --> OMPT: class bound ompt_callback_device_initialize=0x14cc822b5fa0
Target AMDGPU RTL --> OMPT: class bound ompt_callback_device_finalize=0x14cc822b68c0
Target AMDGPU RTL --> OMPT: class bound ompt_callback_device_load=0x14cc822b61a0
Target AMDGPU RTL --> OMPT: class bound ompt_callback_device_unload=0x14cc822b6700
Target AMDGPU RTL --> OMPT: class bound ompt_callback_target=(nil)
Target AMDGPU RTL --> OMPT: class bound ompt_callback_target_data_op=(nil)
Target AMDGPU RTL --> OMPT: class bound ompt_callback_target_submit=(nil)
Target AMDGPU RTL --> OMPT: class bound ompt_callback_target_map=(nil)
Target AMDGPU RTL --> OMPT: class bound ompt_callback_target_emi=0x14cc822b69a0
Target AMDGPU RTL --> OMPT: class bound ompt_callback_target_data_op_emi=0x14cc822b6ca0
Target AMDGPU RTL --> OMPT: class bound ompt_callback_target_submit_emi=0x14cc822b7720
Target AMDGPU RTL --> OMPT: class bound ompt_callback_target_map_emi=0x14cc822b7570
Target AMDGPU RTL --> OMPT: Exit ompt_device_init
Libomptarget --> OMPT: Leave libomptarget_ompt_connect
Target AMDGPU RTL --> OMPT: Exiting ompt_init
Libomptarget --> Successfully loaded library 'libomptarget.rtl.amdgpu.so'!
Libomptarget --> Registering RTL libomptarget.rtl.amdgpu.so supporting 8 devices!
Libomptarget --> Loading library 'libomptarget.rtl.rpc.so'...
Libomptarget --> Unable to load 'libomptarget.rtl.rpc.so': libomptarget.rtl.rpc.so: cannot open shared object file: No such file or directory!
Libomptarget --> RTLs loaded!
Libomptarget -->  register_image_info image 0 of 1 offload-arch:gfx90a VERSION:1
Libomptarget --> Image 0x0000000000201730 is NOT compatible with RTL libomptarget.rtl.x86_64.so!
Libomptarget --> Image 0x0000000000201730 is compatible with RTL libomptarget.rtl.amdgpu.so!
Libomptarget --> RTL 0x000000000221dd50 has index 0!
Libomptarget --> Registering image 0x0000000000201730 with RTL libomptarget.rtl.amdgpu.so!
Libomptarget --> Done registering entries!
Libomptarget --> Call to omp_get_num_devices returning 8
```

---

### 评论 #7 — dhruvachak (2023-05-23T16:44:58Z)

I agree that omp_get_num_devices() will return the correct value if called after the device-init callback is received. If you want to avoid calling omp_get_num_devices() in the callback, I am suggesting the following: (1) Set a Score-P internal attribute recording that the device-init callback has been received. (2) Within the Score-P machinery, create a method checking whether that attribute is set and if so, call omp_get_num_devices(). You may have to call this method at multiple points in the Score-P workflow.

The scenario where the above suggestion won't work is if Score-P needs to initialize data structures based on the number of devices before the device-init callback is received. But, from your description, it does not look like that is the case for you. It would also be non-intuitive since I would think that Score-P should want to initialize device-specific metadata only after the device-init callback is received. 

This is the definition of omp_get_num_devices() from the spec. 
```
The omp_get_num_devices routine returns the number of non-host devices available for offloading code or data.
```
Note "available". Just because there are some GPUs on the system, it does not mean that all of them are available for offloading, given the binary. That guarantee is provided only after the device libraries are loaded and the number of compatible agents validated. 

---

### 评论 #8 — dhruvachak (2023-08-03T17:10:49Z)

@Thyre Does the suggested workaround work for you?

---

### 评论 #9 — Thyre (2023-08-03T17:16:37Z)

Right now, we use this code to get the correct number of available devices during `ompt_callback_device_initialize` which is just early enough to work:

```c
#ifdef __llvm__
    if ( scorep_ompt_devices == NULL )
    {
        scorep_ompt_num_devices = omp_get_num_devices();
        UTILS_BUG_ON( scorep_ompt_num_devices <= 0 );
        [...]
    }
#endif
```

This works as a workaround and I think we will stick with that for the foreseeable future. If there's a runtime which reports the correct number of GPUs when calling `ompt_get_num_devices`  (not `1`), we will use that value instead.


---

### 评论 #10 — ppanchad-amd (2024-05-10T19:12:17Z)

@Thyre Is this ticket still relevant? If not, please close. Thanks!

---

### 评论 #11 — Thyre (2024-05-12T11:28:01Z)

> @Thyre Is this ticket still relevant? If not, please close. Thanks!

As far as I am aware of, this is still an issue of ROCm (and upstream LLVM). LLVM still uses a generic value (see [here](https://github.com/llvm/llvm-project/blob/c8864bceeb20582b4e7a739d8ba3e11052f0e49f/openmp/runtime/src/ompt-general.cpp#L859)). 

While we have found a workaround for this, it should be fixed regardless.

---

### 评论 #12 — ppanchad-amd (2024-08-01T15:07:00Z)

@Thyre Internal ticket has been created to fix the issue. Thanks!

---

### 评论 #13 — jamesxu2 (2024-08-07T19:25:20Z)

Hello @Thyre , thanks for bringing up this issue. While you're right about ```ompt_get_num_devices``` essentially returning a placeholder value, we are not prioritizing the complete implementation of this callback at this time. 

Please continue with your workaround using **omp_get_num_devices** or follow @dhruvachak 's recommendations.  

---
