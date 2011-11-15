# SystemTap support is enabled by default
%{!?sdt:%global sdt 1}

# vendor string (e.g., Fedora, EL)
%global vvendor Fedora

#http://lists.fedoraproject.org/pipermail/devel/2011-August/155358.html
%global _hardened_build 1

# Where dhcp configuration files are stored
%global dhcpconfdir %{_sysconfdir}/dhcp

# Patch version 
#%global patchver P1
# Pre-Release version
#%global prever rc1

#%global VERSION %{version}-%{patchver}
#%global VERSION %{version}%{prever}
%global VERSION %{version}

Summary:  Dynamic host configuration protocol software
Name:     dhcp
Version:  4.2.3
Release:  5%{?dist}
# NEVER CHANGE THE EPOCH on this package.  The previous maintainer (prior to
# dcantrell maintaining the package) made incorrect use of the epoch and
# that's why it is at 12 now.  It should have never been used, but it was.
# So we are stuck with it.
Epoch:    12
License:  ISC
Group:    System Environment/Daemons
URL:      http://isc.org/products/DHCP/
Source0:  ftp://ftp.isc.org/isc/dhcp/dhcp-%{VERSION}.tar.gz
Source1:  dhcpd.init
Source2:  dhcpd6.init
Source3:  dhcrelay.init
Source4:  dhclient-script
Source5:  README.dhclient.d
Source6:  11-dhclient
Source7:  12-dhcpd
Source8:  56dhclient
Source9:   dhcpd.service
Source10:  dhcpd6.service
Source11:  dhcrelay.service

Patch0:   dhcp-4.2.0-errwarn-message.patch
Patch1:   dhcp-4.2.3-options.patch
Patch2:   dhcp-4.2.0-release-by-ifup.patch
Patch3:   dhcp-4.2.0-dhclient-decline-backoff.patch
Patch4:   dhcp-4.2.0-unicast-bootp.patch
Patch6:   dhcp-4.2.2-dhclient-usage.patch
Patch7:   dhcp-4.2.0-default-requested-options.patch
Patch8:   dhcp-4.2.2-xen-checksum.patch
Patch10:  dhcp-4.2.1-manpages.patch
Patch11:  dhcp-4.2.0-paths.patch
Patch12:  dhcp-4.2.2-CLOEXEC.patch
Patch13:  dhcp-4.2.0-inherit-leases.patch
Patch14:  dhcp-4.2.0-garbage-chars.patch
Patch15:  dhcp-4.2.0-missing-ipv6-not-fatal.patch
Patch17:  dhcp-4.2.0-add_timeout_when_NULL.patch
Patch18:  dhcp-4.2.1-64_bit_lease_parse.patch
Patch19:  dhcp-4.2.2-capability.patch
Patch20:  dhcp-4.2.0-logpid.patch
Patch21:  dhcp-4.2.0-UseMulticast.patch
Patch22:  dhcp-4.2.1-sendDecline.patch
Patch23:  dhcp-4.2.1-retransmission.patch
Patch25:  dhcp-4.2.3-rfc3442-classless-static-routes.patch
Patch27:  dhcp-4.2.0-honor-expired.patch
Patch28:  dhcp-4.2.0-noprefixavail.patch
Patch29:  dhcp-4.2.2-remove-bind.patch
Patch30:  dhcp-4.2.2-sharedlib.patch
Patch31:  dhcp-4.2.0-PPP.patch
Patch32:  dhcp-4.2.3-paranoia.patch
Patch33:  dhcp-4.2.2-lpf-ib.patch
Patch34:  dhcp-4.2.2-improved-xid.patch
Patch35:  dhcp-4.2.2-gpxe-cid.patch
Patch36:  dhcp-4.2.2-systemtap.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: groff
BuildRequires: libtool
BuildRequires: openldap-devel
BuildRequires: libcap-ng-devel
BuildRequires: bind-lite-devel
%if %sdt
BuildRequires: systemtap-sdt-devel
%global tapsetdir    /usr/share/systemtap/tapset
%endif

Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(post): coreutils
Requires(post): systemd-units
# This is actually needed for the %%triggerun script but Requires(triggerun) is not valid.
Requires(post): systemd-sysv
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(preun): systemd-units
Requires(postun): initscripts
Requires(postun): systemd-units

Obsoletes: dhcpv6 <= 2.0.0alpha4-1
Provides:  dhcpv6  = 2.0.0alpha4-2

# In _docdir we ship some perl scripts and module from contrib subdirectory.
# Because nothing under _docdir is allowed to "require" anything,
# prevent _docdir from being scanned. (#674058)
%filter_requires_in %{_docdir}
%filter_setup

%description
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.

To use DHCP on your network, install a DHCP service (or relay agent),
and on clients run a DHCP client daemon.  The dhcp package provides
the ISC DHCP service and relay agent.

%package -n dhclient
Summary: Provides the ISC DHCP client daemon and dhclient-script
Group: System Environment/Base
Requires: initscripts
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires(post): coreutils
Requires(post): grep
Obsoletes: dhcpcd <= 1.3.22pl1-7
Provides:  dhcpcd  = 1.3.22pl1-8
Obsoletes: libdhcp4client <= 12:4.0.0-34
Provides:  libdhcp4client  = 12:4.0.0-35
Obsoletes: libdhcp <= 1.99.8-1
Provides:  libdhcp  = 1.99.8-2
Obsoletes: dhcpv6-client <= 2.0.0alpha4-1
Provides:  dhcpv6-client  = 2.0.0alpha4-2

%description -n dhclient
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.

To use DHCP on your network, install a DHCP service (or relay agent),
and on clients run a DHCP client daemon.  The dhclient package
provides the ISC DHCP client daemon.

%package common
Summary: Common files used by ISC dhcp client and server
Group: System Environment/Base
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description common
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.

This package provides common files used by dhcp and dhclient package.

%package libs
Summary: Shared libraries used by ISC dhcp client and server
Group: System Environment/Base

%description libs
This package contains shared libraries used by ISC dhcp client and server


%package devel
Summary: Development headers and libraries for interfacing to the DHCP server
Group: Development/Libraries
Obsoletes: libdhcp4client-devel <= 12:4.0.0-34
Provides:  libdhcp4client-devel  = 12:4.0.0-35
Obsoletes: libdhcp-devel <= 1.99.8-1
Provides:  libdhcp-devel  = 1.99.8-2
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
Header files and API documentation for using the ISC DHCP libraries.  The
libdhcpctl and libomapi static libraries are also included in this package.

%package sysvinit
Summary: Legacy SysV initscripts for DHCP server and relay agent
Group: System Environment/Base

%description sysvinit
Legacy SysV initscripts for init mechanisms such as upstart
which do not support the systemd unit file format.

%prep
%setup -q -n dhcp-%{VERSION}

# Remove bundled BIND source
rm bind/bind.tar.gz

# Fire away bundled BIND source.
%patch29 -p1 -b .remove-bind %{?_rawbuild}

# Replace the standard ISC warning message about requesting help with an
# explanation that this is a patched build of ISC DHCP and bugs should be
# reported through bugzilla.redhat.com
%patch0 -p1 -b .errwarn

# Add more dhclient options (-I, -B, -H, -F, -timeout, -V, and -R)
%patch1 -p1 -b .options

# Handle releasing interfaces requested by /sbin/ifup
# pid file is assumed to be /var/run/dhclient-$interface.pid
%patch2 -p1 -b .ifup

# If we receive a DHCP offer in dhclient and it's DECLINEd in dhclient-script,
# backoff for an amount of time before trying again
%patch3 -p1 -b .backoff

# Support unicast BOOTP for IBM pSeries systems (and maybe others)
# (Submitted to dhcp-bugs@isc.org - [ISC-Bugs #19146])
%patch4 -p1 -b .unicast

# Update the usage screen for dhclient(8) indicating new options
# Use printf() rather than log_info() to display the information
# Also, return EXIT_FAILURE when the usage() screen is displayed (stop parsing)
%patch6 -p1 -b .usage

# Add NIS domain, NIS servers, NTP servers, interface-mtu and domain-search
# to the list of default requested DHCP options
%patch7 -p1 -b .requested

# Handle Xen partial UDP checksums
%patch8 -p1 -b .xen

# Patch man page contents
%patch10 -p1 -b .man

# Change paths to conform to our standards
%patch11 -p1 -b .paths

# Make sure all open file descriptors are closed-on-exec for SELinux (#446632)
# (Submitted to dhcp-bugs@isc.org - [ISC-Bugs #19148])
%patch12 -p1 -b .cloexec

# If we have an active lease, do not down the interface (#453982)
%patch13 -p1 -b .inherit

# Fix 'garbage in format string' error (#450042)
%patch14 -p1 -b .garbage

# If the ipv6 kernel module is missing, do not segfault
# (Submitted to dhcp-bugs@isc.org - [ISC-Bugs #19367])
%patch15 -p1 -b .noipv6

# Handle cases in add_timeout() where the function is called with a NULL
# value for the 'when' parameter
# (Submitted to dhcp-bugs@isc.org - [ISC-Bugs #19867])
%patch17 -p1 -b .dracut

# Ensure 64-bit platforms parse lease file dates & times correctly (#448615, #628258)
# (Partly submitted to dhcp-bugs@isc.org - [ISC-Bugs #22033])
%patch18 -p1 -b .64-bit_lease_parse

# Drop unnecessary capabilities in
# dhclient (#517649, #546765), dhcpd/dhcrelay (#699713)
%patch19 -p1 -b .capability

# dhclient logs its pid to make troubleshooting NM managed systems
# with multiple dhclients running easier (#546792)
%patch20 -p1 -b .logpid

# Discard unicast Request/Renew/Release/Decline message
# (unless we set unicast option) and respond with Reply
# with UseMulticast Status Code option (#573090)
# (Submitted to dhcp-bugs@isc.org - [ISC-Bugs #21235])
%patch21 -p1 -b .UseMulticast

# If any of the bound addresses are found to be in use on the link,
# the dhcpv6 client sends a Decline message to the server
# as described in section 18.1.7 of RFC-3315 (#559147)
# (Submitted to dhcp-bugs@isc.org - [ISC-Bugs #21237])
%patch22 -p1 -b .sendDecline

# In client initiated message exchanges stop retransmission
# upon reaching the MRD rather than at some point after it (#559153)
# (Submitted to dhcp-bugs@isc.org - [ISC-Bugs #21238])
%patch23 -p1 -b .retransmission

# RFC 3442 - Classless Static Route Option for DHCPv4 (#516325)
%patch25 -p1 -b .rfc3442

# check whether there is any unexpired address in previous lease
# prior to confirming (INIT-REBOOT) the lease (#585418)
# (Submitted to dhcp-suggest@isc.org - [ISC-Bugs #22675])
%patch27 -p1 -b .honor-expired

# 1) When server has empty pool of addresses/prefixes it must send Advertise with
#    NoAddrsAvail/NoPrefixAvail status in response to clients Solicit.
#    Without this patch server having empty pool of addresses/prefixes was ignoring
#    client's' Solicit when client was also sending address in IA_NA or prefix in IA_PD as a preference.
# 2) When client sends prefix in IA_PD as a preference and server doesn't have
#    this prefix in any pool the server should offer other free prefix.
#    Without this patch server ignored client's Solicit in which the client was sending
#    prefix in IA_PD (as a preference) and this prefix was not in any of server's pools.
#   (Submitted to dhcp-bugs@isc.org - [ISC-Bugs #22676])
%patch28 -p1 -b .noprefixavail

