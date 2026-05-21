# [Issue]: Fresh Ubuntu 22.04.3 install with only one screen resolution after setup complete.

> **Issue #2613**
> **状态**: closed
> **创建时间**: 2023-10-29T02:02:54Z
> **更新时间**: 2024-06-19T14:29:04Z
> **关闭时间**: 2024-06-19T14:29:04Z
> **作者**: as-shura
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2613

## 描述

### Problem Description


![Screenshot from 2023-10-29 03-01-58](https://github.com/RadeonOpenCompute/ROCm/assets/123847861/a096f61f-d3d6-48f0-92ba-8769e8a2cbe0)

I cannot set the screen resolution to higher than what it is shown. I need at least HD resolution.


### Operating System

Ubuntu

### CPU

AMD Ryzen 9 5950X 16-Core Processor

### GPU

Radeon 6600 XT

### ROCm Version

rocm-5.7.0

### ROCm Component

_No response_

### Steps to Reproduce

Install based on this screenshot:

![Screenshot from 2023-10-29 02-47-12](https://github.com/RadeonOpenCompute/ROCm/assets/123847861/b70fb9b6-d3b1-47d7-95fb-3e30911104c0)

And reboot at the end.

### Output of /opt/rocm/bin/rocminfo --support

cvb

---

## 评论 (16 条)

### 评论 #1 — SebaLenny (2023-11-01T23:21:35Z)

Literally same issue. 
Fresh ~~20.04 install~~ 22.04.3 install, sorry my bad
5950X cpu with 7900XTX gpu

---

### 评论 #2 — SebaLenny (2023-11-01T23:42:28Z)

Also if relevant after running command `sudo journalctl -p 3 -b` i get following output
```
lis 02 00:36:27 sebalenny-System-Product-Name kernel: amd_gpio AMDI0030:00: Invalid config param 0014
lis 02 00:36:27 sebalenny-System-Product-Name kernel: blacklist: Problem blacklisting hash (-13)
lis 02 00:36:27 sebalenny-System-Product-Name kernel: blacklist: Problem blacklisting hash (-13)
lis 02 00:36:27 sebalenny-System-Product-Name kernel: blacklist: Problem blacklisting hash (-13)
lis 02 00:36:27 sebalenny-System-Product-Name kernel: blacklist: Problem blacklisting hash (-13)
lis 02 00:36:28 sebalenny-System-Product-Name systemd-udevd[569]: /etc/udev/rules.d/70-amdgpu.rules:1 Invalid operator for GROUP.
lis 02 00:36:29 sebalenny-System-Product-Name systemd[1]: Failed to start Process error reports when automatic reporting is enabled.
lis 02 00:36:41 sebalenny-System-Product-Name gnome-session-binary[1453]: GLib-GIO-CRITICAL: g_bus_get_sync: assertion 'error == NULL || *error == NULL' failed
lis 02 00:36:41 sebalenny-System-Product-Name gnome-session-binary[1453]: GLib-GIO-CRITICAL: g_bus_get_sync: assertion 'error == NULL || *error == NULL' failed
lis 02 00:36:44 sebalenny-System-Product-Name gdm-password][1931]: gkr-pam: unable to locate daemon control file
lis 02 00:36:45 sebalenny-System-Product-Name systemd[1939]: Failed to start Application launched by gnome-session-binary.
lis 02 00:36:45 sebalenny-System-Product-Name systemd[1939]: Failed to start Application launched by gnome-session-binary.
lis 02 00:36:46 sebalenny-System-Product-Name systemd[1939]: Failed to start Application launched by gnome-session-binary.
lis 02 00:36:47 sebalenny-System-Product-Name gdm-launch-environment][1341]: GLib-GObject: g_object_unref: assertion 'G_IS_OBJECT (object)' failed
lis 02 00:37:06 sebalenny-System-Product-Name pulseaudio[1948]: GetManagedObjects() failed: org.freedesktop.DBus.Error.TimedOut: Failed to activate service 'org.bluez': timed out (service_start_timeout=25000ms)
```

---

### 评论 #3 — danielzgtg (2023-11-07T22:34:30Z)

- You don't need `amdgpu-install`, and I was never able to get it working. I just added the repo and installed only the packages I needed. Specifically, don't install the kernel driver on newer kernels
- Most of your journalctl was normal for me except for the first line
- What's the output of `xrandr` (should work even on Wayland)? Do the resolutions appear there?
- Do the options appear if you lower your refresh rate?
- ROCm 5.7 ***.1*** is out
- Run `apt-cache policy PACKAGENAME` for all ROCm packages that were installed. If the "*" says you installed from the Ubuntu repo instead of repo.radeon.com, you need to uninstall everything, create a file in `/etc/apt/preferences.d/`, and reinstall everything

> Literally same issue.
> Fresh 20.04 install

I trust that you installed the corresponding version, not the "for Ubuntu 2***2***.04.3 HWE"?

---

### 评论 #4 — SebaLenny (2023-11-09T18:22:49Z)

Sorry for late response (it was Ubuntu 22.04... my bad). 
I have decided to reinstall Ubuntu again (full install) and on fresh install i have `lis 09 19:04:52 Kompek kernel: amd_gpio AMDI0030:00: Invalid config param 0014` error ... weird.

Command `xrandr` gave following result ... weird that its not full 165 Hz 
```
sebalenny@Kompek:~$ xrandr
Screen 0: minimum 16 x 16, current 2560 x 1440, maximum 32767 x 32767
XWAYLAND0 connected primary 2560x1440+0+0 (normal left inverted right x axis y axis) 600mm x 340mm
   2560x1440    164.91*+
   1920x1440    164.91  
   1600x1200    164.80  
   1440x1080    164.74  
   1400x1050    164.77  
   1280x1024    164.81  
   1280x960     164.80  
   1152x864     164.77  
   1024x768     164.78  
   800x600      164.72  
   640x480      164.26  
   320x240      163.69  
   1920x1200    164.80  
   1680x1050    164.73  
   1440x900     164.74  
   1280x800     164.65  
   720x480      164.67  
   640x400      164.01  
   320x200      161.83  
   2048x1152    164.83  
   1920x1080    164.76  
   1600x900     164.77  
   1368x768     164.82  
   1280x720     164.71  
   1024x576     164.65  
   864x486      164.71  
   720x400      164.23  
   640x350      164.46 
```
I will install ROCm and see what happens... (I will try to follow this guide `https://rocm.docs.amd.com/en/latest/deploy/linux/quick_start.html` this time)

---

### 评论 #5 — SebaLenny (2023-11-09T18:45:28Z)

And after rebooting I got ...
```
sebalenny@Kompek:~$ xrandr 
xrandr: Failed to get size of gamma for output default
Screen 0: minimum 1024 x 768, current 1024 x 768, maximum 1024 x 768
default connected primary 1024x768+0+0 0mm x 0mm
   1024x768      76.00* 
```

---

### 评论 #6 — danielzgtg (2023-11-12T03:16:36Z)

> amd_gpio AMDI0030:00: Invalid config param 0014

It's harmless. I Googled https://forum.endeavouros.com/t/new-error-warning-amd-gpio-amdi0030-invalid-config-param-0014/43651 . They silenced the warning in newer kernels with https://lore.kernel.org/lkml/20230717201652.17168-1-mario.limonciello@amd.com/T/

> weird that its not full 165 Hz

I assume that's also fine. North American TV is advertised as 60Hz but it's actually 59.97Hz. This is seen in some mp4 files and I assume your monitor is similar.

> I will try to follow this guide https://rocm.docs.amd.com/en/latest/deploy/linux/quick_start.html this time)
> sudo apt install amdgpu-dkms

I never got the dkms version of amdgpu to work. I always used Ubuntu's builtin amdgpu module and it worked for both monitor resolution and ROCm last time.

---

### 评论 #7 — SebaLenny (2023-11-13T21:29:36Z)

Managed to make it working.
This time I used `https://repo.radeon.com/amdgpu-install/5.7.1/ubuntu/jammy/` script. For my case I used `sudo amdgpu-install --usecase=graphics,rocm` usecases.
Important step is to grant user proper accesses
```
sudo usermod -aG video $USER
sudo usermod -aG render $USER
```
Also very important is secure boot thing ... when encountering `Perform MOK management` screen be sure to select `Enroll MOK` (that is not default option) instead of `Continue boot` ... go figure if you are linux noob like myself ...
After rebooting I still had proper resolution and performing  command `rocminfo | grep gfx` (relevant for my usecase) gives following output 
```
  Name:                    gfx1100                            
      Name:                    amdgcn-amd-amdhsa--gfx1100 
```

---

### 评论 #8 — as-shura (2023-11-15T21:02:49Z)

Thanks for your detailed process. It works for me also but I was not able to run pytorch with GPU...
It returns False all the time when I try this code: 

```
rocminfo | grep gfx
  Name:                    gfx1032                            
      Name:                    amdgcn-amd-amdhsa--gfx1032 

import torch
cuda = torch.cuda.is_available()
```

I used this command for the install process:

`
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.6
`

---

### 评论 #9 — SebaLenny (2023-11-15T21:25:04Z)

I assume you did `pip3 uninstall torch torchvision torchaudio` before `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.6` ? (I assume you are propably trying to get `Automatic1111` working).

---

### 评论 #10 — as-shura (2023-11-15T22:17:31Z)

Good point I didn't uninstall anything I am trying what you just have suggested. I will update after the 1.5 GB download finished.

Thank you appreciated

---

### 评论 #11 — as-shura (2023-11-17T02:48:44Z)

Damn I uninstalled python 3.10 and all my system broke I ended up with only command line login all the desktop was removed all the programs, etc...

I did a bad move but I will now install python 3.8 and then remove python 3.10

```
The following additional packages will be installed:
  libllvm16.0.50701-amdgpu:i386
The following NEW packages will be installed:
  libllvm16.0.50701-amdgpu:i386
0 upgraded, 1 newly installed, 0 to remove and 15 not upgraded.
24 not fully installed or removed.
Need to get 0 B/24,6 MB of archives.
After this operation, 101 MB of additional disk space will be used.
Do you want to continue? [Y/n] Y
(Reading database ... 232599 files and directories currently installed.)
Preparing to unpack .../libllvm16.0.50701-amdgpu_1%3a16.0.50701-1664922.22.04_i386.deb ...
Unpacking libllvm16.0.50701-amdgpu:i386 (1:16.0.50701-1664922.22.04) ...
dpkg: error processing archive /var/cache/apt/archives/libllvm16.0.50701-amdgpu_1%3a16.0.50701-1664922.22.04_i386.deb (--unpack):
 trying to overwrite '/opt/amdgpu/lib/i386-linux-gnu/llvm-16.0/lib/libLLVM-16.so', which is also in package libllvm16.0.50700-amdgpu:i386 1:16.0
.50700-1666569.22.04
dpkg-deb: error: paste subprocess was killed by signal (Broken pipe)
Errors were encountered while processing:
 /var/cache/apt/archives/libllvm16.0.50701-amdgpu_1%3a16.0.50701-1664922.22.04_i386.deb
E: Sub-process /usr/bin/dpkg returned an error code (1)

```

I found this solution :
`https://askubuntu.com/questions/1062171/dpkg-deb-error-paste-subprocess-was-killed-by-signal-broken-pipe`

---

### 评论 #12 — as-shura (2023-11-18T01:10:17Z)

Everything is working pretty nice right now!

---

### 评论 #13 — danielzgtg (2023-11-18T02:14:30Z)

@as-shura It is not recommended to uninstall Ubuntu's system Python version. It is recommended to install the desired version side-by-side and configure venv to use that version. It is also more reproducible to avoid `pip uninstall` and just delete and recreate the venv to correct the version of packages.

---

### 评论 #14 — as-shura (2023-11-18T23:37:19Z)

> @as-shura It is not recommended to uninstall Ubuntu's system Python version. It is recommended to install the desired version side-by-side and configure venv to use that version. It is also more reproducible to avoid `pip uninstall` and just delete and recreate the venv to correct the version of packages.

I realized that the gnome-terminal is using Python 3.10 and when I switched to 3.8 it stopped working. I replaced the gnome-terminal with another terminal which is not depending on 3.10.

What are you recommending then? Do you have any tutorial to clarify what you are trying to explain please.


---

### 评论 #15 — danielzgtg (2023-11-19T00:50:25Z)

```bash
# Install Python3.8 and its venv
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8-venv python3.8
# Avoid uninstalling anything or pip installing anything into the global environment

# Create venv
cd /path/to/project
python3.8 -m venv ./venv # Cleanly scope all package installs to ./venv directory
source ./venv/bin/activate # Point the current bash instance to use the ./venv directory
# Your shell prompt should now say (venv)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.6 # Install everything you need into the ./venv
pip freeze > ./requirements.txt # Back up all the packages' versions

# Use the venv
source ./venv/bin/activate
python --version
python ./your_file.py

# Reinstall packages when cloning the git repo on another computer or undoing a package install
# Maybe do this in a new terminal
rm -rf ./venv # Just delete the broken environment, we will recreate it from backup.
python3.8 -m venv ./venv
source ./venv/bin/activate
pip install -r ./requirements.txt # Restore backed up versions
pip install the_correct_packages # Add --index-url when necessary
pip freeze > ./requirements.txt # Create new backup
```

Most machine learning projects assume you will be using some kind of virtual environment. The above is just an overview of what you might need now but Googling venv gives you https://stackoverflow.com/questions/1534210/use-different-python-version-with-virtualenv and https://docs.python.org/3/library/venv.html . 

You can replace venv with conda or something else, but that would be even more complicated and off topic. Generally on Ubuntu, you should not use `pip` outside of an active venv. It's because the files in `/usr` are assumed to be controlled by Ubuntu and should not be manually modified. Using pip to modify the home directory is not as bad but still risks package conflicts with Ubuntu and different packages that expect different versions of dependencies. The only time it's acceptable is when you're in a Docker container. If you want to automate or make the above steps visual, PyCharm has a dropdown to select the Python version when creating the venv.

---

### 评论 #16 — ppanchad-amd (2024-05-15T19:06:49Z)

@as-shura Has your issue been resolved? Thanks!

---
