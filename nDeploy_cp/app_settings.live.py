#!/usr/bin/python
import os
import socket
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
print('<li><a href="xtendweb.live.py">Select Domain</a></li><li class="active">Application Settings</li>')
print('</ol>')
print('<div class="panel panel-default">')
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
        naxsi = yaml_parsed_profileyaml.get('naxsi', 'disabled')
        naxsi_mode = yaml_parsed_profileyaml.get('naxsi_mode', 'learn')
        naxsi_whitelist = yaml_parsed_profileyaml.get('naxsi_whitelist', 'none')
        mod_security = yaml_parsed_profileyaml.get('mod_security', 'disabled')
        lua_waf = yaml_parsed_profileyaml.get('lua_waf', 'disabled')
        auth_basic = yaml_parsed_profileyaml.get('auth_basic', 'disabled')
        set_expire_static = yaml_parsed_profileyaml.get('set_expire_static', 'disabled')
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
            print('<div class="alert alert-danger">ERROR: app template data file error</div>')
            sys.exit(0)
        # Ok we are done with getting the settings,now lets present it to the user
        print(('<div class="panel-heading"><h3 class="panel-title">Application Server: <strong>'+mydomain+'</strong></h3></div>'))
        print('<div class="panel-body">')
        print('<form id="config" class="form-inline config-save" action="select_app_settings.live.py" method="post">')
        print('<ul class="list-group">')
        if backend_category == 'PROXY':
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6 col-radio"><strong>NGINX is proxying to</strong></div>')
            print(('<div class="col-sm-6"><div class="label label-info">'+backend_version+'</div>'))
            print('</div>')
            print('</li>')
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6 col-radio"><strong>Template</strong></div>')
            print(('<div class="col-sm-6"><div class="label label-info">'+apptemplate_description+'</div>'))
        else:
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6 col-radio"><strong>native NGINX and </strong></div>')
            print(('<div class="col-sm-6"><div class="label label-info">'+backend_category+'</div>'))
            print('</div>')
            print('</li>')
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6 col-radio"><strong>Backend Version</strong></div>')
            print(('<div class="col-sm-6"><div class="label label-info">'+backend_version+'</div>'))
            print('</div>')
            print('</li>')
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6 col-radio"><strong>Template</strong></div>')
            print(('<div class="col-sm-6"><div class="label label-info">'+apptemplate_description+'</div>'))
        print('</ul>')
        print('<p><em>To change application server select a BACKEND from the drop down below:</em></p>')
        print('<select name="backend">')
        for backends_defined in backend_data_yaml_parsed.keys():
            if backends_defined == backend_category:
                print(('<option selected value="'+backends_defined+'">'+backends_defined+'</option>'))
            else:
                print(('<option value="'+backends_defined+'">'+backends_defined+'</option>'))
        print('</select>')
        # Pass on the domain name to the next stage
        print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
        print('<input class="btn btn-primary" type="submit" value="Submit">')
        print('</form>')
        print('</div>')
        print('</li>')
        print('</ul>')
        # Next section start here
        print(('<div class="panel-heading"><h3 class="panel-title">Passenger project deps installer: <strong>'+mydomain+'</strong></h3></div>'))
        print('<div class="panel-body">')
        print('<form id="config" class="form-inline config-save" action="passenger_module_installer.live.py" method="post">')
        print('<ul class="list-group">')
        if backend_category == "RUBY":
            print(('<div class="alert alert-info alert-top">Detected <span class="label label-info">RUBY</span> project, specify project dependencies in <br><br><kbd>'+ document_root +'/Gemfile</kbd></div>'))
        print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
        print('<input class="btn btn-primary" type="submit" value="INSTALL DEPS">')
        print('</form>')
        print('</div>')
        print('</li>')
        print('</ul>')
        # Next section start here
        print(('<div class="panel-heading"><h3 class="panel-title">Application Settings: '+mydomain+'</h3></div><div class="panel-body">'))
        print('<form id="config" class="form-inline" action="save_app_extra_settings.live.py" method="post">')
        # auth_basic
        print('<ul class="list-group"><li class="list-group-item">')
        print('<div class="row">')
        auth_basic_hint = "Setup password for "+document_root+" in cPanel>>Files>>Directory Privacy first"
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
        # # lua_waf
        # print('<ul class="list-group"><li class="list-group-item">')
        # print('<div class="row">')
        # lua_waf_hint = "OpenResty LUA WAF"
        # if lua_waf == 'enabled':
        #     print_green('lua_waf', lua_waf_hint)
        #     print('<div class="col-sm-6 col-radio">')
        #     print('<div class="radio"><label><input type="radio" name="lua_waf" value="enabled" checked/> Enabled</label></div>')
        #     print('<div class="radio"><label><input type="radio" name="lua_waf" value="disabled" /> Disabled</label></div>')
        #     print('</div>')
        # else:
        #     print_red('lua_waf', lua_waf_hint)
        #     print('<div class="col-sm-6 col-radio">')
        #     print('<div class="radio"><label><input type="radio" name="lua_waf" value="enabled" /> Enabled</label></div>')
        #     print('<div class="radio"><label><input type="radio" name="lua_waf" value="disabled" checked/> Disabled</label></div>')
        #     print('</div>')
        #     print('</div>')
        # print('</li>')
        # naxsi
        print('<ul class="list-group"><li class="list-group-item">')
        print('<div class="row">')
        naxsi_hint = "NAXSI is a web application firewall"
        if naxsi == 'enabled':
            print_green("naxsi", naxsi_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="naxsi" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="naxsi" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("naxsi", naxsi_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="naxsi" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="naxsi" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # naxsi_mode
        print('<li class="list-group-item">')
        print('<div class="row">')
        naxsi_mode_hint = 'active mode blocks requests, learn mode just logs it'
        if naxsi_mode == 'learn':
            print_red('naxsi_mode', naxsi_mode_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<select name="naxsi_mode">')
            print(('<option selected value="learn">learn</option>'))
            print(('<option value="active">active</option>'))
        else:
            print_green('naxsi_mode', naxsi_mode_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<select name="naxsi_mode">')
            print(('<option value="learn">learn</option>'))
            print(('<option selected value="active">active</option>'))
        print('</select>')
        print('</div>')
        print('</div>')
        print('</li>')
        # NAXSI Whitelist
        print('<li class="list-group-item">')
        print('<div class="row">')
        naxsi_whitelist_hint = 'Select community contributed NAXSI whitelist rules'
        if naxsi_whitelist == 'none':
            print_red('naxsi whitelist', naxsi_whitelist_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<select name="naxsi_whitelist">')
            print(('<option selected value="none">none</option>'))
            print(('<option value="wordpress">Wordpress</option>'))
            print(('<option value="drupal">Drupal</option>'))
        elif naxsi_whitelist == 'wordpress':
            print_green('naxsi whitelist', naxsi_whitelist_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<select name="naxsi_whitelist">')
            print(('<option value="none">none</option>'))
            print(('<option value="drupal">Drupal</option>'))
            print(('<option selected value="wordpress">Wordpress</option>'))
        elif naxsi_whitelist == 'drupal':
            print_green('naxsi whitelist', naxsi_whitelist_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<select name="naxsi_whitelist">')
            print(('<option value="none">none</option>'))
            print(('<option selected value="drupal">Drupal</option>'))
            print(('<option value="wordpress">Wordpress</option>'))
        print('</select>')
        print('</div>')
        print('</div>')
        print('</li>')
        # end
        print('</ul>')
        # Pass on the domain name to the next stage
        print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
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
