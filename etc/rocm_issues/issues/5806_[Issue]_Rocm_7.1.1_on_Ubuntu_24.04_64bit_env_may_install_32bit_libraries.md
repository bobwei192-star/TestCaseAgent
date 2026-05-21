# [Issue]: Rocm 7.1.1 on Ubuntu 24.04 64bit env may install 32bit libraries

> **Issue #5806**
> **状态**: closed
> **创建时间**: 2025-12-20T05:01:17Z
> **更新时间**: 2026-03-02T19:30:47Z
> **关闭时间**: 2026-03-02T19:30:47Z
> **作者**: Qubitium
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5806

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

Why is RoCM install on a 64bit system bundling and requring 32bit libraries? Can we remove these as the pkg 24GB total install is already on the very large side and should be trimmed as much as possible.

### Operating System

Ubuntu 24.04

### CPU

AMD Milan

### GPU

AMD Radeon 7900XTX

### ROCm Version

RoCM 7.1.1

### Additional Information

```
server:/$ dpkg --print-architecture
amd64
server:/$ dpkg --print-foreign-architectures
[empty]
server:/$ sudo apt list | grep installed | grep i386
[empty]
```

```
apt install rocm
```

```
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  amd-smi-lib amdgpu-core comgr composablekernel-dev g++-13-multilib g++-multilib gcc-13-multilib gcc-multilib gdal-data gdal-plugins half hip-dev hip-doc hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt
  hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr
  hsa-rocr-dev i965-va-driver icu-devtools intel-media-va-driver lib32asan8 lib32atomic1 lib32gcc-13-dev lib32gcc-s1 lib32gomp1 lib32itm1 lib32quadmath0 lib32stdc++-13-dev lib32stdc++6 lib32ubsan1 libaacs0 libaec0 libamd3 libaom3
  libarmadillo12 libarpack2t64 libavcodec-dev libavcodec60 libavformat-dev libavformat60 libavutil-dev libavutil58 libbdplus0 libblas3 libblosc1 libbluray2 libc6-dev-i386 libc6-dev-x32 libc6-i386 libc6-x32 libcamd3 libccolamd3
  libcfitsio10t64 libcharls2 libcholmod5 libchromaprint1 libcjson1 libcodec2-1.2 libcolamd3 libdav1d7 libdc1394-25 libdc1394-dev libde265-0 libdeflate-dev libdouble-conversion3 libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common
  libdrm-amdgpu-dev libdrm-amdgpu-radeon1 libdrm2-amdgpu libexif-dev libexif-doc libfile-copy-recursive-perl libfile-which-perl libfreexl1 libfyba0t64 libgd3 libgdal34t64 libgdcm-dev libgdcm3.0t64 libgeos-c1t64 libgeos3.12.1t64
  libgeotiff5 libgl2ps1.4 libglew2.2 libgme0 libgphoto2-6t64 libgphoto2-dev libgphoto2-l10n libgphoto2-port12t64 libgsm1 libhdf4-0-alt libhdf5-103-1t64 libhdf5-hl-100t64 libheif-plugin-aomdec libheif-plugin-aomenc
  libheif-plugin-libde265 libheif1 libhwy1t64 libicu-dev libigdgmm12 libimath-dev libinput-bin libinput10 libjbig-dev libjpeg-dev libjpeg-turbo8-dev libjpeg8-dev libjsoncpp25 libjxl0.7 libkmlbase1t64 libkmldom1t64 libkmlengine1t64
  liblapack3 liblept5 liblerc-dev liblzma-dev libmbedcrypto7t64 libmd4c0 libminizip1t64 libmp3lame0 libmpg123-0t64 libmtdev1t64 libncurses-dev libnetcdf19t64 libnorm1t64 libodbc2 libodbcinst2 libogdi4.1 libopencv-calib3d-dev
  libopencv-calib3d406t64 libopencv-contrib-dev libopencv-contrib406t64 libopencv-core-dev libopencv-core406t64 libopencv-dev libopencv-dnn-dev libopencv-dnn406t64 libopencv-features2d-dev libopencv-features2d406t64
  libopencv-flann-dev libopencv-flann406t64 libopencv-highgui-dev libopencv-highgui406t64 libopencv-imgcodecs-dev libopencv-imgcodecs406t64 libopencv-imgproc-dev libopencv-imgproc406t64 libopencv-java libopencv-ml-dev
  libopencv-ml406t64 libopencv-objdetect-dev libopencv-objdetect406t64 libopencv-photo-dev libopencv-photo406t64 libopencv-shape-dev libopencv-shape406t64 libopencv-stitching-dev libopencv-stitching406t64 libopencv-superres-dev
  libopencv-superres406t64 libopencv-video-dev libopencv-video406t64 libopencv-videoio-dev libopencv-videoio406t64 libopencv-videostab-dev libopencv-videostab406t64 libopencv-viz-dev libopencv-viz406t64 libopencv406-jni
  libopenexr-dev libopenmpt0t64 libpcre2-16-0 libpgm-5.3-0t64 libpng-dev libpng-tools libproj25 libprotobuf32t64 libqhull-r8.0 libqt5core5t64 libqt5dbus5t64 libqt5gui5t64 libqt5network5t64 libqt5opengl5t64 libqt5qml5
  libqt5qmlmodels5 libqt5quick5 libqt5svg5 libqt5test5t64 libqt5waylandclient5 libqt5waylandcompositor5 libqt5widgets5t64 librabbitmq4 librav1e0 libraw1394-11 libraw1394-dev libraw1394-tools librist4 librttopo1 libsharpyuv-dev
  libshine3 libsnappy1v5 libsocket++1 libsodium23 libsoxr0 libspatialite8t64 libspeex1 libsrt1.5-gnutls libssh-gcrypt-4 libsuitesparseconfig7 libsuperlu6 libsvtav1enc1d1 libswresample-dev libswresample4 libswscale-dev libswscale7
  libsz2 libtbb-dev libtbb12 libtbbbind-2-5 libtbbmalloc2 libtesseract5 libtiff-dev libtiffxx6 libtwolame0 libudfread0 liburiparser1 libva-drm2 libva-x11-2 libva2 libvorbisfile3 libvpl2 libvpx9 libvtk9.1t64 libwacom-common
  libwacom9 libwebp-dev libwebpdecoder3 libx265-199 libx32asan8 libx32atomic1 libx32gcc-13-dev libx32gcc-s1 libx32gomp1 libx32itm1 libx32quadmath0 libx32stdc++-13-dev libx32stdc++6 libx32ubsan1 libxerces-c3.2t64 libxml2-dev
  libxvidcore4 libzmq5 libzvbi-common libzvbi0t64 mesa-common-dev mesa-va-drivers migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev ocl-icd-opencl-dev opencl-c-headers opencl-clhpp-headers opencv-data
  openmp-extras-dev openmp-extras-runtime proj-bin proj-data python3-argcomplete qt5-gtk-platformtheme qttranslations5-l10n qtwayland5 rccl rccl-dev rocalution rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm-cmake
  rocm-core rocm-dbgapi rocm-debug-agent rocm-developer-tools rocm-device-libs rocm-gdb rocm-hip rocm-language-runtime rocm-llvm rocm-opencl rocm-opencl-dev rocm-opencl-sdk rocm-openmp rocm-smi-lib rocminfo rocprim-dev rocprofiler
  rocprofiler-compute rocprofiler-dev rocprofiler-plugins rocprofiler-register rocprofiler-sdk rocprofiler-sdk-rocpd rocprofiler-sdk-roctx rocprofiler-systems rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev
  rocthrust-dev roctracer roctracer-dev rocwmma-dev rpp rpp-dev unixodbc-common va-driver-all valgrind
Suggested packages:
  lib32stdc++6-13-dbg libx32stdc++6-13-dbg i965-va-driver-shaders libcuda1 libnvcuvid1 libnvidia-encode1 libbluray-bdj libgd-tools geotiff-bin gdal-bin libgeotiff-epsg glew-utils gphoto2 libhdf4-doc libhdf4-alt-dev hdf4-tools
  libheif-plugin-x265 libheif-plugin-ffmpegdec libheif-plugin-jpegdec libheif-plugin-jpegenc libheif-plugin-j2kdec libheif-plugin-j2kenc libheif-plugin-rav1e libheif-plugin-svtenc icu-doc liblzma-doc ncurses-doc odbc-postgresql
  tdsodbc ogdi-bin opencv-doc qgnomeplatform-qt5 qt5-image-formats-plugins qt5-qmltooling-plugins libraw1394-doc speex libtbb-doc mpi-default-bin vtk9-doc vtk9-examples libwacom-bin opencl-clhpp-headers-doc valgrind-dbg
  valgrind-mpi kcachegrind alleyoop valkyrie
The following NEW packages will be installed:
  amd-smi-lib amdgpu-core comgr composablekernel-dev g++-13-multilib g++-multilib gcc-13-multilib gcc-multilib gdal-data gdal-plugins half hip-dev hip-doc hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt
  hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr
  hsa-rocr-dev i965-va-driver icu-devtools intel-media-va-driver lib32asan8 lib32atomic1 lib32gcc-13-dev lib32gcc-s1 lib32gomp1 lib32itm1 lib32quadmath0 lib32stdc++-13-dev lib32stdc++6 lib32ubsan1 libaacs0 libaec0 libamd3 libaom3
  libarmadillo12 libarpack2t64 libavcodec-dev libavcodec60 libavformat-dev libavformat60 libavutil-dev libavutil58 libbdplus0 libblas3 libblosc1 libbluray2 libc6-dev-i386 libc6-dev-x32 libc6-i386 libc6-x32 libcamd3 libccolamd3
  libcfitsio10t64 libcharls2 libcholmod5 libchromaprint1 libcjson1 libcodec2-1.2 libcolamd3 libdav1d7 libdc1394-25 libdc1394-dev libde265-0 libdeflate-dev libdouble-conversion3 libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common
  libdrm-amdgpu-dev libdrm-amdgpu-radeon1 libdrm2-amdgpu libexif-dev libexif-doc libfile-copy-recursive-perl libfile-which-perl libfreexl1 libfyba0t64 libgd3 libgdal34t64 libgdcm-dev libgdcm3.0t64 libgeos-c1t64 libgeos3.12.1t64
  libgeotiff5 libgl2ps1.4 libglew2.2 libgme0 libgphoto2-6t64 libgphoto2-dev libgphoto2-l10n libgphoto2-port12t64 libgsm1 libhdf4-0-alt libhdf5-103-1t64 libhdf5-hl-100t64 libheif-plugin-aomdec libheif-plugin-aomenc
  libheif-plugin-libde265 libheif1 libhwy1t64 libicu-dev libigdgmm12 libimath-dev libinput-bin libinput10 libjbig-dev libjpeg-dev libjpeg-turbo8-dev libjpeg8-dev libjsoncpp25 libjxl0.7 libkmlbase1t64 libkmldom1t64 libkmlengine1t64
  liblapack3 liblept5 liblerc-dev liblzma-dev libmbedcrypto7t64 libmd4c0 libminizip1t64 libmp3lame0 libmpg123-0t64 libmtdev1t64 libncurses-dev libnetcdf19t64 libnorm1t64 libodbc2 libodbcinst2 libogdi4.1 libopencv-calib3d-dev
  libopencv-calib3d406t64 libopencv-contrib-dev libopencv-contrib406t64 libopencv-core-dev libopencv-core406t64 libopencv-dev libopencv-dnn-dev libopencv-dnn406t64 libopencv-features2d-dev libopencv-features2d406t64
  libopencv-flann-dev libopencv-flann406t64 libopencv-highgui-dev libopencv-highgui406t64 libopencv-imgcodecs-dev libopencv-imgcodecs406t64 libopencv-imgproc-dev libopencv-imgproc406t64 libopencv-java libopencv-ml-dev
  libopencv-ml406t64 libopencv-objdetect-dev libopencv-objdetect406t64 libopencv-photo-dev libopencv-photo406t64 libopencv-shape-dev libopencv-shape406t64 libopencv-stitching-dev libopencv-stitching406t64 libopencv-superres-dev
  libopencv-superres406t64 libopencv-video-dev libopencv-video406t64 libopencv-videoio-dev libopencv-videoio406t64 libopencv-videostab-dev libopencv-videostab406t64 libopencv-viz-dev libopencv-viz406t64 libopencv406-jni
  libopenexr-dev libopenmpt0t64 libpcre2-16-0 libpgm-5.3-0t64 libpng-dev libpng-tools libproj25 libprotobuf32t64 libqhull-r8.0 libqt5core5t64 libqt5dbus5t64 libqt5gui5t64 libqt5network5t64 libqt5opengl5t64 libqt5qml5
  libqt5qmlmodels5 libqt5quick5 libqt5svg5 libqt5test5t64 libqt5waylandclient5 libqt5waylandcompositor5 libqt5widgets5t64 librabbitmq4 librav1e0 libraw1394-11 libraw1394-dev libraw1394-tools librist4 librttopo1 libsharpyuv-dev
  libshine3 libsnappy1v5 libsocket++1 libsodium23 libsoxr0 libspatialite8t64 libspeex1 libsrt1.5-gnutls libssh-gcrypt-4 libsuitesparseconfig7 libsuperlu6 libsvtav1enc1d1 libswresample-dev libswresample4 libswscale-dev libswscale7
  libsz2 libtbb-dev libtbb12 libtbbbind-2-5 libtbbmalloc2 libtesseract5 libtiff-dev libtiffxx6 libtwolame0 libudfread0 liburiparser1 libva-drm2 libva-x11-2 libva2 libvorbisfile3 libvpl2 libvpx9 libvtk9.1t64 libwacom-common
  libwacom9 libwebp-dev libwebpdecoder3 libx265-199 libx32asan8 libx32atomic1 libx32gcc-13-dev libx32gcc-s1 libx32gomp1 libx32itm1 libx32quadmath0 libx32stdc++-13-dev libx32stdc++6 libx32ubsan1 libxerces-c3.2t64 libxml2-dev
  libxvidcore4 libzmq5 libzvbi-common libzvbi0t64 mesa-common-dev mesa-va-drivers migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev ocl-icd-opencl-dev opencl-c-headers opencl-clhpp-headers opencv-data
  openmp-extras-dev openmp-extras-runtime proj-bin proj-data python3-argcomplete qt5-gtk-platformtheme qttranslations5-l10n qtwayland5 rccl rccl-dev rocalution rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm rocm-cmake
  rocm-core rocm-dbgapi rocm-debug-agent rocm-developer-tools rocm-device-libs rocm-gdb rocm-hip rocm-language-runtime rocm-llvm rocm-opencl rocm-opencl-dev rocm-opencl-sdk rocm-openmp rocm-smi-lib rocminfo rocprim-dev rocprofiler
  rocprofiler-compute rocprofiler-dev rocprofiler-plugins rocprofiler-register rocprofiler-sdk rocprofiler-sdk-rocpd rocprofiler-sdk-roctx rocprofiler-systems rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev
  rocthrust-dev roctracer roctracer-dev rocwmma-dev rpp rpp-dev unixodbc-common va-driver-all valgrind
0 upgraded, 347 newly installed, 0 to remove and 0 not upgraded.
Need to get 5,952 MB/5,955 MB of archives.
After this operation, 24.3 GB of additional disk space will be used.
```

