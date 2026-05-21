# [Issue]: hipcc requires non-existent libxml2.so.2 - ROCm 7.2.1 on Ubuntu 26.04

> **Issue #6194**
> **状态**: open
> **创建时间**: 2026-04-29T22:06:12Z
> **更新时间**: 2026-05-15T17:13:15Z
> **作者**: robegan21
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6194

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

After installing ROCm 7.2.1 on Ubuntu 26.04 successfully (without dkms - see Issue #6193)  hipcc was not functioning because /opt/rocm-7.2.1/lib/llvm/bin/ld.lld is hard-coded to require libxml2.so.2.  Ubuntu 26.04 only has libxml2.so.16 so building anything with hipcc failed because it could not find a compatible shared library for libxml2

The fix I implemented was to download a version of libxml2.so.2 and install it into /lib/x86_64-linux-gnu

wget https://launchpad.net/ubuntu/+archive/primary/+files/libxml2_2.12.7+dfsg+really2.9.14-0.4ubuntu0.4_amd64.deb
sudo dpkg --fsys-tarfile libxml2_2.12.7+dfsg+really2.9.14-0.4ubuntu0.4_amd64.deb | tar -xO ./usr/lib/x86_64-linux-gnu/libxml2.so.2.9.14 > /lib/x86_64-linux-gnu/libxml2.so.2.9.14
sudo ln -s /lib/x86_64-linux-gnu/libxml2.so.2.9.14 /lib/x86_64-linux-gnu/libxml2.so.2




### Operating System

Ubuntu 26.04 (Resolute Raccoon)

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

ROCm 7.2.1

### ROCm Component

HIP

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — andyskw (2026-05-06T16:59:21Z)

Confirming this on **AMD Ryzen AI 9 HX 470 / Radeon 890M (gfx1150, Strix Point)** + ROCm 7.2.1 + Ubuntu 26.04 — same `lld: error while loading shared libraries: libxml2.so.2` blocking a vLLM source build (HIP compiler test fails at cmake configure).

Background for anyone hitting this: libxml2 bumped its SONAME from `2` to `16` in v2.14 (April 2025), so Ubuntu 26.04 ships only `libxml2.so.16` (`libxml2-16` package, v2.15.2). ROCm 7.2 binaries were linked pre-bump.

A simpler workaround that doesn't require pulling an older `.deb` from Launchpad — just symlink the new SONAME to the old name:

```bash
sudo ln -sf /usr/lib/x86_64-linux-gnu/libxml2.so.16 /usr/lib/x86_64-linux-gnu/libxml2.so.2
```

`lld` then emits a benign warning on every link (`/lib/x86_64-linux-gnu/libxml2.so.2: no version information available`) because versioned-symbol tags from SONAME=2 are absent — but linking succeeds and the produced binaries run correctly. libxml2 has been ABI-stable for years; the v2.14 SONAME bump was for symbol-versioning hygiene, not an actual ABI break.

Real fix should be on ROCm side: either rebuild `lld` against `libxml2.so.16`, or ship a private copy of `libxml2.so.2` next to the bundled toolchain.

---

### 评论 #2 — robegan21 (2026-05-06T18:26:59Z)

On my system I also tried that simpler workaround, and ran in to that same benign warning with some builds but later also encountered real broken builds downstream where it refused to link the binary.  However I didn't keep those logs.  That is when I pivoted to installing the older version of the xml2 shared library.  Agree the real fix is on the ROCm side.

---

### 评论 #3 — w-sky (2026-05-11T13:36:35Z)

Have you tried 7.2.3 ?

---

### 评论 #4 — lucbruni-amd (2026-05-11T19:38:23Z)

>Have you tried 7.2.3 ?

I can reproduce this with ROCm 7.2.3 and Ubuntu 26.04. I will gather some more context and update this issue when this is addressed on the ROCm side.

---

### 评论 #5 — BoneHorror (2026-05-15T17:13:15Z)

Fwiw essentially this same issue was reported and previously closed here - https://github.com/ROCm/ROCm/issues/6046
It seems to be resolved in what is I think one of the beta ROCm versions, 7.13, otherwise the advice was to download and export older versions of libxml and libicu


---
