%define _name amule
%define svn 0
#%define date 20080205
%define _rc rc2
%if %{_rc}
%define _dotrc .%{?_rc}
%endif

Name: aMule
Version:	 2.3.1
#Release: 0.cvs%{date}.2mgc
%if %{svn}
Release: 0.svn.%{svn}.1%{?dist}
%endif
%if %{_rc}
Release: 0.1%{?_dotrc}.%{?dist}
%else
Release: 1%{?dist}
%endif
Summary: aMule - eMule client
Summary(zh_CN.UTF-8): aMule - eMule 客户端
License:	 GPL
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL: http://www.amule.org
#cvsurl: http://www.hirnriss.net/?area=cvs
#Source0: %{name}-CVS-%{date}.tar.bz2
#Source1: %_name
%if %{svn}
Source0: http://amule.sourceforge.net/tarballs/aMule-SVN-%{svn}.tar.bz2
%else
Source0: http://cdnetworks-kr-1.dl.sourceforge.net/project/amule/%{name}/%{version}%?{_rc}/%{name}-%{version}%{?_rc}.tar.bz2
%endif
Source1: amule.desktop
Source2: alc.desktop
Source3: wxcas.desktop
Source10: aMule.addresses.dat
Source11: aMule.server.met

Conflicts: xmule
Provides: amule
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
# Automatically added by buildreq on Fri Aug 20 2004
BuildRequires: bc fontconfig freetype gcc-c++ glib2-devel atk-devel libcurl-devel gtk2-devel pango-devel openssl-devel libstdc++-devel pkgconfig wx-gtk2-unicode-devel zlib-devel
BuildRequires: flex cryptopp-devel
BuildRequires: libupnp-devel >= 1.6.6

Requires: libupnp >= 1.6.6

# 文件名转码为 gb18030
Patch0: aMule-2.2.1-convfilenames-gb18030.patch
Patch1: aMule-2.2.2-convfilenames-gb18030.patch
# dlp 补丁
#Patch100: http://amule-dlp.googlecode.com/files/aMule-2.3.1rc1-DLP4401.patch
Patch100: aMule-2.3.1rc2-DLP4401.patch

%description
The "all-platform eMule", it is a eMule-like client for ed2k network, 
supporting Linux, *BSD platforms, Solaris, *MacOSX and *Win32 (*soon). 
It was forked from xMule project back in september 2003 (not related 
to it anymore, except little bits of old code), to drive it to a brand 
new direction and quality. Uses wxWidgets (formely known as wxWindows) 
for multiplatform support.

%description -l zh_CN.UTF-8
“所有平台的 eMule”，它是一个类 eMule 的 ed2k 网络客户端，支持
Linux，*BSD 平台，Solaris，*MacOSX 和 *Win32 (*快有了)。它派生
于 2003 年 9 月的 xMule 项目（现在已经没有关系了，除了一点儿
老的代码），以使其转向崭新的开发方向并获得更高的质量。它使用
wxWidgets (众所周知的 wxWindow)，从而支持多平台。


%package alc
Summary: aMule Link Creater
Summary(zh_CN.UTF-8): aMule ed2k 链接创建器
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Requires: %{name} = %{version}-%{release}

%description alc
aMule Link Creater.

%description alc -l zh_CN.UTF-8
aMule ed2k 链接创建器。

%package wxcas
Summary: aMule statistics
Summary(zh_CN.UTF-8): aMule 运行统计信息
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Requires: %{name} = %{version}-%{release}

%description wxcas
aMule statistics.

%description wxcas -l zh_CN.UTF-8
aMule 运行统计信息。

%package -n xchat-aMule
Summary: xchat aMule plugin
Summary(zh_CN.UTF-8): xchat aMule 插件
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Requires: %{name} = %{version}-%{release}
Requires: xchat

%description -n xchat-aMule
xchat aMule plugin.

%description -n xchat-aMule -l zh_CN.UTF-8
xchat aMule 插件。


%prep
%if %{svn}
%setup -q -n %{name}-SVN-%{svn}
%else
%setup -q -n %{name}-%{version}%{_rc}
%endif
%patch1 -p1 -b .fixgb18030

%patch100 -p1

