# [Issue]: Unable to fine tune Lamma3

> **Issue #4468**
> **状态**: closed
> **创建时间**: 2025-03-08T14:05:09Z
> **更新时间**: 2025-03-24T17:36:32Z
> **关闭时间**: 2025-03-24T17:36:32Z
> **作者**: EngrAwab
> **标签**: Under Investigation, AMD Radeon Pro W7900, ROCm 6.2.3
> **URL**: https://github.com/ROCm/ROCm/issues/4468

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon Pro W7900** (颜色: #ededed)
- **ROCm 6.2.3** (颜色: #ededed)

## 描述

### Problem Description

I was following the AMD doc to fine tune lama 3 https://rocm.docs.amd.com/projects/ai-developer-hub/en/latest/notebooks/fine_tune/QLoRA_Llama-3.1.html
and got this issues by the running the cell 
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True, 
    bnb_4bit_quant_type="nf4", 
    bnb_4bit_compute_dtype="float16", 
    bnb_4bit_use_double_quant=True
)

# Load the pre-trained Llama-3.1 model with device mapping for GPU
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    device_map="auto",
    quantization_config=bnb_config,
    trust_remote_code=True
)

# Disable caching to optimize for fine-tuning
base_model.config.use_cache = False
base_model.config.pretraining_tp = 1

---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
Cell In[24], line 9
      1 bnb_config = BitsAndBytesConfig(
      2     load_in_4bit=True, 
      3     bnb_4bit_quant_type="nf4", 
      4     bnb_4bit_compute_dtype="float16", 
      5     bnb_4bit_use_double_quant=True
      6 )
      8 # Load the pre-trained Llama-3.1 model with device mapping for GPU
