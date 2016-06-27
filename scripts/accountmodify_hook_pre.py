#!/usr/bin/env python


import yaml
import sys
import json
import os
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
nginx_dir = "/etc/nginx/sites-enabled/"


cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpanelnewuser = mydict["newuser"]
cpaneluser = mydict["user"]
maindomain = mydict["domain"]
cpuserdatayaml = "/var/cpanel/userdata/" + cpaneluser + "/main"
cpaneluser_data_stream = open(cpuserdatayaml, 'r')
yaml_parsed_cpaneluser = yaml.safe_load(cpaneluser_data_stream)
cpaneluser_data_stream.close()
main_domain = yaml_parsed_cpaneluser.get('main_domain')
sub_domains = yaml_parsed_cpaneluser.get('sub_domains')
if cpanelnewuser != cpaneluser:
    try:
        os.remove(installation_path + "/php-fpm.d/" + cpaneluser + ".conf")
    except OSError:
        pass
    subprocess.call(installation_path+"/scripts/init_backends.py reload", shell=True)
    os.remove(installation_path+"/domain-data/"+main_domain)
    os.remove(nginx_dir+main_domain+".conf")
    os.remove(nginx_dir+main_domain+".include")
    os.remove(nginx_dir+main_domain+".nxapi.wl")
    subprocess.call("rm -rf /var/resin/hosts/"+main_domain, shell=True)
    if os.path.isfile("/var/cpanel/userdata/" + cpaneluser + "/" + main_domain + "_SSL"):
        os.remove(installation_path+"/domain-data/"+main_domain+"_SSL")
        os.remove(nginx_dir+main_domain+"_SSL.conf")
        os.remove(nginx_dir+main_domain+"_SSL.include")
    for domain_in_subdomains in sub_domains:
        if domain_in_subdomains.startswith("*"):
            domain_in_subdomains = "_wildcard_."+domain_in_subdomains.replace('*.', '')
        os.remove(installation_path+"/domain-data/"+domain_in_subdomains)
        os.remove(nginx_dir+domain_in_subdomains+".conf")
        os.remove(nginx_dir+domain_in_subdomains+".include")
        os.remove(nginx_dir+domain_in_subdomains+".nxapi.wl")
        subprocess.call("rm -rf /var/resin/hosts/"+domain_in_subdomains, shell=True)
        if os.path.isfile("/var/cpanel/userdata/" + cpaneluser + "/" + domain_in_subdomains + "_SSL"):
            os.remove(installation_path+"/domain-data/"+domain_in_subdomains+"_SSL")
            os.remove(nginx_dir+domain_in_subdomains+"_SSL.conf")
            os.remove(nginx_dir+domain_in_subdomains+"_SSL.include")
    print(("1 nDeploy:olduser:"+cpaneluser+":newuser:"+cpanelnewuser))
elif maindomain != main_domain:
    os.remove(installation_path+"/domain-data/"+main_domain)
    os.remove(nginx_dir+main_domain+".conf")
    os.remove(nginx_dir+main_domain+".include")
    os.remove(nginx_dir+main_domain+".nxapi.wl")
    subprocess.call("rm -rf /var/resin/hosts/"+main_domain, shell=True)
    if os.path.isfile("/var/cpanel/userdata/" + cpaneluser + "/" + main_domain + "_SSL"):
        os.remove(installation_path+"/domain-data/"+main_domain+"_SSL")
        os.remove(nginx_dir+main_domain+"_SSL.conf")
        os.remove(nginx_dir+main_domain+"_SSL.include")
    subprocess.call("/usr/sbin/nginx -s reload", shell=True)
    print(("1 nDeploy:olddomain:"+main_domain+":newdomain:"+maindomain))
else:
    print("1 nDeploy::skiphook")
