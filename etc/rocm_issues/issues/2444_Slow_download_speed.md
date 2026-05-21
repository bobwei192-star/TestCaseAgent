# Slow download speed

> **Issue #2444**
> **状态**: closed
> **创建时间**: 2023-09-10T20:29:16Z
> **更新时间**: 2024-04-19T19:05:19Z
> **关闭时间**: 2024-04-19T19:05:19Z
> **作者**: LoGiCa7
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2444

## 描述

I'm in the UK and I always get incredibly slow download speed when installing rocm.

I only have the issue with https://repo.radeon.com/rocm/apt/

![Screenshot from 2023-09-10 21-27-45](https://github.com/RadeonOpenCompute/ROCm/assets/47193468/b393032e-f5ac-4e9b-bdfa-7138fe77f31d)


---

## 评论 (17 条)

### 评论 #1 — saadrahim (2023-09-11T13:45:50Z)

I know you did say always, but can you elaborate on the different times that you got a slow connection? 

Anyone else in the experiencing slow downloads?

---

### 评论 #2 — LoGiCa7 (2023-09-13T00:17:51Z)

It's painfully slow no matter what time of day I am trying to install it.

This was about 01:00am:

![Screenshot from 2023-09-13 01-13-46](https://github.com/RadeonOpenCompute/ROCm/assets/47193468/70ac45d2-797d-448f-84b7-7503dab1862e)
![Screenshot from 2023-09-13 01-17-22](https://github.com/RadeonOpenCompute/ROCm/assets/47193468/0976e978-7cf3-4f94-a36b-a4aff27728d9)


---

### 评论 #3 — LoGiCa7 (2023-09-14T18:31:30Z)

i tried again today and it's still as slow.

![Screenshot from 2023-09-14 19-30-59](https://github.com/RadeonOpenCompute/ROCm/assets/47193468/b93316d2-c722-4ced-b99b-842b99abb336)


---

### 评论 #4 — deke997 (2023-10-07T23:40:14Z)

Hi,

I also have this problem with https://repo.radeon.com/rocm/apt/

<img width="851" alt="image" src="https://github.com/RadeonOpenCompute/ROCm/assets/21989537/1ee586be-f821-4ab6-b131-67c8a9d14914">


---

### 评论 #5 — LoGiCa7 (2023-10-12T22:09:29Z)

I'm still having the speed issue when installing ROCM. Has there been any progress on fixing this?

---

### 评论 #6 — kolu4iy (2023-11-02T16:59:12Z)

Hello. Now is 02.11.2023, 19:57 UTC +03:00 (Moscow)
![image](https://github.com/RadeonOpenCompute/ROCm/assets/6008116/b0aea86a-e8b7-4bf2-bb97-c49e7bb7b75e)
![image](https://github.com/RadeonOpenCompute/ROCm/assets/6008116/3ad5acc8-2335-449a-92aa-cd1ad8e22007)

Very slow download of ROCm.

---

### 评论 #7 — nartmada (2024-03-16T01:25:08Z)

@LoGiCa7, @deke997, @kolu4iy, apologies for not following up.  Do you folks still see this slow download speed?  Thanks.

---

### 评论 #8 — kolu4iy (2024-03-16T07:22:12Z)

Hello.
Today i see aceptable download rate, about 4-5 MBit/s. It's unstable
(0,8-5 MBit/s), but aceptable. Today i'm wait downloading about 10
minutes, but early it was take hours. Thank you.

сб, 16 мар. 2024 г. в 04:25, Adam Tran - AMD ***@***.***>:
>
> @LoGiCa7, @deke997, @kolu4iy, apologies for not following up. Do you folks still see this slow download speed? Thanks.
>
> —
> Reply to this email directly, view it on GitHub, or unsubscribe.
> You are receiving this because you were mentioned.Message ID: ***@***.***>



-- 
Йош


---

### 评论 #9 — nartmada (2024-04-05T14:38:03Z)

Several of my team members have tried and not observed the slow download speed on our side.  Closing the ticket.

![image](https://github.com/ROCm/ROCm/assets/144284448/98d1bf41-6d80-476a-adc5-880b9c6e9c6c)


---

### 评论 #10 — AdrianIleana (2024-04-05T17:55:47Z)

@nartmada I am experiencing the same problem right now:
![image](https://github.com/ROCm/ROCm/assets/40955689/11bb439e-d62b-4eaa-a693-4e04f9d8d28f)

My usual download speed is 50MB/s

---

### 评论 #11 — AdrianIleana (2024-04-05T18:15:12Z)

As a side note for people who might hit this problem in the future. 

I've been playing around with a VPN solution to see if I get better results from different locations, and yes things are quite different when using a North America location.

My download speed is not the best, but definitely a considerable improvement. From **US - Washington** I get the following speed:
![image](https://github.com/ROCm/ROCm/assets/40955689/44b4a467-ada6-4b5d-ab57-a437ca92e694)


---

### 评论 #12 — yogesh-kapoor (2024-04-06T11:36:10Z)

![image](https://github.com/ROCm/ROCm/assets/483623/af14f00f-24d3-4c3b-823f-69599b1f3b4c)
Still experiencing slow download speeds.

---

### 评论 #13 — nartmada (2024-04-07T03:52:18Z)

Hi @yogesh-kapoor, which part of the world are you located in?  Thanks.

---

### 评论 #14 — yogesh-kapoor (2024-04-07T04:34:51Z)

> Hi @yogesh-kapoor, which part of the world are you located in? Thanks.

India, Maharashtra

---

### 评论 #15 — LoGiCa7 (2024-04-11T02:16:28Z)

It's still just as slow

---

### 评论 #16 — saadrahim (2024-04-18T23:30:04Z)

To address slow downloads, AMD is upgrading our download infrastructure today. Please try again and let's see if we can close this issue. The changes should finalize by 6pm GMT on April 19th, if not earlier.

You may need to clear your DNS cache.

---

### 评论 #17 — saadrahim (2024-04-19T19:05:19Z)

Closing based on feedback #3042 

---
