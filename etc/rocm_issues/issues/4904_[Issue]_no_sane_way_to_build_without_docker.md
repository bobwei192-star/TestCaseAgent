# [Issue]: no sane way to build without docker

> **Issue #4904**
> **状态**: closed
> **创建时间**: 2025-06-09T14:35:27Z
> **更新时间**: 2025-06-11T02:18:25Z
> **关闭时间**: 2025-06-10T03:36:57Z
> **作者**: ObiWahn
> **标签**: AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/4904

## 标签

- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

```
» make -f ../ROCm-6.4.1/ROCm/tools/rocm-build/ROCm.mk all
OUT_DIR=
ROCM_INSTALL_PATH=
sudo mkdir -p -m 775 "" && \
sudo chown -R "1000:1000" "/opt"     #<-- DAMN IT AMD WHAT IS WRONG HERE?
[sudo] password for <user>:
sudo: a password is required
make: *** [../ROCm-6.4.1/ROCm/tools/rocm-build/ROCm.mk:269: /logs] Error 1
```

Why would any step except `make install` require root permissions? This is seriously fucked up. I think I am going to buy an NVIDIA card for AI play. It was a mistake to buy an AMD device. This is something nobody somewhat sane would want to touch  with a ten-foot pole. How can you hope that anyone will use this? I really hope for your that you will get it straight some day, so there is a bit competition in the AI hardware space. But if the rest of your software is, as the first few minutes promise, your hardware could be the best, but you still would not get adopted widely.
I guess your developers hate it and nobody, who does not get get payed, is willing to invest time into this. Please hire someone who is willing to fix the build and support this guy as good as you can. 

### How To Reproduce

Just follow the official instructions. Note that the makefile does not support `PREFIX`, and there is not other documented way to change the output directory. 



---

## 评论 (6 条)

### 评论 #1 — polarathene (2025-06-09T22:44:49Z)

System deps should be installed as root. Just like programs typically are, but that doesn't prevent you running them as a user which only requires read + execute permissions. Then when updating software on linux you'd use root again to write the updates.

A Docker container will have the same problem when it's rootful and you try to perform operations as a non-root user within the container. Just because you may grant a non-root user on the system to run rootful docker commands doesn't mean it's more secure, nor is doing so with a rootful container that runs as a non-root container user that ideal. Instead you'd want to use rootless containers if you care about security / non-root system users, this allows the container user to run as root but without the concerns of rootful containers.

Beyond this, sure you can install portable software as a non-root user on a system, but when you need system deps it's not as advisable. ROCm requires access to some system paths that a non-root user would typically not belong to (groups like `video`) for security reasons.

---

Do you have an actual valid use-case that requires non-root? How is it better with Nvidia? Outside of a container, you just need the system packages installed, then you can use those as non-root, or for containers you can enable GPU support for the container (_both AMD and Nvidia support the more modern CDI spec for this, you just need to follow eithers instructions for the initial setup_).

---

### 评论 #2 — stellaraccident (2025-06-10T03:36:57Z)

While it does not support all of ROCm, and it will only support building against release tags that come into existence from this point forward, we are addressing most of this feedback with the new TheRock build system.

Specifically, per your comment:

* Just git and submodules (although we do have to use a fetch_sources.py right now which also applies some patches locally while we get everything caught up -- sorry... best we can do for the moment).
* Aims to be compatible with arbitrary Linux (and Windows) systems (while most current CI is based off of an AlmaLinux container, it has minimal additions).
* Avoids all AMD shell script based solutions and does not modify system state.
* Defaults to build from source for dependencies which usually come from the system and can vary wildly (can be overridden for OS packagers in order to use system packages) so that the default experience should work.
* If using build-from-source deps, the default is to use fetch content to source bundles that we mirror with SHA hashes, third party deps are centrally managed so that external fetches can be disabled completely if needed (some ROCm sub-projects currently also do secondary fetches, but we are working to eliminate these).
* It is just a build system. Packaging exists separately, and we do not rely on packaging to build.
* We have reference PyTorch build scripts in the repo with patch sets for HEAD (currently requires no patches) and current stable 2.7 (with patches).

Various individual ROCm projects are being upgraded to meet many of the standards you are asking for, but this involves several large scale changes that we are still working through, so the present state is not yet perfect.

Closing this and several other related issue in favor of this one: https://github.com/ROCm/TheRock/issues/797

New build system: https://github.com/ROCm/TheRock

I apologize for the poor experience so far and hope that the new approaches will meet your needs as they mature.

---

### 评论 #3 — ObiWahn (2025-06-10T08:46:05Z)

