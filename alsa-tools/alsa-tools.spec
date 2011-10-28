# 如果你想略过 firmware 子包的编译，把 _without_firmware 宏设成 1。
# 这不是固件自身（那是 alsa-firmware 包），这是一些相关的工具。
# *不要*设成 0 或注释掉这个宏，不然就没办法编译了。

%ifarch ppc ppc64
# sb16_csp 不能在 PPC 上编译; 查看 bug #219010
%{?!_without_tools:     %global builddirstools as10k1 echomixer envy24control hdspconf hdspmixer hwmixvolume rmedigicontrol sbiload sscape_ctl us428control }
%else
%{?!_without_tools:     %global builddirstools as10k1 echomixer envy24control hdspconf hdspmixer hwmixvolume rmedigicontrol sbiload sb16_csp sscape_ctl us428control }
%endif

%{?!_without_firmware:  %global builddirsfirmw hdsploader mixartloader usx2yloader vxloader }

Summary:        Specialist tools for ALSA
Summary(zh_CN.UTF-8): ALSA 相关的工具
Name:           alsa-tools
Version:        1.0.24.1
Release:        3%{?dist}

License:        GPLv2+
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:            http://www.alsa-project.org/
Source0:        %{name}-%{version}.tar.bz2

Source1:        envy24control.desktop
Source2:        envy24control.png
Source3:        echomixer.desktop
Source4:        echomixer.png
Source5:        90-alsa-tools-firmware.rules
# Resized version of public domain clipart found here:
# http://www.openclipart.org/detail/17428
Source6:	hwmixvolume.png
Source7:	hwmixvolume.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  alsa-lib-devel >= 1.0.24
%if 0%{!?_without_tools:1}
BuildRequires:  gtk+-devel
BuildRequires:  gtk2-devel
BuildRequires:  fltk-devel
Buildrequires:  desktop-file-utils
Requires:       xorg-x11-fonts-misc
# Needed for hwmixvolume
Requires:	python-alsa
%endif

%description
This package contains several specialist tools for use with ALSA, including
a number of programs that provide access to special hardware facilities on
certain sound cards.

* as10k1 - AS10k1 Assembler
%ifnarch ppc ppc64
* cspctl - Sound Blaster 16 ASP/CSP control program
%endif
* echomixer - Mixer for Echo Audio (indigo) devices
* envy24control - Control tool for Envy24 (ice1712) based soundcards
* hdspmixer - Mixer for the RME Hammerfall DSP cards
* hwmixvolume - Control the volume of individual streams on sound cards that
  use hardware mixing
* rmedigicontrol - Control panel for RME Hammerfall cards
* sbiload - An OPL2/3 FM instrument loader for ALSA sequencer
* sscape_ctl - ALSA SoundScape control utility
* us428control - Control tool for Tascam 428

%description -l zh_CN.UTF-8
ALSA 相关的一些工具，包括访问一些特殊型号的声卡需要的程序。


%package firmware
Summary:        ALSA tools for uploading firmware to some soundcards
Summary(zh_CN.UTF-8): 上传固件到一些声卡的 ALSA 工具
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires:       udev
Requires:       alsa-firmware
Requires:       fxload


%description firmware
This package contains tools for flashing firmware into certain sound cards.
The following tools are available:

* hdsploader   - for RME Hammerfall DSP cards
* mixartloader - for Digigram miXart soundcards
* vxloader     - for Digigram VX soundcards
* usx2yloader  - second phase firmware loader for Tascam USX2Y USB soundcards

%description firmware -l zh_CN.UTF-8
上传固件到一些声卡的 ALSA 工具。

%prep
%setup -q -n %{name}-%{version}

%build
mv seq/sbiload . ; rm -rf seqdd
for i in %{?builddirstools:%builddirstools} %{?builddirsfirmw:%builddirsfirmw}
do
  cd $i ; %configure
  %{__make} %{?_smp_mflags} || exit 1
  cd ..
done


%install
%{__rm} -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/{pixmaps,applications}

