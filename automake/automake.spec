%define api_version 1.11

Summary:    A GNU tool for automatically creating Makefiles
Summary(zh_CN.UTF-8): 一套自动建立 Makefile 的 GNU 工具
Name:       automake
Version:    %{api_version}.4
Release:    8%{?dist}
License:    GPLv2+ and GFDL
Group:      Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Source:     http://ftp.gnu.org/gnu/automake/automake-%{version}.tar.xz
Source1:    filter-provides-automake.sh
Source2:    filter-requires-automake.sh
URL:        http://sourceware.org/automake/
Requires:   autoconf >= 2.62
Buildrequires:  autoconf >= 2.62
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildArch:  noarch
Buildroot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# for better tests coverage:
# BuildRequires: libtool gettext-devel flex bison texinfo-tex texlive-dvips
# BuildRequires: gcc-java java-devel-openjdk gcc-gfortran /usr/bin/g77
# BuildRequires: dejagnu expect emacs imake python-docutils vala

# the filtering macros are currently in /etc/rpm/macros.perl:
# BuildRequires: perl-devel

%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE1}
%define __find_requires %{SOURCE2}

# remove bogus Automake perl dependencies and provides
# %{?perl_default_filter:
# %filter_from_provides /^perl(Automake::/d
# %filter_from_requires /^perl(Automake::/d
# %perl_default_filter
# }

%description
Automake is a tool for automatically generating `Makefile.in'
files compliant with the GNU Coding Standards.

You should install Automake if you are developing software and would
like to use its ability to automatically generate GNU standard
Makefiles.

%description -l zh_CN.UTF-8
Automake 是一套自动建立适应 GNU 代码标准的 “Makefile.in” 文件的工具。

如果你安装了 automake，你也需要安装 GNU 的 Autoconf 包。

%prep
%setup -q -n automake-%{version}

%build
./configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
   --bindir=%{_bindir} --datadir=%{_datadir} --libdir=%{_libdir} \
   --docdir=%{_docdir}/%{name}-%{version} PERL=/usr/bin/perl
make %{?_smp_mflags}
mv -f NEWS NEWS_
iconv -f ISO_8859-15 -t UTF-8 NEWS_ -o NEWS

%install
rm -rf ${RPM_BUILD_ROOT}

make install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

magic_rpm_clean.sh

%check
# make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/usr/sbin/install-info %{_infodir}/automake.info.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
    /usr/sbin/install-info --delete %{_infodir}/automake.info.gz %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS README THANKS
%{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/automake-%{api_version}
%{_datadir}/aclocal-%{api_version}
%{_mandir}/man1/*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.11.4-8
- 为 Magic 3.0 重建

* Fri Apr 13 2012 Liu Di <liudidi@gmail.com> - 1.11.4-7
- 为 Magic 3.0 重建

* Fri Apr 13 2012 Liu Di <liudidi@gmail.com> - 1.11.4-6
- 为 Magic 3.0 重建

* Fri Apr 13 2012 Liu Di <liudidi@gmail.com> - 1.11.4-5
- 为 Magic 3.0 重建

* Tue Nov 01 2011 Liu Di <liudidi@gmail.com> - 1.11.1-6
- 更新到 1.11.1

* Thu Jul 31 2008 Liu Di <liudidi@gmail.com> - 1.10.1-1mgc
- 更新到 1.10.1
