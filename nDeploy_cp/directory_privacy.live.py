#!/usr/bin/python
import os
import socket
import yaml
import cgi
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
form = cgi.FieldStorage()


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
if form.getvalue('domain'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        protected_dir = yaml_parsed_profileyaml.get('protected_dir', None)
        cpaneluser = os.environ["USER"]
        cpdomainjson = "/var/cpanel/userdata/" + cpaneluser + "/" + mydomain + ".cache"
        with open(cpdomainjson, 'r') as cpaneldomain_data_stream:
            json_parsed_cpaneldomain = json.load(cpaneldomain_data_stream)
        document_root = json_parsed_cpaneldomain.get('documentroot')
        print(('<p style="background-color:LightGrey">Configuring password protected URL for:  '+mydomain+'</p>'))
        print('<HR>')
        print('<div class="boxedyellow">')
        print('password protection works along with cPanel - "Directory Privacy" feature')
        print('<br>')
        print('please setup a password for the folder in cPanel >> FILES >> Directory Privacy')
        print('<br>')
        print('the path entered below must begin with a "/"&nbsp;&nbsp;examples are&nbsp;&nbsp;/&nbsp;&nbsp;/blog&nbsp;&nbsp;/blog/dev  etc.')
        print('</div>')
        print('<div class="boxedyellow">')
        print('Enter the path below:<br>')
        print('<form action="save_directory_privacy.live.py">')
        print(document_root)
        print('<input type="text" name="protectedurl">')
        print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
        print(('<input style="display:none" name="action" value="add">'))
        print('<input type="submit" value="Submit">')
        print('</form>')
        print('</div>')
        if protected_dir:
            print('<HR>')
            print(('<p style="background-color:LightGrey">list of configured password protected URL for:  '+mydomain+'</p>'))
            for theurl in protected_dir:
                print('<div class="boxedyellow">')
                print('<form action="save_directory_privacy.live.py">')
                print(document_root+theurl)
                print('<input type="submit" value="Delete">')
                print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
                print(('<input style="display:none" name="action" value="del">'))
                print(('<input style="display:none" name="protectedurl" value="'+theurl+'">'))
                print('</form>')
                print('</div>')
    else:
        print('ERROR : domain-data file i/o error')
else:
    print('ERROR : Forbidden')
print('</body>')
print('</html>')
