#!/usr/bin/env python
import os
import socket
import yaml
import subprocess
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
form = cgi.FieldStorage()
cpaneluser = os.environ["USER"]

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>nDeploy</title>')
print('<style>')
print('.boxedyellow {border: 1px solid grey;background-color:LightYellow;font-size: 12px}')
print('.boxedblue {border: 1px solid grey;background-color:LightBlue;font-size: 12px}')
print('</style>')
print('</head>')
print('<body>')
print('<a href="ndeploy.live.cgi"><img border="0" src="letsencrypt.png" alt="nDeploy"></a>')
print('<HR>')
if form.getvalue('domain'):
    if os.path.isfile(installation_path+"/conf/letsencrypt.yaml"):
        mydomain = form.getvalue('domain')
        if mydomain.startswith('*.'):
            print('<p style="background-color:LightGrey">(!) Letsencrypt does not support wildcard domain names</p>')
        else:
            profileyaml = installation_path + "/domain-data/" + mydomain
            if os.path.isfile(profileyaml):
                profileyaml_data_stream = open(profileyaml, 'r')
                yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
                profileyaml_data_stream.close()
                letsencrypt = yaml_parsed_profileyaml.get('letsencrypt')
                if letsencrypt == "1":
                    status = "ENABLED"
                else:
                    status = "DISABLED"
                print('LetsEncrypt cert is currently '+status+' for the domain')
                print('<HR>')
                print('<form action="save_letsencrypt.live.cgi" method="post">')
                print('ENABLE or DISABLE LetsEncrypt cert')
                print('<select name="letsencrypt_status">')
                print(('<option value="1">ENABLE</option>'))
                print(('<option value="0">DISABLE</option>'))
                print('</select>')
                print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
                print('<input type="submit" value="SUBMIT">')
                print('</form>')
            else:
                print("ERROR: domain-data file i/o error")
    else:
        print("ERROR: LetsEncrypt is not setup. Please contact your Server Administrator")
else:
    print('ERROR : Forbidden')
print('</body>')
print('</html>')
