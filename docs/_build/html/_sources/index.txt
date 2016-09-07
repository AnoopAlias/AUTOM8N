.. nDeploy documentation master file, created by
   sphinx-quickstart on Tue Aug  2 11:13:22 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

nDeploy
=======

.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/GPLv3_Logo.svg/320px-GPLv3_Logo.svg.png

Eliminate downtime, replace cPanel's Apache httpd Webstack with NGINX cluster, and horizontally scale your web applications.


.. tip:: neatly rpm packaged, nDeploy does not modify any files or configuration setup by cPanel other than httpd listening port

.. tip:: nDeploy is OpenSource and ready to fork on GitHub. No vendor lock-in and lesser bugs

Features
---------

* Supports CentOS6 CentOS7 CloudLinux6 CloudLinux7 on x86_64 arch
* Multiple backends - Apache HTTPD, PHP-FPM, HHVM, ColdFusion/Java, Python, Ruby on Rails, NodeJS
* Supports caching/conditional cache purging in proxy and FastCGI(ngx_cache_purge)
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
   mod_remoteip
   http_to_https_redirect
   brotli_compression
   http2

.. toctree::
   :maxdepth: 2
   :caption: Backends Setup

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

   nDeploy_Administration
   Monitoring
   Logs

.. toctree::
   :maxdepth: 2
   :caption: nDeploy Cluster

   cluster_architecture
   nDeploy_cluster_setup
   Upgrade_cluster

.. toctree::
   :maxdepth: 2
   :caption: Support

   support





* :ref:`search`
