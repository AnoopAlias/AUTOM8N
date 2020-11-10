#!/usr/bin/env python3

import cgi
import cgitb
import os
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_warning, print_forbidden


__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Production"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('run_installer') == 'enabled':

    if os.path.isfile('/etc/nginx/conf.d/netdata.password'):

        terminal_call(installation_path+'/scripts/easy_netdata_setup.sh', 'Previous Netdata credentials detected. Reinstalling latest Netdata using current credentials...', 'Netdata has been reinstalled using existing credentials!')
        print_success('Netdata reinstalled!')

    elif form.getvalue('netdata_pass') != None:

        terminal_call(installation_path+'/scripts/easy_netdata_setup.sh '+form.getvalue('netdata_pass'), 'Netdata is being set up using netdata::'+form.getvalue('netdata_pass')+' for credentials. Please keep this data for your records...', 'Netdata has been reinstalled using existing the new credentials!')
        print_success('Netdata installed!')

    else:
        print_warning('Try again with credentials!')

elif form.getvalue('remove_netdata_creds') == 'enabled':
    os.remove('/etc/nginx/conf.d/netdata.password')
    print_success('Netdata credentials reset!')

else:
    print_forbidden()

print_simple_footer()
