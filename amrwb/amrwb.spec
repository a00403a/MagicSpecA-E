Name: amrwb
Summary: AMR NarrowBand speech codec
Summary(zh_CN.UTF-8): AMR 宽带语音编码译码器
Version: 7.0.0.4
Release: 2%{?dist}
License: LGPL
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.3gpp.org/
Source: http://distfiles.opendarwin.org/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires: gcc-c++

%description
AMR-NB is a narrowband speech codec used in mobile phones.

%description -l zh_CN.UTF-8
AMR-NB 是一款窄带语音编码译码器，它用于移动电话中。

%package devel
Summary: AMR NarrowBand speech codec development files
Summary(zh_CN.UTF-8): AMR 窄带语音编码译码器开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
AMR-NB is a narrowband speech codec used in mobile phones development files.

%description devel -l zh_CN.UTF-8
AMR-NB 是一款窄带语音编码译码器，它用于移动电话中。这是其开发文件。

%prep
%setup

%build
%configure --enable-shared --enable-static
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/libamrwb.so.*
%{_bindir}/amrwb-*

%files devel
%defattr(-,root,root)
%{_includedir}/amrwb/
%{_libdir}/libamrwb.a
%exclude %{_libdir}/libamrwb.la
%{_libdir}/libamrwb.so

%changelog
* Sat Oct 29 2011 Liu Di <liudidi@gmail.com> - 7.0.0.4-2
- 升级到 7.0.0.4

* Mon Aug 6 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.0.1-0.1mgc
- initialize the first spec file for MagicLinux-2.1
