Name:		chromium-ffmpegsumo
Version:	14.0.827.10
Release:	1%{?dist}
Summary:	Media playback library for chromium

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://www.chromium.org/
# TODO: Document how I made the source for this beast from the chromium checkout
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	libvpx-devel, yasm
ExclusiveArch:	x86_64 %{ix86}

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

%install
%ifarch %{ix86}
make ARCH=ia32 install DESTDIR=%{buildroot} libdir=%{_libdir}  includedir=%{_includedir}
%endif

%ifarch x86_64
make ARCH=x64 install DESTDIR=%{buildroot} libdir=%{_libdir}  includedir=%{_includedir}
%endif

mkdir -p %{buildroot}%{_libdir}/chromium-browser/
pushd %{buildroot}%{_libdir}/chromium-browser/
ln -s ../libffmpegsumo.so.0.0.0 libffmpegsumo.so
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE COPYING.LGPLv2.1
%{_libdir}/libffmpegsumo.so.*
%{_libdir}/chromium-browser/libffmpegsumo.so

%files devel
%{_includedir}/ffmpegsumo/

%changelog
* Mon Jul 25 2011 Tom Callaway <spot@fedoraproject.org> - 14.0.827.10-1
- update to 14.0.827.10 forked tree

* Wed May 18 2011 Tom Callaway <spot@fedoraproject.org> - 11.0.696.68-1
- initial package
