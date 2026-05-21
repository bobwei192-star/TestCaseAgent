# [Issue]: rocm 6.1 install warning "/opt/rocm-6.1.0//hipfc not found"

> **Issue #3035**
> **状态**: closed
> **创建时间**: 2024-04-17T19:29:14Z
> **更新时间**: 2024-12-11T02:31:59Z
> **关闭时间**: 2024-12-11T02:31:58Z
> **作者**: ye-luo
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon VII
> **URL**: https://github.com/ROCm/ROCm/issues/3035

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)

## 描述

### Problem Description

```
$ sudo apt install rocm-hip-sdk6.1.0 rocm-openmp-sdk6.1.0
...
Setting up hipblas-dev6.1.0 (2.1.0.60100-82~20.04) ...
Setting up hipsparse6.1.0 (3.0.1.60100-82~20.04) ...
Setting up hipsparse-dev6.1.0 (3.0.1.60100-82~20.04) ...
Setting up rocalution6.1.0 (3.1.1.60100-82~20.04) ...
Setting up rccl-dev6.1.0 (2.18.6.60100-82~20.04) ...
Setting up hipsolver6.1.0 (2.1.0.60100-82~20.04) ...
Setting up hipblaslt6.1.0 (0.7.0.60100-82~20.04) ...
Setting up hipsparselt6.1.0 (0.1.0.60100-82~20.04) ...
Setting up rocalution-dev6.1.0 (3.1.1.60100-82~20.04) ...
Setting up hipsolver-dev6.1.0 (2.1.0.60100-82~20.04) ...
Setting up rocm-hip-libraries6.1.0 (6.1.0.60100-82~20.04) ...
Setting up hipsparselt-dev6.1.0 (0.1.0.60100-82~20.04) ...
Setting up hipblaslt-dev6.1.0 (0.7.0.60100-82~20.04) ...
Setting up rocm-hip-sdk6.1.0 (6.1.0.60100-82~20.04) ...
/opt/rocm-6.1.0//hipfc not found, but that is OK
```
Noticed the last line warning about `/opt/rocm-6.1.0//hipfc`. It is actually at `/opt/rocm-6.1.0/bin/hipfc`

### Operating System

ubuntu 20.04.6 LTS

### CPU

AMD EPYC 7282 16-Core Processor

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — nartmada (2024-04-17T20:35:09Z)

Thanks @ye-luo.  I will ask someone to take a look.

---

### 评论 #2 — Vexi23 (2024-04-18T17:59:27Z)

I don't make new issue, so i gonna post it here i had problem with updating rocm from 6.0.2 to 6.1 related to llvm #3032 i tried fix it but nothing helped so i did ubuntu re-install this time i had no issues with install rocm 6.1 but i had warning not just hipfc but also runvx

