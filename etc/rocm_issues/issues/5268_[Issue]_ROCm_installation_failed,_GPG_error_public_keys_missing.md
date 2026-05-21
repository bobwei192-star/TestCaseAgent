# [Issue]: ROCm installation failed, GPG error: public keys missing

> **Issue #5268**
> **状态**: closed
> **创建时间**: 2025-09-07T08:00:55Z
> **更新时间**: 2025-09-24T19:59:01Z
> **关闭时间**: 2025-09-23T18:33:53Z
> **作者**: Arthur790916
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5268

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Get:5 https://repo.radeon.com/amdgpu/6.4.2/ubuntu noble InRelease [5,465 B]    
Hit:6 https://repo.radeon.com/amdgpu/6.4.2.1/ubuntu noble InRelease            
Err:5 https://repo.radeon.com/amdgpu/6.4.2/ubuntu noble InRelease              
  The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 9386B48A1A693C5C
Hit:7 https://repo.radeon.com/rocm/apt/6.4.2 noble InRelease                   
Hit:8 http://security.ubuntu.com/ubuntu noble-security InRelease
Reading package lists... Done
W: GPG error: https://repo.radeon.com/amdgpu/6.4.2/ubuntu noble InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 9386B48A1A693C5C
E: The repository 'https://repo.radeon.com/amdgpu/6.4.2/ubuntu noble InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.

### Operating System

Ubuntu 24.04.3

### CPU

Ryzen 7 7700

### GPU

RX 9070 XT

### ROCm Version

ROCm 6.4.2

### ROCm Component

_No response_

### Steps to Reproduce

wget https://repo.radeon.com/amdgpu-install/6.4.2.1/ubuntu/noble/amdgpu-install_6.4.60402-1_all.deb
sudo apt install ./amdgpu-install_6.4.60402-1_all.deb
amdgpu-install -y --usecase=graphics,rocm

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

New to Linux and wants to install ROCm for local LLMS.

---

## 评论 (13 条)

### 评论 #1 — ppanchad-amd (2025-09-08T14:00:13Z)

Hi @Arthur790916. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — harkgill-amd (2025-09-09T19:10:04Z)

Hi @Arthur790916, the GPG error is odd as downloading + adding the package signing key should be handled by the installer. I wasn't able to repro it on my end either - it may just be an intermittent failure.

Could you try running the following to manually add the missing public key to your system,

```
wget https://repo.radeon.com/rocm/rocm.gpg.key -O - | \
    gpg --dearmor | sudo tee /etc/apt/keyrings/rocm.gpg > /dev/null
sudo apt update
```
If the error still persists, I'd recommend a fresh install of the 6.4.2 release. You can do this by first removing all ROCm installations on your system with, 
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```
Then, reinstall ROCm 6.4.2 with, 
```
wget https://repo.radeon.com/amdgpu-install/6.4.2/ubuntu/noble/amdgpu-install_6.4.60402-1_all.deb
sudo apt install ./amdgpu-install_6.4.60402-1_all.deb
sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
sudo apt install rocm amdgpu-dkms
```

---

### 评论 #3 — isapir (2025-09-17T06:36:53Z)

I am getting the same error trying to install 6.4.2.1 for the first time, and this is what I get now for `sudo apt update` after adding the `rocm.gpg` as described above:

```
sudo apt update
Get:1 https://repo.radeon.com/amdgpu/6.4.2/ubuntu noble InRelease [5,465 B]
Hit:2 https://repo.radeon.com/amdgpu/6.4.2.1/ubuntu noble InRelease                                                                                        
Hit:3 https://download.docker.com/linux/ubuntu noble InRelease                                                                                             
Hit:4 https://repo.radeon.com/rocm/apt/6.4.2 noble InRelease                                                                                               
Hit:5 https://packages.microsoft.com/repos/code stable InRelease                                                                                           
Hit:6 http://archive.ubuntu.com/ubuntu noble InRelease                                                                   
Hit:7 https://dl.google.com/linux/chrome/deb stable InRelease                                      
Hit:8 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:9 http://security.ubuntu.com/ubuntu noble-security InRelease
Hit:10 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Err:1 https://repo.radeon.com/amdgpu/6.4.2/ubuntu noble InRelease
  The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 9386B48A1A693C5C
