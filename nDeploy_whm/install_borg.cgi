#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import subprocess
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
whm_terminal_log = installation_path+"/nDeploy_whm/term.log"

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('    <head>')
print('    </head>')
print('    <body>')

if form.getvalue('action'):
    if form.getvalue('action') == 'installborg':

        procExe = subprocess.Popen('echo -e "Installing BorgBackup System... > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/easy_borg_setup.sh >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo -e "BorgBackup System installed! >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        commoninclude.print_success('BorgBackup Installed!')

    elif form.getvalue('action') == 'initrepo':

        procExe = subprocess.Popen('echo -e "Initializing Repo... > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('/usr/local/bin/borgmatic --init --encryption repokey-blake2 >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo -e "Repo Initialized... >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        commoninclude.print_success('Repo initialized!')

        if not os.path.isfile('/etc/borgmatic/BORG_SETUP_LOCK_DO_NOT_REMOVE'):
            os.mknod('/etc/borgmatic/BORG_SETUP_LOCK_DO_NOT_REMOVE')

    else:
        commoninclude.print_forbidden()
else:
    commoninclude.print_forbidden()
print('    </body>')
print('</html>')
