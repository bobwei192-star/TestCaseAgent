# Help CLBlast (The tuned OpenCL BLAS library) by tuning for more AMD chips

> **Issue #2161**
> **状态**: closed
> **创建时间**: 2023-05-22T23:22:39Z
> **更新时间**: 2024-08-01T15:14:45Z
> **关闭时间**: 2024-08-01T15:14:45Z
> **作者**: mikkovedru
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2161

## 描述

CLBlast ( https://github.com/CNugteren/CLBlast ) is a lightweight, performant, and tunable OpenCL BLAS library.

It is used in, among many other projects, [whisper.cpp](https://github.com/ggerganov/whisper.cpp) , a very popular high-performance inference of [OpenAI's Whisper](https://github.com/openai/whisper).

Unfortunately CLBlast's [the list of already tuned-for devices](https://github.com/CNugteren/CLBlast/blob/master/doc/tuning.md#already-tuned-for-devices) is lacking and there are actually more Nvidia GPUs (which have a better alternative in cuBLAS) than AMD's.

It would be nice to drastically improve the situation. I did my part by sending the tuning results of my AMD card. But that's where my power ends. This current post is the only other avenue I could come up with to help with the efforts.

I kindly implore:
1. If there are people with non-tuned GPUs reading my message, I hope that you decide to make a personal contribution and help the project by tuning it to your GPU.
2. I hope that people from the ROCM project understand the importance of CLBlast and how much AMD/ROCM/AI can be helped by expanding the list of tuned AMD GPUs. You have access to all the GPUs and it would be a trivial small side-project to tune all of them at the same time. If this issue is not up to ROCM people's valley of responsibilities, I hope you will forward my request to other AMD people who can make it happen (be it the marketing or engineering side).

Tuning and submitting the results is very easy:
1. Download https://github.com/CNugteren/CLBlast
2. Tune the entire library for your device by running the following commands (starting from the root of the CLBlast folder):
```
mkdir build
cd build
cmake -DTUNERS=ON ..
make
make alltuners
python ../scripts/database/database.py . ..
make
```
The process will take a couple of hours.
3. Collect all the created `.json` files in the `build` directory, pack them into the .zip file, and send your [tuning results into this post](https://github.com/CNugteren/CLBlast/issues/1).

---

## 评论 (4 条)

### 评论 #1 — saadrahim (2023-05-25T02:24:12Z)

Have you seen our BLAS libraries?
https://rocm.docs.amd.com/en/latest/reference/gpu_libraries/linear_algebra.html

They are already tuned for many GPUs.

---

### 评论 #2 — lhl (2023-06-05T15:59:03Z)

I think this is still a good PSA (or something for AMD to submit any missing models officially) since many projects are using CLBLast. For example, llama.cpp's main way of getting AMD GPUs to work atm is with CLBlast.

@mikkovedru is there a list somewhere of already tuned models? I have a Radeon VII (gfx906) that I can submit if it hasn't been done yet.

---

### 评论 #3 — CNugteren (2023-06-06T07:32:42Z)

> is there a list somewhere of already tuned models?

It is here:
https://github.com/CNugteren/CLBlast/blob/master/doc/tuning.md

>  I have a Radeon VII (gfx906) that I can submit

It is not in the list above, however someone else submitted the Radeon VII 3 days ago [here](https://github.com/CNugteren/CLBlast/issues/1#issuecomment-1574727296), I still need to add it. So no need, but thanks for the offer :+1: 

---

### 评论 #4 — ppanchad-amd (2024-05-13T17:38:49Z)

@mikkovedru Is this ticket still relevant? If not, please close the ticket. Thanks!

---
