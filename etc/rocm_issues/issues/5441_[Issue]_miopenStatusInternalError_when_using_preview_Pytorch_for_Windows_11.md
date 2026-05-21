# [Issue]: miopenStatusInternalError when using preview Pytorch for Windows 11

> **Issue #5441**
> **状态**: closed
> **创建时间**: 2025-09-28T14:45:44Z
> **更新时间**: 2025-11-27T19:09:19Z
> **关闭时间**: 2025-11-27T19:09:19Z
> **作者**: skillmaker-dev
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5441

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

I installed Pytorch successfully, and the devices are successfully found by torch. cuda:0 returns the iGPU, cuda:1 returns RX 9070XT
The issues arises when trying to do some training using pytorch, here is the code that triggers the issue:

```py
# Model definition using transfer learning
def build_model(num_classes: int) -> nn.Module:
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
    for param in model.parameters():
        param.requires_grad = False
    for param in model.layer4.parameters():
        param.requires_grad = True
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, 256),
        nn.BatchNorm1d(256),
        nn.ReLU(inplace=True),
        nn.Dropout(0.4),
        nn.Linear(256, num_classes)
    )
    return model.to(DEVICE)
def get_class_weights(dataset: datasets.ImageFolder) -> torch.Tensor:
    counts = np.zeros(len(dataset.classes), dtype=np.float32)
    for _, label in dataset.samples:
        counts[label] += 1
    weights = 1.0 / (counts + 1e-6)
    weights = weights / weights.sum() * len(dataset.classes)
    return torch.tensor(weights, dtype=torch.float32, device=DEVICE)
if train_dataset is not None:
    model = build_model(len(CLASS_NAMES))
    class_weights = get_class_weights(train_dataset)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=LABEL_SMOOTHING)
    optimizer = optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.3, patience=2)
    metric_accuracy = torchmetrics.Accuracy(task="multiclass", num_classes=len(CLASS_NAMES)).to(DEVICE)
else:
    model = None
    criterion = None
    optimizer = None
    scheduler = None
    metric_accuracy = None
```

```py
# Training and evaluation helpers
def train_one_epoch(model, loader, criterion, optimizer, metric):
    model.train()
    running_loss = 0.0
    metric.reset()
    for inputs, labels in loader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * inputs.size(0)
        metric.update(outputs.softmax(dim=1), labels)
    epoch_loss = running_loss / len(loader.dataset)
    epoch_acc = metric.compute().item()
    return epoch_loss, epoch_acc
@torch.no_grad()
def evaluate(model, loader, criterion, metric):
    model.eval()
    running_loss = 0.0
    metric.reset()
    for inputs, labels in loader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        running_loss += loss.item() * inputs.size(0)
        metric.update(outputs.softmax(dim=1), labels)
    epoch_loss = running_loss / len(loader.dataset)
    epoch_acc = metric.compute().item()
    return epoch_loss, epoch_acc
def train_model(model, criterion, optimizer, scheduler, num_epochs=EPOCHS):
    history = {"train_loss": [], "valid_loss": [], "train_acc": [], "valid_acc": []}
    best_model_wts = None
    best_loss = float('inf')
    patience_counter = 0
    for epoch in range(num_epochs):
        print(f"Epoch {epoch + 1}/{num_epochs}")
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, metric_accuracy)
        if valid_loader is not None:
            val_loss, val_acc = evaluate(model, valid_loader, criterion, metric_accuracy)
            scheduler.step(val_loss)
        else:
            val_loss, val_acc = float('nan'), float('nan')
        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["valid_loss"].append(val_loss)
        history["valid_acc"].append(val_acc)
        print(f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f}")
        print(f"Valid Loss: {val_loss:.4f} Acc: {val_acc:.4f}")
        if val_loss < best_loss:
            best_loss = val_loss
            patience_counter = 0
            best_model_wts = model.state_dict()
            torch.save(best_model_wts, MODEL_DIR / "best_model.pt")
            print("→ Saved new best model")
        else:
            patience_counter += 1
            if patience_counter >= PATIENCE:
                print("Early stopping triggered")
                break
    if best_model_wts is not None:
        model.load_state_dict(best_model_wts)
    return model, history
if model is not None and train_loader is not None:
    model, history = train_model(model, criterion, optimizer, scheduler, num_epochs=EPOCHS)
else:
    history = None
    print("Training skipped because dataset is missing.")
```

