#!/usr/bin/env python


import os
import cgitb
import subprocess
import jinja2
import codecs
import platform
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
print('<title>XtendWeb</title>')
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
print('<a href="xtendweb.cgi" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.cgi"><span class="glyphicon glyphicon-refresh"></span></a></li>')
print('<li class="active">Server Config</li>')
print('</ol>')

# Next section start here
with open('/etc/redhat-release','r') as releasefile:
  osrelease = releasefile.read().split(' ')[0]
if not osrelease == 'CloudLinux':
  if 'el7' in platform.uname()[2]:
    # Next sub-section start here
    if os.path.isfile(xtendweb_installation_path+"/conf/secure-php-enabled"): # if per user php-fpm master process is set
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
      print('<div class="panel panel-default">')  # markera1
      print('<div class="panel-heading"><h3 class="panel-title">Resource limit</h3></div>')
      print('<div class="panel-body">') # markera2
      print('<div class="row">')  # markerb1
      print('<div class="col-sm-6">')  # markerc1
      print('<div class="panel panel-default">')  # markerc2
      print('<div class="panel-heading"><h3 class="panel-title">Reseller</h3></div>')
      print('<div class="panel-body">') # markerc3
      print('<form class="form-inline" action="simpler_config.cgi" method="post">')
      print('<select name="reseller">')
      for reseller in resellerlist:
          print(('<option value="'+reseller+'">'+reseller+'</option>'))
      print('</select>')
      print(('<input style="display:none" name="mode" value="user">'))
      print(('<br>'))
      print('<input class="btn btn-primary" type="submit" value="SET LIMIT">')
      print('</form>')
      print('</div>') # markerc3
      print('</div>') # markerc2
      print('</div>') # markerc1
      print('<div class="col-sm-6">')  # markerc1
      print('<div class="panel panel-default">')  # markerc2
      print('<div class="panel-heading"><h3 class="panel-title">Service</h3></div>')
      print('<div class="panel-body">') # markerc3
      print('<form class="form-inline" action="simpler_config.cgi" method="post">')
      print('<select name="service">')
      for service in "nginx", "httpd", "mysql", "ndeploy_backends":
          print(('<option value="'+service+'">'+service+'</option>'))
      print('</select>')
      print(('<input style="display:none" name="mode" value="service">'))
      print('<input class="btn btn-primary" type="submit" value="SET LIMIT">')
      print('</form>')
      print('</div>') # markerc3
      print('</div>') # markerc2
      print('</div>') # markerc1
      print('</div>') # markerb1
      print('</div>') # markera2
      print('</div>') # markera1
    else:
    # Next sub-section start here
      print('<div class="panel panel-default">')  # markera1
      print('<div class="panel-heading"><h3 class="panel-title">Service resource limit</h3></div>')
      print('<div class="panel-body">') # markera2
      print('<form class="form-inline" action="simpler_config.cgi" method="post">')
      print('<select name="service">')
      for service in "nginx", "httpd", "mysql", "ndeploy_backends":
          print(('<option value="'+service+'">'+service+'</option>'))
      print('</select>')
      print(('<input style="display:none" name="mode" value="service">'))
      print('<input class="btn btn-primary" type="submit" value="SET LIMIT">')
      print('</form>')
      print('</div>') # markera2
      print('</div>') # markera1

print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
print('</div>') # marker3
print('</div>') # marker2
print('</div>') # marker1
print('</body>')
print('</html>')
