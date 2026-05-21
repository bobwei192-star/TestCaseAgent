# [Issue]: `amd-smi partition` returns `N/A` for almost all fields

> **Issue #4477**
> **状态**: open
> **创建时间**: 2025-03-10T19:49:42Z
> **更新时间**: 2025-06-25T15:38:54Z
> **作者**: garrettbyrd
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4477

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

What information is supposed to be returned from `amd-smi partition`?

When I run `amd-smi partition` I get the following:

```
~$ amd-smi partition
CURRENT_PARTITION:
GPU_ID       MEMORY  ACCELERATOR_TYPE  ACCELERATOR_PROFILE_INDEX  PARTITION_ID  
0            NPS1    N/A               N/A                        N/A
1            NPS1    N/A               N/A                        N/A
2            NPS1    N/A               N/A                        N/A
3            NPS1    N/A               N/A                        N/A
GPU: 0
    MEMORY_PARTITION:
        CAPS: N/A
        CURRENT: NPS1

GPU: 1
    MEMORY_PARTITION:
        CAPS: N/A
        CURRENT: NPS1

GPU: 2
    MEMORY_PARTITION:
        CAPS: N/A
        CURRENT: NPS1

GPU: 3
    MEMORY_PARTITION:
        CAPS: N/A
        CURRENT: NPS1


ACCELERATOR_PARTITION_PROFILES:
GPU_ID       PROFILE_INDEX  MEMORY_PARTITION_CAPS  ACCELERATOR_TYPE  PARTITION_ID  NUM_PARTITIONS  NUM_RESOURCES  RESOURCE_INDEX  RESOURCE_TYPE  RESOURCE_INSTANCES  RESOURCES_SHARED  
0            N/A            N/A                    N/A               N/A           0               N/A            N/A             N/A            N/A                 N/A
1            N/A            N/A                    N/A               N/A           0               N/A            N/A             N/A            N/A                 N/A
2            N/A            N/A                    N/A               N/A           0               N/A            N/A             N/A            N/A                 N/A
3            N/A            N/A                    N/A               N/A           0               N/A            N/A             N/A            N/A                 N/A
```

which basically only tells me that all four devices are using one NUMA node per socket.

I get similar outputs for MI210 and W7800. Is this intended behavior?



### Operating System

Rocky Linux 9.5 (Blue Onyx) x86_64

### CPU

4 x AMD Instinct MI300A Accelerator (192) @ 3.70 GHz

### GPU

4 x AMD Instinct MI300A Accelerator, 1 x AMD Instinct MI210 Accelerator, 1 x AMD Radeon PRO W7800

### ROCm Version

ROCm 6.3.3

### ROCm Component

amdsmi

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — harkgill-amd (2025-03-12T18:48:39Z)

Hi @garrettbyrd, will confirm HW support for the `partition` command specifically and provide an update. In the meantime, could you please provide the output of 

1. amd-smi partition --loglevel DEBUG
2. amd-smi static --partition
3. amd-smi version
4. amd-smi firmware
5. sudo dkms status

---

### 评论 #2 — garrettbyrd (2025-03-12T20:01:52Z)

