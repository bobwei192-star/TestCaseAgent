# [Issue]: ROCm 7.2.1 on Debian 13.4 Linux with 6.12 kernel on GMKtec EVO-X2 Strix Halo has a ruined hipallocator

> **Issue #6143**
> **状态**: closed
> **创建时间**: 2026-04-12T18:27:23Z
> **更新时间**: 2026-05-19T10:35:07Z
> **关闭时间**: 2026-05-19T10:35:06Z
> **作者**: ThomasKorimort
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6143

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- amd-nicknick

## 描述

### Problem Description

Having set the UMA buffer size to 96 GB in the BIOS and adjusted kernel parameters to 

GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdgpu.gttsize=98304 ttm.pages_limit=25000000 iommu=pt"

 the kernel crashes upon execution of the hip vectoradd test in :

(automatic1111) ai-service@GMKtec-EVO-X2:~/hip-examples/vectorAdd$ sudo dmesg -w | grep -iE "amdgpu|kfd|fault|ring"
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-6.12.74+deb13+1-amd64 root=UUID=cf6e5677-72ee-4993-97c8-635e9a091402 ro quiet splash amdgpu.gttsize=98304 ttm.pages_limit=25000000 iommu=pt
[    0.012587] Kernel command line: BOOT_IMAGE=/boot/vmlinuz-6.12.74+deb13+1-amd64 root=UUID=cf6e5677-72ee-4993-97c8-635e9a091402 ro quiet splash amdgpu.gttsize=98304 ttm.pages_limit=25000000 iommu=pt
[    0.069755] pid_max: default: 32768 minimum: 301
[    0.072231] Yama: disabled by default; enable with sysctl kernel.yama.*
[    0.181675] smp: Bringing up secondary CPUs ...
[    0.207108] ACPI: PM: Registering ACPI NVS region [mem 0x0a200000-0x0a287fff] (557056 bytes)
[    0.207108] ACPI: PM: Registering ACPI NVS region [mem 0x7037f000-0x7137efff] (16777216 bytes)
[    0.429685] PCI: Ignoring E820 reservations for host bridge windows
[    0.460158] Low-power S0 idle used by default for system suspend
[    0.460249] iommu: Default domain type: Passthrough (set via kernel command line)
[    0.461999] NetLabel:  unlabeled traffic allowed by default
[    0.484903] PCI: CLS 64 bytes, default 64
[    0.486124] PCI-DMA: Using software bounce buffering for IO (SWIOTLB)
[    0.489309] Initialise system trusted keyrings
[    0.489520] integrity: Platform Keyring initialized
[    0.489522] integrity: Machine keyring initialized
[    0.632333] Serial: 8250/16550 driver, 4 ports, IRQ sharing enabled
[    2.097755] resctrl: L3 monitoring detected
[    2.283340] nvme nvme0: 16/0/0 default/read/poll queues
[    2.292565] usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    2.292871] usb usb2: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    2.293802] usb usb3: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    2.294492] usb usb4: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    2.295638] usb usb5: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    2.295894] usb usb6: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    2.296825] usb usb7: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    2.297050] usb usb8: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    3.526961] [drm] amdgpu kernel modesetting enabled.
[    3.526966] [drm] amdgpu version: 6.16.13
[    3.527876] amdgpu: Virtual CRAT table created for CPU
[    3.527882] amdgpu: Topology: Add CPU node
[    3.530770] amdgpu 0000:c5:00.0: enabling device (0006 -> 0007)
[    3.530830] amdgpu 0000:c5:00.0: amdgpu: initializing kernel modesetting (IP DISCOVERY 0x1002:0x1586 0x2014:0x801D 0xC1).
[    3.530851] amdgpu 0000:c5:00.0: amdgpu: register mmio base: 0xA0200000
[    3.530852] amdgpu 0000:c5:00.0: amdgpu: register mmio size: 1048576
[    3.533833] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 0 <common_v1_0_0> (soc21_common)
[    3.533835] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 1 <gmc_v11_0_0> (gmc_v11_0)
[    3.533836] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 2 <ih_v6_0_0> (ih_v6_1)
[    3.533837] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 3 <psp_v13_0_0> (psp)
[    3.533838] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 4 <smu_v14_0_0> (smu)
[    3.533839] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 5 <dce_v1_0_0> (dm)
[    3.533840] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 6 <gfx_v11_0_0> (gfx_v11_0)
[    3.533841] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 7 <sdma_v6_0_0> (sdma_v6_0)
[    3.533842] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 8 <vcn_v4_0_5> (vcn_v4_0_5)
[    3.533843] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 9 <jpeg_v4_0_5> (jpeg_v4_0_5)
[    3.533843] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 10 <mes_v11_0_0> (mes_v11_0)
[    3.533844] amdgpu 0000:c5:00.0: amdgpu: detected ip block number 11 <vpe_v6_1_0> (vpe_v6_1)
[    3.533866] amdgpu 0000:c5:00.0: amdgpu: Fetched VBIOS from VFCT
[    3.533867] amdgpu: ATOM BIOS: 113-STRXLGEN-001
[    3.539316] amdgpu 0000:c5:00.0: amdgpu: VPE: collaborate mode true
[    3.539319] amdgpu 0000:c5:00.0: amdgpu: Trusted Memory Zone (TMZ) feature disabled as experimental (default)
[    3.539366] amdgpu 0000:c5:00.0: amdgpu: vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
[    3.539386] amdgpu 0000:c5:00.0: amdgpu: VRAM: 98304M 0x0000008000000000 - 0x00000097FFFFFFFF (98304M used)
[    3.539387] amdgpu 0000:c5:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[    3.539802] amdgpu 0000:c5:00.0: amdgpu: amdgpu: 98304M of VRAM memory ready
[    3.539803] amdgpu 0000:c5:00.0: amdgpu: [drm] Configuring gttsize via module parameter is deprecated, please use ttm.pages_limit
[    3.539803] amdgpu 0000:c5:00.0: amdgpu: [drm] GTT size has been set as 103079215104 but TTM size has been set as 16638816256, this is unusual
[    3.539804] amdgpu 0000:c5:00.0: amdgpu: amdgpu: 98304M of GTT memory ready.
[    3.540839] amdgpu 0000:c5:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x09003500
[    3.541207] amdgpu 0000:c5:00.0: amdgpu: [VCN instance 0] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 27
[    3.541247] amdgpu 0000:c5:00.0: amdgpu: [VCN instance 1] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 27
[    3.564978] amdgpu 0000:c5:00.0: amdgpu: reserve 0x8c00000 from 0x97e0000000 for PSP TMR
[    3.902695] amdgpu 0000:c5:00.0: amdgpu: RAS: optional ras ta ucode is not available
[    3.906615] amdgpu 0000:c5:00.0: amdgpu: RAP: optional rap ta ucode is not available
[    3.906617] amdgpu 0000:c5:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
[    3.942098] amdgpu 0000:c5:00.0: amdgpu: SMU is initialized successfully!
[    3.943392] amdgpu 0000:c5:00.0: amdgpu: [drm] Display Core v3.2.359 initialized on DCN 3.5.1
[    3.943393] amdgpu 0000:c5:00.0: amdgpu: [drm] DP-HDMI FRL PCON supported
[    3.946146] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09003500
[    3.949850] amdgpu 0000:c5:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.949938] amdgpu 0000:c5:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.950057] amdgpu 0000:c5:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.950170] amdgpu 0000:c5:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.950284] amdgpu 0000:c5:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.950333] amdgpu 0000:c5:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.950374] amdgpu 0000:c5:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.950415] amdgpu 0000:c5:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.950454] amdgpu 0000:c5:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.960319] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[    3.960324] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[    3.963144] amdgpu: Virtual CRAT table created for GPU
[    3.963938] amdgpu: Topology: Add dGPU node [0x1586:0x1002]
[    3.963939] kfd kfd: amdgpu: added device 1002:1586
[    3.963948] amdgpu 0000:c5:00.0: amdgpu: SE 2, SH per SE 2, CU per SH 10, active_cu_number 40
[    3.963952] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[    3.963953] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[    3.963953] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[    3.963953] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[    3.963954] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[    3.963954] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[    3.963955] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[    3.963955] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[    3.963955] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[    3.963956] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[    3.963956] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[    3.963957] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[    3.963957] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[    3.963957] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[    3.963958] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[    3.963958] amdgpu 0000:c5:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[    3.965096] amdgpu 0000:c5:00.0: amdgpu: Runtime PM not available
[    3.965457] [drm] Initialized amdgpu 3.64.0 for 0000:c5:00.0 on minor 0
[    3.987436] amdgpu 0000:c5:00.0: [drm] Cannot find any crtc or sizes
[    3.987486] amdgpu 0000:c5:00.0: [drm] Cannot find any crtc or sizes
[    3.987491] amdgpu 0000:c5:00.0: [drm] Cannot find any crtc or sizes
[    4.506008] systemd[1]: Queued start job for default target graphical.target.
[    4.761037] snd_hda_intel 0000:c5:00.1: bound 0000:c5:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
[   10.882122] audit: type=1400 audit(1776016193.288:126): apparmor="STATUS" operation="profile_load" profile="unconfined" name="docker-default" pid=1942 comm="apparmor_parser"
[   11.099753] bridge: filtering via arp/ip/ip6tables is no longer available by default. Update your scripts to load br_netfilter if you need this.
[   11.287325] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
[   11.287341] amdgpu 0000:c5:00.0: amdgpu:  Process ollama pid 2231 thread ollama pid 2231
[   11.287345] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f1b61269000 from client 10
[   11.287349] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[   11.287351] amdgpu 0000:c5:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
[   11.287353] amdgpu 0000:c5:00.0: amdgpu:      MORE_FAULTS: 0x0
[   11.287354] amdgpu 0000:c5:00.0: amdgpu:      WALKER_ERROR: 0x1
[   11.287355] amdgpu 0000:c5:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[   11.287357] amdgpu 0000:c5:00.0: amdgpu:      MAPPING_ERROR: 0x1
[   11.287358] amdgpu 0000:c5:00.0: amdgpu:      RW: 0x0
[   11.772019] NFS: Registering the id_resolver key type
[   13.493502] traps: python[2327] general protection fault ip:7f63db8b09df sp:7f613e9fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f63db623000+481000]
[   28.693387] traps: python[2661] general protection fault ip:7fa6be2b09df sp:7fa4210fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fa6be023000+481000]
[   43.938164] traps: python[2803] general protection fault ip:7fdddb0b09df sp:7fdb3e1fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fdddae23000+481000]
[   59.199907] traps: python[2945] general protection fault ip:7fc142eb09df sp:7fbea5efa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fc142c23000+481000]
[   74.444098] traps: python[3097] general protection fault ip:7f00fdcb09df sp:7efe60cfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f00fda23000+481000]
[   89.722153] traps: python[3267] general protection fault ip:7f82e52b09df sp:7f80482fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f82e5023000+481000]
[  104.950990] traps: python[3411] general protection fault ip:7fec30cb09df sp:7fe9939fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fec30a23000+481000]
[  120.216485] traps: python[3559] general protection fault ip:7f72676b09df sp:7f6fca5fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f7267423000+481000]
[  135.446414] traps: python[3703] general protection fault ip:7f535dcb09df sp:7f50c0bfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f535da23000+481000]
[  150.693087] traps: python[3848] general protection fault ip:7f13924b09df sp:7f10f55fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f1392223000+481000]
[  165.956371] traps: python[3992] general protection fault ip:7f44ee4b09df sp:7f42513fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f44ee223000+481000]
[  181.216082] traps: python[4144] general protection fault ip:7fbdf08b09df sp:7fbb536fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fbdf0623000+481000]
[  196.454978] traps: python[4287] general protection fault ip:7f5778eb09df sp:7f54dbffa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f5778c23000+481000]
[  211.732271] traps: python[4424] general protection fault ip:7fcaa66b09df sp:7fc8095fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fcaa6423000+481000]
[  226.903041] traps: python[4570] general protection fault ip:7f40e8cb09df sp:7f3e4bcfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f40e8a23000+481000]
[  242.221886] traps: python[4712] general protection fault ip:7feafe2b09df sp:7fe8613fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7feafe023000+481000]
[  257.431337] traps: python[4858] general protection fault ip:7f55b50b09df sp:7f5317ffa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f55b4e23000+481000]
[  272.739417] traps: python[5010] general protection fault ip:7f3a6f6b09df sp:7f37d21fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f3a6f423000+481000]
[  287.948286] traps: python[5154] general protection fault ip:7f6e44eb09df sp:7f6ba7dfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f6e44c23000+481000]
[  303.215941] traps: python[5298] general protection fault ip:7fedd5cb09df sp:7feb389fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fedd5a23000+481000]
[  318.417424] traps: python[5699] general protection fault ip:7f3f5cab09df sp:7f3cbf9fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f3f5c823000+481000]
[  333.662547] traps: python[5844] general protection fault ip:7fb6e32b09df sp:7fb4461fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fb6e3023000+481000]
[  348.971308] traps: python[6072] general protection fault ip:7f1e2deb09df sp:7f1b90bfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f1e2dc23000+481000]
[  364.145845] traps: python[6217] general protection fault ip:7fb8e5ab09df sp:7fb6489fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fb8e5823000+481000]
[  379.204057] traps: python[6360] general protection fault ip:7fe97beb09df sp:7fe6dedfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fe97bc23000+481000]
[  394.421930] traps: python[6504] general protection fault ip:7fdd7d6b09df sp:7fdae05fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fdd7d423000+481000]
[  409.721996] traps: python[6648] general protection fault ip:7fbe9dcb09df sp:7fbc00bfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fbe9da23000+481000]
[  424.971988] traps: python[6805] general protection fault ip:7fcab7ab09df sp:7fc81aafa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fcab7823000+481000]
[  440.203222] traps: python[6948] general protection fault ip:7f2bc6cb09df sp:7f2929bfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f2bc6a23000+481000]
[  444.287684] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
[  444.287705] amdgpu 0000:c5:00.0: amdgpu:  Process rvs pid 6958 thread rvs pid 6958
[  444.287710] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f5c29dd8000 from client 10
[  444.287715] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800B32
[  444.287719] amdgpu 0000:c5:00.0: amdgpu:      Faulty UTCL2 client ID: CPC (0x5)
[  444.287723] amdgpu 0000:c5:00.0: amdgpu:      MORE_FAULTS: 0x0
[  444.287725] amdgpu 0000:c5:00.0: amdgpu:      WALKER_ERROR: 0x1
[  444.287728] amdgpu 0000:c5:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[  444.287730] amdgpu 0000:c5:00.0: amdgpu:      MAPPING_ERROR: 0x1
[  444.287732] amdgpu 0000:c5:00.0: amdgpu:      RW: 0x0
[  455.488154] traps: python[7099] general protection fault ip:7f3beaab09df sp:7f394dbfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f3bea823000+481000]
[  470.715484] traps: python[7244] general protection fault ip:7faf102b09df sp:7fac732fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7faf10023000+481000]
[  485.927084] traps: python[7387] general protection fault ip:7f5fafcb09df sp:7f5d12dfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f5fafa23000+481000]
[  501.204396] traps: python[7529] general protection fault ip:7fb5600b09df sp:7fb2c30fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fb55fe23000+481000]
[  516.438004] traps: python[7669] general protection fault ip:7fbdcfab09df sp:7fbb32afa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fbdcf823000+481000]
[  519.732402] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
[  519.732427] amdgpu 0000:c5:00.0: amdgpu:  Process rvs pid 7679 thread rvs pid 7679
[  519.732434] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f8a30ff0000 from client 10
[  519.732440] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800B32
[  519.732444] amdgpu 0000:c5:00.0: amdgpu:      Faulty UTCL2 client ID: CPC (0x5)
[  519.732448] amdgpu 0000:c5:00.0: amdgpu:      MORE_FAULTS: 0x0
[  519.732451] amdgpu 0000:c5:00.0: amdgpu:      WALKER_ERROR: 0x1
[  519.732454] amdgpu 0000:c5:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[  519.732456] amdgpu 0000:c5:00.0: amdgpu:      MAPPING_ERROR: 0x1
[  519.732459] amdgpu 0000:c5:00.0: amdgpu:      RW: 0x0
[  531.666641] traps: python[7820] general protection fault ip:7fc0288b09df sp:7fbd8b5fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fc028623000+481000]
[  546.888059] traps: python[7966] general protection fault ip:7f0eeeeb09df sp:7f0c51efa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f0eeec23000+481000]
[  561.977183] traps: python[8109] general protection fault ip:7f94c38b09df sp:7f92269fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f94c3623000+481000]
[  577.261114] traps: python[8258] general protection fault ip:7fda2d8b09df sp:7fd7907fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fda2d623000+481000]
[  592.461811] traps: python[8401] general protection fault ip:7faddb0b09df sp:7fab3defa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7faddae23000+481000]
[  604.815017] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
[  604.815043] amdgpu 0000:c5:00.0: amdgpu:  Process rvs pid 8500 thread rvs pid 8500
[  604.815049] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007fd5211f1000 from client 10
[  604.815056] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800B32
[  604.815060] amdgpu 0000:c5:00.0: amdgpu:      Faulty UTCL2 client ID: CPC (0x5)
[  604.815064] amdgpu 0000:c5:00.0: amdgpu:      MORE_FAULTS: 0x0
[  604.815067] amdgpu 0000:c5:00.0: amdgpu:      WALKER_ERROR: 0x1
[  604.815070] amdgpu 0000:c5:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[  604.815072] amdgpu 0000:c5:00.0: amdgpu:      MAPPING_ERROR: 0x1
[  604.815075] amdgpu 0000:c5:00.0: amdgpu:      RW: 0x0
[  607.734015] traps: python[8554] general protection fault ip:7fb9856b09df sp:7fb6e85fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fb985423000+481000]
[  622.907110] traps: python[8704] general protection fault ip:7f93f2ab09df sp:7f9155afa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f93f2823000+481000]
[  637.925262] traps: python[8846] general protection fault ip:7f5400ab09df sp:7f51639fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f5400823000+481000]
[  653.211269] traps: python[8991] general protection fault ip:7f8fa3cb09df sp:7f8d06dfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f8fa3a23000+481000]
[  668.436999] traps: python[9130] general protection fault ip:7f133a4b09df sp:7f109d5fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f133a223000+481000]
[  683.425132] traps: python[9278] general protection fault ip:7fd859eb09df sp:7fd5bcdfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fd859c23000+481000]
[  698.726747] traps: python[9420] general protection fault ip:7fc1506b09df sp:7fbeb34fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fc150423000+481000]
[  713.931002] traps: python[9565] general protection fault ip:7fb7c26b09df sp:7fb5257fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fb7c2423000+481000]
[  729.328374] traps: python[9778] general protection fault ip:7fe48d0b09df sp:7fe1f00fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fe48ce23000+481000]
[  744.501655] traps: python[9921] general protection fault ip:7f5cdceb09df sp:7f5a3fefa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f5cdcc23000+481000]
[  759.707549] traps: python[10065] general protection fault ip:7fbaa7eb09df sp:7fb80adfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fbaa7c23000+481000]
[  774.973803] traps: python[10227] general protection fault ip:7fd746cb09df sp:7fd4a9dfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fd746a23000+481000]
[  790.211772] traps: python[10372] general protection fault ip:7f7e8a6b09df sp:7f7bed6fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f7e8a423000+481000]
[  794.299500] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
[  794.299524] amdgpu 0000:c5:00.0: amdgpu:  Process vectoradd_hip.e pid 10436 thread vectoradd_hip.e pid 10436
[  794.299530] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f7dd7eb4000 from client 10
[  794.299535] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[  794.299539] amdgpu 0000:c5:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
[  794.299542] amdgpu 0000:c5:00.0: amdgpu:      MORE_FAULTS: 0x0
[  794.299545] amdgpu 0000:c5:00.0: amdgpu:      WALKER_ERROR: 0x1
[  794.299547] amdgpu 0000:c5:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[  794.299549] amdgpu 0000:c5:00.0: amdgpu:      MAPPING_ERROR: 0x1
[  794.299552] amdgpu 0000:c5:00.0: amdgpu:      RW: 0x0
[  805.408776] traps: python[10575] general protection fault ip:7f5e84eb09df sp:7f5be7cfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f5e84c23000+481000]
[  820.453493] traps: python[10715] general protection fault ip:7f9c39ab09df sp:7f999c9fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f9c39823000+481000]
[  835.708765] traps: python[10867] general protection fault ip:7f0c2e2b09df sp:7f09911fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f0c2e023000+481000]
[  851.000253] traps: python[11012] general protection fault ip:7f2ac0eb09df sp:7f2823ffa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f2ac0c23000+481000]
[  866.230079] traps: python[11158] general protection fault ip:7f8699eb09df sp:7f83fcefa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f8699c23000+481000]
[  878.808351] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
[  878.808376] amdgpu 0000:c5:00.0: amdgpu:  Process vectoradd_hip.e pid 11295 thread vectoradd_hip.e pid 11295
[  878.808384] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f24ee711000 from client 10
[  878.808390] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[  878.808395] amdgpu 0000:c5:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
[  878.808399] amdgpu 0000:c5:00.0: amdgpu:      MORE_FAULTS: 0x0
[  878.808402] amdgpu 0000:c5:00.0: amdgpu:      WALKER_ERROR: 0x1
[  878.808405] amdgpu 0000:c5:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[  878.808408] amdgpu 0000:c5:00.0: amdgpu:      MAPPING_ERROR: 0x1
[  878.808410] amdgpu 0000:c5:00.0: amdgpu:      RW: 0x0
[  881.449186] traps: python[11309] general protection fault ip:7efe370b09df sp:7efb99ffa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7efe36e23000+481000]
[  896.813784] traps: python[11453] general protection fault ip:7fa23b6b09df sp:7f9f9e1fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fa23b423000+481000]
[  912.059073] traps: python[11615] general protection fault ip:7efe47ab09df sp:7efbaaafa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7efe47823000+481000]
[  927.305578] traps: python[11760] general protection fault ip:7f4df32b09df sp:7f4b561fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f4df3023000+481000]
[  942.617103] traps: python[11903] general protection fault ip:7f5c3c2b09df sp:7f599f0fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f5c3c023000+481000]
[  957.849415] traps: python[12047] general protection fault ip:7f9e8c4b09df sp:7f9bef3fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f9e8c223000+481000]
[  973.111781] traps: python[12184] general protection fault ip:7f2079cb09df sp:7f1ddccfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f2079a23000+481000]
[  988.319623] traps: python[12326] general protection fault ip:7f70d6cb09df sp:7f6e39bfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f70d6a23000+481000]
[ 1003.679048] traps: python[12474] general protection fault ip:7f6d5d2b09df sp:7f6ac00fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f6d5d023000+481000]
[ 1019.141086] traps: python[12616] general protection fault ip:7f52d0eb09df sp:7f5033efa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f52d0c23000+481000]
[ 1034.393702] traps: python[12767] general protection fault ip:7fc0190b09df sp:7fbd7c0fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fc018e23000+481000]
[ 1048.901249] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32771)
[ 1048.901274] amdgpu 0000:c5:00.0: amdgpu:  Process vectoradd_hip.e pid 12935 thread vectoradd_hip.e pid 12935
[ 1048.901281] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f648ea76000 from client 10
[ 1048.901287] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[ 1048.901292] amdgpu 0000:c5:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
[ 1048.901296] amdgpu 0000:c5:00.0: amdgpu:      MORE_FAULTS: 0x0
[ 1048.901299] amdgpu 0000:c5:00.0: amdgpu:      WALKER_ERROR: 0x1
[ 1048.901302] amdgpu 0000:c5:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[ 1048.901305] amdgpu 0000:c5:00.0: amdgpu:      MAPPING_ERROR: 0x1
[ 1048.901307] amdgpu 0000:c5:00.0: amdgpu:      RW: 0x0
[ 1049.577357] traps: python[12934] general protection fault ip:7f9785cb09df sp:7f94e8bfa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f9785a23000+481000]
[ 1064.856302] traps: python[13085] general protection fault ip:7fb4edcb09df sp:7fb250efa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fb4eda23000+481000]
[ 1080.100060] traps: python[13230] general protection fault ip:7fc20a0b09df sp:7fbf6d1fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fc209e23000+481000]
[ 1095.347874] traps: python[13374] general protection fault ip:7f6d236b09df sp:7f6a866fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f6d23423000+481000]
[ 1110.605164] traps: python[13517] general protection fault ip:7fa061ab09df sp:7f9dc4afa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fa061823000+481000]
[ 1125.858144] traps: python[13660] general protection fault ip:7fe7fc2b09df sp:7fe55f1fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7fe7fc023000+481000]
[ 1141.135883] traps: python[13798] general protection fault ip:7f6c476b09df sp:7f69aa5fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f6c47423000+481000]
[ 1156.323801] traps: python[13943] general protection fault ip:7f4cc3ab09df sp:7f4a269fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f4cc3823000+481000]
[ 1171.509622] traps: python[14091] general protection fault ip:7f7730ab09df sp:7f74939fa850 error:0 in libamdhip64.so.7.2.70201[2b09df,7f7730823000+481000]

