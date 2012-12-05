Summary: C++ library for scientific computing
Summary(zh_CN.UTF-8): 科学计算的 C++ 库
Name: blitz
Version: 0.9
Release: 2%{?dist}
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License: GPL
URL: http://oonumerics.org/blitz/
Source: %{name}-%{version}.tar.gz
Patch:	%{name}-gcc43.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}

%description
Blitz++ is a C++ class library for scientific computing which provides
performance on par with Fortran 77/90. It uses template techniques to
achieve high performance. The current versions provide dense arrays and
vectors, random number generators, and small vectors and matrices.

%package devel
Summary: Libraries, includes, etc. used to develop an application with %{name}
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
%description devel
This are the header files and libraries needed to develop a %{name}
application

%package doc
Summary: The Blitz html docs
Group: Documentation
Group(zh_CN.UTF-8): 文档
%description doc
HTML documentation files for the Blitz Library

%prep
%setup -q
%patch -p1

%build
%configure --enable-shared --disable-static --disable-fortran \
    --disable-dependency-tracking --disable-cxx-flags-preset
make %{?_smp_mflags}
# blitz.pc is created directly by configure
# I use sed to add %%libdir/blitz to the include directories of the library
# so that different bzconfig.h can be installed for different archs
%{__sed} -i -e "s/Cflags: -I\${includedir}/Cflags: -I\${includedir} -I\${libdir}\/blitz\/include/" blitz.pc

%install
rm -rf %{buildroot}
#一个奇怪的地方，暂时不知道怎么处理
mkdir -p %{buildroot}%{_docdir}/blitz-0.9/doxygen
mv doc/doxygen/html/search %{buildroot}%{_docdir}/blitz-0.9/doxygen
#
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_libdir}/blitz/include/blitz
mv %{buildroot}%{_includedir}/blitz/gnu %{buildroot}%{_libdir}/blitz/include/blitz
rm -rf doc/doxygen/html/installdox
# There are some empty files in doc, remove before copying in doc
(find -empty | xargs rm)
# Put in doc only the source code
rm -rf examples/.deps
rm -rf examples/Makefile*

magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS LEGAL COPYING README LICENSE
%{_libdir}/*so.*

%files devel
%defattr(-,root,root,-)
%doc AUTHORS LEGAL COPYING README LICENSE examples
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/blitz
%{_includedir}/*
%{_infodir}/%{name}*
%exclude %{_libdir}/*.la
%exclude %{_libdir}/pkgconfig/blitz-uninstalled.pc
%exclude %{_infodir}/dir

%files doc
%doc AUTHORS LEGAL COPYING README LICENSE
%defattr(-,root,root,-)
%doc doc/doxygen/html 

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.9-2
- 为 Magic 3.0 重建

* Sun Oct 14 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.9-0.1mgc
- first spec file
