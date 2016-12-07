Setting up HHVM
================

HHVM manages new connections in threads of single process unlike PHP-FPM that handles new connections
by forking a new process . So unlike PHP-FPM there is no process pool in HHVM

XtendWeb support 2 modes of HHVM backend .

Seperate HHVM process for each user managed by systemd( CentOS7/CloudLinux7 required)
--------------------------------------------------------------------------------------

::

  yum -y install epel-release
  yum install cpp gcc-c++ cmake git psmisc {binutils,boost,jemalloc,numactl}-devel {ImageMagick,sqlite,tbb,bzip2,openldap,readline,elfutils-libelf,gmp,lz4,pcre}-devel lib{xslt,event,yaml,vpx,png,zip,icu,mcrypt,memcached,cap,dwarf}-devel {unixODBC,expat}-devel lib{edit,curl,xml2,xslt}-devel glog-devel oniguruma-devel ocaml gperf enca libjpeg-turbo-devel openssl-devel make -y
  yum -y install http://mirrors.linuxeye.com/hhvm-repo/7/x86_64/hhvm-3.15.2-1.el7.centos.x86_64.rpm
  # Above command is based on current version of hhvm at https://github.com/facebook/hhvm/wiki/Prebuilt-Packages-on-Centos-7.xhttps://github.com/facebook/hhvm/wiki/Prebuilt-Packages-on-Centos-7.x
  #Register the HHVM backend in XtendWeb
  /opt/nDeploy/scripts/update_backend.py add HHVM hhvm-3.15 systemd
  # Add a cron job to stop unused HHVM process to be run every 6 hours
  echo "0 */6 * * * bash /opt/nDeploy/scripts/hhvm_ghost_hunter.sh" >> /etc/crontab



Single HHVM process running as nobody user
------------------------------------------------------
Use HHVM running as individual user whenever possible. HHVM running as nobody user is not recommended for shared hosting

#. Install HHVM as per https://github.com/facebook/hhvm/wiki/Prebuilt-Packages-on-Centos-7.x
#. Setup HHVM as an XtendWeb backend app server

::

  cp /opt/nDeploy/conf/hhvm_nobody_server.ini /etc/hhvm/server.ini
  mkdir /var/log/hhvm/
  chown nobody:nobody /var/log/hhvm/
  mkdir /var/run/hhvm/
  chown nobody:nobody /var/run/hhvm/

  edit /usr/lib/systemd/system/hhvm.service and change --user hhvm to --user nobody

  systemctl enable hhvm
  systemctl start hhvm

  You can check hhvm status using
  systemctl status hhvm

  Register the HHVM backend in XtendWeb
  /opt/nDeploy/scripts/update_backend.py add HHVM_NOBODY hhvm-3.15 /var/run/hhvm/hhvm.sock

.. disqus::
