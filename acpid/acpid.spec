Summary: ACPI Event Daemon
Summary(zh_CN.UTF-8): ACPI 事件服务
Name: acpid
Version: 2.0.12
Release: 1%{?dist}
License: GPLv2+
Group: System Environment/Daemons
Group(zh_CN): 系统环境/服务
Source: http://tedfelix.com/linux/acpid-%{version}.tar.gz
Source1: acpid.init
Source2: acpid.video.conf
Source3: acpid.power.conf
Source4: acpid.power.sh
Source5: acpid.service
Source6: acpid.sysconfig

Patch1: acpid-2.0.2-makefile.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch: ia64 x86_64 %{ix86}
URL: http://tedfelix.com/linux/acpid-netlink.html
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires: systemd-units


%description
acpid is a daemon that dispatches ACPI events to user-space programs.

%description -l zh_CN
%{name} 是一个给用户空间程序调度 ACPI 事件的服务。

%package sysvinit
Summary: ACPI Event Daemon
Summary(zh_CN.UTF-8): ACPI 事件服务
Group: System Environment/Daemons
Group(zh_CN): 系统环境/服务
Requires: %{name} = %{version}-%{release}
Requires(preun): /sbin/service

%description sysvinit
The acpid-sysvinit contains SysV initscript.

%description sysvinit -l zh_CN
%{name} 的 SysV 启动脚本。

%prep
%setup -q

%patch1 -p1 -b .makefile

%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions
mkdir -p $RPM_BUILD_ROOT/lib/systemd/system
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig

chmod 755 $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/videoconf
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/powerconf
install -m 755 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions/power.sh
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/lib/systemd/system
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/acpid

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/acpid


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING README Changelog TODO TESTPLAN
/lib/systemd/system/%{name}.service
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/videoconf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/powerconf
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/acpi/actions/power.sh
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/acpid
%{_bindir}/acpi_listen
%{_sbindir}/acpid
%{_mandir}/man8/acpid.8.gz
%{_mandir}/man8/acpi_listen.8.gz

%files sysvinit
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/acpid

%pre
if [ "$1" = "2" ]; then
	conflist=`ls %{_sysconfdir}/acpi/events/*.conf 2> /dev/null`
	RETCODE=$?
	if [ $RETCODE -eq 0 ]; then
		for i in $conflist; do
			rmdot=`echo $i | sed 's/.conf/conf/'`
	 		mv $i $rmdot
		done
	fi
fi

%post
if [ $1 -eq 1 ]; then
	/bin/systemctl enable %{name}.service > /dev/null 2>&1 || :
fi

%preun
if [ "$1" = "0" ]; then
	/bin/systemctl disable %{name}.service > /dev/null 2>&1 || :
	/bin/systemctl stop %{name}.service > /dev/null 2>&1 || :

fi

%postun
if [ "$1" -ge "1" ]; then
	/bin/systemctl daemon-reload >/dev/null 2>&1 || :
	/bin/systemctl try-restart %{name}.service > /dev/null 2>&1 || :
fi

%triggerun -- %{name} < 2.0.10-2
        /sbin/chkconfig --del acpid >/dev/null 2>&1 || :
        /bin/systemctl try-restart acpid.service >/dev/null 2>&1 || :

%triggerpostun -n %{name}-sysvinit -- %{name} < 2.0.10-2
        /sbin/chkconfig --add acpid >/dev/null 2>&1 || :


%changelog
* Thu Oct 27 2011 Liu Di <liudidi@gmail.com> - 2.0.12-1
- 升级到 2.0.12
