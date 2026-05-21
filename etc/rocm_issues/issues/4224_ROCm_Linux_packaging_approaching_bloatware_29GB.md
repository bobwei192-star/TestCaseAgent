# ROCm Linux packaging approaching bloatware: 29GB

> **Issue #4224**
> **状态**: open
> **创建时间**: 2025-01-06T01:40:59Z
> **更新时间**: 2025-10-17T17:36:00Z
> **作者**: Qubitium
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4224

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Why is Linux official Ubuntu 24.04 ROCm 6.3.1 pkgs installing 29G of files under `/opt/rocm-6.3.1`? 

This is borderline bloatware on a new level. Did devs forget to follow standard procedures and share libs? Sorry if this sound negative because I don't know how else to describe it.

Maybe there is a valid reason but please explain the reasons if possible. Cuda toolkit is 3GB for comparison.

I want ROCm to succeed but not with this bloatware size that no sane user would want on any platform.

* Can we and how do we compile rocm so only set arch is included? For examplex, only compile for RDNA2 7900XTX? Trying to think of a way to reduce this monstrosity.





---

## 评论 (26 条)

### 评论 #1 — IMbackK (2025-01-06T10:55:19Z)

rocm uses gpu isa directly. To get good performance you have to have kernels for various problem sizes.
This means that for etach function in rocm libaries like rocblas there are NxM (N= gpu chip, M = problem size) implementations available with N being on the order of 10 and M variing from 1 to 100 or so. So yeah this inevitably results in absoluty huge binaries.

Yes you can build rocm for just one arch, but this is a pretty big undertakeing since rocm is huge.

You can also only install the parts of rocm you care about. Rocm contains a tonne of libaries that provide kernels for specific tasks, most users will only need a couple of those. If you dont need rocsolver dont install rocsolver etc

---

### 评论 #2 — Qubitium (2025-01-06T13:04:44Z)

@IMbackK Makes more sense now but my simple test also show the custom gpu kernels only comprise ~1/2 of the 29GB total. 

The 29GB result is simple following Ubuntu package manager rocm guide. The alternate linux binary install failed for us:

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/native-install/ubuntu.html

* Low-hanging fruit: make the `gfxXXX` specific kernels part of the `hipblaslt-gfxXXX` optional package. This will save  ~`14GB` of pkg space based on my simple test below.  However `15GB` of core libs still remain.  Almost half the size and packaging wise much easier for users. 

Perhaps an util pkg util such as `rocm-kernels-install --gfx1102` or `rocm-kernels-install --auto` util that will `auto` install based on current hardware or manually specify `gfxXXX`? This only solves half the equation as 15GB of core libs still need to be trimmed somehow. 

```py
# keep only gfx1100 (7900XTX) files
import os
import re

def delete_files(directory):
    # Regular expression to match files ending with gfxXXX
    pattern = re.compile(r'gfx\d+(a)*\.(dat|co|hsaco)$')
    # Regular expression to exclude files ending with gfx1100
    exclude_pattern = re.compile(r'gfx1100\.(dat|co|hsaco)$')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern.search(file) and not exclude_pattern.search(file):
                file_path = os.path.join(root, file)
                print(f"Deleting {file_path}")
                os.remove(file_path)

# Replace 'your_directory_path' with the path to the directory you want to clean up
delete_files('./rocm-6.3.1/lib/hipblaslt/library') 
# there are several directories that contain gfx specific files
```
After deleting all non `gfx1100` files, `/opt/rcom-6.3.1` is now `15GB` vs `29GB`. 

```
# du -h | grep G
2.6G ./rocm-6.3.1/lib/rocfft
1.5G	./rocm-6.3.1/lib/llvm
14G	./rocm-6.3.1/lib
15G	./rocm-6.3.1
15G	.
```




---

### 评论 #3 — IMbackK (2025-01-06T13:27:39Z)

Its not just those files, every binary part of rocm is compiled N times and has N embedded binaries. if you look at roc-obj-ls /opt/rocm/lib/libMIOpen.so for instance you will see that libMIOpen.so contains a tonne of embedded code objects, one for every chip. Its the same for every single rocm binary. The tensile code objects like TensileLibrary_Type_ZZ_Contraction_l_Alik_Bljk_Cijk_Dijk_gfx908.co are just the tip of the iceberg

