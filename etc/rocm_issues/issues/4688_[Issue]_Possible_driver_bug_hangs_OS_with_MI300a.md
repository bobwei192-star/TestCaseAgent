# [Issue]: Possible driver bug hangs OS with MI300a

> **Issue #4688**
> **状态**: closed
> **创建时间**: 2025-04-24T21:42:43Z
> **更新时间**: 2025-07-10T18:03:10Z
> **关闭时间**: 2025-07-10T18:03:10Z
> **作者**: ekeever1
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4688

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

On two separate days, our MI300a system was reported as all GPU code and rocminfo hanging/inaccessible. Normal reboot was not sufficient to recover usability, the system had to be completely powered off and powered on again.

Additional emails with our team suggest that this may be related to an attempt to use software PC sampling in Tau. After at least one crash, it was reported that any attempt to talk to the driver provoked the following in dmesg,

[Tue Apr 22 14:05:42 2025] amdgpu 0000:c1:00.0: amdgpu: psp gfx command CONFIG_SQ_PERFMON(0x46) failed and response status is (0x100)

The following snippets were recovered from dmesg before the two resets which may hopefully provide further clues for the driver wizards,

[Tue Apr 22 09:49:27 2025] ------------[ cut here ]------------
[Tue Apr 22 09:49:27 2025] amdgpu 0000:c1:00.0: Cached partition mode 0 not matching with device mode 15
[Tue Apr 22 09:49:27 2025] WARNING: CPU: 58 PID: 3595454 at /tmp/amd.iXiyxKmZ/amd/amdgpu/amdgpu_xcp.c:242 amdgpu_xcp_query_partition_mode+0xa8/0x130 [amdgpu]
[Tue Apr 22 09:49:27 2025] Modules linked in: mmfs26(OE) mmfslinux(OE) tracedev(OE) mptcp_diag xsk_diag tcp_diag udp_diag raw_diag inet_diag unix_diag af_packet_diag netlink_diag squashfs loop socwatch2_15(OE) vtsspp(OE) sep5(OE) veth socperf3(OE) nf_conntrack_netlink pax(OE) xt_CHECKSUM ipt_MASQUERADE xt_conntrack ipt_REJECT xt_addrtype nft_compat nft_counter bridge rpcsec_gss_krb5 auth_rpcgss nfsv4 dns_resolver nfs lockd grace fscache 8021q garp stp mrp overlay llc nf_nat_tftp nft_objref nf_conntrack_tftp nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 rdma_ucm(OE) rdma_cm(OE) iw_cm(OE) ip_set nf_tables nfnetlink ib_ipoib(OE) ib_cm(OE) ib_umad(OE) sunrpc vfat fat intel_rapl_msr intel_rapl_common edac_mce_amd kvm_amd ccp kvm irqbypass crct10dif_pclmul crc32_pclmul ghash_clmulni_intel rapl pcspkr acpi_cpufreq ipmi_ssif joydev ses enclosure wmi_bmof sp5100_tco
[Tue Apr 22 09:49:27 2025]  acpi_ipmi ipmi_si ipmi_devintf i2c_piix4 wmi i2c_designware_platform ipmi_msghandler i2c_designware_core binfmt_misc knem(OE) xfs libcrc32c crc32c_intel mlx5_ib(OE) ib_uverbs(OE) ib_core(OE) amdgpu(OE) sg raid1 amddrm_ttm_helper(OE) amdttm(OE) video amdxcp(OE) amddrm_buddy(OE) drm_display_helper amd_sched(OE) ast amdkcl(OE) drm_shmem_helper i2c_algo_bit mlx5_core(OE) drm_kms_helper pci_hyperv_intf mlxdevm(OE) nvme syscopyarea mlx_compat(OE) psample sysfillrect ixgbe mpt3sas sysimgblt mlxfw(OE) mdio nvme_core raid_class drm scsi_transport_sas t10_pi dca tls(X) rndis_host cdc_ether usbnet mii xpmem(OE) fuse [last unloaded: tracedev]
[Tue Apr 22 09:49:27 2025] CPU: 58 PID: 3595454 Comm: python3 Kdump: loaded Tainted: G        W  OE  X  -------- -  - 4.18.0-553.16.1.el8_10.x86_64 #1
[Tue Apr 22 09:49:27 2025] Hardware name: Supermicro Super Server/H13QSH, BIOS 1.0 10/01/2024
[Tue Apr 22 09:49:27 2025] RIP: 0010:amdgpu_xcp_query_partition_mode+0xa8/0x130 [amdgpu]
[Tue Apr 22 09:49:27 2025] Code: 2b 48 8b 38 4c 8b 77 70 4d 85 f6 74 7a e8 20 23 f7 ee 45 89 e8 44 89 e1 4c 89 f2 48 89 c6 48 c7 c7 a8 06 2a c1 e8 05 cb 9f ee <0f> 0b 85 ed 74 26 5b 44 89 e8 5d 41 5c 41 5d 41 5e e9 4d 67 60 ef
[Tue Apr 22 09:49:27 2025] RSP: 0018:ffffa3b598687e00 EFLAGS: 00010286
[Tue Apr 22 09:49:27 2025] RAX: 0000000000000000 RBX: ffff92ddcad40000 RCX: 0000000000000027
[Tue Apr 22 09:49:27 2025] RDX: 0000000000000027 RSI: 00000001001733e0 RDI: ffff93390f89e690
[Tue Apr 22 09:49:27 2025] RBP: 0000000000000000 R08: 0000000000000000 R09: c0000001001733e0
[Tue Apr 22 09:49:27 2025] R10: 0000000006caf040 R11: ffffa3b598687c18 R12: 0000000000000000
[Tue Apr 22 09:49:27 2025] R13: 000000000000000f R14: ffff92dba7e4cad0 R15: ffff92dbb4501800
[Tue Apr 22 09:49:27 2025] FS:  00007f1aff60e400(0000) GS:ffff93390f880000(0000) knlGS:0000000000000000
[Tue Apr 22 09:49:27 2025] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[Tue Apr 22 09:49:27 2025] CR2: 00007f1aff42a010 CR3: 0000004ec4bea004 CR4: 0000000000770ee0
[Tue Apr 22 09:49:27 2025] PKRU: 55555554
[Tue Apr 22 09:49:27 2025] Call Trace:
[Tue Apr 22 09:49:27 2025]  ? __warn+0x94/0xe0
[Tue Apr 22 09:49:27 2025]  ? amdgpu_xcp_query_partition_mode+0xa8/0x130 [amdgpu]
[Tue Apr 22 09:49:27 2025]  ? amdgpu_xcp_query_partition_mode+0xa8/0x130 [amdgpu]
[Tue Apr 22 09:49:27 2025]  ? report_bug+0xb1/0xe0
[Tue Apr 22 09:49:27 2025]  ? do_error_trap+0x9e/0xd0
[Tue Apr 22 09:49:27 2025]  ? do_invalid_op+0x36/0x40
[Tue Apr 22 09:49:27 2025]  ? amdgpu_xcp_query_partition_mode+0xa8/0x130 [amdgpu]
[Tue Apr 22 09:49:27 2025]  ? invalid_op+0x14/0x20
[Tue Apr 22 09:49:27 2025]  ? amdgpu_xcp_query_partition_mode+0xa8/0x130 [amdgpu]
[Tue Apr 22 09:49:27 2025]  amdgpu_gfx_get_current_compute_partition+0x1e/0x50 [amdgpu]
[Tue Apr 22 09:49:27 2025]  dev_attr_show+0x1c/0x40
[Tue Apr 22 09:49:27 2025]  sysfs_kf_seq_show+0x9b/0x110
[Tue Apr 22 09:49:27 2025]  seq_read+0x163/0x420
[Tue Apr 22 09:49:27 2025]  vfs_read+0x91/0x150
[Tue Apr 22 09:49:27 2025]  ksys_read+0x4f/0xb0
[Tue Apr 22 09:49:27 2025]  do_syscall_64+0x5b/0x1a0
[Tue Apr 22 09:49:27 2025]  entry_SYSCALL_64_after_hwframe+0x66/0xcb
[Tue Apr 22 09:49:27 2025] RIP: 0033:0x7f1aff1e9ab2
[Tue Apr 22 09:49:27 2025] Code: 95 20 00 f7 d8 64 89 02 48 c7 c0 ff ff ff ff eb b6 0f 1f 80 00 00 00 00 f3 0f 1e fa 8b 05 96 d9 20 00 85 c0 75 12 31 c0 0f 05 <48> 3d 00 f0 ff ff 77 56 c3 0f 1f 44 00 00 41 54 49 89 d4 55 48 89
[Tue Apr 22 09:49:27 2025] RSP: 002b:00007ffedafcfb28 EFLAGS: 00000246 ORIG_RAX: 0000000000000000
[Tue Apr 22 09:49:27 2025] RAX: ffffffffffffffda RBX: 00007ffedafcfe20 RCX: 00007f1aff1e9ab2
[Tue Apr 22 09:49:27 2025] RDX: 0000000000001fff RSI: 0000000002ff99e0 RDI: 0000000000000008
[Tue Apr 22 09:49:27 2025] RBP: 0000000000001fff R08: 00007f1af097d970 R09: 00000000024bb018
[Tue Apr 22 09:49:27 2025] R10: 0000000000000000 R11: 0000000000000246 R12: 0000000002ff99e0
[Tue Apr 22 09:49:27 2025] R13: 00007ffedafcfe88 R14: 0000000000000000 R15: 00007ffedafcfe10
[Tue Apr 22 09:49:27 2025] ---[ end trace 8c7941e50bea850e ]---
[Tue Apr 22 09:49:29 2025] amdgpu 0000:02:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000003 SMN_C2PMSG_82:0x00000002
[Tue Apr 22 09:49:29 2025] amdgpu 0000:02:00.0: amdgpu: Failed to retrieve enabled ppfeatures!

