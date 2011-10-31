%define git 1
%define git_date 20111030

Name:           arora
Version:        0.11.1
%if 0%{git}
Release:	0.git%{git_date}.%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        A cross platform web browser
Summary(zh_CN): 一个跨平台的网页浏览器

Group:          Applications/Internet
Group(zh_CN):	应用程序/互联网
License:        GPLv2+
URL:            http://code.google.com/p/arora/
%if 0%{git}
# git clone git://github.com/Arora/arora.git
Source0:	%{name}-git%{?git_date}.tar.xz
%else
Source0:        http://arora.googlecode.com/files/%{name}-%{version}.tar.gz
%endif
Source1:	make_git_package.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel >= 4.4.0
# for gnome default app path
BuildRequires:  control-center-devel


%description
Arora is a simple, cross platform web browser based on the QtWebKit engine.
Currently, Arora is still under development, but it already has support for
browsing and other common features such as web history and bookmarks.

%description -l zh_CN
Arora 是一个简单的，跨平台的网页浏览器，基于 QtWebKit 引擎。

%package gnome
Summary:        Better Gnome support for Arora
Summary(zh_CN): Arora 的更好 Gnome 支持
Group:          Applications/Internet
Group(zh_CN):   应用程序/互联网
Requires:       control-center
Requires:       arora

%description gnome
Adds Arora to Preferred Applications list in Gnome Control Center.

%description gnome -l zh_CN
Arora 的更好 Gnome 支持。

%prep
%if %{git_date}
%setup -q -n %{name}-git%{git_date}
%else
%setup -q
%endif

%build
qmake-qt4 PREFIX=%{_prefix}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make INSTALL_ROOT=$RPM_BUILD_ROOT install 

desktop-file-install --vendor fedora \
      --dir $RPM_BUILD_ROOT%{_datadir}/applications\
      --delete-original\
      $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS README ChangeLog
%doc LICENSE.GPL2 LICENSE.GPL3
%{_bindir}/arora
%{_bindir}/arora-placesimport
%{_bindir}/htmlToXBel
%{_bindir}/arora-cacheinfo
%{_datadir}/applications/fedora-%{name}.desktop    
%{_datadir}/icons/hicolor/128x128/apps/arora.png
%{_datadir}/icons/hicolor/16x16/apps/arora.png
%{_datadir}/icons/hicolor/32x32/apps/arora.png
%{_datadir}/icons/hicolor/scalable/apps/arora.svg
%{_datadir}/arora
%{_datadir}/pixmaps/arora.xpm
%{_datadir}/man/man1

%changelog

