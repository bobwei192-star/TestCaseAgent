# [Issue]: dkms compilation issues on Debian testing: objtool (dma_resv->seq is missing)

> **Issue #3379**
> **状态**: open
> **创建时间**: 2024-06-29T15:03:04Z
> **更新时间**: 2025-06-03T01:29:33Z
> **作者**: nairboon
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3379

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

When compiling rocm with the stock kernel (6.8.12) from Debian testing the following error appears

```
DKMS make.log for amdgpu-6.7.0-1781449.22.04 for kernel 6.8.12-amd64 (amd64)
/tmp/amd.A0EtTvUI/Makefile:52: *** dma_resv->seq is missing. exit....  Stop.
```

However I believe this error message is misleading. The amdgpu-dkms ./configure logs show that basically all checks fail due to:
`objtool: SRCARCH variable not defined ` thus the autoconf check `AC_AMDGPU_DMA_RESV_FENCES` fails because of the build error from objtool and not because of the check. This check sets `HAVE_DMA_RESV_SEQ_BUG`, which is why the dkms builds on recent Debian fails with `dma_resv->seq is missing`.

Newer kernel build tools on Debian (linux-kbuild-6.*) ship multiple objtools:
```
/usr/lib/linux-kbuild-6.8.12/tools/objtool/objtool
/usr/lib/linux-kbuild-6.8.12/tools/objtool/objtool.real-powerpc
/usr/lib/linux-kbuild-6.8.12/tools/objtool/objtool.real-x86
```

where `objtool` expects an environment variable `SRCARCH` to be set to `x86`, otherwise it fails.

I guess somewhere in the autoconf/configure scripts this SRCARCH needs to be properly set to build on recent Debian.

As a workaround you can rename `objtool.real-x86` to `objtool` unless you want to cross-compile.


OS: Debian Testing
ROCM: 6.1.1 & 6.1.2

---

## 评论 (18 条)

### 评论 #1 — kentrussell (2024-07-02T13:05:50Z)

@ppanchad-amd Can you add this information to the JIRA that got made for https://github.com/ROCm/ROCm/issues/3036 ? 

---

### 评论 #2 — ppanchad-amd (2024-07-02T14:12:17Z)

@nairboon @kentrussell I created JIRA ticket for issue #3036 but it was rejected by KCL team since packaged driver is not supported on Debian.  Please re-open the ticket if issue still occurs when Debian is officially supported. Thanks!

---

### 评论 #3 — nairboon (2024-07-07T14:12:24Z)

> @nairboon @kentrussell I created JIRA ticket for issue #3036 but it was rejected by KCL team since packaged driver is not supported on Debian. Please re-open the ticket if issue still occurs when Debian is officially supported. Thanks!

I know Debian is not officially supported, however this issue is kind of preventing to support it at least unofficially. Maybe you can tag it as wishlist or something instead of just closing. Unless you never plan to ever support Debian?

---

### 评论 #4 — jasonriedy (2025-02-04T20:33:33Z)

Ahem. Debian now is included under https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html . And we're not allowed to mention those other tickets/issues here.9

---

### 评论 #5 — schung-amd (2025-02-05T17:12:57Z)

Hi @nairboon, is this still an issue? What steps are you taking to build ROCm? 

---

### 评论 #6 — jasonriedy (2025-02-05T17:19:18Z)

I cannot speak for the original poster directly, but the same issue is occurring building amdgpu-dkms on 6.12.11. The relevant step would be to install amdgpu-dkms.

---

### 评论 #7 — schung-amd (2025-02-05T19:22:33Z)

Marking as a feature request. We currently have official support for Debian 12 + kernel 6.1 only (https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html), will check to see what barriers exist for newer kernel version support. This may be workaround-only for now as our Debian support is new and I'm not sure how much is in scope.

---

### 评论 #8 — ckastner (2025-02-06T13:00:01Z)

Note that the freeze for Debian 13 ("Trixie") will start in March, and we can probably expect a final release sometime around or after DebConf in July.

