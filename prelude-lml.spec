Summary:	A network intrusion detection system
Summary(pl):	System wykrywania intruzów w sieci
Name:		prelude-lml
Version:	0.9.4
Release:	0.3
License:	GPL
Group:		Applications
Source0:	http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz
# Source0-md5:	33ed8f9428df64778041e4d8fe41c479
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.prelude-ids.org/
BuildRequires:	fam-devel
BuildRequires:	libprelude-devel >= 0.9.0
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prelude LML analyze log files and transmit to prelude some
informations. Prelude LML also use syslog to listen for some others
applications, like NTSyslog.

%description -l pl
Prelude LML analizuje pliki logów i przesy³a trochê informacji do
Prelude. Prelude LML mo¿e tak¿e u¿ywaæ sysloga, aby nas³uchiwa³ danych
od innych aplikacji, takich jak NTSyslog.

%package devel
Summary:	Header files for prelude-lml
Summary(pl):	Pliki nag³ówkowe dla prelude-lml
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for prelude-lml.

%description devel -l pl
Pliki nag³ówkowe dla prelude-lml.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d $RPM_BUILD_ROOT/var/lib/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add prelude-lml
%service prelude-lml restart
if [ "$1" = 1 ]; then
	echo "Remember to register with prelude-manager before first launch:"
	echo "prelude-adduser register prelude-lml \"idmef:w\" <manager address> --uid 0 --gid 0"
	echo ""
	echo "Run \"/sbin/service prelude-lml start\" to start Prelude LML."
fi

#
# TODO:
#
# register with prelude-manager:
#
# on one console:
# prelude-adduser registration-server prelude-manager
# 	(remember one shot password)
# on the second one:
# prelude-adduser register prelude-lml "idmef:w" <manager address> --uid 0 --gid 0
#	(enter the password)

%preun
if [ "$1" = "0" ]; then
	%service prelude-lml stop
	/sbin/chkconfig --del prelude-lml
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%{_libdir}/%{name}/*.la
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%dir %{_sysconfdir}/%{name}
%dir /var/lib/%{name}
%{_sysconfdir}/%{name}/ruleset
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
