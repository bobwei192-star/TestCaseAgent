# [Issue]: HIP runtime crashed if the prompt text is too long

> **Issue #3696**
> **状态**: closed
> **创建时间**: 2024-09-10T09:53:12Z
> **更新时间**: 2024-09-12T04:22:12Z
> **关闭时间**: 2024-09-12T04:22:11Z
> **作者**: foreverlms
> **标签**: Under Investigation, AMD Instinct MI210, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3696

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI210** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

Details of SW stack:
```
hipcc: AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.0 24103 7db7f5e49612030319346f900c08f474b1f9023a)
```

I am developing LLM engine with AMD GPU(MI210) as the backend. All is well if I sent short prompt text to the model, such as:
```
Write me a poem about Machine Learning.
```
The model will return results successfully and `dmesg` log shows no exception.

But if I sent long prompt text, like:
```
prompt_text = "Pick some lines from these poem lines:\nBy chance or nature's changing course untrimm'd;\nOf plagues, of dearths, or seasons' quality;\nO, that you were yourself! but, love, you are\nNow stand you on the top of happy hours,\nAnd with old woes new wail my dear time's waste:\nThen of thy beauty do I question make,\nThe sad account of fore-bemoaned moan,\nLook, what an unthrift in the world doth spend\nWhilst I, whom fortune of such triumph bars,\nIn thy soul's thought, all naked, will bestow it;\nTo dry the rain on my storm-beaten face,\nFor where is she so fair whose unear'd womb\nThat 'gainst thyself thou stick'st not to conspire.\nDo in consent shake hands to torture me;\nA dearer birth than this his love had brought,\nBut flowers distill'd though they with winter meet,\nSave breed, to brave him when he takes thee hence.\nBut since he died and poets better prove,\nAnd look upon myself and curse my fate,\nTheir images I loved I view in thee,\nHow many a holy and obsequious tear\nThyself thy foe, to thy sweet self too cruel.\nThat thou among the wastes of time must go,\nWhen that churl Death my bones with dust shall cover,\nNor can I fortune to brief minutes tell,\nWithout this, folly, age and cold decay:\nThough in our lives a separable spite,\nAnon permit the basest clouds to ride\nFeatured like him, like him with friends possess'd,\nYou should live twice; in it and in my rhyme.\nWho lets so fair a house fall to decay,\nThy merit hath my duty strongly knit,\nThe world will wail thee, like a makeless wife;\nLeaving thee living in posterity?\nHow much more praise deserved thy beauty's use,\nNature's bequest gives nothing but doth lend,\nAnd many maiden gardens yet unset\nGreat princes' favourites their fair leaves spread\nBut day by night, and night by day, oppress'd?\nand then tell me a very very long story:"
```
 crash will happen:
