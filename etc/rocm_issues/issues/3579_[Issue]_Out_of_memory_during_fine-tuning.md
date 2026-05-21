# [Issue]: Out of memory during fine-tuning

> **Issue #3579**
> **状态**: closed
> **创建时间**: 2024-08-13T22:34:19Z
> **更新时间**: 2024-09-04T14:28:23Z
> **关闭时间**: 2024-09-04T14:28:23Z
> **作者**: lwshanbd
> **标签**: Under Investigation, AMD Instinct MI250X, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3579

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI250X** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

I am attempting to fine-tune Llama2 following the official documentation [here](https://rocm.docs.amd.com/en/latest/how-to/llm-fine-tuning-optimization/single-gpu-fine-tuning-and-inference.html) on a machine equipped with 4 MI 250X GPUs. Despite strictly adhering to the instructions, the fine-tuning process failed on both single GPU and multiple GPU configurations.



### Operating System

Red Hat Enterprise Linux(Docker: Ubuntu)

### CPU

AMD EPYC 7A53

### GPU

AMD Instinct MI250X

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

https://rocm.docs.amd.com/en/latest/how-to/llm-fine-tuning-optimization/single-gpu-fine-tuning-and-inference.html and https://rocm.docs.amd.com/en/latest/how-to/llm-fine-tuning-optimization/multi-gpu-fine-tuning-and-inference.html

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

[rocminfo.txt](https://github.com/user-attachments/files/16605974/rocminfo.txt)


### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — harkgill-amd (2024-08-14T18:06:50Z)

Hi @lwshanbd, could you please help provide more information on the failure you're encountering? Some preliminary information that would help include:

1. Any error messages.
2. Specific step that you are failing at.
3. Output of torch.cuda.device_count() and torch.cuda.is_available()

Thanks!


---

### 评论 #2 — lwshanbd (2024-08-14T18:35:40Z)

1.
For `peft_model = get_peft_model(base_model, peft_config)`
```
Could not find the bitsandbytes CUDA binary at PosixPath('/var/lib/jenkins/bitsandbytes/bitsandbytes/libbitsandbytes_hip.so')
Could not load bitsandbytes native library: /var/lib/jenkins/bitsandbytes/bitsandbytes/libbitsandbytes_cpu.so: cannot open shared object file: No such file or directory
Traceback (most recent call last):
  File "/var/lib/jenkins/bitsandbytes/bitsandbytes/cextension.py", line 124, in <module>
    lib = get_native_library()
  File "/var/lib/jenkins/bitsandbytes/bitsandbytes/cextension.py", line 104, in get_native_library
    dll = ct.cdll.LoadLibrary(str(binary_path))
  File "/opt/conda/envs/py_3.9/lib/python3.9/ctypes/__init__.py", line 460, in LoadLibrary
    return self._dlltype(name)
  File "/opt/conda/envs/py_3.9/lib/python3.9/ctypes/__init__.py", line 382, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: /var/lib/jenkins/bitsandbytes/bitsandbytes/libbitsandbytes_cpu.so: cannot open shared object file: No such file or directory

CUDA Setup failed despite CUDA being available. Please run the following command to get more information:

python -m bitsandbytes

Inspect the output of the command and see if you can locate CUDA libraries. You might need to add them
to your LD_LIBRARY_PATH. If you suspect a bug, please take the information from python -m bitsandbytes
and open an issue at: https://github.com/TimDettmers/bitsandbytes/issues

```
For `sft_trainer.train()`
```
Original Traceback (most recent call last):
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/nn/parallel/parallel_apply.py", line 83, in _worker
    output = module(*input, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1532, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1541, in _call_impl
    return forward_call(*args, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/peft/peft_model.py", line 1577, in forward
    return self.base_model(
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1532, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1541, in _call_impl
    return forward_call(*args, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/peft/tuners/tuners_utils.py", line 188, in forward
    return self.model.forward(*args, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/transformers/models/llama/modeling_llama.py", line 1189, in forward
    outputs = self.model(
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1532, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1541, in _call_impl
    return forward_call(*args, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/transformers/models/llama/modeling_llama.py", line 1001, in forward
    layer_outputs = decoder_layer(
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1532, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1541, in _call_impl
    return forward_call(*args, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/transformers/models/llama/modeling_llama.py", line 734, in forward
    hidden_states, self_attn_weights, present_key_value = self.self_attn(
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1532, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1541, in _call_impl
    return forward_call(*args, **kwargs)
  File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/transformers/models/llama/modeling_llama.py", line 660, in forward
    attn_output = torch.nn.functional.scaled_dot_product_attention(
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 29.26 GiB. GPU 0 has a total capacity of 63.98 GiB of which 3.36 GiB is free. Of the allocated memory 59.73 GiB is allocated by PyTorch, and 73.51 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
```

3. `peft_model = get_peft_model(base_model, peft_config)` and `sft_trainer.train()`
4. `8` and `True`

---

### 评论 #3 — harkgill-amd (2024-08-15T17:18:55Z)

Thank you for the information, I will go through the steps on my end and see if I can reproduce the issue. I'll also confirm if it is expected for the tuning to run successfully on MI250X as the testing done in the documentation was with a MI300X.

---

### 评论 #4 — lwshanbd (2024-08-15T17:21:51Z)

Thanks for your help. Although MI250X's memory is less than MI300X, I guess at least it should work on 4 MI250X if the memory could be used resonably.

---

### 评论 #5 — harkgill-amd (2024-08-16T13:15:29Z)

During the example installation of bitsandbytes, the `DBNB_ROCM_ARCH` is set to `gfx942` for MI300X as seen below. When installing for MI250X, this flag should be set to  `DBNB_ROCM_ARCH="gfx90a"`. Could you please confirm if this was done? If not set, please try reinstalling with the correct flag.

```
# Install `bitsandbytes` for ROCm 6.0+.
# Use -DBNB_ROCM_ARCH to target a specific GPU architecture.
git clone --recurse https://github.com/ROCm/bitsandbytes.git
cd bitsandbytes
git checkout rocm_enabled
pip install -r requirements-dev.txt
cmake -DBNB_ROCM_ARCH="gfx942" -DCOMPUTE_BACKEND=hip -S . <------ Graphics Arch Flag
python setup.py install
```

---

### 评论 #6 — lwshanbd (2024-08-16T14:02:37Z)

Yes I installed it with gfx90a.

On Fri, Aug 16, 2024 at 09:15 harkgill-amd ***@***.***> wrote:

> During the example installation of bitsandbytes, the DBNB_ROCM_ARCH is
> set to gfx942 for MI300X as seen below. When installing for MI250X, this
> flag should be set to DBNB_ROCM_ARCH="gfx90a". Could you please confirm
> if this was done? If not please try reinstalling and with the correct flag.
>
> # Install `bitsandbytes` for ROCm 6.0+.
> # Use -DBNB_ROCM_ARCH to target a specific GPU architecture.
> git clone --recurse https://github.com/ROCm/bitsandbytes.git
> cd bitsandbytes
> git checkout rocm_enabled
> pip install -r requirements-dev.txt
> cmake -DBNB_ROCM_ARCH="gfx942" -DCOMPUTE_BACKEND=hip -S . <------ Graphics Arch Flag
> python setup.py install
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/3579#issuecomment-2293491006>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AKMWJUYP3UDR6ATWSBBZS33ZRX3QNAVCNFSM6AAAAABMPFJLROVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDEOJTGQ4TCMBQGY>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #7 — harkgill-amd (2024-08-19T20:24:25Z)

@lwshanbd, quick update. After getting access to the Llama2 models, I was able to reproduce the issues you are seeing on a MI210 system. I was able to resolve the bitsandbytes related errors by doing the following

1. Uninstalling bitsandbytes with `pip uninstall bitsandbytes`.
2. Installing bitsandbytes with the instructions directly from the [`rocm_enabled`](https://github.com/ROCm/bitsandbytes/blob/rocm_enabled/README.md) branch.

```
git clone --recurse https://github.com/ROCm/bitsandbytes
cd bitsandbytes
git checkout rocm_enabled
pip install -r requirements-dev.txt
cmake -DCOMPUTE_BACKEND=hip -S . #Use -DBNB_ROCM_ARCH="gfx90a;gfx942" to target specific gpu arch
make
pip install .
```
Now `peft_model.print_trainable_parameters()` outputs the following 
`trainable params: 33,554,432 || all params: 6,771,970,048 || trainable%: 0.4955`

Could you please give this a try and see if it resolves the first issue? I am still encountering the `torch.OutOfMemoryError: HIP out of memory` and will continue to investigate it further.

---

### 评论 #8 — lwshanbd (2024-08-19T21:39:30Z)

Hey @harkgill-amd ,
Thanks for your help.
For the first issue, yes, it has been fixed by your method.
Looking forward your future reply for the out of memory :-)


---

### 评论 #9 — harkgill-amd (2024-08-20T16:05:01Z)

No problem. For the out of memory error, could you try removing
```
device = "cuda:0"
base_model = AutoModelForCausalLM.from_pretrained(base_model_name, trust_remote_code = True).to(device)
```
and replacing it with
```
base_model = AutoModelForCausalLM.from_pretrained(base_model_name, device_map="auto",  trust_remote_code = True)
```
This should distribute the memory load across multiple GPUs on your system rather than trying to load the whole model onto device0. 

---

### 评论 #10 — harkgill-amd (2024-09-04T14:28:23Z)

Hi @lsamuel-amd, I will close out this issue as the above suggestions resolved both of the errors encountered on my end. 

If you are still seeing errors after applying these changes or feel that the issue has not been addressed, please leave a comment and I will re-open this issue. Thanks!

---
