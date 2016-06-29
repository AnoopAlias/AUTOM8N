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
myhome = os.environ["HOME"]


cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()
    return


def update_config_test_status(profile_yaml, value):
    """Function to set custom profile status in domain data yaml"""
    yaml_data_stream_toupdate = open(profile_yaml, 'r')
    yaml_profile_datadict = yaml.safe_load(yaml_data_stream_toupdate)
    yaml_data_stream_toupdate.close()
    yaml_profile_datadict["testconf"] = str(value)
    with open(profile_yaml, 'w') as yaml_file:
        yaml_file.write(yaml.dump(yaml_profile_datadict, default_flow_style=False))
    yaml_file.close()
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
if form.getvalue('domain'):
    mydomain = form.getvalue('domain')
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        profileyaml_data_stream = open(profileyaml, 'r')
        yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        profileyaml_data_stream.close()
        backend_data_yaml = open(backend_config_file, 'r')
        backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
        backend_data_yaml.close()
        print(('<p style="background-color:LightGrey">CONFIGURE:  '+mydomain+'</p>'))
        print('<HR>')
        if form.getvalue('textcontent'):
            text_content = form.getvalue('textcontent')
            custom_conf_file = myhome + '/' + mydomain + '_nginx.include.custom.conf'
            with open(custom_conf_file, 'w') as outfile:
                outfile.write(text_content)
            outfile.close()
            update_config_test_status(profileyaml, 1)
            print('<div class="boxedblue">')
            print('Custom config with errors will not be activated <br>')
            print(('All custom edits are saved in ' + myhome + '/' + mydomain + '_nginx.include.custom.conf'+'<br>'))
            print('</div>')
        elif form.getvalue('version') and form.getvalue('pcode') and form.getvalue('pagespeed') and form.getvalue('backend') and form.getvalue('naxsi'):
            mypcode = form.getvalue('pcode')
            mypagespeed = form.getvalue('pagespeed')
            mynaxsi = form.getvalue('naxsi')
            mybackend = form.getvalue('backend')
            myversion = form.getvalue('version')
            backends_branch_dict = backend_data_yaml_parsed[mybackend]
            mypath = backends_branch_dict[myversion]
            yaml_parsed_profileyaml['backend_path'] = mypath
            yaml_parsed_profileyaml['backend_category'] = mybackend
            yaml_parsed_profileyaml['backend_version'] = myversion
            yaml_parsed_profileyaml['profile'] = mypcode
            yaml_parsed_profileyaml['pagespeed'] = mypagespeed
            yaml_parsed_profileyaml['naxsi'] = mynaxsi
            with open(profileyaml, 'w') as yaml_file:
                yaml_file.write(yaml.dump(yaml_parsed_profileyaml, default_flow_style=False))
            yaml_file.close()
            print(('<p style="background-color:LightGrey">CONFIGURATION SAVED FOR:  '+mydomain+'</p>'))
        else:
            print('ERROR : Invalid POST data')
    else:
        print('ERROR : domain-data file i/o error')
else:
    print('ERROR : Forbidden')
print('</body>')
print('</html>')
