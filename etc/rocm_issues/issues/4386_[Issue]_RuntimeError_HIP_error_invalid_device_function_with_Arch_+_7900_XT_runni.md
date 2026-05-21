# [Issue]: "RuntimeError: HIP error: invalid device function" with Arch + 7900 XT running vllm through docker

> **Issue #4386**
> **状态**: closed
> **创建时间**: 2025-02-17T14:06:10Z
> **更新时间**: 2025-02-26T01:53:50Z
> **关闭时间**: 2025-02-26T01:53:49Z
> **作者**: djkato
> **标签**: Under Investigation, AMD Radeon RX 7900 XT, ROCm 6.3.2
> **URL**: https://github.com/ROCm/ROCm/issues/4386

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.3.2** (颜色: #ededed)

## 描述

### Problem Description

Tried following this guide: https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/inference/vllm-benchmark.html#vllm-benchmark-standalone
But ran into an issue where I can't get any tag of those docker images working.

docker command:
```bash
docker run -it --device=/dev/kfd --device=/dev/dri --group-add video --shm-size 18G --security-opt seccomp=unconfined --security-opt apparmor=unconfined --cap-add=SYS_PTRACE -v $(pwd):/workspace --env HUGGINGFACE_HUB_CACHE=/workspace --name vllm_v0.6.6 rocm/vllm:rocm6.3.1_mi300_ubuntu22.04_py3.12_vllm_0.6.6
```

 The output log from vllm:
```
$: docker exec -it vllm_v0.6.6 /bin/bash
root@ad54d89eebde:/app# vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
INFO 02-17 13:41:21 __init__.py:179] Automatically detected platform rocm.
WARNING 02-17 13:41:21 rocm.py:34] `fork` method is not supported by ROCm. VLLM_WORKER_MULTIPROC_METHOD is overridden to `spawn` instead.
INFO 02-17 13:41:22 api_server.py:768] vLLM API server version 0.6.7.dev220+g84f5d47b
INFO 02-17 13:41:22 api_server.py:769] args: Namespace(subparser='serve', model_tag='deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', config='', host=None, port=8000, uvicorn_log_level='info', allow_credentials=False, allowed_origins=['*'], allowed_methods=['*'], allowed_headers=['*'], api_key=None, lora_modules=None, prompt_adapters=None, chat_template=None, chat_template_content_format='auto', response_role='assistant', ssl_keyfile=None, ssl_certfile=None, ssl_ca_certs=None, ssl_cert_reqs=0, root_path=None, middleware=[], return_tokens_as_token_ids=False, disable_frontend_multiprocessing=False, enable_request_id_headers=False, enable_auto_tool_choice=False, tool_call_parser=None, tool_parser_plugin='', model='deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', task='auto', tokenizer=None, skip_tokenizer_init=False, revision=None, code_revision=None, tokenizer_revision=None, tokenizer_mode='auto', trust_remote_code=False, allowed_local_media_path=None, download_dir=None, load_format='auto', config_format=<ConfigFormat.AUTO: 'auto'>, dtype='auto', kv_cache_dtype='auto', max_model_len=None, guided_decoding_backend='xgrammar', logits_processor_pattern=None, distributed_executor_backend=None, worker_use_ray=False, pipeline_parallel_size=1, tensor_parallel_size=1, max_parallel_loading_workers=None, ray_workers_use_nsight=False, block_size=None, enable_prefix_caching=None, disable_sliding_window=False, use_v2_block_manager=True, num_lookahead_slots=0, seed=0, swap_space=4, cpu_offload_gb=0, gpu_memory_utilization=0.9, num_gpu_blocks_override=None, max_num_batched_tokens=None, max_num_seqs=None, max_logprobs=20, disable_log_stats=False, quantization=None, rope_scaling=None, rope_theta=None, hf_overrides=None, enforce_eager=False, max_seq_len_to_capture=8192, disable_custom_all_reduce=False, tokenizer_pool_size=0, tokenizer_pool_type='ray', tokenizer_pool_extra_config=None, limit_mm_per_prompt=None, mm_processor_kwargs=None, disable_mm_preprocessor_cache=False, enable_lora=False, enable_lora_bias=False, max_loras=1, max_lora_rank=16, lora_extra_vocab_size=256, lora_dtype='auto', long_lora_scaling_factors=None, max_cpu_loras=None, fully_sharded_loras=False, enable_prompt_adapter=False, max_prompt_adapters=1, max_prompt_adapter_token=0, device='auto', num_scheduler_steps=1, multi_step_stream_outputs=True, scheduler_delay_factor=0.0, enable_chunked_prefill=None, speculative_model=None, speculative_model_quantization=None, num_speculative_tokens=None, speculative_disable_mqa_scorer=False, speculative_draft_tensor_parallel_size=None, speculative_max_model_len=None, speculative_disable_by_batch_size=None, ngram_prompt_lookup_max=None, ngram_prompt_lookup_min=None, spec_decoding_acceptance_method='rejection_sampler', typical_acceptance_sampler_posterior_threshold=None, typical_acceptance_sampler_posterior_alpha=None, disable_logprobs_during_spec_decoding=None, model_loader_extra_config=None, ignore_patterns=[], preemption_mode=None, served_model_name=None, qlora_adapter_name_or_path=None, otlp_traces_endpoint=None, collect_detailed_traces=None, disable_async_output_proc=False, scheduling_policy='fcfs', override_neuron_config=None, override_pooler_config=None, compilation_config=None, kv_transfer_config=None, worker_cls='auto', generation_config=None, calculate_kv_scales=False, disable_log_requests=False, max_log_len=None, disable_fastapi_docs=False, enable_prompt_tokens_details=False, dispatch_function=<function serve at 0x7cbd2713ca40>)
INFO 02-17 13:41:22 api_server.py:195] Started engine process with PID 48
config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 679/679 [00:00<00:00, 9.82MB/s]
INFO 02-17 13:41:24 __init__.py:179] Automatically detected platform rocm.
INFO 02-17 13:41:32 config.py:513] This model supports multiple tasks: {'generate', 'classify', 'score', 'reward', 'embed'}. Defaulting to 'generate'.
INFO 02-17 13:41:32 config.py:513] This model supports multiple tasks: {'score', 'generate', 'embed', 'classify', 'reward'}. Defaulting to 'generate'.
INFO 02-17 13:41:34 config.py:1340] Disabled the custom all-reduce kernel because it is not working correctly when using two AMD Navi GPUs.
INFO 02-17 13:41:34 config.py:1352] Disabled the custom all-reduce kernel because it is not working correctly when using two AMD Navi GPUs.
WARNING 02-17 13:41:34 arg_utils.py:1111] The model has a long context length (131072). This may cause OOM errors during the initial memory profiling phase, or result in low performance due to small KV cache space. Consider setting --max-model-len to a smaller value.
tokenizer_config.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3.07k/3.07k [00:00<00:00, 48.8MB/s]
INFO 02-17 13:41:35 config.py:1340] Disabled the custom all-reduce kernel because it is not working correctly when using two AMD Navi GPUs.
INFO 02-17 13:41:35 config.py:1352] Disabled the custom all-reduce kernel because it is not working correctly when using two AMD Navi GPUs.
WARNING 02-17 13:41:35 arg_utils.py:1111] The model has a long context length (131072). This may cause OOM errors during the initial memory profiling phase, or result in low performance due to small KV cache space. Consider setting --max-model-len to a smaller value.
INFO 02-17 13:41:35 engine.py:72] Initializing an LLM engine (v0.6.7.dev220+g84f5d47b) with config: model='deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', speculative_config=None, tokenizer='deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, override_neuron_config=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=131072, download_dir=None, load_format=LoadFormat.AUTO, tensor_parallel_size=1, pipeline_parallel_size=1, disable_custom_all_reduce=True, quantization=None, enforce_eager=False, kv_cache_dtype=auto,  device_config=cuda, decoding_config=DecodingConfig(guided_decoding_backend='xgrammar'), observability_config=ObservabilityConfig(otlp_traces_endpoint=None, collect_model_forward_time=False, collect_model_execute_time=False), seed=0, served_model_name=deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B, num_scheduler_steps=1, multi_step_stream_outputs=True, enable_prefix_caching=False, chunked_prefill_enabled=False, use_async_output_proc=True, disable_mm_preprocessor_cache=False, mm_processor_kwargs=None, pooler_config=None, compilation_config={"splitting_ops":[],"candidate_compile_sizes":[],"compile_sizes":[],"capture_sizes":[256,248,240,232,224,216,208,200,192,184,176,168,160,152,144,136,128,120,112,104,96,88,80,72,64,56,48,40,32,24,16,8,4,2,1],"max_capture_size":256}, use_cached_outputs=True, 
tokenizer.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7.03M/7.03M [00:00<00:00, 9.21MB/s]
generation_config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 181/181 [00:00<00:00, 3.07MB/s]
INFO 02-17 13:41:37 rocm.py:124] None is not supported in AMD GPUs.
INFO 02-17 13:41:37 rocm.py:125] Using ROCmFlashAttention backend.
INFO 02-17 13:41:37 model_runner.py:1095] Starting to load model deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B...
WARNING 02-17 13:41:37 rocm.py:211] Model architecture 'Qwen2ForCausalLM' is partially supported by ROCm: Sliding window attention (SWA) is not yet supported in Triton flash attention. For half-precision SWA support, please use CK flash attention by setting `VLLM_USE_TRITON_FLASH_ATTN=0`
ERROR 02-17 13:41:38 engine.py:381] HIP error: invalid device function
ERROR 02-17 13:41:38 engine.py:381] HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
ERROR 02-17 13:41:38 engine.py:381] For debugging consider passing AMD_SERIALIZE_KERNEL=3
ERROR 02-17 13:41:38 engine.py:381] Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
ERROR 02-17 13:41:38 engine.py:381] Traceback (most recent call last):
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 372, in run_mp_engine
ERROR 02-17 13:41:38 engine.py:381]     engine = MQLLMEngine.from_engine_args(engine_args=engine_args,
ERROR 02-17 13:41:38 engine.py:381]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 120, in from_engine_args
ERROR 02-17 13:41:38 engine.py:381]     return cls(ipc_path=ipc_path,
ERROR 02-17 13:41:38 engine.py:381]            ^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 72, in __init__
ERROR 02-17 13:41:38 engine.py:381]     self.engine = LLMEngine(*args, **kwargs)
ERROR 02-17 13:41:38 engine.py:381]                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "vllm/engine/llm_engine.py", line 271, in vllm.engine.llm_engine.LLMEngine.__init__
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/executor/executor_base.py", line 49, in __init__
ERROR 02-17 13:41:38 engine.py:381]     self._init_executor()
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/executor/uniproc_executor.py", line 40, in _init_executor
ERROR 02-17 13:41:38 engine.py:381]     self.collective_rpc("load_model")
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/executor/uniproc_executor.py", line 49, in collective_rpc
ERROR 02-17 13:41:38 engine.py:381]     answer = run_method(self.driver_worker, method, args, kwargs)
ERROR 02-17 13:41:38 engine.py:381]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "vllm/utils.py", line 2379, in vllm.utils.run_method
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/worker/worker.py", line 182, in load_model
ERROR 02-17 13:41:38 engine.py:381]     self.model_runner.load_model()
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/worker/model_runner.py", line 1097, in load_model
ERROR 02-17 13:41:38 engine.py:381]     self.model = get_model(vllm_config=self.vllm_config)
ERROR 02-17 13:41:38 engine.py:381]                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/__init__.py", line 12, in get_model
ERROR 02-17 13:41:38 engine.py:381]     return loader.load_model(vllm_config=vllm_config)
ERROR 02-17 13:41:38 engine.py:381]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/loader.py", line 376, in load_model
ERROR 02-17 13:41:38 engine.py:381]     model = _initialize_model(vllm_config=vllm_config)
ERROR 02-17 13:41:38 engine.py:381]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/loader.py", line 118, in _initialize_model
ERROR 02-17 13:41:38 engine.py:381]     return model_class(vllm_config=vllm_config, prefix=prefix)
ERROR 02-17 13:41:38 engine.py:381]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/qwen2.py", line 451, in __init__
ERROR 02-17 13:41:38 engine.py:381]     self.model = Qwen2Model(vllm_config=vllm_config,
ERROR 02-17 13:41:38 engine.py:381]                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/decorators.py", line 149, in __init__
ERROR 02-17 13:41:38 engine.py:381]     old_init(self, vllm_config=vllm_config, prefix=prefix, **kwargs)
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/qwen2.py", line 305, in __init__
ERROR 02-17 13:41:38 engine.py:381]     self.start_layer, self.end_layer, self.layers = make_layers(
ERROR 02-17 13:41:38 engine.py:381]                                                     ^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/utils.py", line 556, in make_layers
ERROR 02-17 13:41:38 engine.py:381]     maybe_offload_to_cpu(layer_fn(prefix=f"{prefix}.{idx}"))
ERROR 02-17 13:41:38 engine.py:381]                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/qwen2.py", line 307, in <lambda>
ERROR 02-17 13:41:38 engine.py:381]     lambda prefix: Qwen2DecoderLayer(config=config,
ERROR 02-17 13:41:38 engine.py:381]                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/qwen2.py", line 206, in __init__
ERROR 02-17 13:41:38 engine.py:381]     self.self_attn = Qwen2Attention(
ERROR 02-17 13:41:38 engine.py:381]                      ^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/qwen2.py", line 151, in __init__
ERROR 02-17 13:41:38 engine.py:381]     self.rotary_emb = get_rope(
ERROR 02-17 13:41:38 engine.py:381]                       ^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 1008, in get_rope
ERROR 02-17 13:41:38 engine.py:381]     rotary_emb = RotaryEmbedding(head_size, rotary_dim, max_position, base,
ERROR 02-17 13:41:38 engine.py:381]                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 95, in __init__
ERROR 02-17 13:41:38 engine.py:381]     cache = self._compute_cos_sin_cache()
ERROR 02-17 13:41:38 engine.py:381]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 112, in _compute_cos_sin_cache
ERROR 02-17 13:41:38 engine.py:381]     inv_freq = self._compute_inv_freq(self.base)
ERROR 02-17 13:41:38 engine.py:381]                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 106, in _compute_inv_freq
ERROR 02-17 13:41:38 engine.py:381]     inv_freq = 1.0 / (base**(torch.arange(
ERROR 02-17 13:41:38 engine.py:381]                              ^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381]   File "/usr/local/lib/python3.12/dist-packages/torch/utils/_device.py", line 104, in __torch_function__
ERROR 02-17 13:41:38 engine.py:381]     return func(*args, **kwargs)
ERROR 02-17 13:41:38 engine.py:381]            ^^^^^^^^^^^^^^^^^^^^^
ERROR 02-17 13:41:38 engine.py:381] RuntimeError: HIP error: invalid device function
ERROR 02-17 13:41:38 engine.py:381] HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
ERROR 02-17 13:41:38 engine.py:381] For debugging consider passing AMD_SERIALIZE_KERNEL=3
ERROR 02-17 13:41:38 engine.py:381] Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
ERROR 02-17 13:41:38 engine.py:381] 
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/usr/lib/python3.12/multiprocessing/process.py", line 314, in _bootstrap
    self.run()
  File "/usr/lib/python3.12/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 383, in run_mp_engine
    raise e
  File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 372, in run_mp_engine
    engine = MQLLMEngine.from_engine_args(engine_args=engine_args,
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 120, in from_engine_args
    return cls(ipc_path=ipc_path,
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/engine/multiprocessing/engine.py", line 72, in __init__
    self.engine = LLMEngine(*args, **kwargs)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "vllm/engine/llm_engine.py", line 271, in vllm.engine.llm_engine.LLMEngine.__init__
  File "/usr/local/lib/python3.12/dist-packages/vllm/executor/executor_base.py", line 49, in __init__
    self._init_executor()
  File "/usr/local/lib/python3.12/dist-packages/vllm/executor/uniproc_executor.py", line 40, in _init_executor
    self.collective_rpc("load_model")
  File "/usr/local/lib/python3.12/dist-packages/vllm/executor/uniproc_executor.py", line 49, in collective_rpc
    answer = run_method(self.driver_worker, method, args, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "vllm/utils.py", line 2379, in vllm.utils.run_method
  File "/usr/local/lib/python3.12/dist-packages/vllm/worker/worker.py", line 182, in load_model
    self.model_runner.load_model()
  File "/usr/local/lib/python3.12/dist-packages/vllm/worker/model_runner.py", line 1097, in load_model
    self.model = get_model(vllm_config=self.vllm_config)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/__init__.py", line 12, in get_model
    return loader.load_model(vllm_config=vllm_config)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/loader.py", line 376, in load_model
    model = _initialize_model(vllm_config=vllm_config)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/model_loader/loader.py", line 118, in _initialize_model
    return model_class(vllm_config=vllm_config, prefix=prefix)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/qwen2.py", line 451, in __init__
    self.model = Qwen2Model(vllm_config=vllm_config,
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/compilation/decorators.py", line 149, in __init__
    old_init(self, vllm_config=vllm_config, prefix=prefix, **kwargs)
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/qwen2.py", line 305, in __init__
    self.start_layer, self.end_layer, self.layers = make_layers(
                                                    ^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/utils.py", line 556, in make_layers
    maybe_offload_to_cpu(layer_fn(prefix=f"{prefix}.{idx}"))
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/qwen2.py", line 307, in <lambda>
    lambda prefix: Qwen2DecoderLayer(config=config,
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/qwen2.py", line 206, in __init__
    self.self_attn = Qwen2Attention(
                     ^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/models/qwen2.py", line 151, in __init__
    self.rotary_emb = get_rope(
                      ^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 1008, in get_rope
    rotary_emb = RotaryEmbedding(head_size, rotary_dim, max_position, base,
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 95, in __init__
    cache = self._compute_cos_sin_cache()
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 112, in _compute_cos_sin_cache
    inv_freq = self._compute_inv_freq(self.base)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/rotary_embedding.py", line 106, in _compute_inv_freq
    inv_freq = 1.0 / (base**(torch.arange(
                             ^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/torch/utils/_device.py", line 104, in __torch_function__
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

[rank0]:[W217 13:41:38.699860505 ProcessGroupNCCL.cpp:1487] Warning: WARNING: destroy_process_group() was not called before program exit, which can leak resources. For more info, please see https://pytorch.org/docs/stable/distributed.html#shutdown (function operator())
Traceback (most recent call last):
  File "/usr/local/bin/vllm", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/scripts.py", line 201, in main
    args.dispatch_function(args)
  File "/usr/local/lib/python3.12/dist-packages/vllm/scripts.py", line 42, in serve
    uvloop.run(run_server(args))
  File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 109, in run
    return __asyncio.run(
           ^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 194, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
  File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 61, in wrapper
    return await main
           ^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 796, in run_server
    async with build_async_engine_client(args) as engine_client:
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 125, in build_async_engine_client
    async with build_async_engine_client_from_engine_args(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 219, in build_async_engine_client_from_engine_args
    raise RuntimeError(
RuntimeError: Engine process failed to start. See stack trace for the root cause.
```

### Operating System

EndeavourOS 6.13.2-arch1-1

### CPU

AMD Ryzen 7 7700X

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

AUR/opencl-amd 1:6.3.2-1

### ROCm Component

_No response_

### Steps to Reproduce

```bash
docker run -it --device=/dev/kfd --device=/dev/dri --group-add video --shm-size 18G --security-opt seccomp=unconfined --security-opt apparmor=unconfined --cap-add=SYS_PTRACE -v $(pwd):/workspace --env HUGGINGFACE_HUB_CACHE=/workspace --name vllm_v0.6.6 rocm/vllm:rocm6.3.1_mi300_ubuntu22.04_py3.12_vllm_0.6.6
```
start it:
```bash
docker start vllm_v0.6.6
docker exec -it vllm_v0.6.6 /bin/bash
```
Inside docker container:
```bash
vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
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
  Name:                    AMD Ryzen 7 7700X 8-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7700X 8-Core Processor 
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
  Max Clock Freq. (MHz):   5573                               
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
      Size:                    31978104(0x1e7f278) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    31978104(0x1e7f278) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    31978104(0x1e7f278) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31978104(0x1e7f278) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-ae21e53268ec7fab               
  Marketing Name:          AMD Radeon RX 7900 XT              
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
    L2:                      6144(0x1800) KB                    
    L3:                      81920(0x14000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2025                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            84                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
  Packet Processor uCode:: 522                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    20955136(0x13fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    20955136(0x13fc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1100         
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx1036                            
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
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      256(0x100) KB                      
  Chip ID:                 5710(0x164e)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   3584                               
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
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
  Packet Processor uCode:: 21                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    15989052(0xf3f93c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    15989052(0xf3f93c) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1036         
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

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-02-18T15:10:42Z)

Hi @djkato. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — darren-amd (2025-02-24T19:14:46Z)

Hi @djkato,

I was able to reproduce your issue by following the guide linked. However, the docker container in that guide is for MI300X, which would not work on gfx1100. I tried using a nightly docker container for Navi, available [here](https://hub.docker.com/r/rocm/vllm-dev/tags), and was able to launch the model successfully on a 7900 XT machine. Below is what I ran:

```
sudo docker run -it --network=host --group-add=video --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device /dev/kfd --device /dev/dri rocm/vllm-dev:navi_nightly_main_20250224

vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
```

Give that a try and let me know if you run into any issues, thanks!

---

### 评论 #3 — djkato (2025-02-26T01:53:49Z)

@darren-amd thank you, I got it working with that other docker image.
didn't expect there to be such a strict requirement for gpu type, but alas.


---
