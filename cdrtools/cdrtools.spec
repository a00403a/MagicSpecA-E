%define main_ver 3.01
%define min_ver a07
Summary: A collection of CD/DVD utilities.
Summary(zh_CN.UTF-8): 一套 CD/DVD 工具集合
Name: cdrtools
Version: %{main_ver}.%{min_ver}
Release: 2%{?dist}
%define tarversion %{main_ver}%{min_ver}
License: CDDL
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://cdrecord.berlios.de/old/private/cdrecord.html
Source: ftp://ftp.berlios.de/pub/cdrecord/alpha/cdrtools-%{tarversion}.tar.bz2
Source1: cdrecord.conf

BuildRequires: perl, groff

BuildRoot: %{_tmppath}/%{name}-%{version}-root
# REMOVE epoch if the package NAME ever changes.  When package names change,
# the Epoch information is no longer needed.  However, if someone makes an
# official release by accident with an Epoch, then Epoch is again permanent.
Epoch: 9

%description
cdrtools is a collection of CD/DVD utilities.

%description -l zh_CN.UTF-8
cdrtools是一套 CD/DVD 工具集合。

%package -n cdrecord
Summary: A command line CD/DVD recording program.
Summary(zh_CN.UTF-8): 命令行的 CD/DVD 刻录程序。
Group: Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
Obsoletes: dvdrecord <= 0:0.1.5
Provides: dvdrecord
Provides: wodim

%description -n cdrecord
Cdrecord is an application for creating audio and data CDs. Cdrecord
works with many different brands of CD recorders, fully supports
multi-sessions and provides human-readable error messages.

%description -n cdrecord -l zh_CN.UTF-8
Cdrecord是一个建立音频和数据CD的程序。Cdrecord可以与许多不同的刻录机
工作，完全支持多轨刻录并提供可以可以方便阅读的错误信息。

%package -n cdrecord-devel
Summary: The libschily SCSI user level transport library.
Summary(zh_CN.UTF-8): SCSI 用户级转换库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: cdrecord = %{epoch}:%{version}-%{release}

%description -n cdrecord-devel
The cdrecord-devel package contains a SCSI user level transport
library which can talk to any SCSI device without a special driver for
the device. Cdrecord can easily be ported to any system with a SCSI
device driver similar to the scg driver.

%description -n cdrecord-devel -l zh_CN.UTF-8
cdrecord-devel包包含了SCSI 用户级转换库，它可以不通过特定驱动和SCSI
设备对话。Cdrecord可以简单的进行移植。

%package -n mkisofs
Summary: Creates an image of an ISO9660 filesystem.
Summary(zh_CN.UTF-8): 建立 ISO9660 文件系统的镜像。
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Obsoletes: cdrecord-mkisofs
Provides: cdrecord-mkisofs
Provides: genisoimage

%description -n mkisofs
The mkisofs program is used as a pre-mastering program; i.e., it
generates the ISO9660 filesystem.  Mkisofs takes a snapshot of
a given directory tree and generates a binary image of the tree
which will correspond to an ISO9660 filesystem when written to
a block device.  Mkisofs is used for writing CD-ROMs, and includes
support for creating bootable El Torito CD-ROMs.

Install the mkisofs package if you need a program for writing
CD-ROMs.

%description -n mkisofs
mkisofs是用来制作ISO镜像文件的工具。

如果需要写 CD-ROM，那么需要安装mkisofs。

%package -n cdda2wav
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Summary: A utility for sampling/copying .wav files from digital audio CDs.
Summary(zh_CN.UTF-8): 从音频CD中采样/复制 .wav 文件的工具。
Obsoletes: cdrecord-cdda2wav
Provides: cdrecord-cdda2wav
Provides: icedax

%description -n cdda2wav
Cdda2wav is a sampling utility for CD-ROM drives that are capable of
providing a CD's audio data in digital form to your host. Audio data
read from the CD can be saved as .wav or .sun format sound files.
Recording formats include stereo/mono, 8/12/16 bits and different
rates.  Cdda2wav can also be used as a CD player.

%description -n cdda2wav
Cdda2wav是一个抓音轨的工具，可以把CD上的声音数据保存成 .wav或 .sun
格式的声音文件。格式可以包括 立体声/单声道，8/12/16位和不同的采样率。
Cdda2wav也可以当做CD播放器使用。

%prep
%setup -q -n %{name}-%{main_ver}

%build
./Gmake.linux


%install
rm -rf $RPM_BUILD_ROOT
mandir=%{_mandir}
./Gmake.linux "MANDIR=${mandir#/usr}" "INS_BASE=$RPM_BUILD_ROOT/usr" install

groff -Tps -man doc/cdrecord.man > doc/cdrecord.ps

mkdir -p $RPM_BUILD_ROOT/etc

