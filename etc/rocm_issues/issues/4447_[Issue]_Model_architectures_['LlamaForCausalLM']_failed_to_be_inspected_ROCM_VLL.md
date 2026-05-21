# [Issue]: Model architectures ['LlamaForCausalLM'] failed to be inspected ROCM VLLM

> **Issue #4447**
> **状态**: closed
> **创建时间**: 2025-03-05T06:59:38Z
> **更新时间**: 2025-07-15T05:38:45Z
> **关闭时间**: 2025-07-15T05:38:45Z
> **作者**: prudencedev
> **标签**: Under Investigation, ROCm 6.3.1
> **URL**: https://github.com/ROCm/ROCm/issues/4447

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.1** (颜色: #ededed)

## 描述

### Problem Description

I have an AMD GPU (RX 6800 XT) and am unable to run Docker with vLLM. Below are the details of my setup:

export MODEL=amd/Llama-3.1-8B-Instruct-FP8-KV
export DOCKER_IMG=rocm/vllm:rocm6.3.1_mi300_ubuntu22.04_py3.12_vllm_0.6.6
export HOST_PORT=80
export HF_TOKEN="xxxxxxxxxxx" 

docker run --rm --device=/dev/kfd --device=/dev/dri --group-add video --shm-size 16G \
    -p $HOST_PORT:$HOST_PORT \
    --security-opt seccomp=unconfined \
    --security-opt apparmor=unconfined \
    --cap-add=SYS_PTRACE \
    -v $(pwd):/workspace \
    --env HUGGINGFACE_HUB_CACHE=/workspace \
    --env VLLM_USE_TRITON_FLASH_ATTN=0 \
    --env PYTORCH_TUNABLEOP_ENABLED=1 \
    --env TORCH_USE_HIP_DSA=1 \
    --env HF_TOKEN=$HF_TOKEN \
    --env AMD_SERIALIZE_KERNEL=1 \ 
    $DOCKER_IMG python3 -m vllm.entrypoints.openai.api_server \
    --model $MODEL \
    --swap-space 16 \
    --disable-log-requests \
    --dtype float16 \
    --quantization fp8 \
    --kv-cache-dtype fp8 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9 \
    --host 0.0.0.0 \
    --port $HOST_PORT \
    --distributed-executor-backend "mp"


### Operating System

ubuntu-24.04.1-live-server-amd64

### CPU

 Intel(R) Core(TM) i7-10700F CPU @ 2.90GHz

### GPU

[AMD/ATI] Navi 21 [Radeon RX 6800/6800 XT / 6900 XT]

### ROCm Version

6.3.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — harkgill-amd (2025-03-05T20:55:45Z)

Hi @prudencedev, the `rocm/vllm:rocm6.3.1_mi300_ubuntu22.04_py3.12_vllm_0.6.6` is intended for use with MI300 only. For Navi cards, please try the `navi_nightly` image from [rocm/vllm-dev](https://hub.docker.com/r/rocm/vllm-dev/tags). 

I wasn't able to reproduce the errors you've reported, but switching to the Navi specific image enabled vllm on my end. Still seeing errors related to `torch._scaled_mm` but those have to do with the FP8 quantization of the `amd/Llama-3.1-8B-Instruct-FP8-KV` model specifically. Other models that offer different quantization formats are working fine.

---

### 评论 #2 — prudencedev (2025-03-06T03:57:31Z)

Dear harkgill-amd,

Thank you for the information. I appreciate you clarifying the image
compatibility.

I'm interested in trying out the `navi_nightly` image on my Navi card.
Could you please share the steps on how to run vllm using this image? Any
guidance would be greatly appreciated.

Thank you,
Vinayak


On Thu, 6 Mar, 2025, 2:26 am harkgill-amd, ***@***.***> wrote:

> Hi @prudencedev <https://github.com/prudencedev>, the
> rocm/vllm:rocm6.3.1_mi300_ubuntu22.04_py3.12_vllm_0.6.6 is intended for
> use with MI300 only. For Navi cards, please try the navi_nightly image
> from rocm/vllm-dev <https://hub.docker.com/r/rocm/vllm-dev/tags>.
>
> I wasn't able to reproduce the errors you've reported, but switching to
> the Navi specific image enabled vllm on my end. Still seeing errors related
> to torch._scaled_mm but those have to do with the FP8 quantization of the
> amd/Llama-3.1-8B-Instruct-FP8-KV model specifically. Other models that
> offer different quantization formats are working fine.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2702057340>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/BKZKVX2OWRE5L4JLJVVNIW32S5QGNAVCNFSM6AAAAABYLJYXROVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDOMBSGA2TOMZUGA>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
> [image: harkgill-amd]*harkgill-amd* left a comment (ROCm/ROCm#4447)
> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2702057340>
>
> Hi @prudencedev <https://github.com/prudencedev>, the
> rocm/vllm:rocm6.3.1_mi300_ubuntu22.04_py3.12_vllm_0.6.6 is intended for
> use with MI300 only. For Navi cards, please try the navi_nightly image
> from rocm/vllm-dev <https://hub.docker.com/r/rocm/vllm-dev/tags>.
>
> I wasn't able to reproduce the errors you've reported, but switching to
> the Navi specific image enabled vllm on my end. Still seeing errors related
> to torch._scaled_mm but those have to do with the FP8 quantization of the
> amd/Llama-3.1-8B-Instruct-FP8-KV model specifically. Other models that
> offer different quantization formats are working fine.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2702057340>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/BKZKVX2OWRE5L4JLJVVNIW32S5QGNAVCNFSM6AAAAABYLJYXROVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDOMBSGA2TOMZUGA>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #3 — harkgill-amd (2025-03-06T15:25:32Z)

Sure, you can run the following command to enter into the `navi_nightly` image. Docker will pull the image if you haven't already done so. 

```
sudo docker run -it --network=host --group-add=video --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device /dev/kfd --device /dev/dri rocm/vllm-dev:navi_nightly
```
Then to run the model 
```
vllm serve <model>
#Example 
vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
```
For more information and a similar example, you can reference the documentation at [vLLM Docker image for Llama2 and Llama3](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/advanced/vllm/build-docker-image.html#vllm-docker-image-for-llama2-and-llama3).

---

### 评论 #4 — prudencedev (2025-03-13T06:49:31Z)

Hi ROCm/ROCm

I am getting an error

[image: image.png][image: image.png]

Regards,
Vinayak Walanj

On Thu, Mar 6, 2025 at 8:55 PM harkgill-amd ***@***.***>
wrote:

> Sure, you can run the following command to enter into the navi_nightly
> image. Docker will pull the image if you haven't already done so.
>
> sudo docker run -it --network=host --group-add=video --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device /dev/kfd --device /dev/dri rocm/vllm-dev:navi_nightly
>
> Then to run the model
>
> vllm serve <model>
> #Example
> vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
>
> For more information and a similar example, you can reference the
> documentation at vLLM Docker image for Llama2 and Llama3
> <https://rocm.docs.amd.com/projects/radeon/en/latest/docs/advanced/vllm/build-docker-image.html#vllm-docker-image-for-llama2-and-llama3>
> .
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2704171031>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/BKZKVX73Z4T2QVOUDM37CJ32TBSIHAVCNFSM6AAAAABYLJYXROVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDOMBUGE3TCMBTGE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
> [image: harkgill-amd]*harkgill-amd* left a comment (ROCm/ROCm#4447)
> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2704171031>
>
> Sure, you can run the following command to enter into the navi_nightly
> image. Docker will pull the image if you haven't already done so.
>
> sudo docker run -it --network=host --group-add=video --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device /dev/kfd --device /dev/dri rocm/vllm-dev:navi_nightly
>
> Then to run the model
>
> vllm serve <model>
> #Example
> vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
>
> For more information and a similar example, you can reference the
> documentation at vLLM Docker image for Llama2 and Llama3
> <https://rocm.docs.amd.com/projects/radeon/en/latest/docs/advanced/vllm/build-docker-image.html#vllm-docker-image-for-llama2-and-llama3>
> .
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2704171031>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/BKZKVX73Z4T2QVOUDM37CJ32TBSIHAVCNFSM6AAAAABYLJYXROVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDOMBUGE3TCMBTGE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #5 — prudencedev (2025-03-13T06:51:59Z)

Dear harkgill-amd,

Thank you for the previous instructions. I have encountered an error while
trying to run the model.

I am now attempting to use the command `vllm serve meta-llama/Llama-3.1-8B
--max-model-len=32768`.

I have installed Docker on my machine and the ROCm drivers are already
present in the `rocm/vllm-dev:navi_nightly` image. Do I need to install the
drivers manually again?

Thank you,
Vinayak



On Thu, Mar 13, 2025 at 12:19 PM Vinayak Walanj <
***@***.***> wrote:

> Hi ROCm/ROCm
>
> I am getting an error
>
> [image: image.png][image: image.png]
>
> Regards,
> Vinayak Walanj
>
> On Thu, Mar 6, 2025 at 8:55 PM harkgill-amd ***@***.***>
> wrote:
>
>> Sure, you can run the following command to enter into the navi_nightly
>> image. Docker will pull the image if you haven't already done so.
>>
>> sudo docker run -it --network=host --group-add=video --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device /dev/kfd --device /dev/dri rocm/vllm-dev:navi_nightly
>>
>> Then to run the model
>>
>> vllm serve <model>
>> #Example
>> vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
>>
>> For more information and a similar example, you can reference the
>> documentation at vLLM Docker image for Llama2 and Llama3
>> <https://rocm.docs.amd.com/projects/radeon/en/latest/docs/advanced/vllm/build-docker-image.html#vllm-docker-image-for-llama2-and-llama3>
>> .
>>
>> —
>> Reply to this email directly, view it on GitHub
>> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2704171031>, or
>> unsubscribe
>> <https://github.com/notifications/unsubscribe-auth/BKZKVX73Z4T2QVOUDM37CJ32TBSIHAVCNFSM6AAAAABYLJYXROVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDOMBUGE3TCMBTGE>
>> .
>> You are receiving this because you were mentioned.Message ID:
>> ***@***.***>
>> [image: harkgill-amd]*harkgill-amd* left a comment (ROCm/ROCm#4447)
>> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2704171031>
>>
>> Sure, you can run the following command to enter into the navi_nightly
>> image. Docker will pull the image if you haven't already done so.
>>
>> sudo docker run -it --network=host --group-add=video --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device /dev/kfd --device /dev/dri rocm/vllm-dev:navi_nightly
>>
>> Then to run the model
>>
>> vllm serve <model>
>> #Example
>> vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
>>
>> For more information and a similar example, you can reference the
>> documentation at vLLM Docker image for Llama2 and Llama3
>> <https://rocm.docs.amd.com/projects/radeon/en/latest/docs/advanced/vllm/build-docker-image.html#vllm-docker-image-for-llama2-and-llama3>
>> .
>>
>> —
>> Reply to this email directly, view it on GitHub
>> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2704171031>, or
>> unsubscribe
>> <https://github.com/notifications/unsubscribe-auth/BKZKVX73Z4T2QVOUDM37CJ32TBSIHAVCNFSM6AAAAABYLJYXROVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDOMBUGE3TCMBTGE>
>> .
>> You are receiving this because you were mentioned.Message ID:
>> ***@***.***>
>>
>


---

### 评论 #6 — harkgill-amd (2025-03-13T21:03:50Z)

Could you please provide more information error that you're encountering, the image you sent doesn't seem to be displaying correctly.

> I have installed Docker on my machine and the ROCm drivers are already present in the `rocm/vllm-dev:navi_nightly` image. Do I need to install the drivers manually again?

You don't need to install anything once you've launched a container with the image, it already has all the necessary components. You do however need the `amdgpu-dkms` kernel driver installed on the host. For more information, please see [Running ROCm Docker Containers Prerequisites](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/docker.html#prerequisites).

---

### 评论 #7 — prudencedev (2025-03-17T04:09:09Z)

Hi ROCm/ROCm,

Following up on my previous email, I am providing more details regarding
the error I encountered.

The `dkms status` shows that `amdgpu/6.10.5-2095006.24.04,
6.8.0-55-generic, x86_64` is installed.

I have attached the `vllmerror` and `rocminfo` files for your reference.

Regards,
Vinayak

On Fri, Mar 14, 2025 at 2:34 AM harkgill-amd ***@***.***>
wrote:

> Could you please provide more information error that you're encountering,
> the image you sent doesn't seem to be displaying correctly.
>
> I have installed Docker on my machine and the ROCm drivers are already
> present in the rocm/vllm-dev:navi_nightly image. Do I need to install the
> drivers manually again?
>
> You don't need to install anything once you've launched a container with
> the image, it already has all the necessary components. You do however need
> the amdgpu-dkms kernel driver installed on the host. For more
> information, please see Running ROCm Docker Containers Prerequisites
> <https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/docker.html#prerequisites>
> .
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2722686933>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/BKZKVX75EDSR6GZPD5YJXDL2UHXE3AVCNFSM6AAAAABYLJYXROVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDOMRSGY4DMOJTGM>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
> [image: harkgill-amd]*harkgill-amd* left a comment (ROCm/ROCm#4447)
> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2722686933>
>
> Could you please provide more information error that you're encountering,
> the image you sent doesn't seem to be displaying correctly.
>
> I have installed Docker on my machine and the ROCm drivers are already
> present in the rocm/vllm-dev:navi_nightly image. Do I need to install the
> drivers manually again?
>
> You don't need to install anything once you've launched a container with
> the image, it already has all the necessary components. You do however need
> the amdgpu-dkms kernel driver installed on the host. For more
> information, please see Running ROCm Docker Containers Prerequisites
> <https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/docker.html#prerequisites>
> .
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/4447#issuecomment-2722686933>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/BKZKVX75EDSR6GZPD5YJXDL2UHXE3AVCNFSM6AAAAABYLJYXROVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDOMRSGY4DMOJTGM>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>

***@***.***:/app# vllm serve meta-llama/Llama-3.1-8B
INFO 03-17 03:56:53 [__init__.py:256] Automatically detected platform rocm.
INFO 03-17 03:56:54 [api_server.py:912] vLLM API server version 0.7.4.dev274+g0f2300e3d
INFO 03-17 03:56:54 [api_server.py:913] args: Namespace(subparser='serve', model_tag='meta-llama/Llama-3.1-8B', config='', host=None, port=8000, uvicorn_log_level='info', allow_credentials=False, allowed_origins=['*'], allowed_methods=['*'], allowed_headers=['*'], api_key=None, lora_modules=None, prompt_adapters=None, chat_template=None, chat_template_content_format='auto', response_role='assistant', ssl_keyfile=None, ssl_certfile=None, ssl_ca_certs=None, enable_ssl_refresh=False, ssl_cert_reqs=0, root_path=None, middleware=[], return_tokens_as_token_ids=False, disable_frontend_multiprocessing=False, enable_request_id_headers=False, enable_auto_tool_choice=False, tool_call_parser=None, tool_parser_plugin='', model='meta-llama/Llama-3.1-8B', task='auto', tokenizer=None, hf_config_path=None, skip_tokenizer_init=False, revision=None, code_revision=None, tokenizer_revision=None, tokenizer_mode='auto', trust_remote_code=False, allowed_local_media_path=None, download_dir=None, load_format='auto', config_format=<ConfigFormat.AUTO: 'auto'>, dtype='auto', kv_cache_dtype='auto', max_model_len=None, guided_decoding_backend='xgrammar', logits_processor_pattern=None, model_impl='auto', distributed_executor_backend=None, pipeline_parallel_size=1, tensor_parallel_size=1, enable_expert_parallel=False, max_parallel_loading_workers=None, ray_workers_use_nsight=False, block_size=None, enable_prefix_caching=None, disable_sliding_window=False, use_v2_block_manager=True, num_lookahead_slots=0, seed=None, swap_space=4, cpu_offload_gb=0, gpu_memory_utilization=0.9, num_gpu_blocks_override=None, max_num_batched_tokens=None, max_num_partial_prefills=1, max_long_partial_prefills=1, long_prefill_token_threshold=0, max_num_seqs=None, max_logprobs=20, disable_log_stats=False, quantization=None, rope_scaling=None, rope_theta=None, hf_overrides=None, enforce_eager=False, max_seq_len_to_capture=8192, disable_custom_all_reduce=False, tokenizer_pool_size=0, tokenizer_pool_type='ray', tokenizer_pool_extra_config=None, limit_mm_per_prompt=None, mm_processor_kwargs=None, disable_mm_preprocessor_cache=False, enable_lora=False, enable_lora_bias=False, max_loras=1, max_lora_rank=16, lora_extra_vocab_size=256, lora_dtype='auto', long_lora_scaling_factors=None, max_cpu_loras=None, fully_sharded_loras=False, enable_prompt_adapter=False, max_prompt_adapters=1, max_prompt_adapter_token=0, device='auto', num_scheduler_steps=1, use_tqdm_on_load=True, multi_step_stream_outputs=True, scheduler_delay_factor=0.0, enable_chunked_prefill=None, speculative_model=None, speculative_model_quantization=None, num_speculative_tokens=None, speculative_disable_mqa_scorer=False, speculative_draft_tensor_parallel_size=None, speculative_max_model_len=None, speculative_disable_by_batch_size=None, ngram_prompt_lookup_max=None, ngram_prompt_lookup_min=None, spec_decoding_acceptance_method='rejection_sampler', typical_acceptance_sampler_posterior_threshold=None, typical_acceptance_sampler_posterior_alpha=None, disable_logprobs_during_spec_decoding=None, model_loader_extra_config=None, ignore_patterns=[], preemption_mode=None, served_model_name=None, qlora_adapter_name_or_path=None, show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, disable_async_output_proc=False, scheduling_policy='fcfs', scheduler_cls='vllm.core.scheduler.Scheduler', override_neuron_config=None, override_pooler_config=None, compilation_config=None, kv_transfer_config=None, worker_cls='auto', worker_extension_cls='', generation_config='auto', override_generation_config=None, enable_sleep_mode=False, calculate_kv_scales=False, additional_config=None, enable_reasoning=False, reasoning_parser=None, disable_log_requests=False, max_log_len=None, disable_fastapi_docs=False, enable_prompt_tokens_details=False, dispatch_function=<function ServeSubcommand.cmd at 0x7e893b772980>)
INFO 03-17 03:56:54 [api_server.py:209] Started engine process with PID 37
config.json: 100%|██████████████████████████████████████████████████████████████████████████████| 826/826 [00:00<00:00, 5.56MB/s]
INFO 03-17 03:56:56 [__init__.py:256] Automatically detected platform rocm.
INFO 03-17 03:57:07 [config.py:577] This model supports multiple tasks: {'reward', 'generate', 'embed', 'score', 'classify'}. Defaulting to 'generate'.
INFO 03-17 03:57:10 [config.py:1507] Disabled the custom all-reduce kernel because it is not working correctly when using two AMD Navi GPUs.
INFO 03-17 03:57:10 [config.py:1519] Disabled the custom all-reduce kernel because it is not working correctly when using two AMD Navi GPUs.
WARNING 03-17 03:57:10 [arg_utils.py:1276] The model has a long context length (131072). This may cause OOM errors during the initial memory profiling phase, or result in low performance due to small KV cache space. Consider setting --max-model-len to a smaller value.
tokenizer_config.json: 100%|████████████████████████████████████████████████████████████████| 50.5k/50.5k [00:00<00:00, 21.7MB/s]
INFO 03-17 03:57:11 [config.py:577] This model supports multiple tasks: {'reward', 'embed', 'score', 'generate', 'classify'}. Defaulting to 'generate'.
tokenizer.json: 100%|███████████████████████████████████████████████████████████████████████| 9.09M/9.09M [00:01<00:00, 5.97MB/s]
INFO 03-17 03:57:14 [config.py:1507] Disabled the custom all-reduce kernel because it is not working correctly when using two AMD Navi GPUs.
INFO 03-17 03:57:14 [config.py:1519] Disabled the custom all-reduce kernel because it is not working correctly when using two AMD Navi GPUs.
WARNING 03-17 03:57:14 [arg_utils.py:1276] The model has a long context length (131072). This may cause OOM errors during the initial memory profiling phase, or result in low performance due to small KV cache space. Consider setting --max-model-len to a smaller value.
INFO 03-17 03:57:14 [llm_engine.py:235] Initializing a V0 LLM engine (v0.7.4.dev274+g0f2300e3d) with config: model='meta-llama/Llama-3.1-8B', speculative_config=None, tokenizer='meta-llama/Llama-3.1-8B', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, override_neuron_config=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=131072, download_dir=None, load_format=LoadFormat.AUTO, tensor_parallel_size=1, pipeline_parallel_size=1, disable_custom_all_reduce=True, quantization=None, enforce_eager=False, kv_cache_dtype=auto,  device_config=cuda, decoding_config=DecodingConfig(guided_decoding_backend='xgrammar', reasoning_backend=None), observability_config=ObservabilityConfig(show_hidden_metrics=False, otlp_traces_endpoint=None, collect_model_forward_time=False, collect_model_execute_time=False), seed=None, served_model_name=meta-llama/Llama-3.1-8B, num_scheduler_steps=1, multi_step_stream_outputs=True, enable_prefix_caching=False, chunked_prefill_enabled=False, use_async_output_proc=True, disable_mm_preprocessor_cache=False, mm_processor_kwargs=None, pooler_config=None, compilation_config={"splitting_ops":[],"compile_sizes":[],"cudagraph_capture_sizes":[256,248,240,232,224,216,208,200,192,184,176,168,160,152,144,136,128,120,112,104,96,88,80,72,64,56,48,40,32,24,16,8,4,2,1],"max_capture_size":256}, use_cached_outputs=True,
special_tokens_map.json: 100%|████████████████████████████████████████████████████████████████| 73.0/73.0 [00:00<00:00, 1.16MB/s]
generation_config.json: 100%|████████████████████████████████████████████████████████████████████| 185/185 [00:00<00:00, 568kB/s]
INFO 03-17 03:57:16 [rocm.py:133] None is not supported in AMD GPUs.
INFO 03-17 03:57:16 [rocm.py:134] Using ROCmFlashAttention backend.
INFO 03-17 03:57:16 [parallel_state.py:948] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, TP rank 0
INFO 03-17 03:57:16 [model_runner.py:1110] Starting to load model meta-llama/Llama-3.1-8B...
ERROR 03-17 03:57:17 [engine.py:411] HIP error: invalid device function
ERROR 03-17 03:57:17 [engine.py:411] HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
ERROR 03-17 03:57:17 [engine.py:411] For debugging consider passing AMD_SERIALIZE_KERNEL=3
ERROR 03-17 03:57:17 [engine.py:411] Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
ERROR 03-17 03:57:17 [engine.py:411] Traceback (most recent call last):
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 402, in run_mp_engine
ERROR 03-17 03:57:17 [engine.py:411]     engine = MQLLMEngine.from_engine_args(engine_args=engine_args,
ERROR 03-17 03:57:17 [engine.py:411]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 125, in from_engine_args
ERROR 03-17 03:57:17 [engine.py:411]     return cls(ipc_path=ipc_path,
ERROR 03-17 03:57:17 [engine.py:411]            ^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 77, in __init__
ERROR 03-17 03:57:17 [engine.py:411]     self.engine = LLMEngine(*args, **kwargs)
ERROR 03-17 03:57:17 [engine.py:411]                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/engine/llm_engine.py", line 274, in __init__
ERROR 03-17 03:57:17 [engine.py:411]     self.model_executor = executor_class(vllm_config=vllm_config, )
ERROR 03-17 03:57:17 [engine.py:411]                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/executor/executor_base.py", line 52, in __init__
ERROR 03-17 03:57:17 [engine.py:411]     self._init_executor()
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/executor/uniproc_executor.py", line 47, in _init_executor
ERROR 03-17 03:57:17 [engine.py:411]     self.collective_rpc("load_model")
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/executor/uniproc_executor.py", line 56, in collective_rpc
ERROR 03-17 03:57:17 [engine.py:411]     answer = run_method(self.driver_worker, method, args, kwargs)
ERROR 03-17 03:57:17 [engine.py:411]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/utils.py", line 2409, in run_method
ERROR 03-17 03:57:17 [engine.py:411]     return func(*args, **kwargs)
ERROR 03-17 03:57:17 [engine.py:411]            ^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/worker/worker.py", line 211, in load_model
ERROR 03-17 03:57:17 [engine.py:411]     self.model_runner.load_model()
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/worker/model_runner.py", line 1113, in load_model
ERROR 03-17 03:57:17 [engine.py:411]     self.model = get_model(vllm_config=self.vllm_config)
ERROR 03-17 03:57:17 [engine.py:411]                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/__init__.py", line 14, in get_model
ERROR 03-17 03:57:17 [engine.py:411]     return loader.load_model(vllm_config=vllm_config)
ERROR 03-17 03:57:17 [engine.py:411]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/loader.py", line 423, in load_model
ERROR 03-17 03:57:17 [engine.py:411]     model = _initialize_model(vllm_config=vllm_config)
ERROR 03-17 03:57:17 [engine.py:411]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/loader.py", line 126, in _initialize_model
ERROR 03-17 03:57:17 [engine.py:411]     return model_class(vllm_config=vllm_config, prefix=prefix)
ERROR 03-17 03:57:17 [engine.py:411]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 519, in __init__
ERROR 03-17 03:57:17 [engine.py:411]     self.model = self._init_model(vllm_config=vllm_config,
ERROR 03-17 03:57:17 [engine.py:411]                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 556, in _init_model
ERROR 03-17 03:57:17 [engine.py:411]     return LlamaModel(vllm_config=vllm_config, prefix=prefix)
ERROR 03-17 03:57:17 [engine.py:411]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/decorators.py", line 151, in __init__
ERROR 03-17 03:57:17 [engine.py:411]     old_init(self, vllm_config=vllm_config, prefix=prefix, **kwargs)
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 358, in __init__
ERROR 03-17 03:57:17 [engine.py:411]     self.start_layer, self.end_layer, self.layers = make_layers(
ERROR 03-17 03:57:17 [engine.py:411]                                                     ^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/utils.py", line 558, in make_layers
ERROR 03-17 03:57:17 [engine.py:411]     maybe_offload_to_cpu(layer_fn(prefix=f"{prefix}.{idx}"))
ERROR 03-17 03:57:17 [engine.py:411]                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 360, in <lambda>
ERROR 03-17 03:57:17 [engine.py:411]     lambda prefix: layer_type(config=config,
ERROR 03-17 03:57:17 [engine.py:411]                    ^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 273, in __init__
ERROR 03-17 03:57:17 [engine.py:411]     self.self_attn = LlamaAttention(
ERROR 03-17 03:57:17 [engine.py:411]                      ^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 184, in __init__
ERROR 03-17 03:57:17 [engine.py:411]     self.rotary_emb = get_rope(
ERROR 03-17 03:57:17 [engine.py:411]                       ^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 1117, in get_rope
ERROR 03-17 03:57:17 [engine.py:411]     rotary_emb = Llama3RotaryEmbedding(head_size, rotary_dim,
ERROR 03-17 03:57:17 [engine.py:411]                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 822, in __init__
ERROR 03-17 03:57:17 [engine.py:411]     super().__init__(head_size, rotary_dim, max_position_embeddings, base,
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 99, in __init__
ERROR 03-17 03:57:17 [engine.py:411]     cache = self._compute_cos_sin_cache()
ERROR 03-17 03:57:17 [engine.py:411]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 116, in _compute_cos_sin_cache
ERROR 03-17 03:57:17 [engine.py:411]     inv_freq = self._compute_inv_freq(self.base)
ERROR 03-17 03:57:17 [engine.py:411]                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 826, in _compute_inv_freq
ERROR 03-17 03:57:17 [engine.py:411]     inv_freqs = super()._compute_inv_freq(base)
ERROR 03-17 03:57:17 [engine.py:411]                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 110, in _compute_inv_freq
ERROR 03-17 03:57:17 [engine.py:411]     inv_freq = 1.0 / (base**(torch.arange(
ERROR 03-17 03:57:17 [engine.py:411]                              ^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411]   File "/usr/local/lib/python3.12/dist-packages/torch/utils/_device.py", line 104, in __torch_function__
ERROR 03-17 03:57:17 [engine.py:411]     return func(*args, **kwargs)
ERROR 03-17 03:57:17 [engine.py:411]            ^^^^^^^^^^^^^^^^^^^^^
ERROR 03-17 03:57:17 [engine.py:411] RuntimeError: HIP error: invalid device function
ERROR 03-17 03:57:17 [engine.py:411] HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
ERROR 03-17 03:57:17 [engine.py:411] For debugging consider passing AMD_SERIALIZE_KERNEL=3
ERROR 03-17 03:57:17 [engine.py:411] Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
ERROR 03-17 03:57:17 [engine.py:411]
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/usr/lib/python3.12/multiprocessing/process.py", line 314, in _bootstrap
    self.run()
  File "/usr/lib/python3.12/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 413, in run_mp_engine
    raise e
  File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 402, in run_mp_engine
    engine = MQLLMEngine.from_engine_args(engine_args=engine_args,
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 125, in from_engine_args
    return cls(ipc_path=ipc_path,
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 77, in __init__
    self.engine = LLMEngine(*args, **kwargs)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/engine/llm_engine.py", line 274, in __init__
    self.model_executor = executor_class(vllm_config=vllm_config, )
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/executor/executor_base.py", line 52, in __init__
    self._init_executor()
  File "/usr/local/lib/python3.12/dist-packages/vllm/executor/uniproc_executor.py", line 47, in _init_executor
    self.collective_rpc("load_model")
  File "/usr/local/lib/python3.12/dist-packages/vllm/executor/uniproc_executor.py", line 56, in collective_rpc
    answer = run_method(self.driver_worker, method, args, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/utils.py", line 2409, in run_method
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/worker/worker.py", line 211, in load_model
    self.model_runner.load_model()
  File "/usr/local/lib/python3.12/dist-packages/vllm/worker/model_runner.py", line 1113, in load_model
    self.model = get_model(vllm_config=self.vllm_config)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/__init__.py", line 14, in get_model
    return loader.load_model(vllm_config=vllm_config)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/loader.py", line 423, in load_model
    model = _initialize_model(vllm_config=vllm_config)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/loader.py", line 126, in _initialize_model
    return model_class(vllm_config=vllm_config, prefix=prefix)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 519, in __init__
    self.model = self._init_model(vllm_config=vllm_config,
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 556, in _init_model
    return LlamaModel(vllm_config=vllm_config, prefix=prefix)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/decorators.py", line 151, in __init__
    old_init(self, vllm_config=vllm_config, prefix=prefix, **kwargs)
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 358, in __init__
    self.start_layer, self.end_layer, self.layers = make_layers(
                                                    ^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/utils.py", line 558, in make_layers
    maybe_offload_to_cpu(layer_fn(prefix=f"{prefix}.{idx}"))
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 360, in <lambda>
    lambda prefix: layer_type(config=config,
                   ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 273, in __init__
    self.self_attn = LlamaAttention(
                     ^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/llama.py", line 184, in __init__
    self.rotary_emb = get_rope(
                      ^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 1117, in get_rope
    rotary_emb = Llama3RotaryEmbedding(head_size, rotary_dim,
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 822, in __init__
    super().__init__(head_size, rotary_dim, max_position_embeddings, base,
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 99, in __init__
    cache = self._compute_cos_sin_cache()
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 116, in _compute_cos_sin_cache
    inv_freq = self._compute_inv_freq(self.base)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 826, in _compute_inv_freq
    inv_freqs = super()._compute_inv_freq(base)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 110, in _compute_inv_freq
    inv_freq = 1.0 / (base**(torch.arange(
                             ^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/torch/utils/_device.py", line 104, in __torch_function__
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

[rank0]:[W317 03:57:17.503686534 ProcessGroupNCCL.cpp:1505] Warning: WARNING: destroy_process_group() was not called before program exit, which can leak resources. For more info, please see https://pytorch.org/docs/stable/distributed.html#shutdown (function operator())
Traceback (most recent call last):
  File "/usr/local/bin/vllm", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/cli/main.py", line 73, in main
    args.dispatch_function(args)
  File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/cli/serve.py", line 33, in cmd
    uvloop.run(run_server(args))
  File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 109, in run
    return __asyncio.run(
           ^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
  File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 61, in wrapper
    return await main
           ^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 947, in run_server
    async with build_async_engine_client(args) as engine_client:
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 139, in build_async_engine_client
    async with build_async_engine_client_from_engine_args(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 233, in build_async_engine_client_from_engine_args
    raise RuntimeError(
RuntimeError: Engine process failed to start. See stack trace for the root cause.
***@***.***:/app# rocminfo
clinfo
ROCk module version 6.10.5 is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.14
Runtime Ext Version:     1.6
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    Intel(R) Core(TM) i7-10700F CPU @ 2.90GHz
  Uuid:                    CPU-XX
  Marketing Name:          Intel(R) Core(TM) i7-10700F CPU @ 2.90GHz
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   4800
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            16
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32799920(0x1f47cb0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32799920(0x1f47cb0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32799920(0x1f47cb0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32799920(0x1f47cb0) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1030
  Uuid:                    GPU-19dc3bb6d220d68f
  Marketing Name:          AMD Radeon RX 6800 XT
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      4096(0x1000) KB
    L3:                      131072(0x20000) KB
  Chip ID:                 29631(0x73bf)
  ASIC Revision:           1(0x1)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2575
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            72
  SIMDs per CU:            2
  Shader Engines:          4
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 120
  SDMA engine uCode::      83
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16760832(0xffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1030
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***
Number of platforms:                             1
  Platform Profile:                              FULL_PROFILE
  Platform Version:                              OpenCL 2.1 AMD-APP (3635.0)
  Platform Name:                                 AMD Accelerated Parallel Processing
  Platform Vendor:                               Advanced Micro Devices, Inc.
  Platform Extensions:                           cl_khr_icd cl_amd_event_callback


  Platform Name:                                 AMD Accelerated Parallel Processing
Number of devices:                               1
  Device Type:                                   CL_DEVICE_TYPE_GPU
  Vendor ID:                                     1002h
  Board name:                                    AMD Radeon RX 6800 XT
  Device Topology:                               PCI[ B#3, D#0, F#0 ]
  Max compute units:                             36
  Max work items dimensions:                     3
    Max work items[0]:                           1024
    Max work items[1]:                           1024
    Max work items[2]:                           1024
  Max work group size:                           256
  Preferred vector width char:                   4
  Preferred vector width short:                  2
  Preferred vector width int:                    1
  Preferred vector width long:                   1
  Preferred vector width float:                  1
  Preferred vector width double:                 1
  Native vector width char:                      4
  Native vector width short:                     2
  Native vector width int:                       1
  Native vector width long:                      1
  Native vector width float:                     1
  Native vector width double:                    1
  Max clock frequency:                           2575Mhz
  Address bits:                                  64
  Max memory allocation:                         14588628168
  Image support:                                 Yes
  Max number of images read arguments:           128
  Max number of images write arguments:          8
  Max image 2D width:                            16384
  Max image 2D height:                           16384
  Max image 3D width:                            16384
  Max image 3D height:                           16384
  Max image 3D depth:                            8192
  Max samplers within kernel:                    16
  Max size of kernel argument:                   1024
  Alignment (bits) of base address:              2048
  Minimum alignment (bytes) for any datatype:    128
  Single precision floating point capability
    Denorms:                                     Yes
    Quiet NaNs:                                  Yes
    Round to nearest even:                       Yes
    Round to zero:                               Yes
    Round to +ve and infinity:                   Yes
    IEEE754-2008 fused multiply-add:             Yes
  Cache type:                                    Read/Write
  Cache line size:                               128
  Cache size:                                    16384
  Global memory size:                            17163091968
  Constant buffer size:                          14588628168
  Max number of constant args:                   8
  Local memory type:                             Local
  Local memory size:                             65536
  Max pipe arguments:                            16
  Max pipe active reservations:                  16
  Max pipe packet size:                          1703726280
  Max global variable size:                      14588628168
  Max global variable preferred total size:      17163091968
  Max read/write image args:                     64
  Max on device events:                          1024
  Queue on device max size:                      8388608
  Max on device queues:                          1
  Queue on device preferred size:                262144
  SVM capabilities:
    Coarse grain buffer:                         Yes
    Fine grain buffer:                           Yes
    Fine grain system:                           No
    Atomics:                                     No
  Preferred platform atomic alignment:           0
  Preferred global atomic alignment:             0
  Preferred local atomic alignment:              0
  Kernel Preferred work group size multiple:     32
  Error correction support:                      0
  Unified memory for Host and Device:            0
  Profiling timer resolution:                    1
  Device endianess:                              Little
  Available:                                     Yes
  Compiler available:                            Yes
  Execution capabilities:
    Execute OpenCL kernels:                      Yes
    Execute native function:                     No
  Queue on Host properties:
    Out-of-Order:                                No
    Profiling :                                  Yes
  Queue on Device properties:
    Out-of-Order:                                Yes
    Profiling :                                  Yes
  Platform ID:                                   0x7bca9a458ff0
  Name:                                          gfx1030
  Vendor:                                        Advanced Micro Devices, Inc.
  Device OpenCL C version:                       OpenCL C 2.0
  Driver version:                                3635.0 (HSA1.1,LC)
  Profile:                                       FULL_PROFILE
  Version:                                       OpenCL 2.0
  Extensions:                                    cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_depth_images cl_amd_copy_buffer_p2p cl_amd_assembly_program


---

### 评论 #8 — harkgill-amd (2025-07-11T15:52:47Z)

Thanks for sharing the logs and apologies for my lack of response. I went down a rabbit hole trying to figure out why this wasn't working and if there were any workarounds to enable vLLM on the 6800XT/gfx1030. It turns out while this card is supported for use with ROCm, it's not supported by the ROCm on Radeon releases - which the Navi docker images are built for. 

Building from source and multi stage docker builds were also not successful as vLLM itself only supports gfx1100+ https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html#requirements. As an alternative to vLLM, you can use ollama which utilizes llama.cpp to run LLMs. The steps are simply the following,
```
curl -fsSL https://ollama.com/install.sh | sh 
ollama run <model>
```
For reference, this worked correctly on my end with a 6800XT and ROCm 6.4.1.

---

### 评论 #9 — prudencedev (2025-07-15T05:38:45Z)

Thanks for update on ollama its working fine.

---
