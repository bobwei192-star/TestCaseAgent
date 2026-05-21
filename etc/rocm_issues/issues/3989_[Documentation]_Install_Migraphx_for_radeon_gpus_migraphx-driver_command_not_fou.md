# [Documentation]: Install Migraphx for radeon gpus <migraphx-driver : command not found> and <ERROR: Could not find a version that satisfies the requirement onnxruntime-rocm>

> **Issue #3989**
> **状态**: closed
> **创建时间**: 2024-11-04T19:44:28Z
> **更新时间**: 2024-11-06T21:50:16Z
> **关闭时间**: 2024-11-06T01:04:49Z
> **作者**: WareZTv
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3989

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Description of errors

Hello, theses two lines:
```
echo 'export PATH=$PATH:/opt/rocm-6.2.3/bin' >> ~/.bashrc
source ~/.bashrc
```
needs to be added in the documentation here https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-migraphx.html after the command "sudo apt install migraphx" or else the command "migraphx-driver perf --test" will not be found.

another important error is this one: "ERROR: Could not find a version that satisfies the requirement onnxruntime-rocm" after typing the command 
```pip3 install onnxruntime-rocm -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.0/```
because the right command is this one:
```
pip3 install onnxruntime-rocm -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/
```
You can modify the second error in this webpage: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-migraphx.html#install-migraphx-for-onnx-runtime
### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (7 条)

### 评论 #1 — harkgill-amd (2024-11-05T16:59:15Z)

Hi @WareZTv, thanks for pointing this out. This will be fixed shortly.

---

### 评论 #2 — WareZTv (2024-11-05T20:23:45Z)

no problem, it helps everyone including me so i'm happy to share the issues here

---

### 评论 #3 — harkgill-amd (2024-11-05T20:35:08Z)

Both issues have been addressed over at [Install MIGraphX for ONNX Runtime](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-migraphx.html#install-migraphx-for-onnx-runtime). It was decided to reference the absolute path, `/opt/rocm-6.2.3/bin/migraphx-driver`, for simplicity as it's a simple check to verify the installation. Could you please confirm that the instructions work on your end and close out the ticket?

---

### 评论 #4 — WareZTv (2024-11-05T21:47:24Z)

@harkgill-amd  Works perfectly fine now. Something related to the subject but is less important is this. Under the "Verify MIGraphX installation for ONNX Runtime" section in the same webpage: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-migraphx.html#verify-migraphx-installation-for-onnx-runtime, if i copy paste 
1) first this line:
```
python3
```
then these two lines:
```
import onnxruntime as ort
ort.get_available_providers()
```
then the result is as expected: 
```
>>> import onnxruntime as ort
>>> ort.get_available_providers()
['MIGraphXExecutionProvider', 'ROCMExecutionProvider', 'CPUExecutionProvider']
```

But if i copy paste the 3 lines at the same time only 
```python3```
is taken into account so i have to copy paste the two other lines again which can be destabilizing for those not comfortable with the python console

so maybe this command will be more appropriate for the tutorial:
```
python3 -c "import onnxruntime as ort; print(ort.get_available_providers())"
```

or you can separate the first line from the two others lines, as you prefer

---

### 评论 #5 — WareZTv (2024-11-05T21:48:25Z)

Anyway thanks a lot for being responsive. Not many companies care about their customer like you do. And the more you help us, the more we like to share issues with you to improve rocm so that's win win

---

### 评论 #6 — harkgill-amd (2024-11-06T20:42:11Z)

> python3 -c "import onnxruntime as ort; print(ort.get_available_providers())"

The docs have been updated to use this command. Thanks!

---

### 评论 #7 — WareZTv (2024-11-06T21:50:15Z)

your welcome 👍

---
