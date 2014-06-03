# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2010             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

%{!?release_func:%global release_func() %1%{?dist}}

Summary:        Nagios agent and check plugin by Mathias Kettner for efficient remote monitoring
Name:           check_mk
Version:        1.2.2p3
Release:        5%{dist}
License:        GPL
Group:          Applications/System
Requires:       nagios, nagios-plugins-icmp, pnp4nagios
URL:            http://mathias-kettner.de/check_mk
Source:         http://archive.mathias-kettner.de/check_mk/check_mk-%{version}.tar.gz
Source1:        check_mk.sudo
Source2:        mk-livestatus.cfg
Source3:        pnp4nagios_perfdata.cfg
Source4:        livestatus.xinetd
Patch0:         0001-check_mk_agent-linux-ipmi-sensors-also-check-Power_S.patch
Patch1:         0001-checks-ipmi-sensors-skip-sensors-in-NA-Unknown-state.patch
Patch2:         0002-checks-ipmi-sensors-ignore-sensors-in-NA-on-discover.patch
Patch3:         setup-script.patch
Patch4:         check_mk_agent.linux.ntpq-patch
AutoReq:        off
AutoProv:       off
ExclusiveArch:  i386, x86_64


%description
check_mk is a xinetd-based remote agent for monitoring Linux and Unix-Servers
with Nagios plus a Check-Plugin check_mk written in Python.
This package is only needed on the Nagios server.

%package agent
Group:     Applications/System
Requires:  xinetd
Summary: Linux-Agent for check_mk
AutoReq:   off
AutoProv:  off
BuildArch: noarch
Conflicts: check_mk-caching-agent
%description agent
This package contains the agent for check_mk. Install this on
all Linux machines you want to monitor via check_mk. You'll need
xinetd to run this agent.

%package caching-agent
Group:     Applications/System
Requires:  xinetd
Summary: Caching Linux-Agent for check_mk
AutoReq:   off
AutoProv:  off
BuildArch: noarch
Conflicts: check_mk-agent
%description caching-agent
This package contains the agent for check_mk with an xinetd
configuration that wrap the agent with the check_mk_caching_agent
wrapper. Use it when doing fully redundant monitoring, where
an agent is regularily polled by more than one monitoring
server.

%package agent-apache_status
Group:     Applications/System
Requires:  check_mk-agent, httpd, python
Summary: apache_status-Plugin for check_mk agent
AutoReq:   off
AutoProv:  off
BuildArch: noarch
%description agent-apache_status
Fetches the server-status page from detected or configured apache
processes to gather status information about this apache process.

To make this agent plugin work you have to load the status_module
into your apache process. It is also needed to enable the "server-status"
handler below the URL "/server-status".

By default this plugin tries to detect all locally running apache processes
and to monitor them. If this is not good for your environment you might
create an apache_status.conf file in MK_CONFDIR and populate the servers
list to prevent executing the detection mechanism.

It is also possible to override or extend the ssl_ports variable to make the
check contact other ports than 443 with HTTPS requests.

%package agent-dmi_sysinfo
Group:     Applications/System
Requires:  check_mk-agent, dmidecode, python
Summary: dmi_sysinfo-Plugin for check_mk agent
AutoReq:   off
AutoProv:  off
BuildArch: noarch
%description agent-dmi_sysinfo
The dmi_sysinfo (Desktop Management Interface) plugin for the check_mk agent allows you to monitor
dmi system information on Linux.

%package agent-dmraid
Group:     Applications/System
Requires:  check_mk-agent, dmraid, python
Summary: dmraid-Plugin for check_mk agent
AutoReq:   off
AutoProv:  off
BuildArch: noarch
%description agent-dmraid
The dmraid (Device-mapper RAID tool) plugin for the check_mk agent allows you to monitor
dmraid information on Linux.

