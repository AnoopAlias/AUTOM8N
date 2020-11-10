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

if form.getvalue('run_installer') == 'enabled':
    terminal_call(installation_path+'/scripts/easy_php_setup.sh', 'Rebuilding native PHP support...', 'Native PHP support has been rebuilt!')
    print_success('Native PHP support has been rebuilt!')

else:
    print_forbidden()

print_simple_footer()