#Build dhcp's libraries as shared libs instead of static libs.
%patch30 -p1 -b .sharedlib

# DHCPv6 over PPP support (#626514)
%patch31 -p1 -b .PPP

# Write PID file BEFORE changing of the effective user/group ID.
# (Submitted to dhcp-bugs@isc.org - [ISC-Bugs #25806])
# Write lease file AFTER changing of the effective user/group ID.
%patch32 -p1 -b .paranoia

# IPoIB support (#660681)
# (Submitted to dhcp-bugs@isc.org - [ISC-Bugs #24249])
%patch33 -p1 -b .lpf-ib
%patch34 -p1 -b .improved-xid
%patch35 -p1 -b .gpxe-cid

# http://sourceware.org/systemtap/wiki/SystemTap
%patch36 -p1 -b .systemtap

# Copy in the Fedora/RHEL dhclient script
%{__install} -p -m 0755 %{SOURCE4} client/scripts/linux
%{__install} -p -m 0644 %{SOURCE5} .

pushd contrib
%{__chmod} -x 3.0b1-lease-convert dhclient-tz-exithook.sh ldap/dhcpd-conf-to-ldap
%{__chmod} -x sethostname.sh solaris.init
%{__rm} -f dhcp.spec

# We want UNIX-style line endings
%{__sed} -i -e 's/\r//' ms2isc/readme.txt
%{__sed} -i -e 's/\r//' ms2isc/Registry.pm
%{__sed} -i -e 's/\r//' ms2isc/ms2isc.pl
popd

# Replace @PRODUCTNAME@
%{__sed} -i -e 's|@PRODUCTNAME@|%{vvendor}|g' common/dhcp-options.5
%{__sed} -i -e 's|@PRODUCTNAME@|%{vvendor}|g' configure.ac

# Update paths in all man pages
for page in client/dhclient.conf.5 client/dhclient.leases.5 \
            client/dhclient-script.8 client/dhclient.8 ; do
    %{__sed} -i -e 's|CLIENTBINDIR|/sbin|g' \
                -e 's|RUNDIR|%{_localstatedir}/run|g' \
                -e 's|DBDIR|%{_localstatedir}/lib/dhclient|g' \
                -e 's|ETCDIR|%{dhcpconfdir}|g' $page
done

for page in server/dhcpd.conf.5 server/dhcpd.leases.5 server/dhcpd.8 ; do
    %{__sed} -i -e 's|CLIENTBINDIR|/sbin|g' \
                -e 's|RUNDIR|%{_localstatedir}/run|g' \
                -e 's|DBDIR|%{_localstatedir}/lib/dhcpd|g' \
                -e 's|ETCDIR|%{dhcpconfdir}|g' $page
done

%build
#libtoolize --copy --force
autoreconf --verbose --force --install

CFLAGS="%{optflags} -fno-strict-aliasing -D_GNU_SOURCE" \
%configure \
    --with-srv-lease-file=%{_localstatedir}/lib/dhcpd/dhcpd.leases \
    --with-srv6-lease-file=%{_localstatedir}/lib/dhcpd/dhcpd6.leases \
    --with-cli-lease-file=%{_localstatedir}/lib/dhclient/dhclient.leases \
    --with-cli6-lease-file=%{_localstatedir}/lib/dhclient/dhclient6.leases \
    --with-srv-pid-file=%{_localstatedir}/run/dhcpd.pid \
    --with-srv6-pid-file=%{_localstatedir}/run/dhcpd6.pid \
    --with-cli-pid-file=%{_localstatedir}/run/dhclient.pid \
    --with-cli6-pid-file=%{_localstatedir}/run/dhclient6.pid \
    --with-relay-pid-file=%{_localstatedir}/run/dhcrelay.pid \
    --with-ldap \
    --with-ldapcrypto \
    --with-libbind=%{_includedir} --with-libbind-libs=%{_libdir} \
    --disable-static \
%if %sdt
    --enable-systemtap \
    --with-tapset-install-dir=%{tapsetdir} \
%endif
    --enable-paranoia --enable-early-chroot
%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=%{buildroot}

# Remove files we don't want
%{__rm} -f %{buildroot}%{_sysconfdir}/dhclient.conf
%{__rm} -f %{buildroot}%{_sysconfdir}/dhcpd.conf

# Install correct dhclient-script
%{__mkdir} -p %{buildroot}/sbin
%{__mv} %{buildroot}%{_sbindir}/dhclient %{buildroot}/sbin/dhclient
%{__install} -p -m 0755 client/scripts/linux %{buildroot}/sbin/dhclient-script

# Install legacy SysV initscripts
%{__mkdir} -p %{buildroot}%{_initddir}
%{__install} -p -m 0755 %{SOURCE1} %{buildroot}%{_initddir}/dhcpd
%{__install} -p -m 0755 %{SOURCE2} %{buildroot}%{_initddir}/dhcpd6
%{__install} -p -m 0755 %{SOURCE3} %{buildroot}%{_initddir}/dhcrelay

# Install systemd unit files
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE9} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE10} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE11} %{buildroot}%{_unitdir}

# Start empty lease databases
%{__mkdir} -p %{buildroot}%{_localstatedir}/lib/dhcpd/
touch %{buildroot}%{_localstatedir}/lib/dhcpd/dhcpd.leases
touch %{buildroot}%{_localstatedir}/lib/dhcpd/dhcpd6.leases
%{__mkdir} -p %{buildroot}%{_localstatedir}/lib/dhclient/

# Create default sysconfig files for dhcpd and dhcrelay
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig

%{__cat} << EOF > %{buildroot}%{_sysconfdir}/sysconfig/dhcrelay
# Command line options here
#Example: DHCRELAYARGS="-4 -i eth0 192.168.0.1"
#Example: DHCRELAYARGS="-6 -l eth1 -u eth0"
DHCRELAYARGS=""
# Note: We don't use INTERFACES and DHCPSERVERS anymore (they were DHCPv4 only)
EOF

%{__cat} <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/dhcpd
# Command line options here
DHCPDARGS=""
EOF

%{__cat} <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/dhcpd6
# Command line options here
DHCPDARGS="-cf /etc/dhcp/dhcpd6.conf"
EOF

# Copy sample conf files into position (called by doc macro)
%{__cp} -p client/dhclient.conf dhclient.conf.sample
%{__cp} -p server/dhcpd.conf dhcpd.conf.sample
%{__cp} -p doc/examples/dhclient-dhcpv6.conf dhclient6.conf.sample
%{__cp} -p doc/examples/dhcpd-dhcpv6.conf dhcpd6.conf.sample

# Install default (empty) dhcpd.conf:
%{__mkdir} -p %{buildroot}%{dhcpconfdir}
%{__cat} << EOF > %{buildroot}%{dhcpconfdir}/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp*/dhcpd.conf.sample
#   see dhcpd.conf(5) man page
#
EOF

# Install default (empty) dhcpd6.conf:
%{__cat} << EOF > %{buildroot}%{dhcpconfdir}/dhcpd6.conf
#
# DHCPv6 Server Configuration file.
#   see /usr/share/doc/dhcp*/dhcpd6.conf.sample
#   see dhcpd.conf(5) man page
#
EOF

# Install dhcp.schema for LDAP configuration
%{__mkdir} -p %{buildroot}%{_sysconfdir}/openldap/schema
%{__install} -p -m 0644 -D contrib/ldap/dhcp.schema \
    %{buildroot}%{_sysconfdir}/openldap/schema

# Install empty directory for dhclient.d scripts
%{__mkdir} -p %{buildroot}%{dhcpconfdir}/dhclient.d

# Install NetworkManager dispatcher script
%{__mkdir} -p %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d
%{__install} -p -m 0755 %{SOURCE6} %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d
%{__install} -p -m 0755 %{SOURCE7} %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d

# Install pm-utils script to handle suspend/resume and dhclient leases
%{__mkdir} -p %{buildroot}%{_libdir}/pm-utils/sleep.d
%{__install} -p -m 0755 %{SOURCE8} %{buildroot}%{_libdir}/pm-utils/sleep.d

# Don't package libtool *.la files
find ${RPM_BUILD_ROOT}/%{_libdir} -name '*.la' -exec '/bin/rm' '-f' '{}' ';';

%pre
# /usr/share/doc/setup/uidgid
%global gid_uid 177
getent group dhcpd >/dev/null || groupadd --force --gid %{gid_uid} --system dhcpd
if ! getent passwd dhcpd >/dev/null ; then
    if ! getent passwd %{gid_uid} >/dev/null ; then
      useradd --system --uid %{gid_uid} --gid dhcpd --home / --shell /sbin/nologin --comment "DHCP server" dhcpd
    else
      useradd --system --gid dhcpd --home / --shell /sbin/nologin --comment "DHCP server" dhcpd
    fi
fi
exit 0

%post
sampleconf="#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp*/dhcpd.conf.sample
#   see 'man 5 dhcpd.conf'
#"

contents="$(/bin/cat %{dhcpconfdir}/dhcpd.conf)"
prevconf="%{_sysconfdir}/dhcpd.conf"

if [ ! -z "${prevconf}" ]; then
    if [ ! -f %{dhcpconfdir}/dhcpd.conf -o "${sampleconf}" = "${contents}" ]; then
        /bin/cp -a ${prevconf} %{dhcpconfdir}/dhcpd.conf >/dev/null 2>&1
        /bin/mv ${prevconf} ${prevconf}.rpmsave >/dev/null 2>&1
        if [ -x /sbin/restorecon ]; then
            /sbin/restorecon %{dhcpconfdir}/dhcpd.conf >/dev/null 2>&1
        fi
    fi
fi

# Initial installation 
if [ $1 -eq 1 ] ; then 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

# Update
if [ $1 -gt 1 ] ; then
  chown -R dhcpd:dhcpd %{_localstatedir}/lib/dhcpd/
fi


%post -n dhclient
/bin/ls -1 %{_sysconfdir}/dhclient* >/dev/null 2>&1
if [ $? = 0 ]; then
    /bin/ls -1 %{_sysconfdir}/dhclient* | \
    /bin/grep -v "\.rpmsave$" 2>/dev/null | \
    while read etcfile ; do
        cf="$(/bin/basename ${etcfile})"
        if [ -f ${etcfile} ] && [ ! -r %{dhcpconfdir}/${cf} ]; then
            /bin/cp -a ${etcfile} %{dhcpconfdir}/${cf} >/dev/null 2>&1
            if [ -x /sbin/restorecon ]; then
                /sbin/restorecon %{dhcpconfdir}/${cf} >/dev/null 2>&1
            fi
        fi
    done || :
fi || :


%preun
# Package removal, not upgrade
if [ $1 -eq 0 ] ; then
    /bin/systemctl --no-reload disable dhcpd.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable dhcpd6.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable dhcrelay.service > /dev/null 2>&1 || :
    /bin/systemctl stop dhcpd.service > /dev/null 2>&1 || :
    /bin/systemctl stop dhcpd6.service > /dev/null 2>&1 || :
    /bin/systemctl stop dhcrelay.service > /dev/null 2>&1 || :
