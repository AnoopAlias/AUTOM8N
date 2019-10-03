#!/bin/python

import commoninclude
import cgi
import cgitb
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

if form.getvalue('autofix_status'):

    print('<ul class="shelloutput">')

    if form.getvalue('autofix_status') == 'simple':
        procExe = subprocess.Popen('/opt/nDeploy/scripts/attempt_autofix.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('    <li><b>Attempting Simple AutoFix:</b></li>')
    elif form.getvalue('autofix_status') == 'phpfpm':
        procExe = subprocess.Popen('/opt/nDeploy/scripts/init_backends.py autofix', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('    <li><b>Attempting PHP-FPM Application Server Fix:</b></li>')

    print('    <li>&nbsp;</li>')
    for line in iter(procExe.stdout.readline, b''):
        print('    <li>'+line.rstrip()+'</li>')
    print('    <li>&nbsp;</li>')
    print('    <li><b>AutoFix utility has completed!</b></li>')
    print('</ul>')

else:
    print('Forbidden::Mising AutoFix Data')

print('</body>')
print('</html>')
