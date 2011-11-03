Name:           autotrace
Version:        0.31.1
Release:        22%{?dist}

Summary:        Utility for converting bitmaps to vector graphics
Summary(zh_CN.UTF-8):	转换位力到向量图形的工具

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
License:        GPLv2+ and LGPLv2+
URL:            http://autotrace.sourceforge.net/
Source0:        http://dl.sf.net/autotrace/autotrace-0.31.1.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ImageMagick-devel
BuildRequires:  libpng-devel > 1.2
BuildRequires:  libexif-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libxml2-devel
BuildRequires:  bzip2-devel
BuildRequires:  freetype-devel
#BuildRequires:  pstoedit-devel
BuildConflicts: pstoedit-devel

Patch0:         autotrace-0.31.1-GetOnePixel.patch

%description
AutoTrace is a program similar to CorelTrace or Adobe Streamline for
converting bitmaps to vector graphics.

Supported input formats include BMP, TGA, PNM, PPM, and any format
supported by ImageMagick, whereas output can be produced in
Postscript, SVG, xfig, SWF, and others.

%description -l zh_CN.UTF-8
转换位力到向量图形的工具。

%package devel
Summary:        Header files and static libraries for autotrace
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       ImageMagick-devel
#Requires:       pstoedit-devel


%description devel
This package contains header files and static libraries for autotrace.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
#%patch0 -p1 -b .GetOnePixel

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.LIB ChangeLog FAQ NEWS README THANKS TODO
%{_bindir}/autotrace
%{_libdir}/*.so.*
%{_mandir}/man[^3]/*

%files devel
%defattr(-,root,root,-)
%doc HACKING
%{_bindir}/autotrace-config
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/autotrace/
%{_datadir}/aclocal/*.m4


%changelog

