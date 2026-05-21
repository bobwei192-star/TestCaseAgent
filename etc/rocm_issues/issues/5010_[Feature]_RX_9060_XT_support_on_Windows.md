# [Feature]: RX 9060 XT support on Windows.

> **Issue #5010**
> **状态**: closed
> **创建时间**: 2025-07-08T19:33:43Z
> **更新时间**: 2025-07-22T21:11:51Z
> **关闭时间**: 2025-07-22T20:52:42Z
> **作者**: TawusGames
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5010

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

I installed ComfyUI using ZLUDA. ComfyUI runs and launches properly. However, when I try to generate a 3D model using Hunyuan 3D, I get an error:
rocBLAS error: Cannot read C:\Program Files\AMD\ROCm\6.2\bin/rocblas/library/TensileLibrary.dat: No such file or directory for GPU arch: gfx1200
As far as I understand—please correct me if I’m wrong—AMD ROCm on Windows 11 still doesn't support the RX 9000 series. In the documentation, RDNA 4.0 cards haven't yet been added to the Windows support list.
When will RX 9000 series support be added for Windows 11?

### Operating System

Windows 11

### GPU

Rx 9060xt

### ROCm Component

ROCm 6.2 with zluda

---

## 评论 (44 条)

### 评论 #1 — Nem404 (2025-07-08T21:43:26Z)

Finally someone else has got the rx 9060 xt too and wants to do anything ai related locally on windows. Except they can't, just like me.

---

### 评论 #2 — schung-amd (2025-07-08T21:51:30Z)

Hi @TawusGames @Nem404, sorry for the inconvenience. While we don't currently have HIP SDK support for gfx12, we do have WSL support for the 9060XT listed in the compatibility matrix at https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html, so I'd suggest trying that. If you encounter any issues or need guidance on this, we can discuss this here or in separate issues as you desire. As for timelines on native Windows support, I'll check internally to see if we have any information to provide.

---

### 评论 #3 — 0xDELUXA (2025-07-08T22:12:15Z)

@TawusGames As you said hip sdk 6.2.4 on windows doesnt support rdna4 at all, this is why if you get a rocblas tensile library for the gfx1200, you will not get this error anymore, but the performance will be really bad, in my case its like 5x slower than an rx 7600 xt, thats rdna3, therefore its supported.

For now, the best thing we got is rocm 7 from TheRock repo's tarballs, but zluda doesnt support it. Ive managed to build a pytorch wheel from source for the gfx1200, but currently getting miopen errors, and with every single workaround Ive found, cant get more than like 15 s/it, which is a joke for this card. Made an issue at miopen repo. I think they need to look into it.

@schung-amd Yes, I can confirm that wsl works good with this card, it was a kinda tough to set it up, but this is the only way we can use the  rx 9060 xt for now. I get like 1.10 it/s generating an 1024x1024 image with comfyui using an sdxl checkpoint. But its not that convenient firing up wsl everytime before a generation, and it also has overhead, so its slower than on a native linux os. And I have some workflows that cant be done with wsl and windows, I cant make them cross-platform. One more thing I should mention: tiled vae. Without using it, vae freezes my whole pc for like 10 seconds, tried changing wsl settings, fp16 vae, etc, but couldnt do anything about this problem. So tiled vae is a must for now.

All in all, we need to be patient, amd devs are currently working on pytorch for windows with rocm, it was announced to the public that it will be released sometime in q3, yes its already q3 so its like, not that far (hopefully).

---

### 评论 #4 — TawusGames (2025-07-08T22:48:17Z)

Have you had a chance to try Hunyuan 3D through ComfyUI? Do the 3D model generators work? Reddit users have said it doesn't work, but I haven't seen anyone who has actually tried it.

---

### 评论 #5 — 0xDELUXA (2025-07-08T22:56:19Z)

This is not a question about those 3d model generators. Its way deeper. We cant use comfyui, sdnext, fooocus, automatic1111, etc, so like nothing local ai related on windows with this card.

