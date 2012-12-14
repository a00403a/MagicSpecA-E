# $Id: apt.spec 3053 2005-03-24 17:16:13Z dag $
# Authority: axel
# Upstream: Gustavo Niemeyer <niemeyer$conectiva,com>

%{?dist: %{expand: %%define %dist mgc30}}
%define LIBVER 3.3
%define git 1
%define gitdate 20121214

Summary: Debian's Advanced Packaging Tool with RPM support
Summary(zh_CN.UTF-8): 使用RPM支持的 Debian 高级包工具
Name: apt
Version: 0.5.15lorg3.95
Release: 7%{?dist}
License: GPL
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: https://apt-rpm.org

Packager: Liu Di <liudidi@gmail.com>
Vendor: MagicGroup
%if 0%{git}
#git clone http://apt-rpm.org/scm/apt.git
Source: %{name}-git%{gitdate}.tar.xz
%else
Source: http://apt-rpm.org/testing/apt-0.5.15lorg3.94a.tar.bz2
%endif
Source1: make_apt_git_package.sh
Patch0: apt-0.5.15lorg3.94-rpmpriorities.patch
Patch1: apt-0.5.15lorg3.94-nodignosig.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: rpm-devel >= 4.6, zlib-devel, gettext
BuildRequires: readline-devel, bison, lua-devel

%{!?dist:BuildRequires: beecrypt-devel, elfutils-devel}

Requires: rpm >= 4.0, zlib, bzip2-libs, libstdc++

%description
A port of Debian's apt tools for RPM based distributions, or at least
originally for Conectiva and now Red Hat Linux. It provides the apt-get
utility that provides a simpler, safer way to install and upgrade packages.
APT features complete installation ordering, multiple source capability and
several other unique features.

%description -l zh_CN.UTF-8
Debian的apt工具到基本rpm的发行版的一个移植，至少支持Conectiva和红帽Linux，
当然MagicLinux也支持。它提供了apt-get工具，可以简单安全的安装和升级包。
APT的特性有完全的安装次序，多个源的功能并有其它几个独特的特点。

%package devel
Summary: Header files, libraries and development documentation for %{name}
Summary(zh_CN.UTF-8): %{name}的头文件，库和开发文档
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%description devel -l zh_CN.UTF-8
这个包包含了 %{name} 的头文件，静态链接库和开发文档。如果你想使用 %{name}
开发程序，你需要安装 %{name}-devel。

