#!/usr/bin/python

import cgi
import cgitb
import os
import configparser
import codecs
import subprocess

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
default_domain_data_file = installation_path+'/conf/domain_data_default.yaml'
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"


def print_forbidden():
    print(('<i class="fas fa-exclamation"></i><p>Forbidden</p>'))


def print_error(themessage):
    print(('<i class="fas fa-exclamation"></i><p>'+themessage+'</p>'))


def print_success(themessage):
    print(('<i class="fas fa-thumbs-up"></i><p>'+themessage+'</p>'))


cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('poolfile') and form.getvalue('thekey') and form.getvalue('section') and form.getvalue('action'):
    myphpini = form.getvalue('poolfile')
    mysection = int(form.getvalue('section'))
    if form.getvalue('action') == 'edit':
        if form.getvalue('thevalue'):
            if os.path.isfile(myphpini):
                config = configparser.ConfigParser()
                config.readfp(codecs.open(myphpini, 'r', 'utf8'))

                # myconfig = dict(config.items(config.sections()[0]))
                config.set(config.sections()[mysection], form.getvalue('thekey'), form.getvalue('thevalue'))
                with codecs.open(myphpini, 'w', encoding='utf8') as f:
                    config.write(f)
                if os.path.isfile('/opt/nDeploy/conf/secure-php-enabled'):
                    subprocess.call("kill -9 $(ps aux|grep php-fpm|grep secure-php-fpm.d|grep -v grep|awk '{print $2}')", shell=True)
                else:
                    subprocess.call('service ndeploy_backends restart', shell=True)
                print_success('PHP-FPM pool settings updated')
        else:
        	print_forbidden()
    elif form.getvalue('action') == 'delete':
        if os.path.isfile(myphpini):
            config = configparser.ConfigParser()
            config.readfp(codecs.open(myphpini, 'r', 'utf8'))

            # myconfig = dict(config.items(config.sections()[0]))
            config.remove_option(config.sections()[mysection], form.getvalue('thekey'))
            with codecs.open(myphpini, 'w', encoding='utf8') as f:
                config.write(f)
            if os.path.isfile('/opt/nDeploy/conf/secure-php-enabled'):
                subprocess.call("kill -9 $(ps aux|grep php-fpm|grep secure-php-fpm.d|grep -v grep|awk '{print $2}')", shell=True)
            else:
                subprocess.call('service ndeploy_backends restart', shell=True)
            print_success('PHP-FPM pool settings updated')
else:
	print_forbidden()

print('</body>')
print('</html>')
