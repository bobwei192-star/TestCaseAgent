# [Feature]: using managed memory in XLA

> **Issue #3364**
> **状态**: closed
> **创建时间**: 2024-06-27T01:34:21Z
> **更新时间**: 2024-12-02T00:23:09Z
> **关闭时间**: 2024-12-02T00:23:08Z
> **作者**: dipietrantonio
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3364

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

Dear ROCm developers,

according to some tests I performed, Managed Memory was not really working in ROCm 5.x but it does work at least in ROCm 6.1.2. Is the XLA implementation able to leverage managed memory to allow CPU memory to be used as extension of the GPU memory? The feature is already supported for NVIDIA GPUs and was wondering whether there are any plans to implement it for AMD too.

### Operating System

_No response_

### GPU

MI250

### ROCm Component

XLA

---

## 评论 (56 条)

### 评论 #1 — dipietrantonio (2024-06-29T05:12:58Z)

Sorry, the library I was referring to  was JAX.

---

### 评论 #2 — ppanchad-amd (2024-07-04T15:20:48Z)

@dipietrantonio I will check with the internal team and let you know. Thanks!

---

### 评论 #3 — i-chaochen (2024-07-08T19:36:11Z)

Hi @dipietrantonio could you specify which test you're using for the managed memory?

in JAX/XLA, NV and ROCm uses same [BFC(Best-Fit Coalescing)](https://github.com/openxla/xla/blob/faf0356383fe1ac1f76c6273a9cbe970aa371191/xla/pjrt/gpu/se_gpu_pjrt_client.cc#L895-L907) to manage the gpu memory. 

To cut a long story short, [XLA will take "almost" all gpu memory from ROCm/CUDA driver APIs](https://github.com/openxla/xla/blob/faf0356383fe1ac1f76c6273a9cbe970aa371191/xla/stream_executor/rocm/rocm_driver.cc#L2045), and XLA will make the decision how to use it for each Operator (e.g., BFC, make it as number of different size of bins and try the smallest bins first one by one). 

So, back to your question about memory management in JAX/XLA, AFAIK, we're using same BFC memory management like CUDA, and it doesn't matter which rocm version you're using, because rocm driver APIs are there in day-0.

If you can share what tests you're using and it will help us.


---

### 评论 #4 — dipietrantonio (2024-07-09T02:34:07Z)

Hi @i-chaochen - what I am referring to is HIP [managed memory](https://rocm.docs.amd.com/projects/HIP/en/latest/doxygen/html/group___memory_m.html#gaadf4780d920bb6f5cc755880740ef7dc), and not the custom memory management you may have implemented to handle global memory within the GPU. I have written simple test cases using HIP to allocate and use managed memory with `hipMallocManaged`, and it nondeterministically failed with various errors with ROCm 5.x on a MI250X.

With HIP/CUDA Managed Memory, GPUs are able to access host memory by letting the runtime transfer memory pages from host to GPU memory, making the latter act as a cache for the former. In this way more memory can be used by the program. My understanding is that JAX uses `cudaMallocManaged` to implement such a strategy.

---

### 评论 #5 — dipietrantonio (2024-07-09T03:36:05Z)

My ultimate goal is to run ColabFold, a scientific machine learning tool built on top of AlphaFold, to predict protein structure given a sequence of amino-acids.

The program fails with the error below. The same works on NVIDIA GPUs, where CPU memory is also used in conjunction with GPU memory to allow larger memory allocations. I am inclined to believe that here `hipMallocManaged` is not used somehow.

```
2024-06-24 17:01:13.933585: E external/xla/xla/stream_executor/rocm/rocm_driver.cc:1268] failed to allocate 154.06GiB (165425291480 bytes) from device: HIP_ERROR_OutOfMemory
2024-06-24 17:01:13.936447: E external/xla/xla/pjrt/pjrt_stream_executor_client.cc:2732] Execution of replica 0 failed: RESOURCE_EXHAUSTED: Failed to allocate request for 154.06GiB (165425291480B) on device ordinal 0
BufferAssignment OOM Debugging.
BufferAssignment stats:
             parameter allocation:   10.04GiB
              constant allocation:    24.6KiB
        maybe_live_out allocation:   28.74GiB
     preallocated temp allocation:  154.06GiB
  preallocated temp fragmentation:   24.75MiB (0.02%)
                 total allocation:  192.84GiB
              total fragmentation:    9.71GiB (5.03%)
Peak buffers:
	Buffer 1:
		Size: 38.10GiB
		Operator: op_name="jit(apply_fn)/jit(main)/alphafold/alphafold_iteration/while/body/evoformer/__layer_stack_no_state/while/body/extra_msa_stack/triangle_multiplication_outgoing/add;jit(apply_fn)/jit(main)/a
lphafold/alphafold_iteration/while/body/evoformer/__layer_stack_no_state/while/body/extra_msa_stack/triangle_multiplication_outgoing/div;jit(apply_fn)/jit(main)/alphafold/alphafold_iteration/while/body/evoformer/__layer_st
ack_no_state/while/body/extra_msa_stack/triangle_multiplication_incoming/add;jit(apply_fn)/jit(main)/alphafold/alphafold_iteration/while/body/evoformer/__layer_stack_no_state/while/body/extra_msa_stack/triangle_multiplicat
ion_incoming/div;jit(apply_fn)/jit(main)/alphafold/alphafold_iteration/while/body/evoformer/__layer_stack_no_state_1/while/body/evoformer_iteration/triangle_multiplication_outgoing/add;jit(apply_fn)/jit(main)/alphafold/alp
hafold_iteration/while/body/evoformer/__layer_stack_no_state_1/while/body/evoformer_iteration/triangle_multiplication_outgoing/div;jit(apply_fn)/jit(main)/alphafold/alphafold_iteration/while/body/evoformer/__layer_stack_no
_state_1/while/body/evoformer_iteration/triangle_multiplication_incoming/add;jit(apply_fn)/jit(main)/alphafold/alphafold_iteration/while/body/evoformer/__layer_stack_no_state_1/while/body/evoformer_iteration/triangle_multi
plication_incoming/div" deduplicated_name="fusion.664"
		XLA Label: fusion
		Shape: f32[39955041,256]
		==========================

	Buffer 2:
		Size: 38.10GiB
		Operator: op_name="jit(apply_fn)/jit(main)/alphafold/alphafold_iteration/while/body/evoformer/__layer_stack_no_state_1/while/body/evoformer_iteration/triangle_multiplication_outgoing/mul" source_file="/opt/
miniconda3/bin/colabfold_batch" source_line=8 deduplicated_name="fusion.670"
		XLA Label: fusion
		Shape: f32[256,6321,6321]
		==========================

	Buffer 3:
		Size: 19.05GiB
		Operator: op_name="jit(apply_fn)/jit(main)/alphafold/alphafold_iteration/while/body/evoformer/__layer_stack_no_state_1/while/body/evoformer_iteration/triangle_multiplication_incoming/gate/...a, ah->...h/dot
_general[dimension_numbers=(((2,), (0,)), ((), ())) precision=None preferred_element_type=bfloat16]" source_file="/opt/miniconda3/bin/colabfold_batch" source_line=8
		XLA Label: custom-call
		Shape: bf16[39955048,256]
		==========================
```

---

### 评论 #6 — i-chaochen (2024-07-09T09:14:02Z)

Thanks for sharing the details. Yes, we haven't added `hipMallocManaged` yet, but I think ~`cudaMallocManaged` is not used in XLA neither in NV side.~

I will dig it deeper on it.

---

### 评论 #7 — dipietrantonio (2024-07-09T09:22:02Z)

Thank you @i-chaochen . I have come across[ this comment](https://github.com/google-deepmind/alphafold/issues/340#issuecomment-1017699736) that seems to suggest it is possible. Hope it helps with your investigation.

---

### 评论 #8 — i-chaochen (2024-07-09T11:34:23Z)

In addition, regarding ColabFold, could you provide a simple code I can reproduce this OOM error, please? so I can test it in both NV/ROCm gpu and fix this issue on rocm side.

@dipietrantonio 

---

### 评论 #9 — dipietrantonio (2024-07-15T00:49:42Z)

Here is a container for ColabFold built for ROCm: https://quay.io/sarahbeecroft9/colabfold:rocm6_cpuTF

Here is the input file: [1IH7.7.a3m.txt](https://github.com/user-attachments/files/16229258/1IH7.7.a3m.txt)
(remove the .txt extension)
We use the singularity container engine on our system. Here is how we execute the container

```

A3M=1IH7.7.a3m # input is a multiple sequence alignment 
OUT=$MYSCRATCH/colabfold-out-1IH7.7 # name of the output directory 

# define colabfold container 
containerImage=/path/to/colabfold_rocm6_cpuTF.sif


export SINGULARITYENV_XLA_PYTHON_CLIENT_PREALLOCATE=false
export SINGULARITYENV_TF_FORCE_UNIFIED_MEMORY="1"
export SINGULARITYENV_XLA_PYTHON_CLIENT_MEM_FRACTION="4.0"
export SINGULARITYENV_XLA_PYTHON_CLIENT_ALLOCATOR="platform"
export SINGULARITYENV_TF_FORCE_GPU_ALLOW_GROWTH="true"

openssl s_client -connect api.colabfold.com:443 

# Run colab container
singularity exec --rocm  $containerImage \
        colabfold_batch --num-recycle 5 --pair-mode unpaired --model-type alphafold2_multimer_v3 --num-models 3 $A3M $OUT
```

you can install colabfold on an NVIDIA system without resorting to a container, it is available as a pip package
https://pypi.org/project/colabfold/ 

---

### 评论 #10 — i-chaochen (2024-07-15T08:09:55Z)

thanks for this sharing. I will look it.

---

### 评论 #11 — hsharsha (2024-07-23T15:40:12Z)

@dipietrantonio  I am trying to pull the image using `singularity pull` and running into the issue as shown
```
singularity pull docker://quay.io/sarahbeecroft9/colabfold:rocm6_cpuTF
INFO:    Converting OCI blobs to SIF format
INFO:    Starting build...
INFO:    Fetching OCI image...
0.0b / 32.1MiB [----------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
0.0b / 29.0MiB [----------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
538.0MiB / 538.0MiB [===============================================================================] 100 % 9.1 MiB/s 0s
0.0b / 1.6MiB [-----------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
0.0b / 17.5MiB [----------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
2.6GiB / 4.8GiB [============================================>-------------------------------------] 55 % 9.1 MiB/s 4m7s
0.0b / 2.9MiB [-----------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
249.7MiB / 249.7MiB [=================================================================================] 100 % 0.0 b/s 0s
0.0b / 617.7MiB [---------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
0.0b / 659.5KiB [---------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
1.4GiB / 1.4GiB [=====================================================================================] 100 % 0.0 b/s 0s
0.0b / 116.0MiB [---------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
0.0b / 44.3MiB [----------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
2.5GiB / 4.3GiB [===============================================>---------------------------------] 59 % 8.7 MiB/s 3m24s
0.0b / 3.6MiB [-----------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
0.0b / 214.0MiB [---------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
0.0b / 37.6MiB [----------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
0.0b / 8.7MiB [-----------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
2.0GiB / 2.0GiB [=====================================================================================] 100 % 0.0 b/s 0s
131.4MiB / 131.4MiB [=================================================================================] 100 % 0.0 b/s 0s
0.0b / 165.4KiB [---------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
518.4MiB / 518.4MiB [=================================================================================] 100 % 0.0 b/s 0s
0.0b / 150.7MiB [---------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
0.0b / 69.1MiB [----------------------------------------------------------------------------------------] 0 % 0.0 b/s 0s
FATAL:   While making image from oci registry: error fetching image to cache: while building SIF from layers: conveyor failed to get: error writing layer: stream error: stream ID 67; INTERNAL_ERROR; received from peer
```
How can I generate sif image?

---

### 评论 #12 — i-chaochen (2024-07-25T13:31:44Z)

I have created this PR for adding managed memory in ROCm side https://github.com/openxla/xla/pull/15311

Once it's merged should be no problem. 

You can cherry-pick it on your local and rebuild your jax if you want to try it now. 

Again, thanks for the notice! @dipietrantonio 

---

### 评论 #13 — dipietrantonio (2024-07-26T00:16:29Z)

@hsharsha it must have been a temporary network error, I do not get that error.

@i-chaochen Thank you very much for your work! I will try it as soon as possible :) This will help several large research groups in the bioinformatics space around the world!

---

### 评论 #14 — dipietrantonio (2024-08-02T09:19:56Z)

Hi @i-chaochen , I am trying to build the mentioned branch from source, but I get a failure towards the end. The log file is empty. Any suggestions?

```
root@c1f740575a90:/build_xla# git clone --branch ci_rocm_unify_mem https://github.com/ROCm/xla.git /opt/builds/xla
Cloning into '/opt/builds/xla'...
remote: Enumerating objects: 284356, done.
remote: Counting objects: 100% (21273/21273), done.
remote: Compressing objects: 100% (561/561), done.
remote: Total 284356 (delta 20835), reused 20712 (delta 20712), pack-reused 263083
Receiving objects: 100% (284356/284356), 196.93 MiB | 2.60 MiB/s, done.
Resolving deltas: 100% (223429/223429), done.
root@c1f740575a90:/build_xla# cd /opt/builds/xla/
root@c1f740575a90:/opt/builds/xla# ./configure.py --backend=ROCM
INFO:root:Trying to find path to clang...
INFO:root:Found path to clang at /opt/rocm-6.1.0/lib/llvm/bin/clang-17
INFO:root:Running echo __clang_major__ | /opt/rocm-6.1.0/lib/llvm/bin/clang-17 -E -P -
INFO:root:/opt/rocm-6.1.0/lib/llvm/bin/clang-17 reports major version 17.
INFO:root:Writing bazelrc to /opt/builds/xla/xla_configure.bazelrc...
root@c1f740575a90:/opt/builds/xla# bazel build --test_output=all --spawn_strategy=sandboxed //xla/...
Extracting Bazel installation...
Starting local Bazel server and connecting to it...
INFO: Reading 'startup' options from /opt/builds/xla/.bazelrc: --windows_enable_symlinks
INFO: Options provided by the client:
  Inherited 'common' options: --isatty=1 --terminal_columns=190
INFO: Reading rc options for 'build' from /opt/builds/xla/.bazelrc:
  Inherited 'common' options: --experimental_repo_remote_exec
INFO: Reading rc options for 'build' from /opt/builds/xla/.bazelrc:
  'build' options: --define framework_shared_object=true --define tsl_protobuf_header_only=true --define=use_fast_cpp_protos=true --define=allow_oversize_protos=true --spawn_strategy=standalone -c opt --announce_rc --define=grpc_no_ares=true --noincompatible_remove_legacy_whole_archive --features=-force_no_whole_archive --enable_platform_specific_config --define=with_xla_support=true --config=short_logs --config=v2 --experimental_cc_shared_library --experimental_link_static_libraries_once=false --incompatible_enforce_config_setting_visibility
INFO: Reading rc options for 'build' from /opt/builds/xla/xla_configure.bazelrc:
  'build' options: --action_env CLANG_COMPILER_PATH=/opt/rocm-6.1.0/lib/llvm/bin/clang-17 --repo_env CC=/opt/rocm-6.1.0/lib/llvm/bin/clang-17 --repo_env BAZEL_COMPILER=/opt/rocm-6.1.0/lib/llvm/bin/clang-17 --action_env PYTHON_BIN_PATH=/usr/bin/python3 --python_path /usr/bin/python3 --copt -Wno-sign-compare --copt -Wno-error=unused-command-line-argument --copt -Wno-gnu-offsetof-extensions --build_tag_filters -no_oss --test_tag_filters -no_oss
INFO: Found applicable config definition build:short_logs in file /opt/builds/xla/.bazelrc: --output_filter=DONT_MATCH_ANYTHING
INFO: Found applicable config definition build:v2 in file /opt/builds/xla/.bazelrc: --define=tf_api_version=2 --action_env=TF2_BEHAVIOR=1
INFO: Found applicable config definition build:linux in file /opt/builds/xla/.bazelrc: --host_copt=-w --copt=-Wno-all --copt=-Wno-extra --copt=-Wno-deprecated --copt=-Wno-deprecated-declarations --copt=-Wno-ignored-attributes --copt=-Wno-array-bounds --copt=-Wunused-result --copt=-Werror=unused-result --copt=-Wswitch --copt=-Werror=switch --copt=-Wno-error=unused-but-set-variable --define=PREFIX=/usr --define=LIBDIR=$(PREFIX)/lib --define=INCLUDEDIR=$(PREFIX)/include --define=PROTOBUF_INCLUDE_PATH=$(PREFIX)/include --cxxopt=-std=c++17 --host_cxxopt=-std=c++17 --config=dynamic_kernels --experimental_guard_against_concurrent_changes
INFO: Found applicable config definition build:dynamic_kernels in file /opt/builds/xla/.bazelrc: --define=dynamic_loaded_kernels=true --copt=-DAUTOLOAD_DYNAMIC_KERNELS
DEBUG: /opt/builds/xla/third_party/py/python_repo.bzl:98:14: 
HERMETIC_PYTHON_VERSION variable was not set correctly, using default version.
Python 3.11 will be used.
To select Python version, either set HERMETIC_PYTHON_VERSION env variable in
your shell:
  export HERMETIC_PYTHON_VERSION=3.12
OR pass it as an argument to bazel command directly or inside your .bazelrc
file:
  --repo_env=HERMETIC_PYTHON_VERSION=3.12
DEBUG: /opt/builds/xla/third_party/py/python_repo.bzl:109:10: Using hermetic Python 3.11
DEBUG: /opt/builds/xla/third_party/repo.bzl:132:14: 
Warning: skipping import of repository 'llvm-raw' because it already exists.
DEBUG: /root/.cache/bazel/_bazel_root/ec03954701d0ad83f3b3e8cdb1cb720a/external/tsl/third_party/repo.bzl:132:14: 
Warning: skipping import of repository 'nvtx_archive' because it already exists.
DEBUG: /opt/builds/xla/third_party/repo.bzl:132:14: 
Warning: skipping import of repository 'jsoncpp_git' because it already exists.
WARNING: /opt/builds/xla/xla/BUILD:273:11: target '//xla:status' is deprecated: Use @com_google_absl//absl/status instead.
INFO: Analyzed 4949 targets (315 packages loaded, 33686 targets configured).
INFO: Found 4949 targets...
[3,986 / 4,090] 12 actions running
    Compiling xla/mlir_hlo/mhlo/IR/hlo_ops.cc; 49s processwrapper-sandbox
    Compiling stablehlo/dialect/ChloOps.cpp; 48s processwrapper-sandbox
    Compiling stablehlo/dialect/StablehloOps.cpp; 41s processwrapper-sandbox
    Compiling xla/service/gpu/ir_emission_utils.cc; 39s processwrapper-sandbox
    Compiling xla/service/hlo_runner_pjrt.cc; 36s processwrapper-sandbox
    Compiling xla/pjrt/host_memory_spaces.cc; 35s processwrapper-sandbox
    Compiling xla/pjrt/pjrt_client.cc; 34s processwrapper-sandbox
    Compiling xla/tests/pjrt_client_registry.cc; 29s processwrapper-sandbox ...

Server terminated abruptly (error code: 14, error message: 'Socket closed', log file: '/root/.cache/bazel/_bazel_root/ec03954701d0ad83f3b3e8cdb1cb720a/server/jvm.out')


```

---

### 评论 #15 — i-chaochen (2024-08-02T09:58:22Z)

Hi @dipietrantonio 

I'm not sure what's your XLA branch using before, but I think the best way to have this patch is to cherry-pick this commit https://github.com/openxla/xla/commit/e291d59c3bb3b6ef007943f28c5aaf4638c0ee08 into your initial XLA branch, instead of directly use my ci_rocm_unify_mem branch...because that branch probably is different version to your jax.

---

### 评论 #16 — dipietrantonio (2024-08-03T06:35:05Z)

Hi @i-chaochen I previously installed xla from a binary release. This time I am building from source and I cloned this branch. I don't have any other source I work with.

Can you provide me with the instructions on how to build this branch, or any other branch that would work with JAX for ROCm. I will probably need some guidance on how to build both. Should I also build TensorFlow from source?

---

### 评论 #17 — i-chaochen (2024-08-03T14:24:45Z)

I c....do you know which jax version you're using before?  the one installed XLA from a binary release.

You can know it from `jax.__version__`

---

### 评论 #18 — dipietrantonio (2024-08-05T04:10:43Z)

Here is how I install JAX within the container

```
[...]
RUN python3 -m pip install https://github.com/ROCm/jax/releases/download/rocm-jaxlib-v0.4.30/jaxlib-0.4.30+rocm611-cp310-cp310-manylinux2014_x86_64.whl
RUN python3 -m pip install https://github.com/ROCm/jax/archive/refs/tags/rocm-jaxlib-v0.4.30.tar.gz
ENV JAX_PLATFORMS "rocm"
[...]
```


Here is the version:

```
>>> import jax
2024-08-05 12:08:17.657722: E external/xla/xla/stream_executor/plugin_registry.cc:90] Invalid plugin kind specified: DNN
>>> jax.__version__
'0.4.23.dev20240411'
```

How should I install XLA and JAX? 

---

### 评论 #19 — SarahBeecroft (2024-08-05T10:59:01Z)

Hey, 
My colleague and I are both working on this. 
I was able to get jax to build following these instructions from the LUMI centre (using ROCM 6.0.2)
```
ARG JAX_VERSION=0.4.28
ENV JAX_PLATFORMS "rocm,cpu"
RUN set -eux ; \
 git clone -b rocm-jaxlib-v$JAX_VERSION https://github.com/ROCm/jax.git /opt/xla ; \
  git clone -b rocm-jaxlib-v$JAX_VERSION https://github.com/ROCm/jax.git /opt/jax ; \
  \
  cd /opt/jax ; \
  export TEST_TMPDIR=/opt/.bazel ; \
  python build/build.py --enable_rocm --rocm_path=$ROCM_PATH \
    --rocm_amdgpu_targets=gfx908,gfx90a \
    --bazel_options=--jobs=32 \
    --bazel_startup_options=--host_jvm_args=-Xmx4G \
    --bazel_startup_options=--host_jvm_args=-Xms2g ; \
  mkdir -p /opt/wheels ; \
  cp /opt/jax/dist/jaxlib-*.whl /opt/wheels ; \
  rm -rf /opt/jax /opt/xla /opt/.bazel
RUN  set -eux ; \
  pip install /opt/wheels/jaxlib-*.whl; \
  pip install jax==$JAX_VERSION
```

However, when it comes to running the inference, I get the following error


```
I0801 16:45:44.546491 23122725111616 model.py:165] Running predict with shape(feat) = {'aatype': (4, 10), 'residue_index': (4, 10), 'seq_length': (4,), 'template_aatype': (4, 4, 10), 'template_all_atom_masks': (4, 4, 10, 37), 'template_all_atom_positions': (4, 4, 10, 37, 3), 'template_sum_probs': (4, 4, 1), 'is_distillation': (4,), 'seq_mask': (4, 10), 'msa_mask': (4, 508, 10), 'msa_row_mask': (4, 508), 'random_crop_to_size_seed': (4, 2), 'template_mask': (4, 4), 'template_pseudo_beta': (4, 4, 10, 3), 'template_pseudo_beta_mask': (4, 4, 10), 'atom14_atom_exists': (4, 10, 14), 'residx_atom14_to_atom37': (4, 10, 14), 'residx_atom37_to_atom14': (4, 10, 37), 'atom37_atom_exists': (4, 10, 37), 'extra_msa': (4, 5120, 10), 'extra_msa_mask': (4, 5120, 10), 'extra_msa_row_mask': (4, 5120), 'bert_mask': (4, 508, 10), 'true_msa': (4, 508, 10), 'extra_has_deletion': (4, 5120, 10), 'extra_deletion_value': (4, 5120, 10), 'msa_feat': (4, 508, 10, 49), 'target_feat': (4, 10, 22)}
Traceback (most recent call last):
  File "/opt/alphafold/run_alphafold.py", line 570, in <module>
    app.run(main)
  File "/opt/miniforge3/lib/python3.10/site-packages/absl/app.py", line 312, in run
    _run_main(main, args)
  File "/opt/miniforge3/lib/python3.10/site-packages/absl/app.py", line 258, in _run_main
    sys.exit(main(argv))
  File "/opt/alphafold/run_alphafold.py", line 543, in main
    predict_structure(
  File "/opt/alphafold/run_alphafold.py", line 284, in predict_structure
    prediction_result = model_runner.predict(processed_feature_dict,
  File "/opt/alphafold/alphafold/model/model.py", line 167, in predict
    result = self.apply(self.params, jax.random.PRNGKey(random_seed), feat)
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/traceback_util.py", line 179, in reraise_with_filtered_traceback
    return fun(*args, **kwargs)
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/pjit.py", line 304, in cache_miss
    outs, out_flat, out_tree, args_flat, jaxpr, attrs_tracked = _python_pjit_helper(
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/pjit.py", line 181, in _python_pjit_helper
    out_flat = pjit_p.bind(*args_flat, **params)
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/core.py", line 2789, in bind
    return self.bind_with_trace(top_trace, args, params)
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/core.py", line 391, in bind_with_trace
    out = trace.process_primitive(self, map(trace.full_raise, args), params)
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/core.py", line 879, in process_primitive
    return primitive.impl(*tracers, **params)
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/pjit.py", line 1525, in _pjit_call_impl
    return xc._xla.pjit(
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/pjit.py", line 1508, in call_impl_cache_miss
    out_flat, compiled = _pjit_call_impl_python(
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/pjit.py", line 1438, in _pjit_call_impl_python
    inline=inline, lowering_parameters=mlir.LoweringParameters()).compile()
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/interpreters/pxla.py", line 2363, in compile
    executable = UnloadedMeshExecutable.from_hlo(
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/interpreters/pxla.py", line 2860, in from_hlo
    xla_executable = _cached_compilation(
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/interpreters/pxla.py", line 2678, in _cached_compilation
    xla_executable = compiler.compile_or_get_cached(
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/compiler.py", line 330, in compile_or_get_cached
    return _compile_and_write_cache(
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/compiler.py", line 501, in _compile_and_write_cache
    executable = backend_compile(
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/profiler.py", line 335, in wrapper
    return func(*args, **kwargs)
  File "/opt/miniforge3/lib/python3.10/site-packages/jax/_src/compiler.py", line 237, in backend_compile
    return backend.compile(built_c, compile_options=options)
jaxlib.xla_extension.XlaRuntimeError: INTERNAL: Failed to launch ROCm kernel: redzone_checker with block dimensions: 1024x1x1: hipError_t(303)
srun: error: nid002948: task 0: Exited with exit code 1
srun: launch/slurm: _step_signal: Terminating StepId=14458686.0
```
If I install Jax with pip install as Cristian mentioned above, it works but there is no unified memory. 

The good news is that the fix does seem to allow peer memory access, which is great! 

Thanks a lot, 

Sarah

---

### 评论 #20 — i-chaochen (2024-08-05T11:11:20Z)

Hi @SarahBeecroft 

I notice that you're using v0.4.28 and we have QA branch for it, which is for ROCm6.2 but should be no problem on ROCm6.0.2. And I have added that unify memory for our v0.4.28-qa branch as well.

https://github.com/ROCm/xla/tree/rocm-jaxlib-v0.4.28-qa

So I would suggest you changed that instructions and point our our QA branch to use that unified memory functionality.



@dipietrantonio 

Strangely, I can see both v0.4.30 and v0.4.23 from your side. But I just backported this to our v0.4.23 and v0.4.30-QA branches.
- https://github.com/ROCm/xla/pull/33
- https://github.com/ROCm/xla/pull/32


to install JAX from the scratch, for example you want to try v0.4.28-qa, you can git clone this JAX and XLA
https://github.com/ROCm/jax/commits/rocm-jaxlib-v0.4.28-qa/
https://github.com/ROCm/xla/tree/rocm-jaxlib-v0.4.28-qa

Then, set this [XLA_CLONE_DIR](https://github.com/ROCm/jax/blob/rocm-jaxlib-v0.4.28-qa/build/rocm/build_rocm.sh#L60) to your local XLA's `rocm-jaxlib-v0.4.28-qa` and run this `build_rocm.sh`






---

### 评论 #21 — dipietrantonio (2024-08-05T11:37:47Z)

@i-chaochen Thanks for the explanation! I will try the `rocm-jaxlib-v0.4.28-qa` branch. Did you mean to attach a `build_rocm.sh` script? I do not see any attachment

---

### 评论 #22 — i-chaochen (2024-08-05T11:54:24Z)

If you click that above XLA_CLONE_DIR, you should know what I'm referring to...

---

### 评论 #23 — dipietrantonio (2024-08-05T13:04:53Z)

Thanks! Unfortunately the build stops with the following error. Any idea on how to fix it? Thank you again for your efforts on this issue, it is very much appreciated :) 

```
[551 / 7,375] Executing genrule @local_config_rocm//rocm:rocm-lib; 28s local ... (12 actions running)
[558 / 7,381] Executing genrule @local_config_rocm//rocm:rocm-lib; 29s local ... (11 actions running)
[560 / 7,389] Executing genrule @local_config_rocm//rocm:rocm-lib; 30s local ... (12 actions running)
[561 / 7,389] Executing genrule @local_config_rocm//rocm:rocm-lib; 31s local ... (12 actions, 11 running)
ERROR: /root/.cache/bazel/_bazel_root/c70ff50ec230a16294128bb6a04f27e1/external/xla/xla/stream_executor/rocm/BUILD:177:13: Compiling xla/stream_executor/rocm/hip_conditional_kernels.cu.cc failed: undeclared inclusion(s) in rule '@xla//xla/stream_executor/rocm:hip_conditional_kernels':
this rule is missing dependency declarations for the following files included by 'xla/stream_executor/rocm/hip_conditional_kernels.cu.cc':
  '/opt/rocm/llvm/lib/clang/17/include/__clang_hip_runtime_wrapper.h'
  '/opt/rocm/llvm/lib/clang/17/include/cuda_wrappers/cmath'
  '/opt/rocm/llvm/lib/clang/17/include/stddef.h'
  '/opt/rocm-6.1.0/include/hip/hip_version.h'
  '/opt/rocm/llvm/lib/clang/17/include/__clang_hip_libdevice_declares.h'
  '/opt/rocm/llvm/lib/clang/17/include/__clang_hip_math.h'
  '/opt/rocm/llvm/lib/clang/17/include/cuda_wrappers/algorithm'
  '/opt/rocm/llvm/lib/clang/17/include/cuda_wrappers/new'
  '/opt/rocm/llvm/lib/clang/17/include/limits.h'
  '/opt/rocm/llvm/lib/clang/17/include/stdint.h'
  '/opt/rocm/llvm/lib/clang/17/include/__clang_hip_stdlib.h'
  '/opt/rocm/llvm/lib/clang/17/include/__clang_cuda_math_forward_declares.h'
  '/opt/rocm/llvm/lib/clang/17/include/__clang_hip_cmath.h'
  '/opt/rocm/llvm/lib/clang/17/include/__clang_cuda_complex_builtins.h'
  '/opt/rocm/llvm/lib/clang/17/include/cuda_wrappers/complex'
  '/opt/rocm/llvm/lib/clang/17/include/__stddef_max_align_t.h'
  '/opt/rocm/llvm/lib/clang/17/include/stdarg.h'
  '/opt/rocm-6.1.0/include/hip/hip_runtime.h'
  '/opt/rocm-6.1.0/include/hip/hip_common.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/amd_hip_runtime.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/amd_hip_common.h'
  '/opt/rocm-6.1.0/include/hip/hip_runtime_api.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/host_defines.h'
  '/opt/rocm-6.1.0/include/hip/driver_types.h'
  '/opt/rocm-6.1.0/include/hip/texture_types.h'
  '/opt/rocm-6.1.0/include/hip/channel_descriptor.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/amd_channel_descriptor.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/amd_hip_vector_types.h'
  '/opt/rocm-6.1.0/include/hip/surface_types.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/amd_hip_runtime_pt_api.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/amd_hip_atomic.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/amd_device_functions.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/device_library_decls.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/hip_assert.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/math_fwd.h'
  '/opt/rocm-6.1.0/include/hip/hip_vector_types.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/amd_warp_functions.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/amd_hip_unsafe_atomics.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/amd_surface_functions.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/texture_fetch_functions.h'
  '/opt/rocm-6.1.0/include/hip/hip_texture_types.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/ockl_image.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/texture_indirect_functions.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/hip_ldg.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/amd_math_functions.h'
  '/opt/rocm-6.1.0/include/hip/amd_detail/hip_fp16_math_fwd.h'
  '/opt/rocm-6.1.0/include/hip/library_types.h'
clang: warning: argument unused during compilation: '-fgpu-flush-denormals-to-zero' [-Wunused-command-line-argument]
[577 / 7,389] Executing genrule @local_config_rocm//rocm:rocm-lib; 33s local
[577 / 7,389] Executing genrule @local_config_rocm//rocm:rocm-lib; 43s local
Target //jaxlib/tools:build_wheel failed to build
INFO: Elapsed time: 229.734s, Critical Path: 49.13s
INFO: 578 processes: 423 internal, 155 local.
FAILED: Build did NOT complete successfully
```

---

### 评论 #24 — i-chaochen (2024-08-05T13:25:56Z)

Yes, it seems you didn't give the correct rocm path. You can try this following one in your JAX folder.
 - please edit your local gfx (you can know it from `rocminfo` and MI250 should be gfx90a) and local XLA directory path for `--bazel_options=--override_repository=xla=`

```
$ rm -rf dist/*
$ python3 -m pip uninstall jax jaxlib -y
$ python3 ./build/build.py --enable_rocm --rocm_amdgpu_targets=gfx90a --bazel_options=--override_repository=xla=/your/local/xla/ --rocm_path=/opt/rocm-6.1.0/ && python3 setup.py develop --user && python3 -m pip install dist/*.whl
```

---

### 评论 #25 — dipietrantonio (2024-08-13T02:52:17Z)

Dear @i-chaochen - thanks for your timely and professional help! I am very grateful. I managed to compile JAX and now I am compiling AlphaFold with it. I will keep you up to date with the testing.



---

### 评论 #26 — SarahBeecroft (2024-08-13T03:26:10Z)

Hello again! 

Thank you for your time on this! 

So I think we have implemented your instructions, but we're continuing to have some issues with the build. It does build, but at runtime the error is

```
Traceback (most recent call last):
  File "/opt/miniconda3/bin/colabfold_batch", line 5, in <module>
    from colabfold.batch import main
  File "/opt/miniconda3/lib/python3.10/site-packages/colabfold/batch.py", line 76, in <module>
    import jax
ModuleNotFoundError: No module named 'jax'
```

The full container recipe is this:

```
FROM quay.io/pawsey/rocm-mpich-base:rocm6.0.2-mpich3.4.3-ubuntu22

RUN apt-get update && \
    apt install apt-transport-https curl gnupg sed -y && \
    curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg && \
    mv bazel-archive-keyring.gpg /usr/share/keyrings && \
    echo deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8 | sudo tee /etc/apt/sources.list.d/bazel.list && \
    apt-get install -y build-essential wget aria2 git cmake gcc-10 clang gfortran zlib1g-dev numactl gawk patch tar autoconf automake libtool libjson-c-dev graphviz libncurses-dev nano xz-utils binutils doxygen && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoremove -y && \
    apt-get clean

#
# Alphafold info
#
ENV PYTHON_VERSION='3.10'
ENV ALPHAFOLD_VERSION='69afc4d'
ENV HHSUITE_VERSION='3.3.0'

#
# ROCm environment
#
ENV ROCM_RELEASE 6.0.2
ENV ROCM_PATH /opt/rocm-$ROCM_RELEASE
ENV PATH $ROCM_PATH/bin:$ROCM_PATH/llvm/bin:$PATH
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$ROCM_PATH/lib
#
#
# Mark RCCL as non-debug - this can be overriden by RCCL debug build. 
#
ENV RCCL_DEBUG 0

#
# Install miniconda
#
RUN set -eux ; \
  curl -LO https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-x86_64.sh ; \
  bash ./Miniconda3-* -b -p /opt/miniconda3 -s ; \
  rm -rf ./Miniconda3-*
ENV PATH /opt/miniconda3/bin:$PATH

ENV CC gcc
ENV CXX g++

#
# Install hh-suite.
#
ARG HHSUITE_VERSION
ENV HHSUITE_PATH /opt/hh-suite
RUN set -eux ; \
  mkdir -p /opt/builds ; \
  git clone --branch v$HHSUITE_VERSION https://github.com/soedinglab/hh-suite.git /opt/builds/hh-suite ; \
  mkdir /opt/builds/hh-suite/build ; \
  cd /opt/builds/hh-suite/build ; \
  cmake -DCMAKE_INSTALL_PREFIX=$HHSUITE_PATH .. ; \
  make -j   ; \
  make -j install  ; \
  rm -rf /opt/builds
  

#Install conda environment
 
ARG PYTHON_VERSION
RUN set -eux ; \
  conda install -y \
  conda=23.11.0
RUN conda install -y -c conda-forge -c bioconda  python=$PYTHON_VERSION \
    swig \
    numpy==1.24.3 \
    Cython \
    pandas==2.0.3 \
    dm-tree==0.1.8 \
    pdbfixer==1.9 \
    kalign2=2.04 \
    mmseqs2=15.6f452 \ 
    streamhpc::openmm-hip ; \
    conda clean -af
RUN pip install \
    tensorflow \
    ml-collections==0.1.0 \
    dm-haiku==0.0.10 \
    hmmer \
    absl-py==1.0.0 \
    mock \
    chex==0.0.7 \
    immutabledict==2.0.0 \
    scipy==1.11.1 \
    biopython==1.79 --no-cache-dir

#############
##COLABFOLD##
#############

ENV CURRENTPATH='/opt'
ENV COLABFOLDDIR="${CURRENTPATH}/localcolabfold"

RUN mkdir -p "${COLABFOLDDIR}"
RUN cd "${COLABFOLDDIR}"

# install ColabFold and Jaxlib
RUN pip install --no-warn-conflicts \
    "colabfold[alphafold-without-jax] @ git+https://github.com/sokrypton/ColabFold" --no-cache-dir
RUN pip install "colabfold[alphafold]" --no-cache-dir
RUN pip install --upgrade tensorflow --no-cache-dir

# Download the updater
RUN wget -qnc -O "$COLABFOLDDIR/update_linux.sh" \
    https://raw.githubusercontent.com/YoshitakaMo/localcolabfold/main/update_linux.sh
RUN chmod +x "$COLABFOLDDIR/update_linux.sh"

RUN cd /opt/miniconda3/lib/python3.10/site-packages/colabfold && sed -i -e "s#from matplotlib import pyplot as plt#import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt#g" plot.py && sed -i -e "s#appdirs.user_cache_dir(__package__ or \"colabfold\")#\"${COLABFOLDDIR}/colabfold\"#g" download.py && \
  rm -rf __pycache__

# Download weights
RUN /opt/miniconda3/bin/python3 -m colabfold.download

#
# Install JAX
#
ARG JAX_VERSION=0.4.28
ENV JAX_PLATFORMS "rocm,cpu"
RUN set -eux ; \
  git clone -b rocm-jaxlib-v${JAX_VERSION}-qa https://github.com/ROCm/xla.git /opt/xla ; \
  git clone -b rocm-jaxlib-v${JAX_VERSION}-qa https://github.com/ROCm/jax.git /opt/jax ; \
  cd /opt/jax ; \
  rm -rf dist/* ; \
  /opt/miniconda3/bin/python3 -m pip uninstall jax jaxlib -y ; \
  export TEST_TMPDIR=/opt/.bazel ; \
  /opt/miniconda3/bin/python3 ./build/build.py \
    --enable_rocm \
    --rocm_amdgpu_targets=gfx90a \
    --bazel_options=--override_repository=xla=/opt/xla \
    --rocm_path=$ROCM_PATH && \
    /opt/miniconda3/bin/python3 setup.py develop --user && \
    /opt/miniconda3/bin/python3 -m pip install dist/*.whl
RUN rm -rf /opt/.bazel

WORKDIR ${COLABFOLDDIR}
```

We would be very grateful for edits, fixes, anything for the recipe if we have done something wrong here. 

Thank you!


EDIT:
The same thing also happens with the Alphafold container


```

FROM  quay.io/pawsey/rocm-mpich-base:rocm6.0.2-mpich3.4.3-ubuntu22
RUN apt-get update && \
    apt install apt-transport-https curl gnupg -y && \
    curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg && \
    mv bazel-archive-keyring.gpg /usr/share/keyrings && \
    echo deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8 | sudo tee /etc/apt/sources.list.d/bazel.list && \
    apt-get install -y build-essential wget aria2 git cmake gcc-10 clang gfortran zlib1g-dev numactl gawk patch tar autoconf automake libtool libjson-c-dev graphviz libncurses-dev nano xz-utils binutils doxygen && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoremove -y && \
    apt-get clean
#
# Alphafold info
#
ENV PYTHON_VERSION='3.10'
ENV ALPHAFOLD_VERSION='69afc4d'
ENV HHSUITE_VERSION='3.3.0'
ENV JAX_PLATFORMS "rocm,cpu"
#
# ROCm environment
#
ENV ROCM_RELEASE 6.0.2
ENV ROCM_PATH /opt/rocm-$ROCM_RELEASE
ENV PATH $ROCM_PATH/bin:$ROCM_PATH/llvm/bin:$PATH
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$ROCM_PATH/lib
#
# Mark RCCL as non-debug - this can be overriden by RCCL debug build. 
#
ENV RCCL_DEBUG 0
#
# Install miniforge (mamba)
#
RUN set -eux ; \
    curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" ; \
    bash Miniforge3-$(uname)-$(uname -m).sh -b -p /opt/miniforge3 -s ; \
    rm -rf ./Miniforge3-*
ENV PATH /opt/miniforge3/bin:$PATH
#
# Install hh-suite.
#
ARG HHSUITE_VERSION
ENV HHSUITE_PATH /opt/hh-suite
RUN set -eux ; \
  mkdir -p /opt/builds ; \
  git clone --branch v$HHSUITE_VERSION https://github.com/soedinglab/hh-suite.git /opt/builds/hh-suite ; \
  mkdir /opt/builds/hh-suite/build ; \
  cd /opt/builds/hh-suite/build ; \
  cmake -DCMAKE_INSTALL_PREFIX=$HHSUITE_PATH .. ; \
  make -j   ; \
  make -j install  ; \
  rm -rf /opt/builds
  
#
# Install mamba environment
# 
ARG PYTHON_VERSION
RUN set -eux ; \
    mamba install -y -c conda-forge -c bioconda \
    python=$PYTHON_VERSION \
    swig \
    numpy==1.24.3 \
    Cython \
    pandas==2.0.3 \
    dm-tree==0.1.8 \
    pdbfixer==1.9 \
    kalign2 \
    streamhpc::openmm-hip ; \
    mamba clean -afy
RUN pip install \
    ml-collections==0.1.0 \
    dm-haiku==0.0.12 \
    hmmer \
    absl-py==1.0.0 \
    mock \
    chex==0.0.7 \
    immutabledict==2.0.0 \
    biopython==1.79 \
    typing-extensions \
    tensorflow \
    build \
    --no-cache-dir
#
# Install JAX
#

ARG JAX_VERSION=0.4.28
ENV JAX_PLATFORMS "rocm,cpu"
RUN set -eux ; \
  git clone -b rocm-jaxlib-v${JAX_VERSION}-qa https://github.com/ROCm/xla.git /opt/xla ; \
  git clone -b rocm-jaxlib-v${JAX_VERSION}-qa https://github.com/ROCm/jax.git /opt/jax ; \
  cd /opt/jax ; \
  rm -rf dist/* ; \
  /opt/miniconda3/bin/python3 -m pip uninstall jax jaxlib -y ; \
  export TEST_TMPDIR=/opt/.bazel ; \
  /opt/miniconda3/bin/python3 ./build/build.py \
    --enable_rocm \
    --rocm_amdgpu_targets=gfx90a \
    --bazel_options=--override_repository=xla=/opt/xla \
    --rocm_path=$ROCM_PATH && \
    /opt/miniconda3/bin/python3 setup.py develop --user && \
    /opt/miniconda3/bin/python3 -m pip install dist/*.whl
RUN rm -rf /opt/.bazel



#
# Clone alphafold 
#
ARG ALPHAFOLD_VERSION
ENV ALPHAFOLD_PATH /opt/alphafold
RUN set -eux ; \
  git clone https://github.com/deepmind/alphafold $ALPHAFOLD_PATH ; \
  \
  cd $ALPHAFOLD_PATH ; \
  git checkout -b mydev $ALPHAFOLD_VERSION ; \
  sed -i 's#CUDA#HIP#g' alphafold/relax/amber_minimize.py ; \
  \
  cd $ALPHAFOLD_PATH/alphafold/common ; \
  curl -LO https://git.scicore.unibas.ch/schwede/openstructure/-/raw/7102c63615b64735c4941278d92b554ec94415f8/modules/mol/alg/src/stereo_chemical_props.txt
RUN set -eux ; \
  rm /opt/miniforge3/lib/libstdc++.so* ; \
  ln -s /usr/lib64/libstdc++.so* /opt/miniforge3/lib
WORKDIR /opt/alphafold
```

---

### 评论 #27 — Ruturaj4 (2024-08-15T17:26:51Z)

Hi @SarahBeecroft Can you please change you dockerfile as follows:

```
FROM quay.io/pawsey/rocm-mpich-base:rocm6.0.2-mpich3.4.3-ubuntu22

RUN apt-get update && \
    apt install apt-transport-https curl gnupg sed -y && \
    curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg && \
    mv bazel-archive-keyring.gpg /usr/share/keyrings && \
    echo deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8 | sudo tee /etc/apt/sources.list.d/bazel.list && \
    apt-get install -y build-essential wget aria2 git cmake gcc-10 clang gfortran zlib1g-dev numactl gawk patch tar autoconf automake libtool libjson-c-dev graphviz libncurses-dev nano xz-utils binutils doxygen && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoremove -y && \
    apt-get clean

#
# Alphafold info
#
ENV PYTHON_VERSION='3.10'
ENV ALPHAFOLD_VERSION='69afc4d'
ENV HHSUITE_VERSION='3.3.0'

#
# ROCm environment
#
ENV ROCM_RELEASE 6.0.2
ENV ROCM_PATH /opt/rocm-$ROCM_RELEASE
ENV PATH $ROCM_PATH/bin:$ROCM_PATH/llvm/bin:$PATH
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$ROCM_PATH/lib
#
#
# Mark RCCL as non-debug - this can be overriden by RCCL debug build. 
#
ENV RCCL_DEBUG 0

#
# Install miniconda
#
RUN set -eux ; \
  curl -LO https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-x86_64.sh ; \
  bash ./Miniconda3-* -b -p /opt/miniconda3 -s ; \
  rm -rf ./Miniconda3-*
ENV PATH /opt/miniconda3/bin:$PATH

ENV CC gcc
ENV CXX g++

#
# Install hh-suite.
#
ARG HHSUITE_VERSION
ENV HHSUITE_PATH /opt/hh-suite
RUN set -eux ; \
  mkdir -p /opt/builds ; \
  git clone --branch v$HHSUITE_VERSION https://github.com/soedinglab/hh-suite.git /opt/builds/hh-suite ; \
  mkdir /opt/builds/hh-suite/build ; \
  cd /opt/builds/hh-suite/build ; \
  cmake -DCMAKE_INSTALL_PREFIX=$HHSUITE_PATH .. ; \
  make -j   ; \
  make -j install  ; \
  rm -rf /opt/builds
  

#Install conda environment
 
ARG PYTHON_VERSION
RUN set -eux ; \
  conda install -y \
  conda=23.11.0
RUN conda install -y -c conda-forge -c bioconda  python=$PYTHON_VERSION \
    swig \
    numpy==1.24.3 \
    Cython \
    pandas==2.0.3 \
    dm-tree==0.1.8 \
    pdbfixer==1.9 \
    kalign2=2.04 \
    mmseqs2=15.6f452 \ 
    streamhpc::openmm-hip ; \
    conda clean -af
RUN pip install \
    build \
    tensorflow \
    ml-collections==0.1.0 \
    dm-haiku==0.0.10 \
    hmmer \
    absl-py==1.0.0 \
    mock \
    chex==0.0.7 \
    immutabledict==2.0.0 \
    scipy==1.11.1 \
    biopython==1.79 --no-cache-dir

#############
##COLABFOLD##
#############

ENV CURRENTPATH='/opt'
ENV COLABFOLDDIR="${CURRENTPATH}/localcolabfold"

RUN mkdir -p "${COLABFOLDDIR}"
RUN cd "${COLABFOLDDIR}"

# install ColabFold and Jaxlib
RUN pip install --no-warn-conflicts \
    "colabfold[alphafold-without-jax] @ git+https://github.com/sokrypton/ColabFold" --no-cache-dir
RUN pip install "colabfold[alphafold]" --no-cache-dir
RUN pip install --upgrade tensorflow --no-cache-dir

# Download the updater
RUN wget -qnc -O "$COLABFOLDDIR/update_linux.sh" \
    https://raw.githubusercontent.com/YoshitakaMo/localcolabfold/main/update_linux.sh
RUN chmod +x "$COLABFOLDDIR/update_linux.sh"

RUN cd /opt/miniconda3/lib/python3.10/site-packages/colabfold && sed -i -e "s#from matplotlib import pyplot as plt#import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt#g" plot.py && sed -i -e "s#appdirs.user_cache_dir(__package__ or \"colabfold\")#\"${COLABFOLDDIR}/colabfold\"#g" download.py && \
  rm -rf __pycache__

# Download weights
RUN /opt/miniconda3/bin/python3 -m colabfold.download

#
# Install JAX
#
ARG JAX_VERSION=0.4.28
ENV JAX_PLATFORMS "rocm,cpu"
RUN set -eux ; \
  git clone -b rocm-jaxlib-v${JAX_VERSION}-qa https://github.com/ROCm/xla.git /opt/xla ; \
  git clone -b rocm-jaxlib-v${JAX_VERSION}-qa https://github.com/ROCm/jax.git /opt/jax ; \
  cd /opt/jax ; \
  rm -rf dist/* ; \
  /opt/miniconda3/bin/python3 -m pip uninstall jax jaxlib -y ; \
  export TEST_TMPDIR=/opt/.bazel ; \
  /opt/miniconda3/bin/python3 ./build/build.py \
    --enable_rocm \
    --rocm_amdgpu_targets=gfx90a \
    --bazel_options=--override_repository=xla=/opt/xla \
    --rocm_path=$ROCM_PATH && \
    /opt/miniconda3/bin/python3 setup.py develop --user && \
    /opt/miniconda3/bin/python3 -m pip install dist/*.whl
RUN rm -rf /opt/.bazel

WORKDIR ${COLABFOLDDIR}
```


same with the other container ->

```

FROM  quay.io/pawsey/rocm-mpich-base:rocm6.0.2-mpich3.4.3-ubuntu22
RUN apt-get update && \
    apt install apt-transport-https curl gnupg -y && \
    curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg && \
    mv bazel-archive-keyring.gpg /usr/share/keyrings && \
    echo deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8 | sudo tee /etc/apt/sources.list.d/bazel.list && \
    apt-get install -y build-essential wget aria2 git cmake gcc-10 clang gfortran zlib1g-dev numactl gawk patch tar autoconf automake libtool libjson-c-dev graphviz libncurses-dev nano xz-utils binutils doxygen && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoremove -y && \
    apt-get clean
#
# Alphafold info
#
ENV PYTHON_VERSION='3.10'
ENV ALPHAFOLD_VERSION='69afc4d'
ENV HHSUITE_VERSION='3.3.0'
ENV JAX_PLATFORMS "rocm,cpu"
#
# ROCm environment
#
ENV ROCM_RELEASE 6.0.2
ENV ROCM_PATH /opt/rocm-$ROCM_RELEASE
ENV PATH $ROCM_PATH/bin:$ROCM_PATH/llvm/bin:$PATH
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$ROCM_PATH/lib
#
# Mark RCCL as non-debug - this can be overriden by RCCL debug build. 
#
ENV RCCL_DEBUG 0
#
# Install miniforge (mamba)
#
RUN set -eux ; \
    curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" ; \
    bash Miniforge3-$(uname)-$(uname -m).sh -b -p /opt/miniforge3 -s ; \
    rm -rf ./Miniforge3-*
ENV PATH /opt/miniforge3/bin:$PATH
#
# Install hh-suite.
#
ARG HHSUITE_VERSION
ENV HHSUITE_PATH /opt/hh-suite
RUN set -eux ; \
  mkdir -p /opt/builds ; \
  git clone --branch v$HHSUITE_VERSION https://github.com/soedinglab/hh-suite.git /opt/builds/hh-suite ; \
  mkdir /opt/builds/hh-suite/build ; \
  cd /opt/builds/hh-suite/build ; \
  cmake -DCMAKE_INSTALL_PREFIX=$HHSUITE_PATH .. ; \
  make -j   ; \
  make -j install  ; \
  rm -rf /opt/builds
  
#
# Install mamba environment
# 
ARG PYTHON_VERSION
RUN set -eux ; \
    mamba install -y -c conda-forge -c bioconda \
    python=$PYTHON_VERSION \
    swig \
    numpy==1.24.3 \
    Cython \
    pandas==2.0.3 \
    dm-tree==0.1.8 \
    pdbfixer==1.9 \
    kalign2 \
    streamhpc::openmm-hip ; \
    mamba clean -afy
RUN pip install \
    build \
    ml-collections==0.1.0 \
    dm-haiku==0.0.12 \
    hmmer \
    absl-py==1.0.0 \
    mock \
    chex==0.0.7 \
    immutabledict==2.0.0 \
    biopython==1.79 \
    typing-extensions \
    tensorflow \
    build \
    --no-cache-dir
#
# Install JAX
#

ARG JAX_VERSION=0.4.28
ENV JAX_PLATFORMS "rocm,cpu"
RUN set -eux ; \
  git clone -b rocm-jaxlib-v${JAX_VERSION}-qa https://github.com/ROCm/xla.git /opt/xla ; \
  git clone -b rocm-jaxlib-v${JAX_VERSION}-qa https://github.com/ROCm/jax.git /opt/jax ; \
  cd /opt/jax ; \
  rm -rf dist/* ; \
  /opt/miniconda3/bin/python3 -m pip uninstall jax jaxlib -y ; \
  export TEST_TMPDIR=/opt/.bazel ; \
  /opt/miniconda3/bin/python3 ./build/build.py \
    --enable_rocm \
    --rocm_amdgpu_targets=gfx90a \
    --bazel_options=--override_repository=xla=/opt/xla \
    --rocm_path=$ROCM_PATH && \
    /opt/miniconda3/bin/python3 setup.py develop --user && \
    /opt/miniconda3/bin/python3 -m pip install dist/*.whl
RUN rm -rf /opt/.bazel



#
# Clone alphafold 
#
ARG ALPHAFOLD_VERSION
ENV ALPHAFOLD_PATH /opt/alphafold
RUN set -eux ; \
  git clone https://github.com/deepmind/alphafold $ALPHAFOLD_PATH ; \
  \
  cd $ALPHAFOLD_PATH ; \
  git checkout -b mydev $ALPHAFOLD_VERSION ; \
  sed -i 's#CUDA#HIP#g' alphafold/relax/amber_minimize.py ; \
  \
  cd $ALPHAFOLD_PATH/alphafold/common ; \
  curl -LO https://git.scicore.unibas.ch/schwede/openstructure/-/raw/7102c63615b64735c4941278d92b554ec94415f8/modules/mol/alg/src/stereo_chemical_props.txt
RUN set -eux ; \
  rm /opt/miniforge3/lib/libstdc++.so* ; \
  ln -s /usr/lib64/libstdc++.so* /opt/miniforge3/lib
WORKDIR /opt/alphafold
```

---

### 评论 #28 — dipietrantonio (2024-08-16T06:36:23Z)

@i-chaochen @Ruturaj4 I have managed to build a container with the patched JAX version. However, at runtime, I get the following error. Seems like GPU detection is broken? I am running on a node with AMD GPUs so the GPU is there. I tried setting JAX_PLATFORMS="" but then the code breaks on something else (see output 2)

**Output 1**
```
Singularity>  colabfold_batch --num-recycle 5 --pair-mode unpaired --model-type alphafold2_multimer_v3 --num-models 3 example_colabfold/1IH7.7.a3m output
2024-08-16 14:32:20,111 Running colabfold 1.5.5
Traceback (most recent call last):
  File "/opt/miniconda3/lib/python3.10/site-packages/colabfold/batch.py", line 1268, in run
    jax.tools.colab_tpu.setup_tpu()
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/tools/colab_tpu.py", line 20, in setup_tpu
    raise RuntimeError(
RuntimeError: jax.tools.colab_tpu.setup_tpu() was required for older JAX versions running on older generations of TPUs, and should no longer be used.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 887, in backends
    backend = _init_backend(platform)
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 973, in _init_backend
    backend = registration.factory()
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 456, in make_gpu_client
    return xla_client.make_gpu_client(
  File "/opt/miniconda3/lib/python3.10/site-packages/jaxlib/xla_client.py", line 96, in make_gpu_client
    config = _xla.GpuAllocatorConfig()
AttributeError: module 'jaxlib.xla_extension' has no attribute 'GpuAllocatorConfig'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/opt/miniconda3/bin/colabfold_batch", line 8, in <module>
    sys.exit(main())
  File "/opt/miniconda3/lib/python3.10/site-packages/colabfold/batch.py", line 2031, in main
    run(
  File "/opt/miniconda3/lib/python3.10/site-packages/colabfold/batch.py", line 1273, in run
    if jax.local_devices()[0].platform == 'cpu':
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 1143, in local_devices
    process_index = get_backend(backend).process_index()
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 1019, in get_backend
    return _get_backend_uncached(platform)
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 998, in _get_backend_uncached
    bs = backends()
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 903, in backends
    raise RuntimeError(err_msg)
RuntimeError: Unable to initialize backend 'rocm': module 'jaxlib.xla_extension' has no attribute 'GpuAllocatorConfig' (set JAX_PLATFORMS='' to automatically choose an available backend)
```

**Output 2**
```
Singularity> export JAX_PLATFORMS=""
Singularity>  colabfold_batch --num-recycle 5 --pair-mode unpaired --model-type alphafold2_multimer_v3 --num-models 3 example_colabfold/1IH7.7.a3m output
2024-08-16 14:32:29,670 Running colabfold 1.5.5
2024-08-16 14:32:29,722 Unable to initialize backend 'rocm': module 'jaxlib.xla_extension' has no attribute 'GpuAllocatorConfig'
2024-08-16 14:32:29,853 Unable to initialize backend 'tpu': INTERNAL: Failed to open libtpu.so: libtpu.so: cannot open shared object file: No such file or directory
2024-08-16 14:32:29,863 WARNING: no GPU detected, will be using CPU
Traceback (most recent call last):
  File "/opt/miniconda3/bin/colabfold_batch", line 8, in <module>
    sys.exit(main())
  File "/opt/miniconda3/lib/python3.10/site-packages/colabfold/batch.py", line 2031, in main
    run(
  File "/opt/miniconda3/lib/python3.10/site-packages/colabfold/batch.py", line 1286, in run
    from colabfold.alphafold.models import load_models_and_params
  File "/opt/miniconda3/lib/python3.10/site-packages/colabfold/alphafold/models.py", line 4, in <module>
    import haiku
  File "/opt/miniconda3/lib/python3.10/site-packages/haiku/__init__.py", line 20, in <module>
    from haiku import experimental
  File "/opt/miniconda3/lib/python3.10/site-packages/haiku/experimental/__init__.py", line 34, in <module>
    from haiku._src.dot import abstract_to_dot
  File "/opt/miniconda3/lib/python3.10/site-packages/haiku/_src/dot.py", line 163, in <module>
    @jax.linear_util.transformation
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/deprecations.py", line 55, in getattr
    raise AttributeError(f"module {module!r} has no attribute {name!r}")
AttributeError: module 'jax' has no attribute 'linear_util'
```

---

### 评论 #29 — Ruturaj4 (2024-08-16T14:33:13Z)

@dipietrantonio May I know how are you running this commands after spinning the container? Are you cloning colabfold repo?

```
/opt/localcolabfold# colabfold_batch --num-recycle 5 --pair-mode unpaired --model-type alphafold2_multimer_v3 --num-models 3 example_colabfold/1IH7.7.a3m output
2024-08-16 14:28:57,989 Running colabfold 1.5.5 (1ccca5a53d20c909f3ccf8a4b81df804e6717cb1)
Traceback (most recent call last):
  File "/opt/miniconda3/bin/colabfold_batch", line 8, in <module>
    sys.exit(main())
  File "/opt/miniconda3/lib/python3.10/site-packages/colabfold/batch.py", line 2020, in main
    queries, is_complex = get_queries(args.input, args.sort_queries_by)
  File "/opt/miniconda3/lib/python3.10/site-packages/colabfold/batch.py", line 582, in get_queries
    raise OSError(f"{input_path} could not be found")
OSError: example_colabfold/1IH7.7.a3m could not be found
```

---

### 评论 #30 — dipietrantonio (2024-08-16T14:39:34Z)

Dear @Ruturaj4, you are just missing the input file. Check the earlier comment in this thread, I attached the input file:  https://github.com/ROCm/ROCm/issues/3364#issuecomment-2227550732 

---

### 评论 #31 — Ruturaj4 (2024-08-16T15:28:18Z)

@dipietrantonio Thanks. Let me work on a patch. I think we need to use a custom jax+xla for this.

---

### 评论 #32 — Ruturaj4 (2024-08-19T01:12:04Z)

@dipietrantonio your current error can be eliminated by correctly specifying the gpu during docker/ singularity run command.

Please check if the gpus are correctly detected inside the container using `rocm-smi` command. Also, check -> `python -c 'import jax; print(jax.device_count())'`

Do you happen to know the estimated time does it take to run -> `colabfold_batch --num-recycle 3 --pair-mode unpaired --model-type alphafold2_multimer_v3 --num-models 3 1IH7.7.a3m op_`

I tried on small inputs and it works just fine. However, on something like `1IH7.7.a3m` it already took 5-6 hours and hasn't finished yet.

---

### 评论 #33 — dipietrantonio (2024-08-19T01:47:48Z)

Hi @Ruturaj4,

I am indeed running on a node with GPUs, but I still get the error. Interesting that you don't, it means there is something wrong when I build the software..

What GPU are you using to run the `1IH7.7.a3m` input? A MI250X? Usually we face an out of memory error pretty much at the start (see first comments). So if you are past that on a MI250X then we made great progress.

I will ask the researchers we are helping how long it takes, but you don't have to run to completion really.
```
cdipietrantonio@nid002926:/software/projects/pawsey0001/cdipietrantonio/uptake_projects/colabfold> singularity exec colabfold.sif bash
Singularity> rocm-smi


======================================= ROCm System Management Interface =======================================
================================================= Concise Info =================================================
Device  [Model : Revision]    Temp    Power   Partitions      SCLK    MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
        Name (20 chars)       (Edge)  (Avg)   (Mem, Compute)                                                   
================================================================================================================
0       [0x0b0c : 0x00]       43.0°C  0.0W    N/A, N/A        800Mhz  1600Mhz  0%   auto  0.0W      0%   0%    
        AMD INSTINCT MI200 (                                                                                   
1       [0x0b0c : 0x00]       35.0°C  217.0W  N/A, N/A        800Mhz  1600Mhz  0%   auto  560.0W    0%   0%    
        AMD INSTINCT MI200 (                                                                                   
================================================================================================================
============================================= End of ROCm SMI Log ==============================================
Singularity> python -c 'import jax; print(jax.device_count())'
Traceback (most recent call last):
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 887, in backends
    backend = _init_backend(platform)
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 973, in _init_backend
    backend = registration.factory()
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 456, in make_gpu_client
    return xla_client.make_gpu_client(
  File "/opt/miniconda3/lib/python3.10/site-packages/jaxlib/xla_client.py", line 96, in make_gpu_client
    config = _xla.GpuAllocatorConfig()
AttributeError: module 'jaxlib.xla_extension' has no attribute 'GpuAllocatorConfig'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 1050, in device_count
    return int(get_backend(backend).device_count())
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 1019, in get_backend
    return _get_backend_uncached(platform)
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 998, in _get_backend_uncached
    bs = backends()
  File "/opt/miniconda3/lib/python3.10/site-packages/jax/_src/xla_bridge.py", line 903, in backends
    raise RuntimeError(err_msg)
RuntimeError: Unable to initialize backend 'rocm': module 'jaxlib.xla_extension' has no attribute 'GpuAllocatorConfig' (set JAX_PLATFORMS='' to automatically choose an available backend)
Singularity> python3 -c 'import jax; print(jax.__version__)' # print(jax.device_count())'
0.4.31
```

---

### 评论 #34 — uwwint (2024-08-19T02:33:34Z)

> @dipietrantonio Thanks. Let me work on a patch. I think we need to use a custom jax+xla for this.

Sorry for stepping into this. I made exactly that change on a different tangent. In case you want to inline the correct XLA into jax, you need to either touch this file in jax and update the XLA_COMMIT and XLA_SHA256:
https://github.com/ROCm/jax/blob/main/third_party/xla/workspace.bzl

Or you leave all of that the way it is and overlay it with a patch to the JAX build following this recipe: 
https://github.com/ROCm/jax/compare/rocm-jaxlib-v0.4.28...AustralianBioCommons:jax:rocm-jaxlib-v0.4.28-unifiedmemory

My changes are against Rocm 6.0.2, but the same works for 6.2.0. Hope this is helpful.

KR, 
Uwe

---

### 评论 #35 — Ruturaj4 (2024-08-19T04:22:59Z)

@dipietrantonio

How are you building JAX? I use same container above with branches `rocm-jaxlib-v0.4.28-qa`. If possible can you try manually building xla + jax?

I am using something like ->

```
rm -rf dist/ && pip uninstall jax jaxlib -y && /opt/miniconda3/bin/python3 ./build/build.py --enable_rocm --rocm_amdgpu_targets=gfx942 --bazel_options=--override_repository=xla=/release/xla/ --rocm_path=/opt/rocm-6.0.2/ && /opt/miniconda3/bin/python3 setup.py develop --user && /opt/miniconda3/bin/python3 -m pip install dist/*.whl
```

Also, please check how I ran the model ->

1) export `XLA_PYTHON_CLIENT_ALLOCATOR="platform"` will not take the path of https://github.com/ROCm/xla/blob/604ce72901c0df723b958b4200f904f582c76cec/xla/pjrt/gpu/gpu_helpers.cc#L75 and thus will never reach TF_FORCE_UNIFIED_MEMORY flag dereference.
2) Hence, the relevant options may be -> `TF_FORCE_UNIFIED_MEMORY=1` and `XLA_PYTHON_CLIENT_MEM_FRACTION="4.0"`.
3) If `memory_fraction` is 4.0 the amount of memory allocated is 4x the total memory (e.g. `820,271,644,672` bytes (if total memory is `205,067,911,168`. Some is allocated to gpu and the rest is spilled over cpu)).
4) `TF_FORCE_GPU_ALLOW_GROWTH` isn't really captured in XLA. But one can do so here  -> https://github.com/ROCm/xla/blob/604ce72901c0df723b958b4200f904f582c76cec/xla/pjrt/gpu/gpu_helpers.cc#L122 or by setting `XLA_PYTHON_CLIENT_PREALLOCATE`
5) You may increase fraction to fit the data, but please keep in mind the available memory on your machine.
6) In my first investigation, I started with custom_protein.a3m, a very small example to check if the model works
```
> sp|P61823
MALKSLVLLSLLVLVLLL
```
and it worked well.

