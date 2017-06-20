#!/usr/bin/env python


import os
import cgitb
import subprocess
import jinja2
import codecs
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


xtendweb_installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>SimpleR Resource control</title>')
print(('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'))
print(('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" crossorigin="anonymous"></script>'))
print(('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<div id="main-container" class="container text-center">')
print('<div class="row">')
print('<div class="col-md-6 col-md-offset-3">')
print('<div class="logo">')
print('<h4><span class="label label-primary">SimpleR</span></h4>')
print('<h6><span class="label label-default">Simple Resouce controller</span></h6>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="simpler.cgi"><span class="glyphicon glyphicon-refresh"></span></a></li>')
print('<li class="active">Select Reseller or Service</li>')
print('</ol>')
print('<div class="panel panel-default">')
if os.path.isfile(xtendweb_installation_path+"/conf/secure-php-enabled"):
    print('<div class="panel-heading"><h3 class="panel-title"><span class="label label-default">Select reseller to configure</span></h3></div>')
    print('<div class="panel-body">')
    # The API call and ensuring slices are present
    listresellers = subprocess.check_output('/usr/local/cpanel/bin/whmapi1 listresellers --output=json', shell=True)
    myresellers = json.loads(listresellers)
    resellerdata = myresellers.get('data')
    resellerlist = resellerdata.get('reseller')
    resellerlist.append('root')
    # Ensure the reseller slice is present in the system
    for owner in resellerlist:
        ownerslice = "/etc/systemd/system/"+owner+".slice"
        if not os.path.isfile(ownerslice):
            # create the slice from a template
            templateLoader = jinja2.FileSystemLoader(xtendweb_installation_path + "/conf/")
            templateEnv = jinja2.Environment(loader=templateLoader)
            if os.path.isfile(xtendweb_installation_path+"/conf/simpler_resources_local.j2"):
                TEMPLATE_FILE = "simpler_resources_local.j2"
            else:
                TEMPLATE_FILE = "simpler_resources.j2"
            template = templateEnv.get_template(TEMPLATE_FILE)
            templateVars = {"OWNER": owner
                            }
            generated_config = template.render(templateVars)
            with codecs.open(ownerslice, 'w', 'utf-8') as confout:
                confout.write(generated_config)
    print('<form class="form-inline" action="simpler_config.cgi" method="post">')
    print('<select name="reseller">')
    for reseller in resellerlist:
        print(('<option value="'+reseller+'">'+reseller+'</option>'))
    print('</select>')
    print(('<input style="display:none" name="mode" value="user">'))
    print('<input class="btn btn-primary" type="submit" value="CONFIGURE">')
    print('</form>')
    print('</div>')
print('<div class="panel-heading"><h3 class="panel-title"><span class="label label-default">Select service to configure</span></h3></div>')
print('<div class="panel-body">')
print('<form class="form-inline" action="simpler_config.cgi" method="post">')
print('<select name="service">')
for service in "nginx", "httpd", "mysql", "ndeploy_backends":
    print(('<option value="'+service+'">'+service+'</option>'))
print('</select>')
print(('<input style="display:none" name="mode" value="service">'))
print('<input class="btn btn-primary" type="submit" value="CONFIGURE">')
print('</form>')
print('</div>')
print('<div class="alert alert-info"><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>Limits must be a safe upper value(pressure valve).Do not set very low limits </div>')
print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="https://xtendweb.gnusys.net/docs/user_docs.html">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
