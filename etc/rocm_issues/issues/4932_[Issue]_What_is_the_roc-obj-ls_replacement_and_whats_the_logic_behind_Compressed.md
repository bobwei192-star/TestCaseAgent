# [Issue]: What is the roc-obj-ls replacement and whats the logic behind Compressed Clang Offload Bundle

> **Issue #4932**
> **状态**: closed
> **创建时间**: 2025-06-16T18:53:11Z
> **更新时间**: 2025-12-16T16:20:49Z
> **关闭时间**: 2025-12-16T16:20:49Z
> **作者**: bbiiggppiigg
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4932

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- david-salinas

## 描述

### Problem Description

We need a way of extracing code-objects out of .hip_fatbin and pack them back together, so we can perform binary instrumentation on individual code-objects.
Previously, we rely on the logic implemented in rocm-obj-ls to extract the binaries and create headers that allow us to pack them back together.

With a newer version of rocm (6.3.6) we see .hip_fatbin could be of the format compressed clang offload bundle (CCOB), and the old rocm-obj-ls tool no longer works.
I tried using clang-offload-bundler it wasn't able to identify triples with --list option nor able to unbundle it.
I also tried llvm-objdump --offload-fatbin, but I maybe I didn't pass the right option, as I wasn't able to get it to dump anything.

Please let me know what is the right command/option to do so.
Link to the binary of interest is attached here.
https://mega.nz/file/UxtXmBAb#cE6IGKZ0LAveyjgi9xrPQwOuhZC5jyGXKZdRHJpfCXs

OS:
NAME="Rocky Linux"
VERSION="8.8 (Green Obsidian)"
CPU:
model name      : AMD EPYC 7402 24-Core Processor
GPU:
  Name:                    AMD EPYC 7402 24-Core Processor
  Marketing Name:          AMD EPYC 7402 24-Core Processor
  Name:                    AMD EPYC 7402 24-Core Processor
  Marketing Name:          AMD EPYC 7402 24-Core Processor
  Name:                    gfx900
  Marketing Name:          Radeon Instinct MI25
      Name:                    amdgcn-amd-amdhsa--gfx900:xnack-
      Name:                    amdgcn-amd-amdhsa--gfx9-generic:xnack-
  Name:                    gfx908
  Marketing Name:          AMD Instinct MI100
      Name:                    amdgcn-amd-amdhsa--gfx908:sramecc+:xnack-
  Name:                    gfx90a
  Marketing Name:          AMD Instinct MI210
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a
  Marketing Name:          AMD Instinct MI210
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-


### Operating System

Rocky Linux (RHEL 8.8)

### CPU

AMD EPYC 7402 24-Core Processor

### GPU

MI25 / MI100 / MI210

### ROCm Version

ROCm 6.3.6

### ROCm Component

llvm-project

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (22 条)

### 评论 #1 — ppanchad-amd (2025-06-16T19:06:54Z)

Hi @bbiiggppiigg. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-06-16T19:25:26Z)

