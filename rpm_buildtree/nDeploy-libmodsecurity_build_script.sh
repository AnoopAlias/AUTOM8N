#!/bin/bash
#Author: Anoop P Alias

##Vars
MODSEC_VERSION="3.0"
MODSEC_RPM_ITER="1.el6"

rm -rf /opt/libmodsec
yum install gcc-c++ flex bison yajl yajl-devel curl-devel curl GeoIP-devel doxygen zlib-devel
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
