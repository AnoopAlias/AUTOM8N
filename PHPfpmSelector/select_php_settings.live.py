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
cpaneluser = os.environ["USER"]
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
print('<title>PHP-FPM Selector</title>')
print(('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'))
print(('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" crossorigin="anonymous"></script>'))
print(('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<div id="main-container" class="container text-center">')
print('<div class="row">')
print('<div class="col-md-6 col-md-offset-3">')
print('<div class="logo">')
print('<a href="phpfpm_selector.live.py" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span></a>')
print('<h4>PHP-FPM Selector</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="phpfpm_selector.live.py"><span class="glyphicon glyphicon-refresh"></span></a></li>')
print('<li><a href="phpfpm_selector.live.py">Select Domain</a></li><li class="active">PHP-FPM Selector</li>')
print('</ol>')
print('<div class="panel panel-default">')
if form.getvalue('domain'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    profileyaml = installation_path + "/domain-data/" + mydomain
    # Get data about the backends available
    if os.path.isfile(backend_config_file):
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    if os.path.isfile(profileyaml):
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        # App settings
        phpfpm_selector = yaml_parsed_profileyaml.get('phpfpm_selector', None)
        phpfpm_path = yaml_parsed_profileyaml.get('phpfpm_path', None)
        # Ok we are done with getting the settings,now lets present it to the user
        print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'</strong></h3></div>'))

        print('<div class="panel-body">')

        print('<ul class="list-group">')
        backends_dict = backend_data_yaml_parsed.get("PHP")

        print('<li class="list-group-item">')
        print('<div class="row">')
        print('<div class="col-sm-6 col-radio"><strong>current PHP-FPM Version</strong></div>')
        print(('<div class="col-sm-6"><div class="label label-success">'+phpfpm_selector+'</div></div>'))
        print('</div>')
        print('</li>')

        print('<li class="list-group-item">')
        print('<div class="row">')

        # print('<div class="col-sm-6">')
        print('<div class="panel panel-default">')
        print('<div class="panel-heading"><h3 class="panel-title">SELECT PHP</h3></div>')
        print('<div class="panel-body">')
        print('<form id="config" class="form-inline config-save" action="save_php_settings.live.py" method="post">')
        print(('<div class="col-sm-6">'))
        print('<select name="phpfpm">')
        for mybackend_version in backends_dict.keys():
            if mybackend_version == phpfpm_selector:
                print(('<option selected value="'+mybackend_version+'">'+mybackend_version+'</option>'))
            else:
                print(('<option value="'+mybackend_version+'">'+mybackend_version+'</option>'))
        print('</select>')
        print('</div>')
        print(('<div class="col-sm-6">'))
        print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
        print('<input class="btn btn-primary" type="submit" value="Submit">')
        print('</div>')
        print('</form>')
        print('</div>')
        print('</div>')
        # print('</div>')
        print('</div>')
        print('</li>')

        print('</div>')
    else:
        print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> domain-data file i/o error</div>')
else:
    print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden</div>')
print('</div>')
print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