```
$ amd-smi partition --loglevel DEBUG
DEBUG: Failed to get accelerator partition profile for GPU 0 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
DEBUG: Failed to get accelerator partition profile for GPU 1 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
DEBUG: Failed to get accelerator partition profile for GPU 2 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
DEBUG: Failed to get accelerator partition profile for GPU 3 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
CURRENT_PARTITION:
GPU_ID       MEMORY  ACCELERATOR_TYPE  ACCELERATOR_PROFILE_INDEX  PARTITION_ID  
0            NPS1    N/A               N/A                        N/A
1            NPS1    N/A               N/A                        N/A
2            NPS1    N/A               N/A                        N/A
3            NPS1    N/A               N/A                        N/A
DEBUG: Failed to get accelerator partition profile for GPU 0 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
DEBUG: Failed to get accelerator partition profile for GPU 1 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
DEBUG: Failed to get accelerator partition profile for GPU 2 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
DEBUG: Failed to get accelerator partition profile for GPU 3 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
GPU: 0
    MEMORY_PARTITION:
        CAPS: N/A
        CURRENT: NPS1

GPU: 1
    MEMORY_PARTITION:
        CAPS: N/A
        CURRENT: NPS1

GPU: 2
    MEMORY_PARTITION:
        CAPS: N/A
        CURRENT: NPS1

GPU: 3
    MEMORY_PARTITION:
        CAPS: N/A
        CURRENT: NPS1


DEBUG: Failed to get accelerator partition profile for GPU 0 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
DEBUG: Failed to get accelerator partition profile for GPU 1 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
DEBUG: Failed to get accelerator partition profile for GPU 2 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
DEBUG: Failed to get accelerator partition profile for GPU 3 | AMDSMI_STATUS_NOT_SUPPORTED - Feature not supported
ACCELERATOR_PARTITION_PROFILES:
GPU_ID       PROFILE_INDEX  MEMORY_PARTITION_CAPS  ACCELERATOR_TYPE  PARTITION_ID  NUM_PARTITIONS  NUM_RESOURCES  RESOURCE_INDEX  RESOURCE_TYPE  RESOURCE_INSTANCES  RESOURCES_SHARED  
0            N/A            N/A                    N/A               N/A           0               N/A            N/A             N/A            N/A                 N/A
1            N/A            N/A                    N/A               N/A           0               N/A            N/A             N/A            N/A                 N/A
2            N/A            N/A                    N/A               N/A           0               N/A            N/A             N/A            N/A                 N/A
3            N/A            N/A                    N/A               N/A           0               N/A            N/A             N/A            N/A                 N/A
```

```
$ amd-smi static --partition
GPU: 0
    PARTITION:
        COMPUTE_PARTITION: SPX
        MEMORY_PARTITION: NPS1
        PARTITION_ID: 0

GPU: 1
    PARTITION:
        COMPUTE_PARTITION: SPX
        MEMORY_PARTITION: NPS1
        PARTITION_ID: 0

GPU: 2
    PARTITION:
        COMPUTE_PARTITION: SPX
        MEMORY_PARTITION: NPS1
        PARTITION_ID: 0

GPU: 3
    PARTITION:
        COMPUTE_PARTITION: SPX
        MEMORY_PARTITION: NPS1
        PARTITION_ID: 0
```

```
$ amd-smi version
AMDSMI Tool: 24.7.1+8dc45db | AMDSMI Library version: 25.1.0.0 | ROCm version: 6.3.3
```

