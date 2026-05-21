# [Issue]: MI50 32GB p2p not working

> **Issue #4793**
> **状态**: open
> **创建时间**: 2025-05-23T08:10:00Z
> **更新时间**: 2026-02-27T16:37:56Z
> **作者**: chenfengyuan
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4793

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I am having trouble getting P2P communication to work. BAR address space seems fine. I have no idea how to make it works.
Previously, I used the ROCm 6.4.0 version, but it didn't work properly. Now I'm trying the 5.7.1 version, and it still doesn't work correctly. The information below was all run using version 5.7.1.

Machine Info
```
Motherboard: X11SRA-F
amdgpu-dkms version: 1:6.2.4.50701-1664922.22.04
rocm-hip-sdk5.7.1 version: 5.7.1.50701-98~22.04
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
CPU:
model name      : Intel(R) Xeon(R) W-2135 CPU @ 3.70GHz
GPU:
  Name:                    Intel(R) Xeon(R) W-2135 CPU @ 3.70GHz
  Marketing Name:          Intel(R) Xeon(R) W-2135 CPU @ 3.70GHz
  Name:                    gfx906
  Marketing Name:          AMD Radeon Graphics
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
      Name:                    amdgcn-amd-amdhsa--gfx9-generic:sramecc+:xnack-
  Name:                    gfx906
  Marketing Name:          AMD Radeon Graphics
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
      Name:                    amdgcn-amd-amdhsa--gfx9-generic:sramecc+:xnack-
```
`lspci -vvv -nn`
```
....................................

19:00.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] Vega 20 [Radeon Pro VII/Radeon Instinct MI50 32GB] [1002:66a1] (rev 01)
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Vega 20 WKS GL-XE [Radeon Pro VII] [1002:0834]
        Control: I/O- Mem+ BusMaster+ SpecCycle- MemWINV- VGASnoop- ParErr- Stepping- SERR+ FastB2B- DisINTx+
        Status: Cap+ 66MHz- UDF- FastB2B- ParErr- DEVSEL=fast >TAbort- <TAbort- <MAbort- >SERR- <PERR- INTx-
        Latency: 0, Cache Line Size: 32 bytes
        Interrupt: pin A routed to IRQ 66
        NUMA node: 0
        Region 0: Memory at 5f800000000 (64-bit, prefetchable) [size=16G]
        Region 2: Memory at 5fc00000000 (64-bit, prefetchable) [size=2M]
        Region 5: Memory at bf900000 (32-bit, non-prefetchable) [size=512K]
        Expansion ROM at bf980000 [disabled] [size=128K]
        Capabilities: [48] Vendor Specific Information: Len=08 <?>
        Capabilities: [50] Power Management version 3
                Flags: PMEClk- DSI- D1- D2- AuxCurrent=0mA PME(D0-,D1+,D2+,D3hot+,D3cold+)
                Status: D0 NoSoftRst+ PME-Enable- DSel=0 DScale=0 PME-
        Capabilities: [64] Express (v2) Legacy Endpoint, MSI 00
                DevCap: MaxPayload 256 bytes, PhantFunc 0, Latency L0s <4us, L1 unlimited
                        ExtTag+ AttnBtn- AttnInd- PwrInd- RBE+ FLReset-
                DevCtl: CorrErr+ NonFatalErr+ FatalErr+ UnsupReq-
                        RlxdOrd+ ExtTag+ PhantFunc- AuxPwr- NoSnoop+
                        MaxPayload 256 bytes, MaxReadReq 512 bytes
                DevSta: CorrErr+ NonFatalErr- FatalErr- UnsupReq+ AuxPwr- TransPend-
                LnkCap: Port #0, Speed 16GT/s, Width x16, ASPM L0s L1, Exit Latency L0s <64ns, L1 <1us
                        ClockPM- Surprise- LLActRep- BwNot- ASPMOptComp+
                LnkCtl: ASPM L1 Enabled; RCB 64 bytes, Disabled- CommClk+
                        ExtSynch- ClockPM- AutWidDis- BWInt- AutBWInt-
                LnkSta: Speed 16GT/s (ok), Width x16 (ok)
                        TrErr- Train- SlotClk+ DLActive- BWMgmt- ABWMgmt-
                DevCap2: Completion Timeout: Range ABCD, TimeoutDis+ NROPrPrP- LTR+
                         10BitTagComp+ 10BitTagReq+ OBFF Not Supported, ExtFmt+ EETLPPrefix+, MaxEETLPPrefixes 1
                         EmergencyPowerReduction Not Supported, EmergencyPowerReductionInit-
                         FRS-
                         AtomicOpsCap: 32bit+ 64bit+ 128bitCAS-
                DevCtl2: Completion Timeout: 50us to 50ms, TimeoutDis- LTR- OBFF Disabled,
                         AtomicOpsCtl: ReqEn+
                LnkCap2: Supported Link Speeds: 2.5-16GT/s, Crosslink- Retimer+ 2Retimers+ DRS-
                LnkCtl2: Target Link Speed: 16GT/s, EnterCompliance- SpeedDis-
                         Transmit Margin: Normal Operating Range, EnterModifiedCompliance- ComplianceSOS-
                         Compliance De-emphasis: -6dB
                LnkSta2: Current De-emphasis Level: -3.5dB, EqualizationComplete+ EqualizationPhase1+
                         EqualizationPhase2+ EqualizationPhase3+ LinkEqualizationRequest-
                         Retimer- 2Retimers- CrosslinkRes: unsupported
        Capabilities: [a0] MSI: Enable+ Count=1/1 Maskable- 64bit+
                Address: 00000000fee00098  Data: 0000
        Capabilities: [100 v1] Vendor Specific Information: ID=0001 Rev=1 Len=010 <?>
        Capabilities: [150 v2] Advanced Error Reporting
                UESta:  DLP- SDES- TLP- FCP- CmpltTO- CmpltAbrt- UnxCmplt- RxOF- MalfTLP- ECRC- UnsupReq- ACSViol-
                UEMsk:  DLP- SDES- TLP- FCP- CmpltTO- CmpltAbrt- UnxCmplt- RxOF- MalfTLP- ECRC- UnsupReq+ ACSViol-
                UESvrt: DLP+ SDES+ TLP- FCP+ CmpltTO- CmpltAbrt- UnxCmplt- RxOF+ MalfTLP+ ECRC- UnsupReq- ACSViol-
                CESta:  RxErr- BadTLP- BadDLLP- Rollover- Timeout- AdvNonFatalErr+
                CEMsk:  RxErr- BadTLP- BadDLLP- Rollover- Timeout- AdvNonFatalErr+
                AERCap: First Error Pointer: 00, ECRCGenCap+ ECRCGenEn- ECRCChkCap+ ECRCChkEn-
                        MultHdrRecCap- MultHdrRecEn- TLPPfxPres- HdrLogCap-
                HeaderLog: 00000000 00000000 00000000 00000000
        Capabilities: [270 v1] Secondary PCI Express
                LnkCtl3: LnkEquIntrruptEn- PerformEqu-
                LaneErrStat: 0
        Capabilities: [2a0 v1] Access Control Services
                ACSCap: SrcValid- TransBlk- ReqRedir- CmpltRedir- UpstreamFwd- EgressCtrl- DirectTrans-
                ACSCtl: SrcValid- TransBlk- ReqRedir- CmpltRedir- UpstreamFwd- EgressCtrl- DirectTrans-
        Capabilities: [2b0 v1] Address Translation Service (ATS)
                ATSCap: Invalidate Queue Depth: 00
                ATSCtl: Enable-, Smallest Translation Unit: 00
        Capabilities: [2c0 v1] Page Request Interface (PRI)
                PRICtl: Enable- Reset-
                PRISta: RF- UPRGI- Stopped+
                Page Request Capacity: 00000100, Page Request Allocation: 00000000
        Capabilities: [2d0 v1] Process Address Space ID (PASID)
                PASIDCap: Exec+ Priv+, Max PASID Width: 10
                PASIDCtl: Enable- Exec- Priv-
        Capabilities: [320 v1] Latency Tolerance Reporting
                Max snoop latency: 1048576ns
                Max no snoop latency: 1048576ns
        Capabilities: [400 v1] Data Link Feature <?>
        Capabilities: [410 v1] Physical Layer 16.0 GT/s <?>
        Capabilities: [440 v1] Lane Margining at the Receiver <?>
        Kernel driver in use: amdgpu
        Kernel modules: amdgpu

.........................

67:00.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] Vega 20 [Radeon Pro VII/Radeon Instinct MI50 32GB] [1002:66a1] (rev 01)
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Vega 20 WKS GL-XE [Radeon Pro VII] [1002:0834]
        Control: I/O- Mem+ BusMaster+ SpecCycle- MemWINV- VGASnoop- ParErr- Stepping- SERR+ FastB2B- DisINTx+
        Status: Cap+ 66MHz- UDF- FastB2B- ParErr- DEVSEL=fast >TAbort- <TAbort- <MAbort- >SERR- <PERR- INTx-
        Latency: 0, Cache Line Size: 32 bytes
        Interrupt: pin A routed to IRQ 67
        NUMA node: 0
        Region 0: Memory at 6f800000000 (64-bit, prefetchable) [size=16G]
        Region 2: Memory at 6fc00000000 (64-bit, prefetchable) [size=2M]
        Region 5: Memory at e0d00000 (32-bit, non-prefetchable) [size=512K]
        Expansion ROM at e0d80000 [disabled] [size=128K]
        Capabilities: [48] Vendor Specific Information: Len=08 <?>
        Capabilities: [50] Power Management version 3
                Flags: PMEClk- DSI- D1- D2- AuxCurrent=0mA PME(D0-,D1+,D2+,D3hot+,D3cold+)
                Status: D0 NoSoftRst+ PME-Enable- DSel=0 DScale=0 PME-
        Capabilities: [64] Express (v2) Legacy Endpoint, MSI 00
                DevCap: MaxPayload 256 bytes, PhantFunc 0, Latency L0s <4us, L1 unlimited
                        ExtTag+ AttnBtn- AttnInd- PwrInd- RBE+ FLReset-
                DevCtl: CorrErr+ NonFatalErr+ FatalErr+ UnsupReq-
                        RlxdOrd+ ExtTag+ PhantFunc- AuxPwr- NoSnoop+
                        MaxPayload 256 bytes, MaxReadReq 512 bytes
                DevSta: CorrErr+ NonFatalErr- FatalErr- UnsupReq+ AuxPwr- TransPend-
                LnkCap: Port #0, Speed 16GT/s, Width x16, ASPM L0s L1, Exit Latency L0s <64ns, L1 <1us
                        ClockPM- Surprise- LLActRep- BwNot- ASPMOptComp+
                LnkCtl: ASPM L1 Enabled; RCB 64 bytes, Disabled- CommClk+
                        ExtSynch- ClockPM- AutWidDis- BWInt- AutBWInt-
                LnkSta: Speed 16GT/s (ok), Width x16 (ok)
                        TrErr- Train- SlotClk+ DLActive- BWMgmt- ABWMgmt-
                DevCap2: Completion Timeout: Range ABCD, TimeoutDis+ NROPrPrP- LTR+
                         10BitTagComp+ 10BitTagReq+ OBFF Not Supported, ExtFmt+ EETLPPrefix+, MaxEETLPPrefixes 1
                         EmergencyPowerReduction Not Supported, EmergencyPowerReductionInit-
                         FRS-
                         AtomicOpsCap: 32bit+ 64bit+ 128bitCAS-
                DevCtl2: Completion Timeout: 50us to 50ms, TimeoutDis- LTR- OBFF Disabled,
                         AtomicOpsCtl: ReqEn+
                LnkCap2: Supported Link Speeds: 2.5-16GT/s, Crosslink- Retimer+ 2Retimers+ DRS-
                LnkCtl2: Target Link Speed: 16GT/s, EnterCompliance- SpeedDis-
                         Transmit Margin: Normal Operating Range, EnterModifiedCompliance- ComplianceSOS-
                         Compliance De-emphasis: -6dB
                LnkSta2: Current De-emphasis Level: -3.5dB, EqualizationComplete+ EqualizationPhase1+
                         EqualizationPhase2+ EqualizationPhase3+ LinkEqualizationRequest-
                         Retimer- 2Retimers- CrosslinkRes: unsupported
        Capabilities: [a0] MSI: Enable+ Count=1/1 Maskable- 64bit+
                Address: 00000000fee00098  Data: 0000
        Capabilities: [100 v1] Vendor Specific Information: ID=0001 Rev=1 Len=010 <?>
        Capabilities: [150 v2] Advanced Error Reporting
                UESta:  DLP- SDES- TLP- FCP- CmpltTO- CmpltAbrt- UnxCmplt- RxOF- MalfTLP- ECRC- UnsupReq- ACSViol-
                UEMsk:  DLP- SDES- TLP- FCP- CmpltTO- CmpltAbrt- UnxCmplt- RxOF- MalfTLP- ECRC- UnsupReq+ ACSViol-
                UESvrt: DLP+ SDES+ TLP- FCP+ CmpltTO- CmpltAbrt- UnxCmplt- RxOF+ MalfTLP+ ECRC- UnsupReq- ACSViol-
                CESta:  RxErr- BadTLP- BadDLLP- Rollover- Timeout- AdvNonFatalErr+
                CEMsk:  RxErr- BadTLP- BadDLLP- Rollover- Timeout- AdvNonFatalErr+
                AERCap: First Error Pointer: 00, ECRCGenCap+ ECRCGenEn- ECRCChkCap+ ECRCChkEn-
                        MultHdrRecCap- MultHdrRecEn- TLPPfxPres- HdrLogCap-
                HeaderLog: 00000000 00000000 00000000 00000000
        Capabilities: [270 v1] Secondary PCI Express
                LnkCtl3: LnkEquIntrruptEn- PerformEqu-
                LaneErrStat: 0
        Capabilities: [2a0 v1] Access Control Services
                ACSCap: SrcValid- TransBlk- ReqRedir- CmpltRedir- UpstreamFwd- EgressCtrl- DirectTrans-
                ACSCtl: SrcValid- TransBlk- ReqRedir- CmpltRedir- UpstreamFwd- EgressCtrl- DirectTrans-
        Capabilities: [2b0 v1] Address Translation Service (ATS)
                ATSCap: Invalidate Queue Depth: 00
                ATSCtl: Enable-, Smallest Translation Unit: 00
        Capabilities: [2c0 v1] Page Request Interface (PRI)
                PRICtl: Enable- Reset-
                PRISta: RF- UPRGI- Stopped+
                Page Request Capacity: 00000100, Page Request Allocation: 00000000
        Capabilities: [2d0 v1] Process Address Space ID (PASID)
                PASIDCap: Exec+ Priv+, Max PASID Width: 10
                PASIDCtl: Enable- Exec- Priv-
        Capabilities: [320 v1] Latency Tolerance Reporting
                Max snoop latency: 1048576ns
                Max no snoop latency: 1048576ns
        Capabilities: [400 v1] Data Link Feature <?>
        Capabilities: [410 v1] Physical Layer 16.0 GT/s <?>
        Capabilities: [440 v1] Lane Margining at the Receiver <?>
        Kernel driver in use: amdgpu
        Kernel modules: amdgpu
...........................................................
```

