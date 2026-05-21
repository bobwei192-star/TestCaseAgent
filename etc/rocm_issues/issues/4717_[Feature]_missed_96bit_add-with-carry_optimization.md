# [Feature]: missed 96bit add-with-carry optimization

> **Issue #4717**
> **状态**: closed
> **创建时间**: 2025-05-07T14:47:34Z
> **更新时间**: 2025-08-11T10:50:33Z
> **关闭时间**: 2025-08-11T10:50:33Z
> **作者**: ahorek
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4717

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

```
typedef uint uint32;
typedef ulong uint64;
typedef struct { uint64 s0; uint32 s1; } uint96;

uint96 uint96_add_64(const uint96 x, const uint64 y)
        uint96 r;
	const uint64 s0 = x.s0 + y;
	r.s0 = s0;
	r.s1 = x.s1 + (s0 < y);
	return r;
}
```

On RDNA 3, it gets optimized to
```
	s_waitcnt vmcnt(0) expcnt(0) lgkmcnt(0)
	v_add_co_u32 v0, vcc_lo, v3, v0
	v_add_co_ci_u32_e32 v1, vcc_lo, v4, v1, vcc_lo
	s_delay_alu instid0(VALU_DEP_1)
	v_cmp_lt_u64_e32 vcc_lo, v[0:1], v[3:4]
	v_add_co_ci_u32_e32 v2, vcc_lo, 0, v2, vcc_lo
	s_setpc_b64 s[30:31]
```

Could the v_cmp_lt_u64_e32 instruction be eliminated? It appears to be the same issue reported in https://github.com/ROCm/ROCm/issues/477, yet it still seems to persist on recent GPUs.

### Operating System

_No response_

### GPU

7900 XTX

### ROCm Component

_No response_

---

## 评论 (4 条)

### 评论 #1 — schung-amd (2025-05-09T14:48:46Z)

Hi @ahorek, do you have a minimal reproducer for this? Not seeing a `v_cmp_lt_u64_e32` instruction being generated on ROCm 6.4, although my quick repro is generating a lot of additional assembly so I might be missing something.

---

### 评论 #2 — ahorek (2025-05-09T18:52:05Z)

@schung-amd sure! Here's a simple reproducer:
https://github.com/ahorek/wideadd

I'm using -save-temps=. to generate an assembly file ._0_gfx1100.s, I also tested it on Windows with the latest Adrenalin 25.4.1 drivers, and the result is the same.

but I have an older version of ROCm 6.2.3, let me check if there's any difference with ROCm 6.4...

---

### 评论 #3 — ahorek (2025-05-11T22:43:52Z)

The latest ROCm 6.4 (3649.0 driver) makes no difference
```
	.text
	.amdgcn_target "amdgcn-amd-amdhsa--gfx1100"
	.amdhsa_code_object_version 5
	.p2align	2                               ; -- Begin function uint96_add_64
	.type	uint96_add_64,@function
uint96_add_64:                          ; @uint96_add_64
; %bb.0:
	s_waitcnt vmcnt(0) expcnt(0) lgkmcnt(0)
	v_add_co_u32 v0, vcc_lo, v3, v0
	v_add_co_ci_u32_e32 v1, vcc_lo, v4, v1, vcc_lo
	s_delay_alu instid0(VALU_DEP_1)
	v_cmp_lt_u64_e32 vcc_lo, v[0:1], v[3:4]
	v_add_co_ci_u32_e32 v2, vcc_lo, 0, v2, vcc_lo
	s_setpc_b64 s[30:31]
.Lfunc_end0:
	.size	uint96_add_64, .Lfunc_end0-uint96_add_64
                                        ; -- End function
	.section	.AMDGPU.csdata,"",@progbits
```

---

### 评论 #4 — ahorek (2025-08-11T10:50:33Z)

I think it’s more of an LLVM issue rather than a ROCm one, so I’ve moved it here https://github.com/llvm/llvm-project/issues/152992

---
