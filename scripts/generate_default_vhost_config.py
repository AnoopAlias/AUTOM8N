#!/usr/bin/env python3

import subprocess
import json
import os
import jinja2
import codecs
import yaml
import socket
import hashlib

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"

backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()
if backend_data_yaml_parsed is not None:
    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
    else:
        php_backends_dict = {}
else:
    php_backends_dict = {}

myhostname = socket.gethostname()
iplist_json = json.loads(subprocess.Popen(['/usr/local/cpanel/bin/whmapi1', 'listips', '--output=json'], stdout=subprocess.PIPE).communicate()[0])
data_dict = iplist_json.get('data')
ip_list = data_dict.get('ip')
cpanel_ip_list = []
for myip in ip_list:
    theip = myip.get('ip')
    cpanel_ip_list.append(theip)
    mainaddr_status = myip.get('mainaddr')
    if mainaddr_status == 1:
        mainip = theip
if os.path.isfile('/var/cpanel/ssl/cpanel/mycpanel.pem'):
    cpsrvdsslfile = '/var/cpanel/ssl/cpanel/mycpanel.pem'
else:
    cpsrvdsslfile = '/var/cpanel/ssl/cpanel/cpanel.pem'
if os.path.isfile('/opt/nDeploy/conf/disable_default_vhost_ddos_protection'):
    default_ddos = 'disabled'
else:
    default_ddos = 'enabled'
slaveiplist = []
upstream_setup_dict = {}
if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):  # get the cluster ipmap
    cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
    cluster_data_yaml = open(cluster_config_file, 'r')
    cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    cluster_data_yaml.close()
    serverlist = list(cluster_data_yaml_parsed.keys())
    for slaveserver in serverlist:
        server_dict = cluster_data_yaml_parsed.get(slaveserver)
        ipmap_dict = server_dict.get('dnsmap')
        theiplist = list(ipmap_dict.values())
        slaveiplist = list(set(slaveiplist + theiplist))
        ipmapping_dict = server_dict.get('ipmap')
        for the_upstream_ip in ipmapping_dict.keys():
            if os.path.isfile('/var/cpanel/cpnat'):
                with open('/var/cpanel/cpnat') as f:
                    content = f.readlines()
                content = [x.strip() for x in content]
                if content:
                    upstream_master_ip = the_upstream_ip
                    for line in content:
                        internalip, externalip = line.split()
                        if internalip == the_upstream_ip:
                            upstream_master_ip = externalip
                            break
                else:
                    upstream_master_ip = the_upstream_ip
            else:
                upstream_master_ip = the_upstream_ip
            upstream_slave_ip = ipmapping_dict.get(the_upstream_ip)
            upstream_ident = hashlib.md5((slaveserver+the_upstream_ip).encode('utf-8')).hexdigest()
            upstream_setup_dict[upstream_ident]=[upstream_master_ip, upstream_slave_ip]
# Initiate Jinja2 templateEnv
templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
templateEnv = jinja2.Environment(loader=templateLoader)
templateVars = {"CPIPLIST": cpanel_ip_list,
                "PHPDICT": php_backends_dict,
                "MAINIP": mainip,
                "CPSRVDSSL": cpsrvdsslfile,
                "SLAVEIPLIST": slaveiplist,
                "MYHOSTNAME": myhostname,
                "DEFAULT_VHOST_DDOS": default_ddos,
                "PROXY_TO_MASTER": False,
                "MASTER_MAINIP": '127.0.0.1',
                "UPSTREAM_SETUP_DICT": upstream_setup_dict
                }
# Generate default_server.conf
if os.path.isfile(installation_path+'/conf/default_server_local.conf.j2'):
    my_default_server_conf = 'default_server_local.conf.j2'
else:
    my_default_server_conf = 'default_server.conf.j2'
default_server_template = templateEnv.get_template(my_default_server_conf)
default_server_config = default_server_template.render(templateVars)
with codecs.open('/etc/nginx/conf.d/default_server.conf', 'w', 'utf-8') as default_server_config_file:
    default_server_config_file.write(default_server_config)
# Generate proxy_subdomain.conf
proxy_subdomain_template = templateEnv.get_template('proxy_subdomain.conf.j2')
proxy_subdomain_config = proxy_subdomain_template.render(templateVars)
with codecs.open('/etc/nginx/conf.d/proxy_subdomain.conf', 'w', 'utf-8') as proxy_subdomain_config_file:
    proxy_subdomain_config_file.write(proxy_subdomain_config)
# Generate httpd_mod_remoteip.include
httpd_mod_remoteip_template = templateEnv.get_template('httpd_mod_remoteip.include.j2')
httpd_mod_remoteip_config = httpd_mod_remoteip_template.render(templateVars)
with codecs.open('/etc/nginx/conf.d/httpd_mod_remoteip.include', 'w', 'utf-8') as httpd_mod_remoteip_config_file:
    httpd_mod_remoteip_config_file.write(httpd_mod_remoteip_config)
# Generate the upstream config to be used in slave nodes
upstream_conf_template = templateEnv.get_template('upstream.conf.j2')
upstream_conf_config = upstream_conf_template.render(templateVars)
with codecs.open('/etc/nginx/conf.d/upstream.conf', 'w', 'utf-8') as upstream_conf_config_file:
    upstream_conf_config_file.write(upstream_conf_config)
