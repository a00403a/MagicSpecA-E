# Define aufs version
%define git 1
%define gitdate 20120620

Summary:		Utilities to Manipulate aufs Components
Summary(zh_CN.UTF-8): 	处理 aufs 组件的工具
Name:			aufs-util
Version:			3
Release:			0.git%{gitdate}%{?dist}.1
License:			GPL
Group:			System Environment/Base
Group(zh_CN.UTF-8):		系统环境/基本
URL:				http://aufs.sourceforge.net/
Source0:			%{name}-git%{gitdate}.tar.xz
Source1:			make_aufs-util_git_package.sh
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Packager:		kde <jack@linux.net.cn>
Requires(pre):	%{_sbindir}/groupadd
Requires(postun):	%{_sbindir}/groupdel
Provides:		aufs
Obsoletes:		aufs

AutoReq:		no

%description
These are command line tools to inspect and manipulate the components
merged by aufs in user space.

%description -l zh_CN.UTF-8
这是在用户空间处理 aufs 文件的命令行工具。

%package		libs
Summary:		Aufs lib files
Group:			Development/Librarie

%description libs
Aufs lib files.

%package		devel
Summary:		Aufs devel files
Summary(zh_CN.UTF-8):	Aufs 开发文件
Group:			Development/Libraries
Group(zh_CN.UTF-8):		开发/库
Requires:		%{name} = %{version}-%{release}
Requires: 		pkgconfig

%description		devel
Aufs (Another unionfs) development files.

%description		devel -l zh_CN.UTF-8
Aufs (另一个 Unionfs) 的开发文件。


%prep
%setup -q -n %{name}-git%{gitdate}

%build
make

%install
rm -rf %{buildroot}
install -d ${RPM_BUILD_ROOT}%{_mandir}/man5 ${RPM_BUILD_ROOT}%{_bindir} %{buildroot}%{_sbindir}
make install DESTDIR=%{buildroot}
mv %{buildroot}/sbin %{buildroot}/usr

magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%pre 
if [ "$1" = "1" ]; then
     %{_sbindir}/groupadd -r aufs &>/dev/null || :
fi

%files
%defattr(-,root,root)
%{_bindir}/aubrsync
%{_bindir}/auchk
%{_sbindir}/mount.aufs
%{_sbindir}/umount.aufs
%{_sbindir}/auplink
%{_sysconfdir}/*
%{_mandir}/man5/aufs*
%{_bindir}/aubusy
%{_sbindir}/auibusy
%{_libdir}/libau.so
%{_libdir}/libau.so.2
%{_libdir}/libau.so.2.6

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 3-0.git20120620.1
- 为 Magic 3.0 重建

* Fri Nov 14 2008 Liu Di <liudidi@gmail.com> - cvs20081114-1mgc
- 更新到 cvs20081114
- 在 2.6.25.20 上编译

* Mon Aug 04 2008 Liu Di <liudidi@gmail.com> - cvs20080804-1mgc
- 升级到 cvs20080804
- 在 2.6.25.14 上编译

* Sun Jun 15 2008 Liu Di <liudidi@gmail.com> - cvs20080615-1mgc
- 在 2.6.25.6 内核上重建
