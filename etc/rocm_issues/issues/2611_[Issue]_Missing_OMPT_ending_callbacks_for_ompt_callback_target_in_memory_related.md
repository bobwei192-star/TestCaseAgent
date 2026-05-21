# [Issue]: Missing OMPT ending callbacks for ompt_callback_target in memory related operations

> **Issue #2611**
> **状态**: closed
> **创建时间**: 2023-10-27T17:10:28Z
> **更新时间**: 2024-02-01T15:53:58Z
> **关闭时间**: 2024-02-01T15:53:57Z
> **作者**: jordialcaraz
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2611

## 描述

### Problem Description

Callback end points are not called for kind target_enter_data and others may not be called for both begin and end, such as target_exit_data.

### Operating System

Ubuntu 22.04.2 LTS

### CPU

Xeon 8352V

### GPU

MI210

### ROCm Version

5.6.0, 5.7.0, 5.7.1

### ROCm Component

OMPT

### Steps to Reproduce

Load rocm/5.6.0
Download OMPT reporting tool  [ompt-printf-0.tar.gz](https://forums.developer.nvidia.com/uploads/short-url/nFcmpaiIk1rcZBBVEj2AS1yFHbW.gz)

Uncompress and compile it with:
```
tar xf ompt-printf-0.tar.gz
cd ompt-printf-0
./configure CC=amdclang --prefix=`pwd`/_install
make install
```

Download example from TAU and compile:
```
wget https://raw.githubusercontent.com/UO-OACISS/tau2/master/examples/openmp/target/matmult.c
amdclang   -g -O2 -fopenmp -target x86_64-pc-linux-gnu -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=gfx90a -c matmult.c -o matmult.o
amdclang   -g -fopenmp -target x86_64-pc-linux-gnu -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=gfx90a matmult.o -o matmult 
```

Execute it with the tool:
`LD_PRELOAD=/home/users/jalcaraz/tau2/examples/openmp/amd_target/test_callbacks/ompt-printf-0/install/libompt_tool.so ../matmult`


The output should look like this:

- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20d03d
- [callback_buffer_request] tid = 0| trace buffer for device 0 allocated
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7e241ff010 | dest_addr = (nil) | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f7f41091bde
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7e241ff010 | dest_addr = 0x7f7e1c000000 | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f7f41091bde
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20d095
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7e13fff010 | dest_addr = (nil) | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f7f41091bde
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7e13fff010 | dest_addr = 0x7f7e0be00000 | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f7f41091bde
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20d0ed
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7e03dff010 | dest_addr = (nil) | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f7f41091bde
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7e03dff010 | dest_addr = 0x7f7dfbc00000 | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f7f41091bde
- [parallel_begin_cb] tid = 0 | parallel_data = 7770001 | encountering_task_data = 6660001 | flags = invoker_runtime_team | requested_parallelism = 3 | codeptr_ra = 0x20d128
- [implicit_task_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | endpoint = begin | actual_parallelism = 3 | index = 0 | flags = implicit
- [work_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20c224
- [dispatch_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | kind = ws_loop_chunk
- [thread_begin_cb] tid = 1 | type = worker
- [implicit_task_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | endpoint = begin | actual_parallelism = 3 | index = 1 | flags = implicit
- [work_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20c224
- [dispatch_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | kind = ws_loop_chunk
- [thread_begin_cb] tid = 2 | type = worker
- [implicit_task_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | endpoint = begin | actual_parallelism = 3 | index = 2 | flags = implicit
- [work_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20c224
- [dispatch_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | kind = ws_loop_chunk
- [work_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20c249
- [sync_region_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d128
- [sync_region_wait_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d128
- [work_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20c249
- [sync_region_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [work_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20c249
- [sync_region_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660002 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d128
- [sync_region_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660002 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d128
- [implicit_task_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660002 | endpoint = end | actual_parallelism = 3 | index = 0 | flags = implicit
- [parallel_end_cb] tid = 0 | parallel_data = 7770001 | encountering_task = 6660001 | flags = invoker_runtime_team | codeptr_ra = 0x20d128
- [parallel_begin_cb] tid = 0 | parallel_data = 7770002 | encountering_task_data = 6660001 | flags = invoker_runtime_team | requested_parallelism = 3 | codeptr_ra = 0x20d15f
- [sync_region_wait_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660003 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660003 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660003 | endpoint = end | actual_parallelism = 0 | index = 1 | flags = implicit
- [implicit_task_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | endpoint = begin | actual_parallelism = 3 | index = 0 | flags = implicit
- [sync_region_wait_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660004 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660004 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660004 | endpoint = end | actual_parallelism = 0 | index = 2 | flags = implicit
- [work_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20c224
- [dispatch_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | kind = ws_loop_chunk
- [implicit_task_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660007 | endpoint = begin | actual_parallelism = 3 | index = 2 | flags = implicit
- [implicit_task_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660006 | endpoint = begin | actual_parallelism = 3 | index = 1 | flags = implicit
- [work_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660007 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20c224
- [dispatch_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660007 | kind = ws_loop_chunk
- [work_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660006 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20c224
- [dispatch_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660006 | kind = ws_loop_chunk
- [work_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20c249
- [sync_region_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d15f
- [sync_region_wait_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d15f
- [work_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660006 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20c249
- [sync_region_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660006 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660006 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [work_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660007 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20c249
- [sync_region_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660007 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660007 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660005 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d15f
- [sync_region_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660005 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d15f
- [implicit_task_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660005 | endpoint = end | actual_parallelism = 3 | index = 0 | flags = implicit
- [parallel_end_cb] tid = 0 | parallel_data = 7770002 | encountering_task = 6660001 | flags = invoker_runtime_team | codeptr_ra = 0x20d15f
- [parallel_begin_cb] tid = 0 | parallel_data = 7770003 | encountering_task_data = 6660001 | flags = invoker_runtime_team | requested_parallelism = 3 | codeptr_ra = 0x20d196
- [implicit_task_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | endpoint = begin | actual_parallelism = 3 | index = 0 | flags = implicit
- [sync_region_wait_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660006 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660006 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660006 | endpoint = end | actual_parallelism = 0 | index = 1 | flags = implicit
- [work_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20c224
- [dispatch_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | kind = ws_loop_chunk
- [sync_region_wait_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660007 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660007 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660007 | endpoint = end | actual_parallelism = 0 | index = 2 | flags = implicit
- [implicit_task_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660009 | endpoint = begin | actual_parallelism = 3 | index = 1 | flags = implicit
- [implicit_task_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660010 | endpoint = begin | actual_parallelism = 3 | index = 2 | flags = implicit
- [work_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660009 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20c224
- [dispatch_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660009 | kind = ws_loop_chunk
- [work_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660010 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20c224
- [dispatch_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660010 | kind = ws_loop_chunk
- [work_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20c249
- [sync_region_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d196
- [sync_region_wait_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d196
- [work_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660010 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20c249
- [sync_region_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660010 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660010 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [work_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660009 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20c249
- [sync_region_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660009 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660009 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660008 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d196
- [sync_region_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660008 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x20d196
- [implicit_task_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660008 | endpoint = end | actual_parallelism = 3 | index = 0 | flags = implicit
- [parallel_end_cb] tid = 0 | parallel_data = 7770003 | encountering_task = 6660001 | flags = invoker_runtime_team | codeptr_ra = 0x20d196
- compute_target
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20cc24
- [target_submit_emi_cb] tid = 0 | endpoint = begin
- [target_submit_emi_cb] tid = 0 | endpoint = end
- [target_emi_cb] tid = 0 | endpoint = end | kind = target | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20cc24
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20ccbb
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20d208
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7e1c000000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f7f41093693
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7e1c000000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f7f41093693
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20d25b
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7e0be00000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f7f41093693
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7e0be00000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f7f41093693
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20d2ae
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7dfbc00000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f7f41093693
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f7dfbc00000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f7f41093693
- Done.
- [implicit_task_cb] tid = 0 | parallel_data = 0 | task_data = 6660001 | endpoint = end | actual_parallelism = 0 | index = 1 | flags = initial
- [thread_end_cb] tid = 0
- [sync_region_wait_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660009 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660009 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660009 | endpoint = end | actual_parallelism = 0 | index = 1 | flags = implicit
- [thread_end_cb] tid = 1
- [sync_region_wait_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660010 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660010 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660010 | endpoint = end | actual_parallelism = 0 | index = 2 | flags = implicit
- [thread_end_cb] tid = 2
- [my_finalize_tool] tid = 0
- [device_finalize_cb] tid = 0

Looking at the output, we can see the callbacks and their begin and end points. In the case of callbacks for target that are data related, there are only begin and not ends. For example, if we look at the kind target_enter_data, there are only endpoint = begin:
`[target_emi_cb] tid = 0 | endpoint = begin | kind = target_enter_data `

If we compare this output to rocm/5.5.0, we observe that target_enter_data has endpoint=end and there is also an additional kind, the target_exit_data with both begin and end. This target_exit_data has dissapeared in rocm/5.6.0 and newer versions. 

Output from rocm/5.5.0:

- [callback_buffer_request] tid = 0| trace buffer for device 0 allocated
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f44341ff010 | dest_addr = (nil) | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f454f7a2efa
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f44341ff010 | dest_addr = 0x7f442c000000 | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f454f7a2efa
- [target_emi_cb] tid = 0 | endpoint = end | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x2101cd
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x210225
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f4423fff010 | dest_addr = (nil) | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f454f7a2efa
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f4423fff010 | dest_addr = 0x7f441be00000 | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f454f7a2efa
- [target_emi_cb] tid = 0 | endpoint = end | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x210225
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x21027d
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f4413dff010 | dest_addr = (nil) | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f454f7a2efa
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f4413dff010 | dest_addr = 0x7f440bc00000 | src_device_num = 1 | dest_device_num = 0 | optype = alloc | bytes = 134217728 | codeptr_ra = 0x7f454f7a2efa
- [target_emi_cb] tid = 0 | endpoint = end | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x21027d
- [parallel_begin_cb] tid = 0 | parallel_data = 7770001 | encountering_task_data = 6660001 | flags = invoker_runtime_team | requested_parallelism = 3 | codeptr_ra = 0x2102b8
- [implicit_task_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | endpoint = begin | actual_parallelism = 3 | index = 0 | flags = implicit
- [work_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20f3b4
- [dispatch_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | kind = ws_loop_chunk
- [thread_begin_cb] tid = 1 | type = worker
- [implicit_task_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | endpoint = begin | actual_parallelism = 3 | index = 1 | flags = implicit
- [work_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20f3b4
- [dispatch_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | kind = ws_loop_chunk
- [thread_begin_cb] tid = 2 | type = worker
- [implicit_task_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | endpoint = begin | actual_parallelism = 3 | index = 2 | flags = implicit
- [work_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20f3b4
- [dispatch_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | kind = ws_loop_chunk
- [work_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20f3d9
- [sync_region_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x2102b8
- [sync_region_wait_cb] tid = 0 | parallel_data = 7770001 | task_data = 6660002 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x2102b8
- [work_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20f3d9
- [sync_region_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 2 | parallel_data = 7770001 | task_data = 6660004 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [work_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20f3d9
- [sync_region_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 1 | parallel_data = 7770001 | task_data = 6660003 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660002 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x2102b8
- [sync_region_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660002 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x2102b8
- [implicit_task_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660002 | endpoint = end | actual_parallelism = 3 | index = 0 | flags = implicit
- [parallel_end_cb] tid = 0 | parallel_data = 7770001 | encountering_task = 6660001 | flags = invoker_runtime_team | codeptr_ra = 0x2102b8
- [parallel_begin_cb] tid = 0 | parallel_data = 7770002 | encountering_task_data = 6660001 | flags = invoker_runtime_team | requested_parallelism = 3 | codeptr_ra = 0x2102ef
- [sync_region_wait_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660004 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660004 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660004 | endpoint = end | actual_parallelism = 0 | index = 2 | flags = implicit
- [sync_region_wait_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660003 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660003 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660003 | endpoint = end | actual_parallelism = 0 | index = 1 | flags = implicit
- [implicit_task_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660006 | endpoint = begin | actual_parallelism = 3 | index = 2 | flags = implicit
- [implicit_task_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | endpoint = begin | actual_parallelism = 3 | index = 0 | flags = implicit
- [implicit_task_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660007 | endpoint = begin | actual_parallelism = 3 | index = 1 | flags = implicit
- [work_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660006 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20f3b4
- [dispatch_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660006 | kind = ws_loop_chunk
- [work_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20f3b4
- [dispatch_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | kind = ws_loop_chunk
- [work_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660007 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20f3b4
- [dispatch_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660007 | kind = ws_loop_chunk
- [work_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660006 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20f3d9
- [sync_region_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660006 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 2 | parallel_data = 7770002 | task_data = 6660006 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [work_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20f3d9
- [work_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660007 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20f3d9
- [sync_region_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x2102ef
- [sync_region_wait_cb] tid = 0 | parallel_data = 7770002 | task_data = 6660005 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x2102ef
- [sync_region_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660007 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 1 | parallel_data = 7770002 | task_data = 6660007 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660005 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x2102ef
- [sync_region_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660005 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x2102ef
- [implicit_task_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660005 | endpoint = end | actual_parallelism = 3 | index = 0 | flags = implicit
- [parallel_end_cb] tid = 0 | parallel_data = 7770002 | encountering_task = 6660001 | flags = invoker_runtime_team | codeptr_ra = 0x2102ef
- [parallel_begin_cb] tid = 0 | parallel_data = 7770003 | encountering_task_data = 6660001 | flags = invoker_runtime_team | requested_parallelism = 3 | codeptr_ra = 0x210326
- [implicit_task_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | endpoint = begin | actual_parallelism = 3 | index = 0 | flags = implicit
- [sync_region_wait_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660006 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660006 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660006 | endpoint = end | actual_parallelism = 0 | index = 2 | flags = implicit
- [sync_region_wait_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660007 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660007 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660007 | endpoint = end | actual_parallelism = 0 | index = 1 | flags = implicit
- [work_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20f3b4
- [dispatch_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | kind = ws_loop_chunk
- [implicit_task_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660009 | endpoint = begin | actual_parallelism = 3 | index = 2 | flags = implicit
- [implicit_task_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660010 | endpoint = begin | actual_parallelism = 3 | index = 1 | flags = implicit
- [work_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660009 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20f3b4
- [dispatch_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660009 | kind = ws_loop_chunk
- [work_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660010 | endpoint = begin | work_type = loop | count = 4096 | codeptr_ra = 0x20f3b4
- [dispatch_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660010 | kind = ws_loop_chunk
- [work_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20f3d9
- [sync_region_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x210326
- [sync_region_wait_cb] tid = 0 | parallel_data = 7770003 | task_data = 6660008 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = 0x210326
- [work_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660009 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20f3d9
- [sync_region_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660009 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 2 | parallel_data = 7770003 | task_data = 6660009 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [work_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660010 | endpoint = end | work_type = loop | count = 0 | codeptr_ra = 0x20f3d9
- [sync_region_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660010 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 1 | parallel_data = 7770003 | task_data = 6660010 | endpoint = begin | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_wait_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660008 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x210326
- [sync_region_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660008 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = 0x210326
- [implicit_task_cb] tid = 0 | parallel_data = 7777777 | task_data = 6660008 | endpoint = end | actual_parallelism = 3 | index = 0 | flags = implicit
- [parallel_end_cb] tid = 0 | parallel_data = 7770003 | encountering_task = 6660001 | flags = invoker_runtime_team | codeptr_ra = 0x210326
- compute_target
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20fcb6
- [target_emi_cb] tid = 0 | endpoint = end | kind = target_enter_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20fcb6
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20fdb4
- [target_submit_emi_cb] tid = 0 | endpoint = begin
- [target_submit_emi_cb] tid = 0 | endpoint = end
- [target_emi_cb] tid = 0 | endpoint = end | kind = target | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20fdb4
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_exit_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20fe4b
- [target_emi_cb] tid = 0 | endpoint = end | kind = target_exit_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x20fe4b
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_exit_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x210398
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f442c000000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f454f7a4573
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f442c000000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f454f7a4573
- [target_emi_cb] tid = 0 | endpoint = end | kind = target_exit_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x210398
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_exit_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x2103eb
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f441be00000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f454f7a4573
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f441be00000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f454f7a4573
- [target_emi_cb] tid = 0 | endpoint = end | kind = target_exit_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x2103eb
- [target_emi_cb] tid = 0 | endpoint = begin | kind = target_exit_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x21043e
- [target_data_op_emi_cb] tid = 0 | endpoint = begin | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f440bc00000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f454f7a4573
- [target_data_op_emi_cb] tid = 0 | endpoint = end | target_task_data = 0 | target_data = 0 | host_op_id = 1 | src_addr = 0x7f440bc00000 | dest_addr = (nil) | src_device_num = 0 | dest_device_num = -1 | optype = delete | bytes = 0 | codeptr_ra = 0x7f454f7a4573
- [target_emi_cb] tid = 0 | endpoint = end | kind = target_exit_data | device_num = 0 | task_data = 6660001 | target_task_data = 0 | target_data = 0 | codeptr_ra = 0x21043e
- Done.
- [implicit_task_cb] tid = 0 | parallel_data = 0 | task_data = 6660001 | endpoint = end | actual_parallelism = 0 | index = 1 | flags = initial
- [thread_end_cb] tid = 0
- [sync_region_wait_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660010 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660010 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 1 | parallel_data = 7777777 | task_data = 6660010 | endpoint = end | actual_parallelism = 0 | index = 1 | flags = implicit
- [thread_end_cb] tid = 1
- [sync_region_wait_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660009 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [sync_region_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660009 | endpoint = end | kind = barrier_implicit (deprecated) | codeptr_ra = (nil)
- [implicit_task_cb] tid = 2 | parallel_data = 7777777 | task_data = 6660009 | endpoint = end | actual_parallelism = 0 | index = 2 | flags = implicit
- [thread_end_cb] tid = 2
- [my_finalize_tool] tid = 0
- [device_finalize_cb] tid = 0


### Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    Intel(R) Xeon(R) Platinum 8352V CPU @ 2.10GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Xeon(R) Platinum 8352V CPU @ 2.10GHz
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
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3500                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            72                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    1044047432(0x3e3ae648) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    1044047432(0x3e3ae648) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    1044047432(0x3e3ae648) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    Intel(R) Xeon(R) Platinum 8352V CPU @ 2.10GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Xeon(R) Platinum 8352V CPU @ 2.10GHz
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3500                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            72                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    1044553552(0x3e429f50) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    1044553552(0x3e429f50) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    1044553552(0x3e429f50) KB          
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-14299f3ba2d8ea0d               
  Marketing Name:          AMD Instinct MI210                 
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29711(0x740f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   45824                              
  Internal Node ID:        2                                  
  Compute Unit:            104                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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


---

## 评论 (4 条)

### 评论 #1 — dhruvachak (2023-10-30T19:51:35Z)

I am looking at this problem. Can't assign the issue to me though because of permissions, I think.

---

### 评论 #2 — ronlieb (2023-11-09T22:15:32Z)

fix added to ROCm 6.0 RC2 

---

### 评论 #3 — Thyre (2023-12-15T22:40:49Z)

Yup, the bug initially occured back in AOMP, was then ported to ROCm 5.6 and is now fixed in the latest ROCm release. 
The initial report can be found here (https://github.com/ROCm/aomp/issues/527).

I'm able to confirm that this bug is now fixed. 
Now, the remaining fixes from AOMP 18.0-1 need to be ported to have an almost complete interface. 

@jordialcaraz If you want to test OMPT with AMD GPUs, I would recommend using at least AOMP 18.0-0 or even an in development build of AOMP 18.0-1. With AOMP 18.0-0, you should be able to use one accelerator and multiple OpenMP threads per accelerator correctly, AOMP 18.0-1 includes additional fixes for `buffer_request` and `buffer_complete` which then correctly report the device number (see https://github.com/ROCm/aomp/issues/531 and https://github.com/ROCm/ROCm/issues/2058). 

---

### 评论 #4 — nartmada (2024-02-01T03:09:20Z)

Hi @jordialcaraz, please close the ticket when the issue has been fixed.  Thanks.

---
