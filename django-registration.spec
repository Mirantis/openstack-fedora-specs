%global with_doc 1
%global pkg django-registration

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:		%{pkg}
Version:	0.7
Release:	1%{?dist}
Summary:	An extensible user-registration application for Django

Group:		Development/Python
License:	BSD
URL:		http://www.bitbucket.org/ubernostrum/django-registration/wiki
Source0:	http://pypi.python.org/packages/source/d/django-registration/django-registration-0.7.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:	noarch
BuildRequires:	python-devel

%description
An extensible user-registration application for Django

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
%{python_sitelib}/registration
%{python_sitelib}/django_registration*.egg-info
