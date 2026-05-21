# Rocm unable to detect GPU (Warn: GPU not getting identified)

> **Issue #2995**
> **状态**: closed
> **创建时间**: 2024-04-04T11:07:06Z
> **更新时间**: 2025-03-21T17:56:03Z
> **关闭时间**: 2025-03-21T17:56:02Z
> **作者**: anoopsinghnegi
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2995

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

We have installed the Rocm packages but it is unable to recognize the GPU. We have followed https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html to install the Rocm software.

"rocm-smi" returns WARNING: No AMD GPUs specified

GPU type: [Radeon Pro V620 MxGPU]
OS: Rhel 8.9

```
[root@amd-gpu ]# cat /etc/*release* | grep -i version
VERSION="8.9 (Ootpa)"
VERSION_ID="8.9"
REDHAT_BUGZILLA_PRODUCT_VERSION=8.9
REDHAT_SUPPORT_PRODUCT_VERSION="8.9"

[root@amd-gpu]# lspci -nn | grep -i amd
0002:00:00.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] Navi 21 [Radeon Pro V620 MxGPU] [1002:73ae]

```

after the installation, we rebooted the VM and when we ran "rocminfo" it failed with an error "Rock module not loaded"
```
[root@amd-gpu]# rocminfo
ROCk module is NOT loaded, possibly no GPU devices
[root@amd-gpu]#
```
then we added the module manually by running "**modprobe amdgpu**" The earlier issue was solved but it is unable to detect the GPU.
```
[root@amd-gpu]# modprobe amdgpu
[root@amd-gpu]# rocminfo
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD EPYC 7763 64-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 7763 64-Core Processor
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
  Max Clock Freq. (MHz):   0
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            8
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    16074216(0xf545e8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16074216(0xf545e8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16074216(0xf545e8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***

[root@amd-gpu]# rocminfo | grep -i gfx
[root@amd-gpu]# rocminfo | grep -i gpu
[root@amd-gpu]#
```
rocm-smi output
```
[root@amd-gpu]# rocm-smi


WARNING: No AMD GPUs specified
=================================== ROCm System Management Interface ===================================
============================================= Concise Info =============================================
Device  [Model : Revision]  Temp    Power  Partitions      SCLK  MCLK  Fan  Perf  PwrCap  VRAM%  GPU%
        Name (20 chars)     (Edge)  (Avg)  (Mem, Compute)
========================================================================================================
========================================================================================================
========================================= End of ROCm SMI Log ==========================================
[root@amd-gpu]#
```
amdgpu module was loaded but still GPU is unidentified.
```
[root@amd-gpu]# lsmod | grep amdgpu
amdgpu              11243520  0
amddrm_ttm_helper      16384  1 amdgpu
amdttm                 77824  2 amdgpu,amddrm_ttm_helper
amdxcp                 16384  1 amdgpu
amddrm_buddy           20480  1 amdgpu
amd_sched              45056  1 amdgpu
amdkcl                 36864  3 amd_sched,amdttm,amdgpu
video                  53248  1 amdgpu
i2c_algo_bit           16384  1 amdgpu
drm_display_helper    155648  1 amdgpu
drm_kms_helper        184320  2 drm_display_helper,amdgpu
drm                   602112  9 drm_kms_helper,amd_sched,amdttm,drm_display_helper,amdgpu,amddrm_buddy,amdkcl,amddrm_ttm_helper,amdxcp
[root@amd-gpu]#
```

We are planning to consume GPU by running pytorch application but since the driver is unable to recognise the GPU we are stuck and now looking for quick support, let us know if any further logs are needed.


---

## 评论 (26 条)

### 评论 #1 — kentrussell (2024-04-04T13:20:24Z)

A full dmesg and the output of "dkms status" would be the first step in seeing why the kernel didn't initialize the GPU

---

### 评论 #2 — anoopsinghnegi (2024-04-04T13:28:35Z)

