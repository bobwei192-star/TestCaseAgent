# Obtain CU physical ID from HIP kernel?

> **Issue #2059**
> **状态**: closed
> **创建时间**: 2023-04-18T05:25:38Z
> **更新时间**: 2023-04-22T01:46:25Z
> **关闭时间**: 2023-04-22T01:46:25Z
> **作者**: xuantengh
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2059

## 描述

Is there any approach for programmers to obtain the CU's physical ID like the way in CUDA:
```cpp
__device__ uint get_smid(void) {
   uint ret;
   asm("mov.u32 %0, %smid;" : "=r"(ret) );
}
```


---

## 评论 (10 条)

### 评论 #1 — langyuxf (2023-04-20T02:32:19Z)

```
__device__ uint get_smid(void) {
     uint cu_id;
     
     // for gfx9
     asm volatile ("s_getreg_b32 %0, hwreg(HW_REG_HW_ID, 8, 4)" : "=s"(cu_id));
     
     // for gfx10, gfx11
     asm volatile ("s_getreg_b32 %0, hwreg(HW_REG_HW_ID1, 10, 4)" : "=s"(cu_id));
     
     return cu_id;
}
```

---

### 评论 #2 — xuantengh (2023-04-20T05:32:51Z)

It works! Thanks very much!

---

### 评论 #3 — xuantengh (2023-04-21T02:04:58Z)

> ```
> __device__ uint get_smid(void) {
>      uint cu_id;
>      
>      // for gfx9
>      asm volatile ("s_getreg_b32 %0, hwreg(HW_REG_HW_ID, 8, 4)" : "=s"(cu_id));
>      
>      // for gfx10, gfx11
>      asm volatile ("s_getreg_b32 %0, hwreg(HW_REG_HW_ID1, 10, 4)" : "=s"(cu_id));
>      
>      return cu_id;
> }
> ```

BTW, I'm wondering how the bit starter offset and the bit width determined? I only find one docs describing the `hwreg` semantics but no register format for each `hwreg` ID. Thank you.

---

### 评论 #4 — langyuxf (2023-04-21T02:34:17Z)

For gfx11,
https://www.amd.com/system/files/TechDocs/rdna3-shader-instruction-set-architecture-feb-2023_0.pdf
3.4.8. Hardware Internal Registers
or
https://elixir.bootlin.com/linux/latest/source/drivers/gpu/drm/amd/include/asic_reg/gc/gc_11_0_0_sh_mask.h#L41544

For gfx9,
https://elixir.bootlin.com/linux/latest/source/drivers/gpu/drm/amd/include/asic_reg/gc/gc_9_0_sh_mask.h#L28475

You may need SE_ID and SA_ID to calculate the global CU_ID/WGP_ID.
 

---

### 评论 #5 — b-sumner (2023-04-21T03:07:49Z)

It's a bad idea to use inline asm unless absolutely necessary.  It's not necessary here.  See, e.g. https://github.com/ROCm-Developer-Tools/hipamd/blob/develop/include/hip/amd_detail/amd_device_functions.h#L957 

---

### 评论 #6 — xuantengh (2023-04-21T05:05:12Z)

I can obtain the CU ID from the built-in device intrinsic function `__smid()` now, but all the CTA returns 0 in the following code:
```cpp
__global__ void get_cu_id(uint32_t *ids) {
  uint32_t cu_id;
  if (threadIdx.x == 0) {
    // asm volatile("s_getreg_b32 %0, hwreg(HW_REG_HW_ID1, 10, 4)" : "=s"(cu_id));
    cu_id = __smid();
    ids[blockIdx.x] = cu_id;
  }
}

get_cu_id<<<num_cta, warpSize, 0, stream>>>(cu_id_d);
```

All the elements in `cu_id_d` are 0, does it make sense?

Note that if I use the inline asm, the return values indicate that the CTAs are dispatched to each CU in a round-robin fashion:
```
CTA 0, CU ID: 0
CTA 1, CU ID: 1
CTA 2, CU ID: 2
CTA 3, CU ID: 3
CTA 4, CU ID: 0
CTA 5, CU ID: 1
CTA 6, CU ID: 2
CTA 7, CU ID: 3
```

---

### 评论 #7 — b-sumner (2023-04-21T14:32:44Z)

Unfortunately __smid is broken, and should be fixed in an upcoming release.  But note how it doesn't use any inline asm to do its job.  I hope you're aware that the result from SMID or any ID query can change over time.

---

### 评论 #8 — xuantengh (2023-04-21T15:49:21Z)

So the results obtained via the manual inline asm are correct?
```cpp
asm volatile ("s_getreg_b32 %0, hwreg(HW_REG_HW_ID1, 10, 4)" : "=s"(cu_id));
```

---

### 评论 #9 — b-sumner (2023-04-21T16:05:11Z)

I recommend using __builtin_amdgcn_s_getreg to read such registers.  The result is only "correct" at the time the operation executes and can change at any time. 



---

### 评论 #10 — xuantengh (2023-04-22T01:46:25Z)

Thanks for your reply.

---
