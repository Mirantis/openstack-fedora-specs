Name:		openstack-dashboard
Version:	2011.05
Release:	48%{?dist}
Summary:	Dashboard for OpenStack

Group:		Applications/System
License:	ASL 2.0
URL:		https://launchpad.net/openstack-dashboard
Source0:	https://launchpad.net/openstack-dashboard/dashboard.tar.gz
#BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Patch1:           %{name}-confs.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
Requires:	python-setuptools
Requires:	python-boto >= 1.9b
Requires:	python-nose
Requires:	Django
Requires:	django-nose
Requires:	django-registration >= 0.7
Requires:	nova-adminclient

Packager:	"Mirantis Inc." <openstack-support@mirantis.com>

%description
The Dashboard for OpenStack is a reference Django implementation that uses the django-nova project. It serves as an example of how to make use of the django-nova project. See http://launchpad.net/django-nova for more details about the django-nova project. This is a work in progress and is considered an OpenStack "incubation" and is under consideration to become a fully supported OpenStack offering.


%package          openstack-dashboard
Summary:          OpenStack dashboard installation
Group:            Applications/System

%description      openstack-dashboard
The Dashboard for OpenStack is a reference Django implementation that uses the django-nova project. It serves as an example of how to make use of the django-nova project. See http://launchpad.net/django-nova for more details about the django-nova project. This is a work in progress and is considered an OpenStack "incubation" and is under consideration to become a fully supported OpenStack offering.

%prep
%setup -q -n openstack-dashboard

%patch1 -p1

%build
pushd django-nova
%{__python} setup.py build
popd
pushd django-nova-syspanel
%{__python} setup.py build
popd

%install
rm -rf %{buildroot}
pushd django-nova
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd
pushd django-nova-syspanel
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd
install -d -m 755 %{buildroot}/opt/openstack-dashboard
cp -r openstack-dashboard %{buildroot}/opt/

%clean
#rm -rf %{buildroot}


%files 
/opt/openstack-dashboard
/usr

#%defattr(-,root,root,-)
#%doc



%changelog

