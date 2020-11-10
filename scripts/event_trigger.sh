#!/usr/bin/env bash
if [[ $# -ne 3 ]];then
	exit 1
fi
if [[ $2 -eq 1 ]]; then
	if [ $3 = "IN_ATTRIB" ];then
		grep "backend_category: PROXY" $1 > /dev/null
		if [ $? -ne 0 ];then
			CPANELUSER=$(stat -c "%U" $1)
			if [[ ${CPANELUSER} == root ]];then
				exit 0
			else
				kill -s SIGUSR1 $(cat /var/run/nginx.pid)
				echo "$(date) Domain::Stats::Reload ${CPANELUSER}"
			fi
		fi
	else
		CPANELUSER=$(stat -c "%U" $1)
		/opt/nDeploy/scripts/generate_config.py ${CPANELUSER}
		kill -s SIGHUP $(cat /var/run/nginx.pid)
		echo "$(date) Domain::Data::Modify ${CPANELUSER}"
	fi
else
	exit 1
fi
