#!/usr/bin/env python

import os
import cgitb
import yaml
try:
    import simplejson as json
except ImportError:
    import json
from commoninclude import close_cpanel_liveapisock, print_header, bcrumb, cardheader, cardfooter, print_footer


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
app_template_file = installation_path+"/conf/apptemplates.yaml"
cpaneluser = os.environ["USER"]
user_app_template_file = installation_path+"/conf/"+cpaneluser+"_apptemplates.yaml"


cgitb.enable()
close_cpanel_liveapisock()

cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
with open(cpuserdatajson, 'r') as cpaneluser_data_stream:
    json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
main_domain = json_parsed_cpaneluser.get('main_domain')
# parked_domains = yaml_parsed_cpaneluser.get('parked_domains') # This data is irrelevant as parked domain list is in ServerAlias
addon_domains_dict = json_parsed_cpaneluser.get('addon_domains') # So we know which addon is mapped to which sub-domain
sub_domains = json_parsed_cpaneluser.get('sub_domains')

# Settings Lock
if os.path.exists("/var/cpanel/users.cache/" + cpaneluser):
    with open("/var/cpanel/users.cache/" + cpaneluser) as users_file:
        json_parsed_cpusersfile = json.load(users_file)
    hostingplan_filename = json_parsed_cpusersfile.get('PLAN', 'default').encode('utf-8').replace(' ', '_')
else:
    hostingplan_filename = 'default'
if hostingplan_filename == 'undefined' or hostingplan_filename == 'default':
    if os.path.isfile(installation_path+"/conf/domain_data_default_local.yaml"):
        TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local.yaml"
    else:
        TEMPLATE_FILE = installation_path+"/conf/domain_data_default.yaml"
else:
    if os.path.isfile(installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"):
        TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local_"+hostingplan_filename+".yaml"
    else:
        if os.path.isfile(installation_path+"/conf/domain_data_default_local.yaml"):
            TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local.yaml"
        else:
            TEMPLATE_FILE = installation_path+"/conf/domain_data_default.yaml"
with open(TEMPLATE_FILE, 'r') as templatefile_data_stream:
    yaml_parsed_templatefile = yaml.safe_load(templatefile_data_stream)
settings_lock = yaml_parsed_templatefile.get('settings_lock', 'disabled')

# Print domain and all the fixins.
def print_domain_stacks(mydomain, mydomainvisual):
    profileyaml = installation_path + "/domain-data/" + mydomain

    if os.path.isfile(profileyaml):
        
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        
        # App Settings
        backend_category = yaml_parsed_profileyaml.get('backend_category')
        backend_version = yaml_parsed_profileyaml.get('backend_version')
        backend_path = yaml_parsed_profileyaml.get('backend_path')
        apptemplate_code = yaml_parsed_profileyaml.get('apptemplate_code')

        # Get the human friendly name of the app template
        if os.path.isfile(app_template_file):
            with open(app_template_file, 'r') as apptemplate_data_yaml:
                apptemplate_data_yaml_parsed = yaml.safe_load(apptemplate_data_yaml)
            apptemplate_dict = apptemplate_data_yaml_parsed.get(backend_category)
            if os.path.isfile(user_app_template_file):
                with open(user_app_template_file, 'r') as user_apptemplate_data_yaml:
                    user_apptemplate_data_yaml_parsed = yaml.safe_load(user_apptemplate_data_yaml)
                user_apptemplate_dict = user_apptemplate_data_yaml_parsed.get(backend_category)
            else:
                user_apptemplate_dict = {}
            if apptemplate_code in apptemplate_dict.keys():
                apptemplate_description = apptemplate_dict.get(apptemplate_code)
            else:
                if apptemplate_code in user_apptemplate_dict.keys():
                    apptemplate_description = user_apptemplate_dict.get(apptemplate_code)
        else:
            apptemplate_description = 'Application Template IO Error!'

    # Card Output
    cardheader(mydomainvisual, 'fas fa-cogs')
    print('                 <div class="card-body p-0">  <!-- Card Body Start -->')
    print('                     <div id="'+mydomainvisual+'-stack-status" class="row no-gutters row-1"> <!-- Row Start -->')

    # Htaccess quick show
    print('                         <div class="col-md-6 alert d-flex align-items-center text-center justify-content-center">Upstream: '+backend_category+'</div>')
    print('                         <div class="col-md-6">')
    print('                             <div class="row no-gutters">')
    if backend_category == 'PROXY':
        if backend_version == 'httpd':
            print('                        <div class="col-6 alert text-success"><i class="fas fa-check-circle"></i> .htaccess</div>')
    else:
        print('                            <div class="col-6 alert text-danger"><i class="fas fa-times-circle"></i> .htaccess</div>')
    
    print('                                 <div class="col-md-6 alert d-flex align-items-center text-center justify-content-center"> Template: '+apptemplate_description+'</div>')
    print('                             </div>')
    print('                         </div>')
    print('                     </div>')
    print('                 </div> <!-- Card Body End -->')

    print('                        <div class="card-body">  <!-- Card Body Start -->')
    print('                            <form class="form" action="app_settings.live.py" method="get">')
    print('                                <div class="input-group mb-1">')
    print('                                    <input hidden name="domain" value="'+mydomain+'">')
    print('                                        <button class="btn btn-outline-warning btn-block" type="submit">Configure</button>')
    print('                                </div>')
    print('                            </form>')

    print('                        </div> <!-- Card Body End -->')
    cardfooter('')


print_header('Home')
bcrumb('Home')

print('            <!-- cPanel Starter Row -->')
print('            <div class="row justify-content-lg-center">')
print('')
print('                <!-- Column Start -->')
print('                <div class="col-lg-6">')

# Auto Switch To Nginx
cardheader('Auto Configuration','fas fa-cogs')
print('                        <div class="card-body">  <!-- Card Body Start -->')

if settings_lock == 'enabled':
    print('                        <div class="text-center alert alert-info">Application Server settings are locked by the administrator</div>')
else:
    print('                            <form class="form mb-3" method="post" id="auto_switch_nginx" onsubmit="return false;">')
    print('                                <input hidden name="cpaneluser" value="'+cpaneluser+'">')
    print('                                <button id="auto-switch-nginx-btn" class="btn btn-outline-primary btn-block" type="submit">Auto Switch To Nginx</button>')
    print('                            </form>')

print('                        </div> <!-- Card Body End -->')
cardfooter('')

print_domain_stacks(main_domain, main_domain)

for domain_in_subdomains in sub_domains:
    if domain_in_subdomains not in addon_domains_dict.values():

        if domain_in_subdomains.startswith("*"):
            wildcard_domain = "_wildcard_."+domain_in_subdomains.replace('*.', '')
            print_domain_stacks(wildcard_domain, domain_in_subdomains)

        else:
            print_domain_stacks(domain_in_subdomains, domain_in_subdomains)

for the_addon_domain in addon_domains_dict.keys():
    print_domain_stacks(addon_domains_dict.get(the_addon_domain), the_addon_domain)

print('                        </div> <!-- Card Body End -->')
cardfooter('')

# Column End
print('                <!-- Column End -->')
print('                </div>')
print('')
print('            <!-- cPanel End Row -->')
print('            </div>')

print_footer()
