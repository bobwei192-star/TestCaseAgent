# [Issue]: Failed to find DRM devices after restart

> **Issue #3352**
> **状态**: closed
> **创建时间**: 2024-06-23T07:39:06Z
> **更新时间**: 2024-07-24T17:46:30Z
> **关闭时间**: 2024-07-24T17:46:29Z
> **作者**: yuuahmad
> **标签**: AMD Radeon VII, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3352

## 标签

- **AMD Radeon VII** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

after i reboot my laptop, drm suddenly not detected. here my log
```sh
yuuahmad@yuuahmad-HP-Pavilion-Laptop-14-ec0xxx:~/Downloads$ neofetch
            .-/+oossssoo+/-.               yuuahmad@yuuahmad-HP-Pavilion-Laptop-14-ec0xxx 
        `:+ssssssssssssssssss+:`           ---------------------------------------------- 
      -+ssssssssssssssssssyyssss+-         OS: Ubuntu 22.04.4 LTS x86_64 
    .ossssssssssssssssssdMMMNysssso.       Host: HP Pavilion Laptop 14-ec0xxx 
   /ssssssssssshdmmNNmmyNMMMMhssssss/      Kernel: 6.5.0-41-generic 
  +ssssssssshmydMMMMMMMNddddyssssssss+     Uptime: 48 mins 
 /sssssssshNMMMyhhyyyyhmNMMMNhssssssss/    Packages: 1764 (dpkg), 9 (snap) 
.ssssssssdMMMNhsssssssssshNMMMdssssssss.   Shell: bash 5.1.16 
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   Resolution: 1920x1080 
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   DE: GNOME 42.9 
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   WM: Mutter 
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   WM Theme: Adwaita 
.ssssssssdMMMNhsssssssssshNMMMdssssssss.   Theme: Yaru [GTK2/3] 
 /sssssssshNMMMyhhyyyyhdNMMMNhssssssss/    Icons: Yaru [GTK2/3] 
  +sssssssssdmydMMMMMMMMddddyssssssss+     Terminal: gnome-terminal 
   /ssssssssssshdmNNNNmyNMMMMhssssss/      CPU: AMD Ryzen 5 5500U with Radeon Graphics (12) @ 4.056GHz 
    .ossssssssssssssssssdMMMNysssso.       GPU: AMD ATI 04:00.0 Lucienne 
      -+sssssssssssssssssyyyssss+-         Memory: 2604MiB / 15299MiB 
        `:+ssssssssssssssssss+:`
            .-/+oossssoo+/-.                                       
                                                                   
```
and here is my terminal logger that i save before i reboot my laptop (my process to install rocm)
iam using this tutorial [APU on Linux](https://agieverywhere.com/apuguide/AMDAPU/APU_Linux#amdlin) hoping that i can use tensorflow or torch using my apu in ryzen 5 5500u
[output-install-rocm.txt](https://github.com/user-attachments/files/15942923/output-install-rocm.txt)

why is it so difficult for amd to adapt to machine learning and artificial intelligence? not like nvidia with cuda or intel with oneapi and openvino

and why does AMD only support the newest hardware, really the "latest". even though Intel with Open Vino still supports their 6th generation processors

Please, AMD if you see this I hope you fix it immediately

### Operating System

jammy jellyfish

### CPU

ryzen 5 5500u apu

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

using amd ryzen 5 5500u apu 
follow this tutorial, but change version to 6.1.3 [APU on Linux](https://agieverywhere.com/apuguide/AMDAPU/APU_Linux#amdlin)

reboot laptop
here my ss about my laptop
![Screenshot from 2024-06-23 14-37-27](https://github.com/ROCm/ROCm/assets/22028802/ecd39a5b-5104-4b46-8fba-7552918ce885)


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```sh
yuuahmad@yuuahmad-HP-Pavilion-Laptop-14-ec0xxx:~$ /opt/rocm/bin/rocminfo --support
ROCk module is NOT loaded, possibly no GPU devices

```

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-06-24T18:52:58Z)

Hi @yuuahmad, other users have had success running ROCm on their APUs following the steps outlined in the threads below. Could you please give these a try?

https://github.com/ROCm/ROCm/issues/2216
https://github.com/ROCm/ROCm/issues/2014

---

### 评论 #2 — harkgill-amd (2024-07-08T15:15:54Z)

Hi @yuuahmad, were you able to give the suggestions in the above threads a try?

---

### 评论 #3 — harkgill-amd (2024-07-24T17:46:30Z)

Closing this issue. If you have any further issues, please open a new ticket. Thanks!

---
