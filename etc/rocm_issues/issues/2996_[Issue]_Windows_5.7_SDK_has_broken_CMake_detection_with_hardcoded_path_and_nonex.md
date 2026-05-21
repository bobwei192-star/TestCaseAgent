# [Issue]: Windows 5.7 SDK has broken CMake detection with hardcoded path and nonexistent amdhip64.dll

> **Issue #2996**
> **状态**: closed
> **创建时间**: 2024-04-04T12:32:27Z
> **更新时间**: 2024-08-21T14:35:11Z
> **关闭时间**: 2024-08-21T14:35:11Z
> **作者**: GZGavinZhao
> **标签**: Under Investigation, AMD Radeon VII, ROCm 5.7.0
> **URL**: https://github.com/ROCm/ROCm/issues/2996

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon VII** (颜色: #ededed)
- **ROCm 5.7.0** (颜色: #ededed)

## 描述

### Problem Description

The HIP 5.7 SDK for Windows cannot be used with CMake because it hardcodes some HIP import prefix as `C:/constructicon/builds/gfx/two/23.30/drivers/compute/install/native/Release/x64/hip` and tries to find a non-existent `amdhip64.dll` file in the SDK.

### Operating System

Windows 11, will update exact version later, on linux right now

### CPU

AMD Ryzen 7 5800H with Radeon Graphics

### GPU

AMD Radeon VII

### ROCm Version

ROCm 5.7.0

### ROCm Component

_No response_

### Steps to Reproduce

  Install the ROCm 5.7 SDK for Windows with default settings: https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html. This example uses the "Windows 10 & 11" version, but the "Windows Server" version has the same problem. All commands are run in Powershell.
  
  1. Write a simple CMake file. This examples uses the native CMake support, but using the legacy `target_link_libraries(MyLib PRIVATE hip::device)` gives the same result.
  ```cmake
  cmake_minimum_required(VERSION 3.21) # HIP language support requires 3.21
  cmake_policy(VERSION 3.21.3...3.27)
  project(MyProj LANGUAGES HIP)
  add_executable(vectoradd_hip vectoradd_hip.cpp)
  set_source_files_properties(vectoradd_hip.cpp PROPERTIES LANGUAGE HIP)
  ```
  2. Create a file at `vectoradd_hip.cpp`. I just used https://github.com/ROCm/HIP-Examples/blob/master/vectorAdd/vectoradd_hip.cpp.
  3. Run `cmake -GNinja -B build -S . -DCMAKE_PREFIX_PATH="C:/Program Files/AMD/ROCm/5.7`. If CMake claims that it can't find a valid HIP compiler, run `$env:Path = "C:\Program Files\AMD\ROCm\5.7;$env:Path"` prior to executing CMake.
  4. Now you should see an error message, claiming that the file `C:/constructicon/builds/gfx/two/23.30/drivers/compute/install/native/Release/x64/hip/lib/amdhip64.lib` is not found. This shouldn't happen.

<details>
<summary> error message </summary>

```
CMake Error at C:/Program Files/AMD/ROCm/5.7/lib/cmake/hip-lang/hip-lang-targets.cmake:82 (message):
  The imported target "hip-lang::amdhip64" references the file

     "C:/constructicon/builds/gfx/two/23.30/drivers/compute/install/native/Release/x64/hip/lib/amdhip64.lib"

  but this file does not exist.  Possible reasons include:

  * The file was deleted, renamed, or moved to another location.

  * An install or uninstall procedure did not complete successfully.

  * The installation package was faulty and contained

     "C:/Program Files/AMD/ROCm/5.7/lib/cmake/hip-lang/hip-lang-targets.cmake"

  but not all the files it references.

Call Stack (most recent call first):
  C:/Program Files/AMD/ROCm/5.7/lib/cmake/hip-lang/hip-lang-config.cmake:87 (include)
  C:/Program Files/CMake/share/cmake-3.29/Modules/CMakeHIPInformation.cmake:159 (find_package)
  CMakeLists.txt:3 (project)


CMake Debug Log at C:/Program Files/CMake/share/cmake-3.29/Modules/CMakeHIPInformation.cmake:159 (find_package):
    C:/Program Files/AMD/ROCm/5.7/lib/cmake/hip-lang/hip-langConfig.cmake
    C:/Program Files/AMD/ROCm/5.7/lib/cmake/hip-lang/hip-lang-config.cmake

Call Stack (most recent call first):
  CMakeLists.txt:3 (project)


-- Configuring incomplete, errors occurred!
```

</details>  


  5. Now, (might need admin privileges), go edit `C:\Program Files\AMD\ROCm\5.7\lib\cmake\hip-lang\hip-lang-targets.cmake`. You'll see that line 45 has `set(_IMPORT_PREFIX "C:/constructicon/builds/gfx/two/23.30/drivers/compute/install/native/Release/x64/hip")`. Replace that with `set(_IMPORT_PREFIX "C:/Program Files/AMD/ROCm/5.7")`, and run the CMake command in step 3 again.
  6. Now you should get a different error, claiming that CMake fails to find `amdhip64.dll`, but that file is not present anywhere in `C:/Program Files/AMD/ROCm/5.7`:
  <details>
  
  <summary> error message </summary>
  
  ```
  CMake Error at C:/Program Files/AMD/ROCm/5.7/lib/cmake/hip-lang/hip-lang-targets.cmake:83 (message):
    The imported target "hip-lang::amdhip64" references the file
  
       "C:/Program Files/AMD/ROCm/5.7/bin/amdhip64.dll"
  
    but this file does not exist.  Possible reasons include:
  
    * The file was deleted, renamed, or moved to another location.
  
    * An install or uninstall procedure did not complete successfully.
  
    * The installation package was faulty and contained
  
       "C:/Program Files/AMD/ROCm/5.7/lib/cmake/hip-lang/hip-lang-targets.cmake"
  
    but not all the files it references.
  
  Call Stack (most recent call first):
    C:/Program Files/AMD/ROCm/5.7/lib/cmake/hip-lang/hip-lang-config.cmake:87 (include)
    C:/Program Files/CMake/share/cmake-3.29/Modules/CMakeHIPInformation.cmake:159 (find_package)
    CMakeLists.txt:3 (project)
  
  
  CMake Debug Log at C:/Program Files/CMake/share/cmake-3.29/Modules/CMakeHIPInformation.cmake:159 (find_package):
      C:/Program Files/AMD/ROCm/5.7/lib/cmake/hip-lang/hip-langConfig.cmake
      C:/Program Files/AMD/ROCm/5.7/lib/cmake/hip-lang/hip-lang-config.cmake
  
  Call Stack (most recent call first):
    CMakeLists.txt:3 (project)
  
  
  -- Configuring incomplete, errors occurred!
  ```
  
  </details>


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — nartmada (2024-04-04T14:13:24Z)

An internal ticket has been created for investigation.

---

### 评论 #2 — YellowRoseCx (2024-04-12T19:41:05Z)

try using ``find_package(hip)`` instead of setting the language to HIP

---

### 评论 #3 — Gardene-el (2024-04-28T01:52:42Z)

> try using `find_package(hip)` instead of setting the language to HIP尝试使用 `find_package(hip)` 而不是将语言设置为 HIP

Is that a practiced method? I tried to follow the [ROCm-examples](https://github.com/rocm/rocm-examples) building guide 
 but also met the same problem, therefore I don't think `find_package(hip)` is an official practice. Did you try it?

---

### 评论 #4 — YellowRoseCx (2024-05-01T14:57:58Z)

> > try using `find_package(hip)` instead of setting the language to HIP尝试使用 `find_package(hip)` 而不是将语言设置为 HIP
> 
> Is that a practiced method? I tried to follow the [ROCm-examples](https://github.com/rocm/rocm-examples) building guide but also met the same problem, therefore I don't think `find_package(hip)` is an official practice. Did you try it?

When I would set my "LANGUAGE" to HIP in my CMake file, I would get the same/similar error. In my current project, I use 
```    
find_package(hip)
find_package(hipblas)
find_package(rocblas)
``` 
to make it build on Windows
https://github.com/YellowRoseCx/koboldcpp-rocm/blob/4a3626eebf36565e93b3d5f79ebbcfdcbb815d97/CMakeLists.txt#L151C1-L153C26

It's also briefly mentioned in the ROCm Documentation here: 
https://rocm.docs.amd.com/en/latest/conceptual/cmake-packages.html#consuming-the-hip-api-in-c-code


---

### 评论 #5 — harkgill-amd (2024-06-26T16:13:20Z)

Hi @GZGavinZhao, it is recommended on Windows to use `find_package(hip)` rather than setting the language through `project(MyProj LANGUAGES HIP)`, this should allow the build to complete successfully. 
```
cmake_minimum_required(VERSION 3.21)
cmake_policy(VERSION 3.21.3...3.27)
project(MyProj)
find_package(hip)
add_executable(vectoradd_hip MyProj/vectoradd_hip.cpp)
set_source_files_properties(vectoradd_hip.cpp PROPERTIES LANGUAGE HIP)
```

The error referencing `amdhip64.lib` in hip-lang-targets.cmake will also be fixed in the next release for the HIP SDK.

---

### 评论 #6 — harkgill-amd (2024-07-10T20:13:33Z)

Hi @GZGavinZhao, could you please try to use CMake with the latest HIP SDK 6.1.2. 

You should no longer see any errors if using `find_package(hip)` as mentioned above. If everything is working, please close this ticket. Thanks!

---

### 评论 #7 — harkgill-amd (2024-08-21T14:35:11Z)

Closing this issue. If you are still encountering issues with CMake on the 6.1.2 HIP SDK, please open a new ticket and we will investigate it further from there. 

---