# sed -i -e 's|ConvAmuleBrokenFileNames aMuleConvBrokenFileNames(wxT("ISO-8859-1"));|ConvAmuleBrokenFileNames aMuleConvBrokenFileNames(wxT("GB18030"));|' src/libs/common/ConvAmule.h
# 替换掉无效的服务器地址更新列表
sed -i -e 's|http://ocbmaurice.dyndns.org/pl/slist.pl/server.met?download/server-max.met|http://www.emule.org.cn/server.met|' src/Preferences.cpp
sed -i -e 's|http://ocbmaurice.dyndns.org/pl/slist.pl/server.met?download/server-max.met|http://www.emule.org.cn/server.met|' src/amule.cpp
sed -i -e 's|http://ocbmaurice.dyndns.org/pl/slist.pl/server.met?download/server-max.met|http://www.emule.org.cn/server.met|' docs/README
# 默认不自动更新服务器列表
sed -i -e 's|new Cfg_Bool( wxT("/eMule/AddServersFromServer"), s_addserversfromserver, true)|new Cfg_Bool( wxT("/eMule/AddServersFromServer"), s_addserversfromserver, false)|' src/Preferences.cpp
sed -i -e 's|new Cfg_Bool( wxT("/eMule/AddServersFromClient"), s_addserversfromclient, true )|new Cfg_Bool( wxT("/eMule/AddServersFromClient"), s_addserversfromclient, false )|' src/Preferences.cpp
# 开启安全连接服务器
sed -i -e 's|new Cfg_Bool( wxT("/eMule/SafeServerConnect"), s_safeServerConnect, false )|new Cfg_Bool( wxT("/eMule/SafeServerConnect"), s_safeServerConnect, true )|' src/Preferences.cpp



%build
%configure	--enable-ccache \
		--enable-optimize \
		--enable-alc \
		--enable-wxcas \
		--enable-xas \
		--enable-upnp \
		--enable-geoip \
		--enable-profile \
		--enable-amule-daemon  \
		--enable-amule-gui \
		--enable-webserver \
		--enable-alcc \
		--enable-amulecmd \
		--enable-cas \
		--enable-plasmamule \
		--disable-debug

# smp 选项编译出错  :(  --by nihui
#%{__make} %{?_smp_mflags}
make

%install
%{__rm} -rf %{buildroot}
%makeinstall

# 菜单项中文化
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications/amule.desktop
install -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/applications/alc.desktop
install -D -m 644 %{SOURCE3} %{buildroot}%{_datadir}/applications/wxcas.desktop

# 准备初始化数据
mkdir -p %{buildroot}/etc/skel/.aMule
mkdir -p %{buildroot}/root/.aMule
# ed2k 服务器地址更新地址列表
install -m 600 %{SOURCE10} %{buildroot}/etc/skel/.aMule/addresses.dat
install -m 600 %{SOURCE10} %{buildroot}/root/.aMule/addresses.dat
# ed2k 初始化服务器地址列表
install -m 600 %{SOURCE11} %{buildroot}/etc/skel/.aMule/server.met
install -m 600 %{SOURCE11} %{buildroot}/root/.aMule/server.met


magic_rpm_clean.sh
%find_lang %{_name}

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post
for D in `cat /etc/passwd | grep ':/home/' | cut -f 6 -d:`; do
if [ -d $D ];then
  cp -auf /etc/skel/.aMule $D/
  USRHOME=`ls -la $D | grep "[^\.\.]\.$"`
  OWNER=`echo $USRHOME | cut -f 3 -d\ `
  GROUP=`echo $USRHOME | cut -f 4 -d\ `
  chown -hR ${OWNER}:${GROUP} $D/.aMule
  chmod 600 $D/.aMule/addresses.dat
  chmod 600 $D/.aMule/server.met
fi
done


%postun

