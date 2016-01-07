#!/usr/bin/env python

import cuisine
import pwd
import subprocess

with open("/etc/domainusers", 'r') as domainusers:
    for line in domainusers:
        cpaneluser, domain = line.split(":")
        user_info = pwd.getpwnam(cpaneluser)
        cpaneluserhome = user_info.pw_dir
        cuisine.user_ensure_linux(cpaneluser, home=cpaneluserhome)
subprocess.call('/usr/bin/unison', shell=True)
