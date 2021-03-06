# Expected failures in mock, hangs in koji
%bcond_with tests
# The *.py files we ship are not python scripts, #813651
%global _python_bytecompile_errors_terminate_build 0

Name:           bash-completion
Version:        2.0
Release:        3%{?dist}
Epoch:          1
Summary:        Programmable completion for Bash

License:        GPLv2+
URL:            http://bash-completion.alioth.debian.org/
Source0:        http://bash-completion.alioth.debian.org/files/%{name}-%{version}.tar.bz2
Source2:        CHANGES.package.old
# https://bugzilla.redhat.com/677446, see also noblacklist patch
Source3:        %{name}-2.0-redefine_filedir.bash
# https://bugzilla.redhat.com/677446, see also redefine_filedir source
Patch0:         %{name}-1.99-noblacklist.patch

BuildArch:      noarch
%if %{with tests}
BuildRequires:  dejagnu
BuildRequires:  screen
BuildRequires:  tcllib
%endif
Requires:       bash >= 4.1

%description
bash-completion is a collection of shell functions that take advantage
of the programmable completion feature of bash.


%prep
%setup -q
%patch0 -p1
install -pm 644 %{SOURCE2} .


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Updated completion shipped in cowsay package:
rm $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/{cowsay,cowthink}

install -Dpm 644 %{SOURCE3} \
    $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/redefine_filedir


%if %{with tests}
%check
# For some tests involving non-ASCII filenames
export LANG=en_US.UTF-8
# This stuff borrowed from dejagnu-1.4.4-17 (tests need a terminal)
tmpfile=$(mktemp)
screen -D -m sh -c '( make check ; echo $? ) >'$tmpfile
cat $tmpfile
result=$(tail -n 1 $tmpfile)
rm -f $tmpfile
exit $result
%endif


%files
%doc AUTHORS CHANGES CHANGES.package.old COPYING README
# Temporarily not noreplace for < 1.90 to 1.90+ updates (changed location)
%config %{_sysconfdir}/profile.d/bash_completion.sh
%{_sysconfdir}/bash_completion.d/
%{_datadir}/bash-completion/
%{_datadir}/pkgconfig/bash-completion.pc


%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1:2.0-3
- 为 Magic 3.0 重建

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:2.0-1
- Update to 2.0 (fixes #817902, #831835).
- Don't try to python-bytecompile our non-python *.py (#813651).

* Sun Jan  8 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:1.99-1
- Update to 1.99.

* Fri Nov  4 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:1.90-1
- Update to 1.90.
- Specfile cleanups.
- Move pre-1.2 %%changelog entries to CHANGES.package.old.

* Mon Sep  5 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:1.3-6
- Apply upstream patch providing a config and profile hook to make it
  easier to disable bash-completion on per user basis.

* Mon Aug 15 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:1.3-5
- Fix ant completion when complete-ant-cmd.pl is N/A (#729771).
- Fix bash < 4 _filedir_xspec uppercase expansion issue (#726220).
- Drop _filedir_xspec self-parsing with bash >= 4 for speedups (#479936).
- Do install triggers with lua where available to speed up package install.
- Add completion for sum (#717341).

* Tue May 10 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:1.3-4
- Work around problems caused by Adobe Reader overriding _filedir (#677446).

* Tue Apr 12 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:1.3-3
- Patch to not test command availability for each snippet, improves load time.
- Apply upstream libreoffice flat XML extensions fix for #692548.
- Apply upstream MANPAGER fix for #689180.
- Apply upstream (la)tex *.dbj fix for #678122.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:1.3-1
- Update to 1.3.

* Wed Oct 13 2010 Ville Skyttä <ville.skytta@iki.fi> - 1:1.2-5
- Install util-linux completions unconditionally.
- Make trigger target package rename etc tracking easier to maintain, and
  handle man-db/man (#642193, Yanko Kaneti), mysql/MySQL-client-community,
  and tigervnc/vnc renames better.
- Move pre-1.0 %%changelog entries to CHANGES.package.old.

* Tue Oct  5 2010 Ville Skyttä <ville.skytta@iki.fi> - 1:1.2-4
- More IPv6 address completion fixes, #630658.

* Tue Sep 28 2010 Ville Skyttä <ville.skytta@iki.fi> - 1:1.2-3
- Apply upstream ~username completion fix for #628130.
- Apply upstream rpm completion improvements for #630328.
- Apply upstream IPv6 address completion fix for #630658.
- Drop some completions that are included in respective upstream packages.
- Fix qdbus/dcop uninstall trigger.

* Mon Jun 28 2010 Ville Skyttä <ville.skytta@iki.fi> - 1:1.2-2
- Apply upstream post 1.2 /etc/init.d/* completion improvements to fix #608351.

* Wed Jun 16 2010 Ville Skyttä <ville.skytta@iki.fi> - 1:1.2-1
- Update to 1.2, all patches applied upstream.
- Fixes #444469, #538433, #541423, and #601813, works around #585384.
