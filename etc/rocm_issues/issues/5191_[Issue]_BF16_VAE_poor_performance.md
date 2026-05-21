# [Issue]: BF16 VAE poor performance

> **Issue #5191**
> **状态**: open
> **创建时间**: 2025-08-13T00:46:00Z
> **更新时间**: 2025-12-23T16:41:53Z
> **作者**: YuChuXi
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5191

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 负责人

- tcgu-amd

## 描述

### Problem Description

I observed that BF16 VAE is much slower than FP16 and is more prone to OOM.  


### Operating System

Ubuntu 24.04.2 LTS (Noble Numbat)

### CPU

7950X

### GPU

AMD Radeon RX7900XTX

### ROCm Version

ROCm 6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

Execute the following Python file, which can calculate the performance overhead  

```shell
# I found these environment variables from related cases on the Internet, but they didn't seem to bring any improvement.
export PYTORCH_HIP_ALLOC_CONF=expandable_segments:True
export HIPDNN_BENCHMARK=1
export MIOPEN_FIND_MODE=2
python vae_benchmark.py
```

```python
import torch
from diffusers import AutoencoderKL
from PIL import Image
import time
import torchvision.transforms as T
from collections import defaultdict

class ModuleTimer:
    def __init__(self):
        self.module_times = defaultdict(float)
        self.module_counts = defaultdict(int)
        self.module_peak_mems = defaultdict(float) # Store peak memory for each module
        self.handles = []
        self.current_module_name = None
        self.start_time = None

    def _pre_hook(self, module, input):
        torch.cuda.synchronize()
        self.start_time = time.time()
        # Reset peak memory stats before each module call to get accurate peak for that module
        torch.cuda.reset_peak_memory_stats(torch.cuda.current_device())

    def _post_hook(self, module, input, output):
        torch.cuda.synchronize()
        end_time = time.time()
        if self.start_time is not None: # Ensure timing started
            duration = end_time - self.start_time
            peak_mem = torch.cuda.max_memory_allocated(torch.cuda.current_device()) / (1024 ** 2)
            
            self.module_times[self.current_module_name] += duration
            self.module_counts[self.current_module_name] += 1
            # Store the maximum peak memory observed for this module
            self.module_peak_mems[self.current_module_name] = max(self.module_peak_mems[self.current_module_name], peak_mem)
            
        self.start_time = None
        self.current_module_name = None # Reset for next module

    def register_hooks(self, model):
        for name, module in model.named_modules():
            if not list(module.children()): # Only register to leaf modules
                # Bind the module name to the pre-hook and post-hook
                def pre_hook_closure(mod, inp, module_name=name):
                    self.current_module_name = module_name
                    self._pre_hook(mod, inp)
                
                def post_hook_closure(mod, inp, out, module_name=name):
                    self.current_module_name = module_name # Ensure correct name for post_hook
                    self._post_hook(mod, inp, out)

                handle_pre = module.register_forward_pre_hook(pre_hook_closure)
                self.handles.append(handle_pre)
                handle_post = module.register_forward_hook(post_hook_closure)
                self.handles.append(handle_post)

    def remove_hooks(self):
        for handle in self.handles:
            handle.remove()
        self.handles = []

    def get_average_times(self):
        avg_times = {}
        for name, total_time in self.module_times.items():
            if self.module_counts[name] > 0:
                avg_times[name] = total_time / self.module_counts[name]
        return avg_times

def benchmark_vae_performance(model, image_tensor, dtype, device='cuda'):
    """
    Benchmarks the VAE performance for a given data type, including time and memory.
    Reports separate metrics for a warm-up run and subsequent timed runs,
    with fine-grained timing for each module using forward hooks.
    """
    print(f"--- Benchmarking {dtype} ---")
    try:
        model.to(device).to(dtype)
        image_tensor = image_tensor.to(device).to(dtype)

        # --- Warm-up Run (Full Encode/Decode) ---
        torch.cuda.reset_peak_memory_stats(device)
        torch.cuda.synchronize(device)
        start_time = time.time()
        with torch.no_grad():
            latents = model.encode(image_tensor).latent_dist.sample()
            _ = model.decode(latents)
        torch.cuda.synchronize(device)
        warmup_total_time = time.time() - start_time
        warmup_total_mem = torch.cuda.max_memory_allocated(device) / (1024 ** 2)
        print(f"Warm-up (Full) -> Total Time: {warmup_total_time:.4f}s, Peak Memory: {warmup_total_mem:.2f} MB")

        # --- Fine-grained Timed Runs (10 runs) ---
        encoder_timer = ModuleTimer()
        decoder_timer = ModuleTimer()

        encoder_timer.register_hooks(model.encoder)
        decoder_timer.register_hooks(model.decoder)
        
        print("\n--- Fine-grained Timed Runs (Avg of 10) ---")
        for i in range(10):
            # Reset memory stats for the entire run before each full encode/decode cycle
            torch.cuda.reset_peak_memory_stats(device) 
            with torch.no_grad():
                latents = model.encode(image_tensor).latent_dist.sample()
                _ = model.decode(latents)
            # No need to track peak_mem_fine_grained here, as ModuleTimer tracks per-module peak mem

        encoder_avg_times = encoder_timer.get_average_times()
        decoder_avg_times = decoder_timer.get_average_times()
        encoder_peak_mems = encoder_timer.module_peak_mems
        decoder_peak_mems = decoder_timer.module_peak_mems

        encoder_timer.remove_hooks()
        decoder_timer.remove_hooks()

        return {
            'warmup_total_time': warmup_total_time,
            'warmup_total_mem_mb': warmup_total_mem,
            'fine_grained_encoder_times': encoder_avg_times,
            'fine_grained_decoder_times': decoder_avg_times,
            'fine_grained_encoder_mems': encoder_peak_mems,
            'fine_grained_decoder_mems': decoder_peak_mems,
        }

    except Exception as e:
        print(f"Failed to benchmark {dtype}: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    image_path = "image_a.jpg" # Replace with any image path
    model_id = "madebyollin/sdxl-vae-fp16-fix"
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    if device == 'cpu':
        print("CUDA not available.")
        return
    
    print(f"Loading VAE model: {model_id}")
    vae = AutoencoderKL.from_pretrained(model_id)
    
    print(f"Loading image: {image_path}")
    image = Image.open(image_path).convert("RGB")
    
    transform = T.Compose([
        T.Resize((1024, 1024)),
        T.ToTensor(),
        T.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    image_tensor = transform(image).unsqueeze(0)

    results = {}
    
    results['fp16'] = benchmark_vae_performance(vae, image_tensor, torch.float16, device)

    if torch.cuda.is_available() and torch.cuda.is_bf16_supported():
        results['bf16'] = benchmark_vae_performance(vae, image_tensor, torch.bfloat16, device)
    else:
        print("\n--- Benchmarking bf16 ---")
        print("Skipping bfloat16 benchmark: Not supported on this hardware.")

    print("\n--- Final Benchmark Summary ---")
    for dtype, data in results.items():
        if data:
            print(f"{dtype.upper()}:")
            print(f"  Warm-up (Full) -> Total Time: {data['warmup_total_time']:.4f}s, Peak Memory: {data['warmup_total_mem_mb']:.2f} MB")
            print("  Fine-grained Encoder Times (Avg per call):")
            for k, v in sorted(data['fine_grained_encoder_times'].items(), key=lambda item: item[1], reverse=True):
                print(f"    {k:<40}: {v:.6f}s")
            print("  Fine-grained Encoder Peak Memory (per call):")
            for k, v in sorted(data['fine_grained_encoder_mems'].items(), key=lambda item: item[1], reverse=True):
                print(f"    {k:<40}: {v:.2f} MB")
            print("  Fine-grained Decoder Times (Avg per call):")
            for k, v in sorted(data['fine_grained_decoder_times'].items(), key=lambda item: item[1], reverse=True):
                print(f"    {k:<40}: {v:.6f}s")
            print("  Fine-grained Decoder Peak Memory (per call):")
            for k, v in sorted(data['fine_grained_decoder_mems'].items(), key=lambda item: item[1], reverse=True):
                print(f"    {k:<40}: {v:.2f} MB")
    print("-----------------------------")

    # Calculate and print BF16/FP16 ratios for each module
    if 'fp16' in results and results['fp16'] and 'bf16' in results and results['bf16']:
        print("\n--- BF16 / FP16 Performance Ratios (Time and Memory) ---")
        fp16_enc_times = results['fp16']['fine_grained_encoder_times']
        bf16_enc_times = results['bf16']['fine_grained_encoder_times']
        fp16_dec_times = results['fp16']['fine_grained_decoder_times']
        bf16_dec_times = results['bf16']['fine_grained_decoder_times']

        fp16_enc_mems = results['fp16']['fine_grained_encoder_mems']
        bf16_enc_mems = results['bf16']['fine_grained_encoder_mems']
        fp16_dec_mems = results['fp16']['fine_grained_decoder_mems']
        bf16_dec_mems = results['bf16']['fine_grained_decoder_mems']

        print("\nEncoder Module Ratios (BF16 / FP16):")
        all_encoder_modules = sorted(set(fp16_enc_times.keys()) | set(bf16_enc_times.keys()))
        for module_name in all_encoder_modules:
            fp16_time = fp16_enc_times.get(module_name, 0)
            bf16_time = bf16_enc_times.get(module_name, 0)
            fp16_mem = fp16_enc_mems.get(module_name, 0)
            bf16_mem = bf16_enc_mems.get(module_name, 0)

            time_ratio = bf16_time / fp16_time if fp16_time > 0 else float('nan')
            mem_ratio = bf16_mem / fp16_mem if fp16_mem > 0 else float('nan')
            
            time_ratio_str = f"{time_ratio:.3f}"
            mem_ratio_str = f"{mem_ratio:.3f}"

            # Apply red color if ratio is significantly higher than 1.0 (e.g., > 1.1)
            if time_ratio > 1.1:
                time_ratio_str = f"\033[91m{time_ratio_str}\033[0m" # Red color
            if mem_ratio > 1.1:
                mem_ratio_str = f"\033[91m{mem_ratio_str}\033[0m" # Red color
            
            print(f"  {module_name:<40}: Time Ratio={time_ratio_str}, Memory Ratio={mem_ratio_str}")

        print("\nDecoder Module Ratios (BF16 / FP16):")
        all_decoder_modules = sorted(set(fp16_dec_times.keys()) | set(bf16_dec_times.keys()))
        for module_name in all_decoder_modules:
            fp16_time = fp16_dec_times.get(module_name, 0)
            bf16_time = bf16_dec_times.get(module_name, 0)
            fp16_mem = fp16_dec_mems.get(module_name, 0)
            bf16_mem = bf16_dec_mems.get(module_name, 0)

            time_ratio = bf16_time / fp16_time if fp16_time > 0 else float('nan')
            mem_ratio = bf16_mem / fp16_mem if fp16_mem > 0 else float('nan')
            
            time_ratio_str = f"{time_ratio:.3f}"
            mem_ratio_str = f"{mem_ratio:.3f}"

            # Apply red color if ratio is significantly higher than 1.0 (e.g., > 1.1)
            if time_ratio > 1.1:
                time_ratio_str = f"\033[91m{time_ratio_str}\033[0m" # Red color
            if mem_ratio > 1.1:
                mem_ratio_str = f"\033[91m{mem_ratio_str}\033[0m" # Red color
            
            print(f"  {module_name:<40}: Time Ratio={time_ratio_str}, Memory Ratio={mem_ratio_str}")
    else:
        print("\nCould not calculate BF16 / FP16 ratios: Missing data.")

if __name__ == "__main__":
    main()

```

