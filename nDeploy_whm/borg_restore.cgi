#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import os
import subprocess

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
print('				<li class="breadcrumb-item active">Borg backup restore</li>')
print('			</ol>')
print('		</nav>')

print('		<div class="row justify-content-lg-center">')
print('			<div class="col-lg-8">')

print('		<div class="card">')  # card
print('			<div class="card-header">')
print('				<h5 class="card-title mb-0"><i class="fas fa-sitemap float-right"></i> Backup Restore points</h5>')
print('			</div>')
print('			<div class="card-body last">')  # card-body

if os.path.isfile('/etc/borgmatic/BORG_SETUP_LOCK_DO_NOT_REMOVE'):
    pass
else:
    commoninclude.print_forbidden()

print('			</div>')  # card-body end
print('		</div>')  # card end

print('			</div>')  # col end
print('		</div>')  # row end

print('</div>')  # main-container end

commoninclude.print_modals()
commoninclude.print_loader()

print('</body>')
print('</html>')