%package agent-logwatch
Group:     Applications/System
Requires:  check_mk-agent, python
Summary: Logwatch-Plugin for check_mk agent
AutoReq:   off
AutoProv:  off
BuildArch: noarch
%description agent-logwatch
The logwatch plugin for the check_mk agent allows you to monitor
logfiles on Linux and UNIX. In one or more configuration files you
specify patters for log messages that should raise a warning or
critical state. For each logfile the current position is remembered.
This way only new messages are being sent.

%package agent-mysql
Group:     Applications/System
Requires:  check_mk-agent, mysql, python
Summary: mysql-Plugin for check_mk agent
AutoReq:   off
AutoProv:  off
BuildArch: noarch
%description agent-mysql
The mk_mysql plugin for the check_mk agent allows you to monitor
mysql information.
 
%package agent-nfsexports
Group:     Applications/System
Requires:  check_mk-agent, python
Summary: nfsexports-Plugin for check_mk agent
AutoReq:   off
AutoProv:  off
BuildArch: noarch
%description agent-nfsexports
The nfsexports plugin for the check_mk agent allows you to monitor
NFS exports information.
 
%package agent-oracle
Group:     Applications/System
Requires:  check_mk-agent
Summary: ORACLE-Plugin for check_mk agent
AutoReq:   off
AutoProv:  off
BuildArch: noarch
%description agent-oracle
The ORACLE plugin for the check_mk agent allows you to monitor
several aspects of ORACLE databases. You need to adapt the
script %{_sysconfdir}/check_mk/sqlplus.sh to your needs.

%package agent-postgresql
Group:     Applications/System
Requires:  check_mk-agent, postgresql, python
Summary: postgresql-Plugin for check_mk agent
AutoReq:   off
AutoProv:  off
BuildArch: noarch
%description agent-postgresql
The mk_postgres plugin for the check_mk agent allows you to monitor
postgres information.

%package agent-smart
Group:     Applications/System
Requires:  check_mk-agent, python, smartmontools
Summary: smart-Plugin for check_mk agent
AutoReq:   off
AutoProv:  off
BuildArch: noarch
%description agent-smart
The smart plugin for the check_mk agent allows you to monitor
SMART capable hard disks.

%package livestatus
Group:     Applications/System
Requires:  check_mk
Summary: Check_mk livestatus
AutoReq:   off
AutoProv:  off
%description livestatus
Just as NDO, Livestatus make use of the Nagios Event Broker API and loads a binary module into your Nagios process. But other then NDO, Livestatus does not actively write out data. Instead, it opens a socket by which data can be retrieved on demand.

The socket allows you to send a request for hosts, services or other pieces of data and get an immediate answer. The data is directly read from Nagios' internal data structures. Livestatus does not create its own copy of that data. 

%package web
Group:     Applications/System
Requires:  python, mod_python
Summary: Check_mk web pages
AutoReq:   off
AutoProv:  off
BuildArch: noarch
%description web
This package contains the Check_mk webpages. They allow you to
search for services and apply Nagios commands to the search results.

%prep
%setup -q

# fix the path to livestatus.o in mk-livestatus.cfg
sed -i -e 's:$libdir:\%{_libdir}:' %{SOURCE2} 

# fix sudo command for check_mk automation
sed -i 's/$(id -un)/root/' ./setup.sh

# patch setup script
patch -p3 ./setup.sh < %{PATCH3}

%install
R=$RPM_BUILD_ROOT
rm -rf $R

