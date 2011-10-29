%define use_utf8_dict 1
%define pkg  anthy

Name:  anthy
Version: 9100h
Release: 17%{?dist}
# The entire source code is LGPLv2+ and dictionaries is GPLv2.
License: LGPLv2+ and GPLv2
URL:  http://sourceforge.jp/projects/anthy/
BuildRequires: emacs
%if 0%{?rhel} == 0
BuildRequires: xemacs
%endif

Source0: http://osdn.dl.sourceforge.jp/anthy/37536/anthy-%{version}.tar.gz
Source1: anthy-init.el
Patch0:  anthy-fix-typo-in-dict.patch
Patch1:  anthy-fix-typo-in-dict-name.patch
Patch10: anthy-corpus.patch

Summary: Japanese character set input library
Summary(zh_CN.UTF-8): 日文字符设置输入库
Group:  System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description
Anthy provides the library to input Japanese on the applications, such as
X applications and emacs. and the user dictionaries and the users information
which is used for the conversion, is stored into their own home directory.
So Anthy is secure than other conversion server.

%description -l zh_CN.UTF-8
Anthy 提供了一个在应用程序，比如 X 程序和 emacs 上输入日文的库。
用户字典和用来转换的用户信息，存储在自己的家目录，所以它比其它的
转换服务更安全。

%package devel
Summary: Header files and library for developing programs which uses Anthy
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:  Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: anthy = %{version}-%{release}
Requires: pkgconfig

%description devel
The anthy-devel package contains the development files which is needed to build
the programs which uses Anthy.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n emacs-%{pkg}
Summary: Compiled elisp files to run Anthy under GNU Emacs
Summary(zh_CN.UTF-8): 编译好的在 GNU Emacs 上运行 Anthy 的 elisp 文件
Group:  System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: emacs(bin) >= %{_emacs_version}
Requires: anthy = %{version}-%{release}
BuildArch: noarch

%description -n emacs-%{pkg}
This package contains the byte compiled elisp packages to run Anthy with GNU
Emacs.

%description -n emacs-%{pkg} -l zh_CN.UTF-8
编译好的在 GNU Emacs 上运行 Anthy 的 elisp 文件。

%package -n emacs-%{pkg}-el
Summary: Elisp source files for Anthy under GNU Emacs
Summary(zh_CN.UTF-8): GNU Emacs 上的 Anthy 的 Elisp 源代码
Group:  System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: emacs-%{pkg} = %{version}-%{release}
BuildArch: noarch

%description -n emacs-%{pkg}-el
This package contains the elisp source files for Anthy under GNU Emacs. You
do not need to install this package to run Anthy. Install the emacs-%{pkg}
package to use Anthy with GNU Emacs.

%description -n emacs-%{pkg}-el -l zh_CN.UTF-8
GNU Emacs 上的 Anthy 的 Elisp 源代码。

# 在 RHEL 上有 xemacs，暂时不编译
%if 0%{?rhel} == 0
%package -n xemacs-%{pkg}
Summary: Compiled elisp files to run Anthy under XEmacs
Summary(zh_CN.UTF-8): XEmacs 上运行的 Anthy 的编译好的 elisp 文件
Group:  System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: xemacs(bin) >= %{_xemacs_version}
Requires: anthy = %{version}-%{release}
BuildArch: noarch

%description -n xemacs-%{pkg}
This package contains the byte compiled elisp packages to use Anthy with
XEmacs.

%description -n xemacs-%{pkg} -l zh_CN.UTF-8
XEmacs 上运行的 Anthy 的编译好的 elisp 文件。

%package -n xemacs-%{pkg}-el
Summary: Elisp source files for Anthy under XEmacs
Summary(zh_CN.UTF-8): XEmacs 下的 Anthy 的 Elisp 源代码
Group:  System Environment/Libraries
Group(zh_CN): 系统环境/库
Requires: xemacs-%{pkg} = %{version}-%{release}
BuildArch: noarch

%description -n xemacs-%{pkg}-el
This package contains the elisp source files for Anthy under XEmacs. You do
not need to install this package to run Anthy. Install the xemacs-%{pkg}
package to use Anthy with XEmacs.

%description -n xemacs-%{pkg}-el -l zh_CN.UTF-8
XEmacs 下的 Anthy 的 Elisp 源代码。
%endif


%prep
%setup -q #-a 2
%patch0 -p1 -b .0-typo
%patch1 -p1 -b .1-typo-name
%patch10 -p1 -b .10-corpus

