# Why VALUBusy decreases when I increaseed m,n,k in hipBlas for GEMM

> **Issue #3122**
> **状态**: closed
> **创建时间**: 2024-05-13T04:17:22Z
> **更新时间**: 2024-09-23T19:02:26Z
> **关闭时间**: 2024-09-23T19:02:26Z
> **作者**: jaslip
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/3122

## 描述

I did some tests to understand the metrics meanings. ROCM version is 5.6
From VALUBusy definition , it should be a metric for computational intensibility
But by using hipBlas to do the matrix multiplication, when I increase the m,n,k from 1024 to 16384 , the VALUBusy decreases.
Is there a good way to make VALUBusy 100%.

m=n=k=1024, VALUBusy = ~13%

> dispatch[0], gpu-id(2), queue-id(1), queue-index(0), pid(270193), tid(270193), grd(131072), wgr(256), lds(28672), scr(0), arch_vgpr(120), accum_vgpr(136), sgpr(80), wave_size(64), sig(0x0), obj(0x7f07629ba280), kernel-name("Cijk_Ailk_Bjlk_SB_MT64x32x32_MI16x16x4x1_SE_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_DTL0_DTVA0_DVO0_ETSP_EPS0_FL0_GRPM1_GRVW4_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPP0_LPA0_LPB0_LDL1_LRVW1_LWPMn1_LDW0_MAC_MIAV0_MDA2_MO40_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR1_RK0_SIA3_SS0_SU0_SUM0_SUS0_SCIUI1_SPO0_SRVW2_SSO0_SVW4_SNLL0_TT2_16_TLDS0_USFGROn1_VAW1_VSn1_VW1_WSGRA1_WSGRB1_WS64_WG32_8_1_WGM1.kd"), time(15277600032233532,15277600042830898,15277600043827538,15277600043857508)
>   Wavefronts (2048.0000000000)
>   VALUUtilization (99.9811096718)
>   VALUBusy (13.5734378537)
>   CU_OCCUPANCY (0.0001708716)
>   MemUnitBusy (64.2969409816)
>   MemUnitStalled (0.0678148650)
> dispatch[1], gpu-id(2), queue-id(1), queue-index(1), pid(270193), tid(270193), grd(131072), wgr(256), lds(28672), scr(0), arch_vgpr(120), accum_vgpr(136), sgpr(80), wave_size(64), sig(0x0), obj(0x7f07629ba280), kernel-name("Cijk_Ailk_Bjlk_SB_MT64x32x32_MI16x16x4x1_SE_1LDSB0_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS0_ASE_ASGT_ASLT_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_DTL0_DTVA0_DVO0_ETSP_EPS0_FL0_GRPM1_GRVW4_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPP0_LPA0_LPB0_LDL1_LRVW1_LWPMn1_LDW0_MAC_MIAV0_MDA2_MO40_NTA0_NTB0_NTC0_NTD0_NEPBS0_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR1_RK0_SIA3_SS0_SU0_SUM0_SUS0_SCIUI1_SPO0_SRVW2_SSO0_SVW4_SNLL0_TT2_16_TLDS0_USFGROn1_VAW1_VSn1_VW1_WSGRA1_WSGRB1_WS64_WG32_8_1_WGM1.kd"), time(15277600042868279,15277600044102738,15277600045083218,15277600045095188)
>   Wavefronts (2048.0000000000)
>   VALUUtilization (99.9811096718)
>   VALUBusy (13.5306094163)
>   CU_OCCUPANCY (0.0001710446)
>   MemUnitBusy (66.6775008290)
>   MemUnitStalled (0.0764187533

)

m=n=k=16394, VALUBusy=~3%

> dispatch[0], gpu-id(2), queue-id(1), queue-index(0), pid(268793), tid(268793), grd(8388608), wgr(256), lds(12288), scr(0), arch_vgpr(96), accum_vgpr(0), sgpr(80), wave_size(64), sig(0x0), obj(0x7fafcc3bcb00), kernel-name("Cijk_Ailk_Bjlk_SB_MT128x64x16_MI16x16x4x1_SN_1LDSB1_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS3_ASE_ASGT_ASLT_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_DTL0_DTVA0_DVO0_ETSP_EPS1_FL0_GRPM1_GRVW4_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPP0_LPA0_LPB0_LDL1_LRVW1_LWPMn1_LDW0_FMA_MIAV1_MDA2_MO40_NTA0_NTB0_NTC3_NTD3_NEPBS4_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR5_RK0_SIA3_SS1_SU0_SUM0_SUS0_SCIUI1_SPO1_SRVW0_SSO4_SVW2_SNLL0_TT2_64_TLDS0_USFGRO0_VAW1_VSn1_VW2_WSGRA0_WSGRB1_WS64_WG64_4_1_WGM14.kd"), time(15276736681320367,15276736691842430,15276737627464944,15276737627526083)
>   Wavefronts (136755.0000000000)
>   VALUUtilization (99.9970170944)
>   VALUBusy (2.9285860827)
>   CU_OCCUPANCY (0.0000679340)
>   MemUnitBusy (99.2617638191)
>   MemUnitStalled (1.0302317526)
> dispatch[1], gpu-id(2), queue-id(1), queue-index(1), pid(268793), tid(268793), grd(8388608), wgr(256), lds(12288), scr(0), arch_vgpr(96), accum_vgpr(0), sgpr(80), wave_size(64), sig(0x0), obj(0x7fafcc3bcb00), kernel-name("Cijk_Ailk_Bjlk_SB_MT128x64x16_MI16x16x4x1_SN_1LDSB1_APM1_ABV0_ACED0_AF0EM1_AF1EM1_AMAS3_ASE_ASGT_ASLT_ASAE01_ASCE01_ASEM1_AAC0_BL1_BS1_DTL0_DTVA0_DVO0_ETSP_EPS1_FL0_GRPM1_GRVW4_GSU1_GSUASB_GLS0_ISA90a_IU1_K1_KLA_LBSPP0_LPA0_LPB0_LDL1_LRVW1_LWPMn1_LDW0_FMA_MIAV1_MDA2_MO40_NTA0_NTB0_NTC3_NTD3_NEPBS4_NLCA1_NLCB1_ONLL1_OPLV0_PK0_PAP0_PGR2_PLR5_RK0_SIA3_SS1_SU0_SUM0_SUS0_SCIUI1_SPO1_SRVW0_SSO4_SVW2_SNLL0_TT2_64_TLDS0_USFGRO0_VAW1_VSn1_VW2_WSGRA0_WSGRB1_WS64_WG64_4_1_WGM14.kd"), time(15276736691881553,15276737627742518,15276738616671622,15276738616765102)
>   Wavefronts (142864.0000000000)
>   VALUUtilization (99.9970179241)
>   VALUBusy (2.9557710412)
>   CU_OCCUPANCY (0.0000685492)
>   MemUnitBusy (99.4561729112)
>   MemUnitStalled (1.1018496450)
> 

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2024-05-30T13:51:33Z)

@jaslip Please tell us your OS and platform/GPU device. 
Also, provide commands that were run and output logs (with and without profiling).

Can you also check if issue is still reproducible with latest ROCm 6.1.2? Thanks!


---

### 评论 #2 — ppanchad-amd (2024-09-23T19:02:26Z)

@jaslip Closing this ticket for now. If you still need assistance with the ticket, please leave a comment and I will re-open the ticket for further investigation. Thanks!

---
