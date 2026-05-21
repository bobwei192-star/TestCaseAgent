# [Feature]: Request for ROCm Support: AMD PRO A8-8650B (R7, 10 Compute Cores)

> **Issue #4359**
> **状态**: closed
> **创建时间**: 2025-02-08T16:39:14Z
> **更新时间**: 2025-05-26T19:52:51Z
> **关闭时间**: 2025-05-26T19:52:49Z
> **作者**: SoftEng-Islam
> **标签**: Feature Request, ROCm 6.3.2
> **URL**: https://github.com/ROCm/ROCm/issues/4359

## 标签

- **Feature Request** (颜色: #fbca04)
- **ROCm 6.3.2** (颜色: #ededed)

## 描述

### Problem Description

### System Information
- **CPU/APU**: AMD PRO A8-8650B (R7, 10 Compute Cores, 3.7 GHz)
- **RAM**: 8GB
- **OS**: NixOS 25.05 (Kernel 6.12.9)
- **GPU Architecture**: GCN 2.0 (Volcanic Islands, Carrizo-based)

### Issue Description
I would like to request ROCm support for older APUs like the AMD PRO A8-8650B.  
This APU has an integrated Radeon R7 GPU based on the **GCN 2.0 (Volcanic Islands)** architecture.  

Currently, ROCm only officially supports **GCN 3.0+ (Hawaii and newer GPUs)**. However, many users with older AMD APUs still want to use ROCm for AI workloads (like Stable Diffusion).  

### Request
- Could ROCm be extended to support GCN 2.0-based APUs?
- Are there any workarounds or patches to enable partial ROCm support?

Thank you for considering this request!


**echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";**
```bash
OS:
NAME=NixOS
VERSION="25.05 (Warbler)"
```

**echo "CPU: " && cat /proc/cpuinfo | grep "model name" | sort --unique;**
```bash
CPU: 
model name	: AMD PRO A8-8650B R7, 10 Compute Cores 4C+6G
```
 
**echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";**
```bash
GPU:
  Name:                    AMD PRO A8-8650B R7, 10 Compute Cores 4C+6G
  Marketing Name:  AMD PRO A8-8650B R7, 10 Compute Cores 4C+6G
  Name:                    gfx700                             
  Marketing Name:  AMD Radeon R7 Graphics             
  Name:                    amdgcn-amd-amdhsa--gfx700
```

**hashcat -I**              
```bash
hashcat (6.2.6) starting in backend information mode

clGetPlatformIDs(): CL_PLATFORM_NOT_FOUND_KHR

ATTENTION! No OpenCL, HIP or CUDA compatible platform found.

You are probably missing the OpenCL, CUDA or HIP runtime installation.

* AMD GPUs on Linux require this driver:
  "AMDGPU" (21.50 or later) and "ROCm" (5.0 or later)
* Intel CPUs require this runtime:
  "OpenCL Runtime for Intel Core and Intel Xeon Processors" (16.1.1 or later)
* NVIDIA GPUs require this runtime and/or driver (both):
  "NVIDIA Driver" (440.64 or later)
  "CUDA Toolkit" (9.0 or later)
```

**nix-store --query --requisites $(which hipcc) | grep rocm**
```bash
/nix/store/av323b05mfq0qqz324p5v4a2h643ldh5-rocm-llvm-libunwind-6.0.2
```

### Operating System

NixOS 25

### CPU

AMD PRO A8-8650B R7, 10 Compute Cores 4C+6G

### GPU

AMD Radeon R7 Graphics

### ROCm Version

5.7.0

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support
```bash
/opt/rocm/bin/rocminfo --support
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
  Name:                    AMD PRO A8-8650B R7, 10 Compute Cores 4C+6G
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD PRO A8-8650B R7, 10 Compute Cores 4C+6G
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
    L1:                      16384(0x4000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3200                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            4                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    7065704(0x6bd068) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    7065704(0x6bd068) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    7065704(0x6bd068) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx700                             
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon R7 Graphics             
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
    L1:                      16(0x10) KB                        
  Chip ID:                 4883(0x1313)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   757                                
  BDFID:                   8                                  
  Internal Node ID:        1                                  
  Compute Unit:            6                                  
  SIMDs per CU:            4                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      FALSE                              
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 421                                
  SDMA engine uCode::      76                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    3532852(0x35e834) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    3532852(0x35e834) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx700          
      Machine Models:          HSA_MACHINE_MODEL_LARGE            
      Profiles:                HSA_PROFILE_BASE HSA_PROFILE_FULL  
      Default Rounding Mode:   NEAR                               
      Default Rounding Mode:   NEAR                               
      Fast f16:                FALSE                              
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
*** Done ***        
```


_No response_

### hipcc --version
```bash
hipcc --version

sh: line 1: /opt/rocm/llvm/bin/clang: No such file or directory
/opt/rocm/bin/rocm_agent_enumerator:95: SyntaxWarning: invalid escape sequence '\w'
  @staticVars(search_name=re.compile("gfx[0-9a-fA-F]+(:[-+:\w]+)?"))
/opt/rocm/bin/rocm_agent_enumerator:152: SyntaxWarning: invalid escape sequence '\A'
  line_search_term = re.compile("\A\s+Name:\s+(amdgcn-amd-amdhsa--gfx\d+)")
/opt/rocm/bin/rocm_agent_enumerator:154: SyntaxWarning: invalid escape sequence '\A'
  line_search_term = re.compile("\A\s+Name:\s+(gfx\d+)")
/opt/rocm/bin/rocm_agent_enumerator:175: SyntaxWarning: invalid escape sequence '\w'
  target_search_term = re.compile("1002:\w+")
HIP version: 5.7.0-0
sh: line 1: /opt/rocm/llvm/bin/clang: No such file or directory
```
_No response_

---

## 评论 (3 条)

### 评论 #1 — SoftEng-Islam (2025-02-08T16:50:55Z)

My ROCM Configs in nixos:
```nix
# Do not modify this file!  It was generated by ‘nixos-generate-config’
# and may be overwritten by future invocations.  Please make changes
# to /etc/nixos/configuration.nix instead.
{ lib, settings, inputs, pkgs, modulesPath, ... }: {
  imports = [ (modulesPath + "/installer/scan/not-detected.nix") ];
  fileSystems."/" = {
    device = "/dev/disk/by-uuid/ba8daecb-c5d6-4dc9-bc51-a38b344ca6ed";
    fsType = "btrfs";
    options = [ "subvol=@" ];
  };

  fileSystems."/boot" = {
    device = "/dev/disk/by-uuid/7FD3-5156";
    fsType = "vfat";
    # options = [ "fmask=0077" "dmask=0077" ];
    options = [ "rw" ];
  };

  swapDevices = [{
    device = "/dev/disk/by-uuid/d06b1b0e-01c1-4874-98af-9f8e2cc53b4e";
    # size = 4 * 1024; # Size in MB for a 4GB swap file
  }];

  fileSystems."/data" = {
    device = "/dev/disk/by-uuid/67F7388D1080E3AB";
    # fsType = "auto";
    fsType = "ntfs-3g";
    options = [
      "rw"
      "nofail"
      "nodev"
      "uid=1000"
      "gid=1000"
      "utf8"
      "umask=022"
      "exec"
      "x-gvfs-show"
    ];
  };

  # Enables DHCP on each ethernet and wireless interface. In case of scripted networking
  # (the default) this is the recommended approach. When using systemd-networkd it's
  # still possible to use this option, but it's recommended to use it in conjunction
  # with explicit per-interface declarations with `networking.interfaces.<interface>.useDHCP`.
  networking.useDHCP = lib.mkDefault true;
  # networking.interfaces.eno1.useDHCP = lib.mkDefault true;
  # networking.interfaces.wlp0s16f1u2.useDHCP = lib.mkDefault true;

  nixpkgs.hostPlatform = lib.mkDefault "${settings.system.architecture}";
  services = {
    # fstrim.enable = true;
    xserver.videoDrivers = settings.hardware.videoDrivers;
    # auto-epp.enable = true;
  };
  hardware = {
    uinput.enable = true;
    enableAllFirmware = true;
    cpu.amd.updateMicrocode = true;
    # cpu.amd.sev.enable = true;
    enableRedistributableFirmware = true;
    amdgpu.initrd.enable = true;
    amdgpu.amdvlk.enable = true;
    amdgpu.amdvlk.support32Bit.enable = true;
    amdgpu.amdvlk.supportExperimental.enable = true;
    amdgpu.opencl.enable = true;
    amdgpu.legacySupport.enable = false;
    amdgpu.amdvlk.settings = {
      IFH = 0;
      ShaderCacheMode = 1;
      EnableVmAlwaysValid = 1;
      IdleAfterSubmitGpuMask = 1;
      AllowVkPipelineCachingToDisk = 1;
    };
    graphics = {
      enable = true;
      enable32Bit = true;
      extraPackages = with pkgs; [
        amdvlk
        mesa.opencl
        libvdpau-va-gl
        rocmPackages.clr
        rocmPackages.clr.icd
        rocmPackages.rocm-runtime
        rocmPackages.rocm-smi
        rocmPackages.rocminfo
        libGL
        libGLU
        libGLX
        libva
        libva-utils
        vaapiVdpau
      ];
      extraPackages32 = [
        pkgs.driversi686Linux.amdvlk
        #  pkgs.pkgsi686Linux.libva
      ];
    };
  };
  systemd.tmpfiles.rules = let
    rocmEnv = pkgs.symlinkJoin {
      name = "rocm-combined";
      paths = with pkgs.rocmPackages; [ rocblas hipblas clr ];
    };
  in [ "L+    /opt/rocm   -    -    -     -    ${rocmEnv}" ];

  environment.variables = {

    ROCM_PATH = "${pkgs.rocmPackages.rocm-runtime}";
    HIP_PATH = "${pkgs.rocmPackages.hip-common}/libexec/hip";
    PATH =
      "${pkgs.rocmPackages.rocm-runtime}/bin:${pkgs.rocmPackages.hip-common}/bin:$PATH";

    # Load AMD driver for Xorg and Waylandard
    LIBVA_DRIVER_NAME = "amdgpu";
    VDPAU_DRIVER = "amdgpu";
    OCL_ICD_VENDORS = ''
      ${pkgs.rocmPackages.clr.icd}/etc/OpenCL/vendors/
    '';
    VK_ICD_FILENAMES = ''
      ${pkgs.amdvlk}/share/vulkan/icd.d/amd_icd64.json
    '';
    GPU_MAX_ALLOC_PERCENT = "50";
    GPU_MAX_HEAP_SIZE = "50";
    GPU_SINGLE_ALLOC_PERCENT = "50";
    GPU_MAX_USE_SYNC_OBJECTS = "1";
    GPU_FORCE_64BIT_PTR = "1";
    AMD_VULKAN_ICD = "RADV";
  };

  # We are creating the lact daemon service manually because the provided one hangs
  systemd.services.lactd = {
    enable = false;
    description = "Radeon GPU monitor";
    after = [ "syslog.target" "systemd-modules-load.service" ];

    unitConfig = { ConditionPathExists = "${pkgs.lact}/bin/lact"; };

    serviceConfig = {
      User = "root";
      ExecStart = "${pkgs.lact}/bin/lact daemon";
    };

    wantedBy = [ "multi-user.target" ];
  };

  # services.ucodenix = {
  #   enable = false;
  #   # docs: https://github.com/e-tho/ucodenix?tab=readme-ov-file#usage
  #   cpuModelId = "00A70F41";
  # };

  environment.systemPackages = with pkgs; [
    # xivlauncher # Custom launcher for FFXIV
    # zenstates # Linux utility for Ryzen processors and motherboards
    # amdgpu_top # Tool to display AMDGPU usage

    nvtopPackages.amd
    llvmPackages.mlir # Multi-Level IR Compiler Framework

    rocmPackages.hip-common
    rocmPackages.hipblas
    rocmPackages.hipcc
    rocmPackages.hipcub
    rocmPackages.hipfft
    rocmPackages.hipify
    rocmPackages.hiprand
    rocmPackages.rocminfo

    # zluda # ZLUDA - CUDA on Intel GPUs

    oclgrind # OpenCL device simulator and debugger
    amd-ucodegen # Tool to generate AMD microcode files
    microcode-amd # AMD Processor microcode patch
    microcodeAmd
    pciutils # Collection of programs for inspecting and manipulating configuration of PCI devices
    linux-firmware # Binary firmware collection packaged by kernel.org

    # AMD Stuff
    amdvlk # AMD Open Source Driver For Vulkan
    driversi686Linux.amdvlk # AMD Open Source Driver For Vulkan
    driversi686Linux.mesa # An open source 3D graphics library
    amdenc # AMD Encode Core Library
    amdctl # Set P-State voltages and clock speeds on recent AMD CPUs on Linux
    amd-blis # BLAS-compatible library optimized for AMD CPUs
    # amd-libflame # LAPACK-compatible linear algebra library optimized for AMD CPUs
    # amf # AMD's closed source Advanced Media Framework (AMF) driver
    aocl-utils # Interface to all AMD AOCL libraries to access CPU features

    clinfo # Print all known information about all available OpenCL platforms and devices in the system
    dxvk # A Vulkan-based translation layer for Direct3D
    glaxnimate # Simple vector animation program.
    glmark2 # OpenGL (ES) 2.0 benchmark
    gpu-viewer # A front-end to glxinfo, vulkaninfo, clinfo and es2_info
    hwdata # Hardware Database, including Monitors, pci.ids, usb.ids, and video cards
    khronos-ocl-icd-loader # Official Khronos OpenCL ICD Loader
    libdrm # Direct Rendering Manager library and headers
    libplacebo # Reusable library for GPU-accelerated video/image rendering primitives
    libva # An implementation for VA-API (Video Acceleration API)
    mesa # An open source 3D graphics library
    mesa_glu # OpenGL utility library
    mesa_i686 # Open source 3D graphics library
    mesa-demos # Collection of demos and test programs for OpenGL and Mesa
    ocl-icd # OpenCL ICD Loader for opencl-headers-2023.12.14
    openal # OpenAL alternative
    opencl-clang # A clang wrapper library with an OpenCL-oriented API and the ability to compile OpenCL C kernels to SPIR-V modules
    opencl-clhpp # OpenCL Host API C++ bindings
    opencl-headers # Khronos OpenCL headers version 2023.12.14
    oclgrind # OpenCL device simulator and debugger

    spirv-cross
    spirv-headers
    spirv-llvm-translator
    spirv-tools
    libunwind
    llvm

    vkbasalt # Vulkan post processing layer for Linux
    vkquake # Vulkan Quake port based on QuakeSpasm
    vulkan-extension-layer # Layers providing Vulkan features when native support is unavailable
    vulkan-headers # Vulkan Header files and API registry
    vulkan-tools # Khronos official Vulkan Tools and Utilities
    vulkan-utility-libraries # Set of utility libraries for Vulkan

    xorg.xf86videoamdgpu

    lact # Linux AMDGPU Controller and GPU overclocking tool
  ];
}

```

---

### 评论 #2 — HyperWinX (2025-03-15T12:33:56Z)

Honestly, I'd like to see ROCm support too. I have a home server based on that exact CPU, and GPU acceleration like that would help me a lot.

---

### 评论 #3 — harkgill-amd (2025-05-26T19:52:49Z)

Hi @SoftEng-Islam, unfortunately, graphics architectures older than gfx7/Hawaii are missing key HW features that inhibit them from being ROCm compatible. These limitations restrict KFD which is fundamental for all compute based operations in ROCm. I'm not aware of any available patches to enable these older architectures.

You can find similar responses to previous asks at https://github.com/ROCm/ROCm/issues/509#issuecomment-422999215 and https://github.com/ROCm/ROCm/issues/2232. 

---
