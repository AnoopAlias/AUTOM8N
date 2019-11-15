#!/usr/bin/env python

import os
import yaml
import socket


installation_path = "/opt/nDeploy"  # Absolute Installation Path
ndeploy_control_file = installation_path+"/conf/ndeploy_control.yaml"
branding_file = installation_path+"/conf/branding.yaml"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
homedir_config_file = installation_path+"/conf/nDeploy-cluster/group_vars/all"
autom8n_version_info_file = installation_path+"/conf/version.yaml"
nginx_version_info_file = "/etc/nginx/version.yaml"


# nDeploy Control
if os.path.isfile(ndeploy_control_file):
    with open(ndeploy_control_file, 'r') as ndeploy_control_data_file:
        yaml_parsed_ndeploy_control_settings = yaml.safe_load(ndeploy_control_data_file)
    ndeploy_theme_color = yaml_parsed_ndeploy_control_settings.get("ndeploy_theme_color", "light")
    primary_color = yaml_parsed_ndeploy_control_settings.get("primary_color", "#121212")
    logo_url = yaml_parsed_ndeploy_control_settings.get("logo_url", "None")
    app_email = yaml_parsed_ndeploy_control_settings.get("app_email", "None")
else:
    ndeploy_theme_color = "light"
    primary_color = "#121212"
    logo_url = "None"
    app_email = "None"


# Branding Support
if os.path.isfile(branding_file):
    with open(branding_file, 'r') as brand_data_file:
        yaml_parsed_brand = yaml.safe_load(brand_data_file)
    brand_logo = yaml_parsed_brand.get("brand_logo", "xtendweb.png")
    brand = yaml_parsed_brand.get("brand", "AUTOM8N")
    brand_group = yaml_parsed_brand.get("brand_group", "NGINX AUTOMATION")
else:
    brand_logo = "xtendweb.png"
    brand = "AUTOM8N"
    brand_group = "NGINX AUTOMATION"


# Get version of Nginx and plugin
with open(autom8n_version_info_file, 'r') as autom8n_version_info_yaml:
    autom8n_version_info_yaml_parsed = yaml.safe_load(autom8n_version_info_yaml)

# Bypass Cloudlinux perms
if os.access(nginx_version_info_file, os.R_OK): # Check for read access
    with open(nginx_version_info_file, 'r') as nginx_version_info_yaml:
        nginx_version_info_yaml_parsed = yaml.safe_load(nginx_version_info_yaml)
    nginx_version = nginx_version_info_yaml_parsed.get('nginx_version')
else:
    nginx_version = ""
autom8n_version = autom8n_version_info_yaml_parsed.get('autom8n_version')


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


def return_label(theoption, hint):
    result = '<div class="d-flex w-50 justify-content-end align-items-center" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'
    return result


def return_prepend(theoption, hint):
    result = '<div class="d-flex w-50 align-items-center" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'
    return result

def return_sys_tip(theoption, hint):
    result = '<div class="col-6 alert" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'
    return result


# Non-Toast Error func() for main pages
def print_nontoast_error(thenotice, thereason):
    print('            <div id="footer" class="row justify-content-center">')
    print('                <div class="col-lg-6 alert alert-danger">')
    print('                    <div class="text-center">')
    print('                        <span class="h1">')
    print('                            <i class="fas fa-exclamation"></i>')
    print('                        </span>')
    print('                        <h3>'+thenotice+'</h3>')
    print('                        <h5>'+thereason+'</h5>')
    if app_email != 'None':
        print('                    <p>Please contact <a href="mailto:'+app_email+'">'+app_email+'</a> if you need assistance.</p>')
    print('                    </div>')
    print('                </div>')
    print('            </div>')


# TOASTS
def print_close_button():
    print('<button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close"><span aria-hidden="true">&times;</span></button>')


# Sucess Toast DIV
def print_success_alert(themessage):
    print('<div class="alert alert-success">')
    print_close_button()
    print('<p>'+themessage+'</p></div>')


