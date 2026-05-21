# [Documentation]: Debian 12 installation

> **Issue #4330**
> **状态**: closed
> **创建时间**: 2025-02-03T14:25:46Z
> **更新时间**: 2025-02-28T15:41:35Z
> **关闭时间**: 2025-02-28T15:41:35Z
> **作者**: fpeterschmitt
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/4330

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

* `amdgpu-dkms` fails while building kernel module
* wrong `environment-modules` directions

### Suggestions

* remove the need for`amdgpu-dkms`: kernel 6.1 with its amdgpu (and firmware?) is enough. your dkms version of the module will fail to build on current debian stable. you can get it work on debian unstable but that's out of this issue scope.
* documentation for `environment-modules` doesn't seem accurate for Debian's version. as a replacement, `export ROCM_PATH=/opt/rocm` works.

---

## 评论 (12 条)

### 评论 #1 — harkgill-amd (2025-02-03T21:04:16Z)

Hi @fpeterschmitt, 

1. I was able to get both ROCm 6.3.2 installed and amdgpu-dkms built successfully on a fresh installation of Debian 12. This was done on the `6.1.0-30` kernel. Which kernel/ROCm version are you encountering failures building amdgpu-dkms with? Could you also please provide the build logs for these failures.
2. The `environment-modules` package is not installed by default on Debian. In order to install it and begin using it, you must run the below commands. After this, you can create `modulefiles` for different ROCm version and swap between them by loading and unloading their respective modules.
```
sudo apt install environment-modules
source /etc/profile.d/modules.sh
```
More information on `environment-modules` can be found on the project's [documentation portal](https://modules.readthedocs.io/en/latest/index.html).

---

### 评论 #2 — fpeterschmitt (2025-02-03T21:29:31Z)

Thanks for your answer @harkgill-amd 

1. Well, it comes as a surprise that a fresh debian 12 install doesn't have any issue. I cannot reproduce anymore because i reinstalled from scratch. The previous install was not modified either (apart from debian stable packages). There was one issue with compiler failing on syntax, and another error with a kernel struct not having the fields required by amdgpu-dkms code… the kernel was a `6.1.0-30` just as yours and same as this fresh install. Weird.

Now, there is another issue:

```
$ sudo modprobe amdgpu
modprobe: ERROR: could not insert 'amdgpu': Key was rejected by service
```

I guess this is a signing issue.

Before going into the rabbit hole, is there any benefit at using `amdgpu-dkms` driver instead of the one provided by distro, since it’s working?

With distro's module and thanks to `amd-smi metric` i can clearly see GPU usage when running models through LM-Studio or just tensorflow directly (which identifies the GPU and everything).

2. I installed the package but sourcing the profile.d file was the missing step. However even when sourcing it, `module avail` doesn't list rocm.

---

### 评论 #3 — harkgill-amd (2025-02-03T22:14:15Z)

That does look like a signing issue. I'd recommend either disabling Secure boot or signing the kernel driver modules with a machine owner key as highlighted in the [amdgpu-install docs](https://amdgpu-install.readthedocs.io/en/latest/install-installing.html#secure-boot-support).

> Is there any benefit at using amdgpu-dkms driver instead of the one provided by distro, since it’s working

The `amdgpu-dkms` packaged with ROCm is optimized/tested for compute workloads and it's a hard requirement. I'm curious to see the dkms version currently installed on your system as you mentioned the build was successful. Also, without the amdgpu module loaded, neither `rocminfo` nor `amd-smi`/`rocm-smi` would function correctly. To double check both of these, could you please provide the output of `sudo dkms status` and `lsmod | grep amd`?

> However even when sourcing it, module avail doesn't list rocm.

