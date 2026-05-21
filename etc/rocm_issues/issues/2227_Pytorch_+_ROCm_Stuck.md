# Pytorch + ROCm Stuck

> **Issue #2227**
> **状态**: closed
> **创建时间**: 2023-06-08T05:43:46Z
> **更新时间**: 2023-10-07T16:29:23Z
> **关闭时间**: 2023-10-07T16:27:58Z
> **作者**: linwk20
> **标签**: application:pytorch
> **URL**: https://github.com/ROCm/ROCm/issues/2227

## 标签

- **application:pytorch** (颜色: #bfdadc)

## 描述

I am trying to run Pytorch on my Provii and RX6300, the environment is:

OS: Ubuntu 20.04.6

Torch: 2.0.1 + ROCm-5.4.2

ROCm: 5.4.5

 

But when I used any operations related to GPU, like tensor.cuda(), the Provii will just stuck and RX6300 will return Segmentation Fault. That is, the pytorch with rocm did not work at all.

 

I have tried different OS (22.04) and ROCm(5.4.2), docker version torch, host version ... They all did not works... What can I try? I guess the problem may come from the driver?

 

Thanks in advance!

---

## 评论 (7 条)

### 评论 #1 — tucnak (2023-06-08T11:43:36Z)

I experience the same issue with AMD Instinct (gfx906 in particular) series data-center grade cards in a single GPU setup.

---

### 评论 #2 — linwk20 (2023-06-08T12:42:47Z)

> I experience the same issue with AMD Instinct (gfx906 in particular) series data-center grade cards in a single GPU setup.

How did you solve it, I plan to downgrade to ubuntu20.04, because in 22.04 I can only install --no-dkms version of driver. Maybe it is the reason?


---

### 评论 #3 — tucnak (2023-06-08T12:43:59Z)

I didn't solve it 🥇 

---

### 评论 #4 — winstonma (2023-07-18T03:16:05Z)

There are several things you can try

**Check if Pytorch + ROCm is working**
You can first verify by running the following command
```bash
# Check the GFX version
$ clinfo --list 
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1030

# This is the output of the correct Pytorch+ROCm setting
$HSA_OVERRIDE_GFX_VERSION=10.3.0 python -c 'import torch; print(torch.cuda.is_available())'
True

# If you see the following error it means that you installed the CPU version of Pytorch
$ HSA_OVERRIDE_GFX_VERSION=10.3.0 python -c 'import torch; print(torch.cuda.is_available())'
Traceback (most recent call last):
  File "<string>", line 1, in <module>
AttributeError: module 'torch' has no attribute 'cuda'

```
If you see a `True` that means it is working. The only thing that is missing the GFX export
```bash
$export HSA_OVERRIDE_GFX_VERSION=10.3.0
$python3 main.py
```


**Install AMD Driver**
Not sure if this is the root cause but you can try the following script. If you use Ubuntu 20.04 then please replace `jammy` with `focal`. Based on my experience, the driver only can be installed with the Ubuntu default kernel. So please uninstall the external kernel first (e.g. [mainline kernel](https://github.com/bkw777/mainline)).
```bash
filename=$(curl https://repo.radeon.com/amdgpu-install/latest/ubuntu/jammy/ | grep deb | xmllint --html --format --xpath "string(//a/@href)" - )
wget https://repo.radeon.com/amdgpu-install/latest/ubuntu/jammy/$filename
sudo dpkg -i $filename
amdgpu-install --opencl=rocr

# Add user to groups render and video
sudo usermod -a -G render ${USER}
sudo usermod -a -G video ${USER}
```
After the system is rebooted then you can use the bash command in the previous step and check


**Install latest kernel (optional)**
Please do that **after** installing AMD graphics driver
```bash
# Add the mainline kernel updater PPA
sudo add-apt-repository ppa:cappelikan/ppa
# Install mainline kernel updater
sudo apt install -y mainline
# Use install latest kernel
sudo mainline --install-latest
```

---

### 评论 #5 — xuhuisheng (2023-07-25T11:48:12Z)

pytorch-2.x with gfx906 always raise error on mnist of examples.
While pytorch-1.13 with gfx903 is just fine.

I cannot find the reason recently. Since there is only one error message: 
```
Traceback (most recent call last):
  File "/home/work/examples/mnist/main.py", line 145, in <module>
    main()
  File "/home/work/examples/mnist/main.py", line 136, in main
    train(args, model, device, train_loader, optimizer, epoch)
  File "/home/work/examples/mnist/main.py", line 43, in train
    loss = F.nll_loss(output, target)
  File "/home/work/.local/lib/python3.10/site-packages/torch/nn/functional.py", line 2703, in nll_loss
    return torch._C._nn.nll_loss_nd(input, target, weight, _Reduction.get_enum(reduction), ignore_index)
RuntimeError: HIP error: the operation cannot be performed in the present state
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing HIP_LAUNCH_BLOCKING=1.

```

---

### 评论 #6 — DGdev91 (2023-10-05T23:49:39Z)

> RuntimeError: HIP error: the operation cannot be performed in the present state

That error usually means your configuration doesn't support PCI atomics, wich has become a needed feature for rocm after rocm 5.3

There's a workaround for that in 5.7, basically compiling the programs you need to run using the flag "-mprintf-kind=buffered".

There's someone working on that on a separate branch in RocmSoftwarePlatform/pytorch, read here: https://github.com/pytorch/pytorch/issues/103973#issuecomment-1747779668

---

### 评论 #7 — linwk20 (2023-10-07T16:29:23Z)

I close the issue because I have solved the problem.
I plug 2 types of AMD GPU into my machine and it causes AMD driver problems.

As long as I only leave one type on it, everything works fine.

---
