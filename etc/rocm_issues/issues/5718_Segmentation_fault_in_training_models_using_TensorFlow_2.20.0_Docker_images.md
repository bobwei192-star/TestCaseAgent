# Segmentation fault in training models using TensorFlow 2.20.0 Docker images

> **Issue #5718**
> **状态**: open
> **创建时间**: 2025-11-28T15:15:21Z
> **更新时间**: 2025-11-28T15:15:51Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.1
> **URL**: https://github.com/ROCm/ROCm/issues/5718

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.1** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Training models `tf2_tfm_resnet50_fp16_train` and `tf2_tfm_resnet50_fp32_train` might fail with a segmentation fault when run on the TensorFlow 2.20.0 Dockerimage with ROCm 7.1.1. As a workaround, use TensorFlow 2.19.x Docker image for training the models in ROCm 7.1.1. This issue will be fixed in a future ROCm release.
