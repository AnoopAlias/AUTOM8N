#!/usr/bin/env python
import os
import socket
import yaml
import cgi
import cgitb
import subprocess


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
form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>nDeploy</title>')
print('<style>')
print('.boxedyellow {border: 1px solid grey;background-color:LightYellow;font-size: 10px}')
print('.boxedblue {border: 1px solid grey;background-color:LightBlue;font-size: 10px}')
print('</style>')
print('</head>')
print('<body>')
print('<a href="ndeploy.live.cgi"><img border="0" src="letsencrypt.png" alt="nDeploy - LetsEncrypt"></a>')
print('<HR>')
if form.getvalue('letsencrypt_status') and form.getvalue('domain'):
    mydomain = form.getvalue('domain')
    letsencrypt_status = form.getvalue('letsencrypt_status')
    if os.path.isfile(installation_path+"/domain-data/"+mydomain):
        domaindatayaml = installation_path+"/domain-data/"+mydomain
        domaindatayaml_data_stream = open(domaindatayaml, 'r')
        yaml_parsed_domaindata = yaml.safe_load(domaindatayaml_data_stream)
        yaml_parsed_domaindata['letsencrypt'] = letsencrypt_status
        if letsencrypt_status == "0":
            yaml_parsed_domaindata['leretry'] = "0"
        domaindatayaml_data_stream.close()
        with open(domaindatayaml, 'w') as yaml_file:
            yaml_file.write(yaml.dump(yaml_parsed_domaindata, default_flow_style=False))
        yaml_file.close()
        if letsencrypt_status == "1":
            print('<p style="background-color:LightGrey">(!) LetsEncrypt cert is now enabled</p>')
            print('<p style="background-color:LightGrey">(!) Certificates installed via WHM/cPanel will have precedence</p>')
            print('<p style="background-color:LightGrey">(!) You must delete the SSL host in WHM to ensure LetsEncrypt cert usage</p>')
            print('<HR>')
            print('<p style="background-color:LightGrey">(!) Cert is only enabled in nginX</p>')
            print('<p style="background-color:LightGrey">(!) So if you are PROXY-ing to cPanel httpd</p>')
            print('<p style="background-color:LightGrey">(!) Ensure backend is "apache" and template is "Proxy to cPanel httpd"</p>')
        else:
            print('<p style="background-color:LightGrey">(!) LetsEncrypt cert is disabled</p>')
    else:
        print('ERROR : cannot access domaindata')
else:
    print('ERROR: Forbidden')
print('</body>')
print('</html>')
