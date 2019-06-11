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
app_template_file = installation_path+"/conf/apptemplates_subdir.yaml"
cpaneluser = os.environ["USER"]
user_app_template_file = installation_path+"/conf/"+cpaneluser+"_apptemplates_subdir.yaml"
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
        brand_name = yaml_parsed_brand.get("brand", "AUTOM8N")
    else:
        brand_name = "AUTOM8N"
    return brand_name


def branding_print_support():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_support = yaml_parsed_brand.get("brand_support", '<div class="help float-right"><a class="btn btn-primary" target="_blank" href="https://autom8n.com"> docs <i class="fas fa-book-open"></i></a></div>')
    else:
        brand_support = '<div class="help float-right"><a class="btn btn-primary" target="_blank" href="https://autom8n.com"> docs <i class="fas fa-book-open"></i></a></div>'
    return brand_support


def print_forbidden():
    print(('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body"><i class="fas fa-exclamation"></i><p>Forbidden</p></div></div>'))


def print_error(themessage):
    print(('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body"><i class="fas fa-exclamation"></i><p>'+themessage+'</p></div></div>'))


close_cpanel_liveapisock()
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
print('				<li class="breadcrumb-item"><a href="xtendweb.live.py"><i class="fas fa-redo"></i></a></li>')
print('				<li class="breadcrumb-item active">Subdir Settings</li>')
print('			</ol>')
print('		</nav>')

print('		<div class="row justify-content-lg-center"">')

print('			<div class="col-lg-6">')