%prep
%if 0%{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup
%endif
%patch0 -p1 -b .rpmpriorities
#%patch1 -p1 -b .nodignosig

%{__perl} -pi.orig -e 's|RPM APT-HTTP/1.3|Dag RPM Repository %{dist}/%{_arch} APT-HTTP/1.3|' methods/http.cc

%build
autoreconf -fisv
%configure \
	--program-prefix="%{?_program_prefix}" \
	--includedir="%{_includedir}/apt-pkg"
#	--with-hashmap
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall \
	includedir="%{buildroot}%{_includedir}/apt-pkg"
magic_rpm_clean.sh
#%find_lang %{name}

%{__install} -d -m0755 \
		%{buildroot}%{_sysconfdir}/apt/{apt.conf.d,sources.list.d} \
		%{buildroot}%{_localstatedir}/cache/apt/{archives/partial,genpkglist,gensrclist} \
		%{buildroot}%{_localstatedir}/state/apt/lists/partial \
		%{buildroot}%{_libdir}/apt/scripts/
%{__install} -p -m0644 etc/rpmpriorities %{buildroot}%{_sysconfdir}/apt/

touch %{buildroot}%{_sysconfdir}/apt/preferences \
	%{buildroot}%{_sysconfdir}/apt/vendors.list

magic_rpm_clean.sh

#%{__ln_s} -f %{_libdir}libapt-pkg-libc6.3-5.so.0 %{buildroot}%{_libdir}libapt-pkg-libc6.3-5.so.%{LIBVER}
mkdir -p %{buildroot}/var/lib/apt/lists/partial
touch %{buildroot}/var/lib/apt/lists/lock

%post
/usr/sbin/ldconfig 2>/dev/null

%postun
/usr/sbin/ldconfig 2>/dev/null

%clean
%{__rm} -rf %{buildroot}

#%files -f %{name}.lang
%files
%defattr(-, root, root, 0755)
%doc AUTHORS* COPYING* TODO contrib/ doc/examples/
%doc %{_mandir}/man?/*
%dir %{_sysconfdir}/apt/
%config(noreplace) %{_sysconfdir}/apt/preferences
%config(noreplace) %{_sysconfdir}/apt/vendors.list
%config %{_sysconfdir}/apt/rpmpriorities
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/
%{_bindir}/apt-cache
%{_bindir}/apt-cdrom
%{_bindir}/apt-config
%{_bindir}/apt-get
%{_bindir}/apt-shell
%{_bindir}/genbasedir
%{_bindir}/genpkglist
%{_bindir}/gensrclist
%{_bindir}/countpkglist
%{_libdir}/apt/
%{_libdir}/libapt-pkg*.so.*
%{_localstatedir}/cache/apt/
%{_localstatedir}/state/apt/
/var/lib/apt/*

%files devel
%defattr(-, root, root, 0755)
%{_libdir}/libapt-pkg.a
%exclude %{_libdir}/libapt-pkg.la
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libapt-pkg.so
%{_includedir}/apt-pkg/
#exclude %{_libdir}/*.la

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.95-7
- 为 Magic 3.0 重建

* Fri Apr 13 2012 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.95-6
- 为 Magic 3.0 重建

* Thu Apr 30 2009 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.94a-4
- 在 rpm 4.7.0 上重建

* Mon Jan 21 2008 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.94a-1mgc
- update 

* Fri Sep 15 2006 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.90-1mgc
- update

* Fri Jul 09 2006 Liu Di <liudidi@gmail.com> - 0.5.15lorg3-2mgc
- Rebuild for RPM 4.4, add cuit.lcuc.ort to apt source

* Tue May 16 2006 Liudi <liudidi@gmail.com>
- fix magic-apt setting

* Tue Aug 2 2005 KanKer <kanker@163.com>
- fix magic-apt setting error

* Wed Jul 27 2005 KanKer <kanker@163.com>
- rebuild

* Sat Nov 20 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc6-4 - 3053+/dag
- Added readline-devel as buildrequirement for apt-shell.

* Thu Jul 01 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc6-3
- Fix for apt-bug triggered by mach.

* Fri Jun 04 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc6-2
- Make apt understand about architectures.

* Tue Mar 23 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc6-1
- Updated to release 0.5.15cnc6.

* Sat Jan 24 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc1-1
- Added RHAS21 repository.

* Sun Jan 04 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc5-0
- Updated to release 0.5.15cnc5.

* Sat Dec 06 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc4-1
- Disabled the epoch promotion behaviour on RH9.

* Thu Dec 04 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc4-0
- Updated to release 0.5.15cnc4.

* Tue Nov 25 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc3-0
- Updated to release 0.5.15cnc3.

* Mon Nov 10 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc2-0
- Updated to release 0.5.15cnc2.

* Mon Nov 10 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc1-1
- Fixed apt pinning.
- Added RHFC1 repository.

* Sat Nov 08 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc1-0
- Updated to release 0.5.15cnc1.

* Sun Oct 26 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc6-1
- Added RHEL3 repository.

* Tue Jun 10 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc6-0
- Added newrpms and enable it by default.
- Updated to release 0.5.5cnc6.

* Tue Jun 03 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc5-4
- Added freshrpms and enable it by default.

* Sun Jun 01 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc5-3
- Work around a bug in apt (apt.conf).

* Fri May 30 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc5-2
- Moved sources.list to sources.d/

* Wed Apr 16 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc5-1
- Updated to release 0.5.5cnc5.

* Tue Apr 08 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc4.1-2
- RH90 repository rename from redhat/9.0 to redhat/9.

* Sat Apr 05 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc4.1-1
- FreshRPMS fixes to repository locations.

* Sun Mar 09 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc4.1-0
- Updated to release 0.5.5cnc4.1.

* Fri Feb 28 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc3-0
- Updated to release 0.5.5cnc3.

* Tue Feb 25 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc2-0
- Updated to release 0.5.5cnc2.

* Mon Feb 10 2003 Dag Wieers <dag@wieers.com> - 0.5.4cnc9-0
- Initial package. (using DAR)
