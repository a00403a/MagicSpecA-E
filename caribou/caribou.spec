Name:           caribou
Version:        0.4.1
Release:        5%{?dist}
Summary:        A simplified in-place on-screen keyboard

Group:          User Interface/Desktops
License:        LGPLv2+
URL:            http://live.gnome.org/Caribou
Source0:        http://download.gnome.org/sources/caribou/0.4/caribou-%{version}.tar.xz
Patch0:         caribou-0.4.1-multilib.patch

BuildRequires:  python-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  pygobject3-devel
BuildRequires:  intltool
BuildRequires:  gnome-doc-utils
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  clutter-devel
BuildRequires:  vala-devel
BuildRequires:  libXtst-devel
BuildRequires:  libxklavier-devel
BuildRequires:  libgee06-devel
BuildRequires:  gobject-introspection-devel

Requires:       pygobject3
Requires:       pyatspi

#Following is needed as package moved from noarch to arch
Obsoletes:      caribou < 0.4.1-3

%description
Caribou is a text entry application that currently manifests itself as
a simplified in-place on-screen keyboard.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package     -n python-caribou
Summary:        Keyboard UI for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3
BuildArch:      noarch

%description  -n python-caribou
This package contains caribou python GUI

%package        gtk2-module
Summary:        Gtk2 im module for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3

%description    gtk2-module
This package contains caribou im module for gtk2

%package        gtk3-module
Summary:        Gtk3 im module for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3

%description    gtk3-module
This package contains caribou im module for gtk3

%package        antler
Summary:        Keyboard implementation for %{name}
Group:          User Interface/Desktops
Requires:       %{name} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3

%description    antler
This package contains caribou keyboard implementation

%prep
%setup -q
%patch0 -p1 -b .multilib

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

echo "NoDisplay=true" >> $RPM_BUILD_ROOT%{_datadir}/applications/caribou.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/caribou.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop || :
desktop-file-validate $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/caribou-gtk-module.desktop || :

%find_lang caribou

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f caribou.lang
%doc NEWS COPYING README
%{_bindir}/caribou
%{_bindir}/caribou-preferences
%{_datadir}/caribou
%{_libdir}/girepository-1.0/Caribou-1.0.typelib
%{_datadir}/applications/caribou.desktop
%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.caribou.gschema.xml
%{_libdir}/libcaribou.so.0*
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/caribou-gtk-module.desktop

%files -n python-caribou
%{python_sitelib}/caribou

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/gir-1.0/Caribou-1.0.gir

%files gtk2-module
%{_libdir}/gtk-2.0/modules/libcaribou-gtk-module.so

%files gtk3-module
%{_libdir}/gtk-3.0/modules/libcaribou-gtk-module.so

%files antler
%{_datadir}/antler
%{_datadir}/dbus-1/services/org.gnome.Caribou.Antler.service
%{_libexecdir}/antler-keyboard
%{_datadir}/glib-2.0/schemas/org.gnome.antler.gschema.xml


%changelog
* Tue Feb 07 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.1-5
- Resolves:rh#768033 - Update Requires for caribou

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.1-3
- split package to subpackages -gtk2-module, -gtk3-module, -antler and python-caribou

* Thu Nov 17 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.1-2
- Resolves:rh#753149 - Upgraded F15 -> F16 gnome fails - wrong version of caribou

* Tue Oct 18 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.1-1
- upstream release 0.4.1

* Tue Sep 27 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.0-1
- upstream release 0.4.0

* Tue Sep 20 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.92-1
- upstream release 0.3.92

* Tue Sep 06 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.91-1
- Update to new upstream release 0.3.91

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.5-2
- Rebuild with pygobject3

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.5-1
- Update to 0.3.5

* Tue Jul 05 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.3-1
- Update to new upstream release 0.3.3

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.3.2-2
- Tweak BuildRequires

* Tue Jun 14 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.2-1
- Update to new upstream release 0.3.2

* Fri May  6 2011 Christopher Aillon <caillon@redhat.com> - 0.2.00-3
- Update scriptlets per packaging guidelines

* Thu May 05 2011 Parag Nemade <pnemade AT redhat.com> - 0.2.00-2
- Caribou now only be shown in GNOME. (rh#698603)
- Add desktop-file-validate for caribou-autostart.desktop
- Add ||: for caribou-autostart.desktop to skip the error.

* Tue Apr  5 2011 Matthias Clasen <mclasen@redhat.com> - 0.2.00-1
- Update to 0.2.00

* Tue Mar 22 2011 Parag Nemade <pnemade AT redhat.com> - 0.1.92-1
- Update to 0.1.92

* Thu Mar 10 2011 Parag Nemade <pnemade AT redhat.com> - 0.1.91-1
- Update to 0.1.91

* Thu Mar 10 2011 Parag Nemade <pnemade AT redhat.com> - 0.1.7-1
- Update to 0.1.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Wed Jun 16 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.2-3
- Require pyatspi, not at-spi-python

* Sat May 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.2-2
- Rewrite spec for autotools

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.2-1
- Update to 0.1.2

* Thu Jan 21 2009 Ben Konrath <ben@bagu.org> - 0.0.2-1
- Initial release.
