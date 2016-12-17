.. XtendWeb documentation master file, created by
   sphinx-quickstart on Tue Aug  2 11:13:22 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: Xtendweb_banner.jpg


XtendWeb is the worlds easiest and scalable nginX deployment tool that seemlessly plugs into your
cPanel/WHM powered server .The result - you get a faster reliable webstack and can deploy your web applications to multiple web
servers which are DNS load-balanced .

XtendWeb is free and Open Source with commercial support and customization service provided by the developers 24x7

.. tip:: XtendWeb is tuned for speedy config generation and effecient high performance web server working

Features
---------

* worlds simplest nginx config wizard
* configuration curated for high performance and incorporates nginx best practices
* template based application configuration+ support application in sub-directories
* password protection setup by cpanel can be reused in nginx
* cpanel user can configure nginx for their application without editing any configuration
* Supports CentOS6 CentOS7 CloudLinux6 CloudLinux7 on x86_64 arch
* Multiple backends - Apache HTTPD, PHP-FPM, HHVM, ColdFusion/Java, Python, Ruby on Rails, NodeJS
* PHP-FPM multiple master setup and HHVM server run per user ( for the security conscious )
* Supports caching in proxy and FastCGI
* Google PageSpeed support
* limit_req, limit_conn support
* NAXSI Web Application Firewall - (mod_security via libmodsecurity support coming soon!)
* IPv6 support
* TLS(HTTPS) support
* HTTP/2 support
* Brotli Compression support
* GeoIP support
* Fast installation, upgrade and easy uninstall available via yum/rpm.
* High Available Webstack - csync2 config sync and unison file sync for nginX
* High Available SMTP service - PostFix backup MX automatically configured for all domains
* High Available Database (MariaDB/MySQL) - MySQL replication(master-master/galera) & tcp loadbalancing
* Clustering in the application layer(csync2,unison,rsync).Easy to troubleshoot and fix errors


.. toctree::
   :maxdepth: 2
   :caption: Installation & Basic Configuration

   installation
   migrating_from_nDeploy
   mod_remoteip
   brotli_compression
   http2

.. toctree::
   :maxdepth: 2
   :caption: Support & Development

   support
   project_sponsors
   nginx_friendly_web_hosts

.. toctree::
   :maxdepth: 2
   :caption:  Backends Setup

   HHVM
   PHP
   PYTHON_WSGI
   RUBY_RACK
   NodeJS
   Meteor
   ColdFusion_Java

.. toctree::
   :maxdepth: 2
   :caption: Administration & Monitoring

   XtendWeb_Administration
   Monitoring
   Logs

.. toctree::
   :maxdepth: 2
   :caption: XtendWeb Cluster

   cluster_architecture
   XtendWeb_cluster_setup
   Upgrade_cluster


* :ref:`search`
