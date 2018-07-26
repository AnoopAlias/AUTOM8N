#!/bin/bash
if [[ $# -ne 3 ]];then
	exit 1
fi
if [[ $2 -eq 1 ]]; then
	CPANELUSER=$(stat -c "%U" $1)
	if [[ $CPANELUSER == root ]];then
		exit 0
	else
		if [ $3 = "IN_ATTRIB" ];then
			ps aux | grep "nginx -s reload"|grep -v grep
			if [ $? -ne 0 ];then
				/usr/sbin/nginx -s reload > /dev/null 2>&1
			fi
		else
			echo "$(date) Domain::Data::Modify ${CPANELUSER}"
			/opt/nDeploy/scripts/generate_config.py $CPANELUSER
			/usr/sbin/nginx -s reload > /dev/null 2>&1
		fi
	fi
else
	exit 1
fi
