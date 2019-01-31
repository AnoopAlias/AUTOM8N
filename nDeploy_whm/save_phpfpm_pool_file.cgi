#!/usr/bin/python
import cgi
import cgitb
import os
import configparser
import codecs
import subprocess
import yaml


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
default_domain_data_file = installation_path+'/conf/domain_data_default.yaml'
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"


def branding_print_logo_name():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_logo = yaml_parsed_brand.get("brand_logo", "xtendweb.png")
    else:
        brand_logo = "xtendweb.png"
    return brand_logo


def branding_print_banner():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_name = yaml_parsed_brand.get("brand", "AUTOM8N")
    else:
        brand_name = "AUTOM8N"
    return brand_name


def branding_print_footer():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_footer = yaml_parsed_brand.get("brand_footer", '<a target="_blank" href="https://autom8n.com">A U T O M 8 N</a>')
    else:
        brand_footer = '<a target="_blank" href="https://autom8n.com">A U T O M 8 N</a>'
    return brand_footer


cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')

print('<title>')
print(branding_print_banner())
print('</title>')

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
print('<a href="xtendweb.cgi"><img border="0" src="')
print(branding_print_logo_name())
print('" width="48" height="48"></a>')
print('<h4>')
print(branding_print_banner())
print('</h4>')
print('</div>')

print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.cgi"><span class="glyphicon glyphicon-repeat"></span></a></li>')
print('<li class="active">Server Config</li>')
print('</ol>')

if form.getvalue('poolfile') and form.getvalue('thekey') and form.getvalue('section') and form.getvalue('action'):
    myphpini = form.getvalue('poolfile')
    mysection = int(form.getvalue('section'))
    if form.getvalue('action') == 'edit':
        if form.getvalue('thevalue'):
            if os.path.isfile(myphpini):
                config = configparser.ConfigParser()
                config.readfp(codecs.open(myphpini, 'r', 'utf8'))
                # Next section start here
                print('<div class="panel panel-default">')  # marker6
                print('<div class="panel-heading"><h3 class="panel-title">Edit PHP-FPM pool: '+config.sections()[mysection]+'</h3></div>')
                print('<div class="panel-body">')  # marker7
                # myconfig = dict(config.items(config.sections()[0]))
                config.set(config.sections()[mysection], form.getvalue('thekey'), form.getvalue('thevalue'))
                with codecs.open(myphpini, 'w', encoding='utf8') as f:
                    config.write(f)
                if os.path.isfile('/opt/nDeploy/conf/secure-php-enabled'):
                    subprocess.call("kill -9 $(ps aux|grep php-fpm|grep secure-php-fpm.d|grep -v grep|awk '{print $2}')", shell=True)
                else:
                    subprocess.call('service ndeploy_backends restart', shell=True)
                print('<div class="icon-box">')
                print('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> PHP-FPM pool settings updated')
                print('</div>')
                print('</div>')  # div8
                print('</div>')  # div7
        else:
            print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')
    elif form.getvalue('action') == 'delete':
        if os.path.isfile(myphpini):
            config = configparser.ConfigParser()
            config.readfp(codecs.open(myphpini, 'r', 'utf8'))
            # Next section start here
            print('<div class="panel panel-default">')  # marker6
            print('<div class="panel-heading"><h3 class="panel-title">Edit PHP-FPM pool: '+config.sections()[mysection]+'</h3></div>')
            print('<div class="panel-body">')  # marker7
            # myconfig = dict(config.items(config.sections()[0]))
            config.remove_option(config.sections()[mysection], form.getvalue('thekey'))
            with codecs.open(myphpini, 'w', encoding='utf8') as f:
                config.write(f)
            if os.path.isfile('/opt/nDeploy/conf/secure-php-enabled'):
                subprocess.call("kill -9 $(ps aux|grep php-fpm|grep secure-php-fpm.d|grep -v grep|awk '{print $2}')", shell=True)
            else:
                subprocess.call('service ndeploy_backends restart', shell=True)
            print('<div class="icon-box">')
            print('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> PHP-FPM pool settings updated')
            print('</div>')
            print('</div>')  # div8
            print('</div>')  # div7
else:
        print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')

print('<div class="panel-footer"><small>')
print(branding_print_footer())
print('</small></div>')

print('</div>')  # marker3
print('</div>')  # marker2
print('</body>')
print('</html>')
