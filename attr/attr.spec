Summary: Utilities for managing filesystem extended attributes
Summary(zh_CN.UTF-8): 处理文件系统扩展属性的工具
Name: attr
Version: 2.4.46
Release: 3%{?dist}
Conflicts: xfsdump < 2.0.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source: http://download.savannah.gnu.org/releases-noredirect/attr/attr-%{version}.src.tar.gz

# make it ready for rpmbuild
Patch1: attr-2.4.32-build.patch

# prepare the test-suite for SELinux
Patch3: attr-2.4.44-tests.patch

# silence compile-time warnings
Patch4: attr-2.4.44-warnings.patch

# getfattr: return non-zero exit code on failure (#660619)
Patch7: attr-2.4.44-bz660619.patch

# walk_tree: do not follow symlink to directory with -h (#660613)
Patch8: attr-2.4.44-bz660613.patch

# fix typos in attr(1) man page (#669095)
Patch9: attr-2.4.44-bz669095.patch

License: GPLv2+
URL: http://acl.bestbits.at/
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
BuildRequires: gettext
BuildRequires: libtool
Requires: libattr = %{version}-%{release}

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%description -l zh_CN.UTF-8
一组处理文件系统扩展属性的工具。

%package -n libattr
Summary: Dynamic library for extended attribute support
Summary(zh_CN.UTF-8): %{name} 的动态链接库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: LGPLv2+

%description -n libattr
This package contains the libattr.so dynamic library which contains
the extended attribute system calls and library functions.

%description -n libattr -l zh_CN.UTF-8
%{name} 的动态链接库。

%package -n libattr-devel
Summary: Extended attribute static libraries and headers
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License: LGPLv2+
Requires: libattr = %{version}-%{release}

%description -n libattr-devel
This package contains the libraries and header files needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

Currently only ext2, ext3 and XFS support extended attributes.
The SGI IRIX compatibility API built above the Linux system calls is
used by programs such as xfsdump(8), xfsrestore(8) and xfs_fsr(8).

You should install libattr-devel if you want to develop programs
which make use of extended attributes.  If you install libattr-devel,
you'll also want to install attr.

%description -n libattr-devel -l zh_CN.UTF-8
lib%{name} 的开发包。

%prep
%setup -q
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
# attr abuses libexecdir
%configure --libdir=/%{_lib} --libexecdir=%{_libdir}

# uncomment to turn on optimizations
# sed -i 's/-O2/-O0/' libtool include/builddefs
# unset CFLAGS

make %{?_smp_mflags} LIBTOOL="libtool --tag=CC"

%check
if ./setfattr/setfattr -n user.name -v value .; then
    make tests || exit $?

    # FIXME: root-tests are not ready for the SELinux
    #if test 0 = `id -u`; then
    #    make root-tests || exit $?
    #fi
else
    echo '*** xattrs are probably not supported by the file system,' \
         'the test-suite will NOT run ***'
fi

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-dev DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT

# get rid of libattr.a and libattr.la
rm -f $RPM_BUILD_ROOT/%{_lib}/libattr.a
rm -f $RPM_BUILD_ROOT/%{_lib}/libattr.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libattr.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libattr.la

# fix links to shared libs and permissions
rm -f $RPM_BUILD_ROOT%{_libdir}/libattr.so
ln -sf ../../%{_lib}/libattr.so $RPM_BUILD_ROOT/%{_libdir}/libattr.so
chmod 0755 $RPM_BUILD_ROOT/%{_lib}/libattr.so.*.*.*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libattr -p /sbin/ldconfig

%postun -n libattr -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc doc
%{_bindir}/attr
%{_bindir}/getfattr
%{_bindir}/setfattr
%{_mandir}/man1/attr.1*
%{_mandir}/man1/getfattr.1*
%{_mandir}/man1/setfattr.1*
%{_mandir}/man5/attr.5*

%files -n libattr-devel
%defattr(-,root,root,-)
/%{_lib}/libattr.so
%{_libdir}/libattr.so
%{_includedir}/attr
%{_mandir}/man2/*attr.2*
%{_mandir}/man3/attr_*.3.*

%files -n libattr
%defattr(-,root,root,-)
/%{_lib}/libattr.so.*

%changelog
* Tue Nov 01 2011 Liu Di <liudidi@gmail.com> - 2.4.26-3
- 为 Magic 3.0 重建　