Hi @bbiiggppiigg, there is no ROCm 6.3.6, so not sure what version your package corresponds to, but the deprecation note for `roc-obj-ls` in ROCm 6.4 (https://rocm.docs.amd.com/en/docs-6.4.0/about/release-notes.html#changes-to-rocm-object-tooling) suggests using `llvm-objdump --offloading`.

---

### 评论 #3 — bwelton (2025-06-16T19:39:33Z)

It is in CCOB format (https://github.com/ROCm/llvm-project/blob/47cf464183f41372a9ec0481a1f74ac03f477a45/clang/include/clang/Driver/OffloadBundler.h#L96-L108). HIP checks for this magic header to determine if the fatbin is compressed or not. My understanding is that we don't add any special sauce in compressing the fatbin vs standard CCOB support (useful info since you may be modifying then recompressing this bin). 

---

### 评论 #4 — bbiiggppiigg (2025-06-16T20:03:33Z)

> Hi [@bbiiggppiigg](https://github.com/bbiiggppiigg), there is no ROCm 6.3.6, so not sure what version your package corresponds to, but the deprecation note for `roc-obj-ls` in ROCm 6.4 (https://rocm.docs.amd.com/en/docs-6.4.0/about/release-notes.html#changes-to-rocm-object-tooling) suggests using `llvm-objdump --offloading`.

This is the version I got with a rocm built with the AOMP scripits.
https://github.com/ROCm/aomp/blob/aomp-dev/docs/SOURCEINSTALL.md

I tried running llvm-objdump --offloading.
On the newer MIOpen I built, I got an error to decompress.
On the older MIOpen I built, it simply shows nothing.
So I have no way of confirming whether the tool is working as intended.
![Image](https://github.com/user-attachments/assets/9706f802-864f-44d0-9958-b8ca34b0ba99)

---

### 评论 #5 — bbiiggppiigg (2025-06-16T20:05:12Z)

> It is in CCOB format (https://github.com/ROCm/llvm-project/blob/47cf464183f41372a9ec0481a1f74ac03f477a45/clang/include/clang/Driver/OffloadBundler.h#L96-L108). HIP checks for this magic header to determine if the fatbin is compressed or not. My understanding is that we don't add any special sauce in compressing the fatbin vs standard CCOB support (useful info since you may be modifying then recompressing this bin).

Yeah I suppose I could write a tool that do the compression and decompression and add the headers myself, if there is no tooling to do so, or maybe llvm-objdump is the intended tool

---

### 评论 #6 — schung-amd (2025-06-17T14:39:04Z)

> On the newer MIOpen I built, I got an error to decompress.

@bbiiggppiigg Thanks for checking, I can repro the error you're seeing on various .so files in the ROCm directory as well. Seems like this is potentially a known issue with `llvm-objdump` that we've been investigating, I'll take a look.

---

### 评论 #7 — schung-amd (2025-06-20T13:53:07Z)

This was indeed a known issue, and we are currently working on a solution. The fix will likely be aimed at ROCm 7, but hopefully we'll be able to cherry pick it or provide a patch in the interim.

---

### 评论 #8 — david-salinas (2025-10-15T20:14:45Z)

The patch for compressed bundles is available in llvm-objdump as of ROCm 7.0.

Also of note, the option "--offloading" has been added to llvm-readobj.  This functionality replicates the behaviour of roc-obj-ls and gives a listing (in URI form) of all HIP offload bundle entries in the same way roc-obj-ls did.  You can use a command similar to "llvm-readobj --offloading <exe | object file>".  This is probably more in line with the functionality you are looking for, I believe. 

---

### 评论 #9 — bbiiggppiigg (2025-10-15T20:17:55Z)

> The patch for compressed bundles is available in llvm-objdump as of ROCm 7.0.
> 
> Also of note, the option "--offloading" has been added to llvm-readobj. This functionality replicates the behaviour of roc-obj-ls and gives a listing (in URI form) of all HIP offload bundle entries in the same way roc-obj-ls did. You can use a command similar to "llvm-readobj --offloading <exe | object file>". This is probably more in line with the functionality you are looking for, I believe.

I'll give it a try.
Thank you.

---

### 评论 #10 — bbiiggppiigg (2025-10-20T17:11:40Z)

@schung-amd @david-salinas 

Hi, I can verify that on ROCM-7.0.2
llvm-readobj --offloading is giving me the file URIs of the embedded code-objects, and that 
llvm-objdump --offloading dumps "all" the embedded code-objects associated with the input binary.

Now suppose I want to examine only one particular code-object, what should I do ?
I tried to pass the FILE URI reported by llvm-readobj to roc-obj-extract, but it seems like the tool is broken and creates a file that is not of the specified size nor an ELF.




---

### 评论 #11 — bbiiggppiigg (2025-10-20T17:16:09Z)

Here is a screenshot of the result of executing roc-obj-extract.
The files vectoradd_hip.exe.0.hipv4-* are generated by llvm-objdump --offloading.
I specified offset 4096, and size 30816, end up getting a file of size 95680.

<img width="1668" height="390" alt="Image" src="https://github.com/user-attachments/assets/c54f63a4-43fe-4c02-baf0-aeee7146e59d" />


---

### 评论 #12 — david-salinas (2025-10-20T18:09:08Z)

@bbiiggppiigg If the executable was generated with compressed bundles the roc-obj-extract tool will not work. But i suspect the issue is that you need to escape the '&' character in the URI, and the "size" is not being given to the (deprecated) roc-obj-extract tool.

Also, you can use "llvm-objcopy --dump-offload-bundle=<URI>" which should handle compressed bundles.  But don't forget to escape the '&' character in URI otherwise your command shell will treat it as the "run in background command" and not pick up the "size" in the URI properly.  Which might be the issue you're facing if the executable wasn't built with compressed bundles.

---

### 评论 #13 — bbiiggppiigg (2025-10-20T18:22:37Z)

@david-salinas 
Thanks for pointing out the problem with escaping &. I should have noticed it from the background execution.
That being said, llvm-objcopy doesn't seem to work, and output the same stuff as roc-obj-extract.


<img width="1668" height="400" alt="Image" src="https://github.com/user-attachments/assets/fd31d725-75ce-4eb5-8548-565d05412c96" />

---

### 评论 #14 — david-salinas (2025-10-20T18:53:19Z)

The generated .co file is a Binary code object file, so it's not human readable.  You can disassemble the binary code object with "llvm-objdump -d vectoradd_hip.exe-offset4096-size30816.co".  That will give you ISA instructions.

---

### 评论 #15 — bbiiggppiigg (2025-10-20T18:58:14Z)

I know it is not suppose to be human readable. I was trying to make the point that it is not an ELF so it didnt' start with the ELF magic, but I  guess I didn't make it clear enough.

---

### 评论 #16 — lamb-j (2025-10-21T17:32:39Z)

> We need a way of extracing code-objects out of .hip_fatbin and pack them back together, so we can perform binary instrumentation on individual code-objects.

If you want to unbundle/rebundle a Clang Offload Bundle (contents of the .hip_fatbin section), you can use the clang-offload-bundler tool. It works with both compressed and uncompressed bundles:

https://clang.llvm.org/docs/ClangOffloadBundler.html

"llvm-objdump --offload" has a similar functionality, but we can't re-bundle without the clang-offload-bundler

> I tried using clang-offload-bundler it wasn't able to identify triples with --list option nor able to unbundle it.

That should work. If you post your clang-offload-bundler commands and errors I can help debug

---

### 评论 #17 — bbiiggppiigg (2025-10-21T18:23:31Z)

> If you want to unbundle/rebundle a Clang Offload Bundle (contents of the .hip_fatbin section), you can use the clang-offload-bundler tool. It works with both compressed and uncompressed bundles:
> 
> https://clang.llvm.org/docs/ClangOffloadBundler.html
> 

> 
> > I tried using clang-offload-bundler it wasn't able to identify triples with --list option nor able to unbundle it.
> 
> That should work. If you post your clang-offload-bundler commands and errors I can help debug


fatbin.out is the content of the .hip_fatbin section, which I dumped using llvm-objcopy --dump-section, and contains two CCOBs.

<img width="833" height="87" alt="Image" src="https://github.com/user-attachments/assets/f47b3c75-742f-40d6-9a4d-e27757626b0d" />

Running clang-offload-bundler on them wouldn't work, I'm guessing maybe I need to chop it into separate CCOBs first for clang-offload-bundler to work?

<img width="1498" height="164" alt="Image" src="https://github.com/user-attachments/assets/2bb2736e-b542-4998-981d-1c6908283595" />


> "llvm-objdump --offload" has a similar functionality, but we can't re-bundle without the clang-offload-bundler

llvm-objdump --offloading works that dumps all the code-objects in all the bundles in the binary.
I'm working on a tool that based on the output of llvm-objudmp --offloading, to merge these dumped code-objects into separate bundles and concat them back together to form the content of a new .hip_fatbin section. 

But the alternative solution you guys mentioned, llvm-objcopy --dump-offload-bundle,  does not work.

<img width="1370" height="563" alt="Image" src="https://github.com/user-attachments/assets/3bc7948a-de66-434b-b9f0-f8f46fb9c39b" />

As you can see here, the output file is identified as data.
Indeed it does not start with ELF.


<img width="1024" height="46" alt="Image" src="https://github.com/user-attachments/assets/62cb3640-616c-4d36-8780-56974df3e7a3" />






---

### 评论 #18 — lamb-j (2025-10-21T18:42:16Z)

Can you share the command you used to generate the fat binary? I'm curious how we ended up with two concatenated compressed offload bundles in the .hip_fatbin section

---

### 评论 #19 — david-salinas (2025-10-21T18:42:38Z)

@bbiiggppiigg llvm-objcopy (and roc-obj-extract) only extracts the specific offload bundle entry specified in the URI.  It does not generate a standalone ELF object. 

| I'm working on a tool that based on the output of llvm-objudmp --offloading, to merge these dumped code-objects into separate bundles and concat them back together to form the content of a new .hip_fatbin section.

I think you will need to use the clang-offload-bundler (or maybe clang-offload packager?) to do this with the extracted bundle entries.  But then I'm not sure how you would setup the host side to call the offload bundle entries (kernels).

---

### 评论 #20 — bbiiggppiigg (2025-10-21T19:07:25Z)

> Can you share the command you used to generate the fat binary? I'm curious how we ended up with two concatenated compressed offload bundles in the .hip_fatbin section

.hip_fatbin section contains a list of clang_offload_bundle, one for each compilation unit, each containing the code objects for multiple possible architectures supported on the system.

For example, in a libMIOpen I built, it contains 151 CCOBs in the .hip_fatbin section, each containing 4 code objects (or 3 since the host one doesn't really matter), so roughly 604 lines of output when llvm-readobj --offloading is called.

<img width="1112" height="153" alt="Image" src="https://github.com/user-attachments/assets/5a99c3d9-37ca-4e46-9d8f-713bc7190d32" />



> I think you will need to use the clang-offload-bundler (or maybe clang-offload packager?) to do this with the extracted bundle entries. But then I'm not sure how you would setup the host side to call the offload bundle entries (kernels).

.hipFatinSegment contains a list of pointers, each pointing to the where these code-objects will be loaded (The address of the .hip_fatbin section + offsets of the CCOB within the section).

At least previously, all we need to do is to get the repacked code-object to work is to patch the pointers in .hipFatbinSegment to point to the corresponding CCOB in the new .hip_fatbin Section. 






---

### 评论 #21 — david-salinas (2025-10-21T19:30:15Z)

Ok, I think the issue you may face is that the bundles are compressed.  And you can't rely on the "offset" in the URI to be accurate.  The tools (llvm-readobj, llvm-objcopy, and llvm-objdump) auto-magically handle compressed bundles under the covers.  So even if you pass the URI to llvm-objcopy, it will know/see that the source file is compressed, decompress it and then extract based on the URI offset and size.  

---

### 评论 #22 — david-salinas (2025-12-03T21:20:38Z)

Latest ROCm 7.* has support in llvm tools that replicates functionality in the roc-obj-* tools:

- roc-obj-ls --> "llvm-readobj --offloading"
- roc-obj-extract --> "llvm-objcopy --dump-offload-bundle <URI>"
- roc-obj --> "llvm-objdump --offloading"

The old roc-obj* tools did not support compressed offload bundles, but the new llvm-* tools do.

Closing this issue if there are no other concerns.


---
