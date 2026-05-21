# TDR work around on Windows

> **Issue #2335**
> **状态**: closed
> **创建时间**: 2023-07-27T15:20:49Z
> **更新时间**: 2024-04-21T13:32:39Z
> **关闭时间**: 2024-04-21T13:32:39Z
> **作者**: saadrahim
> **标签**: Verified Issue, Windows, 5.5.1
> **URL**: https://github.com/ROCm/ROCm/issues/2335

## 标签

- **Verified Issue** (颜色: #0052cc)
- **Windows** (颜色: #c2e0c6)
- **5.5.1** (颜色: #bfd4f2)

## 描述

Timeout detection and recovery (TDR) may cause issues when running HIP applications on the Windows operating system. TDR is a Windows feature that enables the operating system to detect when the UI is unresponsive and recover by resetting the graphics driver.

When the GPU is busy processing intensive operations the UI may become unresponsive. Thus, triggering TDR and causing the operations to fail after being cut short when the graphics driver is reset. When running HIP applications, applications may use demanding parameters that fully utilizes the GPU. These tests may cause the UI to become unresponsive which in turn, triggers TDR and results in test failures.

There are two options to work around TDR to allow these tests to complete on the Windows operating system.

1. TDR can be disabled by setting the following Windows registry key to 0.
    - Value is set to 3 by default for TdrLevelRecover which enables detection of and recovery from timeout.
    - Value should be set to 0 for TdrLevelOff which disables detection.

```
KeyPath   : HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\GraphicsDrivers
KeyValue  : TdrLevel
ValueType : REG_DWORD
ValueData : Value
```

2. Increase the timeout threshold before TDR resets the driver through the following Windows registry.
    - Value is the number of seconds to delay which is 2 seconds by default.
    - Increase Value to a sufficient time that allow the operations to complete before TDR is triggered (~15 seconds).
```
KeyPath   : HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\GraphicsDrivers
KeyValue  : TdrDelay
ValueType : REG_DWORD
ValueData : Value
```

