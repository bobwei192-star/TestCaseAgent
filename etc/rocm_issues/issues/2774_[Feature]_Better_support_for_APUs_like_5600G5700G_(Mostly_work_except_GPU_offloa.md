# [Feature]: Better support for APUs like 5600G/5700G (Mostly work except GPU offloading of LLMs)

> **Issue #2774**
> **状态**: closed
> **创建时间**: 2024-01-03T11:20:37Z
> **更新时间**: 2025-01-30T22:36:06Z
> **关闭时间**: 2024-06-19T17:58:24Z
> **作者**: taweili
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2774

## 描述

### Suggestion Description

I just picked up a small computer with 5700G+64G RAM+1T drive for $400 to experiment with ROCm and plan to use it as a smart document assistance with some RAG programs. I am excited to see the improvement of ROCm over the past year. I was a bit frustrated and disappointed that APUs with gfx90c isn't officially support but I found some good hack and discussion on #1799 to get most of these works. I am documenting my setup in case they are useful. I really like to see official support in ROCm in these APUs. 

0. Picking the hardware. The main thing is to pick a good mainboard that support adjusting VRAM size in BIOS. 5700G is capable to have up to 16G of RAM dedicated. I am using [ASRock X300TM-ITX](https://www.asrock.com/mb/AMD/X300TM-ITX/index.asp). It's suggested to use DDR4 over 3200 MHz.
1. For the OS, I use Ubuntu 22.04
2. Getting Pytorch to work (mostly works...). Since gfx90c isn't officially support, one has to set the environment `HSA_OVERRIDE_GFX_VERSION` to 9.0.0 for gfx900. This makes most of the Pytorch examples work and takes advantages of the GPU in computation.  
```
$ export HSA_OVERRIDE_GFX_VERSION=9.0.0
```
3. This hack works for tiny LLMs like Phi-2 which can be loaded into memory and compute with GPU. However, it's extremely slow. And when it come sot use mid-size model like Mistral 7B. I am testing this with Huggingface transformers libraries. 
4. Getting [llama.cpp](https://github.com/ggerganov/llama.cpp) to work. This is another popular way to run LLMs. I built it from source with the following instructions. 
```
CMAKE_ARGS="-DLLAMA_HIPBLAS=on -DAMDGPU_TARGETS=gfx900" \
      CC=/opt/rocm/bin/hipcc CXX=/opt/rocm/bin/hipcc \
      pip install llama-cpp-python
```
5. The setup works to some extend. The CPU only inference delivers a 8.8 tokens/second with Mistral 7B. The speed is usable. 
```
$ ./bin/main -m models/dolphin-2.6-mistral-7b-dpo.Q4_K_M.gguf -p "Why is sky blue in 100 words?"
```
However, it hangs while attempting to offload layers of network to GPU. 
```
$ ./bin/main -m models/dolphin-2.6-mistral-7b-dpo.Q4_K_M.gguf -p "Why is sky blue in 100 words?" -ngl 2

...

llm_load_tensors: offloaded 2/33 layers to GPU
.............................................................................................

```

I am still digging into where it goes wrong with the GPU offloading. But with the current GPU speed, this little box is already usable as a small AI Assistant box. I hope to see the GPU working and official APUs support in the ROCm.

### Operating System

Ubuntu 22.04

### GPU

5700G

### ROCm Component

6.0.0 with everything

---

## 评论 (46 条)

### 评论 #1 — Dragomir-Ivanov (2024-02-03T01:20:26Z)

I am not sure VEGA architecture has INT4 data type computation support. I think only FP32 and FP16 are supported. Was your Phi-2 model quantized? 

---

### 评论 #2 — taweili (2024-02-07T14:37:29Z)

> I am not sure VEGA architecture has INT4 data type computation support. I think only FP32 and FP16 are supported. Was your Phi-2 model quantized?

Good point. Let me give fp16 model a try tomorrow. Thanks for the tip. 


---

### 评论 #3 — taweili (2024-02-08T08:58:03Z)

> I am not sure VEGA architecture has INT4 data type computation support. I think only FP32 and FP16 are supported. Was your Phi-2 model quantized?

Just got a chance to test. The fp16 model is loaded with Ollama and the VRAM is used. But the execution is still stuck. I am going to dig into this. 

Thanks for the suggestion. 


---

### 评论 #4 — cocoderss (2024-03-03T15:17:03Z)

> I am not sure VEGA architecture has INT4 data type computation support. I think only FP32 and FP16 are supported. Was your Phi-2 model quantized?

This is big deal. I have been trying for weeks to figure out why ollama was not offloading my models into gpu. This might be reason. It sucks that I invested in an iGPU only to learn to it won't work for my use case.   

1- Is this a hardware limitation or can be solved with a driver/software update? I assume the former?    
2- Would using Vulkan or CLBlast mitigate this limitation (ie allows us to use quantized models?).

---

### 评论 #5 — Dragomir-Ivanov (2024-03-03T17:53:12Z)

@cocoderss No, and No! If this is your issue, there is nothing else you can do about it, as it is hardware limitation. 
Also, investing in iGPU for ML is a stupid idea(apart from Mac M2/3), why would you consider it? Memory access of the iGPU is just too slow for ML to work good(again apart from Mac M2/3), even if you have INT4/8 support, as the latest AMD iGPUs.

---

### 评论 #6 — cocoderss (2024-03-03T19:08:05Z)

@Dragomir-Ivanov Thanks for confirming! It is not strictly for ML, mainly for a low cost/consumption home server with transcoding ability, but I wanted to have SD and some LLMs but I guess my options are quite limited. SD worked fine (slow generation but not bad). LLMs works fine on CPU, but ideally I wanted to offload it to the GPU. 

---

### 评论 #7 — Dragomir-Ivanov (2024-03-04T13:50:11Z)

@cocoderss 
You can't have more than 16GB VRAM on those iGPUs anyway. If you want to test things out, you can try free Google Colab, with T4 GPU with 16GB.

---

### 评论 #8 — taweili (2024-03-07T14:54:10Z)

> > I am not sure VEGA architecture has INT4 data type computation support. I think only FP32 and FP16 are supported. Was your Phi-2 model quantized?
> 
> This is big deal. I have been trying for weeks to figure out why ollama was not offloading my models into gpu. This might be reason. It sucks that I invested in an iGPU only to learn to it won't work for my use case.
> 
> 1- Is this a hardware limitation or can be solved with a driver/software update? I assume the former? 2- Would using Vulkan or CLBlast mitigate this limitation (ie allows us to use quantized models?).

I follow the suggestion here and use `export HSA_ENABLE_SDMA=0` before running ollama serve. It works for me to load mistral and other even it's Q4. 

https://github.com/ROCm/ROCm/issues/2781#issuecomment-1974938958

---

### 评论 #9 — taweili (2024-03-07T14:59:24Z)

> I am not sure VEGA architecture has INT4 data type computation support. I think only FP32 and FP16 are supported. Was your Phi-2 model quantized?

Happy to report that once I set the `export HSA_ENABLE_SDMA=0` before running Ollama, it works to load Q4 Mistral with Ollama on a 5700G. It brings the speed from 3.2 tokens/sec with CPU to 9.2 tokens/sec with iGPU. It's amazing to be able to do with with a sub-$500 PC and 50W TDP. 

---

### 评论 #10 — taweili (2024-03-07T15:13:48Z)

> @cocoderss No, and No! If this is your issue, there is nothing else you can do about it, as it is hardware limitation. Also, investing in iGPU for ML is a stupid idea(apart from Mac M2/3), why would you consider it? Memory access of the iGPU is just too slow for ML to work good(again apart from Mac M2/3), even if you have INT4/8 support, as the latest AMD iGPUs.

The use case I am looking for is a cheap server to run some RAG apps with Ollama backend in the office as a better document search engine. My testing 5700G machine with 64G memory and 1T drive costs about $450. Mac Mini with M2 can easily be $3000. I am sure M2 would run faster, but in this case, 9 tokens/sec is sufficient. 

---

### 评论 #11 — Dragomir-Ivanov (2024-03-08T12:05:37Z)

@taweili Congratulations :)
I may test this with my 5700G when have more time. 
I see one discrepancy, in the initial message "Suggestion Description", you say that your CPU perf is 8.8T/s on Mixtral7B, 
but in your final statement is 3.2T/s. Can you double check.
Also, did you made any additional setup than your initial description? I thing it would be immensely valuable for other people trying to achieve the same thing.

---

### 评论 #12 — taweili (2024-03-08T14:37:33Z)

> @taweili Congratulations :) I may test this with my 5700G when have more time. I see one discrepancy, in the initial message "Suggestion Description", you say that your CPU perf is 8.8T/s on Mixtral7B, but in your final statement is 3.2T/s. Can you double check. Also, did you made any additional setup than your initial description? I thing it would be immensely valuable for other people trying to achieve the same thing.

One is taken directly from llama.cpp and the other is using Ollama. I plan to do better benchmarking this weekend. 

---

### 评论 #13 — GZGavinZhao (2024-03-08T14:46:16Z)

Can confirm that `HSA_ENABLE_SDMA=0` also works with Ryzen 7 5800H (`gfx90c` / emulated as `gfx900`).

---

### 评论 #14 — taweili (2024-03-09T13:19:14Z)

@Dragomir-Ivanov 

Here are some benchmarking result from the 5700G using llama.cpp and [Mistral-7b gguf ](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF). The llama.cpp is the latest version and configured as described in this post. The improvement is not as significant as seen with Ollama. I suspect Ollama has hold back some of the CPU optimization of llama.cpp. The CPU was loaded at 95% on all 16 threads observed using `htop` while in GPU mode and at about 75% while offloads are enabled. The data on VRAM and GPU usage is from rocm-smi. 

While result of 8.83 to 9.35 T/s isn't significant, it's worth investigate whether there are a lot of movement of data between CPU and GPU and whether or not that can be optimized with hipHostMalloc #2781 to reduce the data copy and hopefully improve the performance.   

|NGL/Layers|Tokens/second|GPU Loading|VRAM% (16G)|
|--|--|--|--|
|0|8.83|2%|2%|
|5|7.36|30%|10%|
|10|7.57|40%|14%|
|15|8.10|50%|17%|
|20|8.30|64%|21%|
|25|8.77|77%|25%|
|30|9.10|90%|29%|
|33|9.35|99%|34%|

---

### 评论 #15 — taweili (2024-03-09T14:14:59Z)

I just found this on #2014 and it could be of interest here as well. It forces the use of hipHostMalloc on APU. I am going to try it when I get some time. 

https://github.com/segurac/force-host-alloction-APU

---

### 评论 #16 — Dragomir-Ivanov (2024-03-09T14:18:17Z)

@taweili 
Thank you for all the effort putting into this. Keep in mind that Ollama is just a wrapper over llama.cpp, so it might be using older version of llama.cpp, and probably could catch soon. From your results, it suggests all the effort of using ROCm is not worth it. Just 0.5T/s increase. I hope `hipHostMalloc` gives some gains.

---

### 评论 #17 — marcopennelli (2024-03-10T18:53:46Z)

@taweili 
Which version of Ollama are you using?

---

### 评论 #18 — robertvazan (2024-03-10T23:58:42Z)

> From your results, it suggests all the effort of using ROCm is not worth it. Just 0.5T/s increase.

Prompt processing improvement is likely more dramatic. On Ryzen 5600G with ROCm 5.7, it goes from 17t/s to 40t/s. GPU offload also has the side benefits of releasing CPU for other workload and reducing power consumption.

---

### 评论 #19 — taweili (2024-03-11T01:50:58Z)

> @taweili Which version of Ollama are you using?

I am running 0.1.28. 

---

### 评论 #20 — robertvazan (2024-03-11T02:07:06Z)

@Dragomir-Ivanov 

> Also, investing in iGPU for ML is a stupid idea(apart from Mac M2/3), why would you consider it? Memory access of the iGPU is just too slow for ML to work good(again apart from Mac M2/3), even if you have INT4/8 support, as the latest AMD iGPUs.

I would briefly challenge this. $200 APU with 64GB of DDR5 RAM (also $200) can run 4-bit Mixtral 8x7B smoothly whereas $2,000 GPU cannot even fit it in its 24GB VRAM. If iGPU is used (requires UMA or a system supporting 32GB preallocated VRAM), you get faster prompt processing and lower power/heat.

---

### 评论 #21 — taweili (2024-03-11T02:10:49Z)

> > From your results, it suggests all the effort of using ROCm is not worth it. Just 0.5T/s increase.
> 
> Prompt processing improvement is likely more dramatic. On Ryzen 5600G with ROCm 5.7, it goes from 17t/s to 40t/s. GPU offload also has the side benefits of releasing CPU for other workload and reducing power consumption.

That's a good point. I am using these small APU machines to run RAG applications. I will soon benchmark this with a large document collection and a large vector database. With LLM offloaded to the GPU, the freed GPU can be used on the application side. 

Given that the 5600G/5700G has a fairly modern CPU (R7 Zen 3) and a slightly outdated GPU (Radeon RX 550*, or the GeForce GTX 560* equivalence), a small performance gain should be expected. However, the UMA memory model in the APU could now be exploited for potential optimization. Most codes today assume discrete GPUs with much data moving in the memory. 

I expect a more drastic improvement with the new 8700G and 8845HS. I am getting a new notebook with 8845HS soon and will report with a new benchmark. I am setting my sights on the Lenovo Xiaoxin 14", which packs a lot of potential for $700. 

---

### 评论 #22 — GZGavinZhao (2024-03-11T02:16:41Z)

My experience with UMA (5800H + 64GB DDR4 RAM) is that it drastically slows down inference speed, possibly due to the need to transfer memory back and forth between iGPU and RAM. Admittedly it's 5800H, whose iGPU can be considered as `gfx900` (something like Vega 64) and not even RDNA, but still I'm surprised when UMA llama.cpp inference speed is even slower than CPU. Hopefully its because the older iGPUs are just not optimized for UMA.

---

### 评论 #23 — Dragomir-Ivanov (2024-03-11T11:19:37Z)

@robertvazan I might be mistaken, but with ROCm, you can't get beyond VRAM allocation allowed in the BIOS. In my case, it is 16GB. If you were able to run Mixtral Q4 can you please point us to how-to do this on 5(6/7)00G, and were able to see the boost from 17 T/s to 40 T/s.
You mentioned 32GB VRAM allocation, can you share how you did that? Which motherboard, etc. Mine is ASRock B550M Pro4, so only 16GB available.
Currently my main machine is 5700G, but in a month or so, I will get Framework Laptop with AMD 7640U, which has RDNA3 type of iGPU, and more interestingly AMD's NPU unit, that supports UMA, with perormance of 10 TOPs of INT8.

---

### 评论 #24 — Ristovski (2024-03-11T12:33:07Z)

Most of the limitations I am seeing here are from ROCm seemingly doing CPU <-> iGPU memory copies on APUs despite both sharing the same physical RAM. This is not only causing duplicate memory usage, but it also requires people to allocate large amounts of RAM as VRAM which is quite inconvenient, especially given that the max amount of VRAM you can allocate differs across motherboards.

In OpenGL, it is possible to map a CPU-side buffer directly to the GPU with [AMD_pinned_memory](https://registry.khronos.org/OpenGL/extensions/AMD/AMD_pinned_memory.txt), on Vulkan this is possible by setting the `HOST_VISIBLE | HOST_COHERENT | HOST_CACHED` flags. Doing this on regular GPUs would be slow as the memory bandwidth would be limited by PCI speeds, but on APUs the memory is shared - I have benchmarked this and there is negligible performance loss doing `memcpy`/`memset` across CPU <-> GPU with mapped buffers.

I have tested both approaches and I can indeed share a large CPU-side 12GB buffer to the iGPU with no copies being made (with mere 512MB VRAM allocated in BIOS), which shows up as `GTT` in tools like `radeontop`.

Both OpenGL and Vulkan have a limit on how big a single allocation/map can be, in this case: 1 byte short of 4GB. The 5700G with `radv` Vulkan driver however supports the [VK_AMD_memory_overallocation_behavior](https://registry.khronos.org/vulkan/specs/1.3-extensions/man/html/VK_AMD_memory_overallocation_behavior.html) extension which allows to bypass this limit. Using this, I can map the 12GB buffer in one go.

There are also several approaches to get ROCm to use "host memory" ala https://github.com/pomoke/torch-apu-helper/, but I am still not sure if ROCm is smart enough to realize this is shared memory and thus prevent memory copies from happening. From my testing, the passed memory buffer also needs to be page-aligned.

If there is some way to get ROCm to properly work on APUs such as the 5700G while allowing the use of mapped/shared memory buffers, and given ROCm has no inherent buffer size limit like OpenGL/Vulkan, then it should in theory be possible to load arbitrarily large models, with the amount of system RAM being the only limit.

Sadly, even high-end consumer GPUs are second-class citizens in ROCm, let alone APUs :)

----

PS: Just to give a rough idea on the performance of the 5700G iGPU (overclocked to 2300MHz): 
```
fp32-scalar  = 2348.02 GFLOPS
fp32-vec4    = 2352.85 GFLOPS

fp16-scalar  = 2351.20 GFLOPS
fp16-vec4    = 4179.10 GFLOPS
```
(measured with [vkpeak](https://github.com/nihui/vkpeak))

---

### 评论 #25 — robertvazan (2024-03-11T16:39:38Z)

@Dragomir-Ivanov When I said "requires UMA or a system supporting 32GB preallocated VRAM", I meant that as a prerequisite. 64GB systems can have 32GB UMA AFAIK, but ROCm would have to support UMA. I don't know whether the 16GB VRAM limitation is just in BIOS or whether it's hardwired in hardware.

---

### 评论 #26 — Dragomir-Ivanov (2024-03-11T18:23:30Z)

@robertvazan Thank you for clarification. I wonder what is the topology of Radeon Instincts, especially MI300A? Don't they used UMA, since they also include CPU inside. Fun fact, MI300A, has 1960 TOPs of INT8 performance :)

---

### 评论 #27 — GZGavinZhao (2024-03-15T00:57:05Z)

> There are also several approaches to get ROCm to use "host memory" ala https://github.com/pomoke/torch-apu-helper/, but I am still not sure if ROCm is smart enough to realize this is shared memory and thus prevent memory copies from happening. From my testing, the passed memory buffer also needs to be page-aligned.

According to my testing, at least on 5800H (`gfx90c`) + ROCm 6.0, ROCm unfortunately doesn't realize it's shared memory and the memory is still copied back and forth between the CPU and iGPU.

---

### 评论 #28 — ppanchad-amd (2024-05-17T19:20:23Z)

@taweili Do you still need assistance with ticket? If not, please close. Thanks!

---

### 评论 #29 — Djip007 (2024-06-22T22:07:48Z)

I'd be curious to see what it can look like with a ryzen 6800 and its RDNA2

Anyway many progress have be made evryware (CPU (thanks to llamafile) and GPU):
- https://github.com/ggerganov/llama.cpp/pull/7414
- https://github.com/Mozilla-Ocho/llamafile/discussions/468

for AMD 7640U and the new 8700G and 8845HS , you can see some bench with my 7940HS that has pretty the same hardware. (hop to make some more progress an iGPU but not as simple as last patch)

The next think I am waiting is what we can get with the next Ryzen AI HX 370/365.

---

### 评论 #30 — winstonma (2024-06-25T23:59:41Z)

@Djip007 I am using Ryzen 6800U on Ubuntu 24.04. Yesterday I tested the llamafile but I have no luck running on the GPU. I would like to know how can I troubleshoot? Thanks

First of all I couldn't install AMD driver because Ubuntu 24.04 is not officially supported (Ubuntu 24.04 already have [hipcc](https://packages.ubuntu.com/en/noble/hipcc) and [libhipblas0](https://packages.ubuntu.com/en/noble/libhipblas0)) so do I need to install the AMD driver?

I should provide more information on my current system. I am running Stable Diffusion on Ubuntu 24.04 with only installing Linux Kernel 6.10-rc as it support ["Small" Ryzen APUs](https://gitlab.freedesktop.org/drm/kernel/-/commit/eb853413d02c8d9b27942429b261a9eef228f005).

EDIT: Seems running the llamafile using `-ngl 9999` would offload to iGPU

---

### 评论 #31 — cocoderss (2024-06-26T10:00:17Z)

> @Djip007 I am using Ryzen 6800U on Ubuntu 24.04. Yesterday I tested the llamafile but I have no luck running on the GPU. I would like to know how can I troubleshoot? Thanks
> 
> First of all I couldn't install AMD driver because Ubuntu 24.04 is not officially supported (Ubuntu 24.04 already have [hipcc](https://packages.ubuntu.com/en/noble/hipcc) and [libhipblas0](https://packages.ubuntu.com/en/noble/libhipblas0)) so do I need to install the AMD driver?
> 
> I should provide more information on my current system. I am running Stable Diffusion on Ubuntu 24.04 with only installing Linux Kernel 6.10-rc as it support ["Small" Ryzen APUs](https://gitlab.freedesktop.org/drm/kernel/-/commit/eb853413d02c8d9b27942429b261a9eef228f005).

To preface, I don't have experience with Ubuntu 24.04, but the setup is now rather simple to get llama.cpp running on AMD APU (iGPU). Tested on my 4650G setup. Did you follow any specific guide if so link it, or list the steps taken to help you debug.   
But generally speaking, what you need to do is (feel free to google/gpt how to do each step):

- [ ] Grant your user access to `/dev/kfd` 
- [ ] Add your user to `render` and `video` group
- [ ] Make sure you have the latest [AMD linux drivers](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html#ubuntu)
- [ ] You have to update the environment variable `HSA_OVERRIDE_GFX_VERSION` to match your APU version, in your case after a quick search the 6800U is RDNA2 base thus you need to set the following value `HSA_OVERRIDE_GFX_VERSION=10.3.0`
- [ ]  Additionally as mentioned earlier, you need to also set the following env variable `HSA_ENABLE_SDMA=0`
- [ ] For llama.cpp, after cloning the repo, you can build it using the following flags `make LLAMA_HIPBLAS=1 LLAMA_HIP_UMA=1 AMDGPU_TARGETS=gfx1030`, make sure to replace `AMDGPU_TARGETS` with the correct ones depending on your APU version (in your case I think it's gfx1030). 

That's it, if you take care of all of these points, you should have a functioning llama.cpp running on your iGPU. I tested this recently on Debian 12, and Ubuntu 22.04.


---

### 评论 #32 — Dragomir-Ivanov (2024-06-26T16:13:59Z)

@cocoderss Thanks for the guidance. What is the expected performance vs CPU only?

---

### 评论 #33 — taweili (2024-08-05T15:15:23Z)

> @cocoderss Thanks for the guidance. What is the expected performance vs CPU only?

I am using 8845HS running Ollama. It's nine tokens/sec with CPU vs 13 tokens/sec with the iGPU. The difference is small, but using iGPU frees up the CPU for other tasks. 

---

### 评论 #34 — roger- (2024-08-31T22:05:08Z)

@cocoderss I'm considering a small PC with a 4650GE; do you see any advantage using the iGPU? I hear [mixed results](https://www.reddit.com/r/LocalLLaMA/comments/18ny92b/full_memory_available_for_amd_apus/kh29v2n/). 

---

### 评论 #35 — cocoderss (2024-09-10T13:27:20Z)

> @cocoderss I'm considering a small PC with a 4650GE; do you see any advantage using the iGPU? I hear [mixed results](https://www.reddit.com/r/LocalLLaMA/comments/18ny92b/full_memory_available_for_amd_apus/kh29v2n/).

Unforunately I moved on, trying to get ROCm to work reliably on the APU (iGPU) was really frustrating. It was exciting to tinker with it in the beginning, especially with the promise of taking advantage of the full ram capability of my system (which is nicer with linux 6.10), especially when you get it to work, but it is extremely unstable, even with llama.cpp built with ROCm support there is always something to debug between (kernel, llama, rocm, amdgpu) updates. This wore me down progressively, as it's really unreliable.

But to answer your question, 1 example for `deepseek-coder-33b-instruct.Q6_K.gguf`, on the CPU I got around 1 tk/s, on the GPU (many LLama.cpp moons ago) around 1.3 tk/s.   

Recently I got myself an Nvidia RTX 4000 SFF with 20GB VRAM which is perfect for my setup (low consmption home server). If you have the time to Highly recommended if you have the budget for it. 

As of today, AMD APU (GPU) development stack is not even on the same level to that of Nvidia, which is sad, because APUs seems to be the best consumer available hardware right now. So I hope this changes. 

---

### 评论 #36 — rohitnanda1443 (2024-10-02T07:32:09Z)

Any ideas howto use vllm on a 780m / Ryzen 8700G chip? 

---

### 评论 #37 — roger- (2024-10-02T11:21:37Z)

I ended up getting an 8845hs with a 780m and getting it to working with Ollama isn't too hard. 

Major problem is the stability. I get pretty frequent crashes and have trouble loading larger models. Still some ways to go but it's promising if upstream gets improved. 

---

### 评论 #38 — Dragomir-Ivanov (2024-10-02T13:23:52Z)

Roger @roger- ! Buy why,?

---

### 评论 #39 — rohitnanda1443 (2024-10-02T14:07:53Z)

> Roger @roger- ! Buy why,?

I tried Ollama: Mistral works on iGPU but the llama3.1 does not (Both are similar sizes ~6.5GB) and available vram is 16GB. 

Yes, there is some issue here. 

---

### 评论 #40 — Dragomir-Ivanov (2024-10-03T11:38:45Z)

@rohitnanda1443 My question wasn't to you, but still the same? Why go through all this hassle, when you can buy inexpensive R 7600 XT with 16GB of VRAM, and NN will work much faster there.

---

### 评论 #41 — roger- (2024-10-03T13:33:45Z)

> @rohitnanda1443 My question wasn't to you, but still the same? Why go through all this hassle, when you can buy inexpensive R 7600 XT with 16GB of VRAM, and NN will work much faster there.

My priority was a low power, yet capable mini PC. LLMs are a bonus :) 

---

### 评论 #42 — rohitnanda1443 (2024-10-04T01:56:57Z)

> @rohitnanda1443 My question wasn't to you, but still the same? Why go through all this hassle, when you can buy inexpensive R 7600 XT with 16GB of VRAM, and NN will work much faster there.

I had read on a reddit post that Ryzen 8700G can have 32GB of UMA. That is why took that. 

---

### 评论 #43 — Dragomir-Ivanov (2024-10-08T11:40:58Z)

@rohitnanda1443 
Theoretically maybe, however my BIOS has the option to go only to 16GB.  In any case, UMA will be much much slower than dedicated VRAM you have on your GPU. Don't look at M3 chips, there the RAM is soldered directly on the CPU substrate, so it is much closer to the CPU, and have much less latency and higher frequencies, only because the wires to the RAM are the shortest. 

Also theoretically you will have the same 32GB of memory with 2 x 7600 XT, where you divide the parts of the model into the two GPUs. 

In any case, I was enthusiastic about this whole AMD APU LLM think, but now I think it is more of a masochism. 

---

### 评论 #44 — SMH17 (2024-12-06T22:57:27Z)

In BIOS you set UMA frame buffer dedicated memory, not whole memory that can be actually used in UMA mode by iGPU. The main problem here is the missing of proper software support that currently uses iGPUs in an awfully inefficient way and so limiting a lot the hardware potential of these small inexpensive pieces of hardware.

---

### 评论 #45 — winstonma (2024-12-09T09:18:27Z)

@rohitnanda1443 You can take a look at https://github.com/ollama/ollama/pull/6282. You can set the amount of graphics translation table (GTT) memory by setting `/etc/modprobe.d/ttm.conf`. By default the GTT memory is half of the system.

This is the setting from my 16GB memory laptop:

```bash
$ sudo dmesg | grep -P '^(?=.*amdgpu)(?=.*memory)'
[    4.258469] [drm] amdgpu: 512M of VRAM memory ready
[    4.258473] [drm] amdgpu: 12288M of GTT memory ready.
```

Under default settings, the GTT memory allocation is configured to be 50% of the total system memory.

Currently ollama doesn't support iGPU. You need to follow the above post to download and build the ollama from patched sourcecode.

---

### 评论 #46 — lkraav (2025-01-30T22:36:04Z)

> In any case, I was enthusiastic about this whole AMD APU LLM think, but now I think it is more of a masochism.

Regardless, this 🧵 has been super-educational for a new person's discovery process of all the available options and why something is better than something else, tyvm all 🙏 

Also looking into what I can do on my 5700G/64GB passively cooled case server, that could potentially also fit a real video card, but concerned a bit about increasing thermals.

---
