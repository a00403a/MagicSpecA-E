Summary: An Enchanting Spell Checking Library
Name: enchant
Version: 1.6.0
Release: 3%{?dist}
Epoch: 1
Group: System Environment/Libraries
License: LGPLv2+
Source: http://www.abisource.com/downloads/enchant/%{version}/enchant-%{version}.tar.gz
URL: http://www.abisource.com/
BuildRequires: glib2-devel >= 2.6.0
BuildRequires: aspell-devel
BuildRequires: hunspell-devel
BuildRequires: libvoikko-devel
BuildRequires: automake, libtool
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
A library that wraps other spell checking backends.

%package aspell
Summary: Integration with aspell for libenchant
Group: System Environment/Libraries
Requires: enchant = %{epoch}:%{version}-%{release}

%description aspell
Libraries necessary to integrate applications using libenchant with aspell.

%package voikko
Summary: Integration with voikko for libenchant
Group: System Environment/Libraries
Requires: enchant = %{epoch}:%{version}-%{release}

%description voikko
Libraries necessary to integrate applications using libenchant with voikko.


%package devel
Summary: Support files necessary to compile applications with libenchant.
Group: Development/Libraries
Requires: enchant = %{epoch}:%{version}-%{release}
Requires: glib2-devel

%description devel
Libraries, headers, and support files necessary to compile applications using libenchant.

%prep
%setup -q

%build
%configure --enable-myspell --with-myspell-dir=/usr/share/myspell --disable-static --disable-ispell --disable-hspell --disable-zemberek
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/enchant/*.la

%files
%defattr(-,root,root)
%doc AUTHORS COPYING.LIB README
%{_bindir}/*
%{_libdir}/lib*.so.*
%dir %{_libdir}/enchant
%{_libdir}/enchant/lib*myspell.so*
%{_mandir}/man1/enchant.1.gz
%{_datadir}/enchant

%files aspell
%{_libdir}/enchant/lib*aspell.so*

%files voikko
%{_libdir}/enchant/lib*_voikko.so*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/enchant.pc
%{_includedir}/enchant

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -r $RPM_BUILD_ROOT

%changelog
* Thu Nov 17 2011 Liu Di <liudidi@gmail.com> - 1:1.6.0-3
- 为 Magic 3.0 重建

