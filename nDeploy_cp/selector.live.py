#!/usr/bin/python
import os
import socket
import cgi
import cgitb


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
print('<li><a href="xtendweb.live.py">Set Domain</a></li><li class="active">Server Options</li>')
print('</ol>')
print('<div id="config" class="panel panel-default">')
if form.getvalue('domain'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'</strong></h3></div><div class="panel-body">'))
    print('<div class="row">')
    print('<div class="col-sm-6">')
    print('<form action="server_settings.live.py" method="post">')
    print('<input class="btn btn-primary" data-toggle="tooltip" title="content optimizations, redirections, server headers" type="submit" value="SERVER SETTINGS">')
    # Pass on the domain name to the next stage
    print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
    print('</form>')
    print('</div>')
    print('<div class="col-sm-6">')
    print('<form action="app_settings.live.py" method="post">')
    print('<input class="btn btn-primary" data-toggle="tooltip" title="application server, version, application template" type="submit" value="APPLICATION SETTINGS">')
    # Pass on the domain name to the next stage
    print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
    print('</form>')
    print('</div>')
    print('<div class="col-sm-6">')
    print('<form action="subdir_selector.live.py" method="post">')
    print('<input class="btn btn-primary" data-toggle="tooltip" title="application installed in sub-directory like domain.com/blog/" type="submit" value="SUBDIR APPS">')
    # Pass on the domain name to the next stage
    print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
    print('</form>')
    print('</div>')
    print('<div class="col-sm-6">')
    print('<form action="directory_privacy.live.py" method="post">')
    print('<input class="btn btn-primary" data-toggle="tooltip" title="password protected URL" type="submit" value="PASSWORD PROTECTED URL">')
    # Pass on the domain name to the next stage
    print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
    print('</form>')
    print('</div>')
    print('</div>')
else:
    print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> domain-data file i/o error</div>')
print('</div>')
print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
