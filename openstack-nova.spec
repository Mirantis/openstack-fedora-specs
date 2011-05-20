%global with_doc 0

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-nova
Version:          2011.3
Release:          1087%{?dist}
Summary:          OpenStack Compute (nova)
Distribution:     Fedora
Vendor:           Mirantis

Group:            Development/Languages
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          http://nova.openstack.org/tarballs/nova.tar.gz
Source2:          %{name}-noVNC-snap2011.03.24.tgz
Source6:          %{name}.logrotate

# Initscripts
Source11:         %{name}-api.init
Source12:         %{name}-compute.init
Source13:         %{name}-network.init
Source14:         %{name}-objectstore.init
Source15:         %{name}-scheduler.init
Source16:         %{name}-volume.init
Source17:         %{name}-direct-api.init
Source18:         %{name}-ajax-console-proxy.init
Source19:         %{name}-vncproxy.init

Source20:         %{name}-sudoers
Source21:         %{name}-polkit.pkla
Source22:         %{name}-ifc-template

Patch1:           %{name}-ldapnotifier.patch
Patch2:           %{name}-bridgeip.patch
Patch3:           nova-api-creds.patch
Patch4:           assign-net2project.patch

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

Packager:         "Mirantis Inc." <openstack-support@mirantis.com>

%description
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

Nova is intended to be easy to extend, and adapt. For example, it currently
uses an LDAP server for users and groups, but also includes a fake LDAP server,
that stores data in Redis. It has extensive test coverage, and uses the Sphinx
toolkit (the same as Python itself) for code and user documentation.

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
Requires:         openstack-glance
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
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Python library.

%package          api
Summary:          A nova API server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon
Requires:         python-paste
Requires:         python-paste-deploy

%description      api
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} API Server.

%package          compute
Summary:          A nova compute server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon
Requires:         libvirt-python
Requires:         libvirt >= 0.8.2
Requires:         libxml2-python
Requires:         python-cheetah
Requires:         MySQL-python

%description      compute
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Compute Worker.

%package          instancemonitor
Summary:          A nova instancemonitor server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

%description      instancemonitor
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} instance monitor.

%package          network
Summary:          A nova network server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

%description      network
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Network Controller.

%package          objectstore
Summary:          A nova objectstore server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

%description      objectstore
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} object store server.

%package          scheduler
Summary:          A nova scheduler server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

%description      scheduler
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Scheduler.

%package          volume
Summary:          A nova volume server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

%description      volume
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Volume service.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for %{name}
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

%description      doc
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains documentation files for %{name}.
%endif

%prep
%setup -q -n nova

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_doc}
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/images
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/instances
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/keys
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/networks
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/nova
cp -rp nova/CA %{buildroot}%{_sharedstatedir}/nova

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
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/%{name}

# Install logrotate
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/nova

# Install template files
install -p -D -m 644 nova/auth/novarc.template %{buildroot}%{_datarootdir}/nova/novarc.template
install -p -D -m 644 nova/cloudpipe/client.ovpn.template %{buildroot}%{_datarootdir}/nova/client.ovpn.template
install -p -D -m 644 nova/virt/libvirt.xml.template %{buildroot}%{_datarootdir}/nova/libvirt.xml.template
install -p -D -m 644 nova/virt/interfaces.template %{buildroot}%{_datarootdir}/nova/interfaces.template
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_datarootdir}/nova/interfaces.template

# Clean CA directory
find %{buildroot}%{_sharedstatedir}/nova/CA -name .gitignore -delete
find %{buildroot}%{_sharedstatedir}/nova/CA -name .placeholder -delete

install -d -m 755 %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-%{name}.pkla

# Fixing ajaxterm installation
mv %{buildroot}%{_datarootdir}/nova/euca-get-ajax-console %{buildroot}%{_bindir}
rm -fr %{buildroot}%{_datarootdir}/nova/{install_venv.py,nova-debug,pip-requires,clean-vlans,with_venv.sh,esx} %{buildroot}%{_datarootdir}/nova/ajaxterm/configure*

# Remove unneeded in production stuff
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}%{_bindir}/nova-combined
rm -f %{buildroot}/usr/share/doc/nova/README*

# Add noVNC console
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/noVNC
tar zxf %{SOURCE2} -C %{buildroot}%{_sharedstatedir}/nova/noVNC

