#!/usr/bin/python
import os
import socket
import yaml
import cgi
import cgitb
import sys
import re

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
app_template_file = installation_path+"/conf/apptemplates.yaml"


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
print('<a href="xtendweb.live.py" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-cog" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.live.py"><span class="glyphicon glyphicon-home"></span></a></li>')
print('<li><a href="xtendweb.live.py">Select Domain</a></li><li class="active">Server Settings</li>')
print('</ol>')
print('<div class="panel panel-default">')
# Get the domain name
if 'domain' in form.keys():
    mydomain = form.getvalue('domain')
else:
    print('ERROR: Forbidden::domain')
    print('</div>')
    print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
    print('</div>')
    print('</div>')
    print('</div>')
    print('</div>')
    print('</body>')
    print('</html>')
    sys.exit(0)
# Getting the current domain data
profileyaml = installation_path + "/domain-data/" + mydomain
if os.path.isfile(profileyaml):
    # Get all config settings from the domains domain-data config file
    with open(profileyaml, 'r') as profileyaml_data_stream:
        yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
else:
    print('ERROR: Domain data file i/o error')
    print('</div>')
    print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
    print('</div>')
    print('</div>')
    print('</div>')
    print('</div>')
    print('</body>')
    print('</html>')
    sys.exit(0)
