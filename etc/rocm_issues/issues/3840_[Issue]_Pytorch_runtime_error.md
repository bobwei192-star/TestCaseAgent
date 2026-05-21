# [Issue]: Pytorch runtime error

> **Issue #3840**
> **状态**: closed
> **创建时间**: 2024-09-30T21:42:15Z
> **更新时间**: 2025-01-20T19:11:52Z
> **关闭时间**: 2025-01-20T18:39:14Z
> **作者**: shifrin8101
> **标签**: Under Investigation, ROCm 5.7.1, AMD Radeon Pro W6800
> **URL**: https://github.com/ROCm/ROCm/issues/3840

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 5.7.1** (颜色: #ededed)
- **AMD Radeon Pro W6800** (颜色: #ededed)

## 描述

### Problem Description

Hello, my GPU output is:
03:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 33 [Radeon RX 7700S/7600/7600S/7600M XT/PRO W7600] (rev c0)

I installed with pytorch installation guide.
I have the following error:
ocBLAS error: Cannot read /home/mark/PycharmProjects/WSN-MA/venv/lib/python3.12/site-packages/torch/lib/rocblas/library/TensileLibrary.dat: Illegal seek

do not know how to proceed?

### Operating System

OS: NAME="Ubuntu" VERSION="24.04.1 LTS (Noble Numbat)"

### CPU

CPU:  model name	: Intel(R) Core(TM) i5-14400

### GPU

AMD Radeon Pro W6800

### ROCm Version

ROCm 5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (24 条)

### 评论 #1 — harkgill-amd (2024-10-01T14:56:06Z)

Hi @shifrin8101, while your GPU is not supported, you can try to set the environment variable `export HSA_OVERRIDE_GFX_VERSION=10.3.0` to mimic a supported architecture. This may allow you to workaround the rocBLAS error but please note that without a supported GPU, it will be difficult to debug any further issues that may arise.

---

### 评论 #2 — shifrin8101 (2024-10-01T15:13:29Z)

> Hi @shifrin8101, while your GPU is not supported, you can try to set the environment variable `export HSA_OVERRIDE_GFX_VERSION=10.3.0` to mimic a supported architecture. This may allow you to workaround the rocBLAS error but please note that without a supported GPU, it will be difficult to debug any further issues that may arise.

Will try and report here if worked, thanks!

---

### 评论 #3 — harkgill-amd (2024-10-15T20:00:26Z)

@shifrin8101, did you get a chance to try out the workaround?


---

### 评论 #4 — harkgill-amd (2024-10-18T14:02:01Z)

Closing this issue out. @shifrin8101, if you are still encountering issues after setting the HSA Override environment variables, please leave a comment and I will re-open this ticket. Thanks!

---

### 评论 #5 — shifrin8101 (2024-10-18T15:22:55Z)

Hi, I have not had a chance to get to my AMD desktop yet. Will have it in
the next few days, hopefully.
Will let you know, so it would take some patience please :)
Thanks!

‫בתאריך יום ו׳, 18 באוק׳ 2024 ב-17:02 מאת ‪harkgill-amd‬‏ <‪
***@***.***‬‏>:‬

> Closing this issue out. @shifrin8101 <https://github.com/shifrin8101>, if
> you are still encountering issues after setting the HSA Override
> environment variables, please leave a comment and I will re-open this
> ticket. Thanks!
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/3840#issuecomment-2422551223>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/BEE26YAFHWFRCLJVLUCYK5LZ4EIHBAVCNFSM6AAAAABPEIQYOSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDIMRSGU2TCMRSGM>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #6 — shifrin8101 (2024-10-18T18:07:11Z)

Hello,
at the moment I am seeing
Process finished with exit code 139 (interrupted by signal 11:SIGSEGV)
when trying to execute

w3_init = torch.randn(l3_params, 1)
b1_init = torch.randn(l2_params)
b2_init = torch.randn(l3_params)
b3_init = torch.randn(1)
try:
    self.W1 = w1_init.clone().detach().to(self.device).requires_grad_(True)
except Exception as e:
    print(f"An error occurred: {e}")

so I cannot even see the exception details, unfortunately.
No BLAS error, however. Still nothing was run yet. Is all in constructors.

‫בתאריך יום ו׳, 18 באוק׳ 2024 ב-18:22 מאת ‪Mark Shifrin‬‏ <‪
***@***.***‬‏>:‬

> Hi, I have not had a chance to get to my AMD desktop yet. Will have it in
> the next few days, hopefully.
> Will let you know, so it would take some patience please :)
> Thanks!
>
> ‫בתאריך יום ו׳, 18 באוק׳ 2024 ב-17:02 מאת ‪harkgill-amd‬‏ <‪
> ***@***.***‬‏>:‬
>
>> Closing this issue out. @shifrin8101 <https://github.com/shifrin8101>,
>> if you are still encountering issues after setting the HSA Override
>> environment variables, please leave a comment and I will re-open this
>> ticket. Thanks!
>>
>> —
>> Reply to this email directly, view it on GitHub
>> <https://github.com/ROCm/ROCm/issues/3840#issuecomment-2422551223>, or
>> unsubscribe
>> <https://github.com/notifications/unsubscribe-auth/BEE26YAFHWFRCLJVLUCYK5LZ4EIHBAVCNFSM6AAAAABPEIQYOSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDIMRSGU2TCMRSGM>
>> .
>> You are receiving this because you were mentioned.Message ID:
>> ***@***.***>
>>
>


