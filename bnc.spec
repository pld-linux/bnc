Summary:	Simple IRC bouncer
Summary(pl):	Proste narzêdzie do tunelowania irc
Name:		bnc
Version:	2.8.6
Release:	3
License:	GPL
Group:		Networking/Utilities
Source0:	http://gotbnc.com/files/%{name}%{version}.tar.gz
Source1:	%{name}setup.pld
BuildRequires:	autoconf
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

%build
%{__autoconf}
%configure

%{__make} CC="%{__cc} %{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT%{_bindir} -p
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
