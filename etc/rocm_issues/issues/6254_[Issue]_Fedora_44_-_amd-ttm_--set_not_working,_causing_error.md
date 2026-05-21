# [Issue]: Fedora 44 - amd-ttm --set not working, causing error

> **Issue #6254**
> **状态**: closed
> **创建时间**: 2026-05-13T13:08:54Z
> **更新时间**: 2026-05-13T16:14:37Z
> **关闭时间**: 2026-05-13T15:10:09Z
> **作者**: PCAssistSoftware
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6254

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Fedora 44 - amd-ttm --set 100 not working, causing error as below?


darren@fedora:~$ amd-ttm --set 100
🐧 Successfully set TTM pages limit to 26214400 pages (100.00 GB)
🐧 Configuration written to /etc/modprobe.d/ttm.conf
○ NOTE: You need to reboot for changes to take effect.
Would you like to reboot the system now? (y/n): y
Traceback (most recent call last):
  File "/home/darren/.local/bin/amd-ttm", line 6, in <module>
    sys.exit(amd_ttm())
             ~~~~~~~^^
  File "/home/darren/.local/share/pipx/venvs/amd-debug-tools/lib64/python3.14/site-packages/amd_debug/__init__.py", line 29, in amd_ttm
    return ttm.main()
           ~~~~~~~~^^
  File "/home/darren/.local/share/pipx/venvs/amd-debug-tools/lib64/python3.14/site-packages/amd_debug/ttm.py", line 150, in main
    ret = tool.set(args.set)
  File "/home/darren/.local/share/pipx/venvs/amd-debug-tools/lib64/python3.14/site-packages/amd_debug/ttm.py", line 101, in set
    return maybe_reboot()
  File "/home/darren/.local/share/pipx/venvs/amd-debug-tools/lib64/python3.14/site-packages/amd_debug/ttm.py", line 28, in maybe_reboot
    return reboot()
  File "/home/darren/.local/share/pipx/venvs/amd-debug-tools/lib64/python3.14/site-packages/amd_debug/common.py", line 276, in reboot
    loop = asyncio.get_event_loop()
  File "/usr/lib64/python3.14/asyncio/events.py", line 715, in get_event_loop
    raise RuntimeError('There is no current event loop in thread %r.'
                       % threading.current_thread().name)
RuntimeError: There is no current event loop in thread 'MainThread'.


### Operating System

Fedora 44

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

gfx1151 AMD Radeon 8060S Graphics  

### ROCm Version

7.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2026-05-13T16:12:04Z)

Thanks for the catch @PCAssistSoftware. This was due to the deprecation of an `asyncio.get_event_loop()` with Python 3.14 which Fedora 44 comes standard with. The above PR replaces it with supported operations. You can pickup the changes by following the steps [here](https://github.com/superm1/amd-debug-tools#from-source).

---

### 评论 #2 — PCAssistSoftware (2026-05-13T16:14:37Z)

@harkgill-amd - no problem at all, and thank you

---
