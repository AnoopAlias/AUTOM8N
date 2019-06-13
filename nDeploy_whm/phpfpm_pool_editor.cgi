#!/usr/bin/python

import commoninclude
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

cgitb.enable()

form = cgi.FieldStorage()

commoninclude.print_header()

print('<body>')

commoninclude.print_branding()

print('<div id="main-container" class="container">')  # main container

print('		<nav aria-label="breadcrumb">')
print('			<ol class="breadcrumb">')
print('				<li class="breadcrumb-item"><a href="xtendweb.cgi"><i class="fas fa-redo"></i></a></li>')
print('				<li class="breadcrumb-item active">PHP-FPM pool edit</li>')
print('			</ol>')
print('		</nav>')

print('		<div class="row justify-content-lg-center">')
print('			<div class="col-lg-8">')

if form.getvalue('poolfile') and form.getvalue('section'):
    myphpini = form.getvalue('poolfile')
    mysection = int(form.getvalue('section'))
    if os.path.isfile(myphpini):
        config = configparser.ConfigParser()
        config.readfp(codecs.open(myphpini, 'r', 'utf8'))
        print('		<div class="card">')  # card
        print('			<div class="card-header">')
        print('				<h5 class="card-title mb-0"><i class="fas fa-sitemap float-right"></i> '+config.sections()[mysection]+'</h5>')
        print('			</div>')
        print('			<div class="card-body">')  # card-body

        myconfig = dict(config.items(config.sections()[mysection]))
        mykeypos=1
        for mykey in myconfig.keys():
            print('			<label for="'+mykey+'">')
            print(mykey)
            print('			</label>')
            print('			<form class="m-0 modalForm10-wrap" id="modalForm10'+'-'+str(mykeypos)+'"  method="post" onsubmit="return false;">')
            print('			<div class="input-group btn-2 mb-4">')
            print('				<input class="form-control" value='+myconfig.get(mykey)+' type="text" name="thevalue">')
            print('				<div class="input-group-append">')
            print('						<button class="btn btn-outline-primary" type="submit"><span class="sr-only">Save</span><i class="fas fa-pen"></i></button>')
            print(('					<input class="hidden" name="poolfile" value="'+myphpini+'">'))
            print(('					<input class="hidden" name="section" value="'+form.getvalue('section')+'">'))
            print(('					<input class="hidden" name="thekey" value="'+mykey+'">'))
            print(('					<input class="hidden" name="action" value="edit">'))
            print('			</form>')
            print('			<form class="m-0 modalForm9-wrap" id="modalForm9'+'-'+str(mykeypos)+'"  method="post" onsubmit="return false;">')
            print('						<button class="btn btn-outline-danger" type="submit"><span class="sr-only">Delete</span><i class="fas fa-times"></i></button>')
            print(('					<input class="hidden" name="poolfile" value="'+myphpini+'">'))
            print(('					<input class="hidden" name="section" value="'+form.getvalue('section')+'">'))
            print(('					<input class="hidden" name="thekey" value="'+mykey+'">'))
            print(('					<input class="hidden" name="action" value="delete">'))
            print('			</form>')
            print('				</div>')
            print('			</div>')
            mykeypos = mykeypos + 1

        print('			</div>')  # card-body end
        print('		</div>')  # card end

        # New PHP Param
        print('		<div class="card">')  # card
        print('			<div class="card-header">')
        print('				<h5 class="card-title mb-0"><i class="fas fa-sitemap float-right"></i> Add new pool setting</h5>')
        print('			</div>')
        print('			<div class="card-body">')  # card-body

        print('				<form class="m-0" method="post" id="modalForm20" onsubmit="return false;">')
        print('					<div class="input-group">')
        print('						<div class="input-group-prepend">')
        print('							<span class="input-group-text">Key & Value</span>')
        print('				     	</div>')
        print('						<input type="text" aria-label="Key" placeholder="Key" name="thekey" class="form-control">')
        print('						<input type="text" aria-label="Value" placeholder="Value" name="thevalue" class="form-control">')
        print('						<div class="input-group-append">')
        print(('						<input class="hidden" name="section" value="'+form.getvalue('section')+'">'))
        print(('						<input class="hidden" name="poolfile" value="'+myphpini+'">'))
        print(('						<input class="hidden" name="action" value="edit">'))
        print('							<button class="btn btn-outline-primary" type="submit"><span class="sr-only">Add</span><i class="fas fa-plus"></i></button>')
        print('						</div>')
        print('					</div>')
        print('				</form>')

        print('			</div>')  # card-body end
        print('			<div class="card-footer footer-warning">')
        print('				<small>WARNING: Editing pool config with invalid settings can bring down your PHP application server. Edit at your own risk</small>')
        print('			</div>')
else:
        commoninclude.print_forbidden()

print('				</div>')  # card end

print('			</div>')  # col end
print('		</div>')  # row end

print('</div>')  # main-container end

commoninclude.print_modals()
commoninclude.print_loader()

print('</body>')
print('</html>')
