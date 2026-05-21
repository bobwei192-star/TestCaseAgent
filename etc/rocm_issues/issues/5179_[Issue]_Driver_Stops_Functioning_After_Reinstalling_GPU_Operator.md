# [Issue]: Driver Stops Functioning After Reinstalling GPU Operator

> **Issue #5179**
> **状态**: closed
> **创建时间**: 2025-06-06T22:48:48Z
> **更新时间**: 2025-10-03T17:09:29Z
> **关闭时间**: 2025-10-03T17:09:29Z
> **作者**: CcccYxx
> **标签**: Question
> **URL**: https://github.com/ROCm/ROCm/issues/5179

## 标签

- **Question** (颜色: #cc317c)

## 负责人

- yansun1996

## 描述

### Problem Description

After installing AMD GPU operator v1.3.0 via helm -> uninstall it via helm-> reinstall it via helm again. The driver stops functioning. The metrics exporter pod reported coredump 
```shell
$:~# kubectl logs -n amd-operator  amd-gpu-metrics-exporter-bv869
exporter 2025/06/03 23:55:53 rocpclient.go:66: exec error :signal: aborted (core dumped)
exporter 2025/06/03 23:56:08 rocpclient.go:66: exec error :signal: aborted (core dumped)
exporter 2025/06/03 23:56:23 rocpclient.go:66: exec error :signal: aborted (core dumped)
```
Running `rocm-smi` command within the metrics exporter container hangs without any outputs:
```shell
$:~# kubectl exec -it -n amd-operator amd-gpu-metrics-exporter-bv869 -- /bin/bash
Defaulted container "metrics-exporter-container" out of: metrics-exporter-container, driver-init (init)
[root@amd-gpu-metrics-exporter-bv869 ~]# rocm-smi
(hangs)
```
This issue can only be fixed after a node reboot. 

### Operating System

Ubuntu 22.04.4 LTS (Jammy Jellyfish)

### CPU

Intel Xeon Processor (Icelake)

### GPU

AMD Instinct MI210 

### ROCm Version

ROCm 6.4

### ROCm Component

_No response_

### Steps to Reproduce

1. Prepare an env without pre-installed amd drivers.
2. Install amd gpu operator v1.3.0 via helm: with deviceconfig settings: `spec.driver.enable=true`, `spec.driver.version="6.4"` with proper private image registry. Use default values for everything else.
3. Uninstall amd gpu operator via helm
4. Repeat step 2 without rebooting the node

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — CcccYxx (2025-06-06T22:53:18Z)

adding dmesg output:
```shell
[10309.382713] amdgpu 0000:05:00.0: amdgpu: amdgpu: finishing device.
[10310.522796] [drm] amdgpu: ttm finalized
[10802.505089] [drm] amdgpu kernel modesetting enabled.
[10802.505094] [drm] amdgpu version: 6.12.12
[10802.505518] amdgpu: Virtual CRAT table created for CPU
[10802.505542] amdgpu: Topology: Add CPU node
[10802.516459] amdgpu 0000:05:00.0: amdgpu: detected ip block number 0 <soc15_common>
[10802.516466] amdgpu 0000:05:00.0: amdgpu: detected ip block number 1 <gmc_v9_0>
[10802.516470] amdgpu 0000:05:00.0: amdgpu: detected ip block number 2 <vega20_ih>
[10802.516473] amdgpu 0000:05:00.0: amdgpu: detected ip block number 3 <psp>
[10802.516476] amdgpu 0000:05:00.0: amdgpu: detected ip block number 4 <smu>
[10802.516480] amdgpu 0000:05:00.0: amdgpu: detected ip block number 5 <gfx_v9_0>
[10802.516484] amdgpu 0000:05:00.0: amdgpu: detected ip block number 6 <sdma_v4_0>
[10802.516487] amdgpu 0000:05:00.0: amdgpu: detected ip block number 7 <vcn_v2_6>
[10802.516490] amdgpu 0000:05:00.0: amdgpu: detected ip block number 8 <jpeg_v2_6>
[10802.524679] amdgpu 0000:05:00.0: Invalid PCI ROM header signature: expecting 0xaa55, got 0x0030
[10802.530273] amdgpu 0000:05:00.0: amdgpu: Fetched VBIOS from ROM
[10802.530282] amdgpu: ATOM BIOS: 113-D67301-059
[10802.539732] amdgpu 0000:05:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[10802.539804] amdgpu 0000:05:00.0: amdgpu: PCIE atomic ops is not supported
[10802.539816] amdgpu 0000:05:00.0: amdgpu: MODE1 reset
[10802.539821] amdgpu 0000:05:00.0: amdgpu: GPU mode1 reset
[10802.541051] amdgpu 0000:05:00.0: amdgpu: GPU smu mode1 reset
[10802.541056] amdgpu 0000:05:00.0: amdgpu: GPU mode1 reset failed
[10802.542852] amdgpu 0000:05:00.0: amdgpu: asic reset on init failed
[10802.544766] amdgpu 0000:05:00.0: amdgpu: Fatal error during GPU init
[10802.546711] amdgpu 0000:05:00.0: amdgpu: amdgpu: finishing device.
[10802.547347] amdgpu: probe of 0000:05:00.0 failed with error -22
[10802.547365] amdgpu: legacy kernel without apple_gmux_detect()
```

---

### 评论 #2 — yansun1996 (2025-06-09T20:39:30Z)

Hi @CcccYxx thanks for reporting this, this issue was triggered by reloading driver. Based on the steps you performed you are doing driver install + uninstall + re-install. May I know the GPU node is a BM or guest VM ?

---

### 评论 #3 — CcccYxx (2025-06-09T20:45:48Z)

Hi @yansun1996, thank you for the response! The GPU node is a VM, and the k8s server version is: v1.30.13. Kernel: 5.15.0-126-generic.

---

### 评论 #4 — yansun1996 (2025-08-02T00:14:51Z)

Hi @CcccYxx seems like the node requires a reboot during the kernel module reload. Can you use the same VM node, try to manually install + uninstall + install again ? If that hits the same thing you discovered in dmesg, you can start to file a ticket in https://github.com/ROCm/ROCm/issues

---

### 评论 #5 — ppanchad-amd (2025-10-03T17:09:29Z)

Hi @CcccYxx. Closing ticket.  Please feel free to comment if you still have any issues and we'll take a look. Thanks!

---
