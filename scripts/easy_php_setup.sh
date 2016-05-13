#!/bin/bash
#Author: Anoop P Alias

#Function defs

setup_lve_patched_php(){
	wget -O /tmp/phpversion.hint https://rpm.piserve.com/phpversion.hint

	#Compile PHP54
	compile_php54(){

	php54_ver=$(cat /tmp/phpversion.hint|grep "^5.4")
	echo "Compiling .... ${php54_ver}"
	wget -O /usr/local/src/php-${php54_ver}.tar.bz2 http://us2.php.net/distributions/php-${php54_ver}.tar.bz2
	tar -xvjf /usr/local/src/php-${php54_ver}.tar.bz2 -C /usr/local/src/
	wget -O /usr/local/src/cl-apache-patches.tar.gz http://repo.cloudlinux.com/cloudlinux/sources/da/cl-apache-patches.tar.gz
	cd /usr/local/src/php-${php54_ver}
	tar -xvzf /usr/local/src/cl-apache-patches.tar.gz fpm-lve-php5.4_autoconf.patch
	patch -p1 --fuzz=10 < fpm-lve-php5.4_autoconf.patch
	autoconf
	config_args=$(php-config --configure-options|sed "s/LDFLAGS= /LDFLAGS=/;s/--prefix=\/usr\/local //;s/--with-apxs2=\/usr\/local\/apache\/bin\/apxs//;s/--with-config-file-path=\/usr\/local\/lib//;s/--with-config-file-scan-dir=\/usr\/local\/lib\/php\.ini\.d//")
	./configure ${config_args} --enable-fpm --prefix=/usr/local/php54_fpm
	make
	make install
	cd -
	rm -rf /usr/local/src/php-${php54_ver} /usr/local/src/php-${php54_ver}.tar.bz2 /usr/local/src/cl-apache-patches.tar.gz
	/opt/nDeploy/scripts/update_backend.py PHP PHP54_LVE /usr/local/php54_fpm
	}

	#Compile PHP55
	compile_php55(){

	php55_ver=$(cat /tmp/phpversion.hint|grep "^5.5")
	echo "Compiling .... ${php55_ver}"
	wget -O /usr/local/src/php-${php55_ver}.tar.bz2 http://us2.php.net/distributions/php-${php55_ver}.tar.bz2
	tar -xvjf /usr/local/src/php-${php55_ver}.tar.bz2 -C /usr/local/src/
	wget -O /usr/local/src/cl-apache-patches.tar.gz http://repo.cloudlinux.com/cloudlinux/sources/da/cl-apache-patches.tar.gz
	cd /usr/local/src/php-${php55_ver}
	tar -xvzf /usr/local/src/cl-apache-patches.tar.gz fpm-lve-php5.5_autoconf.patch
	patch -p1 --fuzz=10 < fpm-lve-php5.5_autoconf.patch
	autoconf
	config_args=$(php-config --configure-options|sed "s/LDFLAGS= /LDFLAGS=/;s/--prefix=\/usr\/local //;s/--with-apxs2=\/usr\/local\/apache\/bin\/apxs//;s/--with-config-file-path=\/usr\/local\/lib//;s/--with-config-file-scan-dir=\/usr\/local\/lib\/php\.ini\.d//")
	./configure ${config_args} --enable-fpm --enable-opcache --prefix=/usr/local/php55_fpm
	make
	make install
	cd -
	rm -rf /usr/local/src/php-${php55_ver} /usr/local/src/php-${php55_ver}.tar.bz2 /usr/local/src/cl-apache-patches.tar.gz
	/opt/nDeploy/scripts/update_backend.py PHP PHP55_LVE /usr/local/php55_fpm
	}

	#Compile PHP56
	compile_php56(){

	php56_ver=$(cat /tmp/phpversion.hint|grep "^5.6")
	echo "Compiling .... ${php56_ver}"
	wget -O /usr/local/src/php-${php56_ver}.tar.bz2 http://us2.php.net/distributions/php-${php56_ver}.tar.bz2
	tar -xvjf /usr/local/src/php-${php56_ver}.tar.bz2 -C /usr/local/src/
	wget -O /usr/local/src/cl-apache-patches.tar.gz http://repo.cloudlinux.com/cloudlinux/sources/da/cl-apache-patches.tar.gz
	cd /usr/local/src/php-${php56_ver}
	tar -xvzf /usr/local/src/cl-apache-patches.tar.gz fpm-lve-php5.6_autoconf.patch
	patch -p1 --fuzz=10 < fpm-lve-php5.6_autoconf.patch
	autoconf
	config_args=$(php-config --configure-options|sed "s/LDFLAGS= /LDFLAGS=/;s/--prefix=\/usr\/local //;s/--with-apxs2=\/usr\/local\/apache\/bin\/apxs//;s/--with-config-file-path=\/usr\/local\/lib//;s/--with-config-file-scan-dir=\/usr\/local\/lib\/php\.ini\.d//")
	./configure ${config_args} --enable-fpm --enable-opcache --prefix=/usr/local/php56_fpm
	make
	make install
	cd -
	rm -rf /usr/local/src/php-${php56_ver} /usr/local/src/php-${php56_ver}.tar.bz2 /usr/local/src/cl-apache-patches.tar.gz
	/opt/nDeploy/scripts/update_backend.py PHP PHP56_LVE /usr/local/php56_fpm
	}

	#Compile PHP56
	compile_php70(){

	php70_ver=$(cat /tmp/phpversion.hint|grep "^7.0")
	echo "Compiling .... ${php70_ver}"
	wget -O /usr/local/src/php-${php70_ver}.tar.bz2 http://us2.php.net/distributions/php-${php70_ver}.tar.bz2
	tar -xvjf /usr/local/src/php-${php70_ver}.tar.bz2 -C /usr/local/src/
	wget -O /usr/local/src/cl-apache-patches.tar.gz http://repo.cloudlinux.com/cloudlinux/sources/da/cl-apache-patches.tar.gz
	cd /usr/local/src/php-${php70_ver}
	tar -xvzf /usr/local/src/cl-apache-patches.tar.gz fpm-lve-php5.6_autoconf.patch
	patch -p1 --fuzz=10 < fpm-lve-php5.6_autoconf.patch
	autoconf
	config_args=$(php-config --configure-options|sed "s/LDFLAGS= /LDFLAGS=/;s/--prefix=\/usr\/local //;s/--with-apxs2=\/usr\/local\/apache\/bin\/apxs//;s/--with-config-file-path=\/usr\/local\/lib//;s/--with-config-file-scan-dir=\/usr\/local\/lib\/php\.ini\.d//")
	./configure ${config_args} --enable-fpm --enable-opcache --prefix=/usr/local/php70_fpm
	make
	make install
	cd -
	rm -rf /usr/local/src/php-${php70_ver} /usr/local/src/php-${php70_ver}.tar.bz2 /usr/local/src/cl-apache-patches.tar.gz
	/opt/nDeploy/scripts/update_backend.py PHP PHP70_LVE /usr/local/php70_fpm
	}

	#comment any of the functions below to prevent that version from compiling
	compile_php54
	compile_php55
	compile_php56
	compile_php70



	osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
	echo ${osversion}
	if [ ${osversion} -eq 6 ];then
		/etc/init.d/ndeploy_backends stop
		/etc/init.d/ndeploy_backends start
		chkconfig ndeploy_backends on
	elif [ ${osversion} -eq 7 ];then
		systemctl stop ndeploy_backends
		systemctl start ndeploy_backends
		systemctl enable ndeploy_backends
	else
		echo "ndeploy_backends not restarted"
	fi
}


