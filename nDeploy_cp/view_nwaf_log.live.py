#!/usr/bin/env python3

import os
import cgi
import cgitb
import subprocess
from commoninclude import print_simple_header, print_simple_footer, close_cpanel_liveapisock, print_success, print_error, terminal_call


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

cpanelhome = os.environ['HOME']
close_cpanel_liveapisock()
form = cgi.FieldStorage()

print_simple_header()

nwaf_log = cpanelhome+'/logs/nginx_error_log'
if os.path.isfile(nwaf_log):
    terminal_call('/usr/bin/tail -100 '+nwaf_log, 'Displaying last 100 lines of '+nwaf_log, 'nwaf log dump complete!')
    print_success('Displaying last 100 lines in the terminal window below.')
else:
    print_error('nwaf log file is not present!')

print_simple_footer()
