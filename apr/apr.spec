%define aprver 1

# Arches on which the multilib apr.h hack is needed:
%define multilib_arches %{ix86} ia64 ppc ppc64 s390 s390x x86_64

Summary: Apache Portable Runtime library
Summary(zh_CN.UTF-8): Apache 可移植运行库
Name: apr
Version: 1.4.5
Release: 2%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://apr.apache.org/
Source0: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
Source1: apr-wrapper.h
Patch2: apr-1.2.2-locktimeout.patch
Patch3: apr-1.2.2-libdir.patch
Patch4: apr-1.2.7-pkgconf.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: autoconf, libtool, libuuid-devel, python
# To enable SCTP support
BuildRequires: lksctp-tools-devel

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.

%description -l zh_CN.UTF-8
Apache 可移植运行库。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: APR library development kit
Summary(zh_CN.UTF-8): %{name} 的开发包
Conflicts: subversion-devel < 0.20.1-2
Requires: apr = %{version}-%{release}, pkgconfig

%description devel
This package provides the support files which can be used to 
build applications using the APR library.  The mission of the
Apache Portable Runtime (APR) is to provide a free library of 
C data structures and routines.

%description devel -l zh_CN
%{name} 的开发包。

%prep
%setup -q
%patch2 -p1 -b .locktimeout
%patch3 -p1 -b .libdir
%patch4 -p1 -b .pkgconf

%build
# regenerate configure script etc.
./buildconf

# Forcibly prevent detection of shm_open (which then picks up but
# does not use -lrt).
export ac_cv_search_shm_open=no

%configure \
        --includedir=%{_includedir}/apr-%{aprver} \
        --with-installbuilddir=%{_libdir}/apr-%{aprver}/build \
        --with-devrandom=/dev/urandom
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/aclocal
install -m 644 build/find_apr.m4 $RPM_BUILD_ROOT/%{_datadir}/aclocal

# Trim exported dependecies
sed -ri '/^dependency_libs/{s,-l(uuid|crypt) ,,g}' \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.la
sed -ri '/^LIBS=/{s,-l(uuid|crypt) ,,g;s/  */ /g}' \
      $RPM_BUILD_ROOT%{_bindir}/apr-%{aprver}-config
sed -ri '/^Libs/{s,-l(uuid|crypt) ,,g}' \
      $RPM_BUILD_ROOT%{_libdir}/pkgconfig/apr-%{aprver}.pc

%ifarch %{multilib_arches}
# Ugly hack to allow parallel installation of 32-bit and 64-bit apr-devel 
# packages:
mv $RPM_BUILD_ROOT%{_includedir}/apr-%{aprver}/apr.h \
   $RPM_BUILD_ROOT%{_includedir}/apr-%{aprver}/apr-%{_arch}.h
install -c -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/apr-%{aprver}/apr.h
%endif

# Unpackaged files:
rm -f $RPM_BUILD_ROOT%{_libdir}/apr.exp \
      $RPM_BUILD_ROOT%{_libdir}/libapr-*.a

%check
# Fail if LFS support isn't present in a 32-bit build, since this
# breaks ABI and the soname doesn't change: see #254241
if grep 'define SIZEOF_VOIDP 4' include/apr.h \
   && ! grep off64_t include/apr.h; then
  cat config.log
  : LFS support not present in 32-bit build
  exit 1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE NOTICE
%{_libdir}/libapr-%{aprver}.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/APRDesign.html docs/canonical_filenames.html
%doc docs/incomplete_types docs/non_apr_programs
%{_bindir}/apr-%{aprver}-config
%{_libdir}/libapr-%{aprver}.*a
%{_libdir}/libapr-%{aprver}.so
%{_libdir}/pkgconfig/*.pc
%dir %{_libdir}/apr-%{aprver}
%dir %{_libdir}/apr-%{aprver}/build
%{_libdir}/apr-%{aprver}/build/*
%dir %{_includedir}/apr-%{aprver}
%{_includedir}/apr-%{aprver}/*.h
%{_datadir}/aclocal/*.m4

%changelog
* Sat Oct 29 2011 Liu Di <liudidi@gmail.com> - 1.4.5-2
- 升级到 1.4.5
