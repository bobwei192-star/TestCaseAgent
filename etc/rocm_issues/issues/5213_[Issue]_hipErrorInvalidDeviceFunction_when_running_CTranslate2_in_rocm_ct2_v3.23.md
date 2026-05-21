# [Issue]: hipErrorInvalidDeviceFunction when running CTranslate2 in rocm_ct2_v3.23.0 Docker image on AMD Radeon PRO W7900

> **Issue #5213**
> **状态**: closed
> **创建时间**: 2025-08-21T05:27:25Z
> **更新时间**: 2025-08-21T05:55:56Z
> **关闭时间**: 2025-08-21T05:55:55Z
> **作者**: IvenTW
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5213

## 描述

### Problem Description

Using the rocm_ct2_v3.23.0 Docker image to execute the CTranslate2 translator results in the following error:
RuntimeError: parallel_for failed: hipErrorInvalidDeviceFunction: invalid device function


### Operating System

22.04.4 LTS (Jammy Jellyfish

### CPU

unknown

### GPU

AMD Radeon PRO W7900

### ROCm Version

rocm6.1

### ROCm Component

_No response_

### Steps to Reproduce

1.  git clone https://github.com/ROCm/CTranslate2.git
2.  git checkout amd_dev
3.  cd docker_rocm
4. docker build -t   rocm_ct2_v3.23.0 -f Dockerfile.rocm . 
5. Launch the Docker container
	1. docker run -it --ipc=host --cap-add=SYS_PTRACE --network=host --device=/dev/kfd --device=/dev/dri --security-opt seccomp=unconfined --group-add video --privileged -w /workspace rocm_ct2_v3.23.0
	2. pip install OpenNMT-py==2.* sentencepiece
6. wget https://s3.amazonaws.com/opennmt-models/transformer-ende-wmt-pyOnmt.tar.gz
   tar xf transformer-ende-wmt-pyOnmt.tar.gz
7. ct2-opennmt-py-converter --model_path averaged-10-epoch.pt --output_dir ende_ctranslate2
8. Vim test.py and save

		import ctranslate2
		import sentencepiece as spm
		
		translator = ctranslate2.Translator("ende_ctranslate2/", device="cuda")
		sp = spm.SentencePieceProcessor("sentencepiece.model")
		
		input_text = "Good Morning!"
		input_tokens = sp.encode(input_text, out_type=str)
		
		results = translator.translate_batch([input_tokens])
		
		output_tokens = results[0].hypotheses[0]
		output_text = sp.decode(output_tokens)
		
		print(output_text)
9. Run python test.py. You will then encounter the issue.
	Traceback (most recent call last):
	  File "/workspace/test.py", line 9, in <module>
	    results = translator.translate_batch([input_tokens])
	RuntimeError: parallel_for failed: hipErrorInvalidDeviceFunction: invalid device function

Additional Notes:  1. The same script runs successfully on NVIDIA GPU.
                               2. The GPU using torch.cuda.get_device_name(0), which correctly returns "AMD Radeon PRO W7900" on the AMD system.


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — IvenTW (2025-08-21T05:55:56Z)

Before creating the Docker image, you need to modify CTranslate2/docker_rocm/Dockerfile.rocm to support the AMD Radeon PRO W7900 GPU, which maps to the gfx1100 architecture.

Update the build section as follows to ensure compatibility:

RUN git clone https://github.com/OpenNMT/CTranslate2.git \
    && cd CTranslate2 \
...
    && cmake -DCMAKE_INSTALL_PREFIX=${CTRANSLATE2_ROOT} \
             -DWITH_CUDA=ON -DWITH_CUDNN=ON -DWITH_MKL=OFF -DWITH_DNNL=ON -DOPENMP_RUNTIME=COMP \
             -DCMAKE_HIP_ARCHITECTURES="gfx1100" -DGPU_TARGETS="gfx1100" -DAMDGPU_TARGETS="gfx1100" \
...


---
