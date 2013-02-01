# Hi Googlers! If you're looking in here for patches, nifty.
# You (and everyone else) are welcome to use any of my Chromium spec files and 
# patches under the terms of the GPLv2 or later.
# You (and everyone else) are welcome to use any of my V8-specific spec files 
# and patches under the terms of the BSD license.
# You (and everyone else) may NOT use my spec files or patches under any other 
# terms.
# I hate to be a party-pooper here, but I really don't want to help Google 
# make a proprietary browser. There are enough of those already.
# All copyrightable work in these spec files and patches is Copyright 2011 
# Tom Callaway <spot@fedoraproject.org>

# Update this with every matching v8 build
%global v8ver 1:3.13.7.5

# Update this with every matching libjingle build
%global jingle_version 0.6.19

# If we're using a svn checkout, define this
# %%global svncheckout 20100819svn56724

# We need policy first.
%global selinux 0

# Useful for debugging
%global noisy 0

# Google has abandoned any concept of shared bits, so we shall as well.
%global sharedbuild 0

# DO NOT DISTRIBUTE ANY BUILDS WITH THIS ON.
# It is only for debugging issues.
%global vanillabuild 0

## Maybe, someday, I'll be able to flip these on. ##

# Chromium depends on forked sqlite features not foind in upstream.
%global sqlite 0

# Chromium depends on forked NSS features not found in upstream.
%global nss 0

# It may at some point become too painful to maintain this.
# That point arrived with chromium 19. :P
%global jingle 0

# System libsrtp
# Chromium only uses this if we're using their bundled libjingle.
%global libsrtp 1

# System flac
%global flac 1

# System v8
%global sysv8 1

# vanillabuild overrides
%if 0%{?vanillabuild}
%global jingle 0
%global libsrtp 0
%global nss 0
%global sqlite 0
%global flac 0
%global v8 0
%endif

Name:		chromium
# see src/chrome/VERSION
# Google's versioning is interesting (and by that I mean, dumb). They never reset "BUILD", 
# which is how we jumped from 3.0.201.0 to 4.0.202.0 as they moved to a new major branch
Version:	23.0.1271.95
Release:	1%{?svncheckout:.%{svncheckout}}%{?dist}
Summary:	A WebKit powered web browser
# Licensing Overview
# 
# ffmpeg headers are LGPLv2+
# libjingle is BSD

# TODO: Proper list of licenses
License:	BSD and LGPLv2+
Group:		Applications/Internet
# Just the code changes, none of the "makefile" changes
Patch0:		chromium-23.0.1271.95-codechanges-system-minizip-nss-nspr-v8.patch

# These are the conditionals that upstream has added:
# bzip2, jpeg, png, zlib, xml, xslt, libevent, v8

# We also remove minizip, which google left in because ubuntu doesn't have it. :P
Patch4:		chromium-20.0.1132.47-gyp-system-minizip.patch

# Use system libicu
Patch7:		chromium-23.0.1271.95-gyp-system-icu.patch
Patch8:		chromium-23.0.1271.95-icu-code-changes.patch

# webkit needs to call nss to pull in nspr headers
Patch10:	chromium-14.0.827.10-system-nss.patch

# Courgette not in source tree
Patch15:	chromium-23.0.1271.95-no-courgette.patch

# Don't try to build non-existent test sources
Patch19:	chromium-23.0.1271.95-no-test-sources.patch

# Fix ffmpeg wrapper compile
Patch25:	chromium-17.0.963.46-ffmpeg-no-pkgconfig.patch

# Use system libjingle
Patch29:	chromium-20.0.1132.47-system-libjingle.patch

# Use system speex
Patch30:	chromium-23.0.1271.95-system-speex.patch

# Use system libsrtp
Patch33:	chromium-20.0.1132.47-system-srtp.patch

# Use system libvpx
Patch34:	chromium-23.0.1271.95-system-libvpx.patch

# Use system copy of FLAC
Patch40:	chromium-23.0.1271.95-system-flac.patch

# Fix gcc46 issues
Patch41:        chromium-23.0.1271.95-gcc46.patch

# Pull in nss for nspr for chrome_common
Patch43:        chromium-19.0.1084.56-chrome-common-nss.patch

# Use system nss in base
Patch45:	chromium-21.0.1180.81-prtimefix.patch

# Replace gnome-volume-control exec with gnome-control-center sound (GNOME3 only)
Patch49:        chromium-14.0.835.186-gnome3.patch

# Fix compile against external ffmpegsumo
# This is a bit hacky, but I didn't want to re-learn GYP.
Patch53:        chromium-13.0.782.112-ffmpegsumo-compile-fix.patch

# Get nacl going
Patch55:	chromium-23.0.1271.95-build-nacl-irt.patch

# Add missing include for header that provides OVERRIDE definition
Patch57:	chromium-20.0.1132.47-OVERRIDE-define-fix.patch

# Use --no-keep-memory in ldflags to ensure the final exec doesn't run
# out of memory while linking.
Patch62:	chromium-20.0.1132.47-ldflags-no-keep-memory.patch

# Use system jsoncpp
Patch66:	chromium-20.0.1132.47-system-jsoncpp.patch

# Use system webrtc
Patch67:	chromium-23.0.1271.95-system-webrtc.patch

# Use system libusb1
Patch71:	chromium-23.0.1271.95-system-libusb.patch

# Chromium contains a local implementation of a string byte sink needed when ICU is compiled without
# support for std::string which is the case on Android. However, Fedora's system ICU has std::string.
Patch72:	chromium-21.0.1180.81-only-droid.patch

# http://code.google.com/p/gperftools/issues/detail?id=444
Patch73:	chromium-21.0.1180.81-glibc216.patch

# Taken from upstream webkit
# http://trac.webkit.org/changeset/124099
Patch74:	changeset_124099.diff

# Don't unpack nacl-sources. We've got it.
Patch75:	chromium-23.0.1271.95-more-naclfixes.patch

