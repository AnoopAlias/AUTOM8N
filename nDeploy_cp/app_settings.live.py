#!/usr/bin/python

import os
import cgi
import cgitb
import sys
import yaml
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
app_template_file = installation_path+"/conf/apptemplates.yaml"
cpaneluser = os.environ["USER"]
user_app_template_file = installation_path+"/conf/"+cpaneluser+"_apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"

cgitb.enable()
close_cpanel_liveapisock()

form = cgi.FieldStorage()

print_header('Manual Configuration')
bcrumb('Manual Configuration', 'fas fa-redo')

if form.getvalue('domain'):

    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    if mydomain.startswith('_wildcard_.'):
        cpmydomain = '*.'+mydomain.replace('_wildcard_.', '')
    else:
        cpmydomain = mydomain
    profileyaml = installation_path + "/domain-data/" + mydomain

    # Get data about the backends available
    if os.path.isfile(backend_config_file):
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    cpaneluser = os.environ["USER"]

    # Settings Lock
    if os.path.exists("/var/cpanel/users.cache/" + cpaneluser):
        with open("/var/cpanel/users.cache/" + cpaneluser) as users_file:
            json_parsed_cpusersfile = json.load(users_file)
        hostingplan_filename = json_parsed_cpusersfile.get('PLAN', 'default').encode('utf-8').replace(' ', '_')
    else:
        hostingplan_filename = 'default'
    if hostingplan_filename == 'undefined' or hostingplan_filename == 'default':
        if os.path.isfile(installation_path+"/conf/domain_data_default_local.yaml"):
            TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local.yaml"
        else:
            TEMPLATE_FILE = installation_path+"/conf/domain_data_default.yaml"
    else:
        if os.path.isfile(installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"):
            TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"
        else:
            if os.path.isfile(installation_path+"/conf/domain_data_default_local.yaml"):
                TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local.yaml"
            else:
                TEMPLATE_FILE = installation_path+"/conf/domain_data_default.yaml"
    with open(TEMPLATE_FILE, 'r') as templatefile_data_stream:
        yaml_parsed_templatefile = yaml.safe_load(templatefile_data_stream)
    settings_lock = yaml_parsed_templatefile.get('settings_lock', 'disabled')
    cpdomainjson = "/var/cpanel/userdata/" + cpaneluser + "/" + cpmydomain + ".cache"
    with open(cpdomainjson, 'r') as cpaneldomain_data_stream:
        json_parsed_cpaneldomain = json.load(cpaneldomain_data_stream)
    document_root = json_parsed_cpaneldomain.get('documentroot')

    if os.path.isfile(profileyaml):

        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)

        # App Settings
        backend_category = yaml_parsed_profileyaml.get('backend_category')
        backend_version = yaml_parsed_profileyaml.get('backend_version')
        backend_path = yaml_parsed_profileyaml.get('backend_path')
        apptemplate_code = yaml_parsed_profileyaml.get('apptemplate_code')
        mod_security = yaml_parsed_profileyaml.get('mod_security', 'disabled')
        auth_basic = yaml_parsed_profileyaml.get('auth_basic', 'disabled')
        set_expire_static = yaml_parsed_profileyaml.get('set_expire_static', 'disabled')

        # Server Settings
        autoindex = yaml_parsed_profileyaml.get('autoindex', 'disabled')
        pagespeed = yaml_parsed_profileyaml.get('pagespeed', 'disabled')
        brotli = yaml_parsed_profileyaml.get('brotli', 'disabled')
        gzip = yaml_parsed_profileyaml.get('gzip', 'disabled')
        http2 = yaml_parsed_profileyaml.get('http2', 'disabled')
        access_log = yaml_parsed_profileyaml.get('access_log', 'enabled')
        open_file_cache = yaml_parsed_profileyaml.get('open_file_cache', 'disabled')
        ssl_offload = yaml_parsed_profileyaml.get('ssl_offload', 'disabled')
        proxy_to_master = yaml_parsed_profileyaml.get('proxy_to_master', 'disabled')
        wwwredirect = yaml_parsed_profileyaml.get('wwwredirect', 'none')
        redirect_to_ssl = yaml_parsed_profileyaml.get('redirect_to_ssl', 'disabled')
        redirect_aliases = yaml_parsed_profileyaml.get('redirect_aliases', 'disabled')
        security_headers = yaml_parsed_profileyaml.get('security_headers', 'disabled')
        dos_mitigate = yaml_parsed_profileyaml.get('dos_mitigate', 'disabled')
        pagespeed_filter = yaml_parsed_profileyaml.get('pagespeed_filter', 'CoreFilters')
        redirecturl = yaml_parsed_profileyaml.get('redirecturl', 'none')
        redirectstatus = yaml_parsed_profileyaml.get('redirectstatus', 'none')
        append_requesturi = yaml_parsed_profileyaml.get('append_requesturi', 'disabled')
        test_cookie = yaml_parsed_profileyaml.get('test_cookie', 'disabled')
        symlink_protection = yaml_parsed_profileyaml.get('symlink_protection', 'disabled')
        subdir_apps = yaml_parsed_profileyaml.get('subdir_apps', None)

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
            if apptemplate_code in apptemplate_dict.keys():
                apptemplate_description = apptemplate_dict.get(apptemplate_code)
            else:
                if apptemplate_code in user_apptemplate_dict.keys():
                    apptemplate_description = user_apptemplate_dict.get(apptemplate_code)
        else:
            print_nontoast_error('Forbidden!', 'Application Template IO Error!')
            sys.exit(0)

        print('            <!-- cPanel Start Dash Row -->')
        print('            <div class="row justify-content-lg-center">')
        print('')
        print('                <!-- Dash Start -->')
        print('                <div class="col-lg-12">')

        # Domain Status
        cardheader('Current Application Settings: <kbd class="p-1">'+mydomain+'</kbd>','far fa-lightbulb')
        cardfooter('')

        print('                </div> <!-- Dash End -->')
        print('')
        print('            </div> <!-- cPanel End Dash Row -->')

        print('            <!-- Dash Widgets Start -->')
        print('            <div id="dashboard" class="row flex-row">')
        print('')

        print('                <div id="nginx_status_widget" class="col-sm-6 col-xl-4"> <!-- Nginx Dash Start -->')
        cardheader('')
        print('                    <div class="card-body text-center"> <!-- Card Body Start -->')
        print('                        <h4 class="mb-0"><i class="fas fa-play"></i> Running</h4>')
        print('                        <ul class="list-unstyled mb-0">')
        print('                            <li class="mt-2 text-success">Nginx</li>')
        print('                        </ul>')
        print('                    </div> <!-- Card Body End -->')
        cardfooter('')
        print('                </div> <!-- Nginx Dash End -->')

        print('                <div id="backend_upstream_widget" class="col-sm-6 col-xl-4"> <!-- Backend Dash Start -->')
        cardheader('')
        print('                    <div class="card-body text-center"> <!-- Card Body Start -->')
        print('                        <h4 class="mb-0"><i class="fa fa-server"></i> Upstream</h4>')
        print('                        <ul class="list-unstyled mb-0">')
        print('                            <li class="mt-2 text-success">'+backend_version+'</li>')
        print('                        </ul>')
        print('                    </div> <!-- Card Body End -->')
        cardfooter('')
        print('                </div> <!-- Backend Dash End -->')

        print('                <div id="app_template_widget" class="col-sm-12 col-xl-4"> <!-- Tamplate Dash Start -->')
        cardheader('')
        print('                    <div class="card-body text-center"> <!-- Card Body Start -->')
        print('                        <h4 class="mb-0"><i class="fas fa-cog"></i> Template</h4>')
        print('                        <ul class="list-unstyled mb-0">')
        print('                            <li class="mt-2 text-success">'+apptemplate_description+'</li>')
        print('                        </ul>')
        print('                    </div> <!-- Card Body End -->')
        cardfooter('')
        print('                </div> <!-- Tamplate Dash End -->')

        print('')
        print('            </div> <!-- Dash Widgets End -->')
        print('')

        print('            <!-- CP Tabs Row -->')
        print('            <div id="primary-tabs" class="row justify-content-lg-center flex-nowrap">')
        print('')
        print('                <!-- Secondary Navigation -->')
        print('                <div class="pl-3 col-md-3 nav flex-column nav-pills d-none d-lg-block d-xl-block d-xs-none d-sm-none" id="v-pills-tab" role="tablist" aria-orientation="vertical">')
        print('                    <a class="nav-link active" id="v-pills-system-tab" data-toggle="pill" href="#v-pills-system" role="tab" aria-controls="v-pills-system-tab">Application Status</a>')
        print('                    <a class="nav-link" id="v-pills-general-tab" data-toggle="pill" href="#v-pills-general" role="tab" aria-controls="v-pills-general">General Settings</a>')
        print('                    <a class="nav-link" id="v-pills-security-tab" data-toggle="pill" href="#v-pills-security" role="tab" aria-controls="v-pills-security">Security Settings</a>')
        print('                    <a class="nav-link" id="v-pills-optimizations-tab" data-toggle="pill" href="#v-pills-optimizations" role="tab" aria-controls="v-pills-optimizations">Content Optimizations</a>')
        print('                    <a class="nav-link" id="v-pills-redirections-tab" data-toggle="pill" href="#v-pills-redirections" role="tab" aria-controls="v-pills-redirections">Redirections</a>')
        print('                    <a class="nav-link mb-4" id="v-pills-subdirectory-tab" data-toggle="pill" href="#v-pills-subdirectory" role="tab" aria-controls="v-pills-subdirectory">Subdirectory Applications</a>')

        # Save Settings
        print('                    <button class="btn btn-primary btn-block app-backend-settings-btn" type="submit" form="app_backend_settings">Apply Settings</button>')

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
        print('                            <a class="dropdown-item" id="v-pills-security-tab" data-toggle="pill" href="#v-pills-security" role="tab" aria-controls="v-pills-security" aria-selected="false">Security Settings</a>')
        print('                            <a class="dropdown-item" id="v-pills-optimizations-tab" data-toggle="pill" href="#v-pills-optimizations" role="tab" aria-controls="v-pills-optimizations" aria-selected="false">Content Optimizations</a>')
        print('                            <a class="dropdown-item" id="v-pills-redirections-tab" data-toggle="pill" href="#v-redirections-php" role="tab" aria-controls="v-redirections-php" aria-selected="false">Redirections</a>')
        print('                            <a class="dropdown-item" id="v-pills-subdirectory-tab" data-toggle="pill" href="#v-pills-subdirectory" role="tab" aria-controls="v-pills-subdirectory" aria-selected="false">Subdirectory Applications</a>')
        print('                        </div>')

        # Save Settings
        print('                        <button class="btn btn-primary btn-block mb-4 app-backend-settings-btn" type="submit" form="app_backend_settings">Apply Settings</button>')
        print('                    </div>')

        print('')
        print('                    <!-- System Tab -->')
        print('                    <div class="tab-pane fade show active" id="v-pills-system" role="tabpanel" aria-labelledby="v-pills-system-tab">')

        # System Setup
        cardheader('Application Status', 'fas fa-users-cog')
        print('                        <div class="card-body p-0"> <!-- Card Body Start -->')
        print('                            <div class="row no-gutters row-2-col"> <!-- Row Start -->')

        # .htaccess
        if backend_category == 'PROXY':
            if backend_version == 'httpd':
                print('                        <div class="col-6 alert"><i class="fas fa-file-code"></i> .htaccess</div>')
                print('                        <div class="col-6 alert text-success"><i class="fas fa-check-circle"></i></div>')
        else:
            print('                            <div class="col-6 alert"><i class="fas fa-file-code"></i> .htaccess</div>')
            print('                            <div class="col-6 alert text-danger"><i class="fas fa-times-circle"></i></div>')

        # User config reload
        nginx_log_hint = document_root + '/nginx.conf'
        print('                                '+return_sys_tip('<i class="fas fa-user-cog"></i> nginx.conf', nginx_log_hint))
        if os.path.isfile(nginx_log_hint):
            if os.path.isfile("/etc/nginx/sites-enabled/"+mydomain+".manualconfig_user"):
                print('                        <div class="col-6 alert text-success"><i class="fa fa-check-circle"></i> Valid</div>')
            else:
                print('                        <div class="col-6 alert text-danger"><i class="fas fa-times-cicle"></i> Invalid/Require Reload</div>')
        else:
            print('                            <div class="col-6 alert text-center"><i class="fas fa-file-upload"></i> Not Present</div>')

        # Reload Nginx
        print('                                <div class="col-6 alert"><i class="fas fa-sync-alt"></i>nginx.conf reload</div>')
        print('                                <div class="col-6">')
        print('                                    <form class="form" method="post" id="reload_nginx" onsubmit="return false;">')
        print('                                        <input hidden name="domain" value="'+mydomain+'">')
        print('                                        <button id="reload-nginx-btn" class="btn btn-block text-center" type="submit">Reload</button>')
        print('                                    </form>')
        print('                                </div>')

        # Nginx Log
        print('                                <div class="col-6 alert"><i class="fas fa-clipboard-list"></i>nginx.conf reload log</div>')
        print('                                <div class="col-6">')
        print('                                    <form class="form" method="post" id="view_nginx_log" onsubmit="return false;">')
        print('                                        <button id="view-nginx-log-btn" class="btn btn-block text-center" type="submit">View Log</button>')
        print('                                        <input hidden name="domain" value="'+mydomain+'">')
        print('                                    </form>')
        print('                                </div>')
        print('                            </div> <!-- Row End -->')
        print('                        </div> <!-- Card Body End -->')

        # Dependencies
        if backend_category == 'RUBY' or backend_category == 'PYTHON' or backend_category == 'NODEJS' or backend_category == 'PHP':
            print('                        <div class="card-body pt-3 pb-0"> <!-- Card Body Start -->')
            print('                            <form class="form" id="dependency_installer" onsubmit="return false;">')
            if backend_category == "RUBY":
                dep_file = document_root + '/Gemfile'
            elif backend_category == "NODEJS":
                dep_file = document_root + '/package.json'
            elif backend_category == 'PYTHON':
                dep_file = document_root + '/requirements.txt'
            elif backend_category == 'PHP':
                dep_file = document_root + '/composer.json'
            print('                                <input hidden name="domain" value="'+mydomain+'">')
            print('                                <input hidden name="document_root" value="'+document_root+'">')
            print('                                <input hidden name="backend_category" value="'+backend_category+'">')
            print('                                <input hidden name="backend_version" value="'+backend_version+'">')
            print('                            </form>')

            print('                            <div class="btn-group btn-block mt-1">')
            print('                                <button id="dependency-installer-btn" class="btn btn-outline-warning btn-block" data-toggle="tooltip" title="'+dep_file+'" type="submit" form="dependency_installer">Install '+backend_category+' Project Deps</button>')

            if backend_category == 'PHP':
                print('                            <form class="form" id="view_php_log" onsubmit="return false;"></form>')
                print('                            <button id="view-php-log-btn" class="btn btn-outline-warning btn-block" type="submit" form="view_php_log">View PHP Log</button>')

            print('                            </div>')
            print('                        </div> <!-- Card Body End -->')

        print('                        <div class="card-body"> <!-- Card Body Start -->')

        if settings_lock == 'enabled':
            print('                            <div class="alert alert-info mb-0 text-center">Application Server settings are locked by the administrator.</div>')
        else:
            print('                            <form class="mb-0" action="select_app_settings.live.py" method="get">')
            print('                                <div class="input-group">')
            print('                                    <select name="backend" class="custom-select">')
            for backends_defined in backend_data_yaml_parsed.keys():
                if backends_defined == backend_category:
                    print('                                        <option selected value="'+backends_defined+'">'+backends_defined+'</option>')
                else:
                    print('                                        <option value="'+backends_defined+'">'+backends_defined+'</option>')
            print('                                    </select>')

            # Pass on the domain name to the next stage
            print('                                    <div class="input-group-append">')
            print('                                        <input hidden name="domain" value="'+mydomain+'">')
            print('                                        <button type="submit" class="btn btn-outline-primary">Select</button>')
            print('                                    </div>')
            print('                                </div>')
            print('                            </form>')

        print('                        </div> <!-- Card Body End -->')
        cardfooter('To change the upstream select a new category above.')

        print('                    </div><!-- System Tab End -->')

        print('                    <!-- General Setting Tab -->')
        print('                    <div class="tab-pane fade show" id="v-pills-general" role="tabpanel" aria-labelledby="v-pills-general-tab">')

        # Application Settings
        cardheader('General Settings', 'fas fa-sliders-h')
        print('                        <div class="card-body">  <!-- Card Body Start -->')

        print('                        <form class="form" method="post" id="app_backend_settings" onsubmit="return false;">')
        print('                            <input form="app_backend_settings" hidden name="domain" value="'+mydomain+'">')
        print('                            <div class="row row-btn-group-toggle">')

        # auth_basic
        auth_basic_hint = " Setup password for "+document_root+" in cPanel -> Files -> Directory Privacy. "
        print('                                '+return_label("Password Protect Application", auth_basic_hint))
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')

        if auth_basic == 'enabled':
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="auth_basic" value="enabled" id="AuthBasicOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="auth_basic" value="disabled" id="AuthBasicOff" autocomplete="off"> Disabled')
        else:
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="auth_basic" value="enabled" id="AuthBasicOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="auth_basic" value="disabled" id="AuthBasicOff" autocomplete="off" checked> Disabled')

        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

        # autoindex
        autoindex_hint = " Enable for Native NGINX directory listing. "
        print('                                '+return_label("AutoIndex", autoindex_hint))
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

        if autoindex == 'enabled':
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="autoindex" value="enabled" id="AutoIndexOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="autoindex" value="disabled" id="AutoIndexOff" autocomplete="off"> Disabled')
        else:
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="autoindex" value="enabled" id="AutoIndexOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="autoindex" value="disabled" id="AutoIndexOff" autocomplete="off" checked> Disabled')

        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

        # ssl_offload
        ssl_offload_hint = " Enable for a performance increase. Disable if a redirect loop error occurs. "
        print('                                '+return_label("SSL Offload", ssl_offload_hint))
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

        if ssl_offload == 'enabled':
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="ssl_offload" value="enabled" id="SslOffloadOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="ssl_offload" value="disabled" id="SslOffloadOff" autocomplete="off"> Disabled')
        else:
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="ssl_offload" value="enabled" id="SslOffloadOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="ssl_offload" value="disabled" id="SslOffloadOff" autocomplete="off" checked> Disabled')

        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

        # access_log
        access_log_hint = " Disabling access_log will increase performance, but cPanel stats fail to work. "
        print('                                '+return_label("Access Log", access_log_hint))
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

        if access_log == 'enabled':
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="access_log" value="enabled" id="AccessLogOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="access_log" value="disabled" id="AccessLogOff" autocomplete="off"> Disabled')
        else:
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="access_log" value="enabled" id="AccessLogOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="access_log" value="disabled" id="AccessLogOff" autocomplete="off" checked> Disabled')

        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

        # open_file_cache
        open_file_cache_hint = " Enable for performance increase. Disable on development environment to not cache. "
        print('                                '+return_label("Open File Cache", open_file_cache_hint))
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')

        if open_file_cache == 'enabled':
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="open_file_cache" value="enabled" id="OpenFileCacheOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="open_file_cache" value="disabled" id="OpenFileCacheOff" autocomplete="off"> Disabled')
        else:
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="open_file_cache" value="enabled" id="OpenFileCacheOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="open_file_cache" value="disabled" id="OpenFileCacheOff" autocomplete="off" checked> Disabled')

        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

        print('                            </div> <!-- Row End -->')
        print('                        </div> <!-- Card Body End -->')
        cardfooter('')

        print('                    </div><!-- System Tab End -->')

        print('                    <!-- Security Tab -->')
        print('                    <div class="tab-pane fade show" id="v-pills-security" role="tabpanel" aria-labelledby="v-pills-security-tab">')

        # Security Settings
        cardheader('Security Settings','fas fa-shield-alt')
        print('                        <div class="card-body">  <!-- Card Body Start -->')

        if settings_lock == 'enabled':
            print('                        <div class="alert alert-info text-center mb-0">Security settings have been disabled by your host. A customized messages needs to be added to nDeploy Control. </div>')
            print('                        <input hidden name="security_headers" value="'+security_headers+'">')
            print('                        <input hidden name="dos_mitigate" value="'+dos_mitigate+'">')
            print('                        <input hidden name="test_cookie" value="'+test_cookie+'">')
            print('                        <input hidden name="symlink_protection" value="'+symlink_protection+'">')
            print('                        <input hidden name="mod_security" value="'+mod_security+'">')
        else:
            print('                            <div class="row row-btn-group-toggle">')

            # security_headers
            security_headers_hint = " X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, HSTS "
            print('                                '+return_label("Security Headers", security_headers_hint))
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')

            if security_headers == 'enabled':
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="security_headers" value="enabled" id="SecurityHeadersOn" autocomplete="off" checked> Enabled')
                print('                                        </label>')
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="security_headers" value="disabled" id="SecurityHeadersOff" autocomplete="off"> Disabled')
            else:
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="security_headers" value="enabled" id="SecurityHeadersOn" autocomplete="off"> Enabled')
                print('                                        </label>')
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="security_headers" value="disabled" id="SecurityHeadersOff" autocomplete="off" checked> Disabled')

            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')

            # dos_mitigate
            dos_mitigate_hint = " Enable ONLY when under a (D)DOS Attack. "
            print('                                '+return_label("DOS Mitigate", dos_mitigate_hint))
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

            if dos_mitigate == 'enabled':
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="dos_mitigate" value="enabled" id="DosMitigateOn" autocomplete="off" checked> Enabled')
                print('                                        </label>')
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="dos_mitigate" value="disabled" id="DosMitigateOff" autocomplete="off"> Disabled')
            else:
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="dos_mitigate" value="enabled" id="DosMitigateOn" autocomplete="off"> Enabled')
                print('                                        </label>')
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="dos_mitigate" value="disabled" id="DosMitigateOff" autocomplete="off" checked> Disabled')

            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')

            # test_cookie
            test_cookie_hint = " Allow good bots in (like Google/Yahoo). Disable most bad bots by using a cookie challenge. "
            print('                                '+return_label("Bot Mitigate", test_cookie_hint))

            if os.path.isfile('/etc/nginx/modules.d/testcookie_access.load'):

                print('                                <div class="col-md-6">')
                print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

                if test_cookie == 'enabled':
                    print('                                        <label class="btn btn-light active">')
                    print('                                            <input type="radio" name="test_cookie" value="enabled" id="TestCookieOn" autocomplete="off" checked> Enabled')
                    print('                                        </label>')
                    print('                                        <label class="btn btn-light">')
                    print('                                            <input type="radio" name="test_cookie" value="disabled" id="TestCookieOff" autocomplete="off"> Disabled')
                else:
                    print('                                        <label class="btn btn-light">')
                    print('                                            <input type="radio" name="test_cookie" value="enabled" id="TestCookieOn" autocomplete="off"> Enabled')
                    print('                                        </label>')
                    print('                                        <label class="btn btn-light active">')
                    print('                                            <input type="radio" name="test_cookie" value="disabled" id="TestCookieOff" autocomplete="off" checked> Disabled')

                print('                                        </label>')
                print('                                    </div>')
                print('                                </div>')


            else:
                print_disabled()
                print('                                <input hidden name="test_cookie" value="'+test_cookie+'">')

            # symlink_protection
            symlink_protection_hint = " Access to a file is denied if any component of the pathname is a symbolic link, and if the link and object that the link points to has different owners. "
            print('                                '+return_label("Symlink Protection", symlink_protection_hint))
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

            if symlink_protection == 'enabled':
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="symlink_protection" value="enabled" id="SymlinkProtectionOn" autocomplete="off" checked> Enabled')
                print('                                        </label>')
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="symlink_protection" value="disabled" id="SymlinkProtectionOff" autocomplete="off"> Disabled')
            else:
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="symlink_protection" value="enabled" id="SymlinkProtectionOn" autocomplete="off"> Enabled')
                print('                                        </label>')
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="symlink_protection" value="disabled" id="SymlinkProtectionOff" autocomplete="off" checked> Disabled')

            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')

            # mod_security
            mod_security_hint = " Mod Security v3 Web Application Firewall "
            print('                                '+return_label("Mod Security", mod_security_hint))

            if os.path.isfile('/etc/nginx/modules.d/zz_modsecurity.load'):
                print('                                <div class="col-md-6">')
                print('                                    <div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')

                if mod_security == 'enabled':
                    print('                                        <label class="btn btn-light active">')
                    print('                                            <input type="radio" name="mod_security" value="enabled" id="ModSecurityOn" autocomplete="off" checked> Enabled')
                    print('                                        </label>')
                    print('                                        <label class="btn btn-light">')
                    print('                                            <input type="radio" name="mod_security" value="disabled" id="ModSecurityOff" autocomplete="off"> Disabled')
                else:
                    print('                                        <label class="btn btn-light">')
                    print('                                            <input type="radio" name="mod_security" value="enabled" id="ModSecurityOn" autocomplete="off"> Enabled')
                    print('                                        </label>')
                    print('                                        <label class="btn btn-light active">')
                    print('                                            <input type="radio" name="mod_security" value="disabled" id="ModSecurityOff" autocomplete="off" checked> Disabled')

                print('                                        </label>')
                print('                                    </div>')
                print('                                </div>')

            else:
                print_disabled()
                print('                                <input hidden name="mod_security" value="'+mod_security+'">')

            print('                            </div> <!-- Row End -->')

        print('                        </div> <!-- Card Body End -->')
        cardfooter('')

        print('                    </div><!-- System Tab End -->')

        print('                    <!-- Optimizations Tab -->')
        print('                    <div class="tab-pane fade show" id="v-pills-optimizations" role="tabpanel" aria-labelledby="v-pills-optimizations-tab">')

        # Content Optimizations
        cardheader('Content Optimizations', 'fas fa-dumbbell')

        print('                        <div class="card-body">  <!-- Card Body Start -->')
        print('                            <div class="row row-btn-group-toggle"> <!-- Row Start -->')

        # set_expire_static
        set_expire_static_hint = " Set Expires/Cache-Control headers for STATIC content. "
        print('                                '+return_label("Expires / Cache-Control", set_expire_static_hint))
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')

        if set_expire_static == 'enabled':
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="set_expire_static" value="enabled" id="SetExpireStaticOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="set_expire_static" value="disabled" id="SetExpireStaticOff" autocomplete="off"> Disabled')
        else:
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="set_expire_static" value="enabled" id="SetExpireStaticOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="set_expire_static" value="disabled" id="SetExpireStaticOff" autocomplete="off" checked> Disabled')

        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

        # pagespeed
        pagespeed_hint = " Delivers PageSpeed-optimized pages, but is resource intensive. "
        print('                                '+return_label("PageSpeed", pagespeed_hint))

        if os.path.isfile('/etc/nginx/modules.d/pagespeed.load'):
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

            if pagespeed == 'enabled':
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="pagespeed" value="enabled" id="PagespeedOn" autocomplete="off" checked> Enabled')
                print('                                        </label>')
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="pagespeed" value="disabled" id="PagespeedOff" autocomplete="off"> Disabled')
            else:
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="pagespeed" value="enabled" id="PagespeedOn" autocomplete="off"> Enabled')
                print('                                        </label>')
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="pagespeed" value="disabled" id="PagespeedOff" autocomplete="off" checked> Disabled')

            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')

        else:
            print_disabled()
            print('                                <input hidden name="pagespeed" value="'+pagespeed+'">')

        # pagespeed filter level
        pagespeed_filter_hint = " CoreFilters loads the Core Filters, PassThrough allows you to enable individual filters via a custom NGINX Configuration. "
        print('                                '+return_label("PageSpeed Filters", pagespeed_filter_hint))

        if os.path.isfile('/etc/nginx/modules.d/pagespeed.load'):
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

            if pagespeed_filter == 'CoreFilters':
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="pagespeed_filter" value="CoreFilters" id="PagespeedFilterOn" autocomplete="off" checked> Core')
                print('                                        </label>')
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="pagespeed_filter" value="PassThrough" id="PagespeedFilterOff" autocomplete="off"> Pass')
            else:
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="pagespeed_filter" value="CoreFilters" id="PagespeedFilterOn" autocomplete="off"> Core')
                print('                                        </label>')
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="pagespeed_filter" value="PassThrough" id="PagespeedFilterOff" autocomplete="off" checked> Pass')

            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')

        else:
            print_disabled()
            print('                                <input hidden name="pagespeed_filter" value="'+pagespeed_filter+'">')

        # brotli
        brotli_hint = " A newer bandwidth optimization created by Google. It is resource intensive and applies to TLS (HTTPS) ONLY. "
        print('                                '+return_label("Brotli", brotli_hint))

        if os.path.isfile('/etc/nginx/modules.d/brotli.load'):
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

            if brotli == 'enabled':
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="brotli" value="enabled" id="BrotliOn" autocomplete="off" checked> Enabled')
                print('                                        </label>')
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="brotli" value="disabled" id="BrotliOff" autocomplete="off"> Disabled')
            else:
                print('                                        <label class="btn btn-light">')
                print('                                            <input type="radio" name="brotli" value="enabled" id="BrotliOn" autocomplete="off"> Enabled')
                print('                                        </label>')
                print('                                        <label class="btn btn-light active">')
                print('                                            <input type="radio" name="brotli" value="disabled" id="BrotliOff" autocomplete="off" checked> Disabled')

            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')

        else:
            print_disabled()
            print('                                <input hidden name="brotli" value="'+brotli+'">')

        # gzip
        gzip_hint = " A bandwidth optimization that is mildly resource intensive. "
        print('                                '+return_label("GZip", gzip_hint))
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

        if gzip == 'enabled':
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="gzip" value="enabled" id="GzipOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="gzip" value="disabled" id="GzipOff" autocomplete="off"> Disabled')
        else:
            print('                                        <label class="btn btn-light">')
            print('                                           <input type="radio" name="gzip" value="enabled" id="GzipOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="gzip" value="disabled" id="GzipOff" autocomplete="off" checked> Disabled')

        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

        # http2
        http2_hint = " A newer protocol that works with TLS (HTTPS) Only. "
        print('                                '+return_label("HTTP/2", http2_hint))
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')

        if http2 == 'enabled':
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="http2" value="enabled" id="Http2On" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="http2" value="disabled" id="Http2On" autocomplete="off"> Disabled')
        else:
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="http2" value="enabled" id="Http2On" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="http2" value="disabled" id="Http2On" autocomplete="off" checked> Disabled')

        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

        print('                            </div> <!-- Row End -->')
        print('                        </div> <!-- Card Body End -->')
        cardfooter('')

        print('                    </div><!-- System Tab End -->')

        print('                    <!-- Redirections Tab -->')
        print('                    <div class="tab-pane fade show" id="v-pills-redirections" role="tabpanel" aria-labelledby="v-pills-redirections-tab">')

        # Redirections
        cardheader('Redirections', 'fas fa-directions')
        print('                        <div class="card-body"> <!-- Card Body Start -->')
        print('                            <div class="row row-btn-group-toggle"> <!-- Row Start -->')

        # redirect_to_ssl
        redirect_to_ssl_hint = " Redirect HTTP -> HTTPS. "
        print('                                '+return_label("Redirect to SSL", redirect_to_ssl_hint))
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')

        if redirect_to_ssl == 'enabled':
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="redirect_to_ssl" value="enabled" id="RedirectToSslOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="redirect_to_ssl" value="disabled" id="RedirectToSslOn" autocomplete="off"> Disabled')
        else:
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="redirect_to_ssl" value="enabled" id="RedirectToSslOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="redirect_to_ssl" value="disabled" id="RedirectToSslOn" autocomplete="off" checked> Disabled')

        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

        # proxy_to_master
        proxy_to_master_hint = " When running in a cluster, PROXY to MASTER instead of local server. "
        print('                                '+return_label("Proxy to Master", proxy_to_master_hint))
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

        # redirect_aliases
        redirect_aliases_hint = " Redirect all cPanel aliases to the main domain. "
        print('                                '+return_label("Redirect Aliases", redirect_aliases_hint))
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

        if redirect_aliases == 'enabled':
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="redirect_aliases" value="enabled" id="RedirectAliasesOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="redirect_aliases" value="disabled" id="RedirectAliasesOff" autocomplete="off"> Disabled')
        else:
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="redirect_aliases" value="enabled" id="RedirectAliasesOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="redirect_aliases" value="disabled" id="RedirectAliasesOff" autocomplete="off" checked> Disabled')

        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

        # wwwredirect
        www_redirect_hint = " Select WWW redirection mode. "
        print('                                '+return_label("WWW Redirect", www_redirect_hint))
        print('                                <div class="col-md-6">')
        print('                                    <div class="input-group btn-group">')
        print('                                        <select name="wwwredirect" class="custom-select">')

        if wwwredirect == 'none':
            print('                                            <option selected value="none">No Redirection</option>')
            print('                                            <option value="tononwww">WWW -> Non-WWW</option>')
            print('                                            <option value="towww">Non-WWW -> WWW</option>')
        elif wwwredirect == 'towww':
            print('                                            <option value="none">No Redirection</option>')
            print('                                            <option value="tononwww">WWW -> Non-WWW</option>')
            print('                                            <option selected value="towww">Non-WWW -> WWW</option>')
        elif wwwredirect == 'tononwww':
            print('                                            <option value="none">No Redirection</option>')
            print('                                            <option selected value="tononwww">WWW -> Non-WWW</option>')
            print('                                            <option value="towww">Non-WWW -> WWW</option>')

        print('                                        </select>')
        print('                                    </div>')
        print('                                </div>')

        # URL Redirect
        url_redirect_hint = " Select URL redirection type. "
        print('                                '+return_label("URL Redirect", url_redirect_hint))
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
        print('                                '+return_label("Append Redirect URL", append_requesturi_hint))
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
        print('                                                '+return_prepend("Redirect to URL", redirecturl_hint))
        print('                                            </span>')
        print('                                        </div>')
        print('                                        <input class="form-control" value='+redirecturl+' type="text" name="redirecturl">')
        print('                                        </form>')
        print('                                    </div>')
        print('                                </div>')

        print('                            </div> <!-- Row End -->')
        print('                        </div> <!-- Card Body End -->')
        cardfooter('')

        print('                    </div><!-- System Tab End -->')

        print('                    <!-- Subdirectory Tab -->')
        print('                    <div class="tab-pane fade show" id="v-pills-subdirectory" role="tabpanel" aria-labelledby="v-pills-subdirectory-tab">')

        # Subdirectory Applications
        cardheader('Subdirectory Applications', 'fas fa-level-down-alt')
        print('                        <div id="subdirectory-panel" class="card-body">  <!-- Card Body Start -->')

        # Get the currently configured subdirectory
        if subdir_apps:
            print('                            <div class="label label-default mt-2 mb-2">Current subdirectory apps:</div>')
            mykeypos=1
            for thesubdir in subdir_apps.keys():
                print('                            <div class="input-group input-group-inline input-group">')
                print('                                <div class="input-group-prepend">')
                print('                                    <span class="input-group-text">')
                print('                                        '+mydomain + '/' + thesubdir)
                print('                                    </span>')
                print('                                </div>')
                print('                                <div class="input-group-append">')
                print('                                    <form class="form" method="get" id="subdirectory_edit'+'-'+str(mykeypos)+'" action="subdir_app_settings.live.py">')
                print('                                        <input hidden name="domain" value="'+mydomain+'">')
                print('                                        <input hidden name="thesubdir" value="'+thesubdir+'">')
                print('                                    </form>')

                print('                                    <form class="form" method="post" id="subdirectory_delete'+'-'+str(mykeypos)+'" onsubmit="return false;">')
                print('                                        <input hidden name="domain" value="'+mydomain+'">')
                print('                                        <input hidden name="thesubdir" value="'+thesubdir+'">')
                print('                                    </form>')
                print('                                    <button id="subdirectory-edit-btn'+'-'+str(mykeypos)+'" form="subdirectory_edit'+'-'+str(mykeypos)+'" class="btn btn-outline-primary" type="submit"><span class="sr-only">Edit</span><i class="fas fa-pen"></i></button>')
                print('                                    <button id="subdirectory-delete-btn'+'-'+str(mykeypos)+'" form="subdirectory_delete'+'-'+str(mykeypos)+'" class="btn btn-outline-danger " type="submit"><span class="sr-only">Delete</span><i class="fas fa-times"></i></button>')
                print('                                </div>')
                print('                            </div>')
                mykeypos = mykeypos + 1

        print('                            <div class="clearfix"></div>')
        print('                            <div class="label label-default mb-2">Add new subdirectory apps:</div>')
        print('                            <form class="form" method="get" action="subdir_app_settings.live.py">')
        print('                                <div class="input-group mb-0">')
        print('                                    <div class="input-group-prepend">')
        print('                                        <span class="input-group-text">'+mydomain+'</span>')
        print('                                    </div>')
        print('                                    <input class="form-control" placeholder="/blog" type="text" name="thesubdir">')
        print('                                    <input hidden name="domain" value="'+mydomain+'">')
        print('                                    <input hidden name="action" value="add">')
        print('                                    <div class="input-group-append"><button class="btn btn-outline-primary" type="submit"><span class="sr-only">Add</span><i class="fas fa-plus"></i></button></div>')
        print('                                </div>')
        print('                            </form>')
        print('                        </div> <!-- Card Body End -->')
        cardfooter('The path entered above must follow this format <kbd>/blog</kbd>, <kbd>/us/forum</kbd>, etc.')

        print('                    </div> <!-- Subdirectory Tab End -->')

        print('                </div> <!-- Container Tabs End -->')

        print('            </div> <!-- CP Row End -->')

    else:
        print_nontoast_error('Error!', 'Domain Data File IO Error!')
        sys.exit(0)

else:
    print_nontoast_error('Forbidden!', 'Domain Data Missing!')
    sys.exit(0)

print_footer()
