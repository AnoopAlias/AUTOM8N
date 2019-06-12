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
        brand_name = yaml_parsed_brand.get("brand", "AUTOM8N")
    else:
        brand_name = "AUTOM8N"
    return brand_name


def branding_print_support():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_support = yaml_parsed_brand.get("brand_support", '<div class="help float-right"><a class="btn btn-primary" target="_blank" href="help.txt"> docs <i class="fas fa-book-open"></i></a></div>')
    else:
        brand_support = '<div class="help float-right"><a class="btn btn-primary" target="_blank" href="help.txt"> docs <i class="fas fa-book-open"></i></a></div>'
    return brand_support


def print_forbidden():
    print(('<i class="fas fa-exclamation"></i><p>Forbidden</p>'))


cgitb.enable()
form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')

print('<head>')

print('<title>')
print(branding_print_banner())
print('</title>')

print(('<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>'))
print(('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>'))
print(('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">'))
print(('<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>'))
print(('<link href="https://fonts.googleapis.com/css?family=Poppins&display=swap" rel="stylesheet">'))
print(('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.1/css/all.min.css" rel="stylesheet">'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))

print('</head>')

print('<body>')

print('<header id="main-header">')

print(branding_print_support())
print('		<div class="logo">')
print('			<h4>')
print('				<a href="xtendweb.cgi"><img border="0" src="')
print(					branding_print_logo_name())
print('					" width="48" height="48"></a>')
print(					branding_print_banner())
print('			</h4>')
print('		</div>')

print('</header>')

print('<div id="main-container" class="container">')  # main container

print('		<nav aria-label="breadcrumb">')
print('			<ol class="breadcrumb">')
print('				<li class="breadcrumb-item"><a href="xtendweb.cgi"><i class="fas fa-redo"></i></a></li>')
print('				<li class="breadcrumb-item active">Resource Limits</li>')
print('			</ol>')
print('		</nav>')

print('		<div class="row justify-content-lg-center">')
print('			<div class="col-lg-6">')

print('				<div class="card">')  # card

