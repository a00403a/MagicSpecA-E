Name:           cheese
Epoch:          2
Version:        3.3.90
Release:        2%{?dist}
Summary:        Application for taking pictures and movies from a webcam

Group:          Amusements/Graphics
License:        GPLv2+
URL:            http://projects.gnome.org/cheese/
#VCS: git:git://git.gnome.org/cheese
Source0:        http://download.gnome.org/sources/cheese/3.3/%{name}-%{version}.tar.xz

BuildRequires: gtk3-devel >= 3.0.0
BuildRequires: gstreamer-devel >= 0.10.23
BuildRequires: gstreamer-plugins-base-devel >= 0.10.12
BuildRequires: cairo-devel >= 1.4.0
BuildRequires: librsvg2-devel >= 2.18.0
BuildRequires: evolution-data-server-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libXtst-devel
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: gnome-doc-utils
BuildRequires: intltool
BuildRequires: gnome-desktop3-devel >= 2.91.0
BuildRequires: libgudev1-devel
BuildRequires: libcanberra-devel
BuildRequires: scrollkeeper
BuildRequires: clutter-devel
BuildRequires: clutter-gtk-devel
BuildRequires: clutter-gst-devel
BuildRequires: libmx-devel
BuildRequires: vala-devel
BuildRequires: pkgconfig(gee-1.0)
BuildRequires: gnome-video-effects
BuildRequires: gnome-desktop3-devel
BuildRequires: chrpath
BuildRequires: itstool

Requires: gstreamer-plugins-good >= 0.10.6-2
Requires: gstreamer-plugins-bad-free
Requires: gnome-video-effects

%description
Cheese is a Photobooth-inspired GNOME application for taking pictures and
videos from a webcam. It can also apply fancy graphical effects.

%package libs
Summary:	Webcam display and capture widgets
Group:		System Environment/Libraries
License:	GPLv2+

%description libs
This package contains libraries needed for applications that
want to display a webcam in their interface.

%package libs-devel
Summary:	Development files for %{name}-libs
Group:		Development/Libraries
License:	GPLv2+
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description libs-devel
This package contains the libraries and header files that are needed
for writing applications that require a webcam display widget.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libcheese.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/libcheese-gtk.{a,la}

desktop-file-install --delete-original --vendor="" 	\
 	--dir=$RPM_BUILD_ROOT%{_datadir}/applications 	\
	--add-category X-AudioVideoImport		\
	$RPM_BUILD_ROOT%{_datadir}/applications/cheese.desktop

%find_lang %{name} --with-gnome

chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cheese
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libcheese-gtk.so.*

%post
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :


%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%post libs
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%postun libs
/sbin/ldconfig
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files
%doc AUTHORS COPYING README
%{_bindir}/cheese
%{_datadir}/applications/cheese.desktop
%{_datadir}/cheese
%{_datadir}/icons/hicolor/*/apps/cheese.png
%{_datadir}/icons/hicolor/*/actions/*.png
%{_datadir}/icons/hicolor/scalable/actions/*.svg
%{_mandir}/man1/cheese.1.gz
# FIXME find-lang is supposed to pick these up
%doc %{_datadir}/help/*/cheese

%files -f %{name}.lang libs
%{_libdir}/libcheese.so.*
%{_libdir}/libcheese-gtk.so.*
%{_datadir}/glib-2.0/schemas/org.gnome.Cheese.gschema.xml
%{_libdir}/girepository-1.0/Cheese-3.0.typelib

%files libs-devel
%doc COPYING
%{_libdir}/libcheese.so
%{_libdir}/libcheese-gtk.so
%{_includedir}/cheese/
%{_datadir}/gtk-doc/
%{_libdir}/pkgconfig/cheese.pc
%{_libdir}/pkgconfig/cheese-gtk.pc
%{_datadir}/gir-1.0/Cheese-3.0.gir

%changelog
* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 2:3.3.90-2
- Rebuild against new cogl

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 2:3.3.90-1
- Update to 3.3.90

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 2:3.3.5-1
- Update to 3.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 2:3.3.4-1
- Update to 3.3.4

* Mon Jan 16 2012 Matthias Clasen <mclasen@redhat.com> - 2:3.3.3-3
- Add a BuildRequires for itstool

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Matthias Clasen <mclasen@redhat.com> - 2:3.3.3-1
- Update to 3.3.3

* Thu Nov 24 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.3.2-2
- Rebuild against new clutter

* Tue Nov 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 1:3.3.2-1
- Update to 3.3.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.3.1-1
- Update to 3.3.1-1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.2.1-1
- Update to 3.2.1

