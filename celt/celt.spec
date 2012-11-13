Name:          celt
Version:       0.11.1
Release:       4%{?dist}
Summary:       An audio codec for use in low-delay speech and audio communication

Group:         System Environment/Libraries
License:       BSD
URL:           http://www.celt-codec.org/
Source0:       http://downloads.us.xiph.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires: libogg-devel

%description
CELT (Constrained Energy Lapped Transform) is an ultra-low delay audio 
codec designed for realtime transmission of high quality speech and audio. 
This is meant to close the gap between traditional speech codecs 
(such as Speex) and traditional audio codecs (such as Vorbis). 

%package devel
Summary: Development package for celt
Group: Development/Libraries
Requires: libogg-devel
Requires: celt = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with celt.

%prep
%setup -q

%build
%configure --enable-custom-modes
# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

rm %{buildroot}%{_libdir}/*.a
rm %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_bindir}/celtenc
%{_bindir}/celtdec
%{_libdir}/libcelt0.so.2
%{_libdir}/libcelt0.so.2.0.0

%files devel
%defattr(-,root,root,-)
%doc COPYING README
%{_includedir}/celt
%{_libdir}/pkgconfig/celt.pc
%{_libdir}/libcelt0.so

%changelog
* Tue Nov 13 2012 Liu Di <liudidi@gmail.com> - 0.11.1-4
- 为 Magic 3.0 重建

