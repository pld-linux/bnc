Summary:	Simple IRC bouncer
Summary(pl):	Proste narzêdzie do tunelowania irc
Name:		bnc
Version:	2.8.4
Release:	1
License:	GPL
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(pl):	Sieciowe/Narzêdzia
Source0:	http://gotbnc.com/files/%{name}%{version}.tar.gz
Source1:	bncsetup.pld	
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Easy-configurable IRC proxy.

%description -l pl
Prosty tunel IRC.

%prep
%setup -q -n %{name}%{version}

%configure2_13

%build
%{__make} CC="gcc %{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT/usr/bin -p
install bnc $RPM_BUILD_ROOT/usr/bin
install bncchk $RPM_BUILD_ROOT/usr/bin
install %{SOURCE1} $RPM_BUILD_ROOT/usr/bin/bncsetup
install mkpasswd $RPM_BUILD_ROOT/usr/bin/bncmkpasswd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*

%doc README CHANGES COPYING
