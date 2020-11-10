#!/usr/bin/env python3

import os
import cgi
import cgitb
from commoninclude import print_simple_header, print_simple_footer, close_cpanel_liveapisock, print_success, print_error, terminal_call, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


cgitb.enable()

close_cpanel_liveapisock()
form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('domain') and form.getvalue('backend_category') and form.getvalue('backend_version') and form.getvalue('document_root'):
    mydomain = form.getvalue('domain')
    mybackend = form.getvalue('backend_category')
    mybackendversion = form.getvalue('backend_version')
    mydocroot = form.getvalue('document_root')
    terminal_call('','Project root: '+mydocroot,'')

    if mybackend == 'RUBY':

        if os.path.isfile(mydocroot+'/Gemfile'):

            if os.path.isfile('/usr/local/rvm/gems/'+mybackendversion+'/bin/bundle'):
                install_cmd = '/usr/local/rvm/bin/rvm '+mybackendversion+' do bundle install --path vendor/bundle'
                terminal_call(install_cmd, 'Installing Ruby project dependencies','Ruby project dependencies install complete!','',mydocroot)
                terminal_call('','','If the install failed, run the following command in your shell to proceed with manual installation: <kbd>cd '+mydocroot+';/usr/local/rvm/bin/rvm '+mybackendversion+' do bundle install --path vendor/bundle</kbd>')
                print_success('Ruby project dependencies install complete!')
            else:
                print_error('Bundler command not found!')

        else:
            terminal_call('','','Gemfile not found for <kbd>RUBY</kbd> project. Specify project dependencies in: '+mydocroot+'/Gemfile')
            print_error('Gemfile not found!')

    elif mybackend == 'NODEJS':

        if os.path.isfile(mydocroot+'/package.json'):
            if os.path.isfile('/usr/local/nvm/versions/node/'+mybackendversion+'/bin/npm'):
                install_cmd = '/usr/local/nvm/versions/node/'+mybackendversion+'/bin/npm -q install --production'
                my_env = os.environ.copy()
                my_env["PATH"] = "/usr/local/nvm/versions/node/"+mybackendversion+"/bin:"+my_env["PATH"]
                terminal_call(install_cmd, 'Installing NodeJS project dependencies','NodeJS project dependencies install complete!', my_env, mydocroot)
                terminal_call('','','If the install failed, run the following command in your shell to proceed with manual installation: <kbd>export PATH="/usr/local/nvm/versions/node/'+mybackendversion+'/bin:$PATH";cd '+mydocroot+';npm install --production</kbd>')
                print_success('NodeJS project dependencies install complete!')
            else:
                print_error('NPM command not found!')

        else:
            terminal_call('','','package.json not found for <kbd>NODEJS</kbd> project. Specify project dependencies in: '+mydocroot+'/package.json')
            print_error('package.json not found!')

    elif mybackend == 'PYTHON':

        if os.path.isfile(mydocroot+'/requirements.txt'):
            if os.path.isfile('/usr/local/pythonz/pythons/'+mybackendversion+'/bin/pip'):
                install_cmd = '/usr/local/pythonz/pythons/'+mybackendversion+'/bin/pip install --user -r requirements.txt'
                terminal_call(install_cmd, 'Installing Python project dependencies','Python project dependencies install complete!','', mydocroot)
                terminal_call('','','If the install failed, run the following command in your shell to proceed with manual installation: <kbd>export PATH="/usr/local/pythonz/pythons/'+mybackendversion+'/bin:$PATH";cd '+mydocroot+';pip install --user -r requirements.txt</kbd>')
                print_success('Python project dependencies install complete!')
            else:
                print_error('PIP command not found!')

        else:
            terminal_call('','','requirements.txt not found for <kbd>PYTHON</kbd> project. Specify project dependencies in: '+mydocroot+'/requirements.txt')
            print_error('requirements.txt not found!')

    elif mybackend == 'PHP':

        if os.path.isfile(mydocroot+'/composer.json'):
            if os.path.isfile('/opt/cpanel/composer/bin/composer'):
                install_cmd = '/usr/local/bin/php -d allow_url_fopen=1 -d detect_unicode=0 /opt/cpanel/composer/bin/composer install'
                terminal_call(install_cmd, 'Installing PHP project dependencies','PHP project dependencies install complete!','', mydocroot)
                terminal_call('','','If the install failed, run the following command in your shell to proceed with manual installation: <kbd>export PATH="$PATH:/opt/cpanel/composer/bin";cd '+mydocroot+';/usr/local/bin/php -d allow_url_fopen=1 -d detect_unicode=0 /opt/cpanel/composer/bin/composer install</kbd>','',mydocroot)
                print_success('PHP project dependencies install complete!')
            else:
                print_error('Composer command not found!')

        else:
            terminal_call('','','composer.json not found for <kbd>PHP</kbd> project. Specify project dependencies in: '+mydocroot+'/composer.json')
            print_error('composer.json not found!')

else:
    print_forbidden()

print_simple_footer()
