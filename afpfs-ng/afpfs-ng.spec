# No FUSE on RHEL5
%if %{?el5:1}0
%define _without_fuse 1
%endif

Name:           afpfs-ng
Version:        0.8.1
Release:        12%{?dist}.3
Summary:        Apple Filing Protocol client

Group:          System Environment/Base
License:        GPL+
URL:            http://alexthepuffin.googlepages.com/home
Source0:        http://downloads.sourceforge.net/afpfs-ng/%{name}-%{version}.tar.bz2
Patch0:         afpfs-ng-0.8.1-overflows.patch
Patch1:         afpfs-ng-0.8.1-pointer.patch
Patch2:		afpfs-ng-0.8.1-headers.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%{?!_without_fuse:BuildRequires: fuse-devel}
BuildRequires: libgcrypt-devel gmp-devel readline-devel


%description
A command line client to access files exported from Mac OS system via
Apple Filing Protocol.
%{?!_without_fuse:The FUSE filesystem module for AFP is in fuse-afp package}


%if %{?!_without_fuse:1}0
%package -n fuse-afp
Summary:        FUSE driver for AFP filesystem
Group:          System Environment/Base

%description -n fuse-afp
A FUSE file system server to access files exported from Mac OS system
via AppleTalk or TCP using Apple Filing Protocol.
The command line client for AFP is in fuse-afp package
%endif


%package devel
Summary:        Development files for afpfs-ng
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
Library for dynamic linking and header files of afpfs-ng.


%prep
%setup -q
%patch0 -p1 -b .overflows
%patch1 -p1 -b .pointer
%patch2 -p1

%build
# make would rebuild the autoconf infrastructure due to the following:
# Prerequisite `configure.ac' is newer than target `Makefile.in'.
# Prerequisite `aclocal.m4' is newer than target `Makefile.in'.
# Prerequisite `configure.ac' is newer than target `aclocal.m4'.
touch --reference aclocal.m4 configure.ac Makefile.in

%configure %{?_without_fuse:--disable-fuse} --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/afpfs-ng
cp -p include/* $RPM_BUILD_ROOT%{_includedir}/afpfs-ng


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/afpcmd
%{_bindir}/afpgetstatus
%{_mandir}/man1/afpcmd.1*
%{_mandir}/man1/afpgetstatus.1*
%{_libdir}/*.so.*
%exclude %{_libdir}/*.la
%doc COPYING AUTHORS ChangeLog docs/README docs/performance docs/FEATURES.txt docs/REPORTING-BUGS.txt


%if %{?!_without_fuse:1}0
%files -n fuse-afp
%defattr(-,root,root,-)
%{_bindir}/afp_client
%{_bindir}/afpfs
%{_bindir}/afpfsd
%{_bindir}/mount_afp
%{_mandir}/man1/afp_client.1*
%{_mandir}/man1/afpfsd.1*
%{_mandir}/man1/mount_afp.1*
%doc COPYING AUTHORS ChangeLog
%endif


%files devel
%defattr(-,root,root,-)
%{_includedir}/afpfs-ng
%{_libdir}/*.so


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.8.1-12.3
- 为 Magic 3.0 重建

* Tue Dec 04 2012 Liu Di <liudidi@gmail.com> - 0.8.1-11.3
- 为 Magic 3.0 重建

* Mon Apr 09 2012 Liu Di <liudidi@gmail.com> - 0.8.1-10.3
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-9.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.8.1-8.3
- rebuild with new gmp without compat lib

* Mon Oct 10 2011 Peter Schiffer <pschiffe@redhat.com> - 0.8.1-8.2
- rebuild with new gmp

* Mon Sep 26 2011 Peter Schiffer <pschiffe@redhat.com> - 0.8.1-8.1
- rebuild with new gmp

* Mon Jul  4 2011 Jan F. Chadima <jchadima@redhat.com> - 0.8.1-8
- Repair ponter arithmetic

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> - 0.8.1-6
- Rebuild with new fuse

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.8.1-4
- Don't refer to AppleTalk in Summary

* Tue Jul 14 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.8.1-3
- Fix up license tag

* Thu Mar 19 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.8.1-2
- Add more include files (Jan F. Chadima)
- Don't needlessly build static library (Stefan Kasal)
- Fix fuse-afp summary (Stefan Kasal)
- Remove redundant license file from -devel (Stefan Kasal)

* Mon Oct 6 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.8.1-1
- Initial packaging attempt
