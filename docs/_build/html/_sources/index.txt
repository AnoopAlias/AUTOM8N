.. nDeploy documentation master file, created by
   sphinx-quickstart on Tue Aug  2 11:13:22 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

nDeploy
=======

Contents:

Features
========
* Supports CentOS6 CentOS7 CloudLinux6 CloudLinux7 on x86_64 arch
* Multiple backends - Apache HTTPD, PHP-FPM, HHVM, ColdFusion/Java, Python, Ruby on Rails, NodeJS
* Supports caching/conditional cache purging in proxy and FastCGI(ngx_cache_purge)
* Google PageSpeed support
* limit_req, limit_conn support
* NAXSI Web Application Firewall
* IPv6 support
* SSL support
* HTTP2 support
* Fast installation,upgrade and uninstall via yum
* High Available WebStack
* High Available SMTP service
* High Available DataBase (MariaDB/MySQL)

Installation
============
Requirement : cPanel 11.48+ server with Centos6/Centos7/CloudLinux6/CloudLinux7 64 bit OS installed

nDeploy 3.x is available via yum (Supports PHP-FPM from EasyApache4 or REMI repo)

nDeploy 2.0.65 is available as an RPM package for manual install

CentOS6/CloudLinux6 - https://rpm.piserve.com/CentOS/6/x86_64/

CentOS7/CloudLinux7 - https://rpm.piserve.com/CentOS/7/x86_64/

1. Install EPEL repo
::

  yum -y install epel-release

2. Install nDeploy yum repo
::

  rpm --import https://rpm.piserve.com/RPM-GPG-KEY-ndeploy
  yum -y install https://rpm.piserve.com/nDeploy-release-centos-1.0-2.noarch.rpm

3. Install nDeploy plugin and nginx .Be patient as this may take sometime to complete
::

  yum --enablerepo=ndeploy install nginx-nDeploy nDeploy

4. Install or enable Application servers .You can skip any step below as per your app server requirement
::

  #Install PHP-FPM Application server for PHP
  /opt/nDeploy/scripts/easy_php_setup.sh

  #Enable Phusion Passenger Application Server backend. This is required for Ruby/Python/NodeJs
  /usr/nginx/scripts/nginx-passenger-setup.sh

5. Enable the plugin. This will make nginX your frontend webServer
::

  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh enable

6. Step4(Optional) : Setup NAXSI learning .This is required to generate NAXSI whitelist rules
::

  #Note that this step will install JAVA and ElasticSearch daemon for NXAPI
  /usr/nginx/scripts/nxapi-setup.sh





.. toctree::
   :maxdepth: 2

   mod_remoteip


* :ref:`search`
