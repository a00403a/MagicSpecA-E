#% define beta_tag rc2
%define patchleveltag .10
%define baseversion 4.2
%bcond_without tests

Version: %{baseversion}%{patchleveltag}
Name: bash
Summary: The GNU Bourne Again shell
Summary(zh_CN.UTF-8): GNU Bash
Release: 4%{?dist}
Group: System Environment/Shells
Group(zh_CN.UTF-8): 系统环境/外壳
License: GPLv3+
Url: http://www.gnu.org/software/bash
Source0: ftp://ftp.gnu.org/gnu/bash/bash-%{baseversion}.tar.gz

# For now there isn't any doc
#Source2: ftp://ftp.gnu.org/gnu/bash/bash-doc-%{version}.tar.gz

Source1: dot-bashrc
Source2: dot-bash_profile
Source3: dot-bash_logout

# Official upstream patches
Patch001: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.2-patches/bash42-001
Patch002: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.2-patches/bash42-002
Patch003: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.2-patches/bash42-003
Patch004: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.2-patches/bash42-004
Patch005: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.2-patches/bash42-005
Patch006: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.2-patches/bash42-006
Patch007: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.2-patches/bash42-007
Patch008: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.2-patches/bash42-008
Patch009: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.2-patches/bash42-009
Patch010: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.2-patches/bash42-010

# Other patches
Patch101: bash-2.02-security.patch
Patch102: bash-2.03-paths.patch
Patch103: bash-2.03-profile.patch
Patch104: bash-2.05a-interpreter.patch
Patch105: bash-2.05b-debuginfo.patch
Patch106: bash-2.05b-manso.patch
Patch107: bash-2.05b-pgrp_sync.patch
Patch108: bash-2.05b-readline-oom.patch
Patch109: bash-2.05b-xcc.patch
Patch110: bash-3.2-audit.patch
Patch111: bash-3.2-ssh_source_bash.patch
Patch112: bash-bashbug.patch
Patch113: bash-infotags.patch
Patch114: bash-requires.patch
Patch115: bash-setlocale.patch
Patch116: bash-tty-tests.patch

# 484809, check if interp section is NOBITS
Patch117: bash-4.0-nobits.patch

# Do the same CFLAGS in generated Makefile in examples
Patch118: bash-4.1-examples.patch

# Builtins like echo and printf won't report errors
# when output does not succeed due to EPIPE
Patch119: bash-4.1-broken_pipe.patch

# Enable system-wide .bash_logout for login shells
Patch120: bash-4.2-rc2-logout.patch

# Static analyzis shows some issues in bash-2.05a-interpreter.patch
Patch121: bash-4.2-coverity.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: texinfo bison
BuildRequires: ncurses-devel
BuildRequires: autoconf, gettext

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh). Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh). Most sh scripts can be run by bash without modification.

%description -l zh_CN.UTF-8
一个 Linux 下常用的 shell，Magic 默认就是此 shell。

%package doc
Summary: Documentation files for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Documentation
Group(zh_CN.UTF-8): 文档
Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation files for %{name}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%define pkgdocdir %{_datadir}/doc/%{name}-%{version}

%prep
#%setup -q -a 2
%setup -q -n %{name}-%{baseversion}

# Official upstream patches
%patch001 -p0 -b .001
%patch002 -p0 -b .002
%patch003 -p0 -b .003
%patch004 -p0 -b .004
%patch005 -p0 -b .005
%patch006 -p0 -b .006
%patch007 -p0 -b .007
%patch008 -p0 -b .008
%patch009 -p0 -b .009
%patch010 -p0 -b .010

# Other patches
%patch101 -p1 -b .security
%patch102 -p1 -b .paths
%patch103 -p1 -b .profile
%patch104 -p1 -b .interpreter
%patch105 -p1 -b .debuginfo
%patch106 -p1 -b .manso
%patch107 -p1 -b .pgrp_sync
%patch108 -p1 -b .readline_oom
%patch109 -p1 -b .xcc
%patch110 -p1 -b .audit
%patch111 -p1 -b .ssh_source_bash
%patch112 -p1 -b .bashbug
%patch113 -p1 -b .infotags
%patch114 -p1 -b .requires
%patch115 -p1 -b .setlocale
%patch116 -p1 -b .tty_tests
%patch117 -p1 -b .nobits
%patch118 -p1 -b .examples
%patch119 -p1 -b .broken_pipe
%patch120 -p1 -b .logout
%patch121 -p1 -b .coverity

echo %{version} > _distribution
echo %{release} > _patchlevel

%build
autoconf
%configure --with-bash-malloc=no --with-afs

# Recycles pids is neccessary. When bash's last fork's pid was X
# and new fork's pid is also X, bash has to wait for this same pid.
# Without Recycles pids bash will not wait.
make "CPPFLAGS=-D_GNU_SOURCE -DRECYCLES_PIDS `getconf LFS_CFLAGS`"

%install
rm -rf $RPM_BUILD_ROOT

if [ -e autoconf ]; then
  # Yuck. We're using autoconf 2.1x.
  export PATH=.:$PATH
