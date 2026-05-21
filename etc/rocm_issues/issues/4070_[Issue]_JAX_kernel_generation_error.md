# [Issue]: JAX kernel generation error

> **Issue #4070**
> **状态**: open
> **创建时间**: 2024-12-02T00:47:15Z
> **更新时间**: 2025-07-17T03:54:36Z
> **作者**: dipietrantonio
> **标签**: Under Investigation, ROCm 6.2.2, MI250X
> **URL**: https://github.com/ROCm/ROCm/issues/4070

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.2** (颜色: #ededed)
- **MI250X** (颜色: #ededed)

## 负责人

- Ruturaj4

## 描述

### Problem Description

# Problem description

I am trying to run ColabFold, a scientific machine learning tool built on top of AlphaFold, to predict protein structure given a sequence of amino-acids. The following kernel generation problem arises on very large problem instances where a single GCD's memory is not enough. 

AlphaFold uses JAX/XLA to offload operations to GPUs.

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
In previous work, we worked with AMD devs to implement Managed Memory support (https://github.com/ROCm/ROCm/issues/3364) to run these large problem instances in the first place.

# Steps to reproduce

The software has been built in a container: `singularity pull colabfold.sif docker://quay.io/dipietrantonio/colabfold:v8`

Here is the Dockerfile: https://github.com/PawseySC/pawsey-containers/blob/cdp-colabfold/colabfold/colabfold.dockerfile 

Input file: https://github.com/user-attachments/files/16229258/1IH7.7.a3m.txt (remove the .txt extension)

We want the software to run on a MI250X, which are the GPUs powering the Setonix supercomputer at Pawsey Supercomputing Research Centre. We know that the same test case runs on a MI300 because it has enough memory to hold the entire computation in its GPU memory.

Script to run the test case:

```
A3M=1IH7.7.a3m # input is a multiple sequence alignment 
OUT=$MYSCRATCH/colabfold-out-1IH7.7 # name of the output directory 

# define colabfold container 
containerImage=/path/to/colabfold.sif


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


### Operating System

Ubuntu 22 (in a container)

### CPU

AMD Milan (zen3) CPU

### GPU

MI250X

### ROCm Version

ROCm 6.2.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

This ticket is a continuation of https://github.com/ROCm/ROCm/issues/3364 

---

## 评论 (20 条)

### 评论 #1 — harkgill-amd (2024-12-03T14:11:53Z)

Hi @dipietrantonio, thanks for reporting this. I've notified the team members that worked on https://github.com/ROCm/ROCm/issues/3364 and they are looking into this.

---

### 评论 #2 — JehandadKhan (2024-12-16T22:23:48Z)

Hello @Ruturaj4  Can you please take a look at this? 

---

### 评论 #3 — al-rigazzi (2025-01-06T09:27:24Z)

Hello @JehandadKhan @Ruturaj4, any update on this?

---

### 评论 #4 — Ruturaj4 (2025-01-10T01:32:17Z)

@al-rigazzi Sorry for late reply, I was following up with one of our colleagues and he said that he is looking into it and will update soon he has some results.

---

### 评论 #5 — dipietrantonio (2025-01-20T02:38:33Z)

I have got an update on my latest experiment with ColabFold, that is, running it on a smaller test case. The job times out after 1 hour (I had set 1 hour time limit), so it progresses further than the other one crashing after 10 minutes. But looking at the logfile,  (`grep -i error colabfold_batch_20264283_4294967294.err -A 7 -B 7`) I see the following messages, which as very similar to the other case.

```
--
:3:hip_device_runtime.cpp   :636 : 3700546381595 us: [pid:1688798 tid:0x14bcd9061840]  hipGetDevice ( 0x7fff465e7ff4 ) 
:3:hip_device_runtime.cpp   :644 : 3700546381606 us: [pid:1688798 tid:0x14bcd9061840] hipGetDevice: Returned hipSuccess : 
:3:hip_device.cpp           :635 : 3700546381618 us: [pid:1688798 tid:0x14bcd9061840]  hipGetDevicePropertiesR0600 ( 0x7fff465e7ff8, 0 ) 
:3:hip_device.cpp           :637 : 3700546381629 us: [pid:1688798 tid:0x14bcd9061840] hipGetDevicePropertiesR0600: Returned hipSuccess : 
:3:hip_module.cpp           :74  : 3700546381656 us: [pid:1688798 tid:0x14bcd9061840]  hipModuleGetFunction ( 0x7fff465e86a8, 0x55b982caa730, Cijk_Ailk_Bljk_SB_MT128x96x16_MI32x32x2x1_SN_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASM_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_CLR0_DTLA0_DTLB0_DTVA0_DTVB0_DVO0_ETSP_EPS1_ELFLR0_EMLL0_FSSC10_FL0_GLVWA2_GLVWB2_GRCGA1_GRCGB1_GRPM1_GRVW2_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPPA0_LBSPPB128_LPA0_LPB4_LDL1_LRVW4_LWPMn1_LDW0_FMA_MIAV1_MDA2_MO40_MMFGLC_MKFGSU256_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR9_PKA0_SIA1_SLW1_SS0_SU0_SUM0_SUS0_SCIUI1_SPO0_SRVW0_SSO4_SVW4_SNLL0_TSGRA0_TSGRB0_TT1_96_TLDS1_UMLDSA0_UMLDSB1_USFGROn1_VAW1_VSn1_VW1_VWB1_VFLRP0_WSGRA0_WSGRB0_WS64_WG128_2_1_WGM15 ) 
:1:hip_code_object.cpp      :1006: 3700546381670 us: [pid:1688798 tid:0x14bcd9061840] Cannot find the function: Cijk_Ailk_Bljk_SB_MT128x96x16_MI32x32x2x1_SN_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASM_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_CLR0_DTLA0_DTLB0_DTVA0_DTVB0_DVO0_ETSP_EPS1_ELFLR0_EMLL0_FSSC10_FL0_GLVWA2_GLVWB2_GRCGA1_GRCGB1_GRPM1_GRVW2_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPPA0_LBSPPB128_LPA0_LPB4_LDL1_LRVW4_LWPMn1_LDW0_FMA_MIAV1_MDA2_MO40_MMFGLC_MKFGSU256_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR9_PKA0_SIA1_SLW1_SS0_SU0_SUM0_SUS0_SCIUI1_SPO0_SRVW0_SSO4_SVW4_SNLL0_TSGRA0_TSGRB0_TT1_96_TLDS1_UMLDSA0_UMLDSB1_USFGROn1_VAW1_VSn1_VW1_VWB1_VFLRP0_WSGRA0_WSGRB0_WS64_WG128_2_1_WGM15 
:1:hip_module.cpp           :84  : 3700546381681 us: [pid:1688798 tid:0x14bcd9061840] Cannot find the function: Cijk_Ailk_Bljk_SB_MT128x96x16_MI32x32x2x1_SN_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASM_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_CLR0_DTLA0_DTLB0_DTVA0_DTVB0_DVO0_ETSP_EPS1_ELFLR0_EMLL0_FSSC10_FL0_GLVWA2_GLVWB2_GRCGA1_GRCGB1_GRPM1_GRVW2_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPPA0_LBSPPB128_LPA0_LPB4_LDL1_LRVW4_LWPMn1_LDW0_FMA_MIAV1_MDA2_MO40_MMFGLC_MKFGSU256_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR9_PKA0_SIA1_SLW1_SS0_SU0_SUM0_SUS0_SCIUI1_SPO0_SRVW0_SSO4_SVW4_SNLL0_TSGRA0_TSGRB0_TT1_96_TLDS1_UMLDSA0_UMLDSB1_USFGROn1_VAW1_VSn1_VW1_VWB1_VFLRP0_WSGRA0_WSGRB0_WS64_WG128_2_1_WGM15 for module: 0x82caa730
:3:hip_module.cpp           :85  : 3700546381692 us: [pid:1688798 tid:0x14bcd9061840] hipModuleGetFunction: Returned hipErrorNotFound : 
:3:hip_error.cpp            :36  : 3700546381712 us: [pid:1688798 tid:0x14bcd9061840]  hipGetLastError (  ) 
:3:hip_module.cpp           :74  : 3700546381725 us: [pid:1688798 tid:0x14bcd9061840]  hipModuleGetFunction ( 0x7fff465e86a8, 0x55b983f32ce0, Cijk_Ailk_Bljk_SB_MT128x96x16_MI32x32x2x1_SN_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASM_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_CLR0_DTLA0_DTLB0_DTVA0_DTVB0_DVO0_ETSP_EPS1_ELFLR0_EMLL0_FSSC10_FL0_GLVWA2_GLVWB2_GRCGA1_GRCGB1_GRPM1_GRVW2_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPPA0_LBSPPB128_LPA0_LPB4_LDL1_LRVW4_LWPMn1_LDW0_FMA_MIAV1_MDA2_MO40_MMFGLC_MKFGSU256_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR9_PKA0_SIA1_SLW1_SS0_SU0_SUM0_SUS0_SCIUI1_SPO0_SRVW0_SSO4_SVW4_SNLL0_TSGRA0_TSGRB0_TT1_96_TLDS1_UMLDSA0_UMLDSB1_USFGROn1_VAW1_VSn1_VW1_VWB1_VFLRP0_WSGRA0_WSGRB0_WS64_WG128_2_1_WGM15 ) 
:3:hip_module.cpp           :88  : 3700546381739 us: [pid:1688798 tid:0x14bcd9061840] hipModuleGetFunction: Returned hipSuccess : 
:3:hip_module.cpp           :466 : 3700546381756 us: [pid:1688798 tid:0x14bcd9061840]  hipExtModuleLaunchKernel ( 0x0x55b988ba6fb0, 1280, 19, 1, 256, 1, 1, 0, stream:0x55b96dab18e0, char array:<null>, 0x7fff465e86f0, event:0, event:0, 0 ) 
:3:rocvirtual.cpp           :799 : 3700546381770 us: [pid:1688798 tid:0x14bcd9061840] Arg0:  Tensor2dSizeA = val:221184
:3:rocvirtual.cpp           :799 : 3700546381781 us: [pid:1688798 tid:0x14bcd9061840] Arg1:  Tensor2dSizeB = val:693504
:3:rocvirtual.cpp           :799 : 3700546381792 us: [pid:1688798 tid:0x14bcd9061840] Arg2:  AddressD = val:22722809858048
:3:rocvirtual.cpp           :799 : 3700546381803 us: [pid:1688798 tid:0x14bcd9061840] Arg3:  AddressC = val:22722809858048
```

However, the log does not present the message `hipGraphAddKernelNode: Returned hipErrorInvalidConfiguration : `
which is present in the crash log of the bigger test case.

---

### 评论 #6 — psanal35 (2025-06-16T17:35:44Z)

Hi @dipietrantonio, I'm following up to check on the current status of the issue. Are you still experiencing the same problem? If so, could you please share the version of JAX, and ROCm if it is updated?

---

### 评论 #7 — dipietrantonio (2025-06-18T09:27:56Z)

As far as I am aware there have not been further experiments and it was left as unresolved.

@al-rigazzi is there any update on your side?

---

### 评论 #8 — psanal35 (2025-06-19T15:10:08Z)

Hi @dipietrantonio and @al-rigazzi, I reviewed the earlier comments --just checking, are you using JAX 0.4.28-qa? Would you be open to trying a newer version, JAX/XLA 0.5.0 + ROCm 6.4.1? I've tested the same workload on a newer version, haven't seen the issue.

---

### 评论 #9 — al-rigazzi (2025-06-19T15:32:59Z)

@dipietrantonio I believe we agreed to stop, waiting for new ROCm versions to fix this issue.

OK @psanal35 , I can give it a try, thanks!

---

### 评论 #10 — dipietrantonio (2025-06-19T23:53:35Z)

I will also give it a try!

---

### 评论 #11 — SarahBeecroft (2025-06-23T07:54:49Z)

@psanal35 Just checking- were you using MI250 or MI300? It's not an issue on the MI300s, just 200 series. 

---

### 评论 #12 — psanal35 (2025-06-23T18:39:13Z)

Hi @SarahBeecroft, yes, I have tested on an MI200 series.

---

### 评论 #13 — dipietrantonio (2025-06-30T06:03:41Z)

Dear @psanal35, I have updated the Dockerfile and rebuilt the container to use JAX 0.5, but I do get another error:

In `stdout` I get:
```
2025-06-30 13:53:51,864 Could not predict 1IH7.7. Not Enough GPU memory? INTERNAL: Failed to launch ROCm kernel: gemm_fusion_dot_605 with block dimensions: 256x1x1: hipError_t(9)
```

I have built the container using ROCm 6.4, and the following line in the Docker recipe to build JAX.

```
RUN mkdir /opt/build-jax;\
    cd /opt/build-jax &&\
    git clone --branch rocm-jaxlib-v0.5.0  https://github.com/ROCm/jax.git &&\
    git clone --branch rocm-jaxlib-v0.5.0  https://github.com/ROCm/xla.git &&\
    cd jax &&\
    git status &&\
    /opt/miniconda3/bin/python3 -m pip install build &&\
    /opt/miniconda3/bin/python3 ./build/build.py build --wheels="jaxlib,jax-rocm-plugin,jax-rocm-pjrt"  --rocm_amdgpu_targets=gfx90a --bazel_options=--override_repository=xla=/opt/build-jax/xla --rocm_path=/opt/rocm-6.4.1
```

I am running on a MI250X GPU system.

---

### 评论 #14 — psanal35 (2025-07-08T04:06:00Z)

Hi @dipietrantonio, is it possible to share `AMD_LOG_LEVEL=3` logs? It would be good if you could also provide the output from `XLA_FLAGS="--xla_dump_to=<dump dir>"`.

---

### 评论 #15 — dipietrantonio (2025-07-10T06:41:56Z)

The log is 30MB of size, had to share it through Dropbox: https://www.dropbox.com/scl/fi/xtzurdesn0rp143qvwa4l/colabfold_log.txt?rlkey=i74ty529pq3ms484we7ouqwag&st=fqmnv43m&dl=0 

Where and how should I specify the second option, XLA_FLAGS="--xla_dump_to=<dump dir>"?


---

### 评论 #16 — psanal35 (2025-07-11T19:38:09Z)

Hi @dipietrantonio, thank you for sharing the logs. I'd like to suggest disabling Triton GEMM by setting: `XLA_FLAGS="--xla_gpu_enable_triton_gemm=false"` as a workaround. We're actively working on resolving the issue.

You can set XLA_FLAGS environment variables while running colabfold_batch, for example: `XLA_FLAGS="--xla_dump_to=<dump dir>" colabfold_batch input output`.

---

### 评论 #17 — dipietrantonio (2025-07-15T12:15:47Z)

@psanal35 Thank you for the tip! Disabling Triton GEMM has solved the reported issue. The software is currently running past the point where it would previously fail. So we can consider this issue solved.

Thank you very much for your help, and for the help of everyone involved in this work!

---

### 评论 #18 — dipietrantonio (2025-07-16T03:02:05Z)

@psanal35 you mentioned some known issues with GEMM algorithms. I get the output below from `stderr`. Most likely this is another issue. Let me know if you want me to open another GitHub issue.

```
E0716 10:15:06.907384 3367440 buffer_comparator.cc:156] Difference at 293739432: nan, expected 1600
E0716 10:15:06.907488 3367440 buffer_comparator.cc:156] Difference at 293739433: nan, expected 1592
E0716 10:15:06.907502 3367440 buffer_comparator.cc:156] Difference at 293739434: nan, expected 1576
E0716 10:15:06.907533 3367440 buffer_comparator.cc:156] Difference at 293739435: nan, expected 1592
E0716 10:15:06.907546 3367440 buffer_comparator.cc:156] Difference at 293739436: nan, expected 1576
E0716 10:15:06.907558 3367440 buffer_comparator.cc:156] Difference at 293739437: nan, expected 1576
E0716 10:15:06.907569 3367440 buffer_comparator.cc:156] Difference at 293739438: nan, expected 1576
E0716 10:15:06.907580 3367440 buffer_comparator.cc:156] Difference at 293739439: nan, expected 1584
E0716 10:15:06.907591 3367440 buffer_comparator.cc:156] Difference at 293739440: nan, expected 1584
E0716 10:15:06.907602 3367440 buffer_comparator.cc:156] Difference at 293739441: nan, expected 1608
2025-07-16 10:15:06.979073: E external/xla/xla/service/gpu/autotuning/gemm_algorithm_picker.cc:371] Results mismatch between different GEMM algorithms. This is likely a bug/unexpected loss of precision.
```

---

### 评论 #19 — psanal35 (2025-07-16T17:49:41Z)

Hi @dipietrantonio, is it possible share the output from `XLA_FLAGS="--xla_dump_to=<dump dir>"`?

---

### 评论 #20 — dipietrantonio (2025-07-17T03:52:28Z)

@psanal35 here it is: https://www.dropbox.com/scl/fi/a58lqzxjr34xa981gd7pv/dump_dir.tar.gz?rlkey=2339iue83e2okdrvpzizbm6e9&st=64nr6cjc&dl=0 

In addition, the job turns out to end because it kills the GPU node it's running on, due to some kernel bug. Here is what we could extract from the logs

```
[2025-07-16T20:42:48+08:00][1854229.275568][T4056360] Hardware name: HPE HPE_CRAY_EX235A/HPE CRAY EX235A, BIOS 2.1.0 01-23-2025
[2025-07-16T20:42:49+08:00][1854229.283887][T4056360] Workqueue: events svm_range_evict_svm_bo_worker [amdgpu]
[2025-07-16T20:42:49+08:00][1854229.290017][T4056360] RIP: 0010:svm_range_evict_svm_bo_worker+0x313/0x330 [amdgpu]
[2025-07-16T20:42:49+08:00][1854229.296808][T4056360] Code: 83 c4 28 be 03 00 00 00 5b 5d 41 5c 41 5d 41 5e 41 5f e9 b0 30 d3 d0 48 c7 c7 b8 1d d2 c1 c6 05 4a ed 75 00 01 e8 4d c0 88 d0 <0f> 0b e9 91 fe ff ff 31 db e9 28 ff ff ff 66 66 2e 0f 1f 84 00 00
[2025-07-16T20:42:49+08:00][1854229.314240][T4056360] RSP: 0018:ffffb74311317e40 EFLAGS: 00010286
[2025-07-16T20:42:49+08:00][1854229.320658][T4056360] RAX: 0000000000000000 RBX: 0000000000000001 RCX: 0000000000000027
[2025-07-16T20:42:49+08:00][1854229.329625][T4056360] RDX: 0000000000000000 RSI: 0000000000000002 RDI: ffff9f258e562948
[2025-07-16T20:42:49+08:00][1854229.338873][T4056360] RBP: ffff9f1801aea6b0 R08: 0000000000000000 R09: c0000000fffbffff
[2025-07-16T20:42:49+08:00][1854229.349256][T4056360] R10: ffff9f1802ec80d0 R11: ffffb74311317bb8 R12: ffff9ef80db09000
[2025-07-16T20:42:49+08:00][1854229.359824][T4056360] R13: 0000000000000000 R14: ffff9ef5cdbd50c0 R15: 0000000000000000
[2025-07-16T20:42:49+08:00][1854229.370888][T4056360] FS:  0000000000000000(0000) GS:ffff9f258e540000(0000) knlGS:0000000000000000
[2025-07-16T20:42:49+08:00][1854229.381317][T4056360] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[2025-07-16T20:42:49+08:00][1854229.387634][T4056360] CR2: 00007fdd91e270fe CR3: 000000369a810002 CR4: 0000000000770ee0
[2025-07-16T20:42:49+08:00][1854229.395567][T4056360] PKRU: 55555554
[2025-07-16T20:42:49+08:00][1854229.399444][T4056360] Call Trace:
[2025-07-16T20:42:49+08:00][1854229.403938][T4056360]  <TASK>
[2025-07-16T20:42:49+08:00][1854229.407497][T4056360]  process_one_work+0x2e2/0x4f0
[2025-07-16T20:42:49+08:00][1854229.412626][T4056360]  worker_thread+0x2d/0x3e0
[2025-07-16T20:42:49+08:00][1854229.417740][T4056360]  ? process_one_work+0x4f0/0x4f0
[2025-07-16T20:42:49+08:00][1854229.422032][T4056360]  kthread+0x13e/0x170
[2025-07-16T20:42:49+08:00][1854229.425651][T4056360]  ? set_kthread_struct+0x50/0x50
[2025-07-16T20:42:49+08:00][1854229.429948][T4056360]  ret_from_fork+0x22/0x30
[2025-07-16T20:42:49+08:00][1854229.433846][T4056360]  </TASK>
[2025-07-16T20:42:49+08:00][1854229.436831][T4056360] ---[ end trace 7e580e7cb8ff4c32 ]---
[2025-07-16T21:00:42+08:00][1855302.328139][T2276852] ------------[ cut here ]------------
**[2025-07-16T21:00:42+08:00][1855302.333710][T2276852] kernel BUG at /tmp/amd.2l5fjPEG/amd/amdgpu/amdgpu_res_cursor.h:65!
[2025-07-16T21:00:42+08:00][1855302.341491][T2276852] invalid opcode: 0000 [#1] SMP NOPTI**
[2025-07-16T21:00:42+08:00][1855302.345726][T2276852] CPU: 53 PID: 2276852 Comm: kworker/53:1 Tainted: G        W  OE      5.14.21-150500.55.83_13.0.62-cray_shasta_c #1 SLE15-SP5 (unreleased) 44ca073eaa01776d3993779fdb654d613836199b
[2025-07-16T21:00:42+08:00][1855302.345730][T2276852] Hardware name: HPE HPE_CRAY_EX235A/HPE CRAY EX235A, BIOS 2.1.0 01-23-2025
[2025-07-16T21:00:42+08:00][1855302.345732][T2276852] Workqueue: events amdgpu_irq_handle_ih_soft [amdgpu]
[2025-07-16T21:00:42+08:00][1855302.368642][T2276852] RIP: 0010:svm_migrate_copy_to_vram.isra.18+0x623/0x7f0 [amdgpu]
[2025-07-16T21:00:42+08:00][1855302.382601][T2276852] Code: 58 e9 51 fb ff ff be 02 00 00 00 48 89 44 24 58 e8 72 cc d2 d0 48 8b 04 24 48 8b 88 a8 02 00 00 48 8b 44 24 58 e9 2d fb ff ff <0f> 0b 0f 0b 49 01 c5 e9 ef fc ff ff 48 8b 54 24 40 48 8b 74 24 18
```

---
