# Expected failures in mock, hangs in koji
%bcond_with tests

Name:           bash-completion
Version:        1.3
Release:        6%{?dist}
Epoch:          1
Summary:        Programmable completion for Bash
Summary(zh_CN.UTF-8): Bash 的可编程补全
Group:          System Environment/Shells
Group(zh_CN.UTF-8):     系统环境/外壳
License:        GPLv2+
URL:            http://bash-completion.alioth.debian.org/
Source0:        http://bash-completion.alioth.debian.org/files/%{name}-%{version}.tar.bz2
Source1:        %{name}-plague-client
Source2:        CHANGES.package.old
# https://bugzilla.redhat.com/677446
Source3:        %{name}-1.3-filedir.bash
# Non-upstream: adjust helpers dir location to our modified layout
Patch0:         %{name}-1.3-helpersdir.patch
# Non-upstream: see comments in patch
Patch1:         %{name}-1.3-yeswehave.patch
# http://anonscm.debian.org/gitweb/?p=bash-completion/bash-completion.git;a=commitdiff;h=d066ace
Patch2:         %{name}-1.3-gendiff.patch
# http://anonscm.debian.org/gitweb/?p=bash-completion/bash-completion.git;a=commitdiff;h=f1b9580
Patch3:         %{name}-1.3-manpager-689180.patch
# http://anonscm.debian.org/gitweb/?p=bash-completion/bash-completion.git;a=commitdiff;h=e10848b
Patch4:         %{name}-1.3-libreoffice-692548.patch
# http://anonscm.debian.org/gitweb/?p=bash-completion/bash-completion.git;a=commitdiff;h=2eb713f
Patch5:         %{name}-1.3-latexdbj-678122.patch
# http://anonscm.debian.org/gitweb/?p=bash-completion/bash-completion.git;a=commitdiff;h=75309e9
Patch6:         %{name}-1.3-xspec-726220.patch
# http://anonscm.debian.org/gitweb/?p=bash-completion/bash-completion.git;a=commitdiff;h=d74e169
Patch7:         %{name}-1.3-selfparse-479936.patch
# http://anonscm.debian.org/gitweb/?p=bash-completion/bash-completion.git;a=commitdiff;h=e7b3abf
Patch8:         %{name}-1.3-sum-717341.patch
# http://anonscm.debian.org/gitweb/?p=bash-completion/bash-completion.git;a=commitdiff;h=525d6e7
Patch9:         bash-completion-1.3-profile-hook.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
%if %{with tests}
BuildRequires:  dejagnu
BuildRequires:  screen
BuildRequires:  tcllib
%endif
%if 0%{?fedora} || 0%{?rhel} > 5
# For Patch7
Requires:       bash >= 4
%else
Requires:       bash >= 3.2
%endif
# For symlinking in triggers, #490768
Requires:       coreutils

%description
bash-completion is a collection of shell functions that take advantage
of the programmable completion feature of bash.

%description -l zh_CN.UTF-8
bash-completion 是一组 shell 函数集合，它可以给 bash 2 添加可编程的
命令补全。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%if 0%{?fedora} || 0%{?rhel} > 5
# bash >= 4 only
%patch7 -p1
%endif
%patch8 -p1
%patch9 -p1
install -pm 644 %{SOURCE2} .


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT %{name}-files.list
make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d

# Updated completions shipped upstream:
rm cowsay

# Combine to per-package files to work around #585384:
( echo ; cat update-alternatives ) >> chkconfig
rm update-alternatives
( echo ; cat sysctl ) >> procps
rm sysctl
( echo ; cat chsh ; echo ; cat mount ; echo ; cat rtcwake ) >> util-linux
rm chsh mount rtcwake
( echo ; cat xmodmap ; echo ; cat xrandr ; echo ; cat xrdb ) >> xhost
mv xhost xorg-x11-server-utils ; rm xmodmap xrandr xrdb

# Not applicable to Fedora and derivatives:
rm apache2ctl
rm apt-build
rm aptitude
rm cardctl
rm heimdal
rm kldload
rm lilo
rm links
rm lintian
rm pkg_install
rm pkgtools
rm portupgrade
rm reportbug
rm sysv-rc

