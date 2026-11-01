#!/usr/bin/env python3

import cgi
import cgitb
import re
import shlex
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

user = form.getvalue('user')

if user and re.match(r'^[a-zA-Z0-9_\.\-]+$', user):
    terminal_call(installation_path+'/scripts/cluster_filesync_ensure_user.py '+shlex.quote(user), 'Syncing web files...', 'Web files synchronization complete!')
    print_success('Web files synchronization complete!')
else:
    print_forbidden()

print_simple_footer()
