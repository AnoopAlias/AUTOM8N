#!/bin/sh

echo -n "Rebuild:"
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1); do
	/opt/nDeploy/scripts/generate_config.py $CPANELUSER
	echo -n " $CPANELUSER";
done

service nginx configtest && service nginx reload
