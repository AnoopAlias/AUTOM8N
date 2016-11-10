#!/usr/bin/env python


import sys
import os
import subprocess
try:
    import simplejson as json
except ImportError:
    import json
import shutil


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


# This hook script is called by cPanel before an account is modified
# We are intrested in username and main-domain name modifications
# Mainly take care of removing stuff here as the post-accountmodify hook will
# take care of creating new configs
installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_dir = "/etc/nginx/sites-enabled/"

# Get data send by cPanel on stdin
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpanelnewuser = mydict["newuser"]
cpaneluser = mydict["user"]
maindomain = mydict["domain"]

# Get details of current main-domain and sub-domain stored in cPanel datastore
cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
with open(cpuserdatajson, 'r') as cpaneluser_data_stream:
    json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
main_domain = json_parsed_cpaneluser.get('main_domain')
sub_domains = json_parsed_cpaneluser.get('sub_domains')
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
# If cPanel username is modified
if cpanelnewuser != cpaneluser or maindomain != main_domain:
    if cpanelnewuser != cpaneluser:
        # Remove php-fpm pool file and reload php-fpm
        silentremove(installation_path + "/php-fpm.d/" + cpaneluser + ".conf")
        subprocess.Popen(installation_path+"/scripts/init_backends.py reload", shell=True)
    # Remove domains associated with the user
    silentremove(installation_path+"/domain-data/"+main_domain)
    silentremove(nginx_dir+main_domain+".conf")
    silentremove(nginx_dir+main_domain+".include")
    silentremove(nginx_dir+main_domain+".nxapi.wl")
    if os.path.isfile(installation_path+"/conf/ndeploy_cluster_slaves"):
        with open(installation_path+"/conf/ndeploy_cluster_slaves") as cluster_slave_list:
            for server in cluster_slave_list:
                silentremove("/etc/nginx/"+server.replace('\n', '')+"/"+main_domain+".conf")
                silentremove("/etc/nginx/"+server.replace('\n', '')+"/"+main_domain+".include")
                silentremove("/etc/nginx/"+server.replace('\n', '')+"/"+main_domain+".nxapi.wl")
    if os.path.exists('/var/resin/hosts/'+main_domain):
        shutil.rmtree('/var/resin/hosts/'+main_domain)
    for domain_in_subdomains in sub_domains:
        if domain_in_subdomains.startswith("*"):
            domain_in_subdomains = "_wildcard_."+domain_in_subdomains.replace('*.', '')
        silentremove(installation_path+"/domain-data/"+domain_in_subdomains)
        silentremove(nginx_dir+domain_in_subdomains+".conf")
        silentremove(nginx_dir+domain_in_subdomains+".include")
        silentremove(nginx_dir+domain_in_subdomains+".nxapi.wl")
        if os.path.isfile(installation_path+"/conf/ndeploy_cluster_slaves"):
            with open(installation_path+"/conf/ndeploy_cluster_slaves") as cluster_slave_list:
                for server in cluster_slave_list:
                    silentremove("/etc/nginx/"+server.replace('\n', '')+"/"+domain_in_subdomains+".conf")
                    silentremove("/etc/nginx/"+server.replace('\n', '')+"/"+domain_in_subdomains+".include")
                    silentremove("/etc/nginx/"+server.replace('\n', '')+"/"+domain_in_subdomains+".nxapi.wl")
        if os.path.exists('/var/resin/hosts/'+domain_in_subdomains):
            shutil.rmtree('/var/resin/hosts/'+domain_in_subdomains)
    print("1 nDeploy:olddomain:"+main_domain+":newdomain:"+maindomain+":olduser:"+cpaneluser+":newuser:"+cpanelnewuser)
else:
    print("1 nDeploy::skiphook::accountModify::pre")
