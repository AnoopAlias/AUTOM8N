#!/usr/bin/env python

import os
import yaml

installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
homedir_config_file = installation_path+"/conf/nDeploy-cluster/group_vars/all"


#Theming Support
if os.path.isfile(installation_path+"/conf/theming.yaml"):
    with open(installation_path+"/conf/theming.yaml", 'r') as theme_data_file:
        yaml_parsed_theme = yaml.safe_load(theme_data_file)
    heading_background_color = yaml_parsed_theme.get("heading_background_color","#FFFFFF")
    heading_foreground_color = yaml_parsed_theme.get("heading_foreground_color","#3D4366")
    body_background_color = yaml_parsed_theme.get("body_background_color","#F1F1F8")
    card_color = yaml_parsed_theme.get("card_color","light")
    text_color = yaml_parsed_theme.get("text_color","dark")
    breadcrumb_active_color = yaml_parsed_theme.get("breadcrumb_active_color","#121212")
    heading_height = yaml_parsed_theme.get("heading_height","50")
    header_button_color = yaml_parsed_theme.get("header_button_color","primary")
    icon_height = yaml_parsed_theme.get("icon_height","48")
    icon_width = yaml_parsed_theme.get("icon_width","48")
    logo_not_icon = yaml_parsed_theme.get("logo_not_icon","disabled")
    logo_height = yaml_parsed_theme.get("logo_height","29")
    logo_width = yaml_parsed_theme.get("logo_width","242")
    logo_url = yaml_parsed_theme.get("logo_url","https://autom8n.com/assets/img/logo-dark.png")

    app_title = yaml_parsed_theme.get("app_title","AUTOM8N")
    theme_data_file.close()

#Branding Support
if os.path.isfile(installation_path+"/conf/branding.yaml"):
    with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
        yaml_parsed_brand = yaml.safe_load(brand_data_file)
    brand_logo = yaml_parsed_brand.get("brand_logo", "xtendweb.png")
    brand_name = yaml_parsed_brand.get("brand", "AUTOM8N")
    brand_group = yaml_parsed_brand.get("brand_group", "NGINX AUTOMATION")

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
    print(('Content-Type: text/html'))
    print((''))
    print(('<html>'))
    print(('    <head>'))
    print(('        <title>'+app_title+' - '+title+'</title>'))
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
    print('        <header id="main-header" class="d-flex justify-content-between align-items-center" style="height:'+heading_height+';color:'+heading_foreground_color+';background-color:'+heading_background_color+'">')
    print('            <div class="logo">')
    print('                <h4>')
    if logo_not_icon == 'enabled':
        print('                    <a href="xtendweb.cgi"><img border="0" src="'+logo_url+'" width="'+logo_width+'" height="'+logo_height+'"></a>')
    else:
        print('                    <a href="xtendweb.cgi"><img border="0" src="'+brand_logo+'" width="'+icon_width+'" height="'+icon_height+'"></a>'+brand_name)
    print('                </h4>')
    print('            </div>')
    print('            <div class="d-flex header-buttons">')
    print('                <div class="buttons p-1"><a class="btn btn-'+header_button_color+'" href="branding.cgi"> branding <i class="fas fa-code-branch"></i></a></div>')
    print('                <div class="buttons p-1"><a class="btn btn-'+header_button_color+'" href="bootstrap_layout.cgi"> bootstrap layout <i class="fas fa-swatchbook"></i></a></div>')
    print('                <div class="buttons p-1"><a class="btn btn-'+header_button_color+'" target="_blank" href="help.txt"> docs <i class="fas fa-book-open"></i></a></div>')
    print('            </div>')
    print('        </header>')
    print('')
    print('        <!-- Main Container Start -->')
    print('        <div id="main-container" class="container">') #Main Container


#CardStart
def cardheader(header='Untitled Card',faicon='fas fa-cogs'):
    print('                    <!-- Bootstrap Card Start for '+header+' -->')
    print('                    <div class="card mb-4 text-'+text_color+' bg-'+card_color+'">')
    print('                        <div class="card-header">')
    print('                            <h5 class="card-title mb-0"><i class="'+faicon+' float-right"></i>'+header+'</h5>')
    print('                        </div>')
    print('')


#CardFooter
def cardfooter(text='Unmodified Footer Text'):
    print('')
    print('                        <!-- Card Footer Start -->')
    print('                        <div class="card-footer">')
    print('                            <small><center>'+text+'</center></small>')
    print('                        </div>')
    print('')
    print('                    <!-- Bootstrap Card End -->')
    print('                    </div>')
    print('')


#Breadcrumbs
def bcrumb(pagename="Unnamed Page",active_fa_icon="fas fa-infinity"):
    print('')
    print('            <!-- Navigation -->')
    print('            <nav aria-label="breadcrumb">')
    print('                <ol class="breadcrumb justify-content-md-center">')
    if pagename != 'Home':
        print('                    <li class="breadcrumb-item"><a href="xtendweb.cgi"><i class="fas fa-infinity"></i>&nbsp;Home</a></li>')
        print('                    <li style="color:'+breadcrumb_active_color+'" class="breadcrumb-item active" aria-current="page"><i class="'+active_fa_icon+'"></i>&nbsp;'+pagename+'</li>')
    else:
        print('                    <li class="breadcrumb-item active" aria-current="page"><a style="color:'+breadcrumb_active_color+' !important;" href="xtendweb.cgi"><i class="fas fa-infinity"></i>&nbsp;Home</a></li>')
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
    print('        <div class="modal fade" id="myModal-nl" tabindex="-1" role="dialog"> ')
    print('            <div class="modal-dialog modal-xl modal-dialog-centered" role="document">')
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

    # Modal Large Width
    print('        <div class="modal fade" id="myModal-xl" tabindex="-1" role="dialog">')
    print('            <div class="modal-dialog modal-xl modal-dialog-centered" role="document">')
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

    # Toast
    print('        <div class="toast fade hide" id="myToast" role="alert" aria-live="assertive" aria-atomic="true">')
    print('            <div class="toast-header">')
    print('                <strong class="mr-auto">Command Output</strong>')
    print('                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                    <span aria-hidden="true">&times;</span>')
    print('                </button>')
    print('            </div>')
    print('            <div class="toast-body">')
    print('            </div>')
    print('        </div>')

    # Toast with long autohide
    print('        <div class="toast fade hide" id="myToastnohide" role="alert" aria-live="assertive" aria-atomic="true" data-delay="5000">')
    print('            <div class="toast-header">')
    print('                <strong class="mr-auto">Command Output</strong>')
    print('                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                    <span aria-hidden="true">&times;</span>')
    print('                </button>')
    print('            </div>')
    print('            <div class="toast-body">')
    print('            </div>')
    print('        </div>')

    # Toast with no reload
    print('        <div class="toast fade hide" id="myToast-nl" role="alert" aria-live="assertive" aria-atomic="true">')
    print('            <div class="toast-header">')
    print('                <strong class="mr-auto">Command Output</strong>')
    print('                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                    <span aria-hidden="true">&times;</span>')
    print('                </button>')
    print('            </div>')
    print('            <div class="toast-body">')
    print('            </div>')
    print('        </div>')

    # Toastback
    print('        <div class="toast fade hide" id="myToastback" role="alert" aria-live="assertive" aria-atomic="true">')
    print('            <div class="toast-header">')
    print('                <strong class="mr-auto">Command Output</strong>')
    print('                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                    <span aria-hidden="true">&times;</span>')
    print('                </button>')
    print('            </div>')
    print('            <div class="toast-body">')
    print('            </div>')
    print('        </div>')
