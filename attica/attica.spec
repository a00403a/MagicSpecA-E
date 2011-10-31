
Name:           attica
Version:        0.2.0
Release:        2%{?dist}
Summary:        Implementation of the Open Collaboration Services API
Summary(zh_CN.UTF-8): 开放式协作服务 API 的实现 

#?
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        LGPLv2+
URL:            http://www.kde.org
Source0:        ftp://ftp.kde.org/pub/kde/stable/attica/attica-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake
BuildRequires:  qt4-devel
BuildRequires:  openssl-devel

%description
Attica is a Qt library that implements the Open Collaboration Services
API version 1.4.

%description -l zh-CN.UTF-8
%{name} 是开放式协作服务 API 版本 1.4 的一个 Qt 库实现。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  %{?_cmake_skip_rpath} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
# verify pkg-config version (notoriously wrong in recent releases)
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion libattica)" = "%{version}"


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/libattica.so.0*

%files devel
%defattr(-,root,root,-)
%{_includedir}/attica/
%{_libdir}/libattica.so
%{_libdir}/pkgconfig/libattica.pc


%changelog
* Mon Oct 31 2011 Liu Di <liudidi@gmail.com> - 0.2.0-2
- 为 Magic 3.0 重建 

