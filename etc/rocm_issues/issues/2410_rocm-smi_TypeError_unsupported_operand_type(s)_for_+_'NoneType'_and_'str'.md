# rocm-smi TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'

> **Issue #2410**
> **状态**: closed
> **创建时间**: 2023-08-28T15:01:02Z
> **更新时间**: 2024-03-22T23:25:32Z
> **关闭时间**: 2024-03-22T23:25:32Z
> **作者**: grigio
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2410

## 描述

I'm using your dev rocm container with `ubuntu:22:04`

```
rocm-smi -a


========================= ROCm System Management Interface =========================
=========================== Version of System Component ============================
Driver version: 6.1.5
====================================================================================
======================================== ID ========================================
GPU[0]		: GPU ID: 0x164e
====================================================================================
==================================== Unique ID =====================================
GPU[0]		: Unique ID: N/A
====================================================================================
====================================== VBIOS =======================================
GPU[0]		: VBIOS version: 102-RAPHAEL-008
====================================================================================
=================================== Temperature ====================================
GPU[0]		: Temperature (Sensor edge) (C): 47.0
====================================================================================
============================ Current clock frequencies =============================
GPU[0]		: mclk clock level: 0: (2600Mhz)
GPU[0]		: sclk clock level: 1: (600Mhz)
GPU[0]		: socclk clock level: 1: (1200Mhz)
====================================================================================
================================ Current Fan Metric ================================
GPU[0]		: Unable to detect fan speed for GPU 0
====================================================================================
============================== Show Performance Level ==============================
GPU[0]		: Performance Level: auto
====================================================================================
================================= OverDrive Level ==================================
GPU[0]		: GPU OverDrive value (%): 0
====================================================================================
================================= OverDrive Level ==================================
GPU[0]		: GPU Memory OverDrive value (%): 0
====================================================================================
==================================== Power Cap =====================================
GPU[0]		: get_power_cap, Not supported on the given system
GPU[0]		: Max Graphics Package Power Unsupported
====================================================================================
=============================== Show Power Profiles ================================
GPU[0]		: get_power_profiles, Not supported on the given system
====================================================================================
================================ Power Consumption =================================
Traceback (most recent call last):
  File "/usr/bin/rocm-smi", line 3586, in <module>
    showPower(deviceList)
  File "/usr/bin/rocm-smi", line 2190, in showPower
    if checkIfSecondaryDie(device):
  File "/usr/bin/rocm-smi", line 715, in checkIfSecondaryDie
    if not (rsmi_ret_ok(ret, None, None, False) and power_cap.value == 0):
  File "/usr/bin/rocm-smi", line 3227, in rsmi_ret_ok
    printLog(device, metric + ", " + rsmi_status_verbose_err_out[my_ret], None)
TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'

```

```
rocm_agent_enumerator -a
gfx000
gfx1036

```

---

## 评论 (6 条)

### 评论 #1 — nartmada (2024-03-16T02:13:49Z)

Hi @grigio, apologies for the lack of response.  Do you still observe this issue with latest ROCm 6.0.2?

---

### 评论 #2 — grigio (2024-03-16T08:27:15Z)

i didn't try because the software i use still depends on rocm 5.7

---

### 评论 #3 — nartmada (2024-03-22T16:08:27Z)

Hi @grigio, which GPU are you using?  What is your system config?  We can try to repro your issue with ROCm 5.7 and 6.0.2 on our side.  Thanks.

---

### 评论 #4 — grigio (2024-03-22T18:09:30Z)

> Hi @grigio, which GPU are you using? What is your system config? We can try to repro your issue with ROCm 5.7 and 6.0.2 on our side. Thanks.

CPU: AMD Ryzen 7 7700
OS: Debian Linux 12

But those was a docker container I don't have anymore


---

### 评论 #5 — grigio (2024-03-22T18:19:15Z)

ok tried in another image

