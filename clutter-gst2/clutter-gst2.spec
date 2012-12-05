Name:           clutter-gst2
Version:        1.9.92
Release:        2%{?dist}
Summary:        GStreamer integration for Clutter

License:        LGPLv2+
URL:            http://www.clutter-project.org
Source0:        http://ftp.gnome.org/pub/GNOME/sources/clutter-gst/1.9/clutter-gst-%{version}.tar.xz

BuildRequires:  clutter-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel

%description
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces.

Clutter GStreamer enables the use of GStreamer with Clutter.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces.

Clutter GStreamer enables the use of GStreamer with Clutter.

The %{name}-devel package contains libraries and header files for
developing applications that use clutter-gst API version 2.0.

%prep
%setup -q -n clutter-gst-%{version}

%build
%configure
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Remove the documentation for now as it conflicts with the files in
# clutter-gst-devel. I'll work with upstream to fix this properly.
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc/
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README
%{_libdir}/girepository-1.0/ClutterGst-2.0.typelib
%{_libdir}/gstreamer-1.0/libgstclutter.so
%{_libdir}/libclutter-gst-2.0.so.*

%files devel
%{_includedir}/clutter-gst-2.0/
%{_libdir}/libclutter-gst-2.0.so
%{_libdir}/pkgconfig/clutter-gst-2.0.pc
%{_datadir}/gir-1.0/ClutterGst-2.0.gir
#doc #{_datadir}/gtk-doc/

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.9.92-2
- 为 Magic 3.0 重建

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.92-1
- Update to 1.9.92

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.90-2
- Rebuilt with gstreamer1 0.11.99

* Wed Aug 29 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.90-1
- Initial clutter-gst2 packaging, based on Fedora clutter-gst (#852778)
