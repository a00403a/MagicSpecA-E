%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Text based document generation
Summary(zh_CN.UTF-8): 基于文本的文档生成器
Name: asciidoc
Version: 8.4.5
Release: 7%{?dist}
# The python code does not specify a version.
# The javascript example code is GPLv2+.
License: GPL+ and GPLv2+
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://www.methods.co.nz/asciidoc/
Source0: http://downloads.sourceforge.net/project/asciidoc/%{name}/%{version}/%{name}-%{version}.tar.gz
# http://groups.google.com/group/asciidoc/browse_thread/thread/7f7a633c5b11ddc3
Patch0: asciidoc-8.4.5-datadir.patch
# https://bugzilla.redhat.com/506953
Patch1: asciidoc-8.4.5-use-unsafe-mode-by-default.patch
BuildRequires: python >= 2.4
Requires: python >= 2.4
Requires: docbook-style-xsl
Requires: libxslt
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
AsciiDoc is a text document format for writing short documents,
articles, books and UNIX man pages. AsciiDoc files can be translated
to HTML and DocBook markups using the asciidoc(1) command.

%description -l zh_CN.UTF-8
AsciiDoc 是基于文本的文档生成器。

%prep
%setup -q
%patch0 -p1 -b .datadir
%patch1 -p1 -b .use-unsafe-mode-by-default

# Fix line endings on COPYRIGHT file
sed -i "s/\r//g" COPYRIGHT

# Convert CHANGELOG and README to utf-8
for file in CHANGELOG README; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
%configure

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# real conf data goes to sysconfdir, rest to datadir; symlinks so asciidoc works
for d in dblatex docbook-xsl images javascripts stylesheets ; do
    mv %{buildroot}%{_sysconfdir}/asciidoc/$d \
        %{buildroot}%{_datadir}/asciidoc
    ln -s %{_datadir}/asciidoc/$d %{buildroot}%{_sysconfdir}/asciidoc/
done

# Python API
install -Dpm 644 asciidocapi.py %{buildroot}%{python_sitelib}/asciidocapi.py

# Make it easier to %exclude these with both rpm < and >= 4.7
for file in %{buildroot}{%{_bindir},%{_datadir}/asciidoc/filters/*}/*.py ; do
    touch ${file}{c,o}
done


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%config(noreplace) %{_sysconfdir}/asciidoc
%exclude %{_bindir}/*.py[co]
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/asciidoc/
%exclude %{_datadir}/asciidoc/filters/*/*.py[co]
%{python_sitelib}/asciidocapi.py*
%doc README BUGS CHANGELOG COPYRIGHT

%changelog
* Fri Jan 13 2012 Liu Di <liudidi@gmail.com> - 8.4.5-7
- 为 Magic 3.0 重建

* Mon Oct 31 2011 Liu Di <liudidi@gmail.com> - 8.4.5-6
- 为 Magic 3.0 重建 
- *升级到 8.6.6 有问题*

