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
    subprocess.call(installation_path+"/scripts/easy_php_setup.sh", shell=True)
    commoninclude.print_success('Native nGinx PHP support has been configured.')        

else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
