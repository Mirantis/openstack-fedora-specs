%global with_doc 1
%global pkg nova-adminclient

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:		%{pkg}
Version:	0.1.7
Release:	1%{?dist}
Summary:	Nova admin client. Sincerly yours, K.O.

Group:		Development/Python
License:	MIT
URL:		http://www.openstack.org
Source0:	http://pypi.python.org/packages/source/n/nova-adminclient/nova-adminclient-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:	noarch
BuildRequires:	python-devel

%description
Nova admin client. Sincerly yours, K.O.

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
%{python_sitelib}/nova_adminclient
%{python_sitelib}/nova_adminclient*.egg-info