---

## 评论 (9 条)

### 评论 #1 — Qubitium (2025-12-20T07:13:05Z)

But `rocm` on a `vm` also 24.04 64bit shows that the lib32 libraies are not installed and everything looks correct with all pkgs in 64bit form. Both the host (issue thread) and this `vm` under `host` on the same machine and both do not have i386 arch installed. Need to check what is the diff. 

```
root@u:~# sudo apt install rocm
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  libpcp-archive1t64 libpcp-gui2t64 libpcp-import1t64 libpcp-mmv1t64 libpcp-pmda-perl libpcp-pmda3t64 libpcp-trace2t64 libpcp-web1t64 libpcp3t64 libpfm4 pcp-conf python3-pcp
Use 'sudo apt autoremove' to remove them.
The following additional packages will be installed:
  amd-smi-lib amdgpu-core comgr composablekernel-dev gdal-data gdal-plugins gdb gstreamer1.0-plugins-base half hip-dev hip-doc hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt hipblaslt-dev hipcc
  hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev libaacs0
  libamd-comgr2 libamd3 libamdhip64-5 libarmadillo12 libarpack2t64 libavcodec-dev libavformat-dev libavformat60 libavutil-dev libbdplus0 libblas3 libblosc1 libbluray2 libc6-dbg libcamd3 libccolamd3 libcdparanoia0 libcharls2
  libcholmod5 libchromaprint1 libcjson1 libcolamd3 libdc1394-25 libdc1394-dev libdouble-conversion3 libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm-amdgpu-dev libdrm-amdgpu-radeon1 libdrm-dev libdrm-nouveau2 libdrm-radeon1
  libdrm2-amdgpu libevdev2 libevent-pthreads-2.1-7t64 libfabric1 libfile-copy-recursive-perl libfreexl1 libfyba0t64 libgdal34t64 libgdcm-dev libgdcm3.0t64 libgeos-c1t64 libgeos3.12.1t64 libgeotiff5 libgl2ps1.4 libglew2.2 libgme0
  libgphoto2-6t64 libgphoto2-dev libgphoto2-l10n libgphoto2-port12t64 libgstreamer-plugins-base1.0-0 libgudev-1.0-0 libhdf4-0-alt libhsa-runtime64-1 libhsakmt1 libinput-bin libinput10 libkmlbase1t64 libkmldom1t64 libkmlengine1t64
  liblapack3 liblept5 libllvm17t64 libmbedcrypto7t64 libmd4c0 libminizip1t64 libmtdev1t64 libmunge2 libmysqlclient21 libnetcdf19t64 libnorm1t64 libnuma-dev libodbc2 libodbcinst2 libogdi4.1 libopencv-calib3d-dev
  libopencv-calib3d406t64 libopencv-contrib-dev libopencv-contrib406t64 libopencv-core-dev libopencv-core406t64 libopencv-dev libopencv-dnn-dev libopencv-dnn406t64 libopencv-features2d-dev libopencv-features2d406t64
  libopencv-flann-dev libopencv-flann406t64 libopencv-highgui-dev libopencv-highgui406t64 libopencv-imgcodecs-dev libopencv-imgcodecs406t64 libopencv-imgproc-dev libopencv-imgproc406t64 libopencv-java libopencv-ml-dev
  libopencv-ml406t64 libopencv-objdetect-dev libopencv-objdetect406t64 libopencv-photo-dev libopencv-photo406t64 libopencv-shape-dev libopencv-shape406t64 libopencv-stitching-dev libopencv-stitching406t64 libopencv-superres-dev
  libopencv-superres406t64 libopencv-video-dev libopencv-video406t64 libopencv-videoio-dev libopencv-videoio406t64 libopencv-videostab-dev libopencv-videostab406t64 libopencv-viz-dev libopencv-viz406t64 libopencv406-jni
  libopenmpi3t64 libopenmpt0t64 liborc-0.4-0t64 libpciaccess-dev libpgm-5.3-0t64 libpmix2t64 libpq5 libproj25 libpsm-infinipath1 libpsm2-2 libqhull-r8.0 libqt5core5t64 libqt5dbus5t64 libqt5gui5t64 libqt5network5t64 libqt5opengl5t64
  libqt5qml5 libqt5qmlmodels5 libqt5quick5 libqt5svg5 libqt5test5t64 libqt5waylandclient5 libqt5waylandcompositor5 libqt5widgets5t64 librabbitmq4 libraw1394-11 libraw1394-dev libraw1394-tools librist4 librttopo1 libsocket++1
  libspatialite8t64 libsrt1.5-gnutls libssh-gcrypt-4 libsuitesparseconfig7 libsuperlu6 libswresample-dev libswscale-dev libswscale7 libtesseract5 libucx0 libudfread0 liburiparser1 libvisual-0.4-0 libvtk9.1t64 libwacom-common
  libwacom9 libxerces-c3.2t64 libzmq5 mesa-common-dev migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev opencv-data openmp-extras-dev openmp-extras-runtime proj-bin proj-data python3-argcomplete
  qt5-gtk-platformtheme qttranslations5-l10n qtwayland5 rccl rccl-dev rocalution rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm-cmake rocm-core rocm-dbgapi rocm-debug-agent rocm-developer-tools rocm-device-libs rocm-gdb
  rocm-hip rocm-language-runtime rocm-llvm rocm-opencl rocm-opencl-dev rocm-opencl-sdk rocm-openmp rocm-smi-lib rocminfo rocprim-dev rocprofiler rocprofiler-compute rocprofiler-dev rocprofiler-plugins rocprofiler-register
  rocprofiler-sdk rocprofiler-sdk-rocpd rocprofiler-sdk-roctx rocprofiler-systems rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev rocthrust-dev roctracer roctracer-dev rocwmma-dev rpp rpp-dev unixodbc-common
  valgrind
Suggested packages:
  gdb-doc gdbserver gvfs libbluray-bdj geotiff-bin gdal-bin libgeotiff-epsg glew-utils gphoto2 libvisual-0.4-plugins libhdf4-doc libhdf4-alt-dev hdf4-tools odbc-postgresql tdsodbc ogdi-bin opencv-doc qgnomeplatform-qt5
  qt5-image-formats-plugins qt5-qmltooling-plugins libraw1394-doc mpi-default-bin vtk9-doc vtk9-examples libwacom-bin valgrind-dbg valgrind-mpi kcachegrind alleyoop valkyrie
The following NEW packages will be installed:
  amd-smi-lib amdgpu-core comgr composablekernel-dev gdal-data gdal-plugins gdb gstreamer1.0-plugins-base half hip-dev hip-doc hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt hipblaslt-dev hipcc
  hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev libaacs0
  libamd-comgr2 libamd3 libamdhip64-5 libarmadillo12 libarpack2t64 libavcodec-dev libavformat-dev libavformat60 libavutil-dev libbdplus0 libblas3 libblosc1 libbluray2 libc6-dbg libcamd3 libccolamd3 libcdparanoia0 libcharls2
  libcholmod5 libchromaprint1 libcjson1 libcolamd3 libdc1394-25 libdc1394-dev libdouble-conversion3 libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm-amdgpu-dev libdrm-amdgpu-radeon1 libdrm-dev libdrm-nouveau2 libdrm-radeon1
  libdrm2-amdgpu libevdev2 libevent-pthreads-2.1-7t64 libfabric1 libfile-copy-recursive-perl libfreexl1 libfyba0t64 libgdal34t64 libgdcm-dev libgdcm3.0t64 libgeos-c1t64 libgeos3.12.1t64 libgeotiff5 libgl2ps1.4 libglew2.2 libgme0
  libgphoto2-6t64 libgphoto2-dev libgphoto2-l10n libgphoto2-port12t64 libgstreamer-plugins-base1.0-0 libgudev-1.0-0 libhdf4-0-alt libhsa-runtime64-1 libhsakmt1 libinput-bin libinput10 libkmlbase1t64 libkmldom1t64 libkmlengine1t64
  liblapack3 liblept5 libllvm17t64 libmbedcrypto7t64 libmd4c0 libminizip1t64 libmtdev1t64 libmunge2 libmysqlclient21 libnetcdf19t64 libnorm1t64 libnuma-dev libodbc2 libodbcinst2 libogdi4.1 libopencv-calib3d-dev
  libopencv-calib3d406t64 libopencv-contrib-dev libopencv-contrib406t64 libopencv-core-dev libopencv-core406t64 libopencv-dev libopencv-dnn-dev libopencv-dnn406t64 libopencv-features2d-dev libopencv-features2d406t64
  libopencv-flann-dev libopencv-flann406t64 libopencv-highgui-dev libopencv-highgui406t64 libopencv-imgcodecs-dev libopencv-imgcodecs406t64 libopencv-imgproc-dev libopencv-imgproc406t64 libopencv-java libopencv-ml-dev
  libopencv-ml406t64 libopencv-objdetect-dev libopencv-objdetect406t64 libopencv-photo-dev libopencv-photo406t64 libopencv-shape-dev libopencv-shape406t64 libopencv-stitching-dev libopencv-stitching406t64 libopencv-superres-dev
  libopencv-superres406t64 libopencv-video-dev libopencv-video406t64 libopencv-videoio-dev libopencv-videoio406t64 libopencv-videostab-dev libopencv-videostab406t64 libopencv-viz-dev libopencv-viz406t64 libopencv406-jni
  libopenmpi3t64 libopenmpt0t64 liborc-0.4-0t64 libpciaccess-dev libpgm-5.3-0t64 libpmix2t64 libpq5 libproj25 libpsm-infinipath1 libpsm2-2 libqhull-r8.0 libqt5core5t64 libqt5dbus5t64 libqt5gui5t64 libqt5network5t64 libqt5opengl5t64
  libqt5qml5 libqt5qmlmodels5 libqt5quick5 libqt5svg5 libqt5test5t64 libqt5waylandclient5 libqt5waylandcompositor5 libqt5widgets5t64 librabbitmq4 libraw1394-11 libraw1394-dev libraw1394-tools librist4 librttopo1 libsocket++1
  libspatialite8t64 libsrt1.5-gnutls libssh-gcrypt-4 libsuitesparseconfig7 libsuperlu6 libswresample-dev libswscale-dev libswscale7 libtesseract5 libucx0 libudfread0 liburiparser1 libvisual-0.4-0 libvtk9.1t64 libwacom-common
  libwacom9 libxerces-c3.2t64 libzmq5 mesa-common-dev migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev opencv-data openmp-extras-dev openmp-extras-runtime proj-bin proj-data python3-argcomplete
  qt5-gtk-platformtheme qttranslations5-l10n qtwayland5 rccl rccl-dev rocalution rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm rocm-cmake rocm-core rocm-dbgapi rocm-debug-agent rocm-developer-tools rocm-device-libs
  rocm-gdb rocm-hip rocm-language-runtime rocm-llvm rocm-opencl rocm-opencl-dev rocm-opencl-sdk rocm-openmp rocm-smi-lib rocminfo rocprim-dev rocprofiler rocprofiler-compute rocprofiler-dev rocprofiler-plugins rocprofiler-register
  rocprofiler-sdk rocprofiler-sdk-rocpd rocprofiler-sdk-roctx rocprofiler-systems rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev rocthrust-dev roctracer roctracer-dev rocwmma-dev rpp rpp-dev unixodbc-common
  valgrind
0 upgraded, 270 newly installed, 0 to remove and 35 not upgraded.
Need to get 5950 MB/5950 MB of archives.
After this operation, 24.3 GB of additional disk space will be used.
Do you want to continue? [Y/n]
```

