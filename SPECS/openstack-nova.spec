%define shortname nova
%define bzrtag ~bzr1130
%global with_doc 1

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-nova
Version:          2011.3
Release:          1087.1%{?dist}
Summary:          OpenStack Compute (nova)

Group:            Applications/System
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          http://nova.openstack.org/tarballs/nova-%{version}%{bzrtag}.tar.gz
Source6:          %{shortname}.logrotate

# Initscripts
Source11:         %{shortname}-api.init
Source12:         %{shortname}-compute.init
Source13:         %{shortname}-network.init
Source14:         %{shortname}-objectstore.init
Source15:         %{shortname}-scheduler.init
Source16:         %{shortname}-volume.init
Source17:         %{shortname}-direct-api.init
Source18:         %{shortname}-ajax-console-proxy.init
Source19:         %{shortname}-vncproxy.init

Source20:         %{shortname}-sudoers
Source21:         %{shortname}-polkit.pkla
Source22:         %{shortname}-ifc-template


BuildRoot:        %{_tmppath}/nova-%{version}-%{release}-root-%(%{__id_u} -n)

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

Requires(post):   chkconfig grep sudo libselinux-utils
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
Requires:         %{name}-cc-config = %{version}
Requires:         %{name}-api = %{version}-%{release}
Requires:         %{name}-compute = %{version}-%{release}
Requires:         %{name}-instancemonitor = %{version}-%{release}
Requires:         %{name}-network = %{version}-%{release}
Requires:         %{name}-objectstore = %{version}-%{release}
Requires:         %{name}-scheduler = %{version}-%{release}
Requires:         %{name}-volume = %{version}-%{release}
Requires:         openstack-client
Requires:         glance
Requires:         rabbitmq-server

%if 0%{?with_doc}
Requires:         %{name}-doc
%endif

%description      node-full
This package installs full set of OpenStack Nova packages and Cloud Controller
configuration.

%package          node-compute
Summary:          OpenStack Nova compute node installation
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-compute-config = %{version}
Requires:         %{name}-compute = %{version}-%{release}
Requires:         %{name}-instancemonitor = %{version}-%{release}

%description      node-compute
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package installs compute set of OpenStack Nova packages and Compute node
configuration.

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
Requires:         start-stop-daemon
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
Requires:         start-stop-daemon
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

%package          instancemonitor
Summary:          A OpenStack Compute instancemonitor server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

%description      instancemonitor
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the Nova instance monitor.

%package          network
Summary:          A OpenStack Compute network server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

%description      network
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the Nova Network Controller.

%package          objectstore
Summary:          A OpenStack Compute objectstore server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

%description      objectstore
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the Nova object store server.

%package          scheduler
Summary:          A OpenStack Compute scheduler server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

%description      scheduler
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the Nova Scheduler.

%package          volume
Summary:          A OpenStack Compute volume server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

%description      volume
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the Nova Volume service.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Compute
Group:            Documentation

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


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
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

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}/images
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}/instances
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}/keys
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}/networks
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{shortname}/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/nova
cp -rp nova/CA %{buildroot}%{_sharedstatedir}/nova

# Install initscripts for Nova services
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{shortname}-api
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{shortname}-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{shortname}-network
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/%{shortname}-objectstore
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/%{shortname}-scheduler
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/%{shortname}-volume
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_initrddir}/%{shortname}-direct-api
install -p -D -m 755 %{SOURCE18} %{buildroot}%{_initrddir}/%{shortname}-ajax-console-proxy
install -p -D -m 755 %{SOURCE19} %{buildroot}%{_initrddir}/%{shortname}-vncproxy

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/%{shortname}

# Install logrotate
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/%{shortname}

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/nova

# Install template files
install -p -D -m 644 %{shortname}/auth/novarc.template %{buildroot}%{_datarootdir}/%{shortname}/novarc.template
install -p -D -m 644 %{shortname}/cloudpipe/client.ovpn.template %{buildroot}%{_datarootdir}/%{shortname}/client.ovpn.template
install -p -D -m 644 %{shortname}/virt/libvirt.xml.template %{buildroot}%{_datarootdir}/%{shortname}/libvirt.xml.template
install -p -D -m 644 %{shortname}/virt/interfaces.template %{buildroot}%{_datarootdir}/%{shortname}/interfaces.template
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_datarootdir}/%{shortname}/interfaces.template

