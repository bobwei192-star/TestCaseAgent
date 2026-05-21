# [Issue]:Build script multiple issues.

> **Issue #4624**
> **状态**: closed
> **创建时间**: 2025-04-14T19:28:11Z
> **更新时间**: 2025-06-10T03:35:09Z
> **关闭时间**: 2025-06-10T03:35:07Z
> **作者**: emerth
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4624

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Regarding the build script presented at https://github.com/ROCm/ROCm, section "Build ROCm from source".

1) Script WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22/install-prerequisites.sh tries to run apt install, but it does not call "sudo apt install ...". 

So you need to run the install-prerequisites.sh script using `sudo sh install-prerequisites.sh`. 

OTOH same script runs pip installs. Running pip install as root clobbers system packages, is generally a bad idea.

How about writing a prerequisites install script that invokes various bits and bobs with appropriate use of sudo?

2) We declare in the build script that we are doing ROCm-6.4:

```
export ROCM_VERSION=6.4.0
~/bin/repo init -u http://github.com/ROCm/ROCm.git -b roc-6.4.x -m tools/rocm-build/rocm-${ROCM_VERSION}.xml
~/bin/repo sync
```

However in WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22 there is no branch checked out. Git says "no branch".

3) In directory WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22 are two versions of the install prerequisites shell script:

```
emerth@desktop ~/WORKSPACE $ pushd ROCm/tools/rocm-build/docker/ubuntu22
~/WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22 ~/WORKSPACE ~/WTF
emerth@desktop ~/WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22 ((no branch))$ ls -lF
total 40
-rw-rw-r-- 1 emerth emerth   312 Apr 14 18:19 Dockerfile
-rw-rw-r-- 1 emerth emerth  9835 Apr 14 18:19 install-prerequisites.sh
-rw-rw-r-- 1 emerth emerth 10875 Apr 14 18:19 install-prerequisities.sh
-rw-rw-r-- 1 emerth emerth    43 Apr 14 18:19 local-pin-600
-rw-rw-r-- 1 emerth emerth  1654 Apr 14 18:19 packages
-rw-rw-r-- 1 emerth emerth   582 Apr 14 18:19 README.md
emerth@desktop ~/WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22 ((no branch))$
```
The two versions are substantially different. 

The one which name is not an obvious typo fails to complete:

```
<SNIP>
Resolving repo.radeon.com (repo.radeon.com)... 184.30.150.219, 184.30.150.213, 2600:140a:1000:f::b81e:960e, ...
Connecting to repo.radeon.com (repo.radeon.com)|184.30.150.219|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 17000 (17K) [application/octet-stream]
Saving to: ‘amdgpu-install_6.3.60300-1_all.deb’

amdgpu-install_6.3.60300-1_all.deb     100%[============================================================================>]  16.60K  --.-KB/s    in 0.003s

2025-04-14 17:52:18 (5.36 MB/s) - ‘amdgpu-install_6.3.60300-1_all.deb’ saved [17000/17000]

+ apt install -y ./amdgpu-install_6.3.60300-1_all.deb
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Note, selecting 'amdgpu-install' instead of './amdgpu-install_6.3.60300-1_all.deb'
The following packages were automatically installed and are no longer required:
  libgoogle-glog0v5 libstdc++-12-dev rocdecode rocdecode-dev
Use 'sudo apt autoremove' to remove them.
The following packages will be DOWNGRADED:
  amdgpu-install
0 upgraded, 0 newly installed, 1 downgraded, 0 to remove and 0 not upgraded.
E: Packages were downgraded and -y was used without --allow-downgrades.

```
It appears to want to install drivers(?) from rocm 6.3 despite this being a build for 6.4.

The one which name is an obvious typo also has to be run as root else it fails running apt, and also fails at modifying system directories as well, some of which don't even exist (/var/lib/apt/lists/partial, /usr/local/ccache, others). AFAIK on Ubuntu there has never been a /var/lib/apt/lists/partial directory? 

At this point in the ROCm adventure I decided `WTH the machine is half trashed by now, what with all the crap the other prereq script just did`, so just run install-prequities.sh as root. Finally this script has been running for over thirty minutes wall clock time on my 5900X using an NVMe SSD - it's building stuff from GRPC, from OFED I think, lapack, boring ssl, other HPC-like stuff, it even seems to have built the entire Boost binary library suite from source. Maybe this script is not suppose to be there? If it is supposed to be there maybe it needs a name that indicates it's purpose (something like I_AM_THE_SCRIPT_THAT_WILL_TURN_YOUR_PC_INTO_A_SOFTWARE_CLONE_OF_FRONTIER_SUPERCOMPUTER.sh). Remarkably this version of the prereq script runs to completion.

