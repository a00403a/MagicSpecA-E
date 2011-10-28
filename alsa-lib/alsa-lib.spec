#define  prever         rc3
#define  prever_dot     .rc3
#define postver		a

Summary: The Advanced Linux Sound Architecture (ALSA) library
Summary(zh_CN.UTF-8): 高级 Linux 声音架构 (ALSA) 库
Name:    alsa-lib
Version: 1.0.24.1
Release: 1%{?prever_dot}%{?dist}
License: LGPLv2+
Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source:  ftp://ftp.alsa-project.org/pub/lib/%{name}-%{version}%{?prever}%{?postver}.tar.bz2
Source10: asound.conf
Patch0:  alsa-lib-1.0.24-config.patch
Patch2:  alsa-lib-1.0.14-glibc-open.patch
Patch4:	 alsa-lib-1.0.16-no-dox-date.patch
URL:     http://www.alsa-project.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: doxygen
Requires(post): /sbin/ldconfig, coreutils

%description
The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
functionality to the Linux operating system.

This package includes the ALSA runtime libraries to simplify application
programming and provide higher level functionality as well as support for
the older OSS API, providing binary compatibility for most OSS programs.

%description -l zh_CN.UTF-8
高级 Linux 声音架构 (ALSA) 为 Linux 操作系统提供了音频和 MIDI 功能。

这个包包含了 ALSA 的运行库，可以简化程序开发并提供了高级函数，也支持旧的
OSS API，使其能提供大多数 OSS 程序的二进制兼容。

%package devel
Summary: Development files from the ALSA library
Summary(zh_CN.UTF-8): %{name} 的开发库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
functionality to the Linux operating system.

This package includes the ALSA development libraries for developing
against the ALSA libraries and interfaces.

%description devel -l zh_CN.UTF-8
%{name} 的开发库。

%prep
%setup -q -n %{name}-%{version}%{?prever}%{?postver}
%patch0 -p1 -b .config
%patch2 -p1 -b .glibc-open
%patch4 -p1 -b .no-dox-date

%build
%configure --disable-aload --with-plugindir=%{_libdir}/alsa-lib
# Remove useless /usr/lib64 rpath on 64bit archs
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
make doc

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# We need the library to be available even before /usr might be mounted
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libasound.so.* %{buildroot}/%{_lib}
ln -snf ../../%{_lib}/libasound.so.2 %{buildroot}%{_libdir}/libasound.so

# Install global configuration files
mkdir -p -m 755 %{buildroot}/etc
install -p -m 644 %{SOURCE10} %{buildroot}/etc

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog TODO doc/asoundrc.txt
%config %{_sysconfdir}/asound.conf
/%{_lib}/libasound.so.*
%{_bindir}/aserver
%{_libdir}/alsa-lib/
%{_datadir}/alsa/

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen/
%{_includedir}/alsa/
%{_includedir}/sys/asoundlib.h
%{_libdir}/libasound.so
%exclude %{_libdir}/libasound.la
%{_libdir}/pkgconfig/alsa.pc
%{_datadir}/aclocal/alsa.m4

%changelog
* Fri Oct 28 2011 Liu Di <liudidi@gmail.com> - 1.0.24.1-1
- 升级到 1.0.24.1

