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
print('<a href="xtendweb.live.py"><img border="0" src="xtendweb.png" alt="nDeploy"></a>')
print('<HR>')
# Get the domain name
if 'domain' in form.keys():
    mydomain = form.getvalue('domain')
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# Getting the current domain data
profileyaml = installation_path + "/domain-data/" + mydomain
if os.path.isfile(profileyaml):
    # Get all config settings from the domains domain-data config file
    with open(profileyaml, 'r') as profileyaml_data_stream:
        yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
else:
    print('ERROR : Domain data file i/o error')
    print('</body>')
    print('</html>')
    sys.exit(0)
# autoindex
if 'autoindex' in form.keys():
    autoindex = form.getvalue('autoindex')
    yaml_parsed_profileyaml['autoindex'] = autoindex
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# ssl_offload
if 'ssl_offload' in form.keys():
    ssl_offload = form.getvalue('ssl_offload')
    yaml_parsed_profileyaml['ssl_offload'] = ssl_offload
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# pagespeed
if 'pagespeed' in form.keys():
    pagespeed = form.getvalue('pagespeed')
    yaml_parsed_profileyaml['pagespeed'] = pagespeed
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# brotli
if 'brotli' in form.keys():
    brotli = form.getvalue('brotli')
    yaml_parsed_profileyaml['brotli'] = brotli
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# gzip
if 'gzip' in form.keys():
    gzip = form.getvalue('gzip')
    yaml_parsed_profileyaml['gzip'] = gzip
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# http2
if 'http2' in form.keys():
    http2 = form.getvalue('http2')
    yaml_parsed_profileyaml['http2'] = http2
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# access_log
if 'access_log' in form.keys():
    access_log = form.getvalue('access_log')
    yaml_parsed_profileyaml['access_log'] = access_log
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# open_file_cache
if 'open_file_cache' in form.keys():
    open_file_cache = form.getvalue('open_file_cache')
    yaml_parsed_profileyaml['open_file_cache'] = open_file_cache
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# clickjacking_protect
if 'clickjacking_protect' in form.keys():
    clickjacking_protect = form.getvalue('clickjacking_protect')
    yaml_parsed_profileyaml['clickjacking_protect'] = clickjacking_protect
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# disable_contenttype_sniffing
if 'disable_contenttype_sniffing' in form.keys():
    disable_contenttype_sniffing = form.getvalue('disable_contenttype_sniffing')
    yaml_parsed_profileyaml['disable_contenttype_sniffing'] = disable_contenttype_sniffing
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# xss_filter
if 'xss_filter' in form.keys():
    xss_filter = form.getvalue('xss_filter')
    yaml_parsed_profileyaml['xss_filter'] = xss_filter
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# content_security_policy
if 'content_security_policy' in form.keys():
    content_security_policy = form.getvalue('content_security_policy')
    yaml_parsed_profileyaml['content_security_policy'] = content_security_policy
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# hsts
if 'hsts' in form.keys():
    hsts = form.getvalue('hsts')
    yaml_parsed_profileyaml['hsts'] = hsts
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# dos_mitigate
if 'dos_mitigate' in form.keys():
    dos_mitigate = form.getvalue('dos_mitigate')
    yaml_parsed_profileyaml['dos_mitigate'] = dos_mitigate
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# naxsi
if 'naxsi' in form.keys():
    naxsi = form.getvalue('naxsi')
    yaml_parsed_profileyaml['naxsi'] = naxsi
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# naxsi_mode
if 'naxsi_mode' in form.keys():
    naxsi_mode = form.getvalue('naxsi_mode')
    yaml_parsed_profileyaml['naxsi_mode'] = naxsi_mode
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# redirect_to_ssl
if 'redirect_to_ssl' in form.keys():
    redirect_to_ssl = form.getvalue('redirect_to_ssl')
    yaml_parsed_profileyaml['redirect_to_ssl'] = redirect_to_ssl
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# redirect_aliases
if 'redirect_aliases' in form.keys():
    redirect_aliases = form.getvalue('redirect_aliases')
    yaml_parsed_profileyaml['redirect_aliases'] = redirect_aliases
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
# wwwredirect
if 'wwwredirect' in form.keys():
    wwwredirect = form.getvalue('wwwredirect')
    yaml_parsed_profileyaml['wwwredirect'] = wwwredirect
else:
    print('ERROR : Forbidden')
    print('</body>')
    print('</html>')
    sys.exit(0)
print(('<p style="background-color:LightGrey">CONFIGURING:  '+mydomain+'</p>'))
print('<HR>')
with open(profileyaml, 'w') as yaml_file:
    yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
print('<div class="boxedyellow">')
print('configuration for '+mydomain+' saved')
print('</div>')
print('</body>')
print('</html>')
