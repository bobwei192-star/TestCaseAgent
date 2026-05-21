# [Feature]: Add PopOS to amdgpu-install

> **Issue #5925**
> **状态**: open
> **创建时间**: 2026-02-03T12:05:54Z
> **更新时间**: 2026-02-03T16:48:31Z
> **作者**: SeanTheITGuy
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/5925

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

around line 423 of amdgpu-install, there's a case matching that checks if OS ID matches `ubuntu|linuxmint|debian)`. The installer has worked flawlessly on PopOS with a simple adding of `pop|` to the front of that line since time immemorial. Adding it officially would remove a roadblock for introductory users, removing the need to manually hack install scripts to make it work.

I understand this would require testing on the part of your developers, but it is a relatively simple fix and given that PopOS has as much of a Ubuntu base as Linux Mint, there's no reason it wouldn't work.  PopOS is gaining momentum as a gaming-focussed distribution, so this seems reasonable.

### Operating System

PopOS 24.04

### GPU

_No response_

### ROCm Component

amdgpu-install
