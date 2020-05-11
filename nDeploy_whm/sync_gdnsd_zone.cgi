#!/usr/bin/python

import cgi
import cgitb
import os
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


print_simple_header()

if form.getvalue('user'):
    if os.path.isfile(installation_path+'/conf/skip_geodns'):
        terminal_call(installation_path+'/scripts/cluster_dns_ensure_user.py '+form.getvalue('user'), 'Syncing DNS zones...', 'DNS zones synced successfully!')
    else:
        terminal_call(installation_path+'/scripts/cluster_gdnsd_ensure_user.py '+form.getvalue('user'), 'Syncing GeoDNS zones...', 'GeoDNS zones synced successfully!')
    print_success('DNS zones synced successfully!')
elif form.getvalue('action'):
    if form.getvalue('action') == 'enabled':
        terminal_call('touch '+installation_path+'/conf/DECLUSTER_DNSZONE', 'Enabling DNS cleanup lock...', 'DNS cleanup lock enabled!')
        print_success('DNS cleanup lock is set.Run sync zone now')
    elif form.getvalue('action') == 'disabled':
        silentremove(installation_path+'/conf/DECLUSTER_DNSZONE')
        print_success('DNS cleanup lock removed')
    else:
        print_forbidden()
else:
    print_forbidden()

print_simple_footer()
