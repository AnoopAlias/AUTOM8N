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

Automatic selection of template based on application detection
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

A very IMPORTANT thing to note here is that auto_config.py is doing an educated guess work
and determining the application that is installed .
It MAY NOT! be always accurate . The administrator must be aware of this .
Of course, any change made by the auto_config can be reverted by the end user
or the admin from the cPanel plugin UI.

Adding more application templates
--------------------------------------------
Application templates provides end users with drop down list of templates that generate a vhost application configuration.
The rpm provides a set of templates ; but admins can extend this by adding more

::

[root@master conf]# /opt/nDeploy/scripts/update_profiles.py
usage: update_profiles.py [-h]
                          action user scope backend_category file_name
                          application_description_in_doublequotes
update_profiles.py: error: too few arguments



Upgrading XtendWeb and nginx
----------------------------

nDeploy-nginx is mated with a phusion passenger ruby gem .
So we don't encourage unmanned upgrades and have therefore set enable=0 in the yum repository .
The upgrade must be done manually by running the following commands
::

  yum -y install https://github.com/AnoopAlias/nDeploy/raw/master/nDeploy-release-centos-1.0-3.noarch.rpm
  yum --enablerepo=ndeploy install nginx-nDeploy nDeploy
  #For setups using Phusion Passenger app server
  /usr/nginx/scripts/nginx-passenger-setup.sh
  #For upgrading PHP application server(additional packages are to upgraded via yum)
  /opt/nDeploy/scripts/easy_php_setup.sh

Temporarily disable the plugin
-------------------------------

  ``/opt/nDeploy/scripts/cpanel-nDeploy-setup.sh disable``

Uninstall the plugin
---------------------

::

  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh disable
  yum remove nginx-nDeploy nDeploy

Building nginx-nDeploy from source
-----------------------------------

XtendWeb is a collection of scripts and contains no binary file.
nginx-nDeploy is distributed as a binary application .

While using the XtendWeb RPM repository is the easiest and fastest way to get XtendWeb on your server . You may sometimes wish to compile your own RPM's

The reason why one may wish to do this is

1. Add /extend nginX with more plugins
2. If you don't trust the nginX binary compiled on our server.
3. You notice an error and wish to debug nginX . https://www.nginx.com/resources/wiki/start/topics/tutorials/debugging/ , which requires that you compile Nginx with the –with-debug flag .
4. For the fun (and knowledge) of doing it

The instructions for creating your own nginX rpms are listed below. Run the following on your cPanel server
::

  git clone https://github.com/AnoopAlias/XtendWeb.git
  cd XtendWeb/rpm_buildtree/
  #Open nDeploy-nginx_build_script.sh in a text editor
  #The line starting with ./configure --prefix=/etc/nginx
  #is what you have to modify to add or remove configure arguments
  # comment out the line starting with rsync -av nginx-nDeploy-*
  root@cpanel [~/nDeploy/rpm_buildtree]# ./nDeploy-nginx_build_script.sh $OSVERSION where OSVERSION=6/7

  It will take some time to build . Once this is complete you will have the nginx-nDeploy rpm inside nginx-pkg- folder . which you can install using rpm -Uvh command


.. disqus::
