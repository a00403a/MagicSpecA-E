# Compile options:
# --with mp3          : enable mp3 support

%define tartopdir audacity-src-%{version}-beta
%define realname audacity

Name: audacity
Version: 1.3.13
Release: 0.1%{?dist}
Summary: Multitrack audio editor
Summary(zh_CN): 多轨音频编辑器 
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
License: GPLv2
URL: http://audacity.sourceforge.net

Source0: http://audacity.googlecode.com/files/audacity-minsrc-%{version}-beta.tar.bz2
# 手册没有版本
Source1: http://manual.audacityteam.org/help.zip

Patch1: audacity-1.3.7-libmp3lame-default.patch
Patch2: audacity-1.3.9-libdir.patch
Patch3: audacity-1.3.13-ffmpeg.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: alsa-lib-devel
BuildRequires: desktop-file-utils
BuildRequires: expat-devel
BuildRequires: flac-devel
BuildRequires: gettext
BuildRequires: ladspa-devel
BuildRequires: libid3tag-devel
BuildRequires: taglib-devel
BuildRequires: libogg-devel
BuildRequires: libsamplerate-devel
BuildRequires: libsndfile-devel
BuildRequires: libvorbis-devel
BuildRequires: soundtouch-devel
BuildRequires: vamp-plugin-sdk-devel >= 2.0
BuildRequires: zip
BuildRequires: zlib-devel
BuildRequires: wx-gtk2-unicode-devel
BuildRequires: libmad-devel
BuildRequires: ffmpeg-devel


%description
Audacity is a cross-platform multitrack audio editor. It allows you to
record sounds directly or to import files in various formats. It features
a few simple effects, all of the editing features you should need, and
unlimited undo. The GUI was built with wxWidgets and the audio I/O
supports OSS and ALSA under Linux.

%description -l zh_CN
%name 是一个跨平台的多轨音频编辑器，它允许你直接录音或导入多种格式的文件。

%package manual
Summary: manual for Audacity - offline install
Summary(zh_CN.UTF-8): %{name} 的离线手册

Group: Documentation
Group(zh_CN.UTF-8): 文档
# -manual suits either audacity or audacity-freeworld; both create the path:
Requires: /usr/bin/audacity


%description manual
Audacity Manual can be installed locally if preferred, or accessed on-line
if internet connection is available.
For the most up to date manual content, use the on-line manual.

%description manual -l zh_CN.UTF-8
%{name} 的手册。

%prep
%setup -q -n %{tartopdir}

%patch3 -p1

# Substitute hardcoded library paths.
%patch1 -p1
%patch2 -p1
for i in src/effects/ladspa/LoadLadspa.cpp src/AudacityApp.cpp
do
    sed -i -e 's!__RPM_LIBDIR__!%{_libdir}!g' $i
    sed -i -e 's!__RPM_LIB__!%{_lib}!g' $i
done
grep -q -s __RPM_LIB * -R && exit 1

# Substitute occurences of "libmp3lame.so" with "libmp3lame.so.0".
for i in locale/*.po src/export/ExportMP3.cpp
do
    sed -i -e 's!libmp3lame.so\([^.]\)!libmp3lame.so.0\1!g' $i
done


%build
%configure \
    --with-help \
    --with-libsndfile=system \
    --without-libresample \
    --with-libsamplerate=system \
    --with-libflac=system \
    --with-ladspa \
    --with-vorbis=system \
    --with-id3tag=system \
    --with-expat=system \
    --with-soundtouch=system \
    --with-ffmpeg=system \
    --with-libmad=system
# _smp_mflags cause problems
make


%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/pixmaps

make DESTDIR=${RPM_BUILD_ROOT} install

# audacity manual must be unzipped to correct location
unzip %{SOURCE1} -d $RPM_BUILD_ROOT%{_datadir}/%{realname}/help

magic_rpm_clean.sh
%{find_lang} %{realname}

#暂不需要
#rm -f $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop
#desktop-file-install \
#    --vendor fedora \
#    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
#    %{SOURCE2}


%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir} 

%post
umask 022
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :


%postun
umask 022
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_mandir}/man*/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/*.*
%{_datadir}/mime/packages/*
%doc %{_datadir}/doc/*

%files manual
%{_datadir}/%{realname}/help/

%changelog

