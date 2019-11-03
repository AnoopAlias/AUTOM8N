#!/bin/python

import commoninclude
import cgi
import cgitb
import os
import subprocess
from commoninclude import print_simple_header, print_simple_footer


__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Production"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
whm_terminal_log = installation_path+"/nDeploy_whm/term.log"
php_secure_mode_file = installation_path+"/conf/secure-php-enabled"
php_chroot_mode_file = "/var/cpanel/feature_toggles/apachefpmjail"

cgitb.enable()

form = cgi.FieldStorage()

# Get PHP Chroot and Secure status
php_chroot_status = False
php_secure_status = False

if os.path.isfile(php_secure_mode_file):
    php_secure_status = True

if os.path.isfile(php_chroot_mode_file):
    php_chroot_status = True

print_simple_header()

if form.getvalue('php_mode') or form.getvalue('chroot_mode'):

    if form.getvalue('php_mode') == 'multi' and php_secure_status == False:

        # Start secure mode installation.
        procExe = subprocess.Popen('echo "*** Initiating Multi-Master PHP Mode ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py secure-php >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** Multi-Master PHP Mode Activated ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        procExe = subprocess.Popen('echo "*** Attempting AutoFix of Accounts ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/attempt_autofix.sh >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** AutoFix of Accounts Completed ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        procExe = subprocess.Popen('echo "*** Attempting AutoFix of PHP Application Server ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py autofix >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** PHP Application Server AutoFix Completed ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        commoninclude.print_success('Multi-Master PHP activated!')

    elif form.getvalue('php_mode') == 'multi' and php_secure_status == True:

    	# Secure mode status is already multi so this should already be disabled via nDeploy Control
        commoninclude.print_warning('Multi-Master aleady active!')

    if form.getvalue('php_mode') == 'single' and php_secure_status == False:

    	# Single mode status is already single so this should already be disabled via nDeploy Control
        commoninclude.print_warning('Single Master aleady active!')

    elif form.getvalue('php_mode') == 'single' and php_secure_status == True:

        # Start the single mode install.
        procExe = subprocess.Popen('echo "*** Initiating Single Master PHP Mode ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py disable-secure-php >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** Single Master PHP Mode Activated ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        procExe = subprocess.Popen('echo "*** Attempting AutoFix of Accounts ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/attempt_autofix.sh >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** AutoFix of Accounts Completed ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        procExe = subprocess.Popen('echo "*** Attempting AutoFix of PHP Application Server ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py autofix >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** PHP Application Server AutoFix Completed ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        procExe = subprocess.Popen('echo "*** Restarting PHP Backends ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('service ndeploy_backends restart >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** PHP Backends Restarted ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        commoninclude.print_success('Single Master PHP activated!')

    if form.getvalue('chroot_mode') == 'enabled' and php_secure_status == True:

        # Chroot only works with Single Master PHP Mode - This should be a modal
        commoninclude.print_warning('Chroot requires Single Master PHP!')

    elif form.getvalue('chroot_mode') == 'disabled' and php_secure_status == True:

        # Chroot only works with Single Master PHP Mode - This should be a modal
        commoninclude.print_warning('Chroot requires Single Master PHP!')

    elif form.getvalue('chroot_mode') == 'enabled' and php_secure_status == False:

        # Enabled Chroot PHP
        procExe = subprocess.Popen('echo "*** Activating Chrooted PHP Mode ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py jailphpfpm >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** Chrooted PHP Mode Activated ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        procExe = subprocess.Popen('echo "*** Restarting PHP Backends ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('service ndeploy_backends restart >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** PHP Backends Restarted ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        commoninclude.print_success('Chroot PHP activated!')

    elif form.getvalue('chroot_mode') == 'disabled' and php_secure_status == False:

        # Disabled Chroot PHP
        procExe = subprocess.Popen('echo "*** Deactivating Chrooted PHP Mode ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py disable-jailphpfpm >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** Chrooted PHP Mode Deactivated ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        procExe = subprocess.Popen('echo "*** Restarting PHP Backends ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('service ndeploy_backends restart >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** PHP Backends Restarted ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        commoninclude.print_success('Chroot PHP deactivated!')

else:
    commoninclude.print_forbidden()

print_simple_footer()
