#!/usr/bin/python
import cgi
import cgitb
import subprocess
import os
import yaml
import platform
import psutil
import signal
import jinja2
import codecs
import sys
import re

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backup_config_file = "/opt/nDeploy/conf/backup_config.yaml"

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

if form.getvalue('system_files') and form.getvalue('mysql_backup'):
    system_files = form.getvalue('system_files')
    mysql_backup = form.getvalue('mysql_backup')
    # Check if backup config file is present or initilize otherwise
    if os.path.isfile(backup_config_file):
        # Get all config settings from the backup config file
        with open(backup_config_file, 'r') as backup_config_file_stream:
            yaml_parsed_backupyaml = yaml.safe_load(backup_config_file_stream)
        yaml_parsed_backupyaml['system_files'] = system_files
        yaml_parsed_backupyaml['mysql_backup'] = mysql_backup
        if form.getvalue('backup_path'):
            if not form.getvalue('backup_path').startswith('/'):
                backup_path_pass1 = '/'+form.getvalue('backup_path')
            else:
                backup_path_pass1 = form.getvalue('backup_path')
            if backup_path_pass1.endswith('/'):
                backup_path = backup_path_pass1[:-1]
            else:
                backup_path = backup_path_pass1
            if not backup_path:
                print('ERROR: Invalid backup_path')
                sys.exit(0)
            if not re.match("^[\.0-9a-zA-Z/_-]*$", backup_path):
                print("Error: Invalid char in backup_path")
                sys.exit(0)
            yaml_parsed_backupyaml['backup_path'] = backup_path
        else:
            backup_path = yaml_parsed_backupyaml.get('backup_path')
        with open(backup_config_file, 'w') as new_backup_config_file:
            yaml.dump(yaml_parsed_backupyaml, new_backup_config_file, default_flow_style=False)
        # We create the borgmatic hook now
        # Initiate Jinja2 templateEnv
        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        templateVars = {"BACKUP_PATH": backup_path,
                        "SYSTEM_FILES": system_files,
                        "MYSQL_BACKUP": mysql_backup
                        }
        borgmatic_hook_template = templateEnv.get_template("borgmatic_cpanel_backup_hook.sh.j2")
        borgmatic_hook_script = borgmatic_hook_template.render(templateVars)
        with codecs.open('/opt/nDeploy/scripts/borgmatic_cpanel_backup_hook.sh', 'w', 'utf-8') as borgmatic_hook_myscript:
            borgmatic_hook_myscript.write(borgmatic_hook_script)
        os.chmod("/opt/nDeploy/scripts/borgmatic_cpanel_backup_hook.sh", 0o755)
        print('<div class="panel panel-default">')
        print(('<div class="panel-heading"><h3 class="panel-title">BACKUP SETTINGS:</h3></div>'))
        print('<div class="panel-body">')
        print('<div class="icon-box">')
        print('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> Backup Settings updated')
        print('</div>')
        print('</div>')
        print('</div>')
    else:
        print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Backup config error </div>')
else:
        print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')

print('<div class="panel-footer"><small>')
print(branding_print_footer())
print('</small></div>')

print('</div>')  # marker3
print('</div>')  # marker2
print('</body>')
print('</html>')
