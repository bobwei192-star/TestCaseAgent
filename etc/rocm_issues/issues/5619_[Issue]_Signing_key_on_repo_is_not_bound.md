# [Issue]: Signing key on repo is not bound

> **Issue #5619**
> **状态**: closed
> **创建时间**: 2025-11-03T19:42:31Z
> **更新时间**: 2025-11-04T19:10:31Z
> **关闭时间**: 2025-11-04T19:10:31Z
> **作者**: loidor
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5619

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

sudo apt update gives:

```
Warning: https://repo.radeon.com/rocm/6.4.4/ubuntu/dists/noble/InRelease: Policy will reject signature within a year, see --audit for details
Audit: https://repo.radeon.com/amdgpu/6.4.4/ubuntu/dists/noble/InRelease: Sub-process /usr/bin/sqv returned an error code (1), error message is:
   Signing key on CA8BB4727A47B4D09B4EE8969386B48A1A693C5C is not bound:
              No binding signature at time 2025-09-18T22:16:53Z
     because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
     because: SHA1 is not considered secure since 2026-02-01T00:00:00Z
```

### Operating System

Irrelevant

### CPU

Irrelevant

### GPU

Irrelevant

### ROCm Version

Irrelevant

### ROCm Component

_No response_

### Steps to Reproduce

run `sudo apt update`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2025-11-04T17:12:30Z)

Wasn't able to repro this on my end but it looks like by default my system (Ubuntu 24.04) uses `gpgv` and not `sqv` - are you on Debian? Could you also share the output of `apt-config dump | grep APT`? 

---

### 评论 #2 — loidor (2025-11-04T17:25:04Z)

Yes, Trixie. 

EDIT: More specifically, crunchbang++. But that's pretty much just debian with openbox.

Here's the output:

