%global with_doc 0
%global prj glance

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             %{prj}
Version:          2011.3
Release:          141%{?dist}
Summary:          OpenStack Image Registry and Delivery Service

Group:            Development/Languages
License:          ASL 2.0
URL:              http://%{prj}.openstack.org
Source0:          http://glance.openstack.org/tarballs/glance.tar.gz
Source1:          %{name}-api.init
Source2:          %{name}-registry.init
Source3:          %{name}-logging-api.conf
Source4:          %{name}-logging-registry.conf
Source5:          %{name}.conf

BuildRoot:        %{_tmppath}/%{prj}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    python-devel
BuildRequires:    python-setuptools

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils
Requires:         python-%{prj} = %{version}-%{release}

%description
The Glance project provides services for discovering, registering, and
retrieving virtual machine images. Glance has a RESTful API that allows
querying of VM image metadata as well as retrieval of the actual image.

This package contains the API server and a reference implementation registry
server, along with a client library.

%package -n       python-%{prj}
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

%description -n   python-%{prj}
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
%setup -q -n %{prj}

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
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{prj}/images

# Config file
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/%{prj}/%{prj}.conf
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{prj}/logging-api.conf
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{prj}/logging-registry.conf

# Initscripts
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-registry

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{prj}

# Install log directory
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{prj}

%clean
rm -rf %{buildroot}

%pre
getent group %{prj} >/dev/null || groupadd -r %{prj}
getent passwd %{prj} >/dev/null || \
useradd -r -g %{prj} -d %{_sharedstatedir}/%{prj} -s /sbin/nologin \
-c "OpenStack Glance Daemons" %{prj}
exit 0

%post
/sbin/chkconfig --add openstack-%{prj}-api
/sbin/chkconfig --add openstack-%{prj}-registry

%preun
if [ $1 = 0 ] ; then
    /sbin/service openstack-%{prj}-api stop
    /sbin/chkconfig --del openstack-%{prj}-api
    /sbin/service openstack-%{prj}-registry stop
    /sbin/chkconfig --del openstack-%{prj}-registry
fi

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/%{prj}
%{_bindir}/%{prj}-api
%{_bindir}/%{prj}-control
%{_bindir}/%{prj}-manage
%{_bindir}/%{prj}-registry
%{_bindir}/%{prj}-upload
%{_initrddir}/%{name}-api
%{_initrddir}/%{name}-registry
%defattr(-,%{prj},nobody,-)
%config(noreplace) %{_sysconfdir}/%{prj}/%{prj}.conf
%config(noreplace) %{_sysconfdir}/%{prj}/logging-api.conf
%config(noreplace) %{_sysconfdir}/%{prj}/logging-registry.conf
%{_sharedstatedir}/%{prj}
%dir %attr(0755, %{prj}, nobody) %{_localstatedir}/log/%{prj}
%dir %attr(0755, %{prj}, nobody) %{_localstatedir}/run/%{prj}

%files -n python-%{prj}
%{python_sitelib}/%{prj}
%{python_sitelib}/%{prj}-%{version}-*.egg-info

%if 0%{?with_doc}
%files doc
%defattr(-,root,root,-)
%doc ChangeLog
%doc doc/build/html
%endif

%changelog
