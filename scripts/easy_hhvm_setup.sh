#!/bin/bash
#Author: Anoop P Alias

# HHVM_RPM_LOCATION="http://mirrors.linuxeye.com/hhvm-repo/7/x86_64/hhvm-3.15.3-1.el7.centos.x86_64.rpm"
HHVM_RPM_LOCATION="http://dev.sc-networks.com/centos/7/x86_64/hhvm/hhvm-3.21.3-1.x86_64.rpm"


osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
if [ ${osversion} -le 6 ];then
  echo -e '\e[93m XtendWeb HHVM setup needs CentOS7 or CloudLinux7 as the OS \e[0m'
else
  yum -y install epel-release
  yum -y install libc-client-2007f cpp gcc-c++ cmake git psmisc {binutils,boost,jemalloc,numactl}-devel {ImageMagick,sqlite,tbb,bzip2,openldap,readline,elfutils-libelf,gmp,lz4,pcre}-devel
  yum -y install lib{xslt,event,yaml,vpx,png,zip,icu,mcrypt,memcached,cap,dwarf}-devel {unixODBC,expat}-devel lib{edit,curl,xml2,xslt}-devel glog-devel oniguruma-devel ocaml gperf
  yum -y install enca libjpeg-turbo-devel openssl-devel make
  yum -y install ${HHVM_RPM_LOCATION}
  /opt/nDeploy/scripts/update_backend.py add HHVM hhvm-3.15 systemd
  ln -s /usr/bin/hhvm /usr/local/bin/hhvm
  grep "hhvm_ghost_hunter.sh" /etc/crontab || echo "0 */6 * * * bash /opt/nDeploy/scripts/hhvm_ghost_hunter.sh" >> /etc/crontab
  systemctl restart crond
  echo -e '\e[93m ::WARNING:: Using binary HHVM from third party software mirrors \e[0m'
  echo -e '\e[93m HHVM setup : OK \e[0m'
fi
