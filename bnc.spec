# TODO:
# - SECURITY: http://securitytracker.com/alerts/2004/Oct/1011583.html
#
%define		_pre	beta2
Summary:	Simple IRC bouncer
Summary(pl):	Proste narzêdzie do tunelowania irc
Name:		bnc
Version:	2.8.8
Release:	0.%{_pre}.3
License:	GPL
Group:		Networking/Utilities
Source0:	http://gotbnc.com/files/%{name}%{version}%{_pre}.tar.gz
# Source0-md5:	5ec74cf2f8d50104c0d512c212417e86
Source1:	%{name}setup.pld
Patch0:		%{name}-c_fix.patch
URL:		http://gotbnc.com/
BuildRequires:	autoconf
BuildRequires:	automake
Requires:	dialog
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
%configure

%{__make} \
	CFLAGS="%{rpmcflags}" \
	OFLAGS="%{rpmcflags}" \
	LIBS="-lcrypt"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install bnc $RPM_BUILD_ROOT%{_bindir}
install bncchk $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/bncsetup
install mkpasswd $RPM_BUILD_ROOT%{_bindir}/bncmkpasswd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGES
%attr(755,root,root) %{_bindir}/*
