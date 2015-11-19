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
print('</head>')
print('<body>')
print('<a href="ndeploy.live.cgi"><img border="0" src="nDeploy.png" alt="nDeploy"></a>')
print('<HR>')
if form.getvalue('domain'):
    mydomain = form.getvalue('domain')
    domainyaml = "/var/cpanel/userdata/" + cpaneluser + "/" + mydomain
    domainyaml_data_stream = open(domainyaml, 'r')
    yaml_parsed_domainyaml = yaml.safe_load(domainyaml_data_stream)
    domainyaml_data_stream.close()
    main_domain = yaml_parsed_domainyaml.get('servername')
    server_aliases = yaml_parsed_domainyaml.get('serveralias')
    if server_aliases:
        server_aliases_list = server_aliases.split(' ')
    else:
        server_aliases_list = []
    homedir = yaml_parsed_domainyaml.get('homedir')
    if main_domain.startswith('*.'):
        outputfile = homedir + '/_wildcard_.'+main_domain.replace('*.', '') + '.naxsi.wl'
        naxsiwlconffile = '/etc/nginx/sites-enabled' + '/_wildcard_.'+main_domain.replace('*.', '') + '.nxapi.wl'
    else:
        outputfile = homedir + '/' + main_domain + '.naxsi.wl'
        naxsiwlconffile = '/etc/nginx/sites-enabled/' + main_domain + '.nxapi.wl'
    subprocess.call('/usr/nginx/nxapi/nxtool.py --colors -c /usr/nginx/nxapi/nxapi.json -s '+main_domain+' -w /etc/nginx/sites-enabled/' + main_domain + '.nxapi.wl --tag > /dev/null', shell=True)
    subprocess.call('/usr/nginx/nxapi/nxtool.py --colors -c /usr/nginx/nxapi/nxapi.json -s ' + main_domain + ' -f --slack >> ' + outputfile, shell=True)
    for aliases in server_aliases_list:
        subprocess.call('/usr/nginx/nxapi/nxtool.py --colors -c /usr/nginx/nxapi/nxapi.json -s ' + aliases + ' -w /etc/nginx/sites-enabled/' + main_domain + '.nxapi.wl --tag > /dev/null', shell=True)
        subprocess.call('/usr/nginx/nxapi/nxtool.py --colors -c /usr/nginx/nxapi/nxapi.json -s ' + aliases + ' -f --slack >> ' + outputfile, shell=True)
    print('<p style="background-color:LightGrey"> Whitelist generated . Download whitelist file  ' + outputfile + ' using FTP</p>')
    print('<p style="background-color:LightGrey">You must analyze the file and copy genuine whitelist rules starting with BasicRule </p>')
    print('<p style="background-color:LightGrey">Update new rules below and click "UPDATE WHITELIST"</p>')
    print('<HR>')
    print('<form action="naxsiupdate.live.cgi" method="post">')
    print('<textarea name="textcontent" cols="120" rows="50">')
    with open(naxsiwlconffile, 'r') as content_file:
                content = content_file.read()
    content_file.close()
    print(content)
    print('</textarea>')
    print('<HR>')
    print('<input type="submit" value="UPDATE WHITELIST" />')
    print(('<input style="display:none" name="domain" value="'+main_domain+'">'))
    print('</form>')
else:
    print('ERROR : Forbidden')
print('</body>')
print('</html>')
