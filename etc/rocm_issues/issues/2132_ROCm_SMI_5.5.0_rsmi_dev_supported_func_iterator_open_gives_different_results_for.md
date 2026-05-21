# ROCm SMI 5.5.0 rsmi_dev_supported_func_iterator_open gives different results for the same call

> **Issue #2132**
> **状态**: closed
> **创建时间**: 2023-05-12T05:23:25Z
> **更新时间**: 2024-08-15T14:52:56Z
> **关闭时间**: 2024-08-15T14:52:55Z
> **作者**: bertwesarg
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2132

## 描述

When calling `rsmi_dev_supported_func_iterator_open` the first time on an "AMD Ryzen 7 PRO 4750U with Radeon Graphics" laptop it returns `RSMI_STATUS_INTERNAL_EXCEPTION`, but calling it the second time with the same arguments returns `RSMI_STATUS_SUCCESS`. See example:

```c
#include <rocm_smi/rocm_smi.h>

int
main(int ac, char *av[])
{
    rsmi_status_t status = rsmi_init(0);
    if (status != RSMI_STATUS_SUCCESS) abort();

    uint32_t device_count;
    status = rsmi_num_monitor_devices(&device_count);
    if (status != RSMI_STATUS_SUCCESS) abort();

    uint32_t dev;
    for (dev = 0; dev < device_count; ++dev) {
        rsmi_func_id_iter_handle_t iter;
        status = rsmi_dev_supported_func_iterator_open(dev, &iter);
        fprintf(stderr, "first call dev#%d:  %d\n", dev, status);
        status = rsmi_dev_supported_func_iterator_open(dev, &iter);
        fprintf(stderr, "second call dev#%d: %d\n", dev, status);
        if (status == RSMI_STATUS_SUCCESS) {
            status = rsmi_dev_supported_func_iterator_close(&iter);
            if (status != RSMI_STATUS_SUCCESS) abort();
        }
    }

    rsmi_shut_down();

    return 0;
}
```

Output:

```
first call dev#0:  6
second call dev#0: 0
```

This behavior brakes the ROCm PAPI component, as it does two passes over all devices. First just counts the available events and the second pass queries all features of the events. With this behavior the first pass delivers a lower number of events than the second discovers and breaks it. See here: https://bitbucket.org/icl/papi/issues/134

I'm aware that this is not a supported ROCm platform, but the behavior should nevertheless be consistent.

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2024-07-10T18:46:02Z)

Hi @bertwesarg, I was not able to reproduce your issue on a 7900XTX with ROCm 6.1.2/rocm-smi-lib 7.2.0. 

Are you still experiencing this issue on the latest ROCm release? 

---

### 评论 #2 — harkgill-amd (2024-08-15T14:52:55Z)

Closing this ticket as the issue is not reproducible. @bertwesarg, if you encounter this discrepancy on a supported configuration with the latest ROCm release, please open a new issue. Thanks!

---
