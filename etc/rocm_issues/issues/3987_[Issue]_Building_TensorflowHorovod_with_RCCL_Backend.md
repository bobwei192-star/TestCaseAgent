# [Issue]: Building Tensorflow/Horovod with RCCL Backend 

> **Issue #3987**
> **状态**: closed
> **创建时间**: 2024-11-04T04:10:11Z
> **更新时间**: 2025-05-29T06:37:07Z
> **关闭时间**: 2024-11-19T15:01:35Z
> **作者**: vitduck
> **标签**: Under Investigation, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3987

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

The current ROCm documentation outlines methods to build/install TensorFlow2. 
However, a crucial component for multi-GPU scaling is neglected, i.e. `horovod`.  

Here, building `horovod` with RCCL backend fails during configure stage.    

### Operating System

RHEL 8.9

### CPU

N/A

### GPU

N/A

### ROCm Version

ROCm 6.1.0

### ROCm Component

rccl

### Steps to Reproduce

```
$ conda create -n tf+rocm_6.1+mpich python=3.10
$ conda activate tf+rocm_6.1+mpich  

$ pip install  tensorflow-rocm==2.15.0 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1/ 

$ module purge 
$ module load cmake/3.30.1
$ module load PrgEnv-cray/8.5.0 craype-x86-genoa  craype-accel-amd-gfx942 rocm/6.1.1

$ export HOROVOD_WITH_TENSORFLOW=1 
$ export HOROVOD_GPU=ROCM 
$ export HOROVOD_GPU_OPERATIONS=NCCL 
$ export HOROVOD_ROCM_PATH=$ROCM_PATH 

$ pip install --no-cache-dir --force-reinstall git+https://github.com/horovod/horovod.git@v0.28.1

   -- Build Horovod for ROCm
      CMake Error at horovod/common/ops/rocm/CMakeLists.txt:21 (hip_add_library):
        Unknown CMake command "hip_add_library".
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

- Despite using a recent version of cmake, there error indicates that `hip_add_library` command is not available. 
- I have tried containers provided at https://hub.docker.com/r/rocm/tensorflow, unfortunately they are built without `horovod`. 

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — harkgill-amd (2024-11-04T20:44:59Z)

Hi @vitduck, an internal ticket has been created to further investigate the build errors with horovold+ROCm.

---

### 评论 #2 — huanrwan-amd (2024-11-06T20:52:25Z)

Hi @vitduck, can you provide a full log while running:
`pip install --no-cache-dir --force-reinstall git+https://github.com/horovod/horovod.git@v0.28.1`
Thanks.

---

### 评论 #3 — vitduck (2024-11-07T01:09:03Z)

Hi @huanrwan-amd 
Thanks for reaching out. 

Sorry for not including the full log. I have now attached it per your request. 

