# TODO
#  - bncsetup still not working, needs newer dialog
Summary:	Simple IRC bouncer
Summary(pl):	Proste narzêdzie do tunelowania irc
Name:		bnc
Version:	2.9.3
Release:	0.1
License:	GPL
Group:		Networking/Utilities
# http://gotbnc.com/files/%{name}%{version}.tar.gz - doesn't work with distfiles, reason unknown
#Source0:	ftp://distfiles.pld-linux.org/src/%{name}%{version}.tar.gz
Source0:	http://www.gotbnc.com/files/%{name}%{version}.tar.gz
# Source0-md5:	5012f3eb112f0fda545b1aaf66a06150
Patch0:		%{name}-setup.patch
URL:		http://gotbnc.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssl-devel
Requires:	dialog >= 1:0.70
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
cp -f /usr/share/automake/config.sub .
%{__autoconf}
%configure \
	--with-ssl

%{__make} \
	CFLAGS="%{rpmcflags}" \
	OFLAGS="%{rpmcflags}" \
	LIBS="-lcrypt"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install bnc $RPM_BUILD_ROOT%{_bindir}
install bncchk $RPM_BUILD_ROOT%{_bindir}
install bncsetup $RPM_BUILD_ROOT%{_bindir}/bncsetup
install mkpasswd $RPM_BUILD_ROOT%{_bindir}/bncmkpasswd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README Changelog motd example.conf
%attr(755,root,root) %{_bindir}/*