# Convert to utf-8
for file in ChangeLog doc/protocol.txt; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%if %{use_utf8_dict}
function normalize_extra_dict() {
 sed -e 's/^\([^  ]*\)t[  ]*\(#[A-Z0-9\*]*\)[  ]*\([^  ]*\)$/\1 \2 \3/g' $1 > $1.norm
}
function dict_conv() {
 iconv -f euc-jp -t utf-8 $1 > $1.utf8
}
function gen_dict_args() {
 if ! test -f $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in-orig; then
  cp -a $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in{,-orig}
 fi
 cat <<_EOF_ > $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in
# Generated by rpm script
set_input_encoding utf8
read @top_srcdir@/alt-cannadic/gcanna.ctd.utf8
read @top_srcdir@/alt-cannadic/gcannaf.ctd.utf8
read @top_srcdir@/alt-cannadic/gtankan.ctd.utf8
read @top_srcdir@/alt-cannadic/extra/g-jiritu-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gc-fullname-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gt-tankanji_kanji-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gt-tankanji_hikanji-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gf-fuzoku-34.t.norm
read @top_srcdir@/mkworddic/adjust.t.utf8
read @top_srcdir@/mkworddic/compound.t.utf8
read @top_srcdir@/mkworddic/extra.t.utf8
read @top_srcdir@/alt-cannadic/g_fname.t
#
build_reverse_dict
set_dict_encoding utf8
read_uc @top_srcdir@/mkworddic/udict.utf8
write anthy.wdic
done
_EOF_
touch -r $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in{-orig,}
}

(
 cd alt-cannadic
 for i in gcanna.ctd gcannaf.ctd gtankan.ctd; do
  dict_conv $i
 done
 cd extra
 for i in g-jiritu-34.t gc-fullname-34.t gf-fuzoku-34.t gt-tankanji_hikanji-34.t gt-tankanji_kanji-34.t; do
  normalize_extra_dict $i
 done
);(
 cd mkworddic
 for i in adjust.t compound.t extra.t udict zipcode.t; do
  dict_conv $i
 done
)
gen_dict_args
%endif


%build
%configure --disable-static
# fix rpath issue
sed -ie 's/^hardcode_libdir_flag_spec.*$'/'hardcode_libdir_flag_spec=" -D__LIBTOOL_IS_A_FOOL__ "/' libtool
LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/src-main/.libs:$RPM_BUILD_DIR/%{name}-%{version}/src-worddic/.libs make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# remove unnecessary files
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.{la,a}

## for emacs-anthy
%__mkdir_p $RPM_BUILD_ROOT%{_emacs_sitestartdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_emacs_sitestartdir}

%if 0%{?rhel} == 0
## for xemacs-anthy
%__mkdir_p $RPM_BUILD_ROOT%{_xemacs_sitestartdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_xemacs_sitestartdir}
pushd $RPM_BUILD_DIR/%{name}-%{version}/src-util
make clean
make EMACS=xemacs lispdir="%{_xemacs_sitelispdir}/%{pkg}"
make install-lispLISP DESTDIR=$RPM_BUILD_ROOT EMACS=xemacs lispdir="%{_xemacs_sitelispdir}/%{pkg}"
popd
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr (-, root, root, -)
%doc AUTHORS COPYING ChangeLog DIARY NEWS README
%{_bindir}/*
%{_sysconfdir}/*
%{_libdir}/lib*.so.*
%{_datadir}/anthy/

%files devel
%defattr (-, root, root, -)
%doc doc/DICLIB doc/DICUTIL doc/GLOSSARY doc/GRAMMAR doc/GUIDE.english doc/ILIB doc/LEARNING doc/LIB doc/MISC doc/POS doc/SPLITTER doc/TESTING doc/protocol.txt
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files -n emacs-%{pkg}
%defattr(-, root, root, -)
%doc doc/ELISP
%{_emacs_sitelispdir}/%{pkg}/*.elc
%{_emacs_sitestartdir}/*.el
%dir %{_emacs_sitelispdir}/%{pkg}

%files -n emacs-%{pkg}-el
%defattr(-, root, root, -)
%{_emacs_sitelispdir}/%{pkg}/*.el

%if 0%{?rhel} == 0
%files -n xemacs-%{pkg}
%defattr(-, root, root, -)
%doc doc/ELISP
%{_xemacs_sitelispdir}/%{pkg}/*.elc
%{_xemacs_sitestartdir}/*.el
%dir %{_xemacs_sitelispdir}/%{pkg}

%files -n xemacs-%{pkg}-el
%defattr(-, root, root, -)
%{_xemacs_sitelispdir}/%{pkg}/*.el
%endif

%changelog
* Sat Oct 29 2011 Liu Di <liudidi@gmail.com> - 9100h-17
- 为 Magic 3.0 重建
