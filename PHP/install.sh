#!/bin/sh

yum install libmcrypt-devel openssl-devel gmp-devel curl-devel libcurl-devel libcurlssl-devel -y
yum install firebird-devel -y

curl -L -O https://github.com/phpbrew/phpbrew/raw/master/phpbrew
chmod +x phpbrew
sudo mv phpbrew /usr/bin/phpbrew

phpbrew init

# Download cloudlinux patches
if [ ! -f "cl-apache-patches.tar.gz" ]; then
	wget http://repo.cloudlinux.com/cloudlinux/sources/da/cl-apache-patches.tar.gz -O cl-apache-patches.tar.gz
fi

read

# patch -p1 < fpm-lve-php5.4.patch

source ~/.phpbrew/bashrc

export PHPBREW_ROOT=/usr/local/phpbrew
mkdir $PHPBREW_ROOT -v

php -n /usr/bin/phpbrew --debug install --jobs 12 --patch fpm-lve-php5.4_fixed.patch 5.6.15 +default +fpm +mysql +exif +ftp +gd +intl +soap +pdo +curl +gmp +imap +opcache -- --with-libdir=lib64 --with-gd=shared --enable-gd-natf --with-jpeg-dir=/usr --with-png-dir=/usr
php -n /usr/bin/phpbrew --debug install --jobs 12 --patch fpm-lve-php5.4_fixed.patch 5.5.30 +default +fpm +mysql +exif +ftp +gd +intl +soap +pdo +curl +gmp +imap -- --with-libdir=lib64 --with-gd=shared --enable-gd-natf --with-jpeg-dir=/usr --with-png-dir=/usr
php -n /usr/bin/phpbrew --debug install --jobs 12 --patch fpm-lve-php5.4_fixed.patch 5.4.45 +default +fpm +mysql +exif +ftp +gd +intl +soap +pdo +curl +gmp +imap -- --with-libdir=lib64 --with-gd=shared --enable-gd-natf --with-jpeg-dir=/usr --with-png-dir=/usr
php -n /usr/bin/phpbrew --debug install --jobs 12 --patch fpm-lve-php5.4_fixed.patch 5.3.29 +default +fpm +mysql +exif +ftp +gd +intl +soap +pdo +curl +gmp +imap -- --with-libdir=lib64 --with-gd=shared --enable-gd-natf --with-jpeg-dir=/usr --with-png-dir=/usr


phpbrew use php-5.4.42

phpbrew ext install imagick
phpbrew ext install iconv
phpbrew ext install pdo_sqlite
phpbrew ext install pdo_dblib
phpbrew ext install pdo_firebird
# phpbrew ext install curl
phpbrew ext install memcached
phpbrew ext install memcache
phpbrew ext install gd
phpbrew ext install uploadprogress
phpbrew ext install sqlite3
phpbrew ext install xhprof 0.9.4
phpbrew ext disable xhprof

# for bnpmd
phpbrew ext install gettext

http://www.directadmin.com/imap.txt
yum install libc-client-devel uw-imap.x86_64
phpbrew ext install imap


/opt/nDeploy/scripts/update_backend.py PHP php-5.4.45 /usr/local/phpbrew/php/php-5.4.45