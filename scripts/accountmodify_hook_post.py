#!/usr/bin/env python

import os
import sys
import pwd
import subprocess
import shutil
import yaml
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


# This script is supposed to be called by cPanel after an account is modified
# All we need to do is call config generator with the new username as arg
installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
nginx_dir = "/etc/nginx/sites-enabled/"

# Get the values send by cPanel in stdin
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
# Assuming someone changed the cPanel username
cpanelnewuser = mydict["newuser"]
cpaneluser = mydict["user"]
maindomain = mydict["domain"]
# Calling the config generate script for the user
if cpanelnewuser != cpaneluser:
    if os.path.exists(cluster_config_file):
        subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m user -a "name='+cpaneluser+' state=absent remove=yes"', shell=True)
    silentremove(installation_path + "/php-fpm.d/" + cpaneluser + ".conf")
    subprocess.Popen(installation_path+"/scripts/init_backends.py reload", shell=True)
    cpuserdatajson = installation_path+"/lock/"+cpaneluser+".userdata"
    if os.path.exists(cpuserdatajson):
        with open(cpuserdatajson, 'r') as cpaneluser_data_stream:
            json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
        main_domain = json_parsed_cpaneluser.get('main_domain')
        sub_domains = json_parsed_cpaneluser.get('sub_domains')
        silentremove(installation_path+"/domain-data/"+main_domain)
        silentremove(nginx_dir+main_domain+".conf")
        silentremove(nginx_dir+main_domain+".include")
        if os.path.isfile(cluster_config_file):
            with open(cluster_config_file, 'r') as cluster_data_yaml:
                cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            for server in cluster_data_yaml_parsed.keys():
                silentremove("/etc/nginx/"+server+"/"+main_domain+".conf")
                silentremove("/etc/nginx/"+server+"/"+main_domain+".include")
        if os.path.exists('/var/resin/hosts/'+main_domain):
            shutil.rmtree('/var/resin/hosts/'+main_domain)
        for domain_in_subdomains in sub_domains:
            if domain_in_subdomains.startswith("*"):
                domain_in_subdomains = "_wildcard_."+domain_in_subdomains.replace('*.', '')
            silentremove(installation_path+"/domain-data/"+domain_in_subdomains)
            silentremove(nginx_dir+domain_in_subdomains+".conf")
            silentremove(nginx_dir+domain_in_subdomains+".include")
            if os.path.isfile(cluster_config_file):
                with open(cluster_config_file, 'r') as cluster_data_yaml:
                    cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
                for server in cluster_data_yaml_parsed.keys():
                    silentremove("/etc/nginx/"+server+"/"+domain_in_subdomains+".conf")
                    silentremove("/etc/nginx/"+server+"/"+domain_in_subdomains+".include")
            if os.path.exists('/var/resin/hosts/'+domain_in_subdomains):
                shutil.rmtree('/var/resin/hosts/'+domain_in_subdomains)
        subprocess.Popen("/usr/sbin/nginx -s reload", shell=True)
        silentremove(cpuserdatajson)
    subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpanelnewuser, shell=True)
    if os.path.exists(cluster_config_file):
        cpaneluserhome = pwd.getpwnam(cpanelnewuser).pw_dir
        # Create the new user
        subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m user -a "name='+cpanelnewuser+' home='+cpaneluserhome+'"', shell=True)
        subprocess.call(installation_path + "/scripts/cluster_dns_ensure_user.py "+cpanelnewuser, shell=True)
        subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpanelnewuser, shell=True)
    print(("1 nDeploy:postmodify:"+cpanelnewuser))
else:
    # Get details of current main-domain and sub-domain stored in cPanel datastore
    cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
    with open(cpuserdatajson, 'r') as cpaneluser_data_stream:
        json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
    main_domain = json_parsed_cpaneluser.get('main_domain')
    sub_domains = json_parsed_cpaneluser.get('sub_domains')
    if maindomain != main_domain:
            silentremove(installation_path+"/domain-data/"+main_domain)
            silentremove(nginx_dir+main_domain+".conf")
            silentremove(nginx_dir+main_domain+".include")
            if os.path.isfile(cluster_config_file):
                with open(cluster_config_file, 'r') as cluster_data_yaml:
                    cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
                for server in cluster_data_yaml_parsed.keys():
                    silentremove("/etc/nginx/"+server+"/"+main_domain+".conf")
                    silentremove("/etc/nginx/"+server+"/"+main_domain+".include")
            if os.path.exists('/var/resin/hosts/'+main_domain):
                shutil.rmtree('/var/resin/hosts/'+main_domain)
            for domain_in_subdomains in sub_domains:
                if domain_in_subdomains.startswith("*"):
                    domain_in_subdomains = "_wildcard_."+domain_in_subdomains.replace('*.', '')
                silentremove(installation_path+"/domain-data/"+domain_in_subdomains)
                silentremove(nginx_dir+domain_in_subdomains+".conf")
                silentremove(nginx_dir+domain_in_subdomains+".include")
                if os.path.isfile(cluster_config_file):
                    with open(cluster_config_file, 'r') as cluster_data_yaml:
                        cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
                    for server in cluster_data_yaml_parsed.keys():
                        silentremove("/etc/nginx/"+server+"/"+domain_in_subdomains+".conf")
                        silentremove("/etc/nginx/"+server+"/"+domain_in_subdomains+".include")
                if os.path.exists('/var/resin/hosts/'+domain_in_subdomains):
                    shutil.rmtree('/var/resin/hosts/'+domain_in_subdomains)
    subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpaneluser, shell=True)
    if os.path.exists(cluster_config_file):
        subprocess.call(installation_path + "/scripts/cluster_dns_ensure_user.py "+cpaneluser, shell=True)
        subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpanelnewuser, shell=True)
    print(("1 nDeploy:postmodify:"+cpaneluser))
