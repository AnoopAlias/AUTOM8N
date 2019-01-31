#!/usr/bin/env python


import cgitb
import cgi
import subprocess
import yaml
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


xtendweb_installation_path = "/opt/nDeploy"  # Absolute Installation Path
installation_path = "/opt/nDeploy"  # Absolute Installation Path
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
        brand_name = "AUTOM8N"
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

if form.getvalue('mode') and form.getvalue('unit'):
    if form.getvalue('mode') == 'service':
        myservice = form.getvalue('unit')+".service"
        print('<div class="panel panel-default">')
        print('<div class="panel-heading"><h3 class="panel-title">Current Resource Usage</h3></div>')
        print('<div class="panel-body">')  # marker6
        print(('<div class="alert alert-success alert-btm">'))
        print(('<div class="panel-heading"><h3 class="panel-title">Current Resource Usage:'+myservice+'</h3></div>'))
        mymem = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  MemoryLimit', shell=True).split('=')[1]
        mycpu = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  CPUShares', shell=True).split('=')[1]
        myio = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  BlockIOWeight', shell=True).split('=')[1]
        if int(myio) == 18446744073709551615:
            print('BlockIOWeight=nolimit')
        else:
            print('BlockIOWeight='+myio)
        print('<br>')
        if int(mycpu) == 18446744073709551615:
            print('CPUShares=nolimit')
        else:
            print('CPUShares='+mycpu)
        print('<br>')
        if int(mymem) == 18446744073709551615:
            print('MemoryLimit=nolimit')
        else:
            mymem_inmb = float(mymem) / (1024.0 * 1024.0)
            print('MemoryLimit='+str(mymem_inmb)+'Mb')
        print('<br>')
        print(('</div>'))
        print('</div>')  # marker6
        print('</div>')
    elif form.getvalue('mode') == 'user':
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        print('<div class="panel panel-default">')
        print(('<div class="panel-heading"><h3 class="panel-title">Current Resource usage:'+form.getvalue('unit')+'</h3></div>'))
        print('<div class="panel-body">')  # marker6
        print('<ul class="list-group">')
        print(('<div class="alert alert-info alert-top">'))
        for backend_name in list(php_backends_dict.keys()):
            myservice = backend_name+'@'+form.getvalue('unit')+".service"
            mymem = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  MemoryLimit', shell=True).split('=')[1]
            mycpu = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  CPUShares', shell=True).split('=')[1]
            myio = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  BlockIOWeight', shell=True).split('=')[1]
            print(myservice)
            print('<br>')
            if int(myio) == 18446744073709551615:
                print('BlockIOWeight=nolimit')
            else:
                print('BlockIOWeight='+myio)
            print('<br>')
            if int(mycpu) == 18446744073709551615:
                print('CPUShares=nolimit')
            else:
                print('CPUShares='+mycpu)
            print('<br>')
            if int(mymem) == 18446744073709551615:
                print('MemoryLimit=nolimit')
            else:
                mymem_inmb = float(mymem) / (1024.0 * 1024.0)
                print('MemoryLimit='+str(mymem_inmb)+'Mb')
            print('<br>')
            print('<br>')
        myservice = 'ndeploy_hhvm@'+form.getvalue('unit')+".service"
        mymem = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  MemoryLimit', shell=True).split('=')[1]
        mycpu = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  CPUShares', shell=True).split('=')[1]
        myio = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  BlockIOWeight', shell=True).split('=')[1]
        print(myservice)
        print('<br>')
        if int(myio) == 18446744073709551615:
            print('BlockIOWeight=nolimit')
        else:
            print('BlockIOWeight='+myio)
        print('<br>')
        if int(mycpu) == 18446744073709551615:
            print('CPUShares=nolimit')
        else:
            print('CPUShares='+mycpu)
        print('<br>')
        if int(mymem) == 18446744073709551615:
            print('MemoryLimit=nolimit')
        else:
            mymem_inmb = float(mymem) / (1024.0 * 1024.0)
            print('MemoryLimit='+str(mymem_inmb)+'Mb')
        print('<br>')
        print('<br>')
        print(('</div>'))
        print('</ul>')
        print('</div>')  # marker6
        print('</div>')
    # Next section start here
    print('<div class="panel panel-default">')  # markera1
    print('<div class="panel-heading"><h3 class="panel-title">Set Resource limit</h3></div>')
    print('<div class="panel-body">')  # markera2
    print('<form class="form-inline" action="save_resource_limit.cgi" method="post">')
    print('<div class="row">')  # markerb1

    print('<div class="col-sm-4">')  # markerc1
    print('<div class="panel panel-default">')  # markerc2
    print('<div class="panel-heading"><h3 class="panel-title">CPU</h3></div>')
    print('<div class="panel-body">')  # markerc3
    print('<select name="cpu">')
    for percentage in '100', '75', '50', '25':
        print(('<option value="'+percentage+'">'+percentage+'%</option>'))
    print('</select>')
    print('</div>')  # markerc3
    print('</div>')  # markerc2
    print('</div>')  # markerc1
    print('<div class="col-sm-4">')  # markerc1
    print('<div class="panel panel-default">')  # markerc2
    print('<div class="panel-heading"><h3 class="panel-title">MEMORY</h3></div>')
    print('<div class="panel-body">')  # markerc3
    print('<select name="memory">')
    for percentage in '100', '75', '50', '25':
        print(('<option value="'+percentage+'">'+percentage+'%</option>'))
    print('</select>')
    print('</div>')  # markerc3
    print('</div>')  # markerc2
    print('</div>')  # markerc1
    print('<div class="col-sm-4">')  # markerc1
    print('<div class="panel panel-default">')  # markerc2
    print('<div class="panel-heading"><h3 class="panel-title">BLOCKIO</h3></div>')
    print('<div class="panel-body">')  # markerc3
    print('<select name="blockio">')
    for percentage in '100', '75', '50', '25':
        print(('<option value="'+percentage+'">'+percentage+'%</option>'))
    print('</select>')
    print('</div>')  # markerc3
    print('</div>')  # markerc2
    print('</div>')  # markerc1

    print('</div>')  # markerb1
    print(('<input style="display:none" name="mode" value="'+form.getvalue('mode')+'">'))
    print(('<input style="display:none" name="unit" value="'+form.getvalue('unit')+'">'))
    print('<input class="btn btn-primary" type="submit" value="SET LIMIT">')
    print('</form>')
    print('</div>')  # markera2
    print('</div>')  # markera1
else:
    print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')

print('<div class="panel-footer"><small>')
print(branding_print_footer())
print('</small></div>')

print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
