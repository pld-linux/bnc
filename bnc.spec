Summary:	Simple IRC bouncer
Summary(pl):	Proste narz�dzie do tunelowania irc
Name:		bnc
Version:	2.8.9
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	http://gotbnc.com/files/%{name}%{version}.tar.gz
# Source0-md5:	4cabd254443c803fc759b1f062e7bedb
# Source0-size:	57527
Source1:	%{name}setup.pld
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
licencji GPL (General Public License). BNC pozwala u�ytkownikom na
po��czenie si� z serwerem IRC wykorzystuj�c do tego komputer na kt�rym
BNC zosta�o uruchomione. M�wi�c w skr�cie, BNC przekazuje informacje
od u�ytkownika do serwera i vice versa.

%prep
%setup -q -n %{name}%{version}

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
%doc README Changelog
%attr(755,root,root) %{_bindir}/*
