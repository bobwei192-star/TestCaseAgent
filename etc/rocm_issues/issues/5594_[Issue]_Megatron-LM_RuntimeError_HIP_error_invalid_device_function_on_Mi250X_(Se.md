# [Issue]: Megatron-LM: "RuntimeError: HIP error: invalid device function" on Mi250X (Setonix)

> **Issue #5594**
> **状态**: closed
> **创建时间**: 2025-10-29T09:45:02Z
> **更新时间**: 2025-11-27T17:05:18Z
> **关闭时间**: 2025-11-27T17:05:18Z
> **作者**: alexchen5
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5594

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

I’m encountering a `RuntimeError: HIP error: invalid device function` when trying to run LLM pretraining using Megatron-LM. I've tried running both images [rocm/megatron-lm:latest](https://hub.docker.com/layers/rocm/megatron-lm/latest/images/sha256-0030c4a3dcb233c66dd5f61135821f9f5c4e321cbe0a2cdc74f110752f28c869) and [rocm/megatron-lm:v25.4](https://hub.docker.com/layers/rocm/megatron-lm/v25.4/images/sha256-941aa5387918ea91c376c13083aa1e6c9cab40bb1875abbbb73bbb65d8736b3f), but both get the same error. 

I suspect the cause is due to the "nccl" backend option being used for `torch.distributed` throughout the Megatron-LM codebase. Now "nccl" isn't supported for AMD GPUs (i think??), so to me it seems that "gloo" should be used instead, but I'm probably missing something as it's unclear how others have been running successfully with the same images. 

### Operating System

SLES 15-SP6

### CPU

AMD EPYC 7A53 64-Core Processor

### GPU

8 x AMD Instinct MI250X

### ROCm Version

6.4.43484-123eb5128

### ROCm Component

_No response_

### Steps to Reproduce

1. `module load singularity/3.11.4-slurm` to load singularity (which used in place of docker in Setonix)
2. `singularity pull --dir $MYSOFTWARE/singularity/rocm docker://rocm/megatron-lm:latest` to pull rocm image of megatron-lm
3. `singularity exec
    --pwd /workspace/Megatron-LM
    $MYSOFTWARE/singularity/rocm/megatron-lm_latest.sif
    bash ~/scripts/megatron_benchmark/bench_llama3.sh`
to run the training script (`bench_llama3.sh` is a clone of `examples/llama/train_llama3.sh` - which I have included below). 

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

<details>
<summary>bench_llama3.sh</summary>

```
#!/bin/bash
###############################################################################
# Copyright (c) 2024, Advanced Micro Devices, Inc. All rights reserved.
#
# See LICENSE for license information.
#################################################################################
#set -x

export HIP_VISIBLE_DEVICES=$ROCR_VISIBLE_DEVICES
echo HIP_VISIBLE_DEVICES=$HIP_VISIBLE_DEVICES
EXPERIMENT_DIR="$MYSCRATCH/megatron_experiment"
declare -i MODEL_SIZE=8

TEE_OUTPUT=1 
MBS=2 
BS=64 
TP=8 
TE_FP8=0 
SEQ_LENGTH=4096 

# TOKENIZER_MODEL=meta-llama/Llama-3.3-70B-Instruct 
# CKPT_FORMAT=torch_dist 
# TEE_OUTPUT=1 
# RECOMPUTE=1 
# SEQ_LENGTH=8192 
# MBS=2 
# BS=16 
# TE_FP8=0 
# TP=1 
# PP=1 
# FSDP=1 
# MODEL_SIZE=70 
# TOTAL_ITERS=50 

# set envs 
export GPU_MAX_HW_QUEUES=${GPU_MAX_HW_QUEUES:-2}
export TORCH_NCCL_HIGH_PRIORITY=${TORCH_NCCL_HIGH_PRIORITY:-1}
export NCCL_CHECKS_DISABLE=${NCCL_CHECKS_DISABLE:-1}
NCCL_IB_HCA_LIST=$(rdma link -j | python3 -c "import sys, json; links=json.load(sys.stdin);names=[links[i]['ifname'] for i in range(8)]; print(*names,sep=',')")
export NCCL_IB_HCA=${NCCL_IB_HCA:-$NCCL_IB_HCA_LIST}
export NCCL_IB_GID_INDEX=${NCCL_IB_GID_INDEX:-3}
export NCCL_CROSS_NIC=${NCCL_CROSS_NIC:-0}
export CUDA_DEVICE_MAX_CONNECTIONS=${CUDA_DEVICE_MAX_CONNECTIONS:-1}
export NCCL_PROTO=${NCCL_PROTO:-Simple}
export RCCL_MSCCL_ENABLE=${RCCL_MSCCL_ENABLE:-0}
export TOKENIZERS_PARALLELISM=${TOKENIZERS_PARALLELISM:-false}
export HSA_NO_SCRATCH_RECLAIM=${HSA_NO_SCRATCH_RECLAIM:-1}

# parsing input arguments
for ARGUMENT in "$@"
do
   KEY=$(echo $ARGUMENT | cut -f1 -d=)

   KEY_LENGTH=${#KEY}
   VALUE="${ARGUMENT:$KEY_LENGTH+1}"

   export "$KEY"="$VALUE"
done

TIME_STAMP=$(date +"%Y-%m-%d_%H-%M-%S")
EXP_NAME="${EXP_NAME:-perf}"

TEE_OUTPUT="${TEE_OUTPUT:-1}"
USE_FLASH_ATTN="${USE_FLASH_ATTN:-1}"
NO_TRAINING="${NO_TRAINING:-0}" # NO_TRAINING=1: for computing metrics only
ENABLE_PROFILING="${ENABLE_PROFILING:-0}" #enable pytorch profiling
echo "NO_TRAINING=$NO_TRAINING"

CWD=`pwd`
GPUS_PER_NODE=`python3 -c "import torch; print(torch.cuda.device_count())"`

# single node config, Change for multinode config
MASTER_ADDR="${MASTER_ADDR:-"127.0.0.1"}"
MASTER_PORT="${MASTER_PORT:-29500}"
NNODES="${NNODES:-1}"
NODE_RANK="${NODE_RANK:-0}"
WORLD_SIZE=$(($GPUS_PER_NODE*$NNODES))

if [ "${NNODES:-1}" -gt 1 ]; then
    export NCCL_SOCKET_IFNAME="${NCCL_SOCKET_IFNAME:-ens51np0}"
    export GLOO_SOCKET_IFNAME="${GLOO_SOCKET_IFNAME:-ens51np0}"
    echo "NCCL and GLOO socket interfaces set."
else
    echo "Single node setup, skipping NCCL and GLOO socket interface settings."
fi

MODEL_SIZE="${MODEL_SIZE:-70}"
TP="${TP:-8}"
PP="${PP:-1}"
CP="${CP:-1}"
MBS="${MBS:-1}"
BS="${BS:-8}"
SEQ_LENGTH="${SEQ_LENGTH:-2048}"
MAX_POSITION_EMBEDDINGS=131072
TOTAL_ITERS="${TOTAL_ITERS:-10}"
SEQ_PARALLEL="${SEQ_PARALLEL:-1}" 
CONTI_PARAMS="${CONTI_PARAMS:-0}"
TE_FP8="${TE_FP8:-0}"  # 0: disable FP8, 1: enable FP8
GEMM_TUNING="${GEMM_TUNING:-1}"
MCORE="${MCORE:-1}"
OPTIMIZER="${OPTIMIZER:-adam}"
FSDP="${FSDP:-0}"
RECOMPUTE="${RECOMPUTE:-0}"
TOKENIZER_TYPE="${TOKENIZER_TYPE:-HuggingFaceTokenizer}"
TOKENIZER_MODEL="${TOKENIZER_MODEL:-NousResearch/Meta-Llama-3-8B}"
ROPE_FUSION="${ROPE_FUSION:-1}" # 1: use rope-fusion, 0: no-rope-fusion
LOG_INTERVAL="${LOG_INTERVAL:-1}"
EVAL_INTERVAL="${EVAL_INTERVAL:-5000}"
SAVE_INTERVAL="${SAVE_INTERVAL:-5000}"
EVAL_ITERS="${EVAL_ITERS:-'-1'}"
CKPT_FORMAT="${CKPT_FORMAT:-torch}"
DATA_CACHE_PATH="${DATA_CACHE_PATH:-/root/cache}"
FP8_WEIGHT_TRANSPOSE_CACHE="${FP8_WEIGHT_TRANSPOSE_CACHE:-1}"

if [ "$FSDP" -eq 1 ]; then
    if [ "$TP" -gt 1 ]; then
        echo "It is not recommended to use FSDP and TP together. Disabling TP."
        TP=1
        echo "Resetting TP=$TP"
    fi
fi

EXPERIMENT_DIR="${EXPERIMENT_DIR:-"experiment"}"
mkdir -p $EXPERIMENT_DIR
DEFAULT_LOG_DIR="${EXPERIMENT_DIR}/${NNODES}nodes_rank${NODE_RANK}_train_${MODEL_SIZE}B_mbs${MBS}_bs${BS}_tp${TP}_pp${PP}_cp${CP}_iter${TOTAL_ITERS}/TE_FP8_${TE_FP8}/${TIME_STAMP}"
LOG_DIR="${LOG_DIR:-${DEFAULT_LOG_DIR}}"
TRAIN_LOG="${LOG_DIR}/output_${EXP_NAME}.log"
mkdir -p $LOG_DIR
echo $TRAIN_LOG

# gemm tuning
if [ "$GEMM_TUNING" -eq 1 ]; then
    export TE_HIPBLASLT_TUNING_RUN_COUNT=10
    export TE_HIPBLASLT_TUNING_ALGO_COUNT=50
fi

if [ "$SEQ_LENGTH" -le 8192 ]; then
    ds_works=8
else
    ds_works=24
fi

if [[ $MODEL_SIZE -eq 8 ]]; then #llama3.1-8B
    HIDDEN_SIZE=4096 # e.g. llama-13b: 5120
    FFN_HIDDEN_SIZE=14336 # e.g. llama-13b: 13824
    NUM_LAYERS=${NUM_LAYERS:-32} # e.g. llama-13b: 40
    NUM_HEADS=32 # e.g. llama-13b: 40
    NUM_KV_HEADS=8
elif [[ $MODEL_SIZE -eq 70 ]]; then
    HIDDEN_SIZE=8192 # e.g. llama-13b: 5120
    FFN_HIDDEN_SIZE=28672 # e.g. llama-13b: 13824
    NUM_LAYERS=${NUM_LAYERS:-80} # e.g. llama-13b: 40
    NUM_HEADS=64 # e.g. llama-13b: 40
    NUM_KV_HEADS=8 # llama3 70B uses GQA
else
    echo "Model size not supported."
    exit 1
fi

GROUP_SIZE=$(( ${NUM_HEADS} / ${NUM_KV_HEADS} ))
NUM_GROUPS=$(( ${NUM_HEADS} / ${GROUP_SIZE} ))

PROFILING_DIR="${LOG_DIR}/trace_${EXP_NAME}"

GPT_ARGS="
    --tensor-model-parallel-size ${TP} \
    --pipeline-model-parallel-size ${PP} \
    --context-parallel-size ${CP} \
    --num-layers $NUM_LAYERS \
    --hidden-size $HIDDEN_SIZE \
    --ffn-hidden-size $FFN_HIDDEN_SIZE \
    --num-attention-heads $NUM_HEADS \
    --seq-length $SEQ_LENGTH \
    --max-position-embeddings $MAX_POSITION_EMBEDDINGS \
    --untie-embeddings-and-output-weights \
    --position-embedding-type rope \
    --no-position-embedding \
    --swiglu \
    --disable-bias-linear \
    --init-method-std 0.02 \
    --attention-dropout 0.0 \
    --hidden-dropout 0.0 \
    --normalization RMSNorm \
    --micro-batch-size $MBS \
    --global-batch-size $BS \
    --train-iters $TOTAL_ITERS \
    --no-async-tensor-model-parallel-allreduce \
    --bf16 \
    --no-masked-softmax-fusion \
"

if [ "$RECOMPUTE" -eq 1 ]; then
    GPT_ARGS="$GPT_ARGS --recompute-num-layers $NUM_LAYERS \
        --recompute-granularity full \
        --recompute-method block \
        "
fi
if [ "$ROPE_FUSION" -eq 0 ]; then
    GPT_ARGS="$GPT_ARGS --no-rope-fusion"
fi

TRAIN_ARGS="--lr 1e-4 \
    --min-lr 1e-5 \
    --lr-decay-iters 320000 \
    --lr-decay-style cosine \
    --weight-decay 1.0e-1 \
    --clip-grad 1.0 \
"
if [ "$OPTIMIZER" == "adam" ]; then
    TRAIN_ARGS="$TRAIN_ARGS --optimizer adam \
        --adam-beta1 0.9 \
        --adam-beta2 0.95 \
        "
else
    TRAIN_ARGS="$TRAIN_ARGS --optimizer sgd \
        "
fi

DATA_ARGS="
    --tokenizer-type ${TOKENIZER_TYPE} \
    --tokenizer-model ${TOKENIZER_MODEL} \
    --dataloader-type cyclic \
    --save-interval 200000 \
    --tensorboard-dir $LOG_DIR \
    --log-interval 1 \
    --eval-interval 320000 \
    --eval-iters 10 \
    --num-workers $ds_works \
"
if [ -z ${DATA_PATH+x} ]; then
    DATA_ARGS="$DATA_ARGS --mock-data"
    echo "Using Mock data"
else
    DATA_ARGS="$DATA_ARGS --data-path $DATA_PATH"
    echo "Using ${DATA_PATH} data"
fi
if [ "$NNODES" -gt 1 ]; then
    # For multi-node runs DATA_CACHE_PATH should exist and should point to a common
    # path accessible by all the nodes (for example, a NFS directory)"
    DATA_ARGS="$DATA_ARGS --data-cache-path $DATA_CACHE_PATH"
fi

OUTPUT_ARGS="
    --log-interval $LOG_INTERVAL \
    --log-throughput \
    --no-save-optim \
    --no-save-rng \
    --eval-iters $EVAL_ITERS
"
if [ -n "$SAVE_CKPT_PATH" ]; then
    OUTPUT_ARGS="$OUTPUT_ARGS \
        --save-interval $SAVE_INTERVAL \
        --eval-interval $EVAL_INTERVAL \
        --ckpt-format $CKPT_FORMAT \
        --save $SAVE_CKPT_PATH
    "
fi

CKPT_LOAD_ARGS=""
if [ -n "$LOAD_CKPT_PATH" ]; then
    CKPT_LOAD_ARGS="$CKPT_LOAD_ARGS \
        --exit-on-missing-checkpoint \
        --no-load-optim \
        --no-load-rng \
        --use-checkpoint-args \
        --load ${LOAD_CKPT_PATH}"
fi

DISTRIBUTED_ARGS="
    --nproc_per_node $GPUS_PER_NODE \
    --nnodes $NNODES \
    --node_rank $NODE_RANK \
    --master_addr $MASTER_ADDR \
    --master_port $MASTER_PORT \
"

EXTRA_ARGS="
    --group-query-attention \
    --num-query-groups $NUM_GROUPS \
    --no-gradient-accumulation-fusion \
    --distributed-backend gloo \
    --tp_comm_bootstrap_backend gloo \
    --distributed-timeout-minutes 120 \
    --overlap-grad-reduce \
"

if [ "$FSDP" -eq 1 ]; then
    EXTRA_ARGS="$EXTRA_ARGS --use-torch-fsdp2"
    if [ "$SEQ_PARALLEL" -eq 1 ]; then
        echo "Warning: Sequence Parallelism and FSDP2 have conflicting CUDA_MAX_CONNECTIONS requirements. It is recommended not to use them together."
        echo "FSDP2 and sequence parallel are on. Disabling sequence parallel."
        SEQ_PARALLEL=0
    fi
else
    if [ "$OPTIMIZER" == "adam" ]; then
        EXTRA_ARGS="$EXTRA_ARGS --use-distributed-optimizer --overlap-param-gather"
    fi
fi

if [ "$ENABLE_PROFILING" -eq 1 ]; then
    EXTRA_ARGS="$EXTRA_ARGS --profile --use-pytorch-profiler --tensorboard-dir $LOG_DIR"
fi

if [ "$USE_FLASH_ATTN" -eq 1 ]; then
    EXTRA_ARGS="$EXTRA_ARGS --use-flash-attn"
fi

if [ "$SEQ_PARALLEL" -eq 1 ]; then
    EXTRA_ARGS="$EXTRA_ARGS --sequence-parallel"
fi

if [ "$CONTI_PARAMS" -eq 1 ]; then
    EXTRA_ARGS="$EXTRA_ARGS --use-contiguous-parameters-in-local-ddp"
fi

if [ "$MCORE" -eq 1 ]; then
    EXTRA_ARGS="$EXTRA_ARGS --use-mcore-models"
fi

if [ "$TE_FP8" -eq 1 ]; then
    # cast transpose optimization for fp8
    export NVTE_USE_CAST_TRANSPOSE_TRITON=1
    
    EXTRA_ARGS="$EXTRA_ARGS --transformer-impl=transformer_engine \
        --fp8-margin=0 \
        --fp8-format=hybrid \
        --fp8-interval=1 \
        --fp8-amax-history-len=1024 \
        --fp8-amax-compute-algo=max \
        --attention-softmax-in-fp32 \
"

    if [ "$FSDP" -eq 1 ] && [ "$FP8_WEIGHT_TRANSPOSE_CACHE" -eq 0 ]; then
        EXTRA_ARGS="$EXTRA_ARGS --no-fp8-weight-transpose-cache \
        --no-fp8-reduce-amax \
        " 
        # NOTE: This option may cause performance regression
        # EXTRA_ARGS="$EXTRA_ARGS --no-fp8-weight-cache \
        # " 
    fi
fi

if [ -n "${WANDB_API_KEY}" ]; then
    LOGGING_ARGS="--wandb-project=LLama \
        --wandb-exp-name=LLama_${MODEL_SIZE}B \
        --wandb-save-dir logs/wandb \
    "
else
   LOGGING_ARGS=""
fi

run_cmd="
    python -m torch.distributed.run $DISTRIBUTED_ARGS pretrain_gpt.py \
        $GPT_ARGS \
        $DATA_ARGS \
        $OUTPUT_ARGS \
        $EXTRA_ARGS \
        $TRAIN_ARGS \
        $LOGGING_ARGS \
        $CKPT_LOAD_ARGS
"

if [ "$TEE_OUTPUT" -eq 0 ]; then 
    run_cmd="$run_cmd >& $TRAIN_LOG"
else
    run_cmd="$run_cmd |& tee $TRAIN_LOG"
fi

if [ "$NO_TRAINING" -eq 0 ]; then 
    eval $run_cmd
fi


echo 'import argparse
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog="Process Log")
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        lines = f.readlines()
    lines = lines[2:-1]
    lines = [float(a) for a in lines]
    mean = np.mean(np.array(lines))
    print(mean)' > ${LOG_DIR}/mean_log_value.py


# echo '============================================================================================================'
grep -Eo 'throughput per GPU [^|]*' $TRAIN_LOG | sed -E 's/.*throughput per GPU \(TFLOP\/s\/GPU\): ([0-9\.]+).*/\1/' > ${LOG_DIR}/tmp.txt
PERFORMANCE=$(python3 ${LOG_DIR}/mean_log_value.py ${LOG_DIR}/tmp.txt)
echo "throughput per GPU: $PERFORMANCE" |& tee -a $TRAIN_LOG
rm ${LOG_DIR}/tmp.txt

# echo '============================================================================================================'
grep -Eo 'elapsed time per iteration [^|]*' $TRAIN_LOG | sed -E 's/.*elapsed time per iteration \(ms\): ([0-9\.]+).*/\1/' > ${LOG_DIR}/tmp.txt
ETPI=$(python3 ${LOG_DIR}/mean_log_value.py ${LOG_DIR}/tmp.txt)
echo "elapsed time per iteration: $ETPI" |& tee -a $TRAIN_LOG

TIME_PER_ITER=$(python3 ${LOG_DIR}/mean_log_value.py ${LOG_DIR}/tmp.txt 2>/dev/null | awk '{printf "%.6f", $0}')
TGS=$(awk -v bs="$BS" -v sl="$SEQ_LENGTH" -v tpi="$TIME_PER_ITER" -v ws="$WORLD_SIZE" 'BEGIN {printf "%.6f", bs * sl * 1000/ (tpi * ws)}')
echo "tokens/GPU/s: $TGS" |& tee -a $TRAIN_LOG

# Extract memory usage
grep -Eo 'mem usages: [^|]*' "$TRAIN_LOG" | sed -E 's/.*mem usages: ([0-9\.]+).*/\1/' > ${LOG_DIR}/tmp.txt
MEMUSAGE=$(python3 ${LOG_DIR}/mean_log_value.py ${LOG_DIR}/tmp.txt)
echo "mem usages: $MEMUSAGE" |& tee -a "$TRAIN_LOG"
rm ${LOG_DIR}/tmp.txt

```
</details>

---

## 评论 (6 条)

### 评论 #1 — alexchen5 (2025-11-02T01:28:52Z)

"nccl" should be supported on AMD GPUs, as with proper pytorch installation "rccl" would be used under the hood. The root cause of the issue is probably an incompatibility of the megatron-lm images with MI250X. I've confirmed this by running a simple pytorch.distributed test script using "nccl" (see below) which ran with no issues on [rocm/pytorch:latest](https://hub.docker.com/layers/rocm/pytorch/latest/images/sha256-3e917342db23b080cc7aa274321b4a7f33eb321e71b9607d69c0cb4deaaa8820) but fails on both [rocm/megatron-lm:latest](https://hub.docker.com/layers/rocm/megatron-lm/latest/images/sha256-0030c4a3dcb233c66dd5f61135821f9f5c4e321cbe0a2cdc74f110752f28c869) and [rocm/megatron-lm:v25.4](https://hub.docker.com/layers/rocm/megatron-lm/v25.4/images/sha256-941aa5387918ea91c376c13083aa1e6c9cab40bb1875abbbb73bbb65d8736b3f). 

<details>

<summary>Test script: nccl_barrier.py</summary>

```
import os
import time
import torch
import torch.distributed as dist
import torch.multiprocessing as mp


def worker(rank, world_size):
    """Worker function for each process."""
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = "29500"  # Use any free port

    # Initialize the process group
    dist.init_process_group("nccl", rank=rank, world_size=world_size)

    print(f"Rank {rank} initialized")

    # Simulate staggered start to test synchronization
    if rank == 0:
        print(f"Rank {rank} sleeping 3 seconds before barrier...")
        time.sleep(3)

    print(f"Rank {rank} entering barrier at {time.strftime('%X')}")
    dist.barrier()
    print(f"Rank {rank} passed barrier at {time.strftime('%X')}")

    dist.destroy_process_group()


def main():
    world_size = 4  # Number of processes to test
    mp.spawn(worker, args=(world_size,), nprocs=world_size, join=True)


if __name__ == "__main__":
    main()
```

</details>

---

### 评论 #2 — lucbruni-amd (2025-11-02T18:15:23Z)

Hi @alexchen5,

You are correct, this is not a RCCL issue and instead compatibility of the Docker image with MI250X. See [here](https://hub.docker.com/layers/rocm/megatron-lm/latest/) for image layering which favours MI300-series GPUs. The [documentation](https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/training/benchmark-docker/primus-megatron.html) also supports this.

Unfortunately these cards are not supported with the latest images. I will check whether there is an alternative for you, as I know you will likely not have admin privileges on Setonix to run everything baremetal. Sorry for the inconvenience.

---

### 评论 #3 — lucbruni-amd (2025-11-03T14:39:44Z)

Hi @alexchen5,

Could you try building this image with the following Dockerfile:

```
FROM "rocm/pytorch:rocm6.3.4_ubuntu22.04_py3.10_pytorch_release_2.4.0"

RUN rm -rf apex

RUN apt update \
    && apt install -y nano wget ninja-build \
    && apt install -y python3 python3-pip git \
    && apt install -y sqlite3 libsqlite3-dev libfmt-dev libmsgpack-dev libsuitesparse-dev \
    && apt install -y python3.10-venv ccache \
    && apt install iproute2 -y \
    && apt install -y linux-headers-"$(uname -r)" libelf-dev \
    && apt install -y gcc make libtool autoconf librdmacm-dev rdmacm-utils infiniband-diags ibverbs-utils perftest ethtool libibverbs-dev rdma-core strace libibmad5 libibnetdisc5 ibverbs-providers libibumad-dev libibumad3 libibverbs1 libnl-3-dev libnl-route-3-dev

RUN python3 -m pip install --upgrade pip
RUN pip install ninja cmake==3.31 setuptools wheel
RUN pip install uv tabulate
RUN pip install ipython pytest fire pydantic pybind11

RUN pip uninstall -y torch torchvision triton

RUN apt --fix-broken install -y
RUN apt install -y libzstd-dev
RUN apt install -y libibverbs-dev

ENV LLVM_SYMBOLIZER_PATH=/opt/rocm/llvm/bin/llvm-symbolizer
ENV PATH=$PATH:/opt/rocm/bin:
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib/:

ENV PYTORCH_ROCM_ARCH=gfx90a
ARG MAX_JOBS=256

# update triton to 3.3.0
#RUN pip uninstall -y triton

# aotirton 0.9.2
ENV AOTRITON_TARGET_ARCH=gfx90a
RUN wget https://github.com/ROCm/aotriton/releases/download/0.9.2b/aotriton-0.9.2b-manylinux_2_28_x86_64-rocm6.3-shared.tar.gz \
    && tar xvf aotriton-0.9.2b-manylinux_2_28_x86_64-rocm6.3-shared.tar.gz \
    && rm -rf /opt/rocm/aotriton \
    && mv aotriton /opt/rocm  \
    && rm -f aotriton-0.9.2b-manylinux_2_28_x86_64-rocm6.3-shared.tar.gz

# latest hipBLASLt
# Merged in Jan 24 2025
ARG HIPBLASLT_BRANCH="258a2162"

RUN git clone https://github.com/rocm/hipblaslt \
    && cd hipblaslt \
    && git checkout ${HIPBLASLT_BRANCH} \
    && rm -fr /opt/rocm/include/hipblaslt \
    && rm -fr /opt/rocm/lib/libhipblaslt* \
    && ./install.sh -i --architecture ${PYTORCH_ROCM_ARCH} \
    && cd ../ && rm -fr hipblaslt

ENV HIP_FORCE_DEV_KERNARG=1

RUN pip install triton==3.2.0
# pytorch v2.7.0 dev
#ARG PYTORCH_BRANCH="f42cff4"
ARG PYTORCH_BRANCH="6374332"
RUN rm -fr pytorch \
    && git clone https://github.com/pytorch/pytorch \
    && cd pytorch \
    && git checkout ${PYTORCH_BRANCH} \
    && git submodule update --recursive --init \
    && ./tools/amd_build/build_amd.py \
    && BUILD_TEST=0 python3 setup.py install \
    && cd .. && rm -fr pytorch

# vision
RUN rm -rf vision && git clone https://github.com/pytorch/vision \
    && cd vision \
    && python setup.py install \
    && cd ../ && rm -fr vision \
    && cp /opt/conda/lib/libjpeg.so.9* /lib/x86_64-linux-gnu/

# APEX v1.6.0
RUN pip uninstall -y apex \
    && git clone https://github.com/rocm/apex -b release/1.6.0 \
    && cd apex \
    && python setup.py install \
    && cd .. && rm -r apex

# FA v3.0.0.r1
ENV GPU_ARCHS="gfx90a"
RUN git clone --recursive https://github.com/ROCm/flash-attention.git -b v3.0.0.r1-cktile \
    && cd flash-attention \
    && MAX_JOBS=${MAX_JOBS} python setup.py install \
    && cd .. \
    && rm -rf flash-attention


# TransformerEngine latest
ENV NVTE_USE_HIPBLASLT=1
ENV NVTE_FRAMEWORK=pytorch
ENV NVTE_ROCM_ARCH=${PYTORCH_ROCM_ARCH}
ENV NVTE_USE_CAST_TRANSPOSE_TRITON=0
ENV NVTE_CK_USES_BWD_V3=0
ENV GPU_TARGETS=gfx90a
ENV TARGET_GPUS=MI250X
ENV NVTE_AOTRITON_PATH=/opt/rocm/aotriton
#ENV NVTE_FUSED_ATTN_CK=0
ENV NVTE_FUSED_ATTN=0

RUN git clone --recursive https://github.com/ROCm/TransformerEngine.git \
    && cd TransformerEngine \
    && git submodule update --init --recursive \
    && MAX_JOBS=${MAX_JOBS} pip install . \
    && cd ..

RUN apt --fix-broken install -y
RUN pip install datasets numpy==1.26.4 transformers
RUN pip install --upgrade 'optree>=0.13.0'

WORKDIR /workspace/

RUN git clone https://github.com/ROCm/FluxBenchmark.git
RUN git clone https://github.com/ROCm/torchtitan.git

#torchtune
RUN git clone https://github.com/AMD-AIG-AIMA/torchtune.git \
    && cd torchtune \
    && pip install -e . && pip install numpy==1.26.4 \
    && pip install torchao --index-url https://download.pytorch.org/whl/nightly/rocm6.3 \
    && cd ..

RUN cp /opt/conda/lib/libjpeg.so.9* /lib/x86_64-linux-gnu/
RUN pip install --upgrade sympy

RUN pip install accelerate==1.2.1
RUN pip install peft
RUN pip install trl==0.12.2
RUN pip install deepspeed

# Setup environment variables
ENV WORKSPACE_DIR=/workspace

# Install Python dependencies
RUN pip3 install --upgrade pip \
    && pip3 install \
    scipy \
    einops \
    flask-restful \
    nltk \
    pytest \
    pytest-cov \
    pytest_mock \
    pytest-csv \
    pytest-random-order \
    sentencepiece \
    wrapt \
    zarr \
    wandb \
    tensorstore==0.1.45 \
    pybind11 \
    setuptools==69.5.1 \
    datasets \
    tiktoken \
    pynvml \
    pulp

RUN pip3 install "huggingface_hub[cli]"

# Download NLTK data
RUN python3 -m nltk.downloader punkt_tab

RUN pip uninstall triton -y
RUN pip install triton==3.2.0
CMD ["/usr/bin/bash"]
 
```

The architecture in each build step above is for `gfx90a`, corresponding directly to the MI200-series GPUs and should support your MI250X environment. Please let me know if there are any issues with this.

Thanks for your patience!

---

### 评论 #4 — alexchen5 (2025-11-12T02:19:38Z)

Hi @lucbruni-amd,

I'm unable to build the image (using MacOS) and the Setonix support team has advised me that they generally "do not provide support for custom-built user containers, as these builds are executed outside Setonix". Therefore if possible - it would be great if your team could release+document Megatron-LM images with broader GPU support - I'm sure this would also be much appreciated by the AMD community. 

Otherwise, I am also working with the Setonix support team to include additional software packages (triton, flash-attn, transformer-engine) to their provided base container images for PyTorch for ROCm - so I should be able to install Megatron-LM that way. 

---

### 评论 #5 — lucbruni-amd (2025-11-12T16:31:22Z)

Thanks for letting me know. I will get in touch with the Primus team to answer your questions as we will be moving forward with `rocm/primus` images in favour of the old Megatron-LM images, but I'm not sure as far as plans for hardware support goes.

Let me know if there are any issues setting up the additional packages.

---

### 评论 #6 — lucbruni-amd (2025-11-27T17:05:18Z)

I have received word that support for these images in particular with broader (mainly older) GPU support will be a limited effort and not a priority of the team in the foreseeable future. I will close this issue due to this, and as `Megatron-LM`/`primus` image support is documented.

For installing Megatron-LM and its dependencies on baremetal - if you encounter any issues, please feel free to open new issues in their respective repositories, and we'll be happy to help out.

Apologies for the inconvenience.

---
