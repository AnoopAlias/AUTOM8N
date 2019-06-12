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

cgitb.enable()

form = cgi.FieldStorage()


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


def print_green(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-info" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_red(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_forbidden():
    print(('<i class="fas fa-exclamation"></i><p>Forbidden</p>'))


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
            print('						<button class="btn btn-outline-primary btn-ajax-sm" type="submit"><span class="sr-only">Save</span><i class="fas fa-pen"></i></button>')
            print(('					<input class="hidden" name="poolfile" value="'+myphpini+'">'))
            print(('					<input class="hidden" name="section" value="'+form.getvalue('section')+'">'))
            print(('					<input class="hidden" name="thekey" value="'+mykey+'">'))
            print(('					<input class="hidden" name="action" value="edit">'))
            print('			</form>')
            print('			<form class="m-0 modalForm9-wrap" id="modalForm9'+'-'+str(mykeypos)+'"  method="post" onsubmit="return false;">')
            print('						<button class="btn btn-outline-danger btn-ajax-sm" type="submit"><span class="sr-only">Delete</span><i class="fas fa-times"></i></button>')
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

        print('				<form class="m-0" id="modalForm8" onsubmit="return false;">')
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
        print('							<button class="btn btn-outline-primary btn-ajax-slow" type="submit"><span class="sr-only">Add</span><i class="fas fa-plus"></i></button>')
        print('						</div>')
        print('					</div>')
        print('				</form>')

        print('			</div>')  # card-body end
        print('			<div class="card-footer footer-warning">')
        print('				<small>WARNING: Editing pool config with invalid settings can bring down your PHP application server. Edit at your own risk</small>')
        print('			</div>')
else:
        print_forbidden()

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
print('        				<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>')
print('      			</div>')
print('      		</div>')
print('    		</div>')
print('     </div>')

print('</body>')
print('</html>')
