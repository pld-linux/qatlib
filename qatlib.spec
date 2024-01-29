#
# Conditional build:
%bcond_without	asm		# fast CRC in assembler
%bcond_without	static_libs	# static libraries

# quickassist/lookaside/access_layer/src/common/compression/{crc32_gzip_refl_by8,crc64_ecma_norm_by8}.S is 64-bit only
%ifnarch %{x8664}
%undefine	with_asm
%endif
Summary:	Intel QuickAssist Technology library
Summary(pl.UTF-8):	Biblioteka Intel QuickAssist Technology
Name:		qatlib
Version:	23.11.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/intel/qatlib/releases
Source0:	https://github.com/intel/qatlib/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b9220c0a97dab26c763e5644fde98791
Patch0:		%{name}-types.patch
URL:		https://github.com/intel/qatlib
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool >= 2:2.4
%{?with_asm:BuildRequires:	nasm}
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	systemd-devel
# x86_64-specific hardware, allow userspace libs for all ABIs
ExclusiveArch:	%{ix86} %{x8664} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Intel(R) QuickAssist Technology (QAT) provides hardware acceleration
for offloading security, authentication and compression services from
the CPU, thus significantly increasing the performance and efficiency
of standard platform solutions.

Its services include symmetric encryption and authentication,
asymmetric encryption, digital signatures, RSA, DH and ECC, and
lossless data compression.

This package provides user space libraries that allow access to
Intel(R) QuickAssist devices and expose the Intel(R) QuickAssist APIs.

%description -l pl.UTF-8
Intel(R) QuickAssist Technology (QAT) zapewnia sprzętową akcelerację
przejmującą z procesora usługi bezpieczeństwa, uwierzytelniania i
kompresji, znacząco zwiększając wydajność standardowych rozwiązań.

Usługi obejmują szyfrowanie symetryczne i uwierzytelnianie,
szyfrowanie asymetryczne, podpisy cyfrowe, RSA, DH, ECC oraz
bezstratną kompresję danych.

Ten pakiet zawiera biblioteki przestrzeni użytkownika, pozwalające na
dostęp do urządzeń Intel(R) QuickAssist oraz udostępniające API
Intel(R) QuickAssist.

%package devel
Summary:	Header files for QATlib libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek QATlib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel

%description devel
Header files for QATlib libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek QATlib.

%package static
Summary:	Static QATlib libraries
Summary(pl.UTF-8):	Statyczne biblioteki QATlib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static QATlib libraries.

%description static -l pl.UTF-8
Statyczne biblioteki QATlib.

%package tools
Summary:	Tools to initialize and manage QAT devices
Summary(pl.UTF-8):	Narzędzia do inicjowania i zarządzania urządzeniami QAT
Group:		Applications/System
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(postun):	/usr/sbin/groupdel
Provides:	group(qat)

%description tools
Tools to initialize and manage QAT devices.

%description tools -l pl.UTF-8
Narzędzia do inicjowania i zarządzania urządzeniami QAT.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_asm:--disable-fast-crc-in-assembler} \
	--disable-silent-rules
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkgconfig
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%pre tools
%groupadd -g 268 qat

%postun tools
if [ "$1" = "0" ]; then
	%groupremove qat
fi

%files
%defattr(644,root,root,755)
%doc INSTALL LICENSE README.md
%attr(755,root,root) %{_libdir}/libqat.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqat.so.4
%attr(755,root,root) %{_libdir}/libusdm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libusdm.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqat.so
%attr(755,root,root) %{_libdir}/libusdm.so
%{_includedir}/qat
%{_pkgconfigdir}/libqat.pc
%{_pkgconfigdir}/libusdm.pc
%{_pkgconfigdir}/qatlib.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libqat.a
%{_libdir}/libusdm.a
%endif

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/qat_init.sh
%attr(755,root,root) %{_sbindir}/qatmgr
%{systemdunitdir}/qat.service
%{_mandir}/man8/qat_init.sh.8*
%{_mandir}/man8/qatmgr.8*
