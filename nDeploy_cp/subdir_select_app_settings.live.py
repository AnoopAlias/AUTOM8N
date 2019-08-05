#!/usr/bin/python

import os
import yaml
import cgi
import cgitb
import sys
from commoninclude import close_cpanel_liveapisock, print_nontoast_error, print_disabled, bcrumb, return_sys_tip, return_prepend, return_label, print_header, print_footer, print_modals, print_loader, cardheader, cardfooter


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
close_cpanel_liveapisock()

form = cgi.FieldStorage()

print_header('Subdirectory Settings')
bcrumb('Subdirectory Settings', 'fas fa-cogs')

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
        commoninclude.print_error_wrapper('Error: app template data file error')
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
                print('			<form class="form" method="post" id="toastForm8" onsubmit="return false;">')
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
                print('				<button class="btn btn-outline-primary btn-block" type="submit">Update settings</button>')
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
                print('			<form class="form" method="post" id="toastForm8" onsubmit="return false;">')
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
            print('				<form class="form" id="toastForm8" onsubmit="return false;">')
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
            print('					<button class="btn btn-outline-primary btn-block " type="submit">Update Settings</button>')
            print('				</form>')
            print('			</div>')  # card-body end
            print('		</div>')  # card end
    else:
        commoninclude.print_error_wrapper('domain-data file i/o error')
else:
    commoninclude.print_forbidden_wrapper()

print('			</div>')  # end col
print('		</div>')  # row end

print('</div>')  # main-container end

print_modals()
print_loader()

print('</body>')
print('</html>')
