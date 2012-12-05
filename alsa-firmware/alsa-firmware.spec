# This is a firmware package, so binaries (which are not run on the host)
# in the end package are expected.
%define _binaries_in_noarch_packages_terminate_build   0

Summary:        Firmware for several ALSA-supported sound cards
Summary(zh_CN.UTF-8): 一些 ALSA 支持的声卡需要的固件
Name:           alsa-firmware
Version:        1.0.24.1
Release:        3%{?dist}
# See later in the spec for a breakdown of licensing
License:        GPL+ and BSD and GPLv2+ and GPLv2 and LGPLv2+
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:            http://www.alsa-project.org/
Source0:        %{name}-%{version}.tar.bz2
Source1:        alsa-firmware.README
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       alsa-tools-firmware >= %{version}
Requires:       udev
BuildRequires:  automake
BuildRequires:  autoconf

# noarch, since the package is firmware
BuildArch:      noarch

%description
This package contains the firmware binaries for a number of sound cards.
Some (but not all of these) require firmware loaders which are included in
the alsa-tools-firmware package.

%description -l zh_CN.UTF-8


%prep
%setup -q


%build
# Leaving this directory in place ends up with the following crazy, broken
# symlinks in the output RPM, with no sign of the actual firmware (*.bin) files
# themselves:
#
# /lib/firmware/turtlebeach:
# msndinit.bin -> /etc/sound/msndinit.bin
# msndperm.bin -> /etc/sound/msndperm.bin
# pndsperm.bin -> /etc/sound/pndsperm.bin
# pndspini.bin -> /etc/sound/pndspini.bin
#
# Probably an upstream package bug.
sed -i s#'multisound/Makefile \\'## configure.in
sed -i s#multisound## Makefile.am

%__aclocal
%__automake
%__autoconf
%configure --disable-loader
make %{?_smp_mflags}

# Rename README files from firmware subdirs that have them
for i in hdsploader mixartloader pcxhrloader usx2yloader vxloader
do
  mv ${i}/README README.${i}
done


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}
cp -p %{SOURCE1} README.fedora

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README*

# License: KOS (BSD-alike)
/lib/firmware/aica_firmware.bin

# License: No explicit license; default package license is GPLv2+
/lib/firmware/asihpi

# License: GPL (undefined version)
/lib/firmware/digiface_firmware*

%dir /lib/firmware/ea
# The licenses for the Echo Audio firmware vary slightly so each is enumerated
# separately, to be really sure.
# LGPLv2.1+
/lib/firmware/ea/3g_asic.fw
# GPL (undefined version)
/lib/firmware/ea/darla20_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/darla24_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/echo3g_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina20_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_301_asic.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_301_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_361_asic.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_361_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_dj_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_djx_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_io_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_iox_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/layla20_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla20_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_1_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_2A_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_2S_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/loader_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/mia_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/mona_2_asic.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_1_asic_48.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_1_asic_96.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_1_asic_48.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_1_asic_96.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_dsp.fw

%dir /lib/firmware/emu
# Licenses vary so are enumerated separately
# GPLv2
/lib/firmware/emu/audio_dock.fw
# GPLv2
/lib/firmware/emu/emu0404.fw
# GPLv2
/lib/firmware/emu/emu1010_notebook.fw
# GPLv2
/lib/firmware/emu/emu1010b.fw
# GPLv2
/lib/firmware/emu/hana.fw
# GPLv2+
/lib/firmware/emu/micro_dock.fw

# License: GPL (undefined version)
/lib/firmware/ess

# License: No explicit license; default package license is GPLv2+
/lib/firmware/korg

# License: GPL (undefined version)
/lib/firmware/mixart

# License: GPL (undefined version)
/lib/firmware/multiface_firmware*

# License: GPL (undefined version)
/lib/firmware/pcxhr

# License: GPL (undefined version)
/lib/firmware/rpm_firmware.bin

# License: GPLv2+
/lib/firmware/sb16

# License: GPL (undefined version)
/lib/firmware/vx

# License: No explicit license; default package license is GPLv2+
# See ALSA bug #3412
/lib/firmware/yamaha

# License: Unknown
/lib/firmware/emagic/emi26-bitstream.bin
/lib/firmware/emagic/emi26-firmware.bin
/lib/firmware/emagic/emi26-loader.bin
/lib/firmware/emagic/emi62-bitstream.bin
/lib/firmware/emagic/emi62-firmware-midi.bin
/lib/firmware/emagic/emi62-firmware-spdif.bin
/lib/firmware/emagic/emi62-firmware.bin
/lib/firmware/emagic/emi62-loader.bin
/lib/firmware/emagic/license.txt

# upstream bug
# /lib/firmware/turtlebeach/msndinit.bin
# /lib/firmware/turtlebeach/msndperm.bin
# /lib/firmware/turtlebeach/pndsperm.bin
# /lib/firmware/turtlebeach/pndspini.bin

# Even with --disable-loader, we still get usxxx firmware here; looking at the
# alsa-tools-firmware package, it seems like these devices probably use an old- 
# style hotplug loading method
# License: GPL (undefined version)
%{_datadir}/alsa/firmware


%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.0.24.1-3
- 为 Magic 3.0 重建

* Fri Oct 28 2011 Liu Di <liudidi@gmail.com> - 1.0.24.1-3
- 为 Magic 3.0 重建　

