#!/usr/bin/python
import cgi
import cgitb
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

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
print('<div id="main-container" class="container text-center">')  # marker1
print('<div class="row">')  # marker2
print('<div class="col-md-6 col-md-offset-3">')  # marker3
print('<div class="logo">')
print('<a href="xtendweb.cgi" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.cgi"><span class="glyphicon glyphicon-repeat"></span></a></li>')
print('<li class="active">Server Config</li>')
print('</ol>')

if form.getvalue('mode'):
        if form.getvalue('mode') == 'restart':
                run_cmd = subprocess.Popen(installation_path+'/scripts/fix_unison_filesync.py restart', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                print('<div class="panel panel-default">')
                print(('<div class="panel-heading"><h3 class="panel-title">Command Output:</h3></div>'))
                print('<div class="panel-body">')  # marker6
                print('<ul class="list-group">')
                print(('<div class="alert alert-info alert-top">'))
                while True:
                    line = run_cmd.stdout.readline()
                    if not line:
                        break
                    print('<br>'+line)
                print(('</div>'))
                print('</ul>')
                print('</div>')  # marker6
                print('</div>')
        elif form.getvalue('mode') == 'reset':
                run_cmd = subprocess.Popen(installation_path+'/scripts/fix_unison_filesync.py reset', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                print('<div class="panel panel-default">')
                print(('<div class="panel-heading"><h3 class="panel-title">Command Output:</h3></div>'))
                print('<div class="panel-body">')  # marker6
                print('<ul class="list-group">')
                print(('<div class="alert alert-info alert-top">'))
                while True:
                        line = run_cmd.stdout.readline()
                        if not line:
                                break
                        print('<br>'+line)
                print(('</div>'))
                print('</ul>')
                print('</div>')  # marker6
                print('</div>')
else:
        print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')
print('<div class="panel-footer"><small><a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">&#8734; A U T O M 8 N</a></small></div>')
print('</div>')  # marker3
print('</div>')  # marker2
print('</body>')
print('</html>')