Or are you asking If I've tried those inside wsl?

---

### 评论 #6 — TawusGames (2025-07-08T23:04:57Z)

I know it doesn't work on Windows. I should have asked the question more specifically. If I install it with ZLUDA on Ubuntu, will Hunyuan 3D work?

---

### 评论 #7 — Nem404 (2025-07-08T23:05:08Z)

Eyy if we had the 9070... For that card everything is built and working amazing on windows, so pytorch wheels and everything, they say its even faster than zluda. *cries in poor*

---

### 评论 #8 — 0xDELUXA (2025-07-08T23:06:45Z)

> I know it doesn't work on Windows. I should have asked the question more specifically. If I install it with ZLUDA on Ubuntu, will Hunyuan 3D work?

What do you mean, linux doesnt need zluda at all. Everything is supported natively. I mean thats needed for image generation. I dont know about this Hunyuan 3D thing specifically, havent tried it yet

---

### 评论 #9 — TawusGames (2025-07-08T23:10:16Z)

I thought ComfyUI uses CUDA. Doesn’t it use it on the Linux version too? If it doesn’t, I’ll go ahead and install Ubuntu as a secondary OS. And even hunyuan 3d page says Nvidia gpu requiered.

---

### 评论 #10 — 0xDELUXA (2025-07-08T23:17:34Z)

> I thought ComfyUI uses CUDA. Doesn’t it use it on the Linux version too? If it doesn’t, I’ll go ahead and install Ubuntu as a secondary OS. And even hunyuan 3d page says Nvidia gpu requiered.

Cuda on nvidia but amd doesn't have any of it. Its equivalent is rocm. That's what comfyui uses. But this specific hunyuan 3d thing idk even whats this about

---

### 评论 #11 — TawusGames (2025-07-08T23:21:51Z)

3D model generator. Just like trellis, roblox cube, stable fast 3d. I'm thinking of using it as a game asset. 

---

### 评论 #12 — 0xDELUXA (2025-07-08T23:26:05Z)

> 3D model generator. Just like trellis, roblox cube, stable fast 3d. I'm thinking of using it as a game asset. 

I see. Cant say if it's working or not, you can try it if you have time. But if it's only a pytorch thing like average image or video generation, then it should work (assuming bc it can be used inside comfyui as you said earlier)


---

### 评论 #13 — TawusGames (2025-07-08T23:30:49Z)

I'll try it tomorrow and leave the result here. I don't even know if anyone has tried it before. Maybe it'll help someone.

---

### 评论 #14 — 0xDELUXA (2025-07-08T23:37:03Z)

As schung said, feel free to ask things here. Based on my experience, amd people are really nice

---

### 评论 #15 — TawusGames (2025-07-08T23:41:57Z)

I don't have much experience with GitHub—I've used it with my previous account, and usually others reply after about a week. I was surprised that AMD employees responded so quickly.
I might be the happiest person that competition has returned to the GPU market. It reminds me of the GTX 1060 and RX 580 days. The only difference is that this time, AMD is much stronger.

---

### 评论 #16 — TawusGames (2025-07-09T16:47:12Z)

The Linux world is really troublesome for someone like me who doesn’t have much experience. I tried four different distros and had issues with all of them. One—I don’t remember the name—didn’t even boot. Ubuntu got stuck at the boot screen. On Debian, AMD drivers were problematic. Arch Linux was the only one I managed to boot successfully. I’ve been struggling for about 3–4 hours. Anyway, the AI that generates shapes seems to be working fine. The one that applies textures to shapes has some issues. So that’s good news. Texturing isn’t that important to me—once the shape is created, I can take care of the rest myself. I don’t plan to use it via Linux. I’m eagerly awaiting Windows ROCm SDK support for the AMD 9000 series GPUs. Good luck to the AMD team. I’m closing the topic.

---

### 评论 #17 — niknishant (2025-07-12T07:27:34Z)

