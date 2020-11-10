#!/usr/bin/env python3

import subprocess
import pwd
import argparse
import sys

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_bin = "/usr/sbin/nginx"

parser = argparse.ArgumentParser(description="fix virtfs jailshell for user")
parser.add_argument("CPANELUSER")
args = parser.parse_args()
cpaneluser = args.CPANELUSER
# if user is not in /etc/passwd we dont proceed any further
try:
    pwd.getpwnam(cpaneluser)
    user_shell = pwd.getpwnam(cpaneluser).pw_shell
    user_homedir = pwd.getpwnam(cpaneluser).pw_dir
    if user_shell == '/usr/local/cpanel/bin/jailshell':
        subprocess.call('su - '+cpaneluser+' -c "touch '+user_homedir+'/public_html"', shell=True)
except KeyError:
    sys.exit(0)
