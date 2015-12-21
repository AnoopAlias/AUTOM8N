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
    subprocess.call("touch "+installation_path+"/lock/todel_"+cpaneluser, shell=True)
    fhandle = open(installation_path+"/lock/todel_"+cpaneluser, 'a')
    fhandle.write(installation_path+"/domain-data/"+main_domain+"\n")
    fhandle.write(installation_path+"/user-data/"+cpaneluser+"\n")
    fhandle.write(nginx_dir+main_domain+".conf\n")
    fhandle.write(nginx_dir+main_domain+".include\n")
    subprocess.call("rm -rf /var/resin/hosts/"+main_domain, shell=True)
    if os.path.isfile("/var/cpanel/userdata/" + cpaneluser + "/" + main_domain + "_SSL"):
        fhandle.write(installation_path+"/domain-data/"+main_domain+"_SSL\n")
        fhandle.write(nginx_dir+main_domain+"_SSL.conf\n")
        fhandle.write(nginx_dir+main_domain+"_SSL.include\n")
    for domain_in_subdomains in sub_domains:
        fhandle.write(installation_path+"/domain-data/"+domain_in_subdomains+"\n")
        fhandle.write(nginx_dir+domain_in_subdomains+".conf\n")
        fhandle.write(nginx_dir+domain_in_subdomains+".include\n")
        subprocess.call("rm -rf /var/resin/hosts/"+domain_in_subdomains, shell=True)
        if os.path.isfile("/var/cpanel/userdata/" + cpaneluser + "/" + domain_in_subdomains + "_SSL"):
            fhandle.write(installation_path+"/domain-data/"+domain_in_subdomains+"_SSL\n")
            fhandle.write(nginx_dir+domain_in_subdomains+"_SSL.conf\n")
            fhandle.write(nginx_dir+domain_in_subdomains+"_SSL.include\n")
    fhandle.close()
    print(("1 nDeploy:olduser:"+cpaneluser+":newuser:"+cpanelnewuser))
elif maindomain != main_domain:
    subprocess.call("touch "+installation_path+"/lock/todel_"+cpaneluser, shell=True)
    fhandle = open(installation_path+"/lock/todel_"+cpaneluser, 'a')
    fhandle.write(installation_path+"/domain-data/"+main_domain+"\n")
    fhandle.write(nginx_dir+main_domain+".conf\n")
    fhandle.write(nginx_dir+main_domain+".include\n")
    if os.path.isfile("/var/cpanel/userdata/" + cpaneluser + "/" + main_domain + "_SSL"):
        fhandle.write(installation_path+"/domain-data/"+main_domain+"_SSL\n")
        fhandle.write(nginx_dir+main_domain+"_SSL.conf\n")
        fhandle.write(nginx_dir+main_domain+"_SSL.include\n")
    subprocess.call("/usr/sbin/nginx -s reload", shell=True)
    fhandle.close()
    print(("1 nDeploy:olddomain:"+main_domain+":newdomain:"+maindomain))
else:
    print("1 nDeploy::skiphook")
