# [Issue]: HIP programs hang inside amdhip64.dll after main

> **Issue #3418**
> **状态**: closed
> **创建时间**: 2024-07-12T21:33:35Z
> **更新时间**: 2024-10-05T19:50:49Z
> **关闭时间**: 2024-10-05T19:50:49Z
> **作者**: MathiasMagnus
> **标签**: Under Investigation, AMD Instinct MI300X, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3418

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

Using the recently released HIP SDK for Windows 6.1.2 with Visual Studio 2022 17.10.4 and latest Radeon Software 24.6.1, compiling the simplest of SAXPY programs (my own, but also AMD's ROCm-examples one), when the program is compiled in Debug mode (both using the VS Extension and MSBuild or using CMake+Ninja), the program after leaving main hangs inside amdhip64.dll. Everything works as expected when compiled in Release mode.

![kép](https://github.com/user-attachments/assets/eea8e6ca-064e-4fe9-8a9f-3533ff59e2ae)

### Operating System

Windows 11 Pro (10.0.22631)

### CPU

AMD Ryzen 9 7945HX with Radeon Graphics

### GPU

AMD Instinct MI300X

### ROCm Version

ROCm 6.1.0

### ROCm Component

HIP

### Steps to Reproduce

1. Clone https://github.com/ROCm/rocm-examples/blob/develop/HIP-Basic/saxpy/main.hip
2. Build in Debug mode
3. Run
4. Profit

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Not really MI300X, but I can't select AMD Radeon(TM) 610M from the HW drop-down. I know this device isn't strictly speaking supported, but the issue doesn't seem to be related to the device itself. (I wouldn't want to go into the perception of the sparsity of the support matrix.)

---

## 评论 (17 条)

### 评论 #1 — ppanchad-amd (2024-07-15T18:12:26Z)

@MathiasMagnus Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — jamesxu2 (2024-07-17T15:02:59Z)

Hello @MathiasMagnus ,

I've been unable to reproduce your issue using the [ROCm-Examples version of saxpy](https://github.com/ROCm/rocm-examples/blob/develop/HIP-Basic/saxpy/main.hip). I've tested using:

1. Debug and release builds with MSBuild on Visual Studio Community. I installed Visual Studio Community 2022 and then the HIP-SDK. As part of the HIP-SDK install, I installed the HIP-VS plugin. 
  - I don't see a hang with either the release or debug builds. The program exits cleanly with correct values calculated at the end of the program.

![image](https://github.com/user-attachments/assets/0fde7354-7288-4e35-a837-86b802cbd361)
  
2. Compiling from command line clang++ (need to add your ROCm/bin to environment PATH) using:
```
clang++ main.hip -o saxpy.exe -I .\Common -lamdhip64 --offload-arch=gfx1100
```
and optionally ```-ggdb -O0``` . 

This also runs correctly and exits cleanly.  There's a [detailed tutorial on Windows + HIP CLI setup](https://rocm.docs.amd.com/projects/HIP/en/latest/tutorial/saxpy.html#setting-up-the-command-line) if you'd like to reference that.

One caveat is that I'm running these tests on a Radeon Pro W7800 which is [officially supported](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html#supported-skus-win). Like you said, the issue is probably not device related, considering you can run the program with the release build. 

Do you see any other relevant setup differences? 



---

### 评论 #3 — MathiasMagnus (2024-07-17T15:38:08Z)

@jamesxu2 Thanks for giving it a spin.

> This also runs correctly and exits cleanly. There's a [detailed tutorial on Windows + HIP CLI setup](https://rocm.docs.amd.com/projects/HIP/en/latest/tutorial/saxpy.html#setting-up-the-command-line) if you'd like to reference that.

["Do not cite the deep magic to me witch..."](https://knowyourmeme.com/memes/do-not-cite-the-deep-magic-to-me-witch) I wrote that very article. 😉 (But at least it's nice to see being referenced in cases like this.)

I'll try an even more minimal CLI compilation or try installing the PRO drivers, but I'm afraid it's gonna boil down to the device difference. As unprobable a source of difference it seems, I don't see many other diffs, beside the exact gfx binary flavor.

---

### 评论 #4 — MathiasMagnus (2024-07-22T11:34:13Z)

@jamesxu2 I have verified, that the issue is the same on the CLI.

```
PS C:\Users\mate> & ${env:HIP_PATH}bin\hipInfo.exe | sls Name:

Name:                             AMD Radeon(TM) 610M
gcnArchName:                      gfx1036

PS D:\Develop\ROCm-examples> & ${env:HIP_PATH}bin\clang++ .\HIP-Basic\saxpy\main.hip -o saxpy.exe -I .\Common -lamdhip64 -L ${env:HIP_PATH}lib -O2 --offload-arch=gfx1036
PS D:\Develop\ROCm-examples> .\saxpy.exe
Calculating y[i] = a * x[i] + y[i] over 1000000 elements.
First 10 elements of the results: [ 3, 5, 7, 9, 11, 13, 15, 17, 19, 21 ]
PS D:\Develop\ROCm-examples> $LASTEXITCODE
0
PS D:\Develop\ROCm-examples> & ${env:HIP_PATH}bin\clang++ .\HIP-Basic\saxpy\main.hip -o saxpy.exe -I .\Common -lamdhip64 -L ${env:HIP_PATH}lib -ggdb -O0 --offload-arch=gfx1036
PS D:\Develop\ROCm-examples> .\saxpy.exe
Calculating y[i] = a * x[i] + y[i] over 1000000 elements.
First 10 elements of the results: [ 3, 5, 7, 9, 11, 13, 15, 17, 19, 21 ]
<cursor_blinking_to_eternity>
```

---

### 评论 #5 — MathiasMagnus (2024-07-23T07:45:51Z)

@jamesxu2 I have found the issue. It is `amdhip64.dll` vs. `amdhip64_6.dll`. I do not know if an ABI change has occured warranting this duality.

The Radeon Software driver installer installs both verisons, so the app will launch but misbehave in debug builds. Notice how clang is instructed to link to the only export lib in the SDK, `amdhip64.lib`, but the resulting binary will erronously result in linking to `amdhip64_6.dll` because it's contents are compatible with `amdhip64.dll` only. Copying the driver's non-6 DLL next to the executable and renaming it to have `_6` in it to make sure it gets picked up runs the program just fine. (I don't know why Dependencies won't find `amdhip64_6.dll` when it is clearly picked up during runtime, show in my first screenshot, as it's installed in `C:\Windows\System32`)

```
PS D:\Develop\ROCm-examples> & ${env:HIP_PATH}bin\clang++ .\HIP-Basic\saxpy\main.hip -o saxpy.exe -I .\Common -lamdhip64 -L ${env:HIP_PATH}lib --offload-arch=gfx1036 -ggdb -O0
PS D:\Develop\ROCm-examples> gci ${env:HIP_PATH}lib -fil amdhip*

    Directory: C:\Program Files\AMD\ROCm\6.1\lib

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---       2024. 06. 24.    15:40         134674 amdhip64.lib

PS D:\Develop\ROCm-examples> gci C:\Windows\System32\ -fil amdhip*

    Directory: C:\Windows\System32

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---       2024. 06. 26.    14:34       20426704 amdhip64_6.dll
-a---       2024. 06. 26.    14:34       21750848 amdhip64.dll

PS D:\Develop\ROCm-examples> Dependencies -depth=1 -modules .\saxpy.exe
[ROOT] saxpy.exe : .\saxpy.exe
[WellKnownDlls] KERNEL32.dll : C:\Windows\system32\kernel32.dll
[NOT_FOUND] amdhip64_6.dll :
PS D:\Develop\ROCm-examples> cpi C:\Windows\System32\amdhip64.dll .\amdhip64_6.dll
PS D:\Develop\ROCm-examples> .\saxpy.exe
Calculating y[i] = a * x[i] + y[i] over 1000000 elements.
First 10 elements of the results: [ 3, 5, 7, 9, 11, 13, 15, 17, 19, 21 ]
PS D:\Develop\ROCm-examples> $LASTEXITCODE
0
```

I'm sorry, but it is mindboggling how such an error can make it beyond QA, let alone vanilla CI testing. I don't want to guess whether this an ordinary SDK packaging problem or a development process issue, because it doesn't concern me, but it could've been caught by running Debug builds in CI or during QA. Please add it to the test matrix.

---

### 评论 #6 — jamesxu2 (2024-07-26T19:55:43Z)

Hello @MathiasMagnus, I just wanted to give an update on this issue:

Thanks for verifying that the minimal CLI reproducer still causes the hang on your side. 

1. Regarding the two DLLs, there was [a change](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/#hip-sdk-changes) in the way the amdhip64.dll is packaged in ROCm 6.1.2, the amdhip64_6.dll is the "new" dll but both are indeed shipped with the HIP SDK for Windows.
2. I'm still unable to reproduce your issue. Using a fresh install of Windows 11 Pro and the HIP SDK I don't see a hang with debug or release builds. (Thanks for your documentation by the way. I did not expect to encounter the author in this thread!)
3. My clang does link to the correct dll in system32. I'm not sure why your system is unable to find it. 
```
Dependencies.exe -depth=1 -modules .\saxpy.exe
[ROOT] saxpy.exe : .\saxpy.exe
[WellKnownDlls] KERNEL32.dll : C:\Windows\system32\kernel32.dll
[WindowsFolder] amdhip64_6.dll : C:\Windows\system32\amdhip64_6.dll
```
4. I can swap (via renaming) the amdhip64_6.dll and the amdhip64.dll and recompile saxpy using the "old" non-6 dll which works for you, and don't see a hang on either version. 

At this point, the only delta between our configurations appears to be the device and I'm starting to guess that the hang is an artifact of that, but I'm not sure what mechanism could cause a debug-only hang. I'm discussing this with our internal Windows HIP team and will keep you posted.

---

### 评论 #7 — MathiasMagnus (2024-07-26T20:28:34Z)

Do note that the SDK installer bundles the Pro driver only, but it doesn't appear as an installable component (the 610M PCI ID isn't allow-listed in the XML), so I'm running latest (non-PRO) Radeon Software, although AFAICT that shouldn't be too big a change either. _(I also wrote the Windows install guide, so I've fiddled with that to some extent too.)_

---

### 评论 #8 — jamesxu2 (2024-08-16T17:53:19Z)

Hi @MathiasMagnus, given the debugging effort so far I think your issue is specific to your device, in that the HIP SDK is not yet supported for APU, and attempting to use it on unsupported hardware might cause unexpected behavior . 

There is an effort to enable HIP SDK support for APU and you should try again when official support is released. Unfortunately, there's not much we can do until then.

amdhip64.dll is deprecated in favour of amdhip64_6.dll from ROCm 6.1.2 onwards, and the former is included in the install for backwards compatibility only. While it appears that you can swap them in your case, when APU support is officially enabled you should expect to link to amdhip64_6.dll (or whatever the most recent library is) to run on APU.



---

### 评论 #9 — Tilroe (2024-09-28T23:51:53Z)

Hi, apologies if its bad GitHub etiquette to comment on closed issues, I'm still new to GitHub collaboration. Just wanted to mention that I am experiencing pretty much the exact same issue, having tried on both my own project, as well as the provided Visual Studio HIP extension template that does matrix transpose. The hack of copying the non-'_6' dll from System32 into my own project's executable directory and renaming it to have the _6 did work.

Also, I'm running on a 7900 XTX, which [does appear to be supported](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html#supported-skus-win), so I am unconvinced of it being an issue of supported vs unsupported devices.

---

### 评论 #10 — jamesxu2 (2024-09-30T13:27:12Z)

Hi @Tilroe , can you provide some more information on what exactly you're running as well as your ROCm version and Windows version? I think it is okay to reopen this ticket, as it does appear that you're likely experiencing the same issue and I agree this issue wasn't fully resolved - I only came to the device-unsupported conclusion after ruling out all other system differences I could think of. 

Please provide the following information and I'll try to reproduce the issue on my side:

- ROCm version
- Windows version 
- CPU
- AMD driver (Adrenalin) Version 
- Code reproducer - I'm not sure what matrix transpose example you're referring to exactly. You could try the SAXPY example that's linked in this ticket. Also, some more detailed information on how you're compiling the code.


---

### 评论 #11 — Tilroe (2024-09-30T16:49:06Z)

Hi @jamesxu2 , thanks for reopening the ticket.

- ROCm version - 6.1.2
- Windows version - Windows 11 Home Version 10.0.22631 
- CPU - AMD Ryzen 9 7950X
- AMD driver - 24.7.1
- Code reproducer - Did the saxpy example too, just to keep the testing contained. Same problem. Letting Visual Studio do the compilation for me.

The matrix transpose example seems to have come when I installed the HIP for Visual Studio (HIP-VS) extension. I can see it when creating a new project as a template
![image](https://github.com/user-attachments/assets/4d8611d4-2519-44cd-b4a0-8882655cea25)



---

### 评论 #12 — DsoTsin (2024-10-01T08:19:35Z)

[main-compute.zip](https://github.com/user-attachments/files/17201802/main-compute.zip)
This executable reproduced this issue, hanging inside **amdhip64_6.dll**
![image](https://github.com/user-attachments/assets/94454311-def0-4b07-9859-fc33f4d060f5)
The only difference on the compilation flags are below:
![image](https://github.com/user-attachments/assets/daa4acfd-a3b1-48b9-8895-cbc068d4aa4a)
ROCm version - 6.1.2
Windows version - Windows 11 Home Version 10.0.22631
CPU - AMD Ryzen 9 7950X
AMD driver - 24.7.1
Code reproducer - Did the saxpy example too, just to keep the testing contained. Same problem. Letting Visual Studio do the compilation for me.
<img width="708" alt="image" src="https://github.com/user-attachments/assets/841699e5-4ae1-422c-a7cd-934c8f7326bc">
The amdhip64_6.dll are also different...
<img width="937" alt="image" src="https://github.com/user-attachments/assets/13ef4a49-c85e-495c-9219-c48cb83ccef3">
After replaced with **driver package's** dll, it will hang (dll provided by **sdk** will not hang when exitting) with debuggable build configuration..
So, can you provide static library of amdhip64_6 like cudart_static?

---

### 评论 #13 — jamesxu2 (2024-10-03T15:38:23Z)

Hi @Tilroe and @DsoTsin ,

I notice both of you are using 7950X CPUs, which have an integrated graphics processor (IGP). ROCm may default to use IGP instead of your discrete GPU, in which case you would be encountering the same issue as the original issue reporter who is also encountering a hang with the same symptoms and resolution when running on an unsupported IGP. There's a [warning to disable IGP](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#disable-integrated-graphics-igp-if-applicable) in your BIOS in the ROCm install prerequisites, though I don't think there's mention of this in the HIP on Windows docs.

@Tilroe , thanks for the source of the Matrix Transpose example - I notice it prints out the Device name at the start of the program - what does this say for you? With a Debug x64 Build compiled from the MatrixTranspose example via Visual Studio, I see:

```
Device name AMD Radeon RX 7900 XTX
Matrix[0]: 0.000000  |  TransposeMatrix[0]: 0.000000  |  cpuTransposeMatrix[0]: 0.000000
Matrix[1]: 10.987654  |  TransposeMatrix[1]: 703.209839  |  cpuTransposeMatrix[1]: 703.209839
Matrix[2]: 21.975307  |  TransposeMatrix[2]: 1406.419678  |  cpuTransposeMatrix[2]: 1406.419678
Matrix[3]: 32.962959  |  TransposeMatrix[3]: 2109.629395  |  cpuTransposeMatrix[3]: 2109.629395
Matrix[4]: 43.950615  |  TransposeMatrix[4]: 2812.839355  |  cpuTransposeMatrix[4]: 2812.839355
  [...]
Matrix[4094]: 44983.453125  |  TransposeMatrix[4094]: 44291.230469  |  cpuTransposeMatrix[4094]: 44291.230469
Matrix[4095]: 44994.441406  |  TransposeMatrix[4095]: 44994.441406  |  cpuTransposeMatrix[4095]: 44994.441406
The margin of error = 0.000001
PASSED!

C:\Users\rocm\source\repos\MatrixTranspose1\Debug\HIP clang 6.1\MatrixTranspose1.exe (process 13416) exited with code 0.
To automatically close the console when debugging stops, enable Tools->Options->Debugging->Automatically close the console when debugging stops.
```

---

### 评论 #14 — Tilroe (2024-10-03T18:13:09Z)

Hi @jamesxu2 , the matrix transpose example does correctly identify my 7900 XTX, so it does not appear to be an issue of accidentally using IGP.

```
Device name AMD Radeon RX 7900 XTX
Matrix[0]: 0.000000  |  TransposeMatrix[0]: 0.000000  |  cpuTransposeMatrix[0]: 0.000000
Matrix[1]: 10.987654  |  TransposeMatrix[1]: 703.209839  |  cpuTransposeMatrix[1]: 703.209839
Matrix[2]: 21.975307  |  TransposeMatrix[2]: 1406.419678  |  cpuTransposeMatrix[2]: 1406.419678
Matrix[3]: 32.962959  |  TransposeMatrix[3]: 2109.629395  |  cpuTransposeMatrix[3]: 2109.629395
Matrix[4]: 43.950615  |  TransposeMatrix[4]: 2812.839355  |  cpuTransposeMatrix[4]: 2812.839355
Matrix[5]: 54.938271  |  TransposeMatrix[5]: 3516.049316  |  cpuTransposeMatrix[5]: 3516.049316
Matrix[6]: 65.925919  |  TransposeMatrix[6]: 4219.258789  |  cpuTransposeMatrix[6]: 4219.258789
Matrix[7]: 76.913574  |  TransposeMatrix[7]: 4922.468750  |  cpuTransposeMatrix[7]: 4922.468750
   [...]
Matrix[4094]: 44983.453125  |  TransposeMatrix[4094]: 44291.230469  |  cpuTransposeMatrix[4094]: 44291.230469
Matrix[4095]: 44994.441406  |  TransposeMatrix[4095]: 44994.441406  |  cpuTransposeMatrix[4095]: 44994.441406
The margin of error = 0.000001
PASSED!
  [..blinking indefinitely..]
 ```
 
 (Also with Debug x64 Build)

---

### 评论 #15 — jamesxu2 (2024-10-04T20:47:32Z)

Hi @Tilroe  and @DsoTsin , 

I did a clean install of Windows 11 + ROCm 6.1.2 + Ryzen 7950X + 7900XTX with iGPU disabled and I only see a hang while using the Adrenalin 24.7.1 driver. I also tried running the matrix transpose with iGPU enabled and it didn't hang, though it did give incorrect results and fail the test.

I wasn't able to reproduce the hang on the Adrenalin driver that comes with the [HIP SDK installer](https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html) - 24.10.16
<img width="395" alt="image" src="https://github.com/user-attachments/assets/997d7fd2-e912-41c7-9200-125617feef3e">

**Please try upgrading your display driver** and let me know if you still encounter the hang. The [HIP SDK installer](https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html) can optionally do this (see above screenshot) while doing a factory reset (uninstalling previous graphics driver).

This might also fix the root issue of this original ticket @MathiasMagnus .

---

### 评论 #16 — DsoTsin (2024-10-05T01:23:02Z)

> Hi @Tilroe and @DsoTsin ,
> 
> I did a clean install of Windows 11 + ROCm 6.1.2 + Ryzen 7950X + 7900XTX with iGPU disabled and I only see a hang while using the Adrenalin 24.7.1 driver. I also tried running the matrix transpose with iGPU enabled and it didn't hang, though it did give incorrect results and fail the test.
> 
> I wasn't able to reproduce the hang on the Adrenalin driver that comes with the [HIP SDK installer](https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html) - 24.10.16 <img alt="image" width="395" src="https://private-user-images.githubusercontent.com/172289477/373803274-997d7fd2-e912-41c7-9200-125617feef3e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjgwOTEzMjIsIm5iZiI6MTcyODA5MTAyMiwicGF0aCI6Ii8xNzIyODk0NzcvMzczODAzMjc0LTk5N2Q3ZmQyLWU5MTItNDFjNy05MjAwLTEyNTYxN2ZlZWYzZS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQxMDA1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MTAwNVQwMTE3MDJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT02MGNlYzIxZDJmNzI0NTdlNjZhYzc2NjE4ZjY0NGZlNDhhOWQzZTVjZmY5YjhmYzkyNTViNTllZGY3ZTdmYmJlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.OTwy6k4fsCWjNkRWFX9jbZil25EJRNiDVrOhzCa2-bo">
> 
> **Please try upgrading your display driver** and let me know if you still encounter the hang. The [HIP SDK installer](https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html) can optionally do this (see above screenshot) while doing a factory reset (uninstalling previous graphics driver).
> 
> This might also fix the root issue of this original ticket @MathiasMagnus .

After driver upgraded, hang issue didn't occur. Thanks!

---

### 评论 #17 — MathiasMagnus (2024-10-05T19:50:49Z)

@jamesxu2 @DsoTsin Radeon Software 24.9.1 does indeed seem to solve the issue, not having to copy the old DLL as the new.

---