7) Now I am running bigger model and seems to work fine (not giving me any errors at least). However, it seems like it needs long time to run.

@uwwint 

we use the branch -> `rocm-jaxlib-v0.4.28-qa` for both jax and xla where we already include that patch.

---

### 评论 #36 — dipietrantonio (2024-08-20T06:45:39Z)

@Ruturaj4 the prediction takes 44 hours on a A100 GPU. 

I managed to build a container with the correct version of JAX (the branch mentioned above). I will update you in a few hours.

---

### 评论 #37 — dipietrantonio (2024-08-20T08:52:44Z)

@Ruturaj4 Long story short, I managed to build the container, but when I run it on our system (4x MI250X on each node), I get the following output in `stdout` (`stderr` is empty).

```
2024-08-20 16:43:35,506 Running colabfold 1.5.5
2024-08-20 16:43:53,225 Running on GPU
2024-08-20 16:43:54,219 Found 5 citations for tools or databases
2024-08-20 16:43:54,219 Query 1/1: 1IH7.7 (length 903)
2024-08-20 16:43:56,730 Setting max_seq=508, max_extra_seq=1540
2024-08-20 16:45:15,243 Could not predict 1IH7.7. Not Enough GPU memory? INTERNAL: Failed to launch ROCm kernel: redzone_checker with block dimensions: 1024x1x1: hipError_t(98)
2024-08-20 16:45:15,243 Done
```

