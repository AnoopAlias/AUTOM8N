#!/usr/bin/env python3


import sys
import io
import subprocess
import os
import pwd
import grp
import shutil
import yaml
try:
    import simplejson as json
except ImportError:
    import json
from commoninclude import silentremove, sighupnginx


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


# This hook script is supposed to be called after account creation by cPanel
installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
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
        if hostingplan_filename == 'undefined' or hostingplan_filename == 'default':
            if os.path.isfile(installation_path+"/conf/domain_data_default_local.yaml"):
                TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local.yaml"
            else:
                TEMPLATE_FILE = installation_path+"/conf/domain_data_default.yaml"
        else:
            if os.path.isfile((installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml").encode('utf-8')):
                TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"
            else:
                if os.path.isfile(installation_path+"/conf/domain_data_default_local.yaml"):
                    TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local.yaml"
                else:
                    TEMPLATE_FILE = installation_path+"/conf/domain_data_default.yaml"
        if os.path.isfile(cpuserdatajson) and os.path.isfile(TEMPLATE_FILE.encode('utf-8')):
            with open(TEMPLATE_FILE, 'r', encoding='utf-8') as profileyaml_data_stream:
                yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
            phpmaxchildren = yaml_parsed_profileyaml.get('phpmaxchildren', '8')
            with open(cpuserdatajson) as cpaneluser_data_stream:
                json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
            main_domain = json_parsed_cpaneluser.get('main_domain')
            main_domain_data_file = installation_path+"/domain-data/"+main_domain
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
                shutil.copyfile(TEMPLATE_FILE, sub_domain_data_file)
                cpuser_uid = pwd.getpwnam(cpaneluser).pw_uid
                cpuser_gid = grp.getgrnam(cpaneluser).gr_gid
                os.chown(sub_domain_data_file, cpuser_uid, cpuser_gid)
                os.chmod(sub_domain_data_file, 0o660)
        if os.path.isfile(installation_path+'/php-fpm.d/'+cpaneluser+'.conf'):
            silentremove(installation_path+'/php-fpm.d/'+cpaneluser+'.conf')
        if os.path.isfile(installation_path+'/secure-php-fpm.d/'+cpaneluser+'.conf'):
            silentremove(installation_path+'/secure-php-fpm.d/'+cpaneluser+'.conf')
        subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
        sighupnginx()
        print(("1 nDeploy:account_change_package:"+cpaneluser))