---

### 评论 #7 — harkgill-amd (2024-10-18T20:23:16Z)

Upon re-examination, your setup has a Navi33 which is `gfx1102`. The HSA Override method works effectively on older GPUs such as Navi22 as the ISAs were identical (gfx1036 ISA is identical to gfx1030). With Navi33/gfx1102, the most relevant override would be to Navi31/gfx1100, but this still isn't guaranteed to work and not recommended as there are known differences between these two chips. 

I'll confirm if there are any other workarounds present for Navi33. In the meantime, could you please provide the complete sample program you are running so we can test this on our end as well?

---

### 评论 #8 — shifrin8101 (2024-10-19T21:36:41Z)

Here, this the simplest example which results  the latest error:
import torch

def get_device():  #start indent
    if torch.cuda.is_available():
        #device =  torch.cuda.get_device_name(0)
        device = torch.device(0)
        print(f'device name [0]:', torch.cuda.get_device_name(0), ' GPU is available')
    else:
        device = torch.device("cpu")
        print("GPU is not available. Using CPU.")
    return device
#end function end indent

device = get_device()
print(device)

torch.autograd.set_detect_anomaly(True)

w1_init = torch.randn(2, 2)
try:
    W1=w1_init.clone().detach().to(device).requires_grad_(True)
except Exception as e:
    print(f"An error occurred: {e}")

finished_sample=1

---

### 评论 #9 — shifrin8101 (2024-10-19T21:38:59Z)

for some reason the indentation wasn't kept, sorry

---

### 评论 #10 — harkgill-amd (2024-10-21T19:47:26Z)