if form.getvalue('mode') and form.getvalue('unit'):
    if form.getvalue('mode') == 'service':
        myservice = form.getvalue('unit')+".service"

        print('			<div class="card-header">')
        print('				<h5 class="card-title mb-0"><i class="fas fa-compress float-right"></i> Resource Usage '+myservice+'</h5>')
        print('			</div>')
        print('			<div class="card-body text-center">')  # card-body

        mymem = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  MemoryLimit', shell=True).split('=')[1]
        mycpu = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  CPUShares', shell=True).split('=')[1]
        myio = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  BlockIOWeight', shell=True).split('=')[1]
        print('			<div class="alert alert-success">')
        print('				<ul class="list-unstyled text-center mb-0">')
        if int(myio) == 18446744073709551615:
            print('				<li>BlockIOWeight = nolimit</li>')
        else:
            print('				<li>BlockIOWeight = '+myio+'</li>')
        if int(mycpu) == 18446744073709551615:
            print('				<li>CPUShares = nolimit</li>')
        else:
            print('				<li>CPUShares = '+mycpu+'</li>')
        if int(mymem) == 18446744073709551615:
            print('				<li>MemoryLimit = nolimit</li>')
        else:
            mymem_inmb = float(mymem) / (1024.0 * 1024.0)
            print('				<li>MemoryLimit = '+str(mymem_inmb)+'Mb</li>')
        print('				</ul>')
        print('			</div>')

    elif form.getvalue('mode') == 'user':
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
        php_backends_dict = backend_data_yaml_parsed["PHP"]

        print('			<div class="card-header">')
        print('				<h5 class="card-title mb-0"><i class="fas fa-signal float-right"></i> Resource Usage '+form.getvalue('unit')+'</h5>')
        print('			</div>')
        print('			<div class="card-body text-center">')  # card-body

        for backend_name in list(php_backends_dict.keys()):
            myservice = backend_name+'@'+form.getvalue('unit')+".service"
            mymem = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  MemoryLimit', shell=True).split('=')[1]
            mycpu = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  CPUShares', shell=True).split('=')[1]
            myio = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  BlockIOWeight', shell=True).split('=')[1]
            print(myservice)
            print('			<div class="alert alert-success">')
            print('				<ul class="list-unstyled text-center mb-0">')
            if int(myio) == 18446744073709551615:
                print('				<li>BlockIOWeight = nolimit</li>')
            else:
                print('				<li>BlockIOWeight = '+myio+'</li>')
            if int(mycpu) == 18446744073709551615:
                print('				<li>CPUShares = nolimit</li>')
            else:
                print('				<li>CPUShares = '+mycpu+'</li>')
            if int(mymem) == 18446744073709551615:
                print('				<li>MemoryLimit = nolimit</li>')
            else:
                mymem_inmb = float(mymem) / (1024.0 * 1024.0)
                print('				<li>MemoryLimit = '+str(mymem_inmb)+'Mb</li>')
            print('				</ul>')
            print('			</div>')

    # Set Limits
    print('					<form class="form" method="post" id="modalForm19" onsubmit="return false;">')

    print('						<div class="input-group">')
    print('							<div class="input-group-prepend input-group-prepend-min">')
    print('								<label class="input-group-text">CPU</label>')
    print('							</div>')
    print('							<select name="cpu" class="custom-select">')
    for percentage in '100', '75', '50', '25':
        print(('						<option value="'+percentage+'">'+percentage+'%</option>'))
    print('							</select>')
    print('						</div>')

    print('						<div class="input-group">')
    print('							<div class="input-group-prepend input-group-prepend-min">')
    print('								<label class="input-group-text">Memory</label>')
    print('							</div>')
    print('							<select name="memory" class="custom-select">')
    for percentage in '100', '75', '50', '25':
        print(('						<option value="'+percentage+'">'+percentage+'%</option>'))
    print('							</select>')
    print('						</div>')

    print('						<div class="input-group">')
    print('							<div class="input-group-prepend input-group-prepend-min">')
    print('								<label class="input-group-text">Block IO</label>')
    print('							</div>')
    print('							<select name="blockio" class="custom-select">')
    for percentage in '100', '75', '50', '25':
        print(('						<option value="'+percentage+'">'+percentage+'%</option>'))
    print('							</select>')
    print('						</div>')

    print(('					<input class="hidden" name="mode" value="'+form.getvalue('mode')+'">'))
    print(('					<input class="hidden" name="unit" value="'+form.getvalue('unit')+'">'))
    print('						<button class="btn btn-outline-primary btn-block" type="submit">Set Limit</button>')
    print('					</form>')
else:
    print_forbidden()

print('					</div>')  # card-body end
print('				</div>')  # card end

print('			</div>')  # col end
print('		</div>')  # row end

print('</div>')  # main-container end

# Modal
print('		<div class="modal fade" id="myModal" tabindex="-1" role="dialog"> ')
print('    		<div class="modal-dialog modal-dialog-centered" role="document">')
print('      		<div class="modal-content">')
print('        			<div class="modal-header">')
print('          			<h4 class="modal-title">Command Output</h4>')
print('						<button type="button" class="close" data-dismiss="modal" aria-label="Close">')
print('          				<span aria-hidden="true">&times;</span>')
print('        				</button>')
print('        			</div>')
print('        			<div class="modal-body">')
print('        			</div>')
print('					<div class="modal-footer">')
print('        				<button type="button" class="btn btn-outline-secondary" data-dismiss="modal">Close</button>')
print('      			</div>')
print('      		</div>')
print('    		</div>')
print('     </div>')

print(('<div id="wait" style="display: none; width: 100%; height: 100%; top: 100px; left: 0px; position: fixed; z-index: 10000; text-align: center;">'))
print(('            <img src="ajax-loader.gif" width="45" height="45" alt="Loading..." style="position: fixed; top: 50%; left: 50%;" />'))
print(('</div>'))

print('</body>')
print('</html>')
