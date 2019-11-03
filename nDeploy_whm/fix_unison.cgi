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

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('mode'):
    print('<ul class="list-unstyled text-left">')
    if form.getvalue('mode') == 'restart':
        run_cmd = subprocess.Popen(installation_path+'/scripts/fix_unison_filesync.py restart', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        commoninclude.print_success('Soft Restart Complete')
        print('<samp>')
        while True:
            line = run_cmd.stdout.readline()
            if not line:
                break
            print('<li class="mb-2"><samp>'+line+'</samp></li><hr>')
        print('</samp>')
    elif form.getvalue('mode') == 'reset':
        run_cmd = subprocess.Popen(installation_path+'/scripts/fix_unison_filesync.py reset', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        commoninclude.print_success('Hard Restart Complete')
        print('<samp>')
        while True:
            line = run_cmd.stdout.readline()
            if not line:
                break
            print('<li class="mb-2"><samp>'+line+'</samp></li><hr>')
        print('<samp>')
    else:
        commoninclude.print_forbidden()
else:
    commoninclude.print_forbidden()

print_simple_footer()
