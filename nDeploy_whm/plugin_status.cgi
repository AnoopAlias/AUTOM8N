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
    print('    <li><b>Plugin Status Start</b></li>')
    print('    <li>&nbsp;</li>')
    for line in iter(procExe.stdout.readline, b''):
        print('    <li>'+line.rstrip()+'</li>')
    print('    <li>&nbsp;</li>')
    print('    <li><b>Plugin Status End</b></li>')
    print('</ul>')

if form.getvalue('plugin_status') == 'enable':
    print('<p>Enabling Application</p>')
    procExe = subprocess.Popen(installation_path+"/scripts/cpanel-nDeploy-setup.sh enable", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    shelloutput()
    
elif form.getvalue('plugin_status') == 'disable':
    print('<p>Disabling Application</p>')
    procExe = subprocess.Popen(installation_path+"/scripts/cpanel-nDeploy-setup.sh disable", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    shelloutput()

else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
