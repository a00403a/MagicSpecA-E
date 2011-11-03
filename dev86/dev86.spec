Summary: A real mode 80x86 assembler and linker
Summary(zh_CN.UTF-8): 实模式 80x86 汇编器和链接器
Name: dev86
Version: 0.16.18
Release: 1%{?dist}
License: GPL+ and GPLv2+ and LGPLv2+
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
URL: http://homepage.ntlworld.com/robert.debath/
Source: http://homepage.ntlworld.com/robert.debath/dev86/Dev86src-%{version}.tar.gz
Patch0: dev86-noelks.patch
Patch1: dev86-64bit.patch
Patch2: dev86-nostrip.patch
Patch3: dev86-overflow.patch
Patch4: dev86-long.patch
Patch5: dev86-print-overflow.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: bin86

# don't try to strip binaries generated by dev86 unknown to /usr/bin/strip
%define __os_install_post    /usr/lib/rpm/redhat/brp-compress /usr/lib/rpm/redhat/brp-strip %{__strip} /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} %{nil}

%description
The dev86 package provides an assembler and linker for real mode 80x86
instructions. You'll need to have this package installed in order to
build programs that run in real mode, including LILO and the kernel's
bootstrapping code, from their sources.

You should install dev86 if you intend to build programs that run in real
mode from their source code.

%description -l zh_CN.UTF-8
实模式 80x86 汇编器和链接器，如果你要编译运行在实模式的程序需要安装它。
包括 LILO 和其它内核程序。

%prep
%setup -q
%patch0 -p1 -b .noelks
%if %{__isa_bits} == 64
%patch1 -p1 -b .64bit
%endif
%patch2 -p1 -b .nostrip
%patch3 -p1 -b .overflow
%patch4 -p1 -b .long
%patch5 -p1 -b .print-overflow

%build
# the main makefile doesn't allow parallel build
make bcc86 unproto copt as86 ld86 CFLAGS="$RPM_OPT_FLAGS"
make -C cpp CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}
make -C ar CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}
make -C ld CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}
# ncc doesn't support gcc optflags
make

%install
rm -rf ${RPM_BUILD_ROOT}

make	DIST=${RPM_BUILD_ROOT} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}/bcc \
	INCLDIR=%{_libdir}/bcc \
	LOCALPREFIX=%{_prefix} \
	install install-man

# preserve READMEs
for i in bootblocks copt dis88 unproto bin86 ; do cp $i/README README.$i ; done
cp bin86/README-0.4 README-0.4.bin86
cp bin86/ChangeLog ChangeLog.bin86
mv libc/COPYING COPYING.LGPL

pushd ${RPM_BUILD_ROOT}%{_bindir}
rm -f nm86 size86
ln -s objdump86 nm86
ln -s objdump86 size86
popd

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc README MAGIC Contributors README.bootblocks README.copt README.dis88
%doc README.unproto README-0.4.bin86 README.bin86 ChangeLog.bin86 COPYING
%doc COPYING.LGPL
%dir %{_libdir}/bcc
%{_bindir}/bcc
%{_bindir}/ar86
%{_bindir}/as86
%{_bindir}/ld86
%{_bindir}/objdump86
%{_bindir}/nm86
%{_bindir}/size86
%{_libdir}/bcc/*
%{_mandir}/man1/*

%changelog
* Thu Nov 03 2011 Liu Di <liudidi@gmail.com> - 0.16.18-1
- 更新到 0.16.18

