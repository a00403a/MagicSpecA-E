# emacs packaging macros
%if %($(pkg-config emacs) ; echo $?)
%define emacs_version 22.1
%define emacs_lispdir %{_datadir}/emacs/site-lisp
%define emacs_startdir %{_datadir}/emacs/site-lisp/site-start.d
%else
%define emacs_version %(pkg-config emacs --modversion)
%define emacs_lispdir %(pkg-config emacs --variable sitepkglispdir)
%define emacs_startdir %(pkg-config emacs --variable sitestartdir)
%endif


Summary: Converts text and other types of files to PostScript(TM)
Summary(zh_CN.UTF-8): 转换文本或其它类型的文件到PostScript(TM)。
Name: a2ps
Version: 4.14
Release: 2%{?dist}
License: GPLv3+
Group: Applications/Publishing
Group(zh_CN.UTF-8): 应用程序/出版
Source0: http://ftp.gnu.org/gnu/a2ps/%{name}-%{version}.tar.gz
Source1: ftp://ftp.enst.fr/pub/unix/a2ps/i18n-fonts-0.1.tar.gz
Patch0: a2ps-4.13-conf.patch
Patch1: a2ps-4.13-etc.patch
Patch3: a2ps-4.13-security.patch
Patch4: a2ps-4.13-glibcpaper.patch
Patch7: a2ps-sort.patch
Patch8: a2ps-iso5-minus.patch
Patch9: a2ps-perl.patch
# EUC-JP support
Patch10: a2ps-4.13-eucjp.patch
Patch11: a2ps-4.13-autoenc.patch
Patch12: a2ps-4.13b-attr.patch
Patch13: a2ps-4.13b-numeric.patch
Patch14: a2ps-4.13b-encoding.patch
Patch15: a2ps-4.13b-tilde.patch
Patch17: a2ps-4.13-euckr.patch
Patch18: a2ps-4.13-gnusource.patch
Patch20: a2ps-4.13-hebrew.patch
Patch26: a2ps-make-fonts-map.patch
Patch28: a2ps-wdiff.patch
Patch29: a2ps-U.patch
Patch31: a2ps-mb.patch
Patch34: a2ps-external-libtool.patch
Patch35: a2ps-4.14-texinfo-nodes.patch
Requires: fileutils sh-utils info
BuildRequires: gperf
BuildRequires: emacs, emacs-el, flex, libtool, texinfo, groff
BuildRequires: ImageMagick
BuildRequires: groff-perl
BuildRequires: cups
BuildRequires: gettext, bison
BuildRequires: psutils, texlive-dvips, texinfo, texlive-latex, html2ps
# instead of gv, xdg-open should certainly be used
#BuildRequires: gv
Url: http://www.gnu.org/software/a2ps/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: psutils, ImageMagick, texinfo-tex, gzip, bzip2, groff-perl
Requires: tetex-dvips, tetex-latex, tetex-fonts, file, html2ps
# for hebrew support, path set. 
# culmus-fonts
# And certainly other font sets for other languages may be needed
Requires(post): coreutils
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Obsoletes: a2ps-i18n <= 0.1-1
Provides: a2ps-i18n = 0.1-2


%package -n emacs-%{name}
Summary: Emacs bindings for a2ps files
Summary(zh_CN.UTF-8): a2ps 文件的 Emacs 绑定
Group: Applications/Editors
Group(zh_CN.UTF-8): 应用程序/编辑器
Requires: emacs(bin) >= %{emacs_version}


%package -n emacs-%{name}-el
Summary: Elisp source files for emacs-%{name} under GNU Emacs
Summary(zh_CN.UTF-8): 在 GNU Emacs 下的 emacs-%{name} 的 elisp 源文件
Group: Applications/Editors
Group(zh_CN.UTF-8): 应用程序/编辑器
Requires:       emacs-%{name} = %{version}-%{release}


%description
The a2ps filter converts text and other types of files to PostScript(TM).
A2ps has pretty-printing capabilities and includes support for a wide
number of programming languages, encodings (ISO Latins, Cyrillic, etc.),
and medias.