* Thu Sep 29 2011 Hans de Goede <hdegoede@redhat.com> - 1:3.2.0-2
- Add Requires: gstreamer-plugins-bad-free for the camerabin element (#717872)

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1:3.2.0-1
- Update to 3.2.0

* Wed Sep 21 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:3.1.92-2
- Rebuld for new libcogl.
- Use old libgee api.

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.1.92-1
- Update to 3.1.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.1.91.1-1
- Update to 3.1.91.1

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.2-2
- Rebuild

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.2-1
- Update to 3.0.2

* Wed Jun 29 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1:3.0.1-3
- Removed RPATHS (RH #703636)

* Wed Jun 15 2011 Bastien Nocera <bnocera@redhat.com> 3.0.1-2
- Rebuild against newest gnome-desktop3

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> 1:3.0.1-1
- Update to 3.0.1

* Tue Apr  5 2011 Matthias Clasen <mclasen@redhat.com> 1:3.0.0-2
- Add newer icons from upstream

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> 1:3.0.0-1
- Update to 3.0

* Wed Mar 30 2011 Alexander Larsson <alexl@redhat.com> - 1:2.91.93-3
- Move gsettings schema to cheese-libs, fixes control-center crash (#691667)
- Move typelib to cheese-libs

* Mon Mar 28 2011 Bastien Nocera <bnocera@redhat.com> 2.91.93-2
- Add missing gnome-video-effects dependency

* Fri Mar 25 2011 Bastien Nocera <bnocera@redhat.com> 2.91.93-1
- Update to 2.91.93

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> 1:2.91.92-1
- Update to 2.91.92

* Sat Mar 12 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91.1-1
- Update to 2.91.91.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.91.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> 1:2.91.4-1
- Update to 2.91.4

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 1:2.91.3-1
- Update to 2.91.3

* Thu Sep 30 2010 Matthias Clasen <mclasen@redhat.com> 1:2.32.0-1
- Update to 2.32.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> 1:2.31.91-1
- Update to 2.31.91

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> 1:2.31.90-2
- Co-own /usr/share/gtk-doc

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> 1:2.31.90-1
- Update to 2.31.90

* Fri Aug 11 2010 Matthias Clasen <mclasen@redhat.com> 1:2.31.1-2
- Add an epoch to stay ahead of F14

* Fri Aug  6 2010 Matthias Clasen <mclasen@redhat.com> 2.31.1-1
- Update to 2.31.1

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1
- Spec file cleanups

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Wed Mar 24 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-4
- Fix possible crasher when countdown reaches zero

* Fri Mar 19 2010 Matthias Clasen <mclasen@redhat.com> 2.29.92-3
- Fix text rendering issues on the effects tab

* Tue Mar 16 2010 Matthias Clasen <mclasen@redhat.com> 2.29.92-2
- Use an existing icon

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Tue Feb 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.90-2
- Fix include path, and missing requires for the pkg-config file

* Tue Feb 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.90-1
- Update to 2.29.90

* Sun Jan 17 2010 Matthias Clasen  <mclasen@redhat.com> 2.29.5-2
- Rebuild

* Tue Jan 12 2010 Matthias Clasen  <mclasen@redhat.com> 2.29.5-1
- Update to 2.29.5

* Sun Sep 27 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.28.0-2
- Update desktop file according to F-12 FedoraStudio feature

* Mon Sep 21 2009 Matthias Clasen  <mclasen@redhat.com> 2.28.0-1
- Update to 2.28.0

* Mon Sep  7 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.92-1
- Update to 2.27.92

* Mon Aug 24 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.91-1
- Update to 2.27.91

* Sat Aug 22 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.90-3
- Update sensitivity of menu items

* Fri Aug 14 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.90-2
- Fix schemas file syntax

* Tue Aug 11 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.90-1
- Update to 2.27.90

* Tue Jul 28 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.4-1
- Update to 2.27.4

* Tue Jun 16 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.3-1
- Update to 2.27.3

* Sun May 31 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.2-1
- Update to 2.27.2

* Fri May 15 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.1-1
- Update to 2.27.1

* Mon Mar 16 2009 Matthias Clasen  <mclasen@redhat.com> 2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.92-1
- Update to 2.25.92

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.90-1
- Update to 2.25.90

* Tue Jan  6 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.4-1
- Update to 2.25.4

* Wed Dec 17 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.3-1
- Update to 2.25.3

* Wed Dec  3 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.2-1
- Update to 2.25.2

* Thu Nov 21 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.1-4
- Better URL

* Thu Nov 13 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.1-3
- Update to 2.25.1

* Sun Nov  9 2008 Hans de Goede <hdegoede@redhat.com> 2.24.1-2
- Fix cams which only support 1 resolution not working (rh470698, gnome560032)

* Mon Oct 20 2008 Matthias Clasen  <mclasen@redhat.com> 2.24.1-1
- Update to 2.24.1

* Wed Oct  8 2008 Matthias Clasen  <mclasen@redhat.com> 2.24.0-2
- Save space

* Mon Sep 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.24.0-1
- Update to 2.24.0

* Tue Sep  9 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.92-3
- Update to 2.23.92
- Drop upstreamed patches

* Wed Sep  3 2008 Hans de Goede <hdegoede@redhat.com> 2.23.91-2
- Fix use with multiple v4l devices (rh 460956, gnome 546868, gnome 547144)

* Tue Sep  2 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.91-1
- Update to 2.23.91

* Fri Aug 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.90-1
- Update to 2.23.90

* Tue Aug  5 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.6-1
- Update to 2.23.6

* Tue Jul 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.5-1
- Update to 2.23.5

* Wed Jun 18 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.4-1
- Update to 2.23.4

* Tue Jun  3 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.3-1
- Update to 2.23.3

* Tue May 13 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.2-1
- Update to 2.23.2

* Fri Apr 25 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.1-1
- Update to 2.23.1

* Tue Apr 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.22.1-2
- Fix an invalid free

* Mon Apr  7 2008 Matthias Clasen  <mclasen@redhat.com> 2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 Matthias Clasen  <mclasen@redhat.com> 2.22.0-1
- Update to 2.22.0

* Tue Feb 26 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.92-1
- Update to 2.21.92

* Fri Feb 15 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.91-3
- Fix a locking problem that causes the UI to freeze

* Fri Feb  8 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.91-2
- Rebuild for gcc 4.3

* Tue Jan 29 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.91-1
- Update to 2.21.91

* Mon Jan 14 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.5-1
- Update to 2.21.5

* Mon Dec 24 2007  Matthias Clasen  <mclasen@redhat.com> 0.3.0-1
- Update to 0.3.0

* Fri Sep  7 2007  Matthias Clasen  <mclasen@redhat.com> 0.2.4-2
- package review feedback

* Thu Sep  6 2007  Matthias Clasen  <mclasen@redhat.com> 0.2.4-1
- Initial packages