# More incorrect hardcoded headers. I would say Google's getting sloppy, but well, this is status quo.
Patch76:	chromium-23.0.1271.95-zlib-fixes.patch

# Taken from upstream chromium
# http://git.chromium.org/gitweb/?p=chromium.git;a=commitdiff;h=de08ebc796c6e7d31c516155e2df5375973d74e5
Patch77:	chromium-23.0.1271.95-de08ebc796c6e7d31c516155e2df5375973d74e5.patch

Patch78:	chromium-23.0.1271.95-stillmorenaclfixes.patch

# Use chromium-latest.py to generate clean tarball from released build tarballs, found here:
# http://build.chromium.org/buildbot/official/
%if 0%{?vanillabuild}
Source0:	chromium-%{version}.tar.bz2
%else
%if %{defined svncheckout}
Source0:	chromium-%{version}-%{?svncheckout}.tar.lzma
%else
Source0:	chromium-%{version}-clean.tar.lzma
%endif
%endif
Source2:	chromium-browser.sh
Source3:	chromium-browser.desktop
Source5:	chromium-browser.xml
# Set default prefs
Source6:	master_preferences
# Also, only used if you want to reproduce the clean tarball.
Source7:	chromium-latest.py
# Nicer icon generated via inkscape from chromium.ai
# http://src.chromium.org/viewvc/chrome/trunk/src/chrome/app/theme/chromium/chromium.ai?view=log&pathrev=81848
Source9:	chromium-12-256x256.svg

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	bzip2-devel, libevent-devel, libjpeg-devel, libpng-devel
BuildRequires:	libxslt-devel, nss-devel, nspr-devel, minizip-devel, expat-devel
BuildRequires:	gcc-c++, bison, flex, gtk2-devel, atk-devel
BuildRequires:	fontconfig-devel, GConf2-devel, dbus-devel, alsa-lib-devel
BuildRequires:	desktop-file-utils, gperf
BuildRequires:	nss-devel >= 3.12.3
BuildRequires:	dbus-glib-devel, libXScrnSaver-devel
BuildRequires:	cups-devel
BuildRequires:	perl(Switch)
BuildRequires:	perl(Digest::MD5)

# Use the forked ffmpeg headers
BuildRequires:	chromium-ffmpegsumo-devel >= 21.0.1180.81

%if 0%{?sysv8}
BuildRequires:	v8-devel >= %{v8ver}
%endif

# Fedora 12 (and presumably, older) don't have libgnome-keyring-devel
%if 0%{?fedora} <= 12 && 0%{?rhel} <= 6
BuildRequires:	gnome-keyring-devel
%else
BuildRequires:	libgnome-keyring-devel
%endif

# You need some special love to build on Fedora 11.
%if 0%{?fedora} <= 11 && 0%{?rhel} <= 5
BuildRequires:  libicu42-devel
%else
BuildRequires:  libicu-devel >= 4.2
%endif

# NaCl needs these
BuildRequires:  libstdc++-devel, openssl-devel
BuildRequires:	nacl-gcc, nacl-binutils, nacl-newlib

%if 0%{?sqlite}
BuildRequires:	sqlite-devel
%endif

%if 0%{?selinux}
BuildRequires:	libselinux-devel
%endif

%if 0%{?jingle}
BuildRequires:	libjingle-devel >= %{jingle_version}
%endif

%if 0%{?libsrtp}
BuildRequires:	libsrtp-devel >= 1.4.4
%endif

%if 0%{?flac}
BuildRequires:	flac-devel
%endif

BuildRequires:	speex-devel = 1.2
BuildRequires:	libvpx-devel
BuildRequires:	libudev-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	elfutils-libelf-devel
BuildRequires:	jsoncpp-devel
BuildRequires:	webrtc-devel >= 0.1-0.9.20121218svn2718, libyuv-devel
BuildRequires:	libusbx-devel

ExclusiveArch:	%{ix86} arm x86_64

%if 0%{?vanillabuild}
# Do nothing.
%else
%if 0%{?jingle}
Requires: libjingle%{?_isa} >= %{jingle_version}
%endif
%endif

# GTK modules it expects to find for some reason.
Requires:	libcanberra-gtk2%{_isa}

# We pick up an automatic requires on the library, but we need the version check
# because the nss shared library is unversioned.
# This is to prevent someone from hitting http://code.google.com/p/chromium/issues/detail?id=26448
Requires:	nss%{_isa} >= 3.12.3
Requires:	nss-mdns%{_isa}

# This is a lie, but it keeps older upgrades semi-sane
Provides:	chromium-libs = %{version}-%{release}
Obsoletes:	chromium-libs <= %{version}-%{release}

%if 0%{?sysv8}
Requires:	v8 >= %{v8ver}
%endif

%description
Chromium is an open-source web browser, powered by WebKit.

%if 0%{?sharedbuild}
%package libs
Summary:	Shared libraries for chromium
Group:		System Environment/Libraries
# We hardcode this because we don't get symbol deps with newer v8 versions
# This forces an upgrade
%if 0%{?sysv8}
Requires:	v8 >= %{v8ver}
%endif

%description libs
This package contains the shared libraries that chromium depends on. Some of 
these libraries are unique to chromium, others are forked versions of system 
libraries.
%endif

%prep
echo "####### BUILD OPTIONS #######"
echo "Using system NSS: %{nss}"
echo "Using system sqlite3: %{sqlite}"
echo "Using system v8: %{sysv8}"
echo "Built-in SELinux support: %{selinux}"
echo "Verbose Build: %{noisy}"
%if 0%{?sharedbuild}
echo "Shared Build"
%else
echo "Static Build"
%endif
%setup -q -n chromium-%{version}%{?svncheckout:-%{svncheckout}}