> System deps should be installed as root. Just like programs typically are, but that doesn't prevent you running them as a user which only requires read + execute permissions. Then when updating software on linux you'd use root again to write the updates.

Since when is `make`  meant to install debs? It is typically the took that does the concurrent build like ninja. If you must have separate target that you have to call consciously.

> A Docker container will have the same problem when it's rootful and you try to perform operations as a non-root user within the container. Just because you may grant a non-root user on the system to run rootful docker commands doesn't mean it's more secure, nor is doing so with a rootful container that runs as a non-root container user that ideal. Instead you'd want to use rootless containers if you care about security / non-root system users, this allows the container user to run as root but without the concerns of rootful containers.

Thank for the explanation in am a happy podman user.

> 
> Beyond this, sure you can install portable software as a non-root user on a system, but when you need system deps it's not as advisable. ROCm requires access to some system paths that a non-root user would typically not belong to (groups like `video`) for security reasons.

Why would it need special path? Why would mechanisms like pkg-config not work? What about RPATH or LD_LIBRARY_PATH? there is zero need to use certain paths. You are right that the software eventually will need access to some paths in `/dev/` but that is all. Maybe you could explain the special requirements in a bit more detail. Have you ever tried `groups`? I bet your user is in the `video` group.

> Do you have an actual valid use-case that requires non-root? How is it better with Nvidia? Outside of a container, you just need the system packages installed, then you can use those as non-root, or for containers you can enable GPU support for the container (_both AMD and Nvidia support the more modern CDI spec for this, you just need to follow eithers instructions for the nitial setup_).

There is no system package for debain/sid that I could simply use. My use case is that I use a running release for about 10 years. I am not interested in setting up a new system. If you lightly run installer scripts like the one given here you break your installation sooner than you wish. Have you ever build gcc, clang, QT6, boost or any other well known software? 

Usually software just lists the dependencies, which you try to install as good as you can. Then you start to configure/build. It will complain about a missing lib or .h or missing symbols when linking. If so you install what is missing. This is something people know and happily do. You on the other hand just need to support generic a Linux without worrying to maintain package lists for different distributions. This in turn will reduce the amount of time needed to maintain the the build infrastructure, allowing you to focus on things that matter instead of checking if a package was renamed in some distribution or is available in a high enough version. 

---

### 评论 #4 — IMbackK (2025-06-10T09:25:39Z)


> Usually software just lists the dependencies, which you try to install as good as you can. Then you start to configure/build. It will complain about a missing lib or .h or missing symbols when linking. If so you install what is missing. This is something people know and happily do. You on the other hand just need to support generic a Linux without worrying to maintain package lists for different distributions. This in turn will reduce the amount of time needed to maintain the the build infrastructure, allowing you to focus on things that matter instead of checking if a package was renamed in some distribution or is available in a high enough version.

If this is what you want you should just build the rocm componants you want individually, ROCM is really just a collection of packages and not a software package itself. The packages all use regular build systems like cmake you can just use for eatch one.
Some of them have some pitfalls in the their individual build system but mostly these are like any other linux software.

---

### 评论 #5 — ObiWahn (2025-06-10T10:19:09Z)

> While it does not support all of ROCm, and it will only support building against release tags that come into existence from this point forward, we are addressing most of this feedback with the new TheRock build system.
> 
> Specifically, per your comment:
> 
>     * Just git and submodules (although we do have to use a fetch_sources.py right now which also applies some patches locally while we get everything caught up -- sorry... best we can do for the moment).
> 
>     * Aims to be compatible with arbitrary Linux (and Windows) systems (while most current CI is based off of an AlmaLinux container, it has minimal additions).
> 
>     * Avoids all AMD shell script based solutions and does not modify system state.
> 
>     * Defaults to build from source for dependencies which usually come from the system and can vary wildly (can be overridden for OS packagers in order to use system packages) so that the default experience should work.
> 
>     * If using build-from-source deps, the default is to use fetch content to source bundles that we mirror with SHA hashes, third party deps are centrally managed so that external fetches can be disabled completely if needed (some ROCm sub-projects currently also do secondary fetches, but we are working to eliminate these).
> 
>     * It is just a build system. Packaging exists separately, and we do not rely on packaging to build.
> 
>     * We have reference PyTorch build scripts in the repo with patch sets for HEAD (currently requires no patches) and current stable 2.7 (with patches).
> 
> 
> Various individual ROCm projects are being upgraded to meet many of the standards you are asking for, but this involves several large scale changes that we are still working through, so the present state is not yet perfect.
> 
> Closing this and several other related issue in favor of this one: [ROCm/TheRock#797](https://github.com/ROCm/TheRock/issues/797)
> 
> New build system: https://github.com/ROCm/TheRock
> 
> I apologize for the poor experience so far and hope that the new approaches will meet your needs as they mature.

Hi, thank you for pointing me to TheRock. So far I just had some `automake` issue where I had to allow version 1.17 for numactl, but otherwise the build is running without issues (~1500 TUs left)

This is really nice and I think you are doing a good job there:) 👍 🥇

