# [OMPT] Callbacks for target directives called after finalization of OMPT

> **Issue #2056**
> **状态**: closed
> **创建时间**: 2023-04-17T11:29:01Z
> **更新时间**: 2025-05-06T06:32:28Z
> **关闭时间**: 2025-05-06T06:32:27Z
> **作者**: Thyre
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2056

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

**Description:**

The OpenMP specification contains a method to manually finalize the OMPT interface. This method is called `ompt_finalize_tool`. This method is retrieved when initializing the OMPT interface via the lookup function. 

The OpenMP specification states the following effect when calling ompt_finalize_tool:

The ompt_finalize_tool routine detaches the tool from the runtime, unregisters all callbacks and invalidates all OMPT entry points passed to the tool in the lookup-function. **Upon completion of ompt_finalize_tool, no further callbacks will be issued on any thread. Before the callbacks are unregistered, the OpenMP runtime should attempt to dispatch all outstanding registered callbacks as well as the callbacks that would be encountered during shutdown of the runtime, if possible in the current execution context.** 

Link to the documentation: https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-5-2.pdf#page=546

Unfortunately, ROCm 5.4 and aomp 17.0 do not follow the specifications here. I've noticed that (at least) `ompt_callback_device_finalize` is called after calling `ompt_finalize_tool`. This seems to affect the `buffer_complete` callback for the device tracing interface as well. However, here we are able to flush the buffer and pause the trace just before calling `ompt_finalize_tool` which seems to work fine as a work around.

In general, sending events after finalizing the OMPT interface could lead to missing events in the resulting traces or even crashes of the tool if required pointers for handling the callbacks are freed. Right now, developers need to work around this issue and for example clean up memory at the latest possible point to ensure that all callbacks are handled. 

**Reproduce the issue:**
You can reproduce the issue by using the following C code:

```C
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <omp-tools.h>

bool                 tool_is_finalized = false;
ompt_finalize_tool_t ompt_finalize_tool;


void callback_ompt_device_initialize(int device_num,
                                     const char *type,
                                     ompt_device_t *device,
                                     ompt_function_lookup_t lookup,
                                     const char *documentation)
{
    assert(tool_is_finalized == false);
    printf("%s\n", __FUNCTION__);
}

void
callback_ompt_device_load( int         device_num,
                           const char* filename,
                           int64_t     offset_in_line,
                           void*       vma_in_file,
                           size_t      bytes,
                           void*       host_addr,
                           void*       device_addr,
                           uint64_t    module_id )
{
    assert(tool_is_finalized == false);
    printf("%s\n", __FUNCTION__);
}

void
callback_ompt_device_finalize( int device_num )
{
    assert(tool_is_finalized == false);
    printf("%s\n", __FUNCTION__);
}



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

    ompt_set_result_t registration_result = set_callback(ompt_callback_device_initialize, (ompt_callback_t) &callback_ompt_device_initialize);
    assert(registration_result == ompt_set_always);

    registration_result = set_callback(ompt_callback_device_load, (ompt_callback_t) &callback_ompt_device_load);
    assert(registration_result == ompt_set_always);

    registration_result = set_callback(ompt_callback_device_finalize, (ompt_callback_t) &callback_ompt_device_finalize);
    assert(registration_result == ompt_set_always);

    return 1;
}

static void
finalize_tool( ompt_data_t* toolData )
{
    printf("%s\n", __FUNCTION__);
    tool_is_finalized = true;
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
> amdclang -fopenmp -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=gfx90a -O3 -g error_ompt_callback_finalization.c -o error_ompt_callback_finalization
> ./error_ompt_callback_finalization 
callback_ompt_device_initialize
callback_ompt_device_load
finalize_tool
error_ompt_callback_finalization: error_ompt_callback_finalization.c:37: void callback_ompt_device_finalize(int): Assertion `tool_is_finalized == false' failed.
Aborted
```

---

## 评论 (6 条)

### 评论 #1 — dhruvachak (2023-08-03T17:07:38Z)

The current LLVM OMPT design and implementation do not take into account the specification of ompt_finalize_tool. I find the following language problematic to implement: "...as well as the callbacks that would be encountered during shutdown of the runtime."

---

### 评论 #2 — Thyre (2023-08-03T17:23:57Z)

I agree with that. If I remember correctly, at least one compiler completely ends the OpenMP runtime upon receiving `ompt_finalize_tool` which somewhat works, but breaks if a user implements an OpenMP directive after calling the function. 

From our side, we have implemented an explicit flush of the device tracing interface for every device which uses it. If all events are stored in the buffer, we will receive them. Regarding callback events, we will miss events sent after `ompt_finalize_tool` during profiling / tracing which will lead to missing events in Vampir and Cube. Missing `ompt_callback_device_finalize` isn't a problem, since we moved the cleanup to the latest possible point of the OMPT adapter, after the users code should have finished already. Other events would be potentially bad, especially when we think about analyzing the traces. 

---

### 评论 #3 — ppanchad-amd (2024-06-18T19:29:38Z)

@Thyre Can you please check if the issue still exists with the latest ROCm 6.1.2? Thanks!

---

### 评论 #4 — Thyre (2024-06-19T12:45:35Z)

> @Thyre Can you please check if the issue still exists with the latest ROCm 6.1.2? Thanks!

The issue is still present in ROCm 6.1.2, but is fixed in LLVM 19-trunk. LLVM 18.1.0 was still broken.

```console
$ amdclang --version                                  
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.2 24193 669db884972e769450470020c06a6f132a8a065b)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/apps/software/ROCm/6.1.2/lib/llvm/bin
Configuration file: /opt/apps/software/ROCm/6.1.2/lib/llvm/bin/clang.cfg
$ amdclang -fopenmp --offload-arch=gfx1101 reproducer.c
$ ./a.out
callback_ompt_device_initialize
callback_ompt_device_load
finalize_tool
a.out: reproducer.c:37: void callback_ompt_device_finalize(int): Assertion `tool_is_finalized == false' failed.
[1]    1983 IOT instruction (core dumped)  ./a.out
```

Upstream:
```console
$ clang --version
clang version 19.0.0git (https://github.com/llvm/llvm-project.git 0f323dc0c43bd45147bdf8ee9cbeef0d8f57165b)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/apps/software/Clang/trunk/bin
Build config: +assertions
$ clang -fopenmp --offload-arch=gfx1101 reproducer.c
$ ./a.out
callback_ompt_device_initialize
callback_ompt_device_load
finalize_tool
```

---

### 评论 #5 — tcgu-amd (2025-05-05T15:50:46Z)

@Thyre, ROCm 6.4 has upgraded to llvm19. Would you be able to see if the issue still persists? Thanks! 

---

### 评论 #6 — Thyre (2025-05-06T06:32:27Z)

Hi @tcgu-amd,
I've just checked ROCm 6.4, and it looks like the issue is resolved.
Thanks a lot!

---
