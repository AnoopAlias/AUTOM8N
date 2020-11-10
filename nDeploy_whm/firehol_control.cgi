#!/usr/bin/env python3

import cgi
import cgitb
import subprocess
import os
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_error, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('ddos'):
    try:
        with open(os.devnull, 'w') as FNULL:
            subprocess.call(['systemctl', '--version'], stdout=FNULL, stderr=subprocess.STDOUT)
    except OSError:
        print_error('IPtables not compatible!')
    else:
        if form.getvalue('ddos') == 'enable':

            if os.path.isfile('/opt/nDeploy/conf/XTENDWEB_FIREHOL_SETUP_LOCK_DO_NOT_REMOVE'):
                terminal_call('sysctl -w net/ipv4/tcp_syncookies=1', 'Enabling SYNPROXY DDOS Mitigation')
                terminal_call('sysctl -w net/ipv4/tcp_timestamps=1')
                terminal_call('sysctl -w net/netfilter/nf_conntrack_tcp_loose=0')
                terminal_call('sysctl -w net/netfilter/nf_conntrack_max=2000000')
                terminal_call('echo 2000000 > /sys/module/nf_conntrack/parameters/hashsize')
                terminal_call('systemctl restart firehol.service','','SYNPROXY DDOS Mitigation is now enabled!')
                print_success('SYNPROXY DDOS Mitigation is now enabled!')
            else:
                print_error('FireHol Firewall not installed! <br>To install, see the <a target="_blank" href="help.txt">docs</a>.')

        elif form.getvalue('ddos') == 'disable':

            if os.path.isfile('/opt/nDeploy/conf/XTENDWEB_FIREHOL_SETUP_LOCK_DO_NOT_REMOVE'):
                terminal_call('systemctl stop firehol.service', 'Disabling SYNPROXY DDOS Mitigation...', 'SYNPROXY DDOS Mitigation is now disabled!')
                print_success('SYNPROXY DDOS Mitigation is now disabled!')
            else:
                print_error('FireHol Firewall not installed! <br>To install, see the <a target="_blank" href="help.txt">docs</a>.')
else:
    print_forbidden()

print_simple_footer()
