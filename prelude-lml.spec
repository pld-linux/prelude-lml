Summary:	A network intrusion detection system
Summary(pl):	System wykrywania intruzów w sieci
Name:		prelude-lml
%define	_rc	rc4
Version:	0.9.0
Release:	0.%{_rc}.1
License:	GPL
Group:		Applications
Source0:	http://www.prelude-ids.org/download/releases/%{name}-%{version}-%{_rc}.tar.gz
# Source0-md5:	c77f4441e53b47e684269b7e66a404de
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.prelude-ids.org/
BuildRequires:	fam-devel
BuildRequires:	libprelude-devel >= 0.9.0
BuildRequires:	pcre-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prelude LML analyze log files and transmit to prelude some
informations. Prelude LML also use syslog to listen for some others
applications, like NTSyslog.

%description -l pl
Prelude LML analizuje pliki logów i przesy³a trochê informacji do
Prelude. Prelude LML mo¿e tak¿e u¿ywaæ sysloga, aby nas³uchiwa³
danych od innych aplikacji, takich jak NTSyslog.

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
%setup -q -n %{name}-%{version}-%{_rc}

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

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add prelude-lml
if [ -f /var/lock/subsys/prelude-lml ]; then
	/etc/rc.d/init.d/prelude-lml restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/prelude-lml start\" to start Prelude LML."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/prelude-lml ]; then
		/etc/rc.d/init.d/prelude-lml stop 1>&2
	fi
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
%dir %{_sysconfdir}/%{name}/metadata
%{_sysconfdir}/%{name}/ruleset
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
