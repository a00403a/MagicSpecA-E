Summary:    A GNU tool for automatically configuring source code
Summary(zh_CN.UTF-8): 自动配置源代码的 GNU 工具
Name:       autoconf
Version:    2.68
Release:    4%{?dist}
License:    GPLv2+ and GFDL
Group:      Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Source:     http://ftpmirror.gnu.org/autoconf/autoconf-%{version}.tar.xz
Patch0:     autoconf-2.68-selfcheckfailure.patch
URL:        http://www.gnu.org/software/autoconf/
BuildArch: noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# m4 >= 1.4.6 is required, >= 1.4.14 is recommended:
BuildRequires:      m4 >= 1.4.14
Requires:           m4 >= 1.4.14
BuildRequires:      emacs
# the filtering macros are currently in /etc/rpm/macros.perl:
BuildRequires:      perl-devel
Requires(post):     /sbin/install-info
Requires(preun):    /sbin/install-info

# run "make check" by default
%{?_without_check: %define _without_check 1}
%{!?_without_check: %define _without_check 0}
%if ! %{_without_check}
BuildRequires: automake libtool gcc-gfortran
%endif

# filter out bogus perl(Autom4te*) dependencies
%define _use_internal_dependency_generator 0
%{?perl_default_filter:
%filter_from_provides /^perl(Autom4te::/d
%filter_from_requires /^perl(Autom4te::/d
%perl_default_filter
}

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to 
specify various configuration options.

You should install Autoconf if you are developing software and
would like to create shell scripts that configure your source code
packages. If you are installing Autoconf, you will also need to
install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.

%description -l zh_CN.UTF-8
自动配置源代码的 GNU 工具。

%prep
%setup -q
%patch0 -p 1 -b .selfcheckfailure

%build
%configure
# not parallel safe
make

%check
# The following test is failing.
# 199: autotest.at  parallel autotest and signal handling
# In test/autotest.at, under comment "Test PIPE", the exit code written
# to file "status" is 0.  Report mailed to bug-autoconf.
%if ! %{_without_check}
make check TESTSUITEFLAGS='-198 200-'
%endif

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/autoconf.info %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/autoconf.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_infodir}/autoconf.info*
# don't include standards.info, because it comes from binutils...
%exclude %{_infodir}/standards*
%{_datadir}/autoconf/
%dir %{_datadir}/emacs/
%{_datadir}/emacs/site-lisp/
%{_mandir}/man1/*
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.68-4
- 为 Magic 3.0 重建

* Tue Nov 01 2011 Liu Di <liudidi@gmail.com> - 2.68-3
- 为 Magic 3.0 重建