For using zluda. You need unofficial rocm library for your gpu (gfx1200) and need to patchzluda2.bat. 9060xt works with comfyui with zluda. But It will take 40-60minutes to generate one image with flux 1 kontext dev

---

### 评论 #18 — 0xDELUXA (2025-07-12T07:42:03Z)

> For using zluda. You need unofficial rocm library for your gpu (gfx1200) and need to patchzluda2.bat. 9060xt works with comfyui with zluda. But It will take 40-60minutes to generate one image with flux 1 kontext dev

Yes, I've tried it. But it's like 4-5x slower than my old rx 7600 xt rdna3 card that was natively supported by hip sdk 6.2. Isn't because of the card itself, but bc hip 6.2 uses fallback logics for this card and that's why its performance is this bad. Looks like Amd thinks no one on Windows has rdna4 cards and wants to do smth ai related locally

---

### 评论 #19 — niknishant (2025-07-12T07:45:04Z)

> > For using zluda. You need unofficial rocm library for your gpu (gfx1200) and need to patchzluda2.bat. 9060xt works with comfyui with zluda. But It will take 40-60minutes to generate one image with flux 1 kontext dev
> 
> Yes, I've tried it. But it's like 4-5x slower than my old rx 7600 xt rdna3 card that was natively supported by hip sdk 6.2. Isn't because of the card itself, but bc hip 6.2 uses fallback logics for this card and that's why its performance is this bad. Looks like Amd thinks no one on Windows has rdna4 cards and wants to do smth ai related locally

Even with official rocm support in ubuntu. It is going worst than the zluda taking 2 hours

---

### 评论 #20 — 0xDELUXA (2025-07-12T07:53:38Z)

> 
> Even with official rocm support in ubuntu. It is going worst than the zluda taking 2 hours

For me, on wsl2 ubuntu 24.04 using rocm 6.4.1 wheels recommended by Amd on their website, I get 1.10 it/s while generating a normal 1024x1024 image with sdxl. Its not that bad but I need a windows solution

---

### 评论 #21 — TawusGames (2025-07-18T13:44:52Z)

Hi, I reinstalled ComfyUI with WSL. I reached the final step and launched ComfyUI, but I got an error saying it couldn't find a HIP device.

```
(.venv) rotinda@Rotinda:~/ComfyUI$ python main.py
Checkpoint files will always be loaded safely.
Traceback (most recent call last):
  File "/home/rotinda/ComfyUI/main.py", line 138, in <module>
    import execution
  File "/home/rotinda/ComfyUI/execution.py", line 15, in <module>
    import comfy.model_management
  File "/home/rotinda/ComfyUI/comfy/model_management.py", line 221, in <module>
    total_vram = get_total_memory(get_torch_device()) / (1024 * 1024)
                                  ^^^^^^^^^^^^^^^^^^
  File "/home/rotinda/ComfyUI/comfy/model_management.py", line 172, in get_torch_device
    return torch.device(torch.cuda.current_device())
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rotinda/ComfyUI/.venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 940, in current_device
    _lazy_init()
  File "/home/rotinda/ComfyUI/.venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 319, in _lazy_init
    torch._C._cuda_init()
RuntimeError: No HIP GPUs are available

```
When I typed 'rocm info', it recognized my graphics card.

```
*******
Agent 2
*******
  Name:                    gfx1200
  Marketing Name:          AMD Radeon RX 9060 XT
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
```



---

### 评论 #22 — niknishant (2025-07-18T13:52:44Z)

