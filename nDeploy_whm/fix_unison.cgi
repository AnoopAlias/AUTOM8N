#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import subprocess
from commoninclude import print_simple_header, print_simple_footer


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
whm_terminal_log = installation_path+"/nDeploy_whm/term.log"

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('mode'):
    if form.getvalue('mode') == 'restart':

        procExe = subprocess.Popen('echo -e "Initiating Unison Soft Restart..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/fix_unison_filesync.py restart >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo -e "Unison Soft Restart Complete..." >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        commoninclude.print_success('Unison Soft Restart Complete!')

    elif form.getvalue('mode') == 'reset':

        procExe = subprocess.Popen('echo -e "Initiating Unison Hard Reset..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/fix_unison_filesync.py reset >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo -e "Unison Hard Reset Complete..." >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        commoninclude.print_success('Unison Hard Reset Complete!')

    else:
        commoninclude.print_forbidden()
else:
    commoninclude.print_forbidden()

print_simple_footer()
