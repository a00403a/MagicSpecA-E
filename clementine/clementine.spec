#先使用内置的依赖库
%define use_external_dependence 0

%define _unpackaged_files_terminate_build	0

Name:           clementine
Version:        1.1.1
Release:        3%{?dist}
Summary:        A music player and library organiser
Summary(zh_CN.UTF-8):	一个音乐播放器和曲库管理工具

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
License:        GPLv3 and GPLv2+
URL:            http://code.google.com/p/clementine-player
Source0:        http://clementine-player.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:		clementine-0.3-no3rd.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  liblastfm-devel
BuildRequires:  taglib-devel
BuildRequires:  xine-lib-devel
BuildRequires:  libnotify-devel
BuildRequires:  qt4-devel
BuildRequires:  boost-devel
BuildRequires:  notification-daemon
BuildRequires:  cmake
BuildRequires:  sqlite-devel
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-compiler

%if %{use_external_dependence}
BuildRequires:  qtsingleapplication-devel
BuildRequires:  libqxt-devel
BuildRequires:  gtest-devel
%endif

%description
Clementine is a modern music player and library organiser.
It is largely a port of Amarok 1.4, with some features rewritten to take
advantage of Qt4.

%description -l zh_CN.UTF-8
Clementine 是一个新潮的音乐播放器和曲库管理工具。它大体上是
Amarok 1.4 的一个移植版，捎带一些特性的重写以便得益于Qt4。

%prep
%setup -q
#%patch0 -p1 -R -b .no3rd
#%patch0 -p1 -b .no-external-lib
#%patch1 -p1 -b .static

%if %{use_external_dependence}
# We already don't use these but just to make sure
rm -fr 3rdparty
%endif

# Don't build tests. They require gmock which is not available on MagicLinux
sed -i '/tests/d' CMakeLists.txt


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
make #%{?_smp_mflags}
popd

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}

%check
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changelog COPYING
%{_bindir}/clementine
%{_datadir}/applications/clementine.desktop
#%{_datadir}/clementine/projectm-presets/*
%{_datadir}/icons/hicolor/*/apps/application-x-clementine.*
%{_bindir}/clementine-spotifyblob
%{_bindir}/clementine-tagreader
%{kde4_servicesdir}/clementine-*.protocol

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.1.1-2
- 为 Magic 3.0 重建

* Mon Nov 07 2011 Liu Di <liudidi@gmail.coM> - 0.7.1-1
- 更新到 0.7.1

* Sun May 30 2010 Liu Songhe <athena_star {at} 163 {dot} com> - 0.3-0.1
- Port to magic linux 2.5

* Sat Apr 17 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.2-2
- Patch out the external libraries
- Build the libclementine_lib into the final executable

* Sat Mar 27 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.2-1
- Fedorized the upstream specfile

* Mon Mar 22 2010 David Sansome <me@davidsansome.com> - 0.2
- Version 0.2

* Sun Feb 21 2010 David Sansome <me@davidsansome.com> - 0.1-5
- Various last-minute bugfixes

* Sun Jan 17 2010 David Sansome <me@davidsansome.com> - 0.1-1
- Initial package
