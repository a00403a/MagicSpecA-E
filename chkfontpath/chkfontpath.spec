Summary: Simple interface for editing the font path for the X font server.
Summary(zh_CN.UTF-8): 为X字体服务编辑字体路径的简单接口。
Name: chkfontpath
Version: 1.10.1
Release: 3%{?dist}
License: GPL
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
BuildRoot: %{_tmppath}/%{name}-%{version}-root
# Canonical CVS repository for in house upstream chkfontpath:
#       cvs -d :ext:elvis.redhat.com:/usr/local/CVS co chkfontpath
Source: %{name}-%{version}.tar.gz

# Do not add Requires on XFree86-* or xorg-x11-* subpackages, because that
# makes this package unnecessarily dependant on a specific X11
# implementation.  Instead, use a virtual Requires, or depend on a file or
# directory which will be present in one of the X11 implementation's file
# lists, thus avoiding the problem.  See bugzilla #118469 for details.
Requires: xfs
Requires: /sbin/pidof

%description 
This is a simple command line utility for configuring the directories
in the X font server's path.  It is mostly intended to be used
'internally' by RPM when packages with fonts are added or removed, but
it may be useful as a stand-alone utility in some instances.

%description -l zh_CN.UTF-8
这是一个配置X字体服务路径目录的简单命令行工具。它大多数时候是做为RPM
包里添加或删除字体的时候用的，不过也可以做为单独的工具使用。

%prep
%setup -q

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
make INSTROOT=$RPM_BUILD_ROOT BINDIR=%{_sbindir} MANDIR=%{_mandir} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Thu Oct 05 2006 Liu Di <liudidi@gmail.com> - 1.10.1-1mgc
- update to 1.10.1

* Mon Jul 25 2005 KanKer <kanker@163.com>
- rebuild 

* Fri Feb 11 2005 Mike A. Harris <mharris@redhat.com> 1.10.0-4
- Rebuilt with gcc 4 for FC4

* Fri Feb 11 2005 Mike A. Harris <mharris@redhat.com> 1.10.0-3
- Rebuilt for FC4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 1.10.0-2
- rebuilt

* Tue Mar 16 2004 Mike A. Harris <mharris@redhat.com> 1.10.0-1
- Change PreReq: XFree86-xfs to Requires: xfs, which is a virtual Provide
  that is present in the xorg-x11 packaging, and in XFree86-4.3.0-64 and
  later builds.  This is necessary in order to make packages not require a
  specific X11 implementation unnecessarily.  (#118469)

* Wed May 28 2003 Mike A. Harris <mharris@redhat.com> 1.9.10-1
- Add patch from Uli, with some cosmetic cleanups to fix bug (#90942)

* Tue May 20 2003 Bill Nottingham <notting@redhat.com> 1.9.9-1
- don't forcibly strip binaries on make install

* Fri May 16 2003 Mike A. Harris <mharris@redhat.com> 1.9.8-1
- Fix serious problem where chkfontpath sends SIGUSR1 to PID 2 bug (#90999)
- Replace hard coded xfs config file paths with constants
- Implemented fatalerror() for displaying variadic error messages and bailing
  with EXIT_FAILURE when "quiet" mode is not enabled, or silencing error
  output and exiting with EXIT_SUCCESS when "quiet" mode is enabled.  Replaced
  all conditionalized tests for quiet mode throughout the code, and changed
  all critical error messages with calls to fatalerror()
- Make restartXfs() more robust, with a fallback for if /proc isn't available.

* Mon Feb 10 2003 Mike A. Harris <mharris@redhat.com> 1.9.7-1
- Bump and rebuild in new environment as 1.9.7-1
- Fixes for GNU extension usage isblank()

* Tue May 21 2002 Mike A. Harris <mharris@redhat.com> 1.9.6-1
- Bump and rebuild in new environment as 1.9.6-1

* Thu Jan 18 2001 Preston Brown <pbrown@redhat.com>
- document missing arguments (#24055) in man page
- use popt to generate help text for the program

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- #ifdef out some debugging code (#24054)
- do a setlocale() before using ctype functions

* Fri Jan 12 2001 Preston Brown <pbrown@redhat.com>
- fixed up handling of catalogue line in situations where there is no
  path listed on the first line (#10128)
- fixed up handling when adding a directory to empty font path (#11108)
- use fputs where more correct (#14286)

* Tue Jul  4 2000 Matt Wilson <msw@redhat.com>
- Prereq: XFree86-xfs to insure that it gets installed before
  chkfontpath is.  This should promote XFree86-xfs to be installed
  before any package that has a Prereq: on chkfontpath
- Prereq: /sbin/pidof (even though a Requires: should be sufficient)

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- FHS macros

* Wed May 17 2000 Matt Wilson <msw@redhat.com>
- rebuilt to get rid of broken deps

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man page, update description.

* Mon Oct 18 1999 Preston Brown <pbrown@redhat.com>
- patches from JJ understand :unscaled automatically, no longer necessary
  to specify manually on the cmd line
- tries to keep specific font groups together much harder.

* Mon Sep 27 1999 Preston Brown <pbrown@redhat.com>
- incorporated patches to deal with :unscaled font dir entries, and
  add a --first flag to add the path at the beginning instead of the end.
- minor cleanups

* Fri Aug 15 1999 Preston Brown <pbrown@redhat.com>
- fixed up basename
- default to list, not help
- if trailing slash '/' is appended to paths given, strip it off

* Wed Apr 14 1999 Preston Brown <pbrown@redhat.com>
- preserve permissions on config file

* Thu Apr 07 1999 Preston Brown <pbrown@redhat.com>
- if /proc isn't mounted, don't do a killall

* Tue Mar 30 1999 Preston Brown <pbrown@redhat.com>
- don't use psmisc, use pidof from SysVinit

* Fri Mar 12 1999 Preston Brown <pbrown@redhat.com>
- made psmisc a requirement.

* Tue Mar 09 1999 Preston Brown <pbrown@redhat.com>
- added "quiet" option.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- injected new group / description.

* Tue Feb 16 1999 Preston Brown <pbrown@redhat.com>
- important fix - kill font server with USR1 instead of HUP.

* Mon Feb 15 1999 Preston Brown <pbrown@redhat.com>
- initial spec file
