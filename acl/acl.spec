Summary: Access control list utilities
Summary(zh_CN.UTF-8): 访问控制列表工具
Name: acl
Version: 2.2.51
Release: 3%{?dist}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gawk
BuildRequires: gettext
BuildRequires: libattr-devel
BuildRequires: libtool
Requires: libacl = %{version}-%{release}
Source: http://download.savannah.gnu.org/releases-noredirect/acl/acl-%{version}.src.tar.gz
Patch1: acl-2.2.39-build.patch

# prepare the test-suite for SELinux and arbitrary umask
Patch4: acl-2.2.49-tests.patch

# fix typos in setfacl(1) man page (#675451)
Patch6: acl-2.2.49-bz675451.patch

License: GPLv2+
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: http://acl.bestbits.at/

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%description -l zh_CN.UTF-8
这个包包含了处理访问控制列表需要的 getfacl 和 setfacl 工具。

%package -n libacl
Summary: Dynamic library for access control list support
Summary(zh_CN.UTF-8): %{name} 的动态库
License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libacl
This package contains the libacl.so dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%description -n libacl -l zh_CN.UTF-8
%{name} 的动态运行库。

%package -n libacl-devel
Summary: Access control list static libraries and headers
Summary(zh_CN.UTF-8): %{name} 的开发文件
License: LGPLv2+
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: libacl = %{version}-%{release}, libattr-devel

%description -n libacl-devel
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

%description -n libacl-devel -l zh_CN.UTF-8
%{name} 的开发文件。

%prep
%setup -q
%patch1 -p1
%patch4 -p1
%patch6 -p1

%build
touch .census
# acl abuses libexecdir
%configure --libdir=/%{_lib} --libexecdir=%{_libdir}

# uncomment to turn on optimizations
# sed -i 's/-O2/-O0/' libtool include/builddefs
# unset CFLAGS

make %{?_smp_mflags} LIBTOOL="libtool --tag=CC"

%check
if ./setfacl/setfacl -m u:`id -u`:rwx .; then
    make tests || exit $?
    if test 0 = `id -u`; then
        make root-tests || exit $?
    fi
else
    echo '*** ACLs are probably not supported by the file system,' \
         'the test-suite will NOT run ***'
fi

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-dev DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT

# get rid of libacl.a and libacl.la
rm -f $RPM_BUILD_ROOT/%{_lib}/libacl.a
rm -f $RPM_BUILD_ROOT/%{_lib}/libacl.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libacl.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libacl.la

# fix links to shared libs and permissions
rm -f $RPM_BUILD_ROOT%{_libdir}/libacl.so
ln -sf ../../%{_lib}/libacl.so $RPM_BUILD_ROOT/%{_libdir}/libacl.so
chmod 0755 $RPM_BUILD_ROOT/%{_lib}/libacl.so.*.*.*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libacl -p /sbin/ldconfig

%postun -n libacl -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/chacl
%{_bindir}/getfacl
%{_bindir}/setfacl
%{_datadir}/doc/acl-%{version}
%{_mandir}/man1/chacl.1*
%{_mandir}/man1/getfacl.1*
%{_mandir}/man1/setfacl.1*
%{_mandir}/man5/acl.5*

%files -n libacl-devel
%defattr(-,root,root,-)
/%{_lib}/libacl.so
%{_libdir}/libacl.so
%{_includedir}/acl
%{_includedir}/sys/acl.h
%{_mandir}/man3/acl_*

%files -n libacl
%defattr(-,root,root,-)
/%{_lib}/libacl.so.*

%changelog
* Thu Oct 27 2011 Liu Di <liudidi@gmail.com> - 2.2.51-3
- 为 Magic 3.0 重建