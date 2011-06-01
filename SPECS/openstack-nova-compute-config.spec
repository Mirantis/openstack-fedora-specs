Name:             openstack-nova-compute-config
Version:          2011.3
Release:          1
Summary:          OpenStack Compute (nova) - Compute node configuration

Group:            Development/Languages
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          %{name}.conf
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch

BuildRequires:    perl

Conflicts:        openstack-nova-cc-config
Requires:         openstack-nova
Provides:         openstack-nova-config

%description
Configuration files for Nova as compute node.

%prep
#setup -q -n nova-%{version}

%build
#{__python} setup.py build

%install
rm -rf %{buildroot}

# Setup directories
install -d -m 755 %{buildroot}%{_sysconfdir}/nova

# Install config files
install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nova/nova.conf

%changelog
