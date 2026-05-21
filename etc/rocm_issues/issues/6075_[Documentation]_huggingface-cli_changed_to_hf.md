# [Documentation]: huggingface-cli changed to hf

> **Issue #6075**
> **状态**: closed
> **创建时间**: 2026-03-28T19:39:07Z
> **更新时间**: 2026-04-21T15:31:59Z
> **关闭时间**: 2026-04-21T15:31:59Z
> **作者**: ckime-amd
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/6075

## 负责人

- harkgill-amd

## 描述

### Description of errors

The documentation uses `huggingface-cli` in multiple places in examples.  

The CLI changed to `hf` in 1.0, re: [Say hello to `hf`: a faster, friendlier Hugging Face CLI ](https://huggingface.co/blog/hf-cli).  

The documentation should be changed to use `hf` in examples, I specifically hit the issue with [Benchmark Llama 3.3/3.1 FP4 inference with vLLM](https://rocm.docs.amd.com/en/docs-7.0-docker/benchmark-docker/inference-vllm-llama-3.1-405b-fp4.html), but a search of the documentation finds numerous other examples ([21 files under docs](https://github.com/search?q=repo%3AROCm%2FROCm+huggingface-cli&type=code)). 

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2026-04-20T19:14:20Z)

Thanks for the report @ckime-amd. The docs team is aware of this and will be updating the commands in a future docs release.

---
