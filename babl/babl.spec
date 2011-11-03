Summary:	A dynamic, any to any, pixel format conversion library
Summary(zh_CN.UTF-8): 一个动态的，任何到任何，像素格式转换库
Name:		babl
Version:	0.1.4
Release:	2%{?dist}
# The gggl codes contained in this package are under the GPL, with exceptions allowing their use under libraries covered under the LGPL
License:	LGPLv3+ and GPLv3+
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://www.gegl.org/babl/
Source0:	ftp://ftp.gimp.org/pub/babl/0.1/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	librsvg2 w3m

%global develdocdir %{_docdir}/%{name}-devel-%{version}/html

%description
Babl is a dynamic, any to any, pixel format conversion library. It
provides conversions between the myriad of buffer types images can be
stored in. Babl doesn't only help with existing pixel formats, but also
facilitates creation of new and uncommon ones.

%description -l zh_CN.UTF-8
一个动态的，任何到任何，像素格式转换库。

%package devel
Summary:	Headers for developing programs that will use %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig
# Split off devel docs from 0.1.2-2 on
Obsoletes:	%{name}-devel < 0.1.2-2%{?dist}
Conflicts:	%{name}-devel < 0.1.2-2%{?dist}

%description devel
This package contains the libraries and header files needed for
developing with %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package devel-docs
Summary:	Documentation for developing programs that will use %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文档
Group:		Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:	noarch
Requires:	%{name}-devel = %{version}-%{release}
# Split off devel docs from 0.1.2-2 on
Obsoletes:	%{name}-devel < 0.1.2-2%{?dist}
Conflicts:	%{name}-devel < 0.1.2-2%{?dist}

%description devel-docs
This package contains documentation needed for developing with %{name}.

%description devel-docs -l zh_CN.UTF-8
%{name} 的开发文档。

%prep
%setup -q

%build
# use PIC/PIE because babl is likely to deal with data coming from untrusted
# sources
CFLAGS="-fPIC %optflags -fno-strict-aliasing"
LDFLAGS="-pie"
%configure --disable-static

make V=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install INSTALL='install -p'

mkdir -p "%{buildroot}/%{develdocdir}"
cp -pr docs/graphics docs/*.html docs/babl.css "%{buildroot}/%{develdocdir}"
rm -rf "%{buildroot}/%{develdocdir}"/graphics/Makefile*

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%check
make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING README NEWS
%{_libdir}/*.so.*
%{_libdir}/babl-0.1/

%files devel
%defattr(-, root, root, -)
%{_includedir}/babl-0.1/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
/usr/lib/girepository-1.0/Babl-0.1.typelib
/usr/share/gir-1.0/Babl-0.1.gir

%files devel-docs
%defattr(-, root, root, -)
%doc %{develdocdir}

%changelog

