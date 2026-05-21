# Cannot install on WSL

> **Issue #4281**
> **状态**: closed
> **创建时间**: 2025-01-21T16:29:28Z
> **更新时间**: 2025-01-27T14:48:42Z
> **关闭时间**: 2025-01-27T14:48:41Z
> **作者**: SauvageThomas
> **标签**: Under Investigation, ROCm 6.2.3, AMD Radeon RX 6800 XT
> **URL**: https://github.com/ROCm/ROCm/issues/4281

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **AMD Radeon RX 6800 XT** (颜色: #ededed)

## 描述

### Problem Description

I'm following this doc for WSL installation on a fresh WSL
https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html

When I arrive on this step

`
amdgpu-install -y --usecase=wsl,rocm --no-dkms
`

Nothing happens on the terminal and the terminal is frozen (can't CTRL + C)

The doc uses the 6.2.3 version, but I have the same issue with https://repo.radeon.com/amdgpu-install/latest/ubuntu/jammy/.

Is it the right way to install it on WSL or am I missing somethin

### Operating System

22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 7 5800X 8-Core Processor

### GPU

AMD Radeon RX 6800 XT

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

```
thsauvag@Thomas-PC:~$ wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/jammy/amdgpu-install_6.2.60203-1_all.deb
--2025-01-21 17:09:27--  https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/jammy/amdgpu-install_6.2.60203-1_all.deb
Resolving repo.radeon.com (repo.radeon.com)... 2.22.151.132, 2.22.151.157, 2a02:26f0:9100:9::1748:f955, ...
Connecting to repo.radeon.com (repo.radeon.com)|2.22.151.132|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 16932 (17K) [application/octet-stream]
Saving to: ‘amdgpu-install_6.2.60203-1_all.deb.1’

amdgpu-install_6.2.60203-1_al 100%[=================================================>]  16.54K  --.-KB/s    in 0s

2025-01-21 17:09:27 (286 MB/s) - ‘amdgpu-install_6.2.60203-1_all.deb.1’ saved [16932/16932]

thsauvag@Thomas-PC:~$ sudo apt install ./amdgpu-install_6.2.60203-1_all.deb
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Note, selecting 'amdgpu-install' instead of './amdgpu-install_6.2.60203-1_all.deb'
The following packages were automatically installed and are no longer required:
  gir1.2-javascriptcoregtk-4.1 gir1.2-webkit2-4.1 htop libnl-3-200 libnl-genl-3-200 linux-tools-5.15.0-112
  linux-tools-5.15.0-112-generic
Use 'sudo apt autoremove' to remove them.
The following packages will be DOWNGRADED:
  amdgpu-install
0 upgraded, 0 newly installed, 1 downgraded, 0 to remove and 0 not upgraded.
Need to get 0 B/16.9 kB of archives.
After this operation, 0 B of additional disk space will be used.
Do you want to continue? [Y/n] y
Get:1 /home/thsauvag/amdgpu-install_6.2.60203-1_all.deb amdgpu-install all 6.2.60203-2044426.22.04 [16.9 kB]
dpkg: warning: downgrading amdgpu-install from 6.3.60301-2095006.22.04 to 6.2.60203-2044426.22.04
(Reading database ... 58402 files and directories currently installed.)
Preparing to unpack .../amdgpu-install_6.2.60203-1_all.deb ...
Unpacking amdgpu-install (6.2.60203-2044426.22.04) over (6.3.60301-2095006.22.04) ...
Setting up amdgpu-install (6.2.60203-2044426.22.04) ...
Installing new version of config file /etc/amdgpu-install/amdgpu-setup.conf ...
Installing new version of config file /etc/apt/sources.list.d/amdgpu.list ...
Installing new version of config file /etc/apt/sources.list.d/rocm.list ...
N: Download is performed unsandboxed as root as file '/home/thsauvag/amdgpu-install_6.2.60203-1_all.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
thsauvag@Thomas-PC:~$ amdgpu-install -y --usecase=wsl,rocm --no-dkms
```
Then, nothing happens.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — lucbruni-amd (2025-01-21T19:59:55Z)

Hi @SauvageThomas,

Thanks for reaching out about this, an internal ticket has been opened for investigation.

Would you mind trying the command without `-y` option? It automatically answers "yes" to any prompts during the installation process, but might also suppress some output that could give us clues as to what went wrong.

Also since you are on a fresh WSL instance, and if you do not have important data on it, perhaps you could reset it with `wsl --unregister Ubuntu-22.04` and reinstall with `wsl --install -d Ubuntu-22.04`. This might help me compare installation logs later on. If you do this, please repost the entire installation log again as you did in the original post if the issue persists. Thanks!

---

### 评论 #2 — SauvageThomas (2025-01-21T21:45:40Z)

To show you what is happening, here is the screenshot of the terminal hanging infinitely and not registering CTRL + C

![Image](https://github.com/user-attachments/assets/aa866f22-9374-4c97-a6e2-9c5b92eed9eb)

Here is the full output:

```
PS C:\Program Files\PowerShell\7> wsl --install -d Ubuntu-22.04
Ubuntu 22.04 LTS est déjà installé.
Lancement de Ubuntu 22.04 LTS...
Installing, this may take a few minutes...
Please create a default UNIX user account. The username does not need to match your Windows username.
For more information visit: https://aka.ms/wslusers
Enter new UNIX username: thsauvag
New password:
Retype new password:
passwd: password updated successfully
Installation successful!
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.167.4-microsoft-standard-WSL2 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Tue Jan 21 22:40:55 CET 2025

  System load:  0.14                Processes:             54
  Usage of /:   0.1% of 1006.85GB   Users logged in:       0
  Memory usage: 4%                  IPv4 address for eth0: 172.21.178.252
  Swap usage:   0%


This message is shown once a day. To disable it please create the
/home/thsauvag/.hushlogin file.
thsauvag@Thomas-PC:~$ sudo apt update
[sudo] password for thsauvag:
Get:1 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
Hit:2 http://archive.ubuntu.com/ubuntu jammy InRelease
Get:3 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
Get:4 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
Get:5 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [2041 kB]
Get:6 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [14.1 MB]
Get:7 http://security.ubuntu.com/ubuntu jammy-security/main Translation-en [321 kB]
Get:8 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [2772 kB]
Get:9 http://security.ubuntu.com/ubuntu jammy-security/restricted Translation-en [484 kB]
Get:10 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [960 kB]
Get:11 http://security.ubuntu.com/ubuntu jammy-security/universe Translation-en [205 kB]
Get:12 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 c-n-f Metadata [19.5 kB]
Get:13 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [37.6 kB]
Get:14 http://security.ubuntu.com/ubuntu jammy-security/multiverse Translation-en [8260 B]
Get:15 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 c-n-f Metadata [224 B]
Get:16 http://archive.ubuntu.com/ubuntu jammy/universe Translation-en [5652 kB]
Get:17 http://archive.ubuntu.com/ubuntu jammy/universe amd64 c-n-f Metadata [286 kB]
Get:18 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [217 kB]
Get:19 http://archive.ubuntu.com/ubuntu jammy/multiverse Translation-en [112 kB]
Get:20 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 c-n-f Metadata [8372 B]
Get:21 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [2276 kB]
Get:22 http://archive.ubuntu.com/ubuntu jammy-updates/main Translation-en [382 kB]
Get:23 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [2877 kB]
Get:24 http://archive.ubuntu.com/ubuntu jammy-updates/restricted Translation-en [501 kB]
Get:25 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1182 kB]
Get:26 http://archive.ubuntu.com/ubuntu jammy-updates/universe Translation-en [289 kB]
Get:27 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 c-n-f Metadata [26.4 kB]
Get:28 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [44.5 kB]
Get:29 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse Translation-en [11.5 kB]
Get:30 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 c-n-f Metadata [440 B]
Get:31 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [67.7 kB]
Get:32 http://archive.ubuntu.com/ubuntu jammy-backports/main Translation-en [11.1 kB]
Get:33 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 c-n-f Metadata [388 B]
Get:34 http://archive.ubuntu.com/ubuntu jammy-backports/restricted amd64 c-n-f Metadata [116 B]
Get:35 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [28.9 kB]
Get:36 http://archive.ubuntu.com/ubuntu jammy-backports/universe Translation-en [16.5 kB]
Get:37 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 c-n-f Metadata [672 B]
Get:38 http://archive.ubuntu.com/ubuntu jammy-backports/multiverse amd64 c-n-f Metadata [116 B]
Fetched 35.3 MB in 2s (14.5 MB/s)
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
16 packages can be upgraded. Run 'apt list --upgradable' to see them.
thsauvag@Thomas-PC:~$ wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/jammy/amdgpu-install_6.2.60203-1_all.deb
--2025-01-21 22:43:02--  https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/jammy/amdgpu-install_6.2.60203-1_all.deb
Resolving repo.radeon.com (repo.radeon.com)... 2.22.151.132, 2.22.151.157, 2a02:26f0:9100:9::1748:f955, ...
Connecting to repo.radeon.com (repo.radeon.com)|2.22.151.132|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 16932 (17K) [application/octet-stream]
Saving to: ‘amdgpu-install_6.2.60203-1_all.deb’

amdgpu-install_6.2.60203-1_al 100%[=================================================>]  16.54K  --.-KB/s    in 0s

2025-01-21 22:43:02 (321 MB/s) - ‘amdgpu-install_6.2.60203-1_all.deb’ saved [16932/16932]

thsauvag@Thomas-PC:~$ sudo apt install ./amdgpu-install_6.2.60203-1_all.deb
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Note, selecting 'amdgpu-install' instead of './amdgpu-install_6.2.60203-1_all.deb'
The following additional packages will be installed:
  dialog
The following NEW packages will be installed:
  amdgpu-install dialog
0 upgraded, 2 newly installed, 0 to remove and 16 not upgraded.
Need to get 303 kB/320 kB of archives.
After this operation, 1333 kB of additional disk space will be used.
Do you want to continue? [Y/n] y
Get:1 /home/thsauvag/amdgpu-install_6.2.60203-1_all.deb amdgpu-install all 6.2.60203-2044426.22.04 [16.9 kB]
Get:2 http://archive.ubuntu.com/ubuntu jammy/universe amd64 dialog amd64 1.3-20211214-1 [303 kB]
Fetched 303 kB in 1s (431 kB/s)
Selecting previously unselected package amdgpu-install.
(Reading database ... 42578 files and directories currently installed.)
Preparing to unpack .../amdgpu-install_6.2.60203-1_all.deb ...
Unpacking amdgpu-install (6.2.60203-2044426.22.04) ...
Selecting previously unselected package dialog.
Preparing to unpack .../dialog_1.3-20211214-1_amd64.deb ...
Unpacking dialog (1.3-20211214-1) ...
Setting up dialog (1.3-20211214-1) ...
Setting up amdgpu-install (6.2.60203-2044426.22.04) ...
Processing triggers for man-db (2.10.2-1) ...
N: Download is performed unsandboxed as root as file '/home/thsauvag/amdgpu-install_6.2.60203-1_all.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
thsauvag@Thomas-PC:~$ amdgpu-install --usecase=wsl,rocm --no-dkms
``

---

### 评论 #3 — smazurov (2025-01-22T07:30:17Z)

not sure you're gonna get anywhere, next step will `rocminfo` will output unsupported gpu

---

### 评论 #4 — SauvageThomas (2025-01-22T08:06:37Z)

Mhhh, I saw that it was not in the support matrix but that some people managed to use it. Is it completly out of the scope ? 

---

### 评论 #5 — lucbruni-amd (2025-01-22T15:20:14Z)

While your GPU is not officially supported per the support matrix, and it is unlikely you will be able to use ROCm with it on WSL, it is still worth investigating this issue as `amdgpu-install` shouldn't just hang like that.

Since `amdgpu-install` is a bash script, do you receive any output running the following?

`bash -x $(which amdgpu-install) -y --usecase=wsl,rocm --no-dkms`

---

### 评论 #6 — SauvageThomas (2025-01-23T08:06:59Z)

Is here all the output:

```
thsauvag@Thomas-PC:~$ bash -x $(which amdgpu-install) -y --usecase=wsl,rocm --no-dkms
+ set -e
+ REPOSITORY=/var/opt/amdgpu-local
+ EULA_FILE=/usr/share/amdgpu-install/AMDGPUPROEULA
+ DKMS_PACKAGE=amdgpu-dkms
+ BASE_ROCM_PACKAGE=rocm-core
+ BASE_PACKAGES=("$DKMS_PACKAGE" amdgpu-core "$BASE_ROCM_PACKAGE")
+ MESA_PACKAGES=(amdgpu-lib amdgpu-lib32)
+ OPENCL_ROCR_PACKAGE=rocm-opencl-runtime
+ SUPPLEMENTAL_FW_PACKAGES=
+ USECASE_DKMS_PACKAGES=("$DKMS_PACKAGE")
+ USECASE_GRAPHICS_PACKAGES=(${MESA_PACKAGES[*]})
+ USECASE_MULTIMEDIA_PACKAGES=(mesa-amdgpu-multimedia)
+ USECASE_WORKSTATION_PACKAGES=(amdgpu-pro amdgpu-pro-lib32)
+ USECASE_AMF_PACKAGES=(amf-amdgpu-pro)
+ USECASE_ROCM_PACKAGES=(rocm)
+ USECASE_LRT_PACKAGES=(rocm-language-runtime)
+ USECASE_OPENCL_PACKAGES=($OPENCL_ROCR_PACKAGE)
+ USECASE_OPENCLSDK_PACKAGES=(rocm-opencl-sdk)
+ USECASE_HIP_PACKAGES=(rocm-hip-runtime)
+ USECASE_HIPLIBSDK_PACKAGES=(rocm-hip-sdk)
+ USECASE_MLLIB_PACKAGES=(rocm-ml-libraries)
+ USECASE_MLSDK_PACKAGES=(rocm-ml-sdk)
+ USECASE_ROCMDEVTOOLS_PACKAGES=(rocm-developer-tools rocm-utils)
+ USECASE_ROCMDEV_PACKAGES=(rocm-dev)
+ USECASE_OPENMPSDK_PACKAGES=(rocm-openmp-sdk)
+ USECASE_ASAN_PACKAGES=(rocm-asan)
+ USECASE_WSL_PACKAGES=(hsa-runtime-rocr4wsl-amdgpu)
+ OPENGL_MESA_PACKAGES=(${MESA_PACKAGES[*]})
+ OPENGL_OGLP_PACKAGES=(amdgpu-pro-oglp amdgpu-pro-oglp:i386)
+ OPENCL_ROCR_PACKAGES=($OPENCL_ROCR_PACKAGE)
+ OPENCL_LEGACY_PACKAGES=(clinfo-amdgpu-pro opencl-legacy-amdgpu-pro-icd)
+ VULKAN_AMDVLK_PACKAGES=(vulkan-amdgpu)
+ VULKAN_PRO_PACKAGES=(vulkan-amdgpu-pro vulkan-amdgpu-pro:i386)
+ VULKAN_RADV_PACKAGES=(mesa-amdgpu-vulkan-drivers)
+ PROG=amdgpu-install
++ cd /usr/bin
++ pwd -P
+ PROG_DIR=/usr/bin
+++ id -u
++ [[ 1000 -ne 0 ]]
++ echo sudo
+ SUDO=sudo
+ SBIN=/usr/bin
++ dirname /usr/bin/amdgpu-install
+ SCRIPT_DIR=/usr/bin
+ USECASE_OPTION=graphics,opencl,hip
+ OPENCL_OPTION=
+ OPENGL_OPTION=
+ VULKAN_OPTION=
+ ROCM_RELEASE=
+ OPTIONS=()
+ os_release
+ [[ -r /etc/os-release ]]
+ . /etc/os-release
++ PRETTY_NAME='Ubuntu 22.04.5 LTS'
++ NAME=Ubuntu
++ VERSION_ID=22.04
++ VERSION='22.04.5 LTS (Jammy Jellyfish)'
++ VERSION_CODENAME=jammy
++ ID=ubuntu
++ ID_LIKE=debian
++ HOME_URL=https://www.ubuntu.com/
++ SUPPORT_URL=https://help.ubuntu.com/
++ BUG_REPORT_URL=https://bugs.launchpad.net/ubuntu/
++ PRIVACY_POLICY_URL=https://www.ubuntu.com/legal/terms-and-policies/privacy-policy
++ UBUNTU_CODENAME=jammy
+ PKGUPDATE=
+ case "$ID" in
+ PKGUPDATE='apt-get update'
+ PKGMAN=apt-get
+ OS_CLASS=debian
+ :
+ debian_repo_setup
+ local listfile=/etc/apt/sources.list.d/amdgpu-local.list
+ local pinfile=/etc/apt/preferences.d/amdgpu-pin-600
+ local repo url suite
+ ls -d '/usr/bin/*/dists'
+ return
+ (( 3 ))
+ case "$1" in
+ ARGS+='-y '
+ shift
+ (( 2 ))
+ case "$1" in
+ option=--usecase
+ option=usecase
+ eval USECASE_OPTION=wsl,rocm
++ USECASE_OPTION=wsl,rocm
+ shift
+ (( 1 ))
+ case "$1" in
+ OPTIONS+=(${1#--})
+ shift
+ (( 0 ))
+ set -- -y
+ amdgpu_install -y
+ check_options
+ [[ no-dkms =~ no-dkms ]]
+ [[ wsl,rocm =~ dkms ]]
+ [[ wsl,rocm =~ workstation ]]
+ [[ '' =~ legacy ]]
+ [[ '' =~ legacy ]]
+ [[ wsl,rocm =~ workstation ]]
+ build_package_list
+ list=()
+ local list
+ add_package_list Usecase
+ local listname=Usecase
+ local option
+ array=()
+ local array
+ local listopts
+ eval 'listopts=$USECASE_OPTION'
++ listopts=wsl,rocm
+ for option in ${listopts//,/ }
+ eval 'array=(${USECASE_WSL_PACKAGES[*]})'
++ array=(${USECASE_WSL_PACKAGES[*]})
+ [[ -z hsa-runtime-rocr4wsl-amdgpu ]]
+ PACKAGES+=(${array[*]})
+ for option in ${listopts//,/ }
+ eval 'array=(${USECASE_ROCM_PACKAGES[*]})'
++ array=(${USECASE_ROCM_PACKAGES[*]})
+ [[ -z rocm ]]
+ PACKAGES+=(${array[*]})
+ [[ ! no-dkms =~ no-dkms ]]
+ [[ -n '' ]]
+ [[ -n '' ]]
+ add_package_list Vulkan
+ local listname=Vulkan
+ local option
+ array=()
+ local array
+ local listopts
+ eval 'listopts=$VULKAN_OPTION'
++ listopts=
+ debian_build_package_list
+ dpkg --print-foreign-architectures
+ grep -q i386
+ OPTIONS+=(no-32)
+ [[ hsa-runtime-rocr4wsl-amdgpu rocm = *\-\l\i\b\3\2* ]]
+ [[ hsa-runtime-rocr4wsl-amdgpu rocm = *\:\i\3\8\6* ]]
+ [[ ! no-dkms no-32 =~ no-dkms ]]
+ [[ no-dkms no-32 =~ no-32 ]]
+ PACKAGES=("${PACKAGES[@]/*lib32/}")
+ PACKAGES=("${PACKAGES[@]/*i386/}")
+ [[ ! -z '' ]]
+ add_rocm_release
+ local i
+ [[ -n '' ]]
+ debian_check_multi_rocm_install
+ dpkg -l
+ grep -q 'rocm-core[0-9]'
+ command -v wslinfo
++ wslinfo --msal-proxy-path
```

If I execute the wslinfo separatly it also hangs.
```
 wslinfo --msal-proxy-path
```

This one works
```
thsauvag@Thomas-PC:~$ wslinfo --wsl-version
2.3.26
```

Just to be sure, I checked and I'm up to date on the wsl version (sorry for the french)
```
PS C:\Users\sauva> wsl --update
Recherche des mises à jour.
La version la plus récente de Sous-système Windows pour Linux est déjà installée.
PS C:\Users\sauva> wsl --version
Version WSL : 2.3.26.0
Version du noyau : 5.15.167.4-1
Version WSLg : 1.0.65
Version MSRDC : 1.2.5620
Version direct3D : 1.611.1-81528511
Version de DXCore : 10.0.26100.1-240331-1435.ge-release
Version de Windows : 10.0.26100.2894
```

---

### 评论 #7 — lucbruni-amd (2025-01-23T16:03:36Z)

Hi @SauvageThomas,

Thanks for providing this information. This almost certainly is an issue with WSL as you are not able to run `wslinfo --msal-proxy-path`. As per `wslinfo -h`, `--msal-proxy-path` should only display the path to the MSAL proxy application. I am not able to reproduce your issue and here is my output:

```
rocm@MKMLUCBRUNI01:~$ wslinfo --msal-proxy-path
/mnt/c/Program Files/WSL/msal.wsl.proxy.exe
```

and, here is my version information, as a comparison:

```
rocm@MKMLUCBRUNI01:~$ wslinfo --wsl-version
2.3.26
...
PS C:\Users\lucbruni> wsl --version
WSL version: 2.3.26.0
Kernel version: 5.15.167.4-1
WSLg version: 1.0.65
MSRDC version: 1.2.5620
Direct3D version: 1.611.1-81528511
DXCore version: 10.0.26100.1-240331-1435.ge-release
Windows version: 10.0.22621.4317
```

Only difference here is Windows version.

As we've isolated this to WSL, my first suggestion would be to try [installing an older version of WSL](https://learn.microsoft.com/en-us/windows/wsl/install-manual) as this could be a newer issue on some systems. Their releases list is [here](https://github.com/microsoft/WSL/releases). Then, try again with Ubuntu 22.04. I recommend recording all your installation steps as well.

If the issue persists, you will need to file an issue with WSL on their [issues](https://github.com/microsoft/WSL/issues) page, since `wslinfo --msal-proxy-path` should not be hanging when run in isolation.

Please let me know if you need further assistance. Thanks!

---

### 评论 #8 — SauvageThomas (2025-01-27T07:59:07Z)

Hi, thanks for the answers. Right now I don't really have the time to investigate it more. I might test it again in the future. You can close it since it' an issue with WSL.

---

### 评论 #9 — lucbruni-amd (2025-01-27T14:48:41Z)

No problem. Feel free to reach out if you have additional issues with ROCm in the future, and I'd be happy to help.

---
