#!/usr/bin/python

import cgi
import cgitb
import os
import yaml
from commoninclude import return_label, return_prepend, bcrumb, print_header, print_footer, print_modals, print_loader, cardheader, cardfooter

__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Development"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
ndeploy_control_file = installation_path+"/conf/ndeploy_control.yaml"
branding_file = installation_path+"/conf/branding.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print_header('nDeploy Control Center')
bcrumb('nDeploy Control Center','fab fa-bootstrap')

#Theming Support
print('            <!-- WHM Starter Row -->')
print('            <div class="row justify-content-lg-center flex-nowrap">')

if os.path.isfile(ndeploy_control_file):
    with open(ndeploy_control_file, 'r') as ndeploy_control_data_file:
        yaml_parsed_ndeploy_control_settings = yaml.safe_load(ndeploy_control_data_file)
    heading_background_color = yaml_parsed_ndeploy_control_settings.get("heading_background_color","#FFFFFF") #done
    heading_foreground_color = yaml_parsed_ndeploy_control_settings.get("heading_foreground_color","#3D4366") #done
    body_background_color = yaml_parsed_ndeploy_control_settings.get("body_background_color","#F1F1F8") #done
    card_color = yaml_parsed_ndeploy_control_settings.get("card_color","light") #done
    text_color = yaml_parsed_ndeploy_control_settings.get("text_color","dark") #done
    breadcrumb_active_color = yaml_parsed_ndeploy_control_settings.get("breadcrumb_active_color","#121212") #done
    heading_height = yaml_parsed_ndeploy_control_settings.get("heading_height","50") #done
    header_button_color = yaml_parsed_ndeploy_control_settings.get("header_button_color","primary") #done
    icon_height = yaml_parsed_ndeploy_control_settings.get("icon_height","48") #done
    icon_width = yaml_parsed_ndeploy_control_settings.get("icon_width","48") #done
    logo_not_icon = yaml_parsed_ndeploy_control_settings.get("logo_not_icon","disabled") #done
    logo_height = yaml_parsed_ndeploy_control_settings.get("logo_height","29") #done
    logo_width = yaml_parsed_ndeploy_control_settings.get("logo_width","242") #done
    logo_url = yaml_parsed_ndeploy_control_settings.get("logo_url","https://autom8n.com/assets/img/logo-dark.png") #done
    app_title = yaml_parsed_ndeploy_control_settings.get("app_title","AUTOM8N") #done
    app_email = yaml_parsed_ndeploy_control_settings.get("app_email","ops@gnusys.net") #done
else:
    heading_background_color = "#FFFFFF"
    heading_foreground_color = "#3D4366"
    body_background_color = "#F1F1F8"
    card_color = "light"
    text_color = "dark"
    breadcrumb_active_color = "#121212"
    heading_height = "50"
    header_button_color = "primary"
    icon_height = "48"
    icon_width = "48"
    logo_not_icon = "disabled"
    logo_height = "29"
    logo_width = "242"
    logo_url = "https://autom8n.com/assets/img/logo-dark.png"
    app_title = "AUTOM8N"
    app_email = "ops@gnusys.net"


#Branding Support
if os.path.isfile(branding_file):
    with open(branding_file, 'r') as brand_data_file:
        yaml_parsed_brand = yaml.safe_load(brand_data_file)
    brand_logo = yaml_parsed_brand.get("brand_logo", "xtendweb.png")
    brand = yaml_parsed_brand.get("brand", "AUTOM8N")
    brand_group = yaml_parsed_brand.get("brand_group", "NGINX AUTOMATION")
    brand_footer = yaml_parsed_brand.get("brand_footer", '<a target="_blank" href="https://autom8n.com/">A U T O M 8 N</a>') #Depreciated
    brand_anchor = yaml_parsed_brand.get("brand_anchor", "A U T O M 8 N")
    brand_link = yaml_parsed_brand.get("brand_link", "https://autom8n.com/")
