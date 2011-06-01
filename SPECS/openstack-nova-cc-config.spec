Name:             nova-cc-config
Version:          2011.3
Release:          1
Summary:          OpenStack Compute (nova) - Cloud Controller config

Group:            Development/Languages
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          %{name}.conf
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch

BuildRequires:    perl

Conflicts:        nova-compute-config
Requires:         nova
Requires:         MySQL-python
Requires:         mysql-server
Provides:         nova-config

%description
Configuration files for Nova as Cloud Controller.

%install
rm -rf %{buildroot}

# Setup directories
install -d -m 750 %{buildroot}%{_sysconfdir}/nova

# Install config files
install -p -D -m 640 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,nova,-)
%config(noreplace) %{_sysconfdir}/nova/nova.conf

%changelog
