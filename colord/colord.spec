Summary:   Color daemon
Name:      colord
Version:   0.1.14
Release:   1%{?dist}
License:   GPLv2+ and LGPLv2+
URL:       http://www.freedesktop.org/software/colord/
Source0:   http://www.freedesktop.org/software/colord/releases/%{name}-%{version}.tar.xz

BuildRequires: dbus-devel
BuildRequires: docbook-utils
BuildRequires: gettext
BuildRequires: glib2-devel
BuildRequires: intltool
BuildRequires: lcms2-devel
BuildRequires: libgudev1-devel
BuildRequires: libusb1-devel
BuildRequires: polkit-devel
BuildRequires: sane-backends-devel
BuildRequires: sqlite-devel
BuildRequires: gobject-introspection-devel
BuildRequires: vala-tools
Requires: shared-color-profiles

%description
colord is a low level system activated daemon that maps color devices
to color profiles in the system context.

%package devel
Summary: Development package for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
Files for development with %{name}.

%prep
%setup -q

%build
%configure \
        --disable-static \
        --disable-rpath \
        --disable-examples \
        --disable-dependency-tracking

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove static libs and libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# databases
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/colord/mapping.db
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/colord/storage.db

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README AUTHORS NEWS COPYING
%{_libexecdir}/colord
%dir %{_localstatedir}/lib/colord
%{_bindir}/*
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ColorManager.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorManager*.xml
%{_datadir}/polkit-1/actions/org.freedesktop.color.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.ColorManager.service
%{_datadir}/man/man1/*.1.gz
%{_libdir}/libcolord.so.*
%config %{_sysconfdir}/colord.conf
/lib/udev/rules.d/*.rules
%dir %{_datadir}/color/icc/colord
%{_datadir}/color/icc/colord/*.ic?
%{_libdir}/colord-sensors
%{_libdir}/girepository-1.0/*.typelib
%ghost %{_localstatedir}/lib/colord/*.db

%files devel
%defattr(-,root,root,-)
%{_includedir}/colord-1
%{_libdir}/libcolord.so
%{_libdir}/pkgconfig/colord.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/*.vapi

%changelog
* Tue Nov 01 2011 Richard Hughes <richard@hughsie.com> 0.1.14-1
- New upstream version
- Remove upstreamed patches

* Mon Oct 03 2011 Richard Hughes <richard@hughsie.com> 0.1.13-1
- New upstream version
- Ensure uid 0 can always create devices and profiles
- Reduce the CPU load of clients when assigning profiles

* Tue Aug 30 2011 Richard Hughes <richard@hughsie.com> 0.1.12-1
- New upstream version

* Mon Aug 01 2011 Richard Hughes <richard@hughsie.com> 0.1.11-2
- Remove the sedding libtool's internals as it breaks
  generation of the GObject Introspection data.

* Mon Aug 01 2011 Richard Hughes <richard@hughsie.com> 0.1.11-1
- New upstream version

* Wed Jul 06 2011 Richard Hughes <richard@hughsie.com> 0.1.10-1
- New upstream version

* Mon Jun 13 2011 Richard Hughes <richard@hughsie.com> 0.1.9-1
- New upstream version

* Fri Jun 02 2011 Richard Hughes <richard@hughsie.com> 0.1.8-1
- New upstream version
- Add a webcam device kind
- Add a timestamp when making profiles default
- Add support for reading and writing ICC profile metadata
- Allow the client to pass file descriptors out of band to CreateProfile
- Prettify the device vendor and model names
- Split out the sensors into runtime-loadable shared objects
- Provide some GIO async variants for the methods in CdClient
- Ensure GPhoto2 devices get added to the device list

* Fri May 06 2011 Richard Hughes <richard@hughsie.com> 0.1.7-1
- New upstream version.
- Create /var/lib/colord at buildtime not runtime for SELinux
- Ensure profiles with embedded profile checksums are parsed correctly
- Move the colorimeter rules to be run before 70-acl.rules
- Stop watching the client when the sensor is finalized
- Ensure the source is destroyed when we unref CdUsb to prevent a crash
- Only enable the volume mount tracking when searching volumes

* Tue Apr 26 2011 Richard Hughes <rhughes@redhat.com> 0.1.6-2
- Own /var/lib/colord and /var/lib/colord/*.db

* Sun Apr 24 2011 Richard Hughes <richard@hughsie.com> 0.1.6-1
- New upstream version.

* Thu Mar 31 2011 Richard Hughes <richard@hughsie.com> 0.1.5-1
- New upstream version.

* Wed Mar 09 2011 Richard Hughes <richard@hughsie.com> 0.1.4-1
- New upstream version.

* Mon Feb 28 2011 Richard Hughes <richard@hughsie.com> 0.1.3-1
- New upstream version.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Richard Hughes <richard@hughsie.com> 0.1.1-2
- Rebuild in the vain hope koji isn't broken today.

* Wed Jan 26 2011 Richard Hughes <richard@hughsie.com> 0.1.1-1
- New upstream version.

* Thu Jan 13 2011 Richard Hughes <richard@hughsie.com> 0.1.0-1
- Initial version for Fedora package review.
