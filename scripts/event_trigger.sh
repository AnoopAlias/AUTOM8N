#!/bin/bash
if [[ $# -ne 3 ]];then
	exit 1
fi

echo $1 |grep -E "*\.cache$|*\.lock$|*\.cache\.tmp\.[0-9]*\.[0-9]*$" > /dev/null && exit 0

if [[ $2 -eq 0 ]]; then
	if [[ $3 == "IN_DELETE" ]];then
		THEDOMAIN=$(echo $1|awk -F'/' '{print $6}')
		rm -f /etc/nginx/sites-enabled/$THEDOMAIN\.* /opt/nDeploy/domain-data/$THEDOMAIN
	else
		CPANELUSER=$(echo $1|awk -F'/' '{print $5}')
		(
	         flock -x -w 300 500
			 sleep 20
		 	/opt/nDeploy/scripts/generate_config.py $CPANELUSER
			/opt/nDeploy/scripts/apache_php_config_generator.py $CPANELUSER
		) 500>/opt/nDeploy/lock/$CPANELUSER_cpanel.lock
		rm -f /opt/nDeploy/lock/$CPANELUSER_cpanel.lock
	fi
elif [[ $2 -eq 1 ]]; then
	CPANELUSER=$(stat -c "%U" $1)
	if [[ $CPANELUSER == root ]];then
		exit 0
	else
		(
	         flock -x -w 300 500
			 sleep 20
		 	/opt/nDeploy/scripts/generate_config.py $CPANELUSER
		) 500>/opt/nDeploy/lock/$CPANELUSER_nginx.lock
		rm -f /opt/nDeploy/lock/$CPANELUSER_nginx.lock
	fi
elif [[ $2 -eq 2 ]];then
	CPANELUSER=$(stat -c "%U" $1)
	if [[ $CPANELUSER == root ]];then
		exit 0
	else
		(
	         flock -x -w 300 500
			 sleep 20
		 	/opt/nDeploy/scripts/apache_php_config_generator.py $CPANELUSER
		) 500>/opt/nDeploy/lock/$CPANELUSER_apache.lock
		rm -f /opt/nDeploy/lock/$CPANELUSER_apache.lock
	fi
else
	exit 1
fi
