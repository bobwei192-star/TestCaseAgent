# [BUG]: ROCm Fails to Recognize Integrated GPU on Ryzen 7 9700X (RDNA 3.5)

> **Issue #5193**
> **状态**: closed
> **创建时间**: 2025-08-13T01:45:28Z
> **更新时间**: 2025-10-09T03:30:29Z
> **关闭时间**: 2025-10-09T03:30:29Z
> **作者**: ghost
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/5193

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Problem Description

The integrated GPU on the mainstream Ryzen 7 9700X desktop CPU is not recognized by the current ROCm 6.x stack. This prevents any ROCm-accelerated applications, such as Ollama, from using the iGPU, forcing a fallback to CPU mode. This issue persists despite the hardware being available for over a year and is similar to other open iGPU support requests like #3398.

**System Information:**
*   **Kernel:** 6.15.9-201.fc42.x86_64

I would like the official ROCm software stack to recognize and fully support the integrated GPU of the Ryzen 7 9700X CPU. This would involve adding its hardware ID to the list of supported devices, allowing applications to use it for AI and HPC workloads without requiring unstable overrides or workarounds.




### Operating System

Fedora Linux 42 (Sway)

### CPU

AMD Ryzen 7 9700X 8-Core Processor

### GPU

Integrated RDNA 3.5 Graphics

### ROCm Version

ROCm 6.1.2 and 6.3

### ROCm Component

_No response_

### Steps to Reproduce

I have performed extensive troubleshooting to isolate the issue to the ROCm userspace stack.
1.  **Host `dmesg` logs confirm that the `amdgpu` and `kfd` kernel drivers are loading successfully.** This proves the kernel and hardware are functioning correctly.
2.  **A Docker-based approach was used to bypass any host OS dependency issues.** The container was given full hardware access (`--device=/dev/kfd`, `--device=/dev/dri`) and correct permissions (`--group-add`).
3.  **The `HSA_OVERRIDE_GFX_VERSION` was applied.** This did not resolve the issue, indicating a deeper incompatibility within the ROCm version used by the application.
4.  **Proof-of-concept tests show that AMD's own `apt` repositories for Ubuntu 22.04 are currently misconfigured**, preventing a clean install of the latest drivers even in an ideal container environment.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

no such file or directory: /opt/rocm/bin/rocminfo

### Additional Information

The lack of iGPU support for new, mainstream desktop CPUs is a significant gap. As AI becomes more prevalent, enabling developers and enthusiasts to use the full capabilities of their hardware is crucial. Adding support for the Ryzen 9000 series iGPUs would align with the growing interest in local AI development.
