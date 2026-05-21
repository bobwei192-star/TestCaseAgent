# [Issue]: ROCm 6.3.x driver failed on fips enabled system with _hashlib.UnsupportedDigestmodError

> **Issue #4475**
> **状态**: closed
> **创建时间**: 2025-03-10T18:57:38Z
> **更新时间**: 2025-03-10T18:59:50Z
> **关闭时间**: 2025-03-10T18:59:14Z
> **作者**: tarukumar
> **标签**: ROCm 6.3.1
> **URL**: https://github.com/ROCm/ROCm/issues/4475

## 标签

- **ROCm 6.3.1** (颜色: #ededed)

## 描述

### Problem Description

When deploying the model of vllm runtime whihc is build on 6.3.1 rocm version it fails to deploy with below error because the cluster was fips enabled:

```makefile
WARNING 03-06 14:06:33 rocm.py:31] `fork` method is not supported by ROCm. VLLM_WORKER_MULTIPROC_METHOD is overridden to `spawn` instead.
INFO 03-06 14:06:35 api_server.py:199] Started engine process with PID 76
ERROR 03-06 14:06:50 registry.py:327] Error in inspecting model architecture 'GraniteForCausalLM'
ERROR 03-06 14:06:50 registry.py:327] Traceback (most recent call last):
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/vllm/model_executor/models/registry.py", line 522, in _run_in_subprocess
ERROR 03-06 14:06:50 registry.py:327]     returned.check_returncode()
ERROR 03-06 14:06:50 registry.py:327]   File "/usr/lib64/python3.12/subprocess.py", line 502, in check_returncode
ERROR 03-06 14:06:50 registry.py:327]     raise CalledProcessError(self.returncode, self.args, self.stdout,
ERROR 03-06 14:06:50 registry.py:327] subprocess.CalledProcessError: Command '['/opt/vllm/bin/python3', '-m', 'vllm.model_executor.models.registry']' returned non-zero exit status 1.
ERROR 03-06 14:06:50 registry.py:327] 
ERROR 03-06 14:06:50 registry.py:327] The above exception was the direct cause of the following exception:
ERROR 03-06 14:06:50 registry.py:327] 
ERROR 03-06 14:06:50 registry.py:327] Traceback (most recent call last):
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/vllm/model_executor/models/registry.py", line 325, in _try_inspect_model_cls
ERROR 03-06 14:06:50 registry.py:327]     return model.inspect_model_cls()
ERROR 03-06 14:06:50 registry.py:327]            ^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/vllm/model_executor/models/registry.py", line 287, in inspect_model_cls
ERROR 03-06 14:06:50 registry.py:327]     return _run_in_subprocess(
ERROR 03-06 14:06:50 registry.py:327]            ^^^^^^^^^^^^^^^^^^^
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/vllm/model_executor/models/registry.py", line 525, in _run_in_subprocess
ERROR 03-06 14:06:50 registry.py:327]     raise RuntimeError(f"Error raised in subprocess:\n"
ERROR 03-06 14:06:50 registry.py:327] RuntimeError: Error raised in subprocess:
ERROR 03-06 14:06:50 registry.py:327] <frozen runpy>:128: RuntimeWarning: 'vllm.model_executor.models.registry' found in sys.modules after import of package 'vllm.model_executor.models', but prior to execution of 'vllm.model_executor.models.registry'; this may result in unpredictable behaviour
ERROR 03-06 14:06:50 registry.py:327] Traceback (most recent call last):
ERROR 03-06 14:06:50 registry.py:327]   File "<frozen runpy>", line 198, in _run_module_as_main
ERROR 03-06 14:06:50 registry.py:327]   File "<frozen runpy>", line 88, in _run_code
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/vllm/model_executor/models/registry.py", line 546, in <module>
ERROR 03-06 14:06:50 registry.py:327]     _run()
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/vllm/model_executor/models/registry.py", line 539, in _run
ERROR 03-06 14:06:50 registry.py:327]     result = fn()
ERROR 03-06 14:06:50 registry.py:327]              ^^^^
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/vllm/model_executor/models/registry.py", line 288, in <lambda>
ERROR 03-06 14:06:50 registry.py:327]     lambda: _ModelInfo.from_model_cls(self.load_model_cls()))
ERROR 03-06 14:06:50 registry.py:327]                                       ^^^^^^^^^^^^^^^^^^^^^
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/vllm/model_executor/models/registry.py", line 291, in load_model_cls
ERROR 03-06 14:06:50 registry.py:327]     mod = importlib.import_module(self.module_name)
ERROR 03-06 14:06:50 registry.py:327]           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-06 14:06:50 registry.py:327]   File "/usr/lib64/python3.12/importlib/__init__.py", line 90, in import_module
ERROR 03-06 14:06:50 registry.py:327]     return _bootstrap._gcd_import(name[level:], package, level)
ERROR 03-06 14:06:50 registry.py:327]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-06 14:06:50 registry.py:327]   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
ERROR 03-06 14:06:50 registry.py:327]   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
ERROR 03-06 14:06:50 registry.py:327]   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
ERROR 03-06 14:06:50 registry.py:327]   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
ERROR 03-06 14:06:50 registry.py:327]   File "<frozen importlib._bootstrap_external>", line 995, in exec_module
ERROR 03-06 14:06:50 registry.py:327]   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/vllm/model_executor/models/granite.py", line 39, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from vllm.model_executor.layers.logits_processor import LogitsProcessor
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/vllm/model_executor/layers/logits_processor.py", line 11, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from vllm.model_executor.layers.vocab_parallel_embedding import (
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/vllm/model_executor/layers/vocab_parallel_embedding.py", line 136, in <module>
ERROR 03-06 14:06:50 registry.py:327]     @torch.compile(dynamic=True)
ERROR 03-06 14:06:50 registry.py:327]      ^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/__init__.py", line 2506, in fn
ERROR 03-06 14:06:50 registry.py:327]     return compile(
ERROR 03-06 14:06:50 registry.py:327]            ^^^^^^^^
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/__init__.py", line 2535, in compile
ERROR 03-06 14:06:50 registry.py:327]     return torch._dynamo.optimize(
ERROR 03-06 14:06:50 registry.py:327]            ^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_dynamo/eval_frame.py", line 852, in optimize
ERROR 03-06 14:06:50 registry.py:327]     return _optimize(rebuild_ctx, *args, **kwargs)
ERROR 03-06 14:06:50 registry.py:327]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_dynamo/eval_frame.py", line 927, in _optimize
ERROR 03-06 14:06:50 registry.py:327]     backend.get_compiler_config()
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/__init__.py", line 2317, in get_compiler_config
ERROR 03-06 14:06:50 registry.py:327]     from torch._inductor.compile_fx import get_patched_config_dict
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_inductor/compile_fx.py", line 103, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from .fx_passes.joint_graph import joint_graph_passes
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_inductor/fx_passes/joint_graph.py", line 22, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from ..pattern_matcher import (
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_inductor/pattern_matcher.py", line 96, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from .lowering import fallback_node_due_to_unsupported_type
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_inductor/lowering.py", line 6650, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from . import kernel
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_inductor/kernel/__init__.py", line 1, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from . import mm, mm_common, mm_plus_mm, unpack_mixed_mm
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_inductor/kernel/mm.py", line 16, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from torch._inductor.codegen.cpp_gemm_template import CppGemmTemplate
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_inductor/codegen/cpp_gemm_template.py", line 25, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from .cpp_micro_gemm import (
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_inductor/codegen/cpp_micro_gemm.py", line 16, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from .cpp_template_kernel import CppTemplateKernel
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_inductor/codegen/cpp_template_kernel.py", line 21, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from .cpp_wrapper_cpu import CppWrapperCpu
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_inductor/codegen/cpp_wrapper_cpu.py", line 23, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from .aoti_hipify_utils import maybe_hipify_code_wrapper
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/_inductor/codegen/aoti_hipify_utils.py", line 4, in <module>
ERROR 03-06 14:06:50 registry.py:327]     from torch.utils.hipify.hipify_python import PYTORCH_MAP, PYTORCH_TRIE
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/utils/hipify/hipify_python.py", line 770, in <module>
ERROR 03-06 14:06:50 registry.py:327]     CAFFE2_TRIE = Trie()
ERROR 03-06 14:06:50 registry.py:327]                   ^^^^^^
ERROR 03-06 14:06:50 registry.py:327]   File "/opt/vllm/lib64/python3.12/site-packages/torch/utils/hipify/hipify_python.py", line 683, in __init__
ERROR 03-06 14:06:50 registry.py:327]     self._hash = hashlib.md5()
ERROR 03-06 14:06:50 registry.py:327]                  ^^^^^^^^^^^^^
ERROR 03-06 14:06:50 registry.py:327] _hashlib.UnsupportedDigestmodError: [digital envelope routines] unsupported
ERROR 03-06 14:06:50 registry.py:327] 
Traceback (most recent call last):
``` 

### Operating System

RHEL 9.x

### CPU

Intel(R) Xeon(R) Platinum 8480C

### GPU

AMD Instinct MI300X

### ROCm Version

ROCm 6.3.1

### ROCm Component

_No response_

### Steps to Reproduce

We have openshift cluster with FIPS enabled and when we try to deploy vllm whihc is build on ROCm 6.3.1 we observed that it failed with below error.

```makefile
 File "/opt/vllm/lib64/python3.12/site-packages/torch/utils/hipify/hipify_python.py", line 683, in __init__
ERROR 03-10 18:09:03 registry.py:327]     self._hash = hashlib.md5()
ERROR 03-10 18:09:03 registry.py:327]                  ^^^^^^^^^^^^^
ERROR 03-10 18:09:03 registry.py:327] _hashlib.UnsupportedDigestmodError: [digital envelope routines] unsupported
``` 

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

we can fix the issue by add the `usedforsecurity=False kwarg to the hash generation call`

---

## 评论 (1 条)

### 评论 #1 — tarukumar (2025-03-10T18:59:49Z)

Issue seem to be related to pytoch

---
