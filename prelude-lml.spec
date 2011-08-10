#
# Conditional build:
%bcond_without	fam			# build without FAM support
%bcond_without	unsupported_rulesets	# build without unsupported rulesets
#
Summary:	A network intrusion detection system
Summary(pl.UTF-8):	System wykrywania intruzów w sieci
Name:		prelude-lml
Version:	1.0.0
Release:	1
License:	GPL v2+
Group:		Applications
#Source0Download: http://www.prelude-ids.com/developpement/telechargement/index.html
Source0:	http://www.prelude-ids.com/download/releases/prelude-lml/%{name}-%{version}.tar.gz
# Source0-md5:	7bf0b9081eedf3fd58bb41a9695b121a
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.prelude-ids.com/
%{?with_fam:BuildRequires:	fam-devel}
BuildRequires:	libicu-devel >= 3.0
BuildRequires:	libprelude-devel >= %{version}
BuildRequires:	pcre-devel >= 4.1
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	libprelude >= 0.9.8
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prelude LML analyze log files and transmit to prelude some
informations. Prelude LML also use syslog to listen for some others
applications, like NTSyslog.

%description -l pl.UTF-8
Prelude LML analizuje pliki logów i przesyła trochę informacji do
Prelude. Prelude LML może także używać sysloga, aby nasłuchiwał danych
od innych aplikacji, takich jak NTSyslog.

%package devel
Summary:	Header files for prelude-lml
Summary(pl.UTF-8):	Pliki nagłówkowe dla prelude-lml
Group:		Development/Libraries
Requires:	libprelude-devel >= 0.9.8

%description devel
Header files for prelude-lml.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla prelude-lml.

%prep
%setup -q

%build
%configure \
	--with%{!?with_fam:out}-fam \
	--%{!?with_unsupported_rulesets:dis}%{?with_unsupported_rulesets:en}able-unsupported_rulesets
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# are generating wrong dependencies (and are not needed anyway)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d $RPM_BUILD_ROOT/var/lib/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add prelude-lml
if [ "$1" = "1" ]; then
%banner -e %{name} <<EOF
Remember to register with prelude-manager before first launch:
prelude-adduser register prelude-lml "idmef:w admin:r" <manager address> --uid 0 --gid 0

EOF
fi
%service prelude-lml restart

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
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%dir %{_sysconfdir}/%{name}
%dir /var/lib/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.*
%{_sysconfdir}/%{name}/ruleset

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
