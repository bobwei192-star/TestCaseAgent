# AMDGPU DKMS Not Compiling Linux 6.1.52

> **Issue #2451**
> **状态**: closed
> **创建时间**: 2023-09-13T02:33:25Z
> **更新时间**: 2024-04-19T10:23:07Z
> **关闭时间**: 2023-11-10T15:55:59Z
> **作者**: blu006
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2451

## 描述

Compiling the AMDGPU present in the jammy repository (1:6.1.5.50600-1609671.20.04) against kernel headers version 6.1.52 

```
CC [M]  /var/lib/dkms/amdgpu/6.1.5-1609671.20.04/build/amd/amdgpu/../display/dc/basics/vector.o
/var/lib/dkms/amdgpu/6.1.5-1609671.20.04/build/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm.c: In function ‘dm_handle_mst_sideband_msg’:
/var/lib/dkms/amdgpu/6.1.5-1609671.20.04/build/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm.c:3314:25: error: implicit declaration of function ‘drm_dp_mst_hpd_irq’; did you mean ‘drm_dp_mst_dpcd_write’? [-Werror=implicit-function-declaration]
 3314 |                         drm_dp_mst_hpd_irq(
      |                         ^~~~~~~~~~~~~~~~~~
      |                         drm_dp_mst_dpcd_write
  CC [M]  /var/lib/dkms/amdgpu/6.1.5-1609671.20.04/build/amd/amdgpu/../display/dc/basics/dc_common.o
```

A similar issue was reported on another project https://github.com/strongtz/i915-sriov-dkms/issues/97 I believe the summary from that issue was something like drm_dp_mst_hpd_irq() being split into multiple functions in a later kernel (6.4?) and that change being backported to later versions of kernel 6.1.

Unfortunately, I am not familiar enough with the codebase to make any changes to the code.

---

## 评论 (18 条)

### 评论 #1 — dsteinmo (2023-09-15T22:01:41Z)

I'm seeing this as well on Debian 12 bookworm. 

---

### 评论 #2 — tuleo1 (2023-09-16T17:48:02Z)

mine doesn't work either but mine is different. when checking on the makebuild.log all i get is this 
`error dma_resv->seq is missing. exit...`
I have no idea how or why it's happening
 i tried to build this both on 6.1.0 and 6.4 and 6.5 kernel and all 3 don't build with the same error

---

### 评论 #3 — feiyax (2023-09-25T22:36:55Z)

