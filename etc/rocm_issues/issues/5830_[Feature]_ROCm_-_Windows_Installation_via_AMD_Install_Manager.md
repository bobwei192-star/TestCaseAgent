# [Feature]: ROCm - Windows Installation via AMD Install Manager

> **Issue #5830**
> **状态**: closed
> **创建时间**: 2026-01-03T07:21:35Z
> **更新时间**: 2026-01-30T22:30:21Z
> **关闭时间**: 2026-01-30T06:45:32Z
> **作者**: Spitlebug
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5830

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Suggestion Description

Suggestion: ROCm Installation in Windows via AMD Install Manager or Binary Executable with Installer/Uninstaller.

Background:
WSL is no longer required for ROCm Installation and use in Windows Environment.
ROCm currently only supports installation with Git.
It is difficult to Install/Uninstall ROCm in Windows.
It is difficult to check the current ROCm version in Windows.
It is difficult if not impossible to downgrade ROCm in Windows.
ROCm versions can cause conflicts with Existing AMD Software and/or Drivers.
Installation via Git doesn't allow for directory specific installation paths.

Solution:
Installation in Windows via AMD Install Manager or Binary Executable solves all of these issues.


### Operating System

Windows 11

### GPU

All viable AMD GPUs

### ROCm Component

ROCm

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2026-01-09T21:21:34Z)

Hey @Spitlebug, thanks for sharing this feedback. We are looking into a couple different solutions to simplify the installation of both ROCm and third party apps on the Windows side. While I can't go into the specifics right now, https://blog.comfy.org/p/official-amd-rocm-support-arrives is just one example of the improvements with more in the pipeline!

> ROCm currently only supports installation with Git.
Installation via Git doesn't allow for directory specific installation paths.

If you'd like a directory specific installation of ROCm, you can pull in the latest development build from TheRock and install wherever you see fit. For steps on how to do this, see https://github.com/ROCm/TheRock/blob/main/RELEASES.md#installing-from-tarballs. Let me know if you have any questions regarding this.

---

### 评论 #2 — Spitlebug (2026-01-10T03:31:13Z)

> While I can't go into the specifics right now, https://blog.comfy.org/p/official-amd-rocm-support-arrives is just one example of the improvements with more in the pipeline!

Non-productive.

> If you'd like a directory specific installation of ROCm, you can pull in the latest development build from TheRock and install wherever you see fit. For steps on how to do this, see https://github.com/ROCm/TheRock/blob/main/RELEASES.md#installing-from-tarballs. Let me know if you have any questions regarding this.

Is this (therock-dist-windows-gfx120X-all-7.11.0a20260109.tar) TAR file supposed to be 11.7gb when extracted from the GZ file with 7-Zip?

Documentation is outdated, uses Acronyms without explanation as to what the Acronyms are.
Reliance on Git Documentation for User facing software is poor form. See above comment.
Jargon too foreign.

Installing TAR requires PIP? Documentation unclear.
Simply Extract installs ROCm? Documentation unclear.
Simply Deleting Extracted Archive uninstalls ROCm? Documentation unclear.

HIP SDK is no longer required in Windows to use ROCm 7.0+
WSL is no longer required in Windows to use ROCm
hipInfo.exe was found inside \ROCm\bin in (therock-dist-windows-gfx120X-all-7.11.0a20260109.tar)
hipInfo.exe was also found in several other locations (see Screenshot).
Windows Defender flagged all hipInfo.exe Executables (see Screenshot).

Still unsure how to uninstall / downgrade ROCm 7.1.1 as installed with Git/Pip in Windows. ROCm 7.1.1 has broken AMD Chat. Seemingly requires knowledge on Git / Python commands in CMD / PowerShell that 99.99% of Windows users do not / will not know. Furtherance to Documentation outdated / incomplete.

I am trying to make this as actionable as possible (see postscript below for personal thoughts / observations).

<img width="1239" height="158" alt="Image" src="https://github.com/user-attachments/assets/9d136de7-2edb-43b9-8453-5ab8b7dac725" />

<img width="720" height="485" alt="Image" src="https://github.com/user-attachments/assets/9ed6fb42-e98b-4359-b3dd-e051ee23aa90" />


