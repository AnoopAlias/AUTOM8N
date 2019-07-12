#!/usr/bin/python

#import cgi
import cgitb
#import subprocess
import os
import yaml
#import platform
#import psutil
#import signal
#import jinja2
#import codecs
#import sys
from commoninclude import print_success, return_prepend, bcrumb, print_header, print_modals, print_loader, cardheader, cardfooter

__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Development"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
bs_themer_file = installation_path+"/conf/bs_themer.yaml"
branding_file = installation_path+"/conf/branding.yaml"

cgitb.enable()

#form = cgi.FieldStorage()

print_header('nDeploy Control Center')
bcrumb('nDeploy Control Center','fab fa-bootstrap')

#Theming Support
print('            <!-- WHM Starter Row -->')
print('            <div class="row justify-content-lg-center flex-nowrap">')

if os.path.isfile(bs_themer_file):
    with open(bs_themer_file, 'r') as theme_data_file:
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
    app_email = yaml_parsed_theme.get("app_email","ops@gnusys.net")

#Branding Support
if os.path.isfile(branding_file):
    with open(branding_file, 'r') as brand_data_file:
        yaml_parsed_brand = yaml.safe_load(brand_data_file)
    brand_logo = yaml_parsed_brand.get("brand_logo", "xtendweb.png")
    brand_name = yaml_parsed_brand.get("brand", "AUTOM8N")
    brand_group = yaml_parsed_brand.get("brand_group", "NGINX AUTOMATION")
    brand_footer = yaml_parsed_brand.get("brand_footer", '<a target="_blank" href="https://autom8n.com/">A U T O M 8 N</a>') #Depreciated
    brand_anchor = yaml_parsed_brand.get("brand_anchor", "A U T O M 8 N")
    brand_link = yaml_parsed_brand.get("brand_link", "https://autom8n.com/")

print('')
print('                <!-- Secondary Navigation -->')
print('                <div class="col-md-3 nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">')
print('                    <a class="nav-link active" id="v-pills-home-tab" data-toggle="pill" href="#v-pills-home" role="tab" aria-controls="v-pills-home" aria-selected="true">Home</a>')
print('                    <a class="nav-link" id="v-pills-branding-tab" data-toggle="pill" href="#v-pills-branding" role="tab" aria-controls="v-pills-branding" aria-selected="false">Branding</a>')
print('                    <a class="nav-link" id="v-pills-breadcrumb-tab" data-toggle="pill" href="#v-pills-breadcrumb" role="tab" aria-controls="v-pills-breadcrumb" aria-selected="false">Breadcrumb</a>')
print('                    <a class="nav-link" id="v-pills-heading-tab" data-toggle="pill" href="#v-pills-heading" role="tab" aria-controls="v-pills-heading" aria-selected="false">Heading</a>')
print('                    <a class="nav-link" id="v-pills-application-tab" data-toggle="pill" href="#v-pills-application" role="tab" aria-controls="v-pills-application" aria-selected="false">Application</a>')
print('                </div>')
print('')
print('                <div class="tab-content col-md-9" id="v-pills-tabContent">')

#Home Tab
print('')
print('                <!-- Home Tab -->')
print('                <div class="tab-pane fade show active" id="v-pills-home" role="tabpanel" aria-labelledby="v-pills-home-tab">')

cardheader('Welcome to nDeploy Control','fab fa-bootstrap')

print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->') #Row Start
print('                                <p>Welcome to the nDeploy Control Center.&nbsp;&nbsp;Here you will have control over various theme and configuration aspects of nDeploy whether it is branding or theme configuration settings to what features you want available to the users.</p>')
print('                            </div> <!-- Row End -->') #End Row
print('                        </div> <!-- Card Body End -->') #Card Body End

cardfooter('')

print('                </div> <!-- End Home Tab -->')

#Branding Tab
print('')
print('                <!-- Branding Tab -->')
print('                <div class="tab-pane fade" id="v-pills-branding" role="tabpanel" aria-labelledby="v-pills-branding-tab">')

cardheader('Branding Settings','fas fa-infinity')
brand_logo_hint = " This is a brand_logo hint. "
brand_name_hint = " This is a brand_name hint. "
brand_group_hint = " This is a brand_group hint. "
brand_footer_hint = " This is a brand_footer hint. "
brand_anchor_hint = " This is a brand_anchor hint. "
brand_link_hint = " This is a brand_link hint. "


print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->') #Row Start

print('                                <form class="form w-100" action="save_ndeploy_control_settings.cgi" method="get">')

