Summary:	Simple IRC bouncer
Summary(pl):	Proste narzêdzie do tunelowania irc
Name:		bnc
Version:	2.8.4
Release:	2
License:	GPL
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narzêdzia
Group(pt_BR):	Rede/Utilitários
Source0:	http://gotbnc.com/files/%{name}%{version}.tar.gz
Source1:	%{name}setup.pld
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Easy-configurable IRC proxy.

%description -l pl
Prosty tunel IRC.

%prep
%setup -q -n %{name}%{version}

%build
%configure2_13

%{__make} CC="%{__cc} %{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT%{_bindir} -p
install bnc $RPM_BUILD_ROOT%{_bindir}
install bncchk $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/bncsetup
install mkpasswd $RPM_BUILD_ROOT%{_bindir}/bncmkpasswd

gzip -9nf README CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz CHANGES.gz
%attr(755,root,root) %{_bindir}/*
