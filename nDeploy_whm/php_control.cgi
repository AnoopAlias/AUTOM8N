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
php_secure_mode_file = installation_path+"/conf/PHP_SECURE_MODE"
php_chroot_mode_file = installation_path+"/conf/PHP_CHROOT_MODE"

cgitb.enable()

form = cgi.FieldStorage()

# Get PHP Chroot and Secure status
php_chroot_status = ''
php_secure_status = ''

if os.path.isfile(php_secure_mode_file):
    with open(php_secure_mode_file, 'r') as php_secure_status_value:
        php_secure_status = php_secure_status_value.read(1)

if os.path.isfile(php_chroot_mode_file):
    with open(php_chroot_mode_file, 'r') as php_chroot_status_value:
        php_secure_status = php_chroot_status_value.read(1)

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('php_mode') or form.getvalue('chroot_mode'):

    if form.getvalue('php_mode') == 'multi' and php_secure_status == '':
    	# Start secure mode installation from scratch (This should be set to 0 after Easy PHP Install)

    elif form.getvalue('php_mode') == 'multi' and php_secure_status == '0':
    	# Start secure mode installation from a regular previous installation.

    elif form.getvalue('php_mode') == 'multi' and php_secure_status == '1':
    	# Secure mode status is already multi so this should already be disabled via nDeploy Control

    if form.getvalue('php_mode') == 'single' and php_secure_status == '':
    	# Regular mode is being called but we should call the Easy PHP Install

    elif form.getvalue('php_mode') == 'single' and php_secure_status == '0':
    	# Single mode status is already single so this should already be disabled via nDeploy Control

    elif form.getvalue('php_mode') == 'single' and php_secure_status == '1':
    	# Start the multi mode install.
    	
    if True:
        procExe = subprocess.Popen('command', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        procExe = subprocess.Popen('command', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

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
