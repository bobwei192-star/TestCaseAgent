# [Feature]: CDI generator for a universal container support

> **Issue #3029**
> **状态**: open
> **创建时间**: 2024-04-17T11:52:59Z
> **更新时间**: 2025-05-31T11:29:57Z
> **作者**: Scapal
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/3029

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

In order to make it easier way to expose AMD GPUs in containers, ROCm should embrace the [Container Device Interface](https://github.com/cncf-tags/container-device-interface).

It should be quite straightforward to implement as it is just about naming the devices in a yaml file and having hooks.
```yaml
cdiVersion: 0.5.0
kind: amd.com/gpu
devices:
- name: "0"
  containerEdits:
    deviceNodes:
    - path: /dev/kfd
    - path: /dev/dri/renderD128
- name: "1"
  containerEdits:
    deviceNodes:
    - path: /dev/kfd
    - path: /dev/dri/renderD130
- name: "all"
  containerEdits:
    deviceNodes:
    - path: /dev/kfd
    - path: /dev/dri/renderD128
    - path: /dev/dri/renderD130
```

CDI is now supported by Docker (v25), containers, CRI-O and Podman.

For example, for Docker or Podman, you can then specify `--device amd.com/gpu/1` instead of `--device /dev/kfd --device /dev/dri/renderD130`

### Operating System

Linux

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (3 条)

### 评论 #1 — gabrielmougard (2024-06-04T13:10:16Z)

Hello @Scapal! I'm currently working on integrating CDI for LXD (https://github.com/canonical/lxd/tree/main) and would be very interested in having a CDI generator for AMD GPUs! Also, like in `nvidia-ctk` (https://github.com/NVIDIA/nvidia-container-toolkit/blob/main/cmd/nvidia-ctk/README.md), the generated CDI spec should discover runtime libraries on the host to pass into the container namespace and list them in the CDI (with their associated hooks). Here is the example for an NVIDIA GPU:
```json
{
  "cdiVersion": "0.5.0",
  "kind": "nvidia.com/gpu",
  "devices": [
    {
      "name": "0",
      "containerEdits": {
        "deviceNodes": [
          {
            "path": "/dev/nvidia0"
          },
          {
            "path": "/dev/dri/card1"
          },
          {
            "path": "/dev/dri/renderD128"
          }
        ],
        "hooks": [
          {
            "hookName": "createContainer",
            "path": "/usr/bin/nvidia-ctk",
            "args": [
              "nvidia-ctk",
              "hook",
              "chmod",
              "--mode",
              "755",
              "--path",
              "/dev/dri"
            ]
          }
        ]
      }
    },
    {
      "name": "GPU-8836a272-ca08-9629-24b6-54ca9b98cd30",
      "containerEdits": {
        "deviceNodes": [
          {
            "path": "/dev/nvidia0"
          },
          {
            "path": "/dev/dri/card1"
          },
          {
            "path": "/dev/dri/renderD128"
          }
        ],
        "hooks": [
          {
            "hookName": "createContainer",
            "path": "/usr/bin/nvidia-ctk",
            "args": [
              "nvidia-ctk",
              "hook",
              "chmod",
              "--mode",
              "755",
              "--path",
              "/dev/dri"
            ]
          }
        ]
      }
    },
    {
      "name": "all",
      "containerEdits": {
        "deviceNodes": [
          {
            "path": "/dev/nvidia0"
          },
          {
            "path": "/dev/dri/card1"
          },
          {
            "path": "/dev/dri/renderD128"
          }
        ],
        "hooks": [
          {
            "hookName": "createContainer",
            "path": "/usr/bin/nvidia-ctk",
            "args": [
              "nvidia-ctk",
              "hook",
              "chmod",
              "--mode",
              "755",
              "--path",
              "/dev/dri"
            ]
          }
        ]
      }
    }
  ],
  "containerEdits": {
    "env": [
      "NVIDIA_VISIBLE_DEVICES=void"
    ],
    "deviceNodes": [
      {
        "path": "/dev/nvidia-modeset"
      },
      {
        "path": "/dev/nvidia-uvm"
      },
      {
        "path": "/dev/nvidia-uvm-tools"
      },
      {
        "path": "/dev/nvidiactl"
      }
    ],
    "hooks": [
      {
        "hookName": "createContainer",
        "path": "/usr/bin/nvidia-ctk",
        "args": [
          "nvidia-ctk",
          "hook",
          "create-symlinks",
          "--link",
          "libglxserver_nvidia.so.535.161.08::/usr/lib/aarch64-linux-gnu/nvidia/xorg/libglxserver_nvidia.so"
        ]
      },
      {
        "hookName": "createContainer",
        "path": "/usr/bin/nvidia-ctk",
        "args": [
          "nvidia-ctk",
          "hook",
          "update-ldcache",
          "--folder",
          "/usr/lib/aarch64-linux-gnu"
        ]
      }
    ],
    "mounts": [
      {
        "hostPath": "/run/nvidia-persistenced/socket",
        "containerPath": "/run/nvidia-persistenced/socket",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind",
          "noexec"
        ]
      },
      {
        "hostPath": "/usr/bin/nvidia-cuda-mps-control",
        "containerPath": "/usr/bin/nvidia-cuda-mps-control",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/bin/nvidia-cuda-mps-server",
        "containerPath": "/usr/bin/nvidia-cuda-mps-server",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/bin/nvidia-debugdump",
        "containerPath": "/usr/bin/nvidia-debugdump",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/bin/nvidia-persistenced",
        "containerPath": "/usr/bin/nvidia-persistenced",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/bin/nvidia-smi",
        "containerPath": "/usr/bin/nvidia-smi",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libEGL_nvidia.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libEGL_nvidia.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libGLESv1_CM_nvidia.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libGLESv1_CM_nvidia.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libGLESv2_nvidia.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libGLESv2_nvidia.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libGLX_nvidia.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libGLX_nvidia.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libcuda.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libcuda.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libcudadebugger.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libcudadebugger.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvcuvid.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvcuvid.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-allocator.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-allocator.so.535.161.08",
        "options": [
          "ro",
          "nosudGPUid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-cfg.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-cfg.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-egl-gbm.so.1.1.0",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-egl-gbm.so.1.1.0",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-eglcore.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-eglcore.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-encode.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-encode.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-fbc.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-fbc.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-glcore.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-glcore.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-glsi.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-glsi.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-glvkspirv.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-glvkspirv.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-ml.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-ml.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-ngx.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-ngx.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-nvvm.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-nvvm.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-opencl.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-opencl.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-opticalflow.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-opticalflow.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-ptxjitcompiler.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-ptxjitcompiler.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-rtcore.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-rtcore.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-tls.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-tls.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvidia-vulkan-producer.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvidia-vulkan-producer.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/libnvoptix.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/libnvoptix.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/share/nvidia/nvoptix.bin",
        "containerPath": "/usr/share/nvidia/nvoptix.bin",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/lib/firmware/nvidia/535.161.08/gsp_ga10x.bin",
        "containerPath": "/lib/firmware/nvidia/535.161.08/gsp_ga10x.bin",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/lib/firmware/nvidia/535.161.08/gsp_tu10x.bin",
        "containerPath": "/lib/firmware/nvidia/535.161.08/gsp_tu10x.bin",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/share/X11/xorg.conf.d/10-nvidia.conf",
        "containerPath": "/usr/share/X11/xorg.conf.d/10-nvidia.conf",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/share/egl/egl_external_platform.d/15_nvidia_gbm.json",
        "containerPath": "/usr/share/egl/egl_external_platform.d/15_nvidia_gbm.json",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/share/glvnd/egl_vendor.d/10_nvidia.json",
        "containerPath": "/usr/share/glvnd/egl_vendor.d/10_nvidia.json",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/share/vulkan/icd.d/nvidia_icd.json",
        "containerPath": "/usr/share/vulkan/icd.d/nvidia_icd.json",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/share/vulkan/implicit_layer.d/nvidia_layers.json",
        "containerPath": "/usr/share/vulkan/implicit_layer.d/nvidia_layers.json",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/nvidia/xorg/libglxserver_nvidia.so.535.161.08",
        "containerPath": "/usr/lib/aarch64-linux-gnu/nvidia/xorg/libglxserver_nvidia.so.535.161.08",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      },
      {
        "hostPath": "/usr/lib/aarch64-linux-gnu/nvidia/xorg/nvidia_drv.so",
        "containerPath": "/usr/lib/aarch64-linux-gnu/nvidia/xorg/nvidia_drv.so",
        "options": [
          "ro",
          "nosuid",
          "nodev",
          "bind"
        ]
      }
    ]
  }
}
```


What would be even more amazing, is to apply filtering capabilities. NVIDIA is doing this for their `nvidia-container-runtime` through env variables to passthhrough only certain runtime libs. Example: only the libs related to `compute` or `display`. See [here](https://github.com/NVIDIA/nvidia-container-toolkit/blob/main/cmd/nvidia-container-runtime/README.md) for more info. Note that they do not support this kind of filtering yet with CDI generation, but maybe they will at some point.

---

### 评论 #2 — elezar (2024-06-04T14:00:33Z)

@Scapal as a maintainer of the CDI specification (as well as the NVIDIA tooling to generate CDI specifications for our devices), it would definitely be beneficial to have the ability to generate CDI specifications for ROCm devices.

As @gabrielmougard mentions, they are currently looking into what is required to add CDI support to LXC/LXD. This would add to the existing support in OCI-compliant runtimes such as Docker, Podman, Containerd, and Cri-o.

---

### 评论 #3 — polarathene (2025-05-31T11:29:56Z)

Seems official CDI support has landed recently?:
- https://github.com/ROCm/container-toolkit/releases/tag/v1.0.0
- https://github.com/ROCm/container-toolkit?tab=readme-ov-file#docker-runtime-integration
- https://instinct.docs.amd.com/projects/container-toolkit/en/latest/container-runtime/release-notes.html

Seems to be rather limited at a glance, but that may only be official support? I don't have any AMD GPU at the moment to try but if someone could confirm broader compatibility that would be appreciated :)

---

> ![Image](https://github.com/user-attachments/assets/b44dfbf0-8531-4bcc-b579-0b998d8e942e)

> ![Image](https://github.com/user-attachments/assets/3122fdab-f814-4186-8a5b-1b05e9f6ed9b)

> ![Image](https://github.com/user-attachments/assets/d0262cd7-882e-4682-946a-0a408d1c520f)

---
