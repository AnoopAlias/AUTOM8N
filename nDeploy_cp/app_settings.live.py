#!/usr/bin/python

import commoninclude
import os
import yaml
import cgi
import cgitb
import sys
try:
    import simplejson as json
except ImportError:
    import json


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

commoninclude.close_cpanel_liveapisock()
form = cgi.FieldStorage()

commoninclude.print_header()

print('<body>')

commoninclude.print_branding()

print('<div id="main-container" class="container">')  # main container

print('		<nav aria-label="breadcrumb">')
print('			<ol class="breadcrumb">')
print('				<li class="breadcrumb-item"><a href="xtendweb.live.py"><i class="fas fa-redo"></i></a></li>')
print('				<li class="breadcrumb-item active">Manual Config</li>')
print('			</ol>')
print('		</nav>')

print('		<div class="row justify-content-lg-center">')

print('			<div class="col-lg-6">')  # col left

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
        # App settings
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
            commoninclude.print_error_wrapper()
            sys.exit(0)

        # Ok we are done with getting the settings,now lets present it to the user
        # System Setup
        print('		<div class="card">')  # card
        print('			<div class="card-header">')
        print('				<h5 class="card-title mb-0"><i class="fas fa-users-cog float-right"></i> server: '+mydomain+'</h5>')
        print('			</div>')

        print('			<div class="card-body p-0">')  # card-body
        print('				<div class="row no-gutters">')  # row
        if backend_category == 'PROXY':
            if backend_version == 'httpd':
                # Running
                print('			<div class="col-md-6 alert alert-light"><i class="fas fa-play"></i> Running</div>')
                print('			<div class="col-md-6 alert alert-success">Nginx</div>')

                # Backend
                print('			<div class="col-md-6 alert alert-light"><i class="fa fa-server"></i> Upstream</div>')
                print('			<div class="col-md-6 alert alert-success">'+backend_version+'</div>')

                # Description
                print('			<div class="col-md-6 alert alert-light"><i class="fas fa-cog"></i> Template</div>')
                print('			<div class="col-md-6 alert alert-success">'+apptemplate_description+'</div>')

                # .hitaccess
                print('			<div class="col-md-6 alert alert-light"><i class="fas fa-file-code"></i> .htaccess</div>')
                print('			<div class="col-md-6 alert alert-success"><i class="fas fa-check"></i> &nbsp;</div>')
            else:
                # Running
                print('			<div class="col-md-6 alert alert-light"><i class="fas fa-play"></i> Running</div>')
                print('			<div class="col-md-6 alert alert-success">Nginx</div>')

                # Backend
                print('			<div class="col-md-6 alert alert-light"><i class="fas fa-server"></i> Upstream</div>')
                print('			<div class="col-md-6 alert alert-success">'+backend_version+'</div>')

                # Description
                print('			<div class="col-md-6 alert alert-light"><i class="fas fa-cog"></i> Template</div>')
                print('			<div class="col-md-6 alert alert-success">'+apptemplate_description+'</div>')

                # .hitaccess
                print('			<div class="col-md-6 alert alert-light"><i class="fas fa-file-code"></i> .htaccess</div>')
                print('			<div class="col-md-6 alert alert-danger"><i class="fas fa-times"></i> Ignored</div>')
        else:
            # Running
            print('				<div class="col-md-6 alert alert-light"><i class="fas fa-play"></i> Running</div>')
            print('				<div class="col-md-6 alert alert-success">Nginx</div>')

            # Backend
            print('				<div class="col-md-6 alert alert-light"><i class="fas fa-server"></i> Upstream</div>')
            print('				<div class="col-md-6 alert alert-success">'+backend_version+'</div>')

            # Description
            print('				<div class="col-md-6 alert alert-light"><i class="fas fa-cog"></i> Template</div>')
            print('				<div class="col-md-6 alert alert-success">'+apptemplate_description+'</div>')

            # .hitaccess
            print('				<div class="col-md-6 alert alert-light"><i class="fas fa-file-code"></i> .htaccess</div>')
            print('				<div class="col-md-6 alert alert-danger"><i class="fas fa-times"></i> Ignored</div>')

        # User config reload
        nginx_log_hint = document_root + '/nginx.conf'
        commoninclude.print_sys_tip('<i class="fas fa-user-cog"></i> nginx.conf', nginx_log_hint)
        if os.path.isfile(nginx_log_hint):
            if os.path.isfile("/etc/nginx/sites-enabled/"+mydomain+".manualconfig_user"):
                print('			<div class="col-md-6 alert alert-success"><i class="fas fa-check"></i> Valid</div>')
            else:
                print('			<div class="col-md-6 alert alert-danger"><i class="fas fa-times"></i> Invalid or require reload</div>')
        else:
            print('			<div class="col-md-6 alert alert-secondary"><i class="fas fa-file-upload"></i> No File uploaded</div>')

        # Reload Nginx
        print('					<div class="col-md-6 alert alert-light"><i class="fas fa-sync-alt"></i>nginx.conf reload</div>')
        print('					<div class="col-md-6">')
        print('						<form class="form" method="post" id="toastForm4" onsubmit="return false;">')
        print('							<button class="alert alert-info btn btn-info" type="submit">Reload</button>')
        print(('						<input class="hidden" name="domain" value="'+mydomain+'">'))
        print('						</form>')
        print('					</div>')

        # Nginx Log
        print('					<div class="col-md-6 alert alert-light"><i class="fas fa-clipboard-list"></i>nginx.conf reload log</div>')
        print('					<div class="col-md-6">')
        print('						<form class="form" method="post" id="modalForm5" onsubmit="return false;">')
        print('							<button class="alert alert-info btn btn-info" type="submit">View Log</button>')
        print(('						<input class="hidden" name="domain" value="'+mydomain+'">'))
        print('						</form>')
        print('					</div>')

        print('				</div>')  # row end
        print('			</div>')  # card-body end

        # Dependencies
        if backend_category == 'RUBY' or backend_category == 'PYTHON' or backend_category == 'NODEJS' or backend_category == 'PHP':
            print('		<div class="card-body pb-0">')  # card-body
            print('			<form class="mb-0" id="modalForm10" onsubmit="return false;">')
            if backend_category == "RUBY":
                dep_file = document_root + '/Gemfile'
            elif backend_category == "NODEJS":
                dep_file = document_root + '/package.json'
            elif backend_category == 'PYTHON':
                dep_file = document_root + '/requirements.txt'
            elif backend_category == 'PHP':
                dep_file = document_root + '/composer.json'
            print(('			<input class="hidden" name="domain" value="'+mydomain+'">'))
            print(('			<input class="hidden" name="document_root" value="'+document_root+'">'))
            print(('			<input class="hidden" name="backend_category" value="'+backend_category+'">'))
            print(('			<input class="hidden" name="backend_version" value="'+backend_version+'">'))
            print('				<button class="btn btn-outline-warning btn-block " data-toggle="tooltip" title="'+dep_file+'" type="submit">Install '+backend_category+' project deps</button>')
            print('			</form>')

            if backend_category == 'PHP':
                print('			<form class="mb-0 mt-3" id="modalForm1" onsubmit="return false;">')
                print('				<button class="btn btn-outline-warning btn-block " type="submit">View PHP Log</button>')
                print('			</form>')

            print('		</div>')  # card-body end

        print('			<div class="card-body">')  # card-body

        if settings_lock == 'enabled':
            print(('<div class="alert alert-info mb-0">Application Server settings are locked by the administrator</div>'))
        else:
            print('			<form class="mb-0" action="select_app_settings.live.py" method="get">')
            print('				<div class="input-group">')
            print('					<select name="backend" class="custom-select">')
            for backends_defined in backend_data_yaml_parsed.keys():
                if backends_defined == backend_category:
                    print(('			<option selected value="'+backends_defined+'">'+backends_defined+'</option>'))
                else:
                    print(('			<option value="'+backends_defined+'">'+backends_defined+'</option>'))
            print('					</select>')
            # Pass on the domain name to the next stage
            print('					<div class="input-group-append">')
            print(('					<input class="hidden" name="domain" value="'+mydomain+'">'))
            print('						<button type="submit" class="btn btn-outline-primary">Select</button>')
            print('					</div>')
            print('				</div>')
            print('			</form>')
        print('			</div>')  # card-body end

        print('			<div class="card-footer">')
        print('				<small>To change the Upstream select a new category above.</small>')
        print('			</div>')
        print('		</div>')  # card end

        # Application Settings
        print('		<div class="card">')  # card
        print('			<div class="card-header">')
        print('				<h5 class="card-title mb-0"><i class="fas fa-sliders-h float-right"></i> General Settings</h5>')
        print('			</div>')
        print('			<div class="card-body">')  # card-body

        print('				<form class="form" method="post" id="toastForm3" onsubmit="return false;">')
        print('					<div class="row align-items-center">')

        # auth_basic
        auth_basic_hint = "Setup password for "+document_root+" in cPanel -> Files -> Directory Privacy"
        if auth_basic == 'enabled':
            commoninclude.print_green('password protect app url', auth_basic_hint)
            print('				<div class="col-md-6">')
            print('					<div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
            print('						<label class="btn btn-light active">')
            print('							<input type="radio" name="auth_basic" value="enabled" id="AuthBasicOn" autocomplete="off" checked> Enabled')
            print('						</label>')
            print('						<label class="btn btn-light">')
            print('							<input type="radio" name="auth_basic" value="disabled" id="AuthBasicOff" autocomplete="off"> Disabled')
            print('						</label>')
            print('					</div>')
            print('				</div>')
        else:
            commoninclude.print_red('password protect app url', auth_basic_hint)
            print('				<div class="col-md-6">')
            print('					<div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
            print('						<label class="btn btn-light">')
            print('							<input type="radio" name="auth_basic" value="enabled" id="AuthBasicOn" autocomplete="off"> Enabled')
            print('						</label>')
            print('						<label class="btn btn-light active">')
            print('							<input type="radio" name="auth_basic" value="disabled" id="AuthBasicOff" autocomplete="off" checked> Disabled')
            print('						</label>')
            print('					</div>')
            print('				</div>')

        # autoindex
        autoindex_hint = "enable for directory listing"
        if autoindex == 'enabled':
            commoninclude.print_green("autoindex", autoindex_hint)
            print('				<div class="col-md-6">')
            print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('						<label class="btn btn-light active">')
            print('							<input type="radio" name="autoindex" value="enabled" id="AutoIndexOn" autocomplete="off" checked> Enabled')
            print('						</label>')
            print('						<label class="btn btn-light">')
            print('							<input type="radio" name="autoindex" value="disabled" id="AutoIndexOff" autocomplete="off"> Disabled')
            print('						</label>')
            print('					</div>')
            print('				</div>')
        else:
            commoninclude.print_red("autoindex", autoindex_hint)
            print('				<div class="col-md-6">')
            print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('						<label class="btn btn-light">')
            print('							<input type="radio" name="autoindex" value="enabled" id="AutoIndexOn" autocomplete="off"> Enabled')
            print('						</label>')
            print('						<label class="btn btn-light active">')
            print('							<input type="radio" name="autoindex" value="disabled" id="AutoIndexOff" autocomplete="off" checked> Disabled')
            print('						</label>')
            print('					</div>')
            print('				</div>')

        # ssl_offload
        ssl_offload_hint = "enable for performance, disable if redirect loop error"
        if ssl_offload == 'enabled':
            commoninclude.print_green("ssl_offload", ssl_offload_hint)
            print('				<div class="col-md-6">')
            print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('						<label class="btn btn-light active">')
            print('							<input type="radio" name="ssl_offload" value="enabled" id="SslOffloadOn" autocomplete="off" checked> Enabled')
            print('						</label>')
            print('						<label class="btn btn-light">')
            print('							<input type="radio" name="ssl_offload" value="disabled" id="SslOffloadOff" autocomplete="off"> Disabled')
            print('						</label>')
            print('					</div>')
            print('				</div>')
        else:
            commoninclude.print_red("ssl_offload", ssl_offload_hint)
            print('				<div class="col-md-6">')
            print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('						<label class="btn btn-light">')
            print('							<input type="radio" name="ssl_offload" value="enabled" id="SslOffloadOn" autocomplete="off"> Enabled')
            print('						</label>')
            print('						<label class="btn btn-light active">')
            print('							<input type="radio" name="ssl_offload" value="disabled" id="SslOffloadOff" autocomplete="off" checked> Disabled')
            print('						</label>')
            print('					</div>')
            print('				</div>')

        # access_log
        access_log_hint = "disabling access_log increase performance but stats wont work"
        if access_log == 'enabled':
            commoninclude.print_green("access_log", access_log_hint)
            print('				<div class="col-md-6">')
            print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('						<label class="btn btn-light active">')
            print('							<input type="radio" name="access_log" value="enabled" id="AccessLogOn" autocomplete="off" checked> Enabled')
            print('						</label>')
            print('						<label class="btn btn-light">')
            print('							<input type="radio" name="access_log" value="disabled" id="AccessLogOff" autocomplete="off"> Disabled')
            print('						</label>')
            print('					</div>')
            print('				</div>')
        else:
            commoninclude.print_red("access_log", access_log_hint)
            print('				<div class="col-md-6">')
            print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('						<label class="btn btn-light">')
            print('							<input type="radio" name="access_log" value="enabled" id="AccessLogOn" autocomplete="off"> Enabled')
            print('						</label>')
            print('						<label class="btn btn-light active">')
            print('							<input type="radio" name="access_log" value="disabled" id="AccessLogOff" autocomplete="off" checked> Disabled')
            print('						</label>')
            print('					</div>')
            print('				</div>')

        # open_file_cache
        open_file_cache_hint = "increase performance, disable on dev environment for no caching"
        if open_file_cache == 'enabled':
            commoninclude.print_green("open_file_cache", open_file_cache_hint)
            print('				<div class="col-md-6">')
            print('					<div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')
            print('						<label class="btn btn-light active">')
            print('							<input type="radio" name="open_file_cache" value="enabled" id="OpenFileCacheOn" autocomplete="off" checked> Enabled')
            print('						</label>')
            print('						<label class="btn btn-light">')
            print('							<input type="radio" name="open_file_cache" value="disabled" id="OpenFileCacheOff" autocomplete="off"> Disabled')
            print('						</label>')
            print('					</div>')
            print('				</div>')
        else:
            commoninclude.print_red("open_file_cache", open_file_cache_hint)
            print('				<div class="col-md-6">')
            print('					<div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')
            print('						<label class="btn btn-light">')
            print('							<input type="radio" name="open_file_cache" value="enabled" id="OpenFileCacheOn" autocomplete="off"> Enabled')
            print('						</label>')
            print('						<label class="btn btn-light active">')
            print('							<input type="radio" name="open_file_cache" value="disabled" id="OpenFileCacheOff" autocomplete="off" checked> Disabled')
            print('						</label>')
            print('					</div>')
            print('				</div>')

        print('				</div>')  # row end
        print('			</div>')  # card-body end
        print('		</div>')  # card end

        # Security Settings
        print('		<div class="card">')  # card
        print('			<div class="card-header">')
        print('				<h5 class="card-title mb-0"><i class="fas fa-shield-alt float-right"></i> Security Settings</h5>')
        print('			</div>')
        print('			<div class="card-body">')  # card-body

        if settings_lock == 'enabled':
            print(('		<div class="alert alert-info mb-0">Security settings are locked by the administrator</div>'))
            print(('		<input class="hidden" name="security_headers" value="'+security_headers+'">'))
            print(('		<input class="hidden" name="dos_mitigate" value="'+dos_mitigate+'">'))
            print(('		<input class="hidden" name="test_cookie" value="'+test_cookie+'">'))
            print(('		<input class="hidden" name="symlink_protection" value="'+symlink_protection+'">'))
            print(('		<input class="hidden" name="mod_security" value="'+mod_security+'">'))
        else:

            print('			<div class="row align-items-center">')

            # security_headers
            security_headers_hint = "X-Frame-Options,X-Content-Type-Options,X-XSS-Protection,HSTS"
            if security_headers == 'enabled':
                commoninclude.print_green("security_headers", security_headers_hint)
                print('			<div class="col-md-6">')
                print('				<div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
                print('					<label class="btn btn-light active">')
                print('						<input type="radio" name="security_headers" value="enabled" id="SecurityHeadersOn" autocomplete="off" checked> Enabled')
                print('					</label>')
                print('					<label class="btn btn-light">')
                print('						<input type="radio" name="security_headers" value="disabled" id="SecurityHeadersOff" autocomplete="off"> Disabled')
                print('					</label>')
                print('				</div>')
                print('			</div>')
            else:
                commoninclude.print_red("security_headers", security_headers_hint)
                print('			<div class="col-md-6">')
                print('				<div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
                print('					<label class="btn btn-light">')
                print('						<input type="radio" name="security_headers" value="enabled" id="SecurityHeadersOn" autocomplete="off"> Enabled')
                print('					</label>')
                print('					<label class="btn btn-light active">')
                print('						<input type="radio" name="security_headers" value="disabled" id="SecurityHeadersOff" autocomplete="off" checked> Disabled')
                print('					</label>')
                print('				</div>')
                print('			</div>')

            # dos_mitigate
            dos_mitigate_hint = "Enable only when under a dos attack"
            if dos_mitigate == 'enabled':
                commoninclude.print_green("dos_mitigate", dos_mitigate_hint)
                print('			<div class="col-md-6">')
                print('				<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                print('					<label class="btn btn-light active">')
                print('						<input type="radio" name="dos_mitigate" value="enabled" id="DosMitigateOn" autocomplete="off" checked> Enabled')
                print('					</label>')
                print('					<label class="btn btn-light">')
                print('						<input type="radio" name="dos_mitigate" value="disabled" id="DosMitigateOff" autocomplete="off"> Disabled')
                print('					</label>')
                print('				</div>')
                print('			</div>')
            else:
                commoninclude.print_red("dos_mitigate", dos_mitigate_hint)
                print('			<div class="col-md-6">')
                print('				<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                print('					<label class="btn btn-light">')
                print('						<input type="radio" name="dos_mitigate" value="enabled" id="DosMitigateOn" autocomplete="off"> Enabled')
                print('					</label>')
                print('					<label class="btn btn-light active">')
                print('						<input type="radio" name="dos_mitigate" value="disabled" id="DosMitigateOff" autocomplete="off" checked> Disabled')
                print('					</label>')
                print('				</div>')
                print('			</div>')

            # test_cookie
            test_cookie_hint = "Disable most bots except good ones like google/yahoo etc with a cookie challenge"
            if os.path.isfile('/etc/nginx/modules.d/testcookie_access.load'):
                if test_cookie == 'enabled':
                    commoninclude.print_green("bot_mitigate", test_cookie_hint)
                    print('			<div class="col-md-6">')
                    print('				<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                    print('					<label class="btn btn-light active">')
                    print('						<input type="radio" name="test_cookie" value="enabled" id="TestCookieOn" autocomplete="off" checked> Enabled')
                    print('					</label>')
                    print('					<label class="btn btn-light">')
                    print('						<input type="radio" name="test_cookie" value="disabled" id="TestCookieOff" autocomplete="off"> Disabled')
                    print('					</label>')
                    print('				</div>')
                    print('			</div>')
                else:
                    commoninclude.print_red("bot_mitigate", test_cookie_hint)
                    print('			<div class="col-md-6">')
                    print('				<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                    print('					<label class="btn btn-light">')
                    print('						<input type="radio" name="test_cookie" value="enabled" id="TestCookieOn" autocomplete="off"> Enabled')
                    print('					</label>')
                    print('					<label class="btn btn-light active">')
                    print('						<input type="radio" name="test_cookie" value="disabled" id="TestCookieOff" autocomplete="off" checked> Disabled')
                    print('					</label>')
                    print('				</div>')
                    print('			</div>')
            else:
                commoninclude.print_red("bot_mitigate", test_cookie_hint)
                commoninclude.print_disabled()
                print(('<input class="hidden" name="test_cookie" value="'+test_cookie+'">'))

            # symlink_protection
            symlink_protection_hint = "Access to a file is denied if any component of the pathname is a symbolic link, and the link and object that the link points to have different owners"
            if symlink_protection == 'enabled':
                commoninclude.print_green("symlink_protection", symlink_protection_hint)
                print('				<div class="col-md-6">')
                print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                print('						<label class="btn btn-light active">')
                print('							<input type="radio" name="symlink_protection" value="enabled" id="SymlinkProtectionOn" autocomplete="off" checked> Enabled')
                print('						</label>')
                print('						<label class="btn btn-light">')
                print('							<input type="radio" name="symlink_protection" value="disabled" id="SymlinkProtectionOff" autocomplete="off"> Disabled')
                print('						</label>')
                print('					</div>')
                print('				</div>')
            else:
                commoninclude.print_red("symlink_protection", symlink_protection_hint)
                print('				<div class="col-md-6">')
                print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                print('						<label class="btn btn-light">')
                print('							<input type="radio" name="symlink_protection" value="enabled" id="SymlinkProtectionOn" autocomplete="off"> Enabled')
                print('						</label>')
                print('						<label class="btn btn-light active">')
                print('							<input type="radio" name="symlink_protection" value="disabled" id="SymlinkProtectionOff" autocomplete="off" checked> Disabled')
                print('						</label>')
                print('					</div>')
                print('				</div>')

            # mod_security
            mod_security_hint = "mod_security v3 WAF"
            if os.path.isfile('/etc/nginx/modules.d/zz_modsecurity.load'):
                if mod_security == 'enabled':
                    commoninclude.print_green('mod_security', mod_security_hint)
                    print('			<div class="col-md-6">')
                    print('				<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                    print('					<label class="btn btn-light active">')
                    print('						<input type="radio" name="mod_security" value="enabled" id="ModSecurityOn" autocomplete="off" checked> Enabled')
                    print('					</label>')
                    print('					<label class="btn btn-light">')
                    print('						<input type="radio" name="mod_security" value="disabled" id="ModSecurityOff" autocomplete="off"> Disabled')
                    print('					</label>')
                    print('				</div>')
                    print('			</div>')
                else:
                    commoninclude.print_red('mod_security', mod_security_hint)
                    print('			<div class="col-md-6">')
                    print('				<div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')
                    print('					<label class="btn btn-light">')
                    print('						<input type="radio" name="mod_security" value="enabled" id="ModSecurityOn" autocomplete="off"> Enabled')
                    print('					</label>')
                    print('					<label class="btn btn-light active">')
                    print('						<input type="radio" name="mod_security" value="disabled" id="ModSecurityOff" autocomplete="off" checked> Disabled')
                    print('					</label>')
                    print('				</div>')
                    print('			</div>')
            else:
                commoninclude.print_red('mod_security', mod_security_hint)
                commoninclude.print_disabled()
                print(('<input class="hidden" name="mod_security" value="'+mod_security+'">'))
            print('					</div>')  # row end

        print('				</div>')  # card-body end
        print('			</div>')  # card end

        print('		</div>')   # col left end

        print('		<div class="col-lg-6">')  # col Right

        # Content Optimizations
        print('			<div class="card">')  # card
        print('				<div class="card-header">')
        print('					<h5 class="card-title mb-0"><i class="fas fa-dumbbell float-right"></i> Content Optimization</h5>')
        print('				</div>')
        print('				<div class="card-body">')  # card-body

        print('					<div class="row align-items-center">')

        # set_expire_static
        set_expire_static_hint = "Set Expires/Cache-Control headers for satic content"
        if set_expire_static == 'enabled':
            commoninclude.print_green('set expires header', set_expire_static_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="set_expire_static" value="enabled" id="SetExpireStaticOn" autocomplete="off" checked> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="set_expire_static" value="disabled" id="SetExpireStaticOff" autocomplete="off"> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')
        else:
            commoninclude.print_red('set expires header', set_expire_static_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="set_expire_static" value="enabled" id="SetExpireStaticOn" autocomplete="off"> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="set_expire_static" value="disabled" id="SetExpireStaticOff" autocomplete="off" checked> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')

        # pagespeed
        pagespeed_hint = "delivers pagespeed optimized webpage, resource intensive"
        if os.path.isfile('/etc/nginx/modules.d/pagespeed.load'):
            if pagespeed == 'enabled':
                commoninclude.print_green("pagespeed", pagespeed_hint)
                print('				<div class="col-md-6">')
                print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                print('						<label class="btn btn-light active">')
                print('							<input type="radio" name="pagespeed" value="enabled" id="PagespeedOn" autocomplete="off" checked> Enabled')
                print('						</label>')
                print('						<label class="btn btn-light">')
                print('							<input type="radio" name="pagespeed" value="disabled" id="PagespeedOff" autocomplete="off"> Disabled')
                print('						</label>')
                print('					</div>')
                print('				</div>')
            else:
                commoninclude.print_red("pagespeed", pagespeed_hint)
                print('				<div class="col-md-6">')
                print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                print('						<label class="btn btn-light">')
                print('							<input type="radio" name="pagespeed" value="enabled" id="PagespeedOn" autocomplete="off"> Enabled')
                print('						</label>')
                print('						<label class="btn btn-light active">')
                print('							<input type="radio" name="pagespeed" value="disabled" id="PagespeedOff" autocomplete="off" checked> Disabled')
                print('						</label>')
                print('					</div>')
                print('				</div>')
        else:
            commoninclude.print_red("pagespeed", pagespeed_hint)
            commoninclude.print_disabled()
            print(('<input class="hidden" name="pagespeed" value="'+pagespeed+'">'))

        # pagespeed filter level
        pagespeed_filter_hint = "CoreFilters loads the Core filters. PassThrough allows you to enable individual filters via custom nginx conf"
        if os.path.isfile('/etc/nginx/modules.d/pagespeed.load'):
            if pagespeed_filter == 'CoreFilters':
                commoninclude.print_red("pagespeed filters", pagespeed_filter_hint)
                print('				<div class="col-md-6">')
                print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                print('						<label class="btn btn-light active">')
                print('							<input type="radio" name="pagespeed_filter" value="CoreFilters" id="PagespeedFilterOn" autocomplete="off" checked> Core')
                print('						</label>')
                print('						<label class="btn btn-light">')
                print('							<input type="radio" name="pagespeed_filter" value="PassThrough" id="PagespeedFilterOff" autocomplete="off"> Pass')
                print('						</label>')
                print('					</div>')
                print('				</div>')
            else:
                commoninclude.print_green("pagespeed filters", pagespeed_filter_hint)
                print('				<div class="col-md-6">')
                print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                print('						<label class="btn btn-light">')
                print('							<input type="radio" name="pagespeed_filter" value="CoreFilters" id="PagespeedFilterOn" autocomplete="off"> Core')
                print('						</label>')
                print('						<label class="btn btn-light active">')
                print('							<input type="radio" name="pagespeed_filter" value="PassThrough" id="PagespeedFilterOff" autocomplete="off" checked> Pass')
                print('						</label>')
                print('					</div>')
                print('				</div>')
        else:
            commoninclude.print_red("pagespeed filters", pagespeed_filter_hint)
            commoninclude.print_disabled()
            print(('<input class="hidden" name="pagespeed_filter" value="'+pagespeed_filter+'">'))

        # brotli
        brotli_hint = "bandwidth optimization, resource intensive, tls only"
        if os.path.isfile('/etc/nginx/modules.d/brotli.load'):
            if brotli == 'enabled':
                commoninclude.print_green("brotli", brotli_hint)
                print('				<div class="col-md-6">')
                print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                print('						<label class="btn btn-light active">')
                print('							<input type="radio" name="brotli" value="enabled" id="BrotliOn" autocomplete="off" checked> Enabled')
                print('						</label>')
                print('						<label class="btn btn-light">')
                print('							<input type="radio" name="brotli" value="disabled" id="BrotliOff" autocomplete="off"> Disabled')
                print('						</label>')
                print('					</div>')
                print('				</div>')
            else:
                commoninclude.print_red("brotli", brotli_hint)
                print('				<div class="col-md-6">')
                print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                print('						<label class="btn btn-light">')
                print('							<input type="radio" name="brotli" value="enabled" id="BrotliOn" autocomplete="off"> Enabled')
                print('						</label>')
                print('						<label class="btn btn-light active">')
                print('							<input type="radio" name="brotli" value="disabled" id="BrotliOff" autocomplete="off" checked> Disabled')
                print('						</label>')
                print('					</div>')
                print('				</div>')
        else:
            commoninclude.print_red("brotli", brotli_hint)
            commoninclude.print_disabled()
            print(('<input class="hidden" name="brotli" value="'+brotli+'">'))

        # gzip
        gzip_hint = "bandwidth optimization, resource intensive"
        if gzip == 'enabled':
            commoninclude.print_green("gzip", gzip_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="gzip" value="enabled" id="GzipOn" autocomplete="off" checked> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="gzip" value="disabled" id="GzipOff" autocomplete="off"> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')
        else:
            commoninclude.print_red("gzip", gzip_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="gzip" value="enabled" id="GzipOn" autocomplete="off"> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="gzip" value="disabled" id="GzipOff" autocomplete="off" checked> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')

        # http2
        http2_hint = "works only with TLS"
        if http2 == 'enabled':
            commoninclude.print_green("http2", http2_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="http2" value="enabled" id="Http2On" autocomplete="off" checked> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="http2" value="disabled" id="Http2On" autocomplete="off"> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')
        else:
            commoninclude.print_red("http2", http2_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="http2" value="enabled" id="Http2On" autocomplete="off"> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="http2" value="disabled" id="Http2On" autocomplete="off" checked> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')

        print('					</div>')  # row end
        print('				</div>')  # card-body end
        print('			</div>')  # card end

        # Redirections
        print('			<div class="card">')  # card
        print('				<div class="card-header">')
        print('					<h5 class="card-title mb-0"><i class="fas fa-directions float-right"></i> Redirections</h5>')
        print('				</div>')
        print('				<div class="card-body">')  # card-body

        print('					<div class="row align-items-center">')

        # redirect_to_ssl
        redirect_to_ssl_hint = "redirect http:// to https:// "
        if redirect_to_ssl == 'enabled':
            commoninclude.print_green("redirect_to_ssl", redirect_to_ssl_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="redirect_to_ssl" value="enabled" id="RedirectToSslOn" autocomplete="off" checked> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="redirect_to_ssl" value="disabled" id="RedirectToSslOn" autocomplete="off"> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')
        else:
            commoninclude.print_red("redirect_to_ssl", redirect_to_ssl_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="redirect_to_ssl" value="enabled" id="RedirectToSslOn" autocomplete="off"> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="redirect_to_ssl" value="disabled" id="RedirectToSslOn" autocomplete="off" checked> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')

        # proxy_to_master
        proxy_to_master_hint = "in cluster proxy to master instead of local server "
        if proxy_to_master == 'enabled':
            commoninclude.print_green("proxy_to_master", proxy_to_master_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="proxy_to_master" value="enabled" id="ProxyToMasterOn" autocomplete="off" checked> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="proxy_to_master" value="disabled" id="ProxyToMasterOff" autocomplete="off"> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')
        else:
            commoninclude.print_red("proxy_to_master", proxy_to_master_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="proxy_to_master" value="enabled" id="ProxyToMasterOn" autocomplete="off"> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="proxy_to_master" value="disabled" id="ProxyToMasterOff" autocomplete="off" checked> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')

        # redirect_aliases
        redirect_aliases_hint = "redirect all alias domains to the main domain"
        if redirect_aliases == 'enabled':
            commoninclude.print_green("redirect_aliases", redirect_aliases_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="redirect_aliases" value="enabled" id="RedirectAliasesOn" autocomplete="off" checked> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="redirect_aliases" value="disabled" id="RedirectAliasesOff" autocomplete="off"> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')
        else:
            commoninclude.print_red("redirect_aliases", redirect_aliases_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="redirect_aliases" value="enabled" id="RedirectAliasesOn" autocomplete="off"> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="redirect_aliases" value="disabled" id="RedirectAliasesOff" autocomplete="off" checked> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')

        # wwwredirect
        www_redirect_hint = "select redirection mode"
        if wwwredirect == 'none':
            commoninclude.print_red("www redirect", www_redirect_hint)
        else:
            commoninclude.print_green("www redirect", www_redirect_hint)
        print('						<div class="col-md-6">')
        print('							<div class="input-group btn-group">')
        print('								<select name="wwwredirect" class="custom-select">')
        if wwwredirect == 'none':
            print(('							<option selected value="none">no redirection</option>'))
            print(('							<option value="tononwww">www to non-www</option>'))
            print(('							<option value="towww">non-www to www</option>'))
        elif wwwredirect == 'towww':
            print(('							<option value="none">no redirection</option>'))
            print(('							<option value="tononwww">www to non-www</option>'))
            print(('							<option selected value="towww">non-www to www</option>'))
        elif wwwredirect == 'tononwww':
            print(('							<option value="none">no redirection</option>'))
            print(('							<option selected value="tononwww">www to non-www</option>'))
            print(('							<option value="towww">non-www to www</option>'))
        print('								</select>')
        print('							</div>')
        print('						</div>')

        # URL Redirect
        url_redirect_hint = "select redirection status 301 or 307"
        if redirectstatus == 'none':
            commoninclude.print_red("URL redirect", url_redirect_hint)
        else:
            commoninclude.print_green("URL redirect", url_redirect_hint)
        print('						<div class="col-md-6">')
        print('							<div class="input-group btn-group">')
        print('								<select name="redirectstatus" class="custom-select">')
        if redirectstatus == 'none':
            print(('							<option selected value="none">no redirection</option>'))
            print(('							<option value="301">permanent (301)</option>'))
            print(('							<option value="307">temporary (307)</option>'))
        elif redirectstatus == '301':
            print(('							<option value="none">no redirection</option>'))
            print(('							<option value="307">temporary (307)</option>'))
            print(('							<option selected value="301">permanent (301)</option>'))
        elif redirectstatus == '307':
            print(('							<option value="none">no redirection</option>'))
            print(('							<option selected value="307">temporary (307)</option>'))
            print(('							<option value="301">permanent (301)</option>'))
        print('								</select>')
        print('							</div>')
        print('						</div>')

        # Append request_uri to redirect
        append_requesturi_hint = 'maintain original request $request_uri (with arguments)'
        if append_requesturi == 'enabled' and redirectstatus != 'none':
            commoninclude.print_green("append redirecturl", append_requesturi_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="append_requesturi" value="enabled" id="AppendRequesturiOn" autocomplete="off" checked> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="append_requesturi" value="disabled" id="AppendRequesturiOff" autocomplete="off"> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')
        else:
            commoninclude.print_red("append redirecturl", append_requesturi_hint)
            print('					<div class="col-md-6">')
            print('						<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('							<label class="btn btn-light">')
            print('								<input type="radio" name="append_requesturi" value="enabled" id="AppendRequesturiOn" autocomplete="off"> Enabled')
            print('							</label>')
            print('							<label class="btn btn-light active">')
            print('								<input type="radio" name="append_requesturi" value="disabled" id="AppendRequesturiOff" autocomplete="off" checked> Disabled')
            print('							</label>')
            print('						</div>')
            print('					</div>')

        # Redirect URL
        redirecturl_hint = "A Valid URL, eg: http://mynewurl.tld"
        print('						<div class="col-md-12">')
        print('							<div class="input-group btn-group mb-0">')
        print('								<div class="input-group-prepend">')
        print('									<span class="input-group-text">')
        if redirecturl == "none" or redirectstatus == 'none':
            commoninclude.print_red("Redirect to URL", redirecturl_hint)
        else:
            commoninclude.print_green("Redirect to URL", redirecturl_hint)
        print('									</span>')
        print('								</div>')
        print(('							<input class="form-control" placeholder='+redirecturl+' type="text" name="redirecturl">'))
        print('							</div>')
        print('						</div>')

        print('					</div>')
        print('				</div>')  # card-body end
        print('			</div>')  # card end

        # Save Settings
        print('			<div class="card">')  # card
        print('				<div class="card-body text-center">')  # card-body
        print(('				<input class="hidden" name="domain" value="'+mydomain+'">'))
        print('					<button class="btn btn-outline-primary btn-block " type="submit">Save Settings</button>')
        print('				</form>')
        print('				</div>')  # card-body end
        print('			</div>')  # card end

        # Subdirectory Applications
        print('			<div class="card">')  # card
        print('				<div class="card-header">')
        print('					<h5 class="card-title mb-0"><i class="fas fa-level-down-alt float-right"></i> Subdirectory Applications</h5>')
        print('				</div>')
        print('				<div class="card-body">')  # card-body

        # get the currently configured subdir
        if subdir_apps:
            print('				<div class="label label-default mt-2 mb-2">Current subdirectory apps:</div>')
            mykeypos=1
            for thesubdir in subdir_apps.keys():
                print('			<div class="input-group input-group-inline input-group">')
                print('				<div class="input-group-prepend"><span class="input-group-text">')
                print(mydomain + '/' + thesubdir)
                print('				</span></div>')
                print('				<div class="input-group-append">')
                print('					<form class="form" method="get" action="subdir_app_settings.live.py">')
                print('						<button class="btn btn-outline-primary" type="submit"><span class="sr-only">Edit</span><i class="fas fa-pen"></i></button>')
                print(('					<input class="hidden" name="domain" value="'+mydomain+'">'))
                print(('					<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
                print('					</form>')

                print('					<form class="form toastForm7-wrap" method="post" id="toastForm7'+'-'+str(mykeypos)+'" onsubmit="return false;">')
                print('						<button class="btn btn-outline-danger " type="submit"><span class="sr-only">Delete</span><i class="fas fa-times"></i></button>')
                print(('					<input class="hidden" name="domain" value="'+mydomain+'">'))
                print(('					<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
                print('					</form>')
                print('				</div>')
                print('			</div>')
                mykeypos = mykeypos + 1

        print('					<div class="clearfix"></div>')
        print(('				<div class="label label-default mb-2">Add new subdirectory apps:</div>'))
        print('					<form class="form" method="get" action="subdir_app_settings.live.py">')
        print('						<div class="input-group mb-0">')
        print('							<div class="input-group-prepend">')
        print('								<span class="input-group-text">')
        print(mydomain)
        print('								</span>')
        print('							</div>')
        print('							<input class="form-control" placeholder="/blog" type="text" name="thesubdir">')
        print(('						<input class="hidden" name="domain" value="'+mydomain+'">'))
        print(('						<input class="hidden" name="action" value="add">'))
        print('							<div class="input-group-append"><button class="btn btn-outline-primary" type="submit"><span class="sr-only">Add</span><i class="fas fa-plus"></i></button></div>')
        print('						</div>')
        print('					</form>')
        print('				</div>')  # card-body end
        print('				<div class="card-footer">')
        print('					<small>The path entered above must follow this format <kbd>/blog</kbd> <kbd>/us/forum</kbd></small>')
        print('				</div>')
        print('			</div>')  # card end
    else:
        commoninclude.print_error_wrapper('domain-data file i/o error')
else:
    commoninclude.print_forbidden_wrapper()

print('			</div>')  # col end
print('		</div>')  # row end

print('</div>')  # main-container end

commoninclude.print_modals()
commoninclude.print_loader()

print('</body>')
print('</html>')
