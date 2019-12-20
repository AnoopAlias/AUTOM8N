#!/bin/python

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

if form.getvalue('autofix_status'):

    if form.getvalue('autofix_status') == 'simple':
        terminal_call(installation_path+'/scripts/attempt_autofix.sh', 'Attempting Nginx AutoFix...', 'Nginx AutoFix Completed!')
        print_success('Nginx AutoFix Complete!')

    elif form.getvalue('autofix_status') == 'phpfpm':
        terminal_call(installation_path+'/scripts/init_backends.py autofix', 'Attempting AutoFix of PHP Application Server...', 'PHP Application Server AutoFix Completed!')
        print_success('PHP-FPM AutoFix Complete!')

else:
    print_forbidden()

print_simple_footer()
