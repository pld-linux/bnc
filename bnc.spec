# TODO
#  - bncsetup working partially, needs newer dialog
Summary:	Simple IRC bouncer
Summary(pl.UTF-8):	Proste narzędzie do tunelowania IRC
Name:		bnc
Version:	2.9.4
Release:	3
License:	GPL
Group:		Networking/Utilities
Source0:	http://www.gotbnc.com/files/%{name}%{version}.tar.gz
# Source0-md5:	190486d2346415e30f6381377e82eb3b
Source1:	%{name}.sysconfig
Source2:	%{name}.init
Source3:	%{name}.conf
Patch0:		%{name}-setup.patch
Patch1:		%{name}-typo.patch
URL:		http://www.gotbnc.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	dialog >= 1:0.69
Provides:	group(bnc)
Provides:	user(bnc)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%description
BNC is a great IRC (Internet Relay Chat) proxying server under the GPL
(General Public License). It allows users to connect to chat servers
by bouncing off the computer which is running BNC. Basically, it
forwards the information from the user to the server and vise versa.

%description -l pl.UTF-8
BNC jest rewelacyjnym i prostym proxy do IRC (Internet Relay Chat) na
licencji GPL (General Public License). BNC pozwala użytkownikom na
połączenie się z serwerem IRC wykorzystując do tego komputer na którym
BNC zostało uruchomione. Mówiąc w skrócie, BNC przekazuje informacje
od użytkownika do serwera i vice versa.

%package init
Summary:	Simple IRC bouncer daemon
Summary(pl.UTF-8):	Prosty demon do tunelowania IRC
Group:		Networking/Utilities
Requires(post):	grep
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name} = %{version}-%{release}
Requires:	/sbin/start-stop-daemon

%description init
This package contains the initscript to start bnc as system service.

%description init -l pl.UTF-8
Ten pakiet zawiera skrypt init do uruchamiania bnc jako usługi
systemowej.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__autoconf}
%configure \
	--with-ssl

%{__make} \
	CFLAGS="%{rpmcflags} -include config.h"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_bindir},%{_sysconfdir},/var/{log,run/%{name}}}

install bnc $RPM_BUILD_ROOT%{_bindir}
install bncsetup $RPM_BUILD_ROOT%{_bindir}/bncsetup
install mkpasswd $RPM_BUILD_ROOT%{_bindir}/bncmkpasswd
install motd $RPM_BUILD_ROOT%{_sysconfdir}/motd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
> $RPM_BUILD_ROOT/var/log/%{name}.log

%clean
rm -rf $RPM_BUILD_ROOT

%pre init
%groupadd -g 142 %{name}
%useradd -u 142 -d /var/run/%{name} -s /bin/false -c "%{name} User" -g %{name} %{name}

%post init
if ! egrep -q '^(adminpass|password)' /etc/bnc/bnc.conf; then
%banner %{name} -e <<EOF
You need to setup passwords in %{_sysconfdir}/%{name}.conf!
The daemon will not start unless you've set them!

EOF
# ' vim

fi
/sbin/chkconfig --add %{name}
%service %{name} restart "%{name} daemon"

%preun init
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun init
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc README Changelog motd example.conf bncchk
%attr(755,root,root) %{_bindir}/*

%files init
%defattr(644,root,root,755)
%dir %attr(750,root,bnc) %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,bnc) %{_sysconfdir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %attr(770,root,bnc) /var/run/%{name}
%attr(620,bnc,bnc) %ghost /var/log/%{name}.log
