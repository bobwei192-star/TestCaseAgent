# [Documentation]: Inconsistent install instructions for `ROCm/bitsandbytes`

> **Issue #3132**
> **状态**: closed
> **创建时间**: 2024-05-15T16:24:22Z
> **更新时间**: 2024-08-02T19:01:33Z
> **关闭时间**: 2024-08-02T19:01:33Z
> **作者**: garrettbyrd
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/3132

## 负责人

- eliotli
- SeanSong-amd

## 描述

### Description of errors

There are some recent blog posts [1,2,3] that provide the following install instructions for `ROCm/bitsandbytes` for ROCm v6.x:
```
git clone --recurse https://github.com/ROCm/bitsandbytes.git
cd bitsandbytes
git checkout rocm_enabled
make hip
python setup.py install
```

One can easily verify that the `rocm_enabled` branch does not include a `Makefile`.

In the README for this branch, it does provide the following instructions for installing `ROCm/bitsandbytes`: 
```
git clone --recurse https://github.com/ROCm/bitsandbytes
cd bitsandbytes
# Checkout branch as needed
# for rocm 5.7 - rocm5.7_internal_testing
# for rocm 6.x - rocm6.2_internal_testing
git checkout <branch>
make hip
python setup.py install
```

These instructions seem to work. 

However, in the README for the branch `rocm6.2_internal_testing`, the same incorrect install steps are provided for `ROCm/bitsandbytes`:
```
# Install BitsandBytes
git clone --recurse https://github.com/ROCmSoftwarePlatform/bitsandbytes
cd bitsandbytes
git checkout rocm_enabled
make hip
python setup.py install
```

The same incorrect instructions are in the README for the branch `rocm5.7_internal_testing`.

The branch `rocm6.2_internal_testing` needs to be corrected to have the following install instructions:
```
git clone --recurse https://github.com/ROCm/bitsandbytes
cd bitsandbytes
git checkout rocm6.2_internal_testing
make hip
python setup.py install
```

And the branch `rocm5.7_internal_testing` needs to be corrected to have the following install instructions
```
git clone --recurse https://github.com/ROCm/bitsandbytes
cd bitsandbytes
git checkout rocm5.7_internal_testing
make hip
python setup.py install
```

This would provide working, consistent install instructions between the three branches `rocm5.7_internal_testing`, `rocm6.2_internal_testing`, and `rocm_enabled`.

Other branches might have incorrect instructions, but I have not checked branches besides these three.


