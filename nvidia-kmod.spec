# Define the kmod package name here.
%global	kmod_name nvidia

# If kversion isn't defined on the rpmbuild line, define it here. For Fedora,
# kversion needs always to be defined as there is no kABI support.

# RHEL 7.9
%if 0%{?rhel} == 7
%{!?kversion: %global kversion 3.10.0-1160.6.1.el7}
%endif

# RHEL 8.3
%if 0%{?rhel} == 8
%{!?kversion: %global kversion 4.18.0-240.1.1.el8_3}
%endif

Name:           %{kmod_name}-kmod
Version:        450.80.02
Release:        2%{?dist}
Summary:        NVIDIA display driver kernel module
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/
ExclusiveArch:  x86_64

Source0:        %{kmod_name}-kmod-%{version}-x86_64.tar.xz
Source10:       kmodtool-%{kmod_name}-el6.sh

BuildRequires:  gcc
BuildRequires:  redhat-rpm-config
BuildRequires:  kernel-devel %{?kversion:== %{kversion}}
BuildRequires:  kernel-abi-whitelists %{?kversion:== %{kversion}}
BuildRequires:  kmod

%if 0%{?rhel} == 8
BuildRequires:  elfutils-libelf-devel
%endif

# Magic hidden here.
%global kmodtool sh %{SOURCE10}
%{expand:%(%{kmodtool} rpmtemplate %{kmod_name} %{kversion}.%{_target_cpu} "" 2>/dev/null)}

# Disable building of the debug package(s).
%global	debug_package %{nil}

%description
This package provides the proprietary NVIDIA OpenGL kernel driver module.
It is built to depend upon the specific ABI provided by a range of releases of
the same variant of the Linux kernel and not on any one specific build.

%prep
%autosetup -p1 -n %{kmod_name}-kmod-%{version}-x86_64