From previous runs I can see that unified memory is indeed used (in the following case, I was running on a node with not enough memory. I then moved to a node with 450GB).

```
2024-08-20 16:40:02.497097: E external/xla/xla/stream_executor/rocm/rocm_driver.cc:1345] failed to alloc 270515830784 bytes unified memory; result: HIP_ERROR_OutOfMemory
2024-08-20 16:40:02.502319: E external/xla/xla/stream_executor/rocm/rocm_driver.cc:1345] failed to alloc 243464241152 bytes unified memory; result: HIP_ERROR_OutOfMemory
```

So this is good progress :) 

Edit: now that I remember @SarahBeecroft showed me the same error some time ago..so I ll wait for her to tell me how to fix this.


---

### 评论 #38 — SarahBeecroft (2024-08-21T04:26:22Z)

Hello again @Ruturaj4 :) 

We never got past the 'failed to launch ROCm kernel' error above so unfortunately I don't have a fix for that one. 

I'm attaching a log file from newest run of the container.

We suspect that xla is not installed correctly. the module installed in python3.10/site-packages/jaxlib/xls_extension.so does not contain binary code for gfx90a. jaxlib also has the same issue in /opt/miniconda3/lib/python3.10/site-packages/jaxlib/rocm/_prng.so

If we run with HSA_XNACK=1, we still get the same error. 