fi


%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
# Package upgrade, not uninstall
if [ $1 -ge 1 ]; then
    /bin/systemctl try-restart dhcpd.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart dhcpd6.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart dhcrelay.service >/dev/null 2>&1 || :
fi


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%triggerun -- dhcp < 12:4.2.0-21.P1
# https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply dhcpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save dhcpd >/dev/null 2>&1 ||:
/usr/bin/systemd-sysv-convert --save dhcpd6 >/dev/null 2>&1 ||:
/usr/bin/systemd-sysv-convert --save dhcrelay >/dev/null 2>&1 ||:
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del dhcpd >/dev/null 2>&1 || :
/sbin/chkconfig --del dhcpd6 >/dev/null 2>&1 || :
/sbin/chkconfig --del dhcrelay >/dev/null 2>&1 || :
/bin/systemctl try-restart dhcpd.service >/dev/null 2>&1 || :
/bin/systemctl try-restart dhcpd6.service >/dev/null 2>&1 || :
/bin/systemctl try-restart dhcrelay.service >/dev/null 2>&1 || :

%triggerpostun -n dhcp-sysvinit -- dhcp < 12:4.2.0-21.P1
# https://fedoraproject.org/wiki/Packaging:SysVInitScript#Initscripts_in_addition_to_systemd_unit_files
/sbin/chkconfig --add dhcpd >/dev/null 2>&1 || :
/sbin/chkconfig --add dhcpd6 >/dev/null 2>&1 || :
/sbin/chkconfig --add dhcrelay >/dev/null 2>&1 || :

