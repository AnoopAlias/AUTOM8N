#!/bin/bash

echo $1 |grep -E "\.cache|\.lock|^.*cache$" && exit 0

if [ $2 -eq 1 ] ; then
	CPANELUSER=$(stat -c "%U" $1)
else
	if [ $3 == "IN_DELETE" ]; then
		THEDOMAIN=$(echo $1|awk -F'/' '{print $6}')
		rm -f /etc/nginx/sites-enabled/$THEDOMAIN\.* /opt/nDeploy/domain-data/$THEDOMAIN
	fi
	CPANELUSER=$(echo $1|awk -F'/' '{print $5}')
fi

if [[ $CPANELUSER == root || $CPANELUSER == *.lock || $CPANELUSER == .* ]];then
	exit 0
else
	(
	         flock -x -w 300 500
		 	/opt/nDeploy/scripts/generate_config.py $CPANELUSER
			/opt/nDeploy/scripts/apache_php_config_generator.py $CPANELUSER
	) 500>/opt/nDeploy/lock/$CPANELUSER.lock		
	rm -f /opt/nDeploy/lock/$CPANELUSER.lock
fi
