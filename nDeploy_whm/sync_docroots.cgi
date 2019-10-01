#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import subprocess


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
    subprocess.call(installation_path+'/scripts/cluster_filesync_ensure_user.py '+form.getvalue('user'), shell=True)
    commoninclude.print_success('GeoDNS zones synced successfully.')
else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