---

### 评论 #2 — Qubitium (2025-12-20T07:42:02Z)

I am perplexied. Both host and vm have very simlar packages installed. For whatever reason, the inter dependencies in `apt` on  `host` is causing `32bit` libraries to be installed when there are zero `i386` libs installed on host and the `i386` arch is not added to host arch. 

---

### 评论 #3 — Qubitium (2025-12-20T08:07:07Z)

Below is pkg depends in a `clean` `ubuntu 24.04` `vm` just was just booted up to test. rocm install is following official guide:

32bit libs are getting installed in a just booted clean env.  Example: `lib32stdc++6-13-dbg` and others. 

install 
```
wget https://repo.radeon.com/amdgpu-install/7.1.1/ubuntu/noble/amdgpu-install_7.1.1.70101-1_all.deb
sudo apt install ./amdgpu-install_7.1.1.70101-1_all.deb
sudo apt update
sudo apt install python3-setuptools python3-wheel
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
sudo apt install rocm
```

rocm depends: many 32bit libs

```
The following additional packages will be installed:
  adwaita-icon-theme amd-smi-lib amdgpu-core at-spi2-common at-spi2-core binutils binutils-common binutils-x86-64-linux-gnu build-essential bzip2 comgr composablekernel-dev cpp cpp-13 cpp-13-x86-64-linux-gnu cpp-x86-64-linux-gnu
  dconf-gsettings-backend dconf-service dpkg-dev fakeroot fontconfig fontconfig-config fonts-dejavu-core fonts-dejavu-mono g++ g++-13 g++-13-multilib g++-13-x86-64-linux-gnu g++-multilib g++-x86-64-linux-gnu gcc gcc-13 gcc-13-base
  gcc-13-multilib gcc-13-x86-64-linux-gnu gcc-multilib gcc-x86-64-linux-gnu gdal-data gdal-plugins gdb gsettings-desktop-schemas gstreamer1.0-plugins-base gtk-update-icon-cache half hicolor-icon-theme hip-dev hip-doc
  hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev
  hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev humanity-icon-theme i965-va-driver icu-devtools intel-media-va-driver javascript-common lib32asan8 lib32atomic1 lib32gcc-13-dev
  lib32gcc-s1 lib32gomp1 lib32itm1 lib32quadmath0 lib32stdc++-13-dev lib32stdc++6 lib32ubsan1 libaacs0 libaec0 libalgorithm-diff-perl libalgorithm-diff-xs-perl libalgorithm-merge-perl libamd-comgr2 libamd3 libamdhip64-5 libaom3
  libarmadillo12 libarpack2t64 libasan8 libatk-bridge2.0-0t64 libatk1.0-0t64 libatomic1 libatspi2.0-0t64 libavahi-client3 libavahi-common-data libavahi-common3 libavcodec-dev libavcodec60 libavformat-dev libavformat60 libavutil-dev
  libavutil58 libbabeltrace1 libbdplus0 libbinutils libblas3 libblosc1 libbluray2 libc-dev-bin libc-devtools libc6-dbg libc6-dev libc6-dev-i386 libc6-dev-x32 libc6-i386 libc6-x32 libcairo-gobject2 libcairo2 libcamd3 libcc1-0
  libccolamd3 libcdparanoia0 libcfitsio10t64 libcharls2 libcholmod5 libchromaprint1 libcjson1 libcodec2-1.2 libcolamd3 libcolord2 libcrypt-dev libctf-nobfd0 libctf0 libcups2t64 libdatrie1 libdav1d7 libdc1394-25 libdc1394-dev
  libdconf1 libde265-0 libdebuginfod-common libdebuginfod1t64 libdeflate-dev libdeflate0 libdouble-conversion3 libdpkg-perl libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm-amdgpu-dev libdrm-amdgpu-radeon1 libdrm-amdgpu1
  libdrm-dev libdrm-intel1 libdrm-nouveau2 libdrm-radeon1 libdrm2-amdgpu libegl-mesa0 libegl1 libelf-dev libepoxy0 libevent-pthreads-2.1-7t64 libexif-dev libexif-doc libexif12 libexpat1-dev libfabric1 libfakeroot
  libfile-copy-recursive-perl libfile-fcntllock-perl libfile-listing-perl libfile-which-perl libfontconfig1 libfreetype6 libfreexl1 libfyba0t64 libgbm1 libgcc-13-dev libgd3 libgdal34t64 libgdcm-dev libgdcm3.0t64 libgdk-pixbuf-2.0-0
  libgdk-pixbuf2.0-bin libgdk-pixbuf2.0-common libgeos-c1t64 libgeos3.12.1t64 libgeotiff5 libgfortran5 libgif7 libgl-dev libgl1 libgl1-mesa-dri libgl2ps1.4 libglew2.2 libglvnd0 libglx-dev libglx-mesa0 libglx0 libgme0 libgomp1
  libgphoto2-6t64 libgphoto2-dev libgphoto2-l10n libgphoto2-port12t64 libgprofng0 libgraphite2-3 libgsm1 libgstreamer-plugins-base1.0-0 libgtk-3-0t64 libgtk-3-bin libgtk-3-common libharfbuzz0b libhdf4-0-alt libhdf5-103-1t64
  libhdf5-hl-100t64 libheif-plugin-aomdec libheif-plugin-aomenc libheif-plugin-libde265 libheif1 libhsa-runtime64-1 libhsakmt1 libhttp-date-perl libhwasan0 libhwloc-plugins libhwloc15 libhwy1t64 libice6 libicu-dev libigdgmm12
  libimath-3-1-29t64 libimath-dev libinput-bin libinput10 libipt2 libisl23 libitm1 libjbig-dev libjbig0 libjpeg-dev libjpeg-turbo8 libjpeg-turbo8-dev libjpeg8 libjpeg8-dev libjs-jquery libjs-sphinxdoc libjs-underscore libjsoncpp25
  libjxl0.7 libkmlbase1t64 libkmldom1t64 libkmlengine1t64 liblapack3 liblcms2-2 liblept5 liblerc-dev liblerc4 libllvm17t64 libllvm20 liblsan0 libltdl7 liblzma-dev libmbedcrypto7t64 libmd4c0 libminizip1t64 libmp3lame0 libmpc3
  libmpg123-0t64 libmtdev1t64 libmunge2 libmysqlclient21 libncurses-dev libnetcdf19t64 libnorm1t64 libnuma-dev libodbc2 libodbcinst2 libogdi4.1 libogg0 libopencv-calib3d-dev libopencv-calib3d406t64 libopencv-contrib-dev
  libopencv-contrib406t64 libopencv-core-dev libopencv-core406t64 libopencv-dev libopencv-dnn-dev libopencv-dnn406t64 libopencv-features2d-dev libopencv-features2d406t64 libopencv-flann-dev libopencv-flann406t64
  libopencv-highgui-dev libopencv-highgui406t64 libopencv-imgcodecs-dev libopencv-imgcodecs406t64 libopencv-imgproc-dev libopencv-imgproc406t64 libopencv-java libopencv-ml-dev libopencv-ml406t64 libopencv-objdetect-dev
  libopencv-objdetect406t64 libopencv-photo-dev libopencv-photo406t64 libopencv-shape-dev libopencv-shape406t64 libopencv-stitching-dev libopencv-stitching406t64 libopencv-superres-dev libopencv-superres406t64 libopencv-video-dev
  libopencv-video406t64 libopencv-videoio-dev libopencv-videoio406t64 libopencv-videostab-dev libopencv-videostab406t64 libopencv-viz-dev libopencv-viz406t64 libopencv406-jni libopenexr-3-1-30 libopenexr-dev libopengl0 libopenjp2-7
  libopenmpi3t64 libopenmpt0t64 libopus0 liborc-0.4-0t64 libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libpciaccess-dev libpciaccess0 libpcre2-16-0 libpgm-5.3-0t64 libpixman-1-0 libpkgconf3 libpmix2t64 libpng-dev
  libpng-tools libpoppler134 libpq5 libproj25 libprotobuf32t64 libpsm-infinipath1 libpsm2-2 libpthread-stubs0-dev libpython3-dev libpython3.12-dev libqhull-r8.0 libqt5core5t64 libqt5dbus5t64 libqt5gui5t64 libqt5network5t64
  libqt5opengl5t64 libqt5qml5 libqt5qmlmodels5 libqt5quick5 libqt5svg5 libqt5test5t64 libqt5waylandclient5 libqt5waylandcompositor5 libqt5widgets5t64 libquadmath0 librabbitmq4 librav1e0 libraw1394-11 libraw1394-dev libraw1394-tools
  librdmacm1t64 librist4 librsvg2-2 librsvg2-common librttopo1 libsframe1 libsharpyuv-dev libsharpyuv0 libshine3 libsm6 libsnappy1v5 libsocket++1 libsource-highlight-common libsource-highlight4t64 libsoxr0 libspatialite8t64
  libspeex1 libsrt1.5-gnutls libssh-gcrypt-4 libstdc++-13-dev libsuitesparseconfig7 libsuperlu6 libsvtav1enc1d1 libswresample-dev libswresample4 libswscale-dev libswscale7 libsz2 libtbb-dev libtbb12 libtbbbind-2-5 libtbbmalloc2
  libtesseract5 libthai-data libthai0 libtheora0 libtiff-dev libtiff6 libtiffxx6 libtimedate-perl libtk8.6 libtsan2 libtwolame0 libubsan1 libucx0 libudfread0 liburi-perl liburiparser1 libva-drm2 libva-x11-2 libva2 libvdpau1
  libvisual-0.4-0 libvorbis0a libvorbisenc2 libvorbisfile3 libvpl2 libvpx9 libvtk9.1t64 libvulkan1 libwacom-common libwacom9 libwayland-client0 libwayland-cursor0 libwayland-egl1 libwayland-server0 libwebp-dev libwebp7
  libwebpdecoder3 libwebpdemux2 libwebpmux3 libx11-dev libx11-xcb1 libx264-164 libx265-199 libx32asan8 libx32atomic1 libx32gcc-13-dev libx32gcc-s1 libx32gomp1 libx32itm1 libx32quadmath0 libx32stdc++-13-dev libx32stdc++6
  libx32ubsan1 libxau-dev libxcb-dri3-0 libxcb-glx0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-present0 libxcb-randr0 libxcb-render-util0 libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-sync1 libxcb-util1 libxcb-xfixes0
  libxcb-xinerama0 libxcb-xinput0 libxcb-xkb1 libxcb1-dev libxcomposite1 libxcursor1 libxdamage1 libxdmcp-dev libxerces-c3.2t64 libxfixes3 libxft2 libxi6 libxinerama1 libxkbcommon-x11-0 libxml2-dev libxnvctrl0 libxpm4 libxrandr2
  libxrender1 libxshmfence1 libxss1 libxtst6 libxvidcore4 libxxf86vm1 libzmq5 libzstd-dev libzvbi-common libzvbi0t64 linux-libc-dev lto-disabled-list make manpages-dev mesa-common-dev mesa-libgallium mesa-va-drivers
  mesa-vdpau-drivers mesa-vulkan-drivers migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev mysql-common ocl-icd-libopencl1 ocl-icd-opencl-dev opencl-c-headers opencl-clhpp-headers opencv-data openmp-extras-dev
  openmp-extras-runtime pkg-config pkgconf pkgconf-bin poppler-data proj-bin proj-data python3-argcomplete python3-dev python3-pip python3.12-dev qt5-gtk-platformtheme qttranslations5-l10n qtwayland5 rccl rccl-dev rocalution
  rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm-cmake rocm-core rocm-dbgapi rocm-debug-agent rocm-developer-tools rocm-device-libs rocm-gdb rocm-hip rocm-language-runtime rocm-llvm rocm-opencl rocm-opencl-dev
  rocm-opencl-sdk rocm-openmp rocm-smi-lib rocminfo rocprim-dev rocprofiler rocprofiler-compute rocprofiler-dev rocprofiler-plugins rocprofiler-register rocprofiler-sdk rocprofiler-sdk-rocpd rocprofiler-sdk-roctx
  rocprofiler-systems rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev rocthrust-dev roctracer roctracer-dev rocwmma-dev rpcsvc-proto rpp rpp-dev session-migration ubuntu-mono unixodbc-common va-driver-all
  valgrind vdpau-driver-all x11-common x11proto-dev xorg-sgml-doctools xtrans-dev zlib1g-dev
Suggested packages:
  binutils-doc gprofng-gui bzip2-doc cpp-doc gcc-13-locales cpp-13-doc debian-keyring gcc-13-doc lib32stdc++6-13-dbg libx32stdc++6-13-dbg autoconf automake libtool flex bison gcc-doc gdb-x86-64-linux-gnu gdb-doc gdbserver gvfs
  i965-va-driver-shaders apache2 | lighttpd | httpd libcuda1 libnvcuvid1 libnvidia-encode1 libbluray-bdj glibc-doc colord cups-common bzr libgd-tools geotiff-bin gdal-bin libgeotiff-epsg glew-utils gphoto2 libvisual-0.4-plugins
  libhdf4-doc libhdf4-alt-dev hdf4-tools libheif-plugin-x265 libheif-plugin-ffmpegdec libheif-plugin-jpegdec libheif-plugin-jpegenc libheif-plugin-j2kdec libheif-plugin-j2kenc libheif-plugin-rav1e libheif-plugin-svtenc
  libhwloc-contrib-plugins icu-doc liblcms2-utils liblzma-doc ncurses-doc odbc-postgresql tdsodbc ogdi-bin opencv-doc opus-tools qgnomeplatform-qt5 qt5-image-formats-plugins qt5-qmltooling-plugins libraw1394-doc librsvg2-bin speex
  libstdc++-13-doc libtbb-doc tk8.6 libbusiness-isbn-perl libregexp-ipv6-perl libwww-perl mpi-default-bin vtk9-doc vtk9-examples libwacom-bin libx11-doc libxcb-doc make-doc opencl-icd opencl-clhpp-headers-doc poppler-utils
  ghostscript fonts-japanese-mincho | fonts-ipafont-mincho fonts-japanese-gothic | fonts-ipafont-gothic fonts-arphic-ukai fonts-arphic-uming fonts-nanum valgrind-dbg valgrind-mpi kcachegrind alleyoop valkyrie libvdpau-va-gl1
The following NEW packages will be installed:
  adwaita-icon-theme amd-smi-lib amdgpu-core at-spi2-common at-spi2-core binutils binutils-common binutils-x86-64-linux-gnu build-essential bzip2 comgr composablekernel-dev cpp cpp-13 cpp-13-x86-64-linux-gnu cpp-x86-64-linux-gnu
  dconf-gsettings-backend dconf-service dpkg-dev fakeroot fontconfig fontconfig-config fonts-dejavu-core fonts-dejavu-mono g++ g++-13 g++-13-multilib g++-13-x86-64-linux-gnu g++-multilib g++-x86-64-linux-gnu gcc gcc-13 gcc-13-base
  gcc-13-multilib gcc-13-x86-64-linux-gnu gcc-multilib gcc-x86-64-linux-gnu gdal-data gdal-plugins gdb gsettings-desktop-schemas gstreamer1.0-plugins-base gtk-update-icon-cache half hicolor-icon-theme hip-dev hip-doc
  hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev
  hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev humanity-icon-theme i965-va-driver icu-devtools intel-media-va-driver javascript-common lib32asan8 lib32atomic1 lib32gcc-13-dev
  lib32gcc-s1 lib32gomp1 lib32itm1 lib32quadmath0 lib32stdc++-13-dev lib32stdc++6 lib32ubsan1 libaacs0 libaec0 libalgorithm-diff-perl libalgorithm-diff-xs-perl libalgorithm-merge-perl libamd-comgr2 libamd3 libamdhip64-5 libaom3
  libarmadillo12 libarpack2t64 libasan8 libatk-bridge2.0-0t64 libatk1.0-0t64 libatomic1 libatspi2.0-0t64 libavahi-client3 libavahi-common-data libavahi-common3 libavcodec-dev libavcodec60 libavformat-dev libavformat60 libavutil-dev
  libavutil58 libbabeltrace1 libbdplus0 libbinutils libblas3 libblosc1 libbluray2 libc-dev-bin libc-devtools libc6-dbg libc6-dev libc6-dev-i386 libc6-dev-x32 libc6-i386 libc6-x32 libcairo-gobject2 libcairo2 libcamd3 libcc1-0
  libccolamd3 libcdparanoia0 libcfitsio10t64 libcharls2 libcholmod5 libchromaprint1 libcjson1 libcodec2-1.2 libcolamd3 libcolord2 libcrypt-dev libctf-nobfd0 libctf0 libcups2t64 libdatrie1 libdav1d7 libdc1394-25 libdc1394-dev
  libdconf1 libde265-0 libdebuginfod-common libdebuginfod1t64 libdeflate-dev libdeflate0 libdouble-conversion3 libdpkg-perl libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm-amdgpu-dev libdrm-amdgpu-radeon1 libdrm-amdgpu1
  libdrm-dev libdrm-intel1 libdrm-nouveau2 libdrm-radeon1 libdrm2-amdgpu libegl-mesa0 libegl1 libelf-dev libepoxy0 libevent-pthreads-2.1-7t64 libexif-dev libexif-doc libexif12 libexpat1-dev libfabric1 libfakeroot
  libfile-copy-recursive-perl libfile-fcntllock-perl libfile-listing-perl libfile-which-perl libfontconfig1 libfreetype6 libfreexl1 libfyba0t64 libgbm1 libgcc-13-dev libgd3 libgdal34t64 libgdcm-dev libgdcm3.0t64 libgdk-pixbuf-2.0-0
  libgdk-pixbuf2.0-bin libgdk-pixbuf2.0-common libgeos-c1t64 libgeos3.12.1t64 libgeotiff5 libgfortran5 libgif7 libgl-dev libgl1 libgl1-mesa-dri libgl2ps1.4 libglew2.2 libglvnd0 libglx-dev libglx-mesa0 libglx0 libgme0 libgomp1
  libgphoto2-6t64 libgphoto2-dev libgphoto2-l10n libgphoto2-port12t64 libgprofng0 libgraphite2-3 libgsm1 libgstreamer-plugins-base1.0-0 libgtk-3-0t64 libgtk-3-bin libgtk-3-common libharfbuzz0b libhdf4-0-alt libhdf5-103-1t64
  libhdf5-hl-100t64 libheif-plugin-aomdec libheif-plugin-aomenc libheif-plugin-libde265 libheif1 libhsa-runtime64-1 libhsakmt1 libhttp-date-perl libhwasan0 libhwloc-plugins libhwloc15 libhwy1t64 libice6 libicu-dev libigdgmm12
  libimath-3-1-29t64 libimath-dev libinput-bin libinput10 libipt2 libisl23 libitm1 libjbig-dev libjbig0 libjpeg-dev libjpeg-turbo8 libjpeg-turbo8-dev libjpeg8 libjpeg8-dev libjs-jquery libjs-sphinxdoc libjs-underscore libjsoncpp25
  libjxl0.7 libkmlbase1t64 libkmldom1t64 libkmlengine1t64 liblapack3 liblcms2-2 liblept5 liblerc-dev liblerc4 libllvm17t64 libllvm20 liblsan0 libltdl7 liblzma-dev libmbedcrypto7t64 libmd4c0 libminizip1t64 libmp3lame0 libmpc3
  libmpg123-0t64 libmtdev1t64 libmunge2 libmysqlclient21 libncurses-dev libnetcdf19t64 libnorm1t64 libnuma-dev libodbc2 libodbcinst2 libogdi4.1 libogg0 libopencv-calib3d-dev libopencv-calib3d406t64 libopencv-contrib-dev
  libopencv-contrib406t64 libopencv-core-dev libopencv-core406t64 libopencv-dev libopencv-dnn-dev libopencv-dnn406t64 libopencv-features2d-dev libopencv-features2d406t64 libopencv-flann-dev libopencv-flann406t64
  libopencv-highgui-dev libopencv-highgui406t64 libopencv-imgcodecs-dev libopencv-imgcodecs406t64 libopencv-imgproc-dev libopencv-imgproc406t64 libopencv-java libopencv-ml-dev libopencv-ml406t64 libopencv-objdetect-dev
  libopencv-objdetect406t64 libopencv-photo-dev libopencv-photo406t64 libopencv-shape-dev libopencv-shape406t64 libopencv-stitching-dev libopencv-stitching406t64 libopencv-superres-dev libopencv-superres406t64 libopencv-video-dev
  libopencv-video406t64 libopencv-videoio-dev libopencv-videoio406t64 libopencv-videostab-dev libopencv-videostab406t64 libopencv-viz-dev libopencv-viz406t64 libopencv406-jni libopenexr-3-1-30 libopenexr-dev libopengl0 libopenjp2-7
  libopenmpi3t64 libopenmpt0t64 libopus0 liborc-0.4-0t64 libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libpciaccess-dev libpciaccess0 libpcre2-16-0 libpgm-5.3-0t64 libpixman-1-0 libpkgconf3 libpmix2t64 libpng-dev
  libpng-tools libpoppler134 libpq5 libproj25 libprotobuf32t64 libpsm-infinipath1 libpsm2-2 libpthread-stubs0-dev libpython3-dev libpython3.12-dev libqhull-r8.0 libqt5core5t64 libqt5dbus5t64 libqt5gui5t64 libqt5network5t64
  libqt5opengl5t64 libqt5qml5 libqt5qmlmodels5 libqt5quick5 libqt5svg5 libqt5test5t64 libqt5waylandclient5 libqt5waylandcompositor5 libqt5widgets5t64 libquadmath0 librabbitmq4 librav1e0 libraw1394-11 libraw1394-dev libraw1394-tools
  librdmacm1t64 librist4 librsvg2-2 librsvg2-common librttopo1 libsframe1 libsharpyuv-dev libsharpyuv0 libshine3 libsm6 libsnappy1v5 libsocket++1 libsource-highlight-common libsource-highlight4t64 libsoxr0 libspatialite8t64
  libspeex1 libsrt1.5-gnutls libssh-gcrypt-4 libstdc++-13-dev libsuitesparseconfig7 libsuperlu6 libsvtav1enc1d1 libswresample-dev libswresample4 libswscale-dev libswscale7 libsz2 libtbb-dev libtbb12 libtbbbind-2-5 libtbbmalloc2
  libtesseract5 libthai-data libthai0 libtheora0 libtiff-dev libtiff6 libtiffxx6 libtimedate-perl libtk8.6 libtsan2 libtwolame0 libubsan1 libucx0 libudfread0 liburi-perl liburiparser1 libva-drm2 libva-x11-2 libva2 libvdpau1
  libvisual-0.4-0 libvorbis0a libvorbisenc2 libvorbisfile3 libvpl2 libvpx9 libvtk9.1t64 libvulkan1 libwacom-common libwacom9 libwayland-client0 libwayland-cursor0 libwayland-egl1 libwayland-server0 libwebp-dev libwebp7
  libwebpdecoder3 libwebpdemux2 libwebpmux3 libx11-dev libx11-xcb1 libx264-164 libx265-199 libx32asan8 libx32atomic1 libx32gcc-13-dev libx32gcc-s1 libx32gomp1 libx32itm1 libx32quadmath0 libx32stdc++-13-dev libx32stdc++6
  libx32ubsan1 libxau-dev libxcb-dri3-0 libxcb-glx0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-present0 libxcb-randr0 libxcb-render-util0 libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-sync1 libxcb-util1 libxcb-xfixes0
  libxcb-xinerama0 libxcb-xinput0 libxcb-xkb1 libxcb1-dev libxcomposite1 libxcursor1 libxdamage1 libxdmcp-dev libxerces-c3.2t64 libxfixes3 libxft2 libxi6 libxinerama1 libxkbcommon-x11-0 libxml2-dev libxnvctrl0 libxpm4 libxrandr2
  libxrender1 libxshmfence1 libxss1 libxtst6 libxvidcore4 libxxf86vm1 libzmq5 libzstd-dev libzvbi-common libzvbi0t64 linux-libc-dev lto-disabled-list make manpages-dev mesa-common-dev mesa-libgallium mesa-va-drivers
  mesa-vdpau-drivers mesa-vulkan-drivers migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev mysql-common ocl-icd-libopencl1 ocl-icd-opencl-dev opencl-c-headers opencl-clhpp-headers opencv-data openmp-extras-dev
  openmp-extras-runtime pkg-config pkgconf pkgconf-bin poppler-data proj-bin proj-data python3-argcomplete python3-dev python3-pip python3.12-dev qt5-gtk-platformtheme qttranslations5-l10n qtwayland5 rccl rccl-dev rocalution
  rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm rocm-cmake rocm-core rocm-dbgapi rocm-debug-agent rocm-developer-tools rocm-device-libs rocm-gdb rocm-hip rocm-language-runtime rocm-llvm rocm-opencl rocm-opencl-dev
  rocm-opencl-sdk rocm-openmp rocm-smi-lib rocminfo rocprim-dev rocprofiler rocprofiler-compute rocprofiler-dev rocprofiler-plugins rocprofiler-register rocprofiler-sdk rocprofiler-sdk-rocpd rocprofiler-sdk-roctx
  rocprofiler-systems rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev rocthrust-dev roctracer roctracer-dev rocwmma-dev rpcsvc-proto rpp rpp-dev session-migration ubuntu-mono unixodbc-common va-driver-all
  valgrind vdpau-driver-all x11-common x11proto-dev xorg-sgml-doctools xtrans-dev zlib1g-dev
0 upgraded, 602 newly installed, 0 to remove and 26 not upgraded.
Need to get 6192 MB of archives.
After this operation, 25.3 GB of additional disk space will be used.
```