> Hi, I reinstalled ComfyUI with WSL. I reached the final step and launched ComfyUI, but I got an error saying it couldn't find a HIP device.
> 
> ```
> (.venv) rotinda@Rotinda:~/ComfyUI$ python main.py
> Checkpoint files will always be loaded safely.
> Traceback (most recent call last):
>   File "/home/rotinda/ComfyUI/main.py", line 138, in <module>
>     import execution
>   File "/home/rotinda/ComfyUI/execution.py", line 15, in <module>
>     import comfy.model_management
>   File "/home/rotinda/ComfyUI/comfy/model_management.py", line 221, in <module>
>     total_vram = get_total_memory(get_torch_device()) / (1024 * 1024)
>                                   ^^^^^^^^^^^^^^^^^^
>   File "/home/rotinda/ComfyUI/comfy/model_management.py", line 172, in get_torch_device
>     return torch.device(torch.cuda.current_device())
>                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
>   File "/home/rotinda/ComfyUI/.venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 940, in current_device
>     _lazy_init()
>   File "/home/rotinda/ComfyUI/.venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 319, in _lazy_init
>     torch._C._cuda_init()
> RuntimeError: No HIP GPUs are available
> ```
> 
> When I typed 'rocm info', it recognized my graphics card.
> 
> ```
> *******
> Agent 2
> *******
>   Name:                    gfx1200
>   Marketing Name:          AMD Radeon RX 9060 XT
>   Vendor Name:             AMD
>   Feature:                 KERNEL_DISPATCH
>   Profile:                 BASE_PROFILE
>   Float Round Mode:        NEAR
>   Max Queue Number:        128(0x80)
>   Queue Min Size:          64(0x40)
>   Queue Max Size:          131072(0x20000)
>   Queue Type:              MULTI
>   Node:                    1
>   Device Type:             GPU
>   Cache Info:
> ```

Did you try this command after installing rocm in wsl===}.    sudo usermod -a -G render,video $LOGNAME .
But for your information. This gpu is not for using flux kontext or wan2.1

---

### 评论 #23 — 0xDELUXA (2025-07-18T13:53:09Z)

> Hi, I reinstalled ComfyUI with WSL. I reached the final step and launched ComfyUI, but I got an error saying it couldn't find a HIP device.
> 
> ```
> (.venv) rotinda@Rotinda:~/ComfyUI$ python main.py
> Checkpoint files will always be loaded safely.
> Traceback (most recent call last):
>   File "/home/rotinda/ComfyUI/main.py", line 138, in <module>
>     import execution
>   File "/home/rotinda/ComfyUI/execution.py", line 15, in <module>
>     import comfy.model_management
>   File "/home/rotinda/ComfyUI/comfy/model_management.py", line 221, in <module>
>     total_vram = get_total_memory(get_torch_device()) / (1024 * 1024)
>                                   ^^^^^^^^^^^^^^^^^^
>   File "/home/rotinda/ComfyUI/comfy/model_management.py", line 172, in get_torch_device
>     return torch.device(torch.cuda.current_device())
>                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
>   File "/home/rotinda/ComfyUI/.venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 940, in current_device
>     _lazy_init()
>   File "/home/rotinda/ComfyUI/.venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 319, in _lazy_init
>     torch._C._cuda_init()
> RuntimeError: No HIP GPUs are available
> 
> ```
> When I typed 'rocm info', it recognized my graphics card.
> 
> ```
> *******
> Agent 2
> *******
>   Name:                    gfx1200
>   Marketing Name:          AMD Radeon RX 9060 XT
>   Vendor Name:             AMD
>   Feature:                 KERNEL_DISPATCH
>   Profile:                 BASE_PROFILE
>   Float Round Mode:        NEAR
>   Max Queue Number:        128(0x80)
>   Queue Min Size:          64(0x40)
>   Queue Max Size:          131072(0x20000)
>   Queue Type:              MULTI
>   Node:                    1
>   Device Type:             GPU
>   Cache Info:
> ```
> 
> 

Which torch are you using? The AMD recommended one? Think it's smth like 2.6.0+rocm6.4.1

---

### 评论 #24 — 0xDELUXA (2025-07-18T13:55:58Z)


> Which torch are you using? The AMD recommended one? Think it's smth like 2.6.0+rocm6.4.1

If so, then it will not detect the gpu until you run these commands:

`location=$(pip show torch | grep Location | awk -F ": " '{print $2}') cd ${location}/torch/lib/ rm libhsa-runtime64.so*`

