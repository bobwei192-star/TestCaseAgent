# [Issue]: Windows Preview PyTorch crashing

> **Issue #5440**
> **状态**: closed
> **创建时间**: 2025-09-28T07:08:50Z
> **更新时间**: 2025-10-24T14:36:07Z
> **关闭时间**: 2025-10-24T14:35:56Z
> **作者**: marcussacana
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5440

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

The recent Pytorch preview for windows crashes on 7900 XTX.
I'm using the Preview Pytorch Adrenaline Drivers.


### Operating System

Windows 24H2

### CPU

AMD Ryzen 9 7950X3D 16-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

6.4.4

### ROCm Component

_No response_

### Steps to Reproduce

1 - Clean install the [Adrenaline Preview Pytorch Driver](https://www.amd.com/en/resources/support-articles/release-notes/RN-AMDGPU-WINDOWS-PYTORCH-PREVIEW.html)
2 - Install and Setup the project (Python 3.12.0)
```ps1
git clone https://github.com/zyddnys/manga-image-translator
cd manga-image-translator
python -m venv venv
# it may be .bat instead .ps1 if on cmd
.\venv\Scripts\Activate.ps1
pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/torch-2.8.0a0%2Bgitfc14c65-cp312-cp312-win_amd64.whl
pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/torchaudio-2.6.0a0%2B1a8f621-cp312-cp312-win_amd64.whl
pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/torchvision-0.24.0a0%2Bc85f008-cp312-cp312-win_amd64.whl
pip install -r requirements.txt
cd server
# Required if integrated graphics enabled (my case)
$env:HIP_VISIBLE_DEVICES = "1"
#Use in case of CMD instead powershell
#set HIP_VISIBLE_DEVICES=1
python main.py --use-gpu
```
3 - Open the web server link that you will see on terminal, usually http://127.0.0.1:8000
4 - Copy and paste some image with text
5 - Click at "Start Translating"
6 - Go back to the terminal output, you can see pytorch crashing

```
[shared] Running ocr
Exception Code: 0xC0000094
0x00007FFFA52E98D5, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll(0x00007FFFA3FB0000) + 0x13398D5 byte(s), ?_chunk_cat_out_cuda@native@at@@YAAEAVTensor@2@V?$ArrayRef@VTensor@at@@@c10@@_J1AEAV32@@Z() + 0x37985 byte(s)
0x00007FFFA52BB03E, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll(0x00007FFFA3FB0000) + 0x130B03E byte(s), ?_chunk_cat_out_cuda@native@at@@YAAEAVTensor@2@V?$ArrayRef@VTensor@at@@@c10@@_J1AEAV32@@Z() + 0x90EE byte(s)
0x00007FFFA52B55A4, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll(0x00007FFFA3FB0000) + 0x13055A4 byte(s), ?_chunk_cat_out_cuda@native@at@@YAAEAVTensor@2@V?$ArrayRef@VTensor@at@@@c10@@_J1AEAV32@@Z() + 0x3654 byte(s)
0x00007FFFA5BE68F1, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll(0x00007FFFA3FB0000) + 0x1C368F1 byte(s), ?impl@structured_topk_out_cuda@native@at@@QEAAXAEBVTensor@3@_J1_N200@Z() + 0x161 byte(s)
0x00007FFFA5CF748A, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll(0x00007FFFA3FB0000) + 0x1D4748A byte(s), ?topk@cuda@at@@YA?AV?$tuple@VTensor@at@@V12@@std@@AEBVTensor@2@_J1_N2@Z() + 0xEA byte(s)
0x00007FFFA5E7475F, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll(0x00007FFFA3FB0000) + 0x1EC475F byte(s), ?_fused_sgd_@cuda@at@@YAXV?$ArrayRef@VTensor@at@@@c10@@00NNAEBVTensor@2@N_N22AEBV?$optional@VTensor@at@@@std@@3@Z() + 0xD751F byte(s)
0x00007FFFE52E7045, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFFE4160000) + 0x1187045 byte(s), ?redispatch@_fused_adamw_tensor_lr@_ops@at@@SA?AV?$tuple@V?$vector@VTensor@at@@V?$allocator@VTensor@at@@@std@@@std@@V12@V12@V12@V12@@std@@VDispatchKeySet@c10@@V?$ArrayRef@VTensor@at@@@7@11111AEBVTensor@3@NNNN_N3AEBV?$optional@VTensor@at@@@5@4@Z() + 0x69E55 byte(s)
0x00007FFFE51F3F7E, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFFE4160000) + 0x1093F7E byte(s), ?redispatch@topk@_ops@at@@SA?AV?$tuple@VTensor@at@@V12@@std@@VDispatchKeySet@c10@@AEBVTensor@3@VSymInt@7@_J_N4@Z() + 0xCE byte(s)
0x00007FFFE7AA8088, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFFE4160000) + 0x3948088 byte(s), ??0JitDecompRegisterer@impl@autograd@torch@@QEAA@PEAUJitDecompInterface@123@@Z() + 0x359208 byte(s)
0x00007FFFE51860C1, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFFE4160000) + 0x10260C1 byte(s), ?call@topk@_ops@at@@SA?AV?$tuple@VTensor@at@@V12@@std@@AEBVTensor@3@VSymInt@c10@@_J_N3@Z() + 0x1C1 byte(s)
0x00007FFFE4173DC1, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFFE4160000) + 0x13DC1 byte(s), ?topk_symint@Tensor@at@@QEBA?AV?$tuple@VTensor@at@@V12@@std@@VSymInt@c10@@_J_N2@Z() + 0x51 byte(s)
0x00007FFFA2B61A2C, C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_python.dll(0x00007FFFA2960000) + 0x201A2C byte(s), ?release@?$THPPointer@UTHPStorage@@@@QEAAPEAUTHPStorage@@XZ() + 0xB718C byte(s)
0x00007FFFFD5EA8C4, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x5A8C4 byte(s), PyObject_VectorcallMethod() + 0x178 byte(s)
0x00007FFFFD5CB71A, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x3B71A byte(s), PyObject_Vectorcall() + 0xB8A byte(s)
0x00007FFFFD5CABC5, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x3ABC5 byte(s), PyObject_Vectorcall() + 0x35 byte(s)
0x00007FFFFD5CCA97, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x3CA97 byte(s), _PyEval_EvalFrameDefault() + 0x767 byte(s)
0x00007FFFFD663015, C:\Python312\python312.dll(0x00007FFFFD590000) + 0xD3015 byte(s), PyErr_SetNone() + 0x18D byte(s)
0x00007FFFFD7E095D, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x25095D byte(s), PyGen_NewWithQualName() + 0x29 byte(s)
0x00007FFFFD7D7211, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x247211 byte(s), PyIter_Send() + 0x35 byte(s)
0x00007FF8CD307130, C:\Python312\DLLs\_asyncio.pyd(0x00007FF8CD300000) + 0x7130 byte(s), PyInit__asyncio() + 0x58D0 byte(s)
0x00007FF8CD306ABE, C:\Python312\DLLs\_asyncio.pyd(0x00007FF8CD300000) + 0x6ABE byte(s), PyInit__asyncio() + 0x525E byte(s)
0x00007FFFFD64F05B, C:\Python312\python312.dll(0x00007FFFFD590000) + 0xBF05B byte(s), _PyObject_MakeTpCall() + 0x9B byte(s)
0x00007FFFFD804274, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x274274 byte(s), _PyContext_NewHamtForTests() + 0x80 byte(s)
0x00007FFFFD804563, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x274563 byte(s), _PyContext_NewHamtForTests() + 0x36F byte(s)
0x00007FFFFD5A874E, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x1874E byte(s), PyUnicode_RichCompare() + 0x191E byte(s)
0x00007FFFFD608279, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x78279 byte(s), PyObject_Call() + 0x125 byte(s)
0x00007FFFFD6081C3, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x781C3 byte(s), PyObject_Call() + 0x6F byte(s)
0x00007FFFFD5D1A9B, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x41A9B byte(s), _PyEval_EvalFrameDefault() + 0x576B byte(s)
0x00007FFFFD5E4A22, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x54A22 byte(s), PyMapping_Check() + 0x222 byte(s)
0x00007FFFFD5E4081, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x54081 byte(s), PyEval_EvalCode() + 0xAD byte(s)
0x00007FFFFD5E312C, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x5312C byte(s), _PyDict_GetItemStringWithError() + 0x384 byte(s)
0x00007FFFFD5E2FD0, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x52FD0 byte(s), _PyDict_GetItemStringWithError() + 0x228 byte(s)
0x00007FFFFD5A874E, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x1874E byte(s), PyUnicode_RichCompare() + 0x191E byte(s)
0x00007FFFFD5CAC76, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x3AC76 byte(s), PyObject_Vectorcall() + 0xE6 byte(s)
0x00007FFFFD5CABC5, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x3ABC5 byte(s), PyObject_Vectorcall() + 0x35 byte(s)
0x00007FFFFD5CCA97, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x3CA97 byte(s), _PyEval_EvalFrameDefault() + 0x767 byte(s)
0x00007FFFFD5FB38A, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x6B38A byte(s), _PyFunction_Vectorcall() + 0x17A byte(s)
0x00007FFFFD608279, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x78279 byte(s), PyObject_Call() + 0x125 byte(s)
0x00007FFFFD6081C3, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x781C3 byte(s), PyObject_Call() + 0x6F byte(s)
0x00007FFFFD637FF2, C:\Python312\python312.dll(0x00007FFFFD590000) + 0xA7FF2 byte(s), PyArg_Parse() + 0x1BE byte(s)
0x00007FFFFD638723, C:\Python312\python312.dll(0x00007FFFFD590000) + 0xA8723 byte(s), Py_RunMain() + 0x333 byte(s)
0x00007FFFFD638405, C:\Python312\python312.dll(0x00007FFFFD590000) + 0xA8405 byte(s), Py_RunMain() + 0x15 byte(s)
0x00007FFFFD594845, C:\Python312\python312.dll(0x00007FFFFD590000) + 0x4845 byte(s), Py_Main() + 0x25 byte(s)
0x00007FF756E91230, C:\Python312\python.exe(0x00007FF756E90000) + 0x1230 byte(s)
0x00007FF8F346E8D7, C:\WINDOWS\System32\KERNEL32.DLL(0x00007FF8F3440000) + 0x2E8D7 byte(s), BaseThreadInitThunk() + 0x17 byte(s)
0x00007FF8F5128D9C, C:\WINDOWS\SYSTEM32\ntdll.dll(0x00007FF8F5120000) + 0x8D9C byte(s), RtlUserThreadStart() + 0x2C byte(s)
```

### Output of hipinfo

```
--------------------------------------------------------------------------------
device#                           0
Name:                             AMD Radeon(TM) Graphics
pciBusID:                         18
pciDeviceID:                      0
pciDomainID:                      0
multiProcessorCount:              1
maxThreadsPerMultiProcessor:      2048
isMultiGpuBoard:                  0
clockRate:                        2200 Mhz
memoryClockRate:                  2000 Mhz
memoryBusWidth:                   0
totalGlobalMem:                   12.20 GB
totalConstMem:                    2147483647
sharedMemPerBlock:                64.00 KB
canMapHostMemory:                 1
regsPerBlock:                     0
warpSize:                         32
l2CacheSize:                      4194304
computeMode:                      0
maxThreadsPerBlock:               1024
maxThreadsDim.x:                  1024
maxThreadsDim.y:                  1024
maxThreadsDim.z:                  1024
maxGridSize.x:                    2147483647
maxGridSize.y:                    65536
maxGridSize.z:                    65536
major:                            10
minor:                            3
concurrentKernels:                1
cooperativeLaunch:                0
cooperativeMultiDeviceLaunch:     0
isIntegrated:                     1
maxTexture1D:                     16384
maxTexture2D.width:               16384
maxTexture2D.height:              16384
maxTexture3D.width:               2048
maxTexture3D.height:              2048
maxTexture3D.depth:               2048
hostNativeAtomicSupported:        0
isLargeBar:                       0
asicRevision:                     0
maxSharedMemoryPerMultiProcessor: 64.00 KB
clockInstructionRate:             1000.00 Mhz
arch.hasGlobalInt32Atomics:       1
arch.hasGlobalFloatAtomicExch:    1
arch.hasSharedInt32Atomics:       1
arch.hasSharedFloatAtomicExch:    1
arch.hasFloatAtomicAdd:           1
arch.hasGlobalInt64Atomics:       1
arch.hasSharedInt64Atomics:       1
arch.hasDoubles:                  1
arch.hasWarpVote:                 1
arch.hasWarpBallot:               1
arch.hasWarpShuffle:              1
arch.hasFunnelShift:              0
arch.hasThreadFenceSystem:        1
arch.hasSyncThreadsExt:           0
arch.hasSurfaceFuncs:             0
arch.has3dGrid:                   1
arch.hasDynamicParallelism:       0
gcnArchName:                      gfx1036
peers:
non-peers:                        device#0 device#1

memInfo.total:                    12.20 GB
memInfo.free:                     12.06 GB (99%)
--------------------------------------------------------------------------------
device#                           1
Name:                             AMD Radeon RX 7900 XTX
pciBusID:                         3
pciDeviceID:                      0
pciDomainID:                      0
multiProcessorCount:              48
maxThreadsPerMultiProcessor:      2048
isMultiGpuBoard:                  0
clockRate:                        2526 Mhz
memoryClockRate:                  1250 Mhz
memoryBusWidth:                   0
totalGlobalMem:                   23.98 GB
totalConstMem:                    2147483647
sharedMemPerBlock:                64.00 KB
canMapHostMemory:                 1
regsPerBlock:                     0
warpSize:                         32
l2CacheSize:                      6291456
computeMode:                      0
maxThreadsPerBlock:               1024
maxThreadsDim.x:                  1024
maxThreadsDim.y:                  1024
maxThreadsDim.z:                  1024
maxGridSize.x:                    2147483647
maxGridSize.y:                    65536
maxGridSize.z:                    65536
major:                            11
minor:                            0
concurrentKernels:                1
cooperativeLaunch:                0
cooperativeMultiDeviceLaunch:     0
isIntegrated:                     0
maxTexture1D:                     16384
maxTexture2D.width:               16384
maxTexture2D.height:              16384
maxTexture3D.width:               2048
maxTexture3D.height:              2048
maxTexture3D.depth:               2048
hostNativeAtomicSupported:        1
isLargeBar:                       0
asicRevision:                     0
maxSharedMemoryPerMultiProcessor: 64.00 KB
clockInstructionRate:             1000.00 Mhz
arch.hasGlobalInt32Atomics:       1
arch.hasGlobalFloatAtomicExch:    1
arch.hasSharedInt32Atomics:       1
arch.hasSharedFloatAtomicExch:    1
arch.hasFloatAtomicAdd:           1
arch.hasGlobalInt64Atomics:       1
arch.hasSharedInt64Atomics:       1
arch.hasDoubles:                  1
arch.hasWarpVote:                 1
arch.hasWarpBallot:               1
arch.hasWarpShuffle:              1
arch.hasFunnelShift:              0
arch.hasThreadFenceSystem:        1
arch.hasSyncThreadsExt:           0
arch.hasSurfaceFuncs:             0
arch.has3dGrid:                   1
arch.hasDynamicParallelism:       0
gcnArchName:                      gfx1100
peers:
non-peers:                        device#0 device#1

memInfo.total:                    23.98 GB
memInfo.free:                     23.84 GB (99%)
```

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — schung-amd (2025-09-30T17:59:57Z)

Hi @marcussacana, it looks like you have integrated graphics enabled, which might be causing some interference; does this occur with the integrated graphics disabled?

---

### 评论 #2 — marcussacana (2025-09-30T21:10:22Z)

Hi @schung-amd, I just tried with disabled iGPU, the crashes appears again, but the log seems a bit different
```
[shared] Running ocr
Exception Code: 0xC0000094
 #0 0x00007ffecadc98d5 at::native::_chunk_cat_out_cuda(class c10::ArrayRef<class at::Tensor>, __int64, __int64, class at::Tensor &) (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll+0x13398d5)
 #1 0x00007ffecad9b03e at::native::_chunk_cat_out_cuda(class c10::ArrayRef<class at::Tensor>, __int64, __int64, class at::Tensor &) (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll+0x130b03e)
 #2 0x00007ffecad955a4 at::native::_chunk_cat_out_cuda(class c10::ArrayRef<class at::Tensor>, __int64, __int64, class at::Tensor &) (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll+0x13055a4)
 #3 0x00007ffecb6c68f1 at::native::structured_topk_out_cuda::impl(class at::Tensor const &, __int64, __int64, bool, bool, class at::Tensor const &, class at::Tensor const &) (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll+0x1c368f1)
 #4 0x00007ffecb7d748a at::cuda::topk(class at::Tensor const &, __int64, __int64, bool, bool) (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll+0x1d4748a)
 #5 0x00007ffecb95475f at::cuda::_fused_sgd_(class c10::ArrayRef<class at::Tensor>, class c10::ArrayRef<class at::Tensor>, class c10::ArrayRef<class at::Tensor>, double, double, class at::Tensor const &, double, bool, bool, bool, class std::optional<class at::Tensor> const &, class std::optional<class at::Tensor> const &) (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_hip.dll+0x1ec475f)
 #6 0x00007fff0b2d7045 at::_ops::_fused_adamw_tensor_lr::redispatch(class c10::DispatchKeySet, class c10::ArrayRef<class at::Tensor>, class c10::ArrayRef<class at::Tensor>, class c10::ArrayRef<class at::Tensor>, class c10::ArrayRef<class at::Tensor>, class c10::ArrayRef<class at::Tensor>, class c10::ArrayRef<class at::Tensor>, class at::Tensor const &, double, double, double, double, bool, bool, class std::optional<class at::Tensor> const &, class std::optional<class at::Tensor> const &) (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_cpu.dll+0x1187045)
 #7 0x00007fff0b1e3f7e at::_ops::topk::redispatch(class c10::DispatchKeySet, class at::Tensor const &, class c10::SymInt, __int64, bool, bool) (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_cpu.dll+0x1093f7e)
 #8 0x00007fff0da98088 torch::autograd::impl::JitDecompRegisterer::JitDecompRegisterer(struct torch::autograd::impl::JitDecompInterface *) (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_cpu.dll+0x3948088)
 #9 0x00007fff0b1760c1 at::_ops::topk::call(class at::Tensor const &, class c10::SymInt, __int64, bool, bool) (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_cpu.dll+0x10260c1)
#10 0x00007fff0a163dc1 at::Tensor::topk_symint(class c10::SymInt, __int64, bool, bool) const (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_cpu.dll+0x13dc1)
#11 0x00007ffec8641a2c THPPointer<struct THPStorage>::release(void) (C:\manga-image-translator\venv\Lib\site-packages\torch\lib\torch_python.dll+0x201a2c)
#12 0x00007fff2301a8c4 (C:\Python312\python312.dll+0x5a8c4)
#13 0x00007fff22ffb71a (C:\Python312\python312.dll+0x3b71a)
#14 0x00007fff22ffabc5 (C:\Python312\python312.dll+0x3abc5)
#15 0x00007fff22ffca97 (C:\Python312\python312.dll+0x3ca97)
#16 0x00007fff23093015 (C:\Python312\python312.dll+0xd3015)
#17 0x00007fff2321095d (C:\Python312\python312.dll+0x25095d)
#18 0x00007fff23207211 (C:\Python312\python312.dll+0x247211)
#19 0x00007fff322f7130 (C:\Python312\DLLs\_asyncio.pyd+0x7130)
#20 0x00007fff322f6abe (C:\Python312\DLLs\_asyncio.pyd+0x6abe)
#21 0x00007fff2307f05b (C:\Python312\python312.dll+0xbf05b)
#22 0x00007fff23234274 (C:\Python312\python312.dll+0x274274)
#23 0x00007fff23234563 (C:\Python312\python312.dll+0x274563)
#24 0x00007fff22fd874e (C:\Python312\python312.dll+0x1874e)
#25 0x00007fff23038279 (C:\Python312\python312.dll+0x78279)
#26 0x00007fff230381c3 (C:\Python312\python312.dll+0x781c3)
#27 0x00007fff23001a9b (C:\Python312\python312.dll+0x41a9b)
#28 0x00007fff23014a22 (C:\Python312\python312.dll+0x54a22)
#29 0x00007fff23014081 (C:\Python312\python312.dll+0x54081)
#30 0x00007fff2301312c (C:\Python312\python312.dll+0x5312c)
#31 0x00007fff23012fd0 (C:\Python312\python312.dll+0x52fd0)
#32 0x00007fff22fd874e (C:\Python312\python312.dll+0x1874e)
#33 0x00007fff22ffac76 (C:\Python312\python312.dll+0x3ac76)
#34 0x00007fff22ffabc5 (C:\Python312\python312.dll+0x3abc5)
#35 0x00007fff22ffca97 (C:\Python312\python312.dll+0x3ca97)
#36 0x00007fff2302b38a (C:\Python312\python312.dll+0x6b38a)
#37 0x00007fff23038279 (C:\Python312\python312.dll+0x78279)
#38 0x00007fff230381c3 (C:\Python312\python312.dll+0x781c3)
#39 0x00007fff23067ff2 (C:\Python312\python312.dll+0xa7ff2)
#40 0x00007fff23068723 (C:\Python312\python312.dll+0xa8723)
#41 0x00007fff23068405 (C:\Python312\python312.dll+0xa8405)
#42 0x00007fff22fc4845 (C:\Python312\python312.dll+0x4845)
#43 0x00007ff771751230 (C:\Python312\python.exe+0x1230)
#44 0x00007ff81308e8d7 (C:\WINDOWS\System32\KERNEL32.DLL+0x2e8d7)
#45 0x00007ff814568d9c (C:\WINDOWS\SYSTEM32\ntdll.dll+0x8d9c)
```

My new hipinfo output
```
device#                           0
Name:                             AMD Radeon RX 7900 XTX
pciBusID:                         3
pciDeviceID:                      0
pciDomainID:                      0
multiProcessorCount:              48
maxThreadsPerMultiProcessor:      2048
isMultiGpuBoard:                  0
clockRate:                        2526 Mhz
memoryClockRate:                  1250 Mhz
memoryBusWidth:                   0
totalGlobalMem:                   23.98 GB
totalConstMem:                    2147483647
sharedMemPerBlock:                64.00 KB
canMapHostMemory:                 1
regsPerBlock:                     0
warpSize:                         32
l2CacheSize:                      6291456
computeMode:                      0
maxThreadsPerBlock:               1024
maxThreadsDim.x:                  1024
maxThreadsDim.y:                  1024
maxThreadsDim.z:                  1024
maxGridSize.x:                    2147483647
maxGridSize.y:                    65536
maxGridSize.z:                    65536
major:                            11
minor:                            0
concurrentKernels:                1
cooperativeLaunch:                0
cooperativeMultiDeviceLaunch:     0
isIntegrated:                     0
maxTexture1D:                     16384
maxTexture2D.width:               16384
maxTexture2D.height:              16384
maxTexture3D.width:               2048
maxTexture3D.height:              2048
maxTexture3D.depth:               2048
hostNativeAtomicSupported:        1
isLargeBar:                       0
asicRevision:                     0
maxSharedMemoryPerMultiProcessor: 64.00 KB
clockInstructionRate:             1000.00 Mhz
arch.hasGlobalInt32Atomics:       1
arch.hasGlobalFloatAtomicExch:    1
arch.hasSharedInt32Atomics:       1
arch.hasSharedFloatAtomicExch:    1
arch.hasFloatAtomicAdd:           1
arch.hasGlobalInt64Atomics:       1
arch.hasSharedInt64Atomics:       1
arch.hasDoubles:                  1
arch.hasWarpVote:                 1
arch.hasWarpBallot:               1
arch.hasWarpShuffle:              1
arch.hasFunnelShift:              0
arch.hasThreadFenceSystem:        1
arch.hasSyncThreadsExt:           0
arch.hasSurfaceFuncs:             0
arch.has3dGrid:                   1
arch.hasDynamicParallelism:       0
gcnArchName:                      gfx1100
peers:
non-peers:                        device#0

memInfo.total:                    23.98 GB
memInfo.free:                     23.84 GB (99%)
```

---

### 评论 #3 — schung-amd (2025-10-22T20:22:13Z)

Thanks for the reply, sorry for the delay on this. Have you tried ROCm 7.0.2, and if so do you see this issue there? Will try to repro later this week.

---

### 评论 #4 — marcussacana (2025-10-22T22:07:51Z)

There are a different build than this for windows?
https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/

---

### 评论 #5 — schung-amd (2025-10-23T18:20:56Z)

Yes, we have releases for ROCm 7.0.2; see updated instructions at https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-pytorch.html. I assume you'll also need ROCm 7.0.2 (instructions can be found in those same docs) which is a preview release, so there may be other issues, but curious to see if this addresses the issue you're seeing here.

---

### 评论 #6 — marcussacana (2025-10-23T23:22:22Z)

I tested the prerelease of ROCm 7.x as long newest pytorch and the issue didn't happens at all, seems to be a issue already fixed in this case, the tool is now working fine, my thanks, I think it's fine to close the issue

---

### 评论 #7 — schung-amd (2025-10-24T14:35:56Z)

Great, glad to hear things are working for you. I'll close this for now then, if I see it elsewhere or if you run into related problems we can reopen if necessary. Thanks for the report!

---
