# [Issue]:  rocminfo error:./sources/wsl/libhsakmt/src/thunk_proxy/thunk_proxy.cpp:111: void thunk_proxy::QueryAdapterInfo(D3DKMT_HANDLE, ATIADAPTERINFO*): Assertion `ret == STATUS_SUCCESS' failed

> **Issue #4460**
> **状态**: closed
> **创建时间**: 2025-03-07T11:31:06Z
> **更新时间**: 2025-05-21T02:49:21Z
> **关闭时间**: 2025-03-19T19:44:52Z
> **作者**: herokillerJ
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/4460

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

1. Follow the instructions at https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html to install.
2. execute "rocminfo"
3. print:
WSL environment detected.
rocminfo: ./sources/wsl/libhsakmt/src/thunk_proxy/thunk_proxy.cpp:111: void thunk_proxy::QueryAdapterInfo(D3DKMT_HANDLE, ATIADAPTERINFO*): Assertion `ret == STATUS_SUCCESS' failed.
Aborted (core dumped)



### Operating System

WSL-Ubuntu24.04

### CPU

AMD 5900x

### GPU

AMD 7900XTX

### ROCm Version

ROCm 6.3.4

### ROCm Component

_No response_

### Steps to Reproduce

1. Follow the instructions at https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html to install.
2. execute "rocminfo"
3. print:
```
WSL environment detected.
rocminfo: ./sources/wsl/libhsakmt/src/thunk_proxy/thunk_proxy.cpp:111: void thunk_proxy::QueryAdapterInfo(D3DKMT_HANDLE, ATIADAPTERINFO*): Assertion `ret == STATUS_SUCCESS' failed.
Aborted (core dumped)
```
![Image](https://github.com/user-attachments/assets/80576668-af84-4efe-a8a9-f8de147bbf43)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

still print:
```
WSL environment detected.
rocminfo: ./sources/wsl/libhsakmt/src/thunk_proxy/thunk_proxy.cpp:111: void thunk_proxy::QueryAdapterInfo(D3DKMT_HANDLE, ATIADAPTERINFO*): Assertion `ret == STATUS_SUCCESS' failed.
Aborted (core dumped)
```

### Additional Information

AMD GPU driver version: 25.3.1
WSL version： 2.4.11.0
kernel version： 5.15.167.4-1
WSLg version： 1.0.65
MSRDC version： 1.2.5716
Direct3D version： 1.611.1-81528511
DXCore version： 10.0.26100.1-240331-1435.ge-release
Windows version： 10.0.26100.3323

![Image](https://github.com/user-attachments/assets/8d56b925-6ca2-4dfe-81f4-c4cf36334c21)

---

## 评论 (27 条)

### 评论 #1 — ppanchad-amd (2025-03-07T14:34:03Z)

Hi @herokillerJ. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — imkow (2025-03-07T18:52:28Z)

I encountered the very same error. damn.

---

### 评论 #3 — CellerX (2025-03-08T12:26:31Z)

same error with 7900xt

---

### 评论 #4 — tcgu-amd (2025-03-11T14:51:34Z)

Hi @herokillerJ thanks for reaching out! Would you be able to run rocminfo with `HSAKMT_DEBUG_INFO=7` and show the logs? Thanks! 

---

### 评论 #5 — herokillerJ (2025-03-11T15:42:12Z)

> Hi [@herokillerJ](https://github.com/herokillerJ) thanks for reaching out! Would you be able to run rocminfo with `HSAKMT_DEBUG_INFO=7` and show the logs? Thanks!

![Image](https://github.com/user-attachments/assets/dd318adb-2a48-4327-902e-127f2369e119)

```
WSL environment detected.
rocminfo: ./sources/wsl/libhsakmt/src/thunk_proxy/thunk_proxy.cpp:111: void thunk_proxy::QueryAdapterInfo(D3DKMT_HANDLE, ATIADAPTERINFO*): Assertion `ret == STATUS_SUCCESS' failed.
Aborted (core dumped)
```

---

### 评论 #6 — tcgu-amd (2025-03-11T15:48:36Z)

@herokillerJ Thanks for the quick repsonse! How about `HSAKMT_DEBUG_LEVEL=7`?

---

### 评论 #7 — herokillerJ (2025-03-11T16:08:03Z)

> [@herokillerJ](https://github.com/herokillerJ) Thanks for the quick repsonse! How about `HSAKMT_DEBUG_LEVEL=7`?

![Image](https://github.com/user-attachments/assets/860744aa-8b4f-44dc-adda-7db80abb57c8)

---

### 评论 #8 — tcgu-amd (2025-03-11T18:02:15Z)

Hmm that's strange...thanks for the information, will look into it further!

---

### 评论 #9 — ff2009 (2025-03-11T18:58:06Z)

I have the exact same problem and I tried on Ubuntu 22.04 and 24.04.

---

### 评论 #10 — tcgu-amd (2025-03-17T14:45:06Z)

Hi @herokillerJ, sorry, I cannot seem to reproduce this issue on our dev systems.. Just to rule out potential issues with the underlying drivers and hardware, are you able to run rocminfo with HIP SDK?

---

### 评论 #11 — herokillerJ (2025-03-17T15:53:56Z)

> Hi [@herokillerJ](https://github.com/herokillerJ), sorry, I cannot seem to reproduce this issue on our dev systems.. Just to rule out potential issues with the underlying drivers and hardware, are you able to run rocminfo with HIP SDK?

I have already installed version 25.3.1 of the driver, do I still need to install the pro version of the driver?

![Image](https://github.com/user-attachments/assets/92df0c90-2bca-4d39-b753-57abf20f0fb1)

---

### 评论 #12 — tcgu-amd (2025-03-17T20:21:20Z)

Hi @herokillerJ, I don't think installing the pro driver is necessary. Here is a guide for installing HIP SDK on windows https://rocm.docs.amd.com/projects/install-on-windows/en/develop/. 

Alternatively, would you be able to verify if ROCm 6.2.3 works with WSL2? 

Thanks!

---

### 评论 #13 — ff2009 (2025-03-17T21:05:23Z)

> Hi [@herokillerJ](https://github.com/herokillerJ), I don't think installing the pro driver is necessary. Here is a guide for installing HIP SDK on windows https://rocm.docs.amd.com/projects/install-on-windows/en/develop/.
> 
> Alternatively, would you be able to verify if ROCm 6.2.3 works with WSL2?
> 
> Thanks!

I have installed a new instance of Ubuntu 22.04 LTS under WSL2 and installed ROCm 6.2.3 as suggested and ROCM was working.

![Image](https://github.com/user-attachments/assets/8a693a3a-267c-4373-ba3e-68df8adb7135)

Then I tried to update to ROCm 6.3.4 and rocm stopped working.

![Image](https://github.com/user-attachments/assets/09305f8d-2101-44e4-9dad-e9bbc936e2bc)

I have installed the HIP SDK for windows before doing this.

---

### 评论 #14 — tcgu-amd (2025-03-18T14:39:43Z)

@ff2009 Thanks for the update! Seems like the issue is strictly with 6.3.4 then. This should help us narrow down the search. Thanks again!

---

### 评论 #15 — tcgu-amd (2025-03-18T17:28:40Z)

 @ff2009 @herokillerJ Sorry for the redundancy, but would you be able to upload the exact commands you used to install ROCm 6.3.4? Thanks!

---

### 评论 #16 — tcgu-amd (2025-03-18T17:31:02Z)

Hi @herokillerJ, additional question, do you have an Nvidia card set up as well on your machine?

![Image](https://github.com/user-attachments/assets/174a2779-6401-43d2-b894-0d409365cf1b)

Edit @ff2009, @CellerX, @imkow, do you also have a different GPU setup as well? 

---

### 评论 #17 — imkow (2025-03-18T17:52:04Z)

@tcgu-amd yes, I got another GPU from NV in the same system.

---

### 评论 #18 — herokillerJ (2025-03-18T18:23:54Z)

> Hi [@herokillerJ](https://github.com/herokillerJ), additional question, do you have an Nvidia card set up as well on your machine?
> 
> ![Image](https://github.com/user-attachments/assets/174a2779-6401-43d2-b894-0d409365cf1b)
> 
> Edit [@ff2009](https://github.com/ff2009), [@CellerX](https://github.com/CellerX), [@imkow](https://github.com/imkow), do you also have a different GPU setup as well?

yes, I got another GPU from NV in the same system.

---

### 评论 #19 — ff2009 (2025-03-18T18:58:25Z)

> Sorry for the redundancy, but would you be able to upload the exact commands you used to install ROCm 6.3.4? Thanks!

After installing the ROCM 6.2.3 and checking that was working, I used the following commands:

`sudo apt update`
`wget https://repo.radeon.com/amdgpu-install/6.3.4/ubuntu/jammy/amdgpu-install_6.3.60304-1_all.deb`
`sudo apt install ./amdgpu-install_6.3.60304-1_all.deb`

`amdgpu-install -y --usecase=wsl,rocm --no-dkms`

`rocminfo`

> Edit @ff2009, additional question, do you have an Nvidia card set up as well on your machine?

Yes. I have a second Nvidia card on my system as well. 

![Image](https://github.com/user-attachments/assets/ca67524b-5df0-435d-a6f2-4e375c2e421d)



---

### 评论 #20 — ff2009 (2025-03-18T19:06:41Z)

Just a quick update. I tried to disable my NVIDIA GPU in Device Manager, and `rocminfo` worked again.

Device Manager
![Image](https://github.com/user-attachments/assets/d84a93e5-b799-40e8-a6ea-7cc900c5aa5a)

rocminfo output.
![Image](https://github.com/user-attachments/assets/969556fc-aeb4-465b-ab8b-f17864f9c218)

---

### 评论 #21 — imkow (2025-03-18T19:19:51Z)

> Just a quick update. I tried to disable my NVIDIA GPU in Device Manager, and `rocminfo` worked again.
> 
> Device Manager
> ![Image](https://github.com/user-attachments/assets/d84a93e5-b799-40e8-a6ea-7cc900c5aa5a)
> 
> rocminfo output.
> ![Image](https://github.com/user-attachments/assets/969556fc-aeb4-465b-ab8b-f17864f9c218)

same here. Hope they fix soon.

---

### 评论 #22 — tcgu-amd (2025-03-18T20:58:58Z)

@imkow @ff2009 @CellerX @herokillerJ Thanks for verifying! To help us identify if this is a ROCm issue or a windows driver issue, would you mind downgrading driver version to 24.12.1 to see if anything changes? No need to change the WSL/ROCm version. Thanks! 

---

### 评论 #23 — ff2009 (2025-03-18T22:00:46Z)

I have downgraded my driver to version 24.12.1, but didn't do a clean install, just rebooted my system.
After doing this the issue still persist. Disabling the Nvidia GPU in device manager has the same behavior as before. 


---

### 评论 #24 — CellerX (2025-03-19T03:57:10Z)





> [@imkow](https://github.com/imkow) [@ff2009](https://github.com/ff2009) [@CellerX](https://github.com/CellerX) [@herokillerJ](https://github.com/herokillerJ) Thanks for verifying! To help us identify if this is a ROCm issue or a windows driver issue, would you mind downgrading driver version to 24.12.1 to see if anything changes? No need to change the WSL/ROCm version. Thanks!

Maybe it's caused by multiple GPUs. I have 7900xt and 6800. I will remove 6800 and try again later.

I removed 6800 and it still shows the same error，but removed all irrelevant GPUs，finally worked
![Image](https://github.com/user-attachments/assets/15c58b7e-4d44-4bcd-a6da-bdc46c7dc6ec)

---

### 评论 #25 — tcgu-amd (2025-03-19T19:44:52Z)

@imkow @ff2009 @CellerX @herokillerJ. Thank you for your patience! We have identified the root cause. A patch will be released with the next ROCm for WSL release. For now, please disable other unsupported GPUs on the system as a temporary workaround. Thanks!

---

### 评论 #26 — AI-Unicorn-D (2025-05-01T15:35:49Z)

> 。感谢您的耐心等待！我们已经确定了根本原因。补丁将随下一个 ROCm for WSL 版本一起发布。目前，请禁用系统上其他不受支持的 GPU 作为临时解决方法。谢谢！

My card also meet the same problem, I use my w7900, cpu 7950x3d, also has another n card 4070tis, when I try to use wsl2 ubuntu 24.04 to install rocm for my w7900 still meet this problem. My host driver is  adrenalin 25.3.1 @ 

---

### 评论 #27 — datGryphon (2025-05-21T02:49:20Z)

I am also experiencing this issue with Windows 11, host driver 25.3.1 w/ factory reset install, and wsl ROCM 6.4.3. If there are any other display adapters enabled in the device manager, `rocminfo` fails accordingly. 

---
