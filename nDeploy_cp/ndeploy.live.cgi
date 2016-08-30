#!/usr/bin/env python
import os
import socket
import yaml
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
print('<style>')
print('.boxedyellow {border:1px solid grey;background-color:LightYellow;font-size:12px}')
print('.boxedblue {border:1px solid grey;background-color:LightBlue;font-size:12px}')
print('</style>')
print('</head>')
print('<body>')
print('<a href="ndeploy.live.cgi"><img border="0" src="nDeploy.png" alt="nDeploy"></a>')
print('<HR>')
print('<form action="selector.live.cgi" method="post">')
print('<select name="domain">')
if main_domain.startswith('*.'):
    print(('<option value="_wildcard_.'+main_domain.replace('*.', '')+'">'+main_domain+'</option>'))
    if os.path.isfile(installation_path+"/domain-data/_wildcard_."+main_domain.replace('*.', '')+"_SSL"):
        print(('<option value="_wildcard_.'+main_domain.replace('*.', '')+'_SSL">'+main_domain+'(SSL)</option>'))
else:
    print(('<option value="'+main_domain+'">'+main_domain+'</option>'))
    if os.path.isfile(installation_path+"/domain-data/"+main_domain+"_SSL"):
        print(('<option value="'+main_domain+'_SSL">'+main_domain+'(SSL)</option>'))

for domain_in_subdomains in sub_domains:
    if domain_in_subdomains.startswith('*.'):
        print(('<option value="_wildcard_.'+domain_in_subdomains.replace('*.', '')+'">'+domain_in_subdomains+'</option>'))
        if os.path.isfile(installation_path+"/domain-data/_wildcard_." + domain_in_subdomains.replace('*.', '') + "_SSL"):
            print(('<option value="_wildcard_.'+domain_in_subdomains.replace('*.', '')+'_SSL">'+domain_in_subdomains+'(SSL)</option>'))
    else:
        print(('<option value="'+domain_in_subdomains+'">'+domain_in_subdomains+'</option>'))
        if os.path.isfile(installation_path+"/domain-data/" + domain_in_subdomains + "_SSL"):
            print(('<option value="'+domain_in_subdomains+'_SSL">'+domain_in_subdomains+'(SSL)</option>'))
print('</select>')
print('<input type="submit" value="CONFIGURE">')
print('</form>')
print('<div class="boxedyellow">')
print('For Addon domain select the corresponding subdomain<br>')
print('Click on the nginx icon above to restart the configuration process anytime<br>')
print('</div>')
if os.path.isfile("/usr/nginx/scripts/nxapi-learn.sh"):
  print('<HR>')
  print('<form action="naxsiwl.live.cgi" method="post">')
  print('<select name="domain">')
  print(('<option value="'+main_domain+'">'+main_domain+'</option>'))
  for domain_in_subdomains in sub_domains:
      print(('<option value="'+domain_in_subdomains+'">'+domain_in_subdomains+'</option>'))
  print('</select>')
  print('<input type="submit" value="GENERATE NAXSI WHITELIST">')
  print('</form>')
print('</body>')
print('</html>')
