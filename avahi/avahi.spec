%{?!WITH_MONO:          %define WITH_MONO 1}
%{?!WITH_COMPAT_DNSSD:  %define WITH_COMPAT_DNSSD 1}
%{?!WITH_COMPAT_HOWL:   %define WITH_COMPAT_HOWL  1}
%ifarch sparc64 s390 %{arm}
%define WITH_MONO 0
%endif
Name:           avahi
Version:        0.6.30
Release:        2%{?dist}
Summary:        Local network service discovery
Group:          System Environment/Base
License:        LGPLv2
URL:            http://avahi.org
Requires:       dbus
Requires:       expat
Requires:       libdaemon >= 0.11
Requires:       systemd-units
Requires(post): initscripts, chkconfig, ldconfig
Requires(pre):  shadow-utils
Requires:       %{name}-libs = %{version}-%{release}
BuildRequires:  automake libtool
BuildRequires:  dbus-devel >= 0.90
BuildRequires:  dbus-glib-devel >= 0.70
BuildRequires:  dbus-python
BuildRequires:  libxml2-python
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel >= 2.99.0
#BuildRequires:  gobject-introspection-devel
BuildRequires:  qt-devel
BuildRequires:  qt4-devel
BuildRequires:  libglade2-devel
BuildRequires:  libdaemon-devel >= 0.11
BuildRequires:  glib2-devel
BuildRequires:  libcap-devel
BuildRequires:  expat-devel
BuildRequires:  python
BuildRequires:  gdbm-devel
BuildRequires:  pygtk2
BuildRequires:  intltool
BuildRequires:  perl-XML-Parser
%if %{WITH_MONO}
BuildRequires:  mono-devel >= 1.1.13
BuildRequires:  monodoc-devel
%endif
Obsoletes:      howl
Source0:        http://avahi.org/download/%{name}-%{version}.tar.gz

%description
Avahi is a system which facilitates service discovery on
a local network -- this means that you can plug your laptop or
computer into a network and instantly be able to view other people who
you can chat with, find printers to print to or find files being
shared. This kind of technology is already found in MacOS X (branded
'Rendezvous', 'Bonjour' and sometimes 'ZeroConf') and is very
convenient.

%package tools
Summary: Command line tools for mDNS browsing and publishing
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}

%description tools
Command line tools that use avahi to browse and publish mDNS services.

%package ui-tools
Summary: UI tools for mDNS browsing
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: %{name}-ui-gtk3 = %{version}-%{release}
Requires: vnc
Requires: openssh-clients
Requires: pygtk2
Requires: pygtk2-libglade
Requires: gdbm
Requires: python
Requires: dbus-python

%description ui-tools
Graphical user interface tools that use Avahi to browse for mDNS services.

%package glib
Summary: Glib libraries for avahi
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}

%description glib
Libraries for easy use of avahi from glib applications.

%package glib-devel
Summary: Libraries and header files for avahi glib development
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-glib = %{version}-%{release}
Requires: glib2-devel

%description glib-devel
The avahi-devel package contains the header files and libraries
necessary for developing programs using avahi with glib.

%package gobject
Summary: GObject wrapper library for Avahi
Group: System Environment/Base
Requires: %{name}-glib = %{version}-%{release}

%description gobject
This library contains a GObject wrapper for the Avahi API

%package gobject-devel
Summary: Libraries and header files for Avahi GObject development
Group: Development/Libraries
Requires: %{name}-gobject = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-glib-devel = %{version}-%{release}

%description gobject-devel
The avahi-gobject-devel package contains the header files and libraries
necessary for developing programs using avahi-gobject.

%package ui
Summary: Gtk user interface library for Avahi (Gtk+ 2 version)
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: gtk2

%description ui
This library contains a Gtk 2.x widget for browsing services.

%package ui-gtk3
Summary: Gtk user interface library for Avahi (Gtk+ 3 version)
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: gtk3

%description ui-gtk3
This library contains a Gtk 3.x widget for browsing services.

%package ui-devel
Summary: Libraries and header files for Avahi UI development
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-ui = %{version}-%{release}
Requires: %{name}-glib-devel = %{version}-%{release}

%description ui-devel
The avahi-ui-devel package contains the header files and libraries
necessary for developing programs using avahi-ui.

%package qt3
Summary: Qt3 libraries for avahi
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}

