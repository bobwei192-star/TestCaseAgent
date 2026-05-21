# Sending data to device in Pytorch causes it to contain nan values

> **Issue #2055**
> **状态**: closed
> **创建时间**: 2023-04-16T17:53:42Z
> **更新时间**: 2024-05-10T19:02:38Z
> **关闭时间**: 2024-05-10T19:02:38Z
> **作者**: Dunedin87
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2055

## 描述

Pytorch Version 2.0 ROCm version 5.4.2 on Linux Mint 20.3 (Ubuntu 20.04)

Initiating checking for cuda device results in the following warning.
`/home/sm/.local/lib/python3.8/site-packages/torch/cuda/__init__.py:546: UserWarning: Can't initialize NVML
  warnings.warn("Can't initialize NVML")` 

`torch.cuda.is_available()` comes out as `True`

`print(torch.cuda.get_device_name(device=device))` shows simply AMD Radeon Graphics instead of AMD 6950XT.

Onto to the problem, my loss and model outputs were showing nan, puzzled I went back and checked the data for nan, which also showed it to be True. This was odd as I had previously run the code on Kaggle notebooks, which didn't show it to be a problem. I then decided to test it with random data and the data was still showing it containing nan. I then checked it before sending it `.to(device)` and after, and as expected initial data did not contain nan values but after `.to(device)` it did. Following is the code for testing.

    device = torch.device("cuda" if (torch.cuda.is_available()) else "cpu")
    model = ENet(3,2)
    model.to(device)
    criterion = nn.BCELoss()
    opt = torch.optim.Adam(model.parameters(), lr = 1e-4)

    for i in range(10):

      data = torch.rand(3,3,512,512).float()
      print('Initial Data nan', torch.any(torch.isnan(data)))
      labels =torch.randint(low = 0, high = 2, size = (3,2)).float()
      data = data.to(device)
      print('Device Data nan',torch.any(torch.isnan(data)))
      labels = labels.to(device)

      output = model(data)
      loss = criterion(output, labels)
      loss.backward()
      opt.step()
      opt.zero_grad()

The output for the first loop is 

    Initial Data nan tensor(False)

    Device Data nan tensor(True, device='cuda:0')


The problem is agnostic to the model or data (even doing to randomly generated data), but the following is a basic model for anyone wanting to replicate and troubleshoot. Uses the package timm for efficientnet. I have tried it on a Resnet model (not from timm but locally coded) with the same error.

    class ENet(nn.Module):
        def __init__(self, in_channels, num_classes):
            super(ENet, self).__init__()
            
            self.first_conv = nn.Conv2d(in_channels = in_channels, out_channels = 3, kernel_size = 1)
            self.backbone = timm.create_model('efficientnet_b0', pretrained = False)
            self.relu = nn.ReLU()
            self.classifier = nn.Linear(1000,num_classes)
            self.softmax = nn.Softmax(dim = -1)
            
        def forward(self, x):
            out = self.first_conv(x)
            out = self.relu(out)
            out = self.backbone(out)
            out = self.relu(out)
            out = self.classifier(out)
            out = self.softmax(out)
            return out

below is an excerpt from `rocminfo` My card is 6950 XT but agent 2 shows as gfx1030, not sure if that's relevant, along with the initial warning of NVML.

    ROCk module is loaded
    =====================    
    HSA System Attributes    
    =====================    
    Runtime Version:         1.1
    System Timestamp Freq.:  1000.000000MHz
    Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
    Machine Model:           LARGE                              
    System Endianness:       LITTLE                             
    
    ==========               
    HSA Agents               
    ==========               
    *******                  
    Agent 1                  
    *******                  
      Name:                    AMD Ryzen 7 3700X 8-Core Processor 
      Uuid:                    CPU-XX                             
      Marketing Name:          AMD Ryzen 7 3700X 8-Core Processor 
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
    
    *******                  
    Agent 2                  
    *******                  
      Name:                    gfx1030                            
      Uuid:                    GPU-618b03fa3848708f               
      Marketing Name:                                             
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
      ASIC Revision:           1(0x1)                             
      Cacheline Size:          64(0x40)                           
      Max Clock Freq. (MHz):   2720                                                          
      ISA Info:                
        ISA 1                    
          Name:                    amdgcn-amd-amdhsa--gfx1030         
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

Any help would be appreciated, thanks.

---

## 评论 (8 条)

### 评论 #1 — wxianxin (2023-06-05T05:24:58Z)

@Dunedin87 I am experiencing a similar issue. What's your hardware layout? Is the GPU connected to a full x16 PCIE slot or not?

---

### 评论 #2 — Dunedin87 (2023-07-15T17:07:13Z)

@wxianxin Sorry for the delayed response. Yes it's connected to a full PCIe x16 slot. Which pytorch version are you using? I think the problem might be only in Pytorch 2.0 and not in 1.3

---

### 评论 #3 — wxianxin (2023-07-16T02:47:21Z)

> 

Thanks! Mine setup is different, so my problem can actually be a totally different from yours. I use thunderbolt to connect to external 6800XT. After I send to data to GPU, I see the data is fine(not NaN). However as long as I calculate some matrix operations, I got NaN. I am using pytorch 2.0

---

### 评论 #4 — Dunedin87 (2023-07-19T21:49:10Z)

@wxianxin Interesting. Does the problem persist in pre 2.0 version of pytorch?

---

### 评论 #5 — xuhuisheng (2023-07-19T22:55:18Z)

Even mnist from examples cannot get correct result, in my MI50 instinct with pytorch 2.0.1 or pytorch 2.1.0 nightly.
I tried ROCm-5.4, ROCm-5.5 and ROCm-5.6 under ubuntu-22.04.2, all of them get same incorrect result.

After downgrade to pytorch-1.13, the error had gone. The mnist run properly. SD wont show black pictures. Even exllama can should result with example_basic.
But example_chatbot need pytorch-2.0, so I just want to know, if anyone have clue for pytorch-2.0 part.

---

### 评论 #6 — wxianxin (2023-07-19T23:18:10Z)

> @wxianxin Interesting. Does the problem persist in pre 2.0 version of pytorch?

I didn't have the chance to try  pytorch 1.x unfortunately.

---

### 评论 #7 — Dunedin87 (2023-07-23T17:40:51Z)

> > @wxianxin Interesting. Does the problem persist in pre 2.0 version of pytorch?
> 
> I didn't have the chance to try pytorch 1.x unfortunately.

No worries, as @xuhuisheng has also confirmed, I think the problem lies in Pytorch 2.0. To be honest,a bit ridiculous that this wasn't even tested for.
@xuhuisheng , I think you might stand a better chance of posting the issue on Pytorch's repo. Hopefully they'll fix it in the next 2.xx


---

### 评论 #8 — ppanchad-amd (2024-05-10T19:02:38Z)

Closing ticket since issue is related to Pytorch, not ROCm

---
