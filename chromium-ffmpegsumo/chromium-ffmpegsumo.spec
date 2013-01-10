Name:		chromium-ffmpegsumo
Version:	23.0.1271.95
Release:	1%{?dist}
Summary:	Media playback library for chromium

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://www.chromium.org/
# TODO: Document how I made the source for this beast from the chromium checkout
Source0:	%{name}-%{version}.tar.bz2
%ifarch %{ix86} x86_64
BuildRequires:	yasm
%endif
BuildRequires:	libvpx-devel
ExclusiveArch:	x86_64 %{ix86} %{arm}

%description
A media playback library for chromium. This is a fork of ffmpeg.
Because Google doesn't understand open source community involvement.
It only supports unencumbered codecs.

%package devel
Group:		Development/Libraries
Summary:	Development headers and libraries for ffmpegsumo
Requires:	%{name} = %{version}-%{release}

%description devel
Development headers and	libraries for ffmpegsumo.

%prep
%setup -q

%build
%ifarch %{ix86}
make ARCH=ia32 OPTFLAGS="%{optflags}" libdir=%{_libdir} includedir=%{_includedir}
%endif

%ifarch x86_64
make ARCH=x64 OPTFLAGS="%{optflags}" libdir=%{_libdir}	includedir=%{_includedir}
%endif

%ifarch %{arm}
make ARCH=arm OPTFLAGS="%{optflags}" libdir=%{_libdir}  includedir=%{_includedir}
%endif

%install
%ifarch %{ix86}
make ARCH=ia32 install DESTDIR=%{buildroot} libdir=%{_libdir}  includedir=%{_includedir}
%endif

%ifarch x86_64
make ARCH=x64 install DESTDIR=%{buildroot} libdir=%{_libdir}  includedir=%{_includedir}
%endif

%ifarch	%{arm}
make ARCH=arm install DESTDIR=%{buildroot} libdir=%{_libdir}  includedir=%{_includedir}
%endif

mkdir -p %{buildroot}%{_libdir}/chromium-browser/
pushd %{buildroot}%{_libdir}/chromium-browser/
ln -s ../libffmpegsumo.so.0.0.0 libffmpegsumo.so
popd

# HACK
cp -a config/libavutil/avconfig.h %{buildroot}%{_includedir}/ffmpegsumo/libavutil/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE COPYING.LGPLv2.1
%{_libdir}/libffmpegsumo.so.*
%{_libdir}/chromium-browser/libffmpegsumo.so

%files devel
%{_includedir}/ffmpegsumo/

%changelog
* Thu Dec 13 2012 Tom Callaway <spot@fedoraproject.org> - 23.0.1271.95
- resync with chromium 23.0.1271.95

* Tue Aug 28 2012 Tom Callaway <spot@fedoraproject.org> - 21.0.1180.81-1
- sync with chromium 21.0.1180.81

* Thu Jun 14 2012 Tom Callaway <spot@fedoraproject.org> - 19.0.1084.56-2
- include config header

* Tue Jun 12 2012 Tom Callaway <spot@fedoraproject.org> - 19.0.1084.56-1
- update to 19.0.1084.56 forked tree

* Mon Feb 13 2012 Tom Callaway <spot@fedoraproject.org> - 17.0.963.46-1
- update to 17.0.963.46 forked tree

* Sat Feb  4 2012 Tom Callaway <spot@fedoraproject.org> - 14.0.827.10-2
- rebuild for newer libvpx

* Mon Jul 25 2011 Tom Callaway <spot@fedoraproject.org> - 14.0.827.10-1
- update to 14.0.827.10 forked tree

* Wed May 18 2011 Tom Callaway <spot@fedoraproject.org> - 11.0.696.68-1
- initial package
