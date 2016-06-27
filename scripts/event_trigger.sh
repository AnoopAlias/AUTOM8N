#!/bin/bash
if [[ $# -ne 3 ]];then
	exit 1
fi

echo $1 |egrep ".*main$|.*cache$|.*\.cache$|.*\.lock$|.*\.cache\.tmp\.[0-9]*\.[0-9]*$|/opt/nDeploy/domain-data/\..*|.*\.cache\.tmp\.[0-9]*" > /dev/null && exit 0

if [[ $2 -eq 0 ]]; then
	if [[ $3 == "IN_DELETE" ]];then
		THEDOMAIN=$(echo "${1}"|awk -F'/' '{print $6}'|sed "s/\*/_wildcard_/")
		echo "Conf:Del /etc/nginx/sites-enabled/${THEDOMAIN} /opt/nDeploy/domain-data/${THEDOMAIN}"
		rm -f /etc/nginx/sites-enabled/${THEDOMAIN}{.conf,.include,.nxapi.wl,_SSL.conf,_SSL.include} /opt/nDeploy/domain-data/${THEDOMAIN}
		if [ -f /opt/nDeploy/conf/ndeploy_cluster_slaves ];then
			for slave in $(cat /opt/nDeploy/conf/ndeploy_cluster_slaves)
			do
				rm -f /etc/nginx/${slave}/${THEDOMAIN}{.conf,.include,.nxapi.wl,_SSL.conf,_SSL.include}
			done
		fi
		/usr/sbin/nginx -s reload
	else
		CPANELUSER=$(echo $1|awk -F'/' '{print $5}')
		echo "Conf:Gen Queued ${CPANELUSER}"
		echo ${CPANELUSER} >> /opt/nDeploy/lock/config_generation_queue
	fi
elif [[ $2 -eq 1 ]]; then
	CPANELUSER=$(stat -c "%U" $1)
	if [[ $CPANELUSER == root ]];then
		exit 0
	else
		if [ $3 = "IN_ATTRIB" ];then
			/usr/sbin/nginx -s reload
		else
			echo "Domain::Data::Modify ${CPANELUSER}"
			/opt/nDeploy/scripts/generate_config.py $CPANELUSER
		fi
	fi
else
	exit 1
fi
