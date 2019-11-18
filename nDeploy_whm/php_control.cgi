#!/bin/python

import cgi
import cgitb
import os
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_warning, print_forbidden


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
        terminal_call(installation_path+'/scripts/init_backends.py secure-php', 'Initiating Multi-Master PHP mode...', 'Attempting AutoFix of accounts...')
        terminal_call(installation_path+'/scripts/attempt_autofix.sh', '', 'Attempting AutoFix of PHP application server...')
        terminal_call(installation_path+'/scripts/init_backends.py autofix', '', 'Multi-Master PHP mode activated!')
        print_success('Multi-Master PHP mode activated!')

    elif form.getvalue('php_mode') == 'multi' and php_secure_status == True:

    	# Secure mode status is already multi so this should already be disabled via nDeploy Control
        print_warning('Multi-Master aleady active!')

    if form.getvalue('php_mode') == 'single' and php_secure_status == False:

    	# Single mode status is already single so this should already be disabled via nDeploy Control
        print_warning('Single Master aleady active!')

    elif form.getvalue('php_mode') == 'single' and php_secure_status == True:

        # Start the single mode install.
        terminal_call(installation_path+'/scripts/init_backends.py disable-secure-php', 'Initiating Single Master PHP mode...', 'Attempting AutoFix of accounts...')
        terminal_call(installation_path+'/scripts/attempt_autofix.sh', '', 'Attempting AutoFix of PHP application server...')
        terminal_call(installation_path+'/scripts/init_backends.py autofix', '', 'Restarting PHP backends...')
        terminal_call('service ndeploy_backends restart', '', 'Single Master PHP mode activated!')
        print_success('Single Master PHP mode activated!')

    if form.getvalue('chroot_mode') == 'enabled' and php_secure_status == True:

        # Chroot only works with Single Master PHP Mode - This should be a modal
        print_warning('Chroot requires Single Master PHP!')

    elif form.getvalue('chroot_mode') == 'disabled' and php_secure_status == True:

        # Chroot only works with Single Master PHP Mode - This should be a modal
        print_warning('Chroot requires Single Master PHP!')

    elif form.getvalue('chroot_mode') == 'enabled' and php_secure_status == False:

        # Enabled Chroot PHP
        terminal_call(installation_path+'/scripts/init_backends.py jailphpfpm', 'Activating Chrooted PHP mode...', 'Restarting PHP backends...')
        terminal_call('service ndeploy_backends restart', '', 'Chrooted PHP mode activated!')
        print_success('Chrooted PHP mode activated!')

    elif form.getvalue('chroot_mode') == 'disabled' and php_secure_status == False:

        # Disabled Chroot PHP
        terminal_call(installation_path+'/scripts/init_backends.py disable-jailphpfpm', 'Deactivating Chrooted PHP mode...', 'Restarting PHP backends...')
        terminal_call('service ndeploy_backends restart', '', 'Chrooted PHP mode deactivated!')
        print_success('Chrooted PHP mode deactivated!')

else:
    print_forbidden()

print_simple_footer()
