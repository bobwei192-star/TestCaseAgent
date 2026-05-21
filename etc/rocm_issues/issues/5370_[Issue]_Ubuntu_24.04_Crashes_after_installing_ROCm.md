# [Issue]: Ubuntu 24.04 Crashes after installing ROCm

> **Issue #5370**
> **状态**: closed
> **创建时间**: 2025-09-17T20:03:29Z
> **更新时间**: 2025-10-08T14:49:52Z
> **关闭时间**: 2025-09-25T16:22:20Z
> **作者**: isapir
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5370

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- harkgill-amd

## 描述

### Problem Description

At random times, the screen becomes pixelated with random colors and nothing can be done until a hard reboot

```
echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";
echo "CPU: " && cat /proc/cpuinfo | grep "model name" | sort --unique;
echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
```
Output:
>```
>OS:
>NAME="Ubuntu"
>VERSION="24.04.3 LTS (Noble Numbat)"
>CPU: 
>model name	: AMD Ryzen AI 9 HX PRO 370 w/ Radeon 890M
>GPU:
>  Name:                    AMD Ryzen AI 9 HX PRO 370 w/ Radeon 890M
>  Marketing Name:          AMD Ryzen AI 9 HX PRO 370 w/ Radeon 890M
>  Name:                    gfx1150                            
>  Marketing Name:          AMD Radeon Graphics                
>      Name:                    amdgcn-amd-amdhsa--gfx1150         
>      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
>  Name:                    aie2                               
>  Marketing Name:          AIE-ML
>```


### Operating System

24.04.3 LTS (Noble Numbat)

### CPU

AMD Ryzen AI 9 HX PRO 370 w/ Radeon 890M

### GPU

Radeon 890M

### ROCm Version

ROCm 6.4.2.1

### ROCm Component

_No response_

### Steps to Reproduce

