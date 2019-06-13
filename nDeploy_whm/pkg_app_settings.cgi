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
        brand_name = yaml_parsed_brand.get("brand", "AUTOM8N")
    else:
        brand_name = "AUTOM8N"
    return brand_name


def branding_print_support():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_support = yaml_parsed_brand.get("brand_support", '<div class="help float-right"><a class="btn btn-primary" target="_blank" href="help.txt"> docs <i class="fas fa-book-open"></i></a></div>')
    else:
        brand_support = '<div class="help float-right"><a class="btn btn-primary" target="_blank" href="help.txt"> docs <i class="fas fa-book-open"></i></a></div>'
    return brand_support


def print_forbidden():
    print(('<i class="fas fa-exclamation"></i><p>Forbidden</p>'))


def print_error(themessage):
    print(('<i class="fas fa-exclamation"></i><p>'+themessage+'</p>'))


cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')

print('<title>')
print(branding_print_banner())
print('</title>')

print(('<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>'))
print(('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>'))
print(('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">'))
print(('<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>'))
print(('<link href="https://fonts.googleapis.com/css?family=Poppins&display=swap" rel="stylesheet">'))
print(('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.1/css/all.min.css" rel="stylesheet">'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')

print('<body>')

print('<header id="main-header">')

print(branding_print_support())
print('		<div class="logo">')
print('			<h4>')
print('				<a href="xtendweb.cgi"><img border="0" src="')
print(					branding_print_logo_name())
print('					" width="48" height="48"></a>')
print(					branding_print_banner())
print('			</h4>')
print('		</div>')

print('</header>')

print('<div id="main-container" class="container">')  # main container

print('		<nav aria-label="breadcrumb">')
print('			<ol class="breadcrumb">')
print('				<li class="breadcrumb-item"><a href="xtendweb.cgi"><i class="fas fa-redo"></i></a></li>')
print('				<li class="breadcrumb-item active">Upstream Settings</li>')
print('			</ol>')
print('		</nav>')

print('		<div class="row justify-content-lg-center">')
print('			<div class="col-lg-6">')

print('				<div class="card">')  # card
print('					<div class="card-header">')
print('						<h5 class="card-title mb-0"><i class="fas fa-box-open float-right"></i> "'+form.getvalue('cpanelpkg')+'" cPanel Package</h5>')
print('					</div>')
print('					<div class="card-body">')  # card-body

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
            print_error('ERROR: app template data file error')
            sys.exit(0)

        # Ok we are done with getting the settings,now lets present it to the user
        print('				<form class="form" method="post" id="modalForm18" onsubmit="return false;">')
        if backend_category == 'PROXY':
            print(('			<div class="alert alert-success">Your current setup is: <br>Nginx proxying to <span class="label label-success">'+backend_version+'</span> with template <span class="label label-success">'+apptemplate_description+'</span></div>'))
        else:
            print(('			<div class="alert alert-info">Your current project is <span class="label label-primary">'+apptemplate_description+'</span> on native <span class="label label-primary">NGINX</span> with <span class="label label-primary">'+backend_category+'</span> <span class="label label-primary">'+backend_version+'</span> upstream server</div>'))
        print(('				<div class="alert alert-info">You selected <span class="label label-primary">'+mybackend+'</span> as the new upstream, select the version and template for this upstream below</div>'))
        backends_dict = backend_data_yaml_parsed.get(mybackend)
        new_apptemplate_dict = apptemplate_data_yaml_parsed.get(mybackend)
        if mybackend == backend_category:
            print('				<div class="input-group">')
            print('					<div class="input-group-prepend input-group-prepend-min">')
            print('						<label class="input-group-text">Upstream</label>')
            print('					</div>')
            print('					<select name="backendversion" class="custom-select">')
            for mybackend_version in backends_dict.keys():
                if mybackend_version == backend_version:
                    print(('			<option selected value="'+mybackend_version+'">'+mybackend_version+'</option>'))
                else:
                    print(('			<option value="'+mybackend_version+'">'+mybackend_version+'</option>'))
            print('					</select>')
            print('				</div>')

            print('				<div class="input-group">')
            print('					<div class="input-group-prepend input-group-prepend-min">')
            print('						<label class="input-group-text">Config template</label>')
            print('					</div>')
            print('					<select name="apptemplate" class="custom-select">')
            for myapptemplate in sorted(new_apptemplate_dict.keys()):
                if myapptemplate == apptemplate_code:
                    print(('			<option selected value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
                else:
                    print(('			<option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
            print('					</select>')
            print('				</div>')
        else:
            print('				<div class="input-group">')
            print('					<div class="input-group-prepend input-group-prepend-min">')
            print('						<label class="input-group-text">Upstream</label>')
            print('					</div>')
            print('					<select name="backendversion" class="custom-select">')
            for mybackend_version in backends_dict.keys():
                print(('				<option value="'+mybackend_version+'">'+mybackend_version+'</option>'))
            print('					</select>')
            print('				</div>')
            print('				<div class="input-group">')
            print('					<div class="input-group-prepend input-group-prepend-min">')
            print('						<label class="input-group-text">Config template</label>')
            print('					</div>')
            print('					<select name="apptemplate" class="custom-select">')
            for myapptemplate in sorted(new_apptemplate_dict.keys()):
                print(('				<option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
            print('					</select>')
            print('				</div>')

        # Pass on the domain name to the next stage
        print(('				<input class="hidden" name="cpanelpkg" value="'+form.getvalue('cpanelpkg')+'">'))
        print(('				<input class="hidden" name="backend" value="'+mybackend+'">'))
        print('					<button class="btn btn-outline-primary btn-block" type="submit">Update Package</button>')
        print('				</form>')
else:
    print_forbidden()

print('					</div>')  # card-body end
print('				</div>')  # card end

print('			</div>')  # col end
print('		</div>')  # row end

print('</div>')  # main-container end

# Modal
print('		<div class="modal fade" id="myModal" tabindex="-1" role="dialog"> ')
print('    		<div class="modal-dialog modal-dialog-centered" role="document">')
print('      		<div class="modal-content">')
print('        			<div class="modal-header">')
print('          			<h4 class="modal-title">Command Output</h4>')
print('						<button type="button" class="close" data-dismiss="modal" aria-label="Close">')
print('          				<span aria-hidden="true">&times;</span>')
print('        				</button>')
print('        			</div>')
print('        			<div class="modal-body">')
print('        			</div>')
print('					<div class="modal-footer">')
print('        				<button type="button" class="btn btn-outline-secondary" data-dismiss="modal">Close</button>')
print('      			</div>')
print('      		</div>')
print('    		</div>')
print('     </div>')

print('</body>')
print('</html>')
