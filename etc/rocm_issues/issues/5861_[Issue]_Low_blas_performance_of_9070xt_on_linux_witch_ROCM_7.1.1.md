# [Issue]: Low blas performance of 9070xt on linux witch ROCM 7.1.1

> **Issue #5861**
> **状态**: open
> **创建时间**: 2026-01-16T14:18:49Z
> **更新时间**: 2026-04-22T21:17:04Z
> **作者**: ca1ic0
> **标签**: Under Investigation, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5861

## 标签

- **Under Investigation** (颜色: #0052cc)
- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

I clean install an ubuntu24.04 and install rocm7.1.1. I use the [https://github.com/ROCm/mblas-bench](mblas-bench) to do a benchmark. However, the fp32 flops is `12TFLOPS` which is much lower than the peak `48.7TFLOPS`. And the fp16 flops is  `70TFLOPS` which lower than the peak  vector flops `97.3TLOPS` or the peak mma flops `389TFLOPS`.

```bash
(base) calico@calico-System-Product-Name:~/code/mblas-bench$ build/mblas-bench -m 4096 -n 4096 -k 4096 --alpha 1 --beta 0 --transposeA N --transposeB T --initialization trig_float --iters 100 --cold_iters 2 --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --compute_type f32_r --function matmul --rotating 512 --driver ${DRIVER}
Using flush_batch_count = 1
transA_option,transB_option,M,N,K,lda,ldb,ldc,hipBLASLt-Gflops,hipBLASLt-GB/s,hipBLASLt-us,
N,T,4096,4096,4096,4096,4096,4096,11755.29,17.21966,11691.67,
```

```bash
(base) calico@calico-System-Product-Name:~/code/mblas-bench$ build/mblas-bench -m 4096 -n 4096 -k 4096 --alpha 1 --beta 0 --transposeA N --transposeB T --initialization trig_float --iters 10 --cold_iters 2 --a_type f16_r --b_type f16_r --c_type f16_r --d_type f16_r --compute_type f32_r --function matmul --rotating 512 --driver ${DRIVER}
Using flush_batch_count = 3
transA_option,transB_option,M,N,K,lda,ldb,ldc,hipBLASLt-Gflops,hipBLASLt-GB/s,hipBLASLt-us,
N,T,4096,4096,4096,4096,4096,4096,71130.39,52.09745,1932.211,
```

### Operating System

Ubuntu24.04LTS

### CPU

Ryzen9600x

### GPU

RX9070xt

### ROCm Version

ROCm 7.1.1

### ROCm Component

rocBLAS

### Steps to Reproduce

```bash
git clone git@github.com:ROCm/mblas-bench.git
cd mblas-bench

cmake -S src -B build -DWITH_ROCM=true -DWITH_CUDA=false  
cmake --build build -j 

export DRIVER="hipblaslt"

build/mblas-bench -m 4096 -n 4096 -k 4096 --alpha 1 --beta 0 --transposeA N --transposeB T --initialization trig_float --iters 10 --cold_iters 2 --a_type f32_r --b_type f32_r --c_type f32_r --d_type f32_r --compute_type f32_r --function matmul --rotating 512 --driver ${DRIVER}
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

(base) calico@calico-System-Product-Name:~/code/mblas-bench$ /opt/rocm/bin/rocminfo --support
ROCk module version 6.16.6 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.14
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
  Name:                    AMD Ryzen 5 9600X 6-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 9600X 6-Core Processor 
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
  Max Clock Freq. (MHz):   5486                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    31994972(0x1e8345c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    31994972(0x1e8345c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    31994972(0x1e8345c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31994972(0x1e8345c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-33cdcaebba902e5f               
  Marketing Name:          AMD Radeon RX 9070 XT              
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30032(0x7550)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2570                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
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
  Packet Processor uCode:: 108                                
  SDMA engine uCode::      662                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16695296(0xfec000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1201         
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
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
  Name:                    gfx1036                            
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
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      256(0x100) KB                      
  Chip ID:                 5056(0x13c0)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   3584                               
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
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
  Packet Processor uCode:: 121                                
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    15997484(0xf41a2c) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    15997484(0xf41a2c) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1036         
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
      Name:                    amdgcn-amd-amdhsa--gfx10-3-generic 
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
*** Done ***  

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — ca1ic0 (2026-01-17T00:55:32Z)

When using Torch:
```
import torch
import time
import numpy as np
from typing import Tuple

def gemm_performance_test(
    M: int = 4096,
    N: int = 4096,
    K: int = 4096,
    dtype: torch.dtype = torch.float32,
    num_warmup: int = 10,
    num_iter: int = 100,
    use_cuda: bool = torch.cuda.is_available()
) -> Tuple[float, float]:
    """
    测试GEMM性能并返回带宽和FLOPS
    
    Args:
        M, N, K: 矩阵维度 (M x K) * (K x N) = (M x N)
        dtype: 数据类型
        num_warmup: 预热迭代次数
        num_iter: 测试迭代次数
        use_cuda: 是否使用CUDA
    """
    
    # 设置设备
    device = torch.device('cuda' if use_cuda else 'cpu')
    print(f"测试设备: {device}")
    print(f"矩阵维度: A[{M}x{K}] * B[{K}x{N}] = C[{M}x{N}]")
    print(f"数据类型: {dtype}")
    
    # 创建随机矩阵
    A = torch.randn(M, K, dtype=dtype, device=device)
    B = torch.randn(K, N, dtype=dtype, device=device)
    
    # 预热
    print("预热中...")
    for _ in range(num_warmup):
        C = torch.matmul(A, B)
    if use_cuda:
        torch.cuda.synchronize()
    
    # 性能测试
    print("性能测试中...")
    start_time = time.perf_counter()
    
    for _ in range(num_iter):
        C = torch.matmul(A, B)
    
    if use_cuda:
        torch.cuda.synchronize()
    
    end_time = time.perf_counter()
    
    # 计算统计信息
    elapsed_time = (end_time - start_time) / num_iter  # 平均单次运行时间
    total_flops = 2 * M * N * K  # GEMM的总浮点运算次数: 2*M*N*K (乘加各算一次)
    
    # 计算带宽 (读取A和B，写入C)
    if dtype == torch.float32 or dtype == torch.float:
        bytes_per_element = 4
    elif dtype == torch.float64 or dtype == torch.double:
        bytes_per_element = 8
    elif dtype == torch.float16 or dtype == torch.half:
        bytes_per_element = 2
    elif dtype == torch.bfloat16:
        bytes_per_element = 2
    else:
        bytes_per_element = 4  # 默认
    
    # 内存访问量: 读取A + 读取B + 写入C
    memory_access = (M * K + K * N + M * N) * bytes_per_element
    
    # 计算性能指标
    flops = total_flops / elapsed_time  # FLOPS
    bandwidth = memory_access / elapsed_time / 1e9  # 带宽 (GB/s)
    
    return flops, bandwidth

def format_number(num: float) -> str:
    """格式化大数字显示"""
    if num >= 1e12:
        return f"{num/1e12:.2f} T"
    elif num >= 1e9:
        return f"{num/1e9:.2f} G"
    elif num >= 1e6:
        return f"{num/1e6:.2f} M"
    elif num >= 1e3:
        return f"{num/1e3:.2f} K"
    else:
        return f"{num:.2f}"

def main():
    """主测试函数"""
    
    # 测试配置
    test_cases = [
        {"M": 1024, "N": 1024, "K": 1024, "name": "小规模 (1Kx1K)"},
        {"M": 2048, "N": 2048, "K": 2048, "name": "中规模 (2Kx2K)"},
        {"M": 4096, "N": 4096, "K": 4096, "name": "大规模 (4Kx4K)"},
        {"M": 8192, "N": 8192, "K": 8192, "name": "超大规模 (8Kx8K)"},
    ]
    
    dtypes_to_test = []
    if torch.cuda.is_available():
        dtypes_to_test = [
            (torch.float32, "FP32"),
            (torch.float16, "FP16"),
        ]
        # 检查是否支持bfloat16
        if torch.cuda.is_bf16_supported():
            dtypes_to_test.append((torch.bfloat16, "BF16"))
    else:
        dtypes_to_test = [
            (torch.float32, "FP32"),
            (torch.float64, "FP64"),
        ]
    
    print("=" * 70)
    print("GEMM性能测试报告")
    print("=" * 70)
    
    for test_case in test_cases:
        M, N, K = test_case["M"], test_case["N"], test_case["K"]
        print(f"\n{test_case['name']}:")
        print("-" * 50)
        
        for dtype, dtype_name in dtypes_to_test:
            try:
                flops, bandwidth = gemm_performance_test(
                    M=M, N=N, K=K,
                    dtype=dtype,
                    num_warmup=5,
                    num_iter=20,
                    use_cuda=torch.cuda.is_available()
                )
                
                # 打印结果
                print(f"{dtype_name}:")
                print(f"  → 性能: {format_number(flops)}FLOPS")
                print(f"  → 带宽: {bandwidth:.2f} GB/s")
                print(f"  → 计算强度: {flops/bandwidth/1e9:.2f} FLOPs/byte")
                
            except RuntimeError as e:
                print(f"{dtype_name}: 测试失败 - {str(e)}")
                continue
    
    # 添加理论峰值计算（仅CUDA）
    if torch.cuda.is_available():
        print("\n" + "=" * 70)
        print("CUDA设备信息:")
        print("-" * 50)
        device_props = torch.cuda.get_device_properties(0)
        print(f"设备名称: {device_props.name}")
        print(f"计算能力: {device_props.major}.{device_props.minor}")
        print(f"SM数量: {device_props.multi_processor_count}")
        
        # 估算理论峰值FLOPS（简化版本）
        clock_rate = device_props.clock_rate / 1e6  # GHz
        # 假设每个SM每个时钟周期可以执行一定数量的FP32运算
        # 这只是一个粗略估计，实际值取决于架构
        theoretical_tflops_fp32 = (device_props.multi_processor_count * 
                                  clock_rate * 128) / 1e3  # 简化模型
        
        print(f"估算理论峰值FP32性能: {theoretical_tflops_fp32:.2f} TFLOPS")
        print(f"显存大小: {device_props.total_memory / 1e9:.2f} GB")
        print(f"显存带宽: {device_props.memory_clock_rate * 2 * 
                           device_props.memory_bus_width / 8 / 1e6:.2f} GB/s")

if __name__ == "__main__":
    main()
```
```bash
torch-rocm) calico@calico-System-Product-Name:~/code/torch-rocm$ python3 gemm.py 
======================================================================
GEMM性能测试报告
======================================================================

小规模 (1Kx1K):
--------------------------------------------------
测试设备: cuda
矩阵维度: A[1024x1024] * B[1024x1024] = C[1024x1024]
数据类型: torch.float32
预热中...
性能测试中...
FP32:
  → 性能: 5.63 TFLOPS
  → 带宽: 32.96 GB/s
  → 计算强度: 170.67 FLOPs/byte
测试设备: cuda
矩阵维度: A[1024x1024] * B[1024x1024] = C[1024x1024]
数据类型: torch.float16
预热中...
性能测试中...
FP16:
  → 性能: 46.65 TFLOPS
  → 带宽: 136.68 GB/s
  → 计算强度: 341.33 FLOPs/byte
测试设备: cuda
矩阵维度: A[1024x1024] * B[1024x1024] = C[1024x1024]
数据类型: torch.bfloat16
预热中...
性能测试中...
BF16:
  → 性能: 47.42 TFLOPS
  → 带宽: 138.94 GB/s
  → 计算强度: 341.33 FLOPs/byte

中规模 (2Kx2K):
--------------------------------------------------
测试设备: cuda
矩阵维度: A[2048x2048] * B[2048x2048] = C[2048x2048]
数据类型: torch.float32
预热中...
性能测试中...
FP32:
  → 性能: 8.15 TFLOPS
  → 带宽: 23.89 GB/s
  → 计算强度: 341.33 FLOPs/byte
测试设备: cuda
矩阵维度: A[2048x2048] * B[2048x2048] = C[2048x2048]
数据类型: torch.float16
预热中...
性能测试中...
FP16:
  → 性能: 68.80 TFLOPS
  → 带宽: 100.78 GB/s
  → 计算强度: 682.67 FLOPs/byte
测试设备: cuda
矩阵维度: A[2048x2048] * B[2048x2048] = C[2048x2048]
数据类型: torch.bfloat16
预热中...
性能测试中...
BF16:
  → 性能: 74.66 TFLOPS
  → 带宽: 109.36 GB/s
  → 计算强度: 682.67 FLOPs/byte

大规模 (4Kx4K):
--------------------------------------------------
测试设备: cuda
矩阵维度: A[4096x4096] * B[4096x4096] = C[4096x4096]
数据类型: torch.float32
预热中...
性能测试中...
FP32:
  → 性能: 12.68 TFLOPS
  → 带宽: 18.58 GB/s
  → 计算强度: 682.67 FLOPs/byte
测试设备: cuda
矩阵维度: A[4096x4096] * B[4096x4096] = C[4096x4096]
数据类型: torch.float16
预热中...
性能测试中...
FP16:
  → 性能: 123.59 TFLOPS
  → 带宽: 90.52 GB/s
  → 计算强度: 1365.33 FLOPs/byte
测试设备: cuda
矩阵维度: A[4096x4096] * B[4096x4096] = C[4096x4096]
数据类型: torch.bfloat16
预热中...
性能测试中...
BF16:
  → 性能: 122.97 TFLOPS
  → 带宽: 90.06 GB/s
  → 计算强度: 1365.33 FLOPs/byte

超大规模 (8Kx8K):
--------------------------------------------------
测试设备: cuda
矩阵维度: A[8192x8192] * B[8192x8192] = C[8192x8192]
数据类型: torch.float32
预热中...
性能测试中...
FP32:
  → 性能: 1.42 TFLOPS
  → 带宽: 1.04 GB/s
  → 计算强度: 1365.33 FLOPs/byte
测试设备: cuda
矩阵维度: A[8192x8192] * B[8192x8192] = C[8192x8192]
数据类型: torch.float16
预热中...
性能测试中...
FP16:
  → 性能: 110.47 TFLOPS
  → 带宽: 40.45 GB/s
  → 计算强度: 2730.67 FLOPs/byte
测试设备: cuda
矩阵维度: A[8192x8192] * B[8192x8192] = C[8192x8192]
数据类型: torch.bfloat16
预热中...
性能测试中...
BF16:
  → 性能: 111.76 TFLOPS
  → 带宽: 40.93 GB/s
  → 计算强度: 2730.67 FLOPs/byte
======================================================================
```

---

### 评论 #2 — tcgu-amd (2026-01-21T17:58:17Z)

Hi @ca1ic0, thanks for reaching out! Yes I think you are describing a known issue where hipblaslt kernels are not optimized on gfx12. We are currently tuning them and the updated configurations will be rolled out in future ROCm releases. Thanks!  

---

### 评论 #3 — bbslxj (2026-04-22T21:17:04Z)

@tcgu-amd Any updates on the tuning for gfx12? Looking at the 8Kx8K results, the FP32 performance (only 1.42 TFLOPS) suggests that the AI cores are not being engaged properly, indicating a severe bottleneck in the current rocBLAS/hipblaslt implementation for this scale.

---
