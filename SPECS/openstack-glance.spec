%define shortname glance
%define bzrtag ~d4~20110805.967

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-glance
Version:          2011.3
Release:          141%{?dist}
Summary:          OpenStack Image Registry and Delivery Service

Group:            Applications/System
License:          ASL 2.0
URL:              http://%{shortname}.openstack.org
Source0:          http://glance.openstack.org/tarballs/glance-%{version}%{bzrtag}.tar.gz
Source1:          %{shortname}-api.init
Source2:          %{shortname}-registry.init
Source3:          %{shortname}-api.conf
Source4:          %{shortname}-registry.conf

BuildRoot:        %{_tmppath}/%{shortname}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    python-devel
BuildRequires:    python-setuptools

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils
Requires:         python-%{shortname} = %{version}-%{release}

%description
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images. The Image Service API server
provides a standard REST interface for querying information about virtual disk
images stored in a variety of back-end stores, including OpenStack Object
Storage. Clients can register new virtual disk images with the Image Service,
query for information on publicly available disk images, and use the Image
Service's client library for streaming virtual disk images.

This package contains the API and registry servers.

%package -n       python-%{shortname}
Summary:          Glance Python libraries
Group:            Applications/System

Requires:         python-anyjson
Requires:         python-argparse
Requires:         python-daemon
Requires:         python-eventlet
Requires:         python-gflags
Requires:         python-lockfile
Requires:         python-mox
Requires:         python-routes
Requires:         python-sqlalchemy
Requires:         python-webob

%description -n   python-%{shortname}
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images.

This package contains the %{shortname} Python library.

%package doc
Summary:          Documentation for OpenStack Glance
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    python-sphinx
BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python-boto
BuildRequires:    python-daemon
BuildRequires:    python-eventlet
BuildRequires:    python-gflags
BuildRequires:    python-routes
BuildRequires:    python-sqlalchemy
BuildRequires:    python-webob

%description      doc
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images.

This package contains documentation files for %{shortname}.

%prep
%setup -q -n %{shortname}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}/images

# Config file
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{shortname}/%{shortname}-api.conf
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{shortname}/%{shortname}-registry.conf

# Initscripts
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{shortname}-api
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{shortname}-registry

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{shortname}

# Install log directory
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{shortname}

%clean
rm -rf %{buildroot}

%pre
getent group %{shortname} >/dev/null || groupadd -r %{shortname}
getent passwd %{shortname} >/dev/null || \
useradd -r -g %{shortname} -d %{_sharedstatedir}/%{shortname} -s /sbin/nologin \
-c "OpenStack Glance Daemons" %{shortname}
exit 0

%post
/sbin/chkconfig --add %{shortname}-api
/sbin/chkconfig --add %{shortname}-registry

%preun
if [ $1 = 0 ] ; then
    /sbin/service %{shortname}-api stop
    /sbin/chkconfig --del %{shortname}-api
    /sbin/service %{shortname}-registry stop
    /sbin/chkconfig --del %{shortname}-registry
fi

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/%{shortname}
%{_bindir}/%{shortname}-api
%{_bindir}/%{shortname}-control
%{_bindir}/%{shortname}-manage
%{_bindir}/%{shortname}-registry
%{_bindir}/%{shortname}-upload
%{_bindir}/%{shortname}-cache-prefetcher
%{_bindir}/%{shortname}-cache-pruner
%{_bindir}/%{shortname}-cache-reaper
%{_bindir}/%{shortname}-scrubber
%{_initrddir}/%{shortname}-api
%{_initrddir}/%{shortname}-registry
%defattr(-,%{shortname},nobody,-)
%config(noreplace) %{_sysconfdir}/%{shortname}/%{shortname}-api.conf
%config(noreplace) %{_sysconfdir}/%{shortname}/%{shortname}-registry.conf
%{_sharedstatedir}/%{shortname}
%dir %attr(0755, %{shortname}, nobody) %{_localstatedir}/log/%{shortname}
%dir %attr(0755, %{shortname}, nobody) %{_localstatedir}/run/%{shortname}

%files -n python-%{shortname}
%doc README
%{python_sitelib}/%{shortname}
%{python_sitelib}/%{shortname}-%{version}-*.egg-info

%files doc
%defattr(-,root,root,-)
%doc doc/build/html

%changelog
