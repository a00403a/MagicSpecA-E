Name: elfutils
Summary: A collection of utilities and DSOs to handle compiled objects
Version: 0.154
%global baserelease 3
URL: https://fedorahosted.org/elfutils/
%global source_url http://fedorahosted.org/releases/e/l/elfutils/%{version}/
License: GPLv3+ and (GPLv2+ or LGPLv3+)
Group: Development/Tools

%if %{?_with_compat:1}%{!?_with_compat:0}
%global compat 1
%else
%global compat 0
%endif

%global portability             0
%global scanf_has_m             1
%global separate_devel_static   1
%global use_zlib                1
%global use_xz                  1

%global nocheck true

%global depsuffix %{?_isa}%{!?_isa:-%{_arch}}

Source: %{?source_url}%{name}-%{version}.tar.bz2
Patch1: %{?source_url}elfutils-robustify.patch
Patch2: %{?source_url}elfutils-portability.patch
Patch3: elfutils-0.154-binutils-pr-ld-13621.patch
Patch4: elfutils-0.154-xlatetom-835877.patch

%if !%{compat}
Release: %{baserelease}%{?dist}
%else
Release: 0.%{baserelease}
%endif

Requires: elfutils-libelf%{depsuffix} = %{version}-%{release}
Requires: elfutils-libs%{depsuffix} = %{version}-%{release}

BuildRequires: gettext
BuildRequires: bison >= 1.875
BuildRequires: flex >= 2.5.4a
BuildRequires: bzip2
%if !%{compat}
BuildRequires: gcc >= 3.4
# Need <byteswap.h> that gives unsigned bswap_16 etc.
BuildRequires: glibc-headers >= 2.3.4-11
%else
BuildRequires: gcc >= 3.2
%endif

%if %{use_zlib}
BuildRequires: zlib-devel >= 1.2.2.3
BuildRequires: bzip2-devel
%endif

%if %{use_xz}
BuildRequires: xz-devel
%endif

%global _gnu %{nil}
%global _program_prefix eu-

%description
Elfutils is a collection of utilities, including ld (a linker),
nm (for listing symbols from object files), size (for listing the
section sizes of an object or archive file), strip (for discarding
symbols), readelf (to see the raw ELF file structures), and elflint
(to check for well-formed ELF files).


%package libs
Summary: Libraries to handle compiled objects
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-libs%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libelf%{depsuffix} = %{version}-%{release}

%description libs
The elfutils-libs package contains libraries which implement DWARF, ELF,
and machine-specific ELF handling.  These libraries are used by the programs
in the elfutils package.  The elfutils-devel package enables building
other programs using these libraries.

%package devel
Summary: Development libraries to handle compiled objects
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-devel%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libs%{depsuffix} = %{version}-%{release}
Requires: elfutils-libelf-devel%{depsuffix} = %{version}-%{release}
%if !%{separate_devel_static}
Requires: elfutils-devel-static%{depsuffix} = %{version}-%{release}
%endif

%description devel
The elfutils-devel package contains the libraries to create
applications for handling compiled objects.  libebl provides some
higher-level ELF access functionality.  libdw provides access to
the DWARF debugging information.  libasm provides a programmable
assembler interface.

%package devel-static
Summary: Static archives to handle compiled objects
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-devel-static%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-devel%{depsuffix} = %{version}-%{release}
Requires: elfutils-libelf-devel-static%{depsuffix} = %{version}-%{release}

%description devel-static
The elfutils-devel-static package contains the static archives
with the code to handle compiled objects.

%package libelf
Summary: Library to read and write ELF files
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-libelf%{depsuffix} = %{version}-%{release}
%endif
Obsoletes: libelf <= 0.8.2-2

%description libelf
The elfutils-libelf package provides a DSO which allows reading and
writing ELF files on a high level.  Third party programs depend on
this package to read internals of ELF files.  The programs of the
elfutils package use it also to generate new ELF files.

%package libelf-devel
Summary: Development support for libelf
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-libelf-devel%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libelf%{depsuffix} = %{version}-%{release}
%if !%{separate_devel_static}
Requires: elfutils-libelf-devel-static%{depsuffix} = %{version}-%{release}
%endif
Obsoletes: libelf-devel <= 0.8.2-2

%description libelf-devel
The elfutils-libelf-devel package contains the libraries to create
applications for handling compiled objects.  libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file.