setup_ea4_php(){
		yum -y install ea-php54-php-fpm ea-php55-php-fpm ea-php56-php-fpm ea-php70-php-fpm

		for ver in 54 55 56 70
		do
			if [ ! -d /opt/cpanel/php$ver/root/var ];then
				mkdir -p /opt/cpanel/ea-php$ver/root/var/log
				mkdir -p /opt/cpanel/ea-php$ver/root/var/run
			fi
			/opt/nDeploy/scripts/update_backend.py PHP CPANELPHP$ver /opt/cpanel/ea-php$ver/root
			service ndeploy_backends stop || systemctl stop ndeploy_backends
			service ndeploy_backends start || systemctl start ndeploy_backends
			chkconfig ndeploy_backends on || systemctl enable ndeploy_backends
		done
	}

setup_remi_php(){
		yum -y install scl-utils libmcrypt
		osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
		echo ${osversion}
		if [ ${osversion} -eq 6 ];then
			yum -y install http://rpms.remirepo.net/enterprise/remi-release-6.rpm
			for ver in 54 55 56 70
			do
				yum -y --disableexcludes=main --enablerepo=remi install php$ver php$ver-php-fpm php$ver-php-opcache php$ver-php-mysqlnd php$ver-php-gd php$ver-php-imap php$ver-php-intl php$ver-php-ioncube-loader php$ver-php-xmlrpc php$ver-php-xml php$ver-php-mcrypt php$ver-php-mbstring php$ver-php-ioncube-loader php$ver-php-intl php$ver-php-imap php$ver-php-gd
				ln -s /opt/remi/php$ver/root/usr/sbin /opt/remi/php$ver/root/
				if [ ! -d /opt/remi/php$ver/root/var ];then
					ln -s /var/opt/remi/php$ver /opt/remi/php$ver/root/var
				fi
				/opt/nDeploy/scripts/update_backend.py PHP PHP$ver /opt/remi/php$ver/root
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
				/opt/nDeploy/scripts/update_backend.py PHP PHP$ver /opt/remi/php$ver/root
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
		setup_lve_patched_php
	elif [ -f /etc/cpanel/ea4/is_ea4 ];then
		setup_ea4_php
	else
		setup_remi_php
	fi
}

#End Function defs

if [ ! -z $1 ];then
	case $1 in
		cloudlinux)
			setup_lve_patched_php
			;;
		ea4)
			setup_ea4_php
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