if form.getvalue('domain') and form.getvalue('backend') and form.getvalue('thesubdir'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    mybackend = form.getvalue('backend')
    thesubdir = form.getvalue('thesubdir')
    profileyaml = installation_path + "/domain-data/" + mydomain
    # Get data about the backends available
    if os.path.isfile(backend_config_file):
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    if os.path.isfile(app_template_file):
        with open(app_template_file, 'r') as apptemplate_data_yaml:
            apptemplate_data_yaml_parsed = yaml.safe_load(apptemplate_data_yaml)
        if os.path.isfile(user_app_template_file):
            with open(user_app_template_file, 'r') as user_apptemplate_data_yaml:
                user_apptemplate_data_yaml_parsed = yaml.safe_load(user_apptemplate_data_yaml)
    else:
        print_error('Error: app template data file error')
        sys.exit(0)
    if os.path.isfile(profileyaml):
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        subdir_apps_dict = yaml_parsed_profileyaml.get('subdir_apps')
        # If there are no entries in subdir_apps_dict or there is no specific config for the subdirectory
        # We do a fresh config
        if subdir_apps_dict:
            if not subdir_apps_dict.get(thesubdir):
                # Ok we are done with getting the settings,now lets present it to the user

                print('<div class="card">')  # card
                print('		<div class="card-header">')
                print('			<h5 class="card-title mb-0"><i class="fas fa-sliders-h float-right"></i> Upstream & Template</h5>')
                print('		</div>')
                print('		<div class="card-body text-center">')  # card-body
                print('			<form class="form" method="post" id="modalForm8" onsubmit="return false;">')
                print(('			<div class="alert alert-info">You selected <span class="label label-primary">'+mybackend+'</span> as the upstream, select the version and template for this upstream</div>'))
                backends_dict = backend_data_yaml_parsed.get(mybackend)
                new_apptemplate_dict = apptemplate_data_yaml_parsed.get(mybackend)
                if os.path.isfile(user_app_template_file):
                    user_new_apptemplate_dict = user_apptemplate_data_yaml_parsed.get(mybackend)
                else:
                    user_new_apptemplate_dict = {}
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
                print('						<label class="input-group-text">Template</label>')
                print('					</div>')
                print('					<select name="apptemplate" class="custom-select">')
                for myapptemplate in sorted(new_apptemplate_dict.keys()):
                    print(('				<option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
                if user_new_apptemplate_dict:
                    for user_myapptemplate in sorted(user_new_apptemplate_dict.keys()):
                        print(('			<option value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>'))
                print('					</select>')
                print('				</div>')

                # Pass on the domain name to the next stage
                print(('			<input class="hidden" name="domain" value="'+mydomain+'">'))
                print(('			<input class="hidden" name="backend" value="'+mybackend+'">'))
                print(('			<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
                print('				<button class="btn btn-outline-primary btn-block btn-ajax" type="submit">Update settings</button>')
                print('			</form>')
                print('		</div>')  # card-body end
                print('</div>')  # card end
            else:
                # we get the current app settings for the subdir
                the_subdir_dict = subdir_apps_dict.get(thesubdir)
                backend_category = the_subdir_dict.get('backend_category')
                backend_version = the_subdir_dict.get('backend_version')
                backend_path = the_subdir_dict.get('backend_path')
                apptemplate_code = the_subdir_dict.get('apptemplate_code')
                # get the human friendly name of the app template
                apptemplate_dict = apptemplate_data_yaml_parsed.get(backend_category)
                apptemplate_description = apptemplate_dict.get(apptemplate_code)
                if apptemplate_code in apptemplate_dict.keys():
                    apptemplate_description = apptemplate_dict.get(apptemplate_code)
                else:
                    user_apptemplate_dict = user_apptemplate_data_yaml_parsed.get(backend_category)
                    if apptemplate_code in user_apptemplate_dict.keys():
                        apptemplate_description = user_apptemplate_dict.get(apptemplate_code)

                # Ok we are done with getting the settings,now lets present it to the user
                print('<div class="card">')  # card
                print('		<div class="card-header">')
                print('			<h5 class="card-title mb-0"><i class="fas fa-user-cog float-right"></i> Upstream & Template</h5>')
                print('		</div>')
                print('		<div class="card-body text-center">')  # card-body
                print('			<form class="form" method="post" id="modalForm8" onsubmit="return false;">')
                if backend_category == 'PROXY':
                    print(('		<div class="alert alert-info">Your current setup is: Nginx proxying to <span class="label label-primary">'+backend_version+'</span> with settings  <span class="label label-primary">'+apptemplate_description+'</span></div>'))
                else:
                    print(('		<div class="alert alert-success">Your current project is <span class="label label-success">'+apptemplate_description+'</span> on native <span class="label label-success">NGINX</span> with <span class="label label-success">'+backend_category+'</span> <span class="label label-success">'+backend_version+'</span> upstream server</div>'))
                print(('			<div class="alert alert-info">You selected <span class="label label-primary">'+mybackend+'</span> as the new upstream, select the version and template for this upstream</div>'))
                backends_dict = backend_data_yaml_parsed.get(mybackend)
                new_apptemplate_dict = apptemplate_data_yaml_parsed.get(mybackend)
                if os.path.isfile(user_app_template_file):
                    user_new_apptemplate_dict = user_apptemplate_data_yaml_parsed.get(mybackend)
                else:
                    user_new_apptemplate_dict = {}
                if mybackend == backend_category:
                    print('			<div class="input-group">')
                    print('				<div class="input-group-prepend input-group-prepend-min">')
                    print('					<label class="input-group-text">Upstream</label>')
                    print('				</div>')
                    print('				<select name="backendversion" class="custom-select">')
                    for mybackend_version in backends_dict.keys():
                        if mybackend_version == backend_version:
                            print(('		<option selected value="'+mybackend_version+'">'+mybackend_version+'</option>'))
                        else:
                            print(('		<option value="'+mybackend_version+'">'+mybackend_version+'</option>'))
                    print('				</select>')
                    print('			</div>')

                    print('			<div class="input-group">')
                    print('				<div class="input-group-prepend input-group-prepend-min">')
                    print('					<label class="input-group-text">Template</label>')
                    print('				</div>')
                    print('				<select name="apptemplate" class="custom-select">')
                    for myapptemplate in sorted(new_apptemplate_dict.keys()):
                        if myapptemplate == apptemplate_code:
                            print(('		<option selected value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
                        else:
                            print(('		<option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
                    if user_new_apptemplate_dict:
                        for user_myapptemplate in sorted(user_new_apptemplate_dict.keys()):
                            if user_myapptemplate == apptemplate_code:
                                print(('	<option selected value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>'))
                            else:
                                print(('	<option value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>'))
                    print('				</select>')
                    print('			</div>')
                else:
                    print('			<div class="input-group">')
                    print('				<div class="input-group-prepend input-group-prepend-min">')
                    print('					<label class="input-group-text">Upstream</label>')
                    print('				</div>')
                    print('				<select name="backendversion" class="custom-select">')
                    for mybackend_version in backends_dict.keys():
                        print(('			<option selected value="'+mybackend_version+'">'+mybackend_version+'</option>'))
                    print('				</select>')
                    print('			</div>')

                    print('			<div class="input-group">')
                    print('				<div class="input-group-prepend input-group-prepend-min">')
                    print('					<label class="input-group-text">Template</label>')
                    print('				</div>')
                    print('				<select name="apptemplate" class="custom-select">')
                    for myapptemplate in sorted(new_apptemplate_dict.keys()):
                        print(('			<option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
                    if user_new_apptemplate_dict:
                        for user_myapptemplate in sorted(user_new_apptemplate_dict.keys()):
                            print(('		<option value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>'))
                    print('				</select>')
                    print('			</div>')

                # Pass on the domain name to the next stage
                print(('			<input class="hidden" name="domain" value="'+mydomain+'">'))
                print(('			<input class="hidden" name="backend" value="'+mybackend+'">'))
                print(('			<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
                print('				<button class="btn btn-outline-primary btn-block" type="submit">Update settings</button>')
                print('			</form>')
                print('		</div>')  # card-body end
                print('</div>')  # card end
        else:
            # Ok we are done with getting the settings,now lets present it to the user
            print('		<div class="card">')  # card
            print('			<div class="card-header">')
            print('				<h5 class="card-title mb-0"><i class="fas fa-user-cog float-right"></i> Upstream & Template</h5>')
            print('			</div>')
            print('			<div class="card-body text-center">')  # card-body
            print('				<form class="form" id="modalForm8" onsubmit="return false;">')
            print(('				<div class="alert alert-info">You selected <span class="label label-primary">'+mybackend+'</span> as the upstream, select the version and template for this upstream</div>'))
            backends_dict = backend_data_yaml_parsed.get(mybackend)
            new_apptemplate_dict = apptemplate_data_yaml_parsed.get(mybackend)
            if os.path.isfile(user_app_template_file):
                user_new_apptemplate_dict = user_apptemplate_data_yaml_parsed.get(mybackend)
            else:
                user_new_apptemplate_dict = {}
            print('					<div class="input-group">')
            print('						<div class="input-group-prepend input-group-prepend-min">')
            print('							<label class="input-group-text">Upstream</label>')
            print('						</div>')
            print('						<select name="backendversion" class="custom-select">')
            for mybackend_version in backends_dict.keys():
                print(('					<option value="'+mybackend_version+'">'+mybackend_version+'</option>'))
            print('						</select>')
            print('					</div>')

            print('					<div class="input-group">')
            print('						<div class="input-group-prepend input-group-prepend-min">')
            print('							<label class="input-group-text">Template</label>')
            print('						</div>')
            print('						<select name="apptemplate" class="custom-select">')
            for myapptemplate in sorted(new_apptemplate_dict.keys()):
                print(('					<option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>'))
            for user_myapptemplate in sorted(user_new_apptemplate_dict.keys()):
                print(('					<option value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>'))
            print('						</select>')
            print('					</div>')

            # Pass on the domain name to the next stage
            print(('				<input class="hidden" name="domain" value="'+mydomain+'">'))
            print(('				<input class="hidden" name="backend" value="'+mybackend+'">'))
            print(('				<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
            print('					<button class="btn btn-outline-primary btn-block btn-ajax" type="submit">Update settings</button>')
            print('				</form>')
            print('			</div>')  # card-body end
            print('		</div>')  # card end
    else:
        print_error('domain-data file i/o error')
else:
    print_forbidden()

print('		</div>')  # row end

print('</div>')  # main-container end

# Modal
print('		<div class="modal fade" id="myModal" tabindex="-1" role="dialog">')
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

# Modal with no reload
print('		<div class="modal fade" id="myModal-nl" tabindex="-1" role="dialog">')
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

# Modal Large Width
print('		<div class="modal fade" id="myModal-xl" tabindex="-1" role="dialog">')
print('    		<div class="modal-dialog modal-xl modal-dialog-centered" role="document">')
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
