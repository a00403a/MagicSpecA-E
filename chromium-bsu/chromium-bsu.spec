Name:           chromium-bsu
Version:        0.9.15
Release:        1%{?dist}
Summary:        Fast paced, arcade-style, top-scrolling space shooter
Summary(zh_CN):	一个纵版射击游戏
Group:          Amusements/Games
Group(zh_CN): 	娱乐/游戏
License:        Artistic clarified
URL:            http://chromium-bsu.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        chromium-bsu-README.license
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  desktop-file-utils SDL-devel alsa-lib-devel libvorbis-devel
BuildRequires:  libpng-devel libglpng-devel ftgl-devel
BuildRequires:  openal-soft-devel freealut-devel >= 1.1.0-10
Requires:       hicolor-icon-theme

%description
You are captain of the cargo ship Chromium B.S.U., responsible for delivering
supplies to our troops on the front line. Your ship has a small fleet of
robotic fighters which you control from the relative safety of the Chromium
vessel. This is an OpenGL-based shoot 'em up game with fine graphics.

%description -l zh_CN
一个纵版射击游戏。

%prep
%setup -q
cp -a %{SOURCE1} README.license
iconv -f iso8859-1 -t utf8 NEWS -o NEWS.utf8
touch -r NEWS.utf8 NEWS
mv NEWS.utf8 NEWS


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cp -a AUTHORS README README.license COPYING NEWS \
  $RPM_BUILD_ROOT%{_docdir}/%{name}
# Put icon in the new fdo location
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps
mv $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_mandir}/man6/%{name}.6.gz


%changelog

