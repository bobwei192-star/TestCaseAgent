# Not clear where to acquire VBIOS upgrade for MI100 for ROCm 7.1

> **Issue #5775**
> **状态**: closed
> **创建时间**: 2025-12-15T15:41:27Z
> **更新时间**: 2026-01-29T19:04:14Z
> **关闭时间**: 2026-01-29T19:04:14Z
> **作者**: LunNova
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5775

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- lucbruni-amd

## 描述

The release notes for ROCm 7.1.1 list supported VBIOS versions for MI100 cards: https://rocm.docs.amd.com/en/docs-7.1.1/about/release-notes.html

```
MI100 	VBIOS D3430401-037 	Not Applicable
```

I have some MI100s that aren't on that rev. Where are updates hosted?

---

## 评论 (7 条)

### 评论 #1 — lucbruni-amd (2025-12-16T18:04:59Z)

Hi @LunNova, thanks for opening this issue. I agree the documentation is a bit unclear in that regard. What is the source of your MI100s, are they from a server vendor? Have you already checked this page for more details on [firmware updates](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/common/firmware-updates.html#firmware-update-instructions), specifically [OEM-provided firmware](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/common/firmware-updates.html#oem-provided-firmware)?

---

### 评论 #2 — LunNova (2025-12-16T18:11:25Z)

Mine are from HPE. They're running either D3431500-101 or D3431500-100 currently. D3431500-101 seems to be the newest available version from the HPE support site. Is that outdated? It definitely doesn't match the version in the release notes. https://support.hpe.com/connect/s/softwaredetails?language=en_US&collectionId=MTX-d2334c58a87e4e62&tab=releaseNotes

---

### 评论 #3 — lucbruni-amd (2025-12-22T05:36:37Z)

`D3431500-100` from HPE and `D3430401-037` listed in the docs are effectively equivalent. The latter is a version number tied to internal releases. The `100` and `101` numbering sequences are used by HPE specifically but can vary by vendor. The revisions on your MI100s are totally fine, and we are working to have this communicated more effectively for the release notes.

---

### 评论 #4 — jacazek (2025-12-22T08:20:02Z)

Would you be able to confirm if the following VBIOS versions are compatible?
1. `D3431401-100`
2. `D3432400-100`

Unfortunately I know not the vendor of the devices having those particular VBIOS versions.

---

### 评论 #5 — lucbruni-amd (2026-01-03T14:59:04Z)

> Would you be able to confirm if the following VBIOS versions are compatible?
> 
> 1. `D3431401-100`
> 2. `D3432400-100`
> 
> Unfortunately I know not the vendor of the devices having those particular VBIOS versions.

Yes, `D3431401-100` and `D3432400-100` are suitable. They are the correct and required VBIOS versions for their respective MI100 PCB variants (`D34314` and `D34324` respectively). However they are not interchangeable, in that the `D34324` SKU requires the use of the updated IFWI to support hardware changes from the `D34314` SKU. For now, keep these VBIOS versions specifically while we sort out the documentation to clear this all up. Thanks!

---

### 评论 #6 — jacazek (2026-01-05T01:40:45Z)

Awesome! Thanks so much!

---

### 评论 #7 — lucbruni-amd (2026-01-29T19:04:14Z)

Closing this issue as the [release notes](https://rocm.docs.amd.com/en/latest/about/release-notes.html#user-space-driver-and-firmware-dependent-changes) are now providing additional context going forward. Please feel free to reopen this issue or a new one if there are further concerns. Thanks!

---
