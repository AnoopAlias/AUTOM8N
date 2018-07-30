#!/bin/bash
if [[ $# -ne 3 ]];then
	exit 1
fi
if [[ $2 -eq 1 ]]; then
	if [ $3 = "IN_ATTRIB" ];then
		/usr/bin/grep "backend_category: PROXY" $1 > /dev/null
		if [ $? -ne 0 ];then
			CPANELUSER=$(stat -c "%U" $1)
			if [[ $CPANELUSER == root ]];then
				exit 0
			else
				ps aux | grep -v grep | grep "nginx -s reload" > /dev/null
				if [ $? -ne 0 ];then
					/usr/sbin/nginx -s reload > /dev/null 2>&1
					echo "$(date) Domain::Stats::Reload ${CPANELUSER}"
				fi
			fi
		fi
	else
		CPANELUSER=$(stat -c "%U" $1)
		/opt/nDeploy/scripts/generate_config.py $CPANELUSER
		/usr/sbin/nginx -s reload > /dev/null 2>&1
		echo "$(date) Domain::Data::Modify ${CPANELUSER}"
	fi
else
	exit 1
fi
