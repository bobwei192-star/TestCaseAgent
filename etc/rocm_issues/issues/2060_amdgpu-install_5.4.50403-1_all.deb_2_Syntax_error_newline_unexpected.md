# /amdgpu-install_5.4.50403-1_all.deb: 2: Syntax error: newline unexpected

> **Issue #2060**
> **状态**: closed
> **创建时间**: 2023-04-18T08:56:33Z
> **更新时间**: 2023-04-22T18:52:15Z
> **关闭时间**: 2023-04-22T18:52:15Z
> **作者**: Dvalin21
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2060

## 描述

Every time I try to install the latest from deb file, I get this error. Is there an issue with the download?


---

## 评论 (2 条)

### 评论 #1 — Thyre (2023-04-18T11:30:26Z)

Are you actually using `dpkg` or `apt` to install the package? Seems like you're trying to run the `.deb` file as an executable, which will not work. 

These steps are shown in the documentation (Ubuntu 22.04):
```bash
sudo apt-get update
wget https://repo.radeon.com/amdgpu-install/5.4/ubuntu/jammy/amdgpu-install_5.4.50400-1_all.deb
sudo apt-get install ./amdgpu-install_5.4.50400-1_all.deb
```

---

### 评论 #2 — Dvalin21 (2023-04-18T20:47:32Z)

You know what your right. DUH! Thanks for this. Its been a long few weeks.

On Tue, Apr 18, 2023 at 6:30 AM Jan André Reuter ***@***.***>
wrote:

> Are you actually using dpkg or apt to install the package? Seems like
> you're trying to run the .deb file as an executable, which will not work.
>
> These steps are shown in the documentation (Ubuntu 22.04):
>
> sudo apt-get update
> wget https://repo.radeon.com/amdgpu-install/5.4/ubuntu/jammy/amdgpu-install_5.4.50400-1_all.deb
> sudo apt-get install ./amdgpu-install_5.4.50400-1_all.deb
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/RadeonOpenCompute/ROCm/issues/2060#issuecomment-1512915933>,
> or unsubscribe
> <https://github.com/notifications/unsubscribe-auth/ABY7PVN5EPDUBOZYUZ53JFLXBZ3N3ANCNFSM6AAAAAAXCJ7DZY>
> .
> You are receiving this because you authored the thread.Message ID:
> ***@***.***>
>


---
