# [Issue]: AMD clang 17.0.0 fatal error: error in backend: Instruction Combining seems stuck in an infinite loop after 1000 iterations

> **Issue #2785**
> **状态**: closed
> **创建时间**: 2024-01-09T06:01:54Z
> **更新时间**: 2024-04-12T19:55:20Z
> **关闭时间**: 2024-03-22T22:53:46Z
> **作者**: pwxy
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2785

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-5.7.0 23352 d1e13c5) on OLCF Frontier crashed during PETSc build
(PETSc release 3.20.3, SHA1 1580af9fcba34756b20ac647dbc5659db3fdd05b) with error "fatal error: error in backend: Instruction Combining seems stuck in an infinite loop after 1000 iterations."

fatal error: error in backend: Instruction Combining seems stuck in an infinite loop after 1000 iterations.
PLEASE submit a bug report to https://github.com/llvm/llvm-project/issues/ and include the crash backtrace, preprocessed source, and associated run script.
Stack dump:
0. Program arguments: /opt/rocm-5.7.0/llvm/bin/clang -march=znver3 -D__CRAY_X86_TRENTO -D__CRAY_AMD_GFX90A -D__CRAYXT_COMPUTE_LINUX_TARGET -c -g -O2 -fPIC -std=c2x -I/autofs/nccs-svm1_home1/ptlin/projects/wdmapp/tpl/petsc/petsc-release-20231231/include -I/autofs/nccs-svm1_home1/ptlin/projects/wdmapp/tpl/petsc/petsc-release-20231231/arch-frontier-amd_rocm5.7.0/include -I/ccs/home/ptlin/projects/wdmapp/tpl/install/petsc/petsc-release-20231231/frontier-amd-5.7.0-g-O2/include -I/opt/rocm-5.7.0/include -MMD -MP /autofs/nccs-svm1_home1/ptlin/projects/wdmapp/tpl/petsc/petsc-release-20231231/src/mat/impls/baij/seq/baij2.c -o arch-frontier-amd_rocm5.7.0/obj/src/mat/impls/baij/seq/baij2.o -I/opt/cray/pe/mpich/8.1.27/ofi/amd/5.0/include -I/opt/cray/pe/dsmml/0.2.2/dsmml//include -I/opt/cray/pe/pmi/6.1.8/include -I/opt/cray/xpmem/2.6.2-2.5_2.22__gd067c3f.shasta/include

 <eof> parser at end of file
 Optimizer
