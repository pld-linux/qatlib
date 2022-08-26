# NOTE: 22.07.0 no longer supports 32-bit ABI
Summary:	Intel QuickAssist Technology library
Summary(pl.UTF-8):	Biblioteka Intel QuickAssist Technology
Name:		qatlib
Version:	21.11.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/intel/qatlib/releases
Source0:	https://github.com/intel/qatlib/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3e47ec666c1e0499c42558505a80e054
Patch0:		%{name}-types.patch
URL:		https://github.com/intel/qatlib
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool >= 2:2.4
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
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%attr(755,root,root) %ghost %{_libdir}/libqat.so.2
%attr(755,root,root) %{_libdir}/libusdm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libusdm.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqat.so
%attr(755,root,root) %{_libdir}/libusdm.so
%{_libdir}/libqat.la
%{_libdir}/libusdm.la
%{_includedir}/qat

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/qat_init.sh
%attr(755,root,root) %{_sbindir}/qatmgr
%{systemdunitdir}/qat.service
%{_mandir}/man8/qat_init.sh.8*
%{_mandir}/man8/qatmgr.8*
