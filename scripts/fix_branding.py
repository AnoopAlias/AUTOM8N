#!/usr/bin/env python3

import json
import os
import yaml
import fileinput
import sys


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


if __name__ == "__main__":
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_logo = yaml_parsed_brand.get("brand_logo", "xtendweb.png")
        brand_name = yaml_parsed_brand.get("brand", "XtendWeb")
        brand_group = yaml_parsed_brand.get("brand_group", "NGINX CLUSTER CONTROL")
        # Set brand name in cpanel
        with open(installation_path+"/nDeploy_cp/install.json", 'r') as cp_plugin_config:
            cp_plugin_conf_data = json.load(cp_plugin_config)
        cp_group_conf = cp_plugin_conf_data[0]
        cp_item_conf = cp_plugin_conf_data[1]
        cp_group_conf['name'] = brand_group
        cp_item_conf['name'] = brand_name
        cp_item_conf['icon'] = brand_logo
        with open(installation_path+"/nDeploy_cp/install.json", 'w') as cp_plugin_config_new:
            json.dump(cp_plugin_conf_data, cp_plugin_config_new)
        # Set brand name in WHM
        if not os.path.islink("/usr/local/cpanel/whostmgr/docroot/addon_plugins/"+brand_logo):
            os.symlink(installation_path+"/nDeploy_whm/"+brand_logo, "/usr/local/cpanel/whostmgr/docroot/addon_plugins/"+brand_logo)
        for line in fileinput.input(installation_path+"/nDeploy_whm/xtendweb.conf", inplace=True):
            if line.strip().startswith('displayname='):
                line = 'displayname='+brand_name+'\n'
            elif line.strip().startswith('icon='):
                line = 'icon='+brand_logo+'\n'
            sys.stdout.write(line)