running the second cell returns this error:
```py
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
Cell In[13], [line 66](vscode-notebook-cell:?execution_count=13&line=66)
     64     return model, history
     65 if model is not None and train_loader is not None:
---> [66](vscode-notebook-cell:?execution_count=13&line=66)     model, history = train_model(model, criterion, optimizer, scheduler, num_epochs=EPOCHS)
     67 else:
     68     history = None

Cell In[13], [line 39](vscode-notebook-cell:?execution_count=13&line=39)
     37 for epoch in range(num_epochs):
     38     print(f"Epoch {epoch + 1}/{num_epochs}")
---> [39](vscode-notebook-cell:?execution_count=13&line=39)     train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, metric_accuracy)
     40     if valid_loader is not None:
     41         val_loss, val_acc = evaluate(model, valid_loader, criterion, metric_accuracy)

Cell In[13], [line 9](vscode-notebook-cell:?execution_count=13&line=9)
      7 inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
      8 optimizer.zero_grad()
----> [9](vscode-notebook-cell:?execution_count=13&line=9) outputs = model(inputs)
     10 loss = criterion(outputs, labels)
     11 loss.backward()

File c:\Users\Anas\Projects\AI\Image Classification\ImageClassification\Lib\site-packages\torch\nn\modules\module.py:1773, in Module._wrapped_call_impl(self, *args, **kwargs)
   1771     return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]
   1772 else:
-> [1773](file:///C:/Users/Anas/Projects/AI/Image%20Classification/ImageClassification/Lib/site-packages/torch/nn/modules/module.py:1773)     return self._call_impl(*args, **kwargs)

File c:\Users\Anas\Projects\AI\Image Classification\ImageClassification\Lib\site-packages\torch\nn\modules\module.py:1784, in Module._call_impl(self, *args, **kwargs)
   1779 # If we don't have any hooks, we want to skip the rest of the logic in
   1780 # this function, and just call forward.
   1781 if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks
   1782         or _global_backward_pre_hooks or _global_backward_hooks
   1783         or _global_forward_hooks or _global_forward_pre_hooks):
-> [1784](file:///C:/Users/Anas/Projects/AI/Image%20Classification/ImageClassification/Lib/site-packages/torch/nn/modules/module.py:1784)     return forward_call(*args, **kwargs)
   1786 result = None
   1787 called_always_called_hooks = set()

File c:\Users\Anas\Projects\AI\Image Classification\ImageClassification\Lib\site-packages\torchvision\models\resnet.py:285, in ResNet.forward(self, x)
    284 def forward(self, x: Tensor) -> Tensor:
--> [285](file:///C:/Users/Anas/Projects/AI/Image%20Classification/ImageClassification/Lib/site-packages/torchvision/models/resnet.py:285)     return self._forward_impl(x)

File c:\Users\Anas\Projects\AI\Image Classification\ImageClassification\Lib\site-packages\torchvision\models\resnet.py:269, in ResNet._forward_impl(self, x)
    266 def _forward_impl(self, x: Tensor) -> Tensor:
    267     # See note [TorchScript super()]
    268     x = self.conv1(x)
--> [269](file:///C:/Users/Anas/Projects/AI/Image%20Classification/ImageClassification/Lib/site-packages/torchvision/models/resnet.py:269)     x = self.bn1(x)
    270     x = self.relu(x)
    271     x = self.maxpool(x)

File c:\Users\Anas\Projects\AI\Image Classification\ImageClassification\Lib\site-packages\torch\nn\modules\module.py:1773, in Module._wrapped_call_impl(self, *args, **kwargs)
   1771     return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]
   1772 else:
-> [1773](file:///C:/Users/Anas/Projects/AI/Image%20Classification/ImageClassification/Lib/site-packages/torch/nn/modules/module.py:1773)     return self._call_impl(*args, **kwargs)

File c:\Users\Anas\Projects\AI\Image Classification\ImageClassification\Lib\site-packages\torch\nn\modules\module.py:1784, in Module._call_impl(self, *args, **kwargs)
   1779 # If we don't have any hooks, we want to skip the rest of the logic in
   1780 # this function, and just call forward.
   1781 if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks
   1782         or _global_backward_pre_hooks or _global_backward_hooks
   1783         or _global_forward_hooks or _global_forward_pre_hooks):
-> [1784](file:///C:/Users/Anas/Projects/AI/Image%20Classification/ImageClassification/Lib/site-packages/torch/nn/modules/module.py:1784)     return forward_call(*args, **kwargs)
   1786 result = None
   1787 called_always_called_hooks = set()

File c:\Users\Anas\Projects\AI\Image Classification\ImageClassification\Lib\site-packages\torch\nn\modules\batchnorm.py:193, in _BatchNorm.forward(self, input)
    186     bn_training = (self.running_mean is None) and (self.running_var is None)
    188 r"""
    189 Buffers are only updated if they are to be tracked and we are in training mode. Thus they only need to be
    190 passed when the update should occur (i.e. in training mode when they are tracked), or when buffer stats are
    191 used for normalization (i.e. in eval mode when buffers are not None).
    192 """
--> [193](file:///C:/Users/Anas/Projects/AI/Image%20Classification/ImageClassification/Lib/site-packages/torch/nn/modules/batchnorm.py:193) return F.batch_norm(
    194     input,
    195     # If buffers are not to be tracked, ensure that they won't be updated
    196     self.running_mean
    197     if not self.training or self.track_running_stats
    198     else None,
    199     self.running_var if not self.training or self.track_running_stats else None,
    200     self.weight,
    201     self.bias,
    202     bn_training,
    203     exponential_average_factor,
    204     self.eps,
    205 )

File c:\Users\Anas\Projects\AI\Image Classification\ImageClassification\Lib\site-packages\torch\nn\functional.py:2817, in batch_norm(input, running_mean, running_var, weight, bias, training, momentum, eps)
   2814 if training:
   2815     _verify_batch_size(input.size())
-> [2817](file:///C:/Users/Anas/Projects/AI/Image%20Classification/ImageClassification/Lib/site-packages/torch/nn/functional.py:2817) return torch.batch_norm(
   2818     input,
   2819     weight,
   2820     bias,
   2821     running_mean,
   2822     running_var,
   2823     training,
   2824     momentum,
   2825     eps,
   2826     torch.backends.cudnn.enabled,
   2827 )

RuntimeError: miopenStatusInternalError
```