you cant exclude archtiectures at install time because the binaries are created at compile time with code for eatch architecture. the only way to exclude architectures is to recompile everything, which requires a lot of time and absolutly huge amounts of memory for some rocm componants, makeing it impossible to do on client machines.

---

### 评论 #4 — Qubitium (2025-01-06T13:55:01Z)

You are right about `/opt/rocm/lib/libMIOpen.so`. This file and many like it are absolutely huge too that embeds the custom kernels per gpu per shape. But I don't amd has to statically linking all the libs inside huge files. Use dynamic links via support/aux package.

The problem is huge, for the package people,.but there is gotta be way to fix this. The gpu * shape * feature will continue to grow will only get worse. Deprecating and not supporting or dropping support for fairly recent gpus is already a problem for amd so that route is closed. Or not. Move all the older than 2 generation and earlier gpus to `package-legacy`. Installable, linkable but separated.

Like you said, we cant fix this post install. The packaging and hw/shape/feature kernels and runtime dynamic linking needs to be reimagined and designed from first lib entry/binding. Forget backward compat, fix it for good for now and future gens.



---

### 评论 #5 — saadrahim (2025-01-06T16:09:43Z)

Perhaps an util pkg util such as rocm-kernels-install --gfx1102 or rocm-kernels-install --auto util that will auto install based on current hardware or manually specify gfxXXX? This only solves half the equation as 15GB of core libs still need to be trimmed somehow.

@Qubitium Can you elaborate what a util pkg is? I did not know that packages can take arguments. 

---

### 评论 #6 — Qubitium (2025-01-06T17:29:59Z)

> @Qubitium Can you elaborate what a util pkg is? I did not know that packages can take arguments. 

In my example, `rocm-kernels` is an command installed by base rocm pkg or rocm-kernels package. 

After the rocm-base/core is installed, end user can execute `rocm-kernels -install` and pass it args to assist secondary install of kernels/precompiled custom gpu * shape * feature libraries. The command would understand the gfxXXX options and platform and use the correct pkg manager (deb, rpm, etc) to install the correct aux files.





---

### 评论 #7 — fxmarty-amd (2025-01-09T15:21:53Z)

