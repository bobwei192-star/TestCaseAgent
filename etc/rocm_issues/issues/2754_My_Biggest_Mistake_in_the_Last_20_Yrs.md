# My Biggest Mistake in the Last 20 Yrs.

> **Issue #2754**
> **状态**: closed
> **创建时间**: 2023-12-19T18:56:47Z
> **更新时间**: 2024-10-13T14:52:11Z
> **关闭时间**: 2024-10-13T14:52:11Z
> **作者**: ArtisticMusician
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2754

## 描述

I'm a digital artist (Mostly 3D but I d some 2D work as well) and A music composer. So every few years I either build a new Desktop or or upgrade the one I have if the upgrades are worth it. Up until this last year I had always gone with intel for my CPU and Nvidia for my GPU. This year I wasn't all that happy with the way intel's CPUs had some cores fast and some cores slow, and I was impressed with the number comparisons that AMD GPUs were showing. So I thought what the hell I'll build my first AMD system. I went with the Ryzen 9 7950X in the CPU department, and Radeon 7900 XTX for the GPU.  Toi be honest I made as big mistake and I didn't do enough research because I thought AMD is a well establish company by now. It didn't even cross my mind that AMD wouldn't be compatible with a bunch of 3D software or stable diffusion. (On windows 11) Yeah I know, and believe me I've learned that lesson in gobs of wasted time and energy trying to get my New slightly Expensive GPU to do what I expected it to do in the first place, out of the box.

I've pretty much spent the entire year (I built it last December) trying to get the GPU to work with Stable diffusion fully like I expected, and like it should. I'm pretty good with computers but I'm in no way a programmer. But I tried getting it to work on In Docker, In WSL, In virtualbox, hyper-something, and now I finally broke down and dual booted ubuntu. And still I can't get it to work. I follow instructions over here, then start over and follow instructions over here. And this video and that video. You know what? My Nvidia GPU always just worked. I didn't have to spend weeks trying to get them to function how I expected them to function they just did. 

TBH. Buying the AMD GPU was the biggest mistake I've made in 20 yrs. and I'm not exaggerating at all. And I still don't have it working. It shouldn't be this difficult. I'm exhausted by this GPU that should be making things better. I spent enough money on it, that it should just work. The biggest lesson of all is that I will never buy an AMD GPU ever again. 

---

## 评论 (22 条)

### 评论 #1 — illwieckz (2023-12-19T20:16:49Z)

This is something that Lisa Su should hear. AMD is best than anything else on everything but compute, and the worst of all on compute.

I own more than 10 GCN & RDNA GPUs and iGPUs, only one is running ROCm HIP, only twos are running ROCm OpenCL.

