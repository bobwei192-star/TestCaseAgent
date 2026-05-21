# How to access AMD GPU with PyTorch

> **Issue #2588**
> **状态**: closed
> **创建时间**: 2023-10-20T05:20:32Z
> **更新时间**: 2023-10-23T08:17:34Z
> **关闭时间**: 2023-10-23T08:14:23Z
> **作者**: Aditya-Scalers
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2588

## 描述

Using PyTorch we are able to access AMD GPU by specifying device as 'cuda'.
Is this the recommended way to access AMD GPU through PyTorch ROCM?
What about 'hip' as a parameter for device?

```
from transformers import GPT2Tokenizer, GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained('gpt2', device_map="auto")
model = GPT2LMHeadModel.from_pretrained('gpt2', device_map="auto")
prompt = "What is Quantum Computing?"

encoded_input = tokenizer(prompt, return_tensors='pt')
encoded_input = encoded_input.to('cuda')

output = model.generate(**encoded_input, max_length=100)
print(tokenizer.decode(output[0], skip_special_tokens = True))
```



---

## 评论 (3 条)

### 评论 #1 — danielzgtg (2023-10-23T07:11:50Z)

> Is this the recommended way to access AMD GPU through PyTorch ROCM?

Yes, that is the recommended way, which I use, according to https://rocm.docs.amd.com/en/latest/how_to/pytorch_install/pytorch_install.html

> What about 'hip' as a parameter for device?

HIP aims to be compatible with CUDA. Many PyTorch projects only care about CUDA, and we are lucky that we can just install the ROCm version of PyTorch and it will still work with 'cuda' as a parameter. We don't want a 'hip' parameter because that would just make us AMD users get cut off from a big chunk of the ecosystem.

---

### 评论 #2 — jithunnair-amd (2023-10-23T08:14:23Z)

@Aditya-Scalers You're right: from the user api perspective, we try to reuse the "cuda" interfaces and types to work on ROCm when using a ROCm-supported build of PyTorch.
Please refer: https://github.com/pytorch/pytorch/blob/fb8876069d89aaf27cc9dace075dd36b8e7df4c7/docs/source/notes/hip.rst#hip-interfaces-reuse-the-cuda-interfaces 
for more details.

A notable exception would be `torch.version.hip`.

---

### 评论 #3 — Aditya-Scalers (2023-10-23T08:17:34Z)

Thanks @danielzgtg, @jithunnair-amd for your response.

---
