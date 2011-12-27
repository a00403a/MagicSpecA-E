#已切换到 git
%define git 1
%define git_date 20111227
%define _prefix /usr
%define ver 1.5.14

%define debug 0
%define final 1

%define alsa 1
%define qt_version 3.3.8d

Version: %{ver}
%if %{git}
Release: 0.%{git_date}.%{?dist}
%else
Release: 0.1%{?dist}
%endif
Summary: aRts (analog realtime synthesizer) - the KDE sound system
Summary(zh_CN.UTF-8): aRts (analog realtime synthesizer) - KDE 的声音系统
Name: arts
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
License: LGPL
Url: http://www.kde.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
%if %{git}
Source0: %{name}-git%{git_date}.tar.xz
%else
Source0: ftp://ftp.kde.org/pub/kde/stable/%{ver}/src/%{name}-%{version}.tar.bz2
%endif

Source1: make_%{name}_git_package.sh

Patch0: arts-vorbis-fix.dif
Patch1: arts-1.3.1-alsa.patch

Prereq: /sbin/ldconfig
Requires: audiofile

%if %{alsa}
BuildRequires: alsa-lib-devel >= 1.0.2
%endif
BuildRequires: autoconf >= 2.53
BuildRequires: automake
BuildRequires: qt-devel >= %{qt_version}
BuildRequires: perl
BuildRequires: glib2-devel
BuildRequires: libvorbis-devel
BuildRequires: audiofile-devel
BuildRequires: tqtinterface-devel

## workaround for gcc bug on ia64
%ifarch ia64
%define optflags -O0 -g
%endif

%description
arts (analog real-time synthesizer) is the sound system of KDE 3.

The principle of arts is to create/process sound using small modules which do
certain tasks. These may be create a waveform (oscillators), play samples,
filter data, add signals, perform effects like delay/flanger/chorus, or
output the data to the soundcard.

By connecting all those small modules together, you can perform complex
tasks like simulating a mixer, generating an instrument or things like
playing a wave file with some effects.

%description -l zh_CN.UTF-8
arts (模拟实时合成器，analog realtime synthesizer) 是 KDE 3 的
声音系统。

arts 的原理是使用小模块来建立、加工声音的某些任务。这些可能是
建立一个波形（振荡），播放采样，过滤数据，添加信号，操作像延
迟、提升、混响等效果，或者输出数据到声卡。

通过把这些小模块放在一起，您可以进行一些复杂的操作，比如模拟
混音器，生成乐器或带有一些效果地播放波形文件。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Development files for the aRts sound server
Summary(zh_CN.UTF-8): aRts 声音服务器的开发文件
Requires: %{name} = %{version}-%{release}
Requires: esound-devel
Requires: glib2-devel
Requires: libvorbis-devel
Requires: audiofile-devel
%if %{alsa}
Requires: alsa-lib-devel
%endif


%description devel
arts (analog real-time synthesizer) is the sound system of KDE 3.

The principle of arts is to create/process sound using small modules which do
certain tasks. These may be create a waveform (oscillators), play samples,
filter data, add signals, perform effects like delay/flanger/chorus, or
output the data to the soundcard.

By connecting all those small modules together, you can perform complex
tasks like simulating a mixer, generating an instrument or things like
playing a wave file with some effects.

Install arts-devel if you intend to write applications using arts (such as
KDE applications using sound).

%description devel -l zh_CN.UTF-8
如果您需要编写使用 arts 的程序（比如使用声音的 KDE 程序）可以
安装 arts-devel。

%prep
%if %{git}
%setup -q -n %{name}-git%{git_date}
%else
%setup -q -n %{name}-%{version}
%endif
%patch0 -p0
%patch1 -p1 

%build
mkdir build
cd build
%{cmake} ..
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}
#install -m 0644 ../artsc/artsc.h %{buildroot}%{_includedir}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}


%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude /usr/*/debug*
%exclude /usr/src

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
* Mon Oct 31 2011 Liu Di <liudidi@gmail.com> - 1.5.13-0.20111031
- 更新到 trinity 的 git 20111031 版本

* Fri Aug 29 2008 Liu Di <liudidi@gmail.com> - 1.5.10-1mgc
- 更新到 1.5.10

* Tue Feb 19 2008 Liu Di <liudidi@gmail.com> - 1.5.9-1mgc
- update to 1.5.9

* Thu Oct 18 2007 kde <athena_star {at} 163 {dot} com>  - 1.5.8-1mgc
- 1.5.8

* Fri May 25 2007 kde <athena_star {at} 163 {dot} com>  - 1.5.7-1mgc
- 1.5.7

* Fri Jan 25 2007 Liu Di <liudidi@gmail.com> - 1.5.6-1mgc
- 1.5.6

* Fri Oct 20 2006 Liu Di <liudidi@gmail.com> - 1.5.5-1mgc
- 1.5.5

* Thu Aug 24 2006 Liu Di <liudidi@gmail.com> - 1.5.4-1mgc
- 1.5.4

* Wed May 31 2006 Liu Di <liudidi@gmail.com> - 1.5.3-1mgc
- 1.5.3

* Sat Apr 15 2006 KanKer <kanker@163.com>
- 1.5.2

* Thu Dec 13 2005 KanKer <kanker@163.com>
- rebuild on new alsa

* Mon Oct 17 2005 KanKer <kanker@163.com>
- 1.4.3

* Sun Jul 31 2005 KanKer <kanker@163.com>
- 1.4.2

* Thu May 31 2005 KanKer <kanker@163.com>
- 1.4.1

* Sat Mar 19 2005 KanKer <kanker@163.com>
- 1.4.0

* Fri Dec 17 2004 KanKer <kanker@163.com>
- 1.3.2

*Sat Aug 21 2004 KanKer <kanker@163.com>
- 1.3.0

