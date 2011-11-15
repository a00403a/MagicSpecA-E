Epoch: 1

%define _javadir /usr/share/java

Summary: Eclipse Compiler for Java
Summary(zh_CN.UTF-8): Java 的 Eclipse 编译器
Name: ecj
Version: 3.4.2
Release: 4%{?dist}
URL: http://www.eclipse.org
License: EPL
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: %{name}.tar.bz2

Autoreq: no

Requires: libgcj >= 4.0.0

Provides: eclipse-ecj = %{epoch}:%{version}-%{release}
Obsoletes: eclipse-ecj < 1:3.4.2-4

%description
ECJ is the Java bytecode compiler of the Eclipse Platform.  It is also known as
the JDT Core batch compiler.

%prep
%setup -q -n ecj

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
cp -rf * $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi

%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_javadir}/%{name}*.jar
%{_javadir}/eclipse-%{name}*.jar
%{_javadir}/jdtcore.jar
%{_libdir}/gcj/%{name}
%{_docdir}/ecj-3.4.2/about.html

%changelog