Running `py -m torch.utils.collect_env` returns the iGPU info, I had to set `$env:HIP_VISIBLE_DEVICES=1` and then it returns the dGPU info:
```
PyTorch version: 2.8.0a0+gitfc14c65
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 6.4.50101-9a6572ae7

OS: Microsoft Windows 11 Pro (10.0.26100 64-bit)
GCC version: Could not collect
Clang version: Could not collect
CMake version: Could not collect
Libc version: N/A

Python version: 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)] (64-bit runtime)
Python platform: Windows-11-10.0.26100-SP0
Is CUDA available: True
CUDA runtime version: Could not collect
CUDA_MODULE_LOADING set to: LAZY
GPU models and configuration: AMD Radeon RX 9070 XT (gfx1201)
Nvidia driver version: Could not collect
cuDNN version: Could not collect
HIP runtime version: 6.4.50101
MIOpen runtime version: 3.4.1
Is XNNPACK available: False

CPU:
Name: AMD Ryzen 5 9600X 6-Core Processor
Manufacturer: AuthenticAMD
Family: 107
Architecture: 9
ProcessorType: 3
DeviceID: CPU0
CurrentClockSpeed: 3866
MaxClockSpeed: 3900
L2CacheSize: 6144
L2CacheSpeed: None
Revision: 17408

Versions of relevant libraries:
[pip3] numpy==1.26.4
[pip3] torch==2.8.0a0+gitfc14c65
[pip3] torchaudio==2.6.0a0+1a8f621
[pip3] torchmetrics==1.4.0
[pip3] torchvision==0.24.0a0+c85f008
[conda] Could not collect
```
I couldn't find a way to run `rocminfo` as I don't know where the installation path for ROCm 6.4.4 is.