```
$ amd-smi firmware
GPU: 0
    FW_LIST:
        FW 0:
            FW_ID: CP_MEC1
            FW_VERSION: 166
        FW 1:
            FW_ID: CP_MEC2
            FW_VERSION: 166
        FW 2:
            FW_ID: RLC
            FW_VERSION: 65
        FW 3:
            FW_ID: SDMA0
            FW_VERSION: 22
        FW 4:
            FW_ID: SDMA1
            FW_VERSION: 22
        FW 5:
            FW_ID: VCN
            FW_VERSION: 06.11.30.0C
        FW 6:
            FW_ID: PSP_SOSDRV
            FW_VERSION: 00.36.01.50
        FW 7:
            FW_ID: TA_RAS
            FW_VERSION: 1B.36.02.0F
        FW 8:
            FW_ID: TA_XGMI
            FW_VERSION: 20.00.01.13
        FW 9:
            FW_ID: PM
            FW_VERSION: 04.85.103.184

GPU: 1
    FW_LIST:
        FW 0:
            FW_ID: CP_MEC1
            FW_VERSION: 166
        FW 1:
            FW_ID: CP_MEC2
            FW_VERSION: 166
        FW 2:
            FW_ID: RLC
            FW_VERSION: 65
        FW 3:
            FW_ID: SDMA0
            FW_VERSION: 22
        FW 4:
            FW_ID: SDMA1
            FW_VERSION: 22
        FW 5:
            FW_ID: VCN
            FW_VERSION: 06.11.30.0C
        FW 6:
            FW_ID: PSP_SOSDRV
            FW_VERSION: 00.36.01.50
        FW 7:
            FW_ID: TA_RAS
            FW_VERSION: 1B.36.02.0F
        FW 8:
            FW_ID: TA_XGMI
            FW_VERSION: 20.00.01.13
        FW 9:
            FW_ID: PM
            FW_VERSION: 04.85.103.184

GPU: 2
    FW_LIST:
        FW 0:
            FW_ID: CP_MEC1
            FW_VERSION: 166
        FW 1:
            FW_ID: CP_MEC2
            FW_VERSION: 166
        FW 2:
            FW_ID: RLC
            FW_VERSION: 65
        FW 3:
            FW_ID: SDMA0
            FW_VERSION: 22
        FW 4:
            FW_ID: SDMA1
            FW_VERSION: 22
        FW 5:
            FW_ID: VCN
            FW_VERSION: 06.11.30.0C
        FW 6:
            FW_ID: PSP_SOSDRV
            FW_VERSION: 00.36.01.50
        FW 7:
            FW_ID: TA_RAS
            FW_VERSION: 1B.36.02.0F
        FW 8:
            FW_ID: TA_XGMI
            FW_VERSION: 20.00.01.13
        FW 9:
            FW_ID: PM
            FW_VERSION: 04.85.103.184

GPU: 3
    FW_LIST:
        FW 0:
            FW_ID: CP_MEC1
            FW_VERSION: 166
        FW 1:
            FW_ID: CP_MEC2
            FW_VERSION: 166
        FW 2:
            FW_ID: RLC
            FW_VERSION: 65
        FW 3:
            FW_ID: SDMA0
            FW_VERSION: 22
        FW 4:
            FW_ID: SDMA1
            FW_VERSION: 22
        FW 5:
            FW_ID: VCN
            FW_VERSION: 06.11.30.0C
        FW 6:
            FW_ID: PSP_SOSDRV
            FW_VERSION: 00.36.01.50
        FW 7:
            FW_ID: TA_RAS
            FW_VERSION: 1B.36.02.0F
        FW 8:
            FW_ID: TA_XGMI
            FW_VERSION: 20.00.01.13
        FW 9:
            FW_ID: PM
            FW_VERSION: 04.85.103.184
```

```
$ sudo dkms status
Deprecated feature: REMAKE_INITRD (/var/lib/dkms/lustre-client/2.15.6/source/dkms.conf)
amdgpu/6.10.5-2095006.el9, 5.14.0-503.19.1.el9_5.x86_64, x86_64: installed (original_module exists)
lustre-client/2.15.6, 5.14.0-503.19.1.el9_5.x86_64, x86_64: installed
```

---

### 评论 #3 — harkgill-amd (2025-04-01T18:16:18Z)

Hi @garrettbyrd, support for the `amd-smi partition` command is currently only available on MI300X+ROCm 6.3.3.

Support will be extended to MI300A in an upcoming release which will replace the `N/A` values with the correct readings.

---

### 评论 #4 — harkgill-amd (2025-04-17T14:12:25Z)

Hi @garrettbyrd, could you please give this a try with ROCm 6.4 and share the output/BKC version you're testing with.

---

### 评论 #5 — garrettbyrd (2025-04-23T20:28:50Z)

Here is the output using 6.4.0:

