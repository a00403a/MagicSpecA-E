Name:      elinks
Summary:   A text-mode Web browser
Summary(zh_CN): 文本模式的网页浏览器
Version:   0.12
Release:   0.20.pre5%{?dist}
License:   GPLv2
URL:       http://elinks.or.cz
Group:     Applications/Internet
Group(zh_CN):	应用程序/互联网
Source:    http://elinks.or.cz/download/elinks-%{version}pre5.tar.bz2
Source2:   elinks.conf
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: automake
BuildRequires: bzip2-devel
BuildRequires: expat-devel
BuildRequires: libidn-devel
BuildRequires: krb5-devel
BuildRequires: nss_compat_ossl-devel >= 0.9.3
BuildRequires: nss-devel
BuildRequires: pkgconfig
Requires: zlib >= 1.2.0.2
Requires(preun): %{_sbindir}/alternatives
Requires(post): coreutils
Requires(post): %{_sbindir}/alternatives
Requires(postun): coreutils
Requires(postun): %{_sbindir}/alternatives
Provides:  webclient
Obsoletes: links < 1:0.97
Provides:  links = 1:0.97-1
Provides: text-www-browser

Patch0: elinks-0.11.0-ssl-noegd.patch
Patch1: elinks-0.10.1-utf_8_io-default.patch
Patch2: elinks-0.10.1-pkgconfig.patch
Patch3: elinks-0.11.0-getaddrinfo.patch
Patch4: elinks-0.11.0-sysname.patch
Patch5: elinks-0.10.1-xterm.patch
Patch6: elinks-0.11.0-union.patch
Patch7: elinks-0.11.3-macropen.patch
Patch8: elinks-scroll.patch
Patch9: elinks-nss.patch
Patch10: elinks-nss-inc.patch

%description
Elinks is a text-based Web browser. Elinks does not display any images,
but it does support frames, tables and most other HTML tags. Elinks'
advantage over graphical browsers is its speed--Elinks starts and exits
quickly and swiftly displays Web pages.

%description -l zh_CN
文本界面的网页浏览器，不支持图像，但支持框架、表格及其它 HTML 标签.

%prep
%setup -q -n %{name}-%{version}pre5

# Prevent crash when HOME is unset (bug #90663).
%patch0 -p1
# UTF-8 by default
%patch1 -p1
%patch2 -p1
# Make getaddrinfo call use AI_ADDRCONFIG.
%patch3 -p1
# Don't put so much information in the user-agent header string (bug #97273).
%patch4 -p1
# Fix xterm terminal: "Linux" driver seems better than "VT100" (#128105)
%patch5 -p1
# Fix #157300 - Strange behavior on ppc64
%patch6 -p1
# fix for open macro in new glibc
%patch7 -p1
#upstream fix for out of screen dialogs
%patch8 -p1
# Port elinks to use NSS library for cryptography (#346861) - accepted upstream
%patch9 -p1
# Port elinks to use NSS library for cryptography (#346861) - incremental patch
%patch10 -p1

%build
./autogen.sh

export CFLAGS="$RPM_OPT_FLAGS $(getconf LFS_CFLAGS) -D_GNU_SOURCE"
%configure %{?rescue:--without-gpm} --without-x --with-gssapi \
  --enable-bittorrent --with-nss_compat_ossl
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/elinks.conf
touch $RPM_BUILD_ROOT%{_bindir}/links
touch $RPM_BUILD_ROOT%{_mandir}/man1/links.1.gz
%find_lang elinks

%postun
if [ "$1" -ge "1" ]; then
	links=`readlink %{_sysconfdir}/alternatives/links`
	if [ "$links" == "%{_bindir}/elinks" ]; then
		%{_sbindir}/alternatives --set links %{_bindir}/elinks
	fi
fi
exit 0

%post
#Set up alternatives files for links
%{_sbindir}/alternatives --install %{_bindir}/links links %{_bindir}/elinks 90 \
  --slave %{_mandir}/man1/links.1.gz links-man %{_mandir}/man1/elinks.1.gz
links=`readlink %{_sysconfdir}/alternatives/links`
if [ "$links" == "%{_bindir}/elinks" ]; then
	%{_sbindir}/alternatives --set links %{_bindir}/elinks
fi


%preun
if [ $1 = 0 ]; then
	%{_sbindir}/alternatives --remove links %{_bindir}/elinks
fi
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files -f elinks.lang
%defattr(-,root,root,-)
%doc README SITES TODO COPYING
%ghost %verify(not md5 size mtime) %{_bindir}/links
%{_bindir}/elinks
%ghost %verify(not md5 size mtime) %{_mandir}/man1/links.1.gz
%config(noreplace) %{_sysconfdir}/elinks.conf
%{_mandir}/man1/elinks.1*
%{_mandir}/man5/*

%changelog