Is there something I'm missing?

### Operating System

10.0.26100

### CPU

AMD Ryzen 5 9600X 6-Core Processor

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

6.4.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Here are the MIOpen logs:
```
C:\Users\Anas\Projects\AI\Image Classification\ImageClassification\Lib\site-packages\torch\utils\data\_utils\pin_memory.py:21: UserWarning: Cannot set number of intraop threads after parallel work has started or after set_num_threads call when using native parallel backend (Triggered internally at C:\develop\pytorch-test\aten\src\ATen\ParallelNative.cpp:231.)
  torch.set_num_threads(1)
MIOpen(HIP): Info [get_device_name] Raw device name: gfx1201
MIOpen(HIP): Info [Handle] stream: 0000000000000000, device_id: 0
MIOpen(HIP): Info [get_device_name] Raw device name: gfx1201
MIOpen(HIP): Info [SetStream] stream: 0000000000000000, device_id: 0
MIOpen(HIP): Info [] MIOPEN_FIND_MODE = DYNAMIC_HYBRID(5)
MIOpen(HIP): Info [AmdRocmMetadataVersionDetect] ROCm MD version AMDHSA_COv3, HIP version 6.4.50101, MIOpen version 3.4.1.76e3cde91
MIOpen(HIP): Info2 [GetWorkSpaceSize]
MIOpen(HIP): Info [GetSolutions]
MIOpen(HIP): Info2 [GetInstalledPathFile] inexact find database search
MIOpen(HIP): Info [GetInstalledPathFile] Database directory does not exist
MIOpen(HIP): Info [Measure] ReadonlyRamDb::Prefetch time: 0.0014 ms
MIOpen(HIP): Info [Measure] RamDb::Prefetch time: 0.2424 ms
MIOpen(HIP): Info2 [ValidateUnsafe] DB file is newer than cache: 10811935574800, 6419093615000
MIOpen(HIP): Info2 [FindRecord] RamDb file is newer than cache, prefetching
MIOpen(HIP): Info [Measure] RamDb::Prefetch time: 0.051 ms
MIOpen(HIP): Info2 [FindRecordUnsafe] Looking for key 3-224-224-7x7-64-112-112-16-3x3-2x2-1x1-0-NCHW-FP32-F in cache for file "C:\\Users\\Anas\\.miopen\\db\\gfx1201_32.HIP.3_4_1_76e3cde91.ufdb.txt"
MIOpen(HIP): Info2 [Measure] Db::FindRecord time: 0.4181 ms
MIOpen(HIP): Info2 [GetSolutions] id: 91, algo: 0, time: 3.13128, ws: 7375872, name: GemmFwdRest
MIOpen(HIP): Info [GetWorkSpaceSize] 7375872
MIOpen(HIP): Info [FindConvFwdAlgorithm] requestAlgoCount = 1, workspace = 7375872
MIOpen(HIP): Info [GetSolutions]
MIOpen(HIP): Info2 [ValidateUnsafe] DB file is newer than cache: 10811935574800, 6419094010000
MIOpen(HIP): Info2 [FindRecord] RamDb file is newer than cache, prefetching
MIOpen(HIP): Info [Measure] RamDb::Prefetch time: 0.038 ms
MIOpen(HIP): Info2 [FindRecordUnsafe] Looking for key 3-224-224-7x7-64-112-112-16-3x3-2x2-1x1-0-NCHW-FP32-F in cache for file "C:\\Users\\Anas\\.miopen\\db\\gfx1201_32.HIP.3_4_1_76e3cde91.ufdb.txt"
MIOpen(HIP): Info2 [Measure] Db::FindRecord time: 0.3593 ms
MIOpen(HIP): Info2 [GetSolutions] id: 91, algo: 0, time: 3.13128, ws: 7375872, name: GemmFwdRest
MIOpen(HIP): Info2 [GetInvoker] Returning an invoker for problem 3x224x224x7x7x64x112x112x16xNCHWxFP32x3x3x2x2x1x1x1xFxDefault and solver GemmFwdRest
MIOpen(HIP): Info [FindSolutionImpl] GemmFwdRest (not searchable)
MIOpen(HIP): Info2 [Register] Invoker registered for algorithm 3x224x224x7x7x64x112x112x16xNCHWxFP32x3x3x2x2x1x1x1xFxDefault and solver GemmFwdRest
MIOpen(HIP): Info2 [SetAsFound1_0] Solver GemmFwdRest registered as find 1.0 best for miopenConvolutionFwdAlgoGEMM in 3x224x224x7x7x64x112x112x16xNCHWxFP32x3x3x2x2x1x1x1xFxDefault
MIOpen(HIP): Info [FindConvolution] miopenConvolutionFwdAlgoGEMM        3.13128 7375872
MIOpen(HIP): Info [FillFindReturnParameters] FW Chosen Algorithm: GemmFwdRest , 7375872, 3.13128
MIOpen(HIP): Info [ConvolutionForward] algo = 0, workspace = 7375872
MIOpen(HIP): Info2 [GetInvoker] Returning an invoker for problem 3x224x224x7x7x64x112x112x16xNCHWxFP32x3x3x2x2x1x1x1xFxDefault and algorithm miopenConvolutionFwdAlgoGEMM
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [SQLiteBase] Initializing system database file ""
MIOpen(HIP): Info [KernDb] database not present
MIOpen(HIP): Info2 [SQLiteBase] Initializing user database file "C:\\Users\\Anas\\.miopen\\cache\\3.4.1.76e3cde91\\gfx1201_32.ukdb"
MIOpen(HIP): Info2 [KernDb] Database created successfully
MIOpen(HIP): Info2 [LoadBinary] Loading binary for: "MIOpenIm2d2Col.cl.obj"; args:  -DLOCAL_MEM_SIZE=1449 -DSTRIDE_GT_1=1 -DNUM_IM_BLKS_EQ_1=0 -DUSE_IM_OFF_GUARD=1 -DMIOPEN_USE_FP16=0 -DMIOPEN_USE_FP16x4=0 -DMIOPEN_USE_FP16x8=0 -DMIOPEN_USE_FP32=1 -DMIOPEN_USE_INT8=0 -DMIOPEN_USE_BFP16=0 -DMIOPEN_USE_INT32=0 -DMIOPEN_USE_RNE_BFLOAT16=1 -DMIOPEN_FP8_IEEE_EXPONENT_BIAS=0 -DMIOPEN_FP8_CLIPPING=1 -mcpu=gfx1201
MIOpen(HIP): Info2 [Prepare] SELECT kernel_blob, kernel_hash, uncompressed_size FROM kern_db WHERE (kernel_name = 'MIOpenIm2d2Col.cl.obj') AND (kernel_args = ' -DLOCAL_MEM_SIZE=1449 -DSTRIDE_GT_1=1 -DNUM_IM_BLKS_EQ_1=0 -DUSE_IM_OFF_GUARD=1 -DMIOPEN_USE_FP16=0 -DMIOPEN_USE_FP16x4=0 -DMIOPEN_USE_FP16x8=0 -DMIOPEN_USE_FP32=1 -DMIOPEN_USE_INT8=0 -DMIOPEN_USE_BFP16=0 -DMIOPEN_USE_INT32=0 -DMIOPEN_USE_RNE_BFLOAT16=1 -DMIOPEN_FP8_IEEE_EXPONENT_BIAS=0 -DMIOPEN_FP8_CLIPPING=1 -mcpu=gfx1201');
MIOpen(HIP): Info2 [Measure] Db::FindRecord time: 0.3974 ms
MIOpen(HIP): Info2 [LoadBinary] Successfully loaded binary for: "MIOpenIm2d2Col.cl.obj"; args:  -DLOCAL_MEM_SIZE=1449 -DSTRIDE_GT_1=1 -DNUM_IM_BLKS_EQ_1=0 -DUSE_IM_OFF_GUARD=1 -DMIOPEN_USE_FP16=0 -DMIOPEN_USE_FP16x4=0 -DMIOPEN_USE_FP16x8=0 -DMIOPEN_USE_FP32=1 -DMIOPEN_USE_INT8=0 -DMIOPEN_USE_BFP16=0 -DMIOPEN_USE_INT32=0 -DMIOPEN_USE_RNE_BFLOAT16=1 -DMIOPEN_FP8_IEEE_EXPONENT_BIAS=0 -DMIOPEN_FP8_CLIPPING=1 -mcpu=gfx1201
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info2 [GetKernels] 0 kernels for key: miopenIm2d2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [AddKernel] Key: miopenIm2Col "c3i224_224w7_7p3_3s2_2d1_1t1"
MIOpen(HIP): Info2 [run] kernel_name = Im2d2Col_v2, global_work_dim = { 43008, 1, 1 }, local_work_dim = { 256, 1, 1 }
MIOpen(HIP): Info2 [CallGemm] gemm_desc: {isColMajor 0, transA 0, transB 0, m 64, n 12544, k 147, lda 147, ldb 12544, ldc 12544, batch_count 1, strideA 0, strideB 0, strideC 0, alpha 1, beta 0, dataType float, a_cast_type float, b_cast_type float}
MIOpen(HIP): Info2 [CallGemm] rocBLAS
MIOpen(HIP): Info [get_device_name] Raw device name: gfx1201
MIOpen(HIP): Info [SetStream] stream: 0000000000000000, device_id: 0
MIOpen(HIP): Info2 [GetInvoker] Returning an invoker for problem 64x1x112x112x16xNCHWxNCHWxFP32xFP32xFP32xFP32xFP32xFP32x0xTrnx1x1x1x0 and algorithm miopenBatchNormForwardTrainingSpatial
MIOpen(HIP): Info2 [GetFound1_0] No invokers found for 64x1x112x112x16xNCHWxNCHWxFP32xFP32xFP32xFP32xFP32xFP32x0xTrnx1x1x1x0
MIOpen(HIP): Info [FindSolutionImpl] BnFwdTrainingSpatial
MIOpen(HIP): Info2 [GetPerfDbPathFile] inexact perf database search
MIOpen(HIP): Info [GetPerfDbPathFile] Database directory does not exist
MIOpen(HIP): Info2 [SQLiteBase] Initializing system database file ""
MIOpen(HIP): Info [SQLitePerfDb] database not present
MIOpen(HIP): Info2 [SQLiteBase] Initializing user database file "C:\\Users\\Anas\\.miopen\\db\\batchnorm_gfx1201_32_1.1.0.udb"
MIOpen(HIP): Info2 [Prepare] SELECT solver, params FROM perf_db INNER JOIN config ON perf_db.config = config.id WHERE ( (layout = ? ) AND (direction = ? ) AND (data_type = ? ) AND (mode = ? ) AND (spatial_dim = ? ) AND (batchsize = ? ) AND (in_channels = ? ) AND (in_h = ? ) AND (in_w = ? ) AND (in_d = ? ) AND (resultsave = ? ) AND (resultrunning = ? ) AND (useSaved = ? ) );
MIOpen Error: C:\develop\MIOpen\src\sqlite_db.cpp:298: SQLite prepare error: Internal error while accessing SQLite database: no such column: mode
```

