Simpler reseller resource control
=======================================

Simpler is an alternative to cloudLinux . Simpler use systemd available in modern system to offer resource control.
The adavantages of simpler are

1. No need of a custom kernel

2. Resource isolation at Reseller level ,instead of user level

3. No additional software is required

4. Future proof as Simpler can follow future development trends in Kernel and Systemd without additional patching

5. And the best of all - Its simple and straightforward - Simplicity is the ultimate sophistication

How does simpleR work
------------------------
Simpler needs the php-fpm management system provided by https://xtendweb.gnusys.net/

XtendWeb forks a seperate PHP-FPM/HHVM  master process for each user (did we say its more secure too?) and XtendWeb
scripts automatically assign the process to a slice named after the reseller . The slice is a systemd unit that can have
resource controls using cgroup. In short you can view all PHP-FPM process/HHVM process running under a reseller as a single entity
and manage its resource simply by editing the reseller resource from the WHM User Interface

FAQ
------
1. Why are you not providing user level resource control

  In fact this is more easier than doing it at the reseller level. We thought reseller level control is more apt.
  You can say like all accounts under reseller x use 4 GB of RAM and 1/2 of the processing power .
  Its more easy to visualize and manage

2. Why only php-fpm?. Cant you manage Apache httpd,mysql, nginx etc?

   Sure why not . Each process in a systemd managed system can have resource limit . We feel that php-fpm will be the culprit when things go bad.
   Please see examples below on how you can set a upper limit to resource used by httpd,mysql etc.

3. Does this work with Apache httpd?

   Yes it works with apache httpd as well . XtendWeb php-fpm system is integrated with apache httpd and users are provided
   with the php-fpm selector plugin from which they can manage php version on a per website basis.


4. Why is Simpler Free

   Simpler is bundled along with https://xtendweb.gnusys.net/ . Together with Simpler,XtendWeb and XtendWeb cluster it offers a webhost or enterprise
   to have a great , stable ,high available and scalable hosting infrastructure . The software is all free and open source .
   But all support ,Installation assistance etc is commercial. GNUSYS is a service centric company and we charge only for the support services provided and not the product




Installation
---------------------

.. tip:: Simpler setting must be viewed as a safe upper limit for reseller resource usage . For example you can say that reseller x cannot consume more than 75% of memory and CPU.
         Setting very low limits on high end servers will only give you unhappy users and wasted resource . At the end of the day server is for serving not limiting !


.. tip:: Instead of limiting the resource you can scale the Websites to multiple servers using XtendWeb cluster . Assuming that each sever can handle 128 PHP process ,adding a
         new server to XtendWeb cluster will add another 128 PHP process capable server and allow your website to be served by 256 PHP process via DNS load balancing.

Simpler needs systemd .So you will need CentOS7 or RHEL7 .The php-fpm management is provided by XtendWeb so you will need XtendWeb
installed as well . You dont need to switch to native nginx.But we urge that you try the native nginx feature as well of XtendWeb .


1. Install XtendWeb : https://xtendweb.gnusys.net/docs/installation_standalone.html

2. Enable secure PHP-FPM
::

  /opt/nDeploy/scripts/init_backends.py secure-php

3. Enable httpd-php ( this enables Apache httpd to use php-fpm )
::

  /opt/nDeploy/scripts/init_backends.py httpd-php-install

4. Autofix configuration
::

  /opt/nDeploy/scripts/attempt_autofix.sh

5. Install SimpleR WHM plugin
::

  yum --enablerepo=ndeploy install simpler-nDeploy

Installation is complete and you can manage reseller resources from WHM >> Home »Plugins >> SimpleR Reseller Resource

Default resource
-------------------

The default resource a reseller gets on creation in WHM is controlled by the file
::

  # cat /opt/nDeploy/conf/simpler_resources.j2
  [Unit]
  Description={{ OWNER }} Slice
  DefaultDependencies=no
  Before=slices.target

  [Slice]
  CPUShares=1024
  MemoryLimit=4G
  BlockIOWeight=1000
  # CPUWeight=200
  # MemoryHigh=2G
  # IOWeight=200

If you need a different set of values do
::

  cp -p /opt/nDeploy/conf/simpler_resources.j2 /opt/nDeploy/conf/simpler_resources_local.j2 # Adjust simpler_resources_local.j2 accordingly


Tools to view resource usage
----------------------------------

Tools are provided by systemd

