# [Issue]: Excessive VRAM Allocation with ComfyUI

> **Issue #5778**
> **状态**: closed
> **创建时间**: 2025-12-15T19:34:47Z
> **更新时间**: 2026-01-04T11:15:13Z
> **关闭时间**: 2026-01-04T11:15:13Z
> **作者**: TawusGames
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5778

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

wan2.2 I2V A14B High noise Q2_K with high noise lora
wan2.2 I2V A14B Low noise Q2_K with low noise lora
umt5 xxl encoder Q3_K_S

latent size 848x480

5 second first image to last image video generation. It tried to allocate 85 GB of memory. I’m not sure if it’s normal for it to request this much memory, but it seems a bit excessive to me.

### Operating System

Bazzite OS (distrobox ubuntu) ComfyUI git clone non portable

### CPU

r7 7700 32 gb ram

### GPU

rx 9060 xt 16 gb

### ROCm Version

7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

Download the workflow I’m using. Install the dependencies. Add two images, don’t enter a prompt, and just run it.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

[wan22_ftl_14B_gguf_upscale 2.0.json](https://github.com/user-attachments/files/24174043/wan22_ftl_14B_gguf_upscale.2.0.json)

![Image](https://github.com/user-attachments/assets/89120825-77f3-4b25-8cfc-269d4a5c3092)

---

## 评论 (8 条)

### 评论 #1 — TawusGames (2025-12-16T17:48:16Z)

This issue occurs when generating only in 16:9 resolutions. (I even tried 640×360.) In 1:1 aspect ratio resolutions, I can generate even a 10-second video at 1024×1024.

---

### 评论 #2 — TawusGames (2025-12-23T13:08:41Z)

After turning off the CWSR feature, I resolved the memory access error. The likelihood of successfully generating videos has increased significantly, but it still cannot always generate some 640x640 videos. Sometime tries to allocate about 25GB of RAM but some times fit in 16 gb VRAM. For 848x480 videos, it still requires around 83GB of RAM. I am using wan.2.2 i2v Q2_K gguf (high and low noise model with 4 step lora) version of the model but no luck for 16/9 aspect ratio.

---

### 评论 #3 — amd-nicknick (2025-12-29T06:08:38Z)

Hi @TawusGames, could you please try with Unet Loader (GGUF) and CLIP Loader (GGUF) instead of DisTorchMultiGPU? I tested and it works fine on my end.

---

### 评论 #4 — TawusGames (2025-12-29T11:16:45Z)

I had tried this before, but I tried again today. (848x480 gguf (unet) 4 step) It still doesn't work due to absurd amounts of RAM allocation. I experience fewer issues with square images. It doesn’t work with 16/9 images completely.  I also tried other workflows (S2V, I2V, FTL2V, comfyui offical workflows), thinking there might be an issue with the workflow itself. 

![Image](https://github.com/user-attachments/assets/b1f4cbdd-1d57-48de-af89-bf19924c55f2)

---

### 评论 #5 — amd-nicknick (2026-01-02T06:52:45Z)

@TawusGames I wasn't able to repro the issue with your workflow + ROCm Nightlies.
Are you sure you're using the correct model?
My PIP freeze:
```
accelerate==1.12.0
aiohappyeyeballs==2.6.1
aiohttp==3.13.2
aiosignal==1.4.0
alembic==1.17.2
annotated-types==0.7.0
anyio==4.12.0
attrs==25.4.0
av==16.0.1
certifi==2025.11.12
charset-normalizer==3.4.4
clip-interrogator==0.6.0
color-matcher==0.6.0
coloredlogs==15.0.1
comfyui-embedded-docs==0.3.1
comfyui-workflow-templates-core==0.3.61
comfyui-workflow-templates-media-api==0.3.34
comfyui-workflow-templates-media-image==0.3.43
comfyui-workflow-templates-media-other==0.3.62
comfyui-workflow-templates-media-video==0.3.22
comfyui_frontend_package==1.35.9
comfyui_workflow_templates==0.7.64
contourpy==1.3.3
cupy-cuda12x==12.3.0
cupy-wheel==12.3.0
cycler==0.12.1
ddt==1.7.2
deepdiff==8.6.1
diffusers==0.36.0
docutils==0.22.4
einops==0.8.1
fastrlock==0.8.3
filelock==3.19.1
flatbuffers==25.12.19
fonttools==4.61.1
frozenlist==1.8.0
fsspec==2025.7.0
ftfy==6.3.1
gguf==0.17.1
gguf-node==0.2.8
greenlet==3.3.0
h11==0.16.0
hf-xet==1.2.0
httpcore==1.0.9
httpx==0.28.1
huggingface-hub==0.36.0
humanfriendly==10.0
idna==3.11
ImageIO==2.37.2
imageio-ffmpeg==0.6.0
importlib_metadata==8.7.1
Jinja2==3.1.6
kiwisolver==1.4.9
kornia==0.8.2
kornia_rs==0.1.10
lark==1.3.1
Mako==1.3.10
MarkupSafe==3.0.2
matplotlib==3.10.8
mpmath==1.3.0
mss==10.1.0
multidict==6.7.0
networkx==3.5
numpy==2.2.6
nvidia-ml-py==13.590.44
onnxruntime==1.23.2
open_clip_torch==3.2.0
opencv-contrib-python==4.12.0.88
opencv-python==4.12.0.88
opencv-python-headless==4.12.0.88
orderly-set==5.5.0
packaging==25.0
peft==0.18.0
piexif==1.1.3
pillow==11.3.0
propcache==0.4.1
protobuf==6.33.2
psutil==7.2.0
py-cpuinfo==9.0.0
pydantic==2.12.5
pydantic-settings==2.12.0
pydantic_core==2.41.5
pynvml==13.0.1
pyparsing==3.3.1
python-dateutil==2.9.0.post0
python-dotenv==1.2.1
PyYAML==6.0.3
regex==2025.11.3
requests==2.32.5
rocm==7.11.0a20251225
rocm-sdk-core==7.11.0a20251225
rocm-sdk-libraries-gfx120X-all==7.11.0a20251225
safetensors==0.7.0
scipy==1.16.3
sentencepiece==0.2.1
setuptools==80.9.0
six==1.17.0
spandrel==0.4.1
SQLAlchemy==2.0.45
sympy==1.14.0
timm==1.0.22
tokenizers==0.22.1
torch==2.11.0a0+rocm7.11.0a20251225
torchaudio==2.10.0a0+rocm7.11.0a20251225
torchsde==0.2.6
torchvision==0.25.0a0+rocm7.11.0a20251225
tqdm==4.67.1
trampoline==0.1.2
transformers==4.57.3
triton==3.6.0+gita1fa3509.rocm7.11.0a20251225
typing-inspection==0.4.2
typing_extensions==4.14.1
urllib3==2.6.2
wcwidth==0.2.14
yarl==1.22.0
zipp==3.23.0
```
Which phase is it failing at? ComfyUI auto-fallback to tiled VAE for me, and the VRAM utilization never surpassed 86% during sampling.
Could you provide logs and identify which model / node is issuing the allocation? My log for reference:
```
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
[MultiGPU Core Patching] text_encoder_device_patched returning device: cuda:0 (current_text_encoder_device=cuda:0)
Requested to load CLIPVisionModelProjection
loaded completely; 14540.80 MB usable, 1208.10 MB loaded, full load: True
gguf qtypes: Q3_K (168), F32 (73), Q6_K (1)
Attempting to recreate sentencepiece tokenizer from GGUF file metadata...
Created tokenizer with vocab size of 256384
Dequantizing token_embd.weight to prevent runtime OOM.
[MultiGPU Core Patching] text_encoder_device_patched returning device: cuda:0 (current_text_encoder_device=cuda:0)
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cpu, dtype: torch.float16
Requested to load WanTEModel
loaded completely; 12974.63 MB usable, 3901.45 MB loaded, full load: True
gguf qtypes: F16 (694), Q2_K (320), Q3_K (80), F32 (1)
model weight dtype torch.float16, manual cast: None
model_type FLOW
Requested to load WanVAE
loaded completely; 5109.68 MB usable, 242.03 MB loaded, full load: True
Warning: Ran out of memory when regular VAE encoding, retrying with tiled VAE encoding.
Requested to load WAN21
loaded completely; 8674.94 MB usable, 5187.97 MB loaded, full load: True
[ComfyUI-Easy-Use] server: v1.3.4 Loaded
[ComfyUI-Easy-Use] web root: /home/nick/Documents/comfyui/ComfyUI/custom_nodes/ComfyUI-Easy-Use/web_version/v2 Loaded

[rgthree-comfy] Loaded 48 extraordinary nodes. 🎉

[rgthree-comfy] ComfyUI's new Node 2.0 rendering may be incompatible with some rgthree-comfy nodes and features, breaking some rendering as well as losing the ability to access a node's properties (a vital part of many nodes). It also appears to run MUCH more slowly spiking CPU usage and causing jankiness and unresponsiveness, especially with large workflows. Personally I am not planning to use the new Nodes 2.0 and, unfortunately, am not able to invest the time to investigate and overhaul rgthree-comfy where needed. If you have issues when Nodes 2.0 is enabled, I'd urge you to switch it off as well and join me in hoping ComfyUI is not planning to deprecate the existing, stable canvas rendering all together.

[rgthree-comfy][Power Lora Loader] Lora "high_noise_model.safetensors" not found, skipping.
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [01:07<00:00, 33.61s/it]
gguf qtypes: F16 (694), Q2_K (320), Q3_K (80), F32 (1)
model weight dtype torch.float16, manual cast: None
model_type FLOW
Requested to load WanVAE
loaded completely; 4261.31 MB usable, 242.03 MB loaded, full load: True
Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.
Prompt executed in 229.42 seconds
```

---

### 评论 #6 — TawusGames (2026-01-02T12:50:11Z)

@amd-nicknick 

I've also tried different models and workflows, but the same issue persists. I'm sure I'm using the correct model.

I’m getting an out-of-memory error during ksampler. I’ve tried different GGUF versions. I’ve also experimented with various workflows with Wan2.1 and Wan2.2 model but the issue occurs with all of them. I'm unsure what's causing it. I will try a different video generation AI (hunyuan video) model now.  I am happy to share anything you need from my side.

```
absl-py==2.3.1
accelerate==1.12.0
addict==2.4.0
aeiou==0.0.21
aenum==3.1.16
aiofiles==24.1.0
aiohappyeyeballs==2.6.1
aiohttp==3.10.11
aiohttp-retry==2.8.3
aiohttp_socks==0.11.0
aioice==0.10.2
aiortc==1.14.0
aiosignal==1.4.0
aiosqlite==0.22.0
aisuite==0.1.14
albucore==0.0.24
albumentations==2.0.8
alembic==1.17.2
alias-free-torch==0.0.6
altair==6.0.0
annotated-doc==0.0.4
annotated-types==0.7.0
anthropic==0.30.1
antlr4-python3-runtime==4.9.3
anyascii==0.3.3
anyio==4.12.0
APScheduler==3.11.1
argbind==0.3.9
arxiv==2.3.1
asttokens==3.0.1
asyncua==1.1.8
attrdict==2.0.1
attrs==25.4.0
audioread==3.1.0
auraloss==0.4.0
av==16.0.1
babel==2.17.0
backoff==2.2.1
banks==2.2.0
beautifulsoup4==4.14.3
bitsandbytes==0.47.0
bleach==6.3.0
blend_modes==2.2.0
blendmodes==2025
blind-watermark==0.4.4
blinker==1.9.0
blis==1.3.3
bokeh==3.8.1
boto3==1.41.5
botocore==1.41.5
braceexpand==0.1.7
brotli==1.2.0
cachetools==5.5.2
catalogue==2.0.10
ccimport==0.4.4
cerebras_cloud_sdk==1.59.0
certifi==2025.11.12
cffi==2.0.0
cfgv==3.5.0
chardet==5.2.0
charset-normalizer==3.4.4
clean-fid==0.1.35
click==8.1.8
clip-anytorch==2.6.0
clip-interrogator==0.6.0
cloudpathlib==0.23.0
cohere==5.20.0
colorama==0.4.6
colorcet==3.1.0
coloredlogs==15.0.1
colour-science==0.4.7
comfyui-embedded-docs==0.3.0
comfyui_frontend_package==1.27.10
comfyui_workflow_templates==0.1.95
confection==0.1.5
configparser==7.2.0
conformer==0.3.2
contourpy==1.3.3
cpm-kernels==1.0.11
cryptography==46.0.3
csvw==3.7.0
cumm==0.7.11
curated-tokenizers==0.0.9
curated-transformers==0.1.1
custom_rasterizer==0.1.0+torch2100dev20251208.rocm7051831
cycler==0.12.1
cymem==2.0.13
Cython==3.0.12
dataclasses-json==0.6.7
dctorch==0.1.2
decorator==5.2.1
decord==0.6.0
deepdiff==8.6.1
deepgram-sdk==5.3.0
defusedxml==0.7.1
Deprecated==1.2.18
descript-audio-codec==1.0.0
descript-audiotools==0.7.2
diffusers==0.36.0
dill==0.3.8
dirtyjson==1.0.8
diskcache==5.6.3
distlib==0.4.0
distro==1.9.0
dlinfo==2.0.0
dnspython==2.8.0
docker==7.1.0
docopt==0.6.2
docstring-parser==0.15
docx2txt==0.9
dotenv==0.9.9
easydict==1.13
easyocr==1.7.2
einops==0.8.0
einops-exts==0.0.4
einx==0.3.0
ema-pytorch==0.7.7
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl#sha256=1932429db727d4bff3deed6b34cfc05df17794f4a52eeb26cf8928f7c1a0fb85
encodec==0.1.1
espeakng-loader==0.2.4
et_xmlfile==2.0.0
eval_type_backport==0.3.1
executing==2.2.1
fairscale==0.4.0
faiss-cpu==1.13.1
fastapi==0.115.14
fastavro==1.12.1
fastcore==1.9.2
feedparser==6.0.12
ffmpeg-python==0.2.0
ffmpy==1.0.0
filelock==3.17.0
filetype==1.2.0
fire==0.7.1
fish-audio-sdk==1.1.0
flatbuffers==25.9.23
flatten-dict==0.4.2
fonttools==4.61.0
fpsample==1.0.1
frozendict==2.4.7
frozenlist==1.8.0
fsspec==2025.12.0
ftfy==6.3.1
future==1.0.0
gdown==5.2.0
gguf==0.17.1
gin-config==0.5.0
gitdb==4.0.12
GitPython==3.1.45
google-ai-generativelanguage==0.6.15
google-api-core==2.28.1
google-api-python-client==2.187.0
google-auth==2.45.0
google-auth-httplib2==0.3.0
google-cloud-aiplatform==1.71.1
google-cloud-bigquery==3.39.0
google-cloud-core==2.5.0
google-cloud-resource-manager==1.15.0
google-cloud-speech==2.34.0
google-cloud-storage==2.19.0
google-crc32c==1.8.0
google-generativeai==0.8.5
google-resumable-media==2.8.0
googleapis-common-protos==1.72.0
gradio==6.1.0
gradio_client==2.0.1
greenlet==3.3.0
griffe==1.15.0
groovy==0.1.2
groq==0.9.0
grpc-google-iam-v1==0.14.3
grpcio==1.76.0
grpcio-status==1.71.2
h11==0.16.0
h2==4.3.0
h5py==3.15.1
hf-xet==1.2.0
hf_transfer==0.1.9
holoviews==1.22.1
hpack==4.1.0
html2image==2.0.7
html5lib==1.1
httpcore==1.0.9
httplib2==0.31.0
httpx==0.27.2
httpx-sse==0.4.0
httpx-ws==0.8.2
huggingface-hub==0.36.0
humanfriendly==10.0
hydra-core==1.3.2
hyper-connections==0.2.1
hyperframe==6.1.0
ibm-cos-sdk==2.14.3
ibm-cos-sdk-core==2.14.3
ibm-cos-sdk-s3transfer==2.14.3
ibm_watsonx_ai==1.4.11
identify==2.6.15
idna==3.11
ifaddr==0.2.0
ImageIO==2.37.2
imageio-ffmpeg==0.6.0
importlib_metadata==8.7.0
importlib_resources==6.5.2
inference-cli==0.62.5
inference-exp==0.17.3
inference-gpu==0.62.5
iniconfig==2.3.0
insightface==0.7.3
iopath==0.1.10
ipython==9.8.0
ipython_pygments_lexers==1.1.1
isodate==0.7.2
jax==0.7.1
jaxlib==0.7.1
jedi==0.19.2
Jinja2==3.1.6
jiter==0.12.0
jmespath==1.0.1
joblib==1.5.2
json_repair==0.54.3
jsonmerge==1.9.2
jsonpatch==1.33
jsonpath-python==1.1.4
jsonpointer==3.0.0
jsonschema==4.25.1
jsonschema-specifications==2025.9.1
julius==0.2.7
k-diffusion==0.1.1.post1
keyboard==0.13.5
kiwisolver==1.4.9
kokoro==0.9.4
kornia==0.8.2
kornia_rs==0.1.10
laion_clap==1.1.7
langchain==1.2.0
langchain-classic==1.0.0
langchain-community==0.4.1
langchain-core==1.2.1
langchain-ollama==1.0.1
langchain-openai==1.1.3
langchain-text-splitters==1.1.0
langdetect==1.0.9
langgraph==1.0.5
langgraph-checkpoint==3.0.1
langgraph-prebuilt==1.0.5
langgraph-sdk==0.3.0
langsmith==0.4.59
language-tags==1.2.0
lark==1.3.1
latex2mathml==3.78.1
lazy_loader==0.4
librosa==0.11.0
lightning==2.6.0
lightning-utilities==0.15.2
linkify-it-py==2.0.3
llama-cloud==0.1.35
llama-cloud-services==0.6.54
llama-index==0.14.10
llama-index-cli==0.5.3
llama-index-core==0.14.10
llama-index-embeddings-openai==0.5.1
llama-index-indices-managed-llama-cloud==0.9.4
llama-index-instrumentation==0.4.2
llama-index-llms-openai==0.6.12
llama-index-readers-file==0.5.5
llama-index-readers-llama-parse==0.5.1
llama-index-workflows==2.11.5
llama-parse==0.6.54
llvmlite==0.46.0
local-attention==1.11.2
loguru==0.7.3
lomond==0.3.3
lxml==6.0.2
Mako==1.3.10
Markdown==3.10
markdown-it-py==4.0.0
markdown2==2.5.4
markdownify==1.2.2
MarkupSafe==3.0.3
marshmallow==3.26.1
matplotlib==3.10.7
matplotlib-inline==0.2.1
matrix-nio==0.25.2
mcp==1.24.0
mdit-py-plugins==0.5.0
mdtex2html==1.3.2
mdurl==0.1.2
mediapipe==0.10.21
meshlib==3.0.9.196
misaki==0.9.4
mistralai==1.5.2
ml_dtypes==0.5.4
more-itertools==10.8.0
moviepy==2.2.1
mpmath==1.3.0
msgpack==1.1.2
multidict==6.7.0
murmurhash==1.0.15
mypy_extensions==1.1.0
narwhals==2.14.0
neo4j==6.0.3
nest-asyncio==1.6.0
networkx==3.6.1
ninja==1.13.0
nltk==3.9.2
nodeenv==1.9.1
num2words==0.5.14
numba==0.63.1
numpy==1.26.4
nvidia-cublas-cu12==12.8.4.1
nvidia-cuda-cupti-cu12==12.8.90
nvidia-cuda-nvrtc-cu12==12.8.93
nvidia-cuda-runtime-cu12==12.8.90
nvidia-cufft-cu12==11.3.3.83
nvidia-cufile-cu12==1.13.1.3
nvidia-curand-cu12==10.3.9.90
nvidia-cusparse-cu12==12.5.8.93
nvidia-cusparselt-cu12==0.7.1
nvidia-ml-py==12.575.51
nvidia-nccl-cu12==2.27.5
nvidia-nvjitlink-cu12==12.8.93
nvidia-nvshmem-cu12==3.3.20
nvidia-nvtx-cu12==12.8.90
ollama==0.6.0
omegaconf==2.3.0
onnx==1.20.0
onnxruntime==1.23.2
onnxruntime-gpu==1.21.1
onvif-zeep-async==2.0.0
open_clip_torch==3.2.0
openai==1.109.1
openai-whisper==20250625
opencv-contrib-python==4.10.0.84
opencv-python==4.10.0.84
opencv-python-headless==4.11.0.86
openpyxl==3.1.5
opt_einsum==3.4.0
optimum==2.0.0
ordered-set==4.1.0
orderly-set==5.5.0
orjson==3.11.5
ormsgpack==1.12.1
outcome==1.3.0.post0
packaging==24.2
paho-mqtt==1.6.1
pandas==2.2.3
panel==1.8.4
param==2.3.1
parso==0.8.5
pccm==0.4.16
pdfminer.six==20251107
pdfplumber==0.11.8
pedalboard==0.9.19
peft==0.17.1
perth==1.0.0
pexpect==4.9.0
phonemizer-fork==3.3.2
piexif==1.1.3
pillow==11.3.0
platformdirs==4.5.1
plotly==6.5.0
pluggy==1.6.0
polars==1.36.1
polars-runtime-32==1.36.1
pooch==1.8.2
portalocker==3.2.0
pre_commit==4.5.0
prefigure==0.0.10
preshed==3.0.12
prettytable==3.17.0
proglog==0.1.12
progressbar==2.5
prometheus-fastapi-instrumentator==6.0.0
prometheus_client==0.23.1
prompt_toolkit==3.0.52
propcache==0.4.1
proto-plus==1.27.0
protobuf==6.33.2
psd-tools==1.12.1
psutil==7.1.3
ptyprocess==0.7.0
pure_eval==0.2.3
py-cord==2.6.1
py-cpuinfo==9.0.0
pyarrow==22.0.0
pyasn1==0.6.1
pyasn1_modules==0.4.2
pybase64==1.0.2
pybind11==3.0.1
pyclipper==1.4.0
pycocotools==2.0.11
pycparser==2.23
pycryptodome==3.23.0
pydantic==2.11.10
pydantic-settings==2.12.0
pydantic_core==2.33.2
pydeck==0.9.1
pydot==2.0.0
pydub==0.25.1
pyee==13.0.0
PyGithub==2.8.1
pygltflib==1.16.5
Pygments==2.19.2
PyJWT==2.10.1
pylibsrtp==1.0.0
pylogix==1.0.5
pyloudnorm==0.1.1
PyMatting==1.1.14
pymeshlab==2023.12.post3
pymodbus==3.8.3
PyNaCl==1.5.0
pynndescent==0.5.13
pynvml==13.0.1
pyopenjtalk==0.4.1
pyOpenSSL==25.3.0
pyparsing==3.2.5
pypdf==6.4.2
pypdfium2==4.30.0
PySocks==1.7.1
pystoi==0.4.1
pytest==8.4.2
pytest-timeout==2.4.0
python-bidi==0.6.7
python-dateutil==2.9.0.post0
python-doctr==0.11.0
python-dotenv==1.0.1
python-multipart==0.0.20
python-socks==2.8.0
pytorch-lightning==2.6.0
pytorch-triton-rocm==3.6.0+git5261b273
pytz==2025.2
pyvips==2.2.3
pyviz_comms==3.0.6
PyWavelets==1.9.0
PyYAML==6.0.3
pyzbar==0.1.9
qrcode==8.0
qwen-vl-utils==0.0.14
randomname==0.2.1
RapidFuzz==3.14.3
rdflib==7.5.0
redis==5.0.8
referencing==0.37.0
regex==2025.11.3
rembg==2.0.69
requests==2.32.5
requests-file==3.0.1
requests-toolbelt==1.0.0
resampy==0.4.3
resemble-perth==1.0.1
rf-clip==1.1
rf_groundingdino==0.3.0
rfc3986==1.5.0
rich==14.2.0
rotary-embedding-torch==0.8.9
rpds-py==0.30.0
rsa==4.9.1
s3tokenizer==0.2.0
s3transfer==0.15.0
safehttpx==0.1.7
safetensors==0.7.0
sageattention==1.0.6
SAM-2 @ git+https://github.com/facebookresearch/sam2@2b90b9f5ceec907a1c18123530e92e794ad901a4
scikit-image==0.25.2
scikit-learn==1.8.0
scipy==1.16.3
seaborn==0.13.2
segment-anything==1.0
segmentation_models_pytorch==0.5.0
segments==2.3.0
selenium==4.39.0
semantic-version==2.10.0
sentence-transformers==5.2.0
sentencepiece==0.2.1
sentry-sdk==2.48.0
setuptools==80.9.0
sgmllib3k==1.0.0
shapely==2.0.7
shellingham==1.5.4
simple-pid==2.0.1
simsimd==6.5.3
six==1.17.0
slack_sdk==3.33.5
smart_open==7.5.0
smmap==5.0.2
sniffio==1.3.1
sortedcontainers==2.4.0
sounddevice==0.5.3
soundfile==0.12.1
soupsieve==2.8
soxr==1.0.0
spacy==3.8.11
spacy-curated-transformers==0.3.1
spacy-legacy==3.0.12
spacy-loggers==1.0.5
spandrel==0.4.1
spconv==2.3.8
SQLAlchemy==2.0.45
srsly==2.5.2
srt==3.5.3
sse-starlette==3.0.4
stack-data==0.6.3
starlette==0.46.2
streamlit==1.52.1
stringzilla==4.4.0
striprtf==0.0.26
structlog==24.4.0
supervision==0.27.0
sympy==1.14.0
tabulate==0.9.0
tenacity==9.1.2
tensorboard==2.20.0
tensorboard-data-server==0.7.2
termcolor==3.2.0
thinc==8.3.10
threadpoolctl==3.6.0
tifffile==2025.10.16
tiktoken==0.12.0
timm==1.0.22
tldextract==5.1.3
tokenizers==0.22.1
toml==0.10.2
tomlkit==0.13.3
torch==2.10.0.dev20251208+rocm7.0
torch-stoi==0.2.3
torchaudio==2.10.0.dev20251210+rocm7.0
torchdiffeq==0.2.5
torchlibrosa==0.1.0
torchmetrics==1.8.2
torchscale==0.3.0
torchsde==0.2.6
torchvision==0.25.0.dev20251210+rocm7.0
tornado==6.5.4
tqdm==4.67.1
traitlets==5.14.3
trampoline==0.1.2
transformers==4.57.3
transformers-stream-generator==0.0.5
transparent-background==1.3.4
trimesh==4.10.1
trio==0.32.0
trio-websocket==0.12.2
triton==3.5.1
twilio==9.3.8
typer==0.16.0
typer-config==1.4.3
typer-slim==0.20.1
types-requests==2.32.4.20250913
typing-inspect==0.9.0
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2025.2
tzlocal==5.3.1
uc-micro-py==1.0.3
ultralytics==8.3.40
ultralytics-thop==2.0.18
umap-learn==0.5.9.post2
unpaddedbase64==2.1.0
uritemplate==4.2.0
urllib3==2.6.1
uuid==1.30
uuid_utils==0.12.0
uv==0.9.17
uvicorn==0.38.0
v-diffusion-pytorch==0.0.2
vector-quantize-pytorch==1.27.15
verovio==5.7.0
vertexai==1.71.1
virtualenv==20.35.4
wandb==0.23.1
wasabi==1.1.3
watchdog==6.0.0
wcwidth==0.2.14
weasel==0.4.3
webdataset==1.0.2
webencodings==0.5.1
websocket-client==1.9.0
websockets==15.0.1
Werkzeug==3.1.4
wget==3.2
wheel==0.45.1
wikipedia==1.4.0
wrapt==1.17.3
wsproto==1.3.2
x-transformers==2.11.24
xatlas==0.0.11
xlrd==2.0.2
xxhash==3.6.0
xyzservices==2025.11.0
yapf==0.43.0
yarl==1.22.0
zeep==4.3.2
zipp==3.23.0
zstandard==0.25.0
zxing-cpp==2.2.0
```



```
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
[MultiGPU Core Patching] text_encoder_device_patched returning device: cuda:0 (current_text_encoder_device=cuda:0)
FETCH ComfyRegistry Data: 60/117
Requested to load CLIPVisionModelProjection
loaded completely; 15002.80 MB usable, 1208.10 MB loaded, full load: True
FETCH ComfyRegistry Data: 65/117
FETCH ComfyRegistry Data: 70/117
gguf qtypes: Q3_K (168), F32 (73), Q6_K (1)
Attempting to recreate sentencepiece tokenizer from GGUF file metadata...
FETCH ComfyRegistry Data: 75/117
/run/host/run/media/system/Depolama/ComfyUI/custom_nodes/ComfyUI-GGUF/loader.py:36: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return field_type(field.parts[field.data[-1]])
Created tokenizer with vocab size of 256384
Dequantizing token_embd.weight to prevent runtime OOM.
FETCH ComfyRegistry Data: 80/117
[MultiGPU Core Patching] text_encoder_device_patched returning device: cuda:0 (current_text_encoder_device=cuda:0)
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cpu, dtype: torch.float16
Requested to load WanTEModel
FETCH ComfyRegistry Data: 85/117
loaded completely; 13458.63 MB usable, 3901.45 MB loaded, full load: True
FETCH ComfyRegistry Data: 90/117
gguf qtypes: F16 (694), Q2_K (320), Q3_K (80), F32 (1)
model weight dtype torch.float16, manual cast: None
model_type FLOW
Requested to load WanTEModel
loaded completely; 13338.13 MB usable, 3901.45 MB loaded, full load: True
FETCH ComfyRegistry Data: 95/117
Requested to load WanVAE
loaded completely; 5613.68 MB usable, 242.03 MB loaded, full load: True
Warning: Ran out of memory when regular VAE encoding, retrying with tiled VAE encoding.
FETCH ComfyRegistry Data: 100/117
FETCH ComfyRegistry Data: 105/117
FETCH ComfyRegistry Data: 110/117
FETCH ComfyRegistry Data: 115/117
FETCH ComfyRegistry Data [DONE]
[ComfyUI-Manager] default cache updated: https://api.comfy.org/nodes
FETCH DATA from: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json [DONE]
[ComfyUI-Manager] All startup tasks have been completed.
/usr/lib/python3.12/asyncio/selector_events.py:879: ResourceWarning: unclosed transport <_SelectorSocketTransport fd=18>
  _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
Requested to load WAN21
0 models unloaded.
loaded completely; 6261.60 MB usable, 5187.97 MB loaded, full load: True
  0%|                                                                                    | 0/2 [00:00<?, ?it/s][MultiGPU_Memory_Management] Triggering PromptExecutor cache reset. Reason: forced_soft_empty
out of memory error, emptying cache and trying again
[MultiGPU_Memory_Management] Triggering PromptExecutor cache reset. Reason: forced_soft_empty
  0%|                                                                                    | 0/2 [00:01<?, ?it/s]
!!! Exception during processing !!! HIP out of memory. Tried to allocate 83.07 GiB. GPU 0 has a total capacity of 15.92 GiB of which 5.83 GiB is free. Of the allocated memory 8.36 GiB is allocated by PyTorch, and 1.02 GiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
Traceback (most recent call last):
  File "/run/host/run/media/system/Depolama/ComfyUI/execution.py", line 515, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/execution.py", line 329, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/execution.py", line 303, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/run/host/run/media/system/Depolama/ComfyUI/execution.py", line 291, in process_inputs
    result = f(**inputs)
             ^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/nodes.py", line 1572, in sample
    return common_ksampler(model, noise_seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise, disable_noise=disable_noise, start_step=start_at_step, last_step=end_at_step, force_full_denoise=force_full_denoise)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/nodes.py", line 1505, in common_ksampler
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/sample.py", line 60, in sample
    samples = sampler.sample(noise, positive, negative, cfg=cfg, latent_image=latent_image, start_step=start_step, last_step=last_step, force_full_denoise=force_full_denoise, denoise_mask=noise_mask, sigmas=sigmas, callback=callback, disable_pbar=disable_pbar, seed=seed)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 1163, in sample
    return sample(self.model, noise, positive, negative, cfg, self.device, sampler, sigmas, self.model_options, latent_image=latent_image, denoise_mask=denoise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 1053, in sample
    return cfg_guider.sample(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 1035, in sample
    output = executor.execute(noise, latent_image, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 997, in outer_sample
    output = self.inner_sample(noise, latent_image, device, sampler, sigmas, denoise_mask, callback, disable_pbar, seed, latent_shapes=latent_shapes)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 980, in inner_sample
    samples = executor.execute(self, sigmas, extra_args, callback, noise, latent_image, denoise_mask, disable_pbar)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 752, in sample
    samples = self.sampler_function(model_k, noise, sigmas, extra_args=extra_args, callback=k_callback, disable=disable_pbar, **self.extra_options)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/venv/lib/python3.12/site-packages/torch/utils/_contextlib.py", line 124, in decorate_context
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/k_diffusion/sampling.py", line 199, in sample_euler
    denoised = model(x, sigma_hat * s_in, **extra_args)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 401, in __call__
    out = self.inner_model(x, sigma, model_options=model_options, seed=seed)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 953, in __call__
    return self.outer_predict_noise(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 960, in outer_predict_noise
    ).execute(x, timestep, model_options, seed)
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 963, in predict_noise
    return sampling_function(self.inner_model, x, timestep, self.conds.get("negative", None), self.conds.get("positive", None), self.cfg, model_options=model_options, seed=seed)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 381, in sampling_function
    out = calc_cond_batch(model, conds, x, timestep, model_options)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 206, in calc_cond_batch
    return _calc_cond_batch_outer(model, conds, x_in, timestep, model_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 214, in _calc_cond_batch_outer
    return executor.execute(model, conds, x_in, timestep, model_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/samplers.py", line 326, in _calc_cond_batch
    output = model.apply_model(input_x, timestep_, **c).chunk(batch_chunks)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/model_base.py", line 162, in apply_model
    return comfy.patcher_extension.WrapperExecutor.new_class_executor(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/model_base.py", line 204, in _apply_model
    model_output = self.diffusion_model(xc, t, context=context, control=control, transformer_options=transformer_options, **extra_conds)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1776, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1787, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/ldm/wan/model.py", line 627, in forward
    return comfy.patcher_extension.WrapperExecutor.new_class_executor(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/patcher_extension.py", line 112, in execute
    return self.original(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/ldm/wan/model.py", line 647, in _forward
    return self.forward_orig(x, timestep, context, clip_fea=clip_fea, freqs=freqs, transformer_options=transformer_options, **kwargs)[:, :, :t, :h, :w]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/ldm/wan/model.py", line 580, in forward_orig
    x = block(x, e=e0, freqs=freqs, context=context, context_img_len=context_img_len, transformer_options=transformer_options)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1776, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1787, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/ldm/wan/model.py", line 236, in forward
    y = self.self_attn(
        ^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1776, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1787, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/ldm/wan/model.py", line 81, in forward
    x = optimized_attention(
        ^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/ldm/modules/attention.py", line 130, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/ldm/modules/attention.py", line 377, in attention_split
    raise e
  File "/run/host/run/media/system/Depolama/ComfyUI/comfy/ldm/modules/attention.py", line 350, in attention_split
    s1 = einsum('b i d, b j d -> b i j', q[:, i:end], k) * scale
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/run/host/run/media/system/Depolama/ComfyUI/venv/lib/python3.12/site-packages/torch/functional.py", line 373, in einsum
    return _VF.einsum(equation, operands)  # type: ignore[attr-defined]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 83.07 GiB. GPU 0 has a total capacity of 15.92 GiB of which 5.83 GiB is free. Of the allocated memory 8.36 GiB is allocated by PyTorch, and 1.02 GiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)

Got an OOM, unloading all loaded models.
Prompt executed in 80.17 seconds
```

---

### 评论 #7 — TawusGames (2026-01-04T10:01:45Z)

I tried to generate videos using the hunyuanvideo1.5_480p_i2v-Q4_K_M.gguf model. Unfortunately, it was trying to allocate 24GB of VRAM even for a 480x480 video. I did some experimenting, but couldn't generate even a single video. When I tried 848x480, it attempted to allocate 85GB of VRAM. It seems like there might be an issue with my ComfyUI setup. I'm going to do a fresh install of ComfyUI and see if the same problem occurs.

---

### 评论 #8 — TawusGames (2026-01-04T11:15:09Z)

I found the source of the problem. I was starting Envermiont like this: `python3 main.py --use-split-cross-attention`

Removing the `--use-split-cross-attention` parameter now allows me to generate videos without any issues.

I apologize for bothering you with this.

---
