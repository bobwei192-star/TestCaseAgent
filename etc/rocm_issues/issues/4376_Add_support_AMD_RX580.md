# Add support AMD RX580

> **Issue #4376**
> **状态**: open
> **创建时间**: 2025-02-14T14:06:54Z
> **更新时间**: 2025-02-20T23:25:57Z
> **作者**: Tamila-2017
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/4376

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

Hi,
When will you add the long-awaited AMD RX580 GPU support? This is a very common GPU.
A lot of people have bought it, are waiting and really hoping when you implement its support.
To do this, one year ago they created a [huge theme](https://github.com/ollama/ollama/issues/2453 )
Look at what's going on in this topic, and how many unsuccessful efforts they're making to make it work with ROCm by various workarounds!
Why don't you do anything to maintain your reputation??

### Operating System

Linux

### GPU

AMD RX580

### ROCm Component

_No response_

---

## 评论 (5 条)

### 评论 #1 — gl2007 (2025-02-16T19:19:20Z)

See [this thread](https://github.com/whyvl/ollama-vulkan/issues/7#issuecomment-2656349506) under [ollama-vulkan](https://github.com/whyvl/ollama-vulkan): got it to build and working

---

### 评论 #2 — Tamila-2017 (2025-02-19T21:43:19Z)

`See https://github.com/whyvl/ollama-vulkan/issues/7#issuecomment-2656349506 under [ollama-vulkan](https://github.com/whyvl/ollama-vulkan): got it to build and working`

Dear **gl 2007**,

Thank you. I have looked at these links and pages, but my modest knowledge is not enough to combine and get clear installation instructions.
Could you help me and explain how to make this installation so that the RX580 starts working?

PS. [**It**](https://github.com/ollama/ollama/issues/2453#issuecomment-2662481037) didn't work for me.

---

### 评论 #3 — gl2007 (2025-02-20T00:21:06Z)

> `See https://github.com/whyvl/ollama-vulkan/issues/7#issuecomment-2656349506 under [ollama-vulkan](https://github.com/whyvl/ollama-vulkan): got it to build and working`

[This comment](https://github.com/whyvl/ollama-vulkan/issues/7#issuecomment-2656379924) has ubuntu version. You might wanna try that if you cannot get the build to work. Anyway, what part of build didn't work for you? 

If you follow that thread, right from the comment above that, it should work i.e. from merging the patch, adding in the environment variables, installing gcc, installing Inno setup, and then running the relevant powershell script.



---

### 评论 #4 — Tamila-2017 (2025-02-20T05:59:10Z)

> https://github.com/whyvl/ollama-vulkan/issues/7#issuecomment-2656379924 has ubuntu version. You might wanna try that if you cannot get the build to work. Anyway, what part of build didn't work for you?

Yes, I see that there is a pleasant conversation going on in this topic between experienced experts who understand these complex things 😊
Unfortunately, I am not able to extract a complete guide to action from this conversation, it is too difficult.
Could you do me a favor and make a clear step-by-step guide for Debian or Ubuntu?

Here is an [example](https://github.com/ollama/ollama/issues/2453#issuecomment-2366982275) of such a clear guide.





---

### 评论 #5 — Tamila-2017 (2025-02-20T23:25:55Z)

I have installed **ubuntu-24.04.2-live-server-amd64** in console mode (without X).
Then I unfolded the contents [dist.zip]( https://github.com/whyvl/ollama-vulkan/issues/7#issuecomment-2656379924) in the /bin and /lib directories.

However, the **ollama serve** command generated a lot of errors 😔
What did I do wrong?

```
$ ollama serve
Couldn't find '/home/ai/.ollama/id_ed25519'. Generating new private key.
Your new public key is: 

ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBHZntlBob4JMCo2hbeo/HEJ3bEBGK3gIn0cagJYuCyp

2025/02/20 21:32:35 routes.go:1186: INFO server config env="map[CUDA_VISIBLE_DEVICES: GGML_VK_VISIBLE_DEVICES: GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_DEBUG:false OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://127.0.0.1:11434 OLLAMA_INTEL_GPU:false OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:/home/ai/.ollama/models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NUM_PARALLEL:0 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://*] OLLAMA_SCHED_SPREAD:false ROCR_VISIBLE_DEVICES: http_proxy: https_proxy: no_proxy:]"
time=2025-02-20T21:32:35.056Z level=INFO source=images.go:432 msg="total blobs: 0"
time=2025-02-20T21:32:35.056Z level=INFO source=images.go:439 msg="total unused blobs removed: 0"
[GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.

[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
 - using env:	export GIN_MODE=release
 - using code:	gin.SetMode(gin.ReleaseMode)

[GIN-debug] POST   /api/pull                 --> github.com/ollama/ollama/server.(*Server).PullHandler-fm (5 handlers)
[GIN-debug] POST   /api/generate             --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (5 handlers)
[GIN-debug] POST   /api/chat                 --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (5 handlers)
[GIN-debug] POST   /api/embed                --> github.com/ollama/ollama/server.(*Server).EmbedHandler-fm (5 handlers)
[GIN-debug] POST   /api/embeddings           --> github.com/ollama/ollama/server.(*Server).EmbeddingsHandler-fm (5 handlers)
[GIN-debug] POST   /api/create               --> github.com/ollama/ollama/server.(*Server).CreateHandler-fm (5 handlers)
[GIN-debug] POST   /api/push                 --> github.com/ollama/ollama/server.(*Server).PushHandler-fm (5 handlers)
[GIN-debug] POST   /api/copy                 --> github.com/ollama/ollama/server.(*Server).CopyHandler-fm (5 handlers)
[GIN-debug] DELETE /api/delete               --> github.com/ollama/ollama/server.(*Server).DeleteHandler-fm (5 handlers)
[GIN-debug] POST   /api/show                 --> github.com/ollama/ollama/server.(*Server).ShowHandler-fm (5 handlers)
[GIN-debug] POST   /api/blobs/:digest        --> github.com/ollama/ollama/server.(*Server).CreateBlobHandler-fm (5 handlers)
[GIN-debug] HEAD   /api/blobs/:digest        --> github.com/ollama/ollama/server.(*Server).HeadBlobHandler-fm (5 handlers)
[GIN-debug] GET    /api/ps                   --> github.com/ollama/ollama/server.(*Server).PsHandler-fm (5 handlers)
[GIN-debug] POST   /v1/chat/completions      --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (6 handlers)
[GIN-debug] POST   /v1/completions           --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (6 handlers)
[GIN-debug] POST   /v1/embeddings            --> github.com/ollama/ollama/server.(*Server).EmbedHandler-fm (6 handlers)
[GIN-debug] GET    /v1/models                --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (6 handlers)
[GIN-debug] GET    /v1/models/:model         --> github.com/ollama/ollama/server.(*Server).ShowHandler-fm (6 handlers)
[GIN-debug] GET    /                         --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func1 (5 handlers)
[GIN-debug] GET    /api/tags                 --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (5 handlers)
[GIN-debug] GET    /api/version              --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func2 (5 handlers)
[GIN-debug] HEAD   /                         --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func1 (5 handlers)
[GIN-debug] HEAD   /api/tags                 --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (5 handlers)
[GIN-debug] HEAD   /api/version              --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func2 (5 handlers)
time=2025-02-20T21:32:35.056Z level=INFO source=routes.go:1237 msg="Listening on 127.0.0.1:11434 (version 0.0.0)"
time=2025-02-20T21:32:35.057Z level=INFO source=gpu.go:255 msg="looking for compatible GPUs"
time=2025-02-20T21:32:35.060Z level=INFO source=gpu.go:203 msg="vulkan: failed to load libvulkan or libcap"
time=2025-02-20T21:32:35.060Z level=WARN source=amd_linux.go:61 msg="ollama recommends running the https://www.amd.com/en/support/linux-drivers" error="amdgpu version file missing: /sys/module/amdgpu/version stat /sys/module/amdgpu/version: no such file or directory"
time=2025-02-20T21:32:35.060Z level=WARN source=amd_linux.go:443 msg="amdgpu detected, but no compatible rocm library found.  Either install rocm v6, or follow manual install instructions at https://github.com/ollama/ollama/blob/main/docs/linux.md#manual-install"
time=2025-02-20T21:32:35.060Z level=WARN source=amd_linux.go:348 msg="unable to verify rocm library: no suitable rocm found, falling back to CPU"
time=2025-02-20T21:32:35.060Z level=INFO source=gpu.go:448 msg="no compatible GPUs were discovered"
time=2025-02-20T21:32:35.060Z level=INFO source=types.go:137 msg="inference compute" id=0 library=cpu variant="" compute="" driver=0.0 name="" total="15.6 GiB" available="15.1 GiB"

```




---
