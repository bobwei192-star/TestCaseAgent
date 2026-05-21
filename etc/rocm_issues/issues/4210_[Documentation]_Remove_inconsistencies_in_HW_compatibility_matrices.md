# [Documentation]: Remove inconsistencies in HW compatibility matrices

> **Issue #4210**
> **状态**: closed
> **创建时间**: 2024-12-30T20:56:48Z
> **更新时间**: 2025-06-26T18:45:41Z
> **关闭时间**: 2025-06-26T18:45:41Z
> **作者**: winfriedgerlach
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/4210

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

The compatiblity matrices are amongst the first pages that a prospective ROCm user reads. And this first impression is not the best, to say the least. The confusion about ROCm compatibility with certain GPUs is apparent in many Stack Overflow and Reddit posts as well as issues in this bug tracker, cf. #2788, #2972, #3863,...

There are at least 5 different places where HW compatibility is listed in the ROCm documentation and most contradict each other:
1. https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html
2. https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html
3. https://rocm.docs.amd.com/projects/radeon/en/latest/index.html
4. https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/native_linux/native_linux_compatibility.html
5. https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html

Note that 1. and 2. are from the "core" documentation while 3., 4., 5. are from the "radeon" documentation.

I have the feeling that it may be better to drop 4. and 5. entirely to have a "single source of truth", but you will know better whether this would have unwanted side effects.

Comparing 1. and 2.:
* AMD Instinct hardware is obviously not supported on Windows. It would be nice if this was mentioned on 2. explicitly instead of just implicitly omitting the "AMD Instinct" tab.
* "Radeon Pro" models: 1. lacks a row for W6600 and W5500 while 2. lacks a row for V710. Again, I would prefer explicitly mentioning incompatibility over just omitting the models, so the reader knows that Linux and Windows indeed support different models and this is not just a documentation inconsistency.
* "Radeon" models: 1. lacks rows for 7600, 7700 XT, 7800 XT, and all 6000 models while 2. lacks rows for 7900 GRE and Radeon VII. Note that 5. lists the 7900 GRE as supported under Windows, so at least this model should probably be added to 2. AFAIU from many forum posts and issue comments, 7600, 7700 XT, and 7800 XT work fine under Linux, so they should probably be added to 1., even if they are not "officially" or "fully" supported, maybe with an exclamation mark instead of a checkmark (students and hobbyists will accept some pain if support is "limited").

Regarding 3., 4., 5.:
* The "Radeon" documentation has obviously generally not been updated to ROCm 6.3.x / Ubuntu 24.04 / lower-end Radeon 7000 cards. This is a real pity as support for lower-end Radeon 7000 cards seems to be an FAQ. I couldn't even find these "Radeon" docs on Github, are they hosted somewhere else?
* Page 5. lists "Radeon PRO W7800 48GB" while 4. doesn't; is this a real compatibility difference or just a documentation inconsistency?
* Pages 3. and 5. do not list the 7600/7700 XT/7800 XT that were added to 2. with #2788.

Neither 1., 2., 3., 4., or 5. list the RX 7600 XT (16 GB). @nartmada mentions in #2972 that the 7600 XT is indeed not supported, but it is unclear whether this information is meanwhile outdated. Again, I would prefer to explicitly list this card as "unsupported" if this is the case, to avoid first user confusion. If the 7600 XT is _really_ not supported, I'd consider this to be quite unfortunate, as the 7600 XT would be the ideal GPU for students and hobbyists on a tight budget who want to get in the ROCm game - remember, today's students and hobbyists are tomorrow's professional users!

Finally, I am a little confused about https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/shared/compatibility.html which looks like an abandoned older compatibility matrix. It seems outdated (despite for "latest" in the URL), points to ROCm 6.0.2/5.7. Maybe check for links to this page and remove it?

Thanks and have a nice end of 2024!


### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2024-12-30T21:20:13Z)

Hi @winfriedgerlach. Internal ticket has been created to fix docs. Thanks!

---

### 评论 #2 — harkgill-amd (2025-02-11T19:06:11Z)

Hi @winfriedgerlach, thanks for pointing out the page at https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/shared/compatibility.html. It was an artifact of a previous docs release that slipped through and has since been removed. We're also doing some further clean up on this portal, specifically with the version list and previous release flyout so keep an eye out for that.

Before I dive in to the specific points you brought up, I'd like to highlight the difference between all the offerings that the support matrices you've linked refer to. For each project, I've linked the documentation portal and relevant support matrix.