@kentrussell - thanks, below are the capture logs, many errors are showing for admgpu in dmesg logs 
```
[root@amd-gpu]# dmesg | grep -i amdgpu
[  602.598995] [drm] amdgpu kernel modesetting enabled.
[  602.598998] [drm] amdgpu version: 6.3.6
[  602.599236] amdgpu: Virtual CRAT table created for CPU
[  602.599257] amdgpu: Topology: Add CPU node
[  602.604280] amdgpu 0002:00:00.0: enabling device (0000 -> 0002)
[  602.942000] [drm] add ip block number 5 <amdgpu_vkms>
[  602.955113] amdgpu 0002:00:00.0: amdgpu: Fetched VBIOS from VRAM BAR
[  602.955117] amdgpu: ATOM BIOS: 113-D6030120-104
[  602.955662] amdgpu 0002:00:00.0: amdgpu: Trusted Memory Zone (TMZ) feature disabled as experimental (default)
[  602.955705] amdgpu 0002:00:00.0: amdgpu: VRAM: 7568M 0x0000008000000000 - 0x00000081D8FFFFFF (7568M used)
[  602.955708] amdgpu 0002:00:00.0: amdgpu: GART: 512M 0x0000000000000000 - 0x000000001FFFFFFF
[  602.955880] [drm] amdgpu: 7568M of VRAM memory ready
[  602.955882] [drm] amdgpu: 7848M of GTT memory ready.
[  602.962054] amdgpu 0002:00:00.0: amdgpu: Will use PSP to load VCN firmware
[  603.029519] [drm:psp_hw_init [amdgpu]] *ERROR* PSP firmware loading failed
[  603.029706] [drm:amdgpu_device_ip_init [amdgpu]] *ERROR* hw_init of IP block <psp> failed -22
[  603.029902] amdgpu 0002:00:00.0: amdgpu: amdgpu_device_ip_init failed
[  603.039912] amdgpu 0002:00:00.0: amdgpu: Fatal error during GPU init
[  603.039915] amdgpu 0002:00:00.0: amdgpu: amdgpu: finishing device.
[  603.596660] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.596865] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.596954] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.597123]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.597264]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.597418]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.597561]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.597700]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.597838]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.597980]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.598160]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.598330]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.598513] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.598668] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.598750] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.598924]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.599077]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.599238]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.599406]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.599556]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.599706]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.599859]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.600051]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.600235]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.600425] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.600588] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.600669] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.600843]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.600995]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.601155]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.601312]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.601462]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.601611]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.601764]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.601960]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.602143]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.602335] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.602498] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.602578] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.602751]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.602903]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.603064]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.603218]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.603371]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.603528]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.603681]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.603872]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.604056]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.604246] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.604415] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.604496] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.604668]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.604820]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.604981]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.605135]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.605287]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.605446]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.605598]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.605790]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.605974]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.606165] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.606330] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.606410] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.606583]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.606734]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.606895]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.607049]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.607199]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.607358]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.607523]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.607715]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.607898]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.608088] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.608250] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.608333] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.608506]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.608657]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.608817]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.608971]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.609121]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.609271]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.609423]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.609613]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.609796]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.609987] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.610149] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.610230] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.610405]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.610556]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.610716]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.610870]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.611020]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.611170]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.611323]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.611518]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.611700]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.611891] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.612054] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.612134] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.612310]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.612461]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.612621]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.612775]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.612925]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.613074]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.613227]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.613416]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.613598]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.613790] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.613953] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.614034] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.614207]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.614360]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.614521]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.614675]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.614825]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.614975]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.615128]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.615320]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.615510]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.615702] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.615870] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.615950] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.616123]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.616275]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.616438]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.616592]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.616742]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.616891]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.617043]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.617234]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.617418]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.617609] WARNING: CPU: 0 PID: 301 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.617772] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod
[  603.617852] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.618025]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.618176]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.618339]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.618493]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[  603.618644]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[  603.618795]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[  603.618947]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[  603.619136]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[  603.619320]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[  603.625089] amdgpu: probe of 0002:00:00.0 failed with error -22
[  603.691429] [drm] amdgpu: ttm finalized
[  603.691435] amdgpu: legacy kernel without apple_gmux_detect()
[10500.473882] [drm] amdgpu kernel modesetting enabled.
[10500.473885] [drm] amdgpu version: 6.3.6
[10500.474005] amdgpu: Virtual CRAT table created for CPU
[10500.474022] amdgpu: Topology: Add CPU node
[10500.493808] [drm] add ip block number 5 <amdgpu_vkms>
[10500.506876] amdgpu 0002:00:00.0: amdgpu: Fetched VBIOS from VRAM BAR
[10500.506880] amdgpu: ATOM BIOS: 113-D6030120-104
[10500.507325] amdgpu 0002:00:00.0: amdgpu: Trusted Memory Zone (TMZ) feature disabled as experimental (default)
[10500.507374] amdgpu 0002:00:00.0: amdgpu: VRAM: 7568M 0x0000008000000000 - 0x00000081D8FFFFFF (7568M used)
[10500.507378] amdgpu 0002:00:00.0: amdgpu: GART: 512M 0x0000000000000000 - 0x000000001FFFFFFF
[10500.507568] [drm] amdgpu: 7568M of VRAM memory ready
[10500.507570] [drm] amdgpu: 7848M of GTT memory ready.
[10500.513548] amdgpu 0002:00:00.0: amdgpu: Will use PSP to load VCN firmware
[10500.580947] [drm:psp_hw_init [amdgpu]] *ERROR* PSP firmware loading failed
[10500.581135] [drm:amdgpu_device_ip_init [amdgpu]] *ERROR* hw_init of IP block <psp> failed -22
[10500.581332] amdgpu 0002:00:00.0: amdgpu: amdgpu_device_ip_init failed
[10500.591341] amdgpu 0002:00:00.0: amdgpu: Fatal error during GPU init
[10500.591344] amdgpu 0002:00:00.0: amdgpu: amdgpu: finishing device.
[10501.148280] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.148511] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.148656] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.148940]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.149087]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.149238]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.149379]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.149518]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.149656]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.149798]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.149978]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.150148]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.150331] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.150484] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.150560] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.150721]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.150860]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.151015]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.151163]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.151301]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.151439]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.151579]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.151756]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.151925]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.152100] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.152250] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.152326] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.152486]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.152626]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.152773]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.152917]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.153060]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.153218]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.153370]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.153564]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.153790]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.153986] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.154149] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.154231] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.154403]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.154557]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.154740]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.154884]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.155035]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.155181]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.155321]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.155495]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.155664]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.155839] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.155991] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.156066] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.156225]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.156364]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.156512]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.156653]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.156791]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.156936]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.157087]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.157280]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.157463]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.157655] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.157817] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.157898] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.158073]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.158224]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.158384]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.158537]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.158687]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.158836]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.158996]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.159187]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.159370]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.159560] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.159730] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.159812] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.159987]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.160138]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.160298]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.160451]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.160614]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.160785]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.160925]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.161100]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.161269]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.161445] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.161595] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.161670] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.161829]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.161971]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.162118]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.162260]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.162398]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.162535]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.162675]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.162860]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.163033]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.163222] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.163385] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.163466] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.163657]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.163832]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.164000]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.164153]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.164303]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.164453]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.164612]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.164816]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.164985]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.165160] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.165310] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.165385] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.165545]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.165684]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.165831]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.165974]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.166112]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.166250]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.166390]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.166565]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.166733]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.166909] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.167068] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.167143] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.167304]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.167443]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.167597]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.167765]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.167910]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.168051]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.168191]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.168366]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.168535]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.168742] WARNING: CPU: 0 PID: 10633 at /var/lib/dkms/amdgpu/6.3.6-1718217.el8/build/amd/amdgpu/amdgpu_irq.c:627 amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.168899] Modules linked in: amdgpu(OE+) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) video i2c_algo_bit drm_display_helper drm_kms_helper syscopyarea sysfillrect sysimgblt drm nft_counter xt_conntrack xt_owner nft_compat nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet ext4 nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct mbcache jbd2 nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 ip_set nf_tables nfnetlink vfat fat mlx5_ib intel_rapl_msr intel_rapl_common ib_uverbs amd_energy crct10dif_pclmul crc32_pclmul ib_core ghash_clmulni_intel pcspkr hyperv_fb hv_balloon hv_utils joydev xfs libcrc32c mlx5_core mlxfw tls psample nvme nvme_core sr_mod cdrom sd_mod t10_pi sg hv_netvsc serio_raw hv_storvsc pci_hyperv scsi_transport_fc pci_hyperv_intf hid_hyperv hyperv_keyboard hv_vmbus crc32c_intel dm_mirror dm_region_hash dm_log dm_mod [last unloaded: amdgpu]
[10501.168980] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.169140]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.169279]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.169426]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.169567]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[10501.169706]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[10501.169843]  amdgpu_fence_driver_hw_fini+0xd8/0x100 [amdgpu]
[10501.169982]  amdgpu_device_fini_hw+0xac/0x2b1 [amdgpu]
[10501.170157]  amdgpu_driver_load_kms.cold.14+0x54/0x6a [amdgpu]
[10501.170326]  amdgpu_pci_probe+0x178/0x3d0 [amdgpu]
[10501.176034] amdgpu: probe of 0002:00:00.0 failed with error -22
[10501.242172] [drm] amdgpu: ttm finalized
[10501.242177] amdgpu: legacy kernel without apple_gmux_detect()
[root@amd-gpu]#
```

