#!/usr/bin/env python


import sys
import subprocess
import os
import pwd
import grp
import shutil
import yaml
import platform
import psutil
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def nginxreload():
    with open(os.devnull, 'w') as FNULL:
        subprocess.Popen(['/usr/sbin/nginx', '-s', 'reload'], stdout=FNULL, stderr=subprocess.STDOUT)


def safenginxreload():
    nginx_status = False
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if '/usr/sbin/nginx' in mycmdline and 'reload' in mycmdline:
            nginx_status = True
            break
    if not nginx_status:
        with open(os.devnull, 'w') as FNULL:
            subprocess.Popen(['/usr/sbin/nginx', '-s', 'reload'], stdout=FNULL, stderr=subprocess.STDOUT)


# This hook script is supposed to be called after account creation by cPanel
installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
# Loading the json in on stdin send by cPanel
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
cur_pkg = mydict["cur_pkg"].encode('utf-8')
new_pkg = mydict["new_pkg"].encode('utf-8')
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
            if os.path.isfile(installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"):
                TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"
            else:
                if os.path.isfile(installation_path+"/conf/domain_data_default_local.yaml"):
                    TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local.yaml"
                else:
                    TEMPLATE_FILE = installation_path+"/conf/domain_data_default.yaml"
        if os.path.isfile(cpuserdatajson) and os.path.isfile(TEMPLATE_FILE):
            with open(TEMPLATE_FILE, 'r') as profileyaml_data_stream:
                yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
            phpmaxchildren = yaml_parsed_profileyaml.get('phpmaxchildren', '16')
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
            setphpmaxchildren = 'sed -i "s/^pm.max_children.*/pm.max_children = '+phpmaxchildren+'" '+installation_path+'/php-fpm.d/'+cpaneluser+'.conf'
            subprocess.call(setphpmaxchildren, shell=True)
        if os.path.isfile(installation_path+'/secure-php-fpm.d/'+cpaneluser+'.conf'):
            setsecurephpmaxchildren = 'sed -i "s/^pm.max_children.*/pm.max_children = '+phpmaxchildren+'" '+installation_path+'/secure-php-fpm.d/'+cpaneluser+'.conf'
            subprocess.call(setsecurephpmaxchildren, shell=True)
        subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
        nginxreload()
        print("1 nDeploy:account_change_package:"+cpaneluser)
