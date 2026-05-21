# [Documentation]: Tweak Ryzen HOWTo to include Debian

> **Issue #5671**
> **状态**: open
> **创建时间**: 2025-11-17T05:53:04Z
> **更新时间**: 2025-12-11T15:17:19Z
> **作者**: ianbmacdonald
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5671

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Description of errors

Just walking through the online docs to see how they line up with my own best practice on Debian 13 for the Strix Halo. 

I noticed the [Linux HOWTO page](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#prepare-the-system) opens with 

`sudo apt update && sudo apt-get install linux-oem-24.04c`

Since this page is Ubuntu-only, it might be good to switch to the tabbed OS approach to broaden procedures for the other ROCm supported distibutions.  Debian 13 already ships the default kernel with the [MES kernel fixes](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1118658). 

The Debian 13 Trixie equivalent is

```
sudo apt update
wget https://repo.radeon.com/amdgpu-install/7.1/ubuntu/noble/amdgpu-install_7.1.70100-1_all.deb
sudo apt install ./amdgpu-install_7.1.70100-1_all.deb
sudo amdgpu-install -y --usecase=rocm
sudo mokutil --import /var/lib/dkms/mok.pub  # Add DKMS MOK key, enter a password for prompt on reboot w/ Secure Boot
sudo dpkg-reconfigure amdgpu-dkms  #Rebuild initramfs with signed modules
sudo usermod -a -G render,video $LOGNAME
sudo reboot   # Reboot enroll MOK key to pass Secure Boot
```



### Attach any links, screenshots, or additional evidence you think will be helpful.

The following convienently allows all the memory to be used by the GPU for AI workloads on all amdgpu versions (including future distribution kernels that use just `ttm`), works around the [MES hang](https://github.com/ROCm/ROCm/issues/5590).   It uses standard grub drop-in configuration to avoid any unecessary prompts at the next distribution upgrade and does not require creating a venv or running update-initramfs to apply the memory configuration.

`sudo vi /etc/default/grub.d/amdgpu.cfg`
```
# /etc/default/grub.d/amdgpu.cfg
GRUB_CMDLINE_LINUX="${GRUB_CMDLINE_LINUX:+$GRUB_CMDLINE_LINUX }ttm.pages_limit=32768000 ttm.page_pool_size=32768000 amdttm.pages_limit=32768000 amdttm.page_pool_size=32768000 amdgpu.cwsr_enable=0"

```
`update-grub`

Boot times are fast, and free memory is maximized with swap disabled in a headless configuration

```
sudo systemd-analyze
Startup finished in 4.395s (kernel) + 1.705s (userspace) = 6.101s 
graphical.target reached after 1.705s in userspace.

sudo free 
               total        used        free      shared  buff/cache   available
Mem:       131171464     1246480   130706828        1636      138376   129924984
Swap:              0           0           0

sudo amd-smi 
+------------------------------------------------------------------------------+
| AMD-SMI 26.1.0+5df6c765      amdgpu version: 6.16.6   ROCm version: 7.1.0    |
| VBIOS version: 00107962                                                      |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:c2:00.0    AMD Radeon Graphics | N/A        N/A   0             N/A/0 W |
|   0       0     N/A             N/A | N/A        N/A              161/512 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+

sudo cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080

sudo modinfo amdgpu | head -n 3
filename:       /lib/modules/6.12.57+deb13-amd64/updates/dkms/amdgpu.ko.xz
version:        6.16.6
license:        GPL and additional rights

sudo dmesg | grep amdgpu | grep memory
[    3.543771] amdgpu 0000:c2:00.0: amdgpu: amdgpu: 512M of VRAM memory ready
[    3.543773] amdgpu 0000:c2:00.0: amdgpu: amdgpu: 128000M of GTT memory ready.
```




---

## 评论 (6 条)

### 评论 #1 — elatov (2025-11-18T07:00:30Z)

Sorry for the random note, but I gave this a try. And it seems to have loaded fine:

```
> sudo dmesg | grep amdgpu
[    0.000000] Command line: BOOT_IMAGE=/vmlinuz-6.12.57+deb13-amd64 root=/dev/mapper/ubuntu--vg-ubuntu--lv ro amdgpu.gttsize=65536 ttm.pages_limit=16777216 amdgpu.cwsr_enable=0 amd_iommu=off
[    0.014670] Kernel command line: BOOT_IMAGE=/vmlinuz-6.12.57+deb13-amd64 root=/dev/mapper/ubuntu--vg-ubuntu--lv ro amdgpu.gttsize=65536 ttm.pages_limit=16777216 amdgpu.cwsr_enable=0 amd_iommu=off
[    2.618892] [drm] amdgpu kernel modesetting enabled.
[    2.620869] [drm] amdgpu version: 6.16.6
[    2.621357] amdgpu: Virtual CRAT table created for CPU
[    2.621510] amdgpu: Topology: Add CPU node
[    2.624684] amdgpu 0000:01:00.0: amdgpu: initializing kernel modesetting (IP DISCOVERY 0x1002:0x1586 0x103C:0x8D1D 0xD1).
[    2.624798] amdgpu 0000:01:00.0: amdgpu: register mmio base: 0x89000000
[    2.624892] amdgpu 0000:01:00.0: amdgpu: register mmio size: 1048576
[    2.627412] amdgpu 0000:01:00.0: amdgpu: detected ip block number 0 <common_v1_0_0> (soc21_common)
[    2.627555] amdgpu 0000:01:00.0: amdgpu: detected ip block number 1 <gmc_v11_0_0> (gmc_v11_0)
[    2.627650] amdgpu 0000:01:00.0: amdgpu: detected ip block number 2 <ih_v6_0_0> (ih_v6_1)
[    2.627743] amdgpu 0000:01:00.0: amdgpu: detected ip block number 3 <psp_v13_0_0> (psp)
[    2.627832] amdgpu 0000:01:00.0: amdgpu: detected ip block number 4 <smu_v14_0_0> (smu)
[    2.627922] amdgpu 0000:01:00.0: amdgpu: detected ip block number 5 <dce_v1_0_0> (dm)
[    2.628011] amdgpu 0000:01:00.0: amdgpu: detected ip block number 6 <gfx_v11_0_0> (gfx_v11_0)
[    2.628102] amdgpu 0000:01:00.0: amdgpu: detected ip block number 7 <sdma_v6_0_0> (sdma_v6_0)
[    2.628193] amdgpu 0000:01:00.0: amdgpu: detected ip block number 8 <vcn_v4_0_5> (vcn_v4_0_5)
[    2.628294] amdgpu 0000:01:00.0: amdgpu: detected ip block number 9 <jpeg_v4_0_5> (jpeg_v4_0_5)
[    2.628386] amdgpu 0000:01:00.0: amdgpu: detected ip block number 10 <mes_v11_0_0> (mes_v11_0)
[    2.628477] amdgpu 0000:01:00.0: amdgpu: detected ip block number 11 <vpe_v6_1_0> (vpe_v6_1)
[    2.628592] amdgpu 0000:01:00.0: amdgpu: Fetched VBIOS from VFCT
[    2.628684] amdgpu: ATOM BIOS: 113-STRXLGEN-001
[    2.630473] amdgpu 0000:01:00.0: amdgpu: VPE: collaborate mode true
[    2.630590] amdgpu 0000:01:00.0: amdgpu: Trusted Memory Zone (TMZ) feature disabled as experimental (default)
[    2.630731] amdgpu 0000:01:00.0: amdgpu: vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
[    2.630859] amdgpu 0000:01:00.0: amdgpu: VRAM: 65536M 0x0000008000000000 - 0x0000008FFFFFFFFF (65536M used)
[    2.630961] amdgpu 0000:01:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[    2.631457] amdgpu 0000:01:00.0: amdgpu: amdgpu: 65536M of VRAM memory ready
[    2.633575] amdgpu 0000:01:00.0: amdgpu: [drm] Configuring gttsize via module parameter is deprecated, please use ttm.pages_limit
[    2.633682] amdgpu 0000:01:00.0: amdgpu: [drm] GTT size has been set as 68719476736 but TTM size has been set as 12593328128, this is unusual
[    2.633788] amdgpu 0000:01:00.0: amdgpu: amdgpu: 65536M of GTT memory ready.
[    2.635521] amdgpu 0000:01:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x09002F00
[    2.635812] amdgpu 0000:01:00.0: amdgpu: [VCN instance 0] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 25
[    2.636005] amdgpu 0000:01:00.0: amdgpu: [VCN instance 1] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 25
[    2.658948] amdgpu 0000:01:00.0: amdgpu: reserve 0x8c00000 from 0x8fe0000000 for PSP TMR
[    3.364363] amdgpu 0000:01:00.0: amdgpu: RAS: optional ras ta ucode is not available
[    3.370079] amdgpu 0000:01:00.0: amdgpu: RAP: optional rap ta ucode is not available
[    3.370321] amdgpu 0000:01:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
[    3.402731] amdgpu 0000:01:00.0: amdgpu: SMU is initialized successfully!
[    3.407031] amdgpu 0000:01:00.0: amdgpu: [drm] Display Core v3.2.351 initialized on DCN 3.5.1
[    3.407137] amdgpu 0000:01:00.0: amdgpu: [drm] DP-HDMI FRL PCON supported
[    3.410200] amdgpu 0000:01:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09002F00
[    3.413953] amdgpu 0000:01:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.441695] amdgpu 0000:01:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.441974] amdgpu 0000:01:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.442247] amdgpu 0000:01:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.443191] amdgpu 0000:01:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.444643] amdgpu 0000:01:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.444830] amdgpu 0000:01:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.445017] amdgpu 0000:01:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.445203] amdgpu 0000:01:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    3.456298] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[    3.456408] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[    3.456878] amdgpu: Virtual CRAT table created for GPU
[    3.460937] amdgpu: Topology: Add dGPU node [0x1586:0x1002]
[    3.461026] kfd kfd: amdgpu: added device 1002:1586
[    3.461126] amdgpu 0000:01:00.0: amdgpu: SE 2, SH per SE 2, CU per SH 10, active_cu_number 40
[    3.461222] amdgpu 0000:01:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[    3.461320] amdgpu 0000:01:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[    3.461411] amdgpu 0000:01:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[    3.461500] amdgpu 0000:01:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[    3.461589] amdgpu 0000:01:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[    3.461677] amdgpu 0000:01:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[    3.461763] amdgpu 0000:01:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[    3.461849] amdgpu 0000:01:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[    3.461934] amdgpu 0000:01:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[    3.462018] amdgpu 0000:01:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[    3.462102] amdgpu 0000:01:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[    3.462203] amdgpu 0000:01:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[    3.462296] amdgpu 0000:01:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[    3.462378] amdgpu 0000:01:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[    3.462457] amdgpu 0000:01:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[    3.462535] amdgpu 0000:01:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[    3.467186] amdgpu 0000:01:00.0: amdgpu: Runtime PM not available
[    3.468390] [drm] Initialized amdgpu 3.64.0 for 0000:01:00.0 on minor 0
[    3.474872] amdgpu 0000:01:00.0: [drm] fb1: amdgpudrmfb frame buffer device
```

But `ollama` is still unable to see the device with `rocm`:

```
export ROCM_VISIBLE_DEVICES=0
export OLLAMA_DEBUG=1
export LD_LIBRARY_PATH=/opt/rocm-7.1.0/lib
> ollama serve
time=2025-11-17T23:54:57.372-07:00 level=INFO source=routes.go:1544 msg="server config" env="map[CUDA_VISIBLE_DEVICES: GGML_VK_VISIBLE_DEVICES: GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_CONTEXT_LENGTH:4096 OLLAMA_DEBUG:DEBUG OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://127.0.0.1:11434 OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:/home/elatov/.ollama/models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NEW_ENGINE:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NUM_PARALLEL:1 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://* vscode-file://*] OLLAMA_REMOTES:[ollama.com] OLLAMA_SCHED_SPREAD:false OLLAMA_VULKAN:false ROCR_VISIBLE_DEVICES: http_proxy: https_proxy: no_proxy:]"
time=2025-11-17T23:54:57.372-07:00 level=INFO source=images.go:522 msg="total blobs: 0"
time=2025-11-17T23:54:57.372-07:00 level=INFO source=images.go:529 msg="total unused blobs removed: 0"
time=2025-11-17T23:54:57.373-07:00 level=INFO source=routes.go:1597 msg="Listening on 127.0.0.1:11434 (version 0.12.11)"
time=2025-11-17T23:54:57.373-07:00 level=DEBUG source=sched.go:120 msg="starting llm scheduler"
time=2025-11-17T23:54:57.373-07:00 level=INFO source=runner.go:67 msg="discovering available GPUs..."
time=2025-11-17T23:54:57.373-07:00 level=INFO source=server.go:392 msg="starting runner" cmd="/usr/local/ollama/bin/ollama runner --ollama-engine --port 46387"
time=2025-11-17T23:54:57.373-07:00 level=DEBUG source=server.go:393 msg=subprocess PATH=/opt/puppetlabs/bin:/opt/local/bin:/opt/local/sbin:/sbin:/usr/sbin:/ec/bin:/ec/sbin:/opt/local/bin:/opt/local/sbin:/usr/local/sbin:/opt/omni/bin/i386:/opt/omni/bin:/usr/local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/elatov/.local/bin:/home/elatov/.local/bin ROCM_VISIBLE_DEVICES=0 OLLAMA_DEBUG=1 LD_LIBRARY_PATH=/usr/local/ollama/lib/ollama:/usr/local/ollama/lib/ollama/cuda_v12:/opt/rocm-7.1.0/lib OLLAMA_LIBRARY_PATH=/usr/local/ollama/lib/ollama:/usr/local/ollama/lib/ollama/cuda_v12
time=2025-11-17T23:54:57.395-07:00 level=DEBUG source=runner.go:418 msg="bootstrap discovery took" duration=22.438706ms OLLAMA_LIBRARY_PATH="[/usr/local/ollama/lib/ollama /usr/local/ollama/lib/ollama/cuda_v12]" extra_envs=map[]
time=2025-11-17T23:54:57.396-07:00 level=INFO source=server.go:392 msg="starting runner" cmd="/usr/local/ollama/bin/ollama runner --ollama-engine --port 39553"
time=2025-11-17T23:54:57.396-07:00 level=DEBUG source=server.go:393 msg=subprocess PATH=/opt/puppetlabs/bin:/opt/local/bin:/opt/local/sbin:/sbin:/usr/sbin:/ec/bin:/ec/sbin:/opt/local/bin:/opt/local/sbin:/usr/local/sbin:/opt/omni/bin/i386:/opt/omni/bin:/usr/local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/elatov/.local/bin:/home/elatov/.local/bin ROCM_VISIBLE_DEVICES=0 OLLAMA_DEBUG=1 LD_LIBRARY_PATH=/usr/local/ollama/lib/ollama:/usr/local/ollama/lib/ollama/cuda_v13:/opt/rocm-7.1.0/lib OLLAMA_LIBRARY_PATH=/usr/local/ollama/lib/ollama:/usr/local/ollama/lib/ollama/cuda_v13
time=2025-11-17T23:54:57.412-07:00 level=DEBUG source=runner.go:418 msg="bootstrap discovery took" duration=16.438582ms OLLAMA_LIBRARY_PATH="[/usr/local/ollama/lib/ollama /usr/local/ollama/lib/ollama/cuda_v13]" extra_envs=map[]
time=2025-11-17T23:54:57.413-07:00 level=INFO source=server.go:392 msg="starting runner" cmd="/usr/local/ollama/bin/ollama runner --ollama-engine --port 33345"
time=2025-11-17T23:54:57.413-07:00 level=DEBUG source=server.go:393 msg=subprocess PATH=/opt/puppetlabs/bin:/opt/local/bin:/opt/local/sbin:/sbin:/usr/sbin:/ec/bin:/ec/sbin:/opt/local/bin:/opt/local/sbin:/usr/local/sbin:/opt/omni/bin/i386:/opt/omni/bin:/usr/local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/elatov/.local/bin:/home/elatov/.local/bin ROCM_VISIBLE_DEVICES=0 OLLAMA_DEBUG=1 LD_LIBRARY_PATH=/usr/local/ollama/lib/ollama:/usr/local/ollama/lib/ollama/rocm:/opt/rocm-7.1.0/lib OLLAMA_LIBRARY_PATH=/usr/local/ollama/lib/ollama:/usr/local/ollama/lib/ollama/rocm
time=2025-11-17T23:54:57.455-07:00 level=DEBUG source=runner.go:418 msg="bootstrap discovery took" duration=42.004725ms OLLAMA_LIBRARY_PATH="[/usr/local/ollama/lib/ollama /usr/local/ollama/lib/ollama/rocm]" extra_envs=map[]
time=2025-11-17T23:54:57.455-07:00 level=DEBUG source=runner.go:116 msg="evluating which if any devices to filter out" initial_count=0
time=2025-11-17T23:54:57.455-07:00 level=DEBUG source=runner.go:40 msg="GPU bootstrap discovery took" duration=82.072628ms
time=2025-11-17T23:54:57.455-07:00 level=INFO source=types.go:60 msg="inference compute" id=cpu library=cpu compute="" name=cpu description=cpu libdirs=ollama driver="" pci_id="" type="" total="23.5 GiB" available="21.3 GiB"
time=2025-11-17T23:54:57.455-07:00 level=INFO source=routes.go:1638 msg="entering low vram mode" "total vram"="0 B" threshold="20.0 GiB"
```

And here is all the information about the device:

```
> sudo rocminfo
ROCk module version 6.16.6 is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.14
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
  Name:                    AMD RYZEN AI MAX+ PRO 395 w/ Radeon 8060S
  Uuid:                    CPU-XX
  Marketing Name:          AMD RYZEN AI MAX+ PRO 395 w/ Radeon 8060S
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
    L1:                      65536(0x10000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   0
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            4
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    24596344(0x1774f78) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24596344(0x1774f78) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    24596344(0x1774f78) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    24596344(0x1774f78) KB
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
  BDFID:                   256
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
      Size:                    67108864(0x4000000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67108864(0x4000000) KB
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
*** Done ***
```

At the current moment, `debian` has the following latest kernel:

```
> uname -r
6.12.57+deb13-amd64
```

---

### 评论 #2 — tcgu-amd (2025-11-18T19:13:04Z)

Hi @ianbmacdonald, I believe the link points to our ROCm on Radeon page -- which is for special ROCm releases for windows WSL support specifically. As far as I know ROCm on Radeon does not support debian images. Did you perhaps link it by mistake? Thanks! 

---

### 评论 #3 — elatov (2025-11-18T23:51:44Z)

Sorry this is my bad, this actually worked (I just forgot to add the groups):

```
time=2025-11-18T21:50:29.850Z level=INFO source=routes.go:1544 msg="server config" env="map[CUDA_VISIBLE_DEVICES: GGML_VK_VISIBLE_DEVICES: GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_CONTEXT_LENGTH:4096 OLLAMA_DEBUG:DEBUG OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://0.0.0.0:11434 OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:/root/.ollama/models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NEW_ENGINE:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NUM_PARALLEL:1 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://* vscode-file://*] OLLAMA_REMOTES:[ollama.com] OLLAMA_SCHED_SPREAD:false OLLAMA_VULKAN:false ROCR_VISIBLE_DEVICES: http_proxy: https_proxy: no_proxy:]"
time=2025-11-18T21:50:29.868Z level=INFO source=images.go:522 msg="total blobs: 5"
time=2025-11-18T21:50:29.870Z level=INFO source=images.go:529 msg="total unused blobs removed: 0"
time=2025-11-18T21:50:29.873Z level=INFO source=routes.go:1597 msg="Listening on [::]:11434 (version 0.12.11)"
time=2025-11-18T21:50:29.874Z level=DEBUG source=sched.go:120 msg="starting llm scheduler"
time=2025-11-18T21:50:29.875Z level=INFO source=runner.go:67 msg="discovering available GPUs..."
time=2025-11-18T21:50:29.878Z level=INFO source=server.go:392 msg="starting runner" cmd="/usr/bin/ollama runner --ollama-engine --port 36581"
time=2025-11-18T21:50:29.878Z level=DEBUG source=server.go:393 msg=subprocess PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin LD_LIBRARY_PATH=/usr/lib/ollama:/usr/lib/ollama/rocm:/usr/local/nvidia/lib:/usr/local/nvidia/lib64 OLLAMA_HOST=0.0.0.0:11434 OLLAMA_DEBUG=1 OLLAMA_LIBRARY_PATH=/usr/lib/ollama:/usr/lib/ollama/rocm
time=2025-11-18T21:50:30.387Z level=DEBUG source=runner.go:418 msg="bootstrap discovery took" duration=511.04519ms OLLAMA_LIBRARY_PATH="[/usr/lib/ollama /usr/lib/ollama/rocm]" extra_envs=map[]
time=2025-11-18T21:50:30.387Z level=DEBUG source=runner.go:116 msg="evluating which if any devices to filter out" initial_count=1
time=2025-11-18T21:50:30.387Z level=DEBUG source=runner.go:128 msg="verifying device is supported" library=/usr/lib/ollama/rocm description="AMD Radeon Graphics" compute=gfx1151 id=0 pci_id=0000:01:00.0
time=2025-11-18T21:50:30.388Z level=INFO source=server.go:392 msg="starting runner" cmd="/usr/bin/ollama runner --ollama-engine --port 44781"
time=2025-11-18T21:50:30.388Z level=DEBUG source=server.go:393 msg=subprocess PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin LD_LIBRARY_PATH=/usr/lib/ollama:/usr/lib/ollama/rocm:/usr/local/nvidia/lib:/usr/local/nvidia/lib64 OLLAMA_HOST=0.0.0.0:11434 OLLAMA_DEBUG=1 OLLAMA_LIBRARY_PATH=/usr/lib/ollama:/usr/lib/ollama/rocm ROCR_VISIBLE_DEVICES=0 GGML_CUDA_INIT=1
time=2025-11-18T21:50:30.944Z level=DEBUG source=runner.go:418 msg="bootstrap discovery took" duration=556.333456ms OLLAMA_LIBRARY_PATH="[/usr/lib/ollama /usr/lib/ollama/rocm]" extra_envs="map[GGML_CUDA_INIT:1 ROCR_VISIBLE_DEVICES:0]"
time=2025-11-18T21:50:30.944Z level=DEBUG source=runner.go:175 msg="adjusting filtering IDs" FilterID=0 new_ID=0
time=2025-11-18T21:50:30.944Z level=DEBUG source=runner.go:40 msg="GPU bootstrap discovery took" duration=1.070181506s
time=2025-11-18T21:50:30.944Z level=INFO source=types.go:42 msg="inference compute" id=0 filter_id=0 library=ROCm compute=gfx1151 name=ROCm0 description="AMD Radeon Graphics" libdirs=ollama,rocm driver=60342.13 pci_id=0000:01:00.0 type=iGPU total="64.0 GiB" available="63.8 GiB"
```

So I can confirm the above instructions work on `debian13`. 

---

### 评论 #4 — elatov (2025-11-19T18:01:49Z)

One more random note, I ran into https://github.com/ROCm/ROCm/issues/5536 and when I tried to install the `vulkan` option, it failed:

```
> sudo amdgpu-install --usecase=dkms --vulkan=radv
Hit:1 http://deb.debian.org/debian trixie InRelease
Hit:2 http://security.debian.org/debian-security trixie-security InRelease
Hit:3 http://deb.debian.org/debian trixie-updates InRelease
Hit:4 https://apt.postgresql.org/pub/repos/apt trixie-pgdg InRelease
Hit:5 https://repo.radeon.com/amdgpu/30.20/ubuntu noble InRelease
Hit:6 https://repo.radeon.com/rocm/apt/7.1 noble InRelease
Hit:7 https://repo.radeon.com/graphics/7.1/ubuntu noble InRelease
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
amdgpu-dkms is already the newest version (1:6.16.6.30200000-2238411.24.04).
linux-headers-6.12.57+deb13-amd64 is already the newest version (6.12.57-1).
Solving dependencies... Error!
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 mesa-amdgpu-vulkan-drivers : Depends: libdisplay-info1 (>= 0.1.1) but it is not installable
E: Unable to correct problems, you have held broken packages.
E: The following information from --solver 3.0 may provide additional context:
   Unable to satisfy dependencies. Reached two conflicting decisions:
   1. mesa-amdgpu-vulkan-drivers:amd64=1:25.3.0.70100-2238427.24.04 is selected for install
   2. mesa-amdgpu-vulkan-drivers:amd64 Depends libdisplay-info1 (>= 0.1.1)
      but none of the choices are installable:
      [no choices]
```

it looks like in `debian 13` it's ` libdisplay-info2`:

```
> sudo apt search libdisplay-info
libdisplay-info-bin/stable 0.2.0-2 amd64
  EDID and DisplayID library (utils)

libdisplay-info-dev/stable 0.2.0-2 amd64
  EDID and DisplayID library (development files)

libdisplay-info2/stable,now 0.2.0-2 amd64 [installed]
  EDID and DisplayID library (shared library)
```

So maybe not all use cases are support for `debian 13`.

---

### 评论 #5 — ianbmacdonald (2025-11-21T03:38:05Z)

> As far as I know ROCm on Radeon does not support debian images. Did you perhaps link it by mistake? Thanks!

Not sure what to say to this one.   I guess compute workloads on Strix Halo (headless) are not really being looked at by the Ryzen team [yet].   I wouldn't recommend trying to play games on Debian either. 

Both Debian 12 and 13 are supported [in software] on Radeon with ROCm on anything RDNA3 or later.    https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems

I might suggest AMD should just add gfx1151 to the main ROCm matrix.  For anyone stumbling on this thread, and looking for a Strix Halo blueprint for ROCm that more closely aligns with requirements for business inference workflows locally with low concurrency, I'd be happy to show you the path while the online support plays catch-up.




---

### 评论 #6 — tcgu-amd (2025-11-21T16:25:01Z)

> > As far as I know ROCm on Radeon does not support debian images. Did you perhaps link it by mistake? Thanks!
> 
> Not sure what to say to this one. I guess compute workloads on Strix Halo (headless) are not really being looked at by the Ryzen team [yet]. I wouldn't recommend trying to play games on Debian either.
> 
> Both Debian 12 and 13 are supported [in software] on Radeon with ROCm on anything RDNA3 or later. https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems
> 
> I might suggest AMD should just add gfx1151 to the main ROCm matrix. For anyone stumbling on this thread, and looking for a Strix Halo blueprint for ROCm that more closely aligns with requirements for business inference workflows locally with low concurrency, I'd be happy to show you the path while the online support plays catch-up.

@ianbmacdonald yeah that's definitely the goal here. Currently gfx115x support in 7.1 is but a "preview release", that's why it is hosted under ROCm on Radeon and Ryzen (which you can think of as a subproject of the broader ROCm project with a narrower support matrix). Currently, support for gfx151x is still undergoing integration into our broader ROCm release pipelines. Once everything is in place, it will definitely be promoted to the main ROCm project and you will find gfx115x under the main ROCm matrix as well. Guides for getting started will also be updated accordingly for the supported Linux distributions under the main ROCm docs. 

---
