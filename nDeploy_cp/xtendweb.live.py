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
print('<title>XtendWeb</title>')
print(('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'))
print(('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" crossorigin="anonymous"></script>'))
print(('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<div id="main-container" class="container text-center">')
print('<div class="row">')
print('<div class="col-md-6 col-md-offset-3">')
print('<div class="logo">')
print('<a href="xtendweb.live.py" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-cog" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.live.py"><span class="glyphicon glyphicon-home"></span></a></li>')
print('<li class="active">Select domain</li>')
print('</ol>')
print('<div class="panel panel-default">')
print('<div class="panel-heading"><h3 class="panel-title">Select domain to configure:</h3></div>')
print('<div class="panel-body">')
print('<form class="form-inline" action="selector.live.py" method="post">')
print('<select name="domain">')
print(('<option value="'+main_domain+'">'+main_domain+'</option>'))
for domain_in_subdomains in sub_domains:
    if domain_in_subdomains not in addon_domains_dict.values():
        if domain_in_subdomains.startswith("*"):
            wildcard_domain = "_wildcard_."+domain_in_subdomains.replace('*.', '')
            print(('<option value="'+wildcard_domain+'">'+domain_in_subdomains+'</option>'))
        else:
            print(('<option value="'+domain_in_subdomains+'">'+domain_in_subdomains+'</option>'))
for the_addon_domain in addon_domains_dict.keys():
    print(('<option value="'+addon_domains_dict.get(the_addon_domain)+'">'+the_addon_domain+'</option>'))
print('</select>')
print('<input class="btn btn-primary" type="submit" value="CONFIGURE">')
print('</div>')
print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')