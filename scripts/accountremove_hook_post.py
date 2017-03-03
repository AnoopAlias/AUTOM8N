#!/usr/bin/env python


import sys
import subprocess
import os
import shutil
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_dir = "/etc/nginx/sites-enabled/"


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
# If cluster is configured , we remove user from cluster
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
    subprocess.Popen("/usr/sbin/nginx -s reload", shell=True)
    silentremove(cpuserdatajson)
    print(("1 nDeploy:remove:post:"+cpaneluser))