%clean
rm -rf %{buildroot}

%pre
getent group nova >/dev/null || groupadd -r nova
getent passwd nova >/dev/null || \
useradd -r -g nova -G nova,nobody,qemu -d %{_sharedstatedir}/nova -s /sbin/nologin \
-c "OpenStack Nova Daemons" nova
exit 0

%post
if ! fgrep '#includedir /etc/sudoers.d' /etc/sudoers 2>&1 >/dev/null; then
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
		updated_version=$(cd %{python_sitelib}/nova/db/sqlalchemy/migrate_repo; %{__python} manage.py version)
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
#if [ $1 -eq 1 ] ; then
#    /sbin/service %{name}-api condrestart
#    /sbin/service %{name}-direct-api condrestart
#fi

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
#if [ $1 -eq 1 ] ; then
#    /sbin/service %{name}-ajax-console-proxy condrestart
#    /sbin/service %{name}-compute condrestart
#fi

# network

%post network
/sbin/chkconfig --add %{name}-network

%preun network
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-network stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-network
fi

%postun network
#if [ $1 -eq 1 ] ; then
#    /sbin/service %{name}-network condrestart
#fi

# objectstore

%post objectstore
/sbin/chkconfig --add %{name}-objectstore

%preun objectstore
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-objectstore stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-objectstore
fi

%postun objectstore
#if [ $1 -eq 1 ] ; then
#    /sbin/service %{name}-objectstore condrestart
#fi

# scheduler

%post scheduler
/sbin/chkconfig --add %{name}-scheduler

%preun scheduler
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-scheduler stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-scheduler
fi

%postun scheduler
#if [ $1 -eq 1 ] ; then
#    /sbin/service %{name}-scheduler condrestart
#fi

# volume

%post volume
/sbin/chkconfig --add %{name}-volume

%preun volume
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-volume stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-volume
fi

%postun volume
#if [ $1 -eq 1 ] ; then
#    /sbin/service %{name}-volume condrestart
#fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sudoers.d/%{name}
%dir %attr(0755, nova, root) %{_localstatedir}/log/nova
%dir %attr(0755, nova, root) %{_localstatedir}/run/nova
%{_bindir}/nova-console
%{_bindir}/nova-debug
%{_bindir}/nova-logspool
%{_bindir}/nova-manage
%{_bindir}/nova-spoolsentry
%{_bindir}/nova-vncproxy
%{_initrddir}/%{name}-vncproxy
%{_bindir}/stack
%{_datarootdir}/nova
%defattr(-,nova,nobody,-)
%{_sharedstatedir}/nova
%{_datarootdir}/nova/setup_iptables.sh

%files -n python-nova
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/nova
%{python_sitelib}/nova-%{version}-*.egg-info

%files api
%defattr(-,root,root,-)
%{_initrddir}/%{name}-api
%{_initrddir}/%{name}-direct-api
%{_bindir}/nova-api
%{_bindir}/nova-direct-api
%defattr(-,nova,nobody,-)
%config(noreplace) %{_sysconfdir}/nova/api-paste.ini

%files compute
%defattr(-,root,root,-)
%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-openstack-nova.pkla
%{_bindir}/euca-get-ajax-console
%{_bindir}/nova-ajax-console-proxy
%{_bindir}/nova-compute
%{_initrddir}/%{name}-compute
%{_initrddir}/%{name}-ajax-console-proxy
%{_datarootdir}/nova/ajaxterm

%files instancemonitor
%defattr(-,root,root,-)
%{_bindir}/nova-instancemonitor
#{_initrddir}/%{name}-instancemonitor

%files network
%defattr(-,root,root,-)
%{_bindir}/nova-network
%{_bindir}/nova-dhcpbridge
%{_initrddir}/%{name}-network

%files objectstore
%defattr(-,root,root,-)
%{_bindir}/nova-import-canonical-imagestore
%{_bindir}/nova-objectstore
%{_initrddir}/%{name}-objectstore

%files scheduler
%defattr(-,root,root,-)
%{_bindir}/nova-scheduler
%{_initrddir}/%{name}-scheduler

%files volume
%defattr(-,root,root,-)
%{_bindir}/nova-volume
%{_initrddir}/%{name}-volume

%if 0%{?with_doc}
%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html
%endif

%files node-full

%files node-compute

%changelog
