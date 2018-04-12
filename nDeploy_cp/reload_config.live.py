#!/usr/bin/python
import os
import socket
import yaml
import cgi
import cgitb


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"


cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


def branding_print_logo_name():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_logo = yaml_parsed_brand.get("brand_logo", "xtendweb.png")
    else:
        brand_logo = "xtendweb.png"
    return brand_logo


def branding_print_banner():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_name = yaml_parsed_brand.get("brand", "XtendWeb")
    else:
        brand_name = "XtendWeb"
    return brand_name


def branding_print_footer():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_footer = yaml_parsed_brand.get("brand_footer", '<a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">A U T O M 8 N</a>')
    else:
        brand_footer = '<a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">A U T O M 8 N</a>'
    return brand_footer


close_cpanel_liveapisock()
form = cgi.FieldStorage()


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')

print('<title>')
print(branding_print_banner())
print('</title>')

print(('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'))
print(('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" crossorigin="anonymous"></script>'))
print(('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<div id="main-container" class="container text-center">')  # marker1
print('<div class="row">')  # marker2
print('<div class="col-md-6 col-md-offset-3">')  # marker3

print('<div class="logo">')
print('<a href="xtendweb.live.py"><img border="0" src="')
print(branding_print_logo_name())
print('" width="48" height="48"></a>')
print('<h4>')
print(branding_print_banner())
print('</h4>')
print('</div>')

print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.live.py"><span class="glyphicon glyphicon-repeat"></span></a></li>')
print('<li><a href="xtendweb.live.py">Select Domain</a></li><li class="active">Application Settings</li>')
print('</ol>')
if form.getvalue('domain'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
        print('<div class="panel panel-default">')
        print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'</strong></h3></div>'))
        print('<div class="panel-body">')
        print('<div class="icon-box">')
        print('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> Nginx configuration reloaded')
        print('</div>')
        print('</div>')
        print('</div>')
    else:
        print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> domain-data file i/o error</div>')
else:
    print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden</div>')

print('<div class="panel-footer"><small>')
print(branding_print_footer())
print('</small></div>')

print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
