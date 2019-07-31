#!/usr/bin/python

import cgi
import cgitb
import subprocess
import os
from commoninclude import sighupnginx, print_success, print_nontoast_error


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('user'):
    subprocess.call(installation_path+'/scripts/cluster_gdnsd_ensure_user.py '+form.getvalue('user'), shell=True)
    print_success('GeoDNS zones synced successfully.')
else:
    print_nontoast_error('<h3>Forbidden!</h3>Though shall not Pass!')

print('</body>')
print('</html>')