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
cpaneluser = os.environ["USER"]
user_app_template_file = installation_path+"/conf/"+cpaneluser+"_apptemplates.yaml"
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
print('<title>XtendWeb</title>')
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
print('<a href="xtendweb.live.py" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.live.py"><span class="glyphicon glyphicon-refresh"></span></a></li>')
print('<li><a href="xtendweb.live.py">Select Domain</a></li><li class="active">Application Settings</li>')
print('</ol>')
print('<div class="panel panel-default">')
if form.getvalue('domain') and form.getvalue('backend'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    mybackend = form.getvalue('backend')
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
        backend_category = yaml_parsed_profileyaml.get('backend_category')
        backend_version = yaml_parsed_profileyaml.get('backend_version')
        backend_path = yaml_parsed_profileyaml.get('backend_path')
        apptemplate_code = yaml_parsed_profileyaml.get('apptemplate_code')
        # get the human friendly name of the app template
        if os.path.isfile(app_template_file):
            with open(app_template_file, 'r') as apptemplate_data_yaml:
                apptemplate_data_yaml_parsed = yaml.safe_load(apptemplate_data_yaml)
            apptemplate_dict = apptemplate_data_yaml_parsed.get(backend_category)
            if os.path.isfile(user_app_template_file):
                with open(user_app_template_file, 'r') as user_apptemplate_data_yaml:
                    user_apptemplate_data_yaml_parsed = yaml.safe_load(user_apptemplate_data_yaml)
                user_apptemplate_dict = user_apptemplate_data_yaml_parsed.get(backend_category)
            else:
                user_apptemplate_dict = {}
            if apptemplate_code in apptemplate_dict.keys():
                apptemplate_description = apptemplate_dict.get(apptemplate_code)
            else:
                if apptemplate_code in user_apptemplate_dict.keys():
                    apptemplate_description = user_apptemplate_dict.get(apptemplate_code)
        else:
            print('<div class="alert alert-danger">ERROR: app template data file error</div>')
            sys.exit(0)
        # Ok we are done with getting the settings,now lets present it to the user
        print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'</strong></h3></div>'))
        print('<div class="panel-body">')
        print('<form id="config" class="form-inline config-save" action="save_app_settings.live.py" method="post">')
        print('<ul class="list-group">')
        if backend_category == 'PROXY':
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6 col-radio"><strong>NGINX is proxying to</strong></div>')
            print(('<div class="col-sm-6"><div class="label label-info">'+backend_version+'</div></div>'))
            print('</div>')
            print('</li>')
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6 col-radio"><strong>Template</strong></div>')
            print(('<div class="col-sm-6"><div class="label label-info">'+apptemplate_description+'</div></div>'))
            print('</div>')
            print('</li>')
            print('</ul>')
        else:
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6 col-radio"><strong>native NGINX and</strong></div>')
            print(('<div class="col-sm-6"><div class="label label-info">'+backend_category+'</div></div>'))
            print('</div>')
            print('</li>')
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6 col-radio"><strong>Backend Version</strong></div>')
            print('<div class="col-sm-6"><div class="label label-info">'+backend_version+'</div></div>')
            print('</div>')
            print('</li>')
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6 col-radio"><strong>Template</strong></div>')
            print(('<div class="col-sm-6"><div class="label label-info">'+apptemplate_description+'</div></div>'))
            print('</div>')
            print('</li>')
        print('</ul>')
        print(('<div class="alert alert-info alert-top">You selected <span class="label label-info">'+mybackend+'</span> as the new backend, select the version and template for this backend below</div>'))
        backends_dict = backend_data_yaml_parsed.get(mybackend)
        new_apptemplate_dict = apptemplate_data_yaml_parsed.get(mybackend)
        if os.path.isfile(user_app_template_file):
            user_new_apptemplate_dict = user_apptemplate_data_yaml_parsed.get(mybackend)
        else:
            user_new_apptemplate_dict = {}
        if mybackend == backend_category:
            print('<div class="row">')
            print('<div class="col-sm-6">')
            print('<div class="panel panel-default">')
            print('<div class="panel-heading"><h3 class="panel-title">Backend version</h3></div>')
            print('<div class="panel-body">')
            print('<select name="backendversion">')
            for mybackend_version in backends_dict.keys():
                if mybackend_version == backend_version:
                    print(('<option selected value="'+mybackend_version+'">'+mybackend_version+'</option>'))
                else:
                    print(('<option value="'+mybackend_version+'">'+mybackend_version+'</option>'))
            print('</select>')
            print('</div>')
            print('</div>')
            print('</div>')
            print('<div class="col-sm-6">')
            print('<div class="panel panel-default">')
            print('<div class="panel-heading"><h3 class="panel-title">Application template</h3></div>')
            print('<div class="panel-body">')
            print('<select name="apptemplate">')
            for myapptemplate in new_apptemplate_dict.keys():
                if myapptemplate == apptemplate_code:
                    print(('<option selected value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
                else:
                    print(('<option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
            if user_new_apptemplate_dict:
                for user_myapptemplate in user_new_apptemplate_dict.keys():
                    if user_myapptemplate == apptemplate_code:
                        print(('<option selected value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>'))
                    else:
                        print(('<option value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>'))
            print('</select>')
            print('</div>')
            print('</div>')
            print('</div>')
            print('</div>')
        else:
            print('<div class="row">')
            print('<div class="col-sm-6">')
            print('<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">Backend version</h3></div>')
            print('<div class="panel-body">')
            print('<select name="backendversion">')
            for mybackend_version in backends_dict.keys():
                print(('<option value="'+mybackend_version+'">'+mybackend_version+'</option>'))
            print('</select>')
            print('</div>')
            print('</div>')
            print('</div>')
            print('<div class="col-sm-6">')
            print('<div class="panel panel-default"><div class="panel-heading"><h3 class="panel-title">Application template</h3></div>')
            print('<div class="panel-body">')
            print('<select name="apptemplate">')
            for myapptemplate in new_apptemplate_dict.keys():
                print(('<option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
            if user_new_apptemplate_dict:
                for user_myapptemplate in user_new_apptemplate_dict.keys():
                    print(('<option value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>'))
            print('</select>')
            print('</div>')
            print('</div>')
            print('</div>')
            print('</div>')
        # Pass on the domain name to the next stage
        print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
        print(('<input class="hidden" name="backend" value="'+mybackend+'">'))
        print('<input class="btn btn-primary" type="submit" value="Submit">')
        print('</form>')
    else:
        print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> domain-data file i/o error</div>')
else:
    print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden</div>')
print('</div>')
print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
