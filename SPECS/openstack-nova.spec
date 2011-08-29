%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%global milestone d4

Name:             openstack-nova
Version:          2011.3
Release:          0.4.%{milestone}%{?dist}
Summary:          OpenStack Compute (nova)

Group:            Applications/System
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          http://launchpad.net/nova/diablo/diablo-4/+download/nova-%{version}~%{milestone}.tar.gz
Source1:          nova.conf
Source6:          nova.logrotate

Source11:         openstack-nova-api.init
Source12:         openstack-nova-compute.init
Source13:         openstack-nova-network.init
Source14:         openstack-nova-objectstore.init
Source15:         openstack-nova-scheduler.init
Source16:         openstack-nova-volume.init
Source17:         openstack-nova-direct-api.init
Source18:         openstack-nova-ajax-console-proxy.init
Source19:         openstack-nova-vncproxy.init

Source20:         nova-sudoers
Source21:         nova-polkit.pkla
Source22:         nova-ifc-template

Patch1:           nova-fix-flavorid-migration-failure.patch
Patch2:           nova-fix-quotas-migration-failure.patch
Patch3:           nova-do-not-require-bridge_interface-for-flatdhcpmanager.patch

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-setuptools
BuildRequires:    python-distutils-extra >= 2.18
BuildRequires:    python-netaddr
BuildRequires:    python-lockfile

Requires:         python-nova = %{version}-%{release}
Requires:         openstack-glance

Requires:         python-paste
Requires:         python-paste-deploy

Requires:         libvirt-python
Requires:         libvirt >= 0.8.2
Requires:         libxml2-python
Requires:         python-cheetah
Requires:         MySQL-python

Requires:         euca2ools
Requires:         openssl
Requires:         rabbitmq-server
Requires:         sudo

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

This package contains the nova Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Compute
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    python-sphinx
BuildRequires:    graphviz

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

This package contains documentation files for nova.
%endif

%prep
%setup -q -n nova-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1

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
# Manually auto-generate to work around sphinx-build segfault
./generate_autodoc_index.sh
SPHINX_DEBUG=1 sphinx-build -b html source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

# Give stack, instance-usage-audit and clear_rabbit_queues a reasonable prefix
mv %{buildroot}%{_bindir}/stack %{buildroot}%{_bindir}/nova-stack
mv %{buildroot}%{_bindir}/instance-usage-audit %{buildroot}%{_bindir}/nova-instance-usage-audit
mv %{buildroot}%{_bindir}/clear_rabbit_queues %{buildroot}%{_bindir}/nova-clear-rabbit-queues

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/buckets
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/images
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/instances
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/keys
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/networks
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/nova

# Setup ghost sqlite DB
touch %{buildroot}%{_sharedstatedir}/nova/nova.sqlite

