# Can't install 5.7

> **Issue #4575**
> **状态**: closed
> **创建时间**: 2025-04-08T17:30:27Z
> **更新时间**: 2025-04-10T16:04:07Z
> **关闭时间**: 2025-04-10T16:04:07Z
> **作者**: Krytern
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4575

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

So I am trying to do a multi install on Ubuntu 22.04 (Jammy).

6.3.3 will install fine, but if I use `sudo apt install rocm5.7` then it can't find the package.

The following doesn't work either;
```
for ver in 6.3.3 5.7; do
    sudo apt install rocm$ver
done
```
If I remove the 6.3.3 from above, it still won't find 5.7

Here's my rocm.list file
```
deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.3.3 jammy main
deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/5.7 jammy main
```


Here is what I see if I type in `sudo apt update`
```
Hit:1 https://repo.radeon.com/amdgpu/6.3.3/ubuntu jammy InRelease
Hit:2 http://gb.archive.ubuntu.com/ubuntu jammy InRelease           
Hit:3 http://gb.archive.ubuntu.com/ubuntu jammy-updates InRelease                                                
Hit:4 https://esm.ubuntu.com/apps/ubuntu jammy-apps-security InRelease                                           
Hit:5 http://gb.archive.ubuntu.com/ubuntu jammy-backports InRelease                                              
Hit:6 https://esm.ubuntu.com/apps/ubuntu jammy-apps-updates InRelease                                            
Hit:7 https://esm.ubuntu.com/infra/ubuntu jammy-infra-security InRelease
Hit:8 http://security.ubuntu.com/ubuntu jammy-security InRelease    
Hit:9 https://esm.ubuntu.com/infra/ubuntu jammy-infra-updates InRelease
Hit:10 https://repo.radeon.com/rocm/apt/6.3.3 jammy InRelease
Hit:11 https://repo.radeon.com/rocm/apt/5.7 jammy InRelease
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
3 packages can be upgraded. Run 'apt list --upgradable' to see them.
```

---

## 评论 (8 条)

### 评论 #1 — ppanchad-amd (2025-04-08T18:06:35Z)

Hi @Krytern. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — Krytern (2025-04-08T18:25:31Z)

Thanks, here's my terminal when I try the final install step again;
```
ubuntu@desktop:~$ for ver in 6.3.3 5.7; do
    sudo apt install rocm$ver
done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
rocm6.3.3 is already the newest version (6.3.3.60303-74~22.04).
0 to upgrade, 0 to newly install, 0 to remove and 3 not to upgrade.
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package rocm5.7
E: Couldn't find any package by glob 'rocm5.7'
```

---

### 评论 #3 — schung-amd (2025-04-08T18:33:46Z)

Hi @Krytern, I don't think the `rocm` meta-package exists in ROCm 6.0 and earlier; you should use `rocm-hip-sdk` instead (i.e. `rocm-hip-sdk5.7` in this case) per the [5.7 installation instructions](https://rocm.docs.amd.com/en/docs-5.7.0/deploy/linux/os-native/install.html).

---

### 评论 #4 — Krytern (2025-04-08T20:21:28Z)

> Hi [@Krytern](https://github.com/Krytern), I don't think the `rocm` meta-package exists in ROCm 6.0 and earlier; you should use `rocm-hip-sdk` instead (i.e. `rocm-hip-sdk5.7` in this case) per the [5.7 installation instructions](https://rocm.docs.amd.com/en/docs-5.7.0/deploy/linux/os-native/install.html).

Hello, while it doesn't find a package for rocm-hip-sdk5.7 it does find 5.7 if I use rocm-hip-sdk but even when following the multi install instructions it wants to uninstall 6.3.3 before installing 5.7

---

### 评论 #5 — schung-amd (2025-04-08T20:42:17Z)

Won't have the resources to test on my end for a couple of days, but in the meanwhile I'd suggest uninstalling 6.3.3 and then trying to install 6.3.3 and 5.7 together with the 5.7 rocm-hip-sdk multi-version instructions. You can also try using the amdgpu installer rather than the package manager with `--rocmrelease=<release-number>` as it streamlines the multi-version installation: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/amdgpu-installer/amdgpu-installer-ubuntu.html; however I haven't tested this for such a large version gap either so this may have the same issue you're running into. Will update once I have a chance to test on my end.

---

### 评论 #6 — Krytern (2025-04-09T18:16:05Z)

> Won't have the resources to test on my end for a couple of days, but in the meanwhile I'd suggest uninstalling 6.3.3 and then trying to install 6.3.3 and 5.7 together with the 5.7 rocm-hip-sdk multi-version instructions. You can also try using the amdgpu installer rather than the package manager with `--rocmrelease=<release-number>` as it streamlines the multi-version installation: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/amdgpu-installer/amdgpu-installer-ubuntu.html; however I haven't tested this for such a large version gap either so this may have the same issue you're running into. Will update once I have a chance to test on my end.

Just gave those two methods a go and it finds 6.3.3 fine but just won't find 5.7, even though if I go to the link in the `rocm.list`file then the 5.7 link is definitely correct. Strange behavior not sure why the system won't find 5.7 unless it is being installed on it's own as the latest version.

EDIT: So for a sanity check I did a complete clean install of Ubuntu 22.04.5 and went to do a multi install of 6.3.3 alongside 6.1 since they aren't far apart just to see if it would work. It finds 6.3.3 but can't find 6.1 in the multi install, no matter what method I use. For whatever reason my system seems to be only able to find whatever the latest is that I set and that is on a fresh OS install so I am lost.

EDIT2: If I add 6.3.2 to my rocm.list file using the multi install instructions, it detects it and wants to install it just fine. 6.2.4 works as well, so maybe the issue starts when trying to install a version from 6.1.x and lower, unless it is the newest version being installed for multiinstall?

---

### 评论 #7 — Krytern (2025-04-10T15:16:34Z)

I've figured it out. The version numbers have to be written differently depending on what you're doing.

When adding the ROCm repositories it has to be written as "5.7"
When installing the packages it has to be written as "5.7.0"

Doing it the other way around doesn't work for either one. Here are the two commands that worked in installing 3 different versions of ROCm, 5.7 having to be a little different due to the name change;

```
for ver in 6.3.4 6.1 5.7; do
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/$ver jammy main" \
    | sudo tee --append /etc/apt/sources.list.d/rocm.list
done
echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' \
    | sudo tee /etc/apt/preferences.d/rocm-pin-600
sudo apt update
```
```
for ver in 6.3.4 6.1.0; do
    sudo apt install rocm$ver
done
for ver in 5.7.0; do
    sudo apt install rocm-hip-sdk$ver
done
```

---

### 评论 #8 — schung-amd (2025-04-10T15:44:46Z)

Interesting, glad you figured it out! Not sure why this is the case, something must have changed since 5.7 as those instructions don't have the the trailing .0:

> Sample Multi-version installation
> sudo apt install rocm-hip-sdk5.7 rocm-hip-sdk5.6.1 rocm-hip-sdk5.5.3

but I do see the .0 in the [6.3 install instructions](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.3.0/install/native-install/multi-version-install.html). Thanks for pointing this out, the multi-version install instructions should specify where the .0 is required. I'll forward this to the docs team.

---