To view reseller slice.
::

  # systemctl status root.slice
  ● root.slice - root Slice
     Loaded: loaded (/etc/systemd/system/root.slice; static; vendor preset: disabled)
     Active: active since Fri 2017-05-12 07:12:17 UTC; 2h 21min ago
     Memory: 164.7M (limit: 250.0M)
     CGroup: /root.slice
             ├─CPANELPHP70@godisgreat.service
             │ └─31361 php-fpm: master process (/opt/nDeploy/secure-php-fpm.d/godisgreat.conf)
             └─ndeploy_hhvm@godisgreat.service
               └─30776 /usr/local/bin/hhvm --config /opt/nDeploy/hhvm.d/godisgreat.ini --user godisgreat --mode daemon

  May 12 07:16:02 li1311-27.members.linode.com hhvm[30776]: [Fri May 12 07:16:02 2017] [hphp] [30776:7f90c1325580:0:000056] [] BootStats: xmlInitParser = 0ms wall, 0ms cpu, 0 MB RSS
  May 12 07:18:37 li1311-27.members.linode.com php-fpm::godisgreat[31361]: [NOTICE] [pool godisgreat] 'user' directive is ignored when FPM is not running as root
  May 12 07:18:37 li1311-27.members.linode.com php-fpm[31361]: [NOTICE] [pool godisgreat] 'user' directive is ignored when FPM is not running as root
  May 12 07:18:37 li1311-27.members.linode.com php-fpm::godisgreat[31361]: [NOTICE] [pool godisgreat] 'group' directive is ignored when FPM is not running as root
  May 12 07:18:37 li1311-27.members.linode.com php-fpm[31361]: [NOTICE] [pool godisgreat] 'group' directive is ignored when FPM is not running as root
  May 12 07:18:37 li1311-27.members.linode.com php-fpm::godisgreat[31361]: [NOTICE] using inherited socket fd=3, "/opt/cpanel/ea-php70/root/var/run/godisgreat.sock"
  May 12 07:18:37 li1311-27.members.linode.com php-fpm[31361]: [NOTICE] using inherited socket fd=3, "/opt/cpanel/ea-php70/root/var/run/godisgreat.sock"
  May 12 07:18:37 li1311-27.members.linode.com php-fpm::godisgreat[31361]: [NOTICE] fpm is running, pid 31361
  May 12 07:18:37 li1311-27.members.linode.com php-fpm::godisgreat[31361]: [NOTICE] ready to handle connections
  May 12 07:18:37 li1311-27.members.linode.com php-fpm::godisgreat[31361]: [NOTICE] systemd monitor interval set to 10000ms

To view which reseller is consuming more resource
::

  systemd-cgtop

  Path                                                                                                                                               Tasks   %CPU   Memory  Input/s Output/s

  /                                                                                                                                                    106    1.8   676.8M        -        -
  /user.slice                                                                                                                                           10    1.2    87.5M        -        -
  /system.slice                                                                                                                                         50    0.5   158.7M        -        -
  /root.slice                                                                                                                                            2    0.0   164.7M        -        -
  /root.slice/CPANELPHP70@godisgreat.service                                                                                                             1      -        -        -        -
  /root.slice/ndeploy_hhvm@godisgreat.service                                                                                                            1      -        -        -        -

Note that the above gives resource usage on a per process level and also at the reseller level. Look for resellername.slice for the reseller level usage


To know more about systemd-resource-control
::

  # man systemd.resource-control


Limit httpd resource
-------------------------

Since dynamic page is served by php-fpm . Apache httpd is left with dealing mostly static pages and other web server jobs .
This does not cause much issues unless you are under an attack etc. In such situation you can place an upper limit to resource
that can be used by Apache httpd

::

  # systemctl status httpd.service
  ● httpd.service - Apache web server managed by cPanel EasyApache
     Loaded: loaded (/etc/systemd/system/httpd.service; enabled; vendor preset: disabled)
     Active: active (running) since Fri 2017-05-12 07:01:15 UTC; 3h 45min ago
   Main PID: 27720 (httpd)
     CGroup: /system.slice/httpd.service
             ├─ 5858 /usr/local/cpanel/3rdparty/bin/perl /usr/local/cpanel/bin/leechprotect
             ├─ 5859 /usr/sbin/httpd -k start
             ├─ 5860 /usr/sbin/httpd -k start
             ├─ 5861 /usr/sbin/httpd -k start
             ├─ 5862 /usr/sbin/httpd -k start
             ├─ 5863 /usr/sbin/httpd -k start
             ├─ 6117 /usr/sbin/httpd -k start
             └─27720 /usr/sbin/httpd -k start

  May 12 07:01:14 li1311-27.members.linode.com systemd[1]: Starting Apache web server managed by cPanel EasyApache...
  May 12 07:01:15 li1311-27.members.linode.com systemd[1]: PID file /run/apache2/httpd.pid not readable (yet?) after start.
  May 12 07:01:15 li1311-27.members.linode.com systemd[1]: Started Apache web server managed by cPanel EasyApache.

  vi /etc/systemd/system/httpd.service
  # Add below settings under the [Service] section

  CPUShares=1024
  MemoryLimit=8G
  BlockIOWeight=1000

You can follow the same procedure and put a upper limit to resource used by mysql by editing /etc/systemd/system/mysql.service


.. tip:: Did you know that the XtendWeb plugin you installed for Simpler can serve contents using the highly effecient nginx web server ?
         This is something you must try out instead of limiting resource used by Apache httpd


To view systemd config loaded
---------------------------------

Run following command
::

  systemctl cat CPANELPHP56@cpaneluser.service  # Assuming php56 is used and user is cpaneluser


To view the cgroup tree
--------------------------

::

  systemd-cgls    # You will see a slice named aftereach reseller


Support?
----------

Please email ops@gnusys.net for commercial support . Anoop Alias (aka gnusys) can be hired for all kinds of sysadmin/DevOps job

Please contact : anoop@gnusys.net .
