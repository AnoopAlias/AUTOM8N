#!/usr/bin/env python

import commoninclude
import cgitb
import subprocess
import cgi
import os
import yaml

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
xtendweb_installation_path = "/opt/nDeploy"  # Absolute Installation Path
borgmatic_config_file = "/etc/borgmatic/config.yaml"


cgitb.enable()
form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('action') and os.path.isfile(borgmatic_config_file):
    # We will retrive the borg repo details from borgmatic config
    # Get all config settings from the borgmatic config file
    with open(borgmatic_config_file, 'r') as borgmatic_config_file_stream:
        yaml_parsed_borgmaticyaml = yaml.safe_load(borgmatic_config_file_stream)
    borg_repo = yaml_parsed_borgmaticyaml['location']['repositories'][0]
    encryption_passphrase = yaml_parsed_borgmaticyaml['storage']['encryption_passphrase']
    my_env = os.environ.copy()
    my_env["BORG_PASSPHRASE"] = encryption_passphrase
    if form.getvalue('action') == 'umount':
        the_raw_cmd = 'borg umount /root/borg_restore_point'
    elif form.getvalue('action') == 'mount':
        if form.getvalue('restorepoint'):
            the_raw_cmd = 'borg mount '+borg_repo+'::'+form.getvalue('restorepoint')+' /root/borg_restore_point'
        else:
            commoninclude.print_forbidden()
            exit(0)
    else:
        commoninclude.print_forbidden()
        exit(0)
    run_cmd = subprocess.Popen(the_raw_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=my_env, shell=True)
    print('<samp>')
    commoninclude.print_success("Done. Check /root/borg_restore_point ")
    while True:
        line = run_cmd.stdout.readline()
        if not line:
            break
        print('<li class="mb-2"><samp>'+line+'</samp></li><hr>')
    print('</samp>')
else:
    commoninclude.print_forbidden()
print('</body>')
print('</html>')