I wasn't able to reproduce the error on my end with a Navi33, see the output of the sample below.
```
device name [0]: AMD Radeon RX 7600  GPU is available
cuda:0
```
Could you please try to run the sample on the rocm/pytorch docker image? You can launch a container with the image by utilizing the following commands:
```
docker pull rocm/pytorch:latest
docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
--device=/dev/kfd --device=/dev/dri --group-add video \
--ipc=host --shm-size 8G rocm/pytorch:latest
```
More information on setting up PyTorch with ROCm on Docker can be found [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html#using-a-docker-image-with-pytorch-pre-installed).

Also, try setting the `HIP_VISIBLE_DEVICES` environment variable at the beginning of your script with `os.environ['HIP_VISIBLE_DEVICES']='0'`. This will ensure that your dGPU is being targeted during execution.

---

### 评论 #11 — shifrin8101 (2024-10-24T10:13:14Z)

Hi,
Will try this during the following week, thanks a lot, meanwhile

On Mon, Oct 21, 2024, 10:47 PM harkgill-amd ***@***.***>
wrote:

> I wasn't able to reproduce the error on my end with a Navi33, see the
> output of the sample below.
>
> device name [0]: AMD Radeon RX 7600  GPU is available
> cuda:0
>
> Could you please try to run the sample on the rocm/pytorch docker image?
> You can launch a container with the image by utilizing the following
> commands:
>
> docker pull rocm/pytorch:latest
> docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
> --device=/dev/kfd --device=/dev/dri --group-add video \
> --ipc=host --shm-size 8G rocm/pytorch:latest
>
> Also, try setting the HIP_VISIBLE_DEVICES environment variable at the
> beginning of your script with os.environ['HIP_VISIBLE_DEVICES']='0'. This
> will ensure that your dGPU is being targeted during execution.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/3840#issuecomment-2427581864>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/BEE26YFWB5GLWAMZ3Q3FAATZ4VK6JAVCNFSM6AAAAABPEIQYOSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDIMRXGU4DCOBWGQ>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #12 — shifrin8101 (2024-11-13T06:06:35Z)

Hi sorry for the delay, I never tried anything with docker image before.

It actually writes:
sudo docker pulldocker pull rocm/pytorch:latest
docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
--device=/dev/kfd --device=/dev/dri --group-add video \
--ipc=host --shm-size 8G rocm/pytorch:latest
latest: Pulling from rocm/pytorch
Digest: sha256:54422bee895f9e44bc5257ab03011aae532c5b7cfa39dda00a3000c46db81239
Status: Image is up to date for rocm/pytorch:latest
docker.io/rocm/pytorch:latest
docker: unknown server OS: .
See 'docker run --help'.

So I am not sure I did the right thing. Also pleas note I am not running the pycharm with sudo (it cause me problems)
So getting back to you...

Thanks

---

### 评论 #13 — harkgill-amd (2024-11-13T14:42:13Z)

This a docker permissions error. Please try the second command with `sudo` privelages.
```
sudo docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
--device=/dev/kfd --device=/dev/dri --group-add video \
--ipc=host --shm-size 8G rocm/pytorch:latest
```
To run the command without `sudo`, you can utilize the docker group which grants root-level privileges to the user.
```
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
--device=/dev/kfd --device=/dev/dri --group-add video \
--ipc=host --shm-size 8G rocm/pytorch:latest
```

---

### 评论 #14 — shifrin8101 (2024-11-18T21:33:19Z)

I try this:
root@5cebad1f088b:/var/lib/jenkins# hostname
5cebad1f088b
looks like I should somehow bring there my python file

---

### 评论 #15 — shifrin8101 (2024-11-18T21:47:54Z)

OK I just created new file - same code.
p1.py looks like this:
import torch
import os
os.environ['HIP_VISIBLE_DEVICES']='0'
def get_device():
    if torch.cuda.is_available():
        #device =  torch.cuda.get_device_name(0)
        device = torch.device(0)
        print(f'device name [0]:', torch.cuda.get_device_name(0), ' GPU is available')
    else:
        device = torch.device("cpu")
        print("GPU is not available. Using CPU.")
    return device


device = get_device()
print(device)

torch.autograd.set_detect_anomaly(True)

w1_init = torch.randn(2, 2)
try:
    W1=w1_init.clone().detach().to(device).requires_grad_(True)
    print(W1)
except Exception as e:
    print(f"An error occurred: {e}")

finished_sample=1

running at the docker:

python p1.py
root@416198dec828:/var/lib/jenkins# python p1.py
device name [0]: AMD Radeon™ RX 7600 XT  GPU is available
cuda:0
An error occurred: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3.
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

running in my machine just made it 
device name [0]: AMD Radeon RX 7600 XT  GPU is available
cuda:0

Process finished with exit code 139 (interrupted by signal 11:SIGSEGV)


so apparently something is fundamentally wrong. (Consider getting a better GPU? which one?)

hope this provides some useful info about the situation.
thanks!

---

### 评论 #16 — harkgill-amd (2024-11-19T15:08:16Z)

Could you please provide the dmesg output after you hit the error? This can be done with

```
sudo dmesg > dmesg_output.txt
```

---

### 评论 #17 — shifrin8101 (2024-11-19T22:37:22Z)

root@416198dec828:/var/lib/jenkins# sudo dmesg > dmesg_output.txt
dmesg: read kernel buffer failed: Operation not permitted


---

### 评论 #18 — harkgill-amd (2024-11-20T18:49:33Z)

You'd have to get the dmesg output from the host system outside the container (After running the sample on the host). 

---

### 评论 #19 — shifrin8101 (2024-11-20T21:18:12Z)

[dmesg_output.txt](https://github.com/user-attachments/files/17836868/dmesg_output.txt)

OK, that one produced really a lot, here it is, attached, really hope it would be useful!


---

### 评论 #20 — YumingChang02 (2024-11-26T06:24:17Z)

@harkgill-amd may i ask if the ISA disagree is across 780m  7600(xt) 7700/7800xt? is there some insight to which rdna3 gpus are ISA compatable with NAVI31/gfx1100?

---

### 评论 #21 — harkgill-amd (2024-11-27T19:30:37Z)

@shifrin8101, I was finally able to reproduce the `Invalid device function` error with a 7600XT using a different workload. Did some digging and it is due to the gfx1102 architecture not being supported, see the relevant logs below.

```
1:hip_fatbin.cpp           :117 : 6041234758 us: [pid:840   tid:0x78e4cb2a4740] Missing CO for these ISAs -
:1:hip_fatbin.cpp           :120 : 6041234760 us: [pid:840   tid:0x78e4cb2a4740]      amdgcn-amd-amdhsa--gfx1102
:3:hip_platform.cpp         :715 : 6041234763 us: [pid:840   tid:0x78e4cb2a4740] init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules
:1:hip_fatbin.cpp           :276 : 6041235417 us: [pid:840   tid:0x78e4cb2a4740] Cannot find CO in the bundle /opt/rocm-6.2.3/magma/lib/libmagma.so for ISA: a
```
Overriding to gfx1100 with `export HSA_OVERRIDE_GFX_VERSION=11.0.0` worked around this issue and would be your best bet despite the ISAs not being identical. There may be certain low level instructions that are missing due to the differences between the versions which can cause crashes. However, in most cases workloads should run without any issues. You can also set this variable locally with the following so it only affects the current Python process
```
import os
os.environ['HSA_OVERRIDE_GFX_VERSION'] = '11.0.0'
```

Please give this a try and let me know if it resolves your issue.

@YumingChang02 Here's a list that answers your question https://salsa.debian.org/rocm-team/community/team-project/-/wikis/Supported-GPU-list#architecture-notes. The ISAs for gfx1100, gfx1101 and gfx1102 all have differences but in cases such as this, overriding to gfx1100 is the only course that can provide usability. 7800/7700 being gfx1101 and 7600/7600XT being gfx1102.

---

### 评论 #22 — shifrin8101 (2024-12-01T09:27:27Z)

Thanks a lot for this great assistance! 
So far it is successfully running.
I will check the situation again after some runtime will pass. Will let know here if new problems emerge, otherwise will let know that the solution to the problem was found.

---

### 评论 #23 — harkgill-amd (2025-01-20T18:39:14Z)

Hi @shifrin8101, I'll close this issue out as the workload runs correctly with the `HSA_OVERRIDE_GFX_VERSION` environment variable set. If you do have any other questions or updates, feel free to leave a comment on this thread and I'll re-open this issue.

---

### 评论 #24 — shifrin8101 (2025-01-20T19:11:51Z)

No more comments, thanks

It keeps working well, well done!

‫בתאריך יום ב׳, 20 בינו׳ 2025 ב-20:39 מאת ‪harkgill-amd‬‏ <‪
***@***.***‬‏>:‬

> Closed #3840 <https://github.com/ROCm/ROCm/issues/3840> as completed.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/3840#event-16003475201>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/BEE26YCPFL6TFYUW2VWDTD32LU7GPAVCNFSM6AAAAABPEIQYOSVHI2DSMVQWIX3LMV45UABCJFZXG5LFIV3GK3TUJZXXI2LGNFRWC5DJN5XDWMJWGAYDGNBXGUZDAMI>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---
