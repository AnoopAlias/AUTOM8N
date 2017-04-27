Administration of XtendWeb plugin
=================================

The end user has a intutive UI for managing domains hosted on cPanel .

Sysadmins can manipulate server wide settings using various scripts accessible from commandline

Layer7(Application layer) DDOS mitigation
-----------------------------------------

::

  To deal with a server wide DDOS on http (application layer)
  Edit /etc/nginx/conf.d/http_settings.conf
  and uncomment the include line as mentioned

  # Uncomment following to enable DOS mitigation server wide
  # include /etc/nginx/conf.d/dos_mitigate.conf;

  nginx -s reload


Automatic fixing of most errors
--------------------------------

The following script rebuilds all config and restarts backend app servers

::

  /opt/nDeploy/scripts/attempt_autofix.sh


Managing default server settings
-----------------------------------------

The default config generation in XtendWeb is governed by
::

  /opt/nDeploy/conf/domain_data_default.yaml
  /opt/nDeploy/conf/domain_data_suspended.yaml (for suspended users)

You can change the default server setting by creating /opt/nDeploy/conf/domain_data_default_local.conf
::

  cp -p /opt/nDeploy/conf/domain_data_default.yaml /opt/nDeploy/conf/domain_data_default_local.yaml
  cp -p /opt/nDeploy/conf/domain_data_suspended.yaml /opt/nDeploy/conf/domain_data_suspended_local.yaml

Automatic selection of template based on application
---------------------------------------------------------------

The following script can detect the application installed in the webroot(only!) based on filenames

While cPanel users can always change the vhost configuration for nginX
anytime from their cPanel login
sometimes the server administrator want to automatically switch supporting applications
to be directly served by nginX instead of apache.
::

  /opt/nDeploy/scripts/auto_config.py CPANELUSER

does this.

The script works by checking the presence of certain files like for example the wp-config.php in case of wordpress and switches the profile accordingly
::

  root@cpanel [~]# cat /opt/nDeploy/conf/appsignatures.yaml
  PHP:
    '/wp-config.php': '5001.j2'
    '/libraries/joomla/version.php': '5002.j2'
    '/sites/default/settings.php': '5017.j2'
    '/app/etc/local.xml': '5003.j2'


Admin can update the appsignatures.yaml file with file names and the corresponding
profile that auto_config.py switch the domain to if the file exists.
The default list provided by us is not extensive.
Admins can also remove entries from the file above to negate auto-switching should there be a need for it .

  ``/opt/nDeploy/conf/auto_config.exclude``

if present and contain the CPANELUSERNAME in it will prevent auto switching of profiles
for any domain (addon,subdomain etc) of the cpanel user.
This is useful while running the auto_config script in a for loop over a list of
cpanel users and if the script should omit any user.
To make this all work
::

  1. Edit /opt/nDeploy/conf/appsignatures.yaml . Add or remove filenames (relative to document root) and the corresponding profile names to switch to should the file be present in document root

  2.Create a file named /opt/nDeploy/conf/auto_config.exclude and add any cpanelusername for which you wish to exclude auto_config. If the file is not present or is empty ;no user is excluded

  3.run

  for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1)
      do
          echo "Auto ConfGen:: $CPANELUSER" && /opt/nDeploy/scripts/auto_config.py $CPANELUSER
      done
      service nginx restart

The first time auto_config.py runs it will ask your preference of PHP version
that automatic switching should use.
On cpanel servers you can safely use the same version as the default installed PHP
as most of your domains will be running that version without issues

Adding application templates
--------------------------------------------
Application templates are a way of extending the plugin with dealing with more web applications and user specific
nginx config customization

Application templates can be distributed server wide or to specific users
Application templates can be created for an application in the document_root as well as a subdirectory

Distributing templates to all users
::

  /opt/nDeploy/scripts/update_profiles.py add root main PHP 5001.j2 "Wordpress"

Distributing templates for a subdirectory to all users
::

  /opt/nDeploy/scripts/update_profiles.py add root subdir PHP 5001_subdir.j2 "Wordpress in subdir"

Distributing template to a specific cpaneluser
::

  /opt/nDeploy/scripts/update_profiles.py add cpanelusername main PHP 5001.j2 "Wordpress"
  /opt/nDeploy/scripts/update_profiles.py add cpanelusername subdir PHP 5001_subdir.j2 "Wordpress in subdir"

In short the template registration has the following syntax
::

  /opt/nDeploy/scripts/update_profiles.py [add|del] [root|cpanelusername] [main|subdir] [backend] [templatefilename] [quoted description]

Templates use Python Jinja2 templating engine . But there isnt much template logic used to make application template
simpler for most users. You can check existing templates for the commonly used variables.

.. tip:: Open an issue at the github repo if you wish template for a commonly used application to be added



Adding Application servers or backends
---------------------------------------

XtendWeb supports php-fpm or hhvm via FastCGI , Other web/application servers like httpd,tomcat etc via Proxy .
Ruby/Python/NodeJs using the Phusion Passenger module

To register a backend use the follwoing command
::

  /opt/nDeploy/scripts/update_backend.py [add|del] backend_category backend_name backend_path


Upgrading XtendWeb and nginx
----------------------------

nDeploy-nginx is mated with a phusion passenger ruby gem .
So we don't encourage unmanned upgrades and have therefore set enable=0 in the yum repository .
The upgrade must be done manually by running the following commands
::

  yum -y install https://github.com/AnoopAlias/XtendWeb/raw/ndeploy4/nDeploy-release-centos-1.0-5.noarch.rpm
  yum --enablerepo=ndeploy upgrade
  #For setups using Phusion Passenger app server
  /opt/nDeploy/scripts/easy_passenger_setup.sh
  #For upgrading PHP application server(additional packages are to upgraded via yum)
  /opt/nDeploy/scripts/easy_php_setup.sh

XtendWeb cluster upgrade
----------------------------

On All slaves

::

  yum --enablerepo=ndeploy upgrade

On master


::

  yum --enablerepo=ndeploy upgrade
  cd /opt/nDeploy/conf/nDeploy-cluster
  ansible-playbook -i ./hosts cluster.yml


Migrating Xtendweb settings
--------------------------------
In case you are migrating the entire cPanel accounts to a new server .

1. Do the cPanel migration
2. Install Xtendweb on the new server
3. Edit the file /opt/nDeploy/scripts/migrate_xtendweb_settings.sh and change REMOTE_SERVER='ip.ip.ip.ip' with the remote servers IP address
4. Run the script /opt/nDeploy/scripts/migrate_xtendweb_settings.sh  #Input password of remote server whenever prompted


Temporarily disable the plugin
-------------------------------

  ``/opt/nDeploy/scripts/cpanel-nDeploy-setup.sh disable``

Uninstall the plugin
---------------------

::

  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh disable
  yum remove nginx-nDeploy nDeploy


.. disqus::
