%define svndate	20110325
%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d
%define	static	%mklibname %{name} -d -s

%bcond_without	perl
%bcond_without	python

Summary:	A CPU identification tool and library
Name:		cpuinfo
Version:	1.0
Release:	%{?svndate:0.%{svndate}.}3
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
BuildRequires:	python-devel python-setuptools
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
Requires:	%{libname} = %{version}-%{release}
%rename		%{name}-devel

%description -n	%{devname}
This package contains headers and libraries needed to use cpuinfo's
processor characterisation features in your programs.

%package -n	%{static}
Summary:	Static library for cpuinfo
Group:		Development/C
Provides:	%{name}-static-devel = %{version}-%{release}
Requires:       %{devname} = %{version}-%{release}

%description -n	%{static}
This package contains static libraries needed to statically link cpuinfo's
processor characterisation features in your programs.

%if %{with perl}
%package -n	perl-Cpuinfo
Summary:	Perl bindings for cpuinfo
Group:		Development/Perl

%description -n	perl-Cpuinfo
Provides a Perl API to the cpuinfo library.
%endif

%if %{with python}
%package -n	python-cpuinfo
Summary:	Python bindings for cpuinfo
Group:		Development/Perl

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
LDFLAGS="%{ldflags}" %make

%install
%makeinstall_std

# nuke unpackaged files
find $RPM_BUILD_ROOT -name cpuinfo.pl -exec rm -f {} \;
find $RPM_BUILD_ROOT -name perllocal.pod -exec rm -f {} \;
find $RPM_BUILD_ROOT -name .packlist -exec rm -f {} \;

%files
%doc README COPYING NEWS
%{_bindir}/cpuinfo

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libcpuinfo.so.%{major}*

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
%{python_sitearch}/CPUInfo.so
%dir %{python_sitearch}/pycpuinfo-*.egg-info/
%{python_sitearch}/pycpuinfo-*.egg-info/*
%endif


%changelog
* Fri Mar 25 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0-0.20110325.1
+ Revision: 648432
- clean out old junk
- link with %%{ldflags}
- new snapshot

* Mon Nov 08 2010 Funda Wang <fwang@mandriva.org> 1.0-0.20090313.7mdv2011.0
+ Revision: 595031
- rebuild

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix so that it's possible to build with perl or python bindings

* Tue Nov 02 2010 Funda Wang <fwang@mandriva.org> 1.0-0.20090313.6mdv2011.0
+ Revision: 592111
- rebuild for py2.7

* Wed Jul 21 2010 Jérôme Quelin <jquelin@mandriva.org> 1.0-0.20090313.5mdv2011.0
+ Revision: 556337
- rebuild for perl 5.12

* Tue Nov 17 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0-0.20090313.4mdv2010.1
+ Revision: 466991
- split static library into a separate package
- don't report 64 bit if built for 32 bit (P501)
- add dependency on library package for devel package

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Thu Mar 19 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0-0.20090313.2mdv2009.1
+ Revision: 357588
- only report 64bit if PER_LINUX_32BIT personality isn't set (P0)

* Fri Mar 13 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0-0.20090313.1mdv2009.1
+ Revision: 354626
- add missing buildrequires
- build shared library, perl & python bindings
- update copyright tag
- cosmetics
  update to snapshot from my own bzr branch:
  	o adds python bindings
  	o adds feature detection of ancient features all the way back to
  	  'alignment check' to latest and greatest described in intel & amd manuals
  	o several improvements for making it easier for rpm5 to use library

* Thu Jan 17 2008 Olivier Blin <oblin@mandriva.com> 1.0-0.20070715.1mdv2008.1
+ Revision: 153914
- update to 20070715 snapshot
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed May 09 2007 Gwenole Beauchesne <gbeauchesne@mandriva.org> 1.0-0.20070509.1mdv2008.0
+ Revision: 25631
- update from SVN (2007/05/09):
  * add Perl bindings
  * fix detection of VIA processors (C3, C7)
  * fix detection of early AMD processors (K5, K6)
  * add more x86 feature flags (3dnow, sse4, popcnt)

* Wed Apr 18 2007 Gwenole Beauchesne <gbeauchesne@mandriva.org> 1.0-0.20070415.1mdv2008.0
+ Revision: 14616
- initial mandriva linux package


* Tue Feb 14 2006 Nicolas L�cureuil <neoclust@mandriva.org> 0.3-3mdk
- Fix BuildRequires

* Sat Feb 11 2006 Sebastien Savarin <plouf@mandriva.org> 0.3-2mdk
- Fix wrong perms

* Sat Feb 11 2006 Sebastien Savarin <plouf@mandriva.org> 0.3-1mdk
- First Mandriva Linux release

