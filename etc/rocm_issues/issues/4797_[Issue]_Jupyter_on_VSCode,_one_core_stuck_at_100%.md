# [Issue]: Jupyter on VSCode, one core stuck at 100%

> **Issue #4797**
> **状态**: open
> **创建时间**: 2025-05-23T23:09:00Z
> **更新时间**: 2025-07-17T17:26:33Z
> **作者**: TikoTako
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4797

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

First , i'm using wsl2 on windows 10 so maybe is this.
I used a cell (vscode + jupyter) to load a whisper model and keep it loaded but one CPU core is stuck at 100%, this happens with torch load too.
If i use device = cpu instead of cuda it work fine (model is loaded ram usage go up, the cpu does nothing since the model is not in use).

### Operating System

Ubuntu 24.04.2 LTS (Noble Numbat)

### CPU

13th Gen Intel(R) Core(TM) i5-13600K

### GPU

AMD Radeon RX 7800 XT

### ROCm Version

ROCm 6.4.0

### ROCm Component

_No response_

### Steps to Reproduce

whisper_model = whisper.load_model("tiny", device="cuda")

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — schung-amd (2025-05-26T14:24:40Z)

Hi @TikoTako, to clarify, are you seeing a hang? If so, does setting `HSA_ENABLE_SDMA=0` change anything? 

---

### 评论 #2 — TikoTako (2025-05-27T11:39:13Z)

Hi @schung-amd, thanks for your reply.
No, I'm not seeing a hang, when I use device="cpu" in cell 1, the model loads, and the CPU (all cores) goes idle until I run cell 2.
At that point, the CPU cores work as expected and return to idle when processing is done.
However, when I use device="cuda", the model loads onto the GPU (I can see VRAM usage increase), but instead of the CPU going idle, one core stays stuck at 100% usage.

I made this as test:
Cell 1:
```
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HSA_ENABLE_SDMA"] = "0"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

device = "cpu" # "cuda"
model_n = "Qwen/Qwen2-0.5B"

tokenizer = AutoTokenizer.from_pretrained(model_n, local_files_only=True, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_n, local_files_only=True, trust_remote_code=True, torch_dtype=torch.float16).to(device)
model.eval()
```
Cell 2:
```
prompt = "the dog is"
inputs = tokenizer(prompt, return_tensors="pt").to(device)

with torch.no_grad():
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=150,          # Numero massimo di token generati
        temperature=0.7,             # Casualità della generazione
        top_p=0.9,                   # Nucleus sampling
        do_sample=True,              # Abilita campionamento
        pad_token_id=tokenizer.eos_token_id  # Evita warning
    )

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("qwen >", response)
```


---

### 评论 #3 — schung-amd (2025-05-27T13:26:39Z)

Thanks for the reproducer! I'll take a look.

---

### 评论 #4 — TikoTako (2025-05-27T13:30:28Z)

I've checked with the profiler, i think is the hipDeviceSynchronize in busy-waiting mode and only that mode is implemented.
HIP docs -> [hipDeviceSynchronize()](https://rocm.docs.amd.com/projects/HIP/en/docs-6.4.0/doxygen/html/group___device.html#gaefdc2847fb1d6c3fb1354e827a191ebd)


---

### 评论 #5 — schung-amd (2025-06-24T19:44:56Z)

@TikoTako Sorry for the delay on this, was sidetracked with other issues. To clarify, are you seeing a CPU core stuck spinning at 100% after running cell 1 and before running cell 2? I tried to reproduce this in a Jupyter notebook both inside and outside of VSCode (albeit on native Linux and not WSL), I only see a spin while cell 2 is performing inference. If this is a wait as you've seen in the profiler, then I think the spinning is expected here.

---

### 评论 #6 — TikoTako (2025-06-24T21:28:12Z)

with just cell 1 and device = "cuda" one core is stuck at 100%
with device = "cpu" the cpu is idle when the cell 1 load end


---

### 评论 #7 — schung-amd (2025-06-27T18:55:24Z)

Ok, I can repro this in WSL. I also see the issue in WSL when running a Jupyter server in WSL outside of VSCode. Looking into it, not sure at the moment if this issue is on our end or with Jupyter's backend. It seems like there are some forked processes being spawned under the hood which are not being terminated properly in WSL.

---

### 评论 #8 — schung-amd (2025-07-17T17:26:32Z)

It turns out we don't yet officially support the ROCm + Jupyter + WSL stack, so this may take a while to get a fix for.

---
