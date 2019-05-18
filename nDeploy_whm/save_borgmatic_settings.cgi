#!/usr/bin/python
import cgi
import cgitb
import subprocess
import os
import yaml
import platform
import psutil
import signal


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backup_config_file = "/opt/nDeploy/conf/backup_config.yaml"
borgmatic_config_file = "/etc/borgmatic/config.yaml"

cgitb.enable()


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def safenginxreload():
    nginx_status = False
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if '/usr/sbin/nginx' in mycmdline and 'reload' in mycmdline:
            nginx_status = True
            break
    if not nginx_status:
        with open(os.devnull, 'w') as FNULL:
            subprocess.Popen(['/usr/sbin/nginx', '-s', 'reload'], stdout=FNULL, stderr=subprocess.STDOUT)


def sighupnginx():
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
            nginxpid = myprocess.pid
            os.kill(nginxpid, signal.SIGHUP)


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


def print_green(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-info" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_red(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


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

with open(borgmatic_config_file, 'r') as borgmatic_conf:
    yaml_parsed_borgmaticyaml = yaml.safe_load(borgmatic_conf)
backup_dir_list = yaml_parsed_borgmaticyaml['location']['source_directories']

if form.getvalue('repositories'):
    yaml_parsed_borgmaticyaml['location']['repositories'][0] = form.getvalue('repositories')
if form.getvalue('remote_rate_limit'):
    yaml_parsed_borgmaticyaml['storage']['remote_rate_limit'] = int(form.getvalue('remote_rate_limit'))
if form.getvalue('ssh_command'):
    yaml_parsed_borgmaticyaml['storage']['ssh_command'] = form.getvalue('ssh_command')
if form.getvalue('encryption_passphrase'):
    yaml_parsed_borgmaticyaml['storage']['encryption_passphrase'] = form.getvalue('encryption_passphrase')
if form.getvalue('keep_hourly'):
    yaml_parsed_borgmaticyaml['retention']['keep_hourly'] = form.getvalue('keep_hourly')
if form.getvalue('keep_daily'):
    yaml_parsed_borgmaticyaml['retention']['keep_daily'] = form.getvalue('keep_daily')
if form.getvalue('keep_weekly'):
    yaml_parsed_borgmaticyaml['retention']['keep_weekly'] = form.getvalue('keep_weekly')
if form.getvalue('keep_monthly'):
    yaml_parsed_borgmaticyaml['retention']['keep_monthly'] = form.getvalue('keep_monthly')
if form.getvalue('thehomedir'):
    if form.getvalue('action'):
        if form.getvalue('action') == "add":
            if form.getvalue('thehomedir') not in backup_dir_list:
                backup_dir_list.append(form.getvalue('thehomedir'))
            yaml_parsed_borgmaticyaml['location']['source_directories'] = backup_dir_list
        elif form.getvalue('action') == "delete":
            backup_dir_list.remove(form.getvalue('thehomedir'))
            yaml_parsed_borgmaticyaml['location']['source_directories'] = backup_dir_list

with open(borgmatic_config_file, 'w') as borgmatic_conf:
    yaml.dump(yaml_parsed_borgmaticyaml, borgmatic_conf, default_flow_style=False)

print('<div class="panel panel-default">')
print(('<div class="panel-heading"><h3 class="panel-title">BORGMATIC SETTINGS:</h3></div>'))
print('<div class="panel-body">')
print('<div class="icon-box">')
print('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> Borgmatic Settings updated')
print('</div>')
print('</div>')
print('</div>')

print('<div class="panel-footer"><small>')
print(branding_print_footer())
print('</small></div>')

print('</div>')  # marker3
print('</div>')  # marker2
print('</body>')
print('</html>')
