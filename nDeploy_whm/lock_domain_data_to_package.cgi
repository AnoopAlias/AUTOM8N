#!/usr/bin/env python3

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

if form.getvalue('package_lock'):
    if form.getvalue('package_lock') == 'enabled':

        terminal_call('touch '+installation_path+'/conf/lock_domaindata_to_package', 'Enabling NGINX package lock...', 'NGINX package lock enabled!')
        print_success('NGINX settings will change with cPanel package upgrades/downgrades!')

    elif form.getvalue('package_lock') == 'disabled':

        silentremove(installation_path+'/conf/lock_domaindata_to_package')
        print_success('NGINX settings will be preserved throughout cPanel package changes!')

else:
    print_forbidden()

print_simple_footer()
