# [Issue]: Ubuntu 24.04.4 crashing every other day (Radeon 780m)

> **Issue #6033**
> **状态**: open
> **创建时间**: 2026-03-12T05:45:06Z
> **更新时间**: 2026-05-13T18:59:25Z
> **作者**: peterwwillis
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6033

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- Jonathan03ant

## 描述

### Problem Description

Every other day, my laptop locks up. Can't do anything but force-shutdown.

I am not running anything but Firefox, typing into a window, when suddenly, the whole screen freezes. I try to switch away from X11 to a TTY, but it doesn't work. Caps lock works for a little while, then doesn't any longer.

Laptop is a ThinkPad T14s Gen4 w/AMD Ryzen 7 PRO 7840U & Radeon 780M.
System memory is 32GB. I think I have the BIOS VRAM allocation on "auto".
I have updated all the firmware updates Ubuntu has for this laptop.

OS is Ubuntu 24.04.4 LTS. Latest ROCm installed using amdgpu-install script.

Desktop is LXQt.

Below are my journalctl merged logs before I have to force-shutdown.

```
Mar 12 00:26:24 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:26:24 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:26:24 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:26:34 thinkpaddy kernel: amdgpu 0000:c3:00.0: [drm] *ERROR* [CRTC:81:crtc-0] flip_done timed out
Mar 12 00:27:47 thinkpaddy kernel: amdgpu 0000:c3:00.0: [drm] *ERROR* flip_done timed out
Mar 12 00:27:47 thinkpaddy kernel: amdgpu 0000:c3:00.0: [drm] *ERROR* [CRTC:81:crtc-0] commit wait timed out
Mar 12 00:27:57 thinkpaddy kernel: amdgpu 0000:c3:00.0: [drm] *ERROR* flip_done timed out
Mar 12 00:27:57 thinkpaddy kernel: amdgpu 0000:c3:00.0: [drm] *ERROR* [PLANE:60:plane-3] commit wait timed out
Mar 12 00:27:58 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:27:58 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:27:58 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:27:58 thinkpaddy systemd-logind[1351]: Lid opened.
Mar 12 00:27:58 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:27:59 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:27:59 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:27:59 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:27:59 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:00 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:00 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:00 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:00 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:01 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:01 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:01 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:01 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:02 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:02 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:02 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:02 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event8  - Logitech MX Ergo: SYN_DROPPED event - some input events have been lost.
Mar 12 00:28:02 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:02 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event6  - SYNA8018:00 06CB:CE67 Touchpad: SYN_DROPPED event - some input events have been lost.
Mar 12 00:28:06 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:06 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:06 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:07 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:07 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:07 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:07 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:08 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:08 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:08 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:08 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:09 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:09 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:09 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:09 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:10 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:10 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event3  - AT Translated Set 2 keyboard: SYN_DROPPED event - some input events have been lost.
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[161371]: Error on DBus request(:1.70,/StatusNotifierItem): QDBusError(org.freedesktop.DBus.Error.UnknownProperty, Property org.kde.Stat>
Mar 12 00:28:10 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[304050]: Updated device 'amdgpu_bl1':
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[304050]: Device 'amdgpu_bl1' of class 'backlight':
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[304050]:         Current brightness: 42259 (65%)
Mar 12 00:28:10 thinkpaddy /usr/libexec/gdm-x-session[304050]:         Max brightness: 64764
Mar 12 00:28:10 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:11 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:11 thinkpaddy /usr/libexec/gdm-x-session[304052]: Updated device 'amdgpu_bl1':
Mar 12 00:28:11 thinkpaddy /usr/libexec/gdm-x-session[304052]: Device 'amdgpu_bl1' of class 'backlight':
Mar 12 00:28:11 thinkpaddy /usr/libexec/gdm-x-session[304052]:         Current brightness: 39021 (60%)
Mar 12 00:28:11 thinkpaddy /usr/libexec/gdm-x-session[304052]:         Max brightness: 64764
Mar 12 00:28:11 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:11 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:11 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:12 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:12 thinkpaddy /usr/libexec/gdm-x-session[304054]: Updated device 'amdgpu_bl1':
Mar 12 00:28:12 thinkpaddy /usr/libexec/gdm-x-session[304054]: Device 'amdgpu_bl1' of class 'backlight':
Mar 12 00:28:12 thinkpaddy /usr/libexec/gdm-x-session[304054]:         Current brightness: 39021 (60%)
Mar 12 00:28:12 thinkpaddy /usr/libexec/gdm-x-session[304054]:         Max brightness: 64764
Mar 12 00:28:12 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "27"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event4  - Video Bus: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "30"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event0  - Power Button: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "31"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event2  - Sleep Button: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "37"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event5  - SYNA8018:00 06CB:CE67 Mouse: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "38"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event6  - SYNA8018:00 06CB:CE67 Touchpad: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "39"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event3  - AT Translated Set 2 keyboard: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "40"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event7  - TPPS/2 Synaptics TrackPoint: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "41"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event13 - ThinkPad Extra Buttons: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "34"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "34"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event8  - Logitech MX Ergo: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "35"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "35"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event9  - Logitech M325: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "36"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event10 - [cyh.cn](http://cyh.cn/) USB Keyboard: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "84"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "84"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event12 - [cyh.cn](http://cyh.cn/) USB Keyboard: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "86"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "86"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event11 - [cyh.cn](http://cyh.cn/) USB Keyboard: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "32"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "32"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event19 - mWave Keyboard: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (**) Option "fd" "33"
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) event20 - mWave Mouse: device removed
Mar 12 00:28:40 thinkpaddy /usr/libexec/gdm-x-session[160480]: (II) AIGLX: Suspending AIGLX clients for VT switch
Mar 12 00:28:40 thinkpaddy kernel: ------------[ cut here ]------------
Mar 12 00:28:40 thinkpaddy kernel: WARNING: CPU: 13 PID: 160480 at amd/amdgpu/../display/amdgpu_dm/amdgpu_dm.c:10396 amdgpu_dm_atomic_commit_tail+0x3c86/0x4540 [amdgpu]
Mar 12 00:28:40 thinkpaddy kernel: Modules linked in: typec_displayport nf_conntrack_netlink xt_nat veth tls xt_MASQUERADE bridge stp llc xfrm_user xfrm_algo xt_set ip_set nft_chain_nat nf_>
Mar 12 00:28:40 thinkpaddy kernel:  soundwire_bus snd_soc_sdca qrtr xt_conntrack snd_hda_codec_alc269 snd_hda_scodec_component snd_soc_core ath11k_pci edac_mce_amd snd_hda_codec_realtek_lib>
Mar 12 00:28:40 thinkpaddy kernel:  async_tx xor raid6_pq raid1 raid0 linear hid_apple cdc_ether usbnet hid_logitech_hidpp hid_logitech_dj usbhid r8152 mii amdgpu(O) ucsi_acpi typec_ucsi ty>
Mar 12 00:28:40 thinkpaddy kernel: CPU: 13 UID: 1001 PID: 160480 Comm: Xorg Tainted: G           O        6.17.0-14-generic #14~24.04.1-Ubuntu PREEMPT(voluntary) 
Mar 12 00:28:40 thinkpaddy kernel: Tainted: [O]=OOT_MODULE
Mar 12 00:28:40 thinkpaddy kernel: Hardware name: LENOVO 21F8CTO1WW/21F8CTO1WW, BIOS R2EET47W (1.28 ) 11/30/2025
Mar 12 00:28:40 thinkpaddy kernel: RIP: 0010:amdgpu_dm_atomic_commit_tail+0x3c86/0x4540 [amdgpu]
Mar 12 00:28:40 thinkpaddy kernel: Code: d0 42 df f3 e9 30 fb ff ff 31 f6 e9 e9 c9 ff ff 31 f6 e9 19 f7 ff ff 31 f6 e9 a9 f0 ff ff 80 8d 98 fe ff ff 80 e9 4f fe ff ff <0f> 0b e9 39 f5 ff ff>
Mar 12 00:28:40 thinkpaddy kernel: RSP: 0018:ffffcbd6c746f680 EFLAGS: 00010002
Mar 12 00:28:40 thinkpaddy kernel: RAX: 0000000000000246 RBX: 0000000000000246 RCX: 0000000000000000
Mar 12 00:28:40 thinkpaddy kernel: RDX: 0000000000000002 RSI: 0000000000000000 RDI: 0000000000000000
Mar 12 00:28:40 thinkpaddy kernel: RBP: ffffcbd6c746f8e8 R08: 0000000000000000 R09: 0000000000000000
Mar 12 00:28:40 thinkpaddy kernel: R10: 0000000000000000 R11: 0000000000000000 R12: ffff8984daae0000
Mar 12 00:28:40 thinkpaddy kernel: R13: 0000000000000000 R14: ffff8984e4500010 R15: ffff8984ca165800
Mar 12 00:28:40 thinkpaddy kernel: FS:  00007c312b960ac0(0000) GS:ffff898a8f0e3000(0000) knlGS:0000000000000000
Mar 12 00:28:40 thinkpaddy kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Mar 12 00:28:40 thinkpaddy kernel: CR2: 00007c312b8bf120 CR3: 00000001736d5000 CR4: 0000000000f50ef0
Mar 12 00:28:40 thinkpaddy kernel: PKRU: 55555554
Mar 12 00:28:40 thinkpaddy kernel: Call Trace:
Mar 12 00:28:40 thinkpaddy kernel:  <TASK>
Mar 12 00:28:40 thinkpaddy kernel:  commit_tail+0xc6/0x1b0
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  drm_atomic_helper_commit+0x132/0x160
Mar 12 00:28:40 thinkpaddy kernel:  drm_atomic_commit+0xac/0xf0
Mar 12 00:28:40 thinkpaddy kernel:  ? __pfx___drm_printfn_info+0x10/0x10
Mar 12 00:28:40 thinkpaddy kernel:  drm_atomic_helper_set_config+0x82/0xd0
Mar 12 00:28:40 thinkpaddy kernel:  drm_mode_setcrtc+0x3ff/0x9e0
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? drm_syncobj_array_free+0x5a/0x80
Mar 12 00:28:40 thinkpaddy kernel:  ? __pfx_drm_mode_setcrtc+0x10/0x10
Mar 12 00:28:40 thinkpaddy kernel:  drm_ioctl_kernel+0xb4/0x110
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  drm_ioctl+0x2ec/0x5b0
Mar 12 00:28:40 thinkpaddy kernel:  ? __pfx_drm_mode_setcrtc+0x10/0x10
Mar 12 00:28:40 thinkpaddy kernel:  amdgpu_drm_ioctl+0x4b/0xa0 [amdgpu]
Mar 12 00:28:40 thinkpaddy kernel:  __x64_sys_ioctl+0xa2/0x100
Mar 12 00:28:40 thinkpaddy kernel:  x64_sys_call+0x1226/0x2680
Mar 12 00:28:40 thinkpaddy kernel:  do_syscall_64+0x80/0xa30
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? __futex_wait+0xa1/0x110
Mar 12 00:28:40 thinkpaddy kernel:  ? __pfx_futex_wake_mark+0x10/0x10
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? futex_wait+0x72/0x120
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? __rseq_handle_notify_resume+0xb3/0x1a0
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? restore_fpregs_from_fpstate+0x3d/0xc0
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? switch_fpu_return+0x5c/0x100
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? arch_exit_to_user_mode_prepare.isra.0+0xc2/0xe0
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? do_syscall_64+0xb6/0xa30
Mar 12 00:28:40 thinkpaddy kernel:  ? irqentry_exit+0x43/0x50
Mar 12 00:28:40 thinkpaddy kernel:  entry_SYSCALL_64_after_hwframe+0x76/0x7e
Mar 12 00:28:40 thinkpaddy kernel: RIP: 0033:0x7c312bd24e1d
Mar 12 00:28:40 thinkpaddy kernel: Code: 04 25 28 00 00 00 48 89 45 c8 31 c0 48 8d 45 10 c7 45 b0 10 00 00 00 48 89 45 b8 48 8d 45 d0 48 89 45 c0 b8 10 00 00 00 0f 05 <89> c2 3d 00 f0 ff ff>
Mar 12 00:28:40 thinkpaddy kernel: RSP: 002b:00007ffeab1290e0 EFLAGS: 00000246 ORIG_RAX: 0000000000000010
Mar 12 00:28:40 thinkpaddy kernel: RAX: ffffffffffffffda RBX: 00006230c849a670 RCX: 00007c312bd24e1d
Mar 12 00:28:40 thinkpaddy kernel: RDX: 00007ffeab129170 RSI: 00000000c06864a2 RDI: 000000000000000f
Mar 12 00:28:40 thinkpaddy kernel: RBP: 00007ffeab129130 R08: 0000000000000000 R09: 00006230c83ee090
Mar 12 00:28:40 thinkpaddy kernel: R10: 0000000000000000 R11: 0000000000000246 R12: 00000000c06864a2
Mar 12 00:28:40 thinkpaddy kernel: R13: 000000000000000f R14: 00006230c6f30810 R15: 00006230c6b8df90
Mar 12 00:28:40 thinkpaddy kernel:  </TASK>
Mar 12 00:28:40 thinkpaddy kernel: ---[ end trace 0000000000000000 ]---
Mar 12 00:28:40 thinkpaddy kernel: ------------[ cut here ]------------
Mar 12 00:28:40 thinkpaddy kernel: WARNING: CPU: 13 PID: 160480 at amd/amdgpu/../display/amdgpu_dm/amdgpu_dm.c:9772 amdgpu_dm_atomic_commit_tail+0x3cb1/0x4540 [amdgpu]
Mar 12 00:28:40 thinkpaddy kernel: Modules linked in: typec_displayport nf_conntrack_netlink xt_nat veth tls xt_MASQUERADE bridge stp llc xfrm_user xfrm_algo xt_set ip_set nft_chain_nat nf_>
Mar 12 00:28:40 thinkpaddy kernel:  soundwire_bus snd_soc_sdca qrtr xt_conntrack snd_hda_codec_alc269 snd_hda_scodec_component snd_soc_core ath11k_pci edac_mce_amd snd_hda_codec_realtek_lib>
Mar 12 00:28:40 thinkpaddy kernel:  async_tx xor raid6_pq raid1 raid0 linear hid_apple cdc_ether usbnet hid_logitech_hidpp hid_logitech_dj usbhid r8152 mii amdgpu(O) ucsi_acpi typec_ucsi ty>
Mar 12 00:28:40 thinkpaddy kernel: CPU: 13 UID: 1001 PID: 160480 Comm: Xorg Tainted: G        W  O        6.17.0-14-generic #14~24.04.1-Ubuntu PREEMPT(voluntary) 
Mar 12 00:28:40 thinkpaddy kernel: Tainted: [W]=WARN, [O]=OOT_MODULE
Mar 12 00:28:40 thinkpaddy kernel: Hardware name: LENOVO 21F8CTO1WW/21F8CTO1WW, BIOS R2EET47W (1.28 ) 11/30/2025
Mar 12 00:28:40 thinkpaddy kernel: RIP: 0010:amdgpu_dm_atomic_commit_tail+0x3cb1/0x4540 [amdgpu]
Mar 12 00:28:40 thinkpaddy kernel: Code: 0b e9 39 f5 ff ff 0f 0b 49 8d 84 24 88 59 04 00 c6 85 20 fe ff ff 00 48 89 85 18 fe ff ff e9 51 ca ff ff 0f 0b e9 9c ca ff ff <0f> 0b e9 2f f5 ff ff>
Mar 12 00:28:40 thinkpaddy kernel: RSP: 0018:ffffcbd6c746f680 EFLAGS: 00010082
Mar 12 00:28:40 thinkpaddy kernel: RAX: 0000000000000001 RBX: 0000000000000246 RCX: 0000000000000000
Mar 12 00:28:40 thinkpaddy kernel: RDX: 0000000000000002 RSI: 0000000000000000 RDI: 0000000000000000
Mar 12 00:28:40 thinkpaddy kernel: RBP: ffffcbd6c746f8e8 R08: 0000000000000000 R09: 0000000000000000
Mar 12 00:28:40 thinkpaddy kernel: R10: 0000000000000000 R11: 0000000000000000 R12: ffff8984daae0000
Mar 12 00:28:40 thinkpaddy kernel: R13: 0000000000000000 R14: ffff8984e4500010 R15: ffff8984ca165800
Mar 12 00:28:40 thinkpaddy kernel: FS:  00007c312b960ac0(0000) GS:ffff898a8f0e3000(0000) knlGS:0000000000000000
Mar 12 00:28:40 thinkpaddy kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Mar 12 00:28:40 thinkpaddy kernel: CR2: 00007c312b8bf120 CR3: 00000001736d5000 CR4: 0000000000f50ef0
Mar 12 00:28:40 thinkpaddy kernel: PKRU: 55555554
Mar 12 00:28:40 thinkpaddy kernel: Call Trace:
Mar 12 00:28:40 thinkpaddy kernel:  <TASK>
Mar 12 00:28:40 thinkpaddy kernel:  commit_tail+0xc6/0x1b0
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  drm_atomic_helper_commit+0x132/0x160
Mar 12 00:28:40 thinkpaddy kernel:  drm_atomic_commit+0xac/0xf0
Mar 12 00:28:40 thinkpaddy kernel:  ? __pfx___drm_printfn_info+0x10/0x10
Mar 12 00:28:40 thinkpaddy kernel:  drm_atomic_helper_set_config+0x82/0xd0
Mar 12 00:28:40 thinkpaddy kernel:  drm_mode_setcrtc+0x3ff/0x9e0
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? drm_syncobj_array_free+0x5a/0x80
Mar 12 00:28:40 thinkpaddy kernel:  ? __pfx_drm_mode_setcrtc+0x10/0x10
Mar 12 00:28:40 thinkpaddy kernel:  drm_ioctl_kernel+0xb4/0x110
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  drm_ioctl+0x2ec/0x5b0
Mar 12 00:28:40 thinkpaddy kernel:  ? __pfx_drm_mode_setcrtc+0x10/0x10
Mar 12 00:28:40 thinkpaddy kernel:  amdgpu_drm_ioctl+0x4b/0xa0 [amdgpu]
Mar 12 00:28:40 thinkpaddy kernel:  __x64_sys_ioctl+0xa2/0x100
Mar 12 00:28:40 thinkpaddy kernel:  x64_sys_call+0x1226/0x2680
Mar 12 00:28:40 thinkpaddy kernel:  do_syscall_64+0x80/0xa30
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? __futex_wait+0xa1/0x110
Mar 12 00:28:40 thinkpaddy kernel:  ? __pfx_futex_wake_mark+0x10/0x10
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? futex_wait+0x72/0x120
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? __rseq_handle_notify_resume+0xb3/0x1a0
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? restore_fpregs_from_fpstate+0x3d/0xc0
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? switch_fpu_return+0x5c/0x100
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? arch_exit_to_user_mode_prepare.isra.0+0xc2/0xe0
Mar 12 00:28:40 thinkpaddy kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 12 00:28:40 thinkpaddy kernel:  ? do_syscall_64+0xb6/0xa30
Mar 12 00:28:40 thinkpaddy kernel:  ? irqentry_exit+0x43/0x50
Mar 12 00:28:40 thinkpaddy kernel:  entry_SYSCALL_64_after_hwframe+0x76/0x7e
Mar 12 00:28:40 thinkpaddy kernel: RIP: 0033:0x7c312bd24e1d
Mar 12 00:28:40 thinkpaddy kernel: Code: 04 25 28 00 00 00 48 89 45 c8 31 c0 48 8d 45 10 c7 45 b0 10 00 00 00 48 89 45 b8 48 8d 45 d0 48 89 45 c0 b8 10 00 00 00 0f 05 <89> c2 3d 00 f0 ff ff>
Mar 12 00:28:40 thinkpaddy kernel: RSP: 002b:00007ffeab1290e0 EFLAGS: 00000246 ORIG_RAX: 0000000000000010
Mar 12 00:28:40 thinkpaddy kernel: RAX: ffffffffffffffda RBX: 00006230c849a670 RCX: 00007c312bd24e1d
Mar 12 00:28:40 thinkpaddy kernel: RDX: 00007ffeab129170 RSI: 00000000c06864a2 RDI: 000000000000000f
Mar 12 00:28:40 thinkpaddy kernel: RBP: 00007ffeab129130 R08: 0000000000000000 R09: 00006230c83ee090
Mar 12 00:28:40 thinkpaddy kernel: R10: 0000000000000000 R11: 0000000000000246 R12: 00000000c06864a2
Mar 12 00:28:40 thinkpaddy kernel: R13: 000000000000000f R14: 00006230c6f30810 R15: 00006230c6b8df90
Mar 12 00:28:40 thinkpaddy kernel:  </TASK>
Mar 12 00:28:40 thinkpaddy kernel: ---[ end trace 0000000000000000 ]---
Mar 12 00:28:41 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:41 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:41 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:41 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:41 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:42 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:42 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
Mar 12 00:28:52 thinkpaddy kernel: amdgpu 0000:c3:00.0: [drm] *ERROR* [CRTC:81:crtc-0] flip_done timed out
Mar 12 00:30:13 thinkpaddy kernel: Linux version 6.17.0-14-generic (buildd@lcy02-amd64-067) (x86_64-linux-gnu-gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0, GNU ld (GNU Binutils for Ubuntu) >
Mar 12 00:30:13 thinkpaddy kernel: Command line: BOOT_IMAGE=/boot/vmlinuz-6.17.0-14-generic root=UUID=6e0be196-fd6a-4f4d-9a3b-25d4955be15a ro quiet splash vt.handoff=7
Mar 12 00:30:13 thinkpaddy kernel: KERNEL supported cpus:
Mar 12 00:30:13 thinkpaddy kernel:   Intel GenuineIntel
Mar 12 00:30:13 thinkpaddy kernel:   AMD AuthenticAMD
Mar 12 00:30:13 thinkpaddy kernel:   Hygon HygonGenuine
Mar 12 00:30:13 thinkpaddy kernel:   Centaur CentaurHauls
Mar 12 00:30:13 thinkpaddy kernel:   zhaoxin   Shanghai  
```


