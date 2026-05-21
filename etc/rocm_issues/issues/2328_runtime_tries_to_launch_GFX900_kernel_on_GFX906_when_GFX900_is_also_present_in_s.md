# runtime tries to launch GFX900 kernel on GFX906 when GFX900 is also present in system

> **Issue #2328**
> **状态**: closed
> **创建时间**: 2023-07-22T00:15:31Z
> **更新时间**: 2024-01-17T12:59:31Z
> **关闭时间**: 2024-01-17T12:59:31Z
> **作者**: IMbackK
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2328

## 描述

This issue can be reproduced with huggingface transformers

System:
* ROCM 5.6
* torch-2.1.0.dev20230721+rocm5.6 
* GFX900 GPU (MI25) (HIP device 2)
* GFX906 GPU (MI50) (HIP device 1)
* GFX1030 GPU (rx6800xt) (HIP device 0)
* transformers @b257c46a075419c09e5ce5c5aa39bc346ecdb9a5
* Linux 6.4.3 with AMDGPU p2p activated

Reproduction:
1. Have GFX900 and GFX906 gpu in system

2. run the following script:
```
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import argparse

if __name__ == "__main__":

	parser = argparse.ArgumentParser("Transformers llm testing script")
	parser.add_argument('--tokenizer', '-t', help="tokenizer to use")
	parser.add_argument('--model', '-m', required=True, help="model to use")
	parser.add_argument('--device', '-d', default="cpu", help="device to use")
	parser.add_argument('--prompt', '-p', default="Today was a long day ", help="the promt to generate from")
	args = parser.parse_args()

	if args.device != 'cpu':
		dtype = torch.bfloat16
	else:
		dtype = torch.float32

	if args.tokenizer is None:
		tokenizer = AutoTokenizer.from_pretrained(args.model, padding_side='left')
	else:
		tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, padding_side='left')

	model = AutoModelForCausalLM.from_pretrained(args.model, low_cpu_mem_usage=True, torch_dtype=dtype).to(args.device)
	model.eval()

	input_ids = tokenizer(args.prompt, return_tensors="pt").input_ids.to(args.device)
	attention_mask = torch.ones(input_ids.shape, device=args.device, requires_grad=False)
	outputs = model.generate(input_ids, attention_mask=attention_mask, do_sample=True, temperature=1)
	response_decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
	response = response_decoded[0]
	print(response)

```

I used bloom-6b for the model, however this dosent matter. If device is set to the GFX1030 gpu everything works. If the deivce is set to the GFX900 GPU everything works, if the deivce is set to the GFX906 the script fails with:

```
Traceback (most recent call last):
  File "/home/philipp/machine-lerning/Transformersplayground/janachat/test-simple.py", line 29, in <module>
    outputs = model.generate(input_ids, attention_mask=attention_mask, do_sample=True, temperature=1)
  File "/home/philipp/machine-lerning/Transformersplayground/venv/lib/python3.9/site-packages/torch/utils/_contextlib.py", line 115, in decorate_context
    return func(*args, **kwargs)
  File "/home/philipp/machine-lerning/Transformersplayground/venv/lib/python3.9/site-packages/transformers/generation/utils.py", line 1563, in generate
    return self.sample(
  File "/home/philipp/machine-lerning/Transformersplayground/venv/lib/python3.9/site-packages/transformers/generation/utils.py", line 2665, in sample
    next_tokens.tile(eos_token_id_tensor.shape[0], 1).ne(eos_token_id_tensor.unsqueeze(1)).prod(dim=0)
RuntimeError: CUDA driver error: 303
```

running with export AMD_LOG_LEVEL=8 reveals that the runtime appears to try to launch a GFX900 kernel on GFX906:

```
:1:devprogram.cpp           :1873: 1265234165 us: 21877: [tid:0x7f3bf549b740] Error: The program ISA amdgcn-amd-amdhsa--gfx900:xnack- is not compatible with the device ISA amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-Error: create kernel metadata map using COMgr
Error: Cannot Find Global Var Sizes
Error: Cannot create kernels.
```

Indeed removeing the GFX900 gpu from the system makes the GFX906 work

full log:
[tf.log](https://github.com/RadeonOpenCompute/ROCm/files/12135233/tf.log)


---

## 评论 (1 条)

### 评论 #1 — nartmada (2024-01-17T12:59:31Z)

Closing the ticket as the issue has been fixed, please refer to https://github.com/huggingface/transformers/issues/25007.  

---
