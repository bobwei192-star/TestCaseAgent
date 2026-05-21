# GPG issue on ubuntu

> **Issue #2362**
> **状态**: closed
> **创建时间**: 2023-08-02T21:40:21Z
> **更新时间**: 2023-12-11T22:39:32Z
> **关闭时间**: 2023-12-11T22:39:32Z
> **作者**: ye-luo
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2362

## 负责人

- Naraenda

## 描述

I followed https://rocm.docs.amd.com/en/latest/deploy/linux/os-native/install.html to re-add key but I keep getting
```
The following signatures were invalid: EXPKEYSIG 9386B48A1A693C5C James Adrian Edwards (ROCm Release Manager) <JamesAdrian.Edwards@amd.com>
```
I tried to verify the key and got
```
sha1sum /etc/apt/keyrings/rocm.gpg 
ececf5eea22ced391975f46ba3e11ad58a12c794  /etc/apt/keyrings/rocm.gpg
```
which is different from 73f5d8100de6048aa38a8b84cd9a87f05177d208 mentioned in https://rocm.docs.amd.com/en/latest/deploy/linux/os-native/install.html

How to fix this?


---

## 评论 (2 条)

### 评论 #1 — cgmb (2023-08-24T06:23:37Z)

I think I made the exact same mistakes when following the instructions.

> `The following signatures were invalid: EXPKEYSIG 9386B48A1A693C5C James Adrian Edwards (ROCm Release Manager) <JamesAdrian.Edwards@amd.com>`

The problem might be that you are missing `signed-by=/etc/apt/keyrings/rocm.gpg` in `/etc/apt/sources.list.d/amdgpu.list` or `/etc/apt/sources.list.d/rocm.list`. That didn't used to be necessary, so if you just updated the repo version number on an old rocm.list file, I think it results in that error.

> I tried to verify the key and got
> 
> ```
> sha1sum /etc/apt/keyrings/rocm.gpg 
> ececf5eea22ced391975f46ba3e11ad58a12c794  /etc/apt/keyrings/rocm.gpg
> ```
> which is different from 73f5d8100de6048aa38a8b84cd9a87f05177d208 mentioned in https://rocm.docs.amd.com/en/latest/deploy/linux/os-native/install.html

That is the sha1sum of `/etc/apt/keyrings/rocm.gpg`, but the instructions say `73f5d8100de6048aa38a8b84cd9a87f05177d208` is the sha1sum of rocm.gpg.key. It is confusing because if you follow the download instructions, rocm.gpg.key is streamed directly into `gpg --dearmor`, so it doesn't exist on disk for you to verify. I was confused by this too, but you have the correct sha1sum for rocm.gpg.

---

### 评论 #2 — Xdavius (2023-09-07T13:16:39Z)

Up please (error on Opensuse TW too)

1 nouveau paquet à installer.
Taille de téléchargement totale : 23,3 KiB. Déjà en cache : 0 B. Après l'opération, 41,6 KiB d'espace disque
supplémentaire sera utilisé.
Continue? [o/n/v/...? affiche toutes les options] (o): 
Récupération : amdgpu-install-5.5.50503-1620033.noarch (Cache local des fichiers RPM)     (1/1),  23,3 KiB    
amdgpu-install-5.5.50503-1.noarch.rpm:
    Header V4 RSA/SHA512 Signature, key ID 9386b48a1a693c5c: NOKEY

attention : /var/tmp/zypp.CI50Ze/zypper/_tmpRPMcache_/%CLI%/amdgpu-install-5.5.50503-1.noarch.rpm: Entête V4 RSA/SHA512 Signature, clé ID 1a693c5c: NOKEY
Recherche de la clé gpg 1A693C5C dans le cache /var/cache/zypp/pubkeys.
Le dépôt Cache local des fichiers RPM ne définie pas d'URL 'gpgkey=' additionnelles.
amdgpu-install-5.5.50503-1620033.noarch (Cache local des fichiers RPM): Échec de la vérification de la signature [4-La clé publique des signatures n'est pas disponible]
Abandonner, réessayer, ignorer ? [a/r/i] (a): r
Récupération : amdgpu-install-5.5.50503-1620033.noarch (Cache local des fichiers RPM)     (0/1),  23,3 KiB    
amdgpu-install-5.5.50503-1.noarch.rpm:
    Header V4 RSA/SHA512 Signature, key ID 9386b48a1a693c5c: NOKEY

Recherche de la clé gpg 1A693C5C dans le cache /var/cache/zypp/pubkeys.
Le dépôt Cache local des fichiers RPM ne définie pas d'URL 'gpgkey=' additionnelles.
amdgpu-install-5.5.50503-1620033.noarch (Cache local des fichiers RPM): Échec de la vérification de la signature [4-La clé publique des signatures n'est pas disponible]




---