Kernel boot messages from amdgpu:

```
Mar 12 00:30:13 thinkpaddy kernel: [drm] amdgpu kernel modesetting enabled.
Mar 12 00:30:13 thinkpaddy kernel: [drm] amdgpu version: 6.16.13
Mar 12 00:30:13 thinkpaddy kernel: [drm] OS DRM version: 6.17.0
Mar 12 00:30:13 thinkpaddy kernel: amdgpu: Virtual CRAT table created for CPU
Mar 12 00:30:13 thinkpaddy kernel: amdgpu: Topology: Add CPU node
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: enabling device (0006 -> 0007)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: initializing kernel modesetting (IP DISCOVERY 0x1002:0x15BF 0x17AA:0x50D8 0xDD).
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: register mmio base: 0x90500000
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: register mmio size: 524288
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: detected ip block number 0 <common_v1_0_0> (soc21_common)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: detected ip block number 1 <gmc_v11_0_0> (gmc_v11_0)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: detected ip block number 2 <ih_v6_0_0> (ih_v6_0)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: detected ip block number 3 <psp_v13_0_4> (psp)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: detected ip block number 4 <smu_v13_0_0> (smu)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: detected ip block number 5 <dce_v1_0_0> (dm)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: detected ip block number 6 <gfx_v11_0_0> (gfx_v11_0)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: detected ip block number 7 <sdma_v6_0_0> (sdma_v6_0)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: detected ip block number 8 <vcn_v4_0_0> (vcn_v4_0)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: detected ip block number 9 <jpeg_v4_0_0> (jpeg_v4_0)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: detected ip block number 10 <mes_v11_0_0> (mes_v11_0)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: Fetched VBIOS from VFCT
Mar 12 00:30:13 thinkpaddy kernel: amdgpu: ATOM BIOS: 113-PHXGENERIC-001
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: vgaarb: deactivate vga console
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: Trusted Memory Zone (TMZ) feature enabled
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: VRAM: 8192M 0x0000008000000000 - 0x00000081FFFFFFFF (8192M used)
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
Mar 12 00:30:13 thinkpaddy kernel: [drm] Detected VRAM RAM=8192M, BAR=8192M
Mar 12 00:30:13 thinkpaddy kernel: [drm] RAM width 128bits LPDDR5
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: amdgpu: 8192M of VRAM memory ready
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: amdgpu: 11834M of GTT memory ready.
Mar 12 00:30:13 thinkpaddy kernel: [drm] GART: num cpu pages 131072, num gpu pages 131072
Mar 12 00:30:13 thinkpaddy kernel: [drm] PCIE GART of 512M enabled (table at 0x00000081FFD00000).
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x08005400
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: [VCN instance 0] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 27
Mar 12 00:30:13 thinkpaddy kernel: amdgpu 0000:c3:00.0: amdgpu: reserve 0x4000000 from 0x81f8000000 for PSP TMR
```

