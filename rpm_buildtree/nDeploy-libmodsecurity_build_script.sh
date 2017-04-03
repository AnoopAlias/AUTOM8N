#!/bin/bash
#Author: Anoop P Alias

##Vars
MODSEC_VERSION="3.0"
MODSEC_RPM_ITER="1.el6"

rpm --import https://linux.web.cern.ch/linux/scientific6/docs/repository/cern/slc6X/i386/RPM-GPG-KEY-cern
wget -O /etc/yum.repos.d/slc6-devtoolset.repo https://linux.web.cern.ch/linux/scientific6/docs/repository/cern/devtoolset/slc6-devtoolset.repo
yum install devtoolset-2-gcc-c++ devtoolset-2-binutils

yum install https://www.softwarecollections.org/en/scls/praiskup/autotools/epel-6-x86_64/download/praiskup-autotools-epel-6-x86_64.noarch.rpm
yum install autotools-latest
scl enable autotools-latest bash
scl enable devtoolset-2 bash



rm -rf /opt/libmodsec ModSecurity
yum install gcc-c++ flex bison yajl yajl-devel curl-devel curl GeoIP-devel doxygen zlib-devel pcre-devel
git clone https://github.com/SpiderLabs/ModSecurity
cd ModSecurity
git checkout -b v3/master origin/v3/master
sh build.sh
git submodule init
git submodule update
./configure --prefix=/opt/nDeploy-libmodsecurity
make DESTDIR=/opt/libmodsec install
cd /opt/libmodsec

fpm -s dir -t rpm -C ../libmodsec --vendor "Anoop P Alias" --version ${MODSEC_VERSION} --iteration ${MODSEC_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com -e --description "nDeploy custom libmodsecurity package" --url https://github.com/SpiderLabs/ModSecurity -d libcurl -d GeoIP -d yajl -d libxml2 --name libmodsecurity-nDeploy .
rsync -av libmodsecurity-nDeploy-* root@gnusys.net:/usr/share/nginx/html/CentOS/6/x86_64/
