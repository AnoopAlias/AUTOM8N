#!/usr/bin/env python

import os
import yaml

installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
homedir_config_file = installation_path+"/conf/nDeploy-cluster/group_vars/all"


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


def print_branding():
    print('        <header id="main-header">')
    print('            '+branding_print_support())
    print('            <div class="logo">')
    print('                <h4>')
    print('                    <a href="xtendweb.cgi"><img border="0" src="'+branding_print_logo_name()+'" width="48" height="48"></a>'+branding_print_banner())
    print('                </h4>')
    print('            </div>')
    print('        </header>')


def print_green(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-info" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_red(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_forbidden():
    print(('<i class="fas fa-exclamation"></i><p>Forbidden</p>'))


def print_error(themessage):
    print(('<i class="fas fa-exclamation"></i><p>'+themessage+'</p>'))


def print_success(themessage):
    print(('<i class="fas fa-thumbs-up"></i><p>'+themessage+'</p>'))


def print_error_alert(themessage):
    print(('<div class="alert alert-danger text-left">'+themessage+'</div>'))


def print_sys_tip(theoption, hint):
    print(('<div class="col-md-6"><div class="alert alert-light" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_disabled():
    print(('<div class="col-md-6 align-self-center"><div class="btn btn-light btn-block btn-not-installed" data-toggle="tooltip" title="An additional nginx module is required for this functionality">Not Installed</div></div>'))


def print_forbidden_wrapper():
    print(('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body"><i class="fas fa-exclamation"></i><p>Forbidden</p></div></div>'))


def print_error_wrapper(themessage):
    print(('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body"><i class="fas fa-exclamation"></i><p>'+themessage+'</p></div></div>'))


def print_success_wrapper(themessage):
    print(('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body text-center"><i class="fas fa-thumbs-up"></i><p>'+themessage+'</p></div></div>'))


def print_multi_input(theoption, hint):
    print(('<div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'))


def print_loader():
    print(('<div id="loader"><i class="fas fa-infinity fa-spin"></i></div>'))


def print_header(title=''):
    print(('Content-Type: text/html'))
    print((''))
    print(('<html>'))
    print(('    <head>'))
    print(('        <title>'+title+'</title>'))
    print(('        <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>'))
    print(('        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>'))
    print(('        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>'))
    print(('        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">'))
    print(('        <link href="https://fonts.googleapis.com/css?family=Poppins&display=swap" rel="stylesheet">'))
    print(('        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.1/css/all.min.css" rel="stylesheet">'))
    print(('        <script src="js.js"></script>'))
    print(('        <link rel="stylesheet" href="styles.css">'))
    print('    </head>')
    print('')
    print('    <body>')
    print_branding()
    print('')
    print('        <div id="main-container" class="container">') #Main Container


#CardStart
def cardheader(header='Untitled Card',faicon='fas fa-cogs'):
    print('                    <!-- Bootstrap Card Start for '+header+' -->')
    print('                    <div class="card">')
    print('                        <div class="card-header">')
    print('                            <h5 class="card-title mb-0"><i class="'+faicon+' float-right"></i>'+header+'</h5>')
    print('                        </div>')
    print('')


#CardFooter
def cardfooter(text='Unmodified Footer Text'):
    #print('')
    #print('                        </div> <!-- Card Body End -->')
    print('')
    print('                        <!-- Card Footer Start -->')
    print('                        <div class="card-footer">')
    print('                            <small>'+text+'</small>')
    print('                        </div>')
    print('')
    print('                    <!-- Bootstrap Card End -->')
    print('                    </div>')
    print('')


#Breadcrumbs
def bcrumb(pagename):
    print('')
    print('            <!-- Navigation -->')
    print('            <nav aria-label="breadcrumb">')
    print('                <ol class="breadcrumb">')
    if pagename != 'Home':
        print('                    <li class="breadcrumb-item"><a href="xtendweb.cgi"><i class="fas fa-redo"></i> Home</a></li>')
        print('                    <li class="breadcrumb-item active" aria-current="page">'+pagename+'</li>')
    else:
        print('                    <li class="breadcrumb-item active" aria-current="page"><a href="xtendweb.cgi"><i class="fas fa-redo"></i> Home</a></li>')
    print('                </ol>')
    print('            </nav>')
    print('')


def print_modals():
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

    # Modal with no reload
    print('		<div class="modal fade" id="myModal-nl" tabindex="-1" role="dialog">')
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

    # Modal Large Width
    print('		<div class="modal fade" id="myModal-xl" tabindex="-1" role="dialog">')
    print('    		<div class="modal-dialog modal-xl modal-dialog-centered" role="document">')
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
