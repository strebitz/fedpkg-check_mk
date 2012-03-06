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

Summary:   Nagios agent and check plugin by Mathias Kettner for efficient remote monitoring
Name:      check_mk
Version:   1.1.12p7
Release:   3 %{dist}
License:   GPL
Group:     System/Monitoring
Requires:  nagios, nagios-plugins, pnp4nagios
URL:       http://mathias-kettner.de/check_mk
Source:    http://mathias-kettner.de/download/check_mk-%{version}.tar.gz
AutoReq:   off
AutoProv:  off
BuildArch: noarch


%description
check_mk is a xinetd-based remote agent for monitoring Linux and Unix-Servers
with Nagios plus a Check-Plugin check_mk written in Python.
This package is only needed on the Nagios server.

%package agent
Group:     System/Monitoring
Requires:  xinetd
Summary: Linux-Agent for check_mk
AutoReq:   off
AutoProv:  off
Conflicts: check_mk-caching-agent
%description agent
This package contains the agent for check_mk. Install this on
all Linux machines you want to monitor via check_mk. You'll need
xinetd to run this agent.

%package caching-agent
Group:     System/Monitoring
Requires:  xinetd
Summary: Caching Linux-Agent for check_mk
AutoReq:   off
AutoProv:  off
Conflicts: check_mk-agent
%description caching-agent
This package contains the agent for check_mk with an xinetd
configuration that wrap the agent with the check_mk_caching_agent
wrapper. Use it when doing fully redundant monitoring, where
an agent is regularily polled by more than one monitoring
server.

%package agent-logwatch
Group:     System/Monitoring
Requires:  check_mk-agent, python
Summary: Logwatch-Plugin for check_mk agent
AutoReq:   off
AutoProv:  off
%description agent-logwatch
The logwatch plugin for the check_mk agent allows you to monitor
logfiles on Linux and UNIX. In one or more configuration files you
specify patters for log messages that should raise a warning or
critical state. For each logfile the current position is remembered.
This way only new messages are being sent.

%package agent-oracle
Group:     System/Monitoring
Requires:  check_mk-agent
Summary: ORACLE-Plugin for check_mk agent
AutoReq:   off
AutoProv:  off
%description agent-oracle
The ORACLE plugin for the check_mk agent allows you to monitor
several aspects of ORACLE databases. You need to adapt the
script %{_sysconfdir}/check_mk/sqlplus.sh to your needs.

%package web
Group:     System/Monitoring
Requires:  python
Summary: Check_mk web pages
AutoReq:   off
AutoProv:  off
%description web
This package contains the Check_mk webpages. They allow you to
search for services and apply Nagios commands to the search results.

%prep
%setup -q

%install
R=$RPM_BUILD_ROOT
rm -rf $R

export bindir="%{_bindir}"
export confdir="%{_sysconfdir}/check_mk"
export checksdir="%{_datarootdir}/check_mk/checks"
export modulesdir="%{_datarootdir}/check_mk/modules"
export web_dir="%{_datarootdir}check_mk/web"
export localedir="%{_datarootdir}/check_mk/locale"
export docdir="%{_datarootdir}/doc/check_mk"
export checkmandir="%{_datarootdir}/doc/check_mk/checks"
export vardir="%{_sharedstatedir}/check_mk"
export agentsdir="%{_datarootdir}/check_mk/agents"
export agentslibdir="%{_libdir}/check_mk_agent"
export agentsconfdir="%{_sysconfdir}/check_mk"
export nagiosuser="nagios"
export wwwuser="apache"
export wwwgroup="nagios"
export nagios_binary="%{_sbindir}/nagios"
export nagios_config_file="%{_sysconfdir}/nagios/nagios.cfg"
export nagconfdir="%{_sysconfdir}/nagios/objects"
export nagios_startscript="%{_sysconfdir}/init.d/nagios"
export nagpipe="%{_localstatedir}/spool/nagios/cmd/nagios.cmd"
export check_result_path="/usr/local/nagios%{_localstatedir}/spool/checkresults"
export nagios_status_file="%{_localstatedir}/log/nagios/status.dat"
export check_icmp_path="%{_libdir}/nagios/plugins/check_icmp"
export url_prefix="/"
export apache_config_dir="%{_sysconfdir}/httpd/conf.d"
export htpasswd_file="%{_sysconfdir}/nagios/htpasswd.users"
export nagios_auth_name="Nagios Access"
export pnptemplates='%{_datarootdir}/check_mk/pnp-templates'
export pnprraconf='%{_datarootdir}/check_mk/pnp-rraconf'
export enable_livestatus='yes'
export libdir='%{_libdir}/check_mk'
export livesock='%{_localstatedir}/spool/nagios/socket/live'
export livebackendsdir='%{_datarootdir}/check_mk/livestatus'

