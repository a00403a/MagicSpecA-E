Summary:   Color daemon
Name:      colord
Version:   0.1.18
Release:   2%{?dist}
License:   GPLv2+ and LGPLv2+
URL:       http://www.freedesktop.org/software/colord/
Source0:   http://www.freedesktop.org/software/colord/releases/%{name}-%{version}.tar.xz
Patch0:    0001-Do-not-enable-PrivateNetwork-yes-as-it-breaks-hotplu.patch
Patch1:	   colord-0.1.18-udevdir.patch

BuildRequires: dbus-devel
BuildRequires: docbook-utils
BuildRequires: gettext
BuildRequires: glib2-devel
BuildRequires: intltool
BuildRequires: lcms2-devel >= 2.2
BuildRequires: libgudev1-devel
BuildRequires: polkit-devel >= 0.103
BuildRequires: sane-backends-devel
BuildRequires: sqlite-devel
BuildRequires: gobject-introspection-devel
BuildRequires: vala-tools
BuildRequires: libgusb-devel

Requires: shared-color-profiles
Requires: color-filesystem
Requires: systemd-units
Requires(pre): shadow-utils

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
%patch0 -p1 -b .fix-device-hotplug
%patch1 -p1

%build
%configure \
        --with-daemon-user=colord \
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

magic_rpm_clean.sh
%find_lang %{name} || touch %{name}.lang

%pre
getent group colord >/dev/null || groupadd -r colord
getent passwd colord >/dev/null || \
    useradd -r -g colord -d /var/lib/colord -s /sbin/nologin \
    -c "User for colord" colord
exit 0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README AUTHORS NEWS COPYING
%{_libexecdir}/colord
%attr(755,colord,colord) %dir %{_localstatedir}/lib/colord
%attr(755,colord,colord) %dir %{_localstatedir}/lib/colord/icc
%{_bindir}/*
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ColorManager.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorManager*.xml
%{_datadir}/polkit-1/actions/org.freedesktop.color.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.ColorManager.service
%{_datadir}/man/man1/*.1.gz
%{_libdir}/libcolord.so.*
%config %{_sysconfdir}/colord.conf
%{_libdir}/udev/rules.d/*.rules
%dir %{_datadir}/color/icc/colord
%{_datadir}/color/icc/colord/*.ic?
%{_libdir}/colord-sensors
%{_libdir}/girepository-1.0/*.typelib
%ghost %{_localstatedir}/lib/colord/*.db

# TODO: split this out into a subpackage?
/usr/lib/systemd/system/colord.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.colord.sane.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.colord-sane.service
/usr/lib/systemd/system/colord-sane.service
%{_libexecdir}/colord-sane
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.colord-sane.conf

%files devel
%defattr(-,root,root,-)
%{_includedir}/colord-1
%{_libdir}/libcolord.so
%{_libdir}/pkgconfig/colord.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/*.vapi

%changelog
* Thu Mar 29 2012 Richard Hughes <richard@hughsie.com> 0.1.18-2
- Disable PrivateNetwork=1 as it breaks sensor hotplug.

* Thu Mar 15 2012 Richard Hughes <richard@hughsie.com> 0.1.18-1
- New upstream version
- Add a Manager.CreateProfileWithFd() method for QtDBus
- Split out the SANE support into it's own process
- Fix a small leak when creating devices and profiles in clients
- Fix cd-fix-profile to add and remove metadata entries
- Install per-machine profiles in /var/lib/colord/icc

* Wed Feb 22 2012 Richard Hughes <richard@hughsie.com> 0.1.17-1
- New upstream version
- Add an LED sample type
- Add PrivateNetwork and PrivateTmp to the systemd service file
- Fix InstallSystemWide() when running as the colord user

* Fri Jan 20 2012 Matthias Clasen <mclasen@redha.com> - 0.1.16-4
- Fix some obvious bugs

* Tue Jan 17 2012 Richard Hughes <richard@hughsie.com> 0.1.16-1
- New upstream version
- Now runs as a colord user rather than as root.
- Support more ICC metadata keys
- Install a systemd service file
- Support 2nd generation Huey hardware

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Richard Hughes <richard@hughsie.com> 0.1.15-1
- New upstream version
- This release fixes an important security bug: CVE-2011-4349.
- Do not crash the daemon if adding the device to the db failed
- Fix a memory leak when getting properties from a device

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