%description -l zh_CN.UTF-8
A2ps过滤器转换文本或其它类型的文件到PostScript(TM)。
A2ps有完美的可打印能力并且包括了对程序语言、编码(ISO Latins, Cyrillic等)
和媒体的广泛支持。

%description -n emacs-%{name}
Postscript printing hook for a2ps and major mode for a2ps style sheets
for emacs.

%description -n emacs-%{name} -l zh_CN.UTF-8
emacs 的 a2ps 和 a2ps 样式表的主模式的 Postscript 打印钩子。

%description -n emacs-%{name}-el
This package contains the elisp source files for emacs-%{name} under GNU 
Emacs. You do not need to install this package to run emacs-%{name}. Install 
the emacs-%{name} package to use emacs-%{name} with GNU Emacs.

%description -n emacs-%{name}-el -l zh_CN.UTF-8
这个包包含了在 GNU Emacs 下的 emacs-%{name} 的 elisp 源文件。
你要运行 emacs-%{name} 的话不需要安装这个包。

%prep
%setup -q -a 1

# use fedora postscript font paths
%patch0 -p1 -b .conf

# add /etc/a2ps in directories searched for config files
%patch1 -p1 -b .etc 

%patch3 -p1 -b .security
%patch4 -p1 -b .glibcpaper
%patch7 -p1 -b .sort
%patch8 -p1 -b .iso5-minus
%patch9 -p1 -b .perl

%patch10 -p1 -b .euc
%patch11 -p1 -b .ae
%patch12 -p1 -b .attr

# Use C locale's decimal point style (bug #53715).
%patch13 -p1 -b .numeric

# Use locale to determine a sensible default encoding (bug #64584).
%patch14 -p1 -b .encoding

# Fix koi8 tilde (bug #66393).
%patch15 -p1 -b .tilde

# Add Korean resource file (bug #81421).
%patch17 -p1 -b .euckr

# Prevent strsignal segfaulting (bug #104970).
%patch18 -p1 -b .gnusource

# Hebrew support (bug #113191).
%patch20 -p1 -b .hebrew

# Use external libtool (bug #225235).
%patch34 -p1 -b .external-libtool

# Fix problems in make_fonts_map script (bug #142299).  Patch from
# Michal Jaegermann.
%patch26 -p1 -b .make-fonts-map

# Make pdiff default to not requiring wdiff (bug #68537).
%patch28 -p1 -b .wdiff

# Make pdiff use diff(1) properly (bug #156916).
%patch29 -p1 -b .U

# Fixed multibyte handling (bug #212154).
%patch31 -p1 -b .mb

# Remove dots in node names, patch from Vitezslav Crhonek (Bug #445971)
%patch35 -p1 -b .nodes

for file in AUTHORS ChangeLog; do
  iconv -f latin1 -t UTF-8 < $file > $file.utf8
  touch -c -r $file $file.utf8
  mv $file.utf8 $file
done

mv doc/encoding.texi doc/encoding.texi.utf8
iconv -f KOI-8 -t UTF-8 doc/encoding.texi.utf8 -o doc/encoding.texi

# Fix reference to a2ps binary (bug #112930).
sed -i -e "s,/usr/local/bin,%{_bindir}," contrib/emacs/a2ps.el

chmod -x lib/basename.c lib/xmalloc.c

# restore timestamps of patched files
touch -c -r configure.in.conf configure.in
touch -c -r config.h.in.euc config.h.in
touch -c -r configure.conf configure
touch -c -r src/Makefile.am.euc src/Makefile.am
touch -c -r etc/Makefile.am.etc etc/Makefile.am
#touch -c -r fonts/Makefile.in src/Makefile.in lib/Makefile.in
touch -c -r etc/Makefile.in.etc etc/Makefile.in

chmod 644 encoding/iso8.edf.hebrew
chmod 644 encoding/euc-kr.edf.euckr

