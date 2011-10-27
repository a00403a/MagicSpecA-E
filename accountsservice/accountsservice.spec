
Name:           accountsservice
Version:        0.6.15
Release:        1%{?dist}
Summary:        D-Bus interfaces for querying and manipulating user account information
Summary(zh_CN.UTF-8): 查询和管理用户账号信息的 D-Bus 接口

Group:          System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
License:        GPLv3+
URL:            http://www.fedoraproject.org/wiki/Features/UserAccountDialog
#VCS: git:git://git.freedesktop.org/accountsservice
Source0:        http://www.freedesktop.org/software/accountsservice/accountsservice-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  polkit-devel
BuildRequires:  intltool
BuildRequires:  systemd-units
BuildRequires:  gobject-introspection-devel

Requires:       polkit
Requires:       shadow-utils

%description
The accountsservice project provides a set of D-Bus interfaces for
querying and manipulating user account information and an implementation
of these interfaces, based on the useradd, usermod and userdel commands.

%description -l zh_CN.UTF-8
查询和管理用户账号信息的 D-Bus 接口。

%package libs
Summary: Client-side library to talk to accountservice
Summary(zh_CN.UTF-8): 与 %{name} 通信的客户端库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{version}-%{release}

%description libs
The accountsservice-libs package contains a library that can
be used by applications that want to interact with the accountsservice
daemon.

%description libs -l zh_CN.UTF-8
与 %{name} 通信的客户端库。

%package devel
Summary: Development files for accountsservice-libs
Summary(zh_CN.UTF-8): %{name}-libs 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-libs = %{version}-%{release}

%description devel
The accountsservice-devel package contains headers and other
files needed to build applications that use accountsservice-libs.

%description devel -l zh_CN.UTF-8
%{name}-libs 的开发文件。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a
%find_lang accounts-service


%files -f accounts-service.lang
%defattr(-,root,root,-)
%doc COPYING README AUTHORS
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.Accounts.conf
%{_libexecdir}/accounts-daemon
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.User.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.Accounts.service
%{_datadir}/polkit-1/actions/org.freedesktop.accounts.policy
%dir %{_localstatedir}/lib/AccountsService/
%dir %{_localstatedir}/lib/AccountsService/users
%dir %{_localstatedir}/lib/AccountsService/icons
/lib/systemd/system/accounts-daemon.service

%files libs
%{_libdir}/libaccountsservice.so.*
%{_libdir}/girepository-1.0/AccountsService-1.0.typelib

%files devel
%{_includedir}/accountsservice-1.0
%{_libdir}/libaccountsservice.so
%{_libdir}/pkgconfig/accountsservice.pc
%{_datadir}/gir-1.0/AccountsService-1.0.gir

%changelog
* Thu Oct 27 2011 Liu Di <liudidi@gmail.com> - 0.6.15-1
- 升级到 0.6.15
