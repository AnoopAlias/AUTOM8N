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
php_secure_mode_file = installation_path+"/conf/secure-php-enabled"
php_chroot_mode_file = "/var/cpanel/feature_toggles/apachefpmjail"

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
php_chroot_status = False
php_secure_status = False

if os.path.isfile(php_secure_mode_file):
    php_secure_status = True

if os.path.isfile(php_chroot_mode_file):
    php_chroot_status = True

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('php_mode') or form.getvalue('chroot_mode'):

    if form.getvalue('php_mode') == 'multi' and php_secure_status == False:
        # Start secure mode installation.
        print('<ul class="shelloutput">')
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py secure-php', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Initiating Multi-Master PHP Mode (Secure PHP Mode)', 'Multi-Master PHP Mode Completed.')
        procExe = subprocess.Popen(installation_path+'/scripts/attempt_autofix.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Attempting AutoFix of Accounts', 'AutoFix Completed.')
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py autofix', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Attempting AutoFix of PHP Application Server.', 'PHP Application Server AutoFix Completed.')
        print('</ul>')

    elif form.getvalue('php_mode') == 'multi' and php_secure_status == True:
    	# Secure mode status is already multi so this should already be disabled via nDeploy Control - This should be a modal
        print('<ul class="shelloutput">')
        print('    <li><b>Multi-Master PHP Mode already in plcace.</b></li>')
        print('</ul>')

    if form.getvalue('php_mode') == 'single' and php_secure_status == False:
    	# Single mode status is already single so this should already be disabled via nDeploy Control - This should be a modal
        print('<ul class="shelloutput">')
        print('    <li><b>Single Master PHP Mode already in place.</b></li>')
        print('</ul>')

    elif form.getvalue('php_mode') == 'single' and php_secure_status == True:
        # Start the single mode install.
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

    if form.getvalue('chroot_mode') == 'enabled' and php_secure_status == True:
        # Chroot only works with Single Master PHP Mode - This should be a modal
        print('<ul class="shelloutput">')
        print('    <li><b>Chroot configuration is only available for Single Master PHP Mode.</b></li>')
        print('</ul>')

    elif form.getvalue('chroot_mode') == 'disabled' and php_secure_status == True:
        # Chroot only works with Single Master PHP Mode - This should be a modal
        print('<ul class="shelloutput">')
        print('    <li><b>Chroot configuration is only available for Single Master PHP Mode.</b></li>')
        print('</ul>')

    elif form.getvalue('chroot_mode') == 'enabled' and php_secure_status == False:
        # Enabled Chroot PHP
        print('<ul class="shelloutput">')
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py jailphpfpm', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Activating Chrooted PHP Mode.', 'Chrooted PHP Mode Activated.')
        procExe = subprocess.Popen('service ndeploy_backends restart', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Restarting PHP Backends.', 'PHP Backends Restarted.')
        print('</ul>')

    elif form.getvalue('chroot_mode') == 'disabled' and php_secure_status == False:
        # Disabled Chroot PHP
        print('<ul class="shelloutput">')
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py disable-jailphpfpm', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Deactivating Chrooted PHP Mode.', 'Chrooted PHP Mode Deactivated.')
        procExe = subprocess.Popen('service ndeploy_backends restart', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        shellout(procExe, 'Restarting PHP Backends.', 'PHP Backends Restarted.')
        print('</ul>')

else:
    print('Forbidden::Mising PHP Mode Data')

print('</body>')
print('</html>')
