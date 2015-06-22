#!/bin/sh

echo -e '\e[93m Setting up default vhost proxy in nginx \e[0m'
cpanelmainip=$(grep ADDR /etc/wwwacct.conf|awk '{print $2}')
hostname=$(grep HOST /etc/wwwacct.conf|awk '{print $2}')
if [ -z $cpanelmainip ] || [ -z $hostname ]; then
	echo "Cant read IP ADDRESS from /etc/wwwacct.conf";
	exit 1;
fi
sed -i "s/CPANELIP/$cpanelmainip/g" /etc/nginx/conf.d/default_server.conf
sed -i "s/HOSTNAME/$hostname/g" /etc/nginx/conf.d/default_server.conf
sed -i "s/CPANELIP/$cpanelmainip/g" /etc/nginx/conf.d/cpanel_services.conf

if [ -f /etc/csf/csf.pignore ]; then
	echo -e '\e[93m Setting up CSF firewall to ignore nginx process \e[0m'
	grep -w '/usr/sbin/nginx' /etc/csf/csf.pignore || echo 'exe:/usr/sbin/nginx' >> /etc/csf/csf.pignore
fi
if [ ! -d /etc/nginx/sites-enabled ]; then
	mkdir /etc/nginx/sites-enabled
fi
if [ ! -d /etc/nginx/ssl ]; then
	mkdir /etc/nginx/ssl
fi
