#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import subprocess
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


cgitb.enable()


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('user'):
    subprocess.call(installation_path+'/scripts/cluster_gdnsd_ensure_user.py '+form.getvalue('user'), shell=True)
    commoninclude.print_success('DNS Zone Synced')
else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
