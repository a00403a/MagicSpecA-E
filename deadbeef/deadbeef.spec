Name: deadbeef
Version: 0.5.6
Release: 1%{?dist}

Summary: mp3/ogg/flac/sid/mod/nsf music player based on GTK2
Summary(zh_CN): 基于 GTK2 的音乐播放器
License: GPLv2+
Group: Applications/Multimedia
Group(zh_CN): 应用程序/多媒体
Url: http://deadbeef.sourceforge.net/

Source0: http://downloads.sourceforge.net/project/deadbeef/%name-%version.tar.bz2

BuildRequires: gcc-c++ alsa-lib-devel libcurl-devel flac-devel gtk2-devel libmad-devel libsamplerate-devel libsndfile-devel libvorbis-devel wavpack-devel

%description
mp3/ogg/flac/sid/mod/nsf music player based on GTK2.

%description -l zh_CN
基于 GTK2 的音乐播放器.

%prep
%setup -q
#临时性的
sed -i 's/CODEC_TYPE/AVMEDIA_TYPE/g' plugins/ffmpeg/ffmpeg.c

%build
%configure \
  --disable-static
%{__make} %{?_smp_mflags}

%install
%makeinstall
magic_rpm_clean.sh
rm %{buildroot}%{_libdir}/deadbeef/*.la

%files
%_bindir/*
%dir %_libdir/deadbeef
%_libdir/deadbeef/*.so*
%_libdir/deadbeef/convpresets/*
%dir %_datadir/deadbeef
%_datadir/deadbeef/
%_datadir/applications/deadbeef.desktop
%_datadir/icons/hicolor/*/apps/deadbeef.*
%_includedir/deadbeef/*.h
%_docdir/*
%_datadir/locale/*

%changelog

