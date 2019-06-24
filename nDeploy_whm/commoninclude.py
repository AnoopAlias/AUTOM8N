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
    heading_background_color = "#121212"
    heading_foreground_color = "ghostwhite"
    print('        <header id="main-header" style="color:'+heading_foreground_color+';background-color:'+heading_background_color+'">')
    print('            '+branding_print_support())
    print('            <div class="logo">')
    print('                <h4>')
    print('                    <a href="xtendweb.cgi"><img border="0" src="'+branding_print_logo_name()+'" width="48" height="48"></a>'+branding_print_banner())
    print('                </h4>')
    print('            </div>')
    print('        </header>')


def return_green(theoption, hint):
    result = '<div class="col-md-6 d-flex align-items-center justify-content-end"><div class="label label-info" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'
    return result


def print_green(theoption, hint):
    print(('<div class="col-md-6 label" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'))


def print_red(theoption, hint):
    print(('<div class="col-md-6 label" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'))


def return_red(theoption, hint):
    result = '<div class="col-md-6 d-flex align-items-center justify-content-end"><div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'
    return result


def print_forbidden():
    print(('<i class="fas fa-exclamation"></i><p>Forbidden</p>'))


def print_error(themessage):
    print(('<i class="fas fa-exclamation"></i><p>'+themessage+'</p>'))


def print_success(themessage):
    print(('<i class="fas fa-thumbs-up"></i><p>'+themessage+'</p>'))


def print_error_alert(themessage):
    print(('<div class="alert alert-danger text-left">'+themessage+'</div>'))


def print_sys_tip(theoption, hint):
    print(('<div class="col-md-6 alert alert-light" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'))


def print_disabled():
    print(('<div class="col-md-6"><div class="btn btn-light btn-block btn-not-installed" data-toggle="tooltip" title="An additional nginx module is required for this functionality">Not Installed</div></div>'))


def print_forbidden_wrapper():
    print(('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body"><i class="fas fa-exclamation"></i><p>Forbidden</p></div></div>'))


def print_error_wrapper(themessage):
    print(('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body"><i class="fas fa-exclamation"></i><p>'+themessage+'</p></div></div>'))


def print_success_wrapper(themessage):
    print(('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body text-center"><i class="fas fa-thumbs-up"></i><p>'+themessage+'</p></div></div>'))


def print_multi_input(theoption, hint):
    print(('<div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'))


def return_multi_input(theoption, hint):
    result = '<div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'
    return result


def print_loader():
    print('')
    print(('        <div id="loader"><i class="fas fa-infinity fa-spin"></i></div>'))
    print('')


def print_header(title=''):
    body_background_color = "#101010"
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
    print('    <!-- Body Start -->')
    print('    <body style="background-color:'+body_background_color+'">')
    print_branding()
    print('')
    print('        <!-- Main Container Start -->')
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
def bcrumb(pagename="Unnamed Page",active_page_color="ghostwhite",active_fa_icon="fas fa-database",):
    print('')
    print('            <!-- Navigation -->')
    print('            <nav aria-label="breadcrumb">')
    print('                <ol class="breadcrumb justify-content-md-center">')
    if pagename != 'Home':
        print('                    <li class="breadcrumb-item"><a href="xtendweb.cgi"><i class="fas fa-redo"></i>&nbsp;Home</a></li>')
        print('                    <li style="color:'+active_page_color+'" class="breadcrumb-item active" aria-current="page"><i class="'+active_fa_icon+'"></i>&nbsp;'+pagename+'</li>')
    else:
        print('                    <li class="breadcrumb-item active" aria-current="page"><a style="color:'+active_page_color+' !important;" href="xtendweb.cgi"><i class="fas fa-redo"></i>&nbsp;Home</a></li>')
    print('                </ol>')
    print('            </nav>')
    print('')


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass

def safenginxreload():
    nginx_status = False
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if '/usr/sbin/nginx' in mycmdline and 'reload' in mycmdline:
            nginx_status = True
            break
    if not nginx_status:
        with open(os.devnull, 'w') as FNULL:
            subprocess.Popen(['/usr/sbin/nginx', '-s', 'reload'], stdout=FNULL, stderr=subprocess.STDOUT)


def sighupnginx():
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
            nginxpid = myprocess.pid
            os.kill(nginxpid, signal.SIGHUP)        


def print_modals():

    # Modal
    print('        <div class="modal fade" id="myModal" tabindex="-1" role="dialog">')
    print('            <div class="modal-dialog modal-dialog-centered" role="document">')
    print('                <div class="modal-content">')
    print('                    <div class="modal-header">')
    print('                        <h4 class="modal-title">Command Output</h4>')
    print('                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">')
    print('                            <span aria-hidden="true">&times;</span>')
    print('                        </button>')
    print('                    </div>')
    print('                    <div class="modal-body">')
    print('                    </div>')
    print('                    <div class="modal-footer">')
    print('                        <button type="button" class="btn btn-outline-secondary" data-dismiss="modal">Close</button>')
    print('                    </div>')
    print('                </div>')
    print('            </div>')
    print('        </div>')

    # Modal with no reload
    print('		<div class="modal fade" id="myModal-nl" tabindex="-1" role="dialog"> ')
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

    # Toast
    print('     <div class="toast fade hide" id="myToast" role="alert" aria-live="assertive" aria-atomic="true">')
    print('         <div class="toast-header">')
    print('             <strong class="mr-auto">Command Output</strong>')
    print('             <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                 <span aria-hidden="true">&times;</span>')
    print('             </button>')
    print('         </div>')
    print('         <div class="toast-body">')
    print('         </div>')
    print('     </div>')

    # Toast with long autohide
    print('     <div class="toast fade hide" id="myToastnohide" role="alert" aria-live="assertive" aria-atomic="true" data-delay="5000">')
    print('         <div class="toast-header">')
    print('             <strong class="mr-auto">Command Output</strong>')
    print('             <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                 <span aria-hidden="true">&times;</span>')
    print('             </button>')
    print('         </div>')
    print('         <div class="toast-body">')
    print('         </div>')
    print('     </div>')

    # Toast with no reload
    print('     <div class="toast fade hide" id="myToast-nl" role="alert" aria-live="assertive" aria-atomic="true">')
    print('         <div class="toast-header">')
    print('             <strong class="mr-auto">Command Output</strong>')
    print('             <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                 <span aria-hidden="true">&times;</span>')
    print('             </button>')
    print('         </div>')
    print('         <div class="toast-body">')
    print('         </div>')
    print('     </div>')

    # Toastback
    print('     <div class="toast fade hide" id="myToastback" role="alert" aria-live="assertive" aria-atomic="true">')
    print('         <div class="toast-header">')
    print('             <strong class="mr-auto">Command Output</strong>')
    print('             <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                 <span aria-hidden="true">&times;</span>')
    print('             </button>')
    print('         </div>')
    print('         <div class="toast-body">')
    print('         </div>')
    print('     </div>')
