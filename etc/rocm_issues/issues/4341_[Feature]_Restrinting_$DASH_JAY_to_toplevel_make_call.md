# [Feature]: Restrinting $DASH_JAY to toplevel make call

> **Issue #4341**
> **状态**: open
> **创建时间**: 2025-02-04T23:01:11Z
> **更新时间**: 2025-02-05T15:19:25Z
> **作者**: jdumke
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/4341

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

In nearly all subprojects eveery submake gets $DASH_JAY as flag, which resets make's jobserver and makes it pissed off, you can see it in the logs. 
Could you restrict this CLI-Option  to the most top-level call builds run more smooth.
Also could you implement, thats if DASH_JAY is set by user in  shell, it won't be overwritten by your scripts.
In my case, I want to restrict the build to eight threads, to have some cpu-threads are availiable to the OS and the desktop, but it's regularly overwritten by the build-scripts with "-j 12".

### Operating System

Any

### GPU

_No response_

### ROCm Component

all