Just using the computer

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.12.12 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
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
  Name:                    AMD Ryzen AI 9 HX PRO 370 w/ Radeon 890M
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen AI 9 HX PRO 370 w/ Radeon 890M
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
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   5157                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    90245004(0x561078c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    90245004(0x561078c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    90245004(0x561078c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    90245004(0x561078c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1150                            
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
  Chip ID:                 5390(0x150e)                       
  ASIC Revision:           4(0x4)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   50432                              
  Internal Node ID:        1                                  
  Compute Unit:            16                                 
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 25                                 
  SDMA engine uCode::      11                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    45122500(0x2b083c4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    45122500(0x2b083c4) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1150         
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*******                  
Agent 3                  
*******                  
  Name:                    aie2                               
  Uuid:                    AIE-XX                             
  Marketing Name:          AIE-ML                             
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
      Size:                    90245004(0x561078c) KB             
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
      Size:                    90245004(0x561078c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***   

### Additional Information

_No response_

---

## 评论 (29 条)

### 评论 #1 — isapir (2025-09-17T20:04:37Z)

This is what I see on my screen:

![Image](https://github.com/user-attachments/assets/c17eb2da-0d72-44ab-84ff-8ecd76705092)
![Image](https://github.com/user-attachments/assets/e629356b-9066-4c39-8562-35f356784d34)
https://github.com/user-attachments/assets/46104814-58db-4c85-93e0-01e842d1861c

---

### 评论 #2 — isapir (2025-09-17T20:13:02Z)

Shortly after posting the above the computer screen turned black and the computer became unusable until a hard reboot.  This is making it impossible for me to work.

I hope that you can respond in a timely manner.

---

### 评论 #3 — isapir (2025-09-17T20:15:39Z)

This is the output of `journalctl -b -2 -p 0..4 --no-pager` (Pixelated Screen Crash):

```
Sep 17 10:27:49 p14s kernel: i8042: Warning: Keylock active
Sep 17 10:27:49 p14s kernel: device-mapper: core: CONFIG_IMA_DISABLE_HTABLE is disabled. Duplicate IMA measurements will not be recorded in the IMA log.
Sep 17 10:27:49 p14s kernel: amdkcl: loading out-of-tree module taints kernel.
Sep 17 10:27:49 p14s systemd-journald[972]: File /var/log/journal/cd15e59b9d334020a0dfd6a12d3e1f20/system.journal corrupted or uncleanly shut down, renaming and replacing.
Sep 17 10:27:50 p14s (udev-worker)[1138]: controlC1: Process '/usr/sbin/alsactl -E HOME=/run/alsa -E XDG_RUNTIME_DIR=/run/alsa/runtime restore 1' failed with exit code 99.
Sep 17 10:27:51 p14s (uetoothd)[1791]: bluetooth.service: ConfigurationDirectory 'bluetooth' already exists but the mode is different. (File system: 755 ConfigurationDirectoryMode: 555)
Sep 17 10:27:51 p14s systemd[1]: Dependency failed for sssd-nss.socket - SSSD NSS Service responder socket.
Sep 17 10:27:51 p14s systemd[1]: Dependency failed for sssd-autofs.socket - SSSD AutoFS Service responder socket.
Sep 17 10:27:51 p14s systemd[1]: Dependency failed for sssd-pac.socket - SSSD PAC Service responder socket.
Sep 17 10:27:51 p14s systemd[1]: Dependency failed for sssd-pam-priv.socket - SSSD PAM Service responder private socket.
Sep 17 10:27:51 p14s systemd[1]: Dependency failed for sssd-pam.socket - SSSD PAM Service responder socket.
Sep 17 10:27:51 p14s systemd[1]: Dependency failed for sssd-ssh.socket - SSSD SSH Service responder socket.
Sep 17 10:27:51 p14s systemd[1]: Dependency failed for sssd-sudo.socket - SSSD Sudo Service responder socket.
Sep 17 10:27:51 p14s (cron)[1815]: cron.service: Referenced but unset environment variable evaluates to an empty string: EXTRA_OPTS
Sep 17 10:27:51 p14s bluetoothd[1791]: src/plugin.c:plugin_init() System does not support csip plugin
Sep 17 10:27:51 p14s bluetoothd[1791]: profiles/audio/micp.c:micp_init() D-Bus experimental not enabled
Sep 17 10:27:51 p14s bluetoothd[1791]: src/plugin.c:plugin_init() System does not support micp plugin
Sep 17 10:27:51 p14s bluetoothd[1791]: src/plugin.c:plugin_init() System does not support vcp plugin
Sep 17 10:27:51 p14s bluetoothd[1791]: src/plugin.c:plugin_init() System does not support mcp plugin
Sep 17 10:27:51 p14s bluetoothd[1791]: src/plugin.c:plugin_init() System does not support bass plugin
Sep 17 10:27:51 p14s bluetoothd[1791]: src/plugin.c:plugin_init() System does not support bap plugin
Sep 17 10:27:51 p14s gnome-remote-de[1795]: Init TPM credentials failed because Failed to initialize transmission interface context: tcti:IO failure, using GKeyFile as fallback
Sep 17 10:27:51 p14s systemd[1]: Cannot find unit for notify message of PID 1946, ignoring.
Sep 17 10:27:51 p14s kernel: nvme nvme0: using unchecked data buffer
Sep 17 10:27:51 p14s kernel: block nvme0n1: No UUID available providing old NGUID
Sep 17 10:27:51 p14s boltd[1952]: [92733804-004c-domain0                    ] udev: failed to determine if uid is stable: unknown NHI PCI id '0x151c'
Sep 17 10:27:51 p14s boltd[1952]: [92733804-014c-domain1                    ] udev: failed to determine if uid is stable: unknown NHI PCI id '0x151d'
Sep 17 10:27:51 p14s generate[1979]: Permissions for /etc/netplan/01-network-manager-all.yaml are too open. Netplan configuration should NOT be accessible by others.
Sep 17 10:27:51 p14s kernel: Bluetooth: hci0: HCI Enhanced Setup Synchronous Connection command is advertised, but not supported.
Sep 17 10:27:51 p14s bluetoothd[1791]: profiles/sap/server.c:sap_server_register() Sap driver initialization failed.
Sep 17 10:27:51 p14s bluetoothd[1791]: sap-server: Operation not permitted (1)
Sep 17 10:27:52 p14s systemd[1]: Cannot find unit for notify message of PID 2072, ignoring.
Sep 17 10:27:52 p14s systemd[1]: Cannot find unit for notify message of PID 2234, ignoring.
Sep 17 10:27:56 p14s wpa_supplicant[1848]: bgscan simple: Failed to enable signal strength monitoring
Sep 17 10:27:57 p14s systemd[1]: kerneloops.service: Found left-over process 2392 (kerneloops) in control group while starting unit. Ignoring.
Sep 17 10:27:57 p14s systemd[1]: kerneloops.service: This usually indicates unclean termination of a previous run, or service implementation deficiencies.
Sep 17 10:27:57 p14s (rneloops)[2394]: kerneloops.service: Referenced but unset environment variable evaluates to an empty string: DAEMON_ARGS
Sep 17 10:27:57 p14s kernel: kauditd_printk_skb: 181 callbacks suppressed
Sep 17 10:27:57 p14s ModemManager[1948]: <wrn> [modem0] modem couldn't be initialized: eSIM without profiles detected
Sep 17 10:28:02 p14s gdm3[2160]: Gdm: on_display_added: assertion 'GDM_IS_REMOTE_DISPLAY (display)' failed
Sep 17 10:28:03 p14s pipewire[2724]: mod.jackdbus-detect: Failed to receive jackdbus reply: org.freedesktop.DBus.Error.ServiceUnknown: The name org.jackaudio.service was not provided by any .service files
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Activating service name='org.freedesktop.systemd1' requested by ':1.2' (uid=120 pid=2759 comm="/usr/libexec/gnome-session-binary --autostart /usr" label="unconfined")
Sep 17 10:28:03 p14s wireplumber[2727]: Failed to get percentage from UPower: org.freedesktop.DBus.Error.NameHasNoOwner
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Activated service 'org.freedesktop.systemd1' failed: Process org.freedesktop.systemd1 exited with status 1
Sep 17 10:28:03 p14s gnome-session-binary[2759]: WARNING: Could not check if unit gnome-session-wayland@gnome-login.target is active: Error calling StartServiceByName for org.freedesktop.systemd1: Process org.freedesktop.systemd1 exited with status 1
Sep 17 10:28:03 p14s wireplumber[2727]: Failed to create 'api.alsa.acp.device' device
Sep 17 10:28:03 p14s systemd[2712]: snap.snapd-desktop-integration.snapd-desktop-integration.service: Failed with result 'exit-code'.
Sep 17 10:28:03 p14s wireplumber[2727]: <WpPortalPermissionStorePlugin:0x62e396f2ab30> Failed to call Lookup: GDBus.Error:org.freedesktop.portal.Error.NotFound: No entry for camera
Sep 17 10:28:03 p14s wireplumber[2727]: <WpPortalPermissionStorePlugin:0x62e396f2ab30> Failed to call Lookup: GDBus.Error:org.freedesktop.portal.Error.NotFound: No entry for camera
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Activating service name='org.a11y.Bus' requested by ':1.4' (uid=120 pid=2813 comm="/usr/bin/gnome-shell" label="unconfined")
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Successfully activated service 'org.a11y.Bus'
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2896]: dbus-daemon[2896]: Activating service name='org.a11y.atspi.Registry' requested by ':1.0' (uid=120 pid=2813 comm="/usr/bin/gnome-shell" label="unconfined")
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2896]: dbus-daemon[2896]: Successfully activated service 'org.a11y.atspi.Registry'
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Activating service name='org.gnome.Shell.Screencast' requested by ':1.3' (uid=120 pid=2813 comm="/usr/bin/gnome-shell" label="unconfined")
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Activating service name='org.freedesktop.impl.portal.PermissionStore' requested by ':1.3' (uid=120 pid=2813 comm="/usr/bin/gnome-shell" label="unconfined")
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Successfully activated service 'org.freedesktop.impl.portal.PermissionStore'
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Activating service name='org.gnome.Shell.Notifications' requested by ':1.3' (uid=120 pid=2813 comm="/usr/bin/gnome-shell" label="unconfined")
Sep 17 10:28:03 p14s gnome-shell[2813]: Unable to connect to ibus: Could not connect: No such file or directory
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Successfully activated service 'org.gnome.Shell.Notifications'
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Activating service name='org.freedesktop.systemd1' requested by ':1.9' (uid=120 pid=2952 comm="/usr/libexec/gsd-sharing" label="unconfined")
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Activated service 'org.freedesktop.systemd1' failed: Process org.freedesktop.systemd1 exited with status 1
Sep 17 10:28:03 p14s gsd-sharing[2952]: Failed to StopUnit service: GDBus.Error:org.freedesktop.DBus.Error.Spawn.ChildExited: Process org.freedesktop.systemd1 exited with status 1
Sep 17 10:28:03 p14s gsd-sharing[2952]: Failed to StopUnit service: GDBus.Error:org.freedesktop.DBus.Error.Spawn.ChildExited: Process org.freedesktop.systemd1 exited with status 1
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Activating service name='org.freedesktop.portal.IBus' requested by ':1.24' (uid=120 pid=2991 comm="ibus-daemon --panel disable" label="unconfined")
Sep 17 10:28:03 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Successfully activated service 'org.freedesktop.portal.IBus'
Sep 17 10:28:04 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Activating service name='org.gnome.ScreenSaver' requested by ':1.22' (uid=120 pid=3045 comm="/usr/libexec/gsd-power" label="unconfined")
Sep 17 10:28:04 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Successfully activated service 'org.gnome.Shell.Screencast'
Sep 17 10:28:04 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Activating service name='org.freedesktop.portal.IBus' requested by ':1.34' (uid=120 pid=3192 comm="ibus-daemon --panel disable -r --xim" label="unconfined")
Sep 17 10:28:04 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Successfully activated service 'org.freedesktop.portal.IBus'
Sep 17 10:28:04 p14s /usr/libexec/gdm-wayland-session[2757]: dbus-daemon[2757]: [session uid=120 pid=2757] Successfully activated service 'org.gnome.ScreenSaver'
Sep 17 10:28:04 p14s gsd-media-keys[2999]: Failed to grab accelerator for keybinding settings:hibernate
Sep 17 10:28:04 p14s gsd-media-keys[2999]: Failed to grab accelerator for keybinding settings:playback-repeat
Sep 17 10:28:07 p14s ModemManager[1948]: <wrn> [modem0] couldn't load supported assistance data types: Failed to receive indication with the predicted orbits data source
Sep 17 10:28:08 p14s kernel: workqueue: pm_runtime_work hogged CPU for >13333us 4 times, consider switching to WQ_UNBOUND
Sep 17 10:28:08 p14s ModemManager[1948]: <wrn> [modem0] error initializing: Modem in failed state: esim-without-profiles
Sep 17 10:28:13 p14s gdm-fingerprint][3296]: gkr-pam: no password is available for user
Sep 17 10:28:16 p14s gdm-password][3295]: gkr-pam: unable to locate daemon control file
Sep 17 10:28:17 p14s systemd-journald[972]: File /var/log/journal/cd15e59b9d334020a0dfd6a12d3e1f20/user-1000.journal corrupted or uncleanly shut down, renaming and replacing.
Sep 17 10:28:17 p14s pipewire[3332]: mod.jackdbus-detect: Failed to receive jackdbus reply: org.freedesktop.DBus.Error.ServiceUnknown: The name org.jackaudio.service was not provided by any .service files
Sep 17 10:28:17 p14s wireplumber[3336]: <WpPortalPermissionStorePlugin:0x5ccb71b9d250> Failed to call Lookup: GDBus.Error:org.freedesktop.portal.Error.NotFound: No entry for camera
Sep 17 10:28:17 p14s wireplumber[3336]: <WpPortalPermissionStorePlugin:0x5ccb71b9d250> Failed to call Lookup: GDBus.Error:org.freedesktop.portal.Error.NotFound: No entry for camera
Sep 17 10:28:17 p14s gdm3[2160]: Gdm: on_display_added: assertion 'GDM_IS_REMOTE_DISPLAY (display)' failed
Sep 17 10:28:17 p14s gsd-media-keys[2999]: Unable to get default sink
Sep 17 10:28:17 p14s gsd-media-keys[2999]: Unable to get default source
Sep 17 10:28:17 p14s wireplumber[3336]: Failed to create 'api.alsa.acp.device' device
Sep 17 10:28:17 p14s gnome-keyring-daemon[3565]: discover_other_daemon: 1
Sep 17 10:28:17 p14s gnome-keyring-daemon[3568]: discover_other_daemon: 1
Sep 17 10:28:17 p14s systemd[3317]: app-gnome-gnome\x2dkeyring\x2dpkcs11-3557.scope: No PIDs left to attach to the scope's control group, refusing.
Sep 17 10:28:17 p14s systemd[3317]: app-gnome-gnome\x2dkeyring\x2dpkcs11-3557.scope: Failed with result 'resources'.
Sep 17 10:28:17 p14s systemd[3317]: Failed to start app-gnome-gnome\x2dkeyring\x2dpkcs11-3557.scope - Application launched by gnome-session-binary.
Sep 17 10:28:17 p14s systemd[3317]: app-gnome-gnome\x2dkeyring\x2dsecrets-3555.scope: No PIDs left to attach to the scope's control group, refusing.
Sep 17 10:28:17 p14s systemd[3317]: app-gnome-gnome\x2dkeyring\x2dsecrets-3555.scope: Failed with result 'resources'.
Sep 17 10:28:17 p14s systemd[3317]: Failed to start app-gnome-gnome\x2dkeyring\x2dsecrets-3555.scope - Application launched by gnome-session-binary.
Sep 17 10:28:17 p14s gnome-keyring-daemon[3573]: discover_other_daemon: 1
Sep 17 10:28:17 p14s systemd[3317]: app-gnome-xdg\x2duser\x2ddirs-3582.scope: No PIDs left to attach to the scope's control group, refusing.
Sep 17 10:28:17 p14s systemd[3317]: app-gnome-xdg\x2duser\x2ddirs-3582.scope: Failed with result 'resources'.
Sep 17 10:28:17 p14s systemd[3317]: Failed to start app-gnome-xdg\x2duser\x2ddirs-3582.scope - Application launched by gnome-session-binary.
Sep 17 10:28:18 p14s systemd[3317]: Dependency failed for org.gnome.SettingsDaemon.XSettings.service - GNOME XSettings service.
Sep 17 10:28:18 p14s gnome-shell[3580]: Gio.UnixInputStream has been moved to a separate platform-specific library. Please update your code to use GioUnix.InputStream instead.
                                        0 inhibit() ["resource:///org/gnome/shell/misc/loginManager.js":209:8]
                                        1 InterpretGeneratorResume() ["self-hosted":1461:33]
                                        2 AsyncFunctionNext() ["self-hosted":852:26]
                                        3 anonymous() ["resource:///org/gnome/shell/ui/init.js":21:19]
Sep 17 10:28:18 p14s at-spi2-registr[3679]: Failed to register client: GDBus.Error:org.gnome.SessionManager.AlreadyRegistered: Unable to register client
Sep 17 10:28:18 p14s at-spi2-registr[3679]: Unable to register client with session manager
Sep 17 10:28:18 p14s gnome-session-binary[3522]: GnomeDesktop-WARNING: Could not create transient scope for PID 3835: GDBus.Error:org.freedesktop.DBus.Error.UnixProcessIdUnknown: Failed to set unit properties: No such process
Sep 17 10:28:18 p14s gnome-session-binary[3522]: GnomeDesktop-WARNING: Could not create transient scope for PID 3855: GDBus.Error:org.freedesktop.DBus.Error.UnixProcessIdUnknown: Failed to set unit properties: No such process
Sep 17 10:28:18 p14s systemd[3317]: app-gnome-ubuntu\x2dreport\x2don\x2dupgrade-3842.scope: No PIDs left to attach to the scope's control group, refusing.
Sep 17 10:28:18 p14s systemd[3317]: app-gnome-ubuntu\x2dreport\x2don\x2dupgrade-3842.scope: Failed with result 'resources'.
Sep 17 10:28:18 p14s systemd[3317]: Failed to start app-gnome-ubuntu\x2dreport\x2don\x2dupgrade-3842.scope - Application launched by gnome-session-binary.
Sep 17 10:28:18 p14s gsd-media-keys[3744]: Failed to grab accelerator for keybinding settings:playback-repeat
Sep 17 10:28:18 p14s gsd-media-keys[3744]: Failed to grab accelerator for keybinding settings:hibernate
Sep 17 10:28:18 p14s gnome-shell[2813]: Connection to xwayland lost
Sep 17 10:28:18 p14s gnome-shell[2813]: Xwayland terminated, exiting since it was mandatory
Sep 17 10:28:18 p14s gnome-shell[2813]: (../src/core/meta-context.c:542):meta_context_terminate: runtime check failed: (g_main_loop_is_running (priv->main_loop))
Sep 17 10:28:18 p14s gnome-shell[2813]: JS ERROR: Gio.IOErrorEnum: Xwayland exited unexpectedly
                                        @resource:///org/gnome/shell/ui/init.js:21:20
Sep 17 10:28:18 p14s gsd-rfkill[2978]: Error releasing name org.gnome.SettingsDaemon.Rfkill: The connection is closed
Sep 17 10:28:18 p14s gsd-smartcard[2987]: Error releasing name org.gnome.SettingsDaemon.Smartcard: The connection is closed
Sep 17 10:28:18 p14s gsd-screensaver[3008]: Error releasing name org.freedesktop.ScreenSaver: The connection is closed
Sep 17 10:28:19 p14s gdm3[2160]: Gdm: on_display_removed: assertion 'GDM_IS_REMOTE_DISPLAY (display)' failed
Sep 17 10:28:26 p14s gnome-shell[3580]: meta_window_set_stack_position_no_sync: assertion 'window->stack_position >= 0' failed
Sep 17 10:28:32 p14s gnome-shell[3580]: meta_window_set_stack_position_no_sync: assertion 'window->stack_position >= 0' failed
Sep 17 10:28:33 p14s tracker-miner-f[4064]: tracker_resource_set_relation: NULL is not a valid value.
Sep 17 10:28:43 p14s kernel: kauditd_printk_skb: 28 callbacks suppressed
Sep 17 10:28:43 p14s gnome-shell[3580]: meta_window_set_stack_position_no_sync: assertion 'window->stack_position >= 0' failed
Sep 17 10:28:43 p14s io.snapcraft.Settings[4751]: userd.go:93: Starting snap userd
Sep 17 10:29:59 p14s kernel: kauditd_printk_skb: 106 callbacks suppressed
Sep 17 10:30:09 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
Sep 17 10:30:16 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
Sep 17 10:30:25 p14s gnome-shell[3580]: meta_window_set_stack_position_no_sync: assertion 'window->stack_position >= 0' failed
Sep 17 10:32:52 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
Sep 17 10:45:56 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
Sep 17 10:46:08 p14s kernel: kauditd_printk_skb: 28 callbacks suppressed
Sep 17 10:46:22 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
Sep 17 10:51:06 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
Sep 17 10:51:12 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
Sep 17 10:52:41 p14s kernel: kauditd_printk_skb: 142 callbacks suppressed
Sep 17 10:54:35 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
Sep 17 11:00:19 p14s update-notifier[5442]: gtk_widget_get_scale_factor: assertion 'GTK_IS_WIDGET (widget)' failed
Sep 17 11:00:19 p14s update-notifier[5442]: gtk_widget_get_scale_factor: assertion 'GTK_IS_WIDGET (widget)' failed
Sep 17 11:02:52 p14s kernel: workqueue: pm_runtime_work hogged CPU for >13333us 5 times, consider switching to WQ_UNBOUND
Sep 17 11:51:14 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
Sep 17 12:00:32 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
Sep 17 12:21:04 p14s gdm-fingerprint][10438]: gkr-pam: no password is available for user
```

---

### 评论 #4 — isapir (2025-09-17T20:16:45Z)

This is the output of `journalctl -b -1 -p 0..4 --no-pager` (Black Screen Crash):

```
Sep 17 12:26:58 p14s kernel: i8042: Warning: Keylock active
Sep 17 12:26:58 p14s kernel: device-mapper: core: CONFIG_IMA_DISABLE_HTABLE is disabled. Duplicate IMA measurements will not be recorded in the IMA log.
Sep 17 12:26:58 p14s kernel: amdkcl: loading out-of-tree module taints kernel.
Sep 17 12:27:00 p14s kernel: Bluetooth: hci0: HCI Enhanced Setup Synchronous Connection command is advertised, but not supported.
Sep 17 12:27:00 p14s (uetoothd)[1772]: bluetooth.service: ConfigurationDirectory 'bluetooth' already exists but the mode is different. (File system: 755 ConfigurationDirectoryMode: 555)
Sep 17 12:27:00 p14s systemd[1]: Dependency failed for sssd-nss.socket - SSSD NSS Service responder socket.
Sep 17 12:27:00 p14s systemd[1]: Dependency failed for sssd-autofs.socket - SSSD AutoFS Service responder socket.
Sep 17 12:27:00 p14s systemd[1]: Dependency failed for sssd-pac.socket - SSSD PAC Service responder socket.
Sep 17 12:27:00 p14s systemd[1]: Dependency failed for sssd-pam-priv.socket - SSSD PAM Service responder private socket.
Sep 17 12:27:00 p14s systemd[1]: Dependency failed for sssd-pam.socket - SSSD PAM Service responder socket.
Sep 17 12:27:00 p14s systemd[1]: Dependency failed for sssd-ssh.socket - SSSD SSH Service responder socket.
Sep 17 12:27:00 p14s systemd[1]: Dependency failed for sssd-sudo.socket - SSSD Sudo Service responder socket.
Sep 17 12:27:00 p14s (cron)[1795]: cron.service: Referenced but unset environment variable evaluates to an empty string: EXTRA_OPTS
Sep 17 12:27:00 p14s bluetoothd[1772]: src/plugin.c:plugin_init() System does not support csip plugin
Sep 17 12:27:00 p14s bluetoothd[1772]: profiles/audio/micp.c:micp_init() D-Bus experimental not enabled
Sep 17 12:27:00 p14s bluetoothd[1772]: src/plugin.c:plugin_init() System does not support micp plugin
Sep 17 12:27:00 p14s bluetoothd[1772]: src/plugin.c:plugin_init() System does not support vcp plugin
Sep 17 12:27:00 p14s bluetoothd[1772]: src/plugin.c:plugin_init() System does not support mcp plugin
Sep 17 12:27:00 p14s bluetoothd[1772]: src/plugin.c:plugin_init() System does not support bass plugin
Sep 17 12:27:00 p14s bluetoothd[1772]: src/plugin.c:plugin_init() System does not support bap plugin
Sep 17 12:27:00 p14s gnome-remote-de[1776]: Init TPM credentials failed because Failed to initialize transmission interface context: tcti:IO failure, using GKeyFile as fallback
Sep 17 12:27:00 p14s kernel: nvme nvme0: using unchecked data buffer
Sep 17 12:27:00 p14s kernel: block nvme0n1: No UUID available providing old NGUID
Sep 17 12:27:00 p14s bluetoothd[1772]: profiles/sap/server.c:sap_server_register() Sap driver initialization failed.
Sep 17 12:27:00 p14s bluetoothd[1772]: sap-server: Operation not permitted (1)
Sep 17 12:27:00 p14s systemd[1]: Cannot find unit for notify message of PID 1921, ignoring.
Sep 17 12:27:00 p14s systemd[1]: Cannot find unit for notify message of PID 1949, ignoring.
Sep 17 12:27:00 p14s boltd[1954]: [92733804-004c-domain0                    ] udev: failed to determine if uid is stable: unknown NHI PCI id '0x151c'
Sep 17 12:27:00 p14s boltd[1954]: [92733804-014c-domain1                    ] udev: failed to determine if uid is stable: unknown NHI PCI id '0x151d'
Sep 17 12:27:01 p14s generate[1978]: Permissions for /etc/netplan/01-network-manager-all.yaml are too open. Netplan configuration should NOT be accessible by others.
Sep 17 12:27:01 p14s systemd[1]: Cannot find unit for notify message of PID 2059, ignoring.
Sep 17 12:27:02 p14s systemd[1]: Cannot find unit for notify message of PID 2224, ignoring.
Sep 17 12:27:05 p14s ModemManager[1930]: <wrn> [modem0] modem couldn't be initialized: eSIM without profiles detected
Sep 17 12:27:06 p14s wpa_supplicant[1840]: bgscan simple: Failed to enable signal strength monitoring
Sep 17 12:27:07 p14s systemd[1]: kerneloops.service: Found left-over process 2382 (kerneloops) in control group while starting unit. Ignoring.
Sep 17 12:27:07 p14s systemd[1]: kerneloops.service: This usually indicates unclean termination of a previous run, or service implementation deficiencies.
Sep 17 12:27:07 p14s (rneloops)[2384]: kerneloops.service: Referenced but unset environment variable evaluates to an empty string: DAEMON_ARGS
Sep 17 12:27:07 p14s kernel: kauditd_printk_skb: 181 callbacks suppressed
Sep 17 12:27:11 p14s gdm3[2146]: Gdm: on_display_added: assertion 'GDM_IS_REMOTE_DISPLAY (display)' failed
Sep 17 12:27:12 p14s pipewire[2714]: mod.jackdbus-detect: Failed to receive jackdbus reply: org.freedesktop.DBus.Error.ServiceUnknown: The name org.jackaudio.service was not provided by any .service files
Sep 17 12:27:12 p14s wireplumber[2717]: Failed to get percentage from UPower: org.freedesktop.DBus.Error.NameHasNoOwner
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Activating service name='org.freedesktop.systemd1' requested by ':1.2' (uid=120 pid=2746 comm="/usr/libexec/gnome-session-binary --autostart /usr" label="unconfined")
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Activated service 'org.freedesktop.systemd1' failed: Process org.freedesktop.systemd1 exited with status 1
Sep 17 12:27:12 p14s gnome-session-binary[2746]: WARNING: Could not check if unit gnome-session-wayland@gnome-login.target is active: Error calling StartServiceByName for org.freedesktop.systemd1: Process org.freedesktop.systemd1 exited with status 1
Sep 17 12:27:12 p14s wireplumber[2717]: Failed to create 'api.alsa.acp.device' device
Sep 17 12:27:12 p14s systemd[2702]: snap.snapd-desktop-integration.snapd-desktop-integration.service: Failed with result 'exit-code'.
Sep 17 12:27:12 p14s wireplumber[2717]: <WpPortalPermissionStorePlugin:0x5b530ec3f7b0> Failed to call Lookup: GDBus.Error:org.freedesktop.portal.Error.NotFound: No entry for camera
Sep 17 12:27:12 p14s wireplumber[2717]: <WpPortalPermissionStorePlugin:0x5b530ec3f7b0> Failed to call Lookup: GDBus.Error:org.freedesktop.portal.Error.NotFound: No entry for camera
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Activating service name='org.a11y.Bus' requested by ':1.4' (uid=120 pid=2799 comm="/usr/bin/gnome-shell" label="unconfined")
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Successfully activated service 'org.a11y.Bus'
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2882]: dbus-daemon[2882]: Activating service name='org.a11y.atspi.Registry' requested by ':1.0' (uid=120 pid=2799 comm="/usr/bin/gnome-shell" label="unconfined")
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2882]: dbus-daemon[2882]: Successfully activated service 'org.a11y.atspi.Registry'
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Activating service name='org.gnome.Shell.Screencast' requested by ':1.3' (uid=120 pid=2799 comm="/usr/bin/gnome-shell" label="unconfined")
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Activating service name='org.freedesktop.impl.portal.PermissionStore' requested by ':1.3' (uid=120 pid=2799 comm="/usr/bin/gnome-shell" label="unconfined")
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Successfully activated service 'org.freedesktop.impl.portal.PermissionStore'
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Activating service name='org.gnome.Shell.Notifications' requested by ':1.3' (uid=120 pid=2799 comm="/usr/bin/gnome-shell" label="unconfined")
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Successfully activated service 'org.gnome.Shell.Notifications'
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Activating service name='org.freedesktop.systemd1' requested by ':1.9' (uid=120 pid=2946 comm="/usr/libexec/gsd-sharing" label="unconfined")
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Activated service 'org.freedesktop.systemd1' failed: Process org.freedesktop.systemd1 exited with status 1
Sep 17 12:27:12 p14s gsd-sharing[2946]: Failed to StopUnit service: GDBus.Error:org.freedesktop.DBus.Error.Spawn.ChildExited: Process org.freedesktop.systemd1 exited with status 1
Sep 17 12:27:12 p14s gsd-sharing[2946]: Failed to StopUnit service: GDBus.Error:org.freedesktop.DBus.Error.Spawn.ChildExited: Process org.freedesktop.systemd1 exited with status 1
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Activating service name='org.freedesktop.portal.IBus' requested by ':1.25' (uid=120 pid=2993 comm="ibus-daemon --panel disable" label="unconfined")
Sep 17 12:27:12 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Successfully activated service 'org.freedesktop.portal.IBus'
Sep 17 12:27:13 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Successfully activated service 'org.gnome.Shell.Screencast'
Sep 17 12:27:13 p14s gsd-media-keys[2990]: Failed to grab accelerator for keybinding settings:playback-repeat
Sep 17 12:27:13 p14s gsd-media-keys[2990]: Failed to grab accelerator for keybinding settings:hibernate
Sep 17 12:27:13 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Activating service name='org.gnome.ScreenSaver' requested by ':1.24' (uid=120 pid=3030 comm="/usr/libexec/gsd-power" label="unconfined")
Sep 17 12:27:13 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Activating service name='org.freedesktop.portal.IBus' requested by ':1.34' (uid=120 pid=3209 comm="ibus-daemon --panel disable -r --xim" label="unconfined")
Sep 17 12:27:13 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Successfully activated service 'org.gnome.ScreenSaver'
Sep 17 12:27:13 p14s /usr/libexec/gdm-wayland-session[2743]: dbus-daemon[2743]: [session uid=120 pid=2743] Successfully activated service 'org.freedesktop.portal.IBus'
Sep 17 12:27:15 p14s ModemManager[1930]: <wrn> [modem0] couldn't load supported assistance data types: Failed to receive indication with the predicted orbits data source
Sep 17 12:27:16 p14s ModemManager[1930]: <wrn> [modem0] error initializing: Modem in failed state: esim-without-profiles
Sep 17 12:32:22 p14s gnome-shell[2799]: Page flip failed: Timer disarmed
Sep 17 12:52:34 p14s gdm-fingerprint][3368]: gkr-pam: no password is available for user
Sep 17 12:52:36 p14s gdm-password][3367]: gkr-pam: unable to locate daemon control file
Sep 17 12:52:36 p14s pipewire[3420]: mod.jackdbus-detect: Failed to receive jackdbus reply: org.freedesktop.DBus.Error.ServiceUnknown: The name org.jackaudio.service was not provided by any .service files
Sep 17 12:52:36 p14s wireplumber[3423]: <WpPortalPermissionStorePlugin:0x649f4c4960c0> Failed to call Lookup: GDBus.Error:org.freedesktop.portal.Error.NotFound: No entry for camera
Sep 17 12:52:36 p14s wireplumber[3423]: <WpPortalPermissionStorePlugin:0x649f4c4960c0> Failed to call Lookup: GDBus.Error:org.freedesktop.portal.Error.NotFound: No entry for camera
Sep 17 12:52:36 p14s gdm3[2146]: Gdm: on_display_added: assertion 'GDM_IS_REMOTE_DISPLAY (display)' failed
Sep 17 12:52:36 p14s gsd-media-keys[2990]: Unable to get default sink
Sep 17 12:52:36 p14s gsd-media-keys[2990]: Unable to get default source
Sep 17 12:52:36 p14s wireplumber[3423]: Failed to create 'api.alsa.acp.device' device
Sep 17 12:52:36 p14s gnome-keyring-daemon[3651]: discover_other_daemon: 1
Sep 17 12:52:36 p14s gnome-keyring-daemon[3654]: discover_other_daemon: 1
Sep 17 12:52:36 p14s systemd[3399]: app-gnome-gnome\x2dkeyring\x2dpkcs11-3644.scope: Failed to add PIDs to scope's control group: No such process
Sep 17 12:52:36 p14s systemd[3399]: app-gnome-gnome\x2dkeyring\x2dpkcs11-3644.scope: Failed with result 'resources'.
Sep 17 12:52:36 p14s systemd[3399]: Failed to start app-gnome-gnome\x2dkeyring\x2dpkcs11-3644.scope - Application launched by gnome-session-binary.
Sep 17 12:52:36 p14s systemd[3399]: app-gnome-gnome\x2dkeyring\x2dsecrets-3642.scope: No PIDs left to attach to the scope's control group, refusing.
Sep 17 12:52:36 p14s systemd[3399]: app-gnome-gnome\x2dkeyring\x2dsecrets-3642.scope: Failed with result 'resources'.
Sep 17 12:52:36 p14s systemd[3399]: Failed to start app-gnome-gnome\x2dkeyring\x2dsecrets-3642.scope - Application launched by gnome-session-binary.
Sep 17 12:52:36 p14s gnome-keyring-daemon[3655]: discover_other_daemon: 1
Sep 17 12:52:36 p14s systemd[3399]: app-gnome-xdg\x2duser\x2ddirs-3661.scope: No PIDs left to attach to the scope's control group, refusing.
Sep 17 12:52:36 p14s systemd[3399]: app-gnome-xdg\x2duser\x2ddirs-3661.scope: Failed with result 'resources'.
Sep 17 12:52:36 p14s systemd[3399]: Failed to start app-gnome-xdg\x2duser\x2ddirs-3661.scope - Application launched by gnome-session-binary.
Sep 17 12:52:37 p14s systemd[3399]: Dependency failed for org.gnome.SettingsDaemon.XSettings.service - GNOME XSettings service.
Sep 17 12:52:37 p14s gnome-shell[3659]: Gio.UnixInputStream has been moved to a separate platform-specific library. Please update your code to use GioUnix.InputStream instead.
                                        0 inhibit() ["resource:///org/gnome/shell/misc/loginManager.js":209:8]
                                        1 InterpretGeneratorResume() ["self-hosted":1461:33]
                                        2 AsyncFunctionNext() ["self-hosted":852:26]
                                        3 anonymous() ["resource:///org/gnome/shell/ui/init.js":21:19]
Sep 17 12:52:37 p14s at-spi2-registr[3769]: Failed to register client: GDBus.Error:org.gnome.SessionManager.AlreadyRegistered: Unable to register client
Sep 17 12:52:37 p14s at-spi2-registr[3769]: Unable to register client with session manager
Sep 17 12:52:37 p14s gnome-session-binary[3612]: GnomeDesktop-WARNING: Could not create transient scope for PID 3961: GDBus.Error:org.freedesktop.DBus.Error.UnixProcessIdUnknown: Failed to set unit properties: No such process
Sep 17 12:52:37 p14s systemd[3399]: app-gnome-user\x2ddirs\x2dupdate\x2dgtk-3946.scope: No PIDs left to attach to the scope's control group, refusing.
Sep 17 12:52:37 p14s systemd[3399]: app-gnome-user\x2ddirs\x2dupdate\x2dgtk-3946.scope: Failed with result 'resources'.
Sep 17 12:52:37 p14s systemd[3399]: Failed to start app-gnome-user\x2ddirs\x2dupdate\x2dgtk-3946.scope - Application launched by gnome-session-binary.
Sep 17 12:52:37 p14s gsd-media-keys[3820]: Failed to grab accelerator for keybinding settings:playback-repeat
Sep 17 12:52:37 p14s gsd-media-keys[3820]: Failed to grab accelerator for keybinding settings:hibernate
Sep 17 12:52:38 p14s gnome-shell[2799]: Connection to xwayland lost
Sep 17 12:52:38 p14s gnome-shell[2799]: Xwayland terminated, exiting since it was mandatory
Sep 17 12:52:38 p14s gnome-shell[2799]: JS ERROR: Gio.IOErrorEnum: Xwayland exited unexpectedly
                                        @resource:///org/gnome/shell/ui/init.js:21:20
Sep 17 12:52:38 p14s gdm3[2146]: Gdm: on_display_removed: assertion 'GDM_IS_REMOTE_DISPLAY (display)' failed
Sep 17 12:52:41 p14s gnome-shell[3659]: meta_window_set_stack_position_no_sync: assertion 'window->stack_position >= 0' failed
Sep 17 12:52:41 p14s io.snapcraft.Settings[4771]: userd.go:93: Starting snap userd
Sep 17 12:52:42 p14s kernel: kauditd_printk_skb: 68 callbacks suppressed
Sep 17 12:52:48 p14s systemd[2702]: xdg-permission-store.service: Failed with result 'exit-code'.
Sep 17 12:52:48 p14s systemd[2702]: xdg-document-portal.service: Failed with result 'exit-code'.
Sep 17 12:52:52 p14s kernel: kauditd_printk_skb: 66 callbacks suppressed
Sep 17 12:52:52 p14s tracker-miner-f[4167]: tracker_resource_set_relation: NULL is not a valid value.
Sep 17 12:54:43 p14s nautilus[5746]: Attempted to add a non-existent file to the view.
Sep 17 12:55:05 p14s nautilus[5746]: Attempted to add a non-existent file to the view.
Sep 17 12:55:15 p14s gnome-shell[3659]: meta_window_set_stack_position_no_sync: assertion 'window->stack_position >= 0' failed
Sep 17 12:56:04 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
Sep 17 12:57:42 p14s kernel: warning: `ThreadPoolForeg' uses wireless extensions which will stop working for Wi-Fi 7 hardware; use nl80211
Sep 17 12:57:43 p14s gnome-keyring-daemon[3428]: asked to register item /org/freedesktop/secrets/collection/login/1, but it's already registered
Sep 17 12:57:43 p14s gnome-keyring-d[3428]: asked to register item /org/freedesktop/secrets/collection/login/1, but it's already registered
Sep 17 13:03:55 p14s gnome-shell[3659]: meta_window_set_stack_position_no_sync: assertion 'window->stack_position >= 0' failed
Sep 17 13:07:08 p14s kernel: kauditd_printk_skb: 9 callbacks suppressed
```

---

### 评论 #5 — ppanchad-amd (2025-09-17T20:38:10Z)

Hi @isapir. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #6 — isapir (2025-09-17T21:14:58Z)

Thank you @ppanchad-amd 

Is there any other information that you need from me before I try to uninstall ROCm?

---

### 评论 #7 — harkgill-amd (2025-09-17T21:49:53Z)

Hi @isapir, could you try to uninstall just the kernel mode driver to try and narrow down which part of the installation is faulting?
```
sudo apt autoremove amdgpu-dkms
```
Let me know if you still see any crashes/black screen/pixelation after running this command and rebooting.

---

### 评论 #8 — isapir (2025-09-17T22:25:23Z)

> ```
> sudo apt autoremove amdgpu-dkms
> ```
> 
> Let me know if you still see any crashes/black screen/pixelation after running this command and rebooting.

@harkgill-amd - Done.  Since the crashes are random I will have to wait and see before I can tell if the crashes are gone.

---

### 评论 #9 — isapir (2025-09-17T23:25:18Z)

@harkgill-amd - Looks like removing `amdgpu-dkms` was sufficient to prevent the crashes.  It's only been an hour (playing YouTube music and running background processes) but earlier the system would crash within a few minutes without any load.

---

### 评论 #10 — isapir (2025-09-18T15:50:17Z)

@ppanchad-amd @harkgill-amd Removing `amdgpu-dkms` version `6.4.2.1` stopped the OS from crashing.

Is there an older version that is believed to be stable that I can try in the meantime or do you recommend that I wait?  If there is a stable older version, can you provide the steps to install it?  Thanks!

---

### 评论 #11 — harkgill-amd (2025-09-18T16:08:17Z)

@isapir, please proceed without `amdgpu-dkms`. You should have the inbox amdgpu kernel driver loaded which is recommended for  ROCm on Ryzen APUs. To confirm, could you share the output of `lsmod | grep amdgpu`  and `modinfo amdgpu`?

---

### 评论 #12 — isapir (2025-09-18T16:15:19Z)

@harkgill-amd I would like to use ROCm with Ollama and other LLM workloads.  Is `amdgpu-dkms` not required for that?

Output of `lsmod | grep amdgpu`:
```
amdgpu              19722240  28
amdxcp                 12288  1 amdgpu
drm_panel_backlight_quirks    12288  1 amdgpu
drm_buddy              24576  1 amdgpu
drm_ttm_helper         16384  1 amdgpu
ttm                   118784  2 amdgpu,drm_ttm_helper
drm_exec               12288  1 amdgpu
drm_suballoc_helper    20480  1 amdgpu
drm_display_helper    278528  1 amdgpu
cec                    94208  2 drm_display_helper,amdgpu
gpu_sched              61440  2 amdxdna,amdgpu
i2c_algo_bit           16384  1 amdgpu
video                  77824  2 thinkpad_acpi,amdgpu
```

Output of `modinfo amdgpu`:
```
filename:       /lib/modules/6.14.0-29-generic/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu.ko.zst
license:        GPL and additional rights
description:    AMD GPU
author:         AMD linux driver team
firmware:       amdgpu/navi12_gpu_info.bin
firmware:       amdgpu/arcturus_gpu_info.bin
firmware:       amdgpu/raven2_gpu_info.bin
firmware:       amdgpu/picasso_gpu_info.bin
firmware:       amdgpu/raven_gpu_info.bin
firmware:       amdgpu/vega12_gpu_info.bin
firmware:       amdgpu/vega10_gpu_info.bin
import_ns:      DMA_BUF
firmware:       amdgpu/ip_discovery.bin
firmware:       amdgpu/mullins_mec.bin
firmware:       amdgpu/mullins_rlc.bin
firmware:       amdgpu/mullins_ce.bin
firmware:       amdgpu/mullins_me.bin
firmware:       amdgpu/mullins_pfp.bin
firmware:       amdgpu/kabini_mec.bin
firmware:       amdgpu/kabini_rlc.bin
firmware:       amdgpu/kabini_ce.bin
firmware:       amdgpu/kabini_me.bin
firmware:       amdgpu/kabini_pfp.bin
firmware:       amdgpu/kaveri_mec2.bin
firmware:       amdgpu/kaveri_mec.bin
firmware:       amdgpu/kaveri_rlc.bin
firmware:       amdgpu/kaveri_ce.bin
firmware:       amdgpu/kaveri_me.bin
firmware:       amdgpu/kaveri_pfp.bin
firmware:       amdgpu/hawaii_mec.bin
firmware:       amdgpu/hawaii_rlc.bin
firmware:       amdgpu/hawaii_ce.bin
firmware:       amdgpu/hawaii_me.bin
firmware:       amdgpu/hawaii_pfp.bin
firmware:       amdgpu/bonaire_mec.bin
firmware:       amdgpu/bonaire_rlc.bin
firmware:       amdgpu/bonaire_ce.bin
firmware:       amdgpu/bonaire_me.bin
firmware:       amdgpu/bonaire_pfp.bin
firmware:       amdgpu/mullins_sdma1.bin
firmware:       amdgpu/mullins_sdma.bin
firmware:       amdgpu/kabini_sdma1.bin
firmware:       amdgpu/kabini_sdma.bin
firmware:       amdgpu/kaveri_sdma1.bin
firmware:       amdgpu/kaveri_sdma.bin
firmware:       amdgpu/hawaii_sdma1.bin
firmware:       amdgpu/hawaii_sdma.bin
firmware:       amdgpu/bonaire_sdma1.bin
firmware:       amdgpu/bonaire_sdma.bin
firmware:       amdgpu/si58_mc.bin
firmware:       amdgpu/hainan_mc.bin
firmware:       amdgpu/oland_mc.bin
firmware:       amdgpu/verde_mc.bin
firmware:       amdgpu/pitcairn_mc.bin
firmware:       amdgpu/tahiti_mc.bin
firmware:       amdgpu/hainan_rlc.bin
firmware:       amdgpu/hainan_ce.bin
firmware:       amdgpu/hainan_me.bin
firmware:       amdgpu/hainan_pfp.bin
firmware:       amdgpu/oland_rlc.bin
firmware:       amdgpu/oland_ce.bin
firmware:       amdgpu/oland_me.bin
firmware:       amdgpu/oland_pfp.bin
firmware:       amdgpu/verde_rlc.bin
firmware:       amdgpu/verde_ce.bin
firmware:       amdgpu/verde_me.bin
firmware:       amdgpu/verde_pfp.bin
firmware:       amdgpu/pitcairn_rlc.bin
firmware:       amdgpu/pitcairn_ce.bin
firmware:       amdgpu/pitcairn_me.bin
firmware:       amdgpu/pitcairn_pfp.bin
firmware:       amdgpu/tahiti_rlc.bin
firmware:       amdgpu/tahiti_ce.bin
firmware:       amdgpu/tahiti_me.bin
firmware:       amdgpu/tahiti_pfp.bin
firmware:       amdgpu/topaz_mc.bin
firmware:       amdgpu/hawaii_mc.bin
firmware:       amdgpu/bonaire_mc.bin
firmware:       amdgpu/polaris12_k_mc.bin
firmware:       amdgpu/polaris10_k_mc.bin
firmware:       amdgpu/polaris11_k_mc.bin
firmware:       amdgpu/polaris12_32_mc.bin
firmware:       amdgpu/polaris12_mc.bin
firmware:       amdgpu/polaris10_mc.bin
firmware:       amdgpu/polaris11_mc.bin
firmware:       amdgpu/tonga_mc.bin
firmware:       amdgpu/vega12_asd.bin
firmware:       amdgpu/vega12_sos.bin
firmware:       amdgpu/vega10_cap.bin
firmware:       amdgpu/vega10_asd.bin
firmware:       amdgpu/vega10_sos.bin
firmware:       amdgpu/raven_ta.bin
firmware:       amdgpu/raven2_ta.bin
firmware:       amdgpu/picasso_ta.bin
firmware:       amdgpu/raven2_asd.bin
firmware:       amdgpu/picasso_asd.bin
firmware:       amdgpu/raven_asd.bin
firmware:       amdgpu/beige_goby_ta.bin
firmware:       amdgpu/beige_goby_sos.bin
firmware:       amdgpu/dimgrey_cavefish_ta.bin
firmware:       amdgpu/dimgrey_cavefish_sos.bin
firmware:       amdgpu/vangogh_toc.bin
firmware:       amdgpu/vangogh_asd.bin
firmware:       amdgpu/navy_flounder_ta.bin
firmware:       amdgpu/navy_flounder_sos.bin
firmware:       amdgpu/sienna_cichlid_cap.bin
firmware:       amdgpu/sienna_cichlid_ta.bin
firmware:       amdgpu/sienna_cichlid_sos.bin
firmware:       amdgpu/arcturus_ta.bin
firmware:       amdgpu/arcturus_asd.bin
firmware:       amdgpu/arcturus_sos.bin
firmware:       amdgpu/navi12_cap.bin
firmware:       amdgpu/navi12_ta.bin
firmware:       amdgpu/navi12_asd.bin
firmware:       amdgpu/navi12_sos.bin
firmware:       amdgpu/navi14_ta.bin
firmware:       amdgpu/navi14_asd.bin
firmware:       amdgpu/navi14_sos.bin
firmware:       amdgpu/navi10_ta.bin
firmware:       amdgpu/navi10_asd.bin
firmware:       amdgpu/navi10_sos.bin
firmware:       amdgpu/vega20_ta.bin
firmware:       amdgpu/vega20_asd.bin
firmware:       amdgpu/vega20_sos.bin
firmware:       amdgpu/green_sardine_ta.bin
firmware:       amdgpu/green_sardine_asd.bin
firmware:       amdgpu/renoir_ta.bin
firmware:       amdgpu/renoir_asd.bin
firmware:       amdgpu/psp_14_0_4_ta.bin
firmware:       amdgpu/psp_14_0_4_toc.bin
firmware:       amdgpu/psp_14_0_1_ta.bin
firmware:       amdgpu/psp_14_0_1_toc.bin
firmware:       amdgpu/psp_14_0_0_ta.bin
firmware:       amdgpu/psp_14_0_0_toc.bin
firmware:       amdgpu/psp_13_0_14_ta.bin
firmware:       amdgpu/psp_13_0_14_sos.bin
firmware:       amdgpu/psp_13_0_12_ta.bin
firmware:       amdgpu/psp_13_0_12_sos.bin
firmware:       amdgpu/psp_13_0_6_ta.bin
firmware:       amdgpu/psp_13_0_6_sos.bin
firmware:       amdgpu/psp_13_0_11_ta.bin
firmware:       amdgpu/psp_13_0_11_toc.bin
firmware:       amdgpu/psp_13_0_10_ta.bin
firmware:       amdgpu/psp_13_0_10_sos.bin
firmware:       amdgpu/psp_13_0_7_ta.bin
firmware:       amdgpu/psp_13_0_7_sos.bin
firmware:       amdgpu/psp_13_0_0_ta.bin
firmware:       amdgpu/psp_13_0_0_sos.bin
firmware:       amdgpu/psp_13_0_8_ta.bin
firmware:       amdgpu/psp_13_0_8_toc.bin
firmware:       amdgpu/psp_13_0_5_ta.bin
firmware:       amdgpu/psp_13_0_5_toc.bin
firmware:       amdgpu/yellow_carp_ta.bin
firmware:       amdgpu/yellow_carp_toc.bin
firmware:       amdgpu/aldebaran_cap.bin
firmware:       amdgpu/aldebaran_ta.bin
firmware:       amdgpu/aldebaran_sos.bin
firmware:       amdgpu/psp_13_0_4_ta.bin
firmware:       amdgpu/psp_13_0_4_toc.bin
firmware:       amdgpu/psp_14_0_3_ta.bin
firmware:       amdgpu/psp_14_0_3_sos.bin
firmware:       amdgpu/psp_14_0_2_ta.bin
firmware:       amdgpu/psp_14_0_2_sos.bin
firmware:       amdgpu/vegam_rlc.bin
firmware:       amdgpu/vegam_mec2.bin
firmware:       amdgpu/vegam_mec.bin
firmware:       amdgpu/vegam_me.bin
firmware:       amdgpu/vegam_pfp.bin
firmware:       amdgpu/vegam_ce.bin
firmware:       amdgpu/polaris12_rlc.bin
firmware:       amdgpu/polaris12_mec2_2.bin
firmware:       amdgpu/polaris12_mec2.bin
firmware:       amdgpu/polaris12_mec_2.bin
firmware:       amdgpu/polaris12_mec.bin
firmware:       amdgpu/polaris12_me_2.bin
firmware:       amdgpu/polaris12_me.bin
firmware:       amdgpu/polaris12_pfp_2.bin
firmware:       amdgpu/polaris12_pfp.bin
firmware:       amdgpu/polaris12_ce_2.bin
firmware:       amdgpu/polaris12_ce.bin
firmware:       amdgpu/polaris11_rlc.bin
firmware:       amdgpu/polaris11_mec2_2.bin
firmware:       amdgpu/polaris11_mec2.bin
firmware:       amdgpu/polaris11_mec_2.bin
firmware:       amdgpu/polaris11_mec.bin
firmware:       amdgpu/polaris11_me_2.bin
firmware:       amdgpu/polaris11_me.bin
firmware:       amdgpu/polaris11_pfp_2.bin
firmware:       amdgpu/polaris11_pfp.bin
firmware:       amdgpu/polaris11_ce_2.bin
firmware:       amdgpu/polaris11_ce.bin
firmware:       amdgpu/polaris10_rlc.bin
firmware:       amdgpu/polaris10_mec2_2.bin
firmware:       amdgpu/polaris10_mec2.bin
firmware:       amdgpu/polaris10_mec_2.bin
firmware:       amdgpu/polaris10_mec.bin
firmware:       amdgpu/polaris10_me_2.bin
firmware:       amdgpu/polaris10_me.bin
firmware:       amdgpu/polaris10_pfp_2.bin
firmware:       amdgpu/polaris10_pfp.bin
firmware:       amdgpu/polaris10_ce_2.bin
firmware:       amdgpu/polaris10_ce.bin
firmware:       amdgpu/fiji_rlc.bin
firmware:       amdgpu/fiji_mec2.bin
firmware:       amdgpu/fiji_mec.bin
firmware:       amdgpu/fiji_me.bin
firmware:       amdgpu/fiji_pfp.bin
firmware:       amdgpu/fiji_ce.bin
firmware:       amdgpu/topaz_rlc.bin
firmware:       amdgpu/topaz_mec.bin
firmware:       amdgpu/topaz_me.bin
firmware:       amdgpu/topaz_pfp.bin
firmware:       amdgpu/topaz_ce.bin
firmware:       amdgpu/tonga_rlc.bin
firmware:       amdgpu/tonga_mec2.bin
firmware:       amdgpu/tonga_mec.bin
firmware:       amdgpu/tonga_me.bin
firmware:       amdgpu/tonga_pfp.bin
firmware:       amdgpu/tonga_ce.bin
firmware:       amdgpu/stoney_rlc.bin
firmware:       amdgpu/stoney_mec.bin
firmware:       amdgpu/stoney_me.bin
firmware:       amdgpu/stoney_pfp.bin
firmware:       amdgpu/stoney_ce.bin
firmware:       amdgpu/carrizo_rlc.bin
firmware:       amdgpu/carrizo_mec2.bin
firmware:       amdgpu/carrizo_mec.bin
firmware:       amdgpu/carrizo_me.bin
firmware:       amdgpu/carrizo_pfp.bin
firmware:       amdgpu/carrizo_ce.bin
firmware:       amdgpu/aldebaran_sjt_mec2.bin
firmware:       amdgpu/aldebaran_sjt_mec.bin
firmware:       amdgpu/aldebaran_rlc.bin
firmware:       amdgpu/aldebaran_mec2.bin
firmware:       amdgpu/aldebaran_mec.bin
firmware:       amdgpu/green_sardine_rlc.bin
firmware:       amdgpu/green_sardine_mec2.bin
firmware:       amdgpu/green_sardine_mec.bin
firmware:       amdgpu/green_sardine_me.bin
firmware:       amdgpu/green_sardine_pfp.bin
firmware:       amdgpu/green_sardine_ce.bin
firmware:       amdgpu/renoir_rlc.bin
firmware:       amdgpu/renoir_mec.bin
firmware:       amdgpu/renoir_me.bin
firmware:       amdgpu/renoir_pfp.bin
firmware:       amdgpu/renoir_ce.bin
firmware:       amdgpu/arcturus_rlc.bin
firmware:       amdgpu/arcturus_mec.bin
firmware:       amdgpu/raven_kicker_rlc.bin
firmware:       amdgpu/raven2_rlc.bin
firmware:       amdgpu/raven2_mec2.bin
firmware:       amdgpu/raven2_mec.bin
firmware:       amdgpu/raven2_me.bin
firmware:       amdgpu/raven2_pfp.bin
firmware:       amdgpu/raven2_ce.bin
firmware:       amdgpu/picasso_rlc_am4.bin
firmware:       amdgpu/picasso_rlc.bin
firmware:       amdgpu/picasso_mec2.bin
firmware:       amdgpu/picasso_mec.bin
firmware:       amdgpu/picasso_me.bin
firmware:       amdgpu/picasso_pfp.bin
firmware:       amdgpu/picasso_ce.bin
firmware:       amdgpu/raven_rlc.bin
firmware:       amdgpu/raven_mec2.bin
firmware:       amdgpu/raven_mec.bin
firmware:       amdgpu/raven_me.bin
firmware:       amdgpu/raven_pfp.bin
firmware:       amdgpu/raven_ce.bin
firmware:       amdgpu/vega20_rlc.bin
firmware:       amdgpu/vega20_mec2.bin
firmware:       amdgpu/vega20_mec.bin
firmware:       amdgpu/vega20_me.bin
firmware:       amdgpu/vega20_pfp.bin
firmware:       amdgpu/vega20_ce.bin
firmware:       amdgpu/vega12_rlc.bin
firmware:       amdgpu/vega12_mec2.bin
firmware:       amdgpu/vega12_mec.bin
firmware:       amdgpu/vega12_me.bin
firmware:       amdgpu/vega12_pfp.bin
firmware:       amdgpu/vega12_ce.bin
firmware:       amdgpu/vega10_rlc.bin
firmware:       amdgpu/vega10_mec2.bin
firmware:       amdgpu/vega10_mec.bin
firmware:       amdgpu/vega10_me.bin
firmware:       amdgpu/vega10_pfp.bin
firmware:       amdgpu/vega10_ce.bin
firmware:       amdgpu/gc_9_4_4_sjt_mec.bin
firmware:       amdgpu/gc_9_4_3_sjt_mec.bin
firmware:       amdgpu/gc_9_5_0_rlc.bin
firmware:       amdgpu/gc_9_4_4_rlc.bin
firmware:       amdgpu/gc_9_4_3_rlc.bin
firmware:       amdgpu/gc_9_5_0_mec.bin
firmware:       amdgpu/gc_9_4_4_mec.bin
firmware:       amdgpu/gc_9_4_3_mec.bin
firmware:       amdgpu/gc_10_3_7_rlc.bin
firmware:       amdgpu/gc_10_3_7_mec2.bin
firmware:       amdgpu/gc_10_3_7_mec.bin
firmware:       amdgpu/gc_10_3_7_me.bin
firmware:       amdgpu/gc_10_3_7_pfp.bin
firmware:       amdgpu/gc_10_3_7_ce.bin
firmware:       amdgpu/gc_10_3_6_rlc.bin
firmware:       amdgpu/gc_10_3_6_mec2.bin
firmware:       amdgpu/gc_10_3_6_mec.bin
firmware:       amdgpu/gc_10_3_6_me.bin
firmware:       amdgpu/gc_10_3_6_pfp.bin
firmware:       amdgpu/gc_10_3_6_ce.bin
firmware:       amdgpu/cyan_skillfish2_rlc.bin
firmware:       amdgpu/cyan_skillfish2_mec2.bin
firmware:       amdgpu/cyan_skillfish2_mec.bin
firmware:       amdgpu/cyan_skillfish2_me.bin
firmware:       amdgpu/cyan_skillfish2_pfp.bin
firmware:       amdgpu/cyan_skillfish2_ce.bin
firmware:       amdgpu/yellow_carp_rlc.bin
firmware:       amdgpu/yellow_carp_mec2.bin
firmware:       amdgpu/yellow_carp_mec.bin
firmware:       amdgpu/yellow_carp_me.bin
firmware:       amdgpu/yellow_carp_pfp.bin
firmware:       amdgpu/yellow_carp_ce.bin
firmware:       amdgpu/beige_goby_rlc.bin
firmware:       amdgpu/beige_goby_mec2.bin
firmware:       amdgpu/beige_goby_mec.bin
firmware:       amdgpu/beige_goby_me.bin
firmware:       amdgpu/beige_goby_pfp.bin
firmware:       amdgpu/beige_goby_ce.bin
firmware:       amdgpu/dimgrey_cavefish_rlc.bin
firmware:       amdgpu/dimgrey_cavefish_mec2.bin
firmware:       amdgpu/dimgrey_cavefish_mec.bin
firmware:       amdgpu/dimgrey_cavefish_me.bin
firmware:       amdgpu/dimgrey_cavefish_pfp.bin
firmware:       amdgpu/dimgrey_cavefish_ce.bin
firmware:       amdgpu/vangogh_rlc.bin
firmware:       amdgpu/vangogh_mec2.bin
firmware:       amdgpu/vangogh_mec.bin
firmware:       amdgpu/vangogh_me.bin
firmware:       amdgpu/vangogh_pfp.bin
firmware:       amdgpu/vangogh_ce.bin
firmware:       amdgpu/navy_flounder_rlc.bin
firmware:       amdgpu/navy_flounder_mec2.bin
firmware:       amdgpu/navy_flounder_mec.bin
firmware:       amdgpu/navy_flounder_me.bin
firmware:       amdgpu/navy_flounder_pfp.bin
firmware:       amdgpu/navy_flounder_ce.bin
firmware:       amdgpu/sienna_cichlid_rlc.bin
firmware:       amdgpu/sienna_cichlid_mec2.bin
firmware:       amdgpu/sienna_cichlid_mec.bin
firmware:       amdgpu/sienna_cichlid_me.bin
firmware:       amdgpu/sienna_cichlid_pfp.bin
firmware:       amdgpu/sienna_cichlid_ce.bin
firmware:       amdgpu/navi12_rlc.bin
firmware:       amdgpu/navi12_mec2.bin
firmware:       amdgpu/navi12_mec.bin
firmware:       amdgpu/navi12_me.bin
firmware:       amdgpu/navi12_pfp.bin
firmware:       amdgpu/navi12_ce.bin
firmware:       amdgpu/navi14_rlc.bin
firmware:       amdgpu/navi14_mec2.bin
firmware:       amdgpu/navi14_mec.bin
firmware:       amdgpu/navi14_me.bin
firmware:       amdgpu/navi14_pfp.bin
firmware:       amdgpu/navi14_ce.bin
firmware:       amdgpu/navi14_mec2_wks.bin
firmware:       amdgpu/navi14_mec_wks.bin
firmware:       amdgpu/navi14_me_wks.bin
firmware:       amdgpu/navi14_pfp_wks.bin
firmware:       amdgpu/navi14_ce_wks.bin
firmware:       amdgpu/navi10_rlc.bin
firmware:       amdgpu/navi10_mec2.bin
firmware:       amdgpu/navi10_mec.bin
firmware:       amdgpu/navi10_me.bin
firmware:       amdgpu/navi10_pfp.bin
firmware:       amdgpu/navi10_ce.bin
firmware:       amdgpu/gc_11_5_2_imu.bin
firmware:       amdgpu/gc_11_5_1_imu.bin
firmware:       amdgpu/gc_11_5_0_imu.bin
firmware:       amdgpu/gc_11_0_4_imu.bin
firmware:       amdgpu/gc_11_0_3_imu.bin
firmware:       amdgpu/gc_11_0_2_imu.bin
firmware:       amdgpu/gc_11_0_1_imu.bin
firmware:       amdgpu/gc_11_0_0_imu.bin
firmware:       amdgpu/gc_11_5_2_rlc.bin
firmware:       amdgpu/gc_11_5_2_mec.bin
firmware:       amdgpu/gc_11_5_2_me.bin
firmware:       amdgpu/gc_11_5_2_pfp.bin
firmware:       amdgpu/gc_11_5_1_rlc.bin
firmware:       amdgpu/gc_11_5_1_mec.bin
firmware:       amdgpu/gc_11_5_1_me.bin
firmware:       amdgpu/gc_11_5_1_pfp.bin
firmware:       amdgpu/gc_11_5_0_rlc.bin
firmware:       amdgpu/gc_11_5_0_mec.bin
firmware:       amdgpu/gc_11_5_0_me.bin
firmware:       amdgpu/gc_11_5_0_pfp.bin
firmware:       amdgpu/gc_11_0_4_rlc.bin
firmware:       amdgpu/gc_11_0_4_mec.bin
firmware:       amdgpu/gc_11_0_4_me.bin
firmware:       amdgpu/gc_11_0_4_pfp.bin
firmware:       amdgpu/gc_11_0_3_rlc.bin
firmware:       amdgpu/gc_11_0_3_mec.bin
firmware:       amdgpu/gc_11_0_3_me.bin
firmware:       amdgpu/gc_11_0_3_pfp.bin
firmware:       amdgpu/gc_11_0_2_rlc.bin
firmware:       amdgpu/gc_11_0_2_mec.bin
firmware:       amdgpu/gc_11_0_2_me.bin
firmware:       amdgpu/gc_11_0_2_pfp.bin
firmware:       amdgpu/gc_11_0_1_rlc.bin
firmware:       amdgpu/gc_11_0_1_mec.bin
firmware:       amdgpu/gc_11_0_1_me.bin
firmware:       amdgpu/gc_11_0_1_pfp.bin
firmware:       amdgpu/gc_11_0_0_toc.bin
firmware:       amdgpu/gc_11_0_0_rlc_1.bin
firmware:       amdgpu/gc_11_0_0_rlc.bin
firmware:       amdgpu/gc_11_0_0_mec.bin
firmware:       amdgpu/gc_11_0_0_me.bin
firmware:       amdgpu/gc_11_0_0_pfp.bin
firmware:       amdgpu/gc_12_0_1_toc.bin
firmware:       amdgpu/gc_12_0_1_rlc.bin
firmware:       amdgpu/gc_12_0_1_mec.bin
firmware:       amdgpu/gc_12_0_1_me.bin
firmware:       amdgpu/gc_12_0_1_pfp.bin
firmware:       amdgpu/gc_12_0_0_toc.bin
firmware:       amdgpu/gc_12_0_0_rlc.bin
firmware:       amdgpu/gc_12_0_0_mec.bin
firmware:       amdgpu/gc_12_0_0_me.bin
firmware:       amdgpu/gc_12_0_0_pfp.bin
firmware:       amdgpu/gc_12_0_1_imu.bin
firmware:       amdgpu/gc_12_0_0_imu.bin
firmware:       amdgpu/topaz_sdma1.bin
firmware:       amdgpu/topaz_sdma.bin
firmware:       amdgpu/vegam_sdma1.bin
firmware:       amdgpu/vegam_sdma.bin
firmware:       amdgpu/polaris12_sdma1.bin
firmware:       amdgpu/polaris12_sdma.bin
firmware:       amdgpu/polaris11_sdma1.bin
firmware:       amdgpu/polaris11_sdma.bin
firmware:       amdgpu/polaris10_sdma1.bin
firmware:       amdgpu/polaris10_sdma.bin
firmware:       amdgpu/stoney_sdma.bin
firmware:       amdgpu/fiji_sdma1.bin
firmware:       amdgpu/fiji_sdma.bin
firmware:       amdgpu/carrizo_sdma1.bin
firmware:       amdgpu/carrizo_sdma.bin
firmware:       amdgpu/tonga_sdma1.bin
firmware:       amdgpu/tonga_sdma.bin
firmware:       amdgpu/aldebaran_sdma.bin
firmware:       amdgpu/green_sardine_sdma.bin
firmware:       amdgpu/renoir_sdma.bin
firmware:       amdgpu/arcturus_sdma.bin
firmware:       amdgpu/raven2_sdma.bin
firmware:       amdgpu/picasso_sdma.bin
firmware:       amdgpu/raven_sdma.bin
firmware:       amdgpu/vega20_sdma1.bin
firmware:       amdgpu/vega20_sdma.bin
firmware:       amdgpu/vega12_sdma1.bin
firmware:       amdgpu/vega12_sdma.bin
firmware:       amdgpu/vega10_sdma1.bin
firmware:       amdgpu/vega10_sdma.bin
firmware:       amdgpu/sdma_4_4_5.bin
firmware:       amdgpu/sdma_4_4_2.bin
firmware:       amdgpu/cyan_skillfish2_sdma1.bin
firmware:       amdgpu/cyan_skillfish2_sdma.bin
firmware:       amdgpu/navi12_sdma1.bin
firmware:       amdgpu/navi12_sdma.bin
firmware:       amdgpu/navi14_sdma1.bin
firmware:       amdgpu/navi14_sdma.bin
firmware:       amdgpu/navi10_sdma1.bin
firmware:       amdgpu/navi10_sdma.bin
firmware:       amdgpu/sdma_5_2_7.bin
firmware:       amdgpu/sdma_5_2_6.bin
firmware:       amdgpu/yellow_carp_sdma.bin
firmware:       amdgpu/vangogh_sdma.bin
firmware:       amdgpu/beige_goby_sdma.bin
firmware:       amdgpu/dimgrey_cavefish_sdma.bin
firmware:       amdgpu/navy_flounder_sdma.bin
firmware:       amdgpu/sienna_cichlid_sdma.bin
firmware:       amdgpu/sdma_6_1_2.bin
firmware:       amdgpu/sdma_6_1_1.bin
firmware:       amdgpu/sdma_6_1_0.bin
firmware:       amdgpu/sdma_6_0_3.bin
firmware:       amdgpu/sdma_6_0_2.bin
firmware:       amdgpu/sdma_6_0_1.bin
firmware:       amdgpu/sdma_6_0_0.bin
firmware:       amdgpu/sdma_7_0_1.bin
firmware:       amdgpu/sdma_7_0_0.bin
firmware:       amdgpu/gc_11_5_2_mes1.bin
firmware:       amdgpu/gc_11_5_2_mes_2.bin
firmware:       amdgpu/gc_11_5_1_mes1.bin
firmware:       amdgpu/gc_11_5_1_mes_2.bin
firmware:       amdgpu/gc_11_5_0_mes1.bin
firmware:       amdgpu/gc_11_5_0_mes_2.bin
firmware:       amdgpu/gc_11_0_4_mes1.bin
firmware:       amdgpu/gc_11_0_4_mes_2.bin
firmware:       amdgpu/gc_11_0_4_mes.bin
firmware:       amdgpu/gc_11_0_3_mes1.bin
firmware:       amdgpu/gc_11_0_3_mes_2.bin
firmware:       amdgpu/gc_11_0_3_mes.bin
firmware:       amdgpu/gc_11_0_2_mes1.bin
firmware:       amdgpu/gc_11_0_2_mes_2.bin
firmware:       amdgpu/gc_11_0_2_mes.bin
firmware:       amdgpu/gc_11_0_1_mes1.bin
firmware:       amdgpu/gc_11_0_1_mes_2.bin
firmware:       amdgpu/gc_11_0_1_mes.bin
firmware:       amdgpu/gc_11_0_0_mes1.bin
firmware:       amdgpu/gc_11_0_0_mes_2.bin
firmware:       amdgpu/gc_11_0_0_mes.bin
firmware:       amdgpu/gc_12_0_1_uni_mes.bin
firmware:       amdgpu/gc_12_0_1_mes1.bin
firmware:       amdgpu/gc_12_0_1_mes.bin
firmware:       amdgpu/gc_12_0_0_uni_mes.bin
firmware:       amdgpu/gc_12_0_0_mes1.bin
firmware:       amdgpu/gc_12_0_0_mes.bin
firmware:       amdgpu/vega20_uvd.bin
firmware:       amdgpu/vega12_uvd.bin
firmware:       amdgpu/vega10_uvd.bin
firmware:       amdgpu/vegam_uvd.bin
firmware:       amdgpu/polaris12_uvd.bin
firmware:       amdgpu/polaris11_uvd.bin
firmware:       amdgpu/polaris10_uvd.bin
firmware:       amdgpu/stoney_uvd.bin
firmware:       amdgpu/fiji_uvd.bin
firmware:       amdgpu/carrizo_uvd.bin
firmware:       amdgpu/tonga_uvd.bin
firmware:       amdgpu/mullins_uvd.bin
firmware:       amdgpu/hawaii_uvd.bin
firmware:       amdgpu/kaveri_uvd.bin
firmware:       amdgpu/kabini_uvd.bin
firmware:       amdgpu/bonaire_uvd.bin
firmware:       amdgpu/oland_uvd.bin
firmware:       amdgpu/pitcairn_uvd.bin
firmware:       amdgpu/verde_uvd.bin
firmware:       amdgpu/tahiti_uvd.bin
firmware:       amdgpu/vega20_vce.bin
firmware:       amdgpu/vega12_vce.bin
firmware:       amdgpu/vega10_vce.bin
firmware:       amdgpu/vegam_vce.bin
firmware:       amdgpu/polaris12_vce.bin
firmware:       amdgpu/polaris11_vce.bin
firmware:       amdgpu/polaris10_vce.bin
firmware:       amdgpu/stoney_vce.bin
firmware:       amdgpu/fiji_vce.bin
firmware:       amdgpu/carrizo_vce.bin
firmware:       amdgpu/tonga_vce.bin
firmware:       amdgpu/mullins_vce.bin
firmware:       amdgpu/hawaii_vce.bin
firmware:       amdgpu/kaveri_vce.bin
firmware:       amdgpu/kabini_vce.bin
firmware:       amdgpu/bonaire_vce.bin
firmware:       amdgpu/vcn_5_0_1.bin
firmware:       amdgpu/vcn_5_0_0.bin
firmware:       amdgpu/vcn_4_0_6_1.bin
firmware:       amdgpu/vcn_4_0_6.bin
firmware:       amdgpu/vcn_4_0_5.bin
firmware:       amdgpu/vcn_4_0_4.bin
firmware:       amdgpu/vcn_4_0_3.bin
firmware:       amdgpu/vcn_4_0_2.bin
firmware:       amdgpu/vcn_4_0_0.bin
firmware:       amdgpu/vcn_3_1_2.bin
firmware:       amdgpu/yellow_carp_vcn.bin
firmware:       amdgpu/beige_goby_vcn.bin
firmware:       amdgpu/dimgrey_cavefish_vcn.bin
firmware:       amdgpu/vangogh_vcn.bin
firmware:       amdgpu/navy_flounder_vcn.bin
firmware:       amdgpu/sienna_cichlid_vcn.bin
firmware:       amdgpu/navi12_vcn.bin
firmware:       amdgpu/navi14_vcn.bin
firmware:       amdgpu/navi10_vcn.bin
firmware:       amdgpu/aldebaran_vcn.bin
firmware:       amdgpu/green_sardine_vcn.bin
firmware:       amdgpu/renoir_vcn.bin
firmware:       amdgpu/arcturus_vcn.bin
firmware:       amdgpu/raven2_vcn.bin
firmware:       amdgpu/picasso_vcn.bin
firmware:       amdgpu/raven_vcn.bin
firmware:       amdgpu/vpe_6_1_3.bin
firmware:       amdgpu/vpe_6_1_1.bin
firmware:       amdgpu/vpe_6_1_0.bin
firmware:       amdgpu/umsch_mm_4_0_0.bin
firmware:       amdgpu/beige_goby_smc.bin
firmware:       amdgpu/dimgrey_cavefish_smc.bin
firmware:       amdgpu/navy_flounder_smc.bin
firmware:       amdgpu/sienna_cichlid_smc.bin
firmware:       amdgpu/navi12_smc.bin
firmware:       amdgpu/navi14_smc.bin
firmware:       amdgpu/navi10_smc.bin
firmware:       amdgpu/arcturus_smc.bin
firmware:       amdgpu/smu_13_0_10.bin
firmware:       amdgpu/smu_13_0_7.bin
firmware:       amdgpu/smu_13_0_0.bin
firmware:       amdgpu/aldebaran_smc.bin
firmware:       amdgpu/smu_13_0_14.bin
firmware:       amdgpu/smu_13_0_6.bin
firmware:       amdgpu/smu_14_0_3.bin
firmware:       amdgpu/smu_14_0_2.bin
firmware:       amdgpu/vega20_smc.bin
firmware:       amdgpu/vega12_smc.bin
firmware:       amdgpu/vega10_acg_smc.bin
firmware:       amdgpu/vega10_smc.bin
firmware:       amdgpu/vegam_smc.bin
firmware:       amdgpu/polaris12_k_smc.bin
firmware:       amdgpu/polaris12_smc.bin
firmware:       amdgpu/polaris11_k2_smc.bin
firmware:       amdgpu/polaris11_k_smc.bin
firmware:       amdgpu/polaris11_smc_sk.bin
firmware:       amdgpu/polaris11_smc.bin
firmware:       amdgpu/polaris10_k2_smc.bin
firmware:       amdgpu/polaris10_k_smc.bin
firmware:       amdgpu/polaris10_smc_sk.bin
firmware:       amdgpu/polaris10_smc.bin
firmware:       amdgpu/fiji_smc.bin
firmware:       amdgpu/tonga_k_smc.bin
firmware:       amdgpu/tonga_smc.bin
firmware:       amdgpu/topaz_k_smc.bin
firmware:       amdgpu/topaz_smc.bin
firmware:       amdgpu/hawaii_k_smc.bin
firmware:       amdgpu/hawaii_smc.bin
firmware:       amdgpu/bonaire_k_smc.bin
firmware:       amdgpu/bonaire_smc.bin
firmware:       amdgpu/banks_k_2_smc.bin
firmware:       amdgpu/hainan_k_smc.bin
firmware:       amdgpu/hainan_smc.bin
firmware:       amdgpu/oland_k_smc.bin
firmware:       amdgpu/oland_smc.bin
firmware:       amdgpu/verde_k_smc.bin
firmware:       amdgpu/verde_smc.bin
firmware:       amdgpu/pitcairn_k_smc.bin
firmware:       amdgpu/pitcairn_smc.bin
firmware:       amdgpu/tahiti_smc.bin
firmware:       amdgpu/dcn_4_0_1_dmcub.bin
firmware:       amdgpu/dcn_3_5_1_dmcub.bin
firmware:       amdgpu/dcn_3_5_dmcub.bin
firmware:       amdgpu/navi12_dmcu.bin
firmware:       amdgpu/raven_dmcu.bin
firmware:       amdgpu/dcn_3_2_1_dmcub.bin
firmware:       amdgpu/dcn_3_2_0_dmcub.bin
firmware:       amdgpu/dcn_3_1_6_dmcub.bin
firmware:       amdgpu/dcn_3_1_5_dmcub.bin
firmware:       amdgpu/dcn_3_1_4_dmcub.bin
firmware:       amdgpu/yellow_carp_dmcub.bin
firmware:       amdgpu/beige_goby_dmcub.bin
firmware:       amdgpu/dimgrey_cavefish_dmcub.bin
firmware:       amdgpu/vangogh_dmcub.bin
firmware:       amdgpu/green_sardine_dmcub.bin
firmware:       amdgpu/navy_flounder_dmcub.bin
firmware:       amdgpu/sienna_cichlid_dmcub.bin
firmware:       amdgpu/renoir_dmcub.bin
srcversion:     660832F85C76D8FBD69930F
alias:          pci:v00001002d*sv*sd*bc12sc00i00*
alias:          pci:v00001002d*sv*sd*bc03sc80i00*
alias:          pci:v00001002d*sv*sd*bc03sc00i00*
alias:          pci:v00001002d0000743Fsv*sd*bc*sc*i*
alias:          pci:v00001002d00007424sv*sd*bc*sc*i*
alias:          pci:v00001002d00007423sv*sd*bc*sc*i*
alias:          pci:v00001002d00007422sv*sd*bc*sc*i*
alias:          pci:v00001002d00007421sv*sd*bc*sc*i*
alias:          pci:v00001002d00007420sv*sd*bc*sc*i*
alias:          pci:v00001002d0000143Fsv*sd*bc*sc*i*
alias:          pci:v00001002d000013FEsv*sd*bc*sc*i*
alias:          pci:v00001002d00007410sv*sd*bc*sc*i*
alias:          pci:v00001002d0000740Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000740Csv*sd*bc*sc*i*
alias:          pci:v00001002d00007408sv*sd*bc*sc*i*
alias:          pci:v00001002d000073FFsv*sd*bc*sc*i*
alias:          pci:v00001002d000073EFsv*sd*bc*sc*i*
alias:          pci:v00001002d000073EDsv*sd*bc*sc*i*
alias:          pci:v00001002d000073ECsv*sd*bc*sc*i*
alias:          pci:v00001002d000073EBsv*sd*bc*sc*i*
alias:          pci:v00001002d000073EAsv*sd*bc*sc*i*
alias:          pci:v00001002d000073E9sv*sd*bc*sc*i*
alias:          pci:v00001002d000073E8sv*sd*bc*sc*i*
alias:          pci:v00001002d000073E3sv*sd*bc*sc*i*
alias:          pci:v00001002d000073E2sv*sd*bc*sc*i*
alias:          pci:v00001002d000073E1sv*sd*bc*sc*i*
alias:          pci:v00001002d000073E0sv*sd*bc*sc*i*
alias:          pci:v00001002d000073DFsv*sd*bc*sc*i*
alias:          pci:v00001002d000073DEsv*sd*bc*sc*i*
alias:          pci:v00001002d000073DDsv*sd*bc*sc*i*
alias:          pci:v00001002d000073DCsv*sd*bc*sc*i*
alias:          pci:v00001002d000073DBsv*sd*bc*sc*i*
alias:          pci:v00001002d000073DAsv*sd*bc*sc*i*
alias:          pci:v00001002d000073C3sv*sd*bc*sc*i*
alias:          pci:v00001002d000073C1sv*sd*bc*sc*i*
alias:          pci:v00001002d000073C0sv*sd*bc*sc*i*
alias:          pci:v00001002d00001681sv*sd*bc*sc*i*
alias:          pci:v00001002d0000164Dsv*sd*bc*sc*i*
alias:          pci:v00001002d000073BFsv*sd*bc*sc*i*
alias:          pci:v00001002d000073AFsv*sd*bc*sc*i*
alias:          pci:v00001002d000073AEsv*sd*bc*sc*i*
alias:          pci:v00001002d000073ADsv*sd*bc*sc*i*
alias:          pci:v00001002d000073ACsv*sd*bc*sc*i*
alias:          pci:v00001002d000073ABsv*sd*bc*sc*i*
alias:          pci:v00001002d000073A9sv*sd*bc*sc*i*
alias:          pci:v00001002d000073A8sv*sd*bc*sc*i*
alias:          pci:v00001002d000073A5sv*sd*bc*sc*i*
alias:          pci:v00001002d000073A3sv*sd*bc*sc*i*
alias:          pci:v00001002d000073A2sv*sd*bc*sc*i*
alias:          pci:v00001002d000073A1sv*sd*bc*sc*i*
alias:          pci:v00001002d000073A0sv*sd*bc*sc*i*
alias:          pci:v00001002d00007362sv*sd*bc*sc*i*
alias:          pci:v00001002d00007360sv*sd*bc*sc*i*
alias:          pci:v00001002d0000164Csv*sd*bc*sc*i*
alias:          pci:v00001002d00001638sv*sd*bc*sc*i*
alias:          pci:v00001002d00001636sv*sd*bc*sc*i*
alias:          pci:v00001002d000015E7sv*sd*bc*sc*i*
alias:          pci:v00001002d0000734Fsv*sd*bc*sc*i*
alias:          pci:v00001002d00007347sv*sd*bc*sc*i*
alias:          pci:v00001002d00007341sv*sd*bc*sc*i*
alias:          pci:v00001002d00007340sv*sd*bc*sc*i*
alias:          pci:v00001002d0000731Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000731Esv*sd*bc*sc*i*
alias:          pci:v00001002d0000731Bsv*sd*bc*sc*i*
alias:          pci:v00001002d0000731Asv*sd*bc*sc*i*
alias:          pci:v00001002d00007319sv*sd*bc*sc*i*
alias:          pci:v00001002d00007318sv*sd*bc*sc*i*
alias:          pci:v00001002d00007312sv*sd*bc*sc*i*
alias:          pci:v00001002d00007310sv*sd*bc*sc*i*
alias:          pci:v00001002d00007390sv*sd*bc*sc*i*
alias:          pci:v00001002d0000738Esv*sd*bc*sc*i*
alias:          pci:v00001002d00007388sv*sd*bc*sc*i*
alias:          pci:v00001002d0000738Csv*sd*bc*sc*i*
alias:          pci:v00001002d000015D8sv*sd*bc*sc*i*
alias:          pci:v00001002d000015DDsv*sd*bc*sc*i*
alias:          pci:v00001002d000066AFsv*sd*bc*sc*i*
alias:          pci:v00001002d000066A7sv*sd*bc*sc*i*
alias:          pci:v00001002d000066A4sv*sd*bc*sc*i*
alias:          pci:v00001002d000066A3sv*sd*bc*sc*i*
alias:          pci:v00001002d000066A2sv*sd*bc*sc*i*
alias:          pci:v00001002d000066A1sv*sd*bc*sc*i*
alias:          pci:v00001002d000066A0sv*sd*bc*sc*i*
alias:          pci:v00001002d000069AFsv*sd*bc*sc*i*
alias:          pci:v00001002d000069A3sv*sd*bc*sc*i*
alias:          pci:v00001002d000069A2sv*sd*bc*sc*i*
alias:          pci:v00001002d000069A1sv*sd*bc*sc*i*
alias:          pci:v00001002d000069A0sv*sd*bc*sc*i*
alias:          pci:v00001002d0000687Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000686Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000686Esv*sd*bc*sc*i*
alias:          pci:v00001002d0000686Dsv*sd*bc*sc*i*
alias:          pci:v00001002d0000686Csv*sd*bc*sc*i*
alias:          pci:v00001002d0000686Bsv*sd*bc*sc*i*
alias:          pci:v00001002d0000686Asv*sd*bc*sc*i*
alias:          pci:v00001002d00006869sv*sd*bc*sc*i*
alias:          pci:v00001002d00006868sv*sd*bc*sc*i*
alias:          pci:v00001002d00006867sv*sd*bc*sc*i*
alias:          pci:v00001002d00006864sv*sd*bc*sc*i*
alias:          pci:v00001002d00006863sv*sd*bc*sc*i*
alias:          pci:v00001002d00006862sv*sd*bc*sc*i*
alias:          pci:v00001002d00006861sv*sd*bc*sc*i*
alias:          pci:v00001002d00006860sv*sd*bc*sc*i*
alias:          pci:v00001002d0000694Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000694Esv*sd*bc*sc*i*
alias:          pci:v00001002d0000694Csv*sd*bc*sc*i*
alias:          pci:v00001002d0000699Fsv*sd*bc*sc*i*
alias:          pci:v00001002d00006997sv*sd*bc*sc*i*
alias:          pci:v00001002d00006995sv*sd*bc*sc*i*
alias:          pci:v00001002d00006987sv*sd*bc*sc*i*
alias:          pci:v00001002d00006986sv*sd*bc*sc*i*
alias:          pci:v00001002d00006985sv*sd*bc*sc*i*
alias:          pci:v00001002d00006981sv*sd*bc*sc*i*
alias:          pci:v00001002d00006980sv*sd*bc*sc*i*
alias:          pci:v00001002d00006FDFsv*sd*bc*sc*i*
alias:          pci:v00001002d000067CFsv*sd*bc*sc*i*
alias:          pci:v00001002d000067CCsv*sd*bc*sc*i*
alias:          pci:v00001002d000067CAsv*sd*bc*sc*i*
alias:          pci:v00001002d000067C9sv*sd*bc*sc*i*
alias:          pci:v00001002d000067C8sv*sd*bc*sc*i*
alias:          pci:v00001002d000067DFsv*sd*bc*sc*i*
alias:          pci:v00001002d000067D0sv*sd*bc*sc*i*
alias:          pci:v00001002d000067C7sv*sd*bc*sc*i*
alias:          pci:v00001002d000067C4sv*sd*bc*sc*i*
alias:          pci:v00001002d000067C2sv*sd*bc*sc*i*
alias:          pci:v00001002d000067C1sv*sd*bc*sc*i*
alias:          pci:v00001002d000067C0sv*sd*bc*sc*i*
alias:          pci:v00001002d000067E9sv*sd*bc*sc*i*
alias:          pci:v00001002d000067E7sv*sd*bc*sc*i*
alias:          pci:v00001002d000067E1sv*sd*bc*sc*i*
alias:          pci:v00001002d000067FFsv*sd*bc*sc*i*
alias:          pci:v00001002d000067EFsv*sd*bc*sc*i*
alias:          pci:v00001002d000067EBsv*sd*bc*sc*i*
alias:          pci:v00001002d000067E8sv*sd*bc*sc*i*
alias:          pci:v00001002d000067E3sv*sd*bc*sc*i*
alias:          pci:v00001002d000067E0sv*sd*bc*sc*i*
alias:          pci:v00001002d000098E4sv*sd*bc*sc*i*
alias:          pci:v00001002d00009877sv*sd*bc*sc*i*
alias:          pci:v00001002d00009876sv*sd*bc*sc*i*
alias:          pci:v00001002d00009875sv*sd*bc*sc*i*
alias:          pci:v00001002d00009874sv*sd*bc*sc*i*
alias:          pci:v00001002d00009870sv*sd*bc*sc*i*
alias:          pci:v00001002d0000730Fsv*sd*bc*sc*i*
alias:          pci:v00001002d00007300sv*sd*bc*sc*i*
alias:          pci:v00001002d00006939sv*sd*bc*sc*i*
alias:          pci:v00001002d00006938sv*sd*bc*sc*i*
alias:          pci:v00001002d00006930sv*sd*bc*sc*i*
alias:          pci:v00001002d0000692Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000692Bsv*sd*bc*sc*i*
alias:          pci:v00001002d00006929sv*sd*bc*sc*i*
alias:          pci:v00001002d00006928sv*sd*bc*sc*i*
alias:          pci:v00001002d00006921sv*sd*bc*sc*i*
alias:          pci:v00001002d00006920sv*sd*bc*sc*i*
alias:          pci:v00001002d00006907sv*sd*bc*sc*i*
alias:          pci:v00001002d00006903sv*sd*bc*sc*i*
alias:          pci:v00001002d00006902sv*sd*bc*sc*i*
alias:          pci:v00001002d00006901sv*sd*bc*sc*i*
alias:          pci:v00001002d00006900sv*sd*bc*sc*i*
alias:          pci:v00001002d0000985Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000985Esv*sd*bc*sc*i*
alias:          pci:v00001002d0000985Dsv*sd*bc*sc*i*
alias:          pci:v00001002d0000985Csv*sd*bc*sc*i*
alias:          pci:v00001002d0000985Bsv*sd*bc*sc*i*
alias:          pci:v00001002d0000985Asv*sd*bc*sc*i*
alias:          pci:v00001002d00009859sv*sd*bc*sc*i*
alias:          pci:v00001002d00009858sv*sd*bc*sc*i*
alias:          pci:v00001002d00009857sv*sd*bc*sc*i*
alias:          pci:v00001002d00009856sv*sd*bc*sc*i*
alias:          pci:v00001002d00009855sv*sd*bc*sc*i*
alias:          pci:v00001002d00009854sv*sd*bc*sc*i*
alias:          pci:v00001002d00009853sv*sd*bc*sc*i*
alias:          pci:v00001002d00009852sv*sd*bc*sc*i*
alias:          pci:v00001002d00009851sv*sd*bc*sc*i*
alias:          pci:v00001002d00009850sv*sd*bc*sc*i*
alias:          pci:v00001002d0000983Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000983Esv*sd*bc*sc*i*
alias:          pci:v00001002d0000983Dsv*sd*bc*sc*i*
alias:          pci:v00001002d0000983Csv*sd*bc*sc*i*
alias:          pci:v00001002d0000983Bsv*sd*bc*sc*i*
alias:          pci:v00001002d0000983Asv*sd*bc*sc*i*
alias:          pci:v00001002d00009839sv*sd*bc*sc*i*
alias:          pci:v00001002d00009838sv*sd*bc*sc*i*
alias:          pci:v00001002d00009837sv*sd*bc*sc*i*
alias:          pci:v00001002d00009836sv*sd*bc*sc*i*
alias:          pci:v00001002d00009835sv*sd*bc*sc*i*
alias:          pci:v00001002d00009834sv*sd*bc*sc*i*
alias:          pci:v00001002d00009833sv*sd*bc*sc*i*
alias:          pci:v00001002d00009832sv*sd*bc*sc*i*
alias:          pci:v00001002d00009831sv*sd*bc*sc*i*
alias:          pci:v00001002d00009830sv*sd*bc*sc*i*
alias:          pci:v00001002d000067BEsv*sd*bc*sc*i*
alias:          pci:v00001002d000067BAsv*sd*bc*sc*i*
alias:          pci:v00001002d000067B9sv*sd*bc*sc*i*
alias:          pci:v00001002d000067B8sv*sd*bc*sc*i*
alias:          pci:v00001002d000067B1sv*sd*bc*sc*i*
alias:          pci:v00001002d000067B0sv*sd*bc*sc*i*
alias:          pci:v00001002d000067AAsv*sd*bc*sc*i*
alias:          pci:v00001002d000067A9sv*sd*bc*sc*i*
alias:          pci:v00001002d000067A8sv*sd*bc*sc*i*
alias:          pci:v00001002d000067A2sv*sd*bc*sc*i*
alias:          pci:v00001002d000067A1sv*sd*bc*sc*i*
alias:          pci:v00001002d000067A0sv*sd*bc*sc*i*
alias:          pci:v00001002d0000665Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000665Dsv*sd*bc*sc*i*
alias:          pci:v00001002d0000665Csv*sd*bc*sc*i*
alias:          pci:v00001002d00006658sv*sd*bc*sc*i*
alias:          pci:v00001002d00006651sv*sd*bc*sc*i*
alias:          pci:v00001002d00006650sv*sd*bc*sc*i*
alias:          pci:v00001002d00006649sv*sd*bc*sc*i*
alias:          pci:v00001002d00006647sv*sd*bc*sc*i*
alias:          pci:v00001002d00006646sv*sd*bc*sc*i*
alias:          pci:v00001002d00006641sv*sd*bc*sc*i*
alias:          pci:v00001002d00006640sv*sd*bc*sc*i*
alias:          pci:v00001002d0000131Dsv*sd*bc*sc*i*
alias:          pci:v00001002d0000131Csv*sd*bc*sc*i*
alias:          pci:v00001002d0000131Bsv*sd*bc*sc*i*
alias:          pci:v00001002d00001318sv*sd*bc*sc*i*
alias:          pci:v00001002d00001317sv*sd*bc*sc*i*
alias:          pci:v00001002d00001316sv*sd*bc*sc*i*
alias:          pci:v00001002d00001315sv*sd*bc*sc*i*
alias:          pci:v00001002d00001313sv*sd*bc*sc*i*
alias:          pci:v00001002d00001312sv*sd*bc*sc*i*
alias:          pci:v00001002d00001311sv*sd*bc*sc*i*
alias:          pci:v00001002d00001310sv*sd*bc*sc*i*
alias:          pci:v00001002d0000130Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000130Esv*sd*bc*sc*i*
alias:          pci:v00001002d0000130Dsv*sd*bc*sc*i*
alias:          pci:v00001002d0000130Csv*sd*bc*sc*i*
alias:          pci:v00001002d0000130Bsv*sd*bc*sc*i*
alias:          pci:v00001002d0000130Asv*sd*bc*sc*i*
alias:          pci:v00001002d00001309sv*sd*bc*sc*i*
alias:          pci:v00001002d00001307sv*sd*bc*sc*i*
alias:          pci:v00001002d00001306sv*sd*bc*sc*i*
alias:          pci:v00001002d00001305sv*sd*bc*sc*i*
alias:          pci:v00001002d00001304sv*sd*bc*sc*i*
alias:          pci:v00001002d0000666Fsv*sd*bc*sc*i*
alias:          pci:v00001002d00006667sv*sd*bc*sc*i*
alias:          pci:v00001002d00006665sv*sd*bc*sc*i*
alias:          pci:v00001002d00006664sv*sd*bc*sc*i*
alias:          pci:v00001002d00006663sv*sd*bc*sc*i*
alias:          pci:v00001002d00006660sv*sd*bc*sc*i*
alias:          pci:v00001002d0000683Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000683Dsv*sd*bc*sc*i*
alias:          pci:v00001002d0000683Bsv*sd*bc*sc*i*
alias:          pci:v00001002d00006839sv*sd*bc*sc*i*
alias:          pci:v00001002d00006838sv*sd*bc*sc*i*
alias:          pci:v00001002d00006837sv*sd*bc*sc*i*
alias:          pci:v00001002d00006835sv*sd*bc*sc*i*
alias:          pci:v00001002d00006831sv*sd*bc*sc*i*
alias:          pci:v00001002d00006830sv*sd*bc*sc*i*
alias:          pci:v00001002d0000682Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000682Dsv*sd*bc*sc*i*
alias:          pci:v00001002d0000682Csv*sd*bc*sc*i*
alias:          pci:v00001002d0000682Bsv*sd*bc*sc*i*
alias:          pci:v00001002d0000682Asv*sd*bc*sc*i*
alias:          pci:v00001002d00006829sv*sd*bc*sc*i*
alias:          pci:v00001002d00006828sv*sd*bc*sc*i*
alias:          pci:v00001002d00006827sv*sd*bc*sc*i*
alias:          pci:v00001002d00006826sv*sd*bc*sc*i*
alias:          pci:v00001002d00006825sv*sd*bc*sc*i*
alias:          pci:v00001002d00006824sv*sd*bc*sc*i*
alias:          pci:v00001002d00006823sv*sd*bc*sc*i*
alias:          pci:v00001002d00006822sv*sd*bc*sc*i*
alias:          pci:v00001002d00006821sv*sd*bc*sc*i*
alias:          pci:v00001002d00006820sv*sd*bc*sc*i*
alias:          pci:v00001002d00006631sv*sd*bc*sc*i*
alias:          pci:v00001002d00006623sv*sd*bc*sc*i*
alias:          pci:v00001002d00006621sv*sd*bc*sc*i*
alias:          pci:v00001002d00006620sv*sd*bc*sc*i*
alias:          pci:v00001002d00006617sv*sd*bc*sc*i*
alias:          pci:v00001002d00006613sv*sd*bc*sc*i*
alias:          pci:v00001002d00006611sv*sd*bc*sc*i*
alias:          pci:v00001002d00006610sv*sd*bc*sc*i*
alias:          pci:v00001002d00006608sv*sd*bc*sc*i*
alias:          pci:v00001002d00006607sv*sd*bc*sc*i*
alias:          pci:v00001002d00006606sv*sd*bc*sc*i*
alias:          pci:v00001002d00006605sv*sd*bc*sc*i*
alias:          pci:v00001002d00006604sv*sd*bc*sc*i*
alias:          pci:v00001002d00006603sv*sd*bc*sc*i*
alias:          pci:v00001002d00006602sv*sd*bc*sc*i*
alias:          pci:v00001002d00006601sv*sd*bc*sc*i*
alias:          pci:v00001002d00006600sv*sd*bc*sc*i*
alias:          pci:v00001002d00006819sv*sd*bc*sc*i*
alias:          pci:v00001002d00006818sv*sd*bc*sc*i*
alias:          pci:v00001002d00006817sv*sd*bc*sc*i*
alias:          pci:v00001002d00006816sv*sd*bc*sc*i*
alias:          pci:v00001002d00006811sv*sd*bc*sc*i*
alias:          pci:v00001002d00006810sv*sd*bc*sc*i*
alias:          pci:v00001002d00006809sv*sd*bc*sc*i*
alias:          pci:v00001002d00006808sv*sd*bc*sc*i*
alias:          pci:v00001002d00006806sv*sd*bc*sc*i*
alias:          pci:v00001002d00006802sv*sd*bc*sc*i*
alias:          pci:v00001002d00006801sv*sd*bc*sc*i*
alias:          pci:v00001002d00006800sv*sd*bc*sc*i*
alias:          pci:v00001002d0000679Fsv*sd*bc*sc*i*
alias:          pci:v00001002d0000679Esv*sd*bc*sc*i*
alias:          pci:v00001002d0000679Bsv*sd*bc*sc*i*
alias:          pci:v00001002d0000679Asv*sd*bc*sc*i*
alias:          pci:v00001002d00006799sv*sd*bc*sc*i*
alias:          pci:v00001002d00006798sv*sd*bc*sc*i*
alias:          pci:v00001002d00006792sv*sd*bc*sc*i*
alias:          pci:v00001002d00006791sv*sd*bc*sc*i*
alias:          pci:v00001002d00006790sv*sd*bc*sc*i*
alias:          pci:v00001002d0000678Asv*sd*bc*sc*i*
alias:          pci:v00001002d00006788sv*sd*bc*sc*i*
alias:          pci:v00001002d00006784sv*sd*bc*sc*i*
alias:          pci:v00001002d00006780sv*sd*bc*sc*i*
depends:        drm_display_helper,drm_buddy,cec,drm_panel_backlight_quirks,ttm,video,drm_suballoc_helper,gpu-sched,drm_exec,drm_ttm_helper,i2c-algo-bit,amdxcp
intree:         Y
name:           amdgpu
retpoline:      Y
vermagic:       6.14.0-29-generic SMP preempt mod_unload modversions 
sig_id:         PKCS#7
signer:         Build time autogenerated kernel key
sig_key:        2D:4F:FB:11:40:28:46:70:59:5E:B6:BE:30:1F:11:2B:42:54:B6:EA
sig_hashalgo:   sha512
signature:      AD:AA:D1:3A:5F:87:03:98:97:EB:BE:CF:7A:FA:8C:46:C7:F0:C3:FA:
		78:97:0B:A6:12:75:B3:8A:62:3B:EC:82:16:58:07:79:E7:76:E9:CC:
		41:6D:EA:BD:98:E4:CD:74:DA:00:1C:AA:72:6F:B5:6C:8E:0B:2A:DD:
		9A:D8:C3:7F:6F:B6:34:6B:1F:7D:5E:23:BF:37:EB:DA:DF:16:CC:08:
		EF:FD:99:86:F6:6D:63:DD:93:C1:CD:5D:E2:E1:9C:F3:D8:3A:35:EC:
		69:65:6A:5B:6D:D4:88:A0:08:7D:3B:DD:67:15:4E:E6:65:35:81:BC:
		79:E4:9D:69:3E:B7:4E:F4:79:FB:B7:A3:6E:51:06:79:30:11:DD:94:
		BD:D3:49:99:4F:6D:33:72:E1:8B:70:48:8C:7F:A9:E0:F9:51:D2:9E:
		5D:23:22:38:9F:92:AA:75:A1:DD:8D:D0:4B:75:9D:B7:35:97:98:F4:
		7A:6C:8B:AF:CA:09:44:CC:F6:84:C8:09:C9:27:01:95:C0:8E:A0:EB:
		37:88:29:EF:AB:91:50:B1:08:07:04:AD:B5:9A:59:79:2C:B1:1F:92:
		A5:5D:38:85:43:33:59:12:2D:19:04:B5:6F:D0:39:0D:1F:35:C6:E1:
		72:72:EB:6D:96:F2:87:92:F9:EA:13:84:10:0F:A7:C9:87:02:6A:55:
		6E:10:DA:ED:17:58:6C:08:14:D7:1D:B4:DE:EF:54:1A:F3:63:05:FF:
		DB:88:53:F7:F1:1D:0D:EC:01:71:7A:B9:A1:B6:E4:7C:67:53:D5:0D:
		5D:E3:FC:26:48:67:A0:5A:3D:A5:DC:78:5A:68:97:E5:B9:3F:D4:EA:
		BB:9F:B9:CA:DC:E5:A5:E7:CE:15:86:4E:A4:CA:C8:01:DD:5C:C5:6A:
		28:72:C3:62:53:89:74:96:93:7E:2C:54:A8:06:D4:76:42:D7:C5:82:
		85:8C:9E:77:25:A3:72:FB:6B:DE:3D:AF:FF:FF:7D:29:44:22:E5:F6:
		CA:BD:E7:F6:8E:84:A3:19:E7:B3:A1:57:E9:7F:DA:D3:FF:2C:53:A0:
		4A:DF:C7:0B:10:05:B0:5A:8E:2A:77:FC:7C:6B:09:27:AB:E8:70:52:
		11:B5:16:11:4D:88:51:BC:C2:F4:A8:5A:ED:B0:EE:E4:5E:A7:54:FB:
		50:66:9B:FC:33:46:9C:B9:C2:81:92:5B:E8:C9:55:3A:81:26:88:5C:
		34:BE:C6:CC:C8:3F:26:06:8E:73:C4:14:46:73:53:5C:A4:8A:9D:97:
		15:C6:A1:0F:E4:55:D8:47:99:46:6A:20:E9:32:9D:EC:30:86:F5:62:
		2E:7C:E3:92:E8:79:B7:2F:10:C1:8F:CB
parm:           vramlimit:Restrict VRAM for testing, in megabytes (int)
parm:           vis_vramlimit:Restrict visible VRAM for testing, in megabytes (int)
parm:           gartsize:Size of kernel GART to setup in megabytes (32, 64, etc., -1=auto) (uint)
parm:           gttsize:Size of the GTT userspace domain in megabytes (-1 = auto) (int)
parm:           moverate:Maximum buffer migration rate in MB/s. (32, 64, etc., -1=auto, 0=1=disabled) (int)
parm:           audio:Audio enable (-1 = auto, 0 = disable, 1 = enable) (int)
parm:           disp_priority:Display Priority (0 = auto, 1 = normal, 2 = high) (int)
parm:           hw_i2c:hw i2c engine enable (0 = disable) (int)
parm:           pcie_gen2:PCIE Gen2 mode (-1 = auto, 0 = disable, 1 = enable) (int)
parm:           msi:MSI support (1 = enable, 0 = disable, -1 = auto) (int)
parm:           svm_default_granularity:SVM's default granularity in log(2^Pages), default 9 = 2^9 = 2 MiB (uint)
parm:           lockup_timeout:GPU lockup timeout in ms (default: for bare metal 10000 for non-compute jobs and 60000 for compute jobs; for passthrough or sriov, 10000 for all jobs. 0: keep default value. negative: infinity timeout), format: for bare metal [Non-Compute] or [GFX,Compute,SDMA,Video]; for passthrough or sriov [all jobs] or [GFX,Compute,SDMA,Video]. (string)
parm:           dpm:DPM support (1 = enable, 0 = disable, -1 = auto) (int)
parm:           fw_load_type:firmware loading type (3 = rlc backdoor autoload if supported, 2 = smu load if supported, 1 = psp load, 0 = force direct if supported, -1 = auto) (int)
parm:           aspm:ASPM support (1 = enable, 0 = disable, -1 = auto) (int)
parm:           runpm:PX runtime pm (2 = force enable with BAMACO, 1 = force enable with BACO, 0 = disable, -1 = auto, -2 = auto with displays) (int)
parm:           ip_block_mask:IP Block Mask (all blocks enabled (default)) (uint)
parm:           bapm:BAPM support (1 = enable, 0 = disable, -1 = auto) (int)
parm:           deep_color:Deep Color support (1 = enable, 0 = disable (default)) (int)
parm:           vm_size:VM address space size in gigabytes (default 64GB) (int)
parm:           vm_fragment_size:VM fragment size in bits (4, 5, etc. 4 = 64K (default), Max 9 = 2M) (int)
parm:           vm_block_size:VM page table size in bits (default depending on vm_size) (int)
parm:           vm_fault_stop:Stop on VM fault (0 = never (default), 1 = print first, 2 = always) (int)
parm:           vm_update_mode:VM update using CPU (0 = never (default except for large BAR(LB)), 1 = Graphics only, 2 = Compute only (default for LB), 3 = Both (int)
parm:           exp_hw_support:experimental hw support (1 = enable, 0 = disable (default)) (int)
parm:           dc:Display Core driver (1 = enable, 0 = disable, -1 = auto (default)) (int)
parm:           sched_jobs:the max number of jobs supported in the sw queue (default 32) (int)
parm:           sched_hw_submission:the max number of HW submissions (default 2) (int)
parm:           ppfeaturemask:all power features enabled (default)) (hexint)
parm:           forcelongtraining:force memory long training (uint)
parm:           pcie_gen_cap:PCIE Gen Caps (0: autodetect (default)) (uint)
parm:           pcie_lane_cap:PCIE Lane Caps (0: autodetect (default)) (uint)
parm:           cg_mask:Clockgating flags mask (0 = disable clock gating) (ullong)
parm:           pg_mask:Powergating flags mask (0 = disable power gating) (uint)
parm:           sdma_phase_quantum:SDMA context switch phase quantum (x 1K GPU clock cycles, 0 = no change (default 32)) (uint)
parm:           disable_cu:Disable CUs (se.sh.cu,...) (charp)
parm:           virtual_display:Enable virtual display feature (the virtual_display will be set like xxxx:xx:xx.x,x;xxxx:xx:xx.x,x) (charp)
parm:           lbpw:Load Balancing Per Watt (LBPW) support (1 = enable, 0 = disable, -1 = auto) (int)
parm:           compute_multipipe:Force compute queues to be spread across pipes (1 = enable, 0 = disable, -1 = auto) (int)
parm:           gpu_recovery:Enable GPU recovery mechanism, (1 = enable, 0 = disable, -1 = auto) (int)
parm:           emu_mode:Emulation mode, (1 = enable, 0 = disable) (int)
parm:           ras_enable:Enable RAS features on the GPU (0 = disable, 1 = enable, -1 = auto (default)) (int)
parm:           ras_mask:Mask of RAS features to enable (default 0xffffffff), only valid when ras_enable == 1 (uint)
parm:           timeout_fatal_disable:disable watchdog timeout fatal error (false = default) (bool)
parm:           timeout_period:watchdog timeout period (0 = timeout disabled, 1 ~ 0x23 = timeout maxcycles = (1 << period) (uint)
parm:           si_support:SI support (1 = enabled, 0 = disabled (default)) (int)
parm:           cik_support:CIK support (1 = enabled, 0 = disabled (default)) (int)
parm:           smu_memory_pool_size:reserve gtt for smu debug usage, 0 = disable,0x1 = 256Mbyte, 0x2 = 512Mbyte, 0x4 = 1 Gbyte, 0x8 = 2GByte (uint)
parm:           async_gfx_ring:Asynchronous GFX rings that could be configured with either different priorities (HP3D ring and LP3D ring), or equal priorities (0 = disabled, 1 = enabled (default)) (int)
parm:           mcbp:Enable Mid-command buffer preemption (0 = disabled, 1 = enabled), -1 = auto (default) (int)
parm:           discovery:Allow driver to discover hardware IPs from IP Discovery table at the top of VRAM (int)
parm:           mes:Enable Micro Engine Scheduler (0 = disabled (default), 1 = enabled) (int)
parm:           mes_log_enable:Enable Micro Engine Scheduler log (0 = disabled (default), 1 = enabled) (int)
parm:           mes_kiq:Enable Micro Engine Scheduler KIQ (0 = disabled (default), 1 = enabled) (int)
parm:           uni_mes:Enable Unified Micro Engine Scheduler (0 = disabled, 1 = enabled(default) (int)
parm:           noretry:Disable retry faults (0 = retry enabled, 1 = retry disabled, -1 auto (default)) (int)
parm:           force_asic_type:A non negative value used to specify the asic type for all supported GPUs (int)
parm:           use_xgmi_p2p:Enable XGMI P2P interface (0 = disable; 1 = enable (default)) (int)
parm:           sched_policy:Scheduling policy (0 = HWS (Default), 1 = HWS without over-subscription, 2 = Non-HWS (Used for debugging only) (int)
parm:           hws_max_conc_proc:Max # processes HWS can execute concurrently when sched_policy=0 (0 = no concurrency, #VMIDs for KFD = Maximum(default)) (int)
parm:           cwsr_enable:CWSR enable (0 = Off, 1 = On (Default)) (int)
parm:           max_num_of_queues_per_device:Maximum number of supported queues per device (1 = Minimum, 4096 = default) (int)
parm:           send_sigterm:Send sigterm to HSA process on unhandled exception (0 = disable, 1 = enable) (int)
parm:           halt_if_hws_hang:Halt if HWS hang is detected (0 = off (default), 1 = on) (int)
parm:           hws_gws_support:Assume MEC2 FW supports GWS barriers (false = rely on FW version check (Default), true = force supported) (bool)
parm:           queue_preemption_timeout_ms:queue preemption timeout in ms (1 = Minimum, 9000 = default) (int)
parm:           debug_evictions:enable eviction debug messages (false = default) (bool)
parm:           no_system_mem_limit:disable system memory limit (false = default) (bool)
parm:           no_queue_eviction_on_vm_fault:No queue eviction on VM fault (0 = queue eviction, 1 = no queue eviction) (int)
parm:           mtype_local:MTYPE for local memory (0 = MTYPE_RW (default), 1 = MTYPE_NC, 2 = MTYPE_CC) (int)
parm:           pcie_p2p:Enable PCIe P2P (requires large-BAR). (N = off, Y = on(default)) (bool)
parm:           dcfeaturemask:all stable DC features enabled (default)) (uint)
parm:           dcdebugmask:all debug options disabled (default)) (uint)
parm:           visualconfirm:Visual confirm (0 = off (default), 1 = MPO, 5 = PSR) (uint)
parm:           abmlevel:ABM level (0 = off, 1-4 = backlight reduction level, -1 auto (default)) (int)
parm:           backlight:Backlight control (0 = pwm, 1 = aux, -1 auto (default)) (bint)
parm:           damageclips:Damage clips support (0 = disable, 1 = enable, -1 auto (default)) (int)
parm:           tmz:Enable TMZ feature (-1 = auto (default), 0 = off, 1 = on) (int)
parm:           freesync_video:Enable freesync modesetting optimization feature (0 = off (default), 1 = on) (uint)
parm:           reset_method:GPU reset method (-1 = auto (default), 0 = legacy, 1 = mode0, 2 = mode1, 3 = mode2, 4 = baco/bamaco) (int)
parm:           bad_page_threshold:Bad page threshold(-1 = ignore threshold (default value), 0 = disable bad page retirement, -2 = driver sets threshold) (int)
parm:           num_kcq:number of kernel compute queue user want to setup (8 if set to greater than 8 or less than 0, only affect gfx 8+) (int)
parm:           vcnfw_log:Enable vcnfw log(0 = disable (default value), 1 = enable) (int)
parm:           sg_display:S/G Display (-1 = auto (default), 0 = disable) (int)
parm:           umsch_mm:Enable Multi Media User Mode Scheduler (0 = disabled (default), 1 = enabled) (int)
parm:           umsch_mm_fwlog:Enable umschfw log(0 = disable (default value), 1 = enable) (int)
parm:           smu_pptable_id:specify pptable id to be used (-1 = auto(default) value, 0 = use pptable from vbios, > 0 = soft pptable id) (int)
parm:           user_partt_mode:specify partition mode to be used (-2 = AMDGPU_AUTO_COMPUTE_PARTITION_MODE(default value) 						0 = AMDGPU_SPX_PARTITION_MODE, 						1 = AMDGPU_DPX_PARTITION_MODE, 						2 = AMDGPU_TPX_PARTITION_MODE, 			3 = AMDGPU_QPX_PARTITION_MODE, 						4 = AMDGPU_CPX_PARTITION_MODE) (uint)
parm:           enforce_isolation:enforce process isolation between graphics and compute . enforce_isolation = on (bool)
parm:           seamless:Seamless boot (-1 = auto (default), 0 = disable, 1 = enable) (int)
parm:           debug_mask:debug options for amdgpu, disabled by default (uint)
parm:           agp:AGP (-1 = auto (default), 0 = disable, 1 = enable) (int)
parm:           wbrf:Enable Wifi RFI interference mitigation (0 = disabled, 1 = enabled, -1 = auto(default) (int)
```

---

### 评论 #13 — harkgill-amd (2025-09-18T16:24:53Z)

The in-kernel amdgpu driver you currently have loaded will work just fine to run LLM workloads. The `amdgpu-dkms` driver and ROCm releases were originally tightly coupled as that pairing helped define what configurations we "support". We're working on decoupling the two - more information regarding this can be found here https://rocm.blogs.amd.com/ecosystems-and-partners/instinct-gpu-driver/README.html and specifically this excerpt

> AMD’s open source GPU driver is available through several channels. Users currently get the driver, amdgpu, through ROCm releases, through Radeon Software for Linux and it is present in many Linux kernel builds. The build of the amdgpu driver and related packages currently distributed and documented with ROCm, is now renamed as the Instinct driver.

---

### 评论 #14 — isapir (2025-09-18T16:42:00Z)

Thanks @harkgill-amd.  For some reason when I ran Ollama before I installed ROCm it was running, though slowly.  After installing ROCm it stopped working.

I opened a ticket with Ollama at https://github.com/ollama/ollama/issues/12320 but I'm not sure if that's a ROCm issue or an Ollama one.

---

### 评论 #15 — harkgill-amd (2025-09-18T18:13:35Z)

I gave this a try on my end with gfx1151 + ROCm 6.4.2.1 + in-kernel driver and ollama worked correctly. Looking at `https://ollama.com/install.sh`, ollama installs the required ROCm libraries in isolation after checking for an AMD gpu. This might not've been done correctly the first time around given the nature of the errors you were seeing with `amdgpu-dkms` - could you rerun `curl -fsSL https://ollama.com/install.sh | sh` to reinstall ollama? You should see the following during your installation,
```
>>> Downloading Linux ROCm amd64 bundle
...
>>> Install complete. Run "ollama" from the command line.
>>> AMD GPU ready.


---

### 评论 #16 — isapir (2025-09-18T18:24:08Z)

I already tried to reinstall Ollama a few times, and it always ended with **">>> AMD GPU ready"**, but I'll give it another try.

To clarify, if I run 

```
curl -fsSL https://ollama.com/install.sh | sh
```

Then there should not be a need to run the ROCm command that is mentioned in the Manual Installation, right? 

<img width="1133" height="1019" alt="Image" src="https://github.com/user-attachments/assets/5a7903f4-a2f8-4161-b700-867bd0b8edb1" />

---

### 评论 #17 — harkgill-amd (2025-09-18T18:43:27Z)

As I understand, that's correct. Just noticed the following in your logs from the other ticket
```
types:[gfx1010 gfx1012 gfx1030 gfx1100 gfx1101 gfx1102 gfx1151 gfx1200 gfx1201 gfx900 gfx906 gfx908 gfx90a gfx942])" gpu_type=gfx1150 gpu=0 library=/usr/local/lib/ollama/rocm
Sep 16 22:09:19 p14s ollama[25207]: time=2025-09-16T22:09:19.181-07:00 level=WARN source=amd_linux.go:387 msg="See https://github.com/ollama/ollama/blob/main/docs/gpu.md#overrides for HSA_OVERRIDE_GFX_VERSION usage"
Sep 16 22:09:19 p14s ollama[25207]: time=2025-09-16T22:09:19.181-07:00 level=INFO source=amd_linux.go:406 msg="no compatible amdgpu devices detected"

Sep 17 10:02:07 p14s ollama[3014]: ROCm error: invalid device function
```
Will try to get my hands on a gfx1150 machine to test this out.

---

### 评论 #18 — isapir (2025-09-18T18:49:34Z)

Thank you @harkgill-amd 🙏 

---

### 评论 #19 — isapir (2025-09-23T18:15:39Z)

@harkgill-amd Is there anything I can do to help expedite a solution for this issue?

---

### 评论 #20 — isapir (2025-09-23T18:47:05Z)

Do you think that ROCm 7.0.1 might solve it? I am running `Ubuntu 24.04.3 LTS (Noble Numbat)` with kernel `6.11.0-1027-oem`

<img width="1000" height="484" alt="Image" src="https://github.com/user-attachments/assets/7f597fbc-f57d-49b8-b59d-c86553454fc2" />

---

### 评论 #21 — harkgill-amd (2025-09-23T18:59:10Z)

> Is there anything I can do to help expedite a solution for this issue?

Without having the system to test it's a little trickier and requires some more trial and error. For starters, could you try setting the following environment variable then running ollama? `HSA_OVERRIDE_GFX_VERSION=11.5.1`

Also, if you have UMA set to Auto in your BIOS, try setting it to a fixed size as described in https://github.com/ollama/ollama/issues/11451.

---

### 评论 #22 — isapir (2025-09-23T19:56:04Z)

I have added the environment variable to the Systemd ollama.service unit file.  My UMA is now set to 32GB (originally when I opened the ticket it was set to the default 8GB).

I guess I installed ROCm in the other ticket and did not fully reinstall it yet so I am trying to do that now, but I am a bit confused and I don't remember what I did the first time.

Do I need to install both ROCm AND the AMDGPU Driver or only ROCm? 

<img width="1166" height="954" alt="Image" src="https://github.com/user-attachments/assets/d21b2ead-5521-4386-b6b8-0bf412dac6af" />

---

### 评论 #23 — isapir (2025-09-23T20:44:06Z)

I installed only the ROCm installation.  I guess it is using the GPU now?  

<img width="1236" height="699" alt="Image" src="https://github.com/user-attachments/assets/076a6ba5-b1d9-40da-9ce5-abdbfe29af98" />

---

### 评论 #24 — harkgill-amd (2025-09-23T21:12:00Z)

Yes that looks correct. If the UMA setting was already set to a fixed value, the environment variable likely resolved the error in the end.

For future reference, you'd only ever need the ROCm packages in your case - `amdgpu-dkms` isn't intended for Ryzen APUs.

---

### 评论 #25 — isapir (2025-09-23T21:18:29Z)

Thanks for clarifying about the different software packages.  

Yes, the UMA setting was fixed on 8GB.

I am surprised that the `VRAM%` usage never goes over 2% in the `rocm-smi` output while the `GPU%` goes up to 100%.  I expected it to go higher.  I'm not sure if that's normal or if I got some configuration wrong.

The workloads I'm running are rather simple and yet they feel slow, but I don't have much experience for comparison so they might just be working as expected.

---

### 评论 #26 — harkgill-amd (2025-09-25T16:22:20Z)

Was able to reproduce the low reported VRAM usage on gfx1151 as well. On my end, the VRAM would consistently be at around ~4%.
```
Device  Node  IDs              Temp    Power     Partitions          SCLK  MCLK  Fan  Perf  PwrCap  VRAM%  GPU%
              (DID,     GUID)  (Edge)  (Socket)  (Mem, Compute, ID)
==================================================================================================================
0       1     0x1586,   65487  33.0°C  4.062W    N/A, N/A, 0         N/A   N/A   0%   auto  N/A     4%     0%
```

This is due to GTT memory being used rather than VRAM when loading the models - `amd-smi metric -m` helps to better illustrate the split between GTT vs VRAM.
```
GPU: 0
    MEM_USAGE:
        TOTAL_VRAM: 8192 MB
        USED_VRAM: 340 MB
        FREE_VRAM: 7852 MB
        TOTAL_VISIBLE_VRAM: 8192 MB
        USED_VISIBLE_VRAM: 340 MB
        FREE_VISIBLE_VRAM: 7852 MB
        TOTAL_GTT: 11901 MB
        USED_GTT: 5699 MB <-- Model loaded here
        FREE_GTT: 6202 MB
```
Another way to confirm that you're GPU is actually in use is through the ollama server logs, for example
```
load_tensors: offloading output layer to GPU
load_tensors: offloaded 29/29 layers to GPU
```
or with `ollama ps`,
```
NAME               ID              SIZE      PROCESSOR    CONTEXT    UNTIL              
llama3.2:latest    a80c4f17acd5    3.3 GB    100% GPU     4096       4 minutes from now  
```
I'm going to close this issue out for the sake of clarity as we're starting to deviate away from the initial report which has been resolved but feel free to open another issue if you still have questions or concerns.

---

### 评论 #27 — harkgill-amd (2025-09-25T16:24:04Z)

Also re: the initial crashes reported being caused by the `amdgpu-dkms` driver - The ROCm 6.4.4 preview release is out with APU support. The instructions also now explicitly mention to use the `--no-dkms` flag during installation to avoid this same issue.

https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#set-up-rocm-usecase

---

### 评论 #28 — isapir (2025-09-25T19:08:57Z)

Thanks for the information @harkgill-amd.  Sounds good RE: closing this issue.  Your last comment raises a quick question though:

A few days ago I installed ROCm 7.0.1 - is there a reason to use version 6.4.4 instead?

---

### 评论 #29 — harkgill-amd (2025-10-08T14:49:52Z)

Apologies for the late reply. Answered a similar question regarding versioning over here https://github.com/ROCm/ROCm/issues/5339#issuecomment-3352694671. To sum it up, use the latest supported release (6.4.4) if you want software that's been tested for your specific usecase/hardware configuration. If you'd rather have the latest features/optimizations while running the risk of encountering hw specific limitations, you can update to a newer unsupported release. 

---
