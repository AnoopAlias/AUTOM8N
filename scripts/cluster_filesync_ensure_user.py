#!/usr/bin/env python

try:
    import simplejson as json
except ImportError:
    import json
import argparse
import subprocess
import os
import sys
import pwd

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate gdnsd zone file")
    parser.add_argument("CPANELUSER")
    args = parser.parse_args()
    cpaneluser = args.CPANELUSER
    # if user is not in /etc/passwd we dont proceed any further
    try:
        pwd.getpwnam(cpaneluser)
    except KeyError:
        sys.exit(0)
    else:
        # Try loading the main userdata cache file
        cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
        if os.path.isfile(cpuserdatajson):
            with open(cpuserdatajson) as cpaneluser_data_stream:
                json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
            main_domain = json_parsed_cpaneluser.get('main_domain')
            sub_domains = json_parsed_cpaneluser.get('sub_domains')
            with open("/etc/userdatadomains.json") as userdata_stream:
                json_parsed_userdata = json.load(userdata_stream)
            maindom_docroot = json_parsed_userdata.get(main_domain)[4]
            the_raw_cmd = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m synchronize -a "src='+maindom_docroot+'/ dest='+maindom_docroot+'/"'
            un_cmd = subprocess.Popen(the_raw_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            for mydomain in sub_domains:
                subdom_docroot = json_parsed_userdata.get(mydomain)[4]
                the_raw_cmd = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m synchronize -a "src='+subdom_docroot+'/ dest='+subdom_docroot+'/"'
                un_cmd = subprocess.Popen(the_raw_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