[slurm-14769603.txt](https://github.com/user-attachments/files/16685967/slurm-14769603.txt)

Thanks very much!

---

### 评论 #39 — Ruturaj4 (2024-08-23T16:35:52Z)

Thanks @dipietrantonio and @SarahBeecroft let me take a look

remember to ->

unset XLA_PYTHON_CLIENT_ALLOCATOR
export XLA_PYTHON_CLIENT_PREALLOCATE=0

TF_FORCE_UNIFIED_MEMORY=1 and XLA_PYTHON_CLIENT_MEM_FRACTION="4.0".

most important is to not use XLA_PYTHON_CLIENT_ALLOCATOR

---

### 评论 #40 — dipietrantonio (2024-08-26T01:16:06Z)

I did that and I get the error anyway, unfortunately.

---

### 评论 #41 — dipietrantonio (2024-08-28T11:16:35Z)

Dear @Ruturaj4 , usually the error shown in the log Sarah posted means that the code was not compiled for the correct GPU architecture. I did specify the target option, `./build/build.py --enable_rocm --rocm_amdgpu_targets=gfx90a [...]` , and even set `ENV CXXFLAGS=--offload-arch=gfx90a` in the recipe.

Unfortunately I can't build directly on a machine with a MI250X. I am building the container on a virtual machine without GPU access. I think that is where the problem is.

Also, you are doing your experiments on a MI300. Would it be possible to confirm your build works on a MI250X? And if so, could you share the container? It would allow researchers to start using our supercomputer to run ColabFold and doing their research.

Thank you

---

### 评论 #42 — Ruturaj4 (2024-08-28T14:00:35Z)

@dipietrantonio Thanks for letting know.

Yes I tested this on mi300, however one of my colleague tested this on Mi250 as well. Let me confirm that with him.

Let me get back to in a few about container sharing.



---

### 评论 #43 — Ruturaj4 (2024-08-28T14:06:52Z)

My colleague tested this on MI250 and it works fine. He didn't use container, but built everything in a conda environment.

```
export JAX_VERSION=0.4.30
export JAX_PLATFORMS="rocm,cpu"
git clone -b rocm-jaxlib-v${JAX_VERSION}-qa https://github.com/ROCm/xla.git $wd/xla
git clone -b rocm-jaxlib-v${JAX_VERSION}-qa https://github.com/ROCm/jax.git $wd/jax
#rm -rf dist; python3 -m pip uninstall jax jaxlib
 
echo "-----------------------------------Bazel options passing--------------------------------"
 
if [ ! -f $wd/jax/dist/jaxlib-*.whl ] ; then
  cd $wd/jax
  export TEST_TMPDIR=$wd/.bazel
  echo "-----------------------------------bazel with rocm and xla building----------------------------"
  nice python build/build.py --enable_rocm --rocm_path=$ROCM_PATH \
    --rocm_amdgpu_targets=gfx90a \
    --bazel_options=--override_repository=xla=$wd/xla \
    --bazel_options=--jobs=128 \
   --bazel_startup_options=--host_jvm_args=-Xmx512m
##    --bazel_startup_options=--host_jvm_args=-Xms256m
 
  echo "-----------------------------------jaxlib install--------------------------------"
  pip install $wd/jax/dist/jaxlib-*.whl --force-reinstall
##  https://pypi.org/project/tensorflow-rocm/#files
 
  pip install jax==$JAX_VERSION
fi
```



---

### 评论 #44 — SarahBeecroft (2024-08-29T03:57:17Z)

Just to second @dipietrantonio's  comment here- if you are able to build and ship a working container that would be amazing and basically solve all the issues. We can ship some beers to your office in gratitude haha

I'll give the Conda build a shot today on Setonix though.

If a container direct from AMD isn't possible, we could also try to use an AWS instance to build against MI250x. Greg Oakes also talked about getting us access to an AMD internal cluster to try things out, so I've followed that up with him today. I've also raised at Pawsey the idea of us having a GPU node set aside for internal container building. That would take at least a few weeks to get approved and implemented through.

Again, thanks for your help with this! We are getting closer and it'll be a huge deal for Pawsey, AMD, and Australian medical research to get this working. Just think about all the press releases- _AMD helps treat sick kids with AI protein folding breakthrough_

---

### 评论 #45 — dipietrantonio (2024-09-03T07:07:48Z)

Dear @Ruturaj4,

I have managed to compile the software outside a container on a GPU compute node. The error described in https://github.com/ROCm/ROCm/issues/3364#issuecomment-2298327466 is gone, indicating that compilation requires a GPU to be detectable.

The computation runs for about 10 minutes, but then dies with this other error.

stderr:
```
:hip_graph_internal.cpp   :120 : 1770507739737 us: [pid:2822116 tid:0x1516c44521c0] [hipGraph] Add KernelNode(0x273f28f0)
:3:hip_graph.cpp            :1113: 1770507739749 us: [pid:2822116 tid:0x1516c44521c0] hipGraphAddKernelNode: Returned hipSuccess : 
:3:hip_module.cpp           :181 : 1770507739763 us: [pid:2822116 tid:0x1516c44521c0]  hipFuncSetAttribute ( 0x1d254f30, 8, 16384 ) 
:3:hip_module.cpp           :185 : 1770507739775 us: [pid:2822116 tid:0x1516c44521c0] hipFuncSetAttribute: Returned hipSuccess : 
:3:hip_graph.cpp            :1102: 1770507739788 us: [pid:2822116 tid:0x1516c44521c0]  hipGraphAddKernelNode ( 0x1ea505e0, 0x1ee31290, 0x7ffffd1b7688, 1, 0x7ffffd1b7300 ) 
:3:hip_graph_internal.cpp   :120 : 1770507739801 us: [pid:2822116 tid:0x1516c44521c0] [hipGraph] Add KernelNode(0x2517b020)
:3:hip_graph.cpp            :1113: 1770507739813 us: [pid:2822116 tid:0x1516c44521c0] hipGraphAddKernelNode: Returned hipSuccess : 
:3:hip_graph.cpp            :1102: 1770507739828 us: [pid:2822116 tid:0x1516c44521c0]  hipGraphAddKernelNode ( 0x1ea505e8, 0x1ee31290, 0x7ffffd1b7688, 1, 0x7ffffd1b7300 ) 
:3:hip_graph_internal.cpp   :120 : 1770507739842 us: [pid:2822116 tid:0x1516c44521c0] [hipGraph] Add KernelNode(0x270f6540)
:3:hip_graph.cpp            :1113: 1770507739854 us: [pid:2822116 tid:0x1516c44521c0] hipGraphAddKernelNode: Returned hipSuccess : 
:3:hip_graph.cpp            :1102: 1770507739868 us: [pid:2822116 tid:0x1516c44521c0]  hipGraphAddKernelNode ( 0x1ea505f0, 0x1ee31290, 0x7ffffd1b7688, 1, 0x7ffffd1b7300 ) 
:3:hip_graph.cpp            :1113: 1770507739881 us: [pid:2822116 tid:0x1516c44521c0] hipGraphAddKernelNode: Returned hipErrorInvalidConfiguration : 
E0903 08:21:32.186647 2822116 pjrt_stream_executor_client.cc:2826] Execution of replica 0 failed: INTERNAL: Failed to add kernel node to a HIP graph: hipError_t(9)
```


stdout:
```
2024-09-03 14:46:17,662 Running colabfold 1.5.5
2024-09-03 14:46:35,455 Running on GPU
2024-09-03 14:46:36,467 Found 5 citations for tools or databases
2024-09-03 14:46:36,468 Query 1/1: 1IH7.7 (length 903)
2024-09-03 14:46:38,983 Setting max_seq=508, max_extra_seq=1540
2024-09-03 14:55:41,556 Could not predict 1IH7.7. Not Enough GPU memory? INTERNAL: Failed to add kernel node to a HIP graph: hipError_t(9)
2024-09-03 14:55:41,556 Done
```

I tried to compile with both ROCm 6.1.0 and 6.2.0. I get the same error. 

During the computation, I see the following stats on `rocm-smi`. They are constant throughout the 10 minutes.
```
======================= ROCm System Management Interface =======================
================================= Concise Info =================================
GPU  Temp   AvgPwr  SCLK    MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
0    41.0c  96.0W   800Mhz  1600Mhz  0%   auto  560.0W    1%   0%    
1    31.0c  N/A     800Mhz  1600Mhz  0%   auto  0.0W      1%   0%    
2    34.0c  92.0W   800Mhz  1600Mhz  0%   auto  560.0W    1%   0%    
3    35.0c  N/A     800Mhz  1600Mhz  0%   auto  0.0W      1%   0%    
4    35.0c  93.0W   800Mhz  1600Mhz  0%   auto  560.0W    1%   0%    
5    43.0c  N/A     800Mhz  1600Mhz  0%   auto  0.0W      1%   0%    
6    35.0c  87.0W   800Mhz  1600Mhz  0%   auto  560.0W    1%   0%    
7    37.0c  N/A     800Mhz  1600Mhz  0%   auto  0.0W      1%   0%    
================================================================================
============================= End of ROCm SMI Log ==============================
cdipietrantonio@nid002980:~> rocm-smi --showpids


======================= ROCm System Management Interface =======================
================================ KFD Processes =================================
KFD process information:
PID    	PROCESS NAME   	GPU(s)	VRAM USED 	SDMA USED	CU OCCUPANCY	
3458806	colabfold_batch	8     	1254109184	0        	0           	
================================================================================
============================= End of ROCm SMI Log ==============================
```


.. and `top` gives this
```    
PID           USER       PR NI VIRT       RES      SHR       S %CPU%MEM     TIME+ COMMAND                                                                                                                                                                                                                         
3493998 cdipiet+  20  0  82.973g 8.707g 324328 R 100.3 1.733   7:13.73 colabfold_batch           
```

Any ideas?

---

### 评论 #46 — dipietrantonio (2024-09-04T01:38:01Z)

Grepping for "error" in the stderr output, I get

```
:3:hip_error.cpp            :36  : 1860534317681 us: [pid:3243700 tid:0x14944785a740]  hipGetLastError (  ) 
:3:hip_module.cpp           :85  : 1860534331522 us: [pid:3243700 tid:0x14944785a740] hipModuleGetFunction: Returned hipErrorNotFound : 
:3:hip_error.cpp            :36  : 1860534331534 us: [pid:3243700 tid:0x14944785a740]  hipGetLastError (  ) 
:3:hip_module.cpp           :85  : 1860534348192 us: [pid:3243700 tid:0x14944785a740] hipModuleGetFunction: Returned hipErrorNotFound : 
:3:hip_error.cpp            :36  : 1860534348203 us: [pid:3243700 tid:0x14944785a740]  hipGetLastError (  ) 
:3:hip_module.cpp           :85  : 1860534364834 us: [pid:3243700 tid:0x14944785a740] hipModuleGetFunction: Returned hipErrorNotFound : 
:3:hip_error.cpp            :36  : 1860534364845 us: [pid:3243700 tid:0x14944785a740]  hipGetLastError (  ) 
:3:hip_module.cpp           :85  : 1860534382063 us: [pid:3243700 tid:0x14944785a740] hipModuleGetFunction: Returned hipErrorNotFound : 
:3:hip_error.cpp            :36  : 1860534382074 us: [pid:3243700 tid:0x14944785a740]  hipGetLastError (  ) 
:3:hip_graph.cpp            :1036: 1861027810613 us: [pid:3243700 tid:0x14944785a740] hipGraphAddKernelNode: Returned hipErrorInvalidConfiguration : 
E0904 09:30:05.065742 3243700 pjrt_stream_executor_client.cc:2826] Execution of replica 0 failed: INTERNAL: Failed to add kernel node to a HIP graph: hipError_t(9)
```

---

### 评论 #47 — dipietrantonio (2024-09-04T01:42:45Z)

I suppose this is not a Unified Memory issue anymore, and we can consider this as resolved. Should I open a new Issue for the error above?


---

### 评论 #48 — dipietrantonio (2024-09-04T03:08:51Z)

Upon inspecting the log more carefully (see below), I suspect the following. JAX/XLA is trying to generate the compute kernel at runtime and perform JIT compilation. However, when later it creates the computational graph with HIP Graph, that kernel's object code is not found. Hence it cannot be added to the graph.

```
:3:hip_module.cpp           :74  : 305270480312 us: [pid:312732 tid:0x15533460c740]  hipModuleGetFunction ( 0x7ffd650e5788, 0x559d78ba0e70, Cijk_Ailk_Bljk_SB_MT128x96x16_MI32x32x2x1_SN_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASM_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_CLR0_DTLA0_DTLB0_DTVA0_DTVB0_DVO0_ETSP_EPS1_ELFLR0_EMLL0_FSSC10_FL0_GLVWA2_GLVWB2_GRCGA1_GRCGB1_GRPM1_GRVW2_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPPA0_LBSPPB128_LPA0_LPB4_LDL1_LRVW4_LWPMn1_LDW0_FMA_MIAV1_MDA2_MO40_MMFGLC_MKFGSU256_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR9_SIA1_SS0_SU0_SUM0_SUS0_SCIUI1_SPO0_SRVW0_SSO4_SVW4_SNLL0_TSGRA0_TSGRB0_TT1_96_TLDS1_UMLDSA0_UMLDSB1_U64SL1_USFGROn1_VAW1_VSn1_VW1_VWB1_VFLRP0_WSGRA0_WSGRB0_WS64_WG128_2_1_WGM15 ) 
:1:hip_code_object.cpp      :624 : 305270480327 us: [pid:312732 tid:0x15533460c740] Cannot find the function: Cijk_Ailk_Bljk_SB_MT128x96x16_MI32x32x2x1_SN_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASM_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_CLR0_DTLA0_DTLB0_DTVA0_DTVB0_DVO0_ETSP_EPS1_ELFLR0_EMLL0_FSSC10_FL0_GLVWA2_GLVWB2_GRCGA1_GRCGB1_GRPM1_GRVW2_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPPA0_LBSPPB128_LPA0_LPB4_LDL1_LRVW4_LWPMn1_LDW0_FMA_MIAV1_MDA2_MO40_MMFGLC_MKFGSU256_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR9_SIA1_SS0_SU0_SUM0_SUS0_SCIUI1_SPO0_SRVW0_SSO4_SVW4_SNLL0_TSGRA0_TSGRB0_TT1_96_TLDS1_UMLDSA0_UMLDSB1_U64SL1_USFGROn1_VAW1_VSn1_VW1_VWB1_VFLRP0_WSGRA0_WSGRB0_WS64_WG128_2_1_WGM15 
:1:hip_module.cpp           :84  : 305270480339 us: [pid:312732 tid:0x15533460c740] Cannot find the function: Cijk_Ailk_Bljk_SB_MT128x96x16_MI32x32x2x1_SN_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASM_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_CLR0_DTLA0_DTLB0_DTVA0_DTVB0_DVO0_ETSP_EPS1_ELFLR0_EMLL0_FSSC10_FL0_GLVWA2_GLVWB2_GRCGA1_GRCGB1_GRPM1_GRVW2_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPPA0_LBSPPB128_LPA0_LPB4_LDL1_LRVW4_LWPMn1_LDW0_FMA_MIAV1_MDA2_MO40_MMFGLC_MKFGSU256_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR9_SIA1_SS0_SU0_SUM0_SUS0_SCIUI1_SPO0_SRVW0_SSO4_SVW4_SNLL0_TSGRA0_TSGRB0_TT1_96_TLDS1_UMLDSA0_UMLDSB1_U64SL1_USFGROn1_VAW1_VSn1_VW1_VWB1_VFLRP0_WSGRA0_WSGRB0_WS64_WG128_2_1_WGM15 for module: 0x78ba0e70
:3:hip_module.cpp           :85  : 305270480350 us: [pid:312732 tid:0x15533460c740] hipModuleGetFunction: Returned hipErrorNotFound : 
:3:hip_error.cpp            :36  : 305270480362 us: [pid:312732 tid:0x15533460c740]  hipGetLastError (  ) 
:3:hip_module.cpp           :74  : 305270480374 us: [pid:312732 tid:0x15533460c740]  hipModuleGetFunction ( 0x7ffd650e5788, 0x559d7aa260b0, Cijk_Ailk_Bljk_SB_MT128x96x16_MI32x32x2x1_SN_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASM_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_CLR0_DTLA0_DTLB0_DTVA0_DTVB0_DVO0_ETSP_EPS1_ELFLR0_EMLL0_FSSC10_FL0_GLVWA2_GLVWB2_GRCGA1_GRCGB1_GRPM1_GRVW2_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPPA0_LBSPPB128_LPA0_LPB4_LDL1_LRVW4_LWPMn1_LDW0_FMA_MIAV1_MDA2_MO40_MMFGLC_MKFGSU256_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR9_SIA1_SS0_SU0_SUM0_SUS0_SCIUI1_SPO0_SRVW0_SSO4_SVW4_SNLL0_TSGRA0_TSGRB0_TT1_96_TLDS1_UMLDSA0_UMLDSB1_U64SL1_USFGROn1_VAW1_VSn1_VW1_VWB1_VFLRP0_WSGRA0_WSGRB0_WS64_WG128_2_1_WGM15 ) 
:3:hip_module.cpp           :88  : 305270480397 us: [pid:312732 tid:0x15533460c740] hipModuleGetFunction: Returned hipSuccess : 
:3:hip_module.cpp           :470 : 305270480415 us: [pid:312732 tid:0x15533460c740]  hipExtModuleLaunchKernel ( 0x0x559d7d771340, 768, 66, 1, 256, 1, 1, 0, stream:0x559d688e6a50, char array:<null>, 0x7ffd650e57d0, event:0, event:0, 0 ) 
:3:rocvirtual.cpp           :798 : 305270480430 us: [pid:312732 tid:0x15533460c740] Arg0:  Tensor2dSizeA = val:110592
:3:rocvirtual.cpp           :798 : 305270480442 us: [pid:312732 tid:0x15533460c740] Arg1:  Tensor2dSizeB = val:2427264
:3:rocvirtual.cpp           :798 : 305270480453 us: [pid:312732 tid:0x15533460c740] Arg2:  AddressD = val:23372033148928
:3:rocvirtual.cpp           :798 : 305270480465 us: [pid:312732 tid:0x15533460c740] Arg3:  AddressC = val:23372033148928
--
:3:hip_graph.cpp            :1024: 305757611363 us: [pid:312732 tid:0x15533460c740]  hipGraphAddKernelNode ( 0x559d777c1cb0, 0x559d7f33a2c0, 0x7ffd650ed648, 1, 0x7ffd650ed2c0 ) 
:3:hip_graph_internal.cpp   :129 : 305757611376 us: [pid:312732 tid:0x15533460c740] [hipGraph] Add KernelNode(0x559d887c3bf0)
:3:hip_graph.cpp            :1036: 305757611388 us: [pid:312732 tid:0x15533460c740] hipGraphAddKernelNode: Returned hipSuccess : 
:3:hip_graph.cpp            :1024: 305757611403 us: [pid:312732 tid:0x15533460c740]  hipGraphAddKernelNode ( 0x559d777c1cb8, 0x559d7f33a2c0, 0x7ffd650ed648, 1, 0x7ffd650ed2c0 ) 
:3:hip_graph_internal.cpp   :129 : 305757611426 us: [pid:312732 tid:0x15533460c740] [hipGraph] Add KernelNode(0x559d83e52510)
:3:hip_graph.cpp            :1036: 305757611439 us: [pid:312732 tid:0x15533460c740] hipGraphAddKernelNode: Returned hipSuccess : 
:3:hip_graph.cpp            :1024: 305757611454 us: [pid:312732 tid:0x15533460c740]  hipGraphAddKernelNode ( 0x559d777c1cc0, 0x559d7f33a2c0, 0x7ffd650ed648, 1, 0x7ffd650ed2c0 ) 
:3:hip_graph.cpp            :1036: 305757611467 us: [pid:312732 tid:0x15533460c740] hipGraphAddKernelNode: Returned hipErrorInvalidConfiguration : 
E0904 10:53:24.344123  312732 pjrt_stream_executor_client.cc:2826] Execution of replica 0 failed: INTERNAL: Failed to add kernel node to a HIP graph: hipError_t(9)

```

---

### 评论 #49 — Ruturaj4 (2024-09-04T14:37:36Z)

Thanks @dipietrantonio and @SarahBeecroft. we had long weekend in the US last week.

thanks for additional info and logs @dipietrantonio. Let me talk to my colleague who built and tested this in mi250 and get back to you if we can arrange a container for you.

---

### 评论 #50 — dipietrantonio (2024-09-11T08:00:46Z)

Any news @Ruturaj4 ?

---

### 评论 #51 — Ruturaj4 (2024-09-11T13:41:20Z)

Sorry about delay. My colleague had requested an access to the the Pawsey machine and now has an access to it, however, the institution is having a network issue that prevents downloading packages including jax/xla. He said that the engineers are working on solving the technical issue.

---

### 评论 #52 — dipietrantonio (2024-10-02T01:33:39Z)

Hi @Ruturaj4, how is your colleague going on Setonix? Did he manage to run the software? I would be happy to enter in contact with him or her to help get things running.

---

### 评论 #53 — Ruturaj4 (2024-10-02T02:15:27Z)

Greetings, @dipietrantonio. He told me that he has already in contact with @SarahBeecroft!

---

### 评论 #54 — dipietrantonio (2024-10-02T02:25:14Z)

@Ruturaj4 that is right, Sarah told me he has issues building the software natively on Setonix. I built the software on Setonix without containers or conda, thanks to the help of Sarah and other people, but then I face the error I presented in https://github.com/ROCm/ROCm/issues/3364#issuecomment-2327826232 . I think it would be productive if this person could enter in contact with me directly (cdipietrantonio [at] pawey.org.au ) so that we could put our minds together and try to solve the issue.

---

### 评论 #55 — Ruturaj4 (2024-10-02T14:08:51Z)

@dipietrantonio Yup, I think so too. I will let him know to contact you!

---

### 评论 #56 — dipietrantonio (2024-12-02T00:23:08Z)

Dear all, the original issue has been resolved, in that managed memory is now used. Hence, I will close this ticket and open a new issue regarding the kernel generation error.

Thanks to all the people who helped on this issue, your efforts were invaluable and greatly appreciated.

---
