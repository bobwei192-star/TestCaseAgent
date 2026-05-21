# [Feature]: Support and or Instructions for Debian

> **Issue #2646**
> **状态**: closed
> **创建时间**: 2023-11-15T19:59:14Z
> **更新时间**: 2025-12-01T18:11:36Z
> **关闭时间**: 2025-01-23T16:24:33Z
> **作者**: tinfoil-hat-net
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/2646

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

Hi, on the Documentation are Instructions for how to install ROCm on Ubuntu. There is a PPA for Ubuntu, but not for Debian. I and other Debian Users, would benefit for a Debian apt mirror. I fear a dependecy hell, by installing via the Ubuntu PPA. If there is a save way to install ROCm on Debian, there should be some instructions in Documentation.

Cheers
     - tinfoil-hat

### Operating System

Debian

---

## 评论 (34 条)

### 评论 #1 — supersonictw (2023-11-16T05:22:10Z)

It seems to be working in progress the support of Debian and its derivatives...

I hope it will to be work, it helps most of dpkg/apt distro with installing AMD ROCm easier.

https://news.ycombinator.com/item?id=37663194

---

### 评论 #2 — supersonictw (2023-11-16T05:35:55Z)

Some ROCm suites are ready and available on [the repository of Debian](https://packages.debian.org/search?lang=en&suite=bookworm&searchon=names&keywords=rocm),

![圖片](https://github.com/RadeonOpenCompute/ROCm/assets/13705584/e02562bf-2e7f-487b-a653-5d794f5f2c69)

but `librccl.so` or something likes is still in Debian sid.

```
ImportError: librccl.so.1: cannot open shared object file: No such file or directory
```

You can take ROCm with docker if you can't wait for the packages ready, but the Docker image will cost you a lot of disk spaces.

```sh
#!/bin/sh

echo "Tensorflow with AMD ROCm"
echo "==="
docker run -it \
    -e PIP_ROOT_USER_ACTION=ignore \
    -e HSA_OVERRIDE_GFX_VERSION=10.3.0 \
    -v $PWD:/root/place \
    --ipc=host \
    --shm-size 16G \
    --device=/dev/kfd \
    --device=/dev/dri \
    --group-add video \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    rocm/tensorflow:latest \
    sh -c "cd /root/place && pip install -Uq pip ipython && ipython"
```

```sh
#!/bin/sh

echo "PyTorch with AMD ROCm"
echo "==="
docker run -it \
    -e PIP_ROOT_USER_ACTION=ignore \
    -e HSA_OVERRIDE_GFX_VERSION=10.3.0 \
    -v $PWD:/root/place \
    --ipc=host \
    --shm-size 16G \
    --device=/dev/kfd \
    --device=/dev/dri \
    --group-add video \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    rocm/pytorch:latest \
    sh -c "cd /root/place && pip install -Uq pip ipython && ipython"
```

Anyway, Debian needs the native ROCm, it won't let us down. And I have to say, AMD Yes!

---

### 评论 #3 — supersonictw (2023-11-16T05:40:22Z)

My card is `gfx1031` which needs to override as `gfx1030`.
The `HSA_OVERRIDE_GFX_VERSION` can be set you need.

---

### 评论 #4 — tinfoil-hat-net (2023-11-16T14:35:26Z)

> Some ROCm suites are ready and available on [the repository of Debian](https://packages.debian.org/search?lang=en&suite=bookworm&searchon=names&keywords=rocm),
> 
> ![圖片](https://user-images.githubusercontent.com/13705584/283330879-e02562bf-2e7f-487b-a653-5d794f5f2c69.png)
> 
> but `librccl.so` or something likes is still in Debian sid.
> 
> ```
> ImportError: librccl.so.1: cannot open shared object file: No such file or directory
> ```
> 
> You can take ROCm with docker if you can't wait for the packages ready, but the Docker image will cost you a lot of disk spaces.
> 
> ```shell
> #!/bin/sh
> 
> echo "Tensorflow with AMD ROCm"
> echo "==="
> docker run -it \
>     -e PIP_ROOT_USER_ACTION=ignore \
>     -e HSA_OVERRIDE_GFX_VERSION=10.3.0 \
>     -v $PWD:/root/place \
>     --ipc=host \
>     --shm-size 16G \
>     --device=/dev/kfd \
>     --device=/dev/dri \
>     --group-add video \
>     --cap-add=SYS_PTRACE \
>     --security-opt seccomp=unconfined \
>     rocm/tensorflow:latest \
>     sh -c "cd /root/place && pip install -Uq pip ipython && ipython"
> ```
> 
> ```shell
> #!/bin/sh
> 
> echo "PyTorch with AMD ROCm"
> echo "==="
> docker run -it \
>     -e PIP_ROOT_USER_ACTION=ignore \
>     -e HSA_OVERRIDE_GFX_VERSION=10.3.0 \
>     -v $PWD:/root/place \
>     --ipc=host \
>     --shm-size 16G \
>     --device=/dev/kfd \
>     --device=/dev/dri \
>     --group-add video \
>     --cap-add=SYS_PTRACE \
>     --security-opt seccomp=unconfined \
>     rocm/pytorch:latest \
>     sh -c "cd /root/place && pip install -Uq pip ipython && ipython"
> ```
> 
> Anyway, Debian needs the native ROCm, it won't let us down. And I have to say, AMD Yes!

Wouldn't it make more sense to use it with Distrobox, instead with Docker?

---

### 评论 #5 — supersonictw (2023-11-17T03:19:02Z)

> > Some ROCm suites are ready and available on [the repository of Debian](https://packages.debian.org/search?lang=en&suite=bookworm&searchon=names&keywords=rocm),
> > ![圖片](https://user-images.githubusercontent.com/13705584/283330879-e02562bf-2e7f-487b-a653-5d794f5f2c69.png)
> > but `librccl.so` or something likes is still in Debian sid.
> > ```
> > ImportError: librccl.so.1: cannot open shared object file: No such file or directory
> > ```
> > 
> > 
> >     
> >       
> >     
> > 
> >       
> >     
> > 
> >     
> >   
> > You can take ROCm with docker if you can't wait for the packages ready, but the Docker image will cost you a lot of disk spaces.
> > ```shell
> > #!/bin/sh
> > 
> > echo "Tensorflow with AMD ROCm"
> > echo "==="
> > docker run -it \
> >     -e PIP_ROOT_USER_ACTION=ignore \
> >     -e HSA_OVERRIDE_GFX_VERSION=10.3.0 \
> >     -v $PWD:/root/place \
> >     --ipc=host \
> >     --shm-size 16G \
> >     --device=/dev/kfd \
> >     --device=/dev/dri \
> >     --group-add video \
> >     --cap-add=SYS_PTRACE \
> >     --security-opt seccomp=unconfined \
> >     rocm/tensorflow:latest \
> >     sh -c "cd /root/place && pip install -Uq pip ipython && ipython"
> > ```
> > 
> > 
> >     
> >       
> >     
> > 
> >       
> >     
> > 
> >     
> >   
> > ```shell
> > #!/bin/sh
> > 
> > echo "PyTorch with AMD ROCm"
> > echo "==="
> > docker run -it \
> >     -e PIP_ROOT_USER_ACTION=ignore \
> >     -e HSA_OVERRIDE_GFX_VERSION=10.3.0 \
> >     -v $PWD:/root/place \
> >     --ipc=host \
> >     --shm-size 16G \
> >     --device=/dev/kfd \
> >     --device=/dev/dri \
> >     --group-add video \
> >     --cap-add=SYS_PTRACE \
> >     --security-opt seccomp=unconfined \
> >     rocm/pytorch:latest \
> >     sh -c "cd /root/place && pip install -Uq pip ipython && ipython"
> > ```
> > 
> > 
> >     
> >       
> >     
> > 
> >       
> >     
> > 
> >     
> >   
> > Anyway, Debian needs the native ROCm, it won't let us down. And I have to say, AMD Yes!
> 
> Wouldn't it make more sense to use it with Distrobox, instead with Docker?

Umm... It's just an example, you can try other flavor if it works.

---

### 评论 #6 — supersonictw (2023-11-19T19:20:07Z)

`chroot` works, I use the scripts eventually.

https://github.com/supersonictw/uruha

Hoping Debian 12/13 will work along with ROCm natively someday.

---

### 评论 #7 — nairboon (2024-01-02T13:22:32Z)

it can be installed on debian bookworm with the amdgpu-install tool: https://blog.moubou.com/2023/11/install-amd-rocm-on-debian-bookworm/

---

### 评论 #8 — supersonictw (2024-01-15T04:19:01Z)

> it can be installed on debian bookworm with the amdgpu-install tool: https://blog.moubou.com/2023/11/install-amd-rocm-on-debian-bookworm/

~~The article said `ROCm only supports Python 3.10`, but it seems Python 3.11 is working on my Debian 12 with ROCm 5.7.~~

---

### 评论 #9 — nairboon (2024-01-15T07:33:01Z)

> The article said `ROCm only supports Python 3.10`, but it seems Python 3.11 is working on my Debian 12 with ROCm 5.7.

That's good to know. 
I remember having to install python3.10 for some reason. Maybe it was to get Pytorch with ROCm running...


---

### 评论 #10 — supersonictw (2024-01-15T14:40:42Z)

> > ~~The article said `ROCm only supports Python 3.10`, but it seems Python 3.11 is working on my Debian 12 with ROCm 5.7.~~
> 
> That's good to know. I remember having to install python3.10 for some reason. Maybe it was to get Pytorch with ROCm running...

I'm sorry that I try it on another clean Debian after the reply, the method will cause
```
The following packages have unmet dependencies:
 rocm-gdb : Depends: libpython3.10 but it is not installable or
                     libpython3.8 but it is not installable
E: Unable to correct problems, you have held broken packages
```

It seems will be broken due to the system dependencies.

---

### 评论 #11 — Escain (2024-02-16T15:50:18Z)

Exactly the same issue there trying to install rocm on Debian 12 (or PyTorch).
Y have Python 3.11

```
The following packages have unmet dependencies:
 rocm-gdb : Depends: libpython3.10 but it is not installable or
                     libpython3.8 but it is not installable
E: Unable to correct problems, you have held broken packages
```

---

### 评论 #12 — Escain (2024-02-17T09:51:42Z)

I found a "hack" that make it work:

This is a simplified procedure, I recommend understanding each line, creating folders when required, etc.

**1) Build python3.10**
wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz
tar -xf Python-3.10.*.tgz
cd Python-3.10.*/
./configure --prefix=/usr/local --enable-optimizations --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make -j $(nproc)
sudo make altinstall

**2) Create a dummy deb to mark the dependency as installed**
sudo apt-get install equivs
equivs-control libpython3.10.control
nano libpython3.10.control


Section: misc
Priority: optional
Standards-Version: 3.9.2

```
Package: libpython3.10
Version: 3.10.1-1
Description: Dummy package for manually installed libpython3.10
 This is a dummy package created to satisfy dependencies for libpython3.10.
 ```
 equivs-build libpython3.10.control
 sudo dpkg -i libpython3.10_3.10.1-1_all.deb
 
 **3) Install rocm**
 amdgpu-install --usecase=rocm
 
 
 Disclaim: It's obviously a temporary patch, that should be uninstalled and fixed as soon as possible.
 
 

---

### 评论 #13 — nairboon (2024-02-20T13:34:53Z)


> **1) Build python3.10**

You can also simply install the python3.10 package from sid as explained in the link above.

---

### 评论 #14 — inneroot (2024-03-15T21:47:13Z)

> I found a "hack" that make it work:

thx a lot, was able to install rocm on Debian 12

---

### 评论 #15 — inneroot (2024-03-16T08:25:26Z)

Found that after reboot  drivers for RX 6900XT stop working. Timeshifted back and now i see that as soon as i install  `sudo amdgpu-install --usecase=dkms` and reboot, drivers broken, if no reboot everything works fine. ` sudo amdgpu-uninstall` fixing it to preinstall working state. Its funny that before i reboot i could use ollama and stable-diffusion perfectly :) but after reboot - gpu not found.

---

### 评论 #16 — supersonictw (2024-05-01T10:58:24Z)

In fact, if you just want to use pytorch.
The thing you only need to do is installing it with the command from pytorch.org to be like:

```sh
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0
```

PyTorch will be working without any extra system dependencies (no /opt/rocm).

> this comment is just hoping to tip someone who doesn't know it.

---

### 评论 #17 — supersonictw (2024-05-01T11:08:23Z)

> as soon as i install `sudo amdgpu-install --usecase=dkms`

DKMS is not compatible with Debian. Don't use it.

---

### 评论 #18 — nairboon (2024-05-18T12:20:23Z)

> Found that after reboot drivers for RX 6900XT stop working. Timeshifted back and now i see that as soon as i install `sudo amdgpu-install --usecase=dkms` and reboot, drivers broken, if no reboot everything works fine. ` sudo amdgpu-uninstall` fixing it to preinstall working state. Its funny that before i reboot i could use ollama and stable-diffusion perfectly :) but after reboot - gpu not found.

