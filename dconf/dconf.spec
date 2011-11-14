%define glib2_version 2.27.2
%define vala_version 0.11.7

Name:           dconf
Version:        0.7.4
Release:        2%{?dist}
Summary:        A configuration system

Group:          System Environment/Base
License:        LGPLv2+
URL:            http://live.gnome.org/dconf
#VCS:           git:git://git.gnome.org/dconf
Source0:        http://download.gnome.org/sources/dconf/0.7/dconf-%{version}.tar.bz2

# https://bugzilla.gnome.org/show_bug.cgi?id=646220
Patch0: dconf-editor-crash.patch

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  dbus-devel
Requires:       dbus

BuildRequires:  gtk3-devel
BuildRequires:  libxml2-devel
BuildRequires:  vala-devel >= %{vala_version}
BuildRequires:  libgee-devel
# BuildRequires:  gobject-introspection-devel
# Bootstrap requirements
BuildRequires:  autoconf automake libtool
BuildRequires:  gtk-doc
BuildRequires:  vala
BuildRequires:  gobject-introspection-devel >= 0.9.6

%description
dconf is a low-level configuration system. Its main purpose is to provide a
backend to the GSettings API in GLib.

%package devel
Summary: Header files and libraries for dconf development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel >= %{glib2_version}

%description devel
dconf development package. Contains files needed for doing software
development using dconf.

%package editor
Summary: Configuration editor for dconf
Group:   Applications/System
Requires: %{name} = %{version}-%{release}

%description editor
docnf-editor allows you to browse and modify dconf databases.


%prep
%setup -q
%patch0 -p1 -b .editor-crash

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
	--disable-static \
)
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%post
/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules

%postun
/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/gio/modules/libdconfsettings.so
%{_libexecdir}/dconf-service
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_datadir}/dbus-1/system-services/ca.desrt.dconf.service
%{_bindir}/dconf
%{_libdir}/libdconf.so.*
%{_libdir}/libdconf-dbus-1.so.*
#%{_libdir}/girepository-1.0/dconf-1.0.typelib
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/dconf-bash-completion.sh


%files devel
%defattr(-,root,root,-)
%{_includedir}/dconf
%{_libdir}/libdconf.so
%{_libdir}/pkgconfig/dconf.pc
%{_includedir}/dconf-dbus-1
%{_libdir}/libdconf-dbus-1.so
%{_libdir}/pkgconfig/dconf-dbus-1.pc
# temporarily disable introspection until we have a new-enough goi
#%{_datadir}/gir-1.0/dconf-1.0.gir
%{_datadir}/gtk-doc/html/dconf
%{_datadir}/vala

%files editor
%defattr(-,root,root,-)
%{_bindir}/dconf-editor
%{_datadir}/applications/dconf-editor.desktop
%dir %{_datadir}/dconf-editor
%{_datadir}/dconf-editor/dconf-editor.ui

%changelog
* Fri May  6 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.4-1
- Update to 0.7.4

* Wed Apr  6 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.3-2
- Fix a crash in dconf-editor

* Tue Mar 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.2-3
- Rebuild for newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb  5 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Jan 17 2011 Matthias Clasen <mclasen@redhat.com> - 0.7-1
- Update to 0.7

* Wed Sep 29 2010 jkeating - 0.5.1-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 0.5.1-1
- Update to 0.5.1

* Thu Aug  5 2010 Matthias Clasen <mclasen@redhat.com> - 0.5-2
- Fix up shared library symlinks (#621733)

* Tue Aug  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.5-1
- Update to 0.5

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.2-1
- Update to 0.4.2

* Wed Jun 30 2010 Colin Walters <walters@verbum.org> - 0.4.1-2
- Changes to support snapshot builds

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 0.4.1-1
- Update to 0.4.1
- Include dconf-editor (in a subpackage)

* Wed Jun 23 2010 Matthias Clasen <mclasen@redhat.com> 0.4-2
- Rebuild against glib 2.25.9

* Sat Jun 12 2010 Matthias Clasen <mclasen@redhat.com> 0.4-1
- Update to 0.4

* Tue Jun 08 2010 Richard Hughes <rhughes@redhat.com> 0.3.2-0.1.20100608
- Update to a git snapshot so that users do not get a segfault in every
  application using GSettings.

* Wed Jun 02 2010 Bastien Nocera <bnocera@redhat.com> 0.3.1-2
- Rebuild against latest glib2

* Tue May 24 2010 Matthias Clasen <mclasen@redhat.com> 0.3.1-1
- Update to 0.3.1
- Add a -devel subpackage

* Fri May 21 2010 Matthias Clasen <mclasen@redhat.com> 0.3-3
- Make batched writes (e.g. with delayed settings) work

* Thu May 20 2010 Matthias Clasen <mclasen@redhat.com> 0.3-2
- Make the registration of the backend work

* Wed May 19 2010 Matthias Clasen <mclasen@redhat.com> 0.3-1
- Initial packaging