#0 0x000000000218f267 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) (/opt/rocm-5.7.0/llvm/bin/clang+0x218f267)
#1 0x000000000218d0c4 llvm::sys::CleanupOnSignal(unsigned long) (/opt/rocm-5.7.0/llvm/bin/clang+0x218d0c4)
#2 0x00000000020f0c43 llvm::CrashRecoveryContext::HandleExit(int) (/opt/rocm-5.7.0/llvm/bin/clang+0x20f0c43)
#3 0x000000000218455e llvm::sys::Process::Exit(int, bool) (/opt/rocm-5.7.0/llvm/bin/clang+0x218455e)
#4 0x0000000000b48d96 (/opt/rocm-5.7.0/llvm/bin/clang+0xb48d96)
#5 0x00000000020f909c llvm::report_fatal_error(llvm::Twine const&, bool) (/opt/rocm-5.7.0/llvm/bin/clang+0x20f909c)
#6 0x0000000001d69b79 combineInstructionsOverFunction(llvm::Function&, llvm::InstructionWorklist&, llvm::AAResults*, llvm::AssumptionCache&, llvm::TargetLibraryInfo&, llvm::TargetTransformInfo&, llvm::DominatorTree&, llvm::OptimizationRemarkEmitter&, llvm::BlockFrequencyInfo*, llvm::ProfileSummaryInfo*, unsigned int, llvm::LoopInfo*) InstructionCombining.cpp:0:0
#7 0x0000000001d6a073 llvm::InstCombinePass::run(llvm::Function&, llvm::AnalysisManagerllvm::Function&) (/opt/rocm-5.7.0/llvm/bin/clang+0x1d6a073)
#8 0x00000000023ab2ed llvm::detail::PassModel<llvm::Function, llvm::InstCombinePass, llvm::PreservedAnalyses, llvm::AnalysisManagerllvm::Function>::run(llvm::Function&, llvm::AnalysisManagerllvm::Function&) (/opt/rocm-5.7.0/llvm/bin/clang+0x23ab2ed)
#9 0x0000000000b8263e llvm::detail::PassModel<llvm::Function, llvm::PassManager<llvm::Function, llvm::AnalysisManagerllvm::Function>, llvm::PreservedAnalyses, llvm::AnalysisManagerllvm::Function>::run(llvm::Function&, llvm::AnalysisManagerllvm::Function&) (/opt/rocm-5.7.0/llvm/bin/clang+0xb8263e)
#10 0x000000000134ab8a llvm::CGSCCToFunctionPassAdaptor::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) (/opt/rocm-5.7.0/llvm/bin/clang+0x134ab8a)
#11 0x0000000000b7e70d llvm::detail::PassModel<llvm::LazyCallGraph::SCC, llvm::CGSCCToFunctionPassAdaptor, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&>::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) (/opt/rocm-5.7.0/llvm/bin/clang+0xb7e70d)
#12 0x0000000001344305 llvm::PassManager<llvm::LazyCallGraph::SCC, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&>::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) (/opt/rocm-5.7.0/llvm/bin/clang+0x1344305)
#13 0x0000000003179e4d llvm::detail::PassModel<llvm::LazyCallGraph::SCC, llvm::PassManager<llvm::LazyCallGraph::SCC, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&>, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&>::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) (/opt/rocm-5.7.0/llvm/bin/clang+0x3179e4d)
#14 0x00000000013476e6 llvm::DevirtSCCRepeatedPass::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) (/opt/rocm-5.7.0/llvm/bin/clang+0x13476e6)
#15 0x0000000003179e6d llvm::detail::PassModel<llvm::LazyCallGraph::SCC, llvm::DevirtSCCRepeatedPass, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&>::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) (/opt/rocm-5.7.0/llvm/bin/clang+0x3179e6d)
#16 0x000000000134575f llvm::ModuleToPostOrderCGSCCPassAdaptor::run(llvm::Module&, llvm::AnalysisManagerllvm::Module&) (/opt/rocm-5.7.0/llvm/bin/clang+0x134575f)
#17 0x00000000032d6f4d llvm::ModuleInlinerWrapperPass::run(llvm::Module&, llvm::AnalysisManagerllvm::Module&) (/opt/rocm-5.7.0/llvm/bin/clang+0x32d6f4d)
#18 0x0000000003179a7d llvm::detail::PassModel<llvm::Module, llvm::ModuleInlinerWrapperPass, llvm::PreservedAnalyses, llvm::AnalysisManagerllvm::Module>::run(llvm::Module&, llvm::AnalysisManagerllvm::Module&) (/opt/rocm-5.7.0/llvm/bin/clang+0x3179a7d)
#19 0x0000000001c13a93 llvm::PassManager<llvm::Module, llvm::AnalysisManagerllvm::Module>::run(llvm::Module&, llvm::AnalysisManagerllvm::Module&) (/opt/rocm-5.7.0/llvm/bin/clang+0x1c13a93)
#20 0x00000000023b8e3f (anonymous namespace)::EmitAssemblyHelper::RunOptimizationPipeline(clang::BackendAction, std::unique_ptr<llvm::raw_pwrite_stream, std::default_deletellvm::raw_pwrite_stream>&, std::unique_ptr<llvm::ToolOutputFile, std::default_deletellvm::ToolOutputFile>&) BackendUtil.cpp:0:0
#21 0x00000000023bb86b clang::EmitBackendOutput(clang::DiagnosticsEngine&, clang::HeaderSearchOptions const&, clang::CodeGenOptions const&, clang::TargetOptions const&, clang::LangOptions const&, llvm::StringRef, llvm::Module*, clang::BackendAction, llvm::IntrusiveRefCntPtrllvm::vfs::FileSystem, std::unique_ptr<llvm::raw_pwrite_stream, std::default_deletellvm::raw_pwrite_stream>) (/opt/rocm-5.7.0/llvm/bin/clang+0x23bb86b)