It's important to note that BF16 requires more time and VRAM than FP16 in some aspects, especially conv_out which can be up to ten times higher.
Be like:
<img width="852" height="601" alt="Image" src="https://github.com/user-attachments/assets/ce5919f2-856a-4808-9e99-5df4aaf77575" />


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
  Name:                    AMD Ryzen 9 7950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7950X 16-Core Processor
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
  Max Clock Freq. (MHz):   5883                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    97950900(0x5d69cb4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    97950900(0x5d69cb4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    97950900(0x5d69cb4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    97950900(0x5d69cb4) KB             
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
  Uuid:                    GPU-08ca8cb142948e79               
  Marketing Name:          Radeon RX 7900 XTX                 
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
    L2:                      6144(0x1800) KB                    
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2526                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 542                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
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
  Chip ID:                 5710(0x164e)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   6400                               
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 22                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    48975448(0x2eb4e58) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    48975448(0x2eb4e58) KB             
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***         

### Additional Information

_No response_

---

## 评论 (11 条)

### 评论 #1 — harkgill-amd (2025-08-13T21:06:35Z)

Hi @YuChuXi, thanks for the report and the detailed reproducer. We'll give it a try on our end and circle back.

---

### 评论 #2 — YuChuXi (2025-08-14T05:55:41Z)

I tested it again on ROCm6.4.2 and PyTorch2.8.0, 2.9.0.dev20250811, torch-2.9.0.dev20250813, and the problem still exists  


---

### 评论 #3 — tcgu-amd (2025-08-14T15:23:12Z)

> I tested it again on ROCm6.4.2 and PyTorch2.8.0, 2.9.0.dev20250811, torch-2.9.0.dev20250813, and the problem still exists

@YuChuXi Thanks for reaching out! Can you try with MIOPEN_ENABLE_LOGGING_CMD=1 and show us the outputs? Thanks! 

---

### 评论 #4 — YuChuXi (2025-08-14T16:50:16Z)

> > 我在 ROCm6.4.2 和 PyTorch2.8.0、2.9.0.dev20250811、torch-2.9.0.dev20250813 上再次测试，问题依然存在I tested it again on ROCm6.4.2 and PyTorch2.8.0, 2.9.0.dev20250811, torch-2.9.0.dev20250813, and the problem still exists
> 
> [@YuChuXi](https://github.com/YuChuXi)感谢您的联系！您能尝试一下 MIOPEN_ENABLE_LOGGING_CMD=1 并展示一下输出结果吗？谢谢！ Thanks for reaching out! Can you try with MIOPEN_ENABLE_LOGGING_CMD=1 and show us the outputs? Thanks!

OK, the output is a bit long, I wrote it to the file  
`MIOPEN_ENABLE_LOGGING_CMD=5 python vae_benchmark.py > cmds.log 2>&1`  
 [cmds.log](https://github.com/user-attachments/files/21777118/cmds.log)  

There are also the following logs, hope this helps  
`MIOPEN_LOG_LEVEL=6 python3 vae_benchmark.py > level6.log 2>&1`

[level6.log](https://github.com/user-attachments/files/21777186/level6.log)

---

### 评论 #5 — tcgu-amd (2025-08-14T16:51:41Z)

Thanks! 

---

### 评论 #6 — tcgu-amd (2025-08-14T18:22:41Z)

Hi @YuChuXi. It seems like this is expected. The issue is that fp16 were able to utilize more advanced winograd algorithm, which is not supported on bf16 by MIOpen. There's currently no short term plan to release bf16 support for winograd to the Radeon series, as far as I am aware. However, we are constantly working on adding more support to MIOpen, so please stay tuned. For now, unfortunately, this is the current state things. I would advise sticking to fp16 or fp32 for now if memory and speed are your main concerns. Thanks! 

---

### 评论 #7 — tcgu-amd (2025-08-14T18:23:28Z)

For reference, please see attached logs 

['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '256', '-H', '512', '-W', '512', '-k', '256', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 256 -H 512 -W 512 -k 256 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 2.539060 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 256, 512, 512, 3, 3, 256,  309237645312, 135397376, 134217728, 121792, 106, 2.539060
Forward Convolution Verifies OK on GPU reference (0.00037644 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '256', '-H', '256', '-W', '256', '-k', '512', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 256 -H 256 -W 256 -k 512 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 1.596283 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 256, 256, 256, 3, 3, 512,  154618822656, 35913728, 67108864, 96862, 65, 1.596283
Forward Convolution Verifies OK on GPU reference (0.000387208 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '512', '-H', '128', '-W', '128', '-k', '512', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 512 -H 128 -W 128 -k 512 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 84/ConvBinWinogradRxSf2x3g1
GPU Kernel Time Forward Conv. Elapsed: 1.117565 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 512, 128, 128, 3, 3, 512,  77309411328, 21495808, 16777216, 69177, 34, 1.117565
Forward Convolution Verifies OK on GPU reference (0.00011947 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '128', '-H', '512', '-W', '512', '-k', '256', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 128 -H 512 -W 512 -k 256 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 88/GemmFwd1x1_0_1
GPU Kernel Time Forward Conv. Elapsed: 0.514266 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 128, 512, 512, 1, 1, 256,  17179869184, 67174400, 134217728, 33407, 392, 0.514266
Forward Convolution Verifies OK on GPU reference (4.58707e-06 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '128', '-H', '1025', '-W', '1025', '-k', '128', '-y', '3', '-x', '3', '-p', '0', '-q', '0', '-u', '2', '-v', '2', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 128 -H 1025 -W 1025 -k 128 -y 3 -x 3 -p 0 -q 0 -u 2 -v 2 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 37/ConvBinWinogradRxSf3x2
GPU Kernel Time Forward Conv. Elapsed: 1.800405 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u2, 1, 128, 512, 512, 3, 3, 128,  77309411328, 269254912, 67108864, 42940, 187, 1.800405
Forward Convolution Verifies OK on GPU reference (0.000118173 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '3', '-H', '1024', '-W', '1024', '-k', '128', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 3 -H 1024 -W 1024 -k 128 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 84/ConvBinWinogradRxSf2x3g1
GPU Kernel Time Forward Conv. Elapsed: 0.971614 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 3, 1024, 1024, 3, 3, 128,  7247757312, 6298368, 268435456, 7460, 283, 0.971614
Forward Convolution Verifies OK on GPU reference (0.000138464 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '128', '-H', '512', '-W', '512', '-k', '256', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 128 -H 512 -W 512 -k 256 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 88/GemmFwd1x1_0_1
GPU Kernel Time Forward Conv. Elapsed: 0.642458 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 128, 512, 512, 1, 1, 256,  17179869184, 67174400, 134217728, 26741, 313, 0.642458
Forward Convolution Verifies OK on GPU reference (3.12713e-06 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '128', '-H', '1024', '-W', '1024', '-k', '3', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 128 -H 1024 -W 1024 -k 3 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 8.899709 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 128, 1024, 1024, 3, 3, 3,  7247757312, 268442368, 6291456, 814, 31, 8.899709
Forward Convolution Verifies OK on GPU reference (1.92295e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '8', '-H', '128', '-W', '128', '-k', '8', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 8 -H 128 -W 128 -k 8 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 0.016209 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 8, 128, 128, 1, 1, 8,  2097152, 262272, 262144, 129, 32, 0.016209
Forward Convolution Verifies OK on GPU reference (0.000671408 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '3', '-H', '1024', '-W', '1024', '-k', '128', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 3 -H 1024 -W 1024 -k 128 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 1.212810 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 3, 1024, 1024, 3, 3, 128,  7247757312, 6298368, 268435456, 5976, 227, 1.212810
Forward Convolution Verifies OK on GPU reference (2.41662e-06 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '128', '-H', '1025', '-W', '1025', '-k', '128', '-y', '3', '-x', '3', '-p', '0', '-q', '0', '-u', '2', '-v', '2', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 128 -H 1025 -W 1025 -k 128 -y 3 -x 3 -p 0 -q 0 -u 2 -v 2 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 3.698522 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u2, 1, 128, 512, 512, 3, 3, 128,  77309411328, 269254912, 67108864, 20903, 91, 3.698522
Forward Convolution Verifies OK on GPU reference (1.03228e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '256', '-H', '1024', '-W', '1024', '-k', '128', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 256 -H 1024 -W 1024 -k 128 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 88/GemmFwd1x1_0_1
GPU Kernel Time Forward Conv. Elapsed: 1.993599 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 256, 1024, 1024, 1, 1, 128,  68719476736, 536936448, 268435456, 34470, 404, 1.993599
Forward Convolution Verifies OK on GPU reference (8.14301e-06 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '256', '-H', '1024', '-W', '1024', '-k', '128', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 256 -H 1024 -W 1024 -k 128 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 19.576643 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 256, 1024, 1024, 3, 3, 128,  618475290624, 537460736, 268435456, 31593, 41, 19.576643
Forward Convolution Verifies OK on GPU reference (1.87989e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '512', '-H', '512', '-W', '512', '-k', '512', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 512 -H 512 -W 512 -k 512 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 11.709092 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 512, 512, 512, 3, 3, 512,  1236950581248, 273154048, 268435456, 105640, 46, 11.709092
Forward Convolution Verifies OK on GPU reference (0.000451375 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '512', '-H', '256', '-W', '256', '-k', '512', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 512 -H 256 -W 256 -k 512 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 2.833126 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 512, 256, 256, 3, 3, 512,  309237645312, 71827456, 67108864, 109151, 49, 2.833126
Forward Convolution Verifies OK on GPU reference (0.000476645 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '512', '-H', '256', '-W', '256', '-k', '512', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 512 -H 256 -W 256 -k 512 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 4.929845 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 512, 256, 256, 3, 3, 512,  309237645312, 71827456, 67108864, 62728, 28, 4.929845
Forward Convolution Verifies OK on GPU reference (2.71049e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '4', '-H', '128', '-W', '128', '-k', '512', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 4 -H 128 -W 128 -k 512 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 0.088210 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 4, 128, 128, 3, 3, 512,  603979776, 167936, 16777216, 6847, 192, 0.088210
Forward Convolution Verifies OK on GPU reference (1.82182e-06 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '128', '-H', '512', '-W', '512', '-k', '256', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 128 -H 512 -W 512 -k 256 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 1.423350 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 128, 512, 512, 3, 3, 256,  154618822656, 67698688, 134217728, 108630, 142, 1.423350
Forward Convolution Verifies OK on GPU reference (0.000338107 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '256', '-H', '512', '-W', '512', '-k', '256', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 256 -H 512 -W 512 -k 256 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 6.546124 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 256, 512, 512, 3, 3, 256,  309237645312, 135397376, 134217728, 47240, 41, 6.546124
Forward Convolution Verifies OK on GPU reference (2.13155e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '128', '-H', '1024', '-W', '1024', '-k', '128', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 128 -H 1024 -W 1024 -k 128 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 2.484872 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 128, 1024, 1024, 3, 3, 128,  309237645312, 268730368, 268435456, 124448, 216, 2.484872
Forward Convolution Verifies OK on GPU reference (0.000316882 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '256', '-H', '256', '-W', '256', '-k', '512', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 256 -H 256 -W 256 -k 512 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 2.952186 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 256, 256, 256, 3, 3, 512,  154618822656, 35913728, 67108864, 52374, 35, 2.952186
Forward Convolution Verifies OK on GPU reference (1.90843e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '256', '-H', '1024', '-W', '1024', '-k', '128', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 256 -H 1024 -W 1024 -k 128 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 4.818978 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 256, 1024, 1024, 3, 3, 128,  618475290624, 537460736, 268435456, 128342, 167, 4.818978
Forward Convolution Verifies OK on GPU reference (0.000344062 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '128', '-H', '1024', '-W', '1024', '-k', '3', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 128 -H 1024 -W 1024 -k 3 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 0.633326 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 128, 1024, 1024, 3, 3, 3,  7247757312, 268442368, 6291456, 11444, 434, 0.633326
Forward Convolution Verifies OK on GPU reference (0.000359276 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '512', '-H', '128', '-W', '128', '-k', '8', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 512 -H 128 -W 128 -k 8 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 0.830851 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 512, 128, 128, 3, 3, 8,  1207959552, 16850944, 262144, 1454, 21, 0.830851
Forward Convolution Verifies OK on GPU reference (4.66275e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '4', '-H', '128', '-W', '128', '-k', '4', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 4 -H 128 -W 128 -k 4 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 0.014360 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 4, 128, 128, 1, 1, 4,  524288, 131104, 131072, 37, 18, 0.014360
Forward Convolution Verifies OK on GPU reference (0.000710518 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '256', '-H', '1024', '-W', '1024', '-k', '256', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 256 -H 1024 -W 1024 -k 256 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 25.037432 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 256, 1024, 1024, 3, 3, 256,  1236950581248, 538050560, 536870912, 49404, 43, 25.037432
Forward Convolution Verifies OK on GPU reference (1.92929e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '512', '-H', '512', '-W', '512', '-k', '256', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 512 -H 512 -W 512 -k 256 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 88/GemmFwd1x1_0_1
GPU Kernel Time Forward Conv. Elapsed: 1.256277 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 512, 512, 512, 1, 1, 256,  68719476736, 268697600, 134217728, 54701, 321, 1.256277
Forward Convolution Verifies OK on GPU reference (1.14695e-05 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '256', '-H', '1024', '-W', '1024', '-k', '256', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 256 -H 1024 -W 1024 -k 256 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 9.753479 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 256, 1024, 1024, 3, 3, 256,  1236950581248, 538050560, 536870912, 126821, 110, 9.753479
Forward Convolution Verifies OK on GPU reference (0.000352503 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '256', '-H', '256', '-W', '256', '-k', '512', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 256 -H 256 -W 256 -k 512 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 88/GemmFwd1x1_0_1
GPU Kernel Time Forward Conv. Elapsed: 0.487078 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 256, 256, 256, 1, 1, 512,  17179869184, 33816576, 67108864, 35271, 207, 0.487078
Forward Convolution Verifies OK on GPU reference (7.37393e-06 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '8', '-H', '128', '-W', '128', '-k', '8', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 8 -H 128 -W 128 -k 8 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 88/GemmFwd1x1_0_1
GPU Kernel Time Forward Conv. Elapsed: 0.027715 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 8, 128, 128, 1, 1, 8,  2097152, 262272, 262144, 76, 19, 0.027715
Forward Convolution Verifies OK on GPU reference (4.69071e-06 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '512', '-H', '512', '-W', '512', '-k', '256', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 512 -H 512 -W 512 -k 256 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 88/GemmFwd1x1_0_1
GPU Kernel Time Forward Conv. Elapsed: 1.283613 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 512, 512, 512, 1, 1, 256,  68719476736, 268697600, 134217728, 53536, 314, 1.283613
Forward Convolution Verifies OK on GPU reference (6.26313e-06 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '128', '-H', '512', '-W', '512', '-k', '256', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 128 -H 512 -W 512 -k 256 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 3.447958 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 128, 512, 512, 3, 3, 256,  154618822656, 67698688, 134217728, 44844, 59, 3.447958
Forward Convolution Verifies OK on GPU reference (1.12851e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '512', '-H', '512', '-W', '512', '-k', '256', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 512 -H 512 -W 512 -k 256 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 4.791127 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 512, 512, 512, 3, 3, 256,  618475290624, 270794752, 134217728, 129088, 85, 4.791127
Forward Convolution Verifies OK on GPU reference (0.000462034 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '512', '-H', '257', '-W', '257', '-k', '512', '-y', '3', '-x', '3', '-p', '0', '-q', '0', '-u', '2', '-v', '2', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 512 -H 257 -W 257 -k 512 -y 3 -x 3 -p 0 -q 0 -u 2 -v 2 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 1.754180 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u2, 1, 512, 128, 128, 3, 3, 512,  77309411328, 72352768, 16777216, 44072, 51, 1.754180
Forward Convolution Verifies OK on GPU reference (7.96039e-05 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '512', '-H', '257', '-W', '257', '-k', '512', '-y', '3', '-x', '3', '-p', '0', '-q', '0', '-u', '2', '-v', '2', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 512 -H 257 -W 257 -k 512 -y 3 -x 3 -p 0 -q 0 -u 2 -v 2 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 1.789220 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u2, 1, 512, 128, 128, 3, 3, 512,  77309411328, 72352768, 16777216, 43208, 50, 1.789220
Forward Convolution Verifies OK on GPU reference (3.19971e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '4', '-H', '128', '-W', '128', '-k', '4', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 4 -H 128 -W 128 -k 4 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 88/GemmFwd1x1_0_1
GPU Kernel Time Forward Conv. Elapsed: 0.028587 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 4, 128, 128, 1, 1, 4,  524288, 131104, 131072, 18, 9, 0.028587
Forward Convolution Verifies OK on GPU reference (2.43574e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '256', '-H', '1024', '-W', '1024', '-k', '128', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 256 -H 1024 -W 1024 -k 128 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 88/GemmFwd1x1_0_1
GPU Kernel Time Forward Conv. Elapsed: 1.972061 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 256, 1024, 1024, 1, 1, 128,  68719476736, 536936448, 268435456, 34847, 408, 1.972061
Forward Convolution Verifies OK on GPU reference (4.83614e-06 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '512', '-H', '512', '-W', '512', '-k', '512', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 512 -H 512 -W 512 -k 512 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 18.501274 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 512, 512, 512, 3, 3, 512,  1236950581248, 273154048, 268435456, 66858, 29, 18.501274
Forward Convolution Verifies OK on GPU reference (3.19174e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '256', '-H', '256', '-W', '256', '-k', '512', '-y', '1', '-x', '1', '-p', '0', '-q', '0', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 256 -H 256 -W 256 -k 512 -y 1 -x 1 -p 0 -q 0 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 88/GemmFwd1x1_0_1
GPU Kernel Time Forward Conv. Elapsed: 0.557020 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv1x1u1, 1, 256, 256, 256, 1, 1, 512,  17179869184, 33816576, 67108864, 30842, 181, 0.557020
Forward Convolution Verifies OK on GPU reference (4.26255e-06 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '512', '-H', '512', '-W', '512', '-k', '256', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 512 -H 512 -W 512 -k 256 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 12.509912 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 512, 512, 512, 3, 3, 256,  618475290624, 270794752, 134217728, 49439, 32, 12.509912
Forward Convolution Verifies OK on GPU reference (3.266e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '128', '-H', '1024', '-W', '1024', '-k', '128', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 128 -H 1024 -W 1024 -k 128 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 10.238641 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 128, 1024, 1024, 3, 3, 128,  309237645312, 268730368, 268435456, 30203, 52, 10.238641
Forward Convolution Verifies OK on GPU reference (1.24315e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '4', '-H', '128', '-W', '128', '-k', '512', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 4 -H 128 -W 128 -k 512 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 0.064081 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 4, 128, 128, 3, 3, 512,  603979776, 167936, 16777216, 9425, 264, 0.064081
Forward Convolution Verifies OK on GPU reference (0.000245467 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '256', '-H', '513', '-W', '513', '-k', '256', '-y', '3', '-x', '3', '-p', '0', '-q', '0', '-u', '2', '-v', '2', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 256 -H 513 -W 513 -k 256 -y 3 -x 3 -p 0 -q 0 -u 2 -v 2 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 2.122674 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u2, 1, 256, 256, 256, 3, 3, 256,  77309411328, 135922176, 33554432, 36421, 80, 2.122674
Forward Convolution Verifies OK on GPU reference (2.03356e-05 < 0.0656)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '256', '-H', '513', '-W', '513', '-k', '256', '-y', '3', '-x', '3', '-p', '0', '-q', '0', '-u', '2', '-v', '2', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 256 -H 513 -W 513 -k 256 -y 3 -x 3 -p 0 -q 0 -u 2 -v 2 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 37/ConvBinWinogradRxSf3x2
GPU Kernel Time Forward Conv. Elapsed: 2.013753 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u2, 1, 256, 256, 256, 3, 3, 256,  77309411328, 135922176, 33554432, 38391, 84, 2.013753
Forward Convolution Verifies OK on GPU reference (0.000113774 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convfp16', '-n', '1', '-c', '512', '-H', '128', '-W', '128', '-k', '8', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convfp16 -n 1 -c 512 -H 128 -W 128 -k 8 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 3, Solution: 139/ConvWinoFuryRxS<2-3>
GPU Kernel Time Forward Conv. Elapsed: 0.092143 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 512, 128, 128, 3, 3, 8,  1207959552, 16850944, 262144, 13110, 186, 0.092143
Forward Convolution Verifies OK on GPU reference (0.000486065 < 0.0082)
['/opt/rocm/bin/MIOpenDriver', 'convbfp16', '-n', '1', '-c', '512', '-H', '128', '-W', '128', '-k', '512', '-y', '3', '-x', '3', '-p', '1', '-q', '1', '-u', '1', '-v', '1', '-l', '1', '-j', '1', '-m', 'conv', '-g', '1', '-F', '1', '-t', '1']
MIOpenDriver convbfp16 -n 1 -c 512 -H 128 -W 128 -k 512 -y 3 -x 3 -p 1 -q 1 -u 1 -v 1 -l 1 -j 1 -m conv -g 1 -F 1 -t 1
PRNG seed: 12345678
MIOpen Forward Conv. Algorithm: 0, Solution: 91/GemmFwdRest
GPU Kernel Time Forward Conv. Elapsed: 1.706908 ms (average)
stats: name, n, c, ho, wo, x, y, k, flopCnt, bytesRead, bytesWritten, GFLOPs, GB/s, timeMs
stats: fwd-conv3x3u1, 1, 512, 128, 128, 3, 3, 512,  77309411328, 21495808, 16777216, 45292, 22, 1.706908
Forward Convolution Verifies OK on GPU reference (2.97341e-05 < 0.0656)

---

### 评论 #8 — YuChuXi (2025-12-22T15:44:15Z)

Any progress? Four months have passed.

---

### 评论 #9 — tcgu-amd (2025-12-22T16:27:02Z)

Hi @YuChuXi, sorry for the lack of updates. This is currently being bundled in a major change that will bring support for a wide range of solvers to Radeon cards. While I cannot say when it will be released yet, please know that it is receiving proper attention it deserves and is being worked on actively. Meanwhile, just out of curiosity, can you add 

`torch.backends.cudnn.enabled=False` to the top of your file and see if that changes anything? Thanks! 

---

### 评论 #10 — YuChuXi (2025-12-23T04:33:24Z)

Many changes have occurred during this time. My current environment is Fedora 43, rocm 6.4.4, and PyTorch 2.9.1 + rocm 6.4.
After adding `torch.backends.cudnn.enabled=False` to the top of the file
The FP16 time decreased from 0.7783s to 0.7406s, and the memory usage increased from 2810.58 MB to 6298.57 MB.
The BF16 time decreased from 0.5671s to 0.5003s, and the memory usage increased from 6295.07 MB to 6295.07 MB.

---

### 评论 #11 — tcgu-amd (2025-12-23T16:41:53Z)

@YuChuXi Oh you are on Torch 2.9.1 + ROCm 6.4 still. So the point of disabling cudnn (MIOpen) is to avoid using slower MIOpen naive kernels due to the lack of faster supported algorithms. If you see a performance gain, then that's likely the reason. You can use this as a temporary workaround for BF16. 

---
