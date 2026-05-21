# Cannot access GPU inside docker images for PyTorch (and Tensorflow)

> **Issue #2741**
> **状态**: closed
> **创建时间**: 2023-12-17T16:57:53Z
> **更新时间**: 2023-12-18T20:14:30Z
> **关闭时间**: 2023-12-18T20:13:32Z
> **作者**: marcopigg
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2741

## 描述

**Problem Description**
I'm trying to install ROCm PyTorch on a fresh Ubuntu 22.04.3 install, following all the recommend steps in the [rocm installation page](https://rocm.docs.amd.com/en/docs-5.7.1/deploy/linux/installer/install.html) and using docker containers as specified [in the docs](https://rocm.docs.amd.com/en/docs-5.7.1/how_to/pytorch_install/pytorch_install.html) (Option 1):

However, no GPU is detected in the docker container: `cuda.is_available()` returns `False` and `rocminfo` doesen't detect the GPU.

You can find a detailed terminal session with all the commands and output [in this gist](https://gist.github.com/marcopigg/689eb21d01df5fbb7cd0c22d0bbcf40b) (I skipped the output from the initial install commands).

Note also that `docker run` doesn't work without the `--privileged` option.

I don't think the issue is in PyTorch as I have the same problem with the `rocm/tensorflow` containers. No GPU is passed to the docker image.

The iGPU is disabled in BIOS.

**Operating System**
Ubuntu 22.04.3

**CPU**
AMD Ryzen 7700X

**GPU**
AMD Radeon RX 7900 XTX

**ROCm Version**
5.7.1

EDIT: updated gist with docker version (24.0.7, build afdd53b)

---

## 评论 (3 条)

### 评论 #1 — baryluk (2023-12-18T02:07:32Z)

`docker version`, just for completes.  (You can edit existing post with output of it)


---

### 评论 #2 — baryluk (2023-12-18T02:10:07Z)

BTW. It works perfectly fine on Debian for me:

```
docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device=/dev/kfd --device=/dev/dri --group-add video --ipc=host --shm-size 8G rocm/pytorch:latest
...

...

  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1030         
      Machine Models:          HSA_MACHINE_MODEL_LARGE            
      Profiles:                HSA_PROFILE_BASE                   
      Default Rounding Mode:   NEAR                               
      Default Rounding Mode:   NEAR                               
      Fast f16:                TRUE                               
      Workgroup Max Size:      1024(0x400)                        
      Workgroup Max Size per Dimension:
        x                        1024(0x400)                        
        y                        1024(0x400)                        
        z                        1024(0x400)                        
      Grid Max Size:           4294967295(0xffffffff)             
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***             
root@37fc2cc36e1e:/var/lib/jenkins# python3 -c 'import torch; print(torch.cuda.is_available())'
True
root@37fc2cc36e1e:/var/lib/jenkins# 
```

with Radeon RX 6900 XT.  (not officially supported GPU tho). I am on a custom 6.7.0-rc4 kernel.



---

### 评论 #3 — marcopigg (2023-12-18T20:13:33Z)

I've done a few more tests:

- PyTorch works, i.e. runs [the mnist test](https://rocm.docs.amd.com/en/docs-5.7.1/how_to/pytorch_install/pytorch_install.html#run-a-basic-pytorch-example), using a python3 virtualenv with the rocm5.7 wheel package installed (using a local folder, not in docker)
- I've tried uninstalling docker desktop and installing the docker engine alone. Now the docker image works correctly (correct `rocminfo` display, etc.) but I have to prefix the initial `docker run` command with `sudo`

so I guess the issue is with Docker Desktop, maybe with the specific version I installed.

I'll mark this as closed for now, as the issue seems to be with the docker desktop application.

---
