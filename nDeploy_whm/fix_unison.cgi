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
    if form.getvalue('mode') == 'restart':

        terminal_call(installation_path+'/scripts/fix_unison_filesync.py restart', 'Initiating Unison soft restart...', 'Unison soft restart complete!')
        print_success('Unison soft restart complete!')

    elif form.getvalue('mode') == 'reset':

        terminal_call(installation_path+'/scripts/fix_unison_filesync.py reset', 'Initiating Unison hard reset...', 'Unison hard reset complete!')
        print_success('Unison hard reset complete!')

    else:
        print_forbidden()
else:
    print_forbidden()

print_simple_footer()
