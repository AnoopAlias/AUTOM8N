#!/usr/bin/python
import os
import socket
import yaml
import cgi
import cgitb
import sys

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
print('<a href="ndeploy.live.cgi"><img border="0" src="nDeploy.png" alt="nDeploy"></a>')
print('<HR>')
# Get the domain name
if 'domain' in form.keys():
    mydomain = form.getvalue('domain')
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# autoindex
if 'autoindex' in form.keys():
    autoindex = form.getvalue('autoindex')
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# ssl_offload
if 'ssl_offload' in form.keys():
    ssl_offload = form.getvalue('ssl_offload')
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# pagespeed
if 'pagespeed' in form.keys():
    pagespeed = form.getvalue('pagespeed')
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# brotli
if 'brotli' in form.keys():
    brotli = form.getvalue('brotli')
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# gzip
if 'gzip' in form.keys():
    gzip = form.getvalue('gzip')
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# gzip
if 'gzip' in form.keys():
    gzip = form.getvalue('gzip')
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)




print(('<p style="background-color:LightGrey">CONFIGURING:  '+mydomain+'</p>'))
print('<HR>')
