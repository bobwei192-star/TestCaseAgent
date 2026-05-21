# 7900XTX cannot pass rocm-bandwidth-test

> **Issue #2253**
> **状态**: closed
> **创建时间**: 2023-06-19T16:26:21Z
> **更新时间**: 2023-06-26T05:55:23Z
> **关闭时间**: 2023-06-26T05:55:23Z
> **作者**: sdli1995
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2253

## 描述

test result is：
```
................
          RocmBandwidthTest Version: 2.6.0

          Launch Command is: /opt/rocm/bin/rocm-bandwidth-test (rocm_bandwidth -a + rocm_bandwidth -A)


          Device: 0,  AMD EPYC 7542 32-Core Processor
          Device: 1,  Radeon RX 7900 XTX,  GPU-XX,  83:0.0
          Device: 2,  Radeon RX 7900 XTX,  GPU-XX,  03:0.0

          Inter-Device Access

          D/D       0         1         2

          0         1         1         1

          1         1         1         0

          2         1         0         1


          Inter-Device Numa Distance

          D/D       0         1         2

          0         0         20        20

          1         20        0         N/A

          2         20        N/A       0


          Unidirectional copy peak bandwidth GB/s

          D/D       0           1           2

          0         N/A         28.411      28.410

          1         29.013      649.528     N/A

          2         29.016      N/A         636.462


          Bidirectional copy peak bandwidth GB/s

          D/D       0           1           2

          0         N/A         48.226      48.102

          1         48.226      N/A         N/A

          2         48.102      N/A         N/A


```
and every time i running rocm-bandwidth dmesg show logs like this
```
[89409.687795] [drm] PCIE GART of 512M enabled (table at 0x00000085FEB00000).
[89409.687822] [drm] PSP is resuming...
[89409.830428] [drm] reserve 0x1300000 from 0x85fc000000 for PSP TMR
[89409.958427] amdgpu 0000:83:00.0: amdgpu: RAP: optional rap ta ucode is not available
[89409.958429] amdgpu 0000:83:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[89409.958432] amdgpu 0000:83:00.0: amdgpu: SMU is resuming...
[89409.958436] amdgpu 0000:83:00.0: amdgpu: smu driver if version = 0x00000037, smu fw if version = 0x00000034, smu fw program = 0, smu fw version = 0x004e4b00 (78.75.0)
[89409.958440] amdgpu 0000:83:00.0: amdgpu: SMU driver if version not matched
[89410.122809] amdgpu 0000:83:00.0: amdgpu: SMU is resumed successfully!
[89410.124713] [drm] DMUB hardware initialized: version=0x07000A01
[89410.128965] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:91
[89410.131585] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:99
[89410.134208] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:107
[89410.136827] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:115
[89410.139587] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:91
[89410.142223] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:99
[89410.144859] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:107
[89410.147489] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:115
[89410.148818] [drm] kiq ring mec 3 pipe 1 q 0
[89410.153328] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[89410.153670] amdgpu 0000:83:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
[89410.154226] amdgpu 0000:83:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[89410.154227] amdgpu 0000:83:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[89410.154229] amdgpu 0000:83:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[89410.154230] amdgpu 0000:83:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[89410.154232] amdgpu 0000:83:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[89410.154233] amdgpu 0000:83:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[89410.154234] amdgpu 0000:83:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[89410.154235] amdgpu 0000:83:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[89410.154237] amdgpu 0000:83:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[89410.154238] amdgpu 0000:83:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[89410.154239] amdgpu 0000:83:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[89410.154240] amdgpu 0000:83:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 1
[89410.154241] amdgpu 0000:83:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 1
[89410.154243] amdgpu 0000:83:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 1
[89410.154244] amdgpu 0000:83:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[89410.157513] amdgpu 0000:83:00.0: [drm] Cannot find any crtc or sizes
[89410.157518] amdgpu 0000:83:00.0: [drm] Cannot find any crtc or sizes
[89410.158516] [drm] ring gfx_32793.1.1 was added
[89410.159065] [drm] ring compute_32793.2.2 was added
[89410.159547] [drm] ring compute_32793.2.3 was added
[89410.160270] [drm] ring compute_32793.2.4 was added
[89410.161219] [drm] ring compute_32793.2.5 was added
[89410.162523] [drm] ring sdma_32793.3.6 was added
[89410.162905] [drm] ring sdma_32793.3.7 was added
[89410.162916] [drm] ring gfx_32793.1.1 test pass
[89410.162953] [drm] ring gfx_32793.1.1 ib test pass
[89410.162959] [drm] ring compute_32793.2.2 test pass
[89410.162977] [drm] ring compute_32793.2.2 ib test pass
[89410.162991] [drm] ring compute_32793.2.3 test pass
[89410.163009] [drm] ring compute_32793.2.3 ib test pass
[89410.163017] [drm] ring compute_32793.2.4 test pass
[89410.163034] [drm] ring compute_32793.2.4 ib test pass
[89410.163045] [drm] ring compute_32793.2.5 test pass
[89410.163064] [drm] ring compute_32793.2.5 ib test pass
[89410.163189] [drm] ring sdma_32793.3.6 test pass
[89410.163227] [drm] ring sdma_32793.3.6 ib test pass
[89410.163306] [drm] ring sdma_32793.3.7 test pass
[89410.163343] [drm] ring sdma_32793.3.7 ib test pass
[89410.442671] [drm] PCIE GART of 512M enabled (table at 0x00000085FEB00000).
[89410.442697] [drm] PSP is resuming...
[89410.584425] [drm] reserve 0x1300000 from 0x85fc000000 for PSP TMR
[89410.712069] amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
[89410.712071] amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[89410.712073] amdgpu 0000:03:00.0: amdgpu: SMU is resuming...
[89410.712076] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x00000037, smu fw if version = 0x00000034, smu fw program = 0, smu fw version = 0x004e4b00 (78.75.0)
[89410.712079] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[89410.871431] amdgpu 0000:03:00.0: amdgpu: SMU is resumed successfully!
[89410.873435] [drm] DMUB hardware initialized: version=0x07000A01
[89410.877662] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:91
[89410.880293] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:99
[89410.882932] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:107
[89410.885568] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:115
[89410.888333] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:91
[89410.890978] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:99
[89410.893623] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:107
[89410.896264] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:115
[89410.897876] [drm] kiq ring mec 3 pipe 1 q 0
[89410.902957] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[89410.903116] amdgpu 0000:03:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
[89410.903653] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[89410.903655] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[89410.903656] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[89410.903658] amdgpu 0000:03:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[89410.903659] amdgpu 0000:03:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[89410.903660] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[89410.903661] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[89410.903662] amdgpu 0000:03:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[89410.903664] amdgpu 0000:03:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[89410.903665] amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[89410.903666] amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[89410.903668] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 1
[89410.903669] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 1
[89410.903670] amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 1
[89410.903671] amdgpu 0000:03:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[89410.907282] amdgpu 0000:03:00.0: [drm] Cannot find any crtc or sizes
[89410.907286] amdgpu 0000:03:00.0: [drm] Cannot find any crtc or sizes
[89410.908296] [drm] ring gfx_32795.1.1 was added
[89410.908832] [drm] ring compute_32795.2.2 was added
[89410.909308] [drm] ring compute_32795.2.3 was added
[89410.910048] [drm] ring compute_32795.2.4 was added
[89410.911013] [drm] ring compute_32795.2.5 was added
[89410.912311] [drm] ring sdma_32795.3.6 was added
[89410.912704] [drm] ring sdma_32795.3.7 was added
[89410.912716] [drm] ring gfx_32795.1.1 test pass
[89410.912754] [drm] ring gfx_32795.1.1 ib test pass
[89410.912760] [drm] ring compute_32795.2.2 test pass
[89410.912778] [drm] ring compute_32795.2.2 ib test pass
[89410.912791] [drm] ring compute_32795.2.3 test pass
[89410.912809] [drm] ring compute_32795.2.3 ib test pass
[89410.912821] [drm] ring compute_32795.2.4 test pass
[89410.912840] [drm] ring compute_32795.2.4 ib test pass
[89410.912848] [drm] ring compute_32795.2.5 test pass
[89410.912866] [drm] ring compute_32795.2.5 ib test pass
[89410.912985] [drm] ring sdma_32795.3.6 test pass
[89410.913024] [drm] ring sdma_32795.3.6 ib test pass
[89410.913100] [drm] ring sdma_32795.3.7 test pass
[89410.913139] [drm] ring sdma_32795.3.7 ib test pass
[89416.397435] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[89416.397449] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[89416.397454] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3A
[89416.397459] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: CPC (0x5)
[89416.397462] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x0
[89416.397466] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x5
[89416.397469] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[89416.397472] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x1
[89416.397475] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[89416.399005] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[89416.399017] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[89416.399023] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3A
[89416.399027] amdgpu 0000:03:00.0: amdgpu:      Faulty UTCL2 client ID: CPC (0x5)
[89416.399031] amdgpu 0000:03:00.0: amdgpu:      MORE_FAULTS: 0x0
[89416.399034] amdgpu 0000:03:00.0: amdgpu:      WALKER_ERROR: 0x5
[89416.399037] amdgpu 0000:03:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[89416.399040] amdgpu 0000:03:00.0: amdgpu:      MAPPING_ERROR: 0x1
[89416.399043] amdgpu 0000:03:00.0: amdgpu:      RW: 0x0
[89416.415415] amdgpu 0000:83:00.0: amdgpu: free PSP TMR buffer
[89416.417094] amdgpu 0000:03:00.0: amdgpu: free PSP TMR buffer

```

---

## 评论 (1 条)

### 评论 #1 — sdli1995 (2023-06-26T05:55:22Z)

slove by install amdgpu-dkms

---
