#!/usr/bin/env python

import subprocess
import json
import os
import jinja2
import codecs


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


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
# Initiate Jinja2 templateEnv
templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
templateEnv = jinja2.Environment(loader=templateLoader)
templateVars = {"CPIPLIST": cpanel_ip_list,
                "MAINIP": mainip,
                "CPSRVDSSL": cpsrvdsslfile
                }
# Generate default_server.conf
default_server_template = templateEnv.get_template('default_server.conf.j2')
default_server_config = default_server_template.render(templateVars)
with codecs.open('/etc/nginx/conf.d/default_server.conf', 'w', 'utf-8') as default_server_config_file:
    default_server_config_file.write(default_server_config)
# Generate cpanel_services.conf
cpanel_services_template = templateEnv.get_template('cpanel_services.conf.j2')
cpanel_services_config = cpanel_services_template.render(templateVars)
with codecs.open('/etc/nginx/conf.d/cpanel_services.conf', 'w', 'utf-8') as cpanel_services_config_file:
    cpanel_services_config_file.write(cpanel_services_config)
# Generate httpd_mod_remoteip.include
httpd_mod_remoteip_template = templateEnv.get_template('httpd_mod_remoteip.include.j2')
httpd_mod_remoteip_config = httpd_mod_remoteip_template.render(templateVars)
with codecs.open('/etc/nginx/conf.d/httpd_mod_remoteip.include', 'w', 'utf-8') as httpd_mod_remoteip_config_file:
    httpd_mod_remoteip_config_file.write(httpd_mod_remoteip_config)
# Generate yoast_seo_wordpress.conf
yoast_seo_wordpress_template = templateEnv.get_template('yoast_seo_wordpress.conf.j2')
yoast_seo_wordpress_config = yoast_seo_wordpress_template.render(templateVars)
with codecs.open('/etc/nginx/conf.d/yoast_seo_wordpress.conf', 'w', 'utf-8') as yoast_seo_wordpress_config_file:
    yoast_seo_wordpress_config_file.write(yoast_seo_wordpress_config)