# Setup ghost CA cert
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/CA
install -p -m 755 nova/CA/*.sh %{buildroot}%{_sharedstatedir}/nova/CA
install -p -m 644 nova/CA/openssl.cnf.tmpl %{buildroot}%{_sharedstatedir}/nova/CA
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/CA/{certs,crl,newcerts,projects,reqs}
touch %{buildroot}%{_sharedstatedir}/nova/CA/{cacert.pem,crl.pem,index.txt,openssl.cnf,serial}
install -d -m 750 %{buildroot}%{_sharedstatedir}/nova/CA/private
touch %{buildroot}%{_sharedstatedir}/nova/CA/private/cakey.pem

# Install config file
install -d -m 755 %{buildroot}%{_sysconfdir}/nova
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_sysconfdir}/nova/nova.conf

# Install initscripts for Nova services
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/openstack-nova-api
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/openstack-nova-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/openstack-nova-network
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/openstack-nova-objectstore
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/openstack-nova-scheduler
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/openstack-nova-volume
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_initrddir}/openstack-nova-direct-api
install -p -D -m 755 %{SOURCE18} %{buildroot}%{_initrddir}/openstack-nova-ajax-console-proxy
install -p -D -m 755 %{SOURCE19} %{buildroot}%{_initrddir}/openstack-nova-vncproxy

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/nova

# Install logrotate
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-nova

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/nova

# Install template files
install -p -D -m 644 nova/auth/novarc.template %{buildroot}%{_datarootdir}/nova/novarc.template
install -p -D -m 644 nova/cloudpipe/client.ovpn.template %{buildroot}%{_datarootdir}/nova/client.ovpn.template
install -p -D -m 644 nova/virt/libvirt.xml.template %{buildroot}%{_datarootdir}/nova/libvirt.xml.template
install -p -D -m 644 nova/virt/interfaces.template %{buildroot}%{_datarootdir}/nova/interfaces.template
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_datarootdir}/nova/interfaces.template

install -d -m 755 %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-nova.pkla

# Remove ajaxterm and various other tools
rm -fr %{buildroot}%{_datarootdir}/nova/{ajaxterm,euca-get-ajax-console,install_venv.py,nova-debug,pip-requires,clean-vlans,with_venv.sh,esx}

# Remove unneeded in production stuff
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}%{_bindir}/nova-combined
rm -f %{buildroot}/usr/share/doc/nova/README*

%pre
getent group nova >/dev/null || groupadd -r nova --gid 162
getent passwd nova >/dev/null || \
useradd --uid 162 -r -g nova -G nova,nobody,qemu -d %{_sharedstatedir}/nova -s /sbin/nologin \
-c "OpenStack Nova Daemons" nova
exit 0

%post
# Initialize the DB
if [ ! -f %{_sharedstatedir}/nova/nova.sqlite ]; then
    runuser -l -s /bin/bash -c 'nova-manage --flagfile=/dev/null --logdir=%{_localstatedir}/log/nova --state_path=%{_sharedstatedir}/nova db sync' nova
    chmod 600 %{_sharedstatedir}/nova/nova.sqlite
fi

# Register the services
for svc in api compute network objectstore scheduler volume direct-api ajax-console-proxy vncproxy; do
    /sbin/chkconfig --add openstack-nova-${svc}
done

%preun
if [ $1 -eq 0 ] ; then
    for svc in api compute network objectstore scheduler volume direct-api ajax-console-proxy vncproxy; do
        /sbin/service openstack-nova-${svc} stop >/dev/null 2>&1
        /sbin/chkconfig --del openstack-nova-${svc}
    done
fi

%postun
if [ "$1" -ge 1 ] ; then
    for svc in api compute network objectstore scheduler volume direct-api ajax-console-proxy vncproxy; do
        /sbin/service openstack-nova-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

%files
%doc LICENSE
%dir %{_sysconfdir}/nova
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/nova.conf
%config(noreplace) %{_sysconfdir}/nova/api-paste.ini
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-nova
%config(noreplace) %{_sysconfdir}/sudoers.d/nova
%config(noreplace) %{_sysconfdir}/polkit-1/localauthority/50-local.d/50-nova.pkla

%dir %attr(0755, nova, root) %{_localstatedir}/log/nova
%dir %attr(0755, nova, root) %{_localstatedir}/run/nova

%{_bindir}/nova-*
%{_initrddir}/openstack-nova-*
%{_datarootdir}/nova

%defattr(-, nova, nova, -)
%dir %{_sharedstatedir}/nova
%dir %{_sharedstatedir}/nova/buckets
%dir %{_sharedstatedir}/nova/images
%dir %{_sharedstatedir}/nova/instances
%dir %{_sharedstatedir}/nova/keys
%dir %{_sharedstatedir}/nova/networks
%dir %{_sharedstatedir}/nova/tmp
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/nova.sqlite

%dir %{_sharedstatedir}/nova/CA/
%dir %{_sharedstatedir}/nova/CA/certs
%dir %{_sharedstatedir}/nova/CA/crl
%dir %{_sharedstatedir}/nova/CA/newcerts
%dir %{_sharedstatedir}/nova/CA/projects
%dir %{_sharedstatedir}/nova/CA/reqs
%{_sharedstatedir}/nova/CA/*.sh
%{_sharedstatedir}/nova/CA/openssl.cnf.tmpl
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/cacert.pem
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/crl.pem
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/index.txt
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/openssl.cnf
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/serial
%dir %attr(0750, -, -) %{_sharedstatedir}/nova/CA/private
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/private/cakey.pem

%files -n python-nova
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/nova
%{python_sitelib}/nova-%{version}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc LICENSE doc/build/html
%endif

%changelog
* Mon Aug 29 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.4.d4
- Don't generate root CA during %post (#707199)
- The nobody group shouldn't own files in /var/lib/nova
- Add workaround for sphinx-build segfault

* Fri Aug 26 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.3.d4
- Update to diablo-4 milestone
- Use statically assigned uid:gid 162:162 (#732442)
- Collapse all sub-packages into openstack-nova; w/o upgrade path
- Reduce use of macros
- Rename stack to nova-stack
- Fix openssl.cnf.tmpl script-without-shebang rpmlint warning
- Really remove ajaxterm
- Mark polkit file as %config

* Mon Aug 22 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.2.1449bzr
- Remove dependency on python-novaclient

* Wed Aug 17 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.1.1449bzr
- Update to latest upstream.
- nova-import-canonical-imagestore has been removed
- nova-clear-rabbit-queues was added

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
