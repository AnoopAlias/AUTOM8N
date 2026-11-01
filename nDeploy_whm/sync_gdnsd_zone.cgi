#!/usr/bin/env python3

import cgi
import cgitb
import os
import re
import shlex
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

user = form.getvalue('user')
action = form.getvalue('action')

if user:
    # Sanitize username - strictly alphanumeric and safe characters
    if re.match(r'^[a-zA-Z0-9_\.\-]+$', user):
        safe_user = shlex.quote(user)
        if os.path.isfile(installation_path+'/conf/skip_geodns'):
            terminal_call(installation_path+'/scripts/cluster_dns_ensure_user.py '+safe_user, 'Syncing DNS zones...', 'DNS zones synced successfully!')
        else:
            terminal_call(installation_path+'/scripts/cluster_gdnsd_ensure_user.py '+safe_user, 'Syncing GeoDNS zones...', 'GeoDNS zones synced successfully!')
        print_success('DNS zones synced successfully!')
    else:
        print_forbidden()
elif action:
    # Sanitize action against allowlist
    if action == 'enabled':
        terminal_call('touch '+installation_path+'/conf/DECLUSTER_DNSZONE', 'Enabling DNS cleanup lock...', 'DNS cleanup lock enabled!')
        print_success('DNS cleanup lock is set.Run sync zone now')
    elif action == 'disabled':
        silentremove(installation_path+'/conf/DECLUSTER_DNSZONE')
        print_success('DNS cleanup lock removed')
    else:
        print_forbidden()
else:
    print_forbidden()

print_simple_footer()
