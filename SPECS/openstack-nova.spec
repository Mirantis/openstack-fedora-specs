%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%global shortname nova
%global bzrtag 1409
%global snaptag ~d4~20110809.%{bzrtag}

Name:             openstack-nova
Version:          2011.3
Release:          0.2.%{bzrtag}bzr%{?dist}
Summary:          OpenStack Compute (nova)

Group:            Applications/System
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          http://nova.openstack.org/tarballs/nova-%{version}%{snaptag}.tar.gz
Source1:          %{shortname}.conf
Source6:          %{shortname}.logrotate

Source11:         %{name}-api.init
Source12:         %{name}-compute.init
Source13:         %{name}-network.init
Source14:         %{name}-objectstore.init
Source15:         %{name}-scheduler.init
Source16:         %{name}-volume.init
Source17:         %{name}-direct-api.init
Source18:         %{name}-ajax-console-proxy.init
Source19:         %{name}-vncproxy.init

Source20:         %{shortname}-sudoers
Source21:         %{shortname}-polkit.pkla
Source22:         %{shortname}-ifc-template

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-devel
BuildRequires:    python-setuptools
BuildRequires:    python-distutils-extra >= 2.18
BuildRequires:    python-netaddr
BuildRequires:    python-lockfile

Requires:         python-nova = %{version}-%{release}
Requires:         sudo
Requires:         euca2ools

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils qemu-kvm

%description
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

%package          node-full
Summary:          OpenStack Nova full node installation
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-api = %{version}-%{release}
Requires:         %{name}-compute = %{version}-%{release}
Requires:         %{name}-network = %{version}-%{release}
Requires:         %{name}-objectstore = %{version}-%{release}
Requires:         %{name}-scheduler = %{version}-%{release}
Requires:         %{name}-volume = %{version}-%{release}
Requires:         openstack-novaclient
Requires:         openstack-glance
Requires:         rabbitmq-server

%description      node-full
This package installs full set of OpenStack Nova Cloud Controller packages.

%package          node-compute
Summary:          OpenStack Nova compute node installation
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-compute = %{version}-%{release}

%description      node-compute
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package installs compute set of OpenStack Nova packages.

%package -n       python-nova
Summary:          Nova Python libraries
Group:            Applications/System

Requires:         vconfig
Requires:         PyXML
Requires:         curl
Requires:         m2crypto
Requires:         libvirt-python
Requires:         python-anyjson
Requires:         python-IPy
Requires:         python-boto
Requires:         python-carrot
Requires:         python-daemon
Requires:         python-eventlet
Requires:         python-greenlet
Requires:         python-gflags
Requires:         python-lockfile
Requires:         python-lxml
Requires:         python-mox
Requires:         python-redis
Requires:         python-routes
Requires:         python-sqlalchemy
Requires:         python-tornado
Requires:         python-twisted-core
Requires:         python-twisted-web
Requires:         python-webob
Requires:         python-netaddr
Requires:         python-glance
Requires:         python-novaclient
Requires:         python-paste-deploy
Requires:         python-migrate
Requires:         python-ldap
Requires:         radvd
Requires:         iptables iptables-ipv6
Requires:         iscsi-initiator-utils
Requires:         scsi-target-utils
Requires:         lvm2
Requires:         socat
Requires:         coreutils
Requires:         python-libguestfs

%description -n   python-nova
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the %{shortname} Python library.

%package          api
Summary:          A OpenStack Compute API server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         python-paste
Requires:         python-paste-deploy

%description      api
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the Nova API Server.

%package          compute
Summary:          A OpenStack Compute compute server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         libvirt-python
Requires:         libvirt >= 0.8.2
Requires:         libxml2-python
Requires:         python-cheetah
Requires:         MySQL-python

%description      compute
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the Nova Compute Worker.

%package          network
Summary:          A OpenStack Compute network server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      network
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the Nova Network Controller.

%package          objectstore
Summary:          A OpenStack Compute objectstore server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      objectstore
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the Nova object store server.

%package          scheduler
Summary:          A OpenStack Compute scheduler server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      scheduler
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the Nova Scheduler.

