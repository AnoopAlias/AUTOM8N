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

if form.getvalue('package_lock'):
    if form.getvalue('package_lock') == 'enabled':
        subprocess.call('touch '+installation_path+'/conf/lock_domaindata_to_package', shell=True)
        commoninclude.print_success('Nginx config will change with package upgrade/downgrade')
    elif form.getvalue('package_lock') == 'disabled':
        silentremove(installation_path+'/conf/lock_domaindata_to_package')
        commoninclude.print_success('cPanel set Nginx setting will be preserved in package changes')
else:
        commoninclude.print_forbidden()

print('</body>')
print('</html>')
