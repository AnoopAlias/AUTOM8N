#!/usr/bin/env bash
#Author: Anoop P Alias

#Function defs
setup_ea4_php_cloudlinux(){
		for ver in 54 55 56 70 71 72 73 74 80
		do
			yum -y --disableplugin=universal-hooks --enablerepo=cloudlinux-updates-testing install ea-php$ver ea-php$ver-php-fpm ea-php$ver-php-opcache ea-php$ver-php-mysqlnd ea-php$ver-php-gd ea-php$ver-php-imap ea-php$ver-php-intl ea-php$ver-php-ioncube-loader ea-php$ver-php-xmlrpc ea-php$ver-php-xml ea-php$ver-php-mcrypt ea-php$ver-php-mbstring
			if [ ! -d /opt/cpanel/php$ver/root/var ];then
				mkdir -p /opt/cpanel/ea-php$ver/root/var/log
				mkdir -p /opt/cpanel/ea-php$ver/root/var/run
			fi
			/opt/nDeploy/scripts/update_backend.py add PHP CPANELPHP$ver /opt/cpanel/ea-php$ver/root
		done
		service ndeploy_backends stop || systemctl stop ndeploy_backends
		service ndeploy_backends start || systemctl start ndeploy_backends
		chkconfig ndeploy_backends on || systemctl enable ndeploy_backends
		if [ -f /opt/nDeploy/scripts/generate_default_vhost_config.py ];then
			/opt/nDeploy/scripts/generate_default_vhost_config.py
		else
			/opt/nDeploy/scripts/generate_default_vhost_config_slave.py
		fi
		nginx -s reload
	}

setup_ea4_php(){
		for ver in 54 55 56 70 71 72 73 74 80
		do
			yum -y --disableplugin=universal-hooks install ea-php$ver ea-php$ver-php-fpm ea-php$ver-php-opcache ea-php$ver-php-mysqlnd ea-php$ver-php-gd ea-php$ver-php-imap ea-php$ver-php-intl ea-php$ver-php-ioncube-loader ea-php$ver-php-xmlrpc ea-php$ver-php-xml ea-php$ver-php-mcrypt ea-php$ver-php-mbstring
			if [ ! -d /opt/cpanel/php$ver/root/var ];then
				mkdir -p /opt/cpanel/ea-php$ver/root/var/log
				mkdir -p /opt/cpanel/ea-php$ver/root/var/run
			fi
			/opt/nDeploy/scripts/update_backend.py add PHP CPANELPHP$ver /opt/cpanel/ea-php$ver/root
		done
		service ndeploy_backends stop || systemctl stop ndeploy_backends
		service ndeploy_backends start || systemctl start ndeploy_backends
		chkconfig ndeploy_backends on || systemctl enable ndeploy_backends
		if [ -f /opt/nDeploy/scripts/generate_default_vhost_config.py ];then
			/opt/nDeploy/scripts/generate_default_vhost_config.py
		else
			/opt/nDeploy/scripts/generate_default_vhost_config_slave.py
		fi
		nginx -s reload
	}

setup_remi_php(){
		yum -y install scl-utils libmcrypt
		osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
		if [ ${osversion} -eq 6 ];then
			yum -y install http://rpms.remirepo.net/enterprise/remi-release-6.rpm
		elif [ ${osversion} -eq 7 ];then
			yum -y install http://rpms.remirepo.net/enterprise/remi-release-7.rpm
		fi
		for ver in 54 55 56 70 71 72 73 74 80
		do
			yum -y --disableexcludes=main --enablerepo=remi install php$ver php$ver-php-fpm php$ver-php-opcache php$ver-php-mysqlnd php$ver-php-gd php$ver-php-imap php$ver-php-intl php$ver-php-ioncube-loader php$ver-php-xmlrpc php$ver-php-xml php$ver-php-mcrypt php$ver-php-mbstring
			ln -s /opt/remi/php$ver/root/usr/sbin /opt/remi/php$ver/root/
			if [ ! -d /opt/remi/php$ver/root/var ];then
				ln -s /var/opt/remi/php$ver /opt/remi/php$ver/root/var
			fi
			/opt/nDeploy/scripts/update_backend.py add PHP PHP$ver /opt/remi/php$ver/root
		done
		service ndeploy_backends stop || systemctl stop ndeploy_backends
		service ndeploy_backends start || systemctl start ndeploy_backends
		chkconfig ndeploy_backends on || systemctl enable ndeploy_backends
		if [ -f /opt/nDeploy/scripts/generate_default_vhost_config.py ];then
			/opt/nDeploy/scripts/generate_default_vhost_config.py
		else
			/opt/nDeploy/scripts/generate_default_vhost_config_slave.py
		fi
		nginx -s reload
	}

auto_setup(){
	if [ $(uname -r|grep lve) ];then
		if [ -f /etc/cpanel/ea4/is_ea4 ];then
			setup_ea4_php_cloudlinux
		else
			echo "EasyApache4 is not enabled.Please enable EasyApache4 and rerun this script"
			echo "You need ea-php* from the cloudlinux-updates-testing repo"
			echo "https://cloudlinux.com/cloudlinux-os-blog/entry/beta-easyapache-4-released-for-cloudlinux"
		fi
	elif [ -f /etc/cpanel/ea4/is_ea4 ];then
		setup_ea4_php
	else
		echo "EasyApache4 is not enabled.Please enable EasyApache4 and rerun this script"
		echo "https://documentation.cpanel.net/display/EA4/EasyApache+4+Home"
	fi
}

setup_ea4_cluster_php(){
			if [ ! -f /opt/nDeploy/conf/XTENDWEB_PHP_SETUP_LOCK_DO_NOT_REMOVE ]; then
				auto_setup
			fi
			for ver in 54 55 56 70 71 72 73 74 80
			do
				if [ -f /opt/nDeploy/conf/zz_xtendweb.ini ]; then
					rsync -a /opt/nDeploy/conf/zz_xtendweb.ini /opt/cpanel/ea-php$ver/root/etc/php.d/
				fi
			done
			service ndeploy_backends stop || systemctl stop ndeploy_backends
			service ndeploy_backends start || systemctl start ndeploy_backends
			chkconfig ndeploy_backends on || systemctl enable ndeploy_backends
	}

#End Function defs

if [ ! -z $1 ];then
	case $1 in
		cloudlinux)
			setup_ea4_php_cloudlinux
			;;
		ea4)
			setup_ea4_php
			;;
		ea4_cluster)
			setup_ea4_cluster_php
			;;
		remi)
			setup_remi_php
			;;
		*)
			auto_setup
			;;
	esac
else
	auto_setup
fi
