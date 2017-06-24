Simple Resource controller
=======================================

SimpleR stands for Simple Resource isolator and use systemd in modern systems to isolate CPU/Memory/IO on a per process basis

SimpleR can also group php-fpm and HHVM application servers running under user to a reseller.slice and individually limit the resource at a reseller level

Highlights are:

1. No need of a custom kernel

2. Resource isolation at Reseller level ,instead of user level

3. Resource limit on a process level for Apache/Nginx/MySQL/PHP . A safety valve like setting

3. No additional software is required

4. Future proof as Simpler can follow future development trends in Kernel and Systemd without additional patching

5. And the best of all - Its simple and straightforward - Simplicity is the ultimate sophistication

How does simpleR work
------------------------

Application Limits - SimpleR drops in an additional resource limit under the [Service] section in systemd unit file to achieve resource limit
for Apache/Nginx/MySQL/PHP . These limit can act as a safety net ( pressure value!) in extreme cases and prevent a single service from using up entire server resources

User Limits - If PHP-FPM or HHVM process is run under user .Simpler can group the process to a reseller.slice and ensure each user is limited in terms of memory/CPU and IO.
This can come handy when an admin want to allocate low resources to certain scripts and prevent them from affecting useable resources of other users


Installation
---------------------


Simpler needs systemd .So you will need CentOS7 or RHEL7 .

1. Install SimpleR WHM plugin
::

  yum --enablerepo=ndeploy install simpler-nDeploy


Simpler will allow setting upper limits for computing resources used by httpd/nginx/mysql/php-fpm(xtendweb managed)


For user level resource isolation do the following

.. note:: Running php-fpm master process under user forbids it from chrooting. PHP process are thus able to access any files user has access to normally.
          Because of lack of chroot , run the following setup only on private VPS where all accounts belong to one user and are trusted.

2. Enable user level PHP-FPM master process
::

  /opt/nDeploy/scripts/init_backends.py secure-php

2.1. Enable httpd-php ( this enables Apache httpd to use the above php-fpm process )
::

  /opt/nDeploy/scripts/init_backends.py httpd-php-install

2.2. Autofix configuration
::

  /opt/nDeploy/scripts/attempt_autofix.sh


Default resource for user
----------------------------

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

  Path                                                     Tasks   %CPU   Memory  Input/s Output/s

  /                                                        106    1.8   676.8M        -        -
  /user.slice                                              10    1.2    87.5M        -        -
  /system.slice                                            50    0.5   158.7M        -        -
  /root.slice                                              2    0.0   164.7M        -        -
  /root.slice/CPANELPHP70@godisgreat.service               1      -        -        -        -
  /root.slice/ndeploy_hhvm@godisgreat.service              1      -        -        -        -

Note that the above gives resource usage on a per process level and also at the reseller level. Look for resellername.slice for the reseller level usage


To know more about systemd-resource-control
::

  # man systemd.resource-control


To view systemd config loaded
---------------------------------

Run following command
::

  systemctl cat CPANELPHP56@cpaneluser.service  # Assuming php56 is used and user is cpaneluser


To view the cgroup tree
--------------------------

::

  systemd-cgls    # You will see a slice named aftereach reseller