```
Memory access fault by GPU node-3 (Agent handle: 0xa30c040) on address 0x9d000. Reason: Unknown.
[7d485d3128b5:3223459] *** Process received signal ***
[7d485d3128b5:3223459] Signal: Aborted (6)
[7d485d3128b5:3223459] Signal code:  (-6)
[7d485d3128b5:3223459] [ 0] /lib/x86_64-linux-gnu/libpthread.so.0(+0x14420)[0x7fc230707420]
[7d485d3128b5:3223459] [ 1] /lib/x86_64-linux-gnu/libc.so.6(gsignal+0xcb)[0x7fc2303ea00b]
[7d485d3128b5:3223459] [ 2] /lib/x86_64-linux-gnu/libc.so.6(abort+0x12b)[0x7fc2303c9859]
[7d485d3128b5:3223459] [ 3] /opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/lib/libhsa-runtime64.so(+0x259ff)[0x7fbdf20049ff]
[7d485d3128b5:3223459] [ 4] /opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/lib/libhsa-runtime64.so(+0x7192c)[0x7fbdf205092c]
[7d485d3128b5:3223459] [ 5] /opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/lib/libhsa-runtime64.so(+0x2a957)[0x7fbdf2009957]
[7d485d3128b5:3223459] [ 6] /lib/x86_64-linux-gnu/libpthread.so.0(+0x8609)[0x7fc2306fb609]
[7d485d3128b5:3223459] [ 7] /lib/x86_64-linux-gnu/libc.so.6(clone+0x43)[0x7fc2304c6353]
[7d485d3128b5:3223459] *** End of error message ***
```
I checked the HW error log with dmesg:
```
[Tue Sep 10 09:37:08 2024] gmc_v9_0_process_interrupt: 184 callbacks suppressed
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32769, for process pt_main_thread pid 2919831 thread pt_main_thread pid 2919831)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:   in page starting at address 0x0000000000003000 from IH client 0x1b (UTCL2)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00341041
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MORE_FAULTS: 0x1
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          PERMISSION_FAULTS: 0x4
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          RW: 0x1
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32769, for process pt_main_thread pid 2919831 thread pt_main_thread pid 2919831)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:   in page starting at address 0x0000000000007000 from IH client 0x1b (UTCL2)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          RW: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32769, for process pt_main_thread pid 2919831 thread pt_main_thread pid 2919831)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:   in page starting at address 0x0000000000008000 from IH client 0x1b (UTCL2)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          RW: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32769, for process pt_main_thread pid 2919831 thread pt_main_thread pid 2919831)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:   in page starting at address 0x0000000000004000 from IH client 0x1b (UTCL2)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          RW: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32769, for process pt_main_thread pid 2919831 thread pt_main_thread pid 2919831)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:   in page starting at address 0x0000000000006000 from IH client 0x1b (UTCL2)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          RW: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32769, for process pt_main_thread pid 2919831 thread pt_main_thread pid 2919831)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:   in page starting at address 0x0000000000009000 from IH client 0x1b (UTCL2)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          RW: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32769, for process pt_main_thread pid 2919831 thread pt_main_thread pid 2919831)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:   in page starting at address 0x0000000000005000 from IH client 0x1b (UTCL2)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] [drm] Skip scheduling IBs!
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          RW: 0x0
[Tue Sep 10 09:37:08 2024] [drm] Skip scheduling IBs!
[Tue Sep 10 09:37:08 2024] [drm] Skip scheduling IBs!
[Tue Sep 10 09:37:08 2024] [drm] Skip scheduling IBs!
[Tue Sep 10 09:37:08 2024] [drm] Skip scheduling IBs!
[Tue Sep 10 09:37:08 2024] [drm] Skip scheduling IBs!
[Tue Sep 10 09:37:08 2024] [drm] Skip scheduling IBs!
[Tue Sep 10 09:37:08 2024] [drm] Skip scheduling IBs!
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32769, for process pt_main_thread pid 2919831 thread pt_main_thread pid 2919831)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:   in page starting at address 0x000000000000a000 from IH client 0x1b (UTCL2)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: [gfxhub0] no-retry page fault (src_id:0 ring:144 vmid:3 pasid:32769, for process pt_main_thread pid 2919831 thread pt_main_thread pid 2919831)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:   in page starting at address 0x0000000000003000 from IH client 0x1b (UTCL2)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          RW: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: [gfxhub0] no-retry page fault (src_id:0 ring:144 vmid:3 pasid:32769, for process pt_main_thread pid 2919831 thread pt_main_thread pid 2919831)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:   in page starting at address 0x0000000000003000 from IH client 0x1b (UTCL2)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          Faulty UTCL2 client ID: CB (0x0)
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          RW: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MORE_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Sep 10 09:37:08 2024] amdgpu 0000:25:00.0: amdgpu:          RW: 0x0
[Tue Sep 10 09:37:12 2024] amdgpu: HIQ MQD's queue_doorbell_id0 is not 0, Queue preemption time out
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 3, data 0x0, sh 0, priv 1, wave_id 1, simd_id 0, cu_id 3, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 3, data 0x0, sh 0, priv 1, wave_id 1, simd_id 2, cu_id 3, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 3, data 0x0, sh 0, priv 1, wave_id 1, simd_id 1, cu_id 3, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 3, data 0x0, sh 0, priv 1, wave_id 1, simd_id 3, cu_id 3, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 2, data 0x0, sh 0, priv 1, wave_id 1, simd_id 0, cu_id 4, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 2, data 0x0, sh 0, priv 1, wave_id 1, simd_id 1, cu_id 4, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 0, cu_id 3, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 2, data 0x0, sh 0, priv 1, wave_id 1, simd_id 3, cu_id 4, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 1, cu_id 3, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 2, data 0x0, sh 0, priv 1, wave_id 1, simd_id 2, cu_id 4, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 0, data 0x0, sh 0, priv 1, wave_id 1, simd_id 2, cu_id 9, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 2, cu_id 3, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 0, data 0x0, sh 0, priv 1, wave_id 1, simd_id 3, cu_id 9, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 3, cu_id 3, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 0, data 0x0, sh 0, priv 1, wave_id 1, simd_id 0, cu_id 9, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 0, cu_id 2, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 0, data 0x0, sh 0, priv 1, wave_id 1, simd_id 1, cu_id 9, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 1, cu_id 2, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 2, cu_id 2, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 3, cu_id 2, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 0, data 0x0, sh 0, priv 1, wave_id 1, simd_id 2, cu_id 0, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 0, data 0x0, sh 0, priv 1, wave_id 1, simd_id 0, cu_id 0, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 2, data 0x0, sh 0, priv 1, wave_id 1, simd_id 0, cu_id 1, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 2, data 0x0, sh 0, priv 1, wave_id 1, simd_id 1, cu_id 1, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 3, data 0x0, sh 0, priv 1, wave_id 1, simd_id 0, cu_id 11, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 2, data 0x0, sh 0, priv 1, wave_id 1, simd_id 2, cu_id 1, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 3, data 0x0, sh 0, priv 1, wave_id 1, simd_id 3, cu_id 11, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 2, data 0x0, sh 0, priv 1, wave_id 1, simd_id 3, cu_id 1, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 2, cu_id 11, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 3, cu_id 11, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 1, cu_id 11, err_type 2
[Tue Sep 10 09:37:12 2024] amdgpu: sq_intr: error, se 1, data 0x0, sh 0, priv 1, wave_id 1, simd_id 0, cu_id 11, err_type 2
```

It seems driver error happened and the log I added to CPP sources won't print. It seems that runtime crashed without entering the source code. The fault address is weird, which is not usual as application level program could meet. I am so mad and hope you could help me to figure it out why. Sorry that I can't provide the whole details, but you can feel free to ask me for other info to track this.

### Operating System

20.04.6 LTS (Focal Fossa)

### CPU

AMD EPYC 7643 48-Core Processor

### GPU

AMD Instinct MI210

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-09-11T15:09:32Z)

Hi @foreverlms, an internal ticket has been created to further investigate this issue.

---

### 评论 #2 — schung-amd (2024-09-11T15:20:26Z)

Hi @foreverlms, could you provide the model/code which reproduces this issue? Alternatively, if you could provide enough information for us to recreate it, that would help a lot. These error logs unfortunately don't provide much helpful info.

---

### 评论 #3 — foreverlms (2024-09-12T04:22:12Z)

> Hi @foreverlms, could you provide the model/code which reproduces this issue? Alternatively, if you could provide enough information for us to recreate it, that would help a lot. These error logs unfortunately don't provide much helpful info.

Sorry to reply late. I have fixed the kernel

---
