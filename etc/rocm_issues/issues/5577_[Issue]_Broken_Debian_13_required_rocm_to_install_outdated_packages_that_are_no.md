# [Issue]: Broken Debian 13 required rocm to install outdated packages that are no longer provided

> **Issue #5577**
> **状态**: closed
> **创建时间**: 2025-10-27T16:07:20Z
> **更新时间**: 2025-10-29T20:03:03Z
> **关闭时间**: 2025-10-29T10:36:49Z
> **作者**: yodaxtah
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5577

## 描述

### Problem Description

> [!NOTE]
> I am aware that **Debian 13** is currently not officially supported for the **RX 7800 RX**. [I was recommended](https://github.com/ROCm/ROCm/discussions/2599#discussioncomment-14794484) to report this issue nonetheless, since this should also be a problem for consumers with an **AMD Instinct MI300X GPU**.

I am unable to `sudo apt install rocm` as described in the documentation guide, because some packages do not have the required version. I tried this a few weeks back, so I don't have the complete 

<details>
<summary>
CLI output of trying to install the rocm package.
</summary>

```bash
$ sudo apt install rocm
Installing:                     
  rocm

Installing dependencies:
  amd-smi-lib           lib32stdc++-14-dev           libgeotiff5               libopencv-imgproc-dev       libtbb12               rocblas-dev
  amdgpu-core           lib32ubsan1                  libgl2ps1.4               libopencv-imgproc410        libtbbbind-2-5         rocfft
  comgr                 libaec0                      libgphoto2-dev            libopencv-java              libtbbmalloc2          rocfft-dev
  composablekernel-dev  libamd-comgr2                libhdf4-0-alt             libopencv-ml-dev            libtcl8.6              rocm-cmake
  g++-14-multilib       libamd3                      libhdf5-310               libopencv-ml410             libtesseract5          rocm-core
  g++-multilib          libamdhip64-5                libhdf5-hl-310            libopencv-objdetect-dev     libtk8.6               rocm-dbgapi
  gcc-14-multilib       libarmadillo14               libhsa-runtime64-1        libopencv-objdetect410      libucx0                rocm-debug-agent
  gcc-multilib          libarpack2t64                libhsakmt1                libopencv-photo-dev         libvtk9.3              rocm-developer-tools
  gdal-data             libavcodec-dev               libhwloc-plugins          libopencv-photo410          libx32asan8            rocm-device-libs
  gdal-plugins          libavformat-dev              libhwloc15                libopencv-shape-dev         libx32atomic1          rocm-gdb
  gdb                   libavutil-dev                libibmad5                 libopencv-shape410          libx32gcc-14-dev       rocm-hip
  half                  libbabeltrace1               libibumad3                libopencv-stitching-dev     libx32gcc-s1           rocm-hip-runtime
  hip-dev               libblosc1                    libimath-dev              libopencv-stitching410      libx32gomp1            rocm-hip-runtime-dev
  hip-doc               libc6-dbg                    libipt2                   libopencv-superres-dev      libx32itm1             rocm-language-runtime
  hip-runtime-amd       libc6-dev-i386               libjs-sphinxdoc           libopencv-superres410       libx32quadmath0        rocm-llvm
  hip-samples           libc6-dev-x32                libjs-underscore          libopencv-video-dev         libx32stdc++-14-dev    rocm-opencl
  hipblas               libc6-x32                    libkmlbase1t64            libopencv-video410          libx32stdc++6          rocm-opencl-dev
  hipblas-common-dev    libcamd3                     libkmldom1t64             libopencv-videoio-dev       libx32ubsan1           rocm-opencl-sdk
  hipblas-dev           libccolamd3                  libkmlengine1t64          libopencv-videoio410        libxerces-c3.2t64      rocm-openmp
  hipblaslt             libcfitsio10t64              libleptonica6             libopencv-videostab-dev     libze1                 rocm-smi-lib
  hipblaslt-dev         libcharls2                   libllvm17t64              libopencv-videostab410      mariadb-common         rocminfo
  hipcc                 libcholmod5                  libmariadb3               libopencv-viz-dev           mesa-common-dev        rocprim-dev
  hipcub-dev            libdc1394-dev                libmunge2                 libopencv-viz410            migraphx               rocprofiler
  hipfft                libdebuginfod-common         libnetcdf22               libopencv410-jni            migraphx-dev           rocprofiler-compute
  hipfft-dev            libdebuginfod1t64            libnuma-dev               libopenexr-dev              miopen-hip             rocprofiler-dev
  hipfort-dev           libdrm-amdgpu-amdgpu1        libodbc2                  libopenmpi40                miopen-hip-dev         rocprofiler-plugins
  hipify-clang          libdrm-amdgpu-common         libodbccr2                libpmix2t64                 mivisionx              rocprofiler-register
  hiprand               libdrm-amdgpu-dev            libodbcinst2              libpq5                      mivisionx-dev          rocprofiler-sdk
  hiprand-dev           libdrm-amdgpu-radeon1        libogdi4.1                libproj25                   mysql-common           rocprofiler-sdk-rocpd
  hipsolver             libdrm2-amdgpu               libopencv-calib3d-dev     libpsm2-2                   ocl-icd-opencl-dev     rocprofiler-sdk-roctx
  hipsolver-dev         libelf-dev                   libopencv-calib3d410      libpython3-dev              opencl-c-headers       rocprofiler-systems
  hipsparse             libevent-core-2.1-7t64       libopencv-contrib-dev     libpython3.13-dev           opencl-clhpp-headers   rocrand
  hipsparse-dev         libevent-pthreads-2.1-7t64   libopencv-contrib410      libqhull-r8.0               opencv-data            rocrand-dev
  hipsparselt           libexif-dev                  libopencv-core-dev        libqt5opengl5t64            openmp-extras-dev      rocsolver
  hipsparselt-dev       libexif-doc                  libopencv-core410         libqt5test5t64              openmp-extras-runtime  rocsolver-dev
  hiptensor             libexpat1-dev                libopencv-dev             libraw1394-dev              proj-bin               rocsparse
  hiptensor-dev         libfabric1                   libopencv-dnn-dev         libraw1394-tools            proj-data              rocsparse-dev
  hsa-amd-aqlprofile    libfile-copy-recursive-perl  libopencv-dnn410          librttopo1                  python3-argcomplete    rocthrust-dev
  hsa-rocr              libfile-which-perl           libopencv-features2d-dev  libsocket++1                python3-dev            roctracer
  hsa-rocr-dev          libfreexl1                   libopencv-features2d410   libsource-highlight-common  python3-pip            roctracer-dev
  lib32asan8            libfyba0t64                  libopencv-flann-dev       libsource-highlight4t64     python3.13-dev         rocwmma-dev
  lib32atomic1          libgdal36                    libopencv-flann410        libspatialite8t64           rccl                   rpp
  lib32gcc-14-dev       libgdcm-dev                  libopencv-highgui-dev     libswresample-dev           rccl-dev               rpp-dev
  lib32gomp1            libgdcm3.0t64                libopencv-highgui410      libswscale-dev              rocalution             unixodbc-common
  lib32itm1             libgeos-c1t64                libopencv-imgcodecs-dev   libsz2                      rocalution-dev         valgrind
  lib32quadmath0        libgeos3.13.1                libopencv-imgcodecs410    libtbb-dev                  rocblas

Suggested packages:
  lib32stdc++6-14-dbg   gdbserver    libgeotiff-epsg  libhwloc-contrib-plugins  ogdi-bin        libtbb-doc  mpi-default-bin  opencl-clhpp-headers-doc
  libx32stdc++6-14-dbg  geotiff-bin  libhdf4-alt-dev  odbc-postgresql           opencv-doc      tcl8.6      vtk9-doc         valgrind-mpi
  gdb-doc               gdal-bin     hdf4-tools       tdsodbc                   libraw1394-doc  tk8.6       vtk9-examples    kcachegrind

Summary:
  Upgrading: 0, Installing: 276, Removing: 0, Not Upgrading: 8
  Download size: 441 kB / 5,121 MB
  Space needed: 22.2 GB / 1,333 GB available

Continue? [Y/n] Y
Err:1 http://deb.debian.org/debian trixie/main amd64 mariadb-common all 1:11.8.2-1
  404  Not Found [IP: 2a04:4e42:2::644 80]
Err:2 http://deb.debian.org/debian trixie/main amd64 libmariadb3 amd64 1:11.8.2-1
  404  Not Found [IP: 2a04:4e42:2::644 80]
Err:3 http://deb.debian.org/debian trixie/main amd64 libpq5 amd64 17.5-1
  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Failed to fetch http://deb.debian.org/debian/pool/main/m/mariadb/mariadb-common_11.8.2-1_all.deb  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Failed to fetch http://deb.debian.org/debian/pool/main/m/mariadb/libmariadb3_11.8.2-1_amd64.deb  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Failed to fetch http://deb.debian.org/debian/pool/main/p/postgresql-17/libpq5_17.5-1_amd64.deb  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
```
</details>

### Operating System

Debian 13 (trixie)

### CPU

AMD Ryzen 7 7800X3D 8-Core Processor

### GPU

AMD Radeon RX 7800 XT

### ROCm Version

ROCm 7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

Follow [the installation guide for Debian 13, described at rocmdocs.amd.com](https://rocmdocs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#rocm-installation)

```bash
wget https://repo.radeon.com/amdgpu-install/7.0.2/ubuntu/noble/amdgpu-install_7.0.2.70002-1_all.deb
sudo apt install ./amdgpu-install_7.0.2.70002-1_all.deb
sudo apt update
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
sudo apt install rocm # fails
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

`rocminfo` was installed with `sudo apt install rocminfo` before. It caused issues while following the setup guide, so I removed those packages Debian provides. There should no longer be any of those Debian provided rocm packages on my system, as filtering `apt list` on "rocm" doesn't produce any matches. Feel free to ask me on other filters.

```bash
apt list --installed | grep rocm

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
```

---

## 评论 (5 条)

### 评论 #1 — ianbmacdonald (2025-10-27T16:28:12Z)

What does your error look like for `apt install rocm`?  Given there was some stuff from 'before' it is probably a bit of cruft not handled cleanly by the amdgpu-install wrapper. 

In addition to the error, you should share your `/etc/apt/sources.list.d/rocm.list` and `/etc/apt/sources.list.d/amdgpu.list`. 




---

### 评论 #2 — yodaxtah (2025-10-27T16:38:09Z)

Regarding your first question, I'm not sure if you missed the collapsed details section in the issue description. The collapsed log contains these lines:

```
Err:1 http://deb.debian.org/debian trixie/main amd64 mariadb-common all 1:11.8.2-1
  404  Not Found [IP: 2a04:4e42:2::644 80]
Err:2 http://deb.debian.org/debian trixie/main amd64 libmariadb3 amd64 1:11.8.2-1
  404  Not Found [IP: 2a04:4e42:2::644 80]
Err:3 http://deb.debian.org/debian trixie/main amd64 libpq5 amd64 17.5-1
  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Failed to fetch http://deb.debian.org/debian/pool/main/m/mariadb/mariadb-common_11.8.2-1_all.deb  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Failed to fetch http://deb.debian.org/debian/pool/main/m/mariadb/libmariadb3_11.8.2-1_amd64.deb  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Failed to fetch http://deb.debian.org/debian/pool/main/p/postgresql-17/libpq5_17.5-1_amd64.deb  404  Not Found [IP: 2a04:4e42:2::644 80]
Error: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
```

Is this what you wanted to know?

Regarding your second question, here is a log of `cat`ing those files:

```bash
$ cat /etc/apt/sources.list.d/rocm.list
deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/7.0.2 noble main
deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/graphics/7.0.2/ubuntu noble main

$ cat /etc/apt/sources.list.d/amdgpu.list
deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.10.2/ubuntu noble main
#deb-src [signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.10.2/ubuntu noble main
```

---

### 评论 #3 — ianbmacdonald (2025-10-27T19:15:13Z)

I did miss your collapsed cli output.  The only errors present show 404 errors (not found) from apt trying to download packages from the Internet. 

Those apt sources will work just fine. (and are what amdgpu-install created commented -src, multi-arch et al) 

The issue here, is that your 'before' state includes a Debian 13 system that has not been updated in the better part of a year.

the solution is `apt update` ; details follow.

The first thing apt trips on is a 404 (just like a 404 in your browser, this means it can't find what it is looking for.).   The reason is because you have not recently performed an `apt update` ; which you should do everytime you are thinking about doing an `apt upgrade` or `apt install`.   

`apt update` is what tells your Debian (or Ubuntu, or Mint, etc.) system what packages are available.  In your case, the last time you ran that command, mariadb (database) had a new version 11.8.2-1 available.  I can tell by looking at the [package changelog](https://metadata.ftp-master.debian.org/changelogs//main/m/mariadb/mariadb_11.8.3-0+deb13u1_changelog) that version 11.8.2-1 was replaced with version 11.8.3-0 on August 25th of this year.  

Welcome to Debian 13.  I am guessing in Q2, or earlier of this year you were tinkering with SQL databases, noting you have both postgresql and mariadb installed.   In Q3 you happen to run apt update, but did not actually upgrade your system.  Now in Q4 you are experimenting with ROCm on this system which has an RX 7800 XT in it.  

If you are thinking it would be nice to do some local inference, the easy options which require no building whatsever are:
- Fire up [Lemonade](https://netstatz.com/strix_halo_lemonade/)
- Fire up vLLM using the AMD nightly;  I can confirm last nights build `[docker pull rocm/vllm-dev:nightly_main_20251026](https://hub.docker.com/layers/rocm/vllm-dev/nightly_main_20251026/images/sha256-46d2e8735b4b619f02f7d8c3583071afa281b1cf3a018250fe3f16dbb5d60831)` works on the RX 7900 XTX

---

### 评论 #4 — yodaxtah (2025-10-27T20:21:11Z)

Hi, thanks for looking into this already, you took the time to write out a lot of information.

### How to fix?

So, let's say I should have done something that I didn't do. What can I do about this _now_? I don't know how to fix this. Should I maybe reach out to Debian contributors for this?

> the solution is `apt update`; details follow.

I have already reran the installation commands again:
```
wget https://repo.radeon.com/amdgpu-install/7.0.2/ubuntu/noble/amdgpu-install_7.0.2.70002-1_all.deb
sudo apt install ./amdgpu-install_7.0.2.70002-1_all.deb
sudo apt update
sudo apt install rocm
```
(Which includes `apt update`, once more.) This produces the same errors, as of today, 28th of October.

Perhaps you meant that details will follow in another answer later?

### Understanding the issue

I'm a bit confused by some things you wrote.

> The issue here, is that your 'before' state includes a Debian 13 system that has not been updated in the **better part of a year**.

What is "the better part of the year"? Around the official Debian release? Also, do you mean with the "before state" the period before I started following the tutorial?

> The first thing apt trips on is a 404 (just like a 404 in your browser, this means it can't find what it is looking for.). The reason is **because you have not recently performed an apt update** ; which you should do everytime you are thinking about doing an apt upgrade or apt install.

I'm sure I have ran `apt update` a few times, after all the upgrades should come from somewhere, no? (You can find a collapsed history of apt installs below.) I know for sure at least I ran `apt update`, as it's part of the tutorial.

> I am guessing in Q2, or earlier of this year you were tinkering with SQL databases, noting you have both postgresql and mariadb installed.

I built this PC at the start of July, so the system is only as old as Q3. (The logs below indicate 13th of July, to be precise.) I never worked with postgresql directly. My Debian system should be quite "vanilla" and I install most software through either `brew` or `flatpak`. I started with Debian 13 Testing (installed from the first Release Candidate), as the official release was still a month away at the time and Debian 12's kernel was too old for my graphics card (already RX 7800 RT). Using the release candidate was suggested by Debian contributors trying to figure out how to get my GPU working. To my knowledge, I'm still on Debian 13 -- not on Debian (14) Testing.

> In Q3 you happen to run apt update, but did not actually upgrade your system.

Possible.

> Now in Q4 you are experimenting with ROCm on this system which has an RX 7800 XT in it.

According to the logs (see below), I had installed `rocminfo` (from Debian) on the 26th of August. That must be around the time I first tried installing ROCm. So, not sure if it's relevant, but my first attempts are actually from back in late August, when I believe I was following the Ubuntu 24.04 or Debian 12 installation process, I'm not sure, but I didn't get far. Whenever my first attempt was, I'm only sure the docs didn't have a "Debian 13" section yet.

> In your case, the last time you ran that command, mariadb (database) had a new version 11.8.2-1 available. I can tell by looking at the [package changelog](https://metadata.ftp-master.debian.org/changelogs//main/m/mariadb/mariadb_11.8.3-0+deb13u1_changelog) that version 11.8.2-1 was replaced with version 11.8.3-0 on August 25th of this year.

Okay, so from what I understand it's actually dangerous to do `apt update` not followed by `apt upgrade`, and I'm only discovering that now, after 4 years of using Linux?

### Apt log

I mainly use `nala` to keep track of all the `apt` commands I execute; you can find a full history here, if you need to check whether I installed a certain piece of software.

<details>
<summary>
APT install/remove/upgrade history
</summary>

```
$ nala history
  ID    Command                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        Date and Time               Altered    Requested-By  
  1     install flatpak                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                2025-07-13 11:19:08 CEST          1    username (1000)   
  2     install gnome-software-plugin-flatpak                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          2025-07-13 11:21:40 CEST          1    username (1000)   
  3     install lshw                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   2025-07-13 11:44:19 CEST          1    username (1000)   
  4     upgrade gir1.2-soup-3.0 libegl-mesa0 libgbm1 libgl1-mesa-dri libglx-mesa0 libgnutls30t64 libsoup-3.0-0 libsoup-3.0-common libxatracker2 mesa-libgallium mesa-va-drivers mesa-vdpau-drivers mesa-vulkan-drivers mobile-broadband-provider-info                                                                                                                                                                                                                                                                                                                                                  2025-07-14 22:33:25 CEST         14    username (1000)   
  5     install gir1.2-gda-5.0 gir1.2-gsound-1.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       2025-07-16 19:37:41 CEST          5    username (1000)   
  6     upgrade gnome-remote-desktop                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   2025-07-16 23:39:21 CEST          1    username (1000)   
  7     install gddrescue                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              2025-07-17 22:40:04 CEST          1    username (1000)   
  8     install curl                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   2025-07-17 22:47:30 CEST          1    username (1000)   
  9     install git                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    2025-07-17 22:48:04 CEST          4    username (1000)   
  10    history undo 7                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 2025-07-17 22:56:50 CEST          1    username (1000)   
  11    install mame-tools                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             2025-07-18 23:55:30 CEST         27    username (1000)   
  12    upgrade apache2-bin                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            2025-07-19 00:45:32 CEST          1    username (1000)   
  13    upgrade gdm3 gir1.2-gdm-1.0 gir1.2-mutter-16 gnome-shell gnome-shell-common libgdm1 libmutter-16-0 mutter-common mutter-common-bin                                                                                                                                                                                                                                                                                                                                                                                                                                                             2025-07-20 01:23:02 CEST          9    username (1000)   
  14    upgrade adwaita-icon-theme libssl3t64 openssl openssl-provider-legacy task-desktop task-english task-gnome-desktop tasksel tasksel-data                                                                                                                                                                                                                                                                                                                                                                                                                                                        2025-07-21 01:15:31 CEST          9    username (1000)   
  15    install waydroid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               2025-07-21 10:05:44 CEST          1    username (1000)   
  16    install rocminfo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               2025-07-26 00:46:30 CEST          3    username (1000)   
  17    upgrade bind9-dnsutils bind9-host bind9-libs evince evince-common firefox-esr fuse3 gir1.2-evince-3.0 gir1.2-nm-1.0 gnome-maps gnome-software gnome-software-common gnome-software-plugin-deb gnome-software-plugin-flatpak gnome-software-plugin-fwupd gnome-terminal gnome-terminal-data gnome-text-editor libblas3 libc-bin libc-l10n libc6 libevdocument3-4t64 libevview3-3t64 libexpat1 libfuse3-4 libgfapi0 libgfrpc0 libgfxdr0 libglusterfs0 liblapack3 libmbedcrypto16 libnautilus-extension4 libnm0 libxml2 locales locales-all nautilus nautilus-data nautilus-extension-gnome-t…    2025-07-26 09:55:54 CEST         44    username (1000)   
  18    install rocminfo rocm-device-libs-17 rocm-opencl-icd rocm-smi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  2025-07-26 10:57:53 CEST          6    username (1000)   
  19    upgrade apache2-bin bash bind9-dnsutils bind9-host bind9-libs busybox console-setup console-setup-linux debianutils dirmngr distro-info-data e2fsprogs evince evince-common firefox-esr gir1.2-evince-3.0 gir1.2-gdkpixbuf-2.0 gir1.2-soup-3.0 gnupg-utils gpg gpg-agent gpg-wks-client gpgconf gpgsm gpgv iio-sensor-proxy installation-report keyboard-configuration libarchive13t64 libblas3 libc-bin libc-l10n libc6 libcap2 libcap2-bin libcom-err2 libdebconfclient0 libdjvulibre-text libdjvulibre21 libevdocument3-4t64 libevview3-3t64 libext2fs2t64 libgdk-pixbuf-2.0-0 libgdk-p…    2025-08-10 09:53:11 CEST         85    username (1000)   
  20    install build-essential                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        2025-08-10 11:52:00 CEST         42    username (1000)   
  21    install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        2025-08-10 12:00:09 CEST        107    username (1000)   
  22    install libglu1-mesa-dev libglew-dev zlib1g-dev libgeoip-dev                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   2025-08-10 12:11:54 CEST          8    username (1000)   
  23    upgrade firefox-esr gir1.2-javascriptcoregtk-4.1 gir1.2-webkit2-4.1 libjavascriptcoregtk-4.1-0 libjavascriptcoregtk-6.0-1 libwebkit2gtk-4.1-0 libwebkitgtk-6.0-4 libxslt1.1                                                                                                                                                                                                                                                                                                                                                                                                                    2025-08-21 23:29:23 CEST         10    username (1000)   
  24    upgrade qemu-block-extra qemu-utils                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            2025-08-24 01:11:16 CEST          2    username (1000)   
  25    upgrade libudisks2-0 libxml2 udisks2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           2025-08-29 19:31:04 CEST          3    username (1000)   
  26    install cmake ninja-build nasm clang-format libgl1-mesa-dev                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    2025-09-14 14:08:15 CEST         12    username (1000)   
  27    upgrade cups cups-client cups-common cups-core-drivers cups-daemon cups-ipp-utils cups-ppdc cups-server-common imagemagick-7-common libcjson1 libcups2t64 libmagickcore-7.q16-10 libmagickcore-7.q16-10-extra libmagickwand-7.q16-10 libnss-myhostname libnss-systemd libpam-systemd libsystemd-dev libsystemd-shared libsystemd0 libudev-dev libudev1 systemd systemd-sysv systemd-timesyncd udev                                                                                                                                                                                             2025-09-16 00:20:48 CEST         26    username (1000)   
  28    install htop iotop sysstat                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     2025-09-19 17:21:42 CEST          3    username (1000)   
  29    install lm-sensors                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             2025-09-19 17:24:24 CEST          1    username (1000)   
  30    upgrade firefox-esr libavcodec61 libavfilter10 libavformat61 libavutil59 libpostproc58 libswresample5 libswscale8 libxslt1.1 linux-libc-dev                                                                                                                                                                                                                                                                                                                                                                                                                                                    2025-09-29 01:25:16 CEST         10    username (1000)   
  31    upgrade ghostscript libgs-common libgs10 libgs10-common libssl-dev libssl3t64 libtiff-dev libtiff6 libtiffxx6 openssl openssl-provider-legacy                                                                                                                                                                                                                                                                                                                                                                                                                                                  2025-10-15 08:59:29 CEST         11    username (1000)   
  32    install unshield                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               2025-10-16 22:47:29 CEST          2    username (1000)   
  33    install ./amdgpu-install_7.0.2.70002-1_all.deb                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 2025-10-18 17:59:53 CEST          4    username (1000)   
  34    install python3-setuptools python3-wheel                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       2025-10-18 18:00:37 CEST         11    username (1000)   
  35    remove rocminfo rocm-device-libs-17 rocm-opencl-icd rocm-smi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   2025-10-18 18:05:59 CEST          9    username (1000)   
```
</details>

### Alternatives

> If you are thinking it would be nice to do some local inference, the easy options which require no building whatsever are:

I'm not familiar with Lemonade. Skimming the article you linked, it says to install rocm, which I'm failing at, but perhaps looking a bit further into it in the future would help. I much rather prefer to just have the system work with the typical installation tools, `apt`, `brew`, etc. The second is a docker; I deliberatly avoid docker/podman.

I appreciate nonetheless that you're informing me on these options, who knows I might need it in the end.

---

### 评论 #5 — yodaxtah (2025-10-29T10:36:49Z)

Thanks to a very helpful, knowledgeable person in the Debian community, we discovered that the sources list was corrupted. (Or we think, at least.)

Running the following commands seemed to have fixed the issue.

```
sudo find /var/lib/apt/lists -type f -delete
sudo apt update
apt-cache policy mariadb-common
```

So I was able to `apt install rocm` without errors and will follow the remainder of the tutorial.

---