Looks like 6.1.0-12 has [this](https://github.com/torvalds/linux/commit/104d79eb58aa63330e9cbcb5095177c234b9c859#diff-64c40ff9cbb474c836acf8b162cd955aece5344841961b7defba295f948ff1eeL818) ported in, which removed `drm_dp_mst_hpd_irq()`. 

I'm on Debian bookworm, and i ended up rolling back to 6.10.0-11 for now, until a proper fix comes in.

```
$ diff -u $PWD/linux*/include/drm/display/drm_dp_mst_helper.h
--- /usr/src/linux-headers-6.1.0-11-common/include/drm/display/drm_dp_mst_helper.h      2023-07-05 12:27:38.000000000 -0500
+++ /usr/src/linux-headers-6.1.0-12-common/include/drm/display/drm_dp_mst_helper.h      2023-09-06 15:27:03.000000000 -0500
@@ -815,8 +815,11 @@
 bool drm_dp_read_mst_cap(struct drm_dp_aux *aux, const u8 dpcd[DP_RECEIVER_CAP_SIZE]);
 int drm_dp_mst_topology_mgr_set_mst(struct drm_dp_mst_topology_mgr *mgr, bool mst_state);

-int drm_dp_mst_hpd_irq(struct drm_dp_mst_topology_mgr *mgr, u8 *esi, bool *handled);
-
+int drm_dp_mst_hpd_irq_handle_event(struct drm_dp_mst_topology_mgr *mgr,
+                                   const u8 *esi,
+                                   u8 *ack,
+                                   bool *handled);
+void drm_dp_mst_hpd_irq_send_new_request(struct drm_dp_mst_topology_mgr *mgr);

 int
 drm_dp_mst_detect_port(struct drm_connector *connector,
```

I also tried grabbing the diff from [the commit](https://github.com/torvalds/linux/commit/72f1de49ffb90b29748284f27f1d6b829ab1de95) and i can see it apply cleanly, so maybe someone can check to confirm if that works or not. (I didn't actually install it yet). For reference: 

```
$ git -C linux show  72f1de4 -- drivers/gpu/drm/amd/display/amdgpu_dm/amdgpu_dm.c | patch --dry-run  /usr/src/amdgpu-6.2.4-1637781.22.04/amd/display/amdgpu_dm/amdgpu_dm.c
File /usr/src/amdgpu-6.2.4-1637781.22.04/amd/display/amdgpu_dm/amdgpu_dm.c is read-only; trying to patch anyway
checking file /usr/src/amdgpu-6.2.4-1637781.22.04/amd/display/amdgpu_dm/amdgpu_dm.c
Hunk #1 succeeded at 3289 with fuzz 2 (offset 22 lines).
Hunk #2 succeeded at 3299 (offset 23 lines).
```



---

### 评论 #4 — barchstien (2023-11-03T00:08:38Z)

I get it too on Ubuntu 23.04 when trying to run apt upgrade which installs kernel 6.2.0-36
I've reverted to 6.2.0-35

---

### 评论 #5 — jadefennec (2023-11-03T04:41:13Z)

> I get it too on Ubuntu 23.04 when trying to run apt upgrade which installs kernel 6.2.0-36 I've reverted to 6.2.0-35

Same here. Here's my errors in make.log:

`/var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/amd/amdgpu/amdgpu_amdkfd.c: In function ‘amdgpu_amdkfd_unmap_hiq’:
/var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/amd/amdgpu/amdgpu_amdkfd.c:880:1: warning: the frame size of 1280 bytes is larger than 1024 >
  880 | }
      | ^
`

`/var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm.c: In function ‘dm_handle_mst_sideband_msg’:
/var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm.c:3301:25: error: implicit declaration of function>
 3301 |                         drm_dp_mst_hpd_irq(
      |                         ^~~~~~~~~~~~~~~~~~
      |                         drm_dp_mst_dpcd_write
`

Occurring for 6.2.0-36, on version 6.2.4-1646729.22.04. Looks like this is a new issue.

---

### 评论 #6 — kentrussell (2023-11-10T15:56:00Z)

drm_dp_mst_hpd_irq should be handled in the 5.7.* releases. 5.6 was based off of the 6.1 kernel, so 6.2 wasn't tested with it (see https://rocm.docs.amd.com/en/docs-5.6.1/release/gpu_os_support.html) . For 5.7.1, we support a 6.2-based kernel (https://rocm.docs.amd.com/en/docs-5.7.1/release/gpu_os_support.html). Please give that a shot, and reopen if the issue persists. Note that some releases may work with some kernel versions, but the official support list there will detail what kernels we've compiled against. Always good to reference that when getting a compilation failure in the kernel.

---

### 评论 #7 — Flashwalker (2024-02-05T20:56:24Z)

Same fail on 6.5.4 and 6.6.6 kernels on Ubuntu 22.04



---

### 评论 #8 — kentrussell (2024-02-05T21:41:35Z)

@Flashwalker Just to clarify, you have drm_dp_mst_hpd_irq being undefined in 6.5.4 and 6.6.6? Have you tried the HWE kernel specifically? The crew in charge of documentation say that the 6.6-based HWE kernel is preview-supported. Officially full support is still just 6.2 for UB22 (see https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.0.0/reference/system-requirements.html)

---

### 评论 #9 — Flashwalker (2024-02-06T07:25:05Z)

> @Flashwalker Just to clarify, you have drm_dp_mst_hpd_irq being undefined in 6.5.4 and 6.6.6? Have you tried the HWE kernel specifically? The crew in charge of documentation say that the 6.6-based HWE kernel is preview-supported. Officially full support is still just 6.2 for UB22 (see https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.0.0/reference/system-requirements.html)

Here is my logs:

<details>
<summary>Installation stdout</summary>

```
 $ amdgpu-install
Чтение списков пакетов… Готово
Построение дерева зависимостей… Готово
Чтение информации о состоянии… Готово         
Уже установлен пакет linux-headers-6.6.6-76060606-generic самой новой версии (6.6.6-76060606.202312111032~1702306143~22.04~d28ffec).
linux-headers-6.6.6-76060606-generic помечен как установленный вручную.
Следующие пакеты устанавливались автоматически и больше не требуются:
  bbswitch-dkms gir1.2-matepanelapplet-4.0 glib-networking:i386 libfftw3-single3:i386 libgomp1:i386 libice6:i386 libjson-glib-1.0-0:i386 libproxy1v5:i386 libpulsedsp:i386 libqt5location5-plugins libqt5positioning5-plugins libsm6:i386
  libsnapd-glib1:i386 libsoup2.4-1:i386 libsoxr0:i386 libspeexdsp1:i386 libtdb1:i386 libwebrtc-audio-processing1:i386 libxtst6:i386 qml-module-qt-labs-location qml-module-qtlocation qml-module-qtpositioning
Для их удаления используйте «sudo apt autoremove».
Будут установлены следующие дополнительные пакеты:
  amdgpu-core amdgpu-dkms-firmware comgr g++-11-multilib g++-multilib gcc-11-multilib gcc-multilib gst-omx-amdgpu hip-dev hip-runtime-amd hipcc hsa-rocr hsa-rocr-dev hsakmt-roct-dev lib32asan6 lib32atomic1 lib32gcc-11-dev lib32gomp1 lib32itm1
  lib32quadmath0 lib32stdc++-11-dev lib32ubsan1 libc-dev-bin libc6 libc6:i386 libc6-dbg libc6-dev libc6-dev-i386 libc6-dev-x32 libc6-i386 libc6-x32 libdrm-amdgpu-amdgpu1 libdrm-amdgpu-amdgpu1:i386 libdrm-amdgpu-common libdrm-amdgpu-dev
  libdrm-amdgpu-radeon1 libdrm-amdgpu-radeon1:i386 libdrm2-amdgpu libdrm2-amdgpu:i386 libegl1-amdgpu-mesa libegl1-amdgpu-mesa:i386 libegl1-amdgpu-mesa-drivers libegl1-amdgpu-mesa-drivers:i386 libgbm1-amdgpu libgbm1-amdgpu:i386
  libgl1-amdgpu-mesa-dri libgl1-amdgpu-mesa-dri:i386 libgl1-amdgpu-mesa-glx libgl1-amdgpu-mesa-glx:i386 libglapi-amdgpu-mesa libglapi-amdgpu-mesa:i386 libllvm17.0.60001-amdgpu libllvm17.0.60001-amdgpu:i386 libomxil-bellagio-bin
  libomxil-bellagio0 libva-amdgpu-drm2 libva-amdgpu-drm2:i386 libva-amdgpu-glx2 libva-amdgpu-glx2:i386 libva-amdgpu-wayland2 libva-amdgpu-wayland2:i386 libva-amdgpu-x11-2 libva-amdgpu-x11-2:i386 libva2-amdgpu libva2-amdgpu:i386 libvdpau1:i386
  libwayland-amdgpu-client0 libwayland-amdgpu-client0:i386 libwayland-amdgpu-server0 libwayland-amdgpu-server0:i386 libx32asan6 libx32atomic1 libx32gcc-11-dev libx32gcc-s1 libx32gomp1 libx32itm1 libx32quadmath0 libx32stdc++-11-dev
  libx32stdc++6 libx32ubsan1 libxatracker2-amdgpu libxatracker2-amdgpu:i386 mesa-amdgpu-omx-drivers mesa-amdgpu-va-drivers mesa-amdgpu-va-drivers:i386 mesa-amdgpu-vdpau-drivers mesa-amdgpu-vdpau-drivers:i386 mesa-vdpau-drivers
  mesa-vdpau-drivers:i386 mokutil openmp-extras-runtime rocm-core rocm-language-runtime rocm-llvm rocm-ocl-icd rocm-opencl rocminfo shim-signed valgrind vdpau-driver-all:i386 xserver-xorg-amdgpu-video-amdgpu
Предлагаемые пакеты:
  lib32stdc++6-11-dbg libx32stdc++6-11-dbg glibc-doc glibc-doc:i386 locales:i386 libglide3 libglide3:i386 libomxil-bellagio0-components-base valgrind-dbg valgrind-mpi kcachegrind alleyoop valkyrie libvdpau-va-gl1:i386
Рекомендуемые пакеты:
  libc-devtools libtxc-dxtn-s2tc0 | libtxc-dxtn0 libtxc-dxtn-s2tc0:i386 | libtxc-dxtn0:i386
Следующие НОВЫЕ пакеты будут установлены:
  amdgpu-core amdgpu-dkms amdgpu-dkms-firmware amdgpu-lib amdgpu-lib32 comgr g++-11-multilib g++-multilib gcc-11-multilib gcc-multilib gst-omx-amdgpu hip-dev hip-runtime-amd hipcc hsa-rocr hsa-rocr-dev hsakmt-roct-dev lib32asan6 lib32atomic1
  lib32gcc-11-dev lib32gomp1 lib32itm1 lib32quadmath0 lib32stdc++-11-dev lib32ubsan1 libc6-dev-i386 libc6-dev-x32 libc6-x32 libdrm-amdgpu-amdgpu1 libdrm-amdgpu-amdgpu1:i386 libdrm-amdgpu-common libdrm-amdgpu-dev libdrm-amdgpu-radeon1
  libdrm-amdgpu-radeon1:i386 libdrm2-amdgpu libdrm2-amdgpu:i386 libegl1-amdgpu-mesa libegl1-amdgpu-mesa:i386 libegl1-amdgpu-mesa-drivers libegl1-amdgpu-mesa-drivers:i386 libgbm1-amdgpu libgbm1-amdgpu:i386 libgl1-amdgpu-mesa-dri
  libgl1-amdgpu-mesa-dri:i386 libgl1-amdgpu-mesa-glx libgl1-amdgpu-mesa-glx:i386 libglapi-amdgpu-mesa libglapi-amdgpu-mesa:i386 libllvm17.0.60001-amdgpu libllvm17.0.60001-amdgpu:i386 libomxil-bellagio-bin libomxil-bellagio0 libva-amdgpu-drm2
  libva-amdgpu-drm2:i386 libva-amdgpu-glx2 libva-amdgpu-glx2:i386 libva-amdgpu-wayland2 libva-amdgpu-wayland2:i386 libva-amdgpu-x11-2 libva-amdgpu-x11-2:i386 libva2-amdgpu libva2-amdgpu:i386 libvdpau1:i386 libwayland-amdgpu-client0
  libwayland-amdgpu-client0:i386 libwayland-amdgpu-server0 libwayland-amdgpu-server0:i386 libx32asan6 libx32atomic1 libx32gcc-11-dev libx32gcc-s1 libx32gomp1 libx32itm1 libx32quadmath0 libx32stdc++-11-dev libx32stdc++6 libx32ubsan1
  libxatracker2-amdgpu libxatracker2-amdgpu:i386 mesa-amdgpu-omx-drivers mesa-amdgpu-va-drivers mesa-amdgpu-va-drivers:i386 mesa-amdgpu-vdpau-drivers mesa-amdgpu-vdpau-drivers:i386 mesa-vdpau-drivers:i386 mokutil openmp-extras-runtime
  rocm-core rocm-hip-runtime rocm-language-runtime rocm-llvm rocm-ocl-icd rocm-opencl rocm-opencl-runtime rocminfo shim-signed valgrind vdpau-driver-all:i386 xserver-xorg-amdgpu-video-amdgpu
Следующие пакеты будут обновлены:
  libc-dev-bin libc6 libc6:i386 libc6-dbg libc6-dev libc6-i386 mesa-vdpau-drivers
Обновлено 7 пакетов, установлено 99 новых пакетов, для удаления отмечено 0 пакетов, и 230 пакетов не обновлено.
Необходимо скачать 1 669 MB архивов.
После данной операции объём занятого дискового пространства возрастёт на 1 637 MB.
Хотите продолжить? [Д/н] 
Пол:1 http://apt.pop-os.org/release jammy/main amd64 mesa-vdpau-drivers amd64 23.3.2-1pop0~1704238321~22.04~36f1d0e [3 773 kB]
Пол:2 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libc6-i386 amd64 2.35-0ubuntu3.6 [2 837 kB]
Пол:3 http://apt.pop-os.org/release jammy/main i386 mesa-vdpau-drivers i386 23.3.2-1pop0~1704238321~22.04~36f1d0e [4 120 kB]                       
Пол:4 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 amdgpu-core all 1:6.0.60001-1710620.22.04 [2 232 B]       
Пол:5 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libc6-dev amd64 2.35-0ubuntu3.6 [2 100 kB]
Пол:6 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libdrm2-amdgpu i386 1:2.4.116.60001-1710620.22.04 [39,2 kB]
Пол:7 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libglapi-amdgpu-mesa i386 1:23.3.0.60001-1710620.22.04 [23,4 kB]
Пол:8 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libgl1-amdgpu-mesa-glx i386 1:23.3.0.60001-1710620.22.04 [153 kB]
Пол:9 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libc-dev-bin amd64 2.35-0ubuntu3.6 [20,3 kB]
Пол:10 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libc6-dbg amd64 2.35-0ubuntu3.6 [13,8 MB]
Пол:11 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libva2-amdgpu i386 2.16.0.60001-1710620.22.04 [51,1 kB]
Пол:12 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libva-amdgpu-drm2 i386 2.16.0.60001-1710620.22.04 [7 696 B]
Пол:13 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libva-amdgpu-x11-2 i386 2.16.0.60001-1710620.22.04 [12,5 kB]
Пол:14 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libva-amdgpu-glx2 i386 2.16.0.60001-1710620.22.04 [11,3 kB]
Пол:15 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libwayland-amdgpu-client0 i386 1.22.0.60001-1710620.22.04 [26,0 kB]
Пол:16 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libva-amdgpu-wayland2 i386 2.16.0.60001-1710620.22.04 [9 552 B]
Пол:17 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libdrm-amdgpu-common all 1.0.0.60001-1716197.22.04 [5 096 B]
Пол:18 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libdrm-amdgpu-amdgpu1 i386 1:2.4.116.60001-1710620.22.04 [24,2 kB]
Пол:19 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libdrm-amdgpu-radeon1 i386 1:2.4.116.60001-1710620.22.04 [23,2 kB]
Пол:20 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libllvm17.0.60001-amdgpu i386 1:17.0.60001-1710620.22.04 [25,5 MB]
Пол:21 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 mesa-amdgpu-va-drivers i386 1:23.3.0.60001-1710620.22.04 [3 404 kB]                                                                                                              
Пол:22 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libgl1-amdgpu-mesa-dri i386 1:23.3.0.60001-1710620.22.04 [6 278 kB]                                                                                                              
Пол:23 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libdrm2-amdgpu amd64 1:2.4.116.60001-1710620.22.04 [37,6 kB]                                                                                                                    
Пол:24 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libglapi-amdgpu-mesa amd64 1:23.3.0.60001-1710620.22.04 [23,3 kB]                                                                                                               
Пол:25 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libgl1-amdgpu-mesa-glx amd64 1:23.3.0.60001-1710620.22.04 [143 kB]                                                                                                              
Пол:26 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libva2-amdgpu amd64 2.16.0.60001-1710620.22.04 [52,7 kB]                                                                                                                        
Пол:27 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libva-amdgpu-drm2 amd64 2.16.0.60001-1710620.22.04 [7 492 B]                                                                                                                    
Пол:28 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libva-amdgpu-x11-2 amd64 2.16.0.60001-1710620.22.04 [12,3 kB]                                                                                                                   
Пол:29 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libva-amdgpu-glx2 amd64 2.16.0.60001-1710620.22.04 [11,2 kB]                                                                                                                    
Пол:30 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libwayland-amdgpu-client0 amd64 1.22.0.60001-1710620.22.04 [25,6 kB]                                                                                                            
Пол:31 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libva-amdgpu-wayland2 amd64 2.16.0.60001-1710620.22.04 [9 572 B]                                                                                                                
Пол:32 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libdrm-amdgpu-amdgpu1 amd64 1:2.4.116.60001-1710620.22.04 [21,2 kB]                                                                                                             
Пол:33 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libdrm-amdgpu-radeon1 amd64 1:2.4.116.60001-1710620.22.04 [22,6 kB]                                                                                                             
Пол:34 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libllvm17.0.60001-amdgpu amd64 1:17.0.60001-1710620.22.04 [22,6 MB]                                                                                                             
Пол:35 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libc6 amd64 2.35-0ubuntu3.6 [3 236 kB]                                                                                                                                             
Пол:36 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 mesa-amdgpu-va-drivers amd64 1:23.3.0.60001-1710620.22.04 [3 085 kB]                                                                                                            
Пол:37 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libgl1-amdgpu-mesa-dri amd64 1:23.3.0.60001-1710620.22.04 [5 789 kB]                                                                                                            
Пол:38 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 mesa-amdgpu-vdpau-drivers i386 1:23.3.0.60001-1710620.22.04 [3 374 kB]                                                                                                           
Пол:39 http://mirror.timeweb.ru/ubuntu jammy-security/main i386 libc6 i386 2.35-0ubuntu3.6 [3 013 kB]                                                                                                                                               
Пол:40 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 mesa-amdgpu-vdpau-drivers amd64 1:23.3.0.60001-1710620.22.04 [3 055 kB]                                                                                                         
Пол:41 http://mirror.timeweb.ru/ubuntu jammy/main i386 libvdpau1 i386 1.4-3build2 [26,5 kB]                                                                                                                                                         
Пол:42 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 mokutil amd64 0.6.0-2~22.04.2 [27,3 kB]                                                                                                                                            
Пол:43 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 shim-signed amd64 1.51.3+15.7-0ubuntu1 [667 kB]                                                                                                                                    
Пол:44 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 amdgpu-dkms-firmware all 1:6.3.6.60001-1710620.22.04 [12,4 MB]                                                                                                                  
Пол:45 http://mirror.timeweb.ru/ubuntu jammy/universe amd64 libomxil-bellagio0 amd64 0.9.3-7ubuntu1 [37,4 kB]                                                                                                                                       
Пол:46 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libc6-dev-i386 amd64 2.35-0ubuntu3.6 [1 445 kB]                                                                                                                                    
Пол:47 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libc6-x32 amd64 2.35-0ubuntu3.6 [2 978 kB]                                                                                                                                         
Пол:48 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libc6-dev-x32 amd64 2.35-0ubuntu3.6 [1 632 kB]                                                                                                                                     
Пол:49 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 amdgpu-dkms all 1:6.3.6.60001-1710620.22.04 [10,7 MB]                                                                                                                           
Пол:50 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libx32gcc-s1 amd64 12.3.0-1ubuntu1~22.04 [54,0 kB]                                                                                                                                 
Пол:51 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 lib32gomp1 amd64 12.3.0-1ubuntu1~22.04 [133 kB]                                                                                                                                    
Пол:52 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libx32gomp1 amd64 12.3.0-1ubuntu1~22.04 [127 kB]                                                                                                                                   
Пол:53 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 lib32itm1 amd64 12.3.0-1ubuntu1~22.04 [32,0 kB]                                                                                                                                    
Пол:54 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libx32itm1 amd64 12.3.0-1ubuntu1~22.04 [30,2 kB]                                                                                                                                   
Пол:55 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 lib32atomic1 amd64 12.3.0-1ubuntu1~22.04 [8 500 B]                                                                                                                                 
Пол:56 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libx32atomic1 amd64 12.3.0-1ubuntu1~22.04 [10,2 kB]                                                                                                                                
Пол:57 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 lib32asan6 amd64 11.4.0-1ubuntu1~22.04 [2 154 kB]                                                                                                                                  
Пол:58 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libx32asan6 amd64 11.4.0-1ubuntu1~22.04 [2 128 kB]                                                                                                                                 
Пол:59 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libwayland-amdgpu-server0 amd64 1.22.0.60001-1710620.22.04 [33,2 kB]                                                                                                            
Пол:60 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libxatracker2-amdgpu amd64 1:23.3.0.60001-1710620.22.04 [1 537 kB]                                                                                                              
Пол:61 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 lib32ubsan1 amd64 12.3.0-1ubuntu1~22.04 [959 kB]                                                                                                                                   
Пол:62 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libgbm1-amdgpu amd64 1:23.3.0.60001-1710620.22.04 [28,6 kB]                                                                                                                     
Пол:63 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libegl1-amdgpu-mesa amd64 1:23.3.0.60001-1710620.22.04 [118 kB]                                                                                                                 
Пол:64 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libegl1-amdgpu-mesa-drivers amd64 1:23.3.0.60001-1710620.22.04 [4 364 B]                                                                                                        
Пол:65 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 mesa-amdgpu-omx-drivers amd64 1:23.3.0.60001-1710620.22.04 [2 965 kB]                                                                                                           
Пол:66 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libx32stdc++6 amd64 12.3.0-1ubuntu1~22.04 [682 kB]                                                                                                                                 
Пол:67 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 xserver-xorg-amdgpu-video-amdgpu amd64 1:22.0.0.60001-1710620.22.04 [58,4 kB]                                                                                                   
Пол:68 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 gst-omx-amdgpu amd64 1:1.0.0.1.60001-1710620.22.04 [59,0 kB]                                                                                                                    
Пол:69 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 amdgpu-lib amd64 1:6.0.60001-1710620.22.04 [2 124 B]                                                                                                                            
Пол:70 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libwayland-amdgpu-server0 i386 1.22.0.60001-1710620.22.04 [34,3 kB]                                                                                                              
Пол:71 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libx32ubsan1 amd64 12.3.0-1ubuntu1~22.04 [963 kB]                                                                                                                                  
Пол:72 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 lib32quadmath0 amd64 12.3.0-1ubuntu1~22.04 [244 kB]                                                                                                                                
Пол:73 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libx32quadmath0 amd64 12.3.0-1ubuntu1~22.04 [156 kB]                                                                                                                               
Пол:74 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 lib32gcc-11-dev amd64 11.4.0-1ubuntu1~22.04 [2 339 kB]                                                                                                                             
Пол:75 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libxatracker2-amdgpu i386 1:23.3.0.60001-1710620.22.04 [1 710 kB]                                                                                                                
Пол:76 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libgbm1-amdgpu i386 1:23.3.0.60001-1710620.22.04 [30,1 kB]                                                                                                                       
Пол:77 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libegl1-amdgpu-mesa i386 1:23.3.0.60001-1710620.22.04 [128 kB]                                                                                                                   
Пол:78 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main i386 libegl1-amdgpu-mesa-drivers i386 1:23.3.0.60001-1710620.22.04 [4 364 B]                                                                                                          
Пол:79 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 amdgpu-lib32 amd64 1:6.0.60001-1710620.22.04 [1 824 B]                                                                                                                          
Пол:80 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 rocm-core amd64 6.0.1.60001-108~22.04 [9 032 B]                                                                                                                                      
Пол:81 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 comgr amd64 2.6.0.60001-108~22.04 [51,7 MB]                                                                                                                                          
Пол:82 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libx32gcc-11-dev amd64 11.4.0-1ubuntu1~22.04 [2 107 kB]                                                                                                                            
Пол:83 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 gcc-11-multilib amd64 11.4.0-1ubuntu1~22.04 [876 B]                                                                                                                                
Пол:84 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 lib32stdc++-11-dev amd64 11.4.0-1ubuntu1~22.04 [989 kB]                                                                                                                            
Пол:85 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 libx32stdc++-11-dev amd64 11.4.0-1ubuntu1~22.04 [906 kB]                                                                                                                           
Пол:86 http://mirror.timeweb.ru/ubuntu jammy-security/main amd64 g++-11-multilib amd64 11.4.0-1ubuntu1~22.04 [890 B]                                                                                                                                
Пол:87 http://mirror.timeweb.ru/ubuntu jammy/main amd64 gcc-multilib amd64 4:11.2.0-1ubuntu1 [1 382 B]                                                                                                                                              
Пол:88 http://mirror.timeweb.ru/ubuntu jammy/main amd64 g++-multilib amd64 4:11.2.0-1ubuntu1 [854 B]                                                                                                                                                
Пол:89 http://mirror.timeweb.ru/ubuntu jammy/main amd64 valgrind amd64 1:3.18.1-1ubuntu2 [14,1 MB]                                                                                                                                                  
Пол:90 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 hip-dev amd64 6.0.32831.60001-108~22.04 [266 kB]                                                                                                                                     
Пол:91 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 hsa-rocr amd64 1.12.0.60001-108~22.04 [823 kB]                                                                                                                                       
Пол:92 https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy/main amd64 libdrm-amdgpu-dev amd64 1:2.4.116.60001-1710620.22.04 [141 kB]                                                                                                                  
Пол:93 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 hsakmt-roct-dev amd64 20231016.2.245.60001-108~22.04 [376 kB]                                                                                                                        
Пол:94 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 hsa-rocr-dev amd64 1.12.0.60001-108~22.04 [99,0 kB]                                                                                                                                  
Пол:95 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 rocminfo amd64 1.0.0.60001-108~22.04 [31,0 kB]                                                                                                                                       
Пол:96 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 rocm-llvm amd64 17.0.0.24012.60001-108~22.04 [1 275 MB]                                                                                                                              
Пол:97 http://mirror.timeweb.ru/ubuntu jammy/main i386 vdpau-driver-all i386 1.4-3build2 [4 508 B]                                                                                                                                                  
Пол:98 http://mirror.timeweb.ru/ubuntu jammy/universe amd64 libomxil-bellagio-bin amd64 0.9.3-7ubuntu1 [12,8 kB]                                                                                                                                    
Пол:99 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 hipcc amd64 1.0.0.60001-108~22.04 [265 kB]                                                                                                                                           
Пол:100 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 hip-runtime-amd amd64 6.0.32831.60001-108~22.04 [27,1 MB]                                                                                                                           
Пол:101 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 openmp-extras-runtime amd64 17.60.0.60001-108~22.04 [140 MB]                                                                                                                        
Пол:102 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 rocm-language-runtime amd64 6.0.1.60001-108~22.04 [834 B]                                                                                                                           
Пол:103 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 rocm-hip-runtime amd64 6.0.1.60001-108~22.04 [2 036 B]                                                                                                                              
Пол:104 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 rocm-ocl-icd amd64 2.0.0.60001-108~22.04 [16,3 kB]                                                                                                                                  
Пол:105 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 rocm-opencl amd64 2.0.0.60001-108~22.04 [595 kB]                                                                                                                                    
Пол:106 https://repo.radeon.com/rocm/apt/6.0.1 jammy/main amd64 rocm-opencl-runtime amd64 6.0.1.60001-108~22.04 [2 020 B]                                                                                                                           
Получено 1 669 MB за 2мин 8с (13,0 MB/s)                                                                                                                                                                                                            
Извлекаются шаблоны из пакетов: 100%
Предварительная настройка пакетов …
Выбор ранее не выбранного пакета amdgpu-core.
(Чтение базы данных … на данный момент установлено 918192 файла и каталога.)
Подготовка к распаковке …/00-amdgpu-core_1%3a6.0.60001-1710620.22.04_all.deb …
Распаковывается amdgpu-core (1:6.0.60001-1710620.22.04) …
Подготовка к распаковке …/01-libc6-i386_2.35-0ubuntu3.6_amd64.deb …
Распаковывается libc6-i386 (2.35-0ubuntu3.6) на замену (2.35-0ubuntu3.5) …
Заменено файлами из установленного пакета libc6:i386 (2.35-0ubuntu3.5) …
Подготовка к распаковке …/02-libc-dev-bin_2.35-0ubuntu3.6_amd64.deb …
Распаковывается libc-dev-bin (2.35-0ubuntu3.6) на замену (2.35-0ubuntu3.5) …
Подготовка к распаковке …/03-libc6-dev_2.35-0ubuntu3.6_amd64.deb …
Распаковывается libc6-dev:amd64 (2.35-0ubuntu3.6) на замену (2.35-0ubuntu3.5) …
Подготовка к распаковке …/04-libc6-dbg_2.35-0ubuntu3.6_amd64.deb …
Распаковывается libc6-dbg:amd64 (2.35-0ubuntu3.6) на замену (2.35-0ubuntu3.5) …
Подготовка к распаковке …/05-libc6_2.35-0ubuntu3.6_amd64.deb …
Деконфигурируется libc6:i386 (2.35-0ubuntu3.5), чтобы можно было настроить libc6:amd64 (2.35-0ubuntu3.5) …
Распаковывается libc6:amd64 (2.35-0ubuntu3.6) на замену (2.35-0ubuntu3.5) …
Подготовка к распаковке …/06-libc6_2.35-0ubuntu3.6_i386.deb …
Распаковывается libc6:i386 (2.35-0ubuntu3.6) на замену (2.35-0ubuntu3.5) …
Выбор ранее не выбранного пакета libdrm2-amdgpu:amd64.
Подготовка к распаковке …/07-libdrm2-amdgpu_1%3a2.4.116.60001-1710620.22.04_amd64.deb …
Распаковывается libdrm2-amdgpu:amd64 (1:2.4.116.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libglapi-amdgpu-mesa:amd64.
Подготовка к распаковке …/08-libglapi-amdgpu-mesa_1%3a23.3.0.60001-1710620.22.04_amd64.deb …
Распаковывается libglapi-amdgpu-mesa:amd64 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libgl1-amdgpu-mesa-glx:amd64.
Подготовка к распаковке …/09-libgl1-amdgpu-mesa-glx_1%3a23.3.0.60001-1710620.22.04_amd64.deb …
Распаковывается libgl1-amdgpu-mesa-glx:amd64 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libva2-amdgpu:amd64.
Подготовка к распаковке …/10-libva2-amdgpu_2.16.0.60001-1710620.22.04_amd64.deb …
Распаковывается libva2-amdgpu:amd64 (2.16.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libva-amdgpu-drm2:amd64.
Подготовка к распаковке …/11-libva-amdgpu-drm2_2.16.0.60001-1710620.22.04_amd64.deb …
Распаковывается libva-amdgpu-drm2:amd64 (2.16.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libva-amdgpu-x11-2:amd64.
Подготовка к распаковке …/12-libva-amdgpu-x11-2_2.16.0.60001-1710620.22.04_amd64.deb …
Распаковывается libva-amdgpu-x11-2:amd64 (2.16.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libva-amdgpu-glx2:amd64.
Подготовка к распаковке …/13-libva-amdgpu-glx2_2.16.0.60001-1710620.22.04_amd64.deb …
Распаковывается libva-amdgpu-glx2:amd64 (2.16.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libwayland-amdgpu-client0:amd64.
Подготовка к распаковке …/14-libwayland-amdgpu-client0_1.22.0.60001-1710620.22.04_amd64.deb …
Распаковывается libwayland-amdgpu-client0:amd64 (1.22.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libva-amdgpu-wayland2:amd64.
Подготовка к распаковке …/15-libva-amdgpu-wayland2_2.16.0.60001-1710620.22.04_amd64.deb …
Распаковывается libva-amdgpu-wayland2:amd64 (2.16.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libdrm-amdgpu-common.
Подготовка к распаковке …/16-libdrm-amdgpu-common_1.0.0.60001-1716197.22.04_all.deb …
Распаковывается libdrm-amdgpu-common (1.0.0.60001-1716197.22.04) …
Выбор ранее не выбранного пакета libdrm-amdgpu-amdgpu1:amd64.
Подготовка к распаковке …/17-libdrm-amdgpu-amdgpu1_1%3a2.4.116.60001-1710620.22.04_amd64.deb …
Распаковывается libdrm-amdgpu-amdgpu1:amd64 (1:2.4.116.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libdrm-amdgpu-radeon1:amd64.
Подготовка к распаковке …/18-libdrm-amdgpu-radeon1_1%3a2.4.116.60001-1710620.22.04_amd64.deb …
Распаковывается libdrm-amdgpu-radeon1:amd64 (1:2.4.116.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libllvm17.0.60001-amdgpu:amd64.
Подготовка к распаковке …/19-libllvm17.0.60001-amdgpu_1%3a17.0.60001-1710620.22.04_amd64.deb …
Распаковывается libllvm17.0.60001-amdgpu:amd64 (1:17.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета mesa-amdgpu-va-drivers:amd64.
Подготовка к распаковке …/20-mesa-amdgpu-va-drivers_1%3a23.3.0.60001-1710620.22.04_amd64.deb …
Распаковывается mesa-amdgpu-va-drivers:amd64 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libc6:amd64 (2.35-0ubuntu3.6) …
Настраивается пакет amdgpu-core (1:6.0.60001-1710620.22.04) …
Настраивается пакет libdrm2-amdgpu:amd64 (1:2.4.116.60001-1710620.22.04) …
Настраивается пакет libglapi-amdgpu-mesa:amd64 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libgl1-amdgpu-mesa-glx:amd64 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libva2-amdgpu:amd64 (2.16.0.60001-1710620.22.04) …
Настраивается пакет libva-amdgpu-drm2:amd64 (2.16.0.60001-1710620.22.04) …
Настраивается пакет libva-amdgpu-x11-2:amd64 (2.16.0.60001-1710620.22.04) …
Настраивается пакет libva-amdgpu-glx2:amd64 (2.16.0.60001-1710620.22.04) …
Настраивается пакет libwayland-amdgpu-client0:amd64 (1.22.0.60001-1710620.22.04) …
Настраивается пакет libva-amdgpu-wayland2:amd64 (2.16.0.60001-1710620.22.04) …
Настраивается пакет libdrm-amdgpu-common (1.0.0.60001-1716197.22.04) …
Настраивается пакет libdrm-amdgpu-amdgpu1:amd64 (1:2.4.116.60001-1710620.22.04) …
Настраивается пакет libdrm-amdgpu-radeon1:amd64 (1:2.4.116.60001-1710620.22.04) …
Настраивается пакет libllvm17.0.60001-amdgpu:amd64 (1:17.0.60001-1710620.22.04) …
Настраивается пакет mesa-amdgpu-va-drivers:amd64 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libgl1-amdgpu-mesa-dri:amd64.
(Чтение базы данных … на данный момент установлено 918283 файла и каталога.)
Подготовка к распаковке …/00-libgl1-amdgpu-mesa-dri_1%3a23.3.0.60001-1710620.22.04_amd64.deb …
Распаковывается libgl1-amdgpu-mesa-dri:amd64 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libdrm2-amdgpu:i386.
Подготовка к распаковке …/01-libdrm2-amdgpu_1%3a2.4.116.60001-1710620.22.04_i386.deb …
Распаковывается libdrm2-amdgpu:i386 (1:2.4.116.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libglapi-amdgpu-mesa:i386.
Подготовка к распаковке …/02-libglapi-amdgpu-mesa_1%3a23.3.0.60001-1710620.22.04_i386.deb …
Распаковывается libglapi-amdgpu-mesa:i386 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libgl1-amdgpu-mesa-glx:i386.
Подготовка к распаковке …/03-libgl1-amdgpu-mesa-glx_1%3a23.3.0.60001-1710620.22.04_i386.deb …
Распаковывается libgl1-amdgpu-mesa-glx:i386 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libva2-amdgpu:i386.
Подготовка к распаковке …/04-libva2-amdgpu_2.16.0.60001-1710620.22.04_i386.deb …
Распаковывается libva2-amdgpu:i386 (2.16.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libva-amdgpu-drm2:i386.
Подготовка к распаковке …/05-libva-amdgpu-drm2_2.16.0.60001-1710620.22.04_i386.deb …
Распаковывается libva-amdgpu-drm2:i386 (2.16.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libva-amdgpu-x11-2:i386.
Подготовка к распаковке …/06-libva-amdgpu-x11-2_2.16.0.60001-1710620.22.04_i386.deb …
Распаковывается libva-amdgpu-x11-2:i386 (2.16.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libva-amdgpu-glx2:i386.
Подготовка к распаковке …/07-libva-amdgpu-glx2_2.16.0.60001-1710620.22.04_i386.deb …
Распаковывается libva-amdgpu-glx2:i386 (2.16.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libwayland-amdgpu-client0:i386.
Подготовка к распаковке …/08-libwayland-amdgpu-client0_1.22.0.60001-1710620.22.04_i386.deb …
Распаковывается libwayland-amdgpu-client0:i386 (1.22.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libva-amdgpu-wayland2:i386.
Подготовка к распаковке …/09-libva-amdgpu-wayland2_2.16.0.60001-1710620.22.04_i386.deb …
Распаковывается libva-amdgpu-wayland2:i386 (2.16.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libdrm-amdgpu-amdgpu1:i386.
Подготовка к распаковке …/10-libdrm-amdgpu-amdgpu1_1%3a2.4.116.60001-1710620.22.04_i386.deb …
Распаковывается libdrm-amdgpu-amdgpu1:i386 (1:2.4.116.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libdrm-amdgpu-radeon1:i386.
Подготовка к распаковке …/11-libdrm-amdgpu-radeon1_1%3a2.4.116.60001-1710620.22.04_i386.deb …
Распаковывается libdrm-amdgpu-radeon1:i386 (1:2.4.116.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libllvm17.0.60001-amdgpu:i386.
Подготовка к распаковке …/12-libllvm17.0.60001-amdgpu_1%3a17.0.60001-1710620.22.04_i386.deb …
Распаковывается libllvm17.0.60001-amdgpu:i386 (1:17.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета mesa-amdgpu-va-drivers:i386.
Подготовка к распаковке …/13-mesa-amdgpu-va-drivers_1%3a23.3.0.60001-1710620.22.04_i386.deb …
Распаковывается mesa-amdgpu-va-drivers:i386 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libc6:i386 (2.35-0ubuntu3.6) …
Настраивается пакет libdrm2-amdgpu:i386 (1:2.4.116.60001-1710620.22.04) …
Настраивается пакет libglapi-amdgpu-mesa:i386 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libgl1-amdgpu-mesa-glx:i386 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libva2-amdgpu:i386 (2.16.0.60001-1710620.22.04) …
Настраивается пакет libva-amdgpu-drm2:i386 (2.16.0.60001-1710620.22.04) …
Настраивается пакет libva-amdgpu-x11-2:i386 (2.16.0.60001-1710620.22.04) …
Настраивается пакет libva-amdgpu-glx2:i386 (2.16.0.60001-1710620.22.04) …
Настраивается пакет libwayland-amdgpu-client0:i386 (1.22.0.60001-1710620.22.04) …
Настраивается пакет libva-amdgpu-wayland2:i386 (2.16.0.60001-1710620.22.04) …
Настраивается пакет libdrm-amdgpu-amdgpu1:i386 (1:2.4.116.60001-1710620.22.04) …
Настраивается пакет libdrm-amdgpu-radeon1:i386 (1:2.4.116.60001-1710620.22.04) …
Настраивается пакет libllvm17.0.60001-amdgpu:i386 (1:17.0.60001-1710620.22.04) …
Настраивается пакет mesa-amdgpu-va-drivers:i386 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libgl1-amdgpu-mesa-dri:i386.
(Чтение базы данных … на данный момент установлен 918331 файл и каталог.)
Подготовка к распаковке …/00-libgl1-amdgpu-mesa-dri_1%3a23.3.0.60001-1710620.22.04_i386.deb …
Распаковывается libgl1-amdgpu-mesa-dri:i386 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libvdpau1:i386.
Подготовка к распаковке …/01-libvdpau1_1.4-3build2_i386.deb …
Распаковывается libvdpau1:i386 (1.4-3build2) …
Выбор ранее не выбранного пакета mesa-amdgpu-vdpau-drivers:i386.
Подготовка к распаковке …/02-mesa-amdgpu-vdpau-drivers_1%3a23.3.0.60001-1710620.22.04_i386.deb …
Распаковывается mesa-amdgpu-vdpau-drivers:i386 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета mesa-amdgpu-vdpau-drivers:amd64.
Подготовка к распаковке …/03-mesa-amdgpu-vdpau-drivers_1%3a23.3.0.60001-1710620.22.04_amd64.deb …
Распаковывается mesa-amdgpu-vdpau-drivers:amd64 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета mokutil.
Подготовка к распаковке …/04-mokutil_0.6.0-2~22.04.2_amd64.deb …
Распаковывается mokutil (0.6.0-2~22.04.2) …
Выбор ранее не выбранного пакета shim-signed.
Подготовка к распаковке …/05-shim-signed_1.51.3+15.7-0ubuntu1_amd64.deb …
Распаковывается shim-signed (1.51.3+15.7-0ubuntu1) …
Выбор ранее не выбранного пакета amdgpu-dkms-firmware.
Подготовка к распаковке …/06-amdgpu-dkms-firmware_1%3a6.3.6.60001-1710620.22.04_all.deb …
Распаковывается amdgpu-dkms-firmware (1:6.3.6.60001-1710620.22.04) …
Выбор ранее не выбранного пакета amdgpu-dkms.
Подготовка к распаковке …/07-amdgpu-dkms_1%3a6.3.6.60001-1710620.22.04_all.deb …
Распаковывается amdgpu-dkms (1:6.3.6.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libwayland-amdgpu-server0:amd64.
Подготовка к распаковке …/08-libwayland-amdgpu-server0_1.22.0.60001-1710620.22.04_amd64.deb …
Распаковывается libwayland-amdgpu-server0:amd64 (1.22.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libxatracker2-amdgpu:amd64.
Подготовка к распаковке …/09-libxatracker2-amdgpu_1%3a23.3.0.60001-1710620.22.04_amd64.deb …
Распаковывается libxatracker2-amdgpu:amd64 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libgbm1-amdgpu:amd64.
Подготовка к распаковке …/10-libgbm1-amdgpu_1%3a23.3.0.60001-1710620.22.04_amd64.deb …
Распаковывается libgbm1-amdgpu:amd64 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libegl1-amdgpu-mesa:amd64.
Подготовка к распаковке …/11-libegl1-amdgpu-mesa_1%3a23.3.0.60001-1710620.22.04_amd64.deb …
Распаковывается libegl1-amdgpu-mesa:amd64 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libegl1-amdgpu-mesa-drivers:amd64.
Подготовка к распаковке …/12-libegl1-amdgpu-mesa-drivers_1%3a23.3.0.60001-1710620.22.04_amd64.deb …
Распаковывается libegl1-amdgpu-mesa-drivers:amd64 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libomxil-bellagio0.
Подготовка к распаковке …/13-libomxil-bellagio0_0.9.3-7ubuntu1_amd64.deb …
Распаковывается libomxil-bellagio0 (0.9.3-7ubuntu1) …
Выбор ранее не выбранного пакета mesa-amdgpu-omx-drivers:amd64.
Подготовка к распаковке …/14-mesa-amdgpu-omx-drivers_1%3a23.3.0.60001-1710620.22.04_amd64.deb …
Распаковывается mesa-amdgpu-omx-drivers:amd64 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета xserver-xorg-amdgpu-video-amdgpu.
Подготовка к распаковке …/15-xserver-xorg-amdgpu-video-amdgpu_1%3a22.0.0.60001-1710620.22.04_amd64.deb …
Распаковывается xserver-xorg-amdgpu-video-amdgpu (1:22.0.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета gst-omx-amdgpu.
Подготовка к распаковке …/16-gst-omx-amdgpu_1%3a1.0.0.1.60001-1710620.22.04_amd64.deb …
Распаковывается gst-omx-amdgpu (1:1.0.0.1.60001-1710620.22.04) …
Выбор ранее не выбранного пакета amdgpu-lib.
Подготовка к распаковке …/17-amdgpu-lib_1%3a6.0.60001-1710620.22.04_amd64.deb …
Распаковывается amdgpu-lib (1:6.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libwayland-amdgpu-server0:i386.
Подготовка к распаковке …/18-libwayland-amdgpu-server0_1.22.0.60001-1710620.22.04_i386.deb …
Распаковывается libwayland-amdgpu-server0:i386 (1.22.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libxatracker2-amdgpu:i386.
Подготовка к распаковке …/19-libxatracker2-amdgpu_1%3a23.3.0.60001-1710620.22.04_i386.deb …
Распаковывается libxatracker2-amdgpu:i386 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libgbm1-amdgpu:i386.
Подготовка к распаковке …/20-libgbm1-amdgpu_1%3a23.3.0.60001-1710620.22.04_i386.deb …
Распаковывается libgbm1-amdgpu:i386 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libegl1-amdgpu-mesa:i386.
Подготовка к распаковке …/21-libegl1-amdgpu-mesa_1%3a23.3.0.60001-1710620.22.04_i386.deb …
Распаковывается libegl1-amdgpu-mesa:i386 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета libegl1-amdgpu-mesa-drivers:i386.
Подготовка к распаковке …/22-libegl1-amdgpu-mesa-drivers_1%3a23.3.0.60001-1710620.22.04_i386.deb …
Распаковывается libegl1-amdgpu-mesa-drivers:i386 (1:23.3.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета amdgpu-lib32.
Подготовка к распаковке …/23-amdgpu-lib32_1%3a6.0.60001-1710620.22.04_amd64.deb …
Распаковывается amdgpu-lib32 (1:6.0.60001-1710620.22.04) …
Выбор ранее не выбранного пакета rocm-core.
Подготовка к распаковке …/24-rocm-core_6.0.1.60001-108~22.04_amd64.deb …
Распаковывается rocm-core (6.0.1.60001-108~22.04) …
Выбор ранее не выбранного пакета comgr.
Подготовка к распаковке …/25-comgr_2.6.0.60001-108~22.04_amd64.deb …
Распаковывается comgr (2.6.0.60001-108~22.04) …
Выбор ранее не выбранного пакета libc6-dev-i386.
Подготовка к распаковке …/26-libc6-dev-i386_2.35-0ubuntu3.6_amd64.deb …
Распаковывается libc6-dev-i386 (2.35-0ubuntu3.6) …
Выбор ранее не выбранного пакета libc6-x32.
Подготовка к распаковке …/27-libc6-x32_2.35-0ubuntu3.6_amd64.deb …
Распаковывается libc6-x32 (2.35-0ubuntu3.6) …
Выбор ранее не выбранного пакета libc6-dev-x32.
Подготовка к распаковке …/28-libc6-dev-x32_2.35-0ubuntu3.6_amd64.deb …
Распаковывается libc6-dev-x32 (2.35-0ubuntu3.6) …
Выбор ранее не выбранного пакета libx32gcc-s1.
Подготовка к распаковке …/29-libx32gcc-s1_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается libx32gcc-s1 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета lib32gomp1.
Подготовка к распаковке …/30-lib32gomp1_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается lib32gomp1 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета libx32gomp1.
Подготовка к распаковке …/31-libx32gomp1_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается libx32gomp1 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета lib32itm1.
Подготовка к распаковке …/32-lib32itm1_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается lib32itm1 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета libx32itm1.
Подготовка к распаковке …/33-libx32itm1_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается libx32itm1 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета lib32atomic1.
Подготовка к распаковке …/34-lib32atomic1_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается lib32atomic1 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета libx32atomic1.
Подготовка к распаковке …/35-libx32atomic1_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается libx32atomic1 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета lib32asan6.
Подготовка к распаковке …/36-lib32asan6_11.4.0-1ubuntu1~22.04_amd64.deb …
Распаковывается lib32asan6 (11.4.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета libx32asan6.
Подготовка к распаковке …/37-libx32asan6_11.4.0-1ubuntu1~22.04_amd64.deb …
Распаковывается libx32asan6 (11.4.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета lib32ubsan1.
Подготовка к распаковке …/38-lib32ubsan1_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается lib32ubsan1 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета libx32stdc++6.
Подготовка к распаковке …/39-libx32stdc++6_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается libx32stdc++6 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета libx32ubsan1.
Подготовка к распаковке …/40-libx32ubsan1_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается libx32ubsan1 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета lib32quadmath0.
Подготовка к распаковке …/41-lib32quadmath0_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается lib32quadmath0 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета libx32quadmath0.
Подготовка к распаковке …/42-libx32quadmath0_12.3.0-1ubuntu1~22.04_amd64.deb …
Распаковывается libx32quadmath0 (12.3.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета lib32gcc-11-dev.
Подготовка к распаковке …/43-lib32gcc-11-dev_11.4.0-1ubuntu1~22.04_amd64.deb …
Распаковывается lib32gcc-11-dev (11.4.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета libx32gcc-11-dev.
Подготовка к распаковке …/44-libx32gcc-11-dev_11.4.0-1ubuntu1~22.04_amd64.deb …
Распаковывается libx32gcc-11-dev (11.4.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета gcc-11-multilib.
Подготовка к распаковке …/45-gcc-11-multilib_11.4.0-1ubuntu1~22.04_amd64.deb …
Распаковывается gcc-11-multilib (11.4.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета lib32stdc++-11-dev.
Подготовка к распаковке …/46-lib32stdc++-11-dev_11.4.0-1ubuntu1~22.04_amd64.deb …
Распаковывается lib32stdc++-11-dev (11.4.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета libx32stdc++-11-dev.
Подготовка к распаковке …/47-libx32stdc++-11-dev_11.4.0-1ubuntu1~22.04_amd64.deb …
Распаковывается libx32stdc++-11-dev (11.4.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета g++-11-multilib.
Подготовка к распаковке …/48-g++-11-multilib_11.4.0-1ubuntu1~22.04_amd64.deb …
Распаковывается g++-11-multilib (11.4.0-1ubuntu1~22.04) …
Выбор ранее не выбранного пакета gcc-multilib.
Подготовка к распаковке …/49-gcc-multilib_4%3a11.2.0-1ubuntu1_amd64.deb …
Распаковывается gcc-multilib (4:11.2.0-1ubuntu1) …
Выбор ранее не выбранного пакета g++-multilib.
Подготовка к распаковке …/50-g++-multilib_4%3a11.2.0-1ubuntu1_amd64.deb …
Распаковывается g++-multilib (4:11.2.0-1ubuntu1) …
Выбор ранее не выбранного пакета hip-dev.
Подготовка к распаковке …/51-hip-dev_6.0.32831.60001-108~22.04_amd64.deb …
Распаковывается hip-dev (6.0.32831.60001-108~22.04) …
Выбор ранее не выбранного пакета hsa-rocr.
Подготовка к распаковке …/52-hsa-rocr_1.12.0.60001-108~22.04_amd64.deb …
Распаковывается hsa-rocr (1.12.0.60001-108~22.04) …
Выбор ранее не выбранного пакета valgrind.
Подготовка к распаковке …/53-valgrind_1%3a3.18.1-1ubuntu2_amd64.deb …
Распаковывается valgrind (1:3.18.1-1ubuntu2) …
Выбор ранее не выбранного пакета libdrm-amdgpu-dev:amd64.
Подготовка к распаковке …/54-libdrm-amdgpu-dev_1%3a2.4.116.60001-1710620.22.04_amd64.deb …
Распаковывается libdrm-amdgpu-dev:amd64 (1:2.4.116.60001-1710620.22.04) …
Выбор ранее не выбранного пакета hsakmt-roct-dev.
Подготовка к распаковке …/55-hsakmt-roct-dev_20231016.2.245.60001-108~22.04_amd64.deb …
Распаковывается hsakmt-roct-dev (20231016.2.245.60001-108~22.04) …
Выбор ранее не выбранного пакета hsa-rocr-dev.
Подготовка к распаковке …/56-hsa-rocr-dev_1.12.0.60001-108~22.04_amd64.deb …
Распаковывается hsa-rocr-dev (1.12.0.60001-108~22.04) …
Выбор ранее не выбранного пакета rocminfo.
Подготовка к распаковке …/57-rocminfo_1.0.0.60001-108~22.04_amd64.deb …
Распаковывается rocminfo (1.0.0.60001-108~22.04) …
Выбор ранее не выбранного пакета rocm-llvm.
Подготовка к распаковке …/58-rocm-llvm_17.0.0.24012.60001-108~22.04_amd64.deb …
Распаковывается rocm-llvm (17.0.0.24012.60001-108~22.04) …
Выбор ранее не выбранного пакета hipcc.
Подготовка к распаковке …/59-hipcc_1.0.0.60001-108~22.04_amd64.deb …
Распаковывается hipcc (1.0.0.60001-108~22.04) …
Выбор ранее не выбранного пакета hip-runtime-amd.
Подготовка к распаковке …/60-hip-runtime-amd_6.0.32831.60001-108~22.04_amd64.deb …
Распаковывается hip-runtime-amd (6.0.32831.60001-108~22.04) …
Подготовка к распаковке …/61-mesa-vdpau-drivers_23.3.2-1pop0~1704238321~22.04~36f1d0e_amd64.deb …
Распаковывается mesa-vdpau-drivers:amd64 (23.3.2-1pop0~1704238321~22.04~36f1d0e) на замену (23.3.0-1pop0~1702935939~22.04~67e417a) …
Выбор ранее не выбранного пакета mesa-vdpau-drivers:i386.
Подготовка к распаковке …/62-mesa-vdpau-drivers_23.3.2-1pop0~1704238321~22.04~36f1d0e_i386.deb …
Распаковывается mesa-vdpau-drivers:i386 (23.3.2-1pop0~1704238321~22.04~36f1d0e) …
Выбор ранее не выбранного пакета openmp-extras-runtime.
Подготовка к распаковке …/63-openmp-extras-runtime_17.60.0.60001-108~22.04_amd64.deb …
Распаковывается openmp-extras-runtime (17.60.0.60001-108~22.04) …
Выбор ранее не выбранного пакета rocm-language-runtime.
Подготовка к распаковке …/64-rocm-language-runtime_6.0.1.60001-108~22.04_amd64.deb …
Распаковывается rocm-language-runtime (6.0.1.60001-108~22.04) …
Выбор ранее не выбранного пакета rocm-hip-runtime.
Подготовка к распаковке …/65-rocm-hip-runtime_6.0.1.60001-108~22.04_amd64.deb …
Распаковывается rocm-hip-runtime (6.0.1.60001-108~22.04) …
Выбор ранее не выбранного пакета rocm-ocl-icd.
Подготовка к распаковке …/66-rocm-ocl-icd_2.0.0.60001-108~22.04_amd64.deb …
Распаковывается rocm-ocl-icd (2.0.0.60001-108~22.04) …
Выбор ранее не выбранного пакета rocm-opencl.
Подготовка к распаковке …/67-rocm-opencl_2.0.0.60001-108~22.04_amd64.deb …
Распаковывается rocm-opencl (2.0.0.60001-108~22.04) …
Выбор ранее не выбранного пакета rocm-opencl-runtime.
Подготовка к распаковке …/68-rocm-opencl-runtime_6.0.1.60001-108~22.04_amd64.deb …
Распаковывается rocm-opencl-runtime (6.0.1.60001-108~22.04) …
Выбор ранее не выбранного пакета vdpau-driver-all:i386.
Подготовка к распаковке …/69-vdpau-driver-all_1.4-3build2_i386.deb …
Распаковывается vdpau-driver-all:i386 (1.4-3build2) …
Выбор ранее не выбранного пакета libomxil-bellagio-bin.
Подготовка к распаковке …/70-libomxil-bellagio-bin_0.9.3-7ubuntu1_amd64.deb …
Распаковывается libomxil-bellagio-bin (0.9.3-7ubuntu1) …
Настраивается пакет mesa-vdpau-drivers:amd64 (23.3.2-1pop0~1704238321~22.04~36f1d0e) …
Настраивается пакет libxatracker2-amdgpu:amd64 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libxatracker2-amdgpu:i386 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libgl1-amdgpu-mesa-dri:amd64 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libgl1-amdgpu-mesa-dri:i386 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libomxil-bellagio-bin (0.9.3-7ubuntu1) …
Настраивается пакет libwayland-amdgpu-server0:amd64 (1.22.0.60001-1710620.22.04) …
Настраивается пакет libwayland-amdgpu-server0:i386 (1.22.0.60001-1710620.22.04) …
Настраивается пакет libgbm1-amdgpu:amd64 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libgbm1-amdgpu:i386 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет mokutil (0.6.0-2~22.04.2) …
Настраивается пакет libomxil-bellagio0 (0.9.3-7ubuntu1) …
Настраивается пакет mesa-amdgpu-vdpau-drivers:amd64 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет shim-signed (1.51.3+15.7-0ubuntu1) …
update-alternatives: используется /usr/lib/shim/shimx64.efi.signed.latest для предоставления /usr/lib/shim/shimx64.efi.signed (shimx64.efi.signed) в автоматическом режиме
Trying to migrate /boot/efi into esp config
Installing grub to /boot/efi.
Выполняется установка для платформы x86_64-efi.
Установка завершена. Ошибок нет.
Generating a new Secure Boot signing key:
Can't load /var/lib/shim-signed/mok/.rnd into RNG
4037593A2A730000:error:12000079:random number generator:RAND_load_file:Cannot open file:../crypto/rand/randfile.c:106:Filename=/var/lib/shim-signed/mok/.rnd
.+..+...+....+..+.+........+.......+........+.+...+........+....+...+..................+.....+....+.........+..+...+.......+..+..........+...+...+.....+.+.....+.+..+.+..+....+...+............+.....+....+...........+.+.....+.......+..+...+...+.......+.....+.+.....+.+........+.+......+.....+......+...+....+..+...+................+.....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...+...+........+....+.........+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.......+.........+.....+....+.....+......+....+.....+....+........+.........+...............+......+..................+.+...+...+.....+....+......+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+...+.........+...+..........+...+...............+...+......+......+...+..+....+...+...+............+..+.+........+..........+......+.....+...+..........+...+..+...+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*........+...+......+..+....+...+.....+...+...+....+..+....+....................+.+......+..............+.+...+.........+...+.....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----
Error! The module/version combo: bbswitch-0.8/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: bbswitch/0.8/6.6.6-76060606-generic
  kernel: 6.5.4-76060504-generic
Error! The module/version combo: nvidia-545.29.06/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: nvidia/545.29.06/6.6.6-76060606-generic
  kernel: 6.5.4-76060504-generic
Error! The module/version combo: rtl88x2bu-5.8.7.1/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: rtl88x2bu/5.8.7.1/6.6.6-76060606-generic
  kernel: 6.5.4-76060504-generic
Error! The module/version combo: system76-1.0.14~1684961628~22.04~8c2ff21/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: system76/1.0.14~1684961628~22.04~8c2ff21/6.6.6-76060606-generic
  kernel: 6.5.4-76060504-generic
Error! The module/version combo: system76_acpi-1.0.2~1689789919~22.04~03a5804/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: system76_acpi/1.0.2~1689789919~22.04~03a5804/6.6.6-76060606-generic
  kernel: 6.5.4-76060504-generic
Error! The module/version combo: system76-io-1.0.3~1695233384~22.04~0f86350/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: system76-io/1.0.3~1695233384~22.04~0f86350/6.6.6-76060606-generic
  kernel: 6.5.4-76060504-generic
Error! The module/version combo: bbswitch-0.8/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: bbswitch/0.8/6.6.6-76060606-generic
  kernel: 6.6.6-76060606-generic
Error! The module/version combo: nvidia-545.29.06/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: nvidia/545.29.06/6.6.6-76060606-generic
  kernel: 6.6.6-76060606-generic
Error! The module/version combo: rtl88x2bu-5.8.7.1/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: rtl88x2bu/5.8.7.1/6.6.6-76060606-generic
  kernel: 6.6.6-76060606-generic
Error! The module/version combo: system76-1.0.14~1684961628~22.04~8c2ff21/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: system76/1.0.14~1684961628~22.04~8c2ff21/6.6.6-76060606-generic
  kernel: 6.6.6-76060606-generic
Error! The module/version combo: system76_acpi-1.0.2~1689789919~22.04~03a5804/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: system76_acpi/1.0.2~1689789919~22.04~03a5804/6.6.6-76060606-generic
  kernel: 6.6.6-76060606-generic
Error! The module/version combo: system76-io-1.0.3~1695233384~22.04~0f86350/6.6.6-76060606-generic is not located in the DKMS tree.

shim-signed: failed to prepare dkms module for signing; ignoring.
  module: system76-io/1.0.3~1695233384~22.04~0f86350/6.6.6-76060606-generic
  kernel: 6.6.6-76060606-generic
Secure Boot not enabled on this system.
Настраивается пакет libc6-dbg:amd64 (2.35-0ubuntu3.6) …
Настраивается пакет rocm-core (6.0.1.60001-108~22.04) …
update-alternatives: используется /opt/rocm-6.0.1 для предоставления /opt/rocm (rocm) в автоматическом режиме
Настраивается пакет libc6-x32 (2.35-0ubuntu3.6) …
Настраивается пакет rocm-ocl-icd (2.0.0.60001-108~22.04) …
Настраивается пакет libx32gomp1 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет amdgpu-dkms-firmware (1:6.3.6.60001-1710620.22.04) …
Настраивается пакет xserver-xorg-amdgpu-video-amdgpu (1:22.0.0.60001-1710620.22.04) …
Настраивается пакет mesa-amdgpu-omx-drivers:amd64 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libvdpau1:i386 (1.4-3build2) …
Настраивается пакет libegl1-amdgpu-mesa:amd64 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libegl1-amdgpu-mesa:i386 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libc6-i386 (2.35-0ubuntu3.6) …
Настраивается пакет libx32quadmath0 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет libc-dev-bin (2.35-0ubuntu3.6) …
Настраивается пакет valgrind (1:3.18.1-1ubuntu2) …
Настраивается пакет lib32atomic1 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет libx32atomic1 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет hip-dev (6.0.32831.60001-108~22.04) …
Настраивается пакет rocm-llvm (17.0.0.24012.60001-108~22.04) …
Настраивается пакет mesa-vdpau-drivers:i386 (23.3.2-1pop0~1704238321~22.04~36f1d0e) …
Настраивается пакет comgr (2.6.0.60001-108~22.04) …
Настраивается пакет lib32itm1 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет gst-omx-amdgpu (1:1.0.0.1.60001-1710620.22.04) …
Настраивается пакет libx32gcc-s1 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет mesa-amdgpu-vdpau-drivers:i386 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libx32itm1 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет lib32ubsan1 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет hsa-rocr (1.12.0.60001-108~22.04) …
Настраивается пакет lib32gomp1 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет libx32asan6 (11.4.0-1ubuntu1~22.04) …
Настраивается пакет libdrm-amdgpu-dev:amd64 (1:2.4.116.60001-1710620.22.04) …
Настраивается пакет libegl1-amdgpu-mesa-drivers:amd64 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет libegl1-amdgpu-mesa-drivers:i386 (1:23.3.0.60001-1710620.22.04) …
Настраивается пакет rocm-opencl (2.0.0.60001-108~22.04) …
Настраивается пакет lib32asan6 (11.4.0-1ubuntu1~22.04) …
Настраивается пакет vdpau-driver-all:i386 (1.4-3build2) …
Настраивается пакет lib32quadmath0 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет hipcc (1.0.0.60001-108~22.04) …
Настраивается пакет libc6-dev:amd64 (2.35-0ubuntu3.6) …
Настраивается пакет hsakmt-roct-dev (20231016.2.245.60001-108~22.04) …
Настраивается пакет libx32stdc++6 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет libc6-dev-i386 (2.35-0ubuntu3.6) …
Настраивается пакет libx32ubsan1 (12.3.0-1ubuntu1~22.04) …
Настраивается пакет rocminfo (1.0.0.60001-108~22.04) …
Настраивается пакет amdgpu-lib (1:6.0.60001-1710620.22.04) …
Настраивается пакет hsa-rocr-dev (1.12.0.60001-108~22.04) …
Настраивается пакет openmp-extras-runtime (17.60.0.60001-108~22.04) …
Настраивается пакет amdgpu-dkms (1:6.3.6.60001-1710620.22.04) …
Loading new amdgpu-6.3.6-1710620.22.04 DKMS files...
Building for 6.6.6-76060606-generic
Building for architecture amd64
Building initial module for 6.6.6-76060606-generic
ERROR (dkms apport): kernel package linux-headers-6.6.6-76060606-generic is not supported
Error! Bad return status for module build on kernel: 6.6.6-76060606-generic (amd64)
Consult /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/make.log for more information.
dpkg: ошибка при обработке пакета amdgpu-dkms (--configure):
 подпроцесс из пакета amdgpu-dkms установлен сценарий post-installation возвратил код ошибки 10
Настраивается пакет libc6-dev-x32 (2.35-0ubuntu3.6) …
Настраивается пакет amdgpu-lib32 (1:6.0.60001-1710620.22.04) …
Настраивается пакет libx32gcc-11-dev (11.4.0-1ubuntu1~22.04) …
Настраивается пакет libx32stdc++-11-dev (11.4.0-1ubuntu1~22.04) …
Настраивается пакет lib32gcc-11-dev (11.4.0-1ubuntu1~22.04) …
Настраивается пакет lib32stdc++-11-dev (11.4.0-1ubuntu1~22.04) …
Настраивается пакет rocm-language-runtime (6.0.1.60001-108~22.04) …
Настраивается пакет hip-runtime-amd (6.0.32831.60001-108~22.04) …
Настраивается пакет rocm-hip-runtime (6.0.1.60001-108~22.04) …
update-alternatives: используется /opt/rocm-6.0.1/bin/rocm_agent_enumerator для предоставления /usr/bin/rocm_agent_enumerator (rocm_agent_enumerator) в автоматическом режиме
update-alternatives: используется /opt/rocm-6.0.1/bin/rocminfo для предоставления /usr/bin/rocminfo (rocminfo) в автоматическом режиме
Настраивается пакет gcc-11-multilib (11.4.0-1ubuntu1~22.04) …
Настраивается пакет gcc-multilib (4:11.2.0-1ubuntu1) …
Настраивается пакет rocm-opencl-runtime (6.0.1.60001-108~22.04) …
update-alternatives: используется /opt/rocm-6.0.1/bin/clinfo для предоставления /usr/bin/clinfo (clinfo) в автоматическом режиме
update-alternatives: предупреждение: /usr/bin/clinfo на ссылку не заменён
Настраивается пакет g++-11-multilib (11.4.0-1ubuntu1~22.04) …
Настраивается пакет g++-multilib (4:11.2.0-1ubuntu1) …
Обрабатываются триггеры для doc-base (0.11.1) …
Обработка 1 добавленный файл doc-base...
Обрабатываются триггеры для libc-bin (2.35-0ubuntu3.5) …
Обрабатываются триггеры для man-db (2.10.2-1) …
При обработке следующих пакетов произошли ошибки:
 amdgpu-dkms
E: Sub-process /usr/bin/dpkg returned an error code (1)
W: Действие прервано до его завершения
```
</details>
summary:

```
...
Running the post_remove script:
depmod...
Deleting module amdgpu-6.3.6-1710620.22.04 completely from the DKMS tree.
Loading new amdgpu-6.3.6-1710620.22.04 DKMS files...
Building for 6.6.6-76060606-generic
Building for architecture amd64
Building initial module for 6.6.6-76060606-generic
ERROR (dkms apport): kernel package linux-headers-6.6.6-76060606-generic is not supported
Error! Bad return status for module build on kernel: 6.6.6-76060606-generic (amd64)
...
```

<details>
<summary>amdgpu-6.3.6-1710620.22.04 build make.log (6.6.10-76060610-generic kernel)</summary>

```
DKMS make.log for amdgpu-6.3.6-1710620.22.04 for kernel 6.6.10-76060610-generic (amd64)
Вт 06 фев 2024 13:03:13 +07
make: вход в каталог «/usr/src/linux-headers-6.6.10-76060610-generic»
warning: the compiler differs from the one used to build the kernel
  The kernel was built by: x86_64-linux-gnu-gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
  You are using:           gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/scheduler/sched_main.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/scheduler/sched_fence.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/scheduler/sched_entity.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdxcp/amdgpu_xcp_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdxcp/./backport/kcl_drm_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_tt.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_bo.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_bo_util.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_bo_vm.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_module.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/main.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/drm_gem_ttm_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_execbuf_util.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_common.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_range_manager.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_kernel_params.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_resource.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/dma-buf/dma-resv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_pool.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_backlight.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_device.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_ioctl.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_kthread.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_sys_manager.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_io.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_agp_backend.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_seq_file.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_suspend.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_pci.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/drm_buddy.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_mm.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_memory.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_sched.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_fence.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_device.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_reservation.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_cache.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_fb.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_doorbell_mgr.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_print.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_crtc.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdxcp/amdxcp.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_kms.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_connector.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_atombios.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_atomic_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_device_cgroup.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/atombios_crtc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_connectors.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_mn.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_modes.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/atom.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_time.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amddrm_ttm_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_acpi_table.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_fence.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_page_alloc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_ttm.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amddrm_buddy.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_numa.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_object.o
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:2954:31: error: ‘drm_gem_prime_handle_to_fd’ undeclared here (not in a function)
 2954 |         .prime_handle_to_fd = drm_gem_prime_handle_to_fd,
      |                               ^~~~~~~~~~~~~~~~~~~~~~~~~~
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_gart.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_encoders.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_display.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_i2c.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_fs_read_write.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_gem.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_aperture.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_simple_kms_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_ring.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_bitmap.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_cs.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_vmscan.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_dma_fence_chain.o
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:2955:31: error: ‘drm_gem_prime_fd_to_handle’ undeclared here (not in a function)
 2955 |         .prime_fd_to_handle = drm_gem_prime_fd_to_handle,
      |                               ^~~~~~~~~~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:10: error: ‘struct drm_driver’ has no member named ‘gem_prime_mmap’; did you mean ‘gem_prime_import’?
 2979 |         .gem_prime_mmap = amdkcl_drm_gem_prime_mmap,
      |          ^~~~~~~~~~~~~~
      |          gem_prime_import
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:27: error: initialization of ‘struct drm_gem_object * (*)(struct drm_device *, struct dma_buf_attachment *, struct sg_table *)’ from incompatible pointer type ‘int (*)(struct drm_gem_object *, struct vm_area_struct *)’ [-Werror=incompatible-pointer-types]
 2979 |         .gem_prime_mmap = amdkcl_drm_gem_prime_mmap,
      |                           ^~~~~~~~~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:27: note: (near initialization for ‘amdgpu_kms_driver.gem_prime_import_sg_table’)
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:10: error: ‘const struct drm_driver’ has no member named ‘gem_prime_mmap’; did you mean ‘gem_prime_import’?
 3009 |         .gem_prime_mmap = drm_gem_prime_mmap,
      |          ^~~~~~~~~~~~~~
      |          gem_prime_import
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:27: error: initialization of ‘struct drm_gem_object * (*)(struct drm_device *, struct dma_buf_attachment *, struct sg_table *)’ from incompatible pointer type ‘int (*)(struct drm_gem_object *, struct vm_area_struct *)’ [-Werror=incompatible-pointer-types]
 3009 |         .gem_prime_mmap = drm_gem_prime_mmap,
      |                           ^~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:27: note: (near initialization for ‘amdgpu_partition_driver.gem_prime_import_sg_table’)
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_bios.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_mce_amd.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_workqueue.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_benchmark.o
cc1: some warnings being treated as errors
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.o] Ошибка 1
make[3]: *** Ожидание завершения заданий…
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_cpumask.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_dsc_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_mm_slab.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_irqdesc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_suballoc.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/amdttm.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_dp_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_hdcp.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_debugfs_inode.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_debugfs_file.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_sysfs_emit.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/scheduler/amd-sched.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/amdkcl.o
make[2]: *** [scripts/Makefile.build:480: /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu] Ошибка 2
make[1]: *** [/usr/src/linux-headers-6.6.10-76060610-generic/Makefile:1919: /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build] Ошибка 2
make: *** [Makefile:234: __sub-make] Ошибка 2
make: выход из каталога «/usr/src/linux-headers-6.6.10-76060610-generic»
```
</details>
summary:


```
...
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:2954:31: error: ‘drm_gem_prime_handle_to_fd’ undeclared here (not in a function)
 2954 |         .prime_handle_to_fd = drm_gem_prime_handle_to_fd,
      |                               ^~~~~~~~~~~~~~~~~~~~~~~~~~
...
```

I'll try 6.2 kernel, but it's unusable for me because of the lack of wifi and touchpad drivers.

---

### 评论 #10 — kentrussell (2024-02-06T14:34:15Z)

So that's a different error. This is resolved with the upstream patch https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0514f63cfff38a0dcb7ba9c5f245827edc0c5107 . If you get that in there, 6.6 should compile. Also make sure that if you're using the HWE kernel that it has this patch and this specific issue will be resolved. 

---

### 评论 #11 — Flashwalker (2024-02-06T21:24:11Z)

> So that's a different error. This is resolved with the upstream patch https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0514f63cfff38a0dcb7ba9c5f245827edc0c5107 . If you get that in there, 6.6 should compile. Also make sure that if you're using the HWE kernel that it has this patch and this specific issue will be resolved.

I tried to build with patched 6.6.10 (was built using the patch from the url you provided) kernel (from Ubuntu repo) and amdgpu build fails with it too.
<details>
<summary>make.log</summary>

```log
DKMS make.log for amdgpu-6.3.6-1710620.22.04 for kernel 6.6.10-76060610-generic (amd64)
Ср 07 фев 2024 05:00:52 +07
make: вход в каталог «/usr/src/linux-headers-6.6.10-76060610-generic»
warning: the compiler differs from the one used to build the kernel
  The kernel was built by: x86_64-linux-gnu-gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
  You are using:           gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/scheduler/sched_main.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/scheduler/sched_fence.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/scheduler/sched_entity.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdxcp/amdgpu_xcp_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdxcp/./backport/kcl_drm_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_tt.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_bo.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_bo_util.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_bo_vm.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_module.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_execbuf_util.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/drm_gem_ttm_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/main.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_range_manager.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_common.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_resource.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_pool.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_kernel_params.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/dma-buf/dma-resv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_device.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_backlight.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_sys_manager.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_ioctl.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/ttm_agp_backend.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_kthread.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_io.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_seq_file.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_suspend.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/drm_buddy.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_pci.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_mm.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_memory.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_sched.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_fence.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_reservation.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_device.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_cache.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_fb.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_print.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_doorbell_mgr.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdxcp/amdxcp.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_crtc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_connector.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_kms.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_atomic_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_atombios.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/atombios_crtc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_device_cgroup.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_mn.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_connectors.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_modes.o
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:10: error: ‘struct drm_driver’ has no member named ‘gem_prime_mmap’; did you mean ‘gem_prime_import’?
 2979 |         .gem_prime_mmap = amdkcl_drm_gem_prime_mmap,
      |          ^~~~~~~~~~~~~~
      |          gem_prime_import
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:27: error: initialization of ‘struct drm_gem_object * (*)(struct drm_device *, struct dma_buf_attachment *, struct sg_table *)’ from incompatible pointer type ‘int (*)(struct drm_gem_object *, struct vm_area_struct *)’ [-Werror=incompatible-pointer-types]
 2979 |         .gem_prime_mmap = amdkcl_drm_gem_prime_mmap,
      |                           ^~~~~~~~~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:27: note: (near initialization for ‘amdgpu_kms_driver.gem_prime_import_sg_table’)
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:10: error: ‘const struct drm_driver’ has no member named ‘gem_prime_mmap’; did you mean ‘gem_prime_import’?
 3009 |         .gem_prime_mmap = drm_gem_prime_mmap,
      |          ^~~~~~~~~~~~~~
      |          gem_prime_import
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:27: error: initialization of ‘struct drm_gem_object * (*)(struct drm_device *, struct dma_buf_attachment *, struct sg_table *)’ from incompatible pointer type ‘int (*)(struct drm_gem_object *, struct vm_area_struct *)’ [-Werror=incompatible-pointer-types]
 3009 |         .gem_prime_mmap = drm_gem_prime_mmap,
      |                           ^~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:27: note: (near initialization for ‘amdgpu_partition_driver.gem_prime_import_sg_table’)
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_time.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/atom.o
cc1: some warnings being treated as errors
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_acpi_table.o
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu/amdgpu_drv.o] Ошибка 1
make[3]: *** Ожидание завершения заданий…
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_page_alloc.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amddrm_ttm_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_numa.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_fs_read_write.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_aperture.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_simple_kms_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_bitmap.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amddrm_buddy.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_vmscan.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_dma_fence_chain.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_workqueue.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_mce_amd.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_cpumask.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_dsc_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_mm_slab.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_irqdesc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_suballoc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_dp_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_drm_hdcp.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_debugfs_inode.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_debugfs_file.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/kcl_sysfs_emit.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/ttm/amdttm.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/scheduler/amd-sched.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdkcl/amdkcl.o
make[2]: *** [scripts/Makefile.build:480: /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build/amd/amdgpu] Ошибка 2
make[1]: *** [/usr/src/linux-headers-6.6.10-76060610-generic/Makefile:1919: /var/lib/dkms/amdgpu/6.3.6-1710620.22.04/build] Ошибка 2
make: *** [Makefile:234: __sub-make] Ошибка 2
make: выход из каталога «/usr/src/linux-headers-6.6.10-76060610-generic»
```
</details>



---

### 评论 #12 — Flashwalker (2024-02-06T23:54:59Z)

After the purging kernel 6.6 and installing **6.5.0 HWE** one, amdgpu build finally succeeded.

![Снимок экрана_2024-02-07_06-17-15](https://github.com/ROCm/ROCm/assets/2188215/05703abd-f0df-4a7e-88fc-6fdbd749f089)

I was able to run the system in hybrid graphics mode, but...
But even in integrated-gpu--only graphics mode after a short time of system run at the random moment (e.g. when closing/opening the lid, run browser) the graphics starts glitching and crashing and **X** freezes up and crashing which often leads to entire system hangup and crash. Relogging (DM restart) helps if I can do it in time. It's a sad moment.
![Снимок экрана_2024-02-07_06-30-43](https://github.com/ROCm/ROCm/assets/2188215/65d7661e-082e-4d1b-b72e-21bb5d7eb182)

Testing is required in hybrid graphics mode.




---

### 评论 #13 — Flashwalker (2024-02-08T02:32:53Z)

It looks like the `--enable-unsafe-webgpu` **Chromium** flag cause **X** crash on my integrated AMD GPU.

I run **Ryzen 9 7945HX**, Graphics Model **AMD Radeon™ 610M**. 
Uninstalled amdgpu.

```
$ inxi -Gxx
Graphics:
  Device-1: NVIDIA vendor: Lenovo driver: N/A pcie: speed: 16 GT/s lanes: 8
    bus-ID: 01:00.0 chip-ID: 10de:28e0
  Device-2: AMD vendor: Lenovo driver: amdgpu v: kernel pcie:
    speed: 16 GT/s lanes: 16 ports: active: eDP-1 empty: none bus-ID: 08:00.0
    chip-ID: 1002:164e
  Device-3: Syntek Integrated Camera type: USB driver: uvcvideo
    bus-ID: 3-2.4:4 chip-ID: 174f:246a
  Display: x11 server: X.Org v: 1.21.1.4 compositor: xfwm v: 4.18.0 driver:
    X: loaded: ati,modesetting unloaded: fbdev,vesa alternate: amdgpu
    gpu: amdgpu display-ID: :0.0 screens: 1
  Screen-1: 0 s-res: 2560x1600 s-dpi: 96
  Monitor-1: eDP-1 model: BOE Display res: 2560x1600 dpi: 188
    diag: 407mm (16")
  OpenGL: renderer: RAPHAEL_MENDOCINO (radeonsi raphael_mendocino LLVM
    15.0.7 DRM 3.54 6.5.0-15-generic)
    v: 4.6 Mesa 23.3.2-1pop0~1704238321~22.04~36f1d0e direct render: Yes
```

**UPD:**

I found that my glitchy problem is more complicated issue:
- https://community.amd.com/t5/graphics-cards/solved-random-reboots-and-crashes-ryzen-and-amd-gpu-under-linux/td-p/441637
- https://bugzilla.kernel.org/show_bug.cgi?id=206903#c135
- https://bbs.archlinux.org/viewtopic.php?id=265282
- https://wiki.archlinux.org/title/AMDGPU#Screen_artifacts_and_frequency_problem
- https://askubuntu.com/questions/1239149/graphics-glitches-and-artifacts-with-ryzen-5-3400g-apu










---

### 评论 #14 — Flashwalker (2024-02-09T18:00:13Z)

It seems that adding `iommu=pt` to the boot kernel parameters helped with the glitches.
But I suppose this disables the GPU forwarding feature for virtualization

---

### 评论 #15 — vkomenda (2024-02-10T13:28:51Z)

On Debian with kernels 6.5.0 and 6.6.13, there is this build error:
```
$ cat /var/lib/dkms/amdgpu/6.2.4-1683306.22.04/build/make.log
DKMS make.log for amdgpu-6.2.4-1683306.22.04 for kernel 6.6.13-amd64 (x86_64)
Sat 10 Feb 13:23:07 GMT 2024
make: Entering directory '/usr/src/linux-headers-6.6.13-amd64'
/var/lib/dkms/amdgpu/6.2.4-1683306.22.04/build/Makefile:52: *** dma_resv->seq is missing. exit....  Stop.
make[1]: *** [/usr/src/linux-headers-6.6.13-common/Makefile:1938: /var/lib/dkms/amdgpu/6.2.4-1683306.22.04/build] Error 2
make: *** [/usr/src/linux-headers-6.6.13-common/Makefile:246: __sub-make] Error 2
make: Leaving directory '/usr/src/linux-headers-6.6.13-amd64'
```

Is there a patch for that?

---

### 评论 #16 — kentrussell (2024-02-12T14:22:54Z)

The only 6.6-based kernel that is supported by ROCm 6.0 is the HWE kernel provided by Ubuntu. For newer kernel support, you'll have to wait until ROCm 6.1. You can refer to  https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.0.0/reference/system-requirements.html for the list of known-good-and-tested OS+kernel configurations. But for newer support, you'll need to wait until ROCm 6.1.

---

### 评论 #17 — hankster112 (2024-04-17T14:30:57Z)

6.1 has been released but I still get the same error as @tuleo1 
```
DKMS make.log for amdgpu-6.7.0-1756574.22.04 for kernel 6.6.13+bpo-amd64 (amd64)
Wed Apr 17 09:26:34 AM CDT 2024
make: Entering directory '/usr/src/linux-headers-6.6.13+bpo-amd64'
/tmp/amd.Z35UpKSZ/Makefile:52: *** dma_resv->seq is missing. exit....  Stop.
make[1]: *** [/usr/src/linux-headers-6.6.13+bpo-common/Makefile:1938: /tmp/amd.Z35UpKSZ] Error 2
make: *** [/usr/src/linux-headers-6.6.13+bpo-common/Makefile:246: __sub-make] Error 2
make: Leaving directory '/usr/src/linux-headers-6.6.13+bpo-amd64'
```
Used the latest install instructions from https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html for Ubuntu 22.04 and Ubuntu 20.04 which should also work on Debian. Purged all config files and AMD apt sources beforehand.

Devuan 5 Daedalus (fork of Debian 12 without systemd)
AMD Ryzen 7 2700
MSI Radeon 5700 XT
Kernel 6.6.13+bpo-amd64 

---

### 评论 #18 — vkomenda (2024-04-19T10:23:06Z)

> The only 6.6-based kernel that is supported by ROCm 6.0 is the HWE kernel provided by Ubuntu. For newer kernel support, you'll have to wait until ROCm 6.1. You can refer to https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.0.0/reference/system-requirements.html for the list of known-good-and-tested OS+kernel configurations. But for newer support, you'll need to wait until ROCm 6.1.

Hey! The 6.1 release seems to have *downgraded* the kernel version support in Ubuntu 22? In the [table](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems) it's now 6.5 as opposed to 6.6 in the 6.0 release!

The DKMS driver doesn't compile on 6.6.15 in Debian. Same errors as in the release 6.0.

What's going on with newer kernel support? Is this driver stuck in Ubuntu HWE?

---
