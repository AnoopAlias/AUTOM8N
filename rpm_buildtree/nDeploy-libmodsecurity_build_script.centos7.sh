#!/bin/bash
#Author: Anoop P Alias

##Vars
MODSEC_VERSION="3.0"
MODSEC_RPM_ITER="3.el7"

rm -rf ModSecurity*
yum install gcc-c++ flex bison yajl yajl-devel curl-devel curl GeoIP-devel doxygen zlib-devel pcre-devel
git clone https://github.com/SpiderLabs/ModSecurity
cd ModSecurity
git checkout -b v3/master origin/v3/master
sh build.sh
git submodule init
git submodule update
./configure --prefix=/opt/nDeploy-libmodsecurity
make DESTDIR=$(pwd)/tempo install
cd tempo

fpm -s dir -t rpm -C ../tempo --vendor "Anoop P Alias" --version ${MODSEC_VERSION} --iteration ${MODSEC_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com -e --description "nDeploy custom libmodsecurity package" --url https://github.com/SpiderLabs/ModSecurity -d libcurl -d GeoIP -d yajl -d libxml2 --name libmodsecurity-nDeploy .
rsync -av libmodsecurity-nDeploy-* root@gnusys.net:/usr/share/nginx/html/CentOS/7/x86_64/