else:
    brand_logo = "xtendweb.png"
    brand = "AUTOM8N"
    brand_group = "NGINX AUTOMATION"
    brand_footer = '<a target="_blank" href="https://autom8n.com/">A U T O M 8 N</a>' #Depreciated
    brand_anchor = "A U T O M 8 N"
    brand_link = "https://autom8n.com/"


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
brand_logo_hint = " Enter the filename of the brand logo used for this system in the suggested directories. "
brand_hint = " Enter the text you want to represent this application as for whitelabeling purposes. This shows up in both WHM and cPanel."
brand_group_hint = " This is a brand_group hint. "
brand_footer_hint = " This is a brand_footer hint. "
brand_anchor_hint = " This is a brand_anchor hint. "
brand_link_hint = " This is a brand_link hint. "


print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->') #Row Start
print('                                <form class="form w-100" id="ndeploy_control_branding" method="post" onsubmit="return false;">')

print('                                <label for="brand">Enter the brand name you want to represent for cPanel\'s and WHM\'s icon label, as well as the header if not using the full <kbd>logo_not_icon</kbd> method.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="brand_desc">')
print('                                            '+return_prepend("brand", brand_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="brand" value="'+brand+'" id="brand" aria-describedby="brand_desc">')
print('                                </div>')

print('                                <label for="brand_logo">Place a 48 x 48 pixel icon of your brand in <kbd>'+installation_path+'/nDeploy_whm</kbd> and <kbd>'+installation_path+'/nDeploy_cp</kbd> folders to personalize the panel\'s icon in various areas.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="brand_logo_desc">')
print('                                            '+return_prepend("brand_logo", brand_logo_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="brand_logo" value="'+brand_logo+'" id="brand_logo" aria-describedby="brand_logo_desc">')
print('                                </div>')


print('                                <label for="brand_group">Enter the section you want this application to be placed in within each user\'s cPanel.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="brand_group_desc">')
print('                                            '+return_prepend("brand_group", brand_group_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="brand_group" value="'+brand_group+'" id="brand_group" aria-describedby="brand_group_desc">')
print('                                </div>')

print('                                <label for="brand_anchor">Enter your brand\'s anchor text that will be used on the footer of the application.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="brand_anchor_desc">')
print('                                            '+return_prepend("brand_anchor", brand_anchor_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="brand_anchor" value="'+brand_anchor+'" id="brand_anchor" aria-describedby="brand_anchor_desc">')
print('                                </div>')

print('                                <label for="brand_link">Enter your brand\'s website link that the above anchor text will link to via the footer.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="brand_link_desc">')
print('                                            '+return_prepend("brand_link", brand_link_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="brand_link" value="'+brand_link+'" id="brand_link" aria-describedby="brand_link_desc">')
print('                                </div>')
print('                                <button class="mb-2 btn btn-outline-primary btn-block" type="submit">Save Branding Options</button>')
print('                                </form>')

print('                                <form class="form w-100" id="ndeploy_control_rebuild_brand" method="post" onsubmit="return false;">')
print('                                <input hidden class="form-control" name="rebuild_brand" value="enabled">')
print('                                <button class="btn btn-outline-primary btn-block" type="submit">Rebuild Brand</button>')
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
breadcrumb_active_color_hint = " This can be a HEX code, a RGB color code, or just a web browser supported color format like grey, black, white, etc. "

print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->') #Row Start
print('                                <form class="form w-100" id="ndeploy_control_config" method="post" onsubmit="return false;">')

print('                                <label for="breadcrumb_active_color">Enter the desired color code for the currently ACTIVE page in this application\'s breadcrumb section which is located beneath the header.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="breadcrumb_active_color_desc">')
print('                                            '+return_prepend("Breadcrumb Active Page Color", breadcrumb_active_color_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="breadcrumb_active_color" value="'+breadcrumb_active_color+'" id="breadcrumb_active_color" aria-describedby="breadcrumb_active_color_desc">')
print('                                </div>')
print('                                    <button class="btn btn-outline-primary btn-block" type="submit">Save BreadCrumb Settings</button>')

print('                            </div> <!-- Row End -->') #End Row
print('                        </div> <!-- Card Body End -->') #Card Body End

cardfooter('')

print('                </div> <!-- End Breadcrumbs Tab -->')

#Heading Tab
print('')
print('                <!-- Heading Tab -->')
print('                <div class="tab-pane fade" id="v-pills-heading" role="tabpanel" aria-labelledby="v-pills-heading-tab">')

cardheader('Heading Settings','fas fa-heading')
heading_background_color_hint = " This can be a HEX code, a RGB color code, or just a web browser supported color format like grey, black, white, etc. "
heading_foreground_color_hint = " This can be a HEX code, a RGB color code, or just a web browser supported color format like grey, black, white, etc. "
heading_height_hint = " This can be in pixels, REM, EM, VH, VW or any other supported size supported by the browser. "
header_button_color_hint = " This is a header_button_color hint. "
icon_height_hint = " This is a icon_height hint. "
icon_width_hint = " This is a icon_width hint. "
logo_not_icon_hint = " This is a logo_not_icon hint. "
logo_height_hint = " This is a logo_height hint. "
logo_width_hint = " This is a logo_width hint. "
logo_url_hint = " This is a logo_url hint. "


print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->') #Row Start

print('                                <label for="heading_background_color">Enter the desired background color for the header.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="heading_background_color_desc">')
print('                                            '+return_prepend("Header Background Color", heading_background_color_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="heading_background_color" value="'+heading_background_color+'" id="heading_background_color" aria-describedby="heading_background_color_desc">')
print('                                </div>')

print('                                <label for="heading_foreground_color">Enter the desired foreground color for the header.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="heading_foreground_color_desc">')
print('                                            '+return_prepend("Header Foreground Color", heading_foreground_color_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="heading_foreground_color" value="'+heading_foreground_color+'" id="heading_foreground_color" aria-describedby="heading_foreground_color_desc">')
print('                                </div>')

print('                                <label for="heading_height">Enter the desired header height. Use this to present your logo more cleanly.</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="heading_height_desc">')
print('                                            '+return_prepend("Header Height", heading_height_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="heading_height" value="'+heading_height+'" id="heading_height" aria-describedby="heading_height_desc">')
print('                                </div>')

print('                                <label for="header_button_color">header_button_color</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <label class="input-group-text">'+return_prepend("Header Button Color", header_button_color_hint)+'</label>')
print('                                    </div>')
print('                                    <select name="header_button_color" class="custom-select">')

bootstrap_colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark', 'muted', 'white']
for color in bootstrap_colors:
    if header_button_color != color:
        print('                                        <option value="'+color+'">'+color+'</option>')
    else:
        print('                                        <option selected value="'+color+'">'+color+'</option>')
print('                                    </select>')
print('                                </div>')

print('                                <label for="icon_height">icon_height</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="icon_height_desc">')
print('                                            '+return_prepend("icon_height", icon_height_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="icon_height" value="'+icon_height+'" id="icon_height" aria-describedby="icon_height_desc">')
print('                                </div>')

print('                                <label for="icon_width">icon_width</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="icon_width_desc">')
print('                                            '+return_prepend("icon_width", icon_width_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="icon_width" value="'+icon_width+'" id="icon_width" aria-describedby="icon_width_desc">')
print('                                </div>')

# logo_not_icon 
if logo_not_icon == 'enabled':
    print('                                    '+return_label("logo_not_icon", logo_not_icon_hint))
    print('                                    <div class="col-md-6">')
    print('                                        <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
    print('                                            <label class="btn btn-light active">')
    print('                                                <input type="radio" name="logo_not_icon" value="enabled" id="BuFilesOn" autocomplete="off" checked> Enabled')
    print('                                            </label>')
    print('                                            <label class="btn btn-light">')
    print('                                                <input type="radio" name="logo_not_icon" value="disabled" id="BuFilesOff" autocomplete="off"> Disabled')
    print('                                            </label>')
    print('                                        </div>')
    print('                                    </div>')
else:
    print('                                    '+return_label("logo_not_icon", logo_not_icon_hint))
    print('                                    <div class="col-md-6">')
    print('                                        <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
    print('                                            <label class="btn btn-light">')
    print('                                                <input type="radio" name="logo_not_icon" value="enabled" id="BuFilesOn" autocomplete="off"> Enabled')
    print('                                            </label>')
    print('                                            <label class="btn btn-light active">')
    print('                                                <input type="radio" name="logo_not_icon" value="disabled" id="BuFilesOff" autocomplete="off" checked> Disabled')
    print('                                            </label>')
    print('                                        </div>')
    print('                                    </div>')

print('                                <label for="logo_height">logo_height</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="logo_height_desc">')
print('                                            '+return_prepend("logo_height", logo_height_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="logo_height" value="'+logo_height+'" id="logo_height" aria-describedby="logo_height_desc">')
print('                                </div>')

print('                                <label for="logo_width">logo_width</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="logo_width_desc">')
print('                                            '+return_prepend("logo_width", logo_width_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="logo_width" value="'+logo_width+'" id="logo_width" aria-describedby="logo_width_desc">')
print('                                </div>')

print('                                <label for="logo_url">logo_url</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="logo_url_desc">')
print('                                            '+return_prepend("logo_url", logo_url_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="logo_url" value="'+logo_url+'" id="logo_url" aria-describedby="logo_url_desc">')
print('                                </div>')


print('                                <button class="btn btn-outline-primary btn-block" type="submit">Save Heading Settings</button>')

print('                            </div> <!-- Row End -->') #End Row
print('                        </div> <!-- Card Body End -->') #Card Body End

cardfooter('')

print('                </div> <!-- End Heading Tab -->')

#Application Tab
print('')
print('                <!-- Application Tab -->')
print('                <div class="tab-pane fade" id="v-pills-application" role="tabpanel" aria-labelledby="v-pills-application-tab">')
cardheader('Application Settings','fas fa-tools')
app_title_hint = " This is a app_title hint. "
app_email_hint = " This is a app_email hint. "
body_background_color_hint = " This is a body_background_color hint. "
card_color_hint = " This is a card_color hint. "
text_color_hint = " This is a text_color hint. "

print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
print('                            <div class="row ml-auto mr-auto"> <!-- Row Start -->') #Row Start

print('                                <label for="app_title">app_title</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="app_title_desc">')
print('                                            '+return_prepend("app_title", app_title_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="app_title" value="'+app_title+'" id="app_title" aria-describedby="app_title_desc">')
print('                                </div>')

print('                                <label for="app_email">app_email</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="app_email_desc">')
print('                                            '+return_prepend("app_email", app_email_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="app_email" value="'+app_email+'" id="app_email" aria-describedby="app_email_desc">')
print('                                </div>')

print('                                <label for="body_background_color">body_background_color</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text" id="body_background_color_desc">')
print('                                            '+return_prepend("body_background_color", body_background_color_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <input type="text" class="form-control" name="body_background_color" value="'+body_background_color+'" id="body_background_color" aria-describedby="body_background_color_desc">')
print('                                </div>')

print('                                <label for="card_color">card_color</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <label class="input-group-text">'+return_prepend("card_color", card_color_hint)+'</label>')
print('                                    </div>')
print('                                    <select name="card_color" class="custom-select">')

bootstrap_colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark', 'muted', 'white']
for color in bootstrap_colors:
    if card_color != color:
        print('                                        <option value="'+color+'">'+color+'</option>')
    else:
        print('                                        <option selected value="'+color+'">'+color+'</option>')
print('                                    </select>')
print('                                </div>')

print('                                <label for="text_color">text_color</label>')
print('                                <div class="input-group mb-4">')
print('                                    <div class="input-group-prepend">')
print('                                        <label class="input-group-text">'+return_prepend("text_color", text_color_hint)+'</label>')
print('                                    </div>')
print('                                    <select name="text_color" class="custom-select">')

bootstrap_colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark', 'muted', 'white']
for color in bootstrap_colors:
    if text_color != color:
        print('                                        <option value="'+color+'">'+color+'</option>')
    else:
        print('                                        <option selected value="'+color+'">'+color+'</option>')
print('                                    </select>')
print('                                </div>')


print('                                <button class="btn btn-outline-primary btn-block" type="submit">Save Application Settings</button>')

print('                                </form>')
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

print_footer()

print('        </div> <!-- Main Container End -->')
print('')

print_modals()
print_loader()

print('    <!-- Body End -->')
print('    </body>')
print('</html>')