```
APT "";
APT::Architecture "amd64";
APT::Build-Essential "";
APT::Build-Essential:: "build-essential";
APT::Install-Recommends "true";
APT::Install-Suggests "0";
APT::Key "";
APT::Key::Assert-Pubkey-Algo ">=rsa2048,ed25519,ed448,nistp256,nistp384,nistp512,brainpoolP256r1,brainpoolP320r1,brainpoolP384r1,brainpoolP512r1,secp256k1";
APT::Key::Assert-Pubkey-Algo::Next ">=rsa2048,ed25519,ed448,nistp256,nistp384,nistp512";
APT::Key::Assert-Pubkey-Algo::Future ">=rsa3072,ed25519,ed448";
APT::Sandbox "";
APT::Sandbox::User "_apt";
APT::Authentication "";
APT::Authentication::TrustCDROM "true";
APT::NeverAutoRemove "";
APT::NeverAutoRemove:: "^firmware-linux.*";
APT::NeverAutoRemove:: "^linux-firmware$";
APT::NeverAutoRemove:: "^linux-image-[a-z0-9]*$";
APT::NeverAutoRemove:: "^linux-image-[a-z0-9]*-[a-z0-9]*$";
APT::VersionedKernelPackages "";
APT::VersionedKernelPackages:: "linux-.*";
APT::VersionedKernelPackages:: "kfreebsd-.*";
APT::VersionedKernelPackages:: "gnumach-.*";
APT::VersionedKernelPackages:: ".*-modules";
APT::VersionedKernelPackages:: ".*-kernel";
APT::Never-MarkAuto-Sections "";
APT::Never-MarkAuto-Sections:: "metapackages";
APT::Never-MarkAuto-Sections:: "tasks";
APT::Move-Autobit-Sections "";
APT::Move-Autobit-Sections:: "oldlibs";
APT::Periodic "";
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::AutocleanInterval "7";
APT::Update "";
APT::Update::Post-Invoke-Success "";
APT::Update::Post-Invoke-Success:: "if /usr/bin/test -w /var/cache/swcatalog -a -e /usr/bin/appstreamcli; then appstreamcli refresh --source=os > /dev/null || true; fi";
APT::Solver "3.0";
APT::Architectures "";
APT::Architectures:: "amd64";
APT::Compressor "";
APT::Compressor::. "";
APT::Compressor::.::Name ".";
APT::Compressor::.::Extension "";
APT::Compressor::.::Binary "";
APT::Compressor::.::Cost "0";
APT::Compressor::zstd "";
APT::Compressor::zstd::Name "zstd";
APT::Compressor::zstd::Extension ".zst";
APT::Compressor::zstd::Binary "zstd";
APT::Compressor::zstd::Cost "60";
APT::Compressor::zstd::CompressArg "";
APT::Compressor::zstd::CompressArg:: "-6";
APT::Compressor::zstd::UncompressArg "";
APT::Compressor::zstd::UncompressArg:: "-d";
APT::Compressor::lz4 "";
APT::Compressor::lz4::Name "lz4";
APT::Compressor::lz4::Extension ".lz4";
APT::Compressor::lz4::Binary "false";
APT::Compressor::lz4::Cost "50";
APT::Compressor::gzip "";
APT::Compressor::gzip::Name "gzip";
APT::Compressor::gzip::Extension ".gz";
APT::Compressor::gzip::Binary "gzip";
APT::Compressor::gzip::Cost "100";
APT::Compressor::gzip::CompressArg "";
APT::Compressor::gzip::CompressArg:: "-6n";
APT::Compressor::gzip::UncompressArg "";
APT::Compressor::gzip::UncompressArg:: "-d";
APT::Compressor::xz "";
APT::Compressor::xz::Name "xz";
APT::Compressor::xz::Extension ".xz";
APT::Compressor::xz::Binary "xz";
APT::Compressor::xz::Cost "200";
APT::Compressor::xz::CompressArg "";
APT::Compressor::xz::CompressArg:: "-6";
APT::Compressor::xz::UncompressArg "";
APT::Compressor::xz::UncompressArg:: "-d";
APT::Compressor::bzip2 "";
APT::Compressor::bzip2::Name "bzip2";
APT::Compressor::bzip2::Extension ".bz2";
APT::Compressor::bzip2::Binary "bzip2";
APT::Compressor::bzip2::Cost "300";
APT::Compressor::bzip2::CompressArg "";
APT::Compressor::bzip2::CompressArg:: "-6";
APT::Compressor::bzip2::UncompressArg "";
APT::Compressor::bzip2::UncompressArg:: "-d";
APT::Compressor::lzma "";
APT::Compressor::lzma::Name "lzma";
APT::Compressor::lzma::Extension ".lzma";
APT::Compressor::lzma::Binary "xz";
APT::Compressor::lzma::Cost "400";
APT::Compressor::lzma::CompressArg "";
APT::Compressor::lzma::CompressArg:: "--format=lzma";
APT::Compressor::lzma::CompressArg:: "-6";
APT::Compressor::lzma::UncompressArg "";
APT::Compressor::lzma::UncompressArg:: "--format=lzma";
APT::Compressor::lzma::UncompressArg:: "-d";
Binary::apt-cdrom::APT "";
Binary::apt-cdrom::APT::Internal "";
Binary::apt-cdrom::APT::Internal::OpProgress "";
Binary::apt-cdrom::APT::Internal::OpProgress::EraseLines "0";
Version::1.2::APT "";
Version::1.2::APT::Color "1";
Version::1.2::APT::Keep-Downloaded-Packages "0";
Version::3.0::APT "";
Version::3.0::APT::Output-Version "30";
Version::1.1::APT "";
Version::1.1::APT::Cache "";
Version::1.1::APT::Cache::Show "";
Version::1.1::APT::Cache::Show::Version "2";
Version::1.1::APT::Cache::AllVersions "0";
Version::1.1::APT::Cache::ShowVirtuals "1";
Version::1.1::APT::Cache::Search "";
Version::1.1::APT::Cache::Search::Version "2";
Version::1.1::APT::Cache::ShowDependencyType "1";
Version::1.1::APT::Cache::ShowVersion "1";
Version::1.1::APT::Get "";
Version::1.1::APT::Get::Upgrade-Allow-New "1";
Version::1.1::APT::Cmd "";
Version::1.1::APT::Cmd::Show-Update-Stats "1";
Version::1.5::APT "";
Version::1.5::APT::Get "";
Version::1.5::APT::Get::Update "";
Version::1.5::APT::Get::Update::InteractiveReleaseInfoChanges "1";
Version::2.0::APT "";
Version::2.0::APT::Cmd "";
Version::2.0::APT::Cmd::Pattern-Only "1";
Version::1.21::APT "";
Version::1.21::APT::Solver "3.0";
Version::2.11::APT "";
Version::2.11::APT::Solver "3.0";
Version::3.1::APT "";
Version::3.1::APT::Solver "3.0";
```

---

### 评论 #3 — harkgill-amd (2025-11-04T18:37:37Z)

I believe the stricter signing policy on Debian is the result of 
```
APT::Key::Assert-Pubkey-Algo ">=rsa2048,ed25519,ed448,nistp256,nistp384,nistp512,brainpoolP256r1,brainpoolP320r1,brainpoolP384r1,brainpoolP512r1,secp256k1";
APT::Key::Assert-Pubkey-Algo::Next ">=rsa2048,ed25519,ed448,nistp256,nistp384,nistp512";
APT::Key::Assert-Pubkey-Algo::Future ">=rsa3072,ed25519,ed448";
```
Was able to repro this issue with the official Trixie docker image + ROCm 6.4.4. With the latest ROCm 7.1 release I don't see any warnings - for context, we only officially started supporting Debian 13 in ROCm 7+ which is likely why the signing issues are resolved there. Could you try upgrading on your side as well to see if the issue is resolved with the latest ROCm release?

---

### 评论 #4 — loidor (2025-11-04T19:10:31Z)

That fixed it! Never thought about the repos being version specific (i.e. one for 6.4.4, another one for 7.1).

Thanks for solving a quite minor but likewise annoying problem 😄 

---
