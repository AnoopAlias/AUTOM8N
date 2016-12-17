Setting up PHP
================

On CentOS6/CentOS7
-------------------

XtendWeb can work with PHP installed from the following Software Collection( SCL)

1. cPanel EA-PHP repo
``/opt/nDeploy/scripts/easy_php_setup.sh``

Additional PHP modules from ea-php repo can be added similar to example below
::

  yum search ea-php
  yum install ea-php70-php-intl
  systemctl restart ndeploy_backends || service ndeploy_backends restart

2. REMI repo
``/opt/nDeploy/scripts/easy_php_setup.sh remi``

Additional PHP modules from remi repo can be added similar to example below
::

  yum --disableexcludes=all --enablerepo=remi search php
  yum --disableexcludes=all --enablerepo=remi install php56-php-pecl-memcached
  systemctl restart ndeploy_backends || service ndeploy_backends restart

On CloudLinux6/CloudLinux7
------------------------------

XtendWeb can work with ea-php packages installed from the CloudLinux cloudlinux-updates-testing repo
Note that remi repo may work but the php in remi is not compiled with the CloudLinux patches so it
may not adhere to limits setup in CloudLinux

1. CloudLinux EA-PHP repo
::

  yum --enablerepo=cloudlinux-updates-testing search ea-php
  yum --enablerepo=cloudlinux-updates-testing install ea-php70-php-intl
  systemctl restart ndeploy_backends || service ndeploy_backends restart


Secure php-fpm setup
------------------------

The default PHP-FPM setup creates a single master process owned by root, which then spawns multiple pools
which run under the user credentials .The downside of this setup is that opcode caches like OpCache,APC etc share a single
cache making it less secure on a shared hosting environment

XtendWeb offers a solution on Centos7/CloudLinux7 servers by using socket activated php-fpm masters which run under each user
This setup requires more memory as each user will have a php-fpm master spawned

To use secure php-fpm
::

  #Works only on Centos7/CloudLinux7
  /opt/nDeploy/scripts/init_backends.py secure-php

To revert to single php-fpm master setup do
::

  rm -f /opt/nDeploy/conf/secure-php-enabled
  /opt/nDeploy/scripts/attempt_autofix.sh




Where are my php logs?
----------------------

XtendWeb creates php-fpm pool files for each user with the PHP error log file set to

``/home/CPANELUSER/logs/php_error_log``
Users can check the logs from their FileManager/FTP/SSH login


ZendOpcache and security considerations on php-fpm single master setup
-----------------------------------------------------------------------

. XtendWeb currently offers the following settings
that can mitigate the security risk of a shared OpCache memory to some extend

1. opcache.restrict_api
::

  opcache.restrict_api
  Allows calling OPcache API functions only from PHP scripts which path is started from specified string. The default "" means no restriction.
  This is set to /home/CPANELUSER/

2. opcache.blacklist_filename
::

  opcache.blacklist_filename
  The location of the OPcache blacklist file. A blacklist file is a text file containing the names of files that should not be accelerated, one per line. Wildcards are allowed, and prefixes can also be provided. Lines starting with a semi-colon are ignored as comments.
  This is set to /home/CPANELUSER/opcache-blacklist.txt
  User can upload the opcache-blacklist.txt to his homedir via FTP or ssh and paths in this file will not be cached.


Per user php.ini custom settings
---------------------------------

php-fpm lets users configure settings of type PHP_INI_PERDIR and PHP_INI_USER in .user.ini files

Ref: http://php.net/manual/en/configuration.file.per-user.php

the settings can be provided in ini format(same as php.ini) and the file must be named .user.ini


High Performance Wordpress setup using Redis cache and nginx-helper plugin
----------------------------------------------------------------------------

.. caution:: Require extra modules. System will break if not setup correctly

XtendWeb supports wordpress full page cache to redis as described at https://easyengine.io/wordpress-nginx/tutorials/single-site/redis_cache-with-conditional-purging/

Note that the template for this is not enabled by default as it needs support for additional optional
modules for the nginX server . If template is activated without installing the modules , it can lead into an invalid
server configuration .

Install Redis server
::

  yum install redis
  systemctl enable redis.service && systemctl start redis.service #centos7/cl7
  service redis start && chkconfig redis on #centos6/cl6

Install additional modules required by the template
::

  yum --enablerepo=ndeploy install nginx-nDeploy-module-redis nginx-nDeploy-module-redis2 nginx-nDeploy-module-echo nginx-nDeploy-module-set_misc nginx-nDeploy-module-srcache_filter

Register the template
::

  /opt/nDeploy/scripts/update_profiles.py add root main PHP wpredis_helper.j2 "Wordpress+Redis+nginx-helper"

Install the nginx-helper plugin in wordpress https://wordpress.org/plugins/nginx-helper/

Setup the nginx helper plugin as mentioned in https://easyengine.io/wordpress-nginx/tutorials/single-site/redis_cache-with-conditional-purging/
Leave the "Prefix" field blank in "Redis settings"



.. disqus::