# Not handled due to other reasons (e.g. no known packages) (yet?):
rm larch
rm p4

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
mv * $RPM_BUILD_ROOT%{_datadir}/%{name}
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{name}/plague-client

# Always installed (not triggered) completions for practically always
# installed packages or non-triggerable common ones:
for f in bash-builtins configure coreutils dd getent iconv ifupdown \
    module-init-tools rpm service sh util-linux ; do
    mv $RPM_BUILD_ROOT%{_datadir}/%{name}/$f .
done
install -pm 644 %{SOURCE3} redefine_filedir

cd - # $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d

%if 0%{?rhel} == 5
 # mock >= 1.1.1, subversion >= 1.6.5-2, yum-utils >= 1.1.24, yum >= 3.2.25-2
install -pm 644 completions/_{mock,subversion,yum-utils,yum} \
    $RPM_BUILD_ROOT%{_datadir}/%{name}
%endif

# file list
filelist=$(pwd)/%{name}-files.list
cd $RPM_BUILD_ROOT%{_datadir}/%{name}
for f in * ; do
    [ $f = helpers ] && continue
    ln -s %{_datadir}/%{name}/$f $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
    echo "%ghost %{_sysconfdir}/bash_completion.d/$f" >> $filelist
    echo "%{_datadir}/%{name}/$f" >> $filelist
done
cd - # $RPM_BUILD_ROOT%{_datadir}/%{name}

# avoid dependency on perl (will only be invoked if perl is installed)
chmod -x $RPM_BUILD_ROOT%{_datadir}/%{name}/helpers/perl


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


%clean
rm -rf $RPM_BUILD_ROOT


# Note that this *must* be %%define, not %%global, otherwise the %%{?2}/%%{!?2}
# conditional is apparently evaluated too early (at spec parse time when arg 2
# is never defined)?
%define bashcomp_trigger() \
%if 0%{?fedora} || 0%{?rhel} > 5\
%triggerin -p <lua> -- %{?2}%{!?2:%1}\
if not posix.access("%{_sysconfdir}/bash_completion.d/%1") then\
    posix.symlink("%{_datadir}/%{name}/%1",\
                  "%{_sysconfdir}/bash_completion.d/%1")\
end\
%else\
%triggerin -- %{?2}%{!?2:%1}\
[ -e %{_sysconfdir}/bash_completion.d/%1 ] || \\\
    ln -s %{_datadir}/%{name}/%1 %{_sysconfdir}/bash_completion.d || :\
%endif\
%triggerun -- %{?2}%{!?2:%1}\
[ $2 -gt 0 ]%{?3: || [ -x %3 ]}%{?4: || [ -x %4 ]}%{?5: || [ -x %5 ]} || \\\
    rm -f %{_sysconfdir}/bash_completion.d/%1 || :\
%{nil}

