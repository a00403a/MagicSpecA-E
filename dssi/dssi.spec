Summary:      Disposable Soft Synth Interface
Name:         dssi
Version:      1.1.1
Release:      1%{?dist}
License:      MIT
Group:        Applications/Multimedia
URL:          http://dssi.sourceforge.net/
Source0:      http://download.sf.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:      http://download.sf.net/sourceforge/%{name}/README
# Fix 64bit plugin path
# http://sourceforge.net/tracker/?func=detail&aid=2798711&group_id=104230&atid=637350
Patch1:       dssi-lib64.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: alsa-lib-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: ladspa-devel
BuildRequires: liblo-devel
BuildRequires: libsamplerate-devel
BuildRequires: libsndfile-devel
# for the examples
BuildRequires: qt4-devel

%description
Disposable Soft Synth Interface (DSSI, pronounced "dizzy") is a proposal for a
plugin API for software instruments (soft synths) with user interfaces,
permitting them to be hosted in-process by Linux audio applications. Think of
it as LADSPA-for-instruments, or something comparable to a simpler version of
VSTi.

%package examples
Summary:  DSSI plugin examples
Group:    Applications/Multimedia
License:  Public Domain
Requires: %{name} = %{version}

%description examples
Example plugins for the Disposable Soft Synth Interface.

%package devel
Summary:  Libraries, includes, etc to develop DSSI applications
Group:    Development/Libraries
License:  LGPLv2+
Requires: alsa-lib-devel
Requires: ladspa-devel
Requires: pkgconfig

%description devel
Libraries, include files, etc you can use to develop DSSI based applications.

%prep
%setup -q
%patch1 -p1

cp -a %{SOURCE1} README.%{version}

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/dssi/*.la

%check
# Build and run the tests
make -C tests controller
tests/controller

%files
%defattr(-,root,root,-)
%doc README* ChangeLog doc/TODO
%{_bindir}/dssi_osc_send
%{_bindir}/dssi_osc_update
%{_bindir}/jack-dssi-host
%{_bindir}/dssi_analyse_plugin
%{_bindir}//dssi_list_plugins
%dir %{_libdir}/dssi
%{_mandir}/man1/*

%files examples
%defattr(-,root,root,-)
%{_libdir}/dssi/less_trivial_synth.so
%{_libdir}/dssi/less_trivial_synth
%{_libdir}/dssi/trivial_sampler.so
%{_libdir}/dssi/trivial_sampler
%{_libdir}/dssi/trivial_synth.so
%{_libdir}/dssi/karplong.so
%{_bindir}/trivial_sampler
%{_bindir}/trivial_synth
%{_bindir}/less_trivial_synth
%{_bindir}/karplong

%files devel
%defattr(-,root,root,-)
%doc doc/*.txt COPYING
%{_includedir}/dssi.h
%{_libdir}/pkgconfig/dssi.pc

%changelog
* Sat Oct 08 2011 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.1.1-1
- Update to 1.1.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.1.0-3
- Rebuilt for gcc bug 634757

* Sun Sep 26 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.1.0-2
- Fix 64bit plugin paths, once again

* Sat Sep 25 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.1.0-1
- Update to 1.1.0

* Tue Jul 20 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.0.0-5
- Rebuild against new liblo

* Wed Feb 10 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.0.0-4
- Fix DSO-linking failure

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.0.0-2
- Fix the default DSSI plugin path to avoid a crash

* Fri May 29 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.0.0-1
- Update to 1.0.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.9.1-15
- fix license tag
- patch0 was unnecessary

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.1-14
- Autorebuild for GCC 4.3

* Thu Jan 03 2008 Anthony Green <green@redhat.com> 0.9.1-13
- Add cstdlib patch for gcc 4.3 support.

* Mon Oct 07 2007 Anthony Green <green@redhat.com> 0.9.1-11
- Rebuild for new lash.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.9.1-10
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 18 2006 Anthony Green <green@redhat.com> 0.9.1-9
- Fix release tag.

* Mon Sep 18 2006 Anthony Green <green@redhat.com> 0.9.1-8.1
- Rebuild.

* Mon Sep  4 2006 Anthony Green <green@redhat.com> 0.9.1-8
- -devel packages with .pc files must now Require pkgconfig.

* Sun Jun  4 2006 Anthony Green <green@redhat.com> 0.9.1-7
- Tweak URL.

* Fri Jun  2 2006 Anthony Green <green@redhat.com> 0.9.1-6
- Tweak License again.

* Tue May 30 2006 Anthony Green <green@redhat.com> 0.9.1-5
- Add dssi-lib64.patch so jack-dssi-host looks in lib64 dir for
  x86-64 systems.

* Fri May 26 2006 Anthony Green <green@redhat.com> 0.9.1-4
- Tweak License fields.

* Sun May 21 2006 Anthony Green <green@redhat.com> 0.9.1-3
- Move .pc file from examples to devel.
- Delete the .la files instead of %%exclude-ing them.
- Add some dependencies to the -devel package.
- dssi-devel package no longer depends on dssi.
- Move COPYING to devel package.

* Thu May 18 2006 Anthony Green <green@redhat.com> 0.9.1-2
- Clean up BuildRequires.
- Add "%%dir" to dssi lib dir in $files.
- Move plugin examples to a new -examples package.

* Sat May 13 2006 Anthony Green <green@redhat.com> 0.9.1-1
- Upgrade to 0.9.1 sources.
- Remove fluidsynth-dssi bits.
- Own %%{_libdir}/dssi.

* Tue Apr 25 2006 Anthony Green <green@redhat.com> 0.9-3
- Own %%{_libdir}/dssi/* directories.

* Tue Apr 18 2006 Anthony Green <green@redhat.com> 0.9-2
- Build for Fedora Extras.

* Thu Aug 19 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.4-1
- initial build.
- include fluidsynth sources, dssi needs them for the fluidsynth-dssi
  example (it relies on more than the standard fluidsynth API)