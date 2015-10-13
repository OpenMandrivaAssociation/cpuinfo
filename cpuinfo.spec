%define svndate 20110325
%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define static %mklibname %{name} -d -s

%define _disable_lto 1

%bcond_without perl
%bcond_without python

Summary:	A CPU identification tool and library
Name:		cpuinfo
Version:	1.0
Release:	%{?svndate:0.%{svndate}.}7
# based on branch at https://code.launchpad.net/cpuinfo/trunk, please don't
# replace until merged upstream
Source0:	%{name}-%{version}%{?svndate:-%{svndate}}.tar.xz
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://gwenole.beauchesne.info/projects/cpuinfo/
ExclusiveArch:	%{ix86} x86_64 ppc ppc64 ia64
%if %{with perl}
BuildRequires:	perl-devel
%endif
%if %{with python}
BuildRequires:	pkgconfig(python2)
BuildRequires:	python2-setuptools
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
License:	LGPLv2.1+

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with cpuinfo.

%package -n	%{devname}
Summary:	Development files for cpuinfo
Group:		Development/C
License:	LGPLv2.1+
Requires:	%{libname} = %{version}-%{release}
%rename		%{name}-devel

%description -n	%{devname}
This package contains headers and libraries needed to use cpuinfo's
processor characterisation features in your programs.

%package -n	%{static}
Summary:	Static library for cpuinfo
Group:		Development/C
License:	LGPLv2.1+
Provides:	%{name}-static-devel = %{version}-%{release}
Requires:       %{devname} = %{version}-%{release}

%description -n	%{static}
This package contains static libraries needed to statically link cpuinfo's
processor characterisation features in your programs.

%if %{with perl}
%package -n	perl-Cpuinfo
Summary:	Perl bindings for cpuinfo
Group:		Development/Perl
License:	GPLv2+

%description -n	perl-Cpuinfo
Provides a Perl API to the cpuinfo library.
%endif

%if %{with python}
%package -n	python-cpuinfo
Summary:	Python bindings for cpuinfo
Group:		Development/Perl
License:	GPLv2+

%description -n python-cpuinfo
Provides a Python API to the cpuinfo library.
%endif

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
sed -i 's|python setup.py|%{__python2} setup.py|g' Makefile

LDFLAGS="%{ldflags}" %make

%install
%makeinstall_std

mkdir %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libcpuinfo.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libcpuinfo.so.%{major}.*.* %{buildroot}%{_libdir}/libcpuinfo.so

# nuke unpackaged files
find %{buildroot} -name cpuinfo.pl -exec rm -f {} \;

%files
%doc README NEWS
%{_bindir}/cpuinfo

%files -n %{libname}
/%{_lib}/libcpuinfo.so.%{major}*

%files -n %{devname}
%{_includedir}/cpuinfo.h
%{_libdir}/pkgconfig/libcpuinfo.pc
%{_libdir}/libcpuinfo.so

%files -n %{static}
%{_libdir}/libcpuinfo.a

%if %{with perl}
%files -n perl-Cpuinfo
%doc src/bindings/perl/cpuinfo.pl
%{perl_vendorarch}/Cpuinfo.pm
%dir %{perl_vendorarch}/auto/Cpuinfo
%{perl_vendorarch}/auto/Cpuinfo/*
%endif

%if %{with python}
%files -n python-cpuinfo
%{python2_sitearch}/CPUInfo.so
%dir %{python2_sitearch}/pycpuinfo-*.egg-info/
%{python2_sitearch}/pycpuinfo-*.egg-info/*
%endif

