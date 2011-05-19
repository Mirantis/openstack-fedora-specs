%global with_doc 1
%global pkg django-nose

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:		%{pkg}
Version:	0.1.3
Release:	1%{?dist}
Summary:	Django test runner that uses nose.

Group:		Development/Python
License:	BSD
URL:		http://github.com/jbalogh/django-nose
Source0:	http://pypi.python.org/packages/source/d/django-nose/django-nose-0.1.3.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:	noarch
BuildRequires:	python-devel

%description
Django test runner that uses nose.

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
%{python_sitelib}/django_nose
%{python_sitelib}/django_nose*.egg-info
