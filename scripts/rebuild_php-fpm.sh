#!/bin/sh

echo -n "Rebuild:"
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1); do
	/opt/nDeploy/scripts/apache_php_config_generator.py $CPANELUSER
	echo -n " $CPANELUSER";
done

echo -e "\nNow you can reload php-fpm"