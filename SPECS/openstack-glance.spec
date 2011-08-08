%define shortname glance
%define bzrtag 967
%define snaptag ~d4~20110805.%{bzrtag}

Name:             openstack-glance
Version:          2011.3
Release:          0.1.%{bzrtag}bzr%{?dist}
Summary:          OpenStack Image Service

Group:            Applications/System
License:          ASL 2.0
URL:              http://%{shortname}.openstack.org
Source0:          http://glance.openstack.org/tarballs/glance-%{version}%{snaptag}.tar.gz
Source1:          %{name}-api.init
Source2:          %{name}-registry.init

BuildArch:        noarch
BuildRequires:    python-devel
BuildRequires:    python-setuptools

Requires(post):   chkconfig
Requires(preun):  initscripts
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

Requires:         python-eventlet
Requires:         python-routes
Requires:         python-sqlalchemy
Requires:         python-webob

%description -n   python-%{shortname}
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images.

This package contains the %{shortname} Python library.

%package doc
Summary:          Documentation for OpenStack Image Service
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

sed -i 's|\(sql_connection = sqlite://\)\(/glance.sqlite\)|\1%{_sharedstatedir}/%{shortname}\2|' etc/%{shortname}-registry.conf

sed -i '/\/usr\/bin\/env python/d' glance/common/config.py glance/registry/db/migrate_repo/manage.py

%build
%{__python} setup.py build

%install
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
install -p -D -m 644 etc/%{shortname}-api.conf %{buildroot}%{_sysconfdir}/%{shortname}/%{shortname}-api.conf
install -p -D -m 644 etc/%{shortname}-registry.conf %{buildroot}%{_sysconfdir}/%{shortname}/%{shortname}-registry.conf

# Initscripts
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-registry

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{shortname}

# Install log directory
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{shortname}

%pre
getent group %{shortname} >/dev/null || groupadd -r %{shortname}
getent passwd %{shortname} >/dev/null || \
useradd -r -g %{shortname} -d %{_sharedstatedir}/%{shortname} -s /sbin/nologin \
-c "OpenStack Glance Daemons" %{shortname}
exit 0

%post
/sbin/chkconfig --add %{name}-api
/sbin/chkconfig --add %{name}-registry

%preun
if [ $1 = 0 ] ; then
    /sbin/service %{name}-api stop
    /sbin/chkconfig --del %{name}-api
    /sbin/service %{name}-registry stop
    /sbin/chkconfig --del %{name}-registry
fi

%files
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
%{_initrddir}/%{name}-api
%{_initrddir}/%{name}-registry
%dir %{_sysconfdir}/glance
%config(noreplace) %{_sysconfdir}/%{shortname}/%{shortname}-api.conf
%config(noreplace) %{_sysconfdir}/%{shortname}/%{shortname}-registry.conf
%dir %attr(0755, %{shortname}, nobody) %{_sharedstatedir}/%{shortname}
%dir %attr(0755, %{shortname}, nobody) %{_localstatedir}/log/%{shortname}
%dir %attr(0755, %{shortname}, nobody) %{_localstatedir}/run/%{shortname}

%files -n python-%{shortname}
%doc README
%{python_sitelib}/%{shortname}
%{python_sitelib}/%{shortname}-%{version}-*.egg-info

%files doc
%doc doc/build/html

%changelog