```
MIOpen Error: C:\develop\MIOpen\src\sqlite_db.cpp:298: SQLite prepare error: Internal error while accessing SQLite database: no such column: mode
```

This error happens even after deleting the MIOpen cache and trying again.

---

## 评论 (9 条)

### 评论 #1 — eziohuang251-code (2025-09-29T16:15:04Z)

same issue

---

### 评论 #2 — skillmaker-dev (2025-09-30T19:07:41Z)

@harkgill-amd I used the wheels from TheRock, Pytorch + ROCm 7, and I no longer have issues with Pytorch so far.

---

### 评论 #3 — skillmaker-dev (2025-09-30T19:10:44Z)

> same issue

@eziohuang251-code You can follow these steps (you can skip the ComfyUI ones) in the following guide, it worked for me, you only need to run this in a venv or globally as you wish: `python -m pip install --index-url https://d2awnip2yjpvqn.cloudfront.net/v2/gfx120X-all/ torch torchvision torchaudio` I guess the Visual studio step is necessary, I already had Visual Studio installed so I'm not sure.

https://www.reddit.com/r/ROCm/comments/1n1jwh3/installation_guide_windows_11_rocm_7_rc_with/

---

### 评论 #4 — harkgill-amd (2025-09-30T21:23:07Z)

@skillmaker-dev, I was able to reproduce the miopenStatusInternalError when calling `BatchNorm2d`/`BatchNorm1d` and we're tracking this internally. Unfortunately, for now this usecase falls under the Known Issues/Limitations for 6.4.4 as training is not supported in the preview release https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/limitations/limitationsrad.html#limitations. This page will be updated to call out batch normalization specifically and we hope to resolve the issues surrounding this in a future Windows release.

