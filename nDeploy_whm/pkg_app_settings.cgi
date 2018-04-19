#!/usr/bin/python
import cgi
import cgitb
import os
import yaml
import sys


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
default_domain_data_file = installation_path+'/conf/domain_data_default.yaml'
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"


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


cgitb.enable()

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
print('<a href="xtendweb.cgi"><img border="0" src="')
print(branding_print_logo_name())
print('" width="48" height="48"></a>')
print('<h4>')
print(branding_print_banner())
print('</h4>')
print('</div>')

print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.cgi"><span class="glyphicon glyphicon-repeat"></span></a></li>')
print('<li class="active">Server Config</li>')
print('</ol>')

if form.getvalue('cpanelpkg') and form.getvalue('backend'):
    if form.getvalue('cpanelpkg') == 'default':
        pkgdomaindata = installation_path+'/conf/domain_data_default_local.yaml'
    else:
        pkgdomaindata = installation_path+'/conf/domain_data_default_local_'+form.getvalue('cpanelpkg')+'.yaml'
    mybackend = form.getvalue('backend')
    # Get data about the backends available
    if os.path.isfile(backend_config_file):
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    if os.path.isfile(pkgdomaindata):
        # Get all config settings from the domains domain-data config file
        with open(pkgdomaindata, 'r') as profileyaml_data_stream:
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
            if apptemplate_code in apptemplate_dict.keys():
                apptemplate_description = apptemplate_dict.get(apptemplate_code)
        else:
            print('<div class="alert alert-danger">ERROR: app template data file error</div>')
            sys.exit(0)
        # Ok we are done with getting the settings,now lets present it to the user
        print('<div class="alert alert-warning alert-domain"><strong>'+form.getvalue('cpanelpkg')+'</strong></div>')
        print('<div class="panel panel-default">')  # marker3
        print(('<div class="panel-heading"><h3 class="panel-title">cPanel Package</h3></div>'))
        print('<div class="panel-body">')  # marker4
        print('<form id="config" class="form-inline config-save" action="save_pkg_app_settings.cgi" method="post">')
        if backend_category == 'PROXY':
            print(('<div class="alert alert-success">Your current setup is: <br>Nginx proxying to <span class="label label-success">'+backend_version+'</span> with settings  <span class="label label-success">'+apptemplate_description+'</span></div>'))
        else:
            print(('<div class="alert alert-info alert-top">Your current project is <span class="label label-primary">'+apptemplate_description+'</span> on native <span class="label label-primary">NGINX</span> with <span class="label label-primary">'+backend_category+'</span> <span class="label label-primary">'+backend_version+'</span> application server</div>'))
        print(('<div class="alert alert-info alert-top">You selected <span class="label label-primary">'+mybackend+'</span> as the new backend, select the version and template for this backend below</div>'))
        backends_dict = backend_data_yaml_parsed.get(mybackend)
        new_apptemplate_dict = apptemplate_data_yaml_parsed.get(mybackend)
        if mybackend == backend_category:
            print('<div class="row">')  # marker5
            print('<div class="col-sm-6">')  # marker6
            print('<div class="panel panel-default">')  # marker7
            print('<div class="panel-heading"><h3 class="panel-title">Backend version</h3></div>')
            print('<div class="panel-body">')  # marker8
            print('<select name="backendversion">')
            for mybackend_version in backends_dict.keys():
                if mybackend_version == backend_version:
                    print(('<option selected value="'+mybackend_version+'">'+mybackend_version+'</option>'))
                else:
                    print(('<option value="'+mybackend_version+'">'+mybackend_version+'</option>'))
            print('</select>')
            print('</div>')  # marker8
            print('</div>')  # marker7
            print('</div>')  # marker6
            print('<div class="col-sm-6">')  # marker9
            print('<div class="panel panel-default">')
            print('<div class="panel-heading"><h3 class="panel-title">Application template</h3></div>')
            print('<div class="panel-body">')
            print('<select name="apptemplate">')
            for myapptemplate in sorted(new_apptemplate_dict.keys()):
                if myapptemplate == apptemplate_code:
                    print(('<option selected value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
                else:
                    print(('<option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
            print('</select>')
            print('</div>')
            print('</div>')
            print('</div>')  # marker9
            print('</div>')  # marker5
        else:
            print('<div class="row">')  # marker10
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
            for myapptemplate in sorted(new_apptemplate_dict.keys()):
                print(('<option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
            print('</select>')
            print('</div>')
            print('</div>')
            print('</div>')
            print('</div>')  # marker10
        # Pass on the domain name to the next stage
        print(('<input class="hidden" name="cpanelpkg" value="'+form.getvalue('cpanelpkg')+'">'))
        print(('<input class="hidden" name="backend" value="'+mybackend+'">'))
        print('<input class="btn btn-primary" type="submit" value="Submit">')
        print('</form>')
        print('</div>')  # marker4
        print('</div>')  # marker3
else:
        print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')

print('<div class="panel-footer"><small>')
print(branding_print_footer())
print('</small></div>')

print('</div>')  # marker3
print('</div>')  # marker2
print('</body>')
print('</html>')
