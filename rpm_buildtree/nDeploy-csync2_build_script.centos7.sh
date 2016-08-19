#!/bin/bash
CSYNC2_VERSION="2.0"
CSYNC2_RPM_ITER="5.el7"

yum install librsync gnutls sqlite librsync-devel gnutls-devel sqlite-devel
rm -rf csync2-*
rm -f nDeploy-csync2-pkg-centos7/usr/sbin/csync2*
rm -f nDeploy-csync2-pkg-centos7/*.rpm
wget http://oss.linbit.com/csync2/csync2-${CSYNC2_VERSION}.tar.gz
tar -xvzf csync2-${CSYNC2_VERSION}.tar.gz
cd csync2-${CSYNC2_VERSION}
./configure --prefix=/usr --sysconfdir=/etc/csync2 --localstatedir=/var
make install DESTDIR=../nDeploy-csync2-pkg-centos7
cd ../nDeploy-csync2-pkg-centos7
mkdir -p var/backups/csync2
mkdir -p var/lib/csync2
fpm -s dir -t rpm -C ../nDeploy-csync2-pkg-centos7 --vendor "PiServe Technologies" --version ${CSYNC2_VERSION} --iteration ${CSYNC2_RPM_ITER} -a $(arch) -m info@piserve.com -e --description "nDeploy custom csync2 package" --url http://piserve.com --conflicts csync2 -d librsync -d gnutls -d sqlite -d sqlite-devel --after-install ../after_csync2_install --before-remove ../after_csync2_uninstall --name csync2-nDeploy .
rsync -av *.rpm root@rpm.piserve.com:/home/gnusys/public_html/CentOS/7/x86_64/
