Name:		openstack-repo
Version:	2011.3
Release:	1
Summary:	OpenStack repository configuration from download.mirantis.com

Group:		System Environment/Base
License:	GPL
Source0:	%{name}.repo
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch

%description
OpenStack repository for Fedora 14.

%prep

%build

%install
rm -rf %{buildroot}
install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d/openstack.repo


%files
%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/openstack.repo

%changelog