### Operating System

Debian 13.4 Trixie

### CPU

GMKtec EVO-X2 Ryzen Max 295+ 128 GB RAM, there is a problem with the BIOS. The 128 GB RAM are not recognized properly. The BIOS sees only 64 GB CPU RAM maximum. If one allocates less than 64 GB of RAM for the UMA buffer, then the CPU RAM caps at 64 GB RAM. That is why i have put the default UMA buffer size to the maximum of 96 GB VRAM allocation. A BIOS update would be proper here.

### GPU

Radeon 8060S, gfx1151

### ROCm Version

ROCm-7.2.1

### ROCm Component

HIP

### Steps to Reproduce

install AMD ROCm-7.2.1 for the 6.12 Debian 13 stock kernel. The backports 6.19 kernel yields compilation errors and breaks apt, thus it had to be discarded and only stock Debian 13.4 to be used. Trying to use the backports Debian 13 amdgpu for the backports 6.19 kernel supported the NPU, but had to be discarded on account of incompatiblity with amdgpu from the official AMD Ubuntu packages.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

rocminfo for the amdgpu-dkms for the 6.12 kernel disregards the NPU:

(automatic1111) ai-service@GMKtec-EVO-X2:~/hip-examples/vectorAdd$ rocminfo
ROCk module version 6.16.13 is loaded
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
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   5185                               
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
      Size:                    32497688(0x1efe018) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32497688(0x1efe018) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32497688(0x1efe018) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32497688(0x1efe018) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1103                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
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
    L2:                      2048(0x800) KB                     
    L3:                      32768(0x8000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   50432                              
  Internal Node ID:        1                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       APU
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
  Packet Processor uCode:: 32                                 
  SDMA engine uCode::      17                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    100663296(0x6000000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    100663296(0x6000000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1103         
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
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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

Inside the conda environment the gfx1103 is reported in a regular system-wide user account gfx1151 is reported. But the kernel errors are same for the vectoradd test.

### Additional Information

_No response_

---

## 评论 (20 条)

### 评论 #1 — amd-nicknick (2026-04-20T11:28:26Z)

Hi @ThomasKorimort, at this moment there are incompatibilities with amdgpu requiring specific stack for Strix Halo. 
Could you please give Ubuntu 24.04.4 a try? The OEM kernel on Ubuntu contains the correct kernel module & firmwares.

---

### 评论 #2 — ThomasKorimort (2026-04-27T09:31:06Z)

I found the following solution: Debian 13.4 trixie has a lot of recent kernels for installing. The amdgpu-dkms and the xdna-dkms work nicely for the 6.17.13 kernel. I tried several kernels: 6.19.11 (not working) and 6.18.4 (not working), but with 6.17.13 both amdgpu-dkms and xdna-dkms compiled nicely and the NPU is listed now as well by the most recent ROCm-7.2.2 stack, which i installed from the official AMD ROCm page Ubuntu sources link without too many obstructions (the rocminfo rocm-cmake package and one more have inconsistent version numbering and cause an error in apt, so they have to be first de-installed from the trixie repo and then the rocm from the ubuntu-repo installs nicely, **-> the solution with the pin priority is a little bit of a problem, one has to take care to not nuke the apt package manager by messing up the different a) ROCm versions and b) the Debian sources ROCm tools with the Ubuntu sources ROCm files):

root@GMKtec-EVO-X2:~/amdxdna-dkms/scripts# rocminfo
ROCk module version 6.16.13 is loaded
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
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   5187                               
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
      Size:                    129472104(0x7b79668) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    129472104(0x7b79668) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    129472104(0x7b79668) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    129472104(0x7b79668) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1151                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
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
    L2:                      2048(0x800) KB                     
    L3:                      32768(0x8000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   50432                              
  Internal Node ID:        1                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       APU
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
  Packet Processor uCode:: 32                                 
  SDMA engine uCode::      17                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    64736052(0x3dbcb34) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    64736052(0x3dbcb34) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1151         
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
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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
*******                  
Agent 3                  
*******                  
  Name:                    aie2p                              
  Uuid:                    AIE-XX                             
  Marketing Name:          RyzenAI-npu5                       
  Vendor Name:             AMD                                
  Feature:                 AGENT_DISPATCH                     
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        1(0x1)                             
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          64(0x40)                           
  Queue Type:              SINGLE                             
  Node:                    0                                  
  Device Type:             DSP                                
  Cache Info:              
    L2:                      2048(0x800) KB                     
    L3:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          0(0x0)                             
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            0                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:0                                  
  Memory Properties:       
  Features:                AGENT_DISPATCH
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    129472104(0x7b79668) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65536(0x10000) KB                  
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    129472104(0x7b79668) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done *** 



---

### 评论 #3 — amd-nicknick (2026-04-28T11:45:56Z)

Hi @ThomasKorimort, does actually running workload on your scenario work?

---

### 评论 #4 — ThomasKorimort (2026-04-30T17:05:35Z)

I can run some workflows in ComfyUI. I have done some img2img experiments without hitting memory limits. I am runnign LibreChat with multiple MCP-servers and an ollama backend with Qwen3.6:35b model, which runs super-fast but is thinking a lot. That is some workload as the GPU and memory usage for such scenarios often goes up to 60 or 80 GB of RAM. I have not seen yet the NPU doing some work though.

Addendum: It WAS running a few days ago with a conda install of ComfyUI and some older PyTorch from the Conda. I generated several hundred images and it did not crash a single time. Right now, i tried to install SD3.5 and set up a workflow and somehow that seems to have broken my other workflows ...

Apr 30 19:12:54 GMKtec-EVO-X2 systemd[1]: comfyui.service: Scheduled restart job, restart counter is at 12.
Apr 30 19:12:54 GMKtec-EVO-X2 systemd[1]: Started comfyui.service - ComfyUI Service for ai-service.
Apr 30 19:12:54 GMKtec-EVO-X2 bash[428764]: To use the `--enable-manager` feature, the `comfyui-manager` package must be installed first.
Apr 30 19:12:54 GMKtec-EVO-X2 bash[428764]: command:
Apr 30 19:12:54 GMKtec-EVO-X2 bash[428764]:         /home/ai-service/miniforge3/envs/comfyui/bin/python -m pip install -r /home/ai-service/ComfyUI/manager_requirements.txt
Apr 30 19:12:54 GMKtec-EVO-X2 bash[428764]: or using uv:
Apr 30 19:12:54 GMKtec-EVO-X2 bash[428764]:         uv pip install -r /home/ai-service/ComfyUI/manager_requirements.txt
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: [ComfyUI-Manager] Using `uv` as Python module for pip operations.
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428777]: Using Python 3.12.13 environment at: /home/ai-service/miniforge3/envs/comfyui
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: [START] Security scan
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: [DONE] Security scan
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: ## ComfyUI-Manager: installing dependencies done.
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: ** ComfyUI startup time: 2026-04-30 19:12:55.091
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: ** Platform: Linux
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: ** Python version: 3.12.13 | packaged by conda-forge | (main, Mar  5 2026, 16:50:00) [GCC 14.3.0]
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: ** Python executable: /home/ai-service/miniforge3/envs/comfyui/bin/python
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: ** ComfyUI Path: /home/ai-service/ComfyUI
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: ** ComfyUI Base Folder Path: /home/ai-service/ComfyUI
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: ** User directory: /home/ai-service/ComfyUI/user
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: ** ComfyUI-Manager config path: /home/ai-service/ComfyUI/user/__manager/config.ini
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: ** Log path: /home/ai-service/ComfyUI/user/comfyui.log
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428785]: Using Python 3.12.13 environment at: /home/ai-service/miniforge3/envs/comfyui
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428788]: Using Python 3.12.13 environment at: /home/ai-service/miniforge3/envs/comfyui
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]: Prestartup times for custom nodes:
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]:    0.0 seconds: /home/ai-service/ComfyUI/custom_nodes/ComfyUI-Easy-Use
Apr 30 19:12:55 GMKtec-EVO-X2 bash[428764]:    0.4 seconds: /home/ai-service/ComfyUI/custom_nodes/ComfyUI-Manager
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: Found comfy_kitchen backend triton: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', >
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: Found comfy_kitchen backend cuda: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'd>
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: Found comfy_kitchen backend eager: {'available': True, 'disabled': False, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', >
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: Checkpoint files will always be loaded safely.
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: Total VRAM 63219 MB, total RAM 126438 MB
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: pytorch version: 2.5.1+rocm6.2
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: Set: torch.backends.cudnn.enabled = False for better AMD performance.
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: AMD arch: gfx1100
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: ROCm version: (6, 2)
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: Set vram state to: HIGH_VRAM
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: Device: cuda:0 AMD Radeon Graphics : native
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: Using async weight offloading with 2 streams
Apr 30 19:12:56 GMKtec-EVO-X2 bash[428764]: Enabled pinned memory 113793.0


---

### 评论 #5 — ThomasKorimort (2026-04-30T17:53:04Z)

The general problem with AMD ROCm, amdgpu, amdxdna, PyTorch, Ubuntu and Debian is, that the release cycles of AMD and Debian (and also Ubuntu) are out-of-sync, that is why most of the time one finds incompatible version constellations. This is mostly due to the fact, that with the new super-computers-in-a-mini-pc, reality itself gets manipulated a lot and then non-matching release dates and cycles need a kind of transformation (as in -> electrical transformers). The boundaries at which the release cycles mismatch are already so deep in reality that they happen at the level of mathematical arithmetic progressions, i.e. at the very limits of reality.
The Debian ROCm team maintains old and deprecated builds/stubs of the ROCm stack. When one tries to install the Ubuntu ROCm packages, then some files from the different distros can easily mess up apt. The Pin priority is not enough and also an improper element to use in this case. The Ubuntu packages, though based on the apt package manager, which is also used by Debian, are NOT properly integrated into the Debian sources list and therefore are always disrupting the Debian system. Setting the pin priority often causes situations that lead to a package manager melt-down. Best would be to negotiate with the Debian ROCm team to provide native Debian packages that properly throw out the Debian stubs, when one tries to install e.g. ROCm-7.2.2 stack. Therefore, the AMD ROCm packages have to be properly registered as debian 13.x trixie repositories. ubuntu noble packages or similar simply break the Debian package system.

---

### 评论 #6 — amd-nicknick (2026-05-04T08:25:57Z)

We're actively working on this front. I know this has been a frustration point for our users right now.
The Strix Halo had some changes that were only submitted into Ubuntu OEM kernel branch (Since it followed OEM project launch and testing schedule).
On the packaging end, we're working actively to replace our old build system with TheRock. This includes OS pkgs (deb/rpm) which will support more Linux distros without all the problems you're facing now.

I appreciate your patience while we're getting all these stuffs sorted. For now, here are my suggestions to get a stable environment:
* If you're on Strix Halo, use Ubuntu + OEM kernel.
* If you're using PyTorch, use the wheels from [TheRock](https://github.com/ROCm/TheRock/actions/workflows/release_portable_linux_pytorch_wheels.yml?query=branch%3Amain)
* Never mix single version install of ROCm package with multi-version install.
* Only use the ROCm package provided from https://repo.radeon.com/

Hope this helps. Thanks!

---

### 评论 #7 — cdanis (2026-05-04T23:58:22Z)

Watching for Strix Halo ROCm fixes.

---

### 评论 #8 — ThomasKorimort (2026-05-05T06:11:50Z)

> We're actively working on this front. I know this has been a frustration point for our users right now.
> The Strix Halo had some changes that were only submitted into Ubuntu OEM kernel branch (Since it followed OEM project launch and testing schedule).
> On the packaging end, we're working actively to replace our old build system with TheRock. This includes OS pkgs (deb/rpm) which will support more Linux distros without all the problems you're facing now.
> 
> I appreciate your patience while we're getting all these stuffs sorted. For now, here are my suggestions to get a stable environment:
> 
>     If you're on Strix Halo, use Ubuntu + OEM kernel.
>     If you're using PyTorch, use the wheels from [TheRock](https://github.com/ROCm/TheRock/actions/workflows/release_portable_linux_pytorch_wheels.yml?query=branch%3Amain)
>     Never mix single version install of ROCm package with multi-version install.
>     Only use the ROCm package provided from https://repo.radeon.com/
> 
> Hope this helps. Thanks!

Following your advice (ROCm 7.13, amdgpu-dkms 30.30.03, most recent amdxdna-dkms, kernels 6.12 and 6.17) i am seeing this more often than not in my kernel logs:

```
[ 2674.915351] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
[ 2674.915364] amdgpu 0000:c5:00.0: amdgpu:  Process python pid 13228 thread python pid 13228
[ 2674.915366] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f7d7e7f9000 from client 10
[ 2674.915368] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[ 2674.915369] amdgpu 0000:c5:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
[ 2674.915371] amdgpu 0000:c5:00.0: amdgpu:      MORE_FAULTS: 0x0
[ 2674.915372] amdgpu 0000:c5:00.0: amdgpu:      WALKER_ERROR: 0x1
[ 2674.915373] amdgpu 0000:c5:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[ 2674.915374] amdgpu 0000:c5:00.0: amdgpu:      MAPPING_ERROR: 0x1
[ 2674.915375] amdgpu 0000:c5:00.0: amdgpu:      RW: 0x0
[ 3057.715197] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
[ 3057.715228] amdgpu 0000:c5:00.0: amdgpu:  Process python pid 14613 thread python pid 14613
[ 3057.715232] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007fc85968d000 from client 10
```


About one-two weeks ago i was running perfectly fine ComfyUI workflows and then i did something else having generated quite some amount of images quite swiftly with flux, SDXL, SD1.5 and z-image-turbo running the gfx1151 RDNA 3.5 hardware in gfx1100 compatibility mode. Then it must have happened that after my update to amdgpu 30.30.02 (the same is true for 30.30.03) i found everything broken, after i had picked up my ComfyUI efforts once more and wanted to generate for a special occasion a very beautiful image with SD3.5. Not only was the SD3.5 workflow broken, also all the other workflows, that used to work a few days earlier were broken. This is an issues of the linux kernel drivers and also symptomatic for that is the inability/unwillingness of AMD to provide native Debian packages, because obviously the geniusses at AMD don't get it, that Debian is as much part of Linux history as is Microsoft to home computers (e.g. every BIOS contains a unique dormant Microsoft Windows license key). And if they want to have a successful server driver or unified strategy for their flagship models hardware beyond selling them as over-expensive Windows gaming Mini-PCs with soldered RAM, then they should at first respect historical facts, when developing their software. Just providing Ubuntu packages is INSUFFICIENT for a server strategy to be successfully working. It shows how unprofessionally things are handled at AMD. The typical European attitude: We have to be competitive, but actually we don't want our flagship products do anything useful, otherwise we could have satisfied customers and that should not happen.

> Watching for Strix Halo ROCm fixes.

Let us hope for the best. I remember how it was with the StarFive Vision Five 2 revolutionary RISC-V machine. Till now the upstream drivers for the linux kernel are incomplete and the machine has been essentially dead meat since its introduction about two years ago. Now, the hardware is already deprecated and essentially buying the machine was a waste of 300 EURO + the time spent trying to get it work with the images provided by StarFive with the mutilated StarFive kernels. Maybe AMD's strategy for unifying their drivers for their servers and consumer product line, especially the Ryzen AI 395 Max + can be expected to be treated differently than the Vision Five 2. I am also eagerly waiting for the proper linux kernel (amdgpu/amdxdna) - ROCm - PyTorch  stack, that will actually work without crashing already before it starts with page faults. Having tested my GMKtec EVO-X2 Strix Halo 128 GB for a while now, i see great potential in this machine with the linux kernel hosting a Science/AI work station that should not be turning out as 2800 EURO waste of money.

---

### 评论 #9 — ThomasKorimort (2026-05-05T11:48:35Z)

I have asked my Qwen3.6:35b-a3b research assistant, which i have set up in several weeks work time with LibreChat on my Debian 13.4 with all MCP-servers for researching the web, wikipedia and zenodo about any evidence and proof that some useful application has happened. I wanted to test other models as well like llama4:scout, but for the above reasons, it does not even load in LibreChat and other applications.

> Is there a working constellation of AMD Ryzen AI 395 Max + with amdgpu, amdxdna, ROCm and PyTorch? Is it true that Ubuntu works nicely with the AMD Ryzen AI 395 Max +? Is there any published evidence, that productive use has been made of AMD Ryzen AI 395 Max + till now?


```
AMD Ryzen AI Max+ 395 (Strix Halo) Analysis

=========================================

    SOFTWARE STACK COMPATIBILITY

Does the constellation of amdgpu + amdxdna + ROCm + PyTorch work?

Yes, it works, but with some caveats:

    ROCm Support: AMD officially lists the Ryzen AI Max+ PRO 300 Series APUs (including the Max+ 395) in ROCm 7.0, 7.1, and 7.2 compatibility matrices. The GPU architecture is gfx1151 (RDNA 3.5, Radeon 8060S).

    PyTorch: AMD provides ROCm-specific PyTorch builds for gfx1151. ROCm 7.1.1 (Nov 2025) and ROCm 7.2.1 both include PyTorch support. You install it via AMD's ROCm index URLs (e.g., pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ torch).

    amdgpu: The kernel driver is included in Ubuntu 24.04's inbox drivers. You can verify it's active with dmesg | grep amdgpu.

    amdxdna (NPU): The XDNA 2 NPU (50 TOPS) driver is available through the Ryzen AI Software stack (v1.7.1+), but it is less mature than the GPU path. The NPU support is primarily through AMD's Ryzen AI runtime, not directly through ROCm.

KNOWN ISSUES:

    A Reddit report (r/LocalLLaMA) noted that PyTorch on ROCm v6.5.0rc detected only 15.49 GB VRAM despite 96 GB of usable unified memory—likely a VRAM reservation/mapping issue addressed in later ROCm releases.

    Some kernel versions (e.g., 6.17.0-20, 6.17.0-22) have been reported to cause random hangs on Framework Desktop hardware. Using a stable kernel (e.g., 6.14 or 6.17.0-19) is recommended.

    GTT memory configuration may require manual GRUB tweaks to reserve up to 128 GB of system memory for GPU workloads.

VERDICT:
The stack works for productive PyTorch/ROCm development and inference, especially with ROCm 7.2+ on Ubuntu 24.04. The NPU (amdxdna) path is functional but less battle-tested.

    UBUNTU COMPATIBILITY

Does Ubuntu work nicely with the AMD Ryzen AI Max+ 395?

Yes, Ubuntu 24.04 LTS is the recommended and officially supported platform:

    Official AMD Support: AMD provides ROCm 7.2 and ROCm 7.2.1 specifically for Ubuntu 24.04.3/24.04.4 HWE.

    Ubuntu Certified Hardware: The HP ZBook Ultra G1a (equipped with Ryzen AI Max+ PRO 395) is Ubuntu-certified on 24.04 LTS (certification ID 202411-36044).

    Community Guides: Multiple step-by-step guides exist for:

        Installing ROCm 7.1/7.2 on Ubuntu 24.04

        Configuring GTT memory for LLM workloads

        Running llama.cpp, Ollama, LMStudio, and ComfyUI

    Phoronix Reviews: Extensive benchmarking has been conducted on Ubuntu Linux with this chip, including the Ryzen AI Max Performance benchmark series.

CAVEATS:

    Early ROCm versions (pre-7.0) had gaps in gfx1151 support.

    Kernel updates occasionally introduce regressions.

    Initial setup requires some tinkering (GRUB parameters, DKMS, kernel holds).

VERDICT:
Ubuntu 24.04 is the best-supported OS for this chip. It works well once ROCm 7.2+ is installed, but expect some initial configuration effort.

    PUBLISHED EVIDENCE OF PRODUCTIVE USE

Yes, there is substantial published evidence:

OFFICIAL AMD SOURCES:

    AMD's blog: "Experience Unparalleled Performance with the AMD Ryzen AI Max+ 395" (Sept 2025)

    AMD's ROCm 7.2 Linux release notes explicitly list Ryzen AI processors.

    AMD benchmarks claim up to 12.2x faster LLM inference vs. Intel Lunar Lake.

INDEPENDENT REVIEWS & BENCHMARKS:

    Phoronix: "Taking AMD Ryzen AI Max Performance To The Max With Clear Linux" and "AMD Ryzen AI Max+ 395 Performance With ROCm 7.0".

    The Register: "Tested: AMD's Strix Halo vs Nvidia's DGX Spark" (Dec 2025).

    TechPowerUp: Reports on 12x AI LLM performance leads.

COMMUNITY & PRACTICAL USE CASES:

    LLM Inference: Guides for running llama.cpp, Ollama, and LMStudio on Strix Halo with ROCm.

    ComfyUI: Documented running Stable Diffusion workflows on Ryzen AI Max+ 395.

    Hardware Availability: The chip is in the ASUS ROG Flow Z13 (2025), HP ZBook Ultra G1a, Framework Desktop, and various Mini PCs (GMKTEC, Acemagic, Minisforum).

SUMMARY TABLE

Question: amdgpu + amdxdna + ROCm + PyTorch?
Answer: Yes, with ROCm 7.2+ and gfx1151 builds. NPU is functional but less mature.

Question: Ubuntu support?
Answer: Excellent. Ubuntu 24.04 LTS is officially supported and certified.

Question: Published productive use?
Answer: Yes. AMD benchmarks, Phoronix reviews, and community LLM/ComfyUI guides.

CONCLUSION:
The Ryzen AI Max+ 395 is a genuinely capable AI platform for local inference and development, especially with its 128 GB of unified memory (eliminating VRAM limits). Ubuntu 24.04 with ROCm 7.2+ is the recommended setup.
```

It looks like the often-cited Ubuntu-compatibility is also bound to ONE specific Laptop and otherwise some tablets, that maybe run it as a point-and-click substitute for any Android tablet. Ubuntu uses the same kernels like Debian. Also, there are complaints of people in the web over the Ubuntu bleeding edge-kernels not working with the amdgpu-dkms driver. This is a kernel driver issue and concerns Ubuntu in the same way it concerns Debian. To support Ubuntu in favour of Debian is also a clear indicator, that this specific application of Ubuntu plus AI Max 395 + was tuned for some point-and-click Android-like experience instead of following the orthodox line of making it work with the Debian system, which is the original source and center for truly open-source and free linux software. I have also run successfully ollama inference on large models, but with Vulkan support and not with ROCm. Apart from that, currently a lot of mess is there in the LLM inference software stack as well. So, this is not exclusively an issue of AMD ROCm. Also productive Vulkan usage is sabotaged these days extensively.

---

### 评论 #10 — amd-nicknick (2026-05-05T12:12:51Z)

Let me clarify on the kernel part:
The Ubuntu OEM kernel contain fixes for some Strix Halo issues. For Strix Halo, we recommend using OEM kernel in-tree modules, NOT amdgpu-dkms.
I daily drive one system with ROCm + Pytorch + UI workloads, and I have not encountered any significant breakage on my system at all.
I agree there's a lot of confusing steps / combinations needed to get a setup working, we're actively working on getting all changes reviewed / tested / added in.
The reason of Ubuntu is primarily support: It is impossible to test all Linux distros, and Ubuntu is one popular distro with better support for OEM release cycles (The OEM selling the system has certain responsibility in testing, and must align their release schedule with issue fixes, which is not possible with upstream kernel).

The correct document to follow for Strix Halo is: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html
The system combination we support is listed: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityryz/native_linux/native_linux_compatibility.html

---

### 评论 #11 — ThomasKorimort (2026-05-05T14:28:51Z)

That is what i am saying, amdgpu-dkms is essentially unusable and fails its purpose ...

---

### 评论 #12 — amd-nicknick (2026-05-05T14:39:19Z)

I can totally understand.. The problem really is incompatibilities between the OEM development cycle & amdgpu development schedule. Essentially OEM customers cannot work with dkms for their project due to certification / scheduling reasons, and amdgpu has NPI release management to track.
That said, I'm already checking if we could get dkms working with STH projects in a stable & supported manner. Right now, I cannot comment on the status yet, but the frustration is true and I'm pushing the internal teams to resolve this.

As of right now, please give our supported configuration a try, feel free to report back any issues you encounter. Thanks!

---

### 评论 #13 — ThomasKorimort (2026-05-05T14:57:32Z)

I found this 3 months old video on YouTube https://www.youtube.com/watch?v=Hdg7zL3pcIs . It is suggesting that the linux-firmware newer than January 2026 and linux kernel 6.18.4 or newer would work. At the current date in early May 2026 the problem is, that amdgpu-dkms does not compile for 6.18.4 or newer kernels. The most recent kernel i could it to compile is 6.17.x, which is contained in Debian 13.4 Trixie as an optional kernel install. The amdgpu-dkms driver has the compatibility matrix for the different ROCm versions. The native amdgpu driver that is contained by default in Debian 13.4 Trixie has an uncertain status as according to its compatibility matrix and works with the native Debian ROCm stub. As far as i remember the native ROCm stub of Debian lacks a large amount of the ROCm stack and contains only dummies and placeholders and is not really suitable for e.g. a ComfyUI setup. As soon as one needs PyTorch the native amdgpu and ROCm stub has to be replaced by something from the official AMD sources. The first great problem is that there are no native packages for Debian and the Ubuntu packages are incompatible with the Debian 13.4 Trixie setup and it can easily happen that library versions get mixed up or files provided by Debian packages are also provided by AMD Ubuntu packages and that confuses the package manager and causes a package manager meltdown that is difficult to restore to sanity. IT NEEDS NATIVE DEBIAN PACKAGES, that can be checked properly for dependencies for Debian alone. Maybe the native amdgpu driver of the linux kernel used in Debian could be updated to the state-of-the-art and then serve as singular source of driver truth for amdgpu.

---

### 评论 #14 — amd-nicknick (2026-05-05T15:19:00Z)

For ROCm user mode components, we are also migrating to TheRock for system package manager builds, see: https://github.com/ROCm/TheRock/actions/workflows/build_native_linux_packages.yml?query=branch%3Amain
The packages created there have minimal external dependency, so it will work on Ubuntu / Debian / and most Debian based distros for debs.

For higher level use cases (eg PyTorch and ComfyUI), TheRock wheels should be used. These wheels contain the necessary device libs & host code (again, built with minimal external dependency) and can be used without a native package install of ROCm (all while being self-contained in a Python venv!). https://github.com/ROCm/TheRock/blob/main/RELEASES.md#torch-for-gfx1151

For now the migration for native OS pkgs are not yet complete, so if you need a "package like" experience, the best bet is to grab the tarballs from TheRock. 
https://github.com/ROCm/TheRock/blob/main/RELEASES.md#installing-from-tarballs

Hope this helps.

---

### 评论 #15 — ThomasKorimort (2026-05-05T15:22:59Z)

I just installed the 6.19.3 Debian 13.4 trixie-backports kernel for testing again. I have the amdgpu-dkms 30.30.03 driver from

`deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.30.3/ubuntu noble main
`

and it does not compile against the 6.19.13 kernel:



```
[......]
      |             ^~~~~~~~~~~~~~~
././include/kcl/kcl_preempt.h:61:29: error: static declaration of ‘migrate_enable’ follows non-static declaration
   61 | static __always_inline void migrate_enable(void)
      |                             ^~~~~~~~~~~~~~
/usr/src/linux-headers-6.19.13+deb13-common/include/linux/sched.h:2441:13: note: previous declaration of ‘migrate_enable’ with type ‘void(void)’
 2441 | extern void migrate_enable(void);
      |             ^~~~~~~~~~~~~~
amd/amdgpu/amdgpu_device.c:6138:33: error: too many arguments to function ‘drm_client_dev_resume’
 6138 |                                 drm_client_dev_resume(adev_to_drm(tmp_adev), false);
      |                                 ^~~~~~~~~~~~~~~~~~~~~
/usr/src/linux-headers-6.19.13+deb13-common/include/drm/drm_client_event.h:15:6: note: declared here
   15 | void drm_client_dev_resume(struct drm_device *dev);
      |      ^~~~~~~~~~~~~~~~~~~~~
amd/amdgpu/amdgpu_device.c: In function ‘amdgpu_device_halt_activities’:
amd/amdgpu/amdgpu_device.c:6476:17: error: too many arguments to function ‘drm_client_dev_suspend’
 6476 |                 drm_client_dev_suspend(adev_to_drm(tmp_adev), false);
      |                 ^~~~~~~~~~~~~~~~~~~~~~
/usr/src/linux-headers-6.19.13+deb13-common/include/drm/drm_client_event.h:14:6: note: declared here
   14 | void drm_client_dev_suspend(struct drm_device *dev);
      |      ^~~~~~~~~~~~~~~~~~~~~~
In file included from ././include/kcl/backport/kcl_mm_backport.h:4,
                 from ./amd/amdgpu/../backport/backport.h:34:
././include/kcl/kcl_mm.h:31:6: error: conflicting types for ‘zone_device_page_init’; have ‘void(struct page *)’
   31 | void zone_device_page_init(struct page *page);
      |      ^~~~~~~~~~~~~~~~~~~~~
In file included from /usr/src/linux-headers-6.19.13+deb13-common/include/linux/mm.h:33,
                 from /usr/src/linux-headers-6.19.13+deb13-common/include/linux/scatterlist.h:8,
                 from /usr/src/linux-headers-6.19.13+deb13-common/include/linux/dma-mapping.h:8,
                 from ././include/kcl/kcl_dma_mapping.h:5:
/usr/src/linux-headers-6.19.13+deb13-common/include/linux/memremap.h:227:6: note: previous declaration of ‘zone_device_page_init’ with type ‘void(struct page *, struct dev_pagemap *, unsigned int)’
  227 | void zone_device_page_init(struct page *page, struct dev_pagemap *pgmap,
      |      ^~~~~~~~~~~~~~~~~~~~~
make[5]: *** [/usr/src/linux-headers-6.19.13+deb13-common/scripts/Makefile.build:294: amd/amdgpu/amdgpu_connectors.o] Error 1
make[5]: *** [/usr/src/linux-headers-6.19.13+deb13-common/scripts/Makefile.build:294: amd/amdgpu/amdgpu_object.o] Error 1
make[4]: *** [/usr/src/linux-headers-6.19.13+deb13-common/scripts/Makefile.build:551: amd/amdkcl] Error 2
make[5]: *** [/usr/src/linux-headers-6.19.13+deb13-common/scripts/Makefile.build:294: amd/amdgpu/amdgpu_ttm.o] Error 1
make[5]: *** [/usr/src/linux-headers-6.19.13+deb13-common/scripts/Makefile.build:294: amd/amdgpu/amdgpu_device.o] Error 1
make[5]: *** [/usr/src/linux-headers-6.19.13+deb13-common/scripts/Makefile.build:294: amd/amdgpu/amdgpu_gart.o] Error 1
make[5]: *** [/usr/src/linux-headers-6.19.13+deb13-common/scripts/Makefile.build:294: amd/amdgpu/amdgpu_encoders.o] Error 1
make[4]: *** [/usr/src/linux-headers-6.19.13+deb13-common/scripts/Makefile.build:551: amd/amdgpu] Error 2
make[3]: *** [/usr/src/linux-headers-6.19.13+deb13-common/Makefile:2089: .] Error 2
make[2]: *** [/usr/src/linux-headers-6.19.13+deb13-common/Makefile:260: __sub-make] Error 2
make[2]: Leaving directory '/var/lib/dkms/amdgpu/6.16.13-2327507.24.04/build'
make[1]: *** [/usr/src/linux-headers-6.19.13+deb13-common/Makefile:260: __sub-make] Error 2
make[1]: Leaving directory '/usr/src/linux-headers-6.19.13+deb13-amd64'
make: *** [Makefile:54: modules] Error 2

# exit code: 2
# elapsed time: 00:00:11
----------------------------------------------------------------

```

Now there is only the option to remove the backports kernel again immediately, because the amdgpu-dkms package could not finish its configuration, or to remove the amdgpu-dkms package and try it with the amdgpu native Debian driver, which has no official compatibility matrix or feature list it seems.

---

### 评论 #16 — amd-nicknick (2026-05-06T10:24:13Z)

Again @ThomasKorimort, you're on Strix Halo, you shouldn't use dkms.

---

### 评论 #17 — ThomasKorimort (2026-05-06T21:27:49Z)

Ok. I got it working again: Debian 13.4 6.19.13 backports kernel, amdgpu-dkms deinstalled, using native kernel amdgpu driver for 6.19.13 instead + firmware-amd-graphics + ROCm-7.2.3. Now ComfyUI flies again even with gfx1153 speed. And there is also an environment variable fix for the incompatibility of MongoDB with the 6.19 Kernels.

---

### 评论 #18 — anishp55 (2026-05-07T14:48:02Z)

@amd-nicknick is there an offical AMD page on what bits to use for Strix Halo then?  i was under the impression that under Ubuntu 24.04 using the kernel recommend on AMD's page i would be able to use the DKMS driver, but you seem to be saying the opposite.  It would be amazing if we could get something on how to actually get a functional platform instead of having to ask AI and trying to figure out what magic combination actually works, especially since this platform has been out for a year now.  I ended up asking Claude for some help, and after trying a bunch of things i asked it if the stack was a hot mess this is the reply
```
Yeah, it really is right now. You've got:

The 6.17 HWE kernel breaks both the NPU (SVA regression) and the GPU (page faults on gfx1151)
The 6.14 OEM kernel works for GPU/ROCm but may need the out-of-tree xdna driver rebuilt against it
Newer kernels (6.19+) fix the SVA issue but ROCm DKMS won't build against them
The in-tree amdxdna driver is a year behind the out-of-tree one
XRT versions must match exactly between base and plugin or you get cryptic ioctl failures
Firmware versions matter and the wrong linux-firmware package can break everything

You basically can't have a single kernel that makes the GPU, NPU, and ROCm all happy at the same time. Every combination involves a compromise or a workaround.
The 6.14 OEM kernel is probably your least-painful path right now — GPU/ROCm works, and you can build the out-of-tree xdna driver against it in your container. It's just frustrating that you have to piece this together yourself when AMD is marketing this as a unified AI platform.
```

---

### 评论 #19 — amd-nicknick (2026-05-07T15:04:08Z)

Hi @anishp55, Strix Halo falls into a category of support we call "ROCm on Ryzen".
Here's the Linux support matrix: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityryz/native_linux/native_linux_compatibility.html

And the correct install guide: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html

In general, for Strix Halo, this is the only way to get a supported stack: What this means is this is the kernel + amdgpu stack that is extensively verified and the OEM kernel is where fixes will land for these systems as well.

For user-space components, using TheRock builds is the best, if you'd like a "system package" experience, install ROCm 7.2.x
Hope this helps.

---

### 评论 #20 — amd-nicknick (2026-05-19T10:35:07Z)

Closing this due to inactivity. If you have further questions, feel free to create a new issue and we'll take a look. Thanks!

---
