# Adrenalin AI Bundle fails to create virtual environment

> **Issue #5909**
> **状态**: closed
> **创建时间**: 2026-01-28T15:25:35Z
> **更新时间**: 2026-03-18T17:49:22Z
> **关闭时间**: 2026-03-18T17:49:22Z
> **作者**: harkgill-amd
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5909

## 负责人

- harkgill-amd

## 描述

Originally reported in https://github.com/ROCm/ROCm/issues/5871#issuecomment-3792900807.

After selecting "Create a Virtual Environment" in the AI Bundle options, the command block that's supposed to house the `pip install` commands is empty.

<img width="1092" height="917" alt="Image" src="https://github.com/user-attachments/assets/5961dae0-0aee-45f8-9926-caad48c23a45" />

In this case, opting to create the virtual environment fails with the following error,

<img width="754" height="525" alt="Image" src="https://github.com/user-attachments/assets/a56d54a3-f823-483b-8255-3b3d0476f9ad" />

---

## 评论 (9 条)

### 评论 #1 — brubeedoobee (2026-01-29T00:28:07Z)

[amddime_CheckForUpdates_2026_01_24_12_00_00_036.zip](https://github.com/user-attachments/files/24924399/amddime_CheckForUpdates_2026_01_24_12_00_00_036.zip)

Let me know if these are the correct logs.

---

### 评论 #2 — harkgill-amd (2026-01-29T21:42:09Z)

Thanks! Could you also share the logs from `C:\Program Files\AMD\CIM\Log`?

---

### 评论 #3 — brubeedoobee (2026-01-30T14:19:41Z)

You're everywhere, and I appreciate it. 
 [additional logs.zip](https://github.com/user-attachments/files/24967239/additional.logs.zip)

---

### 评论 #4 — harkgill-amd (2026-01-30T16:50:54Z)

We just made some changes configuration changes on our end - could you try relaunching the AI bundle and checking if the "Create Venv" option is working correctly now?

---

### 评论 #5 — brubeedoobee (2026-01-31T18:33:12Z)

"Just tested - no change. The 'Create Venv' option still fails with the same behavior as before. Same installer (amd-software-adrenalin-edition-26.1.1-minimalsetup-260119_web), same result.
Do I need to download a new version of the installer, or should your server-side changes have been reflected automatically? If you need new logs, let me know which ones."
Why this matters:

Either their server-side changes didn't propagate correctly
Or there's still an underlying issue they haven't fixed
Or (less likely) you do need an updated installer despite what they implied

---

### 评论 #6 — harkgill-amd (2026-02-05T15:09:12Z)

The changes (Pytorch Versioning update) are actually available through the AMD Install Manager. Could you open it up and navigate to the AI Bundle section

<img width="867" height="589" alt="Image" src="https://github.com/user-attachments/assets/0614dba9-9644-4609-9e6e-963ac2bb9918" />

And then select the "Install" option for Pytorch,

<img width="860" height="583" alt="Image" src="https://github.com/user-attachments/assets/16da9725-42d4-47d0-b5c7-287f1ccbb533" />

This'll set you up with the latest PyTorch 2.9.1 from our side which should then allow your "Create Virtual Environment" option in Adrenalin to work.

---

### 评论 #7 — brubeedoobee (2026-02-06T16:37:51Z)

<img width="1375" height="878" alt="Image" src="https://github.com/user-attachments/assets/62b62768-ccd6-4990-b152-0b4b33087b59" />

---

### 评论 #8 — harkgill-amd (2026-02-06T19:12:35Z)

Is the "Create Venv" option still not working despite being on the latest PyTorch. If so, could you share the latest logs at `C:\Program Files\AMD\CIM\Log` and `C:\Program Files\AMD\AMDInstallManager\Logs`. Apologies for the back and forth - we haven't been able to reproduce this on our end yet.

---

### 评论 #9 — harkgill-amd (2026-03-18T17:49:22Z)

Closing this out but if anyone does still see this issue - please leave a comment and I'll reopen the ticket. 

---
