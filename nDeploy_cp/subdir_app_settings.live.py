#!/usr/bin/python

import commoninclude
import os
import socket
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


close_cpanel_liveapisock()
form = cgi.FieldStorage()


commoninclude.print_header()

print('<body>')

commoninclude.print_branding()

print('<div id="main-container" class="container">')  # main container

print('		<nav aria-label="breadcrumb">')
print('			<ol class="breadcrumb">')
print('				<li class="breadcrumb-item"><a href="xtendweb.live.py"><i class="fas fa-redo"></i></a></li>')
print('				<li class="breadcrumb-item active">Subdir Config</li>')
print('			</ol>')
print('		</nav>')

print('		<div class="row justify-content-lg-center">')

print('			<div class="col-lg-6">')  # col left

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
        commoninclude.print_error_wrapper('Error: Invalid sub-directory name')
        sys.exit(0)
    if not re.match("^[\.0-9a-zA-Z/_-]*$", thesubdir):
        commoninclude.print_error_wrapper('Error: Invalid char in sub-directory name')
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
                print('	<div class="card">')  # card
                print('		<div class="card-header">')
                print('			<h5 class="card-title mb-0"><i class="fas fa-signal float-right"></i> '+mydomain+'/'+thesubdir+'</h5>')
                print('		</div>')
                print('		<div class="card-body">')  # card-body
                print('			<form class="form mb-0" action="subdir_select_app_settings.live.py" method="get">')
                print(('			<div class="alert alert-info">Select an upstream for this subdirectory</div>'))
                print('				<div class="input-group mb-3">')
                print('					<div class="input-group-prepend input-group-prepend-min">')
                print('						<label class="input-group-text">Upstream</label>')
                print('					</div>')
                print('					<select name="backend" class="custom-select">')
                for backends_defined in backend_data_yaml_parsed.keys():
                    print(('				<option value="'+backends_defined+'">'+backends_defined+'</option>'))
                print('					</select>')
                print('				</div>')

                # Pass on the domain name to the next stage
                print(('			<input class="hidden" name="domain" value="'+mydomain+'">'))
                print(('			<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
                print('				<button class="btn btn-outline-primary btn-block " type="submit">Select</button>')
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
                mod_security = the_subdir_dict.get('mod_security', 'disabled')
                auth_basic = the_subdir_dict.get('auth_basic', 'disabled')
                set_expire_static = the_subdir_dict.get('set_expire_static', 'disabled')
                redirectstatus = the_subdir_dict.get('redirectstatus', 'none')
                append_requesturi = the_subdir_dict.get('append_requesturi', 'disabled')
                redirecturl = the_subdir_dict.get('redirecturl', 'none')
                uniq_path = document_root+thesubdir
                uniq_filename = md5(uniq_path.encode("utf-8")).hexdigest()
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
                    commoninclude.print_error_wrapper('Error: app template data file error')
                    sys.exit(0)

                # Ok we are done with getting the settings,now lets present it to the user
                print('	<div class="card">')  # card
                print('		<div class="card-header">')
                print('			<h5 class="card-title mb-0"><i class="fas fa-users-cog float-right"></i> '+mydomain+'/'+thesubdir+'</h5>')
                print('		</div>')
                print('		<div class="card-body p-0">')  # card-body
                print('			<div class="row no-gutters">')  # row
                if backend_category == 'PROXY':
                    if backend_version == 'httpd':
                        # Running
                        print('		<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-play"></i> Running</div></div>')
                        print('		<div class="col-md-6"><div class="alert alert-success">Nginx</div></div>')

                        # Backend
                        print('		<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-server"></i> Upstream</div></div>')
                        print('		<div class="col-md-6"><div class="alert alert-success">'+backend_version+'</div></div>')

                        # Description
                        print('		<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-cog"></i> Template</div></div>')
                        print('		<div class="col-md-6"><div class="alert alert-success">'+apptemplate_description+'</div></div>')

                        # .hitaccess
                        print('		<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-file-code"></i> .htaccess</div></div>')
                        print('		<div class="col-md-6"><div class="alert alert-success"><i class="fas fa-check"></i> &nbsp;</div></div>')
                    else:
                        # Running
                        print('		<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-play"></i> Running</div></div>')
                        print('		<div class="col-md-6"><div class="alert alert-success">Nginx</div></div>')

                        # Backend
                        print('		<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-server"></i> Upstream</div></div>')
                        print('		<div class="col-md-6"><div class="alert alert-success">'+backend_version+'</div></div>')

                        # Description
                        print('		<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-cog"></i> Template</div></div>')
                        print('		<div class="col-md-6"><div class="alert alert-success">'+apptemplate_description+'</div></div>')

                        # .hitaccess
                        print('		<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-file-code"></i> .htaccess</div></div>')
                        print('		<div class="col-md-6"><div class="alert alert-danger"><i class="fas fa-times"></i> Ignored</div></div>')
                else:
                    # Running
                    print('			<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-play"></i> Running</div></div>')
                    print('			<div class="col-md-6"><div class="alert alert-success">Nginx</div></div>')

                    # Backend
                    print('			<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-server"></i> Upstream</div></div>')
                    print('			<div class="col-md-6"><div class="alert alert-success">'+backend_version+'</div></div>')

                    # Description
                    print('			<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-cog"></i> Template</div></div>')
                    print('			<div class="col-md-6"><div class="alert alert-success">'+apptemplate_description+'</div></div>')

                    # .hitaccess
                    print('			<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-file-code"></i> .htaccess</div></div>')
                    print('			<div class="col-md-6"><div class="alert alert-danger"><i class="fas fa-times"></i> Ignored</div></div>')

                # User config reload
                nginx_log_hint = document_root+"/"+thesubdir+"/nginx.conf"
                commoninclude.print_sys_tip('<i class="fas fa-user-cog"></i> nginx.conf', nginx_log_hint)
                if os.path.isfile("/etc/nginx/sites-enabled/"+mydomain+"_"+uniq_filename+".manualconfig_user"):
                    print('		<div class="col-md-6"><div class="alert alert-success"><i class="fas fa-check"></i> Valid</div></div>')
                else:
                    print('		<div class="col-md-6"><div class="alert alert-danger"><i class="fas fa-times"></i> Invalid or require reload</div></div>')

                # Reload Nginx
                print('					<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-sync-alt"></i>nginx.conf reload</div></div>')
                print('					<div class="col-md-6">')
                print('						<form class="form" method="post" id="modalForm4" onsubmit="return false;">')
                print('							<button class="alert alert-info btn btn-info " type="submit">Reload</button>')
                print(('						<input class="hidden" name="domain" value="'+mydomain+'">'))
                print('						</form>')
                print('					</div>')

                # Nginx Log
                print('					<div class="col-md-6"><div class="alert alert-light"><i class="fas fa-clipboard-list"></i>nginx.conf reload log</div></div>')
                print('					<div class="col-md-6">')
                print('						<form class="form" method="post" id="modalForm5" onsubmit="return false;">')
                print('							<button class="alert alert-info btn btn-info " type="submit">View Log</button>')
                print(('						<input class="hidden" name="domain" value="'+mydomain+'">'))
                print('						</form>')
                print('					</div>')

                print('			</div>')  # row end
                print('		</div>')  # card-body end

                if backend_category == 'RUBY' or backend_category == 'PYTHON' or backend_category == 'NODEJS' or backend_category == 'PHP':
                    # Next section start here
                    print('<div class="card-body pb-0">')  # card-body
                    print('		<form class="form mb-0" method="post" id="modalForm10" onsubmit="return false;">')
                    if backend_category == "RUBY":
                        dep_file = document_root+'/'+thesubdir+'/Gemfile'
                    elif backend_category == "NODEJS":
                        dep_file = document_root+'/'+thesubdir+'/package.json'
                    elif backend_category == 'PYTHON':
                        dep_file = document_root+'/'+thesubdir+'/requirements.txt'
                    elif backend_category == 'PHP':
                        dep_file = document_root+'/'+thesubdir+'/composer.json'
                    print(('		<input class="hidden" name="domain" value="'+mydomain+'/'+thesubdir+'">'))
                    print(('		<input class="hidden" name="document_root" value="'+document_root+'/'+thesubdir+'">'))
                    print(('		<input class="hidden" name="backend_category" value="'+backend_category+'">'))
                    print(('		<input class="hidden" name="backend_version" value="'+backend_version+'">'))
                    print('			<button class="btn btn-outline-warning btn-block " data-toggle="tooltip" data-placement="top" title="'+dep_file+'" type="submit">Install '+backend_category+' project deps</button>')
                    print('		</form>')

                    if backend_category == 'PHP':
                        print('			<form class="mb-0 mt-3" method="post" id="modalForm1" onsubmit="return false;">')
                        print('				<button class="btn btn-outline-warning btn-block " type="submit">View PHP Log</button>')
                        print('			</form>')

                    print('</div>')  # card-body end

                print('		<div class="card-body mb-0">')  # card-body

                print('			<form class="form mb-0" action="subdir_select_app_settings.live.py" method="get">')
                print('				<div class="input-group mb-0">')
                print('					<select name="backend" class="custom-select">')
                for backends_defined in backend_data_yaml_parsed.keys():
                    if backends_defined == backend_category:
                        print(('			<option selected value="'+backends_defined+'">'+backends_defined+'</option>'))
                    else:
                        print(('			<option value="'+backends_defined+'">'+backends_defined+'</option>'))
                print('					</select>')
                # Pass on the domain name to the next stage
                print('					<div class="input-group-apend">')
                print(('					<input class="hidden" name="domain" value="'+mydomain+'">'))
                print(('					<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
                print('						<button class="btn btn-outline-primary" type="submit">Select</button>')
                print('					</div>')
                print('				</div>')
                print('			</form>')
                print('		</div>')  # card-body end
                print('		<div class="card-footer">')
                print('			<small>To change the application server select a new category below and hit select</small>')
                print('		</div>')

                print('</div>')  # card end

                print('</div>')  # col left end

                print('<div class="col-lg-6">')  # col right

                # Application Settings
                print('		<div class="card">')  # card
                print('			<div class="card-header">')
                print('				<h5 class="card-title mb-0"><i class="fas fa-sliders-h float-right"></i> General Settings</h5>')
                print('			</div>')
                print('			<div class="card-body text-right">')  # card-body

                print('			<form class="form" id="modalForm6" onsubmit="return false;">')
                print('				<div class="row align-items-center">')

                # auth_basic
                auth_basic_hint = "Setup password for "+document_root+"/"+thesubdir+" in cPanel -> Files -> Directory Privacy"
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

                # set_expire_static
                set_expire_static_hint = "Set Expires/Cache-Control headers for satic content"
                if set_expire_static == 'enabled':
                    commoninclude.print_green('set expires header', set_expire_static_hint)
                    print('				<div class="col-md-6">')
                    print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                    print('						<label class="btn btn-light active">')
                    print('							<input type="radio" name="set_expire_static" value="enabled" id="SetExpireStaticOn" autocomplete="off" checked> Enabled')
                    print('						</label>')
                    print('						<label class="btn btn-light">')
                    print('							<input type="radio" name="set_expire_static" value="disabled" id="SetExpireStaticOff" autocomplete="off"> Disabled')
                    print('						</label>')
                    print('					</div>')
                    print('				</div>')
                else:
                    commoninclude.print_red('set expires header', set_expire_static_hint)
                    print('				<div class="col-md-6">')
                    print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                    print('						<label class="btn btn-light">')
                    print('							<input type="radio" name="set_expire_static" value="enabled" id="SetExpireStaticOn" autocomplete="off"> Enabled')
                    print('						</label>')
                    print('						<label class="btn btn-light active">')
                    print('							<input type="radio" name="set_expire_static" value="disabled" id="SetExpireStaticOff" autocomplete="off" checked> Disabled')
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
                        print('				<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
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

                # URL Redirect
                url_redirect_hint = "select redirection status 301 or 307"
                if redirectstatus == 'none':
                    commoninclude.print_red("URL Redirect", url_redirect_hint)
                else:
                    commoninclude.print_green("URL Redirect", url_redirect_hint)
                print('					<div class="col-md-6">')
                print('						<div class="input-group btn-group">')
                print('							<select name="redirectstatus" class="custom-select">')
                if redirectstatus == 'none':
                    print(('						<option selected value="none">no redirection</option>'))
                    print(('						<option value="301">Permanent Redirect</option>'))
                    print(('						<option value="307">Temporary Redirect</option>'))
                elif redirectstatus == '301':
                    print(('						<option value="none">no redirection</option>'))
                    print(('						<option value="307">Temporary Redirect</option>'))
                    print(('						<option selected value="301">Permanent Redirect</option>'))
                elif redirectstatus == '307':
                    print(('						<option value="none">no redirection</option>'))
                    print(('						<option selected value="307">Temporary Redirect</option>'))
                    print(('						<option value="301">Permanent Redirect</option>'))
                print('							</select>')
                print('						</div>')
                print('					</div>')

                # Append request_uri to redirect
                append_requesturi_hint = 'append $request_uri to the redirect URL'
                if append_requesturi == 'enabled' and redirectstatus != 'none':
                    commoninclude.print_green("append $request_uri to redirecturl", append_requesturi_hint)
                    print('				<div class="col-md-6">')
                    print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                    print('						<label class="btn btn-light active">')
                    print('							<input type="radio" name="append_requesturi" value="enabled" id="AppendRequestUriOn" autocomplete="off" checked> Enabled')
                    print('						</label>')
                    print('						<label class="btn btn-light">')
                    print('							<input type="radio" name="append_requesturi" value="disabled" id="AppendRequestUriOff" autocomplete="off"> Disabled')
                    print('						</label>')
                    print('					</div>')
                    print('				</div>')
                else:
                    commoninclude.print_red("append $request_uri to redirecturl", append_requesturi_hint)
                    print('				<div class="col-md-6">')
                    print('					<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
                    print('						<label class="btn btn-light">')
                    print('							<input type="radio" name="append_requesturi" value="enabled" id="AppendRequestUriOn" autocomplete="off"> Enabled')
                    print('						</label>')
                    print('						<label class="btn btn-light active">')
                    print('							<input type="radio" name="append_requesturi" value="disabled" id="AppendRequestUriOff" autocomplete="off" checked> Disabled')
                    print('						</label>')
                    print('					</div>')
                    print('				</div>')

                # Redirect URL
                redirecturl_hint = "A Valid URL, eg: http://mynewurl.tld"
                print('					<div class="col-md-12">')
                print('						<div class="input-group btn-group mb-0">')
                print('							<div class="input-group-prepend">')
                print('								<span class="input-group-text">')
                if redirecturl == "none" or redirectstatus == 'none':
                    commoninclude.print_red("Redirect to URL", redirecturl_hint)
                else:
                    commoninclude.print_green("Redirect to URL", redirecturl_hint)
                print('								</span>')
                print('							</div>')
                print(('						<input class="form-control" placeholder='+redirecturl+' type="text" name="redirecturl">'))
                print('						</div>')
                print('					</div>')

                print('				</div>')  # Row end
                print('			</div>')  # card-body end
                print('		</div>')  # card end

                # Save Settings
                print('		<div class="card">')  # card
                print('			<div class="card-body text-center">')  # card-body
                print(('			<input class="hidden" name="domain" value="'+mydomain+'">'))
                print(('			<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
                print('				<button class="btn btn-outline-primary btn-block " type="submit">Save Settings</button>')
                print('			</div>')  # card-body end
                print('		</div>')  # card end
                print('			</form>')
                print('	</div>')  # col right end
        else:
            print('			<div class="card">')  # card
            print('				<div class="card-header">')
            print('					<h5 class="card-title mb-0"><i class="fas fa-sliders-h float-right"></i> Upstream settings</h5>')
            print('				</div>')
            print('				<div class="card-body text-center">')  # card-body
            print('					<form class="form" action="subdir_select_app_settings.live.py" method="get">')
            print('						<div class="input-group mb-0">')
            print('							<select name="backend" class="custom-select">')
            for backends_defined in backend_data_yaml_parsed.keys():
                print(('						<option value="'+backends_defined+'">'+backends_defined+'</option>'))
            print('							</select>')
            print('							<div class="input-group-apend">')
            print(('							<input class="hidden" name="domain" value="'+mydomain+'">'))
            print(('							<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
            print('								<button class="btn btn-outline-primary" type="submit" value="Submit">Select</button>')
            print('							</div>')
            print('						</div>')
            print('					</form>')
            print('				</div>')  # card-body end
            print('				<div class="card-footer">')
            print('					<small>To change the application server choose a new category above and hit select</small>')
            print('				</div>')
            print('			</div>')  # card end
    else:
        commoninclude.print_error_wrapper('domain-data file i/o error')
else:
    commoninclude.print_forbidden_wrapper()

print('		</div>')  # row end

print('</div>')  # main-container end

commoninclude.print_modals()
commoninclude.print_loader()

print('</body>')
print('</html>')
