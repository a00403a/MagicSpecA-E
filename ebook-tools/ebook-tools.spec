Summary: Tools for accessing and converting various ebook file formats
Summary(zh_CN.UTF-8): 访问和转换多种 ebook 文件格式的工具
Name: ebook-tools
Version: 0.2.1
Release: 3%{?dist}
URL: http://ebook-tools.sourceforge.net/
License: The MIT License
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Source: http://downloads.sourceforge.net/project/ebook-tools/ebook-tools/%{version}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

BuildRequires: cmake >= 2.4.7
BuildRequires: libzip-devel
BuildRequires: libxml2-devel
BuildRequires: zip

Requires: clit
Requires: libzip
Requires: libxml2
Requires: zip

Provides: libepub

%description
Tools for accessing and converting various ebook file formats.

%description -l zh_CN.UTF-8
访问和转换多种 ebook 文件格式的工具。

%package devel
Summary: Support files necessary to compile applications with libepub
Summary(zh_CN.UTF-8): 使用 libepub 编译应用程序的支持文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: ebook-tools = %{version}-%{release}
Provides: libepub-devel

%description devel
Libraries, headers, and support files necessary to compile applications using libepub.

%description devel -l zh_CN.UTF-8
使用 libepub 编译应用程序的库、头文件和支持文件。

%prep
%setup -q -n %{name}-%{version}

%build
mkdir build
cd build
export CFLAGS=$RPM_OPT_FLAGS
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_BUILD_TYPE=debug \
	-DCMAKE_CXX_FLAGS_DEBUG:STRING="$RPM_OPT_FLAGS" \
	-DLIB_INSTALL_DIR=%{_libdir} ..

make %{?_smp_mflags}

%install
cd build
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%doc README TODO
%{_bindir}/*
%{_libdir}/libepub.so.*

%files devel
%{_includedir}/*
%{_libdir}/libepub.so

%changelog
* Wed Jan 14 2009 Ni Hui <shuizhuyuanluo@126.com> - 0.1.1-0.1mgc
- 更新至 0.1.1
- 戊子  十二月十九

* Fri Apr 18 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.1.0-0.1mgc
- Initial package
