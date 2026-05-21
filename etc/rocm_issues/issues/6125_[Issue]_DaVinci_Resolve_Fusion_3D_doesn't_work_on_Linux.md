# [Issue]: DaVinci Resolve Fusion 3D doesn't work on Linux

> **Issue #6125**
> **状态**: closed
> **创建时间**: 2026-04-07T19:43:08Z
> **更新时间**: 2026-04-17T18:56:31Z
> **关闭时间**: 2026-04-17T18:56:30Z
> **作者**: NIICKTCHUNS
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6125

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

### Problem Description

As I said on https://github.com/ROCm/ROCm/issues/5982#issuecomment-4199305082

The Fusion tab of DaVinci Resolve is not working for a long time now, this is probably something that Blackmagic needs to fix by itself so I don't know if this is exactly related to ROCm, but it would be appreciated some attention. The track for this on [Blackmagic Forum](https://forum.blackmagicdesign.com/viewtopic.php?f=22&t=222293).

The entire 3D workflow doesn't work, Hardware Render doesn't work, the 3D Viewer doesn't work, the prints below show the Fusion console, the 3D Viewer space and a simple node tree for demonstration, anything on the Renderer3D being hardware accelerated doesn't appear, and the 3D viewer is always rendered by the GPU it seems, so it doesn't show anything.

<img width="564" height="354" alt="Image" src="https://github.com/user-attachments/assets/9f7ca933-75a0-49e7-be1b-4b5ad1d2ada5" />
<img width="704" height="406" alt="Image" src="https://github.com/user-attachments/assets/43bb13d1-ca15-4a44-b5b4-57f0635fab7f" />
<img width="692" height="239" alt="Image" src="https://github.com/user-attachments/assets/27e1e002-ecfb-4a21-a0c2-e5fd69deef99" />

I'm using the latest version of DaVinci Resolve (20.3.2 at the moment), some users on the Blackmagic Forum says that on older versions of DaVinci Resolve worked just fine, I didn't tested it so I can't speak for them, some NVIDIA users says that Blackmagic solved the issue, some AMD users says that works with distrobox and others says that it doesn't, I'm not following up that thread anymore so thats all I know, I didn't tested distrobox either.

### Operating System

Arch Linux

### CPU

AMD Ryzen 5 5600

### GPU

AMD Radeon RX 7600

### ROCm Version

7.2.1

### ROCm Component

_No response_

### Steps to Reproduce

Use the Fusion tab of DaVinci Resolve, add some nodes to make a simple 3D scene, like adding a text to the renderer3d like i've shown on the image

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

My environment variables are

```
GTK_CSD=0
GTK_USE_PORTAL=1
XMODIFIERS=@im=fcitx
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
QT_IM_MODULES="wayland;fcitx"
SDL_IM_MODULE=wayland
MANGOHUD=1
KWIN_WAYLAND_SUPPORT_XX_PIP_V1=1
ENABLE_LAYER_MESA_ANTI_LAG=1
```

---

## 评论 (10 条)

### 评论 #1 — lseurttyuu (2026-04-07T19:57:27Z)

I confirm the issue on my platform - it's easy to validate the issue using 3D preset titles like "Ribbon Text" for example. From what I remember it was working fine in Davinci Resolve Studio 19.

My platform:
- GPU: Radeon RX 7900 XTX
- OS: Debian 13 (kernel 6.12)
- ROCm version: 7.2.1
- DaVinci Resolve version: 20.3.2 (Studio)


Davinci Resolve console logs:
```
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 38, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 39, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 40, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 40, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 40, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 41, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 41, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 41, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 42, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 44, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 44, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 44, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 47, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 45, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 45, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 78, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 41, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 47, layer [Main]
Renderer3D1_1:  Error - ImagePlane3D1_1 (Image Plane 3D):  material tree creation failed
Renderer3D1_1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 47, layer [Main]

```

---

### 评论 #2 — sshi-amd (2026-04-12T21:08:46Z)