If it helps, the following packages have been installed in my conda environment: 
```
Package                      Version
---------------------------- ---------
absl-py                      2.1.0
astunparse                   1.6.3
cachetools                   5.5.0
certifi                      2024.8.30
cffi                         1.17.1
charset-normalizer           3.4.0
cloudpickle                  3.1.0
flatbuffers                  24.3.25
gast                         0.6.0
google-auth                  2.35.0
google-auth-oauthlib         1.2.1
google-pasta                 0.2.0
grpcio                       1.67.1
h5py                         3.12.1
horovod                      0.28.1
idna                         3.10
keras                        2.15.0
libclang                     18.1.1
Markdown                     3.7
MarkupSafe                   3.0.2
ml-dtypes                    0.2.0
numpy                        1.26.4
oauthlib                     3.2.2
opt_einsum                   3.4.0
packaging                    24.1
pip                          24.2
protobuf                     4.25.5
psutil                       6.1.0
pyasn1                       0.6.1
pyasn1_modules               0.4.1
pycparser                    2.22
PyYAML                       6.0.2
requests                     2.32.3
requests-oauthlib            2.0.0
rsa                          4.9
setuptools                   75.1.0
six                          1.16.0
tensorboard                  2.15.2
tensorboard-data-server      0.7.2
tensorflow-estimator         2.15.0
tensorflow-io-gcs-filesystem 0.37.1
tensorflow-rocm              2.15.0
termcolor                    2.5.0
typing_extensions            4.12.2
urllib3                      2.2.3
Werkzeug                     3.0.6
wheel                        0.44.0
wrapt                        1.14.1
```
Other approaches I have tried: 
- Older horovod versions, e.g. `v0.28.0`, `v0.27.0`, gave same error. 
    - Though `v0.28.1` supposes to include fixes for ROCm build, according to release notes [ref](https://github.com/horovod/horovod/releases/tag/v0.28.1)
- The MPI backend built with `cray-mpich` works well. But we are hoping for better scalability with `RCCL`

My guess is that Horovod's build system is only compatible with ROCm up to v5, and not yet for v6. 
Since I don't have access to older ROCm tool chain, it is much appreciated if you can verify it on your end. 

Regards.
[horovod.txt](https://github.com/user-attachments/files/17654683/horovod.txt)


---

### 评论 #4 — huanrwan-amd (2024-11-07T17:02:25Z)

Hi @vitduck , thank for providing the logs. Can you please try setting env variable as:
```
HOROVOD_WITHOUT_MXNET=1 # Disable to build against MXNET
HOROVOD_WITH_TENSORFLOW=1
HOROVOD_ROCM_PATH=/opt/rocm # where your ROCm installation directory
HOROVOD_GPU=ROCM
HOROVOD_WITHOUT_PYTORCH=1 # Disable to build against pytorch
```
Thanks.


---

### 评论 #5 — vitduck (2024-11-08T00:47:16Z)

Thanks for the suggestion. 

While horovod was successfully built this way, without explicit set `HOROVOD_GPU_OPERATIONS=NCCL`, only the MPI backend with be built. 

This can be confirm with `horovod --check-build`

``` 
$ horovodrun --check-build 
Horovod v0.28.1:

Available Frameworks:
    [X] TensorFlow
    [X] PyTorch
    [ ] MXNet

Available Controllers:
    [X] MPI
    [X] Gloo

Available Tensor Operations:
    [ ] NCCL
    [ ] DDL
    [ ] CCL
    [X] MPI
    [X] Gloo    
```
Could you kindly check again on your end ? 
Thanks. 

---

### 评论 #6 — huanrwan-amd (2024-11-15T18:32:53Z)

Hi @vitduck , thanks for posting the findings.
We have some workaround on our HPE Cray, the environment may slightly different. You could try these on your side:
```
$ git clone --recursive https://github.com/horovod/horovod.git
$ cd horovod
$ ln -s $ROCM_PATH/lib/cmake/hip/FindHIP* cmake/Modules/
$ sed -i 's/rccl\.h/rccl\/rccl\.h/' horovod/common/ops/nccl_operations.h
$ CC=cc CXX=CC MAKEFLAGS=-j16 HOROVOD_GPU_BROADCAST=NCCL HOROVOD_GPU_ALLREDUCE=NCCL HOROVOD_WITHOUT_MXNET=1 HOROVOD_WITH_TENSORFLOW=1 HOROVOD_WITHOUT_GLOO=1 HOROVOD_WITH_MPI=1 HOROVOD_ROCM_PATH=$ROCM_PATH HOROVOD_ROCM_HOME=$ROCM_PATH HOROVOD_GPU=ROCM HOROVOD_WITHOUT_PYTORCH=1 python setup.py bdist_wheel
```
It adds symbolic link and modify the header location for rccl. Can you try these and send us the output? Thanks. 

---

### 评论 #7 — vitduck (2024-11-19T11:57:51Z)

Hi @huanrwan-amd 

Sorry for belated reply. 
I would like to confirm that the workaround allows horovod to be built against RCCL. 

The wheel package `horovod-0.28.1-cp310-cp310-linux_x86_64.whl` was successfully generated. 
Here is the correct output from `horovodrun`
```
$ horovodrun --check-build 
Available Frameworks:
    [X] TensorFlow
    [ ] PyTorch
    [ ] MXNet

Available Controllers:
    [X] MPI
    [X] Gloo

Available Tensor Operations:
    [X] NCCL
    [ ] DDL
    [ ] CCL
    [X] MPI
    [X] Gloo    
``` 

Setting `NCCL_DEBUG=info` also confirms that communication is carried out via RCCL at runtime, e.g. 
```
[1] NCCL INFO Channel 00/0 : 1[102000] -> 2[202000] via P2P/IPC comm 0x7f2ab8622e40 nRanks 08
[1] NCCL INFO Channel 01/0 : 6[202000] -> 1[102000] [receive] via NET/AWS Libfabric/1 comm 0x7f2ab8622e40 nRanks 08
```

This has been a major road block for us. Thanks so much for your help ! 
Please close the ticket as you see fit. 

Regards. 

---

### 评论 #8 — huanrwan-amd (2024-11-19T14:53:23Z)

Thank you for your response. We will also acknowledge the contributions of our internal team members. Happy to see it working on your side!

---

### 评论 #9 — TaneshimaPopura (2025-05-29T05:27:50Z)

Issue Report: Horovod ROCm Installation Failure
Environment Details
Build Methods: Both Docker and Conda environments
Base Image: rocm/pytorch
Configuration:
```
HOROVOD_GPU=ROCM
HOROVOD_ROCM_HOME=/opt/rocm
HOROVOD_GPU_OPERATIONS=NCCL
HOROVOD_WITH_PYTORCH=1
```
Error Description
During Horovod installation with ROCm support, the following errors occur consistently:
```
Total number of replaced kernel launches: 0
-- Build Horovod for ROCm
CMake Error at horovod/common/ops/rocm/CMakeLists.txt:21 (hip_add_library):
Unknown CMake command "hip_add_library"
```

Current Setup
```dockerfile
ARG VERSION
FROM rocm/pytorch:${VERSION}

RUN apt-get update && apt-get install -y \
    openmpi-bin \
    openmpi-common \
    libopenmpi-dev

RUN apt-get install -y \
    cmake \
    && rm -rf /var/lib/apt/lists/*

ENV HOROVOD_GPU=ROCM \
    HOROVOD_ROCM_HOME=/opt/rocm \
    HOROVOD_GPU_OPERATIONS=NCCL \
    HOROVOD_WITHOUT_TENSORFLOW=1 \
    HOROVOD_WITH_PYTORCH=1 \
    HOROVOD_WITH_MPI=1 \
    HOROVOD_WITHOUT_MXNET=1


# RUN pip install --no-cache-dir horovod

WORKDIR /workspace
```

## Full logs
```log
root@machine-learning:/workspace# pip install --no-cache-dir --force-reinstall git+https://github.com/horovod/horovod.git@v0.28.1
Collecting git+https://github.com/horovod/horovod.git@v0.28.1
  Cloning https://github.com/horovod/horovod.git (to revision v0.28.1) to /tmp/pip-req-build-_gn10hqn
  Running command git clone --filter=blob:none --quiet https://github.com/horovod/horovod.git /tmp/pip-req-build-_gn10hqn
  Running command git checkout -q 1d217b59949986d025f6db93c49943fb6b6cc78f
  Resolved https://github.com/horovod/horovod.git to commit 1d217b59949986d025f6db93c49943fb6b6cc78f
  Running command git submodule update --init --recursive -q
  Preparing metadata (setup.py) ... done
Collecting cloudpickle (from horovod==0.28.1)
  Downloading cloudpickle-3.1.1-py3-none-any.whl.metadata (7.1 kB)
Collecting psutil (from horovod==0.28.1)
  Downloading psutil-7.0.0-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (22 kB)
Collecting pyyaml (from horovod==0.28.1)
  Downloading PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
Collecting packaging (from horovod==0.28.1)
  Downloading packaging-25.0-py3-none-any.whl.metadata (3.3 kB)
Collecting cffi>=1.4.0 (from horovod==0.28.1)
  Downloading cffi-1.17.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (1.5 kB)
Collecting pycparser (from cffi>=1.4.0->horovod==0.28.1)
  Downloading pycparser-2.22-py3-none-any.whl.metadata (943 bytes)
Downloading cffi-1.17.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (479 kB)
Downloading cloudpickle-3.1.1-py3-none-any.whl (20 kB)
Downloading packaging-25.0-py3-none-any.whl (66 kB)
Downloading psutil-7.0.0-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (277 kB)
Downloading pycparser-2.22-py3-none-any.whl (117 kB)
Downloading PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (767 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 767.5/767.5 kB 9.0 MB/s eta 0:00:00
Building wheels for collected packages: horovod
  DEPRECATION: Building 'horovod' using the legacy setup.py bdist_wheel mechanism, which will be removed in a future version. pip 25.3 will enforce this behaviour change. A possible replacement is to use the standardized build interface by setting the `--use-pep517` option, (possibly combined with `--no-build-isolation`), or adding a `pyproject.toml` file to the source tree of 'horovod'. Discussion can be found at https://github.com/pypa/pip/issues/6334
  Building wheel for horovod (setup.py) ... error
  error: subprocess-exited-with-error
  
  × python setup.py bdist_wheel did not run successfully.
  │ exit code: 1
  ╰─> [323 lines of output]
      /opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/__init__.py:94: _DeprecatedInstaller: setuptools.installer and fetch_build_eggs are deprecated.
      !!
      
              ********************************************************************************
              Requirements should be satisfied by a PEP 517 installer.
              If you are using pip, you can try `pip install --use-pep517`.
              ********************************************************************************
      
      !!
        dist.fetch_build_eggs(dist.setup_requires)
      /opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/_distutils/dist.py:289: UserWarning: Unknown distribution option: 'tests_require'
        warnings.warn(msg)
      /opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/dist.py:759: SetuptoolsDeprecationWarning: License classifiers are deprecated.
      !!
      
              ********************************************************************************
              Please consider removing the following classifiers in favor of a SPDX license expression:
      
              License :: OSI Approved :: Apache Software License
      
              See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license for details.
              ********************************************************************************
      
      !!
        self._finalize_license_expression()
      running bdist_wheel
      running build
      running build_py
      creating build/lib.linux-x86_64-cpython-312/horovod
      copying horovod/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod
      creating build/lib.linux-x86_64-cpython-312/horovod/common
      copying horovod/common/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/common
      copying horovod/common/util.py -> build/lib.linux-x86_64-cpython-312/horovod/common
      copying horovod/common/elastic.py -> build/lib.linux-x86_64-cpython-312/horovod/common
      copying horovod/common/process_sets.py -> build/lib.linux-x86_64-cpython-312/horovod/common
      copying horovod/common/exceptions.py -> build/lib.linux-x86_64-cpython-312/horovod/common
      copying horovod/common/basics.py -> build/lib.linux-x86_64-cpython-312/horovod/common
      creating build/lib.linux-x86_64-cpython-312/horovod/torch
      copying horovod/torch/sync_batch_norm.py -> build/lib.linux-x86_64-cpython-312/horovod/torch
      copying horovod/torch/compression.py -> build/lib.linux-x86_64-cpython-312/horovod/torch
      copying horovod/torch/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/torch
      copying horovod/torch/optimizer.py -> build/lib.linux-x86_64-cpython-312/horovod/torch
      copying horovod/torch/mpi_ops.py -> build/lib.linux-x86_64-cpython-312/horovod/torch
      copying horovod/torch/functions.py -> build/lib.linux-x86_64-cpython-312/horovod/torch
      creating build/lib.linux-x86_64-cpython-312/horovod/_keras
      copying horovod/_keras/callbacks.py -> build/lib.linux-x86_64-cpython-312/horovod/_keras
      copying horovod/_keras/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/_keras
      copying horovod/_keras/elastic.py -> build/lib.linux-x86_64-cpython-312/horovod/_keras
      creating build/lib.linux-x86_64-cpython-312/horovod/spark
      copying horovod/spark/gloo_run.py -> build/lib.linux-x86_64-cpython-312/horovod/spark
      copying horovod/spark/runner.py -> build/lib.linux-x86_64-cpython-312/horovod/spark
      copying horovod/spark/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/spark
      copying horovod/spark/mpi_run.py -> build/lib.linux-x86_64-cpython-312/horovod/spark
      copying horovod/spark/conf.py -> build/lib.linux-x86_64-cpython-312/horovod/spark
      creating build/lib.linux-x86_64-cpython-312/horovod/mxnet
      copying horovod/mxnet/compression.py -> build/lib.linux-x86_64-cpython-312/horovod/mxnet
      copying horovod/mxnet/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/mxnet
      copying horovod/mxnet/mpi_ops.py -> build/lib.linux-x86_64-cpython-312/horovod/mxnet
      copying horovod/mxnet/functions.py -> build/lib.linux-x86_64-cpython-312/horovod/mxnet
      creating build/lib.linux-x86_64-cpython-312/horovod/keras
      copying horovod/keras/callbacks.py -> build/lib.linux-x86_64-cpython-312/horovod/keras
      copying horovod/keras/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/keras
      copying horovod/keras/elastic.py -> build/lib.linux-x86_64-cpython-312/horovod/keras
      creating build/lib.linux-x86_64-cpython-312/horovod/ray
      copying horovod/ray/driver_service.py -> build/lib.linux-x86_64-cpython-312/horovod/ray
      copying horovod/ray/runner.py -> build/lib.linux-x86_64-cpython-312/horovod/ray
      copying horovod/ray/utils.py -> build/lib.linux-x86_64-cpython-312/horovod/ray
      copying horovod/ray/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/ray
      copying horovod/ray/strategy.py -> build/lib.linux-x86_64-cpython-312/horovod/ray
      copying horovod/ray/ray_logger.py -> build/lib.linux-x86_64-cpython-312/horovod/ray
      copying horovod/ray/adapter.py -> build/lib.linux-x86_64-cpython-312/horovod/ray
      copying horovod/ray/worker.py -> build/lib.linux-x86_64-cpython-312/horovod/ray
      copying horovod/ray/elastic.py -> build/lib.linux-x86_64-cpython-312/horovod/ray
      copying horovod/ray/elastic_v2.py -> build/lib.linux-x86_64-cpython-312/horovod/ray
      creating build/lib.linux-x86_64-cpython-312/horovod/data
      copying horovod/data/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/data
      copying horovod/data/data_loader_base.py -> build/lib.linux-x86_64-cpython-312/horovod/data
      creating build/lib.linux-x86_64-cpython-312/horovod/tensorflow
      copying horovod/tensorflow/sync_batch_norm.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow
      copying horovod/tensorflow/compression.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow
      copying horovod/tensorflow/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow
      copying horovod/tensorflow/util.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow
      copying horovod/tensorflow/gradient_aggregation.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow
      copying horovod/tensorflow/elastic.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow
      copying horovod/tensorflow/gradient_aggregation_eager.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow
      copying horovod/tensorflow/mpi_ops.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow
      copying horovod/tensorflow/functions.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow
      creating build/lib.linux-x86_64-cpython-312/horovod/runner
      copying horovod/runner/launch.py -> build/lib.linux-x86_64-cpython-312/horovod/runner
      copying horovod/runner/gloo_run.py -> build/lib.linux-x86_64-cpython-312/horovod/runner
      copying horovod/runner/run_task.py -> build/lib.linux-x86_64-cpython-312/horovod/runner
      copying horovod/runner/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/runner
      copying horovod/runner/mpi_run.py -> build/lib.linux-x86_64-cpython-312/horovod/runner
      copying horovod/runner/task_fn.py -> build/lib.linux-x86_64-cpython-312/horovod/runner
      copying horovod/runner/js_run.py -> build/lib.linux-x86_64-cpython-312/horovod/runner
      creating build/lib.linux-x86_64-cpython-312/horovod/torch/elastic
      copying horovod/torch/elastic/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/torch/elastic
      copying horovod/torch/elastic/state.py -> build/lib.linux-x86_64-cpython-312/horovod/torch/elastic
      copying horovod/torch/elastic/sampler.py -> build/lib.linux-x86_64-cpython-312/horovod/torch/elastic
      creating build/lib.linux-x86_64-cpython-312/horovod/spark/lightning
      copying horovod/spark/lightning/estimator.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/lightning
      copying horovod/spark/lightning/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/lightning
      copying horovod/spark/lightning/util.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/lightning
      copying horovod/spark/lightning/remote.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/lightning
      copying horovod/spark/lightning/legacy.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/lightning
      copying horovod/spark/lightning/datamodule.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/lightning
      creating build/lib.linux-x86_64-cpython-312/horovod/spark/driver
      copying horovod/spark/driver/driver_service.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/driver
      copying horovod/spark/driver/rendezvous.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/driver
      copying horovod/spark/driver/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/driver
      copying horovod/spark/driver/rsh.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/driver
      copying horovod/spark/driver/host_discovery.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/driver
      copying horovod/spark/driver/mpirun_rsh.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/driver
      copying horovod/spark/driver/job_id.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/driver
      creating build/lib.linux-x86_64-cpython-312/horovod/spark/common
      copying horovod/spark/common/cache.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/common
      copying horovod/spark/common/estimator.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/common
      copying horovod/spark/common/serialization.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/common
      copying horovod/spark/common/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/common
      copying horovod/spark/common/util.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/common
      copying horovod/spark/common/store.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/common
      copying horovod/spark/common/params.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/common
      copying horovod/spark/common/backend.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/common
      copying horovod/spark/common/datamodule.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/common
      copying horovod/spark/common/constants.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/common
      copying horovod/spark/common/_namedtuple_fix.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/common
      creating build/lib.linux-x86_64-cpython-312/horovod/spark/torch
      copying horovod/spark/torch/estimator.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/torch
      copying horovod/spark/torch/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/torch
      copying horovod/spark/torch/util.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/torch
      copying horovod/spark/torch/remote.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/torch
      copying horovod/spark/torch/datamodule.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/torch
      creating build/lib.linux-x86_64-cpython-312/horovod/spark/data_loaders
      copying horovod/spark/data_loaders/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/data_loaders
      copying horovod/spark/data_loaders/pytorch_data_loaders.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/data_loaders
      creating build/lib.linux-x86_64-cpython-312/horovod/spark/task
      copying horovod/spark/task/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/task
      copying horovod/spark/task/gloo_exec_fn.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/task
      copying horovod/spark/task/mpirun_exec_fn.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/task
      copying horovod/spark/task/task_service.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/task
      copying horovod/spark/task/task_info.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/task
      creating build/lib.linux-x86_64-cpython-312/horovod/spark/keras
      copying horovod/spark/keras/estimator.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/keras
      copying horovod/spark/keras/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/keras
      copying horovod/spark/keras/util.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/keras
      copying horovod/spark/keras/remote.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/keras
      copying horovod/spark/keras/bare.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/keras
      copying horovod/spark/keras/optimizer.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/keras
      copying horovod/spark/keras/tensorflow.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/keras
      copying horovod/spark/keras/datamodule.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/keras
      creating build/lib.linux-x86_64-cpython-312/horovod/spark/tensorflow
      copying horovod/spark/tensorflow/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/tensorflow
      copying horovod/spark/tensorflow/compute_worker.py -> build/lib.linux-x86_64-cpython-312/horovod/spark/tensorflow
      creating build/lib.linux-x86_64-cpython-312/horovod/tensorflow/keras
      copying horovod/tensorflow/keras/callbacks.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow/keras
      copying horovod/tensorflow/keras/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow/keras
      copying horovod/tensorflow/keras/elastic.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow/keras
      creating build/lib.linux-x86_64-cpython-312/horovod/tensorflow/data
      copying horovod/tensorflow/data/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow/data
      copying horovod/tensorflow/data/compute_worker.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow/data
      copying horovod/tensorflow/data/compute_service.py -> build/lib.linux-x86_64-cpython-312/horovod/tensorflow/data
      creating build/lib.linux-x86_64-cpython-312/horovod/runner/http
      copying horovod/runner/http/http_server.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/http
      copying horovod/runner/http/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/http
      copying horovod/runner/http/http_client.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/http
      creating build/lib.linux-x86_64-cpython-312/horovod/runner/driver
      copying horovod/runner/driver/driver_service.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/driver
      copying horovod/runner/driver/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/driver
      creating build/lib.linux-x86_64-cpython-312/horovod/runner/common
      copying horovod/runner/common/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common
      creating build/lib.linux-x86_64-cpython-312/horovod/runner/util
      copying horovod/runner/util/cache.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/util
      copying horovod/runner/util/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/util
      copying horovod/runner/util/threads.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/util
      copying horovod/runner/util/network.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/util
      copying horovod/runner/util/remote.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/util
      copying horovod/runner/util/lsf.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/util
      copying horovod/runner/util/streams.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/util
      creating build/lib.linux-x86_64-cpython-312/horovod/runner/elastic
      copying horovod/runner/elastic/settings.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/elastic
      copying horovod/runner/elastic/rendezvous.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/elastic
      copying horovod/runner/elastic/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/elastic
      copying horovod/runner/elastic/worker.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/elastic
      copying horovod/runner/elastic/constants.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/elastic
      copying horovod/runner/elastic/driver.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/elastic
      copying horovod/runner/elastic/discovery.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/elastic
      copying horovod/runner/elastic/registration.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/elastic
      creating build/lib.linux-x86_64-cpython-312/horovod/runner/task
      copying horovod/runner/task/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/task
      copying horovod/runner/task/task_service.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/task
      creating build/lib.linux-x86_64-cpython-312/horovod/runner/common/service
      copying horovod/runner/common/service/driver_service.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/service
      copying horovod/runner/common/service/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/service
      copying horovod/runner/common/service/task_service.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/service
      copying horovod/runner/common/service/compute_service.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/service
      creating build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/settings.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/secret.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/__init__.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/network.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/config_parser.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/hosts.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/env.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/tiny_shell_exec.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/timeout.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/host_hash.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/codec.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      copying horovod/runner/common/util/safe_shell_exec.py -> build/lib.linux-x86_64-cpython-312/horovod/runner/common/util
      running build_ext
      Running CMake in build/temp.linux-x86_64-cpython-312/RelWithDebInfo:
      cmake /tmp/pip-req-build-_gn10hqn -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO=/tmp/pip-req-build-_gn10hqn/build/lib.linux-x86_64-cpython-312 -DPYTHON_EXECUTABLE:FILEPATH=/opt/conda/envs/py_3.12/bin/python3.12
      cmake --build . --config RelWithDebInfo -- -j8 VERBOSE=1
      -- Could not find CCache. Consider installing CCache to speed up compilation.
      -- The CXX compiler identification is GNU 13.3.0
      -- Detecting CXX compiler ABI info
      -- Detecting CXX compiler ABI info - done
      -- Check for working CXX compiler: /usr/bin/c++ - skipped
      -- Detecting CXX compile features
      -- Detecting CXX compile features - done
      -- Build architecture flags: -mf16c -mavx -mfma
      -- Using command /opt/conda/envs/py_3.12/bin/python3.12
      -- Found MPI_CXX: /usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi_cxx.so (found version "3.1")
      -- Found MPI: TRUE (found version "3.1")
      -- Looking for a CUDA compiler
      -- Looking for a CUDA compiler - NOTFOUND
      -- Looking for a CUDA host compiler - /usr/bin/c++
      -- Could not find nvcc, please set CUDAToolkit_ROOT.
      -- Performing Test CMAKE_HAVE_LIBC_PTHREAD
      -- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Success
      -- Found Threads: TRUE
      -- HIP library name: amdhip64
      -- Found ROCM: /opt/rocm/lib/libamdhip64.so
      -- Could NOT find NVTX (missing: NVTX_INCLUDE_DIR)
      CMake Deprecation Warning at third_party/gloo/CMakeLists.txt:1 (cmake_minimum_required):
        Compatibility with CMake < 3.10 will be removed from a future version of
        CMake.
      
        Update the VERSION argument <min> value.  Or, use the <min>...<max> syntax
        to tell CMake that the project requires at least <min> but has been updated
        to work with policies introduced by <max> or earlier.
      
      
      -- The C compiler identification is GNU 13.3.0
      -- Detecting C compiler ABI info
      -- Detecting C compiler ABI info - done
      -- Check for working C compiler: /usr/bin/cc - skipped
      -- Detecting C compile features
      -- Detecting C compile features - done
      -- Enabling sccache for CXX
      -- Enabling sccache for C
      -- Gloo build as STATIC library
      -- Found MPI_C: /usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi.so (found version "3.1")
      -- Found MPI: TRUE (found version "3.1")
      -- MPI include path: /usr/lib/x86_64-linux-gnu/openmpi/include/usr/lib/x86_64-linux-gnu/openmpi/include/openmpi
      -- MPI libraries: /usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi_cxx.so/usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi.so
      -- Found Pytorch: 2.6.0+git684f6f2 (found suitable version "2.6.0+git684f6f2", minimum required is "1.5.0")
      /tmp/pip-req-build-_gn10hqn/horovod/torch/handle_manager.h -> /tmp/pip-req-build-_gn10hqn/horovod/torch/handle_manager.h [skipped, no changes]
      /tmp/pip-req-build-_gn10hqn/horovod/torch/handle_manager.cc -> /tmp/pip-req-build-_gn10hqn/horovod/torch/handle_manager.cc [skipped, no changes]
      /tmp/pip-req-build-_gn10hqn/horovod/torch/adapter_v2.h -> /tmp/pip-req-build-_gn10hqn/horovod/torch/adapter_v2.h [skipped, no changes]
      /tmp/pip-req-build-_gn10hqn/horovod/torch/cuda_util.h -> /tmp/pip-req-build-_gn10hqn/horovod/torch/cuda_util.h [skipped, no changes]
      /tmp/pip-req-build-_gn10hqn/horovod/torch/ready_event.h -> /tmp/pip-req-build-_gn10hqn/horovod/torch/ready_event_hip.h [ok]
      /tmp/pip-req-build-_gn10hqn/horovod/torch/adapter_v2.cc -> /tmp/pip-req-build-_gn10hqn/horovod/torch/adapter_v2_hip.cc [ok]
      /tmp/pip-req-build-_gn10hqn/horovod/torch/ready_event.h -> /tmp/pip-req-build-_gn10hqn/horovod/torch/ready_event_hip.h [skipped, already hipified]
      /tmp/pip-req-build-_gn10hqn/horovod/torch/handle_manager.h -> /tmp/pip-req-build-_gn10hqn/horovod/torch/handle_manager.h [skipped, no changes]
      /tmp/pip-req-build-_gn10hqn/horovod/torch/cuda_util.h -> /tmp/pip-req-build-_gn10hqn/horovod/torch/cuda_util.h [skipped, no changes]
      /tmp/pip-req-build-_gn10hqn/horovod/torch/cuda_util.cc -> /tmp/pip-req-build-_gn10hqn/horovod/torch/hip_util.cc [ok]
      /tmp/pip-req-build-_gn10hqn/horovod/torch/ready_event.cc -> /tmp/pip-req-build-_gn10hqn/horovod/torch/ready_event_hip.cc [ok]
      /tmp/pip-req-build-_gn10hqn/horovod/torch/mpi_ops_v2.cc -> /tmp/pip-req-build-_gn10hqn/horovod/torch/mpi_ops_v2_hip.cc [ok]
      Successfully preprocessed all matching files.
      Total number of unsupported CUDA function calls: 0
      
      
      Total number of replaced kernel launches: 0
      -- Build Horovod for ROCm
      CMake Error at horovod/common/ops/rocm/CMakeLists.txt:21 (hip_add_library):
        Unknown CMake command "hip_add_library".
      
      
      -- Configuring incomplete, errors occurred!
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
        File "<pip-setuptools-caller>", line 35, in <module>
        File "/tmp/pip-req-build-_gn10hqn/setup.py", line 213, in <module>
          setup(name='horovod',
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/__init__.py", line 117, in setup
          return distutils.core.setup(**attrs)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/_distutils/core.py", line 186, in setup
          return run_commands(dist)
                 ^^^^^^^^^^^^^^^^^^
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/_distutils/core.py", line 202, in run_commands
          dist.run_commands()
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/_distutils/dist.py", line 1002, in run_commands
          self.run_command(cmd)
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/dist.py", line 1104, in run_command
          super().run_command(command)
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/_distutils/dist.py", line 1021, in run_command
          cmd_obj.run()
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/command/bdist_wheel.py", line 370, in run
          self.run_command("build")
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/_distutils/cmd.py", line 357, in run_command
          self.distribution.run_command(command)
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/dist.py", line 1104, in run_command
          super().run_command(command)
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/_distutils/dist.py", line 1021, in run_command
          cmd_obj.run()
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/_distutils/command/build.py", line 135, in run
          self.run_command(cmd_name)
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/_distutils/cmd.py", line 357, in run_command
          self.distribution.run_command(command)
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/dist.py", line 1104, in run_command
          super().run_command(command)
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/_distutils/dist.py", line 1021, in run_command
          cmd_obj.run()
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/command/build_ext.py", line 99, in run
          _build_ext.run(self)
        File "/opt/conda/envs/py_3.12/lib/python3.12/site-packages/setuptools/_distutils/command/build_ext.py", line 368, in run
          self.build_extensions()
        File "/tmp/pip-req-build-_gn10hqn/setup.py", line 145, in build_extensions
          subprocess.check_call(command, cwd=cmake_build_dir)
        File "/opt/conda/envs/py_3.12/lib/python3.12/subprocess.py", line 413, in check_call
          raise CalledProcessError(retcode, cmd)
      subprocess.CalledProcessError: Command '['cmake', '/tmp/pip-req-build-_gn10hqn', '-DCMAKE_BUILD_TYPE=RelWithDebInfo', '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO=/tmp/pip-req-build-_gn10hqn/build/lib.linux-x86_64-cpython-312', '-DPYTHON_EXECUTABLE:FILEPATH=/opt/conda/envs/py_3.12/bin/python3.12']' returned non-zero exit status 1.
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for horovod
  Running setup.py clean for horovod
Failed to build horovod
ERROR: Failed to build installable wheels for some pyproject.toml based projects (horovod)
root@machine-learning:/workspace# 
```

---

### 评论 #10 — TaneshimaPopura (2025-05-29T06:04:37Z)

![Image](https://github.com/user-attachments/assets/73cd510b-0243-4ed1-baec-d331462f1953)
Maybe should I make a link?

I found that many problems come from the path changes of the new version. Are there any related links for the original old version?

---