---

### 评论 #6 — polarathene (2025-06-11T02:18:24Z)

> Thank for the explanation in am a happy podman user.

Same should apply to Podman, it just runs as rootless by default for non-root user, while the container user itself can be "root" (mapped to subuid/subgid on host).

> Why would it need special path? Why would mechanisms like pkg-config not work? What about RPATH or LD_LIBRARY_PATH? there is zero need to use certain paths

I recall some software builds where packages weren't being discovered properly, but it was rather niche and specific to Cargo on Fedora (_IIRC it was related to where OpenSSL package installed something_).

`LD_LIBRARY_PATH` at build time is ok, although I've seen some projects publish images with that set. One in particular is Deno building for glibc then copying over to Alpine image where they rely on `LD_LIBRARY_PATH` to ensure it runs on Alpine without going through musl libc.

That image shouldn't have `LD_LIBRARY_PATH` set as global ENV, and should instead of leveraged `patchelf` to configure the rpath. In it's current state, attempting to use other software in that image that isn't Deno is fragile since libraries aren't resolved properly.

My advice was not that you can't do these things (_since as mentioned they clearly occur or can be problematic in niche cases_), but how system deps are typically handled to be compatible with other software dependent upon it without expecting the user to do any additional workarounds.

---

> You are right that the software eventually will need access to some paths in `/dev/` but that is all. Maybe you could explain the special requirements in a bit more detail.

Another example related to `/dev/` IIRC (_might have been one of the other special paths_), was when using openSUSE Leap in a container to install to a custom install root directory via `zypper`. Their package management relied on running some scripts that weren't entirely compatible for that scenario due to interaction with `/dev`.

Meanwhile the equivalent in Fedora with `dnf` works absolutely fine.

Regarding `/dev/` for GPUs, it's been a while personally, I only came across this issue when browsing this repo to look into concerns about building/running ROCm with containers. My last interaction with GPUs was on a linux host and virt-manager/virsh with something to do with an nvidia GPU using EGL properly for a VM guest (via virgl). So completely unrelated here for ROCm or builds.

---

> Have you ever tried `groups`? I bet your user is in the `video` group.

Yes you're correct, in WSL2 the non-root user has `video` in their groups, same as it'd be on a regular linux host.

Sorry, I must have recalled incorrectly and was thinking about the `render` group for `/dev/dri/renderD128` which I think had some risk to expose to non-root processes that you don't trust.


---

> If you lightly run installer scripts like the one given here you break your installation sooner than you wish. Have you ever build gcc, clang, QT6, boost or any other well known software?

Presently I just use containers, or if necessary VMs. When I have a linux host as the OS I'd just stick to packages (_I used ArchLinux or Fedora, which aren't as held back as Debian though_). I also had backups and the ability to rollback, or if necessary I'm comfortable troubleshooting a system that doesn't even boot because of an update or change I made.

But no, I've not needed to build any of those deps from source personally since I often had the latest available or I could defer a container to the task and copy build artifacts from that.

---

> Usually software just lists the dependencies, which you try to install as good as you can. Then you start to configure/build. It will complain about a missing lib or .h or missing symbols when linking. If so you install what is missing. This is something people know and happily do.

I am familiar with this process and have done it plenty of times when building others projects.

---

> You on the other hand just need to support generic a Linux without worrying to maintain package lists for different distributions. This in turn will reduce the amount of time needed to maintain the the build infrastructure, allowing you to focus on things that matter instead of checking if a package was renamed in some distribution or is available in a high enough version.

Are you packaging for a distro? I'm not sure if this quote was directed at me, I contribute to a variety of projects that use containers with different base images, sometimes they support more than one and need to manage the different packages they're reliant on (_software is built for a base image, rather than packaged to deb/rpm/etc_). Others have a CI step to package properly for distribution, sometimes with tools like GoReleaser that help simplify that.

If you instead have your own projects and don't want to fuss about that compatibility issue, publishing with a base image you're comfortable with and having the user install anything needed on their container host such as the ROCm/CUDA container toolkits for CDI support makes it simpler to offer broader support.

---

> Since when is `make` meant to install debs?

Is that what is happening here? I've not looked into the build process of this project yet personally (_and it doesn't seem like I need to_). Or is that what you inferred from my statement?

---
