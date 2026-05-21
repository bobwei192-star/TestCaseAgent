# MI100 memory Operating points

> **Issue #2844**
> **状态**: closed
> **创建时间**: 2024-01-26T23:44:59Z
> **更新时间**: 2024-02-13T22:50:02Z
> **关闭时间**: 2024-02-13T22:50:02Z
> **作者**: IMbackK
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2844

## 描述

sorry if this is an inappropriate place for this question. I have a couple of MI100s in a server, but they idle terribly, it would appear that they have no lower vram operating power level than full speed, see:

```

# cat /sys/class/drm/card2/device/pp_dpm_mclk 
0: 1200Mhz *
```

I was wondering if you guys have access to a newer vbios that potentially includes more power levels as idle consumption like this is fairly unreasonable. Below for reference amdvbflash output:

```
adapter seg  bn dn dID       asic           flash      romsize test    bios p/n   
======= ==== == == ==== =============== ============== ======= ==== ================
  0    0000 03 00 738C MI100(Slave)    GD25Q80C        100000 pass 113-D3431401-100
```

Thank you very much for any help you can provide and i apologize for the intrusion.

---

## 评论 (3 条)

### 评论 #1 — nartmada (2024-02-01T17:10:09Z)

Hi @IMbackK, can you please reach out to your HW vendor for the newer VBIOS?  Thanks.

---

### 评论 #2 — IMbackK (2024-02-01T19:43:24Z)

Hi @nartmada unfortunately we cobbled this machine together from parts so there is'ent really a vendor point of contact for it.

---

### 评论 #3 — nartmada (2024-02-13T22:50:02Z)

I am sorry @IMbackK.  We cannot distribute the VBIOS arbitrarily, and VBIOS update must go thru the HW vendor.

---