---

### 评论 #4 — schung-amd (2025-12-22T16:18:33Z)

Hi @Qubitium, will poke around a bit to see what's still depending on those, but AFAICT the 32 bit libs are being pulled in by `gcc-multilib` and `g++-multilib`, not explicitly on our end.

---

### 评论 #5 — Qubitium (2025-12-22T17:03:22Z)

> Hi @Qubitium, will poke around a bit to see what's still depending on those, but AFAICT the 32 bit libs are being pulled in by `gcc-multilib` and `g++-multilib`, not explicitly on our end.

To reproduce exactly my setup, if necessary 

1. ubuntu 24.04 host
2. snap install lxd
3. lxd launch ubuntu24:04
4. run in new thin vm rocm install




---

### 评论 #6 — schung-amd (2026-02-10T16:19:29Z)

Sorry for the delay on this @Qubitium. `gcc-multilib` is in the recommended package list and not a dependency, so you can skip installing it and the related 32 bit libraries with `sudo apt install --no-install-recommends rocm`. You'll need to install any other recommended packages you want/need separately afterward. I don't see the recommended package list in your output, so for clarity, with `https://repo.radeon.com/amdgpu-install/7.1.1/ubuntu/noble/amdgpu-install_7.1.1.70101-1_all.deb`,
```
Recommended packages:
  python3-argcomplete libfile-copy-recursive-perl libfile-listing-perl libfile-which-perl liburi-perl libcholmod5
  libsuitesparseconfig7 libaacs0 manpages-dev libc-devtools libexif-doc proj-bin libgdk-pixbuf2.0-bin libgphoto2-l10n
  gstreamer1.0-plugins-base libheif-plugin-aomenc javascript-common opencv-data libopencv-java libpng-tools poppler-data
  qttranslations5-l10n libqt5svg5 qt5-gtk-platformtheme qtwayland5 libraw1394-tools librsvg2-common va-driver-all
  | va-driver vdpau-driver-all | vdpau-driver mesa-vulkan-drivers | vulkan-icd gcc g++ build-essential gcc-multilib
  g++-multilib gdb

```

