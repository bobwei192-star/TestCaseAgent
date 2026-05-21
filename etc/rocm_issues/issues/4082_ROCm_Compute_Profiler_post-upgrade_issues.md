# ROCm Compute Profiler post-upgrade issues

> **Issue #4082**
> **状态**: closed
> **创建时间**: 2024-12-03T22:19:32Z
> **更新时间**: 2025-03-16T07:14:10Z
> **关闭时间**: 2024-12-20T23:07:28Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4082

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.3.0** (颜色: #303737)

## 描述

In ROCm 6.3.0, the omniperf package is now named rocprofiler-compute. As a result, running `apt install omniperf` will fail to locate the package. Instead, use `apt install rocprofiler-compute`. See [ROCm Compute Profiler 3.0.0](https://rocm-stg.amd.com/en/latest/about/release-notes.html#rocm-compute-profiler-3-0-0).

When upgrading from ROCm 6.2 to 6.3, any existing `/opt/rocm-6.2/../omniperf` folders are not automatically removed. To clean up these folders, manually uninstall Omniperf using `apt remove omniperf`.

---

## 评论 (4 条)

### 评论 #1 — prbasyal-amd (2024-12-20T23:07:28Z)

Fixed in ROCm 6.3.1.

---

### 评论 #2 — yiakwy-xpu-ml-framework-team (2025-03-16T05:21:14Z)

@prbasyal-amd I can build rocprof-compute locally with ROCm 6.3.0 SDK, but cannot istall it from apt. I updated my apt sources to ROCm 6.3.3 but no lucky to install it from apt. Any hints ?

```
# details can be found in https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/native-install/ubuntu.html#installing
#                         https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-ubuntu.html

ROCM_VERSION=${ROCM_VERSION:-6.3.3}

# Make the directory if it doesn't exist yet.
# This location is recommended by the distribution maintainers.
# SIGNED_KEY_SAVE_DEST=/etc/apt/trusted.gpg.d # /etc/apt/keyrings
   SIGNED_KEY_SAVE_DEST=/etc/apt/keyrings
sudo mkdir --parents --mode=0755 $SIGNED_KEY_SAVE_DEST

# Add rocm repository

# Download the key, convert the signing-key to a full
# keyring required by apt and store in the keyring directory
if [ -d $SIGNED_KEY_SAVE_DEST ]; then
wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | \
    gpg --dearmor | sudo tee $SIGNED_KEY_SAVE_DEST/rocm.gpg > /dev/null
else
wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | apt-key add -
fi

# register kernel-mode driver
echo "deb [arch=amd64,i386 signed-by=$SIGNED_KEY_SAVE_DEST/rocm.gpg] https://repo.radeon.com/amdgpu/${ROCM_VERSION}/ubuntu jammy main" \
    | sudo tee /etc/apt/sources.list.d/amdgpu.list
sudo apt update

# add the ROCm repository.
echo "deb [arch=amd64 signed-by=$SIGNED_KEY_SAVE_DEST/rocm.gpg] https://repo.radeon.com/rocm/apt/${ROCM_VERSION} jammy main" \
    | sudo tee --append /etc/apt/sources.list.d/rocm.list
echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' \
    | sudo tee /etc/apt/preferences.d/rocm-pin-600
sudo apt update

sudo apt install -y rocm

```

---

### 评论 #3 — yiakwy-xpu-ml-framework-team (2025-03-16T05:22:14Z)

But I can do `apt install omniperf`:

```
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Note, selecting 'rocprofiler-compute' instead of 'omniperf'
rocprofiler-compute is already the newest version (3.0.0.60303-74~22.04).
The following packages were automatically installed and are no longer required:
  composablekernel-dev half hipcub-dev rccl rccl-dev
Use 'apt autoremove' to remove them.
0 upgraded, 0 newly installed, 0 to remove and 142 not upgraded. 
```

And if we also need to goto rocprofiler-compute (SDK 6.3.3) repo to install some python dependencies :

```
[ERROR] The 'astunparse==1.6.2' package was not found in the current execution environment.
[ERROR] The 'colorlover' package was not found in the current execution environment.
[ERROR] The 'dash>=1.12.0' package was not found in the current execution environment.
[ERROR] The 'matplotlib' package was not found in the current execution environment.
[ERROR] The 'pymongo' package was not found in the current execution environment.
[ERROR] The 'tabulate' package was not found in the current execution environment.
[ERROR] The 'dash-svg' package was not found in the current execution environment.
[ERROR] The 'dash-bootstrap-components' package was not found in the current execution environment.
[ERROR] The 'kaleido' package was not found in the current execution environment.
[ERROR] The 'plotille' package was not found in the current execution environment.
```

auxiliar_requirements.txt :

```
astunparse==1.6.2
colorlover
dash>=1.12.0 --no-deps
matplotlib
pymongo
tabulate
dash-svg
dash-bootstrap-components
dash-bootstrap-components --no-deps
kaleido
plotille
# used by GUI program
flask --no-deps
```

Besides the system requires locale : 

```
apt install locales
locale-gen "en_US.UTF-8"
```

After doing this, then we got :

```
$ /opt/rocm-6.3.3/bin/rocprof-compute --version
----------------------------------------
rocprofiler-compute version: 3.0.0 (release)
Git revision:     dc8dc2c3
----------------------------------------

```



---

### 评论 #4 — yiakwy-xpu-ml-framework-team (2025-03-16T05:55:46Z)

Is the function valid ?

<img width="1000" alt="Image" src="https://github.com/user-attachments/assets/29d372bf-ee77-4c2d-a46a-ec548f38054e" />

What is the plan in the future ?

I can see the details by scrolling down the screen:

<img width="700" alt="Image" src="https://github.com/user-attachments/assets/f7cf274f-0d72-43e7-84b8-93990ade0309" />

and

<img width="700" alt="Image" src="https://github.com/user-attachments/assets/c4cc406d-36d0-4b4e-9608-c56c4a02469a" />

---
