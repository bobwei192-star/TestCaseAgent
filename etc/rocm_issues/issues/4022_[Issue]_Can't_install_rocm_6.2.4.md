# [Issue]: Can't install rocm 6.2.4

> **Issue #4022**
> **状态**: closed
> **创建时间**: 2024-11-09T19:11:20Z
> **更新时间**: 2024-11-12T18:31:15Z
> **关闭时间**: 2024-11-12T18:31:14Z
> **作者**: jdchn
> **标签**: Under Investigation, ROCm 6.2.3, N/A
> **URL**: https://github.com/ROCm/ROCm/issues/4022

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **N/A** (颜色: #ededed)

## 描述

### Problem Description

The repository InRelease indices for ROCm 6.2.4 appear to be inconsistent with Release artifacts as of 2024-11-09 1900Z. This issue applies to "noble", "focal", and "jammy".

Note — I had to set the ROCm Version field to `ROCm 6.2.3` because there was no option for `ROCm 6.2.4`.

### Operating System

Ubuntu 24.04.1 LTS (Noble Numbat) 

### CPU

N/A

### GPU

N/A

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

```bash
$ echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.2.4 noble main"     | sudo tee --append /etc/apt/sources.list.d/rocm.list
$ sudo apt update
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

```bash
$ sudo apt update
...
Get:5 https://repo.radeon.com/rocm/apt/6.2.4 noble/main amd64 Packages [29.6 kB]
Err:5 https://repo.radeon.com/rocm/apt/6.2.4 noble/main amd64 Packages
  File has unexpected size (68560 != 29552). Mirror sync in progress? [IP: 69.192.139.240 443]
  Hashes of expected file:
   - Filesize:29552 [weak]
   - SHA256:5cba5765fe11410ac7a3679e5c8b2eab8c2e294971d8a9e4267c8784b746f21c
   - SHA1:53982ce2011f79dedaf8a5a69c361b8825fea447 [weak]
   - MD5Sum:d55fc8f653990ff0a080cdb20e55fc22 [weak]
  Release file created at: Wed, 06 Nov 2024 18:36:13 +0000
Hit:6 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:7 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Fetched 2617 B in 1s (3549 B/s)
Reading package lists... Done
E: Failed to fetch https://repo.radeon.com/rocm/apt/6.2.4/dists/noble/main/binary-amd64/Packages.gz  File has unexpected size (68560 != 29552). Mirror sync in progress? [IP: 69.192.139.240 443]
   Hashes of expected file:
    - Filesize:29552 [weak]
    - SHA256:5cba5765fe11410ac7a3679e5c8b2eab8c2e294971d8a9e4267c8784b746f21c
    - SHA1:53982ce2011f79dedaf8a5a69c361b8825fea447 [weak]
    - MD5Sum:d55fc8f653990ff0a080cdb20e55fc22 [weak]
   Release file created at: Wed, 06 Nov 2024 18:36:13 +0000
```

https://repo.radeon.com/rocm/apt/6.2.4/dists/noble/Release
```text
Origin: repo.radeon.com
Label: repo.radeon.com
Suite: noble
Codename: noble
Version: 6.2.4
Date: Fri, 08 Nov 2024 18:58:55 UTC
Architectures: amd64
Components: main proprietary
Description: ROCm APT Repository
MD5Sum:
 3e929ad7bef77ab769bdcc7cb2e921fe 351040 main/binary-amd64/Packages
 46d07f487bf91c2cb2ab321a7b96178a 68560 main/binary-amd64/Packages.gz
```

https://repo.radeon.com/rocm/apt/6.2.4/dists/noble/InRelease
```text
Origin: repo.radeon.com
Label: repo.radeon.com
Suite: noble
Codename: noble
Version: 6.2.4
Date: Wed, 06 Nov 2024 18:36:13 UTC
Architectures: amd64
Components: main proprietary
Description: ROCm APT Repository
MD5Sum:
 292daa54c9cacecd4d8915fbdee83897 111626 main/binary-amd64/Packages
 d55fc8f653990ff0a080cdb20e55fc22 29552 main/binary-amd64/Packages.gz
```

See also #3980 .

---

## 评论 (12 条)

### 评论 #1 — johnnynunez (2024-11-10T06:45:47Z)

> ### Problem Description
> The repository InRelease indices for ROCm 6.2.4 appear to be inconsistent with Release artifacts as of 2024-11-09 1900Z. This issue applies to "noble", "focal", and "jammy".
> 
> Note — I had to set the ROCm Version field to `ROCm 6.2.3` because there was no option for `ROCm 6.2.4`.
> 
> ### Operating System
> Ubuntu 24.04.1 LTS (Noble Numbat)
> 
> ### CPU
> N/A
> 
> ### GPU
> N/A
> 
> ### ROCm Version
> ROCm 6.2.3
> 
> ### ROCm Component
> _No response_
> 
> ### Steps to Reproduce
> ```shell
> $ echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.2.4 noble main"     | sudo tee --append /etc/apt/sources.list.d/rocm.list
> $ sudo apt update
> ```
> 
> ### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support
> _No response_
> 
> ### Additional Information
> ```shell
> $ sudo apt update
> ...
> Get:5 https://repo.radeon.com/rocm/apt/6.2.4 noble/main amd64 Packages [29.6 kB]
> Err:5 https://repo.radeon.com/rocm/apt/6.2.4 noble/main amd64 Packages
>   File has unexpected size (68560 != 29552). Mirror sync in progress? [IP: 69.192.139.240 443]
>   Hashes of expected file:
>    - Filesize:29552 [weak]
>    - SHA256:5cba5765fe11410ac7a3679e5c8b2eab8c2e294971d8a9e4267c8784b746f21c
>    - SHA1:53982ce2011f79dedaf8a5a69c361b8825fea447 [weak]
>    - MD5Sum:d55fc8f653990ff0a080cdb20e55fc22 [weak]
>   Release file created at: Wed, 06 Nov 2024 18:36:13 +0000
> Hit:6 http://archive.ubuntu.com/ubuntu noble-updates InRelease
> Hit:7 http://archive.ubuntu.com/ubuntu noble-backports InRelease
> Fetched 2617 B in 1s (3549 B/s)
> Reading package lists... Done
> E: Failed to fetch https://repo.radeon.com/rocm/apt/6.2.4/dists/noble/main/binary-amd64/Packages.gz  File has unexpected size (68560 != 29552). Mirror sync in progress? [IP: 69.192.139.240 443]
>    Hashes of expected file:
>     - Filesize:29552 [weak]
>     - SHA256:5cba5765fe11410ac7a3679e5c8b2eab8c2e294971d8a9e4267c8784b746f21c
>     - SHA1:53982ce2011f79dedaf8a5a69c361b8825fea447 [weak]
>     - MD5Sum:d55fc8f653990ff0a080cdb20e55fc22 [weak]
>    Release file created at: Wed, 06 Nov 2024 18:36:13 +0000
> ```
> 
> https://repo.radeon.com/rocm/apt/6.2.4/dists/noble/Release
> 
> ```
> Origin: repo.radeon.com
> Label: repo.radeon.com
> Suite: noble
> Codename: noble
> Version: 6.2.4
> Date: Fri, 08 Nov 2024 18:58:55 UTC
> Architectures: amd64
> Components: main proprietary
> Description: ROCm APT Repository
> MD5Sum:
>  3e929ad7bef77ab769bdcc7cb2e921fe 351040 main/binary-amd64/Packages
>  46d07f487bf91c2cb2ab321a7b96178a 68560 main/binary-amd64/Packages.gz
> ```
> 
> https://repo.radeon.com/rocm/apt/6.2.4/dists/noble/InRelease
> 
> ```
> Origin: repo.radeon.com
> Label: repo.radeon.com
> Suite: noble
> Codename: noble
> Version: 6.2.4
> Date: Wed, 06 Nov 2024 18:36:13 UTC
> Architectures: amd64
> Components: main proprietary
> Description: ROCm APT Repository
> MD5Sum:
>  292daa54c9cacecd4d8915fbdee83897 111626 main/binary-amd64/Packages
>  d55fc8f653990ff0a080cdb20e55fc22 29552 main/binary-amd64/Packages.gz
> ```
> 
> See also #3980 .

For ubuntu 24.04.1
```bash
sudo apt-get remove --purge '^rocm-.*'
sudo apt remove rocm-*
sudo apt purge '*rocm*'
sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"

wget https://repo.radeon.com/amdgpu-install/6.2.4/ubuntu/noble/amdgpu-install_6.2.60204-1_all.deb
sudo apt install ./amdgpu-install_6.2.60204-1_all.deb
sudo amdgpu-install -y --usecase=graphics,rocm

sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
```

---

### 评论 #2 — HardAndHeavy (2024-11-10T08:17:37Z)

I was experiencing the same problem. When I cleaned everything, I came to the error "Unable to locate package rocm"
![image](https://github.com/user-attachments/assets/c50aead5-9fa2-4e9d-93b2-afa8c0aad533)

The rocm package is also not visible on the [ubuntu packages website](https://packages.ubuntu.com/search?suite=oracular&section=all&arch=any&keywords=rocm&searchon=names)


---

### 评论 #3 — johnnynunez (2024-11-10T14:41:04Z)

> I was experiencing the same problem. When I cleaned everything, I came to the error "Unable to locate package rocm" ![image](https://private-user-images.githubusercontent.com/2789372/384670592-c50aead5-9fa2-4e9d-93b2-afa8c0aad533.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzEyNDk5MjYsIm5iZiI6MTczMTI0OTYyNiwicGF0aCI6Ii8yNzg5MzcyLzM4NDY3MDU5Mi1jNTBhZWFkNS05ZmEyLTRlOWQtOTNiMi1hZmE4YzBhYWQ1MzMucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MTExMCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDExMTBUMTQ0MDI2WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ZDQzYTgxMDRjZDkxMDU3NzYwOGRlN2I5MWU2NWQ4YmNhMzMyYmFmOGFmYTI0YmJiNDYxMTU5MGU5NDM3ZDNhNSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.bI0rprs5TwWChCNNTH7VhOVrCEFhsp4css4nGgPB0k8)
> 
> The rocm package is also not visible on the [ubuntu packages website](https://packages.ubuntu.com/search?suite=oracular&section=all&arch=any&keywords=rocm&searchon=names)

You are using wrong command
sudo amdgpu-install -y --usecase=rocm


---

### 评论 #4 — sofiageo (2024-11-10T19:03:36Z)

It looks to me that someone silently updated the 6.2.4 release and the akamai cache is still serving the old files (until 17 november probably?). Silently updating the files has happened a few more times in the past.

---

### 评论 #5 — matoro (2024-11-11T01:22:13Z)

Yes, this is coming up fro rocm 6.2.4 on noble now.

---

### 评论 #6 — HardAndHeavy (2024-11-11T07:47:33Z)

> You are using wrong command sudo amdgpu-install -y --usecase=rocm

Executed all commands in order.
An error appears after the "make" command ` sudo amdgpu-install -y --usecase=graphics,rocm`:
`E: Unable to locate package rocm`
![image](https://github.com/user-attachments/assets/2d518152-47b7-434f-93c0-fc9eab737467)


---

### 评论 #7 — harkgill-amd (2024-11-11T15:13:58Z)

Thanks for the report. There was previously an issue with the ROCm 6.2.3 debian metadata that caused the same `File has unexpected size` error. I do see the differing sizes of `Release` and `InRelease` again, will confirm if the root cause is the same.

@HardAndHeavy, the `Unable to locate package rocm` is due to the rocm repository missing at `/etc/apt/sources.list.d/rocm.list`. A reinstallation of the 6.2.4 amdgpu-install should fix this 
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove

wget https://repo.radeon.com/amdgpu-install/6.2.4/ubuntu/noble/amdgpu-install_6.2.60204-1_all.deb
sudo apt install ./amdgpu-install_6.2.60204-1_all.deb
sudo apt update
```



---

### 评论 #8 — radugrecu97 (2024-11-11T17:17:49Z)

> Thanks for the report. There was previously an issue with the ROCm 6.2.3 debian metadata that caused the same `File has unexpected size` error. I do see the differing sizes of `Release` and `InRelease` again, will confirm if the root cause is the same.
> 
> @HardAndHeavy, the `Unable to locate package rocm` is due to the rocm repository missing at `/etc/apt/sources.list.d/rocm.list`. A reinstallation of the 6.2.4 amdgpu-install should fix this
> 
> ```
> sudo amdgpu-install --uninstall --rocmrelease=all
> sudo apt purge amdgpu-install
> sudo apt autoremove
> 
> wget https://repo.radeon.com/amdgpu-install/6.2.4/ubuntu/noble/amdgpu-install_6.2.60204-1_all.deb
> sudo apt install ./amdgpu-install_6.2.60204-1_all.deb
> sudo apt update
> ```

Had this error yesterday as well when trying to install 6.2.3 on WSL. Now I am trying to install on native Ubuntu but same issue...

```
Get:1 https://repo.radeon.com/amdgpu/6.2.4/ubuntu noble InRelease [5,465 B]
Get:2 https://repo.radeon.com/rocm/apt/6.2.4 noble InRelease [2,617 B]                    
Get:3 https://repo.radeon.com/amdgpu/6.2.4/ubuntu noble/main i386 Packages [10.9 kB]      
Get:4 https://repo.radeon.com/amdgpu/6.2.4/ubuntu noble/main amd64 Packages [13.4 kB]     
Get:5 https://repo.radeon.com/rocm/apt/6.2.4 noble/main amd64 Packages [29.6 kB]
Err:5 https://repo.radeon.com/rocm/apt/6.2.4 noble/main amd64 Packages    
  File has unexpected size (68560 != 29552). Mirror sync in progress? [IP: 95.166.124.186 443]
  Hashes of expected file:
   - Filesize:29552 [weak]
   - SHA256:5cba5765fe11410ac7a3679e5c8b2eab8c2e294971d8a9e4267c8784b746f21c
   - SHA1:53982ce2011f79dedaf8a5a69c361b8825fea447 [weak]
   - MD5Sum:d55fc8f653990ff0a080cdb20e55fc22 [weak]
  Release file created at: Wed, 06 Nov 2024 18:36:13 +0000
Hit:6 http://security.ubuntu.com/ubuntu noble-security InRelease          
Hit:7 http://archive.ubuntu.com/ubuntu noble InRelease
Hit:8 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:9 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Fetched 32.3 kB in 1s (60.4 kB/s)
Reading package lists... Done
E: Failed to fetch https://repo.radeon.com/rocm/apt/6.2.4/dists/noble/main/binary-amd64/Packages.gz  File has unexpected size (68560 != 29552). Mirror sync in progress? [IP: 95.166.124.186 443]
   Hashes of expected file:
    - Filesize:29552 [weak]
    - SHA256:5cba5765fe11410ac7a3679e5c8b2eab8c2e294971d8a9e4267c8784b746f21c
    - SHA1:53982ce2011f79dedaf8a5a69c361b8825fea447 [weak]
    - MD5Sum:d55fc8f653990ff0a080cdb20e55fc22 [weak]
   Release file created at: Wed, 06 Nov 2024 18:36:13 +0000
E: Some index files failed to download. They have been ignored, or old ones used instead.
```



---

### 评论 #9 — harkgill-amd (2024-11-11T18:36:40Z)

The file size mismatch issue has been resolved, and I no longer see any errors on my end. @jdchn, @johnnynunez, and @radugrecu97, could you please try running sudo apt update and proceed with the installation?

---

### 评论 #10 — johnnynunez (2024-11-11T21:29:52Z)

> The file size mismatch issue has been resolved, and I no longer see any errors on my end. @jdchn, @johnnynunez, and @radugrecu97, could you please try running sudo apt update and proceed with the installation?

I have no errors. 

---

### 评论 #11 — jdchn (2024-11-12T01:50:58Z)

> The file size mismatch issue has been resolved, and I no longer see any errors on my end. @jdchn, @johnnynunez, and @radugrecu97, could you please try running sudo apt update and proceed with the installation?

Looks good to me, now. Thank you!

---

### 评论 #12 — harkgill-amd (2024-11-12T18:31:14Z)

Thanks everyone! Closing this out.

---