for i in %{?builddirstools:%builddirstools} %{?builddirsfirmw:%builddirsfirmw}
do
  case $i in
    echomixer)
      (cd $i ; %makeinstall ; install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/pixmaps/ ; install -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_datadir}/applications/ ) || exit 1
      ;;
    envy24control)
      (cd $i ; %makeinstall ; install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/ ; install -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/applications/ ) || exit 1
      ;;
    hdspconf)
      (cd $i ; %makeinstall pixmapdir=${RPM_BUILD_ROOT}%{_datadir}/pixmaps desktopdir=${RPM_BUILD_ROOT}%{_datadir}/applications ) || exit 1
      ;;
    hdspmixer)
      (cd $i ; %makeinstall pixmapdir=${RPM_BUILD_ROOT}%{_datadir}/pixmaps desktopdir=${RPM_BUILD_ROOT}%{_datadir}/applications ) || exit 1
      ;;
    hwmixvolume)
      (cd $i ; %makeinstall ; install -m 644 %{SOURCE6} %{buildroot}%{_datadir}/pixmaps/ ; install -m 644 %{SOURCE7} ${RPM_BUILD_ROOT}%{_datadir}/applications/ ) || exit 1
      ;;
    usx2yloader)
      (cd $i ; %makeinstall hotplugdir=${RPM_BUILD_ROOT}%{_sysconfdir}/hotplug/usb) || exit 1
      ;;
    *) (cd $i ; %makeinstall) || exit 1
   esac
   if [[ -s "${i}"/README ]]
   then
      if [[ ! -d "${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/${i}" ]]
      then
         mkdir -p "${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/${i}"
      fi
      cp "${i}"/README "${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/${i}"
   fi
   if [[ -s "${i}"/COPYING ]]
   then
      if [[ ! -d "${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/${i}" ]]
      then
         mkdir -p "${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/${i}"
      fi
      cp "${i}"/COPYING "${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/${i}"
   fi
   if [[ -s ${RPM_BUILD_ROOT}%{_datadir}/applications/${i}.desktop ]] ; then
      desktop-file-install --vendor fedora \
        --add-category "X-Fedora" \
        --delete-original \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications \
        ${RPM_BUILD_ROOT}%{_datadir}/applications/${i}.desktop
   fi
done

# convert hotplug stuff to udev
rm -f ${RPM_BUILD_ROOT}%{_sysconfdir}/hotplug/usb/tascam_fw.usermap
mkdir -p ${RPM_BUILD_ROOT}/lib/udev
mv ${RPM_BUILD_ROOT}%{_sysconfdir}/hotplug/usb/* ${RPM_BUILD_ROOT}/lib/udev
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/udev/rules.d
install -m 644 %{SOURCE5} ${RPM_BUILD_ROOT}%{_sysconfdir}/udev/rules.d

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%if 0%{!?_without_tools:1}
%files
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/as10k1
%doc %{_docdir}/%{name}-%{version}/echomixer
%doc %{_docdir}/%{name}-%{version}/envy24control
%doc %{_docdir}/%{name}-%{version}/hdspconf
%doc %{_docdir}/%{name}-%{version}/hdspmixer
%doc %{_docdir}/%{name}-%{version}/hwmixvolume
%doc %{_docdir}/%{name}-%{version}/rmedigicontrol
%doc %{_docdir}/%{name}-%{version}/sbiload
%{_bindir}/as10k1
%{_bindir}/echomixer
%{_bindir}/envy24control
%{_bindir}/hdspconf
%{_bindir}/hdspmixer
%{_bindir}/hwmixvolume
%{_bindir}/rmedigicontrol
%{_bindir}/sbiload
%{_bindir}/sscape_ctl
%{_bindir}/us428control
%{_datadir}/applications/fedora-echomixer.desktop
%{_datadir}/applications/fedora-envy24control.desktop
%{_datadir}/applications/fedora-hdspconf.desktop
%{_datadir}/applications/fedora-hdspmixer.desktop
%{_datadir}/applications/fedora-hwmixvolume.desktop
%{_datadir}/man/man1/envy24control.1.gz
%{_datadir}/pixmaps/echomixer.png
%{_datadir}/pixmaps/envy24control.png
%{_datadir}/pixmaps/hdspconf.png
%{_datadir}/pixmaps/hdspmixer.png
%{_datadir}/pixmaps/hwmixvolume.png
%{_datadir}/sounds/*

# sb16_csp stuff which is excluded for PPCx
%ifnarch ppc ppc64
%doc %{_docdir}/%{name}-%{version}/sb16_csp
%{_bindir}/cspctl
%{_datadir}/man/man1/cspctl.1.gz
%endif

%endif

%if 0%{!?_without_firmware:1}
%files firmware
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/hdsploader
%doc %{_docdir}/%{name}-%{version}/mixartloader
%doc %{_docdir}/%{name}-%{version}/usx2yloader
%doc %{_docdir}/%{name}-%{version}/vxloader
%config(noreplace) %{_sysconfdir}/udev/rules.d/*.rules
/lib/udev/tascam_fpga
/lib/udev/tascam_fw
%{_bindir}/hdsploader
%{_bindir}/mixartloader
%{_bindir}/usx2yloader
%{_bindir}/vxloader
%endif

%changelog
* Fri Oct 28 2011 Liu Di <liudidi@gmail.com> - 1.0.24.1-3
- 为 Magic 3.0 重建