Reading package lists... Done
W: GPG error: https://repo.radeon.com/amdgpu/6.4.2/ubuntu noble InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 9386B48A1A693C5C
E: The repository 'https://repo.radeon.com/amdgpu/6.4.2/ubuntu noble InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
```

---

### 评论 #4 — ykeyani (2025-09-17T10:47:56Z)

exporting the key seemed to resolve it for me:

```
sudo gpg --keyserver keyserver.ubuntu.com --recv-keys 9386B48A1A693C5C
sudo gpg --export --armor 9386B48A1A693C5C | sudo tee /etc/apt/trusted.gpg.d/amdgpu.asc
```

---

### 评论 #5 — isapir (2025-09-17T16:09:22Z)

Thanks @ykeyani - I ran the commands you posted and now I don't get the error anymore so I will proceed with trying to install ROCm

For future reference, and for anyone who is interested - the output of the commands is posted below:

```
$ sudo gpg --keyserver keyserver.ubuntu.com --recv-keys 9386B48A1A693C5C
```
>```
>gpg: directory '/root/.gnupg' created
>gpg: keybox '/root/.gnupg/pubring.kbx' created
>gpg: /root/.gnupg/trustdb.gpg: trustdb created
>gpg: key 9386B48A1A693C5C: public key "AMD MLSE DevOps <dl.MLSE.DevOps@amd.com>" imported
>gpg: Total number processed: 1
>gpg:               imported: 1
>```

```
$ sudo gpg --export --armor 9386B48A1A693C5C | sudo tee /etc/apt/trusted.gpg.d/amdgpu.asc
```
>```
>-----BEGIN PGP PUBLIC KEY BLOCK-----
>
>mQINBFefsSABEADmVqQyRi5bcUs/eG8mnKLdY+V+xuKuHLuujlXinSaMFRO640Md
>C2HNYLSd58Z8cB1rKfiN639CZp+SkDWq60cFXDCcX9djT0JmBzsTD/gwoMr16tMY
>...
>wQsw/xBJaxAHQn5lN/8t0eLt+U653ooEEr0ota5TfPumStSQ1UjP8pPny4l+JQ==
>=qMx4
>-----END PGP PUBLIC KEY BLOCK-----
>```


---

### 评论 #6 — stephenlauck (2025-09-20T05:02:21Z)

I got this error too on fresh Ubuntu 24.04.3 install. @isapir comment fixes it.

---

### 评论 #7 — harkgill-amd (2025-09-23T18:17:29Z)

@stephenlauck  and @isapir, could you share the contents of your `/etc/apt/sources.list.d/amdgpu.list` file? The 6.4.2.1 `amdgpu-install` should only be pulling in the 6.4.2.1 amdgpu and 6.4.2 rocm repositories not the 6.4.2 amdgpu repo - this is what I'm seeing on my end and what is set in the package configuration.

If both 6.4.2.1 and 6.4.2 amdgpu repos are configured in `amdgpu.list`, could you try uninstalling and reinstalling with 
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove

sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.4.2.1/ubuntu/noble/amdgpu-install_6.4.60402-1_all.deb
sudo apt install ./amdgpu-install_6.4.60402-1_all.deb
```
Then check the contents of `amdgpu.list` again. I'd want to see if `https://repo.radeon.com/amdgpu/6.4.2/ubuntu` is still being added  as a repository on your end.

---

### 评论 #8 — isapir (2025-09-23T18:22:03Z)

@harkgill-amd below is the output of `cat /etc/apt/sources.list.d/amdgpu.list`, but keep in mind that I used @ykeyani 's commands to generate that: 
>```
>deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/6.4.2.1/ubuntu noble main
>#deb-src [signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/6.4.2.1/ubuntu noble main
>```

I will uninstall and reinstall and post the output shortly

---

### 评论 #9 — isapir (2025-09-23T18:26:55Z)

@harkgill-amd After an uninstall (and confirming that `/etc/apt/sources.list.d/amdgpu.list` no long exists), followed by install per the instructions above, `cat /etc/apt/sources.list.d/amdgpu.list` shows:
>```
>deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/6.4.2.1/ubuntu noble main
>#deb-src [signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/6.4.2.1/ubuntu noble main
>```

---

### 评论 #10 — isapir (2025-09-23T18:28:21Z)

But I still think that "the fix" was adding `/etc/apt/trusted.gpg.d/amdgpu.asc` as proposed by @ykeyani 

---

### 评论 #11 — harkgill-amd (2025-09-23T18:33:53Z)

Yup, exporting the key was definitely the fix for the GPG errors - thanks for that @ykeyani!

In parallel, the 6.4.2.1 installer shouldn't have been configuring the 6.4.2 amdgpu repo which from your testing looks to be resolved. I'm going to tentatively close this one out as it's not reproduceable but if someone does come across more of these errors, feel free to leave a comment and I'll re-open this issue.

---

### 评论 #12 — harkgill-amd (2025-09-23T18:34:27Z)

Also thanks for the help testing @isapir :)

---

### 评论 #13 — stephenlauck (2025-09-24T19:59:01Z)

@harkgill-amd Sorry for the late response but on a fresh build of the OS today on the same hardware I have this:

```
spellcaster@vengeance:~$ cat /etc/apt/sources.list.d/amdgpu.list 
deb [arch=amd64,i386 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.10.1/ubuntu noble main
#deb-src [signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/amdgpu/30.10.1/ubuntu noble main
```

It also looks like I got an updated deb `amdgpu-install_7.0.1.70001-1_all.deb` and no GPG errors.

Looking good, thanks @harkgill-amd !


---