```
$ sudo amd-smi partition
CURRENT_PARTITION:
GPU_ID  MEMORY  ACCELERATOR_TYPE  ACCELERATOR_PROFILE_INDEX  PARTITION_ID  
0       NPS1    N/A               N/A                        0
1       NPS1    N/A               N/A                        0
2       NPS1    N/A               N/A                        0
3       NPS1    N/A               N/A                        0

MEMORY_PARTITION:
GPU_ID  MEMORY_PARTITION_CAPS  CURRENT_MEMORY_PARTITION  
0                              NPS1
1                              NPS1
2                              NPS1
3                              NPS1

ACCELERATOR_PARTITION_PROFILES:
GPU_ID  PROFILE_INDEX  MEMORY_PARTITION_CAPS  ACCELERATOR_TYPE  PARTITION_ID     NUM_PARTITIONS  NUM_RESOURCES  RESOURCE_INDEX  RESOURCE_TYPE  RESOURCE_INSTANCES  RESOURCES_SHARED  
0       0                                     SPX               N/A              1               0              N/A             N/A            N/A                 N/A
        1                                     TPX               N/A              3               0              N/A             N/A            N/A                 N/A
        2                                     CPX               N/A              6               0              N/A             N/A            N/A                 N/A
1       0                                     SPX               N/A              1               0              N/A             N/A            N/A                 N/A
        1                                     TPX               N/A              3               0              N/A             N/A            N/A                 N/A
        2                                     CPX               N/A              6               0              N/A             N/A            N/A                 N/A
2       0                                     SPX               N/A              1               0              N/A             N/A            N/A                 N/A
        1                                     TPX               N/A              3               0              N/A             N/A            N/A                 N/A
        2                                     CPX               N/A              6               0              N/A             N/A            N/A                 N/A
3       0                                     SPX               N/A              1               0              N/A             N/A            N/A                 N/A
        1                                     TPX               N/A              3               0              N/A             N/A            N/A                 N/A
        2                                     CPX               N/A              6               0              N/A             N/A            N/A                 N/A

ACCELERATOR_PARTITION_RESOURCES:
RESOURCE_INDEX  RESOURCE_TYPE  RESOURCE_INSTANCES  RESOURCES_SHARED  
N/A             N/A            N/A                 N/A
N/A             N/A            N/A                 N/A
N/A             N/A            N/A                 N/A
N/A             N/A            N/A                 N/A


Legend:
  * = Current mode
```

also relevant

```
$ amd-smi version -g -c
AMDSMI Tool: 25.3.0+ede62f2 | AMDSMI Library version: 25.3.0 | ROCm version: 6.4.0 | amdgpu version: 6.10.5 | amd_hsmp version: 2.2
```

Do you have a recommended method for finding the BKC version?

---

### 评论 #6 — garrettbyrd (2025-04-25T16:09:08Z)

Tagging this in case it is related https://github.com/ROCm/amdsmi/issues/86

---

### 评论 #7 — harkgill-amd (2025-06-25T15:38:54Z)

Quick update on this - the changes in https://github.com/ROCm/amdsmi/commit/391451752bcc6b9e8d6cd48a2f64d6aacaaf246c address the `N/A` values in the output of the partition command. You'll have to wait for the upcoming release for the changes to take effect as there is a dependency on the prepackaged kernel driver. Here's a peak at what the output will look like once the release is out
```
sudo amd-smi partition
CURRENT_PARTITION:
GPU_ID  MEMORY  ACCELERATOR_TYPE  ACCELERATOR_PROFILE_INDEX  PARTITION_ID
0       NPS1    SPX               0                          0
1       NPS1    SPX               0                          0
2       NPS1    SPX               0                          0
3       NPS1    SPX               0                          0

MEMORY_PARTITION:
GPU_ID  MEMORY_PARTITION_CAPS  CURRENT_MEMORY_PARTITION
0       N/A                    NPS1
1       N/A                    NPS1
2       N/A                    NPS1
3       N/A                    NPS1

ACCELERATOR_PARTITION_PROFILES:
GPU_ID  PROFILE_INDEX  MEMORY_PARTITION_CAPS  ACCELERATOR_TYPE  PARTITION_ID     NUM_PARTITIONS  NUM_RESOURCES  RESOURCE_INDEX  RESOURCE_TYPE  RESOURCE_INSTANCES  RESOURCES_SHARED
0       0              N/A                    SPX*              0                1               4              0               XCC            6                   1
                                                                                                                1               DECODER        3                   1
                                                                                                                2               DMA            12                  1
                                                                                                                3               JPEG           24                  1
        1              N/A                    TPX               N/A              3               4  
...
ACCELERATOR_PARTITION_RESOURCES:
RESOURCE_INDEX  RESOURCE_TYPE  RESOURCE_INSTANCES  RESOURCES_SHARED
0               XCC            6                   1
1               DECODER        3                   1
2               DMA            12                  1
```
The `N/A` values under `MEMORY_PARTITION_CAPS` are expected due to the underlying mechanism (partition switching) not being available on MI300A.

---
