# Question about best ROCm version for gfx906 (on windows)

> **Issue #5177**
> **状态**: open
> **创建时间**: 2025-08-10T20:46:36Z
> **更新时间**: 2025-08-12T02:49:08Z
> **作者**: janhec
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5177

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Dear all,
I have ROCm working on windows 11 using version 5.7.1. The old version was selected as it appears the last that fully supports Radeon Pro VII.
I would really like to migrate to version 6.x.x having more fft support, also in the examples, but it has to work on Radeon Pro VII.
A minor lack of support is not critical, as long as there are FFT examples that work.
Please advice whether I should install additional 6.x.x and what version I can use best.
The sudden transfer from (end of) support to support matrix has me confused.
Thanx in advance!

---

## 评论 (4 条)

### 评论 #1 — janhec (2025-08-11T20:16:36Z)

Not getting a timely reply, I tried installing ROCm 6.1.2. It won't accept gfx906 as a target. So 5.7.1 is it.
Unfortunately, ROCm 5.7.1 appears to have limited FFT support, at least in terms of examples.
My opinion of AMD(-gpu) is now: nice hardware, sucking software.
Almost a pity AMD ever bought ATI, probably, although there's no knowing ATI could have done a software effort comparable to cuda.
I still like my AMD CPU and still hope my Radeon Pro VII will be included again in the targets.

---

### 评论 #2 — harkgill-amd (2025-08-11T20:34:58Z)

Hi @janhec, while the HIP SDK no longer supports gfx906, you can still build ROCm components, including rocFFT, from source with [TheRock](https://github.com/ROCm/TheRock). TheRock is a lightweight build system for ROCm which still maintains support for the Radeon PRO VII and other older architectures https://github.com/ROCm/TheRock/blob/main/cmake/therock_amdgpu_targets.cmake#L45 - this should enable FFT examples to work.

You can find the build instructions for Windows here https://github.com/ROCm/TheRock?tab=readme-ov-file#setup---windows-11-vs-2022. Please let me know if you have any questions.

---

### 评论 #3 — janhec (2025-08-11T21:08:45Z)

Thank you, that sounds great where I didn't think this would be happening.

On Mon, Aug 11, 2025 at 10:35 PM harkgill-amd ***@***.***>
wrote:

> *harkgill-amd* left a comment (ROCm/ROCm#5177)
> <https://github.com/ROCm/ROCm/issues/5177#issuecomment-3176812799>
>
> Hi @janhec <https://github.com/janhec>, while the HIP SDK no longer
> supports gfx906, you can still build ROCm components, including rocFFT,
> from source with TheRock <https://github.com/ROCm/TheRock>. TheRock is a
> lightweight build system for ROCm which still maintains support for the
> Radeon PRO VII and other older architectures
> https://github.com/ROCm/TheRock/blob/main/cmake/therock_amdgpu_targets.cmake#L45
> - this should enable FFT examples to work.
>
> You can find the build instructions for Windows here
> https://github.com/ROCm/TheRock?tab=readme-ov-file#setup---windows-11-vs-2022.
> Please let me know if you have any questions.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5177#issuecomment-3176812799>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/ADTBHLZGZ2QSO44YFXJEFMT3ND5APAVCNFSM6AAAAACDRXHKVSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTCNZWHAYTENZZHE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #4 — slavap (2025-08-12T02:46:41Z)

Under Linux 6.4.0 works with "hack", see https://github.com/ROCm/ROCm/issues/4625#issuecomment-2899838977

And probably 6.4.3 will work, although I have not tried it yet, at least I see 6.4.3 rocblas compiled for gfx906 https://archlinux.org/packages/extra-testing/x86_64/rocblas/

---
