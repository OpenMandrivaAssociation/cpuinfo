%define svndate	20090313
%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

%bcond_without	perl
%bcond_without	python

Summary:	A CPU identification tool and library
Name:		cpuinfo
Version:	1.0
Release:	%mkrel %{?svndate:0.%{svndate}.}1
# based on branch at https://code.launchpad.net/cpuinfo/trunk, please don't
# replace until merged upstream
Source0:	%{name}-%{version}%{?svndate:-%{svndate}}.tar.xz
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://gwenole.beauchesne.info/projects/cpuinfo/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
ExclusiveArch:	%{ix86} x86_64 ppc ppc64 ia64
%if %{with perl}
BuildRequires:	perl-devel
%endif
%if %{with python}
BuildRequires:	python-devel
%endif

%description
cpuinfo consists of an API/library used by programs to get information
about the underlying CPU. Such information includes CPU vendor, model
name, cache hierarchy, and supported features (e.g. CMP, SMT, and
SIMD). cpuinfo is also a standalone program to demonstrate the use of
this API.

%package -n	%{libname}
Summary:	Library for cpuinfo
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with cpuinfo.

%package -n	%{devname}
Summary:	Development files for cpuinfo
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel 

%description -n	%{devname}
This package contains headers and libraries needed to use cpuinfo's
processor characterisation features in your programs.

%package -n	perl-Cpuinfo
Summary:	Perl bindings for cpuinfo
Group:		Development/Perl

%description -n	perl-Cpuinfo
Provides a Perl API to the cpuinfo library.

%package -n	python-cpuinfo
Summary:	Python bindings for cpuinfo
Group:		Development/Perl

%description -n python-cpuinfo
Provides a Python API to the cpuinfo library.

%prep
%setup -q

%build
%configure \
	--enable-shared \
%if %{with perl}
	--enable-perl=vendor \
%endif
%if %{with python}
	--enable-python \
%endif
	--install-sdk
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# nuke unpackaged files
find $RPM_BUILD_ROOT -name cpuinfo.pl -exec rm -f {} \;
find $RPM_BUILD_ROOT -name perllocal.pod -exec rm -f {} \;
find $RPM_BUILD_ROOT -name .packlist -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README COPYING NEWS
%{_bindir}/cpuinfo

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libcpuinfo.so.%{major}*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/cpuinfo.h
%{_libdir}/libcpuinfo.a
%{_libdir}/pkgconfig/libcpuinfo.pc
%{_libdir}/libcpuinfo.so

%if %{with perl}
%files -n perl-Cpuinfo
%defattr(-,root,root)
%doc src/bindings/perl/cpuinfo.pl
%{perl_vendorarch}/Cpuinfo.pm
%dir %{perl_vendorarch}/auto/Cpuinfo
%{perl_vendorarch}/auto/Cpuinfo/*
%endif

%if %{with python}
%files -n python-cpuinfo
%defattr(-,root,root)
%{python_sitearch}/CPUInfo.so
%dir %{python_sitearch}/pycpuinfo-*.egg-info/
%{python_sitearch}/pycpuinfo-*.egg-info/*
%endif
