#!/usr/bin/env python


import os
import socket
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


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>nDeploy</title>')
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<a href="xtendweb.live.py"><img border="0" src="xtendweb.png" alt="nDeploy"></a>')
print('<HR>')
print(('<p style="background-color:LightGrey">select domain to configure: </p>'))
print('<form action="selector.live.py" method="post">')
print('<select name="domain">')
print(('<option value="'+main_domain+'">'+main_domain+'</option>'))
for domain_in_subdomains in sub_domains:
    if domain_in_subdomains not in addon_domains_dict.values():
        print(('<option value="'+domain_in_subdomains+'">'+domain_in_subdomains+'</option>'))
for the_addon_domain in addon_domains_dict.keys():
    print(('<option value="'+addon_domains_dict.get(the_addon_domain)+'">'+the_addon_domain+'</option>'))
print('</select>')
print('<input type="submit" value="CONFIGURE">')
print('</form>')
print('<div class="boxedyellow">')
print('Click on the nginx icon above to restart the configuration process anytime')
print('</div>')
print('</body>')
print('</html>')