%bashcomp_trigger abook
%bashcomp_trigger ant
%bashcomp_trigger apt
%bashcomp_trigger aptitude
%bashcomp_trigger aspell
%bashcomp_trigger autoconf
%bashcomp_trigger automake
%bashcomp_trigger autorpm
%bashcomp_trigger bind-utils
%bashcomp_trigger bitkeeper
%bashcomp_trigger bittorrent
%bashcomp_trigger bluez
%bashcomp_trigger brctl bridge-utils
%bashcomp_trigger bzip2
%bashcomp_trigger cfengine
%bashcomp_trigger chkconfig
%bashcomp_trigger cksfv
%bashcomp_trigger clisp
%bashcomp_trigger cpan2dist perl-CPANPLUS
%bashcomp_trigger cpio
%bashcomp_trigger crontab cronie,vixie-cron %{_bindir}/crontab
%bashcomp_trigger cryptsetup cryptsetup-luks
%bashcomp_trigger cups
%bashcomp_trigger cvs
%bashcomp_trigger cvsps
%bashcomp_trigger dhclient
%bashcomp_trigger dict dictd
%bashcomp_trigger dpkg
%bashcomp_trigger dselect
%bashcomp_trigger dsniff
%bashcomp_trigger dvd+rw-tools
%bashcomp_trigger e2fsprogs
%bashcomp_trigger findutils
%bashcomp_trigger freeciv
%bashcomp_trigger freerdp
%bashcomp_trigger fuse
%bashcomp_trigger gcc
%bashcomp_trigger gcl
%bashcomp_trigger gdb
%bashcomp_trigger genisoimage
%bashcomp_trigger gkrellm
%bashcomp_trigger gnatmake gcc-gnat
%bashcomp_trigger gpg gnupg
%bashcomp_trigger gpg2 gnupg2
%bashcomp_trigger gzip
%bashcomp_trigger hping2 hping3
%bashcomp_trigger imagemagick ImageMagick
%bashcomp_trigger iftop
%bashcomp_trigger info
%bashcomp_trigger ipmitool
%bashcomp_trigger iproute2 iproute
%bashcomp_trigger ipsec openswan
%bashcomp_trigger iptables
%bashcomp_trigger ipv6calc
%bashcomp_trigger isql unixODBC
%bashcomp_trigger jar java-1.6.0-openjdk-devel
%bashcomp_trigger java java-1.6.0-openjdk
%bashcomp_trigger k3b
%bashcomp_trigger ldapvi
%bashcomp_trigger lftp
%bashcomp_trigger lisp cmucl
%bashcomp_trigger lrzip
%bashcomp_trigger lsof
%bashcomp_trigger lvm lvm2
%bashcomp_trigger lzma xz-lzma-compat
%bashcomp_trigger lzop
%bashcomp_trigger mailman
%bashcomp_trigger make
%bashcomp_trigger man man-db,man %{_bindir}/man
%bashcomp_trigger mc
%bashcomp_trigger mcrypt
%bashcomp_trigger mdadm
%bashcomp_trigger medusa
%bashcomp_trigger minicom
%bashcomp_trigger mkinitrd

%if 0%{?rhel} == 5
%triggerin -- mock
if [ -e %{_sysconfdir}/bash_completion.d/mock.bash ] ; then
    # Upstream completion in mock >= 1.1.1
    rm -f %{_sysconfdir}/bash_completion.d/_mock || :
elif [ ! -e %{_sysconfdir}/bash_completion.d/_mock ] ; then
    ln -s %{_datadir}/%{name}/_mock %{_sysconfdir}/bash_completion.d || :
fi
%triggerun -- mock
[ $2 -gt 0 ] || rm -f %{_sysconfdir}/bash_completion.d/_mock || :
%endif

%bashcomp_trigger monodevelop
%bashcomp_trigger mplayer
%bashcomp_trigger msynctool
%bashcomp_trigger mtx
%bashcomp_trigger munin-node
%bashcomp_trigger mutt
%bashcomp_trigger mysqladmin mysql,MySQL-client-community %{_bindir}/mysqladmin
%bashcomp_trigger ncftp
%bashcomp_trigger net-tools
%bashcomp_trigger nmap
%bashcomp_trigger ntpdate
%bashcomp_trigger open-iscsi iscsi-initiator-utils
%bashcomp_trigger openldap openldap-clients
%bashcomp_trigger openssl
%bashcomp_trigger perl
%bashcomp_trigger pine
%bashcomp_trigger pkg-config pkgconfig
%bashcomp_trigger plague-client
%bashcomp_trigger pm-utils
%bashcomp_trigger postfix
%bashcomp_trigger postgresql
%bashcomp_trigger povray
%bashcomp_trigger procps
%bashcomp_trigger python
%bashcomp_trigger qdbus qt,kdelibs3,kdelibs %{_bindir}/qdbus %{_bindir}/dcop
%bashcomp_trigger qemu
%bashcomp_trigger quota-tools quota
%bashcomp_trigger rcs
%bashcomp_trigger rdesktop
%bashcomp_trigger resolvconf
%bashcomp_trigger rfkill
%bashcomp_trigger ri ruby-ri
%bashcomp_trigger rpcdebug nfs-utils
%bashcomp_trigger rpmcheck
%bashcomp_trigger rrdtool
%bashcomp_trigger rsync
%bashcomp_trigger samba samba-common
%bashcomp_trigger sbcl
%bashcomp_trigger screen
%bashcomp_trigger shadow shadow-utils
%bashcomp_trigger sitecopy
%bashcomp_trigger smartctl smartmontools
%bashcomp_trigger snownews
%bashcomp_trigger sqlite3 sqlite
%bashcomp_trigger ssh openssh-clients
%bashcomp_trigger sshfs fuse-sshfs
%bashcomp_trigger strace

