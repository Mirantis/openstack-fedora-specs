
Name:             openstack-novaclient
Version:          2.5.1
Release:          1
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

%package doc
Summary:          Documentation for OpenStack Nova API Client
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    python-sphinx

%description      doc
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

This package contains auto-generated documentation.

%prep
%setup -q -n python-novaclient-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html docs html

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%{_bindir}/nova

%files -n python-novaclient
%doc README.rst
%{python_sitelib}/novaclient
%{python_sitelib}/*.egg-info

%files doc
%doc html