export bindir="%{_bindir}"
export confdir="%{_sysconfdir}/check_mk"
export sharedir="%{_datadir}/check_mk"
export checksdir="%{_datadir}/check_mk/checks"
export modulesdir="%{_datadir}/check_mk/modules"
export notificationsdir="%{_datadir}/check_mk/notifications"
export web_dir="%{_datadir}/check_mk/web"
export localedir="%{_datadir}/check_mk/locale"
export docdir="%{_datadir}/doc/check_mk"
export checkmandir="%{_datadir}/doc/check_mk/checks"
export vardir="%{_sharedstatedir}/check_mk"
export agentsdir="%{_datadir}/check_mk/agents"
export agentslibdir="%{_datadir}/check_mk_agent"
export agentsconfdir="%{_sysconfdir}/check_mk"
export nagiosuser="nagios"
export wwwuser="apache"
export wwwgroup="nagios"
export nagios_binary="%{_sbindir}/nagios"
export nagios_config_file="%{_sysconfdir}/nagios/nagios.cfg"
export nagconfdir="%{_sysconfdir}/nagios/conf.d"
export nagios_startscript="%{_sysconfdir}/init.d/nagios"
export nagpipe="%{_localstatedir}/spool/nagios/cmd/nagios.cmd"
export check_result_path="%{_localstatedir}/log/nagios/spool/checkresults"
export nagios_status_file="%{_localstatedir}/log/nagios/status.dat"
export check_icmp_path="%{_libdir}/nagios/plugins/check_icmp"
export url_prefix="/"
export apache_config_dir="%{_sysconfdir}/httpd/conf.d"
export htpasswd_file="%{_sysconfdir}/nagios/passwd"
export nagios_auth_name="Nagios Access"
export pnptemplates='%{_datadir}/check_mk/pnp-templates'
export pnprraconf='%{_datadir}/check_mk/pnp-rraconf'
export enable_livestatus='yes'
export libdir='%{_libdir}/check_mk'
export livesock='%{_localstatedir}/spool/nagios/socket/live'
export livebackendsdir='%{_datadir}/check_mk/livestatus'

