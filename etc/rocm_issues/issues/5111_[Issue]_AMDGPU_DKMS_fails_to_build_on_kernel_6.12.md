# [Issue]: AMDGPU DKMS fails to build on kernel 6.12

> **Issue #5111**
> **状态**: open
> **创建时间**: 2025-07-28T15:14:27Z
> **更新时间**: 2025-11-08T23:46:16Z
> **作者**: roryyamm
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5111

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Attempting to install amdgpu-dkms from the Ubuntu/Debian sources using any kernel version in the 6.12 series causes installation to fail. Upon inspection, for the current Debian Unstable/Devuan Ceres kernel version, the end of the build log looks like this:

```
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
grep: /usr/src/ofa_kernel/x86_64/6.12.33+deb13-amd64/Module.symvers: No such file or directory
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for module configuration... done
configure: creating ./config.status
config.status: creating config/config.h
Makefile:54: *** dma_resv->seq is missing. exit....  Stop.

# exit code: 2
# elapsed time: 00:00:13
```

[make.log](https://github.com/user-attachments/files/21471718/make.log)

Symlinking `/usr/src/linux-headers-6.12.38+deb13-amd64` to `/usr/src/ofa_kernel/x86_64/6.12.38+deb13-amd64` produces the following output:

```
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for module configuration... done
configure: creating ./config.status
config.status: creating config/config.h
Makefile:54: *** dma_resv->seq is missing. exit....  Stop.

# exit code: 2
# elapsed time: 00:00:13
----------------------------------------------------------------
```

[make.log](https://github.com/user-attachments/files/21472014/make.log)

This same behavior is experienced on kernel versions 6.12.33, 6.12.37, and 6.12.38. This same behavior is experienced on Debian and Devuan, which is to be expected as both are identical save for their init systems. 

This result is unexpected, as amdgpu-dkms is explicitly supported on kernel 6.11, and will apparently be supported on 6.14 after the official Ubuntu 24.04.3 HWE kernel release. 6.12 is in between the two, yet fails to work. 

### Operating System

Devuan Excalibur/Ceres (equivalent to Debian Trixie/Sid)

### CPU

AMD Ryzen 7 5700X 8-Core Processor

### GPU

 Advanced Micro Devices [AMD/ATI] Navi 23 [Radeon RX 6650 XT / 6700S 6800S]

### ROCm Version

ROCm 6.4.2, ROCm 6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

1. Install Debian Trixie/Devuan Excalibur 
2. (Alternatively) Install Debian Bookworm/Devuan Daedalus and add `testing` or `unstable` repositories
3. Upgrade linux-image and linux-headers to their up-to-date versions
4. Install the ROCm repository
5. Attempt to install amdgpu-dkms
6. Curse the darkness

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Debian Trixie is due to release on August 9th, 2 days after the Ubuntu HWE kernel release on the 7th. It will use some point release of kernel 6.12. Neither 6.14 nor 6.11 are offered in the Debian package repositories of Trixie or Sid, precluding their installation. It would be appreciated if ROCm were able to support 6.12, so that Debian users do not have to choose between a functioning AMDGPU setup and a new version of their operating system. 

Barring that, it would be nice if uninstalling amdgpu-dkms also removed `/etc/modprobe.d/blacklist-amdgpu.conf` so that users aren't left with a fallback graphics stack when they fail to install amdgpu-dkms. 

---

## 评论 (23 条)

### 评论 #1 — ppanchad-amd (2025-07-28T15:43:38Z)

Hi @roryyamm. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — damnms (2025-08-02T12:20:22Z)

just hit the same problem, running debian trixie on a 8845hs

---

### 评论 #3 — adityas-amd (2025-08-06T15:00:01Z)

At this time, Linux kernel 6.12 is not officially supported by the `amdgpu-dkms` module, and there are no current plans to add support for this version. It is recommended to use a supported kernel version — either: 6.11, which is currently supported, or 6.14, which will be supported with the upcoming Ubuntu 24.04.3 HWE kernel release (expected August 7).
Unfortunately, so you may need to consider- Downgrading to 6.11 (if available via backports) or waiting for 6.14 to be available upstream.


---

### 评论 #4 — damnms (2025-08-06T17:42:59Z)

@adityas-amd thats pretty bad because debian trixie, which is supposed to be released this friday, will run on 6.12 and i highly doubt there will be an easy way to downgrade or to get 6.14. 

---

### 评论 #5 — aha1zint (2025-08-10T21:28:14Z)

are there is any plans to support debian 13 ? i just want the dkms drivers for the opencl 

---

### 评论 #6 — roryyamm (2025-08-11T15:42:14Z)

> Unfortunately, so you may need to consider- Downgrading to 6.11 (if available via backports) or waiting for 6.14 to be available upstream.

Kernel 6.11 ISN'T available in backports. Only 6.1. Conversely, 6.14 isn't going to be available either; they're already testing 6.15 in Experimental, and 6.14 never made it to Unstable or Testing.  

I had to compile the entire kernel from scratch to get this to work properly. You say you support Debian, yet somehow skip over supporting the only kernel version the current Trixie ships? 

If you're going to support Debian, at least package a version of the kernel that supports AMDGPU in your repo, so we can install it if we don't have it. 

---

### 评论 #7 — JonChesterfield (2025-08-19T00:20:08Z)

This can be done but it was not obvious.

First, kernel 6.11 is available in Trixie under "snapshots", which are magic strings one can add to the apt machinery to find other things.

```
# This has a 6.11.10 kernel in it
sudo cat << EOF >> /etc/apt/sources.list/snapshot.list
deb     [check-valid-until=no] https://snapshot.debian.org/archive/debian/20241201T111800Z/ trixie main
deb-src [check-valid-until=no] https://snapshot.debian.org/archive/debian/20241201T111800Z/ trixie main
EOF

# Don't forget the headers
sudo apt install linux-headers-6.11.10-amd64 linux-image-6.11.10-amd64
```

The amdgpu-dkms package from rocm 6.4.3 (specifically the Ubuntu 24.04 deb in my case) then refuses to build because 'ofa_kernel' doesn't exist. Brief searching doesn't reveal what that is so I'm going to assume it's an ubuntu naming convention and hack around it:

```
ln -s /usr/src/linux-headers-6.11.10-amd64 /usr/src/ofa_kernel/x86_64/6.11.10-amd64
```

That brings us to https://github.com/ROCm/ROCm/issues/3379 which points out that the config scripts somewhere in this need to be updated (as of 6.8 era), but proposes a workaround (which probably harms cross compiling):

```
cd /usr/lib/linux-kbuild-6.11.10/tools/objtool
sudo mv objtool objtool_old
sudo ln -s objtool.real-x86 objtool
```

At that point the deb pulled from Ubuntu compiles successfully. Machine reboots successfully too.

Probably also important are the associated firmware files, which look to be _older_ than that found in linux 6.12 - but I'd expect it to be important for stability to have firmware files matching the driver.


-----------

Sigh. The above is true but insufficient. That'll get you the dkms driver built and inserted. Took a while to discover that the debian kernel has some features switched off that carry over into the driver.

Specifically, see here: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/drivers/gpu/drm/amd/amdkfd/kfd_chardev.c?h=v6.11#n1689

The 'xnack' feature is the one that lets at least some cards access host memory effectively. Rocm's driver built against trixie's 6.11 will have that macro disabled so trying to set xnack returns EPERM. I _think_ this will be unblocked by Debian 6.13 when that comes around, see https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1015871#75 for enabling the corresponding parts in the kernel config, but haven't verified. With the 6.11 kernel rebuilt with a modified config (to enable everything named hsa) plus the dkms driver, tests are running successfully.

---

### 评论 #8 — leonzwrx (2025-08-20T17:21:20Z)

Any clue when mainstream Debian stable (kernel 6.12) will be supported.. Guessing there is a sea of people that are stuck now

---

### 评论 #9 — RobertoMaurizzi (2025-09-05T13:16:26Z)

I was able to compile amdgpu-dkms on Trixie's 6.12.xx months ago (around April on a Minisforum AI Max Pro with a Ryzen 370) but I had to download gcc-11 packages from testing (this might have changed in the meantime, I still have them installed so I'm not sure).

After installing:

```
gcc-11-base_11.5.0-2_amd64.deb
libasan6_11.5.0-2_amd64.deb
libgcc-11-dev_11.5.0-2_amd64.deb
libstdc++-11-dev_11.5.0-2_amd64.deb
libtsan0_11.5.0-2_amd64.deb
```

...and setting `export SRCARCH=x86` it started working.

I now moved from `trixie` to `testing` directly (I want recent desktop packages) and I'm having troubles compiling the module, but on the other hand 6.16.3 probably comes with a very recent version (not sure if equivalent to what's available in ROCm 6.4.3 however...) so I'll simply try what happens with the in-kernel module (6.16 release is recent enough I still have to try a reboot, I'll do it over the weekend when I have time to recover from any disaster that it might cause 😅 ).
We can hope ROCm 7.0 will work with 6.16 (and maybe support gfx1150 so I didn't buy one "for nothing" :-P )

---

### 评论 #10 — karora (2025-09-06T04:15:52Z)

@ppanchad-amd just to note that the Linux 6.12 series is the most recent LTS kernel release (EOL December 2026), if that's worth noting on AMD's internal bug tracker.  I'm sure that it being the latest LTS release factored significantly into it being chosen for Trixie.
Tagging @cgmb to see if there's anything he can add since this has been extant for over a month now - I guess I'm late to the party with my shiny new HX370 laptop, but I'd love there to be a party :-)

---

### 评论 #11 — meefik (2025-09-13T18:01:25Z)

My system is Debian 13 with the `6.12.43+deb13-amd64` kernel. I successfully built AMD GPU driver with the following parameters.

APT config `/etc/apt/sources.list.d/amdgpu.list`:
```
deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/6.4.3/ubuntu noble main
```
For more details, visit [the official AMD page](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html).

Create the correct directory for the kernel headers:
```
mkdir -p /usr/src/ofa_kernel/x86_64/
ln -s /usr/src/linux-headers-`uname -r` /usr/src/ofa_kernel/x86_64/`uname -r`
```

Change the current kernel version for amdgpu:
```
uname -r | tee /var/tmp/amdgpu-dkms-kernels
```

Build the amdgpu kernel module:
```
export SRCARCH=x86
dpkg-reconfigure amdgpu-dkms
```


---

### 评论 #12 — daryltucker (2025-09-25T00:37:21Z)

Thank you so much @meefik you had a few pieces I was missing.  I was on `6.4.2` and couldn't get things working, so I tried `7.0.1`, which seems like it was a really bad idea.  It looks like regardless, the DKMS system is pretty broken, so I'm not sure if 6.4.2 could have worked if I had this additional information, but just to be clear, I was able to get `6.4.3` working.

I would never have `ln`'d, as I have the Kernel source in the appropriate path.  Not sure how this one slipped by....

Anyways...

Here is a script to downgrade/switch packages from one repository to another: [apt-switch-repos](https://gist.github.com/daryltucker/fc54f760eeba0993ba299b5d6d99eeb2#file-apt-switch-repos)

Here is a list of all the packages I had installed from `6.4.3` at the time of the successful `.ko` build: [ROCM-6.4.3_Linux-6.12_Packages.txt](https://gist.github.com/daryltucker/e0c2e307c9e234f7d4bd9791138a2942#file-rocm-6-4-3_linux-6-12_packages-txt)

Here are the steps I took to get ROCm 6.4.3 DKMS working on Kernel 6.12 (Debian 13): [ROCM-6.4.3_Linux-6.12_DKMS.mkd](https://gist.github.com/daryltucker/f10140124491347bf4e0f05c1e1e68fb#file-rocm-6-4-3_linux-6-12_dkms-mkd)


I reproduced these steps on another Debian 13 machine.  The steps were different because that machine had access to GCC 11.4.  Not entirely sure (and not really looking for a solution tbh), but I do know the working system uses the old `sources.list` while the machine without access to GCC 11.4 has a `sources.list.d/debian.list`.

---

If anybody knows how to set `SRCARCH=x86` for AMDGPU DKMS (and not the entire system), please let me know.

Edit:  Found it --
```bash
$ tail -n 2 /usr/src/amdgpu-6.12.12-2194681.24.04/dkms.conf
MAKE[0]="SRCARCH=x86 make KERNELVER=$kernelver"
```

---

### 评论 #13 — SakiiCode (2025-09-27T18:59:46Z)

I managed to install `sudo amdgpu-install --usecase=graphics,hip,opencl` but now it looks like the gpu is not detected, it boots to tty1 and when I type `startx` I get 1024x768 single display.

LMDE 7 Cinnamon, RX 6600 XT

Is there anything missing? Already added myself to video and render groups

---

### 评论 #14 — five-elephants (2025-10-09T09:30:57Z)

> If anybody knows how to set SRCARCH=x86 for AMDGPU DKMS (and not the entire system), please let me know.

It seems to work to put it in `/etc/dkms/amdgpu`:
```
MAKE[0]="SRCARCH=x86 'make' KERNELVER=$kernelver"
```
Accoding to `man dkms` it would also be possible to target specific versions.

---

### 评论 #15 — bronger (2025-10-09T10:26:39Z)

> At this time, Linux kernel 6.12 is not officially supported by the `amdgpu-dkms` module, and there are no current plans to add support for this version. It is recommended to use a supported kernel version — either: 6.11, which is currently supported, or 6.14, which will be supported with the upcoming Ubuntu 24.04.3 HWE kernel release (expected August 7). Unfortunately, so you may need to consider- Downgrading to 6.11 (if available via backports) or waiting for 6.14 to be available upstream.

Given the strong arguments to reconsider not supporting Linux 6.12, does it make sense to wait for such support? Because the alternatives mentioned on this issue are extremely tortuous.

---

### 评论 #16 — RobertoMaurizzi (2025-10-09T16:59:53Z)

Again, I compiled amdgpu-dkms on Debian's 6.12 several months ago (April or May). I don't understand why people here say it's unsupported.
I'm now on 6.16.9 where (without dkms) you get the recently patched support for dynamic VRAM. The only thing that protests is ollama because it tried to find a /version file in /proc that with the in-kernel driver isn't there, but then again you can set the version with an env variable and it works.

---

### 评论 #17 — wfjsw (2025-10-09T17:14:51Z)

Because it requires system modification that makes Debian looks like Ubuntu, and it becomes a hassle as soon as you also has an NVIDIA card installed. Those modification will have to be reverted prior to NVIDIA dkms build, otherwise it will fail for some other mysterious reason. Suddenly I have to take whole more steps for a kernel upgrade because they all try to build at the same time which will guarantee failure, rather than a simple `apt upgrade`. 

---

### 评论 #18 — RobertoMaurizzi (2025-10-09T17:21:28Z)

> Because it requires system modification that makes Debian looks like Ubuntu

the only modification I had to make was the one to set the architecture to x86_64.

Then again, I don't have an NVidia card on this computer... but on the ome I do have one, it was a constant fight at every new driver release to get it built properly... their "whoops it won't work if you have 2 monitors" was expecially egregious and made me remove their repository so that it wouldn't break my system at the next release, so maybe the problem isn't in AMD drivers but in Nvidia's ones?


---

### 评论 #19 — wfjsw (2025-10-09T17:31:01Z)

For me it still tries to look for `/usr/src/ofa_kernel`, and when exists, that somehow triggers some Ubuntu specific path for NVIDIA driver which will fail.

I do have some one-off problems with NVIDIA, though I suspect it's also one-off if I only have AMD. It only becomes annoyingly recurring when they are combined.


---

### 评论 #20 — bronger (2025-10-10T10:06:50Z)

Quite frankly, “supported“ means for me that the steps mentioned on https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html work for the current Debian stable.

This is not the case. I do not complain, but I have to make a decision: Wait, or fight through the workarounds? @adityas-amd

---

### 评论 #21 — leonzwrx (2025-10-14T20:16:00Z)

Sweet. Debian 13 and 6.12 is officially supported, install smooth as butter

---

### 评论 #22 — guoh27 (2025-10-30T09:50:34Z)

kernel 6.12 with amdgpu-dkms 6.14.14, still Makefile:62: *** dma_resv->seq is missing. exit....  Stop.

---

### 评论 #23 — SakiiCode (2025-11-08T23:46:16Z)

For anyone having the same problem, booting into tty1 was because of secure boot and the drivers not loading
MOK Manager never showed up for me, that's why it was confusing

To fix it I had to:
```
sudo mokutil --enable-validation
sudo mokutil --import /var/lib/dkms/mok.pub
```
Note that MOK Manager has English keyboard layout

See https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/install-faq.html#issue-8-the-amdgpu-driver-is-not-loaded-after-installation

---