What happens if you run
`sudo amdgpu-install --usecase=graphics,dkms`
to also install the graphic drivers this way?

---

### 评论 #19 — harkgill-amd (2025-01-23T16:24:33Z)

Hi @tinfoil-hat-net, with the release of ROCm 6.3.1, ROCm now supports Debian! You can find the relevant installation instructions under the [quick start installation guide](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.3.1/install/quick-start.html).

---

### 评论 #20 — supersonictw (2025-01-23T16:38:48Z)

I'm glad to hear the great news.
Thanks AMD ROCm Team for Debian supporting. 😊

Thank you very much. 🎊🎊🎊

---

### 评论 #21 — tinfoil-hat-net (2025-01-23T16:38:48Z)

Awesome! Thank you!!! 

---

### 评论 #22 — cyclops1982 (2025-02-12T19:46:50Z)

> Hi [@tinfoil-hat-net](https://github.com/tinfoil-hat-net), with the release of ROCm 6.3.1, ROCm now supports Debian! You can find the relevant installation instructions under the [quick start installation guide](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.3.1/install/quick-start.html).

This is great!
But do i understand correctly that the[ debian install only ](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.3.1/reference/system-requirements.html#single-node) supports AMD Instinct MI300X  ?

I'm on a AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics and would love some better ollama speed.

---

### 评论 #23 — harkgill-amd (2025-02-12T20:02:28Z)

While this is true for official support, many users have successfully gotten ROCm 6.3.2 working with Navi3X and other SKUs running Debian 12. I would suggest giving it a try on your machine as well and creating an issue if you encounter any difficulties. While I can't guarantee it'll work on your iGPU, we'll try our best to enable as much functionality as possible.

---

### 评论 #24 — omerguzelelectronicguy (2025-02-16T20:09:59Z)

> Hi [@tinfoil-hat-net](https://github.com/tinfoil-hat-net), with the release of ROCm 6.3.1, ROCm now supports Debian! You can find the relevant installation instructions under the [quick start installation guide](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.3.1/install/quick-start.html).

Thank you @harkgill-amd . I continue to some part but it tells:
```
The following additional packages will be installed:
  amd-smi-lib amdgpu-core amdgpu-dkms-firmware comgr composablekernel-dev dkms g++-12-multilib g++-multilib gcc-11-base gcc-12-multilib gcc-multilib half hip-dev hip-doc
  hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev
  hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev lib32asan8 lib32atomic1
  lib32gcc-12-dev lib32gcc-s1 lib32gomp1 lib32itm1 lib32quadmath0 lib32stdc++-12-dev lib32stdc++6 lib32ubsan1 libasan6 libc6-dev-i386 libc6-dev-x32 libc6-i386 libc6-x32
  libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm-amdgpu-dev libdrm-amdgpu-radeon1 libdrm2-amdgpu libelf-dev libfile-copy-recursive-perl libfile-which-perl libgcc-11-dev
  libncurses-dev libnuma-dev libstdc++-11-dev libtinfo-dev libtsan0 libx32asan8 libx32atomic1 libx32gcc-12-dev libx32gcc-s1 libx32gomp1 libx32itm1 libx32quadmath0
  libx32stdc++-12-dev libx32stdc++6 libx32ubsan1 libxml2-dev linux-headers-amd64 mesa-common-dev migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev
  openmp-extras-dev openmp-extras-runtime python3-argcomplete rccl rccl-dev rocalution rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm-cmake rocm-core rocm-dbgapi
  rocm-debug-agent rocm-developer-tools rocm-device-libs rocm-gdb rocm-hip-libraries rocm-hip-runtime rocm-hip-runtime-dev rocm-hip-sdk rocm-language-runtime rocm-llvm
  rocm-ml-libraries rocm-ml-sdk rocm-opencl rocm-opencl-dev rocm-opencl-runtime rocm-opencl-sdk rocm-openmp-sdk rocm-smi-lib rocm-utils rocminfo rocprim-dev rocprofiler
  rocprofiler-dev rocprofiler-plugins rocprofiler-register rocprofiler-sdk rocprofiler-sdk-roctx rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev
  rocthrust-dev roctracer roctracer-dev rocwmma-dev rpp rpp-dev
Suggested packages:
  menu lib32stdc++6-12-dbg libx32stdc++6-12-dbg ncurses-doc libstdc++-11-doc
The following NEW packages will be installed:
  amd-smi-lib amdgpu-core amdgpu-dkms amdgpu-dkms-firmware comgr composablekernel-dev dkms g++-12-multilib g++-multilib gcc-11-base gcc-12-multilib gcc-multilib half hip-dev
  hip-doc hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand
  hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev lib32asan8
  lib32atomic1 lib32gcc-12-dev lib32gcc-s1 lib32gomp1 lib32itm1 lib32quadmath0 lib32stdc++-12-dev lib32stdc++6 lib32ubsan1 libasan6 libc6-dev-i386 libc6-dev-x32 libc6-i386
  libc6-x32 libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm-amdgpu-dev libdrm-amdgpu-radeon1 libdrm2-amdgpu libelf-dev libfile-copy-recursive-perl libfile-which-perl
  libgcc-11-dev libncurses-dev libnuma-dev libstdc++-11-dev libtinfo-dev libtsan0 libx32asan8 libx32atomic1 libx32gcc-12-dev libx32gcc-s1 libx32gomp1 libx32itm1
  libx32quadmath0 libx32stdc++-12-dev libx32stdc++6 libx32ubsan1 libxml2-dev linux-headers-amd64 mesa-common-dev migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx
  mivisionx-dev openmp-extras-dev openmp-extras-runtime python3-argcomplete rccl rccl-dev rocalution rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm rocm-cmake
  rocm-core rocm-dbgapi rocm-debug-agent rocm-developer-tools rocm-device-libs rocm-gdb rocm-hip-libraries rocm-hip-runtime rocm-hip-runtime-dev rocm-hip-sdk
  rocm-language-runtime rocm-llvm rocm-ml-libraries rocm-ml-sdk rocm-opencl rocm-opencl-dev rocm-opencl-runtime rocm-opencl-sdk rocm-openmp-sdk rocm-smi-lib rocm-utils
  rocminfo rocprim-dev rocprofiler rocprofiler-dev rocprofiler-plugins rocprofiler-register rocprofiler-sdk rocprofiler-sdk-roctx rocrand rocrand-dev rocsolver rocsolver-dev
  rocsparse rocsparse-dev rocthrust-dev roctracer roctracer-dev rocwmma-dev rpp rpp-dev
0 upgraded, 143 newly installed, 0 to remove and 0 not upgraded.
Need to get 2,826 MB of archives.
After this operation, 35.4 GB of additional disk space will be used.
Do you want to continue? [Y/n]
```
Is this a expected behaviour? I am using `debian12`

---

### 评论 #25 — antwal (2025-02-27T17:58:45Z)

Hi @harkgill-amd, I have several docker servers using "AMD Ryzen 9 6900HX with Radeon Graphics"

`e5:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Rembrandt [Radeon 680M] [1002:1681] (rev c7)`

are these supported to use the gpu or is it a test to do and evaluate if it works. 
all have debian 12. 

Thanks


---

### 评论 #26 — harkgill-amd (2025-02-27T18:34:49Z)

@omerguzelelectronicguy, that's the standard behaviour for the apt installation. From there, you can proceed with the installation by pressing the 'Y' key or simply 'Enter'.

@antwal ROCm does not currently support iGPUs, including the Rembrandt series, as highlighted [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#disable-integrated-graphics-igp-if-applicable). This will likely result in limited functionality but it's best to give it a try and confirm if your use case is still functional. Feel free to open an issue if you run into any errors.

---

### 评论 #27 — cgmb (2025-02-27T22:08:36Z)

@antwal, the Debian Project purchased a Rembrandt system for the Debian ROCm Team's continuous integration system. During an update from ROCm 5.2 to ROCm 5.7, it identified a regression in ROCr on Rembrandt (https://github.com/ROCm/ROCR-Runtime/issues/262#issuecomment-2504541369). Anyone who has donated funds to the Debian project deserves a big thank you for helping to spot that bug!

I know the bug has been [patched](https://salsa.debian.org/rocm-team/rocr-runtime/-/blob/debian/6.1.2-3/debian/patches/0006-initialize-chip-revision.patch?ref_type=tags) in the ROCm packages provided by Debian, but I'm unsure of if the ROCm packages provided by AMD have been fixed. To use the AMD-provided packages on gfx1035 hardware, you might have to set `export HSA_OVERRIDE_GFX_VERSION=10.3.0` in your environment.

ROCm does not officially support Rembrandt, but I've run the tests for all the ROCm mathlibs available on Debian and they pass without any notable issues. It seems to work fine to me, although I haven't tried using it for any applications. It helps if you use a recent kernel, as there were updates in Linux 6.11 that allowed ROCm on APUs to allocate more memory.

---

### 评论 #28 — antwal (2025-02-28T08:25:44Z)

hi @harkgill-amd, @cgmb I did some tests, updating debian 12 to the latest kernel version, the graphics card is recognized and starting pytorch gives a positive result also for cuda; however starting the tests generates several errors. I'm trying to figure out if they can be solved by installing rocm.

---

### 评论 #29 — omerguzelelectronicguy (2025-03-03T10:27:20Z)

>@omerguzelelectronicguy, that's the standard behaviour for the apt installation. From there, you can proceed with the installation by pressing the 'Y' key or simply 'Enter'.


@harkgill-amd I just wanted to use my amd gpu in blender. Is there any other small installation for only that purpose?

---

### 评论 #30 — antwal (2025-03-03T16:10:14Z)

@omerguzelelectronicguy I tried on my test machine via docker and using the linuxserver/blender container the GPU works perfectly

for the other problems with pytorch I solved almost everything without upsetting the system

---

### 评论 #31 — harkgill-amd (2025-03-03T18:01:45Z)

> [@harkgill-amd](https://github.com/harkgill-amd) I just wanted to use my amd gpu in blender. Is there any other small installation for only that purpose?

You can find a list of available meta packages for ROCm under [Packages in ROCm programming models](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/package-manager-integration.html#packages-in-rocm-programming-models). These help modularize the complete ROCm installation and can be installed individually. 

For Blender, you only need to install the rocm-hip-sdk package.

---

### 评论 #32 — omerguzelelectronicguy (2025-03-08T12:22:46Z)

> [@omerguzelelectronicguy](https://github.com/omerguzelelectronicguy) I tried on my test machine via docker and using the linuxserver/blender container the GPU works perfectly
> 
> for the other problems with pytorch I solved almost everything without upsetting the system


@antwal Can you explain how you opened docker. I couldn't open linuxserver/blender. 

I also used below commands but I still couldn't see my GPU in blender as HIP device.
```
# I created image with Dockerfile
$ cat  Dockerfile
FROM debian:bookworm

# Install dependencies and Blender
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    blender \
    x11-apps \
    mesa-utils \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV DISPLAY=:0

# Create a non-root user (optional but recommended)
RUN useradd -m blenderuser
USER blenderuser
WORKDIR /home/blenderuser

# Set the entrypoint to Blender
ENTRYPOINT ["blender"]

$ podman build -t blender-debian:bookworm .
$ podman run -it --rm   --name blender-container   --net=host   -e DISPLAY=$DISPLAY   -v /tmp/.X11-unix:/tmp/.X11-unix   -v /dev/dri:/dev/dri   -v "$PWD:/home//blender"   blender-debian:bookworm
```
Possiblly I have missing something but I couldn't understand?

Does docker uses the part that I couldn't install my system properly? or it has already that part and should work?

I also tried to install blender from flathub instead of apt-get but it didn't work too.

---

### 评论 #33 — antwal (2025-03-08T17:39:45Z)

@omerguzelelectronicguy I simply used 

`docker run -d --name=blender -e PGUI=1000 -e PGID=1000 -e TZ="Etc/UTC" -p 3000:3000 -p 3001:3001 -v /home/antwal/blender/config:/config --restart unless-stopped --privileged --device /dev/dri:/dev/dri lscr.io/linuxserver/blender:latest`

then from the browser I connected on port 3001, I loaded an old project that I had created on the Mac a few years ago and everything worked

---

### 评论 #34 — ianbmacdonald (2025-12-01T18:11:36Z)

https://github.com/ROCm/ROCm/issues/5671

---
