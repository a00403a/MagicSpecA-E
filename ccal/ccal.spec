Summary:		Lunar Calender for Chinese Users	
Summary(zh_CN.UTF-8):		中国的农历
Name:           ccal	
Version:        2.5.2
Release:       	4%{?dist}
License:       	GPL
Group:         User Interface/Desktops
Group(zh_CN.UTF-8):  用户界面/桌面
BuildRoot:     	/var/tmp/%{name}-%{version}-root
Url:		http://ccal.chinesebay.com/ccal/index.html
Source:         http://ccal.chinesebay.com/ccal/%{name}-%{version}.tar.gz

Patch0:		   	ccal-2.4-patch-for-kde-datepicker-usage.patch	
Patch1:		ccal-gcc4.patch

%description
This is a lunar calender utility to export Lunar calender to HTML or PDF.
It is also been used by KDE clock system in Red Flag Linux Desktop.

%description -l zh_CN.UTF-8
这是一个农历工具，可以输出农历为 HTML 或 PDF。
它也被 Magic Linux 中的 KDE 时钟使用。

%prep
%setup
%patch1 -p1

%build
make 
mv ccal ccal.orig
cat %{PATCH0}|patch -p1
make clean
make

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 755 ccal.orig $RPM_BUILD_ROOT/usr/bin/ccal
install -m 755 ccalpdf $RPM_BUILD_ROOT/usr/bin/
install -m 755 ccal $RPM_BUILD_ROOT/usr/bin/ccal-kdatepicker

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/ccal*

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.5.2-4
- 为 Magic 3.0 重建

* Tue Feb 27 2007 Liu Di <liudidi@gmail.com> - 2.4-1mgc
- port to Magic
- update to 2.4

* Fri Feb 17 2006 cjacker <cjacker@redflag-linux.com>
- first build 