```
[root@amd-gpu]# dkms status
amdgpu/6.3.6-1718217.el8, 4.18.0-513.24.1.el8_9.x86_64, x86_64: installed (original_module exists)
[root@amd-gpu]#
```

---

### 评论 #3 — kentrussell (2024-04-04T13:53:05Z)

[  603.029519] [drm:psp_hw_init [amdgpu]] *ERROR* PSP firmware loading failed
[  603.029706] [drm:amdgpu_device_ip_init [amdgpu]] *ERROR* hw_init of IP block <psp> failed -22
[  603.029902] amdgpu 0002:00:00.0: amdgpu: amdgpu_device_ip_init failed
[  603.039912] amdgpu 0002:00:00.0: amdgpu: Fatal error during GPU init
[  603.039915] amdgpu 0002:00:00.0: amdgpu: amdgpu: finishing device.

So the PSP firmware couldn't load. Best suggestion for that is updating the VBIOS/IFWI to the latest release , and ensuring that amdgpu-dkms-firmware got installed successfully.

EDIT: So I just checked, and the VBIOS is reported as the latest one (-104) for that card, so I think that reinstalling the amdgpu-dkms-firmware package would be the best next step. Otherwise we'd need someone on the PSP team to take a look to figure out what's up

---

### 评论 #4 — anoopsinghnegi (2024-04-04T14:09:50Z)