And here is from today's issues which repeated several hundred times in dmesg before I rebooted it,


[86296.267308] WARNING: CPU: 129 PID: 2230367 at /tmp/amd.iXiyxKmZ/amd/amdgpu/amdgpu_irq.c:633 amdgpu_irq_put+0x68/0x90 [amdgpu]
[86296.267419] Modules linked in: squashfs loop mmfs26(OE) mmfslinux(OE) tracedev(OE) veth socwatch2_15(OE) vtsspp(OE) sep5(OE) rpcsec_gss_krb5 auth_rpcgss socperf3(OE) nfsv4 dns_resolver nfs lockd grac
e fscache nf_conntrack_netlink pax(OE) xt_CHECKSUM xt_addrtype ipt_MASQUERADE xt_conntrack ipt_REJECT nft_compat nft_counter bridge 8021q garp stp mrp llc overlay nf_nat_tftp nft_objref nf_conntrack_tft
p nft_fib_inet nft_fib_ipv4 nft_fib_ipv6 nft_fib nft_reject_inet nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_ct nf_tables_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 rdma_ucm(OE
) ip_set rdma_cm(OE) iw_cm(OE) nf_tables nfnetlink ib_ipoib(OE) ib_cm(OE) ib_umad(OE) sunrpc vfat fat intel_rapl_msr intel_rapl_common edac_mce_amd kvm_amd ccp kvm irqbypass crct10dif_pclmul crc32_pclmu
l ghash_clmulni_intel rapl pcspkr acpi_cpufreq ipmi_ssif joydev wmi_bmof acpi_ipmi ses enclosure sp5100_tco ipmi_si ipmi_devintf i2c_piix4 wmi i2c_designware_platform ipmi_msghandler
[86296.267490]  i2c_designware_core binfmt_misc knem(OE) xfs libcrc32c crc32c_intel mlx5_ib(OE) ib_uverbs(OE) ib_core(OE) amdgpu(OE) raid1 sg amddrm_ttm_helper(OE) amdttm(OE) video amdxcp(OE) amddrm_bud
dy(OE) drm_display_helper amd_sched(OE) ast amdkcl(OE) mlx5_core(OE) i2c_algo_bit drm_shmem_helper pci_hyperv_intf drm_kms_helper mlxdevm(OE) syscopyarea nvme mlx_compat(OE) sysfillrect mpt3sas psample
ixgbe sysimgblt raid_class mlxfw(OE) nvme_core mdio drm t10_pi scsi_transport_sas dca tls(X) rndis_host cdc_ether usbnet mii xpmem(OE) fuse
[86296.267530] CPU: 129 PID: 2230367 Comm: kworker/u384:4 Kdump: loaded Tainted: G        W  OE  X  -------- -  - 4.18.0-553.16.1.el8_10.x86_64 #1
[86296.267534] Hardware name: Supermicro Super Server/H13QSH, BIOS 1.0 10/01/2024
[86296.267537] Workqueue: amdgpu-reset-hive amdgpu_amdkfd_reset_work [amdgpu]
[86296.267644] RIP: 0010:amdgpu_irq_put+0x68/0x90 [amdgpu]
[86296.267748] Code: e8 48 8b 53 08 f0 ff 0c 82 b8 00 00 00 00 74 09 5b 5d 41 5c e9 04 17 cf c4 89 ea 48 89 de 4c 89 e7 5b 5d 41 5c e9 88 fd ff ff <0f> 0b b8 ea ff ff ff eb dd b8 ea ff ff ff e9 e0 16 cf
c4 b8 fe ff
[86296.267752] RSP: 0018:ffffaaa88f85bd18 EFLAGS: 00010246  
[86296.267755] RAX: 0000000000000000 RBX: ffff917db5ca9200 RCX: 000000000000000c
[86296.267757] RDX: ffffffffc13c52b0 RSI: 0000000000000000 RDI: ffff917db5ca9200
[86296.267759] RBP: 0000000000000000 R08: 0000000000000008 R09: 0000000000000000
[86296.267762] R10: 0000000000000000 R11: ffffffff86be3988 R12: ffff917db5c80000
[86296.267764] R13: ffffaaa88f85be50 R14: 0000000000000000 R15: ffff917db5c90938
[86296.267767] FS:  0000000000000000(0000) GS:ffff91bd0fe40000(0000) knlGS:0000000000000000
[86296.267770] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[86296.267772] CR2: 00007f8cc4144d20 CR3: 00000025b5a10003 CR4: 0000000000770ee0
[86296.267775] PKRU: 55555554
[86296.267776] Call Trace:
[86296.267779]  ? __warn+0x94/0xe0
[86296.267782]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[86296.267884]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[86296.267987]  ? report_bug+0xb1/0xe0
[86296.267989]  ? apic_timer_interrupt+0xa/0x20
[86296.267992]  ? do_error_trap+0x9e/0xd0
[86296.267996]  ? do_invalid_op+0x36/0x40
[86296.267999]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[86296.268101]  ? invalid_op+0x14/0x20
[86296.268106]  ? amdgpu_irq_put+0x68/0x90 [amdgpu]
[86296.268208]  ? amdgpu_irq_put+0x39/0x90 [amdgpu]
[86296.268311]  gfx_v9_4_3_hw_fini+0x1e/0x90 [amdgpu]
[86296.268419]  amdgpu_ip_block_suspend+0x23/0x40 [amdgpu]
[86296.268523]  aldebaran_mode2_prepare_hwcontext+0xb3/0xc0 [amdgpu]
[86296.268629]  amdgpu_device_pre_asic_reset+0xb6/0x2c0 [amdgpu]
[86296.268734]  amdgpu_device_gpu_recover.cold.70+0x533/0xc9b [amdgpu]
[86296.268851]  amdgpu_amdkfd_reset_work+0x74/0xa0 [amdgpu]
[86296.268963]  process_one_work+0x1d3/0x390  
[86296.268967]  worker_thread+0x30/0x390
[86296.268971]  ? process_one_work+0x390/0x390
[86296.268974]  kthread+0x134/0x150
[86296.268976]  ? set_kthread_struct+0x50/0x50
[86296.268980]  ret_from_fork+0x1f/0x40
[86296.268985] ---[ end trace bc93b43c58c74a45 ]---

