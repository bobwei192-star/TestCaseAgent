# AMD ROCm Windows Installation Error 215

> **Issue #2363**
> **状态**: closed
> **创建时间**: 2023-08-03T15:48:21Z
> **更新时间**: 2026-02-20T15:58:19Z
> **关闭时间**: 2023-08-03T23:16:02Z
> **作者**: TheBurntWaffl3
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2363

## 描述

Near the end of the installation process for AMD HIP SDK Installer, the installation stops with general error 215. The computer has 6800xt with 5600 CPU, windows 10 x64 22H2. Would appreciate any help with this!




---

## 评论 (21 条)

### 评论 #1 — saadrahim (2023-08-03T15:50:57Z)

Can you upload a screenshot?

Can you check if you have any files in C:\Program Files\AMD\ROCm?

---

### 评论 #2 — TheBurntWaffl3 (2023-08-03T16:13:18Z)

![Screenshot (193)](https://github.com/RadeonOpenCompute/ROCm/assets/141348950/12bc73ef-3d61-4e03-8633-2cbd3ffb9d8e)
![Screenshot (192)](https://github.com/RadeonOpenCompute/ROCm/assets/141348950/dcb683c1-6342-4524-9ea4-49da2b698d3d)
it seems I dont currently have an ROCm file in the AMD folder. Is this an issue?

---

### 评论 #3 — briansp2020 (2023-08-03T17:39:23Z)

Did you try removing all the previous driver files using AMD Cleanup Utility (https://www.amd.com/en/support/kb/faq/gpu-601) or DDU (https://www.guru3d.com/files-details/display-driver-uninstaller-download.html)
I think it's worth a try

---

### 评论 #4 — saadrahim (2023-08-03T17:42:10Z)

Please try the installation again and ensure to select the installation directory. Our install team suspects that may be the cause of the error. 

Can you provide logs from C:\Program Files\AMD\CIM\Log\? The Visual Studio plugin has logs at %temp% directory with the naming scheme of dd_setup_*.log and dd_VSIXInstaller_*.log

---

### 评论 #5 — TheBurntWaffl3 (2023-08-03T19:59:47Z)

I attempted the AMD Cleanup Utility to no avail. Here are the logs from C:\Program Files\AMD\CIM\Log: 
[Install AMD Radeon USB LED Application 2023_08_03_15.47.33.log](https://github.com/RadeonOpenCompute/ROCm/files/12254592/Install.AMD.Radeon.USB.LED.Application.2023_08_03_15.47.33.log)
[Install AMD Settings 2023_08_03_15.47.03.log](https://github.com/RadeonOpenCompute/ROCm/files/12254593/Install.AMD.Settings.2023_08_03_15.47.03.log)
[Install AMD WVR64 2023_08_03_15.47.10.log](https://github.com/RadeonOpenCompute/ROCm/files/12254594/Install.AMD.WVR64.2023_08_03_15.47.10.log)
[Install CCC Slim 2023_08_03_15.47.02.log](https://github.com/RadeonOpenCompute/ROCm/files/12254595/Install.CCC.Slim.2023_08_03_15.47.02.log)
[Install HIP SDK Core 2023_08_03_15.47.11.log](https://github.com/RadeonOpenCompute/ROCm/files/12254596/Install.HIP.SDK.Core.2023_08_03_15.47.11.log)
[Install HIP SDK Libraries Development 2023_08_03_15.47.23.log](https://github.com/RadeonOpenCompute/ROCm/files/12254597/Install.HIP.SDK.Libraries.Development.2023_08_03_15.47.23.log)
[Install HIP SDK Libraries Runtime 2023_08_03_15.47.26.log](https://github.com/RadeonOpenCompute/ROCm/files/12254598/Install.HIP.SDK.Libraries.Runtime.2023_08_03_15.47.26.log)
[Install HIP SDK Ray Tracing Development 2023_08_03_15.47.32.log](https://github.com/RadeonOpenCompute/ROCm/files/12254599/Install.HIP.SDK.Ray.Tracing.Development.2023_08_03_15.47.32.log)
[Install HIP SDK Ray Tracing Runtime 2023_08_03_15.47.32.log](https://github.com/RadeonOpenCompute/ROCm/files/12254600/Install.HIP.SDK.Ray.Tracing.Runtime.2023_08_03_15.47.32.log)
[Install HIP SDK Runtime Compiler Development 2023_08_03_15.47.32.log](https://github.com/RadeonOpenCompute/ROCm/files/12254601/Install.HIP.SDK.Runtime.Compiler.Development.2023_08_03_15.47.32.log)
[Install HIP SDK Runtime Compiler Runtime 2023_08_03_15.47.11.log](https://github.com/RadeonOpenCompute/ROCm/files/12254602/Install.HIP.SDK.Runtime.Compiler.Runtime.2023_08_03_15.47.11.log)
[Install HIP SDK Visual Studio 2017 Plugin 2023_08_03_15.47.15.log](https://github.com/RadeonOpenCompute/ROCm/files/12254603/Install.HIP.SDK.Visual.Studio.2017.Plugin.2023_08_03_15.47.15.log)
[Install.log](https://github.com/RadeonOpenCompute/ROCm/files/12254604/Install.log)
[Install.log_2023-8-3_15_51_44.log](https://github.com/RadeonOpenCompute/ROCm/files/12254605/Install.log_2023-8-3_15_51_44.log)
[SetupCD.txt](https://github.com/RadeonOpenCompute/ROCm/files/12254606/SetupCD.txt)
[Uninstall AMD User Experience Program Installer 2310.23.02.720 2023_08_03_15.46.25.log](https://github.com/RadeonOpenCompute/ROCm/files/12254607/Uninstall.AMD.User.Experience.Program.Installer.2310.23.02.720.2023_08_03_15.46.25.log)
[Uninstall HIP SDK Core 5.5.0 2023_08_03_15.46.31.log](https://github.com/RadeonOpenCompute/ROCm/files/12254608/Uninstall.HIP.SDK.Core.5.5.0.2023_08_03_15.46.31.log)
[Uninstall HIP SDK Libraries Development 5.5.0 2023_08_03_15.46.27.log](https://github.com/RadeonOpenCompute/ROCm/files/12254609/Uninstall.HIP.SDK.Libraries.Development.5.5.0.2023_08_03_15.46.27.log)
[Uninstall HIP SDK Libraries Runtime 5.5.0 2023_08_03_15.46.25.log](https://github.com/RadeonOpenCompute/ROCm/files/12254610/Uninstall.HIP.SDK.Libraries.Runtime.5.5.0.2023_08_03_15.46.25.log)
[Uninstall HIP SDK Ray Tracing Development 5.5.0 2023_08_03_15.46.25.log](https://github.com/RadeonOpenCompute/ROCm/files/12254611/Uninstall.HIP.SDK.Ray.Tracing.Development.5.5.0.2023_08_03_15.46.25.log)
[Uninstall HIP SDK Ray Tracing Runtime 5.5.0 2023_08_03_15.46.25.log](https://github.com/RadeonOpenCompute/ROCm/files/12254612/Uninstall.HIP.SDK.Ray.Tracing.Runtime.5.5.0.2023_08_03_15.46.25.log)
[Uninstall HIP SDK Runtime Compiler Development 5.5.0 2023_08_03_15.46.25.log](https://github.com/RadeonOpenCompute/ROCm/files/12254613/Uninstall.HIP.SDK.Runtime.Compiler.Development.5.5.0.2023_08_03_15.46.25.log)
[Uninstall HIP SDK Runtime Compiler Runtime 5.5.0 2023_08_03_15.46.33.log](https://github.com/RadeonOpenCompute/ROCm/files/12254614/Uninstall.HIP.SDK.Runtime.Compiler.Runtime.5.5.0.2023_08_03_15.46.33.log)
Here are the logs for dd_setup:
[dd_setup_20230803154718.log](https://github.com/RadeonOpenCompute/ROCm/files/12254617/dd_setup_20230803154718.log)
[dd_setup_20230803154718_errors.log](https://github.com/RadeonOpenCompute/ROCm/files/12254618/dd_setup_20230803154718_errors.log)
And the logs for dd_VSIXInstaller: 
[dd_VSIXInstaller_20230803154717_30d8.log](https://github.com/RadeonOpenCompute/ROCm/files/12254625/dd_VSIXInstaller_20230803154717_30d8.log)
[dd_VSIXInstaller_20230803154715_405c.log](https://github.com/RadeonOpenCompute/ROCm/files/12254626/dd_VSIXInstaller_20230803154715_405c.log)


---

### 评论 #6 — saadrahim (2023-08-03T20:01:21Z)

Thanks for the logs, I have let our install team know they are available. 

---

### 评论 #7 — Jan-Huber (2023-08-03T20:42:08Z)

I encountered the same error code during my installation. 
It would be very helpful document the problem under:
https://www.amd.com/en/support/kb/faq/gpu-kb215

Sadly my logs are no longer available, because I chose the nuclear option:
My seecond installation attempt went smoothly on a fresh install of Windows 11 with the latest Visual Studio 2022

---

### 评论 #8 — TheBurntWaffl3 (2023-08-03T23:16:02Z)

After updating my visual studio code it successfully installed, no further issue!

---

### 评论 #9 — scarsty (2023-09-04T07:59:40Z)

I've got the same error. Only visual studio plugin is failed. Here is the log:
[Install HIP SDK Visual Studio 2022 Plugin 2023_09_04_15.45.24.log](https://github.com/RadeonOpenCompute/ROCm/files/12511455/Install.HIP.SDK.Visual.Studio.2022.Plugin.2023_09_04_15.45.24.log)


---

### 评论 #10 — jazzar-dev (2023-10-06T07:30:16Z)

Did you find the solution for this error? 

---

### 评论 #11 — hhfff (2023-11-10T03:56:14Z)

I encountered the same error, successful installed after choose not to install visual studio plugin

---

### 评论 #12 — 108806 (2023-11-25T03:54:36Z)

Error 215, cleanup util did not help

---

### 评论 #13 — yanite (2023-12-22T03:06:20Z)

Error 215 ， is reinstall it , fail
Reinstalling it separately HIPExtension2022.vsix can be successful.

---

### 评论 #14 — wdx04 (2024-01-22T01:30:09Z)

Same here, Error 215 when installing with Vision Studio Plugin, Success when installing without Vision Studio Plugin

---

### 评论 #15 — jeus1609 (2024-04-23T02:47:34Z)

I had the visual studio community version installed

---

### 评论 #16 — VictoireWood (2024-05-28T13:17:05Z)

> Error 215 ， is reinstall it , fail Reinstalling it separately HIPExtension2022.vsix can be successful.

How can I get the HIPExtension2022.vsix file?

---

### 评论 #17 — wdx04 (2024-05-29T00:33:20Z)

> > Error 215 ， is reinstall it , fail Reinstalling it separately HIPExtension2022.vsix can be successful.
> 
> How can I get the HIPExtension2022.vsix file?

You need an archiver that can handle MSI files, such as 7-zip.
Open the HIP SDK installer EXE with 7-zip, and extract the MSI file from Packages\Apps\ROCmSDKPackages\VisualStudioPlugin2022,
Then open the extracted MSI file with 7-zip, you can find a 'VisualStudio2022Install' file, extract that file and add a .vsix extension to it. Then double-click VisualStudio2022Install.vsix to install.


---

### 评论 #18 — VictoireWood (2024-05-29T07:10:37Z)

> > > Error 215 ， is reinstall it , fail Reinstalling it separately HIPExtension2022.vsix can be successful.
> > 
> > 
> > How can I get the HIPExtension2022.vsix file?
> 
> You need an archiver that can handle MSI files, such as 7-zip. Open the HIP SDK installer EXE with 7-zip, and extract the MSI file from Packages\Apps\ROCmSDKPackages\VisualStudioPlugin2022, Then open the extracted MSI file with 7-zip, you can find a 'VisualStudio2022Install' file, extract that file and add a .vsix extension to it. Then double-click VisualStudio2022Install.vsix to install.

Holy crap, it works! Thanks a lot! 

---

### 评论 #19 — tomashomecat (2024-06-26T17:59:52Z)

hi guys
this solution looking as a joke. it works, HIP is installed (fu...ing 5GB !!!), but i am some disappointed and now expect that such blunders will repeat again. why nobody still didnt correct this mistake and didnt rename msi to vsix?

---

### 评论 #20 — GitHub-BeiJiXin (2025-11-12T09:58:59Z)

> > > Error 215 ， is reinstall it , fail Reinstalling it separately HIPExtension2022.vsix can be successful.错误 215，重新安装失败。单独重新安装 HIPExtension2022.vsix 可以成功。
> > 
> > 
> > How can I get the HIPExtension2022.vsix file?如何获取 HIPExtension2022.vsix 文件？
> 
> You need an archiver that can handle MSI files, such as 7-zip.你需要一款能够处理 MSI 文件的压缩软件，例如 7-zip。 Open the HIP SDK installer EXE with 7-zip, and extract the MSI file from Packages\Apps\ROCmSDKPackages\VisualStudioPlugin2022,使用 7-zip 打开 HIP SDK 安装程序 EXE，并从 Packages\Apps\ROCmSDKPackages\VisualStudioPlugin2022 中提取 MSI 文件， Then open the extracted MSI file with 7-zip, you can find a 'VisualStudio2022Install' file, extract that file and add a .vsix extension to it. Then double-click VisualStudio2022Install.vsix to install.然后使用 7-zip 打开解压后的 MSI 文件，找到一个名为“VisualStudio2022Install”的文件，解压该文件并添加 .vsix 扩展名。然后双击 VisualStudio2022Install.vsix 进行安装。

OMG，Absolutely amazing!

---

### 评论 #21 — suxiu996 (2026-02-20T15:58:19Z)

> > > 错误 215，重新安装失败。单独重新安装 HIPExtension2022.vsix 可以成功。
> > 
> > 
> > 如何获取 HIPExtension2022.vsix 文件？
> 
> 你需要一款能够处理 MSI 文件的压缩软件，例如 7-Zip。 使用 7-Zip 打开 HIP SDK 安装程序 EXE 文件，并从 Packages\Apps\ROCmSDKPackages\VisualStudioPlugin2022 目录下提取 MSI 文件。 然后使用 7-Zip 打开提取出的 MSI 文件，你会找到一个名为“VisualStudio2022Install”的文件，提取该文件并添加 .vsix 扩展名。最后，双击 VisualStudio2022Install.vsix 文件即可进行安装。

It's fixed my god love you 

---
