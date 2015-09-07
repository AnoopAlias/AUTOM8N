#!/bin/bash
# Author: Anoop P Alias
# SetEnvIf X-Forwarded-Proto patch provided by https://github.com/mdpuma

function enable {
echo -e '\e[93m Modifying apache http and https port in cpanel \e[0m'
sed -i "s/apache_port.*/apache_port=0.0.0.0:9999/" /var/cpanel/cpanel.config
sed -i "s/apache_ssl_port.*/apache_ssl_port=0.0.0.0:4430/" /var/cpanel/cpanel.config
sed -i "s/80/9999/" /etc/chkserv.d/httpd
/usr/local/cpanel/whostmgr/bin/whostmgr2 --updatetweaksettings > /dev/null
/usr/local/cpanel/libexec/tailwatchd --restart

if [ -f /var/cpanel/templates/apache2_4/vhost.local ];then
	sed -i "s/CustomLog/#CustomLog/" /var/cpanel/templates/apache2_4/vhost.local
else
	cp -p /var/cpanel/templates/apache2_4/vhost.default /var/cpanel/templates/apache2_4/vhost.local
	sed -i "s/CustomLog/#CustomLog/" /var/cpanel/templates/apache2_4/vhost.local
fi
if [ -f /var/cpanel/templates/apache2_4/ssl_vhost.local ];then
	sed -i "s/CustomLog/#CustomLog/" /var/cpanel/templates/apache2_4/ssl_vhost.local
else
	cp -p /var/cpanel/templates/apache2_4/ssl_vhost.default /var/cpanel/templates/apache2_4/ssl_vhost.local
	sed -i "s/CustomLog/#CustomLog/" /var/cpanel/templates/apache2_4/ssl_vhost.local
fi

if [ -f /var/cpanel/templates/apache2_2/vhost.local ];then
	sed -i "s/CustomLog/#CustomLog/" /var/cpanel/templates/apache2_2/vhost.local
else
	cp -p /var/cpanel/templates/apache2_2/vhost.default /var/cpanel/templates/apache2_2/vhost.local
	sed -i "s/CustomLog/#CustomLog/" /var/cpanel/templates/apache2_2/vhost.local
fi
if [ -f /var/cpanel/templates/apache2_2/ssl_vhost.local ];then
	sed -i "s/CustomLog/#CustomLog/" /var/cpanel/templates/apache2_2/ssl_vhost.local
else
	cp -p /var/cpanel/templates/apache2_2/ssl_vhost.default /var/cpanel/templates/apache2_2/ssl_vhost.local
	sed -i "s/CustomLog/#CustomLog/" /var/cpanel/templates/apache2_2/ssl_vhost.local
fi

echo "SetEnvIf X-Forwarded-Proto https HTTPS=on" >> /usr/local/apache/conf/includes/pre_virtualhost_global.conf
echo -e '\e[93m Rebuilding Apache httpd backend configs and restarting daemons \e[0m'
/scripts/rebuildhttpdconf
/scripts/restartsrv httpd
osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
if [ ${osversion} -le 6 ];then
	service nginx restart
	service ndeploy_watcher restart
	service ndeploy_backends restart
	chkconfig nginx on
	chkconfig ndeploy_watcher on
	chkconfig ndeploy_backends on
	for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1)
	do
		/opt/nDeploy/scripts/generate_config.py $CPANELUSER
	done
	service nginx restart
else
	systemctl restart nginx
	systemctl restart ndeploy_watcher
	systemctl restart ndeploy_backends
	systemctl enable nginx
	systemctl enable ndeploy_watcher
	systemctl enable ndeploy_backends
	for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1)
        do
                /opt/nDeploy/scripts/generate_config.py $CPANELUSER
        done
	systemctl restart nginx
fi

}

function disable {

echo -e '\e[93m Reverting apache http and https port in cpanel \e[0m'
sed -i "s/apache_port.*/apache_port=0.0.0.0:80/" /var/cpanel/cpanel.config
sed -i "s/apache_ssl_port.*/apache_ssl_port=0.0.0.0:443/" /var/cpanel/cpanel.config
sed -i "s/9999/80/" /etc/chkserv.d/httpd
/usr/local/cpanel/whostmgr/bin/whostmgr2 --updatetweaksettings > /dev/null
/usr/local/cpanel/libexec/tailwatchd --restart

sed -i "s/#CustomLog/CustomLog" /var/cpanel/templates/apache2_2/vhost.local
sed -i "s/#CustomLog/CustomLog" /var/cpanel/templates/apache2_2/ssl_vhost.local
sed -i "s/#CustomLog/CustomLog" /var/cpanel/templates/apache2_4/vhost.local
sed -i "s/#CustomLog/CustomLog" /var/cpanel/templates/apache2_4/ssl_vhost.local

sed -i '/SetEnvIf X-Forwarded-Proto https HTTPS=on/d' /usr/local/apache/conf/includes/pre_virtualhost_global.conf

echo -e '\e[93m Rebuilding Apache httpd backend configs.Apache will listen on default ports!  \e[0m'
osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
if [ ${osversion} -le 6 ];then
	service nginx stop
	service ndeploy_watcher stop
	service ndeploy_backends stop
	chkconfig nginx off
	chkconfig ndeploy_watcher off
	chkconfig ndeploy_backends off
else
	systemctl stop nginx
	systemctl stop ndeploy_watcher
	systemctl stop ndeploy_backends
	systemctl disable nginx
	systemctl disable ndeploy_watcher
	systemctl disable ndeploy_backends
fi
/scripts/rebuildhttpdconf
/scripts/restartsrv httpd

}


case "$1" in
        enable)
            enable
            ;;
         
        disable)
            disable
            ;;
        *)
            echo $"Usage: $0 {enable|disable}"
            exit 1
 
esac
