#!/usr/bin/env python

import commoninclude
import cgitb
import subprocess
import cgi
import os
import yaml
from commoninclude import print_simple_header, print_simple_footer


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
xtendweb_installation_path = "/opt/nDeploy"  # Absolute Installation Path
borgmatic_config_file = "/etc/borgmatic/config.yaml"


cgitb.enable()
form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('action') and os.path.isfile(borgmatic_config_file):
    # We will retrive the borg repo details from borgmatic config
    # Get all config settings from the borgmatic config file
    with open(borgmatic_config_file, 'r') as borgmatic_config_file_stream:
        yaml_parsed_borgmaticyaml = yaml.safe_load(borgmatic_config_file_stream)
    borg_repo = yaml_parsed_borgmaticyaml['location']['repositories'][0]
    encryption_passphrase = yaml_parsed_borgmaticyaml['storage']['encryption_passphrase']
    my_env = os.environ.copy()
    my_env["BORG_PASSPHRASE"] = encryption_passphrase
    my_env["LANG"] = 'en_US.UTF-8'
    if form.getvalue('action') == 'umount':
        the_raw_cmd_orig = 'borg umount /root/borg_restore_point'
        the_raw_cmd = the_raw_cmd_orig.decode('utf-8')
    elif form.getvalue('action') == 'mount':
        if form.getvalue('restorepoint'):
            restore_point_dict = {'restore_point': form.getvalue('restorepoint')}
            with open('/etc/borgmatic/BORG_SETUP_LOCK_DO_NOT_REMOVE', 'w') as restore_point_conf:
                yaml.dump(restore_point_dict, restore_point_conf, default_flow_style=False)
            the_raw_cmd_orig = 'borg mount '+borg_repo+'::'+form.getvalue('restorepoint')+' /root/borg_restore_point'
            the_raw_cmd = the_raw_cmd_orig.decode('utf-8')
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

print_simple_footer()
