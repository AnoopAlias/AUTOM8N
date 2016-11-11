XtendWeb is version 4 of the nDeploy cPanel plugin

While the core ideas of nDeploy like template based config generation etc is reused in XtendWeb ,
XtendWeb is otherwise a complete rewrite of nDeploy .

The major changes in XtendWeb are

1. There are no AUTO and MANUAL mode in the user interface. Users are not allowed to edit nginx configuration
2. Use of the Jinja2 templates
3. Adding templates for specific users is supported in XtendWeb
4. Configuring application in sub-directory is suppoted

These changes were made on careful analysis of end user feedback. A cpanel user never care
for manually editing nginx config( Users are less technical in general ) .

Because of this XtendWeb User Interface is more intuitive

Instructions for upgrading from nDeploy
----------------------------------------

XtendWeb templates and domain-data settings are not backward compatible
So the right way to upgrade from nDeloy is completly removing nDeploy and setting up XtendWeb as a new installation

1. Completly remove the old plugin
::

  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh disable
  yum remove nginx-nDeploy nDeploy
  rm -rf /etc/nginx /opt/nDeploy

.. tip:: removing /etc/nginx and /opt/nDeploy is a crucial step as otherwise the old config files may interfere with the new template system.

2. Follow http://xtendweb.gnusys.net/installation.html for a fresh installation


Contact ops@gnusys.net for commercial upgrade support.
