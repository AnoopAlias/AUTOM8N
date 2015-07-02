#!/bin/bash

if [ $2 -eq 1 ] ; then
	CPANELUSER=$(stat -c "%U" /opt/nDeploy/user-data/$1)
else
	CPANELUSER=$(echo $1)
fi

if [[ $CPANELUSER == root || $CPANELUSER == .* ]];then
	exit 0
else
	(
	         flock -x -w 300 500
		 	/opt/nDeploy/scripts/apache_php_config_generator.py $CPANELUSER
	) 500>/opt/nDeploy/lock/$CPANELUSER.aplock		
	rm -f /opt/nDeploy/lock/$CPANELUSER.aplock
fi
