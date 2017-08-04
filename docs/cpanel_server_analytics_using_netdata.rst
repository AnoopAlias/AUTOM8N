cPanel server analytics using netdata
=========================================

XtendWeb provides easy installation of netdata ( https://github.com/firehol/netdata ) which provides a sysadmin unparalleled insights, in real-time, of everything happening on the system using modern interactive web dashboards.

netdata is fast and efficient, designed to permanently run on all systems (physical & virtual servers, containers, IoT devices), without disrupting their core function.


To install and configure netdata on cPanel/WHM server
::

  /opt/nDeploy/scripts/easy_netdata_setup.sh


Please enter a secure password for the netdata user when prompted by the script

Oce setup , you can access netdata from the URL :  https://servers-FQDN/netdata

Apart from system vitals you will be monitoring Apache httpd, XtendWeb nginx, mysql and redis

To monitor exim and dovecot see sections below


Monitor exim using netdata
------------------------------------------

If you need to monitor Exim queue , do the following to enable netdata to monitor exim
::


  1. Login to WHM

  2. Under Home »Service Configuration »Exim Configuration Manager click on "Advanced Editor"

  3. Under "Section: CONFIG" click on  "[+] Add additional configuration setting"

  4.From the drop down select "queue_list_requires_admin" and set its value to flase

  5. Click "Save" at the bottom

  6. Restart netada using command systemctl restart netdata || service netdata restart


Monitor Dovecot using netdata
-----------------------------------

::

  cp -p /var/cpanel/templates/dovecot2.2/main.default /var/cpanel/templates/dovecot2.2/main.local

Edit the file and add the lines marked with ++ extra
::

  # Edit and add following under heading below :
   # Quota support must be enabled globally for the quota-status
   # service to work
   mail_plugins = quota quota_clone [% IF fts_support %]fts fts_solr[% END %]
   ++ mail_plugins = $mail_plugins stats

  ##
  ## IMAP specific settings
  ##


   protocol imap {
   # Support for dynamically loadable plugins. mail_plugins is a space separated
   # list of plugins to load.
   ...
   .....
   ++ mail_plugins = $mail_plugins imap_stats
   #mail_plugin_dir = /usr/lib/dovecot/imap
   ..
   ...
   }



::

  #Add below lies with ++ above section Dictionary server settings

  ++ service stats {
  ++  inet_listener {
  ++    address = 127.0.0.1
  ++    port = 24242
  ++    }
  ++  }
  ##
  ## Dictionary server settings
  ##

  # Dictionary can be used by some plugins to store key=value lists.
  # Currently this is only used by dict quota backend. The dictionary can be
  # used either directly or though a dictionary server. The following dict block
  # maps dictionary names to URIs when the server is used. These can then be


Once done rebuild dovecot conf and restart dovecot
::

  /scripts/builddovecotconf
  /scripts/restartsrv dovecot

Restart netdata so that it can pick up dovecot monitoring
::

  systemctl restart netdata || service netdata restart
