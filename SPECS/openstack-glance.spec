%define shortname glance
%global with_doc 0

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-glance
Version:          2011.3
Release:          141%{?dist}
Summary:          OpenStack Image Registry and Delivery Service

Group:            Development/Languages
License:          ASL 2.0
URL:              http://%{shortname}.openstack.org
Source0:          http://glance.openstack.org/tarballs/glance.tar.gz
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
The Glance project provides services for discovering, registering, and
retrieving virtual machine images. Glance has a RESTful API that allows
querying of VM image metadata as well as retrieval of the actual image.

This package contains the API server and a reference implementation registry
server, along with a client library.

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
The Glance project provides services for discovering, registering, and
retrieving virtual machine images. Glance has a RESTful API that allows
querying of VM image metadata as well as retrieval of the actual image.

This package contains the project's Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Glance
Group:            Documentation

BuildRequires:    python-sphinx
BuildRequires:    python-nose
# Required to build module documents
BuildRequires:    python-boto
BuildRequires:    python-daemon
BuildRequires:    python-eventlet
BuildRequires:    python-gflags
BuildRequires:    python-routes
BuildRequires:    python-sqlalchemy
BuildRequires:    python-webob

%description      doc
The Glance project provides services for discovering, registering, and
retrieving virtual machine images. Glance has a RESTful API that allows
querying of VM image metadata as well as retrieval of the actual image.

This package contains documentation files for OpenStack Glance.

%endif

%prep
%setup -q -n %{shortname}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

%if 0%{?with_doc}
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

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
%{python_sitelib}/%{shortname}
%{python_sitelib}/%{shortname}-%{version}-*.egg-info

%if 0%{?with_doc}
%files doc
%defattr(-,root,root,-)
%doc ChangeLog
%doc doc/build/html
%endif

%changelog
