# Cannot run YuE on my Radeon 7800XT

> **Issue #4578**
> **状态**: closed
> **创建时间**: 2025-04-09T21:48:15Z
> **更新时间**: 2025-05-16T21:53:03Z
> **关闭时间**: 2025-05-16T21:49:40Z
> **作者**: hartmark
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4578

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

I posted reproduction steps on their repo:

https://github.com/multimodal-art-projection/YuE/issues/110#issue-2959200214

Can anyone please try and see if they can get it working or a way to get it working.

---

## 评论 (18 条)

### 评论 #1 — ppanchad-amd (2025-04-10T14:22:24Z)

Hi @hartmark. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — zgauthier2000 (2025-04-16T14:25:44Z)

I don't believe there's any solution to use flash attention with a 7800XT right now. Please, please, correct me if I'm wrong. My guess is that your best bet is this:
https://github.com/lamikr/rocm_sdk_builder

...but I haven't been able to get the 633 branch to build.


From your other post, it looks like ROCm doesn't see your GPU at all. You can (as of 6.3.3 at least) get it to run on your 7800XT if you set the environmental variable `HSA_OVERRIDE_GFX_VERSION=11.0.0` (pretend to be a 7900XT) before running your application.

---

### 评论 #3 — tcgu-amd (2025-04-16T19:08:56Z)

@hartmark @zgauthier2000, thanks for reaching out! ROCm's flash attention implementation currently has 2 versions, one relies on the Composable Kernel backend, and one using the Triton backend. The CK version, as @zgauthier2000 mentioned, only supports MI200 and MI300 cards. The Triton version should support RDNA cards such as 7800XT, but is currently a work-in-progress with many features unavailable.

It is worth nothing that the "official release" of Flash-Attention's ROCm version is actually hosted on the Dao-AILab's official repo https://github.com/Dao-AILab/flash-attention instead of under ROCm. Please install the version from the main branch there.

@zgauthier2000, based on your logs, seems like the you installed the version hosted under ROCm. Please try the official version. Also, it seems like your GPU is not being recognized. Can you run rocminfo and show the outputs? Thanks! 

---

### 评论 #4 — hartmark (2025-04-16T23:36:29Z)

I tried using the main branch of the upstream repo. But it went even worse as I cannot build it.

`FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE" python setup.py install`

