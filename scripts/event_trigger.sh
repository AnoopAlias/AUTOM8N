#!/bin/bash

# ignore files with .cache, .lock
echo $1 |grep -E "\.cache|\.lock|^.*cache$" && exit 0

# ignore event when directory is removed
echo $3 |grep -E "IN_DELETE\|IN_ISDIR" && exit 0

echo "called $$ $0 $*" >> /opt/nDeploy/hook.log

if [ $2 -eq 1 ]; then
    CPANELUSER=$(stat -c "%U" $1)
else
    CPANELUSER=$(echo $1|awk -F'/' '{print $5}')
fi

# call when is created directory
if [[ $2 -eq 0 && $3 == "IN_CREATE|IN_ISDIR" ]]; then
  echo "from $$ Run INCREATE|IN_ISDIR part"
  /opt/nDeploy/scripts/apache_php_config_generator.py $CPANELUSER
fi

# call when is removed file
if [[ $2 -eq 0 && $3 == "IN_DELETE" ]]; then
  DOMAIN=$(echo $1|awk -F'/' '{print $6}')
  if [ -n "$DOMAIN" ]; then
    rm -f /etc/nginx/sites-enabled/$DOMAIN.conf /etc/nginx/sites-enabled/$DOMAIN.include /opt/nDeploy/domain-data/$DOMAIN
  fi
fi

if [[ $CPANELUSER == root || $CPANELUSER == *.lock || $CPANELUSER == .* || $1 == *main ]]; then
	exit 0
else
	(
		flock -x -w 300 500
		echo "from $$ Run generate_config reload_nginx part"
		/opt/nDeploy/scripts/generate_config.py $CPANELUSER
		/opt/nDeploy/scripts/reload_nginx.sh
	) 500>/opt/nDeploy/lock/$CPANELUSER.lock
	rm -f /opt/nDeploy/lock/$CPANELUSER.lock
fi
