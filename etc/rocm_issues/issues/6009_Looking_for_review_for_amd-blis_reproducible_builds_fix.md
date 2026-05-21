# Looking for review for amd-blis reproducible builds fix

> **Issue #6009**
> **状态**: closed
> **创建时间**: 2026-03-02T05:04:12Z
> **更新时间**: 2026-03-12T14:50:57Z
> **关闭时间**: 2026-03-12T14:50:57Z
> **作者**: LunNova
> **标签**: status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/6009

## 标签

- **status: fix submitted** (颜色: #75d97e)

## 负责人

- darren-amd

## 描述

Hi,

Can I please get some help getting an amd-blis fix for compliance with the [reproducible builds spec](https://reproducible-builds.org/docs/source-date-epoch/) reviewed & merged?

- https://github.com/amd/blis/pull/44

The PR's been sitting since October. For now, we're [vendoring a patch](https://github.com/NixOS/nixpkgs/blob/master/pkgs/by-name/am/amd-blis/build-date.patch) to work around this to ensure the build is reproducible in NixOS.

Please let me know if this isn't the right place for this. amd-blis isn't under the ROCm org, but is a dependency of ROCm BLAS packages.

---

## 评论 (2 条)

### 评论 #1 — darren-amd (2026-03-02T15:53:55Z)

Hi @LunNova,

Thanks for the PR! I'm not familiar with this component but I'll find the team working on it and get it reviewed/moved to the appropriate repo.

---

### 评论 #2 — darren-amd (2026-03-12T14:50:57Z)

Thanks again for the contribution @LunNova, going to close this ticket off as we have reviewed/merged the PR internally. It will show up on the public develop branch shortly.

---