%files
%doc dhcpd.conf.sample dhcpd6.conf.sample
%doc contrib/*
%attr(0750,root,root) %dir %{dhcpconfdir}
%attr(0755,dhcpd,dhcpd) %dir %{_localstatedir}/lib/dhcpd
%attr(0644,dhcpd,dhcpd) %verify(not size md5 mtime) %config(noreplace) %{_localstatedir}/lib/dhcpd/dhcpd.leases
%attr(0644,dhcpd,dhcpd) %verify(not size md5 mtime) %config(noreplace) %{_localstatedir}/lib/dhcpd/dhcpd6.leases
%config(noreplace) %{_sysconfdir}/sysconfig/dhcpd
%config(noreplace) %{_sysconfdir}/sysconfig/dhcpd6
%config(noreplace) %{_sysconfdir}/sysconfig/dhcrelay
%config(noreplace) %{dhcpconfdir}/dhcpd.conf
%config(noreplace) %{dhcpconfdir}/dhcpd6.conf
%config(noreplace) %{_sysconfdir}/openldap/schema/dhcp.schema
%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/dispatcher.d
%{_sysconfdir}/NetworkManager/dispatcher.d/12-dhcpd
%attr(0644,root,root)   %{_unitdir}/dhcpd.service
%attr(0644,root,root)   %{_unitdir}/dhcpd6.service
%attr(0644,root,root)   %{_unitdir}/dhcrelay.service
%{_sbindir}/dhcpd
%{_sbindir}/dhcrelay
%{_bindir}/omshell
%attr(0644,root,root) %{_mandir}/man1/omshell.1.gz
%attr(0644,root,root) %{_mandir}/man5/dhcpd.conf.5.gz
%attr(0644,root,root) %{_mandir}/man5/dhcpd.leases.5.gz
%attr(0644,root,root) %{_mandir}/man8/dhcpd.8.gz
%attr(0644,root,root) %{_mandir}/man8/dhcrelay.8.gz
%if %sdt
%{tapsetdir}/*.stp
%endif

%files -n dhclient
%doc dhclient.conf.sample dhclient6.conf.sample README.dhclient.d
%attr(0750,root,root) %dir %{dhcpconfdir}
%dir %{dhcpconfdir}/dhclient.d
%dir %{_localstatedir}/lib/dhclient
%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/dispatcher.d
%{_sysconfdir}/NetworkManager/dispatcher.d/11-dhclient
/sbin/dhclient
/sbin/dhclient-script
%attr(0755,root,root) %{_libdir}/pm-utils/sleep.d/56dhclient
%attr(0644,root,root) %{_mandir}/man5/dhclient.conf.5.gz
%attr(0644,root,root) %{_mandir}/man5/dhclient.leases.5.gz
%attr(0644,root,root) %{_mandir}/man8/dhclient.8.gz
%attr(0644,root,root) %{_mandir}/man8/dhclient-script.8.gz

%files common
%doc LICENSE README RELNOTES doc/References.txt
%attr(0644,root,root) %{_mandir}/man5/dhcp-options.5.gz
%attr(0644,root,root) %{_mandir}/man5/dhcp-eval.5.gz

%files libs
%{_libdir}/libdhcpctl.so.*
%{_libdir}/libomapi.so.*
%{_libdir}/libdst.so.*

%files devel
%doc doc/IANA-arp-parameters doc/api+protocol
%{_includedir}/dhcpctl
%{_includedir}/isc-dhcp
%{_includedir}/omapip
%{_libdir}/libdhcpctl.so
%{_libdir}/libomapi.so
%{_libdir}/libdst.so
%attr(0644,root,root) %{_mandir}/man3/dhcpctl.3.gz
%attr(0644,root,root) %{_mandir}/man3/omapi.3.gz

%files sysvinit
%{_initddir}/dhcpd
%{_initddir}/dhcpd6
%{_initddir}/dhcrelay

%changelog
* Fri Nov 11 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.3-5
- dhclient-script: arping address in BOUND|RENEW|REBIND|REBOOT (#752116)

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:4.2.3-4
- Rebuilt for glibc bug#747377

* Wed Oct 26 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.3-3
- Write lease file AFTER changing of the effective user/group ID.
- Move omshell from dhcp-common to main package (where it originally was).

* Thu Oct 20 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.3-2
- Write PID file BEFORE changing of the effective user/group ID.
- Really define _hardened_build this time

* Thu Oct 20 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.3-1
- 4.2.3

* Tue Oct 18 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.3-0.1.rc1
- 4.2.3rc1

* Sun Oct 09 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-12
- change ownership of /var/lib/dhcpd/ to dhcpd:dhcpd (#744292)
- no need to drop capabilies in dhcpd since it's been running as regular user

* Fri Sep 30 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-11
- 56dhclient: ifcfg file was not sourced (#742482)

* Thu Sep 29 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-10
- dhclient-script: address alias handling fixes from Scott Shambarger (#741786)

* Thu Sep 22 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-9
- dhclient-script: do not backup&restore /etc/resolv.conf and /etc/localtime.

* Wed Sep 21 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-8
- SystemTap support: spec file change, some dummy probes, tapset, simple script

* Mon Sep 19 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-7
- Support for IPoIB (IP over InfiniBand) interfaces (#660681)
- Hopefully last tweak of adding of user and group (#699713)

* Fri Sep 09 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-6
- PIE-RELRO.patch is not needed anymore, defining _hardened_build does the same
- One more tweak of adding of user and group (#699713)

* Fri Sep 09 2011 Adam Tkac <atkac redhat com> - 12:4.2.2-5
- rebuild against new bind

* Fri Aug 26 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-4
- Fix adding of user and group (#699713)

* Fri Aug 19 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-3
- Tighten explicit libs sub-package requirement so that it includes
  the correct architecture as well.

* Fri Aug 12 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-2
- #699713:
  - Use '--enable-paranoia --enable-early-chroot' configure flags
  - Create/delete dhcpd user in %%post/%%postun
  - Run dhcpd/dhcpd6 services with '-user dhcpd -group dhcpd'

* Thu Aug 11 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-1
- 4.2.2: fix for CVE-2011-2748, CVE-2011-2749 (#729850)

* Wed Aug 10 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-0.4.rc1
- Do not ship default /etc/dhcp/dhclient.conf (#560361,c#9)

* Mon Jul 25 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-0.3.rc1
- Improve capabilities patch to be able to run with PARANOIA & EARLY_CHROOT (#699713)

* Mon Jul 18 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-0.2.rc1
- 4.2.2rc1

* Fri Jul 01 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.2-0.1.b1
- 4.2.2b1: upstream merged initialization-delay.patch
- Drop all capabilities in dhcpd/dhcrelay (#699713)

* Fri Jun 17 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-12.P1
- Removed upstream-merged IFNAMSIZ.patch
- Polished patches according to results from static analysis of code.

* Thu Jun 16 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-11.P1
- Add triggerpostun scriptlet tied to dhcp-sysvinit
- Make it possible to build without downstream patches (Kamil Dudka)

* Tue May 17 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-10.P1
- Fix typo in triggerun scriptlet (#705417)

* Mon May 16 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-9.P1
- Packages dhcp/dhclient/dhcp-common explicitly require the libs sub-package
  with the same version and release (bug #705037).
- Fix triggerun scriptlet

* Mon May 09 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-8.P1
- Fix 11-dhclient to export variables (#702735)

* Fri Apr 29 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-7.P1
- Comply with guidelines for systemd services

* Wed Apr 27 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-6.P1
- Fix NetworkManager dispatcher script for dhcpd to support arbitrary interface names

* Wed Apr 06 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-5.P1
- Better fix for CVE-2011-0997: making domain-name check more lenient (#694005)

* Wed Apr 06 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-4.P1
- 4.2.1-P1: fix for CVE-2011-0997 (#694005)

* Fri Mar 25 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-3
- Polished patches according to results from static analysis of code.

* Mon Mar 07 2011 Rex Dieter <rdieter@fedoraproject.org> - 12:4.2.1-2
- rebuild (bind)

* Wed Mar 02 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-1
- 4.2.1

* Wed Feb 23 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-0.6.rc1
- 4.2.1rc1
- Fixed typo in dhclient.leases(5) (#676284)

* Mon Feb 21 2011 Adam Tkac <atkac redhat com> - 12:4.2.1-0.5.b1
- rebuild against new bind-libs-lite

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:4.2.1-0.4.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-0.3.b1
- Prevent anything under _docdir from being scanned. (#674058)

* Fri Jan 28 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-0.2.b1
- dhclient-script improvements, thanks to Ville Skyttä (#672279)

* Thu Jan 27 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.1-0.1.b1
- 4.2.1b1: fix for CVE-2011-0413 (#672996)
- No longer need invalid-dhclient-conf, parse_date and release6-elapsed patches

* Thu Jan 13 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-26.P2
- Fix loading of configuration when LDAP is used (#668276)

* Mon Jan 03 2011 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-25.P2
- Fix OMAPI (#666441)

* Tue Dec 21 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-24.P2
- Provide default /etc/dhcp/dhclient.conf
- Client always sends dhcp-client-identifier (#560361)

* Wed Dec 15 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-23.P2
- Add dhcp-common subpackage (#634673)

* Mon Dec 13 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-22.P2
- 4.2.0-P2: fix for CVE-2010-3616 (#662326)
- Use upstream fix for #628258
- Provide versioned symbols for rpmlint

* Tue Dec 07 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-21.P1
- Porting dhcpd/dhcpd6/dhcrelay services from SysV to Systemd

* Tue Nov 23 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-20.P1
- Remove explicit Obsoletes (#656310)

* Fri Nov 19 2010 Dan Horák <dan[at]danny.cz> - 12:4.2.0-19.P1
- fix build on sparc and s390

* Tue Nov 09 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-18.P1
- Applied Patrik Lahti's patch for DHCPv6 over PPP support (#626514)

* Fri Nov 05 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-17.P1
- fix broken dependencies

* Thu Nov 04 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-16.P1
- 4.2.0-P1: fix for CVE-2010-3611 (#649880)
- dhclient-script: when updating 'search' statement in resolv.conf,
  add domain part of hostname if it's not already there (#637763)

* Wed Oct 20 2010 Adam Tkac <atkac redhat com> - 12:4.2.0-15
- build dhcp's libraries as shared libs instead of static libs

* Wed Oct 20 2010 Adam Tkac <atkac redhat com> - 12:4.2.0-14
- fire away bundled BIND source

* Wed Oct 20 2010 Adam Tkac <atkac redhat com> - 12:4.2.0-13
- improve PIE patch (build libraries with -fpic, not with -fpie)

* Wed Oct 13 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-12
- Server was ignoring client's
  Solicit (where client included address/prefix as a preference) (#634842)

* Thu Oct 07 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-11
- Use ping instead of arping in dhclient-script to handle
  not-on-local-net gateway in ARP-less device (#524298)

* Thu Oct 07 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-10
- Check whether there is any unexpired address in previous lease
  prior to confirming (INIT-REBOOT) the lease (#585418)

* Mon Oct 04 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-9
- RFC 3442 - ignore Router option only if
  Classless Static Routes option contains default router

* Thu Sep 30 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-8
- Explicitly clear the ARP cache and flush all addresses & routes
  instead of bringing the interface down (#574568)

* Tue Sep 07 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-7
- Hardening dhcpd/dhcrelay/dhclient by making them PIE & RELRO

* Thu Sep 02 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-6
- Another fix for handling time values on 64-bit platforms (#628258)

* Wed Sep 01 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-5
- Fix parsing of lease file dates & times on 64-bit platforms (#628258)

* Tue Aug 31 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-4
- RFC 3442 - Classless Static Route Option for DHCPv4 (#516325)

* Fri Aug 20 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-3
- Add DHCRELAYARGS variable to /etc/sysconfig/dhcrelay

* Fri Jul 30 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-2
- Add 12-dhcpd NM dispatcher script (#565921)
- Rename 10-dhclient to 11-dhclient (10-sendmail already exists)

* Wed Jul 21 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.2.0-1
- 4.2.0: includes ldap-for-dhcp

* Mon Jul 12 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-26.P1
- Add LICENSE file to dhclient subpackage.

* Thu Jul 01 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-25.P1
- Adhere to Static Library Packaging Guidelines (#609605)

* Tue Jun 29 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-24.P1
- Fix parsing of date (#514828)

* Wed Jun 03 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-23.P1
- 4.1.1-P1: pair of bug fixes including one for CVE-2010-2156 (#601405)
- Compile with -fno-strict-aliasing

* Mon May 03 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-22
- Fix the initialization-delay.patch (#587070)

* Thu Apr 29 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-21
- Cut down the 0-4 second delay before sending first DHCPDISCOVER (#587070)

* Wed Apr 28 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-20
- Move /etc/NetworkManager/dispatcher.d/10-dhclient script
  from dhcp to dhclient subpackage (#586999)

* Wed Apr 28 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-19
- Add domain-search to the list of default requested DHCP options (#586906)

* Wed Apr 21 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-18
- If the Reply was received in response to Renew or Rebind message,
  client adds any new addresses in the IA option to the IA (#578097)

* Mon Apr 19 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-17
- Fill in Elapsed Time Option in Release/Decline messages (#582939)

* Thu Mar 25 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-16
- In client initiated message exchanges stop retransmission
  upon reaching the MRD rather than at some point after it (#559153)

* Wed Mar 24 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-15
- In dhclient-script check whether bound address
  passed duplicate address detection (DAD) (#559147)
- If the bound address failed DAD (is found to be in use on the link),
  the dhcpv6 client sends a Decline message to the server
  as described in section 18.1.7 of RFC-3315 (#559147)

* Fri Mar 19 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-14
- Fix UseMulticast.patch to not repeatedly parse dhcpd.conf for unicast option
- Fix dhclient-script to set interface MTU only when it's greater than 576 (#574629)

* Fri Mar 12 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-13
- Discard unicast Request/Renew/Release/Decline message
  (unless we set unicast option) and respond with Reply
  with UseMulticast Status Code option (#573090)
- Remove DHCPV6 OPERATION section from dhclient.conf.5
  describing deprecated 'send dhcp6.oro' syntax

* Thu Feb 25 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-12
- Fix paths in man pages (#568031)
- Remove odd tests in %%preun

* Mon Feb 22 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-11
- Add interface-mtu to the list of default requested DHCP options (#566873)

* Fri Feb 19 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-10
- Fix pm-utils/sleep.d/ directory ownership conflict

* Fri Feb 19 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-9
- In dhclient-script:
  - use ip command options '-4' or '-6' as shortcuts for '-f[amily] inet' resp. '-f[amily] inet6'
  - do not use IP protocol family identifier with 'ip link'

* Thu Feb 18 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-8
- Fix installation of pm-utils script (#479639, c#16)

* Tue Feb 16 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-7
- ldap-for-dhcp-4.1.1-2 (#564810)

* Tue Feb 16 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-6
- Fix ldap patch to explicitly link with liblber (#564810)

* Mon Feb 08 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-5
- Fix dhclient-decline-backoff.patch (#562854)

* Fri Feb 05 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-4
- Fix dhclient-script to delete address which the client is going to release
  as soon as it begins the Release message exchange process (#559142)

* Wed Feb 03 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-3
- move /etc/dhcp.conf to /etc/dhcp.conf.rpmsave in %%post (#561094)
- document -nc option in dhclient(8) man page

* Tue Feb 02 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-2
- Fix capability patch (#546765)

* Wed Jan 20 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.1-1
- Upgraded to ISC dhcp-4.1.1

* Mon Jan 18 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.0p1-18
- Hide startup info when starting dhcpd6 service.
- Remove -TERM from calling killproc when stopping dhcrelay (#555672)

* Fri Jan 15 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.0p1-17
- Added init script to also start dhcpd for IPv6 (#552453)
- Added dhcpd6.conf.sample

* Thu Jan 07 2010 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.0p1-16
- Use %%global instead of %%define.

* Mon Dec 14 2009 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.0p1-15
- dhclient logs its pid to make troubleshooting NM managed systems
  with multiple dhclients running easier (#546792)

* Mon Nov 23 2009 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.0p1-14
- Honor DEFROUTE=yes|no for all connection types (#530209)

* Fri Oct 30 2009 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.0p1-13
- Make dhclient-script add IPv6 address to interface (#531997)

* Tue Oct 13 2009 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.0p1-12
- Fix 56dhclient so network comes back after suspend/hibernate (#527641)

* Thu Sep 24 2009 Jiri Popelka <jpopelka@redhat.com> - 12:4.1.0p1-11
- Make dhcpd and dhcrelay init scripts LSB compliant (#522134, #522146)

* Mon Sep 21 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0p1-10
- Obsolete the dhcpv6 and dhcpv6-client packages

* Fri Sep 18 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0p1-9
- Update dhclient-script with handlers for DHCPv6 states

* Wed Aug 26 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0p1-8
- Conditionalize restorecon calls in post scriptlets (#519479)

* Wed Aug 26 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0p1-7
- Do not require policycoreutils for post scriptlet (#519479)

* Fri Aug 21 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0p1-6
- BR libcap-ng-devel (#517649)

* Tue Aug 18 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0p1-5
- Drop unnecessary capabilities in dhclient (#517649)

* Fri Aug 14 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0p1-4
- Upgrade to latest ldap-for-dhcp patch which makes sure that only
  dhcpd links with OpenLDAP (#517474)

* Wed Aug 12 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0p1-3
- Update NetworkManager dispatcher script to remove case conversion
  and source /etc/sysconfig/network

* Thu Aug 06 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0p1-2
- Add /usr/lib[64]/pm-utils/sleep.d/56dhclient to handle suspend and
  resume with active dhclient leases (#479639)

* Wed Aug 05 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0p1-1
- Upgrade to dhcp-4.1.0p1, which is the official upstream release to fix
  CVE-2009-0692

* Wed Aug 05 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-27
- Fix for CVE-2009-0692
- Fix for CVE-2009-1892 (#511834)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:4.1.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-25
- Include NetworkManager dispatcher script to run dhclient.d scripts (#459276)

* Thu Jul 09 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-24
- Ensure 64-bit platforms parse lease file dates & times correctly (#448615)

* Thu Jul 09 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-23
- Upgrade to ldap-for-dhcp-4.1.0-4

* Wed Jul 01 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-22
- Set permissions on /etc/dhcp to 0750 (#508247)
- Update to new ldap-for-dhcp patch set
- Correct problems when upgrading from a previous release and your
  dhcpd.conf file not being placed in /etc/dhcp (#506600)

* Fri Jun 26 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-21
- Handle cases in add_timeout() where the function is called with a NULL
  value for the 'when' parameter (#506626)
- Fix SELinux denials in dhclient-script when the script makes backup
  configuration files and restores them later (#483747)

* Wed May 06 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-20
- Obsolete libdhcp4client <= 12:4.0.0-34.fc10 (#499290)

* Mon Apr 20 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-19
- Restrict interface names given on the dhcpd command line to length
  IFNAMSIZ or shorter (#441524)
- Change to /etc/sysconfig/network-scripts in dhclient-script before
  calling need_config or source_config (#496233)

* Mon Apr 20 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-18
- Make dhclient-script work with pre-configured wireless interfaces (#491157)

* Thu Apr 16 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-17
- Fix setting default route when client IP address changes (#486512, #473658)
- 'reload' and 'try-restart' on dhcpd and dhcrelay init scripts
  will display usage information and return code 3

* Mon Apr 13 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-16
- Correct %%post problems in dhclient package (#495361)
- Read hooks scripts from /etc/dhcp (#495361)
- Update to latest ldap-for-dhcp

* Fri Apr 03 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-15
- Obsolete libdhcp and libdhcp-devel (#493547)

* Thu Apr 02 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-14
- Obsolete libdhcp and libdhcp-devel (#493547)

* Tue Mar 31 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-13
- dhclient obsoletes libdhcp4client (#493213)
- dhcp-devel obsolets libdhcp4client-devel (#493213)

* Wed Mar 11 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-12
- Fix problems with dhclient.d script execution (#488864)

* Mon Mar 09 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-11
- Use LDAP configuration patch from upstream tarball

* Thu Mar 05 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-10
- restorecon fixes for /etc/localtime and /etc/resolv.conf (#488470)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:4.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-8
- Correct subsystem execution in dhclient-script (#486251)

* Wed Feb 18 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-7
- Do not segfault if the ipv6 kernel module is not loaded (#486097)

* Mon Feb 16 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-6
- Enable dhcpv6 support (#480798)
- Fix config file migration in scriptlets (#480543)
- Allow dhclient-script expansion with /etc/dhcp/dhclient.d/*.sh scripts

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 12:4.1.0-5
- rebuild with new openssl

* Tue Jan 13 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-4
- Updated LSB init script header to reference /etc/dhcp/dhcpd.conf (#479012)

* Sun Jan 11 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-3
- Correct syntax errors in %%post script (#479012)

* Sat Jan 10 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-2
- Make sure all /etc/dhcp config files are marked in the manifest
- Include new config file directies in the dhcp and dhclient packages
- Do not overwrite new config files if they already exist

* Tue Jan 06 2009 David Cantrell <dcantrell@redhat.com> - 12:4.1.0-1
- Upgraded to ISC dhcp-4.1.0
- Had to rename the -T option to -timeout as ISC is now using -T
- Allow package rebuilders to easily enable DHCPv6 support with:
      rpmbuild --with DHCPv6 dhcp.spec
  Note that Fedora is still using the 'dhcpv6' package, but some
  users may want to experiment with the ISC DHCPv6 implementation
  locally.

* Thu Dec 18 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-34
- Move /etc/dhclient.conf to /etc/dhcp/dhclient.conf
- Move /etc/dhcpd.conf to /etc/dhcp/dhcpd.conf

* Thu Dec 18 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-33
- Remove unnecessary success/failure lines in init scripts (#476846)

* Wed Dec 03 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-32
- Enable LDAP/SSL support in dhcpd (#467740)
- Do not calculate a prefix for an address we did not receive (#473885)
- Removed libdhcp4client because libdhcp has been removed from Fedora

* Wed Oct 29 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-31
- Use O_CLOEXEC in open(2) calls and "e" mode in fopen(3) calls, build
  with -D_GNU_SOURCE so we pick up O_CLOEXEC (#468984)
- Add missing prototype for validate_port() in common/inet.c

* Thu Oct 23 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-30
- Fix dhclient.conf man page and sample config file to say 'supersede
  domain-search', which is what was actually demonstrated (#467955)

* Wed Oct 01 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-29
- Make sure /etc/resolv.conf has restorecon run on it (#451560)

* Tue Sep 30 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-28
- Forgot to actually include <errno.h> (#438149)

* Tue Sep 30 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-27
- Fix patch fuzziness and include errno.h in includes/dhcpd.h (#438149)

* Tue Sep 30 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-26
- Validate port numbers for dhclient, dhcpd, and dhcrelay to ensure
  that are within the correct range (#438149)

* Mon Sep 29 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-25
- Fix dhcpd so it can find configuration data via LDAP (#452985)

* Tue Sep 16 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-24
- 'server' -> 'service' in dhclient-script (#462343)

* Fri Aug 29 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-23
- Prevent $metric from being set to '' (#460640)
- Remove unnecessary warning messages
- Do not source config file (ifcfg-DEVICE) unless it exists

* Sun Aug 24 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-22
- Add missing '[' to dhclient-script (#459860)
- Correct test statement in add_default_gateway() in dhclient-script (#459860)

* Sat Aug 23 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-21
- Fix syntax error in dhclient-script (#459860)

* Fri Aug 22 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-20
- Rewrite of /sbin/dhclient-script (make the script a little more readable,
  discontinue use of ifconfig in favor of ip, store backup copies of orig
  files in /var rather than in /etc)

* Wed Aug 06 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-19
- Remove 'c' from the domain-search format string in common/tables.c
- Prevent \032 from appearing in resolv.conf search line (#450042)
- Restore SELinux context on saved /etc files (#451560)

* Sun Aug 03 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 12:4.0.0-18
- filter out false positive perl requires

* Fri Aug 01 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-17
- Carry over RES_OPTIONS from ifcfg-ethX files to /etc/resolv.conf (#202923)
- Clean up Requires tags for devel packages
- Allow SEARCH variable in ifcfg files to override search path (#454152)
- Do not down interface if there is an active lease (#453982)
- Clean up how dhclient-script restarts ypbind
- Set close-on-exec on dhclient.leases for SELinux (#446632)

* Sat Jun 21 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-16
- Remove instaces of \032 in domain search option (#450042)
- Make 'service dhcpd configtest' display text indicating the status

* Fri May 16 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-15
- Set close-on-exec on dhclient.leases for SELinux (#446632)

* Tue Apr 01 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-14
- Avoid dhclient crash when run via NetworkManager (#439796)

* Tue Mar 25 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-13
- Update dhclient-script to handle domain-search correctly (#437840)

* Tue Mar 25 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-12
- Remove Requires on openldap-server (#432180)
- Replace CLIENTBINDIR, ETCDIR, DBDIR, and RUNDIR in the man pages with the
  correct paths

* Wed Feb 13 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-11
- Add missing newline to usage() screen in dhclient

* Thu Feb 07 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-10
- Save conf files adding '.predhclient.$interface' to the name (#306381)
- Only restore conf files on EXPIRE/FAIL/RELEASE/STOP if there are no other
  dhclient processes running (#306381)

* Wed Feb 06 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-9
- Match LDAP server option values in stables.c and dhcpd.h (#431003)
- Fix invalid sprintf() statement in server/ldap.c (#431003)

* Wed Feb 06 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-8
- Remove invalid fclose() patch

* Tue Feb 05 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-7
- Don't leak /var/lib/dhclient/dhclient.leases file descriptors (#429890)

* Tue Jan 22 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-6
- read_function() comes from the LDAP patch, so fix it there
- Init new struct universe structs in libdhcp4client so we don't crash on
  multiple DHCP attempts (#428203)

* Thu Jan 17 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-5
- Patch read_function() to handle size_t from read() correctly (#429207)

* Wed Jan 16 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-4
- Fix dhclient.lease file parsing problems (#428785)
- Disable IPv6 support for now as we already ship dhcpv6 (#428987)

* Tue Jan 15 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-3
- Fix segfault in next_iface4() and next_iface6() (#428870)

* Mon Jan 14 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-2
- -fvisibility fails me again

* Mon Jan 14 2008 David Cantrell <dcantrell@redhat.com> - 12:4.0.0-1
- Upgrade to ISC dhcp-4.0.0 (#426634)
     - first ISC release to incorporate DHCPv6 protocol support
     - source tree now uses GNU autoconf/automake
- Removed the libdhcp4client-static package

* Tue Dec 04 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-12
- Requires line fixes

* Tue Dec 04 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-11
- Postinstall script fixes

* Mon Nov 19 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-10
- Remove dhcdbd check from dhcpd init script

* Thu Nov 15 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-9
- Fix chkconfig lines in dhcpd and dhcrelay init scripts (#384431)
- Improve preun scriptlet

* Mon Nov 12 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-8
- Put dhcp.schema in /etc/openldap/schema (#330471)
- Remove manpages patch and keep modified man pages as Source files
- Improve dhclient.8 man page to list options in a style consistent
  with most other man pages on the planet
- Upgrade to latest dhcp LDAP patch, which brings in a new dhcpd-conf-to-ldap
  script, updated schema file, and other bug fixes including SSL support for
  LDAP authentication (#375711)
- Do not run dhcpd and dhcrelay services by default (#362321)

* Fri Oct 26 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-7
- libdhcp4client-devel requires openldap-devel

* Thu Oct 25 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-6
- Rename Makefile.dist to Makefile.libdhcp4client
- Spec file cleanups
- Include stdarg.h in libdhcp_control.h

* Thu Oct 25 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-5
- Remove chkconfig usage for ypbind in dhclient-script (#351211)
- Combine dhcp-static and dhcp-devel packages since there are no shared
  libraries offered
- Remove Requires: openldap-devel on dhcp-devel and libdhcp4client-devel
- Make libdhcp4client-devel require dhcp-devel (for libdhcp_control.h)
- Do not make dhcp-devel require the dhcp package, those are independent

* Wed Oct 24 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-4
- Install libdhcp_control.h to /usr/include/isc-dhcp/libdhcp_control.h
- Update libdhcp4client patch to use new libdhcp_control.h location
- Remove __fedora_contrib/ subdirectory in /usr/share/doc/dhcp-3.1.0,
  install those docs to /usr/share/doc/dhcp-3.1.0

* Wed Oct 24 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-3
- Remove ISC.Cflags variable from libdhcp4client.pc

* Wed Oct 24 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-2
- Fix 'restart' mode in init script (#349341)

* Tue Oct 23 2007 David Cantrell <dcantrell@redhat.com> - 12:3.1.0-1
- Upgrade to ISC dhcp-3.1.0
- Remove unnecessary /usr/include/dhcp4client/isc_dhcp headers
- Make sure restorecon is run on /var/lib/dhcpd/dhcpd.leases (#251688)
- Install dhcp.schema to /etc/openldap/dhcp.schema (#330471)

* Mon Oct 08 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.6-8
- Init script fixes (#320761)
- Removed linux.dbus-example script since we aren't using dhcdbd now
- Remove dhcdbd leftovers from dhclient-script (#306381)

* Wed Sep 26 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.6-7
- In dhcp.conf.5, explain that if no next-server statement applies to the
  requesting client, the address 0.0.0.0 is used (#184484).

* Wed Sep 26 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.6-6
- Init script fixes for dhcpd and dhcrelay (#278601)

* Mon Sep 10 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.6-5
- Fix typos in ldap.c and correct LDAP macros (#283391)

* Tue Sep 04 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.6-4
- Do not override manually configured NTP servers in /etc/ntp.conf (#274761)

* Wed Aug 15 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.6-3
- Remove the -x switch enabling extended new option info.  If given to
  dhclient now, it's ignored.

* Wed Jul 18 2007 Florian La Roche <laroche@redhat.com> - 12:3.0.6-2
- use a new macro name vendor -> vvendor to not overwrite the
  RPMTAG_VENDOR setting

* Tue Jul 10 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.6-1
- Upgrade to ISC dhcp-3.0.6
- Remove the -TERM option from killproc command (#245317)

* Wed Jun 20 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-37
- For init script functions, echo new line after OK or FAIL msg (#244956)

* Fri Jun 15 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-36
- BOOTP_BROADCAST_ALWAYS is not the same as ATSFP, fixed
- Added anycast mac support to dhclient for OLPC

* Tue May 22 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-35
- Disable -fvisibility=hidden for now as it breaks dhcpv4_client() from
  the shared library (#240804)

* Thu Apr 26 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-34
- Init script fixes (#237985, #237983)
- Reference correct scripts in dhclient-script.8 man page (#238036)

* Fri Apr 20 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-33
- Rename -devel-static packages to -static (#225691)

* Tue Apr 17 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-32
- Added missing newline on usage() screen in dhclient

* Thu Apr 12 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-31
- Spec file cleanups (#225691)
- Put libdhcpctl.a and libomapi.a in dhcp-devel-static package
- Put libdhcp4client.a in libdhcp4client-devel-static package

* Wed Apr 11 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-30
- Enable Xen patch again, kernel bits present (#231444)

* Tue Apr 10 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-29
- Spec file cleanups (#225691)

* Mon Apr 09 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-28
- Remove Xen patch (#235649, from RHEL-5, doesn't work correctly for Fedora)

* Sun Apr 01 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-27
- Ensure that Perl and Perl modules are not added as dependencies (#234688)
- Reorganize patches by feature/bug per packaging guidelines (#225691)
- Move the following files from patches to source files:
     linux.dbus-example, linux, Makefile.dist, dhcp4client.h, libdhcp_control.h
- Compile with -fno-strict-aliasing as ISC coding standards generally don't
  agree well with gcc 4.x.x

* Wed Mar 21 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-26
- Fix formatting problems in dhclient man page (#233076).

* Mon Mar 05 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-25
- Man pages need 0644 permissions (#222572)

* Thu Mar 01 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-24
- Include contrib/ subdirectory in /usr/share/doc (#230476)
- Added back Requires for perl since dhcpd-conf-to-ldap needs it (#225691)
- Put copies of dhcp-options and dhcp-eval man pages in the dhcp and
  dhclient packages rather than having the elaborate symlink collection
- Explicitly name man pages in the %%files listings
- Use the %%{_sysconfdir} and %%{_initrddir} macros (#225691)
- Use macros for commands in %%build and %%install
- Split README.ldap, draft-ietf-dhc-ldap-schema-01.txt, and
  dhcpd-conf-to-ldap.pl out of the LDAP patch
- Split linux.dbus-example script out of the extended new option info patch
- Remove unnecessary changes from the Makefile patch

* Wed Feb 28 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-23
- Update Xen partial checksums patch
- Remove perl Requires (#225691)
- Make dhcp-devel depend on dhcp = e:v-r (#225691)
- libdhcp4client-devel Requires pkgconfig (#225691)
- Do not add to RPM_OPT_FLAGS, use COPTS variable instead (#225691)
- Use %%{buildroot} macro instead of RPM_BUILD_ROOT variable (#225691)
- Preserve timestamps on all installed data files (#225691)
- Remove dhcp-options.5.gz and dhcp-eval.5.gz symlinking in post (#225691)
- Use %%defattr(-,root,root,-) (#225691)
- Do not flag init scripts as %%config in %%files section (#225691)

* Tue Feb 27 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-22
- Change license field to say ISC

* Sat Feb 17 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-21
- Obsoletes dhcpcd <= 1.3.22 (#225691)

* Fri Feb 16 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-20
- Review cleanups (#225691)

* Fri Feb 09 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-19
- Require openldap-devel on dhcp-devel and libdhcp4client-devel packages

* Thu Feb 08 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-18
- Fix libdhcp4client visibility _again_ (#198496)

* Thu Feb 08 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-17
- Remove period from summary line (package review)
- Use preferred BuildRoot (package review)

* Sun Feb 04 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-16
- Disable xen-checksums patch for now as it breaks dhclient (#227266)
- Updated fix-warnings patch

* Sun Feb 04 2007 David Woodhouse <dwmw2@redhat.com> - 12:3.0.5-15
- Fix broken file reading due to LDAP patch

* Fri Feb 02 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-14
- Only export the symbols we want in libdhcp4client (#198496)

* Wed Jan 31 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-13
- Add support for dhcpd(8) to read dhcpd.conf from an LDAP server (#224352)
- Remove invalid ja_JP.eucJP man pages from /usr/share/doc

* Wed Jan 31 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-12
- Rebuild

* Tue Jan 30 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-11
- Remove FORTIFY_SOURCE=0 leftovers from testing last week (whoops)

* Tue Jan 30 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-10
- Fix Xen networking problems with partial checksums (#221964)

* Mon Jan 29 2007 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-9
- Remove dhcptables.pl from the source package
- Mark libres.a symbols hidden (#198496)
- Set DT_SONAME on libdhcp4client to libdhcp4client-VERSION.so.0
- Make function definition for dst_hmac_md5_init() match the prototype

* Wed Nov 29 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-8
- Roll md5 patch in to libdhcp4client patch since it's related
- Do not overwrite /etc/ntp/step-tickers (#217663)
- Resolves: rhbz#217663

* Wed Nov 22 2006 Peter Jones <pjones@redhat.com> - 12:3.0.5-7
- Build the MD5 functions we link against.

* Thu Nov 16 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-6
- Set permission of libdhcp4client.so.1 to 0755 (#215910)

* Tue Nov 14 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-5
- Do not link res_query.o in to libdhcp4client (#215501)

* Mon Nov 13 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-4
- Enable relinquish_timeouts() and cancel_all_timeouts() even when
  DEBUG_MEMORY_LEAKAGE_ON_EXIT is not defined
- Add prototypes for b64_pton() and b64_ntop in dst/
- Move variable declarations and labels around in the fix-warnings patch
- Expand the list of objects needed for libdhcp4client (#215328)
- Use libres.a in libdhcp4client since it gives correct minires objects
- Remove the dhcp options table in C, Perl, Python, and text format (these
  were reference files added to /usr/share/doc)

* Mon Nov 13 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-3
- Remove struct universe *universe from envadd_state in the client patch
- Add struct universe *universe to envadd_state in the enoi patch
- Add example dbusified dhclient-script in the enoi patch

* Fri Nov 10 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-2
- Change the way libdhcp4client is compiled (patch main source, create new
  Makefile rather than copy and patch code after main patches)
- Fix up problems generating compiler warnings
- Use 'gcc' for making dependencies
- Pass -fPIC instead of -fpie/-fPIE in compiler flags
- Combine the extended new option info changes in to one patch file (makes
  it easier for outside projects that want to use dhcdbd and NetworkManager)

* Tue Nov 07 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.5-1
- Upgrade to ISC dhcp-3.0.5

* Fri Oct 27 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.4-24
- Put typedef for dhcp_state_e before it's used in libdhcp_control.h (#212612)
- Remove dhcpctl.3 from minires/Makefile.dist because it's in dhcpctl
- Remove findptrsize.c and just set compiler flag for ppc64 and s390x

* Sat Oct 14 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.4-23
- Remove NODEBUGINFO junk from the spec file as well as old/unused code
- Rolled all 68 patches in to one patch since more than half of them get
  overridden by later patches anyway.

* Fri Oct 13 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.4-22
- Send usage() screen in dhclient to stdout rather than the syslog (#210524)

* Mon Sep 11 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.4-21
- Rebuild (#205505)

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 12:3.0.4-20
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Thu Aug 17 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.4-19
- Fix mkdir problem in libdhcp4client.Makefile

* Thu Aug 17 2006 David Cantrell <dcantrell@redhat.com> - 12:3.0.4-18
- Fix dhclient on s390x platform (#202911)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 12:3.0.4-17.1
- rebuild

* Wed Jun 28 2006 Peter Jones <pjones@redhat.com> - 12:3.0.4-17
- export timeout cancellation functions in libdhcp4client

* Wed Jun 28 2006 Florian La Roche <laroche@redhat.com> - 12:3.0.4-16
- add proper coreutils requires for the scripts

* Thu Jun 22 2006 Peter Jones <pjones@redhat.com> - 12:3.0.4-15
- Make timeout dispatch code not recurse while traversing a linked
  list, so it doesn't try to free an entries that have been removed.
  (bz #195723)
- Don't patch in a makefile, do it in the spec.

* Thu Jun 08 2006 Jason Vas Dias <jvdias@redhat.com> - 12:3.0.4-14
- fix bug 191461: preserve ntp.conf local clock fudge statements
- fix bug 193047: both dhcp and dhclient need to ship common
                  man-pages: dhcp-options(5) dhcp-eval(5)

* Tue May 30 2006 Jason Vas Dias <jvdias@redhat.com> - 12:3.0.4-12
- Make -R option take effect in per-interface client configs

* Fri May 26 2006 Jason Vas Dias <jvdias@redhat.com> - 12:3.0.4-10
- fix bug 193047: allow $METRIC to be specified for dhclient routes
- add a '-R <request option list>' dhclient argument

* Fri May 26 2006 Jason Vas Dias <jvdias@redhat.com> - 12:3.0.4-8.1
- fix a libdhcp4client memory leak (1 strdup) and 
  fill in client->packet.siaddr before bind_lease() for pump
  nextServer option.

* Fri May 19 2006 Jason Vas Dias <jvdias@redhat.com> - 12:3.0.4-8
- Make libdhcp4client a versioned .so (BZ 192146)

* Wed May 17 2006 Jason Vas Dias <jvdias@redhat.com> - 12:3.0.4-4
- Enable libdhcp4client build

* Tue May 16 2006 Jason Vas Dias <jvdias@redhat.com> - 12:3.0.4-2
- Fix bug 191470: prevent dhcpd writing 8 byte dhcp-lease-time 
                  option in packets on 64-bit platforms

* Sun May 14 2006 Jason Vas Dias <jvdias@redhat.com> - 12:3.0.4-2
- Add the libdhcp4client library package for use by the new libdhcp 
  package, which enables dhclient to be invoked by programs in a 
  single process from the library. The normal dhclient code is
  unmodified by this.

* Mon May 08 2006 Jason Vas Dias <jvdias@redhat.com> - 12:3.0.4-2
- Add new dhclient command line argument:
  -V <vendor-class-identifier>

* Sat May 06 2006 Jason Vas Dias <jvdias@redhat.com> - 12:3.0.4-1
- Upgrade to upstream version 3.0.4, released Friday 2006-05-05 .
- Add new dhclient command line arguments:
  -H <host-name> : parse as dhclient.conf 'send host-name "<host-name>";'
  -F <fqdn>      : parse as dhclient.conf 'send fqdn.fqdn "<fqdn>";'
  -T <timeout>   : parse as dhclient.conf 'timeout <timeout>;'

* Thu Mar 02 2006 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-26
- fix bug 181908: enable dhclient to operate on IBM zSeries z/OS linux guests:
  o add -I <dhcp-client-identifier> dhclient command line option
  o add -B "always broadcast" dhclient command line option
  o add 'bootp-broadcast-always;' dhclient.conf statement

* Mon Feb 20 2006 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-24
- Apply upstream fix for bug 176615 / ISC RT#15811

* Tue Feb 14 2006 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-22
- fix bug 181482: resolv.conf not updated on RENEW :
  since dhcp-3.0.1rc12-RHScript.patch: "$new_domain_servers" should have
  been "$new_domain_name_servers" :-(

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 11:3.0.3-21.1.1
- bump again for double-long bug on ppc(64)

* Mon Feb 06 2006 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-21.1
- Rebuild for new gcc, glibc and glibc-kernheaders

* Sun Jan 22 2006 Dan Williams <dcbw@redhat.com> - 11:3.0.3-21
- Fix dhclient-script to use /bin/dbus-send now that all dbus related
  binaries are in /bin rather than /usr/bin

* Mon Jan 16 2006 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-20
- fix bug 177845: allow client ip-address as default router 
- fix bug 176615: fix DDNS update when Windows-NT client sends 
                  host-name with trailing nul

* Tue Dec 20 2005 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-18
- fix bug 176270: allow routers with an octet of 255 in their IP address

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec 05 2005 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-16
- fix gcc 4.1 compile warnings (-Werror)

* Fri Nov 19 2005 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-12
- fix bug 173619: dhclient-script should reconfig on RENEW if 
                  subnet-mask, broadcast-address, mtu, routers, etc.
                  have changed
- apply upstream improvements to trailing nul options fix of bug 160655

* Tue Nov 15 2005 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-11
- Rebuild for FC-5
- fix bug 167028 - test IBM's unicast bootp patch (from xma@us.ibm.com)
- fix bug 171312 - silence chkconfig error message if ypbind not installed
- fix dhcpd.init when -cf arg given to dhcpd
- make dhcpd init touch /var/lib/dhcpd/dhcpd.leases, not /var/lib/dhcp/dhcpd.leases

* Tue Oct 18 2005 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-10
- Allow dhclient route metrics to be specified with DHCP options:
  The dhcp-options(5) man-page states:
  'option routers ... Routers should be listed in order of preference' 
  and
  'option static-routes ... are listed in descending order of priority' .
  No preference / priority could be set with previous dhclient-script .
  Now, dhclient-script provides: 
  Default Gateway (option 'routers') metrics:
    Instead of allowing only one default gateway, if more than one router 
    is specified in the routers option, routers following the first router
    will have a 'metric' of their position in the list (1,...N>1).
  Option static-routes metrics:
    If a target appears in the list more than once, routes for duplicate
    targets will have successively greater metrics, starting at 1.

* Mon Oct 17 2005 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-8
- further fix for bug 160655 / ISC bug 15293 - upstream patch:
  do NOT always strip trailing nulls in the dhcpd server
- handle static-routes option properly in dhclient-script :
  trailing 0 octets in the 'target' IP specify the class -
  ie '172.16.0.0 w.x.y.z' specifies '172.16/16 via w.x.y.z'.

* Fri Sep 23 2005 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-7
- fix bug 169164: separate /var/lib/{dhcpd,dhclient} directories
- fix bug 167292: update failover port info in dhcpd.conf.5; give
                  failover ports default values in server/confpars.c
 
* Mon Sep 12 2005 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-6
- fix bug 167273: time-offset should not set timezone by default
                  tzdata's Etc/* files are named with reverse sign
                  for hours west - ie. 'GMT+5' is GMT offset -18000seconds.

* Mon Aug 29 2005 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-4
- fix bug 166926: make dhclient-script handle interface-mtu option
  make dhclient-script support /etc/dhclient{,-$IF}-{up,down}-hooks scripts
  to allow easy customization to support other non-default DHCP options -
  documented in 'man 8 dhclient-script' .
- handle the 'time-offset' DHCP option, requested by default.

* Tue Aug 23 2005 Jason Vas Dias <jvdias@redhat.com> - 11:3.0.3-3
- fix bug 160655: strip trailing '\0' bytes from text options before append
- fix gcc4 compiler warnings ; now compiles with -Werror
- add RPM_OPT_FLAGS to link as suggested in gcc man-page on '-pie' option
- change ISC version string to 'V3.0.3-RedHat' at request of ISC

* Tue Aug  9 2005 Jeremy Katz <katzj@redhat.com> - 11:3.0.3-2
- don't explicitly require 2.2 era kernel, it's fairly overkill at this point

* Fri Jul 29 2005 Jason Vas Dias <jvdias@redhat.com> 11:3.0.3-1
- Upgrade to upstream version 3.0.3 
- Don't apply the 'default boot file server' patch: legacy
  dhcp behaviour broke RFC 2131, which requires that the siaddr
  field only be non-zero if the next-server or tftp-server-name
  options are specified.
- Try removing the 1-5 second wait on dhclient startup altogether.
- fix bug 163367: supply default configuration file for dhcpd
 
* Thu Jul 14 2005 Jason Vas Dias <jvdias@redhat.com> 10:3.0.3rc1-1
- Upgrade to upstream version 3.0.3rc1
- fix bug 163203: silence ISC blurb on configtest 
- fix default 'boot file server' value (packet->siaddr):
  In dhcp-3.0.2(-), this was defaulted to the server address;
  now it defaults to 0.0.0.0 (a rather silly default!) and
  must be specified with the 'next-server' option (not the tftp-boot-server
  option ?!?) which causes PXE boot clients to fail to load anything after
  the boot file.

* Fri Jul 08 2005 Jason Vas Dias <jvdias@redhat.com> 10:3.0.2-14.FC5
- Allow package to compile with glibc-headers-2.3.5-11 (tr.c's use of __u16)

* Fri May 10 2005 Jason Vas Dias <jvdias@redhat.com> 10:3.0.2-14
- Fix bug 159929: prevent dhclient flooding network on repeated DHCPDECLINE
- dhclient fast startup:
   remove dhclient's  random 1-5 second delay on startup if only
   configuring one interface
   remove dhclient_script's "sleep 1" on PREINIT
- fix new gcc-4.0.0-11 compiler warnings for binding_state_t

* Tue May 03 2005 Jason Vas Dias <jvdias@redhat.com> 10:3.0.2-12
- Rebuild for new glibc
- Fix dhcdbd set for multiple interfaces

* Wed Apr 27 2005 Jason Vas Dias <jvdias@redhat.com> 10:3.0.2-11
- as pointed out by Peter Jones, dhclient-script spews
- 'chkconfig: Usage' if run in init state 1 (runlevel returns "unknown".)
- this is now corrected.

* Mon Apr 25 2005 Jason Vas Dias <jvdias@redhat.com> 10:3.0.2-10
- dhclient-script dhcdbd extensions. 
- Tested to have no effect unless dhcdbd invokes dhclient.

* Thu Apr 21 2005 Jason Vas Dias <jvdias@redhat.com> 10:3.0.2-9
- bugs 153244 & 155143 are now fixed with SELinux policy; 
  autotrans now works for dhcpc_t, so restorecons are not required,
  and dhclient runs OK under dhcpc_t with SELinux enforcing.
- fix bug 155506: 'predhclien' typo (emacs!).

* Mon Apr 18 2005 Jason Vas Dias <jvdias@redhat.com> 10:3.0.2-8
- Fix bugs 153244 & 155143: 
      o restore dhclient-script 'restorecon's
      o give dhclient and dhclient-script an exec context of
        'system_u:object_r:sbin_t' that allows them to run
        domainname / hostname and to update configuration files
        in dhclient post script.
- Prevent dhclient emitting verbose ISC 'blurb' on error exit in -q mode

* Mon Apr 04 2005 Jason Vas Dias <jvdias@redhat.com> 10:3.0.2-7
- Add '-x' "extended option environment" dhclient argument:
-  When -x option given to dhclient:
-    dhclient enables arbitrary option processing by writing information
-    about user or vendor defined option space options to environment.
-
- fix bug 153244: dhclient should not use restorecon
- fix bug 151023: dhclient no 'headers & libraries' 
- fix bug 149780: add 'DHCLIENT_IGNORE_GATEWAY' variable
- remove all usage of /sbin/route from dhclient-script

* Thu Mar 24 2005 Florian La Roche <laroche@redhat.com>
- add "exit 0" to post script

* Mon Mar 07 2005 Jason Vas Dias <jvdias@redhat.com> 10.3.0.2-3
- rebuild for gcc4/glibc-2.3.4-14; fix bad memset

* Thu Feb 24 2005 Jason Vas Dias <jvdias@redhat.com> 10:3.0.2-2
- Fix bug 143640: do not allow more than one dhclient to configure an interface

* Mon Feb 21 2005 Jason Vas Dias <jvdias@redhat.com> 10:3.0.2-1
- Upgrade to ISC 3.0.2 Final Release (documentation change only).

* Tue Feb 14 2005 Jason Vas Dias <jvdias@redhat.com> 8:3.0.2rc3-8
- Add better execshield security link options
- fix dhcpd.init when no /etc/dhcpd.conf exists and -cf in DHCPDARGS

* Mon Feb 14 2005 Jason Vas Dias <jvdias@redhat.com> 8:3.0.2rc3-4
- make dhclient-script TIMEOUT mode do exactly the same configuration
- as BOUND / RENEW / REBIND / REBOOT if router ping succeeds

* Mon Feb 14 2005 Jason Vas Dias <jvdias@redhat.com> 3.0.2rc3-4
- fix bug 147926: dhclient-script should do restorecon for modified conf files
- optimize execshield protection

* Thu Feb 10 2005 Jason Vas Dias <jvdias@redhat.com> 8.3.0.4rc3-3
- fix bug 147375: dhcpd heap corruption on 32-bit 'subnet' masks
- fix bug 147502: dhclient should honor GATEWAYDEV and GATEWAY settings
- fix bug 146600: dhclient's timeout mode ping should use -I
- fix bug 146524: dhcpd.init should discard dhcpd's initial output message
- fix bug 147739: dhcpd.init configtest should honor -cf in DHCPDARGS

* Mon Jan 24 2005 Jason Vas Dias <jvdias@redhat.com> 8:3.0.2rc3-2
- fix bug 145997: allow hex 32-bit integers in user specified options

* Thu Jan 06 2005 Jason Vas Dias <jvdias@redhat.com> 8:3.0.2rc3-1
- still need an epoch to get past nvre test

* Thu Jan 06 2005 Jason Vas Dias <jvdias@redhat.com> 3.0.2rc3-1
- fix bug 144417: much improved dhclient-script

* Thu Jan 06 2005 Jason Vas Dias <jvdias@redhat.com> 3.0.2rc3-1
- Upgrade to latest release from ISC, which includes most of our
- recent patches anyway.

* Thu Jan 06 2005 Jason Vas Dias <jvdias@redhat.com> 7:3.0.1-17
- fix bug 144250: gcc-3.4.3-11 is broken :
- log_error ("Lease with bogus binding state: %%d size: %%d",
-   comp -> binding_state,
-   sizeof(comp->binding_state));
- prints:    'Lease with bogus binding state: 257 1'    !
- compiling with gcc33 (compat-gcc-8-3.3.4.2 fixes for now).

* Mon Jan 03 2005 Jason Vas Dias <jvdias@redhat.com> 7:3.0.1-16
- fix bug 143704: dhclient -r does not work if lease held by
- dhclient run from ifup . dhclient will now look for the pid
- files created by ifup.

* Wed Nov 17 2004 Jason Vas Dias <jvdias@redhat.com> 7:3.0.1-14
- NTP: fix bug 139715: merge in new ntp servers only rather than replace
- all the ntp configuration files; restart ntpd if configuration changed.

* Tue Nov 16 2004 Jason Vas Dias <jvdias@redhat.com> 7:3.0.1-12
- fix bug 138181 & bug 139468: do not attempt to listen/send on
-     unconfigured  loopback, point-to-point or non-broadcast
-     interfaces (don't generate annoying log messages)
- fix bug 138869: dhclient-script: check if '$new_routers' is
-     empty before doing 'set $new_routers;...;ping ... $1'

* Wed Oct 06 2004 Jason Vas Dias <jvdias@redhat.com> 7:3.0.1-11
- dhcp-3.0.2b1 came out today. A diff of the 'ack_lease' function
- Dave Hankins and I patched exposed a missing '!' on an if clause
- that got dropped with the 'new-host' patch. Replacing the '!'.
- Also found one missing host_dereference.

* Wed Oct 06 2004 Jason Vas Dias <jvdias@redhat.com> 7:3.0.1-10
- clean-up last patch: new-host.patch adds host_reference(host)
- without host_dereference(host) before returns in ack_lease
- (dhcp-3.0.1-host_dereference.patch)
 
* Mon Sep 27 2004 Jason Vas Dias <jvdias@redhat.com> 7:3.0.1-9
- Fix bug 133522:
- PXE Boot clients with static leases not given 'file' option
- 104 by server - PXE booting was disabled for 'fixed-address'
- clients.

* Fri Sep 10 2004 Jason Vas Dias <jvdias@redhat.com> 7:3.0.1-8
- Fix bug 131212:
- If "deny booting" is defined for some group of hosts,
- then after one of those hosts is denied booting, all
- hosts are denied booting, because of a pointer not being
- cleared in the lease record. 
- An upstream patch was obtained which will be in dhcp-3.0.2.

* Mon Aug 16 2004 Jason Vas Dias <jvdias@redhat.com> 7:3.0.1-7
- Forward DNS update by client was disabled by a bug that I
- found in code where 'client->sent_options' was being
- freed too early.
- Re-enabled it after contacting upstream maintainer
- who confirmed that this was a bug (bug #130069) -
- submitted patch dhcp-3.0.1.preserve-sent-options.patch.
- Upstream maintainer informs me this patch will be in dhcp-3.0.2 .

* Tue Aug 3  2004 Jason Vas Dias <jvdias@redhat.com> 6:3.0.1-6
- Allow 2.0 kernels to obtain default gateway via dhcp

* Mon Aug 2  2004 Jason Vas Dias <jvdias@redhat.com> 5:3.0.1-5
- Invoke 'change_resolv_conf' function to change resolv.conf

* Fri Jul 16 2004 Jason Vas Dias <jvdias@redhat.com> 3:3.0.1
- Upgraded to new ISC 3.0.1 version

* Thu Jun 24 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0.1rc14-5
- Allow dhclient-script to continue without a config file.
- It will use default values.

* Wed Jun 23 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0.1rc14-4
- fix inherit-leases patch

* Tue Jun 22 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0.1rc14-2
- Turn on inherit-leases patch

* Tue Jun 22 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0.1rc14-1
- User kernelversion instead of uname-r
- Update to latest package from ISC
- Remove inherit-leases patch for now.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun 10 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0.1rc13-1
- Update to latest package from ISC

* Thu Jun 10 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0.1rc12-9
- add route back in after route up call

* Wed Jun 9 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0.1rc12-8
- add alex's dhcp-3.0.1rc12-inherit-leases.patch patch

* Tue Jun  8 2004 Bill Nottingham <notting@redhat.com> 1:3.0.1rc12-7
- set device on default gateway route

* Mon May 17 2004 Thomas Woerner <twoerner@redhat.com> 1:3.0.1rc12-6
- compiling dhcpd PIE

* Thu Mar 25 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0.1rc12-5
- Add static routes patch to dhclient-script

* Wed Mar 25 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0.1rc12-4
- Fix init to check config during restart

* Wed Mar 24 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0.1rc12-3
- Fix init script to create leases file if missing

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 21 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.20
- Fix initialization of memory to prevent compiler error

* Mon Jan 5 2004 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.19
- Close leaseFile before exec, to fix selinux error message

* Mon Dec 29 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.18
- Add BuildRequires groff
- Replace resolv.conf if renew and data changes

* Sun Nov 30 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.17
- Add obsoletes dhcpcd

* Wed Oct 8 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.16
- Fix location of ntp driftfile

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.15
- Bump Release

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.14
- Add div0 patch

* Wed Aug 20 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.13
- Add SEARCH to client script

* Wed Aug 20 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.12
- Bump Release

* Wed Aug 20 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.11
- Add configtest

* Fri Aug 1 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.10
- increment for base

* Fri Aug 1 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.9
- Don't update resolv.conf on renewals

* Tue Jul  29 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.8
- increment for base

* Tue Jul  29 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.7
- Fix name of driftfile

* Tue Jul  29 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.6
- increment for base

* Tue Jul  29 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.5
- Change dhcrelay script to check DHCPSERVERS

* Mon Jul  7 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.4
- increment for base

* Mon Jul  7 2003 Dan Walsh <dwalsh@redhat.com> 1:3.0pl2-6.3
- Fix dhclient-script to support PEERNTP and PEERNIS flags.
- patch submitted by aoliva@redhat.com

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 1:3.0pl2-6.1
- add epoch to dhcp-devel versioned requires on dhcp
- build for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 27 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl2-5
- Fix memory leak in parser.

* Mon May 19 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl2-4
- Change Rev for RHEL

* Mon May 19 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl2-3
- Change example to not give out 255 address.

* Tue Apr 29 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl2-2
- Change Rev for RHEL

* Mon Apr 28 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl2-1
- upgrade to 3.0pl2

* Wed Mar 26 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-26
- add usage for dhcprelay -c
- add man page for dhcprelay -c

* Fri Mar 7 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-25
- Fix man dhcpd.conf man page

* Tue Mar 4 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-24
- Fix man dhcpctl.3 page

* Mon Feb 3 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-23
- fix script to handle ntp.conf correctly

* Thu Jan 29 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-22
- Increment release to add to 8.1

* Wed Jan 29 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-21
- Implement max hops patch

* Wed Jan 29 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-20
- It has now been decided to just have options within dhclient kit

* Sun Jan 26 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add defattr() to have files not owned by root

* Fri Jan 24 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-17
- require kernel version

* Fri Jan 24 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-16
- move dhcp-options to separate package

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 9 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-15
- eliminate dhcp-options from dhclient in order to get errata out

* Wed Jan 8 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-14
- VU#284857 - ISC DHCPD minires library contains multiple buffer overflows

* Mon Jan 6 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-13
- Fix when ntp is not installed.

* Mon Jan 6 2003 Dan Walsh <dwalsh@redhat.com> 3.0pl1-12
- Fix #73079 (dhcpctl man page)

* Thu Nov 14 2002 Elliot Lee <sopwith@redhat.com> 3.0pl1-11
- Use generic PTRSIZE_64BIT detection instead of ifarch.

* Thu Nov 14 2002 Preston Brown <pbrown@redhat.com> 3.0pl1-10
- fix parsing of command line args in dhclient.  It was missing a few.

* Mon Oct 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- work on 64bit archs

* Wed Aug 28 2002 Elliot Lee <sopwith@redhat.com> 3.0pl1-9
- Fix #72795

* Mon Aug 26 2002 Elliot Lee <sopwith@redhat.com> 3.0pl1-8
- More #68650 (modify requested options)
- Fix #71453 (dhcpctl man page) and #71474 (include libdst.a) and
  #72622 (hostname setting)

* Thu Aug 15 2002 Elliot Lee <sopwith@redhat.com> 3.0pl1-7
- More #68650 (modify existing patch to also set NIS domain)

* Tue Aug 13 2002 Elliot Lee <sopwith@redhat.com> 3.0pl1-6
- Patch102 (dhcp-3.0pl1-dhcpctlman-69731.patch) to fix #69731

* Tue Aug 13 2002 Elliot Lee <sopwith@redhat.com> 3.0pl1-5
- Patch101 (dhcp-3.0pl1-dhhostname-68650.patch) to fix #68650

* Fri Jul 12 2002 Elliot Lee <sopwith@redhat.com> 3.0pl1-4
- Fix unaligned accesses when decoding a UDP packet

* Thu Jul 11 2002 Elliot Lee <sopwith@redhat.com> 3.0pl1-3
- No apparent reason for the dhclient -> dhcp dep mentioned in #68001,
  so removed it

* Wed Jun 27 2002 David Sainty <saint@redhat.com> 3.0pl1-2
- Move dhclient.conf.sample from dhcp to dhclient

* Mon Jun 25 2002 David Sainty <saint@redhat.com> 3.0pl1-1
- Change to dhclient, dhcp, dhcp-devel packaging
- Move to 3.0pl1, do not strip binaries
- Drop in sysconfig-enabled dhclient-script

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat Jan 26 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- prereq chkconfig

* Tue Jan 22 2002 Elliot Lee <sopwith@redhat.com> 3.0-5
- Split headers/libs into a devel subpackage (#58656)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 28 2001 Elliot Lee <sopwith@redhat.com> 3.0-3
- Fix the #52856 nit.
- Include dhcrelay scripts from #49186

* Thu Dec 20 2001 Elliot Lee <sopwith@redhat.com> 3.0-2
- Update to 3.0, include devel files installed by it (as part of the main
  package).

* Sun Aug 26 2001 Elliot Lee <sopwith@redhat.com> 2.0pl5-8
- Fix #26446

* Mon Aug 20 2001 Elliot Lee <sopwith@redhat.com>
- Fix #5405 for real - it is dhcpd.leases not dhcp.leases.

* Mon Jul 16 2001 Elliot Lee <sopwith@redhat.com>
- /etc/sysconfig/dhcpd
- Include dhcp.leases file (#5405)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Feb 14 2001 Tim Waugh <twaugh@redhat.com>
- Fix initscript typo (bug #27624).

* Wed Feb  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Improve spec file i18n

* Mon Feb  5 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- i18nize init script (#26084)

* Sun Sep 10 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.0pl5
- redo buildroot patch

* Wed Aug 30 2000 Matt Wilson <msw@redhat.com>
- rebuild to cope with glibc locale binary incompatibility, again

* Mon Aug 14 2000 Preston Brown <pbrown@redhat.com>
- check for existence of /var/lib/dhcpd.leases in initscript before starting

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  7 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- /etc/rc.d/init.d -> /etc/init.d
- fix /var/state/dhcp -> /var/lib/dhcp

* Fri Jun 16 2000 Preston Brown <pbrown@redhat.com>
- condrestart for initscript, graceful upgrades.

* Thu Feb 03 2000 Erik Troan <ewt@redhat.com>
- gzipped man pages
- marked /etc/rc.d/init.d/dhcp as a config file

* Mon Jan 24 2000 Jakub Jelinek <jakub@redhat.com>
- fix booting of JavaStations
  (reported by Pete Zaitcev <zaitcev@metabyte.com>).
- fix SIGBUS crashes on SPARC (apparently gcc is too clever).

* Fri Sep 10 1999 Bill Nottingham <notting@redhat.com>
- chkconfig --del in %%preun, not %%postun

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Fri Jun 25 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.0.

* Fri Jun 18 1999 Bill Nottingham <notting@redhat.com>
- don't run by default

* Wed Jun  2 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.0b1pl28.

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- copy the source file in prep, not move

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Mon Jan 11 1999 Erik Troan <ewt@redhat.com>
- added a sample dhcpd.conf file
- we don't need to dump rfc's in /usr/doc

* Sun Sep 13 1998 Cristian Gafton <gafton@redhat.com>
- modify dhcpd.init to exit if /etc/dhcpd.conf is not present

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- Upgraded to 2.0b1pl6 (patch1 no longer needed).

* Thu Jun 11 1998 Erik Troan <ewt@redhat.com>
- applied patch from Chris Evans which makes the server a bit more paranoid
  about dhcp requests coming in from the wire

* Mon Jun 01 1998 Erik Troan <ewt@redhat.com>
- updated to dhcp 2.0b1pl1
- got proper man pages in the package

* Tue Mar 31 1998 Erik Troan <ewt@redhat.com>
- updated to build in a buildroot properly
- don't package up the client, as it doens't work very well <sigh>

* Tue Mar 17 1998 Bryan C. Andregg <bandregg@redhat.com>
- Build rooted and corrected file listing.

* Mon Mar 16 1998 Mike Wangsmo <wanger@redhat.com>
- removed the actual inet.d links (chkconfig takes care of this for us)
  and made the %%postun section handle upgrades.

* Mon Mar 16 1998 Bryan C. Andregg <bandregg@redhat.com>
- First package.