if form.getvalue('thesubdir'):
    thesubdir = form.getvalue('thesubdir')
    subdir_apps_dict = yaml_parsed_profileyaml.get('subdir_apps')
    if subdir_apps_dict:
        if subdir_apps_dict.get(thesubdir):
            the_subdir_dict = subdir_apps_dict.get(thesubdir)
            current_redirecturl = the_subdir_dict.get('redirecturl', "none")
            # auth_basic
            if 'auth_basic' in form.keys():
                auth_basic = form.getvalue('auth_basic')
                the_subdir_dict['auth_basic'] = auth_basic
            else:
                print('ERROR: Forbidden::auth_basic')
                print('</div>')
                print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</body>')
                print('</html>')
                sys.exit(0)
            # set_expire_static
            if 'set_expire_static' in form.keys():
                set_expire_static = form.getvalue('set_expire_static')
                the_subdir_dict['set_expire_static'] = set_expire_static
            else:
                print('ERROR: Forbidden::set_expire_static')
                print('</div>')
                print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</body>')
                print('</html>')
                sys.exit(0)
            # mod_security
            if 'mod_security' in form.keys():
                mod_security = form.getvalue('mod_security')
                the_subdir_dict['mod_security'] = mod_security
            else:
                print('ERROR: Forbidden::mod_security')
                print('</div>')
                print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</body>')
                print('</html>')
                sys.exit(0)
            # lua_waf
            if 'lua_waf' in form.keys():
                lua_waf = form.getvalue('lua_waf')
                the_subdir_dict['lua_waf'] = lua_waf
            else:
                print('ERROR: Forbidden::lua_waf')
                print('</div>')
                print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</body>')
                print('</html>')
                sys.exit(0)
            # naxsi
            if 'naxsi' in form.keys():
                naxsi = form.getvalue('naxsi')
                the_subdir_dict['naxsi'] = naxsi
            else:
                print('ERROR: Forbidden::naxsi')
                print('</div>')
                print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</body>')
                print('</html>')
                sys.exit(0)
            # naxsi_mode
            if 'naxsi_mode' in form.keys():
                naxsi_mode = form.getvalue('naxsi_mode')
                the_subdir_dict['naxsi_mode'] = naxsi_mode
            else:
                print('ERROR: Forbidden::naxsi_mode')
                print('</div>')
                print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</body>')
                print('</html>')
                sys.exit(0)
            # naxsi_whitelist
            if 'naxsi_whitelist' in form.keys():
                naxsi_whitelist = form.getvalue('naxsi_whitelist')
                the_subdir_dict['naxsi_whitelist'] = naxsi_whitelist
            else:
                print('ERROR: Forbidden::naxsi_whitelist')
                print('</div>')
                print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</body>')
                print('</html>')
                sys.exit(0)
            # redirectstatus
            if 'redirectstatus' in form.keys():
                redirectstatus = form.getvalue('redirectstatus')
                the_subdir_dict['redirectstatus'] = redirectstatus
            else:
                print('ERROR: Forbidden::redirectstatus')
                print('</div>')
                print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</body>')
                print('</html>')
                sys.exit(0)
            # redirecturl
            if redirectstatus != "none":
                if 'redirecturl' in form.keys():
                    redirecturl = form.getvalue('redirecturl')
                    if not redirecturl == "none":
                        regex = re.compile(
                            r'^(?:http|ftp)s?://'
                            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                            r'localhost|'
                            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                            r'(?::\d+)?'
                            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                        it_matches = regex.match(redirecturl)
                        if not it_matches:
                            print('ERROR: Invalid Redirect URL. The URL must be something like https://google.com ')
                            print('</div>')
                            print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
                            print('</div>')
                            print('</div>')
                            print('</div>')
                            print('</div>')
                            print('</body>')
                            print('</html>')
                            sys.exit(0)
                        else:
                            the_subdir_dict['redirecturl'] = redirecturl
                    else:
                        the_subdir_dict['redirecturl'] = current_redirecturl
            # append_requesturi
            if 'append_requesturi' in form.keys():
                append_requesturi = form.getvalue('append_requesturi')
                the_subdir_dict['append_requesturi'] = append_requesturi
            else:
                print('ERROR: Forbidden::append_requesturi')
                print('</div>')
                print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</body>')
                print('</html>')
                sys.exit(0)
            subdir_apps_dict[thesubdir] = the_subdir_dict
            yaml_parsed_profileyaml['subdir_apps'] = subdir_apps_dict
        else:
            print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Missing subdir::'+thesubdir+' in domain data</div>')
    else:
        print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Missing subdir_apps section in domain data</div>')
else:
    # auth_basic
    if 'auth_basic' in form.keys():
        auth_basic = form.getvalue('auth_basic')
        yaml_parsed_profileyaml['auth_basic'] = auth_basic
    else:
        print('ERROR: Forbidden::auth_basic')
        print('</div>')
        print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</body>')
        print('</html>')
        sys.exit(0)
    # set_expire_static
    if 'set_expire_static' in form.keys():
        set_expire_static = form.getvalue('set_expire_static')
        yaml_parsed_profileyaml['set_expire_static'] = set_expire_static
    else:
        print('ERROR: Forbidden::set_expire_static')
        print('</div>')
        print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</body>')
        print('</html>')
        sys.exit(0)
    # mod_security
    if 'mod_security' in form.keys():
        mod_security = form.getvalue('mod_security')
        yaml_parsed_profileyaml['mod_security'] = mod_security
    else:
        print('ERROR: Forbidden::mod_security')
        print('</div>')
        print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</body>')
        print('</html>')
        sys.exit(0)
    # lua_waf
    if 'lua_waf' in form.keys():
        lua_waf = form.getvalue('lua_waf')
        yaml_parsed_profileyaml['lua_waf'] = lua_waf
    else:
        print('ERROR: Forbidden::lua_waf')
        print('</div>')
        print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</body>')
        print('</html>')
        sys.exit(0)
    # naxsi
    if 'naxsi' in form.keys():
        naxsi = form.getvalue('naxsi')
        yaml_parsed_profileyaml['naxsi'] = naxsi
    else:
        print('ERROR: Forbidden::naxsi')
        print('</div>')
        print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</body>')
        print('</html>')
        sys.exit(0)
    # naxsi_mode
    if 'naxsi_mode' in form.keys():
        naxsi_mode = form.getvalue('naxsi_mode')
        yaml_parsed_profileyaml['naxsi_mode'] = naxsi_mode
    else:
        print('ERROR: Forbidden::naxsi_mode')
        print('</div>')
        print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</body>')
        print('</html>')
        sys.exit(0)
    # naxsi_whitelist
    if 'naxsi_whitelist' in form.keys():
        naxsi_whitelist = form.getvalue('naxsi_whitelist')
        yaml_parsed_profileyaml['naxsi_whitelist'] = naxsi_whitelist
    else:
        print('ERROR: Forbidden::naxsi_whitelist')
        print('</div>')
        print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</div>')
        print('</body>')
        print('</html>')
        sys.exit(0)
if form.getvalue('thesubdir'):
    print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'/'+form.getvalue('thesubdir')+'</strong></h3></div><div class="panel-body">'))
else:
    print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'</strong></h3></div><div class="panel-body">'))
with open(profileyaml, 'w') as yaml_file:
    yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
print('<div class="icon-box">')
print('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> Server Settings updated')
print('</div>')
print('</div>')
print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
