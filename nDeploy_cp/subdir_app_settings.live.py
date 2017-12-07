#!/usr/bin/python
import os
import socket
import yaml
import cgi
import cgitb
import sys
import re
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


def print_green(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-info" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_red(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


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
print('<li><a href="xtendweb.live.py">Select Domain</a></li><li class="active">Sub-directory App Settings</li>')
print('</ol>')
print('<div class="panel panel-default">')
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
        print('ERROR: Invalid sub-directory name')
        sys.exit(0)
    if not re.match("^[0-9a-zA-Z/_-]*$", thesubdir):
        print("Error: Invalid char in sub-directory name")
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
        # If there are no entries in subdir_apps_dict or there is no specific config for the subdirectory
        # We do a fresh config
        if subdir_apps_dict:
            if not subdir_apps_dict.get(thesubdir):
                print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'/'+thesubdir+'</strong></h3></div>'))
                print('<div class="panel-body">')
                print('<form action="subdir_select_app_settings.live.py" method="post">')
                print(('<div class="alert alert-info alert-top">To change the application server select a new category below and hit submit</div>'))
                print('<select name="backend">')
                for backends_defined in backend_data_yaml_parsed.keys():
                    print(('<option value="'+backends_defined+'">'+backends_defined+'</option>'))
                print('</select>')
                # Pass on the domain name to the next stage
                print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
                print(('<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
                print('<input class="btn btn-primary" type="submit" value="Submit">')
                print('</form>')
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
                    print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> ERROR: app template data file error</div>')
                    sys.exit(0)
                # Ok we are done with getting the settings,now lets present it to the user
                print(('<div class="panel-heading"><h3 class="panel-title">Application Server: <strong>'+mydomain+'/'+thesubdir+'</strong></h3></div>'))
                print('<div class="panel-body">')
                print('<form id="config" class="form-inline config-save" action="subdir_select_app_settings.live.py" method="post">')
                print('<ul class="list-group">')
                if backend_category == 'PROXY':
                    if backend_version == 'httpd':
                        print(('<div class="alert alert-info alert-top">Nginx is proxying to <span class="label label-info">'+backend_version+'</span> with settings  <span class="label label-info">'+apptemplate_description+'</span><br>The <span class="label label-info">.htaccess</span> file will work with your current settings </div>'))
                    else:
                        print(('<div class="alert alert-info alert-top">Nginx is proxying to <span class="label label-info">'+backend_version+'</span> with settings  <span class="label label-info">'+apptemplate_description+'</span></div>'))
                else:
                    print(('<div class="alert alert-info alert-top">Your current project is <span class="label label-info">'+apptemplate_description+'</span> on native <span class="label label-info">NGINX</span> with <span class="label label-info">'+backend_category+'</span> <span class="label label-info">'+backend_version+'</span> application server</div>'))
                print('</ul>')
                print(('<div class="alert alert-info alert-top">To change the application server select a new category below and hit submit. All backend category other than <span class="label label-info">PROXY</span> will be directly served by high performance nginx webserver(recommended) </div>'))
                print('<select name="backend">')
                for backends_defined in backend_data_yaml_parsed.keys():
                    if backends_defined == backend_category:
                        print(('<option selected value="'+backends_defined+'">'+backends_defined+'</option>'))
                    else:
                        print(('<option value="'+backends_defined+'">'+backends_defined+'</option>'))
                print('</select>')
                # Pass on the domain name to the next stage
                print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
                print(('<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
                print('<input class="btn btn-primary" type="submit" value="Submit">')
                print('</form>')
                print('</div>')
                print('</li>')
                print('</ul>')
                if backend_category == 'RUBY' or backend_category == 'PYTHON' or backend_category == 'NODEJS':
                    # Next section start here
                    print(('<div class="panel-heading"><h3 class="panel-title">Passenger project deps installer: <strong>'+mydomain+'/'+thesubdir+'</strong></h3></div>'))
                    print('<div class="panel-body">')
                    print('<form id="config" class="form-inline config-save" action="passenger_module_installer.live.py" method="post">')
                    print('<ul class="list-group">')
                    print(('<div class="alert alert-info alert-top">Detected <span class="label label-info">'+backend_category+'</span> <span class="label label-info">'+backend_version+'</span> project </div>'))
                    if backend_category == "RUBY":
                        print(('<div class="alert alert-info alert-top">specify project dependencies in <kbd>'+document_root+'/'+thesubdir+'/Gemfile</kbd></div>'))
                    elif backend_category == "NODEJS":
                        print(('<div class="alert alert-info alert-top">specify project dependencies in <kbd>'+document_root+'/'+thesubdir+'/package.json</kbd></div>'))
                    elif backend_category == 'PYTHON':
                        print(('<div class="alert alert-info alert-top">specify project dependencies in <kbd>'+document_root+'/'+thesubdir+'/requirements.txt</kbd></div>'))
                    print(('<input class="hidden" name="domain" value="'+mydomain+'/'+thesubdir+'">'))
                    print(('<input class="hidden" name="document_root" value="'+document_root+'/'+thesubdir+'">'))
                    print(('<input class="hidden" name="backend_category" value="'+backend_category+'">'))
                    print(('<input class="hidden" name="backend_version" value="'+backend_version+'">'))
                    print('<input class="btn btn-primary" type="submit" value="INSTALL DEPS">')
                    print('</form>')
                    print('</div>')
                    print('</li>')
                    print('</ul>')
                # Next section start here
                print(('<div class="panel-heading"><h3 class="panel-title">Application Settings: '+mydomain+'/'+thesubdir+'</h3></div><div class="panel-body">'))
                print('<form id="config" class="form-inline" action="save_app_extra_settings.live.py" method="post">')
                # auth_basic
                print('<ul class="list-group"><li class="list-group-item">')
                print('<div class="row">')
                auth_basic_hint = "Setup password for "+document_root+"/"+thesubdir+" in cPanel>>Files>>Directory Privacy first"
                if auth_basic == 'enabled':
                    print_green('password protect app url', auth_basic_hint)
                    print('<div class="col-sm-6 col-radio">')
                    print('<div class="radio"><label><input type="radio" name="auth_basic" value="enabled" checked/> Enabled</label></div>')
                    print('<div class="radio"><label><input type="radio" name="auth_basic" value="disabled" /> Disabled</label></div>')
                    print('</div>')
                else:
                    print_red('password protect app url', auth_basic_hint)
                    print('<div class="col-sm-6 col-radio">')
                    print('<div class="radio"><label><input type="radio" name="auth_basic" value="enabled" /> Enabled</label></div>')
                    print('<div class="radio"><label><input type="radio" name="auth_basic" value="disabled" checked/> Disabled</label></div>')
                    print('</div>')
                    print('</div>')
                print('</li>')
                # set_expire_static
                print('<ul class="list-group"><li class="list-group-item">')
                print('<div class="row">')
                set_expire_static_hint = "Set Expires/Cache-Control headers for satic content"
                if set_expire_static == 'enabled':
                    print_green('set expires header', set_expire_static_hint)
                    print('<div class="col-sm-6 col-radio">')
                    print('<div class="radio"><label><input type="radio" name="set_expire_static" value="enabled" checked/> Enabled</label></div>')
                    print('<div class="radio"><label><input type="radio" name="set_expire_static" value="disabled" /> Disabled</label></div>')
                    print('</div>')
                else:
                    print_red('set expires header', set_expire_static_hint)
                    print('<div class="col-sm-6 col-radio">')
                    print('<div class="radio"><label><input type="radio" name="set_expire_static" value="enabled" /> Enabled</label></div>')
                    print('<div class="radio"><label><input type="radio" name="set_expire_static" value="disabled" checked/> Disabled</label></div>')
                    print('</div>')
                    print('</div>')
                print('</li>')
                # mod_security
                print('<ul class="list-group"><li class="list-group-item">')
                print('<div class="row">')
                mod_security_hint = "mod_security v3 WAF"
                if mod_security == 'enabled':
                    print_green('mod_security', mod_security_hint)
                    print('<div class="col-sm-6 col-radio">')
                    print('<div class="radio"><label><input type="radio" name="mod_security" value="enabled" checked/> Enabled</label></div>')
                    print('<div class="radio"><label><input type="radio" name="mod_security" value="disabled" /> Disabled</label></div>')
                    print('</div>')
                else:
                    print_red('mod_security', mod_security_hint)
                    print('<div class="col-sm-6 col-radio">')
                    print('<div class="radio"><label><input type="radio" name="mod_security" value="enabled" /> Enabled</label></div>')
                    print('<div class="radio"><label><input type="radio" name="mod_security" value="disabled" checked/> Disabled</label></div>')
                    print('</div>')
                    print('</div>')
                print('</li>')
                # URL Redirect
                print('<li class="list-group-item">')
                print('<div class="row">')
                url_redirect_hint = "select redirection status 301 or 307"
                if redirectstatus == 'none':
                    print_red("URL Redirect", url_redirect_hint)
                else:
                    print_green("URL Redirect", url_redirect_hint)
                print('<div class="col-sm-6 col-radio">')
                print('<select name="redirectstatus">')
                if redirectstatus == 'none':
                    print(('<option selected value="none">no redirection</option>'))
                    print(('<option value="301">Permanent Redirect</option>'))
                    print(('<option value="307">Temporary Redirect</option>'))
                elif redirectstatus == '301':
                    print(('<option value="none">no redirection</option>'))
                    print(('<option value="307">Temporary Redirect</option>'))
                    print(('<option selected value="301">Permanent Redirect</option>'))
                elif redirectstatus == '307':
                    print(('<option value="none">no redirection</option>'))
                    print(('<option selected value="307">Temporary Redirect</option>'))
                    print(('<option value="301">Permanent Redirect</option>'))
                print('</select>')
                print('</div>')
                print('</div>')
                print('</li>')
                # Append request_uri to redirect
                print('<li class="list-group-item">')
                print('<div class="row">')
                append_requesturi_hint = 'append $$request_uri to the redirect URL'
                if append_requesturi == 'enabled':
                    print_green("append $request_uri to redirecturl", append_requesturi_hint)
                    print('<div class="col-sm-6 col-radio">')
                    print('<div class="radio"><label><input type="radio" name="append_requesturi" value="enabled" checked/> Enabled</label></div>')
                    print('<div class="radio"><label><input type="radio" name="append_requesturi" value="disabled" /> Disabled</label></div>')
                    print('</div>')
                else:
                    print_red("append $request_uri to redirecturl", append_requesturi_hint)
                    print('<div class="col-sm-6 col-radio">')
                    print('<div class="radio"><label><input type="radio" name="append_requesturi" value="enabled" /> Enabled</label></div>')
                    print('<div class="radio"><label><input type="radio" name="append_requesturi" value="disabled" checked/> Disabled</label></div>')
                    print('</div>')
                    print('</div>')
                print('</li>')
                # Redirect URL
                print('<li class="list-group-item">')
                print('<div class="row">')
                redirecturl_hint = "A Valid URL, eg: http://mynewurl.tld"
                if redirecturl == "none":
                    print_red("Redirect to URL", redirecturl_hint)
                else:
                    print_green("Redirect to URL", redirecturl_hint)
                print('<div class="col-sm-6 col-radio">')
                print('<input class="form-control" placeholder='+redirecturl+' type="text" name="redirecturl">')
                print('</div>')
                print('</div>')
                print('</li>')
                # end
                print('</ul>')
                # Pass on the domain name to the next stage
                print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
                print(('<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
                print('<input class="btn btn-primary" type="submit" value="Submit">')
                print('</form>')
        else:
            print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'/'+thesubdir+'</strong></h3></div><div class="panel-body">'))
            print('<form action="subdir_select_app_settings.live.py" method="post">')
            print(('<div class="alert alert-info alert-top">To change the application server select a new category below and hit submit. All backend category other than <span class="label label-info">PROXY</span> will be directly served by high performance nginx webserver(recommended) </div>'))
            print('<select name="backend">')
            for backends_defined in backend_data_yaml_parsed.keys():
                print(('<option value="'+backends_defined+'">'+backends_defined+'</option>'))
            print('</select>')
            # Pass on the domain name to the next stage
            print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
            print(('<input class="hidden" name="thesubdir" value="'+thesubdir+'">'))
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
