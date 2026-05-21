# MI100 initiallization issue on AM4 hardware

> **Issue #2927**
> **状态**: closed
> **创建时间**: 2024-02-25T17:17:57Z
> **更新时间**: 2024-10-01T17:05:38Z
> **关闭时间**: 2024-10-01T17:05:38Z
> **作者**: briansp2020
> **标签**: ROCm 6.0.0, AMD Instinct MI100
> **URL**: https://github.com/ROCm/ROCm/issues/2927

## 标签

- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Instinct MI100** (颜色: #ededed)

## 描述

### Problem Description

MI100 fails to initialize and nothing works. I found the following error messages. The hardware works as expected in my AM5 setup. So, it's something about MB/CPU/BIOS set up that is incompatible. I found the [following post](https://forum.level1techs.com/t/amd-mi100-not-being-recognized/204303/2) and made sure to disable CSM and to enable Re-Bar & Above 4G address decoding. dmesg says probe failed with error -12. Is there anything else I can try? What does error -12 mean? 

>$ sudo dmesg | grep amd
[    0.000000] Linux version 5.15.0-97-generic (buildd@lcy02-amd64-033) (gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #107-Ubuntu SMP Wed Feb 7 13:26:48 UTC 2024 (Ubuntu 5.15.0-97.107-generic 5.15.136)
[    0.572509] perf/amd_iommu: Detected AMD IOMMU #0 (2 banks, 4 counters/bank).
[    6.476797] amdkcl: loading out-of-tree module taints kernel.
[    6.476835] amdkcl: module verification failed: signature and/or required key missing - tainting kernel
[    6.556702] amdkcl: Warning: fail to get symbol __cancel_work, replace it with kcl stub
[    6.756137] [drm] amdgpu kernel modesetting enabled.
[    6.756144] [drm] amdgpu version: 6.3.6
[    6.761824] amdgpu: Virtual CRAT table created for CPU
[    6.761833] amdgpu: Topology: Add CPU node
[    6.770241] amdgpu: PeerDirect support was initialized successfully
[    6.770337] amdgpu 0000:09:00.0: enabling device (0000 -> 0003)
[    6.770371] amdgpu 0000:09:00.0: amdgpu: Fatal error during GPU init
[    6.770386] amdgpu: probe of 0000:09:00.0 failed with error -12
[    6.770390] amdgpu: legacy kernel without apple_gmux_detect()

Hardware:
Gigabyte B550I-AORUS-PRO-AX-rev-11, Latest BIOS (F18d), Ryzen 3900X, 32 GB RAM.


### Operating System

22.04.4 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 9 3900X 12-Core Processor

### GPU

AMD Instinct MI100

### ROCm Version

ROCm 6.0.0

### ROCm Component

rocminfo

### Steps to Reproduce

Just plug in the card and boot it up.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

$ /opt/rocm/bin/rocminfo --support
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 9 3900X 12-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 9 3900X 12-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   3800
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            24
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32754184(0x1f3ca08) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32754184(0x1f3ca08) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32754184(0x1f3ca08) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***

### Additional Information

_No response_

---

## 评论 (23 条)

### 评论 #1 — nartmada (2024-02-25T21:08:19Z)

Hi @briansp2020, I will ask one of my developers to check tomorrow.  In the meantime, do you want to give a quick try with ROCm 6.0.2?  Thanks.

---

### 评论 #2 — briansp2020 (2024-02-25T23:25:14Z)

I'm already using 6.0.2. The AM4 setup works fine with 9700XTX. Kernel version is 5.15 because it is Ubuntu Server version. I just realized that AM5 setup is Ubuntu desktop so it has kernel version 6.2. Do you think upgrading kernel version would make a difference?


---

### 评论 #3 — kentrussell (2024-02-26T15:23:36Z)

So -12 is ENOMEM, so something during init is saying that there's unsufficient memory. Can you attach a full, non-grepped dmesg for us to take a look a what's happening before and during init? Thanks

---

### 评论 #4 — briansp2020 (2024-02-26T16:39:16Z)

full dmesg output at https://gist.github.com/briansp2020/0e0c842b085f87cf05ada7f6834871f8

Thank you!

---

### 评论 #5 — kentrussell (2024-02-26T17:36:08Z)

Thanks, I've seen similar things before with different root causes. Can I get a couple more things? 
1: Is your SBIOS up to date?
2: If you blacklist amdgpu (modprobe.blacklist=amdgpu in the kernel params) and then modprobe amdgpu after, does it throw the same error?
3: How much RAM is available on the system? If you run free before the modprobe, how much does it report is available?
4: Lastly, do you know if the VBIOS has been updated or changed, or if it's still the same original one? Thanks!

---

### 评论 #6 — briansp2020 (2024-02-26T18:06:56Z)

1: Is your SBIOS up to date?
>  Yes. I'm running F18d which was released on Dec 25, 2023 (https://www.gigabyte.com/Motherboard/B550I-AORUS-PRO-AX-11/support#support-dl-bios)

2: If you blacklist amdgpu (modprobe.blacklist=amdgpu in the kernel params) and then modprobe amdgpu after, does it throw the same error?
>  I get the same error.

3: How much RAM is available on the system?
>   32GB

   If you run free before the modprobe, how much does it report is available?
> $ free
               total        used        free      shared  buff/cache   available
Mem:        32754200      532304    31558304        2968      663592    31818992
Swap:        8388604           0     8388604

4: Lastly, do you know if the VBIOS has been updated or changed, or if it's still the same original one?
>  I don't know. I bought it off ebay a few month ago. How do I find out VBIOS version?

---

### 评论 #7 — kentrussell (2024-02-26T18:47:46Z)

Buying it off of eBay isn't a great start, as it could've been broken before you received it. That also means you won't have the VBIOS info on you, since you didn't get it from a HW partner. The fact that it can't even read the VBIOS means that it's failing almost immediately. Specifically it's failing here at the ioremap call:
        for (i = 0; i < AMD_IP_BLOCK_TYPE_NUM; i++)
                atomic_set(&adev->pm.pwr_state[i], POWER_STATE_UNKNOWN);

        adev->rmmio = ioremap(adev->rmmio_base, adev->rmmio_size);
        if (!adev->rmmio)
                return -ENOMEM;

, which is the remapping of device address to virtual address space. A VBIOS update would help, but it's difficult to do if the system can't post the GPU successfully. AMD doesn't officially support doing that "in the wild" for MI cards, but if you use your favourite search engine, you will likely find references to tools called amdvbflash and the back of the GPU will have a part number on it, which can help you to find some random 3rd party that posts that specific VBIOS. Again, officially AMD can't help in that case, but people have found things like https://support.hpe.com/connect/s/softwaredetails?language=en_US&softwareId=MTX_b58c883eb17949dfbcc26f0560 that may work if your model is a D34315. 

Officially (and primarily), I'd see if you can return the card. Unless this is a new occurrence with a newer ROCm (unlikely based on the symptoms), I'd look into returning the GPU and trying to get another one. All signs here point to a bad VBIOS flash (or a broken card, or both). And with it being bought from a 3rd party vendor, AMD doesn't have any official support for that. If you can't return it, then you may as well try whatever you can to get it to work, including links like the one above. Good luck!

---

### 评论 #8 — briansp2020 (2024-02-26T19:21:27Z)

There is a sticker that says D34314. How is it different from D34315? 
The card works in my AM5 machine. So, if you suspect that it is VBIOS, I can plug it in to my AM5 machine try to update the VBIOS. Do you happen to know where I can find VBIOS for D34314?

I'm sure the seller won't take it back. Any help would be appreciated.

Thank you!

---

### 评论 #9 — kentrussell (2024-02-26T19:43:41Z)

Each SKU has its own part number, so do you know if it's a D3431400 or D3431401 ? That denotes the revision, and each has its own VBIOS.

---

### 评论 #10 — briansp2020 (2024-02-26T20:48:03Z)

Full part number is 102D3431400 00000 1
SN 692108000055

---

### 评论 #11 — briansp2020 (2024-02-26T21:00:47Z)

![Screenshot 2024-02-26 130001](https://github.com/ROCm/ROCm/assets/3746601/5993187f-a95b-4d54-ac8f-0c50ac57ca2d)


---

### 评论 #12 — visionscaper (2024-03-28T13:23:24Z)

@briansp2020 Was this ever resolved? I have the same issues, same AMD MI100, same error code -12,512GB RAM. But, it did work before. I changed it to another PCIe slot, that's when the issue started. I'm afraid I broke it.

Anyone have any new suggestions?

---

### 评论 #13 — visionscaper (2024-03-28T13:24:28Z)

Can it be related memory encryption somehow?

---

### 评论 #14 — briansp2020 (2024-03-28T13:58:03Z)

@visionscaper 
No. My MI100 seems completely broken now. OS locks up while booting if I have the MI100 installed. The OS boots up fine if I remove the card. I guess the hardware was on its last leg when it was showing weird symptoms...


---

### 评论 #15 — visionscaper (2024-03-28T21:44:17Z)

Hi @briansp2020, sorry to hear that. In my case, and this is hot from the press, after trying since yesterday, I got the GPU back to work again! 

Searching for clues about what could cause a `amdgpu: probe of 0000:09:00.0 failed with error -12`, I came a cross a few hints. In some case people talked about enabling/disabling "SR-IOV". Further, I noticed in my boot messages, I had multiple messages saying `BAR X: no space for [mem size Y 64bit]`:

```
...
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:22:00.0: PCI bridge to [bus 23]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:22:00.0:   bridge window [mem 0xf0a00000-0xf0afffff]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:22:01.0: PCI bridge to [bus 24]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:22:01.0:   bridge window [mem 0xf0900000-0xf09fffff]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:25:00.0: BAR 7: no space for [mem size 0x00100000 64bit]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:25:00.0: BAR 7: failed to assign [mem size 0x00100000 64bit]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:25:00.0: BAR 10: no space for [mem size 0x00100000 64bit]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:25:00.0: BAR 10: failed to assign [mem size 0x00100000 64bit]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:25:00.1: BAR 7: no space for [mem size 0x00100000 64bit]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:25:00.1: BAR 7: failed to assign [mem size 0x00100000 64bit]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:25:00.1: BAR 10: no space for [mem size 0x00100000 64bit]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:25:00.1: BAR 10: failed to assign [mem size 0x00100000 64bit]
Mar 28 20:06:23 deep-visionscaper3 kernel: pci 0000:22:02.0: PCI bridge to [bus 25]
...
```

This could have been why the driver didn't pick up on the GPU.

So, with this background I came across [this post](https://forums.unraid.net/topic/132930-drives-and-usb-devices-visible-in-bios-not-available-once-booted-asus-wrx80-sage-5965wx/?do=findComment&comment=1208168), mentioning the same `error -12` issues, and talked about setting the following in the BIOS:
```
Re-Size BAR Support - AUTO (Was disabled)
SR-IOV Support - ENABLED (Was disabled)
```
This rang a bell with me and, luckily, I also have a ASUS WRX80 SAGE motherboard like in the  post, so I could change these settings too in the BIOS.

Eventually, although I think that setting `Re-Size BAR Support` to `AUTO` made it work, I'm not sure which of the two settings fixed the issue (or maybe both were required).

As you can read this low-level system/kernel stuff is not my expertise, so I would be interested if anyone can shed some more light on this.
 

---

### 评论 #16 — kentrussell (2024-04-01T14:09:55Z)

So the SRIOV part will only really make a difference if you're running Virtualization. I think that the resize BAR support is where we're looking. For all of our GPUs, the BAR size is basically how much VRAM the CPU can access at a single time. The default is usually pretty low, but resizable BARs is a way to allow more access in fewer reads. For MI*, we prefer larger BARs as this will significantly reduce a lot of CPU-to-GPU bottlenecks on large memory accesses (like we get with Compute workloads). 

I'm glad to see it's working here, though! I am less fluent in the PCI driver, which is where the "no space" messages arise, but the error comes from this scheck:

        size = resource_size(res);
        ret = _pci_assign_resource(dev, resno, size, align);

        /*
         * If we failed to assign anything, let's try the address
         * where firmware left it.  That at least has a chance of
         * working, which is better than just leaving it disabled.
         */
        if (ret < 0) {
                pci_info(dev, "BAR %d: no space for %pR\n", resno, res);
                ret = pci_revert_fw_address(res, dev, resno, size);
        }

        if (ret < 0) {
                pci_info(dev, "BAR %d: failed to assign %pR\n", resno, res);
                return ret;
        }

So it looks like the PCI resource couldn't be assigned, so it just fails the device. And since we need the PCI driver support, we just fail out. I'll see if we can try to add a little more verbose logging into the driver to make it a little more obvious where this failure is coming from, but at least we're working, which is a huge improvement! 

And lastly, sorry for not suggesting that before. You had mentioned in your first post about ensuring to enable "above 4G encoding" and "enable Re-bar" which I interpreted as "enable resizable BAR" . Regardless, I should've verified those settings, but at least we got past it!

---

### 评论 #17 — visionscaper (2024-04-01T22:27:54Z)

Hi @kentrussell, thanks for your answer. After my previous post, I did get the  `amdgpu: probe of XYZ failed with error -12` and `BAR X: no space for [mem size Y 64bit]` a few more times. However, I found out that (and now it gets a bit esoteric, please bear with me) the issues went away when I kept a Nvidia GPU, which I used as a display driver, at PCIe slot 1. I don't think this has anything to do with that it is a Nvidia brand GPU, but that for some reason the motherboard and/or OS was expecting it to be there, in slot 1. If I removed it, the issues would come back! Also, when I try to put it in other slot, the same issues would appear.

With this strange behaviour in mind, I'm wondering, can it somehow be that having this Nvidia GPU at PCIe slot 1 is somehow "hardwired" in the (Ubuntu) OS or PCI driver settings when I installed the OS or driver? I think this should never be the case, but it seems like the BAR error messages occur because connected PCI devices appear to want to register certain memory areas, while this has already been registered by other PCI devices. But when having the Nvidia at slot 1 all registrations fall in to place ... With this logic, I'm wondering if reinstalling the OS would make this behaviour go away.

It could very well be this doesn't make much sense, but I'm struggling to understand this behaviour. What are your thoughts on the potential reasons for this occur?

---

### 评论 #18 — kentrussell (2024-04-02T13:24:15Z)

I'm wondering less about nVidia in slot1 and more about wondering if it's about having a graphics card in slot1. The MI doesn't have graphics, so I wonder if having a display card in general (AMD/ATI, Aspeed, etc) would also trigger the same situation. But I also only see 1 slot on the MB specs (https://www.gigabyte-data.com/products/page/mb/B550I-AORUS-PRO-AX-rev-11/kf). Are you using a riser? Or did I just find the wrong model?

In general, the OS shouldn't be "hardcoding" anything, but it could be a quirk with nvidia+AMD on that board, or graphics+compute. Or if you're using a riser/bridge, that could also be causing some issues. 


---

### 评论 #19 — visionscaper (2024-04-02T19:42:13Z)

Hi @kentrussell, I'm using an [Asus Pro WS WRX80E-SAGE SE WIFI II ](https://www.asus.com/motherboards-components/motherboards/workstation/pro-ws-wrx80e-sage-se-wifi-ii/) as motherboard, the other Gigabyte motherboard was mentioned by @briansp2020, who started this issue.

I am using risers, and I'm seeing (not too frequent) (correctable) issues that I think relate to using these:
```
...
kernel: [ 2478.486780] pcieport 0000:00:01.1: AER: aer_layer=Data Link Layer, aer_agent=Receiver ID
kernel: [ 2484.374025] {359}[Hardware Error]: Hardware error from APEI Generic Hardware Error Source: 512
kernel: [ 2484.374028] {359}[Hardware Error]: It has been corrected by h/w and requires no further action
kernel: [ 2484.374029] {359}[Hardware Error]: event severity: corrected
kernel: [ 2484.374030] {359}[Hardware Error]:  Error 0, type: corrected
kernel: [ 2484.374031] {359}[Hardware Error]:   section_type: PCIe error
kernel: [ 2484.374031] {359}[Hardware Error]:   port_type: 4, root port
kernel: [ 2484.374031] {359}[Hardware Error]:   version: 0.2
kernel: [ 2484.374032] {359}[Hardware Error]:   command: 0x0407, status: 0x0010
kernel: [ 2484.374033] {359}[Hardware Error]:   device_id: 0000:20:03.1
kernel: [ 2484.374033] {359}[Hardware Error]:   slot: 0
kernel: [ 2484.374034] {359}[Hardware Error]:   secondary_bus: 0x2d
kernel: [ 2484.374034] {359}[Hardware Error]:   vendor_id: 0x1022, device_id: 0x1483
kernel: [ 2484.374035] {359}[Hardware Error]:   class_code: 060400
kernel: [ 2484.374035] {359}[Hardware Error]:   bridge: secondary_status: 0x0000, control: 0x0012
kernel: [ 2484.374036] {359}[Hardware Error]:  Error 1, type: corrected
kernel: [ 2484.374036] {359}[Hardware Error]:   section_type: PCIe error
kernel: [ 2484.374037] {359}[Hardware Error]:   port_type: 4, root port
kernel: [ 2484.374037] {359}[Hardware Error]:   version: 0.2
kernel: [ 2484.374037] {359}[Hardware Error]:   command: 0x0407, status: 0x0010
kernel: [ 2484.374038] {359}[Hardware Error]:   device_id: 0000:00:01.1
kernel: [ 2484.374038] {359}[Hardware Error]:   slot: 0
kernel: [ 2484.374039] {359}[Hardware Error]:   secondary_bus: 0x01
kernel: [ 2484.374039] {359}[Hardware Error]:   vendor_id: 0x1022, device_id: 0x1483
kernel: [ 2484.374039] {359}[Hardware Error]:   class_code: 060400
kernel: [ 2484.374040] {359}[Hardware Error]:   bridge: secondary_status: 0x0000, control: 0x0012
kernel: [ 2484.374040] {359}[Hardware Error]:  Error 2, type: corrected
kernel: [ 2484.374040] {359}[Hardware Error]:   section_type: PCIe error
kernel: [ 2484.374041] {359}[Hardware Error]:   port_type: 4, root port
kernel: [ 2484.374041] {359}[Hardware Error]:   version: 0.2
kernel: [ 2484.374041] {359}[Hardware Error]:   command: 0x0407, status: 0x0010
kernel: [ 2484.374042] {359}[Hardware Error]:   device_id: 0000:00:01.1
kernel: [ 2484.374042] {359}[Hardware Error]:   slot: 0
kernel: [ 2484.374042] {359}[Hardware Error]:   secondary_bus: 0x01
kernel: [ 2484.374043] {359}[Hardware Error]:   vendor_id: 0x1022, device_id: 0x1483
kernel: [ 2484.374043] {359}[Hardware Error]:   class_code: 060400
kernel: [ 2484.374043] {359}[Hardware Error]:   bridge: secondary_status: 0x0000, control: 0x0012
kernel: [ 2484.374044] {359}[Hardware Error]:  Error 3, type: corrected
kernel: [ 2484.374044] {359}[Hardware Error]:   section_type: PCIe error
kernel: [ 2484.374044] {359}[Hardware Error]:   port_type: 4, root port
kernel: [ 2484.374045] {359}[Hardware Error]:   version: 0.2
kernel: [ 2484.374045] {359}[Hardware Error]:   command: 0x0407, status: 0x0010
kernel: [ 2484.374045] {359}[Hardware Error]:   device_id: 0000:00:01.1
kernel: [ 2484.374046] {359}[Hardware Error]:   slot: 0
kernel: [ 2484.374046] {359}[Hardware Error]:   secondary_bus: 0x01
kernel: [ 2484.374046] {359}[Hardware Error]:   vendor_id: 0x1022, device_id: 0x1483
kernel: [ 2484.374047] {359}[Hardware Error]:   class_code: 060400
kernel: [ 2484.374047] {359}[Hardware Error]:   bridge: secondary_status: 0x0000, control: 0x0012
kernel: [ 2484.374048] {359}[Hardware Error]:  Error 4, type: corrected
kernel: [ 2484.374048] {359}[Hardware Error]:   section_type: PCIe error
kernel: [ 2484.374048] {359}[Hardware Error]:   port_type: 4, root port
kernel: [ 2484.374048] {359}[Hardware Error]:   version: 0.2
kernel: [ 2484.374049] {359}[Hardware Error]:   command: 0x0407, status: 0x0010
kernel: [ 2484.374049] {359}[Hardware Error]:   device_id: 0000:00:01.1
kernel: [ 2484.374050] {359}[Hardware Error]:   slot: 0
kernel: [ 2484.374050] {359}[Hardware Error]:   secondary_bus: 0x01
kernel: [ 2484.374050] {359}[Hardware Error]:   vendor_id: 0x1022, device_id: 0x1483
kernel: [ 2484.374050] {359}[Hardware Error]:   class_code: 060400
kernel: [ 2484.374051] {359}[Hardware Error]:   bridge: secondary_status: 0x0000, control: 0x0012
kernel: [ 2484.374051] {359}[Hardware Error]:  Error 5, type: corrected
kernel: [ 2484.374052] {359}[Hardware Error]:   section_type: PCIe error
kernel: [ 2484.374052] {359}[Hardware Error]:   port_type: 4, root port
kernel: [ 2484.374052] {359}[Hardware Error]:   version: 0.2
kernel: [ 2484.374052] {359}[Hardware Error]:   command: 0x0407, status: 0x0010
kernel: [ 2484.374053] {359}[Hardware Error]:   device_id: 0000:00:01.1
kernel: [ 2484.374053] {359}[Hardware Error]:   slot: 0
kernel: [ 2484.374054] {359}[Hardware Error]:   secondary_bus: 0x01
kernel: [ 2484.374054] {359}[Hardware Error]:   vendor_id: 0x1022, device_id: 0x1483
kernel: [ 2484.374054] {359}[Hardware Error]:   class_code: 060400
kernel: [ 2484.374055] {359}[Hardware Error]:   bridge: secondary_status: 0x0000, control: 0x0012
kernel: [ 2484.374055] {359}[Hardware Error]:  Error 6, type: corrected
kernel: [ 2484.374055] {359}[Hardware Error]:   section_type: PCIe error
kernel: [ 2484.374055] {359}[Hardware Error]:   port_type: 4, root port
kernel: [ 2484.374056] {359}[Hardware Error]:   version: 0.2
kernel: [ 2484.374056] {359}[Hardware Error]:   command: 0x0407, status: 0x0010
kernel: [ 2484.374056] {359}[Hardware Error]:   device_id: 0000:00:01.1
kernel: [ 2484.374057] {359}[Hardware Error]:   slot: 0
kernel: [ 2484.374057] {359}[Hardware Error]:   secondary_bus: 0x01
kernel: [ 2484.374057] {359}[Hardware Error]:   vendor_id: 0x1022, device_id: 0x1483
kernel: [ 2484.374058] {359}[Hardware Error]:   class_code: 060400
kernel: [ 2484.374058] {359}[Hardware Error]:   bridge: secondary_status: 0x0000, control: 0x0012
kernel: [ 2484.374058] {359}[Hardware Error]:  Error 7, type: corrected
kernel: [ 2484.374059] {359}[Hardware Error]:   section_type: PCIe error
kernel: [ 2484.374059] {359}[Hardware Error]:   port_type: 4, root port
kernel: [ 2484.374059] {359}[Hardware Error]:   version: 0.2
kernel: [ 2484.374060] {359}[Hardware Error]:   command: 0x0407, status: 0x0010
kernel: [ 2484.374060] {359}[Hardware Error]:   device_id: 0000:00:01.1
kernel: [ 2484.374061] {359}[Hardware Error]:   slot: 0
kernel: [ 2484.374061] {359}[Hardware Error]:   secondary_bus: 0x01
kernel: [ 2484.374061] {359}[Hardware Error]:   vendor_id: 0x1022, device_id: 0x1483
kernel: [ 2484.374061] {359}[Hardware Error]:   class_code: 060400
kernel: [ 2484.374062] {359}[Hardware Error]:   bridge: secondary_status: 0x0000, control: 0x0012
...
```

The errors come from these PCI bridges
```
$ lspci | grep 20:03.1
20:03.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
$ lspci | grep 00:01.1
00:01.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
```

Which, not surprisingly, are connected to the MI100's:
```
$ lspci -tv
-+-[0000:60]-+-00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
 |           +-00.2  Advanced Micro Devices, Inc. [AMD] Milan IOMMU
 |           +-01.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-02.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-03.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-04.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-05.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-07.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-07.1-[61]----00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
 |           +-08.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           \-08.1-[62]----00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
 +-[0000:40]-+-00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
 |           +-00.2  Advanced Micro Devices, Inc. [AMD] Milan IOMMU
 |           +-01.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-01.1-[41]--+-00.0  NVIDIA Corporation GK104 [GeForce GTX 680]
 |           |            \-00.1  NVIDIA Corporation GK104 HDMI Audio Controller
 |           +-02.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-03.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-04.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-05.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-07.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-07.1-[42]----00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
 |           +-08.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           \-08.1-[43]----00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
 +-[0000:20]-+-00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
 |           +-00.2  Advanced Micro Devices, Inc. [AMD] Milan IOMMU
 |           +-01.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-01.1-[21-2a]----00.0-[22-2a]--+-00.0-[23]----00.0  Micron/Crucial Technology Device 5419
 |           |                               +-01.0-[24]----00.0  ASMedia Technology Inc. ASM3242 USB 3.2 Host Controller
 |           |                               +-02.0-[25-26]--+-00.0  Intel Corporation Ethernet Controller 10G X550T
 |           |                               |               \-00.1  Intel Corporation Ethernet Controller 10G X550T
 |           |                               +-03.0-[27]----00.0  Intel Corporation Wi-Fi 6 AX210/AX211/AX411 160MHz
 |           |                               +-04.0-[28]----00.0  ASMedia Technology Inc. ASM1062 Serial ATA Controller
 |           |                               +-05.0-[29]----00.0  ASMedia Technology Inc. ASM1062 Serial ATA Controller
 |           |                               \-08.0-[2a]--+-00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
 |           |                                            +-00.1  Advanced Micro Devices, Inc. [AMD] Matisse USB 3.0 Host Controller
 |           |                                            \-00.3  Advanced Micro Devices, Inc. [AMD] Matisse USB 3.0 Host Controller
 |           +-01.2-[2b]----00.0  Micron/Crucial Technology Device 5419
 |           +-01.3-[2c]----00.0  Micron/Crucial Technology Device 5419
 |           +-02.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-03.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-03.1-[2d-2f]----00.0-[2e-2f]----00.0-[2f]----00.0  Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [Instinct MI100]
 |           +-04.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-05.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-07.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           +-07.1-[30]----00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
 |           +-08.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
 |           \-08.1-[31]--+-00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
 |                        +-00.1  Advanced Micro Devices, Inc. [AMD] Starship/Matisse Cryptographic Coprocessor PSPCPP
 |                        +-00.3  Advanced Micro Devices, Inc. [AMD] Starship USB 3.0 Host Controller
 |                        \-00.4  Advanced Micro Devices, Inc. [AMD] Starship/Matisse HD Audio Controller
 \-[0000:00]-+-00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
             +-00.2  Advanced Micro Devices, Inc. [AMD] Milan IOMMU
             +-01.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
             +-01.1-[01-03]----00.0-[02-03]----00.0-[03]----00.0  Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [Instinct MI100]
             +-02.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
             +-03.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
             +-04.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
             +-05.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
             +-07.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
             +-07.1-[04]----00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
             +-08.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
             +-08.1-[05]--+-00.0  Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
             |            \-00.3  Advanced Micro Devices, Inc. [AMD] Starship USB 3.0 Host Controller
             +-14.0  Advanced Micro Devices, Inc. [AMD] FCH SMBus Controller
             +-14.3  Advanced Micro Devices, Inc. [AMD] FCH LPC Bridge
             +-18.0  Advanced Micro Devices, Inc. [AMD] Milan Data Fabric; Function 0
             +-18.1  Advanced Micro Devices, Inc. [AMD] Milan Data Fabric; Function 1
             +-18.2  Advanced Micro Devices, Inc. [AMD] Milan Data Fabric; Function 2
             +-18.3  Advanced Micro Devices, Inc. [AMD] Milan Data Fabric; Function 3
             +-18.4  Advanced Micro Devices, Inc. [AMD] Milan Data Fabric; Function 4
             +-18.5  Advanced Micro Devices, Inc. [AMD] Milan Data Fabric; Function 5
             +-18.6  Advanced Micro Devices, Inc. [AMD] Milan Data Fabric; Function 6
             \-18.7  Advanced Micro Devices, Inc. [AMD] Milan Data Fabric; Function 7
```
~^ In the above config I did not have the Nvidia card installed.~

But the following remains true:

1. Without the Nvidia card installed at all, one of the two MI100's is not registered (with `BAR X: no space for [mem size Y 64bit]` errors)
2. With the Nvidia card in slot 7, one of the two MI100's is not registered and the display is not working (with `BAR X: no space for [mem size Y 64bit]` errors)
3. With the Nvidia card in slot 1, both MI100's are registered and the display is working (No `BAR` issues)

In config 3. everything is stable, I have successfully performed PyTorch distributed training in this config.

I think it's quite puzzling, but the current config is stable, so this is the way forward I guess; going to add 4 more MI100 cards later this week, to finish my 6x MI100 machine.

---

### 评论 #20 — kentrussell (2024-04-02T19:48:50Z)

Ah sorry, I skipped over the usernames there when I scrolled up. I know we had some funkiness with risers before, I'll see if I can dig that out. 

---

### 评论 #21 — visionscaper (2024-04-02T20:12:14Z)

Awesome, thanks.

---

### 评论 #22 — kentrussell (2024-04-09T13:42:33Z)

Sorry for the delay, I've been trying to talk to a few people about this internally. Do you have the model of riser onhand? And do you see any Correctable Errors when you just use a single MI100 without the riser? Just trying to make sure it's aligned with what I am talking about with the guys here . Thanks!

---

### 评论 #23 — ppanchad-amd (2024-10-01T17:05:38Z)

@briansp2020 Closing ticket as this appears to be a hardware issue and not ROCm. Thanks!

---
