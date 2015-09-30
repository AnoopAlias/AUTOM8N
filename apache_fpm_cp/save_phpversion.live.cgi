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
backend_config_file = installation_path+"/conf/backends.yaml"


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
print('</head>')
print('<body>')
print('<a href="apache_fpm.live.cgi"><img border="0" src="php-fpm.png" alt="nDeploy - Apache php-fpm"></a>')
print('<HR>')
if form.getvalue('phpversion'):
    if os.path.isfile(installation_path+"/user-data/"+cpaneluser):
        userdatayaml = installation_path+"/user-data/"+cpaneluser
        userdatayaml_data_stream = open(userdatayaml, 'r')
        yaml_parsed_userdata = yaml.safe_load(userdatayaml_data_stream)
        phpversion = form.getvalue('phpversion')
        yaml_parsed_userdata['PHP'] = phpversion
        userdatayaml_data_stream.close()
        with open(userdatayaml, 'w') as yaml_file:
            yaml_file.write(yaml.dump(yaml_parsed_userdata, default_flow_style=False))
        yaml_file.close()
        print('Apache will now use PHP-FPM version: ' + phpversion)
    else:
        print('ERROR : cannot access userdata')
else:
    print('ERROR: Forbidden')
print('</body>')
print('</html>')
