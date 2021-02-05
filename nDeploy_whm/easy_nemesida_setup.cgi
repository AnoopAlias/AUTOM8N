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

if form.getvalue('run_nemesida_installer') == 'enabled':

    if os.path.isfile('/etc/nginx/modules/ngx_http_waf_module.so'):

        terminal_call(installation_path+'/scripts/easy_nemesida_waf_setup.sh', 'Previous Nemesida install detected. Reinstalling latest Nemesida WAF from their linux repo...', 'Nemesida has been reinstalled!')
        print_success('Latest Nemesida WAF reinstalled!')

    else:

        terminal_call(installation_path+'/scripts/easy_nemesida_waf_setup.sh', 'Installing latest Nemesida WAF from their linux repo...', 'Nemesida has been installed!')
        print_success('Latest Namesida WAF installed!')

else:
    print_forbidden()

print_simple_footer()
