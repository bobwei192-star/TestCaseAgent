# [Issue]: Continued System Crashes with BOINC OpenCL Apps Since RDNA3 Release

> **Issue #3575**
> **状态**: closed
> **创建时间**: 2024-08-13T06:31:06Z
> **更新时间**: 2025-02-22T05:06:38Z
> **关闭时间**: 2024-10-21T14:50:50Z
> **作者**: PorcelainMouse
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3575

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

Since launch of RDNA3, I have not been able to resume running BOINC many OpenCL apps that had been working for many years on AMDGPU.  Recently, ROCm 6.1 was released through my distro's official pkg repo, so I thought I would try again.  Things are better; I was able to get expected performance, no crashes, and no invalid results for the Einstein@Home O3MDF Gravitational Wave app.  However, BRP7 (Meerkat) app crashed the whole system.

### Operating System

Fedora Linux 40 (Workstation Edition)

### CPU

AMD Ryzen 9 5950X 16-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

Install BOINC & join Einstein@Home
Enable only BRP7 (Meerkat) app
System is very likely to crash moments after starting a work unit.  Some work units were completed as valid, however, so it isn't wasn't 100%. I estimate less than 2 hours MTBF.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

[rocminfo-support.log](https://github.com/user-attachments/files/16595198/rocminfo-support.log)


### Additional Information

[journal-10.log](https://github.com/user-attachments/files/16595278/journal-10.log)
[Task 1642166730 _ Einstein@Home.pdf](https://github.com/user-attachments/files/16595290/Task.1642166730._.Einstein%40Home.pdf)


---

## 评论 (23 条)

### 评论 #1 — ppanchad-amd (2024-08-13T14:04:05Z)

@PorcelainMouse Internal ticket has been created to fix investigate this issue. Thanks!

---

### 评论 #2 — PorcelainMouse (2024-08-20T19:32:15Z)

Wonderful!  Thank you.  Let me know how I can help.

---

### 评论 #3 — schung-amd (2024-08-22T15:45:16Z)

Hi @PorcelainMouse, a couple BOINC-related questions: is there any way this can be reproduced locally? Currently waiting for Meerkat tasks to be scheduled and run to get output, which will make investigating this very slow. I do see some provided source files for the app, but is there test data I can run it on? Also, you mention enabling only Meerkat; is there a way to do this from the command line?

You mention you've been having these issues since the launch of RDNA3. Can you still run Meerkat tasks without issues on older hardware and ROCm versions?

---

### 评论 #4 — PorcelainMouse (2024-09-07T08:30:29Z)

Sorry for the late reply! Didn't get a message about your update.  Just seeing this now.

Uh, in theory, yes, you can run test applications with text work units.  I looked into it a *long* time ago.  I think you can get these GPU apps that run either entirely outside BOINC or maybe it's inside BOINC with some special setup.  That's a more controlled environment for devs who write BOINC apps. But, I never actually got that environment setup up, myself.  I guess I can look into it for you, though.

If it helps, I've had to abandon the E@H project, again, because even running All-Sky Gravitational Wave search on O3 (GPU) [O3AS] causes crashes within 48 hours.
[journal-11-short.log](https://github.com/user-attachments/files/16917035/journal-11-short.log)

I don't have my old hardware, unfortunately.  Had to sell them to buy 7900.  That's not impossible, though.  I could probably get my hands on a 5700xt for cheep or my old 6800xt if I beg the person I sold it to.  Old ROCm would be harder.  I don't have a dedicated system for BOINC, this is my daily driver, so I can't go back in time that far.  But I could downgrade pkgs to ROCm 6.0 pretty easy.  If you want older than that, I'm assuming I can get old pkgs from F39, F38, but I guess I don't know how far back I can really go.  I probably can't install a kernel prior to 6.8.5 (easily) without having to downgrade my whole system to the previous major distribution release.  I mean, I could build any kernel I want, but haven't done that since the '90's and probably couldn't commit to that.

---

### 评论 #5 — PorcelainMouse (2024-09-07T22:40:05Z)

@schung-amd Thanks again for you help.

Going back one post, I wanted to double check with you on the downloads. I usually doesn't take more than a few seconds to download apps and and work units.  You probably don't need much work, so you can set the work limit to just half a day or something.  But, your system should start crunching as soon as it downloads the first work unit, so normally it doesn't take any time at all to start crunching.  I assume by this time, 2 weeks later, you've had plenty of time to test Meerkat work units?

Here are some instructions on building your own apps.  The "anonymous platform" they refer to just means setting up your own BOINC apps without letting the project configure the app for you.  I ran "anonymous platform" for quite a few years, myself, but I started with an official E@H configuration and then just tweaked it.  But, maybe, you don't even need to use BOINC at all.  If you download the source code and build it, maybe you can just run in manually to test.  The hard part is getting work units to test with.  Maybe there are instructions on getting test work units, though, with the source.  Been a while since I looked into it.
https://einsteinathome.org/application-source-code-and-license 

---

### 评论 #6 — schung-amd (2024-09-09T14:08:29Z)

Hi @PorcelainMouse, thanks for keeping up with this!

Re: Meerkat on older hardware/software, no worries if it's hard to test on your end. When I was searching for similar issues, I saw several clusters of reports of Meerkat breaking which suggested that this issue could be related to changes with the workload, so I'm mostly curious if this issue could be related to changes in Meerkat rather than (or in addition to) changes on our end, which would be a good clue as to what is causing this workload to fail. Once I figure out how to get Meerkat running properly, we have a variety of older hardware I can test this on.

> I assume by this time, 2 weeks later, you've had plenty of time to test Meerkat work units?

Unfortunately my repro system seems to want to run everything except Meerkat when possible, and in addition the Meerkat workload has been failing on my end for unrelated OpenCL reasons, so I haven't been able to repro this yet. I can run the other tasks perfectly fine, which suggests to me that something is not configured properly in the Meerkat app. I've been trying to build from source without much success so far, but I'm still working on it. I'll let you know when I'm able to reproduce your issue.

---

### 评论 #7 — PorcelainMouse (2024-09-11T05:34:44Z)

Okay.  Very interesting.  Thanks for working so hard.  I'm sorry that it's a pain; I wish it were not so hard to test.

- If you use "regular" BOINC & E@H, you can select which specific apps you want.  You could turn off all apps except Meerkat.  Then you could get Meerkat WUs without the other ones.  At least then you wouldn't need to roll your own dev app.
- Yeah, it's possible the WUs or the app has changed over time.  That wouldn't surprise me.
- Just to reiterate, there are two details that I got wrong on my initial report
  - I actually got credit for a few Meerkat WUs before a crash.  The crash was just at the very beginning of a WU and the crash was very hard. The system crashed three times in a row, the second two times it occurred moments after staring BOINC.  So that means that either A) BOINC didn't know the job failed and kept retrying it until I aborted the job, or B) some Meerkat WUs are okay, but some are instant death.
  - Even though the other apps--by which I mean Gravitational Wave apps (GW)--will run for 24 hours, doesn't mean that those apps are safe.  After turning off Meerkat, I've been running GW GPU apps and my system has crashed once every other day.  It's not stable.  I've had to abandon the whole project, again.  So, if you can test the other apps with real WUs from the regular stream for just a few days, I think that would be really helpful too.  I can crunch O(20000) GW WUs in a day, and then it'll crash the next day.  So, don't expect the other apps to be "instant" crash.  But, I'm pretty confident there is a problem with them, also.

When I had my 5700xt, the original blower design,--which I much prefer!!--I'm assuming you know that card was notorious for running too hot.  I had lots of crashes, like A LOT. I had to abandon the project back then too.  I finally got a tool that let me set my own fan curve, and that made a HUGE difference.  MTBF was >30 days, which I could live with.

I upgraded to 6800xt and didn't have to change anything.  Literally swapped the card out, and booted it up, started crunching.  That's why RDNA3 has been such a shocking experience.  Everything changed.  And now it's been almost two years since things worked.  Two of the biggest GPU apps in all of BOINC that I used to crunch with have shutdown in the interim, so much of the work I'm doing now is different than what was stable for me for so long prior to RDNA3.  But, E@H is a project that I used to crunch for.

If we can get Meerkat working or send a bug upstream.  That'd be great.  I thought it had a good chance to lead to something; that's why I reported it.  (Just now realizing that I could have sent you the offending WU, but I didn't think of it.  Crap, that would have been really helpful.  Sorry!  I didn't think of it at the time.)  ...But, TBH, I would have reported these problems with the GW app if Meerkat had worked.  (ooh, maybe I'll get you some of these GW WUs that crashed my system, while I'm thinking of it!)

---

### 评论 #8 — PorcelainMouse (2024-09-11T05:47:31Z)

> (ooh, maybe I'll get you some of these GW WUs that crashed my system, while I'm thinking of it!)

Oh, well, I guess I don't know how to do that.  I looked at the project docs and source code docs, but couldn't see how to download work to use with the app.  Rats.  I'm sure it's possible.  Maybe you figured it out already?  I'll put the "problem" work units here.  Maybe you can get them. But, they don't last forever, so maybe it will not be useful by the time you can look into GW.

```
h1_1591.60_O3aC01Cl1In0__O3ASHF1d_1592.00Hz_43718
h1_1591.60_O3aC01Cl1In0__O3ASHF1d_1592.00Hz_43720
h1_1591.60_O3aC01Cl1In0__O3ASHF1d_1592.00Hz_56112
h1_1591.60_O3aC01Cl1In0__O3ASHF1d_1592.00Hz_56114_2
```

---

### 评论 #9 — schung-amd (2024-09-11T15:05:06Z)

Thanks for the info! I have tried configuring the project to run only Meerkat apps, but it somehow results in my system not running anything, but I'll try that again. As an aside, I am now running into issues with O3AS as well, but I did update to ROCm 6.2 at some point before seeing these failures so those could be on our side. When you say your system was crashing intermittently, did these show up in the task reports as errors? Also, were you running these tasks while using the system, or was this while the system was otherwise idle?

---

### 评论 #10 — PorcelainMouse (2024-09-13T05:27:16Z)

> Thanks for the info! I have tried configuring the project to run only Meerkat apps, but it somehow results in my system not running anything, but I'll try that again.

:-( Hmm, yes, sometimes BOINC is inscrutable; it's very complex with the way it schedules work.  When I make changes to project allocations or tweak things, it often takes 24 hrs to see the results, longer even.  The manager only gets updates periodically, and even when it gets your new preferences, it may not implement them right away; it actually waits until you get new WU sent to you from a project.  So, you can force a "update", and you'll see the new preferences acknowledged in the log, and it just keeps doing the old thing, and then, later, you get new WU downloaded, and *then* it changes behavior.  It can be confusing.

The only other thing I can think of is that it thinks you can't or don't want to run Meerkat, which could be due to many things.  But, it's probably not that.

> As an aside, I am now running into issues with O3AS as well, but I did update to ROCm 6.2 at some point before seeing these failures so those could be on our side. When you say your system was crashing intermittently, did these show up in the task reports as errors?

Hmm, well, maybe.  In my experience (since 1999) I almost never see them.  They usually get detected and error out, then reported.  In theory, it shouldn't need to do that, though, because the tasks are all checkpoint-ed and can be resumed without loosing all the work already done.  The fact that these crashes result in terminated tasks with lost work is unusual to begin with.

I see these tasks on the project website in my list of reported tasks with errors; that's usually where I see them.  But, before they get uploaded, yes, they should be listed in the manager as failed or error-ed tasks.  I just never notice them there.  I think that is for a few reasons: 1) they get cleared very quickly on the next start, so it's not like they hang round an flash red or something; BOINC just starts new tasks.  That's usually what I see: if there is a new task at 0 % when I start BOINC, I know the task that was running error-ed out.  2) I also sort my tasks by status, and I think the error-ed tasks go to the bottom and I just never see them. 3) I think BOINC does an update on startup, so it reports those failed tasks immediately, so they don't sick around on your system for very long.

> Also, were you running these tasks while using the system, or was this while the system was otherwise idle?

Since I run BOINC 24/7, most crashes happen when I'm not at the system doing something else.  These recent ones are no exception to that rule.  But, I have also been typing or clicking when some of the crashes have happened.  My system does everything--web, coding, gaming, CAD, video conferencing, image processing.  It's also full of CRON jobs doing automated clean up jobs here and there.  So yeah, there's is a lot going on on my box other than BOINC.  But, the symptoms are very specific and consistent.  Nothing behaves like a video card crash, and almost nothing else actually crashes the system.  These *always* start with AMDGPU error, card reset, card reset fails, GNOME shell crashes, system hangs, or lately, the system kills all users process without hanging and then GDM restarts and I can start a new desktop session, but I always just reboot in that case anyway.

In the past, like with the 5700xt, I've even gone so far as to stop running BOINC completely for a week or so to prove that it's not something else.  When I got this 7900xtx, I had it RMAed *three* times because I just couldn't believe it couldn't run the same work my 6800xt would run.  I went back to my 6800xt many times over about 8 months, waiting for new drivers and hoping it would just start working.  I ended up replacing every single piece of my system, even the case.  I think the mainboard did actually have a problem, but after that, I started reporting these problems against the drivers because I knew it couldn't be my hardware.  Things have improved since then; there's no doubt.   It used to crash in <1 hr on *every* fp OCL app I tried. Now it's 24-48 hrs.  But, I've been running PrimeGrid instead of E@H, which has been working well, but that's all int work.  

The Fedora ROCm pkg maintainer was very helpful and had me working on upstream kernel branch with a COPR channel with upstream ROCm pkgs.  That was fun, but we didn't get far with troubleshooting.  We just kept waiting for the next ROCm release.  And all the special kernel overrides made for trouble when upgrading my distribution, so I'm not on the upstream kernel anymore.  That started with ROCm 5.8 or something, and, like I said earlier, I had my heart set on 6.1 to be "the one", so I got up the courage to try E@H again after that arrived.

Sorry for the long posts.  Please keep asking questions.  I may not get your answers right away, but I will test or do what else you ask if it is at all possible.

---

### 评论 #11 — schung-amd (2024-09-16T20:14:02Z)

Thanks for the replies, I appreciate your insight. An update from my end: I was able to configure BOINC to pull only Meerkat and O3AS tasks properly this time. My system has completed several of these without crashing. I'm on Ubuntu 22.04 with a 7900XTX and ROCm 6.2. I'll keep the tests running to see if anything changes, but for now ROCm 6.2 (on Ubuntu, at least) seems to be completing Meerkat and O3AS tasks without issue.

---

### 评论 #12 — PorcelainMouse (2024-09-30T04:35:02Z)

Hmm, that's really really frustrating.  You're killing me.  I'm mean, I barely believe you; I've had this problem for nearly two full years, so you can understand my skepticism.  I've replaced every piece of silicon in my rig and upgraded major OS releases *three* times during that interval.  I've ruled out everything I possibly could.

You could be on to something with ROCm 6.2, but that still seems unlikely.  Looks like pkg mgrs are not planning to push 6.2 to current Fedora.  But next version will be out soon, so maybe I'll get it then.

What kernel are you on?

You're getting ROCm 6.2 from where?  This repo?  You're building it yourself?

Is there a reason why you didn't try 6.1?

---

### 评论 #13 — schung-amd (2024-09-30T18:22:54Z)

> Hmm, that's really really frustrating. You're killing me. I'm mean, I barely believe you; I've had this problem for nearly two full years, so you can understand my skepticism. I've replaced every piece of silicon in my rig and upgraded major OS releases three times during that interval. I've ruled out everything I possibly could.
> 
> You could be on to something with ROCm 6.2, but that still seems unlikely. Looks like pkg mgrs are not planning to push 6.2 to current Fedora. But next version will be out soon, so maybe I'll get it then.

It's frustrating to me as well that I can't reproduce your issue. One variable that might be in play here is your distro, we don't officially support Fedora at the moment so there may be some incompatible components causing your issues. I'd advise you to test on Ubuntu if you get a chance, just to rule that out.

> What kernel are you on?
> 
> You're getting ROCm 6.2 from where? This repo? You're building it yourself?
>
> Is there a reason why you didn't try 6.1?

Kernel version is `6.8.0-40-generic` which came with Ubuntu 22.04. ROCm was installed using instructions from https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html; I used the AMDGPU installer but I don't think the method matters.

Generally it makes sense to check if an issue exists in the current version of ROCm, as a lot of issues end up being fixed between versions and we can advise users to upgrade. Of course, distros we don't officially support yet, such as Fedora and Arch, will not necessarily have the latest ROCm versions available, but this is out of our control. I have also checked on ROCm 6.1, and I do not see any issues on Ubuntu 22.04.

---

### 评论 #14 — PorcelainMouse (2024-10-01T05:32:47Z)

Thanks, I appreciate your help.

If you didn't see it with ROCm 6.1, then it's probably not that, either, although there is still chance that 6.2 will improve compatibility.

I have the PowerColor 7900XTX OC.  I suppose manufacturer OC could be another aspect we haven't ruled out.

I've been using OCL since 1999 and never had an nVidia card.  I wouldn't be using AMD if it wasn't for their statements of support for OSS.  I can't imagine what my distribution has to do with it, but if it does, it would be the first time ever.  580, 5700, 6800 all worked...eventually...and whatever I had before the 580, too.  Catalyst was a different time, though. Back then, I was hacking the installer to work on Fedora.  Since ROCm, I haven't had to do that.  Perhaps I've come to expect too much.

For a while, I was using upstream kernel, so, even Fedora kernel patches don't seem likely to be the issue.  It would have to be libs, then?

I'm on kernel 6.10 now; soon 6.11.  I can't even get 6.8 easily; I don't think there is any pkg repo for Fedora with "old" kernels.  Maybe that's something I can look into...hmm, didn't see anything like that.  Mostly folks interested in even newer kernels, not older ones.

You did a lot of work.  I guess I should try to run Ubuntu.  That's conceivable for me to do, but probably too disruptive.  I'll need to do some planning, at the very least.

---

### 评论 #15 — schung-amd (2024-10-04T14:23:14Z)

> I can't imagine what my distribution has to do with it, but if it does, it would be the first time ever.

I don't know the details at the moment, but on Fedora specifically it seems like the ROCm packages have modifications which are not present in the official packages, and this divergence may play a part in why this seems to be fully functional on Ubuntu but broken on your end. Since we don't officially support Fedora, I doubt the modified code has been tested as thoroughly as our mainline code and wouldn't be surprised if something broke because of it.

---

### 评论 #16 — PorcelainMouse (2024-10-05T10:23:23Z)

Oh, really?  Well, that's very interesting.  Thank you for explaining.  I'm surprised to here that.  I will take it up with the maintainers.

---

### 评论 #17 — schung-amd (2024-10-21T14:50:50Z)

Closing this for now, as I can't reproduce the issue on our end. I'm sorry this hasn't worked for you for quite some time on your distro of choice. When you get a chance to try this on Ubuntu in the future, if you're still running into this issue feel free to comment and we can reopen this. I'll also provide an update if we find more information about what might be causing your issues.

---

### 评论 #18 — PorcelainMouse (2024-12-07T08:19:31Z)

Hey, I've got some new information.  I know this is closed, but I'm hoping you can spare some thought on it. I got ROCm 6.2, now, and E@H apps error out immediately on start.  They aren't crashing the system, which is an improvement, but it's still not working.  And it's extra strange because you said you tested 6.2 and didn't have any problems.  I'm assuming you would have noticed if it error-ed out?  That's not why it didn't crash on you, is it?

```
Failed OpenCL buildlog: 
ld.lld: error: undefined symbol: __printf_alloc
>>> referenced by /tmp/comgr-9492ec/input/linked.bc.o:(XLALLoopOverCoarseGridFrequencyBins)
>>> referenced by /tmp/comgr-9492ec/input/linked.bc.o:(XLALLoopOverCoarseGridFrequencyBins)
Error: Creating the executable from LLVM IRs failed.
XLAL Error - XLALOpenCLGetProgramFromSource (/home/jenkins/workspace/workspace/EaH-GW-OpenCL-Testing/SLAVE/LIBC215/TARGET/linux-x86_64/EinsteinAtHome/source/lalsuite/lalpulsar/lib/GPUUtils/OpenCLUtils.c:705): clBuildProgram failed with OpenCL error: CL_BUILD_PROGRAM_FAILURE
XLAL Error - XLALOpenCLGetProgramFromSource (/home/jenkins/workspace/workspace/EaH-GW-OpenCL-Testing/SLAVE/LIBC215/TARGET/linux-x86_64/EinsteinAtHome/source/lalsuite/lalpulsar/lib/GPUUtils/OpenCLUtils.c:705): Generic failure
XLAL Error - XLALGCTOpenCLKernelsSetup (/home/jenkins/workspace/workspace/EaH-GW-OpenCL-Testing/SLAVE/LIBC215/TARGET/linux-x86_64/EinsteinAtHome/source/lalsuite/lalapps/src/pulsar/GCT/HierarchSearchGCT_OpenCL.c:212): Check failed: XLALOpenCLGetProgramFromSource ( source, &(GCTOpenCLKernels.HierarchSearchGCTProgramm) ) == XLAL_SUCCESS
XLAL Error - XLALGCTOpenCLKernelsSetup (/home/jenkins/workspace/workspace/EaH-GW-OpenCL-Testing/SLAVE/LIBC215/TARGET/linux-x86_64/EinsteinAtHome/source/lalsuite/lalapps/src/pulsar/GCT/HierarchSearchGCT_OpenCL.c:212): Internal function call failed: Generic failure
XLAL Error - MAIN (/home/jenkins/workspace/workspace/EaH-GW-OpenCL-Testing/SLAVE/LIBC215/TARGET/linux-x86_64/EinsteinAtHome/source/lalsuite/lalapps/src/pulsar/GCT/HierarchSearchGCT.c:1394): Check failed: XLALGCTOpenCLKernelsSetup( uvar->SortToplist, uvar->getMaxFperSeg, uvar->computeBSGL, detectorIDs, usefulParams.BSGLsetup ) == XLAL_SUCCESS
XLAL Error - MAIN (/home/jenkins/workspace/workspace/EaH-GW-OpenCL-Testing/SLAVE/LIBC215/TARGET/linux-x86_64/EinsteinAtHome/source/lalsuite/lalapps/src/pulsar/GCT/HierarchSearchGCT.c:1394): Internal function call failed: Generic failure
2024-11-20 11:15:54.9516 (162207) [CRITICAL]: ERROR: MAIN() returned with error '-1'
```

https://einsteinathome.org/task/1684803437

---

### 评论 #19 — schung-amd (2025-01-02T14:10:10Z)

Sorry for the late response, and sorry to hear you're still having issues. No, I did not encounter these or any other errors with ROCm 6.2 on Ubuntu; my logs were clean and the results were uploaded and verified successfully.

---

### 评论 #20 — ChihweiLHBird (2025-01-29T21:11:05Z)

I am having a similar issue with AMD RX 6950 XT on Fedora 41 with BOINC project NumberFields@home.

```
GPU Summary String = [CAL|AMDRadeonRX6950XT(radeonsi,navi21,LLVM17.0.6,DRM3.59,6.12.10-200.fc41.x86_64)|1|16384MB||101].
Loading GPU lookup table from file.
GPU was not found in the lookup table.  Using default values:
  numBlocks = 1024.
  threadsPerBlock = 32.
  polyBufferSize = 32768.
Error: clBuildProgram() returned CL_BUILD_PROGRAM_FAILURE
Build Log:

Error: Failed to initialize OpenCL.
```

Hope there will be a solution or workaround soon.

---

### 评论 #21 — schung-amd (2025-01-29T21:26:29Z)

@ChihweiLHBird Are you able to run other OpenCL applications? This seems like it could just be a configuration issue.

---

### 评论 #22 — PorcelainMouse (2025-02-21T08:01:52Z)

> [@ChihweiLHBird](https://github.com/ChihweiLHBird) Are you able to run other OpenCL applications? This seems like it could just be a configuration issue.

Yes, I can run lots of other OpenCL apps, and have been running OpenCL apps for a long long time.  I can even run other E@H apps.

I recently try to make more progress on this issue, and I see now, looking more carefully at the error, that the linker fails to resolve __print_alloc(). This isn't in stdlib, which is what I thought at first.  It's in a few shared libraries, including comgr.  Now, that seems like something that LLVM would try to link with, but I have rocm-comgr, so I'm assuming that isn't quite the right one or something.  Am I thinking about this correctly?

---

### 评论 #23 — ChihweiLHBird (2025-02-22T05:06:36Z)

@PorcelainMouse Sorry, I think @schung-amd was asking me..

@schung-amd I didn't try other OpenCL apps, but another BOINC project was broken as well on that system. There were many updates to Fedora 41 since last time I tried, maybe I can try it again this weekend.

---
