#!/usr/bin/python

import os
import cgi
import cgitb
import time

from commoninclude import print_simple_header, print_simple_footer, close_cpanel_liveapisock, terminal_call, print_success


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

cpanelhome = os.environ["HOME"]
close_cpanel_liveapisock()

form = cgi.FieldStorage()

print_simple_header()

php_log = cpanelhome+"/logs/php_error_log"
if os.path.isfile(php_log):
    terminal_call('/usr/bin/tail -10 '+php_log, 'Showing last ten entries of '+cpanelhome+'/logs/php_error_log', 'PHP Log dump completed!')
    print_success('PHP Log has been written to terminal!')
    time.sleep(1)

print_simple_footer()