4) This absolute gem:

```
emerth@desktop ~/WORKSPACE $ make -f ROCm/tools/rocm-build/ROCm.mk -j ${NPROC:-$(nproc)} rocm-dev
OUT_DIR=/home/emerth/WORKSPACE/out/ubuntu-22.04/22.04
ROCM_INSTALL_PATH=/opt/rocm-6.4.0
sudo mkdir -p -m 775 "/opt/rocm-6.4.0" && \
sudo chown -R "1000:1000" "/opt"
sudo chown -R "1000:1000" "/home/emerth"

```

**### _Just possibly there are people in the world who do not ******* want the ownership of their entire /opt and ~ directory trees overwritten?_**

5) I guess just a general bitch: If you people are going to post a script to build ROCm from source, and point people to that script, how about posting a script that bloody works, and which does not blow away file system ownerships en masse? And if such is not possible, how about posting a detailed instruction on building ROCm?



### Operating System

Ubuntu 22.04

### CPU

AMD Ryzen 9 5900X 12-Core Processor

### GPU

Radeon 780m, Radeon Pro VII, Radeon 9070XT

### ROCm Version

ROCm 6.4.0

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

### 评论 #1 — ppanchad-amd (2025-04-14T19:56:08Z)

Hi @emerth. Internal ticket has been created to investigate these issues. Thanks!

---

### 评论 #2 — schung-amd (2025-04-14T21:45:52Z)

Hi @emerth, first of all this isn't actually a build script. Notice there's no actual version-specific branching being done in e.g. 
```
# Option 1: Start a docker container
# Pulling required base docker images:
# Ubuntu22.04 built from ROCm/tools/rocm-build/docker/ubuntu22/Dockerfile
docker pull rocm/rocm-build-ubuntu-22.04:6.4
# Ubuntu24.04 built from ROCm/tools/rocm-build/docker/ubuntu24/Dockerfile
docker pull rocm/rocm-build-ubuntu-24.04:6.4
```
so running this as-is will not work.

> 1. ... Running pip install as root clobbers system packages, is generally a bad idea.

