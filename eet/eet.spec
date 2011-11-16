%define date %{nil}
Summary: eet
Summary(zh_CN.UTF-8): eet
Name: eet
Version: 1.4.1
%if 0%{date}
Release: 0.cvs%{date}%{?dist}
%else
Release: 0.2%{?dist}
%endif
License: BSD
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.enlightenment.org/
%if 0%{date}
Source:	%{name}-cvs%{date}.tar.bz2
%else
Source: http://download.enlightenment.org/releases/%{name}-%{version}.tar.gz
%endif
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
Enlightenment 窗口管理器的库。

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
%if 0%{date}
%setup -n %{name}-cvs%{date}
%else
%setup -n %{name}-%{version}
%endif

%build
%if 0%{date}
./autogen.sh
%endif
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

%changelog
* Sun Oct 5 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.1.0-0.1mgc
- 更新至 1.1.0
- 戊子  九月初七

* Sat Jun 14 2008 Ni Hui <shuizhuyuanluo@126.com> - 1.0.1-0.1mgc
- 首次生成 rpm 包
- 去除非中文语言文件
- 戊子  五月十一

