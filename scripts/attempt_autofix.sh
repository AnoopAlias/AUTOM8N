#!/bin/bash


##Attempt to re-generate all nginx config
touch /opt/nDeploy/conf/skip_nginx_reload
touch /opt/nDeploy/conf/skip_php-fpm_reload

echo -e '\e[93m Attempting to regenerate all nginx conf  \e[0m'
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);do echo "ConfGen:: $CPANELUSER" && /opt/nDeploy/scripts/generate_config.py $CPANELUSER;done

rm -f /opt/nDeploy/conf/skip_nginx_reload /opt/nDeploy/conf/skip_php-fpm_reload

# Reloading nginx
/usr/sbin/nginx -s reload

##Attempt to fix backends issue
echo -e '\e[93m Attempting to restart all backend Application servers \e[0m'

systemctl restart ndeploy_backends || service ndeploy_backends restart

echo -e '\e[93m The following PHP-FPM master process has started \e[0m'

for pid in $(pidof php-fpm)
do
    lsof -p $pid | grep txt
done


##Restart ndeploy_watcher
echo -e '\e[93m Attempting to restart ndeploy_watcher daemon \e[0m'

service ndeploy_watcher stop || systemctl ndeploy_watcher stop
rm -f /opt/nDeploy/watcher.pid
service ndeploy_watcher start || systemctl ndeploy_watcher start