![image](https://github.com/user-attachments/assets/77c5289d-06f1-466a-82e1-1981b157637a)

Calling `apt install rocblas rocblas-dev hipblas hipblas-dev` from a container running https://hub.docker.com/r/rocm/dev-ubuntu-22.04.

At the same time vllm appears to depend on rocblas/hipblas and the docker image is relatively lighter, wondering why: https://hub.docker.com/r/rocm/vllm-dev/tags

Is there a recommended approach to target a single arch?

---

### 评论 #8 — fxmarty-amd (2025-01-10T10:48:15Z)

Related issue: https://github.com/ROCm/ROCm/issues/2093 https://github.com/ROCm/ROCm-docker/issues/120

This is kind of an issue as building images on top of rocm docker images & pushing them to cloud registries uses several 10s of GB just for a base rocm image.

> As @saadrahim suggested, using multi-stage custom builds that only include the necessary components might be the best way to use ROCm on docker for now if storage is an issue. This needs to be done case-by-case. Unfortunately, there is little we can do at the moment.

@tcgu-amd is there a recommended / example for this? The software I am working with essentially eventually needs me to pull all of `rocrand rocrand-dev hiprand hiprand-dev rocblas rocblas-dev hipblas hipblas-dev hipblaslt-dev hipblaslt miopen-hip miopen-hip-dev hipfft hipfft-dev hipsparse hipsparse-dev rocprim-dev hipcub rocthrust hipsolver` indiscriminately, and I guess my best option would be to build those from source, targeting a single arch? Is there a dockerfile for this?

At least for rocblas, this might be useful:
![image](https://github.com/user-attachments/assets/2fc02ad1-e671-4bc3-a813-f73624444e1d)

HipblasLt is worse, as all the large binaries are for gfx942, so an user working on MI200/MI210/MI250 has to pull many unnecessary GBs:
![image](https://github.com/user-attachments/assets/aaea4e37-5cc0-4637-a42c-6a849b614dae)

rocfft is 2.7 GB, and I suspect in my case the fault is dependency of downstream library on some rocm package that depend on rocfft, and in turns I need to have it installed to have no build error.

Not sure whether librocsolver (1.7 GB) and librocsparse (1.4 GB) are needed for classical deep learning problems, but I need to have these installed as well to have no build error on my downstream software.

I am also wondering whhy tensile .co shared objects are so large?

---

### 评论 #9 — fxmarty-amd (2025-01-10T11:13:34Z)

Looking at the largest 300 MB .co file: https://gist.github.com/fxmarty-amd/33a607cf0431b4b77ac57398735e2175

`file TensileLibrary_BB_BB_A_Bias_SAV_UA_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx942.co` also gives `TensileLibrary_BB_BB_A_Bias_SAV_UA_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx942.co: ELF 64-bit LSB shared object, *unknown arch 0xe0* version 1, dynamically linked, not stripped, too many notes (256)`.

Does this mean debug symbols are shipped with tensile release included in hipblaslt, or is `file` giving erroneous information? If it is, is it intended?

Stripping `TensileLibrary_BB_BB_A_Bias_SAV_UA_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx942.co` from debug symbols with `/opt/rocm/lib/llvm/bin/llvm-strip` gives ~10% reduction in file size. So maybe ~2 GB in the 24 GB from hipblaslt/library are just debug symbols?

---

### 评论 #10 — bstefanuk (2025-01-10T17:47:40Z)

@fxmarty-amd I will investigate the status of the debug symbols in the release builds, if they are being shipped with debug symbols, then we will remove those.

@Qubitium @IMbackK We are aware of this issue and appreciate your feedback on the matter. About a month ago I pushed a PR in hipBLASLt that introduces code object compression (https://github.com/ROCm/hipBLASLt/pull/1374). This reduces the size of gfx942 libraries by 9x. Improvements are on the way.

---

### 评论 #11 — Qubitium (2025-01-11T02:46:43Z)

@fxmarty-amd  @bstefanuk  Thank you two for taking up the task and happy to see the potential results already in progress.  I am sure the end-result will benefit everyone. Knowing the people involved, I know it will get done. Third party developers like myself see the impact first and we are the first line of defense before actual end-users. 

---

### 评论 #12 — polarathene (2025-01-14T03:46:21Z)

> I guess my best option would be to build those from source, targeting a single arch? Is there a dockerfile for this?

The linked issue you provided has a comment that links to someones own `Dockerfile` that produces a 3GB image for PyTorch: https://github.com/ROCm/ROCm-docker/issues/120#issuecomment-2016647700

I am not too familiar with ROCm or given their `Dockerfile` a look but from the repo name they have I assume it's building only for `gfx1012` and anything else they need to support that with PyTorch. Not sure why they're providing their own Python though, perhaps at the time they needed a newer release than their base image had packaged.

As for the vllm image linked, 5.5GB is ROCm, the remainder is PyTorch related support [from the looks of it](https://hub.docker.com/layers/rocm/vllm-dev/20250113/images/sha256-382aa2fa8a9bffe2dd9d56c074c082dcb3935beabfbed21769e0d3cc851c309a), sadly there's no context about where that Dockerfile source is from exactly 😓 You can see that they've restricted support with `ARG PYTORCH_ROCM_ARCH=gfx90a;gfx942` for example.

---

Ideally, ROCm org would officially build and publish slimmed down images for each variant.
- Using Zig would help keep any dependency upon glibc low for compatibility
- If wanting to handle packaging in various formats then using something like GoReleaser can nicely support that.
- For minimal docker images Canonical has `chisel` but would need ROCm to contribute slices. Alternatively Fedora does quite well with `dnf --install-root` (_so long as DNF has the packages to install_), `--install-root` will allow you to build a reasonably minimal image to support just the packages listed.
- CI with Github Actions makes managing all this quite simple, but presumably needs external runners. There's some self-hosted alternative IIRC that could also be used that allows using GHA workflows/actions.

---

### 评论 #13 — AngryLoki (2025-01-15T10:01:01Z)

What is even bigger is official `rocm/pytorch` image. It is 81.4GB! And it is not some comprehensive compatibility kit to verify apps with a matrix of python/pytorch combinations. It is just a single python with a single pytorch.
```
docker images
REPOSITORY               TAG          IMAGE ID       CREATED         SIZE
rocm/pytorch             latest       29b84a99202a   5 weeks ago     71GB
rocm/pytorch-nightly     latest       1ffb192c599b   4 weeks ago     81.4GB
```

@fxmarty-amd, I tried to strip rocm libraries (i. e. Gentoo splits/strips debug info automatically, unless manually disabled), it causes crashes. See https://github.com/gentoo/gentoo/blob/92237158d45e3059ddb7ce058588338cb6449420/sci-libs/hipBLASLt/hipBLASLt-6.3.0.ebuild#L125-L126 for the details. I think it is possible to ask `strip` not to touch `STRTAB` section, but one cannot simply call `strip` for hipBLAS/rocBLAS/hipBLASLt. Also in some cases `*.hsaco` are not elf files (they are clang-offload-bundler files), strip does not know how to work with them.

---

### 评论 #14 — fxmarty-amd (2025-01-15T10:56:40Z)

@AngryLoki thank you for searching. Actually, I was probably misguided by `file`'s `not stripped`, on the other hand e.g. `rocgdb TensileLibrary_BB_BB_A_Bias_SAV_UA_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx942.co` tells me

```
Reading symbols from TensileLibrary_BB_BB_A_Bias_SAV_UA_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx942.co...
(No debugging symbols found in TensileLibrary_BB_BB_A_Bias_SAV_UA_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx942.co)
```

Although stripping with `/opt/rocm/lib/llvm/bin/llvm-strip`'s `--strip-debug` still reduces the binary size.

```
-rw-r--r-- 1 root root  270M Jan 15 10:38 mystrip_all
-rw-r--r-- 1 root root  270M Jan 15 10:37 mystrip_unneeded
-rw-r--r-- 1 root root  290M Jan 15 10:37 mystrip_debug
-rw-r--r-- 1 root root  309M Dec  4 03:06 TensileLibrary_BB_BB_A_Bias_SAV_UA_Type_BB_HPA_Contraction_l_Ailk_Bljk_Cijk_Dijk_gfx942.co
```

Looking at `readelf` though for the binary stripped with `--strip-debug`, it is only the sections `shstrtab` and `strtab` that are shrinked, there is no debug section or anything like that.

Looking at the symbols removed with `--strip-unneeded`, you have some static symbols (actually, all static symbols) like
```
0000000000000008 l       *ABS*	0000000000000000 vgprValuA_X2_I0
000000000000000a l       *ABS*	0000000000000000 vgprValuA_X3_I0
...
000000000012dd7c l       .text	0000000000000000 label_To_Activation_Relu_VW1
000000000012dd94 l       .text	0000000000000000 label_To_Activation_Sigmoid_VW1
000000000012ddac l       .text	0000000000000000 label_To_Activation_Tanh_VW1
000000000014bf00 g     F .text	0000000000000000 .protected Cijk_Alik_Bjlk_S_MX_B_Bias_AS_SAV_UserArgs_MT192x16x64_MI16x16x1_SN_LDSB1_AFC1_AFEM1_AFEM1_ASEM1_CLR1_CADS0_EPS0_GRVWA4_GRVWB4_GSUAMB_ISA942_IU1_K1_LBSPPA256_LBSPPB256_LBSPPM0_LPA8_LPB16_LPM0_LRVW4_LWPMn1_MIAV1_MIWT3_1_MO40_NTn1_NTA4_NTB0_NTC0_NTD0_NTM0_NEPBS8_NLCA1_NLCB1_ONLL1_PGR2_PLR1_PKA1_SIA3_SS1_SPO0_SRVW0_SSO0_SVW1_TLDS1_ULSGRO0_USL1_UIOFGRO0_USFGROn1_VSn1_VWA1_VWB1_WSGRA0_WSGRB0_WS64_WG64_4_1_WGMXCC1_WGMXCCG0
000000000010ccc0 g     O .rodata	0000000000000040 .protected Cijk_Alik_Bjlk_S_MX_B_Bias_AS_SAV_UserArgs_MT192x16x64_MI16x16x1_SN_LDSB1_AFC1_AFEM1_AFEM1_ASEM1_CLR1_CADS0_EPS0_GRVWA4_GRVWB4_GSUAMB_ISA942_IU1_K1_LBSPPA256_LBSPPB256_LBSPPM0_LPA8_LPB16_LPM0_LRVW4_LWPMn1_MIAV1_MIWT3_1_MO40_NTn1_NTA4_NTB0_NTC0_NTD0_NTM0_NEPBS8_NLCA1_NLCB1_ONLL1_PGR2_PLR1_PKA1_SIA3_SS1_SPO0_SRVW0_SSO0_SVW1_TLDS1_ULSGRO0_USL1_UIOFGRO0_USFGROn1_VSn1_VWA1_VWB1_WSGRA0_WSGRB0_WS64_WG64_4_1_WGMXCC1_WGMXCCG0.kd
```
that are removed. Dynamic symbols are untouched. I have no idea whether it is good or not, should actually test to see what happens.

---

### 评论 #15 — LunNova (2025-01-20T23:47:51Z)

Potential long term fix if SPIRV kernel performance is acceptable: https://github.com/ROCm/ROCm/issues/3985#issuecomment-2552432623

---

### 评论 #16 — Spacefish (2025-01-27T12:44:40Z)

Maybe have some "skeleton" package for ROCm / bundled ROCm in pytorch and such, which detects the GPUs and their arch currently present in the machine and downloads the appropriate kernels and compilers and caches them locally.

Much like models are downloaded from different "*hubs" in most machine learning frameworks.

Obviously that would be a huge undertaking especially regarding the hip compiler now having a "shim" binary which downloads other binaries behind the scenes and so on..

An intermediate step could be to offer ROCm builds for all different architectures as seperat packages, so you only need to install the one you really need locally. -> potential complication for users to pick the right package / not easy to depend on.

---

### 评论 #17 — darksylinc (2025-04-06T06:10:44Z)

There are two things I don't understand:

> Yes you can build rocm for just one arch, but this is a pretty big undertakeing since rocm is huge.

What is stopping rocm from having a tool that splices math libraries by ISA?

AMD builds rocm once for all ISA, then another tool ran by AMD splices it by ISA, publishes the packages, then installer in the client machine recombines the spliced ISAs (likely just one ISA for the GPU the user has installed) so it can be used.

> rocm uses gpu isa directly. To get good performance you have to have kernels for various problem sizes.
This means that for etach function in rocm libaries like rocblas there are NxM (N= gpu chip, M = problem size) implementations available with N being on the order of 10 and M variing from 1 to 100 or so. So yeah this inevitably results in absoluty huge binaries.

The other thing I don't understand is that these ISAs are practically 90% the same. Slight predictable changes in the encoding + a few new instructions. They should compress extremely well.
A specifically-written transpiler should be fast enough to do it either at install time, or at runtime when launching an app.

---

### 评论 #18 — mike-callahan (2025-04-16T03:40:58Z)

I am also frustrated by this. We use rocm with jax on a kubernetes cluster and a 32GB image is the smallest I have successfully built. 

I tried building ROCm 6.3.3 from source targeting the mi300x architecture leading to a 21GB container. I deployed the container and got a segmentation fault. 

We usually use 6.2.1 so I also tried building that from source but it wouldn't even compile. 

---

### 评论 #19 — fxmarty-amd (2025-05-16T09:25:37Z)

Any update @powderluv ?

An other issue is that `torch` from https://pytorch.org/get-started/locally/ bundles hipblaslt, rocblas, etc. although the host already has these in `/opt/rocm`.

![Image](https://github.com/user-attachments/assets/6fdb5c83-2052-4ab1-b889-7bbd4231db2c)

![Image](https://github.com/user-attachments/assets/0313e481-3274-4533-abaf-2a7b0b6426d5)

---

### 评论 #20 — Seneral (2025-05-21T21:21:00Z)

This keeps me from using it as a user - had it installed before, but keep uninstalling it, I don't get 30GB of space worth of utility out of it, not even close. Most linux users will also not have accounted for this bloat when sizing their system partition. This desperately needs to be fixed.

---

### 评论 #21 — darren-amd (2025-06-09T15:40:47Z)

> Any update [@powderluv](https://github.com/powderluv) ?
> 
> An other issue is that `torch` from https://pytorch.org/get-started/locally/ bundles hipblaslt, rocblas, etc. although the host already has these in `/opt/rocm`.
> 
> ![Image](https://github.com/user-attachments/assets/6fdb5c83-2052-4ab1-b889-7bbd4231db2c)
> 
> ![Image](https://github.com/user-attachments/assets/0313e481-3274-4533-abaf-2a7b0b6426d5)

Hi @fxmarty-amd ,

We have reduced the size of ROCm to around 22 GB for the 6.4 release, and have further initiatives planned for further reductions. For the second question, I can confirm that we plan to release lightweight wheels for Pytorch in the 7.0 release, which will significantly reduce package size by not including ROCm libraries that are already installed.

---

### 评论 #22 — polarathene (2025-06-09T23:02:10Z)

Are there similar tools for ROCm to these equivalents for CUDA?:
- [`cuobjdump`](https://docs.nvidia.com/cuda/cuda-binary-utilities/index.html#cuobjdump) (_inspect which archs were compiled in_)
- [`nvprune`](https://docs.nvidia.com/cuda/cuda-binary-utilities/index.html#nvprune) (_prune to specific arch(s)_)

With those you can inspect the fat objects provided in nvidia containers and strip away any archs you don't need to reduce weight.

I assume that would allow the rough equivalent of building ROCm libs for a single arch, but be more efficient (vs building) for individuals as they could just bring in the libs from the official image, strip away what isn't necessary and then `COPY` the image to a `FROM scratch`? 🤔 

---

### 评论 #23 — AngryLoki (2025-06-13T04:28:20Z)

I've build a treemap for current `rocm/pytorch-nightly` image.
<img width="950" alt="Image" src="https://github.com/user-attachments/assets/0879dd96-d1e1-403c-94c4-66a11a219fa1" />

Interactive version: [https://angryloki.github.io/rocm_image_vis/](https://angryloki.github.io/rocm_image_vis/), [build script](https://github.com/AngryLoki/rocm_image_vis/blob/main/build.sh)

Few highlights:
* `/var/lib/jenkins` - 18.2 Gb
* `/tmp` - 13 Gb
* `/root/` - 480 Mb
* `/opt/conda/envs/py_3.10/lib/python3.10/site-packages/nvidia` - 2.6 Gb + `cusparselt` - 0.2 Gb
* Few Gb of composable-kernel static libraries (maybe useful in rocm images, not so useful in pytorch images)
* MKL ~ 1 Gb (thanks conda)

---

### 评论 #24 — sylcas (2025-07-17T16:09:50Z)

Good news everyone! ;)

Today I succeeded in shrinking the container to a size of ~6.8 GB (unpacked disk size!) and I could successfully run faster-whisper (then ~7.2 GB) with it.

The trick for a working rocm/pytorch container boils down to this:

The rocm libraries are already shipped with the torch modules, there are only a few things missing to make it run without the rest of the /opt/rocm stuff and the *.dat, etc files can be deleted:

```
# find and delete everything that is not my Radeon 9070 (gfx1201, but gfx1200 is also needed)
find /pytorch/lib/ -type f -regextype posix-extended -regex '.*gfx[0-9]+[^/]*\.(dat|co|hsaco)$' -not -regex '.*gfx120[0-9]+[^/]*\.(dat|co|hsaco)$' -delete

# copy missing profiles
cp /opt/rocm-6.4.1/lib/libhsa-amd-aqlprofile64.so lib/python3.13/site-packages/torch/lib/
# link runtime correctly
cd /pytorch/lib/python3.13/site-packages/torch/lib
ln -s libhsa-runtime64.so libhsa-runtime64.so.1
# copy missing hipversion
cp /opt/rocm/share/hip/version /pytorch/lib/python3.13/site-packages/torch/bin/.hipVersion
```

Aside from that it would be really great if AMD could create a package that holds only the most basic stuff for the gpus (4.4MB):

```
/opt/rocm/amdgcn/bitcode
/opt/amdgpu
```

Here are my Dockerfiles. Please note, that there are no compilers, header files and so on in the pytorch image any longer, so if you need to compile stuff like ctranslate2 for faster-whisper you need to get a little more creative. I managed to do so by creating the rocm image as separate container, that I then can use to copy libraries from it.

This one is the "localhost:5000/tools/rocm:latest" mentioned below:
```
FROM ubuntu:rolling

RUN apt update && apt install -y --no-install-recommends wget                                            \
 && cd /root                                                                                             \
 && wget https://repo.radeon.com/amdgpu-install/6.4.1/ubuntu/jammy/amdgpu-install_6.4.60401-1_all.deb    \
 && apt install -y --no-install-recommends ./amdgpu-install_6.4.60401-1_all.deb                          \
 && amdgpu-install --usecase=rocm --no-dkms -y                                                           \
 && rm /root/amdgpu-install_6.4.60401-1_all.deb

```


This one then is the "localhost:5000/rocm/pytorch:latest":
```
FROM localhost:5000/tools/rocm:latest

RUN mkdir -p /COPY/pytorch/lib/python3.13/site-packages/torch/lib/                                             \
 # copy missing profiles, so that it later can be included correctly from torch
 && cp /opt/rocm-6.4.1/lib/libhsa-amd-aqlprofile64.so /COPY/pytorch/lib/python3.13/site-packages/torch/lib/    \
 # create a softlink, so that the including binaries find the correct file
 && ln -s libhsa-runtime64.so /COPY/pytorch/lib/python3.13/site-packages/torch/lib/libhsa-runtime64.so.1       \
 # copy the missing hipversion file
 && mkdir -p /COPY/pytorch/lib/python3.13/site-packages/torch/bin/                                             \
 && cp /opt/rocm/share/hip/version /COPY/pytorch/lib/python3.13/site-packages/torch/bin/.hipVersion            \
 # now copy the missing files from amdgpu and rocm that are really needed
 && mkdir -p /COPY/opt/rocm/amdgcn                                                                             \
 && cp -R /opt/rocm/amdgcn/bitcode /COPY/opt/rocm/amdgcn/                                                      \
 && cp -R /opt/amdgpu /COPY/opt/


# create the pytorch image
FROM ubuntu:rolling

RUN apt update && apt install -y --no-install-recommends python3-pip python3-venv                              \
 && mkdir /pytorch                                                                                             \
 && python3 -m venv /pytorch/                                                                                  \
 # install torch rocm nightly
 && /pytorch/bin/pip install --no-cache-dir torch torchvision torchaudio                                       \
    --index-url https://download.pytorch.org/whl/nightly/rocm6.4

# install pciutils and torchruntime so that "torchruntime info" and "torchruntime test" work correctly
RUN apt update && apt install -y --no-install-recommends pciutils                                              \
 && /pytorch/bin/pip install --no-cache-dir torchruntime

# delete all gpu profiles that are not needed, mine is the gfx1201, but the gfx1200 is also needed
RUN find /pytorch/lib/ -type f -regextype posix-extended -regex '.*gfx[0-9]+[^/]*\.(dat|co|hsaco)$'            \
        -not -regex '.*gfx120[0-9]+[^/]*\.(dat|co|hsaco)$' -delete                                             \
 # delete triton nvidia libs, this is just wasted space since rocm should be used
 && rm -Rf /pytorch/lib/python3.13/site-packages/triton/backends/nvidia                                        \
 # delete the provided triton libs and instead just link the ones from the torch lib directory
 && cd /pytorch/lib/python3.13/site-packages/triton/backends/amd/lib/                                          \
 && rm libamd_comgr.so               && ln -s ../../../../torch/lib/libamd_comgr.so                            \
 && rm libamdhip64.so                && ln -s ../../../../torch/lib/libamdhip64.so                             \
 && rm libdrm.so                     && ln -s ../../../../torch/lib/libdrm.so                                  \
 && rm libdrm_amdgpu.so              && ln -s ../../../../torch/lib/libdrm_amdgpu.so                           \
 && rm libelf.so                     && ln -s ../../../../torch/lib/libelf.so                                  \
 && rm libhsa-runtime64.so           && ln -s ../../../../torch/lib/libhsa-runtime64.so                        \
 && rm libnuma.so                    && ln -s ../../../../torch/lib/libnuma.so                                 \
 && rm librocprofiler-register.so    && ln -s ../../../../torch/lib/librocprofiler-register.so                 \
 && rm libtinfo.so                   && ln -s ../../../../torch/lib/libtinfo.so                                \
 # cleanup apt and cache
 && rm -Rf /var/cache/*                                                                                        \
 && rm -Rf /var/lib/apt/lists/*.lz4                                                                            \
 && rm -Rf /var/log/apt/


# create the real image, that will hold only the needed parts of rocm and pytorch
FROM scratch

ENV TZ=UTC

# COPY everything from the pytorch image into one clean layer
COPY --from=1 / /

# copy all the needed stuff from the rocm image into one layer
COPY --from=0 /COPY/ /

```
If you have any questions feel free to ask, I will try to come back to you as soon as possible.

---

### 评论 #25 — fxmarty-amd (2025-07-25T11:48:25Z)

if useful to anybody: `rocm/pytorch:rocm6.4.1_ubuntu24.04_py3.12_pytorch_release_2.7.1` is 66GB, with compressed size 23.55 GB.

Targeting only gfx942 and removing bloat, we can easily reduce it to ~28.2 GB uncompressed / 8.45 GB compressed (https://gist.github.com/fxmarty-amd/ea7e7703d1ac85119ab5ed3e4c33451e), which is still too large, but at least it makes it easier to pull in e.g. a kubernetes cluster.

----

I found out that some LLVM objects `libLLVM*.a` are duplicate, but have different sha in different locations:

```
(py_3.12) root@xcomx300-1:/# find . -iname "*libLLVMscalar*"
./opt/rocm-6.4.0/lib/llvm/lib/libLLVMScalarOpts.a
./opt/llvm/lib/libLLVMScalarOpts.a
./opt/conda/envs/py_3.12/lib/libLLVMScalarOpts.a

(py_3.12) root@xcomx300-1:/# sha256sum /opt/rocm-6.4.0/lib/llvm/lib/libLLVMScalarOpts.a
ba8d08456a472016139a51db350b00f6c58e2a3c5cf5ab1d5a17bb5c2435f655  ./opt/rocm-6.4.0/lib/llvm/lib/libLLVMScalarOpts.a
(py_3.12) root@xcomx300-1:/# sha256sum /opt/llvm/lib/libLLVMScalarOpts.a
77b0e3d183fdbf95e9aa8ee37b43a965b8c416f94e14f4082369ab7d0dfc38f6  ./opt/llvm/lib/libLLVMScalarOpts.a
(py_3.12) root@xcomx300-1:/# sha256sum /opt/conda/envs/py_3.12/lib/libLLVMScalarOpts.a
c42984a38131b92c8224c9b3632abb9f9b2ec8720da29ab5368a1d31371aee6f  ./opt/conda/envs/py_3.12/lib/libLLVMScalarOpts.a
```

There are 146 of them in `/opt/conda/envs/py_3.12/lib/`, 108 of them in `/opt/rocm-6.4.0/lib/llvm/lib/`, 64 of them in `/opt/llvm/lib/`.

Not sure whether these are safe to deduplicate.


-----

There is also a lot of bloat from `/opt/conda/envs/py_3.12/lib/libmkl_*.so` which is maybe not safe to remove if one is using an Intel CPU?

-----

I also had good luck so far using `rdfind` to remove duplicate files and replace them with symlinks, although some ROCm files share the same hash although they are arguably different (https://github.com/ROCm/ROCm/issues/5054), and get deduplicated, resulting in later issues when building libraries.

Eventually, I guess one would probably need to build ROCm /pytorch from scratch to target a single architecture to reduce `/opt/rocm` size as suggested above and in https://github.com/ROCm/ROCm-docker/issues/120#issuecomment-2016647700.

I was also pointed out to https://github.com/ROCm/TheRock/blob/main/RELEASES.md where there seems to be efforts to build ROCm for single arch, but this looks WIP.

---

### 评论 #26 — mike-callahan (2025-10-17T17:36:00Z)

I realized if you are fine having the drivers and libs on the nodes themselves, you can just bind mount /opt/amd in your container bypassing almost all of the storage usage.

---
