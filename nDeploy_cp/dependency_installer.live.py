#!/usr/bin/python
import os
import socket
import cgi
import cgitb
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
app_template_file = installation_path+"/conf/apptemplates.yaml"
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
print('<div class="col-md-6 col-md-offset-3">')
print('<div class="logo">')
print('<a href="xtendweb.live.py" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.live.py"><span class="glyphicon glyphicon-repeat"></span></a></li>')
print('<li><a href="xtendweb.live.py">Select Domain</a></li><li class="active">Passenger Module Installer</li>')
print('</ol>')
if form.getvalue('domain') and form.getvalue('backend_category') and form.getvalue('backend_version') and form.getvalue('document_root'):
    mydomain = form.getvalue('domain')
    mybackend = form.getvalue('backend_category')
    mybackendversion = form.getvalue('backend_version')
    mydocroot = form.getvalue('document_root')
    print(('<div class="alert alert-warning alert-domain"><strong>'+mydomain+'</strong></div>'))
    print('<div class="panel panel-default">')  # marker3
    print(('<div class="panel-heading"><h3 class="panel-title">Project</h3></div>'))
    print('<div class="panel-body">')  # marker4
    print('<div class="alert alert-success alert-btm">')  # marker5
    print(('<span class="label label-success">'+mybackend+'</span> <span class="label label-success">'+mybackendversion+'</span>'))
    print(('<br><br><span class="label label-success">Project root: '+mydocroot+'</span>'))
    print('</div>')  # marker5
    print('</div>')  # marker4
    print('</div>')  # marker3
    if mybackend == 'RUBY':
        if os.path.isfile(mydocroot+'/Gemfile'):
            if os.path.isfile('/usr/local/rvm/gems/'+mybackendversion+'/bin/bundle'):
                install_cmd = '/usr/local/rvm/bin/rvm '+mybackendversion+' do bundle install --path vendor/bundle'
                myinstaller = subprocess.Popen(install_cmd, cwd=mydocroot, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
                print('<div class="panel panel-default">')
                print(('<div class="panel-heading"><h3 class="panel-title">Command Output:</h3></div>'))
                print('<div class="panel-body">')  # marker6
                print(('<div class="alert alert-info alert-btm">'))
                while True:
                    line = myinstaller.stdout.readline()
                    if not line:
                        break
                    print('<br>'+line)
                print(('</div>'))
                print(('<div class="alert alert-info alert-btm">'))  # marker8
                print(('If the install failed run the following command in your shell to proceed with manual installation:<br>'))
                print(('cd '+mydocroot+'<br>'))
                print(('/usr/local/rvm/bin/rvm '+mybackendversion+' do bundle install --path vendor/bundle'))
                print('</div>')  # marker8
                print('</div>')  # marker6
                print('</div>')
            else:
                print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> bundler command not found</div>')
        else:
            print('<div class="panel panel-default">')
            print(('<div class="panel-heading"><h3 class="panel-title">Installer Error</h3></div>'))
            print('<div class="panel-body">')  # marker4
            print(('<div class="alert alert-warning alert-btm">Gemfile not found for <span class="label label-warning">RUBY</span> project, specify project dependencies in <br><kbd>' + mydocroot + '/Gemfile</kbd></div>'))
            print('</div>')  # marker4
            print('</div>')
    elif mybackend == 'NODEJS':
        if os.path.isfile(mydocroot+'/package.json'):
            if os.path.isfile('/usr/local/nvm/versions/node/'+mybackendversion+'/bin/npm'):
                install_cmd = '/usr/local/nvm/versions/node/'+mybackendversion+'/bin/npm -q install --production'
                my_env = os.environ.copy()
                my_env["PATH"] = "/usr/local/nvm/versions/node/"+mybackendversion+"/bin:"+my_env["PATH"]
                myinstaller = subprocess.Popen(install_cmd, cwd=mydocroot, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=my_env, shell=True, universal_newlines=True)
                print('<div class="panel panel-default">')
                print(('<div class="panel-heading"><h3 class="panel-title">Command Output:</h3></div>'))
                print('<div class="panel-body">')  # marker6
                print(('<div class="alert alert-info alert-btm">'))
                while True:
                    line = myinstaller.stdout.readline()
                    if not line:
                        break
                    print('<br>'+line)
                print(('</div>'))
                print(('<div class="alert alert-info alert-btm">'))  # marker8
                print(('If the install failed run the following command in your shell to proceed with manual installation:<br>'))
                print(('export PATH="/usr/local/nvm/versions/node/'+mybackendversion+'/bin:$PATH"<br>'))
                print(('cd '+mydocroot))
                print(('<br>npm install --production'))
                print('</div>')  # marker8
                print('</div>')  # marker6
                print('</div>')
            else:
                print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> npm command not found</div>')
        else:
            print('<div class="panel panel-default">')
            print(('<div class="panel-heading"><h3 class="panel-title">Installer Error</h3></div>'))
            print('<div class="panel-body">')  # marker4
            print(('<div class="alert alert-warning alert-btm">package.json not found for <span class="label label-warning">NODEJS</span> project, specify project dependencies in <br><kbd>'+mydocroot+'/package.json</kbd></div>'))
            print('</div>')  # marker4
            print('</div>')
    elif mybackend == 'PYTHON':
        if os.path.isfile(mydocroot+'/requirements.txt'):
            if os.path.isfile('/usr/local/pythonz/pythons/'+mybackendversion+'/bin/pip'):
                install_cmd = '/usr/local/pythonz/pythons/'+mybackendversion+'/bin/pip install --user -r requirements.txt'
                myinstaller = subprocess.Popen(install_cmd, cwd=mydocroot, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
                print('<div class="panel panel-default">')
                print(('<div class="panel-heading"><h3 class="panel-title">Command Output:</h3></div>'))
                print('<div class="panel-body">')  # marker6
                print(('<div class="alert alert-info alert-btm">'))
                while True:
                    line = myinstaller.stdout.readline()
                    if not line:
                        break
                    print('<br>'+line)
                print(('</div>'))
                print(('<div class="alert alert-info alert-btm">'))  # marker8
                print(('If the install failed run the following command in your shell to proceed with manual installation:<br>'))
                print(('export PATH="/usr/local/pythonz/pythons/'+mybackendversion+'/bin:$PATH"<br>'))
                print(('cd '+mydocroot))
                print(('<br>pip install --user -r requirements.txt'))
                print('</div>')  # marker8
                print('</div>')  # marker6
                print('</div>')
            else:
                print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> pip command not found</div>')
        else:
            print('<div class="panel panel-default">')
            print(('<div class="panel-heading"><h3 class="panel-title">Installer Error</h3></div>'))
            print('<div class="panel-body">')  # marker4
            print(('<div class="alert alert-warning alert-btm">requirements.txt not found for <span class="label label-warning">PYTHON</span> project, specify project dependencies in <br><kbd>'+mydocroot+'/requirements.txt</kbd></div>'))
            print('</div>')  # marker4
            print('</div>')
    elif mybackend == 'PHP':
        if os.path.isfile(mydocroot+'/composer.json'):
            if os.path.isfile('/opt/cpanel/composer/bin/composer'):
                install_cmd = '/usr/local/bin/php -d allow_url_fopen=1 -d detect_unicode=0 /opt/cpanel/composer/bin/composer install'
                myinstaller = subprocess.Popen(install_cmd, cwd=mydocroot, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
                print('<div class="panel panel-default">')
                print(('<div class="panel-heading"><h3 class="panel-title">Command Output:</h3></div>'))
                print('<div class="panel-body">')  # marker6
                print(('<div class="alert alert-info alert-btm">'))
                while True:
                    line = myinstaller.stdout.readline()
                    if not line:
                        break
                    print('<br>'+line)
                print(('</div>'))
                print(('<div class="alert alert-info alert-btm">'))  # marker8
                print(('If the install failed run the following command in your shell to proceed with manual installation:<br>'))
                print(('export PATH="$PATH:/opt/cpanel/composer/bin"<br>'))
                print(('cd '+mydocroot))
                print(('<br>/usr/local/bin/php -d allow_url_fopen=1 -d detect_unicode=0 /opt/cpanel/composer/bin/composer install'))
                print('</div>')  # marker8
                print('</div>')  # marker6
                print('</div>')
            else:
                print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> composer command not found</div>')
        else:
            print('<div class="panel panel-default">')
            print(('<div class="panel-heading"><h3 class="panel-title">Installer Error</h3></div>'))
            print('<div class="panel-body">')  # marker4
            print(('<div class="alert alert-warning alert-btm">composer.json not found for <span class="label label-warning">PHP</span> project, specify project dependencies in <br><kbd>'+mydocroot+'/composer.json</kbd></div>'))
            print('</div>')  # marker4
            print('</div>')
else:
    print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden</div>')
print('<div class="panel-footer"><small><a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">&#8734; A U T O M 8 N</a></small></div>')
print('</div>')  # marker3
print('</div>')  # marker2
print('</body>')
print('</html>')