Hi, I've tried copying the configuration following however I'm not sure what the next steps would be for reproducing as I'm not too familiar with Davinci Resolve. Could you elaborate a bit on the reproducer so I can give it a try, thanks!

---

### 评论 #3 — NIICKTCHUNS (2026-04-12T21:54:16Z)

> Hi, I've tried copying the configuration following however I'm not sure what the next steps would be for reproducing as I'm not too familiar with Davinci Resolve. Could you elaborate a bit on the reproducer so I can give it a try, thanks!

@sshi-amd Here it is, when the node fails their text immediately becomes red and outputs it to the console, you can also test if the node has errors by trying to move the text, to move it you click on the Text3D node and go the Transform tab, there you can change the value of XYZ, it will not move since the hardware renderer is not working

https://github.com/user-attachments/assets/574e1838-460a-4a20-acca-a4850624eaad

---

### 评论 #4 — sshi-amd (2026-04-12T23:05:32Z)

Much thanks for the video! I just followed your steps on a gfx 1103 igpu laptop and only managed to get the first error (Renderer3D1: cannot get Parameter for SceneInput at time 0, layer [Main]) and the text is moving for me when changing the XYZ. I'll try to source an gfx 1102 gpu and try again on my desktop tomorrow.

---

### 评论 #5 — NIICKTCHUNS (2026-04-12T23:35:45Z)

> Much thanks for the video! I just followed your steps on a gfx 1103 igpu laptop and only managed to get the first error (Renderer3D1: cannot get Parameter for SceneInput at time 0, layer [Main]) and the text is moving for me when changing the XYZ. I'll try to source an gfx 1102 gpu and try again on my desktop tomorrow.

You're welcome! I get all these errors when switching to the Hardware Renderer, one thing that I forgot to mention in the video, is that in order to show the 3D Viewer you don't actually need to add the Merge3D node, you can use the Text3D node, and after that click on the number 1 or 2 on your keyboard to add it to the left or right preview, you can also drag and drop the node to one of the previews

https://github.com/user-attachments/assets/75d1dc27-c6f2-4e0c-ba34-14cc78a58788

---

### 评论 #6 — sshi-amd (2026-04-14T23:02:55Z)

Had some trouble with Davinci Resolve but I managed to get the setup, however I'm not facing the same errors. I am using a Radeon RX 7900 XTX since @lseurttyuu also faced the same issue with this gpu. 

<img width="2528" height="1366" alt="Image" src="https://github.com/user-attachments/assets/b44c81f4-a4be-4514-a23c-db9b9419cfe3" />

---

### 评论 #7 — lseurttyuu (2026-04-15T11:15:40Z)

Could it be that the free version of DRS handles things differently than the paid Studio version when it comes to Fusion rendering? I've taken the steps @NIICKTCHUNS showcased (`fusion.mp4`) and confirmed the first issue is present on my platform (not just the Ribbon text I hinted up in the conversation):

```
Renderer3D1:  Error - UnknownTool (Unknown Tool):  material tree creation failed
Renderer3D1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 39, layer [Main]
MediaOut1 failed at time 39
Renderer3D1:  Error - UnknownTool (Unknown Tool):  material tree creation failed
Renderer3D1:  Render will be aborted
MediaOut1 cannot get Parameter for Input at time 39, layer [Main]
MediaOut1 failed at time 39
```

However, I dug into the `resolve_graphics_log.txt` file (which is auto-generated DR log file) and when switching to the hardware renderer, it clearly shows a shader compilation failure:

```
[Error] vk-GLSL --> SPIR-V parse failure, Stage=Fragment, Label=, ID=41
[Error] ERROR: 0:445: 'constructor' : too many arguments 
ERROR: 0:445: 'assign' :  cannot convert from ' const float' to ' global highp 3-component vector of float'
ERROR: 0:445: '' : compilation terminated 
ERROR: 3 compilation errors.  No code generated.
```

