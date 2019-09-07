#!/usr/bin/python

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

if form.getvalue('run_installer') == 'enabled':
    procExe = subprocess.Popen(installation_path+"/scripts/easy_php_setup.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    print('<ul class="shelloutput">')
    print('    <li><b>Executing Native NGINX PHP Installer</b>')
    print('    </li><li>&nbsp;</li>')
    for line in iter(procExe.stdout.readline, b''):
        print('    <li>'+line.rstrip()+'</li>')
    print('    <li>&nbsp;</li>')
    print('    <li><b>Native nGinx PHP support has been configured.</b></li>')
    print('</ul>')

else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
