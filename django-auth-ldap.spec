%global with_doc 1
%global pkg django-auth-ldap

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:		%{pkg}
Version:	1.0b7
Release:	%{?dist}
Summary:	Django LDAP authentication backend

Group:		Development/Python
License:	BSD
URL:		http://bitbucket.org/psagers/django-auth-ldap/
Source0:	http://pypi.python.org/packages/source/d/django-auth-ldap/django-auth-ldap-1.0b7.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:	noarch
BuildRequires:	python-devel

Requires:       python-ldap
%description
This is a Django authentication backend that authenticates against an LDAP service. Configuration can be as simple as a single distinguished name template, but there are many rich configuration options for working with users, groups, and permissions.


%prep
%setup -q -n %{pkg}-%{version}


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python_sitelib}/django_auth_ldap
%{python_sitelib}/django_auth_ldap*.egg-info
