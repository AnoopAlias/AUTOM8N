#!/usr/bin/env python
import os
import socket
import sys
import yaml
import cgi
import cgitb


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


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
cpuserdatayaml = "/var/cpanel/userdata/" + cpaneluser + "/main"
cpaneluser_data_stream = open(cpuserdatayaml, 'r')
yaml_parsed_cpaneluser = yaml.safe_load(cpaneluser_data_stream)
cpaneluser_data_stream.close()
main_domain = yaml_parsed_cpaneluser.get('main_domain')
sub_domains = yaml_parsed_cpaneluser.get('sub_domains')


print('Content-Type: text/html')
print('') 
print('<html>')
print('<head>')
print('<title>nDeploy</title>')
print('</head>')
print('<body>')
print('<H2 style="color:grey"><a href="ndeploy.live.cgi"><img border="0" src="nDeploy.png" alt="nDeploy"></a>nDeploy</H2>')
print('<HR>')
print('<form action="selector.live.cgi" method="post">')
print('<select name="domain">')
print('<option value="'+main_domain+'">'+main_domain+'</option>')
if os.path.isfile("/var/cpanel/userdata/" + cpaneluser + "/" + main_domain + "_SSL"):
    print('<option value="'+main_domain+'_SSL">'+main_domain+'(SSL)</option>')
for domain_in_subdomains in sub_domains:
    print('<option value="'+domain_in_subdomains+'">'+domain_in_subdomains+'</option>')
    if os.path.isfile("/var/cpanel/userdata/" + cpaneluser + "/" + domain_in_subdomains + "_SSL"):
        print('<option value="'+domain_in_subdomains+'_SSL">'+domain_in_subdomains+'(SSL)</option>')
print('</select>')
print('<HR>')
print('<input type="submit" value="CONFIGURE">')
print('</form>')
print('<p style="color:grey; background-color:yellow">(!) For Addon domain select the corresponding subdomain</p>')
print('<p style="color:grey; background-color:yellow">(!) click on the icon above to restart the configuration process anytime</p>')
print('</body>')
print('</html>')
