# [Issue]: Problem loading repodata

> **Issue #5593**
> **状态**: closed
> **创建时间**: 2025-10-29T09:26:53Z
> **更新时间**: 2025-11-11T19:07:56Z
> **关闭时间**: 2025-10-31T17:28:41Z
> **作者**: phueper
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5593

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

Hi, 

it seems some of the repo.radeon.com akamai edges are not synced, i get on some of our boxes (depending on internet connection it seems) a 404 for 

```
$ curl --fail-with-body https://repo.radeon.com/amdgpu/7.0.2/rhel/8.10/main/x86_64/repodata/repomd.xml 
<html>
<head><title>404 Not Found</title></head>
<body>
<h1>Release notes</h1>
For information on available ROCm releases, please refer to the
<a href="https://rocm.docs.amd.com/en/latest/">
ROCm Release Notes</a><p>
For information on available Radeon Software for Linux releases,
please refer to
<a href="https://www.amd.com/en/support/download/linux-drivers.html">
Linux&reg; Drivers for AMD Radeon&trade; and Radeon PRO&trade; Graphics</a>.<p>
</body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx/1.18.0 (Ubuntu)</center>
</body>
</html>
```

(also fails in `dnf` )

it is resolving repo.radeon.com like this:

```
$ dig repo.radeon.com                                                                                                                                                                                                                                                            22 ↵

; <<>> DiG 9.20.11-1ubuntu2-Ubuntu <<>> repo.radeon.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 58234
;; flags: qr rd ra; QUERY: 1, ANSWER: 4, AUTHORITY: 0, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;repo.radeon.com.               IN      A

;; ANSWER SECTION:
repo.radeon.com.        14      IN      CNAME   repo.radeon.com.edgekey.net.
repo.radeon.com.edgekey.net. 14 IN      CNAME   e40210.dscd.akamaiedge.net.
e40210.dscd.akamaiedge.net. 14  IN      A       95.101.35.210
e40210.dscd.akamaiedge.net. 14  IN      A       95.101.35.186
```

while other boxes that resolve the host different are working, e.g.:

```
$ dig repo.radeon.com

; <<>> DiG 9.20.11-0ubuntu0.2-Ubuntu <<>> repo.radeon.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25447
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;repo.radeon.com.		IN	A

;; ANSWER SECTION:
repo.radeon.com.	8574	IN	CNAME	repo.radeon.com.edgekey.net.
repo.radeon.com.edgekey.net. 12224 IN	CNAME	e40210.dscd.akamaiedge.net.
e40210.dscd.akamaiedge.net. 18	IN	A	2.21.79.32
```

this one works fine and returns the repo data

### Operating System

Ubuntu 25.10 (Questing Quokka)

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

ROCm 7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — phueper (2025-10-29T23:43:38Z)

seems to be ok now for me, at least on one of the boxes that had the problem previously 


---

### 评论 #2 — lucbruni-amd (2025-10-31T17:17:07Z)

Hi @phueper, I tried on a few of our geographically distant servers and the repo data is returned as expected - can you check whether this is still an issue? If not, we can close the issue. Thanks!

---

### 评论 #3 — phueper (2025-10-31T17:25:39Z)

@lucbruni-amd I commented previously.. for us it's working again, can be closed imho 

---

### 评论 #4 — lucbruni-amd (2025-10-31T17:28:41Z)

Ok thanks. Just wanted to confirm with you before doing so. Please don't hesitate to reopen this ticket or open a new one for further issues.

Thanks for helping us by reporting issues!

---
