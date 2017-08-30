XtendWeb standalone installation
===================================

XtendWeb Requirements: cPanel 60.0+ server with CentOS6/CentOS7/CloudLinux6/CloudLinux7 64 bit OS installed .

.. note:: CentOS7/EA4/PHP-FPM is recommended

.. note:: Starting with Xtendweb version 4.3.20 you need to subscribe to a license for installing XtendWeb
          Please visit https://autom8n.com/plans.html#plans for more info


`PURCHASE XTENDWEB LICENSE <https://support.gnusys.net/order.php?step=0&productGroup=5>`_.



1. Install and Enable the plugin
::

  yum -y install epel-release
  yum -y install https://github.com/AnoopAlias/XtendWeb/raw/ndeploy4/nDeploy-release-centos-1.0-6.noarch.rpm

  # Purchase a license so the server can access xtendweb yum repo

  yum -y --enablerepo=ndeploy install nginx-nDeploy nDeploy # For nginx as webserver
     OR
  yum -y --enablerepo=ndeploy install openresty-nDeploy nDeploy # For openresty as webserver

  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh enable

  # For resource control using systemd on CentOS7
  yum -y --enablerepo=ndeploy install simpler-nDeploy  #Do NOT do this on CloudLinux

  # For installing netdata server health monitoring
  /opt/nDeploy/scripts/easy_netdata_setup.sh



.. note::  OpenResty should be used only if you need to extend Nginx with LUA. OpenResty provided by XtendWeb lacks mod_security and NAXSI WAF's

.. note:: Redis Full page cache for Wordpress and Drupal is not compatible with PageSpeed and ModSec v3




Application servers
-----------------------

For switching to Nginx completely and not proxy to Apache httpd, Nginx must have various application servers for processing dynamic content. Proceed further to install various app servers.


2.1. Install PHP-FPM Application server
::

  /opt/nDeploy/scripts/easy_php_setup.sh
  # php-fpm and a selected set of modules are installed from the EA4 php repo


.. note:: PHP-FPM pools are chrooted to /home/virtfs . In addition with cPanel JailShell, this provides an isolated environment for each user




2.2. Install HHVM Hack/PHP Application server
::

  /opt/nDeploy/scripts/easy_hhvm_setup.sh


2.3. Install Full Page Redis cache template for WordPress and Drupal
::

  /opt/nDeploy/scripts/setup_additional_templates.sh
  # Disable PageSpeed and ModSec on domains using Full page cache


2.4. Install Phusion Passenger App server for Python/Ruby/NodeJS
::

  yum --enablerepo=ndeploy install nginx-nDeploy-module-passenger # Nginx
  OR
  yum --enablerepo=ndeploy install openresty-nDeploy-module-passenger # Openresty

  /opt/nDeploy/scripts/easy_passenger_setup.sh



.. note:: If you modify WHM service certificate run /opt/nDeploy/scripts/generate_default_vhost_config.py && nginx -s reload

3. Best effort switch to native nginx on as many domains as possible . Wordpress, Joomla , Drupal and Magento webapps is targeted
::

  # When the script prompts for the default PHP version using the system default or the one you know is used by most domains
  /opt/nDeploy/scripts/switch_to_native_nginx.sh



4. Install Optional additional modules
::

  #Note that each module increases the nginx size and processing requirements
  #So install only required functionality .
  (pagespeed)   yum --enablerepo=ndeploy install nginx-nDeploy-module-pagespeed
  (pagespeed)   yum --enablerepo=ndeploy install openresty-nDeploy-module-pagespeed  # OpenResty
  (brotli)      yum --enablerepo=ndeploy install nginx-nDeploy-module-brotli
  (brotli)      yum --enablerepo=ndeploy install openresty-nDeploy-module-brotli  # OpenResty
  (geoip)       yum --enablerepo=ndeploy install nginx-nDeploy-module-geoip
  (geoip)       yum --enablerepo=ndeploy install openresty-nDeploy-module-geoip # OpenResty
  (naxsi)       yum --enablerepo=ndeploy install nginx-nDeploy-module-naxsi
  (modsecurityv3) yum --enablerepo=ndeploy install nginx-nDeploy-module-modsecurity
  (redis)       yum --enablerepo=ndeploy install nginx-nDeploy-module-redis
  (redis2)      yum --enablerepo=ndeploy install nginx-nDeploy-module-redis2
  (set_misc)    yum --enablerepo=ndeploy install nginx-nDeploy-module-set_misc
  (srcache)     yum --enablerepo=ndeploy install nginx-nDeploy-module-srcache_filter
  (echo)        yum --enablerepo=ndeploy install nginx-nDeploy-module-echo
  (testcookie_access) yum --enablerepo=ndeploy install nginx-nDeploy-module-testcookie_access
  (testcookie_access) yum --enablerepo=ndeploy install openresty-nDeploy-module-testcookie_access # OpenResty

  # Following modules are installed and loaded by default in nginx but can be disabled
  (headers_more)
  (ndk) Nginx Development ToolKit
  # Following modules are installed and loaded by default in openresty
  https://openresty.org/en/components.html

.. note:: There are no additional configurations required for the loadable modules.XtendWeb activates the functionality if the rpm is found installed
