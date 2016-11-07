#!/usr/bin/python
import os
import socket
import cgi
import cgitb


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
app_template_file = installation_path+"/conf/apptemplates.yaml"


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
    print(('<p style="background-color:LightGrey">CONFIGURING:  '+mydomain+'</p>'))
    print('<HR>')
    print('<div class="boxedyellow">')
    print('<form action="server_settings.live.py" method="post">')
    print(('<center><p style="background-color:LightGrey">Configure -  content optimizations / redirections/ server headers etc. </p></center>'))
    print('<center><input type="submit" value="SERVER SETTINGS"></center>')
    # Pass on the domain name to the next stage
    print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
    print('</form>')
    print('</div>')
    print('<HR>')
    print('<div class="boxedyellow">')
    print('<form action="app_settings.live.py" method="post">')
    print(('<center><p style="background-color:LightGrey">Configure -  application server / version / application template etc </p></center>'))
    print('<center><input type="submit" value="APPLICATION SETTINGS"></center>')
    # Pass on the domain name to the next stage
    print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
    print('</form>')
    print('</div>')
    print('<HR>')
    print('<div class="boxedyellow">')
    print('<form action="subdir_selector.live.py" method="post">')
    print(('<center><p style="background-color:LightGrey">Configure -  applications installed in sub-directory like domain.com/blog/ </p></center>'))
    print('<center><input type="submit" value="APPLICATION IN SUB-DIRECTORY"></center>')
    # Pass on the domain name to the next stage
    print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
    print('</form>')
    print('</div>')
    print('<HR>')
    print('<div class="boxedyellow">')
    print('<form action="directory_privacy.live.py" method="post">')
    print(('<center><p style="background-color:LightGrey">Configure -  password protected URL </p></center>'))
    print('<center><input type="submit" value="PASSWORD PROTECTED URL"></center>')
    # Pass on the domain name to the next stage
    print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
    print('</form>')
    print('</div>')
    print('<HR>')
else:
    print('ERROR : Forbidden')
print('</body>')
print('</html>')
