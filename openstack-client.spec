%global with_doc 1
%global prj client

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-%{prj}
Version:          2.4.1
Release:          3
Summary:          Client for OpenStack Nova API
Distribution:     Fedora

Group:            Applications/System
License:          ASL 2.0
URL:              http://pypi.python.org/pypi/python-novaclient
Source0:          http://pypi.python.org/packages/source/p/python-novaclient/python-novaclient-%{version}.tar.gz

BuildRoot:        %{_tmppath}/%{prj}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    python-devel
BuildRequires:    python-setuptools
BuildRequires:    python-nose

Requires:         python-novaclient = %{version}-%{release}

%description
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

This package contains command-line script.

%package -n       python-novaclient
Summary:          Python API for OpenStack Nova
Group:            Development/Languages

Requires:         python-argparse
Requires:         python-simplejson
Requires:         python-httplib2
Requires:         python-prettytable


%description -n   python-novaclient
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

This package contains Python API.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Nova API
Group:            Documentation

%description      doc
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

This package contains autogenerated documentation.

%endif

%prep
%setup -q -n python-novaclient-%{version}

#patch1 -p1

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

%if 0%{?with_doc}
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html docs html

# Fix hidden-file-or-dir warnings
rm -fr .doctrees .buildinfo
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/nova

%files -n python-novaclient
%defattr(-,root,root,-)
%{python_sitelib}/novaclient
%{python_sitelib}/*.egg-info

%if 0%{?with_doc}
%defattr(-,root,root,-)
%files doc
%doc html
%endif