#22 0x0000000003127297 clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext&) (/opt/rocm-5.7.0/llvm/bin/clang+0x3127297)
#23 0x0000000003f43109 clang::ParseAST(clang::Sema&, bool, bool) (/opt/rocm-5.7.0/llvm/bin/clang+0x3f43109)
#24 0x0000000003127d8d clang::CodeGenAction::ExecuteAction() (/opt/rocm-5.7.0/llvm/bin/clang+0x3127d8d)
#25 0x0000000002ad3941 clang::FrontendAction::Execute() (/opt/rocm-5.7.0/llvm/bin/clang+0x2ad3941)
#26 0x0000000002a681aa clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) (/opt/rocm-5.7.0/llvm/bin/clang+0x2a681aa)
#27 0x0000000002ba1fe3 clang::ExecuteCompilerInvocation(clang::CompilerInstance*) (/opt/rocm-5.7.0/llvm/bin/clang+0x2ba1fe3)
#28 0x0000000000b4a734 cc1_main(llvm::ArrayRef<char const*>, char const*, void*) (/opt/rocm-5.7.0/llvm/bin/clang+0xb4a734)
#29 0x0000000000b456c6 ExecuteCC1Tool(llvm::SmallVectorImpl<char const*>&, llvm::ToolContext const&) driver.cpp:0:0
#30 0x00000000028d77c9 void llvm::function_ref<void ()>::callback_fn<clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optionalllvm::StringRef>, std::__cxx11::basic_string<char, std::char_traits, std::allocator>, bool) const::'lambda'()>(long) Job.cpp:0:0
#31 0x00000000020f0b45 llvm::CrashRecoveryContext::RunSafely(llvm::function_ref<void ()>) (/opt/rocm-5.7.0/llvm/bin/clang+0x20f0b45)
#32 0x00000000028da276 clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optionalllvm::StringRef>, std::__cxx11::basic_string<char, std::char_traits, std::allocator>, bool) const (/opt/rocm-5.7.0/llvm/bin/clang+0x28da276)
#33 0x000000000289e233 clang::driver::Compilation::ExecuteCommand(clang::driver::Command const&, clang::driver::Command const*&, bool) const (/opt/rocm-5.7.0/llvm/bin/clang+0x289e233)
#34 0x000000000289eaf2 std::_Function_handler<void (), clang::driver::Compilation::ExecuteJobs(clang::driver::JobList const&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&, bool) const::'lambda'()>::_M_invoke(std::_Any_data const&) Compilation.cpp:0:0
#35 0x00000000028a4b14 clang::driver::Compilation::ExecuteJobs(clang::driver::JobList const&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&, bool) const (/opt/rocm-5.7.0/llvm/bin/clang+0x28a4b14)
#36 0x00000000028ab12f clang::driver::Driver::ExecuteCompilation(clang::driver::Compilation&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&) (/opt/rocm-5.7.0/llvm/bin/clang+0x28ab12f)
#37 0x0000000000b485ac clang_main(int, char**, llvm::ToolContext const&) (/opt/rocm-5.7.0/llvm/bin/clang+0xb485ac)
#38 0x0000000000aa6e71 main (/opt/rocm-5.7.0/llvm/bin/clang+0xaa6e71)
#39 0x00007fd304a4129d __libc_start_main (/lib64/libc.so.6+0x3529d)
#40 0x0000000000b406aa _start /home/abuild/rpmbuild/BUILD/glibc-2.31/csu/../sysdeps/x86_64/start.S:122:0
clang: error: clang frontend command failed with exit code 70 (use -v to see invocation)
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-5.7.0 23352 d1e13c5)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-5.7.0/llvm/bin
clang: note: diagnostic msg:

PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
Preprocessed source(s) and associated run script(s) are located at:
clang: note: diagnostic msg: /tmp/baij2-b75057.c
clang: note: diagnostic msg: /tmp/baij2-b75057.sh
clang: note: diagnostic msg:

[baij2-b75057.c.gz](https://github.com/ROCm/ROCm/files/13869613/baij2-b75057.c.gz)
[baij2-b75057.sh.gz](https://github.com/ROCm/ROCm/files/13869615/baij2-b75057.sh.gz)


### Operating System

SLE15

### CPU

AMD EPYC 7A53

### GPU

AMD Instinct MI250X

### Other

_No response_

### ROCm Version

ROCm 5.7.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — nartmada (2024-01-09T20:52:41Z)

Internal ticket has been created to track the issue.

---

### 评论 #2 — nartmada (2024-01-31T02:58:41Z)

Same signature from an internal known issue that has been fixed in upcoming 6.0.2 release.  Thanks.

---

### 评论 #3 — nartmada (2024-03-21T19:09:59Z)

Hi @pwxy, can you please check if you still observe the issue with ROCm 6.0.2?  Thanks.

---

### 评论 #4 — nartmada (2024-03-22T22:53:46Z)

Closing this ticket as the issue has been fixed in ROCm 6.0.2.

---

### 评论 #5 — YellowRoseCx (2024-04-12T19:55:19Z)

> Closing this ticket as the issue has been fixed in ROCm 6.0.2.

Will that fix be coming to Windows in the next version?

---
