# [Issue]: RX 9070 / gfx1201: massive prefill slowdown unless ROCBLAS_USE_HIPBLASLT=0 is set

> **Issue #6203**
> **状态**: open
> **创建时间**: 2026-05-07T07:58:49Z
> **更新时间**: 2026-05-17T18:03:44Z
> **作者**: marek99
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6203

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

I have Radeon R9700. I noticed in ollama logs:

rocblaslt error: Cannot read "TensileLibrary_lazy_gfx1201.dat": No such file or directory
rocblaslt error: Could not load "TensileLibrary_lazy_gfx1201.dat"

as I run ollama in podman container, I mounted the 7.2.3 libraries from the host in the quadlet:

Volume=/opt/rocm-7.2.3/lib/hipblaslt/library:/lib/ollama/rocm/hipblaslt/library:ro
Environment=HIPBLASLT_TENSILE_LIBPATH=/lib/ollama/rocm/hipblaslt/library

then the error in the podman/ollama logs was gone. 

However, I got a MASSIVE hit to performance. A medium-sized prompt run against qwen3.6 took 4 minutes to complete. Mostly spent in cold pre-filling.

when i eventually commented out these 7.2.3 libraries and instead added:
Environment=ROCBLAS_USE_HIPBLASLT=0

the performace was back to normal, the same prompt took like 20 secs to execute.

Took me a whole day of scratching my head (and help from Opus) to figure it out... :)



### Operating System

Debian 13 Trixie

### CPU

AMD Ryzen 7 9700X 

### GPU

 AMD Radeon AI PRO R9700 

### ROCm Version

ROCM 7.2.3

### ROCm Component

_No response_

### Steps to Reproduce

create an ollama podman container and provide the host ROCm 7.2.3 libraries to it:

# Provide the missing hipBLASLt kernel directory from the host
Volume=/opt/rocm-7.2.3/lib/hipblaslt/library:/lib/ollama/rocm/hipblaslt/library:ro
Environment=HIPBLASLT_TENSILE_LIBPATH=/lib/ollama/rocm/hipblaslt/library

then run a medium sized prompt (50k long) against it:

time curl http://localhost:11434/api/chat -d @prompt_file.json
real    4m12.321s

when the quadlet config for ollama is changed to:
#Volume=/opt/rocm-7.2.3/lib/hipblaslt/library:/lib/ollama/rocm/hipblaslt/library:ro
#Environment=HIPBLASLT_TENSILE_LIBPATH=/lib/ollama/rocm/hipblaslt/library
Environment=ROCBLAS_USE_HIPBLASLT=0

the same prompt runs much faster:
time curl http://localhost:11434/api/chat -d @prompt_file.json
real    0m29.903s



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2026-05-08T13:25:55Z)

Hey @marek99, there's two main issues here. The first is the `rocblaslt error: Could not load "TensileLibrary_` which is happening due to the hipBLASLt folder not being properly shipped with the ROCm libraries packaged with ollama - this'll be resolved with https://github.com/ollama/ollama/pull/14979. Your workaround corrects this by pulling in the library from your ROCm installation.

