# [Documentation]: Clarify ROCm support status for RDNA 1 GPUs in compatibility documentation

> **Issue #6192**
> **状态**: open
> **创建时间**: 2026-04-29T19:08:10Z
> **更新时间**: 2026-05-12T14:45:07Z
> **作者**: ChihweiLHBird
> **标签**: Documentation, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6192

## 标签

- **Documentation** (颜色: #5319e7)
- **status: triage** (颜色: #585dd7)

## 负责人

- benrichard-amd

## 描述

### Description of errors

Could you please clarify the official ROCm support status for RDNA 1 GPUs in the documentation?

I checked the compatibility matrix here: [docs/compatibility/compatibility-matrix.rst](https://github.com/ROCm/ROCm/blob/4557f6b60c0e448115f363f850de0c445e64f7be/docs/compatibility/compatibility-matrix.rst)

The matrix lists RDNA2, RDNA3, and newer architectures, but RDNA 1 is not shown. At the same time, some RDNA 1 hardware still appears in other documentation such as GPU architecture/specification pages, so it is not obvious whether RDNA 1 is:

1. officially supported,
2. deprecated,
3. unsupported, or
4. partially/community supported only.

It would be very helpful if the ROCm documentation explicitly showed the support status of RDNA 1 / gfx101x devices, even if the status is “not supported”.

Suggested improvement:

- add RDNA 1 (or the relevant gfx101x targets) to the compatibility/support docs with an explicit status,
- or add a short note stating that RDNA 1 is not supported by current ROCm releases, if that is the case.

This would make the support policy much clearer for users trying to determine whether older Radeon / Radeon Pro cards are still supported.

### Attach any links, screenshots, or additional evidence you think will be helpful.

- https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#past-rocm-compatibility-matrix
- https://github.com/ROCm/ROCm/blob/4557f6b60c0e448115f363f850de0c445e64f7be/docs/compatibility/compatibility-matrix.rst
