
%define name alien
%define version 8.85
%define release 2%{?dist}


Summary:	Install Debian and Slackware Packages with RPM
Summary(zh_CN.UTF-8):	用 RPM 安装 Debian 和 Slackware 的包
Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://kitenet.net/programs/code/alien
Source:		http://ftp.debian.org/debian/pool/main/a/alien/alien_%version.tar.gz
License:	GPL
Group: 		Applications/Archiving
Group(zh_CN.UTF-8): 	应用程序/归档
Buildroot:	%{_tmppath}/%{name}-%{version}-root
Requires:	perl 
Requires:       deb
BuildRequires:	perl-devel
BuildArch:      noarch

%description
Alien is a program that converts between the rpm (Mandriva, Redhat ), 
dpkg (Debian), slp (Stampede), and tgz (Slackware) file formats. 
If you want to use a package from another distribution than the one 
you have installed on your system, you can use alien to convert 
it to your preferred package format and install it.

%description -l zh_CN.UTF-8
Alien 是一个可以在 rpm, dpkg, slp 和 tgz 包之间互相转换的程序。

%prep
%setup -n %{name}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
perl -pi -e 's/: :\s*extra_/:: extra_/' Makefile

make

%install
make install DESTDIR=%buildroot

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%doc INSTALL GPL README TODO
%defattr(-,root,root)
%_bindir/*
%{perl_vendorlib}/Alien/Package.pm
%{perl_vendorlib}/Alien/Package/*.pm
%{_libdir}/perl5/perllocal.pod
%{_libdir}/perl5/vendor_perl/auto/Alien/.packlist
%{_mandir}/*/*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 8.85-2
- 为 Magic 3.0 重建

* Thu Oct 27 2011 Liu Di <liudidi@gmail.com> - 8.85-1
- 升级到 8.85

* Sat Jul 06 2009 Liu Di <liudidi@gmail.com> - 8.75-1
- 更新到 8.74

* Mon Sep 22 2008 Liu Di <liudidi@gmail.com> - 8.72-1mgc
- 首次为 Magic 打包