The last time there was an OpenCL AMD driver working on all cards [was at fglrx time](https://rebatir.fr/post/2022-01-25-OpenCL_on_Linux_state_of_AMD_drivers_is_now_worse_than_it_was_back_in_the_days_of_fglrx/).

_Edit_: I forgot to mention that not only AMD has no working compute, but AMD has no usable SR-IOV either. If AMD does nothing to fix that, Intel will take their place as Nvidia contender and do better.

---

### 评论 #2 — danielzgtg (2023-12-20T05:17:14Z)

> Stable diffusion

Try:

```bash
sudo apt install wget git python3 python3-venv libgl1 libglib2.0-0
sudo apt install libtcmalloc4 libgthread-2_0-0
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
git checkout dev
rm -rf venv
./webui.sh # If it fails the first time, do the following:
(. venv/bin/activate; pip install wheel) # The parentheses are intended
./webui.sh # Auto-opens browser. Model loading (without SSD) could take 2 minutes
```

This took me no more than 10 minutes of Googling various error messages.

> a well establish company
> (On windows 11)

ROCm for Windows only came out like yesterday or something. You can't expect the same stability as ROCm Linux which has been around since forever.

> My Nvidia GPU always just worked

Nvidia GPUs would have never worked for me. The nouveau driver doesn't even support reclocking yet. I refuse to install closed-source malware, so a Nvidia GPU might as well be as slower than Intel.

> I'm pretty good with computers but I'm in no way a programmer

AMD stuff works better with Linux. Linux stuff works better with some programming. Programming works better when you ask questions.

> spend weeks trying

Oh no! I would usually ask questions after 6 hours of things getting stuck, maybe 3 days at maximum. Try finding an IRC/Slack/Discord to ask questions.

> I'm a digital artist
> I will never buy an AMD GPU ever again

Have you considered hosted cloud APIs? You don't need a GPU these days. A local GPU is only needed if your work needs reproducibility, latency, or privacy. As models have been getting bigger and bigger, many of my friends have moved to the cloud:

- https://rundiffusion.com/
- https://softwarekeep.com/help-center/best-cloud-provider-for-stable-diffusion
- https://www.diffus.graviti.com/
- https://huggingface.co/spaces/stabilityai/stable-diffusion


---

### 评论 #3 — nartmada (2023-12-21T15:46:47Z)

Hi @ArtisticMusician, sorry to hear you are having problems getting AMD GPUs.  Can you please provide more details on what kind of errors you are running into?  Thanks for your help.

---

### 评论 #4 — ArtisticMusician (2023-12-23T08:09:56Z)

Hey Daniel Tang, the guy who thinks his "no more than 10 minutes of
Googling various error messages." is going to make it work. Nope Not
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 536.2/536.2 KB 3.5 MB/s eta
0:00:00
Using legacy 'setup.py install' for lit, since package 'wheel' is not
installed.
Installing collected packages: mpmath, lit, cmake, urllib3,
typing-extensions, sympy, pillow, numpy, networkx, MarkupSafe, idna,
filelock, charset-normalizer, certifi, requests, jinja2,
pytorch-triton-rocm, torch, torchvision
  Running setup.py install for lit ... done
Successfully installed MarkupSafe-2.1.3 certifi-2022.12.7
charset-normalizer-2.1.1 cmake-3.25.0 filelock-3.9.0 idna-3.4 jinja2-3.1.2
lit-15.0.7 mpmath-1.3.0 networkx-3.0 numpy-1.24.1 pillow-9.3.0
pytorch-triton-rocm-2.0.1 requests-2.28.1 sympy-1.12 torch-2.0.1+rocm5.4.2
torchvision-0.15.2+rocm5.4.2 typing-extensions-4.4.0 urllib3-1.26.13
Traceback (most recent call last):
  File "/home/josh/Documents/Auto1111/stable-diffusion-webui/launch.py",
line 48, in <module>
    main()
  File "/home/josh/Documents/Auto1111/stable-diffusion-webui/launch.py",
line 39, in main
    prepare_environment()
  File
"/home/josh/Documents/Auto1111/stable-diffusion-webui/modules/launch_utils.py",
line 384, in prepare_environment
    raise RuntimeError(
RuntimeError: Torch is not able to use GPU; add --skip-torch-cuda-test to
COMMANDLINE_ARGS variable to disable this check
***@***.***:~/Documents/Auto1111/stable-diffusion-webui$

On Tue, Dec 19, 2023 at 9:17 PM Daniel Tang ***@***.***>
wrote:

> Stable diffusion
>
> Try:
>
> sudo apt install wget git python3 python3-venv libgl1 libglib2.0-0
> sudo apt install libtcmalloc4 libgthread-2_0-0
> git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.gitcd stable-diffusion-webui
> git checkout dev
> rm -rf venv
> ./webui.sh # If it fails the first time, do the following:
> (. venv/bin/activate; pip install wheel) # The parentheses are intended
> ./webui.sh # Auto-opens browser. Model loading (without SSD) could take 2 minutes
>
> This took me no more than 10 minutes of Googling various error messages.
>
> a well establish company
> (On windows 11)
>
> ROCm for Windows only came out like yesterday or something. You can't
> expect the same stability as ROCm Linux which has been around since forever.
>
> My Nvidia GPU always just worked
>
> Nvidia GPUs would have never worked for me. The nouveau driver doesn't
> even support reclocking yet. I refuse to install closed-source malware, so
> a Nvidia GPU might as well be as slower than Intel.
>
> I'm pretty good with computers but I'm in no way a programmer
>
> AMD stuff works better with Linux. Linux stuff works better with some
> programming. Programming works better when you ask questions.
>
> spend weeks trying
>
> Oh no! I would usually ask questions after 6 hours of things getting
> stuck, maybe 3 days at maximum. Try finding an IRC/Slack/Discord to ask
> questions.
>
> I'm a digital artist
> I will never buy an AMD GPU ever again
>
> Have you considered hosted cloud APIs? You don't need a GPU these days. A
> local GPU is only needed if your work needs reproducibility, latency, or
> privacy. As models have been getting bigger and bigger, many of my friends
> have moved to the cloud:
>
>    - https://rundiffusion.com/
>    -
>    https://softwarekeep.com/help-center/best-cloud-provider-for-stable-diffusion
>    - https://www.diffus.graviti.com/
>    - https://huggingface.co/spaces/stabilityai/stable-diffusion
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2754#issuecomment-1863867724>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AN3BRCZDI4HJ2ZEXWTXM5BDYKJYGLAVCNFSM6AAAAABA3UVZAOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMYTQNRTHA3DONZSGQ>
> .
> You are receiving this because you authored the thread.Message ID:
> ***@***.***>
>


-- 
*Josh McCann*
*https://joshmccann.art/ <https://joshmccann.art/>*


*3D Modeling, 3D Texturing, 3D Renderinghttps://laserrot.me/
<https://laserrot.me/>Music Production, Sound Design, Mixing & Mastering*


---

### 评论 #5 — owenRiddy (2023-12-27T10:36:47Z)

Hey, just passing through; sorry if I'm about to be unhelpful. The torch version (`torch-2.0.1+rocm5.4.2`) looks suspicious. [Easy diffusion](https://github.com/easydiffusion/easydiffusion) has done great work supporting the unsupportable for me and I noted this snippet:

```
if is_amd_on_linux():  # hack until AMD works properly on torch 2.0 (avoids black images on some cards)
    amd_gpus = setup_amd_environment()
    if module_name == "torch":
        if "Navi 3" in amd_gpus:
            # No AMD 7x00 support in rocm 5.2, needs nightly 5.5. build
            module_version = "2.1.0.dev-20230614+rocm5.5"
            index_url = "https://download.pytorch.org/whl/nightly/rocm5.5"
```

From these logs the problem might be AUTOMATIC1111 using dependencies that don't know about the Radeon 7900 XTX. Although with the sketchy support between versions it is hard to keep track of what is expected to work.

---

### 评论 #6 — junliume (2023-12-28T19:15:51Z)

@ArtisticMusician have you tried the docker provided here? https://github.com/ROCm/composable_kernel/discussions/1032 I am using it myself, you can either try the installation, or better yet, use the provided docker which should work out of the box.

---

### 评论 #7 — ArtisticMusician (2023-12-28T19:22:01Z)

I have tried many docker variations not sire if I tried this on. Does
isbneed to run on a Linux dual boot or will WSL or VM work?

On Thu, Dec 28, 2023, 11:16 AM Jun Liu ***@***.***> wrote:

> @ArtisticMusician <https://github.com/ArtisticMusician> have you tried
> the docker provided here? ROCm/composable_kernel#1032
> <https://github.com/ROCm/composable_kernel/discussions/1032> I am using
> it myself, you can either try the installation, or better yet, use the
> provided docker which should work out of the box.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2754#issuecomment-1871430049>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AN3BRC5LLW2EAF53QI44X63YLXAPFAVCNFSM6AAAAABA3UVZAOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMYTQNZRGQZTAMBUHE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #8 — junliume (2023-12-28T19:29:13Z)

@ArtisticMusician the above docker needs to be on native Linux (Ubuntu is my env). If you meet any issues with it, please feel free to comment there and I will get it dealt with asap.

---

### 评论 #9 — ArtisticMusician (2023-12-28T19:33:59Z)

To be honest I had issues with just a ubuntu following instructions. I
would tell it to use a specific hard drive and then see that it's messing
with formatting on a completely different hdd

On Thu, Dec 28, 2023, 11:29 AM Jun Liu ***@***.***> wrote:

> @ArtisticMusician <https://github.com/ArtisticMusician> the above docker
> needs to be on native Linux (Ubuntu is my env). If you meet any issues with
> it, please feel free to comment there and I will get it dealt with asap.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2754#issuecomment-1871437653>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AN3BRC6XCWLDBULISNV24RLYLXCBLAVCNFSM6AAAAABA3UVZAOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMYTQNZRGQZTONRVGM>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #10 — drone540 (2024-01-08T13:55:36Z)

On windows you should be using the directML version of automatic1111 found here:
https://github.com/lshqqytiger/stable-diffusion-webui-directml

Make sure to add `--use-directml` to comnmand line args in `webui-user.bat` along with other options like `--precision full --no-half --no-half-vae` (if 7800xt does not support half precision)
Then run `webui-user.bat` on windows.


For Ubuntu ROCm 6.0 just came out and simplified the installation process.
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html
I have not tested this new version specifically but I assume it should work better then the version I'm running below, which can break on a Linux kernel update due to the inconsistent apt sources undoing your changes during installation


I'm running ROCm 5.7.1 I used this:
https://rocm.docs.amd.com/en/docs-5.7.1/deploy/linux/quick_start.html
Just be careful with the copy and pasting from here. Probably should do it one line at a time. As it will not fully work if you copy and paste the whole thing.

Then just use the normal automatic1111:
https://github.com/AUTOMATIC1111/stable-diffusion-webui

Then edit the `webui-user.sh` with whatever ocmmand line args then run `webui.sh`

You also may need to fake your GPU as being supported by ROCm by adding this to your `.bash_profile`
`export HSA_OVERRIDE_GFX_VERSION=10.3.0`

Also apt install this package on ubuntu if you get a TCmalloc error on startup. It will prevent a memory leak that will eventually crash the webui.
`apt install libtcmalloc-minimal4`

---

### 评论 #11 — 2eQTu (2024-01-08T18:52:51Z)

@ArtisticMusician   As others of pointed out with enough effort and hints from the experts you can probably get what you are trying to work.   But your main point stands and it feels like the ROCm team is (sadly) under-resourced within AMD as they just can't stay on top of fixing these quality of life issues impacting the wider potential customer base.   

How much would it cost AMD to add another half dozen senior FTEs to the ROCm team? And compare that to the longer term value of capturing more of the market.  I wonder if folks there have done the math.  

For example: As I type this in Jan 2024, several weeks past the ROCm 6.0 release, upstream pytorch still can't build on 6.0 nor is it even in their CI to show a failing build.   See:  https://github.com/pytorch/pytorch/pull/116270

You'd think the popular PyTorch, which ROCm itself lists right in the [quick-start guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/3rd-party/pytorch-install.html), would be working _before_ cutting a new major new release.  Seems not.

Edit to add:  To any AMD folks reading, this is not a comment on the quailty or (improving) direction of ROCm.  i.e. This is not some overly polite way of saying the team is doing bad work.  Rather, it just seems like there are more things to tackle than hands to help.  At least that's what it looks like to me from the outside.

---

### 评论 #12 — hiepxanh (2024-01-19T03:45:21Z)

The team is working hard, all about the company resource. :( 

---

### 评论 #13 — hiepxanh (2024-01-19T07:18:32Z)

@nartmada Hi, can you take a look or forward to someone on your team please? I see a small PR which would help a lot of people to work on AMD card to run model but. I was calling but no one heard. 
This issue here https://github.com/ROCm/Tensile/pull/1862

some one merge it please, my code wont move without it 😢 

---

### 评论 #14 — nartmada (2024-01-19T13:54:37Z)

@hiepxanh, let me reach out to the internal team regarding your PR.

---

### 评论 #15 — hiepxanh (2024-01-19T14:11:45Z)

thank you, godness . Thank you so so much @nartmada  help me 😢 

---

### 评论 #16 — nartmada (2024-03-22T02:36:48Z)

Hi @hiepxanh, sorry for taking longer to get back to you.  Can you please check if the PR has been merged or not?  There are a few PRs mentioned in https://github.com/ROCm/Tensile/pull/1862.  Thanks.

---

### 评论 #17 — hiepxanh (2024-03-22T03:11:33Z)

@nartmada  sadly, after that merge, [GZGavinZhao](https://github.com/GZGavinZhao) cannot able to build with 5.7 on normal windows, he have to use windows server. All we want is just make llama.cpp to work with AMD ROCm, which can unlock all normal user with AMD card can run AI on there computer. Hope we can put little effort here.
llama.cpp is the foundation for all other package for JS, Python, Native app like LM Studio to run on, so llama.cpp is the key for AMD to run AI on consumer device

https://github.com/ggerganov/llama.cpp/pull/5966#issuecomment-2012543619 

---

### 评论 #18 — nartmada (2024-03-22T03:18:14Z)

Hi @hiepxanh, please file a new ticket for the new issues you are seeing after the merge.  You will need to fill out the Issue Template so that we can try to repro and/or have a better understanding of your issue.  We will use the new ticket to further discuss/debug your issue.  Thanks.

---

### 评论 #19 — GZGavinZhao (2024-03-22T15:28:53Z)

I will file the issue I encountered today.

---

### 评论 #20 — nartmada (2024-03-31T15:05:49Z)

> I will file the issue I encountered today.

Hi @GZGavinZhao, please share the Issue# when it is available.  Thanks.

---

### 评论 #21 — GZGavinZhao (2024-04-04T12:33:46Z)

@nartmada Sorry for the delay, filed #2996. Thanks!

---

### 评论 #22 — soulhunter (2024-10-07T17:07:02Z)

I feel your pain.  I got a Vega FE a long time ago, someone recommended that I sell it and buy a 1080 ti back in the day: I did not, because of AMD's promise of AI and whatnot (and I was thrilled to have an nVidia alternative that was more open, ...).  Also Vega would seem to work better for mining (which was another motive), but the FE was not the best for that (200W!!), so that was more of a excuse (it did not really make sense).  Fast forward to today (when ROCM, finally, seems to be supported for more useful AI things), support for this card seems to have been official dropped:

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html

This one would be gfx900 (similar to the instinct MI25).  Go and check nVidia support for even older cards: 750 ti is still supported!  I just searched for driver for Linux for the 750ti and it was released just on Sep 19, 2024 (version 550.120).

I installed the latest driver on Ubuntu 24.04 and the card seems to be still there! (rocminfo) so, there is hope.  I just wanted to ask AMD: please, unless you have a really good reason to do it, do not drop these cards just yet!!  I will try this with Ollama or similar in the next few days and report back.  I really cannot currently afford to buy an nVidia GPU (sorry, if I cannot make this Vega work, I will probably give up on AMD cards for ML: this was not a cheap card).  If this does not work, I will likely sell it and then save, and save, and save until I get get an nVidia GPU.

And yes, I know AMD is more open-source friendly regarding the drivers (which has been the main reason why I have tried to support AMD as much as I can, with my little budget), but what good is it if they do not work or if hardware just gets dropped out of the driver (this is my main grievance).  They even announced it for deep-learning and similar:

https://www.reddit.com/r/MachineLearning/comments/6boswp/n_radeon_vega_frontier_edition/

I am glad that now it looks like AMD finally has useful ML / AI solutions.

But hey, at least it worked well for quite a few games (not the best, but at least I could game with it)... so, at least I got some enjoyment from it!

---
