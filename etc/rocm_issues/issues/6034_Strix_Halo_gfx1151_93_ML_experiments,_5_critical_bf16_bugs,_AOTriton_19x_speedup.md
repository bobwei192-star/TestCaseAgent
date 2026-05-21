# Strix Halo gfx1151: 93 ML experiments, 5 critical bf16 bugs, AOTriton 19x speedup undocumented

> **Issue #6034**
> **状态**: open
> **创建时间**: 2026-03-13T00:44:00Z
> **更新时间**: 2026-05-17T00:55:02Z
> **作者**: bkpaine1
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6034

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

## Summary

We ran 93+ autonomous ML training experiments on a Strix Halo system (Radeon 8060S, gfx1151) using TheROCk nightly PyTorch and discovered 5 critical bf16 bugs, an undocumented 19x attention speedup, and several ecosystem gaps that prevent consumer AMD GPUs from being viable ML research platforms.

**Full repo with all data, reproduction scripts, and cross-hardware comparison:** https://github.com/bkpaine1/amdsense

## Hardware
- **APU**: AMD Ryzen AI MAX+ 395
- **GPU**: Radeon 8060S (gfx1151) — integrated
- **Memory**: 128 GB unified
- **PyTorch**: 2.11.0a0+rocm7.11.0a20260106 (TheROCk nightly)
- **Workload**: [Karpathy autoresearch](https://github.com/karpathy/autoresearch) — 5-minute pretraining loop, val_bpb metric

## Results

Starting from a baseline val_bpb of 1.819, we achieved **1.227** — a 32.5% improvement through autonomous hyperparameter optimization. For comparison, the same recipe on an RTX 4090 (CUDA 12.4, PyTorch 2.4.1 stable) achieves 1.844.

The AMD system achieves 25% MFU vs the 4090's 7.7%, suggesting unified memory architecture has real advantages for memory-bound ML workloads.

## Critical Bugs (Reproduction Steps Included)

### 1. bf16 accumulation crash at small batch sizes
- **Repro**: Set `TOTAL_BATCH_SIZE = 2**13` in train.py
- **Result**: NaN within 15 steps, every time
- **Expected**: Training should complete without NaN
- **Notes**: `TOTAL_BATCH_SIZE = 2**14` with `DEVICE_BATCH_SIZE = 16` also NaN/crashes. Works fine at `2**15`.

### 2. bf16 crash at small head dimensions
- **Repro**: Set `HEAD_DIM = 32` in train.py
- **Result**: NaN crash
- **Expected**: Training should complete
- **Notes**: `HEAD_DIM = 64` works (and is CRITICAL for best results — +1.11% regression when reverted to 128)

### 3. Deep network instability
- **Repro**: Set `DEPTH = 12` or higher in train.py
- **Result**: Timeout/crash. `DEPTH = 16` NaN at step 23.
- **Expected**: Deeper networks should train stably
- **Notes**: `DEPTH = 10` succeeded once, crashed on second attempt. Non-deterministic.

### 4. Wide aspect ratio crash
- **Repro**: Set `ASPECT_RATIO = 128` in train.py
- **Result**: Timeout/crash
- **Expected**: Training should complete
- **Notes**: `ASPECT_RATIO = 64` and `32` work fine. 32 actually produces best results (val_bpb 1.227).

### 5. Sharp matrix LR cliff
- **Repro**: Set `MATRIX_LR = 0.20` in train.py
- **Result**: NaN/crash
- **Expected**: Graceful degradation
- **Notes**: `MATRIX_LR = 0.15` works fine. The cliff between 0.15 and 0.20 is unusually sharp, suggesting a precision boundary.

## Ecosystem Issues

### AOTriton experimental flag gives 19x speedup but is undocumented
```bash
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
```
SDPA goes from 44ms to 2.3ms per call. This is the difference between "AMD is unusable for ML" and "AMD is competitive." **This should be the default, not hidden behind an undocumented env var.**

### TheROCk nightlies required for gfx1151
Stable ROCm does not ship gfx1151 kernels. Consumer Strix Halo users must use:
```
pip install torch --index-url https://rocm.nightlies.amd.com/v2/gfx1151/
```
There should be stable wheels for consumer GPUs.

### Default shell config crashes PyTorch
`PYTORCH_HIP_ALLOC_CONF=backend:malloc` is set in some ROCm shell profiles and crashes PyTorch. Users must `unset PYTORCH_HIP_ALLOC_CONF`. A framework default that crashes the framework is a bug.

### No HSA_OVERRIDE needed (good news)
TheROCk nightlies ship native gfx1151 kernels. `HSA_OVERRIDE_GFX_VERSION` is no longer needed. This should be documented prominently for consumer GPU users who are still using the override hack from older guides.

## Environment
```
PyTorch: 2.11.0a0+rocm7.11.0a20260106
HIP: 7.2.53150
ROCm Driver: 6.18.1-061801-generic
TheROCk Index: https://rocm.nightlies.amd.com/v2/gfx1151/
OS: Linux 6.18.1
```

## Full Data
- Repo: https://github.com/bkpaine1/amdsense
- Round 3 report (33 experiments, ablation, failure boundaries): [round3_report.md](https://github.com/bkpaine1/amdsense/blob/master/round3_report.md)
- AMD profiling report: [profile_report.md](https://github.com/bkpaine1/amdsense/blob/master/profile_report.md)
- NVIDIA comparison: [nvidia_4090_comparison.md](https://github.com/bkpaine1/amdsense/blob/master/nvidia_4090_comparison.md)
- Autonomous agent script: [autoresearch_agent3.py](https://github.com/bkpaine1/amdsense/blob/master/autoresearch_agent3.py)
- RunPod benchmark script: [runpod_benchmark.sh](https://github.com/bkpaine1/amdsense/blob/master/runpod_benchmark.sh)

---

## 评论 (31 条)

### 评论 #1 — pedapudi (2026-03-15T18:44:39Z)

Hi @ppanchad-amd, I see that you have been triaging recent issues (thank you). As another Strix Halo user, I'm optimistic that AMD can bridge the software divide with a sense of urgency. 

I'd like to corroborate the gaps being discussed in this report. While this report focuses on PyTorch in part, the bf16 issues may be useful more broadly. gfx1151 is a viable platform for inference, and also, as this issue indicates, it's more viable than traditionally discussed for training. 

Please take an earnest look at the issues described here. The low-hanging fruit here also affords an opportunity for a new blog post indicating the viability of autoresearch on Strix Halo. autoresearch is increasing in its popularity, but it's overfit _against_ AMD hardware, unfortunately. Having a Strix Halo-focused blog post showcasing autoresearch would be a welcomed highlight for the platform.

Thanks for the triaging and prioritization efforts. 

---

### 评论 #2 — bkpaine1 (2026-03-15T20:28:17Z)

@pedapudi — thank you for corroborating. Independent validation from another Strix Halo user matters here.

You're right that autoresearch is overfit against AMD hardware, and that's exactly the gap this issue documents. The silicon is not the problem — we've demonstrated **val_bpb 1.227 on gfx1151 vs 1.844 on an RTX 4090**, a 33% training quality advantage, running on a $1,999 mini PC with 128GB unified memory against a ~$2,400+ discrete GPU build with a 24GB hard wall. The hardware argument is already won. What's losing is the software.

The bf16 accumulation bugs documented here are exactly the kind of low-hanging fruit that separates "viable platform" from "science project." Users shouldn't have to discover through trial and error that `HEAD_DIM` must be 64 (not 32), that batch sizes at or below 2^13 produce NaN, or that network depth above 12 crashes on gfx1151. These are fixable precision bugs, not architectural limitations. Fix them and Strix Halo becomes a legitimate autoresearch platform overnight.

The blog post idea is strong and I'd welcome it. But I want to be direct: NVIDIA just shipped Nemotron 3 — model AND optimized runtime AND deployment stack, one package. They're not waiting for the community to file issues. Meanwhile this report has been open for days with zero official response. The enthusiast and small-lab community that drove Ryzen adoption is standing right here, benchmarks in hand, asking AMD to meet them halfway. That window doesn't stay open forever.

AMD did this before with Ryzen — competitive silicon, developer investment, enthusiast evangelism, enterprise wins. The playbook exists. The hardware is ahead of where Ryzen was at the same point in its arc. The question is whether the software org executes with the same urgency.

Full results, methodology, and reproduction scripts: [github.com/bkpaine1/amdsense](https://github.com/bkpaine1/amdsense). Happy to collaborate on anything that moves the platform forward.

---

### 评论 #3 — Petrox (2026-03-16T09:19:26Z)

+1 from strix halo community member with a cluster setup. 

We all see the great potential is already built into the hardware, but lacking software, drivers, userspace tools leave 30-50% performance on the table (and sometimes it is 1900% undocumented env vars as seen above).

Optimizing strixhalo would be a great opportunity to grab a small piece from the [othercompanyname] market share and tell people that "we can do the same but better", but they shouldn't have to patch their own drivers and kernels and containers by hand every week or so.

Thank you all of your efforts both for ROCm and those investing time into reporting strix halo issues like @bkpaine1 

You are very close to the goal, it just needs a few focused sprints to make this platform a good rational choice for stable homelab-smallbiz-cluster for inference and training - without crashes and undocumented env vars. 

Best wishes and have a nice day!

---

### 评论 #4 — bkpaine1 (2026-03-16T14:15:06Z)

@Petrox — welcome to the fight. A cluster setup on Strix Halo is exactly the kind of validation this platform needs.

Your numbers match ours: 30-50% performance left on the table from software gaps, and yeah, that 1900% (19x) AOTriton speedup hidden behind an undocumented env var is the crown jewel of "why is this not the default." We didn't discover it through documentation. We discovered it through an autonomous AI agent running 200+ experiments at 2am.

Since our last update, we've run **two more full rounds** of autonomous research (Rounds 4 and 5, 100+ additional experiments):

- **val_bpb improved from 1.227 → 1.2153** — now 34% better than RTX 4090 (1.844) on the same recipe
- **2 models trained at 29,722 MB VRAM** — impossible on a 4090's 24 GB hard limit. The NVIDIA equivalent is an A100 ($15,000).
- **New bf16 bug found**: Adam beta2 < 0.97 causes NaN crashes. Optimizer precision issue, not user error.
- **Extended training degrades**: 10-minute runs hit NaN on run 3/3 at ~1008 steps. bf16 accumulation erodes over time.
- **Interaction effects mapped**: drop-one ablation across all hyperparams — EMBEDDING_LR and SCALAR_LR are load-bearing (NaN when dropped).

Full data, all experiment results (JSON), updated best recipe, and the autonomous agent script are published: [github.com/bkpaine1/amdsense](https://github.com/bkpaine1/amdsense). 200+ experiments, 5 rounds, zero human intervention during runs. Everything reproducible.

Three independent Strix Halo users with benchmarks on record now. The community is doing AMD's QA for free. We can do this all day — but we shouldn't have to.

---

### 评论 #5 — pedapudi (2026-03-16T23:50:08Z)

Thanks, @bkpaine1 

I think we are unified with our friends at AMD in trying to improve the state of things. As with all things open source, maintainers managing contributions and steering the efforts towards shared goals is important. My hope is that we're providing clear signal on the opportunity for Strix Halo specifically. I think actionable findings are a gift for any maintainer :) And, because ROCm serves a commercial need for AMD, I'm also hoping there is sufficient incentive to prioritize these changes sooner than later to add to very timely go-to-market momentum. I'm glad to say that AMD's enthusiastic community would support AMD in this.

@tcgu-amd Tim, please let us know how we can help you. Thank you.

---

### 评论 #6 — bkpaine1 (2026-03-17T13:20:00Z)

**Round 6: 57 more experiments, val_bpb 1.2080, and a clearer picture of the bf16 boundary**

@pedapudi @Petrox — Round 6 ran overnight. 57 architectural experiments across 7 phases (window patterns, GQA, MLP ratio, residual scaling, depth/LR co-optimization, softcap, combined). Autonomous agent, zero intervention.

**New best: val_bpb 1.2080** (R5 was 1.2153). Six rounds, 250+ experiments total. The gap over RTX 4090 (1.844) keeps widening — now 34.5%.

Key architectural wins:
- Alternating sliding/linear window (`SLSLSL`) slightly edges pure patterns
- GQA with `kv_head_divisor=6` — quality holds at 15.9M params, 114K tok/sec
- Depth 6 + wide (aspect_ratio 48) beats deeper networks — wider wins on this silicon
- Residual scaling sweet spot: `x0_lambda=0.2, resid_lambda=0.8`

**The bf16 picture is getting clearer.** ~40% of experiments this round crashed to NaN — not exotic configs, but mainstream ones: `kv_head_divisor=1`, consecutive sliding windows, `mlp_ratio=8`, `softcap≥30`. Most notably: combining Phase 1-6 winners that each work individually → NaN when stacked. The precision boundary isn't per-config, it's cumulative. Higher compute density per operation hits it faster.

This is good news for AMD, honestly. It means the silicon is outperforming the software path. Fix the accumulation precision and these NaN configs become valid experiments — the real performance ceiling is higher than what we're measuring.

Full Round 6 data (JSON per phase, agent logs, updated recipe) pushed to [github.com/bkpaine1/amdsense](https://github.com/bkpaine1/amdsense).

I'll be honest — I'm one person running these experiments on a single GMKTEC EVO X2. Every overnight research round means my GPU is unavailable for the actual work I bought it for. 250+ experiments and six rounds of autonomous research is about as far as I can take this without hardware support. The data is here, the methodology is reproducible, and the community is growing. But I can't keep dedicating my only AI workstation to improving AMD's software stack full-time. I need help.

Happy to coordinate here or in a dedicated issue. The door's open.

Keep pushing, gentlemen. The hardware deserves the software to match.

---

### 评论 #7 — Petrox (2026-03-17T18:51:05Z)

@bkpaine1 While I'm limited in spare time, but I have two strixhalos mostly not doing significant work (yet), so if that helps, I could clone a repo and run some workloads (fedora 43 bleeding edge 7.0 kernel), it would be great if I could stop and start it at any time though and maybe commit the results back for datacollection. Maybe our sync should be handled in your repos issues, and you could coordinate the datasets and issues, I can provide some compute to that. 

Note: AMD could probably assign 20 strixhalos to the same task and be done in a day should they care about software support.





---

### 评论 #8 — bkpaine1 (2026-03-17T19:32:39Z)

@Petrox — generous offer and exactly what we need. Two more Halos running the same workloads gives us reproducibility across machines, not just across runs.

Repo is at https://github.com/bkpaine1/amdsense — clone it, agent scripts and configs are all there. I'll open an issue for coordinating distributed runs so we can track results cleanly. Stop/start whenever you want — experiments are designed to be independent. Commit results back and we'll merge.

You're right that AMD could throw 20 machines at this and be done in a day. We're three users doing it on our own hardware in our spare time. 250+ experiments, reproducible bf16 bugs, 34% ahead of a 4090 on training quality. The data speaks for itself.

@pedapudi — appreciate the diplomacy. @tcgu-amd Tim, we're here to help. The findings are actionable and the repo is public. Tell us what you need.

— Brent

---

### 评论 #9 — tcgu-amd (2026-03-17T19:47:37Z)

Hi @pedapudi , @bkpaine1 , @Petrox, thank you guys for reaching out and being passionate about ROCm. Proving stable, proper bf16 support has definitely been on our bucket list. We are kind of thin on bandwidth right now, but please let me take a look at what is needed here. Thanks! 

---

### 评论 #10 — tcgu-amd (2026-03-17T20:02:41Z)

But yeah @pedapudi, I guess a few comments out of the way first. Regarding AOTRITON, I am glad you found it helpful in boosting performance, but please do note that it is still an experimental feature. Ideally, it will be recommended as default once we get it stable.  As for HSA_OVERRIDE_GFX_VERSION, please note that this was never meant to be a consumer-oriented feature, and is almost never recommended by AMD. If using this is needed, that means the hardware is not supported by ROCm, and it would always be a "hack" that can lead to unstable results. But yeah, I know in a lot of cases there's no choice but to use it, but please just keep this in mind. Thanks again!!

---

### 评论 #11 — Petrox (2026-03-17T21:06:13Z)

I've forked @bkpaine1 's repo and will run the benchmarks when anthropic fixes their issues (API Error: 529 {"type":"error","error":{"type":"overloaded_error","message":"Overloaded. https://docs.claude.com/en/api/errors"},"request_id":""} ), and will let it cook for a day... please enable issue tracking there. 





---

### 评论 #12 — bkpaine1 (2026-03-17T21:20:26Z)

@Petrox suffering the same...I am good Obelisk is better but together we cooked this up 

---

### 评论 #13 — pedapudi (2026-03-17T23:46:00Z)

> But yeah [@pedapudi](https://github.com/pedapudi), I guess a few comments out of the way first. Regarding AOTRITON, I am glad you found it helpful in boosting performance, but please do note that it is still an experimental feature. Ideally, it will be recommended as default once we get it stable. As for HSA_OVERRIDE_GFX_VERSION, please note that this was never meant to be a consumer-oriented feature, and is almost never recommended by AMD. If using this is needed, that means the hardware is not supported by ROCm, and it would always be a "hack" that can lead to unstable results. But yeah, I know in a lot of cases there's no choice but to use it, but please just keep this in mind. Thanks again!!

Thanks @tcgu-amd. What you're saying is very reasonable, and it matches my understanding as well. I think a part of this discussion is how the main branch for ROCm can extend support for Strix Halo. Thanks for taking a look. It's unsurprising to hear there isn't bandwidth to spare; that is the common case, after all. The argument here is that there is a meaningful opportunity and the timing appears to be right to ensure ROCm and Strix Halo really have a "better together" story.

---

### 评论 #14 — web2bruno (2026-03-18T21:25:55Z)

### Performance Regression on gfx1151 (8060S) - 70% PP Drop in recent ROCm builds

I can confirm the instability and performance regressions on **gfx1151 (Radeon 8060S / Strix Halo)** mentioned in this issue. I have been benchmarking **Qwen 3.5 35B (Q6_K)** across different ROCm builds, and the regression in prompt processing (PP) as context scales is severe.

In older builds (e.g., **Lemonade b1215**), scaling was relatively linear. However, in recent builds (**ROCm 7.x / b8388**), there is a massive "efficiency cliff" once context exceeds 8k tokens.

#### Benchmark Comparison (Qwen 3.5 35B Q6_K)

| Context (PP) | Lemonade b1215 (ROCm) | New ROCm (b8388) | **Performance Change** |
| :--- | :--- | :--- | :--- |
| **pp512** | 986 t/s | 904.98 t/s | -8% |
| **pp8192** | 885 t/s | 516.07 t/s | **-41%** |
| **pp32768** | 705 t/s | **209.54 t/s** | **-70%** |

#### Observations:
* **Memory Management:** Newer builds report `VMM: no` and show a massive spike in CPU `user/sys` time during long-context prefill, suggesting the driver is failing to manage the KV cache on the 8060S natively.
* **Vulkan Comparison:** On the same hardware/build (b8388), **Vulkan** maintains **633.08 t/s** at 32k context, outperforming the current ROCm path by **3x**.
* **Generation:** Interestingly, token generation (`tg128`) improved slightly (from 39 t/s to 43.80 t/s), but the prefill regression makes long-context workflows unusable.

It appears the specialized attention kernels or VMM strategies that were functional in earlier 2026 builds are missing or regressing in the current stack.

---
*This report was drafted with AI assistance to ensure technical clarity and data organization. All benchmarks were performed and verified manually on local hardware.*

---

### 评论 #15 — bkpaine1 (2026-03-19T05:11:56Z)

@tcgu-amd — appreciate you looking at this. Genuinely.

But I want to put something in perspective. AMD's market cap crossed **$320 billion** this week. The Strix Halo is being marketed as the flagship consumer AI chip — "run AI locally" is the pitch. Three independent users on three different machines just provided 250+ experiments, reproducible benchmarks, and now @web2bruno showing a **70% prompt processing regression** in recent builds — with Vulkan outperforming ROCm 3x on the same silicon.

This isn't a feature request. This is the software stack for your marquee consumer AI product regressing between releases with no one assigned to catch it.

We're not asking for a team. We're pointing out that the ecosystem story — the thing that turns a $320B company into a $1T company — lives or dies on whether developers can actually use the hardware they bought. NVIDIA didn't win on silicon alone. They won on CUDA. ROCm is AMD's answer to that, and right now it's going backwards on your own flagship chip.

We've done the QA. We've filed the bugs. We've published the data. We're here because we believe in the hardware. The question is whether AMD believes in it enough to staff the software.

---

### 评论 #16 — Petrox (2026-03-19T11:55:44Z)

I want to add my support for @bkpaine1, and also thank @tcgu-amd, @pedapudi, and everyone working on this.

The frustration in this thread is understandable and I can confirm hundreds of users feel it every week, but I want to be clear that I do not see this as a problem with individual contributors. The real issue is priority and resourcing. Strix Halo support currently feels below the level that AMD’s hardware is capable of and what marketing arches story imply. 

What makes this thread important is that it is not vague complaining. It contains serious repro data, concrete failure modes, and evidence that the platform is close enough to useful that fixing the remaining gaps could materially change perception.

That is why this should be a high-priority issue. The users pushing Strix Halo for ML at home are often the same people who influence workstation, lab, and even datacenter decisions later. If AMD gives them a reliable experience, they become advocates. If the platform feels unstable and under-supported, they will remember that for years.

So “thin on bandwidth” is exactly the signal that should be escalated internally. Hardware ambition without dependable software support leaves a lot of value unrealized.

Please treat this issue as more than a single bug report. It is evidence that Strix Halo support deserves more visibility, more resourcing, better documentation, and faster follow-through. The good news is that the community is already here with repros, testing, and willingness to help.

I appreciate all work already done, and I hope this issue helps raise the priority of Strix Halo / gfx1151 support across the board.

Let me quote https://www.amd.com/content/dam/amd/en/documents/epyc-business-docs/white-papers/rearchitecting-data-centers-ai-workloads-tech-target-report.pdf: 

"Working with the right AI infrastructure partner grants
you access to the expertise, hardware and software
ecosystem needed to accelerate AI adoption while
ensuring cost efficiency, performance and scalability.
Being at the forefront of AI data center innovation,
AMD delivers an end-to-end portfolio of AI solutions
— from CPUs and GPUs, such as AMD EPYCTM and
AMD InstinctTM, to advanced networking solutions
and even AI PCs — you need to build the AI-ready
data center of the future."

We are all eagerly waiting for the end-to-end portfolio to arrive to the strix halo.

---

### 评论 #17 — zhelgadis (2026-03-19T16:17:41Z)

As a fellow Strix Halo owner, I'd like to chime in alongside other users in the hope that AMD gives this project the attention it deserves.
The silicon is great (I'm really having a blast with it, this whole thing is giving me early Internet days vibes) and I'm seeing that local inferencing is a viable option for a software development team, not just for hobbyists.

But as someone who has to report to management, if I had to give my feedback today, I would have to say: "It's not ready yet, we have to go with [maincompetitor]." This because I cannot expect my teammates to jump through all these hoops while also delivering production code under tight deadlines.

I’ll have to provide my feedback a few months from now, and I really hope it will be: "Go ahead and buy a bunch of these machines." :) 

---

### 评论 #18 — lostdisc (2026-03-19T21:16:09Z)

I'm on Strix Point (gfx1150), but hope that Strix Halo fixes/improvements also trickle down where applicable.

---

### 评论 #19 — Petrox (2026-03-19T23:44:57Z)

Disclaimer: I don't know anything deep about ROCm or even training models.  

I just prompted claude to go beyond finding bugs and for any issue dig deep and find the root cause in rocm source and github issues.

 @tcgu-amd would you please take a look, this contains detailed investigation, reproducing snippets and actionable fixes and workarounds at the end: 

 https://github.com/Petrox/amdsense/blob/7d203ce277226ab6739d6b12f787793ecb17ea25/reports/findings_torch_compile_nan_gfx1151.md

 (Hope this is helpful, but feel free to ignore it if it's all invalid or solved somehow or somewhere else.)


---

### 评论 #20 — bkpaine1 (2026-03-20T01:18:01Z)

> Disclaimer: I don't know anything deep about ROCm or even training models.
> 
> I just prompted claude to go beyond finding bugs and for any issue dig deep and find the root cause in rocm source and github issues.
> 
> [@tcgu-amd](https://github.com/tcgu-amd) would you please take a look, this contains detailed investigation, reproducing snippets and actionable fixes and workarounds at the end:
> 
> https://github.com/Petrox/amdsense/blob/7d203ce277226ab6739d6b12f787793ecb17ea25/reports/findings_torch_compile_nan_gfx1151.md
> 
> (Hope this is helpful, but feel free to ignore it if it's all invalid or solved somehow or somewhere else.)
  

@Petrox This is great work — thank you for running our fork on your cluster and for putting this investigation together. The detailed root cause
  analysis with repro snippets is exactly what this thread needs more of.

  The bf16 accumulation issue you're documenting is the same family of bugs we've been hitting since day one. We mapped the failure boundaries in our
  amdsense experiments — small batch sizes, certain HEAD_DIM values, beta2 < 0.97 all trigger NaN cascades that trace back to bf16 precision loss in
  the HIP kernels.

  What's frustrating is that this hardware is genuinely exceptional. Our $2K GMKTEC mini PC beat a 4090 by 33% on training quality once we got past the
   software issues. It took 8 months and moving to Ubuntu 25.10 to get stable. The silicon deserves a software stack that matches it.

  @tcgu-amd — Petrox's report plus our experimental data give you two independent datasets on the same bf16 issues across different Halo
  configurations. Happy to help however we can. We want this platform to win.


---

### 评论 #21 — Petrox (2026-03-21T23:54:08Z)

Let me know if I can help further. I could run these test/diag loops any time, just let me know if/when it is useful.

---

### 评论 #22 — bkpaine1 (2026-03-23T16:14:48Z)

## Update: Karpathy's autoresearch running on Strix Halo (gfx1151)

Ported [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) to the Radeon 8060S. This is the autonomous ML research framework that lets an AI agent run experiments overnight — modify architecture, train for a fixed budget, evaluate, iterate.

**Key result: `torch.compile` fully working on gfx1151 with TheROCk nightly PyTorch 2.11.**

The existing AMD fork ([andyluo7/autoresearch](https://github.com/andyluo7/autoresearch)) targets MI308X and had to disable `torch.compile` entirely due to `lerp_()` dtype issues in PyTorch 2.6. Our PyTorch 2.11 nightly resolves this — we added explicit dtype casts and compile runs clean.

### Results comparison

| Metric | Strix Halo 8060S | MI308X (datacenter) | H100 (upstream) |
|--------|-----------------|---------------------|-----------------|
| MFU | **24.4%** | 3.18% | ~40% |
| torch.compile | **YES** | NO (eager only) | YES |
| tok/sec | ~51K | ~161K | ~1.6M |
| Peak VRAM | 6.2 GB / 64 GB | - | ~44 GB |

**24.4% MFU vs 3.18%** — a consumer APU running 8x the efficiency of the datacenter fork. The difference is entirely `torch.compile`.

### Changes from upstream
- FA3 → PyTorch SDPA (AOTriton dispatches automatically with `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1`)
- `lerp_()` explicit dtype casts for ROCm compatibility in compiled graphs
- Auto GPU FLOPS detection (added 8060S at 49.6 TF bf16)

Fork: https://github.com/bkpaine1/autoresearch-halo

This builds on top of our amdsense work (250+ experiments characterizing gfx1151 behavior). The TheROCk nightlies are making real ML workloads viable on consumer Strix Halo hardware. `torch.compile` working is a big deal — it's the difference between "technically runs" and "actually competitive."

cc @pedapudi @kraln — more gfx1151 data for the pile.

---

### 评论 #23 — bkpaine1 (2026-03-27T00:55:48Z)

## Update: Full NPU Stack Running on Strix Halo (XDNA2) — Built From Source

Quick update for the gfx1151 community:

We now have the **AMD XDNA2 NPU fully operational** on Strix Halo (Ryzen AI MAX+ 395) running Ubuntu 25.10, kernel 6.18.1. FastFlowLM 0.9.37 + Lemonade 10.0.1 serving Qwen 3.5 4B via OpenAI-compatible API on the NPU — zero GPU utilization.

### What it took

The stock Ubuntu 25.10 firmware (`npu.sbin 1.0.0.166`) and in-tree kernel driver (`amdxdna 0.1`) are **incompatible** with FastFlowLM, which requires firmware ≥ 1.1.0.0 and a newer driver protocol. Upgrading just the firmware from upstream `linux-firmware.git` (`npu.sbin 1.1.2.65`) fails because the old kernel driver doesn't speak protocol major 7 — classic version coupling.

**Solution:** Build [amd/xdna-driver](https://github.com/amd/xdna-driver) from source. The DKMS package ships a matched driver (2.23.0) + development firmware (`npu.dev.sbin` 255.0.11.71) that work together. Builds clean on kernel 6.18.1. Total build time: ~16 seconds on Strix Halo. The irony is not lost on us.

### The gap

None of this should require building from source. The firmware and driver ship mismatched in every current Ubuntu release. The Lemonade PPA ships XRT userspace but no DKMS driver. `flm validate` fails out of the box on every non-Arch distribution we've tested. For a chip that AMD is actively marketing for AI workloads, the Linux developer experience remains "figure it out yourself."

We're happy to keep contributing data points (this is our 5th update on this thread — amdsense, autoresearch, torch.compile benchmarks, and now NPU). But it would be encouraging to see Strix Halo appear on the official ROCm support matrix at some point, rather than relying on the community to build and document the entire stack.

### Environment
- **Hardware:** Ryzen AI MAX+ 395, Radeon 8060S (gfx1151), XDNA2 NPU (8 columns)
- **OS:** Ubuntu 25.10, kernel 6.18.1
- **Driver:** xdna-driver 2.23.0 (DKMS, built from source)
- **Firmware:** npu.dev.sbin 255.0.11.71
- **Stack:** FastFlowLM 0.9.37 + Lemonade 10.0.1
- **NPU inference:** Qwen 3.5 4B — 20.8 tok/s prefill, 10.4 tok/s decode

Three compute lanes now operational on a single consumer APU: GPU (ROCm/PyTorch), NPU (FastFlowLM), CPU. All community-built. You're welcome.

cc @pedapudi @kraln

---

### 评论 #24 — tcgu-amd (2026-03-27T15:18:04Z)

Hi @bkpaine1, these are some impressive works and improvements! Thanks for all the hard work! For the NPU related issue, would you mind opening a ticket on the xdna github? Just to let those folks know about this issue since it is a bit out of scope for ROCm. Thanks! 

---

### 评论 #25 — bkpaine1 (2026-03-27T18:44:21Z)

@tcgu-amd Thanks! Filed: https://github.com/amd/xdna-driver/issues/1219

Covers the firmware/driver version coupling issue in detail with repro steps and the build-from-source workaround.

---

### 评论 #26 — woct0rdho (2026-03-28T00:46:20Z)

Hi, I just discovered this issue. I've also been trying something like autoresearch on Strix Halo, but targeting the most basic matrix multiplication operator rather than the attention operator.

I'd say rocm7.11.0a20260106 is not the latest nightly ROCm. I've had experience that a newer ROCm speeds up matrix multiplication both in hipBLAS/hipBLASLt and in custom HIP kernels. Some PyTorch unit tests fail with the newer ROCm and it may be worth investigating.

---

### 评论 #27 — Petrox (2026-04-09T13:50:52Z)

Any progress on this?

---

### 评论 #28 — GrahamJenkins (2026-04-14T05:40:58Z)

## MusicGen Inference: Deterministic GPU Crash at Exactly 2000 Audio Tokens on gfx1151

Adding another reproducible failure case from a different workload — **autoregressive audio generation** via [Meta's MusicGen](https://github.com/facebookresearch/audiocraft) (HuggingFace transformers).

### Hardware / Software
- **APU**: AMD Ryzen AI MAX+ 395
- **GPU**: Radeon 8060S (gfx1151)
- **Memory**: 128 GB unified
- **PyTorch**: 2.9.1 (built from source for gfx1151, ROCm backend)
- **ROCm**: 6.4.2 (Fedora 43 system packages)
- **Mesa**: 25.3.6
- **Kernel**: 6.19.11
- **Model**: MusicGen (transformers library, NOT audiocraft — audiocraft incompatible with Python 3.14)
- **Precision**: fp32 (torch_dtype=torch.float32)

### The Bug

MusicGen crashes with SIGABRT at **exactly ~2000 audio tokens (40.1 seconds of generated audio)**, every time, regardless of model size or generation speed. The crash is in the HSA async event loop inside libamdhip64.so.

### Reproduction

MusicGen generates audio autoregressively at 50 tokens/second across 4 codebooks. We instrumented generation with a custom `StoppingCriteria` callback that logs token count at each step.

**Test 1 — MusicGen-medium (1.5B params):**
- Request: 300s of audio (15,000 tokens)
- Crash at: 2003 tokens, 40.1s audio, **209.9s wall time**
- Speed: 9.5 tok/s

**Test 2 — MusicGen-medium (repeat):**
- Request: 300s of audio
- Crash at: 2003 tokens, 40.1s audio, **209.6s wall time**
- Speed: 9.6 tok/s

**Test 3 — MusicGen-small (300M params):**
- Request: 60s of audio (3,000 tokens)
- Crash at: 2003 tokens, 40.1s audio, **60.9s wall time**
- Speed: 32.9 tok/s

The crash point is **token-count based, not wall-time based**. Small model processes tokens 3.4x faster and crashes at the same token count in 1/3 the wall time. This rules out thermal throttling, power management, or connection timeouts.

### Crash Stack Trace (from coredump)

```
#0  __pthread_kill_implementation (libc.so.6)
#1  raise (libc.so.6)
#2  abort (libc.so.6)
#3  amd::roc::callbackQueue(hsa_status_t, hsa_queue_s*, void*) (libamdhip64.so.6)
#4  rocr::AMD::AqlQueue::ExceptionHandler(long, void*) (libhsa-runtime64.so.1)
#5  rocr::core::Runtime::AsyncEventsLoop(void*) (libhsa-runtime64.so.1)
```

The HSA runtime's async event loop receives a queue error from the GPU and calls abort(). The GPU itself is reporting a fault after exactly ~2000 autoregressive forward passes.

### What We Tried (none helped)

| Mitigation | Result |
|-----------|--------|
| `HSA_ENABLE_SDMA=0` | Same crash at 2000 tokens |
| Mesa 25.3.5 → 25.3.6 | Same crash at 2000 tokens |
| `torch.cuda.synchronize()` every 500 tokens | Same crash at 2000 tokens |
| 10-second generation (500 tokens) | Works fine |
| 30-second generation (~1500 tokens) | Works fine |

### Connection to Existing Findings

This appears related to Bug #3 in the original report (deep network instability / crash at depth 16). Autoregressive generation is functionally equivalent to an extremely deep network unrolled over time — each token is a full forward pass through the transformer, and 2000 tokens = 2000 sequential forward passes with accumulating KV cache state.

The finding that "10-minute training runs hit NaN at ~1008 steps" and "bf16 accumulation erodes over time" matches our pattern, though we're running in fp32. The crash may be in the HIP kernel accumulation path regardless of the user-specified dtype.

### Impact

We purchased Strix Halo hardware specifically for local AI workloads — the use case AMD is actively marketing. This bug makes audio generation beyond 40 seconds impossible on the GPU we bought for exactly this purpose. The hardware is capable, the silicon is excellent, but we're blocked by a driver-level fault that we can't work around.

Seeing "thin on bandwidth" as the response to a growing list of reproducible, well-documented bugs on a flagship product is discouraging. We chose AMD over NVIDIA for this build. That decision currently means accepting hard limits on our workloads that don't exist on competing hardware, with no timeline for resolution. AMD shipped this silicon with a marketing promise of local AI capability — the driver stack needs to deliver on that promise.

@tcgu-amd — this is a clean, deterministic repro with minimal variables (single model, fp32, same crash point across model sizes). Happy to provide coredumps, run additional diagnostics, or test patches if anything becomes available.

cc @bkpaine1 @Petrox @pedapudi

---

### 评论 #29 — mikler (2026-04-20T03:14:11Z)

Cannot fine-tune the Whisper model on ROCm because of this. NVIDIA's CUDA is so much more reliable.

---

### 评论 #30 — jammm (2026-05-01T17:46:35Z)

> Disclaimer: I don't know anything deep about ROCm or even training models.
> 
> I just prompted claude to go beyond finding bugs and for any issue dig deep and find the root cause in rocm source and github issues.
> 
> [@tcgu-amd](https://github.com/tcgu-amd) would you please take a look, this contains detailed investigation, reproducing snippets and actionable fixes and workarounds at the end:
> 
> https://github.com/Petrox/amdsense/blob/7d203ce277226ab6739d6b12f787793ecb17ea25/reports/findings_torch_compile_nan_gfx1151.md
> 
> (Hope this is helpful, but feel free to ignore it if it's all invalid or solved somehow or somewhere else.)

Seems like this has already been fixed in https://github.com/triton-lang/triton/pull/8697 and you should be able to find this in more recent triton nightly builds from April 11th onwards.

---

### 评论 #31 — camerono (2026-05-17T00:55:02Z)

empirical data point from gfx1151 (Strix Halo APU - Ryzen AI Max+ 395 / Radeon 8060S iGPU, GMKtec EVO-X2):

was hitting deterministic `hipErrorLaunchFailure` core-dumps during Z-Image LoRA training via ai-toolkit. non-deterministic crash step - one run at step 253/1500, next run at step 0/1500. stack always lands in `c10::cuda::SetDevice → libtorch_hip.so → HIPFunctions.cpp:334`, SIGABRT.

setting these in the conda activate hook fixed it:

```
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
export MIOPEN_DEBUG_CONV_DIRECT=0
```

(also cleared `~/.config/miopen` and `~/.cache/miopen` before the next launch - had stale kernel cache from a prior torch upgrade)

after that, Z-Image r16 LoRA trained 1500 steps end-to-end, no crash. bf16, batch 1, 1024 res, ~10s/step. torch 2.12.0a0+rocm7.13.0a20260411 from TheRock nightly, ubuntu 6.18.x kernel.

re: AOTRITON being experimental - completely understood, and noted in the thread. but on this hardware specifically it's not "just" a 19x perf win - it's the difference between "training completes" and "core-dumps during model init / first batch". the MIOpen grouped-conv path seems to be the actual crash vector, and AOTRITON sidesteps it.

worth a note in gfx1151-specific docs maybe? for anyone landing here from the same crash via a search engine.


---
