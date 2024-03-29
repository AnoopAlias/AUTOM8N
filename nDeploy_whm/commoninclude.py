#!/usr/bin/env python3

import os
import sys
import io
import subprocess
import yaml
import random
import platform
import psutil
import signal


installation_path = "/opt/nDeploy"  # Absolute Installation Path
ndeploy_control_file = installation_path+"/conf/ndeploy_control.yaml"
branding_file = installation_path+"/conf/branding.yaml"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
homedir_config_file = installation_path+"/conf/nDeploy-cluster/group_vars/all"
autom8n_version_info_file = installation_path+"/conf/version.yaml"
nginx_version_info_file = "/etc/nginx/version.yaml"
whm_terminal_log = installation_path+"/nDeploy_whm/term.log"


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def sighupnginx():
    for myprocess in psutil.process_iter():

        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline or '/usr/sbin/nginx' in mycmdline:
            nginxpid = myprocess.pid
            os.kill(nginxpid, signal.SIGHUP)


# nDeploy Control
if os.path.isfile(ndeploy_control_file):
    with open(ndeploy_control_file, 'r') as ndeploy_control_data_file:
        yaml_parsed_ndeploy_control_settings = yaml.safe_load(ndeploy_control_data_file)
    ndeploy_theme_color = yaml_parsed_ndeploy_control_settings.get("ndeploy_theme_color", "light")
    primary_color = yaml_parsed_ndeploy_control_settings.get("primary_color", "#177EAB")
    logo_url = yaml_parsed_ndeploy_control_settings.get("logo_url", "None")
    app_email = yaml_parsed_ndeploy_control_settings.get("app_email", "None")
    cpanel_documentation_link = yaml_parsed_ndeploy_control_settings.get("cpanel_documentation_link", "None")
    whm_documentation_link = yaml_parsed_ndeploy_control_settings.get("whm_documentation_link", "None")

else:
    ndeploy_theme_color = "light"
    primary_color = "#177EAB"
    logo_url = "None"
    app_email = "None"
    cpanel_documentation_link = "None"
    whm_documentation_link = "None"


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
with open(nginx_version_info_file, 'r') as nginx_version_info_yaml:
    nginx_version_info_yaml_parsed = yaml.safe_load(nginx_version_info_yaml)
nginx_version = nginx_version_info_yaml_parsed.get('nginx_version')
autom8n_version = autom8n_version_info_yaml_parsed.get('autom8n_version')


# Non-Toast Error func() for main pages
def print_nontoast_error(thenotice, thereason):
    print('            <div id="footer" class="row justify-content-center">')
    print('                <div class="col-lg-6 alert alert-danger">')
    print('                    <div class="text-center">')
    print('                        <span class="h1">')
    print('                            <i class="fas fa-exclamation"></i>')
    print('                        </span>')
    print(('                        <h3>'+thenotice+'</h3>'))
    print(('                        <h5>'+thereason+'</h5>'))
    if app_email != 'None':
        print(('                    <p>Please contact <a href="mailto:'+app_email+'">'+app_email+'</a> if you need assistance.</p>'))
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
    print(('<p>'+themessage+'</p></div>'))


# Error Toast DIV
def print_error_alert(themessage):
    print('<div class="alert alert-danger">')
    print_close_button()
    print(('<p>'+themessage+'</p></div>'))


# Warning Toast DIV
def print_warning_alert(themessage):
    print('<div class="alert alert-warning">')
    print_close_button()
    print(('<p>'+themessage+'</p></div>'))


# Info Toast DIV
def print_info_alert(themessage):
    print('<div class="alert alert-info">')
    print_close_button()
    print(('<p>'+themessage+'</p></div>'))


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


# Disabled Nginx Modules
def print_disabled():
    print('                                <div class="col-md-6">')
    if app_email != 'None':
        print(('                                <div class="btn btn-light btn-block" data-toggle="tooltip" title=" An additional '+brand+' module is required for this functionality. Contact '+app_email+' if you need assistance with this. ">Not Installed</div>'))
    else:
        print(('                                <div class="btn btn-light btn-block" data-toggle="tooltip" title=" An additional '+brand+' module is required for this functionality. ">Not Installed</div>'))
    print('                                </div>')


# RETURNS - Helps Keeps HTML Alignment
# Prepend Return
def return_prepend(theoption, hint):
    result = '<div class="d-flex w-50 align-items-center" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'
    return result


# Label Return
def return_label(theoption, hint):
    result = '<div class="d-flex w-50 justify-content-end align-items-center" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'
    return result


# Mutli Input Return
def return_multi_input(theoption, hint):
    result = '<label class="input-group-text" data-toggle="tooltip" title="'+hint+'">'+theoption+'</label>'
    return result


