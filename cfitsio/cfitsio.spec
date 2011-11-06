Name: cfitsio
Version: 3.280
Release: 1%{?dist}
Summary: Library for manipulating FITS data files
Summary(zh_CN.UTF-8): 处理 FITS 数据文件的库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License: GPLv2+
URL: http://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html
Source0: ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio3280.tar.gz
Patch: cfitsio.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:     gcc-gfortran
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%description
CFITSIO is a library of C and FORTRAN subroutines for reading and writing 
data files in FITS (Flexible Image Transport System) data format. CFITSIO 
simplifies the task of writing software that deals with FITS files by 
providing an easy to use set of high-level routines that insulate the 
programmer from the internal complexities of the FITS file format. At the 
same time, CFITSIO provides many advanced features that have made it the 
most widely used FITS file programming interface in the astronomical 
community.

%description -l zh_CN.UTF-8
处理 FITS 数据文件的库.

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Headers required when building programs against cfitsio
Summary(zh_CN.UTF-8): 用 cfitsio 编译程序所需的头文件
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Headers required when building a program against the cfitsio library.

%description devel -l zh_CN.UTF-8
用 cfitsio 编译程序所需的头文件.

%prep
%setup -q -n cfitsio
%patch -p1

%build
FC=f95
export FC
export CC=gcc # fixes -O*, -g
%configure
make shared %{?_smp_mflags}
unset FC

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
make LIBDIR=%{_libdir} INCLUDEDIR=%{_includedir} CFITSIO_LIB=%{buildroot}%{_libdir} \
     CFITSIO_INCLUDE=%{buildroot}%{_includedir} install
pushd %{buildroot}%{_libdir}
ln -s libcfitsio.so.0 libcfitsio.so
popd

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README License.txt changes.txt fitsio.doc fitsio.ps cfitsio.doc cfitsio.ps
%{_libdir}/libcfitsio.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}
%{_libdir}/libcfitsio.a
%{_libdir}/libcfitsio.so
%{_libdir}/pkgconfig/cfitsio.pc


%changelog
* Wed Jan 14 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.100-0.1mgc
- 更新至 3.100
- 戊子  十二月十九

* Fri Feb 8 2008 Ni Hui <shuizhuyuanluo@126.com> - 3.060-0.2mgc
- rebuild
- 修正头文件路径

* Sun Dec 23 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.060-0.1mgc
- rebuild for MagicLinux-2.1>=1107