----> 9 base_model = AutoModelForCausalLM.from_pretrained(
     10     base_model_name,
     11     device_map="auto",
     12     quantization_config=bnb_config,
     13     trust_remote_code=True
     14 )
     16 # Disable caching to optimize for fine-tuning
     17 base_model.config.use_cache = False

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/models/auto/auto_factory.py:564](http://127.0.0.1:8889/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/models/auto/auto_factory.py#line=563), in _BaseAutoModelClass.from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs)
    562 elif type(config) in cls._model_mapping.keys():
    563     model_class = _get_model_class(config, cls._model_mapping)
--> 564     return model_class.from_pretrained(
    565         pretrained_model_name_or_path, *model_args, config=config, **hub_kwargs, **kwargs
    566     )
    567 raise ValueError(
    568     f"Unrecognized configuration class {config.__class__} for this kind of AutoModel: {cls.__name__}.\n"
    569     f"Model type should be one of {', '.join(c.__name__ for c in cls._model_mapping.keys())}."
    570 )

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/modeling_utils.py:4264](http://127.0.0.1:8889/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/modeling_utils.py#line=4263), in PreTrainedModel.from_pretrained(cls, pretrained_model_name_or_path, config, cache_dir, ignore_mismatched_sizes, force_download, local_files_only, token, revision, use_safetensors, weights_only, *model_args, **kwargs)
   4254         load_contexts.append(tp_device)
   4256     with ContextManagers(load_contexts):
   4257         (
   4258             model,
   4259             missing_keys,
   4260             unexpected_keys,
   4261             mismatched_keys,
   4262             offload_index,
   4263             error_msgs,
-> 4264         ) = cls._load_pretrained_model(
   4265             model,
   4266             state_dict,
   4267             loaded_state_dict_keys,  # XXX: rename?
   4268             resolved_archive_file,
   4269             pretrained_model_name_or_path,
   4270             ignore_mismatched_sizes=ignore_mismatched_sizes,
   4271             sharded_metadata=sharded_metadata,
   4272             _fast_init=_fast_init,
   4273             low_cpu_mem_usage=low_cpu_mem_usage,
   4274             device_map=device_map,
   4275             offload_folder=offload_folder,
   4276             offload_state_dict=offload_state_dict,
   4277             dtype=torch_dtype,
   4278             hf_quantizer=hf_quantizer,
   4279             keep_in_fp32_modules=keep_in_fp32_modules,
   4280             gguf_path=gguf_path,
   4281             weights_only=weights_only,
   4282         )
   4284 # make sure token embedding weights are still tied if needed
   4285 model.tie_weights()

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/modeling_utils.py:4777](http://127.0.0.1:8889/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/modeling_utils.py#line=4776), in PreTrainedModel._load_pretrained_model(cls, model, state_dict, loaded_keys, resolved_archive_file, pretrained_model_name_or_path, ignore_mismatched_sizes, sharded_metadata, _fast_init, low_cpu_mem_usage, device_map, offload_folder, offload_state_dict, dtype, hf_quantizer, keep_in_fp32_modules, gguf_path, weights_only)
   4773                 set_module_tensor_to_device(
   4774                     model_to_load, key, "cpu", torch.empty(*param.size(), dtype=dtype)
   4775                 )
   4776     else:
-> 4777         new_error_msgs, offload_index, state_dict_index = _load_state_dict_into_meta_model(
   4778             model_to_load,
   4779             state_dict,
   4780             start_prefix,
   4781             expected_keys,
   4782             device_map=device_map,
   4783             offload_folder=offload_folder,
   4784             offload_index=offload_index,
   4785             state_dict_folder=state_dict_folder,
   4786             state_dict_index=state_dict_index,
   4787             dtype=dtype,
   4788             hf_quantizer=hf_quantizer,
   4789             is_safetensors=is_safetensors,
   4790             keep_in_fp32_modules=keep_in_fp32_modules,
   4791             unexpected_keys=unexpected_keys,
   4792         )
   4793         error_msgs += new_error_msgs
   4794 else:
   4795     # Sharded checkpoint or whole but low_cpu_mem_usage==True

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/modeling_utils.py:944](http://127.0.0.1:8889/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/modeling_utils.py#line=943), in _load_state_dict_into_meta_model(model, state_dict, start_prefix, expected_keys, device_map, offload_folder, offload_index, state_dict_folder, state_dict_index, dtype, hf_quantizer, is_safetensors, keep_in_fp32_modules, unexpected_keys, pretrained_model_name_or_path)
    942     set_module_tensor_to_device(model, param_name, param_device, **set_module_kwargs)
    943 else:
--> 944     hf_quantizer.create_quantized_param(model, param, param_name, param_device, state_dict, unexpected_keys)
    945     # For quantized modules with FSDP[/DeepSpeed](http://127.0.0.1:8889/DeepSpeed) Stage 3, we need to quantize the parameter on the GPU
    946     # and then cast it to CPU to avoid excessive memory usage on each GPU
    947     # in comparison to the sharded model across GPUs.
    948     if is_fsdp_enabled() or is_deepspeed_zero3_enabled():

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/quantizers/quantizer_bnb_4bit.py:238](http://127.0.0.1:8889/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/quantizers/quantizer_bnb_4bit.py#line=237), in Bnb4BitHfQuantizer.create_quantized_param(self, model, param_value, param_name, target_device, state_dict, unexpected_keys)
    235         new_value = new_value.T
    237     kwargs = old_value.__dict__
--> 238     new_value = bnb.nn.Params4bit(new_value, requires_grad=False, **kwargs).to(target_device)
    240 module._parameters[tensor_name] = new_value

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/bitsandbytes-0.42.0-py3.10.egg/bitsandbytes/nn/modules.py:212](http://127.0.0.1:8889/opt/conda/envs/py_3.10/lib/python3.10/site-packages/bitsandbytes-0.42.0-py3.10.egg/bitsandbytes/nn/modules.py#line=211), in Params4bit.to(self, *args, **kwargs)
    209 device, dtype, non_blocking, convert_to_format = torch._C._nn._parse_to(*args, **kwargs)
    211 if (device is not None and device.type == "cuda" and not self.bnb_quantized):
--> 212     return self._quantize(device)
    213 else:
    214     if self.quant_state is not None:

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/bitsandbytes-0.42.0-py3.10.egg/bitsandbytes/nn/modules.py:184](http://127.0.0.1:8889/opt/conda/envs/py_3.10/lib/python3.10/site-packages/bitsandbytes-0.42.0-py3.10.egg/bitsandbytes/nn/modules.py#line=183), in Params4bit._quantize(self, device)
    182 def _quantize(self, device):
    183     w = self.data.contiguous().cuda(device)
--> 184     w_4bit, quant_state = bnb.functional.quantize_4bit(w, blocksize=self.blocksize, compress_statistics=self.compress_statistics,
    185                                                        quant_type=self.quant_type, quant_storage=self.quant_storage)
    186     self.data = w_4bit
    187     self.quant_state = quant_state

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/bitsandbytes-0.42.0-py3.10.egg/bitsandbytes/functional.py:952](http://127.0.0.1:8889/opt/conda/envs/py_3.10/lib/python3.10/site-packages/bitsandbytes-0.42.0-py3.10.egg/bitsandbytes/functional.py#line=951), in quantize_4bit(A, absmax, out, blocksize, compress_statistics, quant_type, quant_storage)
    950     blocks = n // blocksize
    951     blocks += 1 if n % blocksize > 0 else 0
--> 952     absmax = torch.zeros((blocks,), device=A.device, dtype=torch.float32)
    955 if out is None:
    956     mod = dtype2bytes[quant_storage] * 2

RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3.
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

### Operating System

22.04.4 LTS

### CPU

AMD ryzen 9 p00x

### GPU

AMD Radeon PRO w7900

### ROCm Version

6.2.3-124

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — harkgill-amd (2025-03-10T15:49:24Z)

Hi @EngrAwab, just gave the steps in [Fine-tuning Llama-3.1 with QLoRA](https://rocm.docs.amd.com/projects/ai-developer-hub/en/latest/notebooks/fine_tune/QLoRA_Llama-3.1.html) a run and wasn't able to reproduce the `HIP error: invalid device function` on a W7900. I did have to update my bitsandbytes installation from `0.42.0` to `0.43.3.dev0` to get the [Quantization configuration in QLoRA](https://rocm.docs.amd.com/projects/ai-developer-hub/en/latest/notebooks/fine_tune/QLoRA_Llama-3.1.html#quantization-configuration-in-qlora) code block to run, though the errors were not related to your issue.

Could you please set the environment variables `AMD_LOG_LEVEL=3` and `HSAKMT_DEBUG_LEVEL=4` and provide the output when running the script? Also, not sure which CPU you're running on but if it has an iGPU, please disable that as well and give it a rerun. You can either do this directly from the BIOS (preferred) or by setting `HIP_VISIBLE_DEVICES` environment variable to only expose your GPU ([ref](https://rocm.docs.amd.com/en/latest/conceptual/gpu-isolation.html#hip-visible-devices)). 

---

### 评论 #2 — EngrAwab (2025-03-13T14:07:32Z)

I am using this processer https://www.amd.com/en/products/processors/desktops/ryzen/7000-series/amd-ryzen-9-7900x.html
and my bitsandbytes version is  0.42.0 I had verified that as well... 

---

### 评论 #3 — harkgill-amd (2025-03-13T14:16:25Z)

The Ryzen 7900X does include an iGPU. Could you please disable the iGPU and provide the logs as mentioned in https://github.com/ROCm/ROCm/issues/4468#issuecomment-2711049990?

---

### 评论 #4 — EngrAwab (2025-03-15T08:26:37Z)

![Image](https://github.com/user-attachments/assets/fbaaf17b-2deb-41bc-973d-39b0be78274e)

I tried by using this command export HIP_VISIBLE_DEVICES="0" and that issue got resolved but got a new issue 


ValueError                                Traceback (most recent call last)
Cell In[6], line 9
      1 bnb_config = BitsAndBytesConfig(
      2     load_in_4bit=True, 
      3     bnb_4bit_quant_type="nf4", 
      4     bnb_4bit_compute_dtype="float16", 
      5     bnb_4bit_use_double_quant=True
      6 )
      8 # Load the pre-trained Llama-3.1 model with device mapping for GPU
----> 9 base_model = AutoModelForCausalLM.from_pretrained(
     10     base_model_name,
     11     device_map="auto",
     12     quantization_config=bnb_config,
     13     trust_remote_code=True
     14 )
     16 # Disable caching to optimize for fine-tuning
     17 base_model.config.use_cache = False

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/models/auto/auto_factory.py:564](http://127.0.0.1:8888/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/models/auto/auto_factory.py#line=563), in _BaseAutoModelClass.from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs)
    562 elif type(config) in cls._model_mapping.keys():
    563     model_class = _get_model_class(config, cls._model_mapping)
--> 564     return model_class.from_pretrained(
    565         pretrained_model_name_or_path, *model_args, config=config, **hub_kwargs, **kwargs
    566     )
    567 raise ValueError(
    568     f"Unrecognized configuration class {config.__class__} for this kind of AutoModel: {cls.__name__}.\n"
    569     f"Model type should be one of {', '.join(c.__name__ for c in cls._model_mapping.keys())}."
    570 )

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/modeling_utils.py:4342](http://127.0.0.1:8888/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/modeling_utils.py#line=4341), in PreTrainedModel.from_pretrained(cls, pretrained_model_name_or_path, config, cache_dir, ignore_mismatched_sizes, force_download, local_files_only, token, revision, use_safetensors, weights_only, *model_args, **kwargs)
   4339         device_map_kwargs["offload_buffers"] = True
   4341     if not is_fsdp_enabled() and not is_deepspeed_zero3_enabled():
-> 4342         dispatch_model(model, **device_map_kwargs)
   4344 if hf_quantizer is not None:
   4345     hf_quantizer.postprocess_model(model)

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/accelerate/big_modeling.py:498](http://127.0.0.1:8888/opt/conda/envs/py_3.10/lib/python3.10/site-packages/accelerate/big_modeling.py#line=497), in dispatch_model(model, device_map, main_device, state_dict, offload_dir, offload_index, offload_buffers, skip_keys, preload_module_classes, force_hooks)
    496     device = f"xpu:{device}"
    497 if device != "disk":
--> 498     model.to(device)
    499 else:
    500     raise ValueError(
    501         "You are trying to offload the whole model to the disk. Please use the `disk_offload` function instead."
    502     )

File [/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/modeling_utils.py:3154](http://127.0.0.1:8888/opt/conda/envs/py_3.10/lib/python3.10/site-packages/transformers/modeling_utils.py#line=3153), in PreTrainedModel.to(self, *args, **kwargs)
   3149         raise ValueError(
   3150             "`.to` is not supported for `8-bit` bitsandbytes models. Please use the model as it is, since the"
   3151             " model has already been set to the correct devices and casted to the correct `dtype`."
   3152         )
   3153     elif version.parse(importlib.metadata.version("bitsandbytes")) < version.parse("0.43.2"):
-> 3154         raise ValueError(
   3155             "Calling `to()` is not supported for `4-bit` quantized models with the installed version of bitsandbytes. "
   3156             f"The current device is `{self.device}`. If you intended to move the model, please install bitsandbytes >= 0.43.2."
   3157         )
   3158 elif getattr(self, "quantization_method", None) == QuantizationMethod.GPTQ:
   3159     if dtype_present_in_args:

ValueError: Calling `to()` is not supported for `4-bit` quantized models with the installed version of bitsandbytes. The current device is `cuda:0`. If you intended to move the model, please install bitsandbytes >= 0.43.2.

![Image](https://github.com/user-attachments/assets/6890d7bb-5575-492a-a699-252b9fcbaef0)

---

### 评论 #5 — harkgill-amd (2025-03-19T17:29:45Z)

> ValueError: Calling to() is not supported for 4-bit quantized models with the installed version of bitsandbytes. The current device is cuda:0. If you intended to move the model, please install bitsandbytes >= 0.43.2.

This is the bitsandbytes error I mentioned in https://github.com/ROCm/ROCm/issues/4468#issuecomment-2711049990. To resolve this, uninstall bitsandbytes with
```
pip uninstall bitsandbytes
```
Then install the `0.43.3.dev0` version for ROCm with 
```
git clone --recurse https://github.com/ROCm/bitsandbytes
cd bitsandbytes
git checkout rocm_enabled_multi_backend
pip install -r requirements-dev.txt
cmake -DCOMPUTE_BACKEND=hip -S . 
make
pip install .
```

---

### 评论 #6 — EngrAwab (2025-03-23T12:11:40Z)

```
    516         return torch.empty(A.shape[:-1] + B_shape[:1], dtype=A.dtype, device=A.device)
    518 # 1. Dequantize
    519 # 2. MatmulnN
--> 520 output = torch.nn.functional.linear(A, F.dequantize_4bit(B, quant_state).to(A.dtype).t(), bias)
    522 # 3. Save state
    523 ctx.state = quant_state

OutOfMemoryError: HIP out of memory. Tried to allocate 224.00 MiB. GPU 
```

Now I ran again with this configuration 
`from transformers import TrainingArguments

train_params = TrainingArguments(
    output_dir="./results_qlora",
    num_train_epochs=1,

    per_device_train_batch_size=2,                 # Slightly increased batch size (you have 48 GB)
    gradient_accumulation_steps=2,                 # Effective batch size = 4 (2x2)

    optim="paged_adamw_32bit",                     # Recommended for QLoRA
    save_steps=50,
    logging_steps=50,
    learning_rate=4e-5,
    weight_decay=0.001,

    fp16=False,                                    # Disabled because ROCm prefers bf16 on W7900
    bf16=True,                                     # ✅ Enable BF16 for ROCm + RDNA3 (W7900)

    max_grad_norm=0.3,
    max_steps=-1,
    warmup_ratio=0.03,
    group_by_length=True,
    lr_scheduler_type="constant",
    report_to="tensorboard"
)
`
and now it worked 

---

### 评论 #7 — harkgill-amd (2025-03-24T15:58:51Z)

Nice! Playing around with the training arguments is a good way to workaround any OOM errors. If everything is good on your end, feel free to close out this issue.

---
