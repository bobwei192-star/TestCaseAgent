# amd-smi does not work

> **Issue #4216**
> **状态**: closed
> **创建时间**: 2025-01-02T20:47:57Z
> **更新时间**: 2025-03-21T06:04:43Z
> **关闭时间**: 2025-01-10T16:24:33Z
> **作者**: readmodifywrite
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4216

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

The amd-smi command does not work after installing rocm.

LM 22.  rocm 6.2.1.

Error message:

```bash
amd-smi --help
/opt/rocm-6.2.1/libexec/amdsmi_cli/BDF.py:126: SyntaxWarning: invalid escape sequence '\.'
  bdf_regex = "(?:[0-6]?[0-9a-fA-F]{1,4}:)?[0-2]?[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}\.[0-7]"
Still couldn't import 'amdsmi related scripts'. Make sure it's installed in /usr/bin/../libexec/amdsmi_cli
```

I've already done a reinstall via amdgpu_install.

### Operating System

LM 22

### CPU

AMD Ryzen 9 7950X3D

### GPU

AMD Navi 33 [Radeon RX 7600/7600 XT/7600M XT/7600S/7700S / PRO     W7600]

### ROCm Version

ROCm 6.2.1

### ROCm Component

amdsmi

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — readmodifywrite (2025-01-02T20:53:54Z)

Note that amdsmi_cli is not installed to /usr/bin/../libexec/amdsmi_cli

However, by manually copying it to that directory, nothing happens.  amd-smi still cannot find it.

---

### 评论 #2 — ppanchad-amd (2025-01-02T21:19:17Z)

Hi @readmodifywrite. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #3 — tcgu-amd (2025-01-02T21:37:22Z)

Hi @readmodifywrite, thanks for reaching out! Looks like your amd-smi is not installed in the correct path. I would first double check to see if virtual environments such as venv or conda are disabled. I would then try installing amd-smi directly from its directory first:

```
cd /opt/rocm/share/amd_smi
python3 -m pip install .
```

If that didn't work, I would then check to see if the `/usr/bin/amd-smi` symbolic link is pointing to the correct amdsmi_cli.py

```
cd /usr/bin && namei amd-smi
```

It should show linkage to the corresponding file at `/opt/rocm/libexec/amdsmi_cli/amdsmi_cli.py`

For example, on latest 6.3.1 it shows

```
tim@ubt-24:/usr/bin$ namei amd-smi
f: amd-smi
 l amd-smi -> /etc/alternatives/amd-smi
   d /
   d etc
   d alternatives
   l amd-smi -> /opt/rocm-6.3.1/bin/amd-smi
     d /
     d opt
     d rocm-6.3.1
     d bin
     l amd-smi -> ../libexec/amdsmi_cli/amdsmi_cli.py
       d ..
       d libexec
       d amdsmi_cli
       - amdsmi_cli.py
```
If it doesn't show something like this, please share the output and we can help you investigate further :)

Hope this helps.

Thanks! 

---

### 评论 #4 — readmodifywrite (2025-01-09T21:05:09Z)

Hi there!

Installing amd-smi using my system Python (which isn't recommended but is so often necessary):
```bash
jeremy@saturn2 /o/r/s/amd_smi [1]> python3 -m pip install . --break-system-packages
Defaulting to user installation because normal site-packages is not writeable
Processing /opt/rocm-6.2.1/share/amd_smi
  Installing build dependencies ... done
  Getting requirements to build wheel ... error
  error: subprocess-exited-with-error
  
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> [24 lines of output]
      /tmp/pip-build-env-c32ohmr7/overlay/local/lib/python3.12/dist-packages/setuptools/config/_apply_pyprojecttoml.py:74: _MissingDynamic: `classifiers` defined outside of `pyproject.toml` is ignored.
      !!
      
              ********************************************************************************
              The following seems to be defined outside of `pyproject.toml`:
      
              `classifiers = ['Programming Language :: Python :: 3']`
      
              According to the spec (see the link below), however, setuptools CANNOT
              consider this value unless `classifiers` is listed as `dynamic`.
      
              https://packaging.python.org/en/latest/specifications/pyproject-toml/#declaring-project-metadata-the-project-table
      
              To prevent this problem, you can list `classifiers` under `dynamic` or alternatively
              remove the `[project]` table from your file and rely entirely on other means of
              configuration.
              ********************************************************************************
      
      !!
        _handle_missing_dynamic(dist, project_table)
      /tmp/pip-build-env-c32ohmr7/overlay/local/lib/python3.12/dist-packages/setuptools/config/_apply_pyprojecttoml.py:81: SetuptoolsWarning: `install_requires` overwritten in `pyproject.toml` (dependencies)
        corresp(dist, value, root_dir)
      running egg_info
      error: Cannot update time stamp of directory 'amdsmi.egg-info'
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: subprocess-exited-with-error

× Getting requirements to build wheel did not run successfully.
│ exit code: 1
╰─> See above for output.

note: This error originates from a subprocess, and is likely not a problem with pip.
```

Ok here's what's weird:
It works now anyway, despite the errors!

This must have been some bizarre environment issue.  Anyway, thanks for the quick response!  Feel free to close unless you need anything else from me!



---

### 评论 #5 — tcgu-amd (2025-01-09T21:44:32Z)

I am glad it works now! I will close this issue then. Thanks

---

### 评论 #6 — hapasa (2025-03-21T06:03:14Z)

I ran into same with ROCm  6.3.3, but for me the issue was that the python running amdsmi_cli.py did not find yaml.
The import exception handling it not specific enough, so missing yaml module shows up as this issue.

Simple fix was to run `pip install pyyaml` and amd-smi started to work

---
