Summary: e_dbus
Summary(zh_CN.UTF-8): e_dbus
Name: e_dbus
Version: 1.7.3
Release: 2%{?dist}
License: BSD
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.enlightenment.org/
Source: http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: imlib2-devel freetype-devel


%description
Enlightenment is a window manager for the X Window System that
is designed to be powerful, extensible, configurable and
pretty darned good looking! It is one of the more graphically
intense window managers.

Enlightenment goes beyond managing windows by providing a useful
and appealing graphical shell from which to work. It is open
in design and instead of dictating a policy, allows the user to 
define their own policy, down to every last detail.

This package will install the Enlightenment window manager.

%description -l zh_CN.UTF-8
e_dbus

%package devel
Summary: %{name} development files
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Header and library definition files for developing applications
that use the %{name} library.

%description devel -l zh_CN.UTF-8
%{name}-devel 软件包包含了使用 %{name} 开发程序所需的库和头文件。


%prep
%setup -n %{name}-%{version}

%build
%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files devel
%defattr(-, root, root, -)
%{_includedir}
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/e_dbus/logo.png

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.0.1-2
- 为 Magic 3.0 重建

* Sat Jun 14 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.5.0.043-0.1mgc
- 首次生成 rpm 包
- 戊子  五月十一

