Summary: ALSA OSS Compatible Library
Summary(zh_CN.UTF-8): ALSA的OSS兼容库
Name: alsa-oss
Version: 1.0.17
Release: 4%{?dist}
License: GPL
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: http://www.alsa-project.org/
Source: ftp://ftp.alsa-project.org/pub/oss-lib/%{name}-%{version}.tar.bz2
Provides: alsa-oss, alsa-oss-devel, alsa-oss-static, ALSA-oss, ALSA-oss-devel, ALSA-oss-static
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: alsa-lib >= %{version}
BuildRequires: alsa-lib-devel >= %{version}

%description
This is an OSS sound library compatible library for ALSA sound library.

%description -l zh_CN.UTF-8
这是 ALSA 声音库的 OSS 声音库的兼容库。

%prep
%setup -q

%build
%configure -q
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

%post
echo "   Running the post install script..."
/sbin/ldconfig 2>/dev/null && \
echo "   Done."

%postun
if [ "$1" = "0" ] ; then
echo "   Running the post uninstall script..."
/sbin/ldconfig 2>/dev/null && \
echo "   Done."
fi

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir} 

%files
%defattr (-,root,root)
%doc COPYING
%{_prefix}
#%exclude %{_libdir}/*.la
%exclude %{_prefix}/*/debug*
%exclude %{_prefix}/src


%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.0.17-4
- 为 Magic 3.0 重建

* Fri Oct 28 2011 Liu Di <liudidi@gmail.com> - 1.0.17-3
- 为 Magic 3.0 重建

* Fri Sep 05 2008 Liu Di <liudidi@gmail.com> - 1.0.17-1mgc
- 更新到 1.0.17

* Fri Nov 2 2007 Liu Di <liudidi@gmail.com> - 1.0.15-1mgc
- update to 1.0.15

* Mon Jul 2 2007 kde <athena_star {at} 163 {dot} com>  - 1.0.14-1mgc
- update to 1.0.14 release

* Mon Oct 2 2006 kde <jack@linux.net.cn>  - 1.0.12-1mgc
- update to 1.0.12 release

* Fri May 19 2006 kde <jack@linux.net.cn> - 1.0.11-1mgc
- update to release 1.0.11 release

* Sat Jul 23 2005 kde <jack@linux.net.cn> - 1.0.9-1mgc
- update to 1.0.9 release

* Sat Mar 5 2005 kde <jack@linux.net.cn> 1.0.8-1mgc
- initialize the first spec file.
