#!/bin/bash
# Author: Anoop P Alias
# SetEnvIf X-Forwarded-Proto patch provided by https://github.com/mdpuma

function enable {
echo -e '\e[93m Modifying apache http and https port in cpanel \e[0m'
/usr/local/cpanel/bin/whmapi1 set_tweaksetting key=apache_port value=0.0.0.0:9999
/usr/local/cpanel/bin/whmapi1 set_tweaksetting key=apache_ssl_port value=0.0.0.0:4430
sed -i "s/80/9999/" /etc/chkserv.d/httpd
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1)
do
	echo "ConfGen:: $CPANELUSER" && /opt/nDeploy/scripts/generate_config.py $CPANELUSER
done

/usr/local/cpanel/libexec/tailwatchd --restart

echo -e '\e[93m Rebuilding Apache httpd backend configs and restarting daemons \e[0m'
/scripts/rebuildhttpdconf
/scripts/restartsrv httpd
osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
if [ ${osversion} -le 6 ];then
	service nginx restart
	service ndeploy_watcher restart
	service ndeploy_backends restart
	service memcached restart
	chkconfig nginx on
	chkconfig ndeploy_watcher on
	chkconfig ndeploy_backends on
	chkconfig memcached on
else
	systemctl restart nginx
	systemctl restart ndeploy_watcher
	systemctl restart ndeploy_backends
	systemctl restart memcached
	systemctl enable nginx
	systemctl enable ndeploy_watcher
	systemctl enable ndeploy_backends
	systemctl enable memcached
fi

}

function disable {

echo -e '\e[93m Reverting apache http and https port in cpanel \e[0m'
/usr/local/cpanel/bin/whmapi1 set_tweaksetting key=apache_port value=0.0.0.0:80
/usr/local/cpanel/bin/whmapi1 set_tweaksetting key=apache_ssl_port value=0.0.0.0:443
sed -i "s/9999/80/" /etc/chkserv.d/httpd

/usr/local/cpanel/whostmgr/bin/whostmgr2 --updatetweaksettings > /dev/null
/usr/local/cpanel/libexec/tailwatchd --restart

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
