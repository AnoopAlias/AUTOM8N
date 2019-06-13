#!/usr/bin/python

import commoninclude
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
print('</head>')
print('<body>')

if form.getvalue('domain') and form.getvalue('backend_category') and form.getvalue('backend_version') and form.getvalue('document_root'):
    mydomain = form.getvalue('domain')
    mybackend = form.getvalue('backend_category')
    mybackendversion = form.getvalue('backend_version')
    mydocroot = form.getvalue('document_root')
    print(('<p class="text-left">Project root: <kbd>'+mydocroot+'</<kbd></p>'))
    if mybackend == 'RUBY':
        if os.path.isfile(mydocroot+'/Gemfile'):
            if os.path.isfile('/usr/local/rvm/gems/'+mybackendversion+'/bin/bundle'):
                install_cmd = '/usr/local/rvm/bin/rvm '+mybackendversion+' do bundle install --path vendor/bundle'
                myinstaller = subprocess.Popen(install_cmd, cwd=mydocroot, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
                print('<ul class="list-unstyled text-left">')
                while True:
                    line = myinstaller.stdout.readline()
                    if not line:
                        break
                    print('<li class="mb-1">'+line+'</li>')
                print('</ul>')
                print('<div class="alert alert-info">')
                print('<p>If the install failed run the following command in your shell to proceed with manual installation:<p>')
                print('<ul class="list-unstyled text-left">')
                print(('<li class="mb-1">cd '+mydocroot+'</li>'))
                print(('<li class="mb-1">/usr/local/rvm/bin/rvm '+mybackendversion+' do bundle install --path vendor/bundle</li>'))
                print('</ul>')
                print('</div>')
            else:
                commoninclude.print_error('bundler command not found')
        else:
            commoninclude.print_error_alert(('<p>Gemfile not found for <span class="badge badge-warning">RUBY</span> project.</p><ul class="list list-unstyled mb-0"><li>Specify project dependencies in:</li><li><kbd>' + mydocroot + '/Gemfile</kbd></li></ul>'))
    elif mybackend == 'NODEJS':
        if os.path.isfile(mydocroot+'/package.json'):
            if os.path.isfile('/usr/local/nvm/versions/node/'+mybackendversion+'/bin/npm'):
                install_cmd = '/usr/local/nvm/versions/node/'+mybackendversion+'/bin/npm -q install --production'
                my_env = os.environ.copy()
                my_env["PATH"] = "/usr/local/nvm/versions/node/"+mybackendversion+"/bin:"+my_env["PATH"]
                myinstaller = subprocess.Popen(install_cmd, cwd=mydocroot, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=my_env, shell=True, universal_newlines=True)
                print('<ul class="list-unstyled text-left">')
                while True:
                    line = myinstaller.stdout.readline()
                    if not line:
                        break
                    print('<li class="mb-1">'+line+'</li>')
                print('</ul>')
                print('<div class="alert alert-info">')
                print('<p>If the install failed run the following command in your shell to proceed with manual installation:<p>')
                print('<ul class="list list-unstyled mb-0">')
                print(('<li>export PATH="/usr/local/nvm/versions/node/'+mybackendversion+'/bin:$PATH"</li>'))
                print(('<li>cd '+mydocroot+'<li>'))
                print(('<li>npm install --production</li>'))
                print('</ul>')
                print('</div>')
            else:
                commoninclude.print_error('npm command not found')
        else:
            commoninclude.print_error_alert(('<p>package.json not found for <span class="badge badge-warning">NODEJS</span> project.</p><ul class="list list-unstyled mb-0"><li>Specify project dependencies in:<li></li><kbd>'+mydocroot+'/package.json</kbd></li></ul>'))
    elif mybackend == 'PYTHON':
        if os.path.isfile(mydocroot+'/requirements.txt'):
            if os.path.isfile('/usr/local/pythonz/pythons/'+mybackendversion+'/bin/pip'):
                install_cmd = '/usr/local/pythonz/pythons/'+mybackendversion+'/bin/pip install --user -r requirements.txt'
                myinstaller = subprocess.Popen(install_cmd, cwd=mydocroot, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
                print('<ul class="list-unstyled text-left">')
                while True:
                    line = myinstaller.stdout.readline()
                    if not line:
                        break
                    print('<li class="mb-1">'+line+'</li>')
                print('</ul>')
                print('<div class="alert alert-info">')
                print('<p>If the install failed run the following command in your shell to proceed with manual installation:</p>')
                print('<ul class="list list-unstyled mb-0">')
                print(('<li>export PATH="/usr/local/pythonz/pythons/'+mybackendversion+'/bin:$PATH"</li>'))
                print(('<li>cd '+mydocroot+'</li>'))
                print('<li>pip install --user -r requirements.txt</li>')
                print('</ul>')
                print('</div>')
            else:
                commoninclude.print_error('pip command not found')
        else:
            commoninclude.print_error_alert(('<p>requirements.txt not found for <span class="badge badge-warning">PYTHON</span> project</p><ul class="list list-unstyled mb-0"><li>Specify project dependencies in:</li><li><kbd>'+mydocroot+'/requirements.txt</kbd><li></ul>'))
    elif mybackend == 'PHP':
        if os.path.isfile(mydocroot+'/composer.json'):
            if os.path.isfile('/opt/cpanel/composer/bin/composer'):
                install_cmd = '/usr/local/bin/php -d allow_url_fopen=1 -d detect_unicode=0 /opt/cpanel/composer/bin/composer install'
                myinstaller = subprocess.Popen(install_cmd, cwd=mydocroot, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
                print('<ul class="list-unstyled text-left">')
                while True:
                    line = myinstaller.stdout.readline()
                    if not line:
                        break
                    print('<br>'+line)
                print('</ul>')
                print('<div class="alert alert-info">')
                print('<p>If the install failed run the following command in your shell to proceed with manual installation:</p>')
                print('<ul class="list list-unstyled mb-0">')
                print(('<li>export PATH="$PATH:/opt/cpanel/composer/bin"</li>'))
                print(('<li>cd '+mydocroot+'</li>'))
                print(('<li>/usr/local/bin/php -d allow_url_fopen=1 -d detect_unicode=0 /opt/cpanel/composer/bin/composer install</li>'))
                print('</ul>')
                print('</div>')
            else:
                commoninclude.print_error('composer command not found')
        else:
            commoninclude.print_error_alert(('<p>composer.json not found for <span class="badge badge-warning">PHP</span> project.</p><ul class="list list-unstyled mb-0"><li>Specify project dependencies in:</li><li><kbd>'+mydocroot+'/composer.json</kbd></li></ul>'))
else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