# Print Header
def print_header(title=''):
    # Set sys.stdout and sys.stderr to UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    print('Content-Type: text/html')
    print('')
    print('<!doctype html>')
    print('<html lang="en">')
    print('    <head>')
    print('        <!-- Required meta tags -->')
    print('        <meta charset="utf-8">')
    print('        <meta name="viewport" content="width=device-width, initial-scale=1">')
    print(('        <title>'+brand+' - '+title+'</title>'))
    print('        <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>')
    print('        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>')
    print('        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>')
    print('        <link href="https://fonts.googleapis.com/css?family=Poppins&display=swap" rel="stylesheet">')
    print('        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css" rel="stylesheet">')
    print('        <script src="js.js"></script>')
    print('        <link rel="stylesheet" href="styles.css">')
    print('    </head>')
    print('')
    print('    <!-- Body Start -->')
    print(('    <body class="ndeploy-theme-'+ndeploy_theme_color+'">'))
    print('        <header id="main-header" class="d-flex justify-content-between align-items-center">')
    print('            <div class="logo">')
    print('                <h4>')
    if logo_url != 'None':
        print(('                <a href="xtendweb.cgi"><img border="0" alt="'+brand+' Logo" class="logo-url" src="'+logo_url+'"></a>'))
    elif brand_logo != 'xtendweb.png':
        print(('                <a href="xtendweb.cgi"><img border="0" alt="'+brand+' Logo" src="'+brand_logo+'" width="48" height="48"></a><span>'+brand+'</span>'))
    elif ndeploy_theme_color == 'dark':
        print(('                <a href="xtendweb.cgi"><img border="0" alt="'+brand+' Logo" src="xtendweb_light.png" width="48" height="48"></a><span>'+brand+'</span>'))
    elif ndeploy_theme_color == 'light':
        print(('                <a href="xtendweb.cgi"><img border="0" alt="'+brand+' Logo" src="xtendweb_dark.png" width="48" height="48"></a><span>'+brand+'</span>'))

    print('                </h4>')
    print('            </div>')
    print('            <div class="d-flex">')
    # print(('                <div class="buttons p-2"><a class="btn btn-'+ndeploy_theme_color+'" href="ndeploy_control.cgi" data-toggle="tooltip" title="'+brand+'&nbsp;Control"><i class="fas fa-tools"></i> <span class="d-none d-lg-inline-block">'+brand+'&nbsp;Control</span></a></div>'))
    if app_email != 'None':
        print(('            <div class="buttons p-2"><a class="btn btn-'+ndeploy_theme_color+'" href="mailto:'+app_email+'" data-toggle="tooltip" title="Support"><i class="fas fa-envelope"></i> <span class="d-none d-lg-inline-block">Support</span></a></div>'))
    if whm_documentation_link != "None":
        print(('                <div class="buttons p-2"><a class="btn btn-'+ndeploy_theme_color+'" target="_blank" href="'+whm_documentation_link+'" data-toggle="tooltip" title="WHM Docs for '+brand+'"><i class="fas fa-book-open"></i> <span class="d-none d-lg-inline-block">WHM Docs</span></a></div>'))
    else:
        print(('                <div class="buttons p-2"><a class="btn btn-'+ndeploy_theme_color+'" target="_blank" href="help.txt" data-toggle="tooltip" title="WHM Docs for '+brand+'"><i class="fas fa-book-open"></i> <span class="d-none d-lg-inline-block">WHM Docs</span></a></div>'))

    print('            </div>')
    print('        </header>')
    print('')
    print('        <!-- Main Container Start -->')
    print('        <div id="main-container" class="container">')


# Terminal Section
def display_term():
    print('        <div class="modal" id="terminal" tabindex="-1" role="dialog">')
    print('            <div class="modal-dialog" role="document">')
    if ndeploy_theme_color == 'dark':
        print('                <div class="modal-content bg-dark text-white">')
    if ndeploy_theme_color == 'light':
        print('                <div class="modal-content bg-light text-dark">')
    print('                    <div class="modal-header">')
    print('                        <h4 class="modal-title">Command Output <span id="processing"><i class="fas fa-spinner fa-spin"></i></span></h4>')
    print('                        <div class="btn-group">')
    print('                            <button class="icon clearTerminalWindow" data-toggle="tooltip" data-original-title="Clear Terminal"><i class="fas fa-eraser"><span class="sr-only">Clear Terminal Window</span></i></button>')
    print('                            <button class="icon close modalMinimize" data-toggle="tooltip" data-original-title="Minimize/Maximize"><i class="fa fa-minus"><span class="sr-only">Close</span></i></button>')
    print('                        </div>')
    print('                    </div>')
    print('                    <div id="terminal-panel" class="modal-body">Retrieving last terminal function executed...</div>')
    print('                </div>')
    print('            </div>')
    print('        </div>')


