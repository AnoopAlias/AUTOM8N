#!/bin/bash
if [[ $# -ne 3 ]];then
	exit 1
fi
if [[ $2 -eq 0 ]]; then
	if(echo $1|egrep '_SSL$|_SSL.tmp.*');then
		CPANELUSER=$(echo $1|awk -F'/' '{print $5}')
		echo "$(date) Conf:Gen ${CPANELUSER}"
		/opt/nDeploy/scripts/generate_config.py $CPANELUSER
	fi
elif [[ $2 -eq 1 ]]; then
	CPANELUSER=$(stat -c "%U" $1)
	if [[ $CPANELUSER == root ]];then
		exit 0
	else
		if [ $3 = "IN_ATTRIB" ];then
			kill -USR1 $(cat /var/run/nginx.pid)
		else
			echo "$(date) Domain::Data::Modify ${CPANELUSER}"
			/opt/nDeploy/scripts/generate_config.py $CPANELUSER
		fi
	fi
elif [[ $2 -eq 2 ]]; then
	if(echo $1|egrep 'combined$');then
		CPANELDOMAIN=$(echo $1|awk -F'/' '{print $6}')
		CPANELUSER=$(grep $CPANELDOMAIN /etc/userdomains |awk '{print $2}')
		echo "$(date) Conf:Gen:TLS ${CPANELUSER}"
		/opt/nDeploy/scripts/generate_config.py $CPANELUSER
	fi
else
	exit 1
fi
