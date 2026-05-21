# [Issue]: Unable to Run vLLM Inference on AMD Ryzen AI MAX+ 395

> **Issue #4909**
> **状态**: closed
> **创建时间**: 2025-06-10T07:36:05Z
> **更新时间**: 2025-11-25T03:20:26Z
> **关闭时间**: 2025-11-13T18:15:08Z
> **作者**: FlintyLemming
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4909

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I attempted to use vLLM for model inference on an AMD Ryzen AI MAX+ 395 (gfx1151) with ROCm 6.4.1, as it appears that ROCm 6.4.1 has added support for this GPU.

I pulled and ran the docker image rocm/vllm-dev:rocm6.4.1_navi_ubuntu24.04_py3.12_pytorch_2.6_vllm_0.8.5 (and also tried rocm/vllm-dev:rocm6.4.1_navi_ubuntu24.04_py3.12_pytorch_2.7_vllm_0.8.5), but encountered an "invalid device function" error during inference.

### Operating System

Ubuntu 24.04.2 LTS (Noble Numbat)

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

ROCm 6.4.1

### Steps to Reproduce

1. Downloaded the model files from `https://huggingface.co/Qwen/Qwen3-1.7B` to `/home/flintylemming/models/Qwen3-1.7B`.
2. Pulled the ROCm 6.4.1 Navi vLLM Docker image:
   ```bash
   sudo docker pull rocm/vllm-dev:rocm6.41_navi_ubuntu24.04_py3.12_pytorch_2.7_vllm_0.8.5
   ```
3. Followed the documentation at [Radeon ROCm vLLM Docker guide](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/advanced/vllm/build-docker-image.html) to run the container with the necessary path mapping.

   ```bash
   sudo docker run -it   \
      --privileged   \
      --device=/dev/kfd   \
      --device=/dev/dri   \
      --network=host   \
      --group-add sudo   \
      -w /app/vllm/ \
      -v /home/flintylemming/models:/models  \
      --name vllm \
      rocm/vllm-dev:rocm6.4.1_navi_ubuntu24.04_py3.12_pytorch_2.7_vllm_0.8.5   \
      /bin/bash
   ```

4. Ran the following command to perform model inference:

   ```bash
   vllm serve /models/Qwen3-1.7B
   ```
The full error info below

<details>

<summary>vLLM output</summary>
<pre><code>
INFO 06-10 07:31:36 [__init__.py:239] Automatically detected platform rocm.
INFO 06-10 07:31:45 [api_server.py:1042] vLLM API server version 0.7.4.dev1638+ga7ddaa9b9
INFO 06-10 07:31:45 [api_server.py:1043] args: Namespace(subparser='serve', model_tag='/models/Qwen3-1.7B', config='', host=None, port=8000, uvicorn_log_level='info', disable_uvicorn_access_log=False, allow_credentials=False, allowed_origins=['*'], allowed_methods=['*'], allowed_headers=['*'], api_key=None, lora_modules=None, prompt_adapters=None, chat_template=None, chat_template_content_format='auto', response_role='assistant', ssl_keyfile=None, ssl_certfile=None, ssl_ca_certs=None, enable_ssl_refresh=False, ssl_cert_reqs=0, root_path=None, middleware=[], return_tokens_as_token_ids=False, disable_frontend_multiprocessing=False, enable_request_id_headers=False, enable_auto_tool_choice=False, tool_call_parser=None, tool_parser_plugin='', model='/models/Qwen3-1.7B', task='auto', tokenizer=None, tokenizer_mode='auto', trust_remote_code=False, dtype='auto', seed=None, hf_config_path=None, allowed_local_media_path='', revision=None, code_revision=None, rope_scaling={}, rope_theta=None, tokenizer_revision=None, max_model_len=None, quantization=None, enforce_eager=False, max_seq_len_to_capture=8192, max_logprobs=20, disable_sliding_window=False, disable_cascade_attn=False, skip_tokenizer_init=False, enable_prompt_embeds=False, served_model_name=None, disable_async_output_proc=False, config_format='auto', hf_token=None, hf_overrides={}, override_neuron_config={}, override_pooler_config=None, logits_processor_pattern=None, generation_config='auto', override_generation_config={}, enable_sleep_mode=False, model_impl='auto', load_format='auto', download_dir=None, model_loader_extra_config={}, ignore_patterns=None, use_tqdm_on_load=True, qlora_adapter_name_or_path=None, pt_load_map_location='cpu', guided_decoding_backend='auto', guided_decoding_disable_fallback=False, guided_decoding_disable_any_whitespace=False, guided_decoding_disable_additional_properties=False, enable_reasoning=None, reasoning_parser='', distributed_executor_backend=None, pipeline_parallel_size=1, tensor_parallel_size=1, data_parallel_size=1, enable_expert_parallel=False, max_parallel_loading_workers=None, ray_workers_use_nsight=False, disable_custom_all_reduce=False, worker_cls='auto', worker_extension_cls='', block_size=None, gpu_memory_utilization=0.9, swap_space=4, kv_cache_dtype='auto', num_gpu_blocks_override=None, enable_prefix_caching=None, prefix_caching_hash_algo='builtin', cpu_offload_gb=0, calculate_kv_scales=False, tokenizer_pool_size=0, tokenizer_pool_type='ray', tokenizer_pool_extra_config={}, limit_mm_per_prompt={}, mm_processor_kwargs=None, disable_mm_preprocessor_cache=False, enable_lora=None, enable_lora_bias=False, max_loras=1, max_lora_rank=16, lora_extra_vocab_size=256, lora_dtype='auto', long_lora_scaling_factors=None, max_cpu_loras=None, fully_sharded_loras=False, enable_prompt_adapter=None, max_prompt_adapters=1, max_prompt_adapter_token=0, device='auto', speculative_config=None, show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, max_num_batched_tokens=None, max_num_seqs=None, max_num_partial_prefills=1, max_long_partial_prefills=1, cuda_graph_sizes=[512], long_prefill_token_threshold=0, num_lookahead_slots=0, scheduler_delay_factor=0.0, preemption_mode=None, num_scheduler_steps=1, multi_step_stream_outputs=True, scheduling_policy='fcfs', enable_chunked_prefill=None, disable_chunked_mm_input=False, scheduler_cls='vllm.core.scheduler.Scheduler', compilation_config=None, kv_transfer_config=None, kv_events_config=None, additional_config=None, use_v2_block_manager=True, disable_log_stats=False, disable_log_requests=False, max_log_len=None, disable_fastapi_docs=False, enable_prompt_tokens_details=False, enable_server_load_tracking=False, dispatch_function=<function ServeSubcommand.cmd at 0x74229577a3e0>)
INFO 06-10 07:31:56 [config.py:753] This model supports multiple tasks: {'classify', 'reward', 'generate', 'score', 'embed'}. Defaulting to 'generate'.
INFO 06-10 07:31:56 [arg_utils.py:1561] rocm is experimental on VLLM_USE_V1=1. Falling back to V0 Engine.
WARNING 06-10 07:31:56 [arg_utils.py:1402] The model has a long context length (40960). This may causeOOM during the initial memory profiling phase, or result in low performance due to small KV cache size. Consider setting --max-model-len to a smaller value.
INFO 06-10 07:31:56 [config.py:1861] Disabled the custom all-reduce kernel because it is not supported on current platform.
INFO 06-10 07:31:56 [config.py:1832] Disabled the custom all-reduce kernel because it is not working correctly when using two AMD Navi GPUs.
INFO 06-10 07:31:56 [api_server.py:246] Started engine process with PID 165
INFO 06-10 07:31:58 [__init__.py:239] Automatically detected platform rocm.
INFO 06-10 07:32:06 [llm_engine.py:240] Initializing a V0 LLM engine (v0.7.4.dev1638+ga7ddaa9b9) with config: model='/models/Qwen3-1.7B', speculative_config=None, tokenizer='/models/Qwen3-1.7B', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, override_neuron_config={}, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=40960, download_dir=None, load_format=LoadFormat.AUTO, tensor_parallel_size=1, pipeline_parallel_size=1, disable_custom_all_reduce=True, quantization=None, enforce_eager=False, kv_cache_dtype=auto,  device_config=cuda, decoding_config=DecodingConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_backend=''), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None), seed=None, served_model_name=/models/Qwen3-1.7B, num_scheduler_steps=1, multi_step_stream_outputs=True, enable_prefix_caching=None, chunked_prefill_enabled=False, use_async_output_proc=True, pooler_config=None, compilation_config={"splitting_ops":[],"compile_sizes":[],"cudagraph_capture_sizes":[256,248,240,232,224,216,208,200,192,184,176,168,160,152,144,136,128,120,112,104,96,88,80,72,64,56,48,40,32,24,16,8,4,2,1],"max_capture_size":256}, use_cached_outputs=True, 
INFO 06-10 07:32:06 [rocm.py:211] None is not supported in AMD GPUs.
INFO 06-10 07:32:06 [rocm.py:212] Using ROCmFlashAttention backend.
INFO 06-10 07:32:06 [parallel_state.py:1004] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, TP rank 0
INFO 06-10 07:32:06 [model_runner.py:1161] Starting to load model /models/Qwen3-1.7B...
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torch/utils/_device.py:104: UserWarning: Ignoring invalid value for boolean flag AMD_SERIALIZE_KERNEL: 3valid values are 0 or 1. (Triggered internally at /app/pytorch/c10/util/env.cpp:86.)
  return func(*args, **kwargs)
