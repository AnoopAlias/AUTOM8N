#!/usr/bin/python

import os
import yaml
import cgi
import cgitb
import sys
import psutil
import platform
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

print_header('Subdirectory Upstream Configuration')
bcrumb('Subdirectory Upstream Configuration', 'fas fa-cogs')

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

                print('            <!-- cPanel Starter Row -->')
                print('            <div class="row justify-content-lg-center">')
                print('')
                print('                <!-- Column Start -->')
                print('                <div class="col-lg-6">')

                cardheader('New Upstream Configuration', 'fas fa-sliders-h')
                print('                        <div class="card-body text-center"> <!-- Card Body Start -->')
                print('                            <div class="alert alert-info text-center">')
                print('                                <p class="m-0 pb-1">You selected <span class="badge badge-warning">'+mybackend+'</span> as the new upstream type for:</p>')
                print('                                <kbd class="m-1">'+mydomain+'/'+thesubdir+'</kbd>')
                print('                                <p class="m-0 pt-1">Select the version and template for this upstream below.')
                print('                            </div>')
                print('                            <form class="form" method="post" id="toastForm8" onsubmit="return false;">')
                backends_dict = backend_data_yaml_parsed.get(mybackend)
                new_apptemplate_dict = apptemplate_data_yaml_parsed.get(mybackend)
                if os.path.isfile(user_app_template_file):
                    user_new_apptemplate_dict = user_apptemplate_data_yaml_parsed.get(mybackend)
                else:
                    user_new_apptemplate_dict = {}
                print('                                <div class="input-group">')
                print('                                    <div class="input-group-prepend input-group-prepend-min">')
                print('                                        <label class="input-group-text">Upstream</label>')
                print('                                    </div>')
                print('                                    <select name="backendversion" class="custom-select">')
                for mybackend_version in backends_dict.keys():
                    print('                                        <option value="'+mybackend_version+'">'+mybackend_version+'</option>')
                print('                                    </select>')
                print('                                </div>')

                print('                                <div class="input-group">')
                print('                                    <div class="input-group-prepend input-group-prepend-min">')
                print('                                        <label class="input-group-text">Template</label>')
                print('                                    </div>')
                print('                                    <select name="apptemplate" class="custom-select">')
                for myapptemplate in sorted(new_apptemplate_dict.keys()):
                    print('                                        <option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>')
                if user_new_apptemplate_dict:
                    for user_myapptemplate in sorted(user_new_apptemplate_dict.keys()):
                        print('                                        <option value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>')
                print('                                    </select>')
                print('                                </div>')

                # Pass on the domain name to the next stage
                print('                                <input hidden name="domain" value="'+mydomain+'">')
                print('                                <input hidden name="backend" value="'+mybackend+'">')
                print('                                <input hidden name="thesubdir" value="'+thesubdir+'">')
                print('                                <button class="btn btn-outline-primary btn-block" type="submit">Apply Upstream Configuration</button>')
                print('                            </form>')
                print('                        </div> <!-- Card Body End -->')
                cardfooter('')
            else:
                # We get the current app settings for the subdirectory
                the_subdir_dict = subdir_apps_dict.get(thesubdir)
                backend_category = the_subdir_dict.get('backend_category')
                backend_version = the_subdir_dict.get('backend_version')
                backend_path = the_subdir_dict.get('backend_path')
                apptemplate_code = the_subdir_dict.get('apptemplate_code')

                # Get the human friendly name of the app template
                apptemplate_dict = apptemplate_data_yaml_parsed.get(backend_category)
                apptemplate_description = apptemplate_dict.get(apptemplate_code)
                if apptemplate_code in apptemplate_dict.keys():
                    apptemplate_description = apptemplate_dict.get(apptemplate_code)
                else:
                    user_apptemplate_dict = user_apptemplate_data_yaml_parsed.get(backend_category)
                    if apptemplate_code in user_apptemplate_dict.keys():
                        apptemplate_description = user_apptemplate_dict.get(apptemplate_code)


                # Ok we are done with getting the settings,now lets present it to the user
                print('            <!-- cPanel Starter Row -->')
                print('            <div class="row justify-content-lg-center">')
                print('')

                print('                <!-- Column Start -->')
                print('                <div class="col-lg-8">')

                cardheader('Upstream Configuration Settings')
                print('                        <div class="card-body p-0">  <!-- Card Body Start -->')
                print('                            <div class="row no-gutters row-2-col"> <!-- Row Start -->')

                print('                                <div class="col-md-6 alert"><i class="fas fa-play"></i>&nbsp;Nginx</div>')
                print('                                <div class="col-md-6 alert text-success"><i class="fas fa-check"></i>&nbsp;Active</div>')

                # Backend
                print('                                <div class="col-md-6 alert"><i class="fas fa-server"></i>&nbsp;Current&nbsp;Upstream</div>')
                print('                                <div class="col-md-6 alert text-success">'+backend_version+'</div>')

                # Description
                print('                                <div class="col-md-6 alert"><i class="fas fa-cog"></i>&nbsp;Current Template</div>')
                print('                                <div class="col-md-6 alert text-success text-center">'+apptemplate_description+'</div>')

                # .htaccess
                if backend_category == 'PROXY' and backend_version == 'httpd':
                    print('                                <div class="col-md-6 alert"><i class="fas fa-file-code"></i>&nbsp;Current&nbsp;.htaccess&nbsp;Status</div>')
                    print('                                <div class="col-md-6 alert text-success"><i class="fas fa-check"></i>&nbsp;</div>')
                else:
                    print('                                <div class="col-md-6 alert"><i class="fas fa-file-code"></i>&nbsp;Current&nbsp;.htaccess&nbsp;Status</div>')
                    print('                                <div class="col-md-6 alert text-danger"><i class="fas fa-times"></i>&nbsp;Ignored</div>')

                # New Upstream
                print('                                <div class="col-md-6 alert"><i class="fas fa-server"></i>&nbsp;New&nbsp;Upstream&nbsp;Type</div>')
                print('                                <div class="col-md-6 alert text-warning text-center">'+mybackend+'</div>')

                print('                            </div> <!-- Row End -->')
                print('                        </div> <!-- Card Body End -->')

                print('                        <div class="card-body text-center"> <!-- Card Body Start -->')

                print('                            <div class="alert alert-info text-center">')
                print('                                <p class="m-0 pb-1">You selected <span class="badge badge-warning">'+mybackend+'</span> as the new upstream type for:</p>')
                print('                                <kbd class="m-1">'+mydomain+'/'+thesubdir+'</kbd>')
                print('                                <p class="m-0 pt-1">Select the version and template for this upstream below.')
                print('                            </div>')
                print('                            <form class="form" method="post" id="toastForm8" onsubmit="return false;">')
                backends_dict = backend_data_yaml_parsed.get(mybackend)
                new_apptemplate_dict = apptemplate_data_yaml_parsed.get(mybackend)
                if os.path.isfile(user_app_template_file):
                    user_new_apptemplate_dict = user_apptemplate_data_yaml_parsed.get(mybackend)
                else:
                    user_new_apptemplate_dict = {}
                if mybackend == backend_category:
                    print('                                <div class="input-group">')
                    print('                                    <div class="input-group-prepend input-group-prepend-min">')
                    print('                                        <label class="input-group-text">Upstream</label>')
                    print('                                    </div>')
                    print('                                    <select name="backendversion" class="custom-select">')
                    for mybackend_version in backends_dict.keys():
                        if mybackend_version == backend_version:
                            print('                                        <option selected value="'+mybackend_version+'">'+mybackend_version+'</option>')
                        else:
                            print('                                        <option value="'+mybackend_version+'">'+mybackend_version+'</option>')
                    print('                                    </select>')
                    print('                                </div>')

                    print('                                <div class="input-group">')
                    print('                                    <div class="input-group-prepend input-group-prepend-min">')
                    print('                                        <label class="input-group-text">Template</label>')
                    print('                                    </div>')
                    print('                                    <select name="apptemplate" class="custom-select">')
                    for myapptemplate in sorted(new_apptemplate_dict.keys()):
                        if myapptemplate == apptemplate_code:
                            print('                                        <option selected value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>')
                        else:
                            print('                                        <option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>')
                    if user_new_apptemplate_dict:
                        for user_myapptemplate in sorted(user_new_apptemplate_dict.keys()):
                            if user_myapptemplate == apptemplate_code:
                                print('                                        <option selected value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>')
                            else:
                                print('                                        <option value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>')
                    print('                                    </select>')
                    print('                                </div>')
                else:
                    print('                                <div class="input-group">')
                    print('                                    <div class="input-group-prepend input-group-prepend-min">')
                    print('                                        <label class="input-group-text">Upstream</label>')
                    print('                                    </div>')
                    print('                                    <select name="backendversion" class="custom-select">')
                    for mybackend_version in backends_dict.keys():
                        print('                                        <option selected value="'+mybackend_version+'">'+mybackend_version+'</option>')
                    print('                                    </select>')
                    print('                                </div>')

                    print('                                <div class="input-group">')
                    print('                                    <div class="input-group-prepend input-group-prepend-min">')
                    print('                                        <label class="input-group-text">Template</label>')
                    print('                                    </div>')
                    print('                                    <select name="apptemplate" class="custom-select">')
                    for myapptemplate in sorted(new_apptemplate_dict.keys()):
                        print('                                        <option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>')
                    if user_new_apptemplate_dict:
                        for user_myapptemplate in sorted(user_new_apptemplate_dict.keys()):
                            print('                                        <option value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>')
                    print('                                    </select>')
                    print('                                </div>')

                # Pass on the domain name to the next stage
                print('                                <input hidden name="domain" value="'+mydomain+'">')
                print('                                <input hidden name="backend" value="'+mybackend+'">')
                print('                                <input hidden name="thesubdir" value="'+thesubdir+'">')
                print('                                <button class="btn btn-outline-primary btn-block" type="submit">Apply Upstream Configuration</button>')
                print('                            </form>')
                print('                        </div> <!-- Card Body End -->')
                cardfooter('')

        else:

            # Ok we are done with getting the settings,now lets present it to the user
            print('            <!-- cPanel Starter Row -->')
            print('            <div class="row justify-content-lg-center">')
            print('')
            print('                <!-- Column Start -->')
            print('                <div class="col-lg-6">')

            cardheader('Initial Upstream Configuration', 'fas fa-user-cog')
            print('                        <div class="card-body text-center"> <!-- Card Body Start -->')
            print('                            <div class="alert alert-info text-center">')
            print('                                <p class="m-0 pb-1">You selected <span class="badge badge-warning">'+mybackend+'</span> as the new upstream type for:</p>')
            print('                                <kbd class="m-1">'+mydomain+'/'+thesubdir+'</kbd>')
            print('                                <p class="m-0 pt-1">Select the version and template for this upstream below.')
            print('                            </div>')

            print('                            <form class="form" id="toastForm8" onsubmit="return false;">')

            backends_dict = backend_data_yaml_parsed.get(mybackend)
            new_apptemplate_dict = apptemplate_data_yaml_parsed.get(mybackend)
            if os.path.isfile(user_app_template_file):
                user_new_apptemplate_dict = user_apptemplate_data_yaml_parsed.get(mybackend)
            else:
                user_new_apptemplate_dict = {}

            print('                                <div class="input-group">')
            print('                                    <div class="input-group-prepend input-group-prepend-min">')
            print('                                        <label class="input-group-text">Upstream</label>')
            print('                                    </div>')
            print('                                    <select name="backendversion" class="custom-select">')

            for mybackend_version in backends_dict.keys():
                print('                                        <option value="'+mybackend_version+'">'+mybackend_version+'</option>')

            print('                                    </select>')
            print('                                </div>')

            print('                                <div class="input-group">')
            print('                                    <div class="input-group-prepend input-group-prepend-min">')
            print('                                        <label class="input-group-text">Template</label>')
            print('                                    </div>')
            print('                                    <select name="apptemplate" class="custom-select">')

            for myapptemplate in sorted(new_apptemplate_dict.keys()):
                print('                                        <option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>')
            for user_myapptemplate in sorted(user_new_apptemplate_dict.keys()):
                print('                                        <option value="'+user_myapptemplate+'">'+user_new_apptemplate_dict.get(user_myapptemplate)+'</option>')

            print('                                    </select>')
            print('                                </div>')

            # Pass on the domain name to the next stage
            print('                                <input hidden name="domain" value="'+mydomain+'">')
            print('                                <input hidden name="backend" value="'+mybackend+'">')
            print('                                <input hidden name="thesubdir" value="'+thesubdir+'">')
            print('                                <button class="btn btn-outline-primary btn-block" type="submit">Apply Upstream Configuration</button>')
            print('                            </form>')
            print('                        </div> <!-- Card Body End -->')
            cardfooter('')
    else:
        print_nontoast_error('Error!', 'Domain Data File IO Error!')
        sys.exit(0)

else:
    print_nontoast_error('Forbidden!', 'Domain Data Missing!')
    sys.exit(0)


# Column End
print('                <!-- Column End -->')
print('                </div>')
print('')
print('            <!-- cPanel End Row -->')
print('            </div>')

print_footer()

print('        </div> <!-- Main Container End -->')
print('')

print_modals()
print_loader()

print('    <!-- Body End -->')
print('    </body>')
print('</html>')
