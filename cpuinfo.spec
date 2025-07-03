Summary:        A library to detect information about host CPU
Name:           cpuinfo
License:        BSD-2-Clause
Version:        25.06.26
Release:        1
URL:            https://github.com/pytorch/%{name}
Source0:        https://github.com/pytorch/cpuinfo/archive/refs/heads/cpuinfo-main.zip

ExclusiveArch:  x86_64 aarch64

BuildRequires:  cmake
BuildRequires:  make

%description
cpuinfo is a library to detect essential for performance
optimization information about host CPU.

Features
* Cross-platform availability:
  * Linux, Windows, macOS, Android, and iOS operating systems
  * x86, x86-64, ARM, and ARM64 architectures
* Modern C/C++ interface
  * Thread-safe
  * No memory allocation after initialization
  * No exceptions thrown
* Detection of supported instruction sets, up to AVX512 (x86)
  and ARMv8.3 extensions
* Detection of SoC and core information:
  * Processor (SoC) name
  * Vendor and microarchitecture for each CPU core
  * ID (MIDR on ARM, CPUID leaf 1 EAX value on x86) for each CPU core
* Detection of cache information:
  * Cache type (instruction/data/unified), size and line size
  * Cache associativity
  * Cores and logical processors (hyper-threads) sharing the cache
* Detection of topology information (relative between logical
  processors, cores, and processor packages)
* Well-tested production-quality code:
  * 60+ mock tests based on data from real devices
  * Includes work-arounds for common bugs in hardware and OS kernels
  * Supports systems with heterogenous cores, such as big.LITTLE and Max.Med.Min
* Permissive open-source license (Simplified BSD)

%package devel
Summary:        Headers and libraries for cpuinfo
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the developement libraries and headers
for cpuinfo.

%prep
%autosetup -p1 -n %{name}-%{commit0}

# Patch the version patch
sed -i -e 's@cpuinfo_VERSION 23.11.04@cpuinfo_VERSION %{version}@' CMakeLists.txt

%build
%cmake \
    -DCPUINFO_BUILD_UNIT_TESTS=OFF \
    -DCPUINFO_BUILD_MOCK_TESTS=OFF \
    -DCPUINFO_BUILD_BENCHMARKS=OFF

%make_build

%install
%make_install -C build

rm -rf %{buildroot}/%{_includedir}/gmock
rm -rf %{buildroot}/%{_includedir}/gtest
rm -rf %{buildroot}/%{_libdir}/cmake/GTest
rm -rf %{buildroot}/%{_libdir}/libgmock*
rm -rf %{buildroot}/%{_libdir}/libgtest*
rm -rf %{buildroot}/%{_libdir}/pkgconfig/gmock*
rm -rf %{buildroot}/%{_libdir}/pkgconfig/gtest*

%files
%license LICENSE
%{_bindir}/isa-info
%{_bindir}/cpu-info
%{_bindir}/cache-info
%ifarch x86_64
%{_bindir}/cpuid-dump
%endif
%{_libdir}/lib%{name}.so.*

%files devel
%doc README.md
%dir %{_datadir}/%{name}
%{_includedir}/%{name}.h
%{_datadir}/%{name}/%{name}-*.cmake
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/lib%{name}.pc
