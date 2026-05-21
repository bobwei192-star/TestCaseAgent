# Set env var for canonical URL

> **Issue #3464**
> **状态**: closed
> **创建时间**: 2024-07-26T18:05:23Z
> **更新时间**: 2024-07-26T21:37:00Z
> **关闭时间**: 2024-07-26T21:37:00Z
> **作者**: samjwu
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/3464

## 负责人

- samjwu

## 描述

```
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "rocm.docs.amd.com")
html_context = {}
if os.environ.get("READTHEDOCS", "") == "True":
    html_context["READTHEDOCS"] = True
```
