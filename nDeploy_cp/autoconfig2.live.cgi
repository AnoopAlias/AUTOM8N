#!/usr/bin/python
import os
import socket
import yaml
import cgi
import cgitb


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
profile_config_file = installation_path+"/conf/profiles.yaml"


cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()
    return


close_cpanel_liveapisock()
form = cgi.FieldStorage()


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
print('<a href="ndeploy.live.cgi"><img border="0" src="nDeploy.png" alt="nDeploy"></a>')
print('<HR>')
if form.getvalue('domain') and form.getvalue('backend'):
    mydomain = form.getvalue('domain')
    mybackend = form.getvalue('backend')
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        profileyaml_data_stream = open(profileyaml, 'r')
        yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        profileyaml_data_stream.close()
        if os.path.isfile(backend_config_file) and os.path.isfile(profile_config_file):
            backend_data_yaml = open(backend_config_file, 'r')
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
            backend_data_yaml.close()
            profile_data_yaml = open(profile_config_file,'r')
            profile_data_yaml_parsed = yaml.safe_load(profile_data_yaml)
            profile_data_yaml.close()
            print(('<p style="background-color:LightGrey">CONFIGURE:  '+mydomain+'</p>'))
            print('<HR>')
            profile_branch_dict = profile_data_yaml_parsed[mybackend]
            backends_branch_dict = backend_data_yaml_parsed[mybackend]
            print('<form action="update.live.cgi" method="post">')
            print('<p style="background-color:LightGrey">Select backend type: </p>')
            print('<select name="version">')
            for versions_defined in list(backends_branch_dict.keys()):
                print(('<option value="'+versions_defined+'">'+versions_defined+'</option>'))
            print('</select>')
            print('<HR>')
            print('<p style="background-color:LightGrey">Select a configuration template: </p>')
            print('<select name="pcode">')
            for profile_code in list(profile_branch_dict.keys()):
                iter_profile_string = profile_branch_dict[profile_code]
                print(('<option value="'+profile_code+'">'+iter_profile_string+'</option>'))
            print('</select>')
            print('<HR>')
            print('<p style="background-color:LightGrey">Enable/Disable Google PageSpeed Optimizations: </p>')
            print('<input type="radio" name="pagespeed" value="0" checked/> DISABLE')
            print('<input type="radio" name="pagespeed" value="1" /> ENABLE')
            print('<HR>')
            print('<p style="background-color:LightGrey">NAXSI Web Application Firewall: </p>')
            print('<input type="radio" name="naxsi" value="0" checked/> LEARN-MODE')
            print('<input type="radio" name="naxsi" value="1" /> ENFORCE-MODE')
            print('<HR>')
            print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
            print(('<input style="display:none" name="backend" value="'+mybackend+'">'))
            print('<input type="submit" value="GENERATE">')
            print('</form>')
        else:
            print('ERROR : nDeploy backend defs file i/o error')
    else:
        print('ERROR : domain-data file i/o error')
else:
    print('ERROR : Forbidden')
print('</body>')
print('</html>')
