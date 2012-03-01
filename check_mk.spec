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
Release:   %release_func 2
License:   GPL
Group:     System/Monitoring
Requires:  nagios, pnp4nagios
URL:       http://mathias-kettner.de/check_mk
Source:    check_mk-%{version}.tar.gz
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
script /etc/check_mk/sqlplus.sh to your needs.

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
DESTDIR=$R ./setup.sh --yes
rm -vf $R/etc/check_mk/*.mk-*

# Move check_mk apache config to the correct place
mv $R/etc/apache2 $R/etc/httpd

# install agent
mkdir -p $R/etc/xinetd.d
mkdir -p $R/usr/share/doc/check_mk_agent
install -m 644 COPYING ChangeLog AUTHORS $R/usr/share/doc/check_mk_agent
install -m 644 $R/usr/share/check_mk/agents/xinetd.conf $R/etc/xinetd.d/check_mk
install -m 644 $R/usr/share/check_mk/agents/xinetd_caching.conf $R/etc/xinetd.d/check_mk_caching
mkdir -p $R/usr/bin
install -m 755 $R/usr/share/check_mk/agents/check_mk_agent.linux $R/usr/bin/check_mk_agent
install -m 755 $R/usr/share/check_mk/agents/check_mk_caching_agent.linux $R/usr/bin/check_mk_caching_agent
install -m 755 $R/usr/share/check_mk/agents/waitmax $R/usr/bin
mkdir -p $R/usr/lib/check_mk_agent/plugins
mkdir -p $R/usr/lib/check_mk_agent/local

# logwatch and oracle extension
install -m 755 $R/usr/share/check_mk/agents/plugins/mk_* $R/usr/lib/check_mk_agent/plugins
install -m 755 $R/usr/share/check_mk/agents/logwatch.cfg $R/etc/check_mk
install -m 644 $R/usr/share/check_mk/agents/sqlplus.sh   $R/etc/check_mk

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/check_mk/main.mk
%config(noreplace) /etc/check_mk/multisite.mk
/etc/check_mk/conf.d/README
%config(noreplace) /etc/nagios/objects/*
/usr/bin/check_mk
/usr/bin/cmk
/usr/bin/mkp
%dir /usr/share/check_mk
/usr/share/check_mk/agents
/usr/share/check_mk/checks
/usr/share/check_mk/modules
/usr/share/check_mk/pnp-templates/*
/usr/share/check_mk/pnp-rraconf
/usr/share/doc/check_mk
%dir /var/lib/check_mk
%dir %attr(-,nagios,root) /var/lib/check_mk/counters
%dir %attr(-,nagios,root) /var/lib/check_mk/cache
%dir %attr(-,nagios,root) /var/lib/check_mk/logwatch
%dir %attr(-,apache,apache) /var/lib/check_mk/web
%dir /var/lib/check_mk/autochecks
%dir /var/lib/check_mk/precompiled
%dir /var/lib/check_mk/packages
/var/lib/check_mk/packages/check_mk

# Spaeter Subpaket draus machen
/usr/bin/unixcat
/usr/lib/check_mk/livestatus.o


%files agent
%config(noreplace) /etc/xinetd.d/check_mk
/usr/bin/check_mk_agent
/usr/bin/waitmax
/usr/share/doc/check_mk_agent
%dir /usr/lib/check_mk_agent/local
%dir /usr/lib/check_mk_agent/plugins

%files caching-agent
%config(noreplace) /etc/xinetd.d/check_mk_caching
/usr/bin/check_mk_agent
/usr/bin/check_mk_caching_agent
/usr/bin/waitmax
/usr/share/doc/check_mk_agent
%dir /usr/lib/check_mk_agent/local
%dir /usr/lib/check_mk_agent/plugins
%dir /etc/check_mk

%files agent-logwatch
/usr/lib/check_mk_agent/plugins/mk_logwatch
%config(noreplace) /etc/check_mk/logwatch.cfg

%files agent-oracle
/usr/lib/check_mk_agent/plugins/mk_oracle
%config(noreplace) /etc/check_mk/sqlplus.sh

%files web
/usr/share/check_mk/web
%config(noreplace) /etc/httpd/conf.d/*