# Clean CA directory
find %{buildroot}%{_sharedstatedir}/%{shortname}/CA -name .gitignore -delete
find %{buildroot}%{_sharedstatedir}/%{shortname}/CA -name .placeholder -delete

install -d -m 755 %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-%{shortname}.pkla

# Fixing ajaxterm installation
mv %{buildroot}%{_datarootdir}/%{shortname}/euca-get-ajax-console %{buildroot}%{_bindir}
rm -fr %{buildroot}%{_datarootdir}/%{shortname}/{install_venv.py,nova-debug,pip-requires,clean-vlans,with_venv.sh,esx} %{buildroot}%{_datarootdir}/%{shortname}/ajaxterm/configure*

# Remove unneeded in production stuff
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}%{_bindir}/nova-combined
rm -f %{buildroot}/usr/share/doc/%{shortname}/README*

%clean
rm -rf %{buildroot}

%pre
getent group nova >/dev/null || groupadd -r nova --gid 8774
getent passwd nova >/dev/null || \
useradd --uid 8774 -r -g nova -G nova,nobody,qemu -d %{_sharedstatedir}/nova -s /sbin/nologin \
-c "OpenStack Nova Daemons" nova
exit 0

%post
if ! grep -F '#includedir /etc/sudoers.d' /etc/sudoers 2>&1 >/dev/null; then
        echo '#includedir /etc/sudoers.d' >> /etc/sudoers
fi
if /usr/sbin/selinuxenabled; then
	echo -e "\033[47m\033[1;31m***************************************************\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m                                                \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m >> \033[5mYou have SELinux enabled on your host !\033[25m <<  \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m                                                \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31mPlease disable it by setting \`SELINUX=disabled' \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31min /etc/sysconfig/selinux and don't forget      \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31mto reboot your host to apply that change!       \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m                                                \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m***************************************************\033[0m"
fi

if rpmquery openstack-nova-cc-config 1>&2 >/dev/null; then
	# Cloud controller node detected, assuming that is contains database
	
	# Database init/migration
	if [ $1 -gt 1 ]; then
		current_version=$(nova-manage db version 2>/dev/null)
		updated_version=$(cd %{python_sitelib}/%{shortname}/db/sqlalchemy/migrate_repo; %{__python} manage.py version)
		if [ "$current_version" -ne "$updated_version" ]; then
			echo "Performing Nova database upgrade"
			/usr/bin/nova-manage db sync
		fi
# NOTE: Bullshit, what if I want use mysql or postgres instead default sqlite?
#	else
#		echo "DB init code, new installation"
#		/usr/bin/nova-manage db sync
#		echo "Please refer http://wiki.openstack.org/NovaInstall/RHEL6Notes for instructions"
	fi
fi

# api

%post api
/sbin/chkconfig --add %{shortname}-api
/sbin/chkconfig --add %{shortname}-direct-api

%preun api
if [ $1 -eq 0 ] ; then
    /sbin/service %{shortname}-api stop >/dev/null 2>&1
    /sbin/service %{shortname}-direct-api stop >/dev/null 2>&1
    /sbin/chkconfig --del %{shortname}-api
    /sbin/chkconfig --del %{shortname}-direct-api
fi

%postun api
if [ "$1" -ge 1 ] ; then
    /sbin/service %{shortname}-api condrestart > /dev/null 2>&1 || :
    /sbin/service %{shortname}-direct-api condrestart > /dev/null 2>&1 || :
fi

# compute

%post compute
/sbin/chkconfig --add %{shortname}-ajax-console-proxy
/sbin/chkconfig --add %{shortname}-compute

%preun compute
if [ $1 -eq 0 ] ; then
    /sbin/service %{shortname}-ajax-console-proxy stop >/dev/null 2>&1
    /sbin/service %{shortname}-compute stop >/dev/null 2>&1
    /sbin/chkconfig --del %{shortname}-ajax-console-proxy
    /sbin/chkconfig --del %{shortname}-compute
fi

