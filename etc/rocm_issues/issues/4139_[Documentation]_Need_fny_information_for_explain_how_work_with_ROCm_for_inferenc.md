# [Documentation]: Need fny information for explain how work with ROCm for inference model Yolov8

> **Issue #4139**
> **状态**: closed
> **创建时间**: 2024-12-09T11:53:17Z
> **更新时间**: 2024-12-16T16:35:09Z
> **关闭时间**: 2024-12-16T16:35:09Z
> **作者**: ViktorPavlovA
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4139

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Description of errors

Hello, ROCm community. 

I have a question how to use this environment to infer the model and translate the model from fp32 -> fp16 without using tensorflow or pytorch . For example in tensorrt (sorry for this ) i have cpp and python3 api to transfer model in onnx to graphic card model format. Is it possible to do it with using ROCm?

Thank you so much!

### Attach any links, screenshots, or additional evidence you think will be helpful.

.

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-12-11T17:01:06Z)

Hi @ViktorPavlovA, this can be done with ROCm using the MIGraphX library. Here is an example of quantization of YOLOv4 to FP16 ([Object Detection with YoloV4](https://github.com/ROCm/AMDMIGraphX/blob/develop/examples/vision/python_yolov4/yolov4_inference.ipynb)). In this example, we start with an ONNX model and use the `migraphx-driver` tool with flag `--fp16` to compile it to FP16.

Please also refer to the [MIGraphX Driver Options](https://github.com/ROCm/AMDMIGraphX/tree/0860461d626f8cd42a443335c0764925f8195e9c/examples/migraphx/migraphx_driver#options) for a more extensive list of the tools features.

---

### 评论 #2 — ViktorPavlovA (2024-12-11T18:05:13Z)

@harkgill-amd , thank you! I will try to used it ) and answered after all.

---

### 评论 #3 — harkgill-amd (2024-12-16T16:35:09Z)

No problem! 

I'll close out this issue for now. Feel free to leave a comment if you have any other questions.

---
