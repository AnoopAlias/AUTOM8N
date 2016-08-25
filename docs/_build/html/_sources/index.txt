.. nDeploy documentation master file, created by
   sphinx-quickstart on Tue Aug  2 11:13:22 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

nDeploy
=======



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
* HTTP/2 support
* Fast installation, upgrade and easy uninstall available via yum
* High Available WebStack
* High Available SMTP service
* High Available Database (MariaDB/MySQL)

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
