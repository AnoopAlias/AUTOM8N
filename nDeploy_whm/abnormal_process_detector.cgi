#!/usr/bin/python
import cgi
import cgitb
import psutil
import platform
import os
import yaml


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


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
        brand_name = yaml_parsed_brand.get("brand", "XtendWeb")
    else:
        brand_name = "XtendWeb"
    return brand_name


def branding_print_footer():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_footer = yaml_parsed_brand.get("brand_footer", '<a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">A U T O M 8 N</a>')
    else:
        brand_footer = '<a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">A U T O M 8 N</a>'
    return brand_footer


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
print('<li class="active">Sync Zone</li>')
print('</ol>')

print('<div class="panel panel-default">')
print(('<div class="panel-heading"><h3 class="panel-title">Abnormal Process list</h3></div>'))
print('<div class="panel-body">')  # marker6
malware = False
user_list = os.listdir("/var/cpanel/users")
for myprocess in psutil.process_iter():
    # Workaround for Python 2.6
    if platform.python_version().startswith('2.6'):
        mycmdline = myprocess.cmdline
        myexe = myprocess.exe
        myusername = myprocess.username
        mypid = myprocess.pid
        mystatus = myprocess.status
    else:
        mycmdline = myprocess.cmdline()
        myexe = myprocess.exe()
        myusername = myprocess.username()
        mystatus = myprocess.status()
        mypid = myprocess.pid
    if myusername in user_list and mystatus != 'zombie':
        if myexe.startswith(("/usr/bin/perl", "/home")):
            malware = True
            print('<div class="icon-box">')
            print('<span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span> PID: '+str(mypid))
            print('pid: '+str(mypid)+' running under user: '+myusername+' with commandline as: '+mycmdline+' is actually: '+myexe)
            print('</div>')
if not malware:
    print('<div class="icon-box">')
    print('<span class="glyphicon glyphicon-certificate" aria-hidden="true"></span>No suspicious process found')
    print('</div>')
print('</div>')  # marker6
print('</div>')

print('<div class="panel-footer"><small>')
print(branding_print_footer())
print('</small></div>')

print('</div>')  # marker3
print('</div>')  # marker2
print('</body>')
print('</html>')
