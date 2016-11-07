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
app_template_file = installation_path+"/conf/apptemplates_subdir.yaml"
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
        subdir_apps = yaml_parsed_profileyaml.get('subdir_apps', None)
        cpaneluser = os.environ["USER"]
        cpdomainjson = "/var/cpanel/userdata/" + cpaneluser + "/" + mydomain + ".cache"
        with open(cpdomainjson, 'r') as cpaneldomain_data_stream:
            json_parsed_cpaneldomain = json.load(cpaneldomain_data_stream)
        document_root = json_parsed_cpaneldomain.get('documentroot')
        print(('<p style="background-color:LightGrey">Configuring subdirectory apps for:  '+mydomain+'</p>'))
        # get the currently configured subdir
        if subdir_apps:
            print('<HR>')
            print(('<p style="background-color:LightGrey">curently configured subdirectory apps for:  '+mydomain+'</p>'))
            for thesubdir in subdir_apps.keys():
                print('<div class="boxedyellow">')
                print('<form action="subdir_app_settings.live.py">')
                print(thesubdir)
                print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
                print(('<input style="display:none" name="thesubdir" value="'+thesubdir+'">'))
                print('<input type="submit" value="Edit Application Settings">')
                print('</form>')
                print('</div>')
        print('<HR>')
        print(('<p style="background-color:LightGrey">Add new subdirectory apps for:  '+mydomain+'</p>'))
        print('<div class="boxedyellow">')
        print('Enter the directory below&nbsp;&nbsp;(eg:&nbsp;&nbsp;blog&nbsp;&nbsp;us/forum&nbsp;&nbsp;etc.)')
        print('<form action="subdir_app_settings.live.py">')
        print(document_root+'/')
        print('<input type="text" name="thesubdir">')
        print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
        print('<input type="submit" value="Submit">')
        print('</form>')
        print('</div>')
    else:
        print('ERROR : domain-data file i/o error')
else:
    print('ERROR : Forbidden')
print('</body>')
print('</html>')