[build.log](https://github.com/user-attachments/files/19785888/build.log)

---

### 评论 #5 — zgauthier2000 (2025-04-16T23:53:02Z)

> I tried using the main branch of the upstream repo. But it went even worse as I cannot build it.
> 
> `FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE" python setup.py install`
> 
> [build.log](https://github.com/user-attachments/files/19785888/build.log)

I also tried building it, and mine compiled, but, trying to use flash attention, in ComfyUI, results in the ksampler bailing with:

```
AssertionError: expected size 4288==4288, stride 128==3072 at dim=1; expected size 24==24, stride 548864==128 at dim=2
This error most often comes from a incorrect fake (aka meta) kernel for a custom op.

```

---

### 评论 #6 — hartmark (2025-04-17T00:14:03Z)

> I also tried building it, and mine compiled, but, trying to use flash attention, in ComfyUI, results in the ksampler bailing with:
> 
> ```
> AssertionError: expected size 4288==4288, stride 128==3072 at dim=1; expected size 24==24, stride 548864==128 at dim=2
> This error most often comes from a incorrect fake (aka meta) kernel for a custom op.
> ```

I'm building it in a venv like the linked issue, how are you building flash attention?

---

### 评论 #7 — hartmark (2025-04-17T00:39:12Z)

I got flash attention compiling now, seems I borked my repo when I tried to revert to main-branch of upstream repo.

I have also changed so I use ROCm 6.3.4

I rebuilt recreated my venv and ran this commands:

```
pip install -r <(curl -sSL https://raw.githubusercontent.com/multimodal-art-projection/YuE/main/requirements.txt)\npip3 install torch==2.4.0 torchaudio torchvision==0.19.0 pytorch_triton -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4
pip install -r <(curl -sSL https://raw.githubusercontent.com/multimodal-art-projection/YuE/main/requirements.txt)

git clone git@github.com:Dao-AILab/flash-attention.git
cd flash-attention
FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE" python setup.py install

cd .../inference
HSA_OVERRIDE_GFX_VERSION=11.0.0 python infer.py \
    --cuda_idx 0 \
    --stage1_model m-a-p/YuE-s1-7B-anneal-en-cot \
    --stage2_model m-a-p/YuE-s2-1B-general \
    --genre_txt ../prompt_egs/genre.txt \
    --lyrics_txt ../prompt_egs/lyrics.txt \
    --run_n_segments 2 \
    --stage2_batch_size 4 \
    --output_dir ../output \
    --max_new_tokens 3000 \
    --repetition_penalty 1.1
```

Now I get this error:
```
amdgpu.ids: No such file or directory
Traceback (most recent call last):
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/utils/import_utils.py", line 1967, in _get_module
    return importlib.import_module("." + module_name, self.__name__)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/.pyenv/versions/3.12.8/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/models/whisper/modeling_whisper.py", line 30, in <module>
    from ...modeling_flash_attention_utils import flash_attn_supports_top_left_mask, is_flash_attn_available
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/modeling_flash_attention_utils.py", line 36, in <module>
    from flash_attn.bert_padding import index_first_axis, pad_input, unpad_input  # noqa
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/flash_attn-2.7.4.post1-py3.12.egg/flash_attn/__init__.py", line 3, in <module>
    from flash_attn.flash_attn_interface import (
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/flash_attn-2.7.4.post1-py3.12.egg/flash_attn/flash_attn_interface.py", line 15, in <module>
    import flash_attn_2_cuda as flash_attn_gpu
ModuleNotFoundError: No module named 'flash_attn_2_cuda'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/markus/code/YuE/inference/infer.py", line 22, in <module>
    from models.soundstream_hubert_new import SoundStream
  File "/home/markus/code/YuE/inference/xcodec_mini_infer/models/soundstream_hubert_new.py", line 18, in <module>
    from transformers import AutoFeatureExtractor, WhisperModel
  File "<frozen importlib._bootstrap>", line 1412, in _handle_fromlist
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/utils/import_utils.py", line 1956, in __getattr__
    value = getattr(module, name)
            ^^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/utils/import_utils.py", line 1955, in __getattr__
    module = self._get_module(self._class_to_module[name])
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/utils/import_utils.py", line 1969, in _get_module
    raise RuntimeError(
RuntimeError: Failed to import transformers.models.whisper.modeling_whisper because of the following error (look up to see its traceback):
No module named 'flash_attn_2_cuda'
```

ROCm is properly detected, this command:
```
python <<EOF                                     
import torch
import sys

try:
    print("PyTorch version:", torch.__version__)
    cuda_available = torch.cuda.is_available()
    print("Is CUDA available:", cuda_available)
    if cuda_available:
        print("CUDA device count:", torch.cuda.device_count())
        print("CUDA device name:", torch.cuda.get_device_name(0))
    else:
        print("No CUDA device found")
        sys.exit(1)
except Exception as e:
    print("Error:", e)
    sys.exit(1)  # Exit with 1 for other errors
EOF
```
Gives me:
```
PyTorch version: 2.4.0+rocm6.3.4.git7cecbf6d
amdgpu.ids: No such file or directory
Is CUDA available: True
CUDA device count: 1
CUDA device name: AMD Radeon Graphics
```

---

### 评论 #8 — tcgu-amd (2025-04-17T14:43:52Z)

@hartmark, seems like `flash_attn_2_cuda` module cannot be found after the installation. Have you gave https://github.com/Dao-AILab/flash-attention/issues/933#issuecomment-2552588779 a try?

---

### 评论 #9 — hartmark (2025-04-18T18:46:04Z)

> [@hartmark](https://github.com/hartmark), seems like `flash_attn_2_cuda` module cannot be found after the installation. Have you gave [Dao-AILab/flash-attention#933 (comment)](https://github.com/Dao-AILab/flash-attention/issues/933#issuecomment-2552588779) a try?

If I run without the **FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"** flag it won't compile and I get the same error as https://github.com/ROCm/ROCm/issues/4578#issuecomment-2811202232

And running with both **FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"** and **FLASH_ATTENTION_SKIP_CUDA_BUILD=FALSE** doesn't yield me any flash_attn_2_cuda module either.

```
(venv-3.12) ➜  code$ mkdir temp
(venv-3.12) ➜  code$ cd temp
(venv-3.12) ➜  temp> git clone git@github.com:Dao-AILab/flash-attention.git
Cloning into 'flash-attention'...
remote: Enumerating objects: 9462, done.
remote: Counting objects: 100% (487/487), done.
remote: Compressing objects: 100% (254/254), done.
remote: Total 9462 (delta 383), reused 233 (delta 233), pack-reused 8975 (from 4)
Receiving objects: 100% (9462/9462), 9.21 MiB | 10.47 MiB/s, done.
Resolving deltas: 100% (7317/7317), done.
(venv-3.12) ➜  temp$ cd flash-attention 
(venv-3.12) ➜  flash-attention git:(main) FLASH_ATTENTION_SKIP_CUDA_BUILD=FALSE FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE" python setup.py install


Submodule 'csrc/composable_kernel' (https://github.com/ROCm/composable_kernel.git) registered for path 'csrc/composable_kernel'
Cloning into '/home/markus/code/temp/flash-attention/csrc/composable_kernel'...
Submodule path 'csrc/composable_kernel': checked out '72c0261ef1b40587ee8674b9d49b4fd6b46b0335'
Submodule 'csrc/cutlass' (https://github.com/NVIDIA/cutlass.git) registered for path 'csrc/cutlass'
Cloning into '/home/markus/code/temp/flash-attention/csrc/cutlass'...
Submodule path 'csrc/cutlass': checked out '62750a2b75c802660e4894434dc55e839f322277'


torch.__version__  = 2.4.0+rocm6.3.4.git7cecbf6d


/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/setuptools/__init__.py:94: _DeprecatedInstaller: setuptools.installer and fetch_build_eggs are deprecated.
!!

        ********************************************************************************
        Requirements should be satisfied by a PEP 517 installer.
        If you are using pip, you can try `pip install --use-pep517`.
        ********************************************************************************

!!
  dist.fetch_build_eggs(dist.setup_requires)
/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/setuptools/dist.py:759: SetuptoolsDeprecationWarning: License classifiers are deprecated.
!!

        ********************************************************************************
        Please consider removing the following classifiers in favor of a SPDX license expression:

        License :: OSI Approved :: BSD License

        See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license for details.
        ********************************************************************************

!!
  self._finalize_license_expression()
running install
/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/setuptools/_distutils/cmd.py:90: SetuptoolsDeprecationWarning: setup.py install is deprecated.
!!

        ********************************************************************************
        Please avoid running ``setup.py`` directly.
        Instead, use pypa/build, pypa/installer or other
        standards-based tools.

        See https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html for details.
        ********************************************************************************

!!
  self.initialize_options()
/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/setuptools/_distutils/cmd.py:90: EasyInstallDeprecationWarning: easy_install command is deprecated.
!!

        ********************************************************************************
        Please avoid running ``setup.py`` and ``easy_install``.
        Instead, use pypa/build, pypa/installer or other
        standards-based tools.

        See https://github.com/pypa/setuptools/issues/917 for details.
        ********************************************************************************

!!
  self.initialize_options()
running bdist_egg
running egg_info
creating flash_attn.egg-info
writing flash_attn.egg-info/PKG-INFO
writing dependency_links to flash_attn.egg-info/dependency_links.txt
writing requirements to flash_attn.egg-info/requires.txt
writing top-level names to flash_attn.egg-info/top_level.txt
writing manifest file 'flash_attn.egg-info/SOURCES.txt'
reading manifest file 'flash_attn.egg-info/SOURCES.txt'
reading manifest template 'MANIFEST.in'
warning: no files found matching '*.cu' under directory 'flash_attn'
warning: no files found matching '*.h' under directory 'flash_attn'
warning: no files found matching '*.cuh' under directory 'flash_attn'
warning: no files found matching '*.cpp' under directory 'flash_attn'
warning: no files found matching '*.hpp' under directory 'flash_attn'
adding license file 'LICENSE'
adding license file 'AUTHORS'
writing manifest file 'flash_attn.egg-info/SOURCES.txt'
installing library code to build/bdist.linux-x86_64/egg
running install_lib
running build_py
creating build/lib/flash_attn
copying flash_attn/__init__.py -> build/lib/flash_attn
copying flash_attn/bert_padding.py -> build/lib/flash_attn
copying flash_attn/flash_attn_interface.py -> build/lib/flash_attn
copying flash_attn/flash_attn_triton.py -> build/lib/flash_attn
copying flash_attn/flash_attn_triton_og.py -> build/lib/flash_attn
copying flash_attn/flash_blocksparse_attention.py -> build/lib/flash_attn
copying flash_attn/flash_blocksparse_attn_interface.py -> build/lib/flash_attn
copying flash_attn/fused_softmax.py -> build/lib/flash_attn
creating build/lib/hopper
copying hopper/__init__.py -> build/lib/hopper
copying hopper/benchmark_attn.py -> build/lib/hopper
copying hopper/benchmark_flash_attention_fp8.py -> build/lib/hopper
copying hopper/benchmark_mla_decode.py -> build/lib/hopper
copying hopper/benchmark_split_kv.py -> build/lib/hopper
copying hopper/flash_attn_interface.py -> build/lib/hopper
copying hopper/generate_kernels.py -> build/lib/hopper
copying hopper/padding.py -> build/lib/hopper
copying hopper/setup.py -> build/lib/hopper
copying hopper/test_attn_kvcache.py -> build/lib/hopper
copying hopper/test_flash_attn.py -> build/lib/hopper
copying hopper/test_kvcache.py -> build/lib/hopper
copying hopper/test_util.py -> build/lib/hopper
creating build/lib/flash_attn/flash_attn_triton_amd
copying flash_attn/flash_attn_triton_amd/__init__.py -> build/lib/flash_attn/flash_attn_triton_amd
copying flash_attn/flash_attn_triton_amd/bench.py -> build/lib/flash_attn/flash_attn_triton_amd
copying flash_attn/flash_attn_triton_amd/bwd_prefill.py -> build/lib/flash_attn/flash_attn_triton_amd
copying flash_attn/flash_attn_triton_amd/bwd_ref.py -> build/lib/flash_attn/flash_attn_triton_amd
copying flash_attn/flash_attn_triton_amd/fwd_decode.py -> build/lib/flash_attn/flash_attn_triton_amd
copying flash_attn/flash_attn_triton_amd/fwd_prefill.py -> build/lib/flash_attn/flash_attn_triton_amd
copying flash_attn/flash_attn_triton_amd/fwd_ref.py -> build/lib/flash_attn/flash_attn_triton_amd
copying flash_attn/flash_attn_triton_amd/interface_fa.py -> build/lib/flash_attn/flash_attn_triton_amd
copying flash_attn/flash_attn_triton_amd/interface_torch.py -> build/lib/flash_attn/flash_attn_triton_amd
copying flash_attn/flash_attn_triton_amd/test.py -> build/lib/flash_attn/flash_attn_triton_amd
copying flash_attn/flash_attn_triton_amd/utils.py -> build/lib/flash_attn/flash_attn_triton_amd
creating build/lib/flash_attn/layers
copying flash_attn/layers/__init__.py -> build/lib/flash_attn/layers
copying flash_attn/layers/patch_embed.py -> build/lib/flash_attn/layers
copying flash_attn/layers/rotary.py -> build/lib/flash_attn/layers
creating build/lib/flash_attn/losses
copying flash_attn/losses/__init__.py -> build/lib/flash_attn/losses
copying flash_attn/losses/cross_entropy.py -> build/lib/flash_attn/losses
creating build/lib/flash_attn/models
copying flash_attn/models/__init__.py -> build/lib/flash_attn/models
copying flash_attn/models/baichuan.py -> build/lib/flash_attn/models
copying flash_attn/models/bert.py -> build/lib/flash_attn/models
copying flash_attn/models/bigcode.py -> build/lib/flash_attn/models
copying flash_attn/models/btlm.py -> build/lib/flash_attn/models
copying flash_attn/models/falcon.py -> build/lib/flash_attn/models
copying flash_attn/models/gpt.py -> build/lib/flash_attn/models
copying flash_attn/models/gpt_neox.py -> build/lib/flash_attn/models
copying flash_attn/models/gptj.py -> build/lib/flash_attn/models
copying flash_attn/models/llama.py -> build/lib/flash_attn/models
copying flash_attn/models/opt.py -> build/lib/flash_attn/models
copying flash_attn/models/vit.py -> build/lib/flash_attn/models
creating build/lib/flash_attn/modules
copying flash_attn/modules/__init__.py -> build/lib/flash_attn/modules
copying flash_attn/modules/block.py -> build/lib/flash_attn/modules
copying flash_attn/modules/embedding.py -> build/lib/flash_attn/modules
copying flash_attn/modules/mha.py -> build/lib/flash_attn/modules
copying flash_attn/modules/mlp.py -> build/lib/flash_attn/modules
creating build/lib/flash_attn/ops
copying flash_attn/ops/__init__.py -> build/lib/flash_attn/ops
copying flash_attn/ops/activations.py -> build/lib/flash_attn/ops
copying flash_attn/ops/fused_dense.py -> build/lib/flash_attn/ops
copying flash_attn/ops/layer_norm.py -> build/lib/flash_attn/ops
copying flash_attn/ops/rms_norm.py -> build/lib/flash_attn/ops
creating build/lib/flash_attn/utils
copying flash_attn/utils/__init__.py -> build/lib/flash_attn/utils
copying flash_attn/utils/benchmark.py -> build/lib/flash_attn/utils
copying flash_attn/utils/distributed.py -> build/lib/flash_attn/utils
copying flash_attn/utils/generation.py -> build/lib/flash_attn/utils
copying flash_attn/utils/pretrained.py -> build/lib/flash_attn/utils
copying flash_attn/utils/torch.py -> build/lib/flash_attn/utils
creating build/lib/flash_attn/ops/triton
copying flash_attn/ops/triton/__init__.py -> build/lib/flash_attn/ops/triton
copying flash_attn/ops/triton/cross_entropy.py -> build/lib/flash_attn/ops/triton
copying flash_attn/ops/triton/k_activations.py -> build/lib/flash_attn/ops/triton
copying flash_attn/ops/triton/layer_norm.py -> build/lib/flash_attn/ops/triton
copying flash_attn/ops/triton/linear.py -> build/lib/flash_attn/ops/triton
copying flash_attn/ops/triton/mlp.py -> build/lib/flash_attn/ops/triton
copying flash_attn/ops/triton/rotary.py -> build/lib/flash_attn/ops/triton
creating build/bdist.linux-x86_64/egg
creating build/bdist.linux-x86_64/egg/flash_attn
copying build/lib/flash_attn/__init__.py -> build/bdist.linux-x86_64/egg/flash_attn
copying build/lib/flash_attn/bert_padding.py -> build/bdist.linux-x86_64/egg/flash_attn
copying build/lib/flash_attn/flash_attn_interface.py -> build/bdist.linux-x86_64/egg/flash_attn
copying build/lib/flash_attn/flash_attn_triton.py -> build/bdist.linux-x86_64/egg/flash_attn
copying build/lib/flash_attn/flash_attn_triton_og.py -> build/bdist.linux-x86_64/egg/flash_attn
copying build/lib/flash_attn/flash_blocksparse_attention.py -> build/bdist.linux-x86_64/egg/flash_attn
copying build/lib/flash_attn/flash_blocksparse_attn_interface.py -> build/bdist.linux-x86_64/egg/flash_attn
copying build/lib/flash_attn/fused_softmax.py -> build/bdist.linux-x86_64/egg/flash_attn
creating build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
copying build/lib/flash_attn/flash_attn_triton_amd/__init__.py -> build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
copying build/lib/flash_attn/flash_attn_triton_amd/bench.py -> build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
copying build/lib/flash_attn/flash_attn_triton_amd/bwd_prefill.py -> build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
copying build/lib/flash_attn/flash_attn_triton_amd/bwd_ref.py -> build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
copying build/lib/flash_attn/flash_attn_triton_amd/fwd_decode.py -> build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
copying build/lib/flash_attn/flash_attn_triton_amd/fwd_prefill.py -> build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
copying build/lib/flash_attn/flash_attn_triton_amd/fwd_ref.py -> build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
copying build/lib/flash_attn/flash_attn_triton_amd/interface_fa.py -> build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
copying build/lib/flash_attn/flash_attn_triton_amd/interface_torch.py -> build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
copying build/lib/flash_attn/flash_attn_triton_amd/test.py -> build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
copying build/lib/flash_attn/flash_attn_triton_amd/utils.py -> build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd
creating build/bdist.linux-x86_64/egg/flash_attn/layers
copying build/lib/flash_attn/layers/__init__.py -> build/bdist.linux-x86_64/egg/flash_attn/layers
copying build/lib/flash_attn/layers/patch_embed.py -> build/bdist.linux-x86_64/egg/flash_attn/layers
copying build/lib/flash_attn/layers/rotary.py -> build/bdist.linux-x86_64/egg/flash_attn/layers
creating build/bdist.linux-x86_64/egg/flash_attn/losses
copying build/lib/flash_attn/losses/__init__.py -> build/bdist.linux-x86_64/egg/flash_attn/losses
copying build/lib/flash_attn/losses/cross_entropy.py -> build/bdist.linux-x86_64/egg/flash_attn/losses
creating build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/__init__.py -> build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/baichuan.py -> build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/bert.py -> build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/bigcode.py -> build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/btlm.py -> build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/falcon.py -> build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/gpt.py -> build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/gpt_neox.py -> build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/gptj.py -> build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/llama.py -> build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/opt.py -> build/bdist.linux-x86_64/egg/flash_attn/models
copying build/lib/flash_attn/models/vit.py -> build/bdist.linux-x86_64/egg/flash_attn/models
creating build/bdist.linux-x86_64/egg/flash_attn/modules
copying build/lib/flash_attn/modules/__init__.py -> build/bdist.linux-x86_64/egg/flash_attn/modules
copying build/lib/flash_attn/modules/block.py -> build/bdist.linux-x86_64/egg/flash_attn/modules
copying build/lib/flash_attn/modules/embedding.py -> build/bdist.linux-x86_64/egg/flash_attn/modules
copying build/lib/flash_attn/modules/mha.py -> build/bdist.linux-x86_64/egg/flash_attn/modules
copying build/lib/flash_attn/modules/mlp.py -> build/bdist.linux-x86_64/egg/flash_attn/modules
creating build/bdist.linux-x86_64/egg/flash_attn/ops
copying build/lib/flash_attn/ops/__init__.py -> build/bdist.linux-x86_64/egg/flash_attn/ops
copying build/lib/flash_attn/ops/activations.py -> build/bdist.linux-x86_64/egg/flash_attn/ops
copying build/lib/flash_attn/ops/fused_dense.py -> build/bdist.linux-x86_64/egg/flash_attn/ops
copying build/lib/flash_attn/ops/layer_norm.py -> build/bdist.linux-x86_64/egg/flash_attn/ops
copying build/lib/flash_attn/ops/rms_norm.py -> build/bdist.linux-x86_64/egg/flash_attn/ops
creating build/bdist.linux-x86_64/egg/flash_attn/ops/triton
copying build/lib/flash_attn/ops/triton/__init__.py -> build/bdist.linux-x86_64/egg/flash_attn/ops/triton
copying build/lib/flash_attn/ops/triton/cross_entropy.py -> build/bdist.linux-x86_64/egg/flash_attn/ops/triton
copying build/lib/flash_attn/ops/triton/k_activations.py -> build/bdist.linux-x86_64/egg/flash_attn/ops/triton
copying build/lib/flash_attn/ops/triton/layer_norm.py -> build/bdist.linux-x86_64/egg/flash_attn/ops/triton
copying build/lib/flash_attn/ops/triton/linear.py -> build/bdist.linux-x86_64/egg/flash_attn/ops/triton
copying build/lib/flash_attn/ops/triton/mlp.py -> build/bdist.linux-x86_64/egg/flash_attn/ops/triton
copying build/lib/flash_attn/ops/triton/rotary.py -> build/bdist.linux-x86_64/egg/flash_attn/ops/triton
creating build/bdist.linux-x86_64/egg/flash_attn/utils
copying build/lib/flash_attn/utils/__init__.py -> build/bdist.linux-x86_64/egg/flash_attn/utils
copying build/lib/flash_attn/utils/benchmark.py -> build/bdist.linux-x86_64/egg/flash_attn/utils
copying build/lib/flash_attn/utils/distributed.py -> build/bdist.linux-x86_64/egg/flash_attn/utils
copying build/lib/flash_attn/utils/generation.py -> build/bdist.linux-x86_64/egg/flash_attn/utils
copying build/lib/flash_attn/utils/pretrained.py -> build/bdist.linux-x86_64/egg/flash_attn/utils
copying build/lib/flash_attn/utils/torch.py -> build/bdist.linux-x86_64/egg/flash_attn/utils
creating build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/__init__.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/benchmark_attn.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/benchmark_flash_attention_fp8.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/benchmark_mla_decode.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/benchmark_split_kv.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/flash_attn_interface.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/generate_kernels.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/padding.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/setup.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/test_attn_kvcache.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/test_flash_attn.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/test_kvcache.py -> build/bdist.linux-x86_64/egg/hopper
copying build/lib/hopper/test_util.py -> build/bdist.linux-x86_64/egg/hopper
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/__init__.py to __init__.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/bert_padding.py to bert_padding.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_interface.py to flash_attn_interface.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton.py to flash_attn_triton.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_og.py to flash_attn_triton_og.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_blocksparse_attention.py to flash_blocksparse_attention.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_blocksparse_attn_interface.py to flash_blocksparse_attn_interface.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/fused_softmax.py to fused_softmax.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd/__init__.py to __init__.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd/bench.py to bench.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd/bwd_prefill.py to bwd_prefill.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd/bwd_ref.py to bwd_ref.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd/fwd_decode.py to fwd_decode.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd/fwd_prefill.py to fwd_prefill.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd/fwd_ref.py to fwd_ref.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd/interface_fa.py to interface_fa.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd/interface_torch.py to interface_torch.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd/test.py to test.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/flash_attn_triton_amd/utils.py to utils.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/layers/__init__.py to __init__.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/layers/patch_embed.py to patch_embed.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/layers/rotary.py to rotary.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/losses/__init__.py to __init__.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/losses/cross_entropy.py to cross_entropy.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/__init__.py to __init__.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/baichuan.py to baichuan.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/bert.py to bert.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/bigcode.py to bigcode.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/btlm.py to btlm.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/falcon.py to falcon.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/gpt.py to gpt.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/gpt_neox.py to gpt_neox.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/gptj.py to gptj.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/llama.py to llama.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/opt.py to opt.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/models/vit.py to vit.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/modules/__init__.py to __init__.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/modules/block.py to block.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/modules/embedding.py to embedding.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/modules/mha.py to mha.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/modules/mlp.py to mlp.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/__init__.py to __init__.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/activations.py to activations.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/fused_dense.py to fused_dense.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/layer_norm.py to layer_norm.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/rms_norm.py to rms_norm.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/triton/__init__.py to __init__.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/triton/cross_entropy.py to cross_entropy.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/triton/k_activations.py to k_activations.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/triton/layer_norm.py to layer_norm.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/triton/linear.py to linear.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/triton/mlp.py to mlp.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/ops/triton/rotary.py to rotary.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/utils/__init__.py to __init__.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/utils/benchmark.py to benchmark.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/utils/distributed.py to distributed.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/utils/generation.py to generation.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/utils/pretrained.py to pretrained.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/flash_attn/utils/torch.py to torch.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/__init__.py to __init__.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/benchmark_attn.py to benchmark_attn.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/benchmark_flash_attention_fp8.py to benchmark_flash_attention_fp8.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/benchmark_mla_decode.py to benchmark_mla_decode.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/benchmark_split_kv.py to benchmark_split_kv.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/flash_attn_interface.py to flash_attn_interface.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/generate_kernels.py to generate_kernels.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/padding.py to padding.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/setup.py to setup.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/test_attn_kvcache.py to test_attn_kvcache.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/test_flash_attn.py to test_flash_attn.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/test_kvcache.py to test_kvcache.cpython-312.pyc
byte-compiling build/bdist.linux-x86_64/egg/hopper/test_util.py to test_util.cpython-312.pyc
creating build/bdist.linux-x86_64/egg/EGG-INFO
copying flash_attn.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
copying flash_attn.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying flash_attn.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying flash_attn.egg-info/requires.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying flash_attn.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
zip_safe flag not set; analyzing archive contents...
hopper.__pycache__.generate_kernels.cpython-312: module references __file__
hopper.__pycache__.setup.cpython-312: module references __file__
creating dist
creating 'dist/flash_attn-2.7.4.post1-py3.12.egg' and adding 'build/bdist.linux-x86_64/egg' to it
removing 'build/bdist.linux-x86_64/egg' (and everything under it)
Processing flash_attn-2.7.4.post1-py3.12.egg
removing '/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/flash_attn-2.7.4.post1-py3.12.egg' (and everything under it)
creating /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/flash_attn-2.7.4.post1-py3.12.egg
Extracting flash_attn-2.7.4.post1-py3.12.egg to /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Adding flash-attn 2.7.4.post1 to easy-install.pth file

Installed /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/flash_attn-2.7.4.post1-py3.12.egg
Processing dependencies for flash-attn==2.7.4.post1
Searching for einops==0.8.1
Best match: einops 0.8.1
Adding einops 0.8.1 to easy-install.pth file

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Searching for torch==2.4.0+rocm6.3.4.git7cecbf6d
Best match: torch 2.4.0+rocm6.3.4.git7cecbf6d
Adding torch 2.4.0+rocm6.3.4.git7cecbf6d to easy-install.pth file
Installing convert-caffe2-to-onnx script to /home/markus/code/YuE/venv-3.12/bin
Installing convert-onnx-to-caffe2 script to /home/markus/code/YuE/venv-3.12/bin
Installing torchrun script to /home/markus/code/YuE/venv-3.12/bin

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Searching for pytorch-triton-rocm==3.0.0+rocm6.3.4.git75cc27c2
Best match: pytorch-triton-rocm 3.0.0+rocm6.3.4.git75cc27c2
Adding pytorch-triton-rocm 3.0.0+rocm6.3.4.git75cc27c2 to easy-install.pth file
Installing proton script to /home/markus/code/YuE/venv-3.12/bin
Installing proton-viewer script to /home/markus/code/YuE/venv-3.12/bin

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Searching for setuptools==78.1.0
Best match: setuptools 78.1.0
Adding setuptools 78.1.0 to easy-install.pth file

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Searching for fsspec==2025.3.2
Best match: fsspec 2025.3.2
Adding fsspec 2025.3.2 to easy-install.pth file

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Searching for jinja2==3.1.6
Best match: jinja2 3.1.6
Adding jinja2 3.1.6 to easy-install.pth file

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Searching for networkx==3.4.2
Best match: networkx 3.4.2
Adding networkx 3.4.2 to easy-install.pth file

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Searching for sympy==1.12.1
Best match: sympy 1.12.1
Adding sympy 1.12.1 to easy-install.pth file
Installing isympy script to /home/markus/code/YuE/venv-3.12/bin

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Searching for typing-extensions==4.13.2
Best match: typing-extensions 4.13.2
Adding typing-extensions 4.13.2 to easy-install.pth file

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Searching for filelock==3.18.0
Best match: filelock 3.18.0
Adding filelock 3.18.0 to easy-install.pth file

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Searching for MarkupSafe==3.0.2
Best match: MarkupSafe 3.0.2
Adding MarkupSafe 3.0.2 to easy-install.pth file

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Searching for mpmath==1.3.0
Best match: mpmath 1.3.0
Adding mpmath 1.3.0 to easy-install.pth file

Using /home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages
Finished processing dependencies for flash-attn==2.7.4.post1

```

---

### 评论 #10 — tcgu-amd (2025-04-21T15:55:08Z)

Hi @hartmark, after some digging, seems like FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE" should be the correct flag. 
https://github.com/Dao-AILab/flash-attention/blob/main/flash_attn/flash_attn_interface.py#L13-L14. It will eliminate the need for flash_attn_cuda module. 

The fact that you are seeing https://github.com/ROCm/ROCm/issues/4578#issuecomment-2811202232 actually suggests that the flash  attention module is working on you system. However, it is encountering an error where the predicted memory layout and the metadata's data layout is not matching. 

Based on the log, the expected layout should be ending in `[..., SeqLen=4288, NumHeads=24, HeadDim=128]` based on the calculations, but that does not match with the stride provided in the metadata. 

In order the fully analyze this, would you be able to provide me the full back trace of the bug? Thanks!

---

### 评论 #11 — hartmark (2025-04-21T21:43:54Z)

Alright, here's the full reproducing steps with latest YuE and flash-attention:

Setup venv:
```
export PYTHON_VERSION_FULL=3.12.8
export PYTHON_VERSION=3.12
"${HOME}/.pyenv/shims/python${PYTHON_VERSION}" -m venv "./venv-${PYTHON_VERSION}"
source "./venv-${PYTHON_VERSION}/bin/activate"
```

Now I'm in venv and run these commands:

First I install ROCm torch:
```
pip3 uninstall -y torch torchaudio torchvision pytorch_triton
pip3 install torch==2.4.0 torchaudio torchvision==0.19.0 pytorch_triton -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4
```

Verify I get ROCm enabled torch with this command:
```
python <<EOF                                     
import torch
import sys

try:
    print("PyTorch version:", torch.__version__)
    cuda_available = torch.cuda.is_available()
    print("Is CUDA available:", cuda_available)
    if cuda_available:
        print("CUDA device count:", torch.cuda.device_count())
        print("CUDA device name:", torch.cuda.get_device_name(0))
    else:
        print("No CUDA device found")
        sys.exit(1)
except Exception as e:
    print("Error:", e)
    sys.exit(1)  # Exit with 1 for other errors
EOF
```

It got this output:
```
amdgpu.ids: No such file or directory
Is CUDA available: True
CUDA device count: 1
CUDA device name: AMD Radeon Graphics
```

Now time to build flash-attention:
```
git clone git@github.com:Dao-AILab/flash-attention.git
cd flash-attention
FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE" python setup.py install 2>&1 | tee flash_attention.log
```

[flash_attention.log](https://github.com/user-attachments/files/19840405/flash_attention.log)

Run YuE:
```
cd YuE
git pull
pip install -r requirements.txt 2>&1 | tee requirements.log
cd inference
FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE" HSA_OVERRIDE_GFX_VERSION=11.0.0 python infer.py --cuda_idx 0 --stage1_model m-a-p/YuE-s1-7B-anneal-en-cot --stage2_model m-a-p/YuE-s2-1B-general --genre_txt ../prompt_egs/genre.txt --lyrics_txt ../prompt_egs/lyrics.txt --run_n_segments 2 --stage2_batch_size 4 --output_dir ../output --max_new_tokens 3000 --repetition_penalty 1.1 2>&1 | tee YuE.log
```

[requirements.log](https://github.com/user-attachments/files/19840421/requirements.log)

YuE.log:
```
amdgpu.ids: No such file or directory
You are attempting to use Flash Attention 2.0 with a model not initialized on GPU. Make sure to move the model to GPU after initializing it on CPU with `model.to('cuda')`.
Loading checkpoint shards: 100%|██████████| 3/3 [00:00<00:00, 66.88it/s]
/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/torch/nn/utils/weight_norm.py:134: FutureWarning: `torch.nn.utils.weight_norm` is deprecated in favor of `torch.nn.utils.parametrizations.weight_norm`.
  WeightNorm.apply(module, name, dim)
Traceback (most recent call last):
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/modeling_utils.py", line 556, in load_state_dict
    return torch.load(
           ^^^^^^^^^^^
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/torch/serialization.py", line 1113, in load
    raise pickle.UnpicklingError(_get_wo_message(str(e))) from None
_pickle.UnpicklingError: Weights only load failed. Re-running `torch.load` with `weights_only` set to `False` will likely succeed, but it can result in arbitrary code execution. Do it only if you got the file from a trusted source.
 Please file an issue with the following so that we can make `weights_only=True` compatible with your use case: WeightsUnpickler error: Unsupported operand 118

Check the documentation of torch.load to learn more about types accepted by default with weights_only https://pytorch.org/docs/stable/generated/torch.load.html.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/markus/code/YuE/inference/infer.py", line 100, in <module>
    codec_model = eval(model_config.generator.name)(**model_config.generator.config).to(device)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/code/YuE/inference/xcodec_mini_infer/models/soundstream_hubert_new.py", line 102, in __init__
    self.semantic_model = AutoModel.from_pretrained("./xcodec_mini_infer/semantic_ckpts/hf_1_325000")
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/models/auto/auto_factory.py", line 571, in from_pretrained
    return model_class.from_pretrained(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/modeling_utils.py", line 279, in _wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/modeling_utils.py", line 4399, in from_pretrained
    ) = cls._load_pretrained_model(
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/modeling_utils.py", line 4638, in _load_pretrained_model
    load_state_dict(checkpoint_files[0], map_location="meta", weights_only=weights_only).keys()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/markus/code/YuE/venv-3.12/lib/python3.12/site-packages/transformers/modeling_utils.py", line 566, in load_state_dict
    raise OSError(
OSError: You seem to have cloned a repository without having git-lfs installed. Please install git-lfs and run `git lfs install` followed by `git lfs pull` in the folder you cloned.
amdgpu.ids: No such file or directory

```

---

### 评论 #12 — hartmark (2025-04-21T21:45:32Z)

I got a new error now. Check the previous message.

Apparently you need to also use **FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"** so flash-attention uses the ROCm code properly.

---

### 评论 #13 — hartmark (2025-04-21T22:31:21Z)

Seems there was some issue with the lfs. Running these commands got it working. Let's see how long it will take now to generate a song.
```
git lfs install
git lfs pull
```

---

### 评论 #14 — tcgu-amd (2025-04-22T19:57:18Z)

@hartmark, I'm glad that it appears to be working now! Were you able to get it to generate proper outputs? Thanks! 

---

### 评论 #15 — hartmark (2025-04-22T22:24:00Z)

> [@hartmark](https://github.com/hartmark), I'm glad that it appears to be working now! Were you able to get it to generate proper outputs? Thanks!

I haven't had time to wait for it to complete yet. I had to terminate after 20-30 minutes.

I have the same issue with generating images on ComfyUI. For more complex workflows where I max out memory usage it seems to take forever to get the job to complete.

The kernel reports this line 100 times per second:

`[apr 22 01:52:07 bernard kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
`

---

### 评论 #16 — orkutmuratyilmaz (2025-04-27T13:45:46Z)

I'm following this for ComfyUI and YUE issues.

---

### 评论 #17 — hartmark (2025-04-29T00:50:14Z)

> I'm following this for ComfyUI and YUE issues.

I created reproducing steps at https://github.com/ROCm/ROCm/issues/4698


---

### 评论 #18 — tcgu-amd (2025-05-16T21:49:41Z)

Hi @hartmark, I was able to use Yue to successfully generate a short music snippet (about 10 seconds long) following your steps with some modifications. The script took around 15 mins to complete. 

A couple findings: 

- There seems to be an issue with the latest python3.12.9 version, downgrading to python 3.11 worked for me.
- The example prompts is quite long, I reduced it to one verse and one chorus only (without lyrics), which made the inference much faster. 
- However, there is a bug in the infer.py which will throw an error when the prompt is too short. At [infer.py:L355](https://github.com/multimodal-art-projection/YuE/blob/main/inference/infer.py#L355), the `output_duration` variable can be 0 if the prompt is shorter than 300. Adding a line below that makes it default to a minimum value of 6 i.e. `output_duration=max(output_duration, 6)` worked.  This also requires the check [infer.py:L382](https://github.com/multimodal-art-projection/YuE/blob/main/inference/infer.py#L382) to be changed from `if output_duration*50 != prompt.shape[-1]:` to `if output_duration*50 < prompt.shape[-1]:`

With these changes made, the steps I took are:
Install python3.11
```
add-apt-repository ppa:deadsnakes/ppa
apt update
apt install python3.11 python3.11-dev python3.11-venv
```
Create a venv with python3.11
```
python -m venv yue
source /yue/bin/activate
```
Install pytorch with ROCm
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.3
```
Set up environment
```
export FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"
```
Install flash attention
```
pip install triton==3.2.0
cd flash-attention
python setup.py install
```
Install YuE dependencies
```
sudo apt update
sudo apt install git-lfs
git lfs install
git clone https://github.com/multimodal-art-projection/YuE.git
cd Yue
pip install -r ./requirements.txt

cd inference
git clone https://huggingface.co/m-a-p/xcodec_mini_infer
```
And finally, run infer
```
python infer.py     --cuda_idx 0     --stage1_model
 m-a-p/YuE-s1-7B-anneal-en-cot     --stage2_model m-a-p/YuE-s2-1B-general     --genre_txt ../prompt_egs/genre.txt     --
lyrics_txt ../prompt_egs/lyrics.txt     --run_n_segments 2     --stage2_batch_size 4     --output_dir ../output     --ma
x_new_tokens 3000     --repetition_penalty 1.1
```

Hope this helps! Since I was able to confirm that YuE works with ROCm on gfx1100, I will be closing this ticket for now. But please do feel free to follow up below, and I'd be happy to help. 

Thanks! 

---