# Terminal Call with pre/post output
# Adding a preEcho clears terminal window
def terminal_call(runCmd='', preEcho='', postEcho='', shellEnvironment=''):
    if preEcho:
        procExe = subprocess.Popen('echo -e "<em>$(date) [$(hostname)] -> <strong>'+preEcho+'</strong></em>\n" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()
    if runCmd != '':
        if shellEnvironment != '':
            procExe = subprocess.Popen(runCmd+' >> '+whm_terminal_log, env=shellEnvironment, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()
        else:
            procExe = subprocess.Popen(runCmd+' >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()
    if postEcho:
        procExe = subprocess.Popen('echo -e "\n<em>$(date) [$(hostname)] -> <strong>'+postEcho+'</strong></em>" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()


# Input Display
def print_input_fn(label='Label', hint='Hint', inputValue='', inputName='', buttonID='', hiddenName='', hiddenValue=''):
    validateRandom = str(random.randint(0, 100000))
    print('                                        <div class="input-group">')
    print('                                            <div class="input-group-prepend input-group-prepend-min">')
    print(('                                                <label for="validate-'+validateRandom+'" class="input-group-text" data-toggle="tooltip" title="'+hint+'">'+label+'</label>'))
    print('                                            </div>')
    print(('                                            <input class="form-control" id="validate-'+validateRandom+'" value="'+str(inputValue)+'" type="text" name="'+inputName+'" required>'))

    if buttonID:
        print(('                                            <input hidden name="'+hiddenName+'" value="'+hiddenValue+'">'))
        print('                                            <div class="input-group-append">')
        print(('                                                <button id="'+buttonID+'" class="btn btn-outline-primary" type="submit">'))
        print(('                                                    <span class="sr-only">'+hiddenValue+'</span><i class="fas fa-plus"></i>'))
        print('                                                </button>')
        print('                                            </div>')

    print(('                                            <div class="invalid-tooltip">'+hint+'</div>'))
    print('                                        </div>')


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


# SelectBox Display
def print_select_fn(label='Label', hint='Hint', selectQuery='', selectName='name', *selectOptions):
    validateRandom = str(random.randint(0, 100000))
    print('                         <div class="input-group">')
    print('                             <div class="input-group-prepend input-group-prepend-min">')
    print(('                                 <label for="validate-'+validateRandom+'" class="input-group-text" data-toggle="tooltip" title="'+hint+'">'+label+'</label>'))
    print('                             </div>')
    print(('                             <select id="validate-'+validateRandom+'" name="'+selectName+'" class="custom-select">'))
    for option in selectOptions:
        if selectQuery == option:
            print(('                         <option value="'+option+'" selected>'+option+'</option>'))
        else:
            print(('                         <option value="'+option+'">'+option+'</option>'))
    print('                             </select>')
    print('                         </div>')


# Card Start
def cardheader(header='Untitled Card', faicon='fas fa-cogs'):
    print('')
    print(('                    <!-- Bootstrap Card Start for '+header+' -->'))
    if ndeploy_theme_color == 'dark':
        print(('                    <div class="card mb-4 text-white bg-'+ndeploy_theme_color+' shadow-sm">'))
    if ndeploy_theme_color == 'light':
        print(('                    <div class="card mb-4 text-dark bg-'+ndeploy_theme_color+' shadow-sm">'))
    if header != '':
        print('                        <div class="card-header">')
        print(('                            <h3 class="card-title mb-0"><i class="'+faicon+' float-right"></i>'+header+'</h3>'))
        print('                        </div>')
    print('')


# Card Footer
def cardfooter(text='Unmodified Footer Text'):
    if text != '':
        print('')
        print('                        <!-- Card Footer Start -->')
        print('                        <div class="card-footer text-center">')
        print(('                            <small>'+text+'</small>'))
        print('                        </div>')
    print('')
    print('                    <!-- Bootstrap Card End -->')
    print('                    </div>')
    print('')


# Breadcrumbs
def bcrumb(pagename="Unnamed Page", active_fa_icon="fas fa-tools"):
    print('')
    print('            <!-- Navigation -->')
    print('            <nav aria-label="breadcrumb">')
    print('                <ol class="breadcrumb justify-content-md-center">')
    if pagename != 'Main':
        print('                    <li class="breadcrumb-item"><a href="xtendweb.cgi"><i class="fas fa-tools"></i>&nbsp;Main</a></li>')
        print('                     <li class="breadcrumb-item" aria-current="page"><a style="color:'+primary_color+';" href="ndeploy_control.cgi"><i class="fas fa-tools"></i>&nbsp;Extra</a></li>')
    else:
        print(('                    <li class="breadcrumb-item active" aria-current="page"><a style="color:'+primary_color+' !important;" href="xtendweb.cgi"><i class="fas fa-tools"></i>&nbsp;Main</a></li>'))
        print('                     <li class="breadcrumb-item" aria-current="page"><a href="ndeploy_control.cgi"><i class="fas fa-tools"></i>&nbsp;Extra</a></li>')
    print('                </ol>')
    print('            </nav>')
    print('')
