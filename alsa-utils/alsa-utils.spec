%define   baseversion	1.0.24
%define   fixversion	.2

Summary: Advanced Linux Sound Architecture (ALSA) utilities
Summary(zh_CN.UTF-8): 高级 Linux 声音架构 (ALSA) 工具
Name:    alsa-utils
Version: %{baseversion}%{?fixversion}
Release: 1%{?dist}
License: GPLv2+
Group:   Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:     http://www.alsa-project.org/
Source:  ftp://ftp.alsa-project.org/pub/utils/alsa-utils-%{version}.tar.bz2
Source4: alsaunmute
Source5: alsaunmute.1
Source6: alsa-info.sh
Source10: alsa.rules
Source11: alsactl.conf
Source20: alsa-restore.service
Source21: alsa-store.service
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: alsa-lib-devel >= %{baseversion}
BuildRequires: libsamplerate-devel
BuildRequires: ncurses-devel
BuildRequires: gettext-devel
BuildRequires: xmlto
Conflicts: udev < 062
Requires: alsa-lib >= %{baseversion}, systemd-units, dialog

%description
This package contains command line utilities for the Advanced Linux Sound
Architecture (ALSA).

%description -l zh_CN.UTF-8
高级 Linux 声音架构 (ALSA) 的命令行工具。

%prep
%setup -q -n %{name}-%{version}

%build
%configure CFLAGS="$RPM_OPT_FLAGS -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64" --sbindir=/sbin --disable-alsaconf
%{__make} %{?_smp_mflags}
%{__cp} %{SOURCE4} .

%install
%{__rm} -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

# Install ALSA udev rules
install -p -m 644 %{SOURCE10} $RPM_BUILD_ROOT/lib/udev/rules.d/90-alsa-restore.rules
install -p -m 644 %{SOURCE20} $RPM_BUILD_ROOT/lib/systemd/system/basic.target.wants/alsa-restore.service
install -p -m 644 %{SOURCE21} $RPM_BUILD_ROOT/lib/systemd/system/shutdown.target.wants/alsa-store.service

# Install support utilities
mkdir -p -m755 $RPM_BUILD_ROOT/bin
install -p -m 755 alsaunmute %{buildroot}/bin/
mkdir -p -m755 $RPM_BUILD_ROOT/%{_mandir}/man1
install -p -m 644 %{SOURCE5} %{buildroot}/%{_mandir}/man1/alsaunmute.1

# Link alsactl to /usr/sbin
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
ln -s ../../sbin/alsactl $RPM_BUILD_ROOT/%{_sbindir}/alsactl

# Move /usr/share/alsa/init to /lib/alsa/init
mkdir -p -m 755 %{buildroot}/lib/alsa
mv %{buildroot}%{_datadir}/alsa/init %{buildroot}/lib/alsa

# Link /lib/alsa/init to /usr/share/alsa/init back
ln -s ../../../lib/alsa/init %{buildroot}%{_datadir}/alsa/init

# Create a place for global configuration
mkdir -p -m 755 %{buildroot}/etc/alsa
install -p -m 644 %{SOURCE11} %{buildroot}/etc/alsa

# Create /var/lib/alsa tree
mkdir -p -m 755 %{buildroot}/var/lib/alsa

# Install alsa-info.sh script
install -p -m 755 %{SOURCE6} %{buildroot}/usr/bin/alsa-info
ln -s alsa-info %{buildroot}/usr/bin/alsa-info.sh

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING ChangeLog README TODO
%config /etc/alsa/*
/bin/*
/sbin/*
/lib/udev/rules.d/*
/lib/systemd/system/*
/lib/systemd/system/basic.target.wants/*
/lib/systemd/system/shutdown.target.wants/*
/lib/alsa/init/*
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/alsa/
%{_datadir}/sounds/*
%{_mandir}/man?/*
%dir /etc/alsa/
%dir /lib/alsa/
%dir /lib/alsa/init/
%dir /var/lib/alsa/

%post
if [ -s /etc/alsa/asound.state -a ! -s /etc/asound.state ] ; then
  mv /etc/alsa/asound.state /etc/asound.state
fi
if [ -s /etc/asound.state -a ! -s /var/lib/alsa/asound.state ] ; then
  mv /etc/asound.state /var/lib/alsa/asound.state
fi

%changelog
* Fri Oct 28 2011 Liu Di <liudidi@gmail.com> - 1.0.24.2-1
- 升级到 1.0.24.2

