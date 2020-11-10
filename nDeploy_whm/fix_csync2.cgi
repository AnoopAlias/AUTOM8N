#!/usr/bin/env python3

import cgi
import cgitb
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('mode'):
    if form.getvalue('mode') == 'reset':

        terminal_call(installation_path+'/scripts/fix_csync2_configsync.sh', 'Initiating Csync2 Hard Reset...', 'Csync2 Hard Reset Complete!')
        print_success('Csync2 Hard Reset Completed!')

    else:
        print_forbidden()
else:
    print_forbidden()

print_simple_footer()