ERROR 06-10 07:32:06 [engine.py:448] HIP error: invalid device function
ERROR 06-10 07:32:06 [engine.py:448] HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
ERROR 06-10 07:32:06 [engine.py:448] For debugging consider passing AMD_SERIALIZE_KERNEL=3
ERROR 06-10 07:32:06 [engine.py:448] Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
ERROR 06-10 07:32:06 [engine.py:448] Traceback (most recent call last):
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/engine/multiprocessing/engine.py", line 436, in run_mp_engine
ERROR 06-10 07:32:06 [engine.py:448]     engine = MQLLMEngine.from_vllm_config(
ERROR 06-10 07:32:06 [engine.py:448]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/engine/multiprocessing/engine.py", line 128, in from_vllm_config
ERROR 06-10 07:32:06 [engine.py:448]     return cls(
ERROR 06-10 07:32:06 [engine.py:448]            ^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/engine/multiprocessing/engine.py", line 82, in __init__
ERROR 06-10 07:32:06 [engine.py:448]     self.engine = LLMEngine(*args, **kwargs)
ERROR 06-10 07:32:06 [engine.py:448]                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/engine/llm_engine.py", line 275, in __init__
ERROR 06-10 07:32:06 [engine.py:448]     self.model_executor = executor_class(vllm_config=vllm_config)
ERROR 06-10 07:32:06 [engine.py:448]                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/executor/executor_base.py", line 52, in __init__
ERROR 06-10 07:32:06 [engine.py:448]     self._init_executor()
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/executor/uniproc_executor.py", line 47, in _init_executor
ERROR 06-10 07:32:06 [engine.py:448]     self.collective_rpc("load_model")
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/executor/uniproc_executor.py", line 56, in collective_rpc
ERROR 06-10 07:32:06 [engine.py:448]     answer = run_method(self.driver_worker, method, args, kwargs)
ERROR 06-10 07:32:06 [engine.py:448]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/utils.py", line 2645, in run_method
ERROR 06-10 07:32:06 [engine.py:448]     return func(*args, **kwargs)
ERROR 06-10 07:32:06 [engine.py:448]            ^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/worker/worker.py", line 231, in load_model
ERROR 06-10 07:32:06 [engine.py:448]     self.model_runner.load_model()
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/worker/model_runner.py", line 1164, in load_model
ERROR 06-10 07:32:06 [engine.py:448]     self.model = get_model(vllm_config=self.vllm_config)
ERROR 06-10 07:32:06 [engine.py:448]                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/model_loader/__init__.py", line 14, in get_model
ERROR 06-10 07:32:06 [engine.py:448]     return loader.load_model(vllm_config=vllm_config)
ERROR 06-10 07:32:06 [engine.py:448]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/model_loader/loader.py", line 453, in load_model
ERROR 06-10 07:32:06 [engine.py:448]     model = _initialize_model(vllm_config=vllm_config)
ERROR 06-10 07:32:06 [engine.py:448]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/model_loader/loader.py", line 133, in _initialize_model
ERROR 06-10 07:32:06 [engine.py:448]     return model_class(vllm_config=vllm_config, prefix=prefix)
ERROR 06-10 07:32:06 [engine.py:448]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen3.py", line 269, in __init__
ERROR 06-10 07:32:06 [engine.py:448]     self.model = Qwen3Model(vllm_config=vllm_config,
ERROR 06-10 07:32:06 [engine.py:448]                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/compilation/decorators.py", line 151, in __init__
ERROR 06-10 07:32:06 [engine.py:448]     old_init(self, vllm_config=vllm_config, prefix=prefix, **kwargs)
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen3.py", line 241, in __init__
ERROR 06-10 07:32:06 [engine.py:448]     super().__init__(vllm_config=vllm_config,
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/compilation/decorators.py", line 151, in __init__
ERROR 06-10 07:32:06 [engine.py:448]     old_init(self, vllm_config=vllm_config, prefix=prefix, **kwargs)
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen2.py", line 305, in __init__
ERROR 06-10 07:32:06 [engine.py:448]     self.start_layer, self.end_layer, self.layers = make_layers(
ERROR 06-10 07:32:06 [engine.py:448]                                                     ^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/utils.py", line 610, in make_layers
ERROR 06-10 07:32:06 [engine.py:448]     maybe_offload_to_cpu(layer_fn(prefix=f"{prefix}.{idx}"))
ERROR 06-10 07:32:06 [engine.py:448]                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen2.py", line 307, in <lambda>
ERROR 06-10 07:32:06 [engine.py:448]     lambda prefix: decoder_layer_type(config=config,
ERROR 06-10 07:32:06 [engine.py:448]                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen3.py", line 172, in __init__
ERROR 06-10 07:32:06 [engine.py:448]     self.self_attn = Qwen3Attention(
ERROR 06-10 07:32:06 [engine.py:448]                      ^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen3.py", line 108, in __init__
ERROR 06-10 07:32:06 [engine.py:448]     self.rotary_emb = get_rope(
ERROR 06-10 07:32:06 [engine.py:448]                       ^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/layers/rotary_embedding.py", line 1502, in get_rope
ERROR 06-10 07:32:06 [engine.py:448]     rotary_emb = RotaryEmbedding(head_size, rotary_dim, max_position, base,
ERROR 06-10 07:32:06 [engine.py:448]                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/layers/rotary_embedding.py", line 111, in __init__
ERROR 06-10 07:32:06 [engine.py:448]     cache = self._compute_cos_sin_cache()
ERROR 06-10 07:32:06 [engine.py:448]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/layers/rotary_embedding.py", line 128, in _compute_cos_sin_cache
ERROR 06-10 07:32:06 [engine.py:448]     inv_freq = self._compute_inv_freq(self.base)
ERROR 06-10 07:32:06 [engine.py:448]                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/layers/rotary_embedding.py", line 122, in _compute_inv_freq
ERROR 06-10 07:32:06 [engine.py:448]     inv_freq = 1.0 / (base**(torch.arange(
ERROR 06-10 07:32:06 [engine.py:448]                              ^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448]   File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torch/utils/_device.py", line 104, in __torch_function__
ERROR 06-10 07:32:06 [engine.py:448]     return func(*args, **kwargs)
ERROR 06-10 07:32:06 [engine.py:448]            ^^^^^^^^^^^^^^^^^^^^^
ERROR 06-10 07:32:06 [engine.py:448] RuntimeError: HIP error: invalid device function
ERROR 06-10 07:32:06 [engine.py:448] HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
ERROR 06-10 07:32:06 [engine.py:448] For debugging consider passing AMD_SERIALIZE_KERNEL=3
ERROR 06-10 07:32:06 [engine.py:448] Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
ERROR 06-10 07:32:06 [engine.py:448] 
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/opt/conda/envs/py_3.12/lib/python3.12/multiprocessing/process.py", line 314, in _bootstrap
    self.run()
  File "/opt/conda/envs/py_3.12/lib/python3.12/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/engine/multiprocessing/engine.py", line 450, in run_mp_engine
    raise e
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/engine/multiprocessing/engine.py", line 436, in run_mp_engine
    engine = MQLLMEngine.from_vllm_config(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/engine/multiprocessing/engine.py", line 128, in from_vllm_config
    return cls(
           ^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/engine/multiprocessing/engine.py", line 82, in __init__
    self.engine = LLMEngine(*args, **kwargs)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/engine/llm_engine.py", line 275, in __init__
    self.model_executor = executor_class(vllm_config=vllm_config)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/executor/executor_base.py", line 52, in __init__
    self._init_executor()
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/executor/uniproc_executor.py", line 47, in _init_executor
    self.collective_rpc("load_model")
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/executor/uniproc_executor.py", line 56, in collective_rpc
    answer = run_method(self.driver_worker, method, args, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/utils.py", line 2645, in run_method
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/worker/worker.py", line 231, in load_model
    self.model_runner.load_model()
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/worker/model_runner.py", line 1164, in load_model
    self.model = get_model(vllm_config=self.vllm_config)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/model_loader/__init__.py", line 14, in get_model
    return loader.load_model(vllm_config=vllm_config)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/model_loader/loader.py", line 453, in load_model
    model = _initialize_model(vllm_config=vllm_config)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/model_loader/loader.py", line 133, in _initialize_model
    return model_class(vllm_config=vllm_config, prefix=prefix)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen3.py", line 269, in __init__
    self.model = Qwen3Model(vllm_config=vllm_config,
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/compilation/decorators.py", line 151, in __init__
    old_init(self, vllm_config=vllm_config, prefix=prefix, **kwargs)
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen3.py", line 241, in __init__
    super().__init__(vllm_config=vllm_config,
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/compilation/decorators.py", line 151, in __init__
    old_init(self, vllm_config=vllm_config, prefix=prefix, **kwargs)
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen2.py", line 305, in __init__
    self.start_layer, self.end_layer, self.layers = make_layers(
                                                    ^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/utils.py", line 610, in make_layers
    maybe_offload_to_cpu(layer_fn(prefix=f"{prefix}.{idx}"))
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen2.py", line 307, in <lambda>
    lambda prefix: decoder_layer_type(config=config,
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen3.py", line 172, in __init__
    self.self_attn = Qwen3Attention(
                     ^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/models/qwen3.py", line 108, in __init__
    self.rotary_emb = get_rope(
                      ^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/layers/rotary_embedding.py", line 1502, in get_rope
    rotary_emb = RotaryEmbedding(head_size, rotary_dim, max_position, base,
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/layers/rotary_embedding.py", line 111, in __init__
    cache = self._compute_cos_sin_cache()
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/layers/rotary_embedding.py", line 128, in _compute_cos_sin_cache
    inv_freq = self._compute_inv_freq(self.base)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/model_executor/layers/rotary_embedding.py", line 122, in _compute_inv_freq
    inv_freq = 1.0 / (base**(torch.arange(
                             ^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torch/utils/_device.py", line 104, in __torch_function__
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

[rank0]:[W610 07:32:07.050956870 ProcessGroupNCCL.cpp:1476] Warning: WARNING: destroy_process_group() was not called before program exit, which can leak resources. For more info, please see https://pytorch.org/docs/stable/distributed.html#shutdown (function operator())
Traceback (most recent call last):
  File "/opt/conda/envs/py_3.12/bin/vllm", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/entrypoints/cli/main.py", line 53, in main
    args.dispatch_function(args)
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/entrypoints/cli/serve.py", line 27, in cmd
    uvloop.run(run_server(args))
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/uvloop/__init__.py", line 109, in run
    return __asyncio.run(
           ^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/uvloop/__init__.py", line 61, in wrapper
    return await main
           ^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/entrypoints/openai/api_server.py", line 1077, in run_server
    async with build_async_engine_client(args) as engine_client:
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/entrypoints/openai/api_server.py", line 146, in build_async_engine_client
    async with build_async_engine_client_from_engine_args(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/vllm/entrypoints/openai/api_server.py", line 269, in build_async_engine_client_from_engine_args
    raise RuntimeError(
RuntimeError: Engine process failed to start. See stack trace for the root cause.
</code><pre>
</details>


Additionally, I tried adding AMD_SERIALIZE_KERNEL=3 to get more information (by executing `AMD_SERIALIZE_KERNEL=3 vllm serve /models/Qwen3-1.7B` inside the container). However, the error message remains the same as without the parameter. Could you please advise where this parameter should be placed?  

This is my first time using ROCm. If anything is unclear or if you need additional information from me, please let me know—I’m happy to provide it.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

<details>

<summary>rocminfo output</summary>

```
ROCk module version 6.12.12 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   5185                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65464680(0x3e6e968) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65464680(0x3e6e968) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65464680(0x3e6e968) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65464680(0x3e6e968) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1151                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
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
    L1:                      32(0x20) KB                        
    L2:                      2048(0x800) KB                     
    L3:                      16384(0x4000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   50432                              
  Internal Node ID:        1                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       APU
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
  Packet Processor uCode:: 26                                 
  SDMA engine uCode::      14                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67108864(0x4000000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67108864(0x4000000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1151         
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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
```

</details>

### Additional Information

_No response_

---

## 评论 (63 条)

### 评论 #1 — ppanchad-amd (2025-06-10T13:14:24Z)

Hi @FlintyLemming. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — waltercool (2025-06-11T05:34:45Z)

I don't think ROCm 6.4.1 supports Ryzen AI Max+ 395.

This is still in development at TheRock. https://github.com/ROCm/TheRock/discussions/655

---

### 评论 #3 — schung-amd (2025-06-11T14:36:17Z)

Generally `invalid device function` errors indicate that some code was not compiled for your architecture. We don't currently officially support gfx1151 (see compatibility matrix at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html), so I wouldn't be surprised if the docker images don't have a compatible build of ROCm, pytorch, and/or vLLM.

I haven't tried myself, but you may be able to get this to work by installing gfx1151-compatible components. TheRock provides ROCm release tarballs built for gfx1151, and the post linked by @waltercool links to some community-built pytorch wheels with gfx1151 compatibility. You may need to build vLLM from source as well. However, even if this works, we can't guarantee good performance.

Unfortunately at the moment I would not expect the docker images to work out of the box with gfx1151. Hopefully in the future we will have official support and this can be rectified. If you'd like further guidance I'll see if I can get my hands on a gfx1151 system to test this on.

---

### 评论 #4 — FlintyLemming (2025-06-12T08:07:47Z)

Thank you very much for your reply. It does seem to be the case—even when I run a simple PyTorch script using the ROCm PyTorch image(`rocm/pytorch:rocm6.4.1_ubuntu24.04_py3.12_pytorch_release_2.6.0`), it prompts "invalid device function," despite indicating that it found a ROCm device.  

```
--- PyTorch ROCm Verification ---
PyTorch ROCm support available: True
Found 1 ROCm device(s).
Device 0 Name: AMD Radeon Graphics

Attempting to perform a simple calculation on device 0...

An error occurred during GPU operation: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

--- Verification Failed during calculation. ---
```

What I’m particularly curious about now is whether there’s a timeline for ROCm support for this GPU, since I saw at Computex 2025 that AMD mentioned they would adapt ROCm for this GPU. I’m wondering whether I should wait for the official update or refer to community suggestions and compile it myself for now.

![](https://github.com/user-attachments/assets/f3411ec2-1c7f-48ff-a9c7-fd33ff4a4ce0)


---

### 评论 #5 — ion599 (2025-06-17T17:58:21Z)

You guys advertise this as a supported product. It's really upsetting to find out that it isn't actually supported. What kind of time line are we looking to support the gfx1151, or should I return the hardware I bought and go to Nvidia? 

---

### 评论 #6 — waltercool (2025-06-17T18:40:55Z)

> You guys advertise this as a supported product. It's really upsetting to find out that it isn't actually supported. What kind of time line are we looking to support the gfx1151, or should I return the hardware I bought and go to Nvidia?

Calm down my friend, while I agree with you on that, they are working hard to get this available by next big release.

Sadly, their priorities are always business and high-end GPUs, not APU.

They already have a "working" ROCm for gfx1151 for Linux and **currently improving performance**. For Windows, it's already supported using [DirectML](https://learn.microsoft.com/en-us/windows/ai/directml/pytorch-windows), or [ROCm](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html#windows-supported-gpus-and-apus)

Also, pytorch.org provides wheel binaries using created by Torch team, not ROCm. You can always build Torch, Torchvision and Torchaudio by yourself using [TheRock](https://github.com/ROCm/TheRock/pkgs/container/therock_pytorch_dev_ubuntu_24_04_gfx1151) .

---

### 评论 #7 — schung-amd (2025-06-17T19:07:37Z)

We have official support for gfx1151 on Windows (see: https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html) but not Linux at this time. Unfortunately this does not include pytorch support at the moment as we don't have pytorch support in native Windows yet in the first place. Pytorch support for native Windows was announced for Q3 (as a preview), but I'm not 100% sure if that implies it will be ready for gfx1151 as well. I'll see if I can get any more info to provide regarding this.

For now, the community is doing excellent work building pytorch wheels, and I encourage trying the community wheels out (or following their process to build your own) in the interim.

---

### 评论 #8 — ion599 (2025-06-17T21:13:01Z)

I'm not asking for the world here. I want clear support documentation. If gfx1151 is not supported, the table on the website should have it as unsupported and with a release timeline for each platform and major ML library. I don't want to spend 10 hours building various libraries downloading 10s of GB of docker images to find out that the gfx1151 isn't supported by any mainline instructions. I need to go Github to find this issue to find out that none of that documentation is going to work. I need to pull some other repo and build that instead. On top of that I need to now chase down any configuration issues to get that build to work. In a few weeks, I might need to do it all again if I want to use a newer model. 

This processor was launched in January. I'm ok that it didn't have day 1 support, but if AMD is going to let their system integrators (and AMD) advertise it as an [AI chip](https://www.amd.com/en/developer/resources/technical-articles/2025/amd-ryzen-ai-max-395--a-leap-forward-in-generative-ai-performanc.html), it should have tier 1 support by the company. If the dev team is too small, then I hope this comment lets them hire more. I don't think treating AMD with the level of patience everyone is giving them is helping them build better products. 

I would go as far to say that the Macs are much better AI workstations than the gfx1151 in that they support all the major AI libraries (or the reverse is true). The extra memory support is totally useless if I can't do development. Maybe you can forward this to the product manager, and get them to stop writing the puff pieces on the performance of this chip if documentation and support isn't there. I would rather have a M4 macstudio than this AMD machine. 

---

### 评论 #9 — schung-amd (2025-06-17T21:46:37Z)

Not to detract from your concerns, but we don't state mainline support for gfx1151 on Linux (see https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/native_linux/native_linux_compatibility.html) which implies that we don't support it. gfx1151 is only present in the Windows compatibility matrix, where it is supported (but without pytorch).

---

### 评论 #10 — waltercool (2025-06-17T21:46:43Z)

Macbooks come with MacOS, and support is there for MacOS only.

Your computer likely comes with Microsoft Windows, and they provide full support for Microsoft Windows. I don't understand your problem here mate.

I'm a Linux purist, and I do understand your concern here, but you must understand your computer (HP Zbook Ultra, Flow Z13 or Evo X2 AI Mini) does not support Linux **by default**, neither AMD.

In good news, started to change this policy early this year and put more resources and support for their ROCm platform. You can see a large thread here: https://github.com/ROCm/ROCm/discussions/4276 .

If you can't wait, I strongly recommend you to use Windows, or the community effort for now. Scottt have [pytorch for Linux](https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch) and works fine, he does not have provided a build for torchvision (needed for Image AI) or torchaudio (needed for Audio AI) except for Windows.

---

### 评论 #11 — ion599 (2025-06-17T22:17:16Z)

I know you are trying to help, but I read this document around framework support:
https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/component-support.html
Windows looks like a second class citizen for ROCm. I don't know what to go off of. My frustration is with the documentation telling me 2 different things and it's bleed out into the other aspects of the product.

This chart shows that ROCm supports pytorch for Linux only. I spent a ton of time trying to get the instructions on the website to work. I don't even want someone to fix the support. I just want someone to fix the documentation. 

I initially started from the default Windows install and then tried to get the WSL Linux version to work. Then gave up and tried a bare metal install and then the docker version. I don't even like Macs, but from a pragmatic perspective they have documentation that is consistent. I know whether or not the device I bought is going to run the framework I want to use. I don't want someone else to have this super frustrating experience. I'm going to give the community effort a shot, but the product feedback is the documentation is really bad. Please fix it

---

### 评论 #12 — waltercool (2025-06-17T22:27:27Z)

FYI if you need Torch + Vision + Audio on Windows, I would recommend you downloading from the link mentioned [before](https://github.com/scottt/rocm-TheRock/releases/tag/v6.5.0rc-pytorch) for now. They have:
- Torch (Windows py311/py312 + Linux py311)
- Torch Vision (Windows py311/py312)
- Torch Audio ( Windows py311/py312)

It's not like ROCM does not support Torch officially, but Torch does not support ROCM officially on Windows yet.

ROCM on Windows have been live for few months only: https://windowsforum.com/threads/amd-rocm-software-support-expands-for-windows-users-what-you-need-to-know.355138/

---

### 评论 #13 — rikimeow (2025-07-04T04:00:09Z)

Maybe you can try setting the environment variable **`export HSA_OVERRIDE_GFX_VERSION=11.0.0`** to simulate gfx1151 as gfx1100 to deceive the program.these two architectures are similar.

I have already used this method to run some LLM programs on the pytorch nightly version, such as MinerU for PDF recognition.
[<https://github.com/opendatalab/MinerU/discussions/2738>]

I am also testing the functionality compatibility and performance of gfx1151.

---

### 评论 #14 — waltercool (2025-07-04T04:05:06Z)

That works for some stuff, not everything. You can definitively do that for Flux.1 dev, but not for their variants, amdgpu crashes and restarts itself.

Using 11.0.0 gives you better performance than 11.5.1 at least using Flux.1. At least double performance according to some tests made by myself.

Also:

https://github.com/ROCm/ROCm/issues/4748

---

### 评论 #15 — rikimeow (2025-07-04T04:23:59Z)

Haha, actually, the method I mentioned just now came from your message #4748. I also tested with a PyTorch Docker container compiled by ROCm/therock for gfx1151, and it worked. But after all, it's a non-standard approach, so there will be some problems.&nbsp;


Thank you for the reminder.



发自我的iPhone


------------------ Original ------------------
From: WalterCool ***@***.***&gt;
Date: Fri,Jul 4,2025 0:05 PM
To: ROCm/ROCm ***@***.***&gt;
Cc: rikimeow ***@***.***&gt;, Manual ***@***.***&gt;
Subject: Re: [ROCm/ROCm] [Issue]: Unable to Run vLLM Inference on AMD Ryzen AIMAX+ 395 (Issue #4909)



waltercool left a comment (ROCm/ROCm#4909)
 
That works for some stuff, not everything. You can definitively do that for Flux.1 dev, but not for their variants, amdgpu crashes and restarts itself.
 
Using 11.0.0 gives you better performance than 11.5.1 at least using Flux.1. At least double performance according to some tests made by myself.
 
Also:
 
#4748
 
—
Reply to this email directly, view it on GitHub, or unsubscribe.
You are receiving this because you are subscribed to this thread.Message ID: ***@***.***&gt;

---

### 评论 #16 — nameqq2 (2025-08-29T09:30:01Z)

hello,我看到amd官方现在推广rocm7了，但是好像还没看到官方发行的稳定版本，不过有看到预览版本的：https://github.com/ROCm/TheRock/blob/main/RELEASES.md 不过我在跑deepseek vl 模型的官方推理测试代码的时候也出现缺少东西的报错，不知道稳定版什么时候会出。。。


---

### 评论 #17 — waltercool (2025-08-29T14:35:20Z)

Hi @nameqq2 ,

You can use text output LLM models with LM Studio without much hassle at Windows or Linux. Just make sure to use the Vulkan backend.

For Torch models, it works using DirectML I think. ROCm backend have have some WIP stuff and hopefully is ready by next big release.

You can still use ROCm at Windows or Linux using TheRock packages, but I wouldn't fully recommend it now because pending items will give you bad experience overall, like speed or memory optimization.

---

### 评论 #18 — mveigel-softkomplett (2025-09-08T14:56:42Z)

@schung-amd 
Hello, just to be sure to understand you right ... (and please keep in mind i'm not a native english speaker)

- There will be no linux Support for the AI-MAX+ 395 from AMD
- There will be no linux support for ROCM on AI-MAX+ 395 from AMD
- There will be no linux support for pytorch, torchvision and torchaudio for AI-MAX+ 395

Is this correct?

I understand the focus on the expensive cards from a purely economic view. What I don't really understand is the lack of Linux support for the products (we have 2025 not 1985, and Linux is - preferably - used in many environments especially for AI).

I spend a few days now in testing the HP Z2 with 128 GB for AI. I'm using AMD cards now for decades and accepted several (normaly) no-go's (crappy and unusable/untested drivers for RHEL, problems with suspend to ram/disk etc.), but I liked the AMD hardware and find it great to have a counterpart to NVIDIA available.

I build pytorch containers with ROCM 6.4.3, currently building another with ROCM 7.0.0rc1and lvvm instead of ollama (and I'm quite sure it will work, because ollama already works (more or less) on my Z2 with Ubuntu 24.04.3 and Kernel 6.12.12 (nativly supporting the AI Max+). More or less in this context means, I could get an answer, but at all it is unusable.

The only really big issue is the amdgpu driver, which ends (most of the time) in a GPU reset with the well known "GCVM_L2_PROTECTION_FAULT_STATUS" followed by "MES failed to respond to msg=SUSPEND". This makes it impossible to work with it for AI. I found a patch somewhere in the internet (unfortunately I'm currently seeking this in one of the few hundred webpages I had to search, where it is.). First i wouldn't apply this, because I have to patch the AMDGPU driver, but it seems to be possible at least.

With your message (or better: The AMD paper in mind) I think it is best to return my Z2 and buy NVIDIA Hardware. Because Windows is an absolutely no go for me (working only with Linux since 1982) and had to much negative points in using windows (my personal decission ;)). Am I correct with the interpretation of the Roadmap? I'm currently struggling with this decission, because I like the amount of RAM and the speed I had with gpt-oss:120b (and of course with the answers I get from the model in the rare cases it works).

Long speak short :): If the manufacter does not support it's product with software it's just an expensive (and useless) pice of silicon - no matter how much cheaper it is compared to the other manufacter :(.

So AMD is not planing to support it, simply don't buy it. Then it should be like that and I switch over to NVIDIA, where I get Linux Support and a working environment. Sad but true ... but can you please tell your Marketing to point out, that your GPUs are only for Windows and don't work reliably on Linux (No official AMD support)? Because this would have saved me (and many others which hoped to get a payable Workstation with the AI Max+ 395 for AI) days of senseless work.

My personal opinion:
Nowadays the things comes from bottom up (if you don't have the consumer masses behind you, you will not get enough experts to sell your Hardware in Companies, because they only know how it works for NVIDIA, but not for AMD -  so they will buy NVIDIA Products). AMD could ignore this of course - i personally think, this is not the best management decission.


---

### 评论 #19 — nameqq2 (2025-09-08T15:08:07Z)

> Hi [@nameqq2](https://github.com/nameqq2) , 你好,
> 
> You can use text output LLM models with LM Studio without much hassle at Windows or Linux. Just make sure to use the Vulkan backend.您可以在Windows或Linux上使用LM Studio使用文本输出LLM模型，而不会有太多麻烦。只要确保使用Vulkan后端即可。
> 
> For Torch models, it works using DirectML I think. ROCm backend have have some WIP stuff and hopefully is ready by next big release.对于Torch模型，我认为它可以使用DirectML。ROCm后端已经有了一些WIP的东西，希望在下一个大版本中准备好。
> 
> You can still use ROCm at Windows or Linux using TheRock packages, but I wouldn't fully recommend it now because pending items will give you bad experience overall, like speed or memory optimization.您仍然可以在Windows或Linux上使用TheRock软件包使用ROCm，但我现在不完全推荐它，因为悬而未决的项目会给您带来糟糕的体验，比如速度或内存优化。

感谢回复。是的，我现在用的是LMstudio，但是上面的模型都是GGUF的格式，并且模型选择较少，希望官方能加快ROCM7正式版的进度。您建议我用的directml我也试过了，是一个可行的方案但是不太好用，在项目里面又会出现意料之外的BUG。

---

### 评论 #20 — waltercool (2025-09-08T15:10:38Z)

@mveigel-softkomplett 
> Is this correct?

No, that's not what schung-amd said.

AMD does not offer currently any support for the AI Max 395 at ROCm on Linux because the current version (6.4.3) does not support the chipset.

Linux support on the current stack: https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html

AI Max 395 will be supported (likely) at ROCm 7.0.0, but not sure yet. They have some builds right now at [TheRock](http://github.com/ROCm/TheRock/) supporting the 1151 chipset, and they work mostly fine except for some issues.

ROCm 7.X have lot of changes from 6.X, and that breaks the PyTorch implementation, and that's something they are also working too.

> I build pytorch containers with ROCM 6.4.3, currently building another with ROCM 7.0.0rc1and lvvm instead of ollama (and I'm quite sure it will work, because ollama already works (more or less) on my Z2 with Ubuntu 24.04.3 and Kernel 6.12.12 (nativly supporting the AI Max+). More or less in this context means, I could get an answer, but at all it is unusable.

You don't have to. There are two options right now:
1) Wait until they get a mature release, so you have a good experience
2) Install the Pytorch wheels from TheRock. They work mostly fine using Torch 2.9RC +ROCM7.0.0RC.

By going for the second option, everything works to me, even video generation. The [current issue](https://github.com/ROCm/TheRock/issues/1364) is being fixed currently, related to new aotriton implementation. Without this, ROCm takes excessive amount of VRAM. 

If you are expecting this for professional use, I would recommend you to wait, or use Vulkan backend with LMStudio for text generation. For personal use, if you want to play around with experimental builds, then you can use TheRock builds.

---

### 评论 #21 — mveigel-softkomplett (2025-09-08T15:43:49Z)

@waltercool 
AI Max 395 will be supported (likely) at ROCm 7.0.0, but not sure yet. They have some builds right now at [TheRock](https://github.com/ROCm/TheRock/) supporting the 1151 chipset, and they work mostly fine except for some issues.

It is nativly supported with ROCm 7.0.0rc1 I already tested it, but it seems the that the problem is not ROCm, it's the AMDGPU driver. i tested the public available drivers - ROCM works, when you set the HSA_OVERRIDE_GFX_VERSION=11.0.0 like mentioned above and also the new driver in ROCm 7.0.0rc1, where it works out of the box. With both drivers I had these Problems. I also installed the newest Firmware, and it get's better, but not good at all.

There is also no AMDGPU driver to Download for Linux, which indicates, that AMD will not support it later.

You don't have to. There are two options right now:

    Wait until they get a mature release, so you have a good experience
    Install the Pytorch wheels from TheRock. They work mostly fine using Torch 2.9RC +ROCM7.0.0RC

The first is not really an option, I will not spend several thousands of Euro to buy hardware where i *might* get manufactor support somehow in the future. I'm not really a friend of NVIDIA, but they manage to have drivers available, when the sell the hardware (for Linux and Windows). With AMD I had a different exprience (unfortunatelly) and it tooks years to ge a working (mostly stable) Linux driver. So I will not count on this.

Where do you get the pytorch wheels with ROCM7.0.0rc? I only find the windows container with ROCM7.0.0alpha. It looks like you have some experience, did you manage to run ollama with an AI MAX+ 395? Are you on Windows or Linux?

---

### 评论 #22 — schung-amd (2025-09-08T15:47:54Z)

@mveigel-softkomplett We have a commitment to support for the AI Max+ 395 (as shown by the Computex slide), but I can't share any info on timelines for this. Hopefully this is a communication process we can improve on in the future, but for now all I can say is that we have support planned and we're working on it.

> Where do you get the pytorch wheels with ROCM7.0.0rc?

Nightly builds for Strix Halo can be found [here](https://rocm.nightlies.amd.com/v2/gfx1151/).

---

### 评论 #23 — mveigel-softkomplett (2025-09-08T16:05:42Z)

@schung-amd 
Ok, so it looks like I missunderstood your posting. Can I test the lvvm with these wheels, to check if the AMDGPU problem is a ollama problem instead. The model runs fine on CPU, so i don't think it's ollama, which causes the segmentation fault. Can you provide some information on this? I'll give it a try today.

Thanks for the fast response and the links, maybe you can share them on the AMD website, because there I only had problems to find them ...

---

### 评论 #24 — schung-amd (2025-09-08T16:27:12Z)

> to check if the AMDGPU problem is a ollama problem instead

I'm not sure about the problem you're seeing as I haven't tried native Linux on Strix Halo myself yet; however I'm in the process of setting this up to triage another issue so I'll let you know if I see anything similar. I suggest trying TheRock (see simple installation instructions [here](https://github.com/ROCm/TheRock/blob/main/RELEASES.md), can also be built from source if desired) instead of the mainline ROCm releases if you're not already, even if 7.0.0rc1 has some Strix Halo support I'm not sure if it's fully enabled.

> Thanks for the fast response and the links, maybe you can share them on the AMD website, because there I only had problems to find them ...

Sorry about that, there's a bit of fragmentation at the moment; the main ROCm docs pertain to the mainline ROCm releases and these wheels are part of the TheRock project which is building ROCm 7. I think these wheels should work on the mainline ROCm releases once ROCm 7 releases, so at that point we could probably add a note in the main ROCm docs pointing to them. I haven't tested the wheels on ROCm 6.4.x, so if they work there feel free to correct me and I can see if we can make that docs update.

The documentation for these wheels can be found [here](https://github.com/ROCm/TheRock/blob/main/RELEASES.md). Note that there's a known issue at the moment with the `pip install` commands listed there as they will pull in incompatible `torch` and `torchaudio` wheels by default; add `--pre` for torch 2.9.0a0 or specify `torchaudio==2.7.1a0` if you want torch 2.7.1 instead.

---

### 评论 #25 — mveigel-softkomplett (2025-09-08T22:45:51Z)

@schung-amd 


I tried to build and install lvvm, here's my experience :):

- rocm/pytorch installation was easy going, great work (although didn't try to compile something, but looks all good)
- ck flash attention does not support Strix Halo. Is there some support planned, because the principle looks nice
- intalling triton / flash attention:
  - triton loads VERY slow from the cloud :(, would be nice to download it in the webbrowser and specify the file, because when the compile fails for some reason (like here ;)), you have to wait for ages until it is downloaded again ...
    - have a bunch of errors when compiling like on the website mentioned - no success 
  - flash-attention does not support gfx1151, will there be some support in the future? 
  - vllm:
    - installation of amd_smi works, if you change the owner or copy the contents of /opt/rocm/amd_smi to the working user
    - for me the installation text looks wrong:
      - you should install numpy<2 and then the requirements-rocm.txt
        - this is wrong for two reasons:
          - the requirements file (i asume) in the vllm source is rocm.txt, in the requirements directory not "requirements.rocm.txt"
          - when you install the requiremens, numpy is updated to version 2.2.6 and 1.26.4 is removed. This clashes with the previous instruction to install numpy<2
          - when i install numpy<2 again i get the following error:
            - `ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
opencv-python-headless 4.12.0.88 requires numpy<2.3.0,>=2; python_version >= "3.9", but you have numpy 1.26.4 which is incompatible.`
          - when i try to update numpy again, i get
            - `Requirement already satisfied: numpy in /home/mvlsd/vllm_rocm/the-rock/lib/python3.12/site-packages (1.26.4)`
          - when i try to install vllm from git (there is no other location mentioned in the readme):
            - I have to specify the additional variable VLLM_TARGET_DEVICE="rocm" when i start the compile


``` 
VLLM_TARGET_DEVICE="rocm" PYTORCH_ROCM_ARCH="gfx1151" python setup.py develop
/home/mvlsd/vllm_rocm/the-rock/lib/python3.12/site-packages/setuptools_scm/_integration/version_inference.py:51: UserWarning: version of None already set
  warnings.warn(self.message)
running develop
/home/mvlsd/vllm_rocm/the-rock/lib/python3.12/site-packages/setuptools/command/develop.py:41: EasyInstallDeprecationWarning: easy_install command is deprecated.
!!

        ********************************************************************************
        Please avoid running ``setup.py`` and ``easy_install``.
        Instead, use pypa/build, pypa/installer or other
        standards-based tools.

        See https://github.com/pypa/setuptools/issues/917 for details.
        ********************************************************************************

!!
  easy_install.initialize_options(self)
/home/mvlsd/vllm_rocm/the-rock/lib/python3.12/site-packages/setuptools/_distutils/cmd.py:90: SetuptoolsDeprecationWarning: setup.py install is deprecated.
!!

        ********************************************************************************
        Please avoid running ``setup.py`` directly.
        Instead, use pypa/build, pypa/installer or other
        standards-based tools.

        See https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html for details.
        ********************************************************************************

!!
  self.initialize_options()
running egg_info
writing vllm.egg-info/PKG-INFO
writing dependency_links to vllm.egg-info/dependency_links.txt
writing entry points to vllm.egg-info/entry_points.txt
writing requirements to vllm.egg-info/requires.txt
writing top-level names to vllm.egg-info/top_level.txt
reading manifest template 'MANIFEST.in'
adding license file 'LICENSE'
writing manifest file 'vllm.egg-info/SOURCES.txt'
running build_ext
-- Build type: RelWithDebInfo
-- Target device: rocm
-- Found python matching: /home/mvlsd/vllm_rocm/the-rock/bin/python.
CMake Error at cmake/utils.cmake:37 (message):
  Failed to locate torch path: double free or corruption (!prev)

  :import torch; print(torch.utils.cmake_prefix_path)
Call Stack (most recent call first):
  cmake/utils.cmake:45 (run_python)
  CMakeLists.txt:66 (append_cmake_prefix_path)


-- Configuring incomplete, errors occurred!
Traceback (most recent call last):
...
subprocess.CalledProcessError: Command '['cmake', '/home/mvlsd/vllm', '-G', 'Ninja', '-DCMAKE_BUILD_TYPE=RelWithDebInfo', '-DVLLM_TARGET_DEVICE=rocm', '-DVLLM_PYTHON_EXECUTABLE=/home/mvlsd/vllm_rocm/the-rock/bin/python', '-DVLLM_PYTHON_PATH=/home/mvlsd/vllm:/usr/lib/python312.zip:/usr/lib/python3.12:/usr/lib/python3.12/lib-dynload:/home/mvlsd/vllm_rocm/the-rock/lib/python3.12/site-packages:__editable__.triton-2.1.0.finder.__path_hook__:/home/mvlsd/vllm_rocm/the-rock/lib/python3.12/site-packages/setuptools/_vendor', '-DFETCHCONTENT_BASE_DIR=/home/mvlsd/vllm/.deps', '-DCMAKE_JOB_POOL_COMPILE:STRING=compile', '-DCMAKE_JOB_POOLS:STRING=compile=32']' returned non-zero exit status 1.
double free or corruption (!prev)
Aborted (core dumped)
```
The double free happens when I load torch in python e.g.:

```
python
Python 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> quit()
```
=> No error

```
python
Python 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch; print(torch.utils.cmake_prefix_path)
/home/mvlsd/vllm_rocm/the-rock/lib/python3.12/site-packages/torch/share/cmake
>>> quit()
double free or corruption (!prev)
Aborted (core dumped)
```
=> double free or corruption

But this could be, because I only gave it 32 MB of CPU memory. Have seen now oom messages during compile of something in the dmesg file. If you want, I can paste them. But there are a lot of them ;).

Enough for today ;). Just one hint about the Errors on the Halo Strix I mentioned, which makes everything useless ...

```
Sep 08 13:34:10 ai ollama[15414]: time=2025-09-08T13:34:10.079+02:00 level=INFO source=server.go:1288 msg="llama runner started in 12.11 seconds"
Sep 08 13:34:12 ai wpa_supplicant[1424]: wlp194s0: WPA: Group rekeying completed with 7c:ff:4d:f2:4d:a0 [GTK=CCMP]
Sep 08 13:34:12 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Sep 08 13:34:12 ai kernel: amdgpu 0000:c4:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1006
Sep 08 13:34:12 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Sep 08 13:34:12 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 3
Sep 08 13:34:12 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset begin!
Sep 08 13:34:12 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
Sep 08 13:34:12 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 0
Sep 08 13:34:12 ai ollama[15414]: HW Exception by GPU node-1 (Agent handle: 0x78aa98692910) reason :GPU Hang
Sep 08 13:34:12 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Dumping IP State
Sep 08 13:34:12 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Dumping IP State Completed
Sep 08 13:34:12 ai kernel: amdgpu: Freeing queue vital buffer 0x789959e00000, queue evicted
Sep 08 13:34:12 ai kernel: amdgpu: Freeing queue vital buffer 0x789963e00000, queue evicted
Sep 08 13:34:12 ai kernel: amdgpu: Freeing queue vital buffer 0x78a8d4400000, queue evicted
Sep 08 13:34:12 ai kernel: amdgpu: Freeing queue vital buffer 0x78a8d5e00000, queue evicted
Sep 08 13:34:12 ai kernel: amdgpu: Freeing queue vital buffer 0x78a8d6c00000, queue evicted
Sep 08 13:34:12 ai ollama[15414]: time=2025-09-08T13:34:12.737+02:00 level=ERROR source=server.go:1458 msg="post predict" error="Post \"http://127.0.0.1:43609/completion\": EOF"
Sep 08 13:34:12 ai ollama[15414]: [GIN] 2025/09/08 - 13:34:12 | 500 | 15.691771239s |      172.17.0.2 | POST     "/api/chat"
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MORE_FAULTS: 0x1
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          WALKER_ERROR: 0x1
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          PERMISSION_FAULTS: 0x5
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MAPPING_ERROR: 0x1
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          RW: 0x1
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Sep 08 13:34:13 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
Sep 08 13:34:15 ai kernel: [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MORE_FAULTS: 0x1
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          WALKER_ERROR: 0x1
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          PERMISSION_FAULTS: 0x5
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MAPPING_ERROR: 0x1
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          RW: 0x1
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MODE2 reset
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset succeeded, trying to resume
Sep 08 13:34:15 ai kernel: [drm] PCIE GART of 512M enabled (table at 0x00000097FFB00000).
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: SMU is resuming...
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: SMU is resumed successfully!
Sep 08 13:34:15 ai kernel: [drm] DMUB hardware initialized: version=0x09000F00
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
Sep 08 13:34:15 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset(9) succeeded!
```

The value of GCVM_L2_PROTECTION_FAULT_STATUS varies from time to time, the rest is almost the same ...

Again - Thanks for the links, they are quite useful :)




---

### 评论 #26 — schung-amd (2025-09-10T15:42:34Z)

> intalling triton / flash attention:

We intend to have aotriton in the torch wheels for gfx1151 (as far as I'm aware, at least), but currently our builds are broken due to some aotriton changes; see https://github.com/ROCm/TheRock/issues/1408. This should work eventually once that and other build issues are resolved.

> for me the installation text looks wrong

Good catch, I'll take a look at the installation instructions and make a PR upstream if necessary.

> GCVM_L2_PROTECTION_FAULT_STATUS

Usually indicates a kernel/driver issue, will have to try to repro. Do you have a minimal reproducer for this, and what kernel version are you on?

---

### 评论 #27 — mveigel-softkomplett (2025-09-10T23:00:40Z)

Regarding the GCVM_.... message:

It's easy to reproduce. Just run Ollama with gpt-oss:120b (96 GB Graphics memory). It might be, that one question succeeds (I tried e.g. "What can I eat today", followed by "What is the name of the first president of USA"), and (it looks like Ollama suspends the GPU, after the  Question) most of the time you get the error then. If not, ask another Question and you get it ;). It might be, that you see a "thinking" after the second question, but if you have look with "journalctl -xef" you see the question.

It does not depend on the size of the model. Even qwen3-coder:33b with only 19GB last only for 1 or 2 questions ...

SMI says (with gpt-oss:120b):
GPU  POWER   GPU_T   MEM_T   GFX_CLK   GFX%   MEM%   ENC%   DEC%      VRAM_USAGE
  0    N/A     N/A     N/A       N/A    N/A    N/A    N/A    N/A   60.9/ 96.0 GB

I tried it with some stock Ubuntu Kernels (low-latency, hwe) and the repositories with ROCm 6.4.3. Later on I tried it with the Kernel for 6.12.12, and the amdgpu driver I found in the ROCM 7.0.0rc1 repository.

Linux Firmware is the latest one (including the fixes for gfx1151), installed from the file:
linux-firmware_20240318.git3b128b60-0ubuntu2.17_amd64.deb

amd-smi firmware says:

```
GPU: 0
    FW_LIST:
        FW 0:
            FW_ID: CP_PFP
            FW_VERSION: 39
        FW 1:
            FW_ID: CP_ME
            FW_VERSION: 29
        FW 2:
            FW_ID: CP_MEC1
            FW_VERSION: 26
        FW 3:
            FW_ID: RLC
            FW_VERSION: 290653442
        FW 4:
            FW_ID: SDMA0
            FW_VERSION: 14
        FW 5:
            FW_ID: VCN
            FW_VERSION: 09.11.70.03
        FW 6:
            FW_ID: ASD
            FW_VERSION: 553648360
        FW 7:
            FW_ID: PM
            FW_VERSION: 00.100.110.00
```

This one was not easy to build and install, I just found a close match of the Kernel sources in the following files:

```
linux-headers-6.12.12-061212_6.12.12-061212.202502020514_all.deb
linux-image-unsigned-6.12.12-061212-generic_6.12.12-061212.202502020514_amd64.deb
linux-headers-6.12.12-061212-generic_6.12.12-061212.202502020514_amd64.deb
linux-modules-6.12.12-061212-generic_6.12.12-061212.202502020514_amd64.deb

Unfortunatelly I don't know exactly where I downloaded this Kernel, maybe you can get the correct one
(there is a patch missmatch between the kernel and the module. The module is: amdgpu-6.12.12-2187269.24.04 ).

Package of the driver is:
amdgpu_1:7.0.70000-2193521.24.04_amd64.deb
```

The errors happens with all Kernels and all Drivers - but didn't tried it with "the Rock", was using the AMD sources directly. Maybe I compiled something wrong (Ollama), but everything else works and sometimes, you can even anwser a few questions. After the Error you have to stop ollama completely, otherwise you just get these errors. After a reboot you have another question to ask ... Not the way AI should work ;).

I also tried to disable power management (i think sucessfully, but maybe I'm missing something). I added the following to the command line (the error happens with and without, but I think it happens less often, if you add the arguments to the kernel:

Additional settings:
amdgpu.ppfeaturemask=0xf7fff amdgpu.aspm=0 amdgpu.bapm=0 amdgpu.runpm=0 pcie_aspm=off amdgpu.mcbp=0

/proc/cmdline
BOOT_IMAGE=/vmlinuz-6.12.12-061212-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro amdgpu.ppfeaturemask=0xf7fff amdgpu.aspm=0 amdgpu.bapm=0 amdgpu.runpm=0 pcie_aspm=off amdgpu.mcbp=0

and after that, apply another the power managment setting:

echo "high" > /sys/class/drm/card1/device/power_dpm_force_performance_level

If you are interested and provide me a way, I can send you a dump of /opt/rocm, /var/log, binaries and sources (without the models ;) ) maybe you can fiddle out, what i did wrong.

These are the messages, when I started ollama with 64 GB (doesn't matter btw.) - sorry, that they are pretty long, but I wanted to include the full procedure:

```
Sep 11 00:42:09 ai ollama[3110]: time=2025-09-11T00:42:09.787+02:00 level=INFO source=routes.go:1331 msg="server config" env="map[CUDA_VISIBLE_DEVICES: GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_CONTEXT_LENGTH:4096 OLLAMA_DEBUG:INFO OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://0.0.0.0:11434 OLLAMA_INTEL_GPU:false OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:/usr/share/ollama/.ollama/models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NEW_ENGINE:false OLLAMA_NEW_ESTIMATES:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NUM_PARALLEL:1 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://* vscode-file://*] OLLAMA_SCHED_SPREAD:false ROCR_VISIBLE_DEVICES: http_proxy: https_proxy: no_proxy:]"
Sep 11 00:42:09 ai ollama[3110]: time=2025-09-11T00:42:09.789+02:00 level=INFO source=images.go:477 msg="total blobs: 10"
Sep 11 00:42:09 ai ollama[3110]: time=2025-09-11T00:42:09.789+02:00 level=INFO source=images.go:484 msg="total unused blobs removed: 0"
Sep 11 00:42:09 ai ollama[3110]: time=2025-09-11T00:42:09.790+02:00 level=INFO source=routes.go:1384 msg="Listening on [::]:11434 (version 0.11.10-0-g5994e8e)"
Sep 11 00:42:09 ai ollama[3110]: time=2025-09-11T00:42:09.791+02:00 level=INFO source=gpu.go:217 msg="looking for compatible GPUs"
Sep 11 00:42:09 ai ollama[3110]: time=2025-09-11T00:42:09.798+02:00 level=INFO source=amd_linux.go:390 msg="amdgpu is supported" gpu=0 gpu_type=gfx1151
Sep 11 00:42:09 ai ollama[3110]: time=2025-09-11T00:42:09.800+02:00 level=INFO source=types.go:131 msg="inference compute" id=0 library=rocm variant="" compute=gfx1151 driver=6.12 name=1002:1586 total="64.0 GiB" available="63.8 GiB"
Sep 11 00:42:16 ai ollama[3110]: [GIN] 2025/09/11 - 00:42:16 | 200 |      697.23µs |      172.17.0.2 | GET      "/api/tags"
Sep 11 00:42:16 ai ollama[3110]: [GIN] 2025/09/11 - 00:42:16 | 200 |     340.755µs |      172.17.0.2 | GET      "/api/ps"
Sep 11 00:42:49 ai ollama[3110]: time=2025-09-11T00:42:49.544+02:00 level=INFO source=server.go:199 msg="model wants flash attention"
Sep 11 00:42:49 ai ollama[3110]: time=2025-09-11T00:42:49.544+02:00 level=INFO source=server.go:216 msg="enabling flash attention"
Sep 11 00:42:49 ai ollama[3110]: time=2025-09-11T00:42:49.544+02:00 level=WARN source=server.go:224 msg="kv cache type not supported by model" type=""
Sep 11 00:42:49 ai ollama[3110]: time=2025-09-11T00:42:49.544+02:00 level=INFO source=server.go:398 msg="starting runner" cmd="/usr/local/bin/ollama runner --ollama-engine --model /usr/share/ollama/.ollama/models/blobs/sha256-90a618fe6ff21b09ca968df959104eb650658b0bef0faef785c18c2795d993e3 --port 43263"
Sep 11 00:42:49 ai ollama[3110]: time=2025-09-11T00:42:49.545+02:00 level=INFO source=server.go:503 msg="system memory" total="62.6 GiB" free="59.6 GiB" free_swap="8.0 GiB"
Sep 11 00:42:49 ai ollama[3110]: time=2025-09-11T00:42:49.545+02:00 level=INFO source=memory.go:36 msg="new model will fit in available VRAM across minimum required GPUs, loading" model=/usr/share/ollama/.ollama/models/blobs/sha256-90a618fe6ff21b09ca968df959104eb650658b0bef0faef785c18c2795d993e3 library=rocm parallel=1 required="62.4 GiB" gpus=1
Sep 11 00:42:49 ai ollama[3110]: time=2025-09-11T00:42:49.545+02:00 level=INFO source=server.go:543 msg=offload library=rocm layers.requested=-1 layers.model=37 layers.offload=37 layers.split=[37] memory.available="[63.8 GiB]" memory.gpu_overhead="0 B" memory.required.full="62.4 GiB" memory.required.partial="62.4 GiB" memory.required.kv="450.0 MiB" memory.required.allocations="[62.4 GiB]" memory.weights.total="59.7 GiB" memory.weights.repeating="58.6 GiB" memory.weights.nonrepeating="1.1 GiB" memory.graph.full="122.0 MiB" memory.graph.partial="122.0 MiB"
Sep 11 00:42:49 ai ollama[3110]: time=2025-09-11T00:42:49.552+02:00 level=INFO source=runner.go:1251 msg="starting ollama engine"
Sep 11 00:42:49 ai ollama[3110]: time=2025-09-11T00:42:49.553+02:00 level=INFO source=runner.go:1286 msg="Server listening on 127.0.0.1:43263"
Sep 11 00:42:49 ai ollama[3110]: time=2025-09-11T00:42:49.558+02:00 level=INFO source=runner.go:1170 msg=load request="{Operation:commit LoraPath:[] Parallel:1 BatchSize:512 FlashAttention:true KvSize:8192 KvCacheType: NumThreads:16 GPULayers:37[ID:0 Layers:37(0..36)] MultiUserCache:false ProjectorPath: MainGPU:0 UseMmap:false}"
Sep 11 00:42:49 ai ollama[3110]: time=2025-09-11T00:42:49.588+02:00 level=INFO source=ggml.go:131 msg="" architecture=gptoss file_type=MXFP4 name="" description="" num_tensors=471 num_key_values=30
Sep 11 00:42:50 ai ollama[3110]: ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
Sep 11 00:42:50 ai ollama[3110]: ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
Sep 11 00:42:50 ai ollama[3110]: ggml_cuda_init: found 1 ROCm devices:
Sep 11 00:42:50 ai ollama[3110]:   Device 0: AMD Radeon Graphics, gfx1151 (0x1151), VMM: no, Wave Size: 32, ID: 0
Sep 11 00:42:50 ai ollama[3110]: load_backend: loaded ROCm backend from /usr/local/lib/ollama/libggml-hip.so
Sep 11 00:42:50 ai ollama[3110]: load_backend: loaded CPU backend from /usr/local/lib/ollama/libggml-cpu-icelake.so
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.273+02:00 level=INFO source=ggml.go:104 msg=system CPU.0.SSE3=1 CPU.0.SSSE3=1 CPU.0.AVX=1 CPU.0.AVX2=1 CPU.0.F16C=1 CPU.0.FMA=1 CPU.0.BMI2=1 CPU.0.AVX512=1 CPU.0.AVX512_VBMI=1 CPU.0.AVX512_VNNI=1 CPU.0.LLAMAFILE=1 CPU.1.LLAMAFILE=1 ROCm.0.NO_VMM=1 ROCm.0.PEER_MAX_BATCH_SIZE=128 compiler=cgo(gcc)
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=ggml.go:487 msg="offloading 36 repeating layers to GPU"
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=ggml.go:493 msg="offloading output layer to GPU"
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=ggml.go:498 msg="offloaded 37/37 layers to GPU"
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=backend.go:310 msg="model weights" device=ROCm0 size="59.8 GiB"
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=backend.go:315 msg="model weights" device=CPU size="1.1 GiB"
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=backend.go:321 msg="kv cache" device=ROCm0 size="450.0 MiB"
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=backend.go:332 msg="compute graph" device=ROCm0 size="121.8 MiB"
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=backend.go:337 msg="compute graph" device=CPU size="5.6 MiB"
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=backend.go:342 msg="total memory" size="61.4 GiB"
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=sched.go:473 msg="loaded runners" count=1
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=server.go:1250 msg="waiting for llama runner to start responding"
Sep 11 00:42:50 ai ollama[3110]: time=2025-09-11T00:42:50.484+02:00 level=INFO source=server.go:1284 msg="waiting for server to become available" status="llm server loading model"
Sep 11 00:43:02 ai ollama[3110]: time=2025-09-11T00:43:02.770+02:00 level=INFO source=server.go:1288 msg="llama runner started in 13.23 seconds"
Sep 11 00:43:53 ai systemd[2544]: launchpadlib-cache-clean.service - Clean up old files in the Launchpadlib cache was skipped because of an unmet condition check (ConditionPathExists=/home/mvlsd/.launchpadlib/api.launchpad.net/cache).
░░ Subject: A start job for unit UNIT has finished successfully
░░ Defined-By: systemd
░░ Support: http://www.ubuntu.com/support
░░ 
░░ A start job for unit UNIT has finished successfully.
░░ 
░░ The job identifier is 70.
Sep 11 00:44:04 ai ollama[3110]: [GIN] 2025/09/11 - 00:44:04 | 200 |         1m15s |      172.17.0.2 | POST     "/api/chat"
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3184 thread ollama pid 3192)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007f3fa8f64000 from client 10
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MORE_FAULTS: 0x1
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          WALKER_ERROR: 0x0
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MAPPING_ERROR: 0x0
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          RW: 0x0
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3184 thread ollama pid 3192)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007f3fa8f5c000 from client 10
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x008012B1
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          Faulty UTCL2 client ID: SQC (inst) (0x9)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MORE_FAULTS: 0x1
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          WALKER_ERROR: 0x0
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          PERMISSION_FAULTS: 0xb
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MAPPING_ERROR: 0x0
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          RW: 0x0
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3184 thread ollama pid 3192)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007f3fa8f5c000 from client 10
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3184 thread ollama pid 3192)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007f3fa8f56000 from client 10
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:88 vmid:8 pasid:32770)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3184 thread ollama pid 3192)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3184 thread ollama pid 3192)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00000000ff000000 from client 10
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3184 thread ollama pid 3192)
Sep 11 00:44:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x000000003edde000 from client 10
Sep 11 00:44:23 ai ollama[3110]: Memory access fault by GPU node-1 (Agent handle: 0x7f50d8692b30) on address 0x7f3fa8f64000. Reason: Page not present or supervisor privilege.
Sep 11 00:44:23 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
Sep 11 00:44:23 ai kernel: [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
Sep 11 00:44:23 ai kernel: amdgpu 0000:c4:00.0: amdgpu: failed to suspend gangs from MES
Sep 11 00:44:23 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Sep 11 00:44:23 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Suspending all queues failed
Sep 11 00:44:23 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset begin!
Sep 11 00:44:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 5
Sep 11 00:44:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 4
Sep 11 00:44:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 3
Sep 11 00:44:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 2
Sep 11 00:44:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
Sep 11 00:44:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 0
Sep 11 00:44:24 ai kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
Sep 11 00:44:24 ai kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
Sep 11 00:44:24 ai kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
Sep 11 00:44:24 ai kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
Sep 11 00:44:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Dumping IP State
Sep 11 00:44:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Dumping IP State Completed
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
Sep 11 00:44:27 ai kernel: [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MODE2 reset
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset succeeded, trying to resume
Sep 11 00:44:27 ai kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008FFFB00000).
Sep 11 00:44:27 ai kernel: [drm] VRAM is lost due to GPU reset!
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: SMU is resuming...
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: SMU is resumed successfully!
Sep 11 00:44:27 ai kernel: [drm] DMUB hardware initialized: version=0x09000F00
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
Sep 11 00:44:27 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset(1) succeeded!
Sep 11 00:44:27 ai kernel: amdgpu: Freeing queue vital buffer 0x7f3f9de00000, queue evicted
Sep 11 00:44:27 ai kernel: amdgpu: Freeing queue vital buffer 0x7f3fa8200000, queue evicted
Sep 11 00:44:27 ai kernel: amdgpu: Freeing queue vital buffer 0x7f5018a00000, queue evicted
Sep 11 00:44:27 ai kernel: amdgpu: Freeing queue vital buffer 0x7f501a000000, queue evicted
Sep 11 00:44:27 ai kernel: amdgpu: Freeing queue vital buffer 0x7f501ae00000, queue evicted
Sep 11 00:44:27 ai ollama[3110]: [GIN] 2025/09/11 - 00:44:27 | 500 | 23.156863789s |      172.17.0.2 | POST     "/api/chat"
Sep 11 00:44:27 ai ollama[3110]: time=2025-09-11T00:44:27.777+02:00 level=WARN source=server.go:1170 msg="llama runner process no longer running" sys=134 string="signal: aborted (core dumped)"
Sep 11 00:44:27 ai ollama[3110]: time=2025-09-11T00:44:27.777+02:00 level=WARN source=server.go:1170 msg="llama runner process no longer running" sys=134 string="signal: aborted (core dumped)"
Sep 11 00:44:28 ai ollama[3110]: time=2025-09-11T00:44:28.618+02:00 level=INFO source=server.go:199 msg="model wants flash attention"
Sep 11 00:44:28 ai ollama[3110]: time=2025-09-11T00:44:28.618+02:00 level=INFO source=server.go:216 msg="enabling flash attention"
Sep 11 00:44:28 ai ollama[3110]: time=2025-09-11T00:44:28.618+02:00 level=WARN source=server.go:224 msg="kv cache type not supported by model" type=""
Sep 11 00:44:28 ai ollama[3110]: time=2025-09-11T00:44:28.619+02:00 level=INFO source=server.go:398 msg="starting runner" cmd="/usr/local/bin/ollama runner --ollama-engine --model /usr/share/ollama/.ollama/models/blobs/sha256-90a618fe6ff21b09ca968df959104eb650658b0bef0faef785c18c2795d993e3 --port 43209"
Sep 11 00:44:28 ai ollama[3110]: time=2025-09-11T00:44:28.619+02:00 level=INFO source=server.go:503 msg="system memory" total="62.6 GiB" free="59.5 GiB" free_swap="8.0 GiB"
Sep 11 00:44:28 ai ollama[3110]: time=2025-09-11T00:44:28.619+02:00 level=INFO source=memory.go:36 msg="new model will fit in available VRAM across minimum required GPUs, loading" model=/usr/share/ollama/.ollama/models/blobs/sha256-90a618fe6ff21b09ca968df959104eb650658b0bef0faef785c18c2795d993e3 library=rocm parallel=1 required="62.4 GiB" gpus=1
Sep 11 00:44:28 ai ollama[3110]: time=2025-09-11T00:44:28.620+02:00 level=INFO source=server.go:543 msg=offload library=rocm layers.requested=-1 layers.model=37 layers.offload=37 layers.split=[37] memory.available="[63.8 GiB]" memory.gpu_overhead="0 B" memory.required.full="62.4 GiB" memory.required.partial="62.4 GiB" memory.required.kv="450.0 MiB" memory.required.allocations="[62.4 GiB]" memory.weights.total="59.7 GiB" memory.weights.repeating="58.6 GiB" memory.weights.nonrepeating="1.1 GiB" memory.graph.full="122.0 MiB" memory.graph.partial="122.0 MiB"
Sep 11 00:44:28 ai ollama[3110]: time=2025-09-11T00:44:28.627+02:00 level=INFO source=runner.go:1251 msg="starting ollama engine"
Sep 11 00:44:28 ai ollama[3110]: time=2025-09-11T00:44:28.627+02:00 level=INFO source=runner.go:1286 msg="Server listening on 127.0.0.1:43209"
Sep 11 00:44:28 ai ollama[3110]: time=2025-09-11T00:44:28.631+02:00 level=INFO source=runner.go:1170 msg=load request="{Operation:commit LoraPath:[] Parallel:1 BatchSize:512 FlashAttention:true KvSize:8192 KvCacheType: NumThreads:16 GPULayers:37[ID:0 Layers:37(0..36)] MultiUserCache:false ProjectorPath: MainGPU:0 UseMmap:false}"
Sep 11 00:44:28 ai ollama[3110]: time=2025-09-11T00:44:28.660+02:00 level=INFO source=ggml.go:131 msg="" architecture=gptoss file_type=MXFP4 name="" description="" num_tensors=471 num_key_values=30
Sep 11 00:44:29 ai ollama[3110]: ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
Sep 11 00:44:29 ai ollama[3110]: ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
Sep 11 00:44:29 ai ollama[3110]: ggml_cuda_init: found 1 ROCm devices:
Sep 11 00:44:29 ai ollama[3110]:   Device 0: AMD Radeon Graphics, gfx1151 (0x1151), VMM: no, Wave Size: 32, ID: 0
Sep 11 00:44:29 ai ollama[3110]: load_backend: loaded ROCm backend from /usr/local/lib/ollama/libggml-hip.so
Sep 11 00:44:29 ai ollama[3110]: load_backend: loaded CPU backend from /usr/local/lib/ollama/libggml-cpu-icelake.so
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.289+02:00 level=INFO source=ggml.go:104 msg=system CPU.0.SSE3=1 CPU.0.SSSE3=1 CPU.0.AVX=1 CPU.0.AVX2=1 CPU.0.F16C=1 CPU.0.FMA=1 CPU.0.BMI2=1 CPU.0.AVX512=1 CPU.0.AVX512_VBMI=1 CPU.0.AVX512_VNNI=1 CPU.0.LLAMAFILE=1 CPU.1.LLAMAFILE=1 ROCm.0.NO_VMM=1 ROCm.0.PEER_MAX_BATCH_SIZE=128 compiler=cgo(gcc)
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.444+02:00 level=INFO source=ggml.go:487 msg="offloading 36 repeating layers to GPU"
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.445+02:00 level=INFO source=ggml.go:493 msg="offloading output layer to GPU"
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.445+02:00 level=INFO source=ggml.go:498 msg="offloaded 37/37 layers to GPU"
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.445+02:00 level=INFO source=backend.go:310 msg="model weights" device=ROCm0 size="59.8 GiB"
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.445+02:00 level=INFO source=backend.go:315 msg="model weights" device=CPU size="1.1 GiB"
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.445+02:00 level=INFO source=backend.go:321 msg="kv cache" device=ROCm0 size="450.0 MiB"
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.445+02:00 level=INFO source=backend.go:332 msg="compute graph" device=ROCm0 size="121.8 MiB"
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.445+02:00 level=INFO source=backend.go:337 msg="compute graph" device=CPU size="5.6 MiB"
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.445+02:00 level=INFO source=backend.go:342 msg="total memory" size="61.4 GiB"
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.445+02:00 level=INFO source=sched.go:473 msg="loaded runners" count=1
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.445+02:00 level=INFO source=server.go:1250 msg="waiting for llama runner to start responding"
Sep 11 00:44:29 ai ollama[3110]: time=2025-09-11T00:44:29.445+02:00 level=INFO source=server.go:1284 msg="waiting for server to become available" status="llm server loading model"
Sep 11 00:44:41 ai ollama[3110]: time=2025-09-11T00:44:41.480+02:00 level=INFO source=server.go:1288 msg="llama runner started in 12.86 seconds"
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3357 thread ollama pid 3369)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x000070fb1a75c000 from client 10
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MORE_FAULTS: 0x1
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          WALKER_ERROR: 0x0
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MAPPING_ERROR: 0x0
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          RW: 0x0
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3357 thread ollama pid 3369)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x000070fb1a75c000 from client 10
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x008012B0
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          Faulty UTCL2 client ID: SQC (inst) (0x9)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MORE_FAULTS: 0x0
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          WALKER_ERROR: 0x0
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          PERMISSION_FAULTS: 0xb
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MAPPING_ERROR: 0x0
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          RW: 0x0
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3357 thread ollama pid 3369)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x000070fb1a764000 from client 10
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3357 thread ollama pid 3369)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x000070fb1a756000 from client 10
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:88 vmid:8 pasid:32770)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 3357 thread ollama pid 3369)
Sep 11 00:44:53 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
Sep 11 00:44:56 ai kernel: [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: failed to suspend gangs from MES
Sep 11 00:44:56 ai ollama[3110]: Memory access fault by GPU node-1 (Agent handle: 0x710c30692b30) on address 0x70fb1a75c000. Reason: Page not present or supervisor privilege.
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Suspending all queues failed
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset begin!
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 5
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 4
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 3
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 2
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 0
Sep 11 00:44:56 ai kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
Sep 11 00:44:56 ai kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Dumping IP State
Sep 11 00:44:56 ai kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
Sep 11 00:44:56 ai kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
Sep 11 00:44:56 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Dumping IP State Completed
Sep 11 00:44:59 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
Sep 11 00:44:59 ai kernel: [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
Sep 11 00:44:59 ai kernel: amdgpu 0000:c4:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
Sep 11 00:44:59 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MODE2 reset
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset succeeded, trying to resume
Sep 11 00:45:00 ai kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008FFFB00000).
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: SMU is resuming...
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: SMU is resumed successfully!
Sep 11 00:45:00 ai kernel: [drm] DMUB hardware initialized: version=0x09000F00
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
Sep 11 00:45:00 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset(2) succeeded!
Sep 11 00:45:00 ai kernel: amdgpu: Freeing queue vital buffer 0x70fafa800000, queue evicted
Sep 11 00:45:00 ai kernel: amdgpu: Freeing queue vital buffer 0x70fb19a00000, queue evicted
Sep 11 00:45:00 ai kernel: amdgpu: Freeing queue vital buffer 0x710a85c00000, queue evicted
Sep 11 00:45:00 ai kernel: amdgpu: Freeing queue vital buffer 0x710a87200000, queue evicted
Sep 11 00:45:00 ai kernel: amdgpu: Freeing queue vital buffer 0x710a8d200000, queue evicted
Sep 11 00:45:00 ai ollama[3110]: [GIN] 2025/09/11 - 00:45:00 | 500 | 32.518146638s |      172.17.0.2 | POST     "/api/chat"
Sep 11 00:45:00 ai ollama[3110]: time=2025-09-11T00:45:00.315+02:00 level=WARN source=server.go:1170 msg="llama runner process no longer running" sys=134 string="signal: aborted (core dumped)"
Sep 11 00:45:00 ai ollama[3110]: time=2025-09-11T00:45:00.315+02:00 level=WARN source=server.go:1170 msg="llama runner process no longer running" sys=134 string="signal: aborted (core dumped)"
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.161+02:00 level=INFO source=server.go:199 msg="model wants flash attention"
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.161+02:00 level=INFO source=server.go:216 msg="enabling flash attention"
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.161+02:00 level=WARN source=server.go:224 msg="kv cache type not supported by model" type=""
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.161+02:00 level=INFO source=server.go:398 msg="starting runner" cmd="/usr/local/bin/ollama runner --ollama-engine --model /usr/share/ollama/.ollama/models/blobs/sha256-90a618fe6ff21b09ca968df959104eb650658b0bef0faef785c18c2795d993e3 --port 45163"
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.161+02:00 level=INFO source=server.go:503 msg="system memory" total="62.6 GiB" free="59.4 GiB" free_swap="8.0 GiB"
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.162+02:00 level=INFO source=memory.go:36 msg="new model will fit in available VRAM across minimum required GPUs, loading" model=/usr/share/ollama/.ollama/models/blobs/sha256-90a618fe6ff21b09ca968df959104eb650658b0bef0faef785c18c2795d993e3 library=rocm parallel=1 required="62.4 GiB" gpus=1
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.162+02:00 level=INFO source=server.go:543 msg=offload library=rocm layers.requested=-1 layers.model=37 layers.offload=37 layers.split=[37] memory.available="[63.8 GiB]" memory.gpu_overhead="0 B" memory.required.full="62.4 GiB" memory.required.partial="62.4 GiB" memory.required.kv="450.0 MiB" memory.required.allocations="[62.4 GiB]" memory.weights.total="59.7 GiB" memory.weights.repeating="58.6 GiB" memory.weights.nonrepeating="1.1 GiB" memory.graph.full="122.0 MiB" memory.graph.partial="122.0 MiB"
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.169+02:00 level=INFO source=runner.go:1251 msg="starting ollama engine"
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.169+02:00 level=INFO source=runner.go:1286 msg="Server listening on 127.0.0.1:45163"
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.173+02:00 level=INFO source=runner.go:1170 msg=load request="{Operation:commit LoraPath:[] Parallel:1 BatchSize:512 FlashAttention:true KvSize:8192 KvCacheType: NumThreads:16 GPULayers:37[ID:0 Layers:37(0..36)] MultiUserCache:false ProjectorPath: MainGPU:0 UseMmap:false}"
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.204+02:00 level=INFO source=ggml.go:131 msg="" architecture=gptoss file_type=MXFP4 name="" description="" num_tensors=471 num_key_values=30
Sep 11 00:45:01 ai ollama[3110]: ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
Sep 11 00:45:01 ai ollama[3110]: ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
Sep 11 00:45:01 ai ollama[3110]: ggml_cuda_init: found 1 ROCm devices:
Sep 11 00:45:01 ai ollama[3110]:   Device 0: AMD Radeon Graphics, gfx1151 (0x1151), VMM: no, Wave Size: 32, ID: 0
Sep 11 00:45:01 ai ollama[3110]: load_backend: loaded ROCm backend from /usr/local/lib/ollama/libggml-hip.so
Sep 11 00:45:01 ai ollama[3110]: load_backend: loaded CPU backend from /usr/local/lib/ollama/libggml-cpu-icelake.so
Sep 11 00:45:01 ai ollama[3110]: time=2025-09-11T00:45:01.845+02:00 level=INFO source=ggml.go:104 msg=system CPU.0.SSE3=1 CPU.0.SSSE3=1 CPU.0.AVX=1 CPU.0.AVX2=1 CPU.0.F16C=1 CPU.0.FMA=1 CPU.0.BMI2=1 CPU.0.AVX512=1 CPU.0.AVX512_VBMI=1 CPU.0.AVX512_VNNI=1 CPU.0.LLAMAFILE=1 CPU.1.LLAMAFILE=1 ROCm.0.NO_VMM=1 ROCm.0.PEER_MAX_BATCH_SIZE=128 compiler=cgo(gcc)
Sep 11 00:45:01 ai CRON[3477]: pam_unix(cron:session): session opened for user root(uid=0) by root(uid=0)
Sep 11 00:45:01 ai CRON[3478]: (root) CMD (command -v debian-sa1 > /dev/null && debian-sa1 1 1)
Sep 11 00:45:01 ai CRON[3477]: pam_unix(cron:session): session closed for user root
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.001+02:00 level=INFO source=ggml.go:487 msg="offloading 36 repeating layers to GPU"
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.001+02:00 level=INFO source=ggml.go:493 msg="offloading output layer to GPU"
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.001+02:00 level=INFO source=ggml.go:498 msg="offloaded 37/37 layers to GPU"
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.001+02:00 level=INFO source=backend.go:310 msg="model weights" device=ROCm0 size="59.8 GiB"
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.001+02:00 level=INFO source=backend.go:315 msg="model weights" device=CPU size="1.1 GiB"
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.001+02:00 level=INFO source=backend.go:321 msg="kv cache" device=ROCm0 size="450.0 MiB"
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.001+02:00 level=INFO source=backend.go:332 msg="compute graph" device=ROCm0 size="121.8 MiB"
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.001+02:00 level=INFO source=backend.go:337 msg="compute graph" device=CPU size="5.6 MiB"
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.001+02:00 level=INFO source=backend.go:342 msg="total memory" size="61.4 GiB"
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.001+02:00 level=INFO source=sched.go:473 msg="loaded runners" count=1
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.001+02:00 level=INFO source=server.go:1250 msg="waiting for llama runner to start responding"
Sep 11 00:45:02 ai ollama[3110]: time=2025-09-11T00:45:02.002+02:00 level=INFO source=server.go:1284 msg="waiting for server to become available" status="llm server loading model"
Sep 11 00:45:14 ai ollama[3110]: time=2025-09-11T00:45:14.038+02:00 level=INFO source=server.go:1288 msg="llama runner started in 12.88 seconds"
Sep 11 00:45:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Sep 11 00:45:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1006
Sep 11 00:45:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Sep 11 00:45:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 3
Sep 11 00:45:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset begin!
Sep 11 00:45:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
Sep 11 00:45:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 0
Sep 11 00:45:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Dumping IP State
Sep 11 00:45:21 ai ollama[3110]: HW Exception by GPU node-1 (Agent handle: 0x7f7674692cc0) reason :GPU Hang
Sep 11 00:45:21 ai kernel: amdgpu 0000:c4:00.0: amdgpu: Dumping IP State Completed
Sep 11 00:45:21 ai kernel: amdgpu: Freeing queue vital buffer 0x7f652aa00000, queue evicted
Sep 11 00:45:21 ai kernel: amdgpu: Freeing queue vital buffer 0x7f6542200000, queue evicted
Sep 11 00:45:21 ai kernel: amdgpu: Freeing queue vital buffer 0x7f65b4800000, queue evicted
Sep 11 00:45:21 ai kernel: amdgpu: Freeing queue vital buffer 0x7f74b4600000, queue evicted
Sep 11 00:45:21 ai kernel: amdgpu: Freeing queue vital buffer 0x7f74b5c00000, queue evicted
Sep 11 00:45:21 ai ollama[3110]: time=2025-09-11T00:45:21.681+02:00 level=ERROR source=server.go:1458 msg="post predict" error="Post \"http://127.0.0.1:45163/completion\": EOF"
Sep 11 00:45:21 ai ollama[3110]: [GIN] 2025/09/11 - 00:45:21 | 500 | 21.453422508s |      172.17.0.2 | POST     "/api/chat"
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MORE_FAULTS: 0x1
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          WALKER_ERROR: 0x1
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          PERMISSION_FAULTS: 0x5
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MAPPING_ERROR: 0x1
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          RW: 0x1
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Sep 11 00:45:22 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
Sep 11 00:45:24 ai kernel: [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MORE_FAULTS: 0x1
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          WALKER_ERROR: 0x1
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          PERMISSION_FAULTS: 0x5
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          MAPPING_ERROR: 0x1
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu:          RW: 0x1
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: MODE2 reset
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset succeeded, trying to resume
Sep 11 00:45:24 ai kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008FFFB00000).
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: SMU is resuming...
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: SMU is resumed successfully!
Sep 11 00:45:24 ai kernel: [drm] DMUB hardware initialized: version=0x09000F00
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
Sep 11 00:45:24 ai kernel: amdgpu 0000:c4:00.0: amdgpu: GPU reset(3) succeeded!
```

rocminfo gives me this:

```
ROCk module version 6.12.12 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.11
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD RYZEN AI MAX+ PRO 395 w/ Radeon 8060S
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD RYZEN AI MAX+ PRO 395 w/ Radeon 8060S
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
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   5185                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65604776(0x3e90ca8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65604776(0x3e90ca8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65604776(0x3e90ca8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65604776(0x3e90ca8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1151                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
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
    L1:                      32(0x20) KB                        
    L2:                      2048(0x800) KB                     
    L3:                      16384(0x4000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   50176                              
  Internal Node ID:        1                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       APU
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 26                                 
  SDMA engine uCode::      14                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67108864(0x4000000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67108864(0x4000000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1151         
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
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
*** Done ***     
```

Looks correct to me ...

Hope this helps, write me, if you need more :).



---

### 评论 #28 — waltercool (2025-09-10T23:15:29Z)

Honestly, consider you are using an experimental brach for now, I would expect at least to use latest kernels (6.16 or 6.17).

AI Max gets lots of improvenants after 6.14 - 6.15 in terms of stability. How can you use 6.12 with a recent hardware? Honestly surprised if that works :-) 

---

### 评论 #29 — mveigel-softkomplett (2025-09-11T15:36:32Z)

@waltercool I choosed this kernel, because of the AMD package in the rocm7.0.0rc1 repository - which i expect to work best with the provided libraries - is for this kernel (6.12.12). Do you know, how to compile amdgpu from AMD with a 6.14 - 6.17 kernel (reliably? And i don't mean the open source driver ;) ). I had several problems with the driver and much less changed kernels (e.g. only one minor version).

But i get your point, and will try to use the open source driver - but aren't there some features missing? Or is this information outdated?

And it comes from my decission - I choose the distribution and not the kernel ;). The only thing which is not working, is the network driver. Neither with the downloadable sources (dkms) nor with the driver from the vendor (I got it working - somewhat, at least it answered to a ping, but not reliable). A newer kernel might bring support for this device.

Maybe I switch from ubuntu to fedora ... 

---

### 评论 #30 — waltercool (2025-09-12T14:51:20Z)

As far I know, the sole purpose of **amdgpu-pro** is the support for business. It usually perform a bit worse.

AMD does not have control of the Linux kernel entirely, so they can't offer business support as intended. In other hand, AMD have dedicated team to develop and improve the **amdgpu** driver.

You don't have to change Ubuntu to Fedora, you can just upgrade the kernel from repositories if required (Ubuntu 24.04):

https://ubuntuhandbook.org/index.php/2025/07/linux-kernel-6-16-released-with-new-hardware-support-mainline-ppa/

---

### 评论 #31 — Qubitium (2025-09-14T00:40:14Z)

@mveigel-softkomplett  I would highly suggest not compiling your own kernel or assume same kernel version would resolve compat issues. If you want to compile your own kernel on a distro not supported by AMD, you should save tons of headache by copying the Ubuntu kernel `config` file which toggles on/off many kernel features. The config file is part of Ubuntu kernel builds. With the same kernel config (compile) flags, you should now expect close to 100% compat. 

---

### 评论 #32 — mveigel-softkomplett (2025-09-14T10:33:11Z)

@Qubitium I compiled my last Kernel about 10-20 years ago (successfully, and the systems are working well ;) ) -  before that I comiled Kernels for PCs, s370, a lot of embedded systems, even some hardly supporting arm processors ... - all working fine. I think I know how to do it ;) - what doesn't mean that I could not make mistakes! I downloaded the compiled Kernel als deb files. And I was working on Ubuntu 24.04 (as mentioned before, which is supported by the Kernel driver). And as i've written (hopefully) I'm using Kernel 6.12.12 which was the release, which was used for the amdgpu driver.
I also noticed (AFAIK), that this happens on every amdgpu driver (the official distributed for ubuntu 24.04 and all the other kernels). I really thank you for your suggestions and appreciate your help.

@waltercool @schung-amd I tried Kernel 6.16 as suggested by waltercool and it help a bit. The Problems get less, but still exist (with ollama). Especially the message about the GCVM_... stuff get much less. But the Problems with MES still exists - but only at the end of the answer, not after thinking. I'm now able to ask even a few questions. But if it stumbles once, it stumbles often - until a reboot. I will try to check with lvvm and llama.cpp if this works better.
I also successfully compiles llama.cpp and ollama with vulkan support. In this case everything worked fine, but needed an awful lot of memory (about 55 GB für the 24 GB qwen3-coder model). I think it's because of the missing flash attention?

It's a bit anoying, that all these tools try to make their own eco system, so it's hard to interchange the models :(.

@waltercool Regarding Fedora and Ubuntu ... I'm normally working in the Red Hat eco system, so I'm more familiar with Fedora than with Ubuntu. But when it comes to AI or Geo maps, i found ubuntu is better supported by the system and the community. So I use it for these cases. But it looks, that (regarding AI) Fedora now makes a few steps ahead - this is why I wanted to try it. Not just because of the amdgpu driver ;).

I'll test a few scenarios in the evening and will write my findings here ...

---

### 评论 #33 — MachaLvl99 (2025-09-25T09:54:51Z)

Hello everyone! Not normally the type to comment on (or try to resolve) github issues, but I just wanted to mention I'm throwing my hat in the ring here, actively following this thread and [this one over here previously mentioned](https://github.com/ROCm/TheRock/issues/1408), and am doing my best to get a working vllm container going for ROCm that can be deployed on gfx1151 chips ASAP. Currently experimenting with some workarounds, and I think I'm pretty close, but I may still be in over my head here we'll see.
I have a lot invested in this for several reasons, mainly because lm studio isn't capable of doing what i want/need, significantly hindering the performance potential of the 128GB chip, but also because I use and run NixOS, so no one's coming to save or help me lol. What I can do though is containerize it so if I can get it working on my NixOS build (which is otherwise running flawlessly on the Ryzen AI Max+ chip), it should work on pretty much any linux distro and therefore help out everyone. 
Anyways I'll post here again in the coming days once I have a working container for this. 
Stay tuned y'all help is on the way

---

### 评论 #34 — ndrewpj (2025-09-25T17:55:22Z)

AMD lied in their presentation. They said ROCm 7 WILL support the APU. ROCm 7.0 was released - there is no support. 7.0.1 is released - no support. Yes, llama.cpp works but... ROCm is performing just OKish comparing to Vulkan. AMD just don't care about its image in front of end users. As an owner of 395 128GB variant my only hope is that Vllm will make Vulkan compatibility.

PS. Somehow I feel AMD is becoming not a runner-up or competitor to Nvidia in new sectors but a second "Intel"

---

### 评论 #35 — schung-amd (2025-09-25T19:46:04Z)

I don't think we explicitly stated that 7.0 (or any other specific version) would support APUs.

We just released [ROCm 6.4.4](https://www.amd.com/en/resources/support-articles/release-notes/RN-AMDGPU-LINUX-ROCM-6-4-4.html) with added APU support. There is some confusing versioning here, however, as this is released after 7.0.1. Long story short, we wanted to accelerate support, so this release does not have the ROCm 7 changes and has not undergone the amount of testing that our mainline releases are generally subject to. In the future I believe the plan is to have the ROCm on Ryzen releases be more in line with the mainline releases both in terms of versioning and QA.

e: Install docs at https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/, and as noted in the compatibility table, this should be treated as preview support (i.e. some things might be broken)

---

### 评论 #36 — mveigel-softkomplett (2025-09-25T20:16:17Z)

@schung-amd I'm a bit confused now. There are some releases in 7.0rc which support the APU? It looks like the driver or the firmware has Problems, but there seems to be support. So is it better to use 6.4.4 and set the HSA_... variable? To "downgrade" the GPU? And the flag should make make it slower, because some features are not used, am I right? Do these AMD politics make any sense?

And to be honest about the comment of @ndrewpj - he is absolutely right. AMD presents (Still!) the AI 395+ MAX as an AI focused GPU. So do the press articles which mostly rewrite the AMD press releases. And nobody tells you, that this GPU does not really support AI by the drivers or rocm. Of course you might use vulkan to have ANY working model, but using 55 GB for a 24 GB model is far away from something what I would call, a good choice on the hardware.

In this case (schung-amd, please don't take it personally, because I know how much heart you invested in your "the-rock" containers) - schame on AMD. Your Management really did a bad job and I'm sure a lot of people will remember what you did, when they have to buy the next hardware. I know a lot of people, which still remember the time when NVIDIA adds some slower VRAM to a part of the total VRAM (and this is ages ago).

I spend about 2900 (not 290) Euro in this box, which really does not what AMD told me it should do. I'll remember this, when I have to buy the next hardware - for sure.


---

### 评论 #37 — schung-amd (2025-09-25T20:24:25Z)

If you want a mainline ROCm version for Strix and Strix Halo, use the ROCm on Ryzen release. You don't need to use HSA_OVERRIDE_GFX_VERSION with ROCm 6.4.4, it should have support built in. Firmware-wise, there are some required firmware updates to resolve a known issue for gfx1150 and gfx1151 which made their way into recent linux-firmware releases on Ubuntu and Arch, Fedora lagging behind a bit but there is a rawhide package which should have the fixes.

---

### 评论 #38 — ndrewpj (2025-09-25T20:26:15Z)

> I don't think we explicitly stated that 7.0 (or any other specific version) would support APUs.
> 
> We just released [ROCm 6.4.4](https://www.amd.com/en/resources/support-articles/release-notes/RN-AMDGPU-LINUX-ROCM-6-4-4.html) with added APU support. There is some confusing versioning here, however, as this is released after 7.0.1. Long story short, we wanted to accelerate support, so this release does not have the ROCm 7 changes and has not undergone the amount of testing that our mainline releases are generally subject to. In the future I believe the plan is to have the ROCm on Ryzen releases be more in line with the mainline releases both in terms of versioning and QA.
> 
> e: Install docs at https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/, and as noted in the compatibility table, this should be treated as preview support (i.e. some things might be broken)

Well, if such slide in the company's presentation about ROCm 7 is not a large statement I don't know how else to read it:

![Image](https://github.com/user-attachments/assets/0711a41f-119f-428a-a07c-15caafe97408)

---

### 评论 #39 — schung-amd (2025-09-25T20:31:55Z)

Yes, we plan to have support for ROCm 7, but that doesn't specify 7.0. I'm not arguing with your perception, as clearly the marketing slides have not been clear, but trying to clarify what support is actually coming. At the end of the day this will be fixed by providing users with ROCm releases that have APU support (which we are doing), and the marketing slides are just a layer of noise on top of this.

---

### 评论 #40 — schung-amd (2025-09-25T20:35:36Z)

> the flag should make make it slower, because some features are not used, am I right?

To clarify what HSA_OVERRIDE_GFX_VERSION does, it forces a different ISA and kernels to be used over your GPU's default. The specific performance effects depend on your GPU, as some architecture families are more similar than others. For an extreme example of detrimental effects, overriding a gfx1102 GPU to gfx1100 or gfx1101 will cause issues due to a difference in the number of VGPRs on those devices, so some gfx1100 and gfx1101 kernels are not usable. In general I don't recommend doing this unless it is necessary for compatibility, but with the understanding that it may break things.

---

### 评论 #41 — ndrewpj (2025-09-25T20:35:59Z)

> Yes, we plan to have support for ROCm 7, but that doesn't specify 7.0. I'm not arguing with your perception, as clearly the marketing slides have not been clear, but trying to clarify what support is actually coming. At the end of the day this will be fixed by providing users with ROCm releases that have APU support (which we are doing), and the marketing slides are just a layer of noise on top of this.

I am not pushing you personally, if that is the perception - sorry. I understand  big tech companies internals and priorities. But as a simple buyer I am very disappointed. I am true AMD fan but...well...Hope you have devs that will find a fraction(s) of time to make at least MVP. ps. Slide like this was also "circulating"

![Image](https://github.com/user-attachments/assets/49fc17b7-8906-4e01-b5c6-8fe54707ff31)

---

### 评论 #42 — schung-amd (2025-09-25T20:44:58Z)

Yes, that Computex slide has caused a lot of pain. It was technically correct at the time because we had native Windows support and were working on Linux support, but at the same time we're restricted on what info we can provide on future timelines. Furthermore for a lot of users AI support really means PyTorch support, which was not present at the time. 

Unfortunately, the result is that for many months we could only tell users that support was planned, which is not enough information for users to make informed purchasing decisions. I understand the frustration of the many users on this and similar issues, and I'm personally hoping our policies on providing timeline and roadmap information will loosen up a bit in the future.

That being said, with ROCm 6.4.4 mainline support is here (with the caveat that it is preview support). ROCm 7 is planned to be supported in a future point release (but again, there is no specific timeline information I can share).

---

### 评论 #43 — waltercool (2025-09-25T21:33:08Z)

> I am not pushing you personally, if that is the perception - sorry. I understand big tech companies internals and priorities. But as a simple buyer I am very disappointed. I am true AMD fan but...well...Hope you have devs that will find a fraction(s) of time to make at least MVP. ps. Slide like this was also "circulating"

I'm not intending to keep this discussion far longer because it's going in the wrong direction of the reported issue, and annoying 10+ people with every message.

@ndrewpj While gfx1151 is not officially supported, it works fine for AI computing overall, no major hacks. The whole ROCm works fine and I'm running it right now for pytorch based projects using their official Docker with Pytorch included.

As someone who been actively following this process for a while, I know some issues are still being reported, some libraries still need migration (like aotriton) leading to under-perform for Flash Attention (very important for AI stuff), AMD team is very aware and working on those.

Some tools like Ollama, vLLM or LMStudio may have some issues, for example, Ollama have a [long known issue with iGPUs](https://github.com/ollama/ollama/issues/2637) and [not supporting GTT](https://github.com/ollama/ollama/issues/11451), some people decided to create forks like ollama-rocm-docker-gfx1151 or ollama-linux-amd-apu until Ollama team properly does the changes required.

Friendly reminder ROCm is not just "AI stuff", it does ton of complex operations for scientific purposes. AI is just a simple use-case scenario. For Text-AI generation, the **llamacpp Vulkan backend** been working fine since day zero (LMStudio), including the correct GTT calculation, outperforming ROCm.

As a personal experience, you can also use Image and Audio generation without much problems with gfx1151 using ROCM official Docker, the main issue right now is _video generation_ as uses ton of VRAM due lack of aotriton. Please follow [this issue](https://github.com/ROCm/ROCm/issues/5404) until is ready.

You also have to understand AMD won't risk to test in Production, so likely couple of months still need to happen until proven OK for quality purposes, my best suggestion if you want to play with "dev" environment, are the TheRock builds until [this issue](https://github.com/ROCm/TheRock/issues/1408) gets resolved.

---

### 评论 #44 — MachaLvl99 (2025-09-26T05:58:21Z)

I've returned!
So, I've been digging around and trying to make sense of the landscape here. Again, please bear with me as I'm still new-ish to contributing, paying attention to github issues, etc, but I'm focusing and responding purely to this github's issue topic: Getting vllm inferencing stable on these gfx1151 chips and no other noise. There's a lot of moving parts, noticing some of these issues are from repos that AMD **has little to no control over**, and I noticed (again) others have beaten me to resolving some of the issues I discovered when trying to build my own container. I was about halfway through a janky hack when I was pointed to someone else who made (afaik) the first public container for vllm on these chips. They pretty much did the hacks I was trying to finish, so it was validating to know that I was on the right track. 

Container Repo: https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes
Helpful build instructions for this specific combo: https://github.com/kyuz0/amd-strix-halo-pytorch-gfx1151-aotriton

If you want vllm specifically to work on these particular chips, this may be your best bet here. Or, if you're using a fancy linux flavor like me, your *only* option here lol. I wouldn't call it the easiest, but it's something. But also make sure to read what others have already mentioned and tried before pursuing this route. 

**A big note**: this build still doesn't support all models. Notably, it doesn't support the ones I actually care about using (gpt-oss), because the `triton_kernel` for MXFP4  isn't in the container build, which can't be migrated up with triton alone until other issues are fixed/resolved. 

I'm currently working on seeing/trying if I can inject the specific triton kernel here for gpt-oss models on this build to make them work. 

This, afaik, is the farthest edge of the current state of things on this topic.  Things are inching closer.  

---

### 评论 #45 — schung-amd (2025-09-26T14:39:33Z)

@waltercool Slight clarification, gfx1151 is officially supported now with ROCm 6.4.4; but of course if you have things working already I don't think there's a reason to switch (aside from curiosity). Great to see your updates and hopefully our torch build issues will be resolved soon.

@MachaLvl99 Glad to hear you have something working. I think you should be able to use TheRock as well if desired. Building from source may have some issues on exotic distros (e.g. https://github.com/ROCm/TheRock/issues/1135), and vLLM might not know where to find ROCm files if using the `pip install rocm` wheels, but if you're interested I think we can/should work through those issues at some point.

I'll be looking into verifying and documenting vLLM functionality on ROCm 6.4.4 and TheRock with gfx1151 to close out this issue when I get spare bandwidth to do so, hopefully next week. In the meanwhile any reports of things that are working and things that are broken with ROCm 6.4.4 (or TheRock, although those issues will get more visibility in TheRock itself) are greatly appreciated. I'm grateful to everyone in this thread for your patience and work toward getting this resolved, we're almost there.

---

### 评论 #46 — lhl (2025-09-28T09:43:48Z)

@MachaLvl99 @schung-amd since someone pointed me here, you can check out my original scripts for getting vLLM working here (I don't think anyone had actually sat down and slogged through the manifold build issues - among them amdsmi crapping the bed, @schung-amd or someone at AMD, plz fix): https://github.com/lhl/strix-halo-testing/tree/main/vllm

A couple notes - decent vLLM performance depends on a PyTorchb build w/ AOTriton otherwise gfx1151 won't have FA and perf will be even worse (does CK FA work? I've built CK in the past for gfx1151 but it failed last time I tried). I have build scripts for building your own PyTorch + aotriton that leverages TheRock torch build scripts, but with some additional fixes here: https://github.com/lhl/strix-halo-testing/tree/main/torch-therock

This also includes a very basic, but useful (IMO) [attention-bench](https://github.com/lhl/strix-halo-testing/blob/main/torch-therock/05-attention-bench.py) script that's modeled after [attention-gym](https://github.com/meta-pytorch/attention-gym)'s example/benchmark.py script

Note, while vLLM runs, a number of models don't run due to missing kernels, etc. @kyuz0 has a list of these here and is taking PRs for additional models/versions that don't work: https://github.com/kyuz0/amd-strix-halo-vllm-toolboxes?tab=readme-ov-file#tested-models-experimental-matrix

BTW, for those with issues getting gfx1151 running, I've had good luck w/ using a newer kernel (6.15+) and using TheRock nightlies (you can use the pip install but it installs stuff in weird places, or easier, just hunt down the latest gfx1151 nightly tarball and extract it to /opt/rocm) https://github.com/ROCm/TheRock/blob/main/RELEASES.md

---

### 评论 #47 — ndrewpj (2025-09-28T16:38:15Z)

> [@MachaLvl99](https://github.com/MachaLvl99) [@schung-amd](https://github.com/schung-amd) since someone pointed me here, you can check out my original scripts for getting vLLM working here (I don't think anyone had actually sat down and slogged through the manifold build issues - among them amdsmi crapping the bed, [@schung-amd](https://github.com/schung-amd) or someone at AMD, plz fix): https://github.com/lhl/strix-halo-testing/tree/main/vllm
> 
Hi and thank you for your scripts. I spent some hours (mostly due internet issues) today trying to build Vllm using them but because of current TheRock issue I couldn't. Also none of the torch nightlies worked. "Official" ROCm installed fine, tried the suggested by AMD versions for rocm7...  In the end Vllm was built but it won't start due to "unknown platform". gfx1151 was added, the sources were patched etc.

---

### 评论 #48 — schung-amd (2025-10-06T21:57:37Z)

Despite the ROCm on Ryzen docs stating no support for APUs with vLLM at this time, I was able to get vLLM running on gfx1151 with ROCm 6.4.4. Steps:

1. Ensure `linux-firmware` is up to date.
2. Install ROCm 6.4.4 following [ROCm on Ryzen instructions](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html).
3. Install Pytorch following [ROCm on Ryzen instructions](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-pytorch.html).
4. Build vLLM from source mostly following the [ROCm installation instructions, option 2](https://docs.vllm.ai/en/v0.6.5/getting_started/amd-installation.html).

I chose to install triton flash attention in step 1 of the vLLM build from source instructions, skipping step 2. In step 3, 

- Skip the torch reinstallation (as we already have the recommended wheels for ROCm on Ryzen)
- `pip install amdsmi==6.4.4` instead of `pip install /opt/rocm/share/amd_smi` as was running into an error with the latter
- `export PYTORCH_ROCM_ARCH="gfx1151"`

After that, I was able to perform inferencing with vLLM. I ran into GPU hangs without `--enforce-eager`, but not sure at this point if that's a limitation of the model I was using for testing or if this is generally required on gfx1151 at the moment. My priority here is getting vLLM running on TheRock now, I might look into further debug and testing with ROCm 6.4.4 at a later time.

> In the end Vllm was built but it won't start due to "unknown platform"

@ndrewpj I think this is due to a missing `amdsmi` module, try `pip install amdsmi` (or `pip install amdsmi==6.4.4` if using ROCm 6.4.4).

---

### 评论 #49 — Ali-Awad (2025-10-13T13:58:06Z)

> Despite the ROCm on Ryzen docs stating no support for APUs with vLLM at this time, I was able to get vLLM running on gfx1151 with ROCm 6.4.4. Steps:
> 
> 1. Ensure `linux-firmware` is up to date.
> 2. Install ROCm 6.4.4 following [ROCm on Ryzen instructions](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html).
> 3. Install Pytorch following [ROCm on Ryzen instructions](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-pytorch.html).
> 4. Build vLLM from source mostly following the [ROCm installation instructions, option 2](https://docs.vllm.ai/en/v0.6.5/getting_started/amd-installation.html).
> 
> I chose to install triton flash attention in step 1 of the vLLM build from source instructions, skipping step 2. In step 3,
> 
> * Skip the torch reinstallation (as we already have the recommended wheels for ROCm on Ryzen)
> * `pip install amdsmi==6.4.4` instead of `pip install /opt/rocm/share/amd_smi` as was running into an error with the latter
> * `export PYTORCH_ROCM_ARCH="gfx1151"`
> 
> After that, I was able to perform inferencing with vLLM. I ran into GPU hangs without `--enforce-eager`, but not sure at this point if that's a limitation of the model I was using for testing or if this is generally required on gfx1151 at the moment. My priority here is getting vLLM running on TheRock now, I might look into further debug and testing with ROCm 6.4.4 at a later time.
> 
> > In the end Vllm was built but it won't start due to "unknown platform"
> 
> [@ndrewpj](https://github.com/ndrewpj) I think this is due to a missing `amdsmi` module, try `pip install amdsmi` (or `pip install amdsmi==6.4.4` if using ROCm 6.4.4).

Can you please give infromation about the model you used and if poosible, the maximum achieveable tokens/s with parallel requests using Gemma 3 4b it GPTQ model? or at least the max t/s you achieved with your model with parallel requests.

---

### 评论 #50 — mveigel-softkomplett (2025-10-13T14:23:12Z)

@Ali-Awad Currently it seems to be better, to use llama.cpp with Vulkan, which uses more memory, but is much faster than rocm (currently).
I setup my Z2 with 4 llama.cpp processes, each hosting a different model for continue integration. Occupies 80% of the memory, but works quite well ...

---

### 评论 #51 — kyuz0 (2025-10-13T14:58:14Z)

> [@Ali-Awad](https://github.com/Ali-Awad) Currently it seems to be better, to use llama.cpp with Vulkan, which uses more memory, but is much faster than rocm (currently). I setup my Z2 with 4 llama.cpp processes, each hosting a different model for continue integration. Occupies 80% of the memory, but works quite well ...

That is not really the case anymore in most instances, llama.cpp with rocm+rocWMMA has comparable and often better performance than the Vulkan backend:

https://kyuz0.github.io/amd-strix-halo-toolboxes/

And currently there is active work in llama.cpp to write specific kernels for AMD GPUs, so in the next few months inference on gfx1151 might just get faster.

---

### 评论 #52 — mveigel-softkomplett (2025-10-13T15:09:22Z)

@kyuz0 Thanks for the information. For my models, this was the case (not as bad as in the beginning, but still a bit better with Vulkan).

To be honest, I was running your containers and they performed quite good, but a compiled Vulkan was slightly faster. And I know it doesn't fit to this thread, but two things about your containers:

- Congrats, Great work :)
- Is there a posibility to remove the vllm from the ComfyUI Container? Even with the 110 GB you could use on Strix Halo it is hard  to load other models



---

### 评论 #53 — ndrewpj (2025-10-13T15:34:34Z)

I was also curious - for those who managed to build Vllm with gfx1151 support - which models worked in this Vllm? I tried myself the models listed in the repo for amd strix halo Vllm toolbox. I only was successful with SmolLm, every other fp16 model gave me errors...

---

### 评论 #54 — kyuz0 (2025-10-13T16:05:56Z)

> * Is there a posibility to remove the vllm from the ComfyUI Container? Even with the 110 GB you could use on Strix Halo it is hard  to load other models

I think this is the toolbox with ComfyUI and it's different than the vLLM one, and much smaller:

https://github.com/kyuz0/amd-strix-halo-image-video-toolboxes


---

### 评论 #55 — Ali-Awad (2025-10-13T17:43:16Z)

> [@Ali-Awad](https://github.com/Ali-Awad) Currently it seems to be better, to use llama.cpp with Vulkan, which uses more memory, but is much faster than rocm (currently). I setup my Z2 with 4 llama.cpp processes, each hosting a different model for continue integration. Occupies 80% of the memory, but works quite well ...

llama.cpp doesn't support continuous batching or parallel request --> average throughput is way lower than vllm even if vllm is slower per a single request!!!

---

### 评论 #56 — Ali-Awad (2025-10-13T17:47:52Z)

> > [@Ali-Awad](https://github.com/Ali-Awad) Currently it seems to be better, to use llama.cpp with Vulkan, which uses more memory, but is much faster than rocm (currently). I setup my Z2 with 4 llama.cpp processes, each hosting a different model for continue integration. Occupies 80% of the memory, but works quite well ...
> 
> That is not really the case anymore in most instances, llama.cpp with rocm+rocWMMA has comparable and often better performance than the Vulkan backend:
> 
> https://kyuz0.github.io/amd-strix-halo-toolboxes/
> 
> And currently there is active work in llama.cpp to write specific kernels for AMD GPUs, so in the next few months inference on gfx1151 might just get faster.

Great work you have done with llama.cpp. I wonder of you were ever able to configure with vllm and what would the max throughput for parallel users on small models like the gemma 4b it. Thanks

---

### 评论 #57 — ChihayaK (2025-10-14T02:15:56Z)

Can confirm the latest nightly build of torch with vllm main branch works, but the capturing cuda graph failed with triton errors without hangs.
Using the `--enforce-eager` will load the model correctly without cuda graphs, the awq quants is working too.
But, it seems like moe models refuse to load at all, loading with awq will result awq_marlin error. Loading without quatization will just hang with no error or anything.
It is a good progress, keep up the good work.

Edit: It is still quite borken, the model will fail after ideling a while for no reason. Getting the error: `torch.AcceleratorError: HIP error: unspecified launch failure`

---

### 评论 #58 — Qubitium (2025-10-14T02:24:21Z)

> But, it seems like moe models refuse to load at all, loading with awq will result awq_marlin error. Loading without quatization will just hang with no error or anything.

Marlin kernels is only for Nvidia cuda gpus (not hipified) unless it was updated recently to expand to rocm support?

Please retry and use the other awq kernesl such as awq_gemm. Marlin kernel should not be selected for hipified cuda.

---

### 评论 #59 — ChihayaK (2025-10-14T02:46:30Z)

> Marlin kernels is only for Nvidia cuda gpus (not hipified) unless it was updated recently to expand to rocm support?
> 
> Please retry and use the other awq kernesl such as awq_gemm. Marlin kernel should not be selected for hipified cuda.

Yes, I think it does not supports amd gpus. But for some reason the vllm decided that it is ok to do awq moe with marlin kernels. 
And i am kinda not sure how to specify awq_gemm? I tried to patch the vllm code at `check_moe_marlin_supports_layer` to return false on amd platforms, but that ended up giving a bunch of other errors. 
So I think it is a moe specifc issue, or at least on qwen3 models(since normal awq without moe works). I will try older moe models later to see if this is a general moe issue or it is just qwen3-moe issue. 


---

### 评论 #60 — Qubitium (2025-10-14T07:11:59Z)

> > Marlin kernels is only for Nvidia cuda gpus (not hipified) unless it was updated recently to expand to rocm support?
> > Please retry and use the other awq kernesl such as awq_gemm. Marlin kernel should not be selected for hipified cuda.
> 
> Yes, I think it does not supports amd gpus. But for some reason the vllm decided that it is ok to do awq moe with marlin kernels. And i am kinda not sure how to specify awq_gemm? I tried to patch the vllm code at `check_moe_marlin_supports_layer` to return false on amd platforms, but that ended up giving a bunch of other errors. So I think it is a moe specifc issue, or at least on qwen3 models(since normal awq without moe works). I will try older moe models later to see if this is a general moe issue or it is just qwen3-moe issue.

If you can give me a full reproduction script, I can fix this in vllm In PR. But I need the full reproduction script to accelerate this erffort. Imho, this is vllm kernel selection bug. 

---

### 评论 #61 — ChihayaK (2025-10-15T02:45:27Z)

> If you can give me a full reproduction script, I can fix this in vllm In PR. But I need the full reproduction script to accelerate this erffort. Imho, this is vllm kernel selection bug.

Sorry for the late reply but here you go.

The following guide provides step-by-step instructions to reproduce an AWQ Marlin error when serving Qwen3-MoE AWQ models with vLLM on AMD GPUs.

---

## Step 1: Install AMD GPU Drivers

1. Download the AMDGPU install script from:
   - https://www.amd.com/en/support/download/linux-drivers.html

2. Follow the installation instructions at:
   - https://amdgpu-install.readthedocs.io/en/latest/install-script.html

---

## Step 2: Install ROCm 7.0 RC

Follow the installation guide for ROCm 7.0 RC:
- https://rocm.docs.amd.com/en/docs-7.0-rc1/preview/install/rocm.html

---

## Step 3: Clone and Set Up vLLM

### Clone the vLLM Repository
```bash
git clone https://github.com/vllm-project/vllm.git
cd vllm
```

### Create Virtual Environment
```bash
uv venv --python 3.12 --seed
source .venv/bin/activate
```

### Install PyTorch Nightly with ROCm 7.0 Support
```bash
pip3 install --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/rocm7.0
```

---

## Step 4: Install Triton

Follow the unsupported OS build instructions from:
- https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html#unsupported-os-build
```bash
python3 -m pip install ninja cmake wheel pybind11
pip uninstall -y triton

# Clone and install specific Triton version
git clone https://github.com/triton-lang/triton.git
cd triton
git checkout e5be006
if [ ! -f setup.py ]; then cd python; fi
python3 setup.py install
cd ../..
```

---

## Step 5: Build vLLM from Source

### Upgrade pip
```bash
pip install --upgrade pip
```

### Install AMD SMI
```bash
# Copy AMD SMI to avoid permission issues
cp -r /opt/rocm/share/amd_smi ./amd_smi
pip install ./amd_smi

# Alternative: pip install amdsmi
```

### Install Dependencies
```bash
pip install --upgrade numba \
    scipy \
    "huggingface-hub[cli,hf_transfer]" \
    setuptools_scm

pip install "numpy<2"
pip install -r requirements/rocm.txt
```

### Build vLLM for AMD GPU (gfx1151)
```bash
export PYTORCH_ROCM_ARCH="gfx1151"
python3 setup.py develop
```

---

## Step 6: Download AWQ Model

Download the Qwen3-30B-A3B-AWQ model (or similar Qwen3-MoE AWQ model):
```bash
huggingface-cli download QuixiAI/Qwen3-30B-A3B-AWQ
```

**Note:** This is an example model. The issue should occur with any Qwen3-MoE AWQ model due to the shared architecture.

---

## Step 7: Serve the Model

Run vLLM server with the AWQ model:
```bash
vllm serve QuixiAI/Qwen3-30B-A3B-AWQ
```

---

## Expected Result

The server will fail with an **AWQ Marlin error**.

---

### 评论 #62 — ianbmacdonald (2025-11-13T17:29:15Z)

Well, I think we can close off this based on the fact that the OPs scenario on Strix Halo is resolved. 

Here is a pre-built container that works

docker pull rocm/vllm-dev:preview7.1_1117_rc1_20251112


```
APIServer pid=233) INFO 11-13 17:18:48 [api_server.py:1961] vLLM API server version 0.11.1rc6.dev115+gbc926c122
(APIServer pid=233) INFO 11-13 17:18:48 [utils.py:253] non-default args: {'model_tag': 'Qwen/Qwen3-1.7B', 'model': 'Qwen/Qwen3-1.7B'}
(APIServer pid=233) INFO 11-13 17:18:52 [model.py:630] Resolved architecture: Qwen3ForCausalLM
(APIServer pid=233) INFO 11-13 17:18:52 [model.py:1728] Using max model len 40960
(APIServer pid=233) INFO 11-13 17:18:53 [scheduler.py:226] Chunked prefill is enabled with max_num_batched_tokens=8192.
(APIServer pid=233) WARNING 11-13 17:18:53 [vllm.py:576] No piecewise cudagraph for executing cascade attention. Will fall back to eager execution if a batch runs into cascade attentions
(EngineCore_DP0 pid=375) INFO 11-13 17:18:57 [core.py:93] Initializing a V1 LLM engine (v0.11.1rc6.dev115+gbc926c122) with config: model='Qwen/Qwen3-1.7B', speculative_config=None, tokenizer='Qwen/Qwen3-1.7B', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=40960, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, disable_custom_all_reduce=True, quantization=None, enforce_eager=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None), seed=0, served_model_name=Qwen/Qwen3-1.7B, enable_prefix_caching=True, chunked_prefill_enabled=True, pooler_config=None, compilation_config={'level': None, 'mode': 3, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['+rms_norm', '+silu_and_mul', '+quant_fp8', 'none'], 'splitting_ops': [], 'use_inductor': None, 'compile_sizes': [], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL: 2>, 'use_cudagraph': True, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496, 512], 'cudagraph_copy_inputs': False, 'full_cuda_graph': True, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {}, 'max_cudagraph_capture_size': 512, 'local_cache_dir': None}
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
(EngineCore_DP0 pid=375) INFO 11-13 17:18:57 [parallel_state.py:1325] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, TP rank 0, EP rank 0
(EngineCore_DP0 pid=375) INFO 11-13 17:18:58 [gpu_model_runner.py:2932] Starting to load model Qwen/Qwen3-1.7B...
(EngineCore_DP0 pid=375) INFO 11-13 17:18:58 [rocm.py:292] Using Rocm Attention backend.
(EngineCore_DP0 pid=375) WARNING 11-13 17:18:58 [compilation.py:908] Op 'quant_fp8' not present in model, enabling with '+quant_fp8' has no effect
Loading safetensors checkpoint shards:   0% Completed | 0/2 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:  50% Completed | 1/2 [00:00<00:00,  1.65it/s]
Loading safetensors checkpoint shards: 100% Completed | 2/2 [00:00<00:00,  3.30it/s]
(EngineCore_DP0 pid=375) 
(EngineCore_DP0 pid=375) INFO 11-13 17:18:59 [default_loader.py:314] Loading weights took 0.67 seconds
(EngineCore_DP0 pid=375) INFO 11-13 17:19:00 [gpu_model_runner.py:2997] Model loading took 3.3033 GiB and 1.237473 seconds
(EngineCore_DP0 pid=375) /usr/local/lib/python3.12/dist-packages/torch/_dynamo/variables/functions.py:1652: UserWarning: Dynamo detected a call to a `functools.lru_cache`-wrapped function. Dynamo ignores the cache wrapper and directly traces the wrapped function. Silent incorrectness is only a *potential* risk, not something we have observed. Enable TORCH_LOGS="+dynamo" for a DEBUG stack trace.
(EngineCore_DP0 pid=375)   torch._dynamo.utils.warn_once(msg)
(EngineCore_DP0 pid=375) INFO 11-13 17:19:04 [backends.py:620] Using cache directory: /root/.cache/vllm/torch_compile_cache/144895986d/rank_0_0/backbone for vLLM's torch.compile
(EngineCore_DP0 pid=375) INFO 11-13 17:19:04 [backends.py:636] Dynamo bytecode transform time: 3.68 s
(EngineCore_DP0 pid=375) INFO 11-13 17:19:16 [backends.py:250] Cache the graph for dynamic shape for later use
(EngineCore_DP0 pid=375) INFO 11-13 17:19:16 [backends.py:281] Compiling a graph for dynamic shape takes 11.99 s
(EngineCore_DP0 pid=375) INFO 11-13 17:19:16 [monitor.py:34] torch.compile takes 15.68 s in total
(EngineCore_DP0 pid=375) INFO 11-13 17:19:20 [gpu_worker.py:348] Available KV cache memory: 98.89 GiB
(EngineCore_DP0 pid=375) INFO 11-13 17:19:20 [kv_cache_utils.py:1229] GPU KV cache size: 925,792 tokens
(EngineCore_DP0 pid=375) INFO 11-13 17:19:20 [kv_cache_utils.py:1234] Maximum concurrency for 40,960 tokens per request: 22.60x
Capturing CUDA graphs (mixed prefill-decode, FULL): 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 51/51 [00:12<00:00,  4.03it/s]
(EngineCore_DP0 pid=375) INFO 11-13 17:19:39 [gpu_model_runner.py:3925] Graph capturing finished in 14 secs, took 0.20 GiB
(EngineCore_DP0 pid=375) INFO 11-13 17:19:40 [core.py:258] init engine (profile, create kv cache, warmup model) took 40.28 seconds
(EngineCore_DP0 pid=375) WARNING 11-13 17:19:41 [core.py:131] Using configured V1 scheduler class vllm.v1.core.sched.async_scheduler.AsyncScheduler. This scheduler interface is not public and compatibility may not be maintained.
(EngineCore_DP0 pid=375) INFO 11-13 17:19:41 [core.py:196] Batch queue is enabled with size 2
(EngineCore_DP0 pid=375) WARNING 11-13 17:19:41 [compilation.py:798] Using piecewise compilation with empty splitting_ops
(EngineCore_DP0 pid=375) WARNING 11-13 17:19:41 [vllm.py:576] No piecewise cudagraph for executing cascade attention. Will fall back to eager execution if a batch runs into cascade attentions
(APIServer pid=233) INFO 11-13 17:19:41 [api_server.py:1726] Supported tasks: ['generate']
(APIServer pid=233) WARNING 11-13 17:19:41 [model.py:1558] Default sampling parameters have been overridden by the model's Hugging Face generation config recommended from the model creator. If this is not intended, please relaunch vLLM instance with `--generation-config vllm`.
(APIServer pid=233) INFO 11-13 17:19:41 [serving_responses.py:167] Using default chat sampling params from model: {'temperature': 0.6, 'top_k': 20, 'top_p': 0.95}
(APIServer pid=233) INFO 11-13 17:19:41 [serving_chat.py:127] Using default chat sampling params from model: {'temperature': 0.6, 'top_k': 20, 'top_p': 0.95}
(APIServer pid=233) INFO 11-13 17:19:41 [serving_completion.py:68] Using default completion sampling params from model: {'temperature': 0.6, 'top_k': 20, 'top_p': 0.95}
(APIServer pid=233) INFO 11-13 17:19:41 [serving_chat.py:127] Using default chat sampling params from model: {'temperature': 0.6, 'top_k': 20, 'top_p': 0.95}
(APIServer pid=233) INFO 11-13 17:19:41 [api_server.py:2030] Starting vLLM API server 0 on http://0.0.0.0:8000
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:38] Available routes are:
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /openapi.json, Methods: GET, HEAD
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /docs, Methods: GET, HEAD
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /docs/oauth2-redirect, Methods: GET, HEAD
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /redoc, Methods: GET, HEAD
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /health, Methods: GET
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /load, Methods: GET
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /ping, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /ping, Methods: GET
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /tokenize, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /detokenize, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/models, Methods: GET
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /version, Methods: GET
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/responses, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/responses/{response_id}, Methods: GET
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/responses/{response_id}/cancel, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/messages, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/chat/completions, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/completions, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/embeddings, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /pooling, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /classify, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /score, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/score, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/audio/transcriptions, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/audio/translations, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /rerank, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v1/rerank, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /v2/rerank, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /scale_elastic_ep, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /is_scaling_elastic_ep, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /invocations, Methods: POST
(APIServer pid=233) INFO 11-13 17:19:41 [launcher.py:46] Route: /metrics, Methods: GET
(APIServer pid=233) INFO:     Started server process [233]
(APIServer pid=233) INFO:     Waiting for application startup.
(APIServer pid=233) INFO:     Application startup complete.


+------------------------------------------------------------------------------+
| AMD-SMI 26.1.0+5df6c765      amdgpu version: 6.16.6   ROCm version: 7.1.0    |
| VBIOS version: 00107962                                                      |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:c5:00.0    AMD Radeon Graphics | N/A        N/A   0             N/A/0 W |
|   0       0     N/A             N/A | N/A        N/A              161/512 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
```
AWQ Marlin is a separate issue.   AITer path for gfx1151 is disabled currently, unless you override it.  For vLLM 0.11.1, it will always end up as `Unknown GPU architecture: gfx1151`   or  `AttributeError: '_OpNamespace' '_C' object has no attribute 'awq_marlin_repack'`  if you rebuild it enabled, or use an override env. 

---

### 评论 #63 — schung-amd (2025-11-13T18:15:08Z)

Great, thanks for verifying! We'll close this for now as gfx1151 support has improved substantially since the original issue submission and we now have multiple working configs for using vLLM on this hardware. If anyone encounters further issues with gfx1151 + vLLM, feel free to continue discussing here or submit a new issue.

---
