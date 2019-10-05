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

def shellout(procEXE='echo "what?"', before='',after=''):
    print('    <li><b>'+before+'</b></li>')
    print('    <li>&nbsp;</li>')
    for line in iter(procExe.stdout.readline, b''):
        print('    <li>'+line.rstrip()+'</li>')
    print('    <li>&nbsp;</li>')
    print('    <li><b>'+after+'</b></li>')

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
        print('<ul class="shelloutput">')
        procExe = subprocess.Popen(installation_path+'/scripts/easy_php_setup.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Running Easy PHP Setup...', 'Easy PHP Setup Complete.')
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py secure-php', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Initiating Multi-Master PHP Mode (Secure PHP Mode)', 'Multi-Master PHP Mode Completed.')
        procExe = subprocess.Popen(installation_path+'/scripts/attempt_autofix.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Attempting AutoFix of Accounts', 'AutoFix Completed.')
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py autofix', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Attempting AutoFix of PHP Application Server.', 'PHP Application Server AutoFix Completed.')
        print('</ul>')

    elif form.getvalue('php_mode') == 'multi' and php_secure_status == '0':
        print('<ul class="shelloutput">')
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py secure-php', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Initiating Multi-Master PHP Mode (Secure PHP Mode)', 'Multi-Master PHP Mode Completed.')
        procExe = subprocess.Popen(installation_path+'/scripts/attempt_autofix.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Attempting AutoFix of Accounts', 'AutoFix Completed.')
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py autofix', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Attempting AutoFix of PHP Application Server.', 'PHP Application Server AutoFix Completed.')
        print('</ul>')
        # Start secure mode installation as single mode is in effect (Easy PHP Mode has been executed)

    elif form.getvalue('php_mode') == 'multi' and php_secure_status == '1':
        print('<ul class="shelloutput">')
        print('    <li><b>Multi-Master PHP Mode already in plcace.</b></li>')
        print('</ul>')
    	# Secure mode status is already multi so this should already be disabled via nDeploy Control - This should be a modal

    if form.getvalue('php_mode') == 'single' and php_secure_status == '':
        print('<ul class="shelloutput">')
        procExe = subprocess.Popen(installation_path+'/scripts/easy_php_setup.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Running Easy PHP Setup...', 'Easy PHP Setup Complete.')
        print('</ul>')
    	# Regular mode is being called but we should call the Easy PHP Install since it appears to have not been run.

    elif form.getvalue('php_mode') == 'single' and php_secure_status == '0':
        print('<ul class="shelloutput">')
        print('    <li><b>Single Master PHP Mode already in plcace.</b></li>')
        print('</ul>')
    	# Single mode status is already single so this should already be disabled via nDeploy Control - This should be a modal

    elif form.getvalue('php_mode') == 'single' and php_secure_status == '1':
        print('<ul class="shelloutput">')
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py disable-secure-php', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Disabling Multi-Master PHP Mode (Secure PHP Mode) and switching to Single Master PHP Mode.', 'Single Master PHP Mode Completed.')
        procExe = subprocess.Popen(installation_path+'/scripts/attempt_autofix.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Attempting AutoFix of Accounts', 'AutoFix Completed.')
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py autofix', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Attempting AutoFix of PHP Application Server.', 'PHP Application Server AutoFix Completed.')
        procExe = subprocess.Popen('service ndeploy_backends restart', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Restarting PHP Backends.', 'PHP Backends Restarted.')
        print('</ul>')
        # Start the single mode install.

else:
    print('Forbidden::Mising PHP Mode Data')

print('</body>')
print('</html>')
