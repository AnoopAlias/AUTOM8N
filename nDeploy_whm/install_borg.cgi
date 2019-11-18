#!/usr/bin/python

import cgi
import cgitb
import os
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('action'):
    if form.getvalue('action') == 'installborg':

        terminal_call(installation_path+'/scripts/easy_borg_setup.sh', 'Installing BorgBackup...', 'BorgBackup installed!')
        print_success('BorgBackup Installed!')

    elif form.getvalue('action') == 'initrepo':

        terminal_call('/usr/local/bin/borgmatic --init --encryption repokey-blake2', 'Initializing repository...', 'Repository initialized!')
        print_success('Repo initialized!')

        if not os.path.isfile('/etc/borgmatic/BORG_SETUP_LOCK_DO_NOT_REMOVE'):
            os.mknod('/etc/borgmatic/BORG_SETUP_LOCK_DO_NOT_REMOVE')

    else:
        print_forbidden()
else:
    print_forbidden()

print_simple_footer()