### Operating System

RHEL 8.10

### CPU

MI300a / family 25, model 144, stepping 1

### GPU

MI300a SuperMicro system (H13QSH)

### ROCm Version

ROCm 6.4.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

[root@odyssey ~]# rocminfo --support
ROCk module version 6.12.0 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.14
Runtime Ext Version:     1.6
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
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
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
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    130750360(0x7cb1798) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    130750360(0x7cb1798) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    130750360(0x7cb1798) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    130750360(0x7cb1798) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131809200(0x7db3fb0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131809200(0x7db3fb0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131809200(0x7db3fb0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131809200(0x7db3fb0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    2                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        2                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131764472(0x7da90f8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131764472(0x7da90f8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131764472(0x7da90f8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131764472(0x7da90f8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 4                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    3                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        3                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131797612(0x7db126c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131797612(0x7db126c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131797612(0x7db126c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131797612(0x7db126c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 5                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-f68e1753dc12b715               
  Marketing Name:          AMD Instinct MI300A                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    4                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   512                                
  Internal Node ID:        4                                  
  Compute Unit:            228                                
  SIMDs per CU:            4                                  
  Shader Engines:          24                                 
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       APU
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 165                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*******                  
Agent 6                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-5bd3148dc76b831a               
  Marketing Name:          AMD Instinct MI300A                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    5                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   16640                              
  Internal Node ID:        5                                  
  Compute Unit:            228                                
  SIMDs per CU:            4                                  
  Shader Engines:          24                                 
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       APU
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 165                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*******                  
Agent 7                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-a57d04507c371187               
  Marketing Name:          AMD Instinct MI300A                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    6                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   33024                              
  Internal Node ID:        6                                  
  Compute Unit:            228                                
  SIMDs per CU:            4                                  
  Shader Engines:          24                                 
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       APU
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 165                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*******                  
Agent 8                  
*******                  
  Name:                    gfx942                             
  Uuid:                    GPU-cdcfb00895cff553               
  Marketing Name:          AMD Instinct MI300A                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    7                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      262144(0x40000) KB                 
  Chip ID:                 29856(0x74a0)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2100                               
  BDFID:                   49408                              
  Internal Node ID:        7                                  
  Compute Unit:            228                                
  SIMDs per CU:            4                                  
  Shader Engines:          24                                 
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       APU
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 165                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98647808(0x5e13f00) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***             
[root@odyssey ~]# 


### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — ppanchad-amd (2025-04-25T14:28:53Z)

Hi @ekeever1. Internal ticket has been created to investigate this issue. Thanks!

---
