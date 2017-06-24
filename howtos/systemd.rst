systemd and related stuff
============================

Spawning multiple php-fpm masters using systemd socket activation
----------------------------------------------------------------------

`XtendWeb <http://xtendweb.gnusys.net/>`_  being a nginx addon for cPanel and used in environment where user level seperation of web data is a requirement needed a way to run multiple php-fpm master process  .The primary concern for such a system is the requirement of a
process control manager like supervisord to manage the master php-fpm process  for all the users and all the different
php version that a user may switch to.

systemd provided a neat solution for this .

The reference for this is

https://wiki.php.net/rfc/socketactivation

http://thanatos.be/2014/04/12/php-fpm-ondemand.html

While the solutions mentioned above are for a system that mostly needs a single or a few such process to be spawned .I have
used systemd's templating ability for service and socket units to make the solution scale for all users and if required for multiple versions
It does require a third party script to control systemd and create the php-fpm config file ;which in my case was done by
the XtendWeb cPanel nginx plugin

So here is the config
1. Create the systemd socket template /usr/lib/systemd/system/CPANELPHP56@.socket
::

  [Socket]
  ListenStream=/opt/cpanel/ea-php56/var/run/%i.sock
  SocketMode=0660
  SocketUser=%i
  SocketGroup=nobody

  [Install]
  WantedBy=sockets.target

2. Create the systemd service template /usr/lib/systemd/system/CPANELPHP56@.service
Note that the socket and service names must match
::

  [Service]
  User=%i
  Group=nobody
  Environment="FPM_SOCKETS=/opt/cpanel/ea-php56/var/run/%i.sock=3"
  ExecStart=/opt/cpanel/ea-php56/usr/sbin/php-fpm --prefix=/opt/cpanel/ea-php56 --fpm-config=/opt/nDeploy/secure-php-fpm.d/%i.conf
  KillMode=process

Once this is done the only requirement is create the php-fpm config file at /opt/nDeploy/secure-php-fpm.d/cpaneluser.conf

Start the socket by
::

  systemctl enable CPANELPHP56@myuser.socket
  systemctl start CPANELPHP56@myuser.socket

You can see that systemd starts the socket and when a request comes to the socket for the first time ; it will spawn the corresponding
service .

The `Environment="FPM_SOCKETS=/opt/cpanel/ea-php56/var/run/%i.sock=3"` is a requirement as otherwise the php-fpm service will try
to bind to the socket which will then fail. with the above variable set php-fpm will just reuse the socket

A downside of the above setup is that unused master process are not terminated . We can use a cron job to achieve this or just
leave the process idling there.


mount local or remote filesystems using systemd
-----------------------------------------------------

In this example I will describe how systemd can be used to mount remote NFS or CIFS in an ondemand automatic way

This is similar to socket activated service . We define a automount point that when accessed mount a filesytem using details
mentioned in a corresponding mount unit file.

::

  # cat /etc/systemd/system/media-backup.automount
  [Unit]
    Description=Remote cifs backup mount script
    Requires=network-online.target
    After=network-online.service

  [Automount]
    Where=/media/backup
    TimeoutIdleSec="300s"

  [Install]
    WantedBy=multi-user.target

Note that the automount file conveniently omits what is to be mounted and how etc as this part must be defined in the
corresponding mount unit file. Note also the peculiarity in the name of the unit file . It must be named
media-backup.automount as it is mounting to /media/backup. Similarly if you are mounting to /a/b/c, the file must be
named a-b-c.automount

Now lets see the corresponding mount unit file that is called by the automount
::

  # cat /etc/systemd/system/media-backup.mount
  [Unit]
    Description=Remote cifs backup mount script
    Requires=network-online.target
    After=network-online.service

  [Mount]
    What=//remoteshare.your-domain.com/backup
    Where=/media/backup
    Options=username=xyz,password=mysecurepass,rw
    Type=cifs

  [Install]
    WantedBy=multi-user.target

The mount unit must be named the same as the automount unit .You can also see that since the CIFS needs network service
to be up and running to connect; the unit file takes care of this requirement using the After= option
