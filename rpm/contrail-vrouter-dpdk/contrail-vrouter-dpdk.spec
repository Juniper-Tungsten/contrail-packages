%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%define     _contrailetc  /etc/contrail
%define     _distropkgdir %{_sbtop}tools/packages/rpm/%{name}

%if 0%{?_buildTag:1}
%define     _relstr %{_buildTag}
%else
%define     _relstr %(date -u +%y%m%d%H%M)
%endif

%if 0%{?_srcVer:1}
%define     _verstr %{_srcVer}
%else
%define     _verstr 1
%endif

%if 0%{?_opt:1}
%define         _sconsOpt      %{_opt}
%else
%define         _sconsOpt      debug
%endif

%if 0%{?_kVers:1}
%define         _kvers      %{_kVers}
%else
%define         _kvers      3.10.0-327.10.1.el7.x86_64
%endif

%if 0%{?_enableMellanox:1}
%define         _enableMlx %{_enableMellanox}
%else
%define         _enableMlx FALSE
%endif

%define         _kernel_dir /lib/modules/%{_kVers}/build

%if 0%{?_dpdk_build_dir:1}
%define         _dpdk_args --dpdk-dir=%{_dpdk_build_dir}
%else
%define         _dpdk_args %{nil}
%endif


%bcond_without debuginfo

Name:       contrail-vrouter-dpdk
Version:    %{_verstr}
Release:    %{_relstr}%{?dist}
Summary:    Contrail vrouter DPDK %{?_gitVer}

Group:      Applications/System
License:    Commercial
URL:        http://www.juniper.net/
Vendor:     Juniper Networks Inc

BuildRequires: boost-devel
BuildRequires: liburcu-devel
# kernel is required for /lib/modules content
%define is_rhel %(cat /etc/os-release | grep ^NAME | cut -d = -f 2 | sed  's/\"//g')
%if "%{is_rhel}" == "Red Hat Enterprise Linux Server"
BuildRequires: kernel = 3.10.0-1062.el7
BuildRequires: kernel-devel = 3.10.0-1062.el7
%else
BuildRequires: kernel = 3.10.0-1062.el7
BuildRequires: kernel-devel = 3.10.0-1062.el7
%endif
BuildRequires: numactl-devel
BuildRequires: libnl3-devel
BuildRequires: scons
BuildRequires: gcc
BuildRequires: flex
BuildRequires: bison
BuildRequires: gcc-c++
BuildRequires: libpcap
BuildRequires: libpcap-devel
%if 0%{?centos}
BuildRequires: python2-pip
BuildRequires: python3-pip
%endif
Requires: liburcu2
Requires: libnl3
Requires: numactl-libs
Requires: contrail-vrouter-utils >= %{_verstr}-%{_relstr}
%if %{_enableMlx} == "TRUE"
BuildRequires: rdma-core-devel
Requires: rdma-core
Requires: libibverbs
%define         _sconsAddOpts      enableMellanox
%else
%define         _sconsAddOpts      none
%endif


%description
Provides contrail-vrouter-dpdk binary

%if %{with debuginfo}
%debug_package
%endif

%prep
# Cleanup
pushd %{_sbtop}
RTE_KERNELDIR=%{_kernel_dir} scons -c \
    --opt=%{_sconsOpt} \
    --kernel-dir=%{_kernel_dir} \
    %{_dpdk_args} \
    --root=%{_builddir} \
    --add-opts=%{_sconsAddOpts} \
    vrouter/dpdk
popd

%build
pushd %{_sbtop}
RTE_KERNELDIR=%{_kernel_dir} scons \
    --opt=%{_sconsOpt} \
    --kernel-dir=%{_kernel_dir} \
    %{_dpdk_args} \
    --root=%{_builddir} \
    --add-opts=%{_sconsAddOpts} \
    vrouter/dpdk
popd

%install
# Install Directories
install -d -m 755 %{buildroot}/%{_bindir}
install -p -m 755 %{_sbtop}/build/%{_sconsOpt}/vrouter/dpdk/contrail-vrouter-dpdk %{buildroot}/%{_bindir}/contrail-vrouter-dpdk

%files
%defattr(-,root,root,-)
%{_bindir}/contrail-vrouter-dpdk


%changelog
* Thu Feb 16 2017 Nagendra Maynattamai <npchandran@juniper.net> 4.1.1-2.1contrail1
- Initial Build. Rebuilt with patches for Opencontrail
