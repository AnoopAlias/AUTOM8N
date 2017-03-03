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
            subdir_apps_dict[thesubdir] = the_subdir_dict
            yaml_parsed_profileyaml['subdir_apps'] = subdir_apps_dict
        else:
            print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Missing subdir::'+thesubdir+' in domain data</div>')
    else:
        print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Missing subdir_apps section in domain data</div>')
else:
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