`module avail` will show the default modules provided with the installation of the `environment-modules` package. To utilize ROCm with modules, you will have to create a modulefile that points to a specific ROCm installation. The [modulefile documentation ](https://modules.readthedocs.io/en/latest/modulefile.html#modulefile) covers this creation process and much more. Once the modulefile is created in `/usr/share/modules/modulefiles`, it will appear in the `module avail` command.

---

### 评论 #4 — fpeterschmitt (2025-02-03T22:24:10Z)

> That does look like a signing issue. I'd recommend either disabling Secure boot or signing the kernel driver modules with a machine owner key as highlighted in the [amdgpu-install docs](https://amdgpu-install.readthedocs.io/en/latest/install-installing.html#secure-boot-support).

I might give it a shot at a later occasion. Thanks, didn't know those docs.

> > Is there any benefit at using amdgpu-dkms driver instead of the one provided by distro, since it’s working
> 
> The `amdgpu-dkms` packaged with ROCm is optimized/tested for compute workloads and it's a hard requirement. I'm curious to see the dkms version currently installed on your system as you mentioned the build was successful. Also, without the amdgpu module loaded, neither `rocminfo` nor `amd-smi` would function correctly. To double check both of these, could you please provide the output of `sudo dkms status` and `lsmod | grep amd`?

It is built, but cannot load as mentioned earlier. I'm using the distro's `amdgpu` module and tensorflow / lmstudio are both successfully using the GPU as backend.

```
# lsmod |grep amd
edac_mce_amd           40960  0
amdgpu               9617408  18
gpu_sched              53248  1 amdgpu
drm_buddy              20480  1 amdgpu
video                  65536  2 asus_wmi,amdgpu
i2c_algo_bit           16384  1 amdgpu
drm_display_helper    184320  1 amdgpu
drm_ttm_helper         16384  1 amdgpu
ttm                    94208  2 amdgpu,drm_ttm_helper
drm_kms_helper        212992  4 drm_display_helper,amdgpu
gpio_amdpt             20480  0
drm                   614400  15 gpu_sched,drm_kms_helper,drm_display_helper,drm_buddy,amdgpu,drm_ttm_helper,ttm
gpio_generic           16384  1 gpio_amdpt
```

```
$ python check.py 
2025-02-03 23:17:38.644305: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
TensorFlow version: 2.17.0
/home/xxx/rnn/venv/lib/python3.12/site-packages/keras/src/layers/reshaping/flatten.py:37: UserWarning: Do not pass an `input_shape`/`input_dim` argument to a layer. When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead.
  super().__init__(**kwargs)
2025-02-03 23:17:54.022476: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-02-03 23:17:56.771871: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-02-03 23:17:56.771944: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-02-03 23:17:56.773624: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-02-03 23:17:56.773706: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-02-03 23:17:56.773752: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-02-03 23:17:56.773834: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-02-03 23:17:56.773904: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-02-03 23:17:56.773979: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-02-03 23:17:56.774009: I tensorflow/core/common_runtime/gpu/gpu_device.cc:2021] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 23470 MB memory:  -> device: 0, name: Radeon RX 7900 XTX, pci bus id: 0000:09:00.0
^[[1;5HEpoch 1/5
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1738621079.039003  371090 service.cc:146] XLA service 0x7ff770007340 initialized for platform ROCM (this does not guarantee that XLA will be used). Devices:
I0000 00:00:1738621079.039052  371090 service.cc:154]   StreamExecutor device (0): Radeon RX 7900 XTX, AMDGPU ISA version: gfx1100
2025-02-03 23:17:59.051944: I tensorflow/compiler/mlir/tensorflow/utils/dump_mlir_util.cc:268] disabling MLIR crash reproducer, set env var `MLIR_CRASH_REPRODUCER_DIRECTORY` to enable.
I0000 00:00:1738621080.962502  371090 device_compiler.h:188] Compiled cluster using XLA!  This line is logged at most once for the lifetime of the process.
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 6s 2ms/step - accuracy: 0.8593 - loss: 0.4818    
Epoch 2/5
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 4s 2ms/step - accuracy: 0.9541 - loss: 0.1513  
Epoch 3/5
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 4s 2ms/step - accuracy: 0.9670 - loss: 0.1098  
Epoch 4/5
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 4s 2ms/step - accuracy: 0.9740 - loss: 0.0876  
Epoch 5/5
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 4s 2ms/step - accuracy: 0.9753 - loss: 0.0768  
313/313 - 2s - 5ms/step - accuracy: 0.9782 - loss: 0.0703
```

When IDLE:

```
# amd-smi metric|grep CLK|head -n 3
            CLK: 42 MHz
            MIN_CLK: 42 MHz
            MAX_CLK: 2526 MHz
```

When loaded with TF training (using the example on ROCm doc):

```
# amd-smi metric|grep CLK|head -n 20
            CLK: 1249 MHz
            MIN_CLK: 500 MHz
            MAX_CLK: 2526 MHz
```

And when using lm-studio with a 19GB model, GPU and VRAM usage show matching metrics. CPU is not doing anything. If i disable gpu offload from lmm-studio, CPU is doing all the work and it's super slow, obviously.

> > However even when sourcing it, module avail doesn't list rocm.
> 
> `module avail` will show the default modules provided with the installation of the `environment-modules` package. To utilize ROCm with modules, you will have to create a modulefile that points to a specific ROCm installation. The [modulefile documentation ](https://modules.readthedocs.io/en/latest/modulefile.html#modulefile) covers this creation process and much more. Once the modulefile is created in `/usr/share/modules/modulefiles`, it will appear in the `module avail` command.

Ah ok i didn't get that the file was left to the user to create.



---

### 评论 #5 — harkgill-amd (2025-02-04T19:13:44Z)

> I'm using the distro's amdgpu module and tensorflow / lmstudio are both successfully using the GPU as backend.

Got it, sorry for the confusion. This will work but the feature sets are not guaranteed. It's also not officially supported as there's no internal testing or optimization for this pairing (distro amdgpu + ROCm). Our amdgpu-dkms package is a newer version of this module as such, product and feature availability may be lacking on your current configuration. 

> I might give it a shot at a later occasion. Thanks, didn't know those docs.

Great! We are working on updating the ROCm documentation to have more visibility on Secure Boot related troubleshooting. Feel free to create a new issue if you're still encountering difficulties after following the amdgpu-install docs. 

---

### 评论 #6 — fpeterschmitt (2025-02-04T20:20:38Z)

> > I'm using the distro's amdgpu module and tensorflow / lmstudio are both successfully using the GPU as backend.
> 
> Got it, sorry for the confusion. This will work but the feature sets are not guaranteed. It's also not officially supported as there's no internal testing or optimization for this pairing (distro amdgpu + ROCm). Our amdgpu-dkms package is a newer version of this module as such, product and feature availability may be lacking on your current configuration.

Alright 👍 

> > I might give it a shot at a later occasion. Thanks, didn't know those docs.
> 
> Great! We are working on updating the ROCm documentation to have more visibility on Secure Boot related troubleshooting. Feel free to create a new issue if you're still encountering difficulties after following the amdgpu-install docs.

In terms of documentation, i had to rely on https://wiki.debian.org/SecureBoot#MOK_-_Machine_Owner_Key to perform DKMS key enrollment. The key is exactly where this documentation shows, maybe consider adding this to your docs?



Now, the module load correctly and `modinfo amdgpu` shows that it is the DKMS module.

There was some firmware related messages though:

```
W: Possible missing firmware /lib/firmware/amdgpu/ip_discovery.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/vega10_cap.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/navi12_cap.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/aldebaran_cap.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/gc_11_0_0_toc.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/gc_12_0_1_toc.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/gc_12_0_0_toc.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/gc_11_0_4_mes.bin for module amdgpu
W: Possible missing firmware /lib/firmware/amdgpu/gc_11_0_3_mes.bin for module amdgpu
```

However i now have stuttering/freeze. I installed using `amdgpu-install --usecase=workstation`.

Any possibility for it to be related to firmware?

`dmesg | grep amd` seems okay:

```
# dmesg |grep amd 
[    0.000000] Linux version 6.1.0-30-amd64 (debian-kernel@lists.debian.org) (gcc-12 (Debian 12.2.0-14) 12.2.0, GNU ld (GNU Binutils for Debian) 2.40) #1 SMP PREEMPT_DYNAMIC Debian 6.1.124-1 (2025-01-12)
[    0.000000] Command line: BOOT_IMAGE=/vmlinuz-6.1.0-30-amd64 root=UUID=0162acaf-1924-4e08-8546-22f983a2c9d3 ro rootflags=subvol=@rootfs quiet
[    0.010551] Kernel command line: BOOT_IMAGE=/vmlinuz-6.1.0-30-amd64 root=UUID=0162acaf-1924-4e08-8546-22f983a2c9d3 ro rootflags=subvol=@rootfs quiet
[    0.010581] Unknown kernel command line parameters "BOOT_IMAGE=/vmlinuz-6.1.0-30-amd64", will be passed to user space.
[    0.647781] amd_uncore: 4  amd_df counters detected
[    0.647788] amd_uncore: 6  amd_l3 counters detected
[    0.648184] perf/amd_iommu: Detected AMD IOMMU #0 (2 banks, 4 counters/bank).
[    1.314113]     BOOT_IMAGE=/vmlinuz-6.1.0-30-amd64
[    1.840953] usb usb1: Manufacturer: Linux 6.1.0-30-amd64 xhci-hcd
[    1.852215] usb usb2: Manufacturer: Linux 6.1.0-30-amd64 xhci-hcd
[    1.858474] usb usb3: Manufacturer: Linux 6.1.0-30-amd64 xhci-hcd
[    1.858773] usb usb4: Manufacturer: Linux 6.1.0-30-amd64 xhci-hcd
[    5.720430] amdkcl: loading out-of-tree module taints kernel.
[    7.376255] [drm] amdgpu kernel modesetting enabled.
[    7.376256] [drm] amdgpu version: 6.10.5
[    7.383249] amdgpu: Virtual CRAT table created for CPU
[    7.383261] amdgpu: Topology: Add CPU node
[    7.386315] amdgpu 0000:09:00.0: enabling device (0006 -> 0007)
[    7.390962] amdgpu 0000:09:00.0: amdgpu: Fetched VBIOS from VFCT
[    7.390964] amdgpu: ATOM BIOS: 113-4E4710U-T52
[    7.391004] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/psp_13_0_0_sos.bin
[    7.391034] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/psp_13_0_0_ta.bin
[    7.391069] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/smu_13_0_0.bin
[    7.391104] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/dcn_3_2_0_dmcub.bin
[    7.391136] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_pfp.bin
[    7.391139] amdgpu 0000:09:00.0: amdgpu: CP RS64 enable
[    7.391181] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_me.bin
[    7.391206] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_rlc.bin
[    7.391253] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_mec.bin
[    7.391276] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_imu.bin
[    7.391293] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/sdma_6_0_0.bin
[    7.391338] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/vcn_4_0_0.bin
[    7.391375] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_mes_2.bin
[    7.391403] amdgpu 0000:09:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_mes1.bin
[    7.391497] amdgpu 0000:09:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[    7.391526] amdgpu 0000:09:00.0: amdgpu: MEM ECC is not presented.
[    7.391527] amdgpu 0000:09:00.0: amdgpu: SRAM ECC is not presented.
[    7.391541] amdgpu 0000:09:00.0: amdgpu: VRAM: 24560M 0x0000008000000000 - 0x00000085FEFFFFFF (24560M used)
[    7.391543] amdgpu 0000:09:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[    7.391609] [drm] amdgpu: 24560M of VRAM memory ready
[    7.391610] [drm] amdgpu: 15999M of GTT memory ready.
[    7.462804] amdgpu 0000:09:00.0: amdgpu: reserve 0x1300000 from 0x85fc000000 for PSP TMR
[    7.608152] amdgpu 0000:09:00.0: amdgpu: RAP: optional rap ta ucode is not available
[    7.608154] amdgpu 0000:09:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[    7.608250] amdgpu 0000:09:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e7f00 (78.127.0)
[    7.608254] amdgpu 0000:09:00.0: amdgpu: SMU driver if version not matched
[    7.775374] amdgpu 0000:09:00.0: amdgpu: SMU is initialized successfully!
[    8.176270] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[    8.176283] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[    8.176314] amdgpu: Virtual CRAT table created for GPU
[    8.176629] amdgpu: Topology: Add dGPU node [0x744c:0x1002]
[    8.176630] kfd kfd: amdgpu: added device 1002:744c
[    8.176642] amdgpu 0000:09:00.0: amdgpu: SE 6, SH per SE 2, CU per SH 8, active_cu_number 96
[    8.176646] amdgpu 0000:09:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[    8.176647] amdgpu 0000:09:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[    8.176649] amdgpu 0000:09:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[    8.176650] amdgpu 0000:09:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[    8.176651] amdgpu 0000:09:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[    8.176652] amdgpu 0000:09:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[    8.176654] amdgpu 0000:09:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[    8.176655] amdgpu 0000:09:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[    8.176656] amdgpu 0000:09:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[    8.176657] amdgpu 0000:09:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[    8.176659] amdgpu 0000:09:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[    8.176660] amdgpu 0000:09:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[    8.176661] amdgpu 0000:09:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[    8.176662] amdgpu 0000:09:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[    8.176664] amdgpu 0000:09:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[    8.179484] amdgpu 0000:09:00.0: amdgpu: Using BACO for runtime pm
[    8.179855] [drm] Initialized amdgpu 3.59.0 20150101 for 0000:09:00.0 on minor 0
[    8.185690] fbcon: amdgpudrmfb (fb0) is primary device
[    8.420209] amdgpu 0000:09:00.0: [drm] fb0: amdgpudrmfb frame buffer device
[   16.304172] kvm: support for 'kvm_amd' disabled by bios
[   16.642075] snd_hda_intel 0000:09:00.1: bound 0000:09:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
```

Should i open another issue?

**Edit:** i will uninstall amdgpu components and reinstall using only `--usecase=dkms` so that mesa libs are still provided by the OS to see if it could that.

**Edit2:** not sure if it solves the issue, but i have less stutter. Seems that workstation and possibly "graphics" targets install lib versions that are not working well with GNOME.

---

### 评论 #7 — harkgill-amd (2025-02-04T20:54:12Z)

The firmware warnings highlighted are unrelated. Which GPU are you using? Could you also try a `graphics` usecase installation with `amdgpu-install --usecase=graphics,rocm` to see if that resolves the stuttering?

---

### 评论 #8 — fpeterschmitt (2025-02-04T21:06:30Z)

RX 7900 XTX

I went for `--usecase=dkms,rocm` (after deinstalling everything with `amdgpu-uninstall`) which seems to be perfect 👌 

---

### 评论 #9 — harkgill-amd (2025-02-04T22:03:13Z)

Glad to hear it's working on your end. Feel free to close out this ticket if your issue has been resolved.

---

### 评论 #10 — fpeterschmitt (2025-02-05T13:25:30Z)

> Glad to hear it's working on your end. Feel free to close out this ticket if your issue has been resolved.

I will, so to summarize i think the docs could be updated to:

* provide Debian link for DKMS signed module loading with SecureBoot
* provide amdgpu-installer documentation link as well
* warn about potential graphical rendering issues when installing amd's mesa libraries?

Some of those could be put in troubleshooting, but also those pages: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-debian.html#install-kernel-driver and https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#kernel-headers-and-development-packages don't mention this at all.


Thanks for your assistance!



---

### 评论 #11 — harkgill-amd (2025-02-06T20:42:45Z)

The first and second points relate to the lack of Secure Boot documentation which is already being tracked in https://github.com/ROCm/ROCm/issues/4328. The new documentation intends to cover topics in both the Debian and amdgpu-install docs, specifically how to use a machine owner key to sign the kernel modules. 

As for the graphical issues, the ROCm 6.3.2 release is technically meant for a headless configuration. There are separate ROCm releases (see [ROCm on Radeon](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-radeon.html)) that are intended for graphical use cases where a physical display is attached. With that being said, the regular ROCm releases with the graphics use case often resolves most common issues and is recommended in the [Use cases](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/amdgpu-installer/amdgpu-installer-debian.html#use-cases) documentation. 

```
graphics        (for users of graphics applications)
  - Open source Mesa 3D graphics and multimedia libraries
```

Edit: Just gave the graphics usecase install a try on my end and everything looks good. 

---

### 评论 #12 — harkgill-amd (2025-02-28T15:41:35Z)

Closing this issue out. Please leave a comment if you have any further questions.

---
