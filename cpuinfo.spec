%define name	cpuinfo
%define version	1.0
%define svndate	20070415
%define rel	1
%define release	%{?svndate:0.%{svndate}.}%{rel}

Summary:	A CPU identification tool and library
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}%{?svndate:-%{svndate}}.tar.bz2
License:	GPL
Group:		System/Kernel and hardware
Url:		http://gwenole.beauchesne.info/projects/cpuinfo/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
ExclusiveArch:	%{ix86} x86_64 ppc ppc64 ia64 mips

%description
cpuinfo consists of an API/library used by programs to get information
about the underlying CPU. Such information includes CPU vendor, model
name, cache hierarchy, and supported features (e.g. CMP, SMT, and
SIMD). cpuinfo is also a standalone program to demonstrate the use of
this API.

%package devel
Summary:	Development files for cpuinfo
Group:		Development/C

%description devel
This package contains headers and libraries needed to use cpuinfo's
processor characterisation features in your programs.

%prep
%setup -q

%build
%configure --install-sdk
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README COPYING NEWS
%{_bindir}/cpuinfo

%files devel
%defattr(-,root,root)
%{_includedir}/cpuinfo.h
%{_libdir}/libcpuinfo.a

%changelog
