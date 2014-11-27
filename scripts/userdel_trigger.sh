#!/bin/bash

CPANELUSER=$(echo $1)
if [[ $CPANELUSER == *.lock || $CPANELUSER == .* ]];then
        exit 0
else
	for file in $(find /opt/nDeploy/domain-data)
	do
    		grep -w "user: $CPANELUSER" $file && rm -f $file && rm -f /opt/nDeploy-sites-enabled/$(basename $file).conf ; rm -f /opt/nDeploy-sites-enabled/$(basename $file).include && rm -rf /var/resin/hosts/$(basename $file)
	done 

	/usr/sbin/nginx -s reload
	/opt/nDeploy/scripts/delete_backends.py $CPANELUSER
fi
