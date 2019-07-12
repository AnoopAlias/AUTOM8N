#!/usr/bin/python

import cgi
import cgitb
import os
import configparser
import codecs
from commoninclude import print_nontoast_error, bcrumb, print_header, print_modals, print_loader, cardheader, cardfooter


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
default_domain_data_file = installation_path+'/conf/domain_data_default.yaml'
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print_header('PHP-FPM Pool Editor')
bcrumb('PHP-FPM Pool Editor','fas fa-sitemap')
print('            <!-- WHM Starter Row -->')
print('            <div class="row justify-content-lg-center">')
print('                <!-- Column Start -->')
print('                <div class="col-lg-8">') #Column

if form.getvalue('poolfile') and form.getvalue('section'):
    myphpini = form.getvalue('poolfile')
    mysection = int(form.getvalue('section'))

    if os.path.isfile(myphpini):
        config = configparser.ConfigParser()
        config.readfp(codecs.open(myphpini, 'r', 'utf8'))
        cardheader('Edit PHP-FPM Pool Settings for '+config.sections()[mysection].upper(),'fas fa-sitemap')
        print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start

        myconfig = dict(config.items(config.sections()[mysection]))
        mykeypos = 1
        for mykey in myconfig.keys():
            print('                            <label for="'+mykey+'">'+mykey+'</label>')
            print('                            <form class="m-0 toastForm10-wrap" id="toastForm10'+'-'+str(mykeypos)+'" method="post" onsubmit="return false;">')
            print('                                <div class="input-group mb-4">')
            print('                                    <input class="form-control" value="'+myconfig.get(mykey)+'"" type="text" name="thevalue">')
            print('                                    <div class="input-group-append">')
            print('                                        <input hidden name="poolfile" value="'+myphpini+'">')
            print('                                        <input hidden name="section" value="'+form.getvalue('section')+'">')
            print('                                        <input hidden name="thekey" value="'+mykey+'">')
            print('                                        <input hidden name="action" value="edit">')
            print('                                        <button class="btn btn-outline-primary" type="submit">')
            print('                                            <span class="sr-only">Save</span>')
            print('                                            <i class="fas fa-pen"></i>')
            print('                                        </button>')
            print('                                    </form>')
            print('                                    <form class="m-0 toastForm9-wrap" id="toastForm9'+'-'+str(mykeypos)+'"  method="post" onsubmit="return false;">')
            print('                                        <input hidden name="poolfile" value="'+myphpini+'">')
            print('                                        <input hidden name="section" value="'+form.getvalue('section')+'">')
            print('                                        <input hidden name="thekey" value="'+mykey+'">')
            print('                                        <input hidden name="action" value="delete">')
            print('                                        <button class="btn btn-outline-danger" type="submit">')
            print('                                            <span class="sr-only">Delete</span>')
            print('                                            <i class="fas fa-times"></i>')
            print('                                        </button>')
            print('                                    </div>')
            print('                                </div>')
            print('                            </form>')            
            mykeypos = mykeypos + 1

        print('                        </div> <!-- Card Body End -->') #Card End
        cardfooter('')

        # New PHP Param
        cardheader('Add New PHP-FPM Pool Setting for '+config.sections()[mysection].upper(),'fas fa-sitemap')
        print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start

        print('                            <form class="m-0" method="post" id="toastForm20" onsubmit="return false;">')
        print('                                <div class="input-group">')
        print('                                    <div class="input-group-prepend">')
        print('                                        <span class="input-group-text">Key & Value</span>')
        print('                                    </div>')
        print('                                    <input type="text" aria-label="Key" placeholder="Key" name="thekey" class="form-control">')
        print('                                    <input type="text" aria-label="Value" placeholder="Value" name="thevalue" class="form-control">')
        print('                                    <div class="input-group-append">')
        print('                                        <input hidden name="section" value="'+form.getvalue('section')+'">')
        print('                                        <input hidden name="poolfile" value="'+myphpini+'">')
        print('                                        <input hidden name="action" value="edit">')
        print('                                        <button class="btn btn-outline-primary" type="submit">')
        print('                                             <span class="sr-only">Add</span>')
        print('                                             <i class="fas fa-plus"></i>')
        print('                                        </button>')
        print('                                    </div>')
        print('                                </div>')
        print('                            </form>')

        print('                        </div> <!-- Card Body End -->') #Card Body End
        cardfooter('<strong>WARNING USE AT YOUR OWN RISK! </strong><br>Adding or modifying pool configurations with invalid settings can bring down your PHP application server.')
else:
    print_nontoast_error('<h3>Forbidden!</h3>Though shall not Pass!')

#Column End
print('                <!-- Column End -->')
print('                </div>')
print('')
print('            <!-- WHM End Row -->')
print('            </div>')
print('')
print('        </div> <!-- Main Container End -->')
print('')

print_modals()
print_loader()

print('    <!-- Body End -->')
print('    </body>')
print('</html>')