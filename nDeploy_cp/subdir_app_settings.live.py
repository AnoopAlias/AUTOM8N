#!/usr/bin/env python3

import os
import yaml
import cgi
import cgitb
import sys
import re
from hashlib import md5
try:
    import simplejson as json
except ImportError:
    import json
from commoninclude import close_cpanel_liveapisock, print_nontoast_error, print_disabled, bcrumb, return_sys_tip, return_prepend, return_label, print_header, print_footer, cardheader, cardfooter


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

print_header('Subdirectory Configuration')
bcrumb('Subdirectory Configuration', 'fas fa-cogs')

if form.getvalue('domain') and form.getvalue('thesubdir'):

    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    if mydomain.startswith('_wildcard_.'):
        cpmydomain = '*.'+mydomain.replace('_wildcard_.', '')
    else:
        cpmydomain = mydomain
    cpaneluser = os.environ["USER"]
    cpdomainjson = "/var/cpanel/userdata/" + cpaneluser + "/" + cpmydomain + ".cache"
    with open(cpdomainjson, 'r') as cpaneldomain_data_stream:
        json_parsed_cpaneldomain = json.load(cpaneldomain_data_stream)
    document_root = json_parsed_cpaneldomain.get('documentroot')
    thesubdir = form.getvalue('thesubdir')
    if thesubdir.startswith('/'):
        thesubdir = thesubdir[1:]
    if thesubdir.endswith('/'):
        thesubdir = thesubdir[:-1]
    if not thesubdir:
        print_nontoast_error('Error!', 'Invalid subdirectory name!')
        sys.exit(0)
    if not re.match("^[\.0-9a-zA-Z/_-]*$", thesubdir):
        print_nontoast_error('Error!', 'Invalid character in subdirectory name!')
        sys.exit(0)
    profileyaml = installation_path + "/domain-data/" + mydomain

    # Get data about the backends available
    if os.path.isfile(backend_config_file):
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    if os.path.isfile(profileyaml):

        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        subdir_apps_dict = yaml_parsed_profileyaml.get('subdir_apps')
        user_config = yaml_parsed_profileyaml.get('user_config', 'disabled')

        # If there are no entries in subdir_apps_dict or there is no specific config for the subdirectory
        # We do a fresh config
        if subdir_apps_dict:
            if not subdir_apps_dict.get(thesubdir):
                print('            <!-- cPanel Starter Row -->')
                print('            <div class="row justify-content-lg-center">')
                print('')
                print('                <!-- Column Start -->')
                print('                <div class="col-lg-6">')

                cardheader('New Subdirectory Upstream Configuration')
                print('                        <div class="card-body"> <!-- Card Body Start -->')
                print('                            <form class="form mb-0" action="subdir_select_app_settings.live.py" method="get">')
                print('                                <div class="alert alert-info text-center">')
                print('                                    <p class="m-0 pb-1">Select upstream type for:</p>')
                print(('                                    <kbd class="m-1">'+mydomain+'/'+thesubdir+'</kbd>'))
                print('                                </div>')
                print('                                <div class="input-group mb-3">')
                print('                                    <div class="input-group-prepend input-group-prepend-min">')
                print('                                        <label class="input-group-text">Upstream</label>')
                print('                                    </div>')
                print('                                    <select name="backend" class="custom-select">')
                for backends_defined in list(backend_data_yaml_parsed.keys()):
                    print(('                                        <option value="'+backends_defined+'">'+backends_defined+'</option>'))
                print('                                    </select>')
                print('                                </div>')

                # Pass on the domain name to the next stage
                print(('                                <input hidden name="domain" value="'+mydomain+'">'))
                print(('                                <input hidden name="thesubdir" value="'+thesubdir+'">'))
                print('                                <button class="btn btn-outline-primary btn-block" type="submit">Confirm Upstream</button>')
                print('                            </form>')
                print('                        </div> <!-- Card Body End -->')
                cardfooter('Select the upstream category to use with this application.')

            else:

                # We get the current app settings for the subdir
                the_subdir_dict = subdir_apps_dict.get(thesubdir)
                backend_category = the_subdir_dict.get('backend_category')
                backend_version = the_subdir_dict.get('backend_version')
                backend_path = the_subdir_dict.get('backend_path')
                apptemplate_code = the_subdir_dict.get('apptemplate_code')
                proxy_to_master = the_subdir_dict.get('proxy_to_master', 'disabled')
                mod_security = the_subdir_dict.get('mod_security', 'disabled')
                auth_basic = the_subdir_dict.get('auth_basic', 'disabled')
                set_expire_static = the_subdir_dict.get('set_expire_static', 'disabled')
                redirectstatus = the_subdir_dict.get('redirectstatus', 'none')
                append_requesturi = the_subdir_dict.get('append_requesturi', 'disabled')
                redirecturl = the_subdir_dict.get('redirecturl', 'none')
                uniq_path = document_root+thesubdir
                uniq_filename = md5(uniq_path.encode("utf-8")).hexdigest()

                # Get the human friendly name of the app template
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
                    if apptemplate_code in list(apptemplate_dict.keys()):
                        apptemplate_description = apptemplate_dict.get(apptemplate_code)
                    else:
                        if apptemplate_code in list(user_apptemplate_dict.keys()):
                            apptemplate_description = user_apptemplate_dict.get(apptemplate_code)
                else:
                    print_nontoast_error('Error!', 'Application Template Data File Error!')
                    sys.exit(0)

                print('            <!-- cPanel Start Dash Row -->')
                print('            <div class="row justify-content-lg-center">')
                print('')
                print('                <!-- Dash Start -->')
                print('                <div class="col-lg-12">')

                # Domain Status
                cardheader('Current Application Settings: <kbd class="p-1">'+mydomain+'/'+thesubdir+'</kbd>','far fa-lightbulb')
                cardfooter('')

                print('                </div> <!-- Dash End -->')
                print('')
                print('            </div> <!-- cPanel End Dash Row -->')

                print('            <!-- Dash Widgets Start -->')
                print('            <div id="dashboard" class="row flex-row">')
                print('')

                # Nginx Status
                print('                <div class="col-sm-6 col-xl-4"> <!-- Dash Item Start -->')
                cardheader('')
                print('                    <div class="card-body text-center"> <!-- Card Body Start -->')
                print('                        <h4 class="mb-0"><i class="fas fa-play"></i> Running</h4>')
                print('                        <ul class="list-unstyled mb-0">')
                print('                            <li class="mt-2 text-success">Nginx</li>')
                print('                        </ul>')
                print('                    </div> <!-- Card Body End -->')
                cardfooter('')
                print('                </div> <!-- Dash Item End -->')

                # Backend Status
                print('                <div class="col-sm-6 col-xl-4"> <!-- Dash Item Start -->')
                cardheader('')
                print('                    <div class="card-body text-center"> <!-- Card Body Start -->')
                print('                        <h4 class="mb-0"><i class="fa fa-server"></i> Upstream</h4>')
                print('                        <ul class="list-unstyled mb-0">')
                print(('                            <li class="mt-2 text-success">'+backend_version+'</li>'))
                print('                        </ul>')
                print('                    </div> <!-- Card Body End -->')
                cardfooter('')
                print('                </div> <!-- Dash Item End -->')

                # Tamplate Status
                print('                <div class="col-sm-6 col-xl-4"> <!-- Dash Item Start -->')
                cardheader('')
                print('                    <div class="card-body text-center"> <!-- Card Body Start -->')
                print('                        <h4 class="mb-0"><i class="fas fa-cog"></i> Configuration</h4>')
                print('                        <ul class="list-unstyled mb-0">')
                print(('                            <li class="mt-2 text-success">'+apptemplate_description+'</li>'))
                print('                        </ul>')
                print('                    </div> <!-- Card Body End -->')
                cardfooter('')
                print('                </div> <!-- Dash Item End -->')

                print('')
                print('            </div> <!-- Dash Widgets End -->')
                print('')

                # Ok we are done with getting the settings,now lets present it to the user
                print('            <!-- CP Tabs Row -->')
                print('            <div class="row justify-content-lg-center flex-nowrap">')
                print('')
                print('                <!-- Secondary Navigation -->')
                print('                <div class="pl-3 col-md-3 nav flex-column nav-pills d-none d-lg-block d-xl-block d-xs-none d-sm-none" id="v-pills-tab" role="tablist" aria-orientation="vertical">')
                print('                    <a class="nav-link active" id="v-pills-system-tab" data-toggle="pill" href="#v-pills-system" role="tab" aria-controls="v-pills-system-tab">Application Status</a>')
                print('                    <a class="nav-link mb-4" id="v-pills-general-tab" data-toggle="pill" href="#v-pills-general" role="tab" aria-controls="v-pills-general">General Settings</a>')

                # Save Settings
                print(('                    <input hidden name="domain" value="'+mydomain+'" form="save_subdirectory_app_settings">'))
                print(('                    <input hidden name="thesubdir" value="'+thesubdir+'" form="save_subdirectory_app_settings">'))
                print('                    <button id="save-subdirectory-app-settings-btn" class="btn btn-primary btn-block" type="submit" form="save_subdirectory_app_settings">Apply Settings</button>')
                print('                </div>')

                print('')
                print('                <!-- Container Tab -->')
                print('                <div class="tab-content col-md-12 col-lg-9" id="v-pills-tabContent">')
                print('')

                print('                    <!-- Secondary Mobile Navigation -->')
                print('                    <div class="d-lg-none d-xl-none dropdown nav">')
                print('                        <button class="btn btn-primary btn-block dropdown-toggle mb-3" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">')
                print('                            Menu')
                print('                        </button>')
                print('                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">')
                print('                            <a class="dropdown-item" id="v-pills-system-tab" data-toggle="pill" href="#v-pills-system" role="tab" aria-controls="v-pills-system-tab" aria-selected="false">Application Status</a>')
                print('                            <a class="dropdown-item" id="v-pills-general-tab" data-toggle="pill" href="#v-pills-general" role="tab" aria-controls="v-pills-general" aria-selected="false">General Settings</a>')
                print('                        </div>')

                # Save Settings
                print('                    <button id="save-subdirectory-app-settings-btn" class="btn btn-primary btn-block" type="submit" form="save_subdirectory_app_settings">Apply Settings</button>')
                print('                    </div>')

                # System Tab
                print('')
                print('                    <!-- System Tab -->')
                print('                    <div class="tab-pane fade show active" id="v-pills-system" role="tabpanel" aria-labelledby="v-pills-system-tab">')

                cardheader('Application Status', 'fas fa-users-cog')
                print('                        <div class="card-body p-0"> <!-- Card Body Start -->')
                print('                            <div class="row no-gutters row-2-col"> <!-- Row Start -->')

                # .htaccess
                if backend_category == 'PROXY':
                    if backend_version == 'httpd':
                        print('                        <div class="col-md-6 alert"><i class="fas fa-file-code"></i> .htaccess</div>')
                        print('                        <div class="col-md-6 alert text-success"><i class="fas fa-check-circle"></i></div>')
                else:
                    print('                            <div class="col-md-6 alert"><i class="fas fa-file-code"></i> .htaccess</div>')
                    print('                            <div class="col-md-6 alert text-danger"><i class="fas fa-times-circle"></i></div>')

                # User config reload
                nginx_log_hint = document_root+"/"+thesubdir+"/nginx.conf"
                print(('                                '+return_sys_tip('<i class="fas fa-user-cog"></i> nginx.conf', nginx_log_hint)))
                if os.path.isfile(nginx_log_hint):
                    if os.path.isfile("/etc/nginx/sites-enabled/"+mydomain+"_"+uniq_filename+".manualconfig_user"):
                        print('                        <div class="col-md-6 alert text-success"><i class="fas fa-check-circle"></i></div>')
                    else:
                        print('                        <div class="col-md-6 alert text-danger"><i class="fas fa-times-circle"></i> Invalid/Require Reload</div>')
                else:
                    print('                            <div class="col-md-6 alert text-center"><i class="fas fa-file-upload"></i> Not Present</div>')

                # Reload Nginx
                print('                                <div class="col-md-6 alert"><i class="fas fa-sync-alt"></i>nginx.conf reload</div>')
                print('                                <div class="col-md-6">')
                print('                                    <form class="form" method="post" id="reload_nginx" onsubmit="return false;">')
                print(('                                        <input hidden name="domain" value="'+mydomain+'">'))
                print('                                        <button id="reload-nginx-btn" class="btn btn-block text-center" type="submit">Reload</button>')
                print('                                    </form>')
                print('                                </div>')

                # Nginx Log
                print('                                <div class="col-md-6 alert"><i class="fas fa-clipboard-list"></i>nginx.conf reload log</div>')
                print('                                <div class="col-md-6">')
                print('                                    <form class="form" method="post" id="view_nginx_log" onsubmit="return false;">')
                print(('                                        <input hidden name="domain" value="'+mydomain+'">'))
                print('                                        <button id="view-nginx-log-btn" class="btn btn-block text-center" type="submit">View Log</button>')
                print('                                    </form>')
                print('                                </div>')
                print('                            </div> <!-- Row End -->')
                print('                        </div> <!-- Card Body End -->')

                if backend_category == 'RUBY' or backend_category == 'PYTHON' or backend_category == 'NODEJS' or backend_category == 'PHP':
                    print('                        <div class="card-body pt-3 pb-0">  <!-- Card Body Start -->')
                    print('                            <form class="form" id="dependency_installer" onsubmit="return false;">')

                    if backend_category == "RUBY":
                        dep_file = document_root+'/'+thesubdir+'/Gemfile'
                    elif backend_category == "NODEJS":
                        dep_file = document_root+'/'+thesubdir+'/package.json'
                    elif backend_category == 'PYTHON':
                        dep_file = document_root+'/'+thesubdir+'/requirements.txt'
                    elif backend_category == 'PHP':
                        dep_file = document_root+'/'+thesubdir+'/composer.json'
                    print(('                                <input hidden name="domain" value="'+mydomain+'/'+thesubdir+'">'))
                    print(('                                <input hidden name="document_root" value="'+document_root+'/'+thesubdir+'">'))
                    print(('                                <input hidden name="backend_category" value="'+backend_category+'">'))
                    print(('                                <input hidden name="backend_version" value="'+backend_version+'">'))
                    print('                            </form>')

                    print('                            <div class="btn-group btn-block mt-1">')
                    print(('                                <button id="dependency-installer-btn" class="btn btn-outline-warning btn-block" data-toggle="tooltip" data-placement="top" title="'+dep_file+'" type="submit" form="dependency_installer">Install '+backend_category+' Project Deps</button>'))

                    if backend_category == 'PHP':
                        print('                            <form class="form" id="view_php_log" onsubmit="return false;">')
                        print('                            </form>')
                        print('                            <button id="view-php-log-btn" class="btn btn-outline-warning btn-block" type="submit" form="view_php_log">View PHP Log</button>')

                    print('                            </div>')
                    print('                        </div> <!-- Card Body End -->')

                print('                        <div class="card-body mb-0">  <!-- Card Body Start -->')

                print('                            <form class="form mb-0" action="subdir_select_app_settings.live.py" method="get">')
                print('                                <div class="input-group mb-0">')
                print('                                    <select name="backend" class="custom-select">')
                for backends_defined in list(backend_data_yaml_parsed.keys()):
                    if backends_defined == backend_category:
                        print(('                                        <option selected value="'+backends_defined+'">'+backends_defined+'</option>'))
                    else:
                        print(('                                        <option value="'+backends_defined+'">'+backends_defined+'</option>'))
                print('                                    </select>')

                # Pass on the domain name to the next stage
                print('                                    <div class="input-group-append">')
                print(('                                        <input hidden name="domain" value="'+mydomain+'">'))
                print(('                                        <input hidden name="thesubdir" value="'+thesubdir+'">'))
                print('                                        <button class="btn btn-outline-primary" type="submit">Select</button>')
                print('                                    </div>')
                print('                                </div>')
                print('                            </form>')
                print('                        </div> <!-- Card Body End -->')
                cardfooter('Select the upstream category to use with this application.')
                print('                    </div><!-- System Tab End -->')

                # General Tab
                print('')
                print('                    <!-- General Tab -->')
                print('                    <div class="tab-pane fade show" id="v-pills-general" role="tabpanel" aria-labelledby="v-pills-general-tab">')

                cardheader('General Settings', 'fas fa-sliders-h')
                print('                        <div class="card-body"> <!-- Card Body Start -->')
                print('                            <form class="form" id="save_subdirectory_app_settings" onsubmit="return false;">')
                print('                                <div class="row row-btn-group-toggle">')

                # auth_basic
                auth_basic_hint = " Setup password for "+document_root+"/"+thesubdir+" in cPanel -> Files -> Directory Privacy. "
                print(('                                    '+return_label("Password Protect Application", auth_basic_hint)))
                print('                                    <div class="col-md-6">')
                print('                                        <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')

                if auth_basic == 'enabled':
                    print('                                            <label class="btn btn-light active">')
                    print('                                                <input type="radio" name="auth_basic" value="enabled" id="AuthBasicOn" autocomplete="off" checked> Enabled')
                    print('                                            </label>')
                    print('                                            <label class="btn btn-light">')
                    print('                                                <input type="radio" name="auth_basic" value="disabled" id="AuthBasicOff" autocomplete="off"> Disabled')
                else:
                    print('                                            <label class="btn btn-light">')
                    print('                                                <input type="radio" name="auth_basic" value="enabled" id="AuthBasicOn" autocomplete="off"> Enabled')
                    print('                                            </label>')
                    print('                                            <label class="btn btn-light active">')
                    print('                                                <input type="radio" name="auth_basic" value="disabled" id="AuthBasicOff" autocomplete="off" checked> Disabled')

                print('                                            </label>')
                print('                                        </div>')
                print('                                    </div>')

                # proxy_to_master
                proxy_to_master_hint = " When running in a cluster, PROXY to MASTER instead of local server. "
                print(('                                '+return_label("Proxy to Master", proxy_to_master_hint)))
                print('                                <div class="col-md-6">')
                print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

                if proxy_to_master == 'enabled':
                    print('                                        <label class="btn btn-light active">')
                    print('                                            <input type="radio" name="proxy_to_master" value="enabled" id="ProxyToMasterOn" autocomplete="off" checked> Enabled')
                    print('                                        </label>')
                    print('                                        <label class="btn btn-light">')
                    print('                                            <input type="radio" name="proxy_to_master" value="disabled" id="ProxyToMasterOff" autocomplete="off"> Disabled')
                else:
                    print('                                        <label class="btn btn-light">')
                    print('                                            <input type="radio" name="proxy_to_master" value="enabled" id="ProxyToMasterOn" autocomplete="off"> Enabled')
                    print('                                        </label>')
                    print('                                        <label class="btn btn-light active">')
                    print('                                            <input type="radio" name="proxy_to_master" value="disabled" id="ProxyToMasterOff" autocomplete="off" checked> Disabled')

                print('                                        </label>')
                print('                                    </div>')
                print('                                </div>')

                # set_expire_static
                set_expire_static_hint = " Set Expires/Cache-Control headers for STATIC content. "
                print(('                                    '+return_label("Expires / Cache-Control", set_expire_static_hint)))
                print('                                    <div class="col-md-6">')
                print('                                        <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

                if set_expire_static == 'enabled':
                    print('                                            <label class="btn btn-light active">')
                    print('                                                <input type="radio" name="set_expire_static" value="enabled" id="SetExpireStaticOn" autocomplete="off" checked> Enabled')
                    print('                                            </label>')
                    print('                                            <label class="btn btn-light">')
                    print('                                                <input type="radio" name="set_expire_static" value="disabled" id="SetExpireStaticOff" autocomplete="off"> Disabled')
                else:
                    print('                                            <label class="btn btn-light">')
                    print('                                                <input type="radio" name="set_expire_static" value="enabled" id="SetExpireStaticOn" autocomplete="off"> Enabled')
                    print('                                            </label>')
                    print('                                            <label class="btn btn-light active">')
                    print('                                                <input type="radio" name="set_expire_static" value="disabled" id="SetExpireStaticOff" autocomplete="off" checked> Disabled')

                print('                                            </label>')
                print('                                        </div>')
                print('                                    </div>')

                # mod_security
                # mod_security_hint = " Mod Security v3 Web Application Firewall "
                # print(('                                    '+return_label("Mod Security", mod_security_hint)))
                #
                # if os.path.isfile('/etc/nginx/modules.d/zz_modsecurity.load'):
                #     print('                                    <div class="col-md-6">')
                #     print('                                        <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                #
                #     if mod_security == 'enabled':
                #         print('                                            <label class="btn btn-light active">')
                #         print('                                                <input type="radio" name="mod_security" value="enabled" id="ModSecurityOn" autocomplete="off" checked> Enabled')
                #         print('                                            </label>')
                #         print('                                            <label class="btn btn-light">')
                #         print('                                                <input type="radio" name="mod_security" value="disabled" id="ModSecurityOff" autocomplete="off"> Disabled')
                #     else:
                #         print('                                            <label class="btn btn-light">')
                #         print('                                                <input type="radio" name="mod_security" value="enabled" id="ModSecurityOn" autocomplete="off"> Enabled')
                #         print('                                            </label>')
                #         print('                                            <label class="btn btn-light active">')
                #         print('                                                <input type="radio" name="mod_security" value="disabled" id="ModSecurityOff" autocomplete="off" checked> Disabled')
                #
                #     print('                                            </label>')
                #     print('                                        </div>')
                #     print('                                    </div>')
                #
                # else:
                #     print_disabled()
                #     print(('                                <input hidden name="mod_security" value="'+mod_security+'">'))

                # URL Redirect
                url_redirect_hint = " Select URL redirection type. "
                print(('                                '+return_label("URL Redirect", url_redirect_hint)))
                print('                                <div class="col-md-6">')
                print('                                    <div class="input-group btn-group">')
                print('                                        <select name="redirectstatus" class="custom-select">')

                if redirectstatus == 'none':
                    print('                                            <option selected value="none">No Redirection</option>')
                    print('                                            <option value="301">Permanent (301)</option>')
                    print('                                            <option value="307">Temporary (307)</option>')
                elif redirectstatus == '301':
                    print('                                            <option value="none">No Redirection</option>')
                    print('                                            <option value="307">Temporary (307)</option>')
                    print('                                            <option selected value="301">Permanent (301)</option>')
                elif redirectstatus == '307':
                    print('                                            <option value="none">No Redirection</option>')
                    print('                                            <option selected value="307">Temporary (307)</option>')
                    print('                                            <option value="301">Permanent (301)</option>')

                print('                                        </select>')
                print('                                    </div>')
                print('                                </div>')

                # Append request_uri to redirect
                append_requesturi_hint = " Maintain the original Request URI ($request_uri (with arguments)). "
                print(('                                '+return_label("Append Redirect URL", append_requesturi_hint)))
                print('                                <div class="col-md-6">')
                print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

                if append_requesturi == 'enabled' and redirectstatus != 'none':
                    print('                                        <label class="btn btn-light active">')
                    print('                                            <input type="radio" name="append_requesturi" value="enabled" id="AppendRequesturiOn" autocomplete="off" checked> Enabled')
                    print('                                        </label>')
                    print('                                        <label class="btn btn-light">')
                    print('                                           <input type="radio" name="append_requesturi" value="disabled" id="AppendRequesturiOff" autocomplete="off"> Disabled')
                else:
                    print('                                        <label class="btn btn-light">')
                    print('                                            <input type="radio" name="append_requesturi" value="enabled" id="AppendRequesturiOn" autocomplete="off"> Enabled')
                    print('                                        </label>')
                    print('                                        <label class="btn btn-light active">')
                    print('                                            <input type="radio" name="append_requesturi" value="disabled" id="AppendRequesturiOff" autocomplete="off" checked> Disabled')

                print('                                        </label>')
                print('                                    </div>')
                print('                                </div>')

                # Redirect URL
                redirecturl_hint = " A Valid URL, Eg: https://mynewurl.tld "

                print('                                <div class="col-md-12">')
                print('                                    <div class="input-group btn-group mb-0">')
                print('                                        <div class="input-group-prepend">')
                print('                                            <span class="input-group-text">')
                print(('                                                '+return_prepend("Redirect to URL", redirecturl_hint)))
                print('                                            </span>')
                print('                                        </div>')
                print(('                                        <input class="form-control" value='+redirecturl+' type="text" name="redirecturl">'))
                print('                                        </form>')
                print('                                    </div>')
                print('                                </div>')

                print('                            </div> <!-- Row End -->')
                print('                        </div> <!-- Card Body End -->')
                cardfooter('')

                print('                    </div><!-- General Tab End -->')
                print('                </div><!-- System Tab End -->')

        else:
            print('            <!-- cPanel Starter Row -->')
            print('            <div class="row justify-content-lg-center">')
            print('')
            print('                <!-- Column Start -->')
            print('                <div class="col-lg-6">')

            cardheader('Initial Subdirectory Upstream Configuration')
            print('                        <div class="card-body">  <!-- Card Body Start -->')
            print('                            <form class="form mb-0" action="subdir_select_app_settings.live.py" method="get">')
            print('                                <div class="alert alert-info text-center">')
            print('                                    <p class="m-0 pb-1">Select upstream type for:</p>')
            print(('                                    <kbd class="m-1">'+mydomain+'/'+thesubdir+'</kbd>'))
            print('                                </div>')
            print('                                <div class="input-group mb-3">')
            print('                                    <div class="input-group-prepend input-group-prepend-min">')
            print('                                        <label class="input-group-text">Upstream</label>')
            print('                                    </div>')
            print('                                    <select name="backend" class="custom-select">')

            for backends_defined in list(backend_data_yaml_parsed.keys()):
                print(('                                        <option value="'+backends_defined+'">'+backends_defined+'</option>'))

            print('                                    </select>')
            print('                                </div>')

            # Pass on the domain and subdirectory to the next stage
            print(('                                <input hidden name="domain" value="'+mydomain+'">'))
            print(('                                <input hidden name="thesubdir" value="'+thesubdir+'">'))
            print('                                <button class="btn btn-outline-primary btn-block" type="submit">Confirm Upstream</button>')
            print('                            </form>')
            print('                        </div> <!-- Card Body End -->')
            cardfooter('Select the upstream category to use with this application.')

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