install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/etc/cdrecord.conf

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files -n cdrecord
%defattr(-,root,root)
%doc AN-*  Changelog README* 
%doc COPYING cdrecord/LICENSE
%doc cdrecord/cdrecord.dfl
%config(noreplace) /etc/cdrecord.conf
%{_bindir}/cdrecord
%{_bindir}/readcd
%{_bindir}/devdump
#是否还有必要？
#%{_bindir}/dvdrecord
#%{_mandir}/man1/dvdrecord.1*

%files -n cdrecord-devel
%defattr(-,root,root)
%{_libdir}/libdeflt.a
%{_libdir}/libscg.a
%{_libdir}/libschily.a
%{_libdir}/libedc_ecc.a
%{_libdir}/libparanoia.a
/usr/include/schily

%files -n mkisofs
%defattr(-,root,root)
%doc AN-* mkisofs/COPYING mkisofs/ChangeLog
%doc mkisofs/README*
%{_bindir}/mkisofs
%{_bindir}/mkhybrid
%{_bindir}/isoinfo
%{_bindir}/isodump
%{_bindir}/isovfy
%{_bindir}/isodebug

%files -n cdda2wav
%defattr(-,root,root)
%doc AN-* cdda2wav/FAQ cdda2wav/OtherProgs
%doc cdda2wav/README* cdda2wav/Frontends cdda2wav/HOWTOUSE
%{_bindir}/cdda2wav
#以下需要分包
%_bindir/btcflash
%_bindir/cdda2mp3
%_bindir/scgcheck
%{_bindir}/cdda2ogg
%{_bindir}/scgskeleton
%_includedir/scg/*
%_libdir/*.a
%_libdir/profiled/*.a
%_libdir/siconv/*
/usr/sbin/rscsi
   /usr/share/doc/cdda2wav/README
   /usr/share/doc/cdrecord/README
   /usr/share/doc/cdrecord/README.ATAPI
   /usr/share/doc/cdrecord/README.DiskT@2
   /usr/share/doc/cdrecord/README.WORM
   /usr/share/doc/cdrecord/README.audio
   /usr/share/doc/cdrecord/README.cdplus
   /usr/share/doc/cdrecord/README.cdrw
   /usr/share/doc/cdrecord/README.cdtext
   /usr/share/doc/cdrecord/README.clone
   /usr/share/doc/cdrecord/README.copy
   /usr/share/doc/cdrecord/README.multi
   /usr/share/doc/cdrecord/README.parallel
   /usr/share/doc/cdrecord/README.raw
   /usr/share/doc/cdrecord/README.rscsi
   /usr/share/doc/cdrecord/README.solaris-x86-ATAPI-DMA
   /usr/share/doc/cdrecord/README.solaris-x86-ata-DMA
   /usr/share/doc/cdrecord/README.sony
   /usr/share/doc/cdrecord/README.sun-lofi
   /usr/share/doc/cdrecord/README.verify
   /usr/share/doc/cdrecord/README.volmgt
   /usr/share/doc/libparanoia/README.interface
   /usr/share/doc/libparanoia/README.paranoia
   /usr/share/doc/mkisofs/README
   /usr/share/doc/mkisofs/README.compression
   /usr/share/doc/mkisofs/README.eltorito
   /usr/share/doc/mkisofs/README.graft_dirs
   /usr/share/doc/mkisofs/README.hfs_boot
   /usr/share/doc/mkisofs/README.hfs_magic
   /usr/share/doc/mkisofs/README.hide
   /usr/share/doc/mkisofs/README.joliet
   /usr/share/doc/mkisofs/README.macosx
   /usr/share/doc/mkisofs/README.mkhybrid
   /usr/share/doc/mkisofs/README.prep_boot
   /usr/share/doc/mkisofs/README.rootinfo
   /usr/share/doc/mkisofs/README.session
   /usr/share/doc/mkisofs/README.sort
   /usr/share/doc/mkisofs/README.sparcboot
   /usr/share/doc/mkisofs/README.sunx86boot
   /usr/share/doc/rscsi/default-rscsi.sample
   /usr/share/share/man/man1/btcflash.1
   /usr/share/share/man/man1/cdda2mp3.1
   /usr/share/share/man/man1/cdda2ogg.1
   /usr/share/share/man/man1/cdda2wav.1
   /usr/share/share/man/man1/cdrecord.1
   /usr/share/share/man/man1/readcd.1
   /usr/share/share/man/man1/rscsi.1
   /usr/share/share/man/man1/scgcheck.1
   /usr/share/share/man/man1/scgskeleton.1
   /usr/share/share/man/man5/makefiles.5
   /usr/share/share/man/man5/makerules.5
   /usr/share/share/man/man8/devdump.8
   /usr/share/share/man/man8/isodebug.8
   /usr/share/share/man/man8/isodump.8
   /usr/share/share/man/man8/isoinfo.8
   /usr/share/share/man/man8/isovfy.8
   /usr/share/share/man/man8/mkhybrid.8
   /usr/share/share/man/man8/mkisofs.8
%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 9:3.01.a07-2
- 为 Magic 3.0 重建