%description qt3
Libraries for easy use of avahi from Qt3 applications.

%package qt3-devel
Summary: Libraries and header files for avahi Qt3 development
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-qt3 = %{version}-%{release}
Requires: qt-devel

%description qt3-devel
The avahi-qt3-devel package contains the header files and libraries
necessary for developing programs using avahi with Qt3.

%package qt4
Summary: Qt4 libraries for avahi
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}

%description qt4
Libraries for easy use of avahi from Qt4 applications.

%package qt4-devel
Summary: Libraries and header files for avahi Qt4 development
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-qt4 = %{version}-%{release}
Requires: qt4-devel

%description qt4-devel
Th avahi-qt4-devel package contains the header files and libraries
necessary for developing programs using avahi with Qt4.

%if %{WITH_MONO}
%package sharp
Summary:  Mono language bindings for avahi mono development
Group:    Development/Libraries
Requires: mono-core >= 1.1.13
Requires: %{name} = %{version}-%{release}

%description sharp
The avahi-sharp package contains the files needed to develop
mono programs that use avahi.

%package ui-sharp
Summary:  Mono language bindings for avahi-ui
Group:    System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-ui = %{version}-%{release}
Requires: mono-core >= 1.1.13
Requires: gtk-sharp2
BuildRequires: gtk-sharp2-devel

%description ui-sharp
The avahi-sharp package contains the files needed to run
Mono programs that use avahi-ui.

%package ui-sharp-devel
Summary:   Mono language bindings for developing with avahi-ui
Group:     Development/Libraries
Requires:  %{name}-ui-sharp = %{version}-%{release}

%description ui-sharp-devel
The avahi-sharp-ui-devel package contains the files needed to develop
Mono programs that use avahi-ui.
%endif

%package libs
Summary:  Libraries for avahi run-time use
Group:    System Environment/Libraries

%description libs
The avahi-libs package contains the libraries needed
to run programs that use avahi.

%package devel
Summary:  Libraries and header files for avahi development
Group:    Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig

%description devel
The avahi-devel package contains the header files and libraries
necessary for developing programs using avahi.

%package   compat-howl
Summary:   Libraries for howl compatibility
Group:     Development/Libraries
Requires:  %{name} = %{version}-%{release}
Requires:  %{name}-libs = %{version}-%{release}
Obsoletes: howl-libs
Provides:  howl-libs

%description compat-howl
Libraries that are compatible with those provided by the howl package.

%package   compat-howl-devel
Summary:   Header files for development with the howl compatibility libraries
Group:     Development/Libraries
Requires:  avahi-compat-howl = %{version}-%{release}
Obsoletes: howl-devel
Provides:  howl-devel

%description compat-howl-devel
Header files for development with the howl compatibility libraries.

%package   compat-libdns_sd
Summary:   Libraries for Apple Bonjour mDNSResponder compatibility
Group:     Development/Libraries
Requires:  %{name} = %{version}-%{release}
Requires:  %{name}-libs = %{version}-%{release}

%description compat-libdns_sd
Libraries for Apple Bonjour mDNSResponder compatibility.

%package   compat-libdns_sd-devel
Summary:   Header files for the Apple Bonjour mDNSResponder compatibility libraries
Group:     Development/Libraries
Requires:  avahi-compat-libdns_sd = %{version}-%{release}

%description compat-libdns_sd-devel
Header files for development with the Apple Bonjour mDNSResponder compatibility
libraries.

%package   autoipd
Summary:   Link-local IPv4 address automatic configuration daemon (IPv4LL)
Group:     System Environment/Base
Requires(pre):        shadow-utils

%description autoipd
avahi-autoipd implements IPv4LL, "Dynamic Configuration of IPv4
Link-Local Addresses"  (IETF RFC3927), a protocol for automatic IP address
configuration from the link-local 169.254.0.0/16 range without the need for a
central server. It is primarily intended to be used in ad-hoc networks which
lack a DHCP server.

%package   dnsconfd
Summary:   Configure local unicast DNS settings based on information published in mDNS
Group:     System Environment/Base
Requires:  %{name} = %{version}-%{release}
Requires:  %{name}-libs = %{version}-%{release}