%package libelf-devel-static
Summary: Static archive of libelf
Group: Development/Tools
License: GPLv2+ or LGPLv3+
%if 0%{!?_isa:1}
Provides: elfutils-libelf-devel-static%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libelf-devel%{depsuffix} = %{version}-%{release}

%description libelf-devel-static
The elfutils-libelf-static package contains the static archive
for libelf.

%prep
%setup -q

: 'compat=%compat'
: 'portability=%portability'
: 'separate_devel_static=%separate_devel_static'
: 'scanf_has_m=%scanf_has_m'

%patch1 -p1 -b .robustify

%if %{portability}
%patch2 -p1 -b .portability
sleep 1
find . \( -name Makefile.in -o -name aclocal.m4 \) -print | xargs touch
sleep 1
find . \( -name configure -o -name config.h.in \) -print | xargs touch
%else
%if !%{scanf_has_m}
sed -i.scanf-m -e 's/%m/%a/g' src/addr2line.c tests/line2addr.c
%endif
%endif

%patch3 -p1 -b .binutils-pr-ld-13621
%patch4 -p1 -b .xlatetom-835877

find . -name \*.sh ! -perm -0100 -print | xargs chmod +x

%build
# Remove -Wall from default flags.  The makefiles enable enough warnings
# themselves, and they use -Werror.  Appending -Wall defeats the cases where
# the makefiles disable some specific warnings for specific code.
RPM_OPT_FLAGS=${RPM_OPT_FLAGS/-Wall/}

%if %{compat}
# Some older glibc headers can run afoul of -Werror all by themselves.
# Disabling the fancy inlines avoids those problems.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D__NO_INLINE__"
COMPAT_CONFIG_FLAGS="--disable-werror"
%else
COMPAT_CONFIG_FLAGS=""
%endif

%configure $COMPAT_CONFIG_FLAGS CFLAGS="$RPM_OPT_FLAGS -fexceptions" || {
  cat config.log
  exit 2
}
make -s %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make -s install DESTDIR=${RPM_BUILD_ROOT}

chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/lib*.so*
chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/elfutils/lib*.so*

# XXX Nuke unpackaged files
(cd ${RPM_BUILD_ROOT}
 rm -f .%{_bindir}/eu-ld
)
magic_rpm_clean.sh
%find_lang %{name} || touch %{name}.lang

%check
make -s check || %{nocheck}

%clean
rm -rf ${RPM_BUILD_ROOT}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post libelf -p /sbin/ldconfig

%postun libelf -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING COPYING-GPLV2 COPYING-LGPLV3 README TODO CONTRIBUTING
%{_bindir}/eu-addr2line
%{_bindir}/eu-ar
%{_bindir}/eu-elfcmp
%{_bindir}/eu-elflint
%{_bindir}/eu-findtextrel
%{_bindir}/eu-nm
%{_bindir}/eu-objdump
%{_bindir}/eu-ranlib
%{_bindir}/eu-readelf
%{_bindir}/eu-size
%{_bindir}/eu-strings
%{_bindir}/eu-strip
#%%{_bindir}/eu-ld
%{_bindir}/eu-unstrip
%{_bindir}/eu-make-debug-archive

%files libs
%defattr(-,root,root)
%{_libdir}/libasm-%{version}.so
%{_libdir}/libasm.so.*
%{_libdir}/libdw-%{version}.so
%{_libdir}/libdw.so.*
%dir %{_libdir}/elfutils
%{_libdir}/elfutils/lib*.so

%files devel
%defattr(-,root,root)
%{_includedir}/dwarf.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/elf-knowledge.h
%{_includedir}/elfutils/libasm.h
%{_includedir}/elfutils/libebl.h
%{_includedir}/elfutils/libdw.h
%{_includedir}/elfutils/libdwfl.h
%{_includedir}/elfutils/version.h
%{_libdir}/libebl.a
%{_libdir}/libasm.so
%{_libdir}/libdw.so

%files devel-static
%defattr(-,root,root)
%{_libdir}/libasm.a
%{_libdir}/libdw.a

%files -f %{name}.lang libelf
%defattr(-,root,root)
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf.so.*

%files libelf-devel
%defattr(-,root,root)
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%{_libdir}/libelf.so

%files libelf-devel-static
%defattr(-,root,root)
%{_libdir}/libelf.a

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.154-3
- 为 Magic 3.0 重建