%files -f %{_name}.lang
%defattr(-,root,root,-)
%{_bindir}/amule
%{_bindir}/ed2k
%{_datadir}/amule/skins/*.zip
%{_datadir}/applications/amule.desktop
%{_mandir}/man1/amule.1.gz
%{_mandir}/man1/ed2k.1.gz
%{_datadir}/pixmaps/amule.xpm
%{_docdir}/amule/*
/etc
/root

%files alc
%defattr(-,root,root,-)
%{_bindir}/alc
%{_datadir}/pixmaps/alc.xpm
%{_datadir}/applications/alc.desktop
%{_mandir}/man1/alc.1.gz

%files wxcas
%defattr(-,root,root,-)
%{_bindir}/wxcas
%{_datadir}/pixmaps/wxcas.xpm
%{_datadir}/applications/wxcas.desktop
%{_mandir}/man1/wxcas.1.gz

%files -n xchat-aMule
%defattr(-,root,root,-)
%{_bindir}/autostart-xas
%{_libdir}/xchat/plugins/xas.pl
%{_mandir}/man1/xas.1.gz
# 需要分包
%{_bindir}/alcc
%{_bindir}/amulecmd
%{_bindir}/amuled
%{_bindir}/amulegui
%{_bindir}/amuleweb
%{_bindir}/cas
%{_datadir}/amule/webserver/*
%{_datadir}/applications/amulegui.desktop
%{_datadir}/cas/stat.png
%{_datadir}/cas/tmp.html
%{_mandir}/man1/alcc.1.gz
%{_mandir}/man1/amulecmd.1.gz
%{_mandir}/man1/amuled.1.gz
%{_mandir}/man1/amulegui.1.gz
%{_mandir}/man1/amuleweb.1.gz
%{_mandir}/man1/cas.1.gz
%{_datadir}/pixmaps/amulegui.xpm

%changelog
* Fri Oct 28 2011 Liu Di <liudidi@Gmail.com> - 2.3.1.rc2-1
- 升级到 2.3.1rc2

* Mon Oct 26 2009 Liu Di <liudidi@gmail.com>  - 2.2.6-1
- 更新到 2.2.6
- 添加 DLP 补丁

* Fri Jan 16 2009 Liu Di <liudidi@gmail.com>  - 2.2.3-0.1mgc
- 更新到 2.2.3

* Thu Oct 2 2008 Ni Hui <shuizhuyuanluo@126.com> - 2.2.2-0.3mgc
- 修改中文转码补丁(使用 wxConvLibc 替代 wxConvLocal)
- 戊子  九月初四

* Thu Aug 28 2008 Ni Hui <shuizhuyuanluo@126.com> - 2.2.2-0.1mgc
- 更新至 2.2.2
- BuildRequires: libupnp-devel >= 1.6.6
- 戊子  七月廿八

* Thu Jun 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 2.2.1-0.1mgc
- 更新至 2.2.1 正式版
- 更新中文转码补丁
- I'm happy to announce the release of aMule 2.2.1 - the "Excuse me, have you seen my 2.2.0 release anywhere?" version.
- 戊子  五月初九

* Tue Feb 05 2008 Liu Di <liudidi@gmail.com> - 2.2.0-0.cvs20080205
- 更新到 cvs20080205
- 更新中文转码补丁
- 添加对 cryptopp-devel 的编译依赖

* Fri Jan 04 2008 kde <athena_star {at} 163 {dot} com> - 2.2.0-0.cvs20080103
- update to cvs20080103
- 增加初始化服务器地址相关信息、配置以及 post 脚本，使之安装后即可使用
- 为避免代码变化导致补丁失效，以 sed 替换命令取代中文转码补丁
- 为 install 小节增补“%{__rm} -rf %{buildroot}”命令

* Sat Dec 01 2007 Ni Hui <shuizhuyuanluo@126.com> - 2.2.0-0.cvs20071201
- update to cvs20071201
- 添加菜单项

* Fri Nov 30 2007 Ni Hui <shuizhuyuanluo@126.com> - 2.2.0-0.cvs20071130
- update to cvs20071130
- 添加中文转码补丁

* Fri Mar 09 2007 Liu Di <liudidi@gmail.com> - 2.2.0-0.cvs20070309
- update to cvs20070309

* Mon Jan 30 2007 Liu Di <liudidi@gmail.com> - 2.2.0-0.cvs20070129
- update to cvs20070129

* Sat Apr 02 2006 liudi <liudidi@gmail.com>
- update to cvs20060401

* Tue Feb 21 2006 liudi <liudidi@gmail.com>
- Update to CVS20060221

* Mon Feb 20 2006 liudi <liudidi@gmail.com>
- Update to CVS20060220

* Tue Jan 10 2006 liudi <liudidi@gmail.com>
- Update to CVS20060110

* Tue Nov 08 2005 sejishikong <sejishikong@263.net>
- Update to CVS20051107

* Mon Sep 12 2005 sejishikong <sejishikong@263.net>
- Update to CVS20050911

* Tue Mar 01 2005 sejishikong <sejishikong@163.com>
- Update to 2.0.0rc8

* Tue Oct 05 2004 sejishikong <sejishikong@263.net>
- Remove cryptopp

* Tue Oct 05 2004 sejishikong <sejishikong@263.net>
- Update to 2.0.0rc6

* Thu Sep 09 2004 Alex Gorbachenko (agent_007) <algor@altlinux.ru> 2.0.0rc5-alt2
- rebuild with new wxWidgets pgAdmin snapshot.
