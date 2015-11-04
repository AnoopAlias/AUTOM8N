#!/bin/bash
if [[ $# -ne 3 ]];then
	exit 1
fi

echo $1 |egrep ".*main$|.*cache$|.*\.cache$|.*\.lock$|.*\.cache\.tmp\.[0-9]*\.[0-9]*$" > /dev/null && exit 0

if [[ $2 -eq 0 ]]; then
	if [[ $3 == "IN_DELETE" ]];then
		THEDOMAIN=$(echo $1|awk -F'/' '{print $6}')
		echo "Conf:Del /etc/nginx/sites-enabled/${THEDOMAIN}.* /opt/nDeploy/domain-data/${THEDOMAIN}"
		rm -f /etc/nginx/sites-enabled/${THEDOMAIN}\.* /opt/nDeploy/domain-data/${THEDOMAIN}
	else
		CPANELUSER=$(echo $1|awk -F'/' '{print $5}')
		echo "Conf:Gen $CPANELUSER"
		/opt/nDeploy/scripts/generate_config.py $CPANELUSER
		/opt/nDeploy/scripts/apache_php_config_generator.py $CPANELUSER
	fi
elif [[ $2 -eq 1 ]]; then
	CPANELUSER=$(stat -c "%U" $1)
	if [[ $CPANELUSER == root ]];then
		exit 0
	else
		echo "Domain::Data::Modify ${CPANELUSER}"
		/opt/nDeploy/scripts/generate_config.py $CPANELUSER
	fi
elif [[ $2 -eq 2 ]];then
	CPANELUSER=$(stat -c "%U" $1)
	if [[ $CPANELUSER == root ]];then
		exit 0
	else
		echo "User::Data::Modify ${CPANELUSER}"
		 /opt/nDeploy/scripts/apache_php_config_generator.py $CPANELUSER
	fi
else
	exit 1
fi