PS: ComfyUI refuses to output coherent images in Latent Image sizes other than 512 x 512 px. ComfyUI also refuses to output coherent images after a large number of  generations (10-20 images) on RX 9070 XT running ROCM 7.1.1. in Windows 11. Applies to both Portable and Desktop ComfyUI. Could be ComfyUI, could be ROCm. No idea how to dump what is going on as there is no particular "error" other than garbled images (and not in the way AI Image generation can be garbled when operating correctly).

PPS: I understand this is all held together with duct tape, chewing gum and whatnot. Windows doesn't have Dockers outside of using WSL. It is my personal opinion that Dockers are just poor stop gaps by the FOSS ecosystem in creating more forks of projects than one can shake a proverbial stick at. Things such as Python Version, PyTorch Version and ROCm version irrespective of actual software incompatibilities with said dependencies. I also understand that most AI development is done on Linux. Having said that, the manner in which Linux prefers to acquire and install/compile software is an anathema to Windows Environment where the strength of Windows is the uniformity and reliance on Executables and Registry entries. If widespread adoption on Windows is a goal, that will have to be front of mind. Most Windows Users will be running on bare metal, so messing around like one can in a Virtual Machine isn't as viable. That means if an installation is bad or it is not possible to uninstall / downgrade ROCm creates the very real possibility of having to completely wipe and reinstall Windows (like I am facing right now).

---

### 评论 #3 — Spitlebug (2026-01-30T06:45:13Z)

Follow up @harkgill-amd .

While it's not perfect, it is a start. Keep working at it. The UI implementation needs a little work as well as features like upgrading/downgrading/uninstalling various components (ROCm, PyTorch etc...).

I wish there wasn't a need to these kinds of features, but there is. It's still early days for this technology.

Good luck.

![Image](https://github.com/user-attachments/assets/268be7e9-5fb5-4e9c-b562-dd15e1642461)
![Image](https://github.com/user-attachments/assets/dad5fe01-bccf-484e-aeed-05ede40771eb)

---

### 评论 #4 — harkgill-amd (2026-01-30T15:31:14Z)

Hey @Spitlebug, thanks for the feedback again - the AI bundle was what I was alluding to in my initial message :) . It's definitely in it's infancy and we're going to continue to iterate on it. 

> The UI implementation needs a little work

Do you have any specific suggestions that we can push forward?

> features like upgrading/downgrading/uninstalling various components

These are all features that are on the table for future releases - with the current release our focus was mainly to get this basic functionality available as soon as possible.

---

### 评论 #5 — Spitlebug (2026-01-30T22:30:21Z)

> Hey [@Spitlebug](https://github.com/Spitlebug), thanks for the feedback again - the AI bundle was what I was alluding to in my initial message :) . It's definitely in it's infancy and we're going to continue to iterate on it.

@harkgill-amd I understand that, however you are in a position to know these things while I am not. It isn't productive to allude to things. I don't envy your position, not being able to say company business. It is what it is.

> Do you have any specific suggestions that we can push forward?

If Install Manager is to retain it's current UI "feel" more thought is going to have to be put into the UI scalability of the software. Adrenalin for example (even though it has a proprietary skin) can be resized. No such functionality exists with AMD Install Manager. I do not believe it was ever meant for such functionality in the first place. There is already a template that has existed since Windows 95 that would allow installation of "additional features". You could add your own flare to it, but it requires vertical scroll bars if the Install Manager UI stays the same (see example images).

<img width="618" height="368" alt="Image" src="https://github.com/user-attachments/assets/df89925f-8936-4acd-ba55-573fe72f2486" />

<img width="418" height="484" alt="Image" src="https://github.com/user-attachments/assets/66990765-ef00-4255-9b9d-85d783854b86" />

<img width="468" height="422" alt="Image" src="https://github.com/user-attachments/assets/e1f8530e-c277-4324-8458-7e185bb7b0ec" />

> > features like upgrading/downgrading/uninstalling various components

> These are all features that are on the table for future releases - with the current release our focus was mainly to get this basic functionality available as soon as possible.

This is productive. The fractured nature of development on Linux necessitates this.



---