Fair. The Ubuntu 24 prereqs script creates a venv for this reason (although the Ubuntu 22 script doesn't for some reason), but there are other reasons not to pip install as root, I'll discuss with the internal team.

> 2. ... However in WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22 there is no branch checked out. Git says "no branch".

I see this as well, on my end I think it's because MIOpen is failing to sync. Looking into this.

> 3. In directory WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22 are two versions of the install prerequisites shell script

The version with the typo is from the ubuntu22 directory, the one without is from the ubuntu24 directory; see the file structure at https://github.com/ROCm/ROCm/tree/develop/tools/rocm-build/docker. These are in their proper directories on my end. You should use the one which corresponds to your OS, which is the typoed version. As for why this has a typo in the first place, this was added for 6.4 (https://github.com/ROCm/ROCm/commit/295e1e2998f206948c84b5936e008a1a22460e87#diff-bb92fcc28803a2cb8ce4028272460f1a67ba7248d56426182e2cb89b78cbd93b), I'll be checking in regarding that.

> 4. This absolute gem:

These instructions are for the Docker container, although to be fair we don't provide an alternative instruction here for baremetal installation. This is potentially still problematic inside a Docker if a non-default user is required for whatever reason.

> 5. ... how about posting a detailed instruction on building ROCm?

I'd suggest either trying these instructions in a Docker or just installing with one of our other methods at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/index.html. If there isn't a specific reason to build from source on baremetal I would avoid doing so as there are easier ways.


---

### 评论 #3 — emerth (2025-04-14T23:47:10Z)

> Hi [@emerth](https://github.com/emerth), first of all this isn't actually a build script. Notice there's no actual version-specific branching being done in e.g.
> 
> ```
> # Option 1: Start a docker container
> # Pulling required base docker images:
> # Ubuntu22.04 built from ROCm/tools/rocm-build/docker/ubuntu22/Dockerfile
> docker pull rocm/rocm-build-ubuntu-22.04:6.4
> # Ubuntu24.04 built from ROCm/tools/rocm-build/docker/ubuntu24/Dockerfile
> docker pull rocm/rocm-build-ubuntu-24.04:6.4
> ```
> 
> so running this as-is will not work.
> 
> > 1. ... Running pip install as root clobbers system packages, is generally a bad idea.
> 
> Fair. The Ubuntu 24 prereqs script creates a venv for this reason (although the Ubuntu 22 script doesn't for some reason), but there are other reasons not to pip install as root, I'll discuss with the internal team.
> 
> > 2. ... However in WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22 there is no branch checked out. Git says "no branch".
> 
> I see this as well, on my end I think it's because MIOpen is failing to sync. Looking into this.
> 
> > 3. In directory WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22 are two versions of the install prerequisites shell script
> 
> The version with the typo is from the ubuntu22 directory, the one without is from the ubuntu24 directory; see the file structure at https://github.com/ROCm/ROCm/tree/develop/tools/rocm-build/docker. These are in their proper directories on my end. You should use the one which corresponds to your OS, which is the typoed version. As for why this has a typo in the first place, this was added for 6.4 ([295e1e2#diff-bb92fcc28803a2cb8ce4028272460f1a67ba7248d56426182e2cb89b78cbd93b](https://github.com/ROCm/ROCm/commit/295e1e2998f206948c84b5936e008a1a22460e87#diff-bb92fcc28803a2cb8ce4028272460f1a67ba7248d56426182e2cb89b78cbd93b)), I'll be checking in regarding that.
> 

If one clones the repo this is what one gets. IDK how anyone is supposed to know about the file you reference.


> > 4. This absolute gem:
> 
> These instructions are for the Docker container, although to be fair we don't provide an alternative instruction here for baremetal installation. This is potentially still problematic inside a Docker if a non-default user is required for whatever reason.
> 
> > 5. ... how about posting a detailed instruction on building ROCm?
> 
> I'd suggest either trying these instructions in a Docker or just installing with one of our other methods at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/index.html. If there isn't a specific reason to build from source on baremetal I would avoid doing so as there are easier ways.

IDK quite what to say at this point. 

> Hi [@emerth](https://github.com/emerth), first of all this isn't actually a build script. Notice there's no actual version-specific branching being done in e.g.
> 
> ```
> # Option 1: Start a docker container
> # Pulling required base docker images:
> # Ubuntu22.04 built from ROCm/tools/rocm-build/docker/ubuntu22/Dockerfile
> docker pull rocm/rocm-build-ubuntu-22.04:6.4
> # Ubuntu24.04 built from ROCm/tools/rocm-build/docker/ubuntu24/Dockerfile
> docker pull rocm/rocm-build-ubuntu-24.04:6.4
> ```
> 
> so running this as-is will not work.


So take a look at `Option 2: Install required packages into the host machine`. I should have been more clear I am not using Docker I am using the instructions in that not-script for bare metal.

If the balance of the not-a-script is all for Docker then get rid of the Option 2 chunk because it is very misleading.

> 
> > 1. ... Running pip install as root clobbers system packages, is generally a bad idea.
> 
> Fair. The Ubuntu 24 prereqs script creates a venv for this reason (although the Ubuntu 22 script doesn't for some reason), but there are other reasons not to pip install as root, I'll discuss with the internal team.
> 
> > 2. ... However in WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22 there is no branch checked out. Git says "no branch".
> 
> I see this as well, on my end I think it's because MIOpen is failing to sync. Looking into this.
> 
> > 3. In directory WORKSPACE/ROCm/tools/rocm-build/docker/ubuntu22 are two versions of the install prerequisites shell script
> 
> The version with the typo is from the ubuntu22 directory, the one without is from the ubuntu24 directory; see the file structure at https://github.com/ROCm/ROCm/tree/develop/tools/rocm-build/docker. These are in their proper directories on my end. You should use the one which corresponds to your OS, which is the typoed version. As for why this has a typo in the first place, this was added for 6.4 ([295e1e2#diff-bb92fcc28803a2cb8ce4028272460f1a67ba7248d56426182e2cb89b78cbd93b](https://github.com/ROCm/ROCm/commit/295e1e2998f206948c84b5936e008a1a22460e87#diff-bb92fcc28803a2cb8ce4028272460f1a67ba7248d56426182e2cb89b78cbd93b)), I'll be checking in regarding that.
> 

I checked out the 24.04 branch and also the 22.04 branch to check... the files were the same either way.

> > 4. This absolute gem:
> 
> These instructions are for the Docker container, although to be fair we don't provide an alternative instruction here for baremetal installation. This is potentially still problematic inside a Docker if a non-default user is required for whatever reason.
> 

Again, the balance of the not-a-script indicate nothing about being only for Docker. Misleading.

> > 5. ... how about posting a detailed instruction on building ROCm?
> 
> I'd suggest either trying these instructions in a Docker or just installing with one of our other methods at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/index.html. If there isn't a specific reason to build from source on baremetal I would avoid doing so as there are easier ways.

Can't really see why building it in Docker would work any better. The only Docker related thing you've mentioned is clobbering the ownership of /opt and ~. Everything else I have brought up will be as much an issue in Docker as out.

IDK really what to say at this point. You people tout ROCm as entirely open source, but building it is more or less impossible - has always been so since I first started using it six odd years ago. It is so hard to build ROCm that AMD's stock answer is more or less "Use our prebuilt binaries".  

Why do I want to build it?

I have a Radeon Pro VII, ROCm 6.4.0 dropped the gfx906 files, my Radeon Pro VII won't work with ROCm 6.4.0.

I have a 9070xt, enough parts of 6.4.0 ship without complete support that it won't work either. 

Ultimately I want Pytorch to run on ROCm on a 9070xt.  Which means 6.4.0 as a starting point because Pytorch is shipping 6.2.4 libs.

So I try to build it myself to see if I can get gfx1201 support in all the bits and pieces, and nowhere on AMD can I find a set of instructions that actually are consistent. I can find several sets of instructions that are inconsistent, misleading or just wrong though. Heck, I can't even find a description of the dependencies amongst the major parts of ROCm.

AMD should close source this until either AMD can see it's way to supporting the hardware on the shelf or AMD can generate coherent build instructions. The situation as it stands invites people into a vortex of confusion and frustration. 


---

### 评论 #4 — schung-amd (2025-04-15T15:25:55Z)

> If one clones the repo this is what one gets. IDK how anyone is supposed to know about the file you reference.
> I checked out the 24.04 branch and also the 22.04 branch to check... the files were the same either way.

Don't see this on my end at all, repo init and repo sync give me the proper file structure. Not sure what you mean by the 24.04 and 22.04 branch here. When I make a new folder and just do

```
repo init -u http://github.com/ROCm/ROCm.git -b roc-6.4.x -m tools/rocm-build/rocm-6.4.0.xml
repo sync
```
I get
```
rocm@rocm-System-Product-Name:~/ROCm-pull-test$ dir ROCm/tools/rocm-build/docker/ubuntu22
Dockerfile  install-prerequisities.sh  local-pin-600  packages  README.md
rocm@rocm-System-Product-Name:~/ROCm-pull-test$ dir ROCm/tools/rocm-build/docker/ubuntu24
Dockerfile  install-prerequisites.sh  local-pin-600  packages  README.md
```

> building it is more or less impossible

I share your frustration on the difficulty of building from source. The build scripts we publish are based on internal CI scripts and are more like "this is how we build ROCm" rather than "this is how you can build ROCm yourself". There are other issues as well, such as hardcoded distro support, which can make using these scripts cumbersome in some cases.

To make building from source more sane, we're working on TheRock: https://github.com/ROCm/TheRock/. From https://github.com/ROCm/TheRock/blob/main/cmake/therock_amdgpu_targets.cmake this should support both the Radeon VII and the 9070, so you can give this a try.

---

### 评论 #5 — ObiWahn (2025-05-24T17:01:20Z)

I have even trouble with the repo tool as is is not able to checkout rocm 6.4.1 which is currently the latest tag of the main repo. Myabe you need to redo some of the build stuff to get something straight again.

Most extra tools suck:
 - I hate the one invented by the company i work for
 -  gyp for google v8 sucked
 - mozilla firefox/thunderbird scripts sucked
 - this repo tool is not even able to checkout the current tag, and therefor your build is no exception.

I would suggest to just use git. no big objects have them as extra download. With CMake you can even use FetchContent that can handle git repos, zips whatever you need. It would be good if most code is actually C/C++.

Try to avoid being distribution speific (having packages for a certain set of distributions is ok/good), but people should be able to build wherever they want.  CMake's find modules / pkg-config should really suffice to find all libraries people need.

Do no use sudo or chown in your build scripts. Fucking up other peoples systems is never good. Provide a list of dependencies or maybe small easy to read distribution specific scripts that pull in the requirements. Scripts people need to execute as root should have a size that can be easily be read and understood by humans. Keep build and fetching of the requirements apart!

Do not mix build and packaging. I have seen it uncountable times, that people mix this and it is always a mess. Divide and make the build great again! Why? Because the developers will love it the tooling becomes less complex. Packages belong imo mostly in the CI and will most probably be distribution specific if they are worth anything.

I am wiling to help with some smaller module at time if you are interested in the CMake way. But I will most probably need some helpm, as I lack the time to completely read through your whole build in a way that allows me to to sidestep all pitfalls.

---

### 评论 #6 — stellaraccident (2025-06-10T03:35:07Z)

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