%description dnsconfd
avahi-dnsconfd connects to a running avahi-daemon and runs the script
/etc/avahi/dnsconfd.action for each unicast DNS server that is announced on the
local LAN. This is useful for configuring unicast DNS servers in a DHCP-like
fashion with mDNS.

%prep
%setup -q

%build
%configure --with-distro=fedora --disable-monodoc --with-avahi-user=avahi --with-avahi-group=avahi --with-avahi-priv-access-group=avahi --with-autoipd-user=avahi-autoipd --with-autoipd-group=avahi-autoipd --with-systemdsystemunitdir=/lib/systemd/system --enable-introspection=no \
%if %{WITH_COMPAT_DNSSD}
        --enable-compat-libdns_sd \
%endif
%if %{WITH_COMPAT_HOWL}
        --enable-compat-howl \
%endif
%if ! %{WITH_MONO}
        --disable-mono \
%endif
;

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# remove example
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/avahi/services/sftp-ssh.service

# create /var/run/avahi-daemon to ensure correct selinux policy for it:
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/avahi-daemon
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/avahi-autoipd

# remove the documentation directory - let % doc handle it:
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

# Make /etc/avahi/etc/localtime owned by avahi:
mkdir -p $RPM_BUILD_ROOT/etc/avahi/etc
touch $RPM_BUILD_ROOT/etc/avahi/etc/localtime

# fix bug 197414 - add missing symlinks for avahi-compat-howl and avahi-compat-dns-sd
%if %{WITH_COMPAT_HOWL}
ln -s avahi-compat-howl.pc  $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/howl.pc
%endif
%if %{WITH_COMPAT_DNSSD}
ln -s avahi-compat-libdns_sd.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libdns_sd.pc
ln -s avahi-compat-libdns_sd/dns_sd.h $RPM_BUILD_ROOT/%{_includedir}/
%endif
#
:;

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group avahi >/dev/null 2>&1 || groupadd \
        -r \
        -g 70 \
        avahi
getent passwd avahi >/dev/null 2>&1 || useradd \
        -r -l \
        -u 70 \
        -g avahi \
        -d %{_localstatedir}/run/avahi-daemon \
        -s /sbin/nologin \
        -c "Avahi mDNS/DNS-SD Stack" \
        avahi
:;

%post
/sbin/ldconfig || :
dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig >/dev/null 2>&1 || :
/sbin/chkconfig --add avahi-daemon >/dev/null 2>&1 || :
if [ "$1" -eq 1 ]; then
        /bin/systemctl daemon-reload >/dev/null 2>&1 || :
        if [ -s /etc/localtime ]; then
                cp -cfp /etc/localtime /etc/avahi/etc/localtime || :
        fi
fi

%triggerun -- avahi < 0.6.26-1
if /sbin/chkconfig --level 3 avahi-daemon ; then
        /bin/systemctl --no-reload enable avahi-daemon.service >/dev/null 2>&1 || :
fi

%preun
if [ "$1" -eq 0 ]; then
        /bin/systemctl --no-reload disable avahi-daemon.service >/dev/null 2>&1 || :
        /bin/systemctl stop avahi-daemon.service >/dev/null 2>&1 || :
        /sbin/chkconfig --del avahi-daemon >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
/sbin/ldconfig || :

%pre autoipd
getent group avahi-autoipd >/dev/null 2>&1 || groupadd \
        -r \
        -g 170 \
        avahi-autoipd
getent passwd avahi-autoipd >/dev/null 2>&1 || useradd \
        -r -l \
        -u 170 \
        -g avahi-autoipd \
        -d %{_localstatedir}/lib/avahi-autoipd \
        -s /sbin/nologin \
        -c "Avahi IPv4LL Stack" \
        avahi-autoipd
:;

%post dnsconfd
/sbin/chkconfig --add avahi-dnsconfd >/dev/null 2>&1 || :
if [ "$1" -eq 1 ]; then
        /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%triggerun dnsconfd -- avahi-dnsconfd < 0.6.26-1
if /sbin/chkconfig --level 3 avahi-dnsconfd ; then
        /bin/systemctl --no-reload enable avahi-dnsconfd.service >/dev/null 2>&1 || :
fi

%preun dnsconfd
if [ "$1" -eq 0 ]; then
        /bin/systemctl --no-reload disable avahi-dnsconfd.service >/dev/null 2>&1 || :
        /bin/systemctl stop avahi-dnsconfd.service >/dev/null 2>&1 || :
        /sbin/chkconfig --del avahi-dnsconfd >/dev/null 2>&1 || :