@kentrussell, this VM instance is a GPU-enabled virtual machine (NGads series) from Azure.
ok, we will try reinstalling the package.

---

### 评论 #5 — anoopsinghnegi (2024-04-04T15:48:26Z)

it didn't work, same result after reinstallation.
```
uninstall => amdgpu-uninstall
install => amdgpu-install --usecase=rocm
```


---

### 评论 #6 — kentrussell (2024-04-04T16:18:39Z)

Can you return the output for 
dpkg -l|grep amdgpu-dkms
or
rpm -qa|grep amdgpu-dkms
? Depending on the system, of course. 

---

### 评论 #7 — anoopsinghnegi (2024-04-04T16:29:34Z)

[root@amd-gpu ~]# rpm -qa|grep amdgpu-dkms
amdgpu-dkms-firmware-6.3.6.60002-1718217.el8.noarch
amdgpu-dkms-6.3.6.60002-1718217.el8.noarch


---

### 评论 #8 — kentrussell (2024-04-04T16:34:52Z)

@nartmada I think we can make a ticket for this and assign it to the PSP team, they can hopefully help figure out what's going wrong here

---

### 评论 #9 — nartmada (2024-04-04T21:40:46Z)

@kentrussell, an internal ticket has been created for investigation.

---

### 评论 #10 — anoopsinghnegi (2024-04-12T05:47:40Z)

