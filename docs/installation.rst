Installation
============
XtendWeb Requirements: cPanel 60.0+ server with CentOS6/CentOS7/CloudLinux6/CloudLinux7 64 bit OS installed

.. tip:: cPanel 60.0 is required as some hooks necessary for the plugin is only available in this version ownwards


* Migrating from nDeploy 3.x ? . Read the migration doc here:


1. Install EPEL repo
::

  yum -y install epel-release

#. Install XtendWeb yum repo
::

  yum -y install https://github.com/AnoopAlias/XtendWeb/raw/ndeploy4/nDeploy-release-centos-1.0-5.noarch.rpm

#. Install XtendWeb plugin and nginx. Be patient as this may take several minutes to complete.
::

  yum --enablerepo=ndeploy install nginx-nDeploy nDeploy

#. Install PHP-FPM Application server
::

  #Install PHP-FPM Application server for PHP
  /opt/nDeploy/scripts/easy_php_setup.sh

#. Install Phusion Passenger ( only if you need support for RUBY/PYTHON/NODEJS )

  #Enable Phusion Passenger Application Server backend. This is required for Ruby/Python/NodeJS.

  yum --enablerepo=ndeploy install nginx-nDeploy-module-passenger
  /opt/nDeploy/scripts/easy_passenger_setup.sh

#. Enable the plugin. This will make nginx your frontend webserver.
::

  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh enable

#. Install Optional additional modules
::

  #Note that each module increases the nginx size and processing requirements
  #So install only required functionality .
  pagespeed  - yum --enablerepo=ndeploy install nginx-nDeploy-module-pagespeed
  brotli - yum --enablerepo=ndeploy install nginx-nDeploy-module-brotli
  geoip - yum --enablerepo=ndeploy install nginx-nDeploy-module-geoip
  naxsi - yum --enablerepo=ndeploy install nginx-nDeploy-module-naxsi

.. tip:: There are no additonal configurations required for the loadable modules. Users can control the functionality from XtendWeb UI


.. disqus::
