#!/usr/bin/python

import commoninclude
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
                    p = subprocess.Popen("kill -9 $(ps aux|grep php-fpm|grep secure-php-fpm.d|grep -v grep|awk '{print $2}')", shell=True)
                else:
                    p = subprocess.Popen('service ndeploy_backends restart', shell=True)
                commoninclude.print_success('PHP-FPM pool settings updated')
        else:
            commoninclude.print_forbidden()
    elif form.getvalue('action') == 'delete':
        if os.path.isfile(myphpini):
            config = configparser.ConfigParser()
            config.readfp(codecs.open(myphpini, 'r', 'utf8'))

            # myconfig = dict(config.items(config.sections()[0]))
            config.remove_option(config.sections()[mysection], form.getvalue('thekey'))
            with codecs.open(myphpini, 'w', encoding='utf8') as f:
                config.write(f)
            if os.path.isfile('/opt/nDeploy/conf/secure-php-enabled'):
                q = subprocess.Popen("kill -9 $(ps aux|grep php-fpm|grep secure-php-fpm.d|grep -v grep|awk '{print $2}')", shell=True)
            else:
                q = subprocess.Popen('service ndeploy_backends restart', shell=True)
            commoninclude.print_success('PHP-FPM pool settings updated')
else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
