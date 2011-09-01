%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global checkout 20110901git396f0bfd

Name:           openstack-keystone
Version:        1.0
Release:        0.1.%{checkout}%{?dist}
Summary:        OpenStack Identity Service

License:        ASL 2.0
URL:            https://github.com/rackspace/keystone
# git builds
# git archive --format=tar  --prefix=openstack-keystone/ HEAD | bzip2 -9 > ../openstack-keystone.tar.bz2
Source0:        openstack-keystone-%{checkout}.tar.bz2

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires: python-sphinx >= 1.0
BuildRequires: python-coverage python-webtest python-unittest2 python-pep8
Requires: python-eventlet python-lxml python-paste python-paste-deploy python-paste-script python-sqlite2 python-sqlalchemy python-webob python-routes python-httplib2
Requires: python-ldap
Requires: python-memcached

%description
Keystone is a proposed independent authentication service for
OpenStack (http://www.openstack.org).

This initial proof of concept aims to address the current use cases in
Swift and Nova which are:

* REST-based, token auth for Swift
* many-to-many relationship between identity and tenant for Nova.


%prep
%setup -q

find . \( -name .gitignore -o -name .placeholder \) -delete
find keystone -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;


%build
%{__python} setup.py build
find examples -type f -exec chmod 0664 \{\} \;

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/tools
rm -rf %{buildroot}%{python_sitelib}/examples
rm -rf %{buildroot}%{python_sitelib}/doc

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%files
%doc LICENSE README.md
%doc doc/build/html
%doc examples
%{python_sitelib}/*
%{_bindir}/keystone*


%changelog
* Thu Sep  1 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.1.20110901git396f0bfd%{?dist}
- initial packaging
