# AMD SMI controls to mitigate LeftoverLocals and Whispering Pixel vulnerabilities

> **Issue #3500**
> **状态**: closed
> **创建时间**: 2024-08-02T19:10:21Z
> **更新时间**: 2024-11-13T20:33:04Z
> **关闭时间**: 2024-11-06T22:46:50Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3500

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.2.0** (颜色: #31778C)

## 描述

The mitigation for LeftoverLocals (CVE-2023-4969) and Whispering Pixel (CVE-2024-21969) issues is provided in the ROCm 6.2.4 release. The mitigation is turned off by default and can be enabled or disabled via AMD SMI calls.

The following AMD SMI calls can be used depending on the needs of the system administrator.

- **Enable or disable process isolation**.
  This flag is controlled via AMD SMI CLI and will either enable the code path which resets the GPU local memory (LDS) and registers (GPRs) between process switching, or disable it, in which case the LDS and GPRs will not be touched between process switching. 

  - **AMD SMI CLI for setting and reading the process isolation status**
    
    - `amd-smi set --process-isolation STATUS --gpu GPU`
      Where the value of STATUS enables or disables the GPU process isolation: 0 for disable and 1 for enable.
    - `amd-smi static --process-isolation`

  - **AMD SMI API calls for setting and reading the process isolation status**
    - `amdsmi_set_gpu_process_isolation()`
    - `amdsmi_get_gpu_process_isolation()`

- You can also manually clean the LDS and GPRs using the AMD SMI CLI. This can be used by system administrators to either execute on demand or via scheduled jobs.
  
  - **AMD SMI CLI for cleaning the LDS and GPRs**
    `amd-smi reset --clean-local-data --gpu GPU`

  - **AMD SMI API call for cleaning the LDS and GPRs**
    `amdsmi_clean_gpu_local_data()`

For more information, refer to the [AMD SMI CLI tool documentation](https://rocm.docs.amd.com/projects/amdsmi/en/latest/how-to/using-AMD-SMI-CLI-tool.html).