---

### 评论 #7 — Qubitium (2026-02-11T08:12:05Z)

@schung-amd I have never used `--no-install-recommends` flag and didn't know it even exists. Since I do not understand how `-no-install-recommends` works, who is injecting `gcc-multilib` into the `recommended-list` which is installed (enabled) by default and actually not even required? Am I correct to say that `gcc-multilib` is not injected by `rocm` via the `recommend-list` property? I am curious at exactly which package is causing this gcc-multilib to be injected into the `recommended` list. 

---

### 评论 #8 — schung-amd (2026-02-11T16:26:59Z)

`gcc-multilib` is in the recommended list of `rocm-llvm`:
```
$ apt show rocm-llvm
Package: rocm-llvm
Version: 20.0.0.25444.70101-38~24.04
Priority: optional
Section: devel
Maintainer: ROCm Compiler Support <rocm.compiler.support@amd.com>
Installed-Size: unknown
Depends: python3, libc6, libstdc++6|libstdc++8, libstdc++-5-dev|libstdc++-7-dev|libstdc++-11-dev|libstdc++-12-dev|libstdc++-13-dev|libstdc++-14-dev, libgcc-5-dev|libgcc-7-dev|libgcc-11-dev|libgcc-12-dev|libgcc-13-dev|libgcc-14-dev, rocm-core
Recommends: gcc, g++, gcc-multilib, g++-multilib, rocm-device-libs
```
Since this is the compiler stack it makes sense for this package to recommend `gcc-multilib` for cross-compilation.

---

### 评论 #9 — schung-amd (2026-03-02T19:30:47Z)

Closing for now, let me know if you need anything else here and we can reopen if necessary.

---
