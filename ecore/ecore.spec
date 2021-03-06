Name:           ecore
Version:        1.7.3
Release:        2%{?dist}
Summary:        Event/X abstraction layer
Group:          System Environment/Libraries
License:        MIT
URL:            http://web.enlightenment.org/p.php?p=about/efl&l=en
Source0:        http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
# Linux also needs to include <sys/time.h> and <sys/resources.h> for setpriority()
Patch0:		ecore-1.2.1-linux-priority.patch
BuildRequires:  eet-devel evas-devel libX11-devel libXext-devel libeina-devel 
BuildRequires:  libXcursor-devel libXrender-devel libxcb-devel 
BuildRequires:  libXinerama-devel libXrandr-devel libXScrnSaver-devel 
BuildRequires:  libXcomposite-devel libXfixes-devel libXdamage-devel 
BuildRequires:  xorg-x11-proto-devel SDL-devel gettext 
BuildRequires:  openssl-devel libcurl-devel chrpath doxygen pkgconfig
BuildRequires:	c-ares-devel tslib-devel

%description
Ecore is the event/X abstraction layer that makes doing selections,
Xdnd, general X stuff, event loops, timeouts and idle handlers fast,
optimized, and convenient.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       libcurl-devel openssl-devel
Requires:       evas-devel eet-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}
#%patch0 -p1 -b .linux-priority

%build
%configure --disable-static --enable-ecore-fb --enable-ecore-evas-fb --enable-ecore-sdl --disable-ecore-evas-directfb --disable-rpath --enable-openssl --disable-gnutls --enable-doc --enable-cares
## %%configure --disable-static --enable-ecore-fb --enable-ecore-sdl --enable-ecore-desktop
make %{?_smp_mflags}
cd doc; make doc %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'
chrpath --delete %{buildroot}%{_libdir}/lib%{name}_*.so*
find %{buildroot} -name '*.la' -delete
%find_lang %{name}

# remove unfinished manpages
find doc/man/man3 -size -100c -delete

for l in todo %{name}.dox
do
 rm -f doc/man/man3/$l.3
done 

chmod -x doc/html/*

mkdir -p %{buildroot}%{_mandir}/man3
install -Dpm0644 doc/man/man3/* %{buildroot}%{_mandir}/man3

# rename generic and conflicting manpages
mv %{buildroot}%{_mandir}/man3/Examples.3 %{buildroot}%{_mandir}/man3/ecore-Examples.3

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/libecore_*.so.*
%{_libdir}/libecore.so.*
%{_libdir}/ecore/

%files devel
%doc doc/html/*
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Aug  8 2012 Tom Callaway <spot@fedoraproject.org> - 1.2.1-2
- rename generic and conflicting manpages

* Thu Aug  2 2012 Tom Callaway <spot@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 12 2011 Tom Callaway <spot@fedoraproject.org> 1.0.1-2
- enable c-ares support

* Tue Jul 12 2011 Tom Callaway <spot@fedoraproject.org> 1.0.1-1
- update to 1.0.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-1
- final 1.0.0 release

* Wed Dec 15 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-0.1.beta3
- beta 3 release

* Tue Nov 16 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-0.1.beta2
- beta 2 release

* Fri Nov 05 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-0.1.beta1
- beta 1 release

* Fri Jul 02 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.49898-1
- ecore 0.9.9.49898 snapshot release

* Fri Jun 11 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.49539-1
- ecore 0.9.9.49539 snapshot release

* Mon Feb 15 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.063-1
- New upstream source 0.9.9.063

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.9.050-7
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.050-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.050-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.9.050-4
- rebuild with new openssl

* Wed Dec 17 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.050-3
- rebuilt

* Wed Dec 17 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.050-2
- Rebuilt

* Sat Nov 29 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.050-1
- New upstream snapshot

* Mon May 19 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.043-1
- New upstream snapshot
- Removed DirectFB backend, it's unmaintained upstream

* Wed May 14 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.042-4
- Added pkgconfig to buildrequires and ecore-devel requires

* Sun May 04 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.042-3
- Fixed ecore-devel dependencies once again

* Fri May 02 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.042-2
- Fixed ecore-devel dependencies
- Fixed timestamp of source tarball
- Preserve timestamps of installed files
- Added html docs

* Mon Apr 14 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.042-1
- Initial specfile for Ecore
