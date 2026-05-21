# [Issue]: ComfyUI crashing under Arch Linux kernel 6.18 with ROCm 7.12

> **Issue #5990**
> **状态**: open
> **创建时间**: 2026-02-24T00:25:57Z
> **更新时间**: 2026-04-18T22:39:32Z
> **作者**: jab416171
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5990

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

Using the latest available nightly from https://rocm.nightlies.amd.com/v2-staging/gfx120X-all/ (currently that is `torch==2.11.0a0+rocm7.12.0a20260211`) and kernel 6.18 (currently on 6.18.9) I consistently get a crash when running an image workload through comfyui:

```
Memory access fault by GPU node-1 (Agent handle: 0x21df3df0) on address 0x7fac37a5f000. Reason: Page not present or supervisor privilege.
Failed to write segment data to pipe: Broken pipe
GPU coredump: handler exited with error (status: 1)
GPU core dump failed
```

I do not have any crashes on 6.17.9. I do have the following set in my cmdline, the cwsr flag was added to prevent another crash I was having before 6.18: `acpi_enforce_resources=lax split_lock_detect=off amdgpu.cwsr_enable=0`

dmesg output is below:
[dmesg_amd_crash.txt](https://github.com/user-attachments/files/25503326/dmesg_amd_crash.txt)

### Operating System

Arch Linux

### CPU

AMD Ryzen 9 5950X 16-Core Processor

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

7.12

### ROCm Component

_No response_

### Steps to Reproduce

I have been able to reliably reproduce the crash by running this workflow in comfyui: https://github.com/Comfy-Org/workflow_templates/blob/main/templates/templates-1_click_multiple_character_angles-v1.0.json
this workflow uses the qwen image edit 2509 model with the lightning 4 step and multiple angle loras with 8 different prompts.
if it doesn't crash on the first run, changing the image and/or doing a second run is usually enough to trigger a crash.
I have set the following environment variables:
    "HIP_LAUNCH_BLOCKING": "1",
    "TORCH_SHOW_CPP_STACKTRACES": "1",
    "HSA_ENABLE_COREDUMP": "0",
    "HSA_ENABLE_SDMA": "0",
    "HSA_ENABLE_PEER_SDMA": "0"

I only started seeing a full GPU reset after adding the last two. without them I get the memory access fault, and then the python process dies about a minute after that. Here is dmesg output from that setup:

[dmesg_amd_crash_noreset.txt](https://github.com/user-attachments/files/25503426/dmesg_amd_crash_noreset.txt)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.15
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
  Name:                    AMD Ryzen 9 5950X 16-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 9 5950X 16-Core Processor
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
  Max Clock Freq. (MHz):   5086
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
      Size:                    131809364(0x7db4054) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131809364(0x7db4054) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131809364(0x7db4054) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    131809364(0x7db4054) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1201
  Uuid:                    GPU-b901b9604e042be8
  Marketing Name:          AMD Radeon RX 9070 XT
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
    L2:                      8192(0x2000) KB
    L3:                      65536(0x10000) KB
  Chip ID:                 30032(0x7550)
  ASIC Revision:           1(0x1)
  Cacheline Size:          256(0x100)
  Max Clock Freq. (MHz):   2460
  BDFID:                   3328
  Internal Node ID:        1
  Compute Unit:            64
  SIMDs per CU:            2
  Shader Engines:          4
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
    x                        2147483647(0x7fffffff)
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 128
  SDMA engine uCode::      662
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16695296(0xfec000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1201
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic
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

### Additional Information

Full output from pip freeze

```
absl-py==2.4.0
acme==5.3.1
adal==1.2.7
aiohappyeyeballs==2.6.1
aiohttp==3.13.3
aiohttp_socks==0.11.0
aiorpcX==0.25.0
aiosignal==1.4.0
alabaster==1.0.0
ansible==13.3.0
ansible-core==2.20.2
appdirs==1.4.4
arandr==0.1.11
argcomplete==3.6.2
astor==0.8.1
astunparse==1.6.3
attrs==25.4.0
aurman==2.22
autocommand==2.2.2
babel==2.17.0
bcrypt==5.0.0
Beaker==1.13.0
beautifulsoup4==4.14.3
binaryornot==0.4.4
bleach==6.3.0
blessed==1.25.0
bluepy==1.3.0
boolean.py==5.0
bpython==0.26
breathe==5.0.0a5
breezy==3.3.21
btrfsutil==6.19
build==1.4.0
cachetools==7.0.1
cbor2==5.8.0
certbot==5.3.1
certbot-dns-cloudflare==5.3.1
certifi==2026.1.4
cffi==2.0.0
chardet==5.2.0
charset-normalizer==3.4.4
cli_helpers==2.10.1
click==8.3.1
cloudflare==2.15.0
colorama==0.4.6
colorlog==6.9.0
ConfigArgParse==1.7.1
configobj==5.0.9
contourpy==1.3.3
coverage==7.13.4
crcmod==1.7
cryptography==46.0.5
curtsies==0.4.3
cwcwidth==0.1.12
cycler==0.12.1
daemonize==2.5.0
dbus-python==1.4.0
dirty-equals==0.11
distlib==0.4.0
distro==1.9.0
dnspython==2.8.0
docopt==0.6.2
docutils==0.22.3
dulwich==0.25.2
durationpy==0.10
editables==0.5
Electrum==4.7.0
electrum-aionostr==0.1.0
electrum-ecc==0.0.6
entrypoints==0.4
evdev==1.9.3
fastbencode==0.3.9
fastjsonschema==2.21.2
feedparser==6.0.12
fido2==2.1.1
filelock==3.24.0
flake8==7.3.0
flatbuffers==25.12.19
fluidity-sm==0.2.1
fonttools==4.61.1
frozenlist==1.8.0
fsspec==2026.2.0
gallery_dl==1.31.6
gast==0.7.0
gmpy2==2.3.0
google-auth==2.48.0
google-auth-oauthlib==1.2.4
google-pasta==0.2.0
gps==3.27.5
greenlet==3.3.2
grpcio==1.76.0
grpcio-tools==1.76.0
h5py==3.15.1
hatch-fancy-pypi-readme==25.1.0
hatch-vcs==0.5.0
hatchling==1.28.0
hidapi==0.14.0
html5lib==1.1
httplib2==0.31.2
idna==3.11
imagesize==1.4.1
inflect==7.5.0
iniconfig==2.1.0
installer==0.7.0
invoke==2.2.1
iotop==0.6
jaraco.classes==3.4.0
jaraco.collections==5.1.0
jaraco.context==6.0.1
jaraco.functools==4.1.0
jaraco.text==4.0.0
jeepney==0.9.0
Jinja2==3.1.6
josepy==2.2.0
jsonlines==4.0.0
jsonpatch==1.33
jsonpointer==3.0.0
keras==3.13.2
keyring==25.7.0
kiwisolver==1.4.7
kubernetes==35.0.0
lark==1.3.1
lensfun==0.3.4
lexicon==3.0.0
libfdt==1.7.2
libtorrent==2.0.11
libvirt-python==12.0.0
license-expression==30.4.4
liquidctl==1.15.0
lit==21.1.8.dev0
louis==3.36.0
lxml==6.0.2
Mako==1.3.10.dev0
Markdown==3.10.2
markdown-it-py==4.0.0
MarkupSafe==3.0.2
matplotlib==3.10.8
mccabe==0.7.0
mdurl==0.1.2
mercurial==7.2
merge3==0.0.16
meson==1.10.1
ml_dtypes==0.5.4
moddb==0.14.0
more-itertools==10.8.0
mpmath==1.3.0
multidict==6.7.1
netsnmp-python==1.0a1
networkx==3.6.1
nftables==0.1
nlopt==2.10.1
nose==1.3.7
numpy==2.4.2
nvchecker==2.20
oauth2client==4.1.3
oauthlib==3.3.1
openrazer==3.11.0
openrazer_daemon==3.11.0
opt_einsum==3.4.0
optree==0.18.0
ordered-set==4.1.0
packaging==26.0
pandas==2.3.3
paramiko==4.0.0
parsedatetime==2.6
pathspec==1.0.4
patiencediff==0.2.18
pendulum==3.2.0
pgcli==4.4.0
pgspecial==2.2.1
pillow==12.1.1
pipx==1.8.0
pkg_resources==81.0.0
platformdirs==4.9.2
pluggy==1.6.0
ply==3.11
poetry-core==2.3.1
pooch==1.9.0
prettytable==3.17.0
prompt_toolkit==3.0.52
propcache==0.4.1
protobuf==6.33.1
protontricks==1.13.1
psutil==7.2.2
psycopg==3.3.3
psycopg-c==3.3.3
pwquality==1.4.5
py3status==3.63
pyaes==1.6.1
pyalpm==0.11.1
pyaml==24.12.0
pyasn1==0.6.1
pyasn1_modules==0.4.2
pybind11==3.0.2
pycairo==1.29.0
pycodestyle==2.14.0
pycparser==2.23
pycurl==7.45.7
pydot==3.0.4
pyelftools==0.32
pyflakes==3.4.0
Pygments==2.19.2
PyGObject==3.54.5
PyJWT==2.11.0
PyNaCl==1.6.2
pyOpenSSL==25.3.0
pyparsing==3.3.2
pyproject_hooks==1.2.0
PyQt6==6.10.2
PyQt6_sip==13.11.0
pyrate-limiter==4.0.2
pyRFC3339==1.1
pyscard==2.3.1
pytest==8.4.2
pytest-asyncio==1.3.0
pytest-cov==6.1.1
python-dateutil==2.9.0
python-debian==1.0.1
python-distutils-extra==2.39
python-multipart==0.0.22
python-pskc==1.4
python-socks==2.8.0
python-xlib==0.33
pytz==2025.2
pyudev==0.24.4
pyusb==1.3.1
pyxdg==0.28
PyYAML==6.0.3
pyzstd==0.19.1
qrcode==8.2
ranger-fm==1.9.4
Reflector==2023.6.28.0.36.1
regex==2026.2.19
requests==2.32.5
requests-oauthlib==2.0.0
resolvelib==1.2.1
reuse==6.2.0
rich==14.3.3
roman-numerals-py==3.1.0
rrdtool==0.1.10
rsa==4.9.1
scipy==1.17.1
SecretStorage==3.3.3
setproctitle==1.3.7
setuptools==82.0.0
setuptools-scm==9.2.2
sgmllib3k==1.0.0
six==1.17.0
smbus==1.1
sniffio==1.3.1
snowballstemmer==2.2.0
soupsieve==2.8.3
Sphinx==8.2.3
sphinx_rtd_theme==2.0.0
sphinxcontrib-applehelp==2.0.0
sphinxcontrib-devhelp==2.0.0
sphinxcontrib-htmlhelp==2.1.0
sphinxcontrib-jquery==4.1
sphinxcontrib-jsmath==1.0.1
sphinxcontrib-qthelp==2.0.0
sphinxcontrib-serializinghtml==2.0.0
sqlparse==0.5.3
standard-cgi==3.13.0
structlog==25.5.0
sympy==1.14.0
tabulate==0.9.0
TBB==0.2
tensorboard==2.20.0
tensorboard_data_server==0.8.0a0
tensorboard_plugin_wit==1.8.1
tensorflow_cpu==2.20.0.dev0+selfbuilt
termcolor==3.3.0
time-machine==3.2.0
tomli==2.4.0
tomlkit==0.14.0
toolz==1.1.0
torch==2.10.0
torchvision==0.25.0+c94b960
tornado==6.5.2
tqdm==4.67.3
triton==3.5.1+git0add6826
trove-classifiers==2026.1.14.14
typeguard==4.4.4
typing_extensions==4.15.0
tzdata==2025.3
tzlocal==5.3.1
uc-micro-py==1.0.3
umu-launcher==1.3.0
urllib3==2.6.3
userpath==1.9.2
uv==0.10.4
validate==5.0.9
validate-pyproject==0.25
vdf==4.0
virtualenv==20.36.1
wcwidth==0.6.0
webencodings==0.5.1
websocket-client==1.9.0
Werkzeug==3.1.3
wheel==0.46.3
wrapt==1.17.3
wxPython==4.2.4
xmltodict==1.0.4
xxhash==3.6.0
yarl==1.23.0
yq==3.4.3
yt-dlp==2026.2.21
yt-dlp-ejs==0.5.0
yubikey-manager==5.9.0
joe-r9% pwd
/mnt/games/sm/data
joe-r9% cd /mnt/games/sm/data/Packages/ComfyUI-green
joe-r9% source venv/bin/activate
(venv) joe-r9% pip freeze
aiohappyeyeballs==2.6.1
aiohttp==3.13.3
aiosignal==1.4.0
alembic==1.18.4
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.12.1
attrs==25.4.0
av==16.1.0
certifi==2026.1.4
cffi==2.0.0
chardet==6.0.0.post1
charset-normalizer==3.4.4
click==8.3.1
comfy-aimdo==0.2.0
comfy-kitchen==0.2.7
comfyui-embedded-docs==0.4.1
comfyui-manager==4.1b1
comfyui-workflow-templates-core==0.3.145
comfyui-workflow-templates-media-api==0.3.53
comfyui-workflow-templates-media-image==0.3.90
comfyui-workflow-templates-media-other==0.3.121
comfyui-workflow-templates-media-video==0.3.49
comfyui_frontend_package==1.38.14
comfyui_workflow_templates==0.8.43
cryptography==46.0.5
cuda-bindings==12.9.4
cuda-pathfinder==1.3.5
einops==0.8.2
filelock==3.24.2
frozenlist==1.8.0
fsspec==2026.2.0
gitdb==4.0.12
GitPython==3.1.46
greenlet==3.3.2
h11==0.16.0
hf-xet==1.2.0
httpcore==1.0.9
httpx==0.28.1
huggingface_hub==1.4.1
idna==3.11
Jinja2==3.1.6
kornia==0.8.2
kornia_rs==0.1.10
Mako==1.3.10
markdown-it-py==4.0.0
MarkupSafe==3.0.3
mdurl==0.1.2
mpmath==1.3.0
multidict==6.7.1
networkx==3.6.1
numpy==2.4.2
nvidia-cublas-cu12==12.8.4.1
nvidia-cuda-cupti-cu12==12.8.90
nvidia-cuda-nvrtc-cu12==12.8.93
nvidia-cuda-runtime-cu12==12.8.90
nvidia-cudnn-cu12==9.10.2.21
nvidia-cufft-cu12==11.3.3.83
nvidia-cufile-cu12==1.13.1.3
nvidia-curand-cu12==10.3.9.90
nvidia-cusolver-cu12==11.7.3.90
nvidia-cusparse-cu12==12.5.8.93
nvidia-cusparselt-cu12==0.7.1
nvidia-nccl-cu12==2.27.5
nvidia-nvjitlink-cu12==12.8.93
nvidia-nvshmem-cu12==3.4.5
nvidia-nvtx-cu12==12.8.90
packaging==26.0
pillow==12.1.1
propcache==0.4.1
psutil==7.2.2
pycparser==3.0
pydantic==2.12.5
pydantic-settings==2.13.1
pydantic_core==2.41.5
PyGithub==2.8.1
Pygments==2.19.2
PyJWT==2.11.0
PyNaCl==1.6.2
python-dotenv==1.2.1
PyYAML==6.0.3
regex==2026.2.19
requests==2.32.5
rich==14.3.3
rocm==7.12.0a20260211
rocm-sdk-core==7.12.0a20260211
rocm-sdk-libraries-gfx120X-all==7.12.0a20260211
safetensors==0.7.0
scipy==1.17.1
sentencepiece==0.2.1
setuptools==80.9.0
shellingham==1.5.4
smmap==5.0.2
spandrel==0.4.2
SQLAlchemy==2.0.46
sympy==1.14.0
tokenizers==0.22.2
toml==0.10.2
torch==2.11.0a0+rocm7.12.0a20260211
torchaudio==2.11.0a0+rocm7.12.0a20260211
torchsde==0.2.6
torchvision==0.26.0a0+rocm7.12.0a20260211
tqdm==4.67.3
trampoline==0.1.2
transformers==5.2.0
triton==3.6.0+git85db5b6d.rocm7.12.0a20260211
triton-rocm==3.6.0
typer==0.24.1
typer-slim==0.24.0
typing-inspection==0.4.2
typing_extensions==4.15.0
urllib3==2.6.3
uv==0.10.4
wheel==0.46.3
yarl==1.22.0
```

---

## 评论 (12 条)

### 评论 #1 — chejh-amd (2026-02-24T08:52:27Z)

Hi @jab416171 , Thanks a lot for the very detailed report. This appears to be a kernel‑6.18‑specific regression in the ROCm/amdgpu stack, since the same workflow runs correctly on 6.17.9 but triggers GPU page‑fault crashes on 6.18, indicating a low‑level driver/VM bug rather than an application issue.
To help narrow this down, you can try the following tests:
1. Run a simple HIP sample (vector_add or any ROCm sample) on kernel 6.18 to confirm whether the fault occurs outside ComfyUI/PyTorch.
2. Temporarily remove `amdgpu.cwsr_enable=0` from kernel cmdline and test again
3. Re-run the workflow with all HSA_* variables unset (default ROCm runtime settings).
4. Test with SDMA enabled vs disabled to see if the failure mode changes.
These tests will help determine whether this is a kernel‑6.18 regression, a runtime VM bug, or SDMA/CWSR interaction on gfx120X hardware.

---

### 评论 #2 — jab416171 (2026-02-25T02:59:50Z)

Hello @Michelle-HCJ thank you for your response. I hope we can narrow this down.
1. I ran [this script](https://gist.github.com/jab416171/99e1fae358c7cfe5d1cd97e8e49f9db1) and had zero issues. I also bumped up the numElements to 5000000 and it still ran fine. if there's another script you'd like me to run please let me know.
2. I re-ran without `amdgpu.cwsr_enable=0` or any environment variables, and still experienced crashing.
3. same as 2.
4. I also experienced crashing when setting `HSA_ENABLE_SDMA=1`.
No combination of settings or variables seems to avoid crashes as long as I am on the 6.18 kernel.

---

### 评论 #3 — chejh-amd (2026-02-25T08:10:19Z)

Hi @jab416171 Thank you for running all these tests. Could you please provide the full dmesg log so the developers can investigate this further?

---

### 评论 #4 — tcgu-amd (2026-02-25T17:46:54Z)

Hi @jab416171, thanks for reaching out! I tested your comfyUI workflow without any env var or kernel parameters, on Ubuntu24.04 with kernel 6.18 and both 2.9.1+rocm7.12.0a20260211 and 2.9.1+rocm7.12.0a20260225. Both seem to reveal no problems and were able to generate the results properly. Perhaps this is more of an Arch Linux specific problem? 

---

### 评论 #5 — jab416171 (2026-02-26T02:50:04Z)

@Michelle-HCJ here are updated dmesg logs from these tests.

[dmesg_amd_crash_1771987442.txt](https://github.com/user-attachments/files/25562672/dmesg_amd_crash_1771987442.txt)
[dmesg_amd_crash_1771988057.txt](https://github.com/user-attachments/files/25562671/dmesg_amd_crash_1771988057.txt)



@tcgu-amd are you on a 9070 XT or a different GPU? arch does include a few patches in their kernel, you can see those patches [here](https://github.com/archlinux/linux/releases/tag/v6.18.9-arch1). also it looks like they just cut 6.18.13 which doesn't seem to have any extra amd-related patches compared to 6.18.9, but it's still in the testing repo.

---

### 评论 #6 — tcgu-amd (2026-02-27T17:26:56Z)

Hi @jab416171 Yes, I am using 9070XT, the setup should be identical to your case except for the OS. I suggest perhaps bringing this issue to the Arch side as well if the custom patches are suspected to be the potential culprit. Thanks! 

---

### 评论 #7 — jab416171 (2026-02-27T23:56:10Z)

@tcgu-amd I just tested a stock 6.18.9 kernel with no patches from archlinux, no env vars, and without the cwsr_enable cmdline, and it still crashes. here's that dmesg.

[dmesg_amd_crash_1772236407.txt](https://github.com/user-attachments/files/25617015/dmesg_amd_crash_1772236407.txt)

---

### 评论 #8 — Cholerix (2026-02-28T23:33:24Z)

I'm running into the same issue using CachyOS, an arch-based distro.

I used the z-image turbo text-to-image workflow included in ComfyUI. The first run works fine but when I change the query, I get a crash every single time\*:
```
Memory access fault by GPU node-1 (Agent handle: 0x563f6f3b7420) on address 0x7f88b5c01000. Reason: Page not present or supervisor privilege.
GPU core dump created: gpucore.7155
```
The query is very simple, just 10 words. Generating multiple images from the same query is usually no problem.

I somehow can't upload files so here is my dmesg output. It's the same for all kernel or rocm versions.

<details>
<summary>dmesg-2.9.1+rocm7.2.0.git7e1940d4+Linux 6.18.13-2-cachyos-lts</summary>

[  955.602793] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32791)

[  955.602797] amdgpu 0000:09:00.0: amdgpu:  Process python pid 7620 thread python pid 7620

[  955.602799] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00007f3555c00000 from client 10

[  955.602802] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801D3B

[  955.602803] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA1 (0xe)

[  955.602805] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x1

[  955.602806] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x5

[  955.602807] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x3

[  955.602808] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x1

[  955.602810] amdgpu 0000:09:00.0: amdgpu:      RW: 0x0

[  955.602822] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32791)

[  955.602824] amdgpu 0000:09:00.0: amdgpu:  Process python pid 7620 thread python pid 7620

[  955.602826] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00007f3555c00000 from client 10

[  955.602827] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801D3B

[  955.602829] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA1 (0xe)

[  955.602830] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x1

[  955.602831] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x5

[  955.602832] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x3

[  955.602833] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x1

[  955.602834] amdgpu 0000:09:00.0: amdgpu:      RW: 0x0

[  955.602846] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32791)

[  955.602847] amdgpu 0000:09:00.0: amdgpu:  Process python pid 7620 thread python pid 7620

[  955.602849] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00007f3555c00000 from client 10

[  955.602850] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801D3B

[  955.602851] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA1 (0xe)

[  955.602852] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x1

[  955.602853] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x5

[  955.602855] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x3

[  955.602856] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x1

[  955.602857] amdgpu 0000:09:00.0: amdgpu:      RW: 0x0

[  955.602868] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32791)

[  955.602870] amdgpu 0000:09:00.0: amdgpu:  Process python pid 7620 thread python pid 7620

[  955.602871] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00007f3555c00000 from client 10

[  955.602872] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801D3B

[  955.602873] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA1 (0xe)

[  955.602875] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x1

[  955.602876] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x5

[  955.602877] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x3

[  955.602878] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x1

[  955.602879] amdgpu 0000:09:00.0: amdgpu:      RW: 0x0

[  955.602891] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32791)

[  955.602892] amdgpu 0000:09:00.0: amdgpu:  Process python pid 7620 thread python pid 7620

[  955.602893] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00007f3555c01000 from client 10

[  955.602895] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801D3B

[  955.602896] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA1 (0xe)

[  955.602897] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x1

[  955.602898] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x5

[  955.602899] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x3

[  955.602900] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x1

[  955.602901] amdgpu 0000:09:00.0: amdgpu:      RW: 0x0

[  955.602913] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32791)

[  955.602914] amdgpu 0000:09:00.0: amdgpu:  Process python pid 7620 thread python pid 7620

[  955.602916] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00007f3555c01000 from client 10

[  955.602917] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801D3B

[  955.602918] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA1 (0xe)

[  955.602919] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x1

[  955.602920] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x5

[  955.602921] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x3

[  955.602922] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x1

[  955.602924] amdgpu 0000:09:00.0: amdgpu:      RW: 0x0

[  955.602935] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32791)

[  955.602936] amdgpu 0000:09:00.0: amdgpu:  Process python pid 7620 thread python pid 7620

[  955.602938] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00007f3555c01000 from client 10

[  955.602939] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801D3B

[  955.602940] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA1 (0xe)

[  955.602941] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x1

[  955.602942] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x5

[  955.602944] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x3

[  955.602945] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x1

[  955.602946] amdgpu 0000:09:00.0: amdgpu:      RW: 0x0

[  955.602957] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32791)