> Konfigurowanie pakietu hipsparse (3.0.1.60100-82~22.04) ...
Konfigurowanie pakietu rocsolver (3.25.0.60100-82~22.04) ...
Konfigurowanie pakietu miopen-hip-dev (3.1.0.60100-82~22.04) ...
Konfigurowanie pakietu mivisionx (2.5.0.60100-82~22.04) ...
Konfigurowanie pakietu hipblas (2.1.0.60100-82~22.04) ...
Konfigurowanie pakietu rccl-dev (2.18.6.60100-82~22.04) ...
Konfigurowanie pakietu rocblas-dev (4.1.0.60100-82~22.04) ...
Konfigurowanie pakietu rocsparse-dev (3.1.2.60100-82~22.04) ...
Konfigurowanie pakietu hipsparse-dev (3.0.1.60100-82~22.04) ...
Konfigurowanie pakietu hipblas-dev (2.1.0.60100-82~22.04) ...
Konfigurowanie pakietu rocsolver-dev (3.25.0.60100-82~22.04) ...
Konfigurowanie pakietu rocalution (3.1.1.60100-82~22.04) ...
Konfigurowanie pakietu migraphx-dev (2.9.0.60100-82~22.04) ...
Konfigurowanie pakietu hipsolver (2.1.0.60100-82~22.04) ...
Konfigurowanie pakietu hipsolver-dev (2.1.0.60100-82~22.04) ...
Konfigurowanie pakietu hipsparselt (0.1.0.60100-82~22.04) ...
Konfigurowanie pakietu hipblaslt (0.7.0.60100-82~22.04) ...
Konfigurowanie pakietu rocm-hip-libraries (6.1.0.60100-82~22.04) ...
Konfigurowanie pakietu hipblaslt-dev (0.7.0.60100-82~22.04) ...
Konfigurowanie pakietu rocalution-dev (3.1.1.60100-82~22.04) ...
Konfigurowanie pakietu hipsparselt-dev (0.1.0.60100-82~22.04) ...
Konfigurowanie pakietu rocm-ml-libraries (6.1.0.60100-82~22.04) ...
Konfigurowanie pakietu rocm-hip-sdk (6.1.0.60100-82~22.04) ...
/opt/rocm-6.1.0//hipfc not found, but that is OK 
Konfigurowanie pakietu rocm-ml-sdk (6.1.0.60100-82~22.04) ...
Przetwarzanie wyzwalaczy pakietu libc-bin (2.35-0ubuntu3.7)...
Przetwarzanie wyzwalaczy pakietu man-db (2.10.2-1)...
Przetwarzanie wyzwalaczy pakietu sgml-base (1.30)...
Konfigurowanie pakietu x11proto-dev (2021.5-1) ...
Konfigurowanie pakietu libxau-dev:amd64 (1:1.0.9-1build5) ...
Konfigurowanie pakietu libxdmcp-dev:amd64 (1:1.1.3-0ubuntu5) ...
Konfigurowanie pakietu libxcb1-dev:amd64 (1.14-3ubuntu3) ...
Konfigurowanie pakietu libx11-dev:amd64 (2:1.7.5-1ubuntu0.3) ...
Konfigurowanie pakietu libglx-dev:amd64 (1.4.0-1) ...
Konfigurowanie pakietu libgl-dev:amd64 (1.4.0-1) ...
Konfigurowanie pakietu mesa-common-dev:amd64 (23.2.1-1ubuntu3.1~22.04.2) ...
Konfigurowanie pakietu rocm-opencl-dev (2.0.0.60100-82~22.04) ...
Konfigurowanie pakietu rocm-opencl-sdk (6.1.0.60100-82~22.04) ...
Konfigurowanie pakietu rocm (6.1.0.60100-82~22.04) ...
/opt/rocm-6.1.0//runvx not found, but that is OK 



Full version of log on pastebin
[https://pastebin.com/UN1bt8Hv](url)


---

### 评论 #3 — cgmb (2024-07-10T21:55:35Z)

This appears to be a bug in the rocm-hip-sdk `postinst` script. This can be seen with

```bash
wget https://repo.radeon.com/rocm/apt/6.1.2/pool/main/r/rocm-hip-sdk6.1.2/rocm-hip-sdk6.1.2_6.1.2.60102-119~20.04_amd64.deb
ar x rocm-hip-sdk6.1.2_6.1.2.60102-119~20.04_amd64.deb
tar xaf control.tar.xz
cat postinst
```
which includes this snippet:
```bash
    binaries=(
        hipfc
    )

    for i in "${binaries[@]}"
    do
        # No obvious recover strategy if things fail
        # No manual or other slave pages to install
        if [ -e /opt/rocm-6.1.2//"$i" ]
        then
            update-alternatives --install /usr/bin/"$i" "$i" \
                                /opt/rocm-6.1.2//"$i" "$altscore"
        else
            echo "/opt/rocm-6.1.2//$i not found, but that is OK" >&2
        fi
    done
    true
```

---

### 评论 #4 — harkgill-amd (2024-10-01T18:34:02Z)

@ye-luo, a fix has been implemented for this issue and will be available in an upcoming ROCm release. Will keep this open for now and circle back once the fix is live to confirm the issue has been resolved.

---

### 评论 #5 — harkgill-amd (2024-12-10T18:23:04Z)

Hi @ye-luo, this has been fixed in ROCm 6.3.0 as `hipfc` is correctly found at `/opt/rocm-6.3.0/bin/hipfc`. Could you please give the installation a try on your end.

---

### 评论 #6 — ye-luo (2024-12-11T02:31:58Z)

Looks good in 6.3.0

---