%build
# preset the date in README.in to avoid the timestamp of the build time
sed -e "s!@date@!`date -r NEWS`!" etc/README.in > etc/README.in.tmp
touch -c -r etc/README.in etc/README.in.tmp
mv etc/README.in.tmp etc/README.in

EMACS=emacs %configure \
  --with-medium=_glibc \
  --enable-kanji

# Remove prebuilt info files to force regeneration at build time
find . -name "*.info*" -exec rm -f {} \;
# force rebuilding scanners by flex - patched or not
find src lib -name '*.l' -exec touch {} \;
# these scanners use 'lineno' - incompatible with -CFe flex flags
#(
#    cd src
#    /bin/sh ../auxdir/ylwrap "flex" sheets-map.l lex.yy.c sheets-map.c --
#    /bin/sh ../auxdir/ylwrap "flex" lexssh.l lex.yy.c lexssh.c --
#    cd ../lib
#    /bin/sh ../auxdir/ylwrap "flex" lexppd.l lex.yy.c lexppd.c --
#)

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install INSTALL='install -p'

# reset the timestamp for the generated etc/README file
touch -r etc/README.in %{buildroot}%{_datadir}/a2ps/README

mkdir -p %{buildroot}%{_sysconfdir}/a2ps

mkdir -p %{buildroot}%{_datadir}/a2ps/{afm,fonts}
pushd i18n-fonts-0.1/afm
install -p -m 0644 *.afm %{buildroot}%{_datadir}/a2ps/afm
pushd ../fonts
install -p -m 0644 *.pfb %{buildroot}%{_datadir}/a2ps/fonts
popd
popd

# Don't ship the library file or header (bug #203536).
rm %{buildroot}%{_libdir}/*.{so,a,la}
rm %{buildroot}%{_includedir}/*

rm -f %{buildroot}%{_infodir}/dir

magic_rpm_clean.sh
%find_lang %name || touch %{name}.lang

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/%{name}-%{version}

%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
/sbin/install-info %{_infodir}/ogonkify.info %{_infodir}/dir || :
/sbin/install-info %{_infodir}/regex.info %{_infodir}/dir || :
(cd %{_datadir}/a2ps/afm;
 ./make_fonts_map.sh > /dev/null 2>&1 || /bin/true
 if [ -f fonts.map.new ]; then
   mv fonts.map.new fonts.map
 fi
)
exit 0

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
   /sbin/install-info --delete %{_infodir}/ogonkify.info %{_infodir}/dir || :
   /sbin/install-info --delete %{_infodir}/regex.info %{_infodir}/dir || :
fi
exit 0

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_sysconfdir}/a2ps
%config %{_sysconfdir}/a2ps.cfg
%config(noreplace) %{_sysconfdir}/a2ps-site.cfg
%doc AUTHORS ChangeLog COPYING NEWS README TODO THANKS
%{_bindir}/*
%{_infodir}/a2ps.info*
%{_infodir}/ogonkify.info*
%{_infodir}/regex.info*
%{_mandir}/*/*
# automatically regenerated at install and update time
%verify(not size mtime md5) %{_datadir}/a2ps/afm/fonts.map
%{_datadir}/a2ps/afm/*.afm
%{_datadir}/a2ps/afm/make_fonts_map.sh
%{_datadir}/a2ps/README
%{_datadir}/a2ps/encoding
%{_datadir}/a2ps/fonts
%{_datadir}/a2ps/ppd
%{_datadir}/a2ps/ps
%{_datadir}/a2ps/sheets
%{_datadir}/ogonkify/
%dir %{_datadir}/a2ps/afm
%dir %{_datadir}/a2ps
%{_libdir}/*.so*

%files -n emacs-%{name}
%defattr(-,root,root,-)
%{emacs_lispdir}/*.elc

%files -n emacs-%{name}-el
%defattr(-,root,root,-)
%{emacs_lispdir}/*.el

%changelog
* Thu Oct 30 2008 Liu Di <liudidi@gmail.com> - 4.14-1mgc25
- 从 fc 的 srpm 中重建
