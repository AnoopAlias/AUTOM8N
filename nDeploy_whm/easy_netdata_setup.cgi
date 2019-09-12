#!/bin/python

import commoninclude
import cgi
import cgitb
import yaml
import os
import subprocess


__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Development"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

def shelloutput():
    print('<ul class="shelloutput">')
    print('    <li><b>Executing the Easy NETDATA Installer...</b></li>')
    print('    <li>&nbsp;</li>')
    for line in iter(procExe.stdout.readline, b''):
        print('    <li>'+line.rstrip()+'</li>')
    print('    <li>&nbsp;</li>')
    print('    <li><b>NETDATA has been configured on this system.</b></li>')
    print('</ul>')


if form.getvalue('run_installer') == 'enabled':

    if os.path.isfile('/etc/nginx/conf.d/netdata.password'):
        print('<span class="p-1">NetData credentials already exist. Installing latest NetData with current credentials...</span>')
        procExe = subprocess.Popen(installation_path+"/scripts/easy_netdata_setup.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shelloutput()
        
    elif form.getvalue('netdata_pass') != None:
        print('<span class="p-1">NetData is being set up using <kbd>netdata::'+form.getvalue('netdata_pass')+'</kbd> for credentials.</span>')    
        procExe = subprocess.Popen(installation_path+"/scripts/easy_netdata_setup.sh "+form.getvalue('netdata_pass'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shelloutput()

    else:
        print('<span class="p-1">Pass is empty and netdata.password does not exist.<span>')
    
elif form.getvalue('remove_netdata_creds') == 'enabled':
    os.remove('/etc/nginx/conf.d/netdata.password')
    print('NetData Credentials have been removed. You can now set up NetData using a new password.')

else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