print('                                    <label for="brand_logo">brand_logo</label>')
print('                                    <div class="input-group">')
print('                                        <div class="input-group-prepend">')
print('                                            <span class="input-group-text" id="brand_logo_desc">')
print('                                                '+return_prepend("brand_logo", brand_logo_hint))
print('                                            </span>')
print('                                        </div>')
print('                                        <input type="text" class="form-control" value="'+brand_logo+'" id="brand_logo" aria-describedby="brand_logo_desc">')
print('                                    </div>')

print('                                    <label for="brand_name">brand_name</label>')
print('                                    <div class="input-group">')
print('                                        <div class="input-group-prepend">')
print('                                            <span class="input-group-text" id="brand_name_desc">')
print('                                                '+return_prepend("brand_name", brand_name_hint))
print('                                            </span>')
print('                                        </div>')
print('                                        <input type="text" class="form-control" value="'+brand_name+'" id="brand_name" aria-describedby="brand_name_desc">')
print('                                    </div>')

print('                                    <label for="brand_group">brand_group</label>')
print('                                    <div class="input-group">')
print('                                        <div class="input-group-prepend">')
print('                                            <span class="input-group-text" id="brand_group_desc">')
print('                                                '+return_prepend("brand_group", brand_group_hint))
print('                                            </span>')
print('                                        </div>')
print('                                        <input type="text" class="form-control" value="'+brand_group+'" id="brand_group" aria-describedby="brand_group_desc">')
print('                                    </div>')

print('                                    <label for="brand_anchor">brand_anchor</label>')
print('                                    <div class="input-group">')
print('                                        <div class="input-group-prepend">')
print('                                            <span class="input-group-text" id="brand_anchor_desc">')
print('                                                '+return_prepend("brand_anchor", brand_anchor_hint))
print('                                            </span>')
print('                                        </div>')
print('                                        <input type="text" class="form-control" value="'+brand_anchor+'" id="brand_anchor" aria-describedby="brand_anchor_desc">')
print('                                    </div>')

print('                                    <label for="brand_link">brand_link</label>')
print('                                    <div class="input-group">')
print('                                        <div class="input-group-prepend">')
print('                                            <span class="input-group-text" id="brand_link_desc">')
print('                                                '+return_prepend("brand_link", brand_link_hint))
print('                                            </span>')
print('                                        </div>')
print('                                        <input type="text" class="form-control" value="'+brand_link+'" id="brand_link" aria-describedby="brand_link_desc">')
print('                                    </div>')

print('                                    <button class="btn btn-outline-primary btn-block" type="submit">Save Branding Options</button>')

print('                                </form>')

print('                            </div> <!-- Row End -->') #End Row
print('                        </div> <!-- Card Body End -->') #Card Body End

cardfooter('')

print('                </div> <!-- End Branding Tab -->')

#Breadcrumb Tab
print('')
print('                <!-- Breadcrumb Tab -->')
print('                <div class="tab-pane fade" id="v-pills-breadcrumb" role="tabpanel" aria-labelledby="v-pills-breadcrumb-tab">')

cardheader('Breadcrumb Settings','fas fa-bread-slice')

print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->') #Row Start
print('                                <p>Configure your breadcrumb settings here.</p>')
print('                            </div> <!-- Row End -->') #End Row
print('                        </div> <!-- Card Body End -->') #Card Body End

cardfooter('')

print('                </div> <!-- End Breadcrumbs Tab -->')

#Heading Tab
print('')
print('                <!-- Heading Tab -->')
print('                <div class="tab-pane fade" id="v-pills-heading" role="tabpanel" aria-labelledby="v-pills-heading-tab">')

cardheader('Heading Settings','fas fa-heading')

print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->') #Row Start
print('                                <p>Configure your heading settings here.</p>')
print('                            </div> <!-- Row End -->') #End Row
print('                        </div> <!-- Card Body End -->') #Card Body End

cardfooter('')

print('                </div> <!-- End Heading Tab -->')

#Application Tab
print('')
print('                <!-- Application Tab -->')
print('                <div class="tab-pane fade" id="v-pills-application" role="tabpanel" aria-labelledby="v-pills-application-tab">')
cardheader('Application Settings','fas fa-tools')

print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->') #Row Start
print('                                <p>Configure your application settings here.</p>')
print('                            </div> <!-- Row End -->') #End Row
print('                        </div> <!-- Card Body End -->') #Card Body End

cardfooter('')

print('                </div> <!-- End Application Tab -->')

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