rocm bandwidth test result
```
RocmBandwidthTest Version: 2.6.0

          Launch Command is: /opt/rocm-5.7.1/bin/rocm-bandwidth-test (rocm_bandwidth -a + rocm_bandwidth -A)


          Device: 0,  Intel(R) Xeon(R) W-2135 CPU @ 3.70GHz
          Device: 1,  AMD Radeon Graphics,  GPU-9318692173497dfc,  19:0.0
          Device: 2,  AMD Radeon Graphics,  GPU-6a96212172f0fcb5,  67:0.0

          Inter-Device Access

          D/D       0         1         2

          0         1         0         0

          1         1         1         0

          2         1         0         1


          Inter-Device Numa Distance

          D/D       0         1         2

          0         0         N/A       N/A

          1         20        0         N/A

          2         20        N/A       0


          Unidirectional copy peak bandwidth GB/s

          D/D       0           1           2

          0         N/A         13.750      13.769

          1         14.280      696.717     N/A

          2         14.280      N/A         586.201


          Bidirectional copy peak bandwidth GB/s

          D/D       0           1           2

          0         N/A         25.911      25.911

          1         25.911      N/A         N/A

          2         25.911      N/A         N/A
```

### Operating System

Ubuntu 22.04.3 LTS (Jammy Jellyfish)

### CPU

Intel(R) Xeon(R) W-2135 CPU @ 3.70GHz

### GPU

Radeon Instinct MI50 32GB

### ROCm Version

5.7.1 & 6.4.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-05-23T16:07:45Z)

Hi @chenfengyuan. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — Matthew-Jenkins (2025-06-05T15:02:08Z)

MI50 isn't supported anymore. So working with it is going to be increasingly difficult. Especially as docs and resources become increasingly rare as they are updated. MI50 support went through a deprecation and dropped support in ~6 months. It was out less than 5 years. It's why I haven't bought a MI100. AMDs past actions show MI100 could be deprecated then dropped at any moment. Even though you can occasionally find them under $1000. 

---

### 评论 #3 — deugeniy (2026-02-27T13:55:16Z)

Same problem with EPYC 7K62 on Gentoo Linux 6.12.31 - ROCM 7.1.0.
Fixed with: flashing my 32Gb cards with 016.004.000.056.013522 BIOS (P2P enabled) and rebuilding kernel with CONFIG_DMABUF_MOVE_NOTIFY and CONFIG_HSA_AMD_P2P.

---
