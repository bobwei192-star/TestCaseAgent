# [Issue]: EL9 pakages for ROCm 7.1 are actually for EL8

> **Issue #5617**
> **状态**: closed
> **创建时间**: 2025-11-02T20:40:46Z
> **更新时间**: 2025-11-06T13:30:51Z
> **关闭时间**: 2025-11-06T13:30:51Z
> **作者**: fwyzard
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5617

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- adityas-amd

## 描述

### Problem Description

The ROCm 7.1 packages for EL9 at https://repo.radeon.com/rocm/rhel9/7.1/main/ are actually for EL8 as the `.el8.` part of the name suggests:

<img width="652" height="232" alt="Image" src="https://github.com/user-attachments/assets/5c3ab7d2-6510-41d4-a445-b164f8eec916" />

Downloading and unpacking a couple of RPMs showed that indeed the contents of the EL8 and EL9 packages are identical. 

### Operating System

RedHat Enterprise Linux 9

### CPU

n/a

### GPU

n/a

### ROCm Version

ROCm 7.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — adityas-amd (2025-11-06T12:59:10Z)

@fwyzard this is intentional. Our build pipeline targets Manylinux 2.28 - which in turn is Almalinux-8, so the produced RPMs are packaged as el8 artifacts.

---

### 评论 #2 — fwyzard (2025-11-06T13:15:03Z)

Ah, I see.

Is intended then that the packages for RHEL 10 are real el10 packages ?

---

### 评论 #3 — adityas-amd (2025-11-06T13:25:13Z)

yes, the packages rhel10/7.1 are EL10-built RPMs. Previously the rhel9 path contained EL8-built artifacts because our Manylinux CI used AlmaLinux‑8 (Manylinux 2.28). We published EL10 artifacts to the rhel10 tree for users needing RHEL/AlmaLinux 10 compatibility.

---

### 评论 #4 — fwyzard (2025-11-06T13:30:39Z)

OK, thanks.

---