# Error Toast DIV
def print_error_alert(themessage):
    print('<div class="alert alert-danger">')
    print_close_button()
    print('<p>'+themessage+'</p></div>')


# Warning Toast DIV
def print_warning_alert(themessage):
    print('<div class="alert alert-warning">')
    print_close_button()
    print('<p>'+themessage+'</p></div>')


# Info Toast DIV
def print_info_alert(themessage):
    print('<div class="alert alert-info">')
    print_close_button()
    print('<p>'+themessage+'</p></div>')


# Forbidden Toast with icon
def print_forbidden():
    print_error_alert('Forbidden')


# Error Toast with icon
def print_error(themessage):
    print_error_alert(themessage)


# Success Toast with icon
def print_success(themessage):
    print_success_alert(themessage)


# Warning Toast with icon
def print_warning(themessage):
    print_warning_alert(themessage)


# Info Toast with icon
def print_info(themessage):
    print_info_alert(themessage)


def print_sys_tip(theoption, hint):
    print('<div class="col-md-6 alert" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>')


def print_disabled():
    print('                                <div class="col-md-6">')
    if app_email != 'None':
        print('                                <div class="btn btn-light btn-block" data-toggle="tooltip" title=" An additional '+brand+' module is required for this functionality. Contact '+app_email+' if you need assistance with this. ">Not Installed</div>')
    else:
        print('                                <div class="btn btn-light btn-block" data-toggle="tooltip" title=" An additional '+brand+' module is required for this functionality. ">Not Installed</div>')
    print('                                </div>')


def print_forbidden_wrapper():
    print('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body"><i class="fas fa-exclamation"></i><p>Forbidden</p></div></div>')


def print_error_wrapper(themessage):
    print('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body"><i class="fas fa-exclamation"></i><p>'+themessage+'</p></div></div>')


def print_success_wrapper(themessage):
    print('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body text-center"><i class="fas fa-thumbs-up"></i><p>'+themessage+'</p></div></div>')


def return_multi_input(theoption, hint):
    result = '<div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'
    return result


def print_loader():
    print('')
    print('        <div id="loader"><i class="fas fa-infinity fa-spin"></i></div>')
    print('')


# Print Header
def print_header(title=''):
    print('Content-Type: text/html')
    print('')
    print('<!doctype html>')
    print('<html lang="en">')
    print('    <head>')
    print('        <!-- Required meta tags -->')
    print('        <meta charset="utf-8">')
    print('        <meta name="viewport" content="width=device-width, initial-scale=1">')
    print('        <title>'+brand+' - '+title+'</title>')
    print('        <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>')
    print('        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>')
    print('        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>')
    print('        <link href="https://fonts.googleapis.com/css?family=Poppins&display=swap" rel="stylesheet">')
    print('        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.1/css/all.min.css" rel="stylesheet">')
    print('        <script src="js.js"></script>')
    print('        <link rel="stylesheet" href="styles.css">')
    print('    </head>')
    print('')
    print('    <!-- Body Start -->')
    print('    <body class="ndeploy-theme-'+ndeploy_theme_color+'">')
    print('        <header id="main-header" class="d-flex justify-content-between align-items-center">')
    print('            <div class="logo">')
    print('                <h4>')
    if logo_url != 'None':
        print('                <a href="xtendweb.live.py"><img border="0" alt="'+brand+'" class="logo-url" src="'+logo_url+'"></a>')
    else:
        if ndeploy_theme_color == 'dark':
            print('                <a href="xtendweb.live.py"><img border="0" alt="'+brand+'" src="xtendweb_light.png" width="48" height="48"></a><span>'+brand+'</span>')
        else:
            print('                <a href="xtendweb.live.py"><img border="0" alt="'+brand+'" src="xtendweb_dark.png" width="48" height="48"></a><span>'+brand+'</span>')
    print('                </h4>')
    print('            </div>')
    print('            <div class="d-flex">')
    if app_email != 'None':
        print('                <div class="buttons p-2"><a class="btn btn-'+ndeploy_theme_color+'" href="mailto:'+app_email+'" data-toggle="tooltip" title="Support"><i class="fas fa-envelope"></i> <span class="d-none d-lg-inline-block">Support</span></a></div>')
    print('                <div class="buttons p-2"><a class="btn btn-'+ndeploy_theme_color+'" target="_blank" href="help.txt" data-toggle="tooltip" title="Documentation"><i class="fas fa-book-open"></i> <span class="d-none d-lg-inline-block">Documentation</span></a></div>')
    print('            </div>')
    print('        </header>')
    print('')
    print('        <!-- Main Container Start -->')
    print('        <div id="main-container" class="container">') #Main Container


