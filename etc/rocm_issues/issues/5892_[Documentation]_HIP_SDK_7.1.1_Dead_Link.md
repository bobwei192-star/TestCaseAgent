# [Documentation]: HIP SDK 7.1.1 Dead Link

> **Issue #5892**
> **状态**: closed
> **创建时间**: 2026-01-23T12:51:37Z
> **更新时间**: 2026-01-23T21:43:57Z
> **关闭时间**: 2026-01-23T21:43:57Z
> **作者**: prodkt
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5892

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Description of errors

https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html

... click on the 'HIP SDK' Download Link

... Accept/Click terms/button to Download

Dead Link.

### Attach any links, screenshots, or additional evidence you think will be helpful.

<img width="1157" height="345" alt="Image" src="https://github.com/user-attachments/assets/b570b1bd-28b0-40dc-8497-557ecf544efd" />

<img width="1345" height="665" alt="Image" src="https://github.com/user-attachments/assets/842f3399-e795-42ab-ad42-04bdaa85e15a" />

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2026-01-23T14:55:32Z)

Hey @prodkt, the link is working fine on my end - it might've been an intermittent issue. Could you please give it a try again and let me know if it's working?

---

### 评论 #2 — prodkt (2026-01-23T16:08:35Z)

@harkgill-amd Still not sure of exactly why I'm unable to grab it from a workstation. I'd tried a couple different boxes and even networks. What I ultimately had to do is download it from my phone into Drive -- while on the same network even and that worked. 

The culprit might be from within the PDF viewer as its the only thing I've seen throw error. Even if it where I hit the direct link to the executable from my phone bypassing the form action & button (unintentionally) and was successful able to download. From that experience it doesn't appear there's a hard requirement that some sort of handshake take place just to access the file. And if there isn't just maybe its that form that's invalidating the request due to the form errors.

Anyway, thanks @harkgill-amd this is resolved.

<img width="1251" height="850" alt="Image" src="https://github.com/user-attachments/assets/779977bd-fe98-4c64-8160-e31021004234" />

<img width="642" height="1389" alt="Image" src="https://github.com/user-attachments/assets/2e32f247-8ab4-4767-ae99-e54ae3afd1d9" />

---

### 评论 #3 — harkgill-amd (2026-01-23T16:18:04Z)

> Even if it where I hit the direct link to the executable from my phone bypassing the form action & button (unintentionally) and was successful able to download. From that experience it doesn't appear there's a hard requirement that some sort of handshake take place just to access the file. And if there isn't just maybe its that form that's invalidating the request due to the form errors.

Ah that is quite odd. I'm curious to see if the issue is exclusive to the newer release or generic - does this happen with all the download links (ex. ROCm 6.4.2 and 6.2.4)?

---

### 评论 #4 — harkgill-amd (2026-01-23T21:43:57Z)

I was just informed there was an issue going on in our backend that has since been resolved. Closing this issue out but if anyone does see this issue, please leave a comment and I'll reopen this thread.

---
