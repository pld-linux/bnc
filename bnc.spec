# TODO
#  - bncsetup still not working, needs newer dialog
#  - maybe the initscript should be in separate package?
Summary:	Simple IRC bouncer
Summary(pl):	Proste narzêdzie do tunelowania irc
Name:		bnc
Version:	2.9.3
Release:	0.9
License:	GPL
Group:		Networking/Utilities
# http://gotbnc.com/files/%{name}%{version}.tar.gz - doesn't work with distfiles, reason unknown
#Source0:	ftp://distfiles.pld-linux.org/src/%{name}%{version}.tar.gz
Source0:	http://www.gotbnc.com/files/%{name}%{version}.tar.gz
# Source0-md5:	5012f3eb112f0fda545b1aaf66a06150
Source1:	%{name}.sysconfig
Source2:	%{name}.init
Source3:	%{name}.conf
Patch0:		%{name}-setup.patch
Patch1:		%{name}-typo.patch
URL:		http://www.gotbnc.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.177
Provides:	group(bnc)
Provides:	user(bnc)
Requires:	dialog >= 1:0.69
Requires:	/sbin/start-stop-daemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_sysconfdir /etc/%{name}

%define	userid	142
%define	groupid	142

%description
BNC is a great IRC (Internet Relay Chat) proxying server under the GPL
(General Public License). It allows users to connect to chat servers
by bouncing off the computer which is running BNC. Basically, it
forwards the information from the user to the server and vise versa.

%description -l pl
BNC jest rewelacyjnym i prostym proxy do IRC (Internet Relay Chat) na
licencji GPL (General Public License). BNC pozwala u¿ytkownikom na
po³±czenie siê z serwerem IRC wykorzystuj±c do tego komputer na którym
BNC zosta³o uruchomione. Mówi±c w skrócie, BNC przekazuje informacje
od u¿ytkownika do serwera i vice versa.

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
	CFLAGS="%{rpmcflags}" \
	OFLAGS="%{rpmcflags}" \

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

%pre
if [ -n "`/usr/bin/getgid %{name}`" ]; then
	if [ "`/usr/bin/getgid %{name}`" != %{groupid} ]; then
		echo "Error: group %{name} doesn't have gid=%{groupid}. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g %{groupid} %{name}
fi
if [ -n "`/bin/id -u %{name} 2>/dev/null`" ]; then
	if [ "`/bin/id -u %{name}`" != %{userid} ]; then
		echo "Error: user %{name} doesn't have uid=%{userid}. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u %{userid} -d /var/run/%{name} -s /bin/false \
		-c "%{name} User" -g %{name} %{name} 1>&2
fi

%post
if ! egrep -q '^(adminpass|password)' /etc/bnc/bnc.conf; then
%banner %{name} -e <<EOF
You need to setup passwords in /etc/bnc/bnc.conf!
The daemon will not start unless you've set them!

EOF
# ' vim

fi

# add service just once
[ "$1" = "1" ] && /sbin/chkconfig --add %{name}

if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove bnc
	%groupremove bnc
fi

%files
%defattr(644,root,root,755)
%doc README Changelog motd example.conf bncchk
%dir %attr(750,bnc,bnc) %{_sysconfdir}
%config(noreplace) %verify(not size mtime md5) %attr(640,bnc,bnc) %{_sysconfdir}/*

%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/%{name}

%dir %attr(750,bnc,bnc) /var/run/%{name}
%attr(620,bnc,bnc) %ghost /var/log/%{name}.log