@nartmada - any update on this? we are blocked because of this issue.

---

### 评论 #11 — nartmada (2024-04-12T14:39:49Z)

@anoopsinghnegi, I am chasing the PSP team for update.

---

### 评论 #12 — nartmada (2024-04-18T04:13:35Z)

@anoopsinghnegi, would you be able to try ROCm 6.1.0 while I am still sorting the details with the PSP team.  Thanks.

---

### 评论 #13 — anoopsinghnegi (2024-04-18T13:36:25Z)

@nartmada - we upgraded the ROCm to 6.1.0 but r**ocmi-smi** still returning "No AMD GPUs specified"

[root@amd-gpu-2 ~]# rpm -qa|grep amdgpu-dkms
amdgpu-dkms-6.7.0.60100-1756574.el8.noarch
amdgpu-dkms-firmware-6.7.0.60100-1756574.el8.noarch

[root@amd-gpu-2 ~]# rpm -qa | grep rocm
rocm-developer-tools-6.1.0.60100-82.el8.x86_64
rocm-core-6.1.0.60100-82.el8.x86_64
rocminfo-1.0.0.60100-82.el8.x86_64
rocm-hip-runtime-6.1.0.60100-82.el8.x86_64
rocm-openmp-sdk-6.1.0.60100-82.el8.x86_64
rocm-device-libs-1.0.0.60100-82.el8.x86_64
rocm-cmake-0.12.0.60100-82.el8.x86_64
rocm-debug-agent-2.0.3.60100-82.el8.x86_64
rocm-opencl-sdk-6.1.0.60100-82.el8.x86_64
rocm-smi-lib-7.0.0.60100-82.el8.x86_64
rocm-opencl-icd-loader-1.2.60100-82.el8.x86_64
rocm-opencl-devel-2.0.0.60100-82.el8.x86_64
rocm-ml-libraries-6.1.0.60100-82.el8.x86_64
rocm-ml-sdk-6.1.0.60100-82.el8.x86_64
rocm-opencl-2.0.0.60100-82.el8.x86_64
rocm-opencl-runtime-6.1.0.60100-82.el8.x86_64
rocm-gdb-14.1.60100-82.el8.x86_64
rocm-hip-libraries-6.1.0.60100-82.el8.x86_64
rocm-utils-6.1.0.60100-82.el8.x86_64
rocm-hip-sdk-6.1.0.60100-82.el8.x86_64
rocm-dbgapi-0.71.0.60100-82.el8.x86_64
rocm-hip-runtime-devel-6.1.0.60100-82.el8.x86_64
rocm-llvm-17.0.0.24103.60100-82.el8.x86_64
rocm-language-runtime-6.1.0.60100-82.el8.x86_64
[root@amd-gpu-2 ~]#
```
[root@amd-gpu-2 ~]# rocm-smi


WARNING: No AMD GPUs specified
=================================== ROCm System Management Interface ===================================
============================================= Concise Info =============================================
Device  [Model : Revision]  Temp    Power  Partitions      SCLK  MCLK  Fan  Perf  PwrCap  VRAM%  GPU%
        Name (20 chars)     (Edge)  (Avg)  (Mem, Compute)
========================================================================================================
========================================================================================================
========================================= End of ROCm SMI Log ==========================================
```


---

### 评论 #14 — anoopsinghnegi (2024-05-13T08:44:43Z)

@nartmada - I didn't hear from you, kindly update

---

### 评论 #15 — nartmada (2024-05-13T18:23:15Z)

@anoopsinghnegi, I am sorry for not getting back.  Can you please run the command "amd-smi firmware" to dump out the firmware version on your system?  Thanks.

---

### 评论 #16 — anoopsinghnegi (2024-05-14T07:30:21Z)