```
========================= ROCm System Management Interface =========================
=========================== Version of System Component ============================
Driver version: 6.1.0-18-amd64
====================================================================================
======================================== ID ========================================
GPU[0]		: GPU ID: 0x164e
====================================================================================
==================================== Unique ID =====================================
GPU[0]		: Unique ID: N/A
====================================================================================
====================================== VBIOS =======================================
GPU[0]		: VBIOS version: 102-RAPHAEL-008
====================================================================================
=================================== Temperature ====================================
GPU[0]		: Temperature (Sensor edge) (C): 45.0
====================================================================================
============================ Current clock frequencies =============================
GPU[0]		: mclk clock level: 0: (2600Mhz)
GPU[0]		: sclk clock level: 1: (600Mhz)
GPU[0]		: socclk clock level: 1: (1200Mhz)
====================================================================================
================================ Current Fan Metric ================================
GPU[0]		: Unable to detect fan speed for GPU 0
====================================================================================
============================== Show Performance Level ==============================
GPU[0]		: Performance Level: auto
====================================================================================
================================= OverDrive Level ==================================
GPU[0]		: GPU OverDrive value (%): 0
====================================================================================
================================= OverDrive Level ==================================
GPU[0]		: GPU Memory OverDrive value (%): 0
====================================================================================
==================================== Power Cap =====================================
GPU[0]		: get_power_cap, Not supported on the given system
GPU[0]		: Max Graphics Package Power Unsupported
====================================================================================
=============================== Show Power Profiles ================================
GPU[0]		: get_power_profiles, Not supported on the given system
====================================================================================
================================ Power Consumption =================================
, Not supported on the given system
GPU[0]		: Average Graphics Package Power (W): 26.115
====================================================================================
=========================== Supported clock frequencies ============================
GPU[0]		: Supported mclk frequencies on GPU0
GPU[0]		: 0: 2600Mhz *
GPU[0]		: 
GPU[0]		: Supported sclk frequencies on GPU0
GPU[0]		: 0: 400Mhz
GPU[0]		: 1: 600Mhz *
GPU[0]		: 2: 2200Mhz
GPU[0]		: 
GPU[0]		: Supported socclk frequencies on GPU0
GPU[0]		: 0: 400Mhz
GPU[0]		: 1: 1200Mhz *
GPU[0]		: 
------------------------------------------------------------------------------------
====================================================================================
================================ % time GPU is busy ================================
GPU[0]		: GPU use (%): 0
====================================================================================
================================ Current Memory Use ================================
GPU[0]		: % memory use, Not supported on the given system
GPU[0]		: Memory Activity: N/A
====================================================================================
================================== Memory Vendor ===================================
GPU[0]		: GPU memory vendor: unknown
====================================================================================
=============================== PCIe Replay Counter ================================
GPU[0]		: PCIe Replay Count: 0
====================================================================================
================================== Serial Number ===================================
GPU[0]		: Serial Number: N/A
====================================================================================
================================== KFD Processes ===================================
get_compute_process_info_by_pid, Not supported on the given system
KFD process information:
PID    	PROCESS NAME	GPU(s)	VRAM USED	SDMA USED	CU OCCUPANCY	
3828095	UNKNOWN     	0     	UNKNOWN  	UNKNOWN  	UNKNOWN     	
====================================================================================
=============================== GPUs Indexed by PID ================================
PID 3828095 is using 0 DRM device(s)
====================================================================================
==================== GPU Memory clock frequencies and voltages =====================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
====================================================================================
================================= Current voltage ==================================
GPU[0]		: Voltage (mV): 1339
====================================================================================
==================================== PCI Bus ID ====================================
GPU[0]		: PCI Bus: 0000:0F:00.0
====================================================================================
=============================== Firmware Information ===============================
GPU[0]		: ASD firmware version: 	0x21000091
GPU[0]		: CE firmware version: 		2
GPU[0]		: DMCU firmware version: 	0
GPU[0]		: MC firmware version: 		0
GPU[0]		: ME firmware version: 		13
GPU[0]		: MEC firmware version: 	18
GPU[0]		: MEC2 firmware version: 	18
GPU[0]		: PFP firmware version: 	13
GPU[0]		: RLC firmware version: 	26
GPU[0]		: RLC SRLC firmware version: 	1
GPU[0]		: RLC SRLG firmware version: 	1
GPU[0]		: RLC SRLS firmware version: 	1
GPU[0]		: SDMA firmware version: 	1
GPU[0]		: SDMA2 firmware version: 	0
GPU[0]		: SMC firmware version: 	00.84.79.221
GPU[0]		: SOS firmware version: 	0x00000000
GPU[0]		: TA RAS firmware version: 	00.00.00.00
GPU[0]		: TA XGMI firmware version: 	00.00.00.00
GPU[0]		: UVD firmware version: 	0x00000000
GPU[0]		: VCE firmware version: 	0x00000000
GPU[0]		: VCN firmware version: 	0x02118000
====================================================================================
=================================== Product Info ===================================
GPU[0]		: Card series: 		0x164e
GPU[0]		: Card model: 		0x164e
GPU[0]		: Card vendor: 		Advanced Micro Devices, Inc. [AMD/ATI]
GPU[0]		: Card SKU: 		RAPHAEL
====================================================================================
==================================== Pages Info ====================================
GPU[0]		: ras, Not supported on the given system
============================== Show Valid sclk Range ===============================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
====================================================================================
============================== Show Valid mclk Range ===============================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
====================================================================================
============================= Show Valid voltage Range =============================
GPU[0]		: get_od_volt, Requested function is not implemented on this setup
====================================================================================
=============================== Voltage Curve Points ===============================
GPU[0]		: get_od_volt_info, Requested function is not implemented on this setup
====================================================================================
================================= Consumed Energy ==================================
GPU[0]		: % Energy Counter, Not supported on the given system
====================================================================================
============================ Current Compute Partition =============================
GPU[0]		: Not supported on the given system
====================================================================================
================================= Current NPS Mode =================================
GPU[0]		: Not supported on the given system
====================================================================================
=============================== End of ROCm SMI Log ================================
```

it seems fine

---

### 评论 #6 — nartmada (2024-03-22T20:23:47Z)

Hi @grigio, if you are not able to repro the issue anymore, can I close the ticket?  If you find the docker container and able to repro the issue again, you can re-open the ticket.  Thanks.

---