[1] [https://rocm.blogs.amd.com/artificial-intelligence/starcoder-fine-tune/README.html](https://rocm.blogs.amd.com/artificial-intelligence/starcoder-fine-tune/README.html)

[2] [https://rocm.blogs.amd.com/artificial-intelligence/llama2-Qlora/README.html](https://rocm.blogs.amd.com/artificial-intelligence/llama2-Qlora/README.html)

[3] [https://rocm.blogs.amd.com/artificial-intelligence/llama2-lora/README.html](https://rocm.blogs.amd.com/artificial-intelligence/llama2-lora/README.html)

---

## 评论 (9 条)

### 评论 #1 — clintg6 (2024-05-15T23:41:20Z)

Hi Garrett, 

The instructions in the blog will be updated shortly. In the meantime, the recommended installation for bitsandbytes for ROCm is as follows:
```
git clone --recurse https://github.com/ROCm/bitsandbytes
cd bitsandbytes
git checkout rocm_enabled
pip install -r requirements-dev.txt
cmake -DCOMPUTE_BACKEND=hip -S .
make
pip install .
```

---

### 评论 #2 — pnunna93 (2024-05-16T19:27:17Z)

Hi @garrettbyrd , Thanks for bringing it to our attention. There were lot of updates in the last few weeks which made those instructions obsolete. All the branches are updated now with latest instructions.
rocm_enabled - https://github.com/ROCm/bitsandbytes/blob/rocm_enabled/README.md
rocm6.2_internal_testing - https://github.com/ROCm/bitsandbytes/blob/rocm6.2_internal_testing/README.md
rocm5.7_internal_testing - https://github.com/ROCm/bitsandbytes/blob/rocm5.7_internal_testing/README.md

---

### 评论 #3 — ppanchad-amd (2024-05-23T15:02:18Z)

@garrettbyrd Please advise if we can go ahead and close the ticket. Thanks!

---

### 评论 #4 — garrdbyrd (2024-06-04T00:54:33Z)

This is @garrettbyrd using my personal account.

I was not able to reproduce. 

The package is able to build and is successfully added to my conda environment, but errors occur at runtime.

I set up a fresh conda env as follows:
```
# Install ROCm
# ...
# Install conda
# ...

# Conda env setup
conda create -n bits-env
conda activate bits-env
conda install pip jupyterlab

# Install pytorch
# https://pytorch.org/get-started/locally/
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0

# Install bitsandbytes
git clone --recurse https://github.com/ROCm/bitsandbytes
cd bitsandbytes
git checkout rocm_enabled
pip install -r requirements-dev.txt
cmake -DCOMPUTE_BACKEND=hip -S .
make
pip install .
```

I set up an example notebook with two cells.
First cell:
```
import torch
import bitsandbytes
from torch import nn
```
First cell output:
```
Could not load bitsandbytes native library: [/home/USER/.conda/envs/bits-env/lib/python3.12/site-packages/zmq/backend/cython/../../../../.././libstdc](https://file+.vscode-resource.vscode-cdn.net/home/USER/.conda/envs/bits-env/lib/libstdc)++.so.6: version `GLIBCXX_3.4.32' not found (required by [/home/USER/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/libbitsandbytes_hip_nohipblaslt.so](https://file+.vscode-resource.vscode-cdn.net/home/USER/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/libbitsandbytes_hip_nohipblaslt.so))
Traceback (most recent call last):
  File "/home/USER/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/cextension.py", line 124, in <module>
    lib = get_native_library()
          ^^^^^^^^^^^^^^^^^^^^
  File "/home/USER/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/cextension.py", line 104, in get_native_library
    dll = ct.cdll.LoadLibrary(str(binary_path))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/USER/.conda/envs/bits-env/lib/python3.12/ctypes/__init__.py", line 460, in LoadLibrary
    return self._dlltype(name)
           ^^^^^^^^^^^^^^^^^^^
  File "/home/USER/.conda/envs/bits-env/lib/python3.12/ctypes/__init__.py", line 379, in __init__
    self._handle = _dlopen(self._name, mode)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^
OSError: [/home/USER/.conda/envs/bits-env/lib/python3.12/site-packages/zmq/backend/cython/../../../../.././libstdc](https://file+.vscode-resource.vscode-cdn.net/home/USER/.conda/envs/bits-env/lib/libstdc)++.so.6: version `GLIBCXX_3.4.32' not found (required by [/home/USER/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/libbitsandbytes_hip_nohipblaslt.so](https://file+.vscode-resource.vscode-cdn.net/home/USER/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/libbitsandbytes_hip_nohipblaslt.so))

CUDA Setup failed despite CUDA being available. Please run the following command to get more information:

python -m bitsandbytes

Inspect the output of the command and see if you can locate CUDA libraries. You might need to add them
to your LD_LIBRARY_PATH. If you suspect a bug, please take the information from python -m bitsandbytes
and open an issue at: https://github.com/TimDettmers/bitsandbytes/issues
```
Second cell:
```
model = nn.Sequential(
    nn.Linear(10, 50),
    nn.ReLU(),
    nn.Linear(50, 1)
)

optimizer = bitsandbytes.optim.Adam8bit(model.parameters())

input = torch.randn(1, 10)
target = torch.randn(1, 1)

output = model(input)
loss = nn.MSELoss()(output, target)
loss.backward()
optimizer.step()

print("Loss:", loss.item())
```
Second cell output:
```
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[2], [line 21](vscode-notebook-cell:?execution_count=2&line=21)
     [19](vscode-notebook-cell:?execution_count=2&line=19) # Backward pass and optimize
     [20](vscode-notebook-cell:?execution_count=2&line=20) loss.backward()
---> [21](vscode-notebook-cell:?execution_count=2&line=21) optimizer.step()
     [23](vscode-notebook-cell:?execution_count=2&line=23) print("Loss:", loss.item())

File [~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/optim/optimizer.py:391](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/optim/optimizer.py:391), in Optimizer.profile_hook_step.<locals>.wrapper(*args, **kwargs)
    [386](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/optim/optimizer.py:386)         else:
    [387](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/optim/optimizer.py:387)             raise RuntimeError(
    [388](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/optim/optimizer.py:388)                 f"{func} must return None or a tuple of (new_args, new_kwargs), but got {result}."
    [389](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/optim/optimizer.py:389)             )
--> [391](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/optim/optimizer.py:391) out = func(*args, **kwargs)
    [392](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/optim/optimizer.py:392) self._optimizer_step_code()
    [394](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/optim/optimizer.py:394) # call optimizer step post hooks

File [~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/utils/_contextlib.py:115](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/utils/_contextlib.py:115), in context_decorator.<locals>.decorate_context(*args, **kwargs)
    [112](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/utils/_contextlib.py:112) @functools.wraps(func)
    [113](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/utils/_contextlib.py:113) def decorate_context(*args, **kwargs):
    [114](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/utils/_contextlib.py:114)     with ctx_factory():
--> [115](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/torch/utils/_contextlib.py:115)         return func(*args, **kwargs)

File [~/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/optim/optimizer.py:287](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/optim/optimizer.py:287), in Optimizer8bit.step(self, closure)
    [284](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/optim/optimizer.py:284)             self.init_state(group, p, gindex, pindex)
...
-> [1620](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/functional.py:1620)     optim_func = str2optimizer32bit[optimizer_name][0]
   [1621](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/functional.py:1621) elif g.dtype == torch.float16:
   [1622](https://file+.vscode-resource.vscode-cdn.net/home/USER/Documents/temp/~/.conda/envs/bits-env/lib/python3.12/site-packages/bitsandbytes/functional.py:1622)     optim_func = str2optimizer32bit[optimizer_name][1]

NameError: name 'str2optimizer32bit' is not defined
```

This is consistent with some testing I was doing on another system with basically identical (but anecdotal) conditions. I also get the same output when wrapping with `with torch.cuda.device(0):`.

Here is the output of `python -m bitsandbytes`:
```
(bits-env) [USER@USER bitsandbytes]$ python -m bitsandbytes
Could not load bitsandbytes native library: /home/USER/.conda/envs/bits-env/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /home/USER/Documents/temp/bitsandbytes/bitsandbytes/libbitsandbytes_hip_nohipblaslt.so)
Traceback (most recent call last):
  File "/home/USER/Documents/temp/bitsandbytes/bitsandbytes/cextension.py", line 124, in <module>
    lib = get_native_library()
          ^^^^^^^^^^^^^^^^^^^^
  File "/home/USER/Documents/temp/bitsandbytes/bitsandbytes/cextension.py", line 104, in get_native_library
    dll = ct.cdll.LoadLibrary(str(binary_path))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/USER/.conda/envs/bits-env/lib/python3.12/ctypes/__init__.py", line 460, in LoadLibrary
    return self._dlltype(name)
           ^^^^^^^^^^^^^^^^^^^
  File "/home/USER/.conda/envs/bits-env/lib/python3.12/ctypes/__init__.py", line 379, in __init__
    self._handle = _dlopen(self._name, mode)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^
OSError: /home/USER/.conda/envs/bits-env/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /home/USER/Documents/temp/bitsandbytes/bitsandbytes/libbitsandbytes_hip_nohipblaslt.so)

CUDA Setup failed despite CUDA being available. Please run the following command to get more information:

python -m bitsandbytes

Inspect the output of the command and see if you can locate CUDA libraries. You might need to add them
to your LD_LIBRARY_PATH. If you suspect a bug, please take the information from python -m bitsandbytes
and open an issue at: https://github.com/TimDettmers/bitsandbytes/issues

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++ BUG REPORT INFORMATION ++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++ OTHER +++++++++++++++++++++++++++
CUDA specs: CUDASpecs(highest_compute_capability=(11, 0), cuda_version_string='60', cuda_version_tuple=(6, 0))
PyTorch settings found: CUDA_VERSION=60, Highest Compute Capability: (11, 0).
WARNING: CUDA versions lower than 11 are currently not supported for LLM.int8().
You will be only to use 8-bit optimizers and quantization routines!
To manually override the PyTorch CUDA version please see: https://github.com/TimDettmers/bitsandbytes/blob/main/docs/source/nonpytorchcuda.mdx
The directory listed in your path is found to be non-existent: local/USER
The directory listed in your path is found to be non-existent: @/tmp/.ICE-unix/1853,unix/USER
The directory listed in your path is found to be non-existent: /org/freedesktop/DisplayManager/Session1
The directory listed in your path is found to be non-existent: /etc/gtk/gtkrc
The directory listed in your path is found to be non-existent: /home/USER/.gtkrc
The directory listed in your path is found to be non-existent: /etc/gtk-2.0/gtkrc
The directory listed in your path is found to be non-existent: /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-plasmashell.service/memory.pressure
The directory listed in your path is found to be non-existent: /Sessions/1
The directory listed in your path is found to be non-existent: /org/freedesktop/DisplayManager/Seat0
The directory listed in your path is found to be non-existent: /home/USER/.cache/dotnet_bundle_extract
The directory listed in your path is found to be non-existent: //debuginfod.archlinux.org 
The directory listed in your path is found to be non-existent: /var/lib/spack/modules/tcl
The directory listed in your path is found to be non-existent: /Windows/1
CUDA SETUP: WARNING! CUDA runtime files not found in any environmental path.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++ DEBUG INFO END ++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Checking that the library is importable and CUDA is callable...
Couldn't load the bitsandbytes library, likely due to missing binaries.
Please ensure bitsandbytes is properly installed.

For source installations, compile the binaries with `cmake -DCOMPUTE_BACKEND=cuda -S .`.
See the documentation for more details if needed.

Trying a simple check anyway, but this will likely fail...
Traceback (most recent call last):
  File "/home/USER/Documents/temp/bitsandbytes/bitsandbytes/diagnostics/main.py", line 66, in main
    sanity_check()
  File "/home/USER/Documents/temp/bitsandbytes/bitsandbytes/diagnostics/main.py", line 40, in sanity_check
    adam.step()
  File "/home/USER/.conda/envs/bits-env/lib/python3.12/site-packages/torch/optim/optimizer.py", line 391, in wrapper
    out = func(*args, **kwargs)
          ^^^^^^^^^^^^^^^^^^^^^
  File "/home/USER/.conda/envs/bits-env/lib/python3.12/site-packages/torch/utils/_contextlib.py", line 115, in decorate_context
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/USER/Documents/temp/bitsandbytes/bitsandbytes/optim/optimizer.py", line 287, in step
    self.update_step(group, p, gindex, pindex)
  File "/home/USER/.conda/envs/bits-env/lib/python3.12/site-packages/torch/utils/_contextlib.py", line 115, in decorate_context
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/USER/Documents/temp/bitsandbytes/bitsandbytes/optim/optimizer.py", line 496, in update_step
    F.optimizer_update_32bit(
  File "/home/USER/Documents/temp/bitsandbytes/bitsandbytes/functional.py", line 1620, in optimizer_update_32bit
    optim_func = str2optimizer32bit[optimizer_name][0]
                 ^^^^^^^^^^^^^^^^^^
NameError: name 'str2optimizer32bit' is not defined
Above we output some debug information.
Please provide this info when creating an issue via https://github.com/TimDettmers/bitsandbytes/issues/new/choose
WARNING: Please be sure to sanitize sensitive info from the output before posting it.
```

It seems that GCC 13.2 is required (see mentions of `GLIBCXX_3.4.32`, I am using 14.1.1), but I have not found this formally stated anywhere. If this is the case, I can test on another system that uses module environments (same alternative system mentioned above that didn't work before).

Minor note: this hunch did not work with a simple `conda install conda-forge::gcc` (which is 13.2.0) and remake/installing.

---

### 评论 #5 — pnunna93 (2024-06-04T21:21:12Z)

@garrdbyrd , could you please build with this dockerfile and check?
[bnb_rocm_dockerfile.txt](https://github.com/user-attachments/files/15570506/bnb_rocm_dockerfile.txt)
Your environment may have multiple libstdc++.so.* files, which caused the issue.

---

### 评论 #6 — garrettbyrd (2024-07-03T16:06:49Z)

`bitsandbytes` seems to install correctly, but I have encountered an issue when testing.

I am following [this blog](https://rocm.blogs.amd.com/artificial-intelligence/llama2-lora/README.html).

In [this block](https://rocm.blogs.amd.com/artificial-intelligence/llama2-lora/README.html#training-with-lora-configuration)
```
from peft import get_peft_model
# LoRA Config
peft_parameters = LoraConfig(
    lora_alpha=8,
    lora_dropout=0.1,
    r=8,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(base_model, peft_parameters)
model.print_trainable_parameters()
```
I am getting this error:
```
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[7], [line 10](vscode-notebook-cell:?execution_count=7&line=10)
      [2](vscode-notebook-cell:?execution_count=7&line=2) # LoRA Config
      [3](vscode-notebook-cell:?execution_count=7&line=3) peft_parameters = LoraConfig(
      [4](vscode-notebook-cell:?execution_count=7&line=4)     lora_alpha=8,
      [5](vscode-notebook-cell:?execution_count=7&line=5)     lora_dropout=0.1,
   (...)
      [8](vscode-notebook-cell:?execution_count=7&line=8)     task_type="CAUSAL_LM"
      [9](vscode-notebook-cell:?execution_count=7&line=9) )
---> [10](vscode-notebook-cell:?execution_count=7&line=10) model = get_peft_model(base_model, peft_parameters)
     [11](vscode-notebook-cell:?execution_count=7&line=11) model.print_trainable_parameters()

File ~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/mapping.py:149, in get_peft_model(model, peft_config, adapter_name, mixed)
    [147](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/mapping.py:147) if peft_config.is_prompt_learning:
    [148](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/mapping.py:148)     peft_config = _prepare_prompt_learning_config(peft_config, model_config)
--> [149](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/mapping.py:149) return MODEL_TYPE_TO_PEFT_MODEL_MAPPING[peft_config.task_type](model, peft_config, adapter_name=adapter_name)

File ~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/peft_model.py:1395, in PeftModelForCausalLM.__init__(self, model, peft_config, adapter_name)
   [1394](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/peft_model.py:1394) def __init__(self, model: torch.nn.Module, peft_config: PeftConfig, adapter_name: str = "default") -> None:
-> [1395](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/peft_model.py:1395)     super().__init__(model, peft_config, adapter_name)
   [1396](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/peft_model.py:1396)     self.base_model_prepare_inputs_for_generation = self.base_model.prepare_inputs_for_generation

File ~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/peft_model.py:138, in PeftModel.__init__(self, model, peft_config, adapter_name)
    [136](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/peft_model.py:136)     self._peft_config = None
    [137](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/peft_model.py:137)     cls = PEFT_TYPE_TO_MODEL_MAPPING[peft_config.peft_type]
--> [138](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/peft_model.py:138)     self.base_model = cls(model, {adapter_name: peft_config}, adapter_name)
    [139](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/peft_model.py:139)     self.set_additional_trainable_modules(peft_config, adapter_name)
    [141](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/peft_model.py:141) if getattr(model, "is_gradient_checkpointing", True):

File ~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:139, in LoraModel.__init__(self, model, config, adapter_name)
    [138](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:138) def __init__(self, model, config, adapter_name) -> None:
--> [139](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:139)     super().__init__(model, config, adapter_name)

File ~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:166, in BaseTuner.__init__(self, model, peft_config, adapter_name)
    [164](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:164) self.active_adapter: str | list[str] = adapter_name
    [165](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:165) self._pre_injection_hook(self.model, self.peft_config[adapter_name], adapter_name)
--> [166](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:166) self.inject_adapter(self.model, adapter_name)
    [168](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:168) # Copy the peft_config in the injected model.
    [169](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:169) self.model.peft_config = self.peft_config

File ~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:372, in BaseTuner.inject_adapter(self, model, adapter_name)
    [370](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:370)     is_target_modules_in_base_model = True
    [371](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:371)     parent, target, target_name = _get_submodules(model, key)
--> [372](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:372)     self._create_and_replace(peft_config, adapter_name, target, target_name, parent, current_key=key)
    [374](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:374) if not is_target_modules_in_base_model:
    [375](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:375)     raise ValueError(
    [376](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:376)         f"Target modules {peft_config.target_modules} not found in the base model. "
    [377](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:377)         f"Please check the target modules and try again."
    [378](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/tuners_utils.py:378)     )

File ~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:223, in LoraModel._create_and_replace(self, lora_config, adapter_name, target, target_name, parent, current_key)
    [213](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:213)     target.update_layer(
    [214](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:214)         adapter_name,
    [215](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:215)         r,
   (...)
    [220](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:220)         use_dora=lora_config.use_dora,
    [221](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:221)     )
    [222](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:222) else:
--> [223](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:223)     new_module = self._create_new_module(lora_config, adapter_name, target, **kwargs)
    [224](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:224)     if adapter_name not in self.active_adapters:
    [225](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:225)         # adding an additional adapter: it is not automatically trainable
    [226](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:226)         new_module.requires_grad_(False)

File ~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:291, in LoraModel._create_new_module(lora_config, adapter_name, target, **kwargs)
    [289](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:289) # avoid eager bnb import
    [290](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:290) if is_bnb_available():
--> [291](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:291)     from .bnb import dispatch_bnb_8bit
    [293](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:293)     dispatchers.append(dispatch_bnb_8bit)
    [295](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/model.py:295) if is_bnb_4bit_available():

File ~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/bnb.py:272
    [267](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/bnb.py:267)             new_module = Linear8bitLt(target, adapter_name, **eightbit_kwargs)
    [269](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/bnb.py:269)         return new_module
--> [272](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/bnb.py:272) if is_bnb_4bit_available():
    [274](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/bnb.py:274)     class Linear4bit(torch.nn.Module, LoraLayer):
    [275](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/bnb.py:275)         # Lora implemented in a dense layer
    [276](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/bnb.py:276)         def __init__(
    [277](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/bnb.py:277)             self,
    [278](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/bnb.py:278)             base_layer: torch.nn.Module,
   (...)
    [286](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/bnb.py:286)             **kwargs,
    [287](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/tuners/lora/bnb.py:287)         ) -> None:

File ~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/import_utils.py:33, in is_bnb_4bit_available()
     [29](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/import_utils.py:29)     return False
     [31](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/import_utils.py:31) import bitsandbytes as bnb
---> [33](REDACTED.vscode-resource.vscode-cdn.net/home/garrett/amd/rocm-bnb/~/miniconda3/envs/rocm-bnb/lib/python3.12/site-packages/peft/import_utils.py:33) return hasattr(bnb.nn, "Linear4bit")

AttributeError: module 'bitsandbytes' has no attribute 'nn'
```
I am not sure if this is an issue with `peft` that was not present at the time of publication, or there is some install issue with `bitsandbytes`.

---

### 评论 #7 — SeanSong-amd (2024-07-09T06:02:09Z)

@garrdbyrd From the log, it appears there is a version mismatch between peft and bnb.
I tested the blog today and found a numpy version compatibility issue that wasn't present at the time of publication. Though there is a fix for that. The easiest way is use this [docker iamge](https://hub.docker.com/layers/rocm/pytorch/rocm6.1.2_ubuntu22.04_py3.10_pytorch_release-2.1.2/images/sha256-c8b4e8dfcc64e9bf68bf1b38a16fbc5d65b653ec600f98d3290f66e16c8b6078?context=explore). 

After launching the Docker container, if you prefer using a conda environment, you can run "conda activate py_3.10 inside" of it.
Then follow the steps in [llama + lora blog](https://rocm.blogs.amd.com/artificial-intelligence/llama2-lora/README.html) for finetuning.

Please let me know if this wroks for you.

---

### 评论 #8 — garrettbyrd (2024-07-29T18:40:00Z)

@SeanSong-amd I will test with the up-to-date branch as discussed [here](https://github.com/ROCm/ROCm/issues/3447) and then provide a description of any versioning issues.

---

### 评论 #9 — garrettbyrd (2024-08-02T19:01:33Z)

I can confirm this works using the [`multi-backend-refactor` branch of `bitsandbytes`](https://github.com/bitsandbytes-foundation/bitsandbytes/tree/multi-backend-refactor).

Thanks for the assistance.

For posterity, I will list my versions below.

```
$ pip freeze
absl-py==2.1.0
accelerate==0.33.0
aiohappyeyeballs==2.3.4
aiohttp==3.10.0
aiosignal==1.3.1
anyio==4.4.0
argon2-cffi==23.1.0
argon2-cffi-bindings==21.2.0
arrow==1.3.0
asttokens==2.4.1
async-lru==2.0.4
attrs==23.2.0
Babel==2.15.0
beautifulsoup4==4.12.3
bitsandbytes @ file:///home/garrett/bnb <- built from source
bleach==6.1.0
certifi==2024.7.4
cffi==1.16.0
charset-normalizer==3.3.2
comm==0.2.2
contourpy==1.2.1
cycler==0.12.1
datasets==2.20.0
debugpy==1.8.2
decorator==5.1.1
defusedxml==0.7.1
dill==0.3.8
docstring_parser==0.16
einops==0.8.0
executing==2.0.1
fastjsonschema==2.20.0
filelock==3.13.1
fonttools==4.53.1
fqdn==1.5.1
frozenlist==1.4.1
fsspec==2024.2.0
grpcio==1.65.4
h11==0.14.0
httpcore==1.0.5
httpx==0.27.0
huggingface-hub==0.24.5
idna==3.7
iniconfig==2.0.0
ipykernel==6.29.5
ipython==8.26.0
isoduration==20.11.0
jedi==0.19.1
Jinja2==3.1.3
json5==0.9.25
jsonpointer==3.0.0
jsonschema==4.23.0
jsonschema-specifications==2023.12.1
jupyter-events==0.10.0
jupyter-lsp==2.2.5
jupyter_client==8.6.2
jupyter_core==5.7.2
jupyter_server==2.14.2
jupyter_server_terminals==0.5.3
jupyterlab==4.2.4
jupyterlab_pygments==0.3.0
jupyterlab_server==2.27.3
kiwisolver==1.4.5
lion-pytorch==0.2.2
Markdown==3.6
markdown-it-py==3.0.0
MarkupSafe==2.1.5
matplotlib==3.9.1
matplotlib-inline==0.1.7
mdurl==0.1.2
mistune==3.0.2
mpmath==1.3.0
multidict==6.0.5
multiprocess==0.70.16
nbclient==0.10.0
nbconvert==7.16.4
nbformat==5.10.4
nest-asyncio==1.6.0
networkx==3.2.1
notebook_shim==0.2.4
numpy==1.26.3
overrides==7.7.0
packaging==24.1
pandas==2.2.2
pandocfilters==1.5.1
parso==0.8.4
peft==0.12.0
pexpect==4.9.0
pillow==10.2.0
platformdirs==4.2.2
pluggy==1.5.0
prometheus_client==0.20.0
prompt_toolkit==3.0.47
protobuf==4.25.4
psutil==6.0.0
ptyprocess==0.7.0
pure_eval==0.2.3
pyarrow==17.0.0
pyarrow-hotfix==0.6
pycparser==2.22
Pygments==2.18.0
pyparsing==3.1.2
pytest==8.3.2
python-dateutil==2.9.0.post0
python-json-logger==2.0.7
pytorch-triton-rocm==3.0.0
pytz==2024.1
PyYAML==6.0.1
pyzmq==26.0.3
referencing==0.35.1
regex==2024.7.24
requests==2.32.3
rfc3339-validator==0.1.4
rfc3986-validator==0.1.1
rich==13.7.1
rpds-py==0.19.1
safetensors==0.4.3
scipy==1.14.0
Send2Trash==1.8.3
setuptools==69.5.1
shtab==1.7.1
six==1.16.0
sniffio==1.3.1
soupsieve==2.5
stack-data==0.6.3
sympy==1.12
tensorboard==2.17.0
tensorboard-data-server==0.7.2
terminado==0.18.1
tinycss2==1.3.0
tokenizers==0.19.1
torch==2.4.0+rocm6.1
torchaudio==2.4.0+rocm6.1
torchvision==0.19.0+rocm6.1
tornado==6.4.1
tqdm==4.66.4
traitlets==5.14.3
transformers==4.43.3
trl==0.9.6
types-python-dateutil==2.9.0.20240316
typing_extensions==4.9.0
tyro==0.8.5
tzdata==2024.1
uri-template==1.3.0
urllib3==2.2.2
wcwidth==0.2.13
webcolors==24.6.0
webencodings==0.5.1
websocket-client==1.8.0
Werkzeug==3.0.3
wheel==0.43.0
xxhash==3.4.1
yarl==1.9.4
```

---