DESTDIR=$R ./setup.sh --yes
rm -vf $R%{_sysconfdir}/check_mk/*.mk-*

# install agent
mkdir -p $R%{_sysconfdir}/xinetd.d
mkdir -p $R%{_datarootdir}/doc/check_mk_agent
install -m 644 COPYING ChangeLog AUTHORS $R%{_datarootdir}/doc/check_mk_agent
install -m 644 $R%{_datarootdir}/check_mk/agents/xinetd.conf $R%{_sysconfdir}/xinetd.d/check_mk
install -m 644 $R%{_datarootdir}/check_mk/agents/xinetd_caching.conf $R%{_sysconfdir}/xinetd.d/check_mk_caching
mkdir -p $R%{_bindir}
install -m 755 $R%{_datarootdir}/check_mk/agents/check_mk_agent.linux $R%{_bindir}/check_mk_agent
install -m 755 $R%{_datarootdir}/check_mk/agents/check_mk_caching_agent.linux $R%{_bindir}/check_mk_caching_agent
install -m 755 $R%{_datarootdir}/check_mk/agents/waitmax $R%{_bindir}
mkdir -p $R%{_libdir}/check_mk_agent/plugins
mkdir -p $R%{_libdir}/check_mk_agent/local

# logwatch and oracle extension
install -m 755 $R%{_datarootdir}/check_mk/agents/plugins/mk_* $R%{_libdir}/check_mk_agent/plugins
install -m 755 $R%{_datarootdir}/check_mk/agents/logwatch.cfg $R%{_sysconfdir}/check_mk
install -m 644 $R%{_datarootdir}/check_mk/agents/sqlplus.sh   $R%{_sysconfdir}/check_mk

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/check_mk/main.mk
%config(noreplace) %{_sysconfdir}/check_mk/multisite.mk
%{_sysconfdir}/check_mk/conf.d/README
%config(noreplace) %{_sysconfdir}/nagios/objects/*
%{_bindir}/check_mk
%{_bindir}/cmk
%{_bindir}/mkp
%dir %{_datarootdir}/check_mk
%{_datarootdir}/check_mk/agents
%{_datarootdir}/check_mk/checks
%{_datarootdir}/check_mk/modules
%{_datarootdir}/check_mk/pnp-templates/*
%{_datarootdir}/check_mk/pnp-rraconf
%{_datarootdir}/doc/check_mk
%dir %{_sharedstatedir}/check_mk
%dir %attr(-,nagios,root) %{_sharedstatedir}/check_mk/counters
%dir %attr(-,nagios,root) %{_sharedstatedir}/check_mk/cache
%dir %attr(-,nagios,root) %{_sharedstatedir}/check_mk/logwatch
%dir %attr(-,apache,apache) %{_sharedstatedir}/check_mk/web
%dir %{_sharedstatedir}/check_mk/autochecks
%dir %{_sharedstatedir}/check_mk/precompiled
%dir %{_sharedstatedir}/check_mk/packages
%{_sharedstatedir}/check_mk/packages/check_mk

# Spaeter Subpaket draus machen
%{_bindir}/unixcat
%{_libdir}/check_mk/livestatus.o


%files agent
%config(noreplace) %{_sysconfdir}/xinetd.d/check_mk
%{_bindir}/check_mk_agent
%{_bindir}/waitmax
%{_datarootdir}/doc/check_mk_agent
%dir %{_libdir}/check_mk_agent/local
%dir %{_libdir}/check_mk_agent/plugins

%files caching-agent
%config(noreplace) %{_sysconfdir}/xinetd.d/check_mk_caching
%{_bindir}/check_mk_agent
%{_bindir}/check_mk_caching_agent
%{_bindir}/waitmax
%{_datarootdir}/doc/check_mk_agent
%dir %{_libdir}/check_mk_agent/local
%dir %{_libdir}/check_mk_agent/plugins
%dir %{_sysconfdir}/check_mk

%files agent-logwatch
%{_libdir}/check_mk_agent/plugins/mk_logwatch
%config(noreplace) %{_sysconfdir}/check_mk/logwatch.cfg

%files agent-oracle
%{_libdir}/check_mk_agent/plugins/mk_oracle
%config(noreplace) %{_sysconfdir}/check_mk/sqlplus.sh

%files web
%{_datarootdir}/check_mk/web
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*