The second issue here is the performance drop off when enabling hipBLASLt specifically. We've recently had improvements to hipBLASLt on gfx12 as part of https://github.com/ROCm/ROCm/issues/5674#issuecomment-4245008535. These changes wouldn't have made it into ROCm 7.2.3 - can you try mounting the hipBLASLt library from [TheRock nightlies](https://github.com/ROCm/TheRock/blob/main/RELEASES.md#rocm-for-gfx120X-all) to check for any improvements? I'll also run some testing on my end to see if this case is already fixed/improved on or if this is a real bug.

---

### 评论 #2 — harkgill-amd (2026-05-08T14:05:08Z)

Just ran a quick test on my end and I'm not seeing the slowdown with ROCm 7.2.3. A ~50k word prompt took 19.5 secs with a 2884.9 tok/s prompt eval time. Can you run your hipBLASLt case with the following logging environment variables setup and share the output of `hipblaslt.log`. This'll give us a better idea of what kernels are being picked up under the hood. 
```
HIPBLASLT_TENSILE_LIBPATH=/lib/ollama/rocm/hipblaslt/library 
HIPBLASLT_LOG_LEVEL=5  
HIPBLASLT_LOG_MASK=0xFFFFFF           
TENSILE_DB=2  
ollama serve 2>&1 | tee hipblaslt.log

---

### 评论 #3 — marek99 (2026-05-08T15:02:53Z)

As I wrote - I'm running ollama docker image (0.23.1-rocm) inside the container - and there are no hipblast libraries bundled/shipped with this image.
so I assume you wanted me to retry my attempt to mount the hipblast libraries from the host (7.2.3). this is the excerpt of the container config I did then:

Volume=/opt/rocm-7.2.3/lib/hipblaslt/library:/lib/ollama/rocm/hipblaslt/library:ro
Environment=HIPBLASLT_TENSILE_LIBPATH=/lib/ollama/rocm/hipblaslt/library
Environment=HIPBLASLT_LOG_LEVEL=5
Environment=HIPBLASLT_LOG_MASK=0xFFFFFF
Environment=TENSILE_DB=2

then i run the curl to push the 50k chat to ollama,

I have noticed a huge list of mostly identical items like this one:

Single: Cijk_Alik_Bljk_B8F8HS_BH_Bias_SHB_HA_S_SAB_SCD_SAV_UserArgs_MT128x128x64_MI16x16x1_SN_LDSB1_AFC1_AFEM1_AFEM1_ASEM1_CLR1_CADS0_DTLA0_DTLB0_DTVA0_DTVB1_EPS1_FDSI0_GRPM1_GRVWA16_GRVWB16_GSU1_GSUAMB_GSUC0_GSUWGMRR0_GLS0_ISA1201_IU1_K1_LDSTI0_LBSPPA256_LBSPPB0_LBSPPM0_LPA32_LPB0_LPM0_LRVW16_LWPMn1_MIAV1_MIWT4_4_MO40_NTn1_NTA0_NTB0_NTC0_NTD0_NTM0_NEPBS0_NLCA1_NLCB2_ONLL0_PGR1_PLR1_PKA0_SIA3_SS1_SU32_SUM0_SUS256_SPO0_SRVW0_SSO0_SVW4_SK0_SKFTR0_SKXCCM0_TLDS1_ULSGRO0_USL1_UIOFGRO0_USFGROn1_VSn1_VWA4_VWB1_WSGRA0_WSGRB0_WS32_WG32_4_1_WGM8_WGMXCC1_WGMXCCGn1

for about two minutes, then the messages stop, but curl still was waiting for the response (but no log items was produced).
eventually, like 5 mins from starting of the curl the whole system hanged, had to hard reboot the machine...

the log generated was a few GB in size, so its not practical to attach it here I guess :)

tried it a couple of times, with the same result. 

when reverted to disabling hipblast, ollama responds fine in 20secs,

---

### 评论 #4 — harkgill-amd (2026-05-12T21:00:38Z)

> I have noticed a huge list of mostly identical items like this one:

Can you share the first 100 or so lines of the `hipblaslt.log` as a separate file? From what you're describing, it sounds like Tensile is going through all candidate solutions rather than lazy loading a solution based on `TensileLibrary_lazy_gfx1201.dat`. In theory, there could be a conflict between the `libhipblaslt.so.1.2.70201` that ships with ollama and the 7.2.3 libraries mounted into the container but I don't see this on my end where this exact same cases passes with similar performance (hipBLASLt vs rocblas). If you get a chance, it'd be worth testing with mounted 7.2.1 hipBLASLt libraries as well.

---

### 评论 #5 — marek99 (2026-05-17T18:03:44Z)

Surprisingly enough - I'm now unable to reproduce this issue... Not only the slowdown is gone, but it seems the inference is at least twice faster than it was before. No significant difference with/without the mounted libraries from the host. Can't pinpoint the exact reason though :( I did a couple of changes to the server configuration, but nothing directly related. I *might* have upgraded the kernel (but it would be a minor upgrade within the 6.19 line). I did not change ollama version.
So sadly, can't contribute anything meaningful at this moment. Shall I close the issue/ticket?

---