fi

# Fix bug #83776
perl -pi -e 's,bashref\.info,bash.info,' doc/bashref.info

make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/etc

# make manpages for bash builtins as per suggestion in DOC/README
pushd doc
sed -e '
/^\.SH NAME/, /\\- bash built-in commands, see \\fBbash\\fR(1)$/{
/^\.SH NAME/d
s/^bash, //
s/\\- bash built-in commands, see \\fBbash\\fR(1)$//
s/,//g
b
}
d
' builtins.1 > man.pages
for i in echo pwd test kill; do
  perl -pi -e "s,$i,,g" man.pages
  perl -pi -e "s,  , ,g" man.pages
done

install -c -m 644 builtins.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/builtins.1

for i in `cat man.pages` ; do
  echo .so man1/builtins.1 > ${RPM_BUILD_ROOT}%{_mandir}/man1/$i.1
  chmod 0644 ${RPM_BUILD_ROOT}%{_mandir}/man1/$i.1
done
popd

# Link bash man page to sh so that man sh works.
ln -s bash.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/sh.1

# Not for printf, true and false (conflict with coreutils)
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/printf.1
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/true.1
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/false.1

pushd $RPM_BUILD_ROOT
mkdir ./bin
mv ./usr/bin/bash ./bin
ln -sf bash ./bin/sh
rm -f .%{_infodir}/dir
popd
mkdir -p $RPM_BUILD_ROOT/etc/skel
install -c -m644 %SOURCE1 $RPM_BUILD_ROOT/etc/skel/.bashrc
install -c -m644 %SOURCE2 $RPM_BUILD_ROOT/etc/skel/.bash_profile
install -c -m644 %SOURCE3 $RPM_BUILD_ROOT/etc/skel/.bash_logout
LONG_BIT=$(getconf LONG_BIT)
mv $RPM_BUILD_ROOT%{_bindir}/bashbug \
   $RPM_BUILD_ROOT%{_bindir}/bashbug-"${LONG_BIT}"
ln -s bashbug.1 $RPM_BUILD_ROOT/%{_mandir}/man1/bashbug-"$LONG_BIT".1

# Fix missing sh-bangs in example scripts (bug #225609).
for script in \
  examples/scripts/krand.bash \
  examples/scripts/bcsh.sh \
  examples/scripts/precedence \
  examples/scripts/shprompt
do
  cp "$script" "$script"-orig
  echo '#!/bin/bash' > "$script"
  cat "$script"-orig >> "$script"
  rm -f "$script"-orig
done

%find_lang %{name}

# copy doc to /usr/share/doc
cat /dev/null > %{name}-doc.files
mkdir -p $RPM_BUILD_ROOT/%{pkgdocdir}
cp -p COPYING $RPM_BUILD_ROOT/%{pkgdocdir}
# loadables aren't buildable
rm -rf examples/loadables
for file in CHANGES COMPAT NEWS NOTES POSIX doc examples
do
  cp -rp "$file" $RPM_BUILD_ROOT/%{pkgdocdir}
  echo "%%doc %{pkgdocdir}/$file" >> %{name}-doc.files
done


%if %{with tests}
%check
make check
%endif

%clean
rm -rf $RPM_BUILD_ROOT

# ***** bash doesn't use install-info. It's always listed in %{_infodir}/dir
# to prevent prereq loops

# post is in lua so that we can run it without any external deps.  Helps
# for bootstrapping a new install.
# Jesse Keating 2009-01-29 (code from Ignacio Vazquez-Abrams)
%post -p <lua>
bashfound = false;
shfound = false;
 
f = io.open("/etc/shells", "r");
if f == nil
then
  f = io.open("/etc/shells", "w");
else
  repeat
    t = f:read();
    if t == "/bin/bash"
    then
      bashfound = true;
    end
    if t == "/bin/sh"
    then
      shfound = true;
    end
  until t == nil;
end
f:close()
 
f = io.open("/etc/shells", "a");
if not bashfound
then
  f:write("/bin/bash\n")
end
if not shfound
then
  f:write("/bin/sh\n")
end
f:close()

%postun -p <lua>
t={}
for line in io.lines("/etc/shells")
do
  if line ~= "/bin/bash" and line ~= "/bin/sh"
  then
    table.insert(t,line)
  end
end

f = io.open("/etc/shells", "w+")
for n,line in pairs(t)
do
  f:write(line.."\n")
end

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) /etc/skel/.b*
/bin/sh
/bin/bash
%dir %{pkgdocdir}/
%doc %{pkgdocdir}/COPYING
%attr(0755,root,root) %{_bindir}/bashbug-*
%{_infodir}/bash.info*
%{_mandir}/*/*
%{_mandir}/*/..1*

%files doc -f %{name}-doc.files
%defattr(-, root, root)

# For now there isn't any doc
#%doc doc/*.ps doc/*.0 doc/*.html doc/article.txt

%changelog
* Wed Nov 02 2011 Liu Di <liudidi@gmail.com> - 4.2.10-4
- 为 Magic 3.0 重建 

