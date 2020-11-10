#!/usr/bin/env python3

import cgi
import cgitb
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_forbidden


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

if form.getvalue('plugin_status') == 'enable':
    terminal_call(installation_path+'/scripts/cpanel-nDeploy-setup.sh enable', 'Enabling Plugin...', 'Plugin Enabled!')
    print_success('Plugin successfuly enabled!')

elif form.getvalue('plugin_status') == 'disable':
    terminal_call(installation_path+'/scripts/cpanel-nDeploy-setup.sh disable', 'Disabling Plugin...', 'Plugin Disabled!')
    print_success('Plugin successfully disabled...')

else:
    print_forbidden()

print_simple_footer()
