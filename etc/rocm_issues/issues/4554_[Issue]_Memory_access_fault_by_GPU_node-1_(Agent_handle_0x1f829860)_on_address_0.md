# [Issue]: Memory access fault by GPU node-1 (Agent handle: 0x1f829860) on address 0x7a8a4be00000. Reason: Page not present or supervisor privilege. Aborted (core dumped)

> **Issue #4554**
> **状态**: closed
> **创建时间**: 2025-04-01T23:48:56Z
> **更新时间**: 2025-06-06T16:15:48Z
> **关闭时间**: 2025-06-06T16:15:47Z
> **作者**: CrazyCows
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4554

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Gpu crashes when using torch-vision and both training and evaluating on gpu. If training on gpu and evaluating on cpu, it seems ok. Mixed precision not working at all 

Attempted with both the docker image rocm/pytorch:latest and with a local installation with nightly torch build. Both fails.

Tested and working on nvidia & mac.


### Operating System

OS: NAME="Ubuntu" VERSION="22.04.5 LTS (Jammy Jellyfish)"

### CPU

CPU:  model name      : AMD Ryzen 7 9700X 8-Core Processor

### GPU

  Name:                    gfx1100                               Marketing Name:          Radeon RX 7900 XTX                        Name:                    amdgcn-amd-amdhsa--gfx1100   

### ROCm Version

6.3.3

### ROCm Component

_No response_

### Steps to Reproduce

Find some images and run script, crashes after ~1500 steps, or 11 batches. 