---

### 评论 #25 — TawusGames (2025-07-18T14:03:27Z)

> > Hi, I reinstalled ComfyUI with WSL. I reached the final step and launched ComfyUI, but I got an error saying it couldn't find a HIP device.
> > ```
> > (.venv) rotinda@Rotinda:~/ComfyUI$ python main.py
> > Checkpoint files will always be loaded safely.
> > Traceback (most recent call last):
> >   File "/home/rotinda/ComfyUI/main.py", line 138, in <module>
> >     import execution
> >   File "/home/rotinda/ComfyUI/execution.py", line 15, in <module>
> >     import comfy.model_management
> >   File "/home/rotinda/ComfyUI/comfy/model_management.py", line 221, in <module>
> >     total_vram = get_total_memory(get_torch_device()) / (1024 * 1024)
> >                                   ^^^^^^^^^^^^^^^^^^
> >   File "/home/rotinda/ComfyUI/comfy/model_management.py", line 172, in get_torch_device
> >     return torch.device(torch.cuda.current_device())
> >                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
> >   File "/home/rotinda/ComfyUI/.venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 940, in current_device
> >     _lazy_init()
> >   File "/home/rotinda/ComfyUI/.venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 319, in _lazy_init
> >     torch._C._cuda_init()
> > RuntimeError: No HIP GPUs are available
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
> > When I typed 'rocm info', it recognized my graphics card.
> > ```
> > *******
> > Agent 2
> > *******
> >   Name:                    gfx1200
> >   Marketing Name:          AMD Radeon RX 9060 XT
> >   Vendor Name:             AMD
> >   Feature:                 KERNEL_DISPATCH
> >   Profile:                 BASE_PROFILE
> >   Float Round Mode:        NEAR
> >   Max Queue Number:        128(0x80)
> >   Queue Min Size:          64(0x40)
> >   Queue Max Size:          131072(0x20000)
> >   Queue Type:              MULTI
> >   Node:                    1
> >   Device Type:             GPU
> >   Cache Info:
> > ```
> 
> Did you try this command after installing rocm in wsl===}. sudo usermod -a -G render,video $LOGNAME . But for your information. This gpu is not for using flux kontext or wan2.1

I've already tried, but the issue wasn't resolved.

---

### 评论 #26 — TawusGames (2025-07-18T14:09:24Z)

> > Hi, I reinstalled ComfyUI with WSL. I reached the final step and launched ComfyUI, but I got an error saying it couldn't find a HIP device.
> > ```
> > (.venv) rotinda@Rotinda:~/ComfyUI$ python main.py
> > Checkpoint files will always be loaded safely.
> > Traceback (most recent call last):
> >   File "/home/rotinda/ComfyUI/main.py", line 138, in <module>
> >     import execution
> >   File "/home/rotinda/ComfyUI/execution.py", line 15, in <module>
> >     import comfy.model_management
> >   File "/home/rotinda/ComfyUI/comfy/model_management.py", line 221, in <module>
> >     total_vram = get_total_memory(get_torch_device()) / (1024 * 1024)
> >                                   ^^^^^^^^^^^^^^^^^^
> >   File "/home/rotinda/ComfyUI/comfy/model_management.py", line 172, in get_torch_device
> >     return torch.device(torch.cuda.current_device())
> >                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
> >   File "/home/rotinda/ComfyUI/.venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 940, in current_device
> >     _lazy_init()
> >   File "/home/rotinda/ComfyUI/.venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 319, in _lazy_init
> >     torch._C._cuda_init()
> > RuntimeError: No HIP GPUs are available
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
> > When I typed 'rocm info', it recognized my graphics card.
> > ```
> > *******
> > Agent 2
> > *******
> >   Name:                    gfx1200
> >   Marketing Name:          AMD Radeon RX 9060 XT
> >   Vendor Name:             AMD
> >   Feature:                 KERNEL_DISPATCH
> >   Profile:                 BASE_PROFILE
> >   Float Round Mode:        NEAR
> >   Max Queue Number:        128(0x80)
> >   Queue Min Size:          64(0x40)
> >   Queue Max Size:          131072(0x20000)
> >   Queue Type:              MULTI
> >   Node:                    1
> >   Device Type:             GPU
> >   Cache Info:
> > ```
> 
> Which torch are you using? The AMD recommended one? Think it's smth like 2.6.0+rocm6.4.1