[ROCm](https://rocm.docs.amd.com/en/latest/) - https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html

- The main ROCm project that includes all the ROCm libraries, tools and runtimes.

[HIP SDK for Windows](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/) - https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html

- A subset of the ROCm platform intended for usage on Windows. You can find the specific components this project supports [here](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/component-support.html).

[ROCm on Radeon](https://rocm.docs.amd.com/projects/radeon/en/latest/) - https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/native_linux/native_linux_compatibility.html

- For usage of Radeon PRO or Radeon GPUs in a workstation setting with display connected.

[ROCm on WSL](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html) - https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html

- ROCm on Radeon release with WSL support included.

Each of these projects have varying levels of official GPU support defined in their support matrices. With that being said, I do agree that it can be a bit confusing navigating each portal and understanding the difference in support for a given GPU. We are constantly trying to improve this experience and are open to any further suggestions that you and other users may have.

Going through the concerns brought up in this issue

1. AMD Instinct hardware is obviously not supported on Windows. It would be nice if this was mentioned on 2. explicitly instead of just implicitly omitting the "AMD Instinct" tab.
"Radeon Pro" models: 1. lacks a row for W6600 and W5500 while 2. lacks a row for V710. Again, I would prefer explicitly mentioning incompatibility over just omitting the models, so the reader knows that Linux and Windows indeed support different models and this is not just a documentation inconsistency.

I've brought up the idea of adding more unsupported models in our support matrix with the docs team. Will update this thread on the feasibility of implementing this request.

2. "Radeon" models: 1. lacks rows for 7600, 7700 XT, 7800 XT, and all 6000 models while 2. lacks rows for 7900 GRE and Radeon VII. Note that 5. lists the 7900 GRE as supported under Windows, so at least this model should probably be added to 2

Here, you're referring to the standard ROCm on Linux installation. Unfortunately, we do not currently support the GPUs you've listed as noted by their exclusion from the support matrix. See the following statement in the [Supported GPUs](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus) section.

> If a GPU is not listed on this table, it’s not officially supported by AMD.

3. AFAIU from many forum posts and issue comments, 7600, 7700 XT, and 7800 XT work fine under Linux, so they should probably be added to 1., even if they are not "officially" or "fully" supported, maybe with an exclamation mark instead of a checkmark (students and hobbyists will accept some pain if support is "limited").

These SKUs are not supported but limited functionality can be enabled by using a workaround to mimic a supported target. We try to steer clear of advertising support for this case to maintain a clear definition of what support means.  

4. The "Radeon" documentation has obviously generally not been updated to ROCm 6.3.x / Ubuntu 24.04 / lower-end Radeon 7000 cards. This is a real pity as support for lower-end Radeon 7000 cards seems to be an FAQ. I couldn't even find these "Radeon" docs on Github, are they hosted somewhere else?

6.3.2 ROCm on Radeon support has recently been released and the [docs ](https://rocm.docs.amd.com/projects/radeon/en/latest/index.html )have been updated to reflect this. Ubuntu 24.04 support is also included in this release. As for the lower end Radeon cards, the lack of support has been an ongoing discussion and we do understand that this is a need for the community. We are hoping to expand our support to more GPUs going forward this year. The ROCm on Radeon docs are hosted in an internal repository which I believe shouldn't be the case. I'll look into having them ported into a public facing repo in our ROCm organization. 

5. Page 5. lists "Radeon PRO W7800 48GB" while 4. doesn't; is this a real compatibility difference or just a documentation inconsistency?

Not sure if I'm missing something here or if there were recent changes, but currently, both matrices show support for the Radeon PRO W7800 48GB.

6. Pages 3. and 5. do not list the 7600/7700 XT/7800 XT that were added to 2. with https://github.com/ROCm/ROCm/issues/2788.

The ticket linked here references support for these GPUs in the HIP SDK for Windows. The relevant matrix for this project was updated and still does include these SKUs. Page 3 (ROCm on Radeon) and 5 (ROCm on WSL) do not support these GPUs.

We really do appreciate the feedback on the documentation and I'll keep you updated on the progress of the tasks mentioned in 1 and 6. Please let me know if you have any further questions about the documentation.






---

### 评论 #3 — runiq (2025-04-03T07:03:08Z)

> We are hoping to expand our support to more GPUs going forward this year.

Just as a point of confirmation: Is it planned _at all_ to support ROCm on the RX 7600 XT? I'm deliberating whether I should return my card or keep it.

---

### 评论 #4 — harkgill-amd (2025-06-26T18:45:41Z)

Wanted to follow up on this ticket and give a quick update on the major concerns.
1. Confusion surrounding different portals for different projects.
a. Our docs team is aware of this and are in the early stages of scoping an appropriate solution for this. I can't provide a specific timeline as to when changes for this will go live but please be assured that there is work being done to address this.

2. Denoting unsupported SKUs with a "X" in the compatibility matrices
a. I had a discussion with the docs team regarding this and we've chosen to continue with the status quo. That is, a checkmark for all SKUs that are supported and a "X" for SKUs that were previously supported but have been dropped in the latest release. This helps keep the matrix clear and concise. The confusion stems from (1) with different projects having different support catalogs. We hope to make this clearer in the future.
 
3. ROCm on Radeon documentation not being public
a. Thanks to this post, the ROCm on Radeon docs will be hosted in a public repository within the ROCm org. The repo should go public within the next couple weeks.

4. 7600XT and additional SKU support.
a. Since this issue was first created, we've added official support for the RX 7800 XT. For the remaining cards you mentioned, our new build platform, [TheRock](https://github.com/ROCm/TheRock/), supports building ROCm for multiple SKUs including [gfx1102/7600XT](https://github.com/ROCm/TheRock/blob/main/cmake/therock_amdgpu_targets.cmake#L69). While TheRock doesn't currently encompass every component, it's a step in the right direction, enabling user's to get started with ROCm. 

I wanted to say thank you again for providing this feedback. It's been a catalyst for a lot of discussion and change in regards to our documentation. I'll close out this issue for now but feel free to leave a comment if you have any questions.


---
