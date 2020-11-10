#!/usr/bin/env python3

import cgitb
import cgi
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

    if os.path.isfile('/etc/nginx/conf.d/glances.password'):

        terminal_call(installation_path+'/scripts/easy_glances_setup.sh', 'Previous Glances credentials detected. Reinstalling latest Glances using current credentials...', 'Glances has been reinstalled using existing credentials!')
        print_success('Glances reinstalled!')

    elif form.getvalue('glances_pass') != None:

        terminal_call(installation_path+'/scripts/easy_glances_setup.sh '+form.getvalue('glances_pass'), 'Glances is being set up using glances::'+form.getvalue('glances_pass')+' for credentials. Please keep this data for your records...', 'Glances has been reinstalled using the new credentials!')
        print_success('Glances installed!')

    else:
        print_warning('Try again with credentials!')

elif form.getvalue('remove_glances_creds') == 'enabled':
    os.remove('/etc/nginx/conf.d/glances.password')
    print_success('Glances credentials reset!')

else:
    print_forbidden()

print_simple_footer()