[  955.602962] amdgpu 0000:09:00.0: amdgpu:  Process python pid 7620 thread python pid 7620

[  955.602963] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00007f3555c01000 from client 10

[  955.602968] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32791)

[  955.602969] amdgpu 0000:09:00.0: amdgpu:  Process python pid 7620 thread python pid 7620

[  955.602970] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00007f3555c02000 from client 10

[  955.602983] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32791)

[  955.602985] amdgpu 0000:09:00.0: amdgpu:  Process python pid 7620 thread python pid 7620

[  955.602986] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00007f3555c02000 from client 10

</details>

I tested a variety of kernel and rocm versions, all with the same result.

Kernel Versions:

- 6.19.3-2-cachyos
- 6.18.13-2-cachyos-lts 

pytorch+rocm:

- versions 2.12.0.dev20260217+rocm7.1
- 2.9.1+rocm7.2.0.git7e1940d4 ~~([from arch package](https://archlinux.org/packages/extra/x86_64/python-pytorch-rocm/))~~ EDIT: It actually wasn't that arch package, I had selected the wrong python install. Now that I have tried it, I can't get it to work. Torch defaults to CUDA and I can't figure out how to change it.
- 2.9.1+rocm7.2.0.git7e1940d4 ([rocm/pytorch docker image](https://hub.docker.com/r/rocm/pytorch))
- 2.12.0.dev20260224+rocm7.2. Least stable and often crashes on the first run.

Hardware:

- CPU AMD Ryzen 7 5800X
- 64 GB RAM
- GPU AMD Radeon RX 9070 XT

\*On more thing l thing I noticed, after enough crashes and restarts of ComfyUI the crash eventually goes away. But there still seems to be some memory issues, that result in bad prompt adherence, noisy/blurry/deep fried images and NaN values in the generated images.

---

### 评论 #9 — jab416171 (2026-03-06T17:48:59Z)

6.19 is finally in the stable repo for arch, and it still crashes.
```
Memory access fault by GPU node-1 (Agent handle: 0x2f46f960) on address 0x7f8f3789f000. Reason: Page not present or supervisor privilege.
Failed to write segment data to pipe: Broken pipe
GPU coredump: handler exited with error (status: 1)
GPU core dump failed
```


[dmesg_1772819322.txt](https://github.com/user-attachments/files/25801184/dmesg_1772819322.txt)

---

### 评论 #10 — jeroen-mostert (2026-03-14T17:31:41Z)

I have experienced this error consistently from every ROCm version since 7.0 (RTX 7900 XTX on Manjaro here), specifically associated with ComfyUI. Simple workflows can be run many times in succession without trouble, but as soon as the workflow gets complicated and consumes lots of VRAM (using multiple models, upscaling, ComfyUI loading and unloading things repeatedly) a crash is all but guaranteed after a while. Things like llama.cpp run without fail, both with BLAS and Vulkan, as does vanilla 3D acceleration, which makes a hardware issue seem less likely.

None of the proposed workarounds (disabling CWSR, disabling tuning, futzing around with different versions of the kernel, ROCm and Torch, clean boots with different distros, including vanilla Ubuntu with AMD's DKMS driver) have done anything for me. Some combinations crash less frequently, but they all crash, and they all do it with `hipErrorIllegalAddress`.

The only thing that's worked for me is to run ComfyUI with `--disable-smart-memory`[^1]. There is some perf loss associated with this, but it's nothing compared to the time loss of having to restart the backend all the time. The fact that it only happens with sufficiently complicated workflows makes it hard to zoom in on the actual problem, short of the obvious observation that it likely has to do with memory management _somehow_.

I'm posting this here mainly as a reference for others who might also be trying to throw things at the wall to see what sticks, not to imply others are having the same underlying problem (since obviously access violations, especially delayed ones, can be caused by many, many things). The Qwen edit workflow posted in the OP consistently crashes for me as well, and `--disable-smart-memory` makes it run, albeit with Comfy shuffling the model in and out of memory between images.

**Update**: I've since discovered another option that seems to resolve the problems reliably: `--disable-pinned-memory`. This is superior to `--disable-smart-memory` since it keeps more of Comfy's memory management intact.

[^1]: Technically `--highvram` also works in the sense that it won't crash, but it inevitably leads to an OOM error that then destabilizes the environment and requires a manual restart of ComfyUI, which has much the same effect. It does further reinforce the idea that timing issues with active memory management are the culprit somehow.

---

### 评论 #11 — jab416171 (2026-04-14T01:48:28Z)

This is still crashing on 6.19.11-arch1-1 with torch==2.12.0a0+rocm7.13.0a20260413

```[  169.822093] amdgpu 0000:0d:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:8 pasid:32)
[  169.822099] amdgpu 0000:0d:00.0: amdgpu:  Process python3 pid 5772 thread python3 pid 5772
[  169.822102] amdgpu 0000:0d:00.0: amdgpu:   in page starting at address 0x00007f86f75b1000 from client 10
[  169.822104] amdgpu 0000:0d:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801D3B
[  169.822106] amdgpu 0000:0d:00.0: amdgpu: 	 Faulty UTCL2 client ID: SDMA1 (0xe)
[  169.822108] amdgpu 0000:0d:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  169.822110] amdgpu 0000:0d:00.0: amdgpu: 	 WALKER_ERROR: 0x5
[  169.822112] amdgpu 0000:0d:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  169.822114] amdgpu 0000:0d:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  169.822115] amdgpu 0000:0d:00.0: amdgpu: 	 RW: 0x0```

---

### 评论 #12 — jab416171 (2026-04-18T22:39:32Z)

update: `--disable-pinned-memory` did indeed prevent the crash (on 6.19.11). I tried both `--disable-pinned-memory` and `--disable-smart-memory` at first, that worked too, but just disabling pinned memory was a bit faster.

---