For now, please continue to use the latest TheRock wheels for gfx1200.



---

### 评论 #5 — KrisBigK (2025-10-20T06:45:31Z)

> I was able to reproduce the miopenStatusInternalError when calling BatchNorm2d/BatchNorm1d

I have a gfx1151 device, encountered a similar issue when I called `torch.nn.BatchNorm2d`, thought that it was a MIOpen issue before discovering the conversation here, and made an issue report in the rocm-libraries repo https://github.com/ROCm/rocm-libraries/issues/2169 . My error was a compilation error in the assembly language though.

> training is not supported in the preview release https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/limitations/limitationsrad.html#limitations

According to the documentation, "No backward pass support" is mentioned only for the Windows platform. However `torch.nn.BatchNorm2d` failed on Ubuntu too based on my testing. (more details in my issue report) 

---

### 评论 #6 — harkgill-amd (2025-11-26T21:44:06Z)

@skillmaker-dev, this should be resolved in the latest Pytorch on Windows 7.1.1 release - could you give this a try?

https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/windows/install-pytorch.html#pytorch-via-pip-installation

---

### 评论 #7 — skillmaker-dev (2025-11-26T21:57:45Z)

@harkgill-amd Thanks, I'll check it after installing the driver

---

### 评论 #8 — skillmaker-dev (2025-11-27T18:52:21Z)

@harkgill-amd I tried the batch normalization and it's working now, thanks!

---

### 评论 #9 — harkgill-amd (2025-11-27T19:09:19Z)

Glad to hear it's working now, will close this issue out.

---
