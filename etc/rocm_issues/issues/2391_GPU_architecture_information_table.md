# GPU architecture information table

> **Issue #2391**
> **状态**: closed
> **创建时间**: 2023-08-21T13:29:18Z
> **更新时间**: 2024-03-18T18:33:44Z
> **关闭时间**: 2024-03-18T18:33:43Z
> **作者**: saadrahim
> **标签**: Documentation, hardware:Instinct, hardware:Radeon
> **URL**: https://github.com/ROCm/ROCm/issues/2391

## 标签

- **Documentation** (颜色: #5319e7)
- **hardware:Instinct** (颜色: #1d76db)
- **hardware:Radeon** (颜色: #2B113F)

## 负责人

- MKKnorr

## 描述

A table for GPU architecture details is needed

- Compute Units
- Number of Registers 
- Cache Size
- LLVM GPU architecture target (gfx....)
- VRAM
- wavefront size
- shared memory

---

## 评论 (5 条)

### 评论 #1 — Promesis (2023-08-24T07:16:16Z)

I've got a table from AMD website.

CSV:

```
Model,Compute Units,AMD Infinity Cache Technology,Max Memory Size
AMD Radeon RX 7900 XTX,96,96 MB,24GB
AMD Radeon RX 7900 XT,84,80 MB,20GB
AMD Radeon RX 7900 GRE,80,64 MB,16GB
AMD Radeon RX 7600,32,32 MB,8GB
AMD Radeon RX 7600M XT,32,32 MB,8GB
AMD Radeon RX 7600M,28,32 MB,8GB
AMD Radeon RX 7700S,32,32 MB,8GB
AMD Radeon RX 7600S,28,32 MB,8GB
AMD Radeon RX 6950 XT,80,128 MB,16GB
AMD Radeon RX 6900 XT,80,128 MB,16GB
AMD Radeon RX 6800 XT Midnight Black,72,128 MB,16GB
AMD Radeon RX 6800 XT,72,128 MB,16GB
AMD Radeon RX 6850M XT,40,96 MB,12GB
AMD Radeon RX 6800,60,128 MB,16GB
AMD Radeon RX 6750 XT,40,96 MB,12GB
AMD Radeon RX 6800S,32,32 MB,8GB
AMD Radeon RX 6700 XT,40,96 MB,12GB
AMD Radeon RX 6700,36,80 MB,10GB
AMD Radeon RX 5700 XT 50th Anniversary,40,,8GB
AMD Radeon RX 6800M,40,96 MB,12GB
AMD Radeon RX 6650 XT,32,32 MB,8GB
AMD Radeon RX 6700M,36,80 MB,10GB
AMD Radeon RX 5700 XT,40,,8GB
AMD Radeon RX 6600 XT,32,32 MB,8GB
AMD Radeon RX 6600,28,32 MB,8GB
AMD Radeon RX 6650M XT,32,32 MB,8GB
AMD Radeon VII,60,,16GB
AMD Radeon RX 5700,36,,8GB
AMD Radeon RX 6650M,28,32 MB,8GB
AMD Radeon RX 5600 XT,36,,6GB
AMD Radeon RX 6500 XT,16,16 MB,8GB
AMD Radeon RX 5600,32,,6GB
AMD Radeon RX 6600M,28,32 MB,8GB
AMD Radeon RX 6500 XT (4GB),16,16 MB,4GB
AMD Radeon RX 5500 XT,22,,8GB
AMD Radeon RX 5700M,36,,8GB
AMD Radeon RX 6400,12,16 MB,4GB
AMD Radeon RX 6550M,16,16 MB,4GB
AMD Radeon RX 6500M,16,16 MB,4GB
AMD Radeon RX 5600M,36,,6GB
AMD Radeon RX 5500,22,,4GB
Radeon RX Vega 64 Liquid Cooled,64,,8GB
AMD Radeon RX 5300,22,,3GB
AMD Radeon RX 6700S,28,32 MB,8GB
AMD Radeon RX 5500M,22,,4GB
AMD Radeon RX 6450M,12,16 MB,4GB
AMD Radeon RX 5300M,22,,3GB
AMD Radeon RX 6300M,12,8 MB,2GB
Radeon RX Vega 64,64,,8GB
Radeon RX Vega 56,56,,8GB
AMD Radeon RX 6600S,28,32 MB,4GB
Radeon RX 590,36,,8GB
AMD Radeon RX 6550S,16,16 MB,4GB
Radeon RX 580 (OEM),36,,8GB
Radeon RX 640,8  10  ,,4GB
Radeon RX 580,36,,8GB
Radeon RX 580X,36,,8GB
Radeon RX 570,32,,8GB
Radeon RX 570 (OEM),,,8GB
Radeon 630,8,,4GB
Radeon RX 570X,32,,8GB
Radeon RX 560,14/16,,4GB
Radeon RX 560 (OEM),14/16,,4GB
Radeon 625,6,,4GB
Radeon RX 560X,14/16,,4GB
Radeon RX 550,,,4GB
Radeon 620,6,,4GB
Radeon RX 550X,8  10  ,,4GB
Radeon RX 540,8,,4GB
Radeon 610,5,,4GB
Radeon 550X,8  10  ,,4GB
Radeon RX 540X,8,,4GB
Radeon 540,8,,4GB
Radeon 540X,8,,4GB
Radeon 535,6,,4GB
Radeon 530,6,,4GB
Radeon 520,5,,4GB
AMD Radeon RX 480,36,,4GB
Radeon RX 470,32,,4GB
Radeon RX 460,14,,2GB
AMD Radeon R9 Fury X,64,,4GB
AMD Radeon R9 Fury,56,,4GB
AMD Radeon R9 Nano,64,,4GB
AMD Radeon R9 390X,44,,8GB
AMD Radeon R9 390,40,,8GB
AMD Radeon R9 380X,32,,4GB
AMD Radeon R9 380,28,,4GB
AMD Radeon R9 M395X,,,4GB
AMD Radeon R9 M395,,,4GB
AMD Radeon R9 M390X,,,4GB
AMD Radeon R9 M390,,,4GB
AMD Radeon R9 M385X,,,4GB
AMD Radeon R9 M385,,,4GB
AMD Radeon R9 M380,,,4GB
AMD Radeon R9 M375X,10,,4GB
AMD Radeon R9 M375,10,,4GB
AMD Radeon R9 M365X,10,,4GB
AMD Radeon R9 M360,8,,4GB
AMD Radeon R9 295X2,,,8GB
AMD Radeon R9 290X,,,4GB
AMD Radeon R9 290,,,
AMD Radeon R9 285,,,
AMD Radeon R9 280X,,,3GB
AMD Radeon R9 280,,,3GB
AMD Radeon R9 270X,,,2GB
AMD Radeon R9 270,,,2GB
AMD Radeon R9 M295X,,,
AMD Radeon R9 M290X,20,,4GB
AMD Radeon R9 M285X,,,
AMD Radeon R9 M280X,,,
AMD Radeon R9 M280,14,,4GB
AMD Radeon R9 M275X,10,,4GB
AMD Radeon R9 M270X,10,,4GB
AMD Radeon R9 M265X,10,,4GB
AMD Radeon R7 370,,,4GB
AMD Radeon R7 360,,,2GB
AMD Radeon R7 M380,10,,4GB
AMD Radeon R7 M375,8,,4GB
AMD Radeon R7 M370,,,4GB
AMD Radeon R7 M365X,6,,4GB
AMD Radeon R7 M365,,,4GB
AMD Radeon R7 M360,6,,4GB
AMD Radeon R7 M350,6,,4GB
AMD Radeon R7 M340,6,,4GB
AMD Radeon R7 265,,,4GB
AMD Radeon R7 260X,,,4GB
AMD Radeon R7 260,,,2GB
AMD Radeon R7 250X,,,2GB
AMD Radeon R7 250,,,2GB
AMD Radeon R7 240,,,2GB
AMD Radeon R7 M270,,,
AMD Radeon R7 M265X,,,
AMD Radeon R7 M265AE,,,
AMD Radeon R7 M265,6,,4GB
AMD Radeon R7 M260X,6,,4GB
AMD Radeon R7 M260,6,,4GB
AMD Radeon R5 M335X,5,,4GB
AMD Radeon R5 M335,5,,4GB
AMD Radeon R5 M330,5,,4GB
AMD Radeon R5 M320,5,,4GB
AMD Radeon R5 M315,5,,4GB
AMD Radeon R5 235,,,4GB
AMD Radeon R5 230,,,4GB
AMD Radeon R5 M255X,5,,4GB
AMD Radeon R5 M255,5,,4GB
AMD Radeon R5 M240X,,,
AMD Radeon R5 M240,,,
AMD Radeon R5 M230,5,,4GB
AMD Radeon HD 8970M Series GPU,20,,4GB
AMD Radeon HD 8870M Series GPU,10,,2GB
AMD Radeon HD 8850M Series GPU,10,,2GB
AMD Radeon HD 8830M Series GPU,10,,2GB
AMD Radeon HD 8790M Series GPU,6,,2GB
AMD Radeon HD 8770M Series GPU,6,,2GB
AMD Radeon HD 8750M Series GPU,6,,2GB
AMD Radeon HD 8730M Series GPU,6,,2GB
AMD Radeon HD 8690M Series GPU,6,,2GB
AMD Radeon HD 8670M Series GPU,6,,2GB
AMD Radeon HD 8590M Series GPU,5,,2GB
AMD Radeon HD 8570M Series GPU,5,,2GB
AMD Radeon HD 7990,,,
AMD Radeon HD 7970 GHz Edition,,,3GB
AMD Radeon HD 7970,,,3GB
AMD Radeon HD 7950,28,,3GB
AMD Radeon HD 7870 GHz Edition,,,2GB
AMD Radeon HD 7850,,,2GB
AMD Radeon HD 7790,,,
AMD Radeon HD 7770 GHz Edition,,,1GB
AMD Radeon HD 7750,,,1GB
AMD Radeon HD 7730,,,
AMD Radeon HD 6970,,,2GB
AMD Radeon HD 6950,,,2GB
AMD Radeon HD 6870,,,1GB
AMD Radeon HD 6850,,,1GB
AMD Radeon HD 6770,,,1GB
AMD Radeon HD 6750,,,1GB
AMD Radeon HD 6670,,,1GB
AMD Radeon HD 6570,,,1GB
AMD Radeon HD 6450,,,1GB
ATI Radeon HD 5970,,,2GB
ATI Radeon HD 5870,,,1GB
ATI Radeon HD 5850,,,1GB
ATI Radeon HD 5830,,,1GB
ATI Radeon HD 5770,,,1GB
ATI Radeon HD 5750,,,1GB
ATI Radeon HD 5670,,,1GB
ATI Radeon HD 5570,,,1GB
ATI Radeon HD 5450,,,1GB
```

In human-readable tables:

| **Model**                                  | **Compute Units** | **AMD Infinity Cache Technology** | **Max Memory Size** |
|:------------------------------------------:|:-----------------:|:---------------------------------:|:-------------------:|
| **AMD Radeon RX 7900 XTX**                 | 96                | 96 MB                             | 24GB                |
| **AMD Radeon RX 7900 XT**                  | 84                | 80 MB                             | 20GB                |
| **AMD Radeon RX 7900 GRE**                 | 80                | 64 MB                             | 16GB                |
| **AMD Radeon RX 7600**                     | 32                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 7600M XT**                 | 32                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 7600M**                    | 28                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 7700S**                    | 32                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 7600S**                    | 28                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 6950 XT**                  | 80                | 128 MB                            | 16GB                |
| **AMD Radeon RX 6900 XT**                  | 80                | 128 MB                            | 16GB                |
| **AMD Radeon RX 6800 XT Midnight Black**   | 72                | 128 MB                            | 16GB                |
| **AMD Radeon RX 6800 XT**                  | 72                | 128 MB                            | 16GB                |
| **AMD Radeon RX 6850M XT**                 | 40                | 96 MB                             | 12GB                |
| **AMD Radeon RX 6800**                     | 60                | 128 MB                            | 16GB                |
| **AMD Radeon RX 6750 XT**                  | 40                | 96 MB                             | 12GB                |
| **AMD Radeon RX 6800S**                    | 32                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 6700 XT**                  | 40                | 96 MB                             | 12GB                |
| **AMD Radeon RX 6700**                     | 36                | 80 MB                             | 10GB                |
| **AMD Radeon RX 5700 XT 50th Anniversary** | 40                |                                   | 8GB                 |
| **AMD Radeon RX 6800M**                    | 40                | 96 MB                             | 12GB                |
| **AMD Radeon RX 6650 XT**                  | 32                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 6700M**                    | 36                | 80 MB                             | 10GB                |
| **AMD Radeon RX 5700 XT**                  | 40                |                                   | 8GB                 |
| **AMD Radeon RX 6600 XT**                  | 32                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 6600**                     | 28                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 6650M XT**                 | 32                | 32 MB                             | 8GB                 |
| **AMD Radeon VII**                         | 60                |                                   | 16GB                |
| **AMD Radeon RX 5700**                     | 36                |                                   | 8GB                 |
| **AMD Radeon RX 6650M**                    | 28                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 5600 XT**                  | 36                |                                   | 6GB                 |
| **AMD Radeon RX 6500 XT**                  | 16                | 16 MB                             | 8GB                 |
| **AMD Radeon RX 5600**                     | 32                |                                   | 6GB                 |
| **AMD Radeon RX 6600M**                    | 28                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 6500 XT (4GB)**            | 16                | 16 MB                             | 4GB                 |
| **AMD Radeon RX 5500 XT**                  | 22                |                                   | 8GB                 |
| **AMD Radeon RX 5700M**                    | 36                |                                   | 8GB                 |
| **AMD Radeon RX 6400**                     | 12                | 16 MB                             | 4GB                 |
| **AMD Radeon RX 6550M**                    | 16                | 16 MB                             | 4GB                 |
| **AMD Radeon RX 6500M**                    | 16                | 16 MB                             | 4GB                 |
| **AMD Radeon RX 5600M**                    | 36                |                                   | 6GB                 |
| **AMD Radeon RX 5500**                     | 22                |                                   | 4GB                 |
| **Radeon RX Vega 64 Liquid Cooled**        | 64                |                                   | 8GB                 |
| **AMD Radeon RX 5300**                     | 22                |                                   | 3GB                 |
| **AMD Radeon RX 6700S**                    | 28                | 32 MB                             | 8GB                 |
| **AMD Radeon RX 5500M**                    | 22                |                                   | 4GB                 |
| **AMD Radeon RX 6450M**                    | 12                | 16 MB                             | 4GB                 |
| **AMD Radeon RX 5300M**                    | 22                |                                   | 3GB                 |
| **AMD Radeon RX 6300M**                    | 12                | 8 MB                              | 2GB                 |
| **Radeon RX Vega 64**                      | 64                |                                   | 8GB                 |
| **Radeon RX Vega 56**                      | 56                |                                   | 8GB                 |
| **AMD Radeon RX 6600S**                    | 28                | 32 MB                             | 4GB                 |
| **Radeon RX 590**                          | 36                |                                   | 8GB                 |
| **AMD Radeon RX 6550S**                    | 16                | 16 MB                             | 4GB                 |
| **Radeon RX 580 (OEM)**                    | 36                |                                   | 8GB                 |
| **Radeon RX 640**                          | 8  10             |                                   | 4GB                 |
| **Radeon RX 580**                          | 36                |                                   | 8GB                 |
| **Radeon RX 580X**                         | 36                |                                   | 8GB                 |
| **Radeon RX 570**                          | 32                |                                   | 8GB                 |
| **Radeon RX 570 (OEM)**                    |                   |                                   | 8GB                 |
| **Radeon 630**                             | 8                 |                                   | 4GB                 |
| **Radeon RX 570X**                         | 32                |                                   | 8GB                 |
| **Radeon RX 560**                          | 14/16             |                                   | 4GB                 |
| **Radeon RX 560 (OEM)**                    | 14/16             |                                   | 4GB                 |
| **Radeon 625**                             | 6                 |                                   | 4GB                 |
| **Radeon RX 560X**                         | 14/16             |                                   | 4GB                 |
| **Radeon RX 550**                          |                   |                                   | 4GB                 |
| **Radeon 620**                             | 6                 |                                   | 4GB                 |
| **Radeon RX 550X**                         | 8  10             |                                   | 4GB                 |
| **Radeon RX 540**                          | 8                 |                                   | 4GB                 |
| **Radeon 610**                             | 5                 |                                   | 4GB                 |
| **Radeon 550X**                            | 8  10             |                                   | 4GB                 |
| **Radeon RX 540X**                         | 8                 |                                   | 4GB                 |
| **Radeon 540**                             | 8                 |                                   | 4GB                 |
| **Radeon 540X**                            | 8                 |                                   | 4GB                 |
| **Radeon 535**                             | 6                 |                                   | 4GB                 |
| **Radeon 530**                             | 6                 |                                   | 4GB                 |
| **Radeon 520**                             | 5                 |                                   | 4GB                 |
| **AMD Radeon RX 480**                      | 36                |                                   | 4GB                 |
| **Radeon RX 470**                          | 32                |                                   | 4GB                 |
| **Radeon RX 460**                          | 14                |                                   | 2GB                 |
| **AMD Radeon R9 Fury X**                   | 64                |                                   | 4GB                 |
| **AMD Radeon R9 Fury**                     | 56                |                                   | 4GB                 |
| **AMD Radeon R9 Nano**                     | 64                |                                   | 4GB                 |
| **AMD Radeon R9 390X**                     | 44                |                                   | 8GB                 |
| **AMD Radeon R9 390**                      | 40                |                                   | 8GB                 |
| **AMD Radeon R9 380X**                     | 32                |                                   | 4GB                 |
| **AMD Radeon R9 380**                      | 28                |                                   | 4GB                 |
| **AMD Radeon R9 M395X**                    |                   |                                   | 4GB                 |
| **AMD Radeon R9 M395**                     |                   |                                   | 4GB                 |
| **AMD Radeon R9 M390X**                    |                   |                                   | 4GB                 |
| **AMD Radeon R9 M390**                     |                   |                                   | 4GB                 |
| **AMD Radeon R9 M385X**                    |                   |                                   | 4GB                 |
| **AMD Radeon R9 M385**                     |                   |                                   | 4GB                 |
| **AMD Radeon R9 M380**                     |                   |                                   | 4GB                 |
| **AMD Radeon R9 M375X**                    | 10                |                                   | 4GB                 |
| **AMD Radeon R9 M375**                     | 10                |                                   | 4GB                 |
| **AMD Radeon R9 M365X**                    | 10                |                                   | 4GB                 |
| **AMD Radeon R9 M360**                     | 8                 |                                   | 4GB                 |
| **AMD Radeon R9 295X2**                    |                   |                                   | 8GB                 |
| **AMD Radeon R9 290X**                     |                   |                                   | 4GB                 |
| **AMD Radeon R9 290**                      |                   |                                   |                     |
| **AMD Radeon R9 285**                      |                   |                                   |                     |
| **AMD Radeon R9 280X**                     |                   |                                   | 3GB                 |
| **AMD Radeon R9 280**                      |                   |                                   | 3GB                 |
| **AMD Radeon R9 270X**                     |                   |                                   | 2GB                 |
| **AMD Radeon R9 270**                      |                   |                                   | 2GB                 |
| **AMD Radeon R9 M295X**                    |                   |                                   |                     |
| **AMD Radeon R9 M290X**                    | 20                |                                   | 4GB                 |
| **AMD Radeon R9 M285X**                    |                   |                                   |                     |
| **AMD Radeon R9 M280X**                    |                   |                                   |                     |
| **AMD Radeon R9 M280**                     | 14                |                                   | 4GB                 |
| **AMD Radeon R9 M275X**                    | 10                |                                   | 4GB                 |
| **AMD Radeon R9 M270X**                    | 10                |                                   | 4GB                 |
| **AMD Radeon R9 M265X**                    | 10                |                                   | 4GB                 |
| **AMD Radeon R7 370**                      |                   |                                   | 4GB                 |
| **AMD Radeon R7 360**                      |                   |                                   | 2GB                 |
| **AMD Radeon R7 M380**                     | 10                |                                   | 4GB                 |
| **AMD Radeon R7 M375**                     | 8                 |                                   | 4GB                 |
| **AMD Radeon R7 M370**                     |                   |                                   | 4GB                 |
| **AMD Radeon R7 M365X**                    | 6                 |                                   | 4GB                 |
| **AMD Radeon R7 M365**                     |                   |                                   | 4GB                 |
| **AMD Radeon R7 M360**                     | 6                 |                                   | 4GB                 |
| **AMD Radeon R7 M350**                     | 6                 |                                   | 4GB                 |
| **AMD Radeon R7 M340**                     | 6                 |                                   | 4GB                 |
| **AMD Radeon R7 265**                      |                   |                                   | 4GB                 |
| **AMD Radeon R7 260X**                     |                   |                                   | 4GB                 |
| **AMD Radeon R7 260**                      |                   |                                   | 2GB                 |
| **AMD Radeon R7 250X**                     |                   |                                   | 2GB                 |
| **AMD Radeon R7 250**                      |                   |                                   | 2GB                 |
| **AMD Radeon R7 240**                      |                   |                                   | 2GB                 |
| **AMD Radeon R7 M270**                     |                   |                                   |                     |
| **AMD Radeon R7 M265X**                    |                   |                                   |                     |
| **AMD Radeon R7 M265AE**                   |                   |                                   |                     |
| **AMD Radeon R7 M265**                     | 6                 |                                   | 4GB                 |
| **AMD Radeon R7 M260X**                    | 6                 |                                   | 4GB                 |
| **AMD Radeon R7 M260**                     | 6                 |                                   | 4GB                 |
| **AMD Radeon R5 M335X**                    | 5                 |                                   | 4GB                 |
| **AMD Radeon R5 M335**                     | 5                 |                                   | 4GB                 |
| **AMD Radeon R5 M330**                     | 5                 |                                   | 4GB                 |
| **AMD Radeon R5 M320**                     | 5                 |                                   | 4GB                 |
| **AMD Radeon R5 M315**                     | 5                 |                                   | 4GB                 |
| **AMD Radeon R5 235**                      |                   |                                   | 4GB                 |
| **AMD Radeon R5 230**                      |                   |                                   | 4GB                 |
| **AMD Radeon R5 M255X**                    | 5                 |                                   | 4GB                 |
| **AMD Radeon R5 M255**                     | 5                 |                                   | 4GB                 |
| **AMD Radeon R5 M240X**                    |                   |                                   |                     |
| **AMD Radeon R5 M240**                     |                   |                                   |                     |
| **AMD Radeon R5 M230**                     | 5                 |                                   | 4GB                 |
| **AMD Radeon HD 8970M Series GPU**         | 20                |                                   | 4GB                 |
| **AMD Radeon HD 8870M Series GPU**         | 10                |                                   | 2GB                 |
| **AMD Radeon HD 8850M Series GPU**         | 10                |                                   | 2GB                 |
| **AMD Radeon HD 8830M Series GPU**         | 10                |                                   | 2GB                 |
| **AMD Radeon HD 8790M Series GPU**         | 6                 |                                   | 2GB                 |
| **AMD Radeon HD 8770M Series GPU**         | 6                 |                                   | 2GB                 |
| **AMD Radeon HD 8750M Series GPU**         | 6                 |                                   | 2GB                 |
| **AMD Radeon HD 8730M Series GPU**         | 6                 |                                   | 2GB                 |
| **AMD Radeon HD 8690M Series GPU**         | 6                 |                                   | 2GB                 |
| **AMD Radeon HD 8670M Series GPU**         | 6                 |                                   | 2GB                 |
| **AMD Radeon HD 8590M Series GPU**         | 5                 |                                   | 2GB                 |
| **AMD Radeon HD 8570M Series GPU**         | 5                 |                                   | 2GB                 |
| **AMD Radeon HD 7990**                     |                   |                                   |                     |
| **AMD Radeon HD 7970 GHz Edition**         |                   |                                   | 3GB                 |
| **AMD Radeon HD 7970**                     |                   |                                   | 3GB                 |
| **AMD Radeon HD 7950**                     | 28                |                                   | 3GB                 |
| **AMD Radeon HD 7870 GHz Edition**         |                   |                                   | 2GB                 |
| **AMD Radeon HD 7850**                     |                   |                                   | 2GB                 |
| **AMD Radeon HD 7790**                     |                   |                                   |                     |
| **AMD Radeon HD 7770 GHz Edition**         |                   |                                   | 1GB                 |
| **AMD Radeon HD 7750**                     |                   |                                   | 1GB                 |
| **AMD Radeon HD 7730**                     |                   |                                   |                     |
| **AMD Radeon HD 6970**                     |                   |                                   | 2GB                 |
| **AMD Radeon HD 6950**                     |                   |                                   | 2GB                 |
| **AMD Radeon HD 6870**                     |                   |                                   | 1GB                 |
| **AMD Radeon HD 6850**                     |                   |                                   | 1GB                 |
| **AMD Radeon HD 6770**                     |                   |                                   | 1GB                 |
| **AMD Radeon HD 6750**                     |                   |                                   | 1GB                 |
| **AMD Radeon HD 6670**                     |                   |                                   | 1GB                 |
| **AMD Radeon HD 6570**                     |                   |                                   | 1GB                 |
| **AMD Radeon HD 6450**                     |                   |                                   | 1GB                 |
| **ATI Radeon HD 5970**                     |                   |                                   | 2GB                 |
| **ATI Radeon HD 5870**                     |                   |                                   | 1GB                 |
| **ATI Radeon HD 5850**                     |                   |                                   | 1GB                 |
| **ATI Radeon HD 5830**                     |                   |                                   | 1GB                 |
| **ATI Radeon HD 5770**                     |                   |                                   | 1GB                 |
| **ATI Radeon HD 5750**                     |                   |                                   | 1GB                 |
| **ATI Radeon HD 5670**                     |                   |                                   | 1GB                 |
| **ATI Radeon HD 5570**                     |                   |                                   | 1GB                 |
| **ATI Radeon HD 5450**                     |                   |                                   | 1GB                 |


---

### 评论 #2 — saadrahim (2023-08-24T15:40:03Z)

> I've got a table from AMD website.
> 
> CSV:
> 
> ```
> Model,Compute Units,AMD Infinity Cache Technology,Max Memory Size
> AMD Radeon RX 7900 XTX,96,96 MB,24GB
> AMD Radeon RX 7900 XT,84,80 MB,20GB
> AMD Radeon RX 7900 GRE,80,64 MB,16GB
> AMD Radeon RX 7600,32,32 MB,8GB
> AMD Radeon RX 7600M XT,32,32 MB,8GB
> AMD Radeon RX 7600M,28,32 MB,8GB
> AMD Radeon RX 7700S,32,32 MB,8GB
> AMD Radeon RX 7600S,28,32 MB,8GB
> AMD Radeon RX 6950 XT,80,128 MB,16GB
> AMD Radeon RX 6900 XT,80,128 MB,16GB
> AMD Radeon RX 6800 XT Midnight Black,72,128 MB,16GB
> AMD Radeon RX 6800 XT,72,128 MB,16GB
> AMD Radeon RX 6850M XT,40,96 MB,12GB
> AMD Radeon RX 6800,60,128 MB,16GB
> AMD Radeon RX 6750 XT,40,96 MB,12GB
> AMD Radeon RX 6800S,32,32 MB,8GB
> AMD Radeon RX 6700 XT,40,96 MB,12GB
> AMD Radeon RX 6700,36,80 MB,10GB
> AMD Radeon RX 5700 XT 50th Anniversary,40,,8GB
> AMD Radeon RX 6800M,40,96 MB,12GB
> AMD Radeon RX 6650 XT,32,32 MB,8GB
> AMD Radeon RX 6700M,36,80 MB,10GB
> AMD Radeon RX 5700 XT,40,,8GB
> AMD Radeon RX 6600 XT,32,32 MB,8GB
> AMD Radeon RX 6600,28,32 MB,8GB
> AMD Radeon RX 6650M XT,32,32 MB,8GB
> AMD Radeon VII,60,,16GB
> AMD Radeon RX 5700,36,,8GB
> AMD Radeon RX 6650M,28,32 MB,8GB
> AMD Radeon RX 5600 XT,36,,6GB
> AMD Radeon RX 6500 XT,16,16 MB,8GB
> AMD Radeon RX 5600,32,,6GB
> AMD Radeon RX 6600M,28,32 MB,8GB
> AMD Radeon RX 6500 XT (4GB),16,16 MB,4GB
> AMD Radeon RX 5500 XT,22,,8GB
> AMD Radeon RX 5700M,36,,8GB
> AMD Radeon RX 6400,12,16 MB,4GB
> AMD Radeon RX 6550M,16,16 MB,4GB
> AMD Radeon RX 6500M,16,16 MB,4GB
> AMD Radeon RX 5600M,36,,6GB
> AMD Radeon RX 5500,22,,4GB
> Radeon RX Vega 64 Liquid Cooled,64,,8GB
> AMD Radeon RX 5300,22,,3GB
> AMD Radeon RX 6700S,28,32 MB,8GB
> AMD Radeon RX 5500M,22,,4GB
> AMD Radeon RX 6450M,12,16 MB,4GB
> AMD Radeon RX 5300M,22,,3GB
> AMD Radeon RX 6300M,12,8 MB,2GB
> Radeon RX Vega 64,64,,8GB
> Radeon RX Vega 56,56,,8GB
> AMD Radeon RX 6600S,28,32 MB,4GB
> Radeon RX 590,36,,8GB
> AMD Radeon RX 6550S,16,16 MB,4GB
> Radeon RX 580 (OEM),36,,8GB
> Radeon RX 640,8  10  ,,4GB
> Radeon RX 580,36,,8GB
> Radeon RX 580X,36,,8GB
> Radeon RX 570,32,,8GB
> Radeon RX 570 (OEM),,,8GB
> Radeon 630,8,,4GB
> Radeon RX 570X,32,,8GB
> Radeon RX 560,14/16,,4GB
> Radeon RX 560 (OEM),14/16,,4GB
> Radeon 625,6,,4GB
> Radeon RX 560X,14/16,,4GB
> Radeon RX 550,,,4GB
> Radeon 620,6,,4GB
> Radeon RX 550X,8  10  ,,4GB
> Radeon RX 540,8,,4GB
> Radeon 610,5,,4GB
> Radeon 550X,8  10  ,,4GB
> Radeon RX 540X,8,,4GB
> Radeon 540,8,,4GB
> Radeon 540X,8,,4GB
> Radeon 535,6,,4GB
> Radeon 530,6,,4GB
> Radeon 520,5,,4GB
> AMD Radeon RX 480,36,,4GB
> Radeon RX 470,32,,4GB
> Radeon RX 460,14,,2GB
> AMD Radeon R9 Fury X,64,,4GB
> AMD Radeon R9 Fury,56,,4GB
> AMD Radeon R9 Nano,64,,4GB
> AMD Radeon R9 390X,44,,8GB
> AMD Radeon R9 390,40,,8GB
> AMD Radeon R9 380X,32,,4GB
> AMD Radeon R9 380,28,,4GB
> AMD Radeon R9 M395X,,,4GB
> AMD Radeon R9 M395,,,4GB
> AMD Radeon R9 M390X,,,4GB
> AMD Radeon R9 M390,,,4GB
> AMD Radeon R9 M385X,,,4GB
> AMD Radeon R9 M385,,,4GB
> AMD Radeon R9 M380,,,4GB
> AMD Radeon R9 M375X,10,,4GB
> AMD Radeon R9 M375,10,,4GB
> AMD Radeon R9 M365X,10,,4GB
> AMD Radeon R9 M360,8,,4GB
> AMD Radeon R9 295X2,,,8GB
> AMD Radeon R9 290X,,,4GB
> AMD Radeon R9 290,,,
> AMD Radeon R9 285,,,
> AMD Radeon R9 280X,,,3GB
> AMD Radeon R9 280,,,3GB
> AMD Radeon R9 270X,,,2GB
> AMD Radeon R9 270,,,2GB
> AMD Radeon R9 M295X,,,
> AMD Radeon R9 M290X,20,,4GB
> AMD Radeon R9 M285X,,,
> AMD Radeon R9 M280X,,,
> AMD Radeon R9 M280,14,,4GB
> AMD Radeon R9 M275X,10,,4GB
> AMD Radeon R9 M270X,10,,4GB
> AMD Radeon R9 M265X,10,,4GB
> AMD Radeon R7 370,,,4GB
> AMD Radeon R7 360,,,2GB
> AMD Radeon R7 M380,10,,4GB
> AMD Radeon R7 M375,8,,4GB
> AMD Radeon R7 M370,,,4GB
> AMD Radeon R7 M365X,6,,4GB
> AMD Radeon R7 M365,,,4GB
> AMD Radeon R7 M360,6,,4GB
> AMD Radeon R7 M350,6,,4GB
> AMD Radeon R7 M340,6,,4GB
> AMD Radeon R7 265,,,4GB
> AMD Radeon R7 260X,,,4GB
> AMD Radeon R7 260,,,2GB
> AMD Radeon R7 250X,,,2GB
> AMD Radeon R7 250,,,2GB
> AMD Radeon R7 240,,,2GB
> AMD Radeon R7 M270,,,
> AMD Radeon R7 M265X,,,
> AMD Radeon R7 M265AE,,,
> AMD Radeon R7 M265,6,,4GB
> AMD Radeon R7 M260X,6,,4GB
> AMD Radeon R7 M260,6,,4GB
> AMD Radeon R5 M335X,5,,4GB
> AMD Radeon R5 M335,5,,4GB
> AMD Radeon R5 M330,5,,4GB
> AMD Radeon R5 M320,5,,4GB
> AMD Radeon R5 M315,5,,4GB
> AMD Radeon R5 235,,,4GB
> AMD Radeon R5 230,,,4GB
> AMD Radeon R5 M255X,5,,4GB
> AMD Radeon R5 M255,5,,4GB
> AMD Radeon R5 M240X,,,
> AMD Radeon R5 M240,,,
> AMD Radeon R5 M230,5,,4GB
> AMD Radeon HD 8970M Series GPU,20,,4GB
> AMD Radeon HD 8870M Series GPU,10,,2GB
> AMD Radeon HD 8850M Series GPU,10,,2GB
> AMD Radeon HD 8830M Series GPU,10,,2GB
> AMD Radeon HD 8790M Series GPU,6,,2GB
> AMD Radeon HD 8770M Series GPU,6,,2GB
> AMD Radeon HD 8750M Series GPU,6,,2GB
> AMD Radeon HD 8730M Series GPU,6,,2GB
> AMD Radeon HD 8690M Series GPU,6,,2GB
> AMD Radeon HD 8670M Series GPU,6,,2GB
> AMD Radeon HD 8590M Series GPU,5,,2GB
> AMD Radeon HD 8570M Series GPU,5,,2GB
> AMD Radeon HD 7990,,,
> AMD Radeon HD 7970 GHz Edition,,,3GB
> AMD Radeon HD 7970,,,3GB
> AMD Radeon HD 7950,28,,3GB
> AMD Radeon HD 7870 GHz Edition,,,2GB
> AMD Radeon HD 7850,,,2GB
> AMD Radeon HD 7790,,,
> AMD Radeon HD 7770 GHz Edition,,,1GB
> AMD Radeon HD 7750,,,1GB
> AMD Radeon HD 7730,,,
> AMD Radeon HD 6970,,,2GB
> AMD Radeon HD 6950,,,2GB
> AMD Radeon HD 6870,,,1GB
> AMD Radeon HD 6850,,,1GB
> AMD Radeon HD 6770,,,1GB
> AMD Radeon HD 6750,,,1GB
> AMD Radeon HD 6670,,,1GB
> AMD Radeon HD 6570,,,1GB
> AMD Radeon HD 6450,,,1GB
> ATI Radeon HD 5970,,,2GB
> ATI Radeon HD 5870,,,1GB
> ATI Radeon HD 5850,,,1GB
> ATI Radeon HD 5830,,,1GB
> ATI Radeon HD 5770,,,1GB
> ATI Radeon HD 5750,,,1GB
> ATI Radeon HD 5670,,,1GB
> ATI Radeon HD 5570,,,1GB
> ATI Radeon HD 5450,,,1GB
> ```
> 
> In human-readable tables:
> 
> **Model**	**Compute Units**	**AMD Infinity Cache Technology**	**Max Memory Size**
> **AMD Radeon RX 7900 XTX**	96	96 MB	24GB
> **AMD Radeon RX 7900 XT**	84	80 MB	20GB
> **AMD Radeon RX 7900 GRE**	80	64 MB	16GB
> **AMD Radeon RX 7600**	32	32 MB	8GB
> **AMD Radeon RX 7600M XT**	32	32 MB	8GB
> **AMD Radeon RX 7600M**	28	32 MB	8GB
> **AMD Radeon RX 7700S**	32	32 MB	8GB
> **AMD Radeon RX 7600S**	28	32 MB	8GB
> **AMD Radeon RX 6950 XT**	80	128 MB	16GB
> **AMD Radeon RX 6900 XT**	80	128 MB	16GB
> **AMD Radeon RX 6800 XT Midnight Black**	72	128 MB	16GB
> **AMD Radeon RX 6800 XT**	72	128 MB	16GB
> **AMD Radeon RX 6850M XT**	40	96 MB	12GB
> **AMD Radeon RX 6800**	60	128 MB	16GB
> **AMD Radeon RX 6750 XT**	40	96 MB	12GB
> **AMD Radeon RX 6800S**	32	32 MB	8GB
> **AMD Radeon RX 6700 XT**	40	96 MB	12GB
> **AMD Radeon RX 6700**	36	80 MB	10GB
> **AMD Radeon RX 5700 XT 50th Anniversary**	40		8GB
> **AMD Radeon RX 6800M**	40	96 MB	12GB
> **AMD Radeon RX 6650 XT**	32	32 MB	8GB
> **AMD Radeon RX 6700M**	36	80 MB	10GB
> **AMD Radeon RX 5700 XT**	40		8GB
> **AMD Radeon RX 6600 XT**	32	32 MB	8GB
> **AMD Radeon RX 6600**	28	32 MB	8GB
> **AMD Radeon RX 6650M XT**	32	32 MB	8GB
> **AMD Radeon VII**	60		16GB
> **AMD Radeon RX 5700**	36		8GB
> **AMD Radeon RX 6650M**	28	32 MB	8GB
> **AMD Radeon RX 5600 XT**	36		6GB
> **AMD Radeon RX 6500 XT**	16	16 MB	8GB
> **AMD Radeon RX 5600**	32		6GB
> **AMD Radeon RX 6600M**	28	32 MB	8GB
> **AMD Radeon RX 6500 XT (4GB)**	16	16 MB	4GB
> **AMD Radeon RX 5500 XT**	22		8GB
> **AMD Radeon RX 5700M**	36		8GB
> **AMD Radeon RX 6400**	12	16 MB	4GB
> **AMD Radeon RX 6550M**	16	16 MB	4GB
> **AMD Radeon RX 6500M**	16	16 MB	4GB
> **AMD Radeon RX 5600M**	36		6GB
> **AMD Radeon RX 5500**	22		4GB
> **Radeon RX Vega 64 Liquid Cooled**	64		8GB
> **AMD Radeon RX 5300**	22		3GB
> **AMD Radeon RX 6700S**	28	32 MB	8GB
> **AMD Radeon RX 5500M**	22		4GB
> **AMD Radeon RX 6450M**	12	16 MB	4GB
> **AMD Radeon RX 5300M**	22		3GB
> **AMD Radeon RX 6300M**	12	8 MB	2GB
> **Radeon RX Vega 64**	64		8GB
> **Radeon RX Vega 56**	56		8GB
> **AMD Radeon RX 6600S**	28	32 MB	4GB
> **Radeon RX 590**	36		8GB
> **AMD Radeon RX 6550S**	16	16 MB	4GB
> **Radeon RX 580 (OEM)**	36		8GB
> **Radeon RX 640**	8 10		4GB
> **Radeon RX 580**	36		8GB
> **Radeon RX 580X**	36		8GB
> **Radeon RX 570**	32		8GB
> **Radeon RX 570 (OEM)**			8GB
> **Radeon 630**	8		4GB
> **Radeon RX 570X**	32		8GB
> **Radeon RX 560**	14/16		4GB
> **Radeon RX 560 (OEM)**	14/16		4GB
> **Radeon 625**	6		4GB
> **Radeon RX 560X**	14/16		4GB
> **Radeon RX 550**			4GB
> **Radeon 620**	6		4GB
> **Radeon RX 550X**	8 10		4GB
> **Radeon RX 540**	8		4GB
> **Radeon 610**	5		4GB
> **Radeon 550X**	8 10		4GB
> **Radeon RX 540X**	8		4GB
> **Radeon 540**	8		4GB
> **Radeon 540X**	8		4GB
> **Radeon 535**	6		4GB
> **Radeon 530**	6		4GB
> **Radeon 520**	5		4GB
> **AMD Radeon RX 480**	36		4GB
> **Radeon RX 470**	32		4GB
> **Radeon RX 460**	14		2GB
> **AMD Radeon R9 Fury X**	64		4GB
> **AMD Radeon R9 Fury**	56		4GB
> **AMD Radeon R9 Nano**	64		4GB
> **AMD Radeon R9 390X**	44		8GB
> **AMD Radeon R9 390**	40		8GB
> **AMD Radeon R9 380X**	32		4GB
> **AMD Radeon R9 380**	28		4GB
> **AMD Radeon R9 M395X**			4GB
> **AMD Radeon R9 M395**			4GB
> **AMD Radeon R9 M390X**			4GB
> **AMD Radeon R9 M390**			4GB
> **AMD Radeon R9 M385X**			4GB
> **AMD Radeon R9 M385**			4GB
> **AMD Radeon R9 M380**			4GB
> **AMD Radeon R9 M375X**	10		4GB
> **AMD Radeon R9 M375**	10		4GB
> **AMD Radeon R9 M365X**	10		4GB
> **AMD Radeon R9 M360**	8		4GB
> **AMD Radeon R9 295X2**			8GB
> **AMD Radeon R9 290X**			4GB
> **AMD Radeon R9 290**			
> **AMD Radeon R9 285**			
> **AMD Radeon R9 280X**			3GB
> **AMD Radeon R9 280**			3GB
> **AMD Radeon R9 270X**			2GB
> **AMD Radeon R9 270**			2GB
> **AMD Radeon R9 M295X**			
> **AMD Radeon R9 M290X**	20		4GB
> **AMD Radeon R9 M285X**			
> **AMD Radeon R9 M280X**			
> **AMD Radeon R9 M280**	14		4GB
> **AMD Radeon R9 M275X**	10		4GB
> **AMD Radeon R9 M270X**	10		4GB
> **AMD Radeon R9 M265X**	10		4GB
> **AMD Radeon R7 370**			4GB
> **AMD Radeon R7 360**			2GB
> **AMD Radeon R7 M380**	10		4GB
> **AMD Radeon R7 M375**	8		4GB
> **AMD Radeon R7 M370**			4GB
> **AMD Radeon R7 M365X**	6		4GB
> **AMD Radeon R7 M365**			4GB
> **AMD Radeon R7 M360**	6		4GB
> **AMD Radeon R7 M350**	6		4GB
> **AMD Radeon R7 M340**	6		4GB
> **AMD Radeon R7 265**			4GB
> **AMD Radeon R7 260X**			4GB
> **AMD Radeon R7 260**			2GB
> **AMD Radeon R7 250X**			2GB
> **AMD Radeon R7 250**			2GB
> **AMD Radeon R7 240**			2GB
> **AMD Radeon R7 M270**			
> **AMD Radeon R7 M265X**			
> **AMD Radeon R7 M265AE**			
> **AMD Radeon R7 M265**	6		4GB
> **AMD Radeon R7 M260X**	6		4GB
> **AMD Radeon R7 M260**	6		4GB
> **AMD Radeon R5 M335X**	5		4GB
> **AMD Radeon R5 M335**	5		4GB
> **AMD Radeon R5 M330**	5		4GB
> **AMD Radeon R5 M320**	5		4GB
> **AMD Radeon R5 M315**	5		4GB
> **AMD Radeon R5 235**			4GB
> **AMD Radeon R5 230**			4GB
> **AMD Radeon R5 M255X**	5		4GB
> **AMD Radeon R5 M255**	5		4GB
> **AMD Radeon R5 M240X**			
> **AMD Radeon R5 M240**			
> **AMD Radeon R5 M230**	5		4GB
> **AMD Radeon HD 8970M Series GPU**	20		4GB
> **AMD Radeon HD 8870M Series GPU**	10		2GB
> **AMD Radeon HD 8850M Series GPU**	10		2GB
> **AMD Radeon HD 8830M Series GPU**	10		2GB
> **AMD Radeon HD 8790M Series GPU**	6		2GB
> **AMD Radeon HD 8770M Series GPU**	6		2GB
> **AMD Radeon HD 8750M Series GPU**	6		2GB
> **AMD Radeon HD 8730M Series GPU**	6		2GB
> **AMD Radeon HD 8690M Series GPU**	6		2GB
> **AMD Radeon HD 8670M Series GPU**	6		2GB
> **AMD Radeon HD 8590M Series GPU**	5		2GB
> **AMD Radeon HD 8570M Series GPU**	5		2GB
> **AMD Radeon HD 7990**			
> **AMD Radeon HD 7970 GHz Edition**			3GB
> **AMD Radeon HD 7970**			3GB
> **AMD Radeon HD 7950**	28		3GB
> **AMD Radeon HD 7870 GHz Edition**			2GB
> **AMD Radeon HD 7850**			2GB
> **AMD Radeon HD 7790**			
> **AMD Radeon HD 7770 GHz Edition**			1GB
> **AMD Radeon HD 7750**			1GB
> **AMD Radeon HD 7730**			
> **AMD Radeon HD 6970**			2GB
> **AMD Radeon HD 6950**			2GB
> **AMD Radeon HD 6870**			1GB
> **AMD Radeon HD 6850**			1GB
> **AMD Radeon HD 6770**			1GB
> **AMD Radeon HD 6750**			1GB
> **AMD Radeon HD 6670**			1GB
> **AMD Radeon HD 6570**			1GB
> **AMD Radeon HD 6450**			1GB
> **ATI Radeon HD 5970**			2GB
> **ATI Radeon HD 5870**			1GB
> **ATI Radeon HD 5850**			1GB
> **ATI Radeon HD 5830**			1GB
> **ATI Radeon HD 5770**			1GB
> **ATI Radeon HD 5750**			1GB
> **ATI Radeon HD 5670**			1GB
> **ATI Radeon HD 5570**			1GB
> **ATI Radeon HD 5450**			1GB

Thanks for your help on this. We will be adding additional GPU information to this list.

---

### 评论 #3 — nartmada (2024-03-16T02:21:39Z)

Hi @saadrahim, can I close this ticket (if no further efforts needed)?  Thanks.

---

### 评论 #4 — MKKnorr (2024-03-18T12:44:35Z)

@nartmada when https://github.com/ROCm/ROCm/pull/2960 is merged, then all currently supported GPUs are documented. If further GPUs should be added, I'd suggest opening a new issue

---

### 评论 #5 — nartmada (2024-03-18T18:33:44Z)

Thanks @MKKnorr.  Closing the ticket.

---