DESTDIR=$R ./setup.sh --yes
rm -vf $R%{_sysconfdir}/check_mk/*.mk-*

# patches must be apllied here - source tarball contains sub tarballs which are extraced during setup
# patch check_mk_agent.linux: ipmi sensors: also check Power_Supply
patch -p3 $R%{_datadir}/check_mk/agents/check_mk_agent.linux < %{PATCH0}

# patch check_mk_agent.linux: disable reverse DNS resolve for ntpq requests which fail too often
patch -p3 $R%{_datadir}/check_mk/agents/check_mk_agent.linux < %{PATCH4} 

# checks: ipmi sensors: skip sensors in NA Unknown state
patch -p3 $R%{_datadir}/check_mk/checks/ipmi_sensors < %{PATCH1}

# checks: ipmi sensors: ignore sensors in NA or in transition_to_Running on discover
patch -p3 $R%{_datadir}/check_mk/checks/ipmi_sensors < %{PATCH2}

# install agent
mkdir -p $R%{_sysconfdir}/xinetd.d
mkdir -p $R%{_datadir}/doc/check_mk_agent
install -m 0644 COPYING ChangeLog AUTHORS $R%{_datadir}/doc/check_mk_agent
install -m 0644 $R%{_datadir}/check_mk/agents/xinetd.conf $R%{_sysconfdir}/xinetd.d/check_mk
install -m 0644 $R%{_datadir}/check_mk/agents/xinetd_caching.conf $R%{_sysconfdir}/xinetd.d/check_mk_caching
mkdir -p $R%{_bindir}
install -m 0755 $R%{_datadir}/check_mk/agents/check_mk_agent.linux $R%{_bindir}/check_mk_agent
install -m 0755 $R%{_datadir}/check_mk/agents/check_mk_caching_agent.linux $R%{_bindir}/check_mk_caching_agent
install -m 0755 $R%{_datadir}/check_mk/agents/waitmax $R%{_bindir}
mkdir -p $R%{_datadir}/check_mk_agent/plugins
mkdir -p $R%{_datadir}/check_mk_agent/local

# logwatch and oracle extension
mkdir -p $R%{_libdir}/check_mk_agent/plugins
mkdir -p $R%{_libdir}/check_mk_agent/local
install -m 0755 $R%{_datadir}/check_mk/agents/plugins/mk_logwatch $R%{_datadir}/check_mk_agent/plugins
install -m 0755 $R%{_datadir}/check_mk/agents/plugins/mk_oracle $R%{_datadir}/check_mk_agent/plugins
ln -s /usr/share/check_mk_agent/plugins/mk_logwatch $R%{_libdir}/check_mk_agent/plugins
ln -s /usr/share/check_mk_agent/plugins/mk_oracle $R%{_libdir}/check_mk_agent/plugins
install -m 0755 $R%{_datadir}/check_mk/agents/logwatch.cfg $R%{_sysconfdir}/check_mk
install -m 0644 $R%{_datadir}/check_mk/agents/sqlplus.sh   $R%{_sysconfdir}/check_mk

# install some more agent plugins
install -m 0755 $R%{_datadir}/check_mk/agents/plugins/apache_status $R%{_datadir}/check_mk_agent/plugins
install -m 0755 $R%{_datadir}/check_mk/agents/plugins/dmi_sysinfo $R%{_datadir}/check_mk_agent/plugins
install -m 0755 $R%{_datadir}/check_mk/agents/plugins/dmraid $R%{_datadir}/check_mk_agent/plugins
install -m 0755 $R%{_datadir}/check_mk/agents/plugins/mk_mysql $R%{_datadir}/check_mk_agent/plugins
install -m 0755 $R%{_datadir}/check_mk/agents/plugins/mk_postgres $R%{_datadir}/check_mk_agent/plugins
install -m 0755 $R%{_datadir}/check_mk/agents/plugins/nfsexports $R%{_datadir}/check_mk_agent/plugins
install -m 0755 $R%{_datadir}/check_mk/agents/plugins/smart $R%{_datadir}/check_mk_agent/plugins

# install livestatus configuration for nagios and xinetd service
install -m 0644 %{SOURCE2} $R%{_sysconfdir}/nagios
install -m 0644 %{SOURCE4} $R%{_sysconfdir}/xinetd.d/livestatus

# install check_mk sudoers file and config required for WATO
mkdir -p $R%{_sysconfdir}/check_mk/conf.d/wato
mkdir -p $R%{_sysconfdir}/check_mk/multisite.d/wato
mkdir -p $R%{_sysconfdir}/sudoers.d
mkdir -p $R%{_sharedstatedir}/check_mk/tmp
mkdir -p $R%{_sharedstatedir}/check_mk/wato
install -m 0440 %{SOURCE1} $R%{_sysconfdir}/sudoers.d/check_mk

# create directory used for the mk-livestatus broker module socket
mkdir -p $R%{_localstatedir}/spool/nagios/socket

# install pnp4nagios_perfdata configuration
install -m 0644 %{SOURCE3} $R%{_sysconfdir}/nagios/conf.d/pnp4nagios_perfdata.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/check_mk/main.mk
%config(noreplace) %{_sysconfdir}/check_mk/multisite.mk
%{_sysconfdir}/check_mk/conf.d/README
%config(noreplace) %{_sysconfdir}/nagios/conf.d/*
%{_bindir}/check_mk
%{_bindir}/cmk
%{_bindir}/mkp
%dir %{_datadir}/check_mk
%{_datadir}/check_mk/agents
%{_datadir}/check_mk/checks
%{_datadir}/check_mk/modules
%{_datadir}/check_mk/notifications
%{_datadir}/check_mk/pnp-templates/*
%{_datadir}/check_mk/check_mk_templates.cfg
%{_datadir}/doc/check_mk
%dir %{_sharedstatedir}/check_mk
%dir %attr(-,nagios,nagios) %{_sharedstatedir}/check_mk/counters
%dir %attr(-,nagios,nagios) %{_sharedstatedir}/check_mk/cache
%dir %attr(-,nagios,nagios) %{_sharedstatedir}/check_mk/logwatch
%dir %attr(-,nagios,nagios) %{_sharedstatedir}/check_mk/notify
%dir %{_sharedstatedir}/check_mk/autochecks
%dir %{_sharedstatedir}/check_mk/precompiled
%dir %{_sharedstatedir}/check_mk/packages
%{_sharedstatedir}/check_mk/packages/check_mk


%files livestatus
%{_bindir}/unixcat
%{_libdir}/check_mk/livestatus.o
%{_libdir}/check_mk/livecheck
%dir %attr(-,nagios,nagios) %{_localstatedir}/spool/nagios/socket
%config(noreplace) %{_sysconfdir}/nagios/mk-livestatus.cfg
%config(noreplace) %{_sysconfdir}/xinetd.d/livestatus


%files agent
%config(noreplace) %{_sysconfdir}/xinetd.d/check_mk
%{_bindir}/check_mk_agent
%{_bindir}/waitmax
%{_datadir}/doc/check_mk_agent
%dir %{_datadir}/check_mk_agent/local
%dir %{_datadir}/check_mk_agent/plugins


%files caching-agent
%config(noreplace) %{_sysconfdir}/xinetd.d/check_mk_caching
%{_bindir}/check_mk_agent
%{_bindir}/check_mk_caching_agent
%{_bindir}/waitmax
%{_datadir}/doc/check_mk_agent
%dir %{_datadir}/check_mk_agent/local
%dir %{_datadir}/check_mk_agent/plugins
%dir %{_sysconfdir}/check_mk


%files agent-apache_status
%{_datadir}/check_mk_agent/plugins/apache_status


%files agent-dmi_sysinfo
%{_datadir}/check_mk_agent/plugins/dmi_sysinfo


%files agent-dmraid
%{_datadir}/check_mk_agent/plugins/dmraid


%files agent-logwatch
%{_libdir}/check_mk_agent/plugins/mk_logwatch
%{_datadir}/check_mk_agent/plugins/mk_logwatch
%config(noreplace) %{_sysconfdir}/check_mk/logwatch.cfg


%files agent-mysql
%{_datadir}/check_mk_agent/plugins/mk_mysql


%files agent-nfsexports
%{_datadir}/check_mk_agent/plugins/nfsexports


%files agent-oracle
%{_libdir}/check_mk_agent/plugins/mk_oracle
%{_datadir}/check_mk_agent/plugins/mk_oracle
%config(noreplace) %{_sysconfdir}/check_mk/sqlplus.sh


%files agent-postgresql
%{_datadir}/check_mk_agent/plugins/mk_postgres


%files agent-smart
%{_datadir}/check_mk_agent/plugins/smart


%files web
%dir %attr(-,apache,nagios) %{_sysconfdir}/check_mk/conf.d
%dir %attr(2755,apache,nagios) %{_sysconfdir}/check_mk/conf.d/wato
%dir %attr(-,apache,nagios) %{_sysconfdir}/check_mk/multisite.d
%dir %attr(-,apache,nagios) %{_sysconfdir}/check_mk/multisite.d/wato
%config(noreplace) %attr(-,apache,nagios) %{_sysconfdir}/nagios/auth.serials
%config(noreplace) %{_sysconfdir}/sudoers.d/check_mk
%{_datadir}/check_mk/web
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*
%dir %attr(-,apache,nagios) %{_sharedstatedir}/check_mk/tmp
%dir %attr(-,apache,nagios) %{_sharedstatedir}/check_mk/wato
%dir %attr(-,apache,nagios) %{_sharedstatedir}/check_mk/web


%post
chown apache:apache %{_sysconfdir}/nagios/passwd


### changelog ###
%changelog
* Tue Jun 3 2014 Sebastian Trebitz <s.trebitz@mondialtelecom.be> - 1.2.2p3-5
- patch check_mk_agent.linux to disable reverse DNS lookups for ntpq requests which fail too often

* Fri May 30 2014 Sebastian Trebitz <s.trebitz@mondialtelecom.be> - 1.2.2p3-4
- set 'setgid' flag on dir %{_sysconfdir}/check_mk/conf.d/wato
