%define         clutter_version 1.0

Name:           clutter-gtk
Version:        1.0.4
Release:        1%{?dist}
Summary:        A basic GTK clutter widget

Group:          Development/Languages
License:        LGPLv2+
URL:            http://www.clutter-project.org
Source0:        http://www.clutter-project.org/sources/%{name}/1.0/%{name}-%{version}.tar.xz
Patch0:         clutter-gtk-fixdso.patch

BuildRequires:  gtk3-devel >= 3.0.0
BuildRequires:  clutter-devel
BuildRequires:  gobject-introspection-devel

%description
This allows clutter to be embedded in GTK applications.
We hope with further work in the future clutter-gtk will
also allow the reverse, namely embedding GTK in Clutter

%package devel
Summary:        Clutter-gtk development environment
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gtk3-devel clutter-devel

%description devel
Header files and libraries for building a extension library for the
clutter-gtk


%prep
%setup -q
#%patch0 -p1 -b .fixdso


%build
%configure
make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang cluttergtk-1.0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f cluttergtk-1.0.lang
%doc COPYING NEWS
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GtkClutter-%{clutter_version}.typelib

%files devel
%{_includedir}/clutter-gtk-%{clutter_version}/
%{_libdir}/pkgconfig/clutter-gtk-%{clutter_version}.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/GtkClutter-%{clutter_version}.gir
%{_datadir}/gtk-doc/html/clutter-gtk-1.0

%changelog
* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1.0.4-1
- Update to 1.0.4

* Tue Sep 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.2-4
- Rebuild for clutter 1.8.0 again

* Tue Sep 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.2-3
- Rebuild for clutter 1.8.0

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> 1.0.2-2
- Rebuild

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> 1.0.2-1
- Update to 1.0.2

* Tue Apr  5 2011 Matthias Clasen <mclasen@redhat.com> 1.0.0-1
- Update to 1.0.0

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 0.91.8-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 0.91.8-2
- Rebuild against newer gtk

* Fri Jan 14 2011 Matthias Clasen <mclasen@redhat.com> 0.91.8-1
- Update to 0.91.8

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 0.91.6-2
- Rebuild against GTK+ 2.99.0

* Tue Dec 28 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.91.6-1
- Update to 0.91.6
- Fix deps and other bits of spec file

* Wed Dec 22 2010 Dan Horák <dan[at]danny.cz> - 0.91.4-2
- Update to recent gtk (FTBFS)

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 0.91.4-1
- Update to 0.91.4

* Sun Oct 10 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.91.2-1
- Update to 0.91.2

* Wed Sep 29 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.90.2-3
- Add upstream patches to compile with latest gobject-introspection

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> 0.90.2-2
- Rebuild against newer gobject-introspection

* Wed Sep  1 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.90.2-1
- Update to 0.90.2

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.10.4-5
- Rebuild with new gobject-introspection
- Drop gir-repository-devel

* Mon May  3 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.4-3
- cleanup removal of libtool archives

* Wed Mar 24 2010 Bastien Nocera <bnocera@redhat.com> 0.10.4-2
- Move the API docs to -devel

* Sun Mar 21 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.4-1
- Update to 0.10.4

* Wed Jul 29 2009 Bastien Nocera <bnocera@redhat.com> 0.10.2-1
- Update to 0.10.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Bastien Nocera <bnocera@redhat.com> 0.9.2-1
- Update to 0.9.2

* Sat Jun 20 2009 Bastien Nocera <bnocera@redhat.com> 0.9.0-2
- Rebuild for new clutter

* Tue May 26 2009 Bastien Nocera <bnocera@redhat.com> 0.9.0-1
- Update to 0.9.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild


* Fri Jan 23 2009 Allisson Azevedo <allisson@gmail.com> 0.8.2-2
- Rebuild

* Wed Oct 15 2008 Allisson Azevedo <allisson@gmail.com> 0.8.2-1
- Update to 0.8.2

* Sat Sep  6 2008 Allisson Azevedo <allisson@gmail.com> 0.8.1-1
- Update to 0.8.1

* Thu Jun 26 2008 Colin Walters <walters@redhat.com> 0.6.1-1
- Update to 0.6.1 so we can make tweet go
- Loosen files globs so we don't have to touch them every version

* Thu Feb 21 2008 Allisson Azevedo <allisson@gmail.com> 0.6.0-1
- Update to 0.6.0

* Mon Sep  3 2007 Allisson Azevedo <allisson@gmail.com> 0.4.0-1
- Update to 0.4.0

* Thu May 10 2007 Allisson Azevedo <allisson@gmail.com> 0.1.0-3
- fix devel files section

* Thu May 10 2007 Allisson Azevedo <allisson@gmail.com> 0.1.0-2
- INSTALL removed from docs
- fix make install for keeping timestamps
- fix devel files section
- changed license for LGPL

* Fri Apr 13 2007 Allisson Azevedo <allisson@gmail.com> 0.1.0-1
- Initial RPM release