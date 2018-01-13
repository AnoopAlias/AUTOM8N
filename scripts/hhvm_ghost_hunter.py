#!/usr/bin/env python


import yaml
import argparse
import pwd
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
    # This script is mostly intended to be called from a cronjob
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
        # Since we have all domains now..check XtendWeb domain-data files for HHVM enabled
        # Turn off HHVM if no domain using HHVM
        hhvm_flag = False
        with open(installation_path + "/domain-data/" + main_domain, 'r') as domain_data_stream:
            yaml_parsed_domain_data = yaml.safe_load(domain_data_stream)
        backend_category = yaml_parsed_domain_data.get('backend_category', None)
        if backend_category == 'HHVM':
            hhvm_flag = True
        for the_sub_domain in sub_domains:
            if the_sub_domain.startswith("*"):
                subdom_config_dom = "_wildcard_."+the_sub_domain.replace('*.', '')
            else:
                subdom_config_dom = the_sub_domain
            with open(installation_path + "/domain-data/" + subdom_config_dom, 'r') as domain_data_stream:
                yaml_parsed_domain_data = yaml.safe_load(domain_data_stream)
            backend_category = yaml_parsed_domain_data.get('backend_category', None)
            if backend_category == 'HHVM':
                hhvm_flag = True
        if hhvm_flag is False:
            # This means none of the domain has HHVM enabled and we can shut down HHVM for the user
            subprocess.call(['systemctl', 'stop', 'ndeploy_hhvm@'+cpaneluser+'.service'])
            subprocess.call(['systemctl', 'disable', 'ndeploy_hhvm@'+cpaneluser+'.service'])
            if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):
                subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m systemd -a "name=ndeploy_hhvm@'+cpaneluser+'.service state=stopped enabled=no"', shell=True)
