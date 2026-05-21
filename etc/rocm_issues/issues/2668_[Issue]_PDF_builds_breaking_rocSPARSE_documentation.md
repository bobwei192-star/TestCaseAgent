# [Issue]: PDF builds breaking rocSPARSE documentation

> **Issue #2668**
> **状态**: closed
> **创建时间**: 2023-11-22T23:40:51Z
> **更新时间**: 2023-11-23T20:31:47Z
> **关闭时间**: 2023-11-23T20:31:47Z
> **作者**: samjwu
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2668

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- samjwu

## 描述

### Problem Description

```
Use of uninitialized value in concatenation (.) or string at (eval 10) line 1.
Use of uninitialized value in concatenation (.) or string at (eval 10) line 2.
Use of uninitialized value in concatenation (.) or string at (eval 10) line 3.
Use of uninitialized value in concatenation (.) or string at (eval 10) line 4.
Subroutine makeglo redefined at (eval 11) line 7.
Use of uninitialized value in concatenation (.) or string at (eval 11) line 1.
Use of uninitialized value in concatenation (.) or string at (eval 11) line 2.
Use of uninitialized value in concatenation (.) or string at (eval 11) line 3.
Use of uninitialized value in concatenation (.) or string at (eval 11) line 4.
Rc files read:
  /etc/LatexMk
  latexmkrc
  latexmkrc
Latexmk: This is Latexmk, John Collins, 20 November 2021, version: 4.76.
Rule 'pdflatex': File changes, etc:
   Changed files, or newly in use since previous run(s):
      'python.tex'
------------
Run number 1 of rule 'pdflatex'
------------
------------
Running 'pdflatex   -interaction=nonstopmode -recorder --jobname="advanced-micro-devices-rocsparse"  "python.tex"'
------------
Latexmk: applying rule 'pdflatex'...
This is pdfTeX, Version 3.141592653-2.6-1.40.22 (TeX Live 2022/dev/Debian) (preloaded format=pdflatex)
 restricted \write18 enabled.
entering extended mode
(./python.tex
LaTeX2e <2021-11-15> patch level 1
L3 programming layer <2022-01-21> (./sphinxmanual.cls
Document Class: sphinxmanual 2019/12/01 v2.3.0 Document class (Sphinx manual)
(/usr/share/texlive/texmf-dist/tex/latex/base/report.cls
Document Class: report 2021/10/04 v1.4n Standard LaTeX document class
(/usr/share/texlive/texmf-dist/tex/latex/base/size10.clo)))
(/usr/share/texlive/texmf-dist/tex/latex/base/inputenc.sty)
(/usr/share/texlive/texmf-dist/tex/latex/cmap/cmap.sty)
(/usr/share/texlive/texmf-dist/tex/latex/base/fontenc.sty<<t1.cmap>>)
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsmath.sty
For additional information on amsmath, use the `?' option.
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amstext.sty
(/usr/share/texlive/texmf-dist/tex/latex/amsmath/amsgen.sty))
```

...

```
! Missing } inserted.
<inserted text> 
                }
l.3969 \end{array}\end{split}
                             
(That makes 100 errors; please try again.)
!  ==> Fatal error occurred, no output PDF file produced!
Transcript written on advanced-micro-devices-rocsparse.log.
Latexmk: Index file 'advanced-micro-devices-rocsparse.idx' was written
Failure to make 'advanced-micro-devices-rocsparse.pdf'
Collected error summary (may duplicate other messages):
  pdflatex: Command for 'pdflatex' gave return code 1
      Refer to 'advanced-micro-devices-rocsparse.log' for details
Latexmk: Examining 'advanced-micro-devices-rocsparse.log'
=== TeX engine is 'pdfTeX'
Latexmk: Errors, in force_mode: so I tried finishing targets
```

### Operating System

Ubuntu 22

### CPU

N/A

### GPU

N/A

### ROCm Version

5.7.1

### ROCm Component

rocSPARSE

### Steps to Reproduce

latexmk -r latexmkrc -pdf -f -dvi- -ps- -jobname=advanced-micro-devices-rocsparse -interaction=nonstopmode

### Output of /opt/rocm/bin/rocminfo --support

N/A
