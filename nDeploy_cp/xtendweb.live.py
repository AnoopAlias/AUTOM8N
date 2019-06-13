#!/usr/bin/env python

import commoninclude
import os
import socket
import yaml
import cgitb
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"


cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


close_cpanel_liveapisock()
cpaneluser = os.environ["USER"]
cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
with open(cpuserdatajson, 'r') as cpaneluser_data_stream:
    json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
main_domain = json_parsed_cpaneluser.get('main_domain')
# parked_domains = yaml_parsed_cpaneluser.get('parked_domains')   # This data is irrelevant as parked domain list is in ServerAlias
addon_domains_dict = json_parsed_cpaneluser.get('addon_domains')     # So we know which addon is mapped to which sub-domain
sub_domains = json_parsed_cpaneluser.get('sub_domains')

# Settings Lock
if os.path.exists("/var/cpanel/users.cache/" + cpaneluser):
    with open("/var/cpanel/users.cache/" + cpaneluser) as users_file:
        json_parsed_cpusersfile = json.load(users_file)
    hostingplan_filename = json_parsed_cpusersfile.get('PLAN', 'default').encode('utf-8').replace(' ', '_')
else:
    hostingplan_filename = 'default'
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
with open(TEMPLATE_FILE, 'r') as templatefile_data_stream:
    yaml_parsed_templatefile = yaml.safe_load(templatefile_data_stream)
settings_lock = yaml_parsed_templatefile.get('settings_lock', 'disabled')


commoninclude.print_header()

print('<body>')

commoninclude.print_branding()

print('<div id="main-container" class="container">')    # main container

print('		<nav aria-label="breadcrumb">')
print('			<ol class="breadcrumb">')
print('				<li class="breadcrumb-item"><a href="xtendweb.live.py"><i class="fas fa-redo"></i></a></li>')
print('				<li class="breadcrumb-item active">Config</li>')
print('			</ol>')
print('		</nav>')

print('		<div class="row justify-content-lg-center">')
print('			<div class="col-lg-6">')

# Auto Switch To Nginx
print('				<div class="card">')  # card
print('					<div class="card-header">')
print('						<h5 class="card-title mb-0"><i class="fas fa-cogs float-right"></i> Auto/Manual Configuration</h5>')
print('					</div>')
print('					<div class="card-body">')  # card-body

if settings_lock == 'enabled':
    print(('				<div class="alert alert-info">Application Server settings are locked by the administrator</div>'))
else:
    print('					<form class="form mb-4" method="post" id="modalForm9" onsubmit="return false;">')
    print('						<button class="btn btn-outline-primary btn-block " type="submit">Auto Switch To Nginx</button>')
    print(('					<input class="hidden" name="cpaneluser" value="'+cpaneluser+'">'))
    print('					</form>')

print('						<form class="form" action="app_settings.live.py" method="get">')
print('							<div class="input-group mb-0">')
print('								<select name="domain" class="custom-select">')
print(('								<option value="'+main_domain+'">'+main_domain+'</option>'))
for domain_in_subdomains in sub_domains:
    if domain_in_subdomains not in addon_domains_dict.values():
        if domain_in_subdomains.startswith("*"):
            wildcard_domain = "_wildcard_."+domain_in_subdomains.replace('*.', '')
            print(('					<option value="'+wildcard_domain+'">'+domain_in_subdomains+'</option>'))
        else:
            print(('					<option value="'+domain_in_subdomains+'">'+domain_in_subdomains+'</option>'))
for the_addon_domain in addon_domains_dict.keys():
    print(('							<option value="'+addon_domains_dict.get(the_addon_domain)+'">'+the_addon_domain+'</option>'))
print('								</select>')
print('								<div class="input-group-append">')
print('									<button class="btn btn-outline-primary" type="submit">Configure</button>')
print('								</div>')
print('							</div>')
print('						</form>')

print('					</div>')  # card-body end
print('				</div>')  # card end
print('			</div>')  # col end
print('		</div>')  # row end

print('</div>')  # main-container end

commoninclude.print_modals()
commoninclude.print_loader()

print('</body>')
print('</html>')
