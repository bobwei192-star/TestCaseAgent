# [Feature]:  setup.py build with hipcc  always fall back to gcc/g++

> **Issue #3918**
> **状态**: closed
> **创建时间**: 2024-10-18T06:27:07Z
> **更新时间**: 2024-10-23T07:16:31Z
> **关闭时间**: 2024-10-23T07:16:30Z
> **作者**: ZJLi2013
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3918

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

hi, rocm expert, I am trying to build a rocm lib as an python package with setuptools. I tried a few ways, neither works, can someone give a hint ?


```py
ext_modules = [
    CppExtension(
        "mylib",
        [$csrc],
        include_dirs = ["/opt/rocm/include/"],
        library_dirs = ["/opt/rocm/lib/"],
        libraries = ["hiprtc", "hipblas"],
        extra_compile_args={
            "hipcc": hipcc_flags,
        },
        extra_link_args = ["-L/opt/rocm/lib", "-lhiprtc", "-lhipblas"], #  Linking HIP runtime and HIPBL
    )
]
```

the build is always fallback to `c++/gcc`, rather `hipcc` as I wanted.  also tried to replace `CppExtention` with `CUDAExtention`, neither works.

 [torch issue](https://github.com/pytorch/pytorch/pull/35897), looks CppExtension has supported for hipcc, or do we need a customized hipcppExtension ?

Thanks again
David 




### Operating System

Ubuntu 22.04

### GPU

mi300

### ROCm Component

6.2.2

---

## 评论 (7 条)

### 评论 #1 — ZJLi2013 (2024-10-20T04:28:29Z)

some interesting founding's:

the rocm/pytorch image: rocm/pytorch:rocm6.2_ubuntu22.04_py3.9_pytorch_release_2.2.1 has missing `torch.utils.cpp_extension` , and this image `rocm/pytorch:rocm6.2_ubuntu22.04_py3.10_pytorch_release_2.3.0` has this module correctly. 

wonder what may leading to some modules from pytorch missed in the rocm/pytorch image ?





---

### 评论 #2 — ZJLi2013 (2024-10-20T04:43:06Z)

I am now assuming that build rocm as extension for python package is not default supported, so I added manually build_extension for hip:

```py
class HIPBuildExt(BuildExtension):
    def build_extensions(self):
        for ext in self.extensions:
            self.build_extension(ext)

    # enforce manually compile with hipcc 
    def build_extension(self, ext):
        output_path = self.get_ext_fullpath(ext.name)
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_path):
            os.makedirs(output_dir)
        
        hip_compile_flags = ext.extra_compile_args
        hip_link_flags = ['-shared', '-fPIC'] + ext.extra_link_args
        include_dirs = [f'-I{dir}' for dir in ext.include_dirs]        

        # Compile HIP source files manually
        object_files = []
        for source in ext.sources:
            obj_file = source.replace(".cpp", ".o")
            compile_command = ['hipcc', '-c', '-o', obj_file, source] + hip_compile_flags + include_dirs
            print(f"Compiling {source} -> {obj_file}")
            subprocess.check_call(compile_command)
            object_files.append(obj_file)

        # Link object files to create the shared library
        link_command = ['hipcc', '-o', output_path] + object_files + hip_link_flags
        print(f"Linking to create {output_path}")
        subprocess.check_call(link_command)
``` 

it looks work as expect, I can see the logs:

```yml
execute:/opt/rocm/lib/llvm/bin/clang++  --offload-arch=gfx942 --offload-arch=gfx942 --offload-arch=gfx942 --offload-arch=gfx942 --offload-arch=gfx942 --offload-arch=gfx942 --offload-arch=gfx942 --offload-arch=gfx942 -O3  -c -o "csrc/ops.o" -x hip csrc/ops.cpp -fPIC -DENABLE_BF16 -I/opt/rocm/include/ -I\[\'/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include\',\ \'/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/torch/csrc/api/include\',\ \'/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/TH\',\ \'/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/THC\'\] -I/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include -I/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/torch/csrc/api/include -I/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/TH -I/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/THC
``` 

but then it gave me another error:

```yml

In file included from /opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/torch/extension.h:9:
In file included from /opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/torch/csrc/api/include/torch/python.h:8:
In file included from /opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/torch/csrc/Device.h:4:
/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/torch/csrc/python_headers.h:12:10: fatal error: 'Python.h' file not found
   12 | #include <Python.h>
      |          ^~~~~~~~~~
1 error generated when compiling for gfx942.
``` 

the runtime image is : `rocm/pytorch:rocm6.2_ubuntu22.04_py3.10_pytorch_release_2.3.0`, I am expecting all torch/python depends should be ready in the image, but looks there are some broken dependents ?

how should I fix then ?




 

---

### 评论 #3 — tcgu-amd (2024-10-21T20:00:56Z)

Hi @ZJLi2013 thank you for reaching out! Have you installed python dev with
```
sudo apt-get install python3-dev
```
command?

Thanks!

---

### 评论 #4 — ZJLi2013 (2024-10-22T01:56:01Z)

> Hi @ZJLi2013 thank you for reaching out! Have you installed python dev with
> 
> ```
> sudo apt-get install python3-dev
> ```
> 
> command?
> 
> Thanks!

yes,  python3-dev installed. 

looks it's a build issue, has to manually add python header and lib for rocm extension build

```py
include_dirs = ["/opt/rocm/include/"] + ["/opt/conda/envs/py_3.10/include/python3.10/"],
extra_link_args = [ hip_link_libs , "-L/opt/conda/envs/py_3.10/lib/', '-lpython3"]
```

the `Python.h` not found can be fixed manually now.




---

### 评论 #5 — ZJLi2013 (2024-10-22T02:04:44Z)

it's appreciated if you can provide an sample for building rocm as torch cpp extension.

---

### 评论 #6 — tcgu-amd (2024-10-22T14:16:46Z)

Hi @ZJLi2013, apologies for not mentioning this earlier, but building a HIP extension is by default supported by torch.util.cpp_extension.py under the CUDA extension method (see https://github.com/ROCm/pytorch/blob/main/torch/utils/cpp_extension.py#L1117). Would you mind giving it a try to see if it solves any issues? Thanks!

---

### 评论 #7 — ZJLi2013 (2024-10-23T07:16:30Z)

> Hi @ZJLi2013, apologies for not mentioning this earlier, but building a HIP extension is by default supported by torch.util.cpp_extension.py under the CUDA extension method (see https://github.com/ROCm/pytorch/blob/main/torch/utils/cpp_extension.py#L1117). Would you mind giving it a try to see if it solves any issues? Thanks!

verified,  cudaExtension does work for hip code, and these include/lib dependencies are added by `Extension` class itself:

```yml
1. default library_dirs: [ "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/lib", "/opt/rocm/lib"]
2. default libraries: ["c10", "torch", "torch_cpu", "torch_python", "amdhip64", "c10_hip", "torch_hip"]
3. default include_dirs: [
            "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include", 
            "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/torch/csrc/api/include",
            "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/TH",  # not in rocm/torch
            "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/THC", # not in rocm/torch
            "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/include/THH",
            "/opt/rocm/include" ] 
```

so it's well defined.

the only reminder is need to use `*.hip` as suffix, if else the compiler fall back to `cxx`, as the first time I observed.

thanks a lot, will close this issue


---
