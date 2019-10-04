#!/bin/python

import commoninclude
import cgi
import cgitb
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

if form.getvalue('php_mode') or form.getvalue('chroot_mode'):

        print('<ul class="shelloutput">')
        print('    <li><b>...</b></li>')
        print('    <li>&nbsp;</li>')
        for line in iter(procExe.stdout.readline, b''):
            print('    <li>'+line.rstrip()+'</li>')
        print('    <li>&nbsp;</li>')
        print('    <li><b>...</b></li>')
        print('</ul>')

else:
    print('Forbidden::Mising PHP Mode Data')

print('</body>')
print('</html>')