### Operating System

Ubuntu 24.04.4 LTS

### CPU

AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics

### GPU

AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics

### ROCm Version

ROCm 7.2.0.70200-43~24.04

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
[37mROCk module version 6.16.13 is loaded[0m
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.15
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   5134                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    24237588(0x171d614) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24237588(0x171d614) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    24237588(0x171d614) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    24237588(0x171d614) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      2048(0x800) KB                     
  Chip ID:                 5567(0x15bf)                       
  ASIC Revision:           9(0x9)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   49920                              
  Internal Node ID:        1                                  
  Compute Unit:            12                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       APU
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          32(0x20)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    1024(0x400)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 68                                 
  SDMA engine uCode::      23                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    12118792(0xb8eb08) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    12118792(0xb8eb08) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1100         
      Machine Models:          HSA_MACHINE_MODEL_LARGE            
      Profiles:                HSA_PROFILE_BASE                   
      Default Rounding Mode:   NEAR                               
      Default Rounding Mode:   NEAR                               
      Fast f16:                TRUE                               
      Workgroup Max Size:      1024(0x400)                        
      Workgroup Max Size per Dimension:
        x                        1024(0x400)                        
        y                        1024(0x400)                        
        z                        1024(0x400)                        
      Grid Max Size:           4294967295(0xffffffff)             
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
      Machine Models:          HSA_MACHINE_MODEL_LARGE            
      Profiles:                HSA_PROFILE_BASE                   
      Default Rounding Mode:   NEAR                               
      Default Rounding Mode:   NEAR                               
      Fast f16:                TRUE                               
      Workgroup Max Size:      1024(0x400)                        
      Workgroup Max Size per Dimension:
        x                        1024(0x400)                        
        y                        1024(0x400)                        
        z                        1024(0x400)                        
      Grid Max Size:           4294967295(0xffffffff)             
      Grid Max Size per Dimension:
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
*******                  
Agent 3                  
*******                  
  Name:                    aie2                               
  Uuid:                    AIE-XX                             
  Marketing Name:          RyzenAI-npu1                       
  Vendor Name:             AMD                                
  Feature:                 AGENT_DISPATCH                     
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        1(0x1)                             
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          64(0x40)                           
  Queue Type:              SINGLE                             
  Node:                    0                                  
  Device Type:             DSP                                
  Cache Info:              
    L2:                      2048(0x800) KB                     
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          0(0x0)                             
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            0                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:0                                  
  Memory Properties:       
  Features:                AGENT_DISPATCH
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    24237588(0x171d614) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65536(0x10000) KB                  
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    24237588(0x171d614) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***             
```

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — chejh-amd (2026-03-17T02:57:44Z)

This is typically a known issue with the 7840U/780M when using a newer kernel together with the AMD DKMS driver.
Try to add amdgpu.dcdebugmask=0x10 to /etc/default/grub to disable PSR and see if it stabilizes the system.

---

### 评论 #2 — Jonathan03ant (2026-03-23T03:15:13Z)

@peterwwillis as @Michelle-HCJ pointed out, this is a power management bug on newer kernel versions. The driver enables PSR but the Display Microcontroller Firmware has a bug when handling Panel Self Refresh transitions during sleep/wake cycles. When the firmware crashes, the display controller times out and the system freezes. 

A workaround would be to just disable PSR via kernel parameter. 
```bash
 # Add to /etc/default/grub:
  GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdgpu.dcdebugmask=0x10"
  sudo update-grub
  sudo reboot
```
The system will stay stable but the display will refresh continuously instead of self refresh (which might lead to slightly higher battery usage). 

The real fix will require a kernel/firmware bug fix. 

---

### 评论 #3 — peterwwillis (2026-03-24T04:34:01Z)

@Jonathan03ant do you know which kernel versions are the last stable ones so I can try to downgrade? i'd rather keep my limited battery life...

---

### 评论 #4 — chejh-amd (2026-03-24T05:15:20Z)

@peterwwillis kernel version 6.6.2 is stable

---

### 评论 #5 — Jonathan03ant (2026-03-25T16:13:18Z)

@peterwwillis yes 6.6.2 is stable, I will raise an internal ticket so this is fixed from our side properly. 


---

### 评论 #6 — peterwwillis (2026-04-09T13:46:56Z)

@Jonathan03ant FYI, the earliest stable Ubuntu 24.04 LTS kernel is 6.8. I was using it reliably for months before I upgraded both my system firmware and kernel, and the crashing started soon after. So either it's a bug that happened after 6.6, or a firmware bug, or both. Either way, it would be nice to have a stable LTS linux operating system again

---

### 评论 #7 — Jonathan03ant (2026-04-09T16:25:03Z)

@peterwwillis I will include this information, an internal ticket has already been issued to the driver/firmware team. 

---

### 评论 #8 — kumuthu53 (2026-04-23T10:46:24Z)

I, too, am running into this issue frequently.

```
Kernel: Linux 6.19.12-200.fc43.x86_64
CPU: AMD Ryzen 5 PRO 8540U (12) @ 3.20 GHz
GPU: AMD Radeon 740M Graphics [Integrated]
```

---

### 评论 #9 — peterwwillis (2026-05-13T15:53:48Z)

Any updates on this? Yet another crash, and my battery life on suspend is horrible. Starting to feel like I should just sell this laptop and buy an Intel, at least their drivers work

---

### 评论 #10 — Jonathan03ant (2026-05-13T18:59:25Z)

@peterwwillis @kumuthu53 there is an internal ticket on this issue and it is currently being looked at. I will provide update when this is fixed, since its driver/firmware related issue, we might have to wait for a new release. 

Thanks

---
