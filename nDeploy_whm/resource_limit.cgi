#!/usr/bin/env python

import cgitb
import cgi
import subprocess
import yaml
import sys
from commoninclude import print_nontoast_error, bcrumb, print_header, print_footer, display_term, cardheader, cardfooter


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"

cgitb.enable()
form = cgi.FieldStorage()

if form.getvalue('mode') and form.getvalue('unit'):
    if form.getvalue('mode') == 'service':
        myservice = form.getvalue('unit')+".service"

        print_header('Resource Usage for '+myservice)
        bcrumb('Resource Usage for '+myservice,'fas fa-compress')
        print('            <!-- WHM Starter Row -->')
        print('            <div class="row justify-content-lg-center">')
        print('                <!-- First Column Start -->')
        print('                <div class="col-lg-6">') #Left Column
        print('')
        cardheader('Resource Usage for '+myservice,'fas fa-compress')
        print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start

        mymem = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  MemoryLimit', shell=True).split('=')[1]
        mycpu = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  CPUShares', shell=True).split('=')[1]
        myio = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  BlockIOWeight', shell=True).split('=')[1]
        print('                            <div class="alert alert-success">')
        print('                                <ul class="list-unstyled text-center mb-0">')
        if int(myio) == 18446744073709551615:
            print('                                    <li>BlockIOWeight = nolimit</li>')
        else:
            print('                                    <li>BlockIOWeight = '+myio.rstrip()+'</li>')
        if int(mycpu) == 18446744073709551615:
            print('                                    <li>CPUShares = nolimit</li>')
        else:
            print('                                    <li>CPUShares = '+mycpu.rstrip()+'</li>')
        if int(mymem) == 18446744073709551615:
            print('                                    <li>MemoryLimit = nolimit</li>')
        else:
            mymem_inmb = float(mymem) / (1024.0 * 1024.0)
            print('                                    <li>MemoryLimit = '+str(mymem_inmb).rstrip()+'Mb</li>')
        print('                                </ul>')
        print('                            </div>')

    elif form.getvalue('mode') == 'user':
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
        php_backends_dict = backend_data_yaml_parsed["PHP"]

        cardheader('Resource Usage for '+form.getvalue('unit'),'fas fa-signal')
        print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start

        for backend_name in list(php_backends_dict.keys()):
            myservice = backend_name+'@'+form.getvalue('unit')+".service"
            mymem = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  MemoryLimit', shell=True).split('=')[1]
            mycpu = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  CPUShares', shell=True).split('=')[1]
            myio = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  BlockIOWeight', shell=True).split('=')[1]
            print(myservice)
            print('                            <div class="alert alert-success">')
            print('                                <ul class="list-unstyled text-center mb-0">')
            if int(myio) == 18446744073709551615:
                print('                                    <li>BlockIOWeight = nolimit</li>')
            else:
                print('                                    <li>BlockIOWeight = '+myio.rstrip()+'</li>')
            if int(mycpu) == 18446744073709551615:
                print('                                    <li>CPUShares = nolimit</li>')
            else:
                print('                                    <li>CPUShares = '+mycpu.rstrip()+'</li>')
            if int(mymem) == 18446744073709551615:
                print('                                    <li>MemoryLimit = nolimit</li>')
            else:
                mymem_inmb = float(mymem) / (1024.0 * 1024.0)
                print('                                    <li>MemoryLimit = '+str(mymem_inmb).rstrip()+'Mb</li>')
            print('                                </ul>')
            print('                            </div>')

    # Set Limits
    print('                            <form class="form" method="post" id="set_resource_limit" onsubmit="return false;">')

    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend input-group-prepend-min">')
    print('                                        <label class="input-group-text">CPU</label>')
    print('                                    </div>')
    print('                                    <select name="cpu" class="custom-select">')
    for percentage in '100', '75', '50', '25':
        print('                                        <option value="'+percentage+'">'+percentage+'%</option>')
    print('                                    </select>')
    print('                                </div>')

    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend input-group-prepend-min">')
    print('                                        <label class="input-group-text">Memory</label>')
    print('                                    </div>')
    print('                                    <select name="memory" class="custom-select">')
    for percentage in '100', '75', '50', '25':
        print('                                        <option value="'+percentage+'">'+percentage+'%</option>')
    print('                                    </select>')
    print('                                </div>')

    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend input-group-prepend-min">')
    print('                                        <label class="input-group-text">Block IO</label>')
    print('                                    </div>')
    print('                                    <select name="blockio" class="custom-select">')
    for percentage in '100', '75', '50', '25':
        print('                                        <option value="'+percentage+'">'+percentage+'%</option>')
    print('                                    </select>')
    print('                                </div>')

    print('                                <input hidden name="mode" value="'+form.getvalue('mode')+'">')
    print('                                <input hidden name="unit" value="'+form.getvalue('unit')+'">')
    print('                                <button id="set-resource-limit-btn" class="btn btn-outline-primary btn-block" type="submit">Set Limit</button>')
    print('                            </form>')
    print('                        </div> <!-- Card Body End -->') #Card Body End
    cardfooter('Set the desired resource percentages for '+myservice)

else:
    print_header('Resource Usage')
    bcrumb('Resource Usage','fas fa-compress')
    print('            <!-- WHM Starter Row -->')
    print('            <div class="row justify-content-lg-center">')
    print('                <!-- First Column Start -->')
    print('                <div class="col-lg-6">') #Left Column
    print('')

    print_nontoast_error('Forbidden!', 'Missing Data!')
    sys.exit(0)

# Column End
print('                <!-- First Column End -->')
print('                </div>')
print('')
print('            <!-- WHM End Row -->')
print('            </div>')

print_footer()