mv kernel/* .

echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build
export SYSSRC=%{_usrsrc}/kernels/%{kversion}.%{_target_cpu}
export IGNORE_XEN_PRESENCE=1
export IGNORE_PREEMPT_RT_PRESENCE=1
export IGNORE_CC_MISMATCH=1

make %{?_smp_mflags} module

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/%{kmod_name}
ksrc=%{_usrsrc}/kernels/%{kversion}.%{_target_cpu}
make -C "${ksrc}" modules_install M=$PWD

install -d %{buildroot}%{_sysconfdir}/depmod.d/
install kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
# Remove the unrequired files.
rm -f %{buildroot}/lib/modules/%{kversion}.%{_target_cpu}/modules.*

%changelog
* Mon Dec 07 2020 Simone Caronni <negativo17@gmail.com> - 3:450.80.02-2
- Drop support for CentOS/RHEL 6.

* Tue Oct 06 2020 Simone Caronni <negativo17@gmail.com> - 3:450.80.02-1
- Update to 450.80.02.

* Thu Aug 20 2020 Simone Caronni <negativo17@gmail.com> - 3:450.66-1
- Update to 450.66.

* Fri Jul 10 2020 Simone Caronni <negativo17@gmail.com> - 3:450.57-1
- Update to 450.57.

* Thu Jun 25 2020 Simone Caronni <negativo17@gmail.com> - 3:440.100-1
- Update to 440.100.

* Thu Apr 09 2020 Simone Caronni <negativo17@gmail.com> - 3:440.82-1
- Update to 440.82.

* Fri Feb 28 2020 Simone Caronni <negativo17@gmail.com> - 3:440.64-1
- Update to 440.64.

* Tue Feb 04 2020 Simone Caronni <negativo17@gmail.com> - 3:440.59-1
- Update to 440.59.

* Sun Feb 02 2020 Simone Caronni <negativo17@gmail.com> - 3:440.44-2
- Rebuild for CentOS/RHEL 8.1 kernels.

* Sat Dec 14 2019 Simone Caronni <negativo17@gmail.com> - 3:440.44-1
- Update to 440.44.

* Sat Nov 30 2019 Simone Caronni <negativo17@gmail.com> - 3:440.36-1
- Update to 440.36.

* Mon Nov 11 2019 Simone Caronni <negativo17@gmail.com> - 3:440.31-1
- Update to 440.31.

* Tue Oct 01 2019 Simone Caronni <negativo17@gmail.com> - 3:435.21-1
- Update to 435.21.

* Fri Sep 20 2019 Simone Caronni <negativo17@gmail.com> - 3:430.50-2
- Build for 7.7 kernels.

* Sat Sep 14 2019 Simone Caronni <negativo17@gmail.com> - 3:430.50-1
- Update to 430.50.

* Wed Jul 31 2019 Simone Caronni <negativo17@gmail.com> - 3:430.40-1
- Update to 430.40.

* Fri Jul 12 2019 Simone Caronni <negativo17@gmail.com> - 3:430.34-1
- Update to 430.34.

* Wed Jun 12 2019 Simone Caronni <negativo17@gmail.com> - 3:430.26-1
- Update to 430.26.

* Fri Jun 07 2019 Simone Caronni <negativo17@gmail.com> - 3:430.14-1
- Update to 430.14.

* Thu May 09 2019 Simone Caronni <negativo17@gmail.com> - 3:418.74-1
- Update to 418.74.

* Sun Mar 24 2019 Simone Caronni <negativo17@gmail.com> - 3:418.56-1
- Update to 418.56.
- Change logic for kernel versions.

* Fri Feb 22 2019 Simone Caronni <negativo17@gmail.com> - 3:418.43-1
- Update to 418.43.
- Trim changelog.

* Sun Feb 03 2019 Simone Caronni <negativo17@gmail.com> - 3:410.93-2
- Do not require nvidia-driver, require nvidia-kmod-common.

* Fri Jan 04 2019 Simone Caronni <negativo17@gmail.com> - 3:410.93-1
- Update to 410.93.

* Mon Nov 19 2018 Simone Caronni <negativo17@gmail.com> - 3:410.78-1
- Update to 410.78.

* Sun Nov 18 2018 Simone Caronni <negativo17@gmail.com> - 3:410.73-2
- Update for 7.6 kernel.

* Fri Oct 26 2018 Simone Caronni <negativo17@gmail.com> - 3:410.73-1
- Update to 410.73.

* Wed Oct 17 2018 Simone Caronni <negativo17@gmail.com> - 3:410.66-1
- Update to 410.66.

* Thu Sep 06 2018 Simone Caronni <negativo17@gmail.com> - 3:390.87-1
- Update to 390.87.

* Tue Jul 17 2018 Simone Caronni <negativo17@gmail.com> - 3:390.77-1
- Update to 390.77.

* Mon Jun 11 2018 Simone Caronni <negativo17@gmail.com> - 3:390.67-1
- Update to 390.67.

* Tue May 22 2018 Simone Caronni <negativo17@gmail.com> - 3:390.59-1
- Update to 390.59.

* Wed May 02 2018 Simone Caronni <negativo17@gmail.com> - 3:390.48-2
- Update for 7.5 kernel.

* Tue Apr 03 2018 Simone Caronni <negativo17@gmail.com> - 3:390.48-1
- Update to 390.48.

* Wed Mar 21 2018 Simone Caronni <negativo17@gmail.com> - 3:390.42-2
- Re-add kernel 4.15 patch.

* Thu Mar 15 2018 Simone Caronni <negativo17@gmail.com> - 3:390.42-1
- Update to 390.42.

* Tue Feb 27 2018 Simone Caronni <negativo17@gmail.com> - 3:390.25-3
- Update Epoch so packages do not overlap with RPMFusion.

* Wed Feb 21 2018 Simone Caronni <negativo17@gmail.com> - 2:390.25-2
- Add kernel 4.15 patch.

* Tue Jan 30 2018 Simone Caronni <negativo17@gmail.com> - 2:390.25-1
- Update to 390.25.

* Thu Jan 11 2018 Simone Caronni <negativo17@gmail.com> - 2:384.111-1
- Update to 384.111.