Here's the whole log file for reference:
[resolve_graphics_log_HardwareRenderer.txt](https://github.com/user-attachments/files/26746666/resolve_graphics_log_HardwareRenderer.txt)

Based on this, I suspect (correct me if I'm wrong) this issue actually isn't related to ROCm at all. The log shows DaVinci Resolve is (probably?) generating malformed GLSL syntax.

Since I'm using the opensource Mesa driver, I wonder if it is simply rejecting the bad syntax, whereas the proprietary AMD drivers (`amdgpu-pro`) that I assume @sshi-amd is using might be quietly forgiving/fixing it?

---

### 评论 #8 — NIICKTCHUNS (2026-04-15T11:45:34Z)

> Could it be that the free version of DRS handles things differently than the paid Studio version when it comes to Fusion rendering? I've taken the steps [@NIICKTCHUNS](https://github.com/NIICKTCHUNS) showcased (`fusion.mp4`) and confirmed the first issue is present on my platform (not just the Ribbon text I hinted up in the conversation):

I don't think that's the case here, I already tested the free version and it also doesn't work

> However, I dug into the `resolve_graphics_log.txt` file (which is auto-generated DR log file) and when switching to the hardware renderer, it clearly shows a shader compilation failure:
> 
> ```
> [Error] vk-GLSL --> SPIR-V parse failure, Stage=Fragment, Label=, ID=41
> [Error] ERROR: 0:445: 'constructor' : too many arguments 
> ERROR: 0:445: 'assign' :  cannot convert from ' const float' to ' global highp 3-component vector of float'
> ERROR: 0:445: '' : compilation terminated 
> ERROR: 3 compilation errors.  No code generated.
> ```

Yeah, I get that exact same error on that file, I'll probably report this error to the Blackmagic Forum too if someone didn't already do this


> Based on this, I suspect (correct me if I'm wrong) this issue actually isn't related to ROCm at all. The log shows DaVinci Resolve is (probably?) generating malformed GLSL syntax.
> 
> Since I'm using the opensource Mesa driver, I wonder if it is simply rejecting the bad syntax, whereas the proprietary AMD drivers (`amdgpu-pro`) that I assume [@sshi-amd](https://github.com/sshi-amd) is using might be quietly forgiving/fixing it?

As I said in the main text of the issue, I don't think thats an AMD fault, thats probably something that Blackmagic has do solve on their side, I was just making sure that maybe something could be done here since Blackmagic is pretty lazy on this

Also, I'm pretty sure that the AMD Pro drivers doesn't exist anymore, nowdays its only Mesa, and the OpenCL is pulled from here, at least for [opencl-amd](https://aur.archlinux.org/packages/opencl-amd) which is what I use on my PC, so

Mesa 26.0.4-arch1.1
ROCm OpenCL 7.2.1

---

### 评论 #9 — sshi-amd (2026-04-15T14:39:22Z)

>Also, I'm pretty sure that the AMD Pro drivers doesn't exist anymore, nowdays its only Mesa, and the OpenCL is pulled from here, 
at least for [opencl-amd](https://aur.archlinux.org/packages/opencl-amd) which is what I use on my PC, so
>
>Mesa 26.0.4-arch1.1
ROCm OpenCL 7.2.1

My drivers are from https://repo.radeon.com/amdgpu/30.30/ubuntu/ which installs as Mesa 26.0.0-devel - AMD's own build of Mesa.  

From that I installed these packages
```
libgl1-amdgpu-mesa-glx libgl1-amdgpu-mesa-dri libegl1-amdgpu-mesa libegl1-amdgpu-mesa-drivers
```
 Unfortunately these packages are only available as .deb packages for Ubuntu, not for Arch or Debian. But this does confirm it's likely a Blackmagic issue (bad GLSL) rather than a ROCm issue.



---

### 评论 #10 — darren-amd (2026-04-17T18:56:30Z)

Thanks all,

Closing as this does not appear to be ROCm related. If in the future you run into any issues related to ROCm please feel free to reopen/open a new ticket.

---
