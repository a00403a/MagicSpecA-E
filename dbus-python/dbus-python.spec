%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define pyrex_version 0.9.3
%define dbus_glib_version 0.71
%define dbus_version 0.92

Summary: D-Bus Python Bindings
Summary(zh_CN.UTF-8): D-Bus Python 绑定
Name: dbus-python
Version: 0.83.1
Release: 2%{?dist}
URL: http://www.freedesktop.org/software/dbus/
Source0: http://dbus.freedesktop.org/releases/%{name}-%{version}.tar.gz
Patch0: dbus-python-0.70-fix-binary-modules-dir.patch
License: AFL/GPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: Pyrex >= %{pyrex_version}
Requires: libxml2-python

%description

D-Bus python bindings for use with python programs.

%description -l zh_CN.UTF-8

使用python程序的D-Bus python 绑定。

%prep
%setup -q

%build
%configure

%{__make}
#CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf %{buildroot}
%makeinstall
#PKG_CONFIG_PATH=%{_libdir}/pkgconfig %{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

%doc COPYING ChangeLog NEWS

#%{python_sitearch}/dbus/*.so
%{python_sitearch}/*
%{_libdir}/pkgconfig/*
%{_docdir}/*
%{_includedir}/*

%changelog
* Thu Jul 07 2007 Liu Di <liudidi@gmail.com> - 0.81.1-1mgc
- update to 0.81.1

* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> - 0.71-1mgc
- update to 0.71,rebuild for Magic

* Fri Aug 18 2006 Karsten Hopp <karsten@redhat.com> - 0.70-6
- require libxml2-python for site-packages/dbus/introspect_parser.py

* Thu Jul 20 2006 Jesse Keating <jkeating@redhat.com> - 0.70-5
- Remove unnecessary obsoletes

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-4
- Try python_sitearch this time

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-3
- Add a BR on dbus-devel

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-2
- Spec file cleanups
- Add PKG_CONFIG_PATH

* Mon Jul 17 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-1
- Initial package import
