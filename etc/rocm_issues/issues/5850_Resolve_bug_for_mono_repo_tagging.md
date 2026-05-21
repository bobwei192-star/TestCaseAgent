# Resolve bug for mono repo tagging

> **Issue #5850**
> **状态**: open
> **创建时间**: 2026-01-12T12:56:13Z
> **更新时间**: 2026-01-12T12:56:23Z
> **作者**: srayasam-amd
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5850

## 负责人

- srayasam-amd

## 描述

**Current setup:** If there are multiple PR IDs in the commit message of the repo which belongs to super repos, ccurrently, we have the code to take the first PR ID.
**Resolution:**
We need to take the last PR ID of the commit message which means it is the latest PR so that we can tag with that particular commit ID in regard to PR ID.
