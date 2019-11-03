#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import subprocess
import os
import platform
import psutil
import signal
from commoninclude import print_simple_header, print_simple_footer


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
        commoninclude.print_error('iptables not compatible')
    else:
        if form.getvalue('ddos') == 'enable':
            if os.path.isfile('/opt/nDeploy/conf/XTENDWEB_FIREHOL_SETUP_LOCK_DO_NOT_REMOVE'):
                subprocess.call('sysctl -w net/ipv4/tcp_syncookies=1', shell=True)
                subprocess.call('sysctl -w net/ipv4/tcp_timestamps=1', shell=True)
                subprocess.call('sysctl -w net/netfilter/nf_conntrack_tcp_loose=0', shell=True)
                subprocess.call('sysctl -w net/netfilter/nf_conntrack_max=2000000', shell=True)
                subprocess.call('echo 2000000 > /sys/module/nf_conntrack/parameters/hashsize', shell=True)
                subprocess.call(['systemctl', 'restart', 'firehol.service'])
                commoninclude.print_success('SYNPROXY DDOS Mitigation is now enabled')
            else:
                commoninclude.print_error('FireHol firewall not installed')
                print('<div class="alert alert-info">')
                print('<ul class="list-unstyled text-left">')
                print('<li class="mb-1">To install see <a class="btn btn-primary" target="_blank" href="help.txt"> docs <i class="fas fa-book-open"></i></a></li>')
                print('</ul>')
                print('</div>')
        elif form.getvalue('ddos') == 'disable':
            if os.path.isfile('/opt/nDeploy/conf/XTENDWEB_FIREHOL_SETUP_LOCK_DO_NOT_REMOVE'):
                subprocess.call(['systemctl', 'stop', 'firehol.service'])
                commoninclude.print_success('SYNPROXY DDOS Mitigation is now disabled')
            else:
                commoninclude.print_error('FireHol firewall not installed')
                print('<div class="alert alert-info">')
                print('<ul class="list-unstyled text-left">')
                print('<li class="mb-1">To install see <a class="btn btn-primary" target="_blank" href="help.txt"> docs <i class="fas fa-book-open"></i></a></li>')
                print('</ul>')
                print('</div>')
else:
    commoninclude.print_forbidden()

print_simple_footer()
