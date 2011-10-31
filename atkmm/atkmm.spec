%global apiver 1.6
# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           atkmm
Version:        2.22.5
Release:        2%{?dist}
Summary:        C++ interface for the ATK library
Summary(zh_CN.UTF-8): ATK 库的 C++ 接口

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/atkmm/%{release_version}/atkmm-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  atk-devel
BuildRequires:  glibmm24-devel

# atkmm was split out into a separate package in gtkmm24 2.21.1
Conflicts:      gtkmm24 < 2.21.1

%description
atkmm provides a C++ interface for the ATK library. Highlights
include typesafe callbacks, widgets extensible via inheritance and a
comprehensive set of widget classes that can be freely combined to
quickly create complex user interfaces.

%description -l zh_CN.UTF-8
ATK 库的 C++ 接口。


%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       atk-devel
Requires:       glibmm24-devel
Conflicts:      gtkmm24-devel < 2.21.1

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        doc
Summary:        Developer's documentation for the atkmm library
Summary(zh_CN.UTF-8): %[name] 的文档婚外情
Group:          Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       glibmm24-doc

%description    doc
This package contains developer's documentation for the atkmm
library. Atkmm is the C++ API for the ATK accessibility toolkit library.

The documentation can be viewed either through the devhelp
documentation browser or through a web browser.

%description doc -l zh_CN.UTF-8
%{name} 的文档包。

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/atkmm-%{apiver}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/atkmm-%{apiver}/

%files doc
%defattr(-,root,root,-)
%doc %{_docdir}/atkmm-%{apiver}/
%doc %{_datadir}/devhelp/


%changelog
* Mon Oct 31 2011 Liu Di <liudidi@gmail.com> - 2.22.5-2
- 为 Magic 3.0 重建　