%package          volume
Summary:          A OpenStack Compute volume server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      volume
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the Nova Volume service.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Compute
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    python-sphinx
BuildRequires:    python-nose
# Required to build module documents
BuildRequires:    python-IPy
BuildRequires:    python-boto
BuildRequires:    python-eventlet
BuildRequires:    python-gflags
BuildRequires:    python-routes
BuildRequires:    python-sqlalchemy
BuildRequires:    python-tornado
BuildRequires:    python-twisted-core
BuildRequires:    python-twisted-web
BuildRequires:    python-webob
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-carrot, python-mox, python-suds, m2crypto, bpython, python-memcached, python-migrate

%description      doc
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains documentation files for %{shortname}.
%endif

%prep
%setup -q -n %{shortname}-%{version}

find . \( -name .gitignore -o -name .placeholder \) -delete

find nova -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# docs generation requires everything to be installed first
%if 0%{?with_doc}
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

# Give instance-usage-audit a reasonable prefix
mv %{buildroot}%{_bindir}/instance-usage-audit %{buildroot}%{_bindir}/nova-instance-usage-audit

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}/images
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}/instances
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}/keys
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}/networks
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/nova
cp -rp nova/CA %{buildroot}%{_sharedstatedir}/nova

# Install config file
install -d -m 750 %{buildroot}%{_sysconfdir}/nova
install -p -D -m 640 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova.conf

# Install initscripts for Nova services
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{name}-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{name}-network
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/%{name}-objectstore
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/%{name}-scheduler
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/%{name}-volume
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_initrddir}/%{name}-direct-api
install -p -D -m 755 %{SOURCE18} %{buildroot}%{_initrddir}/%{name}-ajax-console-proxy
install -p -D -m 755 %{SOURCE19} %{buildroot}%{_initrddir}/%{name}-vncproxy

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/%{shortname}

# Install logrotate
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/nova

# Install template files
install -p -D -m 644 %{shortname}/auth/novarc.template %{buildroot}%{_datarootdir}/%{shortname}/novarc.template
install -p -D -m 644 %{shortname}/cloudpipe/client.ovpn.template %{buildroot}%{_datarootdir}/%{shortname}/client.ovpn.template
install -p -D -m 644 %{shortname}/virt/libvirt.xml.template %{buildroot}%{_datarootdir}/%{shortname}/libvirt.xml.template
install -p -D -m 644 %{shortname}/virt/interfaces.template %{buildroot}%{_datarootdir}/%{shortname}/interfaces.template
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_datarootdir}/%{shortname}/interfaces.template

install -d -m 755 %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-%{shortname}.pkla

# Fixing ajaxterm installation
mv %{buildroot}%{_datarootdir}/%{shortname}/euca-get-ajax-console %{buildroot}%{_bindir}
rm -fr %{buildroot}%{_datarootdir}/%{shortname}/{install_venv.py,nova-debug,pip-requires,clean-vlans,with_venv.sh,esx} %{buildroot}%{_datarootdir}/%{shortname}/ajaxterm/configure*

# Remove unneeded in production stuff
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}%{_bindir}/nova-combined
rm -f %{buildroot}/usr/share/doc/%{shortname}/README*

%pre
getent group nova >/dev/null || groupadd -r nova --gid 8774
getent passwd nova >/dev/null || \
useradd --uid 8774 -r -g nova -G nova,nobody,qemu -d %{_sharedstatedir}/nova -s /sbin/nologin \
-c "OpenStack Nova Daemons" nova
exit 0

%post
/sbin/chkconfig --add %{name}-vncproxy

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-vncproxy stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-vncproxy
fi

%post api
/sbin/chkconfig --add %{name}-api
/sbin/chkconfig --add %{name}-direct-api

%preun api
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-api stop >/dev/null 2>&1
    /sbin/service %{name}-direct-api stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-api
    /sbin/chkconfig --del %{name}-direct-api
fi

%postun api
if [ "$1" -ge 1 ] ; then
    /sbin/service %{name}-api condrestart > /dev/null 2>&1 || :
    /sbin/service %{name}-direct-api condrestart > /dev/null 2>&1 || :
fi

# compute

%post compute
/sbin/chkconfig --add %{name}-ajax-console-proxy
/sbin/chkconfig --add %{name}-compute

%preun compute
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-ajax-console-proxy stop >/dev/null 2>&1
    /sbin/service %{name}-compute stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-ajax-console-proxy
    /sbin/chkconfig --del %{name}-compute
