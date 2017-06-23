#!/bin/bash
#Author: Anoop P Alias

#Function defs
setup_ea4_php_cloudlinux(){
		for ver in 54 55 56 70 71
		do
			yum -y --enablerepo=cloudlinux-updates-testing install ea-php$ver ea-php$ver-php-fpm ea-php$ver-php-opcache ea-php$ver-php-mysqlnd ea-php$ver-php-gd ea-php$ver-php-imap ea-php$ver-php-intl ea-php$ver-php-ioncube-loader ea-php$ver-php-xmlrpc ea-php$ver-php-xml ea-php$ver-php-mcrypt ea-php$ver-php-mbstring
			if [ ! -d /opt/cpanel/php$ver/root/var ];then
				mkdir -p /opt/cpanel/ea-php$ver/root/var/log
				mkdir -p /opt/cpanel/ea-php$ver/root/var/run
			fi
			/opt/nDeploy/scripts/update_backend.py add PHP CPANELPHP$ver /opt/cpanel/ea-php$ver/root
			if [ -f /opt/nDeploy/conf/ndeploy_cluster.yaml ]; then
				rsync /opt/nDeploy/conf/zz_xtendweb.ini /opt/cpanel/ea-php$ver/root/etc/php.d/
			fi
			service ndeploy_backends stop || systemctl stop ndeploy_backends
			service ndeploy_backends start || systemctl start ndeploy_backends
			chkconfig ndeploy_backends on || systemctl enable ndeploy_backends
		done
	}

setup_ea4_php(){
		for ver in 54 55 56 70 71
		do
			yum -y install ea-php$ver ea-php$ver-php-fpm ea-php$ver-php-opcache ea-php$ver-php-mysqlnd ea-php$ver-php-gd ea-php$ver-php-imap ea-php$ver-php-intl ea-php$ver-php-ioncube-loader ea-php$ver-php-xmlrpc ea-php$ver-php-xml ea-php$ver-php-mcrypt ea-php$ver-php-mbstring
			if [ ! -d /opt/cpanel/php$ver/root/var ];then
				mkdir -p /opt/cpanel/ea-php$ver/root/var/log
				mkdir -p /opt/cpanel/ea-php$ver/root/var/run
			fi
			/opt/nDeploy/scripts/update_backend.py add PHP CPANELPHP$ver /opt/cpanel/ea-php$ver/root

			service ndeploy_backends stop || systemctl stop ndeploy_backends
			service ndeploy_backends start || systemctl start ndeploy_backends
			chkconfig ndeploy_backends on || systemctl enable ndeploy_backends
		done
		# Securing php-fpm with chroot setup using virtfs
		echo -e '\e[93m Setting up chrooted php-fpm using virtfs jails by default \e[0m'
		if [ -d /opt/nDeploy/conf/nDeploy-cluster ];then
			/usr/local/cpanel/bin/whmapi1 set_tweaksetting key=jaildefaultshell value=1
		fi
		if [ ! -d  /var/cpanel/feature_toggles ];then
			mkdir -p /var/cpanel/feature_toggles
		fi
		touch  /var/cpanel/feature_toggles/apachefpmjail
		echo -e '\e[93m SECURITY TIP ::  CHROOTED PHP-FPM :: I have set jail shell as default for newly created accounts \e[0m'
		echo -e '\e[93m For existing accounts please set Jailed Shell(apply to all) at WHM \e[0m'
		echo -e '\e[93m Home »Account Functions »Manage Shell Access \e[0m'

	}

	setup_ea4_cluster_php(){
			for ver in 54 55 56 70 71
			do
				yum -y install ea-php$ver ea-php$ver-php-fpm ea-php$ver-php-opcache ea-php$ver-php-mysqlnd ea-php$ver-php-gd ea-php$ver-php-imap ea-php$ver-php-intl ea-php$ver-php-ioncube-loader ea-php$ver-php-xmlrpc ea-php$ver-php-xml ea-php$ver-php-mcrypt ea-php$ver-php-mbstring
				if [ ! -d /opt/cpanel/php$ver/root/var ];then
					mkdir -p /opt/cpanel/ea-php$ver/root/var/log
					mkdir -p /opt/cpanel/ea-php$ver/root/var/run
				fi
				/opt/nDeploy/scripts/update_backend.py add PHP CPANELPHP$ver /opt/cpanel/ea-php$ver/root
				/opt/cpanel/ea-php$ver/root/usr/bin/pecl install redis
				if [ -f /opt/nDeploy/conf/zz_xtendweb.ini ]; then
					rsync -a /opt/nDeploy/conf/zz_xtendweb.ini /opt/cpanel/ea-php$ver/root/etc/php.d/
				fi

				service ndeploy_backends stop || systemctl stop ndeploy_backends
				service ndeploy_backends start || systemctl start ndeploy_backends
				chkconfig ndeploy_backends on || systemctl enable ndeploy_backends
			done
			# Securing php-fpm with chroot setup using virtfs
			if [ -d /opt/nDeploy/conf/nDeploy-cluster ];then
				/usr/local/cpanel/bin/whmapi1 set_tweaksetting key=jaildefaultshell value=1
			fi
			if [ ! -d  /var/cpanel/feature_toggles ];then
				mkdir -p /var/cpanel/feature_toggles
			fi
			touch  /var/cpanel/feature_toggles/apachefpmjail

		}

setup_remi_php(){
		yum -y install scl-utils libmcrypt
		osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
		echo ${osversion}
		if [ ${osversion} -eq 6 ];then
			yum -y install http://rpms.remirepo.net/enterprise/remi-release-6.rpm
			for ver in 54 55 56 70 71
			do
				yum -y --disableexcludes=main --enablerepo=remi install php$ver php$ver-php-fpm php$ver-php-opcache php$ver-php-mysqlnd php$ver-php-gd php$ver-php-imap php$ver-php-intl php$ver-php-ioncube-loader php$ver-php-xmlrpc php$ver-php-xml php$ver-php-mcrypt php$ver-php-mbstring
				ln -s /opt/remi/php$ver/root/usr/sbin /opt/remi/php$ver/root/
				if [ ! -d /opt/remi/php$ver/root/var ];then
					ln -s /var/opt/remi/php$ver /opt/remi/php$ver/root/var
				fi
				/opt/nDeploy/scripts/update_backend.py add PHP PHP$ver /opt/remi/php$ver/root
				/etc/init.d/ndeploy_backends stop
				/etc/init.d/ndeploy_backends start
				chkconfig ndeploy_backends on
			done
		elif [ ${osversion} -eq 7 ];then
			yum -y install http://rpms.remirepo.net/enterprise/remi-release-7.rpm
			for ver in 54 55 56 70
			do
				yum -y --disableexcludes=main --enablerepo=remi install php$ver php$ver-php-fpm php$ver-php-opcache php$ver-php-mysqlnd php$ver-php-gd php$ver-php-imap php$ver-php-intl php$ver-php-ioncube-loader php$ver-php-xmlrpc php$ver-php-xml php$ver-php-mcrypt php$ver-php-mbstring php$ver-php-ioncube-loader php$ver-php-intl php$ver-php-imap php$ver-php-gd
				if [ ! -d /opt/remi/php$ver/root/var ];then
					ln -s /var/opt/remi/php$ver /opt/remi/php$ver/root/var
				fi
				/opt/nDeploy/scripts/update_backend.py add PHP PHP$ver /opt/remi/php$ver/root

				systemctl stop ndeploy_backends
				systemctl start ndeploy_backends
				systemctl enable ndeploy_backends
			done
		else
			echo "ERROR: Unknown OS Version detected. Aborting Install "
		fi
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
