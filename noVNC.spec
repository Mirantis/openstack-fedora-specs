Name:		noVNC
Version:	2011.05
Release:	i1%{?dist}
Summary:	VNC client using HTML5 (Web Sockets, Canvas) with encryption (wss://) support.

Group:		Applications/System
License:	LGPL 3
URL:		https://github.com/YorikSar/noVNC
Source0:	https://github.com/YorikSar/noVNC/noVNC.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch

Packager:	"Mirantis Inc." <openstack-support@mirantis.com>

%description
noVNC is a VNC client implemented using HTML5 technologies, specifically Canvas and WebSockets (supports 'wss://' encryption).

%setup -q -n noVNC

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}/opt/noVNC
cp -r noVNC %{buildroot}/opt/

%clean
rm -rf %{buildroot}


%files 
/opt/noVNC
