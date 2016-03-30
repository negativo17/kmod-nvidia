%global kmod_name nvidia

%global debug_package %{nil}

# Build flags are inherited from the kernel
%undefine _auto_set_build_flags

%{!?kversion: %global kversion %(uname -r)}

Name:           kmod-%{kmod_name}
Version:        595.71.05
Release:        1%{?dist}
Summary:        NVIDIA display driver kernel module
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/
ExclusiveArch:  x86_64 aarch64

Source0:        https://github.com/NVIDIA/open-gpu-kernel-modules/archive/%{version}/open-gpu-kernel-modules-%{version}.tar.gz

BuildRequires:  elfutils-libelf-devel
BuildRequires:  gcc
# The run file contains precompiled C++ code for the open modules:
#   kernel-open/nvidia/nv-kernel.o_binary
#   kernel-open/nvidia-modeset/nv-modeset-kernel.o_binary
# The full open tarball requires also a c++ compiler to build those bits:
BuildRequires:  gcc-c++
BuildRequires:  kernel-devel
BuildRequires:  kernel-rpm-macros
BuildRequires:  kmod
BuildRequires:  redhat-rpm-config

Provides:       %{kmod_name}-kmod = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       module-init-tools
Requires:       kernel-uname-r = %{kversion}

%description
This package provides the proprietary NVIDIA kernel modules. It is built to
depend upon the specific ABI provided by a range of releases of the same variant
of the Linux kernel and not on any one specific build.

%prep
%autosetup -p1 -n open-gpu-kernel-modules-%{version}

%build
export SYSSRC=%{_usrsrc}/kernels/%{kversion}
export IGNORE_XEN_PRESENCE=1
export IGNORE_PREEMPT_RT_PRESENCE=1
export IGNORE_CC_MISMATCH=1
export EXTRA_CFLAGS+=" -Wno-incompatible-pointer-types"

%make_build modules

%install
export INSTALL_MOD_PATH=%{buildroot}%{_prefix}
export INSTALL_MOD_DIR=extra/%{kmod_name}

make -C %{_usrsrc}/kernels/%{kversion} -j$(nproc) modules_install M=$PWD/kernel-open

# Remove the unrequired files.
rm -f %{buildroot}%{_prefix}/lib/modules/%{kversion}/modules.*

find %{buildroot} -type f -name '*.ko' | xargs %{__strip} --strip-debug
find %{buildroot} -type f -name '*.ko' | xargs xz

%post
if [ -e "/boot/System.map-%{kversion}" ]; then
    %{_sbindir}/depmod -aeF "/boot/System.map-%{kversion}" "%{kversion}" > /dev/null || :
fi

%postun
if [ -e "/boot/System.map-%{kversion}" ]; then
    %{_sbindir}/depmod -aeF "/boot/System.map-%{kversion}" "%{kversion}" > /dev/null || :
fi

%files
%{_prefix}/lib/modules/%{kversion}/extra/*

%changelog
* Tue Apr 28 2026 Simone Caronni <negativo17@gmail.com> - 3:595.71.05-1
- Update to 595.71.05.

* Tue Mar 24 2026 Simone Caronni <negativo17@gmail.com> - 3:595.58.03-1
- Update to 595.58.03.

* Thu Mar 05 2026 Simone Caronni <negativo17@gmail.com> - 3:595.45.04-1
- Update to 595.45.04.

* Thu Dec 18 2025 Simone Caronni <negativo17@gmail.com> - 3:590.48.01-1
- Update to 590.48.01.
