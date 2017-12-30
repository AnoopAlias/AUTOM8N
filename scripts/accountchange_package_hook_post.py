#!/usr/bin/env python


import sys
import subprocess
import os
import pwd
import grp
import shutil
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


# This hook script is supposed to be called after account creation by cPanel
installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
# Loading the json in on stdin send by cPanel
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
cur_pkg = mydict["cur_pkg"]
new_pkg = mydict["new_pkg"]
if new_pkg != cur_pkg:
    if os.path.isfile(installation_path+'/conf/lock_domaindata_to_package'):
        hostingplan_filename = new_pkg.replace(" ", "_")
        cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
        if os.path.isfile(cpuserdatajson):
            with open(cpuserdatajson) as cpaneluser_data_stream:
                json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
            main_domain = json_parsed_cpaneluser.get('main_domain')
            main_domain_data_file = installation_path+"/domain-data/"+main_domain
            if os.path.isfile(installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"):
                TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"
                shutil.copyfile(TEMPLATE_FILE, main_domain_data_file)
                cpuser_uid = pwd.getpwnam(cpaneluser).pw_uid
                cpuser_gid = grp.getgrnam(cpaneluser).gr_gid
                os.chown(main_domain_data_file, cpuser_uid, cpuser_gid)
                os.chmod(main_domain_data_file, 0o660)
            sub_domains = json_parsed_cpaneluser.get('sub_domains')
            for the_sub_domain in sub_domains:
                if the_sub_domain.startswith("*"):
                    sub_domain_data_file = installation_path+"/domain-data/_wildcard_."+the_sub_domain.replace('*.', '')
                else:
                    sub_domain_data_file = installation_path+"/domain-data/"+the_sub_domain
                if os.path.isfile(installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"):
                    TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"
                    shutil.copyfile(TEMPLATE_FILE, sub_domain_data_file)
                    cpuser_uid = pwd.getpwnam(cpaneluser).pw_uid
                    cpuser_gid = grp.getgrnam(cpaneluser).gr_gid
                    os.chown(sub_domain_data_file, cpuser_uid, cpuser_gid)
                    os.chmod(sub_domain_data_file, 0o660)
        subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
        print("1 nDeploy:account_change_package:"+cpaneluser)
