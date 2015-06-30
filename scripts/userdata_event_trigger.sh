#!/bin/bash

CPANELUSER=$(stat -c "%U" /opt/nDeploy/user-data/$1)

	(
	         flock -x -w 300 500
		 	/opt/nDeploy/scripts/apache_php_config_generator.py $CPANELUSER
	) 500>/opt/nDeploy/lock/$CPANELUSER.aplock		
	rm -f /opt/nDeploy/lock/$CPANELUSER.aplock
