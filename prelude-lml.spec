#
# Conditional build:
%bcond_with	system_libev	# system libev (expects libev built with EV_MULTIPLICITY=0)
#
Summary:	A network intrusion detection system - log analyzer
Summary(pl.UTF-8):	System wykrywania intruzów w sieci - analizator logów
Name:		prelude-lml
Version:	3.1.0
Release:	1
License:	GPL v2+
Group:		Applications
#Source0Download: https://www.prelude-siem.org/projects/prelude/files
Source0:	https://www.prelude-siem.org/attachments/download/724/%{name}-%{version}.tar.gz
# Source0-md5:	2433f9dc036f8e4a01fb05adbf9aafb1
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		https://www.prelude-siem.org/
BuildRequires:	gnutls-devel >= 1.0.17
BuildRequires:	libicu-devel >= 3.0
%{?with_system_libev:BuildRequires:	libev-devel}
BuildRequires:	libprelude-devel >= %{version}
BuildRequires:	pcre-devel >= 4.1
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.644
Requires(post,preun):	/sbin/chkconfig
Requires:	gnutls >= 1.0.17
Requires:	libprelude >= %{version}
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
Requires:	libprelude-devel >= %{version}

%description devel
Header files for prelude-lml.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla prelude-lml.

%prep
%setup -q

%if %{with system_libev}
# stub
echo 'all:' > libev/Makefile
%endif

%build
%configure \
%if %{with system_libev}
	LIBEV_CFLAGS=" " \
	LIBEV_LIBS="-lev" \
	--with-libev
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# are generating wrong dependencies (and are not needed anyway)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d $RPM_BUILD_ROOT/var/lib/%{name}
install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}
cat >$RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf <<EOF
d /var/run/%{name} 0700 root root -
EOF

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/plugins.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/prelude-lml.conf
%{systemdtmpfilesdir}/%{name}.conf
%dir /var/lib/%{name}
%dir /var/run/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