fi

%postun dnsconfd
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%post glib -p /sbin/ldconfig
%postun glib -p /sbin/ldconfig

%post compat-howl -p /sbin/ldconfig
%postun compat-howl -p /sbin/ldconfig

%post compat-libdns_sd -p /sbin/ldconfig
%postun compat-libdns_sd -p /sbin/ldconfig

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post qt3 -p /sbin/ldconfig
%postun qt3 -p /sbin/ldconfig

%post qt4 -p /sbin/ldconfig
%postun qt4 -p /sbin/ldconfig

%post ui -p /sbin/ldconfig
%postun ui -p /sbin/ldconfig

%post ui-gtk3 -p /sbin/ldconfig
%postun ui-gtk3 -p /sbin/ldconfig

%post gobject -p /sbin/ldconfig
%postun gobject -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(0644,root,root,0755)
%doc docs/* avahi-daemon/example.service avahi-daemon/sftp-ssh.service
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/avahi-daemon
%dir %{_sysconfdir}/avahi
%dir %{_sysconfdir}/avahi/etc
%ghost %{_sysconfdir}/avahi/etc/localtime
%config(noreplace) %{_sysconfdir}/avahi/hosts
%dir %{_sysconfdir}/avahi/services
%ghost %attr(0755,avahi,avahi) %dir %{_localstatedir}/run/avahi-daemon
%config(noreplace) %{_sysconfdir}/avahi/avahi-daemon.conf
%config(noreplace) %{_sysconfdir}/avahi/services/ssh.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/avahi-dbus.conf
%attr(0755,root,root) %{_sbindir}/avahi-daemon
%dir %{_datadir}/avahi
%{_datadir}/avahi/*.dtd
%{_datadir}/avahi/service-types
%{_libdir}/avahi
%{_datadir}/dbus-1/interfaces/*.xml
%{_mandir}/man5/*
%{_mandir}/man8/avahi-daemon.*
/lib/systemd/system/avahi-daemon.service
/lib/systemd/system/avahi-daemon.socket
%{_datadir}/dbus-1/system-services/org.freedesktop.Avahi.service
%attr(0755,root,root) %{_libdir}/libavahi-core.so.*

%files autoipd
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_sbindir}/avahi-autoipd
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/avahi/avahi-autoipd.action
%{_mandir}/man8/avahi-autoipd.*

%files dnsconfd
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/avahi-dnsconfd
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/avahi/avahi-dnsconfd.action
%attr(0755,root,root) %{_sbindir}/avahi-dnsconfd
%{_mandir}/man8/avahi-dnsconfd.*
/lib/systemd/system/avahi-dnsconfd.service

%files tools
%defattr(0644, root, root, 0755)
%attr(0755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%exclude %{_bindir}/b*
%exclude %{_bindir}/avahi-discover*
%exclude %{_bindir}/avahi-bookmarks
%exclude %{_mandir}/man1/b*
%exclude %{_mandir}/man1/avahi-discover*
%exclude %{_mandir}/man1/avahi-bookmarks*

%files ui-tools
%defattr(0644, root, root, 0755)
%attr(0755,root,root) %{_bindir}/b*
%attr(0755,root,root) %{_bindir}/avahi-discover
# avahi-bookmarks is not really a UI tool, but I won't create a seperate package for it...
%attr(0755,root,root) %{_bindir}/avahi-bookmarks
%{_mandir}/man1/b*
%{_mandir}/man1/avahi-discover*
%{_mandir}/man1/avahi-bookmarks*
%{_datadir}/applications/b*.desktop
%{_datadir}/applications/avahi-discover.desktop
# These are .py files only, so they don't go in lib64
%{_prefix}/lib/python?.?/site-packages/*
%{_datadir}/avahi/interfaces/

%files devel
%defattr(0644, root, root, 0755)
%attr(755,root,root) %{_libdir}/libavahi-common.so
%attr(755,root,root) %{_libdir}/libavahi-core.so
%attr(755,root,root) %{_libdir}/libavahi-client.so
%{_includedir}/avahi-client
%{_includedir}/avahi-common
%{_includedir}/avahi-core
%{_libdir}/pkgconfig/avahi-core.pc
%{_libdir}/pkgconfig/avahi-client.pc

%files libs
%defattr(0644, root, root, 0755)
%attr(0755,root,root) %{_libdir}/libavahi-common.so.*
%attr(0755,root,root) %{_libdir}/libavahi-client.so.*

%files glib
%defattr(0755, root, root, 0755)
%{_libdir}/libavahi-glib.so.*

%files glib-devel
%defattr(0644, root, root, 0755)
%attr(755,root,root) %{_libdir}/libavahi-glib.so
%{_includedir}/avahi-glib
%{_libdir}/pkgconfig/avahi-glib.pc

%files gobject
%defattr(0644, root, root, 0755)
%attr(755,root,root) %{_libdir}/libavahi-gobject.so.*
#%{_libdir}/girepository-1.0/Avahi-0.6.typelib
#%{_libdir}/girepository-1.0/AvahiCore-0.6.typelib

%files gobject-devel
%defattr(0644, root, root, 0755)
%attr(755,root,root) %{_libdir}/libavahi-gobject.so
%{_includedir}/avahi-gobject
%{_libdir}/pkgconfig/avahi-gobject.pc
#%{_datadir}/gir-1.0/Avahi-0.6.gir
#%{_datadir}/gir-1.0/AvahiCore-0.6.gir

%files ui
%defattr(0755, root, root, 0755)
%{_libdir}/libavahi-ui.so.*

%files ui-gtk3
%defattr(0755, root, root, 0755)
%{_libdir}/libavahi-ui-gtk3.so.*

%files ui-devel
%defattr(0644, root, root, 0755)
%attr(755,root,root) %{_libdir}/libavahi-ui.so
%attr(755,root,root) %{_libdir}/libavahi-ui-gtk3.so
%{_includedir}/avahi-ui
%{_libdir}/pkgconfig/avahi-ui.pc
%{_libdir}/pkgconfig/avahi-ui-gtk3.pc

%files qt3
%defattr(0644, root, root, 0755)
%attr(755,root,root) %{_libdir}/libavahi-qt3.so.*

%files qt3-devel
%defattr(0644, root, root, 0755)
%attr(755,root,root) %{_libdir}/libavahi-qt3.so
%{_includedir}/avahi-qt3/
%{_libdir}/pkgconfig/avahi-qt3.pc

%files qt4
%defattr(0644, root, root, 0755)
%attr(755,root,root) %{_libdir}/libavahi-qt4.so.*

%files qt4-devel
%defattr(0644, root, root, 0755)
%attr(755,root,root) %{_libdir}/libavahi-qt4.so
%{_includedir}/avahi-qt4/
%{_libdir}/pkgconfig/avahi-qt4.pc

%if %{WITH_MONO}
%files sharp
%defattr(0644, root, root, 0755)
%{_libdir}/mono/avahi-sharp
%{_libdir}/mono/gac/avahi-sharp
%{_libdir}/pkgconfig/avahi-sharp.pc

%files ui-sharp
%defattr(0644, root, root, 0755)
%{_libdir}/mono/avahi-ui-sharp
%{_libdir}/mono/gac/avahi-ui-sharp

%files ui-sharp-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/avahi-ui-sharp.pc
%endif

%if %{WITH_COMPAT_HOWL}
%files compat-howl
%defattr(0755, root, root, 0755)
%{_libdir}/libhowl.so.*

%files compat-howl-devel
%defattr(0644, root, root, 0755)
%attr(755,root,root) %{_libdir}/libhowl.so
%{_includedir}/avahi-compat-howl
%{_libdir}/pkgconfig/avahi-compat-howl.pc
%{_libdir}/pkgconfig/howl.pc
%endif

%if %{WITH_COMPAT_DNSSD}
%files compat-libdns_sd
%defattr(0755, root, root, 0755)
%{_libdir}/libdns_sd.so.*

%files compat-libdns_sd-devel
%defattr(0644, root, root, 0755)
%attr(755,root,root) %{_libdir}/libdns_sd.so
%{_includedir}/avahi-compat-libdns_sd
%{_includedir}/dns_sd.h
%{_libdir}/pkgconfig/avahi-compat-libdns_sd.pc
%{_libdir}/pkgconfig/libdns_sd.pc
%endif

%changelog
