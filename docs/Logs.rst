Managing Logs
=============

**nDeploy logs**

watcher logs ``/opt/nDeploy/watcher.log``

cPanel hooks log
::

  WHM:: Home »Server Configuration »Tweak Settings
    Standardized Hooks - Debug Mode on
  Log is available at /usr/local/cpanel/logs/error_log

**nginx logs**

nginx logs include the webserver log , stdout from application servers like
php-fpm ,phusion passenger etc

  ``/var/log/nginx/error_log``

**PHP-FPM master process log**

Note that this is not php log ;but logging related to php-fpm master process
php errors will be logged to the webserver's error log
::

  PHPROOT/var/log/php-fpm.log
  eg : /opt/remi/php56/root/var/log/php-fpm.log

.. disqus::
