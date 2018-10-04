#!/usr/bin/python
import cgi
import cgitb
import os
import configparser
import codecs
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
print('<div class="col-md-8 col-md-offset-2">')  # marker3

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

if form.getvalue('poolfile') and form.getvalue('section'):
    myphpini = form.getvalue('poolfile')
    mysection = int(form.getvalue('section'))
    if os.path.isfile(myphpini):
        config = configparser.ConfigParser()
        config.readfp(codecs.open(myphpini, 'r', 'utf8'))
        # Next section start here
        print('<div class="alert alert-warning alert-domain"><strong>'+config.sections()[mysection]+'</strong></div>')
        print('<div class="panel panel-default">')  # marker6
        print('<div class="panel-heading"><h3 class="panel-title">Edit PHP-FPM pool</h3></div>')
        print('<div id="config" class="panel-body">')  # marker7
        print('<ul class="list-group">')
        myconfig = dict(config.items(config.sections()[mysection]))
        for mykey in myconfig.keys():
            print('<li class="list-group-item">')
            print('<div class="row">')
            print(('<div class="col-sm-6 col-radio text-left">'+mykey+'</div>'))
            print('<div class="col-sm-6 col-radio">')
            print('<div class="input-group">')
            print('<div class="form-control">')
            print(myconfig.get(mykey))
            print('</div>')
            print('<form class="form-group" action="save_phpfpm_pool.cgi">')
            print('<span class="input-group-btn"><input class="btn btn-primary" type="submit" value="EDIT"></span>')
            print(('<input class="hidden" name="poolfile" value="'+myphpini+'">'))
            print(('<input class="hidden" name="section" value="'+form.getvalue('section')+'">'))
            print(('<input class="hidden" name="thekey" value="'+mykey+'">'))
            print('</form>')
            print('<form class="form-group" action="save_phpfpm_pool.cgi">')
            print('<span class="input-group-btn"><input class="btn btn-danger" type="submit" value="DEL"></span>')
            print(('<input class="hidden" name="poolfile" value="'+myphpini+'">'))
            print(('<input class="hidden" name="section" value="'+form.getvalue('section')+'">'))
            print(('<input class="hidden" name="thekey" value="'+mykey+'">'))
            print('</form>')
            print('</div>')
            print('</div>')
            print('</li>')
        print('</ul>')
        print('</div>')  # div8
        print('</div>')  # div7
        # Next section start here
        print('<div class="panel panel-default">')  # marker6
        print('<div class="panel-heading"><h3 class="panel-title">Add new pool setting</h3></div>')
        print('<div class="panel-body">')  # marker7
        print(('<div class="alert alert-warning">'))
        print(('WARNING: Editing pool config with invalid settings can bring down your PHP application server. Edit at your own risk'))
        print(('</div>'))
        print('<form class="form-group" action="save_phpfpm_pool_file.cgi">')
        print('<ul class="list-group">')
        print('<li class="list-group-item">')
        print('<div class="row">')
        print('<div class="col-sm-6 col-radio">')
        print('<input class="form-control" placeholder="KEY" type="text" name="thekey">')
        print('</div>')
        print('<div class="col-sm-6 col-radio">')
        print('<input class="form-control" placeholder="VALUE" type="text" name="thevalue">')
        print('</div>')
        print('</div>')
        print('</li>')
        print(('<input style="display:none" name="section" value="'+form.getvalue('section')+'">'))
        print(('<input class="hidden" name="poolfile" value="'+myphpini+'">'))
        print('</ul>')
        print('<input class="btn btn-primary" type="submit" value="Submit">')
        print('</form>')
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