# Terminal Section
def display_term():
    print('        <div class="modal" id="terminal" tabindex="-1" role="dialog">')
    print('            <div class="modal-dialog" role="document">')
    if ndeploy_theme_color == 'dark':
        print('                <div class="modal-content bg-dark text-white">')
    if ndeploy_theme_color == 'light':
        print('                <div class="modal-content bg-light text-dark">')
    print('                    <div class="modal-header">')
    print('                        <h4 class="modal-title">Command Output <span id="processing">- Processing: <i class="fas fa-spinner fa-spin"></i></span></h4>')
    print('                        <button class="close modalMinimize"> <i class="fa fa-minus"><span class="sr-only">Close</span></i> </button>')
    print('                    </div>')
    print('                    <div id="terminal-panel" class="modal-body">Retrieving last terminal function executed...</div>')
    print('                </div>')
    print('            </div>')
    print('        </div>')


# Footer Section
def print_footer():
    print('        </div> <!-- Main Container End -->')
    display_term()
    print('    </body> <!-- Body End -->')
    print('</html>')


# Simple Header
def print_simple_header():
    print('Content-Type: text/html')
    print('')
    print('<html>')
    print('    <head>')
    print('    <meta charset="utf-8">')
    print('    <meta name="viewport" content="width=device-width, initial-scale=1">')
    print('    </head>')
    print('    <body>')


# Simple Footer
def print_simple_footer():
    print('    </body>')
    print('</html>')


# Card Start
def cardheader(header='Untitled Card', faicon='fas fa-cogs'):
    print('')
    print('                    <!-- Bootstrap Card Start for '+header+' -->')
    if ndeploy_theme_color == 'dark':
        print('                    <div class="card mb-4 text-white bg-'+ndeploy_theme_color+'">')
    if ndeploy_theme_color == 'light':
        print('                    <div class="card mb-4 text-dark bg-'+ndeploy_theme_color+'">')
    if header != '':
        print('                        <div class="card-header">')
        print('                            <h5 class="card-title mb-0"><i class="'+faicon+' float-right"></i>'+header+'</h5>')
        print('                        </div>')
    print('')


# Card Footer
def cardfooter(text='Unmodified Footer Text'):
    if text != '':
        print('')
        print('                        <!-- Card Footer Start -->')
        print('                        <div class="card-footer">')
        print('                            <small><center>'+text+'</center></small>')
        print('                        </div>')
    print('')
    print('                    <!-- Bootstrap Card End -->')
    print('                    </div>')
    print('')


# Breadcrumbs
def bcrumb(pagename="Unnamed Page", active_fa_icon="fas fa-infinity"):
    print('')
    print('            <!-- Navigation -->')
    print('            <nav aria-label="breadcrumb">')
    print('                <ol class="breadcrumb justify-content-md-center">')
    if pagename != 'Home':
        print('                    <li class="breadcrumb-item"><a href="xtendweb.live.py"><i class="fas fa-infinity"></i>&nbsp;Home</a></li>')
        print('                    <li style="color:'+primary_color+'" class="breadcrumb-item active" aria-current="page"><i class="'+active_fa_icon+'"></i>&nbsp;'+pagename+'</li>')
    else:
        print('                    <li class="breadcrumb-item active" aria-current="page"><a style="color:'+primary_color+' !important;" href="xtendweb.live.py"><i class="fas fa-infinity"></i>&nbsp;Home</a></li>')
    print('                </ol>')
    print('            </nav>')
    print('')