@nartmada, amd-smi unable to detect GPU device
```
# lspci | grep -i amd
0002:00:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 21 [Radeon Pro V620 MxGPU]
# lspci -nn | grep -i amd
0002:00:00.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] Navi 21 [Radeon Pro V620 MxGPU] [1002:73ae]

```
```
#amd-smi
ERROR:root:Unable to detect any GPU devices, check amdgpu version and module status

# amd-smi firmware
ERROR:root:Unable to detect any GPU devices, check amdgpu version and module status
#
```


---

### 评论 #17 — anoopsinghnegi (2024-05-20T09:35:51Z)

@nartmada - We are using Azure to get an AMD  v620 GPU VM with size: Standard NG8ads V620 v1 (8 vcpus, 16 GiB memory), could you try creating the same instance type at your end and try to reproduce the issue?

---

### 评论 #18 — anoopsinghnegi (2024-06-03T05:06:39Z)

@nartmada - Please update

---

### 评论 #19 — nartmada (2024-06-03T15:38:09Z)

@anoopsinghnegi, apologies for the lack of update :( We will try to repro the issue here.

---

### 评论 #20 — harkgill-amd (2024-06-24T15:35:31Z)

Hi @anoopsinghnegi, wanted to provide you a quick update. We have successfully reproduced the issue internally and are continuing to investigate the cause.

---

### 评论 #21 — anoopsinghnegi (2024-06-26T05:59:54Z)

@harkgill-amd, I appreciate the update. Please keep posting any updates here.

---

### 评论 #22 — harkgill-amd (2024-08-16T19:58:02Z)

@anoopsinghnegi, apologies again for the delay in response. After much internal discussion, we have confirmed that ROCm releases are not currently enabled on Azure NGads instances as of ROCm 6.2. There are plans to introduce support for ROCm on cloud platforms in an upcoming release.

Let's keep this ticket open until support is officially released and we can circle back to confirm if the issue has been resolved.

---

### 评论 #23 — tedliosu (2024-09-28T21:37:30Z)

Can confirm this issue as well on my end after finally getting access to a NGads instance after several days of waiting in a backlog. A bit disappointed that AMD isn't quite on par with their major competitor offerings right now but looking forward to the day when I can use NGads instance with ROCm :crossed_fingers:

---

### 评论 #24 — krishgobinath (2025-01-04T02:33:17Z)

@harkgill-amd I'm seeing same issue on Azure `NGads` with ROCM version `6.3` and ubuntu 24.04
```
azureuser@myVm:~$ rocminfo
ROCk module is NOT loaded, possibly no GPU devices
azureuser@myVm:~$ dkms status
amdgpu/6.10.5-2095006.24.04, 6.8.0-1017-azure, x86_64: installed
azureuser@myVm:~$ lspci
0002:00:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 21 [Radeon Pro V620 MxGPU]
175c:00:00.0 Non-Volatile memory controller: Microsoft Corporation Device b111
6e2b:00:02.0 Ethernet controller: Mellanox Technologies MT27710 Family [ConnectX-4 Lx Virtual Function] (rev 80)
```

---

### 评论 #25 — harkgill-amd (2025-02-28T20:43:05Z)

A brief update on the current status of this issue. 

The V620 / NGads instances requires a special Linux PRO driver build from Microsoft – installing the ROCm amdgpu driver on V620 / NGads will not work, as seen in this thread. For ROCm on V620 / NGads you'd have to reach out to your Microsoft account rep for access to the Linux PRO driver.

As an alternative, the V710 NVv5 instances are also now available in public preview and do not require a special driver. This enables compatibility with the ROCm packaged amdgpu driver allowing users to get started with ROCm by following the generic installation instructions. You can sign up for the public preview of the V710 instances by clicking the blue button at the bottom of the following page. 

[Azure NV V710 v5: Empowering Real-Time AI/ML Inferencing and Advanced Visualization in the Cloud
](https://techcommunity.microsoft.com/blog/azurehighperformancecomputingblog/azure-nv-v710-v5-empowering-real-time-aiml-inferencing-and-advanced-visualizatio/4261890)

---

### 评论 #26 — harkgill-amd (2025-03-21T17:56:02Z)

Closing this issue out. See above comment for more information.

---