%postun compute
if [ "$1" -ge 1 ] ; then
    /sbin/service %{shortname}-ajax-console-proxy condrestart > /dev/null 2>&1 || :
    /sbin/service %{shortname}-compute condrestart > /dev/null 2>&1 || :
fi

# network

%post network
/sbin/chkconfig --add %{shortname}-network

%preun network
if [ $1 -eq 0 ] ; then
    /sbin/service %{shortname}-network stop >/dev/null 2>&1
    /sbin/chkconfig --del %{shortname}-network
fi

%postun network
if [ "$1" -ge 1 ] ; then
    /sbin/service %{shortname}-network condrestart > /dev/null 2>&1 || :
fi

# objectstore

%post objectstore
/sbin/chkconfig --add %{shortname}-objectstore

%preun objectstore
if [ $1 -eq 0 ] ; then
    /sbin/service %{shortname}-objectstore stop >/dev/null 2>&1
    /sbin/chkconfig --del %{shortname}-objectstore
fi

%postun objectstore
if [ "$1" -ge 1 ] ; then
    /sbin/service %{shortname}-objectstore condrestart > /dev/null 2>&1 || :
fi

# scheduler

%post scheduler
/sbin/chkconfig --add %{shortname}-scheduler

%preun scheduler
if [ $1 -eq 0 ] ; then
    /sbin/service %{shortname}-scheduler stop >/dev/null 2>&1
    /sbin/chkconfig --del %{shortname}-scheduler
fi

%postun scheduler
if [ "$1" -ge 1 ] ; then
    /sbin/service %{shortname}-scheduler condrestart > /dev/null 2>&1 || :
fi

# volume

%post volume
/sbin/chkconfig --add %{shortname}-volume

%preun volume
if [ $1 -eq 0 ] ; then
    /sbin/service %{shortname}-volume stop >/dev/null 2>&1
    /sbin/chkconfig --del %{shortname}-volume
fi

%postun volume
if [ "$1" -ge 1 ] ; then
    /sbin/service %{shortname}-volume condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc LICENSE
%config(noreplace) %{_sysconfdir}/logrotate.d/%{shortname}
%config(noreplace) %{_sysconfdir}/sudoers.d/%{shortname}
%dir %attr(0755, nova, root) %{_localstatedir}/log/nova
%dir %attr(0755, nova, root) %{_localstatedir}/run/nova
%{_bindir}/nova-console
%{_bindir}/nova-debug
%{_bindir}/nova-logspool
%{_bindir}/nova-manage
%{_bindir}/nova-spoolsentry
%{_bindir}/nova-vncproxy
%{_bindir}/instance-usage-audit
%{_initrddir}/%{shortname}-vncproxy
%{_bindir}/stack
%{_datarootdir}/nova
%defattr(-,nova,nobody,-)
%{_sharedstatedir}/nova

%files -n python-nova
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/nova
%{python_sitelib}/nova-%{version}-*.egg-info

%files api
%defattr(-,root,root,-)
%doc LICENSE
%{_initrddir}/%{shortname}-api
%{_initrddir}/%{shortname}-direct-api
%{_bindir}/nova-api
%{_bindir}/nova-direct-api
%defattr(-,nova,nobody,-)
%config(noreplace) %{_sysconfdir}/%{shortname}/api-paste.ini

%files compute
%defattr(-,root,root,-)
%doc LICENSE
%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-nova.pkla
%{_bindir}/euca-get-ajax-console
%{_bindir}/nova-ajax-console-proxy
%{_bindir}/nova-compute
%{_initrddir}/%{shortname}-compute
%{_initrddir}/%{shortname}-ajax-console-proxy
%{_datarootdir}/%{shortname}/ajaxterm

%files instancemonitor
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/nova-instancemonitor

%files network
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/nova-network
%{_bindir}/nova-dhcpbridge
%{_initrddir}/%{shortname}-network

%files objectstore
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/nova-import-canonical-imagestore
%{_bindir}/nova-objectstore
%{_initrddir}/%{shortname}-objectstore

%files scheduler
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/nova-scheduler
%{_initrddir}/%{shortname}-scheduler

%files volume
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/nova-volume
%{_initrddir}/%{shortname}-volume

%if 0%{?with_doc}
%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html
%endif

%files node-full

%files node-compute

%changelog
