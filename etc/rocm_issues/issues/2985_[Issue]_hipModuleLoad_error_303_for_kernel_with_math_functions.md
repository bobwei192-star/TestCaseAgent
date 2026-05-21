# [Issue]: hipModuleLoad error 303 for kernel with math functions

> **Issue #2985**
> **状态**: closed
> **创建时间**: 2024-03-26T22:04:10Z
> **更新时间**: 2024-04-12T17:21:00Z
> **关闭时间**: 2024-04-12T17:20:59Z
> **作者**: fwinter
> **标签**: Under Investigation, AMD Instinct MI250X, ROCm 5.6.0
> **URL**: https://github.com/ROCm/ROCm/issues/2985

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI250X** (颜色: #ededed)
- **ROCm 5.6.0** (颜色: #ededed)

## 描述

### Problem Description

My application uses the llvm shipped with ROCm (/opt/rocm/llvm) to build amdgpu kernels. Later calls codegen and ld.lld to create a shared object, after which HIP loads the linked module. This has worked fine prior to ROCm 5.6.0. Since that version only kernels without math functions work (kernel.ll in the reproducer). If a kernel calls a math function (mathkernel.ll) the module loader returns error 303. I have compiled a reproducer.

[rocm_load.TGZ](https://github.com/ROCm/ROCm/files/14765015/rocm_load.TGZ)
 

```
$ make test
/opt/rocm-5.6.0/llvm/bin/llvm-as < kernel.ll > kernel.bc
/opt/rocm-5.6.0/llvm/bin/clang -c -target amdgcn-amd-amdhsa -mcpu=gfx90a kernel.bc -o kernel.o
warning: overriding the module target triple with amdgcn-amd-amdhsa [-Woverride-module]
1 warning generated.
/opt/rocm-5.6.0/llvm/bin/ld.lld -shared kernel.o -o kernel.so
/opt/rocm-5.6.0/llvm/bin/llvm-as < mathkernel.ll > mathkernel.bc
/opt/rocm-5.6.0/llvm/bin/llvm-link mathkernel.bc /opt/rocm-5.6.0/llvm/lib/libomptarget-old-amdgpu-gfx90a.bc /opt/rocm-5.6.0/amdgcn/bitcode/ocml.bc /opt/rocm-5.6.0/amdgcn/bitcode/oclc_finite_only_off.bc /opt/rocm-5.6.0/amdgcn/bitcode/oclc_isa_version_90a.bc /opt/rocm-5.6.0/amdgcn/bitcode/oclc_unsafe_math_off.bc /opt/rocm-5.6.0/amdgcn/bitcode/oclc_daz_opt_off.bc /opt/rocm-5.6.0/amdgcn/bitcode/oclc_correctly_rounded_sqrt_on.bc -o mathkernel-linked.bc
/opt/rocm-5.6.0/llvm/bin/clang -c -target amdgcn-amd-amdhsa -mcpu=gfx90a mathkernel-linked.bc -o mathkernel-linked.o
/opt/rocm-5.6.0/llvm/bin/ld.lld -shared mathkernel-linked.o -o mathkernel-linked.so
/opt/rocm-5.6.0/bin/hipcc -o host host.cc
host.cc:15:11: warning: 'hipCtxCreate' is deprecated: This API is marked as deprecated and may not be supported in future releases. For more details please refer https://github.com/ROCm-Developer-Tools/HIP/blob/master/docs/markdown/hip_deprecated_api_list.md [-Wdeprecated-declarations]
    err = hipCtxCreate(&ctx, hipDeviceScheduleAuto, device);
          ^
/opt/rocm-5.6.0/include/hip/hip_runtime_api.h:4616:1: note: 'hipCtxCreate' has been explicitly marked deprecated here
DEPRECATED(DEPRECATED_MSG)
^
/opt/rocm-5.6.0/include/hip/hip_runtime_api.h:494:41: note: expanded from macro 'DEPRECATED'
#define DEPRECATED(msg) __attribute__ ((deprecated(msg)))
                                        ^
1 warning generated when compiling for gfx90a.
host.cc:15:11: warning: 'hipCtxCreate' is deprecated: This API is marked as deprecated and may not be supported in future releases. For more details please refer https://github.com/ROCm-Developer-Tools/HIP/blob/master/docs/markdown/hip_deprecated_api_list.md [-Wdeprecated-declarations]
    err = hipCtxCreate(&ctx, hipDeviceScheduleAuto, device);
          ^
/opt/rocm-5.6.0/include/hip/hip_runtime_api.h:4616:1: note: 'hipCtxCreate' has been explicitly marked deprecated here
DEPRECATED(DEPRECATED_MSG)
^
/opt/rocm-5.6.0/include/hip/hip_runtime_api.h:494:41: note: expanded from macro 'DEPRECATED'
#define DEPRECATED(msg) __attribute__ ((deprecated(msg)))
                                        ^
1 warning generated when compiling for host.
./host
hipSetdevice Err: 0
hipInit Err: 0
hipCtxCreate Err: 0
hipModuleLoad Err: 0
hipModuleGetFunction Err: 0
math hipModuleLoad Err: 303
math hipModuleGetFunction Err: 500

```

### Operating System

Linux frontier07423 5.14.21-150400.24.46_12.0.83-cray_shasta_c

### CPU

AMD EPYC 7A53 64-Core Processor

### GPU

AMD Instinct MI250X

### ROCm Version

ROCm 5.6.0

### ROCm Component

llvm-project

### Steps to Reproduce

Makefile:

```
GCN=90a

EXTRA=\
${ROCM_PATH}/llvm/lib/libomptarget-new-amdgpu-gfx${GCN}.bc \
${ROCM_PATH}/amdgcn/bitcode/ocml.bc \
${ROCM_PATH}/amdgcn/bitcode/oclc_finite_only_off.bc \
${ROCM_PATH}/amdgcn/bitcode/oclc_isa_version_${GCN}.bc \
${ROCM_PATH}/amdgcn/bitcode/oclc_unsafe_math_off.bc \
${ROCM_PATH}/amdgcn/bitcode/oclc_daz_opt_off.bc \
${ROCM_PATH}/amdgcn/bitcode/oclc_correctly_rounded_sqrt_on.bc

%.bc: %.ll
	${ROCM_PATH}/llvm/bin/llvm-as < $< > $@


host: host.cc
	${ROCM_PATH}/bin/hipcc -o $@ $<


kernel.o: kernel.bc
	${ROCM_PATH}/llvm/bin/clang -c -target amdgcn-amd-amdhsa -mcpu=gfx${GCN} $< -o $@

kernel.so: kernel.o
	${ROCM_PATH}/llvm/bin/ld.lld -shared $< -o $@




mathkernel-linked.bc: mathkernel.bc ${EXTRA}
	${ROCM_PATH}/llvm/bin/llvm-link $^ -o $@

mathkernel-linked.o: mathkernel-linked.bc
	${ROCM_PATH}/llvm/bin/clang -c -target amdgcn-amd-amdhsa -mcpu=gfx${GCN} $< -o $@

mathkernel-linked.so: mathkernel-linked.o
	${ROCM_PATH}/llvm/bin/ld.lld -shared $< -o $@


test: kernel.so mathkernel-linked.so host
	./host

clean:
	rm -f *~
	rm -f *.bc
	rm -f *.o
	rm -f *.so
	rm -f host

```

host.cc

```
#include <hip/hip_runtime.h>

int main()
{
    hipModule_t module;
    hipFunction_t kernelFunction;
    hipError_t err;

    int device = 0;
    err = hipSetDevice(device);
    printf("hipSetdevice Err: %d\n", err);
    err = hipInit(0);
    printf("hipInit Err: %d\n", err);
    hipCtx_t ctx;
    err = hipCtxCreate(&ctx, hipDeviceScheduleAuto, device);
    printf("hipCtxCreate Err: %d\n", err);

    // simplekernel
    
    err = hipModuleLoad(&module, "kernel.so");
    printf("hipModuleLoad Err: %d\n", err);

    err = hipModuleGetFunction(&kernelFunction, module, "eval0");
    printf("hipModuleGetFunction Err: %d\n", err);
    hipModuleUnload(module);


    // mathkernel
    
    hipModule_t m_module;
    hipFunction_t m_kernelFunction;

    err = hipModuleLoad(&m_module, "mathkernel-linked.so");
    printf("math hipModuleLoad Err: %d\n", err);

    err = hipModuleGetFunction(&m_kernelFunction, m_module, "gaussian0");
    printf("math hipModuleGetFunction Err: %d\n", err);
    hipModuleUnload(m_module);

    
    return 0;
}

```

kernel.ll

```
; ModuleID = 'module'
source_filename = "module"
target datalayout = "e-p:64:64-p1:64:64-p2:32:32-p3:32:32-p4:64:64-p5:32:32-p6:32:32-i64:64-v16:16-v24:32-v32:32-v48:64-v96:128-v192:256-v256:256-v512:512-v1024:1024-v2048:2048-n32:64-S32-A5-G1-ni:7"

define amdgpu_kernel void @eval0(i32 %arg0, i32 %arg1, i32 %arg2, ptr %arg3, ptr %arg4, ptr %arg5) {
stack:
  br label %afterstack

afterstack:                                       ; preds = %stack
  %0 = call i32 @llvm.amdgcn.workitem.id.x()
  %1 = call i32 @llvm.amdgcn.workgroup.id.x()
  %2 = call i32 @llvm.amdgcn.workgroup.id.y()
  %3 = mul i32 %2, %arg1
  %4 = add nsw i32 %3, %1
  %5 = mul i32 %4, %arg0
  %6 = add nsw i32 %5, %0
  %7 = icmp sge i32 %6, %arg2
  br i1 %7, label %L0, label %L1

L0:                                               ; preds = %afterstack
  ret void

L1:                                               ; preds = %afterstack
  %8 = getelementptr i32, ptr %arg3, i32 %6
  %9 = load i32, ptr %8, align 4
  %10 = add nsw i32 0, %9
  %11 = getelementptr i32, ptr %arg5, i32 %10
  %12 = load i32, ptr %11, align 4
  %13 = add nsw i32 0, %9
  %14 = getelementptr i32, ptr %arg4, i32 %13
  store i32 %12, ptr %14, align 4
  ret void
}

; Function Attrs: nounwind readnone speculatable willreturn
declare i32 @llvm.amdgcn.workitem.id.x() #0

; Function Attrs: nounwind readnone speculatable willreturn
declare i32 @llvm.amdgcn.workgroup.id.x() #0

; Function Attrs: nounwind readnone speculatable willreturn
declare i32 @llvm.amdgcn.workgroup.id.y() #0

attributes #0 = { nounwind readnone speculatable willreturn }

```


mathkernel.ll

```
; ModuleID = 'module'
source_filename = "module"
target datalayout = "e-p:64:64-p1:64:64-p2:32:32-p3:32:32-p4:64:64-p5:32:32-p6:32:32-i64:64-v16:16-v24:32-v32:32-v48:64-v96:128-v192:256-v256:256-v512:512-v1024:1024-v2048:2048-n32:64-S32-A5-G1-ni:7"

define amdgpu_kernel void @gaussian0(i32 %arg0, i32 %arg1, i32 %arg2, ptr %arg3, ptr %arg4, ptr %arg5, ptr %arg6) {
stack:
  br label %afterstack

afterstack:                                       ; preds = %stack
  %0 = call i32 @llvm.amdgcn.workitem.id.x()
  %1 = call i32 @llvm.amdgcn.workgroup.id.x()
  %2 = call i32 @llvm.amdgcn.workgroup.id.y()
  %3 = mul i32 %2, %arg1
  %4 = add nsw i32 %3, %1
  %5 = mul i32 %4, %arg0
  %6 = add nsw i32 %5, %0
  %7 = icmp sge i32 %6, %arg2
  br i1 %7, label %L0, label %L1

L0:                                               ; preds = %afterstack
  ret void

L1:                                               ; preds = %afterstack
  %8 = getelementptr i32, ptr %arg3, i32 %6
  %9 = load i32, ptr %8, align 4
  %10 = add nsw i32 0, %9
  %11 = add nsw i32 589824, %9
  %12 = add nsw i32 65536, %9
  %13 = add nsw i32 655360, %9
  %14 = add nsw i32 131072, %9
  %15 = add nsw i32 720896, %9
  %16 = add nsw i32 196608, %9
  %17 = add nsw i32 786432, %9
  %18 = add nsw i32 262144, %9
  %19 = add nsw i32 851968, %9
  %20 = add nsw i32 327680, %9
  %21 = add nsw i32 917504, %9
  %22 = add nsw i32 393216, %9
  %23 = add nsw i32 983040, %9
  %24 = add nsw i32 458752, %9
  %25 = add nsw i32 1048576, %9
  %26 = add nsw i32 524288, %9
  %27 = add nsw i32 1114112, %9
  %28 = getelementptr double, ptr %arg5, i32 %10
  %29 = load double, ptr %28, align 8
  %30 = getelementptr double, ptr %arg5, i32 %11
  %31 = load double, ptr %30, align 8
  %32 = getelementptr double, ptr %arg5, i32 %12
  %33 = load double, ptr %32, align 8
  %34 = getelementptr double, ptr %arg5, i32 %13
  %35 = load double, ptr %34, align 8
  %36 = getelementptr double, ptr %arg5, i32 %14
  %37 = load double, ptr %36, align 8
  %38 = getelementptr double, ptr %arg5, i32 %15
  %39 = load double, ptr %38, align 8
  %40 = getelementptr double, ptr %arg5, i32 %16
  %41 = load double, ptr %40, align 8
  %42 = getelementptr double, ptr %arg5, i32 %17
  %43 = load double, ptr %42, align 8
  %44 = getelementptr double, ptr %arg5, i32 %18
  %45 = load double, ptr %44, align 8
  %46 = getelementptr double, ptr %arg5, i32 %19
  %47 = load double, ptr %46, align 8
  %48 = getelementptr double, ptr %arg5, i32 %20
  %49 = load double, ptr %48, align 8
  %50 = getelementptr double, ptr %arg5, i32 %21
  %51 = load double, ptr %50, align 8
  %52 = getelementptr double, ptr %arg5, i32 %22
  %53 = load double, ptr %52, align 8
  %54 = getelementptr double, ptr %arg5, i32 %23
  %55 = load double, ptr %54, align 8
  %56 = getelementptr double, ptr %arg5, i32 %24
  %57 = load double, ptr %56, align 8
  %58 = getelementptr double, ptr %arg5, i32 %25
  %59 = load double, ptr %58, align 8
  %60 = getelementptr double, ptr %arg5, i32 %26
  %61 = load double, ptr %60, align 8
  %62 = getelementptr double, ptr %arg5, i32 %27
  %63 = load double, ptr %62, align 8
  %64 = add nsw i32 0, %9
  %65 = add nsw i32 589824, %9
  %66 = add nsw i32 65536, %9
  %67 = add nsw i32 655360, %9
  %68 = add nsw i32 131072, %9
  %69 = add nsw i32 720896, %9
  %70 = add nsw i32 196608, %9
  %71 = add nsw i32 786432, %9
  %72 = add nsw i32 262144, %9
  %73 = add nsw i32 851968, %9
  %74 = add nsw i32 327680, %9
  %75 = add nsw i32 917504, %9
  %76 = add nsw i32 393216, %9
  %77 = add nsw i32 983040, %9
  %78 = add nsw i32 458752, %9
  %79 = add nsw i32 1048576, %9
  %80 = add nsw i32 524288, %9
  %81 = add nsw i32 1114112, %9
  %82 = getelementptr double, ptr %arg6, i32 %64
  %83 = load double, ptr %82, align 8
  %84 = getelementptr double, ptr %arg6, i32 %65
  %85 = load double, ptr %84, align 8
  %86 = getelementptr double, ptr %arg6, i32 %66
  %87 = load double, ptr %86, align 8
  %88 = getelementptr double, ptr %arg6, i32 %67
  %89 = load double, ptr %88, align 8
  %90 = getelementptr double, ptr %arg6, i32 %68
  %91 = load double, ptr %90, align 8
  %92 = getelementptr double, ptr %arg6, i32 %69
  %93 = load double, ptr %92, align 8
  %94 = getelementptr double, ptr %arg6, i32 %70
  %95 = load double, ptr %94, align 8
  %96 = getelementptr double, ptr %arg6, i32 %71
  %97 = load double, ptr %96, align 8
  %98 = getelementptr double, ptr %arg6, i32 %72
  %99 = load double, ptr %98, align 8
  %100 = getelementptr double, ptr %arg6, i32 %73
  %101 = load double, ptr %100, align 8
  %102 = getelementptr double, ptr %arg6, i32 %74
  %103 = load double, ptr %102, align 8
  %104 = getelementptr double, ptr %arg6, i32 %75
  %105 = load double, ptr %104, align 8
  %106 = getelementptr double, ptr %arg6, i32 %76
  %107 = load double, ptr %106, align 8
  %108 = getelementptr double, ptr %arg6, i32 %77
  %109 = load double, ptr %108, align 8
  %110 = getelementptr double, ptr %arg6, i32 %78
  %111 = load double, ptr %110, align 8
  %112 = getelementptr double, ptr %arg6, i32 %79
  %113 = load double, ptr %112, align 8
  %114 = getelementptr double, ptr %arg6, i32 %80
  %115 = load double, ptr %114, align 8
  %116 = getelementptr double, ptr %arg6, i32 %81
  %117 = load double, ptr %116, align 8
  %118 = add nsw i32 0, %9
  %119 = add nsw i32 589824, %9
  %120 = add nsw i32 65536, %9
  %121 = add nsw i32 655360, %9
  %122 = add nsw i32 131072, %9
  %123 = add nsw i32 720896, %9
  %124 = add nsw i32 196608, %9
  %125 = add nsw i32 786432, %9
  %126 = add nsw i32 262144, %9
  %127 = add nsw i32 851968, %9
  %128 = add nsw i32 327680, %9
  %129 = add nsw i32 917504, %9
  %130 = add nsw i32 393216, %9
  %131 = add nsw i32 983040, %9
  %132 = add nsw i32 458752, %9
  %133 = add nsw i32 1048576, %9
  %134 = add nsw i32 524288, %9
  %135 = add nsw i32 1114112, %9
  %136 = fmul double %83, 0x401921FB54411744
  %137 = call double @cos(double %136)
  %138 = call double @sin(double %136)
  %139 = call double @log(double %29)
  %140 = fmul double -2.000000e+00, %139
  %141 = call double @sqrt(double %140)
  %142 = fmul double %141, %137
  %143 = getelementptr double, ptr %arg4, i32 %118
  store double %142, ptr %143, align 8
  %144 = fmul double %141, %138
  %145 = getelementptr double, ptr %arg4, i32 %119
  store double %144, ptr %145, align 8
  %146 = fmul double %87, 0x401921FB54411744
  %147 = call double @cos(double %146)
  %148 = call double @sin(double %146)
  %149 = call double @log(double %33)
  %150 = fmul double -2.000000e+00, %149
  %151 = call double @sqrt(double %150)
  %152 = fmul double %151, %147
  %153 = getelementptr double, ptr %arg4, i32 %120
  store double %152, ptr %153, align 8
  %154 = fmul double %151, %148
  %155 = getelementptr double, ptr %arg4, i32 %121
  store double %154, ptr %155, align 8
  %156 = fmul double %91, 0x401921FB54411744
  %157 = call double @cos(double %156)
  %158 = call double @sin(double %156)
  %159 = call double @log(double %37)
  %160 = fmul double -2.000000e+00, %159
  %161 = call double @sqrt(double %160)
  %162 = fmul double %161, %157
  %163 = getelementptr double, ptr %arg4, i32 %122
  store double %162, ptr %163, align 8
  %164 = fmul double %161, %158
  %165 = getelementptr double, ptr %arg4, i32 %123
  store double %164, ptr %165, align 8
  %166 = fmul double %95, 0x401921FB54411744
  %167 = call double @cos(double %166)
  %168 = call double @sin(double %166)
  %169 = call double @log(double %41)
  %170 = fmul double -2.000000e+00, %169
  %171 = call double @sqrt(double %170)
  %172 = fmul double %171, %167
  %173 = getelementptr double, ptr %arg4, i32 %124
  store double %172, ptr %173, align 8
  %174 = fmul double %171, %168
  %175 = getelementptr double, ptr %arg4, i32 %125
  store double %174, ptr %175, align 8
  %176 = fmul double %99, 0x401921FB54411744
  %177 = call double @cos(double %176)
  %178 = call double @sin(double %176)
  %179 = call double @log(double %45)
  %180 = fmul double -2.000000e+00, %179
  %181 = call double @sqrt(double %180)
  %182 = fmul double %181, %177
  %183 = getelementptr double, ptr %arg4, i32 %126
  store double %182, ptr %183, align 8
  %184 = fmul double %181, %178
  %185 = getelementptr double, ptr %arg4, i32 %127
  store double %184, ptr %185, align 8
  %186 = fmul double %103, 0x401921FB54411744
  %187 = call double @cos(double %186)
  %188 = call double @sin(double %186)
  %189 = call double @log(double %49)
  %190 = fmul double -2.000000e+00, %189
  %191 = call double @sqrt(double %190)
  %192 = fmul double %191, %187
  %193 = getelementptr double, ptr %arg4, i32 %128
  store double %192, ptr %193, align 8
  %194 = fmul double %191, %188
  %195 = getelementptr double, ptr %arg4, i32 %129
  store double %194, ptr %195, align 8
  %196 = fmul double %107, 0x401921FB54411744
  %197 = call double @cos(double %196)
  %198 = call double @sin(double %196)
  %199 = call double @log(double %53)
  %200 = fmul double -2.000000e+00, %199
  %201 = call double @sqrt(double %200)
  %202 = fmul double %201, %197
  %203 = getelementptr double, ptr %arg4, i32 %130
  store double %202, ptr %203, align 8
  %204 = fmul double %201, %198
  %205 = getelementptr double, ptr %arg4, i32 %131
  store double %204, ptr %205, align 8
  %206 = fmul double %111, 0x401921FB54411744
  %207 = call double @cos(double %206)
  %208 = call double @sin(double %206)
  %209 = call double @log(double %57)
  %210 = fmul double -2.000000e+00, %209
  %211 = call double @sqrt(double %210)
  %212 = fmul double %211, %207
  %213 = getelementptr double, ptr %arg4, i32 %132
  store double %212, ptr %213, align 8
  %214 = fmul double %211, %208
  %215 = getelementptr double, ptr %arg4, i32 %133
  store double %214, ptr %215, align 8
  %216 = fmul double %115, 0x401921FB54411744
  %217 = call double @cos(double %216)
  %218 = call double @sin(double %216)
  %219 = call double @log(double %61)
  %220 = fmul double -2.000000e+00, %219
  %221 = call double @sqrt(double %220)
  %222 = fmul double %221, %217
  %223 = getelementptr double, ptr %arg4, i32 %134
  store double %222, ptr %223, align 8
  %224 = fmul double %221, %218
  %225 = getelementptr double, ptr %arg4, i32 %135
  store double %224, ptr %225, align 8
  ret void
}

; Function Attrs: nounwind readnone speculatable willreturn
declare i32 @llvm.amdgcn.workitem.id.x() #0

; Function Attrs: nounwind readnone speculatable willreturn
declare i32 @llvm.amdgcn.workgroup.id.x() #0

; Function Attrs: nounwind readnone speculatable willreturn
declare i32 @llvm.amdgcn.workgroup.id.y() #0

declare double @cos(double)

declare double @sin(double)

declare double @log(double)

declare double @sqrt(double)

attributes #0 = { nounwind readnone speculatable willreturn }

```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — nartmada (2024-04-01T14:59:04Z)

An internal ticket has been created for investigation.

---

### 评论 #2 — ipanfilo (2024-04-12T17:21:00Z)

Shared object fails to load because it has unresolved symbols. After the following modification of Makefile it works with ROCm 6.0.2 on MI300:
@@ -1,15 +1,16 @@


-GCN=90a
+GCN=942

 EXTRA=\
-${ROCM_PATH}/llvm/lib/libomptarget-new-amdgpu-gfx${GCN}.bc \
+${ROCM_PATH}/llvm/lib/libomptarget-old-amdgpu-gfx${GCN}.bc \
 ${ROCM_PATH}/amdgcn/bitcode/ocml.bc \
 ${ROCM_PATH}/amdgcn/bitcode/oclc_finite_only_off.bc \
 ${ROCM_PATH}/amdgcn/bitcode/oclc_isa_version_${GCN}.bc \
 ${ROCM_PATH}/amdgcn/bitcode/oclc_unsafe_math_off.bc \
 ${ROCM_PATH}/amdgcn/bitcode/oclc_daz_opt_off.bc \
-${ROCM_PATH}/amdgcn/bitcode/oclc_correctly_rounded_sqrt_on.bc
+${ROCM_PATH}/amdgcn/bitcode/oclc_correctly_rounded_sqrt_on.bc \
+${ROCM_PATH}/amdgcn/bitcode/oclc_abi_version_500.bc

 %.bc: %.ll
        ${ROCM_PATH}/llvm/bin/llvm-as < $< > $@


---
