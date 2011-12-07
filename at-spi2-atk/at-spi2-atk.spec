Name:           at-spi2-atk
Version:        2.3.2
Release:        1%{?dist}
Summary:        A GTK+ module that bridges ATK to D-Bus at-spi

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
#VCS: git:git://git.gnome.org/at-spi-atk
Source0:        http://download.gnome.org/sources/at-spi2-atk/2.3/%{name}-%{version}.tar.xz

BuildRequires:  at-spi2-core-devel
BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel
BuildRequires:  atk-devel
BuildRequires:  gtk2-devel
BuildRequires:  intltool

Requires:       at-spi2-core

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

This package includes a gtk-module that bridges ATK to the new
D-Bus based at-spi.


%prep
%setup -q

%build
%configure --disable-relocate
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/libatk-bridge.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/modules/libatk-bridge.la

%find_lang %{name}

%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas

%files -f %{name}.lang
%doc COPYING AUTHORS README
%dir %{_libdir}/gtk-2.0
%dir %{_libdir}/gtk-2.0/modules
%{_libdir}/gtk-2.0/modules/libatk-bridge.so
%dir %{_libdir}/gtk-3.0
%dir %{_libdir}/gtk-3.0/modules
%{_libdir}/gtk-3.0/modules/libatk-bridge.so
%{_datadir}/glib-2.0/schemas/org.a11y.atspi.gschema.xml
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/at-spi2-atk.desktop


%changelog
* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.2-1
- Update to 2.3.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.1-1
- Update to 2.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for glibc bug#747377

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> 2.1.92-1
- Update to 2.1.92

* Mon Sep  5 2011 Matthias Clasen <mclasen@redhat.com> 2.1.91-1
- Update to 2.1.91

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> 2.1.90-1
- Update to 2.1.90

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> 2.1.5-1
- Update to 2.1.5

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> 2.1.4-1
- Update to 2.1.4

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> 2.0.1-1
- Update to 2.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> 2.0.0-1
- Update to 2.0.0

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> 1.91.93-1
- Update to 1.91.93

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> 1.91.92-1
- Update to 1.91.92

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> 1.91.91-1
- Update to 1.91.91

* Tue Feb 21 2011 Matthias Clasen <mclasen@redhat.com> 1.91.90-1
- Update to 1.91.90

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.91.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Bastien Nocera <bnocera@redhat.com> 1.91.6-3
- Add upstream patches to fix crashers

* Fri Feb 04 2011 Bastien Nocera <bnocera@redhat.com> 1.91.6-2
- Revert crashy part of 1.91.6 release

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 1.91.6-1
- Update to 1.91.6

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.5-1
- Update to 1.91.5

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.2-1
- Update to 1.91.2

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.0-1
- Update to 1.91.0

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.91.1-1
- Update to 0.3.91.1

* Fri Aug 27 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.90-2
- Make the gtk module resident to prevent crashes

* Wed Aug 18 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.90-1
- Update to 0.3.90

* Mon Aug  2 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.6-1
- Update to 0.3.6

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.5-1
- Update to 0.3.5

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.4-1
- Update to 0.3.4

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.3-1
- Update to 0.3.3
- Include gtk3 module
- Drop gtk deps, since we don't want to depend on both gtk2 and gtk3;
  instead own the directories

* Tue Jun  1 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.2-2
- Don't relocate the dbus a11y stack

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Sat May 15 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.1-1
- Update to 0.3.1

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.8-1
- Update to 0.1.8

* Sat Feb 20 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.7-1
- Update to 0.1.7

* Wed Feb 10 2010 Tomas Bzatek <tbzatek@redhat.com> - 0.1.6-1
- Update to 0.1.6

* Sun Jan 16 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Tue Dec 22 2009 Matthias Clasen <mclasen@redhat.com> - 0.1.4-1
- Update to 0.1.4

* Sat Dec  5 2009 Matthias Clasen <mclasen@redhat.com> - 0.1.3-1
- Initial packaging
