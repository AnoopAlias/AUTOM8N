#!/usr/bin/env python3

import cgi
import cgitb
import os
import yaml
import sys
import re
from commoninclude import print_simple_header, print_simple_footer, print_success, print_error


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backup_config_file = "/opt/nDeploy/conf/backup_config.yaml"
borgmatic_config_file = "/etc/borgmatic/config.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

with open(borgmatic_config_file, 'r') as borgmatic_conf:
    yaml_parsed_borgmaticyaml = yaml.safe_load(borgmatic_conf)
backup_dir_list = yaml_parsed_borgmaticyaml['location']['source_directories']

if form.getvalue('thehomedir'):
    if not form.getvalue('thehomedir').startswith('/'):
        myhomedir_pass1 = '/'+form.getvalue('thehomedir')
    else:
        myhomedir_pass1 = form.getvalue('thehomedir')
    if myhomedir_pass1.endswith('/'):
        myhomedir = myhomedir_pass1[:-1]
    else:
        myhomedir = myhomedir_pass1
    if not myhomedir:
        print_error('Error: Invalid Homedir name')
        sys.exit(0)
    if not re.match("^[\.0-9a-zA-Z/_-]*$", myhomedir):
        print_error("Error: Invalid char in Homedir name")
        sys.exit(0)

    if form.getvalue('action'):
        if form.getvalue('action') == "add":
            if myhomedir not in backup_dir_list:
                backup_dir_list.append(myhomedir)
            yaml_parsed_borgmaticyaml['location']['source_directories'] = backup_dir_list
            print_success('Directory Added!')

        elif form.getvalue('action') == "delete":
            backup_dir_list.remove(form.getvalue('thehomedir'))
            yaml_parsed_borgmaticyaml['location']['source_directories'] = backup_dir_list
            print_success('Directory Removed!')

    with open(borgmatic_config_file, 'w') as borgmatic_conf:
        yaml.dump(yaml_parsed_borgmaticyaml, borgmatic_conf, default_flow_style=False)
    os.chmod(borgmatic_config_file, 0o640)

    print('    </body>')
    print('</html>')
    sys.exit(0)

# If not add/remove dirs, handle the settings

if form.getvalue('repositories'):
    yaml_parsed_borgmaticyaml['location']['repositories'][0] = form.getvalue('repositories')
else:
    print_error("Missing Repository!")
    sys.exit(0)

if form.getvalue('remote_rate_limit'):

    # Input sanitation
    if not re.match("^[0-9]+$", form.getvalue('remote_rate_limit')):
        print_error("Error: Positive integer value expected for remote_rate_limit")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['storage']['remote_rate_limit'] = int(form.getvalue('remote_rate_limit'))

else:
    print_error("Missing Remote Rate Limit!")
    sys.exit(0)

if form.getvalue('ssh_command'):
    yaml_parsed_borgmaticyaml['storage']['ssh_command'] = form.getvalue('ssh_command')
else:
    print_error("SSH Command!")
    sys.exit(0)

if form.getvalue('encryption_passphrase'):

    # Input sanitation
    if not re.match("^[0-9a-zA-Z]+$", form.getvalue('encryption_passphrase')):
        print_error("Error: Do not use any symbols, use only numbers, small and capital letters in encryption passphrase")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['storage']['encryption_passphrase'] = form.getvalue('encryption_passphrase')

else:
    print_error("Missing Passphrase!")
    sys.exit(0)

if form.getvalue('keep_hourly'):

    # Input sanitation
    if not re.match("^[0-9]+$", form.getvalue('keep_hourly')):
        print_error("Error: Positive integer value expected for keep_hourly")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['retention']['keep_hourly'] = int(form.getvalue('keep_hourly'))

else:
    print_error("Missing Hourly Keep!")
    sys.exit(0)

if form.getvalue('keep_daily'):

    # Input sanitation
    if not re.match("^[0-9]+$", form.getvalue('keep_daily')):
        print_error("Error: Positive integer value expected for keep_daily")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['retention']['keep_daily'] = int(form.getvalue('keep_daily'))

else:
    print_error("Missing Daily Keep!")
    sys.exit(0)

if form.getvalue('keep_weekly'):

    # Input sanitation
    if not re.match("^[0-9]+$", form.getvalue('keep_weekly')):
        print_error("Error: Positive integer value expected for keep_weekly")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['retention']['keep_weekly'] = int(form.getvalue('keep_weekly'))

else:
    print_error("Missing Weekly Keep!")
    sys.exit(0)

if form.getvalue('keep_monthly'):

    # Input sanitation
    if not re.match("^[0-9]+$", form.getvalue('keep_monthly')):
        print_error("Error: Positive integer value expected for keep_monthly")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['retention']['keep_monthly'] = int(form.getvalue('keep_monthly'))

else:
    print_error("Missing Monthly Keep!")
    sys.exit(0)

print_success('Settings saved!')

with open(borgmatic_config_file, 'w') as borgmatic_conf:
    yaml.dump(yaml_parsed_borgmaticyaml, borgmatic_conf, default_flow_style=False)
os.chmod(borgmatic_config_file, 0o640)

print_simple_footer()
