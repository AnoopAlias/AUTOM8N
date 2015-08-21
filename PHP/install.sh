#!/bin/sh

yum install libmcrypt-devel openssl-devel gmp-devel libcurl-devel libcurlssl-devel -y

curl -L -O https://github.com/phpbrew/phpbrew/raw/master/phpbrew
chmod +x phpbrew
sudo mv phpbrew /usr/bin/phpbrew

phpbrew init

# Download cloudlinux patches
if [ ! -f "cl-apache-patches.tar.gz" ]; then
	wget http://repo.cloudlinux.com/cloudlinux/sources/da/cl-apache-patches.tar.gz -O cl-apache-patches.tar.gz
fi

tar xvzf cl-apache-patches.tar.gz fpm-lve-php5.4.patch

read

# patch -p1 < fpm-lve-php5.4.patch

source ~/.phpbrew/bashrc

php -n /usr/bin/phpbrew --debug install --jobs 4 --patch fpm-lve-php5.4.patch 5.4.42 +default +fpm +mysql +exif +ftp +gd +intl +soap +pdo +curl +gmp +imap -- --with-libdir=lib64 --with-gd=shared --enable-gd-natf --with-jpeg-dir=/usr --with-png-dir=/usr

phpbrew use php-5.4.42

phpbrew ext install curl
phpbrew ext install zendopcache
phpbrew ext install memcached
phpbrew ext install memcache
phpbrew ext install pdo_sqlite
phpbrew ext install xhprof 0.9.4
phpbrew ext disable xhprof

/opt/nDeploy/scripts/update_backend.py PHP php-5.4.42 /usr/local/phpbrew/php/php-5.4.42