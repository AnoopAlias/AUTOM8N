#!/bin/bash

echo "called $$ $0 $*" >> /opt/nDeploy/hook.log

CPANELUSER=$(stat -c "%U" $1)

if [[ $CPANELUSER == root || $CPANELUSER == .* ]];then
	exit 0
else
	(
		flock -x -w 300 500
		echo "from $$ Run apache_php_config_generator init_backends part"
		/opt/nDeploy/scripts/apache_php_config_generator.py $CPANELUSER
		/opt/nDeploy/scripts/init_backends.pl --action=reload
	) 500>/opt/nDeploy/lock/$CPANELUSER.aplock
	rm -f /opt/nDeploy/lock/$CPANELUSER.aplock
fi
