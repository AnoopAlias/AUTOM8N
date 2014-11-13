#!/usr/bin/env python

import yaml
import argparse
import subprocess

installation_path = "/opt/nDeploy" #Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
php_fpm_config = installation_path+"/conf/php-fpm.conf"

#Function defs
def control_php_fpm(trigger):
	if backend_data_yaml_parsed.has_key("PHP"):
		php_backends_dict = backend_data_yaml_parsed["PHP"]
		if trigger == "start":
			subprocess.call("sysctl -q -w net.core.somaxconn=4096",shell=True)
			for path in php_backends_dict.values():
				php_fpm_bin = path+"/sbin/php-fpm"
				subprocess.call(php_fpm_bin+" --fpm-config "+php_fpm_config,shell=True)
		elif trigger == "stop":
			for path in php_backends_dict.values():
				php_fpm_pid = path+"/var/run/php-fpm.pid"
				subprocess.call("kill -9 $(cat "+php_fpm_pid+")", shell=True)
		else:
			return


backend_data_yaml = open(backend_config_file,'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()

parser = argparse.ArgumentParser(description = "Start/Stop various nDeploy backends")
parser.add_argument("control_command")
args = parser.parse_args()
trigger = args.control_command

control_php_fpm(trigger)
		

	