fi

%postun compute
if [ "$1" -ge 1 ] ; then
    /sbin/service %{name}-ajax-console-proxy condrestart > /dev/null 2>&1 || :
    /sbin/service %{name}-compute condrestart > /dev/null 2>&1 || :
fi

# network

%post network
/sbin/chkconfig --add %{name}-network

%preun network
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-network stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-network
fi

%postun network
if [ "$1" -ge 1 ] ; then
    /sbin/service %{name}-network condrestart > /dev/null 2>&1 || :
fi

# objectstore

%post objectstore
/sbin/chkconfig --add %{name}-objectstore

%preun objectstore
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-objectstore stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-objectstore
fi

%postun objectstore
if [ "$1" -ge 1 ] ; then
    /sbin/service %{name}-objectstore condrestart > /dev/null 2>&1 || :
fi

# scheduler

%post scheduler
/sbin/chkconfig --add %{name}-scheduler

%preun scheduler
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-scheduler stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-scheduler
fi

%postun scheduler
if [ "$1" -ge 1 ] ; then
    /sbin/service %{name}-scheduler condrestart > /dev/null 2>&1 || :
fi

# volume

%post volume
/sbin/chkconfig --add %{name}-volume

%preun volume
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-volume stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-volume
fi

%postun volume
if [ "$1" -ge 1 ] ; then
    /sbin/service %{name}-volume condrestart > /dev/null 2>&1 || :
fi

%files
%doc LICENSE
%dir %{_sysconfdir}/nova
%config(noreplace) %{_sysconfdir}/nova/nova.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sudoers.d/%{shortname}
%dir %attr(0755, nova, root) %{_localstatedir}/log/nova
%dir %attr(0755, nova, root) %{_localstatedir}/run/nova
%{_bindir}/nova-console
%{_bindir}/nova-debug
%{_bindir}/nova-instance-usage-audit
%{_bindir}/nova-logspool
%{_bindir}/nova-manage
%{_bindir}/nova-spoolsentry
%{_bindir}/nova-vncproxy
%{_initrddir}/%{name}-vncproxy
%{_bindir}/stack
%{_datarootdir}/nova
%attr(-, nova, nobody) %{_sharedstatedir}/nova

%files -n python-nova
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/nova
%{python_sitelib}/nova-%{version}-*.egg-info

%files api
%doc LICENSE
%{_initrddir}/%{name}-api
%{_initrddir}/%{name}-direct-api
%{_bindir}/nova-api
%{_bindir}/nova-direct-api
%config(noreplace) %attr(-, nova, nobody) %{_sysconfdir}/%{shortname}/api-paste.ini

%files compute
%doc LICENSE
%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-nova.pkla
%{_bindir}/euca-get-ajax-console
%{_bindir}/nova-ajax-console-proxy
%{_bindir}/nova-compute
%{_initrddir}/%{name}-compute
%{_initrddir}/%{name}-ajax-console-proxy
%{_datarootdir}/%{shortname}/ajaxterm

%files network
%doc LICENSE
%{_bindir}/nova-network
%{_bindir}/nova-dhcpbridge
%{_initrddir}/%{name}-network

%files objectstore
%doc LICENSE
%{_bindir}/nova-import-canonical-imagestore
%{_bindir}/nova-objectstore
%{_initrddir}/%{name}-objectstore

%files scheduler
%doc LICENSE
%{_bindir}/nova-scheduler
%{_initrddir}/%{name}-scheduler

%files volume
%doc LICENSE
%{_bindir}/nova-volume
%{_initrddir}/%{name}-volume

%if 0%{?with_doc}
%files doc
%doc LICENSE doc/build/html
%endif

%files node-full

%files node-compute

%changelog
* Tue Aug  9 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.2.1409bzr
- Update to newer upstream
- nova-instancemonitor has been removed
- nova-instance-usage-audit added

* Tue Aug  9 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.1.bzr1130
- More cleanups
- Change release tag to reflect pre-release status

* Wed Jun 29 2011 Matt Domsch <mdomsch@fedoraproject.org> - 2011.3-1087.1
- Initial package from Alexander Sakhnov <asakhnov@mirantis.com>
  with cleanups by Matt Domsch
