# [Feature]: Python 3.11, 3.14 Torch wheel availability; official Windows Triton/TF Support

> **Issue #5920**
> **状态**: closed
> **创建时间**: 2026-01-31T04:17:05Z
> **更新时间**: 2026-04-30T19:06:16Z
> **关闭时间**: 2026-04-30T19:06:16Z
> **作者**: xalteropsx
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5920

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- lucbruni-amd

## 描述

### Suggestion Description

 Python 3.12 no one use this version except new python user mostly we use python 3.11 please consider adding torch in this version 

regard to rocm-rel-7.2/torch-2.9.1%2Brocmsdk20260116-cp312-cp312-win_amd64.whl 
is cp 311 is available ? if so please provide an link

### Operating System

window 

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (8 条)

### 评论 #1 — lucbruni-amd (2026-02-04T19:09:17Z)

Hi @xalteropsx!

Thanks for opening this issue. I recommend you to check out the wheels over at [TheRock](https://github.com/ROCm/TheRock). There is a guide for installing release wheels for both Linux and Windows [here](https://github.com/ROCm/TheRock/blob/main/RELEASES.md). The nightly wheels for Torch should support Python 3.11. You can check out a library of pre-release wheels [here](https://rocm.prereleases.amd.com/whl/).

Let me know if you have any additional questions.

---

### 评论 #2 — xalteropsx (2026-02-05T04:28:17Z)

thanks alot ,
kinda triton in window already working with zluda via isqhytiger github

if possible when gfx110X will support official triton in window this much little bit of extra asking but i hope you also consider in future tensorflow support as well just 2 things all we needed for now sorry for asking this much but i hope you can bring someone need to bring attention on missing places xD

---

### 评论 #3 — akuckartz (2026-02-05T09:09:10Z)

Please support the current version. At the moment this is 3.14.3.

https://www.python.org/downloads/release/python-3143/

---

### 评论 #4 — lucbruni-amd (2026-02-19T17:47:16Z)

> Please support the current version. At the moment this is 3.14.3.
> 
> https://www.python.org/downloads/release/python-3143/

This is being tracked here: https://github.com/ROCm/TheRock/issues/2640

---

### 评论 #5 — lucbruni-amd (2026-02-20T19:24:09Z)

> thanks alot , kinda triton in window already working with zluda via isqhytiger github
> 
> if possible when gfx110X will support official triton in window

Refer to [this comment](https://github.com/ROCm/TheRock/issues/1278#issuecomment-3389841623) regarding official Windows support. However, the next best alternative is available as the [legacy/community-driven fork](https://github.com/woct0rdho/triton-windows) for Windows support has been moved to the [triton-lang organization](https://github.com/triton-lang/triton-windows), and is under active development with AMD support. See installation tips [here](https://github.com/triton-lang/triton-windows?tab=readme-ov-file#7-triton), and also the [PyPI project](https://pypi.org/project/triton-windows/). `gfx110X` should be supported when paired with [TheRock Torch wheels](https://github.com/ROCm/TheRock/blob/main/RELEASES.md). See [this PR](https://github.com/woct0rdho/triton-windows/pull/179) for more context. Run the following [tests](https://github.com/triton-lang/triton-windows?tab=readme-ov-file#test-if-it-works) to validate.

---

### 评论 #6 — xalteropsx (2026-03-23T02:44:40Z)

i am getting false print(hasattr(torch._C, "_c10d_init")) False

is window torch Version: 2.12.0a0+rocm7.13.0a20260313 has limitation ? 

---

### 评论 #7 — lucbruni-amd (2026-03-23T16:11:44Z)

> i am getting false print(hasattr(torch._C, "_c10d_init")) False
> 
> is window torch Version: 2.12.0a0+rocm7.13.0a20260313 has limitation ?

Please see https://github.com/triton-lang/triton-windows/issues/2 for more information regarding issue tracking for `triton-windows` - I recommend you open a new issue [here](https://github.com/triton-lang/triton-windows/issues) to give it some visibility for the maintainers.

Also, are you a member of the [AMD Developer Community Discord server](https://www.amd.com/en/developer/browse-by-resource-type/community.html)? We have a wonderful and helpful community there that may provide additional help for some of the miscellaneous questions and issues brought up here. If you are a member, I highly recommend posting some of your questions under the `#rocm-build-install-help` channel as well.

Do note that `triton-windows` is not "official" as in it is not provided by Triton/OpenAI themselves, but AMD is helping maintain it.

`triton-windows` integration into [TheRock](https://github.com/ROCm/TheRock) has also been merged (see https://github.com/ROCm/TheRock/pull/4006), providing an alternative installation path.

---

### 评论 #8 — lucbruni-amd (2026-04-30T19:06:16Z)

Since 3.11 and 3.14 Pytorch wheels are being built via TheRock, Windows Triton support is upstreamed under the triton-land org and is being co-developed by AMD, and official Windows TF support is not planned - I will close this issue. Thank you for providing feedback and reporting issues around the ROCm ecosystem!

---
