#!/usr/bin/env python3


import argparse
import pwd
import grp
import sys
import subprocess
import json
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


if __name__ == "__main__":
    # This script is mostly intended to be called from the migration script
    parser = argparse.ArgumentParser(description="disable HHVM server for user if not in use by any domains")
    parser.add_argument("CPANELUSER")
    args = parser.parse_args()
    cpaneluser = args.CPANELUSER
    # if user is not in /etc/passwd we dont proceed any further
    try:
        pwd.getpwnam(cpaneluser)
    except KeyError:
        sys.exit(0)
    else:
        # Update the userdata cache
        subprocess.Popen(['/scripts/updateuserdatacache', '--force', cpaneluser], shell=True)
        # Try loading the main userdata cache file
        cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
        with open(cpuserdatajson) as cpaneluser_data_stream:
            json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
        main_domain = json_parsed_cpaneluser.get('main_domain')
        # parked_domains = yaml_parsed_cpaneluser.get('parked_domains')   # This data is irrelevant as parked domain list is in ServerAlias
        # addon_domains_dict = json_parsed_cpaneluser.get('addon_domains')     # So we know which addon is mapped to which sub-domain
        sub_domains = json_parsed_cpaneluser.get('sub_domains')
        domain_data_file = installation_path + "/domain-data/" + main_domain
        cpuser_uid = pwd.getpwnam(cpaneluser).pw_uid
        cpuser_gid = grp.getgrnam(cpaneluser).gr_gid
        os.chown(domain_data_file, cpuser_uid, cpuser_gid)
        os.chmod(domain_data_file, 0o660)
        for the_sub_domain in sub_domains:
            if the_sub_domain.startswith("*"):
                subdom_config_dom = "_wildcard_."+the_sub_domain.replace('*.', '')
            else:
                subdom_config_dom = the_sub_domain
            domain_data_file = installation_path + "/domain-data/" + subdom_config_dom
            os.chown(domain_data_file, cpuser_uid, cpuser_gid)
            os.chmod(domain_data_file, 0o660)