%if %{defined svncheckout}
mv src/* .
%endif

%if 0%{?vanillabuild}
# Don't apply any of these patches.

%else

# Patch in code changes for system libs
%patch0 -p1 -b .system-code

# Fix the zlib.gyp file to use system minizip
%patch4 -p1 -b .system-minizip

# Use system libicu
%patch7 -p1 -b .system-icu
%patch8 -p1 -b .icu

# Courgette not in source tree
%patch15 -p1 -b .no-courgette

# Don't try to build non-existent test sources
%patch19 -p1 -b .notests

# Fix ffmpeg wrapper
%patch25 -p1 -b .no-pkgconfig

%endif

%if 0%{?vanillabuild}
# Ignore the rest of the patchset.
%else

%if 0%{?jingle}
# Use system libjingle
%patch29 -p1 -b .jingle
%endif

# Use system speex
%patch30 -p1 -b .speex

%if 0%{?libsrtp}
%patch33 -p1 -b .system-srtp
%endif

%patch34 -p1 -b .system-libvpx

%if 0%{?flac}
%patch40 -p1 -b .system-flac
%endif

%patch41 -p1 -b .gcc46

%patch43 -p1 -b .nss

%patch45 -p1 -b .base-nss

%if 0%{?fedora} >= 15
%patch49 -p1 -b .gnome3
%endif

%patch53 -p1 -b .ffmpegsumo

%patch55 -p1 -b .buildnacl

%patch57 -p1 -b .OVERRIDE

%patch62 -p1 -b .ldflags

%patch66 -p1 -b .system-jsoncpp

%patch67 -p1 -b .system-webrtc

%patch71 -p1 -b .system-libusb

%patch72 -p1 -b .only-droid

%patch73 -p1 -b .glibc216

# %patch74 -p1 -b .124099

%patch75 -p1 -b .naclfixes

%patch76 -p1 -b .zlibfix

%patch77 -p1 -b .de08ebc

%patch78 -p1 -b .stillmorenaclfixes

# We need this because icu changed its pkg-config files in F16+
%if 0%{?fedora} >= 16
sed -i 's|icu)|icu-i18n)|g' build/linux/system.gyp
%endif

# TODO: Remove this from source tarball
rm -rf third_party/libsrtp/ third_party/libvpx/ third_party/speex/
%if 0%{?flac}
rm -rf third_party/flac/
%endif
%if 0%{?jingle}
# Note to self: leave the overrides in place.
rm -rf third_party/libjingle/source
%endif
rm -rf third_party/webrtc
rm -rf third_party/jsoncpp
rm -rf third_party/libyuv
rm -rf third_party/libusb

%endif

# F-17+ needs to disable narrowing, but earlier gcc versions have no idea what it is.
%if 0%{?fedora} >= 17
%global narrowingflag -Wno-error=narrowing
%endif

# Scrape out incorrect optflags and hack in the correct ones
%if 0%{?sharedbuild}
PARSED_OPT_FLAGS=`echo \'$RPM_OPT_FLAGS -DUSE_SYSTEM_LIBEVENT -fPIC -fno-strict-aliasing -fno-ipa-cp -Wno-error=unused-but-set-variable -Wno-error=c++0x-compat -Wno-error=uninitialized -Wno-error=deprecated-declarations %{?narrowingflag} -Wno-error=int-to-pointer-cast \' | sed "s/ /',/g" | sed "s/',/', '/g"`
%else
PARSED_OPT_FLAGS=`echo \'$RPM_OPT_FLAGS -DUSE_SYSTEM_LIBEVENT -fno-strict-aliasing -fno-ipa-cp -Wno-error=unused-but-set-variable -Wno-error=c++0x-compat -Wno-error=uninitialized -Wno-error=deprecated-declarations %{?narrowingflag} -Wno-error=int-to-pointer-cast \' | sed "s/ /',/g" | sed "s/',/', '/g"`
%endif
for i in build/common.gypi; do
        sed -i "s|'-march=pentium4',||g" $i
        sed -i "s|'-mfpmath=sse',||g" $i
        sed -i "s|'-O<(debug_optimize)',||g" $i
        sed -i "s|'-m32',||g" $i
        sed -i "s|'-fno-exceptions',|$PARSED_OPT_FLAGS|g" $i
done

%if 0%{?vanillabuild}
# Don't do this on a vanilla build
%else
# You need some special love to build on Fedora 11 or RHEL older than 6.
%if 0%{?fedora} <= 11 && 0%{?rhel} <= 5
sed -i 's|icu)|icu42)|g' build/linux/system.gyp
%endif
%endif

# Regenerate the make files
# Also, set the sandbox paths correctly.

./build/gyp_chromium -f make build/all.gyp \
			       --depth . \
                               -Dlinux_sandbox_path=%{_libdir}/chromium-browser/chrome-sandbox \
			       -Dlinux_sandbox_chrome_path=%{_libdir}/chromium-browser/chromium-browser \
%ifarch x86_64
                               -Dtarget_arch=x64 \
%else
			       -Dlinux_use_gold_binary=0 \
                               -Dlinux_use_gold_flags=0 \
%endif
		               -Duse_system_libpng=1 \
		 	       -Duse_system_bzip2=1 \
			       -Duse_system_libjpeg=1 \
			       -Duse_system_zlib=1 \
                               -Duse_system_libxslt=1 \
                               -Duse_system_libxml=1 \
%if 0%{?vanillabuild}
			       -Duse_system_ffmpeg=0 \
%else
                               -Duse_system_ffmpeg=1 \
%endif
                               -Duse_system_vpx=1 \
%if 0%{?nss}
                               -Duse_system_ssl=1 \
%endif
                               -Duse_system_libevent=1 \
%if 0%{?selinux}
                               -Dselinux=1 \
%endif
%if 0%{?sqlite}
                               -Duse_system_sqlite=1 \
%endif
%if 0%{?sysv8}
                               -Duse_system_v8=1 \
%endif
%if 0%{?sharedbuild}
                               -Dlibrary=shared_library \
%endif
%if 0%{?sharedbuild}
                               -Drelease_extra_cflags=-fPIC \
%endif
			       -Ddisable_sse2=1 \
                               -Ddisable_glibc=1 \
                               -Ddisable_newlib=1 \
                               -Ddisable_pnacl=1 \
                               -Djavascript_engine=v8

# Make symlinks for nacl
cd native_client/toolchain/
mkdir -p linux_x86/x86_64-nacl/bin/
mkdir -p linux_x86/x86_64-nacl/lib
mkdir -p linux_x86/x86_64-nacl/lib32
mkdir -p linux_x86/x86_64-nacl/nacl/include/bits
mkdir -p linux_x86/x86_64-nacl/nacl/include/machine
mkdir -p linux_x86/x86_64-nacl/nacl/include/sys
ln -s linux_x86 linux_x86_newlib
cd linux_x86/x86_64-nacl/bin/
ln -s /usr/bin/x86_64-nacl-gcc gcc
ln -s /usr/bin/x86_64-nacl-g++ g++
ln -s /usr/bin/x86_64-nacl-ar ar
ln -s /usr/bin/x86_64-nacl-as as
ln -s /usr/bin/x86_64-nacl-ranlib ranlib
ln -s /usr/bin/x86_64-nacl-strip x86-64-nacl-strip
ln -s /usr/bin/x86_64-nacl-strip strip
cp -a /usr/x86_64-nacl/lib/*.a ../lib/
cp -a /usr/x86_64-nacl/lib/32/*.a ../lib32/
cd ../nacl/include
for i in `find /usr/x86_64-nacl/include/ -type f|grep -v "c++"`; do ln -s $i `echo $i | sed 's|/usr/x86_64-nacl/include/||g'`; done
cd ../../../../..

%build
%if 0%{?selinux}
%if 0%{?noisy}
make -r -j5 chrome BUILDTYPE=Release V=1
%else
make -r -j5 chrome BUILDTYPE=Release
%endif
%else
%if 0%{?noisy}
make -r -j5 chrome chrome_sandbox BUILDTYPE=Release V=1
%else
make -r -j5 chrome chrome_sandbox BUILDTYPE=Release
%endif
%endif

# If we're building sandbox without SELINUX, add "chrome_sandbox" here.
# %if 0%{?selinux}
# %if 0%{?noisy}
# ../../depot_tools/hammer --mode=Release --verbose chrome
# %else
# ../../depot_tools/hammer --mode=Release chrome
# %endif
# %else
# %if 0%{?noisy}
# ../../depot_tools/hammer --mode=Release --verbose chrome chrome_sandbox
# %else
# ../../depot_tools/hammer --mode=Release chrome chrome_sandbox
# %endif
# %endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp -a %{SOURCE2} %{buildroot}%{_bindir}/chromium-browser
export BUILDTARGET=`cat /etc/redhat-release`
sed -i "s|@@BUILDTARGET@@|$BUILDTARGET|g" %{buildroot}%{_bindir}/chromium-browser
# x86_64 capable systems need this
sed -i "s|/usr/lib/chromium|%{_libdir}/chromium|g" %{buildroot}%{_bindir}/chromium-browser
mkdir -p %{buildroot}%{_libdir}/chromium-browser/
mkdir -p %{buildroot}%{_mandir}/man1/
pushd out/Release
cp -a *.pak locales nacl_irt_*.nexe nacl_helper* libppGoogleNaClPluginChrome.so resources %{buildroot}%{_libdir}/chromium-browser/
chmod -x %{buildroot}%{_libdir}/chromium-browser/nacl_irt_*.nexe %{buildroot}%{_libdir}/chromium-browser/nacl_helper_bootstrap*
cp -a chrome %{buildroot}%{_libdir}/chromium-browser/chromium-browser
%if 0%{?sharedbuild}
cp -a lib.target/lib*.so %{buildroot}%{_libdir}/chromium-browser/
cp -a lib.host/lib*.so %{buildroot}%{_libdir}/chromium-browser/
%endif
# If we're building without SELINUX support, uncomment this line.
%if 0%{?selinux}
# Do nothing. Sandboxing is in the selinux policy and core binary.
%else
cp -a chrome_sandbox %{buildroot}%{_libdir}/chromium-browser/chrome-sandbox
%endif
cp -a chrome.1 %{buildroot}%{_mandir}/man1/chrome.1
cp -a chrome.1 %{buildroot}%{_mandir}/man1/chromium-browser.1
mkdir -p %{buildroot}%{_libdir}/chromium-browser/plugins/
popd

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
cp -a %{SOURCE9} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/chromium-browser.svg
# cp -a chrome/app/theme/chromium/product_logo_48.png %{buildroot}%{_datadir}/pixmaps/chromium-browser.png

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE3}

mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps/
cp -a %{SOURCE5} %{buildroot}%{_datadir}/gnome-control-center/default-apps/

# Make the dirtree for managed policies
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/policies/managed/
# Install the master_preferences file
mkdir -p %{buildroot}%{_sysconfdir}/%{name}-browser/
install -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/%{name}-browser/default

%if 0%{?vanillabuild}
# No need to do this.
%else
# This enables HTML5 video if you have ffmpeg installed, you naughty naughty user.
pushd %{buildroot}%{_libdir}/chromium-browser
touch %{buildroot}%{_libdir}/libavcodec.so.52
ln -s %{_libdir}/libavcodec.so.52 libavcodec.so.52
touch %{buildroot}%{_libdir}/libavformat.so.52
ln -s %{_libdir}/libavformat.so.52 libavformat.so.52
touch %{buildroot}%{_libdir}/libavutil.so.50
ln -s %{_libdir}/libavutil.so.50 libavutil.so.50
popd
%endif

%clean
rm -rf %{buildroot}

%pre 
if [ -f /etc/chromium ]; then 
    mv /etc/chromium /etc/chromium.rpmsave
fi

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root,-)
%{_bindir}/chromium-browser
%{_libdir}/chromium-browser/*.pak
%{_libdir}/chromium-browser/chromium-browser
%{_libdir}/chromium-browser/nacl_irt_*.nexe
%{_libdir}/chromium-browser/nacl_helper
%attr(0755,root,root) %{_libdir}/chromium-browser/nacl_helper_bootstrap
# %%{_libdir}/chromium-browser/nacl_helper_bootstrap_munge_phdr
# %%{_libdir}/chromium-browser/nacl_helper_bootstrap_raw
%{_libdir}/chromium-browser/libppGoogleNaClPluginChrome.so
# Uncomment this line if building without SELINUX
%if 0%{?selinux}
# Do nothing. Sandboxing is in the selinux policy and core binary.
%else
# These unique permissions are intentional and necessary for the sandboxing
%attr(4555, root, root) %{_libdir}/chromium-browser/chrome-sandbox
%endif
%{_libdir}/chromium-browser/locales/
%{_libdir}/chromium-browser/plugins/
%{_libdir}/chromium-browser/resources/
# %%{_libdir}/chromium-browser/themes/
%{_mandir}/man1/chrom*
%{_datadir}/icons/hicolor/scalable/apps/chromium-browser.svg
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-control-center/default-apps/chromium-browser.xml
%{_sysconfdir}/%{name}-browser/
%{_sysconfdir}/%{name}/
%if 0%{?sharedbuild}
# Do nothing, we're covered in -libs
%else
%dir %{_libdir}/chromium-browser/
%if 0%{?vanillabuild}
# Don't need em
%else
# These are dummy symlinks. You'll have to install ffmpeg-libs to get them for real.
%{_libdir}/chromium-browser/libavcodec.so.52
%{_libdir}/chromium-browser/libavutil.so.50
%{_libdir}/chromium-browser/libavformat.so.52
%exclude %{_libdir}/libavcodec.so.52
%exclude %{_libdir}/libavutil.so.50
%exclude %{_libdir}/libavformat.so.52
%endif
%endif

%if 0%{?sharedbuild}
%files libs
%defattr(-,root,root,-)
%dir %{_libdir}/chromium-browser/
%if 0%{?vanillabuild}
# Don't	need em
%else
# These are dummy symlinks. You'll have to install ffmpeg-libs to get them for real.
%{_libdir}/chromium-browser/libavcodec.so.52
%{_libdir}/chromium-browser/libavutil.so.50
%{_libdir}/chromium-browser/libavformat.so.52
%endif
# These are real.
%{_libdir}/chromium-browser/liballocator.so
%{_libdir}/chromium-browser/libapp_base.so
%{_libdir}/chromium-browser/libappcache.so
%{_libdir}/chromium-browser/libbase.so
%{_libdir}/chromium-browser/libbase_i18n.so
%{_libdir}/chromium-browser/libbase_static.so
%{_libdir}/chromium-browser/libblob.so
%{_libdir}/chromium-browser/libbrowser.so
%{_libdir}/chromium-browser/libcacheinvalidation.so
%{_libdir}/chromium-browser/libcacheinvalidation_proto_cpp.so
# %{_libdir}/chromium-browser/libchrome_gpu.so
# %{_libdir}/chromium-browser/libchrome_version_info.so
%{_libdir}/chromium-browser/libchromoting_base.so
%{_libdir}/chromium-browser/libchromoting_client.so
%{_libdir}/chromium-browser/libchromoting_host.so
%{_libdir}/chromium-browser/libchromoting_jingle_glue.so
%{_libdir}/chromium-browser/libchromoting_protocol.so
%{_libdir}/chromium-browser/libchromotocol_proto_lib.so
%{_libdir}/chromium-browser/libcld.so
%{_libdir}/chromium-browser/libcommon.so
%{_libdir}/chromium-browser/libcommon_constants.so
%{_libdir}/chromium-browser/libcommon_net.so
%{_libdir}/chromium-browser/libcontent_browser.so
%{_libdir}/chromium-browser/libcontent_common.so
%{_libdir}/chromium-browser/libcontent_gpu.so
%{_libdir}/chromium-browser/libcontent_plugin.so
%{_libdir}/chromium-browser/libcontent_ppapi_plugin.so
%{_libdir}/chromium-browser/libcontent_renderer.so
%{_libdir}/chromium-browser/libcontent_worker.so
%{_libdir}/chromium-browser/libcpu_features.so
%{_libdir}/chromium-browser/libcrcrypto.so
%{_libdir}/chromium-browser/libdatabase.so
%{_libdir}/chromium-browser/libdebugger.so
%{_libdir}/chromium-browser/libdefault_plugin.so
%{_libdir}/chromium-browser/libdiffer_block.so
%{_libdir}/chromium-browser/libdiffer_block_sse2.so
%{_libdir}/chromium-browser/libdynamic_annotations.so
# Note: This is a dummy lib. There isn't any troublesome ffmpeg code in here.
# Unless vanillabuild is set. Then there is.
%{_libdir}/chromium-browser/libffmpeg.so
%{_libdir}/chromium-browser/libfileapi.so
%if 0%{?flac}
# Do nothing. We're using system-y goodness.
%else
%{_libdir}/chromium-browser/libflac.so
%endif
# %{_libdir}/chromium-browser/libgfx.so
%{_libdir}/chromium-browser/libgl.so
%{_libdir}/chromium-browser/libglue.so
%{_libdir}/chromium-browser/libgoogleurl.so
%{_libdir}/chromium-browser/libgtest.so
%{_libdir}/chromium-browser/libharfbuzz.so
# %{_libdir}/chromium-browser/libharfbuzz_interface.so
# %{_libdir}/chromium-browser/libhttp_listen_socket.so
%{_libdir}/chromium-browser/libhttp_server.so
%{_libdir}/chromium-browser/libhunspell.so
%{_libdir}/chromium-browser/libiccjpeg.so
%{_libdir}/chromium-browser/libil.so
%{_libdir}/chromium-browser/libin_memory_url_index_cache_proto_cpp.so
%{_libdir}/chromium-browser/libinstaller_util.so
%{_libdir}/chromium-browser/libipc.so
%if 0%{?jingle}
# Do nothing. We're using system-y goodness.
%else
%{_libdir}/chromium-browser/libjingle.so
%{_libdir}/chromium-browser/libjingle_p2p.so
%endif
%{_libdir}/chromium-browser/libjingle_glue.so
%{_libdir}/chromium-browser/libmedia.so
%{_libdir}/chromium-browser/libmodp_b64.so
# This isn't a shared lib anymore. A shame.
# %{_libdir}/chromium-browser/libnacl.so
%{_libdir}/chromium-browser/libnet.so
%{_libdir}/chromium-browser/libnet_base.so
%{_libdir}/chromium-browser/libnotifier.so
%{_libdir}/chromium-browser/libomx_wrapper.so
%{_libdir}/chromium-browser/libots.so
# %{_libdir}/chromium-browser/libpcre.so
# %{_libdir}/chromium-browser/libplugin.so
%{_libdir}/chromium-browser/libpolicy.so
# %{_libdir}/chromium-browser/libppapi_plugin.so
%{_libdir}/chromium-browser/libprinting.so
%{_libdir}/chromium-browser/libprofile_import.so
# %{_libdir}/chromium-browser/libprotobuf.so
%{_libdir}/chromium-browser/libprotobuf_lite.so
%{_libdir}/chromium-browser/libprotobuf_full_do_not_use.so
%{_libdir}/chromium-browser/libquota.so
%{_libdir}/chromium-browser/librenderer.so
%{_libdir}/chromium-browser/libsandbox.so
%{_libdir}/chromium-browser/libsdch.so
%{_libdir}/chromium-browser/libservice.so
%{_libdir}/chromium-browser/libskia.so
%{_libdir}/chromium-browser/libskia_opts.so
%if 0%{?sqlite}
# Do nothing. We're using system-y goodness.
%else
%{_libdir}/chromium-browser/libsqlite3.so
%endif
%if 0%{?nss}
# Do nothing. We're using system-y goodness.
%else
%{_libdir}/chromium-browser/libssl.so
%endif
# %{_libdir}/chromium-browser/libssl_host_info.so
%{_libdir}/chromium-browser/libsurface.so
%{_libdir}/chromium-browser/libsymbolize.so
%{_libdir}/chromium-browser/libsync.so
%{_libdir}/chromium-browser/libsyncapi.so
%{_libdir}/chromium-browser/libsync_notifier.so
%{_libdir}/chromium-browser/libsync_proto_cpp.so
%{_libdir}/chromium-browser/libtess.so
%{_libdir}/chromium-browser/libtrace_proto_lib.so
%{_libdir}/chromium-browser/libui_base.so
%{_libdir}/chromium-browser/libui_gfx.so
%{_libdir}/chromium-browser/libundoview.so
%{_libdir}/chromium-browser/libutility.so
# %{_libdir}/chromium-browser/libwebcore.so
%{_libdir}/chromium-browser/libwebcore_bindings.so
%{_libdir}/chromium-browser/libwebcore_html.so
%{_libdir}/chromium-browser/libwebcore_platform.so
%{_libdir}/chromium-browser/libwebcore_remaining.so
%{_libdir}/chromium-browser/libwebcore_rendering.so
%{_libdir}/chromium-browser/libwebcore_svg.so
%{_libdir}/chromium-browser/libwebkit.so
%{_libdir}/chromium-browser/libwebkit_gpu.so
%{_libdir}/chromium-browser/libwebkit_user_agent.so
%{_libdir}/chromium-browser/libwebp_dec.so
%{_libdir}/chromium-browser/libwebp_enc.so
# %{_libdir}/chromium-browser/libworker.so
%{_libdir}/chromium-browser/libwtf.so
%{_libdir}/chromium-browser/libxdg_mime.so
%{_libdir}/chromium-browser/libyarr.so
%{_libdir}/chromium-browser/libyuv_convert.so
%{_libdir}/chromium-browser/libyuv_convert_sse2.so
%if 0%{?vanillabuild}
# Do nothing here.
%else
%exclude %{_libdir}/libavcodec.so.52
%exclude %{_libdir}/libavutil.so.50
%exclude %{_libdir}/libavformat.so.52
%endif
%endif

%changelog
* Wed Dec 12 2012 Tom Callaway <spot@fedoraproject.org> 23.0.1271.95-1
- update to 23.0.1271.95

* Tue Sep 11 2012 Tom Callaway <spot@fedoraproject.org> 21.0.1180.89-1
- update to 21.0.1180.89
- (there was an unreleased 21.0.1180.81 update, hence the -ffmpegsumo bits)

* Wed Jul 11 2012 Tom Callaway <spot@fedoraproject.org> 20.0.1132.47-2
- drop -Wdelete-non-virtual-dtor flag (not needed, f16 doesn't even know about it)
- add epoch to v8ver

* Fri Jul  6 2012 Tom Callaway <spot@fedoraproject.org> 20.0.1132.47-1
- update to 20.0.1132.47

* Tue Jun 26 2012 Tom Callaway <spot@fedoraproject.org> 19.0.1084.56-2
- use system jsoncpp, libjingle, webrtc

* Wed Jun 13 2012 Tom Callaway <spot@fedoraproject.org> 19.0.1084.56-1
- update to 19.0.1084.56

* Fri Mar 16 2012 Tom Callaway <spot@fedoraproject.org> 17.0.963.79-1
- update to .79
- fix versioned requires for libjingle

* Mon Feb 20 2012 Tom Callaway <spot@fedoraproject.org> 17.0.963.46-3
- apply upstream webkit fix for jpeg rendering

* Fri Feb 17 2012 Tom Callaway <spot@fedoraproject.org> 17.0.963.46-2
- fixes for gcc 4.7 (f17)

* Tue Feb 14 2012 Tom Callaway <spot@fedoraproject.org> 17.0.963.46-1
- 17.0.963.46

* Sat Feb  4 2012 Tom Callaway <spot@fedoraproject.org> 15.0.874.106-3
- rebuild for libvpx.so.1

* Thu Dec  1 2011 Tom Callaway <spot@fedoraproject.org> 15.0.874.106-2
- add fix for glib on f17

* Wed Nov  2 2011 Tom Callaway <spot@fedoraproject.org> 15.0.874.106-1
- 15.0.874.106

* Mon Sep 26 2011 Tom Callaway <spot@fedoraproject.org> 14.0.835.186-1
- 14.0.835.186

* Thu Jul 21 2011 Tom Callaway <spot@fedoraproject.org> 14.0.827.10-1
- 14.0.827.10

* Mon Jul 11 2011 Tom Callaway <spot@fedoraproject.org> 12.0.742.112-1
- update to 12.0.742.112

* Fri Jun 10 2011 Tom Callaway <spot@fedoraproject.org> 12.0.742.91-1
- update to 12.0.742.91

* Sat May 28 2011 Tom Callaway <spot@fedoraproject.org> 11.0.696.71-1
- update to .71

* Wed May 18 2011 Tom Callaway <spot@fedoraproject.org> 11.0.696.68-1
- update to latest "stable"

* Thu Apr 28 2011 Tom Callaway <spot@fedoraproject.org> 11.0.696.57-1
- Package up the current "stable" build

* Tue Feb 22 2011 Tom Callaway <spot@fedoraproject.org> 11.0.679.0-1
- update to 11.0.679.0

* Tue Jan 11 2011 Tom Callaway <spot@fedoraproject.org> 10.0.634.0-1
- update to 10.0.634.0

* Tue Dec 14 2010 Tom Callaway <spot@fedoraproject.org> 9.0.600.0-2
- fix more NULL issues

* Thu Dec  9 2010 Tom "spot" Callaway <tcallawa@redhat.com> 9.0.600.0-1
- update to 9.0.600.0

* Fri Oct 22 2010 Tom "spot" Callaway <tcallawa@redhat.com> 8.0.560.0-1
- update to 8.0.560.0

* Thu Oct 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> 8.0.553.0-1
- update to 8.0.553.0

* Fri Oct  8 2010 Tom "spot" Callaway <tcallawa@redhat.com> 7.0.542.0-4
- pass -fno-ipa-cp as an optflag with gcc 4.5

* Fri Oct  8 2010 Tom "spot" Callaway <tcallawa@redhat.com> 7.0.542.0-3
- add logic path for vanillabuild FOR DEBUGGING ONLY

* Wed Oct  6 2010 Tom "spot" Callaway <tcallawa@redhat.com> 7.0.542.0-2
- fix system-libvpx patch

* Mon Oct  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> 7.0.542.0-1
- update to 7.0.542.0

* Tue Sep 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> 7.0.522.0-1
- update to 7.0.522.0

* Fri Aug 27 2010 Tom "spot" Callaway <tcallawa@redhat.com> 7.0.506.0-1
- update to 7.0.506.0

* Wed Aug 25 2010 Tom "spot" Callaway <tcallawa@redhat.com> 7.0.504.0-1
- update to 7.0.504.0

* Thu Aug 19 2010 Tom "spot" Callaway <tcallawa@redhat.com> 7.0.500.0-1.20100819svn56724
- update to 7.0.500.0 (svn56724)

* Thu Aug 12 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.491.0-1
- update to 6.0.491.0

* Mon Aug  9 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.488.0-1
- fix chromium-latest.py
- fix chromium-browser.desktop
- update to 6.0.488.0

* Fri Aug  6 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.486.0-2
- Fix NULL errors with gcc45

* Mon Jul 26 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.476.0-2
- more gcc 4.5 fixes

* Mon Jul 26 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.476.0-1
- update to 6.0.476.0

* Mon Jul 19 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.467.0-2
- fix code to compile with gcc 4.5

* Fri Jul 16 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.467.0-1
- update to 6.0.467.0

* Tue Jul  6 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.457.0-1
- update to 6.0.457.0

* Fri Jul  2 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.453.1-1
- update to 6.0.453.1

* Wed Jun 30 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.451.0-2.1
- conditionalize gnome-keyring BR for Fedora 12

* Wed Jun 30 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.451.0-2
- fix code to compile against icu 4.4

* Wed Jun 30 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.451.0-1
- update to 6.0.451.0

* Thu Jun  3 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.425.0-1.20100603svn48849
- update to 6.0.425.0, svn 48849

* Thu May 27 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.417.0-1.20100526svn48276
- update to 6.0.417.0, svn 48276
- conditionalize svncheckout so if it is set, it works, and if unset, it works. :)

* Tue May 25 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.416.0-1.20100525svn48189
- update to 6.0.416.0, svn 48189

* Tue May 25 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.414.0-1
- update to 6.0.414.0

* Thu May 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.412.0-1.20100520svn47812
- update to 6.0.412.0, svn 47812

* Tue May 18 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.406.0-1.2
- include rhel fixes (thanks to mcepl)
- debugging for webgl

* Mon May 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.406.0-1
- update to 6.0.406.0

* Fri May 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.401.1-3
- conditionalize -fPIC as part of the shared build only

* Thu May 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.401.1-2
- conditionalize shared/static build

* Thu May 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.401.1-1
- updated to 6.0.401.1

* Mon May 10 2010 Tom "spot" Callaway <tcallawa@redhat.com> 6.0.399.0-1
- updated to 6.0.399.0

* Tue May  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> 5.0.395.0-1
- move to using cleaned versions of official build tarballs
- disable sse2

* Mon Apr 19 2010 Tom "spot" Callaway <tcallawa@redhat.com> 5.0.382.0-0.1.20100419svn44917
- updated to svn44917

* Tue Apr 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> 5.0.377.0-0.1.20100413svn44349
- updated to svn44349

* Thu Apr  8 2010 Tom "spot" Callaway <tcallawa@redhat.com> 5.0.372.0-0.1.20100408svn43945
- updated to svn43945

* Mon Mar 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> 5.0.365.0-0.1.20100329svn42989
- updated to svn42989

* Mon Mar 22 2010 Tom "spot" Callaway <tcallawa@redhat.com> 5.0.360.0-0.1.20100322svn42211
- updated to svn42211

* Thu Mar 18 2010 Tom "spot" Callaway <tcallawa@redhat.com> 5.0.358.0-0.1.20100318svn41971
- merge useful patches from opensuse build
- build with make, not scons
- smaller source, lzma compressed
- updated to svn41971

* Mon Mar 15 2010 Tom "spot" Callaway <tcallawa@redhat.com> 5.0.355.0-0.1.20100315svn41580
- updated to svn41615

* Thu Feb 18 2010 Tom "spot" Callaway <tcallawa@redhat.com> 5.0.330.0-0.1.20100218svn39394
- updated to svn39394

* Fri Jan 22 2010 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.305.0-0.1.20100122svn36865
- updated to svn36865

* Wed Dec 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.285.0-0.1.20091230svn35370
- updated to svn35370
- hardcode v8 requires on chromium-libs to force clean update

* Mon Dec 21 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.277.0-0.1.20091221svn35107
- 20091221svn35107

* Wed Dec 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.268.0-0.1.20091216svn34775
- 20091216svn34775

* Tue Dec 15 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.268.0-0.1.20091209svn34196
- 20091209svn34196
- rewrite most patches
- nuke second copy of zlib
- build libraries as shared libs
- put shared libs in subpackage (in preparation for courgette subpackage)
- add conditional for verbose mode
- conditional for system-sqlite
- courgette subpackage

* Wed Nov 18 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.252.0-0.1.20091119svn32498
- 20091119svn32498
- add minimal nss requires

* Tue Oct 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.227.0-0.1.20091027svn30269
- 20091027svn30269
- apply hack fix to stop double free bug (http://code.google.com/p/chromium/issues/detail?id=23362)

* Tue Oct 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.222.6-0.1.20091013svn28872
- 20091013svn28872

* Thu Oct  8 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.222.2-0.1.20091008svn28391
- 20091008svn28391

* Wed Sep 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.220.0-0.1.20090930svn27599
- 20090930svn27599

* Tue Sep 29 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.219.8-0.1.20090929svn27489
- 20090929svn27489

* Wed Sep 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.212.0-0.1.20090916svn26424
- 20090916svn26424
- revert http://src.chromium.org/viewvc/chrome/trunk/src/chrome/common/sqlite_utils.cc?r1=24321&r2=25633
  to stop crashes when typing in url bar

* Thu Sep 10 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.208.0-0.1.20090910svn25958
- 20090910svn25958

* Wed Sep 9 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.208.0-0.1.20090909svn25824
- 20090909svn25824
- drop hardcoded Requires on bug-buddy (fixes issue where it is being obsoleted by abrt in rawhide)
- disable webkit deopt, flash bug is fixed now
- use system libicu

* Thu Aug 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.204.0-0.1.20090827svn24640
- 20090827svn24640

* Tue Aug 25 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.203.0-0.1.20090824svn24148
- 20090824svn24148
- find proper plugin dir on x86_64
- pass --enable-user-scripts (instead of old --enable-greasemonkey)

* Tue Aug 18 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.202.0-0.1.20090818svn23628
- 20090818svn23628

* Fri Aug 14 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.202.0-0.1.20090814svn23460
- 20090814svn23460

* Wed Aug 12 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.202.0-0.1.20090812svn23201
- Bump to 4.0.202 (we're not tracking 3.0, no one can tell me exactly how to manage that)

* Mon Aug 10 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.198.0-0.1.20090810svn22925
- 20090810svn22925

* Fri Aug  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.198.0-0.1.20090807svn22807
- 20090807svn22807

* Wed Aug  5 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.198.0-0.1.20090805svn22496
- 20090805svn22496

* Mon Aug  3 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.197.0-0.1.20090803svn22262
- 20090803svn22262

* Fri Jul 31 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.197.0-0.1.20090731svn22188
- 20090731svn22188

* Thu Jul 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.197.0-0.1.20090730svn22105
- 20090730svn22105

* Mon Jul 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.196.0-0.1.20090727svn21648
- 20090727svn21648

* Fri Jul 24 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.196.0-0.1.20090724svn21567
- 20090724svn21567
- drop ffmpeg binaries (only code remaining is headers, doesn't infringe patents)
- package up manpage

* Mon Jul 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.195.0-0.1.20090720svn21073
- 20090720svn21073

* Thu Jul 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.195.0-0.1.20090716svn20889
- 20090716svn20889

* Wed Jul 15 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.195.0-0.1.20090715svn20726
- 20090715svn20726

* Mon Jul 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.194.0-0.1.20090713svn20473
- 20090713svn20473

* Sat Jul 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.194.0-0.1.20090711svn20464
- 20090711svn20464
- fix sandboxing up to match code changes (no longer need to be read-only, doesn't need /var/run/chrome-sandbox)

* Wed Jul  8 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.193.0-0.1.20090708svn20141
- 20090708svn20141
- support LinuxZygote sandboxing

* Sat Jul  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.192.0-0.1.20090704svn19929
- 20090704svn19929
- hack in correct optflags

* Sun Jun 28 2009 Tom "spot" Callaway <tcallawa@redhat.com> 
- 20090628svn19474

* Fri Jun 26 2009 Tom "spot" Callaway <tcallawa@redhat.com>
- 20090626svn19370

* Thu Jun 25 2009 Tom "spot" Callaway <tcallawa@redhat.com> 
- 3.0.191.0 20090625svn19237

* Thu Jun 18 2009 Tom "spot" Callaway <tcallawa@redhat.com>
- 3.0.190.0 20090618svn18706

* Mon Jun 8 2009 Tom "spot" Callaway <tcallawa@redhat.com>
- 20090608svn17870

* Sat Jun 6 2009 Tom "spot" Callaway <tcallawa@redhat.com>
- 20090606svn17834
