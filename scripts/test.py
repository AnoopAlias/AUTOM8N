#!/usr/bin/env python

import yaml
my_file = "/opt/xstack/domain-data/gnusys.net"

data_dict = {"user" : "gnusys" , "backend_category"  : "PROXY" , "backend_version" : "none" , "profile" : 1000 , "customconf" : 0 , "backend_path": "none" }
with open(my_file ,'w') as yaml_file:
	yaml_file.write(yaml.dump(data_dict , default_flow_style=False))
yaml_file.close()