I installed ROCm version 6.4.1 and downloaded the PyTorch version using this command.
`pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.4`
I tried to check its version, but I couldn't manage it.

---

### 评论 #27 — 0xDELUXA (2025-07-18T14:10:39Z)

> 
> I've already tried, but the issue wasn't resolved.

I didnt need this sudo usermod thing for wls either. Think its for native linux only


---

### 评论 #28 — 0xDELUXA (2025-07-18T14:12:46Z)

 
> I installed ROCm version 6.4.1 and downloaded the PyTorch version using this command.
> `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.4`
> I tried to check its version, but I couldn't manage it.

No, this way it will not work. Rocm 6.4 doesnt support the rx 9060 xt, only 6.4.1


---

### 评论 #29 — 0xDELUXA (2025-07-18T14:14:15Z)

Start again following carefully the instructions here:
https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html

---

### 评论 #30 — TawusGames (2025-07-18T14:20:44Z)

> Start again following carefully the instructions here: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html

Thank you for your help.

I just want to say something about documentation in general. I spent 30 minutes searching for the WSL installation documentation and couldn’t find it. People often criticize Unity’s documentation, but thanks to its search feature, I can quickly find what I need. I wish other documentation had a search feature too. Since English isn’t my native language, I struggle even more when trying to search.

---

### 评论 #31 — 0xDELUXA (2025-07-18T14:24:34Z)


> 
> Thank you for your help.
> 
> I just want to say something about documentation in general. I spent 30 minutes searching for the WSL installation documentation and couldn’t find it. People often criticize Unity’s documentation, but thanks to its search feature, I can quickly find what I need. I wish other documentation had a search feature too. Since English isn’t my native language, I struggle even more when trying to search.

You're right, it was more than an hour of work for me to finally get wsl work with gfx1200.

If you have any other questions feel free to ask



---

### 评论 #32 — schung-amd (2025-07-18T14:26:42Z)

> I spent 30 minutes searching for the WSL installation documentation and couldn’t find it

Sorry for the inconvenience, where/what did you search? If our documentation isn't pointing people where they need to be, we should take a look at improving that.

---

### 评论 #33 — TawusGames (2025-07-18T14:30:39Z)

<img width="1919" height="1005" alt="Image" src="https://github.com/user-attachments/assets/954cc800-41b7-4f0e-9ee6-5acd7ee274bf" />

There’s nothing wrong with the documentation itself. But without a search feature, I get lost in it. A search bar like the one in Unity’s top-left corner would completely solve the problem.


---

### 评论 #34 — TawusGames (2025-07-18T14:32:13Z)

> > I spent 30 minutes searching for the WSL installation documentation and couldn’t find it
> 
> Sorry for the inconvenience, where/what did you search? If our documentation isn't pointing people where they need to be, we should take a look at improving that.

<img width="1919" height="951" alt="Image" src="https://github.com/user-attachments/assets/73887c02-adb8-47c6-a338-57af7cf28ebd" />

It was my mistake — it was already there.


---

### 评论 #35 — TawusGames (2025-07-19T15:25:50Z)

ComfyUI works perfectly with WSL. Hunyuan3D generates models very well.

<img width="1919" height="955" alt="Image" src="https://github.com/user-attachments/assets/f12ee34d-ce67-4710-85e0-d7d31adf5480" />

The texture generator works a bit slowly. Since it's running through WSL, I feel like it's causing the RAM to fill up.

---

### 评论 #36 — 0xDELUXA (2025-07-19T15:27:51Z)

