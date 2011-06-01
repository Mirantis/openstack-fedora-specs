%global with_doc 1
%global pkg eventlet

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:		python-%{pkg}
Version:	0.9.15
Release:	1%{?dist}
Summary:	Highly concurrent networking library

Group:		Development/Python
License:	MIT
URL:		http://eventlet.net/doc/
Source0:	http://pypi.python.org/packages/source/e/eventlet/eventlet-0.9.15.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:	noarch
BuildRequires:	python-devel

%description
Eventlet is a concurrent networking library for Python that allows you to change how you run your code, not how you write it.It uses epoll or libevent for highly scalable non-blocking I/O. Coroutines ensure that the developer uses a blocking style of programming that is similar to threading, but provide the benefits of non-blocking I/O. The event dispatch is implicit, which means you can easily use Eventlet from the Python interpreter, or as a small part of a larger application.

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
%{python_sitelib}/eventlet
%{python_sitelib}/eventlet*.egg-info
