%define name	cpuinfo
%define version	1.0
%define svndate	20070509
%define rel	1
%define release	%mkrel %{?svndate:0.%{svndate}.}%{rel}

# Define to build shared libraries
# XXX libify when API is declared stable and shared libs are enabled
%define build_shared 0
%{expand: %{?_with_shared:	%%global build_shared 1}}
%{expand: %{?_without_shared:	%%global build_shared 0}}

# Define to build perl bindings
%define build_perl 1
%{expand: %{?_with_perl:	%%global build_perl 1}}
%{expand: %{?_without_perl:	%%global build_perl 0}}

Summary:	A CPU identification tool and library
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}%{?svndate:-%{svndate}}.tar.bz2
Patch0:		cpuinfo-1.0-mdvconfig.patch
License:	GPL
Group:		System/Kernel and hardware
Url:		http://gwenole.beauchesne.info/projects/cpuinfo/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
ExclusiveArch:	%{ix86} x86_64 ppc ppc64 ia64 mips
%if %{build_perl}
BuildRequires:	perl-devel
%endif

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

%package -n perl-Cpuinfo
Summary:	Perl bindings for cpuinfo
Group:		Development/Perl

%description -n perl-Cpuinfo
Provides a Perl API to the cpuinfo library.

%prep
%setup -q
%patch0 -p1 -b .mdvconfig

%build
%configure \
%if %{build_shared}
	--enable-shared \
%endif
%if %{build_perl}
	--enable-perl \
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
%if %{build_shared}
%{_libdir}/libcpuinfo.so.*
%endif

%files devel
%defattr(-,root,root)
%{_includedir}/cpuinfo.h
%{_libdir}/libcpuinfo.a
%if %{build_shared}
%{_libdir}/libcpuinfo.so
%endif

%if %{build_perl}
%files -n perl-Cpuinfo
%defattr(-,root,root)
%doc src/bindings/perl/cpuinfo.pl
%{perl_vendorarch}/Cpuinfo.pm
%dir %{perl_vendorarch}/auto/Cpuinfo
%{perl_vendorarch}/auto/Cpuinfo/*
%endif

%changelog