> ComfyUI works perfectly with WSL. Hunyuan3D generates models very well.
> 
> <img width="1919" height="955" alt="Image" src="https://github.com/user-attachments/assets/f12ee34d-ce67-4710-85e0-d7d31adf5480" />
> 
> The texture generator works a bit slowly. Since it's running through WSL, I feel like it's causing the RAM to fill up.

Good to know that.
How much system ram did you assign to wsl?

---

### 评论 #37 — TawusGames (2025-07-19T15:29:37Z)

> > ComfyUI works perfectly with WSL. Hunyuan3D generates models very well.
> > <img alt="Image" width="1919" height="955" src="https://private-user-images.githubusercontent.com/219904802/468296957-f12ee34d-ce67-4710-85e0-d7d31adf5480.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTI5MzkxNzMsIm5iZiI6MTc1MjkzODg3MywicGF0aCI6Ii8yMTk5MDQ4MDIvNDY4Mjk2OTU3LWYxMmVlMzRkLWNlNjctNDcxMC04NWUwLWQ3ZDMxYWRmNTQ4MC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNzE5JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDcxOVQxNTI3NTNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0zZGFmZGVhMjk0MGRkZGUzNTcxNzdhOTVkYTRiNjVlYjEwZTZkMzMyNzczNjg4Y2FiMjNjZTViMTI2MWY1ZjUyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.Yk4OKSRq5Ro6ZsVYO5zeF9nfzEczeMMv2b53gYgcnhQ">
> > The texture generator works a bit slowly. Since it's running through WSL, I feel like it's causing the RAM to fill up.
> 
> Good to know that. How much system ram did you assign to wsl?

I assigned 22 GB of my 32 GB system RAM to WSL.

---

### 评论 #38 — 0xDELUXA (2025-07-19T15:34:08Z)


> 
> I assigned 22 GB of my 32 GB system RAM to WSL.

I think thats good. Im using it with 24.
If we go further, it can freeze the entire pc

---

### 评论 #39 — TawusGames (2025-07-19T15:41:58Z)

> > I assigned 22 GB of my 32 GB system RAM to WSL.
> 
> I think thats good. Im using it with 24

Which AI model are you using? The reason I ask is that the AI texture generator ‘Hunyuan 3D Texture Turbo’ creates about six images, all the same size at roughly 300 px square, and then stitches them into a single image. When I try to change size it to 512 px, my computer freezes. I often get errors when generating textures and models simultaneously.

---

### 评论 #40 — 0xDELUXA (2025-07-19T15:46:46Z)

An average sdxl checkpoint, generating 1024x1024 images, at the vae stage the pc froze every time, until I figured out I needed tiled vae. Now everything works as it should
But this is still a workaround, AMD needs to optimize their things for rdna4 I think

---

### 评论 #41 — schung-amd (2025-07-22T20:52:42Z)

The freezing is likely due to memory limitations. I've seen this happen with some models (SD included) where the VAE is full precision even though the rest of the model is reduced precision, so even though the model itself fits into memory the VAE step does not without tiling.

Closing again as it looks like you have things working, but feel free to continue discussion and we can reopen again if necesssary.

---

### 评论 #42 — 0xDELUXA (2025-07-22T20:54:53Z)

If I use fp16 vae, it still crashes

---

### 评论 #43 — schung-amd (2025-07-22T21:03:33Z)

Interesting, thanks for the info, I'll have to take a look at that and refresh my memory. I generally recommend tiled VAE anyway to avoid memory issues, although I haven't used it extensively myself so there may be downsides I'm not aware of.

---

### 评论 #44 — 0xDELUXA (2025-07-22T21:09:27Z)

Oh sorry I just realized that it actually renders the windows pc outside wsl fully unusable for like 10 seconds or more but doesnt crash if I wait. Looked at hwinfo and the vae process uses 99% of windows system ram no matter how much I assign to wsl. I mean with full precision vae. Tiled works.

---