%if 0%{?rhel} == 5
%triggerin -- subversion
if [ -e %{_sysconfdir}/bash_completion.d/subversion ] ; then
    # Upstream completion in subversion >= 1.6.5-2
    rm -f %{_sysconfdir}/bash_completion.d/_subversion || :
elif [ ! -e %{_sysconfdir}/bash_completion.d/_subversion ] ; then
    ln -s %{_datadir}/%{name}/_subversion %{_sysconfdir}/bash_completion.d || :
fi
%triggerun -- subversion
[ $2 -gt 0 ] || rm -f %{_sysconfdir}/bash_completion.d/_subversion || :
%endif

%bashcomp_trigger svk perl-SVK
%bashcomp_trigger sysbench
%bashcomp_trigger tar
%bashcomp_trigger tcpdump
%bashcomp_trigger unace
%bashcomp_trigger unrar
%bashcomp_trigger vncviewer tigervnc,vnc %{_bindir}/vncviewer
%bashcomp_trigger vpnc
%bashcomp_trigger wireless-tools
%bashcomp_trigger wodim
%bashcomp_trigger wol
%bashcomp_trigger wtf bsd-games
%bashcomp_trigger wvdial
%bashcomp_trigger xm xen
%bashcomp_trigger xmllint libxml2
%bashcomp_trigger xmlwf expat
%bashcomp_trigger xmms
%bashcomp_trigger xorg-x11-server-utils
%bashcomp_trigger xsltproc libxslt
%bashcomp_trigger xz
%bashcomp_trigger yp-tools

%if 0%{?rhel} == 5
%triggerin -- yum
if [ -e %{_sysconfdir}/bash_completion.d/yum.bash ] ; then
    # Upstream completion in yum >= 3.2.25-2
    rm -f %{_sysconfdir}/bash_completion.d/_yum || :
elif [ ! -e %{_sysconfdir}/bash_completion.d/_yum ] ; then
    ln -s %{_datadir}/%{name}/_yum %{_sysconfdir}/bash_completion.d || :
fi
%triggerun -- yum
[ $2 -gt 0 ] || rm -f %{_sysconfdir}/bash_completion.d/_yum || :

%triggerin -- yum-utils
if [ -e %{_sysconfdir}/bash_completion.d/yum-utils.bash ] ; then
    # Upstream completion in yum-utils >= 1.1.24
    rm -f %{_sysconfdir}/bash_completion.d/_yum-utils || :
elif [ ! -e %{_sysconfdir}/bash_completion.d/_yum-utils ] ; then
    ln -s %{_datadir}/%{name}/_yum-utils %{_sysconfdir}/bash_completion.d || :
fi
%triggerun -- yum-utils
[ $2 -gt 0 ] || rm -f %{_sysconfdir}/bash_completion.d/_yum-utils || :
%endif

%bashcomp_trigger yum-arch


%files -f %{name}-files.list
%defattr(-,root,root,-)
%doc AUTHORS CHANGES CHANGES.package.old COPYING README TODO
%config(noreplace) %{_sysconfdir}/profile.d/bash_completion.sh
%{_sysconfdir}/bash_completion
%dir %{_sysconfdir}/bash_completion.d/
%{_sysconfdir}/bash_completion.d/bash-builtins
%{_sysconfdir}/bash_completion.d/configure
%{_sysconfdir}/bash_completion.d/coreutils
%{_sysconfdir}/bash_completion.d/dd
%{_sysconfdir}/bash_completion.d/getent
%{_sysconfdir}/bash_completion.d/iconv
%{_sysconfdir}/bash_completion.d/ifupdown
%{_sysconfdir}/bash_completion.d/module-init-tools
%{_sysconfdir}/bash_completion.d/redefine_filedir
%{_sysconfdir}/bash_completion.d/rpm
%{_sysconfdir}/bash_completion.d/service
%{_sysconfdir}/bash_completion.d/sh
%{_sysconfdir}/bash_completion.d/util-linux
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/helpers/
%attr(755,root,root) %{_datadir}/%{name}/helpers/perl


%changelog

