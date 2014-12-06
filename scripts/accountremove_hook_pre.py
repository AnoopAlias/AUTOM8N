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


# Function defs
def remove_php_fpm_pool(user_name):
    """Remove the php-fpm pools of deleted accounts"""
    backend_data_yaml = open(backend_config_file, 'r')
    backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    backend_data_yaml.close()
    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        for php_path in list(php_backends_dict.values()):
            phppool_file = php_path + "/etc/fpm.d/" + user_name + ".conf"
            if os.path.isfile(phppool_file):
                os.remove(phppool_file)
                subprocess.call("kill -USR2 `cat " + php_path + "/var/run/php-fpm.pid`", shell=True)
    return



cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
cpuserdatayaml = "/var/cpanel/userdata/" + cpaneluser + "/main"
cpaneluser_data_stream = open(cpuserdatayaml, 'r')
yaml_parsed_cpaneluser = yaml.safe_load(cpaneluser_data_stream)
cpaneluser_data_stream.close()
main_domain = yaml_parsed_cpaneluser.get('main_domain')
sub_domains = yaml_parsed_cpaneluser.get('sub_domains')

os.remove(installation_path+"/domain-data/"+main_domain)
os.remove(nginx_dir+main_domain+".conf")
os.remove(nginx_dir+main_domain+".include")
subprocess.call("rm -rf /var/resin/hosts/"+main_domain, shell=True)
if os.path.isfile("/var/cpanel/userdata/" + cpaneluser + "/" + main_domain + "_SSL"):
    os.remove(installation_path+"/domain-data/"+main_domain+"_SSL")
    os.remove(nginx_dir+main_domain+"_SSL.conf")
    os.remove(nginx_dir+main_domain+"_SSL.include")
for domain_in_subdomains in sub_domains:
    os.remove(installation_path+"/domain-data/"+domain_in_subdomains)
    os.remove(nginx_dir+domain_in_subdomains+".conf")
    os.remove(nginx_dir+domain_in_subdomains+".include")
    subprocess.call("rm -rf /var/resin/hosts/"+domain_in_subdomains, shell=True)
    if os.path.isfile("/var/cpanel/userdata/" + cpaneluser + "/" + domain_in_subdomains + "_SSL"):
        os.remove(installation_path+"/domain-data/"+domain_in_subdomains+"_SSL")
        os.remove(nginx_dir+domain_in_subdomains+"_SSL.conf")
        os.remove(nginx_dir+domain_in_subdomains+"_SSL.include")
remove_php_fpm_pool(cpaneluser)
subprocess.call("/usr/sbin/nginx -s reload", shell=True)
print("1 nDeploy:remove:"+cpaneluser)
