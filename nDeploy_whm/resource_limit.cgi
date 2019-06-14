#!/usr/bin/env python

import commoninclude
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


cgitb.enable()
form = cgi.FieldStorage()

commoninclude.print_header()

print('<body>')

commoninclude.print_branding()

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
    commoninclude.print_forbidden()

print('					</div>')  # card-body end
print('				</div>')  # card end

print('			</div>')  # col end
print('		</div>')  # row end

print('</div>')  # main-container end

commoninclude.print_modals()
commoninclude.print_loader()

print('</body>')
print('</html>')