`
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from ..paths import LOCAL_DATA_DIR
from ..data import data_utils
import os
from tqdm import tqdm
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)

        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3,
                               stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.conv3 = nn.Conv2d(out_channels, out_channels * self.expansion,
                               kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels * self.expansion)

        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample

    def forward(self, x):
        identity = x

        out = self.relu(self.bn1(self.conv1(x)))
        out = self.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)
        return out


class ResNet50(nn.Module):
    def __init__(self, num_classes=1000):
        super(ResNet50, self).__init__()
        self.in_channels = 64

        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1   = nn.BatchNorm2d(64)
        self.relu  = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(Bottleneck, 64, 3)
        self.layer2 = self._make_layer(Bottleneck, 128, 4, stride=2)
        self.layer3 = self._make_layer(Bottleneck, 256, 6, stride=2)
        self.layer4 = self._make_layer(Bottleneck, 512, 3, stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * Bottleneck.expansion, num_classes)

    def _make_layer(self, block, out_channels, blocks, stride=1):
        downsample = None
        if stride != 1 or self.in_channels != out_channels * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.in_channels, out_channels * block.expansion,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels * block.expansion),
            )

        layers = [block(self.in_channels, out_channels, stride, downsample)]
        self.in_channels = out_channels * block.expansion

        for _ in range(1, blocks):
            layers.append(block(self.in_channels, out_channels))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)

        return x

class DatasetResnet(Dataset):
    def __init__(self, paths, labels, user_path, transform) -> None:
        self.paths = paths
        self.labels = labels
        self.transform = transform
        self.user_path = user_path
    
    def __len__(self) -> int:
        return len(self.paths)
    
    def __getitem__(self, idx) -> tuple[torch.tensor, torch.tensor]:
        image = Image.open(self.user_path / self.paths[idx]).resize((224, 224))
        image =  self.transform(image)

        return image, self.labels[idx]
    

class Trainer():
    def __init__(self):
        self.criterion = CrossEntropyLoss()

    def trainer(self, model: nn.Module, train_loader, val_loader, num_epochs=200, weight_decay=0.01):
        self.optimizer = AdamW(model.parameters(), weight_decay=weight_decay)
        for epoch in tqdm(range(num_epochs), desc="Training Epochs"):
            model.train()
            for images, labels in tqdm(train_loader, desc="Training steps", total=len(train_loader)):
                images = images.to(device)
                labels = labels.to(device)
                self.optimizer.zero_grad()
                outputs = model(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

                
            # Validation step
            model.eval()
            with torch.no_grad():
                correct = 0
                total = 0
                for images, labels in val_loader:
                    images = images.to(device)
                    labels = labels.to(device)
                    outputs = model(images)
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()

            print(f'Epoch [{epoch+1}/{num_epochs}], Accuracy: {100 * correct / total:.2f}%')

def create_label_dict(train_label, test_label, val_label):
    label_dict = {}
    for i, label in enumerate(train_label):
        label_dict[label] = i
    
    for i, label in enumerate(test_label):
        if label not in label_dict:
            label_dict[label] = len(label_dict)

    for i, label in enumerate(val_label):
        if label not in label_dict:
            label_dict[label] = len(label_dict)

    return label_dict

def test():
    transform = transforms.ToTensor()
    train_paths, test_paths, val_paths, train_label, test_label, val_label = data_utils.get_data_set(LOCAL_DATA_DIR / "test")
    
    label_dict = create_label_dict(train_label, test_label, val_label)

    train_label = [label_dict[label] for label in train_label]
    test_label = [label_dict[label] for label in test_label]
    val_label = [label_dict[label] for label in val_label]

    train_label = [torch.tensor(label) for label in train_label]
    test_label = [torch.tensor(label) for label in test_label]
    val_label = [torch.tensor(label) for label in val_label]


    train_dataset = DatasetResnet(train_paths, train_label, LOCAL_DATA_DIR / "test", transform)
    test_dataset = DatasetResnet(test_paths, test_label, LOCAL_DATA_DIR / "test", transform)
    val_dataset = DatasetResnet(val_paths, val_label, LOCAL_DATA_DIR / "test", transform)
    
    
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, pin_memory=True)
    

    trainer = Trainer()

    model = ResNet50(num_classes=len(label_dict)).to(device)
    trainer.trainer(model, train_loader, val_loader, num_epochs=2000)
    
    

if __name__ == "__main__":
    test()
`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.10.5 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.14
Runtime Ext Version:     1.6
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 7 9700X 8-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 9700X 8-Core Processor 
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
  Max Clock Freq. (MHz):   5581                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    31992260(0x1e829c4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    31992260(0x1e829c4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    31992260(0x1e829c4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31992260(0x1e829c4) KB             
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
  Uuid:                    GPU-6aa7a6894c7ed8bd               
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
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2431                               
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
  Packet Processor uCode:: 412                                
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
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 21                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    15996128(0xf414e0) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    15996128(0xf414e0) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    15996128(0xf414e0) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
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
*** Done ***             

### Additional Information

(py_3.10) root@ddfdfd480bf6:/workspace# python3 -m app.models.resnet
Training steps: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:05<00:00, 28.49it/s]
Epoch [1/2000], Accuracy: 0.00%███████████████████████████████████████████████████████████████████████████████████████████████▊  | 148/151 [00:05<00:00, 30.99it/s]
Training steps: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:04<00:00, 30.28it/s]
Epoch [2/2000], Accuracy: 0.00%█████████████████████████████████████████████████████████████████████████████████████████████████▎| 150/151 [00:04<00:00, 30.13it/s]
Training steps: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:04<00:00, 30.32it/s]
Epoch [3/2000], Accuracy: 0.00%█████████████████████████████████████████████████████████████████████████████████████████████████▎| 150/151 [00:04<00:00, 30.74it/s]
Training steps: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:04<00:00, 30.40it/s]
Epoch [4/2000], Accuracy: 0.00%███████████████████████████████████████████████████████████████████████████████████████████████▊  | 148/151 [00:04<00:00, 30.44it/s]
Training steps: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:05<00:00, 29.91it/s]
Epoch [5/2000], Accuracy: 0.00%█████████████████████████████████████████████████████████████████████████████████████████████████▎| 150/151 [00:05<00:00, 29.61it/s]
Training steps: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:05<00:00, 30.07it/s]
Epoch [6/2000], Accuracy: 0.00%██████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:05<00:00, 30.36it/s]
Training steps: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:05<00:00, 29.90it/s]
Epoch [7/2000], Accuracy: 0.00%███████████████████████████████████████████████████████████████████████████████████████████████▊  | 148/151 [00:04<00:00, 30.38it/s]
Training steps: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:05<00:00, 30.07it/s]
Epoch [8/2000], Accuracy: 0.00%███████████████████████████████████████████████████████████████████████████████████████████████▊  | 148/151 [00:04<00:00, 30.62it/s]
Training steps: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:05<00:00, 30.05it/s]
Epoch [9/2000], Accuracy: 0.00%████████████████████████████████████████████████████████████████████████████████████████████████▌ | 149/151 [00:04<00:00, 30.46it/s]
Training steps: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:05<00:00, 29.77it/s]
Epoch [10/2000], Accuracy: 0.00%███████████████████████████████████████████████████████████████████████████████████████████████▌ | 149/151 [00:05<00:00, 29.32it/s]
Training steps: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:05<00:00, 30.00it/s]
Epoch [11/2000], Accuracy: 0.00%█████████████████████████████████████████████████████████████████████████████████████████████████| 151/151 [00:05<00:00, 30.87it/s]
Training Epochs:   1%|▌                                                                                                        | 11/2000 [00:57<2:54:28,  5.26s/itMemory access fault by GPU node-1 (Agent handle: 0x380a6dd0) on address 0x77f7e7600000. Reason: Page not present or supervisor privilege.51 [00:04<00:00, 30.92it/s]
Aborted (core dumped)

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-04-02T14:30:23Z)

Hi @CrazyCows. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2025-05-02T19:41:58Z)

Hi @CrazyCows, sorry for the delay on this, I'll take a look. I notice you have integrated graphics enabled (the gfx1036 device in your rocminfo output) which can cause issues as described [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#disable-integrated-graphics-igp-if-applicable); can you disable your integrated graphics and  see if that helps?

---

### 评论 #3 — schung-amd (2025-06-06T16:15:47Z)

Closing for now due to lack of response. Feel free to comment if you are still having this issue and have tried disabling integrated graphics and we can reopen. Will also need some clarification on your reproducer, it is not clear what 
```
from ..paths import LOCAL_DATA_DIR
from ..data import data_utils
```
is meant to import.

---
