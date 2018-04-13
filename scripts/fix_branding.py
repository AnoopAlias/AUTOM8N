#!/usr/bin/env python

import json
import os
import yaml


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
        with open(installation_path+"/nDeploy_whm/xtendweb.conf", 'r') as whm_plugin_config:
            original_whm_conf = whm_plugin_config.read()
        original_whm_conf = original_whm_conf.replace('name=XtendWeb', 'name='+brand_name)
        original_whm_conf = original_whm_conf.replace('icon=xtendweb.png', 'icon='+brand_logo)
        with open(installation_path+"/nDeploy_whm/xtendweb.conf", 'w') as whm_plugin_config:
            whm_plugin_config.write(original_whm_conf)
