#!/bin/bash
#Author: Anoop P Alias

HHVM_RPM_LOCATION="http://mirrors.linuxeye.com/hhvm-repo/7/x86_64/hhvm-3.15.3-1.el7.centos.x86_64.rpm"


osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
if [ ${osversion} -le 6 ];then
  echo "XtendWeb HHVM setup needs CentOS7 or CloudLinux7 as the OS"
else
  echo "Be Warned that you are using binary HHVM from mirrors.linuxeye.com - which XtendWeb project cannot guarentee"
  yum -y install epel-release
  yum install libc-client-2007f cpp gcc-c++ cmake git psmisc {binutils,boost,jemalloc,numactl}-devel {ImageMagick,sqlite,tbb,bzip2,openldap,readline,elfutils-libelf,gmp,lz4,pcre}-devel lib{xslt,event,yaml,vpx,png,zip,icu,mcrypt,memcached,cap,dwarf}-devel {unixODBC,expat}-devel lib{edit,curl,xml2,xs
  yum -y install ${HHVM_RPM_LOCATION}
  /opt/nDeploy/scripts/update_backend.py add HHVM hhvm-3.15 systemd
  echo "0 */6 * * * bash /opt/nDeploy/scripts/hhvm_ghost_hunter.sh" >> /etc/crontab
  echo "HHVM setup : OK"
fi