So if AMD wants to support the kernel of the next stable release (in a 2-year release cadence), it would probably be best to address the issue rather sooner than later.

---

### 评论 #9 — ivucica (2025-02-12T17:03:10Z)

Note that this affects 6.11, but 6.12 is _also_ affected by further issues, such as #4316 involving some issue with `kvrealloc`, which _may_ also impact the freeze. (I did not check if the intended kernel for Debian 13 is 6.11 or 6.12.)

---

### 评论 #10 — yuanwei2023 (2025-02-28T02:36:20Z)

You can find kernel version release info from the link, Debian 12 kernel is supported,  I don`t see kernel 6.11/6.12 on debian is supported so far. (compatibility support)
https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#operating-systems-and-kernel-versions

#install amdgpu dkms 
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/amdgpu-install.html#debian

sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.3.3/ubuntu/jammy/amdgpu-install_6.3.60303-1_all.deb
sudo apt install ./amdgpu-install_6.3.60303-1_all.deb
sudo apt update

amdgpu-install --usecase=dkms

sudo dkms status



---

### 评论 #11 — jasonriedy (2025-02-28T17:46:29Z)

FYI, upstream's is working just fine for ROCm development. I'm not at all sure what this driver adds. It certainly detracts from being able to use all the other enhancements in more recent kernels. I'm running linux-image-6.12.16-amd64 from Debian unstable.

The only problem I've encountered was from trying this repo's driver. It blacklisted the kernel driver on installation but did not un-blacklist it on removal.

---

### 评论 #12 — schung-amd (2025-02-28T19:02:00Z)

The packaged dkms driver is the version we have tested and verified works with the associated ROCm version at the time of release, and allows users to ensure that their driver is compatible with their ROCm version whenever they install or update ROcm. My understanding is that amdgpu-dkms incorporates patches and features from multiple sources which are eventually mirrored upstream, so it's certainly possible that some version of the upstream kernel driver is compatible with a given ROCm version.

That being said, we can't make any guarantees here since we haven't fully tested other driver versions, and by extension we can't make any guarantees about ROCm functionality on Debian 12 with kernel versions outside of our official support (6.1). `objtool` renaming sounds like a reasonable workaround for now until we've scoped out official support for other kernel versions. It doesn't seem like this support is high priority at the moment however.

---

### 评论 #13 — jasonriedy (2025-03-04T19:45:10Z)

That's nice. I'm not pulling my AMD-procured machine back that many kernel versions and restricting my tools similarly.

Upstreaming things ASAP is important. If they matter and are not noise.

---

### 评论 #14 — scodesido (2025-03-16T16:26:18Z)

Same issue here, the "solution" of downgrading the kernel seems quite bad. I've tried the lowest kernel in the backports, 6.9, and it does not work because of these issues. The stable kernel is 6.1, which I cannot use because it breaks other stuff in my relatively new computer (e.g. audio). 

> As a workaround you can rename objtool.real-x86 to objtool unless you want to cross-compile.

I guess this would cause problems with other packages? I tried to do it in desperation, but then I get some compilation error because of kvmalloc. Really quite messy.

---

### 评论 #15 — jasonriedy (2025-03-16T16:58:41Z)

Yeah... That ollama problem feels like it'll be bumping up the priority... Plus Framework's Strix Halo Linux machine. As with many of our ROCm aspects, the support approach needs to adapt to the market.

---

### 评论 #16 — alsgnet (2025-05-28T19:17:38Z)

The issue is fixed at AMD and upcoming release(s) will include the fix. Thanks for reporting!

---

### 评论 #17 — wkernkamp (2025-05-30T15:40:16Z)

Glad it is fixed.  I have the issue now.  Can you post a debian archive with fix to linux-kbuild-6.1 or a newer version of linux-kbuild to install?


---

### 评论 #18 — alsgnet (2025-06-03T01:29:32Z)

I can't post a new driver before it is released. But what I can do is to post a patch so you'll be able to apply it in your system and rebuild dkms modules installation that failed. Will it work for you?

---
