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

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>nDeploy</title>')
print('</head>')
print('<body>')
print('<a href="apache_fpm.live.cgi"><img border="0" src="php-fpm.png" alt="nDeploy - Apache php-fpm"></a>')
print('<HR>')
if os.path.isfile(backend_config_file):
    backend_data_yaml = open(backend_config_file, 'r')
    backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    backend_data_yaml.close()
    if "PHP" in backend_data_yaml_parsed and os.path.isfile(installation_path+"/user-data/"+cpaneluser) and os.path.isfile(installation_path+"/conf/user_data.yaml.tmpl"):
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        userdatayaml = installation_path+"/user-data/"+cpaneluser
        userdatayaml_data_stream = open(userdatayaml, 'r')
        yaml_parsed_userdata = yaml.safe_load(userdatayaml_data_stream)
        userdatayaml_data_stream.close()
        myversion = yaml_parsed_userdata.get('PHP')
        print('<HR>')
        print('Active PHP-FPM backend for Apache httpd : '+myversion)
        print('<HR>')
        print('<form action="save_phpversion.live.cgi" method="post">')
        print('Select new PHP version')
        print('<select name="phpversion">')
        for versions_defined in list(php_backends_dict.keys()):
            print(('<option value="'+versions_defined+'">'+versions_defined+'</option>'))
        print('</select>')
        print('<HR>')
        print('<input type="submit" value="SUBMIT">')
        print('</form>')
    else:
        print('Apache PHP-FPM plugin not enabled')
        print('<br>')
else:
    print('ERROR: Unable to access backend config file')
print('<HR>')
print('<p style="background-color:LightGrey">(!) click on the php-fpm icon above to restart the configuration process anytime</p>')
print('<p style="background-color:LightGrey">(!) Apache PHP-FPM plugin works only if you set nginX plugin to PROXY mode</p>')
print('<p style="background-color:LightGrey">(!) and set template : Proxy to cPanel httpd / cPanel httpd(SSL)</p>')

print('</body>')
print('</html>')
