#!/usr/bin/env python3

import cgitb
import cgi
import os
from commoninclude import print_simple_header, print_simple_footer, print_success, print_forbidden


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

if form.getvalue('autoswitch'):

    if form.getvalue('autoswitch') == 'enable':
        os.rename(installation_path + '/conf/autoswitch.disabled', installation_path + '/conf/autoswitch.enabled')
        print_success('Autoswitch has been enabled for cPanel!')

    elif form.getvalue('autoswitch') == 'disable':
        os.rename(installation_path + '/conf/autoswitch.enabled', installation_path + '/conf/autoswitch.disabled')
        print_success('Autoswitch has been disabled for cPanel!')

else:
    print_forbidden()

print_simple_footer()
